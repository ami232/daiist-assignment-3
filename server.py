"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

Tools:
- search(query): top chunks from THE FINALS wiki index, each with the citation to use.
- add_document(path): runs a file through index.py's pipeline (chunk_file,
  embed_and_store) and stores it. Unchanged files embed nothing; a changed
  file replaces that document's old chunks.

The index in index/ is loaded from disk; the corpus is never re-embedded here.
Nothing is printed to stdout (it carries the MCP protocol); logs go to stderr.
"""

import logging
import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer

from index import ROOT, collection, index_file
from retrieval import SERVED_DESIGN, format_hits, search as run_search

logging.basicConfig(stream=sys.stderr, level=logging.WARNING)
log = logging.getLogger("corpus")

mcp = MCPServer("corpus", log_level="WARNING")

TOP_K = 5
ALLOWED_SUFFIXES = {".json", ".html", ".htm", ".md", ".txt", ".pdf"}
MAX_BYTES = 5_000_000


@mcp.tool()
def search(query: str) -> str:
    """Search THE FINALS Community Wiki (a snapshot of the pages for every gadget,
    weapon and specialization of the Light, Medium and Heavy builds, plus the build,
    game-mode and arena pages of the video game THE FINALS).

    Use it for any question about THE FINALS: what a gadget/weapon/specialization
    does, its stats (damage, cooldown, ammo, range), which build can equip it,
    counters and tips, game-mode rules and arenas. Search again with different
    words if the first results do not answer the question; ask one search per
    item for questions that compare two things.

    Returns the 5 most relevant passages. Each starts with the exact citation to
    copy into the answer, in the form [Page § Section], followed by its URL and
    text. If nothing relevant comes back, the corpus does not cover the question.
    """
    try:
        hits = run_search(query, k=TOP_K, design=SERVED_DESIGN)
    except Exception as e:  # tell the model what went wrong instead of a bare tool error
        log.exception("search failed")
        return f"Search failed ({type(e).__name__}: {e}). Try the search again once; if it fails again, say so."
    return format_hits(hits)


@mcp.tool()
def add_document(path: str) -> str:
    """Add one document to THE FINALS wiki index so search can find it.

    `path` is a file on this machine: a wiki page downloaded by index.py
    (corpus/.../*.json), or an .html, .md, .txt or .pdf file. Relative paths are
    resolved from the project folder. The file is cleaned, split into sections,
    embedded with Gemini and stored. If the same file is already indexed nothing
    is embedded again; if it changed, its old chunks are replaced.

    Only call this when the user explicitly asks to add a document. Returns how
    many chunks were stored and embedded.
    """
    p = Path(path)
    if not p.is_absolute():
        p = ROOT / p
    p = p.resolve()
    if not p.is_file():
        return f"Error: no file at {p}"
    if p.suffix.lower() not in ALLOWED_SUFFIXES:
        return f"Error: {p.suffix} files are not supported; use one of {sorted(ALLOWED_SUFFIXES)}"
    if p.stat().st_size > MAX_BYTES:
        return f"Error: {p.name} is larger than {MAX_BYTES // 1_000_000} MB"
    try:
        report = index_file(p)
    except Exception as e:  # report the failure to the model instead of crashing the server
        log.exception("add_document failed")
        return f"Error while indexing {p.name}: {type(e).__name__}: {e}"
    lines = []
    for design, r in report.items():
        if r["embedded"] == 0 and r["replaced"] == 0:
            state = "already indexed, unchanged (nothing embedded)"
        elif r["replaced"]:
            state = f"updated: {r['replaced']} old chunks replaced, {r['embedded']} embedded"
        else:
            state = f"added: {r['embedded']} chunks embedded"
        lines.append(f"{design}: {r['source']} - {r['chunks']} chunks, {state}; collection now {collection(design).count()} chunks")
    return "\n".join(lines)


if __name__ == "__main__":
    mcp.run()  # stdio
