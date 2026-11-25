"""
Assignment 3: MCP server `corpus` (Deal Desk). Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): EU merger control and FDI screening passages, with citations.
- add_document(path): runs a file through index.py's pipeline, embeds it and stores it.

It loads index/ at startup and never re-embeds the corpus. Nothing is printed to stdout,
which carries the MCP protocol; logs go to stderr.
"""

import hashlib
import json
from pathlib import Path

from mcp.server.mcpserver import MCPServer

import index as pipeline
from retrieve import Searcher, format_results

mcp = MCPServer("corpus", log_level="WARNING")
REGISTRY = pipeline.INDEX / "documents.json"
_searcher: Searcher | None = None


def searcher() -> Searcher:
    global _searcher
    if _searcher is None:
        _searcher = Searcher()
    return _searcher


def registry() -> dict:
    return json.loads(REGISTRY.read_text()) if REGISTRY.exists() else {}


@mcp.tool()
def search(query: str) -> str:
    """Search Deal Desk's library of EU deal regulation: the EU Merger Regulation 139/2004 (EUMR),
    the Commission Consolidated Jurisdictional Notice (CJN), the Remedies Notice (RN), the Ancillary
    Restraints Notice (ARN) and the FDI Screening Regulation 2019/452 (FDI), plus any document added later.

    Use it for any question about EU merger control or EU foreign-investment screening: notification
    thresholds and turnover, control and joint ventures, suspension and fines, deadlines, remedies,
    non-competes and other ancillary restraints, and FDI screening cooperation. It does NOT cover
    national (e.g. Spanish) or non-EU rules unless such a document has been added.

    Write the query as a full question or as the legal concept you need. Returns the 5 most relevant
    passages, each headed by its citation in square brackets, e.g. [EUMR Art. 1(2)] or [CJN para. 156],
    which is the citation to use in the answer. If no passage answers the question, say so.
    """
    return format_results(searcher().search(query, k=5))


@mcp.tool()
def add_document(path: str) -> str:
    """Add a document to the Deal Desk library so that search can find it.

    `path` is a local file: an HTML page saved from EUR-Lex (parsed into articles or numbered
    paragraphs), a PDF (one unit per page) or a .txt/.md file (one unit per paragraph). The file name
    without extension becomes its short name in citations (e.g. FSR.html -> [FSR Art. 20(3)]).

    If exactly the same file is already indexed, nothing is done. If a different version of a
    document with the same short name is indexed, the old version is replaced. Returns what was done:
    the short name, how many chunks were added and how many new embeddings were needed.
    """
    file = Path(path).expanduser().resolve()
    if not file.is_file():
        return f"Error: no file at {file}."
    source = file.stem.upper()
    sha = hashlib.sha256(file.read_bytes()).hexdigest()
    reg = registry()
    if source in pipeline.DOCUMENTS and source not in reg:
        return f"{source} is part of the base corpus already; nothing was added."
    if reg.get(source, {}).get("sha") == sha:
        return f"{source} ({file.name}) is already indexed with identical content; nothing was added."

    design = searcher().design
    base = "structure" if design == "hybrid" else design
    try:
        chunks = pipeline.chunk_file(file, base, source)
    except Exception as error:  # noqa: BLE001 - reported back to the agent
        return f"Error: could not extract {file.name}: {error}"
    before = len(pipeline.load_vectors())
    pipeline.embed_and_store(chunks)
    new_vectors = len(pipeline.load_vectors()) - before

    # replace an older version of the same document, keep everything else
    kept = [c for c in pipeline.load_chunks(base) if c["source"] != source]
    path_chunks = Path(str(pipeline.CHUNKS).format(design=base))
    with path_chunks.open("w") as f:
        for rec in kept:
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    pipeline.save_chunks(chunks, base, append=True)
    replaced = source in reg
    reg[source] = {"sha": sha, "file": file.name, "chunks": len(chunks)}
    REGISTRY.write_text(json.dumps(reg, indent=2))
    searcher().reload()
    action = "replaced the previous version of" if replaced else "added"
    return (f"Done: {action} {source} ({file.name}): {len(chunks)} chunks in the '{base}' index, "
            f"{new_vectors} new embeddings. Cite it as [{source} <location>].")


if __name__ == "__main__":
    mcp.run()  # stdio
