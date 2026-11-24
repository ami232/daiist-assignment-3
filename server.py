"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Loads index/ at startup and never re-embeds the corpus. Logs go to stderr
(stdout carries the MCP protocol).
"""

import logging
import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer

import index
import retrieval

logging.basicConfig(stream=sys.stderr, level=logging.WARNING)
log = logging.getLogger("corpus")

mcp = MCPServer("corpus", log_level="WARNING")
_retriever: retrieval.Retriever | None = None


def retriever() -> retrieval.Retriever:
    global _retriever
    if _retriever is None:
        _retriever = retrieval.Retriever()
    return _retriever


@mcp.tool()
def search(query: str) -> str:
    """Search an index of official U.S. FDA food-safety guidance for consumers: how long
    foods keep in the fridge and freezer (FDA storage chart), safe storing, thawing,
    cooking temperatures, leftovers, power outages, eggs, seafood, produce, raw milk,
    soft cheeses, people at higher risk, and the FDA Bad Bug Book on foodborne bacteria,
    viruses and toxins (symptoms, onset, sources).

    Use it for any question about whether food is still safe to eat or how to handle it.
    Write the query in English with the specific food and situation
    (e.g. "raw chicken refrigerator storage days"). Call it again with other words
    if the first results do not answer the question.

    Returns the 5 most relevant passages, each headed by its citation
    [source | location], the document title and URL. Answer only from these passages.
    """
    query = (query or "").strip()
    if not query:
        return "Empty query: say which food and situation you want to look up."
    hits = retriever().search(query)
    return retrieval.format_hits(hits)


@mcp.tool()
def add_document(path: str) -> str:
    """Add one local file (.pdf, .html, .txt or .md) to the food-safety index so later
    searches can find it. The file is chunked with the same pipeline as the corpus,
    its chunks are embedded with Gemini and stored.

    If the same file (same name) with the same content is already indexed, nothing
    changes. If a file with that name is indexed but its content changed, the old
    chunks are replaced by the new ones.

    Returns how many chunks were added, kept or removed, and the source id to cite.
    """
    p = Path(path).expanduser()
    if not p.is_absolute():
        p = (Path(__file__).resolve().parent / p)
    if not p.is_file():
        return f"Not added: no file at {p}."
    try:
        chunks = index.chunk_file(p)
    except ValueError as e:
        return f"Not added: {e}"
    if not chunks:
        return f"Not added: no text could be extracted from {p.name}."

    col = retriever().col
    source = chunks[0].source
    old_ids = set(col.get(where={"source": source}, include=[])["ids"])
    new_ids = {c.id for c in chunks}

    if old_ids and old_ids == new_ids:
        return f"Already indexed: {p.name} ({len(old_ids)} chunks, source '{source}'). Nothing changed."

    stale = sorted(old_ids - new_ids)
    result = index.embed_and_store(chunks, col)
    if result["pending"]:
        retriever().reload()
        return (f"Partly added: {result['new']} chunks of {p.name} embedded, {result['pending']} still "
                f"pending because the daily embedding quota ran out. Old version kept. Try again tomorrow.")
    if stale:
        col.delete(ids=stale)
    retriever().reload()
    verb = "Replaced" if old_ids else "Added"
    return (f"{verb}: {p.name} as source '{source}'. {result['new']} new chunks embedded, "
            f"{result['skipped']} unchanged, {len(stale)} old chunks removed. "
            f"The index now holds {col.count()} chunks.")


if __name__ == "__main__":
    retriever()  # load the index before the first request
    mcp.run()  # stdio
