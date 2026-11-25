"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Loads index/ at startup and never re-embeds the corpus; only queries are
embedded (and cached). Nothing goes to stdout except MCP messages.
"""

import index
from mcp.server.mcpserver import MCPServer

store = index.Store()
mcp = MCPServer("corpus", log_level="WARNING")

documents = ", ".join(sorted(index.read_docs())) or "none yet"

SEARCH_DESCRIPTION = (
    f"Search {index.CORPUS_TOPIC} (documents: {documents}). "
    "Use it before answering any question these documents might cover, and again with different wording, "
    "or with `source` set to one file name, if the first passages do not contain the answer. "
    f"Returns the {index.TOP_K} most relevant passages, each headed by its source file and location "
    "(section or article and page). Cite every claim as [source, location], copied exactly from those headers. "
    "If no passage states the answer, the documents do not answer the question."
)


def format_results(results: list[dict]) -> str:
    blocks = [
        f"--- [{i}] source: {r['source']} | location: {r['location']} | score: {r['score']:.3f}\n{r['text']}"
        for i, r in enumerate(results, 1)
    ]
    return "\n\n".join(blocks)


@mcp.tool(description=SEARCH_DESCRIPTION)
def search(query: str, source: str | None = None) -> str:
    query = query.strip()
    if not query:
        return "Empty query: say what to search for."
    try:
        results = store.search(query, source=source)
    except index.QuotaExhausted:
        return "Search is unavailable: the daily embedding quota is used up. Tell the user to try again later."
    if not results:
        where = f" in {source}" if source else ""
        return f"No passages found{where}. The index may be empty or the source name wrong."
    return format_results(results)


@mcp.tool()
def add_document(path: str) -> str:
    """Add one document (PDF, TXT, MD or HTML) at a file path to the searchable index.

    Extracts, cleans and chunks it with the same pipeline as the corpus, embeds the new
    chunks and stores them, and copies the file into corpus/. If the identical file is
    already indexed nothing happens; a file with the same name but new content replaces
    the old version. Only use it when the user explicitly asks to add a file. Returns a
    one-line report of what was added, replaced or skipped.
    """
    result = index.add_document(path)
    store.reload()
    return result


if __name__ == "__main__":
    mcp.run()  # stdio
