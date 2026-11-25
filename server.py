"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Load index/ at startup; never re-embed the corpus. Print nothing to stdout
(it carries the protocol); log to stderr. Docstrings become the tool
descriptions the model reads.
"""

import contextlib
import os
import sys
from pathlib import Path

os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")

from mcp.server.mcpserver import MCPServer

import index

ROOT = Path(__file__).resolve().parent
DESIGN = "B"            # the chunking design chosen by the retrieval numbers
TOP_K = 5               # passages returned by a search
MAX_NEW_CHUNKS = 300    # protects the free daily embedding quota

mcp = MCPServer("corpus", log_level="WARNING")
COLLECTION = index.get_collection(DESIGN)   # opens index/ once; nothing is embedded here


# ---------- search ----------

def do_search(query: str) -> str:
    query = (query or "").strip()
    if not query:
        return "ERROR: the query is empty."
    try:
        with contextlib.redirect_stdout(sys.stderr):
            vector = index.embed_texts([query])[0]
        found = COLLECTION.query(query_embeddings=[vector], n_results=TOP_K)
    except Exception as error:  # noqa: BLE001
        return f"ERROR: search failed ({type(error).__name__}: {error})"
    blocks = []
    for n, (text, meta, dist) in enumerate(
            zip(found["documents"][0], found["metadatas"][0], found["distances"][0]), 1):
        blocks.append(f"[{n}] source: {meta['doc']} | location: {meta['location']} | "
                      f"page: {meta['page']} | relevance: {1 - dist:.2f}\n{text}")
    return "\n\n".join(blocks) if blocks else "No passages found: the index is empty."


# ---------- add_document ----------

def pages_for(path):
    """(source, label, pages) for a PDF or a text file. Text files are cut into parts of about 300 words."""
    if path.suffix.lower() == ".pdf":
        source = {"doc": path.name, "kind": "generic", "file": str(path), "first": 1, "last": 100000}
        return source, "page", index.extract_pages(source)
    source = {"doc": path.name, "kind": "generic", "file": str(path)}
    paragraphs = [p.strip() for p in path.read_text(encoding="utf-8", errors="ignore").split("\n\n") if p.strip()]
    pages, current, count = [], [], 0
    for paragraph in paragraphs:
        current.append(paragraph)
        count += len(paragraph.split())
        if count >= 300:
            pages.append((len(pages) + 1, "\n".join(current)))
            current, count = [], 0
    if current:
        pages.append((len(pages) + 1, "\n".join(current)))
    return source, "part", pages


def chunk_new_document(path):
    """Same steps as index.py: clean, label with a location, chunk (design B settings)."""
    source, label, pages = pages_for(path)
    cleaned = index.clean_pages(pages)
    units = [(f"{label} {number}", number, line) for number, lines in cleaned for line in lines]
    return index.merge_tiny(index.make_chunks(source, units, **index.DESIGNS[DESIGN]))


def do_add_document(path: str) -> str:
    file = Path(path).expanduser()
    if not file.is_absolute():
        file = ROOT / file
    if not file.is_file():
        return f"ERROR: file not found: {path}"
    if file.suffix.lower() not in (".pdf", ".txt", ".md"):
        return "ERROR: only .pdf, .txt and .md files can be added."
    try:
        with contextlib.redirect_stdout(sys.stderr):
            chunks = chunk_new_document(file)
            if not chunks:
                return f"ERROR: no text could be extracted from {file.name}."
            if len(chunks) > MAX_NEW_CHUNKS:
                return (f"ERROR: {file.name} would make {len(chunks)} chunks (limit {MAX_NEW_CHUNKS}); "
                        f"nothing was embedded, to protect the daily embedding quota.")
            old = set(COLLECTION.get(where={"doc": file.name})["ids"])
            new = {c["id"] for c in chunks}
            if old and old == new:
                return f"Already indexed: {file.name} is unchanged ({len(new)} chunks). Nothing was embedded."
            stale = old - new
            if stale:
                COLLECTION.delete(ids=list(stale))
            added = index.embed_and_store(chunks, COLLECTION)
    except Exception as error:  # noqa: BLE001
        return f"ERROR: could not add {path} ({type(error).__name__}: {error})"
    note = f"; {len(stale)} chunks of an older version of the file were removed" if stale else ""
    return f"Indexed {file.name}: {len(chunks)} chunks ({added} newly embedded){note}."


# ---------- the two tools ----------

@mcp.tool()
def search(query: str) -> str:
    """Search the food-safety document collection and return the 5 most relevant passages.

    The collection contains: FDA Food Code 2022 (chapter 2 on management and employee
    health, chapter 3 on food: cooking, holding, cooling and storage rules), the FDA Bad Bug
    Book (bacterial pathogens: symptoms, foods, prevention), the USDA FSIS safe minimum
    internal temperature chart, and any documents added later with add_document.

    Use it for any question about safe temperatures, cooling or holding times, hygiene,
    employee illness or foodborne bacteria. Pass a full question or key phrase. For a
    question with two parts, search once per part.

    Each passage starts with a header: source document, location (Food Code section number,
    bacterium name, or chart), PDF page and a relevance score between 0 and 1. If none of
    the passages answers the question, the collection does not cover it.
    """
    return do_search(query)


@mcp.tool()
def add_document(path: str) -> str:
    """Add a document to the searchable collection. Takes a file path (.pdf, .txt or .md).

    The file is extracted, cleaned, split into chunks with a location label, embedded with
    Gemini (this uses the daily embedding quota) and stored. If the same file is already
    indexed and unchanged, nothing is embedded; if its content changed, the old chunks of
    that file are replaced. Files that would make more than 300 chunks are refused.
    Returns how many chunks were added, or an error message.
    """
    return do_add_document(path)


if __name__ == "__main__":
    mcp.run()  # stdio