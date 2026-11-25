"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Loads index/ at startup; never re-embeds the corpus. Nothing is printed to
stdout (it carries the protocol); logs go to stderr.
"""

import contextlib
import sys

from mcp.server.mcpserver import MCPServer

import index as pipeline
import retrieval

mcp = MCPServer("corpus", log_level="WARNING")
TOP_K = 5


@mcp.tool()
def search(query: str) -> str:
    """Search the data protection corpus: the GDPR (Regulation 2016/679, recitals and
    articles) and two EDPB guidelines (05/2020 on consent, 9/2022 on personal data
    breach notification). Use it before answering any question about EU data
    protection law. Returns the 5 most similar passages, each with a citation
    [source, location] (article, recital, section or page) and its text. If none of
    the passages answers the question, the corpus does not cover it."""
    results = retrieval.search(query, k=TOP_K)
    if not results:
        return "No results: the index is empty. Run `uv run python main.py index` first."
    parts = []
    for rank, (score, chunk) in enumerate(results, 1):
        parts.append(
            f"[{rank}] Citation: [{chunk['source']}, {chunk['location']}] (similarity {score:.2f})\n{chunk['text']}"
        )
    return "\n\n".join(parts)


@mcp.tool()
def add_document(path: str) -> str:
    """Add one new document to the search index. Give the file path of a PDF, HTML, TXT or
    MD file. The file is chunked, embedded and stored, and its passages become
    searchable with the document name (file name without extension) as source.
    If a document with the same name is already indexed, nothing is changed and
    the tool says so. Returns a short message with the result."""
    # the pipeline may print; stdout must stay clean for the MCP protocol
    with contextlib.redirect_stdout(sys.stderr):
        message = pipeline.add_to_index(path)
    retrieval.reload()
    return message


if __name__ == "__main__":
    mcp.run()  # stdio
