"""
Assignment 3: your agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with tools from server.py over MCP and
AGENTS.md as system prompt. Asks for approval before add_document runs; has a
call limit and one extra guardrail: an answer that cites a passage the agent
never retrieved is withheld.

answer_question(question) returns (answer, trace) for evaluate.py.
"""

import asyncio
import re
import sys
import warnings
from contextlib import AsyncExitStack
from pathlib import Path

warnings.filterwarnings("ignore")

from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware, wrap_tool_call
from langchain.mcp import MCPAdapter  # beta, as in the session 10 harness
from langchain_core.messages import AIMessage, ToolMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
MODEL = "gemini-3.5-flash-lite"
SERVER = ROOT / "server.py"
NEEDS_APPROVAL = {"add_document"}  # changes the index and spends quota

CITED = re.compile(r"\[(RL|PVH|TPR) \| ([^|\]]+?) \| chunk (\d+)")


async def load_mcp_tools(stack):
    adapter = await stack.enter_async_context(MCPAdapter(SERVER))
    return await adapter.list_tools()


def approval_guardrail(auto_approve):
    @wrap_tool_call
    async def ask_before_adding(request, handler):
        call = request.tool_call
        if call["name"] in NEEDS_APPROVAL and not auto_approve:
            answer = input(f"  Allow {call['name']}({call['args']})? [y/N] ")
            if answer.strip().lower() != "y":
                return ToolMessage(
                    content="The user refused this tool call. Do not try again.",
                    tool_call_id=call["id"],
                    status="error",
                )
        return await handler(request)

    return ask_before_adding


def build_agent(tools, auto_approve=False):
    return create_agent(
        model=ChatGoogleGenerativeAI(model=MODEL),
        tools=tools,
        system_prompt=(ROOT / "AGENTS.md").read_text(),
        middleware=[
            approval_guardrail(auto_approve),
            ModelCallLimitMiddleware(run_limit=8),  # hard stop for runaway loops
        ],
    )


def tool_trace(messages):
    lines = []
    for message in messages:
        if isinstance(message, AIMessage):
            lines += [f"call {c['name']}({c['args']})" for c in message.tool_calls]
        elif isinstance(message, ToolMessage):
            lines.append(f"result {message.text}")
    return lines


def retrieved_citations(trace):
    """(ticker, section, chunk) of every passage the search tool really returned."""
    found = set()
    for line in trace:
        if line.startswith("result "):
            found |= {(t, s.strip(), int(n)) for t, s, n in CITED.findall(line)}
    return found


def invalid_citations(answer, trace):
    """Citations in the answer that were never retrieved. Checked in code, not by a model."""
    real = retrieved_citations(trace)
    return [c for c in {(t, s.strip(), int(n)) for t, s, n in CITED.findall(answer)} if c not in real]


def apply_guardrail(answer, trace):
    bad = invalid_citations(answer, trace)
    if bad:
        return (f"Answer withheld: it cites passages that were not retrieved {sorted(bad)}.")
    return answer


async def ask(agent, question):
    result = await agent.ainvoke({"messages": [{"role": "user", "content": question}]})
    trace = tool_trace(result["messages"])
    return apply_guardrail(result["messages"][-1].text, trace), trace


async def answer_question_async(question, auto_approve=False):
    load_api_key()
    async with AsyncExitStack() as stack:
        agent = build_agent(await load_mcp_tools(stack), auto_approve)
        return await ask(agent, question)


def answer_question(question, auto_approve=False):
    """For evaluate.py: returns (answer, trace)."""
    return asyncio.run(answer_question_async(question, auto_approve))


if __name__ == "__main__":
    question = " ".join(sys.argv[1:]) or "What are PVH's reportable segments?"
    answer, trace = answer_question(question)
    print("\n".join(f"  {line[:300]}" for line in trace), file=sys.stderr)
    print(answer)