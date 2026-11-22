"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Load index/ at startup; never re-embed the corpus. Print nothing to stdout
(it carries the protocol); log to stderr. Docstrings become the tool
descriptions the model reads.
"""

import contextlib
import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer

import index

DESIGN = "b"          # which index to search and extend: "a" (fixed-size) or "b" (structure-based)
TOP_K = 5             # passages returned by search
MAX_FILE_MB = 25      # add_document refuses bigger files
ROOT = Path(__file__).resolve().parent

mcp = MCPServer("corpus", log_level="WARNING")

# Load the saved index once, at startup. Nothing here calls the embedding API.
with contextlib.redirect_stdout(sys.stderr):
    COLLECTION = index.get_collection(DESIGN)


def log(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


@mcp.tool()
def search(query: str) -> str:
    """Search the data-protection corpus and return the most relevant passages with citations.

    The corpus contains three documents: (1) the GDPR, Regulation (EU) 2016/679, articles 1-99
    (source "gdpr", cited as e.g. "Article 33" or "Article 33(1)-(3)"); (2) EDPB Guidelines 9/2022
    on personal data breach notification (source "edpb_breach_notification", cited as e.g.
    "para 33 (p.11)"); (3) EDPB Guidelines 07/2020 on the concepts of controller and processor
    (source "edpb_controller_processor", cited the same way). It does NOT contain national laws,
    court judgments beyond those quoted, cookies/ePrivacy rules, the AI Act or NIS2.

    Use it for any question about breach notification, controller and processor roles, data
    subject rights, DPOs, fines or other GDPR duties. Write the query as a short natural-language
    question or key phrase in English.

    Returns up to 5 passages, best match first. Each shows its source, its location (the citation)
    and a distance score (lower = closer match; a high distance means the passage may not answer
    the question). The search always returns passages, even for questions the corpus does not
    cover, so judge whether the passages really answer the question before relying on them.
    """
    query = (query or "").strip()
    if not query:
        return "Please give a non-empty query."
    try:
        with contextlib.redirect_stdout(sys.stderr):
            vector = index.embed_query(query)
        result = COLLECTION.query(
            query_embeddings=[vector],
            n_results=TOP_K,
            include=["documents", "metadatas", "distances"],
        )
    except index.DailyQuotaReached as error:
        return f"Search is unavailable right now: the embedding quota is used up ({str(error)[:120]}). Try again later."
    except RuntimeError as error:  # e.g. missing API key
        return f"Search is unavailable: {str(error)[:200]}"
    documents = result["documents"][0]
    if not documents:
        return "No passages found."
    parts = []
    for rank, (text, meta, distance) in enumerate(
        zip(documents, result["metadatas"][0], result["distances"][0]), start=1
    ):
        parts.append(
            f"[{rank}] source: {meta['source']} | location: {meta['location']} | distance: {distance:.3f}\n{text}"
        )
    return "\n\n".join(parts)


@mcp.tool()
def add_document(path: str) -> str:
    """Add a document (.pdf, .html, .txt or .md) to the searchable corpus and return a summary.

    Give the path of a file on this computer, relative to the project folder or absolute. The
    file is read, cleaned, split into passages with their location, embedded and stored, so that
    later searches can find it. The document's source name is its file name without extension.

    If the document is already indexed unchanged, nothing is added ("already indexed"). If a
    document with the same file name is already indexed but its content differs, the old passages
    of that name are replaced by the new ones. This tool changes the stored corpus and uses
    embedding quota (about one embedding per passage), so only call it when the user wants the
    document added. Returns how many passages were added, kept or replaced, or the reason it failed.
    """
    file = Path(path).expanduser()
    if not file.is_absolute():
        file = ROOT / file
    if not file.is_file():
        return f"Not added: no file at {path}."
    if file.suffix.lower() not in (".pdf", ".html", ".htm", ".txt", ".md"):
        return f"Not added: unsupported file type {file.suffix!r}. Use .pdf, .html, .txt or .md."
    if file.stat().st_size > MAX_FILE_MB * 1_000_000:
        return f"Not added: the file is bigger than {MAX_FILE_MB} MB."
    try:
        with contextlib.redirect_stdout(sys.stderr):
            chunks = index.chunk_file(file, DESIGN)
            if not chunks:
                return "Not added: no text could be extracted (is it a scanned PDF?)."
            source = chunks[0].source
            existing = COLLECTION.get(where={"source": source}, include=[])["ids"]
            keep = {c.id for c in chunks}
            stale = [i for i in existing if i not in keep]
            if stale:
                COLLECTION.delete(ids=stale)
            stats = index.embed_and_store(chunks, DESIGN)
    except index.DailyQuotaReached as error:
        return f"Partly added: the embedding quota ran out ({str(error)[:120]}). Run add_document again later to finish."
    if stats["added"] == 0 and not stale:
        return f"Already indexed: '{source}' has {stats['total']} passages and nothing changed."
    note = f" Replaced {len(stale)} outdated passage(s) of the same name." if stale else ""
    return (
        f"Added '{source}': {stats['added']} new passage(s), {stats['already_indexed']} already present, "
        f"{stats['total']} in total.{note}"
        + (" The embedding quota ran out before it finished; run again later." if stats["stopped_by_quota"] else "")
    )


if __name__ == "__main__":
    mcp.run()  # stdio