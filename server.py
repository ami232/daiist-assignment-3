"""
MCP server for the drone-rules corpus. Your editor and agent.py start it; by hand: `uv run server.py`.

Loads the committed index/ and never re-embeds the corpus. Logs go to stderr
because stdout carries the protocol.
"""

import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

import index

mcp = MCPServer("corpus", log_level="WARNING")
VERSIONS = {s["source"]: s["version"] for s in index.SOURCES}


@mcp.tool()
def search(query: str) -> str:
    """Search the EU drone (UAS) rules: Regulation 2019/947 (how drones may be flown:
    open/specific/certified categories, A1/A2/A3 subcategories, operator registration,
    remote pilot competency, operational authorisations, standard scenarios),
    Regulation 2019/945 (drone classes C0-C6, manufacturer duties, product requirements,
    remote ID) and EASA's AMC/GM guidance to Part-UAS.

    Use it for any question about operating, buying or building a drone in the EU.
    Returns the 5 most relevant passages. Each one starts with the exact citation to copy,
    [source, location] (article, UAS point or AMC/GM heading), and its document's version.
    """
    try:
        hits = index.retrieve(query)
    except RuntimeError as e:  # no API key: MCP clients pass server.py only a few environment variables
        raise ToolError(f"{e}\nPut the key in .env: the editor or agent that starts server.py "
                        "does not pass GEMINI_API_KEY from your shell.") from e
    except Exception as e:  # network, quota, index: say what failed instead of a bare crash
        raise ToolError(f"search failed: {type(e).__name__}: {e}") from e
    if not hits:
        return "No passages found."
    return "\n\n".join(
        f"Passage {n} (score {h['score']}). Cite as: [{h['source']}, {h['location']}]. "
        f"Version: {VERSIONS.get(h['source'], 'added with add_document')}.\n{h['text']}"
        for n, h in enumerate(hits, start=1)
    )


@mcp.tool()
def add_document(path: str) -> str:
    """Add a local document (.pdf, .html or .txt) to the drone-rules index so search can find it.

    The file is extracted, chunked and embedded with the same pipeline as the corpus.
    The source name is the file name. If that file is already indexed with identical
    content nothing happens; if its content changed, the old chunks are replaced.
    Returns what was done and how many chunks were added.
    """
    file = Path(path).expanduser().resolve()
    if not file.is_file():
        return f"Error: no file at {file}"
    if file.suffix.lower() not in {".pdf", ".html", ".htm", ".txt", ".md"}:
        return f"Error: unsupported file type {file.suffix}"

    source, design = file.name, index.CHOSEN_DESIGN
    col = index.collection(design)
    old = col.get(where={"source": source}, include=["metadatas"])
    if old["ids"] and old["metadatas"][0].get("file_hash") == index.file_hash(file):
        return f"'{source}' is already indexed with the same content ({len(old['ids'])} chunks). Nothing changed."
    if old["ids"]:
        col.delete(ids=old["ids"])

    chunks = index.chunk_file(file, source, file.stem, design)
    if not chunks:
        return f"Error: no text could be extracted from '{source}'."
    added = index.embed_and_store(chunks, design)
    action = "Replaced" if old["ids"] else "Added"
    print(f"add_document: {action.lower()} {source}, {added} chunks", file=sys.stderr)
    return f"{action} '{source}': {added} chunks embedded and stored in the '{design}' index."


if __name__ == "__main__":
    mcp.run()  # stdio
