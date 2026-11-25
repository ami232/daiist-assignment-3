"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Loads index/ at startup (INDEX_DIR overrides the folder); never re-embeds the
corpus. Prints nothing to stdout (it carries the protocol); logs to stderr.
"""

import logging
import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer

import index as index_stage
import rag

logging.basicConfig(stream=sys.stderr, level=logging.WARNING)
log = logging.getLogger("corpus")

ROOT = Path(__file__).resolve().parent
ALLOWED_SUFFIXES = (".pdf", ".html", ".htm", ".txt", ".md")

# Loaded once at startup: the chosen design, search mode and k, and its collection.
CONFIG = rag.load_config()
COLLECTION = rag.load_collection(CONFIG["design"])
print(
    f"corpus server: index {index_stage.index_dir()}, design {CONFIG['design']}, mode {CONFIG['mode']}, "
    f"k {CONFIG['k']}, {COLLECTION.count()} chunks",
    file=sys.stderr, flush=True,
)

mcp = MCPServer("corpus", log_level="WARNING")


@mcp.tool()
def search(query: str) -> str:
    """Search a corpus of EU public procurement law and return the best-matching passages.

    The corpus holds four English texts from EUR-Lex:
    - dir_2014_24: Directive 2014/24/EU on public procurement (articles and annexes):
      thresholds, procedures, time limits, exclusion grounds, selection and award
      criteria, the ESPD, lots, subcontracting, contract modification.
    - reg_2016_7: Implementing Regulation (EU) 2016/7, the ESPD standard form and its instructions.
    - dir_89_665: Remedies Directive 89/665/EEC (consolidated 2014): review procedures,
      standstill period, ineffectiveness, time limits for review.
    - reg_2025_2152: Delegated Regulation (EU) 2025/2152, threshold amounts applying from 1 January 2026.
    Note: Article 4 of dir_2014_24 is the original 2014 text and shows the 2014 amounts;
    reg_2025_2152 gives the amounts that replace them from 2026.

    It does NOT cover: national rules (for example Spain's LCSP) or below-threshold
    contracts, concessions (Directive 2014/23/EU), utilities (Directive 2014/25/EU),
    defence procurement, e-invoicing, case law or guidance.

    Use it for every question about EU public tenders before answering; search again
    with other words if the first results do not contain the answer. The query should
    be a short description of the rule you need, in English.

    Returns the top passages, best first. Each has a citation tag [doc_id | location]
    (for example [dir_2014_24 | Article 27]), a chunk_id, the document title, the
    heading, a relevance score and the text. Answers must cite these tags exactly and
    must only state what the returned text says.
    """
    query = (query or "").strip()
    if not query:
        return "Empty query. Give a short description of the rule you are looking for."
    hits = rag.search(query, design=CONFIG["design"], k=CONFIG["k"], mode=CONFIG["mode"])
    return rag.format_results(hits)


def _resolve_inside_repo(path: str) -> Path:
    candidate = Path(path).expanduser()
    if not candidate.is_absolute():
        candidate = ROOT / candidate
    candidate = candidate.resolve()
    if not candidate.is_relative_to(ROOT):
        raise ValueError(f"Refused: {path} is outside this repository.")
    if not candidate.is_file():
        raise ValueError(f"Refused: {path} does not exist or is not a file.")
    if candidate.suffix.lower() not in ALLOWED_SUFFIXES:
        raise ValueError(f"Refused: {candidate.suffix or 'no extension'} is not supported. Use {', '.join(ALLOWED_SUFFIXES)}.")
    return candidate


@mcp.tool()
def add_document(path: str) -> str:
    """Add one document file to the search index. It changes the index, so call it
    only when the user explicitly asks to add a file.

    `path` must be an existing .pdf, .html, .htm, .txt or .md file inside this
    repository (for example docs_to_add/reg_2025_2151.html). The file goes through
    the same pipeline as the corpus: text extraction, chunking with source and
    location, Gemini embeddings, storage in the collection the search tool uses.
    The doc_id is the file name without extension.

    If the same file (same SHA-256 hash) is already indexed, nothing changes and it
    returns "already indexed, nothing changed". If a file with the same doc_id but
    different content is indexed, its old chunks are deleted and the new version is
    indexed instead. Returns the doc_id and the number of chunks added. Each chunk
    costs one embedding from the daily quota.
    """
    try:
        file = _resolve_inside_repo(path)
    except ValueError as error:
        return str(error)

    design = CONFIG["design"]
    doc_id = index_stage.doc_id_for(file)
    sha = index_stage.file_sha256(file)

    same_file = COLLECTION.get(where={"file_sha256": sha}, include=["metadatas"])
    if same_file["ids"]:
        known_as = same_file["metadatas"][0].get("doc_id", doc_id)
        return f"already indexed, nothing changed (doc_id {known_as}, {len(same_file['ids'])} chunks)."

    try:
        chunks = index_stage.chunk_file(file, design)
    except Exception as error:  # noqa: BLE001 - report a bad file to the caller
        log.warning("add_document failed to read %s: %s", file, error)
        return f"Could not read {file.name}: {type(error).__name__}: {error}"
    if not chunks:
        return f"No text could be extracted from {file.name}; nothing was added."

    old = COLLECTION.get(where={"doc_id": doc_id}, include=[])["ids"]
    if old:
        COLLECTION.delete(ids=old)

    result = index_stage.embed_and_store(chunks, design, COLLECTION)
    replaced = f" Replaced the previous version ({len(old)} chunks deleted)." if old else ""
    if result["quota"]:
        return (
            f"doc_id {doc_id}: added {result['added']} of {len(chunks)} chunks, then the embedding quota ran out."
            f"{replaced} Call add_document again after 09:00 Madrid to add the remaining {result['left']}."
        )
    return f"doc_id {doc_id}: added {result['added']} chunks to the '{design}' collection.{replaced}"


if __name__ == "__main__":
    mcp.run()  # stdio
