"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks of Spanish traffic law with citations.
- add_document(path): runs a BOE XML file through index.py's pipeline,
  embeds only new or changed chunks and stores them.

Loads index/ at startup and never re-embeds the corpus (only the query, once,
cached). Nothing is printed to stdout, which carries the protocol; logs go to
stderr.
"""

from __future__ import annotations

import logging
import re
import sys
import threading
from pathlib import Path

from mcp.server.mcpserver import MCPServer

import index as idx
from retrieval import Index, format_results

logging.basicConfig(stream=sys.stderr, level=logging.WARNING)
log = logging.getLogger("corpus")

TOP_K = 5
DEGRADED = "NOTE: keyword search only"
SEARCH_METHOD = "dense"  # design G: dense, gemini-embedding-001, k=5 (eval/retrieval_summary.json)

mcp = MCPServer("corpus", log_level="WARNING")
_index: Index | None = None
_index_lock = threading.Lock()


def get_index() -> Index:
    """The loaded index. Tools run in worker threads, and two parallel
    searches opening ChromaDB at once crashed it, hence the lock."""
    global _index
    with _index_lock:
        if _index is None:
            _index = Index()
        return _index


@mcp.tool()
def search(query: str, source: str = "") -> str:
    """Search Spanish traffic law: the Ley de Tráfico (LSV, RDL 6/2015: offences,
    fines, the points system, its annexes), the Reglamento General de Circulación
    (RGC, RD 1428/2003: speed and alcohol limits, overtaking, priority, seatbelts,
    phones, breakdowns) and the Reglamento General de Conductores (RGCond,
    RD 818/2009: licence classes, ages, validity, foreign licences), consolidated
    texts from the BOE, plus any document added later.

    Use it for every question about Spanish driving rules; search again with
    different words, or once per sub-question, when the first results do not
    cover everything. The query can be in English or Spanish. Optionally pass
    source="LSV", "RGC" or "RGCond" to search one document only.

    Returns the 5 most relevant passages (in Spanish), each headed by its
    citation in the form [SOURCE, location], e.g. [RGC, Artículo 20], with the
    article title, the date that version came into force and the BOE link.
    If nothing in the passages answers the question, the corpus does not cover it.
    """
    query = (query or "").strip()
    if not query:
        return "Empty query: pass the question or the rule you are looking for."
    ix = get_index()
    source = source.strip() or None
    known = {c["metadata"]["source"] for c in ix.chunks}
    if source and source not in known:
        return f"Unknown source {source!r}. Indexed sources: {', '.join(sorted(known))}."
    try:
        hits = ix.search(query, k=TOP_K, method=SEARCH_METHOD, source=source)
        note = ""
    except Exception as e:  # noqa: BLE001 - e.g. the daily embedding quota
        log.warning("dense search failed (%s); falling back to keyword search", str(e)[:200])
        hits = ix.search(query, k=TOP_K, method="bm25", source=source)
        note = (f"{DEGRADED} (the query could not be embedded). Keyword search works best "
                "with Spanish legal terms, e.g. 'tasa de alcohol conductores noveles'.\n\n")
    return note + format_results(hits)


def add_document_impl(path: str) -> dict:
    """The add-document pipeline, also called directly by evaluate.py."""
    p = Path(path).expanduser()
    if not p.is_absolute():
        p = (idx.ROOT / p).resolve()
    if not p.is_file():
        return {"status": "error", "message": f"No file at {p}."}
    if p.suffix.lower() != ".xml":
        return {"status": "error", "message": "Only consolidated BOE texts in XML (from the BOE open-data API) are supported."}

    # Source name: "<SOURCE>__<BOE id>.xml" as index.py names files, else the BOE id.
    m = re.match(r"(?:(?P<src>[^_]+)__)?(?P<boe>BOE-[A-Z]-\d{4}-\d+)", p.stem)
    if not m:
        return {"status": "error", "message": "File name must contain the BOE id, e.g. BOE-A-2017-12841.xml or ITV__BOE-A-2017-12841.xml."}
    source = m.group("src") or m.group("boe")
    try:
        chunks = idx.chunk_file(p, source)
    except Exception as e:  # noqa: BLE001 - bad XML is a user error, report it
        return {"status": "error", "message": f"Could not read {p.name} as a BOE text: {e}"}
    if not chunks:
        return {"status": "error", "message": f"{p.name} produced no chunks."}

    col = get_index().col  # the collection search uses (its embedding model)
    before_ids = set(col.get(where={"source": source}, include=[])["ids"])
    # Already-indexed policy: same source -> update in place. Unchanged chunks
    # keep their vectors (no quota spent), changed ones are re-embedded, and
    # chunks the new version no longer has (repealed articles) are deleted.
    new, kept = idx.embed_and_store(chunks, col, prune_source=source)
    after_ids = set(col.get(where={"source": source}, include=[])["ids"])
    get_index().reload()
    removed = len(before_ids - after_ids)
    if not before_ids:
        status = "added"
    elif new == 0 and removed == 0:
        status = "unchanged"
    else:
        status = "updated"
    return {"status": status, "source": source, "boe_id": chunks[0]["metadata"]["boe_id"],
            "title": chunks[0]["metadata"]["doc_title"], "chunks": len(after_ids),
            "embedded": new, "reused": kept, "removed": removed}


@mcp.tool()
def add_document(path: str) -> str:
    """Add one consolidated Spanish law (a BOE XML file from the BOE open-data
    API, named like ITV__BOE-A-2017-12841.xml or BOE-A-2017-12841.xml) to the
    search index: it is split into articles, embedded with Gemini and stored,
    so search finds it from then on.

    If that document is already indexed, it is updated in place: unchanged
    articles keep their vectors, changed ones are re-embedded and articles no
    longer in the file are removed. Returns what happened: added / updated /
    unchanged, with the source name to cite and the number of chunks embedded.
    Changes the shared index, so only run it when the user asked for it.
    """
    r = add_document_impl(path)
    if r["status"] == "error":
        return "Error: " + r["message"]
    verb = {"added": "Added", "updated": "Updated", "unchanged": "Already indexed and unchanged:"}[r["status"]]
    return (f"{verb} {r['title']} ({r['boe_id']}) as source {r['source']}: {r['chunks']} chunks in the "
            f"index, {r['embedded']} newly embedded, {r['reused']} reused, {r['removed']} removed.")


if __name__ == "__main__":
    get_index()  # load index/ once at startup (vectors only, nothing is embedded)
    mcp.run()  # stdio
