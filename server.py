"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

Loads the committed index/ at startup and never re-embeds the corpus; only
queries (and documents passed to add_document) are embedded. Logs go to
stderr, because stdout carries the MCP protocol.
"""

import contextlib
import logging
import sys

from mcp.server.mcpserver import MCPServer

import index as ix
import retrieval

logging.basicConfig(stream=sys.stderr, level=logging.WARNING)
mcp = MCPServer("corpus", log_level="WARNING")

# Load the served store once at startup (no embedding happens here).
with contextlib.redirect_stdout(sys.stderr):
    try:
        retrieval.store(ix.served_design())
    except Exception as e:  # report on the first call instead of crashing the editor
        logging.warning("index not loaded: %s", e)


@mcp.tool()
def search(query: str) -> str:
    """Search the EU merger control corpus: the EU Merger Regulation (Regulation 139/2004),
    the Commission Consolidated Jurisdictional Notice, and the horizontal and non-horizontal
    merger assessment guidelines, plus any document added later.

    Use it for any question about EU merger control: what counts as a concentration,
    control and joint ventures, turnover thresholds and how turnover is calculated,
    notification, deadlines and procedure, referrals, and how the Commission assesses
    competitive effects. Write the query in plain English with the key legal terms.
    Call it again with a different query if the first results do not cover the question.

    Returns the 5 most relevant passages, each with its source document id and location
    (article, recital or paragraph) and a ready-made citation such as [EUMR, Article 1].
    """
    with contextlib.redirect_stdout(sys.stderr):
        return retrieval.format_results(retrieval.search(query, k=5))


@mcp.tool()
def add_document(path: str) -> str:
    """Add one document (.html, .pdf, .txt or .md file on this machine) to the corpus index.

    The file goes through the same pipeline as the corpus: text extraction, cleaning,
    chunking by article/paragraph, Gemini embedding, storage in index/. The document id
    is the file name in capitals (e.g. simplified_notice.html -> SIMPLIFIED_NOTICE).
    If the same file is already indexed, nothing is embedded or changed. If a file with
    the same id but different content is added, it replaces the old version.

    Returns the status (added, replaced or already_indexed), the document id and the
    number of chunks stored.
    """
    with contextlib.redirect_stdout(sys.stderr):
        try:
            res = ix.add_document(path)
        except Exception as e:
            return f"error: {type(e).__name__}: {e}"
        retrieval.store.cache_clear()
        return f"status: {res['status']} | source: {res['source']} | chunks: {res['chunks']}"


if __name__ == "__main__":
    mcp.run()  # stdio
