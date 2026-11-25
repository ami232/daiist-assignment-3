"""
Shared RAG pieces: configuration, the Gemini embedder, the Chroma store and search.

index.py (build), server.py (MCP tools) and evaluate.py all import from here, so
there is exactly one way to embed, store and search.

Offline testing: RAG_FAKE_EMBED=1 swaps Gemini for a deterministic hashing
embedder and RAG_INDEX_DIR points the store somewhere else. Never commit an
index built that way.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
import sys
import time
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INDEX_DIR = Path(os.environ.get("RAG_INDEX_DIR", ROOT / "index"))
CHROMA_DIR = INDEX_DIR / "chroma"
REGISTRY_PATH = INDEX_DIR / "documents.json"
QUERY_CACHE_PATH = INDEX_DIR / "query_cache.json"

# ---------------------------------------------------------------- configuration

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768             # smaller than the 3072 default: index stays small, quality barely moves
EMBED_BATCH = 50            # texts per API call; every text counts against the ~1,000/day quota

# The two chunking designs compared in evaluate.py. Each lives in its own Chroma
# collection, so comparing them costs one full embedding pass per design.
DESIGNS = {
    "fixed": {"words": 200, "overlap": 40},          # fixed word windows, blind to structure
    "struct": {"max_words": 350, "min_words": 3},    # one chunk per article / question
}

# DECISION (Jesús): set these from the retrieval numbers in eval/retrieval.csv.
ACTIVE_DESIGN = os.environ.get("RAG_DESIGN", "struct")
SEARCH_MODE = os.environ.get("RAG_SEARCH_MODE", "dense")   # "dense" or "hybrid" (dense + BM25)
TOP_K = 5


def log(*args) -> None:
    """stdout carries the MCP protocol in server.py, so everything logs to stderr."""
    print(*args, file=sys.stderr, flush=True)


# ---------------------------------------------------------------- text helpers

def sha(text: str, n: int = 16) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:n]


def strip_accents(text: str) -> str:
    return "".join(c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn")


SPANISH_STOPWORDS = set(
    """a al algo algunas algunos ante antes como con contra cual cuales cuando de del desde donde dos el
    ella ellas ellos en entre era es esa esas ese eso esos esta estas este esto estos fue ha han hasta la
    las le les lo los mas me mi muy no nos o otra otras otro otros para pero por que quien se sea sean ser
    si sin sobre su sus tambien tiene tienen todo todos tras un una uno unos y ya cuanto cuantos cuanta
    cuantas puede pueden debe deben hay qué cómo cuál""".split()
)


def tokenize(text: str) -> list[str]:
    """Lowercase, accent-free word tokens without Spanish stopwords (for BM25)."""
    words = re.findall(r"[a-z0-9]+", strip_accents(text.lower()))
    return [w for w in words if w not in SPANISH_STOPWORDS and (len(w) > 1 or w.isdigit())]


# ---------------------------------------------------------------- embedder

class QuotaExhausted(RuntimeError):
    """The daily embedding quota is used up. Everything embedded so far is saved."""


def _retry_delay(error: Exception) -> float | None:
    match = re.search(r"retry(?:Delay)?['\"]?\s*[:=]\s*['\"]?(\d+(?:\.\d+)?)s", str(error))
    return float(match.group(1)) if match else None


class Embedder:
    """Gemini embeddings, one vector per text, L2-normalised.

    Gotcha: with gemini-embedding-2 the SDK turns a list of strings into ONE
    Content with several parts, which returns ONE embedding for all of them.
    So every text goes in its own Content.
    """

    def __init__(self) -> None:
        self.fake = bool(os.environ.get("RAG_FAKE_EMBED"))
        self.calls = 0
        self.texts = 0
        if not self.fake:
            from google import genai

            from api_key import load_api_key

            self.client = genai.Client(api_key=load_api_key())

    def embed(self, texts: list[str], task: str) -> list[list[float]]:
        if not texts:
            return []
        if self.fake:
            return [_fake_vector(t) for t in texts]
        from google.genai import types

        contents = [types.Content(parts=[types.Part(text=t)]) for t in texts]
        config = types.EmbedContentConfig(task_type=task, output_dimensionality=EMBED_DIM)
        for attempt in range(6):
            try:
                response = self.client.models.embed_content(model=EMBED_MODEL, contents=contents, config=config)
                break
            except Exception as error:  # noqa: BLE001 - classify and retry API errors
                message = str(error)
                if "429" not in message and "RESOURCE_EXHAUSTED" not in message:
                    if attempt < 2 and any(code in message for code in ("500", "503", "504")):
                        time.sleep(5 * (attempt + 1))
                        continue
                    raise
                if "PerDay" in message or "per day" in message.lower():
                    raise QuotaExhausted(
                        "Daily embedding quota used up. Vectors so far are saved; run again after "
                        "the reset (09:00 Spain time)."
                    ) from error
                wait = _retry_delay(error) or 20 * (attempt + 1)
                log(f"  rate limited, waiting {wait:.0f}s ...")
                time.sleep(wait)
        else:
            raise RuntimeError("Embedding kept failing after retries.")
        self.calls += 1
        self.texts += len(texts)
        vectors = [_normalise(e.values) for e in response.embeddings]
        if len(vectors) != len(texts):
            raise RuntimeError(f"Asked for {len(texts)} embeddings, got {len(vectors)}.")
        return vectors


def _normalise(values) -> list[float]:
    norm = math.sqrt(sum(v * v for v in values)) or 1.0
    return [float(v) / norm for v in values]


def _fake_vector(text: str, dim: int = 256) -> list[float]:
    """Deterministic bag-of-words hashing vector, for offline tests only."""
    vector = [0.0] * dim
    for token in tokenize(text):
        vector[int(hashlib.md5(token.encode()).hexdigest(), 16) % dim] += 1.0
    return _normalise(vector)


_EMBEDDER: Embedder | None = None


def embedder() -> Embedder:
    global _EMBEDDER
    if _EMBEDDER is None:
        _EMBEDDER = Embedder()
    return _EMBEDDER


# Query vectors are cached in index/ so re-running the evaluation (or the
# grader running check.py) does not spend the embedding quota again.
_QUERY_CACHE: dict[str, list[float]] | None = None


def embed_query(query: str) -> list[float]:
    global _QUERY_CACHE
    if _QUERY_CACHE is None:
        _QUERY_CACHE = json.loads(QUERY_CACHE_PATH.read_text()) if QUERY_CACHE_PATH.exists() else {}
    key = sha(f"{EMBED_MODEL}|{EMBED_DIM}|{'fake' if embedder().fake else 'real'}|{query.strip()}")
    if key not in _QUERY_CACHE:
        _QUERY_CACHE[key] = [round(v, 6) for v in embedder().embed([query.strip()], "RETRIEVAL_QUERY")[0]]
        QUERY_CACHE_PATH.parent.mkdir(parents=True, exist_ok=True)
        QUERY_CACHE_PATH.write_text(json.dumps(_QUERY_CACHE))
    return _QUERY_CACHE[key]


# ---------------------------------------------------------------- store

_CLIENT = None


def collection(design: str = ACTIVE_DESIGN):
    """The Chroma collection for one chunking design (created empty if missing)."""
    global _CLIENT
    import chromadb

    if _CLIENT is None:
        CHROMA_DIR.mkdir(parents=True, exist_ok=True)
        _CLIENT = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return _CLIENT.get_or_create_collection(
        f"opas_{design}", embedding_function=None, metadata={"hnsw:space": "cosine"}
    )


def load_registry() -> dict:
    return json.loads(REGISTRY_PATH.read_text(encoding="utf-8")) if REGISTRY_PATH.exists() else {}


def save_registry(registry: dict) -> None:
    REGISTRY_PATH.parent.mkdir(parents=True, exist_ok=True)
    REGISTRY_PATH.write_text(json.dumps(registry, ensure_ascii=False, indent=2), encoding="utf-8")


# ---------------------------------------------------------------- search

def _row(id_, text, meta, score, rank) -> dict:
    return {"id": id_, "text": text, **meta, "score": round(float(score), 4), "rank": rank}


def dense_search(query: str, design: str, k: int, where: dict | None = None) -> list[dict]:
    col = collection(design)
    if col.count() == 0:
        return []
    res = col.query(
        query_embeddings=[embed_query(query)],
        n_results=min(k, col.count()),
        where=where or None,
        include=["documents", "metadatas", "distances"],
    )
    return [
        _row(i, d, m, 1 - dist, r + 1)
        for r, (i, d, m, dist) in enumerate(
            zip(res["ids"][0], res["documents"][0], res["metadatas"][0], res["distances"][0])
        )
    ]


class BM25:
    """Plain Okapi BM25 over one collection's chunk texts (no embeddings needed)."""

    def __init__(self, ids, docs, metas, k1: float = 1.5, b: float = 0.75):
        self.ids, self.docs, self.metas = ids, docs, metas
        self.tokens = [tokenize(d) for d in docs]
        self.k1, self.b = k1, b
        self.avgdl = sum(map(len, self.tokens)) / max(len(self.tokens), 1)
        df = Counter(t for toks in self.tokens for t in set(toks))
        n = len(self.tokens)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}
        self.tf = [Counter(toks) for toks in self.tokens]

    def search(self, query: str, k: int) -> list[dict]:
        q = tokenize(query)
        scores = []
        for i, tf in enumerate(self.tf):
            length = len(self.tokens[i])
            s = 0.0
            for t in q:
                if t in tf:
                    s += self.idf[t] * tf[t] * (self.k1 + 1) / (
                        tf[t] + self.k1 * (1 - self.b + self.b * length / self.avgdl)
                    )
            scores.append(s)
        order = sorted(range(len(scores)), key=lambda i: -scores[i])[:k]
        return [_row(self.ids[i], self.docs[i], self.metas[i], scores[i], r + 1) for r, i in enumerate(order)]


_BM25: dict[str, tuple[int, BM25]] = {}


def bm25_index(design: str) -> BM25:
    col = collection(design)
    count = col.count()
    if design not in _BM25 or _BM25[design][0] != count:
        data = col.get(include=["documents", "metadatas"])
        _BM25[design] = (count, BM25(data["ids"], data["documents"], data["metadatas"]))
    return _BM25[design][1]


def search(query: str, k: int = TOP_K, design: str = ACTIVE_DESIGN, mode: str = SEARCH_MODE,
           where: dict | None = None) -> list[dict]:
    """Top-k chunks for a query. mode="hybrid" fuses dense and BM25 with reciprocal rank fusion."""
    if mode == "dense":
        return dense_search(query, design, k, where)
    if mode != "hybrid":
        raise ValueError(f"Unknown search mode {mode!r}")
    pool = max(20, 4 * k)
    dense = dense_search(query, design, pool, where)
    sparse = bm25_index(design).search(query, pool)
    if where:
        sparse = [r for r in sparse if all(r.get(f) == v for f, v in where.items())]
    fused: dict[str, dict] = {}
    for results in (dense, sparse):
        for r in results:
            entry = fused.setdefault(r["id"], {**r, "score": 0.0})
            entry["score"] += 1 / (60 + r["rank"])
    ranked = sorted(fused.values(), key=lambda r: -r["score"])[:k]
    for i, r in enumerate(ranked, 1):
        r["rank"], r["score"] = i, round(r["score"], 4)
    return ranked


def citation(result: dict) -> str:
    """The exact citation string the agent must use, e.g. [RD1066-2007, Artículo 13]."""
    return f"[{result['doc_id']}, {result['location']}]"


def format_results(results: list[dict]) -> str:
    if not results:
        return "No results: the corpus has no passage for this query."
    blocks = []
    for r in results:
        where = r["doc_title"] + (f" · {r['section']}" if r.get("section") else "")
        blocks.append(
            f"--- Result {r['rank']} | cite as {citation(r)} | score {r['score']}\n"
            f"Source: {where}\n{r['text']}"
        )
    return "\n\n".join(blocks)
