"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and section, each with a citation id.
- add_document(path): runs the file through index.py's pipeline, embeds it and stores it.

It loads the committed index/ and never re-embeds the corpus. Nothing is printed
to stdout (it carries the protocol); logs go to stderr.
"""

import os
import sys
from pathlib import Path

os.chdir(Path(__file__).resolve().parent)
sys.path.insert(0, str(Path(__file__).resolve().parent))

from mcp.server.mcpserver import MCPServer  # noqa: E402

import index as pipeline  # noqa: E402
import retrieval  # noqa: E402

mcp = MCPServer("corpus", log_level="WARNING")

# The description lists the documents that are indexed right now (read from
# index/documents.json), so a label added with add_document is announced too.
INDEXED = ", ".join(sorted(pipeline.read_registry())) or "no documents yet"


@mcp.tool(description=f"""Search a corpus of official FDA prescribing information (drug labels).
Indexed now: {INDEXED}. Covers dosing, contraindications, warnings, interactions, adverse
reactions, use in pregnancy, children, elderly and kidney/liver impairment, overdose,
pharmacology and storage.

Use it before answering ANY question about a medicine, even one not in the list above
(documents can be added at any time). Write the query as a short, specific phrase that
names the drug. Call it again with a different query if the first results do not contain
the answer.

Returns the 5 most relevant passages. Each starts with its citation id in brackets,
e.g. [warfarin:drug_interactions:2], followed by the drug, the label file and the section.
Cite those ids in the answer.""")
def search(query: str) -> str:
    """Search the drug-label corpus and return the 5 best passages with citation ids."""
    return retrieval.search(query)


@mcp.tool()
def add_document(path: str) -> str:
    """Add one document to the corpus index: an openFDA drug-label .json file, or a .pdf,
    .txt or .md file. `path` is the file's path on disk. The file is extracted, cleaned,
    chunked by section, embedded and stored, after which search can find it.

    If a file with the same name and identical content is already indexed, nothing is
    changed. If the name matches but the content changed, the old chunks are replaced.
    Returns a one-line summary: added, already indexed, or why it was not added.
    """
    try:
        return pipeline.add_file(path)
    except Exception as error:  # noqa: BLE001 - tell the model what went wrong
        return f"Not added: {type(error).__name__}: {error}"


if __name__ == "__main__":
    mcp.run()  # stdio
