"""Query embedding and retrieval for the committed Chroma index."""

from __future__ import annotations

import json
from pathlib import Path

import chromadb

from index import INDEX_DIR, embed_texts, get_collection

DEFAULT_DESIGN = "section"
CACHE = INDEX_DIR / "query_cache.json"


def embed_query(query: str) -> list[float]:
    CACHE.parent.mkdir(parents=True, exist_ok=True)
    cache: dict[str, list[float]] = {}
    if CACHE.is_file():
        try:
            cache = json.loads(CACHE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            cache = {}
    key = query.strip()
    if key in cache:
        return cache[key]
    vector = embed_texts([key], "RETRIEVAL_QUERY")[0]
    cache[key] = vector
    CACHE.write_text(json.dumps(cache), encoding="utf-8")
    return vector


def search_chunks(query: str, k: int = 5, design: str = DEFAULT_DESIGN, source: str | None = None):
    collection = get_collection(design)
    count = collection.count()
    if not count:
        return []
    try:
        kwargs = {"query_embeddings": [embed_query(query)], "n_results": min(k, max(1, count))}
        if source:
            kwargs["where"] = {"source": source}
        result = collection.query(**kwargs)
    except Exception:
        terms = {term.lower().strip(".,?!:;()") for term in query.split() if len(term) > 2}
        result_data = collection.get(include=["documents", "metadatas"])
        ranked = []
        for chunk_id, text, meta in zip(result_data["ids"], result_data["documents"], result_data["metadatas"]):
            if source and meta.get("source") != source:
                continue
            lower = text.lower()
            score = sum(lower.count(term) for term in terms)
            ranked.append((score, chunk_id, text, meta))
        ranked.sort(key=lambda item: item[0], reverse=True)
        ranked = ranked[:k]
        result = {
            "ids": [[r[1] for r in ranked]],
            "documents": [[r[2] for r in ranked]],
            "metadatas": [[r[3] for r in ranked]],
            "distances": [[1.0 - r[0] / max(1, len(terms)) for r in ranked]],
        }
    hits = []
    for i, chunk_id in enumerate(result["ids"][0]):
        meta = result["metadatas"][0][i]
        hits.append({
            "id": chunk_id,
            "text": result["documents"][0][i],
            "metadata": meta,
            "distance": result["distances"][0][i],
        })
    return hits


def format_hits(hits: list[dict]) -> str:
    if not hits:
        return "No matching passages found."
    lines = []
    for i, hit in enumerate(hits, 1):
        meta = hit["metadata"]
        lines.append(f"[{i}] Source: {meta.get('source', 'unknown')} | Location: {meta.get('location', 'unknown')}\n{hit['text']}")
    return "\n\n".join(lines)
