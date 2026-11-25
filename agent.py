"""
Assignment 3: your agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, tools from server.py over MCP, AGENTS.md as
system prompt. Guardrails:
  1. approval: add_document only runs after the user types y (never in a
     non-interactive run such as the evaluation);
  2. call limit: at most MAX_TOOL_CALLS tool calls per question;
  3. citation guard (our extra one): an answer must cite passages that were
     actually retrieved in this run, or be an explicit refusal. Otherwise it is
     replaced by a refusal, because an unverifiable answer is worse than none.

`ask(question)` returns the answer plus the tool trace, for evaluate.py.
"""

import asyncio
import re
import sys
import time
from pathlib import Path

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
MODEL = "gemini-2.5-flash"
MAX_TOOL_CALLS = 6
REFUSAL = "The corpus does not cover this."
CITATION = re.compile(r"\[([a-z0-9_]+),\s*(regulation [0-9]+[A-Za-z]*)[^\]]*\]")
PASSAGE_HEAD = re.compile(r"^\[([a-z0-9_]+),\s*(regulation [0-9]+[A-Za-z]*)[^\]]*\]", re.MULTILINE)


def text_of(content) -> str:
    """Message content can be a string or a list of parts."""
    if isinstance(content, str):
        return content
    return "".join(p.get("text", "") if isinstance(p, dict) else str(p) for p in content)


def pick_models() -> list[str]:
    """Ask Google which chat models this key can use; return them best-first (we fall back if one is overloaded)."""
    from google import genai

    client = genai.Client(api_key=load_api_key())
    available = []
    for m in client.models.list():
        if "generateContent" in (getattr(m, "supported_actions", None) or []):
            available.append(m.name.replace("models/", ""))
    preferred = ["gemini-3-flash-preview", "gemini-flash-latest", "gemini-3-flash", "gemini-2.5-flash",
                 "gemini-2.0-flash", "gemini-flash-lite-latest", "gemini-2.5-flash-lite"]
    ordered = [p for p in preferred if p in available]
    others = sorted(n for n in available if "flash" in n and n not in ordered
                    and not any(x in n for x in ("image", "tts", "live", "audio", "thinking", "robotics", "computer")))
    ordered += others
    if not ordered:
        raise SystemExit(f"No usable Gemini chat model found for this key. Models seen: {sorted(available)[:10]}")
    return ordered


RETRIABLE = ("503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED", "404", "NOT_FOUND", "overloaded")


def approve(path: str) -> bool:
    """Ask the user. With no terminal attached (e.g. evaluation) the answer is no."""
    if not sys.stdin.isatty():
        return False
    return input(f"\nThe agent wants to add this file to the index: {path}\nApprove? [y/N] ").strip().lower() == "y"


def to_langchain_tool(session, mcp_tool):
    """Turn one MCP tool (from server.py) into a LangChain tool. add_document needs approval first."""
    from langchain_core.tools import StructuredTool

    name = mcp_tool.name
    schema = getattr(mcp_tool, "input_schema", None) or getattr(mcp_tool, "inputSchema", None)

    async def call(**kwargs) -> str:
        if name == "add_document" and not approve(kwargs.get("path", "")):
            return "Not approved by the user. The document was NOT added."
        result = await session.call_tool(name, kwargs)
        return "\n".join(getattr(c, "text", "") for c in result.content)

    return StructuredTool.from_function(coroutine=call, name=name, description=mcp_tool.description or "", args_schema=schema)


async def run_agent(question: str) -> dict:
    from langchain.agents import create_agent
    from langchain_google_genai import ChatGoogleGenerativeAI
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    load_api_key()
    started = time.time()
    params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT))
    out = {"question": question, "answer": "", "tool_calls": [], "retrieved": [], "guard": "", "input_tokens": 0, "output_tokens": 0}

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = [to_langchain_tool(session, t) for t in (await session.list_tools()).tools]
            messages, error = None, None
            for model_name in pick_models()[:4]:
                print(f"[model: {model_name}]", file=sys.stderr)
                agent = create_agent(ChatGoogleGenerativeAI(model=model_name, temperature=0, max_retries=1), tools,
                                     system_prompt=(ROOT / "AGENTS.md").read_text(encoding="utf-8"))
                try:
                    result = await agent.ainvoke({"messages": [("user", question)]},
                                                 config={"recursion_limit": 2 * MAX_TOOL_CALLS + 3})
                    messages = result["messages"]
                    out["model"] = model_name
                    break
                except Exception as e:  # noqa: BLE001 - overload, recursion limit, ...
                    error = e
                    print(f"[error] {type(e).__name__}: {str(e)[:300]}", file=sys.stderr)
                    if any(x in f"{type(e).__name__} {e}" for x in RETRIABLE):
                        print("[trying the next model]", file=sys.stderr)
                        continue
                    break
            if messages is None:
                out["guard"] = f"call limit or error: {type(error).__name__}"
                out["answer"] = f"{REFUSAL} (stopped: {out['guard']})"
                out["seconds"] = round(time.time() - started, 1)
                return out

    for m in messages:
        usage = getattr(m, "usage_metadata", None) or {}
        out["input_tokens"] += usage.get("input_tokens", 0)
        out["output_tokens"] += usage.get("output_tokens", 0)
        for call in getattr(m, "tool_calls", None) or []:
            out["tool_calls"].append({"name": call["name"], "args": call["args"]})
        if m.type == "tool":
            tool_text = text_of(m.content)
            out["retrieved"] += [f"{s}|{loc}" for s, loc in PASSAGE_HEAD.findall(tool_text)]
            out["evidence"] = out.get("evidence", "") + "\n" + tool_text
    answer = text_of(messages[-1].content).strip()

    # guardrail 2: call limit
    if len(out["tool_calls"]) > MAX_TOOL_CALLS:
        out["guard"] = "call limit"
        answer = f"{REFUSAL} (too many tool calls)"
    # guardrail 3: citation guard
    elif REFUSAL.lower() not in answer.lower():
        cited = CITATION.findall(answer)
        retrieved = set(out["retrieved"])
        bad = [c for c in cited if f"{c[0]}|{c[1]}" not in retrieved]
        if not cited or bad:
            out["guard"] = "citation guard: " + ("no citation" if not cited else f"not retrieved: {bad}")
            answer = f"{REFUSAL} I could not back an answer with a citation from the retrieved passages."
    out["answer"] = answer
    out["seconds"] = round(time.time() - started, 1)
    return out


def ask(question: str) -> dict:
    return asyncio.run(run_agent(question))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit('usage: python agent.py "your question"')
    result = ask(" ".join(sys.argv[1:]))
    print(result["answer"])
    cites = sorted(set(result["retrieved"]))
    if cites:
        print("\nRetrieved passages: " + "; ".join(c.replace("|", ", ") for c in cites))
    print(f"\n({len(result['tool_calls'])} tool calls, {result['input_tokens']}+{result['output_tokens']} tokens, "
          f"{result['seconds']}s)" + (f" [guard: {result['guard']}]" if result["guard"] else ""))
