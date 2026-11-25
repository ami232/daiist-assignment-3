"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Loads index/ at startup; never re-embeds the corpus. Prints nothing to stdout
(it carries the protocol); everything is logged to stderr.
"""

import os
import shutil
import sys
from pathlib import Path

os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")

from mcp.server.mcpserver import MCPServer

import index

mcp = MCPServer("corpus", log_level="WARNING")

TOP_K = 5


@mcp.tool()
def search(query: str) -> str:
    """Search a collection of 49 B2B commercial contracts (Spanish companies; services, supply,
    licensing, distribution, franchise, consulting, IoT, logistics, etc.) and return the 5 passages
    that best match the query. Use it whenever the question is about what a contract says: who the
    parties are, fees, liability caps, termination and notice, data protection, intellectual
    property, governing law, exclusivity, penalties.

    Each result starts with its citation, [CONTRACT_xxx.pdf | clause / page], followed by the
    passage text. Cite the source and clause of every claim you make. Mention the contract's
    parties or subject in the query when you know them: clauses of different contracts look alike.
    Results are the closest passages, not guaranteed answers: if none of them says what the
    question asks, the corpus does not cover it. Lower `distance` means closer.
    """
    try:
        hits = index.retrieve(query, k=TOP_K)
    except index.QuotaExhausted:
        return "ERROR: the embedding quota is exhausted for today; try again later."
    if not hits:
        return "No passages found: the index is empty."
    blocks = []
    for n, h in enumerate(hits, 1):
        m = h["metadata"]
        blocks.append(f"[{n}] [{m['source']} | {m['location']}] (distance {h['distance']:.3f})\n{h['text']}")
    return "\n\n".join(blocks)


@mcp.tool()
def add_document(path: str) -> str:
    """Add one more contract (a PDF file) to the searchable corpus: extracts and chunks it like the
    rest, embeds the chunks (this spends embedding quota) and stores them in the index. `path` is the
    PDF's path on this machine. If the same file is already indexed with the same content, nothing is
    embedded and the tool says so; if a file with the same name but different content is indexed, its
    old chunks are replaced. Only call it when the user asks to add a document, and say what you added."""
    source = Path(path).expanduser()
    if not source.is_file():
        return f"ERROR: no file at {path}."
    if source.suffix.lower() != ".pdf":
        return f"ERROR: only PDF files can be added; {source.name} is not one."
    target = index.CORPUS_DIR / source.name
    try:
        if source.resolve() != target.resolve():       # keep the corpus folder complete and reproducible
            target.parent.mkdir(exist_ok=True)
            shutil.copy2(source, target)
        before = index.collection(index.ACTIVE_DESIGN).get(where={"source": source.name}, include=[])["ids"]
        r = index.index_file(target)
    except index.QuotaExhausted:
        return "ERROR: the embedding quota is exhausted for today; the document was not added."
    except Exception as error:  # noqa: BLE001 - tell the model what went wrong
        return f"ERROR: could not add {source.name}: {type(error).__name__}: {error}"
    if r["new"] == 0 and not r["removed"] and before:
        return f"{source.name} is already indexed with the same content ({r['chunks']} chunks). Nothing was embedded."
    action = "Replaced" if before else "Added"
    return (f"{action} {source.name}: {r['chunks']} chunks ({r['new']} embedded, {r['existing']} already saved, "
            f"{r['removed']} old chunks removed). It is searchable now.")


if __name__ == "__main__":
    print("corpus server: loading index/ ...", file=sys.stderr)
    mcp.run()  # stdio
