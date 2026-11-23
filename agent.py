"""
Assignment 3: your agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the tools of server.py reached over MCP and
AGENTS.md as the system prompt.

Guardrails:
  1. Approval: add_document never runs without the user saying yes (`approve` callback;
     with no terminal the answer is no).
  2. Call limit: at most MAX_TOOL_CALLS tool calls per question (ToolCallLimitMiddleware).
  3. Citation guard (my own): an answer that cites an article the search never returned,
     or that gives an answer without any search, is withheld and replaced by the refusal.

`ask(question, approve=None)` returns a dict for evaluate.py:
  answer, tool_trace, retrieved (citations seen), refused, guardrail (what fired or None),
  withheld_answer, input_tokens, output_tokens, seconds.
"""

from __future__ import annotations

import asyncio
import os
import re
import sys
import time
from contextlib import AsyncExitStack
from pathlib import Path
from typing import Callable

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite")   #any Gemini chat model the key can use
MAX_TOOL_CALLS = 6
REFUSAL_PHRASE = "The indexed documents do not cover this."


def load_system_prompt() -> str:
    text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    return re.sub(r"<!--.*?-->", "", text, flags=re.S).strip()


#guardrails

CITATION_LINE = re.compile(r"^\[\d+\]\s+(.+?),\s+(Article\s+\d+)", re.M)
ARTICLE_REF = re.compile(r"Article\s+\d+")


def is_refusal(answer: str) -> bool:
    return REFUSAL_PHRASE.lower().rstrip(".") in answer.lower()


def retrieved_citations(trace: list[dict]) -> list[str]:
    """'GDPR, Article 33' for every passage returned by search."""
    out = []
    for step in trace:
        if step["tool"] == "search":
            out.extend(f"{s}, {a}" for s, a in CITATION_LINE.findall(step["result"]))
    return out


def citation_guard(answer: str, trace: list[dict]) -> str | None:
    """Return a reason if the answer must be withheld, else None."""
    if is_refusal(answer):
        return None
    if any(step["tool"] == "add_document" for step in trace):   # confirming an added document needs no citations
        return None
    searched = [s for s in trace if s["tool"] == "search"]
    if not searched:
        return "the answer was given without searching"
    seen_text = " ".join(s["result"] for s in searched)
    allowed = set(ARTICLE_REF.findall(seen_text))        # articles in the results (incl. cross-references)
    missing = sorted({a for a in ARTICLE_REF.findall(answer) if a not in allowed})
    if missing:
        return "the answer cites " + ", ".join(missing) + ", which the search did not return"
    if not ARTICLE_REF.search(answer):
        return "the answer cites no article"
    return None


#tools over MCP

def default_approve(path: str) -> bool:
    """Ask in the terminal; without a terminal (evaluation, pipes) the answer is no."""
    if not sys.stdin.isatty():
        return False
    return input(f"\nThe agent wants to add this document to the index: {path}\nAllow? [y/N] ").strip().lower() == "y"


async def open_tools(stack: AsyncExitStack, trace: list[dict], approve: Callable[[str], bool]):
    from langchain_core.tools import StructuredTool
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    params = StdioServerParameters(command=sys.executable, args=[str(ROOT / "server.py")],
                                   cwd=str(ROOT), env=dict(os.environ))
    read, write = await stack.enter_async_context(stdio_client(params))
    session = await stack.enter_async_context(ClientSession(read, write))
    await session.initialize()

    def wrap(tool):
        async def call(**kwargs) -> str:
            if tool.name == "add_document":
                path = str(kwargs.get("path", ""))
                if not await asyncio.to_thread(approve, path):
                    result = "DENIED: the user did not approve adding this document. Do not try again."
                    trace.append({"tool": tool.name, "args": kwargs, "result": result, "denied": True})
                    return result
            response = await session.call_tool(tool.name, kwargs)
            text = "\n".join(getattr(c, "text", "") for c in response.content)
            if getattr(response, "is_error", False) or getattr(response, "isError", False):
                text = "Tool error: " + text
            trace.append({"tool": tool.name, "args": kwargs, "result": text})
            return text

        return StructuredTool(name=tool.name, description=tool.description or "",
                              args_schema=tool.input_schema, coroutine=call)

    listing = await session.list_tools()
    return [wrap(t) for t in listing.tools]


#the agent

async def _ask(question: str, approve: Callable[[str], bool]) -> dict:
    from langchain.agents import create_agent
    from langchain.agents.middleware import ToolCallLimitMiddleware
    from langchain_google_genai import ChatGoogleGenerativeAI

    load_api_key()
    trace: list[dict] = []
    started = time.time()
    async with AsyncExitStack() as stack:
        tools = await open_tools(stack, trace, approve)
        agent = create_agent(
            ChatGoogleGenerativeAI(model=MODEL),
            tools,
            system_prompt=load_system_prompt(),
            middleware=[ToolCallLimitMiddleware(run_limit=MAX_TOOL_CALLS, exit_behavior="continue")],
        )
        state = await agent.ainvoke({"messages": [{"role": "user", "content": question}]})
    seconds = time.time() - started

    messages = state["messages"]
    answer = (messages[-1].text or "").strip() if hasattr(messages[-1], "text") else str(messages[-1].content)
    usage = [m.usage_metadata for m in messages if getattr(m, "usage_metadata", None)]
    result = {
        "question": question,
        "answer": answer,
        "tool_trace": trace,
        "retrieved": retrieved_citations(trace),
        "guardrail": None,
        "withheld_answer": None,
        "input_tokens": sum(u.get("input_tokens", 0) for u in usage),
        "output_tokens": sum(u.get("output_tokens", 0) for u in usage),
        "seconds": round(seconds, 1),
    }
    if not answer:
        result["answer"] = f"{REFUSAL_PHRASE} (The model returned no answer.)"
        result["guardrail"] = "empty answer"
    reason = citation_guard(result["answer"], trace)
    if reason:
        result["guardrail"] = reason
        result["withheld_answer"] = result["answer"]
        result["answer"] = f"{REFUSAL_PHRASE} (Answer withheld by the citation guard: {reason}.)"
    result["refused"] = is_refusal(result["answer"])
    return result


def ask(question: str, approve: Callable[[str], bool] | None = None) -> dict:
    """Run the agent on one question. `approve(path) -> bool` gates add_document."""
    return asyncio.run(_ask(question, approve or default_approve))


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit('usage: python agent.py "your question"')
    result = ask(" ".join(sys.argv[1:]))
    print(result["answer"])
    if result["retrieved"]:
        print("\nPassages retrieved: " + "; ".join(dict.fromkeys(result["retrieved"])))
    if result["guardrail"]:
        print(f"\n[guardrail fired: {result['guardrail']}]")
    print(f"\n[{len(result['tool_trace'])} tool calls, {result['input_tokens']} input / "
          f"{result['output_tokens']} output tokens, {result['seconds']}s, model {MODEL}]", file=sys.stderr)


if __name__ == "__main__":
    main()
