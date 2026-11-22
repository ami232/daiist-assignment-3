"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Loads the committed index/ at startup; never re-embeds the corpus. Logs go to
stderr only (stdout carries the MCP protocol).
"""

import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer

import index as ix
import retrieval as rt

mcp = MCPServer("corpus", log_level="WARNING")

ALLOWED_SUFFIXES = {".xml", ".pdf", ".html", ".htm", ".txt", ".md"}
MAX_FILE_MB = 20


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


@mcp.tool()
def search(query: str) -> str:
    """Search Spanish housing law: the Ley de Arrendamientos Urbanos (LAU, Ley 29/1994),
    the Ley por el derecho a la vivienda (LDV, Ley 12/2023) and the Ley de Propiedad
    Horizontal (LPH, Ley 49/1960), in their consolidated text from the BOE.

    Use it for any question about renting a home in Spain (contract length, extensions,
    deposit/fianza, rent updates, stressed-market areas, repairs, ending the contract,
    selling a rented home) or about owners' communities (comunidad de propietarios,
    meetings, shared costs, works). Write the query in Spanish with the legal terms
    if you know them; call it again with other wording if the first results miss.

    Returns the 5 most relevant passages. Each starts with "Cite as: [SOURCE, location]",
    the exact label to cite, followed by the law, section, date of the text and BOE link.
    """
    hits = rt.search(query)
    log(f"search({query!r}) -> {[rt.citation(h['metadata']) for h in hits]}")
    return rt.format_results(hits)


@mcp.tool()
def add_document(path: str) -> str:
    """Add a document to the housing-law index so search can find it.

    `path` is a local file: a BOE consolidated-law XML (preferred, from
    https://www.boe.es/datosabiertos/api/legislacion-consolidada/id/<BOE-ID>), or a
    PDF, HTML, TXT or MD file. The file is chunked by article (PDF: by page; HTML/MD:
    by heading), embedded and stored.

    If the same document is already indexed with identical text, nothing is embedded.
    If a document with the same source is indexed but its text changed (e.g. a newer
    consolidated version), the old chunks are replaced by the new ones, so search never
    returns two versions of the same law. Returns what was done and how many chunks.
    """
    file = Path(path).expanduser()
    if not file.is_absolute():
        file = (ix.ROOT / file).resolve()
    if not file.is_file():
        return f"Error: no file at {file}."
    if file.suffix.lower() not in ALLOWED_SUFFIXES:
        return f"Error: {file.suffix} files are not supported. Use one of {sorted(ALLOWED_SUFFIXES)}."
    if file.stat().st_size > MAX_FILE_MB * 1e6:
        return f"Error: file is larger than {MAX_FILE_MB} MB."

    design = rt.SEARCH_DESIGN
    try:
        chunks = ix.chunk_file(file, design)
    except Exception as error:  # noqa: BLE001
        return f"Error: could not read {file.name}: {error}"
    source, title = chunks[0]["metadata"]["source"], chunks[0]["metadata"]["title"]
    new_ids = {c["id"] for c in chunks}
    old_ids = set(ix.source_ids(source, design))

    if old_ids and old_ids == new_ids:
        return f"Already indexed: {source} ({title}), {len(chunks)} chunks, unchanged. Nothing was embedded."

    try:
        counts = ix.embed_and_store(chunks, design)
    except ix.QuotaExhausted:
        return "Error: the daily Gemini embedding quota is used up. Chunks embedded so far are saved; try again tomorrow."
    stale = old_ids - new_ids
    if stale:
        ix.collection(design).delete(ids=list(stale))
    action = "Replaced" if old_ids else "Added"
    log(f"add_document: {action} {source}: {counts['new']} embedded, {len(stale)} old chunks removed")
    return (f"{action} {source} ({title}): {len(chunks)} chunks in the index "
            f"({counts['new']} newly embedded, {counts['existing']} reused, {len(stale)} outdated chunks removed). "
            f"Search now covers it; cite it as [{source}, <location>].")


if __name__ == "__main__":
    mcp.run()  # stdio
