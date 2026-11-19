import csv
import sqlite3
from pathlib import Path

import numpy as np
from google import genai
from google.genai import types

from api_key import load_api_key
from vector_store import DB_PATH, DIMENSIONS, MODEL


ROOT = Path(__file__).resolve().parent


def search(query, k=5):
    """Return the k chunks with the highest cosine similarity to the query."""
    if k < 1 or not query.strip():
        raise ValueError("Provide a non-empty query and a positive k.")

    # Read the existing index without modifying it.
    db = sqlite3.connect(f"{DB_PATH.as_uri()}?mode=ro", uri=True)
    try:
        rows = db.execute(
            "SELECT id, source, page, text, vector FROM chunks ORDER BY id"
        ).fetchall()
    finally:
        db.close()

    if not rows:
        raise ValueError("The index is empty. Run main.py index first.")

    # Only the question needs a new embedding.
    with genai.Client(api_key=load_api_key()) as client:
        result = client.models.embed_content(
            model=MODEL,
            contents=f"task: question answering | query: {query.strip()}",
            config=types.EmbedContentConfig(output_dimensionality=DIMENSIONS),
        )

    query_vector = np.asarray(result.embeddings[0].values, dtype=np.float32)
    vectors = np.stack([np.frombuffer(row[4], dtype="<f4") for row in rows])

    # Cosine similarity compares the direction of each vector.
    norms = np.linalg.norm(vectors, axis=1) * np.linalg.norm(query_vector)
    if np.any(norms == 0):
        raise ValueError("Found a zero-length embedding.")

    scores = (vectors @ query_vector) / norms
    ranking = np.argsort(-scores, kind="stable")[:k]

    return [
        {
            "id": rows[i][0],
            "source": rows[i][1],
            "page": rows[i][2],
            "text": rows[i][3],
            "score": float(scores[i]),
        }
        for i in ranking
    ]


if __name__ == "__main__":
    with (ROOT / "eval" / "questions.csv").open(
        encoding="utf-8-sig", newline=""
    ) as file:
        question = next(row for row in csv.DictReader(file) if row["id"] == "q01")

    print(f"Question: {question['question']}\n")
    results = search(question["question"])

    for rank, hit in enumerate(results, start=1):
        print(f"{rank}. {hit['id']} | score: {hit['score']:.3f}")
        print(f"   {hit['text'][:180]}\n")

    expected_rank = next(
        (
            rank
            for rank, hit in enumerate(results, start=1)
            if hit["source"] == question["expected_source"]
            and str(hit["page"]) == question["expected_location"]
        ),
        None,
    )
    print(f"Expected page rank: {expected_rank or 'outside top 5'}")