"""Search over the saved index. Used by server.py and evaluate.py."""

import hashlib
import json
from pathlib import Path

import numpy as np

import index as pipeline

ROOT = Path(__file__).resolve().parent
QUERY_CACHE = ROOT / "eval" / "query_cache.jsonl"
_STATE: dict = {}
_QUERIES: dict | None = None


def reload() -> None:
    """Forget the loaded index (used after add_document)."""
    _STATE.clear()


def load_design(design: str | None = None):
    design = design or pipeline.get_design()
    if design not in _STATE:
        vectors = pipeline.load_vectors()
        chunks = [c for c in pipeline.read_chunks(design) if c["hash"] in vectors]
        matrix = np.array([vectors[c["hash"]] for c in chunks], dtype=np.float32)
        _STATE[design] = (chunks, matrix)
    return _STATE[design]


def embed_query(query: str) -> np.ndarray:
    """Embed a question. Saved in eval/query_cache.jsonl, so each question costs quota only once."""
    global _QUERIES
    if _QUERIES is None:
        _QUERIES = {}
        if QUERY_CACHE.is_file():
            for line in QUERY_CACHE.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    row = json.loads(line)
                    _QUERIES[row["h"]] = row["v"]
    key = hashlib.sha1(query.strip().encode("utf-8")).hexdigest()
    if key not in _QUERIES:
        vector = pipeline.embed_texts(pipeline.get_client(), [query.strip()])[0]
        _QUERIES[key] = vector
        QUERY_CACHE.parent.mkdir(exist_ok=True)
        with QUERY_CACHE.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"h": key, "v": vector}) + "\n")
    return np.asarray(_QUERIES[key], dtype=np.float32)


def search(query: str, k: int = 5, design: str | None = None) -> list[tuple[float, dict]]:
    """Top-k chunks by cosine similarity (vectors are normalised): [(score, chunk)]."""
    chunks, matrix = load_design(design)
    if not chunks:
        return []
    scores = matrix @ embed_query(query)
    top = np.argsort(-scores)[:k]
    return [(float(scores[i]), chunks[i]) for i in top]


def chunk_matches(chunk: dict, source: str, location: str) -> bool:
    if chunk["source"].strip().lower() != source.strip().lower():
        return False
    if not location.strip():
        return True
    return location.strip().lower() in [loc.lower() for loc in chunk["locations"]]


def is_hit(results: list[tuple[float, dict]], expected_source: str, expected_location: str) -> bool:
    """True if every expected (source, location) pair appears in the results.

    Several passages are separated by ';' in both columns, as in eval/README.md.
    """
    sources = [s.strip() for s in expected_source.split(";") if s.strip()]
    locations = [loc.strip() for loc in expected_location.split(";")]
    locations += [""] * (len(sources) - len(locations))
    return all(
        any(chunk_matches(chunk, source, location) for _, chunk in results)
        for source, location in zip(sources, locations)
    )
