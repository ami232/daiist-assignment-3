"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Loads index/ at startup; never re-embeds the corpus. Prints nothing to stdout
(it carries the protocol); logs go to stderr. Tool descriptions are what the model reads.
"""

from mcp.server.mcpserver import MCPServer

import index as indexer
import rag

# >>> EDIT: describe YOUR corpus. The model decides when to call the tool from this text. <<<
CORPUS_DESCRIPTION = "Spanish housing and rental law: the Ley de Arrendamientos Urbanos (LAU), the 2023 Ley por el derecho a la vivienda and the Ley de Propiedad Horizontal"

SEARCH_DESCRIPTION = (
    f"Search the document collection: {CORPUS_DESCRIPTION}. "
    "Use it for every factual question about these documents, and call it again with different "
    "wording, or once per sub-question, when a question needs more than one passage. "
    f"Takes a natural-language `query`. Returns the {rag.CHOSEN['k']} best-matching passages, each "
    "under a citation header `[source | location]` followed by the passage text. "
    "If no passage answers the question, the collection does not cover it."
)

ADD_DESCRIPTION = (
    "Add one new document to the collection so that `search` can find it. Takes the file `path` "
    "(.pdf, .html, .txt or .md). The file is extracted, chunked, embedded and stored. "
    "If identical content is already indexed nothing is changed; if a file with the same name but "
    "different content is indexed, its old passages are replaced. Returns a short report of what "
    "was added, replaced or skipped. Only use this when the user asks to add a document."
)

mcp = MCPServer("corpus", log_level="WARNING")


@mcp.tool(description=SEARCH_DESCRIPTION)
def search(query: str) -> str:
    query = (query or "").strip()
    if not query:
        return "Empty query. Pass the question or key terms to look for."
    hits = rag.search(query)
    return rag.format_hits(query, hits)


@mcp.tool(description=ADD_DESCRIPTION)
def add_document(path: str) -> str:
    try:
        return indexer.index_file(path, designs=(rag.CHOSEN["design"],))
    except ValueError as error:  # bad path / type / size: tell the model, don't crash
        return f"Not added: {error}"
    except rag.QuotaExhausted as error:
        return f"Not added: {error}"


if __name__ == "__main__":
    mcp.run()  # stdio
