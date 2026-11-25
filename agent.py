"""
Assignment 3: your agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with tools from server.py over MCP and
AGENTS.md as system prompt. Two guardrails:
  1. add_document needs a human's approval (a harness rule the model cannot skip).
  2. A hard limit of 8 model calls per question (stops runaway loops).

`ask(agent, question)` returns the answer and the tool trace, for evaluate.py.

Approval modes (build_agent's `approval`):
  "ask"   - ask the person at the keyboard (normal use: main.py ask)
  "deny"  - refuse every add_document call, silently (evaluation: nobody is there to
            answer, and an unattended run must never change the index)
  "allow" - approve everything (only for a demo the person runs on purpose)
"""

import asyncio
import sys
from contextlib import AsyncExitStack
from pathlib import Path

from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware, wrap_tool_call
from langchain_core.messages import AIMessage, ToolMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain.mcp import MCPAdapter  # langchain.mcp is in beta and warns on import

from api_key import load_api_key

ROOT = Path(__file__).parent
MODEL = "gemini-3.5-flash-lite"  # fast, cheap, generous free-tier quota
SERVERS = [ROOT / "server.py"]
NEEDS_APPROVAL = {"add_document"}  # tools that change the index
CALL_LIMIT = 8  # model calls per question


# 1. Tools: connect to the MCP server; MCPAdapter wraps its tools as LangChain tools.
async def load_mcp_tools(stack):
    tools = []
    for script in SERVERS:
        adapter = await stack.enter_async_context(MCPAdapter(script))
        tools += await adapter.list_tools()
    return tools


# 2. Guardrail around the tools: a human must approve before the index is changed.
#    The model cannot skip it, because the harness runs it, not the model.
def approval_guardrail(approval):
    @wrap_tool_call
    async def ask_before_changing_index(request, handler):
        call = request.tool_call
        if call["name"] in NEEDS_APPROVAL and approval != "allow":
            if approval == "ask":
                answer = input(f"  Allow {call['name']}({call['args']})? [y/N] ")
                allowed = answer.strip().lower() == "y"
            else:  # "deny"
                allowed = False
            if not allowed:
                return ToolMessage(
                    content="The user refused this tool call. Do not try to change the index another way.",
                    tool_call_id=call["id"],
                    status="error",
                )
        return await handler(request)

    return ask_before_changing_index


# 3. The agent: model + tools + standing rules + guardrails.
def build_agent(tools, approval="ask"):
    return create_agent(
        model=ChatGoogleGenerativeAI(model=MODEL, google_api_key=load_api_key()),
        tools=tools,
        system_prompt=(ROOT / "AGENTS.md").read_text(encoding="utf-8"),
        middleware=[
            approval_guardrail(approval),
            ModelCallLimitMiddleware(run_limit=CALL_LIMIT),
        ],
    )


def tool_trace(messages):
    """Every tool call and its result, in order: what the harness saw happen."""
    lines = []
    for message in messages:
        if isinstance(message, AIMessage):
            lines += [f"call {c['name']}({c['args']})" for c in message.tool_calls]
        elif isinstance(message, ToolMessage):
            lines.append(f"result {message.text}")  # MCP results arrive as content blocks
    return lines


async def ask(agent, question):
    """Run one question through the agent. Returns the final answer and the tool trace."""
    result = await agent.ainvoke({"messages": [{"role": "user", "content": question}]})
    return result["messages"][-1].text, tool_trace(result["messages"])


async def main(question):
    async with AsyncExitStack() as stack:
        agent = build_agent(await load_mcp_tools(stack), approval="ask")
        answer, trace = await ask(agent, question)
    print("\n".join(f"  {line}" for line in trace))
    print(answer)


if __name__ == "__main__":
    asyncio.run(main(" ".join(sys.argv[1:]) or "How much notice must I give before FMLA leave?"))