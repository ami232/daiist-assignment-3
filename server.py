"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Load index/ at startup; never re-embed the corpus. Print nothing to stdout
(it carries the protocol); log to stderr. Docstrings become the tool
descriptions the model reads.
"""

import os
from pathlib import Path

from mcp.server.mcpserver import MCPServer

import index
import retrieval

# Tests point this at a temporary index; normally it is index/.
INDEX_DIR = Path(os.environ.get("RAG_INDEX_DIR", index.INDEX_DIR))

mcp = MCPServer("corpus", log_level="WARNING")


@mcp.tool()
def search(query: str) -> str:
    """Search Spanish housing law for passages relevant to a question about renting.

    The collection holds the consolidated BOE texts of the Ley de Arrendamientos
    Urbanos (LAU), the Ley 12/2023 por el derecho a la vivienda (LeyVivienda) and
    the Ley de Propiedad Horizontal (LPH). Use it for every question about rental
    contracts, deposits (fianza), rent, duration, repairs or the community of owners;
    search again with other words if the passages do not answer the question.
    Returns the 5 closest passages, each under its citation [source, location];
    copy that citation after every claim you take from it.
    """
    return retrieval.format_hits(retrieval.search(query, path_index=INDEX_DIR))


@mcp.tool()
def add_document(path: str) -> str:
    """Add a document (a PDF, TXT or MD file on this computer) to the collection.

    Extracts, chunks and embeds the file with the same pipeline as the corpus,
    then makes it searchable. The source name in citations is the file name
    without extension. A file already indexed unchanged is skipped; a changed
    file with the same name replaces its old version. Returns what happened.
    """
    try:
        result = index.index_file(path, path_index=INDEX_DIR)
    except (FileNotFoundError, ValueError, index.QuotaExhausted) as error:
        return f"Could not add {path}: {error}"
    if result["status"] == "already indexed":
        return f"'{result['source']}' is already indexed and unchanged; nothing was added."
    return f"{result['status'].capitalize()} '{result['source']}': {result['chunks']} chunks are now searchable."


if __name__ == "__main__":
    mcp.run()  # stdio
