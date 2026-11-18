"""
Assignment 3: the agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the tools of server.py over MCP and
AGENTS.md as system prompt.

Guardrails:
  1. Approval: add_document is interrupted (HumanInTheLoopMiddleware) and runs only
     if a human types "y". With no terminal attached (evaluation, CI) it is rejected.
  2. Call limits: at most 8 model calls and 4 searches per question, so a confused
     agent can't loop and burn the free quota.
  3. Citation check (extra guardrail): every [SOURCE, location] label in the answer
     must match a passage the search tool actually returned in this run. An answer
     with an invented citation, or a non-refusal answer with no citation at all, is
     sent back once to be fixed; if it still fails it is replaced by a refusal.

`answer(question)` returns the answer plus the tool trace, for evaluate.py.
"""

from __future__ import annotations

import asyncio
import os
import re
import sys
import time
import warnings
from contextlib import AsyncExitStack
from pathlib import Path

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
warnings.filterwarnings("ignore", message=".*fixed sampling defaults.*")
CHAT_MODEL = os.environ.get("CHAT_MODEL", "gemini-3.5-flash-lite")
FALLBACK_MODEL = "gemini-flash-lite-latest"  # used only if CHAT_MODEL is overloaded (503) or times out
SYSTEM_PROMPT = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
REFUSAL = "No encuentro la respuesta en las leyes del corpus (LAU, LDV, LPH)."
CITE_RE = re.compile(r"\[((?:LAU|LDV|LPH|BOE-[A-Z]-\d{4}-\d+|[\w.-]+)),\s*([^\]]+?)\]")
LABEL_RE = re.compile(r"Cite as: \[([^\]]+)\]")


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


def is_refusal(text: str) -> bool:
    return text.strip().startswith(REFUSAL[:40])


def citations_in(text: str) -> list[str]:
    return [f"{s}, {re.sub(r'\s*\(parte \d+/\d+\)', '', loc).strip()}" for s, loc in CITE_RE.findall(text)]


def check_citations(answer: str, retrieved: set[str]) -> tuple[bool, str]:
    """Return (ok, reason). ok=False means the guardrail fires."""
    cited = citations_in(answer)
    if is_refusal(answer) and not cited:
        return True, "refusal"
    if not cited:
        return False, "the answer makes claims but cites nothing"
    invalid = [c for c in cited if c not in retrieved]
    if invalid:
        return False, f"cites passages that were not retrieved: {invalid}"
    return True, "all citations retrieved"


def _text(message) -> str:
    content = message.content
    if isinstance(content, list):
        return "".join(p.get("text", "") if isinstance(p, dict) else str(p) for p in content)
    return str(content)


def _mcp_tool(session: ClientSession, tool) -> StructuredTool:
    """Wrap one MCP tool as a LangChain tool that calls the server over the open session.

    (langchain-mcp-adapters doesn't support mcp 2.x yet, hence this small bridge.)
    """
    async def call(**kwargs) -> str:
        result = await session.call_tool(tool.name, kwargs)
        return "\n".join(getattr(c, "text", "") for c in result.content)

    return StructuredTool.from_function(coroutine=call, name=tool.name, description=tool.description,
                                        args_schema=tool.input_schema)


async def open_tools(stack: AsyncExitStack) -> list[StructuredTool]:
    """Start server.py over stdio (as an editor would) and return its tools."""
    params = StdioServerParameters(command=sys.executable, args=[str(ROOT / "server.py")], cwd=str(ROOT))
    read, write = await stack.enter_async_context(stdio_client(params))
    session = await stack.enter_async_context(ClientSession(read, write))
    await session.initialize()
    return [_mcp_tool(session, t) for t in (await session.list_tools()).tools]


async def build_agent(stack: AsyncExitStack):
    load_api_key()
    tools = await open_tools(stack)
    model = ChatGoogleGenerativeAI(model=CHAT_MODEL, temperature=0, timeout=60, max_retries=2)
    fallback = ChatGoogleGenerativeAI(model=FALLBACK_MODEL, temperature=0, timeout=60, max_retries=2)
    agent = create_agent(
        model=model,
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
        middleware=[
            ModelFallbackMiddleware(fallback),
            HumanInTheLoopMiddleware(interrupt_on={"add_document": True, "search": False}),
            ModelCallLimitMiddleware(run_limit=8, exit_behavior="end"),
            ToolCallLimitMiddleware(tool_name="search", run_limit=4, exit_behavior="continue"),
        ],
        checkpointer=InMemorySaver(),
    )
    return agent


def _approve(action: dict, interactive: bool) -> dict:
    if not interactive:
        log(f"[approval] {action['name']}({action['args']}) rejected: no human at the terminal.")
        return {"type": "reject", "message": "The user did not approve adding this document."}
    print(f"\nThe agent wants to run {action['name']} with {action['args']}.", file=sys.stderr)
    reply = input("Approve? [y/N] ").strip().lower()
    if reply in ("y", "yes", "s", "si", "sí"):
        return {"type": "approve"}
    return {"type": "reject", "message": "The user rejected adding this document."}


async def _run(agent, messages, config, interactive) -> dict:
    result = await agent.ainvoke({"messages": messages}, config)
    while result.get("__interrupt__"):
        decisions = [_approve(a, interactive) for i in result["__interrupt__"] for a in i.value["action_requests"]]
        result = await agent.ainvoke(Command(resume={"decisions": decisions}), config)
    return result


async def answer_async(question: str, agent=None, interactive: bool | None = None) -> dict:
    """Answer one question. Returns answer, citations, trace, guardrail info, tokens and seconds."""
    if interactive is None:
        interactive = sys.stdin.isatty()
    if agent is None:  # standalone call: open the server just for this question
        async with AsyncExitStack() as stack:
            return await answer_async(question, await build_agent(stack), interactive)
    config = {"configurable": {"thread_id": f"q-{time.time_ns()}"}}
    started = time.time()

    result = await _run(agent, [HumanMessage(question)], config, interactive)
    messages = result["messages"]

    # tool trace and the labels of every passage actually retrieved
    calls = {}
    trace, retrieved = [], set()
    for m in messages:
        if isinstance(m, AIMessage):
            for tc in m.tool_calls:
                calls[tc["id"]] = tc
        if isinstance(m, ToolMessage):
            out = _text(m)
            tc = calls.get(m.tool_call_id, {})
            trace.append({"tool": tc.get("name", m.name), "args": tc.get("args", {}), "output": out})
            retrieved.update(LABEL_RE.findall(out))
    final = _text(messages[-1]) if isinstance(messages[-1], AIMessage) else ""

    # guardrail: citation check, one repair attempt, then refuse.
    # Skipped for add_document requests: "added / not approved" is a status report, not a legal claim.
    operation = any(t["tool"] == "add_document" for t in trace)
    ok, reason = (True, "add_document request") if operation else check_citations(final, retrieved)
    guardrail = None
    if not ok:
        guardrail = {"first_answer": final, "reason": reason}
        log(f"[guardrail] citation check failed ({reason}); asking for one repair.")
        valid = ", ".join(f"[{r}]" for r in sorted(retrieved)) or "(none)"
        repair = (f"Your answer failed the citation check: {reason}. Rewrite it citing only these labels, "
                  f"exactly as written: {valid}. Remove any claim they don't support. If they don't "
                  f"answer the question, reply starting with: {REFUSAL}")
        result = await _run(agent, [HumanMessage(repair)], config, interactive)
        messages = result["messages"]
        final = _text(messages[-1])
        ok, reason = check_citations(final, retrieved)
        guardrail["repaired"] = ok
        if not ok:
            log(f"[guardrail] still failing ({reason}); replacing the answer with a refusal.")
            final = (f"{REFUSAL} No he podido respaldar una respuesta con citas verificables; "
                     f"consulta el texto en el BOE o a un abogado.")

    tokens = {"input": 0, "output": 0}
    for m in messages:
        usage = getattr(m, "usage_metadata", None) or {}
        tokens["input"] += usage.get("input_tokens", 0)
        tokens["output"] += usage.get("output_tokens", 0)

    return {
        "question": question,
        "answer": final,
        "citations": citations_in(final),
        "retrieved": sorted(retrieved),
        "refused": is_refusal(final),
        "trace": trace,
        "guardrail": guardrail,
        "tokens": tokens,
        "seconds": round(time.time() - started, 1),
    }


def answer(question: str, interactive: bool | None = None) -> dict:
    return asyncio.run(answer_async(question, interactive=interactive))


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit('usage: python agent.py "your question"')
    question = " ".join(sys.argv[1:])
    r = answer(question)
    print(r["answer"])
    if r["citations"]:
        print("\nFuentes:")
        labels = dict.fromkeys(r["citations"])
        for c in labels:
            src = c.split(",")[0]
            url = {"LAU": "BOE-A-1994-26003", "LDV": "BOE-A-2023-12203", "LPH": "BOE-A-1960-10906"}.get(src)
            print(f"  [{c}]" + (f"  https://www.boe.es/buscar/act.php?id={url}" if url else ""))
    log(f"\n({len(r['trace'])} tool calls, {r['tokens']['input']}+{r['tokens']['output']} tokens, {r['seconds']}s"
        + (f", citation guardrail fired: {r['guardrail']['reason']}" if r["guardrail"] else "") + ")")


if __name__ == "__main__":
    main()
