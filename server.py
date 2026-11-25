"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): the chunks most relevant to a question, each with the label to cite.
- add_document(path): runs a file through index.py's pipeline (chunk, embed, store).

It loads the committed index at startup and never re-embeds the corpus. Nothing
is printed to stdout, which carries the MCP protocol; logs go to stderr.
"""

import logging
import sys
from pathlib import Path

import index as ix
from retrieval import CHOSEN_CHUNKING, CHOSEN_METHOD, TOP_K, Retriever, format_hits

from mcp.server.mcpserver import MCPServer

logging.basicConfig(stream=sys.stderr, level=logging.WARNING)
log = logging.getLogger("corpus")

mcp = MCPServer("corpus", log_level="WARNING")
retriever = Retriever(CHOSEN_CHUNKING)  # reads index/chroma once, at startup

ALLOWED_SUFFIXES = {".pdf", ".txt", ".md"}


@mcp.tool()
def search(query: str) -> str:
    """Search FDA food-safety documents for passages that answer a question.

    The collection holds the FDA Food Code 2026 (chapters 1-6: definitions; staff
    health, handwashing and hygiene; food receiving, storage, cooking, cooling,
    hot and cold holding, reheating and date marking; equipment and warewashing;
    water and plumbing; physical facilities), FDA's Employee Health and Personal
    Hygiene Handbook (2020) and FDA's guide to cooling cooked TCS foods (2024).

    Use it for any question about food-safety rules in a small restaurant, takeout
    or delivery-only (ghost) kitchen, before answering. Ask about one topic per call; call it again with other words
    if the passages do not answer the question.

    Returns up to 5 passages, best first. Each starts with "Cite as: [label]", for
    example [Food Code 2026 §3-501.17]: copy that label after every fact taken from
    the passage. If no passage answers the question, the documents do not cover it.
    """
    query = query.strip()
    if not query:
        return "Empty query: pass the question or the topic to search for."
    hits = retriever.search(query, CHOSEN_METHOD, TOP_K)
    return format_hits(query, hits)


@mcp.tool()
def add_document(path: str) -> str:
    """Add one document (PDF, .txt or .md file inside this project folder) to the search index.

    The file goes through the same pipeline as the corpus: text extraction,
    cleaning, chunking by section, embedding with Gemini, storage in the index.
    Afterwards `search` finds its passages. Only call this when the user asks to
    add a document; it changes what every later answer is based on.

    If the identical file is already indexed, nothing is changed. If a different
    version of a document with the same file name is indexed, the old version's
    passages are replaced by the new ones, so the two never contradict each other.

    Returns what happened: the document's name, how many passages were added or
    removed, and the citation labels of its first passages.
    """
    file = Path(path).expanduser()
    if not file.is_absolute():
        file = ix.ROOT / file
    file = file.resolve()

    # Only files inside the project: the model chooses this path, and must not be able
    # to read (and send to the embedding API) arbitrary files on the user's computer.
    if not file.is_relative_to(ix.ROOT):
        return f"Refused: {path} is outside the project folder. Copy the file into the project first."
    if not file.is_file():
        return f"Error: no file at {path}."
    if file.suffix.lower() not in ALLOWED_SUFFIXES:
        return f"Error: {file.suffix} files are not supported; use PDF, .txt or .md."

    digest = ix.file_sha256(file)
    collection = retriever.collection
    same_file = collection.get(where={"file_sha256": digest}, include=[])["ids"]
    if same_file:
        return f"Already indexed: {file.name} is in the index with {len(same_file)} passages. Nothing changed."

    chunks = ix.chunk_file(file, CHOSEN_CHUNKING)
    if not chunks:
        return f"Error: no text could be extracted from {file.name} (a scanned PDF?). Nothing changed."
    source = chunks[0]["metadata"]["source"]

    # Same document name, different content: a new version replaces the old one.
    old_version = collection.get(where={"source": source}, include=[])["ids"]
    if old_version:
        collection.delete(ids=old_version)

    embedded = ix.embed_and_store(chunks, collection, {"file_sha256": digest, "added_by": "add_document"})
    retriever.reload()
    log.warning("add_document: %s -> %d chunks", file.name, embedded)

    labels = list(dict.fromkeys(c["metadata"]["cite"] for c in chunks))
    replaced = f" Replaced {len(old_version)} passages of the previous version." if old_version else ""
    return (
        f"Added {file.name}: {len(chunks)} passages ({embedded} embedded).{replaced} "
        f"The index now holds {len(retriever)} passages. "
        f"First citation labels: {', '.join(labels[:6])}"
        + (" ..." if len(labels) > 6 else "")
    )


if __name__ == "__main__":
    mcp.run()  # stdio
