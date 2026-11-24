"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): the 5 best chunks, each with its citation [doc_id, location],
  document title, source URL, similarity score and text.
- add_document(path): runs the file through index.py's pipeline (imported, not
  rewritten), embeds its chunks and stores them.

The index in index/ is loaded at startup and the corpus is never re-embedded:
a search embeds one query (cached in index/query_cache.json), add_document
embeds only the chunks of the file it is given.

Environment:
  SEARCH_DESIGN=article|fixed   which collection to search and add to (default article)

Nothing is printed to stdout (it carries the MCP protocol); logs go to stderr.
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer

import index

ROOT = Path(__file__).resolve().parent
TOP_K = 5
ADDABLE = {".html", ".htm", ".xhtml", ".xml", ".pdf", ".txt", ".md"}

SEARCH_DESIGN = os.environ.get("SEARCH_DESIGN", "article").strip().lower() or "article"
if SEARCH_DESIGN not in index.DESIGNS:
    print(f"SEARCH_DESIGN must be one of {index.DESIGNS}, not {SEARCH_DESIGN!r}", file=sys.stderr)
    raise SystemExit(2)

mcp = MCPServer("corpus", log_level="WARNING")

# Loaded once at startup. Opening the collection reads index/; it embeds nothing.
COLLECTION = index.get_collection(SEARCH_DESIGN)
index.log(f"[corpus] design={SEARCH_DESIGN}, {COLLECTION.count()} vectors loaded from {index.INDEX_DIR.name}/")


def retrieve(query: str, k: int = TOP_K, design: str | None = None) -> list[dict]:
    """The k most similar chunks, best first. Plain function, so evaluate.py can call it too.

    Raises index.QuotaExhausted if the query has no cached embedding and the quota is used up.
    """
    collection = COLLECTION if design in (None, SEARCH_DESIGN) else index.get_collection(design)
    stored = collection.count()
    if stored == 0:
        return []
    vector = index.embed_query(query)
    found = collection.query(query_embeddings=[vector], n_results=min(k, stored), include=["documents", "metadatas", "distances"])
    hits = []
    for text, meta, distance in zip(found["documents"][0], found["metadatas"][0], found["distances"][0]):
        hits.append({
            "doc_id": meta["doc_id"],
            "location": meta["location"],
            "doc_title": meta["doc_title"],
            "source_url": meta.get("source_url", ""),
            "score": round(1 - distance, 4),  # cosine similarity
            "text": text,
            "chunk_id": meta["chunk_id"],
            "sections": meta.get("sections", ""),
        })
    return hits


def format_hits(query: str, hits: list[dict], stored: int) -> str:
    """The text the model reads. agent.py parses the same layout, so change both together."""
    lines = [
        f"Search results for: {query}",
        f'Index: "{SEARCH_DESIGN}" chunks; {len(hits)} of {stored} stored passages shown, best match first.',
        "To cite a passage, copy its Citation line exactly: [doc_id, location].",
    ]
    for rank, hit in enumerate(hits, 1):
        lines += [
            "",
            f"=== Result {rank} of {len(hits)} ===",
            f"Citation: [{hit['doc_id']}, {hit['location']}]",
            f"Document: {hit['doc_title']}",
            f"Source: {hit['source_url']}",
            f"Similarity: {hit['score']:.4f}",
            "Text:",
            hit["text"],
        ]
    return "\n".join(lines)


@mcp.tool()
def search(query: str) -> str:
    """Search four EU railway acts and return the 5 most relevant passages with their citations.

    The corpus is the English text, as originally published in the Official
    Journal (later amendments are NOT included), of:
      - Dir_2016_797: Directive (EU) 2016/797, interoperability of the rail system
      - Dir_2016_798: Directive (EU) 2016/798, railway safety
      - Reg_1299_2014: Regulation (EU) No 1299/2014, TSI for the infrastructure subsystem (TSI INF)
      - Reg_2019_779: Implementing Regulation (EU) 2019/779, certification of entities in charge of maintenance (ECM)
    plus any document added later with add_document.

    Use it for every question about EU railway safety, interoperability, track
    and infrastructure parameters (gauge, cant, gradients, platforms, tunnels...),
    safety certificates and authorisations, national safety authorities, or
    maintenance and ECM duties. Ask in plain English with the terms the acts
    use; search again with other words if the passages do not answer the question.

    Returns up to 5 passages, best match first. Each has a line
    "Citation: [doc_id, location]" (for example [Dir_2016_798, Article 14(3)]),
    the document title, the source URL, a cosine similarity between 0 and 1,
    and the passage text. Cite with the Citation line copied exactly. A passage
    being returned does not mean it answers the question: read the text.
    """
    query = (query or "").strip()
    if not query:
        return "SEARCH FAILED: the query is empty. Pass the question, or its key terms, as `query`."
    stored = COLLECTION.count()
    if stored == 0:
        return "SEARCH FAILED: the index is empty. Build it with `uv run python main.py index`. No passages were retrieved."
    try:
        hits = retrieve(query)
    except index.QuotaExhausted as error:
        index.log(f"[corpus] search stopped by the embedding quota: {error}")
        return (
            "SEARCH FAILED: the Gemini embedding quota is used up, so this query could not be embedded "
            "(queries already asked are cached and still work). No passages were retrieved: do not answer "
            "from memory. The free quota resets at midnight Pacific time (09:00 in Spain)."
        )
    index.log(f"[corpus] search {query!r}: top {hits[0]['score']:.3f} [{hits[0]['doc_id']}, {hits[0]['location']}]")
    return format_hits(query, hits, stored)


@mcp.tool()
def add_document(path: str) -> str:
    """Add ONE new document file to the search index. It changes the index and spends embedding quota.

    Call it only when the user explicitly asks to add a document. `path` is a
    file on this machine (.html, .xhtml, .pdf, .txt or .md), absolute or
    relative to the project folder. The file goes through the same pipeline as
    the corpus: text extraction and cleaning, chunking, embedding, storage.

    If the document is already indexed:
      - same file contents (same hash): nothing is embedded, it reports "already indexed";
      - same document name but different contents: the old version's passages are
        deleted and the new version is indexed in their place.

    Returns the doc_id to use in citations, and how many passages were added
    (embedded now), skipped (already stored) and replaced (old ones deleted).
    If the embedding quota runs out it says how many passages are still
    missing; calling it again with the same path later continues from there.
    """
    file = Path((path or "").strip()).expanduser()
    if not file.is_absolute():
        file = ROOT / file
    if not file.is_file():
        return f"NOT ADDED: there is no file at {file}. Nothing was changed."
    if file.suffix.lower() not in ADDABLE:
        return f"NOT ADDED: {file.name} is not a supported type ({', '.join(sorted(ADDABLE))}). Nothing was changed."

    chunks = index.chunk_file(file, SEARCH_DESIGN)  # index.py's pipeline: extract, clean, chunk
    if not chunks:
        return f"NOT ADDED: no text could be extracted from {file.name}. Nothing was changed."
    doc_id, doc_hash = chunks[0]["metadata"]["doc_id"], chunks[0]["metadata"]["doc_hash"]
    new_ids = {chunk["id"] for chunk in chunks}

    existing = COLLECTION.get(where={"doc_id": doc_id}, include=["metadatas"])
    old_ids = set(existing["ids"])
    old_hashes = {meta.get("doc_hash", "") for meta in existing["metadatas"]}
    header = f"doc_id: {doc_id}\ndesign: {SEARCH_DESIGN}\ndoc_hash (sha256): {doc_hash}"

    if old_hashes == {doc_hash} and new_ids <= old_ids:
        index.log(f"[corpus] add_document {file.name}: already indexed ({len(old_ids)} chunks)")
        return (
            f"already indexed, nothing embedded\n{header}\n"
            f"chunks added: 0\nchunks skipped (already stored): {len(chunks)}\nchunks replaced: 0"
        )

    # A different version of this doc_id is stored: delete its old chunks, then index the new ones.
    # Chunk ids are hashes of the chunk text, so an old chunk whose text is unchanged in the new
    # version has the same id: it is kept (its metadata is updated) instead of being embedded again.
    replaced = sorted(old_ids - new_ids)
    if replaced:
        COLLECTION.delete(ids=replaced)
    stats = index.embed_and_store(chunks, COLLECTION)

    if not old_ids:
        status = "added"
    elif old_hashes == {doc_hash}:
        status = "continued (the same file was partly indexed before)"
    else:
        status = "replaced (a different version of this document was indexed before)"
    lines = [
        status,
        header,
        f"chunks added (embedded now): {stats['stored']}",
        f"chunks skipped (already stored, same text): {stats['already']}",
        f"chunks replaced (old version deleted): {len(replaced)}",
    ]
    if stats["quota_hit"]:
        lines.insert(0, "INCOMPLETE: the Gemini embedding quota ran out before every passage was embedded.")
        lines.append(
            f"chunks still missing: {stats['remaining']} of {len(chunks)}. The passages stored so far are searchable. "
            "Call add_document again with the same path after the quota resets (midnight Pacific time, "
            "09:00 in Spain); it embeds only what is missing."
        )
    index.log(f"[corpus] add_document {file.name}: {status}; +{stats['stored']} ={stats['already']} -{len(replaced)} missing {stats['remaining']}")
    return "\n".join(lines)


if __name__ == "__main__":
    mcp.run()  # stdio
