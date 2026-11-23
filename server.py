"""Assignment 3 MCP server: started by your editor and by agent.py, or by hand with `uv run server.py`.

Two tools:
    search(query)        passages from the indexed corpus, each with its citation
    add_document(path)   runs a file through the index.py pipeline, embeds it and stores it

Rules kept: the index is opened at startup and the corpus is never re-embedded (only the question
is, and that is cached); nothing is printed to stdout, which carries the protocol (logs go to stderr).
"""
from __future__ import annotations

try:  # trust the Windows certificate store for the embedding API; never let this break the server
    import truststore
    truststore.inject_into_ssl()
except Exception:
    pass

import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer

from index import ACTIVE_DESIGN, DailyQuotaExceeded, chunk_file, embed_and_store
from retrieval import collection, format_hits, retrieve

ROOT = Path(__file__).resolve().parent
TOP_K = 5
MAX_NEW_CHUNKS = 60  # add_document refuses a file that would need more embeddings than this (daily quota)
ALLOWED_SUFFIXES = {".md", ".txt", ".html", ".htm", ".pdf"}

mcp = MCPServer("corpus", log_level="WARNING")
collection(ACTIVE_DESIGN)  # open the index at startup


@mcp.tool()
def search(query: str) -> str:
    """Search the investor-protection corpus and return the 5 closest passages, each with a citation.

    The corpus is public text from the U.S. Securities and Exchange Commission about how brokers and
    advisers must treat retail investors: the Regulation Best Interest and Form CRS compliance guides
    and FAQs, three SEC staff bulletins (care obligations, conflicts of interest, account
    recommendations), a staff statement on Form CRS disclosures, and Investor.gov pages on fees,
    questions to ask before investing, working with an investment professional, common scams and
    crypto assets. Documents added with add_document are searched too.

    Use it for any question about those topics, and before answering from your own knowledge.
    Each result has a Citation like [source | section], a similarity score (higher is closer), the
    document title, its URL and the passage text. Answer only from the passages and cite the
    Citation of every passage you use. If no passage answers the question, say you do not know.
    Pass the question in natural language, for example "What does the care obligation require?".
    """
    query = query.strip()
    if not query:
        return "Error: the query is empty."
    try:
        return format_hits(retrieve(query, k=TOP_K))
    except DailyQuotaExceeded:
        return "Error: the daily embedding quota is used up; search is unavailable until it resets."


@mcp.tool()
def add_document(path: str) -> str:
    """Add one document to the searchable index: read it, split it into chunks, embed and store them.

    path is a file path (absolute, or relative to the project folder); .md, .txt, .html and .pdf are
    supported. Every chunk keeps the file name as its source and its section (or page) as location.
    If the document is already indexed unchanged, nothing is embedded and nothing is duplicated. If
    it changed, its old chunks are replaced by the new ones. A file that would need more than 60 new
    embeddings is refused, to protect the free daily quota. Returns a one-line summary.
    """
    file = Path(path).expanduser()
    if not file.is_absolute():
        file = ROOT / file
    if not file.is_file():
        return f"Error: no file at {file}."
    if file.suffix.lower() not in ALLOWED_SUFFIXES:
        return f"Error: {file.suffix or 'this'} files are not supported; use {', '.join(sorted(ALLOWED_SUFFIXES))}."
    try:
        chunks = chunk_file(file)
        if not chunks:
            return f"Error: no text could be extracted from {file.name}."
        plan = embed_and_store(chunks, dry_run=True)
        if plan["to_embed"] > MAX_NEW_CHUNKS:
            return (f"Refused: {file.name} would need {plan['to_embed']} new embeddings "
                    f"(limit {MAX_NEW_CHUNKS}). Nothing was added.")
        done = embed_and_store(chunks)
    except DailyQuotaExceeded:
        return "Error: the daily embedding quota is used up; try again after it resets (09:00 in Spain)."
    except Exception as error:  # noqa: BLE001 - a bad file must not kill the server
        print(f"add_document failed for {file}: {error!r}", file=sys.stderr)
        return f"Error: could not index {file.name}: {error}"
    if done["embedded"] == 0 and done["removed_stale"] == 0:
        return f"{file.name} was already indexed unchanged ({done['chunks']} chunks); nothing was added."
    return (f"Indexed {file.name} as source '{file.stem}': {done['chunks']} chunks, "
            f"{done['embedded']} newly embedded, {done['already_stored']} already stored, "
            f"{done['removed_stale']} old chunks replaced.")


if __name__ == "__main__":
    mcp.run()  # stdio