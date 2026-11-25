"""
Assignment 3: MCP server.  `uv run server.py` or started by editors / agent.py.

- search(query): returns chunks with citations.
- add_document(path): indexes a new PDF through the same pipeline.

Loads index/ at startup; never re-embeds the corpus.
Only MCP messages go to stdout; everything else to stderr.
"""

import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer

ROOT = Path(__file__).resolve().parent

# Lazy-import index functions so the server starts quickly even if the
# embedding model is slow to initialise.
_index = None


def _load_index():
    global _index
    if _index is None:
        from index import (
            search_index,
            chunk_file,
            embed_and_store,
            file_content_hash,
            load_db,
        )

        _index = {
            "search_index": search_index,
            "chunk_file": chunk_file,
            "embed_and_store": embed_and_store,
            "file_content_hash": file_content_hash,
            "load_db": load_db,
        }
    return _index


mcp = MCPServer("corpus", log_level="WARNING")


@mcp.tool()
def search(query: str) -> str:
    """Search a corpus of US, EU and UK music-copyright law for passages that
    answer questions about copyright registration, royalties, sound recordings,
    musical compositions, performance rights, mechanical rights and related
    legal rules.  Returns up to 5 text chunks, each with a stable chunk_id,
    source document, page/section location and cosine-similarity score.
    Use this tool whenever the user asks about which right applies, who
    collects it, or what the law says."""
    idx = _load_index()
    results = idx["search_index"](query, k=5)
    if not results:
        return "No relevant passages found in the corpus."
    parts = []
    for r in results:
        parts.append(
            f"[chunk_id: {r['chunk_id']}]\n"
            f"[source: {r['source']}, location: {r['location']}, "
            f"score: {r['score']:.3f}]\n"
            f"{r['text']}"
        )
    return "\n\n---\n\n".join(parts)


@mcp.tool()
def add_document(path: str) -> str:
    """Add a new PDF document to the music-copyright corpus.  Takes a file
    path, extracts text, chunks it by structure, embeds with Gemini and stores
    in the index.  If the exact same content is already indexed (content-hash
    match) it is skipped.  If the same filename exists with different content
    the old chunks are replaced."""
    idx = _load_index()
    file_path = Path(path)
    if not file_path.is_absolute():
        file_path = ROOT / file_path
    if not file_path.exists():
        return f"Error: file not found: {file_path}"
    if file_path.suffix.lower() != ".pdf":
        return f"Error: only PDF files are supported, got {file_path.suffix}"

    new_hash = idx["file_content_hash"](file_path)
    db = idx["load_db"]()

    # Already indexed?
    try:
        col = db.get_collection("structure_chunks")
        dup = col.get(where={"content_hash": new_hash})
        if dup["ids"]:
            return (
                f"Document already indexed (content hash {new_hash}). "
                f"{len(dup['ids'])} chunks exist. Skipped."
            )
    except Exception:
        pass

    # Same source name but changed content → delete old chunks
    source = file_path.stem
    for col_name in ("structure_chunks", "fixed_chunks"):
        try:
            col = db.get_collection(col_name)
            old = col.get(where={"source": source})
            if old["ids"]:
                col.delete(ids=old["ids"])
                print(
                    f"Replaced {len(old['ids'])} old chunks for '{source}' in {col_name}.",
                    file=sys.stderr,
                )
        except Exception:
            pass

    chunks = idx["chunk_file"](file_path, design="structure")
    n = idx["embed_and_store"](chunks, "structure_chunks")
    return f"Added {n} chunks from {file_path.name} to the index."


if __name__ == "__main__":
    mcp.run()  # stdio transport
