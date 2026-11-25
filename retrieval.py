"""
Retrieval over the saved index: dense (Gemini vectors), keyword (BM25) and
hybrid (both, merged with reciprocal rank fusion).

No re-embedding of the corpus happens here. Only the *query* is embedded, and
query vectors are cached in index/query_cache.json so repeated questions
(evaluation reruns) cost nothing.
"""

import json
import math
import re
from collections import Counter
from pathlib import Path

import index as ix

CACHE_FILE = ix.INDEX_DIR / "query_cache.json"
DEFAULT_MODE = "hybrid"  # decided by the hit-rate numbers in `main.py evaluate`
_state: dict = {}


def _cache() -> dict:
    if "cache" not in _state:
        try:
            _state["cache"] = json.loads(CACHE_FILE.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            _state["cache"] = {}
    return _state["cache"]


def query_vector(query: str) -> list[float]:
    cache = _cache()
    key = ix.digest(query)
    if key not in cache:
        cache[key] = ix.embed_query(query)
        CACHE_FILE.write_text(json.dumps(cache), encoding="utf-8")
    return cache[key]


def tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def reset() -> None:
    """Forget loaded chunks (call after add_document so new chunks are searchable)."""
    _state.pop("chunks", None)


def _load() -> dict:
    if "chunks" not in _state:
        got = ix.get_collection().get(include=["documents", "metadatas"])
        docs = []
        for cid, text, meta in zip(got["ids"], got["documents"], got["metadatas"]):
            docs.append({"id": cid, "text": text, **meta, "tokens": tokens(text)})
        df = Counter(t for d in docs for t in set(d["tokens"]))
        _state["chunks"] = {
            "docs": docs,
            "df": df,
            "avg_len": sum(len(d["tokens"]) for d in docs) / max(len(docs), 1),
        }
    return _state["chunks"]


def _public(doc: dict, score: float) -> dict:
    return {"id": doc["id"], "source": doc["source"], "location": doc["location"],
            "part": doc.get("part", ""), "text": doc["text"], "score": round(score, 4)}


def dense_search(query: str, k: int, source: str | None = None) -> list[dict]:
    col = ix.get_collection()
    where = {"source": source} if source else None
    res = col.query(query_embeddings=[query_vector(query)], n_results=k, where=where,
                    include=["documents", "metadatas", "distances"])
    return [{"id": i, "text": t, **m, "score": round(1 - d, 4)}
            for i, t, m, d in zip(res["ids"][0], res["documents"][0], res["metadatas"][0], res["distances"][0])]


def bm25_search(query: str, k: int, source: str | None = None) -> list[dict]:
    data = _load()
    n = len(data["docs"])
    q = tokens(query)
    scored = []
    for d in data["docs"]:
        if source and d["source"] != source:
            continue
        tf = Counter(d["tokens"])
        score = 0.0
        for t in q:
            if t not in tf:
                continue
            idf = math.log(1 + (n - data["df"][t] + 0.5) / (data["df"][t] + 0.5))
            denom = tf[t] + 1.5 * (1 - 0.75 + 0.75 * len(d["tokens"]) / data["avg_len"])
            score += idf * tf[t] * 2.5 / denom
        if score > 0:
            scored.append((score, d))
    scored.sort(key=lambda x: -x[0])
    return [_public(d, s) for s, d in scored[:k]]


def hybrid_search(query: str, k: int, source: str | None = None) -> list[dict]:
    pool = max(k * 4, 20)
    fused: dict[str, float] = {}
    by_id: dict[str, dict] = {}
    for results in (dense_search(query, pool, source), bm25_search(query, pool, source)):
        for rank, hit in enumerate(results, start=1):
            fused[hit["id"]] = fused.get(hit["id"], 0.0) + 1 / (60 + rank)
            by_id[hit["id"]] = hit
    top = sorted(fused, key=lambda i: -fused[i])[:k]
    return [{**by_id[i], "score": round(fused[i], 4)} for i in top]


def retrieve(query: str, k: int = 5, mode: str = DEFAULT_MODE, source: str | None = None) -> list[dict]:
    if mode == "dense":
        return dense_search(query, k, source)
    if mode == "bm25":
        return bm25_search(query, k, source)
    return hybrid_search(query, k, source)


def citation(hit: dict) -> str:
    return f"[{hit['source']}, {hit['location']}]"


def format_hits(hits: list[dict]) -> str:
    if not hits:
        return "No passages found."
    return "\n\n".join(f"{citation(h)}\n{h['text']}" for h in hits)
