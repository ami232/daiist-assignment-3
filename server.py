"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Load index/ at startup; never re-embed the corpus. Print nothing to stdout
(it carries the protocol); log to stderr. Docstrings become the tool
descriptions the model reads.
"""

from mcp.server.mcpserver import MCPServer
from retrieval import search as search_chunks
from ingest_document import index_document

mcp = MCPServer("corpus", log_level="WARNING")


@mcp.tool()
def search(query: str) -> str:
    """Search the warehouse safety guides for evidence relevant to a question.
    Returns the five highest-ranked passages with guide, printed page and chunk ID.
    """
    hits = search_chunks(query, k=5)

    passages = []
    for rank, hit in enumerate(hits, start=1):
        citation = f"[{hit['source']}, p. {hit['page']}]"
        passages.append(f"{rank}. {citation} ({hit['id']})\n{hit['text']}")

    return "\n\n".join(passages)


@mcp.tool()
def add_document(path: str) -> str:
    """Add a local text-based PDF to the warehouse guidance index.
    Returns its source ID and chunk count, or reports that it is already indexed.
    """
    return index_document(path)


if __name__ == "__main__":
    mcp.run()  # stdio
