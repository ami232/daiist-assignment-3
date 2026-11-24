"""
Assignment 3: the Chedar help-centre agent. `uv run python agent.py "question"`
(or `main.py ask "question"`).

Built on session 10's 07-own-harness/harness.py: LangChain `create_agent` on
Gemini, tools from server.py over MCP stdio, AGENTS.md as the system prompt,
and guardrails as middleware the model cannot skip:

1. approval: a person must say yes before `add_document` runs;
2. call limits: at most MAX_TOOL_CALLS tool calls and MAX_MODEL_CALLS model calls per question;
3. citation check: an answer that cites no URL from the retrieved passages is
   replaced by a "not found" message.

The harness uses langchain.mcp.MCPAdapter, which needs `fastmcp` (not in this
project's dependencies), so `load_mcp_tools` wraps the tools with the plain
`mcp` client instead: same result, a few more lines.

evaluate.py calls `run_agent(question, approve)`.
"""

import asyncio
import logging
import re
import sys
import time
from contextlib import AsyncExitStack
from pathlib import Path

from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware, ToolCallLimitMiddleware, wrap_tool_call
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.tools import StructuredTool
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
MODEL = "gemini-3.5-flash-lite"  # cheap, fast Flash model with a generous free tier
SERVER = ROOT / "server.py"
NEEDS_APPROVAL = {"add_document"}  # writes to the index and spends embedding quota
MAX_TOOL_CALLS = 6
MAX_MODEL_CALLS = 8
NOT_FOUND = (
    "I couldn't find this in the Chedar help centre (learn.chedar.io). "
    "Please contact Chedar support for help with this question."
)
URL_PATTERN = re.compile(r"https?://[^\s)\]>\"',]+")

logging.basicConfig(stream=sys.stderr, level=logging.INFO, format="[agent] %(message)s")
log = logging.getLogger("agent")


# 1. Tools: start server.py over stdio and wrap each MCP tool as a LangChain tool.
def _as_langchain_tool(session: ClientSession, tool) -> StructuredTool:
    async def call(**args) -> str:
        result = await session.call_tool(tool.name, args)
        text = "\n".join(getattr(block, "text", "") for block in result.content).strip()
        return f"Error: {text}" if result.is_error else text

    return StructuredTool.from_function(
        coroutine=call, name=tool.name, description=tool.description or "", args_schema=tool.input_schema
    )


async def load_mcp_tools(stack: AsyncExitStack) -> list[StructuredTool]:
    params = StdioServerParameters(command=sys.executable, args=[str(SERVER)], cwd=str(ROOT))
    read, write = await stack.enter_async_context(stdio_client(params))
    session = await stack.enter_async_context(ClientSession(read, write))
    await session.initialize()
    tools = (await session.list_tools()).tools
    return [_as_langchain_tool(session, tool) for tool in tools]


# 2. Guardrail 1: ask a person before add_document runs. The harness runs this, not the model.
def ask_on_stdin(tool_name: str, args: dict) -> bool:
    """Default approver: y/N on the terminal. With no terminal (eval, CI) the answer is no."""
    if not sys.stdin.isatty():
        log.info("approval: no terminal, denying %s(%s)", tool_name, args)
        return False
    answer = input(f"  Allow {tool_name}({args})? [y/N] ")
    return answer.strip().lower() == "y"


def approval_guardrail(approve):
    @wrap_tool_call
    async def ask_before_adding(request, handler):
        call = request.tool_call
        if call["name"] in NEEDS_APPROVAL and not approve(call["name"], call["args"]):
            log.info("approval: refused %s(%s)", call["name"], call["args"])
            return ToolMessage(
                content="The user refused this tool call. Do not add the document; tell the user it was not added.",
                tool_call_id=call["id"],
                status="error",
            )
        return await handler(request)

    return ask_before_adding


# 3. The agent: model + tools + AGENTS.md + guardrails 1 and 2.
def build_agent(tools, approve):
    from langchain_google_genai import ChatGoogleGenerativeAI

    return create_agent(
        model=ChatGoogleGenerativeAI(model=MODEL, temperature=0),
        tools=tools,
        system_prompt=(ROOT / "AGENTS.md").read_text(encoding="utf-8"),
        middleware=[
            approval_guardrail(approve),
            ToolCallLimitMiddleware(run_limit=MAX_TOOL_CALLS),  # blocks further calls; the model answers with what it has
            ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS, exit_behavior="end"),  # hard stop for runaway loops
        ],
    )


def tool_trace(messages) -> list[dict]:
    """Every tool call with its args and result, in order."""
    calls, trace = {}, []
    for message in messages:
        if isinstance(message, AIMessage):
            for call in message.tool_calls:
                calls[call["id"]] = {"tool": call["name"], "args": call["args"], "result": None}
                trace.append(calls[call["id"]])
        elif isinstance(message, ToolMessage) and message.tool_call_id in calls:
            calls[message.tool_call_id]["result"] = message.text
    return trace


def total_tokens(messages) -> int:
    return sum((m.usage_metadata or {}).get("total_tokens", 0) for m in messages if isinstance(m, AIMessage))


def _urls(text: str) -> set[str]:
    return {url.rstrip(".;:") for url in URL_PATTERN.findall(text or "")}


def cited_urls(answer: str, trace: list[dict]) -> list[str]:
    """URLs from search results that the answer actually cites."""
    retrieved = set()
    for call in trace:
        if call["tool"] == "search":
            retrieved |= _urls(call["result"] or "")
    return sorted(_urls(answer) & retrieved)


# 4. Guardrail 3: no citation, no answer. Replaces an answer that cites nothing it retrieved.
def citation_guardrail(answer: str, trace: list[dict]) -> str:
    if cited_urls(answer, trace):
        return answer
    if any(call["tool"] == "add_document" for call in trace) and not any(c["tool"] == "search" for c in trace):
        return answer  # a reply about adding a document has nothing to cite
    log.info("citation guardrail fired: the answer cited no retrieved URL; replaced it. Original: %r", answer[:300])
    return NOT_FOUND


async def _run(question: str, approve) -> dict:
    started = time.time()
    async with AsyncExitStack() as stack:
        agent = build_agent(await load_mcp_tools(stack), approve)
        result = await agent.ainvoke({"messages": [{"role": "user", "content": question}]})
    messages = result["messages"]
    trace = tool_trace(messages)
    answer = citation_guardrail(messages[-1].text.strip(), trace)
    return {"answer": answer, "trace": trace, "tokens": total_tokens(messages), "seconds": round(time.time() - started, 2)}


def run_agent(question: str, approve=None) -> dict:
    """Answer one question. Returns {answer, trace, tokens, seconds}.

    `approve(tool_name, args) -> bool` is asked before add_document runs;
    by default it asks on stdin and says no when there is no terminal.
    """
    load_api_key()  # raises a clear error if there is no GEMINI_API_KEY
    return asyncio.run(_run(question, approve or ask_on_stdin))


def main() -> int:
    question = " ".join(sys.argv[1:]).strip()
    if not question:
        print('Usage: uv run python agent.py "your question"', file=sys.stderr)
        return 2
    try:
        result = run_agent(question)
    except RuntimeError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 1
    print(result["answer"])
    sources = cited_urls(result["answer"], result["trace"])
    if sources:
        print("\nSources:")
        print("\n".join(f"- {url}" for url in sources))
    print(f"\n({len(result['trace'])} tool call(s), {result['tokens']} tokens, {result['seconds']} s)", file=sys.stderr)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
