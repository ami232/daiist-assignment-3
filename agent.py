"""
Assignment 3: your agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the tools of server.py loaded over MCP
and AGENTS.md as system prompt. Guardrails:

1. Approval: add_document only runs after a human says yes (a middleware
   around every tool call asks; anything but "y" means no).
2. Call limits: at most MAX_TOOL_CALLS tool calls and MAX_MODEL_CALLS model
   calls per question, so a confused agent cannot loop or burn quota.
3. Citation check (our extra guardrail): after the model answers, code checks
   that every "(Law, Article N)" it cites was actually returned by search in
   this run, and that a non-refusal answer cites at least one passage. If not,
   the answer is withheld and replaced by a refusal: a made-up or missing
   citation is exactly the confident wrong answer the user cannot spot.

evaluate.py uses ask_many(), which returns the answer and the tool trace.
"""

from __future__ import annotations

import asyncio
import re
import sys
import time
from pathlib import Path
from typing import Callable

from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware, ToolCallLimitMiddleware, wrap_tool_call
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.tools import StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
MODEL = "gemini-3.5-flash-lite"   # free tier: 3.5-flash allows only 20 requests/day; 3.8-flash timed out (Nov 2026)
MAX_TOOL_CALLS = 6
MAX_MODEL_CALLS = 8
REFUSAL = "The corpus does not cover this."

CITE_LINE = re.compile(r"Cite as: (.+?), ((?:Article|Recital|Annex|Page|Paragraph) [0-9IVXLC]+)")
KNOWN_SOURCES = ["AI Act", "GDPR", "DSA"]


def citation_pattern(sources: set[str]) -> re.Pattern:
    """Citations like "GDPR, Article 7" for the corpus laws and any source search returned (added documents)."""
    names = "|".join(re.escape(s) for s in sorted(set(KNOWN_SOURCES) | sources, key=len, reverse=True))
    return re.compile(rf"\b({names})\s*,\s*(Article|Recital|Annex|Page|Paragraph)s?\s+([0-9]+|[IVXLC]+)\b")


# --------------------------------------------------------------------------- tools over MCP

async def load_mcp_tools(session: ClientSession) -> list[StructuredTool]:
    """Wrap each tool of the MCP server as a LangChain tool that calls it over the session."""
    tools = []
    for tool in (await session.list_tools()).tools:
        async def call(_name: str = tool.name, **kwargs) -> str:
            result = await session.call_tool(_name, kwargs)
            return "\n".join(getattr(part, "text", "") for part in result.content)

        tools.append(StructuredTool.from_function(
            coroutine=call, name=tool.name, description=tool.description or "", args_schema=tool.input_schema,
        ))
    return tools


# --------------------------------------------------------------------------- guardrails

def ask_human(args: dict) -> bool:
    """Default approval: ask on the terminal. No terminal (e.g. a pipe) means no."""
    if not sys.stdin.isatty():
        print(f"[approval] add_document({args}) refused: no terminal to ask for approval.", file=sys.stderr)
        return False
    reply = input(f"\nThe agent wants to run add_document with {args}. Allow? [y/N] ")
    return reply.strip().lower() == "y"


def approval_middleware(approve: Callable[[dict], bool]):
    @wrap_tool_call
    async def require_approval(request, handler):
        call = request.tool_call
        if call["name"] == "add_document" and not approve(call["args"]):
            return ToolMessage(content="Not run: the user did not approve adding this document.",
                               tool_call_id=call["id"], name=call["name"])
        return await handler(request)
    return require_approval


def normalise(source: str, kind: str, number: str) -> str:
    return f"{source}, {kind} {number}"


def check_citations(answer: str, retrieved: set[str]) -> tuple[list[str], list[str]]:
    """Return (cited, not_retrieved) for the citations in an answer."""
    sources = {c.split(",", 1)[0] for c in retrieved}
    cited = list(dict.fromkeys(normalise(*m) for m in citation_pattern(sources).findall(answer)))
    return cited, [c for c in cited if c not in retrieved]


# --------------------------------------------------------------------------- run

def build_agent(tools, approve):
    model = ChatGoogleGenerativeAI(model=MODEL, api_key=load_api_key(), timeout=90, max_retries=2)  # lite models ignore temperature
    return create_agent(
        model=model,
        tools=tools,
        system_prompt=(ROOT / "AGENTS.md").read_text(encoding="utf-8"),
        middleware=[
            approval_middleware(approve),
            ToolCallLimitMiddleware(run_limit=MAX_TOOL_CALLS, exit_behavior="end"),
            ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS, exit_behavior="end"),
        ],
    )


async def run_one(agent, question: str) -> dict:
    started = time.time()
    state = await agent.ainvoke({"messages": [{"role": "user", "content": question}]})
    messages = state["messages"]

    trace, retrieved, tokens = {}, set(), 0
    for message in messages:
        if isinstance(message, AIMessage):
            tokens += (message.usage_metadata or {}).get("total_tokens", 0)
            for call in message.tool_calls:
                trace[call["id"]] = {"tool": call["name"], "args": call["args"], "result": ""}
        elif isinstance(message, ToolMessage):
            text = message.text
            if message.tool_call_id in trace:
                trace[message.tool_call_id]["result"] = text
            if message.name == "search":
                retrieved |= {normalise(src, *loc.split(" ", 1)) for src, loc in CITE_LINE.findall(text)}

    final = next((m for m in reversed(messages) if isinstance(m, AIMessage) and not m.tool_calls), None)
    draft = final.text.strip() if final else ""
    cited, not_retrieved = check_citations(draft, retrieved)
    refused = draft.startswith(REFUSAL)

    guardrail = None
    if not draft:
        guardrail = "no final answer (call limit reached)"
    elif not_retrieved:
        guardrail = f"cited passages that search did not return: {', '.join(not_retrieved)}"
    elif not refused and not cited and not any(t["tool"] == "add_document" for t in trace.values()):
        guardrail = "answer without any citation"
    answer = draft
    if guardrail:
        answer = (f"{REFUSAL} The draft answer was withheld by the citation check "
                  f"({guardrail}). Please check the official text or ask a lawyer.")

    return {
        "question": question, "answer": answer, "draft": draft, "refused": refused or bool(guardrail),
        "guardrail": guardrail, "cited": cited, "retrieved": sorted(retrieved), "trace": list(trace.values()),
        "tokens": tokens, "seconds": round(time.time() - started, 1),
    }


async def ask_many(questions: list[str], approve: Callable[[dict], bool] = ask_human) -> list[dict]:
    """Answer several questions with one MCP server session. Used by evaluate.py."""
    params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT))
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            agent = build_agent(await load_mcp_tools(session), approve)
            return [await run_one(agent, q) for q in questions]


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit('Usage: python agent.py "your question"')
    result = asyncio.run(ask_many([" ".join(sys.argv[1:])]))[0]
    for step in result["trace"]:
        if step["tool"] == "add_document":
            print(f"[add_document] {step['result']}\n")
    print(result["answer"])
    if result["cited"] and not result["guardrail"]:
        print("\nSources: " + "; ".join(result["cited"]))
    searches = [t["args"].get("query") for t in result["trace"] if t["tool"] == "search"]
    print(f"\n[{len(searches)} search(es): {searches} | {result['tokens']} tokens | {result['seconds']}s"
          + (f" | guardrail fired: {result['guardrail']}" if result["guardrail"] else "") + "]")


if __name__ == "__main__":
    main()
