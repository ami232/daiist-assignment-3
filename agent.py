"""
Assignment 3: the Deal Desk agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the tools of server.py over MCP and AGENTS.md as the
system prompt, built from session 10's 07-own-harness/harness.py. Guardrails, all run by the
harness so the model cannot skip them:
    1. approval: add_document only runs after a person types "y" (refused when nobody can answer)
    2. a call limit: at most 8 model calls per question (ModelCallLimitMiddleware)
    3. a citation check on the output: every [SOURCE location] in the answer must match a passage the
       search tool actually returned, and an answer with facts but no citation is withheld
"""

import asyncio
import os
import re
import sys
import time
from contextlib import AsyncExitStack
from pathlib import Path

from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware, wrap_tool_call
from langchain_core.messages import AIMessage, ToolMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from api_key import load_api_key
from langchain.mcp import MCPAdapter  # langchain.mcp is in beta and warns on import

ROOT = Path(__file__).resolve().parent
MODEL = "gemini-3.5-flash-lite"   # fast, cheap, generous free-tier quota (as in session 10)
SERVER = ROOT / "server.py"
NEEDS_APPROVAL = {"add_document"}  # changes what every later answer is based on
MAX_MODEL_CALLS = 8
REFUSAL = "The Deal Desk documents do not cover this."
CITATION = re.compile(r"\[([A-Z][A-Z0-9_-]{1,15}) ((?:Art\.|para\.|Recital|Annex|p\.)[^\]]*)\]")
REFUSED = re.compile(r"documents do not cover", re.I)
LOC_KIND = re.compile(r"^(Art\.|para\.|Recital|Annex|p\.)\s*")


def parse_citations(answer: str) -> list[str]:
    """Every cited unit as "SOURCE location". One bracket can hold several, as in
    [CJN para. 155, 156] or [FDI Art. 2(2), Art. 2(7)] or [CJN para. 135, CJN para. 177]."""
    out = []
    for source, rest in CITATION.findall(answer):
        kind = ""
        for part in re.split(r"[,;]| and ", rest):
            part = part.strip()
            if not part:
                continue
            first = part.split(" ")[0]
            if re.fullmatch(r"[A-Z][A-Z0-9_-]{1,15}", first) and " " in part:
                source, part = first, part.split(" ", 1)[1]  # another document named inside the bracket
            m = LOC_KIND.match(part)
            if m:
                kind = m.group(1)
            elif part.startswith("(") and out:
                # "(8)" after "Art. 7" means "Art. 7(8)"; "(e)" after "Art. 4(2)(c)" means "Art. 4(2)(e)"
                previous = out[-1].split(" ", 1)[1]
                if re.fullmatch(r"\(\d+\)", part):
                    base = re.match(r"(Art\. \d+[a-z]?|para\. \d+)", previous)
                    base = base.group(1) if base else previous
                else:
                    base = re.sub(r"\([a-z]+\)$", "", previous)
                part = base + part
            elif kind:
                part = f"{kind} {part}"  # "156" after "para. 155" means "para. 156"
            out.append(f"{source} {part}")
    return out


async def load_mcp_tools(stack):
    # the server gets this process's environment (API key, proxy and certificate settings),
    # because by default an MCP stdio server starts with an almost empty one
    from fastmcp import Client
    from fastmcp.client.transports import PythonStdioTransport
    client = Client(PythonStdioTransport(str(SERVER), env=dict(os.environ), cwd=str(ROOT)))
    adapter = await stack.enter_async_context(MCPAdapter(client))
    return await adapter.list_tools()


def approval_guardrail(auto_approve: bool | None):
    """Guardrail 1. auto_approve=None asks at the keyboard; True/False decide without asking."""
    @wrap_tool_call
    async def ask_before_adding(request, handler):
        call = request.tool_call
        if call["name"] in NEEDS_APPROVAL:
            if auto_approve is None:
                try:
                    answer = input(f"  Allow {call['name']}({call['args']})? [y/N] ")
                except EOFError:  # no person at the keyboard: refuse
                    answer = "n"
                allowed = answer.strip().lower() == "y"
            else:
                allowed = auto_approve
            if not allowed:
                return ToolMessage(
                    content="The user refused to add this document. Answer with the current library only.",
                    tool_call_id=call["id"], status="error")
        return await handler(request)

    return ask_before_adding


def build_agent(tools, auto_approve: bool | None = None):
    load_api_key()
    return create_agent(
        model=ChatGoogleGenerativeAI(model=MODEL, temperature=0),
        tools=tools,
        system_prompt=(ROOT / "AGENTS.md").read_text(encoding="utf-8"),
        middleware=[
            approval_guardrail(auto_approve),
            ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS, exit_behavior="end"),  # guardrail 2
        ],
    )


def tool_trace(messages):
    """Every tool call and its result, in order: what the harness saw happen."""
    lines = []
    for message in messages:
        if isinstance(message, AIMessage):
            lines += [f"call {c['name']}({c['args']})" for c in message.tool_calls]
        elif isinstance(message, ToolMessage):
            lines.append(f"result {message.text}")
    return lines


def retrieved_citations(trace: list[str]) -> set[str]:
    """All citations the search tool returned: each passage's label and every unit it covers."""
    found = set()
    for line in trace:
        if not line.startswith("result "):
            continue
        for block in line.split("\n---\n"):
            head = re.match(r"\s*(?:result )?\[([A-Z][A-Z0-9_-]{1,15}) ([^\]]+)\]", block)
            if not head:
                continue
            source = head.group(1)
            found.add(f"{source} {head.group(2)}")
            covers = re.search(r"Covers: (.*)", block)
            if covers:
                found |= {f"{source} {loc.strip()}" for loc in covers.group(1).split(",")}
    return found


def _normalise(citation: str) -> list[str]:
    """[EUMR Art. 1(2)(a)] is supported by a passage covering Art. 1(2); ranges count by their start."""
    source, loc = citation.split(" ", 1)
    loc = loc.split("–")[0].split(" - ")[0].strip()
    out = [f"{source} {loc}"]
    m = re.match(r"(Art\. \d+[a-z]?)(\(\d+[a-z]?\))?", loc)
    if m:
        out.append(f"{source} {m.group(1)}{m.group(2) or ''}")
        out.append(f"{source} {m.group(1)}")
    m = re.match(r"(para\. \d+|Recital \d+)", loc)
    if m:  # "para. 5(a)" is supported by a passage covering para. 5
        out.append(f"{source} {m.group(1)}")
        out.append(f"{source} {m.group(1)}")
    return out


def check_citations(answer: str, trace: list[str]) -> tuple[bool, str]:
    """Guardrail 3 (output). Returns (ok, reason)."""
    cited = parse_citations(answer)
    if REFUSED.search(answer) and not cited:
        return True, "refusal"
    if not cited:
        return False, "the answer states facts without any citation"
    allowed = retrieved_citations(trace)
    allowed_articles = {a.split("(")[0] for a in allowed}

    def supported(citation: str) -> bool:
        forms = _normalise(citation)
        if any(f in allowed for f in forms):
            return True  # the exact unit, or the unit that contains the cited paragraph or point
        # a bare "Art. 7" is fine if some paragraph of Article 7 was retrieved; "Art. 7(3)" is not
        return "(" not in forms[0].split(" ", 1)[1] and forms[0] in allowed_articles

    bad = [c for c in cited if not supported(c)]
    if bad:
        return False, f"citations not found in the search results: {', '.join(sorted(set(bad)))}"
    return True, "all citations match retrieved passages"


def usage(messages) -> dict:
    tokens = {"input": 0, "output": 0}
    for m in messages:
        meta = getattr(m, "usage_metadata", None) or {}
        tokens["input"] += meta.get("input_tokens", 0)
        tokens["output"] += meta.get("output_tokens", 0)
    return tokens


async def ask(agent, question: str) -> dict:
    """Run one question. Returns the shown answer, the model's raw answer, the tool trace,
    the guardrail verdict, token usage and seconds, for evaluate.py."""
    started = time.time()
    result = await agent.ainvoke({"messages": [{"role": "user", "content": question}]})
    messages = result["messages"]
    raw = messages[-1].text if messages and isinstance(messages[-1], AIMessage) else ""
    trace = tool_trace(messages)
    ok, reason = check_citations(raw, trace)
    shown = raw if ok else (f"Answer withheld by the citation guardrail ({reason}). "
                            f"{REFUSAL} Please check with counsel or rephrase the question.")
    return {"answer": shown, "raw_answer": raw, "trace": trace, "guardrail_ok": ok,
            "guardrail_reason": reason, "tokens": usage(messages), "seconds": round(time.time() - started, 1)}


async def main(question: str):
    async with AsyncExitStack() as stack:
        agent = build_agent(await load_mcp_tools(stack))
        out = await ask(agent, question)
    for line in out["trace"]:
        print("  " + line.replace("\n", "\n    ")[:600])
    print()
    print(out["answer"])
    if not out["guardrail_ok"]:
        print(f"\n[guardrail fired: {out['guardrail_reason']}]")


if __name__ == "__main__":
    asyncio.run(main(" ".join(sys.argv[1:]) or "Can the parties close the deal before the Commission clears it?"))
