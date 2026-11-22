"""
Search over index/, shared by server.py and evaluate.py.

- vector search: the query's Gemini embedding against a design's collection;
- hybrid search: vector + BM25 keyword ranks merged by reciprocal rank fusion,
  so exact strings (CAS numbers, INCI names, "Article 19") count as well.

Query vectors are cached in index/query_cache.json: the free tier counts every
embedded question, and the evaluation asks the same ones again and again.
"""

import json
import math
import re
from collections import Counter
from functools import lru_cache

from index import DEFAULT_DESIGN, INDEX, collection, embed

QUERY_CACHE = INDEX / "query_cache.json"
DEFAULT_K = 5
HYBRID = False  # chosen by hit rate: hybrid did not help (REPORT.md, Retrieval)
RRF_K = 60


def _load_cache() -> dict:
    return json.loads(QUERY_CACHE.read_text(encoding="utf-8")) if QUERY_CACHE.exists() else {}


_cache = _load_cache()


def query_vector(query: str) -> list[float]:
    key = query.strip()
    if key not in _cache:
        _cache[key] = embed([key], "RETRIEVAL_QUERY")[0]
        QUERY_CACHE.write_text(json.dumps(_cache), encoding="utf-8")
    return _cache[key]


def vector_search(query: str, k: int, design: str) -> list[dict]:
    res = collection(design).query(query_embeddings=[query_vector(query)], n_results=k,
                                   include=["documents", "metadatas", "distances"])
    return [{"id": i, "text": d, **m, "score": 1 - dist}
            for i, d, m, dist in zip(res["ids"][0], res["documents"][0], res["metadatas"][0], res["distances"][0])]


TOKEN = re.compile(r"[a-z0-9]+(?:[-/][a-z0-9]+)*")


def tokens(text: str) -> list[str]:
    return TOKEN.findall(text.lower())


@lru_cache(maxsize=None)
def _bm25(design: str, size: int):
    """BM25 statistics for a collection; rebuilt when its size changes."""
    data = collection(design).get(include=["documents", "metadatas"])
    docs = [Counter(tokens(t)) for t in data["documents"]]
    df = Counter(term for d in docs for term in d)
    avg = sum(sum(d.values()) for d in docs) / max(len(docs), 1)
    return data, docs, df, avg


def keyword_search(query: str, k: int, design: str, k1: float = 1.5, b: float = 0.75) -> list[dict]:
    data, docs, df, avg = _bm25(design, collection(design).count())
    n, q = len(docs), set(tokens(query))
    scores = []
    for i, d in enumerate(docs):
        length = sum(d.values())
        s = sum(math.log(1 + (n - df[t] + 0.5) / (df[t] + 0.5)) * d[t] * (k1 + 1)
                / (d[t] + k1 * (1 - b + b * length / avg)) for t in q if t in d)
        scores.append((s, i))
    top = sorted(scores, reverse=True)[:k]
    return [{"id": data["ids"][i], "text": data["documents"][i], **data["metadatas"][i], "score": s}
            for s, i in top if s > 0]


def search(query: str, k: int = DEFAULT_K, design: str = DEFAULT_DESIGN, hybrid: bool = HYBRID) -> list[dict]:
    """Top-k chunks for a query, each with source, location and text."""
    if not hybrid:
        return vector_search(query, k, design)
    pool = 4 * k
    fused: dict[str, dict] = {}
    for ranking in (vector_search(query, pool, design), keyword_search(query, pool, design)):
        for rank, hit in enumerate(ranking):
            item = fused.setdefault(hit["id"], {**hit, "score": 0.0})
            item["score"] += 1 / (RRF_K + rank + 1)
    return sorted(fused.values(), key=lambda h: -h["score"])[:k]


def format_results(hits: list[dict]) -> str:
    """What the search tool returns: numbered passages, each with its citation."""
    if not hits:
        return "No passages found in the corpus."
    return "\n\n".join(f"[{i}] {h['source']} | {h['location']}\n{h['text']}" for i, h in enumerate(hits, start=1))
