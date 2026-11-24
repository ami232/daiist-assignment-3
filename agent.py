"""
Assignment 3: the harness (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini; tools come from server.py over MCP (stdio);
AGENTS.md is the system prompt.

Guardrails
  1. Approval: add_document only runs after a human types "yes" (denied
     automatically when there is no terminal, e.g. in evaluate.py / check.py).
  2. Call limits: at most 6 tool calls and 8 model calls per question.
  3. Citation guard (own choice): every [SOURCE, LOCATION] in the answer must
     match a passage the search tool actually returned in this run. If an answer
     makes claims with no valid citation, the agent gets one chance to fix it;
     if it still fails, the answer is replaced by a refusal.

`answer(question)` returns the answer plus the tool trace, retrieved passages,
tokens and seconds, for evaluate.py.
"""

from __future__ import annotations

import asyncio
import os
import re
import sys
import time
from pathlib import Path

from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware, ToolCallLimitMiddleware, wrap_tool_call
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.tools import StructuredTool
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from pydantic import create_model

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
MODEL = os.environ.get("AGENT_MODEL", "gemini-3.5-flash-lite")
MAX_TOOL_CALLS, MAX_MODEL_CALLS = 6, 8
REFUSAL = "El corpus no cubre esta pregunta. / The corpus does not cover this question."

REFUSAL_RE = re.compile(
    r"no cubre|no contiene|no (?:se )?(?:menciona|regula|especifica|aborda|encuentra|incluye)|"
    r"does not cover|doesn't cover|not covered|does not (?:contain|mention|specify|address)|"
    r"no information|cannot answer|can't answer", re.I)
CITATION_RE = re.compile(r"\[([^\[\]]{3,250})\]")
HEADER_RE = re.compile(r"SOURCE: (.+?) \| LOCATION: (.+?)(?: \(part \d+\))? \| URL")


# --------------------------------------------------------------------------- citations

def article_key(location: str) -> str:
    """'Artículo 36. Fianza' -> 'artículo 36'; keeps the bit that identifies the provision."""
    loc = location.lower().split(" [")[0]
    return loc.split(".")[0].strip()


def parse_hits(tool_output: str) -> list[dict]:
    return [{"source": s.strip(), "location": l.strip()} for s, l in HEADER_RE.findall(tool_output)]


def check_citations(answer: str, hits: list[dict]) -> tuple[list[str], list[str]]:
    """(valid, invalid) citations: valid = names a retrieved source AND its article."""
    valid, invalid = [], []
    for cite in CITATION_RE.findall(answer):
        low = cite.lower()
        ok = any(h["source"].lower() in low and article_key(h["location"]) in low for h in hits)
        (valid if ok else invalid).append(cite)
    return valid, invalid


def is_refusal(answer: str) -> bool:
    return bool(REFUSAL_RE.search(answer[:400]))


# --------------------------------------------------------------------------- MCP tools

def mcp_to_langchain(session: ClientSession, tool) -> StructuredTool:
    props = (tool.input_schema or {}).get("properties", {})
    fields = {name: (str, ...) for name in props}
    args_model = create_model(f"{tool.name}_args", **fields)

    async def call(**kwargs) -> str:
        result = await session.call_tool(tool.name, kwargs)
        return "\n".join(getattr(c, "text", "") for c in result.content)

    return StructuredTool.from_function(coroutine=call, name=tool.name,
                                        description=tool.description or "", args_schema=args_model)


@wrap_tool_call
async def approve_add_document(request, handler):
    """Guardrail 1: a human must approve every add_document call."""
    call = request.tool_call
    if call["name"] != "add_document":
        return await handler(request)
    path = call["args"].get("path", "")
    if sys.stdin.isatty():
        reply = input(f"\nThe agent wants to add the document {path!r} to the index. Approve? [yes/no] ")
    else:
        reply = os.environ.get("AUTO_APPROVE_ADD", "no")  # no terminal: deny unless explicitly allowed
    if reply.strip().lower() in ("y", "yes", "s", "si", "sí"):
        print(f"[approved] add_document({path!r})", file=sys.stderr)
        return await handler(request)
    print(f"[denied] add_document({path!r})", file=sys.stderr)
    return ToolMessage(content="The user did NOT approve adding this document. Do not retry; tell the user.",
                       tool_call_id=call["id"], name="add_document")


# --------------------------------------------------------------------------- agent

def build_agent(tools):
    from langchain_google_genai import ChatGoogleGenerativeAI
    load_api_key()
    model = ChatGoogleGenerativeAI(model=MODEL, temperature=0, max_retries=6)
    return create_agent(
        model,
        tools=tools,
        system_prompt=(ROOT / "AGENTS.md").read_text(encoding="utf-8"),
        middleware=[
            approve_add_document,
            ToolCallLimitMiddleware(run_limit=MAX_TOOL_CALLS, exit_behavior="continue"),
            ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS, exit_behavior="end"),
        ],
    )


def collect(messages) -> dict:
    trace, hits, evidence, tokens = [], [], [], {"input": 0, "output": 0}
    for m in messages:
        if isinstance(m, AIMessage):
            for tc in m.tool_calls or []:
                trace.append({"tool": tc["name"], "args": tc["args"]})
            u = m.usage_metadata or {}
            tokens["input"] += u.get("input_tokens", 0)
            tokens["output"] += u.get("output_tokens", 0)
        elif isinstance(m, ToolMessage) and m.name == "search":
            out = m.text if hasattr(m, "text") else str(m.content)
            hits += parse_hits(out)
            evidence.append(out)
    final = next((m for m in reversed(messages) if isinstance(m, AIMessage) and not m.tool_calls), None)
    text = (final.text if final is not None else "").strip()
    return {"answer": text, "trace": trace, "hits": hits, "evidence": evidence, "tokens": tokens}


async def answer_async(question: str, session: ClientSession | None = None) -> dict:
    if session is None:
        params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT),
                                        env={**os.environ, "GEMINI_API_KEY": load_api_key()})
        async with stdio_client(params) as (r, w):
            async with ClientSession(r, w) as s:
                await s.initialize()
                return await answer_async(question, s)

    started = time.time()
    tools = [mcp_to_langchain(session, t) for t in (await session.list_tools()).tools]
    agent = build_agent(tools)
    state = await agent.ainvoke({"messages": [{"role": "user", "content": question}]})
    result = collect(state["messages"])

    # Guardrail 3: citation guard
    valid, invalid = check_citations(result["answer"], result["hits"])
    guard = "ok"
    if not is_refusal(result["answer"]) and (invalid or not valid):
        guard = "retried"
        fix = (f"Your answer has citations that do not match any retrieved passage: {invalid or 'none at all'}. "
               "Rewrite it citing only [SOURCE, LOCATION] exactly as in the search result headers, "
               "dropping any claim you cannot cite. If nothing retrieved supports an answer, say the corpus "
               "does not cover the question.")
        state = await agent.ainvoke({"messages": state["messages"] + [{"role": "user", "content": fix}]})
        retry = collect(state["messages"])
        retry["trace"] = result["trace"] + retry["trace"][len(result["trace"]):]
        result = retry
        valid, invalid = check_citations(result["answer"], result["hits"])
        if not is_refusal(result["answer"]) and (invalid or not valid):
            guard = "blocked"
            result["blocked_answer"] = result["answer"]
            result["answer"] = REFUSAL + " (Respuesta bloqueada: sus citas no coincidían con los pasajes recuperados.)"
    result.update(question=question, guard=guard, valid_citations=valid, invalid_citations=invalid,
                  refusal=is_refusal(result["answer"]), seconds=round(time.time() - started, 1))
    return result


def answer(question: str) -> dict:
    return asyncio.run(answer_async(question))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit('usage: python agent.py "your question"')
    r = answer(" ".join(sys.argv[1:]))
    print(r["answer"])
    if r["valid_citations"]:
        print("\nCitations:")
        for c in dict.fromkeys(r["valid_citations"]):
            print(f"  - [{c}]")
    print(f"\n({len(r['trace'])} tool calls, {r['tokens']['input'] + r['tokens']['output']} tokens, "
          f"{r['seconds']}s, citation guard: {r['guard']})", file=sys.stderr)
