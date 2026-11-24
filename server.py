"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Loads the committed index/ (Chroma) at startup; never re-embeds the corpus.
Prints nothing to stdout (it carries the MCP protocol); logs go to stderr.
"""

import contextlib
import os
import sys
from pathlib import Path

os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")  # keep Chroma quiet

from mcp.server.mcpserver import MCPServer

import index

ROOT = Path(__file__).resolve().parent
DESIGN = "a"  # chunking design served to the agent (a = one chunk per article/section)
TOP_K = 5
HTML_SUFFIXES = {".html", ".htm", ".xhtml"}

mcp = MCPServer("corpus", log_level="WARNING")


def format_results(results: list[dict]) -> str:
    blocks = []
    for n, r in enumerate(results, 1):
        m = r["metadata"]
        blocks.append(
            f"[{n}] source_id: {m['doc_id']} | location: {m['location']} | similarity: {r['score']:.3f}\n"
            f"document: {m['source']}\n"
            f"url: {m['url']}\n"
            f"{r['text']}"
        )
    return "\n\n---\n\n".join(blocks)


@mcp.tool()
def search(query: str) -> str:
    """Search the EU air passenger rights corpus and return the 5 most relevant passages.

    The corpus holds EU law for air passengers: Regulation (EC) 261/2004 (denied boarding,
    cancellations, long delays, upgrading/downgrading: compensation, refunds, re-routing,
    meals and hotels) and the Commission's 2024 interpretative guidelines on it;
    Regulation (EC) 2027/97 (airline liability for accidents and for lost, damaged or
    delayed baggage, Montreal Convention limits); Regulation (EC) 1107/2006 (rights of
    disabled passengers and passengers with reduced mobility) and its 2024 guidelines;
    plus any document added later with add_document.

    Use it for any question about what an air passenger is entitled to in the EU. Write the
    query in English, describing the passenger's situation or the legal concept. Call it
    again with a different query if the passages do not answer the question.

    Returns numbered passages, each with source_id, location (e.g. "Article 7",
    "Section 4.4.7", "Annex I"), a cosine similarity score (higher is closer), the document
    title, its URL and the passage text with its footnotes. Cite answers as source_id + location. If no passage covers the question,
    the corpus does not answer it.
    """
    with contextlib.redirect_stdout(sys.stderr):
        try:
            return format_results(index.search(query, DESIGN, k=TOP_K))
        except index.QuotaExhausted as e:
            return f"ERROR: the daily embedding quota is exhausted, search is unavailable until it resets ({e})."


@mcp.tool()
def add_document(path: str) -> str:
    """Add one EUR-Lex HTML document to the corpus so that search can find it.

    `path` is a local .html file (absolute, or relative to the project folder), for
    example a regulation downloaded from EUR-Lex into corpus/. The file is parsed into
    articles, recitals, sections and annexes, cut into chunks the same way as the rest of
    the corpus, embedded and stored permanently in the index.

    Adding the same file again is safe: chunks already in the index are not embedded twice.
    Returns the new source_id, how many chunks were added and which sections they cover,
    or an error message if the file is missing, not HTML, or the embedding quota is spent.
    """
    with contextlib.redirect_stdout(sys.stderr):
        file = Path(path).expanduser()
        if not file.is_absolute():
            file = ROOT / file
        if not file.is_file():
            return f"ERROR: no file at {file}."
        if file.suffix.lower() not in HTML_SUFFIXES:
            return f"ERROR: {file.name} is not an HTML file; only EUR-Lex HTML documents are supported."
        chunks = index.chunk_file(file, DESIGN)
        if not chunks:
            return f"ERROR: no text could be extracted from {file.name}."
        try:
            new = index.embed_and_store(chunks, DESIGN)
        except index.QuotaExhausted as e:
            return f"ERROR: the daily embedding quota is exhausted; {file.name} was not fully added ({e})."
        meta = chunks[0]["metadata"]
        locations = [c["metadata"]["location"] for c in chunks]
        return (
            f"Added source_id {meta['doc_id']} ({meta['source']}).\n"
            f"{len(chunks)} chunks: {new} newly embedded, {len(chunks) - new} were already in the index.\n"
            f"Sections covered: {locations[0]} ... {locations[-1]}."
        )


if __name__ == "__main__":
    mcp.run()  # stdio
