"""
Assignment 3: MCP server `corpus`. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): the best chunks of the EUDR corpus, each with its citation.
- add_document(path): runs a file through index.py's pipeline, embeds it and stores it.

Loads index/ at startup and never re-embeds the corpus. Prints nothing to stdout (it carries the
MCP protocol); logs go to stderr.
"""

import hashlib
import json
import sys
import time
from pathlib import Path

from mcp.server.mcpserver import MCPServer

import index
import retrieval

REGISTRY = index.INDEX_DIR / "added_documents.json"
TOP_K = 5
SUPPORTED = {".html", ".htm", ".xhtml", ".xml", ".pdf", ".txt", ".md"}

mcp = MCPServer("corpus", log_level="WARNING")


def log(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


def cite_key(chunk: dict) -> str:
    """How the answer must cite a chunk, e.g. [EUDR Article 25(1)–(2)] or [FAQ 10.2, p. 94]."""
    location = chunk["location"]
    return location if location.startswith(chunk["source"]) else f"{chunk['source']} {location}"


def format_results(results: list[dict], note: str = "") -> str:
    if not results:
        return "No passages found in the corpus for this query."
    blocks = [note] if note else []
    for n, chunk in enumerate(results, start=1):
        title = f" | {chunk['unit_title']}" if chunk.get("unit_title") else ""
        blocks.append(f"[{n}] Cite as: [{cite_key(chunk)}]\nDocument: {chunk['doc_title']}{title}\n"
                      f"Similarity: {chunk.get('similarity', '')}\n{chunk['text']}")
    return "\n\n---\n\n".join(blocks)


@mcp.tool()
def search(query: str) -> str:
    """Search the EU Deforestation Regulation (EUDR) corpus: the consolidated Regulation (EU) 2023/1115
    (articles and annexes, as amended up to 18 September 2026), the Commission's 2026 Guidance document
    and the Commission's FAQ (version 5, April 2026), plus any document added with add_document.

    Use it for any question about EUDR obligations of operators, traders and importers (for example
    cocoa importers): scope and product codes, due diligence, geolocation, due diligence statements,
    dates of application, checks and penalties. Search again with other words if the passages do not
    answer the question.

    Returns the 5 most relevant passages, each starting with "Cite as: [...]", the citation to put
    after every claim taken from it, followed by the document title and the passage text.
    """
    note = ""
    try:
        results = retrieval.search(query, index.DEFAULT_DESIGN, k=TOP_K, hybrid=index.DEFAULT_HYBRID)
    except index.DailyQuotaExhausted:
        # Without a query embedding, keyword search still works; say so, the ranking is weaker.
        log("search: daily embedding quota reached, falling back to keyword search")
        all_chunks = retrieval.chunks(index.DEFAULT_DESIGN)
        results = [all_chunks[cid] for cid in retrieval.bm25_rank(query, index.DEFAULT_DESIGN)[:TOP_K]]
        note = "(Keyword search only: the embedding quota is used up for today.)"
    return format_results(results, note)


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_registry() -> dict:
    try:
        return json.loads(REGISTRY.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


@mcp.tool()
def add_document(path: str) -> str:
    """Add a document to the EUDR corpus so that search can find it: an HTML (e.g. EUR-Lex), PDF,
    Markdown or text file on this computer, given by its file path.

    The file is cleaned, cut into passages with their location, embedded and stored in the index.
    If the same content is already indexed, nothing is embedded again. If a file with the same name
    but different content was added before, its old passages are replaced by the new version.

    Returns how many passages were added and how they are cited, or why the file was not added.
    """
    file = Path(path).expanduser()
    if not file.is_absolute():
        file = (index.ROOT / file).resolve()
    if not file.is_file():
        return f"Not added: there is no file at {file}."
    if file.suffix.lower() not in SUPPORTED:
        return f"Not added: {file.suffix} files are not supported (use {', '.join(sorted(SUPPORTED))})."

    digest = file_hash(file)
    for doc in index.CORPUS:  # the original corpus is already indexed
        corpus_file = index.CORPUS_DIR / doc["file"]
        if corpus_file.exists() and file_hash(corpus_file) == digest:
            return f"Already indexed: {file.name} is the corpus document '{doc['title']}'. Nothing was embedded."
    registry = load_registry()
    previous = registry.get(file.name)
    if previous and previous["sha256"] == digest:
        return (f"Already indexed: {file.name} was added on {previous['added']} with {len(previous['ids'])} "
                f"passages. Nothing was embedded.")

    design = index.DEFAULT_DESIGN
    chunks = index.chunk_file(file, design)
    if not chunks:
        return f"Not added: no text could be extracted from {file.name}."
    store = index.collection(design)
    if previous:  # new version of a file added before: drop the old passages first
        store.delete(ids=previous["ids"])
    try:
        index.embed_and_store(chunks, design)
    except index.DailyQuotaExhausted:
        return "Not added: the daily embedding quota is used up. Try again after the reset (09:00 in Spain)."

    added_path = index.INDEX_DIR / f"added_{design}.jsonl"
    kept = []
    if added_path.exists():
        old_ids = set(previous["ids"]) if previous else set()
        kept = [line for line in added_path.read_text(encoding="utf-8").splitlines()
                if json.loads(line)["id"] not in old_ids]
    added_path.write_text("\n".join(kept + [json.dumps(c, ensure_ascii=False) for c in chunks]) + "\n", encoding="utf-8")
    registry[file.name] = {"sha256": digest, "ids": [c["id"] for c in chunks], "design": design,
                           "added": time.strftime("%Y-%m-%d %H:%M")}
    REGISTRY.write_text(json.dumps(registry, indent=2), encoding="utf-8")
    retrieval.chunks.cache_clear()
    retrieval.bm25_index.cache_clear()

    verb = "Replaced the previous version of" if previous else "Added"
    examples = ", ".join(f"[{cite_key(c)}]" for c in chunks[:3])
    return f"{verb} {file.name}: {len(chunks)} passages indexed, cited for example as {examples}."


if __name__ == "__main__":
    mcp.run()  # stdio
