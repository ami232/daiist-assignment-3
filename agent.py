"""
Assignment 3: the agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the tools of server.py reached over MCP
(stdio) and AGENTS.md as the system prompt.

Controls:
  * approval: HumanInTheLoopMiddleware pauses before every add_document call; a
    person approves or rejects it at the terminal. Without a terminal (evaluation,
    check.py) the call is rejected automatically.
  * limits: at most MAX_SEARCHES search calls and MAX_MODEL_CALLS model calls per question.
  * guardrail (citation check): every citation in the answer must match a passage
    that search actually returned in this run. If not, the model gets one
    corrective retry; if it still fails, the answer is replaced by a refusal.

`run(question)` returns the answer plus the trace (tool calls, retrieved
citations, guardrail events, tokens, seconds) for evaluate.py.
"""

from __future__ import annotations

import asyncio
import datetime as dt
import json
import os
import re
import sys
import time
import uuid
import warnings
from pathlib import Path
from zoneinfo import ZoneInfo

from langchain.agents import create_agent
from langchain.agents.middleware import (HumanInTheLoopMiddleware, ModelCallLimitMiddleware, ModelFallbackMiddleware,
                                         ToolCallLimitMiddleware)
from langchain_core.callbacks import BaseCallbackHandler
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_core.tools import StructuredTool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
AGENTS_MD = ROOT / "AGENTS.md"
# Free tier (checked in AI Studio on 2026-11-20): the Flash models allow only 20 requests/day,
# the Flash-Lite models 15 RPM / 250k TPM / 500 RPD. gemini-3.5-flash-lite is the agent model;
# gemini-3.1-flash-lite is used only if it keeps failing (and is the default judge in evaluate.py).
MODEL = os.environ.get("GEMINI_CHAT_MODEL", "gemini-3.5-flash-lite")
FALLBACK_MODEL = os.environ.get("GEMINI_FALLBACK_MODEL", "gemini-3.1-flash-lite")
CHAT_RPM = int(os.environ.get("GEMINI_CHAT_RPM", "10"))                     # limit 15: keep a margin
CHAT_DAILY_BUDGET = int(os.environ.get("GEMINI_CHAT_DAILY_BUDGET", "450"))  # limit 500 per model
CHAT_USAGE_FILE = ROOT / "corpus" / "chat_usage.json"  # local request count per model and day (git-ignored)
MAX_SEARCHES = 6
MAX_MODEL_CALLS = 8
REFUSAL_PREFIX = "NOT IN CORPUS"
# [SOURCE | section > subsection | p. 12]  (as printed by server.py's search)
CITATION_RE = re.compile(r"\[([A-Z][A-Z0-9-]+) \| ([^\]|]+?) \| p\. ([^\]|]+?)\]")
# two citations merged in one bracket: "[A | x | p. 1, B | y | p. 2]" -> "[A | x | p. 1] [B | y | p. 2]"
MERGED_SPLIT_RE = re.compile(r"\s*[,;]\s*(?=[A-Z][A-Z0-9-]+ \| [^\]|]+ \| p\. )")
RESULT_RE = re.compile(r"^\[\d+\] \[([A-Z][A-Z0-9-]+) \| (.+?) \| p\. (.+?)\]", re.M)


def log(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


# --------------------------------------------------------------------------- MCP bridge

async def mcp_tools(session: ClientSession) -> list[StructuredTool]:
    """Expose every tool of the MCP server as a LangChain tool (name, description
    and argument schema come from the server)."""
    tools = []
    for spec in (await session.list_tools()).tools:
        async def call(_name: str = spec.name, **kwargs) -> str:
            result = await session.call_tool(_name, kwargs)
            text = "\n".join(getattr(c, "text", "") for c in result.content).strip()
            if getattr(result, "is_error", False) or getattr(result, "isError", False):
                return f"ERROR: {text}"
            return text
        tools.append(StructuredTool(name=spec.name, description=spec.description or "",
                                    args_schema=spec.input_schema, coroutine=call))
    return tools


# --------------------------------------------------------------------------- guardrail

def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("…", "")).strip().lower()


def retrieved_citations(messages: list) -> set[tuple[str, str, str]]:
    found = set()
    for m in messages:
        if isinstance(m, ToolMessage) and m.name == "search":
            found |= {(s, _norm(l), _norm(p)) for s, l, p in RESULT_RE.findall(str(m.content))}
    return found


def split_merged_citations(answer: str) -> str:
    """Split brackets that hold several citations so each one is parsed and verified
    (otherwise CITATION_RE skips the whole bracket and it escapes the check)."""
    return re.sub(r"\[[A-Z][A-Z0-9-]+ \|[^\[\]]*\]", lambda m: MERGED_SPLIT_RE.sub("] [", m.group(0)), answer)


def find_citations(answer: str) -> list[tuple[str, str, str]]:
    return CITATION_RE.findall(split_merged_citations(answer))


def check_citations(answer: str, retrieved: set[tuple[str, str, str]]) -> dict:
    """Valid if every citation names a retrieved (source, page) and its location is the
    retrieved one or a shortened form of it. Refusals need no citation."""
    cited = find_citations(answer)
    refusal = answer.strip().upper().startswith(REFUSAL_PREFIX)
    invalid = []
    for s, l, p in cited:
        ok = any(s == rs and _norm(p) == rp and (_norm(l) in rl or rl in _norm(l)) for rs, rl, rp in retrieved)
        if not ok:
            invalid.append(f"[{s} | {l} | p. {p}]")
    problem = None
    if invalid:
        problem = f"these citations do not match any search result: {', '.join(invalid)}"
    elif not cited and not refusal:
        problem = "the answer has no citation"
    return {"ok": problem is None, "problem": problem, "cited": len(cited), "refusal": refusal}


# --------------------------------------------------------------------------- agent

def build_agent(model, tools, fallback=None):
    middleware = [
        HumanInTheLoopMiddleware(interrupt_on={"add_document": True},
                                 description_prefix="add_document modifies the index and requires approval"),
        ToolCallLimitMiddleware(tool_name="search", run_limit=MAX_SEARCHES, exit_behavior="continue"),
        ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS, exit_behavior="end"),
    ]
    if fallback is not None:  # the client already retries transient errors; then try the fallback model
        middleware.append(ModelFallbackMiddleware(fallback))
    return create_agent(model, tools=tools, system_prompt=AGENTS_MD.read_text(encoding="utf-8"),
                        middleware=middleware, checkpointer=InMemorySaver())


class DailyBudget(BaseCallbackHandler):
    """Counts chat requests per model and Pacific day (the quota resets at PT midnight) and
    stops before the free-tier daily limit is reached."""

    raise_error = True  # LangChain swallows callback errors unless this is set

    def __init__(self, model: str):
        self.model = model

    def on_chat_model_start(self, serialized, messages, **kwargs) -> None:
        day = dt.datetime.now(ZoneInfo("America/Los_Angeles")).date().isoformat()
        usage = json.loads(CHAT_USAGE_FILE.read_text()) if CHAT_USAGE_FILE.is_file() else {}
        used = usage.get(day, {}).get(self.model, 0)
        if used >= CHAT_DAILY_BUDGET:
            raise RuntimeError(f"RESOURCE_EXHAUSTED: local daily budget of {CHAT_DAILY_BUDGET} requests per day "
                               f"reached for {self.model} ({CHAT_USAGE_FILE.name})")
        usage.setdefault(day, {})[self.model] = used + 1
        CHAT_USAGE_FILE.parent.mkdir(parents=True, exist_ok=True)
        CHAT_USAGE_FILE.write_text(json.dumps(usage, indent=2))


_LIMITERS: dict[str, InMemoryRateLimiter] = {}
# Flash-Lite 3.5 ignores temperature (fixed sampling): answers are not deterministic, which is
# why evaluate.py caches every answer. The repeated warning is silenced.
warnings.filterwarnings("ignore", message=".*uses fixed sampling defaults.*")


def chat_model(name: str, reasoning_effort: str | None = "low"):
    """Gemini chat model with a per-model request limiter (CHAT_RPM) and the daily budget."""
    from langchain_google_genai import ChatGoogleGenerativeAI

    load_api_key()
    limiter = _LIMITERS.setdefault(name, InMemoryRateLimiter(requests_per_second=CHAT_RPM / 60,
                                                             check_every_n_seconds=0.2, max_bucket_size=1))
    # Extractive answering needs little "thinking"; low effort cut latency from ~100 s to ~3 s in a test.
    extra = {"reasoning_effort": reasoning_effort} if reasoning_effort else {}
    return ChatGoogleGenerativeAI(model=name, temperature=0, timeout=90, max_retries=2, rate_limiter=limiter,
                                  callbacks=[DailyBudget(name)], **extra)


def default_model():
    return chat_model(MODEL)


def terminal_approval(request: dict) -> dict:
    """Ask a person at the terminal; without a terminal, reject."""
    print(f"\nApproval needed: {request['name']}({json.dumps(request['args'])})", file=sys.stderr)
    if not sys.stdin.isatty():
        print("  no terminal to ask: rejected automatically", file=sys.stderr)
        return {"type": "reject", "message": "Rejected: no human available to approve add_document."}
    answer = input("  Approve? [y/N] ").strip().lower()
    if answer in {"y", "yes"}:
        return {"type": "approve"}
    return {"type": "reject", "message": "The user rejected adding this document."}


def _final_text(messages: list) -> str:
    for m in reversed(messages):
        if isinstance(m, AIMessage) and not m.tool_calls:
            content = m.content
            if isinstance(content, list):
                content = "".join(part.get("text", "") if isinstance(part, dict) else str(part) for part in content)
            if str(content).strip():
                return str(content).strip()
    return ""


async def run_async(question: str, approve=terminal_approval, model=None, server_env: dict | None = None) -> dict:
    started = time.perf_counter()
    params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT),
                                   env={**os.environ, **(server_env or {})})
    events: list[dict] = []
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            agent = build_agent(model or default_model(), await mcp_tools(session),
                                fallback=None if model is not None else chat_model(FALLBACK_MODEL))
            config = {"configurable": {"thread_id": str(uuid.uuid4())}}
            state = await agent.ainvoke({"messages": [HumanMessage(question)]}, config)
            while state.get("__interrupt__"):  # approval step(s) for add_document
                decisions = []
                for request in state["__interrupt__"][0].value["action_requests"]:
                    decision = approve(request)
                    decisions.append(decision)
                    events.append({"event": "approval", "tool": request["name"], "args": request["args"],
                                   "decision": decision["type"]})
                state = await agent.ainvoke(Command(resume={"decisions": decisions}), config)

            answer = _final_text(state["messages"])
            check = check_citations(answer, retrieved_citations(state["messages"]))
            if not check["ok"]:  # guardrail: one corrective retry
                events.append({"event": "guardrail", "problem": check["problem"], "action": "retry"})
                state = await agent.ainvoke({"messages": [HumanMessage(
                    f"GUARDRAIL: {check['problem']}. Rewrite the answer using only facts and citations that appear "
                    f"in the search results above (copy each citation exactly), or reply starting with "
                    f"'{REFUSAL_PREFIX}:' if the results do not support an answer.")]}, config)
                answer = _final_text(state["messages"])
                check = check_citations(answer, retrieved_citations(state["messages"]))
                if not check["ok"]:
                    events.append({"event": "guardrail", "problem": check["problem"], "action": "replaced by refusal"})
                    answer = (f"{REFUSAL_PREFIX}: I could not produce an answer whose every claim is backed by a "
                              "verifiable citation from the corpus.")

    messages = state["messages"]
    tool_calls = [{"tool": c["name"], "args": c["args"]} for m in messages if isinstance(m, AIMessage) for c in m.tool_calls]
    usage = [m.usage_metadata for m in messages if isinstance(m, AIMessage) and m.usage_metadata]
    return {
        "question": question,
        "answer": answer,
        "citations": [f"[{s} | {l} | p. {p}]" for s, l, p in find_citations(answer)],
        "refusal": answer.upper().startswith(REFUSAL_PREFIX),  # full refusal
        # partial refusal: answers some parts, then a separate "NOT IN CORPUS:" line (AGENTS.md rule 3)
        "partial_refusal": (not answer.upper().startswith(REFUSAL_PREFIX))
                           and re.search(rf"(?m)^\s*{REFUSAL_PREFIX}:", answer) is not None,
        "tool_calls": tool_calls,
        "retrieved": [str(m.content) for m in messages if isinstance(m, ToolMessage) and m.name == "search"],
        "events": events,
        "model_calls": sum(isinstance(m, AIMessage) for m in messages),
        "input_tokens": sum(u.get("input_tokens", 0) for u in usage),
        "output_tokens": sum(u.get("output_tokens", 0) for u in usage),
        "seconds": round(time.perf_counter() - started, 2),
        "model": getattr(model, "model", None) or MODEL,
        # which model actually produced each turn (the fallback may have answered)
        "models_used": sorted({str(m.response_metadata.get("model_name", "")) for m in messages
                               if isinstance(m, AIMessage) and m.response_metadata.get("model_name")}),
    }


def run(question: str, **kwargs) -> dict:
    return asyncio.run(run_async(question, **kwargs))


def main() -> None:
    question = " ".join(sys.argv[1:]).strip()
    if not question:
        raise SystemExit('usage: python agent.py "your question"')
    result = run(question)
    print(result["answer"])
    if result["citations"]:
        print("\nCitations:")
        for c in dict.fromkeys(result["citations"]):
            print(f"  {c}")
    searches = sum(t["tool"] == "search" for t in result["tool_calls"])
    print(f"\n[{searches} search call(s), {result['model_calls']} model call(s), "
          f"{result['input_tokens']}+{result['output_tokens']} tokens, {result['seconds']}s]")
    for e in result["events"]:
        print(f"[{e['event']}: {e.get('problem') or e.get('decision')} -> {e.get('action', e.get('tool'))}]")


if __name__ == "__main__":
    main()
