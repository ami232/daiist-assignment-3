"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): the 5 most relevant passages of the corpus, each with its citation.
- add_document(path): runs one file through index.py's pipeline, embeds it and stores it.

The index is loaded once at startup from index/ (the corpus is never re-embedded);
only a question or a newly added document costs embeddings. Nothing is printed to
stdout, which carries the protocol: logs go to stderr.
"""

import sys
import threading
from pathlib import Path

from mcp.server.mcpserver import MCPServer

import index as ix
from retrieval import Retriever

DESIGN = "B"  # one chunk per article: the design chosen in Step 5
TOP_K = 5     # the right passage is among the top 5 for 97% of the test questions, but first only for 50%

mcp = MCPServer("corpus", log_level="WARNING")

_lock = threading.Lock()
_retriever: Retriever | None = None
_client = None
_query_vectors: dict[str, object] = {}  # a repeated query costs no embedding


def log(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


def get_retriever() -> Retriever:
    global _retriever
    if _retriever is None:
        _retriever = Retriever(DESIGN)
        log(f"corpus server: {len(_retriever.chunks)} chunks loaded (design {DESIGN})")
    return _retriever


def query_vector(query: str):
    global _client
    if query not in _query_vectors:
        _client = _client or ix.make_client()
        _query_vectors[query] = ix.embed_query(query, _client)
    return _query_vectors[query]


def citation(chunk: dict) -> str:
    pages = chunk["pages"]
    return (f"{chunk['source_title']} | {chunk['location']} | "
            f"{'pp.' if '-' in pages else 'p.'} {pages} | id {chunk['chunk_id']}")


@mcp.tool()
def search(query: str) -> str:
    """Search the legal corpus and return the 5 most relevant passages, each with its citation.

    The corpus is in Spanish and holds: the XXIII Convenio colectivo estatal de industrias
    extractivas, vidrio, cerámicas y comercio exclusivista (2025-2027: pay tables for 2025 and
    2026, working hours, vacations, leave, notice, disciplinary rules, workers' representation,
    health and safety); Real Decreto 126/2026 (salario mínimo interprofesional 2026); 24 key
    articles of the Estatuto de los Trabajadores (hours, vacations, leave, pay, contract
    termination and dismissal); and any document added with add_document. It does not hold
    other collective agreements, case law or Social Security rules.

    Use it for every question about these rules; do not answer from memory. Write the query
    in Spanish, as a short question or key words. The passages are ordered from most to least
    similar but may not contain the answer: read them, and say so if the answer is not there.
    If they do not help, search again with different words.

    Returns numbered passages. Each starts with its citation (document | article or section |
    pages | id) followed by the passage text.
    """
    query = (query or "").strip()
    if not query:
        return "Search failed: the query is empty."
    try:
        with _lock:
            retriever = get_retriever()
            results = retriever.search(query, query_vector(query), "vector", TOP_K)
    except Exception as error:  # noqa: BLE001 - the model should read what went wrong
        log(f"search failed: {type(error).__name__}: {error}")
        return f"Search failed: {error}"
    parts = [f"{len(results)} passages for: {query!r}, most similar first.\n"]
    for rank, item in enumerate(results, 1):
        chunk = item["chunk"]
        parts.append(f"[{rank}] {citation(chunk)}\n{chunk['text'].split(chr(10), 1)[1]}\n")
    return "\n".join(parts)


@mcp.tool()
def add_document(path: str) -> str:
    """Add one document to the corpus so that search can find it. This changes the index.

    Takes the path of a PDF, .txt or .md file on this computer (a relative path starts in the
    project folder). The text is cleaned, split into one passage per article or section,
    embedded and stored; it can be searched straight away. The file's name becomes its
    source name in citations.

    A document that is already indexed is not added twice: the same content (whatever the file
    is called) is skipped; a file with the same name but different content replaces the old
    version. Adding uses embedding quota (about one per passage) and a document is limited to
    300 passages. Returns what happened: added, skipped, replaced, incomplete or refused,
    with the number of passages.
    """
    target = Path(path).expanduser()
    if not target.is_absolute():
        target = ix.ROOT / target
    global _client, _retriever
    try:
        with _lock:
            _client = _client or ix.make_client()
            result = ix.add_document_to_index(target, _client)
            if result["status"] in ("added", "replaced", "incomplete"):
                _retriever = None  # reload the index on the next search
    except Exception as error:  # noqa: BLE001
        log(f"add_document failed: {type(error).__name__}: {error}")
        return f"Not added: {type(error).__name__}: {error}"
    status = result["status"]
    if status in ("added", "replaced"):
        verb = "Replaced the earlier version of" if status == "replaced" else "Added"
        return (f"{verb} '{result['title']}' (source name: {result['source']}): "
                f"{result['chunks']} passages, {result['words']} words. It can be searched now.")
    if status == "already_indexed":
        return (f"Skipped: '{result['title']}' is already indexed ({result['note']}). "
                f"Nothing was changed.")
    if status == "incomplete":
        return (f"Only part of '{result['source']}' was embedded ({result['embedded']} of "
                f"{result['chunks']} passages): {result['reason']} Call add_document again with the "
                f"same file to finish; finished passages are kept. It is not searchable yet.")
    return f"Not added: {result['reason']}."


if __name__ == "__main__":
    get_retriever()  # fail now, not on the first question, if index/ is missing or empty
    mcp.run()  # stdio
