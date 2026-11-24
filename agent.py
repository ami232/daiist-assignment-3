"""
Assignment 3: the agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the tools of server.py over MCP and
AGENTS.md as system prompt.

Guardrails:
- approval: add_document only runs if the user types "y" (evaluate.py passes auto_approve);
- call limits: at most 6 model calls and 3 searches per question;
- citation check (own guardrail): every "law, article" the answer cites must be one
  of the citations the search tool returned; otherwise a warning is appended.

For evaluate.py: build the agent once with build_agent(await load_tools(stack)),
then ask(agent, question) -> {"answer", "trace", "citations_ok", "seconds", "tokens"}.
"""

import asyncio
import re
import sys
import time
from contextlib import AsyncExitStack
from pathlib import Path

from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware, ToolCallLimitMiddleware, wrap_tool_call
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.tools import StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
MODEL = "gemini-flash-lite-latest"
NEEDS_APPROVAL = {"add_document"}   # changes the shared index
LAWS = ["LAU", "Llei 18/2007", "Decret-llei 3/2023"]
RE_RETRIEVED = re.compile(r"^\[\d+\] ([^,]+), ([^,(]+)", re.M)   # "[1] LAU, Artículo 36, ..."


# 1. Tools: start server.py over MCP and wrap each of its tools as a LangChain tool.
async def load_tools(stack: AsyncExitStack) -> list:
    params = StdioServerParameters(command=sys.executable, args=[str(ROOT / "server.py")], cwd=str(ROOT))
    read, write = await stack.enter_async_context(stdio_client(params))
    session = await stack.enter_async_context(ClientSession(read, write))
    await session.initialize()

    def wrap(t):
        async def call(**args) -> str:
            result = await session.call_tool(t.name, args)
            return "\n".join(c.text for c in result.content if hasattr(c, "text"))
        return StructuredTool(name=t.name, description=t.description, args_schema=t.input_schema,
                              coroutine=call)

    return [wrap(t) for t in (await session.list_tools()).tools]


# 2. Guardrail around the tools: ask the person at the keyboard before add_document runs.
def approval_guardrail(auto_approve: bool):
    @wrap_tool_call
    async def ask_before_indexing(request, handler):
        call = request.tool_call
        if call["name"] in NEEDS_APPROVAL and not auto_approve:
            if not (sys.stdin.isatty() and input(f"  Allow {call['name']}({call['args']})? [y/N] ").strip().lower() == "y"):
                return ToolMessage(content="The user refused this tool call. Do not retry it.",
                                   tool_call_id=call["id"], status="error")
        return await handler(request)
    return ask_before_indexing


# 3. The agent: model + tools + AGENTS.md + guardrails.
def build_agent(tools: list, auto_approve: bool = False):
    return create_agent(
        model=ChatGoogleGenerativeAI(model=MODEL, api_key=load_api_key(), temperature=0,
                                     timeout=120, max_retries=2),
        tools=tools,
        system_prompt=(ROOT / "AGENTS.md").read_text(encoding="utf-8"),
        middleware=[
            approval_guardrail(auto_approve),
            ModelCallLimitMiddleware(run_limit=6, exit_behavior="end"),
            ToolCallLimitMiddleware(tool_name="search", run_limit=3, exit_behavior="continue"),
        ],
    )


def tool_trace(messages: list) -> list[dict]:
    """Each tool call the model made, with the result the harness sent back."""
    outputs = {m.tool_call_id: m.text for m in messages if isinstance(m, ToolMessage)}
    return [{"tool": c["name"], "args": c["args"], "output": outputs.get(c["id"], "")}
            for m in messages if isinstance(m, AIMessage) for c in m.tool_calls]


def normalise(law: str, unit: str) -> tuple[str, str]:
    return law.strip(), re.sub(r"^art\.\s*", "artículo ", unit.strip().lower())


# 4. Own guardrail, after the model: cited (law, article) pairs must come from the search results.
def check_citations(answer: str, trace: list[dict]) -> set[str]:
    """Return the citations in the answer that no search result contained."""
    retrieved = {normalise(*m) for t in trace if t["tool"] == "search"
                 for m in RE_RETRIEVED.findall(t["output"])}
    laws = "|".join(re.escape(law) for law in set(LAWS) | {law for law, _ in retrieved})
    unit = r"(?:art[íi]culo|art\.|disposici[óo]n|anexo|pre[áa]mbulo)[^,()]*"   # only real citations
    cited = {normalise(*m) for m in re.findall(rf"({laws}),\s*({unit})", answer, re.I)}
    return {f"{law}, {unit}" for law, unit in cited - retrieved}


async def ask(agent, question: str) -> dict:
    start = time.time()
    state = await agent.ainvoke({"messages": [{"role": "user", "content": question}]})
    answer, trace = state["messages"][-1].text, tool_trace(state["messages"])
    unsupported = check_citations(answer, trace)
    if unsupported:
        answer += (f"\n\n⚠ Guardrail: {'; '.join(sorted(unsupported))} not found in the retrieved "
                   "passages. Verify before relying on this answer.")
    tokens = sum(m.usage_metadata.get("total_tokens", 0)
                 for m in state["messages"] if getattr(m, "usage_metadata", None))
    return {"answer": answer, "trace": trace, "citations_ok": not unsupported,
            "seconds": round(time.time() - start, 1), "tokens": tokens}


async def main(question: str) -> None:
    async with AsyncExitStack() as stack:
        agent = build_agent(await load_tools(stack))
        result = await ask(agent, question)
    for t in result["trace"]:
        print(f"  call {t['tool']}({t['args']})", file=sys.stderr)
    print(result["answer"])
    print(f"\n({result['seconds']} s, {result['tokens']} tokens)", file=sys.stderr)


if __name__ == "__main__":
    asyncio.run(main(" ".join(sys.argv[1:]) or input("Question: ")))
