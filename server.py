"""
Assignment 3: MCP server exposing the EU drone-regulation corpus (`uv run server.py`; the editor and
agent.py start it over stdio).

- search(query): top chunks with citations [chunk id] source | location.
- add_document(path): runs a file through index.py's own pipeline (chunk_file + embed_and_store).

It loads the committed index/ at startup and never re-embeds the corpus. Nothing is printed to stdout
(it carries the protocol); logs go to stderr.
"""

import os

os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")

from pathlib import Path  # noqa: E402

from mcp.server.mcpserver import MCPServer  # noqa: E402

import rag  # noqa: E402
from index import SUPPORTED_SUFFIXES, add_file  # noqa: E402

mcp = MCPServer("corpus", log_level="WARNING")


@mcp.tool()
def search(query: str) -> str:
    """Search the EU drone (UAS) regulations corpus: Implementing Regulation (EU) 2019/947 (operating
    rules: open/specific/certified categories, subcategories A1-A3, pilot competency, registration,
    operational authorisations, LUC), Delegated Regulation (EU) 2019/945 and its amendment 2020/1058
    (drone classes C0-C6, technical requirements, remote ID, CE marking), and Implementing Regulation
    (EU) 2021/664 (U-space). Use it for any question about what EU law requires for a drone operation.
    Write the query as a short description of the rule you need (e.g. "minimum distance from uninvolved
    people in subcategory A2"). Returns the 5 most relevant passages, each headed by its citation:
    [chunk id] regulation | article or annex point. Cite those ids. If nothing relevant is returned,
    the corpus does not cover the question."""
    query = (query or "").strip()
    if not query:
        return "Empty query: describe the rule you are looking for."
    exclude = os.environ.get("CORPUS_EXCLUDE_ADDED") == "1"
    return rag.format_results(rag.search(query, rag.ACTIVE_DESIGN, k=rag.TOP_K, exclude_added=exclude))


@mcp.tool()
def add_document(path: str) -> str:
    """Add one document to the drone-regulation index so that search can find it. `path` is a local
    file (EUR-Lex XHTML/HTML, PDF, TXT or MD). The file is extracted, chunked with the same pipeline as
    the corpus, embedded with Gemini and stored. If the identical file is already indexed nothing is
    done; if a different version of the same document is indexed, the old chunks are replaced.
    Returns what happened and how many chunks were stored."""
    p = Path(path).expanduser()
    if not p.is_absolute():
        p = (Path(__file__).resolve().parent / p).resolve()
    if not p.is_file():
        return f"Not added: {p} does not exist or is not a file."
    if p.suffix.lower() not in SUPPORTED_SUFFIXES:
        return f"Not added: unsupported file type {p.suffix}. Supported: {', '.join(sorted(SUPPORTED_SUFFIXES))}."
    return add_file(p)


if __name__ == "__main__":
    mcp.run()  # stdio
