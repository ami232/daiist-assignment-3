"""Assignment 3: MCP server (`uv run server.py`) with the search and add_document tools over index/."""

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

import index

TOP_K = 5

mcp = MCPServer("corpus", log_level="WARNING")


def cite_labels(result: dict) -> str:
    articles = [a for a in str(result.get("articles") or result["article"]).split("; ") if a]
    return "; ".join(f"[{result['source']}, {a}]" for a in articles)


def format_results(results: list[dict]) -> str:
    blocks = []
    for r in results:
        blocks.append(
            f"Result {r['rank']} (similarity {r['score']:.2f})\n"
            f"Cite as: {cite_labels(r)}\n"
            f"Location: {r['title']} › {r['location']}\n"
            f"Link: {r['url']}\n"
            f"{r['text']}"
        )
    return "\n\n---\n\n".join(blocks)


@mcp.tool()
def search(query: str) -> str:
    """Search four legal texts, in Spanish, on shipwrecks and objects found underwater:
    Spain's Historical Heritage Law (Ley 16/1985: archaeological finds, permits, fines),
    Spain's Maritime Navigation Law (Ley 14/2014: salvage, sunken ships and goods, extraction),
    the UNESCO 2001 Convention on the Protection of the Underwater Cultural Heritage,
    and the UN Convention on the Law of the Sea (UNCLOS: sea zones, archaeological objects at sea).

    Use it for any question about who owns a wreck or a find, reporting duties, permits,
    salvage rewards, fines or sea zones. The query can be in English; Spanish legal terms
    (e.g. "hallazgo casual", "buque naufragado") often match better.

    Returns the 5 most similar passages, best first. Each has a "Cite as" label
    (document and article) to cite it by, its location, a link to the official text,
    and the passage itself in Spanish.
    """
    query = query.strip()
    if not query:
        raise ToolError("The query is empty: pass the question or the terms to search for.")
    try:
        results = index.search(query, k=TOP_K)
    except index.QuotaExhausted as e:
        raise ToolError(f"{e} Search works again after 09:00 Spanish time.") from e
    if not results:
        return "No passages found. The index is empty: run `uv run python main.py index`."
    return format_results(results)


@mcp.tool()
def add_document(path: str) -> str:
    """Add a document to the searchable index: a BOE XML, PDF, HTML, Markdown or text file
    at `path` on this computer. It is split into articles, pages or sections, embedded and
    stored, so later searches can find it.

    Use it only when the user asks to add a specific file. If the same content is already
    indexed, nothing is embedded again. If a document with the same name but different
    content is indexed, its old passages are replaced by the new ones.

    Returns what was added: the document's name, how many sections and words it has,
    and the label to cite its passages by.
    """
    try:
        report = index.index_file(path)
    except (FileNotFoundError, ValueError) as e:
        raise ToolError(str(e)) from e
    except index.QuotaExhausted as e:
        raise ToolError(f"{e} Nothing was lost; run add_document again after 09:00 Spanish time.") from e
    designs = "; ".join(f"{d}: {status}" for d, status in report["designs"].items())
    return (
        f"Document '{report['title']}' is indexed as source '{report['source']}' "
        f"({report['units']} sections, {report['words']:,} words). {designs}. "
        f"Cite its passages as [{report['source']}, <section>], with the section shown in each search result."
    )


if __name__ == "__main__":
    mcp.run()
