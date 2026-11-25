"""
Assignment 3: the agent (`main.py ask "question"` runs `python agent.py "question"`).

Built like session 10's 07-own-harness/harness.py: LangChain `create_agent` on
Gemini, the tools of server.py over MCP, AGENTS.md as system prompt, and three
guardrails:
  1. approval: the person at the keyboard must say yes before add_document runs;
  2. a call limit, a hard stop for runaway loops;
  3. a numbers check: every figure in the answer must appear in a passage the
     search tool returned, or the answer is withheld (a seller repeats figures
     to clients, so an invented one is the costliest mistake). The rule is also
     in AGENTS.md, but a system instruction is not a guarantee (session 8), so
     the check is in code.

Every answer is stamped with the versions that produced it (model, prompt,
retrieval design) and logged to logs/requests.jsonl, so a bad answer can be
traced and reproduced (MLOps session: "Tracking an LLM application").

    uv run python main.py ask "What does Saia say about its 2026 capital spending?"
"""

import asyncio
import hashlib
import json
import re
import sys
import time
from contextlib import AsyncExitStack
from datetime import datetime, timezone
from pathlib import Path

from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware, wrap_tool_call
from langchain_core.messages import AIMessage, ToolMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from api_key import load_api_key
from langchain.mcp import MCPAdapter  # langchain.mcp is in beta and warns on import

ROOT = Path(__file__).resolve().parent
MODEL = "gemini-3.5-flash-lite"  # fast, cheap, generous free-tier quota
SERVER = ROOT / "server.py"
NEEDS_APPROVAL = {"add_document"}  # changes what every later answer is based on
REQUEST_LOG = ROOT / "logs" / "requests.jsonl"


def short_hash(text):
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:8]


def prompt_version():
    """A short fingerprint of AGENTS.md. Any change to the rules is a new version."""
    return short_hash((ROOT / "AGENTS.md").read_text(encoding="utf-8"))


def log_request(record):
    """Append one line per question: what was asked, what came back, which versions produced it."""
    REQUEST_LOG.parent.mkdir(exist_ok=True)
    with REQUEST_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


# 1. Tools: start server.py and wrap its tools as LangChain tools.
async def load_mcp_tools(stack):
    adapter = await stack.enter_async_context(MCPAdapter(SERVER))
    return await adapter.list_tools()


# 2. Guardrail around the tools: ask before add_document runs.
#    approval = "ask" (keyboard), "approve" or "deny" (for evaluation runs).
def approval_guardrail(approval):
    @wrap_tool_call
    async def ask_before_adding(request, handler):
        call = request.tool_call
        if call["name"] in NEEDS_APPROVAL:
            allowed = approval == "approve"
            if approval == "ask":
                answer = input(f"  Allow {call['name']}({call['args']})? [y/N] ")
                allowed = answer.strip().lower() == "y"
            if not allowed:
                return ToolMessage(
                    content="The user refused to add this document. Do not try to add it another way.",
                    tool_call_id=call["id"],
                    status="error",
                )
        return await handler(request)

    return ask_before_adding


# 3. The agent: model + tools + standing rules + guardrails.
def build_agent(tools, approval="ask"):
    return create_agent(
        model=ChatGoogleGenerativeAI(model=MODEL),
        tools=tools,
        system_prompt=(ROOT / "AGENTS.md").read_text(),
        middleware=[
            approval_guardrail(approval),
            ModelCallLimitMiddleware(run_limit=8),  # hard stop for runaway loops
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


# 4. Output guardrail: figures in the answer must appear in the retrieved passages.
def numbers_in(text):
    """Figures like 982.5, 17.0%, 1,234 or $2.1 billion, as plain digit strings."""
    text = re.sub(r"\[[^\]]*\]", " ", text)             # ignore citations [SAIA 10-K 2025, Item 7]
    text = re.sub(r"(?m)^\s*\d+[.)]\s", " ", text)       # ignore list numbering "1. "
    found = re.findall(r"\d[\d,]*(?:\.\d+)?", text)
    return {n.replace(",", "").rstrip(".") for n in found if len(n.replace(",", "")) >= 2}


def unsupported_numbers(answer, trace, question=""):
    """Figures in the answer that appear nowhere in what the agent was given:
    the tool results, the user's own question, and the file paths the user asked to add."""
    given = [line for line in trace if line.startswith(("result ", "call add_document"))]
    evidence = " ".join(given + [question]).replace(",", "")
    return sorted(n for n in numbers_in(answer) if n not in evidence)


async def ask(agent, question):
    """Run one question. Returns the answer, the tool trace and run statistics."""
    started = time.perf_counter()
    result = await agent.ainvoke({"messages": [{"role": "user", "content": question}]})
    seconds = time.perf_counter() - started

    messages = result["messages"]
    answer = messages[-1].text.strip()
    trace = tool_trace(messages)
    usage = [m.usage_metadata or {} for m in messages if isinstance(m, AIMessage)]
    stats = {
        "seconds": round(seconds, 1),
        "model_calls": len(usage),
        "input_tokens": sum(u.get("input_tokens", 0) for u in usage),
        "output_tokens": sum(u.get("output_tokens", 0) for u in usage),
        "guardrail": None,
        "model": MODEL,
        "prompt_version": prompt_version(),
    }

    missing = unsupported_numbers(answer, trace, question)
    if missing:
        stats["guardrail"] = {"unsupported_numbers": missing, "withheld_answer": answer}
        answer = ("Answer withheld: it contains figures that are not in the retrieved passages "
                  f"({', '.join(missing)}). Check the filings directly.")

    log_request({
        "time": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "question": question,
        "answer": answer,
        "tools": [line.split("(")[0].removeprefix("call ") for line in trace if line.startswith("call ")],
        **stats,
    })
    return answer, trace, stats


async def main(question):
    load_api_key()
    async with AsyncExitStack() as stack:
        agent = build_agent(await load_mcp_tools(stack))
        answer, trace, stats = await ask(agent, question)
    for line in trace:
        print(f"  {line[:160]}{'...' if len(line) > 160 else ''}")
    print()
    print(answer)
    print(f"\n({stats['seconds']}s, {stats['input_tokens'] + stats['output_tokens']} tokens)")


if __name__ == "__main__":
    asyncio.run(main(" ".join(sys.argv[1:]) or "What are Saia's main risk factors?"))
