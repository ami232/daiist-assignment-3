"""
Assignment 3: the agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the two tools of server.py over MCP and
AGENTS.md as system prompt. Safeguards:

- Approval: add_document only runs after the user types "yes" (in a
  non-interactive run it is refused).
- Call limits: at most 4 searches and 8 model calls per question.
- Model fallback: if the main Gemini model is overloaded, a second one answers.
- Extra guardrail, citation check: every answer that isn't a refusal must cite at
  least one passage, and every citation must point to a passage that the search
  actually returned. Otherwise the answer is replaced by a refusal.

ask(question) returns the answer, the tool trace, tokens and seconds, for evaluate.py.
"""

import asyncio
import re
import sys
import time
import unicodedata
from pathlib import Path

from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware, ModelFallbackMiddleware, ToolCallLimitMiddleware
from langchain_core.tools import StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
MODEL, FALLBACK = "gemini-3.5-flash-lite", "gemini-flash-lite-latest"  # free tier: the "flash" models allow only 20 requests a day
MAX_SEARCHES, MAX_MODEL_CALLS = 4, 8
REFUSAL = "Las leyes consultadas no cubren esta pregunta."


# ---------------------------------------------------------------------------
# Citation guardrail
# ---------------------------------------------------------------------------
def _norm(text: str) -> str:
    text = unicodedata.normalize("NFKD", text.lower())
    return re.sub(r"\s+", " ", "".join(c for c in text if not unicodedata.combining(c))).strip()


def _law_key(source: str) -> str:
    """'Ley 19/2007 contra la violencia…' -> 'ley 19/2007'; other documents keep their full name."""
    m = re.match(r"((?:ley organica|ley|lo|real decreto|rd) \d+/\d{4})", _norm(source))
    return m.group(1).replace("ley organica", "lo") if m else _norm(source)


def _place_key(location: str) -> str:
    """'Artículo 24 (parte 2/3)' / 'Artículo 24.5' / 'art. 24' -> 'articulo 24'."""
    loc = re.sub(r"\(parte \d+/\d+\)", "", _norm(location))
    m = re.match(r"(?:articulo|art\.?) ?(\d+(?: ?(?:bis|ter|quater))?)", loc)
    return f"articulo {m.group(1)}" if m else loc.strip(" .")


def retrieved_passages(trace: list[dict]) -> set[tuple[str, str]]:
    found = set()
    for step in trace:
        if step["tool"] == "search":
            for source, location in re.findall(r"^\[\d+\] (.+?) — (.+)$", step["result"], re.M):
                found.add((_law_key(source), _place_key(location)))
    return found


def citations(answer: str) -> list[tuple[str, str]]:
    """'(Ley 19/2007, Artículo 4)' -> [('ley 19/2007', 'articulo 4')]."""
    out = []
    for law, place in re.findall(r"\(([^(),]+?),\s*([^()]+?)\)", answer):
        if re.search(r"\d+/\d{4}|real decreto|reglamento", law, re.I):
            # "Artículos 6 y 7" / "Artículos 21 y 24.5" cite several articles at once
            many = re.match(r"art[íi]culos\s+(.+)", place.strip(), re.I)
            if many:
                for number in re.findall(r"\d+", re.sub(r"\.\d+", "", many.group(1))):
                    out.append((_law_key(law), f"articulo {number}"))
            else:
                out.append((_law_key(law), _place_key(place)))
    return out


def check_citations(answer: str, trace: list[dict]) -> str | None:
    """None if the answer passes, otherwise the reason it was blocked."""
    if answer.strip().startswith(REFUSAL):
        return None
    tools_used = {step["tool"] for step in trace}
    if tools_used == {"add_document"}:
        return None  # a reply about adding a file is not a legal answer, so it needs no citation
    cited = citations(answer)
    if not cited:
        return "answer without any citation"
    retrieved = retrieved_passages(trace)
    bad = [c for c in cited if c not in retrieved]
    if bad:
        return "cites passages that the search did not return: " + ", ".join(f"{l}, {p}" for l, p in bad)
    return None


# ---------------------------------------------------------------------------
# Agent
# ---------------------------------------------------------------------------
def _text(message) -> str:
    content = message.content
    if isinstance(content, list):
        content = "".join(p.get("text", "") if isinstance(p, dict) else str(p) for p in content)
    return content or ""


def _approve_interactively(path: str) -> bool:
    if not sys.stdin.isatty():
        return False  # nobody to ask: never add documents unattended
    print(f"\nThe assistant wants to add this document to the index:\n  {path}", file=sys.stderr)
    return input("Approve? Type 'yes' to add it: ").strip().lower() in ("yes", "y", "si", "sí")


async def ask_async(question: str, approve=None) -> dict:
    load_api_key()
    approve = approve or _approve_interactively
    trace, started = [], time.time()
    params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT))
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            described = {t.name: t.description for t in (await session.list_tools()).tools}

            async def call(name: str, args: dict) -> str:
                result = await session.call_tool(name, args)
                text = "\n".join(getattr(c, "text", "") for c in result.content)
                trace.append({"tool": name, "args": args, "result": text})
                return text

            async def search(query: str) -> str:
                return await call("search", {"query": query})

            async def add_document(path: str) -> str:
                if not approve(path):  # approval happens BEFORE the tool runs
                    trace.append({"tool": "add_document", "args": {"path": path}, "result": "rejected by the user"})
                    return "The user did not approve adding this document. Nothing was added."
                return await call("add_document", {"path": path})

            tools = [StructuredTool.from_function(coroutine=search, name="search", description=described["search"]),
                     StructuredTool.from_function(coroutine=add_document, name="add_document",
                                                  description=described["add_document"])]
            agent = create_agent(
                ChatGoogleGenerativeAI(model=MODEL, temperature=0),
                tools,
                system_prompt=(ROOT / "AGENTS.md").read_text(encoding="utf-8"),
                middleware=[
                    ToolCallLimitMiddleware(tool_name="search", run_limit=MAX_SEARCHES),
                    ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS, exit_behavior="end"),
                    ModelFallbackMiddleware(ChatGoogleGenerativeAI(model=FALLBACK, temperature=0)),
                ],
            )
            result = await agent.ainvoke({"messages": [("user", question)]})

    messages = result["messages"]
    answer = next((_text(m) for m in reversed(messages) if m.type == "ai" and _text(m).strip()), "")
    blocked = check_citations(answer, trace)
    final = answer if blocked is None else (
        f"{REFUSAL} No he podido dar una respuesta verificable con citas a los artículos encontrados; "
        f"consulte a un abogado o a la federación.")
    tokens = {"input": 0, "output": 0}
    for m in messages:
        usage = getattr(m, "usage_metadata", None) or {}
        tokens["input"] += usage.get("input_tokens", 0)
        tokens["output"] += usage.get("output_tokens", 0)
    return {"question": question, "answer": final, "raw_answer": answer, "guardrail": blocked,
            "trace": trace, "tokens": tokens, "seconds": round(time.time() - started, 1)}


def ask(question: str, approve=None) -> dict:
    return asyncio.run(ask_async(question, approve))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit('Usage: python agent.py "your question"')
    out = ask(" ".join(sys.argv[1:]))
    print(out["answer"])
    sources = sorted({f"{s.split(' — ')[0]} — {s.split(' — ')[1]}" for step in out["trace"] if step["tool"] == "search"
                      for s in re.findall(r"^\[\d+\] (.+? — .+)$", step["result"], re.M)})
    print("\nPasajes consultados:")
    for s in sources:
        print(f"  - {s}")
    if out["guardrail"]:
        print(f"\n[guardrail] Respuesta original bloqueada: {out['guardrail']}", file=sys.stderr)
    print(f"\n({len([t for t in out['trace'] if t['tool'] == 'search'])} búsquedas, "
          f"{sum(out['tokens'].values())} tokens, {out['seconds']} s)")
