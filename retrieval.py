"""
Retrieval over the committed index: dense (Gemini embeddings, cosine), BM25
(keywords), and hybrid (reciprocal rank fusion of the two).

Used by server.py (search tool) and evaluate.py (hit rate per design).
Nothing here re-embeds the corpus; only queries are embedded, and every query
vector is cached in index/query_cache.jsonl so re-running the evaluation does
not spend the daily quota again.
"""

from __future__ import annotations

import json
import math
import re
from collections import Counter
from pathlib import Path

import numpy as np

from settings import EMBED_DIMS, EMBED_MODEL, INDEX_DIR, QUERY_PREFIX, retrieval_config

TOKEN = re.compile(r"[a-z0-9]+(?:[-.()][a-z0-9]+)*")
STOP = set("""a an and are as at be by can do does for from has have how i if in is it its may
must not of on or our that the their them then there these they this to under was we what when
which who will with would you your shall any such""".split())


def tokenize(text: str) -> list[str]:
    tokens = TOKEN.findall(text.lower().replace("–", "-"))
    out = []
    for t in tokens:
        if t in STOP:
            continue
        out.append(t)
        if "-" in t or "(" in t:                # "206(4)-2" also matches "206", "4", "2"
            out.extend(p for p in re.split(r"[-.()]", t) if p and p not in STOP)
    return out


class BM25:
    def __init__(self, docs: list[str], k1: float = 1.5, b: float = 0.75):
        self.docs = [tokenize(d) for d in docs]
        self.k1, self.b = k1, b
        self.avg = sum(len(d) for d in self.docs) / max(len(self.docs), 1)
        df = Counter(t for d in self.docs for t in set(d))
        n = len(self.docs)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}
        self.tf = [Counter(d) for d in self.docs]

    def scores(self, query: str) -> np.ndarray:
        q = tokenize(query)
        out = np.zeros(len(self.docs))
        for i, (tf, d) in enumerate(zip(self.tf, self.docs)):
            norm = self.k1 * (1 - self.b + self.b * len(d) / self.avg)
            out[i] = sum(self.idf.get(t, 0) * tf[t] * (self.k1 + 1) / (tf[t] + norm) for t in q if t in tf)
        return out


class Index:
    """One chunking design loaded into memory: chunks, vector matrix, BM25."""

    def __init__(self, design: str):
        folder = INDEX_DIR / design
        self.design = design
        self.chunks = [json.loads(l) for l in (folder / "chunks.jsonl").read_text(encoding="utf-8").splitlines() if l.strip()]
        vectors = {}
        for line in (folder / "vectors.jsonl").read_text(encoding="utf-8").splitlines():
            if line.strip():
                try:
                    row = json.loads(line)
                    vectors[row["hash"]] = row["embedding"]
                except json.JSONDecodeError:
                    continue
        missing = [c["id"] for c in self.chunks if c["hash"] not in vectors]
        if missing:
            raise RuntimeError(f"{len(missing)} chunks in index/{design} have no vector (e.g. {missing[0]}). "
                               "Run `uv run python main.py index` to finish embedding.")
        matrix = np.array([vectors[c["hash"]] for c in self.chunks], dtype=np.float32)
        self.matrix = matrix / np.linalg.norm(matrix, axis=1, keepdims=True)
        self.bm25 = BM25([f"{c['section_title']} {c['location']} {c['text']}" for c in self.chunks])
        self.stamp = _stamp(design)

    def rank(self, method: str, query: str, query_vector: np.ndarray | None) -> list[int]:
        if method == "bm25":
            return list(np.argsort(-self.bm25.scores(query)))
        dense = list(np.argsort(-(self.matrix @ query_vector)))
        if method == "dense":
            return dense
        # hybrid: reciprocal rank fusion (k = 60) of the dense and keyword rankings
        keyword = list(np.argsort(-self.bm25.scores(query)))
        fused = Counter()
        for ranking in (dense, keyword):
            for rank, i in enumerate(ranking[:100]):
                fused[i] += 1 / (60 + rank + 1)
        return [i for i, _ in fused.most_common()]


def _stamp(design: str) -> tuple:
    folder = INDEX_DIR / design
    return tuple((folder / f).stat().st_mtime_ns for f in ("chunks.jsonl", "vectors.jsonl") if (folder / f).exists())


_INDEXES: dict[str, Index] = {}


def get_index(design: str) -> Index:
    """Load once; reload automatically after add_document rewrites the files."""
    index = _INDEXES.get(design)
    if index is None or index.stamp != _stamp(design):
        index = _INDEXES[design] = Index(design)
    return index


# ---- query embeddings, cached on disk ------------------------------------------

CACHE = INDEX_DIR / "query_cache.jsonl"
_cache: dict[str, list[float]] | None = None


def _load_cache() -> dict[str, list[float]]:
    global _cache
    if _cache is None:
        _cache = {}
        if CACHE.is_file():
            for line in CACHE.read_text(encoding="utf-8").splitlines():
                try:
                    row = json.loads(line)
                    _cache[row["key"]] = row["embedding"]
                except (json.JSONDecodeError, KeyError):
                    continue
    return _cache


def embed_query(query: str) -> np.ndarray:
    key = f"{EMBED_MODEL}|{EMBED_DIMS}|{query.strip()}"
    cache = _load_cache()
    if key not in cache:
        from index import embed_texts

        vector = embed_texts([QUERY_PREFIX + query.strip()])[0]
        cache[key] = vector
        with CACHE.open("a", encoding="utf-8") as out:
            out.write(json.dumps({"key": key, "embedding": [round(x, 6) for x in vector]}) + "\n")
    vector = np.array(cache[key], dtype=np.float32)
    return vector / np.linalg.norm(vector)


def search(query: str, k: int | None = None, design: str | None = None, method: str | None = None,
           source: str | None = None) -> list[dict]:
    """Top-k chunks for a query, each with its score rank and citation fields."""
    config = retrieval_config()
    design, method, k = design or config["design"], method or config["method"], k or config["k"]
    index = get_index(design)
    vector = None if method == "bm25" else embed_query(query)
    results = []
    for i in index.rank(method, query, vector):
        chunk = index.chunks[i]
        if source and chunk["source"] != source:
            continue
        results.append({**chunk, "rank": len(results) + 1})
        if len(results) == k:
            break
    return results


def format_results(results: list[dict]) -> str:
    """What the model reads. The id in brackets is what it must cite."""
    if not results:
        return "No passages found."
    parts = []
    for r in results:
        parts.append(f"=== [{r['id']}] {r['title']} | {r['location']} ===\n{r['text']}")
    return "\n\n".join(parts)


CITATION = re.compile(r"\[([A-Z][A-Z0-9]*:[^\]\s]+)\]")
RESULT_ID = re.compile(r"^=== \[([^\]]+)\] (.+?) \| (.+?) ===$", re.M)


def parse_results(text: str) -> list[dict]:
    """Recover (id, title, location) from a formatted search result."""
    return [{"id": m.group(1), "title": m.group(2), "location": m.group(3)} for m in RESULT_ID.finditer(text)]
