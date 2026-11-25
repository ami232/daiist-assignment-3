import json
import sys
from pathlib import Path
from contextlib import redirect_stdout

from mcp.server.mcpserver import MCPServer
from index import CORPUS, embed_and_store
from retrieval import rank, selected_design

mcp = MCPServer("corpus", log_level="WARNING")


@mcp.tool()
def search(query: str) -> str:
    """Search the historical macroeconomic corpus by Bagehot and Keynes. Return five relevant passages with their citation IDs, source, chapter and text."""

    with redirect_stdout(sys.stderr):
        results = rank(query, selected_design(), k=5)

    return json.dumps(results, ensure_ascii=False)


@mcp.tool()
def add_document(path: str) -> str:
    """Add a local HTML, PDF, TXT or MD document inside corpus/. Existing embeddings are reused when the same document is indexed again."""

    p = Path(path).resolve()

    if not p.is_relative_to(CORPUS.resolve()):
        raise ValueError("File must be inside corpus/.")

    if not p.is_file():
        raise ValueError("File does not exist.")

    with redirect_stdout(sys.stderr):
        result = embed_and_store(p)

    return json.dumps(result)


if __name__ == "__main__":
    mcp.run()
