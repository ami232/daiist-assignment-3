"""
Shared retrieval code: Gemini embeddings, the Chroma index in index/, BM25,
hybrid search and citation formatting. index.py, server.py and evaluate.py
all import from here, so the three always search the same way.

Nothing here prints to stdout (server.py speaks MCP over stdout); logs go to stderr.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
INDEX_DIR = ROOT / "index"
CHROMA_DIR = INDEX_DIR / "chroma"
DOCS_REGISTRY = INDEX_DIR / "documents.json"
QUERY_CACHE = INDEX_DIR / "query_cache.json"

EMBED_MODEL = os.environ.get("EMBED_MODEL", "gemini-embedding-2")
EMBED_DIM = 768            # Matryoshka truncation: 4x smaller index than 3072, same ranking quality for our size
EMBED_BATCH = 20           # texts per request; every text counts against the ~1,000/day free quota

# The two chunking designs we compare (each one is a separate Chroma collection).
DESIGNS = ("fixed", "section")

# The design search uses. evaluate.py picks it by the numbers (best hit@5, then hit@1, then fewest
# words in the prompt) and saves it in index/production.json; this is the default until then.
PRODUCTION_FILE = INDEX_DIR / "production.json"
PRODUCTION = {"design": "section", "hybrid": True, "k": 5}
if PRODUCTION_FILE.is_file():
    PRODUCTION = {**PRODUCTION, **json.loads(PRODUCTION_FILE.read_text(encoding="utf-8"))}


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


# --------------------------------------------------------------------------- Gemini client

_client = None


def client():
    """One google-genai client per process, keyed from .env / GEMINI_API_KEY."""
    global _client
    if _client is None:
        from google import genai

        from api_key import load_api_key

        _client = genai.Client(api_key=load_api_key())
    return _client


def _normalise(vec) -> list[float]:
    v = np.asarray(vec, dtype=np.float32)
    n = float(np.linalg.norm(v))
    return (v / n).tolist() if n else v.tolist()


def doc_prompt(title: str, text: str) -> str:
    # gemini-embedding-2 has no task_type: the task goes into the text itself.
    return f"title: {title} | text: {text}"


def query_prompt(query: str) -> str:
    return f"task: search result | query: {query}"


def _retry_delay(error: Exception) -> float | None:
    """Seconds to wait for a 429, or None if it is the daily quota (waiting won't help)."""
    msg = str(error)
    if "PerDay" in msg or "per day" in msg.lower():
        return None
    m = re.search(r"retry in ([\d.]+)s", msg) or re.search(r"'retryDelay': '(\d+)s'", msg)
    return float(m.group(1)) + 1 if m else 30.0


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed already-prefixed texts in one request. One Content per text so each gets its own vector
    (several parts inside ONE Content would be merged into a single vector by gemini-embedding-2)."""
    from google.genai import types

    contents = [types.Content(parts=[types.Part(text=t)]) for t in texts]
    for attempt in range(6):
        try:
            result = client().models.embed_content(
                model=EMBED_MODEL,
                contents=contents,
                config=types.EmbedContentConfig(output_dimensionality=EMBED_DIM),
            )
            vectors = [e.values for e in result.embeddings]
            if len(vectors) != len(texts):
                raise RuntimeError(f"asked for {len(texts)} embeddings, got {len(vectors)}")
            return [_normalise(v) for v in vectors]
        except Exception as error:  # noqa: BLE001
            if "429" not in str(error) and "RESOURCE_EXHAUSTED" not in str(error):
                raise
            delay = _retry_delay(error)
            if delay is None:
                raise RuntimeError(
                    "Daily embedding quota used up. Everything embedded so far is saved in index/; "
                    "run the same command again after the quota resets (09:00 in Spain)."
                ) from error
            log(f"  rate limited, waiting {delay:.0f}s (attempt {attempt + 1}/6)")
            time.sleep(delay)
    raise RuntimeError("Embedding kept failing with 429; try again later.")


def _load_query_cache() -> dict:
    if QUERY_CACHE.is_file():
        try:
            return json.loads(QUERY_CACHE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def embed_query(query: str) -> list[float]:
    """Embed a question, caching it on disk so repeated evaluations don't spend quota."""
    key = hashlib.sha1(f"{EMBED_MODEL}|{EMBED_DIM}|{query}".encode()).hexdigest()
    cache = _load_query_cache()
    if key in cache:
        return cache[key]
    vec = embed_texts([query_prompt(query)])[0]
    cache = _load_query_cache()  # re-read: another process may have written meanwhile
    cache[key] = vec
    QUERY_CACHE.parent.mkdir(exist_ok=True)
    tmp = QUERY_CACHE.with_suffix(".tmp")
    tmp.write_text(json.dumps(cache), encoding="utf-8")
    tmp.replace(QUERY_CACHE)
    return vec


# --------------------------------------------------------------------------- Chroma

_chroma = None


def chroma():
    global _chroma
    if _chroma is None:
        import chromadb
        from chromadb.config import Settings

        CHROMA_DIR.mkdir(parents=True, exist_ok=True)
        _chroma = chromadb.PersistentClient(path=str(CHROMA_DIR), settings=Settings(anonymized_telemetry=False))
    return _chroma


def collection(design: str):
    """The Chroma collection of one chunking design. Vectors are unit-length, so inner product = cosine."""
    return chroma().get_or_create_collection(
        name=f"padel_{design}",
        embedding_function=None,
        metadata={"hnsw:space": "ip", "design": design, "embed_model": EMBED_MODEL, "dim": EMBED_DIM},
    )


def load_registry() -> dict:
    if DOCS_REGISTRY.is_file():
        return json.loads(DOCS_REGISTRY.read_text(encoding="utf-8"))
    return {}


def save_registry(registry: dict) -> None:
    DOCS_REGISTRY.parent.mkdir(exist_ok=True)
    DOCS_REGISTRY.write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")


# --------------------------------------------------------------------------- BM25 (for hybrid search)

_TOKEN = re.compile(r"[a-z0-9]+(?:\.[0-9]+)?")
_STOP = set(
    "a an and are as at be by for from has have in is it its of on or that the this to was were with what which "
    "how does do did can could should would who whom why when where than then there these those their them they "
    "i my me you your we our".split()
)


def tokenize(text: str) -> list[str]:
    return [t for t in _TOKEN.findall(text.lower()) if t not in _STOP]


class BM25:
    def __init__(self, ids: list[str], texts: list[str], k1: float = 1.5, b: float = 0.75):
        self.ids = ids
        self.docs = [Counter(tokenize(t)) for t in texts]
        self.lens = [sum(d.values()) for d in self.docs]
        self.avg = (sum(self.lens) / len(self.lens)) if self.lens else 1.0
        df = Counter(term for d in self.docs for term in d)
        n = len(self.docs)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}
        self.k1, self.b = k1, b

    def scores(self, query: str) -> np.ndarray:
        q = tokenize(query)
        out = np.zeros(len(self.docs))
        for i, (d, length) in enumerate(zip(self.docs, self.lens)):
            s = 0.0
            for t in q:
                f = d.get(t)
                if f:
                    s += self.idf[t] * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * length / self.avg))
            out[i] = s
        return out


# --------------------------------------------------------------------------- search

class Searcher:
    """Loads one design's chunks once (texts + metadata, for BM25) and answers queries.

    corpus_only=True restricts results to the original corpus (origin == "corpus"), which
    evaluate.py uses so that documents added later through add_document don't change the
    results of a test set written before them.
    """

    def __init__(self, design: str, corpus_only: bool = False):
        self.design = design
        self.corpus_only = corpus_only
        self.reload()

    def reload(self) -> None:
        col = collection(self.design)
        got = col.get(include=["documents", "metadatas"])
        keep = [
            i for i, m in enumerate(got["metadatas"])
            if not self.corpus_only or m.get("origin", "corpus") == "corpus"
        ]
        self.ids = [got["ids"][i] for i in keep]
        self.texts = [got["documents"][i] for i in keep]
        self.metas = [got["metadatas"][i] for i in keep]
        self.pos = {cid: i for i, cid in enumerate(self.ids)}
        self.bm25 = BM25(self.ids, self.texts)
        self.col = col

    def dense(self, qvec: list[float], n: int) -> list[str]:
        if not self.ids:
            return []
        where = {"origin": "corpus"} if self.corpus_only else None
        res = self.col.query(query_embeddings=[qvec], n_results=min(n, len(self.ids)), where=where, include=[])
        return res["ids"][0]

    def search(self, query: str, k: int = 5, hybrid: bool = False, qvec: list[float] | None = None) -> list[dict]:
        if not self.ids:
            return []
        qvec = qvec if qvec is not None else embed_query(query)
        if not hybrid:
            ranked = self.dense(qvec, k)
        else:
            # Reciprocal rank fusion of dense and BM25 rankings (k=60, the usual constant).
            dense_ids = self.dense(qvec, 30)
            bm = self.bm25.scores(query)
            bm_ids = [self.ids[i] for i in np.argsort(-bm)[:30] if bm[i] > 0]
            fused: dict[str, float] = {}
            for ranking in (dense_ids, bm_ids):
                for r, cid in enumerate(ranking):
                    fused[cid] = fused.get(cid, 0.0) + 1.0 / (60 + r + 1)
            ranked = sorted(fused, key=fused.get, reverse=True)[:k]
        return [{"id": cid, "text": self.texts[self.pos[cid]], **self.metas[self.pos[cid]]} for cid in ranked]


def citation(meta: dict) -> str:
    """The exact tag the agent must copy into its answer, e.g. [munoz2022 p.4]."""
    if meta["page_start"] == meta["page_end"]:
        return f"[{meta['doc_id']} p.{meta['page_start']}]"
    return f"[{meta['doc_id']} p.{meta['page_start']}-{meta['page_end']}]"


def year_of(meta: dict) -> str:
    return f" ({meta['year']})" if meta.get("year") else ""


def format_results(results: list[dict]) -> str:
    if not results:
        return "No passages found in the corpus."
    blocks = []
    for i, r in enumerate(results, 1):
        blocks.append(
            f"--- Result {i} | cite as {citation(r)} | {r['title']}{year_of(r)} | section: {r['section']}\n"
            f"{r['text']}"
        )
    return "\n\n".join(blocks)
