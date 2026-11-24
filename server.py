"""
Assignment 3: MCP server "corpus" over the Chedar help centre. `uv run server.py`

- search(query): the top chunks from the committed index/, each with title,
  URL and section, so answers can cite them.
- add_document(path): runs one file through index.py's own pipeline
  (chunk_file + embed_and_store). Chunks whose id is already stored are not
  re-embedded, so adding an indexed file again is a no-op.

index.py (and with it chromadb and google-genai) is imported on the first tool
call, not at startup, so the server answers `initialize` in about a second. It
never re-embeds the corpus: it only reads index/ and embeds the query.
Nothing goes to stdout (it carries the protocol); logs go to stderr.
"""

import logging
import sys
from contextlib import redirect_stdout
from pathlib import Path

from mcp.server.mcpserver import MCPServer

ROOT = Path(__file__).resolve().parent
TOP_K = 5

logging.basicConfig(stream=sys.stderr, level=logging.INFO, format="[corpus] %(message)s")
log = logging.getLogger("corpus")

mcp = MCPServer(
    "corpus",
    instructions=(
        "Search the Chedar help centre (learn.chedar.io), the user guide of a production-management "
        "app for film and advertising production companies. Use `search` before answering any "
        "question about how Chedar works, and cite the URL and section of each chunk you use."
    ),
    log_level="WARNING",
)


def _index():
    """Import index.py on first use; it pulls in chromadb and google-genai, which are slow to load."""
    with redirect_stdout(sys.stderr):
        import index

    return index


def format_results(chunks: list[dict]) -> str:
    """Numbered chunks, each with its title, URL, section and text: what the model reads and cites."""
    if not chunks:
        return "No matching passages in the Chedar help centre."
    blocks = []
    for n, chunk in enumerate(chunks, start=1):
        section = chunk.get("location") or chunk.get("section") or "(whole article)"
        blocks.append(
            f"[{n}] {chunk.get('title', '')}\n"
            f"URL: {chunk.get('source', '')}\n"
            f"Section: {section}\n"
            f"Score: {chunk.get('score', 0):.3f}\n"
            f"{chunk.get('text', '').strip()}"
        )
    return "\n\n---\n\n".join(blocks)


@mcp.tool()
def search(query: str) -> str:
    """Search the Chedar help centre (learn.chedar.io) and return the most relevant passages.

    Chedar is a production-management app for film and advertising production
    companies. The help centre covers: estimates and budget templates (UPC/APFP,
    CNC, AICP), quotes, purchases and purchase orders (POs), supplier invoices and
    invoicing clients, cost tracking and cost reports, bank reconciliation,
    accounting exports (including the French FEC), company and project settings,
    users and permissions, and general production know-how.

    Use this tool for any question about how to do something in Chedar or what a
    Chedar feature does, before answering. Write the query in English, as a short
    description of what the user wants to do (e.g. "convert an estimate into a
    purchase order"). Search again with other words if the passages don't answer.

    Returns up to 5 numbered passages, best first. Each has a [n] number, the
    article title, `URL:` (the article link), `Section:` (heading path inside the
    article), a similarity score and the passage text. Cite the URL and section of
    every passage you rely on. If nothing relevant comes back, the help centre
    does not cover the question.
    """
    log.info("search: %r", query)
    try:
        with redirect_stdout(sys.stderr):  # a stray print in index.py must not reach the protocol channel
            chunks = _index().search_index(query, k=TOP_K)
    except Exception as error:  # noqa: BLE001 - surface the cause to the caller instead of a bare crash
        log.exception("search failed")
        raise RuntimeError(f"Search failed: {type(error).__name__}: {error}") from error
    return format_results(chunks)


def _resolve(path: str) -> Path | None:
    """The file `path` names, relative to the working directory or to this repo."""
    for candidate in (Path(path).expanduser(), ROOT / path):
        if candidate.is_file():
            return candidate.resolve()
    return None


@mcp.tool()
def add_document(path: str) -> str:
    """Add one local file to the Chedar help-centre index so `search` can find it.

    Give the path of a text or Markdown file (absolute, or relative to the
    project folder), for example a help-centre article saved as .md. The file goes
    through the same pipeline as the corpus: it is split into chunks with title,
    URL and section metadata, each new chunk is embedded with Gemini and stored
    in index/.

    Already indexed: chunk ids come from the file name and chunk number, and a
    chunk whose id is already stored is skipped, never re-embedded. Adding a file
    that is already in the index therefore changes nothing and says so. To change
    an indexed article, save it under a new file name.

    Only call this when the user explicitly asks to add a document; it spends
    embedding quota. Returns one line: how many chunks were added, or that the
    file was already indexed, or why it could not be added.
    """
    log.info("add_document: %r", path)
    file = _resolve(path)
    if file is None:
        return f"Not added: no file found at {path!r}."
    index = _index()
    with redirect_stdout(sys.stderr):  # keep index.py's output off the protocol channel
        chunks = index.chunk_file(file)
        added = index.embed_and_store(chunks) if chunks else 0
    if not chunks:
        return f"Not added: {file.name} produced no text to index."
    if added == 0:
        return f"Skipped: {file.name} is already indexed ({len(chunks)} chunks); nothing was re-embedded."
    return f"Added {file.name}: {added} new chunk(s) embedded and stored ({len(chunks) - added} already indexed)."


if __name__ == "__main__":
    mcp.run()  # stdio
