"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Load index/ at startup; never re-embed the corpus. Print nothing to stdout
(it carries the protocol); log to stderr. Docstrings become the tool
descriptions the model reads.
"""

from functools import lru_cache
from pathlib import Path

from mcp.server.mcpserver import MCPServer

import index

ROOT = Path(__file__).resolve().parent
TOP_K = 5              # chosen from the retrieval evaluation (eval/retrieval_summary.json): dense search, k=5
MAX_NEW_CHUNKS = 300   # one embedding request per chunk: refuse documents that would eat the daily quota
MAX_FILE_MB = 30

mcp = MCPServer("corpus", log_level="WARNING")


@lru_cache(maxsize=1)
def _client():
    return index.gemini_client()


def _collection():
    return index.get_collection(index.DEFAULT_DESIGN)


def _format_hit(rank: int, text: str, meta: dict, distance: float) -> str:
    # Gemini vectors have unit length, so squared L2 distance d maps to cosine similarity 1 - d/2.
    similarity = 1 - distance / 2
    page = f", page {meta['page']}" if meta.get("page") else ""
    heading = f"\nHeading: {meta['heading']}" if meta.get("heading") else ""
    return (
        f"[{rank}] Source: {meta['source']} ({meta['title']}) | Location: {meta['location']}{page} "
        f"| similarity {similarity:.2f}{heading}\n{text}"
    )


@mcp.tool()
def search(query: str) -> str:
    """Search the corpus for passages that answer a question. The corpus is the text of the EU GDPR
    (Regulation 2016/679: its 173 recitals and 99 articles) and two EDPB guidelines: Guidelines 05/2020 on
    consent, and Guidelines 9/2022 on personal data breach notification. Use it for any question about
    GDPR obligations of a small business: lawful bases, consent, notifying a breach, data subject rights,
    DPOs, records, fines.

    Takes a natural-language query. Returns the 5 closest passages, best first. Each one starts with its
    source (gdpr, edpb_consent or edpb_breach), its location (an article, a recital, or a guideline section
    and paragraph numbers) and a similarity score, followed by the passage text. Cite the source and
    location for every claim you take from a passage.

    The passages are the nearest ones, not guaranteed to answer the question: read them, and if none of
    them does, say that the corpus does not cover it instead of answering from memory. For a question that
    needs several rules (for example an article and the guideline that explains it), search once per
    sub-question with different wording."""
    query = query.strip()
    if not query:
        return "The query is empty. Give a question or topic to search for."
    collection = _collection()
    total = collection.count()
    if total == 0:
        return "The index is empty. Run `uv run python main.py index` first."
    vector = index.embed_query(query, _client())
    found = collection.query(
        query_embeddings=[vector],
        n_results=min(TOP_K, total),
        include=["documents", "metadatas", "distances"],
    )
    hits = zip(found["documents"][0], found["metadatas"][0], found["distances"][0])
    body = "\n\n".join(_format_hit(i, text, meta, dist) for i, (text, meta, dist) in enumerate(hits, 1))
    return f"{min(TOP_K, total)} closest passages for: {query}\n\n{body}"


@mcp.tool()
def add_document(path: str) -> str:
    """Add one PDF document to the searchable corpus, so that `search` can find it from then on. Takes
    the path of a PDF file on this computer (absolute, or relative to the project folder). The file goes
    through the same pipeline as the original corpus: text extraction, cleaning, chunking with citation
    labels, embedding, storage in the index.

    If exactly the same file is already indexed, nothing happens. If a file with the same name but
    different content is indexed, its old passages are replaced. Returns a one-line report: the document
    name, whether it was added, skipped or replaced, and how many passages it produced. This changes the
    shared index and uses embedding quota (one request per passage, so it can take a few minutes): call
    it only when the user asks to add a specific document. Refuses non-PDF files and documents of more
    than 300 passages."""
    file = Path(path).expanduser()
    if not file.is_absolute():
        file = ROOT / file
    if not file.is_file():
        return f"File not found: {file}"
    if file.suffix.lower() != ".pdf":
        return f"Only PDF files can be indexed, got {file.suffix or 'a file with no extension'}."
    if file.stat().st_size > MAX_FILE_MB * 1_000_000:
        return f"{file.name} is larger than {MAX_FILE_MB} MB; not indexed."
    chunks = len(index.chunk_file(file, index.DEFAULT_DESIGN))
    if chunks > MAX_NEW_CHUNKS:
        return f"{file.name} would produce {chunks} passages; the limit is {MAX_NEW_CHUNKS}. Not indexed."
    return index.index_file(file, index.DEFAULT_DESIGN, _client())


if __name__ == "__main__":
    index.log(f"corpus server: {_collection().count()} passages in the index ({index.DEFAULT_DESIGN})")
    mcp.run()  # stdio
