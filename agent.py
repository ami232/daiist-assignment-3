"""
Assignment 3: your agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the tools of server.py (over MCP) and
AGENTS.md as the system prompt. Three guardrails live in this file:
  1. approval: add_document only runs if the person says yes;
  2. call limit: at most MAX_TOOL_CALLS tool calls per question;
  3. citation check: an answer that is not a refusal must cite a passage that was
     actually retrieved in this run, otherwise it is replaced by a refusal.

`ask(question)` returns the answer and the tool trace, for evaluate.py.
The answer goes to stdout; the trace summary goes to stderr.
"""

from __future__ import annotations

import asyncio
import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite")
MAX_TOOL_CALLS = 6  # guardrail 2
RECURSION_LIMIT = 30  # safety net inside LangGraph: model calls + tool calls
REFUSAL = "I don't know: the corpus does not cover this."
REFUSAL_MARK = "does not cover"  # how code recognises a refusal; AGENTS.md makes the model say it
CITATION = re.compile(r"\[([^\[\]|]+)\|([^\[\]]+)\]")  # [source | location]
HIT_HEADER = re.compile(r"^\[\d+\] (.+?) \| (.+?) \(score [-\d.]+\)$", re.M)  # server.py's result format


def system_prompt() -> str:
    path = ROOT / "AGENTS.md"
    if not path.is_file():
        raise SystemExit("AGENTS.md is missing: it is the agent's system prompt.")
    return path.read_text(encoding="utf-8")


def ask_user_to_approve(name: str, arguments: dict) -> bool:
    """Guardrail 1: a person says yes before add_document changes the index."""
    if not sys.stdin.isatty():
        print(f"{name}({arguments}) needs your approval and there is no terminal: denied.", file=sys.stderr)
        return False
    reply = input(f"\nThe agent wants to run {name}({arguments}). Allow? [y/N] ")
    return reply.strip().lower() in ("y", "yes", "s", "si", "sí")


class Run:
    """Everything that happens between the model and the MCP server in one question."""

    def __init__(self, approve) -> None:
        self.approve = approve
        self.trace: list[dict] = []
        self.calls = 0

    async def call(self, session, name: str, arguments: dict) -> str:
        started = time.time()
        blocked = None
        if self.calls >= MAX_TOOL_CALLS:  # guardrail 2
            blocked = "call limit"
            text = (
                f"Tool call limit reached ({MAX_TOOL_CALLS}). Do not call more tools: answer from the "
                "passages you already have, or say that the corpus does not cover the question."
            )
        else:
            self.calls += 1
            if name == "add_document" and not self.approve(name, arguments):  # guardrail 1
                blocked = "not approved"
                text = "The person did not approve add_document, so nothing was added. Do not try again."
            else:
                response = await session.call_tool(name, arguments)
                text = "\n".join(getattr(c, "text", "") for c in response.content).strip()
                if getattr(response, "is_error", False) or getattr(response, "isError", False):
                    text = f"Tool error: {text}"
        self.trace.append(
            {"tool": name, "args": arguments, "result": text, "seconds": round(time.time() - started, 2), "blocked": blocked}
        )
        return text

    def retrieved(self) -> list[tuple[str, str]]:
        """(source, location) of every passage the search tool returned in this run."""
        pairs = []
        for step in self.trace:
            if step["tool"] == "search" and not step["blocked"]:
                pairs += [(s.strip(), l.strip()) for s, l in HIT_HEADER.findall(step["result"])]
        return pairs


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def _label(location: str) -> str:
    """'Article 5 (part 2), p. 7' -> 'article 5': the section without the part number or the page."""
    return re.sub(r"\s*\(part \d+\)", "", _norm(location)).split(", p.")[0].strip()


def cites_retrieved(answer: str, retrieved: list[tuple[str, str]]) -> bool:
    """True if the answer cites at least one passage (same source, same section) that search returned."""
    for source, location in CITATION.findall(answer):
        cs, cl = _norm(source), _norm(location)
        for rs, rl in retrieved:
            rs, rl = _norm(rs), _norm(rl)
            if cs == rs and cl and (_label(cl) == _label(rl) or rl.startswith(cl) or cl.startswith(rl)):
                return True
    return False


def check_answer(answer: str, retrieved: list[tuple[str, str]]) -> tuple[str, str | None]:
    """Guardrail 3. Returns (answer to show, note if the guardrail changed it)."""
    if REFUSAL_MARK in answer.lower() or cites_retrieved(answer, retrieved):
        return answer, None
    return (
        f"{REFUSAL} (A draft answer had no citation of a passage I retrieved, so I am not giving it.)",
        "uncited answer replaced by a refusal",
    )


def args_model(spec):
    """Pydantic model of a tool's arguments, built from the JSON schema the MCP server publishes
    (Gemini accepts these reliably; a raw MCP schema can contain keys it rejects)."""
    from pydantic import Field, create_model

    schema = spec.input_schema or {}
    py_types = {"string": str, "integer": int, "number": float, "boolean": bool}
    fields = {}
    for key, prop in (schema.get("properties") or {}).items():
        py_type = py_types.get(prop.get("type"), str)
        if key in schema.get("required", []):
            fields[key] = (py_type, Field(..., description=prop.get("description", "")))
        else:
            fields[key] = (py_type | None, Field(None, description=prop.get("description", "")))
    return create_model(f"{spec.name}_arguments", **fields)


def message_text(message) -> str:
    text = getattr(message, "text", None)
    if text is not None and not isinstance(text, str):  # older versions: text is a method
        text = text()
    if text is None:
        content = message.content
        text = content if isinstance(content, str) else "".join(p.get("text", "") for p in content if isinstance(p, dict))
    return (text or "").strip()


async def ask_async(question: str, approve=ask_user_to_approve, llm=None, server_script: str = "server.py") -> dict:
    from langchain.agents import create_agent
    from langchain_core.messages import AIMessage, HumanMessage
    from langchain_core.tools import StructuredTool
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    started = time.time()
    run = Run(approve)
    guardrails: list[str] = []
    params = StdioServerParameters(command=sys.executable, args=[server_script], cwd=str(ROOT))
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = []
            for spec in (await session.list_tools()).tools:

                async def invoke(_name=spec.name, **arguments):
                    return await run.call(session, _name, arguments)

                tools.append(
                    StructuredTool(
                        name=spec.name,
                        description=spec.description or "",
                        args_schema=args_model(spec),
                        coroutine=invoke,
                    )
                )
            if llm is None:
                from langchain_google_genai import ChatGoogleGenerativeAI

                from api_key import load_api_key

                llm = ChatGoogleGenerativeAI(model=MODEL, api_key=load_api_key())
            agent = create_agent(llm, tools, system_prompt=system_prompt())
            try:
                result = await agent.ainvoke({"messages": [HumanMessage(question)]}, config={"recursion_limit": RECURSION_LIMIT})
                messages = result["messages"]
                raw_answer = message_text(messages[-1])
            except Exception as error:  # noqa: BLE001
                if type(error).__name__ != "GraphRecursionError":
                    raise
                messages, raw_answer = [], ""
                guardrails.append("recursion limit reached")

    if not raw_answer:
        raw_answer = REFUSAL
    answer, note = check_answer(raw_answer, run.retrieved())
    if note:
        guardrails.append(note)
    if any(step["blocked"] == "call limit" for step in run.trace):
        guardrails.append("tool call limit reached")
    if any(step["blocked"] == "not approved" for step in run.trace):
        guardrails.append("add_document not approved")
    ai = [m for m in messages if isinstance(m, AIMessage)]
    usage = [m.usage_metadata or {} for m in ai]
    return {
        "question": question,
        "answer": answer,
        "raw_answer": raw_answer,
        "refused": REFUSAL_MARK in answer.lower(),
        "retrieved": run.retrieved(),
        "trace": run.trace,
        "guardrails": guardrails,
        "model_calls": len(ai),
        "tool_calls": run.calls,
        "input_tokens": sum(u.get("input_tokens", 0) for u in usage),
        "output_tokens": sum(u.get("output_tokens", 0) for u in usage),
        "seconds": round(time.time() - started, 2),
        "model": getattr(llm, "model", None) or getattr(llm, "model_name", None) or MODEL,
    }


RETRY_WAITS = (8, 20, 45, 90)  # seconds to wait before each retry when the Gemini API is busy
BUSY = re.compile(r"\b(429|500|503|504)\b|UNAVAILABLE|RESOURCE_EXHAUSTED|DEADLINE_EXCEEDED")


def error_text(error: BaseException) -> str:
    """The message of an error, looking inside the exception groups that anyio raises."""
    if isinstance(error, BaseExceptionGroup):
        return " | ".join(error_text(e) for e in error.exceptions)
    return f"{type(error).__name__}: {error}"


def is_busy(error: BaseException) -> bool:
    """A temporary Gemini error (overloaded or rate limited), so trying again can work."""
    text = error_text(error)
    return bool(BUSY.search(text)) and "PerDay" not in text  # a used-up daily quota will not come back in a minute


def ask(question: str, **kwargs) -> dict:
    for attempt, wait in enumerate((*RETRY_WAITS, None), 1):
        try:
            return asyncio.run(ask_async(question, **kwargs))
        except (Exception, BaseExceptionGroup) as error:
            if wait is None or not is_busy(error):
                raise
            print(f"The model is busy ({error_text(error)[:100]}...). Trying again in {wait}s ({attempt}/{len(RETRY_WAITS)}).", file=sys.stderr)
            time.sleep(wait)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit('usage: python agent.py "your question"')
    try:
        outcome = ask(" ".join(sys.argv[1:]))
    except (Exception, BaseExceptionGroup) as error:
        raise SystemExit(f"The agent could not answer: {error_text(error)[:700]}")
    print(outcome["answer"])
    used = ", ".join(f"{s['tool']}({s['args']})" for s in outcome["trace"]) or "no tools"
    print(
        f"\n[{outcome['model']} | {outcome['seconds']}s | {outcome['input_tokens']} in / {outcome['output_tokens']} out tokens"
        f" | tools: {used} | guardrails: {', '.join(outcome['guardrails']) or 'none'}]",
        file=sys.stderr,
    )