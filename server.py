"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): the 5 most relevant articles of the indexed Spanish sports laws,
  with law and article for every result.
- add_document(path): runs a file through index.py's pipeline (chunk_file +
  embed_and_store) and stores it. Same content already indexed -> nothing is
  added; same document with different content -> the old chunks are replaced.

Loads index/ at startup and never re-embeds the corpus. Logs go to stderr only:
stdout carries the MCP protocol.
"""

import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer

from index import chunk_file, collection, embed_and_store, search as search_index

DESIGN, K = "article", 5  # chosen in REPORT.md, "Retrieval"
SUPPORTED = {".xml", ".pdf", ".txt", ".md", ".html", ".htm"}

mcp = MCPServer("corpus", log_level="WARNING")
_col = collection(DESIGN)  # load the committed index once, at startup
print(f"corpus server: {_col.count()} chunks loaded from index/", file=sys.stderr)


def format_results(results: list[dict]) -> str:
    return "\n\n".join(f"[{r['rank']}] {r['source']} — {r['location']}\n{r['text']}" for r in results)


@mcp.tool()
def search(query: str) -> str:
    """Search Spanish national sports law: Ley 39/2022 del Deporte, Ley Orgánica 11/2021
    de lucha contra el dopaje en el deporte, Ley 19/2007 contra la violencia, el racismo,
    la xenofobia y la intolerancia en el deporte (plus any document added later).

    Use it for any question about licences, competitions, clubs and federations,
    athletes' rights and duties, doping controls and sanctions, or security and
    sanctions at sports events. Write the query in Spanish, as a short question or
    key phrase; for a question with two parts, search once per part.

    Returns the 5 most relevant passages, each headed by [n] law — article
    (e.g. "[1] Ley 19/2007 contra la violencia en el deporte — Artículo 4"),
    followed by the article text. Cite the law and article of every passage you use.
    If none of them answers the question, the laws indexed don't cover it."""
    results = search_index(query, DESIGN, k=K, hybrid=False)
    return format_results(results) if results else "No results: the index is empty."


@mcp.tool()
def add_document(path: str) -> str:
    """Add one document to the searchable index: a BOE consolidated-text XML, a PDF,
    an HTML page or a text file, given as a path on this computer.

    The file goes through the same pipeline as the corpus (extract, clean, split by
    article or page, embed with Gemini, store). If exactly the same content is already
    indexed, nothing is added. If a document with the same name was indexed with
    different content, its old passages are replaced by the new ones.

    Returns what happened: how many passages were added or replaced, or why nothing was."""
    file = Path(path).expanduser()
    if not file.is_file():
        return f"Not added: {file} does not exist or is not a file."
    if file.suffix.lower() not in SUPPORTED:
        return f"Not added: {file.suffix} files are not supported ({', '.join(sorted(SUPPORTED))})."
    chunks = chunk_file(file, DESIGN)
    if not chunks:
        return f"Not added: no text could be extracted from {file.name}."
    sources = sorted({c["source"] for c in chunks})
    old = _col.get(where={"source": {"$in": sources}}, include=[])["ids"]
    new_ids = {c["id"] for c in chunks}
    if old and set(old) == new_ids:
        return f"Already indexed: {', '.join(sources)} ({len(old)} passages), identical content. Nothing added."
    if old:
        _col.delete(ids=[i for i in old if i not in new_ids])  # a new version replaces the old one
    added = embed_and_store(chunks, DESIGN)
    action = f"Replaced the previous version of {', '.join(sources)}" if old else f"Indexed {', '.join(sources)}"
    return f"{action}: {len(chunks)} passages ({added} newly embedded). The index now holds {_col.count()} passages."


if __name__ == "__main__":
    mcp.run()  # stdio
