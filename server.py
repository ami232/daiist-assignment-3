"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

The index in index/ is loaded once at startup and never re-embedded. Nothing is
printed to stdout (it carries the protocol); logs go to stderr.
"""

from pathlib import Path

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

import rag

mcp = MCPServer("corpus", log_level="WARNING")

MAX_NEW_CHUNKS = 400   # one add_document call may not spend more than this many embeddings
_index: rag.Index | None = None


def get_index() -> rag.Index:
    global _index
    if _index is None:
        _index = rag.Index()
        rag.log(f"loaded {len(_index)} chunks from index/")
    return _index


@mcp.tool()
def search(query: str) -> str:
    """Search OSHA's construction safety standards (29 CFR Part 1926) and get the closest passages.

    The corpus holds seven subparts: E (personal protective equipment), K (electrical),
    L (scaffolds), M (fall protection), P (excavations and trenching), Q (concrete and
    masonry) and X (stairways and ladders). Use this tool before answering any question
    about construction site safety rules, heights, loads, distances, training or
    inspection duties. It does not cover other OSHA parts, penalties, other countries,
    or any subpart not listed, unless a document was added later.

    Give a short, specific query in plain words, for example "guardrail top rail height"
    or "trench egress ladder distance". Call it again with different wording, or once per
    part of a multi-part question, if the first results do not contain the answer.

    Returns up to 5 passages ranked by relevance. Each has a 'Cite as' label (source and
    section) to copy into the answer, its document, and its text. The passages are only
    the closest matches. They may not answer the question, so read them before relying on them.
    """
    hits = get_index().search(query, k=rag.TOP_K)
    return rag.format_hits(hits)


@mcp.tool()
def add_document(path: str) -> str:
    """Add one more document to the search index so that later searches can use it.

    Takes the path of a local file (relative to the project folder or absolute). Supported:
    .xml (an eCFR export of a subpart), .pdf, .txt, .md and .html. The file is cleaned,
    cut into chunks with source and section metadata, embedded and stored.

    If the same content is already indexed, nothing is embedded and the call says so.
    If a file with the same source name has changed, its old chunks are replaced.
    This spends embedding quota and changes the shared index, so only call it when the
    user asked for a document to be added. Returns how many chunks were added, skipped
    or replaced.
    """
    import index as pipeline  # imported here so search-only sessions start faster

    target = Path(path).expanduser()
    if not target.is_absolute():
        target = rag.ROOT / target
    if not target.is_file():
        raise ToolError(f"No file at {path!r}. Give the path of an existing file.")

    try:
        chunks = pipeline.chunk_file(target)
        if len(chunks) > MAX_NEW_CHUNKS:
            raise ToolError(
                f"{target.name} makes {len(chunks)} chunks, above the limit of {MAX_NEW_CHUNKS} per call. "
                f"Split it into smaller files so it fits in the daily embedding quota."
            )
        stats = pipeline.embed_and_store(chunks, replace=True, quiet=True)
    except (ValueError, RuntimeError) as error:
        raise ToolError(str(error)) from error
    get_index().reload()

    source = chunks[0]["source"]
    if stats["embedded"] == 0 and stats["removed"] == 0:
        return (f"Already indexed: {target.name} (source '{source}') has {stats['chunks']} chunks "
                f"and none changed, so nothing was embedded.")
    return (f"Added {target.name} as source '{source}': {stats['chunks']} chunks, "
            f"{stats['embedded']} newly embedded, {stats['already_indexed']} unchanged, "
            f"{stats['removed']} old chunks replaced. The index now has {len(get_index())} chunks.")


if __name__ == "__main__":
    mcp.run()  # stdio
