"""
Assignment 3: the harness (`main.py ask "question"` runs `python agent.py "question"`).

A LangChain `create_agent` on Gemini with:
- the tools of server.py, reached over MCP (stdio), exactly as an editor reaches them;
- AGENTS.md as the system prompt;
- approval: add_document only runs after a human types "yes" (refused when no one is there);
- call limits: at most 6 tool calls and 8 model calls per question;
- extra guardrail, the citation check: every [citation] in the answer must be one the
  search tool returned in this run, and every non-refusal answer must cite something.
  If not, the model gets one chance to fix it; if it still fails, the answer is withheld
  and replaced by a refusal, so an uncheckable answer never reaches the user.

evaluate.py uses `CorpusAgent` directly to get the answer and the tool trace.
"""

from __future__ import annotations

import asyncio
import os
import re
import sys
import time
from contextlib import AsyncExitStack
from pathlib import Path

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
SYSTEM_PROMPT = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
MODEL = os.environ.get("AGENT_MODEL", "gemini-3.5-flash-lite")
REFUSAL = "The corpus does not cover this."
TOOL_LIMIT, MODEL_LIMIT = 6, 8

CITE_LINE = re.compile(r"CITE AS: \[([^\]]+)\]")
CITATION = re.compile(r"\[([^\[\]]{3,120})\]")


def norm(cite: str) -> str:
    return re.sub(r"\s+", " ", cite.strip().lower().replace("art.", "article"))


def strip_paragraphs(cite: str) -> str:
    """'GDPR, Article 33(1)(a)' or 'GDPR, Article 83, paragraph 4' -> 'gdpr, article 33' / 'gdpr, article 83':
    pointing to a paragraph inside a retrieved article is fine (first version blocked these, see REPORT.md)."""
    cite = re.sub(r",? (paragraph|para\.?|point|subparagraph) .*$", "", norm(cite))
    return re.sub(r"(\(\w{1,4}\))+$", "", cite).strip()


def citations_in(answer: str) -> list[str]:
    found = []
    for inner in CITATION.findall(answer):
        for piece in inner.split(";"):
            piece = piece.strip()
            if piece and re.search(r"[A-Za-z]", piece) and "," in piece:
                found.append(piece)
    return found


def check_citations(answer: str, retrieved: set[str]) -> dict:
    """The code check behind the guardrail (also used by evaluate.py)."""
    allowed = {norm(c) for c in retrieved}
    cites = citations_in(answer)
    invalid = [c for c in cites if norm(c) not in allowed and strip_paragraphs(c) not in allowed]
    refusal = REFUSAL.lower() in answer.lower()
    return {
        "citations": cites,
        "invalid": invalid,
        "refusal": refusal,
        "uncited": not refusal and not cites,
        "ok": not invalid and (refusal or bool(cites)),
    }


def text_of(message) -> str:
    content = message.content
    if isinstance(content, list):
        return "".join(part.get("text", "") if isinstance(part, dict) else str(part) for part in content)
    return str(content)


def ask_human(path: str) -> bool:
    """Approval step for add_document: a person at the terminal has to type yes."""
    if not sys.stdin.isatty():
        print(f"[approval] add_document({path!r}) refused: nobody is at the terminal to approve it.", file=sys.stderr)
        return False
    try:
        reply = input(f"\nThe agent wants to add {path!r} to the index (this embeds it and changes later answers).\n"
                      f"Approve? [yes/no] ").strip().lower()
    except EOFError:
        reply = ""   # input closed: treat as no
    return reply in ("y", "yes")


class CorpusAgent:
    """Starts server.py over MCP once and answers any number of questions."""

    def __init__(self, approve=ask_human, model: str = MODEL, server_env: dict | None = None):
        self.approve, self.model, self.server_env = approve, model, server_env or {}

    async def __aenter__(self):
        from langchain.agents import create_agent
        from langchain.agents.middleware import ModelCallLimitMiddleware, ToolCallLimitMiddleware
        from langchain_core.tools import StructuredTool
        from langchain_google_genai import ChatGoogleGenerativeAI
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client

        load_api_key()
        self.stack = AsyncExitStack()
        params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT),
                                       env={**os.environ, **self.server_env})
        read, write = await self.stack.enter_async_context(stdio_client(params))
        self.session = await self.stack.enter_async_context(ClientSession(read, write))
        await self.session.initialize()

        tools = []
        for spec in (await self.session.list_tools()).tools:
            tools.append(StructuredTool(
                name=spec.name, description=spec.description or "", args_schema=spec.input_schema,
                coroutine=self._caller(spec.name),
            ))
        self.llm = ChatGoogleGenerativeAI(model=self.model, max_retries=6)
        self.agent = create_agent(
            self.llm, tools, system_prompt=SYSTEM_PROMPT,
            middleware=[ToolCallLimitMiddleware(run_limit=TOOL_LIMIT, exit_behavior="continue"),
                        ModelCallLimitMiddleware(run_limit=MODEL_LIMIT, exit_behavior="end")],
        )
        return self

    async def __aexit__(self, *exc):
        await self.stack.aclose()

    def _caller(self, name: str):
        async def call(**kwargs) -> str:
            if name == "add_document":
                path = kwargs.get("path", "")
                if not self.approve(path):
                    self.trace.append({"tool": name, "args": kwargs, "result": "REFUSED by approval step"})
                    return "The user did not approve adding this document. Nothing was added."
            result = await self.session.call_tool(name, kwargs)
            text = "\n".join(getattr(c, "text", "") for c in result.content)
            self.trace.append({"tool": name, "args": kwargs, "result": text})
            return text
        return call

    async def ask(self, question: str) -> dict:
        from langchain_core.messages import HumanMessage

        self.trace = []
        started = time.time()
        state = await self.agent.ainvoke({"messages": [HumanMessage(question)]})
        messages = state["messages"]
        answer = text_of(messages[-1]).strip()
        retrieved = {c for t in self.trace if t["tool"] == "search" for c in CITE_LINE.findall(t["result"])}
        check = check_citations(answer, retrieved)
        guardrail, draft, problem = "passed", "", ""
        searched = any(t["tool"] == "search" for t in self.trace)
        if not searched and any(t["tool"] == "add_document" for t in self.trace):
            guardrail = "not applicable (add_document request, no facts from the corpus)"
        elif not check["ok"]:
            draft = answer
            # one repair attempt: tell the model exactly what is wrong
            problem = (f"these citations are not in the search results: {check['invalid']}" if check["invalid"]
                       else "it states facts without any citation")
            allowed = "\n".join(f"[{c}]" for c in sorted(retrieved)) or "(none: nothing was retrieved)"
            fix = await self.llm.ainvoke([
                ("system", SYSTEM_PROMPT),
                ("human", f"Question: {question}\n\nDraft answer:\n{answer}\n\nThe draft breaks the citation rule: "
                          f"{problem}. Allowed citations:\n{allowed}\n\nRewrite the answer using only these "
                          f"citations, removing any claim you cannot cite, or reply '{REFUSAL}'."),
            ])
            messages = messages + [fix]
            answer = text_of(fix).strip()
            check = check_citations(answer, retrieved)
            guardrail = "repaired"
            if not check["ok"]:
                guardrail = "blocked"
                answer = (f"{REFUSAL} (An answer was drafted but withheld because its citations could not be "
                          f"verified against the retrieved passages.)")
                check = check_citations(answer, retrieved)
        usage = {"input_tokens": 0, "output_tokens": 0}
        for m in messages:
            meta = getattr(m, "usage_metadata", None) or {}
            usage["input_tokens"] += meta.get("input_tokens", 0)
            usage["output_tokens"] += meta.get("output_tokens", 0)
        return {
            "question": question,
            "answer": answer,
            "trace": self.trace,
            "retrieved_cites": sorted(retrieved),
            "check": check,
            "guardrail": guardrail,
            "guardrail_draft": draft,
            "guardrail_problem": problem,
            "tool_calls": len(self.trace),
            "seconds": round(time.time() - started, 1),
            **usage,
        }


async def run_agent(question: str) -> dict:
    async with CorpusAgent() as agent:
        return await agent.ask(question)


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit('usage: python agent.py "your question"')
    result = asyncio.run(run_agent(" ".join(sys.argv[1:])))
    print(result["answer"])
    print("\nSources searched:")
    for cite in result["retrieved_cites"]:
        print(f"  [{cite}]")
    print(f"\n(guardrail: {result['guardrail']}; {result['tool_calls']} tool calls; "
          f"{result['input_tokens']}+{result['output_tokens']} tokens; {result['seconds']}s)")


if __name__ == "__main__":
    main()
