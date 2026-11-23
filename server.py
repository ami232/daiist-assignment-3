"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it and stores it.

Loads index/ at startup and never re-embeds the corpus. Logs go to stderr only:
stdout carries the MCP protocol.
"""

import logging
import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer

import index as ix
import retrieval

logging.basicConfig(stream=sys.stderr, level=logging.WARNING)
mcp = MCPServer("corpus", log_level="WARNING")
searcher = retrieval.get_searcher()  # loads the committed index once
ALLOWED_SUFFIXES = {".xhtml", ".html"}


def format_results(hits: list[dict]) -> str:
    blocks = []
    for n, hit in enumerate(hits, 1):
        blocks.append(
            f"[{n}] {hit['source']} | {hit['location']} (similarity {hit['score']:.2f})\n{hit['text']}"
        )
    return "\n\n".join(blocks)


@mcp.tool()
def search(query: str) -> str:
    """Search the course texts for A-level Politics (political ideas) and return the 5 most relevant passages.

    The corpus holds primary texts only: Hobbes, Leviathan (1651), chapters XIII-XXI;
    Locke, Second Treatise of Government (1689), all chapters; Mill, On Liberty (1859),
    all chapters; plus any document added later with add_document. It has no commentary,
    biography or other authors.

    Use it before answering any question about these authors or ideas (state of nature,
    social contract, sovereignty, consent, property, liberty, harm principle...).
    Name the author in the query; to compare authors, search each author separately.

    Returns numbered passages, each headed by its citation:
    "[n] <author, work (year)> | Chapter <roman>: <title>, ¶<paragraph(s)> (similarity 0-1)"
    followed by the exact text. Quote only from this text and cite it as shown. A low
    similarity (below about 0.65) usually means the corpus does not cover the question.
    """
    query = query.strip()
    if not query:
        return "Empty query: give a question or keywords to search for."
    return format_results(searcher.search(query))


@mcp.tool()
def add_document(path: str) -> str:
    """Add a document to the searchable corpus: extract, chunk, embed and store it, then make it searchable.

    `path` must be an existing .xhtml or .html file inside the project's corpus/ folder,
    in Standard Ebooks format (chapters as <section> elements); its <title> becomes the
    citation. It uses the same pipeline as `main.py index`.

    If the document is already indexed with the same content, nothing is embedded and it
    says so. If its content changed, only the new or changed chunks are embedded and
    outdated ones are removed, so there are never duplicates. Embedding spends the daily
    Gemini quota, so only call this when the user asks for a document to be added.

    Returns a short report: the citation, chunks added, removed, already present.
    """
    file = Path(path).expanduser()
    if not file.is_absolute():
        file = ix.ROOT / file
    file = file.resolve()
    if not file.is_relative_to(ix.CORPUS_DIR.resolve()):
        return f"Refused: {path} is outside the corpus/ folder. Put the file in corpus/ first."
    if file.suffix.lower() not in ALLOWED_SUFFIXES:
        return f"Refused: {file.name} is not an .xhtml or .html file."
    if not file.is_file():
        return f"Not found: {file.relative_to(ix.ROOT)} does not exist."

    doc_id, source, chapters = ix.describe_file(file)
    chunks = ix.chunk_file(file, doc_id, source, chapters)
    if not chunks:
        return f"No text found in {file.name}: it has no chapter <section> with paragraphs."

    collection = searcher.collection
    already = len(collection.get(ids=[c.id for c in chunks], include=[])["ids"])
    removed = ix.prune(chunks, collection)
    try:
        added = ix.embed_and_store(chunks, collection)
    except ix.QuotaExhausted:
        searcher.refresh()
        return "Stopped: the daily embedding quota is used up. Chunks saved so far are kept; try again after 09:00 (Spain)."
    searcher.refresh()

    if added == 0 and removed == 0:
        return f"Already indexed: {source} ({len(chunks)} chunks). Nothing was embedded."
    return (
        f"Indexed {source} from {file.name}: {added} chunks embedded and added, "
        f"{already} already present, {removed} outdated chunks removed. "
        f"The corpus now has {collection.count()} chunks."
    )


if __name__ == "__main__":
    mcp.run()  # stdio
