"""
Search the index built by index.py. Used by server.py (the search tool) and by
evaluate.py (hit rates), so what you measure is exactly what the agent gets.

    search(query)  -> the k chunks whose vectors are closest to the query's vector
    format_hits()  -> those chunks as text, each under its citation [source, location]
"""

from pathlib import Path

import index


def search(query: str, design: str = index.CHOSEN_DESIGN, k: int = index.TOP_K,
           path_index: Path = index.INDEX_DIR, embed_fn=None) -> list[dict]:
    """Embed the query (cached, so a repeated query costs nothing) and return the
    k nearest chunks by cosine distance: dicts with text, source, location, distance."""
    collection = index.open_collection(design, path=Path(path_index) / "chroma")
    if collection.count() == 0:
        return []
    cache = index.VectorCache(Path(path_index) / "vectors.sqlite")
    vector = index.embed_texts([query], index.QUERY_TASK, embed_fn=embed_fn, cache=cache)[0]
    result = collection.query(query_embeddings=[vector], n_results=min(k, collection.count()),
                              include=["documents", "metadatas", "distances"])
    return [{"id": cid, "text": text, "distance": dist, **meta}
            for cid, text, meta, dist in zip(result["ids"][0], result["documents"][0],
                                             result["metadatas"][0], result["distances"][0])]


def citation(hit: dict) -> str:
    return f"[{hit['source']}, {hit['location']}]"


def format_hits(hits: list[dict]) -> str:
    """What the search tool returns: each chunk under the citation to copy."""
    if not hits:
        return "No passages found in the corpus for this query."
    return "\n\n".join(f"Result {i} {citation(h)}\n{h['text']}" for i, h in enumerate(hits, start=1))
