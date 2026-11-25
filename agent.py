"""
Assignment 3: the agent (`uv run python main.py ask "question"`).

LangChain create_agent on Gemini, with the tools of server.py over MCP and AGENTS.md as
system prompt. Guardrails:
  1. approval: add_document never runs until a person approves it (HumanInTheLoopMiddleware);
  2. call limits: at most 6 model calls and 4 tool calls per question;
  3. citation guardrail (our choice): an answer whose citations are missing, or point to a
     passage that search did not return in this run, is replaced by a refusal.

evaluate.py imports run(), which returns the answer and the full tool trace.
"""

import asyncio
import os
import re
import sys
import time
from pathlib import Path

from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware, ModelCallLimitMiddleware, ToolCallLimitMiddleware
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_core.tools import StructuredTool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

import rag
from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
CHAT_MODEL = os.environ.get("GEMINI_CHAT_MODEL", "gemini-flash-latest")
SYSTEM_PROMPT = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
REFUSAL = "The corpus does not cover this"
CITATION = re.compile(r"\[([A-Za-z0-9_.\-]+:\d{3})\]")
RESULT_ID = re.compile(r"^\[([A-Za-z0-9_.\-]+:\d{3})\]", re.M)
# the free tier allows only a few requests a minute: pace the calls instead of failing
RATE_LIMITER = InMemoryRateLimiter(requests_per_second=0.15, check_every_n_seconds=0.5, max_bucket_size=1)


def make_model():
    from langchain_google_genai import ChatGoogleGenerativeAI
    load_api_key()
    return ChatGoogleGenerativeAI(model=CHAT_MODEL, temperature=0, max_retries=6, rate_limiter=RATE_LIMITER)


def ask_person(request: dict) -> bool:
    """Approval step for add_document: a person types y/n. With nobody at the keyboard, refuse."""
    if not sys.stdin.isatty():
        print(f"[approval] {request['name']}({request['args']}) refused: nobody here to approve it.", file=sys.stderr)
        return False
    answer = input(f"\nThe agent wants to run {request['name']} with {request['args']}. Allow it? [y/N] ")
    return answer.strip().lower() in {"y", "yes"}


def is_refusal(answer: str) -> bool:
    return answer.strip().lower().startswith(REFUSAL.lower())


def citation_guardrail(answer: str, retrieved: list[str]) -> tuple[str, str | None]:
    """Our extra guardrail. Returns (answer to show, reason it fired or None)."""
    if is_refusal(answer):
        return answer, None
    cited = CITATION.findall(answer)
    if not cited:
        reason = "the answer cites no passage"
    elif invalid := sorted(set(cited) - set(retrieved)):
        reason = f"it cites passages search did not return: {', '.join(invalid)}"
    else:
        return answer, None
    return (f"{REFUSAL} with a source I can cite, so I won't answer it. "
            f"(Citation guardrail: {reason}.)"), reason


async def mcp_tools(session: ClientSession, trace: list[dict]) -> list[StructuredTool]:
    """Wrap each tool of the MCP server as a LangChain tool, recording every call in `trace`."""
    tools = []
    for tool in (await session.list_tools()).tools:
        async def call(_name=tool.name, **arguments) -> str:
            result = await session.call_tool(_name, arguments)
            text = "\n".join(getattr(c, "text", "") for c in result.content)
            trace.append({"tool": _name, "args": arguments, "output": text})
            return text
        tools.append(StructuredTool.from_function(coroutine=call, name=tool.name, description=tool.description,
                                                  args_schema=tool.input_schema))
    return tools


def final_text(messages: list) -> str:
    for message in reversed(messages):
        if isinstance(message, AIMessage) and not message.tool_calls:
            content = message.content
            if isinstance(content, list):
                content = "".join(part.get("text", "") if isinstance(part, dict) else str(part) for part in content)
            if content.strip():
                return content.strip()
    return f"{REFUSAL}: the agent stopped before giving an answer."


async def run(question: str, approve=ask_person, base_only: bool = False, model=None) -> dict:
    """Answer one question. Returns the answer, citations, retrieved ids, tool trace, tokens and seconds."""
    started, trace = time.time(), []
    env = {**os.environ, "GEMINI_API_KEY": load_api_key(), "CORPUS_BASE_ONLY": "1" if base_only else "0"}
    server = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT), env=env)
    async with stdio_client(server) as (read, write), ClientSession(read, write) as session:
        await session.initialize()
        agent = create_agent(
            model or make_model(),
            await mcp_tools(session, trace),
            system_prompt=SYSTEM_PROMPT,
            middleware=[
                HumanInTheLoopMiddleware(interrupt_on={"add_document": True}),
                ModelCallLimitMiddleware(run_limit=6, exit_behavior="end"),
                ToolCallLimitMiddleware(run_limit=4),
            ],
            checkpointer=InMemorySaver(),
        )
        config = {"configurable": {"thread_id": "question"}}
        state = await agent.ainvoke({"messages": [HumanMessage(question)]}, config)
        approvals = []
        while state.get("__interrupt__"):            # add_document is waiting for a person
            requests = state["__interrupt__"][0].value["action_requests"]
            decisions = []
            for request in requests:
                ok = approve(request)
                approvals.append({"tool": request["name"], "args": request["args"], "approved": ok})
                decisions.append({"type": "approve"} if ok else
                                 {"type": "reject", "message": "A person refused this action. Do not retry it."})
            state = await agent.ainvoke(Command(resume={"decisions": decisions}), config)

    messages = state["messages"]
    retrieved = [i for step in trace if step["tool"] == "search" for i in RESULT_ID.findall(step["output"])]
    raw_answer = final_text(messages)
    searched = any(step["tool"] == "search" for step in trace)
    # the citation guardrail checks answers about the corpus, not replies to "add this document"
    answer, fired = citation_guardrail(raw_answer, retrieved) if searched or not approvals else (raw_answer, None)
    usage = [m.usage_metadata for m in messages if isinstance(m, AIMessage) and m.usage_metadata]
    return {
        "question": question, "answer": answer, "raw_answer": raw_answer, "guardrail": fired,
        "refusal": is_refusal(answer), "cited": sorted(set(CITATION.findall(answer))),
        "retrieved": list(dict.fromkeys(retrieved)), "trace": trace, "approvals": approvals,
        "model_calls": len([m for m in messages if isinstance(m, AIMessage)]),
        "input_tokens": sum(u.get("input_tokens", 0) for u in usage),
        "output_tokens": sum(u.get("output_tokens", 0) for u in usage),
        "seconds": round(time.time() - started, 1),
    }


def sources(cited: list[str]) -> list[str]:
    design = rag.load_config()["design"]
    chunks = {c["id"]: c for c in rag.read_chunks(design)}
    return [f"[{i}] {rag.cite(chunks[i])} - {chunks[i]['url']}" for i in cited if i in chunks]


def main() -> None:
    question = " ".join(sys.argv[1:]).strip()
    if not question:
        raise SystemExit('Usage: uv run python main.py ask "your question"')
    result = asyncio.run(run(question))
    print(result["answer"])
    if result["cited"]:
        print("\nSources:")
        print("\n".join(sources(result["cited"])))
    if result["guardrail"]:
        print(f"\n(citation guardrail fired: {result['guardrail']})")
    print(f"\n[{result['model_calls']} model calls, {result['input_tokens'] + result['output_tokens']} tokens, "
          f"{result['seconds']}s]")


if __name__ == "__main__":
    main()
