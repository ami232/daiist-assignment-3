"""Retrieval over the ChromaDB index. Shared by server.py (search tool) and evaluate.py (hit rate).

Nothing here embeds the corpus: it embeds only the question (cached on disk by index.embed_query)
and looks up the nearest stored chunks.
"""
from __future__ import annotations

from index import ACTIVE_DESIGN, embed_query, get_collection

_collections: dict = {}


def collection(design: str | None = None):
    design = design or ACTIVE_DESIGN
    if design not in _collections:
        _collections[design] = get_collection(design)
    return _collections[design]


def retrieve(query: str, k: int = 5, design: str | None = None) -> list[dict]:
    """The k stored chunks closest to the query, best first.

    Each hit has: citation ("[source | location]"), source, location, title, url, text, score
    (cosine similarity, higher is closer).
    """
    store = collection(design)
    total = store.count()
    if total == 0:
        return []
    result = store.query(query_embeddings=[embed_query(query)], n_results=min(k, total),
                         include=["documents", "metadatas", "distances"])
    hits = []
    for text, meta, distance in zip(result["documents"][0], result["metadatas"][0], result["distances"][0]):
        hits.append({
            "citation": f"[{meta['source']} | {meta['location']}]",
            "source": meta["source"],
            "location": meta["location"],
            "title": meta.get("title", ""),
            "url": meta.get("url", ""),
            "text": text,
            "score": round(1 - distance, 3),
        })
    return hits


def format_hits(hits: list[dict]) -> str:
    """Plain-text form returned by the search tool: one block per chunk, with its citation."""
    if not hits:
        return "No passages found: the index is empty."
    blocks = []
    for number, hit in enumerate(hits, 1):
        blocks.append(
            f"### Result {number} (similarity {hit['score']})\n"
            f"Citation: {hit['citation']}\n"
            f"Document: {hit['title']}\n"
            f"URL: {hit['url']}\n"
            f"Text: {hit['text']}")
    return "\n\n".join(blocks)