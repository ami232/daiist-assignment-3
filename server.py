"""
Assignment 3: MCP server `corpus`. Your editor and agent.py start it; by hand: `uv run server.py`.

Loads the committed ChromaDB index in index/; never re-embeds the corpus (only the
query is embedded, and queries are cached). Logs go to stderr: stdout carries MCP.
"""

import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer

import index

ROOT = Path(__file__).resolve().parent
TOP_K = 5
DESIGN = index.DEFAULT_DESIGN  # chosen from the retrieval comparison in evaluate.py

mcp = MCPServer("corpus", log_level="WARNING")


def format_results(hits: list[dict]) -> str:
    lines = []
    for n, h in enumerate(hits, start=1):
        lines.append(
            f"[{n}] SOURCE: {h['source']} | LOCATION: {h['location']}"
            + (f" (part {h['part']})" if h.get("part", 1) > 1 and h["design"] == "articles" else "")
            + f" | URL: {h['url']} | score {h['score']}\n{h['text']}"
        )
    return "\n\n".join(lines)


@mcp.tool()
def search(query: str) -> str:
    """Search Spanish residential rental law (official consolidated BOE texts, in Spanish):
    the LAU (Ley 29/1994 de Arrendamientos Urbanos), Ley 12/2023 por el derecho a la vivienda
    and RDL 7/2019 de medidas urgentes en materia de vivienda y alquiler, plus any document
    added later with add_document.

    Use it for any question about renting a home in Spain: contract duration and extensions,
    rent and rent updates, deposits (fianza) and guarantees, who pays repairs, expenses and
    agency fees, ending the contract, eviction protections, stressed-market areas.
    Write the query in Spanish legal terms for best results (e.g. "fianza vivienda
    mensualidades"). Call it again with different words if the results do not cover the question.

    Returns the 5 most relevant passages, each headed with SOURCE (law), LOCATION (article
    or preamble) and URL. Cite answers as [SOURCE, LOCATION]. If no passage covers the
    question, the corpus does not answer it.
    """
    try:
        return format_results(index.search(query, k=TOP_K, design=DESIGN))
    except Exception as e:  # noqa: BLE001 - report to the model instead of crashing the server
        print(f"search failed: {e!r}", file=sys.stderr)
        return f"ERROR: search failed ({type(e).__name__}: {e})"


@mcp.tool()
def add_document(path: str) -> str:
    """Add a legal document to the rental-law corpus so search can find it.

    `path` is a local file: a BOE consolidated-text .xml (from the BOE open-data API),
    or a .pdf, .txt or .md. The file is cleaned, split by article, embedded with Gemini
    and stored in the index.

    If the same file is already indexed and unchanged, nothing is embedded and it says so.
    If it was indexed before but its text changed, the old chunks are replaced.
    Returns how many chunks the document has and how many were newly embedded.
    """
    p = Path(path).expanduser()
    if not p.is_absolute():
        p = (ROOT / p).resolve()
    if not p.is_file():
        return f"ERROR: no file at {p}"
    try:
        report = index.index_file(p, designs=(DESIGN,))[DESIGN]
    except Exception as e:  # noqa: BLE001
        print(f"add_document failed: {e!r}", file=sys.stderr)
        return f"ERROR: could not index {p.name} ({type(e).__name__}: {e})"
    name = index.source_for(p)[1]
    if report["embedded"] == 0 and report["removed"] == 0:
        return f"'{name}' is already indexed and unchanged ({report['chunks']} chunks). Nothing was embedded."
    return (f"Indexed '{name}' from {p.name}: {report['chunks']} chunks, "
            f"{report['embedded']} newly embedded, {report['removed']} outdated chunks removed.")


if __name__ == "__main__":
    mcp.run()  # stdio
