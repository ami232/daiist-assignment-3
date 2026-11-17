"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns the top passages with source and page, ready to cite.
- add_document(path): runs one file through index.py's pipeline, embeds it and stores it.

Loads index/ at startup and never re-embeds the corpus (only the query is embedded).
Prints nothing to stdout (it carries the protocol); logs go to stderr.

Set CORPUS_ONLY=1 to search only the original corpus (evaluate.py does, so documents
added later through add_document don't change the test results).
"""

import os
import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer

import index
import rag

mcp = MCPServer("corpus", log_level="WARNING")

_searcher: rag.Searcher | None = None


def searcher() -> rag.Searcher:
    global _searcher
    if _searcher is None:
        _searcher = rag.Searcher(rag.PRODUCTION["design"], corpus_only=os.environ.get("CORPUS_ONLY") == "1")
        rag.log(f"[corpus] loaded {len(_searcher.ids)} chunks from index/ ({rag.PRODUCTION})")
    return _searcher


@mcp.tool()
def search(query: str) -> str:
    """Search a library of open-access scientific papers about padel: padel rackets (shape, weight,
    balance, moment of inertia, maneuverability, sweet spot, vibration) and padel injuries
    (incidence, prevalence, elbow/shoulder injuries, risk factors such as racket weight or hours
    played), plus reviews of padel performance research and youth padel.

    Use it for any factual question on these topics, before answering. Write the query as a short
    description of the information needed (e.g. "racket weight 350 g injury risk"); search again
    with different words if the first results don't contain the answer.

    Returns the 5 most relevant passages. Each starts with a header such as
    "cite as [munoz2022 p.5]", followed by the paper title, year and section, then the passage text.
    Cite facts with exactly that tag. If no passage contains the answer, the corpus does not cover it.
    """
    query = (query or "").strip()
    if not query:
        return "Empty query: describe what you are looking for."
    try:
        results = searcher().search(query, k=rag.PRODUCTION["k"], hybrid=rag.PRODUCTION["hybrid"])
    except Exception as error:  # noqa: BLE001 - report to the model instead of crashing the server
        rag.log(f"[corpus] search failed: {error!r}")
        return f"Search failed: {type(error).__name__}: {error}"
    return rag.format_results(results)


@mcp.tool()
def add_document(path: str) -> str:
    """Add one document (a .pdf, .txt, .md or .html file on this computer) to the padel corpus:
    extracts and cleans its text, splits it into chunks with page numbers, embeds the chunks
    with Gemini and stores them in the index, so search can find it immediately.

    `path` is the file's path (absolute, or relative to the project folder).
    If the identical file is already indexed, nothing is changed. If a document with the same
    name but different content is indexed, its old chunks are replaced by the new version.
    Returns what happened: the document id to cite, the number of chunks, and how many were embedded.
    """
    p = Path(path).expanduser()
    if not p.is_absolute():
        p = (Path(__file__).resolve().parent / p).resolve()
    try:
        result = index.index_file(p)
    except (FileNotFoundError, ValueError) as error:
        return f"Not added: {error}"
    except Exception as error:  # noqa: BLE001
        rag.log(f"[corpus] add_document failed: {error!r}")
        return f"Not added: {type(error).__name__}: {error}"
    if _searcher is not None:
        _searcher.reload()
    if result["status"] == "already_indexed":
        return (f"Already indexed: identical file as document '{result['doc_id']}' "
                f"({result['chunks']} chunks). Nothing was changed and nothing was embedded.")
    verb = "Replaced the previous version of" if result["status"] == "replaced" else "Added"
    return (f"{verb} document '{result['doc_id']}' from {p.name}: {result['chunks']} chunks, "
            f"{result['embedded']} newly embedded. Cite it as [{result['doc_id']} p.N].")


if __name__ == "__main__":
    print(f"[corpus] MCP server starting (python {sys.version.split()[0]})", file=sys.stderr)
    mcp.run()  # stdio
