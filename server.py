"""
Assignment 3: MCP server `corpus`. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): the top chunks for a question, each with its citation.
- add_document(path): runs one file through index.py's pipeline (imported,
  not rewritten), embeds its chunks and stores them in index/.

It loads the committed index at startup and never re-embeds the corpus: the
only embeddings it requests are for new questions (cached in
index/query_cache.json) and for documents added through add_document.
Nothing is printed to stdout, which carries the MCP protocol.
"""

from pathlib import Path

from mcp.server.mcpserver import MCPServer

from index import add_file
from rag import Searcher, chosen_config, format_results, log

CONFIG = chosen_config()
ALLOWED_SUFFIXES = {".html", ".htm", ".xhtml", ".pdf", ".txt", ".md"}
MAX_FILE_MB = 20

mcp = MCPServer("corpus", log_level="WARNING")
_searcher: Searcher | None = None


def searcher() -> Searcher:
    global _searcher
    if _searcher is None:
        _searcher = Searcher(CONFIG["design"])
        log(f"corpus server: loaded {len(_searcher.ids)} chunks ({CONFIG['design']}, {CONFIG['mode']} search)")
    return _searcher


@mcp.tool()
def search(query: str, document: str = "") -> str:
    """Search the EU data-protection corpus: the GDPR (Regulation (EU) 2016/679, recitals and
    articles), the ePrivacy Directive 2002/58/EC (consolidated 2009, cookies, direct marketing,
    traffic and location data) and the Commission's standard contractual clauses for transfers
    to third countries (Decision (EU) 2021/914), plus any document added later.

    Use it for any question about what these legal texts say. Ask in plain words; quote legal
    terms when you know them. Call it again with different words if the first results do not
    contain the answer. Optional `document` limits results to one document id: "GDPR",
    "ePrivacy" or "SCC 2021/914".

    Returns the 5 most relevant passages, each with a line `CITE AS: [document, location]`.
    Copy that citation exactly after every claim that relies on the passage.
    """
    results = searcher().search(query, k=CONFIG.get("k", 5), mode=CONFIG["mode"], doc_filter=document or None)
    return format_results(results)


@mcp.tool()
def add_document(path: str) -> str:
    """Add one document to the corpus index: a local file path to an .html/.xhtml, .pdf or .txt
    file. The file is extracted, cleaned, chunked with the same pipeline as the corpus, embedded
    with Gemini and stored, and becomes searchable at once.

    If the same file content is already indexed nothing is re-embedded; if a document with the
    same name but different content is indexed, its old chunks are replaced. Returns what was
    done and how to cite the new document. Only use it when the user asks to add a document.
    """
    file = Path(path).expanduser()
    if file.suffix.lower() not in ALLOWED_SUFFIXES:
        return f"Not added: {file.suffix or 'no extension'} files are not supported ({', '.join(sorted(ALLOWED_SUFFIXES))})."
    if file.is_file() and file.stat().st_size > MAX_FILE_MB * 1e6:
        return f"Not added: the file is larger than {MAX_FILE_MB} MB."
    message = add_file(file, CONFIG["design"])
    searcher().reload()
    return message


if __name__ == "__main__":
    mcp.run()  # stdio
