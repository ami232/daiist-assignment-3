"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Loads the committed index/ at startup and never re-embeds the corpus (only
new query vectors are computed, and those are cached). Prints nothing to
stdout; logs go to stderr.

Env vars (used by evaluate.py): CORPUS_ONLY=1 hides documents added later.
"""

import json
import logging
import os
import sys

from mcp.server.mcpserver import MCPServer

import index

logging.basicConfig(stream=sys.stderr, level=logging.WARNING)
mcp = MCPServer("corpus", log_level="WARNING")
CORPUS_ONLY = os.environ.get("CORPUS_ONLY") == "1"
SOURCES = ", ".join(index.DOCUMENTS)


@mcp.tool()
def search(query: str) -> str:
    """Search EU food-supplement law (EUR-Lex): Directive 2002/46/EC (food supplements:
    allowed vitamins/minerals and their forms, labelling), Reg 1924/2006 (nutrition and
    health claims), Reg 432/2012 (the list of permitted health claims and their conditions
    of use), Reg 1925/2006 (adding vitamins, minerals and other substances to foods),
    Reg 2015/2283 (novel foods) and Reg 1169/2011 (food information / labelling),
    plus any document added later.

    Use it for every question about what a supplement may contain, say or must show
    on its label in the EU. Write the query in plain legal English with the key terms
    (e.g. "vitamin D health claim immune system conditions of use").

    Returns the 5 best passages. Each starts with its citation in square brackets,
    e.g. [Reg 1924/2006, Article 10], followed by the passage text. Cite exactly
    these labels. If no passage answers the question, the corpus does not cover it.
    """
    results = index.search(query, k=index.load_config().get("k", 5), corpus_only=CORPUS_ONLY)
    return index.format_results(results)


@mcp.tool()
def add_document(path: str) -> str:
    """Add one document (EUR-Lex HTML, PDF or text file, given by its file path on this
    machine) to the searchable corpus: it is extracted, chunked by article/annex, embedded
    with Gemini and stored in the index, so search can find it from then on.

    If the identical file is already indexed nothing is embedded and the result says
    'already_indexed'. If a document with the same name (e.g. 'Reg 2022/860') but different
    content is indexed, the old version is replaced ('replaced'). Returns a JSON summary:
    status, source name, number of chunks and number newly embedded.
    """
    try:
        return json.dumps(index.index_file(path))
    except Exception as error:  # noqa: BLE001 - report to the model, don't crash the server
        return json.dumps({"status": "error", "error": f"{type(error).__name__}: {error}"})


if __name__ == "__main__":
    mcp.run()  # stdio
