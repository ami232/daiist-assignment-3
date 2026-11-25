"""
Retrieval over the committed index, shared by server.py and evaluate.py.

Methods:
    dense   cosine similarity on Gemini embeddings (ChromaDB);
    bm25    Okapi BM25 over the same chunk texts (built in memory, no embeddings);
    hybrid  reciprocal-rank fusion of dense and bm25.

Query embeddings are cached in index/query_cache.json, so re-running the
evaluation or check.py does not spend embedding quota twice on the same text.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from collections import Counter
from pathlib import Path

import index as pipeline

QUERY_CACHE = pipeline.INDEX_DIR / "query_cache.json"
RRF_K = 60
CANDIDATES = 30

# The design used by server.py; evaluate.py compares all of them and REPORT.md justifies this choice.
ACTIVE_DESIGN = "structural"
ACTIVE_METHOD = "dense"  # chosen on 2026-11-21: best hit@k on both question sets (eval/retrieval*.csv)
DEFAULT_K = 5


# --------------------------------------------------------------------------- query embeddings

def _load_cache() -> dict:
    if QUERY_CACHE.exists():
        return json.loads(QUERY_CACHE.read_text(encoding="utf-8"))
    return {}


_cache: dict | None = None


def embed_query(query: str) -> list[float]:
    global _cache
    if _cache is None:
        _cache = _load_cache()
    key = hashlib.sha1(f"{pipeline.EMBED_MODEL}|{pipeline.EMBED_DIM}|{query}".encode()).hexdigest()
    if key not in _cache:
        _cache[key] = pipeline.embed_texts([query], task="RETRIEVAL_QUERY")[0]
        QUERY_CACHE.write_text(json.dumps(_cache), encoding="utf-8")
    return _cache[key]


# --------------------------------------------------------------------------- BM25

TOKEN = re.compile(r"[a-z0-9]+(?:[.,][0-9]+)?")


def tokenize(text: str) -> list[str]:
    return TOKEN.findall(text.lower())


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
        terms = [t for t in tokenize(query) if t in self.idf]
        scores = []
        for i, (doc, length) in enumerate(zip(self.docs, self.lengths)):
            s = 0.0
            for t in terms:
                tf = doc.get(t, 0)
                if tf:
                    s += self.idf[t] * tf * (self.k1 + 1) / (tf + self.k1 * (1 - self.b + self.b * length / self.avg))
            if s:
                scores.append((self.ids[i], s))
        return sorted(scores, key=lambda x: -x[1])[:k]


# --------------------------------------------------------------------------- retriever

class Retriever:
    """Loads one design's collection once; BM25 is rebuilt after documents are added."""

    def __init__(self, design: str = ACTIVE_DESIGN):
        self.design = design
        self.col = pipeline.collection(design)
        self.reload()

    def reload(self) -> None:
        data = self.col.get(include=["documents", "metadatas"])
        self.docs = dict(zip(data["ids"], data["documents"]))
        self.meta = dict(zip(data["ids"], data["metadatas"]))
        self.bm25 = BM25(data["ids"], data["documents"])

    def __len__(self) -> int:
        return len(self.docs)

    def _dense(self, query: str, k: int, where: dict | None = None) -> list[tuple[str, float]]:
        if not self.docs:
            return []
        result = self.col.query(query_embeddings=[embed_query(query)], n_results=min(k, len(self.docs)),
                                where=where, include=["distances"])
        return [(i, 1 - d) for i, d in zip(result["ids"][0], result["distances"][0])]

    def search(self, query: str, k: int = DEFAULT_K, method: str = ACTIVE_METHOD,
               where: dict | None = None, fallback: bool = False) -> list[dict]:
        """`fallback=True` (server only): if the embedding quota is exhausted, dense or hybrid
        degrades to bm25 and every hit is marked, instead of the tool failing. Evaluation never
        falls back."""
        if fallback and method in ("dense", "hybrid"):
            try:
                embed_query(query)
            except pipeline.QuotaExhausted:
                return [{**h, "degraded": True} for h in self.search(query, k, "bm25")]
        if method == "dense":
            ranked = self._dense(query, k, where)
        elif method == "bm25":
            ranked = self.bm25.search(query, k)
        elif method == "hybrid":
            fused: dict[str, float] = {}
            for results in (self._dense(query, CANDIDATES, where), self.bm25.search(query, CANDIDATES)):
                for rank, (i, _) in enumerate(results):
                    fused[i] = fused.get(i, 0.0) + 1 / (RRF_K + rank + 1)
            ranked = sorted(fused.items(), key=lambda x: -x[1])[:k]
        else:
            raise ValueError(f"unknown method {method!r}")
        return [{"id": i, "score": round(s, 4), "text": self.docs[i], **self.meta[i]} for i, s in ranked]


def citation(hit: dict) -> str:
    """The citation format the agent must copy: [CRR, Article 395(1)]."""
    return f"[{hit['source']}, {hit['location']}]"


def format_hits(hits: list[dict]) -> str:
    if not hits:
        return "No passages found in the corpus for this query."
    blocks = []
    if hits[0].get("degraded"):
        blocks.append("Note: semantic search is unavailable (embedding quota); these are keyword-only results.")
    for n, h in enumerate(hits, 1):
        blocks.append(f"Result {n}  cite as {citation(h)}  (article title: {h.get('article_title', '')})\n{h['text']}")
    return "\n\n---\n\n".join(blocks)
