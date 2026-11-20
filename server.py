"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): top chunks of the Anthropic IPO corpus, each with a citation
  [SOURCE | section path | page] and the document's status/date.
- add_document(path): runs one file through index.py's pipeline (chunk_file ->
  embed_and_store) and stores it in the persistent index.

Loads index/ at startup and never re-embeds the corpus. Prints nothing to
stdout (it carries the protocol); logs go to stderr.
"""

from __future__ import annotations

import datetime as dt
import os
import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import ToolAnnotations

import index as ix
import retrieval

ROOT = Path(__file__).resolve().parent
TOP_K = 5
# Retrieval design served to the agent, chosen by the Phase 4 comparison (eval/retrieval_summary.csv):
# vector beat bm25 and hybrid on evidence Hit@1/3/5 (0.76/0.93/0.97 on 29 answerable questions).
SEARCH_DESIGN = os.environ.get("CORPUS_SEARCH_DESIGN", "vector")
MAX_QUERY_CHARS = 1000
MAX_FILE_MB = 25

mcp = MCPServer("corpus", log_level="WARNING")


def log(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


def format_hits(query: str, hits: list[retrieval.Hit], design: str, note: str = "") -> str:
    lines = [f'Search results for: "{query}" (design: {design}, top {len(hits)})']
    if note:
        lines.append(f"NOTE: {note}")
    lines.append("Cite a passage exactly as its bracketed citation; each is a different chunk.")
    for n, h in enumerate(hits, start=1):
        status = f"{h.status}, filed {h.filed}" if h.filed else h.status
        lines.append(f"\n[{n}] [{h.source} | {h.location} | p. {h.page}]  ({status}; chunk {h.id})\n{h.text}")
    return "\n".join(lines)


@mcp.tool(annotations=ToolAnnotations(title="Search the Anthropic IPO corpus", read_only_hint=True, open_world_hint=False))
def search(query: str) -> str:
    """Search the Anthropic, PBC IPO disclosure corpus and return the 5 most relevant passages.

    The corpus (frozen 2026-11-19) holds: US-PROSPECTUS (Form S-1/A Amendment No. 3, the
    U.S. PRELIMINARY prospectus: offering terms, risk factors, MD&A and financials,
    business, governance, capital stock, lock-ups, underwriting); EU-PROSPECTUS (the
    BaFin-approved EEA prospectus, EU-specific parts: summary, persons responsible,
    terms of the securities, details of the European retail offer); CHARTER (amended
    and restated certificate of incorporation). Personal names are replaced by roles
    such as [Co-founder 1 (CEO)]. All offering terms are preliminary (estimated range
    $70.00-$78.00); final pricing is NOT in the corpus unless a document was added.

    Use it for any factual question about the offering, financials, risks, business,
    governance or shareholder rights. Ask one specific question per call; a question that
    needs several facts (e.g. two documents, or a term and a figure) must be split into one
    search per fact, because one search rarely returns every passage needed. Each result starts with a citation
    [SOURCE | section > subsection | p. page] followed by the passage text; answer only
    from these passages and cite them exactly.
    """
    query = (query or "").strip()
    if not query:
        raise ToolError("the query is empty. Pass a specific question or keywords.")
    if len(query) > MAX_QUERY_CHARS:
        raise ToolError(f"the query is longer than {MAX_QUERY_CHARS} characters. Ask a shorter, specific question.")
    try:
        hits = retrieval.search(query, TOP_K, SEARCH_DESIGN)
        return format_hits(query, hits, SEARCH_DESIGN)
    except Exception as error:  # noqa: BLE001 - degrade to keyword search rather than fail
        log(f"search: {SEARCH_DESIGN} failed ({type(error).__name__}: {str(error)[:200]}); falling back to bm25")
        hits = retrieval.search(query, TOP_K, "bm25")
        return format_hits(query, hits, "bm25",
                           note="semantic search was unavailable (embedding API error); these are keyword (BM25) results")


def _resolve_inside_project(path: str) -> Path:
    candidate = Path(path).expanduser()
    if not candidate.is_absolute():
        candidate = ROOT / candidate
    candidate = candidate.resolve()
    if ROOT not in candidate.parents:
        raise ValueError(f"the file must be inside the project folder ({ROOT.name}/); got {path!r}")
    if not candidate.is_file():
        raise ValueError(f"no such file: {path!r}")
    if candidate.suffix.lower() not in ix.ALLOWED_SUFFIXES:
        raise ValueError(f"unsupported file type {candidate.suffix!r}; allowed: {', '.join(sorted(ix.ALLOWED_SUFFIXES))}")
    if candidate.stat().st_size > MAX_FILE_MB * 1e6:
        raise ValueError(f"the file is larger than {MAX_FILE_MB} MB")
    return candidate


@mcp.tool(annotations=ToolAnnotations(title="Add a document to the corpus index", read_only_hint=False,
                                      destructive_hint=False, idempotent_hint=True, open_world_hint=False))
def add_document(path: str) -> str:
    """Add one document (PDF, HTML, TXT or MD inside the project folder) to the searchable corpus.

    The file goes through the same pipeline as the corpus: text extraction, personal-name
    redaction, structure-aware chunking with source and location metadata, then Gemini
    embeddings stored in the persistent index. Afterwards search() can return it, cited
    under a source id derived from the file name (e.g. notice-of-price.pdf -> NOTICE-OF-PRICE).

    Duplicates: if the exact same file content is already indexed (a corpus document or a
    previously added file), nothing is embedded and the existing source id is returned.
    If a file with the same name but different content was added before, it is treated as
    a new version: the new chunks are stored and the old version's chunks are removed.
    Returns a short report: source id, chunks, words, chunks embedded now, and status.
    Use only when the user explicitly asks to add a document.
    """
    try:
        file = _resolve_inside_project(path)
    except ValueError as error:
        raise ToolError(f"{error}")
    digest = ix.sha256_file(file)

    for doc_id, entry in ix.load_manifest()["documents"].items():
        if entry.get("sha256") == digest:
            return f"Already indexed: this file is the corpus document {doc_id}. Nothing was embedded."
    registry = ix.load_registry()
    for doc_id, entry in registry.items():
        if entry["sha256"] == digest:
            return (f"Already indexed: identical content was added on {entry['added_at']} as {doc_id} "
                    f"({entry['chunks']} chunks). Nothing was embedded.")

    doc_id = ix.doc_id_for(file)
    if doc_id in {s.doc_id for s in ix.SOURCES}:
        raise ToolError(f"{doc_id} is the id of a corpus document; rename the file before adding it.")
    try:
        chunks = ix.chunk_file(file, doc_id)
    except Exception as error:  # noqa: BLE001 - report extraction problems to the caller
        raise ToolError(f"could not extract text from {file.name}: {type(error).__name__}: {error}")
    if not chunks:
        raise ToolError(f"no text could be extracted from {file.name} (is it a scanned PDF?).")

    # All-or-nothing: the index must never mix a partial new version with the old one.
    col = ix.collection()
    new_ids = {c.id for c in chunks}
    stored_before = set(col.get(ids=sorted(new_ids), include=[])["ids"])
    missing = len(new_ids - stored_before)
    remaining = ix.DAILY_BUDGET - ix.used_today()
    if missing > remaining:
        raise ToolError(f"{doc_id} needs {missing} embeddings but only {max(remaining, 0)} remain in today's budget; "
                        "nothing was changed. Try again after the daily quota resets.")

    def rollback() -> None:
        added = (set(col.get(ids=sorted(new_ids), include=[])["ids"]) - stored_before)
        if added:
            col.delete(ids=sorted(added))

    try:
        result = ix.embed_and_store(chunks)
    except SystemExit as error:  # daily quota exhausted inside embed_texts
        rollback()
        raise ToolError(f"embeddings unavailable: {error}; nothing was changed")
    except Exception as error:  # noqa: BLE001
        rollback()
        raise ToolError(f"embedding failed: {type(error).__name__}: {str(error)[:300]}; nothing was changed")
    stored_now = set(col.get(ids=sorted(new_ids), include=[])["ids"])
    if result["pending"] or stored_now != new_ids:
        rollback()
        raise ToolError(f"{doc_id} could not be stored completely ({len(stored_now)}/{len(new_ids)} chunks); "
                        "nothing was changed")

    # Only now, with the new version fully stored, remove the previous version's chunks.
    replaced = doc_id in registry
    removed = ix.delete_source(doc_id, keep_ids=new_ids) if replaced else 0
    registry[doc_id] = {
        "file": str(file.relative_to(ROOT)), "sha256": digest, "chunks": len(chunks),
        "words": sum(c.words for c in chunks), "added_at": dt.datetime.now().isoformat(timespec="seconds"),
    }
    ix.save_registry(registry)
    retrieval.refresh()
    status = f"replaced the previous version ({removed} old chunks removed)" if replaced else "new document"
    return (f"Added {doc_id} from {file.name}: {len(chunks)} chunks, {registry[doc_id]['words']} words; "
            f"{result['embedded']} embedded now, {result['already']} already stored; {status}. "
            f"It is now searchable and cited as [{doc_id} | section | p. page].")


if __name__ == "__main__":
    mcp.run()  # stdio
