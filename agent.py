"""
Assignment 3: the agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the tools of server.py reached over MCP (stdio) and
AGENTS.md as the system prompt.
  - Approval: add_document only runs after a human types "y" (denied when nobody can answer,
    e.g. during evaluation or check.py).
  - Call limit: at most MAX_TOOL_CALLS tool calls per question, plus a graph recursion limit.
  - Guardrail (our choice): citation check. Every citation in the answer must match a passage
    that search actually returned in this run; an answer with an invalid citation, or with no
    citation at all, is replaced by "I don't know". For a compliance analyst an unsupported
    answer is worse than no answer.

ask(question) and ask_many(questions) return the answer, the tool trace, token use and time,
for evaluate.py.
"""
from __future__ import annotations

import asyncio
import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
AGENTS_MD = ROOT / "AGENTS.md"
MAX_TOOL_CALLS = 6
RECURSION_LIMIT = 2 * MAX_TOOL_CALLS + 4
REFUSAL = ("I don't know. The indexed UCITS documents do not answer this question; "
           "please check with the legal or compliance team.")

CITATION_RE = re.compile(r"\[([a-z0-9_]+),\s*([^\]]+)\]")
LOCATION_RE = re.compile(r"Article \d+[a-z]?|Annex [IVXLC]+|Recitals")
REFUSAL_RE = re.compile(r"\b(i don'?t know|i do not know|not (covered|addressed|answered) (by|in)|"
                        r"(do|does) not (contain|cover|answer|address))\b", re.I)


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


# --------------------------------------------------------------------------- model
def candidate_models() -> list[str]:
    """Models to try, in order. GEMINI_MODEL (comma-separated) first; then the stable
    gemini-X-flash models, newest first; then the flash-lite ones. If one is overloaded
    (503) or out of free quota (429), the agent moves on to the next."""
    from google import genai
    from api_key import load_api_key

    chosen = [m.strip() for m in os.environ.get("GEMINI_MODEL", "").split(",") if m.strip()]
    client = genai.Client(api_key=load_api_key())   # keep a reference so it stays open
    names = [m.name.split("/")[-1] for m in client.models.list()
             if "generateContent" in (getattr(m, "supported_actions", None) or [])]

    def version(name: str) -> float:
        return float(re.match(r"gemini-(\d+(?:\.\d+)?)", name).group(1))

    for pattern in (r"gemini-\d+(\.\d+)?-flash", r"gemini-\d+(\.\d+)?-flash-lite"):
        chosen += sorted((n for n in names if re.fullmatch(pattern, n) and n not in chosen),
                         key=version, reverse=True)
    if not chosen:
        raise RuntimeError("No Gemini flash model found; set the GEMINI_MODEL environment variable")
    return chosen


def make_model(name: str):
    from langchain_google_genai import ChatGoogleGenerativeAI
    from api_key import load_api_key

    return ChatGoogleGenerativeAI(model=name, google_api_key=load_api_key(),
                                  temperature=0, max_retries=2)


def is_overloaded(exc: Exception) -> bool:
    """Errors where another model may still work: overloaded (503), out of free quota (429),
    or retired for new users (404)."""
    text = str(exc)
    return any(s in text for s in ("503", "UNAVAILABLE", "high demand", "429", "RESOURCE_EXHAUSTED",
                                   "404", "NOT_FOUND", "no longer available"))


# --------------------------------------------------------------------------- approval
def approve_add_document(path: str) -> bool:
    """Human approval before add_document runs. Without a person at the keyboard: deny."""
    if os.environ.get("AUTO_APPROVE_ADD_DOCUMENT") == "1":
        return True
    if not sys.stdin.isatty():
        log(f"[approval] add_document({path!r}) denied: no one to approve it.")
        return False
    reply = input(f"\nThe agent wants to add '{path}' to the index (uses embeddings). Approve? [y/N] ")
    return reply.strip().lower() in ("y", "yes")


# --------------------------------------------------------------------------- guardrail
def cited_locations(text: str) -> set[tuple[str, str]]:
    """{(doc_id, 'Article N')} for every citation like [doc_id, Article 52(1)] in text.
    A passage citation [doc, Article 52 to Article 53] yields both articles."""
    found = set()
    for doc_id, inside in CITATION_RE.findall(text):
        for loc in LOCATION_RE.findall(inside):
            found.add((doc_id, loc))
    return found


def is_refusal(answer: str) -> bool:
    return bool(REFUSAL_RE.search(answer))


def check_citations(answer: str, retrieved: set) -> dict:
    cited = cited_locations(answer)
    invalid = sorted(c for c in cited if c not in retrieved)
    refusal = is_refusal(answer) and not cited
    ok = refusal or (bool(cited) and not invalid)
    return {"cited": sorted(cited), "invalid": invalid, "refusal": refusal, "ok": ok}


# --------------------------------------------------------------------------- agent run
def _text(message) -> str:
    content = getattr(message, "content", "")
    if isinstance(content, str):
        return content
    return "".join(p.get("text", "") if isinstance(p, dict) else str(p) for p in content)


async def _ask_many(questions: list[str], approve=approve_add_document) -> list[dict]:
    from langchain.agents import create_agent
    from langchain_core.tools import StructuredTool
    from langgraph.errors import GraphRecursionError
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    models = candidate_models()
    current = {"i": 0}
    system_prompt = AGENTS_MD.read_text(encoding="utf-8")
    params = StdioServerParameters(command=sys.executable, args=[str(ROOT / "server.py")], cwd=str(ROOT))
    results = []

    async with stdio_client(params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()
        descriptions = {t.name: t.description for t in (await session.list_tools()).tools}

        for question in questions:
            trace: list[dict] = []
            calls = {"n": 0}

            async def call(name: str, args: dict) -> str:
                calls["n"] += 1
                if calls["n"] > MAX_TOOL_CALLS:
                    out = "Tool call limit reached. Answer from the passages you have, or say you don't know."
                else:
                    res = await session.call_tool(name, args)
                    out = "\n".join(c.text for c in res.content if getattr(c, "text", None)) or "(empty)"
                trace.append({"tool": name, "args": args, "output": out})
                return out

            async def search(query: str) -> str:
                return await call("search", {"query": query})

            async def add_document(path: str) -> str:
                if not approve(path):
                    trace.append({"tool": "add_document", "args": {"path": path}, "output": "DENIED by user"})
                    return "The user did not approve adding this document. Do not retry."
                return await call("add_document", {"path": path})

            tools = [
                StructuredTool.from_function(coroutine=search, name="search",
                                             description=descriptions["search"]),
                StructuredTool.from_function(coroutine=add_document, name="add_document",
                                             description=descriptions["add_document"]),
            ]
            start, messages = time.time(), []
            while True:
                model_name = models[current["i"]]
                agent = create_agent(make_model(model_name), tools=tools, system_prompt=system_prompt)
                trace.clear()
                calls["n"] = 0
                try:
                    out = await agent.ainvoke({"messages": [{"role": "user", "content": question}]},
                                              config={"recursion_limit": RECURSION_LIMIT})
                    messages = out["messages"]
                    raw_answer = _text(messages[-1]).strip()
                    break
                except GraphRecursionError:
                    raw_answer = REFUSAL
                    break
                except Exception as exc:  # overloaded or out of quota: try the next model
                    if is_overloaded(exc) and current["i"] + 1 < len(models):
                        current["i"] += 1
                        log(f"[model] {model_name} unavailable ({str(exc)[:60]}...); "
                            f"switching to {models[current['i']]}")
                        continue
                    raise
            seconds = round(time.time() - start, 2)

            retrieved = set()
            for step in trace:
                if step["tool"] == "search":
                    retrieved |= cited_locations(step["output"])
            check = check_citations(raw_answer, retrieved)
            answer = raw_answer if check["ok"] else REFUSAL

            usage = [getattr(m, "usage_metadata", None) or {} for m in messages]
            results.append({
                "question": question,
                "answer": answer,
                "raw_answer": raw_answer,
                "guardrail_triggered": not check["ok"],
                "citations": check["cited"],
                "invalid_citations": check["invalid"],
                "refusal": is_refusal(answer),
                "tool_calls": len(trace),
                "trace": trace,
                "input_tokens": sum(u.get("input_tokens", 0) for u in usage),
                "output_tokens": sum(u.get("output_tokens", 0) for u in usage),
                "seconds": seconds,
                "model": model_name,
            })
    return results


def ask_many(questions: list[str], approve=approve_add_document) -> list[dict]:
    """Answer several questions with one MCP server session (used by evaluate.py)."""
    return asyncio.run(_ask_many(questions, approve))


def ask(question: str, approve=approve_add_document) -> dict:
    return ask_many([question], approve)[0]


def main() -> int:
    question = " ".join(sys.argv[1:]).strip()
    if not question:
        print('Usage: python agent.py "your question"')
        return 2
    r = ask(question)
    print(r["answer"])
    if r["citations"] and not r["guardrail_triggered"]:
        print("\nSources: " + "; ".join(f"[{d}, {loc}]" for d, loc in r["citations"]))
    if r["guardrail_triggered"]:
        print(f"\n(guardrail: the draft answer had invalid or missing citations {r['invalid_citations']})")
    print(f"\n({r['model']}, {r['tool_calls']} tool call(s), "
          f"{r['input_tokens'] + r['output_tokens']} tokens, {r['seconds']} s)")
    return 0


if __name__ == "__main__":
    sys.exit(main())