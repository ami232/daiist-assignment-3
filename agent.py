"""
Assignment 3: the agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with server.py's two tools reached over MCP
(the same server your editor uses) and AGENTS.md as the system prompt.

Middleware (runs around every model / tool call):
    HumanInTheLoopMiddleware  add_document pauses until a person approves it
    ModelCallLimitMiddleware  at most MAX_MODEL_CALLS model calls per question

Guardrail (after the agent answers): every [source, location] citation must be
one that search returned; otherwise the answer becomes the refusal sentence.

`ask(question)` returns the answer plus a trace (tool calls, retrieved text,
tokens, seconds) so evaluate.py can check and grade it.
"""

from __future__ import annotations

import asyncio
import os
import re
import sys
import time
import uuid
from contextlib import asynccontextmanager
from pathlib import Path

from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware, ModelCallLimitMiddleware
from langchain_core.tools import StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
# Free tier: 3.5-flash allows only 20 requests a day; flash-lite has more room.
MODEL = "gemini-3.5-flash-lite"
MAX_MODEL_CALLS = 6  # a question needs ~2-3 (search, maybe search again, answer)

# "[LAU, Artículo 36, p. 25]": the source has no comma, the location may have one.
CITATION = re.compile(r"\[([^\[\],]+), ([^\[\]]+)\]")


def citations(text: str) -> list[tuple[str, str]]:
    """Every [source, location] citation in a text, in order."""
    return [(source.strip(), location.strip()) for source, location in CITATION.findall(text)]


# Fixed sentences from AGENTS.md. The guardrail and evaluate.py match them literally,
# so they must stay identical there (tests/test_guardrail.py checks it).
REFUSAL = "No encuentro esta información en el corpus legal disponible."
PARTIAL_PREFIX = "Parte no cubierta por el corpus:"
DISCLAIMER = "Aviso: información general basada en la legislación estatal; no es asesoramiento legal."


# ---------------------------------------------------------------------------
# Guardrail: every citation in the answer must be one that search returned
# ---------------------------------------------------------------------------

def citation_problem(answer: str, search_results: list[str]) -> str | None:
    """Why the answer must not reach the user, or None if it may.

    A refusal passes. Any other answer needs at least one citation, and every
    citation must match, character for character, a result header from search.
    """
    if answer.strip() == REFUSAL:
        return None
    cited = citations(answer)
    if not cited:
        return "answer has no citations"
    returned = {c for block in search_results for c in citations(block)}
    invented = [c for c in cited if c not in returned]
    if invented:
        return "cited but not returned by search: " + "; ".join(f"{s}, {loc}" for s, loc in invented)
    return None


def verify_citations(answer: str, search_results: list[str]) -> str:
    """The answer if its citations are all real, otherwise the refusal sentence."""
    return REFUSAL if citation_problem(answer, search_results) else answer


# ---------------------------------------------------------------------------
# MCP -> LangChain: start server.py and wrap each of its tools
# ---------------------------------------------------------------------------

def as_langchain_tool(session: ClientSession, tool) -> StructuredTool:
    """A LangChain tool with the MCP tool's name, description and arguments,
    which forwards every call to the server."""

    async def call(**arguments) -> str:
        result = await session.call_tool(tool.name, arguments)
        return "\n".join(getattr(part, "text", "") for part in result.content)

    return StructuredTool.from_function(coroutine=call, name=tool.name,
                                        description=tool.description, args_schema=tool.input_schema)


@asynccontextmanager
async def mcp_tools(env: dict | None = None):
    """Run server.py over stdio (as an editor does) for as long as the block lasts."""
    params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT),
                                   env=env or dict(os.environ))
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            yield [as_langchain_tool(session, t) for t in (await session.list_tools()).tools]


# ---------------------------------------------------------------------------
# The agent
# ---------------------------------------------------------------------------

def build_agent(tools: list):
    load_api_key()
    return create_agent(
        ChatGoogleGenerativeAI(model=MODEL, temperature=0, max_retries=6),
        tools,
        system_prompt=(ROOT / "AGENTS.md").read_text(encoding="utf-8"),
        middleware=[
            HumanInTheLoopMiddleware(interrupt_on={"add_document": {"allowed_decisions": ["approve", "reject"]}}),
            ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS, exit_behavior="end"),
        ],
        checkpointer=InMemorySaver(),  # the approval pause needs saved state to resume from
    )


def approve_in_terminal(action: dict) -> bool:
    """Ask the person at the keyboard; with no keyboard (e.g. evaluation), refuse."""
    if not sys.stdin.isatty():
        print(f"(no terminal to approve {action['name']}({action['args']}); rejected)", file=sys.stderr)
        return False
    answer = input(f"\nThe agent wants to run {action['name']} with {action['args']}. Allow? [y/N] ")
    return answer.strip().lower() in {"y", "yes", "s", "si", "sí"}


async def ask(question: str, agent, approve=approve_in_terminal) -> dict:
    """Run one question to the end, pausing for approval when the agent asks for it."""
    config = {"configurable": {"thread_id": str(uuid.uuid4())}}
    started = time.time()
    result = await agent.ainvoke({"messages": [{"role": "user", "content": question}]}, config, version="v2")
    while result.interrupts:
        requests = result.interrupts[0].value["action_requests"]
        decisions = [{"type": "approve"} if approve(r) else
                     {"type": "reject", "message": "The user did not approve this action."} for r in requests]
        result = await agent.ainvoke(Command(resume={"decisions": decisions}), config, version="v2")
    return summarise(result.value["messages"], time.time() - started)


def summarise(messages: list, seconds: float) -> dict:
    """The final answer (after the guardrail) plus everything evaluate.py needs."""
    tool_calls = [{"name": c["name"], "args": c["args"]}
                  for m in messages if m.type == "ai" for c in (m.tool_calls or [])]
    tool_results = [{"name": m.name, "text": m.text} for m in messages if m.type == "tool"]
    retrieved = [r["text"] for r in tool_results if r["name"] == "search"]
    usage = [m.usage_metadata for m in messages if m.type == "ai" and m.usage_metadata]
    raw_answer = messages[-1].text if messages[-1].type == "ai" else ""
    # The reply to an add_document request is a status message, not an answer
    # from the corpus, so only answers to questions go through the guardrail.
    added = any(c["name"] == "add_document" for c in tool_calls)
    problem = None if added else citation_problem(raw_answer, retrieved)
    return {
        "answer": REFUSAL if problem else raw_answer,
        "raw_answer": raw_answer,  # what the model wrote, kept to show when the guardrail fired
        "guardrail": problem,      # None, or why the answer was replaced
        "tool_calls": tool_calls,
        "tool_results": tool_results,
        "retrieved": "\n\n".join(retrieved),
        "input_tokens": sum(u["input_tokens"] for u in usage),
        "output_tokens": sum(u["output_tokens"] for u in usage),
        "model_calls": len(usage),
        "seconds": round(seconds, 2),
    }


async def main(question: str) -> None:
    async with mcp_tools() as tools:
        result = await ask(question, build_agent(tools))
    if result["guardrail"]:
        print(f"[guardrail] replaced the answer ({result['guardrail']}). Original:\n{result['raw_answer']}\n",
              file=sys.stderr)
    print(result["answer"] or "(no answer)")
    sources = sorted(set(citations(result["answer"])))
    if sources:
        print("\nCitations:")
        for source, location in sources:
            print(f"  - {source}, {location}")
    print(f"\n({result['model_calls']} model calls, {result['input_tokens'] + result['output_tokens']} tokens, "
          f"{result['seconds']}s)", file=sys.stderr)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit('usage: python agent.py "your question"')
    asyncio.run(main(" ".join(sys.argv[1:])))
