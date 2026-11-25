"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Loads the committed index/ (Chroma + saved vectors); never re-embeds the
corpus, only the query. Logs go to stderr: stdout carries the MCP protocol.
"""

import os
import sys

os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")   # keep chromadb quiet

from mcp.server.mcpserver import MCPServer

import index
import retrieval

mcp = MCPServer("corpus", log_level="WARNING")


@mcp.tool()
def search(query: str) -> str:
    """Search EU law for startup compliance: the AI Act (Regulation (EU) 2024/1689),
    the GDPR (Regulation (EU) 2016/679) and the Digital Services Act (Regulation
    (EU) 2022/2065), including their recitals and the AI Act annexes, plus any
    document added later with add_document.

    Use it for any question about whether an AI system is prohibited or high-risk,
    the obligations of providers and deployers, transparency duties, data-protection
    duties (lawful basis, DPIA, automated decisions), online-platform duties, fines
    and deadlines. Phrase the query in the regulation's own terms (e.g. "AI systems
    used for recruitment or selection of natural persons" rather than "CV tool");
    search again with a different phrasing if the first results don't cover the
    question.

    Returns the 5 most relevant passages, each headed by "CITE AS: [<law>,
    <article/recital/annex>]" plus its title and pages. Cite passages exactly in
    that bracket form. If none of them answers the question, the corpus does not
    cover it.
    """
    try:
        return retrieval.format_results(retrieval.search(query))
    except index.QuotaExhausted:
        return "Search unavailable: the daily embedding quota is used up. Try again after the reset."


@mcp.tool()
def add_document(path: str) -> str:
    """Add a document (PDF, .txt or .md file path on this machine) to the search
    index: it is extracted, chunked by article/recital where it has that
    structure (fixed-size windows otherwise), embedded and stored, and becomes
    searchable immediately.

    If the same file content is already indexed nothing is done; if a file with
    the same name but different content is indexed, the old version's chunks are
    replaced. Returns what happened and how many chunks were added or removed.
    """
    try:
        result = index.add_document(path)
    except (FileNotFoundError, ValueError) as e:
        return f"Not added: {e}"
    except index.QuotaExhausted:
        return "Not added: the daily embedding quota is used up. Nothing was stored; try again after the reset."
    retrieval.refresh()
    if result["status"] == "already_indexed":
        return f"{result['file']} is already indexed with the same content; nothing was added."
    verb = "Replaced the previous version of" if result["status"] == "replaced" else "Added"
    extra = f" ({result['chunks_removed']} old chunks removed)" if result["status"] == "replaced" else ""
    return f"{verb} {result['file']} as source '{result['source']}': {result['chunks_added']} chunks indexed{extra}."


if __name__ == "__main__":
    print("corpus MCP server starting (stdio)", file=sys.stderr)
    mcp.run()  # stdio
