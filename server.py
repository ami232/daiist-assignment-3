"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Loads index/ lazily on the first search; never re-embeds the corpus (only the
query is embedded, and cached). Prints nothing to stdout: it carries the
protocol. Docstrings below are the tool descriptions the model reads.
"""

import json
import sys

from mcp.server.mcpserver import MCPServer

import retrieval
from index import QuotaExhausted, add_document as index_add_document

mcp = MCPServer("corpus", log_level="WARNING")


@mcp.tool()
def search(query: str, k: int = 5) -> str:
    """Search U.S. investment adviser law: the Investment Advisers Act of 1940
    (15 U.S.C. 80b), the SEC rules under it (17 CFR Part 275: registration,
    Form ADV and Form CRS delivery, books and records, codes of ethics,
    performance fees and qualified clients, marketing/advertising, custody,
    pay-to-play, compliance programs) and the SEC's 2019 interpretation of an
    adviser's fiduciary duty (duty of care, best execution, duty of loyalty,
    conflicts disclosure). Plus any document added with add_document.

    Use it for every factual question about these rules, before answering.
    Write the query as a short statement of what you are looking for, using
    the legal terms if you know them (e.g. "custody rule surprise examination
    independent accountant"). Search again with other words if the passages
    do not answer the question; ask separately about each part of a
    two-part question.

    Returns up to k passages (default 5, max 10), each headed
    `=== [ID] document | location ===`. Cite a passage by its [ID].
    """
    k = max(1, min(int(k), 10))
    try:
        return retrieval.format_results(retrieval.search(query, k=k))
    except QuotaExhausted:
        return "Search is unavailable: the embedding quota for today is used up. Try again later."


@mcp.tool()
def add_document(path: str) -> str:
    """Add a document to the searchable corpus. Use only when the user asks to
    add or index a specific file. `path` is a local file path (.html, .htm,
    .xml, .pdf, .txt or .md), absolute or relative to the project folder.

    The file is extracted, chunked and embedded with the same pipeline as the
    corpus, then becomes searchable immediately. If the identical file is
    already indexed nothing changes; if a different version of the same
    document (same file name) was added before, it is replaced. Returns a JSON
    report: status (added, replaced, already_indexed or error), document id,
    words and number of chunks.
    """
    try:
        report = index_add_document(path)
    except QuotaExhausted:
        report = {"status": "error", "message": "Embedding quota used up for today; nothing was added."}
    except Exception as error:  # report the failure to the agent instead of crashing the server
        print(f"add_document failed: {error!r}", file=sys.stderr)
        report = {"status": "error", "message": f"{type(error).__name__}: {error}"}
    return json.dumps(report)


if __name__ == "__main__":
    mcp.run()  # stdio
