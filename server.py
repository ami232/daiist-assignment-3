"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Loads index/ at startup and never re-embeds the corpus. Nothing is printed to
stdout (it carries the protocol); logs go to stderr.
"""

import os
import sys
from pathlib import Path

os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")

from mcp.server.mcpserver import MCPServer  # noqa: E402

import index  # noqa: E402
import retrieval  # noqa: E402

ROOT = Path(__file__).resolve().parent

# What add_document does with a file whose source is already in the index:
# "skip" leaves the index as it is and spends no embeddings. A 10-K is filed once
# a year and never edited; a correction comes as a separate 10-K/A filing, which
# has its own file name and so is indexed as a new source. ("replace" would
# delete the old chunks and embed the file again.)
DUPLICATE_POLICY = "skip"

mcp = MCPServer("corpus", log_level="WARNING")
retrieval.collection()  # open index/ once, at startup


@mcp.tool()
def search(query: str) -> str:
    """Search the FY2025 Form 10-K annual reports of Tesla, Ford and General Motors
    (Item 1 Business, Item 1A Risk Factors, Item 7 MD&A), as filed with the SEC.

    Use it for any question about these companies' business, segments, risks,
    2025 results, costs, tariffs, EV strategy or outlook. Write the query in
    English and name the company. For a comparison between companies, search
    once per company so each report's passage is found.

    Returns the 5 most relevant passages, each headed by its citation
    [source, Item, page] followed by the passage text. Cite those labels exactly.
    If no passage answers the question, the reports do not cover it.
    """
    hits = retrieval.retrieve(query, k=retrieval.DEFAULT_K, design=retrieval.DEFAULT_DESIGN)
    return retrieval.format_hits(hits)


@mcp.tool()
def add_document(path: str) -> str:
    """Add a Form 10-K annual report to the searchable index.

    `path` is a local EDGAR .htm/.html file (absolute, or relative to the
    project folder). Its Items 1, 1A and 7 are cleaned, chunked with source and
    page metadata, embedded with Gemini and stored, after which `search` finds
    them. A file already in the index is not embedded twice.

    Returns how many passages were added, or why nothing was added.
    """
    file = Path(path)
    file = file if file.is_absolute() else ROOT / file
    if not file.is_file():
        return f"Not added: {file} does not exist."
    try:
        chunks = index.chunk_file(file)
    except ValueError as error:
        return f"Not added: {error}"

    source = chunks[0]["metadata"]["source"]
    collection = retrieval.collection()
    existing = collection.get(where={"source": source}, include=[])["ids"]
    if existing:
        if DUPLICATE_POLICY == "skip":
            return f"Not added: {source} is already indexed ({len(existing)} passages). Nothing was embedded."
        collection.delete(ids=existing)
        print(f"Replacing {source}: deleted {len(existing)} old passages", file=sys.stderr)

    added = index.embed_and_store(chunks, collection)
    pages = sorted({c["metadata"]["page_start"] for c in chunks})
    return (
        f"Added {source} ({chunks[0]['metadata']['company']}): {added} passages embedded "
        f"from {', '.join(sorted({c['metadata']['item'] for c in chunks}))}, pages {pages[0]}-{pages[-1]}."
    )


if __name__ == "__main__":
    mcp.run()  # stdio
