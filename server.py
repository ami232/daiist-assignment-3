"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

Loads the committed index at startup and never re-embeds the corpus; only the
query (cached) and newly added documents are embedded. Logs go to stderr.
"""

import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer

import index as ix
import retrieval as rt

mcp = MCPServer("corpus", log_level="WARNING")
SERVED_CHUNKING = "article"          # chunking behind rt.DEFAULT_DESIGN


@mcp.tool()
def search(query: str) -> str:
    """Search EU law that applies to a student-run anonymous social app: the GDPR
    (Regulation 2016/679), the Digital Services Act (Regulation 2022/2065) and the
    ePrivacy Directive 2002/58/EC as consolidated in 2009, plus any document added
    later with add_document. Use it for any question about data protection, user
    rights, content moderation, notices and takedowns, cookies or platform duties.
    Ask in plain English; search again with other words if the first results miss.

    Returns the 5 best passages, each headed by its chunk id in square brackets,
    the act and article (with paragraphs), and a similarity score, then the text.
    Cite passages by their chunk id. Low similarity (under ~0.55) usually means
    the corpus does not cover the question.
    """
    try:
        return rt.format_results(rt.search(query, k=5))
    except Exception as e:  # noqa: BLE001
        print(f"search failed: {e}", file=sys.stderr)
        return f"Search failed: {e}"


@mcp.tool()
def add_document(path: str) -> str:
    """Add one document to the search index from a local file path (EU XHTML/HTML
    from the Publications Office, or plain .txt/.md). The file goes through the
    same extraction and article chunking as the corpus, its chunks are embedded
    with Gemini and saved in index/, and search uses them immediately.

    If the identical file is already indexed it is skipped and nothing is
    embedded. If a document with the same name but different content is indexed
    (e.g. an amended version), its old chunks are replaced. Returns what happened
    and how many chunks were added.
    """
    p = Path(path).expanduser()
    if not p.is_absolute():
        p = ix.ROOT / p
    if not p.is_file():
        return f"No file at {p}."
    per_design = ix.chunk_file(p)
    doc_id = per_design[SERVED_CHUNKING][0]["source"]
    sha = ix.file_hash(p)
    manifest = ix.read_manifest()
    old = manifest.get(doc_id)
    if old and old.get("sha1") == sha:
        return f"'{doc_id}' is already indexed with identical content. Nothing added."
    status = "replaced the previous version of" if old else "added"
    for design in ix.DESIGNS:
        kept = [c for c in ix.read_design(design) if c["source"] != doc_id]
        ix.write_design(design, kept + per_design[design])
    embedded = ix.embed_and_store(per_design[SERVED_CHUNKING])   # served design only, to save quota
    meta = {**ix.DOCS, **ix.EXTRA_DOCS}.get(doc_id, {})
    manifest[doc_id] = {
        "title": meta.get("title", p.stem),
        "url": ix.EURLEX.format(celex=meta["celex"]) if meta else str(p),
        "date": meta.get("date", ""), "file": p.name, "sha1": sha,
        "words": sum(len(c["text"].split()) for c in per_design[SERVED_CHUNKING]),
        "chunks": {d: len(per_design[d]) for d in ix.DESIGNS}, "added_by": "add_document",
    }
    ix.write_manifest(manifest)
    rt.get_index(SERVED_CHUNKING).reload()
    n = len(per_design[SERVED_CHUNKING])
    return f"{status} '{doc_id}': {n} chunks ({embedded} newly embedded). Search now covers it."


if __name__ == "__main__":
    mcp.run()  # stdio
