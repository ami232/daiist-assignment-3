"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Loads the committed index/ at startup and never re-embeds the corpus. Prints
nothing to stdout (it carries the protocol); logs go to stderr.
"""

import logging
import sys

from mcp.server.mcpserver import MCPServer

import index

logging.basicConfig(level=logging.WARNING, stream=sys.stderr, format="%(name)s: %(message)s")
log = logging.getLogger("server")

mcp = MCPServer("corpus", log_level="WARNING")

TOP_K = 5


def citation(hit: dict) -> str:
    return f"[{hit['source']}, p. {hit['page']}]"


def format_hits(hits: list[dict]) -> str:
    if not hits:
        return "No passages found in the corpus."
    blocks = []
    for i, h in enumerate(hits, start=1):
        blocks.append(
            f"Result {i} {citation(h)}  (score {h['score']:.3f})\n"
            f"{h['title']} - {h['chapter']} - {h['section']}\n"
            f"{h['text']}"
        )
    return "\n\n---\n\n".join(blocks)


@mcp.tool()
def search(query: str) -> str:
    """Search the FAA pilot-training corpus and return the 5 most relevant passages.

    The corpus holds selected chapters of three FAA handbooks:
    - FAA-H-8083-25C Pilot's Handbook of Aeronautical Knowledge: ch. 10 Weight and
      Balance, ch. 11 Aircraft Performance (density altitude, takeoff/landing,
      climb, performance charts), ch. 17 Aeromedical Factors (hypoxia, alcohol,
      drugs, fatigue, spatial disorientation, vision);
    - FAA-H-8083-3C Airplane Flying Handbook: ch. 18 Emergency Procedures
      (forced landings, engine failure, fires, system malfunctions);
    - FAA-H-8083-28B Aviation Weather Handbook: ch. 18 Visibility, ch. 19
      Turbulence, ch. 20 Icing, ch. 22 Thunderstorms.
    It does NOT contain the federal regulations (14 CFR), the AIM, or any
    specific aircraft's POH figures.

    Use it for any question about those topics; ask about one thing per call
    and call again for the other part of a two-part question. Each result
    starts with a citation like [FAA-H-8083-25C, p. 11-4] (handbook and printed
    page) followed by the chapter, section and passage text. Cite answers with
    those citations exactly; if no result supports an answer, say the corpus
    does not cover it.
    """
    query = (query or "").strip()
    if not query:
        return "Empty query: pass the question or keywords to search for."
    try:
        return format_hits(index.search(query, k=TOP_K))
    except index.QuotaExhausted as error:
        return f"Search unavailable: the embedding quota is exhausted for today ({error})."


@mcp.tool()
def add_document(path: str) -> str:
    """Add one local document (.pdf, .txt or .md) to the searchable corpus.

    Runs the file through the same extract-clean-chunk pipeline as the corpus
    (index.py), embeds the new chunks with Gemini and stores them in index/.
    The document's source name is its file name without extension. If a file
    with the same name and identical content is already indexed, nothing is
    embedded and it reports "already indexed"; if the name matches but the
    content changed, the old chunks are replaced. Returns the status and how
    many chunks were stored. Uses embedding quota, so only call it when the
    user asked to add that file.
    """
    try:
        result = index.add_document(path)
    except FileNotFoundError as error:
        return f"Not added: {error}"
    except ValueError as error:
        return f"Not added: {error}"
    except index.QuotaExhausted as error:
        return f"Not added: the embedding quota is exhausted for today ({error}). Nothing partial is kept from the failed batch."
    log.warning("add_document %s -> %s", path, result)
    status = result["status"]
    if status == "already indexed":
        return f"Already indexed: '{result['source']}' has {result['chunks']} chunks with identical content; nothing was embedded."
    if status == "no text found":
        return f"Not added: no text could be extracted from {path}."
    extra = f", removed {result.get('removed', 0)} outdated chunks" if status == "replaced" else ""
    return (f"{status.capitalize()}: '{result['source']}' -> {result['chunks']} chunks, "
            f"{result['embedded']} newly embedded{extra}. Cite it as [{result['source']}, p. ...].")


if __name__ == "__main__":
    mcp.run()  # stdio
