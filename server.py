"""
Assignment 3: MCP server `corpus`. Your editor and agent.py start it; by hand: `uv run server.py`.

Tools
  search(query)      -> the 5 most relevant passages of the Spanish anti-doping corpus, each with
                        a numbered citation (document, article, sub-article).
  add_document(path) -> runs a file through index.py's pipeline (extract, chunk, embed, store).

Loads the committed index/ at startup and never re-embeds the corpus. Nothing is printed to
stdout (it carries the MCP protocol); logs go to stderr.
"""

from __future__ import annotations

import json
from pathlib import Path

from mcp.server.mcpserver import MCPServer

import index

ROOT = Path(__file__).resolve().parent
ALLOWED_SUFFIXES = {".xml", ".txt", ".md", ".pdf"}
TOP_K = 5

mcp = MCPServer("corpus", log_level="WARNING")


def format_results(results: list[dict]) -> str:
    if not results:
        return "No passages found."
    blocks = []
    for i, r in enumerate(results, 1):
        sub = f" ({r['sublocation']})" if r.get("sublocation") else ""
        blocks.append(f"[{i}] Cita: [{r['source']}, {r['location']}{sub}] — {r['doc_title']} "
                      f"(score {r['score']})\n{r['text']}")
    return "\n\n".join(blocks)


@mcp.tool()
def search(query: str) -> str:
    """Search the Spanish anti-doping legislation corpus and return the 5 most relevant passages.

    The corpus holds, in Spanish: Ley Orgánica 11/2021 de lucha contra el dopaje en el deporte,
    its implementing regulation (Real Decreto 792/2023, consolidated), and the World Anti-Doping
    Code (Código Mundial Antidopaje 2021, as published in the BOE), plus any document added later.
    It covers doping controls, whereabouts, therapeutic use exemptions (AUT), infractions,
    sanctions, fines, procedures and appeals. It does NOT contain the list of prohibited
    substances unless that list has been added.

    Write the query in Spanish, as a question or keywords. Each passage starts with its citation,
    e.g. "Cita: [LO_11_2021, Artículo 15]", to be copied after every claim that uses it. Call it again with
    different wording if the passages do not answer the question.
    """
    return format_results(index.search(query, k=TOP_K))


@mcp.tool()
def add_document(path: str) -> str:
    """Add one document to the corpus index: extract, chunk, embed with Gemini and store it.

    `path` is a file inside this project folder (BOE consolidated XML, .txt, .md or .pdf). The
    document id is the file name without extension. If the same content is already indexed nothing
    is embedded again; if a document with that id exists with different content, its old passages
    are replaced. Returns a JSON report (chunks created, chunks embedded now, chunks replaced).
    """
    file = (ROOT / path).resolve() if not Path(path).is_absolute() else Path(path).resolve()
    if ROOT not in file.parents:
        return f"Refused: {path} is outside the project folder."
    if not file.is_file():
        return f"Refused: {path} does not exist."
    if file.suffix.lower() not in ALLOWED_SUFFIXES:
        return f"Refused: only {sorted(ALLOWED_SUFFIXES)} files can be added."
    title = None
    try:
        from corpus_sources import HELD_OUT, SOURCES
        title = {**SOURCES, **HELD_OUT}.get(file.stem, {}).get("title")
    except Exception:  # noqa: BLE001
        pass
    report = index.index_file(file, source=file.stem, doc_title=title, designs=(index.chosen_design_collection(),))
    return json.dumps(report, ensure_ascii=False)


if __name__ == "__main__":
    mcp.run()  # stdio
