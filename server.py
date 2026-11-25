"""
Assignment 3: MCP server. Your editor and agent.py start it; by hand: `uv run server.py`.

- search(query): returns chunks with source and location.
- add_document(path): runs the file through index.py's pipeline, embeds it
  and stores it.

Load index/ at startup; never re-embed the corpus. Print nothing to stdout
(it carries the protocol); log to stderr. Docstrings become the tool
descriptions the model reads.
"""

import json
import sys
from contextlib import redirect_stdout
from pathlib import Path

from google import genai
from google.genai import types
from mcp.server.mcpserver import MCPServer

from api_key import load_api_key
from index import CORPUS_DIR, EMBED_DIM, EMBED_MODEL, ROOT, get_collection, index_file

mcp = MCPServer("corpus", log_level="WARNING")


@mcp.tool()
def search(query: str) -> str:
    """Search indexed CFPB personal-finance guides for relevant passages.

    Use for questions on budgeting, bills, debt, credit, or mortgages. Returns
    up to five source passages with PDF filename, page number, and citation.
    Search results are evidence, not a final answer or professional advice.
    """
    if not query.strip():
        return json.dumps({"error": "The search query must not be empty."})

    collection = get_collection()
    count = collection.count()
    if count == 0:
        return json.dumps({"error": "The document index is empty. Run main.py index first."})

    client = genai.Client(api_key=load_api_key())
    try:
        response = client.models.embed_content(
            model=EMBED_MODEL,
            contents=f"query: {query.strip()}",
            config=types.EmbedContentConfig(output_dimensionality=EMBED_DIM),
        )
    finally:
        client.close()

    result = collection.query(
        query_embeddings=[response.embeddings[0].values],
        n_results=min(5, count),
        include=["documents", "metadatas", "distances"],
    )

    passages = []
    for rank, (passage, meta, distance) in enumerate(
        zip(
            result["documents"][0],
            result["metadatas"][0],
            result["distances"][0],
        ),
        start=1,
    ):
        source = str(meta.get("source", "unknown"))
        location = str(meta.get("location", f"page {meta.get('page', '?')}"))
        passages.append(
            {
                "rank": rank,
                "citation": f"{source}, {location}",
                "source": source,
                "location": location,
                "source_url": str(meta.get("source_url", "")),
                "text": passage,
                "distance": round(float(distance), 4),
            }
        )
    return json.dumps({"query": query, "passages": passages}, ensure_ascii=False)


@mcp.tool()
def add_document(path: str) -> str:
    """Index a new, locally uploaded PDF in corpus/ and make it searchable.

    The file must already exist inside this project's corpus/ folder. The
    calling agent must request the user's approval before invoking this tool.
    Identical files are skipped; changed files of the same name are rejected.
    Returns the count of newly added document chunks.
    """
    if not path.strip():
        return json.dumps({"error": "A PDF path is required."})

    proposed = Path(path).expanduser()
    if not proposed.is_absolute():
        proposed = ROOT / proposed
    proposed = proposed.resolve()

    # Only read documents intentionally placed in this project's corpus.
    if not proposed.is_relative_to(CORPUS_DIR.resolve()):
        return json.dumps({"error": "PDF must be inside the project corpus/ folder."})
    if not proposed.is_file() or proposed.suffix.lower() != ".pdf":
        return json.dumps({"error": f"Not a readable PDF: {proposed.name}"})

    # index_file prints progress. MCP stdio reserves stdout for protocol data.
    try:
        with redirect_stdout(sys.stderr):
            added = index_file(proposed)
    except (ValueError, OSError) as error:
        return json.dumps({"error": str(error)})

    return json.dumps(
        {
            "file": proposed.name,
            "new_chunks_added": added,
            "total_indexed_chunks": get_collection().count(),
            "status": "already indexed" if added == 0 else "indexed",
        }
    )


if __name__ == "__main__":
    mcp.run()  # stdio: do not print anything to stdout


