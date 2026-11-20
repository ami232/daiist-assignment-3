"""
Retrieval over the committed index (shared by server.py and evaluate.py).

Three designs over the SAME chunks and the SAME stored vectors, so comparing
them costs no extra document embeddings:

    vector  cosine similarity between the query embedding and the chunk vectors (ChromaDB)
    bm25    lexical BM25 over "location + text" (exact terms, figures, defined names)
    hybrid  Reciprocal Rank Fusion of the vector and BM25 rankings

Query embeddings are cached in index/query_cache.json (keyed by the exact query
text), so a question is embedded at most once, ever.
"""

from __future__ import annotations

import json
import math
import re
import sys
import threading
from collections import Counter
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path

import index as ix

QUERY_CACHE = ix.INDEX_DIR / "query_cache.json"
RRF_K = 60            # standard constant for Reciprocal Rank Fusion
CANDIDATES = 50       # depth of each ranking fed into the fusion
BM25_K1, BM25_B = 1.5, 0.75
DESIGNS = ("vector", "bm25", "hybrid")

STOPWORDS = set("""a an and are as at be by for from has have in is it its of on or that the this to was were
will with what which who whom how when where why did does do our we us their they than then there these those""".split())
TOKEN_RE = re.compile(r"[a-z0-9]+(?:[.,][0-9]+)*%?")


def log(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


def tokenize(text: str) -> list[str]:
    """Lower-case word tokens; figures stay whole ('801,351,354', '65.79', '50.1%')."""
    return [t for t in TOKEN_RE.findall(text.lower().replace("’", "'")) if t not in STOPWORDS]


@dataclass
class Hit:
    id: str
    source: str
    location: str
    page: str
    text: str
    score: float
    status: str = ""
    filed: str = ""

    def citation(self) -> str:
        return f"[{self.source} | {self.location} | p. {self.page}]"


# --------------------------------------------------------------------------- corpus

@lru_cache(maxsize=1)
def _corpus() -> tuple[list[dict], dict[str, int]]:
    """Every chunk that has a stored vector (what the index actually serves)."""
    col = ix.collection()
    data = col.get(include=["documents", "metadatas"])
    chunks = [{"id": i, "text": d, **m} for i, d, m in zip(data["ids"], data["documents"], data["metadatas"])]
    chunks.sort(key=lambda c: (c["source"], c.get("order", 0)))
    return chunks, {c["id"]: n for n, c in enumerate(chunks)}


def refresh() -> None:
    """Forget cached corpus/BM25 statistics (after add_document)."""
    _corpus.cache_clear()
    _bm25.cache_clear()


class BM25:
    def __init__(self, docs: list[list[str]]):
        self.docs = docs
        self.n = len(docs)
        self.avgdl = sum(map(len, docs)) / max(self.n, 1)
        self.tf = [Counter(d) for d in docs]
        df = Counter(t for d in docs for t in set(d))
        self.idf = {t: math.log(1 + (self.n - f + 0.5) / (f + 0.5)) for t, f in df.items()}

    def scores(self, query: list[str]) -> list[float]:
        out = []
        for tf, doc in zip(self.tf, self.docs):
            norm = BM25_K1 * (1 - BM25_B + BM25_B * len(doc) / self.avgdl)
            out.append(sum(self.idf.get(t, 0) * tf[t] * (BM25_K1 + 1) / (tf[t] + norm) for t in query if t in tf))
        return out


@lru_cache(maxsize=1)
def _bm25() -> BM25:
    chunks, _ = _corpus()
    return BM25([tokenize(f"{c['location']} {c['text']}") for c in chunks])


# --------------------------------------------------------------------------- query vectors

_cache_lock = threading.Lock()


def _load_cache() -> dict:
    return json.loads(QUERY_CACHE.read_text()) if QUERY_CACHE.is_file() else {}


def query_vector(query: str) -> list[float]:
    """Embedding of a query, from the persistent cache when available."""
    key = query.strip()
    with _cache_lock:
        cache = _load_cache()
        if key in cache:
            return cache[key]
    vector = ix.embed_query(key)
    with _cache_lock:
        cache = _load_cache()
        cache[key] = [round(v, 7) for v in vector]
        QUERY_CACHE.write_text(json.dumps(cache))
    return vector


# --------------------------------------------------------------------------- designs

def _vector_ranking(query: str, n: int) -> list[tuple[int, float]]:
    chunks, position = _corpus()
    result = ix.collection().query(query_embeddings=[query_vector(query)], n_results=min(n, len(chunks)), include=["distances"])
    return [(position[i], 1 - d) for i, d in zip(result["ids"][0], result["distances"][0])]


def _bm25_ranking(query: str, n: int) -> list[tuple[int, float]]:
    scores = _bm25().scores(tokenize(query))
    ranked = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)
    return [(i, scores[i]) for i in ranked[:n] if scores[i] > 0]


def _rrf(*rankings: list[tuple[int, float]]) -> list[tuple[int, float]]:
    fused: Counter = Counter()
    for ranking in rankings:
        for rank, (i, _) in enumerate(ranking, start=1):
            fused[i] += 1 / (RRF_K + rank)
    return fused.most_common()


def search(query: str, k: int = 5, design: str = "hybrid") -> list[Hit]:
    """Top-k chunks for a query under one of DESIGNS."""
    if design not in DESIGNS:
        raise ValueError(f"design must be one of {DESIGNS}")
    if design == "vector":
        ranking = _vector_ranking(query, k)
    elif design == "bm25":
        ranking = _bm25_ranking(query, k)
    else:
        ranking = _rrf(_vector_ranking(query, CANDIDATES), _bm25_ranking(query, CANDIDATES))
    chunks, _ = _corpus()
    return [Hit(chunks[i]["id"], chunks[i]["source"], chunks[i]["location"], chunks[i]["page"], chunks[i]["text"],
                round(s, 4), chunks[i].get("status", ""), chunks[i].get("filed", ""))
            for i, s in ranking[:k]]
