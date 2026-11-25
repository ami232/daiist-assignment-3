"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks of the EU drone rules with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Loads index/ at startup and never re-embeds the corpus. Prints nothing to
stdout (it carries the protocol); logs go to stderr.
"""

import hashlib
import logging
import sys
from datetime import datetime, timezone
from pathlib import Path

from mcp.server.mcpserver import MCPServer

import index
import rag

logging.basicConfig(stream=sys.stderr, level=logging.WARNING)
log = logging.getLogger("corpus")

mcp = MCPServer("corpus", log_level="WARNING")
import os

# CORPUS_BASE_ONLY=1 (set by evaluate.py) restricts search to the three base documents.
retriever = rag.Retriever(rag.SERVED_DESIGN, base_only=os.environ.get("CORPUS_BASE_ONLY") == "1")


@mcp.tool()
def search(query: str) -> str:
    """Search the EU drone (UAS) rules: Regulation (EU) 2019/947 on drone operations
    (Open/Specific categories, subcategories A1/A2/A3, remote pilot competency, operator
    registration, geographical zones, standard scenarios STS), Regulation (EU) 2019/945
    on drone classes C0-C6 and their technical requirements (class marks, remote ID,
    geo-awareness), and EASA's Acceptable Means of Compliance and Guidance Material.
    Consolidated with all amendments up to June 2026. Not covered: national rules of
    individual Member States, U-space, the SORA risk-assessment method, non-EU rules.

    Use it for any question about what a drone pilot or operator in the EU may or must do.
    Ask one focused question per call (e.g. "minimum age for remote pilots in the open
    category"); call again with different wording if the results miss.

    Returns the 5 most relevant passages, each with a citation in the form
    [source | location], where location is the article, rule point (e.g. UAS.OPEN.020)
    or AMC/GM heading. Cite these exactly.
    """
    try:
        hits = retriever.search(query, k=rag.SERVED_K, method=rag.SERVED_METHOD)
        return rag.format_hits(hits)
    except Exception as error:  # noqa: BLE001 - embedding API down or daily quota used up
        # Degrade instead of failing: keyword search needs no embeddings (hit@5 0.846 vs 1.0 dense).
        log.warning("dense search failed (%s); using keyword fallback", str(error)[:120])
        hits = retriever.search(query, k=rag.SERVED_K, method="bm25")
        return (f"{rag.FALLBACK_NOTE}\n\n" + rag.format_hits(hits)) if hits else (
            f"{rag.FALLBACK_NOTE}\n\nNo passages matched the keywords. Try other words; "
            "this is not evidence that the corpus lacks the topic.")


@mcp.tool()
def add_document(path: str) -> str:
    """Add a document to the drone-rules index so search can find it. Takes a file path
    (relative to the project folder or absolute, inside the project) to a .pdf, .html,
    .xml, .txt or .md file. Extracts, cleans and chunks it with the same pipeline as the
    corpus, embeds the chunks and stores them.

    If the identical file is already indexed it does nothing. If a file with the same
    name but different content is indexed, the new version replaces the old one.
    Returns what happened: source id, number of chunks and the locations indexed.
    """
    root = index.ROOT.resolve()
    file = Path(path)
    file = (file if file.is_absolute() else root / file).resolve()
    if not file.is_relative_to(root):
        return f"Refused: {file} is outside the project folder ({root})."
    if not file.is_file():
        return f"Not found: {file}"

    digest = hashlib.sha256(file.read_bytes()).hexdigest()
    collection = index.get_collection(rag.SERVED_DESIGN)
    same = collection.get(where={"doc_hash": digest}, include=["metadatas"], limit=1)
    if same["ids"]:
        source = same["metadatas"][0]["source"]
        count = len(collection.get(where={"source": source}, include=[])["ids"])
        return f"Already indexed: {file.name} is in the index as source '{source}' ({count} chunks). Nothing changed."

    try:
        chunks = index.chunk_file(file, rag.SERVED_DESIGN)
    except ValueError as error:
        return f"Could not index {file.name}: {error}"
    if not chunks:
        return f"Could not index {file.name}: no text could be extracted."

    added = datetime.now(timezone.utc).isoformat(timespec="seconds")
    for c in chunks:
        c.metadata.update({"doc_hash": digest, "added": added, "file": file.name})
    sources = {c.metadata["source"] for c in chunks}
    if sources & set(index.DOCS):
        return f"Refused: {file.name} would overwrite the base corpus source(s) {sorted(sources & set(index.DOCS))}."

    previous = sum(len(collection.get(where={"source": s}, include=[])["ids"]) for s in sources)
    try:
        embedded = index.embed_and_store(chunks, rag.SERVED_DESIGN)
    except index.QuotaExhausted:
        return "Could not finish: the daily embedding quota is used up. Chunks embedded so far are saved; try again after the reset."
    removed = index.remove_stale(chunks, rag.SERVED_DESIGN, sources)
    retriever.reload()

    locations = list(dict.fromkeys(c.metadata["location"] for c in chunks))
    action = f"Replaced the previous version ({previous} chunks)" if previous else "Added"
    shown = ", ".join(locations[:12]) + (" ..." if len(locations) > 12 else "")
    log.warning("add_document %s: %d chunks, %d embedded, %d removed", file.name, len(chunks), embedded, removed)
    return (f"{action}: {file.name} as source '{', '.join(sorted(sources))}', {len(chunks)} chunks "
            f"({embedded} newly embedded). Locations: {shown}")


if __name__ == "__main__":
    mcp.run()  # stdio
