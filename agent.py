"""
Assignment 3: the corpus agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the tools of server.py over MCP and
AGENTS.md as system prompt.

Guardrails:
- approval: add_document only runs after a person types "y" (refused when
  nobody is at the terminal, e.g. during evaluation);
- call limits: at most MAX_MODEL_CALLS model calls and MAX_TOOL_CALLS tool
  calls per question;
- citation check: every [source | location] the answer cites must be a passage
  that search actually returned in this run, and an answer that is not a
  refusal must cite at least one. Otherwise the answer is withheld and replaced
  by the refusal, so an invented or mis-copied citation never reaches the team.

`ask(question)` returns the answer, the tool trace, tokens and seconds, for evaluate.py.
"""

import asyncio
import os
import re
import sys
import time
from pathlib import Path

from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware, ToolCallLimitMiddleware
from langchain_core.tools import StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from pydantic import Field, create_model

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
# Fast and on the free tier; the larger flash models were overloaded (503) when tested.
CHAT_MODEL = os.environ.get("CHAT_MODEL", "gemini-3.1-flash-lite")
MAX_MODEL_CALLS, MAX_TOOL_CALLS = 6, 4
REFUSAL = "The corpus does not cover this question."
CITATION = re.compile(r"\[([^\[\]|]+?)\s*\|\s*([^\[\]]+?)\]")
HEADER = re.compile(r"^\[\d+\] (.+?) \| (.+)$", re.M)


def system_prompt() -> str:
    return (ROOT / "AGENTS.md").read_text(encoding="utf-8")


def terminal_approval(tool: str, args: dict) -> bool:
    if not sys.stdin.isatty():
        return False
    reply = input(f"\nThe agent wants to run {tool} with {args}. Approve? [y/N] ")
    return reply.strip().lower() in ("y", "yes", "s", "si", "sí")


def langchain_tool(session: ClientSession, tool, approve=None) -> StructuredTool:
    """An MCP tool as a LangChain tool. With `approve`, it only runs after
    approve(name, args) says yes (the add_document approval step)."""
    props = (tool.input_schema or {}).get("properties", {})
    schema = create_model(f"{tool.name}_args",
                          **{name: (str, Field(description=p.get("description", name))) for name, p in props.items()})

    async def call(**kwargs):
        if approve is not None and not approve(tool.name, kwargs):
            return f"The user did not approve {tool.name}; nothing was added."
        result = await session.call_tool(tool.name, kwargs)
        return "\n".join(getattr(c, "text", "") for c in result.content)

    return StructuredTool.from_function(coroutine=call, name=tool.name,
                                        description=tool.description or "", args_schema=schema)


def text_of(content) -> str:
    if isinstance(content, str):
        return content
    return "".join(part.get("text", "") if isinstance(part, dict) else str(part) for part in content)


def check_citations(answer: str, retrieved: set[tuple[str, str]]) -> tuple[str, str | None]:
    """The citation guardrail. Returns (answer to show, why it fired or None)."""
    if answer.strip().startswith(REFUSAL):
        return answer, None
    cited = [(s.strip(), loc.strip()) for s, loc in CITATION.findall(answer)]
    if not cited:
        return REFUSAL, "the answer cited no passage"
    bad = [c for c in cited if c not in retrieved]
    if bad:
        return REFUSAL, f"cited passages search never returned: {bad}"
    return answer, None


async def ask_async(question: str, approve=terminal_approval) -> dict:
    load_api_key()
    started = time.time()
    # Pass our environment on: the MCP client's default one is minimal and
    # drops proxy and certificate settings the server needs to reach Gemini.
    params = StdioServerParameters(command=sys.executable, args=[str(ROOT / "server.py")], cwd=str(ROOT),
                                   env=dict(os.environ))
    async with stdio_client(params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()
        tools = [langchain_tool(session, t, approve if t.name == "add_document" else None)
                 for t in (await session.list_tools()).tools]
        agent = create_agent(
            ChatGoogleGenerativeAI(model=CHAT_MODEL, temperature=0, timeout=90, max_retries=3),
            tools=tools,
            system_prompt=system_prompt(),
            middleware=[ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS, exit_behavior="end"),
                        ToolCallLimitMiddleware(run_limit=MAX_TOOL_CALLS, exit_behavior="continue")],
        )
        result = await agent.ainvoke({"messages": [{"role": "user", "content": question}]})

    trace, retrieved, passages, tokens = [], set(), [], {"input": 0, "output": 0}
    for m in result["messages"]:
        usage = getattr(m, "usage_metadata", None) or {}
        tokens["input"] += usage.get("input_tokens", 0)
        tokens["output"] += usage.get("output_tokens", 0)
        for call in getattr(m, "tool_calls", None) or []:
            trace.append({"tool": call["name"], "args": call["args"]})
        if m.type == "tool":
            text = text_of(m.content)
            passages.append(text)
            retrieved |= {(s.strip(), loc.strip()) for s, loc in HEADER.findall(text)}
    raw = text_of(result["messages"][-1].content).strip() or REFUSAL
    answer, fired = check_citations(raw, retrieved)
    return {"question": question, "answer": answer, "raw_answer": raw, "guardrail": fired,
            "trace": trace, "retrieved": "\n\n".join(passages), "tokens": tokens,
            "seconds": round(time.time() - started, 1)}


def ask(question: str, approve=terminal_approval) -> dict:
    return asyncio.run(ask_async(question, approve))


if __name__ == "__main__":
    out = ask(" ".join(sys.argv[1:]))
    print(out["answer"])
    if out["guardrail"]:
        print(f"\n(guardrail: answer withheld because {out['guardrail']})")
    print(f"\n[{len(out['trace'])} tool call(s), {out['tokens']['input'] + out['tokens']['output']} tokens, "
          f"{out['seconds']} s]")
