"""
Shared retrieval layer: embeddings, the on-disk store and search.

index.py WRITES the store; server.py, agent.py and evaluate.py READ it.

Store layout (plain text files, so an index built on Windows loads on macOS):

    index/config.json          {"design": "structure"}   which chunking design the server uses
    index/chunks_<design>.jsonl  one chunk per line: text + metadata (source, location, page ...)
    index/vectors.jsonl        append-only vector cache: {"k": key, "v": [768 floats]}
    index/queries.jsonl        cache of query vectors (saves quota on repeated questions)
    index/documents.json       registry of indexed documents (file hash, chunk counts)

A vector is looked up by key = hash(model + dims + embedded text), so a chunk
whose text did not change is never embedded twice.

Never print to stdout in this module: server.py uses stdout for the MCP protocol.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import time
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
INDEX_DIR = ROOT / "index"
CONFIG_FILE = INDEX_DIR / "config.json"
VECTORS_FILE = INDEX_DIR / "vectors.jsonl"
QUERIES_FILE = INDEX_DIR / "queries.jsonl"
REGISTRY_FILE = INDEX_DIR / "documents.json"

MODEL = "gemini-embedding-2"
DIMS = 768  # Gemini embeddings can be truncated (Matryoshka); 768 keeps index/ small
DESIGNS = ("fixed", "structure")
DEFAULT_DESIGN = "structure"
BATCH_SIZE = 16

# gemini-embedding-2 has no task_type parameter: the task goes in the text itself.
QUERY_PREFIX = "task: question answering | query: "


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


class QuotaExhausted(RuntimeError):
    """The free-tier daily embedding quota is used up. Saved vectors are kept."""


# --------------------------------------------------------------------------- #
# Embeddings
# --------------------------------------------------------------------------- #

_CLIENT = None


def _client():
    global _CLIENT
    if _CLIENT is None:
        from google import genai

        from api_key import load_api_key

        _CLIENT = genai.Client(api_key=load_api_key())
    return _CLIENT


def vector_key(text: str) -> str:
    return hashlib.sha256(f"{MODEL}|{DIMS}|{text}".encode("utf-8")).hexdigest()[:24]


def chunk_embed_text(chunk: dict) -> str:
    """The exact text that is embedded for a chunk (document format of gemini-embedding-2)."""
    return f"title: {chunk['title']} | text: {chunk['text']}"


def _is_daily_quota(message: str) -> bool:
    m = message.lower().replace("_", "").replace(" ", "")
    return "perday" in m or "daily" in m


def embed_batch(texts: list[str]) -> list[np.ndarray]:
    """Embed several texts in ONE request and return one unit vector per text.

    Each text must be its own Content object. Passing a plain list of strings
    makes gemini-embedding-2 return a SINGLE vector for the whole list
    (it treats them as parts of one multimodal input), which would silently
    break the index. The length check below guards against that.
    """
    from google.genai import types

    contents = [types.Content(parts=[types.Part(text=t)]) for t in texts]
    config = types.EmbedContentConfig(output_dimensionality=DIMS)
    result = None
    for attempt in range(1, 7):
        try:
            result = _client().models.embed_content(model=MODEL, contents=contents, config=config)
            break
        except Exception as error:  # noqa: BLE001 - classify by message
            message = str(error)
            lowered = message.lower()
            if "429" in message or "resource_exhausted" in lowered or "quota" in lowered:
                if _is_daily_quota(message):
                    raise QuotaExhausted(message[:400]) from error
                wait = min(70, 15 * attempt)
                log(f"  rate limit, waiting {wait}s (attempt {attempt}/6)")
                time.sleep(wait)
            elif any(code in message for code in ("500", "502", "503", "504")) or "unavailable" in lowered:
                time.sleep(5 * attempt)
            else:
                raise
    if result is None:
        raise RuntimeError("Embedding failed after 6 attempts (rate limit or server errors).")
    vectors = [np.asarray(e.values, dtype=np.float32) for e in result.embeddings]
    if len(vectors) != len(texts):
        raise RuntimeError(
            f"Sent {len(texts)} texts but got {len(vectors)} vectors back; refusing to store them."
        )
    return [v / np.linalg.norm(v) for v in vectors]


def _append_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False, separators=(",", ":")) + "\n")
        f.flush()


def load_vector_cache(path: Path = VECTORS_FILE) -> dict[str, np.ndarray]:
    cache: dict[str, np.ndarray] = {}
    if path.is_file():
        with path.open(encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    row = json.loads(line)
                    cache[row["k"]] = np.asarray(row["v"], dtype=np.float32)
    return cache


def save_vectors(keys: list[str], vectors: list[np.ndarray], path: Path = VECTORS_FILE) -> None:
    rows = [{"k": k, "v": [round(float(x), 6) for x in v]} for k, v in zip(keys, vectors)]
    _append_jsonl(path, rows)


_QUERY_CACHE: dict[str, np.ndarray] | None = None


def embed_query(query: str) -> np.ndarray:
    """Embed a question (cached on disk: asking the same question twice costs no quota)."""
    global _QUERY_CACHE
    if _QUERY_CACHE is None:
        _QUERY_CACHE = load_vector_cache(QUERIES_FILE)
    key = vector_key(QUERY_PREFIX + query)
    if key not in _QUERY_CACHE:
        vector = embed_batch([QUERY_PREFIX + query])[0]
        _QUERY_CACHE[key] = vector
        try:
            save_vectors([key], [vector], QUERIES_FILE)
        except OSError as error:  # a read-only checkout must not break search
            log(f"could not cache query vector: {error}")
    return _QUERY_CACHE[key]


# --------------------------------------------------------------------------- #
# Store and search
# --------------------------------------------------------------------------- #


def get_design() -> str:
    try:
        design = json.loads(CONFIG_FILE.read_text(encoding="utf-8")).get("design", DEFAULT_DESIGN)
    except (OSError, ValueError):
        design = DEFAULT_DESIGN
    return design if design in DESIGNS else DEFAULT_DESIGN


def chunks_path(design: str) -> Path:
    return INDEX_DIR / f"chunks_{design}.jsonl"


def read_chunks(design: str) -> list[dict]:
    path = chunks_path(design)
    if not path.is_file():
        return []
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def write_chunks(design: str, chunks: list[dict]) -> None:
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    with chunks_path(design).open("w", encoding="utf-8", newline="\n") as f:
        for c in chunks:
            f.write(json.dumps(c, ensure_ascii=False, separators=(",", ":")) + "\n")


class Store:
    def __init__(self, design: str, chunks: list[dict], matrix: np.ndarray):
        self.design, self.chunks, self.matrix = design, chunks, matrix


_STORES: dict[str, Store] = {}


def load_store(design: str | None = None, refresh: bool = False) -> Store:
    """Load chunks and their saved vectors. Never calls the embedding API."""
    design = design or get_design()
    if design in _STORES and not refresh:
        return _STORES[design]
    chunks = read_chunks(design)
    if not chunks:
        raise RuntimeError(f"No chunks for design '{design}'. Run `uv run python main.py index` first.")
    cache = load_vector_cache()
    missing = [c["id"] for c in chunks if c["key"] not in cache]
    if missing:
        raise RuntimeError(
            f"{len(missing)} of {len(chunks)} chunks of design '{design}' have no saved vector "
            f"(e.g. {missing[0]}). Run `uv run python main.py index` to embed them."
        )
    store = Store(design, chunks, np.stack([cache[c["key"]] for c in chunks]))
    _STORES[design] = store
    return store


def citation(chunk: dict) -> str:
    return f"[{chunk['source']} | {chunk['location']}]"


def search_vector(qvec: np.ndarray, k: int = 5, store: Store | None = None, source: str | None = None) -> list[dict]:
    store = store or load_store()
    scores = store.matrix @ qvec
    hits: list[dict] = []
    for i in np.argsort(-scores):
        chunk = store.chunks[int(i)]
        if source and chunk["source"] != source:
            continue
        hits.append({**chunk, "score": float(scores[i])})
        if len(hits) == k:
            break
    return hits


def search(query: str, k: int = 5, design: str | None = None, source: str | None = None) -> list[dict]:
    return search_vector(embed_query(query), k=k, store=load_store(design), source=source)


def format_results(hits: list[dict]) -> str:
    """Text for the model: every result carries the citation it must use."""
    if not hits:
        return "No results."
    blocks = []
    for n, h in enumerate(hits, 1):
        note = " | text amended by Regulation (EU) 2026/1744" if h.get("amended") else ""
        blocks.append(
            f"Result {n} | cite as {citation(h)} | page {h['page']} | score {h['score']:.2f}{note}\n{h['text']}"
        )
    return "\n\n".join(blocks)


# --------------------------------------------------------------------------- #
# Evaluation helper: does a chunk cover an expected (source, location)?
# --------------------------------------------------------------------------- #


def chunk_covers(chunk: dict, source: str, location: str) -> bool:
    """True if `chunk` is from `source` and its text covers `location`.

    Granularity is the article, annex or numbered paragraph: 'Article 5(1)(c)'
    counts as covered by any chunk containing text of Article 5. The same rule
    is applied to every chunking design, so their hit rates are comparable.
    """
    if chunk["source"] != source:
        return False
    loc = location.strip()
    m = re.match(r"(?i)^article\s+(\d+[a-z]?)", loc)
    if m:
        return m.group(1).lower() in [a.lower() for a in chunk.get("articles", [])]
    m = re.match(r"(?i)^annex\s+([ivxl]+)", loc)
    if m:
        return m.group(1).upper() in [a.upper() for a in chunk.get("annexes", [])]
    m = re.match(r"(?i)^(?:paragraphs?|para\.?)\s*\(?(\d+)", loc)
    if m and chunk.get("para_from") is not None:
        return chunk["para_from"] <= int(m.group(1)) <= chunk["para_to"]
    m = re.match(r"(?i)^(?:pages?|p\.)\s*(\d+)", loc)
    if m:
        return chunk["page_from"] <= int(m.group(1)) <= chunk["page_to"]
    return False
