"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Load index/ at startup; never re-embed the corpus. Print nothing to stdout
(it carries the protocol); log to stderr. Docstrings become the tool
descriptions the model reads.
"""

import json
import os
import sys
from pathlib import Path

os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")  # keep chromadb quiet

from mcp.server.mcpserver import MCPServer

from index import INDEX_DIR, embed_texts, get_collection, index_file

ROOT = Path(__file__).resolve().parent
TOP_K = 5
QUERY_CACHE = INDEX_DIR / "query_cache.json"

mcp = MCPServer("corpus", log_level="WARNING")
collection = get_collection()


def embed_query(query: str) -> list[float]:
    """Embed a search query, reusing a saved vector for a query seen before (saves quota)."""
    cache = json.loads(QUERY_CACHE.read_text(encoding="utf-8")) if QUERY_CACHE.is_file() else {}
    if query not in cache:
        cache[query] = embed_texts([query], task_type="RETRIEVAL_QUERY")[0]
        QUERY_CACHE.write_text(json.dumps(cache), encoding="utf-8")
    return cache[query]


def retrieve(query: str, k: int = TOP_K) -> list[dict]:
    """The k chunks closest to the query, best first, as {text, metadata, distance}."""
    result = collection.query(query_embeddings=[embed_query(query)], n_results=k,
                              include=["documents", "metadatas", "distances"])
    return [{"text": t, "metadata": m, "distance": d}
            for t, m, d in zip(result["documents"][0], result["metadatas"][0], result["distances"][0])]


@mcp.tool()
def search(query: str) -> str:
    """Search FDA drug labels (openFDA) for passages that answer a pharmacy question.

    The corpus holds the labels of: Flanax, Aleve and prescription naproxen
    (naproxen), Advil (ibuprofen), Celebrex (celecoxib), Tylenol
    (acetaminophen), Jantoven (warfarin), Plavix (clopidogrel), Amoxil
    (amoxicillin), Augmentin (amoxicillin/clavulanate), Zithromax
    (azithromycin), Cipro (ciprofloxacin), Bactrim
    (sulfamethoxazole/trimethoprim) and Prilosec (omeprazole), plus any label
    added later. Use it for dosing, contraindications, warnings, interactions,
    special populations and counseling points. Name the drug (brand or active
    ingredient) in the query; for a question about two drugs, search each one.

    Returns the 5 most relevant passages, each headed by its citation
    [source, location] (label file and label section) and the product name.
    """
    hits = retrieve(query)
    if not hits:
        return "No passages found."
    return "\n\n".join(
        f"[{h['metadata']['source']}, {h['metadata']['location']}] "
        f"{h['metadata']['brand']} ({h['metadata']['generic']})\n{h['text']}"
        for h in hits
    )


@mcp.tool()
def add_document(path: str) -> str:
    """Add an FDA drug label to the corpus so search can find it.

    Takes the path of an openFDA drug label JSON file (as saved by
    download.py, e.g. corpus/held_back/eliquis.json), chunks it by label
    section, embeds the chunks and stores them in the index. If the label is
    already indexed, unchanged chunks are kept and only new or changed ones
    are embedded. Returns how many chunks were added, reused and removed.
    """
    # Already indexed: never store duplicates. index_file keeps unchanged chunks (same id
    # and hash) with their saved vectors, embeds only new or changed ones, and deletes
    # chunks the new version no longer has; adding the same file twice changes nothing.
    file = (ROOT / path).resolve() if not Path(path).is_absolute() else Path(path)
    if not file.is_file():
        return f"No file at {path}."
    if file.suffix != ".json":
        return f"{path} is not an openFDA label JSON file."
    try:
        result = index_file(file, collection)
    except (json.JSONDecodeError, KeyError) as error:
        return f"Could not read {path} as an openFDA label: {error}"
    print(f"add_document: {result}", file=sys.stderr)
    return (f"Indexed {result['source']}: {result['chunks']} chunks "
            f"({result['embedded']} embedded, {result['reused']} already indexed, {result['deleted']} removed).")


if __name__ == "__main__":
    mcp.run()  # stdio
