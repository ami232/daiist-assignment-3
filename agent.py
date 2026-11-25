"""
Assignment 3: the agent harness (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the tools of server.py loaded over
MCP (stdio) and AGENTS.md as the system prompt.

Guardrails:
- approval: HumanInTheLoopMiddleware interrupts before `add_document`; the
  user approves or rejects at the terminal. Without a terminal (evaluation,
  check.py) the call is rejected.
- call limits: at most MAX_SEARCHES tool calls and MAX_MODEL_CALLS model calls per question.
- citation check (extra guardrail): every citation in the answer must match
  a passage the search tool actually returned in this run. Citations that do
  not are removed and flagged; an answer left with no valid citation that is
  not a refusal is replaced by the refusal.

`answer(question)` returns the answer, the tool trace, tokens and seconds, for evaluate.py.
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

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
# gemini-3.5-flash allows only 20 requests a day on the free tier: too few for
# 30+ questions at 2-3 model calls each, so the agent runs on flash-lite.
CHAT_MODEL = os.environ.get("GEMINI_CHAT_MODEL", "gemini-3.5-flash-lite")
FALLBACK_MODEL = os.environ.get("GEMINI_FALLBACK_MODEL", "gemini-3.1-flash-lite")
MAX_SEARCHES = 4
MAX_MODEL_CALLS = 8
REFUSAL = "The corpus does not cover this."

CITATION = re.compile(r"\[([A-Za-z0-9][\w.-]*),\s*p\.\s*([^\]]+?)\]")
RESULT_HEADER = re.compile(r"^Result \d+ \[([^,\]]+), p\. ([^\]]+)\]", re.M)


# --------------------------------------------------------------------------- #
# MCP tools as LangChain tools
# --------------------------------------------------------------------------- #

@asynccontextmanager
async def mcp_tools():
    """Start server.py over stdio and expose its tools as LangChain StructuredTools."""
    from langchain_core.tools import StructuredTool
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    params = StdioServerParameters(command=sys.executable, args=[str(ROOT / "server.py")], cwd=str(ROOT))
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = []
            for t in (await session.list_tools()).tools:
                async def call(_name=t.name, **kwargs) -> str:
                    result = await session.call_tool(_name, kwargs)
                    return "\n".join(getattr(c, "text", "") for c in result.content)
                tools.append(StructuredTool.from_function(
                    coroutine=call, name=t.name, description=t.description or "",
                    args_schema=t.input_schema,
                ))
            yield tools


# --------------------------------------------------------------------------- #
# Citation guardrail
# --------------------------------------------------------------------------- #

def _page_key(page: str) -> tuple[int, int] | None:
    m = re.fullmatch(r"\s*(\d+)-(\d+)\s*", page)
    return (int(m.group(1)), int(m.group(2))) if m else None


def page_in_span(cited: str, span: str) -> bool:
    """'11-4' is in '11-3 to 11-5'; exact text match otherwise."""
    cited, span = cited.strip(), span.strip()
    if cited == span:
        return True
    ends = [s.strip() for s in span.split(" to ")]
    c, lo, hi = _page_key(cited), _page_key(ends[0]), _page_key(ends[-1])
    return bool(c and lo and hi and lo <= c <= hi)


def retrieved_citations(trace: list[dict]) -> list[tuple[str, str]]:
    out = []
    for step in trace:
        if step["tool"] == "search":
            out += RESULT_HEADER.findall(step.get("result", ""))
    return out


def is_refusal(text: str) -> bool:
    return text.strip().lower().startswith(REFUSAL.lower().rstrip("."))


def cited_pages(pages: str) -> list[str]:
    """'11-7, 11-18' or '11-7 and 11-8' -> each page; '11-3 to 11-4' stays one span."""
    return [p.strip() for p in re.split(r",|;|\band\b", pages) if p.strip()]


def citation_is_valid(source: str, pages: str, retrieved: list[tuple[str, str]]) -> bool:
    """Every page in the citation must lie in a passage retrieved from that source."""
    return all(any(source == rs and page_in_span(p, rp) for rs, rp in retrieved) for p in cited_pages(pages))


def check_citations(answer_text: str, trace: list[dict]) -> tuple[str, dict]:
    """Remove citations that match no retrieved passage; refuse if nothing valid remains.

    v1 compared '[src, p. 11-7, 11-18]' as one page and rejected it, which once
    turned a correct answer (q25) into a refusal; each page is now checked.
    """
    retrieved = retrieved_citations(trace)
    matches = list(CITATION.finditer(answer_text))
    valid = [m for m in matches if citation_is_valid(m.group(1), m.group(2), retrieved)]
    invalid = [m for m in matches if m not in valid]
    report = {"cited": len(matches), "valid": len(valid), "invalid": [m.group(0) for m in invalid],
              "fired": False, "action": ""}
    text = answer_text
    tools = {t["tool"] for t in trace}
    if "add_document" in tools and "search" not in tools:
        return text, report   # an add-document turn makes no factual claims to check
    if invalid:
        report["fired"] = True
        report["action"] = "removed invalid citations"
        for m in invalid:
            text = text.replace(m.group(0), "[citation removed: not in retrieved passages]")
    if not is_refusal(text) and not valid:
        report["fired"] = True
        report["action"] = "no valid citation: replaced answer with refusal"
        text = (f"{REFUSAL} I could not find a retrieved passage that supports an answer, "
                f"so I will not guess. Check your POH/AFM or ask a flight instructor.")
    return text, report


# --------------------------------------------------------------------------- #
# Agent
# --------------------------------------------------------------------------- #

def approve_interactively(action: dict) -> bool:
    if not sys.stdin or not sys.stdin.isatty():
        print(f"[approval] {action['name']}({action.get('args')}) rejected: no terminal to ask.", file=sys.stderr)
        return False
    reply = input(f"\nThe agent wants to run {action['name']}({action.get('args')}). Approve? [y/N] ")
    return reply.strip().lower() in {"y", "yes"}


def _text(message) -> str:
    content = getattr(message, "content", "")
    if isinstance(content, str):
        return content
    return "".join(p.get("text", "") if isinstance(p, dict) else str(p) for p in content)


class Harness:
    """One MCP server and one agent, reused across questions (evaluate.py asks many)."""

    def __init__(self, approve=approve_interactively, model: str = CHAT_MODEL):
        self.approve = approve
        self.model_name = model
        self._cm = None

    async def __aenter__(self):
        from langchain.agents import create_agent
        from langchain.agents.middleware import (
            HumanInTheLoopMiddleware, ModelCallLimitMiddleware, ModelFallbackMiddleware,
            ModelRetryMiddleware, ToolCallLimitMiddleware,
        )
        from langchain_google_genai import ChatGoogleGenerativeAI
        from langgraph.checkpoint.memory import InMemorySaver

        load_api_key()
        self._cm = mcp_tools()
        tools = await self._cm.__aenter__()
        def chat(name):
            # SDK retries off (retries=1 means a single attempt) so ModelRetry and the
            # fallback below decide; otherwise 503s stack into many-minute waits.
            return ChatGoogleGenerativeAI(model=name, retries=1, request_timeout=90)
        model = chat(self.model_name)
        self.agent = create_agent(
            model,
            tools,
            system_prompt=(ROOT / "AGENTS.md").read_text(encoding="utf-8"),
            middleware=[
                HumanInTheLoopMiddleware(interrupt_on={"add_document": True}),
                ToolCallLimitMiddleware(run_limit=MAX_SEARCHES, exit_behavior="continue"),
                ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS, exit_behavior="end"),
                # Free-tier models often answer 503 "high demand": retry, then fall back.
                ModelFallbackMiddleware(chat(FALLBACK_MODEL)),
                ModelRetryMiddleware(max_retries=2, initial_delay=5.0, backoff_factor=2.0, on_failure="error"),
            ],
            checkpointer=InMemorySaver(),
        )
        return self

    async def __aexit__(self, *exc):
        await self._cm.__aexit__(*exc)

    async def answer(self, question: str) -> dict:
        from langchain_core.messages import AIMessage, ToolMessage
        from langgraph.types import Command

        started = time.time()
        config = {"configurable": {"thread_id": str(uuid.uuid4())}, "recursion_limit": 40}
        payload = {"messages": [{"role": "user", "content": question}]}
        approvals = []
        while True:
            state = await self.agent.ainvoke(payload, config=config)
            interrupts = state.get("__interrupt__") or []
            if not interrupts:
                break
            decisions = []
            for action in interrupts[0].value.get("action_requests", []):
                ok = self.approve(action)
                approvals.append({"tool": action["name"], "args": action.get("args"), "approved": ok})
                decisions.append({"type": "approve"} if ok else
                                 {"type": "reject", "message": "The user did not approve adding this document."})
            payload = Command(resume={"decisions": decisions})

        messages = state["messages"]
        trace, calls, models_used = [], {}, []
        tokens = {"input": 0, "output": 0, "total": 0}
        for m in messages:
            if isinstance(m, AIMessage):
                name = (getattr(m, "response_metadata", None) or {}).get("model_name")
                if name and name not in models_used:
                    models_used.append(name)
                for tc in m.tool_calls or []:
                    calls[tc["id"]] = {"tool": tc["name"], "args": tc["args"]}
                usage = getattr(m, "usage_metadata", None) or {}
                tokens["input"] += usage.get("input_tokens", 0)
                tokens["output"] += usage.get("output_tokens", 0)
                tokens["total"] += usage.get("total_tokens", 0)
            elif isinstance(m, ToolMessage):
                step = calls.get(m.tool_call_id, {"tool": m.name, "args": {}})
                trace.append({**step, "result": _text(m)})
        final = next((m for m in reversed(messages) if isinstance(m, AIMessage) and _text(m).strip()), None)
        raw = _text(final).strip() if final else ""
        if not raw:
            raw = f"{REFUSAL} (no answer within the call limits)"
        text, guard = check_citations(raw, trace)
        return {
            "question": question, "answer": text, "raw_answer": raw, "trace": trace,
            "citation_check": guard, "approvals": approvals, "tokens": tokens,
            "seconds": round(time.time() - started, 2), "model": ", ".join(models_used) or self.model_name,
        }


async def answer(question: str, approve=approve_interactively) -> dict:
    async with Harness(approve=approve) as h:
        return await h.answer(question)


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit('usage: python agent.py "your question"')
    question = " ".join(sys.argv[1:])
    result = asyncio.run(answer(question))
    sys.stdout.reconfigure(encoding="utf-8")
    print(result["answer"])
    print("\nSources retrieved:")
    for s, p in dict.fromkeys(retrieved_citations(result["trace"])):
        print(f"  [{s}, p. {p}]")
    guard = result["citation_check"]
    if guard["fired"]:
        print(f"\n[guardrail] citation check: {guard['action']} {guard['invalid']}")
    t = result["tokens"]
    print(f"\n({len(result['trace'])} tool calls, {t['total']} tokens, {result['seconds']}s, {result['model']})")


if __name__ == "__main__":
    main()
