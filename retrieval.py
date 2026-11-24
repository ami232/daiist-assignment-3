"""
Retrieval over the index built by index.py. Used by server.py and evaluate.py.

Two designs share the same chunks and vectors (no extra embeddings):
- "dense":  cosine similarity on Gemini embeddings (ChromaDB)
- "hybrid": dense + BM25 keyword ranking, fused with Reciprocal Rank Fusion
"""

from __future__ import annotations

import math
import re
from collections import Counter

import index

DEFAULT_DESIGN = "dense"   # set after comparing hit rates in evaluate.py
DEFAULT_K = 5
RRF_K = 60                 # standard RRF constant

_TOKEN = re.compile(r"[a-z0-9]+(?:[.'][a-z0-9]+)*")
STOPWORDS = set("""a an and are as at be by can do does for from how i if in is it its my of on or
should the this to was what when where which who why will with you your""".split())


def tokenize(text: str) -> list[str]:
    return [t for t in _TOKEN.findall(text.lower()) if t not in STOPWORDS]


class BM25:
    def __init__(self, docs: list[str], k1: float = 1.5, b: float = 0.75):
        self.k1, self.b = k1, b
        self.tfs = [Counter(tokenize(d)) for d in docs]
        self.lens = [sum(tf.values()) for tf in self.tfs]
        self.avg = sum(self.lens) / max(1, len(self.lens))
        df = Counter(t for tf in self.tfs for t in tf)
        n = len(docs)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}

    def scores(self, query: str) -> list[float]:
        q = tokenize(query)
        out = []
        for tf, ln in zip(self.tfs, self.lens):
            s = 0.0
            for t in q:
                if t in tf:
                    f = tf[t]
                    s += self.idf[t] * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * ln / self.avg))
            out.append(s)
        return out


class Retriever:
    """Loads the committed index once; never re-embeds the corpus."""

    def __init__(self, collection=None):
        self.col = collection or index.get_collection()
        self.reload()

    def reload(self) -> None:
        data = self.col.get(include=["documents", "metadatas"])
        self.ids, self.docs, self.metas = data["ids"], data["documents"], data["metadatas"]
        self.pos = {cid: i for i, cid in enumerate(self.ids)}
        # BM25 sees the title and section too, like the embeddings do
        self.bm25 = BM25([f"{m['title']} {m['location']} {d}" for d, m in zip(self.docs, self.metas)])

    def _hit(self, i: int, score: float) -> dict:
        return {"id": self.ids[i], "text": self.docs[i], "score": round(score, 4), **self.metas[i]}

    def dense(self, query: str, k: int, query_vector=None) -> list[dict]:
        vec = query_vector if query_vector is not None else index.embed_query(query)
        r = self.col.query(query_embeddings=[vec], n_results=min(k, len(self.ids)))
        return [self._hit(self.pos[cid], 1 - dist) for cid, dist in zip(r["ids"][0], r["distances"][0])]

    def keyword(self, query: str, k: int) -> list[dict]:
        s = self.bm25.scores(query)
        order = sorted(range(len(s)), key=lambda i: -s[i])[:k]
        return [self._hit(i, s[i]) for i in order]

    def hybrid(self, query: str, k: int, query_vector=None, pool: int = 30) -> list[dict]:
        dense = self.dense(query, pool, query_vector)
        sparse = self.keyword(query, pool)
        fused: dict[str, float] = {}
        for ranking in (dense, sparse):
            for rank, hit in enumerate(ranking):
                fused[hit["id"]] = fused.get(hit["id"], 0.0) + 1 / (RRF_K + rank + 1)
        order = sorted(fused, key=lambda cid: -fused[cid])[:k]
        return [self._hit(self.pos[cid], fused[cid]) for cid in order]

    def search(self, query: str, k: int = DEFAULT_K, design: str = DEFAULT_DESIGN, query_vector=None) -> list[dict]:
        if design == "dense":
            return self.dense(query, k, query_vector)
        if design == "hybrid":
            return self.hybrid(query, k, query_vector)
        raise ValueError(f"unknown design {design!r}")


def format_hits(hits: list[dict]) -> str:
    """Numbered passages with the citation the agent must copy: [source | location]."""
    if not hits:
        return "No passages found."
    blocks = []
    for n, h in enumerate(hits, 1):
        cite = f"[{h['source']} | {h['location']}]"
        blocks.append(f"### Result {n}  {cite}\nDocument: {h['title']}\nURL: {h.get('url') or '-'}\n\n{h['text']}")
    return "\n\n".join(blocks)
