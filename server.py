"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

Two tools:
- search(query): the 5 most similar chunks, each with its source and location.
- add_document(path): runs a file through index.py's pipeline and stores it.

It loads the saved index; it never re-embeds the corpus (only the query, and
query vectors are cached in index/query_cache.json). Logs go to stderr,
because stdout carries the MCP protocol.
"""

import json
import os
from pathlib import Path

from mcp.server.mcpserver import MCPServer

import index  # the same pipeline as `main.py index`

TOP_K = 5
QUERY_CACHE = index.INDEX_DIR / "query_cache.json"

mcp = MCPServer("corpus", log_level="WARNING")


def embed_query(query: str) -> list[float]:
    """Embed a query once; afterwards read it from the cache (saves free-tier quota)."""
    try:
        cache = json.loads(QUERY_CACHE.read_text(encoding="utf-8")) if QUERY_CACHE.exists() else {}
    except (json.JSONDecodeError, OSError):   # e.g. another server process is writing it right now
        cache = {}
    if query not in cache:
        vector = index.embed_texts([query])[0]
        cache[query] = vector
        # write to a temporary file, then swap it in: a reader never sees a half-written file
        tmp = QUERY_CACHE.with_suffix(f".{os.getpid()}.tmp")
        tmp.write_text(json.dumps(cache), encoding="utf-8")
        try:
            os.replace(tmp, QUERY_CACHE)
        except OSError:
            tmp.unlink(missing_ok=True)
        return vector
    return cache[query]


def retrieve(query: str, design: str = index.CHOSEN_DESIGN, k: int = TOP_K) -> list[dict]:
    """Return the k chunks most similar to the query (cosine similarity)."""
    collection = index.get_collection(design)
    result = collection.query(query_embeddings=[embed_query(query)], n_results=k)
    return [
        {"id": id_, "text": text, "score": round(1 - distance, 3), **meta}
        for id_, text, meta, distance in zip(result["ids"][0], result["documents"][0],
                                             result["metadatas"][0], result["distances"][0])
    ]


def format_results(chunks: list[dict]) -> str:
    return "\n\n".join(
        f"[{i}] [{c['source']}, {c['location']}] (similarity {c['score']})\n{c['text']}"
        for i, c in enumerate(chunks, start=1)
    )


@mcp.tool()
def search(query: str) -> str:
    """Search EU passenger-rights law: air (Regulation 261/2004: denied boarding,
    cancellation, delay), rail (2021/782), bus and coach (181/2011), sea and inland
    waterways (1177/2010) and package travel (Directive 2015/2302).

    Use it for any question about compensation, refunds, re-routing, assistance,
    complaints or the rights of disabled passengers on these modes of transport.
    Write the query in English with the key terms (e.g. "train delay compensation percentage").

    Returns the 5 most relevant passages. Each starts with its citation
    [source, location], e.g. [air-261-2004, Article 7]; cite it exactly like that.
    """
    index.log(f"search: {query!r}")
    return format_results(retrieve(query))


@mcp.tool()
def add_document(path: str) -> str:
    """Add a document (.html or .txt file on this computer) to the passenger-rights index.

    The file is cleaned, split into chunks by article, embedded and stored, so
    `search` can find it. The file name (without extension, lower case, dashes for
    spaces) becomes its source name. If the same file is already indexed nothing is
    done (an interrupted earlier run is completed); if a file with the same name but
    different content is indexed, the old version is replaced.
    Returns how many chunks were added.
    """
    file = Path(path).expanduser().resolve()
    if not file.is_file():
        return f"Error: no file at {file}."
    if file.suffix.lower() not in (".html", ".htm", ".txt"):
        return "Error: only .html and .txt files are supported."

    chunks = index.chunk_file(file)
    source = chunks[0]["source"] if chunks else file.stem
    if not chunks:
        return f"Error: no text found in {file.name}."

    collection = index.get_collection(index.CHOSEN_DESIGN)
    old = collection.get(where={"source": source})
    if old["ids"]:
        if old["metadatas"][0].get("file_hash") == chunks[0]["file_hash"]:
            # Same file. If an earlier call stopped half-way (e.g. rate limit), finish it:
            # embed_and_store only embeds the chunks that have no vector yet.
            missing = index.embed_and_store(chunks, index.CHOSEN_DESIGN)
            if missing:
                return f"'{source}' was partly indexed: {missing} missing chunks embedded and stored."
            return f"'{source}' is already indexed ({len(old['ids'])} chunks). Nothing was changed."
        collection.delete(ids=old["ids"])   # same name, new content: replace the old version
        index.log(f"replaced old version of {source}")

    added = index.embed_and_store(chunks, index.CHOSEN_DESIGN)
    return f"Added '{source}': {added} chunks embedded and stored. It can now be searched."


if __name__ == "__main__":
    mcp.run()  # stdio
