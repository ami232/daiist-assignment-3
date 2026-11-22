"""
Retrieval shared by server.py and evaluate.py.

Three search methods over the chunks stored by index.py:
  - "vector": cosine similarity on Gemini embeddings (ChromaDB)
  - "bm25":   keyword search (Okapi BM25), no API calls
  - "hybrid": both lists fused with Reciprocal Rank Fusion

Query embeddings are cached in index/query_cache.json so repeated questions
(evaluation runs, the agent retrying) don't spend the daily embedding quota.
"""

from __future__ import annotations

import json
import math
import re
import unicodedata
from collections import Counter
from pathlib import Path

import index as ix

# The configuration server.py uses. Set it from the numbers in eval/retrieval_results.csv.
SEARCH_DESIGN = "articles"
SEARCH_METHOD = "vector"
SEARCH_K = 5

QUERY_CACHE = ix.INDEX_DIR / "query_cache.json"
RRF_K = 60  # standard constant for Reciprocal Rank Fusion

STOPWORDS = set("""
a al algo ante antes como con contra cual cuando de del desde donde durante e el ella ellas ellos en entre era es esa
ese eso esta este esto estos estas fue ha han hasta hay la las le les lo los mas me mi muy no nos o os para pero por
que quien se sea ser si sin sobre son su sus tambien te tiene tu un una uno unos unas y ya puede pueden debe deberá
será cada otro otra otros otras dicho dicha mismo misma
""".split())


# ---------------------------------------------------------------- query embeddings (cached)

def _load_cache() -> dict:
    if QUERY_CACHE.exists():
        return json.loads(QUERY_CACHE.read_text(encoding="utf-8"))
    return {}


_cache: dict | None = None


def embed_query(query: str) -> list[float]:
    global _cache
    if _cache is None:
        _cache = _load_cache()
    key = query.strip()
    if key not in _cache:
        _cache[key] = ix.embed([key], task="RETRIEVAL_QUERY")[0]
        QUERY_CACHE.write_text(json.dumps(_cache), encoding="utf-8")
    return _cache[key]


# ---------------------------------------------------------------- BM25

def tokens(text: str) -> list[str]:
    text = unicodedata.normalize("NFKD", text.lower())
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return [t for t in re.findall(r"[a-z0-9]+", text) if t not in STOPWORDS and len(t) > 1]


class BM25:
    def __init__(self, ids: list[str], docs: list[str], k1: float = 1.5, b: float = 0.75):
        self.ids, self.k1, self.b = ids, k1, b
        self.tf = [Counter(tokens(d)) for d in docs]
        self.len = [sum(tf.values()) for tf in self.tf]
        self.avg = sum(self.len) / max(len(self.len), 1)
        df = Counter(t for tf in self.tf for t in tf)
        n = len(docs)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}

    def search(self, query: str, k: int) -> list[str]:
        q = tokens(query)
        scores = []
        for i, tf in enumerate(self.tf):
            s = 0.0
            for t in q:
                if t in tf:
                    f = tf[t]
                    s += self.idf[t] * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * self.len[i] / self.avg))
            scores.append(s)
        order = sorted(range(len(scores)), key=lambda i: -scores[i])
        return [self.ids[i] for i in order[:k] if scores[i] > 0]


_bm25: dict[str, tuple[int, BM25]] = {}


def bm25_index(design: str) -> BM25:
    col = ix.collection(design)
    count = col.count()
    if design not in _bm25 or _bm25[design][0] != count:  # rebuilt after add_document
        data = col.get(include=["documents"])
        _bm25[design] = (count, BM25(data["ids"], data["documents"]))
    return _bm25[design][1]


# ---------------------------------------------------------------- search

def _vector_ids(query: str, design: str, k: int) -> list[str]:
    res = ix.collection(design).query(query_embeddings=[embed_query(query)], n_results=k, include=[])
    return res["ids"][0]


def search(query: str, design: str = SEARCH_DESIGN, method: str = SEARCH_METHOD, k: int = SEARCH_K) -> list[dict]:
    """Return the top-k chunks as dicts: id, text, metadata, rank."""
    if method == "vector":
        ids = _vector_ids(query, design, k)
    elif method == "bm25":
        ids = bm25_index(design).search(query, k)
    elif method == "hybrid":
        pool = 20
        fused: dict[str, float] = {}
        for ranked in (_vector_ids(query, design, pool), bm25_index(design).search(query, pool)):
            for rank, cid in enumerate(ranked):
                fused[cid] = fused.get(cid, 0.0) + 1.0 / (RRF_K + rank + 1)
        ids = sorted(fused, key=lambda c: -fused[c])[:k]
    else:
        raise ValueError(f"unknown method {method!r}")
    if not ids:
        return []
    got = ix.collection(design).get(ids=ids, include=["documents", "metadatas"])
    by_id = {i: (d, m) for i, d, m in zip(got["ids"], got["documents"], got["metadatas"])}
    return [{"id": i, "text": by_id[i][0], "metadata": by_id[i][1], "rank": r + 1}
            for r, i in enumerate(ids) if i in by_id]


def citation(meta: dict) -> str:
    """The citation label the agent must copy, e.g. [LAU, Artículo 36]."""
    return f"[{meta['source']}, {meta['location']}]"


def format_results(hits: list[dict]) -> str:
    if not hits:
        return "No results. The corpus has nothing matching this query."
    out = []
    for h in hits:
        m = h["metadata"]
        body = h["text"].split("\n", 1)[1] if "\n" in h["text"] else h["text"]
        part = f" (parte {m['part']}/{m['parts']})" if m.get("parts", 1) > 1 else ""
        out.append(
            f"--- Result {h['rank']} ---\n"
            f"Cite as: {citation(m)}{part}\n"
            f"Law: {m['title']} | Section: {m.get('section') or '-'} | "
            f"Consolidated text as of {m.get('version_date') or '?'} | {m['url']}\n"
            f"{body}"
        )
    return "\n\n".join(out)
