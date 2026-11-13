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
import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer

import index as ix

# Winning chunking design, chosen from the hit-rate numbers in `main.py evaluate`.
DESIGN = "article"
TOP_K = 5
ALLOWED_SUFFIXES = {".xml", ".pdf", ".txt", ".md", ".html", ".htm"}
QUERY_CACHE = ix.INDEX_DIR / "query_cache.json"

mcp = MCPServer("corpus", log_level="WARNING")


def log(*a):
    print(*a, file=sys.stderr, flush=True)


def _load_cache() -> dict:
    try:
        return json.loads(QUERY_CACHE.read_text(encoding="utf-8"))
    except Exception:
        return {}


def query_vector(query: str) -> list[float]:
    """Embed a query, remembering it on disk so a repeated query costs nothing."""
    cache = _load_cache()
    if query not in cache:
        cache[query] = ix.embed_query(query)
        try:
            QUERY_CACHE.write_text(json.dumps(cache), encoding="utf-8")
        except Exception as e:  # cache is an optimisation only
            log("could not write query cache:", e)
    return cache[query]


def retrieve(query: str, k: int = TOP_K, design: str = DESIGN) -> list[dict]:
    """Return the k nearest chunks as dicts (also used by evaluate.py)."""
    col = ix.open_collection(design)
    if col.count() == 0:
        return []
    res = col.query(query_embeddings=[query_vector(query)], n_results=k,
                    include=["documents", "metadatas", "distances"])
    out = []
    for doc, meta, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0]):
        out.append({"source": meta["source"], "location": meta["location"],
                    "score": round(1 - dist, 3), "text": doc})
    return out


@mcp.tool()
def search(query: str) -> str:
    """Search the corpus of Spanish occupational-safety law for construction work.

    The corpus holds five BOE norms: Ley 31/1995 (Prevención de Riesgos
    Laborales), RD 39/1997 (Servicios de Prevención), RD 1627/1997 (seguridad y
    salud en obras de construcción), RD 1215/1997 (equipos de trabajo) and
    Ley 32/2006 (subcontratación en el sector de la construcción).
    Use it for any question about what these norms require. Write the query in
    Spanish, as a short description of the topic.
    Returns up to 5 passages, each headed by [n] source, location and a
    similarity score, followed by the exact text. Cite source and location.
    If no passage answers the question, the corpus does not cover it.
    """
    try:
        hits = retrieve(query)
    except Exception as e:
        log("search failed:", e)
        return f"Search failed: {e}"
    if not hits:
        return "No passages found."
    return "\n\n".join(f"[{i}] {h['source']}, {h['location']} (score {h['score']})\n{h['text']}"
                       for i, h in enumerate(hits, start=1))


@mcp.tool()
def add_document(path: str) -> str:
    """Add a new document to the corpus index so that search can find it.

    Takes the path of a local file (.xml BOE, .pdf, .txt, .md or .html). The file
    is extracted, split into chunks with source and location, embedded and stored.
    If the document is already indexed nothing is embedded or duplicated and the
    result says so. Returns how many chunks were added and how many were already
    present. This changes the index, so it needs the user's approval.
    """
    p = Path(path).expanduser()
    if not p.is_file():
        return f"File not found: {path}"
    if p.suffix.lower() not in ALLOWED_SUFFIXES:
        return f"Unsupported file type {p.suffix!r}. Allowed: {sorted(ALLOWED_SUFFIXES)}"
    try:
        chunks = ix.chunk_file(p, DESIGN)
        if not chunks:
            return "No text could be extracted from that file."
        res = ix.embed_and_store(chunks, DESIGN)
    except Exception as e:
        log("add_document failed:", e)
        return f"Could not add the document: {e}"
    if res["new"] == 0:
        return f"Already indexed: {p.name} ({res['already_indexed']} chunks present, nothing added)."
    return (f"Added {res['new']} new chunks from {p.name} "
            f"({res['already_indexed']} were already present).")


if __name__ == "__main__":
    mcp.run()  # stdio