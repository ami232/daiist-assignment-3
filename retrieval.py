"""
Search over the committed index. Used by server.py (the search tool) and
evaluate.py (hit rates). Three methods over either chunking design:

- vector: cosine similarity of gemini-embedding-2 vectors (ChromaDB)
- keyword: BM25 over the chunk text
- hybrid: reciprocal rank fusion of the two lists

Query vectors are cached in index/query_cache.json, so the same question is
embedded once, whatever the design or method, and re-runs cost no quota.
"""

from __future__ import annotations

import json
import math
import re
from collections import Counter
from functools import lru_cache

import index as ix

QUERY_CACHE = ix.INDEX_DIR / "query_cache.json"
CANDIDATES = 30       # how deep each list goes before fusion
RRF_K = 60            # standard reciprocal-rank-fusion constant
METHODS = ("vector", "keyword", "hybrid")

STOPWORDS = set("""a an and are as at be by can could do does for from has have how i if in into is it its
may must of on or our shall should so such than that the their them then there these they this those to under
was we what when where which who will with without would you your us any all also been being other""".split())

_query_cache: dict[str, list[float]] | None = None


def _load_cache() -> dict[str, list[float]]:
    global _query_cache
    if _query_cache is None:
        _query_cache = json.loads(QUERY_CACHE.read_text()) if QUERY_CACHE.exists() else {}
    return _query_cache


def embed_query(query: str) -> list[float]:
    cache = _load_cache()
    key = query.strip()
    if key not in cache:
        cache[key] = [round(x, 6) for x in ix.embed_texts([ix.query_prompt(key)])[0]]
        QUERY_CACHE.parent.mkdir(exist_ok=True)
        QUERY_CACHE.write_text(json.dumps(cache))
    return cache[key]


# ---------------------------------------------------------------------- keyword


def tokens(text: str) -> list[str]:
    out = []
    for t in re.findall(r"[a-z0-9]+", text.lower()):
        if t in STOPWORDS or len(t) < 2:
            continue
        if len(t) > 4 and t.endswith("s") and not t.endswith("ss"):
            t = t[:-1]                      # crude plural folding: "obligations" -> "obligation"
        out.append(t)
    return out


class BM25:
    def __init__(self, texts: list[str], k1: float = 1.5, b: float = 0.75):
        self.docs = [Counter(tokens(t)) for t in texts]
        self.lens = [sum(d.values()) for d in self.docs]
        self.avg = sum(self.lens) / max(len(self.lens), 1)
        df = Counter(t for d in self.docs for t in d)
        n = len(self.docs)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}
        self.k1, self.b = k1, b

    def scores(self, query: str) -> list[float]:
        q = tokens(query)
        out = []
        for d, length in zip(self.docs, self.lens):
            s = 0.0
            for t in q:
                f = d.get(t)
                if f:
                    s += self.idf[t] * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * length / self.avg))
            out.append(s)
        return out


@lru_cache(maxsize=None)
def _corpus(design: str, version: int):
    got = ix.collection(design).get(include=["documents", "metadatas"])
    return got["ids"], got["documents"], got["metadatas"], BM25(got["documents"])


_versions: dict[str, int] = {}


def corpus(design: str):
    return _corpus(design, _versions.get(design, 0))


def invalidate(design: str) -> None:
    """Call after add_document changes a collection, so BM25 is rebuilt."""
    _versions[design] = _versions.get(design, 0) + 1


# ----------------------------------------------------------------------- search


def _allowed(meta: dict, base_only: bool) -> bool:
    return not (base_only and meta.get("added"))


def vector_ranked(query: str, design: str, base_only: bool = False, depth: int = CANDIDATES) -> list[tuple[str, float]]:
    col = ix.collection(design)
    where = {"added": False} if base_only else None
    res = col.query(query_embeddings=[embed_query(query)], n_results=depth, where=where, include=["distances"])
    return [(i, 1 - d) for i, d in zip(res["ids"][0], res["distances"][0])]


def keyword_ranked(query: str, design: str, base_only: bool = False, depth: int = CANDIDATES) -> list[tuple[str, float]]:
    ids, _, metas, bm25 = corpus(design)
    scored = [(i, s) for i, s, m in zip(ids, bm25.scores(query), metas) if s > 0 and _allowed(m, base_only)]
    return sorted(scored, key=lambda x: -x[1])[:depth]


def hybrid_ranked(query: str, design: str, base_only: bool = False, depth: int = CANDIDATES) -> list[tuple[str, float]]:
    fused: dict[str, float] = {}
    for ranked in (vector_ranked(query, design, base_only, depth), keyword_ranked(query, design, base_only, depth)):
        for rank, (i, _) in enumerate(ranked, start=1):
            fused[i] = fused.get(i, 0.0) + 1 / (RRF_K + rank)
    return sorted(fused.items(), key=lambda x: -x[1])[:depth]


def search(query: str, design: str | None = None, method: str | None = None, k: int | None = None,
           base_only: bool = False) -> list[dict]:
    """Top-k chunks as dicts with id, text, metadata, score and rank."""
    cfg = ix.chosen_design()
    design, method, k = design or cfg["design"], method or cfg["method"], k or cfg["k"]
    ranked = {"vector": vector_ranked, "keyword": keyword_ranked, "hybrid": hybrid_ranked}[method](query, design, base_only)[:k]
    if not ranked:
        return []
    got = ix.collection(design).get(ids=[i for i, _ in ranked], include=["documents", "metadatas"])
    by_id = {i: (d, m) for i, d, m in zip(got["ids"], got["documents"], got["metadatas"])}
    hits = []
    for rank, (i, score) in enumerate(ranked, start=1):
        doc, meta = by_id[i]
        hits.append({"id": i, "rank": rank, "score": round(score, 4), "text": doc, "metadata": meta})
    return hits


def citation(meta: dict) -> str:
    """The citation tag the agent must copy: [GDPR, Article 6]."""
    return f"[{meta['source']}, {meta['location']}]"


def format_hits(hits: list[dict]) -> str:
    if not hits:
        return "No passages found."
    blocks = []
    for h in hits:
        m = h["metadata"]
        part = f" (part {m['part']} of {m['parts']})" if m.get("parts", 1) > 1 else ""
        blocks.append(
            f"Result {h['rank']}  cite as {citation(m)}{part}  relevance {h['score']}\n"
            f"Source: {m['title']} — {m['url']}\n"
            f"{h['text']}"
        )
    return "\n\n---\n\n".join(blocks)
