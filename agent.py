"""
Assignment 3: the agent (`main.py ask "question"` runs `python agent.py "question"`).

A LangChain agent (`create_agent`) on Gemini. Its tools come from server.py over
MCP, and AGENTS.md is the system prompt. Three safeguards sit around it:

1. Approval: add_document changes the shared index and spends embedding quota,
   so the person must say yes before it runs. With no terminal to ask on, the
   call is refused.
2. Call limits: at most MAX_MODEL_CALLS model calls and MAX_TOOL_CALLS tool
   calls per question, so a confused agent cannot loop and burn quota.
3. Citation guardrail (my extra one): after the agent answers, code checks that
   every citation label points at a passage the search tool really returned and
   that a non-refusal answer has at least one. If not, the agent gets one chance
   to fix it, and otherwise the answer is replaced by a refusal. An invented
   citation never reaches the reader.

For evaluate.py, `ask_many(questions)` returns the answer together with the tool
trace, the retrieved passages and the token and time cost.
"""

from __future__ import annotations

import asyncio
import json
import os
import re
import sys
import time
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Callable

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
SERVER_COMMAND = [sys.executable, str(ROOT / "server.py")]
SYSTEM_PROMPT_FILE = ROOT / "AGENTS.md"

MODEL = os.environ.get("AGENT_MODEL", "gemini-flash-latest")
MAX_MODEL_CALLS = 10
MAX_TOOL_CALLS = 6
QUESTION_TIMEOUT = 150   # seconds; a call that hangs longer than this is cancelled and retried
RETRY_WAIT = 10   # seconds, multiplied by the attempt number, when the model service is busy
APPROVAL_REQUIRED = {"add_document"}

REFUSAL_PREFIX = "NOT IN CORPUS:"
CITATION = re.compile(r"\[([^\[\]|]+?)\s*\|\s*([^\[\]]+?)\]")
RESULT_BLOCK = re.compile(
    r"Cite as: \[(?P<source>[^\[\]|]+?)\s*\|\s*(?P<location>[^\[\]]+?)\]\s*\n"
    r"Document: (?P<doc>[^\n]*)\nText:\n(?P<text>.*?)(?=\n\nResult \d+\nCite as:|\Z)",
    re.DOTALL,
)


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


# ------------------------------------------------------------------ approval

def ask_user(tool: str, args: dict) -> bool:
    """Ask the person to approve a tool call. No terminal means no."""
    if not sys.stdin or not sys.stdin.isatty():
        log(f"[approval] {tool} needs approval but there is no terminal to ask on, so it was refused.")
        return False
    log(f"\n[approval] The agent wants to run {tool} with {json.dumps(args)}.")
    log("[approval] This changes the shared index and uses embedding quota.")
    print("Approve? [y/N] ", end="", file=sys.stderr, flush=True)
    return input().strip().lower() in {"y", "yes"}


# ---------------------------------------------------------- citation helpers

def label_key(source: str, location: str) -> str:
    clean = lambda s: re.sub(r"\s+", " ", s.replace("§", "")).strip().strip(".").lower()
    return f"{clean(source)}|{clean(location)}"


def parse_results(text: str) -> list[dict]:
    """Passages in a search result, as {source, location, doc, text}."""
    return [m.groupdict() for m in RESULT_BLOCK.finditer(text)]


def is_refusal(answer: str) -> bool:
    return answer.strip().upper().startswith(REFUSAL_PREFIX)


def check_answer(answer: str, retrieved: set[str]) -> dict:
    """The guardrail check. retrieved holds label_key() of every passage the search tool returned."""
    cited = [(s.strip(), l.strip()) for s, l in CITATION.findall(answer)]
    valid = [c for c in cited if label_key(*c) in retrieved]
    invalid = [c for c in cited if label_key(*c) not in retrieved]
    refusal = is_refusal(answer)
    if refusal:
        problem = None
    elif not cited:
        problem = "the answer has no citations"
    elif invalid:
        problem = "these citations were not in the search results: " + ", ".join(f"[{s} | {l}]" for s, l in invalid)
    else:
        problem = None
    return {"refusal": refusal, "valid": valid, "invalid": invalid, "problem": problem}


# ------------------------------------------------------------- agent plumbing

def build_model():
    from langchain_google_genai import ChatGoogleGenerativeAI

    return ChatGoogleGenerativeAI(model=MODEL, google_api_key=load_api_key(), max_retries=3)


def _text(message) -> str:
    content = message.content
    if isinstance(content, str):
        return content
    parts = [p.get("text", "") if isinstance(p, dict) else str(p) for p in content]
    return "".join(parts)


def _wrap_tool(session, spec, trace: list, approve: Callable[[str, dict], bool]):
    from langchain_core.tools import StructuredTool

    async def call(**arguments):
        started = time.time()
        if spec.name in APPROVAL_REQUIRED and not approve(spec.name, arguments):
            text = (f"DENIED: the user did not approve {spec.name}. Nothing was changed. "
                    f"Tell the user it was not run and continue without it.")
            trace.append({"tool": spec.name, "args": arguments, "result": text, "denied": True, "seconds": 0.0})
            return text
        result = await session.call_tool(spec.name, arguments)
        text = "\n".join(getattr(c, "text", "") for c in result.content).strip()
        if getattr(result, "is_error", False):
            text = f"ERROR: {text}"
        trace.append({"tool": spec.name, "args": arguments, "result": text, "denied": False,
                      "seconds": round(time.time() - started, 2)})
        return text

    return StructuredTool(
        name=spec.name,
        description=(spec.description or "").strip(),
        args_schema=spec.input_schema,
        coroutine=call,
    )


@asynccontextmanager
async def open_session(trace: list, approve: Callable[[str, dict], bool]):
    """Start server.py over stdio and yield its tools as LangChain tools."""
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    # Pass the whole environment: stdio_client would otherwise hide GEMINI_API_KEY from the server.
    params = StdioServerParameters(command=SERVER_COMMAND[0], args=SERVER_COMMAND[1:],
                                   cwd=str(ROOT), env=dict(os.environ))
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            specs = (await session.list_tools()).tools
            yield [_wrap_tool(session, spec, trace, approve) for spec in specs]


def _usage(messages) -> tuple[int, int]:
    tokens_in = tokens_out = 0
    for message in messages:
        meta = getattr(message, "usage_metadata", None) or {}
        tokens_in += int(meta.get("input_tokens", 0) or 0)
        tokens_out += int(meta.get("output_tokens", 0) or 0)
    return tokens_in, tokens_out


def _retrieved(trace: list) -> tuple[set[str], list[dict]]:
    keys: set[str] = set()
    passages: list[dict] = []
    for step in trace:
        if step["tool"] != "search" or step["result"].startswith("ERROR"):
            continue
        for passage in parse_results(step["result"]):
            keys.add(label_key(passage["source"], passage["location"]))
            passages.append(passage)
    return keys, passages


async def _ask_one(agent, question: str, trace: list) -> dict:
    from langchain_core.messages import AIMessage, HumanMessage

    started = time.time()
    state = await agent.ainvoke({"messages": [HumanMessage(question)]})
    guardrail = None

    def final_answer(messages) -> str:
        for message in reversed(messages):
            if isinstance(message, AIMessage) and _text(message).strip() and not message.tool_calls:
                return _text(message).strip()
        return ""

    def limit_hit(text: str) -> bool:
        return text.lower().startswith(("model call limit", "model call limits exceeded"))

    answer = final_answer(state["messages"])
    keys, _ = _retrieved(trace)
    verdict = check_answer(answer, keys)
    problem = verdict["problem"] or ("the agent hit its call limit" if limit_hit(answer) else None)

    if problem:
        log(f"[guardrail] {problem}. Asking the agent to fix it once.")
        guardrail = "retried"
        correction = (
            f"Your answer cannot be shown yet because {problem}. Rewrite it using only passages you "
            f"retrieved, and put the exact 'Cite as' label after each claim. If the passages do not "
            f"answer the question, start with '{REFUSAL_PREFIX}' instead. You may search again."
        )
        try:
            state = await agent.ainvoke({"messages": state["messages"] + [HumanMessage(correction)]})
            answer = final_answer(state["messages"])
        except Exception as error:  # noqa: BLE001
            log(f"[guardrail] retry failed: {type(error).__name__}: {error}")
            answer = ""
        keys, _ = _retrieved(trace)
        verdict = check_answer(answer, keys)
        problem = verdict["problem"] or ("the agent hit its call limit" if limit_hit(answer) else None)
        if problem or not answer:
            guardrail = "replaced"
            answer = (f"{REFUSAL_PREFIX} I could not produce an answer whose citations check out against "
                      f"the retrieved passages ({problem or 'empty answer'}), so I am not giving one.")
            verdict = check_answer(answer, keys)

    tokens_in, tokens_out = _usage(state["messages"])
    _, passages = _retrieved(trace)
    return {
        "question": question,
        "answer": answer,
        "refused": verdict["refusal"],
        "citations": [f"[{s} | {l}]" for s, l in verdict["valid"]],
        "invalid_citations": [f"[{s} | {l}]" for s, l in verdict["invalid"]],
        "guardrail": guardrail,
        "tool_calls": list(trace),
        "retrieved": passages,
        "input_tokens": tokens_in,
        "output_tokens": tokens_out,
        "seconds": round(time.time() - started, 1),
        "model": MODEL,
    }


async def ask_many_async(questions: list[str], approve: Callable[[str, dict], bool] | None = None,
                         on_result: Callable[[dict], None] | None = None) -> list[dict]:
    from langchain.agents import create_agent
    from langchain.agents.middleware import ModelCallLimitMiddleware, ToolCallLimitMiddleware

    approve = approve or ask_user
    system_prompt = SYSTEM_PROMPT_FILE.read_text(encoding="utf-8")
    model = build_model()
    results = []
    trace: list[dict] = []
    async with open_session(trace, approve) as tools:
        agent = create_agent(
            model,
            tools,
            system_prompt=system_prompt,
            middleware=[
                ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS, exit_behavior="end"),
                ToolCallLimitMiddleware(run_limit=MAX_TOOL_CALLS),
            ],
        )
        for question in questions:
            result = None
            error = None
            for attempt in range(5):
                trace.clear()
                try:
                    result = await asyncio.wait_for(_ask_one(agent, question, trace), QUESTION_TIMEOUT)
                    break
                except Exception as exc:  # noqa: BLE001 - one bad question must not stop an evaluation
                    error = exc
                    text = f"{type(exc).__name__} {exc}"
                    if isinstance(exc, asyncio.TimeoutError):
                        text = f"503 TIMEOUT: no reply within {QUESTION_TIMEOUT}s"
                    if attempt < 4 and any(code in text for code in ("503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED", "500", "DEADLINE")):
                        wait = RETRY_WAIT * (attempt + 1)
                        log(f"[retry] the model service is busy ({text[:80]}). Trying again in {wait}s.")
                        await asyncio.sleep(wait)
                        continue
                    break
            if result is None:
                result = {
                    "question": question,
                    "answer": f"{REFUSAL_PREFIX} the agent failed ({type(error).__name__}: {str(error)[:200]}).",
                    "refused": True, "citations": [], "invalid_citations": [], "guardrail": "error",
                    "tool_calls": list(trace), "retrieved": _retrieved(trace)[1],
                    "input_tokens": 0, "output_tokens": 0, "seconds": 0.0, "model": MODEL,
                    "error": f"{type(error).__name__}: {error}",
                }
            results.append(result)
            if on_result:
                on_result(result)
    return results


def ask_many(questions: list[str], approve=None, on_result=None) -> list[dict]:
    """Answer questions with one server session. Returns answer, citations, tool trace and cost for each."""
    return asyncio.run(ask_many_async(questions, approve=approve, on_result=on_result))


def ask(question: str, approve=None) -> dict:
    return ask_many([question], approve=approve)[0]


def main() -> int:
    if len(sys.argv) < 2 or not " ".join(sys.argv[1:]).strip():
        print('Usage: python agent.py "your question"', file=sys.stderr)
        return 2
    question = " ".join(sys.argv[1:]).strip()
    result = ask(question)

    if result.get("error"):
        print(f"The agent could not run: {result['error']}", file=sys.stderr)
        print("If this says the model is busy (503), wait a minute and try again, "
              "or set AGENT_MODEL to another Gemini model name.", file=sys.stderr)
        return 1
    print(result["answer"])
    if result["citations"]:
        titles = {label_key(p["source"], p["location"]): p["doc"] for p in result["retrieved"]}
        print("\nSources:")
        for label in dict.fromkeys(result["citations"]):
            source, location = [part.strip() for part in label.strip("[]").split("|", 1)]
            print(f"  {label}  {titles.get(label_key(source, location), '')}")
    notes = []
    if result["guardrail"]:
        notes.append(f"citation guardrail: {result['guardrail']}")
    notes.append(f"{result['seconds']}s, {result['input_tokens']} tokens in, {result['output_tokens']} out, "
                 f"{sum(1 for t in result['tool_calls'] if t['tool'] == 'search')} searches")
    log("(" + "; ".join(notes) + ")")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
