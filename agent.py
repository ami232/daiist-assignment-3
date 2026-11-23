"""
Assignment 3: the agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini. Its tools come from server.py over MCP. AGENTS.md is the
system prompt. Guardrails: human approval before add_document runs, a limit of 6 tool calls,
and no answer unless the agent searched the corpus. `answer_question` returns the answer and
the tool trace, for evaluate.py.
"""

import asyncio
import os
import sys
import time
import traceback
from contextlib import asynccontextmanager
from pathlib import Path

from langchain.agents import create_agent
from langchain_core.tools import StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
MODEL = os.getenv("AGENT_MODEL", "gemini-flash-lite-latest")
MAX_TOOL_CALLS = 6
NO_SEARCH_ANSWER = "I don't know: I could not find supporting passages in the corpus."


def terminal_approval(action: str) -> bool:
    """Ask the person in the terminal. Without a terminal (e.g. evaluation), deny."""
    if not sys.stdin.isatty():
        return False
    return input(f"\nThe agent wants to run {action}. Approve? [y/N] ").strip().lower() == "y"


@asynccontextmanager
async def mcp_tools(approve, trace: list):
    """Start server.py over stdio and expose its two tools to LangChain."""
    params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT))
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            described = {t.name: t.description for t in (await session.list_tools()).tools}

            async def call(name: str, args: dict) -> str:
                if len(trace) >= MAX_TOOL_CALLS:  # guardrail: call limit
                    text = "Tool call limit reached. Answer with what you have, or say you do not know."
                else:
                    result = await session.call_tool(name, args)
                    text = "\n".join(getattr(c, "text", "") for c in result.content)
                trace.append({"tool": name, "args": args, "result": text})
                return text

            async def search(query: str) -> str:
                return await call("search", {"query": query})

            async def add_document(path: str) -> str:
                if not approve(f"add_document({path!r})"):  # guardrail: human approval
                    trace.append({"tool": "add_document", "args": {"path": path}, "result": "DENIED"})
                    return "The user did not approve. Nothing was added."
                return await call("add_document", {"path": path})

            yield [
                StructuredTool.from_function(coroutine=search, name="search", description=described["search"]),
                StructuredTool.from_function(
                    coroutine=add_document, name="add_document", description=described["add_document"]
                ),
            ]


def _text(content) -> str:
    if isinstance(content, str):
        return content
    return "".join(p.get("text", "") if isinstance(p, dict) else str(p) for p in content)


async def _ask(question: str, approve) -> dict:
    started = time.time()
    trace: list = []
    async with mcp_tools(approve, trace) as tools:
        agent = create_agent(
            ChatGoogleGenerativeAI(model=MODEL, google_api_key=load_api_key(), temperature=0, max_retries=6),
            tools,
            system_prompt=(ROOT / "AGENTS.md").read_text(encoding="utf-8"),
        )
        result = await agent.ainvoke({"messages": [("user", question)]})
    messages = result["messages"]
    answer = _text(messages[-1].content).strip()
    guardrail = None
    if not any(t["tool"] in ("search", "add_document") for t in trace):  # guardrail: never answer without searching
        answer, guardrail = NO_SEARCH_ANSWER, "no_search"
    usage = [m.usage_metadata for m in messages if getattr(m, "usage_metadata", None)]
    return {
        "question": question,
        "answer": answer,
        "trace": trace,
        "guardrail": guardrail,
        "input_tokens": sum(u.get("input_tokens", 0) for u in usage),
        "output_tokens": sum(u.get("output_tokens", 0) for u in usage),
        "seconds": time.time() - started,
    }


def answer_question(question: str, approve=terminal_approval) -> dict:
    """Answer and tool trace (used by evaluate.py). Retries when Gemini is busy or rate limited."""
    for attempt in range(5):
        try:
            return asyncio.run(_ask(question, approve))
        except Exception as error:  # noqa: BLE001
            details = "".join(traceback.format_exception(error))
            busy = "503" in details or "UNAVAILABLE" in details or "429" in details
            if not busy or attempt == 4:
                raise
            print(f"Gemini is busy (attempt {attempt + 1}/5); waiting 20 s...", file=sys.stderr)
            time.sleep(20)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit('usage: python agent.py "your question"')
    out = answer_question(" ".join(sys.argv[1:]))
    print(out["answer"])
    searches = sum(t["tool"] == "search" for t in out["trace"])
    print(
        f"\n[{out['input_tokens']} tokens in, {out['output_tokens']} out, {out['seconds']:.1f}s, "
        f"{searches} searches, guardrail: {out['guardrail']}]",
        file=sys.stderr,
    )