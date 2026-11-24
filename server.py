"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Loads the committed index/ at startup and never re-embeds the corpus. Prints
nothing to stdout (it carries the protocol); logs go to stderr.
"""

import logging
import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer

import index
import retrieval

logging.basicConfig(stream=sys.stderr, level=logging.WARNING)
mcp = MCPServer("corpus", log_level="WARNING")

TOP_K = 5
ALLOWED = {".xml", ".pdf", ".txt", ".md", ".html", ".htm"}


@mcp.tool()
def search(query: str) -> str:
    """Search Spanish labour law: the Estatuto de los Trabajadores (RDL 2/2015),
    the Ley de Prevención de Riesgos Laborales (Ley 31/1995) and the Ley sobre
    Infracciones y Sanciones en el Orden Social (RDL 5/2000), consolidated
    versions from the BOE, plus any document added with add_document.

    Use it for any question about employment contracts, working time, holidays,
    leave, pay, dismissal and severance, collective bargaining, workplace
    health and safety, or labour inspection fines in Spain. Write the query in
    Spanish with the legal terms you expect in the text (e.g. "indemnización
    despido improcedente"). Call it again with other wording if the results do
    not cover the question.

    Returns the 5 most relevant passages (semantic search, one chunk per article
    or apartado),
    each headed by "CITE AS: [law, article/apartado]", the date that version
    came into force and the BOE link. Cite exactly the CITE AS text.
    """
    hits = retrieval.search(query, k=TOP_K)
    return retrieval.format_hits(hits)


@mcp.tool()
def add_document(path: str) -> str:
    """Add a document to the labour-law index so search can find it.

    `path` is a local file: a BOE consolidated-text XML (best: split by
    article), or a .pdf, .txt, .md or .html (split by "Artículo N" headings
    when present, else by page). The file is cleaned, chunked, embedded with
    Gemini and stored.

    If the same file (same content) is already indexed, nothing is embedded
    and the tool says so. If a different version of a document with the same
    name is indexed, its old chunks are replaced by the new ones.
    Returns how many chunks were added and their locations.
    """
    p = Path(path).expanduser()
    if not p.is_absolute():
        p = (Path(__file__).resolve().parent / p)
    if not p.is_file():
        return f"Error: no file at {p}."
    if p.suffix.lower() not in ALLOWED:
        return f"Error: unsupported file type {p.suffix}. Use one of {sorted(ALLOWED)}."

    chunks = index.chunk_file(p)
    if not chunks:
        return f"Error: no text could be extracted from {p.name}."
    source, sha = chunks[0]["source"], chunks[0]["file_sha1"]
    col = index.get_collection()
    old = col.get(where={"source": source}, include=["metadatas"])
    if old["ids"] and all(m.get("file_sha1") == sha for m in old["metadatas"]):
        return (f"Already indexed: {p.name} ({chunks[0]['title']}) is in the index with the same "
                f"content ({len(old['ids'])} chunks). Nothing was embedded.")
    replaced = ""
    if old["ids"]:
        col.delete(ids=old["ids"])
        replaced = f" Replaced {len(old['ids'])} chunks from an earlier version."
    try:
        added = index.embed_and_store(chunks, col)
    except index.QuotaExhausted:
        return "Error: the daily Gemini embedding quota is used up. Partial progress was saved; try again tomorrow."
    locs = ", ".join(c["location"] for c in chunks[:8]) + (" ..." if len(chunks) > 8 else "")
    return (f"Indexed {p.name} as '{chunks[0]['title']}': {added} new chunks embedded "
            f"({len(chunks)} in total).{replaced} Locations: {locs}")


if __name__ == "__main__":
    mcp.run()  # stdio
