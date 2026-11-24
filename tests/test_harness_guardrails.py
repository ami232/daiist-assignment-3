"""
The harness of agent.py with a scripted model and fake tools: no API call, no MCP server.

    uv run python tests/test_harness_guardrails.py

1. Tool-call limit: a model that keeps searching is stopped after MAX_TOOL_CALLS calls.
2. Approval: add_document does not run when the approval is denied, and runs when it is given.
3. Citation check inside a full run: a forged citation turns the answer into a refusal.
"""

import asyncio
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from langchain_core.language_models.chat_models import BaseChatModel  # noqa: E402
from langchain_core.messages import AIMessage  # noqa: E402
from langchain_core.outputs import ChatGeneration, ChatResult  # noqa: E402
from langchain_core.tools import StructuredTool  # noqa: E402

import agent  # noqa: E402

RESULT = """Search results for: {query}
Index: "article" chunks; 1 of 600 stored passages shown, best match first.
To cite a passage, copy its Citation line exactly: [doc_id, location].

=== Result 1 of 1 ===
Citation: [Reg_1299_2014, Annex, 4.2.4.1]
Document: Commission Regulation (EU) No 1299/2014, TSI for the 'infrastructure' subsystem (TSI INF)
Source: https://publications.europa.eu/resource/celex/32014R1299
Similarity: 0.8100
Text:
(1) European standard nominal track gauge shall be 1 435 mm.
"""


class Scripted(BaseChatModel):
    """A chat model that replays a fixed list of messages, one per call."""

    script: list
    calls: int = 0

    @property
    def _llm_type(self) -> str:
        return "scripted"

    def bind_tools(self, tools, **kwargs):
        return self

    def _generate(self, messages, stop=None, run_manager=None, **kwargs) -> ChatResult:
        message = self.script[min(self.calls, len(self.script) - 1)]
        self.calls += 1
        return ChatResult(generations=[ChatGeneration(message=message)])


def tool_call(name: str, n: int, **args) -> AIMessage:
    return AIMessage(content="", tool_calls=[{"name": name, "args": args, "id": f"call_{n}"}])


def make_tools(ran: list) -> list:
    async def search(query: str) -> str:
        ran.append(("search", query))
        return RESULT.format(query=query)

    async def add_document(path: str) -> str:
        ran.append(("add_document", path))
        return "added\ndoc_id: fake\nchunks added (embedded now): 1"

    return [
        StructuredTool.from_function(coroutine=search, name="search", description="search the corpus"),
        StructuredTool.from_function(coroutine=add_document, name="add_document", description="add a document"),
    ]


def run(script, approve=None) -> tuple[dict, list]:
    ran: list = []
    result = asyncio.run(agent.answer_with(Scripted(script=script), make_tools(ran), "test question", approve, system_prompt="test"))
    return result, ran


def main() -> None:
    limit = agent.MAX_TOOL_CALLS

    # 1. A model that asks for 9 searches, then answers.
    final = AIMessage(content="The nominal track gauge is 1 435 mm [Reg_1299_2014, Annex, 4.2.4.1].")
    result, ran = run([tool_call("search", n, query=f"query {n}") for n in range(9)] + [final])
    statuses = [entry["status"] for entry in result["tool_trace"]]
    assert len(ran) == limit, ran
    assert statuses.count("ok") == limit and statuses.count("blocked") == 9 - limit, statuses
    assert "tool_call_limit" in result["guardrail_fired"], result["guardrail_fired"]
    assert result["answer"] == final.content and len(result["citations"]) == 1
    print(f"1. tool-call limit: 9 searches requested, {len(ran)} ran, {statuses.count('blocked')} blocked; guardrails fired: {result['guardrail_fired']}")
    print(f"   answer kept, citation valid: {result['citations'][0]['doc_id']}, {result['citations'][0]['location']}")

    # 2. add_document: denied, automatically denied (no terminal), approved.
    script = [tool_call("add_document", 0, path="corpus/new.pdf"), AIMessage(content="The document was not added: approval was denied.")]
    result, ran = run(script, approve=lambda name, args: False)
    assert ran == [] and result["tool_trace"][0]["status"] == "denied" and result["guardrail_fired"] == ["approval_denied"]
    print(f"\n2. approval denied: add_document ran {len(ran)} times; trace status: {result['tool_trace'][0]['status']}; guardrails fired: {result['guardrail_fired']}")

    result, ran = run(script)  # default approver; this test has no terminal on stdin
    if not sys.stdin.isatty():
        assert ran == [] and result["guardrail_fired"] == ["approval_denied"]
        print(f"   not interactive: add_document ran {len(ran)} times (denied automatically)")

    result, ran = run([script[0], AIMessage(content="The document was added.")], approve=lambda name, args: True)
    assert ran == [("add_document", "corpus/new.pdf")] and result["guardrail_fired"] == []
    print(f"   approval given: add_document ran {len(ran)} time with {ran[0][1]!r}")

    # 3. A forged citation in a full run.
    forged = AIMessage(content="The gauge is 1 435 mm [Reg_1299_2014, Annex, 4.2.4.1] and must be checked yearly [Reg_1299_2014, Annex, 9.9.9].")
    result, ran = run([tool_call("search", 0, query="nominal track gauge"), forged])
    assert result["guardrail_fired"] == ["citation_check"] and result["invalid_citations"] == ["[Reg_1299_2014, Annex, 9.9.9]"]
    assert "yearly" not in result["answer"] and result["refused"] and result["draft_answer"] == forged.content
    print(f"\n3. forged citation in a run: guardrails fired: {result['guardrail_fired']}; invalid: {result['invalid_citations']}")
    print(f"   answer: {result['answer']}")
    print("\nAll harness guardrail checks passed.")


if __name__ == "__main__":
    main()
