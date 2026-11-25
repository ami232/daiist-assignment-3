"""
Search over the saved index. Used by server.py (the search tool) and evaluate.py.

Two ways to rank chunks:
- "vector": cosine similarity between the question's embedding and each chunk's.
- "hybrid": the vector ranking fused with a BM25 keyword ranking (reciprocal
  rank fusion), so exact terms such as "Blizzard Warning" or "10-513" also count.
"""

import math
import re
from collections import Counter

import index

RRF_K = 60  # standard constant for reciprocal rank fusion

_bm25_cache: dict[str, "BM25"] = {}


def tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+(?:[.-][a-z0-9]+)*", text.lower())


class BM25:
    def __init__(self, ids: list[str], texts: list[str], k1: float = 1.5, b: float = 0.75):
        self.ids, self.k1, self.b = ids, k1, b
        self.docs = [Counter(tokens(t)) for t in texts]
        self.lengths = [sum(d.values()) for d in self.docs]
        self.avg = sum(self.lengths) / max(len(self.lengths), 1)
        df = Counter(term for d in self.docs for term in d)
        n = len(self.docs)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}

    def rank(self, query: str, k: int) -> list[str]:
        q = tokens(query)
        scores = []
        for i, d in enumerate(self.docs):
            s = 0.0
            for t in q:
                if t in d:
                    tf = d[t]
                    s += self.idf[t] * tf * (self.k1 + 1) / (tf + self.k1 * (1 - self.b + self.b * self.lengths[i] / self.avg))
            scores.append(s)
        order = sorted(range(len(scores)), key=lambda i: -scores[i])
        return [self.ids[i] for i in order[:k] if scores[i] > 0]


def bm25_for(design: str) -> BM25:
    store = index.collection(design)
    count = store.count()
    cached = _bm25_cache.get(design)
    if cached is None or len(cached.ids) != count:
        everything = store.get(include=["documents"])
        _bm25_cache[design] = BM25(everything["ids"], everything["documents"])
    return _bm25_cache[design]


def search(query: str, k: int = 5, design: str | None = None, mode: str = "vector",
           query_vector: list[float] | None = None) -> list[dict]:
    """Return the top-k chunks: [{"id", "text", "citation", "source", "section", ...}]."""
    design = design or index.chosen_design()
    store = index.collection(design)
    vector = query_vector or index.embed_query(query)
    pool = k if mode == "vector" else max(k * 4, 20)
    hits = store.query(query_embeddings=[vector], n_results=pool, include=["documents", "metadatas", "distances"])
    by_id = {
        i: {"id": i, "text": t, "score": 1 - d, **m}
        for i, t, m, d in zip(hits["ids"][0], hits["documents"][0], hits["metadatas"][0], hits["distances"][0])
    }
    if mode == "vector":
        return list(by_id.values())[:k]

    vector_rank = hits["ids"][0]
    keyword_rank = bm25_for(design).rank(query, pool)
    fused = Counter()
    for ranking in (vector_rank, keyword_rank):
        for position, chunk_id in enumerate(ranking):
            fused[chunk_id] += 1 / (RRF_K + position + 1)
    top = [chunk_id for chunk_id, _ in fused.most_common(k)]
    missing = [i for i in top if i not in by_id]
    if missing:
        extra = store.get(ids=missing, include=["documents", "metadatas"])
        for i, t, m in zip(extra["ids"], extra["documents"], extra["metadatas"]):
            by_id[i] = {"id": i, "text": t, "score": None, **m}
    return [by_id[i] for i in top]


def format_results(chunks: list[dict]) -> str:
    """What the search tool returns to the model: numbered chunks, each with its citation."""
    if not chunks:
        return "No matching passages in the corpus."
    parts = [f"[{n}] ({c['citation']})\n{c['text']}" for n, c in enumerate(chunks, start=1)]
    return "\n\n".join(parts)
