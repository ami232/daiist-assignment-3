"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it and stores it.

Loads index/ at startup; never re-embeds the corpus. Prints nothing to stdout (it carries the
protocol); everything is logged to stderr.
"""

import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer

import index
import retrieval

mcp = MCPServer("corpus", log_level="WARNING")

TOP_K = 5
MAX_FILE_MB = 30
ROOT = Path(__file__).resolve().parent
_retriever: retrieval.Retriever | None = None


def retriever() -> retrieval.Retriever:
    global _retriever
    if _retriever is None:
        _retriever = retrieval.Retriever(index.SERVING_DESIGN)
        print(f"[corpus] loaded {len(_retriever.chunks)} chunks ({index.SERVING_DESIGN})", file=sys.stderr)
    return _retriever


@mcp.tool()
def search(query: str) -> str:
    """Search the corpus of EBA (European Banking Authority) credit-risk guidelines and return the 5 best passages.

    Corpus: EBA/GL/2016/07 definition of default (Art. 178 CRR: days past due, unlikeliness to pay,
    return to non-defaulted status); EBA/GL/2017/16 PD estimation, LGD estimation and defaulted
    exposures; EBA/GL/2020/05 credit risk mitigation for A-IRB institutions; EBA/GL/2020/06 loan
    origination and monitoring; plus any document added with add_document. It holds the guidelines
    and their rationale only, not the CRR/CRD text, Basel texts, national rules or other EBA products.

    Use it before answering any question about what these guidelines require. Write the query as a
    short description of the rule you need (e.g. "materiality threshold days past due retail").
    Returns numbered passages, each with its citation in brackets, e.g. [EBA-GL-2017-16, p. 55], its
    section and paragraph numbers, and the text. If no passage answers the question, the corpus
    does not cover it: say so instead of guessing.
    """
    if not query or not query.strip():
        return "Empty query. Write what you want to find."
    try:
        r = retriever()
        hits = r.search(query.strip(), k=TOP_K, mode=retrieval.SERVING_MODE)
    except Exception as error:  # noqa: BLE001 - the model should see the failure, not a crash
        print(f"[corpus] search failed: {type(error).__name__}: {error}", file=sys.stderr)
        return f"Search failed ({type(error).__name__}). Try again or tell the user the search is unavailable."
    return retrieval.format_hits(query.strip(), hits, retrieval.SERVING_MODE)


def _check_path(path: str) -> tuple[Path | None, str]:
    p = Path(path).expanduser()
    p = (ROOT / p).resolve() if not p.is_absolute() else p.resolve()
    if ROOT not in p.parents:
        return None, f"Refused: files must be inside the project folder ({ROOT.name}/). Copy the file there first."
    if not p.is_file():
        return None, f"File not found: {p.relative_to(ROOT) if ROOT in p.parents else p}"
    if p.suffix.lower() not in index.ALLOWED_SUFFIXES:
        return None, f"Refused: {p.suffix} is not supported. Use one of {sorted(index.ALLOWED_SUFFIXES)}."
    if p.stat().st_size > MAX_FILE_MB * 1_000_000:
        return None, f"Refused: file is larger than {MAX_FILE_MB} MB."
    return p, ""


@mcp.tool()
def add_document(path: str) -> str:
    """Add one document (.pdf, .txt, .md or .html) from the project folder to the searchable index.

    The file goes through the same pipeline as the original corpus (extract, clean, chunk with
    page and section, embed, store), so afterwards `search` can return its passages with citations.
    Path is relative to the project folder, e.g. "new_docs/report.pdf"; files outside it are refused.

    If the same file (identical content) is already indexed nothing happens and it costs no
    embeddings. If a changed version of an indexed document arrives, its old passages are replaced.
    Uses the free embedding quota (about 1 text per 250 words), so add only what is needed.
    Returns the outcome: added, already_indexed, replaced_version or an error message.
    """
    p, error = _check_path(path)
    if p is None:
        return error
    try:
        result = index.index_file(p)
    except Exception as exc:  # noqa: BLE001
        print(f"[corpus] add_document failed: {type(exc).__name__}: {exc}", file=sys.stderr)
        return f"Could not add the document ({type(exc).__name__}: {exc})."
    if result["status"] in ("added", "replaced_version"):
        retriever().reload()  # the new passages are searchable right away
    return "; ".join(f"{k}={v}" for k, v in result.items())


if __name__ == "__main__":
    mcp.run()  # stdio
