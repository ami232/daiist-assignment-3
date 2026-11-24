"""
Retrieval over the committed index, shared by server.py and evaluate.py.

    search(query, k=5, design="article", mode="hybrid", source=None) -> list[hit]

mode "dense"  : cosine similarity on Gemini embeddings (ChromaDB).
mode "hybrid" : dense + BM25 keyword ranking, fused with reciprocal rank fusion.
                Legal questions often hinge on exact terms ("excedencia",
                "periodo de prueba") that BM25 catches and embeddings blur.

Query embeddings are cached in index/query_cache.json so repeated questions
(evaluation reruns, the same question from server and agent) cost no quota.
"""

from __future__ import annotations

import json
import re
import threading
import unicodedata

import numpy as np

from index import INDEX_DIR, PRODUCTION_DESIGN, SOURCES, embed_texts, get_collection, query_prompt

CACHE_PATH = INDEX_DIR / "query_cache.json"
RRF_K = 60
CANDIDATES = 30
_lock = threading.Lock()
_cache: dict[str, list[float]] | None = None
_bm25: dict[str, tuple] = {}

STOP = set("""a al algo ante antes como con contra cual cuando de del desde donde e el ella ellas ellos en entre era es esa
ese eso esta este esto estos estas fue ha han hasta la las le les lo los mas me mi mis muy ni no nos o os otra otro para
pero por que quien se segun ser si sin sobre su sus tambien te tiene tienen u un una uno unos y ya puede pueden cuanto
cuantos cuanta cuantas cual cuales debe deben qué hay""".split())


def _norm(text: str) -> str:
    text = unicodedata.normalize("NFKD", text.lower())
    return "".join(ch for ch in text if not unicodedata.combining(ch))


def tokenize(text: str) -> list[str]:
    return [t for t in re.findall(r"[a-z0-9]+", _norm(text)) if t not in STOP and len(t) > 1]


def _load_cache() -> dict:
    global _cache
    if _cache is None:
        _cache = json.loads(CACHE_PATH.read_text()) if CACHE_PATH.exists() else {}
    return _cache


def embed_query(query: str) -> list[float]:
    with _lock:
        cache = _load_cache()
        if query not in cache:
            cache[query] = embed_texts([query_prompt(query)])[0]
            CACHE_PATH.write_text(json.dumps(cache))
        return cache[query]


def embed_queries(queries: list[str]) -> None:
    """Warm the cache for many queries in batches (used by evaluate.py)."""
    with _lock:
        cache = _load_cache()
        todo = list(dict.fromkeys(q for q in queries if q not in cache))
        for i in range(0, len(todo), 50):
            batch = todo[i:i + 50]
            for q, v in zip(batch, embed_texts([query_prompt(q) for q in batch])):
                cache[q] = v
            CACHE_PATH.write_text(json.dumps(cache))


def _bm25_for(design: str):
    """BM25 over every chunk in the collection; rebuilt when the count changes."""
    from rank_bm25 import BM25Okapi
    col = get_collection(design)
    n = col.count()
    if design not in _bm25 or _bm25[design][0] != n:
        data = col.get(include=["documents", "metadatas"])
        corpus = [tokenize(m["title"] + " " + m["heading"] + " " + d)
                  for d, m in zip(data["documents"], data["metadatas"])]
        _bm25[design] = (n, BM25Okapi(corpus), data["ids"], data["documents"], data["metadatas"])
    return _bm25[design]


def _hit(id_, doc, meta, score) -> dict:
    return {"id": id_, "text": doc, "score": float(score), **meta}


def search(query: str, k: int = 5, design: str = PRODUCTION_DESIGN, mode: str = "dense",
           source: str | None = None, base_only: bool = False) -> list[dict]:
    """Top-k chunks. `source` restricts to one document; `base_only` to the
    original corpus (so evaluation numbers do not move when documents are added)."""
    col = get_collection(design)
    allowed = {source} if source else set(SOURCES) if base_only else None
    where = {"source": {"$in": sorted(allowed)}} if allowed else None
    n = min(CANDIDATES, col.count())
    res = col.query(query_embeddings=[embed_query(query)], n_results=n, where=where,
                    include=["documents", "metadatas", "distances"])
    dense = [_hit(i, d, m, 1 - dist) for i, d, m, dist in
             zip(res["ids"][0], res["documents"][0], res["metadatas"][0], res["distances"][0])]
    if mode == "dense":
        return dense[:k]

    _, bm25, ids, docs, metas = _bm25_for(design)
    scores = bm25.get_scores(tokenize(query))
    order = [i for i in np.argsort(-scores) if not allowed or metas[i]["source"] in allowed][:n]
    sparse = [_hit(ids[i], docs[i], metas[i], scores[i]) for i in order if scores[i] > 0]

    fused: dict[str, dict] = {}
    for ranking in (dense, sparse):
        for rank, h in enumerate(ranking):
            entry = fused.setdefault(h["id"], {**h, "score": 0.0})
            entry["score"] += 1 / (RRF_K + rank + 1)
    return sorted(fused.values(), key=lambda h: -h["score"])[:k]


def citation(hit: dict) -> str:
    return f"{hit['title']}, {hit['location']}"


def format_hits(hits: list[dict]) -> str:
    if not hits:
        return "No results."
    out = []
    for n, h in enumerate(hits, 1):
        since = f" | en vigor desde {h['in_force_since']}" if h.get("in_force_since") else ""
        url = f" | {h['url']}" if h.get("url") else ""
        out.append(f"[{n}] CITE AS: [{citation(h)}]{since}{url}\n{h['text']}")
    return "\n\n---\n\n".join(out)
