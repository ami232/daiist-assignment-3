"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Loads index/ at startup and never re-embeds the corpus. Nothing is printed to
stdout (it carries the protocol); logging goes to stderr.
"""

import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer

import index as pipeline

mcp = MCPServer("corpus", log_level="WARNING")
INDEX = pipeline.Index()
print(f"corpus server: {len(INDEX.chunks)} chunks loaded", file=sys.stderr)

TOP_K = 5


@mcp.tool()
def search(query: str) -> str:
    """Search the aviation regulations corpus: US Federal Aviation Regulations (14 CFR) on small
    drones (Part 107, registration Part 48, Remote ID Part 89, model aircraft Part 101), airman medical
    standards (Part 67) and general operating and flight rules for aircraft (Part 91 subparts A-D).
    Use it for any question about what the rules require, allow or prohibit; never answer such
    questions from memory. Write the query as the regulatory topic with its key terms (for example
    'remote pilot operating over people' or 'minimum safe altitude over congested area').
    Returns up to 5 passages, best first, each as '[n] <document> — <section>' followed by the exact
    regulation text. Cite the section number of every claim you take from a passage. If nothing relevant
    comes back, the corpus does not cover the question."""
    return pipeline.format_results(INDEX.search(query, k=TOP_K))


@mcp.tool()
def add_document(path: str) -> str:
    """Add a document to the search index so that search can find it. Takes the local file path of an
    .xml (eCFR section format), .pdf, .txt, .md or .html document. The file is split into chunks with
    source and location, embedded and stored. Chunks already in the index are skipped, so adding the same
    file twice changes nothing. Returns how many chunks were added and how many were already indexed.
    This changes the shared index: use it only when the user asks to add a document."""
    p = Path(path).expanduser()
    if not p.is_file():
        return f"Error: file not found: {path}"
    try:
        chunks = pipeline.chunk_file(p)
        stats = pipeline.embed_and_store(chunks)
    except Exception as e:  # noqa: BLE001
        return f"Error while indexing {p.name}: {type(e).__name__}: {e}"
    INDEX.reload()
    if stats["added"] == 0:
        return f"{p.name} was already indexed: {stats['already_indexed']} chunks found, 0 added."
    return (
        f"Indexed {p.name} as '{pipeline.source_for_file(p)}': {stats['added']} chunks added, "
        f"{stats['already_indexed']} already indexed ({stats['total']} in file)."
    )


if __name__ == "__main__":
    mcp.run()  # stdio
