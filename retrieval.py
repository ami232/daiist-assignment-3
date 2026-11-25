"""
Search over the index built by index.py. Used by server.py (the search tool)
and by evaluate.py (hit rate), so both measure exactly the same thing.

Retrieval designs compared in evaluate.py (all over the same section chunks):
    section-bm25    keyword search only (BM25), no embeddings
    section-vector  Gemini embeddings, cosine similarity
    section-hybrid  vector + BM25 rankings merged by reciprocal rank fusion
                    (helps exact item names like "SR-84" or "CL-40")

SERVED_DESIGN is the one the MCP server uses, chosen by the hit-rate numbers.
"""

from __future__ import annotations

import math
import re
from collections import Counter

from index import collection, embed_query

DESIGNS = {
    "section-bm25": ("section", "bm25"),
    "section-vector": ("section", "vector"),
    "section-hybrid": ("section", "hybrid"),
}
SERVED_DESIGN = "section-vector"  # best hit@3 in evaluate.py (0.87 vs 0.83 hybrid, 0.67 BM25)
RRF_K = 60  # standard reciprocal-rank-fusion constant
CANDIDATES = 20


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+(?:[.\-'][a-z0-9]+)*", text.lower())


class _BM25:
    """Plain BM25 over every chunk in a collection (a few hundred chunks: fits in memory)."""

    def __init__(self, ids: list[str], docs: list[str], k1: float = 1.5, b: float = 0.75):
        self.ids, self.k1, self.b = ids, k1, b
        self.tfs = [Counter(_tokens(d)) for d in docs]
        self.lens = [sum(tf.values()) for tf in self.tfs]
        self.avg = sum(self.lens) / max(len(self.lens), 1)
        df = Counter(t for tf in self.tfs for t in tf)
        n = len(docs)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}

    def top(self, query: str, k: int) -> list[str]:
        q = _tokens(query)
        scores = []
        for i, tf in enumerate(self.tfs):
            s = 0.0
            for t in q:
                if t in tf:
                    f = tf[t]
                    s += self.idf[t] * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * self.lens[i] / self.avg))
            if s > 0:
                scores.append((s, self.ids[i]))
        return [i for _, i in sorted(scores, reverse=True)[:k]]


_bm25_cache: dict[str, tuple[int, _BM25]] = {}


def _bm25(chunking: str) -> _BM25:
    col = collection(chunking)
    count = col.count()
    cached = _bm25_cache.get(chunking)
    if cached is None or cached[0] != count:  # rebuilt after add_document changes the collection
        data = col.get(include=["documents"])
        _bm25_cache[chunking] = (count, _BM25(data["ids"], data["documents"]))
    return _bm25_cache[chunking][1]


def search(query: str, k: int = 5, design: str = SERVED_DESIGN) -> list[dict]:
    """Top-k chunks for a query: [{id, source, section, url, text, rank}]"""
    chunking, method = DESIGNS[design]
    col = collection(chunking)
    if col.count() == 0:
        return []
    if method == "bm25":
        vector_ids = []
    else:
        vec = col.query(query_embeddings=[embed_query(query)], n_results=min(CANDIDATES, col.count()), include=[])
        vector_ids = vec["ids"][0]

    if method == "bm25":
        ranked = _bm25(chunking).top(query, k)
    elif method == "vector":
        ranked = vector_ids[:k]
    else:
        fused: dict[str, float] = {}
        for ids in (vector_ids, _bm25(chunking).top(query, CANDIDATES)):
            for rank, cid in enumerate(ids):
                fused[cid] = fused.get(cid, 0.0) + 1.0 / (RRF_K + rank + 1)
        ranked = [cid for cid, _ in sorted(fused.items(), key=lambda x: -x[1])[:k]]

    if not ranked:
        return []
    got = col.get(ids=ranked, include=["documents", "metadatas"])
    by_id = {i: (d, m) for i, d, m in zip(got["ids"], got["documents"], got["metadatas"])}
    hits = []
    for rank, cid in enumerate(ranked, 1):
        doc, meta = by_id[cid]
        text = doc.split("\n\n", 1)[1] if doc.startswith("Page: ") and "\n\n" in doc else doc
        hits.append({"id": cid, "rank": rank, "source": meta["source"], "section": meta["section"],
                     "url": meta["url"], "text": text})
    return hits


def sections_of(hit: dict) -> list[str]:
    """A chunk can cover several small neighbouring sections ("Overview / Usage")."""
    return [s.strip() for s in hit["section"].split(" / ")]


def citation(hit: dict) -> str:
    """The citation the agent copies: [Page § first section the chunk covers]."""
    return f"[{hit['source']} § {sections_of(hit)[0]}]"


def format_hits(hits: list[dict]) -> str:
    if not hits:
        return "No results. The corpus has nothing on this; say so instead of answering."
    blocks = []
    for h in hits:
        covers = sections_of(h)
        extra = f"\ncovers: {' / '.join(covers)} (cite any of these sections of {h['source']})" if len(covers) > 1 else ""
        blocks.append(f"Result {h['rank']}  cite as: {citation(h)}{extra}\nurl: {h['url']}\n{h['text']}")
    return "\n\n---\n\n".join(blocks)
