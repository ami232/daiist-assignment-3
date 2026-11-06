import csv
import json
import re
import time
from pathlib import Path

import chromadb
import numpy as np
from google import genai
from google.genai import types
from rank_bm25 import BM25Okapi

from api_key import load_api_key
from index import INDEX_DIR, COLLECTION_NAME, MODEL, DIMENSIONS


QUESTIONS_PATH = Path("eval/questions.csv")
CHUNKS_PATH = Path("data/processed/chunks.json")
OUTPUT_DIR = Path("eval")

K_VALUES = [1, 3, 5]
CANDIDATE_K = 25
RRF_CONSTANT = 60


def tokenize(text):
    """Tokenize text for BM25."""
    return re.findall(r"[a-z0-9]+", text.lower())


def load_data():
    with QUESTIONS_PATH.open(
        encoding="utf-8", newline=""
    ) as f:
        questions = list(csv.DictReader(f))

    with CHUNKS_PATH.open(encoding="utf-8") as f:
        chunks = json.load(f)

    return questions, chunks


def expected_articles(question):
    """Convert CSV references into (source, article) pairs."""

    sources = [
        s.strip()
        for s in question["expected_source"].split(";")
    ]

    locations = [
        loc.strip()
        for loc in question["expected_location"].split(";")
    ]

    if len(sources) == 1:
        sources *= len(locations)

    if len(sources) != len(locations):
        raise ValueError(
            f"Invalid references for {question['id']}"
        )

    expected = set()

    for source, location in zip(sources, locations):
        match = re.fullmatch(
            r"Article\s+(\d+)", location
        )

        if not match:
            raise ValueError(
                f"Invalid article reference: {location}"
            )

        expected.add((source, int(match.group(1))))

    return expected


def embed_query(client, question):
    """Generate one query embedding with limited retries."""

    for attempt in range(5):
        try:
            response = client.models.embed_content(
                model=MODEL,
                contents=question,
                config=types.EmbedContentConfig(
                    output_dimensionality=DIMENSIONS
                ),
            )
            return response.embeddings[0].values

        except Exception as error:
            if "429" not in str(error) or attempt == 4:
                raise

            match = re.search(
                r"retry in ([\d.]+)s",
                str(error),
                re.IGNORECASE
            )

            delay = (
                float(match.group(1)) + 5
                if match
                else 65
            )

            print(
                f"Rate limit reached. Retrying in "
                f"{delay:.0f}s...",
                flush=True
            )
            time.sleep(delay)


def vector_search(collection, vector, k):
    results = collection.query(
        query_embeddings=[vector],
        n_results=k,
        include=["metadatas"]
    )

    return results["ids"][0]


def bm25_search(model, question, chunks, k):
    scores = model.get_scores(tokenize(question))

    ranking = np.argsort(scores)[::-1][:k]

    return [chunks[i]["id"] for i in ranking]


def hybrid_search(vector_ids, bm25_ids):
    """Combine rankings using Reciprocal Rank Fusion."""

    scores = {}

    for ranking in [vector_ids, bm25_ids]:
        for rank, chunk_id in enumerate(ranking, start=1):
            scores[chunk_id] = (
                scores.get(chunk_id, 0)
                + 1 / (RRF_CONSTANT + rank)
            )

    return sorted(
        scores,
        key=lambda cid: (-scores[cid], cid)
    )


def is_hit(result_ids, expected, chunk_lookup, k):
    """Check whether ALL required articles appear in top k."""

    retrieved = {
        (
            chunk_lookup[cid]["source"],
            chunk_lookup[cid]["article"]
        )
        for cid in result_ids[:k]
    }

    return int(expected.issubset(retrieved))


def evaluate_retrieval():
    questions, chunks = load_data()

    answerable = [
        q for q in questions
        if q["kind"] in ("single", "multi")
    ]

    chunk_lookup = {
        chunk["id"]: chunk for chunk in chunks
    }

    print(f"Loaded {len(chunks)} chunks.")
    print(f"Evaluating {len(answerable)} questions.")

    print("Preparing BM25 index...")

    tokenized_corpus = [
        tokenize(chunk["text"])
        for chunk in chunks
    ]

    bm25 = BM25Okapi(tokenized_corpus)

    db = chromadb.PersistentClient(
        path=str(INDEX_DIR)
    )

    collection = db.get_collection(
        name=COLLECTION_NAME
    )

    client = genai.Client(
        api_key=load_api_key()
    )

    details = []

    for index, question in enumerate(answerable, start=1):
        print(
            f"[{index}/{len(answerable)}] "
            f"{question['id']}: {question['question']}",
            flush=True
        )

        expected = expected_articles(question)

        started = time.perf_counter()

        # Only one Gemini query embedding per question.
        vector = embed_query(client, question["question"])

        vector_ids = vector_search(
            collection, vector, CANDIDATE_K
        )

        bm25_ids = bm25_search(
            bm25,
            question["question"],
            chunks,
            CANDIDATE_K
        )

        hybrid_ids = hybrid_search(
            vector_ids, bm25_ids
        )

        elapsed = time.perf_counter() - started

        row = {
            "id": question["id"],
            "kind": question["kind"],
            "seconds": round(elapsed, 3),
        }

        for method, ids in [
            ("vector", vector_ids),
            ("hybrid", hybrid_ids),
        ]:
            for k in K_VALUES:
                row[f"{method}_hit_{k}"] = is_hit(
                    ids, expected, chunk_lookup, k
                )

            row[f"{method}_top5"] = ";".join(
                f"{chunk_lookup[cid]['source']}:"
                f"{chunk_lookup[cid]['article']}"
                for cid in ids[:5]
            )

        details.append(row)

        # Reduce the chance of a temporary API rate limit.
        time.sleep(1)

    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

    details_path = OUTPUT_DIR / "retrieval_results.csv"

    with details_path.open(
        "w", newline="", encoding="utf-8"
    ) as f:
        writer = csv.DictWriter(
            f, fieldnames=details[0].keys()
        )
        writer.writeheader()
        writer.writerows(details)

    summary = {
        "total_questions": len(answerable),
        "methods": {},
    }

    print("\n" + "=" * 55)
    print("RETRIEVAL EVALUATION RESULTS")
    print("=" * 55)

    for method in ["vector", "hybrid"]:
        summary["methods"][method] = {}

        print(f"\n{method.upper()} SEARCH")

        for k in K_VALUES:
            key = f"{method}_hit_{k}"

            hits = sum(row[key] for row in details)
            rate = hits / len(details)

            summary["methods"][method][f"hit@{k}"] = rate

            print(
                f"Hit@{k}: {hits}/{len(details)} "
                f"({rate:.1%})"
            )

    summary["average_seconds_per_question"] = round(
        sum(row["seconds"] for row in details)
        / len(details), 3
    )

    summary_path = OUTPUT_DIR / "retrieval_summary.json"

    summary_path.write_text(
        json.dumps(summary, indent=2),
        encoding="utf-8"
    )

    print("\nFiles saved:")
    print(details_path)
    print(summary_path)

    return summary


if __name__ == "__main__":
    evaluate_retrieval()
