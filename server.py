"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns the 5 best chunks, each with a citation line.
- add_document(path): runs a PDF through index.py's pipeline (imported, not
  rewritten), embeds its chunks and stores them.

Loads the committed index/ at startup and never re-embeds the corpus. Logs go
to stderr only; stdout carries the MCP protocol.

Optional env var RAG_DOCS=AAR1001,AAR1003,AAR1401 restricts search to those
documents (evaluate.py uses it to evaluate the frozen base corpus).
"""

import os
import sys
import warnings
from pathlib import Path

warnings.filterwarnings("ignore")  # keep stderr readable in the editor's MCP log

from mcp.server.mcpserver import MCPServer

import index as ix

mcp = MCPServer("corpus", log_level="WARNING")
TOP_K = 5
DOC_FILTER = [d.strip() for d in os.environ.get("RAG_DOCS", "").split(",") if d.strip()] or None


@mcp.tool()
def search(query: str) -> str:
    """Search NTSB aircraft accident reports and return the 5 most relevant passages.

    The corpus holds full NTSB accident reports: Colgan Air 3407 (AAR1001, stall on
    approach to Buffalo, 2009), US Airways 1549 (AAR1003, bird strikes and Hudson River
    ditching, 2009) and Asiana 214 (AAR1401, low-speed approach into the San Francisco
    seawall, 2013), plus any report added later with add_document. Use it for any
    question about what these reports found, their probable causes and contributing
    factors, and the safety recommendations they issued. Search once per sub-question
    (for a comparison, search each accident separately) and use specific terms
    (flight number, system, recommendation number like A-10-10).

    Returns numbered passages, each headed by a citation such as
    [AAR1001 p.165 (printed 151) | 3.1 Findings]: report id, PDF page (as shown in a
    PDF viewer), the page number printed on the report page, and the section. Cite
    passages in that form. If no passage addresses the question, the corpus does not
    cover it.
    """
    query = (query or "").strip()
    if not query:
        return "Empty query. Pass the question or key terms to search for."
    hits = ix.search(query, k=TOP_K, design=ix.CHOSEN_DESIGN, doc_ids=DOC_FILTER)
    if not hits:
        return "No passages found. The corpus does not cover this."
    return ix.format_hits(hits)


@mcp.tool()
def add_document(path: str) -> str:
    """Add one PDF report to the searchable corpus (it changes the index; ask the user first).

    `path` is a local PDF file. The file is extracted, cleaned, chunked by section and
    embedded with Gemini, then stored so search() can find it. The document id is the
    file name without extension (e.g. AAR2002.pdf -> AAR2002).

    If the same file (same SHA-256) is already indexed, nothing is done and no embedding
    quota is spent. If a document with the same id but different content exists, it is
    treated as a new version: its old chunks are removed and replaced. Returns a short
    summary: document id, pages, chunks added and whether it was new, unchanged or replaced.
    """
    p = Path(path).expanduser()
    if not p.is_absolute():
        p = (ix.ROOT / p).resolve()
    if not p.is_file():
        return f"Not added: no file at {p}."
    if p.suffix.lower() != ".pdf":
        return f"Not added: {p.name} is not a PDF. Only PDF reports are supported."
    doc_id = p.stem.upper()
    reg = ix.load_registry()
    sha = ix.file_sha256(p)
    old = reg.get(doc_id)
    if old and old.get("sha256") == sha and old.get("complete", {}).get(ix.CHOSEN_DESIGN):
        return (f"Already indexed: {doc_id} ({old.get('pages')} pages, {old.get('chunks_' + ix.CHOSEN_DESIGN)} chunks) "
                f"with identical content. Nothing changed, no embeddings used.")
    status = "replaced (new version)" if old and old.get("sha256") != sha else "new"
    if old and old.get("sha256") == sha:
        status = "resumed (previous run was incomplete)"
    try:
        s = ix.index_file(p, doc_id, title=_guess_title(p, doc_id), designs=(ix.CHOSEN_DESIGN,),
                          meta={"added_by": "add_document"})
    except ix.QuotaExhausted:
        return (f"Partly added: {doc_id} stopped at the daily embedding quota. Chunks embedded so far are saved "
                f"and searchable; call add_document again after the reset to finish.")
    d = s["designs"][ix.CHOSEN_DESIGN]
    ix._bm25_cache.clear()
    return (f"Added {doc_id}: {status}. {d['chunks']} chunks ({d['embedded_now']} embedded now, "
            f"{d['already_stored']} already stored, {d['pruned']} old chunks removed). It is now searchable.")


def _guess_title(path: Path, doc_id: str) -> str:
    """First substantial line of the report's first pages, as a human-readable title."""
    try:
        import pypdf
        r = pypdf.PdfReader(str(path))
        text = " ".join((r.pages[i].extract_text() or "") for i in range(min(2, len(r.pages))))
        for line in text.splitlines():
            line = line.strip()
            if 25 <= len(line) <= 140 and any(w in line for w in ("Flight", "Airlines", "Air ", "Accident")):
                return line
    except Exception as e:  # noqa: BLE001
        print(f"title guess failed: {e}", file=sys.stderr)
    return doc_id


if __name__ == "__main__":
    mcp.run()  # stdio
