"""
Retrieval over the saved index: vector search, BM25 and a hybrid of both.

Used by server.py (search tool) and evaluate.py (hit rate). It only reads
index/; the only thing it ever embeds is the user's query, and each query is
cached in index/query_cache.json so that re-running an evaluation costs nothing.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
from collections import Counter
from pathlib import Path

import numpy as np

import index as ix

CHOSEN_MODE = "hybrid"          # "vector" or "hybrid"; chosen from the numbers in REPORT.md
RRF_K = 60                      # reciprocal rank fusion constant
CANDIDATES = 50                 # how deep each ranking is before fusing

_STOP = frozenset(
    "a an and are as at be by can do does for from has have how if in into is it its of on or "
    "shall that the their them there these this to under what when where which who will with must may".split()
)
_TOKEN = re.compile(r"[a-z0-9]+")


def tokens(text: str) -> list[str]:
    return [t for t in _TOKEN.findall(text.lower()) if t not in _STOP]


# --------------------------------------------------------- query embedding ---
def _cache_path() -> Path:
    return ix.INDEX_DIR / "query_cache.json"


def _load_cache() -> dict:
    p = _cache_path()
    if p.is_file():
        try:
            return json.loads(p.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def embed_query(query: str) -> np.ndarray:
    """Normalised query vector. Cached on disk by (model, dimension, text)."""
    query = " ".join(query.split())
    key = hashlib.sha1(f"{ix.EMBED_MODEL}|{ix.EMBED_DIM}|{query}".encode()).hexdigest()
    cache = _load_cache()
    if key not in cache:
        cache[key] = ix.embed_texts([ix.query_input(query)])[0]
        p = _cache_path()
        p.parent.mkdir(parents=True, exist_ok=True)
        tmp = p.with_suffix(".tmp")
        tmp.write_text(json.dumps(cache, separators=(",", ":")), encoding="utf-8")
        tmp.replace(p)
    return np.asarray(cache[key], dtype=np.float32)


# ------------------------------------------------------------------ index ----
class IndexView:
    """One design's chunks in memory: vectors for cosine search, token counts for BM25."""

    def __init__(self, design: str = ix.CHOSEN_DESIGN):
        self.design = design
        self.reload()

    def reload(self) -> None:
        store = ix.load_store(self.design)
        # chunks without a vector (added while the embedding quota was used up) are kept for keyword search
        self.chunks: list[dict] = list(store.values())
        self.has_vector = np.asarray([bool(c.get("vector")) for c in self.chunks], dtype=bool)
        dim = next((len(c["vector"]) for c in self.chunks if c.get("vector")), ix.EMBED_DIM)
        self.matrix = np.zeros((len(self.chunks), dim), dtype=np.float32)
        for i, c in enumerate(self.chunks):
            if c.get("vector"):
                self.matrix[i] = c["vector"]
        self._docs = [Counter(tokens(f"{c['header']} {c['body']}")) for c in self.chunks]
        self._len = np.asarray([sum(d.values()) for d in self._docs], dtype=np.float32)
        self._avg = float(self._len.mean()) if len(self._len) else 1.0
        df: Counter = Counter()
        for d in self._docs:
            df.update(d.keys())
        n = max(len(self.chunks), 1)
        self._idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}

    def __len__(self) -> int:
        return len(self.chunks)

    def sources(self) -> list[str]:
        return sorted({c["source"] for c in self.chunks})

    # -- rankings -------------------------------------------------------------
    def _bm25(self, query: str, k1: float = 1.5, b: float = 0.75) -> np.ndarray:
        scores = np.zeros(len(self.chunks), dtype=np.float32)
        q = tokens(query)
        for i, d in enumerate(self._docs):
            norm = k1 * (1 - b + b * self._len[i] / self._avg)
            s = 0.0
            for t in q:
                f = d.get(t)
                if f:
                    s += self._idf.get(t, 0.0) * f * (k1 + 1) / (f + norm)
            scores[i] = s
        return scores

    def search(
        self,
        query: str,
        k: int = 5,
        mode: str = CHOSEN_MODE,
        source: str | None = None,
        query_vector: np.ndarray | None = None,
    ) -> list[dict]:
        """Top-k chunks, each a copy of its record (without vector) plus `similarity` (cosine) and `rank`.

        If the query cannot be embedded because the daily quota is used up, the ranking is by keywords
        (BM25) only. Chunks without a vector are only found by keywords. Such hits have
        `keyword_only` = True and similarity 0.
        """
        if not self.chunks:
            return []
        if mode not in ("vector", "hybrid"):
            raise ValueError(f"Unknown mode {mode!r}")
        if query_vector is not None:
            qv = query_vector
        else:
            try:
                qv = embed_query(query)
            except ix.QuotaExhausted:
                qv = None
        cosine = self.matrix @ qv if qv is not None else np.zeros(len(self.chunks), dtype=np.float32)
        allowed = np.ones(len(self.chunks), dtype=bool)
        if source:
            wanted = source.strip().lower()
            allowed = np.asarray([wanted in c["source"].lower() or wanted == c["doc"].lower() for c in self.chunks])
            if not allowed.any():
                return []
        vec_order = [i for i in np.argsort(-cosine) if allowed[i] and self.has_vector[i]][:CANDIDATES] if qv is not None else []
        bm_order: list[int] = []
        if qv is None or mode == "hybrid":
            bm = self._bm25(query)
            bm_order = [i for i in np.argsort(-bm) if allowed[i] and bm[i] > 0][:CANDIDATES]
        if qv is None:
            order = bm_order
        elif mode == "vector":
            order = vec_order
        else:
            fused: dict[int, float] = {}
            for ranking in (vec_order, bm_order):
                for rank, i in enumerate(ranking):
                    fused[i] = fused.get(i, 0.0) + 1.0 / (RRF_K + rank + 1)
            order = sorted(fused, key=lambda i: -fused[i])
        hits = []
        for rank, i in enumerate(order[:k], 1):
            rec = {key: val for key, val in self.chunks[i].items() if key != "vector"}
            rec["keyword_only"] = bool(qv is None or not self.has_vector[i])
            rec["similarity"] = 0.0 if rec["keyword_only"] else round(float(cosine[i]), 4)
            rec["rank"] = rank
            hits.append(rec)
        return hits


# ----------------------------------------------------------------- output ----
def format_hits(hits: list[dict]) -> str:
    """What the model reads: numbered passages, each headed by the citation to copy."""
    if not hits:
        return "No passages found."
    out = [f"{len(hits)} passages, best first. Cite as [source | location]."]
    if any(h.get("keyword_only") for h in hits):
        out.append("Note: passages marked (keyword match) were found by matching words only, because their vectors are "
                   "missing or the embedding quota is used up; there is no similarity score for them, so judge them by their text.")
    for h in hits:
        title = f' \u2014 "{h["title"]}"' if h.get("title") else ""
        score = "keyword match" if h.get("keyword_only") else f"similarity {h['similarity']:.2f}"
        out.append(f"\n[{h['rank']}] {h['source']} | {h['location']}{title} ({score})")
        out.append(h["body"])
    return "\n".join(out)


_HEADER = re.compile(
    r'^\[(?P<rank>\d+)\] (?P<source>[^|\n]+?) \| (?P<location>.+?)(?: \u2014 "(?P<title>[^\n]*)")? \((?:similarity (?P<sim>-?[\d.]+)|(?P<kw>keyword match))\)$',
    re.M,
)


def parse_hits(text: str) -> list[dict]:
    """Inverse of format_hits: the passages a tool result contained (source, location, body)."""
    matches = list(_HEADER.finditer(text))
    hits = []
    for n, m in enumerate(matches):
        end = matches[n + 1].start() if n + 1 < len(matches) else len(text)
        hits.append({
            "rank": int(m["rank"]), "source": m["source"].strip(), "location": m["location"].strip(),
            "title": m["title"] or "", "similarity": float(m["sim"]) if m["sim"] else 0.0, "keyword_only": bool(m["kw"]),
            "body": text[m.end():end].strip(),
        })
    return hits


# ------------------------------------------------------- citation matching ---
_UNIT = re.compile(r"(Article\s+\d+[a-z]?|Recital\s+\d+|Annex\s+[IVXLC0-9]+|p\.\s*\d+)", re.I)


def unit_of(location: str) -> str:
    """'Article 28(3) (part 2/4)' -> 'article 28'; 'Annex III, points 1-3' -> 'annex iii'."""
    m = _UNIT.search(location or "")
    return re.sub(r"\s+", " ", m.group(1)).lower() if m else (location or "").strip().lower()


def units_of(chunk: dict) -> set[str]:
    return {unit_of(u) for u in chunk.get("units") or [chunk["location"]]}


def norm_source(s: str) -> str:
    return re.sub(r"[^a-z0-9]+", "", s.lower())
