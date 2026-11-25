"""
Assignment 3: the agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the tools of server.py over MCP and
AGENTS.md as system prompt. Guardrails:

  1. Approval: add_document only runs after a human says yes (middleware).
  2. Call limits: at most 6 tool calls and 8 model calls per question.
  3. Citation guardrail (extra): after the agent answers, code checks that every
     citation points to a passage the search tool actually returned, and that a
     non-refusal answer cites something. If not, the agent gets one retry with
     the problem spelled out; if it still fails, the answer is replaced by the
     refusal. An invented citation in a compliance answer is worse than no answer.

`Harness` keeps one MCP session open for many questions (evaluate.py uses it);
`ask()` answers one question and returns answer, trace, tokens and seconds.
"""

from __future__ import annotations

import asyncio
import os
import sys
import time
from pathlib import Path
from typing import Callable

os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")

from langchain.agents import create_agent
from langchain.agents.middleware import (ModelCallLimitMiddleware, ModelFallbackMiddleware,
                                        ToolCallLimitMiddleware, wrap_tool_call)
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.tools import StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

import retrieval
from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
# Free-tier daily request limits are per model (gemini-3.5-flash: only 20/day), so
# the agent falls back to the next model when one is exhausted or overloaded.
MODELS = ["gemini-3.5-flash-lite", "gemini-3.1-flash-lite", "gemini-3.5-flash"]
MAX_TOOL_CALLS = 6
MAX_MODEL_CALLS = 8
SYSTEM_PROMPT = (ROOT / "AGENTS.md").read_text(encoding="utf-8")


# --------------------------------------------------------------------------- MCP -> LangChain

def mcp_to_langchain(session: ClientSession, tool) -> StructuredTool:
    """Wrap one MCP tool as a LangChain tool that calls it over the open session."""

    async def call(**kwargs) -> str:
        result = await session.call_tool(tool.name, kwargs)
        text = "\n".join(getattr(c, "text", "") for c in result.content)
        if getattr(result, "is_error", False) or getattr(result, "isError", False):
            return f"Tool error: {text}"
        return text

    return StructuredTool(
        name=tool.name,
        description=tool.description or "",
        args_schema=tool.input_schema,
        coroutine=call,
    )


# --------------------------------------------------------------------------- guardrail 1: approval

def console_approval(tool_name: str, args: dict) -> bool:
    """Ask on the terminal. Non-interactive runs (no TTY) are denied."""
    if not sys.stdin.isatty():
        print(f"[approval] {tool_name}({args}) denied: no one at the terminal to approve it.", file=sys.stderr)
        return False
    reply = input(f"\nThe agent wants to run {tool_name} with {args}. Allow? [y/N] ")
    return reply.strip().lower() in ("y", "yes")


def approval_middleware(approve: Callable[[str, dict], bool], events: list):
    @wrap_tool_call
    async def require_approval(request, handler):
        call = request.tool_call
        if call["name"] == "add_document":
            ok = approve(call["name"], call["args"])
            events.append({"guardrail": "approval", "tool": call["name"], "args": call["args"], "approved": ok})
            if not ok:
                return ToolMessage(
                    content="The user did not approve adding this document. Do not retry; answer without it.",
                    tool_call_id=call["id"], name=call["name"],
                )
        return await handler(request)

    return require_approval


# --------------------------------------------------------------------------- guardrail 3: citations

def citation_problems(answer: str, tool_outputs: list[str], sources: set[str]) -> list[str]:
    """What is wrong with the answer's citations, as instructions to the model."""
    if retrieval.is_refusal(answer):
        return []
    retrieved = retrieval.retrieved_citations(tool_outputs)
    sources = set(sources) | {src for src, _ in retrieved}   # includes documents added since startup
    cites = retrieval.cited(answer, sources)
    problems = []
    if not retrieved:
        problems.append("You answered without any search results. Search first, or start with the refusal sentence.")
    elif not cites:
        problems.append("Your answer has no citations. Cite every claim as [<law>, <location>] from the CITE AS lines.")
    bad = [f"[{s}, {l}]" for s, l in cites if not retrieval.citation_valid((s, l), retrieved)]
    if bad:
        problems.append("These citations are not in your search results: " + ", ".join(bad)
                        + ". Cite only passages you retrieved, or search for them.")
    return problems


# --------------------------------------------------------------------------- harness

def text_of(message) -> str:
    content = message.content
    if isinstance(content, list):
        return "".join(p.get("text", "") if isinstance(p, dict) else str(p) for p in content)
    return content or ""


class Harness:
    """`async with Harness() as h: result = await h.ask("...")`"""

    def __init__(self, approve: Callable[[str, dict], bool] = console_approval):
        self.approve = approve

    async def __aenter__(self):
        load_api_key()
        params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT))
        self._stdio = stdio_client(params)
        read, write = await self._stdio.__aenter__()
        self._session_cm = ClientSession(read, write)
        self.session = await self._session_cm.__aenter__()
        await self.session.initialize()
        mcp_tools = (await self.session.list_tools()).tools
        self.tools = [mcp_to_langchain(self.session, t) for t in mcp_tools]
        self.sources = retrieval.known_sources()
        self.models = [ChatGoogleGenerativeAI(model=m, max_retries=2) for m in MODELS]
        return self

    async def __aexit__(self, *exc):
        await self._session_cm.__aexit__(*exc)
        await self._stdio.__aexit__(*exc)

    def _agent(self, events: list):
        return create_agent(
            self.models[0],
            tools=self.tools,
            system_prompt=SYSTEM_PROMPT,
            middleware=[
                approval_middleware(self.approve, events),
                ToolCallLimitMiddleware(run_limit=MAX_TOOL_CALLS, exit_behavior="continue"),
                ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS, exit_behavior="end"),
                ModelFallbackMiddleware(*self.models[1:]),
            ],
        )

    async def ask(self, question: str) -> dict:
        started = time.time()
        events: list = []
        agent = self._agent(events)
        messages = [HumanMessage(question)]
        trace: list[dict] = []
        tokens = {"input": 0, "output": 0, "total": 0}
        answer = ""

        for attempt in range(2):     # first try + one guardrail retry
            state = await agent.ainvoke({"messages": messages})
            new = state["messages"][len(messages):]
            messages = state["messages"]
            for m in new:
                if isinstance(m, AIMessage):
                    u = m.usage_metadata or {}
                    tokens["input"] += u.get("input_tokens", 0)
                    tokens["output"] += u.get("output_tokens", 0)
                    tokens["total"] += u.get("total_tokens", 0)
                    for tc in m.tool_calls:
                        trace.append({"tool": tc["name"], "args": tc["args"]})
                elif isinstance(m, ToolMessage):
                    trace.append({"tool_result": m.name, "text": text_of(m)})
            answer = text_of(messages[-1]).strip() if isinstance(messages[-1], AIMessage) else ""
            tool_outputs = [t["text"] for t in trace if t.get("tool_result") == "search"]
            problems = citation_problems(answer, tool_outputs, self.sources) if answer else ["You gave no answer."]
            if not problems:
                break
            events.append({"guardrail": "citations", "attempt": attempt + 1, "problems": problems, "answer": answer})
            if attempt == 0:
                messages = messages + [HumanMessage(
                    "Citation check failed: " + " ".join(problems) + " Rewrite your answer following the rules.")]
            else:
                answer = (f"{retrieval.REFUSAL} (A draft answer was withheld because its citations "
                          f"could not be verified against the retrieved passages.)")
                events.append({"guardrail": "citations", "action": "replaced answer with refusal"})

        return {
            "question": question,
            "answer": answer,
            "trace": trace,
            "retrieved": retrieval.retrieved_citations([t["text"] for t in trace if t.get("tool_result") == "search"]),
            "guardrail_events": events,
            "tokens": tokens,
            "seconds": round(time.time() - started, 2),
        }


def run_agent(question: str, approve: Callable[[str, dict], bool] = console_approval) -> dict:
    """Answer one question (starts and stops the MCP server)."""
    async def go():
        async with Harness(approve) as h:
            return await h.ask(question)
    return asyncio.run(go())


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit('usage: python agent.py "your question"')
    result = run_agent(" ".join(sys.argv[1:]))
    print(result["answer"])
    if result["retrieved"]:
        print("\nSources retrieved:")
        for s, l in dict.fromkeys(result["retrieved"]):
            print(f"  - {s}, {l}")
    for e in result["guardrail_events"]:
        print(f"[guardrail] {e}", file=sys.stderr)
    print(f"\n({result['tokens']['total']} tokens, {result['seconds']}s)", file=sys.stderr)
