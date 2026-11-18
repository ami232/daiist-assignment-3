"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Loads index/ at startup; never re-embeds the corpus. Prints nothing to stdout
(it carries the protocol); everything is logged to stderr. Docstrings become the
tool descriptions the model reads.
"""

import hashlib
import json
import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer

import index as ix

mcp = MCPServer("corpus", log_level="WARNING")

TOP_K = 5                    # passages returned by search by default
MAX_K = 10
MAX_NEW_CHUNKS = 300         # add_document refuses bigger jobs: ~1,000 embeddings/day on the free tier
MAX_FILE_MB = 20
ALLOWED_SUFFIXES = {".xml", ".pdf", ".txt", ".md"}
QUERY_CACHE = ix.INDEX_DIR / "query_cache.json"   # query text -> vector, so repeat questions cost no quota


def _log(message: str) -> None:
    print(message, file=sys.stderr)


def _load_cache() -> dict:
    try:
        return json.loads(QUERY_CACHE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def embed_query(query: str) -> list[float]:
    """Embed a search query, reusing a saved vector when we have seen the exact text before."""
    key = hashlib.sha1(query.encode("utf-8")).hexdigest()
    cache = _load_cache()
    if key not in cache:
        cache[key] = [round(x, 6) for x in ix.embed_texts([query], query=True)[0]]
        try:
            QUERY_CACHE.write_text(json.dumps(cache), encoding="utf-8")
        except OSError as error:
            _log(f"could not save query cache: {error}")
    return cache[key]


def format_results(documents, metadatas, distances) -> str:
    blocks = []
    for n, (doc, meta, dist) in enumerate(zip(documents, metadatas, distances), 1):
        section = f" | {meta['section']}" if meta.get("section") else ""
        blocks.append(
            f"[{n}] CITATION: [{meta['source']}, {meta['location']}]  "
            f"(similarity {1 - dist:.2f}{section})\n{doc}"
        )
    return "\n\n".join(blocks)


@mcp.tool()
def search(query: str, k: int = TOP_K) -> str:
    """Search the indexed Spanish rental and tourist-rental law: the Ley de Arrendamientos Urbanos (LAU),
    Ley 12/2023 por el derecho a la vivienda, the Ley de Propiedad Horizontal (LPH), RDL 7/2019, and the
    Valencian tourism law (Ley 15/2018 CV), plus any document added with add_document.

    Use it for any question about these laws: lease duration, rent, deposits, tourist housing, community
    of owners rules, stressed housing zones, fines. Write the query in Spanish, as a short topical phrase
    or question. Returns up to k passages (default 5, max 10), best first. Each starts with a
    CITATION: [source, location] that must be quoted when you use the passage, then similarity (0 to 1,
    higher is closer) and the legal text. If no passage answers the question, the corpus does not cover it.
    """
    query = query.strip()
    if not query:
        raise ValueError("query is empty")
    col = ix.get_collection(ix.DEFAULT_DESIGN)
    if col.count() == 0:
        raise RuntimeError("The index is empty. Run `uv run python main.py index` first.")
    res = col.query(
        query_embeddings=[embed_query(query)],
        n_results=min(max(int(k), 1), MAX_K),
        include=["documents", "metadatas", "distances"],
    )
    return format_results(res["documents"][0], res["metadatas"][0], res["distances"][0])


@mcp.tool()
def add_document(path: str) -> str:
    """Add one document to the searchable index: reads the file at `path` (a BOE .xml law, a .pdf, .txt or .md),
    cleans and chunks it with the same pipeline as the rest of the corpus, embeds the chunks and stores them.
    Every chunk keeps its source and location, so search can cite it afterwards.

    If the document is already indexed and unchanged, nothing is embedded and it says so. If it was indexed
    before but its text changed, the new chunks are added and the outdated ones of that source are removed.
    Refuses files over 20 MB or jobs of more than 300 new chunks (embedding quota). Returns a short report
    with the source name and how many chunks were added. Only use when the user asks to add a document.
    """
    file = Path(path).expanduser()
    if not file.is_absolute():
        file = ix.ROOT / file
    if not file.is_file():
        raise ValueError(f"File not found: {path}")
    if file.suffix.lower() not in ALLOWED_SUFFIXES:
        raise ValueError(f"Unsupported file type {file.suffix!r}; use one of {sorted(ALLOWED_SUFFIXES)}")
    if file.stat().st_size > MAX_FILE_MB * 1_000_000:
        raise ValueError(f"File is larger than {MAX_FILE_MB} MB")

    chunks = ix.chunk_file(file)
    if not chunks:
        raise ValueError("No text could be extracted from this file")
    source = chunks[0]["meta"]["source"]

    col = ix.get_collection(ix.DEFAULT_DESIGN)
    stored = set(col.get(ids=[c["id"] for c in chunks], include=[])["ids"])
    new = len(chunks) - len(stored)
    if new > MAX_NEW_CHUNKS:
        raise ValueError(f"{source} would need {new} new embeddings (limit {MAX_NEW_CHUNKS} per call) "
                         "to protect the daily quota. Split the file or run `main.py index`.")

    result = ix.embed_and_store(chunks)
    if result["new"] == 0 and result["removed"] == 0:
        return f"'{source}' was already indexed and is unchanged ({len(chunks)} chunks): nothing was added."
    _log(f"add_document: {source} {result}")
    return (f"Indexed '{source}' from {file.name}: {result['new']} new chunks embedded, "
            f"{result['existing']} already stored, {result['removed']} outdated chunks removed. "
            f"search can now cite it as [{source}, <location>].")


if __name__ == "__main__":
    mcp.run()  # stdio