"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): the 5 best chunks of the OWASP corpus, each with its id and citation.
- add_document(path): runs a Markdown/text file through index.py's pipeline, embeds it, stores it.

It loads index/ at startup and never re-embeds the corpus (only new questions and new
documents are embedded). Nothing is printed to stdout, which carries the protocol.
Set CORPUS_BASE_ONLY=1 to hide documents added later (evaluate.py does, so the test
set keeps measuring the same corpus).
"""

import hashlib
import os
from pathlib import Path

from mcp.server.mcpserver import MCPServer

import rag
from index import chunk_file, embed_and_store

mcp = MCPServer("corpus", log_level="WARNING")
CONFIG = rag.load_config()
BASE_ONLY = os.environ.get("CORPUS_BASE_ONLY") == "1"
ALLOWED_SUFFIXES = {".md", ".txt"}
_index: rag.Index | None = None


def index() -> rag.Index:
    global _index
    if _index is None:
        _index = rag.Index(CONFIG["design"], include_added=not BASE_ONLY)
        rag.log(f"loaded {len(_index.chunks)} chunks ({CONFIG['design']}, {CONFIG['search']} search)")
    return _index


@mcp.tool()
def search(query: str) -> str:
    """Search the OWASP Cheat Sheet corpus: practical web-application security guidance on
    authentication, passwords, multi-factor auth, password reset, sessions and cookies, CSRF,
    XSS, SQL injection, input validation, file uploads, HTTP security headers, Content Security
    Policy, SSRF, secrets management and security logging.

    Use it for any question about how to build or configure these securely. Write the query as
    a specific question or key phrase. Returns the 5 most relevant passages, each starting with
    an id in brackets (cite it, e.g. [Password_Storage_Cheat_Sheet:005]), the cheat sheet and
    section it comes from, and its URL. If none of them answers the question, the corpus does
    not cover it.
    """
    hits = index().search(query, k=CONFIG["k"], method=CONFIG["search"])
    return rag.format_results(hits)


@mcp.tool()
def add_document(path: str) -> str:
    """Add a Markdown (.md) or text (.txt) document to the corpus, so search can find it.

    `path` is the file's path on this machine, relative to the project folder or absolute.
    The file is cleaned, split into sections, embedded and stored in the index. If the same
    content is already indexed nothing changes; if a document with the same file name but
    different content is indexed, its old chunks are replaced. Returns what was done.
    """
    file = Path(path).expanduser()
    file = file if file.is_absolute() else rag.ROOT / file
    if not file.is_file():
        return f"Not added: there is no file at {path}."
    if file.suffix.lower() not in ALLOWED_SUFFIXES:
        return f"Not added: only {', '.join(sorted(ALLOWED_SUFFIXES))} files can be indexed."

    digest = hashlib.sha256(file.read_bytes()).hexdigest()
    design = CONFIG["design"]
    existing = [c for c in rag.read_chunks(design) if c["source"] == file.stem]
    if existing and all(c.get("sha256") == digest for c in existing):
        return f"Already indexed: {file.name} ({len(existing)} chunks), content unchanged. Nothing was done."

    chunks = chunk_file(file, design, url=f"local file: {file.name}")
    if not chunks:
        return f"Not added: no text could be extracted from {file.name}."
    for chunk in chunks:
        chunk["added"] = True
    new = embed_and_store(chunks, design)
    global _index
    _index = None                       # reload on the next search, with the new chunks
    action = "Replaced" if existing else "Added"
    return (f"{action} {file.name}: {len(chunks)} chunks stored in index/{design} "
            f"({new} newly embedded). Search now covers it.")


if __name__ == "__main__":
    mcp.run()  # stdio
