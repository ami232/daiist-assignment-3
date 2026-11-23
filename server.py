"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

Loads the saved index; never re-embeds the corpus. Nothing is printed to stdout
(it carries the protocol). Docstrings become the tool descriptions the model reads.
"""

from pathlib import Path

from mcp.server.mcpserver import MCPServer

from index import chunk_file, embed_and_store, get_collection
from retrieve import DEFAULT_DESIGN, retrieve

mcp = MCPServer("corpus", log_level="WARNING")


@mcp.tool()
def search(query: str) -> str:
    """Search the official EU product information (summary of product characteristics, SmPC) of
    oral anticoagulants: apixaban (Eliquis), rivaroxaban (Xarelto), dabigatran (Pradaxa) and any
    document added later. Use it for questions about indications, dosing, contraindications,
    warnings, drug interactions, pregnancy, adverse effects or overdose. Returns the 5 closest
    passages, each with its source document, its location (SmPC variant and pages) and a distance
    (lower = more similar), so the answer can be cited. If none of the passages answers the
    question, say you do not know; never answer from memory."""
    hits = retrieve(query, k=5)
    return "\n\n".join(
        f"[{i}] {h['source']} | {h['location']} | distance {h['distance']:.3f}\n{h['text']}"
        for i, h in enumerate(hits, 1)
    )


@mcp.tool()
def add_document(path: str) -> str:
    """Add a PDF of EU product information (SmPC) to the index so that `search` can find it.
    Takes the file path. Splits the SmPC into chunks, embeds them (this uses embedding quota) and
    stores them. If a document with the same file name is already indexed, nothing is added.
    Returns how many chunks were added."""
    file = Path(path).expanduser()
    if not file.is_file() or file.suffix.lower() != ".pdf":
        return f"Not added: {path} is not an existing PDF file."
    if get_collection(DEFAULT_DESIGN).get(where={"source": file.stem}, limit=1)["ids"]:
        return f"Already indexed: {file.stem}. Nothing was added."
    chunks = chunk_file(file, DEFAULT_DESIGN)
    added = embed_and_store(chunks, DEFAULT_DESIGN)
    return f"Added {file.stem}: {len(chunks)} chunks, {added} embedded."


if __name__ == "__main__":
    mcp.run()  # stdio