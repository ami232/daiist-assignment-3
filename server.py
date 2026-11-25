"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

Two tools:
  - search(query):     returns the best label chunks, each with its citation tag.
  - add_document(path): chunks + embeds + stores one more openFDA label (JSON file),
                        using index.py's own functions (not a copy of them).

Rules from the brief: load index/ at startup, never re-embed the corpus,
print NOTHING to stdout (stdout carries the MCP protocol) -> we log to stderr.
The docstrings below are the tool descriptions the model reads.
"""

import sys
from pathlib import Path

from mcp.server.mcpserver import MCPServer

import retrieve
from config import CHOSEN_DESIGN, ROOT
from index import chunk_file, embed_and_store, read_label

mcp = MCPServer("corpus", log_level="WARNING")

# Load the index once, at startup (opening a collection is cheap; nothing is embedded).
COLLECTION = retrieve.collection_for(CHOSEN_DESIGN)
# Which stored chunks the server uses: "sections_hybrid" stores its chunks as "sections".
STORED_DESIGN = "fixed" if CHOSEN_DESIGN == "fixed" else "sections"
print(f"corpus server ready: {COLLECTION.count()} chunks, design '{CHOSEN_DESIGN}'", file=sys.stderr)


@mcp.tool()
def search(query: str) -> str:
    """Search the official FDA prescribing information (drug labels) of anticoagulants:
    ELIQUIS (apixaban), XARELTO (rivaroxaban), PRADAXA (dabigatran), WARFARIN and
    LOVENOX (enoxaparin), plus any label added later with add_document.

    Use it for any question about these drugs: indications, dosing and dose
    adjustments (renal/hepatic impairment, age, weight), switching between
    anticoagulants, stopping before surgery, contraindications, bleeding risk,
    reversal, drug interactions, pregnancy, overdose, storage.

    Ask one specific question per call (name the drug). Returns the 5 most relevant
    passages. Each passage starts with its citation tag, e.g. [ELIQUIS §2.2],
    meaning label ELIQUIS, section 2.2. Cite answers with exactly these tags.
    """
    print(f"search: {query!r}", file=sys.stderr)
    return retrieve.format_results(retrieve.search(query))


@mcp.tool()
def add_document(path: str) -> str:
    """Add one more FDA drug label to the searchable corpus.

    `path` is an openFDA label JSON file inside this project, e.g.
    corpus/extra/SAVAYSA.json. The file is chunked and embedded with the same
    pipeline as the rest of the corpus. If the same version of that label is
    already indexed, nothing is done; if an older version is indexed, it is
    replaced. Returns what happened and how many chunks were stored.
    """
    file = (ROOT / path).resolve()     # relative paths are relative to the project folder

    # Safety checks before spending any embeddings.
    if not file.is_relative_to(ROOT):
        return f"Refused: {path} is outside the project folder."
    if not file.is_file() or file.suffix.lower() != ".json":
        return f"Refused: {path} is not an existing .json label file."

    source, version, sections = read_label(file)
    if not sections:
        return f"Refused: {path} has none of the expected label sections (is it an openFDA label?)."

    # Decision for "already indexed": same version -> skip; other version -> replace it.
    already = COLLECTION.get(where={"source": source})
    if already["ids"]:
        if already["metadatas"][0]["version"] == version:
            return f"{source} ({version}) is already indexed with {len(already['ids'])} chunks. Nothing changed."
        COLLECTION.delete(ids=already["ids"])
        print(f"replacing old version of {source}", file=sys.stderr)

    chunks = chunk_file(file, STORED_DESIGN)          # same chunking as index.py
    added = embed_and_store(chunks, COLLECTION)       # same embedding + storing as index.py
    retrieve.reset_cache()                            # so keyword search sees the new chunks
    return f"Added {source} ({version}): {len(chunks)} chunks stored ({added} embedded). Cite it as [{source} §section]."


if __name__ == "__main__":
    mcp.run()  # stdio
