"""
Assignment 3: your agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with tools from server.py over MCP and
AGENTS.md as system prompt. Ask for approval before add_document runs; add a
call limit and one guardrail of your choice. Print the answer with citations.

Start from session 10's 07-own-harness/harness.py. Expose a function that
returns the answer and the tool trace, for evaluate.py.
"""

import asyncio
import re
import sys
import time
from pathlib import Path

from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware, ModelCallLimitMiddleware
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.tools import StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
CHAT_MODEL = "gemini-3.1-flash-lite"
REFUSAL = "The corpus does not cover this question."
TAG = re.compile(r"\[(\w+) \| ([^\[\]|]+)\]")       # a citation tag such as [gdpr | Article 33]


def approve_in_terminal(tool, args):
    """Ask the person at the keyboard. With nobody there (CI, evaluation) the answer is no."""
    if not sys.stdin or not sys.stdin.isatty():
        return False
    print(f"\nThe agent wants to run {tool}({args}). This changes the index. Approve? [y/N] ",
          end="", file=sys.stderr, flush=True)
    return input().strip().lower() == "y"


def text_of(message):
    """Gemini sometimes returns a list of blocks instead of a string."""
    if isinstance(message.content, str):
        return message.content.strip()
    return "".join(b.get("text", "") for b in message.content if isinstance(b, dict)).strip()


def tags_in(text):
    """Citation tags in a text. "[gdpr | Article 33(1)]" counts as "[gdpr | Article 33]"."""
    return [f"[{source} | {re.sub(r'[(].*', '', location).strip()}]" for source, location in TAG.findall(text)]


async def ask_async(question, approve=approve_in_terminal):
    started = time.perf_counter()
    server = StdioServerParameters(command=sys.executable, args=[str(ROOT / "server.py")], cwd=str(ROOT),
                                   env={"GEMINI_API_KEY": load_api_key()})
    async with stdio_client(server) as (read, write), ClientSession(read, write) as session:
        await session.initialize()

        def as_langchain_tool(spec):                      # one LangChain tool per MCP tool
            async def run(**arguments):
                result = await session.call_tool(spec.name, arguments)
                return "\n".join(getattr(part, "text", "") for part in result.content)
            return StructuredTool.from_function(coroutine=run, name=spec.name,
                                                description=spec.description, args_schema=spec.input_schema)

        agent = create_agent(
            ChatGoogleGenerativeAI(model=CHAT_MODEL, api_key=load_api_key()),
            [as_langchain_tool(spec) for spec in (await session.list_tools()).tools],
            system_prompt=(ROOT / "AGENTS.md").read_text(encoding="utf-8"),
            middleware=[
                HumanInTheLoopMiddleware(interrupt_on={"add_document": True}),      # approval
                ModelCallLimitMiddleware(run_limit=6, exit_behavior="end"),          # call limit
            ],
            checkpointer=InMemorySaver(),                 # needed to pause for approval and resume
        )
        config = {"configurable": {"thread_id": "1"}, "recursion_limit": 60}
        state = await agent.ainvoke({"messages": [("user", question)]}, config)
        while state.get("__interrupt__"):                 # paused before add_document
            requests = state["__interrupt__"][0].value["action_requests"]
            decisions = [{"type": "approve"} if approve(r["name"], r["args"])
                         else {"type": "reject", "message": "The user did not approve this."} for r in requests]
            state = await agent.ainvoke(Command(resume={"decisions": decisions}), config)

    # Collect the answer, the tool trace and the cost from the messages.
    messages = state["messages"]
    answer = text_of(messages[-1])
    names = {call["id"]: call["name"] for m in messages if isinstance(m, AIMessage) for call in m.tool_calls}
    trace = [{"tool": names.get(m.tool_call_id, ""), "result": text_of(m)} for m in messages if isinstance(m, ToolMessage)]
    passages = "\n\n---\n\n".join(t["result"] for t in trace if t["tool"] == "search")
    retrieved = set(tags_in(passages))
    tokens = sum((m.usage_metadata or {}).get("total_tokens", 0) for m in messages if isinstance(m, AIMessage))

    # Guardrail (my choice): an answer is shown only if it refuses, or every citation in it
    # is a passage that search returned. Otherwise it is replaced by the refusal.
    refused = "corpus does not cover" in answer.lower()
    cited = tags_in(answer)
    grounded = refused or (cited and all(tag in retrieved for tag in cited))
    blocked = not grounded and not any(t["tool"] == "add_document" for t in trace)
    if blocked:
        answer, refused, cited = f"{REFUSAL} (A draft answer was withheld: its citations could not be verified.)", True, []
    return {"question": question, "answer": answer, "refused": refused, "blocked": blocked, "citations": cited,
            "retrieved": sorted(retrieved), "passages": passages, "tools": [t["tool"] for t in trace],
            "tokens": tokens, "seconds": round(time.perf_counter() - started, 1)}


def ask(question, approve=approve_in_terminal):
    """Answer one question. Returns the answer, the tool trace and the cost (used by evaluate.py)."""
    return asyncio.run(ask_async(question, approve))


if __name__ == "__main__":
    for stream in (sys.stdout, sys.stderr):
        stream.reconfigure(errors="replace")              # Windows consoles: never crash on a character
    result = ask(" ".join(sys.argv[1:]))
    print(result["answer"])
    print("\nSources: " + (", ".join(result["citations"]) or "none"))
    print(f"({result['tokens']} tokens, {result['seconds']}s, tools: {result['tools']}, "
          f"guardrail fired: {result['blocked']})", file=sys.stderr)
