"""
Search over the saved index. Used by server.py (the search tool) and evaluate.py (hit rates).

Three retrieval designs share the same saved vectors:
    structure   one chunk per legal unit (article paragraph / notice paragraph), dense search
    fixed       200-word windows that ignore the structure, dense search
    hybrid      the structure chunks, dense search fused with BM25 keyword search (RRF)
"""

from __future__ import annotations

import json
import math
import re
from collections import Counter
from pathlib import Path

import numpy as np

import index as pipeline

CONFIG = pipeline.INDEX / "config.json"
BASE_ONLY = pipeline.INDEX / ".base_only"   # while it exists, search ignores documents added later
QUERY_CACHE = pipeline.INDEX / "query_vectors.jsonl"
TOKEN = re.compile(r"[a-z0-9]+")


def chosen_design() -> str:
    """The design picked in evaluate.py (written to index/config.json); structure by default."""
    if CONFIG.exists():
        return json.loads(CONFIG.read_text()).get("design", "structure")
    return "structure"


class QueryEmbedder:
    """Embeds queries once and remembers them, so re-running an evaluation costs no quota."""

    def __init__(self):
        self.cache: dict[str, list[float]] = {}
        if QUERY_CACHE.exists():
            for line in QUERY_CACHE.read_text().splitlines():
                if line.strip():
                    rec = json.loads(line)
                    self.cache[rec["q"]] = rec["v"]

    def __call__(self, query: str) -> np.ndarray:
        if query not in self.cache:
            vector = pipeline.embed_query(query)
            self.cache[query] = vector
            with QUERY_CACHE.open("a") as f:
                f.write(json.dumps({"q": query, "v": [round(x, 6) for x in vector]}) + "\n")
        return np.asarray(self.cache[query], dtype=np.float32)


class BM25:
    def __init__(self, texts: list[str], k1: float = 1.5, b: float = 0.75):
        self.docs = [Counter(TOKEN.findall(t.lower())) for t in texts]
        self.lens = np.array([sum(d.values()) for d in self.docs], dtype=np.float32)
        self.avg = float(self.lens.mean()) if len(self.lens) else 0.0
        df = Counter(term for d in self.docs for term in d)
        n = len(self.docs)
        self.idf = {t: math.log(1 + (n - c + 0.5) / (c + 0.5)) for t, c in df.items()}
        self.k1, self.b = k1, b

    def scores(self, query: str) -> np.ndarray:
        terms = TOKEN.findall(query.lower())
        out = np.zeros(len(self.docs), dtype=np.float32)
        for i, d in enumerate(self.docs):
            s = 0.0
            for t in terms:
                if t in d:
                    tf = d[t]
                    s += self.idf[t] * tf * (self.k1 + 1) / (tf + self.k1 * (1 - self.b + self.b * self.lens[i] / self.avg))
            out[i] = s
        return out


class Searcher:
    def __init__(self, design: str | None = None, embedder: QueryEmbedder | None = None):
        self.design = design or chosen_design()
        base = "structure" if self.design == "hybrid" else self.design
        self.embed = embedder or QueryEmbedder()
        self.load(base)

    def load(self, base: str) -> None:
        vectors = pipeline.load_vectors()
        chunks = [c for c in pipeline.load_chunks(base) if c["sha"] in vectors]
        missing = len(pipeline.load_chunks(base)) - len(chunks)
        if missing:
            pipeline.log(f"warning: {missing} {base} chunks have no saved vector yet and are not searchable")
        self.chunks = chunks
        matrix = np.asarray([vectors[c["sha"]] for c in chunks], dtype=np.float32)
        self.matrix = matrix / np.linalg.norm(matrix, axis=1, keepdims=True)
        self.bm25 = BM25([c["embed_text"] for c in chunks]) if self.design == "hybrid" else None

    def reload(self) -> None:
        self.load("structure" if self.design == "hybrid" else self.design)

    def search(self, query: str, k: int = 5) -> list[dict]:
        q = self.embed(query)
        dense = self.matrix @ (q / np.linalg.norm(q))
        if BASE_ONLY.exists():  # evaluation of the original corpus, before any add_document
            added = np.array([c["source"] not in pipeline.DOCUMENTS for c in self.chunks])
            dense = np.where(added, -1.0, dense)
        if self.bm25 is None:
            order = np.argsort(-dense)[:k]
            return [{**self.chunks[i], "score": float(dense[i])} for i in order]
        # reciprocal rank fusion of the dense and the keyword ranking
        rank_dense = np.argsort(np.argsort(-dense))
        rank_bm25 = np.argsort(np.argsort(-self.bm25.scores(query)))
        fused = 1 / (60 + rank_dense) + 1 / (60 + rank_bm25)
        if BASE_ONLY.exists():
            fused = np.where(added, -1.0, fused)
        order = np.argsort(-fused)[:k]
        return [{**self.chunks[i], "score": float(fused[i])} for i in order]


def cite(chunk: dict) -> str:
    """The citation label the assistant must use, e.g. [EUMR Art. 1(2)]."""
    return f"[{chunk['source']} {chunk['location']}]"


def format_results(results: list[dict]) -> str:
    blocks = []
    for r in results:
        title = pipeline.DOCUMENTS.get(r["source"], {}).get("title", r["source"])
        heading = f" ({r['heading']})" if r.get("heading") else ""
        blocks.append(f"{cite(r)}{heading}\nDocument: {title}\nCovers: {', '.join(r['units'])}\n{r['text']}")
    return "\n\n---\n\n".join(blocks) if blocks else "No results."
