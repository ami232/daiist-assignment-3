"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Loads the committed index/ at startup and never re-embeds the corpus: only the
query is embedded (one embedding per search). Prints nothing to stdout (it
carries the MCP protocol); logs go to stderr. Docstrings become the tool
descriptions the model reads.
"""

import os
import sys
from pathlib import Path

os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")  # keep ChromaDB quiet on stdout

from mcp.server.mcpserver import MCPServer

import index

ROOT = Path(__file__).resolve().parent
TOP_K = 5  # chunks returned per search; chosen from eval/summary.md (hit@5 vs hit@3, multi questions)

mcp = MCPServer("corpus", log_level="WARNING")

# Open the saved index once at startup (no embedding happens here).
_collection = index.collection(index.CHOSEN_DESIGN)
print(f"corpus server: loaded {_collection.count()} chunks ({index.CHOSEN_DESIGN} design)", file=sys.stderr)


def format_results(results: list[dict]) -> str:
    blocks = []
    for n, r in enumerate(results, 1):
        body = r["text"].split("\n", 1)[1] if r["text"].startswith("[") else r["text"]
        blocks.append(
            f"--- Result {n} | cite as [{r['source']}, {r['location']}] | similarity {r['score']}\n"
            f"Document: {r['title']}\n{body}"
        )
    return "\n\n".join(blocks)


@mcp.tool()
def search(query: str) -> str:
    """Search EU food-labelling law and the European Commission's official guidance on it.

    The corpus holds six documents: Regulation (EU) No 1169/2011 on food information
    to consumers (labelling, allergens, ingredients list, nutrition declaration, QUID,
    legibility), Regulation (EC) No 1924/2006 on nutrition and health claims,
    Regulation (EU) No 432/2012 (list of permitted health claims and their conditions),
    and Commission guidance notices on 1169/2011 (Q&A, 2018), on allergen labelling
    (2017) and on quantitative ingredient declaration, QUID (2017).

    Use it for any question about what a food label in the EU must, may or may not
    say. Write the query as a specific question or key terms (e.g. "allergen emphasis
    in the list of ingredients"). Search again with other words if the results do not
    answer the question, and once per part of a question with several parts.

    Returns the 5 most similar passages, each with a citation label
    [SOURCE, location] (an Article, Annex or guidance Section) and a similarity
    score. Cite that label for every claim. If no passage answers the question, the
    corpus does not cover it: say so instead of answering from memory.
    """
    query = (query or "").strip()
    if not query:
        return "Empty query: pass a question or key terms to search for."
    return format_results(index.search(query, k=TOP_K, design=index.CHOSEN_DESIGN))


@mcp.tool()
def add_document(path: str) -> str:
    """Add one document to the food-labelling corpus so that search can find it.

    `path` is a file on this machine (.html, .pdf, .txt or .md), absolute or relative
    to the project folder. The file is extracted, cleaned and chunked with the same
    pipeline as the rest of the corpus (index.py), each chunk is embedded with Gemini
    (this spends embedding quota) and stored in the index with its source and
    location (Article/Section for EUR-Lex pages, Page for PDFs).

    If the same file is already indexed with the same content, nothing is embedded.
    If a file with the same name was indexed before with different content, its old
    chunks are replaced. Returns the document's source id and how many chunks were
    added, kept or replaced. Only use it when the user asks to add a document.
    """
    file = Path(path).expanduser()
    if not file.is_absolute():
        file = (ROOT / file).resolve()
    if not file.is_file():
        return f"Not added: no file at {file}."
    try:
        chunks = index.chunk_file(file, design=index.CHOSEN_DESIGN)
    except ValueError as error:
        return f"Not added: {error}"
    if not chunks:
        return f"Not added: no text could be extracted from {file.name}."

    source = chunks[0]["metadata"]["source"]
    ids = {c["id"] for c in chunks}
    already = set(_collection.get(ids=list(ids), include=[])["ids"])
    if already == ids:
        return f"{source} is already indexed with the same content ({len(ids)} chunks). Nothing was embedded."

    replaced = index.remove_stale(source, ids, index.CHOSEN_DESIGN)
    try:
        added = index.embed_and_store(chunks, index.CHOSEN_DESIGN)
    except index.DailyQuotaExceeded:
        return (f"Partly added {source}: the daily embedding quota ran out. The chunks embedded so far "
                f"are saved; call add_document again tomorrow to finish.")
    locations = sorted({c["metadata"]["location"].split(" (part")[0] for c in chunks})
    shown = ", ".join(locations[:6]) + (" ..." if len(locations) > 6 else "")
    return (f"Added {source} from {file.name}: {added} new chunks embedded, {len(chunks) - added} kept, "
            f"{replaced} outdated chunks removed. Locations: {shown}. Cite it as [{source}, <location>].")


if __name__ == "__main__":
    mcp.run()  # stdio
