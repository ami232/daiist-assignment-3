"""Tests for agent.py's plumbing: the MCP -> LangChain bridge and citation parsing.
They never call the chat model, so they cost nothing."""

import asyncio
import os

import agent
import index
from conftest import fake_embed


def test_citations_are_read_from_an_answer():
    answer = "La fianza es de una mensualidad [LAU, Artículo 36, p. 25] y se deposita [LAU, p. 26]."
    assert agent.citations(answer) == [("LAU", "Artículo 36, p. 25"), ("LAU", "p. 26")]


def test_an_answer_without_citations_has_none():
    assert agent.citations("No lo sé.") == []


def test_mcp_tools_become_langchain_tools_that_call_the_server(tmp_path):
    doc = tmp_path / "guia.txt"
    doc.write_text("Artículo 1. Devolución.\nLa fianza se devuelve en el plazo de un mes.\n")
    index.index_file(doc, path_index=tmp_path, embed_fn=fake_embed)
    query = "cuándo me devuelven la fianza"
    index.embed_texts([query], index.QUERY_TASK, embed_fn=fake_embed, cache=index.VectorCache(tmp_path / "vectors.sqlite"))

    async def run():
        async with agent.mcp_tools(env={**os.environ, "RAG_INDEX_DIR": str(tmp_path)}) as tools:
            by_name = {t.name: t for t in tools}
            assert set(by_name) == {"search", "add_document"}
            assert "fianza" in by_name["search"].description
            return await by_name["search"].ainvoke({"query": query})

    text = asyncio.run(asyncio.wait_for(run(), 60))
    assert "[guia, Artículo 1]" in text
