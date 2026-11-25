"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns the top-5 chunks of the active design (index/active_design.txt,
  chosen by retrieval hit rate) with source and location citations.
- add_document(path): runs the file through index.py's pipeline (chunk_file ->
  embed_and_store via add_file), embeds only its new chunks and stores them.
  Already-indexed identical content is skipped; a changed file with the same name replaces
  its old chunks.

Loads index/ at startup and never re-embeds the corpus. Prints nothing to stdout (it carries
the protocol); index.py logs to stderr.
"""
import index as ix
from mcp.server.mcpserver import MCPServer

TOP_K = 5

mcp = MCPServer("corpus", log_level="WARNING")


@mcp.tool()
def search(query: str) -> str:
    """Search the EU UCITS rulebook: Directive 2009/65/EC (UCITS Directive), Commission
    Directive 2007/16/EC (eligible assets), Commission Directive 2010/43/EU (organisation,
    conflicts of interest, risk management) and Commission Regulation 583/2010 (key investor
    information), plus any document added with add_document.

    Use it for every question about UCITS funds and their management companies: investment
    and diversification limits, eligible assets, derivatives and global exposure, borrowing,
    redemptions, master-feeder funds, cross-border marketing, organisation, conflicts of
    interest, best execution, risk management and the key investor information document.
    Search again with different wording when a question needs two rules.

    Returns the 5 most relevant passages. Each starts with its citation in the form
    [doc_id, Article N] (or [doc_id, Article N to Article M] when a passage spans two
    articles), followed by the act's title, a relevance score between 0 and 1, and the text.
    Cite only these citations; if no passage answers the question, say you do not know.
    """
    try:
        return ix.format_hits(ix.search(query, k=TOP_K))
    except ix.DailyQuotaReached:
        return "Search is unavailable right now: the daily embedding limit was reached."


@mcp.tool()
def add_document(path: str) -> str:
    """Add one document (.html, .pdf, .txt or .md) to the UCITS search index.

    The file at `path` (absolute, or relative to the project folder) is extracted, cleaned,
    split into chunks with source and location metadata, embedded and stored, so that
    search can find it immediately. If a file with identical content is already indexed,
    nothing is embedded; if a file with the same name but different content exists, its
    old chunks are replaced. Returns a one-line summary (document id, number of chunks,
    how many were newly embedded) or an error message.
    """
    return ix.add_file(path)


if __name__ == "__main__":
    ix.collection(ix.active_design())  # load the saved index at startup (no embedding)
    mcp.run()  # stdio