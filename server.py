"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns the most relevant chunks with source, page and section.
- add_document(path): runs a PDF through index.py's pipeline, embeds the new chunks and stores them.

Loads the saved vectors in index/ and never re-embeds the corpus: only the
query is embedded. stdout carries the MCP protocol, so everything else goes
to stderr.
"""

import contextlib
import logging
import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer

import index

DESIGN = "structured"   # the chunking design the server searches (chosen in evaluate.py)
TOP_K = 5               # chunks returned per search

logging.basicConfig(stream=sys.stderr, level=logging.INFO, format="%(asctime)s %(message)s")
log = logging.getLogger("corpus")

mcp = MCPServer("corpus", log_level="WARNING")


def citation(meta: dict) -> str:
    """The label the agent must copy into its answer, e.g. [eliquis p.4 SmPC 4.2]."""
    first_location = meta["location"].split(", ")[0]
    return f"[{meta['source']} p.{meta['page']} {first_location}]"


def search_chunks(query: str, k: int = TOP_K, design: str = DESIGN) -> list[dict]:
    """Top-k chunks for a query: [{citation, source, page, location, text, distance}]. evaluate.py uses this too."""
    vector = index.embed_query(query)
    result = index.collection(design).query(query_embeddings=[vector], n_results=k,
                                            include=["documents", "metadatas", "distances"])
    return [{"citation": citation(meta), "source": meta["source"], "page": meta["page"],
             "location": meta["location"], "text": text, "distance": round(dist, 3)}
            for text, meta, dist in zip(result["documents"][0], result["metadatas"][0], result["distances"][0])]


@mcp.tool()
def search(query: str) -> str:
    """Search the official EMA product information (SmPC and patient leaflet) of the
    anticoagulants in the corpus: Eliquis (apixaban), Xarelto (rivaroxaban) and Pradaxa
    (dabigatran), plus any document added later.

    Use it for any question about these medicines: doses, missed doses, kidney or liver
    problems, contraindications, interactions, pregnancy, side effects, overdose, storage.
    Search once per medicine or topic; rephrase and search again if the results miss.

    Returns the 5 most relevant passages. Each starts with a citation such as
    [eliquis p.4 SmPC 4.2] (document, page, section); cite it after every claim.
    If no passage answers the question, the corpus does not cover it: say so.
    """
    log.info("search: %s", query)
    hits = search_chunks(query)
    return "\n\n".join(f"{h['citation']} (distance {h['distance']})\n{h['text']}" for h in hits)


@mcp.tool()
def add_document(path: str) -> str:
    """Add a PDF of product information (e.g. an EMA SmPC/leaflet) to the searchable corpus.

    Takes the path of a local PDF file. The file goes through the same pipeline as the
    corpus (extract, clean, find sections, remove duplicates, chunk), and only chunks that
    are not stored yet are embedded. The document name is the file name without .pdf.

    If the same document is already indexed and unchanged, nothing is embedded. If a file
    with the same name has changed, its old chunks are replaced by the new ones.
    Returns what was added. Changes the index: only call it when the user asks.
    """
    file = Path(path).expanduser().resolve()
    if not file.is_file():
        return f"Not added: no file at {file}."
    if file.suffix.lower() != ".pdf":
        return f"Not added: {file.name} is not a PDF."
    with contextlib.redirect_stdout(sys.stderr):        # index.py prints progress; keep stdout clean
        chunks = index.chunk_file(file, DESIGN)
        if not chunks:
            return f"Not added: no text could be extracted from {file.name}."
        removed = index.remove_stale(chunks, DESIGN, {file.stem.lower()})
        try:
            new = index.embed_and_store(chunks, DESIGN)
        except index.QuotaExhausted:
            return "Stopped: the daily embedding quota is used up. Chunks saved so far are kept; try again tomorrow."
    source = file.stem.lower()
    if new == 0 and removed == 0:
        return f"'{source}' is already indexed and unchanged ({len(chunks)} chunks). Nothing was embedded."
    action = "updated" if removed else "added"
    log.info("add_document: %s %s, %d new, %d removed", source, action, new, removed)
    return (f"'{source}' {action}: {len(chunks)} chunks, {new} newly embedded"
            + (f", {removed} old chunks removed" if removed else "") + ". It can now be searched.")


if __name__ == "__main__":
    mcp.run()  # stdio