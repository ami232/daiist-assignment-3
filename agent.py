"""
Assignment 3: your agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with tools from server.py over MCP and
AGENTS.md as system prompt. Ask for approval before add_document runs; add a
call limit and one guardrail of your choice. Print the answer with citations.

Start from session 10's 07-own-harness/harness.py. Expose a function that
returns the answer and the tool trace, for evaluate.py.
"""

from __future__ import annotations

import asyncio
import sys
from pathlib import Path
from typing import Callable

from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
MAX_TOOL_CALLS = 6


def call_mcp(tool_name: str, arguments: dict) -> str:
    async def run():
        params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT))
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                result = await session.call_tool(tool_name, arguments)
                return "\n".join(getattr(item, "text", "") for item in result.content).strip()
    return asyncio.run(run())


class AgentHarness:
    def __init__(self, approval: Callable[[str], bool] | None = None):
        self.approval = approval
        self.tool_calls = 0
        self.trace: list[dict] = []
        self.evidence_seen = False

    def search(self, query: str) -> str:
        if self.tool_calls >= MAX_TOOL_CALLS:
            result = "Tool call limit reached. Use only the evidence already retrieved."
        else:
            self.tool_calls += 1
            result = call_mcp("search", {"query": query})
            self.evidence_seen = bool(result and not result.startswith("No matching") and not result.startswith("Search failed"))
            self.trace.append({"tool": "search", "arguments": {"query": query}, "result": result})
        return result

    def add_document(self, path: str) -> str:
        if self.tool_calls >= MAX_TOOL_CALLS:
            result = "Tool call limit reached; document was not added."
        else:
            prompt = f"Approve adding document '{path}' to the corpus?"
            approved = self.approval(prompt) if self.approval else False
            self.trace.append({"tool": "add_document", "arguments": {"path": path}, "approved": approved})
            if not approved:
                result = "Document addition declined by the approval guard."
            else:
                self.tool_calls += 1
                result = call_mcp("add_document", {"path": path})
                self.trace[-1]["result"] = result
        return result


def run_agent(question: str, approval: Callable[[str], bool] | None = None) -> tuple[str, list[dict]]:
    load_api_key()
    harness = AgentHarness(approval)

    @tool
    def search(query: str) -> str:
        """Retrieve relevant FDA drug-label passages and citations from the corpus."""
        return harness.search(query)

    @tool
    def add_document(path: str) -> str:
        """Add a .txt, .md, or .pdf document after explicit approval."""
        return harness.add_document(path)

    system_prompt = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    agent = create_agent(
        ChatGoogleGenerativeAI(model="gemini-3.5-flash-lite", temperature=0),
        tools=[search, add_document],
        system_prompt=system_prompt,
    )
    result = agent.invoke({"messages": [{"role": "user", "content": question}]})
    answer = result["messages"][-1].content
    if not harness.evidence_seen and not any(t["tool"] == "search" for t in harness.trace):
        answer = "I don't know: I did not retrieve corpus evidence for this question."
    if isinstance(answer, list):
        answer = "".join(part.get("text", "") if isinstance(part, dict) else str(part) for part in answer)
    return str(answer), harness.trace


def _terminal_approval(prompt: str) -> bool:
    return input(f"{prompt} [y/N]: ").strip().lower() in {"y", "yes"}


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit('Usage: python agent.py "question"')
    question = " ".join(sys.argv[1:])
    try:
        answer, trace = run_agent(question, _terminal_approval)
    except Exception as error:
        print(f"Agent failed: {type(error).__name__}: {error}", file=sys.stderr)
        raise SystemExit(1)
    print(answer)
