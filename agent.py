"""
Assignment 3: your agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the tools from server.py over MCP and
AGENTS.md as the system prompt. add_document only runs after the user
approves it, and the run is capped at MAX_MODEL_CALLS model calls and
MAX_TOOL_CALLS tool calls. An answer citing a passage that no search returned
is rejected (citation guardrail). Prints the answer with its citations.

For evaluate.py: `open_tools()` starts the server once and `run_agent()`
returns the answer with its tool trace, tokens and seconds.
"""

import asyncio
import re
import sys
import time
from contextlib import asynccontextmanager
from pathlib import Path

from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware, ToolCallLimitMiddleware
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.tools import StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
MODEL = "gemini-3.8-flash"
# `ask` falls back down this list when a model is overloaded (503) or out of free-tier quota (429).
FALLBACK_MODELS = [MODEL, "gemini-3.5-flash", "gemini-3.5-flash-lite"]
MODEL_TIMEOUT = 75  # seconds per model before `ask` treats it as hung (check.py allows 300 s in total)
SYSTEM_PROMPT = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
MAX_MODEL_CALLS = 8
MAX_TOOL_CALLS = 6
NEEDS_APPROVAL = {"add_document"}

# Extra guardrail: an answer is rejected if it cites a passage that no search in
# this run returned (an invented, misspelled or merged citation), because the
# pharmacist could not check that claim against the label.
CITATION = re.compile(r"\[([a-z_]+), ([^\]]+)\]")
REJECTED = ("Answer withheld: it cited {bad}, which the label search did not return, so its claims "
            "cannot be checked. Please look it up in the label directly or ask the supervising pharmacist.")


def invalid_citations(answer: str, trace: list[dict]) -> list[str]:
    """Citations in the answer that do not match a [source, location] heading of any search result."""
    shown = {c for t in trace if t["tool"] == "search" for c in CITATION.findall(t["output"] or "")}
    return [f"[{s}, {l}]" for s, l in CITATION.findall(answer) if (s, l) not in shown]


def ask_approval(tool: str, args: dict) -> bool:
    """Ask in the terminal before a tool in NEEDS_APPROVAL runs; deny when nobody can answer."""
    if not sys.stdin.isatty():
        return False
    answer = input(f"\nThe agent wants to run {tool}({args}). Allow? [y/N] ")
    return answer.strip().lower() in ("y", "yes")


def as_langchain_tool(session: ClientSession, tool, approve) -> StructuredTool:
    """Wrap one MCP tool as a LangChain tool that calls the server."""
    async def call(**args) -> str:
        if tool.name in NEEDS_APPROVAL and not approve(tool.name, args):
            return f"The user did not approve running {tool.name}. Nothing was changed."
        result = await session.call_tool(tool.name, args)
        return "\n".join(getattr(c, "text", "") for c in result.content)

    return StructuredTool(name=tool.name, description=tool.description or "",
                          args_schema=tool.input_schema, coroutine=call)


@asynccontextmanager
async def open_tools(approve=ask_approval):
    """Start server.py over stdio, as an editor would, and yield its tools as LangChain tools."""
    params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT))
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = (await session.list_tools()).tools
            yield [as_langchain_tool(session, t, approve) for t in tools]


def build_agent(tools: list, model_name: str = MODEL):
    model = ChatGoogleGenerativeAI(model=model_name, api_key=load_api_key(), temperature=0)
    return create_agent(model, tools, system_prompt=SYSTEM_PROMPT, middleware=[
        ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS, exit_behavior="end"),
        ToolCallLimitMiddleware(run_limit=MAX_TOOL_CALLS, exit_behavior="end"),
    ])


async def run_agent(question: str, tools: list, model_name: str = MODEL) -> dict:
    """Answer one question. Returns the answer, the tool trace, token counts and seconds."""
    started = time.perf_counter()
    state = await build_agent(tools, model_name).ainvoke({"messages": [{"role": "user", "content": question}]})
    seconds = time.perf_counter() - started

    trace, calls, tokens = [], {}, {"input": 0, "output": 0, "total": 0}
    for message in state["messages"]:
        if isinstance(message, AIMessage):
            usage = message.usage_metadata or {}
            tokens["input"] += usage.get("input_tokens", 0)
            tokens["output"] += usage.get("output_tokens", 0)
            tokens["total"] += usage.get("total_tokens", 0)
            for call in message.tool_calls:
                calls[call["id"]] = {"tool": call["name"], "args": call["args"], "output": None}
                trace.append(calls[call["id"]])
        elif isinstance(message, ToolMessage) and message.tool_call_id in calls:
            calls[message.tool_call_id]["output"] = message.text

    final = state["messages"][-1]
    answer = final.text.strip() if isinstance(final, AIMessage) else ""
    bad = invalid_citations(answer, trace)
    guardrail = {"fired": bool(bad), "invalid_citations": bad, "rejected_answer": answer if bad else None}
    if bad:
        print(f"Citation guardrail fired: {', '.join(bad)}", file=sys.stderr)
        answer = REJECTED.format(bad=", ".join(bad))
    return {"answer": answer, "guardrail": guardrail, "trace": trace, "tokens": tokens, "seconds": round(seconds, 2),
            "model_calls": sum(isinstance(m, AIMessage) for m in state["messages"])}


async def ask(question: str) -> dict:
    async with open_tools() as tools:
        for model in FALLBACK_MODELS:
            try:
                return {**await asyncio.wait_for(run_agent(question, tools, model), MODEL_TIMEOUT), "model": model}
            except Exception as error:  # noqa: BLE001 - only overload, quota or hang moves on to the next model
                retryable = isinstance(error, TimeoutError) or any(c in str(error) for c in ("503", "429"))
                if model == FALLBACK_MODELS[-1] or not retryable:
                    raise
                print(f"{model} unavailable ({str(error)[:60]}...); trying the next model.", file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit('Usage: python agent.py "your question"')
    result = asyncio.run(ask(" ".join(sys.argv[1:])))
    print(result["answer"] or "(no answer)")
    print(f"\n[{result['model']}, {len(result['trace'])} tool call(s), {result['tokens']['total']} tokens, {result['seconds']} s]")
