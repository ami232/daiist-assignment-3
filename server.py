"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks of Spanish tenancy law with [law, article] citations.
- add_document(path): runs a BOE HTML file through index.py's pipeline, embeds and stores it.

Loads index/ at startup and never re-embeds the corpus. Logs go to stderr only.
Set CORPUS_BASE_ONLY=1 to hide documents added after the initial build (used by
evaluate.py for the before/after comparison).
"""

import os
import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer

import retrieval
from index import ROOT, chunk_file, embed_and_store, get_collection

mcp = MCPServer("corpus", log_level="WARNING")
BASE_ONLY = os.environ.get("CORPUS_BASE_ONLY") == "1"


def log(*a):
    print(*a, file=sys.stderr, flush=True)


@mcp.tool()
def search(query: str) -> str:
    """Search Spanish residential-tenancy law: the Ley de Arrendamientos Urbanos (LAU, Ley 29/1994),
    the Ley por el derecho a la vivienda (LDV, Ley 12/2023) and the Ley de Propiedad Horizontal
    (LPH, Ley 49/1960), consolidated BOE texts, plus any law added later with add_document.

    Use it for any question about renting a home in Spain: contract length and renewals, rent and
    rent updates, deposits (fianza), repairs and works, selling a rented flat, tensioned-market
    zones, large landlords (grandes tenedores), and owners' associations (comunidad de propietarios).
    Write the query in Spanish with the legal terms if you know them. Call it again with other
    words if the first results do not answer the question.

    Returns the 5 most relevant passages, each with the citation to use, e.g. [LAU, Artículo 9],
    the law's title, the article heading and the article text.
    """
    hits = retrieval.search(query, base_only=BASE_ONLY)
    return retrieval.format_hits(hits)


@mcp.tool()
def add_document(path: str) -> str:
    """Add one law to the searchable index. `path` is a local BOE HTML page (a file saved from
    boe.es/buscar/act.php?id=... or doc.php?id=...), relative to the project folder or absolute.

    The file is parsed article by article, chunked, embedded with Gemini and stored. If the same
    law is already indexed with identical text, nothing is embedded; if its text changed, the old
    chunks of that law are replaced. Returns what was added (law, chunks, new embeddings).
    Only call it when the user explicitly asks to add a document.
    """
    p = Path(path).expanduser()
    if not p.is_absolute():
        p = ROOT / p
    if not p.is_file():
        return f"ERROR: file not found: {p}"
    try:
        chunks = chunk_file(p, design=retrieval.DEFAULT_DESIGN, origin="added")
    except ValueError as e:
        return f"ERROR: {e}"
    source = chunks[0]["metadata"]["source"]
    col = get_collection(retrieval.DEFAULT_DESIGN)
    old_ids = set(col.get(where={"source": source}, include=[])["ids"])
    new_ids = {c["id"] for c in chunks}
    if old_ids and old_ids == new_ids:
        return (f"Already indexed: {source} ({chunks[0]['metadata']['title']}), {len(chunks)} chunks "
                f"with identical text. Nothing was embedded.")
    stale = old_ids - new_ids
    if stale:
        col.delete(ids=list(stale))
    res = embed_and_store(chunks, retrieval.DEFAULT_DESIGN)
    retrieval._bm25.cache_clear()
    action = "Replaced an older version of" if old_ids else "Added"
    return (f"{action} {source} ({chunks[0]['metadata']['title']}): {len(chunks)} chunks, "
            f"{res['new']} newly embedded, {res['existing']} already stored, {len(stale)} stale chunks removed. "
            f"Cite it as [{source}, <article>].")


if __name__ == "__main__":
    log(f"corpus server: {get_collection(retrieval.DEFAULT_DESIGN).count()} chunks"
        + (" (base corpus only)" if BASE_ONLY else ""))
    mcp.run()  # stdio
