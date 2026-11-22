"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns the top chunks with source and location.
- add_document(path): runs a PDF through index.py's pipeline, embeds it and
  stores it, under the duplicate policy in index.index_document.

The index in index/ is loaded at startup; the corpus is never re-embedded
(only the query is). Nothing is printed to stdout, which carries the MCP
protocol; logs go to stderr. Docstrings become the tool descriptions the
model reads.
"""

import logging
import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

import index as ix
import retrieval

ROOT = Path(__file__).resolve().parent
logging.basicConfig(stream=sys.stderr, level=logging.INFO, format="[corpus] %(message)s")
log = logging.getLogger("corpus")

mcp = MCPServer("corpus", log_level="WARNING")


def _body(text: str) -> str:
    """Chunk text without the "[report · chapter · heading]" line used for embedding."""
    if text.startswith("[") and "\n" in text:
        return text.split("\n", 1)[1]
    return text


def _format_hit(rank: int, hit: dict) -> str:
    pages = f"p. {hit['page']}" if hit["page"] == hit["page_end"] else f"pp. {hit['page']}-{hit['page_end']}"
    context = " · ".join(x for x in (hit["chapter"], hit["heading"]) if x)
    year = f" ({hit['year']})" if hit["year"] else ""
    return (f"[{rank}] Source: {hit['doc_id']}, {pages} | {hit['title']}{year}"
            f"{' | ' + context if context else ''} | relevance {hit['score']:.2f}\n{_body(hit['text'])}")


@mcp.tool()
def search(query: str) -> str:
    """Search IEA reports on the electric-vehicle market and return the 5 most relevant passages.

    Corpus: Global EV Outlook 2026 (executive summary; ch. 1 car markets, ch. 2
    prices and affordability, ch. 5 batteries, ch. 9 outlook to 2030-2035),
    Global EV Outlook 2025 (executive summary; ch. 1 car markets, ch. 2 car
    industry) and Global Critical Minerals Outlook 2026 (executive summary;
    lithium, nickel, cobalt and graphite outlooks), plus any document added
    with add_document. Topics: EV sales, stock and market shares by country and
    region, prices, battery demand and prices, critical-mineral supply, demand
    and prices, and projections. Figures shown only in charts are not indexed.

    Use it for any factual question on these topics, with one focused query per
    fact (e.g. ask separately for the 2024 and the 2025 figure when comparing
    years). The GEVO 2025 and 2026 editions both cover similar topics, so
    include the year you need in the query and check the year of each passage.

    Returns up to 5 passages, best first. Each starts with a header
    "[n] Source: <doc_id>, p. <page> | <report title> (<year>) | <chapter · section> | relevance <score>"
    followed by the passage text. Cite answers as (<doc_id>, p. <page>). If no
    passage states the answer, the corpus does not contain it.
    """
    query = (query or "").strip()
    if not query:
        raise ToolError("The query is empty. Pass a question or keywords.")
    try:
        hits = retrieval.search(query)
    except SystemExit as e:  # daily embedding quota: don't let it stop the server
        raise ToolError(f"Search is unavailable: {e}") from None
    except Exception as e:  # noqa: BLE001 - report the failure to the caller
        log.exception("search failed")
        raise ToolError(f"Search failed: {type(e).__name__}: {e}") from None
    log.info("search %r -> %s", query, ", ".join(f"{h['doc_id']} p.{h['page']}" for h in hits))
    if not hits:
        return "The index is empty: no documents have been indexed."
    return "\n\n".join(_format_hit(i, h) for i, h in enumerate(hits, start=1))


@mcp.tool()
def add_document(path: str) -> str:
    """Add a PDF report to the searchable index (chunked, embedded with Gemini and saved in index/).

    `path` is the path to a local PDF file, absolute or relative to the project
    folder. The document goes through the same extraction, cleaning and
    section-based chunking as the rest of the corpus, and becomes searchable
    with search straight away.

    Duplicate policy: if a file with the same content is already indexed,
    nothing changes and no embeddings are spent; if it is a new version of a
    document already indexed (same document, different content), it replaces
    the old version so the two never mix; otherwise it is added. Only PDFs are
    accepted.

    Returns one line saying whether the document was added, replaced or was
    already indexed, with its document id, title, number of passages and pages.
    This changes the index: only call it when the user asked to add that file.
    """
    p = Path(path.strip()).expanduser()
    if not p.is_absolute() and not p.exists():
        p = ROOT / p
    if not p.is_file():
        raise ToolError(f"File not found: {path}")
    if p.suffix.lower() != ".pdf":
        raise ToolError(f"Only PDF files can be added; got {p.name}")
    try:
        result = ix.index_document(p)
    except SystemExit as e:  # daily embedding quota: index left unchanged
        raise ToolError(f"Not added, the index is unchanged: {e}") from None
    except Exception as e:  # noqa: BLE001 - report the failure to the caller
        log.exception("add_document failed")
        raise ToolError(f"Not added, the index is unchanged: {type(e).__name__}: {e}") from None
    retrieval.reload(ix.CHUNKING)
    total = retrieval.loaded_chunks()
    n_docs = len({c["doc_id"] for c in total})
    who = f"{result['doc_id']} ({result['title']})"
    if result["status"] == "unchanged":
        msg = (f"Already indexed: {p.name} has the same content as {who}, "
               f"{result['chunks']} passages. Nothing was changed.")
    elif result["status"] == "replaced":
        msg = (f"Replaced the previous version of {who}: {result['old_chunks']} old passages removed, "
               f"{result['chunks']} new passages from pp. {result['pages']}.")
    else:
        msg = f"Added {who}: {result['chunks']} passages from pp. {result['pages']}."
    msg += f" The index now holds {len(total)} passages from {n_docs} documents."
    log.info(msg)
    return msg


if __name__ == "__main__":
    n = len(retrieval.loaded_chunks())  # load index/ once at startup
    log.info("index loaded: %d chunks (%s design)", n, ix.CHUNKING)
    mcp.run()  # stdio
