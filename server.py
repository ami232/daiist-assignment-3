"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Loads index/ at startup; never re-embeds the corpus. Nothing is printed to
stdout (it carries the protocol); logs go to stderr.
"""

from pathlib import Path

from mcp.server.mcpserver import MCPServer

import index as ix
import retrieval

mcp = MCPServer("corpus", log_level="WARNING")


@mcp.tool()
def search(query: str) -> str:
    """Search UK financial-crime and payments regulation: the Money Laundering,
    Terrorist Financing and Transfer of Funds Regulations 2017, the Payment
    Services Regulations 2017 and the Electronic Money Regulations 2011 (plus
    any document added later). Use it for any question about what these rules
    require, allow or define. Returns the 5 best-matching passages, each
    starting with a citation in square brackets: [document, regulation number].
    Answer only from the returned text and cite it. If nothing returned
    answers the question, say the corpus does not cover it."""
    try:
        return retrieval.format_hits(retrieval.retrieve(query, k=5))
    except Exception as error:  # noqa: BLE001 - return the problem to the model, never crash the server
        return f"Search failed: {type(error).__name__}: {error}"


@mcp.tool()
def add_document(path: str) -> str:
    """Add a document to the search index. `path` is a file on this computer:
    .xml (legislation.gov.uk), .pdf, .txt or .md. It is split into chunks with
    citations, embedded with Gemini and stored. If the document is already
    indexed, unchanged chunks are skipped (no embedding cost) and only
    changed or new chunks are embedded. Returns how many chunks were new and
    how many were already there. Changes the index, so it needs approval."""
    file = Path(path).expanduser()
    if not file.is_file():
        return f"File not found: {path}"
    try:
        stats = ix.index_file(file)
    except Exception as error:  # noqa: BLE001
        return f"Could not add {file.name}: {type(error).__name__}: {error}"
    retrieval.reset()
    return (f"Indexed {file.name}: {stats['total']} chunks, {stats['embedded']} new or changed "
            f"(embedded), {stats['already_indexed']} already indexed (skipped).")


if __name__ == "__main__":
    mcp.run()  # stdio
