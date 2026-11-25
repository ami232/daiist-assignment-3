"""
Assignment 3: the agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini. Its tools come from server.py over MCP
(stdio), exactly as an editor would start it, and AGENTS.md is the system prompt.

Safety rails:
- approval:   add_document only runs after a human types "y" in the terminal.
              With no terminal (evaluation, CI) it is refused.
- call limit: at most 8 model calls and 6 tool calls per question.
- guardrail:  citation check. Every [Page § Section] in the answer must be a
              passage the search tool actually returned in this run. Citations
              that were not retrieved are removed; an answer left with no valid
              citation (and which is not a refusal) is replaced by a refusal.

ask(question) returns the answer plus the tool trace, tokens and seconds,
for evaluate.py.
"""

from __future__ import annotations

import asyncio
import os
import re
import sys
import time
from pathlib import Path

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
AGENTS_MD = ROOT / "AGENTS.md"
# gemini-3.5-flash and the newer Flash models timed out or returned 503 "high demand" on the free
# tier (25 Nov 2026); the Lite models answered in under a second. FALLBACK_MODEL is tried on errors.
MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite")
FALLBACK_MODEL = os.environ.get("GEMINI_FALLBACK_MODEL", "gemini-flash-lite-latest")
MAX_MODEL_CALLS, MAX_TOOL_CALLS = 8, 6

REFUSAL = "The wiki does not cover this."
REFUSAL_PATTERNS = re.compile(
    r"wiki does not cover|does not cover|doesn't cover|not covered|no information|"
    r"cannot find|can't find|could not find|couldn't find|does not (?:say|mention|state)|"
    r"doesn't (?:say|mention|state)|i don't know|not in the (?:wiki|corpus)",
    re.IGNORECASE,
)
CITATION = re.compile(r"\[([^\[\]]*§[^\[\]]*)\]")  # a bracket with at least one "Page § Section"


def parse_citations(text: str) -> list[str]:
    """Every 'Page § Section' in the text. Models often group several in one bracket:
    [A § X, B § Y] or [A § X; B § Y], so a bracket is split into its parts."""
    out = []
    for inner in CITATION.findall(text):
        for part in re.split(r"\s*[;,]\s*(?=[^;,§]*§)", inner):
            if "§" in part:
                page, _, section = part.partition("§")
                out.append(f"{page.strip()} § {section.strip()}")
    return out


def is_refusal(answer: str) -> bool:
    return bool(REFUSAL_PATTERNS.search(answer))


def _norm(s: str) -> str:
    s = re.sub(r"\s+", " ", s).strip().lower()
    return re.sub(r"\b([^>§]+?) > \1 >", r"\1 >", s)  # "Stats > Stats > Damage" -> "Stats > Damage"


def retrieved_citations(trace: list[dict]) -> dict[str, tuple[str, str]]:
    """{normalised 'page § section': ('[Page § Section]', url)} for every section of every passage
    search returned in this run (a passage can cover several sections)."""
    found = {}
    pattern = re.compile(r"cite as: \[([^\[\]]+?) § ([^\[\]]+?)\](?:\ncovers: (.+?) \(cite any.*?\))?\nurl: (\S*)")
    for step in trace:
        if step["tool"] != "search":
            continue
        for m in pattern.finditer(step["result"]):
            page, first, covers, url = m.groups()
            for section in ([c.strip() for c in covers.split(" / ")] if covers else [first]):
                found[_norm(f"{page} § {section}")] = (f"[{page} § {section}]", url)
    return found


def _match(key: str, allowed: dict) -> str | None:
    """Exact match, or a parent/child of a retrieved section ('Stats' for 'Stats > Effects')."""
    if key in allowed:
        return key
    page, _, section = key.partition(" § ")
    for k in allowed:
        p2, _, s2 = k.partition(" § ")
        if p2 == page and (s2.startswith(section + " >") or section.startswith(s2 + " >")):
            return k
    return None


def citation_guardrail(answer: str, trace: list[dict]) -> tuple[str, list[str], str | None]:
    """Return (answer, valid citations, note on what the guardrail did)."""
    if any(step["tool"] == "add_document" for step in trace) and not any(step["tool"] == "search" for step in trace):
        return answer, [], None  # reporting an action (adding a file), not answering from the wiki
    allowed = retrieved_citations(trace)
    valid, removed = [], []

    def keep_or_drop(m: re.Match) -> str:
        kept = []
        for c in parse_citations(m.group(0)):
            key = _match(_norm(c), allowed)
            if key:
                kept.append(c)
                if key not in valid:
                    valid.append(key)
            else:
                removed.append(f"[{c}]")
        return " ".join(f"[{c}]" for c in kept)

    checked = CITATION.sub(keep_or_drop, answer).strip()
    if not valid and not is_refusal(checked):
        return (f"{REFUSAL} I could not back an answer with a passage from the wiki, so I won't guess.",
                [], "blocked: answer had no citation to a retrieved passage")
    note = f"removed {len(removed)} citation(s) not returned by search: {', '.join(removed)}" if removed else None
    return checked, valid, note


def terminal_approval(path: str) -> bool:
    if not sys.stdin.isatty():
        return False
    print(f"\nThe agent wants to add {path!r} to the index (this embeds it with Gemini).", file=sys.stderr)
    return input("Allow? [y/N] ").strip().lower() in ("y", "yes")


def _text(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(p.get("text", "") if isinstance(p, dict) else str(p) for p in content)
    return str(content)


async def ask_async(question: str, approve=terminal_approval) -> dict:
    from langchain.agents import create_agent
    from langchain.agents.middleware import ModelCallLimitMiddleware, ModelFallbackMiddleware, ToolCallLimitMiddleware
    from langchain_core.tools import StructuredTool
    from langchain_google_genai import ChatGoogleGenerativeAI
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    load_api_key()
    trace: list[dict] = []
    started = time.time()

    params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT))
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            mcp_tools = (await session.list_tools()).tools

            def make_tool(t):
                async def call(**kwargs):
                    t0 = time.time()
                    if t.name == "add_document" and not approve(kwargs.get("path", "")):
                        text = f"Not run: the user did not approve adding {kwargs.get('path')!r}."
                    else:
                        result = await session.call_tool(t.name, kwargs)
                        text = "\n".join(getattr(c, "text", "") for c in result.content)
                    trace.append({"tool": t.name, "args": kwargs, "result": text,
                                  "seconds": round(time.time() - t0, 2)})
                    return text
                return StructuredTool(name=t.name, description=t.description or "",
                                      args_schema=t.input_schema, coroutine=call)

            agent = create_agent(
                model=ChatGoogleGenerativeAI(model=MODEL, timeout=60, max_retries=2),
                tools=[make_tool(t) for t in mcp_tools],
                system_prompt=AGENTS_MD.read_text(encoding="utf-8"),
                middleware=[
                    ModelFallbackMiddleware(ChatGoogleGenerativeAI(model=FALLBACK_MODEL, timeout=60, max_retries=2)),
                    ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS, exit_behavior="end"),
                    ToolCallLimitMiddleware(run_limit=MAX_TOOL_CALLS, exit_behavior="continue"),
                ],
            )
            state = await agent.ainvoke({"messages": [{"role": "user", "content": question}]})

    messages = state["messages"]
    tokens = {"input": 0, "output": 0, "total": 0}
    for m in messages:
        usage = getattr(m, "usage_metadata", None) or {}
        tokens["input"] += usage.get("input_tokens", 0)
        tokens["output"] += usage.get("output_tokens", 0)
        tokens["total"] += usage.get("total_tokens", 0)
    final = next((m for m in reversed(messages) if m.type == "ai" and _text(m.content).strip()), None)
    raw_answer = _text(final.content).strip() if final else ""

    answer, cited, guardrail = citation_guardrail(raw_answer, trace)
    urls = retrieved_citations(trace)
    return {
        "question": question,
        "answer": answer,
        "raw_answer": raw_answer,
        "citations": [urls[c][0] for c in cited],
        "sources": {urls[c][0]: urls[c][1] for c in cited},
        "refused": is_refusal(answer),
        "guardrail": guardrail,
        "trace": trace,
        "tokens": tokens,
        "model_calls": sum(1 for m in messages if m.type == "ai"),
        "seconds": round(time.time() - started, 2),
        "model": MODEL,
    }


def ask(question: str, approve=terminal_approval) -> dict:
    return asyncio.run(ask_async(question, approve))


def main() -> None:
    question = " ".join(sys.argv[1:]).strip()
    if not question:
        raise SystemExit('usage: python agent.py "your question"')
    r = ask(question)
    print(r["answer"])
    if r["sources"]:
        print("\nSources:")
        for c, url in r["sources"].items():
            print(f"- {c}  {url}")
    if r["guardrail"]:
        print(f"\n(guardrail: {r['guardrail']})")
        print(f"(answer before the guardrail: {r['raw_answer'][:600]!r})", file=sys.stderr)
    print(f"\n[{len(r['trace'])} tool call(s), {r['tokens']['total']} tokens, {r['seconds']}s, {r['model']}]")


if __name__ == "__main__":
    main()
