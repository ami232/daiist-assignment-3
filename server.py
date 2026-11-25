"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

The index in index/ is loaded on demand and never rebuilt here. Nothing is
printed to stdout (it carries the protocol); logs go to stderr. The tool
docstrings are the descriptions the model reads, so they say what the corpus
is, when to use each tool and what comes back.
"""

from __future__ import annotations

from pathlib import Path

from mcp.server.mcpserver import MCPServer

import index

mcp = MCPServer("corpus", log_level="WARNING")

TOP_K = 5
ADD_SUFFIXES = (".pdf", ".txt", ".md")
MAX_ADD_BYTES = 50 * 1024 * 1024


def format_hits(hits: list[dict]) -> str:
    blocks = []
    for n, hit in enumerate(hits, 1):
        header = f"[{n}] {hit['source']} | {hit['location']} (score {hit['score']:.2f})"
        blocks.append(f"{header}\n{hit['text']}")
    return "\n\n".join(blocks)


@mcp.tool()
def search(query: str) -> str:
    """Search the EU cosmetics-regulation corpus and return the most relevant passages.

    The corpus is public EU law and guidance about selling cosmetic products in the EU:
    Regulation (EC) No 1223/2009 on cosmetic products (all articles and Annexes I and IV-X;
    Annexes II and III, the long lists of prohibited and restricted substances, are NOT
    indexed), Regulation (EU) No 655/2013 (common criteria for cosmetic claims), Commission
    Decision 2013/674 (guidelines on Annex I, the Cosmetic Product Safety Report), the
    Commission's CPNP notification user guide, and any document added with add_document.

    Use it for any question about what someone must do before or while placing a cosmetic
    product on the EU market: responsible person, safety assessment, product information
    file, notification (CPNP), labelling, claims, animal testing, distributors, serious
    undesirable effects, market surveillance. Do not use it for other topics, or to look up
    the limit of one specific ingredient.

    Args:
        query: the question or key phrase to look for, in English, for example
            "who can be the responsible person for a cosmetic product".

    Returns:
        Up to 5 passages, best first. Each starts with "[n] source | location (score)"
        followed by the passage text. Cite source and location when you answer. If none of
        the passages answers the question, say that the corpus does not answer it instead of
        guessing.
    """
    query = (query or "").strip()
    if not query:
        return "Error: the query is empty. Pass a question or key phrase."
    try:
        hits = index.search_chunks(query, k=TOP_K, design=index.DEFAULT_DESIGN)
    except Exception as error:  # noqa: BLE001 - the model should see what went wrong
        index.log(f"search failed: {error!r}")
        return f"Search failed: {type(error).__name__}: {error}"
    if not hits:
        return "No passages found. The index may be empty: run `uv run python main.py index`."
    return format_hits(hits)


@mcp.tool()
def add_document(path: str) -> str:
    """Add one new document to the search index, so that search can find it afterwards.

    Reads a local PDF, .txt or .md file that lives inside this project folder, splits it
    into passages, embeds them and stores them in the index. The document is cited under its
    file name without the extension. Adding the same file twice changes nothing. It uses the
    embedding quota and takes a few seconds per 10 pages, so only call it when the user
    wants the document added.

    Args:
        path: the file to add, relative to the project folder or absolute, but it must be
            inside the project folder, for example "corpus/new_guidance.pdf".

    Returns:
        How many passages the file has and how many were newly added, or a clear error
        message (file not found, unsupported type, outside the project folder, quota used up).
    """
    raw = (path or "").strip()
    if not raw:
        return "Error: the path is empty."
    file = Path(raw).expanduser()
    if not file.is_absolute():
        file = index.ROOT / file
    file = file.resolve()
    try:
        file.relative_to(index.ROOT)
    except ValueError:
        return f"Error: {raw} is outside the project folder. Copy it into {index.ROOT.name}/corpus/ first."
    if not file.is_file():
        return f"Error: there is no file at {raw}."
    if file.suffix.lower() not in ADD_SUFFIXES:
        return f"Error: {file.suffix or 'this file type'} is not supported. Use a PDF, .txt or .md file."
    if file.stat().st_size > MAX_ADD_BYTES:
        return f"Error: {file.name} is larger than {MAX_ADD_BYTES // (1024 * 1024)} MB."
    try:
        n_chunks, n_new = index.index_file(file, index.DEFAULT_DESIGN)
    except index.QuotaExhausted:
        return (
            f"{file.name} was not fully added: the embedding quota is used up for now. "
            "The part already embedded is saved; call add_document again later to finish."
        )
    except Exception as error:  # noqa: BLE001 - the model should see what went wrong
        index.log(f"add_document failed: {error!r}")
        return f"Could not add {file.name}: {type(error).__name__}: {error}"
    if n_new == 0:
        return f"{file.name} is already in the index ({n_chunks} passages); nothing was added."
    return f"Added {file.name}: {n_chunks} passages in the file, {n_new} newly embedded. search can now find it."


if __name__ == "__main__":
    mcp.run()  # stdio
