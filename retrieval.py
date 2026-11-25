"""
Retrieval over the committed index: dense (Gemini vectors in ChromaDB),
BM25 (keyword, over index/chunks.jsonl) and hybrid (reciprocal rank fusion of
the two). Shared by server.py and evaluate.py.

Query vectors are cached in index/query_cache.json, so asking the same query
twice never spends embedding quota twice.
"""

from __future__ import annotations

import json
import math
import re
import threading
import unicodedata
from collections import Counter
from pathlib import Path

import index as idx

QUERY_CACHE = idx.INDEX_DIR / "query_cache.json"
RRF_K = 60
_lock = threading.Lock()

# Spanish function words that carry no meaning for BM25
STOP = set("""a al algo algunas algunos ante antes como con contra cual cuando de del desde donde dos
el ella ellas ellos en entre era es esa esas ese eso esos esta estas este esto estos fue ha han hasta
hay la las le les lo los mas me mi mientras muy nada ni no nos o otra otras otro otros para pero
poco por porque que quien se sea segun ser si sin sobre su sus tambien tanto te tiene todo todos
tras tu un una uno unos y ya articulo apartado presente dicho dicha siguientes siguiente cada podra
podran debera deberan sera seran caso casos forma""".split())


def fold(text: str) -> str:
    text = unicodedata.normalize("NFKD", text.lower())
    return "".join(c for c in text if not unicodedata.combining(c))


def tokenize(text: str) -> list[str]:
    """Lowercase, strip accents, drop stopwords, crude stemming (first 6
    letters), so 'conductores'/'conductor' and 'velocidades'/'velocidad' meet."""
    toks = re.findall(r"[a-z0-9]+(?:[.,][0-9]+)?", fold(text))
    return [t[:6] if not t[0].isdigit() else t for t in toks if t not in STOP and len(t) > 1]


class Index:
    """Everything search needs, loaded once from index/."""

    def __init__(self, model: str | None = None) -> None:
        self.model = model or idx.EMBED_MODEL
        self.col = idx.load_collection(self.model)
        self.reload()
        self._cache = json.loads(QUERY_CACHE.read_text()) if QUERY_CACHE.exists() else {}

    def reload(self) -> None:
        """(Re)read chunks.jsonl and rebuild BM25 statistics."""
        self.chunks = [json.loads(l) for l in idx.chunks_file(self.col).read_text(encoding="utf-8").splitlines() if l]
        self.by_id = {c["id"]: c for c in self.chunks}
        self.toks = [tokenize(c["text"]) for c in self.chunks]
        self.tf = [Counter(t) for t in self.toks]
        self.avgdl = sum(map(len, self.toks)) / max(len(self.toks), 1)
        df = Counter(w for t in self.toks for w in set(t))
        n = len(self.toks)
        self.idf = {w: math.log(1 + (n - d + 0.5) / (d + 0.5)) for w, d in df.items()}

    # ------------------------------------------------------------ dense
    def query_vector(self, query: str) -> list[float]:
        # cache keys: "q|..." for gemini-embedding-2 (the original), "<model>|q|..." otherwise
        key = f"q|{query}" if self.model == "gemini-embedding-2" else f"{self.model}|q|{query}"
        with _lock:
            if key in self._cache:
                return self._cache[key]
        vec = idx.embed([query], task="RETRIEVAL_QUERY", model=self.model)[0]
        with _lock:
            self._cache[key] = vec
            tmp = QUERY_CACHE.with_suffix(".tmp")
            tmp.write_text(json.dumps(self._cache))
            tmp.replace(QUERY_CACHE)
        return vec

    def dense(self, query: str, k: int = 10, where: dict | None = None) -> list[tuple[str, float]]:
        res = self.col.query(query_embeddings=[self.query_vector(query)], n_results=k,
                             where=where, include=["distances"])
        return [(i, 1 - d) for i, d in zip(res["ids"][0], res["distances"][0])]

    # ------------------------------------------------------------ bm25
    def bm25(self, query: str, k: int = 10, k1: float = 1.5, b: float = 0.75,
             source: str | None = None) -> list[tuple[str, float]]:
        q = tokenize(query)
        scores = []
        for i, tf in enumerate(self.tf):
            if source and self.chunks[i]["metadata"]["source"] != source:
                continue
            dl = len(self.toks[i])
            s = sum(self.idf.get(w, 0) * tf[w] * (k1 + 1) / (tf[w] + k1 * (1 - b + b * dl / self.avgdl))
                    for w in q if w in tf)
            if s > 0:
                scores.append((self.chunks[i]["id"], s))
        return sorted(scores, key=lambda x: -x[1])[:k]

    # ------------------------------------------------------------ hybrid
    def hybrid(self, query: str, k: int = 10, pool: int = 20, source: str | None = None) -> list[tuple[str, float]]:
        where = {"source": source} if source else None
        fused: Counter = Counter()
        for ranking in (self.dense(query, pool, where), self.bm25(query, pool, source=source)):
            for rank, (cid, _) in enumerate(ranking):
                fused[cid] += 1 / (RRF_K + rank + 1)
        return fused.most_common(k)

    def search(self, query: str, k: int = 5, method: str = "hybrid", source: str | None = None) -> list[dict]:
        if method == "dense":
            hits = self.dense(query, k, {"source": source} if source else None)
        elif method == "bm25":
            hits = self.bm25(query, k, source=source)
        else:
            hits = self.hybrid(query, k, source=source)
        out = []
        for cid, score in hits:
            c = self.by_id.get(cid)
            if c is None:  # added after chunks were loaded
                self.reload()
                c = self.by_id[cid]
            out.append({**c, "score": round(score, 4)})
        return out


def cite(meta: dict) -> str:
    """The citation string the agent must reuse: [SOURCE, location]."""
    return f"[{meta['source']}, {meta['location']}]"


def _date(d: str) -> str:
    return f"{d[:4]}-{d[4:6]}-{d[6:]}" if len(d) == 8 else d


def format_results(hits: list[dict]) -> str:
    """Render hits for the model: citation, heading, URL, then the text."""
    if not hits:
        return "No passages found."
    blocks = []
    for h in hits:
        m = h["metadata"]
        body = h["text"].split("\n", 2)[-1]  # drop the "[SOURCE · title]" + heading lines
        part = f" (part {m['part']}/{m['parts']})" if m["parts"] > 1 else ""
        blocks.append(
            f"{cite(m)}{part} {m['heading']}\n"
            f"Document: {m['doc_title']} | version in force from {_date(m['version_date'])} | {m['url']}\n"
            f"{body}"
        )
    return "\n\n---\n\n".join(blocks)
