"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Loads index/ at startup and never re-embeds the corpus. Prints nothing to
stdout (it carries the protocol); logs go to stderr.
"""

import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import index as ix  # noqa: E402  (the same pipeline main.py index uses)

DESIGN = ix.DEFAULT_DESIGN  # "structured", chosen in the retrieval comparison
DEFAULT_K = 5
SUPPORTED = {".pdf", ".txt", ".md", ".html", ".htm"}

collection = ix.get_collection(DESIGN)  # load the committed index once, at startup
ix.log(f"corpus server: {collection.count()} chunks loaded from index/ ({DESIGN})")

mcp = MCPServer("corpus", log_level="WARNING")


def format_results(results: dict) -> str:
    blocks = []
    for n, (text, meta, dist) in enumerate(
        zip(results["documents"][0], results["metadatas"][0], results["distances"][0]), start=1
    ):
        citation = f"{meta['source']}, {meta['location']}"
        blocks.append(
            f"[{n}] {citation}\n"
            f"cite as: [{citation}]\n"
            f"relevance: {1 - dist:.2f}\n"
            f"url: {meta.get('url') or meta.get('file', '')}\n"
            f"{text}"
        )
    return "\n\n---\n\n".join(blocks)


@mcp.tool()
def search(query: str, k: int = DEFAULT_K) -> str:
    """Search IE University's official student rules and policies.

    The corpus holds: the Academic Regulations for Bachelor Degree Programmes,
    the Academic Regulations for Master Degree Programmes, the Bachelor Attendance
    Policy, the Student Code of Conduct (academic integrity, sanctions, appeals,
    discrimination and harassment procedures), the Student Guidelines on AI, the
    Code for the Prevention of Harassment, the Equal Opportunities and Diversity
    Plan, the Environmental Policy and the Climate and Sustainability Plan.

    Use it for any question about attendance, absences, grades, exams, appeals,
    progression, academic integrity, AI use in coursework, harassment reporting or
    sustainability at IE. Ask in plain language; search again with other words, or
    once per sub-question, if the first results do not cover the question.

    Returns the k most relevant passages (default 5, max 10), each with a
    "cite as: [Document, p. X, Article/section]" line to copy into the answer, a
    relevance score from 0 to 1 and the passage text. Cite only what the passages
    say; if none answers the question, say the documents do not cover it.
    """
    query = query.strip()
    if not query:
        raise ToolError("query is empty")
    k = max(1, min(int(k), 10))
    results = collection.query(query_embeddings=[ix.embed_query(query)], n_results=k)
    if not results["documents"][0]:
        return "The index is empty."
    return format_results(results)


@mcp.tool()
def add_document(path: str) -> str:
    """Add one document (PDF, TXT, MD or HTML file on disk) to the searchable corpus.

    The file is extracted, cleaned, chunked with source and page/section metadata,
    embedded and stored in the index that `search` uses. If the same file (same name,
    same content) is already indexed, nothing is embedded and nothing changes. If a
    file with the same name was indexed before with different content, its old
    chunks are replaced by the new ones. Relative paths are resolved from the
    project folder.

    Returns the document title used in citations and how many chunks were added,
    already present or removed.
    """
    file = Path(path).expanduser()
    if not file.is_absolute():
        file = ROOT / file
    file = file.resolve()
    if not file.is_file():
        raise ToolError(f"No such file: {file}")
    if file.suffix.lower() not in SUPPORTED:
        raise ToolError(f"Unsupported file type {file.suffix}; use one of {', '.join(sorted(SUPPORTED))}")

    # a corpus file keeps its corpus title, so re-adding it is recognised as already indexed
    doc = next((d for d in ix.CORPUS if d["file"] == file.name), None) or {
        "title": file.stem.replace("_", " ").replace("-", " ").strip(),
        "file": file.name,
        "url": "",
    }
    stats = ix.index_file(file, doc, designs=[DESIGN])[DESIGN]

    if stats["embedded"] == 0 and stats["removed_stale"] == 0:
        status = "Already indexed with the same content: nothing was embedded or changed."
    elif stats["removed_stale"]:
        status = "This document was indexed before with different content: its old chunks were replaced."
    else:
        status = "New document added."
    return (
        f"{status}\n"
        f"title (used in citations): {doc['title']}\n"
        f"chunks in document: {stats['chunks']}, newly embedded: {stats['embedded']}, "
        f"already present: {stats['already_indexed']}, old chunks removed: {stats['removed_stale']}\n"
        f"index now holds {collection.count()} chunks."
    )


if __name__ == "__main__":
    mcp.run()  # stdio
