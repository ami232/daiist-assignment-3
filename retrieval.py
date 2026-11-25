"""
Search over the stored index. Used by server.py (the served design) and by
evaluate.py (every design, to compare hit rates).

Designs:
  fixed            : 250-word windows, vector search
  structure        : article/paragraph chunks with context header, vector search
  structure_hybrid : structure chunks, vector + BM25 keyword search fused (RRF)

Changing k or the search method costs no embeddings; only queries are embedded
(and cached in index/vectors.jsonl).
"""

from __future__ import annotations

import math
import os
import re
from collections import Counter
from functools import lru_cache

import numpy as np

import index as ix

TOKEN = re.compile(r"[a-z0-9]+(?:\(\d+\))?")
STOP = set("the a an of to in and or for on by is are be with that this which as at from it its any "
           "under shall may not where whether their such other into been has have".split())


def tokens(text: str) -> list[str]:
    return [t for t in TOKEN.findall(text.lower()) if t not in STOP]


class Store:
    """All chunks of one chunking design, their vectors and a BM25 index."""

    def __init__(self, base: str):
        self.base = base
        self.chunks = ix.read_chunks(base)
        if not self.chunks:
            raise RuntimeError(f"index/chunks_{base}.jsonl is missing or empty. Run `main.py index` first.")
        self.collection = ix.chroma_collection(base)
        if self.collection.count() < len(self.chunks):
            raise RuntimeError(f"Chroma collection '{base}' holds {self.collection.count()} of "
                               f"{len(self.chunks)} chunks. Run `main.py index`.")
        self.pos = {c.id: i for i, c in enumerate(self.chunks)}
        # BM25
        self.docs = [tokens(c.embed_text) for c in self.chunks]
        self.avgdl = sum(map(len, self.docs)) / len(self.docs)
        df = Counter(t for d in self.docs for t in set(d))
        n = len(self.docs)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}
        self.tf = [Counter(d) for d in self.docs]

    def mask(self, exclude_added: bool) -> np.ndarray:
        return np.array([not (exclude_added and c.added) for c in self.chunks])

    def vector_rank(self, qv: np.ndarray, exclude_added: bool, n: int = 50) -> list[int]:
        """Nearest chunks by cosine distance, from the Chroma collection."""
        res = self.collection.query(query_embeddings=[qv.tolist()], n_results=n,
                                    where={"added": False} if exclude_added else None)
        return [self.pos[i] for i in res["ids"][0] if i in self.pos]

    def bm25_rank(self, query: str, mask: np.ndarray, k1: float = 1.5, b: float = 0.75) -> list[int]:
        q = tokens(query)
        scores = np.zeros(len(self.chunks))
        for i, tf in enumerate(self.tf):
            if not mask[i]:
                scores[i] = -np.inf
                continue
            dl = len(self.docs[i])
            scores[i] = sum(self.idf.get(t, 0) * tf[t] * (k1 + 1) / (tf[t] + k1 * (1 - b + b * dl / self.avgdl))
                            for t in q if t in tf)
        return [int(i) for i in np.argsort(-scores) if mask[i]]


@lru_cache(maxsize=None)
def store(base: str) -> Store:
    return Store(base)


def search(query: str, design: str | None = None, k: int = 5, exclude_added: bool | None = None) -> list[dict]:
    """Top-k chunks for a query as dicts with text, source, location, units, score rank."""
    if design is None:
        cfg = ix.served_design()
        design = cfg
        import json
        if ix.CONFIG_FILE.exists() and json.loads(ix.CONFIG_FILE.read_text()).get("hybrid"):
            design = f"{cfg}_hybrid"
    if exclude_added is None:
        exclude_added = os.environ.get("CORPUS_EXCLUDE_ADDED") == "1"
    hybrid = design.endswith("_hybrid")
    s = store(design.removesuffix("_hybrid"))
    mask = s.mask(exclude_added)
    vec = s.vector_rank(ix.embed_query(query), exclude_added)
    if hybrid:
        kw = s.bm25_rank(query, mask)
        rrf: dict[int, float] = {}
        for ranking in (vec[:50], kw[:50]):
            for r, i in enumerate(ranking):
                rrf[i] = rrf.get(i, 0) + 1 / (60 + r + 1)
        order = sorted(rrf, key=rrf.get, reverse=True)
    else:
        order = vec
    out = []
    for r, i in enumerate(order[:k]):
        c = s.chunks[i]
        out.append({"rank": r + 1, "source": c.source, "location": c.location, "units": c.units,
                    "section": c.section, "text": c.text, "added": c.added})
    return out


def format_results(results: list[dict]) -> str:
    if not results:
        return "No results."
    parts = []
    for r in results:
        head = f"[{r['rank']}] source: {r['source']} | location: {r['location']}"
        if r["section"]:
            head += f" | section: {r['section']}"
        parts.append(f"{head}\ncite as: [{r['source']}, {r['location']}]\n{r['text']}")
    return "\n\n---\n\n".join(parts)


# ---- citation helpers shared by agent.py and evaluate.py -------------------
CITATION = re.compile(r"\[([A-Z][A-Z0-9_]+),\s*([^\]]+)\]")


def norm_unit(label: str) -> list[str]:
    """Expand a cited location into unit labels: 'paras 12-14' -> para 12..14,
    'paras 92, 104' -> para 92 and para 104, 'Article 5(1)' -> Article 5,
    'Recitals 31, 33, and Article 8' -> recital 31, recital 33, article 8."""
    label = re.sub(r"\s*\(part \d+\)", "", label.strip().rstrip("."))
    out, kind = [], None
    for part in re.split(r"\s*(?:,|;|\band\b|&)\s*", label):
        part = part.strip()
        if not part:
            continue
        m = re.match(r"(?i)(paras?\.?|paragraphs?|points?|recitals?|articles?|art\.)?\s*(\d+)[a-z]?(?:\(\d+\))*(?:\s*(?:-|–|to)\s*(\d+))?", part)
        if not m or not m.group(2):
            out.append(part.lower())
            continue
        if m.group(1):
            k = m.group(1).lower()
            kind = "article" if k.startswith("art") else "recital" if k.startswith("recital") else "para"
        if kind is None:
            out.append(part.lower())
            continue
        a, b = int(m.group(2)), m.group(3)
        out.extend(f"{kind} {n}" for n in range(a, int(b) + 1)) if b else out.append(f"{kind} {a}")
    return out or [label.lower()]


def chunk_units(r: dict) -> set[str]:
    out = set()
    for u in r["units"]:
        out.update(norm_unit(u))
    out.update(norm_unit(r["location"]))
    return out


def citations(answer: str) -> list[tuple[str, str]]:
    return CITATION.findall(answer)


def citation_valid(source: str, location: str, retrieved: list[dict]) -> bool:
    """A citation is valid if every unit it names (article, recital, paragraph)
    is covered by some passage of that source returned by search in this run."""
    covered = set()
    for r in retrieved:
        if r["source"] == source:
            covered |= chunk_units(r)
    return bool(covered) and set(norm_unit(location)) <= covered
