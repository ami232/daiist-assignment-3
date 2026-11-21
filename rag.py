"""
Shared RAG plumbing used by index.py, server.py and evaluate.py:
configuration, Gemini embeddings with an on-disk cache, ChromaDB access and retrieval.

Nothing here may print to stdout (server.py speaks MCP over stdout): log to stderr.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import sys
import time
import unicodedata
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

import numpy as np

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
INDEX_DIR = ROOT / "index"
CORPUS_DIR = ROOT / "corpus"  # git-ignored; filled by index.py
CHROMA_DIR = INDEX_DIR / "chroma"
DOC_CACHE_FILE = INDEX_DIR / "vector_cache.jsonl"  # text -> vector, written as we go
QUERY_CACHE_FILE = INDEX_DIR / "query_cache.jsonl"  # question -> vector

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768  # 768 / 1536 / 3072 are the recommended sizes; smaller = smaller index
BATCH_SIZE = 20  # texts per embedding request (each text counts against the daily quota)

DESIGNS = ("fixed", "structure")  # the two chunking designs we compare

# >>> Update this after you have read the numbers from `main.py evaluate`. <<<
# The server and the agent use it. design: "fixed" | "structure"; method: "dense" | "hybrid".
CHOSEN = {"design": "structure", "method": "hybrid", "k": 5}


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


class QuotaExhausted(RuntimeError):
    """The Gemini free-tier daily embedding quota is used up."""


# ---------------------------------------------------------------- embeddings

# gemini-embedding-2 does not use `task_type`; the task goes into the text itself.
# (Formats as documented by Google for gemini-embedding-2; verify against
#  https://ai.google.dev/gemini-api/docs/embeddings if retrieval looks odd.)
def doc_prompt(text: str) -> str:
    return f"title: none | text: {text}"


def query_prompt(query: str) -> str:
    return f"task: search result | query: {query}"


class VectorCache:
    """Append-only JSONL cache: a crash or the daily limit never loses a vector."""

    def __init__(self, path: Path):
        self.path = path
        self._data: dict[str, list[float]] | None = None

    def _load(self) -> dict[str, list[float]]:
        if self._data is None:
            self._data = {}
            if self.path.exists():
                for line in self.path.read_text(encoding="utf-8").splitlines():
                    if not line.strip():
                        continue
                    try:
                        row = json.loads(line)
                    except json.JSONDecodeError:  # half-written last line after a crash
                        continue
                    self._data[row["k"]] = row["v"]
        return self._data

    def get(self, key: str):
        return self._load().get(key)

    def __contains__(self, key: str) -> bool:
        return key in self._load()

    def add(self, keys: list[str], vectors: list[list[float]]) -> None:
        data = self._load()
        self.path.parent.mkdir(parents=True, exist_ok=True)
        with self.path.open("a", encoding="utf-8") as f:
            for k, v in zip(keys, vectors):
                v = [round(float(x), 6) for x in v]
                data[k] = v
                f.write(json.dumps({"k": k, "v": v}) + "\n")


_DOC_CACHE = VectorCache(DOC_CACHE_FILE)
_QUERY_CACHE = VectorCache(QUERY_CACHE_FILE)
_client = None
EMBEDDED_THIS_RUN = 0  # texts sent to the API in this process (for quota bookkeeping)


def _cache_key(prompt: str) -> str:
    return hashlib.sha1(f"{EMBED_MODEL}|{EMBED_DIM}|{prompt}".encode("utf-8")).hexdigest()


def _genai_client():
    global _client
    if _client is None:
        from google import genai

        _client = genai.Client(api_key=load_api_key())
    return _client


def _normalize(vectors) -> list[list[float]]:
    arr = np.asarray(vectors, dtype=np.float64)
    norms = np.linalg.norm(arr, axis=1, keepdims=True)
    norms[norms == 0] = 1.0
    return (arr / norms).tolist()


def _embed_batch(prompts: list[str]) -> list[list[float]]:
    """One embedding request (with retries). Returns one vector per prompt."""
    from google.genai import types

    delay = 5.0
    for attempt in range(6):
        try:
            contents = [types.Content(parts=[types.Part.from_text(text=p)]) for p in prompts]
            response = _genai_client().models.embed_content(
                model=EMBED_MODEL,
                contents=contents,
                config=types.EmbedContentConfig(output_dimensionality=EMBED_DIM),
            )
            vectors = [e.values for e in response.embeddings]
            if len(vectors) != len(prompts):
                # Some multimodal models fuse a batch into one vector: go one by one.
                log(f"batch of {len(prompts)} returned {len(vectors)} vectors; embedding one by one")
                vectors = []
                for p in prompts:
                    r = _genai_client().models.embed_content(
                        model=EMBED_MODEL,
                        contents=[types.Content(parts=[types.Part.from_text(text=p)])],
                        config=types.EmbedContentConfig(output_dimensionality=EMBED_DIM),
                    )
                    vectors.append(r.embeddings[0].values)
            return _normalize(vectors)
        except Exception as error:  # noqa: BLE001
            message = str(error)
            exhausted = "RESOURCE_EXHAUSTED" in message or "429" in message
            if exhausted and ("PerDay" in message or "per day" in message.lower()):
                raise QuotaExhausted(
                    "Daily Gemini embedding quota reached. Everything embedded so far is saved; "
                    "re-run after midnight Pacific time (09:00 in Spain) and it will carry on."
                ) from error
            if exhausted and attempt < 5:
                log(f"rate limited; waiting {delay:.0f}s (attempt {attempt + 1}/5)")
                time.sleep(delay)
                delay *= 2
                continue
            raise
    raise RuntimeError("unreachable")


def embed_texts(prompts: list[str], kind: str) -> np.ndarray:
    """Embed prompts (already prefixed). kind: 'doc' or 'query'. Cached; saves after every batch."""
    global EMBEDDED_THIS_RUN
    cache = _DOC_CACHE if kind == "doc" else _QUERY_CACHE
    keys = [_cache_key(p) for p in prompts]
    todo: dict[str, str] = {}
    for key, prompt in zip(keys, prompts):
        if key not in cache and key not in todo:
            todo[key] = prompt
    items = list(todo.items())
    for start in range(0, len(items), BATCH_SIZE):
        batch = items[start : start + BATCH_SIZE]
        vectors = _embed_batch([p for _, p in batch])
        cache.add([k for k, _ in batch], vectors)
        EMBEDDED_THIS_RUN += len(batch)
        log(f"embedded {min(start + BATCH_SIZE, len(items))}/{len(items)} new texts")
    return np.asarray([cache.get(k) for k in keys], dtype=np.float64)


# -------------------------------------------------------------------- chroma

_chroma = None


def get_collection(design: str):
    global _chroma
    import chromadb

    if _chroma is None:
        CHROMA_DIR.mkdir(parents=True, exist_ok=True)
        _chroma = chromadb.PersistentClient(
            path=str(CHROMA_DIR), settings=chromadb.Settings(anonymized_telemetry=False)
        )
    return _chroma.get_or_create_collection(name=design, metadata={"hnsw:space": "cosine"})


@dataclass
class Chunk:
    id: str
    design: str
    source: str  # file name, e.g. "lau.pdf"  (this is what expected_source refers to)
    location: str  # "p.12", "p.12-13" or a section title
    section: str  # nearest heading, "" if unknown
    text: str
    page_start: int | None
    page_end: int | None
    doc_sha1: str

    def metadata(self) -> dict:
        return {
            "source": self.source,
            "location": self.location,
            "section": self.section,
            "page_start": -1 if self.page_start is None else self.page_start,
            "page_end": -1 if self.page_end is None else self.page_end,
            "doc_sha1": self.doc_sha1,
            "words": len(self.text.split()),
        }


# ----------------------------------------------------------------- retrieval

def _tokens(text: str) -> list[str]:
    text = unicodedata.normalize("NFKD", text.lower())
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.findall(r"\w+", text)


class BM25:
    def __init__(self, docs: list[str], k1: float = 1.5, b: float = 0.75):
        self.k1, self.b = k1, b
        self.tf = [Counter(_tokens(d)) for d in docs]
        self.len = np.array([sum(c.values()) for c in self.tf], dtype=float)
        self.avg = self.len.mean() if len(docs) else 1.0
        df: Counter = Counter()
        for c in self.tf:
            df.update(c.keys())
        n = len(docs)
        self.idf = {t: math.log(1 + (n - d + 0.5) / (d + 0.5)) for t, d in df.items()}

    def scores(self, query: str) -> np.ndarray:
        out = np.zeros(len(self.tf))
        for t in set(_tokens(query)):
            idf = self.idf.get(t)
            if idf is None:
                continue
            for i, c in enumerate(self.tf):
                f = c.get(t, 0)
                if f:
                    out[i] += idf * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * self.len[i] / self.avg))
        return out


_bm25_cache: dict[str, tuple[int, BM25, dict]] = {}


def _bm25(design: str):
    col = get_collection(design)
    count = col.count()
    cached = _bm25_cache.get(design)
    if cached and cached[0] == count:  # rebuilt automatically after add_document
        return cached[1], cached[2]
    data = col.get(include=["documents", "metadatas"])
    rows = {
        "ids": data["ids"],
        "docs": data["documents"],
        "metas": data["metadatas"],
    }
    index = BM25(rows["docs"])
    _bm25_cache[design] = (count, index, rows)
    return index, rows


def _hit(id_: str, text: str, meta: dict, score: float) -> dict:
    return {
        "id": id_,
        "text": text,
        "source": meta["source"],
        "location": meta["location"],
        "section": meta.get("section", ""),
        "page_start": None if meta.get("page_start", -1) == -1 else meta["page_start"],
        "page_end": None if meta.get("page_end", -1) == -1 else meta["page_end"],
        "score": float(score),
    }


def dense_search(design: str, query: str, k: int) -> list[dict]:
    col = get_collection(design)
    n = min(k, col.count())
    if n == 0:
        return []
    q = embed_texts([query_prompt(query)], "query")[0]
    res = col.query(
        query_embeddings=[q.tolist()], n_results=n, include=["documents", "metadatas", "distances"]
    )
    return [
        _hit(i, d, m, 1 - dist)
        for i, d, m, dist in zip(res["ids"][0], res["documents"][0], res["metadatas"][0], res["distances"][0])
    ]


def bm25_search(design: str, query: str, k: int) -> list[dict]:
    index, rows = _bm25(design)
    if not rows["ids"]:
        return []
    scores = index.scores(query)
    order = np.argsort(-scores)[:k]
    return [_hit(rows["ids"][i], rows["docs"][i], rows["metas"][i], scores[i]) for i in order if scores[i] > 0]


def hybrid_search(design: str, query: str, k: int, pool: int = 30, rrf_k: int = 60) -> list[dict]:
    """Reciprocal-rank fusion of dense and BM25 rankings. Costs one query embedding, like dense."""
    dense = dense_search(design, query, pool)
    lexical = bm25_search(design, query, pool)
    fused: dict[str, float] = {}
    by_id: dict[str, dict] = {}
    for ranking in (dense, lexical):
        for rank, h in enumerate(ranking):
            fused[h["id"]] = fused.get(h["id"], 0.0) + 1.0 / (rrf_k + rank + 1)
            by_id[h["id"]] = h
    top = sorted(fused, key=fused.get, reverse=True)[:k]
    return [{**by_id[i], "score": fused[i]} for i in top]


def search(query: str, design: str | None = None, method: str | None = None, k: int | None = None) -> list[dict]:
    design = design or CHOSEN["design"]
    method = method or CHOSEN["method"]
    k = k or CHOSEN["k"]
    if method == "dense":
        return dense_search(design, query, k)
    if method == "bm25":
        return bm25_search(design, query, k)
    if method == "hybrid":
        return hybrid_search(design, query, k)
    raise ValueError(f"unknown retrieval method {method!r}")


def format_hits(query: str, hits: list[dict]) -> str:
    """What the search tool returns. The header `[source | location]` is the citation key."""
    if not hits:
        return f"Query: {query}\nNo passages found."
    lines = [f"Query: {query}", f"Top {len(hits)} passages:", ""]
    for n, h in enumerate(hits, 1):
        section = f" (section: {h['section']})" if h["section"] and h["section"] != h["location"] else ""
        lines.append(f"[{n}] [{h['source']} | {h['location']}]{section}")
        lines.append(h["text"])
        lines.append("")
    return "\n".join(lines).strip()


HEADER_RE = re.compile(r"^\[(\d+)\]\s+\[([^\]|]+?)\s*\|\s*([^\]]+?)\]", re.MULTILINE)
CITATION_RE = re.compile(r"\[([^\[\]|]+?)\s*\|\s*([^\[\]]+?)\]")


def norm_key(source: str, location: str) -> str:
    return f"{source.strip().lower()} | {re.sub(r'\s+', ' ', location.strip().lower())}"


def parse_passages(tool_text: str) -> list[dict]:
    """Parse format_hits() output back into passages (used by the agent and the evaluation)."""
    matches = list(HEADER_RE.finditer(tool_text))
    passages = []
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else len(tool_text)
        body = tool_text[m.end() : end]
        body = re.sub(r"^\s*\(section:[^\n]*\)", "", body).strip()
        passages.append({"source": m.group(2).strip(), "location": m.group(3).strip(), "text": body})
    return passages


# ---------------------------------------------------- hit-rate bookkeeping

_PAGE_REF = re.compile(r"^(?:p\.?|pp\.?|page|pág\.?|pagina|página)\s*(\d+)(?:\s*[-–]\s*(\d+))?$", re.IGNORECASE)


def location_match(expected: str, hit: dict) -> bool:
    """Does a retrieved chunk cover the location a test question points to?

    expected may be a page ("p.12", "page 12-13") or a section/article label ("Article 5").
    """
    expected = (expected or "").strip()
    if not expected:
        return True
    m = _PAGE_REF.match(expected)
    if m:
        start, end = hit.get("page_start"), hit.get("page_end")
        if start is None:  # passages parsed back from tool output only carry "p.12-13"
            loc = re.match(r"^p\.(\d+)(?:-(\d+))?$", hit.get("location", ""))
            if loc:
                start, end = int(loc.group(1)), int(loc.group(2) or loc.group(1))
        if start is not None:
            lo = int(m.group(1))
            hi = int(m.group(2) or lo)
            return start <= hi and (end or start) >= lo
    haystack = f"{hit.get('location', '')} {hit.get('section', '')}".lower()
    needle = expected.lower()
    return needle in haystack or (len(haystack.strip()) > 3 and haystack.strip() in needle)


def covers(expected_sources: str, expected_locations: str, hits: list[dict]) -> bool:
    """True if, for every expected (source, location) pair, some retrieved chunk matches it."""
    sources = [s.strip() for s in expected_sources.split(";") if s.strip()]
    locations = [s.strip() for s in (expected_locations or "").split(";")]
    if len(locations) != len(sources):
        locations = [""] * len(sources) if not any(locations) else [expected_locations.strip()] * len(sources)
    for source, location in zip(sources, locations):
        if not any(h["source"] == source and location_match(location, h) for h in hits):
            return False
    return True
