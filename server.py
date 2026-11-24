"""
MCP server with two tools over the Guía trámites index. By hand: `uv run server.py`.

- search(query): returns the 5 closest chunks, each with its citation.
- add_document(path): runs a ficha through index.py's pipeline and stores it.

The server only opens index/ (it never re-embeds the corpus). stdout carries
the MCP protocol, so anything we want to log goes to stderr.
"""

import sys

from mcp.server.mcpserver import MCPServer

import index

mcp = MCPServer("corpus", log_level="WARNING")


def format_hit(hit: dict) -> str:
    """One result as the model will read it: citation first, then the text."""
    return (f"[{hit['source']} · {hit['location']}]\n"
            f"{hit['text']}\n"
            f"Sede: {hit['sede_url']}")


@mcp.tool()
def search(query: str) -> str:
    """Search the official procedure sheets (fichas de trámites) of the Ayuntamiento de
    Santa María de Guía (Gran Canaria): what each trámite is, who can apply, how to identify,
    required documents (documentación), deadlines (plazo de presentación / resolución),
    silencio administrativo, notifications, legal basis (normativa) and FAQs.

    Use it for any question about a municipal procedure in Guía. Write the query in Spanish.
    Returns the 5 most relevant passages; each one starts with its citation
    [trámite-slug · section] and ends with the link to the trámite in the sede electrónica.
    If none of the passages answers the question, the corpus does not cover it.
    """
    hits = index.search(query, k=5)
    if not hits:
        return "No results: the index is empty."
    return "\n\n---\n\n".join(format_hit(hit) for hit in hits)


@mcp.tool()
def add_document(path: str) -> str:
    """Add one trámite ficha (a JSON file with the same fields as data/fichas/*.json) to the
    index, using the same chunking and Gemini embeddings as the rest of the corpus.

    If the trámite is already indexed: it is skipped when the file has not changed, and
    replaced (old chunks deleted, new ones added) when it has. Returns what happened.
    """
    result = index.add_file(path)
    print(result, file=sys.stderr)
    return result


if __name__ == "__main__":
    mcp.run()  # stdio
