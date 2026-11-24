"""
Assignment 3: the agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the tools of server.py over MCP and
AGENTS.md as system prompt.

Guardrails:
- approval: add_document runs only after a person types "y" (refused when
  nobody is at the keyboard, e.g. during evaluation);
- call limits: at most MAX_TOOL_CALLS tool calls and MAX_MODEL_CALLS model calls;
- figure check (our extra guardrail): every number in the answer must appear in
  the passages the agent retrieved, or follow from two of them by a sum,
  difference or ratio. If not, the agent is told which figures are unsupported
  and gets one retry; figures still unsupported are flagged under the answer.

`answer_question(question)` returns the answer and the tool trace, for evaluate.py.
"""

from __future__ import annotations

import asyncio
import itertools
import os
import re
import sys
import time
from pathlib import Path

os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")

from api_key import load_api_key  # noqa: E402

ROOT = Path(__file__).resolve().parent
# Free tier: the flash models allow 20 requests a day each and 3.8-flash returned 503 for
# hours, so every answer comes from 3.5-flash-lite (one model for all 32 questions).
MODEL = os.environ.get("AGENT_MODEL", "gemini-3.5-flash-lite")
MAX_TOOL_CALLS = 6
MAX_MODEL_CALLS = 10


def system_prompt() -> str:
    return (ROOT / "AGENTS.md").read_text(encoding="utf-8")


# --------------------------------------------------------------------------- approval


def ask_in_terminal(path: str) -> bool:
    """Ask the person at the keyboard; refuse if there is nobody to ask."""
    if not sys.stdin or not sys.stdin.isatty():
        return False
    reply = input(f"\nThe agent wants to add {path!r} to the index (this spends embedding quota). Approve? [y/N] ")
    return reply.strip().lower() in {"y", "yes", "s", "si", "sí"}


# --------------------------------------------------------------------------- figure check

UNITS = {"thousand": 1e3, "million": 1e6, "billion": 1e9, "trillion": 1e12}
NUMBER = re.compile(r"(?<![\w.])(\d{1,3}(?:,\d{3})+|\d+)(\.\d+)?\s*(%|percent|thousand|million|billion|trillion)?", re.I)


def figures(text: str) -> list[tuple[str, float, str]]:
    """Numbers in a text as (as written, value, unit), skipping years, citations and Item/page labels."""
    text = re.sub(r"\[[^\]]*\]", " ", text)  # citations
    text = re.sub(r"\b(Item|p\.|pages?|Note|Q[1-4])\s*\d+[A-C]?", " ", text, flags=re.I)
    found = []
    for match in NUMBER.finditer(text):
        whole, decimals, unit = match.group(1), match.group(2) or "", (match.group(3) or "").lower()
        value = float(whole.replace(",", "") + decimals)
        if not unit and not decimals and 1900 <= value <= 2100:
            continue  # a year
        if not unit and not decimals and value <= 10 and "," not in whole:
            continue  # small counts ("two segments", "3 passages") carry little risk
        found.append((match.group(0).strip(), value, "%" if unit in {"%", "percent"} else unit))
    return found


def scaled(value: float, unit: str) -> list[float]:
    """Absolute values a figure may stand for (tables are in millions without saying so)."""
    if unit == "%":
        return [value]
    if unit in UNITS:
        return [value * UNITS[unit]]
    return [value, value * 1e3, value * 1e6]


def close(a: float, b: float) -> bool:
    return a == b or (max(abs(a), abs(b)) > 0 and abs(a - b) / max(abs(a), abs(b)) <= 0.01)


def check_figures(answer: str, evidence: str) -> list[str]:
    """Figures in the answer that neither appear in the evidence nor follow from two evidence figures."""
    source = [(v, u) for _, v, u in figures(evidence)]
    percents = {v for v, u in source if u == "%"}
    amounts = {s for v, u in source if u != "%" for s in scaled(v, u)}
    amounts |= percents  # a percentage written without the sign
    derived: set[float] = set()
    pool = sorted(amounts)
    if len(pool) <= 400:
        for a, b in itertools.combinations(pool, 2):
            derived |= {a + b, abs(a - b)}
            if b:
                derived.add(100 * a / b)
            if a:
                derived.add(100 * b / a)
    unsupported = []
    for written, value, unit in figures(answer):
        candidates = [value] if unit == "%" else scaled(value, unit)
        if not any(close(c, s) for c in candidates for s in amounts | derived):
            unsupported.append(written)
    return unsupported


# --------------------------------------------------------------------------- MCP tools as LangChain tools


def mcp_tool(session, tool, trace: list[dict], approve):
    from langchain_core.tools import StructuredTool

    async def call(**arguments) -> str:
        if tool.name == "add_document" and not approve(arguments.get("path", "")):
            text = "Not added: the user did not approve adding this document."
            trace.append({"tool": tool.name, "args": arguments, "result": text, "approved": False})
            return text
        result = await session.call_tool(tool.name, arguments)
        text = "\n".join(getattr(c, "text", "") for c in result.content)
        trace.append({"tool": tool.name, "args": arguments, "result": text})
        return text

    return StructuredTool.from_function(
        coroutine=call, name=tool.name, description=tool.description or "", args_schema=tool.input_schema
    )


def message_text(message) -> str:
    content = message.content
    if isinstance(content, list):
        return "".join(part.get("text", "") if isinstance(part, dict) else str(part) for part in content)
    return content or ""


def usage(messages) -> dict:
    totals = {"input_tokens": 0, "output_tokens": 0}
    for m in messages:
        meta = getattr(m, "usage_metadata", None) or {}
        for key in totals:
            totals[key] += meta.get(key, 0) or 0
    return totals


async def run(question: str, approve=ask_in_terminal) -> dict:
    from langchain.agents import create_agent
    from langchain.agents.middleware import (
        ModelCallLimitMiddleware,
        ModelRetryMiddleware,
        ToolCallLimitMiddleware,
    )
    from langchain_google_genai import ChatGoogleGenerativeAI
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    load_api_key()
    started = time.time()
    trace: list[dict] = []
    params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT))
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = [mcp_tool(session, t, trace, approve) for t in (await session.list_tools()).tools]
            agent = create_agent(
                model=ChatGoogleGenerativeAI(model=MODEL, temperature=0, timeout=90, max_retries=1),
                tools=tools,
                system_prompt=system_prompt(),
                middleware=[
                    ToolCallLimitMiddleware(run_limit=MAX_TOOL_CALLS, exit_behavior="continue"),
                    ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS, exit_behavior="end"),
                    # free tier: 503 "high demand" and 429 rate limits are common and
                    # temporary. Wait patiently (up to ~15 min) rather than switch to a
                    # weaker model, so every answer comes from the same model.
                    ModelRetryMiddleware(
                        max_retries=8, initial_delay=10.0, max_delay=180.0, on_failure="error",
                        retry_on=lambda e: "PerDay" not in str(e),  # a spent daily quota will not come back in minutes
                    ),
                ],
            )
            state = await agent.ainvoke({"messages": [{"role": "user", "content": question}]})
            messages = state["messages"]
            answer = message_text(messages[-1])

            evidence = "\n".join(t["result"] for t in trace if t["tool"] == "search")
            unsupported = check_figures(answer, evidence)
            guardrail = {"first_unsupported": unsupported, "retried": False, "still_unsupported": []}
            if unsupported:
                guardrail["retried"] = True
                feedback = (
                    "Figure check failed. These figures are not in the passages you retrieved and do not "
                    f"follow from them: {', '.join(unsupported)}. Rewrite the answer using only figures "
                    "that appear in the search results (search again if you need to), with citations."
                )
                state = await agent.ainvoke({"messages": messages + [{"role": "user", "content": feedback}]})
                messages = state["messages"]
                answer = message_text(messages[-1])
                evidence = "\n".join(t["result"] for t in trace if t["tool"] == "search")
                guardrail["still_unsupported"] = check_figures(answer, evidence)
                if guardrail["still_unsupported"]:
                    answer += (
                        "\n\nWarning: these figures could not be verified against the retrieved passages: "
                        + ", ".join(guardrail["still_unsupported"])
                    )

    return {
        "question": question,
        "answer": answer,
        "trace": trace,
        "evidence": evidence,
        "guardrail": guardrail,
        "model_calls": sum(1 for m in messages if m.type == "ai"),
        "tool_calls": len(trace),
        "model": MODEL,
        "seconds": round(time.time() - started, 1),
        **usage(messages),
    }


def answer_question(question: str, approve=ask_in_terminal) -> dict:
    return asyncio.run(run(question, approve))


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit('Usage: python agent.py "your question"')
    result = answer_question(" ".join(sys.argv[1:]))
    print(result["answer"])
    sources = sorted(set(re.findall(r"\[([a-z]+_10k_fy\d{4}), ([^\]]+)\]", result["answer"])))
    if sources:
        print("\nSources:")
        for source, location in sources:
            print(f"  - {source}, {location}")
    g = result["guardrail"]
    if g["first_unsupported"]:
        print(f"\n[figure check fired: {', '.join(g['first_unsupported'])}; retried once]", file=sys.stderr)
    print(
        f"\n[{result['tool_calls']} tool calls, {result['model_calls']} model calls, "
        f"{result['input_tokens']}+{result['output_tokens']} tokens, {result['seconds']}s]",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
