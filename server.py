"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Loads index/ at startup and never re-embeds the corpus: search embeds only
the query (cached in index/embeddings.sqlite, so a repeated question costs
nothing). Prints nothing to stdout, which carries the protocol; logs go to
stderr. The docstrings below are the tool descriptions the model reads.
"""

import sys

from mcp.server.mcpserver import MCPServer

import index

mcp = MCPServer("corpus", log_level="WARNING")
CACHE = index.EmbeddingCache()
CONFIG = index.load_config()


def log(message: str) -> None:
    print(f"[corpus] {message}", file=sys.stderr, flush=True)


@mcp.tool()
def search(query: str) -> str:
    """Search the FY2025 annual reports (Form 10-K) of Goldman Sachs, Morgan
    Stanley and BlackRock: Item 1A Risk Factors and the results part of MD&A
    (firm-wide and segment results, revenues, expenses, margins, client
    assets, AUM/AUS, flows, fee rates). Balance sheet, liquidity and capital
    sections are not indexed. Documents added later with add_document are
    searchable too.

    Use it before answering any question about these firms; search once per
    firm when comparing firms, and use the firm name and the metric in the
    query. Returns the 5 most relevant passages, each with a citation id in
    square brackets, the filing, section, heading and line range, then the
    passage text. Table rows read 'label | 2025 | 2024 | ...' with the column
    header shown first. If nothing relevant comes back, the corpus does not
    cover the question.
    """
    results = index.search(query, design=CONFIG["design"], k=CONFIG["k"], hybrid=CONFIG["hybrid"], cache=CACHE)
    return index.format_results(query, results)


@mcp.tool()
def add_document(path: str) -> str:
    """Add one file from the project folder to the searchable corpus: an SEC
    filing (.htm/.html, cut to Risk Factors and the results part of MD&A if it
    is a filing the pipeline knows), or any .pdf, .txt or .md file. It is
    extracted, chunked, embedded and stored with the same pipeline as the
    corpus, and is searchable straight away.

    Only use it when the user explicitly asks to add a document; the user
    must approve each call. If the same file is already indexed with the same
    content nothing is changed and no embeddings are spent; if its content
    changed, its old passages are replaced. Returns what happened: added,
    unchanged or replaced, with the number of passages.
    """
    try:
        result = index.add_file(path, design=CONFIG["design"])
    except (ValueError, FileNotFoundError) as error:
        return f"Not added: {error}"
    except index.QuotaExhausted as error:
        return f"Not added: {error}"
    log(f"add_document {path}: {result}")
    return (f"{result['status']}: {result['doc_id']}, {result['chunks']} passages "
            f"({result.get('newly_embedded', 0)} newly embedded). It is now searchable.")


if __name__ == "__main__":
    log(f"loaded index/ (design {CONFIG['design']}, k={CONFIG['k']}, hybrid={CONFIG['hybrid']}, "
        f"{index.collection(CONFIG['design']).count()} passages)")
    mcp.run()  # stdio
