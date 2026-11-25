"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Loads index/ at startup and never re-embeds the corpus. Nothing is printed to
stdout (it carries the protocol); problems go to stderr.
"""

import sys
from pathlib import Path
from typing import Annotated

from mcp.server.mcpserver import MCPServer
from pydantic import Field

import index as ix
import retrieval as rt

mcp = MCPServer("corpus", log_level="WARNING")

ROOT = Path(__file__).resolve().parent
# add_document may only read files from these folders. A prompt-injected agent
# must not be able to index (and later quote) any file on the machine.
ALLOWED_DIRS = [ROOT]
FORBIDDEN_PARTS = {".git", ".env", "index", ".venv", "__pycache__"}

VIEW = rt.IndexView(ix.CHOSEN_DESIGN)
print(f"corpus server: {len(VIEW)} chunks loaded ({', '.join(VIEW.sources()) or 'empty index'})", file=sys.stderr)


@mcp.tool()
def search(
    query: Annotated[str, Field(description="What to look for, in English, e.g. 'time limit to notify a personal data breach'.")],
    source: Annotated[str, Field(description="Optional document name to restrict the search to, e.g. 'GDPR'. Empty searches everything.")] = "",
    k: Annotated[int, Field(description="Number of passages to return, 1 to 8.")] = 5,
) -> str:
    """Search the compliance corpus: EU legislation on artificial intelligence and data, split into
    passages. Indexed documents are listed by the `source` names in the results (initially the
    AI Act, the GDPR and the Data Act; more can be added with add_document).

    Use it for every question about what these texts require, allow, define or prohibit. Write the
    query as a short natural-language description of the rule you need, in English, and repeat the
    search with different wording or per document if the first passages do not answer. The text
    only contains the legislation itself: no case law, guidance, national law or opinions.

    Args:
        query: what to look for, e.g. "time limit to notify a personal data breach".
        source: optional document name to restrict the search to, e.g. "GDPR". Leave empty to search everything.
        k: number of passages to return (1-8, default 5).

    Returns passages best first. Each starts with a line `[n] source | location \u2014 "title" (similarity x)`;
    cite exactly as [source | location]. Similarity is cosine similarity: low values (below about
    0.5) usually mean the passage is only loosely related. A passage marked `(keyword match)` was found
    by its words only (its vector is missing or the embedding quota is used up) and has no similarity:
    judge it by its text. Returns "No passages found." when the filter matches nothing.
    """
    query = (query or "").strip()
    if not query:
        return "Error: query is empty."
    k = max(1, min(int(k), 8))
    try:
        hits = VIEW.search(query, k=k, mode=rt.CHOSEN_MODE, source=source.strip() or None)
    except ix.QuotaExhausted:  # normally handled inside the search (keyword ranking); kept as a safety net
        return "Error: the embedding quota is exhausted, search is unavailable right now."
    except Exception as error:  # noqa: BLE001 - the model should see why, not a stack trace
        print(f"search failed: {type(error).__name__}: {error}", file=sys.stderr)
        return f"Error: search failed ({type(error).__name__})."
    if source.strip() and not hits:
        return f"No passages found. Known sources: {', '.join(VIEW.sources())}."
    return rt.format_hits(hits)


def _checked_path(path: str) -> Path:
    p = Path(path).expanduser()
    p = (p if p.is_absolute() else ROOT / p).resolve()
    if not any(p == d or d in p.parents for d in ALLOWED_DIRS):
        raise ValueError(f"{path!r} is outside the project folder. Copy the file into the project (for example corpus/) first.")
    if FORBIDDEN_PARTS & set(p.relative_to(ROOT).parts):
        raise ValueError(f"{path!r} is not allowed to be indexed.")
    if not p.is_file():
        raise ValueError(f"{path!r} is not a file.")
    if p.suffix.lower() not in ix.ALLOWED_SUFFIXES:
        raise ValueError(f"Unsupported file type {p.suffix!r}. Use one of {sorted(ix.ALLOWED_SUFFIXES)}.")
    if p.stat().st_size > ix.MAX_FILE_MB * 1_000_000:
        raise ValueError(f"{path!r} is larger than {ix.MAX_FILE_MB} MB.")
    return p


@mcp.tool()
def add_document(
    path: Annotated[str, Field(description="File inside the project folder, e.g. 'corpus/nis2.xhtml'.")],
) -> str:
    """Add one document to the corpus so that `search` can find it. Runs the same pipeline as the
    initial index: extract the text, clean it, split it into passages that keep their source and
    location, embed them and store them. Takes a few seconds per 100 passages and uses embedding quota.

    Only files inside the project folder are accepted (.xhtml, .html, .pdf, .txt, .md; up to
    25 MB). The user must approve each call. Use it only when the user asks to add a document.

    If the daily embedding quota is used up, the passages are still added and found by keyword
    search; add the same file again after the quota resets to create their vectors.

    If the same file (identical content) is already indexed nothing is embedded and the existing
    entry is reported. If a file with the same name but different content is added, the old
    passages of that document are replaced; unchanged passages keep their saved vectors.

    Args:
        path: path of the file, relative to the project folder or absolute, e.g. "corpus/nis2.xhtml".

    Returns a one-line summary: status (added, replaced or already indexed), the source name to use
    in `search`, and the number of passages.
    """
    try:
        p = _checked_path(path)
        result = ix.index_file(p, ix.CHOSEN_DESIGN, keyword_fallback=True)
    except ix.QuotaExhausted:
        return "Error: the embedding quota is exhausted. Passages embedded so far are saved; retry later."
    except (ValueError, OSError) as error:
        return f"Error: {error}"
    except Exception as error:  # noqa: BLE001
        print(f"add_document failed: {type(error).__name__}: {error}", file=sys.stderr)
        return f"Error: could not index the document ({type(error).__name__}: {error})."
    VIEW.reload()
    if result["status"] == "already_indexed":
        return (f"Already indexed as source '{result['source']}' ({result['chunks']} passages). "
                "Nothing was embedded.")
    verb = "Added" if result["status"] == "added" else "Replaced"
    if result.get("keyword_only"):
        return (f"{verb} source '{result['source']}': {result['chunks']} passages, now searchable by keyword only: the daily "
                f"embedding quota is used up, so {result['keyword_only']} of them have no vector yet "
                "(add the same file again after the quota resets to create them).")
    return (f"{verb} source '{result['source']}': {result['chunks']} passages "
            f"({result['embedded']} newly embedded, {result['reused']} reused). Now searchable.")


if __name__ == "__main__":
    mcp.run()  # stdio
