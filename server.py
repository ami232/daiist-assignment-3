
import sys
from pathlib import Path
from contextlib import redirect_stdout
from mcp.server.fastmcp import FastMCP
from retrieval import search as retrieve
from index import add_document as ingest

mcp = FastMCP("corpus")

ROOT = Path(__file__).resolve().parent

@mcp.tool()
def search(query: str) -> list[dict]:
    """Search aviation documents and return relevant passages with page citations."""
    return retrieve(query, k=5)

@mcp.tool()
def add_document(path: str) -> dict:
    """Index a local PDF document. Previously indexed chunks are skipped."""

    file = Path(path)

    if not file.is_absolute():
        file = ROOT / file

    file = file.resolve()

    if not file.is_relative_to(ROOT):
        raise ValueError("File must be inside the project.")

    if not file.is_file() or file.suffix.lower() != ".pdf":
        raise ValueError("A valid PDF file is required.")

    with redirect_stdout(sys.stderr):
        added = ingest(file)

    return {
        "document": file.name,
        "new_chunks": added,
        "status": "indexed" if added else "already indexed"
    }

if __name__ == "__main__":
    mcp.run(transport="stdio")
