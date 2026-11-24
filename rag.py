"""
Assignment 3: retrieval over the committed index. Used by server.py and evaluate.py.

    load_collection(design)          the ChromaDB collection of one chunking design
    embed_query(text)                query vector, cached in index/query_cache.json
    search(query, design, k, mode)   mode "vector" or "hybrid" (BM25 + vector, RRF)

Hybrid search costs no extra embeddings: BM25 runs on the stored chunk text and
the query vector is the same one vector search uses.
"""

from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

import index as index_stage
from index import DEFAULT_CONFIG, DESIGNS, EMBED_MODEL, index_dir

MODES = ("vector", "hybrid")
RRF_K = 60          # the usual constant of reciprocal rank fusion
CANDIDATES = 30     # how many results each ranker contributes before fusion

_collections: dict[tuple[str, str], object] = {}
_bm25: dict[tuple[str, str], tuple[int, object, list[dict]]] = {}
_query_cache: dict[str, dict[str, list[float]]] = {}


def load_config() -> dict:
    path = index_dir() / "config.json"
    config = dict(DEFAULT_CONFIG)
    if path.exists():
        config.update(json.loads(path.read_text(encoding="utf-8")))
    return config


def load_collection(design: str):
    key = (str(index_dir()), design)
    if key not in _collections:
        _collections[key] = index_stage.open_collection(design)
    return _collections[key]


# --------------------------------------------------------------------------
# Query vectors, embedded once and kept
# --------------------------------------------------------------------------

def _cache_path() -> Path:
    return index_dir() / "query_cache.json"


def _cache_key(text: str) -> str:
    return hashlib.sha256(f"{EMBED_MODEL}\n{text.strip()}".encode("utf-8")).hexdigest()


def _load_query_cache() -> dict[str, list[float]]:
    path = str(_cache_path())
    if path not in _query_cache:
        file = _cache_path()
        _query_cache[path] = json.loads(file.read_text(encoding="utf-8")) if file.exists() else {}
    return _query_cache[path]


def embed_query(text: str) -> list[float]:
    """The vector of a query. Never embeds the same query twice."""
    cache = _load_query_cache()
    key = _cache_key(text)
    if key not in cache:
        vector = index_stage.embed_texts([text.strip()], "query")[0]
        cache[key] = [round(v, 6) for v in vector]
        file = _cache_path()
        file.parent.mkdir(parents=True, exist_ok=True)
        temporary = file.with_suffix(".json.tmp")
        temporary.write_text(json.dumps(cache), encoding="utf-8")
        temporary.replace(file)
    return cache[key]


# --------------------------------------------------------------------------
# Search
# --------------------------------------------------------------------------

_TOKEN = re.compile(r"[a-z0-9]+")
_STOP = set("a an and are as at be by for from in is it of on or that the this to with shall which".split())


def tokenize(text: str) -> list[str]:
    return [t for t in _TOKEN.findall(text.lower()) if t not in _STOP]


def _row(chunk_id: str, text: str, meta: dict, score: float) -> dict:
    return {
        "chunk_id": chunk_id,
        "doc_id": meta.get("doc_id", ""),
        "doc_title": meta.get("doc_title", ""),
        "part": meta.get("part", ""),
        "location": meta.get("location", ""),
        "locations": [x for x in str(meta.get("locations", "")).split(";") if x],
        "heading": meta.get("heading", ""),
        "paragraph": meta.get("paragraph", ""),
        "url": meta.get("url", ""),
        "words": meta.get("words", 0),
        "text": text,
        "score": round(float(score), 4),
    }


def _vector_search(query: str, design: str, n: int) -> list[dict]:
    collection = load_collection(design)
    count = collection.count()
    if count == 0:
        return []
    result = collection.query(
        query_embeddings=[embed_query(query)], n_results=min(n, count),
        include=["documents", "metadatas", "distances"],
    )
    return [
        _row(chunk_id, text, meta, 1.0 - distance)  # cosine similarity
        for chunk_id, text, meta, distance in zip(
            result["ids"][0], result["documents"][0], result["metadatas"][0], result["distances"][0]
        )
    ]


def _bm25_index(design: str):
    """BM25 over every stored chunk; rebuilt when the collection changes size."""
    from rank_bm25 import BM25Okapi

    collection = load_collection(design)
    key = (str(index_dir()), design)
    count = collection.count()
    cached = _bm25.get(key)
    if cached and cached[0] == count:
        return cached[1], cached[2]
    stored = collection.get(include=["documents", "metadatas"])
    rows = [
        _row(chunk_id, text, meta, 0.0)
        for chunk_id, text, meta in zip(stored["ids"], stored["documents"], stored["metadatas"])
    ]
    rows.sort(key=lambda r: r["chunk_id"])  # stable order whatever the storage order
    headers = {i: m.get("header", "") for i, m in zip(stored["ids"], stored["metadatas"])}
    corpus = [tokenize(f"{headers[r['chunk_id']]} {r['text']}") for r in rows]
    bm25 = BM25Okapi(corpus) if corpus else None
    _bm25[key] = (count, bm25, rows)
    return bm25, rows


def _bm25_search(query: str, design: str, n: int) -> list[dict]:
    bm25, rows = _bm25_index(design)
    if bm25 is None:
        return []
    scores = bm25.get_scores(tokenize(query))
    order = sorted(range(len(rows)), key=lambda i: (-scores[i], rows[i]["chunk_id"]))[:n]
    return [dict(rows[i], score=round(float(scores[i]), 4)) for i in order if scores[i] > 0]


def search(query: str, design: str | None = None, k: int | None = None, mode: str | None = None) -> list[dict]:
    """Top k chunks for a query. Defaults come from index/config.json."""
    config = load_config()
    design = design or config["design"]
    k = int(k or config["k"])
    mode = mode or config["mode"]
    if design not in DESIGNS:
        raise ValueError(f"Unknown design {design!r}; use one of {DESIGNS}")
    if mode not in MODES:
        raise ValueError(f"Unknown mode {mode!r}; use one of {MODES}")
    if mode == "vector":
        return _vector_search(query, design, k)
    # hybrid: reciprocal rank fusion of the two rankings
    fused: dict[str, float] = {}
    rows: dict[str, dict] = {}
    for ranking in (_vector_search(query, design, CANDIDATES), _bm25_search(query, design, CANDIDATES)):
        for rank, row in enumerate(ranking, start=1):
            fused[row["chunk_id"]] = fused.get(row["chunk_id"], 0.0) + 1.0 / (RRF_K + rank)
            rows.setdefault(row["chunk_id"], row)
    order = sorted(fused, key=lambda i: (-fused[i], i))[:k]
    return [dict(rows[i], score=round(fused[i], 4)) for i in order]


if __name__ == "__main__":
    import sys

    question = " ".join(sys.argv[1:]) or "minimum time limit for tenders in an open procedure"
    for hit in search(question):
        print(f"[{hit['doc_id']} | {hit['location']}] {hit['score']}  {hit['text'][:120]!r}")
