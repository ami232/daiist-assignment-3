"""
Assignment 3: the harness (`uv run python main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the two tools of server.py loaded over MCP (stdio) and
AGENTS.md as the system prompt.

Guardrails
- Approval: add_document only runs after a human types "y" (or AGENT_APPROVE=yes is set for a scripted
  run). Without a terminal and without that variable it is refused.
- Call limits: at most 8 model calls and 6 tool calls per question (LangChain middleware).
- Citation check (my extra guardrail): every [chunk id] in the final answer must be one that the search
  tool actually returned in this run, and a non-refusal answer must cite at least one. Otherwise the
  draft answer is withheld and replaced by a refusal, because for this user an unverifiable answer is
  worse than "I don't know".

`run_agent(question)` / `run_batch(questions)` return the answer and the full tool trace for evaluate.py.
"""

from __future__ import annotations

import asyncio
import os
import re
import sys
import time
from pathlib import Path

os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")

from api_key import load_api_key  # noqa: E402
from rag import AGENT_MODEL  # noqa: E402

ROOT = Path(__file__).resolve().parent
REFUSAL = "The corpus does not cover this question."
CITE_RE = re.compile(r"\[([A-Za-z0-9_.]+(?:-[A-Za-z0-9_.]+)*-[sf]\d{4})\]")
RESULT_HEAD = re.compile(r"^\[([^\]]+)\] (.+?) \| (.+)$", re.M)
MAX_MODEL_CALLS, MAX_TOOL_CALLS = 8, 6


def is_refusal(text: str) -> bool:
    t = text.lower()
    return "corpus does not cover" in t or "does not cover this question" in t


def _text(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(p.get("text", "") if isinstance(p, dict) else str(p) for p in content)
    return str(content)


def _approve(path: str) -> bool:
    mode = os.environ.get("AGENT_APPROVE", "").lower()
    if mode in {"yes", "y", "1"}:
        print(f"[approval] add_document({path!r}) approved via AGENT_APPROVE.", file=sys.stderr)
        return True
    if mode in {"no", "n", "0"}:
        print(f"[approval] add_document({path!r}) denied via AGENT_APPROVE.", file=sys.stderr)
        return False
    if sys.stdin and sys.stdin.isatty():
        print(f"\nThe agent wants to add this document to the index:\n  {path}\nApprove? [y/N] ",
              end="", file=sys.stderr, flush=True)
        return input().strip().lower() in {"y", "yes"}
    print("[approval] no terminal to ask for approval; add_document refused.", file=sys.stderr)
    return False


async def _answer(session, question: str) -> dict:
    """Answer one question using an open MCP session."""
    from langchain.agents import create_agent
    from langchain.agents.middleware import ModelCallLimitMiddleware, ToolCallLimitMiddleware
    from langchain_core.tools import StructuredTool
    from langchain_google_genai import ChatGoogleGenerativeAI

    trace: list[dict] = []
    retrieved: dict[str, tuple[str, str]] = {}

    async def search(query: str) -> str:
        """Search the EU drone-regulation corpus. Returns passages headed by [chunk id] source | location."""
        res = await session.call_tool("search", {"query": query})
        out = "\n".join(getattr(c, "text", "") for c in res.content)
        for cid, src, loc in RESULT_HEAD.findall(out):
            retrieved[cid] = (src, loc)
        trace.append({"tool": "search", "query": query, "ids": [m[0] for m in RESULT_HEAD.findall(out)],
                      "result": out})
        return out

    async def add_document(path: str) -> str:
        """Add a local file to the index. Only when the user explicitly asks; a human must approve."""
        if not _approve(path):
            out = "Not added: the human reviewer did not approve adding this document."
        else:
            res = await session.call_tool("add_document", {"path": path})
            out = "\n".join(getattr(c, "text", "") for c in res.content)
        trace.append({"tool": "add_document", "path": path, "result": out})
        return out

    tools = [StructuredTool.from_function(coroutine=search, name="search", description=search.__doc__),
             StructuredTool.from_function(coroutine=add_document, name="add_document",
                                          description=add_document.__doc__)]
    llm = ChatGoogleGenerativeAI(model=AGENT_MODEL, temperature=0, max_retries=6,
                                 google_api_key=load_api_key())
    agent = create_agent(
        llm, tools, system_prompt=(ROOT / "AGENTS.md").read_text(encoding="utf-8"),
        middleware=[ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS, exit_behavior="end"),
                    ToolCallLimitMiddleware(run_limit=MAX_TOOL_CALLS, exit_behavior="end")])

    started = time.time()
    state = await agent.ainvoke({"messages": [{"role": "user", "content": question}]},
                                config={"recursion_limit": 40})
    seconds = time.time() - started
    msgs = state["messages"]
    tokens_in = sum((getattr(m, "usage_metadata", None) or {}).get("input_tokens", 0) for m in msgs)
    tokens_out = sum((getattr(m, "usage_metadata", None) or {}).get("output_tokens", 0) for m in msgs)
    model_calls = sum(1 for m in msgs if m.type == "ai")
    draft = next((_text(m.content).strip() for m in reversed(msgs) if m.type == "ai" and _text(m.content).strip()), "")

    # ---- citation guardrail
    cited = list(dict.fromkeys(CITE_RE.findall(draft)))
    invalid = [c for c in cited if c not in retrieved]
    refused = is_refusal(draft) and not cited
    guardrail = None
    # An answer that only reports an add_document outcome is not a regulatory claim: no citation needed.
    doc_only = any(t["tool"] == "add_document" for t in trace) and not any(t["tool"] == "search" for t in trace)
    if doc_only:
        refused = False
    elif not draft:
        guardrail = "empty answer (call limit reached)"
    elif invalid:
        guardrail = f"cited ids never returned by search: {', '.join(invalid)}"
    elif not refused and not cited:
        guardrail = "answer without any citation"
    answer = draft
    if guardrail:
        answer = (f"{REFUSAL} (The harness withheld a draft answer: {guardrail}. "
                  f"Please check the regulation directly or ask again.)")
        refused, cited = True, []
    return {"question": question, "answer": answer, "draft": draft, "cited": cited, "refused": refused,
            "guardrail": guardrail, "trace": trace, "retrieved": retrieved, "seconds": round(seconds, 2),
            "tokens_in": tokens_in, "tokens_out": tokens_out, "model_calls": model_calls}


async def _with_session(questions: list[str], exclude_added: bool) -> list[dict]:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    env = {**os.environ, "CORPUS_EXCLUDE_ADDED": "1" if exclude_added else "0"}
    params = StdioServerParameters(command=sys.executable, args=[str(ROOT / "server.py")], cwd=str(ROOT), env=env)
    out = []
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            for q in questions:
                out.append(await _answer(session, q))
    return out


def run_batch(questions: list[str], exclude_added: bool = False) -> list[dict]:
    return asyncio.run(_with_session(questions, exclude_added))


def run_agent(question: str, exclude_added: bool = False) -> dict:
    return run_batch([question], exclude_added)[0]


def format_answer(result: dict) -> str:
    from index import url_for

    lines = [result["answer"]]
    if result["cited"]:
        lines.append("\nSources:")
        for cid in result["cited"]:
            src, loc = result["retrieved"][cid]
            url = url_for(cid.split("-")[0])
            lines.append(f"- [{cid}] {src}, {loc}" + (f" ({url})" if url else ""))
    if result["guardrail"]:
        lines.append(f"\n[guardrail fired: {result['guardrail']}]")
    lines.append(f"\n({result['model_calls']} model calls, {result['tokens_in'] + result['tokens_out']} tokens, "
                 f"{result['seconds']:.1f}s)")
    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) < 2 or not " ".join(sys.argv[1:]).strip():
        sys.exit('Usage: python agent.py "your question"')
    print(format_answer(run_agent(" ".join(sys.argv[1:]))))
