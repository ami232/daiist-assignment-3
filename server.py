import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer

import index

mcp = MCPServer("corpus", log_level="WARNING")
collection = index.get_collection()
DEFAULT_K = 5
MAX_K = 10


def format_location(meta: dict) -> str:
    """'FDA Food Code 2026 | Chapter 3. Food | 3-501.14 Cooling | PDF page 98 (printed page 70)'."""
    pages = (f"PDF page {meta['page_start']}" if meta["page_start"] == meta["page_end"]
             else f"PDF pages {meta['page_start']}-{meta['page_end']}")
    if meta.get("page_label"):
        pages += f" (printed page {meta['page_label']})"
    parts = [meta["title"], meta.get("part", ""), meta.get("section", ""), pages]
    return " | ".join(dict.fromkeys(p for p in parts if p))


@mcp.tool()
def search(query: str, k: int = DEFAULT_K) -> str:
    """Search the FDA Food Code 2026 and FDA HACCP manuals for food-safety rules; phrase the query like the rule (e.g. "cooling cooked food time and temperature limits"). Returns up to k passages (default 5, max 10), each with a citation line to cite."""
    k = max(1, min(int(k), MAX_K))
    hits = index.ranked_search(collection, index.embed_query(query), k)
    blocks = []
    for n, hit in enumerate(hits, start=1):
        text = hit["text"]
        body = text.split("\n", 1)[1] if text.startswith("[") and "\n" in text else text
        blocks.append(f"[{n}] {format_location(hit['meta'])} (score {hit['score']:.2f})\n{body}")
    return "\n\n".join(blocks) if blocks else "No passages found: the index is empty."


@mcp.tool()
def add_document(path: str) -> str:
    """Add a PDF (path absolute or relative to the project) to the searchable corpus. Returns the document id, title and number of chunks stored."""
    file = Path(path).expanduser()
    if not file.is_absolute():
        file = index.ROOT / file
    if not file.is_file():
        return f"Not added: no file at {file}."
    if file.suffix.lower() != ".pdf":
        return f"Not added: {file.name} is not a PDF. Only PDF files can be indexed."

    sha = index.file_sha256(file)
    documents = index.load_documents()
    for doc_id, info in documents.items():
        if info["sha256"] == sha:
            return (f"Already indexed: {file.name} is the same file as '{info['title']}' "
                    f"(id {doc_id}, {info['chunks']} chunks). Nothing was changed.")

    doc_id = index.doc_id_for(file)
    title = index.pdf_title(file)
    replaced = 0
    if doc_id in documents:  # a new version of a document already indexed
        old = collection.get(where={"doc_id": doc_id}, include=[])["ids"]
        if old:
            collection.delete(ids=old)
        replaced = len(old)

    chunks = index.chunk_file(file, doc_id, title)
    if not chunks:
        return f"Not added: no text could be extracted from {file.name} (is it a scanned PDF?)."
    try:
        embedded = index.embed_and_store(chunks, collection)
    except index.DailyQuotaExhausted:
        stored = len(collection.get(where={"doc_id": doc_id}, include=[])["ids"])
        return (f"Partly added: the daily Gemini embedding quota ran out after {stored} of "
                f"{len(chunks)} chunks of '{title}'. Those are searchable now; call "
                f"add_document again after the quota resets to embed the rest.")
    index.register_document(doc_id, title, file, len(chunks))
    pages = max(c["page_end"] for c in chunks)
    note = f" It replaced {replaced} chunks of the previous version." if replaced else ""
    print(f"add_document: {file.name} -> {doc_id}, {len(chunks)} chunks", file=sys.stderr)
    return (f"Added '{title}' (id {doc_id}): {pages} pages, {len(chunks)} chunks, "
            f"{embedded} newly embedded.{note} It is now searchable.")


if __name__ == "__main__":
    mcp.run()  # stdio
