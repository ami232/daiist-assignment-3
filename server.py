"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

Two tools over the TTS Handbook index built by index.py:

- search(query): the 5 most relevant handbook passages, each with a citation.
- add_document(path): runs a file through index.py's pipeline (clean, chunk,
  embed) and stores it in the index the search tool uses.

Policy when a document is already indexed (decided for this use case):
the document's source (its file name) identifies it.
    same content again   -> nothing is embedded, "already indexed"
    changed content      -> the old version's chunks are deleted and the new
                            ones stored; unchanged sections keep their vectors
An outdated HR rule left next to the new one could be quoted by the agent,
which is the kind of confident wrong answer this system must avoid.

The server loads the committed index and never re-embeds the corpus. It
prints nothing to stdout, which carries the MCP protocol; logs go to stderr.
Docstrings become the tool descriptions the model reads.
"""

import sys
from pathlib import Path

from google.genai import errors as genai_errors
from mcp.server.mcpserver import MCPServer
from mcp.types import ToolAnnotations

import index as ix

ROOT = Path(__file__).resolve().parent
ALLOWED_SUFFIXES = {".md", ".markdown", ".txt"}

mcp = MCPServer(
    "corpus",
    instructions=(
        "Search the TTS Handbook, the employee handbook of the Technology Transformation "
        "Services (US General Services Administration), and add documents to it."
    ),
    log_level="WARNING",
)


def log(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


def passage_text(chunk: dict) -> str:
    """The chunk's text without its first line, which repeats the citation path."""
    first, _, rest = chunk["text"].partition("\n\n")
    return rest if rest and first.startswith(chunk["title"]) else chunk["text"]


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=True, openWorldHint=False))
def search(query: str) -> str:
    """Search the TTS Handbook, the employee handbook of the Technology Transformation
    Services (TTS) at the US General Services Administration (GSA).

    It covers HR policy for TTS employees: leave of every kind (annual, sick,
    parental, FMLA, court, military, administrative, unpaid, donated), overtime,
    comp time and credit hours, work schedules, travel booking and reimbursement,
    personal foreign travel, benefits, equipment and IT rules, performance
    reviews, promotions, details, hiring, conduct, accommodations, and leaving TTS.

    Use it for any question about these policies, and search again with other
    words, or once per part of a question that has several parts, if the first
    results are not enough.

    Returns the 5 most relevant passages, best first. Each starts with a
    citation line, "[n] Page title › Section", then its source page, URL and a
    similarity score, then the passage text. The passages are the only
    evidence: if none of them contains the answer, the handbook does not cover
    the question, so say so instead of answering from general knowledge.
    """
    log(f"search: {query[:80]!r}")
    results = ix.retrieve(query, k=ix.SEARCH_K, design=ix.SEARCH_DESIGN, cache=False)
    blocks = []
    for n, chunk in enumerate(results, start=1):
        citation = f"{chunk['title']} › {chunk['location']}" if chunk["location"] != "Introduction" else chunk["title"]
        blocks.append(
            f"[{n}] {citation}\n"
            f"source: {chunk['source']} | url: {chunk['url']} | similarity: {chunk['score']:.2f}\n\n"
            f"{passage_text(chunk)}"
        )
    return "\n\n========\n\n".join(blocks)


def resolve_inside_project(path: str) -> Path:
    """The file's real location, refused if it is outside this project folder.

    Without this check, a confused or manipulated agent could index any file
    on the computer (keys, private notes), and indexing sends its text to
    Google for embedding.
    """
    candidate = Path(path).expanduser()
    if not candidate.is_absolute():
        candidate = ROOT / candidate
    resolved = candidate.resolve()  # follows "..", and symbolic links
    if not resolved.is_relative_to(ROOT):
        raise ValueError(f"refused: {path} is outside the project folder")
    if not resolved.is_file():
        raise ValueError(f"no such file: {path}")
    if resolved.suffix.lower() not in ALLOWED_SUFFIXES:
        raise ValueError(f"refused: only {', '.join(sorted(ALLOWED_SUFFIXES))} files can be added")
    return resolved


@mcp.tool(annotations=ToolAnnotations(readOnlyHint=False, destructiveHint=False, idempotentHint=True))
def add_document(path: str) -> str:
    """Add a Markdown or plain-text document to the TTS Handbook index, so that
    the search tool can find it.

    `path` is the file's path, absolute or relative to the project folder; files
    outside the project folder are refused. The document is cleaned, split into
    sections and embedded with the same pipeline as the rest of the handbook.
    Its file name identifies it: adding the same file again changes nothing,
    and adding a changed version replaces the old one.

    Returns what happened: added, updated or already indexed, with the number
    of passages embedded.
    """
    try:
        file = resolve_inside_project(path)
        chunks = ix.chunk_file(file, design="structure", origin="added")
    except ValueError as error:
        return str(error)
    if not chunks:
        return f"refused: no text found in {file.name}"

    collection = ix.get_collection("structure")
    source = chunks[0]["metadata"]["source"]
    title = chunks[0]["metadata"]["title"]
    before = set(collection.get(where={"source": source}, include=[])["ids"])
    new_ids = {c["id"] for c in chunks}

    try:
        # Embed the new version first, delete the old one only after: if
        # embedding stops halfway, the old version is still searchable.
        embedded = ix.embed_and_store(chunks, collection)
    except (ix.EmbeddingBudgetExceeded, genai_errors.APIError) as error:
        return (f"stopped while embedding {file.name}: {error}. "
                f"The passages saved so far are kept; call add_document again later to finish.")
    stale = sorted(before - new_ids)
    if stale:
        collection.delete(ids=stale)

    kept = len(chunks) - embedded
    if not before:
        status = f"added '{title}' ({source}): {embedded} passages embedded"
    elif embedded == 0 and not stale:
        status = f"already indexed: '{title}' ({source}) is unchanged, nothing embedded"
    else:
        status = (f"updated '{title}' ({source}): {embedded} new passages embedded, "
                  f"{kept} unchanged kept, {len(stale)} outdated removed")
    log(f"add_document: {status}")
    return status


if __name__ == "__main__":
    mcp.run()  # stdio
