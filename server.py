"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it and stores it.

Loads the committed index/; never re-embeds the corpus. stdout carries the protocol,
so anything index.py prints is redirected to stderr.
"""

import contextlib
import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer

import index

mcp = MCPServer("corpus", log_level="WARNING")

_collection = None
_client = None


def collection():
    global _collection
    if _collection is None:
        _collection = index.get_collection()
    return _collection


def client():
    global _client
    if _client is None:
        _client = index.get_client()
    return _client


@mcp.tool()
def search(query: str, company: str = "", section: str = "", k: int = 5) -> str:
    """Search the 10-K annual reports of Ralph Lauren (RL), PVH and Tapestry (TPR),
    covering Item 1 Business, Item 1A Risk Factors and Item 7 MD&A (narrative text only,
    NOT the financial statements or their notes). Use it for every factual question about
    these companies. Returns the k most relevant passages, each labelled with its citation
    [company | section | chunk number | fiscal year end]. Optional filters: company
    ("RL", "PVH" or "TPR") and section ("Item 1. Business", "Item 1A. Risk Factors",
    "Item 7. MD&A"). If no passage answers the question, the answer is not in the corpus."""
    conditions = []
    if company:
        conditions.append({"ticker": company.upper()})
    if section:
        conditions.append({"section": section})
    where = None if not conditions else (conditions[0] if len(conditions) == 1 else {"$and": conditions})

    vector = index.embed_texts(client(), [index.query_text(query)])[0]
    result = collection().query(
        query_embeddings=[vector], n_results=max(1, min(k, 10)), where=where)

    passages = []
    for doc, meta, dist in zip(result["documents"][0], result["metadatas"][0], result["distances"][0]):
        citation = (f"[{meta['ticker']} | {meta['section']} | chunk {meta['chunk_number']} "
                    f"| fiscal year end {meta['fiscal_year_end']}]")
        passages.append(f"{citation} (similarity {1 - dist:.3f})\n{doc}")
    return "\n\n".join(passages) or "No passages found."


@mcp.tool()
def add_document(path: str) -> str:
    """Add a new document (an .htm, .html or .txt file in this repository) to the search
    index: it is split into chunks, embedded with Gemini and stored. This spends embedding
    quota and changes the index, so it needs user approval. If the same file (same name)
    or identical content is already indexed, nothing is changed and the reply says so; if
    the same name exists with different content, nothing is changed either and the user
    must decide (rename the file to add it as a new version)."""
    file = Path(path).expanduser().resolve()
    if not file.is_file():
        return f"File not found: {path}. Nothing was added."

    digest = index.file_hash(file)
    registry = index.load_registry()

    if file.name in registry:
        if registry[file.name]["sha256"] == digest:
            return (f"Already indexed: {file.name} is in the index with identical content "
                    f"({registry[file.name]['chunks']} chunks). Nothing was changed.")
        return (f"Conflict: a document named {file.name} is already indexed but this file's "
                f"content is DIFFERENT. Nothing was changed. If it is a new version, rename "
                f"the file and add it again.")
    for name, entry in registry.items():
        if entry["sha256"] == digest:
            return f"Already indexed under the name {name} (identical content). Nothing was changed."

    chunks = index.chunk_file(file)
    with contextlib.redirect_stdout(sys.stderr):  # stdout is the MCP channel
        added = index.embed_and_store(chunks, collection())
    index.register_document(file, len(chunks))
    return f"Added {file.name}: {len(chunks)} chunks, {added} newly embedded."


if __name__ == "__main__":
    mcp.run()  # stdio