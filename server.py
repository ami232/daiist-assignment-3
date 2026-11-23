"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): retrieval design B (question rewritten into German legal terms, dense search, k=5);
  returns the chunks with their citations and the German query used.
- add_document(path): runs a file through index.py's pipeline, embeds the new chunks and stores them.

Loads index/ at startup and never re-embeds the corpus: only queries and newly added chunks are embedded.
Prints nothing to stdout (it carries the protocol); logs go to stderr.
"""

from __future__ import annotations

import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer

import index
import retrieval

ROOT = Path(__file__).resolve().parent
mcp = MCPServer("corpus", log_level="WARNING")

_collection = index.get_collection()
_corpus = retrieval.Corpus(_collection)


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


def format_results(result: dict) -> str:
    lines = [f"German search query: {result['query']}", ""]
    for i, c in enumerate(result["chunks"], 1):
        if c["doc_type"] == "judgment":
            meta = f"BGH judgment, decided {c['decision_date']}"
        else:
            meta = f"statute, current version ({c['version']})" if c.get("version") else "statute"
        lines += [
            f"[{i}] {c['location']}",
            f"    title: {c['title']}",
            f"    {meta}",
            f"    url: {c['url']}",
            "    text:",
            c["text"],
            "",
        ]
    return "\n".join(lines).rstrip()


@mcp.tool()
def search(query: str) -> str:
    """Search German law on residential service charges (Betriebskosten / Nebenkostenabrechnung).

    The corpus holds the current texts of BGB §§ 535-580a (Mietrecht), the Betriebskostenverordnung
    (BetrKV), the Heizkostenverordnung (HeizkostenV) and the CO2-Kostenaufteilungsgesetz (CO2KostAufG),
    plus 17 judgments of the Bundesgerichtshof, VIII. Zivilsenat, on service charges (2014-2026), and any
    document added with add_document. Use it for every question about whether a cost can be passed on to
    tenants, how to allocate and bill it, the lease clause needed, deadlines and objections, heating and
    hot-water billing, and the CO2 cost split. It does not cover tax law, WEG law as such, local price
    levels, or rules outside these documents.

    query: the question in full, in English or German. It is rewritten into German legal terms before
    searching, so pass the user's wording with all its facts.

    Returns the 5 most relevant passages in German. Each has its citation: location (§ / Abs. / Nr. of a
    statute, or judgment with Rn. or Leitsatz), title, decision date (judgments) or statute version, and
    URL; the German query actually searched comes first. Cite the location exactly as given. Judgments
    can predate later statute changes: the current statute text wins. If no passage answers the
    question, say so rather than guessing.
    """
    try:
        return format_results(retrieval.search(_corpus, query))
    except index.DailyQuotaExhausted:
        return "Search failed: the daily embedding quota is used up. Try again after the reset (09:00 in Spain)."


@mcp.tool()
def add_document(path: str) -> str:
    """Add one legal document to the search index, so that search can find it.

    path: a file on this machine, either a judgment XML from rechtsprechung-im-internet.de or a statute
    XML from gesetze-im-internet.de (.xml, or the .zip as downloaded). Relative paths are resolved from
    the project folder.

    The file goes through the same extraction and chunking as the base corpus, and only chunks not yet
    in the index are embedded. If a document with the same doc_id (e.g. "BGH VIII ZR 6/24" or
    "HeizkostenV") is already indexed with identical content, nothing changes and the result says
    "already indexed, unchanged". If its content differs, the old version's chunks are replaced and the
    result says "updated". Returns the doc_id, the number of chunks and the number of words indexed.
    This changes the shared index: only call it when the user explicitly asks to add a document.
    """
    global _corpus
    file = Path(path).expanduser()
    if not file.is_absolute():
        file = ROOT / file
    if not file.is_file():
        return f"Not added: no file at {file}."
    try:
        chunks = index.chunk_file(file)
    except Exception as error:  # noqa: BLE001 - report any parsing problem to the caller
        return f"Not added: could not read {file.name} as a judgment or statute XML ({error})."
    if not chunks:
        return f"Not added: no text found in {file.name}."

    doc_id = chunks[0]["metadata"]["doc_id"]
    words = sum(c["metadata"]["words"] for c in chunks)
    new_ids = {c["id"] for c in chunks}
    old_ids = set(index.stored_ids(_collection, doc_id))

    if old_ids and index.content_hash(old_ids) == index.content_hash(new_ids):
        return f"{doc_id}: already indexed, unchanged ({len(chunks)} chunks, {words:,} words). Nothing was embedded."

    stale = old_ids - new_ids
    if stale:
        _collection.delete(ids=list(stale))
    try:
        embedded = index.embed_and_store(chunks, _collection, source="added")
    except index.DailyQuotaExhausted:
        return (f"{doc_id}: stopped, the daily embedding quota is used up. Chunks stored so far stay in the "
                f"index; call add_document again after the reset to finish.")
    index.sync_metadata(_collection, chunks, source="added")
    _corpus = retrieval.Corpus(_collection)  # refresh the in-memory chunk list
    log(f"add_document {doc_id}: {embedded} embedded, {len(stale)} removed")

    if old_ids:
        return (f"{doc_id}: updated. The indexed content differed, so {len(stale)} old "
                f"chunk{'s were' if len(stale) != 1 else ' was'} replaced; "
                f"now {len(chunks)} chunks, {words:,} words ({embedded} newly embedded).")
    return f"{doc_id}: added, {len(chunks)} chunks, {words:,} words."


if __name__ == "__main__":
    mcp.run()  # stdio
