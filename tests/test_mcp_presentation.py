"""Evidence must survive both editor text and structured application transport."""
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from agent import ToolBridge
import server


class PresentationTests(unittest.IsolatedAsyncioTestCase):
    async def test_readable_citations_and_structured_evidence_are_identical(self):
        payload = {"query": "synthetic", "design": "dense", "results": [
            {"id": "synthetic-a", "citation": "[synthetic | 1]", "title": "Synthetic title",
             "url": "https://example.invalid/", "text": "First synthetic passage."},
            {"id": "synthetic-b", "citation": "[synthetic | 2]", "title": "Synthetic title",
             "url": "https://example.invalid/", "text": "Second synthetic passage."}]}
        with patch.object(server, "search_index", return_value=payload):
            result = server.search("synthetic")
        self.assertEqual(result.structured_content, payload)
        readable = result.content[0].text
        for passage in payload["results"]:
            self.assertIn(passage["text"], readable)
            self.assertLess(readable.index(passage["citation"]), readable.index(passage["text"]))

        class Session:
            async def call_tool(self, name, arguments):
                return result

        bridge = ToolBridge(Session())
        await bridge.invoke("search", {"query": "synthetic"})
        self.assertEqual(bridge.trace[0]["status"], "success")
        self.assertEqual(bridge.trace[0]["result"], payload)

    async def test_legacy_json_result_remains_supported(self):
        class Session:
            async def call_tool(self, name, arguments):
                return SimpleNamespace(content=[SimpleNamespace(text='{"results": []}')], is_error=False)

        bridge = ToolBridge(Session())
        await bridge.invoke("search", {"query": "synthetic"})
        self.assertEqual(bridge.trace[0]["status"], "success")
        self.assertEqual(bridge.trace[0]["result"], {"results": []})


if __name__ == "__main__":
    unittest.main()
