"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Loads the committed index/ at startup and never re-embeds the corpus. Nothing
is printed to stdout (it carries the protocol); logs go to stderr.
"""

from __future__ import annotations

import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer

import index as ix
import retrieval

mcp = MCPServer("corpus", log_level="WARNING")


@mcp.tool()
def search(query: str) -> str:
    """Search the binding text of three EU laws: the GDPR (Regulation 2016/679), the AI Act
    (Regulation 2024/1689) and the ePrivacy Directive (2002/58/EC as amended in 2009, cookies
    and electronic marketing). Use it for any question about obligations, definitions, rights,
    deadlines, fines or exemptions under these laws, and search again with other words if the
    first results do not answer the question. Recitals and national laws are not included.

    Returns the 5 most relevant passages, each with a citation tag such as [GDPR, Article 33]
    to copy into the answer, the law's full title and URL, and a relevance score.
    """
    query = (query or "").strip()
    if not query:
        return "Error: give a non-empty query."
    hits = retrieval.search(query)
    return retrieval.format_hits(hits)


@mcp.tool()
def add_document(path: str) -> str:
    """Add one document to the searchable index: a .pdf, .html/.xhtml (EU acts from EUR-Lex are
    split by article), .txt or .md file given by its path on this machine, absolute or relative
    to the project folder. The text is extracted, chunked and embedded like the rest of the corpus,
    and its file name becomes the source name used in citations.

    If the same file content is already indexed, nothing is embedded. If a document with the
    same name but different content is indexed, its old chunks are replaced. Returns the source
    name, how many chunks were added and an example citation tag.
    """
    file = Path(path).expanduser()
    if not file.is_absolute():
        file = (ix.ROOT / file).resolve()
    if not file.is_file():
        return f"Error: no file at {file}."
    try:
        doc = ix.load_document(file, added=True)
    except ValueError as error:
        return f"Error: {error}"

    design = ix.chosen_design()["design"]
    col = ix.collection(design)

    same = col.get(where={"doc_hash": doc.doc_hash}, include=["metadatas"])
    if same["ids"]:
        name = same["metadatas"][0]["source"]
        return (f"Already indexed: this exact file is in the index as '{name}' "
                f"({len(same['ids'])} chunks). Nothing was embedded.")

    existing = col.get(where={"source": doc.source}, include=["metadatas"])
    if existing["ids"] and not existing["metadatas"][0].get("added"):
        doc.source = f"{doc.source} (added)"   # never overwrite one of the three base laws
        existing = col.get(where={"source": doc.source}, include=["metadatas"])
    replaced = len(existing["ids"])
    if replaced:
        col.delete(ids=existing["ids"])

    chunks = ix.chunk_document(doc, design)
    try:
        embedded = ix.embed_and_store(chunks, design)
    except ix.QuotaExhausted:
        retrieval.invalidate(design)
        return "Error: the daily embedding quota is used up; part of the document may be indexed. Try again tomorrow."
    retrieval.invalidate(design)
    print(f"add_document: {doc.source}: {len(chunks)} chunks, {embedded} embedded, {replaced} replaced", file=sys.stderr)

    action = f"Replaced the previous version ({replaced} chunks). " if replaced else ""
    example = retrieval.citation(chunks[0].metadata) if chunks else ""
    return (f"{action}Indexed '{doc.source}': {len(doc.sections)} sections, {len(chunks)} chunks, "
            f"{embedded} newly embedded. Its passages are cited like {example}.")


if __name__ == "__main__":
    mcp.run()  # stdio
