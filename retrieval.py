"""
Retrieval over the committed index, shared by server.py and evaluate.py.

Methods:
  - "vector": cosine similarity in ChromaDB (Gemini embeddings).
  - "hybrid": vector + BM25 keyword ranking, fused with reciprocal rank fusion.
    Legal questions often hinge on exact terms ("fianza", "tanteo", "gran tenedor")
    that BM25 catches even when the embedding ranks a neighbouring article higher.

Query vectors are cached in index/query_cache.json, so re-running the evaluation
or asking the same question twice does not spend embedding quota.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import unicodedata
from collections import Counter
from functools import lru_cache

from index import EMBED_DIM, EMBED_MODEL, INDEX_DIR, embed_texts, get_collection

# Chosen by the numbers in eval/retrieval_results.csv (see REPORT.md).
DEFAULT_DESIGN = "structure"
DEFAULT_METHOD = "vector"
DEFAULT_K = 5

QUERY_CACHE = INDEX_DIR / "query_cache.json"
RRF_K = 60

STOPWORDS = set("""a al algo algun alguna algunas alguno algunos ante antes como con contra cual cuales cuando
de del desde donde dos el ella ellas ello ellos en entre era es esa esas ese eso esos esta estas este esto estos
fue ha han hasta hay la las le les lo los mas me mi mis mucho muy no nos o os otra otro para pero por porque que
quien se sea ser si sin sobre su sus tambien te tiene tu tus un una uno unos y ya yo puede puedo cuanto cuanta
cuantos cuantas mismo misma debe deben""".split())


# --------------------------------------------------------------------------- query embeddings

def _load_cache() -> dict:
    if QUERY_CACHE.exists():
        return json.loads(QUERY_CACHE.read_text(encoding="utf-8"))
    return {}


_cache: dict | None = None


def embed_query(query: str) -> list[float]:
    global _cache
    if _cache is None:
        _cache = _load_cache()
    key = hashlib.sha1(f"{EMBED_MODEL}|{EMBED_DIM}|{query.strip()}".encode()).hexdigest()
    if key not in _cache:
        _cache[key] = [round(x, 6) for x in embed_texts([query.strip()], task="RETRIEVAL_QUERY")[0]]
        QUERY_CACHE.write_text(json.dumps(_cache), encoding="utf-8")
    return _cache[key]


# --------------------------------------------------------------------------- BM25

def tokenize(text: str) -> list[str]:
    text = unicodedata.normalize("NFKD", text.lower())
    text = "".join(c for c in text if not unicodedata.combining(c))
    return [t for t in re.findall(r"[a-z0-9]+", text) if t not in STOPWORDS and len(t) > 1]


class BM25:
    def __init__(self, ids: list[str], texts: list[str], k1: float = 1.5, b: float = 0.75):
        self.ids = ids
        self.docs = [Counter(tokenize(t)) for t in texts]
        self.lens = [sum(d.values()) for d in self.docs]
        self.avg = sum(self.lens) / max(len(self.lens), 1)
        df = Counter(t for d in self.docs for t in d)
        n = len(self.docs)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}
        self.k1, self.b = k1, b

    def top(self, query: str, n: int) -> list[str]:
        q = tokenize(query)
        scores = []
        for i, d in enumerate(self.docs):
            s = 0.0
            for t in q:
                if t in d:
                    tf = d[t]
                    s += self.idf[t] * tf * (self.k1 + 1) / (tf + self.k1 * (1 - self.b + self.b * self.lens[i] / self.avg))
            scores.append(s)
        order = sorted(range(len(scores)), key=lambda i: -scores[i])
        return [self.ids[i] for i in order[:n] if scores[i] > 0]


@lru_cache(maxsize=8)
def _bm25(design: str, count: int, base_only: bool) -> BM25:
    col = get_collection(design)
    where = {"origin": "corpus"} if base_only else None
    got = col.get(where=where, include=["documents", "metadatas"])
    texts = [f"{m.get('heading', '')} {d}" for d, m in zip(got["documents"], got["metadatas"])]
    return BM25(got["ids"], texts)


# --------------------------------------------------------------------------- search

def search(query: str, k: int = DEFAULT_K, design: str = DEFAULT_DESIGN, method: str = DEFAULT_METHOD,
           base_only: bool = False) -> list[dict]:
    """Return the top-k chunks: [{"id", "text", "metadata", "score"}]. base_only skips documents added later."""
    col = get_collection(design)
    where = {"origin": "corpus"} if base_only else None
    pool = max(k, 20) if method == "hybrid" else k
    res = col.query(query_embeddings=[embed_query(query)], n_results=pool, where=where,
                    include=["documents", "metadatas", "distances"])
    vec_ids = res["ids"][0]
    by_id = {i: {"id": i, "text": d, "metadata": m, "score": 1 - dist}
             for i, d, m, dist in zip(vec_ids, res["documents"][0], res["metadatas"][0], res["distances"][0])}
    if method == "vector":
        return [by_id[i] for i in vec_ids[:k]]

    kw_ids = _bm25(design, col.count(), base_only).top(query, pool)
    fused: dict[str, float] = {}
    for ranking in (vec_ids, kw_ids):
        for rank, cid in enumerate(ranking):
            fused[cid] = fused.get(cid, 0.0) + 1 / (RRF_K + rank + 1)
    top = sorted(fused, key=lambda c: -fused[c])[:k]
    missing = [c for c in top if c not in by_id]
    if missing:
        got = col.get(ids=missing, include=["documents", "metadatas"])
        for i, d, m in zip(got["ids"], got["documents"], got["metadatas"]):
            by_id[i] = {"id": i, "text": d, "metadata": m, "score": None}
    out = []
    for c in top:
        hit = dict(by_id[c])
        hit["rrf"] = round(fused[c], 5)
        out.append(hit)
    return out


def citation(meta: dict) -> str:
    return f"[{meta['source']}, {meta['location']}]"


def format_hits(hits: list[dict]) -> str:
    if not hits:
        return "No results."
    blocks = []
    for n, h in enumerate(hits, 1):
        m = h["metadata"]
        blocks.append(f"--- Result {n}  cite as {citation(m)}\n"
                      f"Law: {m['title']}\nSection: {m['heading']}"
                      + (f"\nPart: {m['part']}" if m.get("part") else "")
                      + f"\n\n{h['text']}")
    return "\n\n".join(blocks)
