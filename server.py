"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Load index/ at startup; never re-embed the corpus. Print nothing to stdout
(it carries the protocol); log to stderr. Docstrings become the tool
descriptions the model reads.
"""

import sys
from datetime import date
from pathlib import Path

from mcp.server.mcpserver import MCPServer

import index as ix
from retrieval import Retriever, format_results

mcp = MCPServer("corpus", log_level="WARNING")
retriever = Retriever()          # loads index/ once; the corpus is never re-embedded
print(f"server: {len(retriever.chunks)} chunks loaded ({retriever.design} design)", file=sys.stderr)

ALLOWED_SUFFIXES = {".pdf", ".txt", ".md"}


@mcp.tool()
def search(query: str, k: int = 5) -> str:
    """Search the Spanish housing-law corpus: Ley 29/1994 de Arrendamientos Urbanos (LAU, rental
    contracts), Ley 12/2023 por el derecho a la vivienda (rent limits, tense housing areas,
    large landlords) and Ley 49/1960 de Propiedad Horizontal (apartment-building communities),
    plus any document added with add_document.

    Use it for ANY question about rental contracts, deposits, rent updates, ending a lease or
    community rules, before answering. Write the query in Spanish, in the words of the law.
    Returns up to k passages (default 5), each headed by a citation like [LAU, Artículo 9]
    with pages and a similarity score. Passages are the only valid evidence: if none answers
    the question, the corpus does not cover it.
    """
    k = max(1, min(int(k), 10))
    return format_results(retriever.search(query, k=k))


@mcp.tool()
def add_document(path: str) -> str:
    """Add a document (.pdf, .txt or .md file on this machine) to the searchable corpus.

    It runs the same pipeline as the original corpus: extract, clean, chunk by article, embed
    and store. If the exact same file is already indexed nothing changes and it says so. If a
    different file with the same name is indexed, it refuses: rename the file first. Costs
    embedding quota, so call it only when the user explicitly asks to add a document.
    Returns how many passages were added, or the reason nothing was.
    """
    file = Path(path).expanduser()
    if not file.is_file():
        return f"Not added: {path} is not a file."
    if file.suffix.lower() not in ALLOWED_SUFFIXES:
        return f"Not added: only {', '.join(sorted(ALLOWED_SUFFIXES))} files are supported."

    digest = ix.file_sha256(file)
    documents = ix.load_manifest()["documents"]
    if any(d["sha256"] == digest for d in documents):
        return f"Already indexed: {file.name} has the same content as an indexed document. Nothing changed."
    doc = ix.doc_info(file)
    if any(d["source"] == doc["source"] for d in documents):
        return (f"Not added: a different document named {doc['source']} is already indexed. "
                f"Rename {file.name} and try again.")

    design = retriever.design
    chunks = ix.chunk_file(file, design, doc)
    if not chunks:
        return f"Not added: no text could be extracted from {file.name}."
    for chunk in chunks:
        chunk["downloaded"] = date.today().isoformat()
    ix.embed_and_store(chunks)
    saved = ix.load_vectors()
    if any(c["key"] not in saved for c in chunks):
        return "Not added: embedding quota reached before the document was complete. Try again later."
    ix.register_chunks({**doc, "file": file.name, "sha256": digest,
                        "downloaded": date.today().isoformat()}, {design: chunks})
    retriever.load()
    return f"Added {file.name} as source '{doc['source']}': {len(chunks)} passages indexed ({design} design)."


if __name__ == "__main__":
    mcp.run()  # stdio
