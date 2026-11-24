"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Load index/ at startup; never re-embed the corpus. Print nothing to stdout
(it carries the protocol); log to stderr. Docstrings become the tool
descriptions the model reads.
"""

import shutil
from pathlib import Path

from mcp.server.mcpserver import MCPServer

import index
import retrieve

K = 3

mcp = MCPServer("corpus", log_level="WARNING")
retrieve.load(index.STRATEGY)


@mcp.tool()
def search(query: str) -> str:
    results = retrieve.search(query, k=K)
    if not results:
        return "No passages found."
    return "\n\n---\n\n".join(
        f"[{i}] {r['metadata']['citation']} (source: {r['metadata']['source']})\n{r['text']}"
        for i, r in enumerate(results, start=1))


@mcp.tool()
def add_document(path: str) -> str:
    src = Path(path).expanduser().resolve()
    if not src.is_file() or src.suffix.lower() != ".pdf":
        return f"Error: {path} is not a PDF file."
    dest = index.DOCS_DIR / src.name
    if src != dest.resolve():
        shutil.copy2(src, dest)
    s = index.index_file(dest)
    retrieve._corpus.pop(index.STRATEGY, None)
    return (f"{s['source']}: {s['chunks']} chunks, {s['embedded']} newly embedded, "
            f"{s['already_indexed']} already indexed, {s['removed_stale']} stale removed.")


if __name__ == "__main__":
    mcp.run()  # stdio
