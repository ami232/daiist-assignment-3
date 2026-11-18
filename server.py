"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

Loads the committed index at startup and never re-embeds the corpus. Only MCP
messages go to stdout; logs go to stderr.
"""

import logging
import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer

import config as C
from index import add_file
from retrieval import Retriever, format_results

logging.basicConfig(stream=sys.stderr, level=logging.WARNING)
mcp = MCPServer("corpus", log_level="WARNING")
retriever = Retriever(C.ACTIVE_CHUNKING, C.ACTIVE_METHOD)
ALLOWED_DIRS = [C.ROOT]                  # add_document only reads files inside the repo


@mcp.tool()
def search(query: str) -> str:
    """Search FAA pilot-training handbooks (Pilot's Handbook of Aeronautical
    Knowledge, 2023: weather theory, aviation weather services, airspace,
    aeromedical factors, plus any document added later).

    Use it for every factual aviation question before answering. Pass a short,
    specific query in the handbook's vocabulary (e.g. "Class C airspace
    dimensions", "hypoxia symptoms"); for a question with two parts, search
    once per part.

    Returns up to 5 passages, each headed by its citation in the form
    [doc_id p.PAGE], then the document title, section and pages. Cite passages
    exactly with that citation. If nothing relevant comes back, the corpus does
    not cover the question.
    """
    return format_results(retriever.search(query, C.SEARCH_K))


@mcp.tool()
def add_document(path: str) -> str:
    """Add one document (.pdf, .txt, .md or .html) to the search index.

    `path` is a file path inside this project, e.g. corpus/extra/phak-ch14.pdf.
    The file is extracted, chunked and embedded with the same pipeline as the
    corpus, so it becomes searchable immediately. If the same file is already
    indexed nothing is embedded; if a file with the same name but different
    contents is indexed, it replaces the old version.

    Only use it when the user explicitly asks to add a document. Returns a
    one-line status: added / updated / already indexed / error.
    """
    p = Path(path).expanduser()
    p = (C.ROOT / p if not p.is_absolute() else p).resolve()
    if not any(p.is_relative_to(d) for d in ALLOWED_DIRS):
        return f"Error: {path} is outside the project folder; only files inside it can be added."
    status = add_file(p)
    retriever.refresh()
    return status


if __name__ == "__main__":
    mcp.run()  # stdio
