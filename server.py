"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Load index/ at startup; never re-embed the corpus. Print nothing to stdout
(it carries the protocol); log to stderr. Docstrings become the tool
descriptions the model reads.
"""

from __future__ import annotations

import sys

from mcp.server.mcpserver import MCPServer

from index import add_file
from retrieval import DEFAULT_DESIGN, format_hits, search_chunks

mcp = MCPServer("corpus", log_level="WARNING")


@mcp.tool()
def search(query: str) -> str:
    """Search FDA drug-label passages for a patient or clinician question.

    Use this tool to retrieve evidence for dosing, warnings, interactions,
    contraindications, side effects, and off-label uncertainty. It returns
    up to five passages, each with a source filename and section/location.
    """
    if not query.strip():
        return "No search query was provided."
    try:
        hits = search_chunks(query, k=5, design=DEFAULT_DESIGN)
        return format_hits(hits)
    except Exception as error:
        print(f"search failed: {type(error).__name__}: {error}", file=sys.stderr)
        return "Search failed. No evidence was retrieved."


@mcp.tool()
def add_document(path: str) -> str:
    """Add a .txt, .md, or .pdf document to the corpus index.

    This tool is for explicit document ingestion only. It chunks and embeds the
    file only for the default section design. If the exact file content and
    filename were already indexed, it reports unchanged; if the filename is
    reused with new content, both the old and new content remain available.
    """
    try:
        result = add_file(path, designs=(DEFAULT_DESIGN,))
        counts = result[DEFAULT_DESIGN]
        return (
            f"Document {path} indexed with the {DEFAULT_DESIGN} design: "
            f"{counts['stored']} new chunks stored, {counts['skipped']} unchanged chunks skipped."
        )
    except Exception as error:
        print(f"add_document failed: {type(error).__name__}: {error}", file=sys.stderr)
        return f"Could not add document: {type(error).__name__}: {error}"


if __name__ == "__main__":
    mcp.run()  # stdio
