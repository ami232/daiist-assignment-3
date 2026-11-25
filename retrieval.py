"""
Search over the committed index. Used by server.py (the `search` tool) and evaluate.py.

Three ways to rank the same chunks, so they can be compared without re-embedding anything:
    dense   cosine similarity between the query vector and each chunk vector
    bm25    keyword match (no API call at all)
    hybrid  dense and bm25 rankings merged with reciprocal rank fusion (RRF)

Only the query needs an embedding at search time (1 text of the daily quota).
"""

from __future__ import annotations

import math
import re
from dataclasses import dataclass

import numpy as np

import index

MODES = ("dense", "bm25", "hybrid")
SERVING_MODE = "hybrid"      # which ranking server.py uses (set it by the numbers in evaluate.py)
RRF_K = 60                   # standard constant: score = sum over rankings of 1 / (RRF_K + rank)
POOL = 40                    # how many candidates each ranking contributes to the fusion
STOPWORDS = set(
    "a an the of to in on for and or by with as at is are be been it its this that these those from "
    "which what how when where who whom do does did should must shall may can could would will not no "
    "than then there their they them if into under over about between any all each such per".split()
)


def tokens(text: str) -> list[str]:
    return [t for t in re.findall(r"[a-z0-9]+", text.lower()) if t not in STOPWORDS and len(t) > 1]


@dataclass
class Hit:
    chunk: dict
    score: float          # ranking score (cosine, BM25 or RRF depending on the mode)
    dense: float | None   # cosine similarity of the query with this chunk, when known

    @property
    def source(self) -> str:
        return self.chunk["source"]

    @property
    def pages(self) -> tuple[int, int]:
        return self.chunk["page_start"], self.chunk["page_end"]

    @property
    def citation(self) -> str:
        a, b = self.pages
        return f"[{self.source}, p. {a}]" if a == b else f"[{self.source}, p. {a}-{b}]"


class Retriever:
    def __init__(self, design: str | None = None, require_vectors: bool = True):
        self.design = design or index.SERVING_DESIGN
        self.require_vectors = require_vectors   # False: also keep chunks with no vector (bm25 only)
        self.reload()

    def reload(self) -> None:
        vecs = index.load_vectors()
        records = index.read_chunks(self.design)
        self.chunks = [r for r in records if r["vec_key"] in vecs or not self.require_vectors]
        self.not_embedded = sum(r["vec_key"] not in vecs for r in self.chunks) if not self.require_vectors else len(records) - len(self.chunks)
        if self.chunks:
            zero = [0.0] * index.EMBED_DIM
            m = np.array([vecs.get(r["vec_key"], zero) for r in self.chunks], dtype=np.float32)
            self.matrix = m / np.maximum(np.linalg.norm(m, axis=1, keepdims=True), 1e-9)
        else:
            self.matrix = np.zeros((0, index.EMBED_DIM), dtype=np.float32)
        # BM25 statistics
        self._tf = [self._count(tokens(r["section"] + " " + r["text"])) for r in self.chunks]
        self._len = np.array([sum(tf.values()) for tf in self._tf], dtype=np.float32)
        self._avg = float(self._len.mean()) if len(self._len) else 1.0
        df: dict[str, int] = {}
        for tf in self._tf:
            for t in tf:
                df[t] = df.get(t, 0) + 1
        n = len(self._tf)
        self._idf = {t: math.log(1 + (n - d + 0.5) / (d + 0.5)) for t, d in df.items()}

    @staticmethod
    def _count(toks: list[str]) -> dict[str, int]:
        counts: dict[str, int] = {}
        for t in toks:
            counts[t] = counts.get(t, 0) + 1
        return counts

    # --- rankings -------------------------------------------------------------------------
    def _dense_scores(self, qvec: list[float]) -> np.ndarray:
        q = np.array(qvec, dtype=np.float32)
        q /= max(float(np.linalg.norm(q)), 1e-9)
        return self.matrix @ q

    def _bm25_scores(self, query: str, k1: float = 1.5, b: float = 0.75) -> np.ndarray:
        scores = np.zeros(len(self.chunks), dtype=np.float32)
        for t in set(tokens(query)):
            idf = self._idf.get(t)
            if idf is None:
                continue
            for i, tf in enumerate(self._tf):
                f = tf.get(t)
                if f:
                    scores[i] += idf * f * (k1 + 1) / (f + k1 * (1 - b + b * self._len[i] / self._avg))
        return scores

    def search(self, query: str, k: int = 5, mode: str = "hybrid", qvec: list[float] | None = None) -> list[Hit]:
        """Top-k chunks. dense and hybrid need a query vector: pass qvec or one is embedded (1 API call)."""
        if mode not in MODES:
            raise ValueError(f"mode must be one of {MODES}")
        if not self.chunks:
            return []
        dense = None
        if mode in ("dense", "hybrid"):
            if qvec is None:
                qvec = index.embed_query(query)
            dense = self._dense_scores(qvec)
        if mode == "dense":
            order = np.argsort(-dense)[:k]
            return [Hit(self.chunks[i], float(dense[i]), float(dense[i])) for i in order]
        bm25 = self._bm25_scores(query)
        if mode == "bm25":
            order = [i for i in np.argsort(-bm25)[:k] if bm25[i] > 0]
            return [Hit(self.chunks[i], float(bm25[i]), float(dense[i]) if dense is not None else None) for i in order]
        fused: dict[int, float] = {}
        for ranking in (np.argsort(-dense)[:POOL], [i for i in np.argsort(-bm25)[:POOL] if bm25[i] > 0]):
            for rank, i in enumerate(ranking):
                fused[int(i)] = fused.get(int(i), 0.0) + 1.0 / (RRF_K + rank + 1)
        top = sorted(fused, key=fused.get, reverse=True)[:k]
        return [Hit(self.chunks[i], fused[i], float(dense[i])) for i in top]


def format_hits(query: str, hits: list[Hit], mode: str) -> str:
    """What the search tool returns: numbered passages, each with its citation to copy."""
    if not hits:
        return f'No passages found for "{query}".'
    lines = [f'{len(hits)} passages for "{query}" ({mode} search). Cite a passage as shown in its brackets.', ""]
    for n, h in enumerate(hits, 1):
        c = h.chunk
        where = f"section: {c['section']}" if c.get("section") else "section: -"
        paras = f", paragraphs {c['paras']}" if c.get("paras") else ""
        lines.append(f"[{n}] {h.citation} {c['title']} ({where}{paras})")
        lines.append(c["text"])
        lines.append("")
    return "\n".join(lines).rstrip()


def page_overlap(hit: Hit, source: str, first: int, last: int) -> bool:
    """True if the hit is from `source` and its pages overlap [first, last]."""
    a, b = hit.pages
    return hit.source == source and a <= last and first <= b
