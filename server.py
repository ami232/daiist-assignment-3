"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Load index/ at startup; never re-embed the corpus. Print nothing to stdout
(it carries the protocol); log to stderr. Docstrings become the tool
descriptions the model reads.
"""

from pathlib import Path

from mcp.server.mcpserver import MCPServer
from mcp.server.mcpserver.exceptions import ToolError

import index      # the same pipeline `main.py index` uses

ROOT = Path(__file__).resolve().parent
mcp = MCPServer("corpus", log_level="WARNING")


@mcp.tool()
def search(query: str) -> str:
    """Search the EU data-law corpus: the GDPR (source `gdpr`), the Data Governance
    Act (`dga`) and the Free Flow of Non-Personal Data Regulation (`ffd`), plus any
    document added with add_document. Use it for every question about what these laws
    say (obligations, deadlines, fines, definitions, rights, transfers, data re-use).
    Give a full question in English, one topic per query. Returns the 5 most relevant
    passages. Each starts with its citation tag, for example [gdpr | Article 33]; cite
    a passage by copying its tag exactly. If no passage answers the question, the
    corpus does not cover it."""
    hits = index.search(query)
    return index.format_results(hits) if hits else "The index is empty. Run `uv run python main.py index`."


@mcp.tool()
def add_document(path: str) -> str:
    """Add one document to the corpus index so that search can find it. `path` is an
    EU legal act saved as an .html file from EUR-Lex (absolute, or relative to the
    project folder). It goes through the same extract, chunk, embed and store pipeline
    as the corpus; the file name becomes its source name in citations. If the same
    content is already indexed nothing changes; a different version replaces the old
    one. Returns one line saying what happened. Call it only when the user explicitly
    asks to add a document."""
    file = Path(path) if Path(path).is_absolute() else ROOT / path
    if not file.is_file() or file.suffix.lower() not in (".html", ".htm"):
        raise ToolError(f"{file} is not an existing .html file.")
    try:
        chunks = index.chunk_file(file)
    except ValueError as error:
        raise ToolError(str(error))
    source = chunks[0]["meta"]["source"]
    old = set(index.stored_ids(source))
    if old == {c["id"] for c in chunks}:
        return f"'{source}' is already indexed with the same content ({len(old)} chunks). Nothing changed."
    new = index.embed_and_store(chunks)
    action = "Replaced the older version of" if old else "Added"
    return f"{action} '{source}': {len(chunks)} chunks stored, {new} newly embedded."


if __name__ == "__main__":
    mcp.run()  # stdio
