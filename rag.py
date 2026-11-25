"""
Shared retrieval code: the Gemini embedding client, the ChromaDB store in
index/, and search (dense, keyword BM25, or hybrid). index.py, server.py and
evaluate.py all import from here, so there is exactly one way to embed and
one way to search.

Nothing here prints to stdout (server.py speaks MCP over stdout); logs go to
stderr.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INDEX_DIR = ROOT / "index"
CHROMA_DIR = INDEX_DIR / "chroma"
QUERY_CACHE = INDEX_DIR / "query_cache.json"
CONFIG_FILE = INDEX_DIR / "config.json"

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768          # smaller vectors keep index/ small; retrieval quality barely moves
EMBED_BATCH = 50         # texts per request

DESIGNS = ("structured", "fixed")


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


# ---------------------------------------------------------------- config

def chosen_config() -> dict:
    """The design and search mode evaluate.py chose by the numbers (index/config.json)."""
    if CONFIG_FILE.is_file():
        return json.loads(CONFIG_FILE.read_text())
    return {"design": "structured", "mode": "hybrid", "k": 5}


# ---------------------------------------------------------------- embeddings

_client = None


def client():
    global _client
    if _client is None:
        from google import genai
        from api_key import load_api_key
        _client = genai.Client(api_key=load_api_key())
    return _client


class QuotaExhausted(RuntimeError):
    """The free tier's daily embedding quota is used up. Saved vectors are kept."""


def embed(texts: list[str], task_type: str) -> list[list[float]]:
    """Embed a batch with Gemini, retrying per-minute rate limits.

    Raises QuotaExhausted when the daily quota is gone, so the caller can stop
    cleanly with everything already saved.
    """
    from google.genai import types

    config = types.EmbedContentConfig(task_type=task_type, output_dimensionality=EMBED_DIM)
    for attempt in range(8):
        try:
            # one Content per text: gemini-embedding-2 would merge a plain list of strings into one vector
            contents = [types.Content(parts=[types.Part(text=t)]) for t in texts]
            result = client().models.embed_content(model=EMBED_MODEL, contents=contents, config=config)
            if len(result.embeddings) != len(texts):
                raise RuntimeError(f"asked for {len(texts)} embeddings, got {len(result.embeddings)}")
            return [normalise(e.values) for e in result.embeddings]
        except Exception as error:  # noqa: BLE001 - classify API errors by message
            message = str(error)
            if "429" in message or "RESOURCE_EXHAUSTED" in message:
                if "PerDay" in message or "per day" in message.lower():
                    raise QuotaExhausted(message[:300]) from error
                wait = min(60, 10 * (attempt + 1))
                log(f"  rate limited, waiting {wait}s ...")
                time.sleep(wait)
                continue
            if attempt < 3 and ("500" in message or "503" in message or "timed out" in message.lower()):
                time.sleep(5)
                continue
            raise
    raise QuotaExhausted("still rate limited after several retries")


def normalise(vector) -> list[float]:
    norm = math.sqrt(sum(v * v for v in vector)) or 1.0
    return [v / norm for v in vector]


def _query_cache() -> dict:
    if QUERY_CACHE.is_file():
        return json.loads(QUERY_CACHE.read_text())
    return {}


def embed_query(query: str) -> list[float]:
    """Embed a question, re-using the saved vector if this exact question was seen before.

    Questions count against the same daily quota as chunks, so evaluation
    re-runs and repeated searches cost nothing.
    """
    key = hashlib.sha1(f"{EMBED_MODEL}|{EMBED_DIM}|{query.strip()}".encode()).hexdigest()
    cache = _query_cache()
    if key in cache:
        return cache[key]
    vector = embed([query.strip()], "RETRIEVAL_QUERY")[0]
    cache = _query_cache()  # re-read: another process may have written meanwhile
    cache[key] = [round(v, 6) for v in vector]
    QUERY_CACHE.write_text(json.dumps(cache))
    return vector


# ---------------------------------------------------------------- store

_chroma = None


def store():
    global _chroma
    if _chroma is None:
        import chromadb
        from chromadb.config import Settings
        _chroma = chromadb.PersistentClient(path=str(CHROMA_DIR), settings=Settings(anonymized_telemetry=False))
    return _chroma


def collection(design: str):
    return store().get_or_create_collection(name=design, metadata={"hnsw:space": "cosine"})


# ---------------------------------------------------------------- search

TOKEN = re.compile(r"[a-z0-9]+(?:\(\d+\))?")
STOP = set("""a an and are as at be by for from has have if in is it its of on or that the this to
was were which with what who when where how does do can under any not shall should may must""".split())


def tokens(text: str) -> list[str]:
    return [t for t in TOKEN.findall(text.lower()) if t not in STOP]


class BM25:
    """Plain BM25 keyword scoring over one collection's chunk texts."""

    def __init__(self, ids: list[str], texts: list[str], k1: float = 1.5, b: float = 0.75):
        self.ids, self.k1, self.b = ids, k1, b
        self.docs = [Counter(tokens(t)) for t in texts]
        self.lengths = [sum(d.values()) for d in self.docs]
        self.avg = sum(self.lengths) / max(len(self.lengths), 1)
        df = Counter(term for d in self.docs for term in d)
        n = len(self.docs)
        self.idf = {t: math.log(1 + (n - c + 0.5) / (c + 0.5)) for t, c in df.items()}

    def scores(self, query: str) -> list[float]:
        q = tokens(query)
        out = []
        for doc, length in zip(self.docs, self.lengths):
            s = 0.0
            for term in q:
                f = doc.get(term, 0)
                if f:
                    s += self.idf[term] * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * length / self.avg))
            out.append(s)
        return out


class Searcher:
    """Loads one collection once (vectors, texts, metadata) and searches it in memory."""

    def __init__(self, design: str):
        self.design = design
        self.reload()

    def reload(self) -> None:
        import numpy as np
        import os
        data = collection(self.design).get(include=["embeddings", "documents", "metadatas"])
        # CORPUS_EXCLUDE="SCC 2021/915" hides added documents, so evaluate.py can measure the base corpus
        excluded = {d.strip() for d in os.environ.get("CORPUS_EXCLUDE", "").split(",") if d.strip()}
        keep = [i for i, m in enumerate(data["metadatas"]) if m["doc_id"] not in excluded]
        self.ids = [data["ids"][i] for i in keep]
        self.texts = [data["documents"][i] for i in keep]
        self.metas = [data["metadatas"][i] for i in keep]
        self.vectors = (np.array([data["embeddings"][i] for i in keep], dtype="float32")
                        if keep else np.zeros((0, EMBED_DIM)))
        self.bm25 = BM25(self.ids, [m.get("header", "") + "\n" + t for m, t in zip(self.metas, self.texts)])

    def search(self, query: str, k: int = 5, mode: str = "dense", doc_filter: str | None = None) -> list[dict]:
        import numpy as np
        n = len(self.ids)
        if n == 0:
            return []
        allowed = np.ones(n, dtype=bool)
        if doc_filter:
            allowed = np.array([m["doc_id"] == doc_filter for m in self.metas])

        def ranks(scores):
            order = [i for i in np.argsort(-np.asarray(scores)) if allowed[i]]
            return {i: r for r, i in enumerate(order)}

        if mode in ("dense", "hybrid"):
            q = np.array(embed_query(query), dtype="float32")
            dense = self.vectors @ q
        if mode in ("bm25", "hybrid"):
            keyword = self.bm25.scores(query)
        if mode == "dense":
            final = {i: 1 / (60 + r) for i, r in ranks(dense).items()}
        elif mode == "bm25":
            final = {i: 1 / (60 + r) for i, r in ranks(keyword).items()}
        else:  # reciprocal rank fusion of the two rankings
            rd, rk = ranks(dense), ranks(keyword)
            final = {i: 1 / (60 + rd[i]) + 1 / (60 + rk[i]) for i in rd}
        top = sorted(final, key=final.get, reverse=True)[:k]
        return [
            {"id": self.ids[i], "score": round(float(final[i]), 5), "text": self.texts[i], **self.metas[i]}
            for i in top
        ]


def format_results(results: list[dict]) -> str:
    """What the search tool returns: each chunk with the exact citation to use."""
    if not results:
        return "No passages found. The corpus is empty or nothing matched."
    blocks = []
    for n, r in enumerate(results, 1):
        page = f", page {r['page']}" if r.get("page") else ""
        blocks.append(
            f"[{n}] CITE AS: [{r['cite']}]\n"
            f"    source: {r['doc_title']}{page}\n"
            f"    location: {r['header']}\n"
            f"    document: {r['doc_id']} | covers: {r.get('locations', r['location']).replace('|', '; ')}\n"
            f"{r['text']}"
        )
    return "\n\n".join(blocks)
