"""
Assignment 3: MCP server `corpus`. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): top passages from the EU cosmetics corpus, each with its citation.
- add_document(path): runs a file through index.py's pipeline, embeds it and stores it.

Loads index/ as it is; never re-embeds the corpus. Logs go to stderr: stdout
carries the MCP protocol.
"""

import hashlib
import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer

import retrieval
from index import DEFAULT_DESIGN, ROOT, chunk_file, collection, embed_and_store

mcp = MCPServer("corpus", log_level="WARNING")


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


@mcp.tool()
def search(query: str) -> str:
    """Search the EU cosmetics law corpus: Regulation (EC) No 1223/2009 on cosmetic
    products (consolidated May 2025: articles on safety, responsible person,
    product information file, notification, animal testing, labelling and claims,
    plus the annexes listing prohibited and restricted substances, fragrance
    allergens, colorants, preservatives, UV filters and packaging symbols),
    Implementing Decision 2013/674/EU (guidelines on the cosmetic product safety
    report) and Regulation (EU) No 655/2013 (criteria for product claims).

    Use it for any question about what EU cosmetics law requires or allows.
    Phrase the query with the terms the law uses (e.g. "labelling of fragrance
    allergens in leave-on products", "linalool", a CAS number, "Article 19").
    Returns the 5 most relevant passages, numbered, each headed by
    "source | location" (article, annex entry or guideline section): cite those
    exactly. The corpus covers EU law only.
    """
    hits = retrieval.search(query)
    log(f"search {query!r}: {[h['location'] for h in hits]}")
    return retrieval.format_results(hits)


@mcp.tool()
def add_document(path: str) -> str:
    """Add one document to the corpus index so search can find it.

    `path` is a local file (.pdf, .html/.xhtml or .txt), absolute or relative to
    the project folder. The file is extracted, chunked with the same pipeline
    as the corpus (index.py) and embedded with Gemini. If exactly the same file
    is already indexed, nothing is done; if a file with the same name but
    different content is indexed, its old passages are replaced. Returns what
    was done and how many passages were added.
    """
    file = Path(path)
    if not file.is_absolute():
        file = ROOT / file
    if not file.is_file():
        return f"No file at {file}."
    sha = hashlib.sha256(file.read_bytes()).hexdigest()[:16]
    col = collection(DEFAULT_DESIGN)
    same_name = col.get(where={"file": file.name}, include=["metadatas"])
    if any(m.get("sha") == sha for m in same_name["metadatas"]):
        return f"{file.name} is already indexed ({len(same_name['ids'])} passages); nothing changed."
    replaced = len(same_name["ids"])
    if replaced:
        col.delete(ids=same_name["ids"])
    chunks = chunk_file(file)
    for c in chunks:
        c["sha"] = sha
    added = embed_and_store(chunks)
    log(f"add_document {file.name}: +{added}, replaced {replaced}")
    action = f"replaced the {replaced} old passages of {file.name} with" if replaced else "added"
    return f"Indexed {file.name}: {action} {added} passages (source '{file.stem}')."


if __name__ == "__main__":
    mcp.run()  # stdio
