"""
Assignment 3: the agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the tools of server.py over MCP and
AGENTS.md as system prompt. Guardrails:

  1. Human approval before add_document runs (console prompt; denied when nobody can answer).
  2. Call limits: at most MAX_TOOL_CALLS tool calls and MAX_MODEL_CALLS model calls per run.
  3. Citation validator (Phase 6 decision): every "<Regulation> Article N" in the answer must be
     a passage the search tool returned in this run, and a non-refusal must cite something.
     On a violation the model gets one retry with the problem spelled out; if it fails again the
     answer is withheld and replaced by the refusal.

For evaluate.py: `ask(question)` or, for many questions over one MCP session, `ask_many(questions)`.
Both return dicts with the answer, the tool trace, the retrieved passages, tokens and seconds.
"""

from __future__ import annotations

import asyncio
import re
import sys
import time
from pathlib import Path
from typing import Callable

from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware, ToolCallLimitMiddleware
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.tools import StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from api_key import load_api_key
from retrieval import article_key

ROOT = Path(__file__).resolve().parent
MODEL = "gemini-3.5-flash-lite"          # Phase 6 decision 8 (judge uses a different model)
MAX_TOOL_CALLS = 6
MAX_MODEL_CALLS = 10
TRANSIENT_RETRIES = 4                     # free-tier 503 "high demand" / 429: wait and retry the question
REFUSAL = "The indexed legislation does not cover this question."
REGULATIONS = r"GDPR|AI Act|Data Act|NIS2"
CITATION = re.compile(rf"\b({REGULATIONS})\s*,?\s+((?:Article|Art\.?)\s*\d+[a-z]?|Annex\s+[IVXLC]+)\b")
RETRIEVED = re.compile(rf"^\[\d+\]\s+({REGULATIONS})\s+((?:Article|Annex)\s+.+?)\s+\((?:similarity|keyword)", re.M)

sys.stdout.reconfigure(encoding="utf-8")


# ---------------------------------------------------------------- approval

def console_approver(tool: str, args: dict) -> bool:
    """Ask the person at the terminal. Without a terminal (evaluation, CI) the answer is no."""
    if not sys.stdin or not sys.stdin.isatty():
        print(f"[approval] {tool}({args}) denied: no one at the terminal to approve it.", file=sys.stderr)
        return False
    try:
        reply = input(f"\nThe agent wants to run {tool}({args}).\nThis changes the index. Approve? [y/N] ")
    except (EOFError, KeyboardInterrupt):   # no usable terminal: fail closed
        print(f"\n[approval] {tool}({args}) denied: no answer.", file=sys.stderr)
        return False
    return reply.strip().lower() in ("y", "yes", "s", "si", "sí")


# ---------------------------------------------------------------- MCP tools as LangChain tools

def mcp_tools(session: ClientSession, specs, approver: Callable[[str, dict], bool], events: list) -> list:
    """Wrap each MCP tool of server.py as a LangChain tool; add_document asks for approval first."""
    tools = []
    for spec in specs:
        async def call(_name=spec.name, **kwargs):
            if _name == "add_document":
                if not approver(_name, kwargs):
                    events.append({"guardrail": "approval", "fired": True, "detail": f"denied {kwargs}"})
                    return "The user did not approve add_document. Nothing was added; tell the user."
                events.append({"guardrail": "approval", "fired": False, "detail": f"approved {kwargs}"})
            result = await session.call_tool(_name, kwargs)
            return "\n".join(getattr(c, "text", "") for c in result.content)
        tools.append(StructuredTool.from_function(coroutine=call, name=spec.name,
                                                  description=spec.description or "", args_schema=spec.input_schema))
    return tools


# ---------------------------------------------------------------- citation validator

def text_of(message: AIMessage) -> str:
    content = message.content
    if isinstance(content, str):
        return content
    return "".join(p.get("text", "") if isinstance(p, dict) else str(p) for p in content)


def retrieved_passages(messages) -> set[tuple[str, str]]:
    """(regulation, 'Article N' / 'Annex X') of every passage the search tool returned."""
    found = set()
    for m in messages:
        if isinstance(m, ToolMessage) and m.name == "search":
            for doc, loc in RETRIEVED.findall(m.content if isinstance(m.content, str) else str(m.content)):
                found.add((doc, article_key(loc)))
    return found


def cited_passages(answer: str) -> set[tuple[str, str]]:
    return {(doc, article_key(loc)) for doc, loc in CITATION.findall(answer)}


def is_refusal(answer: str) -> bool:
    return REFUSAL.lower().rstrip(".") in answer.lower()


def validate(answer: str, retrieved: set, searched: bool = True) -> list[str]:
    """Problems with the answer's citations; empty list = OK.

    The "must cite something" rule only applies to legal answers, i.e. runs that searched
    (a reply about an add_document request has nothing to cite).
    """
    cited = cited_passages(answer)
    problems = [f"{d} {a} was cited but not returned by search" for d, a in sorted(cited - retrieved)]
    if searched and not cited and not is_refusal(answer):
        problems.append("the answer makes claims without any citation")
    return problems


def searched(messages) -> bool:
    return any(isinstance(m, ToolMessage) and m.name == "search" for m in messages)


# ---------------------------------------------------------------- running the agent

def build_agent(tools: list):
    model = ChatGoogleGenerativeAI(model=MODEL, api_key=load_api_key(), max_retries=6)  # fixed sampling: no temperature
    return create_agent(
        model, tools,
        system_prompt=(ROOT / "AGENTS.md").read_text(encoding="utf-8"),
        middleware=[ToolCallLimitMiddleware(run_limit=MAX_TOOL_CALLS, exit_behavior="continue"),
                    ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS, exit_behavior="end")],
    )


def usage(messages) -> dict:
    tokens = {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}
    for m in messages:
        if isinstance(m, AIMessage) and m.usage_metadata:
            for k in tokens:
                tokens[k] += m.usage_metadata.get(k, 0) or 0
    return tokens


async def run_one(agent, question: str, events: list) -> dict:
    started = time.time()
    first_event = len(events)
    result = await agent.ainvoke({"messages": [HumanMessage(question)]})
    messages = result["messages"]
    answer = text_of(messages[-1]) if isinstance(messages[-1], AIMessage) else ""
    retrieved = retrieved_passages(messages)
    problems = validate(answer, retrieved, searched(messages))
    guardrail = {"guardrail": "citations", "fired": bool(problems), "detail": "; ".join(problems)}

    if problems:   # one retry, telling the model exactly what was wrong
        correction = ("Your answer failed the citation check: " + "; ".join(problems) + ". Rewrite it citing only "
                      "passages returned by the search tool in this conversation (search again if needed), "
                      f"or reply with the refusal sentence: \"{REFUSAL}\"")
        result = await agent.ainvoke({"messages": messages + [HumanMessage(correction)]})
        messages = result["messages"]
        answer = text_of(messages[-1]) if isinstance(messages[-1], AIMessage) else ""
        retrieved = retrieved_passages(messages)
        still = validate(answer, retrieved, searched(messages))
        guardrail["retry_ok"] = not still
        if still:
            answer = (f"{REFUSAL} (Answer withheld by the citation check: {'; '.join(still)}.) "
                      "Please check the legislation directly or consult a lawyer.")
    events.append(guardrail)

    trace = []
    for m in messages:
        if isinstance(m, AIMessage):
            for call in m.tool_calls:
                trace.append({"tool": call["name"], "args": call["args"]})
    return {
        "question": question,
        "answer": answer.strip(),
        "refused": is_refusal(answer),
        "citations": sorted(f"{d} {a}" for d, a in cited_passages(answer)),
        "retrieved": sorted(f"{d} {a}" for d, a in retrieved),
        "retrieved_text": "\n\n".join(m.content for m in messages if isinstance(m, ToolMessage) and m.name == "search"),
        "trace": trace,
        "tool_calls": len(trace),
        "guardrails": events[first_event:],
        **usage(messages),
        "seconds": round(time.time() - started, 2),
    }


async def ask_many(questions: list[str], approver: Callable[[str, dict], bool] = console_approver,
                   on_result: Callable[[dict], None] | None = None) -> list[dict]:
    """Answer several questions over one MCP session (the server loads the index once)."""
    params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT))
    out = []
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            specs = (await session.list_tools()).tools
            for q in questions:
                for attempt in range(TRANSIENT_RETRIES + 1):
                    events: list = []
                    agent = build_agent(mcp_tools(session, specs, approver, events))
                    try:
                        r = await run_one(agent, q, events)
                        break
                    except Exception as e:  # noqa: BLE001 - only overloads / rate limits are retried
                        if attempt == TRANSIENT_RETRIES or not any(c in str(e) for c in ("503", "504", "429", "UNAVAILABLE")):
                            raise
                        wait = 30 * (attempt + 1)
                        print(f"[agent] model busy ({str(e)[:60]}...), retrying in {wait}s", file=sys.stderr, flush=True)
                        await asyncio.sleep(wait)
                out.append(r)
                if on_result:
                    on_result(r)
    return out


def ask(question: str, approver: Callable[[str, dict], bool] = console_approver) -> dict:
    return asyncio.run(ask_many([question], approver))[0]


def main() -> int:
    if len(sys.argv) < 2:
        print('Usage: python agent.py "your question"', file=sys.stderr)
        return 2
    r = ask(" ".join(sys.argv[1:]))
    print(r["answer"])
    print("\nCitations: " + (", ".join(r["citations"]) if r["citations"] else "none"))
    fired = [g for g in r["guardrails"] if g["fired"]]
    for g in fired:
        print(f"[guardrail {g['guardrail']}] {g['detail']}")
    print(f"\n({r['tool_calls']} tool calls, {r['total_tokens']} tokens, {r['seconds']} s)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
