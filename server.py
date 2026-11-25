"""
Assignment 3: MCP server `corpus`. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline (imported, not
  rewritten), embeds the new chunks and stores them.

index/ is loaded on the first search; the corpus is never re-embedded here,
only the query. Nothing is printed to stdout (it carries the protocol); logs
go to stderr.
"""

import json
import os

from mcp.server.mcpserver import MCPServer

import index as pipeline
from retrieval import DEFAULT_MODE, Store, format_results

mcp = MCPServer("corpus", log_level="WARNING")
MODE = os.environ.get("SEARCH_MODE", DEFAULT_MODE)
_store: Store | None = None


def store() -> Store:
    global _store
    if _store is None:
        _store = Store()
    return _store


@mcp.tool()
def search(query: str, source: str = "", k: int = 5) -> str:
    """Search three EU data-protection laws: the GDPR (Regulation (EU) 2016/679, source
    "GDPR"), the Law Enforcement Directive (Directive (EU) 2016/680, source "LED") and the
    ePrivacy Directive (Directive 2002/58/EC as amended in 2009, source "ePrivacy"), plus
    any document added later.

    Use it for every question about personal data, privacy, cookies, electronic
    communications, marketing e-mails, data breaches, fines, data subjects' rights,
    controllers, processors, DPOs or international transfers. Write the query in plain
    words describing the rule you need (e.g. "deadline to notify a personal data breach
    to the supervisory authority"); search again with other words if the passages do not
    answer the question.

    Optional: `source` restricts the search to one or more documents (e.g. "GDPR" or
    "GDPR,ePrivacy"); `k` is the number of passages (1-10, default 5).

    Returns numbered passages, each headed by `source | location | title`, where location
    is "Article N" or "Recital N". Cite them as [source, location]. "No passages found."
    means nothing matched.
    """
    hits = store().search(query, k=max(1, min(int(k), 10)), mode=MODE, source=source or None)
    return format_results(hits)


@mcp.tool()
def add_document(path: str) -> str:
    """Add one local file (.html, .pdf, .txt or .md) to the searchable corpus.

    `path` is a file path, absolute or relative to the project folder. The file is
    extracted, chunked (EU acts by article and recital, other files by heading or page),
    embedded with Gemini and stored in the index; its source name is the file name
    without extension. If the same file is already indexed nothing is re-embedded; if its
    content changed, only the changed chunks are replaced.

    Only call this when the user explicitly asks to add a document.

    Returns a JSON summary: status ("added", "updated", "already indexed" or "error"),
    source, number of chunks and number of chunks embedded now.
    """
    try:
        result = pipeline.add_document(path)
    except Exception as error:  # noqa: BLE001 - report to the model instead of crashing the server
        return json.dumps({"status": "error", "error": f"{type(error).__name__}: {error}"})
    if _store is not None:
        _store.reload()
    return json.dumps(result)


if __name__ == "__main__":
    mcp.run()  # stdio
