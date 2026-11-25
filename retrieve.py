"""
Retrieval: given a question, find the most relevant chunks in index/.

Three designs (compared in evaluate.py):
  - "fixed":           vector search over the 200-word windows
  - "sections":        vector search over the subsection chunks
  - "sections_hybrid": vector search + keyword (BM25) search over the subsection
                       chunks, merged with Reciprocal Rank Fusion. Keyword search
                       helps with exact terms like "CrCl", "2.5 mg", "idarucizumab".

Used by server.py (the search tool) and evaluate.py (hit rate).
It only LOADS the index: it never re-embeds the corpus (only the question).
"""

import re

from rank_bm25 import BM25Okapi

from config import CHOSEN_DESIGN, TOP_K
from index import embed_queries, get_collection

_collections = {}   # opened Chroma collections, so we open each one only once
_bm25 = {}          # keyword index per collection, built on first use


def collection_for(design: str):
    """'sections_hybrid' uses the same stored chunks as 'sections'."""
    name = "fixed" if design == "fixed" else "sections"
    if name not in _collections:
        _collections[name] = get_collection(name)
    return _collections[name]


def reset_cache() -> None:
    """Forget the keyword index (call after add_document, so the new chunks are searchable)."""
    _bm25.clear()


def as_chunk(chunk_id: str, text: str, metadata: dict) -> dict:
    """One search result as a simple dict."""
    return {"id": chunk_id, "text": text, "source": metadata["source"],
            "location": metadata["location"], "section": metadata["section"]}


# --- Vector search -----------------------------------------------------------

def vector_search(query_vector: list[float], design: str, k: int) -> list[dict]:
    """The k chunks whose vectors are closest to the question's vector."""
    result = collection_for(design).query(query_embeddings=[query_vector], n_results=k)
    # Chroma returns lists of lists (one list per query); we sent one query -> take [0].
    return [as_chunk(i, d, m) for i, d, m in
            zip(result["ids"][0], result["documents"][0], result["metadatas"][0])]


# --- Keyword search (BM25) ----------------------------------------------------

def tokenize(text: str) -> list[str]:
    """Lower-case words and numbers like 2.5 -> ['apixaban', '2.5', 'mg', ...]."""
    return re.findall(r"[a-z0-9]+(?:\.[0-9]+)?", text.lower())


def keyword_search(query: str, design: str, k: int) -> list[dict]:
    """The k chunks that share the most (rare) words with the question."""
    collection = collection_for(design)
    if design not in _bm25:                       # build the keyword index once
        everything = collection.get()             # all chunks (text + metadata), no vectors
        bm25 = BM25Okapi([tokenize(text) for text in everything["documents"]])
        _bm25[design] = (bm25, everything)
    bm25, everything = _bm25[design]

    scores = bm25.get_scores(tokenize(query))
    best = sorted(range(len(scores)), key=lambda i: scores[i], reverse=True)[:k]
    return [as_chunk(everything["ids"][i], everything["documents"][i], everything["metadatas"][i])
            for i in best]


# --- Put it together ----------------------------------------------------------

def search(query: str, design: str = CHOSEN_DESIGN, k: int = TOP_K,
           query_vector: list[float] | None = None) -> list[dict]:
    """Return the top-k chunks for the question, using one of the three designs."""
    if query_vector is None:
        query_vector = embed_queries([query])[0]  # 1 embedding per question, in query format

    if design in ("fixed", "sections"):
        return vector_search(query_vector, design, k)

    # Hybrid: get 20 candidates from each method, then Reciprocal Rank Fusion:
    # every chunk scores 1/(60 + rank) in each list it appears in; add the scores up.
    scores, chunks = {}, {}
    for results in (vector_search(query_vector, design, 20), keyword_search(query, design, 20)):
        for rank, chunk in enumerate(results, start=1):
            scores[chunk["id"]] = scores.get(chunk["id"], 0) + 1 / (60 + rank)
            chunks[chunk["id"]] = chunk
    best = sorted(scores, key=scores.get, reverse=True)[:k]
    return [chunks[i] for i in best]


def format_results(chunks: list[dict]) -> str:
    """Turn the chunks into the text the agent reads. Each starts with its citation tag."""
    if not chunks:
        return "No results."
    # Each chunk's text already starts with "[SOURCE §location] (Section name)".
    return "\n\n---\n\n".join(chunk["text"] for chunk in chunks)
