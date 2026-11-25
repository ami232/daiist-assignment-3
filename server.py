"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Load index/ at startup; never re-embed the corpus. Print nothing to stdout
(it carries the protocol); log to stderr. Docstrings become the tool
descriptions the model reads.
"""

import sys
from pathlib import Path

import index  # the one pipeline: server.py never re-implements chunking or embedding
from mcp.server.mcpserver import MCPServer

mcp = MCPServer("corpus", log_level="WARNING")

TOP_K = 5  # chunks returned per search


def log(message: str) -> None:
    print(message, file=sys.stderr, flush=True)  # stdout is the MCP protocol channel


@mcp.tool()
def search(query: str) -> str:
    """Search the US federal workplace-rules corpus and return the most relevant passages.

    The corpus is the text of three parts of Title 29 of the Code of Federal Regulations
    (eCFR snapshot of 1 November 2026): Part 825 (Family and Medical Leave Act: who is
    eligible, how much leave, notice, certification, job protection), Part 785 (what counts
    as hours worked) and Part 531 (wage payments under the Fair Labor Standards Act).
    It covers federal rules only: no state law, no company policy, no case law.
    Documents added later with add_document are searched too.

    Use it for every question about these rules, and answer only from what it returns.
    It returns up to 5 passages, best first. Each has a source (for example
    "29 CFR Part 825"), a location (for example "§ 825.200") and a relevance score.
    The passages are always the closest ones in the corpus, even when none of them answers
    the question: read them, and if they do not contain the answer, say the corpus does not cover it.

    Args:
        query: the question or the key terms to look for, in English.
    """
    query = query.strip()
    if not query:
        return "Error: the query is empty."
    try:
        hits = index.retrieve(query, k=TOP_K, design=index.ACTIVE_DESIGN)
    except Exception as error:  # noqa: BLE001 - report to the model instead of crashing the server
        log(f"search failed: {type(error).__name__}: {error}")
        return f"Error: the search failed ({type(error).__name__})."
    if not hits:
        return "No passages found: the index is empty."
    blocks = []
    for number, hit in enumerate(hits, start=1):
        blocks.append(
            f"[{number}] {hit['source']}, {hit['location']} (relevance {hit['score']:.2f})\n{hit['text']}"
        )
    return "\n\n".join(blocks)


@mcp.tool()
def add_document(path: str) -> str:
    """Add one document to the corpus so that later searches can use it. This changes the index.

    The document must be an eCFR XML file already saved in the corpus/ folder, for example
    "corpus/29cfr778_2026-11-01.xml". Any other path or file type is refused.
    The file is cleaned, split into chunks and embedded. A document that is already indexed
    is not embedded twice: unchanged chunks are kept, and chunks that no longer exist in the
    file are removed. It returns how many chunks were embedded, kept and removed.

    Only call it when the user asks to add a document, never to answer a question.

    Args:
        path: path of the file inside the corpus/ folder.
    """
    corpus = index.CORPUS_DIR.resolve()
    target = (index.ROOT / path).resolve()  # an absolute path stays as it is
    if corpus not in target.parents:
        return f"Refused: only files inside {corpus.name}/ can be added."
    if not target.is_file():
        return f"Error: no file at {path}."
    try:
        stats = index.index_file(target, index.ACTIVE_DESIGN)
    except Exception as error:  # noqa: BLE001
        log(f"add_document failed: {type(error).__name__}: {error}")
        return f"Error: could not add {path} ({type(error).__name__}: {str(error)[:200]})."
    return (
        f"Indexed {stats['source']} ({target.name}): {stats['chunks']} chunks, "
        f"{stats['embedded']} newly embedded, {stats['kept']} already stored, "
        f"{stats['deleted']} removed."
    )


if __name__ == "__main__":
    log(f"corpus server: design {index.ACTIVE_DESIGN}, {index.get_collection(index.ACTIVE_DESIGN).count()} chunks loaded")
    mcp.run()  # stdio
