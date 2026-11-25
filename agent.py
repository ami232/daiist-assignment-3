"""Own agent harness: LangChain/LangGraph ReAct agent over the MCP server.

System prompt  : AGENTS.md
Guardrail 1    : human approval before add_document runs (denied -> tool returns DENIED, nothing is indexed)
Guardrail 2    : citation check on every answer. Each [doc:Location] cited must have been returned by `search`
                 in this run; otherwise the agent gets one chance to fix it, then the answer is replaced by NOT_FOUND.
                 (Plus a hard step limit so a looping agent cannot burn quota.)"""
from __future__ import annotations

import asyncio
from contextlib import AsyncExitStack
import re
import sys
import time
from typing import Callable

from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.tools import StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from pydantic import BaseModel, Field
from langgraph.errors import GraphRecursionError
try:                                              # LangChain >= 1.0
    from langchain.agents import create_agent

    def make_agent(llm, tools, prompt):
        return create_agent(llm, tools, system_prompt=prompt)
except ImportError:                               # older LangGraph
    from langgraph.prebuilt import create_react_agent

    def make_agent(llm, tools, prompt):
        return create_react_agent(llm, tools, prompt=prompt)

import os

from config import CHAT_MODEL, NOT_FOUND, ROOT, get_key, make_llm

CITE = re.compile(r"\[([a-z0-9_]+:[^\]\[]+?)\]")
BLOCK = re.compile(r"^### \[([^\]]+)\][^\n]*\n", re.M)
MAX_STEPS = 14


TRAIL = re.compile(r"(\s*\((?:part \d+/\d+|\w{1,3})\))+$")


def norm(c: str) -> str:
    """'gdpr:Article 83(5)' and 'ai_act:Article 3 (part 2/8)' both normalise to the article, which is what
    search returns and what we compare against. Paragraph numbers are extra precision, not a fabrication."""
    return TRAIL.sub("", c.strip())


def cites(text: str) -> list[str]:
    """All citations in an answer, normalised. A bracket may hold several: [a:Article 5, b:Article 9]."""
    out = []
    for m in CITE.findall(text):
        for part in re.split(r",\s*(?=[a-z0-9_]+:)|;\s*", m):
            if part.strip():
                out.append(norm(part))
    return out


def text_of(content) -> str:
    if isinstance(content, str):
        return content
    return "".join(b.get("text", "") if isinstance(b, dict) else str(b) for b in content)


def parse_search_output(text: str) -> dict[str, str]:
    """citation -> passage text, from the search tool's output format."""
    out, parts = {}, BLOCK.split(text)
    for cit, body in zip(parts[1::2], parts[2::2]):
        out[norm(cit)] = out.get(norm(cit), "") + body.strip() + "\n"
    return out


def default_approve(path: str) -> bool:
    return input(f"\n⚠  Agent wants to index '{path}'. Allow? [y/N] ").strip().lower() == "y"


class RagAgent:
    def __init__(self, approve: Callable[[str], bool] = default_approve):
        self.approve = approve
        self.denied: list[str] = []

    async def __aenter__(self):
        """Start server.py over stdio (as an editor would) and keep one session open for all questions."""
        self._stack = AsyncExitStack()
        params = StdioServerParameters(command=sys.executable, args=[str(ROOT / "server.py")], cwd=str(ROOT))
        read, write = await self._stack.enter_async_context(stdio_client(params))
        self.session = await self._stack.enter_async_context(ClientSession(read, write))
        await self.session.initialize()
        desc = {t.name: (t.description or "") for t in (await self.session.list_tools()).tools}

        class SearchArgs(BaseModel):
            query: str = Field(description="what to look for, in natural language")
            k: int = Field(default=5, description="number of passages (1-10)")

        class AddArgs(BaseModel):
            path: str = Field(description="path of the file to index")

        async def search(query: str, k: int = 5) -> str:
            return await self._call("search", {"query": query, "k": k})

        async def add_document(path: str) -> str:
            if not self.approve(path):                                   # guardrail 1: human approval
                self.denied.append(path)
                return "DENIED: the human did not approve indexing this file. Tell the user it was not added."
            return await self._call("add_document", {"path": path})

        tools = [StructuredTool.from_function(coroutine=search, name="search", description=desc.get("search", "Search the corpus."), args_schema=SearchArgs),
                 StructuredTool.from_function(coroutine=add_document, name="add_document", description=desc.get("add_document", "Index a file."), args_schema=AddArgs)]
        llm = make_llm(CHAT_MODEL)
        self.agent = make_agent(llm, tools, (ROOT / "AGENTS.md").read_text())
        return self

    async def __aexit__(self, *exc):
        await self._stack.aclose()
        return False

    async def _call(self, name: str, args: dict) -> str:
        for attempt in (1, 2):                                  # one retry: a tool crash must not look like "not found"
            res = await self.session.call_tool(name, args)
            text = "\n".join(getattr(c, "text", "") for c in res.content).strip()
            bad = getattr(res, "is_error", False) or getattr(res, "isError", False)
            if not bad:
                return text
            await asyncio.sleep(1)
        return f"ERROR: {text}"

    async def ask(self, question: str) -> dict:
        t0 = time.time()
        msgs = [HumanMessage(question)]
        guardrail, answer, bad = "", "", []
        drafts: list[str] = []
        for attempt in range(2):
            try:
                out = await self.agent.ainvoke({"messages": msgs}, {"recursion_limit": MAX_STEPS})
            except GraphRecursionError:
                answer, guardrail = f"{NOT_FOUND}: step limit reached.", "step_limit"
                break
            msgs = out["messages"]
            answer = text_of(msgs[-1].content).strip()
            retrieved = self._retrieved(msgs)
            bad = [c for c in cites(answer) if c not in retrieved]
            if bad:
                drafts.append(answer)
            if not bad:
                break
            if attempt == 0:
                msgs.append(HumanMessage(f"Guardrail: you cited {bad}, which `search` did not return. Re-answer using "
                                         f"only citations that search returned, or reply with {NOT_FOUND}:."))
        if bad:
            answer, guardrail = f"{NOT_FOUND}: the draft answer cited passages that were never retrieved.", "bad_citation"
        retrieved = self._retrieved(msgs)
        tin = tout = 0
        for m in msgs:
            if isinstance(m, AIMessage) and m.usage_metadata:
                tin += m.usage_metadata.get("input_tokens", 0)
                tout += m.usage_metadata.get("output_tokens", 0)
        return dict(question=question, answer=answer, refused=answer.upper().startswith(NOT_FOUND),
                    cited=sorted(set(cites(answer))), retrieved=retrieved,
                    guardrail=guardrail, seconds=round(time.time() - t0, 1), tokens_in=tin, tokens_out=tout,
                    searches=sum(1 for m in msgs if isinstance(m, ToolMessage) and m.name == "search"),
                    add_denied=list(self.denied), draft=drafts, bad_citations=bad,
                    tool_errors=sum(1 for m in msgs if isinstance(m, ToolMessage) and text_of(m.content).startswith("ERROR")))

    @staticmethod
    def _retrieved(msgs) -> dict[str, str]:
        out: dict[str, str] = {}
        for m in msgs:
            if isinstance(m, ToolMessage) and m.name == "search":
                for c, t in parse_search_output(text_of(m.content)).items():
                    out[c] = out.get(c, "") + t
        return out


async def ask_once(question: str, approve=default_approve) -> dict:
    async with RagAgent(approve) as a:
        return await a.ask(question)


if __name__ == "__main__":
    r = asyncio.run(ask_once(" ".join(sys.argv[1:]) or "How long do I have to report a personal data breach?"))
    print(r["answer"], f"\n\n[{r['seconds']}s, {r['tokens_in']}+{r['tokens_out']} tokens, searches={r['searches']}]")
