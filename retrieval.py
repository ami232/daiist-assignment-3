"""
Search over the committed index: dense (Gemini embeddings), BM25 (keywords)
and hybrid (reciprocal rank fusion of both). Used by server.py and evaluate.py.

All chunk vectors are loaded from index/ once; the corpus is never re-embedded.
Only queries are embedded, and their vectors are cached in
index/query_cache.json so that re-running the evaluation spends no quota.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from collections import Counter
from pathlib import Path

import numpy as np

import index as pipeline

DEFAULT_MODE = "dense"  # chosen from the retrieval evaluation (see REPORT.md); change if your numbers disagree
MODES = ("dense", "bm25", "hybrid")
RRF_K = 60
CANDIDATES = 50
TOKEN_RE = re.compile(r"[a-z0-9]+")
STOPWORDS = set(
    "a an and are as at be been by for from has have in is it its not of on or shall such "
    "that the their them they this those to was where which with may any".split()
)


def tokenize(text: str) -> list[str]:
    return [t for t in TOKEN_RE.findall(text.lower()) if t not in STOPWORDS]


class Store:
    """In-memory view of the index for fast dense, BM25 and hybrid search."""

    def __init__(self, index_dir: Path | None = None):
        self.index_dir = Path(index_dir or pipeline.INDEX_DIR)
        self.cache_path = self.index_dir / "query_cache.json"
        self._cache: dict | None = None
        self.reload()

    # -------------------------------------------------------------- loading

    def reload(self) -> None:
        """Re-read the collection (after add_document)."""
        col = pipeline.collection(self.index_dir)
        data = col.get(include=["documents", "metadatas", "embeddings"])
        self.ids = list(data["ids"])
        self.texts = list(data["documents"] if data["documents"] is not None else [])
        self.metas = list(data["metadatas"] if data["metadatas"] is not None else [])
        if self.ids:
            self.matrix = np.asarray(data["embeddings"], dtype=np.float32)
        else:
            self.matrix = np.zeros((0, pipeline.EMBED_DIM), dtype=np.float32)
        self._build_bm25()

    def _build_bm25(self) -> None:
        docs = [tokenize(t) for t in self.texts]
        self.tf = [Counter(d) for d in docs]
        self.doc_len = np.array([len(d) for d in docs], dtype=np.float32)
        self.avg_len = float(self.doc_len.mean()) if len(docs) else 1.0
        df = Counter()
        for d in docs:
            df.update(set(d))
        n = len(docs)
        self.idf = {t: math.log(1 + (n - c + 0.5) / (c + 0.5)) for t, c in df.items()}

    # -------------------------------------------------------------- scoring

    def embed_query(self, query: str) -> np.ndarray:
        if self._cache is None:
            try:
                self._cache = json.loads(self.cache_path.read_text(encoding="utf-8"))
            except (OSError, ValueError):
                self._cache = {}
        key = hashlib.sha1(f"{pipeline.EMBED_MODEL}|{query}".encode("utf-8")).hexdigest()
        if key not in self._cache:
            vector = pipeline.normalise(pipeline.embed_texts([query], task="RETRIEVAL_QUERY"))[0]
            self._cache[key] = [round(x, 6) for x in vector]
            self.cache_path.parent.mkdir(parents=True, exist_ok=True)
            self.cache_path.write_text(json.dumps(self._cache), encoding="utf-8")
        return np.asarray(self._cache[key], dtype=np.float32)

    def dense_scores(self, query: str) -> np.ndarray:
        return self.matrix @ self.embed_query(query)

    def bm25_scores(self, query: str, k1: float = 1.5, b: float = 0.75) -> np.ndarray:
        terms = tokenize(query)
        scores = np.zeros(len(self.ids), dtype=np.float32)
        for i, tf in enumerate(self.tf):
            norm = k1 * (1 - b + b * self.doc_len[i] / self.avg_len)
            scores[i] = sum(self.idf[t] * tf[t] * (k1 + 1) / (tf[t] + norm) for t in terms if t in tf)
        return scores

    def _rrf(self, rankings: list[np.ndarray], mask: np.ndarray) -> np.ndarray:
        fused = np.zeros(len(self.ids), dtype=np.float32)
        for scores in rankings:
            masked = np.where(mask, scores, -np.inf)
            for rank, i in enumerate(np.argsort(-masked)[:CANDIDATES], start=1):
                if np.isfinite(masked[i]):
                    fused[i] += 1.0 / (RRF_K + rank)
        return fused

    def _mask(self, source: str | None, kind: str | None) -> np.ndarray:
        mask = np.ones(len(self.ids), dtype=bool)
        if source:
            wanted = {s.strip().lower() for s in source.split(",") if s.strip()}
            mask &= np.array([m["source"].lower() in wanted for m in self.metas], dtype=bool)
        if kind:
            mask &= np.array([m["kind"] == kind for m in self.metas], dtype=bool)
        return mask

    # -------------------------------------------------------------- search

    def search(self, query: str, k: int = 5, mode: str = DEFAULT_MODE,
               source: str | None = None, kind: str | None = None) -> list[dict]:
        """Top-k chunks for the query. `source` filters by document (comma-separated
        names), `kind` by "article" or "recital"."""
        if mode not in MODES:
            raise ValueError(f"mode must be one of {MODES}")
        if not self.ids:
            return []
        mask = self._mask(source, kind)
        if not mask.any():
            return []
        if mode == "dense":
            scores = self.dense_scores(query)
        elif mode == "bm25":
            scores = self.bm25_scores(query)
        else:
            scores = self._rrf([self.dense_scores(query), self.bm25_scores(query)], mask)
        scores = np.where(mask, scores, -np.inf)
        order = [i for i in np.argsort(-scores)[:k] if np.isfinite(scores[i])]
        return [self._hit(i, rank, float(scores[i])) for rank, i in enumerate(order, start=1)]

    def _hit(self, i: int, rank: int, score: float) -> dict:
        meta = self.metas[i]
        return {
            "rank": rank,
            "id": self.ids[i],
            "score": round(score, 4),
            "source": meta["source"],
            "location": meta["location"],
            "heading": meta.get("heading", ""),
            "kind": meta.get("kind", ""),
            "part": int(meta.get("part", 1)),
            "text": self.texts[i],
        }

    def sources(self) -> list[str]:
        return sorted({m["source"] for m in self.metas})


# ------------------------------------------------------------------ formatting

RESULT_RE = re.compile(
    r"^\[(\d+)\] source: (.+?) \| location: (.+?)(?: \| title: (.*?))?(?: \| part: \d+)?$", re.M
)
FOOTER = "\n\nCite each claim as [source, location]"


def format_results(hits: list[dict]) -> str:
    """Text the model reads: one block per chunk with its citation header."""
    if not hits:
        return "No passages found."
    blocks = []
    for h in hits:
        title = f" | title: {h['heading']}" if h.get("heading") else ""
        part = f" | part: {h['part']}" if h.get("part", 1) > 1 else ""
        body = h["text"].split("\n", 1)[-1]  # drop the header line that was embedded
        blocks.append(f"[{h['rank']}] source: {h['source']} | location: {h['location']}{title}{part}\n{body}")
    first = hits[0]
    return "\n\n".join(blocks) + f"{FOOTER}, e.g. [{first['source']}, {first['location']}]."


def parse_results(text: str) -> list[dict]:
    """Inverse of format_results: recover source, location and text of each chunk
    from a search tool result (used by the agent's guardrail and the judge)."""
    text = text.split(FOOTER)[0]
    matches = list(RESULT_RE.finditer(text))
    chunks = []
    for j, m in enumerate(matches):
        end = matches[j + 1].start() if j + 1 < len(matches) else len(text)
        chunks.append({
            "source": m.group(2).strip(),
            "location": m.group(3).strip(),
            "heading": (m.group(4) or "").strip(),
            "text": text[m.end():end].strip(),
        })
    return chunks
