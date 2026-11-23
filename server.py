"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Loads index/ at startup and never re-embeds the corpus (only the query, or a
newly added document). Prints nothing to stdout (it carries the protocol);
logs to stderr. Docstrings become the tool descriptions the model reads.
"""

import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer

import index  #chunk_file,embed_and_store,add_file are here so only one pipeline

ROOT = Path(__file__).resolve().parent
TOP_K = 5

mcp = MCPServer("corpus", log_level="WARNING")

#Open the saved index once, at startup
collection = index.open_collection(index.CHOSEN_DESIGN)
print(f"corpus server: design '{index.CHOSEN_DESIGN}', {collection.count()} chunks loaded", file=sys.stderr)


def format_hit(rank: int, text: str, meta: dict, distance: float) -> str:
    part = f", part {meta['part']}/{meta['parts']}" if meta.get("parts", 0) > 1 else ""
    title = f" - {meta['title']}" if meta.get("title") else ""
    header = f"[{rank}] {meta['source']}, {meta['location']}{title}{part}  (distance {distance:.3f})"
    return f"{header}\n{text}"


@mcp.tool()
def search(query: str) -> str:
    """Search the indexed EU data-regulation corpus and return the best matching passages.

    The corpus is the operative text (articles, no recitals) of three EU regulations:
    the GDPR (Regulation 2016/679), the Data Act (Regulation 2023/2854) and the Data
    Governance Act (Regulation 2022/868), plus any document added with add_document.
    Use it for any question about obligations, rights, deadlines, fines or scope under
    these laws, and always before answering such a question.

    Pass a short, self-contained query in English (for example "deadline to notify a
    personal data breach"); search again with different words if the first results do
    not answer the question. Returns up to 5 passages, best first. Each starts with a
    citation line: [rank] source, article, title, and a distance (lower = closer match),
    followed by the passage text. Cite source and article for every claim. If none of the
    passages answers the question, the corpus does not cover it.
    """
    query = (query or "").strip()
    if not query:
        return "Empty query. Pass the question or key terms to search for."
    try:
        vector = index.embed_query(query)
    except Exception as error:  # noqa: BLE001 - tell the model plainly instead of crashing the server
        return f"Search failed (could not embed the query): {type(error).__name__}: {error}"
    result = collection.query(query_embeddings=[vector], n_results=TOP_K)
    docs, metas, dists = result["documents"][0], result["metadatas"][0], result["distances"][0]
    if not docs:
        return "No passages found."
    return "\n\n---\n\n".join(format_hit(i, d, m, x) for i, (d, m, x) in enumerate(zip(docs, metas, dists), 1))


@mcp.tool()
def add_document(path: str) -> str:
    """Add one document to the searchable corpus. This changes the index, so use it only
    when the user asks for a document to be added.

    `path` is a file on the server's machine, absolute or relative to the project folder
    (for example "corpus/free_flow.html"). Supported: EUR-Lex HTML (split into articles),
    other HTML, PDF and plain text. The file is split into passages, embedded and stored,
    and is searchable straight away.

    If the same document is already indexed and unchanged, nothing is added and the tool
    says so. If a document with the same name was indexed before but its text changed,
    the old passages are replaced. Returns a one-line summary of what happened.
    """
    file = Path(path)
    if not file.is_absolute():
        file = ROOT / file
    try:
        message = index.add_file(file)
    except Exception as error:  # noqa: BLE001
        return f"Could not add '{path}': {type(error).__name__}: {error}"
    return f"{message} Index now holds {collection.count()} passages."


if __name__ == "__main__":
    mcp.run()  # stdio
