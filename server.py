"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Loads index/ at startup; never re-embeds the corpus. Prints nothing to stdout
(it carries the protocol); logs to stderr.
"""

import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer

import index as ix

ROOT = Path(__file__).resolve().parent
TOP_K = 5
ALLOWED = {".pdf", ".txt", ".md", ".html", ".htm"}
MAX_MB = 40

mcp = MCPServer("corpus", log_level="WARNING")


def cite_as(meta: dict) -> str:
    """The citation the assistant must use, e.g. [ai_act, Article 50(1)-(3)]."""
    return f"[{meta['source']}, {meta['location'].split(' - ')[0]}]"


@mcp.tool()
def search(query: str) -> str:
    """Search the EU AI Act, the GDPR and the Commission guidelines on the AI system
    definition (plus any document added later) and return the 5 most relevant passages.

    Use it for any question about what these EU texts say: whether an AI system is
    high-risk or prohibited, transparency duties, obligations of deployers, personal
    data rules, fines, definitions. Write the query as a short, specific description
    of the rule you need, with the key legal terms (for example "transparency
    obligation chatbot interacts with natural persons"); search again with other
    terms if the passages do not answer the question.

    Returns numbered passages. Each has its citation in square brackets
    (source, article / annex / section, page), a relevance score and the text.
    Cite with exactly that bracket. These texts are EU law only: national laws and
    guidance from other bodies are not in the index, so an empty or off-topic result
    means the corpus does not cover the question.
    """
    hits = ix.retrieve(query, k=TOP_K)
    if not hits:
        return "No passages found: the index is empty."
    parts = [f"{len(hits)} passages for: {query}"]
    for n, h in enumerate(hits, 1):
        m = h["meta"]
        parts.append(
            f"\n[{n}] cite as {cite_as(m)} | {m['title']} | {m['location']} | PDF page {m['page']}"
            f" | score {h['score']:.3f}\n{h['text']}"
        )
    return "\n".join(parts)


@mcp.tool()
def add_document(path: str) -> str:
    """Add one document to the searchable index: reads the file at `path`, splits it
    into chunks, embeds them and stores them, so that later searches can cite it.

    `path` is a file on this machine (.pdf, .txt, .md or .html, up to 40 MB),
    absolute or relative to the project folder. The source name used in citations is
    the file name without extension. If the very same file is already indexed,
    nothing is changed and the tool says so. If a file with the same name but
    different content is indexed, its old chunks are replaced by the new ones.
    Returns the status, the number of chunks and how many were newly embedded.
    This changes the shared index: use it only when the user asked to add a document.
    """
    p = Path(path).expanduser()
    if not p.is_absolute():
        p = ROOT / p
    p = p.resolve()
    if not p.is_file():
        return f"Error: no file at {path}."
    if p.suffix.lower() not in ALLOWED:
        return f"Error: {p.suffix or 'this file type'} is not supported. Use one of: {', '.join(sorted(ALLOWED))}."
    if p.stat().st_size > MAX_MB * 1e6:
        return f"Error: file is larger than {MAX_MB} MB."
    try:
        res = ix.index_file(p, designs=(ix.active_design(),))
    except ix.DailyQuotaExceeded:
        return "Error: the daily embedding quota is used up. Nothing was added; try again after the reset."
    except Exception as e:  # noqa: BLE001
        return f"Error: could not index {p.name}: {type(e).__name__}: {e}"
    if res["status"] == "already_indexed":
        return f"Already indexed: {res['source']} ({res['chunks']}). Nothing was changed."
    verb = "Added" if res["status"] == "added" else "Replaced the earlier version of"
    return (f"{verb} {res['source']}: {res['chunks']} chunks, {res['embedded']} newly embedded, "
            f"{res['words']} words. It is now searchable.")


if __name__ == "__main__":
    print(f"corpus server: design={ix.active_design()}, method={ix.active_method()}", file=sys.stderr)
    mcp.run()  # stdio
