"""
Search over the committed index. Used by server.py and evaluate.py.

Query vectors are cached in index/query_cache.json, so asking the same
question twice (evaluation reruns, the server) costs no embedding quota.
"""

import hashlib
import json
import math
import re
from collections import Counter

import config as C
from index import collection, embed_texts

_cache: dict | None = None


def _load_cache() -> dict:
    global _cache
    if _cache is None:
        _cache = json.loads(C.QUERY_CACHE.read_text()) if C.QUERY_CACHE.exists() else {}
    return _cache


def embed_query(text: str) -> list[float]:
    cache = _load_cache()
    key = hashlib.sha1(f"{C.EMBED_MODEL}|{text.strip()}".encode()).hexdigest()
    if key not in cache:
        cache[key] = [round(x, 6) for x in embed_texts([text.strip()])[0]]
        C.QUERY_CACHE.write_text(json.dumps(cache))
    return cache[key]


TOKEN = re.compile(r"[a-z0-9]+(?:-[a-z0-9]+)*")
STOP = set("a an and are as at be by for from has have how in is it of on or that the this to was what when where which who why with do does can i my".split())


def tokenize(text: str) -> list[str]:
    return [t for t in TOKEN.findall(text.lower()) if t not in STOP]


class BM25:
    def __init__(self, docs: list[str], k1: float = 1.5, b: float = 0.75):
        self.toks = [tokenize(d) for d in docs]
        self.k1, self.b = k1, b
        self.avg = sum(map(len, self.toks)) / max(len(self.toks), 1)
        df = Counter(t for doc in self.toks for t in set(doc))
        n = len(self.toks)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}
        self.tf = [Counter(doc) for doc in self.toks]

    def scores(self, query: str) -> list[float]:
        q = tokenize(query)
        out = []
        for tf, doc in zip(self.tf, self.toks):
            s = 0.0
            for t in q:
                if t in tf:
                    f = tf[t]
                    s += self.idf[t] * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * len(doc) / self.avg))
            out.append(s)
        return out


class Retriever:
    """search(query, k) -> [{"id", "text", "metadata", "score"}]"""

    def __init__(self, chunking: str = C.ACTIVE_CHUNKING, method: str = C.ACTIVE_METHOD):
        self.chunking, self.method = chunking, method
        self.col = collection(chunking)
        self.refresh()

    def refresh(self) -> None:
        """Reload chunk texts for BM25 (call after adding a document)."""
        if self.method == "hybrid":
            got = self.col.get(include=["documents", "metadatas"])
            self.ids, self.docs, self.metas = got["ids"], got["documents"], got["metadatas"]
            self.bm25 = BM25(self.docs)

    def _vector(self, vec, n):
        r = self.col.query(query_embeddings=[vec], n_results=min(n, max(self.col.count(), 1)),
                           include=["documents", "metadatas", "distances"])
        return [{"id": i, "text": d, "metadata": m, "score": 1 - dist}
                for i, d, m, dist in zip(r["ids"][0], r["documents"][0], r["metadatas"][0], r["distances"][0])]

    def search(self, query: str, k: int = C.SEARCH_K) -> list[dict]:
        if self.col.count() == 0:
            return []
        vec = embed_query(query)
        if self.method == "vector":
            return self._vector(vec, k)
        # hybrid: reciprocal-rank fusion of the top 30 from each method
        pool = 30
        vec_hits = self._vector(vec, pool)
        bm = self.bm25.scores(query)
        bm_rank = sorted(range(len(bm)), key=lambda i: -bm[i])[:pool]
        fused, info = {}, {}
        for rank, h in enumerate(vec_hits):
            fused[h["id"]] = fused.get(h["id"], 0) + 1 / (60 + rank)
            info[h["id"]] = h
        for rank, i in enumerate(bm_rank):
            cid = self.ids[i]
            fused[cid] = fused.get(cid, 0) + 1 / (60 + rank)
            info.setdefault(cid, {"id": cid, "text": self.docs[i], "metadata": self.metas[i]})
        top = sorted(fused, key=lambda c: -fused[c])[:k]
        return [{**info[c], "score": fused[c]} for c in top]


def citation(meta: dict) -> str:
    return f"[{meta['doc_id']} p.{meta['page']}]"


def format_results(hits: list[dict]) -> str:
    """What the search tool returns to the model."""
    if not hits:
        return "No passages found. The corpus may not cover this question."
    blocks = []
    for h in hits:
        m = h["metadata"]
        pages = m["pages"].replace(",", ", ")
        blocks.append(f"{citation(m)}  {m['title']} | section: {m['section']} | pages: {pages}\n{h['text']}")
    return "\n\n---\n\n".join(blocks)
