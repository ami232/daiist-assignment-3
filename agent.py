"""
Assignment 3: the agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the tools of server.py (started over
MCP stdio, exactly as an editor starts it) and AGENTS.md as system prompt.

Guardrails:
- Approval: add_document only runs after a human types "y". With no terminal
  (e.g. during evaluation) it is denied automatically.
- Call limits: at most MAX_TOOL_CALLS tool calls and MAX_MODEL_CALLS model
  calls per question.
- Citation check (the extra guardrail): every [source, location] in the answer
  must match a passage that the search tool actually returned in this run. An
  answer that is not a refusal and has no valid citation is replaced by a
  refusal; invalid citations are flagged under the answer.

`answer(question)` returns the answer, citations, tool trace, retrieved
passages, tokens and seconds, for evaluate.py.
"""

from __future__ import annotations

import asyncio
import os
import re
import sys
import time
from pathlib import Path

from api_key import load_api_key
from retrieval import parse_results

ROOT = Path(__file__).resolve().parent
MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.6-flash")
MAX_TOOL_CALLS = 6
MAX_MODEL_CALLS = 8
REFUSAL = "The corpus does not cover this."
CITATION_RE = re.compile(
    r"\[\s*([A-Za-z][\w\-]*)\s*,\s*((?:Article|Recital|Annex|page|part|section)\b[^\]]*)\]", re.I
)


# ------------------------------------------------------------------ guardrails


def approve(path: str) -> bool:
    """Human approval before add_document runs."""
    if not sys.stdin.isatty() or os.environ.get("AUTO_DENY_ADD"):
        print(f"[approval] add_document({path!r}) denied: no one at the terminal to approve it.",
              file=sys.stderr)
        return False
    reply = input(f"\nThe agent wants to add {path!r} to the index (this spends embedding quota). "
                  f"Allow? [y/N] ")
    return reply.strip().lower() in ("y", "yes")


def is_refusal(text: str) -> bool:
    return REFUSAL.lower().rstrip(".") in text.lower()


def _same_location(cited: str, retrieved: str) -> bool:
    """"Article 33(1)" matches "Article 33"; "Article 33" does not match "Article 3"."""
    c, r = cited.strip().lower(), retrieved.strip().lower()
    if c == r:
        return True
    return c.startswith(r) and not c[len(r)].isdigit()


def check_citations(answer: str, retrieved: list[dict]) -> tuple[list[str], list[str]]:
    valid, invalid = [], []
    for source, location in CITATION_RE.findall(answer):
        ok = any(r["source"].lower() == source.lower() and _same_location(location, r["location"])
                 for r in retrieved)
        (valid if ok else invalid).append(f"{source}, {location.strip()}")
    return list(dict.fromkeys(valid)), list(dict.fromkeys(invalid))


def citation_guardrail(answer: str, retrieved: list[dict]) -> tuple[str, list[str], list[str], str | None]:
    valid, invalid = check_citations(answer, retrieved)
    if not is_refusal(answer) and not valid:
        return (f"{REFUSAL} (A draft answer was withheld because it did not cite any passage "
                f"returned by the search tool.)", valid, invalid, "no valid citation: answer withheld")
    if invalid:
        warning = "\n\nWarning: these citations do not match any retrieved passage: " + "; ".join(invalid)
        return answer + warning, valid, invalid, "invalid citations flagged"
    return answer, valid, invalid, None


# ------------------------------------------------------------------ agent


def system_prompt() -> str:
    return (ROOT / "AGENTS.md").read_text(encoding="utf-8")


def text_of(message) -> str:
    content = message.content
    if isinstance(content, str):
        return content
    return "".join(p.get("text", "") if isinstance(p, dict) else str(p) for p in content)


def make_tool(session, tool, trace: list, retrieved: list, counter: dict, approve_fn):
    """Wrap one MCP tool as a LangChain tool, with the approval step and call limit."""
    from langchain_core.tools import StructuredTool

    async def call(**kwargs):
        counter["tools"] += 1
        entry = {"tool": tool.name, "args": kwargs}
        trace.append(entry)
        if counter["tools"] > MAX_TOOL_CALLS:
            entry["result"] = "blocked: tool call limit"
            return (f"Tool call limit ({MAX_TOOL_CALLS}) reached. Answer now from the passages you "
                    f"already have, or reply: {REFUSAL}")
        if tool.name == "add_document":
            entry["approved"] = approve_fn(str(kwargs.get("path", "")))
            if not entry["approved"]:
                entry["result"] = "denied by the user"
                return "The user did not approve adding this document. Do not try again."
        result = await session.call_tool(tool.name, kwargs)
        text = "\n".join(getattr(c, "text", "") for c in result.content)
        entry["result"] = text
        if tool.name == "search":
            retrieved.extend(parse_results(text))
        return text

    return StructuredTool(name=tool.name, description=tool.description or "",
                          args_schema=getattr(tool, "input_schema", None) or getattr(tool, "inputSchema"), coroutine=call)


async def run(question: str, approve_fn=approve) -> dict:
    from langchain.agents import create_agent
    from langchain_google_genai import ChatGoogleGenerativeAI
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    load_api_key()
    trace: list[dict] = []
    retrieved: list[dict] = []
    counter = {"tools": 0}
    started = time.time()
    params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT),
                                   env=dict(os.environ))
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = [make_tool(session, t, trace, retrieved, counter, approve_fn)
                     for t in (await session.list_tools()).tools]
            model = ChatGoogleGenerativeAI(model=MODEL, temperature=0, max_retries=6)
            agent = create_agent(model, tools, system_prompt=system_prompt())
            messages = []
            raw = ""
            for attempt in range(1, 5):
                try:
                    state = await agent.ainvoke(
                        {"messages": [{"role": "user", "content": question}]},
                        config={"recursion_limit": 2 * MAX_MODEL_CALLS + 1},
                    )
                    messages = state["messages"]
                    raw = text_of(messages[-1]).strip()
                    break
                except Exception as error:  # noqa: BLE001
                    name = type(error).__name__
                    if name == "GraphRecursionError":
                        raw = f"{REFUSAL} (Stopped: more than {MAX_MODEL_CALLS} model calls.)"
                        break
                    if ("429" in str(error) or "RESOURCE_EXHAUSTED" in str(error)) and attempt < 4:
                        print(f"Rate limited, waiting {30 * attempt}s ...", file=sys.stderr)
                        await asyncio.sleep(30 * attempt)
                        trace.clear(), retrieved.clear()
                        counter["tools"] = 0
                        continue
                    raise

    tokens = {"input": 0, "output": 0, "total": 0}
    model_calls = 0
    for message in messages:
        usage = getattr(message, "usage_metadata", None)
        if getattr(message, "type", "") == "ai":
            model_calls += 1
        if usage:
            tokens["input"] += usage.get("input_tokens", 0)
            tokens["output"] += usage.get("output_tokens", 0)
            tokens["total"] += usage.get("total_tokens", 0)

    final, valid, invalid, fired = citation_guardrail(raw, retrieved)
    unique, seen = [], set()
    for chunk in retrieved:
        key = (chunk["source"], chunk["location"], chunk["text"][:80])
        if key not in seen:
            seen.add(key)
            unique.append(chunk)
    return {
        "question": question,
        "answer": final,
        "raw_answer": raw,
        "refused": is_refusal(final),
        "citations": valid,
        "invalid_citations": invalid,
        "guardrail": fired,
        "trace": trace,
        "retrieved": unique,
        "tool_calls": len(trace),
        "model_calls": model_calls,
        "tokens": tokens,
        "seconds": round(time.time() - started, 1),
        "model": MODEL,
    }


def answer(question: str, approve_fn=approve) -> dict:
    """Synchronous entry point for evaluate.py."""
    return asyncio.run(run(question, approve_fn))


def main() -> None:
    question = " ".join(sys.argv[1:]).strip()
    if not question:
        raise SystemExit('usage: python agent.py "your question"')
    result = answer(question)
    print(result["answer"])
    if result["citations"]:
        print("\nSources:")
        for citation in result["citations"]:
            print(f"  - [{citation}]")
    note = f", guardrail: {result['guardrail']}" if result["guardrail"] else ""
    print(f"\n({result['tool_calls']} tool calls, {result['model_calls']} model calls, "
          f"{result['tokens']['total']} tokens, {result['seconds']}s{note})")


if __name__ == "__main__":
    main()
