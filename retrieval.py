"""
Retrieval over the committed index, shared by server.py and evaluate.py.

    search(query, k=5, design="structured", method="vector")  -> list[Hit]

Designs are the two chunkings stored by index.py ("structured", "fixed"). Methods:
  - "vector": cosine similarity on gemini-embedding-2 vectors (Chroma)
  - "hybrid": vector ranking fused with a BM25 keyword ranking (reciprocal rank fusion), which helps
              on exact legal terms ("chapeau", "Article XX", "Harmonized System") that embeddings blur.

Query vectors are cached in index/query_cache.json so repeated evaluation runs cost no embeddings.
Nothing here prints to stdout (server.py's stdout is the MCP channel).
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from collections import Counter
from dataclasses import dataclass
from functools import lru_cache

import index

QUERY_CACHE = index.INDEX_DIR / "query_cache.json"
RRF_K = 60  # standard reciprocal-rank-fusion constant


@dataclass
class Hit:
    id: str
    text: str
    metadata: dict
    score: float      # higher is better (1 - cosine distance, or fused RRF score)

    @property
    def citation(self) -> str:
        return self.metadata.get("citation", "")


# --------------------------------------------------------------------------- query embeddings

def _load_cache() -> dict:
    return json.loads(QUERY_CACHE.read_text()) if QUERY_CACHE.exists() else {}


def embed_query(query: str) -> list[float]:
    key = hashlib.sha1(f"{index.EMBED_MODEL}:{index.EMBED_DIM}:{query}".encode()).hexdigest()
    cache = _load_cache()
    if key not in cache:
        cache[key] = index.embed_texts([index.query_prefix(query)])[0]
        QUERY_CACHE.write_text(json.dumps(cache))
    return cache[key]


def embed_queries(queries: list[str]) -> None:
    """Warm the cache in batches (one API call per 50 new questions)."""
    cache = _load_cache()
    keys = {q: hashlib.sha1(f"{index.EMBED_MODEL}:{index.EMBED_DIM}:{q}".encode()).hexdigest() for q in queries}
    todo = [q for q in queries if keys[q] not in cache]
    for i in range(0, len(todo), index.EMBED_BATCH):
        batch = todo[i:i + index.EMBED_BATCH]
        for q, v in zip(batch, index.embed_texts([index.query_prefix(q) for q in batch])):
            cache[keys[q]] = v
        QUERY_CACHE.write_text(json.dumps(cache))


# --------------------------------------------------------------------------- BM25

TOKEN = re.compile(r"[a-z0-9]+")


def tokenize(text: str) -> list[str]:
    return TOKEN.findall(text.lower())


@lru_cache(maxsize=4)
def _bm25(design: str):
    col = index.collection(design)
    got = col.get(include=["documents", "metadatas"])
    docs = [tokenize(d) for d in got["documents"]]
    df = Counter(t for d in docs for t in set(d))
    avg = sum(map(len, docs)) / max(len(docs), 1)
    return got, docs, df, avg


def bm25_rank(query: str, design: str, n: int, k1: float = 1.5, b: float = 0.75) -> list[tuple[int, float]]:
    got, docs, df, avg = _bm25(design)
    q = tokenize(query)
    N = len(docs)
    scores = []
    for i, d in enumerate(docs):
        tf = Counter(d)
        s = 0.0
        for t in q:
            if t in tf:
                idf = math.log(1 + (N - df[t] + 0.5) / (df[t] + 0.5))
                s += idf * tf[t] * (k1 + 1) / (tf[t] + k1 * (1 - b + b * len(d) / avg))
        scores.append((i, s))
    scores.sort(key=lambda x: -x[1])
    return [x for x in scores[:n] if x[1] > 0]


# --------------------------------------------------------------------------- search

def invalidate() -> None:
    """Call after add_document changes a collection, so BM25 statistics are rebuilt."""
    _bm25.cache_clear()


def search(query: str, k: int = 5, design: str = "structured", method: str = "vector") -> list[Hit]:
    col = index.collection(design)
    pool = k if method == "vector" else max(k * 4, 20)
    res = col.query(query_embeddings=[embed_query(query)], n_results=pool,
                    include=["documents", "metadatas", "distances"])
    vec = [Hit(i, d, m, 1 - dist) for i, d, m, dist in
           zip(res["ids"][0], res["documents"][0], res["metadatas"][0], res["distances"][0])]
    if method == "vector":
        return vec[:k]
    if method != "hybrid":
        raise ValueError(f"unknown method {method!r}")

    got = _bm25(design)[0]
    kw = [Hit(got["ids"][i], got["documents"][i], got["metadatas"][i], s) for i, s in bm25_rank(query, design, pool)]
    fused: dict[str, float] = {}
    by_id = {}
    for ranking in (vec, kw):
        for rank, h in enumerate(ranking):
            fused[h.id] = fused.get(h.id, 0.0) + 1 / (RRF_K + rank + 1)
            by_id[h.id] = h
    best = sorted(fused, key=lambda i: -fused[i])[:k]
    return [Hit(i, by_id[i].text, by_id[i].metadata, fused[i]) for i in best]


def format_hits(hits: list[Hit]) -> str:
    """What the search tool returns to a model: one block per chunk, citation and link first."""
    blocks = []
    for n, h in enumerate(hits, 1):
        m = h.metadata
        extra = f"\nInterpretive note: {m['interpretive_note']} (search for it if relevant)" if m.get("interpretive_note") else ""
        blocks.append(f"[{n}] Citation: {m['citation']}\nSource: {m['document']}\nURL: {m['url']}{extra}\n\n{h.text}")
    return "\n\n---\n\n".join(blocks) if blocks else "No matching passages in the corpus."
