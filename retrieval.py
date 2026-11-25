"""
Search over the index built by index.py. Shared by server.py (the search tool) and evaluate.py.

Two ways to rank chunks:
- vector:  cosine similarity between the question's Gemini embedding and each chunk's
- hybrid:  vector ranking fused with a BM25 keyword ranking (reciprocal rank fusion), which helps
           with exact terms the embedding can blur: CN codes (1804), article numbers, "GeoJSON"

Query vectors are cached in index/query_cache.json, so asking the same question twice costs one
embedding, not two (the free tier allows about 1,000 a day).
"""

import json
import math
import os
import re
from collections import Counter
from functools import lru_cache

import index

QUERY_CACHE = index.INDEX_DIR / "query_cache.json"
CORPUS_FILES = [doc["file"] for doc in index.CORPUS]
RRF_K = 60           # standard constant of reciprocal rank fusion
CANDIDATES = 50      # how deep each ranking goes before fusion


# ---------------------------------------------------------------- query embeddings

def _load_cache() -> dict:
    try:
        return json.loads(QUERY_CACHE.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


def embed_query(question: str) -> list[float]:
    cache = _load_cache()
    if question not in cache:
        cache[question] = index.embed_texts([question], "RETRIEVAL_QUERY")[0]
        QUERY_CACHE.write_text(json.dumps(cache), encoding="utf-8")
    return cache[question]


def embed_queries(questions: list[str]) -> dict[str, list[float]]:
    """Embed many questions in batches, skipping those already cached."""
    cache = _load_cache()
    todo = [q for q in dict.fromkeys(questions) if q not in cache]
    for start in range(0, len(todo), index.BATCH):
        batch = todo[start:start + index.BATCH]
        for question, vector in zip(batch, index.embed_texts(batch, "RETRIEVAL_QUERY")):
            cache[question] = vector
        QUERY_CACHE.write_text(json.dumps(cache), encoding="utf-8")
    return {q: cache[q] for q in questions}


# ---------------------------------------------------------------- chunks and keyword index

@lru_cache(maxsize=None)
def chunks(design: str) -> dict[str, dict]:
    """All chunks of a design by id, read from index/chunks_<design>.jsonl plus any added documents."""
    result = {}
    for path in [index.INDEX_DIR / f"chunks_{design}.jsonl", index.INDEX_DIR / f"added_{design}.jsonl"]:
        if path.exists():
            for line in path.read_text(encoding="utf-8").splitlines():
                chunk = json.loads(line)
                result[chunk["id"]] = chunk
    return result


def tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+(?:[./][a-z0-9]+)*", text.lower())


@lru_cache(maxsize=None)
def bm25_index(design: str):
    docs = {cid: tokens(c["embed_text"]) for cid, c in chunks(design).items()}
    df = Counter(t for toks in docs.values() for t in set(toks))
    avg = sum(len(t) for t in docs.values()) / max(len(docs), 1)
    return docs, df, avg


def base_only() -> bool:
    """EUDR_BASE_ONLY=1 searches only the original corpus, ignoring documents added with add_document.
    The evaluation uses it, so that its unanswerable questions stay unanswerable after the add-document demo."""
    return os.environ.get("EUDR_BASE_ONLY") == "1"


def bm25_rank(question: str, design: str, k1: float = 1.5, b: float = 0.75) -> list[str]:
    docs, df, avg = bm25_index(design)
    n, query = len(docs), set(tokens(question))
    allowed = set(CORPUS_FILES) if base_only() else None
    scores = {}
    for cid, toks in docs.items():
        if allowed and chunks(design)[cid]["file"] not in allowed:
            continue
        tf = Counter(toks)
        score = 0.0
        for term in query & tf.keys():
            idf = math.log(1 + (n - df[term] + 0.5) / (df[term] + 0.5))
            score += idf * tf[term] * (k1 + 1) / (tf[term] + k1 * (1 - b + b * len(toks) / avg))
        if score:
            scores[cid] = score
    return sorted(scores, key=scores.get, reverse=True)[:CANDIDATES]


# ---------------------------------------------------------------- search

def vector_rank(vector: list[float], design: str, n: int = CANDIDATES) -> list[tuple[str, float]]:
    where = {"file": {"$in": CORPUS_FILES}} if base_only() else None
    result = index.collection(design).query(query_embeddings=[vector], n_results=n, include=["distances"], where=where)
    return [(cid, 1 - d) for cid, d in zip(result["ids"][0], result["distances"][0])]


def search(question: str, design: str = index.DEFAULT_DESIGN, k: int = 5, hybrid: bool = False,
           vector: list[float] | None = None) -> list[dict]:
    """The k best chunks for a question, each with its citation and a score."""
    vector = vector if vector is not None else embed_query(question)
    ranked = vector_rank(vector, design)
    similarity = dict(ranked)
    if hybrid:
        fused = Counter()
        for rank, (cid, _) in enumerate(ranked):
            fused[cid] += 1 / (RRF_K + rank + 1)
        for rank, cid in enumerate(bm25_rank(question, design)):
            fused[cid] += 1 / (RRF_K + rank + 1)
        order = [cid for cid, _ in fused.most_common(k)]
    else:
        order = [cid for cid, _ in ranked[:k]]
    all_chunks = chunks(design)
    results = []
    for cid in order:
        chunk = dict(all_chunks.get(cid) or _from_chroma(cid, design))
        chunk["similarity"] = round(similarity.get(cid, 0.0), 3)
        results.append(chunk)
    return results


def _from_chroma(cid: str, design: str) -> dict:
    """A chunk stored only in ChromaDB (e.g. added by add_document in another process)."""
    got = index.collection(design).get(ids=[cid], include=["documents", "metadatas"])
    meta = got["metadatas"][0]
    return {"id": cid, "text": got["documents"][0], "covers": [meta["location"]], **meta}


def citation(chunk: dict) -> str:
    return f"{chunk['doc_title']}, {chunk['location']}"
