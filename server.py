"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns the top 5 chunks, each with source, section and page.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Loads the committed index/ at startup and never re-embeds the corpus. Prints
nothing to stdout (it carries the protocol); logs go to stderr.
"""

import json
import os
from pathlib import Path

os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")

from mcp.server.mcpserver import MCPServer  # noqa: E402

import index  # noqa: E402
import retrieval  # noqa: E402

TOP_K = 5
SUPPORTED = {".pdf", ".txt", ".md"}

mcp = MCPServer("corpus", log_level="WARNING")


def settings() -> tuple[str, str]:
    config = json.loads(index.CONFIG_FILE.read_text()) if index.CONFIG_FILE.exists() else {}
    return config.get("design", "sections"), config.get("mode", "vector")


@mcp.tool()
def search(query: str) -> str:
    """Search official US National Weather Service (NWS) documents on winter weather:
    what Winter Storm, Blizzard, Ice Storm, Winter Weather, Extreme Cold and Snow Squall
    watches, warnings and advisories mean and when they are issued (NWS Instructions
    10-513, 10-514, 10-515), the official Storm Data event definitions (NWSI 10-1605),
    the Winter Storm Severity Index guide, and the NWS winter safety guide (frostbite,
    hypothermia, preparedness).

    Use it for any question about winter weather alerts, their criteria, or winter
    safety, and search again with other words if the first results do not answer it.
    Returns the 5 most relevant passages, numbered, each with a citation in the form
    (source, section, page). Cite these exactly; if no passage answers the question,
    the corpus does not cover it.
    """
    design, mode = settings()
    return retrieval.format_results(retrieval.search(query, k=TOP_K, design=design, mode=mode))


@mcp.tool()
def add_document(path: str) -> str:
    """Add one document (a .pdf, .txt or .md file on this computer) to the winter
    weather corpus so that later searches can find it. The file is extracted,
    cleaned, chunked by section and embedded with the same pipeline as the corpus.

    The document is identified by its file name. If the same file was already
    indexed with the same content, nothing is embedded again; if a file with that
    name was indexed with different content, its old chunks are replaced.
    Returns how many chunks were added and how many were already there.
    """
    file = Path(path).expanduser().resolve()
    if not file.is_file():
        return f"Not added: {file} does not exist."
    if file.suffix.lower() not in SUPPORTED:
        return f"Not added: {file.suffix} files are not supported (use .pdf, .txt or .md)."

    design, _ = settings()
    chunks = index.chunk_file(file, design)
    source = index.source_id(file)
    store = index.collection(design)
    old_ids = set(store.get(where={"source": source}, include=[])["ids"])
    new_ids = {c["id"] for c in chunks}

    if old_ids == new_ids:
        return f"Already indexed: {source} ({len(chunks)} chunks) has not changed, so nothing was embedded."
    stale = sorted(old_ids - new_ids)
    if stale:
        store.delete(ids=stale)
    added = index.embed_and_store(chunks, design)
    action = "Replaced" if old_ids else "Added"
    return (f"{action} {source}: {added} new chunks embedded, {len(chunks) - added} unchanged, "
            f"{len(stale)} outdated chunks removed. It is now searchable.")


if __name__ == "__main__":
    mcp.run()  # stdio
