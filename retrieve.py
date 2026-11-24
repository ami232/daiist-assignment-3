"""
Search over the committed index; used by evaluate.py and server.py.

    search(query, k, strategy, method)   method: dense | bm25 | hybrid

dense  = cosine similarity of Gemini embeddings (ChromaDB)
bm25   = keyword ranking (BM25 Okapi) over the same chunks, built in memory
hybrid = both lists fused with Reciprocal Rank Fusion (RRF)
"""

import re
import unicodedata
from collections import Counter

import numpy as np

import index

CANDIDATES = 50   # how deep each list goes before fusion
RRF_K = 60        # standard RRF constant

_corpus = {}      # strategy -> loaded chunks + BM25 statistics


def tokenize(text: str) -> list[str]:
    """Lowercase, strip accents ('habitación' == 'habitacion'), split into words."""
    text = unicodedata.normalize("NFKD", text.lower())
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.findall(r"\w+", text)


def load(strategy: str) -> dict:
    """Load a design's chunks once and precompute BM25 statistics."""
    if strategy not in _corpus:
        data = index.get_collection(strategy).get(include=["documents", "metadatas"])
        docs = [Counter(tokenize(d)) for d in data["documents"]]
        lengths = np.array([sum(d.values()) for d in docs], dtype=float)
        df = Counter(term for d in docs for term in d)
        n = len(docs)
        _corpus[strategy] = {
            "ids": data["ids"], "documents": data["documents"], "metadatas": data["metadatas"],
            "tf": docs, "lengths": lengths, "avg_length": lengths.mean(),
            "idf": {t: np.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()},
        }
    return _corpus[strategy]


def bm25_rank(query: str, strategy: str, k1: float = 1.5, b: float = 0.75) -> list[int]:
    c = load(strategy)
    norm = k1 * (1 - b + b * c["lengths"] / c["avg_length"])
    scores = np.zeros(len(c["ids"]))
    for term in set(tokenize(query)):
        if term in c["idf"]:
            tf = np.array([d.get(term, 0) for d in c["tf"]], dtype=float)
            scores += c["idf"][term] * tf * (k1 + 1) / (tf + norm)
    return list(np.argsort(-scores)[:CANDIDATES])


def dense_rank(query_vector: list[float], strategy: str) -> list[int]:
    c = load(strategy)
    result = index.get_collection(strategy).query(
        query_embeddings=[query_vector], n_results=CANDIDATES, include=[])
    position = {id_: i for i, id_ in enumerate(c["ids"])}
    return [position[id_] for id_ in result["ids"][0]]


def search(query: str, k: int = 5, strategy: str = index.STRATEGY, method: str = "hybrid",
           query_vector: list[float] | None = None) -> list[dict]:
    """Top-k chunks: [{id, text, metadata, score}]. Pass query_vector to skip embedding."""
    c = load(strategy)
    if method == "bm25":
        ranked = [(i, 0.0) for i in bm25_rank(query, strategy)]
    else:
        query_vector = query_vector or index.embed_query(query)
        dense = dense_rank(query_vector, strategy)
        if method == "dense":
            ranked = [(i, 0.0) for i in dense]
        else:
            fused = Counter()
            for ranking in (dense, bm25_rank(query, strategy)):
                for rank, i in enumerate(ranking):
                    fused[i] += 1 / (RRF_K + rank + 1)
            ranked = fused.most_common()
    return [{"id": c["ids"][i], "text": c["documents"][i], "metadata": c["metadatas"][i], "score": round(s, 4)}
            for i, s in ranked[:k]]
