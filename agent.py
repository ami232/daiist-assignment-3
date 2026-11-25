"""
Assignment 3: the agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with server.py's tools over MCP (stdio)
and AGENTS.md as the system prompt.

Guardrails:
- approval: add_document is gated by HumanInTheLoopMiddleware. In a terminal
  you are asked y/N; without a terminal it is rejected unless you pass
  --approve-add (or set APPROVE_ADD=1).
- call limits: at most 6 tool calls and 8 model calls per question.
- citation check (extra guardrail): every [SOURCE, location] in the answer must
  be one of the passages search actually returned in this run, and any
  non-refusal answer must cite something. If not, the agent gets one chance
  to fix it; if it still fails, the answer is replaced by a refusal that lists
  the passages it did retrieve.

`ask(question)` returns the answer plus the tool trace, tokens and seconds
(evaluate.py uses it).
"""

from __future__ import annotations

import argparse
import asyncio
import json
import os
import re
import sys
import time
import uuid
from pathlib import Path

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
AGENTS_MD = ROOT / "AGENTS.md"
# flash-lite: ~5-10 s a question on the free tier; 3.5-flash took 80-130 s
# under load and allows only 20 requests a day. If Gemini fails, Groq takes over.
AGENT_MODEL = os.environ.get("AGENT_MODEL", "gemini-3.5-flash-lite")
FALLBACK_MODEL = os.environ.get("AGENT_FALLBACK_MODEL", "groq:openai/gpt-oss-120b")
MAX_TOOL_CALLS = 6
MAX_MODEL_CALLS = 8
REFUSAL = "The corpus does not cover this."

BRACKET = re.compile(r"\[([^\[\]]+)\]")
# one "SOURCE, location" inside a bracket; a bracket may hold several
# ("[LSV, Artículo 63; LSV, Anexo II]"), split where a new SOURCE, starts
ONE_CITATION = re.compile(r"([A-Z][A-Za-z0-9-]*)\s*,\s*(.+?)(?=\s*[;,]\s*[A-Z][A-Za-z0-9-]*\s*,|$)")
RESULT_HEADER = re.compile(r"^\[([A-Za-z][\w-]*), ([^\]]+)\]", re.M)


def parse_citations(text: str) -> list[tuple[str, str]]:
    out = []
    text = " ".join(text.replace("\u200b", "").split(" "))
    # models sometimes write "Artículo\u202f4" (narrow no-break space): normalise all spaces
    text = re.sub(r"[\u00a0\u2000-\u200a\u202f\u205f\u3000]", " ", text)
    for inner in BRACKET.findall(text):
        for s, l in ONE_CITATION.findall(inner.strip().strip("`")):
            if re.match(r"(Art[íi]culo|Anexo|Disposici[óo]n|Norma|Pre[áa]mbulo)", l.strip()):
                out.append((s, l.strip().rstrip(".")))
    return out


def citation_ok(cited: tuple[str, str], allowed: set[tuple[str, str]]) -> bool:
    """Exact match, or a sub-reference of a retrieved article
    ('Artículo 76.z3' or 'Artículo 20.1' when 'Artículo 76' / 'Artículo 20' was retrieved)."""
    s, l = cited
    return any(s == rs and (l == rl or l.startswith((rl + ".", rl + " ", rl + ","))) for rs, rl in allowed)


def log(*a) -> None:
    print(*a, file=sys.stderr, flush=True)


# ------------------------------------------------------------------ MCP -> LangChain

def _mcp_tool(session, tool):
    """Wrap one MCP tool as a LangChain tool that calls it over the session."""
    from langchain_core.tools import StructuredTool

    async def call(**kwargs):
        res = await session.call_tool(tool.name, kwargs)
        text = "\n".join(getattr(c, "text", "") for c in res.content)
        return ("Error: " + text) if getattr(res, "is_error", False) else text

    schema = dict(tool.input_schema or {"type": "object", "properties": {}})
    schema.setdefault("title", tool.name)
    schema.setdefault("description", tool.description or "")
    return StructuredTool(name=tool.name, description=tool.description or "", args_schema=schema,
                          coroutine=call, func=None)


def _model(name: str):
    if name.startswith("groq:"):
        from langchain_groq import ChatGroq
        from llm import groq_key
        groq_key()
        return ChatGroq(model=name.removeprefix("groq:"), temperature=0, max_retries=2, timeout=90)
    from langchain_google_genai import ChatGoogleGenerativeAI
    kwargs = dict(model=name, max_retries=2, timeout=90)
    if "lite" not in name:  # lite models ignore temperature and have no thinking levels
        kwargs.update(temperature=0, thinking_level="low")
    return ChatGoogleGenerativeAI(**kwargs)


def _fallback_available() -> bool:
    if not FALLBACK_MODEL.startswith("groq:"):
        return True
    from llm import groq_key
    return bool(groq_key())


def build_agent(tools):
    from langchain.agents import create_agent
    from langchain.agents.middleware import (HumanInTheLoopMiddleware, ModelCallLimitMiddleware,
                                             ModelFallbackMiddleware, ToolCallLimitMiddleware)
    from langgraph.checkpoint.memory import InMemorySaver

    return create_agent(
        _model(AGENT_MODEL),
        tools=tools,
        system_prompt=AGENTS_MD.read_text(encoding="utf-8"),
        middleware=[
            HumanInTheLoopMiddleware(
                interrupt_on={"add_document": {"allowed_decisions": ["approve", "reject"]}},
                description_prefix="The agent wants to change the shared index",
            ),
            ToolCallLimitMiddleware(run_limit=MAX_TOOL_CALLS, exit_behavior="continue"),
            ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS, exit_behavior="end"),
            *([ModelFallbackMiddleware(_model(FALLBACK_MODEL))] if _fallback_available() else []),
        ],
        checkpointer=InMemorySaver(),
    )


# ------------------------------------------------------------------ guardrail

def retrieved_citations(trace: list[dict]) -> set[tuple[str, str]]:
    got = set()
    for t in trace:
        if t["tool"] == "search":
            got |= {(s, l.strip()) for s, l in RESULT_HEADER.findall(t["result"])}
    return got


def check_citations(answer: str, trace: list[dict]) -> list[str]:
    """Problems with the answer's citations; empty list = passes."""
    cited = parse_citations(answer)
    allowed = retrieved_citations(trace)
    problems = [f"[{s}, {l}] was not among the passages you retrieved" for s, l in cited if not citation_ok((s, l), allowed)]
    refusal = answer.strip().startswith(REFUSAL)
    searched = any(t["tool"] == "search" for t in trace)
    if not refusal and not cited and searched:
        problems.append("the answer makes claims but cites no passage")
    return problems


# ------------------------------------------------------------------ run

def _approve(requests: list[dict], auto: bool | None) -> list[dict]:
    decisions = []
    for r in requests:
        args = json.dumps(r.get("args", {}), ensure_ascii=False)
        if auto is None and sys.stdin.isatty():
            print(f"\nThe agent wants to run {r['name']}({args}). Allow? [y/N] ", end="", file=sys.stderr, flush=True)
            ok = sys.stdin.readline().strip().lower() in ("y", "yes")
        else:
            ok = bool(auto)
            log(f"{'Approved' if ok else 'Rejected'} {r['name']}({args}) "
                f"({'--approve-add' if ok else 'no terminal to ask; pass --approve-add to allow'})")
        decisions.append({"type": "approve"} if ok else
                         {"type": "reject", "message": "The user did not approve adding this document. Do not retry; answer without it."})
    return decisions


async def _run(question: str, approve_add: bool | None) -> dict:
    from langchain_core.messages import AIMessage, ToolMessage
    from langgraph.types import Command
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    load_api_key()
    started = time.time()
    params = StdioServerParameters(command=sys.executable, args=[str(ROOT / "server.py")], cwd=str(ROOT),
                                   env={**os.environ})
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = [_mcp_tool(session, t) for t in (await session.list_tools()).tools]
            agent = build_agent(tools)
            config = {"configurable": {"thread_id": str(uuid.uuid4())}, "recursion_limit": 40}

            async def invoke(payload):
                result = await agent.ainvoke(payload, config, version="v2")
                while getattr(result, "interrupts", None):
                    intr = result.interrupts[0]
                    decisions = _approve(intr.value["action_requests"], approve_add)
                    result = await agent.ainvoke(Command(resume={"decisions": decisions}), config, version="v2")
                return result

            def messages_of(result):
                state = getattr(result, "value", result)
                return state["messages"]

            result = await invoke({"messages": [{"role": "user", "content": question}]})
            msgs = messages_of(result)

            def collect(msgs):
                trace, calls = [], {}
                for m in msgs:
                    if isinstance(m, AIMessage):
                        for tc in m.tool_calls or []:
                            calls[tc["id"]] = tc
                    if isinstance(m, ToolMessage):
                        tc = calls.get(m.tool_call_id, {})
                        trace.append({"tool": tc.get("name", m.name), "args": tc.get("args", {}),
                                      "result": m.content if isinstance(m.content, str) else str(m.content)})
                return trace

            def final_text(msgs):
                for m in reversed(msgs):
                    if isinstance(m, AIMessage) and not m.tool_calls:
                        c = m.content
                        if isinstance(c, list):
                            c = "".join(p.get("text", "") if isinstance(p, dict) else str(p) for p in c)
                        if c.strip():
                            return c.strip()
                return ""

            trace = collect(msgs)
            answer = final_text(msgs)
            problems = check_citations(answer, trace)
            guardrail = {"fired": bool(problems), "problems": problems, "action": "none"}
            if problems:
                log("Citation check failed: " + "; ".join(problems))
                fix = ("Your answer failed the citation check: " + "; ".join(problems) +
                       ". Rewrite it citing only the passages you retrieved, exactly as their headers are written, "
                       f"or start with '{REFUSAL}' if they do not answer the question.")
                result = await invoke({"messages": [{"role": "user", "content": fix}]})
                msgs = messages_of(result)
                trace = collect(msgs)
                answer = final_text(msgs)
                still = check_citations(answer, trace)
                guardrail["action"] = "rewritten"
                if still:
                    seen = ", ".join(f"[{s}, {l}]" for s, l in sorted(retrieved_citations(trace))) or "none"
                    answer = (f"{REFUSAL} I could not give an answer backed by valid citations. "
                              f"Passages retrieved: {seen}.")
                    guardrail.update(action="replaced_with_refusal", problems=problems + still)

            tokens = {"input": 0, "output": 0}
            model_calls = 0
            models_used = set()
            for m in msgs:
                if isinstance(m, AIMessage) and m.usage_metadata:
                    model_calls += 1
                    models_used.add((m.response_metadata or {}).get("model_name") or AGENT_MODEL)
                    tokens["input"] += m.usage_metadata.get("input_tokens", 0)
                    tokens["output"] += m.usage_metadata.get("output_tokens", 0)

    return {
        "question": question,
        "answer": answer,
        "citations": sorted({f"[{s}, {l}]" for s, l in parse_citations(answer)}),
        "refusal": answer.strip().startswith(REFUSAL),
        "trace": trace,
        "guardrail": guardrail,
        "tokens": tokens,
        "model_calls": model_calls,
        "seconds": round(time.time() - started, 1),
        "model": AGENT_MODEL,
        "models_used": sorted(models_used),
    }


def ask(question: str, approve_add: bool | None = None) -> dict:
    """Answer one question. approve_add: None = ask in the terminal (reject if
    there is none), True/False = decide without asking."""
    return asyncio.run(_run(question, approve_add))


def sources_block(result: dict) -> str:
    """URLs for each cited passage, taken from the search results."""
    urls = {}
    for t in result["trace"]:
        for block in t["result"].split("\n---\n"):
            head = RESULT_HEADER.search(block)
            url = re.search(r"https://www\.boe\.es/\S+", block)
            if head and url:
                urls[f"[{head.group(1)}, {head.group(2).strip()}]"] = url.group(0)
    lines = [f"  {c} {urls.get(c, '')}".rstrip() for c in result["citations"]]
    return "Sources:\n" + "\n".join(lines) if lines else ""


def main() -> None:
    ap = argparse.ArgumentParser(description="Ask the Spanish traffic-law assistant.")
    ap.add_argument("question", nargs="+")
    ap.add_argument("--approve-add", action="store_true", default=os.environ.get("APPROVE_ADD") == "1",
                    help="allow add_document without asking")
    ap.add_argument("--json", action="store_true", help="print the full result as JSON")
    a = ap.parse_args()
    r = ask(" ".join(a.question), approve_add=True if a.approve_add else None)
    if a.json:
        print(json.dumps(r, ensure_ascii=False, indent=1))
        return
    print(r["answer"])
    src = sources_block(r)
    if src:
        print("\n" + src)
    searches = [t["args"].get("query") for t in r["trace"] if t["tool"] == "search"]
    print(f"\n({len(searches)} search(es), {r['tokens']['input']}+{r['tokens']['output']} tokens, {r['seconds']}s"
          + (", citation guardrail: " + r["guardrail"]["action"] if r["guardrail"]["fired"] else "") + ")")


if __name__ == "__main__":
    main()
