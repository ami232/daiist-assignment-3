"""
Assignment 3: the agent. `uv run python main.py ask "question"` runs this file.

LangChain `create_agent` on Gemini. Its tools are the ones server.py exposes over MCP
(search, add_document) and AGENTS.md is the system prompt.

Harness controls (all in code, not only in the prompt):
  1. Approval: add_document runs only if a human approves (see `approve`).
  2. Call limit: at most MAX_TOOL_CALLS tool calls per question.
  3. Guardrail (citation check): every citation `[source, location]` in the answer must
     appear in the passages `search` returned in this run. If not, or if the model answered
     without searching, a warning is appended to the answer and recorded in `flags`.

For evaluate.py: `run_agent(question)` returns a dict with the answer, the tool trace,
the guardrail flags, the time and the token usage.
"""

import asyncio
import os
import re
import sys
import time
from pathlib import Path

from langchain.agents import create_agent
from langchain_core.tools import StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
MODEL = os.environ.get("CHAT_MODEL", "gemini-3.5-flash")
FALLBACK_MODELS = ["gemini-3.8-flash", "gemini-flash-latest"]   # tried in order if MODEL is overloaded or gone
MAX_TOOL_CALLS = 6          # guardrail 2: hard limit of tool calls per question
RUN_TIMEOUT = 120           # seconds for one whole question; then it is retried (see run_agent)
RECURSION_LIMIT = 25        # safety net for the agent loop itself


def system_prompt() -> str:
    return (ROOT / "AGENTS.md").read_text(encoding="utf-8")


def cli_approve(tool: str, args: dict) -> bool:
    """Ask the human in the terminal. With no terminal (e.g. check.py), the answer is no."""
    if not sys.stdin.isatty():
        print(f"[approval] {tool}({args}) needs approval and there is no terminal: denied.", file=sys.stderr)
        return False
    reply = input(f"\nThe agent wants to run {tool}({args}). Approve? [y/N] ")
    return reply.strip().lower() in ("y", "yes", "s", "si", "sí")


def _result_text(result) -> str:
    return "\n".join(getattr(block, "text", "") for block in result.content).strip()


def _normalise(text: str) -> str:
    return re.sub(r"\s+", " ", text.lower()).strip()


def _numbers(location: str) -> set[int]:
    """Paragraph or article numbers a location covers.
    'paras 28-29 (p.10)' -> {28, 29}; 'Article 4 part 2' -> {4}; 'Article 15 to Article 16' -> {15, 16}."""
    text = _normalise(location)
    if text.startswith("article"):
        text = re.sub(r"part \d+|\(\d+\)|\([a-z]\)", " ", text)      # drop 'part 2', '(1)', '(a)'
        found = [int(n) for n in re.findall(r"\d+", text)]
        return set(range(min(found), max(found) + 1)) if found else set()
    text = re.sub(r"\(p\.[^)]*\)", "", text)          # drop the page part
    numbers = set()
    for start, end in re.findall(r"(\d+)(?:\s*-\s*(\d+))?", text):
        numbers.update(range(int(start), int(end or start) + 1))
    return numbers


def retrieved_locations(trace: list[dict]) -> set[tuple[str, str]]:
    """(source, location) pairs that search results in this run actually contained."""
    found = set()
    for step in trace:
        if step["tool"] != "search":
            continue
        for source, location in re.findall(r"source: (\S+) \| location: ([^|\n]+?) \| distance", step["result"]):
            found.add((source.strip(), location.strip()))
    return found


def check_citations(answer: str, trace: list[dict]) -> list[str]:
    """Guardrail 3: returns the citations in the answer that no retrieved passage supports.
    A citation [source, location] is supported if the same source was retrieved with the same
    article number, or a paragraph range that contains the cited paragraph number."""
    retrieved = retrieved_locations(trace)
    bad = []
    for source, location in re.findall(r"\[([a-z_0-9]+),\s*([^\]]+)\]", answer):
        kind = "article" if _normalise(location).startswith("article") else "para"
        cited = _numbers(location)
        ok = any(
            source == s
            and (_normalise(l).startswith("article") == (kind == "article"))
            and (not cited or cited & _numbers(l))
            for s, l in retrieved
        )
        if not ok:
            bad.append(f"{source}, {location.strip()}")
    return bad


async def _run(question: str, approve, model_name=None) -> dict:
    load_api_key()
    started = time.time()
    trace: list[dict] = []
    flags: list[str] = []
    calls = {"n": 0}
    params = StdioServerParameters(command=sys.executable, args=[str(ROOT / "server.py")], cwd=str(ROOT), env=dict(os.environ))

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            mcp_tools = (await session.list_tools()).tools

            def wrap(tool):
                async def call(**kwargs) -> str:
                    step = {"tool": tool.name, "args": kwargs, "result": "", "status": "ok"}
                    trace.append(step)
                    if calls["n"] >= MAX_TOOL_CALLS:           # guardrail 2
                        step["status"] = "blocked: call limit"
                        step["result"] = f"Call limit reached ({MAX_TOOL_CALLS}). Answer with what you already have."
                        flags.append("call_limit")
                        return step["result"]
                    calls["n"] += 1
                    if tool.name == "add_document" and not approve(tool.name, kwargs):   # approval
                        step["status"] = "denied by user"
                        step["result"] = "The user did not approve adding this document. Do not add it."
                        flags.append("add_document_denied")
                        return step["result"]
                    result = await session.call_tool(tool.name, kwargs)
                    text = _result_text(result)
                    if getattr(result, "is_error", False) or getattr(result, "isError", False):
                        step["status"] = "error"
                    step["result"] = text
                    return text

                return StructuredTool(
                    name=tool.name,
                    description=tool.description or "",
                    args_schema=tool.input_schema,
                    coroutine=call,
                )

            chosen = model_name or MODEL
            model = ChatGoogleGenerativeAI(model=chosen, temperature=0, max_retries=2, timeout=60) if isinstance(chosen, str) else chosen
            agent = create_agent(model, [wrap(t) for t in mcp_tools], system_prompt=system_prompt())
            state = await agent.ainvoke(
                {"messages": [{"role": "user", "content": question}]},
                config={"recursion_limit": RECURSION_LIMIT},
            )

    messages = state["messages"]
    answer = (getattr(messages[-1], "text", None) or str(messages[-1].content)).strip()
    tokens = {"input": 0, "output": 0}
    for message in messages:
        usage = getattr(message, "usage_metadata", None) or {}
        tokens["input"] += usage.get("input_tokens", 0)
        tokens["output"] += usage.get("output_tokens", 0)

    # guardrail 3: citation check
    if not any(s["tool"] == "search" and s["status"] == "ok" for s in trace):
        flags.append("no_search")
        answer += "\n\n[Guardrail] This answer was given without searching the corpus; do not rely on it."
    bad = check_citations(answer, trace)
    if bad:
        flags.append("unsupported_citation")
        answer += "\n\n[Guardrail] Citation(s) not found in the retrieved passages: " + "; ".join(bad)

    return {
        "question": question,
        "answer": answer,
        "trace": trace,
        "flags": list(dict.fromkeys(flags)),
        "seconds": round(time.time() - started, 1),
        "tokens": tokens,
        "model": chosen if isinstance(chosen, str) else "custom",
    }


def _error_text(error: BaseException) -> str:
    """Text of an error including the errors inside exception groups."""
    parts = [f"{type(error).__name__}: {error}"]
    for inner in getattr(error, "exceptions", ()):
        parts.append(_error_text(inner))
    return " | ".join(parts)


RETRYABLE = ("TimeoutError", "503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED", "NOT_FOUND", "high demand", "overloaded", "timed out")


def run_agent(question: str, approve=cli_approve) -> dict:
    """Answer one question. Returns {answer, trace, flags, seconds, tokens, model} (used by evaluate.py).
    If the model is overloaded or unavailable, it retries once and then tries the fallback models."""
    names = [MODEL, *[m for m in FALLBACK_MODELS if m != MODEL]] if isinstance(MODEL, str) else [MODEL]
    last_error = None
    for name in names:
        for attempt in range(2):
            try:
                return asyncio.run(asyncio.wait_for(_run(question, approve, name), RUN_TIMEOUT))
            except Exception as error:
                text = _error_text(error)
                if not any(word in text for word in RETRYABLE):
                    raise
                last_error = error
                print(f"[agent] {name} failed ({text[-160:]}); retrying or switching model...", file=sys.stderr, flush=True)
                time.sleep(8)
    raise last_error


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit('Usage: uv run python main.py ask "your question"')
    result = run_agent(" ".join(sys.argv[1:]))
    print(result["answer"])
    print("\n--- tool trace ---")
    for step in result["trace"]:
        print(f"{step['tool']}({step['args']}) -> {step['status']}")
    if result["flags"]:
        print("guardrail flags:", ", ".join(result["flags"]))
    print(f"({result['seconds']}s, tokens in/out: {result['tokens']['input']}/{result['tokens']['output']})")


if __name__ == "__main__":
    main()
