"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Loads index/ at startup and never re-embeds the corpus. Prints nothing to
stdout (it carries the protocol); logs go to stderr.
"""

import logging
import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer

from index import chunk_file, embed_and_store
from retrieve import KNOWN_TICKERS, Retriever, format_results

logging.basicConfig(stream=sys.stderr, level=logging.WARNING)

mcp = MCPServer("corpus", log_level="WARNING")
retriever = Retriever()  # loads the saved chunks and vectors from index/


@mcp.tool()
def search(query: str, company: str = "") -> str:
    """Search the annual reports (SEC Form 10-K, fiscal 2025) of four US trucking and
    logistics companies: Old Dominion Freight Line (ODFL), J.B. Hunt Transport
    Services (JBHT), Saia (SAIA) and Knight-Swift Transportation (KNX). The corpus
    holds Item 1 (business: services, segments, customers, strategy, employees,
    equipment), Item 1A (risk factors) and Item 7 (management's discussion of 2025
    results, costs, capital spending and outlook), plus any document added later.

    Use it before answering any question about these companies. Ask one specific
    question per call; for questions about two companies, search once per company.

    Args:
        query: the question in plain words, e.g. "Saia capital expenditure plans for 2026".
        company: optional ticker (ODFL, JBHT, SAIA or KNX) to search only that company.

    Returns up to 5 passages, best first. Each starts with its citation,
    [source, location], e.g. [SAIA 10-K 2025, Item 7 > Outlook]. Cite answers with it.
    """
    company = company.strip().upper()
    if company and company not in KNOWN_TICKERS and company not in {m["ticker"] for m in retriever.metas}:
        return f"Unknown company {company!r}. Use one of: {', '.join(KNOWN_TICKERS)}, or leave it empty."
    return format_results(retriever.search(query, company=company or None))


@mcp.tool()
def add_document(path: str) -> str:
    """Add one SEC filing (an EDGAR .htm file of a 10-K or 10-Q) to the searchable corpus.

    The file is cleaned, cut into chunks with their source and location, embedded
    and stored in the index, so search finds it from then on. If a filing with the
    same company, form and period is already indexed, nothing is added.

    Args:
        path: path of the file on this computer, e.g. "corpus/SAIA_10-Q_2026-09-30.htm".

    Returns what was added: the source label, the number of chunks and sections.
    """
    file = Path(path).expanduser()
    if not file.is_absolute():
        file = Path(__file__).resolve().parent / file
    if not file.is_file():
        return f"No file at {path}."

    try:
        chunks = chunk_file(file)
    except ValueError as error:
        return f"Could not read {file.name}: {error}"
    if not chunks:
        return f"Found no text to index in {file.name}."

    source = chunks[0]["metadata"]["source"]
    already = retriever.collection.get(where={"source": source}, include=[])["ids"]
    if already:
        return f"{source} is already indexed ({len(already)} chunks). Nothing was added."

    new = embed_and_store(chunks, retriever.collection)
    retriever.reload()  # make the new chunks searchable right away
    sections = sorted({c["metadata"]["item"] for c in chunks})
    return f"Added {source}: {new} chunks from {', '.join(sections)}. It is now searchable."


if __name__ == "__main__":
    mcp.run()  # stdio
