"""
Assignment 3: the agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the tools of server.py over MCP and
AGENTS.md as the system prompt.

Guardrails
  1. Approval: add_document pauses (HumanInTheLoopMiddleware) until a person
     approves it at the terminal. With no terminal (evaluation, CI) it is denied.
  2. Call limits: at most MAX_MODEL_CALLS model calls and MAX_SEARCHES searches
     per question.
  3. Citation check (extra guardrail): every [source | location] tag in the
     answer must be one the search tool actually returned, and an answer that
     is not a refusal must cite something. On failure the agent gets one chance
     to fix it; after that the answer is replaced by the refusal.

evaluate.py uses `open_agent()` and `Harness.ask()`, which return the answer,
the tool trace, tokens and seconds.
"""

from __future__ import annotations

import asyncio
import os
import re
import sys
import time
import uuid
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Callable

from langchain.agents import create_agent
from langchain.agents.middleware import (
    HumanInTheLoopMiddleware,
    ModelFallbackMiddleware,
    ModelCallLimitMiddleware,
    ToolCallLimitMiddleware,
)
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.tools import StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
# Overridable with environment variables. gemini-3.8-flash was overloaded/out
# of free quota when this was written; flash-lite answered reliably. Set
# FALLBACK_MODEL to switch to it automatically when CHAT_MODEL fails
# (answers record which model ran).
CHAT_MODEL = os.environ.get("CHAT_MODEL", "gemini-3.1-flash-lite")
FALLBACK_MODEL = os.environ.get("FALLBACK_MODEL", "")
MAX_MODEL_CALLS = 8
MAX_SEARCHES = 5

# Keep in sync with AGENTS.md: evaluate.py detects refusals by this sentence.
REFUSAL = "The corpus does not cover this question."
CITATION_RE = re.compile(r"\[([^\[\]|]+?)\s*\|\s*([^\[\]]+?)\]")
TAG_RE = re.compile(r"^\[([^\[\]|]+?)\s*\|\s*([^\[\]]+?)\] \(score", re.MULTILINE)

Approver = Callable[[str, dict], bool]


def is_refusal(text: str) -> bool:
    return REFUSAL.lower().rstrip(".") in text.lower()


def citations(text: str) -> list[tuple[str, str]]:
    return [(s.strip(), l.strip()) for s, l in CITATION_RE.findall(text)]


def ask_terminal(name: str, args: dict) -> bool:
    """Approval prompt. Without a terminal there is nobody to ask, so the answer is no."""
    if not sys.stdin.isatty():
        print(f"[approval] {name}({args}) denied: no terminal to ask for approval.", file=sys.stderr)
        return False
    reply = input(f"\nThe agent wants to run {name} with {args}. Allow? [y/N] ")
    return reply.strip().lower() in {"y", "yes"}


def deny_all(name: str, args: dict) -> bool:
    return False


async def mcp_tools(session: ClientSession) -> list[StructuredTool]:
    """Wrap each MCP tool of the server as a LangChain tool."""
    tools = []
    for tool in (await session.list_tools()).tools:
        async def call(_name=tool.name, **kwargs):
            result = await session.call_tool(_name, kwargs)
            return "\n".join(getattr(c, "text", "") for c in result.content)

        tools.append(StructuredTool.from_function(
            coroutine=call, name=tool.name, description=tool.description or "",
            args_schema=tool.input_schema))
    return tools


class Harness:
    def __init__(self, tools: list[StructuredTool]):
        self.model = ChatGoogleGenerativeAI(model=CHAT_MODEL, temperature=0, timeout=120,
                                            max_retries=0 if FALLBACK_MODEL else 6)
        fallback = ([ModelFallbackMiddleware(ChatGoogleGenerativeAI(
            model=FALLBACK_MODEL, temperature=0, max_retries=6, timeout=120))] if FALLBACK_MODEL else [])
        self.agent = create_agent(
            model=self.model,
            tools=tools,
            system_prompt=(ROOT / "AGENTS.md").read_text(encoding="utf-8"),
            middleware=[
                HumanInTheLoopMiddleware(interrupt_on={"add_document": True}),
                *fallback,
                ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS, exit_behavior="end"),
                ToolCallLimitMiddleware(tool_name="search", run_limit=MAX_SEARCHES, exit_behavior="continue"),
            ],
            checkpointer=InMemorySaver(),
        )

    async def _run(self, message, config: dict, approve: Approver) -> dict:
        result = await self.agent.ainvoke(message, config)
        while result.get("__interrupt__"):
            request = result["__interrupt__"][0].value
            decisions = []
            for action in request["action_requests"]:
                if approve(action["name"], action["args"]):
                    decisions.append({"type": "approve"})
                else:
                    decisions.append({"type": "reject", "message": "The user did not approve this action."})
            result = await self.agent.ainvoke(Command(resume={"decisions": decisions}), config)
        return result

    async def ask(self, question: str, approve: Approver = ask_terminal) -> dict:
        started = time.time()
        load_api_key()
        config = {"configurable": {"thread_id": str(uuid.uuid4())}}
        result = await self._run({"messages": [HumanMessage(question)]}, config, approve)
        guardrail = []

        answer, problems = self._check(result["messages"])
        if problems:
            guardrail.append({"stage": "first answer", "problems": problems})
            fix = ("Your answer failed the citation check: " + "; ".join(problems) + ". "
                   "Rewrite it citing only tags exactly as the search tool returned them, "
                   f"or, if the search results do not answer the question, reply: {REFUSAL}")
            result = await self._run({"messages": [HumanMessage(fix)]}, config, approve)
            answer, problems = self._check(result["messages"])
            if problems:
                guardrail.append({"stage": "after retry", "problems": problems})
                answer = REFUSAL + " (The answer was withheld because its citations could not be verified.)"

        messages = result["messages"]
        return {
            "question": question,
            "answer": answer,
            "trace": self._trace(messages),
            "retrieved_tags": sorted(self._retrieved(messages)),
            "guardrail": guardrail,
            "tokens": sum((m.usage_metadata or {}).get("total_tokens", 0)
                          for m in messages if isinstance(m, AIMessage)),
            "model_calls": sum(isinstance(m, AIMessage) for m in messages),
            "models": sorted({m.response_metadata.get("model_name", "?") for m in messages
                              if isinstance(m, AIMessage)}),
            "seconds": round(time.time() - started, 2),
        }

    @staticmethod
    def _retrieved(messages) -> set[tuple[str, str]]:
        tags = set()
        for m in messages:
            if isinstance(m, ToolMessage) and m.name == "search":
                tags |= {(s.strip(), l.strip()) for s, l in TAG_RE.findall(m.text)}
        return tags

    def _check(self, messages) -> tuple[str, list[str]]:
        final = next((m for m in reversed(messages) if isinstance(m, AIMessage) and not m.tool_calls), None)
        answer = final.text.strip() if final else ""
        if not answer:
            return answer, ["the answer is empty"]
        if is_refusal(answer):
            return answer, []
        cited = citations(answer)
        if not cited:
            return answer, ["the answer cites no passage"]
        retrieved = self._retrieved(messages)
        bad = [f"[{s} | {l}]" for s, l in cited if (s, l) not in retrieved]
        return answer, [f"{tag} was not returned by search" for tag in bad]

    @staticmethod
    def _trace(messages) -> list[dict]:
        trace, outputs = [], {m.tool_call_id: m.text for m in messages if isinstance(m, ToolMessage)}
        for m in messages:
            if isinstance(m, AIMessage):
                for call in m.tool_calls:
                    trace.append({"tool": call["name"], "args": call["args"],
                                  "output": outputs.get(call["id"], "")})
        return trace


@asynccontextmanager
async def open_agent():
    """Start server.py over stdio and yield a Harness bound to its tools."""
    load_api_key()   # puts the key in os.environ (from .env if needed)
    # The MCP client passes only a few "safe" variables by default; the server needs the key.
    params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT),
                                   env=dict(os.environ))
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            yield Harness(await mcp_tools(session))


async def answer_async(question: str, approve: Approver = ask_terminal) -> dict:
    async with open_agent() as harness:
        return await harness.ask(question, approve)


def answer(question: str, approve: Approver = ask_terminal) -> dict:
    return asyncio.run(answer_async(question, approve))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit('usage: python agent.py "your question"')
    out = answer(" ".join(sys.argv[1:]))
    print(out["answer"])
    sources = sorted(set(citations(out["answer"])))
    if sources:
        print("\nSources:")
        for s, l in sources:
            print(f"  - {s}, {l}")
    for g in out["guardrail"]:
        print(f"[guardrail] {g['stage']}: {'; '.join(g['problems'])}", file=sys.stderr)
    print(f"\n({out['tokens']} tokens, {out['seconds']}s, {len(out['trace'])} tool calls)", file=sys.stderr)
