"""
Assignment 3: the harness (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the tools from server.py over MCP and
AGENTS.md as the system prompt.

Guardrails
1. Approval: add_document only runs after a human types "yes" in the
   terminal. Without a terminal (evaluation, CI) it is refused.
2. Call limit: at most config.MAX_AGENT_STEPS graph steps per question.
3. Citation check (extra guardrail): every citation in the answer must match a
   passage the search tool actually returned in this run, and a non-refusal
   must cite something. If not, the model gets one chance to rewrite; if it
   fails again, the answer is replaced by a refusal.

`answer(question)` returns the answer and the trace; evaluate.py uses it.
"""

import asyncio
import os
import re
import sys
import time

from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.tools import StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.errors import GraphRecursionError
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from pydantic import BaseModel, Field

import config as C
from api_key import load_api_key

CITE = re.compile(r"\[([a-z0-9][a-z0-9\-]*) p\.\s*([A-Za-z0-9\-]+)\]")
RESULT_HEAD = re.compile(r"^\[([a-z0-9][a-z0-9\-]*) p\.([A-Za-z0-9\-]+)\]  .*\| pages: (.*)$", re.M)


class SearchArgs(BaseModel):
    query: str = Field(description="Short, specific search query")


class AddArgs(BaseModel):
    path: str = Field(description="Path of the file to add, inside the project")


def ask_approval(path: str) -> bool:
    if not sys.stdin.isatty():
        return False
    print(f"\nThe agent wants to run add_document(path={path!r}).", file=sys.stderr)
    return input("Allow it? Type 'yes' to approve: ").strip().lower() == "yes"


def is_refusal(text: str) -> bool:
    return text.strip().lower().startswith(C.REFUSAL_PREFIX.lower())


def retrieved_citations(trace: list[dict]) -> set[tuple[str, str]]:
    """(doc_id, page) pairs the search tool returned in this run, every page of each chunk."""
    ok = set()
    for t in trace:
        if t["tool"] == "search":
            for doc_id, _, pages in RESULT_HEAD.findall(t["output"]):
                for p in pages.split(","):
                    ok.add((doc_id, p.strip()))
    return ok


def check_citations(text: str, trace: list[dict]) -> str | None:
    """None if the answer passes; otherwise what is wrong."""
    if is_refusal(text):
        return None
    cited = set(CITE.findall(text))
    if not cited:
        return "The answer has no citations."
    bad = cited - retrieved_citations(trace)
    if bad:
        return "These citations are not in the search results: " + ", ".join(f"[{d} p.{p}]" for d, p in sorted(bad))
    return None


def _usage(messages) -> dict:
    tin = tout = 0
    for m in messages:
        u = getattr(m, "usage_metadata", None) or {}
        tin += u.get("input_tokens", 0)
        tout += u.get("output_tokens", 0)
    return {"input_tokens": tin, "output_tokens": tout}


async def _run(question: str, interactive: bool) -> dict:
    load_api_key()
    system_prompt = (C.ROOT / "AGENTS.md").read_text(encoding="utf-8")
    trace: list[dict] = []
    params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(C.ROOT),
                                    env=dict(os.environ))

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            descriptions = {t.name: t.description for t in (await session.list_tools()).tools}

            async def call(name: str, args: dict) -> str:
                res = await session.call_tool(name, args)
                return "\n".join(getattr(c, "text", "") for c in res.content)

            async def search(query: str) -> str:
                out = await call("search", {"query": query})
                trace.append({"tool": "search", "input": query, "output": out})
                return out

            async def add_document(path: str) -> str:
                if not (interactive and ask_approval(path)):
                    out = "Not run: the user did not approve adding this document."
                else:
                    out = await call("add_document", {"path": path})
                trace.append({"tool": "add_document", "input": path, "output": out})
                return out

            tools = [
                StructuredTool.from_function(coroutine=search, name="search",
                                             description=descriptions["search"], args_schema=SearchArgs),
                StructuredTool.from_function(coroutine=add_document, name="add_document",
                                             description=descriptions["add_document"], args_schema=AddArgs),
            ]
            model = ChatGoogleGenerativeAI(model=C.CHAT_MODEL, temperature=0, max_retries=6)
            agent = create_agent(model, tools, system_prompt=system_prompt)

            messages = [HumanMessage(question)]
            guardrail = None
            for attempt in range(2):
                try:
                    state = await agent.ainvoke({"messages": messages},
                                                config={"recursion_limit": C.MAX_AGENT_STEPS})
                except GraphRecursionError:
                    text = f"{C.REFUSAL_PREFIX}: I stopped after reaching the limit of {C.MAX_AGENT_STEPS} steps."
                    guardrail = f"call limit: stopped after {C.MAX_AGENT_STEPS} steps"
                    break
                messages = state["messages"]
                text = str(messages[-1].text).strip()
                problem = check_citations(text, trace)
                if problem is None:
                    break
                guardrail = f"citation check: {problem}"
                if attempt == 0:
                    messages = messages + [HumanMessage(
                        f"Your answer failed an automatic check. {problem} Rewrite it using only "
                        f"the passages the search tool returned, citing each claim as [doc_id p.PAGE], "
                        f"or start with \"{C.REFUSAL_PREFIX}\" if they do not answer the question.")]
                else:
                    text = (f"{C.REFUSAL_PREFIX} in a way I could verify: my draft answer failed the "
                            f"citation check twice ({problem}), so I withheld it.")
            all_msgs = messages

    return {"answer": text, "trace": trace, "guardrail": guardrail,
            "tool_calls": sum(len(getattr(m, "tool_calls", []) or []) for m in all_msgs if isinstance(m, AIMessage)),
            **_usage(all_msgs)}


def answer(question: str, interactive: bool = False) -> dict:
    """{"answer", "trace", "guardrail", "tool_calls", "input_tokens", "output_tokens", "seconds"}"""
    start = time.time()
    result = asyncio.run(_run(question, interactive))
    result["seconds"] = round(time.time() - start, 1)
    return result


def sources(result: dict) -> list[str]:
    """Cited passages with their titles, for printing."""
    titles = {}
    for t in result["trace"]:
        if t["tool"] == "search":
            for line in t["output"].splitlines():
                m = re.match(r"^\[([a-z0-9\-]+) p\.([A-Za-z0-9\-]+)\]  ([^|]+)\|", line)
                if m:
                    titles[m.group(1)] = m.group(3).strip()
    cited = dict.fromkeys(CITE.findall(result["answer"]))
    return [f"[{d} p.{p}] {titles.get(d, '')}" for d, p in cited]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit('Usage: python agent.py "your question"')
    r = answer(" ".join(sys.argv[1:]), interactive=sys.stdin.isatty())
    print(r["answer"])
    src = sources(r)
    if src:
        print("\nSources:")
        print("\n".join(f"  {s}" for s in src))
    if r["guardrail"]:
        print(f"\n(guardrail fired: {r['guardrail']})")
    print(f"\n({r['tool_calls']} tool calls, {r['input_tokens'] + r['output_tokens']} tokens, {r['seconds']}s)")
