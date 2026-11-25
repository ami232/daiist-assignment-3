"""
Assignment 3: your agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with tools from server.py over MCP and
AGENTS.md as system prompt.

Guardrails (all in this file):
  1. Approval: add_document never runs without the user's explicit yes (`approve` callback).
  2. Call limit: at most MAX_TOOL_CALLS tool calls per question (ToolCallLimitMiddleware).
  3. Citation check (my own guardrail): every [SOURCE, location] in the answer must be one the
     search tool actually returned in this run. Otherwise the model gets one chance to fix the
     answer; if it still cites something it never retrieved, the answer is replaced by a refusal.

`ask(question, approve=None)` returns the answer plus the tool trace, tokens and seconds, for evaluate.py.
"""

import asyncio
import os
import re
import sys
import time
from pathlib import Path

from langchain.agents import create_agent
from langchain.agents.middleware import ToolCallLimitMiddleware
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.tools import StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash")   # gemini-2.5-flash is closed to new users
MAX_TOOL_CALLS = 6
REFUSAL_TEXT = ("No puedo dar una respuesta verificada: no encuentro un apoyo suficiente en los "
                "documentos indexados. / I cannot give a verified answer: the indexed documents do "
                "not support one.")
CITATION = re.compile(r"\[([^\[\]]+?),\s*([^\[\]]+?)\]")
HEADER = re.compile(r"^\[\d+\]\s+\[([^\[\]]+?),\s*([^\[\]]+?)\]", re.M)
REFUSAL = re.compile(r"no (?:puedo|encuentro|figura|aparece|está cubiert|se (?:recoge|prevé))|"
                     r"not (?:covered|found|addressed)|cannot (?:find|answer)|don't know|no sé", re.I)


def cli_approve(path: str) -> bool:
    """Ask the user in the terminal before add_document runs."""
    if not sys.stdin.isatty():
        return False
    print(f"\nThe agent wants to ADD this document to the corpus: {path}", file=sys.stderr)
    return input("Approve? [y/N] ").strip().lower() in {"y", "yes", "s", "si", "sí"}


def retrieved_citations(trace: list[dict]) -> set[tuple[str, str]]:
    """(source, location) pairs that search results contained."""
    found = set()
    for call in trace:
        if call["tool"] == "search":
            found |= {(s.strip(), l.strip()) for s, l in HEADER.findall(call["result"])}
    return found


def base_location(location: str) -> str:
    """'Artículo 36.5' / 'Artículo 36, apartado 2' -> 'Artículo 36': citing a paragraph of a
    retrieved article is valid, so compare articles, not paragraphs."""
    return re.split(r"(?<=\d)\.\d|,\s*\d|\s+(?:apartado|párrafo|letra|apdo)\b", location)[0].strip()


def check_citations(answer: str, trace: list[dict]) -> dict:
    """Code-checkable facts about an answer's citations (also used by evaluate.py)."""
    cited = [(s.strip(), l.strip()) for s, l in CITATION.findall(answer)]
    valid = {(s, base_location(l)) for s, l in retrieved_citations(trace)}
    invalid = [c for c in dict.fromkeys(cited) if (c[0], base_location(c[1])) not in valid]
    return {"cited": cited, "invalid": invalid, "refusal": bool(REFUSAL.search(answer)),
            "ok": not invalid and (bool(cited) or bool(REFUSAL.search(answer)))}


def load_system_prompt() -> str:
    return (ROOT / "AGENTS.md").read_text(encoding="utf-8")


def make_tools(session: ClientSession, mcp_tools: list, approve, trace: list[dict]) -> list[StructuredTool]:
    tools = []
    for spec in mcp_tools:
        async def call(_name=spec.name, **kwargs) -> str:
            if _name == "add_document" and not approve(kwargs.get("path", "")):
                text = "The user did NOT approve adding this document. Nothing was added."
            else:
                result = await session.call_tool(_name, kwargs)
                text = "\n".join(getattr(c, "text", "") for c in result.content)
            trace.append({"tool": _name, "args": kwargs, "result": text})
            return text
        tools.append(StructuredTool.from_function(
            coroutine=call, name=spec.name, description=spec.description or spec.name,
            args_schema=spec.input_schema))
    return tools


def usage(messages: list) -> dict:
    inp = out = 0
    for m in messages:
        if isinstance(m, AIMessage) and m.usage_metadata:
            inp += m.usage_metadata.get("input_tokens", 0)
            out += m.usage_metadata.get("output_tokens", 0)
    return {"input_tokens": inp, "output_tokens": out}


def text_of(message) -> str:
    content = message.content
    if isinstance(content, list):
        return "".join(p.get("text", "") if isinstance(p, dict) else str(p) for p in content).strip()
    return str(content).strip()


async def ask_async(question: str, approve=cli_approve) -> dict:
    started = time.time()
    params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT))
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            trace: list[dict] = []
            tools = make_tools(session, (await session.list_tools()).tools, approve, trace)
            model = ChatGoogleGenerativeAI(model=MODEL, google_api_key=load_api_key(), temperature=0,
                                           reasoning_effort=os.environ.get("GEMINI_EFFORT", "low"))
            agent = create_agent(
                model, tools, system_prompt=load_system_prompt(),
                middleware=[ToolCallLimitMiddleware(run_limit=MAX_TOOL_CALLS, exit_behavior="end")])

            messages = [HumanMessage(question)]
            result = await agent.ainvoke({"messages": messages})
            answer = text_of(result["messages"][-1])
            tokens = usage(result["messages"])
            check = check_citations(answer, trace)
            guardrail = None

            if not check["ok"]:   # guardrail 3: one retry, then a refusal
                guardrail = "retried"
                feedback = ("Your answer cited " + (", ".join(f"[{s}, {l}]" for s, l in check["invalid"])
                            or "nothing") + ", which the search results did not contain. Cite only passages "
                            "returned by the search tool, in the form [SOURCE, location], or say the "
                            "documents do not cover the question.")
                result = await agent.ainvoke({"messages": result["messages"] + [HumanMessage(feedback)]})
                answer = text_of(result["messages"][-1])
                again = usage(result["messages"])
                tokens = {k: tokens[k] + again[k] for k in tokens}
                check = check_citations(answer, trace)
                if not check["ok"]:
                    guardrail = "replaced_by_refusal"
                    answer = REFUSAL_TEXT

    return {"question": question, "answer": answer, "trace": trace, "citations": check,
            "guardrail": guardrail, "tokens": tokens, "seconds": round(time.time() - started, 1),
            "tool_calls": len(trace)}


def ask(question: str, approve=cli_approve) -> dict:
    return asyncio.run(ask_async(question, approve))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit('usage: python agent.py "your question"')
    out = ask(" ".join(sys.argv[1:]))
    print(out["answer"])
    cites = sorted({f"[{s}, {l}]" for s, l in out["citations"]["cited"]})
    if cites:
        print("\nSources: " + "; ".join(cites))
    print(f"\n({out['tool_calls']} tool calls, {out['tokens']['input_tokens']} in / "
          f"{out['tokens']['output_tokens']} out tokens, {out['seconds']}s"
          + (f", guardrail: {out['guardrail']}" if out["guardrail"] else "") + ")", file=sys.stderr)
