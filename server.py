"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Loads index/ at startup and never re-embeds the corpus. Nothing is printed to
stdout (it carries the protocol); index.py logs to stderr.
"""

import logging
import sys

from mcp.server.mcpserver import MCPServer

import index

logging.basicConfig(stream=sys.stderr, level=logging.WARNING)
mcp = MCPServer("corpus", log_level="WARNING")


def format_hits(hits: list[dict]) -> str:
    """Each hit starts with its citation tag, which the agent copies verbatim."""
    if not hits:
        return "No passages found."
    return "\n\n".join(f"[{h['source']} | {h['location']}] (score {h['score']:.3f})\n{h['text']}" for h in hits)


@mcp.tool()
def search(query: str) -> str:
    """Search EU investment-services legislation and return the most relevant passages.

    The corpus holds the English texts of MiFID II (Directive 2014/65/EU), the
    MiFID II Delegated Regulation (EU) 2017/565, MiFIR (Regulation 600/2014) and
    the PRIIPs Regulation (1286/2014), split by article, plus any document added
    with add_document. It does not hold national law, supervisors' guidance or
    later amendments.

    Use this for every factual question about these rules, before answering.
    Phrase `query` as a specific question or keywords; search again with other
    wording if the first results do not answer it.

    Returns up to 5 passages. Each starts with a citation tag
    `[source | location]` (document name, then section and page). Cite a passage
    by copying its tag exactly.
    """
    try:
        return format_hits(index.search(query))
    except index.QuotaExhausted:
        return "Search is unavailable: the daily embedding quota is used up."


@mcp.tool()
def add_document(path: str) -> str:
    """Add one document (PDF, HTML, TXT or MD file on this machine) to the corpus.

    `path` is the file's path. The file is extracted, chunked, embedded and
    stored with the same pipeline as the rest of the corpus, after which search
    can find it. The document is named after the file. If a document with that
    name is already indexed with identical content, nothing changes; if its
    content changed, its old passages are replaced.

    Returns what happened: added, replaced or unchanged, with chunk counts.
    """
    try:
        r = index.add_file(path)
    except (FileNotFoundError, ValueError) as error:
        return f"Not added: {error}"
    except index.QuotaExhausted:
        return "Not added: the daily embedding quota is used up. Try again after the reset."
    if r["status"] == "unchanged":
        return f"'{r['source']}' is already indexed with identical content ({r['chunks']} chunks); nothing changed."
    return (f"{r['status'].capitalize()} '{r['source']}': {r['chunks']} chunks, {r['words']:,} words, "
            f"{r['embedded']} embedded. Cite it as source '{r['source']}'.")


if __name__ == "__main__":
    mcp.run()  # stdio
