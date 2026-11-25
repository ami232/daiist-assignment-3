"""
Retrieval over index/: dense (Gemini embeddings), BM25 (keywords) and hybrid (both,
merged with reciprocal rank fusion).

All three read the same stored vectors, so comparing them costs no extra embeddings,
only one embedding per distinct query. Query vectors are cached in index/query_cache.json
(committed), which keeps the free-tier quota for the questions that really are new.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from collections import Counter
from dataclasses import dataclass

import numpy as np

import index as ix

QUERY_CACHE = ix.INDEX_DIR / "query_cache.json"
MODES = ("dense", "bm25", "hybrid")
RRF_K = 60

STOPWORDS = set(
    "a an and are as at be by for from how in is it of on or that the their this to what when where which who why with "
    "does do did can should would about into than then there these those its not".split()
)


def tokenize(text: str) -> list[str]:
    return [t for t in re.findall(r"[a-z0-9]+", text.lower()) if t not in STOPWORDS]


@dataclass
class Hit:
    id: str
    source: str
    title: str
    url: str
    section: str
    location: str
    page_start: int
    page_end: int
    text: str
    score: float          # score of the mode that ranked it (cosine, BM25 or RRF)
    similarity: float     # cosine similarity to the query, whatever the mode

    @property
    def citation(self) -> str:
        return f"[{self.source}, {self.location}]"


def _load_cache() -> dict:
    try:
        return json.loads(QUERY_CACHE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def embed_query(query: str) -> np.ndarray:
    """Embed a query, reusing the cached vector when we have seen the exact query before."""
    key = hashlib.sha256(f"{ix.EMBED_MODEL}|{ix.EMBED_DIM}|{query}".encode()).hexdigest()[:20]
    cache = _load_cache()
    if key not in cache:
        cache[key] = ix.embed_texts([query])[0]
        QUERY_CACHE.write_text(json.dumps(cache), encoding="utf-8")
    return np.array(cache[key], dtype="float32")


class Retriever:
    def __init__(self) -> None:
        self.refresh()

    def refresh(self) -> None:
        """(Re)load everything from index/. Never embeds a chunk."""
        collection = ix.get_collection()
        data = collection.get(include=["documents", "metadatas", "embeddings"])
        self.ids: list[str] = list(data["ids"])
        self.texts: list[str] = list(data["documents"])
        self.metas: list[dict] = list(data["metadatas"])
        self.matrix = np.array(data["embeddings"], dtype="float32") if len(self.ids) else np.zeros((0, ix.EMBED_DIM), "float32")
        self._build_bm25()

    def __len__(self) -> int:
        return len(self.ids)

    # ---- BM25 ------------------------------------------------------------
    def _build_bm25(self, k1: float = 1.5, b: float = 0.75) -> None:
        self.k1, self.b = k1, b
        self.tokens = [tokenize(f"{m.get('section', '')} {t}") for m, t in zip(self.metas, self.texts)]
        self.tf = [Counter(toks) for toks in self.tokens]
        self.doc_len = np.array([len(t) for t in self.tokens], dtype="float32")
        self.avg_len = float(self.doc_len.mean()) if len(self.tokens) else 0.0
        df = Counter()
        for counter in self.tf:
            df.update(counter.keys())
        n = len(self.tokens)
        self.idf = {t: math.log(1 + (n - d + 0.5) / (d + 0.5)) for t, d in df.items()}

    def bm25_scores(self, query: str) -> np.ndarray:
        scores = np.zeros(len(self.ids), dtype="float32")
        terms = tokenize(query)
        for i, tf in enumerate(self.tf):
            norm = self.k1 * (1 - self.b + self.b * self.doc_len[i] / (self.avg_len or 1.0))
            for t in terms:
                f = tf.get(t)
                if f:
                    scores[i] += self.idf[t] * f * (self.k1 + 1) / (f + norm)
        return scores

    # ---- Search ----------------------------------------------------------
    def dense_scores(self, query: str) -> np.ndarray:
        return self.matrix @ embed_query(query)          # vectors are unit length: dot product = cosine

    def search(self, query: str, k: int = 5, mode: str = "hybrid", source: str | None = None) -> list[Hit]:
        if mode not in MODES:
            raise ValueError(f"mode must be one of {MODES}")
        if not len(self):
            return []
        allowed = np.array([source is None or m["source"] == source for m in self.metas])
        sim = np.full(len(self), -1.0, dtype="float32")
        sim[:] = self.dense_scores(query) if mode != "bm25" else 0.0
        if mode == "bm25":
            scores = self.bm25_scores(query)
        elif mode == "dense":
            scores = sim
        else:
            dense_rank = {i: r for r, i in enumerate(np.argsort(-sim)[:50])}
            bm25 = self.bm25_scores(query)
            bm25_rank = {i: r for r, i in enumerate(np.argsort(-bm25)[:50]) if bm25[i] > 0}
            scores = np.zeros(len(self), dtype="float32")
            for ranks in (dense_rank, bm25_rank):
                for i, r in ranks.items():
                    scores[i] += 1.0 / (RRF_K + r + 1)
        scores = np.where(allowed, scores, -np.inf)
        order = [int(i) for i in np.argsort(-scores)[:k] if np.isfinite(scores[i])]
        if mode == "bm25":
            order = [i for i in order if scores[i] > 0]
        return [self._hit(i, float(scores[i]), float(sim[i])) for i in order]

    def _hit(self, i: int, score: float, similarity: float) -> Hit:
        m = self.metas[i]
        return Hit(
            id=self.ids[i], source=m["source"], title=m["title"], url=m["url"], section=m.get("section", ""),
            location=m["location"], page_start=int(m["page_start"]), page_end=int(m["page_end"]),
            text=self.texts[i], score=score, similarity=similarity,
        )


def format_hits(hits: list[Hit]) -> str:
    """The text the model reads. Each result starts with the citation it must use."""
    if not hits:
        return "No results."
    parts = []
    for n, h in enumerate(hits, start=1):
        where = f" - section: {h.section}" if h.section else ""
        parts.append(f"[{n}] cite as {h.citation}{where} (similarity {h.similarity:.2f})\n{h.text}")
    return "\n\n".join(parts)
