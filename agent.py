"""
Assignment 3: the agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini. Its tools are server.py's MCP tools: this
script starts server.py over stdio (as an editor does) and wraps `search` and
`add_document` as LangChain tools. AGENTS.md is the system prompt.

Safety in the harness:
  - approval: add_document only runs after a person types "y" at the prompt;
    without an interactive terminal it is refused (evaluate.py can pass an
    explicit approve function for the scripted add-document demo);
  - call limits: at most MAX_MODEL_CALLS model calls and MAX_SEARCHES searches
    per question, so a confused agent cannot loop and burn the free quota;
  - guardrail: see apply_guardrail().

evaluate.py imports run_agent(question) -> {"answer", "trace", "tokens", "seconds", ...}.
"""

from __future__ import annotations

import asyncio
import os
import re
import sys
import time
import warnings
from pathlib import Path
from typing import Callable

warnings.filterwarnings("ignore", message=".*fixed sampling defaults.*")
warnings.filterwarnings("ignore", message=".*was never awaited.*", category=RuntimeWarning)

ROOT = Path(__file__).resolve().parent
SYSTEM_PROMPT_FILE = ROOT / "AGENTS.md"
MODEL = os.environ.get("AGENT_MODEL", "gemini-3.5-flash")
# Used in order when the main model errors: 503 "high demand", or 429 when the free tier's
# 20 requests per model per day run out. Each answer records which model produced it.
FALLBACK_MODELS = ("gemini-3.6-flash", "gemini-3.5-flash-lite", "gemini-3.1-flash-lite",
                   "gemini-3.7-flash", "gemini-3.8-flash")
MAX_MODEL_CALLS = 6
MAX_SEARCHES = 4

Approver = Callable[[str], bool]


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


def deny(path: str) -> bool:
    """Approval function for batch runs (evaluation): never add documents."""
    log(f"add_document({path!r}) refused: batch run, no approval possible.")
    return False


def ask_in_terminal(path: str) -> bool:
    """Default approval step for add_document: a person must type y."""
    if not sys.stdin.isatty():
        log(f"add_document({path!r}) needs approval, but there is no interactive terminal: refused.")
        return False
    reply = input(f"\nThe agent wants to add {path!r} to the shared index. Allow? [y/N] ")
    return reply.strip().lower() in {"y", "yes"}


# Phrases that mark an answer as "the labels do not cover this" (a refusal needs no citation).
REFUSAL_MARKERS = (
    "do not cover", "does not cover", "don't cover", "not covered", "no information",
    "do not contain", "does not contain", "do not mention", "does not mention",
    "do not include", "does not include",
    "could not find", "couldn't find", "cannot answer", "can't answer",
)


def is_refusal(answer: str) -> bool:
    return any(marker in answer.lower() for marker in REFUSAL_MARKERS)


def _section_matches(cited_section: str, retrieved_section: str) -> bool:
    """[warfarin 7] is backed by a retrieved 7.3 passage, and [warfarin 7.3] by a retrieved 7."""
    a, b = cited_section, retrieved_section
    return a == b or b.startswith(a + ".") or a.startswith(b + ".")


def check_citations(answer: str, trace: list[dict]) -> str | None:
    """Why the answer fails the citation check, or None if it passes."""
    citations = cited(answer)
    if not citations:
        return None if is_refusal(answer) else "the answer makes claims but cites no passage"
    retrieved = retrieved_passages(trace)
    unbacked = [f"[{d} {s}]" for d, s in citations
                if not any(d == rd and _section_matches(s, rs) for rd, rs in retrieved)]
    if unbacked:
        return f"cites passages the searches never returned: {', '.join(unbacked)}"
    return None


def apply_guardrail(answer: str, trace: list[dict]) -> tuple[str, str | None]:
    """Citation guardrail on the final answer. Returns (answer to show, reason it fired or None).

    Every answer that is not a refusal must cite at least one passage, and every
    citation must point to a passage that a search in this run actually returned.
    If not, the answer is withheld: an uncited or wrongly cited medication claim
    is worse than no answer. The retrieved passages are listed so the user can
    read the label themselves.
    """
    reason = check_citations(answer, trace)
    if reason is None:
        return answer, None
    found = sorted(retrieved_passages(trace))
    listing = "\n".join(f"  [{d} {s}]" for d, s in found) or "  (none)"
    blocked = ("I can't give an answer that is fully supported by the drug labels, so I am not "
               "showing one. Please check with a pharmacist or doctor.\n"
               f"Label passages found for this question:\n{listing}")
    return blocked, reason


def _text(content) -> str:
    """Message content as plain text (Gemini may return a list of parts)."""
    if isinstance(content, str):
        return content
    return "".join(part.get("text", "") if isinstance(part, dict) else str(part) for part in content)


async def _run(question: str, approve: Approver) -> dict:
    from langchain.agents import create_agent
    from langchain.agents.middleware import ModelCallLimitMiddleware, ModelFallbackMiddleware, ToolCallLimitMiddleware
    from langchain_core.tools import StructuredTool
    from langchain_google_genai import ChatGoogleGenerativeAI
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    from api_key import load_api_key

    load_api_key()
    trace: list[dict] = []
    # Pass the environment on: the MCP client otherwise forwards only a few variables,
    # and the demo uses CORPUS_INDEX_DIR to point the server at a copy of the index.
    server = StdioServerParameters(command=sys.executable, args=[str(ROOT / "server.py")], cwd=str(ROOT),
                                   env=dict(os.environ))

    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            descriptions = {t.name: t.description for t in (await session.list_tools()).tools}

            async def call(name: str, arguments: dict) -> str:
                started = time.time()
                result = await session.call_tool(name, arguments)
                output = "\n".join(getattr(c, "text", "") for c in result.content)
                trace.append({"tool": name, "args": arguments, "output": output,
                              "error": bool(result.is_error), "seconds": round(time.time() - started, 2)})
                return output

            async def search(query: str) -> str:
                return await call("search", {"query": query})

            async def add_document(path: str) -> str:
                if not approve(path):
                    trace.append({"tool": "add_document", "args": {"path": path}, "output": "refused: not approved",
                                  "error": True, "seconds": 0})
                    return "The user did not approve adding this document. Nothing was added."
                return await call("add_document", {"path": path})

            tools = [
                StructuredTool.from_function(coroutine=search, name="search", description=descriptions["search"]),
                StructuredTool.from_function(coroutine=add_document, name="add_document",
                                             description=descriptions["add_document"]),
            ]
            def gemini(name: str, retries: int):
                # On the free tier a 429 usually means that model's daily quota is gone, so
                # moving on to the next fallback model is faster than waiting for a retry.
                return ChatGoogleGenerativeAI(model=name, temperature=0, max_retries=retries)

            agent = create_agent(
                gemini(MODEL, retries=1),
                tools,
                system_prompt=SYSTEM_PROMPT_FILE.read_text(encoding="utf-8"),
                middleware=[
                    ModelFallbackMiddleware(*(gemini(name, retries=0) for name in FALLBACK_MODELS)),
                    ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS, exit_behavior="end"),
                    ToolCallLimitMiddleware(tool_name="search", run_limit=MAX_SEARCHES, exit_behavior="continue"),
                ],
            )
            started = time.time()
            state = await agent.ainvoke({"messages": [{"role": "user", "content": question}]})
            seconds = time.time() - started

    messages = state["messages"]
    usage = {"input": 0, "output": 0}
    model_calls = 0
    for m in messages:
        meta = getattr(m, "usage_metadata", None)
        if meta:
            model_calls += 1
            usage["input"] += meta.get("input_tokens", 0)
            usage["output"] += meta.get("output_tokens", 0)
    final = next((m for m in reversed(messages) if m.type == "ai" and _text(m.content).strip()), None)
    answer = _text(final.content).strip() if final else ""
    if not answer:
        answer = "I could not produce an answer within the call limit."
    raw_answer = answer
    answer, guardrail = apply_guardrail(answer, trace)
    return {
        "question": question,
        "answer": answer,
        "raw_answer": raw_answer,  # before the guardrail; equal to answer unless it fired
        "trace": trace,
        "guardrail": guardrail,
        "model": (final.response_metadata.get("model_name") if final else None) or MODEL,
        "model_calls": model_calls,
        "tokens": usage,
        "seconds": round(seconds, 2),
    }


CITATION = re.compile(r"\[([a-z]+) ([^\]\[,;]+)\]")
RESULT_HEADER = re.compile(r"cite as \[([a-z]+) ([^\]]+)\].*\nSource: (.*?); label version ([\d-]+); (\S+)")


def retrieved_passages(trace: list[dict]) -> dict[tuple[str, str], dict]:
    """Every passage the searches returned, keyed by its citation (drug, section)."""
    passages = {}
    for step in trace:
        if step["tool"] == "search" and not step["error"]:
            for drug, section, source, version, url in RESULT_HEADER.findall(step["output"]):
                passages.setdefault((drug, section.strip()), {"source": source, "version": version, "url": url})
    return passages


def cited(answer: str) -> list[tuple[str, str]]:
    """Citations in an answer; '[amiodarone 7, warfarin 7.2]' style lists are split."""
    found = []
    for group in re.findall(r"\[([^\]]+)\]", answer):
        for part in re.split(r"[;,]\s*", group):
            match = CITATION.fullmatch(f"[{part.strip()}]")
            if match:
                found.append((match.group(1), match.group(2).strip()))
    return list(dict.fromkeys(found))


def run_agent(question: str, approve: Approver = ask_in_terminal) -> dict:
    """Answer one question. Returns the answer, the tool trace, tokens and seconds."""
    return asyncio.run(_run(question, approve))


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit('usage: python agent.py "your question"')
    result = run_agent(" ".join(sys.argv[1:]))
    print(result["answer"])
    passages = retrieved_passages(result["trace"])
    citations = cited(result["answer"])
    if citations:
        print("\nSources:")
        for drug, section in citations:
            p = passages.get((drug, section))
            print(f"  [{drug} {section}] {p['source']}, label version {p['version']}: {p['url']}" if p
                  else f"  [{drug} {section}] (not among the retrieved passages)")
    searches = [t for t in result["trace"] if t["tool"] == "search"]
    print(f"\n[{len(searches)} search(es), {result['model_calls']} model call(s), "
          f"{result['tokens']['input'] + result['tokens']['output']} tokens, {result['seconds']}s, {result['model']}]")
    if result["guardrail"]:
        print(f"[guardrail: {result['guardrail']}]")


if __name__ == "__main__":
    main()
