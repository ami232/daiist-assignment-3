"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it and stores it.

Loads index/ at startup and never re-embeds the corpus (only new queries and added documents
are embedded, and both are cached). Prints nothing to stdout, which carries the protocol.
"""

import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer

import index
import retrieval

ROOT = Path(__file__).resolve().parent
MAX_NEW_EMBEDDINGS = 200  # one added document may not spend more than this share of the daily quota

mcp = MCPServer("corpus", log_level="WARNING")
_retriever: retrieval.Retriever | None = None


def retriever() -> retrieval.Retriever:
    global _retriever
    if _retriever is None:
        _retriever = retrieval.Retriever(retrieval.CHOSEN["design"])
    return _retriever


@mcp.tool()
def search(query: str) -> str:
    """Search the indexed NIST publications and return the most relevant passages with citations.

    The index covers NIST AI 100-1 (AI Risk Management Framework 1.0), NIST AI 600-1 (Generative AI
    Profile), NIST SP 800-61r3 (Incident Response Recommendations, a CSF 2.0 Community Profile) and
    NIST SP 800-218 (Secure Software Development Framework 1.1), plus any document added later.
    Use it for any question about what these documents say. Search once per part of a multi-part
    question. Identifiers such as GOVERN 1.2, GV-1.6-001, RS.MA-02 or PO.1.1 match best when written
    exactly; also try a plain-language query if an identifier search misses.

    Returns up to 5 passages, best first. Each has a chunk_id, the document and its version, the PDF
    page range, the printed page, the section, the identifiers it contains, a ready-made citation
    such as [NIST.SP.800-218, p14] or [NIST.SP.800-218, PO.1.1], and the passage text.
    """
    r = retriever()
    hits = r.search(query, k=retrieval.CHOSEN["k"], method=retrieval.CHOSEN["method"],
                    use_route=retrieval.CHOSEN["use_route"])
    return retrieval.format_hits(hits)


@mcp.tool()
def add_document(path: str) -> str:
    """Add one PDF to the search index so that later searches can find it.

    `path` is a PDF file path, absolute or relative to the project folder. The file goes through the
    same extract, clean, chunk and embed pipeline as the original corpus (index.py). If a file with
    identical content is already indexed, nothing is embedded and the reply says so. If a different
    version of a document with the same id is indexed, the new version replaces it. Documents that
    would need more than 200 new embeddings are refused to protect the daily embedding quota.

    Returns one line saying what happened: already indexed, added, or replaced, with chunk counts.
    Only call it when the user has asked to add a specific file.
    """
    file = Path(path).expanduser()
    if not file.is_absolute():
        file = (ROOT / file).resolve()
    if not file.is_file():
        return f"Not added: no file at {file}."
    if file.suffix.lower() != ".pdf":
        return f"Not added: {file.name} is not a PDF; the pipeline only reads PDFs."

    design = retrieval.CHOSEN["design"]
    doc_hash = index.sha256_file(file)
    col = index.get_collection(design)
    same = col.get(where={"doc_hash": doc_hash}, include=["metadatas"])
    if same["ids"]:
        doc_id = same["metadatas"][0]["doc_id"]
        return f"Already indexed: {file.name} is {doc_id} ({len(same['ids'])} chunks). Nothing was embedded."

    chunks = index.chunk_file(file, design)
    if not chunks:
        return f"Not added: no text could be extracted from {file.name}."
    new = index.missing(index.doc_sent_texts(chunks))
    if len(new) > MAX_NEW_EMBEDDINGS:
        return (f"Not added: {file.name} would need {len(new)} new embeddings, above the limit of "
                f"{MAX_NEW_EMBEDDINGS} per document.")

    doc_id = chunks[0].meta["doc_id"]
    old = col.get(where={"doc_id": doc_id}, include=[])["ids"]
    print(f"add_document: embedding {len(new)} new texts for {doc_id}", file=sys.stderr, flush=True)
    index.embed_and_store(chunks, design)
    stale = [i for i in old if i not in {c.chunk_id for c in chunks}]
    if stale:
        col.delete(ids=stale)
    retriever().reload()
    verb = "Replaced" if old else "Added"
    return (f"{verb} {doc_id} ({chunks[0].meta['doc_title']}): {len(chunks)} chunks stored, "
            f"{len(new)} new embeddings" + (f", {len(old)} old chunks replaced." if old else "."))


if __name__ == "__main__":
    mcp.run()  # stdio
