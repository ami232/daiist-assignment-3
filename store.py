"""ChromaDB storage, indexing (resumable) and retrieval (vector / hybrid)."""
from __future__ import annotations

import math
import threading
import re
import sys
from collections import Counter

import chromadb

from config import DEFAULT_DESIGN, DESIGNS, INDEX_DIR
from embed import embed_query

COLLECTIONS = {"article": "chunks_article", "fixed": "chunks_fixed"}


def log(*a):
    print(*a, file=sys.stderr, flush=True)       # never stdout: the MCP server speaks JSON-RPC there


_lock = threading.RLock()
_client = None


def collection(kind: str):
    """One ChromaDB client per process, created once. The MCP server runs tool calls on parallel threads
    and Chroma's shared client setup is not thread-safe, so a client per call crashed under parallel searches.
    (If another process writes to index/ while a long-running server is up, restart the server.)"""
    global _client
    with _lock:
        if _client is None:
            INDEX_DIR.mkdir(exist_ok=True)
            _client = chromadb.PersistentClient(path=str(INDEX_DIR))
        return _client.get_or_create_collection(COLLECTIONS[kind], metadata={"hnsw:space": "cosine"})


# ------------------------------------------------------------------ retrieval
_STOP = set("the a an of to in and or for is are be by on with as at that this it from under what which who when".split())


def tok(s: str) -> list[str]:
    return [w for w in re.findall(r"\w+", s.lower()) if w not in _STOP]


class BM25:
    def __init__(self, docs: list[str], k1: float = 1.5, b: float = 0.75):
        self.tf = [Counter(tok(d)) for d in docs]
        self.len = [sum(t.values()) for t in self.tf]
        self.avg = sum(self.len) / max(1, len(docs))
        df = Counter(w for t in self.tf for w in t)
        n = len(docs)
        self.idf = {w: math.log(1 + (n - c + 0.5) / (c + 0.5)) for w, c in df.items()}
        self.k1, self.b = k1, b

    def scores(self, q: str) -> list[float]:
        qs = tok(q)
        out = []
        for t, L in zip(self.tf, self.len):
            s = 0.0
            for w in qs:
                f = t.get(w, 0)
                if f:
                    s += self.idf[w] * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * L / self.avg))
            out.append(s)
        return out


_bm25_cache: dict[str, tuple[int, BM25, dict]] = {}


def _bm25(kind: str):
    col = collection(kind)
    n = col.count()
    if kind not in _bm25_cache or _bm25_cache[kind][0] != n:
        r = col.get(include=["documents", "metadatas"])
        _bm25_cache[kind] = (n, BM25(r["documents"]), r)
    return _bm25_cache[kind][1:]


def _hit(id_, doc, meta, score) -> dict:
    return dict(id=id_, doc_id=meta["doc_id"], location=meta["location"], locs=meta["locs"].split(" | "),
                title=meta.get("title", ""), text=doc, score=round(float(score), 4),
                citation=f"[{meta['doc_id']}:{meta['location']}]")


def retrieve(query: str, k: int = 5, design: str | None = None) -> list[dict]:
    kind, hybrid = DESIGNS[design or DEFAULT_DESIGN]
    qvec = embed_query(query)                       # network call, outside the lock
    with _lock:
        return _retrieve_locked(query, qvec, k, kind, hybrid)


def _retrieve_locked(query: str, qvec: list[float], k: int, kind: str, hybrid: bool) -> list[dict]:
    col = collection(kind)
    if col.count() == 0:
        raise RuntimeError(f"index '{kind}' is empty: run `uv run python main.py index`")
    n = max(k, 20) if hybrid else k
    r = col.query(query_embeddings=[qvec], n_results=min(n, col.count()),
                  include=["documents", "metadatas", "distances"])
    vec = [_hit(i, d, m, 1 - dist) for i, d, m, dist in zip(r["ids"][0], r["documents"][0], r["metadatas"][0], r["distances"][0])]
    if not hybrid:
        return vec[:k]
    bm, data = _bm25(kind)
    sc = bm.scores(query)
    top = sorted(range(len(sc)), key=lambda i: -sc[i])[:20]
    fused: dict[str, float] = {}
    pool: dict[str, dict] = {}
    for rank, h in enumerate(vec):
        fused[h["id"]] = fused.get(h["id"], 0) + 1 / (60 + rank)
        pool[h["id"]] = h
    for rank, i in enumerate(top):
        if sc[i] <= 0:
            break
        id_ = data["ids"][i]
        fused[id_] = fused.get(id_, 0) + 1 / (60 + rank)
        pool.setdefault(id_, _hit(id_, data["documents"][i], data["metadatas"][i], 0))
    best = sorted(fused, key=lambda i: -fused[i])[:k]
    return [dict(pool[i], score=round(fused[i], 4)) for i in best]


def format_hits(hits: list[dict]) -> str:
    """What the search tool returns: one block per chunk, headed by its citation."""
    if not hits:
        return "No results."
    return "\n\n".join(f"### {h['citation']} (score {h['score']})\n{h['text']}" for h in hits)