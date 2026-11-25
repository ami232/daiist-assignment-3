"""
Assignment 3: the agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the tools from server.py over MCP and
AGENTS.md as the system prompt.

Guardrails:
  1. approval  add_document only runs after a yes from the user (stdin), or from an
               explicit approver function passed in by code. No terminal -> refused.
  2. limits    at most 6 tool calls and 8 model calls per question.
  3. citations (answers about the law; not add_document reports) every [chunk-id] in the answer must be one the search tool returned
               in this run. If not, the model gets one retry with the problem
               spelled out; if it still fails, the answer is withheld and replaced
               by a refusal. An answer with no citation at all that is not a
               refusal is treated the same way.

`run(question)` returns the answer, citations, tool trace, tokens and seconds,
for evaluate.py.
"""

from __future__ import annotations

import asyncio
import os
import re
import sys
import time
from pathlib import Path
from typing import Callable

from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware, ToolCallLimitMiddleware, wrap_tool_call
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.tools import StructuredTool
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from pydantic import create_model

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
MODEL = "gemini-3.5-flash-lite"   # fast; the judge in evaluate.py had to use the same model (quota)
REFUSAL = "The corpus does not cover this."
CITATION = re.compile(r"\b([a-z0-9]+-(?:article|fixed)-\d{4})\b")   # ids anywhere, also several in one bracket
ID_IN_RESULTS = re.compile(r"^\[([a-z0-9]+-(?:article|fixed)-\d{4})\] (.+?) \(similarity", re.M)
SYSTEM_PROMPT = (ROOT / "AGENTS.md").read_text(encoding="utf-8")


def ask_on_terminal(args: dict) -> bool:
    if not sys.stdin.isatty():
        return False
    answer = input(f"\nThe agent wants to add {args.get('path')!r} to the index. Approve? [y/N] ")
    return answer.strip().lower() in {"y", "yes"}


def approval_middleware(approver: Callable[[dict], bool]):
    @wrap_tool_call
    async def require_approval(request, handler):
        call = request.tool_call
        if call["name"] == "add_document" and not approver(call["args"]):
            return ToolMessage(
                content="Not approved by the user. The document was NOT added. Tell the user.",
                tool_call_id=call["id"], name=call["name"], status="error",
            )
        return await handler(request)
    return require_approval


def text_of(message) -> str:
    c = message.content
    if isinstance(c, str):
        return c
    return "".join(p.get("text", "") if isinstance(p, dict) else str(p) for p in c)


def is_refusal(answer: str) -> bool:
    """Full or partial refusal: the answer says the corpus does not cover (part of) the question."""
    a = answer.lower()
    return any(f"corpus does not {v}" in a for v in ("cover", "state", "say", "specify", "contain", "set"))


def as_langchain_tool(session: ClientSession, tool) -> StructuredTool:
    """Wrap one MCP tool (name, description, string arguments) as a LangChain tool."""
    props = (tool.input_schema or {}).get("properties", {})
    required = set((tool.input_schema or {}).get("required", []))
    fields = {name: (str, ...) if name in required else (str | None, None) for name in props}
    schema = create_model(f"{tool.name}_args", **fields)

    async def call(**kwargs) -> str:
        result = await session.call_tool(tool.name, {k: v for k, v in kwargs.items() if v is not None})
        return "\n".join(getattr(c, "text", "") for c in result.content)

    return StructuredTool(name=tool.name, description=tool.description or "", args_schema=schema, coroutine=call)


async def _run(question: str, approver: Callable[[dict], bool]) -> dict:
    params = StdioServerParameters(command=sys.executable, args=[str(ROOT / "server.py")], cwd=str(ROOT), env=dict(os.environ))
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = [as_langchain_tool(session, t) for t in (await session.list_tools()).tools]
            return await _run_agent(question, approver, tools)


async def _run_agent(question: str, approver: Callable[[dict], bool], tools: list) -> dict:
    model = ChatGoogleGenerativeAI(model=MODEL, api_key=load_api_key())
    agent = create_agent(
        model=model, tools=tools, system_prompt=SYSTEM_PROMPT,
        middleware=[
            approval_middleware(approver),
            ToolCallLimitMiddleware(run_limit=6, exit_behavior="end"),
            ModelCallLimitMiddleware(run_limit=8, exit_behavior="end"),
        ],
    )
    started = time.time()
    messages = [HumanMessage(question)]
    guardrail = None
    first_answer = None
    for attempt in range(2):
        state = await agent.ainvoke({"messages": messages})
        messages = state["messages"]
        answer = text_of(messages[-1]) if isinstance(messages[-1], AIMessage) else ""
        retrieved = {}
        for m in messages:
            if isinstance(m, ToolMessage) and m.name == "search":
                for cid, loc in ID_IN_RESULTS.findall(text_of(m)):
                    retrieved[cid] = loc
        cited = list(dict.fromkeys(CITATION.findall(answer)))
        bad = [c for c in cited if c not in retrieved]
        problem = None
        admin = any(isinstance(m, AIMessage) and any(tc["name"] == "add_document" for tc in m.tool_calls) for m in messages)
        if admin:
            break                      # reporting an add_document result, not answering about the law
        if bad:
            problem = f"cited ids not returned by search: {', '.join(bad)}"
        elif not cited and not is_refusal(answer):
            problem = "no citation and not a refusal"
        if not problem:
            break
        guardrail = problem
        if attempt == 0:
            first_answer = answer
            messages = messages + [HumanMessage(
                f"Citation check failed ({problem}). Rewrite your answer citing only chunk ids that the "
                f"search tool returned, or reply '{REFUSAL}' if the passages do not support it.")]
        else:
            answer = f"{REFUSAL} (Answer withheld: its citations could not be verified.)"
            cited = []
    tokens = {"input": 0, "output": 0}
    for m in messages:
        u = getattr(m, "usage_metadata", None) or {}
        tokens["input"] += u.get("input_tokens", 0)
        tokens["output"] += u.get("output_tokens", 0)
    trace = [{"tool": tc["name"], "args": tc["args"]} for m in messages if isinstance(m, AIMessage) for tc in m.tool_calls]
    return {
        "question": question, "answer": answer, "refusal": is_refusal(answer),
        "citations": {c: retrieved.get(c, "?") for c in cited}, "retrieved": retrieved,
        "trace": trace, "guardrail": guardrail, "first_answer": first_answer, "tokens": tokens,
        "seconds": round(time.time() - started, 1),
    }


def run(question: str, approver: Callable[[dict], bool] = ask_on_terminal) -> dict:
    return asyncio.run(_run(question, approver))


def main() -> None:
    question = " ".join(sys.argv[1:]).strip()
    if not question:
        raise SystemExit('usage: python agent.py "your question"')
    r = run(question)
    print(r["answer"])
    if r["citations"]:
        print("\nSources:")
        for cid, loc in r["citations"].items():
            print(f"  [{cid}] {loc}")
    if r["guardrail"]:
        print(f"\n(citation guardrail fired: {r['guardrail']})")
    print(f"\n{len(r['trace'])} tool call(s), {r['tokens']['input']} in / {r['tokens']['output']} out tokens, {r['seconds']}s")


if __name__ == "__main__":
    main()
