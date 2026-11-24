"""Run a LangChain research agent with tools connected to the MCP server over stdio."""
import asyncio
import json
import os
import re
import sys
import time
from contextlib import asynccontextmanager
from pathlib import Path

from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware, ModelRetryMiddleware
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.tools import StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from api_key import load_api_key
from corpus_data import ROOT

REFUSAL = "The indexed documents do not establish an answer."
CHAT_MODEL = os.environ.get("PG_RAG_CHAT_MODEL", "gemini-3.5-flash-lite")
BRACKETS = re.compile(r"\[([^\[\]]*)\]")


def citation_ids(answer):
    # Keep every comma-separated item, including malformed ones, for membership checks.
    return {item.strip() for group in BRACKETS.findall(answer) if "PG-" in group
            for item in group.split(",")}


@asynccontextmanager
async def server_session():
    env = {k: os.environ[k] for k in ("PG_RAG_DB", "GEMINI_API_KEY") if k in os.environ}
    params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT), env=env)
    async with stdio_client(params) as streams, ClientSession(*streams) as session:
        await session.initialize()
        yield session


async def call_mcp(session, name, args):
    result = await session.call_tool(name, args)
    text = "\n".join(item.text for item in result.content if hasattr(item, "text"))
    if result.is_error:
        raise ValueError(text)
    return json.loads(text)


def guard_answer(answer, evidence):
    if answer.strip() == REFUSAL:
        return REFUSAL, None
    cited = citation_ids(answer)
    if not cited or not cited.issubset(evidence):
        return REFUSAL, "missing or unknown citation"
    return answer.strip(), None


def approve(path):
    if not sys.stdin.isatty():
        return False
    return input(f"Add this file to the index? {path} [y/N] ").strip().lower() in {"yes", "y"}


async def answer_question(question, session, *, allow_approval=False):
    trace = []
    passages = {}
    started = time.monotonic()

    async def search(query: str) -> str:
        """Search the PostgreSQL documentation using one query string; returns citable evidence."""
        rows = await call_mcp(session, "search", {"query": query})
        passages.update((r["id"], r) for r in rows)
        trace.append({"tool": "search", "query": query, "ids": [r["id"] for r in rows]})
        return json.dumps(rows, ensure_ascii=False)

    async def add_document(path: str) -> str:
        """Ask the user to approve indexing the named local text or Markdown document."""
        resolved = str(Path(path).expanduser().resolve())
        approved = allow_approval and approve(resolved)
        event = {"tool": "add_document", "path": resolved, "approved": approved}
        trace.append(event)
        if not approved:
            event["result"] = "Addition denied."
        else:
            event["result"] = await call_mcp(session, "add_document", {"path": resolved})
        return json.dumps(event["result"])

    model = ChatGoogleGenerativeAI(model=CHAT_MODEL, api_key=load_api_key(), max_retries=3)
    agent = create_agent(model, [StructuredTool.from_function(coroutine=fn) for fn in (search, add_document)],
                         system_prompt=(ROOT / "AGENTS.md").read_text(),
                         middleware=[ModelCallLimitMiddleware(run_limit=5, exit_behavior="end"),
                                     ModelRetryMiddleware(max_retries=4, initial_delay=2, on_failure="error",
                                         retry_on=lambda err: any(x in str(err) for x in ("429", "502", "503", "504")))])
    first_passages = await search(question)
    initial_call = {"name": "search", "args": {"query": question}, "id": "initial_search"}
    run = await agent.ainvoke({"messages": [
        HumanMessage(content=question),
        AIMessage(content="", tool_calls=[initial_call]),
        ToolMessage(content=first_passages, tool_call_id=initial_call["id"], name="search"),
    ]})
    messages = [m for m in run["messages"] if isinstance(m, AIMessage)]
    raw = messages[-1].text.strip()
    additions = [event for event in trace if event["tool"] == "add_document"]
    if additions and sum(event["tool"] == "search" for event in trace) == 1:
        answer, guard = json.dumps(additions[-1]["result"], ensure_ascii=False), None
    else:
        answer, guard = guard_answer(raw, passages)
    usage = [m.usage_metadata or {} for m in messages]
    return {"question": question, "answer": answer, "raw_answer": raw, "trace": trace,
            "passages": list(passages.values()), "guardrail": guard, "model": CHAT_MODEL,
            "input_tokens": sum(x.get("input_tokens", 0) for x in usage),
            "output_tokens": sum(x.get("output_tokens", 0) for x in usage),
            "seconds": round(time.monotonic() - started, 3)}


async def main(question):
    async with server_session() as session:
        result = await answer_question(question, session, allow_approval=True)
    print(result["answer"])
    cited = citation_ids(result["answer"])
    for r in result["passages"]:
        if r["id"] in cited:
            print(f'[{r["id"]}] {r["source"]} · {r["location"]} · {r["url"]}')


if __name__ == "__main__":
    asyncio.run(main(" ".join(sys.argv[1:])))
