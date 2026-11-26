"""Local stdio MCP server. Only protocol messages go to stdout."""

from __future__ import annotations

import asyncio
import json
from typing import Annotated

from mcp.server.mcpserver import MCPServer
from pydantic import Field

from runtime import Retriever
from runtime import add_document as ingest_document

# Construct only on a tool call: listing tools never needs a key or network.
# The service stores vectors on disk; each operation uses its own connection.
lock = asyncio.Lock()

mcp = MCPServer("corpus", log_level="WARNING")


def _search(query: str) -> dict:
    retriever = Retriever()
    try:
        return retriever.search(query, k=retriever.config.get("retrieval_k", 5))
    finally:
        retriever.close()


@mcp.tool(
    annotations={
        "readOnlyHint": True,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    }
)
async def search(query: Annotated[str, Field(min_length=1, max_length=8000)]) -> str:
    """Search the approved local document corpus for evidence to answer a question.

    Returns JSON with up to five chunks: exact text, source ID, page/word
    location, cosine score, and [chunk:ID] citation. Scores rank passages;
    they are not probabilities that an answer is true. Query embedding may
    call Gemini, but saved corpus vectors are never regenerated here.
    If the passages do not support the question, say the corpus cannot answer.
    """
    async with lock:
        return json.dumps(await asyncio.to_thread(_search, query), ensure_ascii=False)


@mcp.tool(
    annotations={
        "readOnlyHint": False,
        "destructiveHint": False,
        "idempotentHint": True,
        "openWorldHint": True,
    }
)
async def add_document(
    path: Annotated[str, Field(min_length=1, max_length=1000)],
) -> str:
    """Index a registered, provenance-reviewed PDF/TXT/MD under corpus/.

    The harness must obtain human approval before calling this write tool.
    The path must be listed in corpus_config.json, including its reuse licence.
    Imports the shared ingestion pipeline; reuses saved Gemini vectors.
    An identical file is a no-op; a changed file replaces that source's chunks.
    Returns source, status, word/chunk counts and number of new embeddings.
    Never use for arbitrary local files, secrets or personal data.
    """
    async with lock:
        return json.dumps(
            await asyncio.to_thread(ingest_document, path), ensure_ascii=False
        )


if __name__ == "__main__":
    mcp.run()
