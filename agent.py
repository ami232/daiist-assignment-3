"""
Assignment 3: your agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the tools of server.py over MCP and AGENTS.md as the
system prompt. Guardrails:

  1. APPROVAL    add_document never runs without the user's explicit yes (`approve` callback).
  2. LIMITS      at most MAX_TOOL_CALLS tool calls and MAX_MODEL_CALLS model calls per question.
  3. CITATIONS   (my own guardrail) every `[source | location]` in the answer must be a passage
                 that `search` really returned in this run, and an answer that is not a refusal
                 must cite at least one. If not, the agent is sent back once to fix it.

Importable: `ask(question)` / `ask_many(questions)` return Result objects (answer, tool trace,
tokens, seconds) for evaluate.py.
"""

from __future__ import annotations

import asyncio
import os
import sys
import time
from contextlib import AsyncExitStack
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from api_key import load_api_key
from rag import CITATION_RE, norm_key, parse_passages

ROOT = Path(__file__).resolve().parent
MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite")
MAX_TOOL_CALLS = 6
MAX_MODEL_CALLS = 10
REFUSAL_MARKER = "the corpus does not cover"  # keep in sync with rule 5 of AGENTS.md


def is_refusal(answer: str) -> bool:
    return REFUSAL_MARKER in answer.lower()


@dataclass
class Result:
    question: str
    answer: str = ""
    tool_calls: list[dict] = field(default_factory=list)  # {name, args, result}
    retrieved: list[dict] = field(default_factory=list)  # {source, location, text} from search results
    approvals: list[dict] = field(default_factory=list)  # {tool, args, approved}
    guardrail_fired: bool = False
    guardrail_problems: list[str] = field(default_factory=list)
    input_tokens: int = 0
    output_tokens: int = 0
    seconds: float = 0.0
    error: str = ""


def cli_approve(tool: str, args: dict) -> bool:
    """Ask on the terminal. Without a terminal the answer is no (safe default)."""
    if not sys.stdin.isatty():
        return False
    print(f"\nThe agent wants to run {tool} with {args}.", file=sys.stderr)
    return input("Allow? [y/N] ").strip().lower() in {"y", "yes", "s", "si", "sí"}


def deny_all(tool: str, args: dict) -> bool:
    return False


def _text(content) -> str:
    if isinstance(content, str):
        return content
    parts = []
    for block in content or []:
        if isinstance(block, str):
            parts.append(block)
        elif isinstance(block, dict) and block.get("type") == "text":
            parts.append(block.get("text", ""))
    return "".join(parts)


def check_citations(answer: str, retrieved: list[dict]) -> list[str]:
    """Guardrail 3, also used by evaluate.py as a code check. Returns a list of problems."""
    if is_refusal(answer):
        return []
    known = {norm_key(p["source"], p["location"]) for p in retrieved}
    cited = [norm_key(s, l) for s, l in CITATION_RE.findall(answer)]
    problems = []
    if not cited:
        problems.append("the answer contains no citation in the form [source | location]")
    for key in dict.fromkeys(cited):
        if key not in known:
            problems.append(f"cited '{key}' which was not in the search results")
    return problems


class CorpusAgent:
    """Starts server.py over stdio once, builds the agent, answers many questions."""

    def __init__(self, approve: Callable[[str, dict], bool] = cli_approve, server_args=("server.py",)):
        self.approve = approve
        self.server_args = list(server_args)
        self._stack = AsyncExitStack()
        self._approvals: list[dict] = []

    async def __aenter__(self):
        from langchain.agents import create_agent
        from langchain.agents.middleware import ModelCallLimitMiddleware, ToolCallLimitMiddleware
        from langchain_core.tools import StructuredTool
        from langchain_google_genai import ChatGoogleGenerativeAI
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client

        load_api_key()
        params = StdioServerParameters(command=sys.executable, args=self.server_args, cwd=str(ROOT))
        read, write = await self._stack.enter_async_context(stdio_client(params))
        self.session = await self._stack.enter_async_context(ClientSession(read, write))
        await self.session.initialize()
        mcp_tools = (await self.session.list_tools()).tools

        def wrap(mcp_tool):
            async def call(**kwargs):
                if mcp_tool.name == "add_document":  # guardrail 1: approval before it runs
                    ok = bool(self.approve(mcp_tool.name, kwargs))
                    self._approvals.append({"tool": mcp_tool.name, "args": kwargs, "approved": ok})
                    if not ok:
                        return "DENIED: the user did not approve add_document. Nothing was added. Tell the user."
                res = await self.session.call_tool(mcp_tool.name, kwargs)
                text = "\n".join(getattr(c, "text", "") for c in res.content)
                failed = getattr(res, "is_error", False) or getattr(res, "isError", False)
                return f"ERROR: {text}" if failed else text

            return StructuredTool(
                name=mcp_tool.name,
                description=mcp_tool.description or "",
                args_schema=mcp_tool.input_schema,
                coroutine=call,
            )

        self.tools = [wrap(t) for t in mcp_tools]
        model = ChatGoogleGenerativeAI(model=MODEL, temperature=0)
        self.agent = create_agent(
            model,
            self.tools,
            system_prompt=(ROOT / "AGENTS.md").read_text(encoding="utf-8"),
            middleware=[  # guardrail 2
                ToolCallLimitMiddleware(run_limit=MAX_TOOL_CALLS, exit_behavior="continue"),
                ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS, exit_behavior="end"),
            ],
        )
        return self

    async def __aexit__(self, *exc):
        await self._stack.aclose()

    async def _run(self, messages: list):
        out = await self.agent.ainvoke({"messages": messages}, config={"recursion_limit": 40})
        return out["messages"]

    async def ask(self, question: str) -> Result:
        from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

        result = Result(question)
        self._approvals.clear()
        started = time.time()
        try:
            messages = await self._run([HumanMessage(question)])
            self._collect(result, messages)
            problems = check_citations(result.answer, result.retrieved)
            if problems:  # guardrail 3: send the agent back once
                result.guardrail_fired = True
                result.guardrail_problems = problems
                feedback = (
                    "Your answer broke the citation rules: " + "; ".join(problems) + ". Rewrite it using only "
                    "passages you retrieved, citing each as [source | location], or reply exactly "
                    "'The corpus does not cover this question.' if they do not answer it."
                )
                messages = await self._run(messages + [HumanMessage(feedback)])
                self._collect(result, messages, reset=False)
        except Exception as error:  # noqa: BLE001 - the evaluation records failures, it does not stop
            result.error = f"{type(error).__name__}: {error}"
        result.approvals = list(self._approvals)
        result.seconds = round(time.time() - started, 2)
        return result

    @staticmethod
    def _collect(result: Result, messages: list, reset: bool = True) -> None:
        from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

        # Only the messages after the last user turn belong to this attempt.
        last_user = max(i for i, m in enumerate(messages) if isinstance(m, HumanMessage))
        if reset:
            result.tool_calls, result.retrieved, result.input_tokens, result.output_tokens = [], [], 0, 0
        pending: dict[str, dict] = {}
        for m in messages[last_user + 1 :]:
            if isinstance(m, AIMessage):
                usage = getattr(m, "usage_metadata", None) or {}
                result.input_tokens += usage.get("input_tokens", 0)
                result.output_tokens += usage.get("output_tokens", 0)
                for tc in m.tool_calls:
                    entry = {"name": tc["name"], "args": tc["args"], "result": ""}
                    pending[tc["id"]] = entry
                    result.tool_calls.append(entry)
                text = _text(m.content).strip()
                if text and not m.tool_calls:
                    result.answer = text
            elif isinstance(m, ToolMessage):
                entry = pending.get(m.tool_call_id)
                body = _text(m.content)
                if entry is not None:
                    entry["result"] = body
                if entry is not None and entry["name"] == "search":
                    result.retrieved.extend(parse_passages(body))


async def _ask_many(questions: list[str], approve, on_result=None) -> list[Result]:
    results = []
    async with CorpusAgent(approve) as agent:
        for q in questions:
            r = await agent.ask(q)
            results.append(r)
            if on_result:
                on_result(r)
    return results


def ask_many(questions: list[str], approve=deny_all, on_result=None) -> list[Result]:
    return asyncio.run(_ask_many(questions, approve, on_result))


def ask(question: str, approve=cli_approve) -> Result:
    return ask_many([question], approve)[0]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit('usage: python agent.py "your question"')
    r = ask(" ".join(sys.argv[1:]))
    if r.error:
        sys.exit(f"The agent failed: {r.error}")
    for tc in r.tool_calls:
        print(f"[tool] {tc['name']}({tc['args']})", file=sys.stderr)
    if r.guardrail_fired:
        print(f"[guardrail] citation check fired: {r.guardrail_problems}", file=sys.stderr)
    print(f"[cost] {r.input_tokens} in / {r.output_tokens} out tokens, {r.seconds}s", file=sys.stderr)
    print(r.answer or "(no answer)")
