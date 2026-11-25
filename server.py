"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): top 5 chunks from the committed index (structured chunks, vector search: the design
  chosen in evaluate.py), each with its citation, source document and link.
- add_document(path): runs a WTO legal-text HTML page through index.py's own pipeline
  (chunk_file -> embed_and_store) and adds it to the index.

Loads index/ at startup and never re-embeds the corpus. Logs go to stderr only.
"""

import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer

import index
import retrieval

DESIGN, METHOD, TOP_K = "structured", "vector", 5
ALLOWED_SUFFIXES = {".htm", ".html"}
MAX_BYTES = 5_000_000

mcp = MCPServer("corpus", log_level="WARNING")


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


@mcp.tool()
def search(query: str) -> str:
    """Search the WTO legal texts: GATT 1947 (with its Annex I interpretive "Ad Article" notes),
    GATT 1994, GATS, TRIPS (as amended, incl. Art. 31bis), the SPS Agreement and the DSU, plus any
    document added with add_document.

    Use it for any question about what these agreements say: obligations, exceptions, definitions,
    time limits, dispute procedure. The corpus is the treaty text only. It has no panel or Appellate
    Body rulings, no tariff schedules, no other WTO agreements (e.g. Anti-Dumping, Agriculture) unless added with add_document, and no news.
    Search once per agreement or concept when a question spans several (e.g. "GATT Article XX(b)
    health exception" and "SPS Article 2.4 presumption").

    Returns up to 5 passages, best first. Each has a Citation (e.g. "GATT Art. III:1-III:4",
    "SPS Art. 2"), the source document, a URL to the article, and the text. Cite claims with the
    Citation exactly as given.
    """
    hits = retrieval.search(query, k=TOP_K, design=DESIGN, method=METHOD)
    log(f"search {query!r}: {[h.citation for h in hits]}")
    return retrieval.format_hits(hits)


@mcp.tool()
def add_document(path: str) -> str:
    """Add one WTO legal-text web page (an .htm/.html file saved from wto.org/english/docs_e/legal_e/)
    to the searchable index. The file is parsed into article-level chunks with citations, embedded and
    stored, and becomes searchable immediately.

    If the same document (same file name) is already indexed with identical text, nothing is embedded
    and the existing chunks are kept. If it is indexed but its text has changed, the old chunks are
    replaced by the new ones. Returns how many chunks were added, kept and removed.
    """
    p = Path(path).expanduser()
    if not p.is_absolute():
        p = (index.ROOT / p).resolve()
    if not p.is_file():
        return f"Error: no file at {p}."
    if p.suffix.lower() not in ALLOWED_SUFFIXES:
        return f"Error: only WTO legal-text HTML pages ({', '.join(sorted(ALLOWED_SUFFIXES))}) can be added, not {p.suffix or 'a file without extension'}."
    if p.stat().st_size > MAX_BYTES:
        return f"Error: {p.name} is larger than {MAX_BYTES // 1_000_000} MB."

    chunks = index.chunk_file(p, design=DESIGN)
    if not chunks:
        return f"Error: no provisions found in {p.name}; is it a WTO legal-text page?"
    doc_id = chunks[0].metadata["doc_id"]
    removed = index.prune(DESIGN, {c.id for c in chunks}, {doc_id})
    counts = index.embed_and_store(chunks, DESIGN)
    retrieval.invalidate()
    log(f"add_document {p.name}: {counts}, removed {removed}")

    if counts["embedded"] == 0 and removed == 0:
        return f"{p.name} is already indexed with identical text ({counts['total']} chunks); nothing was embedded."
    cites = sorted({c.metadata["citation"] for c in chunks})
    return (f"Indexed {p.name} as '{doc_id}': {counts['embedded']} chunks embedded, {counts['already']} unchanged, "
            f"{removed} outdated chunks removed. Citations now searchable include: {', '.join(cites[:15])}"
            + (" ..." if len(cites) > 15 else ""))


if __name__ == "__main__":
    mcp.run()  # stdio
