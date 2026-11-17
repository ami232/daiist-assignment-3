"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Loads index/ at startup and never re-embeds the corpus. Logs go to stderr only:
stdout carries the protocol.
"""

import logging
import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer

import index as pipeline
from retrieval import ACTIVE_DESIGN, DEFAULT_K, Retriever, format_hits

logging.basicConfig(stream=sys.stderr, level=logging.WARNING)
log = logging.getLogger("corpus")

mcp = MCPServer("corpus", log_level="WARNING")
retriever = Retriever(ACTIVE_DESIGN)
log.warning("corpus server ready: %d chunks in design %r", len(retriever), ACTIVE_DESIGN)


@mcp.tool()
def search(query: str) -> str:
    """Search EU banking regulation: the CRR (Regulation (EU) No 575/2013: own funds,
    capital ratios in Art. 92, large exposures, liquidity, leverage, disclosure; NOT the
    risk-weighted-asset calculation of Part Three Titles II-VI), the CRD (Directive
    2013/36/EU: authorisation of credit institutions, supervision, capital buffers,
    governance and remuneration) and MiFID II (Directive 2014/65/EU: investment firms,
    investor protection, trading venues), in their current consolidated English versions.

    Use it for every question about what these rules require; write the query in English
    with the regulatory terms you expect in the text. Returns the 5 most relevant passages,
    each with the citation to use, e.g. [CRR, Article 395(1)], followed by the passage text.
    If nothing relevant comes back, the corpus does not cover the question.
    """
    hits = retriever.search(query, k=DEFAULT_K, fallback=True)
    return format_hits(hits)


@mcp.tool()
def add_document(path: str) -> str:
    """Add one document to the searchable corpus. `path` is a local file: an EUR-Lex
    (X)HTML act (kept article by article), a PDF (one passage set per page) or a text file.

    It is chunked with the same pipeline as the corpus and only new or changed chunks are
    embedded. If the same file was indexed before, unchanged chunks are kept, changed ones
    re-embedded and chunks no longer in the file removed. Returns what was added.
    Only run it when the user explicitly asks to add a document.
    """
    file = Path(path).expanduser()
    if not file.is_file():
        return f"Not added: no file at {file}."
    try:
        chunks = pipeline.chunk_file(file, ACTIVE_DESIGN)
    except Exception as error:  # noqa: BLE001 - report parse problems to the caller
        return f"Not added: could not read {file.name} ({type(error).__name__}: {error})."
    if not chunks:
        return f"Not added: no text could be extracted from {file.name}."

    col = retriever.col
    previous = col.get(where={"file": file.name}, include=[])["ids"]
    stale = sorted(set(previous) - {c["id"] for c in chunks})
    try:
        stats = pipeline.embed_and_store(chunks, ACTIVE_DESIGN)
    except pipeline.QuotaExhausted:
        retriever.reload()
        return "Partly added: the daily embedding quota ran out. Run add_document again after the reset."
    if stale:
        col.delete(ids=stale)
    retriever.reload()

    source = chunks[0]["metadata"]["source"]
    if stats["embedded"] == 0 and not stale:
        return f"Already indexed: {file.name} ({len(chunks)} chunks as source '{source}'), nothing changed."
    return (f"Indexed {file.name} as source '{source}': {len(chunks)} chunks, "
            f"{stats['embedded']} embedded, {stats['already_saved']} unchanged, {len(stale)} removed. "
            f"The corpus now has {len(retriever)} chunks.")


if __name__ == "__main__":
    mcp.run()  # stdio
