"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): the most relevant chunks, each with a citation label
  [source, location], its section and its GOV.UK link.
- add_document(path): runs one file through index.py's pipeline (chunk_file +
  embed_and_store, via index.add_document) and stores it.

It opens the committed index in index/ and never re-embeds the corpus; only
the query (and an added document) is embedded. Nothing is printed to stdout,
which carries the MCP protocol; logs go to stderr. The docstrings below are
the tool descriptions the model reads.
"""

import logging
import sys

from mcp.server.mcpserver import MCPServer
from mcp_types import CallToolResult, TextContent

import index as ix

# YOUR decision, by the numbers: how many chunks one search returns. More chunks
# raise the hit rate but add words to every prompt (see evaluate.py's table).
TOP_K = 5

log = logging.getLogger("server")
log.addHandler(logging.StreamHandler(sys.stderr))
log.setLevel(logging.INFO)
log.propagate = False

mcp = MCPServer("corpus", log_level="WARNING")


def citation_label(chunk: dict) -> str:
    """How the agent cites a chunk, e.g. [appendix-student, ST 1.2]."""
    return f"[{chunk['source']}, {chunk['location']}]"


def format_results(results: list[dict]) -> str:
    """The text the model reads: label, section, link, then the chunk itself."""
    parts = []
    for n, r in enumerate(results, start=1):
        parts.append(
            f"Result {n}: cite as {citation_label(r)}\n"
            f"{r['title']} > {r['heading_path']}\n"
            f"{r['url']}\n"
            f"{r['text']}"
        )
    return "\n\n---\n\n".join(parts)


@mcp.tool()
def search(query: str) -> CallToolResult:
    """Search official UK government (GOV.UK) guidance on the Student visa and the
    Graduate visa: the Immigration Rules appendices (Student, Graduate, Finance,
    English Language), the Student and Graduate visa guides, and the Home Office
    caseworker guidance for both routes.

    Use it for any question about studying in the UK or staying on after a UK
    degree: eligibility, the CAS, money and bank evidence, English requirements,
    work rules, dependants, fees, applying, extending or switching. Search again
    with different words if the first results don't answer the question.

    Returns the most relevant passages, best first. Each starts with its citation
    label, e.g. [appendix-student, ST 1.2], followed by its section, its GOV.UK
    link and the passage text. If no passage answers the question, the documents
    don't cover it.
    """
    try:
        results = ix.search(query, k=TOP_K)
    except Exception as error:  # quota, missing index...: tell the agent, don't crash
        log.warning(f"search failed: {type(error).__name__}: {error}")
        return CallToolResult(content=[TextContent(type="text", text=f"Search failed: {error}")], is_error=True)
    keep = ("id", "source", "location", "heading_path", "sections", "paths", "rules", "url", "title", "score", "words",
            "text")
    return CallToolResult(
        content=[TextContent(type="text", text=format_results(results))],
        # Machine-readable copy for agent.py's citation check and evaluate.py. It includes the
        # passage text because some clients (Claude Code) show the model this copy, not `content`.
        structured_content={"results": [{k: r.get(k) for k in keep} | {"label": citation_label(r)} for r in results]},
    )


@mcp.tool()
def add_document(path: str) -> str:
    """Add one local file to the searchable corpus. Accepts .html (e.g. a GOV.UK
    page saved from the browser), .json (GOV.UK Content API), .pdf, .md or .txt.
    The file is cleaned, chunked and embedded with the same pipeline as the rest
    of the corpus, and becomes searchable straight away.

    Only use this when the user explicitly asks to add a document, and pass the
    full path they gave. An unchanged file that is already indexed is skipped; a
    changed file with the same name replaces its old version. Returns a one-line
    report of what was added.
    """
    try:
        return ix.add_document(path)
    except ix.QuotaExhausted:
        return "Not added: today's embedding quota is used up. Try again after 09:00 (Spain)."
    except Exception as error:
        log.warning(f"add_document failed: {type(error).__name__}: {error}")
        return f"Not added: {type(error).__name__}: {error}"


def check_index() -> None:
    """At startup: open the committed index (no embedding) and say what's in it."""
    try:
        count = ix.collection(ix.CHOSEN_DESIGN).count()
    except Exception as error:
        log.warning(f"Could not open index/: {error}")
        return
    if count:
        log.info(f"corpus server: {count} chunks in design '{ix.CHOSEN_DESIGN}', top {TOP_K} per search")
    else:
        log.warning(f"index/ has no '{ix.CHOSEN_DESIGN}' chunks yet: run `uv run python main.py index`.")


if __name__ == "__main__":
    check_index()
    mcp.run()  # stdio
