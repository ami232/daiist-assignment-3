"""Against the committed index and the real server over MCP, nothing mocked. Skips without an index or key."""

import asyncio
import sys
import unittest
from pathlib import Path

import index
from api_key import resolve_api_key

ROOT = Path(__file__).resolve().parent.parent
HAS_INDEX = (index.INDEX_DIR / "chroma.sqlite3").exists()
HAS_KEY = resolve_api_key()[0] is not None
QUESTION = "How much compensation is due for a cancelled flight of 1,500 km or less?"


async def search_over_mcp(query):
    """Start server.py as an editor would and call search once. Returns the passage ids."""
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT))
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            names = {t.name for t in (await session.list_tools()).tools}
            result = await session.call_tool("search", {"query": query})
            text = "\n".join(getattr(c, "text", "") for c in result.content)
    ids = [line[1:].split("]")[0] for line in text.splitlines() if line.startswith("[")]
    return names, ids, text


@unittest.skipUnless(HAS_INDEX, "index/ not built yet: run `uv run python main.py index`")
class TestCommittedIndex(unittest.TestCase):
    def test_holdout_absent_from_baseline(self):
        db = index.open_index()
        for design in index.DESIGNS:
            got = index.design_collection(db, design).get(where={"source": "32011R0181"}, include=[])
            self.assertEqual(got["ids"], [], f"design {design} contains the held-out document")

    def test_index_under_90_mb(self):
        size = sum(p.stat().st_size for p in index.INDEX_DIR.rglob("*") if p.is_file()) / 1e6
        self.assertLess(size, 90)

    def test_every_chunk_has_a_vector(self):
        db = index.open_index()
        for design in index.DESIGNS:
            got = index.design_collection(db, design).get(include=["embeddings"])
            self.assertTrue(got["ids"])
            self.assertTrue(all(len(v) == index.EMBEDDING_DIMENSIONS for v in got["embeddings"]))


@unittest.skipUnless(HAS_INDEX and HAS_KEY, "needs the built index and a Gemini key (the query is embedded)")
class TestServerOverMCP(unittest.TestCase):
    def test_search_works_and_survives_restart(self):
        names, first, text = asyncio.run(search_over_mcp(QUESTION))
        self.assertEqual({"search", "add_document"}, names)
        self.assertTrue(first)
        self.assertIn("Location:", text)
        _, second, _ = asyncio.run(search_over_mcp(QUESTION))  # a fresh server process
        self.assertEqual(first, second)


if __name__ == "__main__":
    unittest.main()
