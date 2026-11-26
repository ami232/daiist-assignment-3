"""Real stdio MCP + LangChain loop, with a synthetic model/vector fixture.

These tests verify wiring and guards, not Gemini answer quality.
"""

import asyncio
import json
import shutil
import unittest

from langchain_core.language_models.chat_models import BaseChatModel
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.outputs import ChatGeneration, ChatResult

import test_runtime
from agent import AgentRunner
from runtime import ROOT, Retriever


class ScriptedModel(BaseChatModel):
    invent_citation: bool = False

    @property
    def _llm_type(self):
        return "synthetic-test-only"

    def bind_tools(self, tools, **kwargs):
        return self

    def _generate(self, messages, stop=None, run_manager=None, **kwargs):
        if isinstance(messages[-1], ToolMessage):
            payload = json.loads(messages[-1].content)
            chunk_id = "f" * 64 if self.invent_citation else payload["chunks"][0]["id"]
            message = AIMessage(content=f"Synthetic test answer [chunk:{chunk_id}]")
        else:
            message = AIMessage(
                content="",
                tool_calls=[
                    {
                        "name": "search",
                        "args": {"query": "test question"},
                        "id": "test-call",
                    }
                ],
            )
        return ChatResult(generations=[ChatGeneration(message=message)])


class IntegrationTests(unittest.TestCase):
    def setUp(self):
        self.fixture = test_runtime.RuntimeTests(
            methodName="test_dry_run_never_needs_key_or_embeddings"
        )
        self.fixture.setUp()
        self.fixture.initial_index()
        self.root = self.fixture.root
        for name in [
            "server.py",
            "runtime.py",
            "ingestion.py",
            "index.py",
            "api_key.py",
            "AGENTS.md",
        ]:
            shutil.copy2(ROOT / name, self.root / name)
        policy = {
            "student_approved": True,
            "agent_model": "synthetic-test-only",
            "judge_model": "synthetic-test-only",
            "max_model_calls": 4,
            "extra_guardrail": "citation_allowlist",
            "refusal_text": "Not in the documents.",
            "judge_rubric": "Synthetic engineering fixture, not real evaluation.",
        }
        (self.root / "policy_config.json").write_text(json.dumps(policy))
        retriever = Retriever(self.root, query_embed=lambda _: [1, 0])
        retriever.query_vector("test question")
        retriever.close()

    def tearDown(self):
        self.fixture.tearDown()

    def test_actual_stdio_tool_to_langchain_answer(self):
        result = asyncio.run(self.ask(False))
        self.assertFalse(result["refused"])
        self.assertEqual(result["trace"][0]["tool"], "search")
        self.assertEqual(result["trace"][0]["status"], "ok")
        self.assertEqual(result["model_calls"], 1)
        self.assertTrue(result["retrieved"])

    def test_harness_blocks_invented_citation_after_real_search(self):
        result = asyncio.run(self.ask(True))
        self.assertTrue(result["refused"])
        self.assertTrue(result["guardrail"]["triggered"])
        self.assertEqual(result["guardrail"]["invalid_ids"], ["f" * 64])

    async def ask(self, invent):
        async with AgentRunner(
            self.root, model=ScriptedModel(invent_citation=invent)
        ) as runner:
            return await runner.ask("test question")

    def test_approved_add_tool_reuses_vectors_over_stdio(self):
        config = self.fixture.config
        added = dict(config["documents"][0], source="four", path="corpus/four.txt")
        config["additional_documents"] = [added]
        self.fixture.save_config()
        shutil.copy2(
            self.root / config["documents"][0]["path"], self.root / added["path"]
        )

        async def run():
            async with AgentRunner(
                self.root, model=ScriptedModel(), approval=lambda _: True
            ) as runner:
                descriptor = next(
                    t
                    for t in (await runner.session.list_tools()).tools
                    if t.name == "add_document"
                )
                return json.loads(
                    await runner.wrap(descriptor).ainvoke({"path": added["path"]})
                ), runner.trace

        response, trace = asyncio.run(run())
        self.assertEqual(response["source"], "four")
        self.assertEqual(response["new_embedding_calls"], 0)
        self.assertTrue(trace[0]["approval"])
        self.assertEqual(
            len(
                json.loads((self.root / "corpus_config.json").read_text())["documents"]
            ),
            4,
        )


if __name__ == "__main__":
    unittest.main()
