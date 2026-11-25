"""
Assignment 3: your agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with tools from server.py over MCP and
AGENTS.md as system prompt.

Guardrails:
- approval: add_document runs only after a person types `y` (refused when no one is at the terminal);
- call limits: at most 8 model calls and 6 tool calls per run;
- citation check: every citation in the answer must match a passage the search tool
  returned. If not, the agent gets one retry; if it fails again the answer is withheld
  and replaced by a refusal.

evaluate.py uses open_agent() and run(), which return the answer and the tool trace.
"""

from __future__ import annotations

import asyncio
import os
import re
import sys
import time
from contextlib import asynccontextmanager
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SYSTEM_PROMPT = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
CHAT_MODEL = os.environ.get("GEMINI_CHAT_MODEL", "gemini-2.5-flash")
REFUSAL = "I don't know based on the documents."
MODEL_CALL_LIMIT, TOOL_CALL_LIMIT = 8, 6

CITATION = re.compile(r"\[([^\[\]]+?\.(?:pdf|txt|md|html?))\s*,\s*([^\[\]]+?)\]", re.I)
CHUNK_HEADER = re.compile(r"^--- \[\d+\] source: (.+?) \| location: (.+?) \| score: [-\d.]+$", re.M)


# ---------------------------------------------------------------- helpers (also used by evaluate.py)

def make_llm():
    from langchain_google_genai import ChatGoogleGenerativeAI
    from api_key import load_api_key
    return ChatGoogleGenerativeAI(model=CHAT_MODEL, google_api_key=load_api_key(), temperature=0, max_retries=8)


def text_of(content) -> str:
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(b.get("text", "") if isinstance(b, dict) else str(b) for b in content)
    return str(content or "")


def is_refusal(answer: str) -> bool:
    return "i don't know based on the documents" in answer.replace("’", "'").lower()


def loc_match(a: str, b: str) -> bool:
    """True if location `a` appears in `b` as whole words ('Article 5' is not in 'Article 50')."""
    a, b = a.strip().lower(), b.strip().lower()
    return bool(a) and re.search(rf"(?<!\w){re.escape(a)}(?!\w)", b) is not None


def locations_agree(cited: str, actual: str) -> bool:
    parts_c = [p for p in re.split(r"[,;]", cited) if p.strip()]
    parts_a = [p for p in re.split(r"[,;]| to ", actual) if p.strip()]
    return any(loc_match(c, a) or loc_match(a, c) for c in parts_c + [cited] for a in parts_a + [actual])


def citations_in(answer: str) -> list[tuple[str, str]]:
    return [(s.strip(), l.strip()) for s, l in CITATION.findall(answer)]


def citation_ok(citation: tuple[str, str], retrieved: list[dict]) -> bool:
    source, location = citation
    return any(r["source"].lower() == source.lower() and locations_agree(location, r["location"]) for r in retrieved)


def parse_search_output(text: str) -> list[dict]:
    headers = list(CHUNK_HEADER.finditer(text))
    out = []
    for i, m in enumerate(headers):
        end = headers[i + 1].start() if i + 1 < len(headers) else len(text)
        out.append({"source": m.group(1).strip(), "location": m.group(2).strip(), "text": text[m.end():end].strip()})
    return out


def summarize(messages) -> dict:
    """Final answer, tool trace, retrieved passages and token use from the message list."""
    from langchain_core.messages import AIMessage, ToolMessage
    trace, retrieved, tokens_in, tokens_out = [], [], 0, 0
    answer = ""
    for m in messages:
        if isinstance(m, AIMessage):
            usage = m.usage_metadata or {}
            tokens_in += usage.get("input_tokens", 0)
            tokens_out += usage.get("output_tokens", 0)
            for call in m.tool_calls:
                trace.append({"id": call["id"], "tool": call["name"], "args": call["args"]})
            if not m.tool_calls:
                answer = text_of(m.content).strip()
        elif isinstance(m, ToolMessage):
            content = text_of(m.content)
            for step in trace:
                if step["id"] == m.tool_call_id:
                    step["result"] = content[:2000]
            if m.name == "search":
                retrieved += parse_search_output(content)
    seen, unique = set(), []
    for r in retrieved:
        key = (r["source"], r["location"], r["text"][:80])
        if key not in seen:
            seen.add(key)
            unique.append(r)
    return {"answer": answer, "trace": trace, "retrieved": unique, "tokens_in": tokens_in, "tokens_out": tokens_out}


# ---------------------------------------------------------------- approval

def ask_approval(args: dict) -> bool:
    if not sys.stdin.isatty():
        print("add_document refused: no one is at the terminal to approve it.", file=sys.stderr)
        return False
    reply = input(f"\nThe agent wants to run add_document on {args.get('path')!r}. Approve? [y/N] ")
    return reply.strip().lower() in ("y", "yes")


def build_agent(tools):
    from langchain.agents import create_agent
    from langchain.agents.middleware import ModelCallLimitMiddleware, ToolCallLimitMiddleware, wrap_tool_call
    from langchain_core.messages import ToolMessage

    @wrap_tool_call
    async def require_approval(request, handler):
        call = request.tool_call
        if call["name"] == "add_document" and not await asyncio.to_thread(ask_approval, call["args"]):
            return ToolMessage(
                content="The user did not approve add_document, so nothing was added. Tell the user.",
                tool_call_id=call["id"], name=call["name"], status="error",
            )
        return await handler(request)

    return create_agent(
        model=make_llm(),
        tools=tools,
        system_prompt=SYSTEM_PROMPT,
        middleware=[
            require_approval,
            ModelCallLimitMiddleware(run_limit=MODEL_CALL_LIMIT),
            ToolCallLimitMiddleware(run_limit=TOOL_CALL_LIMIT),
        ],
    )


def _mcp_caller(session, name: str):
    from langchain_core.tools import ToolException

    async def call(**arguments) -> str:
        result = await session.call_tool(name, arguments)
        text = "\n".join(getattr(c, "text", "") for c in result.content).strip()
        if getattr(result, "is_error", False) or getattr(result, "isError", False):
            raise ToolException(text or f"{name} failed")
        return text
    return call


@asynccontextmanager
async def open_agent():
    """Start server.py once over stdio, wrap its MCP tools as LangChain tools, yield the agent."""
    from langchain_core.tools import StructuredTool
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    params = StdioServerParameters(command=sys.executable, args=[str(ROOT / "server.py")],
                                   cwd=str(ROOT), env=dict(os.environ))
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = []
            for t in (await session.list_tools()).tools:
                schema = getattr(t, "input_schema", None) or getattr(t, "inputSchema", None) or {"type": "object"}
                tools.append(StructuredTool(
                    name=t.name, description=t.description or t.name, args_schema=schema,
                    coroutine=_mcp_caller(session, t.name), handle_tool_error=True,
                ))
            yield build_agent(tools)


# ---------------------------------------------------------------- run

async def run(agent, question: str) -> dict:
    """Answer one question. Returns answer, citations, trace, retrieved passages, tokens, seconds."""
    from langchain_core.messages import HumanMessage
    started = time.time()
    state = await agent.ainvoke({"messages": [HumanMessage(question)]})
    result = summarize(state["messages"])
    guardrail = "passed"

    def problems(res):
        cites = citations_in(res["answer"])
        bad = [c for c in cites if not citation_ok(c, res["retrieved"])]
        if is_refusal(res["answer"]) and not cites:
            return []
        if not cites:
            return ["the answer has no citations"]
        return [f"[{s}, {l}] does not match any passage the search returned" for s, l in bad]

    issues = problems(result)
    if issues:
        nudge = ("Your answer failed the citation check: " + "; ".join(issues) + ". Answer again using only the "
                 "passages the search tool returned, citing each claim as [source, location] exactly as in their "
                 f"headers. If they do not contain the answer, reply: {REFUSAL}")
        state = await agent.ainvoke({"messages": state["messages"] + [HumanMessage(nudge)]})
        result = summarize(state["messages"])
        issues = problems(result)
        guardrail = "retried"
        if issues:
            result["withheld"] = result["answer"]
            result["answer"] = f"{REFUSAL} (A drafted answer was withheld because its citations did not match the retrieved passages.)"
            guardrail = "blocked"

    if not result["answer"]:
        result["answer"] = f"{REFUSAL} (The agent stopped before answering, probably at the call limit.)"
        guardrail = "no answer"

    cites = citations_in(result["answer"])
    result.update(
        question=question,
        citations=[{"source": s, "location": l, "valid": citation_ok((s, l), result["retrieved"])} for s, l in cites],
        refused=is_refusal(result["answer"]),
        guardrail=guardrail,
        seconds=round(time.time() - started, 2),
    )
    return result


async def ask(question: str) -> dict:
    async with open_agent() as agent:
        return await run(agent, question)


def main() -> None:
    if len(sys.argv) < 2 or not " ".join(sys.argv[1:]).strip():
        raise SystemExit('Usage: python agent.py "your question"')
    result = asyncio.run(ask(" ".join(sys.argv[1:])))
    print(result["answer"])
    if result["citations"]:
        print("\nSources:")
        for c in dict.fromkeys((c["source"], c["location"], c["valid"]) for c in result["citations"]):
            print(f"- {c[0]}, {c[1]}" + ("" if c[2] else "  (not in retrieved passages)"))
    searches = sum(t["tool"] == "search" for t in result["trace"])
    print(f"\n[{searches} search call(s), {result['tokens_in']}+{result['tokens_out']} tokens, "
          f"{result['seconds']}s, citation guardrail: {result['guardrail']}]")


if __name__ == "__main__":
    main()
