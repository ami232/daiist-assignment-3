"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns the top chunks with source, location and link.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

It serves the "structure" design (one chunk per article or guideline section),
the winner of the retrieval evaluation in eval/retrieval.csv.

The index in index/ is opened at startup and never re-embedded: only the query
(search) or the new file's chunks (add_document) cost embeddings. Nothing is
printed to stdout, which carries the MCP protocol; logs go to stderr.
"""

import hashlib
import logging
import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer

import index

DESIGN = "structure"
TOP_K = 5
SUPPORTED = {".html", ".htm", ".xhtml", ".pdf", ".txt", ".md"}

logging.basicConfig(stream=sys.stderr, level=logging.INFO, format="corpus: %(message)s")
log = logging.getLogger("corpus")

store = index.collection(DESIGN)  # load the saved index once, at startup
log.info("loaded %d chunks (%s design)", store.count(), DESIGN)

mcp = MCPServer("corpus", log_level="WARNING")


def citation(chunk: dict) -> str:
    """The exact text the agent must put in brackets; agent.py checks answers against it."""
    return f"{chunk['source']}, {chunk['location']}"


def format_chunk(rank: int, chunk: dict) -> str:
    heading = f" | {chunk['heading']}" if chunk.get("heading") else ""
    link = f"\nLink: {chunk['url']}" if chunk.get("url") else ""
    return (f"[{rank}] {citation(chunk)}{heading} | relevance {1 - chunk['distance']:.2f}{link}\n"
            f"{chunk['text']}")


@mcp.tool()
def search(query: str) -> str:
    """Search EU passenger-rights law for passages relevant to a question.

    The corpus holds: Regulation (EC) No 261/2004 (air: denied boarding,
    cancellation, long delay), the Commission's 2024 interpretative Guidelines
    on 261/2004, Regulation (EU) 2021/782 (rail), Regulation (EU) No 181/2011
    (bus and coach), Regulation (EU) No 1177/2010 (sea and inland waterway),
    plus any document added with add_document.

    Use it before answering any question about passenger rights, and again
    with different wording (or once per transport mode) when a question needs
    several rules. Write the query in English, with the legal terms you
    expect in the text (e.g. "compensation for cancellation less than two
    weeks before departure").

    Returns the 5 most similar passages, best first. Each one starts with a
    line "[n] <source>, <location> | <heading> | relevance <0-1>", then the
    passage text. Cite a passage as [<source>, <location>], copied exactly
    from that line. Low relevance (under about 0.5) or passages on another
    topic mean the corpus probably does not cover the question.
    """
    query = query.strip()
    if not query:
        return "Empty query: write the question or the rule you are looking for."
    chunks = index.search(query, DESIGN, k=TOP_K)
    log.info("search %r -> %s", query[:80], [f"{c['source']} {c['location']}" for c in chunks])
    return "\n\n".join(format_chunk(i, c) for i, c in enumerate(chunks, 1))


@mcp.tool()
def add_document(path: str) -> str:
    """Add a local file (HTML, PDF, TXT or MD) to the passenger-rights index.

    The file is split into chunks the same way as the original corpus,
    embedded and saved, so later searches can find it. Its file name (without
    extension) becomes the source name used in citations.

    - Same content already indexed: nothing is done.
    - A file with the same name but new content: its old chunks are replaced.

    Returns a short report: the source name and how many chunks were added.
    Only call it when the user asks to add a document.
    """
    file = Path(path).expanduser()
    if not file.is_absolute():
        file = index.ROOT / file
    if not file.is_file():
        return f"Not added: {file} does not exist or is not a file."
    if file.suffix.lower() not in SUPPORTED:
        return f"Not added: {file.suffix or 'no extension'} is not supported (use {', '.join(sorted(SUPPORTED))})."

    source = file.stem
    content_hash = hashlib.sha256(file.read_bytes()).hexdigest()[:16]

    same_content = store.get(where={"content_hash": content_hash}, limit=1)["metadatas"]
    if same_content:
        return f"Not added: this content is already indexed as '{same_content[0]['source']}'."

    replaced = store.get(where={"source": source})["ids"]
    if replaced:
        store.delete(ids=replaced)
        log.info("replacing %d old chunks of %s", len(replaced), source)

    chunks = index.chunk_file(file, DESIGN, source=source,
                              extra={"content_hash": content_hash, "added_by": "add_document"})
    if not chunks:
        return f"Not added: no text could be extracted from {file.name}."
    index.embed_and_store(chunks, DESIGN)
    words = sum(c.meta["words"] for c in chunks)
    action = f"Replaced the previous version ({len(replaced)} chunks) with" if replaced else "Added"
    log.info("%s %s: %d chunks", action, source, len(chunks))
    return f"{action} '{source}': {len(chunks)} chunks, {words} words. It is now searchable."


if __name__ == "__main__":
    mcp.run()  # stdio
