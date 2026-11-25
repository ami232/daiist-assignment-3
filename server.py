"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Loads index/ at startup; never re-embeds the corpus. Prints nothing to stdout
(it carries the protocol); everything is logged to stderr by index.py.
"""

from pathlib import Path

from mcp.server.mcpserver import MCPServer

import index

mcp = MCPServer("corpus", log_level="WARNING")

TOP_K = 5


@mcp.tool()
def search(query: str) -> str:
    """Search the vaccination guidance corpus and return the most relevant passages.

    The corpus is public-health guidance for clinicians: seven CDC Pink Book
    chapters (general best practice for immunization, vaccine safety, hepatitis B,
    measles, mumps, pertussis, rubella) and two ECDC measles documents (a 2024
    threat assessment brief and a 2014 report on measles and rubella elimination).
    Use it for any question about vaccine timing, contraindications, precautions,
    schedules, safety, or these diseases. It does not cover national schedules
    (for example Spain's), other diseases or vaccines, or anything outside these
    documents; if the passages returned do not answer the question, say so.

    Returns the top 5 passages. Each starts with "[n] source | location" and a
    similarity score (higher is closer), followed by the passage text. Cite a
    passage by its source and location.
    """
    try:
        results = index.search_chunks(query, k=TOP_K)
    except index.QuotaExhausted:
        return "Search is unavailable: the daily embedding limit has been reached. Try again later."
    except Exception as error:  # noqa: BLE001 - the model should see what went wrong
        return f"Search failed: {type(error).__name__}: {error}"
    if not results:
        return "The index is empty. Run `uv run python main.py index` first."
    return "\n\n".join(
        f"[{n}] {r['source']} | {r['location']} (similarity {1 - r['distance']:.2f})\n{r['text']}"
        for n, r in enumerate(results, 1)
    )


@mcp.tool()
def add_document(path: str) -> str:
    """Add a local document to the corpus so that search can find it.

    Takes the path of a file on this computer (.pdf, .html, .htm, .txt or .md).
    The file is cleaned, split into passages with source and location, embedded
    and stored in the index; this uses embedding quota. The source name is the
    file name without its extension. If the same document is already indexed,
    nothing is added and the result says so. Returns how many passages were added.
    """
    name = Path(path).stem
    try:
        result = index.index_file(path)[0]
    except (FileNotFoundError, ValueError) as error:
        return f"Error: {error}"
    except Exception as error:  # noqa: BLE001
        return f"Error: could not index {path}: {type(error).__name__}: {error}"
    if result["added"] == 0 and result["left"] == 0:
        return f"'{name}' is already indexed ({result['already_indexed']} passages). Nothing was added."
    message = f"Added {result['added']} passages from '{name}' ({result['already_indexed']} were already indexed)."
    if result["left"]:
        message += (
            f" {result['left']} passages are still missing because the daily embedding limit was reached;"
            " call add_document again later. Passages already saved are not embedded twice."
        )
    return message


if __name__ == "__main__":
    mcp.run()  # stdio
