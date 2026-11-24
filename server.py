"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

The index in index/ is loaded at startup and never rebuilt here: search only
embeds the question. Nothing may be printed to stdout (it carries the MCP
protocol); everything is logged to stderr.
"""

import rag
from mcp.server.mcpserver import MCPServer

TOP_K = 5

mcp = MCPServer("corpus", log_level="WARNING")

try:
    rag.load_store()  # read the committed chunks and vectors once, at startup
except Exception as error:  # noqa: BLE001 - report it on the first call instead of failing to start
    rag.log(f"index not loaded at startup: {error}")


@mcp.tool()
def search(query: str) -> str:
    """Search the EU AI Act corpus and return the most relevant passages with citations.

    The corpus is: Regulation (EU) 2024/1689 (the AI Act), consolidated version of
    27 July 2026 (articles and annexes, including the changes made by Regulation (EU)
    2026/1744); the Commission Guidelines on prohibited AI practices (Article 5); the
    Commission Guidelines on the definition of an AI system (Article 3(1)); and any
    document added later with add_document. Use it for every question about what these
    texts say; do not answer from memory.

    Returns up to 5 passages ranked by similarity. Each starts with
    'cite as [source | location]': copy that exact string as the citation for any claim
    taken from the passage. A passage marked 'amended' contains text changed by
    Regulation (EU) 2026/1744. The ranking always returns something, even for a question
    the corpus does not cover, so judge from the text whether a passage really answers it.
    Query: the question or key terms, in English.
    """
    try:
        return rag.format_results(rag.search(query, k=TOP_K))
    except rag.QuotaExhausted:
        return "Search unavailable: the daily embedding quota is used up. Try again after 09:00 (Spain)."


@mcp.tool()
def add_document(path: str) -> str:
    """Add a document (PDF, .txt or .md) to the searchable corpus and report what happened.

    path: file path on this computer, absolute or relative to the project folder. The file
    goes through the same pipeline as the original corpus (extract, clean, chunk, embed,
    store). If the same file (same content) is already indexed, nothing is embedded and
    the result says 'already_indexed'. If a file with the same name but different content
    is added, its old chunks are replaced. Embedding uses the free-tier daily quota, so only
    call this when the user asked to add a document. Returns the status, the source name
    to cite, the number of chunks and the number of new embeddings.
    """
    import index  # imported here: it needs pypdf, which search never uses

    try:
        result = index.add_document(path)
    except rag.QuotaExhausted as error:
        return f"Not added: {error}"
    except ValueError as error:
        return f"Not added: {error}"
    return (
        f"{result['status']}: source '{result['source']}', {result['chunks']} chunks, "
        f"{result['new_embeddings']} new embeddings."
    )


if __name__ == "__main__":
    mcp.run()  # stdio
