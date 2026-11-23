"""
Assignment 3: the agent harness (`uv run python main.py ask "question"`).

LangChain `create_agent` on Gemini, with the two tools from server.py over MCP
(stdio) and AGENTS.md as the system prompt.

Guardrails
- Approval: add_document only runs after a human types "y". With no terminal
  (evaluation, CI) it is denied.
- Call limits: at most 6 tool calls and 8 model calls per question.
- Citation check (our extra guardrail): every [DOC p.N] tag in the answer must
  point to a page range that a search in THIS run actually returned, and a
  non-refusal answer must cite at least once. If the check fails, the model gets
  one chance to fix it; if it still fails, the answer is withheld and replaced
  by a notice, so an unverifiable claim never reaches the analyst.

`answer(question)` returns the answer plus the tool trace, tokens and timing,
for evaluate.py.
"""

from __future__ import annotations

import asyncio
import os
import sys
import time
import warnings

warnings.filterwarnings("ignore")  # google-genai / pydantic deprecation noise on every call
from pathlib import Path
from typing import Callable

from langchain.agents import create_agent
from langchain.agents.middleware import (ModelCallLimitMiddleware, ModelFallbackMiddleware,
                                         ModelRetryMiddleware, ToolCallLimitMiddleware)
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.tools import StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from pydantic import BaseModel, Field

from api_key import load_api_key
from index import parse_citations

ROOT = Path(__file__).resolve().parent
MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash")
# Free-tier Gemini often answers 503 "high demand": retry with backoff, then fall back to these.
FALLBACK_MODELS = [m for m in os.environ.get("GEMINI_FALLBACKS", "gemini-3.5-flash-lite,gemini-3.1-flash-lite").split(",") if m]
SYSTEM_PROMPT = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
REFUSAL = "The reports in the corpus do not cover this"
MAX_TOOL_CALLS = 6
MAX_MODEL_CALLS = 8


def is_refusal(text: str) -> bool:
    return REFUSAL.lower() in text.lower()


def ask_terminal(path: str) -> bool:
    """Default approval: ask on the terminal; deny if nobody is there to answer."""
    if not sys.stdin.isatty():
        print(f"[approval] add_document({path!r}) denied: no terminal to ask for approval.", file=sys.stderr)
        return False
    reply = input(f"\nThe agent wants to add {path!r} to the index (spends embedding quota). Approve? [y/N] ")
    return reply.strip().lower() in ("y", "yes")


class SearchArgs(BaseModel):
    query: str = Field(description="What to look for: the question or its key terms.")


class AddArgs(BaseModel):
    path: str = Field(description="Local path of the PDF report to add.")


def _text(result) -> str:
    return "\n".join(getattr(c, "text", "") for c in result.content).strip()


def check_citations(answer: str, trace: list[dict]) -> list[str]:
    """Return the problems with the answer's citations (empty list = passes)."""
    retrieved = []
    for step in trace:
        if step["tool"] == "search":
            retrieved += parse_citations(step["result"])
    problems = []
    cites = parse_citations(answer)
    if not cites and not is_refusal(answer):
        problems.append("the answer makes claims but cites no passage")
    for doc, a, b in cites:
        if not any(doc == d and a <= rb and b >= ra for d, ra, rb in retrieved):
            problems.append(f"[{doc} p.{a}{'-' + str(b) if b != a else ''}] was not in any passage returned by search")
    return problems


def _usage(messages) -> dict:
    tin = tout = 0
    for m in messages:
        u = getattr(m, "usage_metadata", None) or {}
        tin += u.get("input_tokens", 0)
        tout += u.get("output_tokens", 0)
    return {"input_tokens": tin, "output_tokens": tout}


def _final_text(messages) -> str:
    for m in reversed(messages):
        if isinstance(m, AIMessage) and not m.tool_calls:
            c = m.content
            if isinstance(c, list):
                c = "".join(p.get("text", "") if isinstance(p, dict) else str(p) for p in c)
            if c.strip():
                return c.strip()
    return ""


async def answer_async(question: str, approve: Callable[[str], bool] = ask_terminal,
                       env: dict | None = None) -> dict:
    load_api_key()
    started = time.time()
    trace: list[dict] = []
    params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT),
                                   env={**os.environ, **(env or {})})
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            async def search(query: str) -> str:
                text = _text(await session.call_tool("search", {"query": query}))
                trace.append({"tool": "search", "args": {"query": query}, "result": text})
                return text

            async def add_document(path: str) -> str:
                if not approve(path):
                    trace.append({"tool": "add_document", "args": {"path": path}, "result": "DENIED"})
                    return "Not run: the user did not approve adding this document. Tell the user it was not added."
                text = _text(await session.call_tool("add_document", {"path": path}))
                trace.append({"tool": "add_document", "args": {"path": path}, "result": text})
                return text

            descs = {t.name: t.description for t in (await session.list_tools()).tools}
            tools = [
                StructuredTool.from_function(coroutine=search, name="search", description=descs["search"], args_schema=SearchArgs),
                StructuredTool.from_function(coroutine=add_document, name="add_document",
                                             description=descs["add_document"], args_schema=AddArgs),
            ]
            def chat(name):
                return ChatGoogleGenerativeAI(model=name, temperature=0, max_retries=1)
            agent = create_agent(
                chat(MODEL), tools, system_prompt=SYSTEM_PROMPT,
                middleware=[ToolCallLimitMiddleware(run_limit=MAX_TOOL_CALLS),
                            ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS),
                            ModelFallbackMiddleware(*[chat(m) for m in FALLBACK_MODELS]),
                            ModelRetryMiddleware(max_retries=1, initial_delay=3, max_delay=10, on_failure="error")],
            )
            state = await agent.ainvoke({"messages": [HumanMessage(question)]})
            messages = state["messages"]
            text = _final_text(messages)

            guardrail = {"fired": False, "problems": [], "repaired": False}
            problems = check_citations(text, trace)
            if problems:
                guardrail.update(fired=True, problems=problems)
                fix = ("Citation check failed: " + "; ".join(problems) + ". Rewrite your answer so every factual "
                       "sentence ends with a tag copied exactly from a passage you retrieved (search again if needed). "
                       f"If the passages do not support an answer, say: \"{REFUSAL}.\"")
                state = await agent.ainvoke({"messages": messages + [HumanMessage(fix)]})
                messages = state["messages"]
                text = _final_text(messages)
                still = check_citations(text, trace)
                guardrail["repaired"] = not still
                if still:
                    text = ("[Answer withheld by the citation check: " + "; ".join(still) + ". "
                            "Verify this question directly in the reports.]")

    return {
        "question": question,
        "answer": text,
        "trace": trace,
        "refused": is_refusal(text),
        "guardrail": guardrail,
        "tool_calls": sum(1 for m in messages if isinstance(m, ToolMessage)),
        **_usage(messages),
        "seconds": round(time.time() - started, 1),
        "model": ",".join(sorted({(m.response_metadata or {}).get("model_name", MODEL)
                                  for m in messages if isinstance(m, AIMessage)})) or MODEL,
    }


def answer(question: str, approve: Callable[[str], bool] = ask_terminal, env: dict | None = None) -> dict:
    return asyncio.run(answer_async(question, approve, env))


def main() -> int:
    if len(sys.argv) < 2:
        print('usage: python agent.py "your question"', file=sys.stderr)
        return 2
    r = answer(" ".join(sys.argv[1:]))
    print(r["answer"])
    print("\nSources searched:")
    for step in r["trace"]:
        tags = sorted({f"[{d} p.{a}{'-' + str(b) if b != a else ''}]" for d, a, b in parse_citations(step["result"])})
        print(f"  {step['tool']}({next(iter(step['args'].values()))!r}) -> {' '.join(tags) or step['result'][:80]}")
    if r["guardrail"]["fired"]:
        print(f"\nCitation check fired: {r['guardrail']['problems']} (repaired: {r['guardrail']['repaired']})")
    print(f"\n({r['tool_calls']} tool calls, {r['input_tokens']}+{r['output_tokens']} tokens, {r['seconds']}s, {r['model']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
