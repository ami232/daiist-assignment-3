"""
Assignment 3: the caregiver's assistant (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with server.py's tools over MCP and
AGENTS.md as system prompt. Guardrails, all enforced by the harness (the model
cannot skip them):
  1. Approval: add_document runs only after the person at the keyboard says yes.
  2. Limits: at most 6 model calls and 4 searches per question.
  3. Citation check: every citation in the answer must be one the search tool
     actually returned. An answer with no valid citation (and no refusal) or with
     an invented citation is withheld and replaced with a safe refusal.

`run_question()` returns the answer, tool trace, tokens and seconds for evaluate.py.
"""

import asyncio
import re
import sys
import time
import warnings
from contextlib import AsyncExitStack
from pathlib import Path

warnings.filterwarnings("ignore")  # langchain.mcp beta notice; keeps CLI output readable

from langchain.agents import create_agent  # noqa: E402
from langchain.agents.middleware import (ModelCallLimitMiddleware,  # noqa: E402
                                         ToolCallLimitMiddleware, wrap_tool_call)
from langchain.mcp import MCPAdapter  # noqa: E402
from langchain_core.messages import AIMessage, ToolMessage  # noqa: E402
from langchain_google_genai import ChatGoogleGenerativeAI  # noqa: E402

from api_key import load_api_key  # noqa: E402

ROOT = Path(__file__).resolve().parent
MODEL = "gemini-3.5-flash-lite"
NEEDS_APPROVAL = {"add_document"}
REFUSAL = "The product information I have does not cover this"
WITHHELD = (REFUSAL + " reliably: I could not check my answer against the official documents, "
            "so I am not giving it. Please ask a doctor or pharmacist.")
CITATION = re.compile(r"\[[a-z0-9_-]+ \| (?:SmPC|Package leaflet) \|[^\]]*\]")


async def load_tools(stack: AsyncExitStack):
    adapter = await stack.enter_async_context(MCPAdapter(ROOT / "server.py"))
    return await adapter.list_tools()


def approval_guardrail(auto_approve: bool):
    @wrap_tool_call
    async def ask_before_adding(request, handler):
        call = request.tool_call
        if call["name"] in NEEDS_APPROVAL and not auto_approve:
            allowed = False
            if sys.stdin.isatty():
                answer = input(f"\n  Allow {call['name']}({call['args']})? This changes the index. [y/N] ")
                allowed = answer.strip().lower() == "y"
            if not allowed:
                return ToolMessage(
                    content="The user did not approve adding this document. Do not retry; "
                            "tell the user it was not added.",
                    tool_call_id=call["id"], status="error")
        return await handler(request)
    return ask_before_adding


def build_agent(tools, auto_approve: bool = False):
    return create_agent(
        model=ChatGoogleGenerativeAI(model=MODEL, api_key=load_api_key()),
        tools=tools,
        system_prompt=(ROOT / "AGENTS.md").read_text(),
        middleware=[
            approval_guardrail(auto_approve),
            ModelCallLimitMiddleware(run_limit=6),
            ToolCallLimitMiddleware(tool_name="search", run_limit=4),
        ],
    )


def normalise(citation: str) -> str:
    return re.sub(r"\s+", " ", citation.strip().lower())


def check_citations(answer: str, retrieved: str) -> dict:
    """Guardrail 3, in code: are the answer's citations ones the tool returned?"""
    valid = {normalise(c) for c in CITATION.findall(retrieved)}
    cited = CITATION.findall(answer)
    invalid = [c for c in cited if normalise(c) not in valid]
    refused = REFUSAL.lower() in answer.lower()
    fired = bool(invalid) or (not cited and not refused)
    return {"cited": cited, "invalid_citations": invalid, "refused": refused, "guardrail_fired": fired}


def summarise(messages) -> dict:
    trace, retrieved, tokens = [], [], {"input": 0, "output": 0}
    for m in messages:
        if isinstance(m, AIMessage):
            trace += [f"call {c['name']}({c['args']})" for c in m.tool_calls]
            usage = m.usage_metadata or {}
            tokens["input"] += usage.get("input_tokens", 0)
            tokens["output"] += usage.get("output_tokens", 0)
        elif isinstance(m, ToolMessage):
            trace.append(f"result {m.text[:200]}...")
            retrieved.append(m.text)
    return {"trace": trace, "retrieved": "\n\n".join(retrieved), "tokens": tokens}


async def run_question(agent, question: str) -> dict:
    start = time.perf_counter()
    result = await agent.ainvoke({"messages": [{"role": "user", "content": question}]})
    info = summarise(result["messages"])
    raw = result["messages"][-1].text or ""
    check = check_citations(raw, info["retrieved"])
    adding = any(t.startswith("call add_document") for t in info["trace"])
    if check["guardrail_fired"] and not adding:
        answer = WITHHELD
    else:
        answer = raw
    return {"question": question, "answer": answer, "raw_answer": raw, **check, **info,
            "seconds": round(time.perf_counter() - start, 2)}


async def main(question: str) -> None:
    async with AsyncExitStack() as stack:
        agent = build_agent(await load_tools(stack))
        result = await run_question(agent, question)
    for line in result["trace"]:
        print(f"  {line[:160]}")
    if result["guardrail_fired"]:
        print(f"  [citation guardrail fired; withheld answer: {result['raw_answer'][:300]!r}]")
    print()
    print(result["answer"])
    t = result["tokens"]
    print(f"\n({t['input']} input + {t['output']} output tokens, {result['seconds']} s)")


if __name__ == "__main__":
    asyncio.run(main(" ".join(sys.argv[1:]) or "What should I do if my mother misses an Eliquis dose?"))
