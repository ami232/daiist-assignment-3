"""
Search over the saved index (no re-embedding of the corpus): used by server.py,
agent.py and evaluate.py.

    from retrieval import search
    hits = search("How many electric cars were sold in 2025?", k=5)
"""

from __future__ import annotations

import numpy as np

import index as ix

_loaded: dict[str, tuple[list[dict], np.ndarray]] = {}


def _load(design: str) -> tuple[list[dict], np.ndarray]:
    """Chunks of a design and their vectors as a normalised matrix (cached in memory)."""
    if design not in _loaded:
        chunks = ix.load_chunks(design)
        cache = ix.load_vectors()
        keep, vecs = [], []
        for c in chunks:
            v = cache.get(ix.vector_key(c["text"], "RETRIEVAL_DOCUMENT"))
            if v is not None:
                keep.append(c)
                vecs.append(v)
        m = np.array(vecs, dtype=np.float32) if vecs else np.zeros((0, ix.EMBED_DIM), np.float32)
        m /= np.linalg.norm(m, axis=1, keepdims=True) + 1e-12
        _loaded[design] = (keep, m)
    return _loaded[design]


def reload(design: str | None = None) -> None:
    """Forget the in-memory copy (after add_document changed the index)."""
    if design:
        _loaded.pop(design, None)
    else:
        _loaded.clear()


def search(query: str, k: int = 5, design: str = ix.CHUNKING) -> list[dict]:
    """Top-k chunks by cosine similarity, each with its score."""
    chunks, m = _load(design)
    if not chunks:
        return []
    q = np.array(ix.embed_texts([query], "RETRIEVAL_QUERY")[0], dtype=np.float32)
    q /= np.linalg.norm(q) + 1e-12
    scores = m @ q
    top = np.argsort(-scores)[:k]
    return [{**chunks[i], "score": float(scores[i])} for i in top]
