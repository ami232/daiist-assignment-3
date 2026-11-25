"""
Search over the committed index. Used by server.py (the search tool) and evaluate.py.

Methods:
- "dense":  cosine similarity between the query's Gemini embedding and each chunk's.
- "hybrid": dense + BM25 keyword ranking, merged with reciprocal rank fusion (RRF).
            Costs no extra embeddings; helps with exact drug names and numbers.
"""

from __future__ import annotations

import math
import re
from collections import Counter

import index

_bm25_cache: dict[str, "BM25"] = {}
TOKEN = re.compile(r"[a-z0-9]+(?:\.[0-9]+)?")


def tokenize(text: str) -> list[str]:
    return TOKEN.findall(text.lower())


class BM25:
    """Okapi BM25 over every chunk of one collection (k1=1.5, b=0.75)."""

    def __init__(self, ids: list[str], texts: list[str], k1: float = 1.5, b: float = 0.75):
        self.ids, self.k1, self.b = ids, k1, b
        self.docs = [Counter(tokenize(t)) for t in texts]
        self.lengths = [sum(d.values()) for d in self.docs]
        self.avg = sum(self.lengths) / max(len(self.docs), 1)
        df = Counter(term for d in self.docs for term in d)
        n = len(self.docs)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}

    def top(self, query: str, n: int) -> list[str]:
        terms = tokenize(query)
        scores = []
        for doc_id, doc, length in zip(self.ids, self.docs, self.lengths):
            s = 0.0
            for t in terms:
                f = doc.get(t, 0)
                if f:
                    s += self.idf[t] * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * length / self.avg))
            scores.append(s)
        order = sorted(range(len(scores)), key=lambda i: -scores[i])
        return [self.ids[i] for i in order[:n] if scores[i] > 0]


def bm25_for(design: str) -> BM25:
    if design not in _bm25_cache:
        data = index.collection(design).get(include=["documents", "metadatas"])
        # Index the heading too, as the dense side sees it in the embedded text.
        texts = [f"{m['product']} {m['section']} {d}" for d, m in zip(data["documents"], data["metadatas"])]
        _bm25_cache[design] = BM25(data["ids"], texts)
    return _bm25_cache[design]


def search(query: str, k: int = 5, design: str | None = None, method: str = "dense",
           where: dict | None = None) -> list[dict]:
    """Return the top-k chunks: [{"id", "text", "metadata", "score"}], best first."""
    design = design or index.active_design()
    col = index.collection(design)
    vector = index.embed_query(query)
    pool = k if method == "dense" else max(20, k)
    found = col.query(query_embeddings=[vector], n_results=pool, where=where,
                      include=["documents", "metadatas", "distances"])
    dense = [{"id": i, "text": d, "metadata": m, "score": 1 - dist}
             for i, d, m, dist in zip(found["ids"][0], found["documents"][0],
                                      found["metadatas"][0], found["distances"][0])]
    if method == "dense":
        return dense[:k]
    if method != "hybrid":
        raise ValueError(f"unknown method {method!r}")

    # Reciprocal rank fusion: score = sum over rankings of 1 / (60 + rank).
    keyword = bm25_for(design).top(query, pool)
    if where:  # keep the keyword side inside the same filter
        allowed = set(col.get(where=where, include=[])["ids"])
        keyword = [i for i in keyword if i in allowed]
    fused: dict[str, float] = {}
    for ranking in ([c["id"] for c in dense], keyword):
        for rank, doc_id in enumerate(ranking):
            fused[doc_id] = fused.get(doc_id, 0) + 1 / (60 + rank)
    best = sorted(fused, key=lambda i: -fused[i])[:k]
    by_id = {c["id"]: c for c in dense}
    missing = [i for i in best if i not in by_id]
    if missing:
        extra = col.get(ids=missing, include=["documents", "metadatas"])
        for i, d, m in zip(extra["ids"], extra["documents"], extra["metadatas"]):
            by_id[i] = {"id": i, "text": d, "metadata": m}
    return [{**by_id[i], "score": round(fused[i], 4)} for i in best]


def format_results(chunks: list[dict]) -> str:
    """Text the model reads: one block per chunk, citation first."""
    if not chunks:
        return "No passages found."
    return "\n\n".join(f"{c['metadata']['citation']}\n{c['text']}" for c in chunks)
