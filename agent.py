"""
Assignment 3: your agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the tools of server.py over MCP and
AGENTS.md as the system prompt.

Guardrails:
  1. Approval: add_document does not run until `approve(path)` says yes. From the
     command line the person is asked; with no terminal the answer is no.
  2. Call limit: at most MAX_SEARCHES searches per question.
  3. Citation check (our own): every [source, Article N] in the answer must name a
     passage that a search really returned. If not, the model gets one chance to
     fix it; if it still cites something it never received, those citations are
     removed and a warning is added.

`corpus_agent()` is what evaluate.py uses: it returns the answer, the tool trace,
the retrieved passages, token counts and seconds.
"""

import asyncio
import os
import re
import sys
import time
from contextlib import asynccontextmanager
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
# The free Gemini tier allows ~20 generate requests a day per Gemini model, far too few for
# an evaluation, so the default is a Gemma model. Override: AGENT_MODEL=gemini-3-flash-preview
MODEL = os.environ.get("AGENT_MODEL", "gemma-4-31b-it")
MAX_SEARCHES = 6
RECURSION_LIMIT = 25

CITE_RE = re.compile(r"\[([a-z0-9_]+), ([^\]]+)\]")
UNIT_RE = re.compile(r"^(Article \d+[a-z]?|Annex [IVX]+|Section [\d.]+|Part [IVX]+)")
CITE_LINE_RE = re.compile(r"cite as \[([a-z0-9_]+), ([^\]]+)\]")


def text_of(message) -> str:
    content = message.content
    if isinstance(content, str):
        return content
    return "".join(b if isinstance(b, str) else b.get("text", "") for b in content)


def unit_of(location: str) -> str:
    m = UNIT_RE.match(location.strip())
    return m.group(1) if m else location.strip()


def check_citations(answer: str, retrieved: set[tuple[str, str]]) -> list[str]:
    """Citations in the answer that no search result supports."""
    bad = []
    for source, location in CITE_RE.findall(answer):
        if (source, unit_of(location)) not in retrieved:
            bad.append(f"[{source}, {location}]")
    return bad


def strip_citations(answer: str, bad: list[str]) -> str:
    for b in bad:
        answer = answer.replace(b, "[citation removed: not in the search results]")
    return answer


class CorpusAgent:
    def __init__(self, session: ClientSession, tools_meta: dict, approve):
        self.session, self.meta, self.approve = session, tools_meta, approve

    async def ask(self, question: str) -> dict:
        from langchain.agents import create_agent
        from langchain_core.tools import StructuredTool
        from langchain_google_genai import ChatGoogleGenerativeAI

        started = time.time()
        trace: list[dict] = []
        retrieved: set[tuple[str, str]] = set()
        passages: list[str] = []
        state = {"searches": 0}

        async def search(query: str) -> str:
            if state["searches"] >= MAX_SEARCHES:
                out = (f"Search limit reached ({MAX_SEARCHES}). Answer now from the passages you "
                       f"already have, or say the corpus does not cover the question.")
            else:
                state["searches"] += 1
                r = await self.session.call_tool("search", {"query": query})
                out = "\n".join(getattr(c, "text", "") for c in r.content)
                for s, loc in CITE_LINE_RE.findall(out):
                    retrieved.add((s, unit_of(loc)))
                passages.append(out)
            trace.append({"tool": "search", "args": {"query": query}, "result": out})
            return out

        async def add_document(path: str) -> str:
            if not self.approve(path):
                out = "The user did not approve adding this document. It was NOT added."
                trace.append({"tool": "add_document", "args": {"path": path}, "result": out, "approved": False})
                return out
            r = await self.session.call_tool("add_document", {"path": path})
            out = "\n".join(getattr(c, "text", "") for c in r.content)
            trace.append({"tool": "add_document", "args": {"path": path}, "result": out, "approved": True})
            return out

        tools = [
            StructuredTool.from_function(coroutine=search, name="search", description=self.meta["search"]),
            StructuredTool.from_function(coroutine=add_document, name="add_document",
                                         description=self.meta["add_document"]),
        ]
        model = ChatGoogleGenerativeAI(model=MODEL, temperature=0, max_retries=6)
        agent = create_agent(model, tools, system_prompt=(ROOT / "AGENTS.md").read_text())

        messages = [("user", question)]
        result = await agent.ainvoke({"messages": messages}, config={"recursion_limit": RECURSION_LIMIT})
        answer = text_of(result["messages"][-1]).strip()

        guardrail = None
        bad = check_citations(answer, retrieved)
        if bad:
            guardrail = "citation_retry"
            fix = ("These citations do not match any passage returned by your searches: "
                   + ", ".join(bad) + ". Rewrite the answer citing only passages you received "
                   "(copy the bracket from the search result), or say the indexed documents do not "
                   "cover the question.")
            result = await agent.ainvoke({"messages": result["messages"] + [("user", fix)]},
                                         config={"recursion_limit": RECURSION_LIMIT})
            answer = text_of(result["messages"][-1]).strip()
            bad = check_citations(answer, retrieved)
            if bad:
                guardrail = "citation_stripped"
                answer = strip_citations(answer, bad) + "\n\n(Warning: some citations could not be verified and were removed.)"

        tin = tout = 0
        for m in result["messages"]:
            u = getattr(m, "usage_metadata", None)
            if u:
                tin += u.get("input_tokens", 0)
                tout += u.get("output_tokens", 0)
        return {
            "question": question, "answer": answer, "trace": trace,
            "retrieved": sorted(retrieved), "passages": "\n\n".join(passages),
            "searches": state["searches"], "guardrail": guardrail,
            "tokens_in": tin, "tokens_out": tout, "seconds": round(time.time() - started, 1),
        }


def ask_in_terminal(path: str) -> bool:
    """Approval for add_document: ask the person; with no terminal, say no."""
    if not sys.stdin.isatty():
        print(f"[approval] add_document({path!r}) refused: no terminal to ask.", file=sys.stderr)
        return False
    return input(f"\nThe assistant wants to add {path!r} to the index. Approve? [y/N] ").strip().lower() in ("y", "yes")


@asynccontextmanager
async def corpus_agent(approve=ask_in_terminal):
    """Start server.py over MCP and yield an agent: `await agent.ask(question)`."""
    load_api_key()
    params = StdioServerParameters(command=sys.executable, args=[str(ROOT / "server.py")],
                                   cwd=str(ROOT), env=dict(os.environ))
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            meta = {t.name: (t.description or "") for t in (await session.list_tools()).tools}
            yield CorpusAgent(session, meta, approve)


async def run(question: str, approve=ask_in_terminal) -> dict:
    async with corpus_agent(approve) as agent:
        return await agent.ask(question)


def main():
    if len(sys.argv) < 2:
        raise SystemExit('usage: python agent.py "your question"')
    res = asyncio.run(run(" ".join(sys.argv[1:])))
    print(res["answer"])
    if res["retrieved"]:
        print("\nPassages retrieved: " + "; ".join(f"{s}, {u}" for s, u in res["retrieved"]))
    print(f"\n[{res['searches']} searches, {res['tokens_in']} tokens in / {res['tokens_out']} out, "
          f"{res['seconds']}s" + (f", guardrail: {res['guardrail']}" if res["guardrail"] else "") + "]")


if __name__ == "__main__":
    main()
