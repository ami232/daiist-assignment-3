"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Loads the committed index/ at startup and never re-embeds the corpus. Prints
nothing to stdout (it carries the protocol); logs go to stderr.
"""

from mcp.server.mcpserver import MCPServer

import index
import rag

mcp = MCPServer("corpus", log_level="WARNING")


@mcp.tool()
def search(query: str) -> str:
    """Search Spanish takeover-bid (OPA) rules used by a merger arbitrage desk.

    The corpus holds: Real Decreto 1066/2007 on takeover bids (OPAs), the CNMV's
    questions and answers on OPAs, Ley 15/2007 on competition (merger control,
    phases and deadlines), and Ley 19/2003 and Real Decreto 571/2023 on foreign
    investment screening. Texts are in Spanish, so
    query in Spanish with the legal terms (e.g. "plazo de aceptación", "venta
    forzosa", "precio equitativo", "segunda fase").

    Use it before answering any question about OPA conditions, prices,
    deadlines, squeeze-out, competing offers, merger control or foreign
    investment authorisation. Call it again with different wording if the
    first results do not answer the question.

    Returns the top 5 passages, best first. Each starts with the exact citation
    to use, e.g. [RD1066-2007, Artículo 23], followed by the source and text.
    """
    rag.log(f"search: {query!r}")
    try:
        return rag.format_results(rag.search(query))
    except rag.QuotaExhausted as error:
        return f"Search unavailable: {error}"


@mcp.tool()
def add_document(path: str) -> str:
    """Add one document to the corpus so that search can find it.

    Takes the path of a local file (.pdf, .html, .xml from the BOE open-data
    API, .txt or .md), extracts and chunks it with the same pipeline as the
    rest of the corpus, embeds the chunks with Gemini and stores them in the
    index. If the identical file is already indexed nothing is embedded; if a
    document with the same name but different content is indexed, its old
    chunks are replaced by the new version.

    Returns what happened: the document id to cite, the number of chunks and
    how many were embedded now. Only use it when the user explicitly asks to
    add a document.
    """
    rag.log(f"add_document: {path!r}")
    try:
        result = index.add_document(path)
    except (FileNotFoundError, ValueError) as error:
        return f"Not added: {error}"
    except rag.QuotaExhausted as error:
        return f"Not added: {error}"
    if result["status"] == "already_indexed":
        return result["message"]
    verb = "Replaced with a new version" if result["status"] == "new_version" else "Added"
    return (
        f"{verb}: {result['title']} as {result['doc_id']}. {result['chunks']} chunks, "
        f"{result['embedded_now']} embedded now, {result['replaced_chunks']} old chunks removed. "
        f"Cite it as [{result['doc_id']}, <location>]."
    )


if __name__ == "__main__":
    mcp.run()  # stdio
