"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

The server only READS the index that is already committed in index/ (it never
re-embeds the corpus). Embedding happens for the search query (1 text) and for
the new chunks of add_document. stdout carries the protocol, so everything we
print goes to stderr (index.log does that).

Which chunking design is searched: env CORPUS_DESIGN (default below = the
design chosen in REPORT.md). How many chunks search returns: env TOP_K.
"""

import os
from pathlib import Path

from mcp.server.mcpserver import MCPServer

from index import (ROOT, DailyQuotaError, chunk_file, embed_and_store,
                   embed_query, get_collection)

DESIGN = os.environ.get("CORPUS_DESIGN", "fixed")
TOP_K = int(os.environ.get("TOP_K", "5"))

mcp = MCPServer("corpus", log_level="WARNING")


@mcp.tool()
def search(query: str) -> str:
    """Search the EU digital-law corpus and return the most relevant passages.

    The corpus is the articles of three EU regulations: the AI Act (Regulation
    (EU) 2024/1689), the GDPR (Regulation (EU) 2016/679) and the Data Act
    (Regulation (EU) 2023/2854), plus any document added with add_document.
    Use it for every question about what these laws require, allow, forbid or
    fine. Write the query as the wording the law itself would use (for example
    "notification of a personal data breach to the supervisory authority"),
    not as a chat message. A question that involves two laws needs one search
    per law.

    Returns up to 5 passages, best first. Each has its source, location
    (article number and paragraphs), title and the exact text, so every claim
    can be cited as source + location. Passages are only the closest matches:
    check that they really answer the question. If none does, the corpus does
    not cover it and you should say so instead of guessing.
    """
    query = (query or "").strip()
    if not query:
        return "Error: the query is empty. Pass the topic to look up."
    try:
        col = get_collection(DESIGN)
        if col.count() == 0:
            return f"Error: the index for design '{DESIGN}' is empty. Run `main.py index` first."
        res = col.query(
            query_embeddings=[embed_query(query)], n_results=TOP_K,
            include=["metadatas", "documents", "distances"],
        )
    except DailyQuotaError:
        return "Error: the embedding quota is used up for today, search is unavailable until it resets."
    except Exception as e:  # report to the model instead of crashing the server
        return f"Error: search failed ({type(e).__name__}: {e})."
    if not res["ids"][0]:
        return "No passages found."
    parts = []
    for i, (meta, text, dist) in enumerate(zip(res["metadatas"][0], res["documents"][0], res["distances"][0]), 1):
        parts.append(
            f"[{i}] {meta['source']} | {meta['location']} | {meta['title']} (distance {dist:.2f})\n{text}"
        )
    return "\n\n".join(parts)


@mcp.tool()
def add_document(path: str) -> str:
    """Add a document to the searchable corpus, then it can be found with search.

    Pass the path of an EUR-Lex HTML file inside this project (for example
    "corpus/ai_act.html"). The file goes through the same pipeline as the
    original corpus: it is parsed (articles and annexes), cleaned, split into
    chunks with source and location, embedded and stored. This costs embedding
    quota and changes the index, so only call it when the user asks to add
    a document or when you need a document that is not yet searchable.

    If the document, or part of it, is already indexed, those chunks are
    skipped and not embedded again; adding the same file twice changes nothing.
    Returns how many chunks were new and how many were already there, or an
    error message (file not found, outside the project, no chunks found).
    """
    p = Path(path)
    p = (p if p.is_absolute() else ROOT / p).resolve()
    if ROOT.resolve() not in p.parents:
        return f"Error: {path} is outside the project folder; only files inside it can be added."
    if not p.is_file():
        return f"Error: file not found: {path}"
    try:
        chunks = chunk_file(p, DESIGN, include_annexes=True)
    except Exception as e:
        return f"Error: could not read {path} ({type(e).__name__}: {e})."
    if not chunks:
        return f"Error: no articles or annexes found in {path}; nothing was added."
    col = get_collection(DESIGN)
    before = col.count()
    try:
        embed_and_store(chunks, DESIGN)
    except DailyQuotaError:
        return "Error: the embedding quota is used up for today; the document was only partly added. Run it again later."
    except Exception as e:
        return f"Error: adding failed ({type(e).__name__}: {e})."
    new = col.count() - before
    source = chunks[0]["source"]
    if new == 0:
        return f"{p.name} was already indexed: all {len(chunks)} chunks of '{source}' exist, nothing added."
    return (f"Added {new} new chunks from {p.name} (source '{source}'); "
            f"{len(chunks) - new} of its {len(chunks)} chunks were already indexed. Index now holds {col.count()} chunks.")


if __name__ == "__main__":
    mcp.run()  # stdio
