"""
Shared RAG pieces: Gemini embeddings with a saved-vector cache, and search over the index.

index.py, server.py and evaluate.py all import this module, so the corpus is embedded
in one place and searched the same way everywhere.

    index/embeddings.jsonl     one saved vector per chunk text (never embedded twice)
    index/queries.jsonl        saved query vectors (the evaluation reuses them)
    index/<design>/chunks.jsonl  the chunks of one chunking design, with their metadata
    index/config.json          the design and search method the server uses
"""

import hashlib
import json
import math
import re
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
INDEX_DIR = ROOT / "index"
EMBEDDINGS = INDEX_DIR / "embeddings.jsonl"
QUERY_CACHE = INDEX_DIR / "queries.jsonl"
CONFIG = INDEX_DIR / "config.json"

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768                 # smaller vectors keep index/ small; plenty for a few hundred chunks
BATCH = 20                      # texts per embedding request (keeps each request under the token limit)
DEFAULT_CONFIG = {"design": "sections", "search": "vector", "k": 5}


def log(*args) -> None:
    """Log to stderr: stdout carries the MCP protocol when the server runs."""
    print(*args, file=sys.stderr, flush=True)


def text_key(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------- embeddings
_client = None
_cache: dict[str, dict[str, list[float]]] = {}


def client():
    global _client
    if _client is None:
        from google import genai

        from api_key import load_api_key
        _client = genai.Client(api_key=load_api_key())
    return _client


def _load_cache(path: Path) -> dict[str, list[float]]:
    if str(path) not in _cache:
        vectors = {}
        if path.is_file():
            for line in path.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    row = json.loads(line)
                    vectors[row["key"]] = row["vector"]
        _cache[str(path)] = vectors
    return _cache[str(path)]


def _embed_batch(texts: list[str], task: str) -> list[list[float]]:
    """One request to Gemini, retried on rate limits (the free tier allows few requests a minute)."""
    from google.genai import types

    config = types.EmbedContentConfig(task_type=task, output_dimensionality=EMBED_DIM)
    # one Content per text: for gemini-embedding-2 the SDK merges a plain list of strings
    # into ONE content and returns ONE vector for all of them
    contents = [types.Content(parts=[types.Part(text=t)]) for t in texts]
    for attempt in range(6):
        try:
            response = client().models.embed_content(model=EMBED_MODEL, contents=contents, config=config)
            vectors = [list(e.values) for e in response.embeddings]
            if len(vectors) != len(texts):
                raise RuntimeError(f"asked for {len(texts)} embeddings, got {len(vectors)}")
            return vectors
        except Exception as error:  # noqa: BLE001
            message = str(error)
            if "429" in message or "RESOURCE_EXHAUSTED" in message or "503" in message:
                if "PerDay" in message or "per day" in message.lower():
                    raise RuntimeError(
                        "The daily embedding quota is used up. Everything embedded so far is saved; "
                        "run the same command again after 09:00 (Spain) and it continues where it stopped."
                    ) from error
                wait = 30 * (attempt + 1)
                log(f"rate limited, waiting {wait}s ...")
                time.sleep(wait)
            else:
                raise
    raise RuntimeError("Gemini kept refusing the embedding request.")


def embed(texts: list[str], task: str = "RETRIEVAL_DOCUMENT") -> np.ndarray:
    """Vectors for these texts. Saved vectors are reused; new ones are saved as soon as they arrive."""
    path = EMBEDDINGS if task == "RETRIEVAL_DOCUMENT" else QUERY_CACHE
    cache = _load_cache(path)
    keys = [text_key(t) for t in texts]
    missing = list(dict.fromkeys(t for t, k in zip(texts, keys) if k not in cache))
    if missing:
        log(f"embedding {len(missing)} new text(s) with {EMBED_MODEL} ...")
        path.parent.mkdir(exist_ok=True)
        for start in range(0, len(missing), BATCH):
            batch = missing[start:start + BATCH]
            vectors = _embed_batch(batch, task)
            with path.open("a", encoding="utf-8") as f:       # save right away: a crash loses nothing
                for text, vector in zip(batch, vectors):
                    vector = [round(v, 6) for v in vector]
                    cache[text_key(text)] = vector
                    f.write(json.dumps({"key": text_key(text), "vector": vector}) + "\n")
    return np.array([cache[k] for k in keys], dtype=np.float32)


def has_vector(text: str) -> bool:
    return text_key(text) in _load_cache(EMBEDDINGS)


# ---------------------------------------------------------------- the index
def read_chunks(design: str) -> list[dict]:
    path = INDEX_DIR / design / "chunks.jsonl"
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def write_chunks(design: str, chunks: list[dict]) -> None:
    path = INDEX_DIR / design / "chunks.jsonl"
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("".join(json.dumps(c, ensure_ascii=False) + "\n" for c in chunks), encoding="utf-8")


def load_config() -> dict:
    if CONFIG.is_file():
        return {**DEFAULT_CONFIG, **json.loads(CONFIG.read_text())}
    return dict(DEFAULT_CONFIG)


WORD = re.compile(r"[a-z0-9]+")


def tokens(text: str) -> list[str]:
    return WORD.findall(text.lower())


class Index:
    """All chunks of one design in memory: a vector matrix plus a BM25 keyword index."""

    def __init__(self, design: str, include_added: bool = True):
        self.design = design
        self.chunks = [c for c in read_chunks(design) if include_added or not c.get("added")]
        if not self.chunks:
            raise RuntimeError(f"index/{design}/chunks.jsonl is empty. Run `uv run python main.py index`.")
        without = [c["id"] for c in self.chunks if not has_vector(c["embed_text"])]
        if without:
            raise RuntimeError(f"{len(without)} chunk(s) in index/{design} have no saved vector. "
                               f"Run `uv run python main.py index` to embed them.")
        vectors = embed([c["embed_text"] for c in self.chunks])
        self.matrix = vectors / np.linalg.norm(vectors, axis=1, keepdims=True)
        # BM25 keyword statistics, for hybrid search (costs no embeddings)
        self.doc_tokens = [Counter(tokens(c["embed_text"])) for c in self.chunks]
        self.lengths = np.array([sum(t.values()) for t in self.doc_tokens], dtype=float)
        df = Counter(term for t in self.doc_tokens for term in t)
        n = len(self.chunks)
        self.idf = {term: math.log(1 + (n - f + 0.5) / (f + 0.5)) for term, f in df.items()}

    def vector_scores(self, query: str) -> np.ndarray:
        q = embed([query], task="RETRIEVAL_QUERY")[0]
        return self.matrix @ (q / np.linalg.norm(q))

    def bm25_scores(self, query: str, k1: float = 1.5, b: float = 0.75) -> np.ndarray:
        avg = self.lengths.mean()
        scores = np.zeros(len(self.chunks))
        for term in set(tokens(query)):
            if term not in self.idf:
                continue
            tf = np.array([t.get(term, 0) for t in self.doc_tokens], dtype=float)
            scores += self.idf[term] * tf * (k1 + 1) / (tf + k1 * (1 - b + b * self.lengths / avg))
        return scores

    def search(self, query: str, k: int = 5, method: str = "vector") -> list[dict]:
        if method == "vector":
            order = np.argsort(-self.vector_scores(query))
        elif method == "hybrid":
            # reciprocal rank fusion: a chunk ranked high by either method rises to the top
            rrf = np.zeros(len(self.chunks))
            for scores in (self.vector_scores(query), self.bm25_scores(query)):
                ranks = np.empty(len(scores), dtype=int)
                ranks[np.argsort(-scores)] = np.arange(len(scores))
                rrf += 1 / (60 + ranks + 1)
            order = np.argsort(-rrf)
        else:
            raise ValueError(f"unknown search method {method!r}")
        return [self.chunks[i] for i in order[:k]]


def cite(chunk: dict) -> str:
    return f"{chunk['title']} > {chunk['location']}"


def format_results(chunks: list[dict]) -> str:
    """What the search tool returns: each chunk with its id and citation."""
    blocks = [f"[{c['id']}] {cite(c)}\nURL: {c['url']}\n\n{c['text']}" for c in chunks]
    return "\n\n---\n\n".join(blocks)
