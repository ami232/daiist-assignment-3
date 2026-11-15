"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Loads index/ at startup and never re-embeds the corpus. Prints nothing to
stdout (it carries the protocol); logs go to stderr. Docstrings become the
tool descriptions the model reads.
"""

from pathlib import Path

from mcp.server.mcpserver import MCPServer

import index

ROOT = Path(__file__).resolve().parent

mcp = MCPServer("corpus", log_level="WARNING")
index.load_chunks()   # load the committed index once at startup; nothing is re-embedded


@mcp.tool()
def search(query: str, k: int = 5) -> str:
    """Search EU digital-regulation law: the AI Act (Regulation 2024/1689), the GDPR
    (Regulation 2016/679) and the Digital Services Act (Regulation 2022/2065), plus any
    documents added later with add_document.

    Use it for any question about what these laws require, allow or prohibit, e.g.
    consent, data subject rights, high-risk or prohibited AI, transparency, platform
    duties, fines and deadlines. Ask in plain words; search again with different
    wording or a narrower question if the passages do not answer it.

    Returns the k (default 5, max 10) most relevant passages. Each starts with
    "Cite as: <law>, <Article N | Recital N | Annex N>" and its type: articles and
    annexes are binding law, recitals only explain how to read them. The texts are
    the versions published in 2016-2024; later amendments, guidance and enforcement
    decisions are not included unless added.
    """
    k = max(1, min(int(k), 10))
    try:
        return index.format_results(index.search(query, k=k))
    except index.DailyQuotaExhausted:
        return ("Search unavailable: the daily Gemini embedding quota is used up, so this query "
                "cannot be embedded. Questions asked before still work. Try again after 09:00 (Spain).")


@mcp.tool()
def add_document(path: str) -> str:
    """Add a document to the searchable corpus: a EUR-Lex regulation (.html/.xhtml, split
    into recitals, articles and annexes), a PDF (split by page) or a .txt/.md file.

    `path` is a file on this machine, absolute or relative to the project folder.
    The file is chunked with the same pipeline as the corpus, embedded and stored.
    If the same file with the same content is already indexed, nothing is added.
    If a file with the same name is indexed with different content, its old
    chunks are replaced by the new version.

    Returns what happened: chunks added or replaced, and the citation name to use.
    """
    file = Path(path).expanduser()
    if not file.is_absolute():
        file = ROOT / file
    if not file.is_file():
        return f"Not added: no file at {file}."
    try:
        chunks = index.chunk_file(file)
    except ValueError as error:
        return f"Not added: {error}"
    if not chunks:
        return f"Not added: no text could be extracted from {file.name}."

    store = index.collection()
    new_ids = {c["id"] for c in chunks}
    old_ids = set(store.get(where={"file": file.name}, include=[])["ids"])
    source = chunks[0]["source"]

    if old_ids == new_ids:
        return f"Already indexed: {file.name} ({len(old_ids)} chunks, cited as '{source}'). Nothing added."

    try:
        added, _ = index.embed_and_store(chunks)
    except index.DailyQuotaExhausted:
        index.load_chunks(refresh=True)
        stored = len(store.get(where={"file": file.name}, include=[])["ids"])
        return (f"Not added: the daily Gemini embedding quota is used up ({stored} of {len(chunks)} chunks "
                f"of {file.name} stored so far; these are kept). Run add_document again after 09:00 (Spain) "
                f"to embed the rest.")
    stale = old_ids - new_ids
    if stale:
        store.delete(ids=sorted(stale))
    index.load_chunks(refresh=True)
    action = f"Replaced the previous version of {file.name}" if old_ids else f"Added {file.name}"
    return (f"{action}: {added} chunks embedded, {len(stale)} old chunks removed, "
            f"{len(new_ids)} chunks in total. Cite it as '{source}' (locations like "
            f"'{chunks[0]['location']}').")


if __name__ == "__main__":
    mcp.run()  # stdio
