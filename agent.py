"""
Assignment 3: the agent harness (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the tools of server.py over MCP (stdio) and
AGENTS.md as the system prompt.

Guardrails:
  1. Approval: add_document only runs after the user types "y" at the prompt.
     Without a terminal (e.g. during evaluation) it is refused.
  2. Call limits: at most 8 model calls and 6 search calls per question.
  3. Citation check (my extra guardrail): every [LAW, Article] in the answer must be one
     of the citations the search tool actually returned in this run, and a non-refusal
     answer must cite at least once. If not, the agent is told what was wrong and gets one
     retry; if it fails again, the answer is withheld and replaced by a refusal.

`run(question)` returns the answer plus its trace (tool calls, retrieved text, tokens,
seconds, guardrail events) for evaluate.py.
"""

from __future__ import annotations

import asyncio
import os
import re
import sys
import time
from contextlib import asynccontextmanager
from pathlib import Path

from langchain.agents import create_agent
from langchain.agents.middleware import (AgentMiddleware, ModelCallLimitMiddleware, ModelFallbackMiddleware,
                                         ToolCallLimitMiddleware)
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.tools import StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
SYSTEM_PROMPT = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.8-flash")
# Free-tier models often return 503 "high demand"; fall back to these, in order.
FALLBACKS = [m for m in os.environ.get("GEMINI_FALLBACKS", "gemini-3.6-flash,gemini-3.5-flash-lite").split(",") if m]

CITE_RE = re.compile(r"\[([A-ZÁÉÍÓÚ][\w/.\-]*),\s*([^\]\[]+?)\]")
OFFERED_RE = re.compile(r"cite as \[([^,\]]+),\s*([^\]]+)\]")
REFUSAL_RE = re.compile(r"no lo s[ée]|does not cover|no cubre|no contiene|no (?:aparece|figura|se regula)|"
                        r"no (?:puedo|es posible) (?:dar|responder|confirmar)|not covered|no incluye", re.I)
WITHHELD = ("No lo sé: no he podido dar una respuesta respaldada por citas válidas del corpus. "
            "Consulta el texto del BOE o a un profesional.")


def norm_cite(source: str, loc: str) -> tuple[str, str]:
    loc = re.sub(r"\s*\(parte \d+/\d+\)", "", loc.strip().rstrip("."))
    return source.strip(), re.sub(r"\s+", " ", loc).lower()


def is_refusal(answer: str) -> bool:
    return bool(REFUSAL_RE.search(answer[:400]))


# --------------------------------------------------------------------------- MCP tools as LangChain tools

def _mcp_tool_to_langchain(session: ClientSession, tool) -> StructuredTool:
    async def call(**kwargs) -> str:
        result = await session.call_tool(tool.name, kwargs)
        text = "\n".join(getattr(c, "text", "") for c in result.content)
        return f"ERROR: {text}" if getattr(result, "is_error", False) else text

    return StructuredTool(name=tool.name, description=tool.description or "", args_schema=tool.input_schema,
                          coroutine=call)


@asynccontextmanager
async def corpus_tools(base_only: bool = False):
    env = dict(os.environ)
    env["GEMINI_API_KEY"] = load_api_key()
    if base_only:
        env["CORPUS_BASE_ONLY"] = "1"
    params = StdioServerParameters(command=sys.executable, args=[str(ROOT / "server.py")], cwd=str(ROOT), env=env)
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = (await session.list_tools()).tools
            yield [_mcp_tool_to_langchain(session, t) for t in tools]


# --------------------------------------------------------------------------- approval guardrail

def ask_human(args: dict) -> bool:
    if not sys.stdin or not sys.stdin.isatty():
        return False
    print(f"\nThe agent wants to run add_document({args}).", file=sys.stderr)
    return input("Approve? [y/N] ").strip().lower() in ("y", "yes", "s", "si", "sí")


class ApproveAddDocument(AgentMiddleware):
    """Blocks add_document unless a human approves it."""

    def __init__(self, approver=ask_human):
        super().__init__()
        self.approver = approver
        self.events: list[str] = []

    async def awrap_tool_call(self, request, handler):
        call = request.tool_call
        if call["name"] == "add_document":
            ok = self.approver(call["args"])
            self.events.append(f"add_document({call['args']}) {'approved' if ok else 'REJECTED'}")
            if not ok:
                return ToolMessage(content="The user did not approve adding this document. Nothing was added. "
                                           "Tell the user it was not added.", tool_call_id=call["id"],
                                   name=call["name"])
        return await handler(request)


# --------------------------------------------------------------------------- run

def _collect(messages) -> dict:
    tool_calls, retrieved, offered = [], [], set()
    tokens_in = tokens_out = 0
    models = []
    for m in messages:
        if isinstance(m, AIMessage):
            for tc in m.tool_calls or []:
                tool_calls.append({"name": tc["name"], "args": tc["args"]})
            name = (m.response_metadata or {}).get("model_name")
            if name and name not in models:
                models.append(name)
            if m.usage_metadata:
                tokens_in += m.usage_metadata.get("input_tokens", 0)
                tokens_out += m.usage_metadata.get("output_tokens", 0)
        if isinstance(m, ToolMessage) and m.name == "search":
            text = m.text if isinstance(m.text, str) else str(m.content)
            retrieved.append(text)
            offered |= {norm_cite(s, l) for s, l in OFFERED_RE.findall(text)}
    final = next((m for m in reversed(messages) if isinstance(m, AIMessage) and not m.tool_calls), None)
    answer = (final.text if final else "").strip()
    return {"answer": answer, "tool_calls": tool_calls, "retrieved": retrieved, "offered": offered,
            "tokens_in": tokens_in, "tokens_out": tokens_out, "models_used": models}


def check_citations(answer: str, offered: set) -> list[str]:
    """Problems with the answer's citations; empty list if it passes."""
    cites = [norm_cite(s, l) for s, l in CITE_RE.findall(answer)]
    problems = [f"[{s}, {l}] was not in the search results" for s, l in cites if (s, l) not in offered]
    if not cites and not is_refusal(answer):
        problems.append("the answer makes claims but cites nothing")
    return problems


async def run_async(question: str, approver=ask_human, base_only: bool = False, tools=None) -> dict:
    started = time.time()
    load_api_key()
    model = ChatGoogleGenerativeAI(model=MODEL, temperature=0, max_retries=2)
    fallbacks = [ChatGoogleGenerativeAI(model=m, temperature=0, max_retries=2) for m in FALLBACKS]
    approval = ApproveAddDocument(approver)

    async def go(tool_list):
        agent = create_agent(model, tool_list, system_prompt=SYSTEM_PROMPT, middleware=[
            approval,
            *([ModelFallbackMiddleware(*fallbacks)] if fallbacks else []),
            ModelCallLimitMiddleware(run_limit=8, exit_behavior="end"),
            ToolCallLimitMiddleware(tool_name="search", run_limit=6, exit_behavior="continue"),
        ])
        messages = [HumanMessage(question)]
        state = await agent.ainvoke({"messages": messages})
        info = _collect(state["messages"])
        events = []
        problems = check_citations(info["answer"], info["offered"])
        if problems:
            events.append("citation check failed: " + "; ".join(problems))
            fix = HumanMessage("Your answer broke the citation rule: " + "; ".join(problems) +
                               ". Rewrite it citing only citations that appear in the search results "
                               "(search again if needed), or say the corpus does not cover it.")
            state = await agent.ainvoke({"messages": state["messages"] + [fix]})
            info = _collect(state["messages"])  # full history, so tokens include both attempts
            problems = check_citations(info["answer"], info["offered"])
            if problems:
                events.append("citation check failed again; answer withheld: " + "; ".join(problems))
                info["answer"] = WITHHELD
            else:
                events.append("citation check passed after retry")
        return info, events

    if tools is None:
        async with corpus_tools(base_only) as tool_list:
            info, events = await go(tool_list)
    else:
        info, events = await go(tools)
    info["offered"] = sorted(f"[{s}, {l}]" for s, l in info["offered"])
    info["guardrail_events"] = approval.events + events
    info["seconds"] = round(time.time() - started, 2)
    info["question"] = question
    info["model"] = MODEL
    return info


def run(question: str, **kwargs) -> dict:
    return asyncio.run(run_async(question, **kwargs))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit('usage: python agent.py "your question"')
    out = run(" ".join(sys.argv[1:]))
    print(out["answer"])
    print(f"\n---\nsearches: {sum(t['name'] == 'search' for t in out['tool_calls'])}, "
          f"tokens: {out['tokens_in']} in / {out['tokens_out']} out, {out['seconds']}s, "
          f"model: {', '.join(out['models_used']) or MODEL}")
    for e in out["guardrail_events"]:
        print(f"guardrail: {e}")
