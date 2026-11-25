"""
Retrieval shared by server.py and evaluate.py, so the evaluation measures
exactly what the tools serve.

    dense   cosine similarity on Gemini embeddings (Chroma)
    bm25    keyword search (Okapi BM25, implemented here, no extra dependency)
    hybrid  reciprocal-rank fusion of dense and bm25

Query vectors are cached in index/query_cache.json so re-running the
evaluation does not spend embedding quota on the same questions again.
"""

from __future__ import annotations

import json
import math
import re
from collections import Counter
from pathlib import Path

import index

# The design served by server.py, chosen by the numbers in eval/retrieval.csv:
# section+dense had the best hit rate at every k (hit@1 0.846, hit@3 1.0 vs 0.577 / 0.885
# for fixed windows); adding BM25 (hybrid) lowered hit@1 to 0.692. k=5 for margin.
SERVED_DESIGN = "section"
SERVED_METHOD = "dense"
SERVED_K = 5

QUERY_CACHE = index.INDEX_DIR / "query_cache.json"
FALLBACK_NOTE = ("Search mode: KEYWORD FALLBACK (semantic search is temporarily unavailable). "
                 "Results may miss passages worded differently from the query.")
RRF_K = 60

_TOKEN = re.compile(r"[a-z0-9]+(?:[.\-/][a-z0-9]+)*")
_STOP = set("a an and are as at be by can do does for from has have how i if in is it its may my of on or "
            "the their there this to under what when which who with without".split())


def tokenize(text: str) -> list[str]:
    return [t for t in _TOKEN.findall(text.lower()) if t not in _STOP]


class BM25:
    def __init__(self, ids: list[str], texts: list[str], k1: float = 1.5, b: float = 0.75):
        self.ids, self.k1, self.b = ids, k1, b
        self.docs = [Counter(tokenize(t)) for t in texts]
        self.lengths = [sum(d.values()) for d in self.docs]
        self.avg = sum(self.lengths) / max(len(self.lengths), 1)
        df = Counter(term for d in self.docs for term in d)
        n = len(self.docs)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}

    def search(self, query: str, k: int) -> list[tuple[str, float]]:
        terms = tokenize(query)
        scores = []
        for i, doc in enumerate(self.docs):
            s = 0.0
            for t in terms:
                f = doc.get(t)
                if f:
                    s += self.idf[t] * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * self.lengths[i] / self.avg))
            if s > 0:
                scores.append((self.ids[i], s))
        return sorted(scores, key=lambda x: -x[1])[:k]


class Retriever:
    """Loads one design's collection from index/ (never re-embeds the corpus)."""

    def __init__(self, design: str = SERVED_DESIGN, base_only: bool = False):
        """base_only: search only the three base documents (evaluation runs, so added documents
        such as the U-space regulation don't change the test set's unanswerable questions)."""
        self.design = design
        self.base_only = base_only
        self.collection = index.get_collection(design)
        self.reload()

    def reload(self) -> None:
        where = {"source": {"$in": list(index.DOCS)}} if self.base_only else None
        data = self.collection.get(where=where, include=["documents", "metadatas"])
        self.docs = {i: (d, m) for i, d, m in zip(data["ids"], data["documents"], data["metadatas"])}
        self.bm25 = BM25(list(self.docs), [d for d, _ in self.docs.values()])

    def dense(self, vector: list[float], k: int) -> list[tuple[str, float]]:
        if not self.docs:
            return []
        where = {"source": {"$in": list(index.DOCS)}} if self.base_only else None
        res = self.collection.query(query_embeddings=[vector], n_results=min(k, len(self.docs)), where=where,
                                    include=["distances"])
        return [(i, 1 - d) for i, d in zip(res["ids"][0], res["distances"][0])]

    def search(self, query: str, k: int = SERVED_K, method: str = SERVED_METHOD) -> list[dict]:
        if method == "bm25":
            ranked = self.bm25.search(query, k)
        else:
            vector = embed_query(query)
            if method == "dense":
                ranked = self.dense(vector, k)
            elif method == "hybrid":
                pool = max(20, 4 * k)
                fused: Counter = Counter()
                for ranking in (self.dense(vector, pool), self.bm25.search(query, pool)):
                    for rank, (i, _) in enumerate(ranking):
                        fused[i] += 1 / (RRF_K + rank + 1)
                ranked = fused.most_common(k)
            else:
                raise ValueError(f"Unknown method {method!r}")
        return [{"id": i, "score": round(s, 4), "text": self.docs[i][0], **self.docs[i][1]} for i, s in ranked]


_cache: dict[str, list[float]] | None = None


def embed_query(query: str) -> list[float]:
    global _cache
    if _cache is None:
        try:
            _cache = json.loads(QUERY_CACHE.read_text(encoding="utf-8"))
        except (FileNotFoundError, json.JSONDecodeError):
            _cache = {}
    key = query.strip()
    if key not in _cache:
        _cache[key] = index.embed_texts([key], "RETRIEVAL_QUERY")[0]
        try:
            QUERY_CACHE.write_text(json.dumps(_cache), encoding="utf-8")
        except OSError:
            pass  # cache is an optimisation only
    return _cache[key]


def cite(hit: dict) -> str:
    return f"[{hit['source']} | {hit['location']}]"


def format_hits(hits: list[dict]) -> str:
    if not hits:
        return "No passages found."
    blocks = []
    for n, h in enumerate(hits, start=1):
        blocks.append(f"### Result {n}\nCitation: {cite(h)}\nDocument: {h.get('doc_title', h['source'])}\n\n{h['text']}")
    return "\n\n".join(blocks)


def words(text: str) -> int:
    return len(text.split())


def location_matches(expected: str, hit_locations: str) -> bool:
    """Does an expected location (e.g. 'UAS.OPEN.020' or 'Article 14') name one of the hit's sections?

    Matches on the rule identifier with word boundaries, so 'Article 1' does not match 'Article 14'.
    """
    expected = index.clean(expected).lower()
    if not expected:
        return False
    pattern = r"(?<![\w.])" + re.escape(expected) + r"(?![\w])"
    return any(re.search(pattern, index.clean(loc).lower()) for loc in hit_locations.split(" || "))


def is_hit(hit: dict, expected_sources: list[str], expected_locations: list[str]) -> bool:
    if hit["source"] not in expected_sources:
        return False
    return any(location_matches(loc, hit.get("locations", hit["location"])) for loc in expected_locations)


if __name__ == "__main__":
    import sys

    r = Retriever()
    print(format_hits(r.search(" ".join(sys.argv[1:]) or "maximum height in the open category")))
