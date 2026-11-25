"""
Search over the committed index. Shared by server.py and evaluate.py.

Designs:
  fixed            dense search over 300-word windows
  article          dense search over article chunks
  article_hybrid   article chunks, dense + BM25 merged with reciprocal rank fusion
  article_bm25     article chunks, keyword (BM25) only, as a check on why hybrid lost
  article_routed   article chunks, dense, but an explicit "Article N" (with the act's
                   name, if given) in the query filters those chunks to the top

Query vectors are cached in index/query_vectors.jsonl so re-running the
evaluation or the grader's check does not spend embedding quota twice.
"""

from __future__ import annotations

import json
import math
import re
from collections import Counter
from pathlib import Path

import numpy as np

import index as ix

DEFAULT_DESIGN = "article"   # routing scored the same on the test set, so the simpler design is served
QUERY_CACHE = ix.INDEX_DIR / "query_vectors.jsonl"
TOKEN = re.compile(r"[a-z0-9]+")
STOP = set("the a an of to and or in on for by with is are be shall that this which as at from it its any such not".split())


def tokens(text: str) -> list[str]:
    return [t for t in TOKEN.findall(text.lower()) if t not in STOP]


class BM25:
    def __init__(self, docs: list[str], k1: float = 1.5, b: float = 0.75):
        self.toks = [tokens(d) for d in docs]
        self.avg = sum(map(len, self.toks)) / max(len(self.toks), 1)
        df = Counter(t for d in self.toks for t in set(d))
        n = len(self.toks)
        self.idf = {t: math.log(1 + (n - c + 0.5) / (c + 0.5)) for t, c in df.items()}
        self.tf = [Counter(d) for d in self.toks]
        self.k1, self.b = k1, b

    def scores(self, query: str) -> np.ndarray:
        q = tokens(query)
        out = np.zeros(len(self.toks))
        for i, (tf, d) in enumerate(zip(self.tf, self.toks)):
            norm = self.k1 * (1 - self.b + self.b * len(d) / self.avg)
            out[i] = sum(self.idf.get(t, 0) * tf[t] * (self.k1 + 1) / (tf[t] + norm) for t in q if t in tf)
        return out


class Index:
    """Chunks and vectors of one chunking, loaded from index/ (never re-embedded)."""

    def __init__(self, chunking: str):
        self.chunking = chunking
        self.reload()

    def reload(self) -> None:
        cache = ix.load_vector_cache()
        chunks = ix.read_design(self.chunking)
        self.chunks = [c for c in chunks if c["hash"] in cache]
        self.matrix = np.array([cache[c["hash"]] for c in self.chunks], dtype=np.float32)
        self.bm25 = BM25([c["text"] for c in self.chunks])

    def dense(self, qvec: np.ndarray) -> np.ndarray:
        return self.matrix @ qvec


_query_cache: dict[str, list[float]] | None = None


def embed_query(query: str) -> np.ndarray:
    global _query_cache
    if _query_cache is None:
        _query_cache = {}
        if QUERY_CACHE.exists():
            for line in QUERY_CACHE.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    row = json.loads(line)
                    _query_cache[row["q"]] = row["v"]
    key = " ".join(query.split())
    if key not in _query_cache:
        v = ix.embed_texts([key])[0]
        _query_cache[key] = v
        with QUERY_CACHE.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"q": key, "v": v}) + "\n")
    return np.asarray(_query_cache[key], dtype=np.float32)


_indexes: dict[str, Index] = {}


def get_index(chunking: str) -> Index:
    if chunking not in _indexes:
        _indexes[chunking] = Index(chunking)
    return _indexes[chunking]


def search(query: str, k: int = 5, design: str = DEFAULT_DESIGN) -> list[dict]:
    """Top-k chunks for a query under one design, each with its score."""
    chunking = "fixed" if design == "fixed" else "article"
    idx = get_index(chunking)
    dense = idx.dense(embed_query(query))
    if design == "article_bm25":
        score = idx.bm25.scores(query)
    elif design == "article_routed":
        refs = article_refs(query)
        boost = np.array([1.0 if any(a in c["articles"] and (s is None or s == c["source"]) for s, a in refs) else 0.0
                          for c in idx.chunks])
        score = dense + boost
    elif design.endswith("hybrid"):
        sparse = idx.bm25.scores(query)
        rd = np.argsort(-dense).argsort()
        rs = np.argsort(-sparse).argsort()
        score = 1 / (60 + rd) + 1 / (60 + rs)
    else:
        score = dense
    top = np.argsort(-score)[:k]
    return [{**idx.chunks[i], "score": float(score[i]), "similarity": float(dense[i])} for i in top]


ACTS = {"gdpr": "gdpr", "dsa": "dsa", "digital services": "dsa", "eprivacy": "eprivacy", "e-privacy": "eprivacy",
        "2016/679": "gdpr", "2022/2065": "dsa", "2002/58": "eprivacy", "tco": "tco", "2021/784": "tco"}


def article_refs(query: str) -> list[tuple[str | None, str]]:
    """Explicit references like 'Article 17 GDPR' -> [('gdpr', '17')]; act None if not named."""
    q = query.lower()
    named = [v for k, v in ACTS.items() if k in q]
    nums = re.findall(r"\bart(?:icle|\.)?\s*(\d+[a-z]?)\b", q)
    if not nums:
        return []
    acts = list(dict.fromkeys(named)) or [None]
    return [(a, n) for a in acts for n in nums]


def cite(chunk: dict) -> str:
    return f"{chunk['source'].upper()} {chunk['location']}"


def format_results(results: list[dict]) -> str:
    if not results:
        return "No results."
    parts = []
    for r in results:
        text = r["text"].split("\n", 1)[-1]
        parts.append(f"[{r['id']}] {cite(r)} (similarity {r['similarity']:.2f})\n{text}")
    return "\n\n---\n\n".join(parts)
