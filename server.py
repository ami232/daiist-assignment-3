"""MCP server (stdio). Two tools: search, add_document. `uv run server.py`
The server never re-embeds the corpus: search embeds one query (cached), add_document embeds only the new file."""
from pathlib import Path

try:                                            # mcp 2.x renamed FastMCP to MCPServer
    from mcp.server.mcpserver import MCPServer as FastMCP
except ImportError:                             # mcp 1.x
    from mcp.server.fastmcp import FastMCP

from config import DEFAULT_DESIGN, DESIGNS, ROOT
from index import index_document
from store import format_hits, retrieve

mcp = FastMCP("corpus")
ALLOWED = {".html", ".htm", ".txt", ".md", ".pdf"}
MAX_BYTES = 30_000_000


@mcp.tool()
def search(query: str, k: int = 5) -> str:
    """Search the indexed EU data-protection / AI law texts (GDPR, AI Act, ePrivacy, plus any added documents).
    Returns up to k passages, each headed by its citation like [gdpr:Article 33]. Cite exactly that string."""
    k = max(1, min(int(k), 10))
    return format_hits(retrieve(query, k=k))


@mcp.tool()
def add_document(path: str) -> str:
    """Index a new document (.html .txt .md .pdf) so search can find it. Path is a file on this machine.
    Already indexed with identical content: nothing happens. Same name but changed content: old passages
    are replaced. Needs human approval in the agent harness."""
    p = Path(path).expanduser()
    if not p.is_absolute():
        p = ROOT / p
    if not p.is_file():
        return f"ERROR: file not found: {path}"
    if p.suffix.lower() not in ALLOWED:
        return f"ERROR: unsupported type {p.suffix}; allowed: {sorted(ALLOWED)}"
    if p.stat().st_size > MAX_BYTES:
        return "ERROR: file larger than 30 MB"
    r = index_document(p, kinds=(DESIGNS[DEFAULT_DESIGN][0],))
    return (f"{r['status'].upper()}: doc_id={r['doc_id']}, {r['words']} words, "
            f"{sum(r['chunks'].values())} chunks ({sum(r['embedded'].values())} newly embedded). "
            f"Cite it as [{r['doc_id']}:<location>].")


if __name__ == "__main__":
    mcp.run()
