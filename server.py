"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Loads index/ at startup and never re-embeds the corpus. Prints nothing to
stdout (it carries the protocol); index.py logs to stderr.
"""

from __future__ import annotations

from pathlib import Path

from mcp.server.mcpserver import MCPServer

import index

ROOT = Path(__file__).resolve().parent
ALLOWED_SUFFIXES = {".pdf", ".html", ".htm", ".txt", ".md"}
MAX_FILE_MB = 20

mcp = MCPServer("corpus", log_level="WARNING")

# Open the committed index once, at startup.
COLLECTION = index.collection(index.DEFAULT_DESIGN)


def format_results(results: list[dict]) -> str:
    blocks = []
    for n, r in enumerate(results, 1):
        m = r["metadata"]
        # The structure design starts each chunk with "Title > Section"; the
        # citation line below already says that, so drop it from the text.
        text = r["text"].split("\n", 1)[1] if r["text"].startswith(m["title"] + " > ") else r["text"]
        date = f", {m['date']}" if m.get("date") else ""
        blocks.append(
            f"[{n}] {m['title']} — {m['location']}{date}\n"
            f"source: {m['source']} | url: {m['url']} | relevance: {1 - r['distance']:.2f}\n"
            f"{text}"
        )
    return "\n\n---\n\n".join(blocks)


@mcp.tool()
def search(query: str, k: int = 5) -> str:
    """Search the official European Commission rules on Erasmus+ grants for
    university students: the Erasmus+ Programme Guide 2026 (who can take part,
    student mobility for studies and traineeships, durations, grant amounts and
    top-ups, glossary), the Erasmus Charter for Higher Education guidelines, the
    Learning Agreement for Studies guidelines and the Erasmus+ Student Charter.

    Use it for any question about Erasmus+ eligibility, duration, money,
    learning agreements, credit recognition or students' rights. Questions may
    be in English or Spanish; the documents are in English. It does NOT contain
    national amounts (e.g. SEPIE in Spain) or any university's own deadlines,
    places or selection criteria.

    Returns the k most relevant passages (default 5, max 10), numbered [1]..[k],
    each with document title, page or section, date, URL and the passage text.
    Cite them by number and by document + page/section.
    """
    if not query.strip():
        return "Empty query: say what to search for."
    k = max(1, min(int(k), 10))
    try:
        results = index.search(query, k=k, design=index.DEFAULT_DESIGN)
    except index.DailyQuotaExhausted:
        return "Search is unavailable: the daily embedding quota is used up. Try again after 09:00 (Spain)."
    if not results:
        return "No passages found. The index is empty."
    return format_results(results)


@mcp.tool()
def add_document(path: str) -> str:
    """Add a document to the Erasmus+ search index so search can find it.

    `path` is a file inside this project folder: .pdf, .html, .txt or .md.
    The file is extracted, cleaned and chunked with the same pipeline as the
    original corpus (index.py), embedded and stored. Its id is the file name.

    If the document is already indexed and unchanged, nothing is embedded and
    nothing is duplicated. If a file with the same name was indexed before but
    its content changed, its old chunks are replaced by the new ones.

    Returns how many chunks were embedded, reused, already present and removed.
    """
    file = Path(path).expanduser()
    if not file.is_absolute():
        file = ROOT / file
    file = file.resolve()
    if not file.is_relative_to(ROOT):
        return f"Refused: {path} is outside the project folder. Copy it into the project first."
    if not file.is_file():
        return f"Not found: {path}"
    if file.suffix.lower() not in ALLOWED_SUFFIXES:
        return f"Unsupported file type {file.suffix}. Use one of: {', '.join(sorted(ALLOWED_SUFFIXES))}."
    if file.stat().st_size > MAX_FILE_MB * 1e6:
        return f"Refused: the file is larger than {MAX_FILE_MB} MB."

    source = index.source_for_file(file)
    try:
        chunks = index.chunk_file(file, source, design=index.DEFAULT_DESIGN)
    except Exception as error:  # noqa: BLE001 - report extraction failures to the model
        return f"Could not read {file.name}: {type(error).__name__}: {error}"
    if not chunks:
        return f"No text found in {file.name}; nothing was added."

    try:
        counts = index.embed_and_store(chunks, design=index.DEFAULT_DESIGN)
    except index.DailyQuotaExhausted:
        return ("Stopped: the daily embedding quota is used up. The chunks embedded so far are saved; "
                "run add_document again after 09:00 (Spain) to finish.")

    if counts["embedded"] == 0 and counts["reused"] == 0 and counts["pruned"] == 0:
        status = "Already indexed and unchanged: nothing was added."
    elif counts["pruned"]:
        status = "Document had changed: its old chunks were replaced."
    else:
        status = "Document added."
    return (
        f"{status}\n"
        f"document id: {source['id']} | title: {source['title']} | chunks: {len(chunks)}\n"
        f"embedded: {counts['embedded']} | reused: {counts['reused']} | "
        f"already present: {counts['already_indexed']} | removed: {counts['pruned']} | "
        f"index now holds {counts['total']} chunks"
    )


if __name__ == "__main__":
    mcp.run()  # stdio
