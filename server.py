"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns the most relevant passages with citations.
- add_document(path): runs a file through index.py's pipeline, embeds its new chunks
  and stores them.

The committed index/ is loaded as is; the corpus is never re-embedded here. Nothing is
printed to stdout (it carries the MCP protocol); logs go to stderr. The docstrings below
are the tool descriptions the model reads.
"""

import logging
import warnings
from pathlib import Path

from mcp.server.mcpserver import MCPServer

warnings.filterwarnings("ignore")
logging.getLogger("pdfminer").setLevel(logging.ERROR)
logging.getLogger("chromadb").setLevel(logging.ERROR)

import index  # noqa: E402  (the index pipeline: chunk_file, embed_and_store)
import rag  # noqa: E402

mcp = MCPServer("corpus", log_level="WARNING")


@mcp.tool()
def search(query: str) -> str:
    """Search an indexed collection of EU data-protection texts for a small business:
    the GDPR (Regulation 2016/679, articles only), EDPB Guidelines 05/2020 on consent and
    EDPB Guidelines 9/2022 on personal data breach notification (plus any document added
    later with add_document).

    Use it for any question about GDPR obligations: legal bases and consent, cookies and
    newsletters, controllers and processors, data breaches (when and how to notify the
    authority or the people affected), rights of individuals, fines. Write the query as a
    full question or with the key legal terms; search again with other words if the
    passages do not answer the question.

    Returns up to 5 passages, best first. Each starts with its citation in the form
    [source | location], e.g. [GDPR | Art. 33(1)–(4)] or [EDPB 9/2022 | para. 29–31],
    followed by the document, page and section. Cite those labels exactly. If no passage
    answers the question, the corpus does not cover it."""
    query = (query or "").strip()
    if not query:
        return "Empty query. Ask a question about the GDPR, consent or data breaches."
    try:
        return rag.format_results(rag.search(query))
    except rag.QuotaExhausted:
        return "Search is unavailable: the daily Gemini embedding quota is used up. Try again after 09:00 (Spain)."


@mcp.tool()
def add_document(path: str) -> str:
    """Add a document to the searchable collection. Takes the path of a local .pdf, .html,
    .txt or .md file, runs it through the same pipeline as the rest of the index (extract,
    clean, chunk with its locations, embed with Gemini) and stores it, so search can find it.

    If the same file is already indexed it is skipped and nothing is embedded. If a document
    with the same name is indexed but its content changed, it is replaced: only changed
    chunks are embedded and removed passages are deleted.

    Returns the document's source id, its number of chunks and how many were embedded.
    This changes the index for every later search, so only call it when the user asked for it."""
    try:
        file = Path(path).expanduser().resolve()
        if not file.is_file():
            return f"Not added: no file at {file}."
        documents = rag.load_documents()
        doc = index.doc_info(file)
        known = documents.get(doc["source"])
        h = index.file_hash(file)
        if known and known.get("file_hash") == h and rag.ACTIVE_DESIGN in known.get("chunks", {}):
            return (f"Already indexed: {doc['source']} ({known['chunks'][rag.ACTIVE_DESIGN]} chunks), "
                    f"same content, so nothing was embedded.")
        result = index.index_file(file, rag.ACTIVE_DESIGN)
        action = "Replaced" if known else "Added"
        return (f"{action} {result['source']}: {result['chunks']} chunks "
                f"({result['embedded']} embedded now, {result['reused']} unchanged, {result['removed']} removed). "
                f"It is now searchable.")
    except rag.QuotaExhausted:
        return "Not added (or only partly): the daily Gemini embedding quota is used up. Run add_document again after 09:00 (Spain); saved chunks are kept."
    except (ValueError, FileNotFoundError) as error:
        return f"Not added: {error}"


if __name__ == "__main__":
    mcp.run()  # stdio
