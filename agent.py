"""
Assignment 3: my agent (`main.py ask "question"` runs `python agent.py "question"`).

A LangChain agent on Gemini. Its tools (search, add_document) come from server.py over MCP, and
AGENTS.md is its system prompt. Three guardrails:
  1. add_document needs a human "yes" in the terminal before it runs (required by the assignment).
  2. Call limit: at most MAX_MODEL_CALLS model calls per question, so it cannot loop and burn quota.
  3. Citation check (my own): every [source | location] cited in the answer must be one that
     search returned during this run. If not, the answer is replaced by a refusal.

run_agent(question) returns the answer and the tool trace, for evaluate.py.
"""
from __future__ import annotations

import asyncio
import os
import re
import sys
import time
from pathlib import Path

from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware
from langchain_core.tools import StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
MODEL = os.getenv("AGENT_MODEL", "gemini-3.5-flash-lite")
MAX_MODEL_CALLS = 6
SERVER_ARGS = [str(ROOT / "server.py")]  # evaluate/tests may point this at another server
CITATION = re.compile(r"\[([a-z0-9][a-z0-9\-]*) \| ([^\]]+)\]")
UNVERIFIED = ("I cannot give a verified answer: my draft cited a passage that the search did not return. "
              "Please rephrase the question or check the SEC source directly.")
LIMIT_REACHED = "I could not finish within the call limit, so I cannot give a verified answer."


def ask_human(path: str) -> bool:
    """Default approval for add_document: the person types y or n in the terminal."""
    print(f"\nThe agent wants to ADD this document to the index: {path}", file=sys.stderr)
    return input("Allow it? [y/N] ").strip().lower() in {"y", "yes"}


def tool_text(result) -> str:
    return "\n".join(part.text for part in result.content if getattr(part, "text", None))


async def make_tools(session: ClientSession, trace: list, approve) -> list:
    """Wrap the MCP tools as LangChain tools; every call is recorded in `trace`."""
    async def search(query: str) -> str:
        """Search the corpus and return the closest passages, each with a citation."""
        text = tool_text(await session.call_tool("search", {"query": query}))
        trace.append({"tool": "search", "args": {"query": query}, "result": text})
        return text

    async def add_document(path: str) -> str:
        """Add one document (a file path) to the searchable index. Asks the human first."""
        if not approve(path):
            text = "The human refused: the document was NOT added."
        else:
            text = tool_text(await session.call_tool("add_document", {"path": path}))
        trace.append({"tool": "add_document", "args": {"path": path}, "result": text})
        return text

    # Reuse the descriptions written in server.py so the model sees the real tool documentation.
    described = {t.name: t.description for t in (await session.list_tools()).tools}
    return [
        StructuredTool.from_function(coroutine=search, name="search", description=described["search"]),
        StructuredTool.from_function(coroutine=add_document, name="add_document",
                                     description=described["add_document"]),
    ]


def _squash(text: str) -> str:
    """Compare citations ignoring case, spaces and punctuation (the model may retype them slightly differently)."""
    return re.sub(r"[^a-z0-9]+", "", text.lower())


def check_citations(answer: str, trace: list) -> bool:
    """Guardrail 3: every citation in the answer must have been returned by a search call."""
    returned = set()
    for step in trace:
        if step["tool"] == "search":
            returned |= {(s, _squash(l)) for s, l in CITATION.findall(step["result"].replace("Citation: ", ""))}
    cited = {(s, _squash(l)) for s, l in CITATION.findall(answer)}
    return cited <= returned

async def run_agent_async(question: str, approve=ask_human) -> dict:
    start = time.time()
    trace: list = []
    server = StdioServerParameters(command=sys.executable, args=SERVER_ARGS, cwd=str(ROOT), env=dict(os.environ))
    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await make_tools(session, trace, approve)
            model = MODEL if not isinstance(MODEL, str) else ChatGoogleGenerativeAI(
                model=MODEL, google_api_key=load_api_key())
            agent = create_agent(
                model, tools,
                system_prompt=(ROOT / "AGENTS.md").read_text(encoding="utf-8"),
                middleware=[ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS, exit_behavior="end")])
            state = await agent.ainvoke({"messages": [{"role": "user", "content": question}]})
    messages = state["messages"]
    answer = str(messages[-1].text).strip()
    usage = [m.usage_metadata for m in messages if getattr(m, "usage_metadata", None)]
    cited_ok = check_citations(answer, trace)
    if os.getenv("AGENT_DEBUG"):
        print("RAW ANSWER:", answer, file=sys.stderr)
        for step in trace:
            if step["tool"] == "search":
                print("RETURNED:", re.findall(r"Citation: (.*)", step["result"]), file=sys.stderr)
    if answer.startswith("Model call limits exceeded"):
        answer = LIMIT_REACHED
    elif not cited_ok:
        answer = UNVERIFIED
    return {
        "question": question,
        "answer": answer,
        "trace": trace,
        "citations_ok": cited_ok,
        "input_tokens": sum(u.get("input_tokens", 0) for u in usage),
        "output_tokens": sum(u.get("output_tokens", 0) for u in usage),
        "seconds": round(time.time() - start, 2),
    }


def run_agent(question: str, approve=ask_human) -> dict:
    return asyncio.run(run_agent_async(question, approve))


def main() -> int:
    if len(sys.argv) < 2:
        print('usage: python agent.py "your question"', file=sys.stderr)
        return 2
    result = run_agent(" ".join(sys.argv[1:]))
    print(result["answer"])
    print(f"\n[{len(result['trace'])} tool call(s), {result['input_tokens']} input / "
          f"{result['output_tokens']} output tokens, {result['seconds']} s]")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())