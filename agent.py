"""
Assignment 3: your agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the tools of server.py over MCP and AGENTS.md as the
system prompt. Guardrails:
  1. approval: add_document runs only if the user says yes (approve callback; no terminal = no);
  2. call limits: at most MAX_TOOL_CALLS tool calls and MAX_MODEL_CALLS model calls per question;
  3. citation guard (our own): every [source: location] in the answer is checked against the
     passages that were actually retrieved; unverified ones are flagged in the answer.

`ask(question)` / `ask_many(questions)` return the answer and the tool trace, for evaluate.py.
"""

import asyncio
import os
import re
import sys
import time
from pathlib import Path

from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware, ToolCallLimitMiddleware
from langchain_core.tools import StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.errors import GraphRecursionError
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
MODEL = os.environ.get("AGENT_MODEL", "gemini-3.5-flash-lite")   # free tier: 500 requests a day (gemini-3.5-flash: 20)
MAX_TOOL_CALLS = 6      # per question
MAX_MODEL_CALLS = 10    # per question
MCP_TIMEOUT = 600       # seconds for one tool call: add_document embeds one request per passage


# --------------------------------------------------------------------------
# Guardrail 3: check the citations against what was retrieved
# --------------------------------------------------------------------------

CITATION = re.compile(r"\[([a-z][a-z0-9_]*):\s*([^\]]+)\]")
RETRIEVED = re.compile(r"Source: (\S+) \(.*?\) \| Location: (.+?)(?:, page \d+)? \| similarity")
REFERENCE = re.compile(r"\b(Article|Recital|Section)\s+((?:[IVX]+|\d+)(?:\.[A-Za-z0-9]+)*)")


SOURCE_MARK = re.compile(r"(?:^|[;,]\s*)([a-z][a-z0-9_]*):\s*")


def references(location: str) -> list[tuple[str, str]]:
    return REFERENCE.findall(location)


def citation_parts(citation: str) -> list[tuple[str, list[tuple[str, str]]]]:
    """One bracket can cite several sources: [gdpr: Article 33, edpb_breach: Section II.A.1]. Returns one
    (source, references) pair per source named in it."""
    pieces = SOURCE_MARK.split(citation[1:-1])        # ['', source, location, source, location, ...]
    return [(pieces[i], references(pieces[i + 1])) for i in range(1, len(pieces) - 1, 2)]


def same_or_nested(a: str, b: str) -> bool:
    return a == b or a.startswith(b + ".") or b.startswith(a + ".")


def check_citations(answer: str, retrieved: list[tuple[str, str]]) -> tuple[list[str], list[str]]:
    """Return (valid, invalid) citations of the answer (each different citation once). A citation is valid
    when every article, recital or section it names was in a retrieved passage of the same source."""
    have = [(source, kind, ident) for source, location in retrieved for kind, ident in references(location)]
    valid, invalid = [], []
    for match in CITATION.finditer(answer):
        text = match.group(0)
        parts = citation_parts(text)
        ok = bool(parts) and all(
            bool(refs) and all(any(s == source and k == kind and same_or_nested(i, ident) for s, k, i in have) for kind, ident in refs)
            for source, refs in parts
        )
        target = valid if ok else invalid
        if text not in target:
            target.append(text)
    return valid, invalid


def apply_guards(answer: str, state: dict) -> tuple[str, list[str]]:
    flags = list(state["events"])
    valid, invalid = check_citations(answer, state["retrieved"])
    state["valid_citations"], state["invalid_citations"] = valid, invalid
    if invalid:
        flags.append("unverified citation: " + "; ".join(invalid))
        answer += ("\n\nWARNING: these citations were not found in the passages retrieved for this question, "
                   "so they could not be verified: " + ", ".join(invalid))
    acted = any(t["tool"] == "add_document" for t in state["trace"])   # adding a document is not a question
    if not state["searched"] and not acted:
        flags.append("answered without searching")
        answer += "\n\nWARNING: this answer was given without searching the documents."
    elif state["searched"] and not valid and not invalid:
        flags.append("no [source: location] citation in the answer")   # recorded for the evaluation, not added to the answer
    return answer, flags


# --------------------------------------------------------------------------
# Guardrail 1: approval before add_document
# --------------------------------------------------------------------------

def cli_approve(tool: str, args: dict) -> bool:
    """Ask on the terminal. With no terminal (tests, evaluation) the answer is no."""
    if not sys.stdin.isatty():
        print(f"[approval] {tool}({args}) needs approval and there is no terminal: refused.", file=sys.stderr)
        return False
    print(f"\nThe agent wants to run {tool} with {args}. This changes the shared index.", file=sys.stderr)
    return input("Allow it? [y/N] ").strip().lower() in ("y", "yes")


# --------------------------------------------------------------------------
# The agent
# --------------------------------------------------------------------------

def _model():
    load_api_key()
    # Default temperature on purpose: Google advises against lowering it for Gemini 3.x models.
    return ChatGoogleGenerativeAI(model=MODEL, max_retries=6)


def _tool(session: ClientSession, definition, state: dict, approve) -> StructuredTool:
    async def run(**kwargs) -> str:
        started = time.time()
        if definition.name == "add_document" and not approve(definition.name, kwargs):
            text = "The user did not approve adding this document, so it was not added."
            state["events"].append(f"add_document refused by the user: {kwargs.get('path')}")
        else:
            result = await session.call_tool(definition.name, kwargs, read_timeout_seconds=MCP_TIMEOUT)
            text = "\n".join(getattr(c, "text", "") for c in result.content).strip()
            if getattr(result, "is_error", False) or getattr(result, "isError", False):
                text = f"Tool error: {text}"
            if definition.name == "search":
                state["searched"] = True
                state["retrieved"] += RETRIEVED.findall(text)
        state["trace"].append(
            {"tool": definition.name, "args": kwargs, "seconds": round(time.time() - started, 2), "result": text}
        )
        return text

    return StructuredTool(
        name=definition.name,
        description=definition.description or "",
        args_schema=definition.input_schema,
        coroutine=run,
    )


def _text(message) -> str:
    text = getattr(message, "text", None)   # a property in langchain >= 1.x
    return (str(text) if text is not None else str(message.content)).strip()


async def _answer(session, definitions, question: str, approve) -> dict:
    state = {"trace": [], "retrieved": [], "events": [], "searched": False}
    tools = [_tool(session, d, state, approve) for d in definitions]
    agent = create_agent(
        _model(),
        tools,
        system_prompt=(ROOT / "AGENTS.md").read_text(encoding="utf-8"),
        middleware=[
            ToolCallLimitMiddleware(run_limit=MAX_TOOL_CALLS, exit_behavior="continue"),
            ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS, exit_behavior="end"),
        ],
    )
    started = time.time()
    try:
        # The call limits above stop the loop first; the recursion limit is only a backstop.
        result = await agent.ainvoke({"messages": [{"role": "user", "content": question}]}, {"recursion_limit": 100})
        messages = result["messages"]
        raw_answer = _text(messages[-1])
    except GraphRecursionError:
        messages, raw_answer = [], "I could not finish answering this question within the allowed number of steps."
        state["events"].append("step limit reached")
    seconds = round(time.time() - started, 2)
    answer, flags = apply_guards(raw_answer, state)
    usage = [getattr(m, "usage_metadata", None) or {} for m in messages if m.type == "ai"]
    return {
        "question": question,
        "answer": answer,
        "raw_answer": raw_answer,
        "flags": flags,
        "tool_calls": state["trace"],
        "retrieved": state["retrieved"],
        "valid_citations": state["valid_citations"],
        "invalid_citations": state["invalid_citations"],
        "input_tokens": sum(u.get("input_tokens", 0) for u in usage),
        "output_tokens": sum(u.get("output_tokens", 0) for u in usage),
        "seconds": seconds,
        "model": MODEL,
    }


async def _run(questions: list[str], approve, on_result=None, keep_going: bool = False) -> list[dict]:
    params = StdioServerParameters(command=sys.executable, args=[str(ROOT / "server.py")], cwd=str(ROOT))
    results = []
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            definitions = (await session.list_tools()).tools
            failures = 0
            for question in questions:
                try:
                    result = await _answer(session, definitions, question, approve)
                except Exception as error:
                    if not keep_going:
                        raise
                    # one failed question must not lose the others; the caller can run it again
                    print(f"  failed: {question[:60]!r}: {type(error).__name__}: {str(error)[:200]}", file=sys.stderr)
                    failures += 1
                    if failures >= 3:
                        print("  stopping after 3 failures in a row (a quota limit?). Run again later to continue.", file=sys.stderr)
                        break
                    continue
                failures = 0
                results.append(result)
                if on_result:
                    on_result(result)     # lets the caller save each answer as soon as it exists
    return results


def ask_many(questions: list[str], approve=cli_approve, on_result=None, keep_going: bool = False) -> list[dict]:
    return asyncio.run(_run(questions, approve, on_result, keep_going))


def ask(question: str, approve=cli_approve) -> dict:
    return ask_many([question], approve)[0]


def main() -> int:
    if len(sys.argv) < 2 or not sys.argv[1].strip():
        print('Usage: python agent.py "your question"', file=sys.stderr)
        return 2
    result = ask(" ".join(sys.argv[1:]))
    print(result["answer"])
    calls = ", ".join(f"{c['tool']}({next(iter(c['args'].values()), '')!s:.50})" for c in result["tool_calls"]) or "none"
    print(
        f"\n[{result['model']}: {len(result['tool_calls'])} tool call(s): {calls} | "
        f"{result['input_tokens']} tokens in, {result['output_tokens']} out | {result['seconds']} s"
        + (f" | guards: {'; '.join(result['flags'])}" if result["flags"] else "") + "]",
        file=sys.stderr,
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
