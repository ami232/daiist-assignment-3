"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Loads the committed index/ and never re-embeds the corpus. Prints nothing to
stdout (it carries the protocol); logs go to stderr.
"""

from pathlib import Path

from mcp.server.mcpserver import MCPServer

import index
import retrieval

ROOT = Path(__file__).resolve().parent
TOP_K = 5

mcp = MCPServer("corpus", log_level="WARNING")


@mcp.tool()
def search(query: str) -> str:
    """Search the official EU product information (EMA SmPC and package leaflet) for the
    blood thinners Eliquis (apixaban), Xarelto (rivaroxaban) and Pradaxa (dabigatran),
    plus any document added later.

    Use it for any question about these medicines: dosing, missed doses, how to take them,
    interactions with other medicines, warnings, side effects, overdose, surgery, storage.
    Write the query as a plain question or keywords and include the medicine name.

    Returns the 5 best passages, each headed by its citation:
    [source | SmPC or Package leaflet | product | section | page].
    If no passage answers the question, the corpus does not cover it.
    """
    index.log(f"search: {query}")
    return retrieval.format_results(retrieval.search(query, k=TOP_K, method=index.active_method()))


@mcp.tool()
def add_document(path: str) -> str:
    """Add a PDF (EMA product information) to the searchable index.

    `path` is a file path, absolute or relative to the project folder. The file is
    extracted, cleaned, chunked, embedded and stored, so later searches can find it.
    If the same file is already indexed, nothing is done. If a different version of a
    document with the same name is indexed, its old passages are replaced.
    Returns what was indexed: source name, words kept and number of passages.
    """
    file = Path(path).expanduser()
    file = file if file.is_absolute() else ROOT / file
    if not file.exists():
        return f"Error: no file at {file}."
    if file.suffix.lower() != ".pdf" or file.read_bytes()[:5] != b"%PDF-":
        return f"Error: {file.name} is not a PDF. Only PDF product information can be added."

    design = index.active_design()
    _, stats = index.chunk_file(file, design)
    existing = index.collection(design).get(where={"source": stats["source"]}, include=["metadatas"])
    hashes = {m["file_hash"] for m in existing["metadatas"]}
    if hashes == {stats["file_hash"]}:
        return (f"'{stats['source']}' is already indexed with identical content "
                f"({len(existing['ids'])} passages). Nothing was changed.")
    if stats["chunks"] == 0:
        return f"Error: no SmPC or package-leaflet text found in {file.name}."

    try:
        result = index.index_file(file, design)
    except index.QuotaExhausted:
        return "Error: the daily embedding quota is used up. Passages embedded so far are saved; try again tomorrow."
    retrieval._bm25_cache.pop(design, None)  # keyword index must see the new chunks
    action = "Replaced the previous version of" if hashes else "Added"
    return (f"{action} '{result['source']}': {result['kept_words']:,} words kept from "
            f"{result['pages']} pages, {result['chunks']} passages ({result['embedded']} newly embedded, "
            f"{result['stale_removed']} old passages removed). It is now searchable.")


if __name__ == "__main__":
    mcp.run()  # stdio
