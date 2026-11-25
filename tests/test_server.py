"""Talk to server.py over stdio, as an editor (and check.py) does. No API calls:
the index is built with the fake embedder and the query vectors are pre-cached."""

import asyncio
import os
import sys
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

import index
from conftest import fake_embed

ROOT = Path(__file__).resolve().parent.parent


def call(index_dir: Path, tool: str | None = None, args: dict | None = None):
    """Start the server, list its tools and optionally call one. Returns (tools, text)."""

    async def run():
        params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT),
                                       env={**os.environ, "RAG_INDEX_DIR": str(index_dir)})
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools = (await session.list_tools()).tools
                text = None
                if tool:
                    result = await session.call_tool(tool, args or {})
                    text = "\n".join(getattr(c, "text", "") for c in result.content)
                return tools, text

    return asyncio.run(asyncio.wait_for(run(), 60))


def test_server_lists_search_and_add_document_with_descriptions(tmp_path):
    tools, _ = call(tmp_path)
    by_name = {t.name: t for t in tools}
    assert by_name["search"].input_schema["required"] == ["query"]
    assert by_name["add_document"].input_schema["required"] == ["path"]
    assert all(len(t.description or "") > 40 for t in tools)


def test_search_on_an_empty_index_says_nothing_was_found(tmp_path):
    _, text = call(tmp_path, "search", {"query": "anything"})
    assert "No passages found" in text


def test_search_returns_chunks_with_citations(tmp_path):
    doc = tmp_path / "guia.txt"
    doc.write_text("Artículo 1. Devolución.\nLa fianza se devuelve en el plazo de un mes.\n")
    index.index_file(doc, path_index=tmp_path, embed_fn=fake_embed)
    query = "cuándo me devuelven la fianza"
    index.embed_texts([query], index.QUERY_TASK, embed_fn=fake_embed, cache=index.VectorCache(tmp_path / "vectors.sqlite"))
    _, text = call(tmp_path, "search", {"query": query})
    assert "[guia, Artículo 1]" in text and "plazo de un mes" in text


def test_add_document_reports_a_document_that_is_already_indexed(tmp_path):
    doc = tmp_path / "guia.txt"
    doc.write_text("Artículo 1. Devolución.\nLa fianza se devuelve en el plazo de un mes.\n")
    index.index_file(doc, path_index=tmp_path, embed_fn=fake_embed)
    _, text = call(tmp_path, "add_document", {"path": str(doc)})
    assert "already indexed" in text


def test_add_document_explains_a_missing_file(tmp_path):
    _, text = call(tmp_path, "add_document", {"path": str(tmp_path / "nope.pdf")})
    assert "Could not add" in text and "No file" in text
