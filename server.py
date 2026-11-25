"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns the top chunks with document title and page.
- add_document(path): runs a PDF through index.py's pipeline, embeds it and stores it.

Loads index/ at startup and never re-embeds the corpus. Prints nothing to
stdout (it carries the protocol); logs go to stderr.
"""

import logging
import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer

from index import DOCUMENTS, chunk_file, embed_and_store, get_collection
from retrieval import search as search_chunks

logging.basicConfig(stream=sys.stderr, level=logging.WARNING)
log = logging.getLogger("corpus")

mcp = MCPServer("corpus", log_level="WARNING")
collection = get_collection()  # load the existing index once, at startup
log.warning("corpus server ready: %d chunks in the index", collection.count())

TOP_K = 5


@mcp.tool()
def search(query: str) -> str:
    """Search the official EIC Accelerator documents: the EIC Work Programme 2027,
    the EIC Accelerator Guide for Applicants and the EIC Fund Investment Guidelines.
    Use it for any question about EIC Accelerator funding: eligibility, grant and
    investment amounts, deadlines and cut-off dates, the application steps, evaluation
    and interviews, and how the EIC Fund invests.

    Returns the 5 most relevant passages, each with its document title and page number.
    Answer only from these passages and cite them as (document title, p. N). If none of
    them answers the question, search again with different words or say the documents
    do not cover it. For a question with two parts, search once for each part."""
    results = search_chunks(query, k=TOP_K)
    if not results:
        return "No passages found."
    blocks = [f"[{r['rank']}] {r['title']}, p. {r['page']}\n{r['text']}" for r in results]
    return "\n\n".join(blocks)


@mcp.tool()
def add_document(path: str) -> str:
    """Add a new PDF document to the searchable collection. Give the full path to a
    PDF file on this computer. The file is extracted, cleaned, cut into chunks, embedded
    and stored, so the search tool can find it straight away.

    If the document is already in the index (same file name, or one of the corpus
    documents), nothing is added: no duplicates and no embedding cost. Returns how many
    chunks were added."""
    file = Path(path).expanduser()
    if not file.is_file():
        return f"Error: no file found at {file}."
    if file.suffix.lower() != ".pdf":
        return "Error: only PDF files are supported."

    known = next((d for d in DOCUMENTS if d["file"] == file.name), None)  # one of the corpus files?
    chunks = chunk_file(file, known["source"], known["title"]) if known else chunk_file(file)
    if not chunks:
        return f"Error: no text could be extracted from {file.name}."
    source = chunks[0]["source"]
    already = collection.get(where={"source": source}, include=[])["ids"]
    if already:
        return (f"'{file.name}' is already indexed ({len(already)} chunks, source '{source}'). "
                "Nothing was added.")

    added = embed_and_store(chunks, collection)
    log.warning("added %s: %d chunks", file.name, added)
    return (f"Added '{file.name}' as source '{source}': {added} chunks from "
            f"{len({c['page'] for c in chunks})} pages. It can now be searched.")


if __name__ == "__main__":
    mcp.run()  # stdio
