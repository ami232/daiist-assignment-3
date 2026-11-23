"""
Shared retrieval code: embeddings (with an on-disk cache), the ChromaDB store in
index/, and search (vector, keyword BM25, or hybrid). Used by index.py,
server.py, agent.py and evaluate.py.

Nothing here prints to stdout: server.py speaks MCP over stdout.
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

ROOT = Path(__file__).resolve().parent
# RAG_INDEX_DIR lets tests point at a copy of the index; normally it is index/.
INDEX_DIR = Path(os.environ.get("RAG_INDEX_DIR") or ROOT / "index")
CHROMA_DIR = INDEX_DIR / "chroma"
QUERY_CACHE = INDEX_DIR / "query_cache.json"
DOCUMENTS_FILE = INDEX_DIR / "documents.json"

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768          # auto-normalised by gemini-embedding-2; keeps index/ small
EMBED_BATCH = 20         # texts per request

# The retrieval designs compared in evaluate.py. Each is one Chroma collection.
# Chunk text differs between A and B, so each costs its own embeddings.
DESIGNS = ["fixed", "structure"]
# The design the server and agent use. Chosen from the hit-rate numbers (see REPORT.md).
ACTIVE_DESIGN = "structure"
ACTIVE_METHOD = "vector"  # "vector", "bm25" or "hybrid" — chosen by hit rate (REPORT.md, Retrieval)
TOP_K = 5


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


# --------------------------------------------------------------------------- embeddings

class QuotaExhausted(RuntimeError):
    """The free tier's daily embedding quota is used up. Everything embedded so far is saved."""


_client = None


def client():
    global _client
    if _client is None:
        from google import genai
        from api_key import load_api_key
        _client = genai.Client(api_key=load_api_key())
    return _client


def document_text(title: str, text: str) -> str:
    # gemini-embedding-2 takes the task as a text prefix, not as task_type.
    return f"title: {title or 'none'} | text: {text}"


def query_text(query: str) -> str:
    return f"task: question answering | query: {query}"


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed a batch, one vector per text. Retries rate limits; raises QuotaExhausted on the daily cap."""
    from google.genai import errors, types

    contents = [types.Content(parts=[types.Part.from_text(text=t)]) for t in texts]
    for attempt in range(6):
        try:
            result = client().models.embed_content(
                model=EMBED_MODEL,
                contents=contents,
                config=types.EmbedContentConfig(output_dimensionality=EMBED_DIM),
            )
            vectors = [list(e.values) for e in result.embeddings]
            if len(vectors) != len(texts):
                raise RuntimeError(f"asked for {len(texts)} embeddings, got {len(vectors)}")
            return vectors
        except errors.APIError as error:
            message = str(error)
            if error.code == 429 and ("PerDay" in message or "per day" in message.lower()):
                raise QuotaExhausted(message) from error
            if error.code in (429, 500, 502, 503, 504) and attempt < 5:
                wait = 15 * (attempt + 1)
                log(f"Gemini {error.code}; retrying in {wait}s")
                time.sleep(wait)
                continue
            raise
    raise RuntimeError("unreachable")


def _load_query_cache() -> dict:
    if QUERY_CACHE.is_file():
        return json.loads(QUERY_CACHE.read_text(encoding="utf-8"))
    return {}


_query_cache: dict | None = None


def embed_query(query: str) -> list[float]:
    """Embed a search query, reusing a saved vector when the same query was seen before."""
    global _query_cache
    if _query_cache is None:
        _query_cache = _load_query_cache()
    text = query_text(query.strip())
    key = hashlib.sha256(f"{EMBED_MODEL}|{EMBED_DIM}|{text}".encode()).hexdigest()[:24]
    if key not in _query_cache:
        vector = embed_texts([text])[0]
        _query_cache[key] = [round(x, 6) for x in vector]
        INDEX_DIR.mkdir(exist_ok=True)
        QUERY_CACHE.write_text(json.dumps(_query_cache), encoding="utf-8")
    return _query_cache[key]


# --------------------------------------------------------------------------- store

_chroma = None


def chroma():
    global _chroma
    if _chroma is None:
        import chromadb
        from chromadb.config import Settings
        _chroma = chromadb.PersistentClient(path=str(CHROMA_DIR), settings=Settings(anonymized_telemetry=False))
    return _chroma


def collection(design: str):
    return chroma().get_or_create_collection(name=f"corpus_{design}", metadata={"hnsw:space": "cosine"})


def load_documents() -> dict:
    if DOCUMENTS_FILE.is_file():
        return json.loads(DOCUMENTS_FILE.read_text(encoding="utf-8"))
    return {}


def save_documents(documents: dict) -> None:
    INDEX_DIR.mkdir(exist_ok=True)
    DOCUMENTS_FILE.write_text(json.dumps(documents, indent=2, ensure_ascii=False), encoding="utf-8")


# --------------------------------------------------------------------------- search

TOKEN = re.compile(r"[a-z0-9]+(?:\(\w+\))*", re.I)
STOP = set("a an the of to in for and or is are be by on with as at that this it its from which "
           "what when how do does i my we our can must should under if any not".split())


def tokenize(text: str) -> list[str]:
    return [t for t in (m.group(0).lower() for m in TOKEN.finditer(text)) if t not in STOP]


class BM25:
    def __init__(self, ids: list[str], texts: list[str], k1: float = 1.5, b: float = 0.75):
        self.ids, self.k1, self.b = ids, k1, b
        self.docs = [Counter(tokenize(t)) for t in texts]
        self.lengths = [sum(d.values()) for d in self.docs]
        self.avg = sum(self.lengths) / max(1, len(self.lengths))
        df = Counter(term for d in self.docs for term in d)
        n = len(self.docs)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}

    def top(self, query: str, k: int) -> list[tuple[str, float]]:
        terms = tokenize(query)
        scores = []
        for i, d in enumerate(self.docs):
            s = 0.0
            for t in terms:
                if t in d:
                    tf = d[t]
                    s += self.idf[t] * tf * (self.k1 + 1) / (tf + self.k1 * (1 - self.b + self.b * self.lengths[i] / self.avg))
            scores.append((self.ids[i], s))
        scores.sort(key=lambda x: -x[1])
        return [x for x in scores[:k] if x[1] > 0]


_bm25: dict[tuple, tuple[int, BM25]] = {}


def bm25_for(design: str, sources: list[str] | None = None) -> BM25:
    """Keyword index over the collection (or only some documents, so word statistics match)."""
    col = collection(design)
    count = col.count()
    key = (design, tuple(sorted(sources or [])))
    if key not in _bm25 or _bm25[key][0] != count:   # rebuilt after add_document
        where = {"source": {"$in": list(sources)}} if sources else None
        data = col.get(where=where, include=["documents"])
        _bm25[key] = (count, BM25(data["ids"], data["documents"]))
    return _bm25[key][1]


def search(query: str, k: int = TOP_K, design: str = ACTIVE_DESIGN, method: str = ACTIVE_METHOD,
           sources: list[str] | None = None) -> list[dict]:
    """Return the top-k chunks as dicts: id, text, score and metadata (source, location, ...).
    `sources` restricts the search to those documents (evaluate.py keeps the design comparison
    on the original corpus even after add_document)."""
    col = collection(design)
    pool = max(k * 4, 20)
    vector_ids: list[str] = []
    bm25_ids: list[str] = []
    if method in ("vector", "hybrid"):
        where = {"source": {"$in": list(sources)}} if sources else None
        res = col.query(query_embeddings=[embed_query(query)], n_results=min(pool, col.count()), where=where)
        vector_ids = res["ids"][0]
    if method in ("bm25", "hybrid"):
        bm25_ids = [i for i, _ in bm25_for(design, sources).top(query, pool)]
    if method == "vector":
        ranked = vector_ids
    elif method == "bm25":
        ranked = bm25_ids
    else:  # reciprocal rank fusion
        fused = Counter()
        for ids in (vector_ids, bm25_ids):
            for rank, i in enumerate(ids):
                fused[i] += 1 / (60 + rank)
        ranked = [i for i, _ in fused.most_common()]
    top = ranked[:k]
    if not top:
        return []
    got = col.get(ids=top, include=["documents", "metadatas"])
    by_id = {i: (d, m) for i, d, m in zip(got["ids"], got["documents"], got["metadatas"])}
    return [{"id": i, "rank": r + 1, "text": by_id[i][0], **by_id[i][1]} for r, i in enumerate(top)]


def citation(chunk: dict) -> str:
    return f"[{chunk['source']} | {chunk['location']}]"


def format_results(chunks: list[dict]) -> str:
    if not chunks:
        return "No passages found in the corpus for this query."
    parts = []
    for c in chunks:
        page = f", p. {c['page']}" if c.get("page", -1) not in (-1, None, "") else ""
        parts.append(
            f"Result {c['rank']}: {citation(c)}\n"
            f"Document: {c['title']}{page}\nSection: {c['section']}\n\n{c['text']}"
        )
    return "\n\n---\n\n".join(parts)


# --------------------------------------------------------------------------- citations

CITATION = re.compile(r"\[([^\[\]|]{2,40}?)\s*\|\s*([^\[\]]{2,60}?)\]")
RESULT_HEADER = re.compile(r"^Result \d+: \[([^\]|]+?) \| ([^\]]+?)\]\s*$", re.M)
ROMAN_VALUES = {"i": 1, "ii": 2, "iii": 3, "iv": 4, "v": 5, "vi": 6, "vii": 7, "viii": 8, "ix": 9, "x": 10,
                "xi": 11, "xii": 12, "xiii": 13, "xiv": 14, "xv": 15}


def find_citations(answer: str) -> list[tuple[str, str]]:
    """All [source | location] labels in an answer."""
    return [(s.strip(), l.strip()) for s, l in CITATION.findall(answer)]


def retrieved_labels(tool_output: str) -> list[tuple[str, str]]:
    """The [source | location] labels of the passages in one search result."""
    return [(s.strip(), l.strip()) for s, l in RESULT_HEADER.findall(tool_output)]


def _point(text: str, context: tuple | None = None) -> tuple | None:
    """Parse one location into a comparable (kind, major, minor) tuple.
    'Art. 33(1)' -> ('art', 33, 1); 'para. 29' -> ('para', 29, 0); 'Annex ex. iv' -> ('annex', 4, 0).
    A bare '(4)' or '31' or 'iii' continues the kind/major of `context` (the start of a range)."""
    t = text.strip().lower().replace("article", "art.").replace("paragraphs", "para.").replace("paragraph", "para.")
    if m := re.match(r"^art\.?\s*(\d+)\s*(?:\((\w+)\))?", t):
        minor = m.group(2)
        return ("art", int(m.group(1)), _minor(minor))
    if m := re.match(r"^paras?\.?\s*(\d+)", t):
        return ("para", int(m.group(1)), 0)
    if m := re.match(r"^annex(?:\s*b)?\s*(?:ex\.?|example)?\s*([ivx]+)\b", t):
        return ("annex", ROMAN_VALUES.get(m.group(1), 0), 0)
    if context:
        if context[0] == "art" and (m := re.match(r"^\((\w+)\)", t)):
            return ("art", context[1], _minor(m.group(1)))
        if context[0] == "para" and t.isdigit():
            return ("para", int(t), 0)
        if context[0] == "annex" and t in ROMAN_VALUES:
            return ("annex", ROMAN_VALUES[t], 0)
    if t.startswith("sec."):
        return ("sec", t, 0)
    return None


def _minor(value: str | None) -> int:
    if value is None:
        return 0
    return int(value) if value.isdigit() else 100 + ord(value[0])   # points (a), (b) after numbers


def _range(location: str) -> tuple | None:
    parts = re.split(r"\s*[–-]\s*(?=[\(\w])", location, maxsplit=1)
    start = _point(parts[0])
    if start is None:
        return None
    end = _point(parts[1], start) if len(parts) > 1 else start
    return start, (end or start)


def location_covered(cited: str, passage: str) -> bool:
    """Is the cited location inside the location span of a retrieved passage?
    'Art. 33(1)' is inside 'Art. 33(1)–(4)'; 'Art. 33' (whole article) counts if the passage is part of it."""
    c, p = _range(cited), _range(passage)
    if not c or not p:
        return cited.strip().lower() == passage.strip().lower()
    (ck, cmaj, cmin), _ = c
    (pk, pmaj, pmin), (_, emaj, emin) = p
    if ck != pk:
        return False
    if ck == "sec":
        return cmaj == pmaj
    if not (pmaj <= cmaj <= emaj):
        return False
    if ck != "art" or cmin == 0:
        return True
    if pmaj == emaj:
        return pmin <= cmin <= emin or pmin == 0
    # span across articles, e.g. Art. 32(4)–Art. 33(2)
    if cmaj == pmaj:
        return cmin >= pmin
    if cmaj == emaj:
        return emin == 0 or cmin <= emin
    return True


def check_citations(answer: str, retrieved: list[tuple[str, str]]) -> tuple[list, list]:
    """Split the answer's citations into (valid, invalid) against the retrieved labels."""
    valid, invalid = [], []
    for source, location in find_citations(answer):
        ok = any(source.lower() == s.lower() and location_covered(location, l) for s, l in retrieved)
        (valid if ok else invalid).append(f"[{source} | {location}]")
    return valid, invalid
