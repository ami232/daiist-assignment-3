"""
Shared retrieval code for Assignment 3.

index.py writes the index with these helpers, server.py serves it, and
evaluate.py measures it. Keeping it in one place means the three stages can't
drift apart (same embedding model, same cache, same ranking code).

Nothing here prints to stdout, because server.py speaks MCP over stdout.
Everything is logged to stderr.
"""

from __future__ import annotations

import hashlib
import json
import math
import os
import re
import sys
import time
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INDEX_DIR = ROOT / "index"
CHROMA_DIR = INDEX_DIR / "chroma"
BASELINE_CACHE = INDEX_DIR / "query_cache.json"      # committed: vectors for the test questions
RUNTIME_CACHE = ROOT / "cache" / "query_cache.json"  # git-ignored: queries the agent invents
COLLECTION = "chunks"

EMBED_MODEL = os.environ.get("EMBED_MODEL", "gemini-embedding-2")
EMBED_DIMS = 768
# gemini-embedding-2 folds a list of texts into ONE vector, so it is called one text at a time.
# Batches are small so that progress is saved often when a rate limit interrupts a run.
PER_TEXT = "embedding-2" in EMBED_MODEL
EMBED_BATCH = 10 if PER_TEXT else 50
PER_TEXT_PAUSE = 0.7   # seconds between calls, to stay under the per-minute limit

TOP_K = 5
DEFAULT_DESIGN = "hybrid"   # chosen from the hit rates in eval/retrieval.csv
DESIGNS = ("vector", "bm25", "hybrid")


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


# ---------------------------------------------------------------- embeddings

def _normalise(vector: list[float]) -> list[float]:
    norm = math.sqrt(sum(x * x for x in vector)) or 1.0
    return [round(x / norm, 6) for x in vector]


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed texts with Gemini, one vector per text, in order.

    Retries on rate limits and server errors. Raises RuntimeError with a plain
    message when the daily quota is gone, so callers can stop and resume later.
    """
    from google import genai
    from google.genai import types

    from api_key import load_api_key

    client = genai.Client(api_key=load_api_key())
    config = types.EmbedContentConfig(output_dimensionality=EMBED_DIMS)
    vectors: list[list[float]] = []

    def call(batch: list[str]):
        delay = 5.0
        for attempt in range(8):
            try:
                return client.models.embed_content(model=EMBED_MODEL, contents=batch, config=config)
            except Exception as error:  # noqa: BLE001
                message = str(error)
                squashed = message.lower().replace(" ", "").replace("_", "")
                quota = "RESOURCE_EXHAUSTED" in message or "429" in message
                transient = quota or "503" in message or "500" in message or "UNAVAILABLE" in message
                if "perday" in squashed or "daily" in squashed:
                    raise RuntimeError(
                        "The daily embedding limit looks used up. Everything embedded so far "
                        "is saved. Run the same command again after midnight Pacific time."
                    ) from error
                if not transient or attempt == 7:
                    raise
                log(f"embedding call failed ({message[:120]}), retrying in {delay:.0f}s")
                time.sleep(delay)
                delay = min(delay * 2, 60)

    for start in range(0, len(texts), EMBED_BATCH):
        batch = texts[start:start + EMBED_BATCH]
        if PER_TEXT:
            got = []
            for text in batch:
                got.append(list(call([text]).embeddings[0].values))
                time.sleep(PER_TEXT_PAUSE)
        else:
            response = call(batch)
            got = [list(e.values) for e in response.embeddings]
            if len(got) != len(batch):
                log(f"batch of {len(batch)} returned {len(got)} vectors, embedding one at a time")
                got = [list(call([text]).embeddings[0].values) for text in batch]
        vectors.extend(_normalise(v) for v in got)
    return vectors


# --------------------------------------------------------------- query cache

def _cache_key(query: str) -> str:
    return hashlib.sha1(f"{EMBED_MODEL}|{EMBED_DIMS}|{query.strip()}".encode("utf-8")).hexdigest()


def _read_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}
    except (OSError, ValueError):
        return {}


def load_query_cache() -> dict[str, list[float]]:
    cache = _read_json(BASELINE_CACHE)
    cache.update(_read_json(RUNTIME_CACHE))
    return cache


def save_baseline_queries(queries: list[str]) -> int:
    """Embed any of these queries not yet cached and store them in index/ (committed).

    Returns the number of new embeddings. This is what lets check.py and the
    evaluation search the test questions without spending quota again.
    """
    baseline = _read_json(BASELINE_CACHE)
    wanted = {_cache_key(q): q for q in queries}
    missing = [(k, q) for k, q in wanted.items() if k not in baseline]
    if missing:
        vectors = embed_texts([q for _, q in missing])
        for (key, _), vector in zip(missing, vectors):
            baseline[key] = vector
        INDEX_DIR.mkdir(exist_ok=True)
        BASELINE_CACHE.write_text(json.dumps(baseline), encoding="utf-8")
    return len(missing)


def embed_query(query: str) -> list[float]:
    key = _cache_key(query)
    cache = load_query_cache()
    if key in cache:
        return cache[key]
    vector = embed_texts([query])[0]
    try:
        runtime = _read_json(RUNTIME_CACHE)
        runtime[key] = vector
        RUNTIME_CACHE.parent.mkdir(exist_ok=True)
        RUNTIME_CACHE.write_text(json.dumps(runtime), encoding="utf-8")
    except OSError:
        pass
    return vector


# -------------------------------------------------------------------- chroma

def get_collection():
    import chromadb
    from chromadb.config import Settings

    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR), settings=Settings(anonymized_telemetry=False))
    return client.get_or_create_collection(COLLECTION, configuration={"hnsw": {"space": "cosine"}})


# ---------------------------------------------------------------------- BM25

_STOP = {
    "the", "a", "an", "of", "to", "in", "and", "or", "is", "are", "be", "for", "on", "by",
    "that", "with", "as", "at", "it", "this", "what", "which", "when", "how", "does", "do",
}


def tokenize(text: str) -> list[str]:
    tokens = []
    for token in re.findall(r"[a-z0-9]+", text.lower()):
        if token in _STOP:
            continue
        if len(token) > 3 and token.endswith("s") and not token.isdigit():
            token = token[:-1]
        tokens.append(token)
    return tokens


class BM25:
    def __init__(self, documents: list[str], k1: float = 1.5, b: float = 0.75):
        self.k1, self.b = k1, b
        self.lengths = []
        self.postings: dict[str, dict[int, int]] = defaultdict(dict)
        for index, document in enumerate(documents):
            counts = Counter(tokenize(document))
            self.lengths.append(sum(counts.values()))
            for term, count in counts.items():
                self.postings[term][index] = count
        self.count = len(documents)
        self.average = (sum(self.lengths) / self.count) if self.count else 1.0

    def scores(self, query: str) -> dict[int, float]:
        scores: dict[int, float] = defaultdict(float)
        for term in set(tokenize(query)):
            postings = self.postings.get(term)
            if not postings:
                continue
            idf = math.log(1 + (self.count - len(postings) + 0.5) / (len(postings) + 0.5))
            for index, tf in postings.items():
                norm = tf + self.k1 * (1 - self.b + self.b * self.lengths[index] / self.average)
                scores[index] += idf * tf * (self.k1 + 1) / norm
        return scores


# -------------------------------------------------------------------- search

@dataclass
class Hit:
    id: str
    text: str
    source: str
    location: str
    doc_title: str
    heading: str
    score: float
    rank: int

    @property
    def label(self) -> str:
        return cite_label(self.source, self.location)


def cite_label(source: str, location: str) -> str:
    return f"[{source} | {location}]"


def normalise_label(source: str, location: str) -> str:
    """Compare citations without caring about case, spacing or a leading section sign."""
    clean = lambda s: re.sub(r"\s+", " ", s.replace("§", "")).strip().strip(".").lower()
    return f"{clean(source)}|{clean(location)}"


class Index:
    """The chunks in Chroma plus an in-memory BM25 over the same text."""

    def __init__(self):
        self.reload()

    def reload(self) -> None:
        collection = get_collection()
        data = collection.get(include=["documents", "metadatas"])
        self.collection = collection
        self.ids: list[str] = list(data["ids"])
        self.docs: list[str] = list(data["documents"])
        self.metas: list[dict] = [dict(m or {}) for m in data["metadatas"]]
        self.position = {chunk_id: i for i, chunk_id in enumerate(self.ids)}
        self.bm25 = BM25(self.docs)

    def __len__(self) -> int:
        return len(self.ids)

    def _hit(self, index: int, score: float, rank: int) -> Hit:
        meta = self.metas[index]
        return Hit(
            id=self.ids[index], text=self.docs[index], source=meta.get("source", ""),
            location=meta.get("location", ""), doc_title=meta.get("doc_title", ""),
            heading=meta.get("heading", ""), score=score, rank=rank,
        )

    def _vector_ranking(self, query: str, depth: int) -> list[tuple[int, float]]:
        vector = embed_query(query)
        result = self.collection.query(query_embeddings=[vector], n_results=min(depth, len(self.ids)),
                                       include=["distances"])
        return [(self.position[i], 1.0 - d) for i, d in zip(result["ids"][0], result["distances"][0])
                if i in self.position]

    def _bm25_ranking(self, query: str, depth: int) -> list[tuple[int, float]]:
        scores = self.bm25.scores(query)
        return sorted(scores.items(), key=lambda item: -item[1])[:depth]

    def search(self, query: str, k: int = TOP_K, design: str = DEFAULT_DESIGN, depth: int = 30) -> list[Hit]:
        """Rank chunks for a query. design is 'vector', 'bm25' or 'hybrid' (reciprocal rank fusion)."""
        if not self.ids or not query.strip():
            return []
        if design == "bm25":
            ranking = self._bm25_ranking(query, depth)
        elif design == "vector":
            ranking = self._vector_ranking(query, depth)
        else:
            try:
                vector_ranking = self._vector_ranking(query, depth)
            except Exception as error:  # noqa: BLE001 - keep answering with keyword search
                log(f"vector search unavailable ({type(error).__name__}: {str(error)[:150]}), using keywords only")
                vector_ranking = []
            fused: dict[int, float] = defaultdict(float)
            for ranking_list in (vector_ranking, self._bm25_ranking(query, depth)):
                for rank, (index, _) in enumerate(ranking_list):
                    fused[index] += 1.0 / (60 + rank)
            ranking = sorted(fused.items(), key=lambda item: -item[1])
        return [self._hit(index, score, rank) for rank, (index, score) in enumerate(ranking[:k], start=1)]


def format_hits(hits: list[Hit]) -> str:
    """The text the model reads. The 'Cite as' line is what it must copy into answers."""
    if not hits:
        return "No passages found. The index is empty or the query was blank."
    blocks = []
    for number, hit in enumerate(hits, start=1):
        blocks.append(
            f"Result {number}\n"
            f"Cite as: {hit.label}\n"
            f"Document: {hit.doc_title}\n"
            f"Text:\n{hit.text}"
        )
    return "\n\n".join(blocks)
