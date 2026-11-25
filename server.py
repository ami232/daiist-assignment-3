"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Loads index/ (Chroma) on first use and never re-embeds the corpus: only the
query is embedded, and that vector is cached. Prints nothing to stdout (it
carries the protocol); logs go to stderr. Docstrings become the tool
descriptions the model reads.
"""

import logging
import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer

import index as ix
import rag

logging.basicConfig(level=logging.WARNING, stream=sys.stderr, format="%(name)s: %(message)s")
log = logging.getLogger("server")

ALLOWED_DIR = ix.ROOT          # add_document only reads files inside this repository (corpus/ included)

mcp = MCPServer("corpus", log_level="WARNING")


@mcp.tool()
def search(query: str) -> str:
    """Search Spanish state legislation for the self-employed (autónomos), BOE consolidated text.

    The corpus holds: the Self-Employed Workers' Statute (LETA, Ley 20/2007), the General
    Social Security Act, titles IV and V (LGSS: RETA, contributions, temporary incapacity,
    cessation of activity), the Invoicing Regulation (RF, RD 1619/2012) and the Tax
    Management and Inspection Regulation, title II (RGAT, RD 1065/2007: tax census
    registration, tax address, NIF, record books), plus any documents added with add_document.

    Use it before answering any question about an autónomo's rights or obligations; you
    can call it several times with other words. Write the query in Spanish, using the
    law's own terms (e.g. "reducción de cuotas inicio de actividad").

    Returns the 5 most relevant fragments, in Spanish. Each one carries a ready-to-copy
    citation in the format [SOURCE, Location] (e.g. [LETA, Artículo 38 ter]), the law's
    title, the consolidation date, the text and the BOE link. It ends with the notice that
    the consolidated text is for information only.
    """
    query = (query or "").strip()
    if not query:
        return "Error: the query is empty. Write what you want to search for."
    try:
        return rag.format_hits(rag.retrieve(query))
    except ix.QuotaExhausted:
        return "Error: the Gemini embeddings API quota is exhausted. Try again later."
    except Exception as error:  # noqa: BLE001 - an MCP tool reports errors, it doesn't raise them
        log.exception("search failed")
        return f"Error while searching: {type(error).__name__}: {error}"


def _resolve(path: str) -> Path:
    """The file to add, as an absolute path inside the repository; ValueError otherwise."""
    candidate = Path(path.strip().strip('"'))
    candidate = (candidate if candidate.is_absolute() else ALLOWED_DIR / candidate).resolve()
    if not candidate.is_relative_to(ALLOWED_DIR):
        raise ValueError(f"only files inside {ALLOWED_DIR.name}/ can be added (e.g. corpus/…)")
    if not candidate.is_file():
        raise ValueError(f"the file {candidate.relative_to(ALLOWED_DIR)} does not exist")
    if candidate.suffix.lower() != ".xml" or candidate.name.endswith(".meta.xml"):
        raise ValueError("only BOE consolidated-text XML is accepted (corpus/<BOE-id>.xml)")
    return candidate


@mcp.tool()
def add_document(path: str) -> str:
    """Add a law in BOE consolidated-text XML to the index and make it available to search.

    `path` is the file's path inside the repository, e.g. "corpus/BOE-A-2026-7296.xml"
    (downloaded from the BOE open-data API; if a .meta.xml sits next to it, the title and
    consolidation date are taken from it). The file goes through the same pipeline as the
    rest of the corpus (cleaning, chunking by article, embeddings), and only new fragments
    are embedded.

    If the law is already indexed with the same consolidation date, nothing changes; if
    the file is a newer version, it replaces the old one; if it is older, nothing changes.
    It modifies the index: use it only when the user asks for it.

    Returns a one-line summary (law, fragments added and skipped) or a message starting
    with "Error:".
    """
    try:
        file = _resolve(path or "")
        result = ix.index_file(file)
    except ValueError as error:
        return f"Error: {error}"
    except ix.QuotaExhausted:
        return "Error: the Gemini embeddings API quota is exhausted. Try again later."
    except Exception as error:  # noqa: BLE001 - unparseable XML and the like
        log.exception("add_document failed")
        return f"Error: could not index {path}: {type(error).__name__}: {error}"

    name = f"{result['source']} ({result['boe_id']}, consolidated as of {result['updated']})"
    if result["status"] == "already":
        return f"{name} was already indexed in this version: nothing added ({result['chunks']} fragments)."
    if result["status"] == "older":
        return (f"{name} not added: the index already has a newer version "
                f"(consolidated as of {result['stored_updated']}).")
    verb = "Replaced with the new version" if result["status"] == "replaced" else "Added"
    line = f"{verb}: {name}. {result['added']} new fragments, {result['skipped']} skipped (already there)."
    if result["pending"]:
        line += f" {result['pending']} still to embed because of the embeddings quota: call again later."
    return line


if __name__ == "__main__":
    mcp.run()  # stdio
