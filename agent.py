"""
Assignment 3: my agent. `uv run python main.py ask "question"` runs `python agent.py "question"`.

- LangChain create_agent on Gemini, with AGENTS.md as the system prompt.
- Tools come from server.py over MCP (stdio): search and add_document.
- Guardrails:
    1. approval: add_document only runs if a human types "y" (no terminal -> denied);
    2. call limits: at most 4 searches and 8 model calls per question;
    3. citation check (my extra guardrail): every [source, location] in the answer
       must be one of the passages the search tool actually returned. An answer
       with no citations or with an invented one is blocked and replaced by a refusal.

evaluate.py imports ask(), which returns the answer plus the tool trace, tokens and seconds.
"""

import asyncio
import os
import re
import sys
import time
from pathlib import Path

from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware, ToolCallLimitMiddleware
from langchain_core.tools import StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
MODEL = "gemini-3.5-flash-lite"
SYSTEM_PROMPT = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
REFUSAL = "The corpus does not cover this."


# ---------------------------------------------------------------- citations

def parse_citations(text: str) -> set[tuple[str, str]]:
    """Find every citation in a text.

    [air-261-2004, Article 7(1)]                    -> (air-261-2004, Article 7)
    [air-261-2004, Article 4, Article 7]            -> (air-261-2004, Article 4), (air-261-2004, Article 7)
    [rail-2021-782, Annex I, Article 33, Article 34] -> both articles inside Annex I
    [bus-181-2011, Article 21; sea-1177-2010, Article 17] -> one per source
    """
    found = set()
    for inside in re.findall(r"\[([^\[\]]+)\]", text):
        source, annex = None, None
        for part in re.split(r"[;,]", inside):
            part = re.sub(r"\s*\(.*?\)", "", part).strip()   # "Article 7(1)(a)" -> "Article 7"
            if re.fullmatch(r"(?=[a-z0-9-]*[a-z])[a-z0-9]+(?:-[a-z0-9]+)*", part):   # a source name
                source, annex = part, None
            elif source and part.startswith("Annex"):
                annex = part
                found.add((source, annex))
            elif source and part.startswith("Article"):
                found.add((source, f"{annex}, {part}" if annex else part))
                found.discard((source, annex))           # "Annex I, Article 33" is one location, not two
            elif source and part:                          # e.g. "Recitals"
                annex = None
                found.add((source, part))
    return found


AMOUNT_RE = re.compile(r"\d\s*%|\bEUR\b|€|\bSDRs?\b|\bunits of account\b", re.IGNORECASE)


def is_refusal(answer: str) -> bool:
    """A real refusal starts with the refusal sentence and gives no amount afterwards.
    "The corpus does not cover this. However, you get EUR 600." is an answer, not a refusal,
    so it still needs valid citations."""
    text = answer.strip()
    if not text.lower().startswith(REFUSAL.lower()):
        return False
    return not AMOUNT_RE.search(text[len(REFUSAL):])


def check_citations(answer: str, search_outputs: list[str]) -> dict:
    """Compare the citations in the answer with the passages that were retrieved."""
    cited = parse_citations(answer)
    retrieved = parse_citations("\n".join(search_outputs))
    return {
        "refused": is_refusal(answer),
        "cited": sorted(cited),
        "invalid": sorted(cited - retrieved),
    }


def apply_citation_guardrail(draft: str, search_outputs: list[str]) -> tuple[str, bool, dict]:
    """Return (final answer, blocked?, citation check). A non-refusal with no citation,
    or with a citation that was not retrieved, is replaced by a refusal.
    A refusal followed by an amount counts as a non-refusal (see is_refusal)."""
    check = check_citations(draft, search_outputs)
    blocked = not check["refused"] and (not check["cited"] or bool(check["invalid"]))
    if blocked:
        return (f"{REFUSAL} (A draft answer was blocked because its citations could not be "
                f"verified against the retrieved passages.)"), True, check
    return draft, False, check


# ---------------------------------------------------------------- approval

def ask_human_approval(path: str) -> bool:
    """Approval step before add_document. Without a terminal (e.g. check.py, evaluation) the answer is no."""
    if not sys.stdin.isatty():
        print(f"[approval] add_document({path!r}) denied: no one at the terminal to approve it.", file=sys.stderr)
        return False
    try:
        reply = input(f"\nThe agent wants to add the document {path!r} to the index. Allow? [y/N] ")
    except EOFError:
        return False
    return reply.strip().lower() in ("y", "yes")


# ---------------------------------------------------------------- the agent

async def ask_async(question: str, approve=ask_human_approval) -> dict:
    load_api_key()
    started = time.time()
    trace, search_outputs = [], []

    server = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT),
                                   env=dict(os.environ))
    async with stdio_client(server) as (read, write), ClientSession(read, write) as session:
        await session.initialize()
        descriptions = {t.name: t.description for t in (await session.list_tools()).tools}

        async def call(name: str, arguments: dict) -> str:
            result = await session.call_tool(name, arguments)
            return "\n".join(getattr(c, "text", "") for c in result.content)

        async def search(query: str) -> str:
            text = await call("search", {"query": query})
            trace.append({"tool": "search", "query": query})
            search_outputs.append(text)
            return text

        async def add_document(path: str) -> str:
            if not approve(path):
                trace.append({"tool": "add_document", "path": path, "approved": False})
                return "The user did not approve adding this document. Nothing was added."
            trace.append({"tool": "add_document", "path": path, "approved": True})
            return await call("add_document", {"path": path})

        tools = [
            StructuredTool.from_function(coroutine=search, name="search", description=descriptions["search"]),
            StructuredTool.from_function(coroutine=add_document, name="add_document",
                                         description=descriptions["add_document"]),
        ]
        agent = create_agent(
            model=ChatGoogleGenerativeAI(model=MODEL, temperature=0, max_retries=6),
            tools=tools,
            system_prompt=SYSTEM_PROMPT,
            middleware=[
                ToolCallLimitMiddleware(tool_name="search", run_limit=4),
                ModelCallLimitMiddleware(run_limit=8, exit_behavior="end"),
            ],
        )
        result = await agent.ainvoke({"messages": [{"role": "user", "content": question}]})

    messages = result["messages"]
    draft = messages[-1].text.strip()
    tokens = sum((getattr(m, "usage_metadata", None) or {}).get("total_tokens", 0) for m in messages)

    # Guardrail 3: block answers whose citations cannot be traced to a retrieved passage.
    # Not for add_document turns: "the document was added" is not a claim about the law.
    if any(t["tool"] == "add_document" for t in trace):
        answer, blocked, check = draft, False, check_citations(draft, search_outputs)
    else:
        answer, blocked, check = apply_citation_guardrail(draft, search_outputs)

    return {
        "question": question,
        "answer": answer,
        "draft": draft,
        "guardrail_fired": blocked,
        "citations": check["cited"],
        "invalid_citations": check["invalid"],
        "trace": trace,
        "retrieved": "\n\n".join(search_outputs),
        "tokens": tokens,
        "seconds": round(time.time() - started, 1),
    }


def ask(question: str, approve=ask_human_approval) -> dict:
    return asyncio.run(ask_async(question, approve))


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    if len(sys.argv) < 2:
        raise SystemExit('Usage: python agent.py "your question"')
    out = ask(" ".join(sys.argv[1:]))
    print(out["answer"])
    if out["citations"] and not out["guardrail_fired"]:
        print("\nSources:")
        for source, location in out["citations"]:
            print(f"  - {source}, {location}")
    if out["guardrail_fired"]:
        print(f"\n[guardrail] blocked draft: {out['draft'][:300]}")
    print(f"\n({len(out['trace'])} tool calls, {out['tokens']} tokens, {out['seconds']} s)")
