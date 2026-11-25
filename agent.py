"""
Assignment 3: the agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the tools of server.py reached over MCP
(stdio) and AGENTS.md as system prompt.

Guardrails
    approval    add_document runs only after a human types "y" (HumanInTheLoopMiddleware);
                without an interactive terminal (evaluation) it is rejected.
    call limit  at most 6 tool calls per question (ToolCallLimitMiddleware).
    citations   after the answer, code checks that every [Source, Article ...] citation was
                returned by a search in this run and that a non-refusal cites something.
                If not, the agent gets one chance to fix it; if it still fails, the answer
                is printed with a warning.

`answer(question)` returns the answer plus the tool trace for evaluate.py.
"""

from __future__ import annotations

import asyncio
import re
import sys
import time
import uuid
from contextlib import AsyncExitStack
from pathlib import Path

import truststore

truststore.inject_into_ssl()

from langchain.agents import create_agent  # noqa: E402
from langchain.agents.middleware import (  # noqa: E402
    HumanInTheLoopMiddleware,
    ModelFallbackMiddleware,
    ToolCallLimitMiddleware,
)
from langchain_core.tools import StructuredTool  # noqa: E402
from langchain_google_genai import ChatGoogleGenerativeAI  # noqa: E402
from langgraph.checkpoint.memory import InMemorySaver  # noqa: E402
from langgraph.types import Command  # noqa: E402
from mcp import ClientSession, StdioServerParameters  # noqa: E402
from mcp.client.stdio import stdio_client  # noqa: E402

from api_key import load_api_key  # noqa: E402

ROOT = Path(__file__).resolve().parent
MODEL = "gemini-3.8-flash"
FALLBACK_MODEL = "gemini-3.5-flash-lite"  # used only when MODEL is overloaded (503/504) after retries
MAX_TOOL_CALLS = 6
REFUSAL = "The corpus does not cover this question."

# Article 395(1), Article 5(4)(a), Article 141(1)-(5); the nested form was missed until q20 (see REPORT.md)
CITATION = re.compile(r"\[([^\[\],]+?),\s*(Article\s+[0-9]+[a-z]*(?:\([0-9a-z]+\))*(?:-\([0-9a-z]+\))?)\]")
RETURNED = re.compile(r"cite as \[([^\[\],]+?),\s*([^\]]+)\]")


# --------------------------------------------------------------------------- citations guardrail

def _article(location: str) -> str:
    """'Article 395(1)-(2)' -> 'Article 395'."""
    m = re.match(r"Article\s+[0-9]+[a-z]*", location.strip())
    return m.group(0) if m else location.strip()


def check_citations(answer: str, tool_outputs: list[str]) -> dict:
    """Which citations in the answer were not returned by search in this run."""
    returned = set()
    for out in tool_outputs:
        for src, loc in RETURNED.findall(out):
            for part in re.split(r"\s+to\s+", loc):
                returned.add((src.strip(), _article(part)))
    cited = [(s.strip(), loc) for s, loc in CITATION.findall(answer)]
    invalid = [f"[{s}, {loc}]" for s, loc in cited if (s, _article(loc)) not in returned]
    refusal = REFUSAL.lower() in answer.lower()
    return {
        "cited": [f"[{s}, {loc}]" for s, loc in cited],
        "invalid": invalid,
        "refusal": refusal,
        "uncited": not refusal and not cited,
        "ok": not invalid and (refusal or bool(cited)),
    }


# --------------------------------------------------------------------------- approval

def ask_human(action: dict) -> bool:
    args = action.get("args", {})
    print(f"\nThe agent wants to run {action.get('name')} with {args}.", file=sys.stderr)
    if not sys.stdin or not sys.stdin.isatty():
        print("No interactive terminal: rejected.", file=sys.stderr)
        return False
    return input("Approve? [y/N] ").strip().lower() in ("y", "yes")


# --------------------------------------------------------------------------- MCP tools

async def mcp_tools(stack: AsyncExitStack) -> list[StructuredTool]:
    params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT))
    read, write = await stack.enter_async_context(stdio_client(params))
    session = await stack.enter_async_context(ClientSession(read, write))
    await session.initialize()

    tools = []
    for spec in (await session.list_tools()).tools:
        async def call(_name=spec.name, **kwargs) -> str:
            result = await session.call_tool(_name, kwargs)
            return "\n".join(getattr(c, "text", "") for c in result.content)

        tools.append(StructuredTool(
            name=spec.name, description=spec.description or "",
            args_schema=spec.input_schema, coroutine=call,
        ))
    return tools


def _text(message) -> str:
    content = message.content
    if isinstance(content, list):
        return "".join(p.get("text", "") if isinstance(p, dict) else str(p) for p in content)
    return content or ""


# --------------------------------------------------------------------------- agent

async def answer_async(question: str, approve=ask_human, verbose: bool = False) -> dict:
    load_api_key()
    started = time.time()
    system_prompt = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    async with AsyncExitStack() as stack:
        tools = await mcp_tools(stack)
        agent = create_agent(
            ChatGoogleGenerativeAI(model=MODEL, temperature=0, max_retries=2, timeout=90),
            tools,
            system_prompt=system_prompt,
            middleware=[
                ModelFallbackMiddleware(
                    ChatGoogleGenerativeAI(model=FALLBACK_MODEL, temperature=0, max_retries=4, timeout=90)),
                HumanInTheLoopMiddleware(interrupt_on={"add_document": True}),
                ToolCallLimitMiddleware(run_limit=MAX_TOOL_CALLS, exit_behavior="continue"),
            ],
            checkpointer=InMemorySaver(),
        )
        config = {"configurable": {"thread_id": str(uuid.uuid4())}}

        async def run(payload):
            state = await agent.ainvoke(payload, config)
            while state.get("__interrupt__"):
                decisions = []
                for interrupt in state["__interrupt__"]:
                    for action in interrupt.value.get("action_requests", []):
                        ok = approve(action)
                        decisions.append({"type": "approve"} if ok else
                                         {"type": "reject", "message": "The user did not approve adding this document."})
                state = await agent.ainvoke(Command(resume={"decisions": decisions}), config)
            return state

        state = await run({"messages": [{"role": "user", "content": question}]})
        guardrail_fired = False
        check = _check(state)
        if not check["ok"]:
            guardrail_fired = True
            problem = (f"These citations were not returned by search: {', '.join(check['invalid'])}. "
                       if check["invalid"] else "Your answer has no citation. ")
            state = await run({"messages": [{"role": "user", "content":
                problem + "Rewrite the answer citing only passages returned by search in this conversation, "
                          f"or reply '{REFUSAL}' if they do not support it."}]})
            check = _check(state)

    messages = state["messages"]
    final = _text(messages[-1]).strip()
    if not check["ok"]:
        final += ("\n\n[Warning: citation check failed"
                  + (f" ({', '.join(check['invalid'])} not in the search results)" if check["invalid"] else
                     " (no citations)") + ". Verify before relying on this answer.]")
    trace, tokens, models = [], {"input": 0, "output": 0}, set()
    for m in messages:
        if m.type == "ai":
            models.add((getattr(m, "response_metadata", None) or {}).get("model_name") or "?")
        for call in getattr(m, "tool_calls", None) or []:
            trace.append({"tool": call["name"], "args": call["args"]})
        if m.type == "tool":
            trace.append({"tool_result": _text(m)})
        usage = getattr(m, "usage_metadata", None)
        if usage:
            tokens["input"] += usage.get("input_tokens", 0)
            tokens["output"] += usage.get("output_tokens", 0)
    return {
        "question": question, "answer": final, "trace": trace,
        "retrieved": [t["tool_result"] for t in trace if "tool_result" in t],
        "citations": check, "guardrail_fired": guardrail_fired,
        "tokens": tokens, "seconds": round(time.time() - started, 1),
        "models": sorted(models), "fallback_used": any(FALLBACK_MODEL in m for m in models),
    }


def _check(state) -> dict:
    messages = state["messages"]
    outputs = [_text(m) for m in messages if m.type == "tool"]
    result = check_citations(_text(messages[-1]), outputs)
    # A turn that only adds a document reports the tool result; there is nothing to cite.
    # (Found in the add_document demo: the check forced a refusal after a successful add.)
    tools = {m.name for m in messages if m.type == "tool"}
    if "add_document" in tools and "search" not in tools and not result["invalid"]:
        result.update(ok=True, uncited=False, skipped="add_document turn")
    return result


def answer(question: str, approve=ask_human) -> dict:
    return asyncio.run(answer_async(question, approve))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit('usage: python agent.py "your question"')
    result = answer(" ".join(sys.argv[1:]))
    print(result["answer"])
    searches = [t["args"].get("query") for t in result["trace"] if t.get("tool") == "search"]
    print(f"\n(searches: {searches}; tokens in/out: {result['tokens']['input']}/{result['tokens']['output']}; "
          f"{result['seconds']}s" + ("; citation guardrail fired" if result["guardrail_fired"] else "") + ")")
