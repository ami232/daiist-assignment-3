"""
Assignment 3: the agent harness (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini. Tools come from server.py over MCP (stdio),
wrapped as LangChain tools. AGENTS.md is the system prompt.

Guardrails:
  1. Approval: add_document runs only after a human types "y". With no
     terminal (evaluation, check.py) it is refused unless AGENT_AUTO_APPROVE=1.
  2. Call limits: at most 6 tool calls and 8 model calls per question.
  3. Citation check (own guardrail): every [SOURCE, location] in the answer
     must point at a passage the search tool actually returned in this run,
     and a non-refusal answer must cite something. If not, the model gets one
     chance to fix it; if it still fails, the answer is replaced by a refusal.

`Harness.run(question)` returns the answer plus a trace (tool calls,
retrieved passages, tokens, seconds, guardrail events) for evaluate.py.
"""

from __future__ import annotations

import asyncio
import os
import sys
import time
from pathlib import Path

from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware, ToolCallLimitMiddleware
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.tools import StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from pydantic import BaseModel, Field

import retrieval
from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite")
REFUSAL = "The corpus does not cover this question."
MAX_TOOL_CALLS, MAX_MODEL_CALLS = 6, 8


def is_refusal(text: str) -> bool:
    """A refusal opens with the refusal sentence. An answer that covers part of
    the question and then says the corpus does not cover the rest (AGENTS.md
    rule 5) is an answer, not a refusal."""
    return text.strip().lstrip("*_> ").lower().startswith(REFUSAL.lower().rstrip("."))


def parse_results(text: str) -> list[dict]:
    """Turn the search tool's text back into passages (source, location, text)."""
    out = []
    for block in text.split("\n\n---\n\n"):
        lines = block.splitlines()
        if not lines or not lines[0].startswith("["):
            continue
        head = dict(part.split(": ", 1) for part in lines[0].split("] ", 1)[1].split(" | ") if ": " in part)
        out.append({"source": head.get("source", ""), "location": head.get("location", ""),
                    "units": [head.get("location", "")], "text": "\n".join(lines[2:])})
    return out


class SearchArgs(BaseModel):
    query: str = Field(description="What to look for in the merger control corpus, in plain English.")


class AddArgs(BaseModel):
    path: str = Field(description="Path of the file to add to the index.")


def ask_approval(path: str) -> bool:
    if os.environ.get("AGENT_AUTO_APPROVE") == "1":
        return True
    if not sys.stdin.isatty():
        return False
    reply = input(f"\nThe agent wants to add_document({path!r}). This embeds it and changes the index. Approve? [y/N] ")
    return reply.strip().lower() in ("y", "yes")


class Harness:
    def __init__(self, exclude_added: bool = False, verbose: bool = False):
        self.exclude_added = exclude_added
        self.verbose = verbose

    async def __aenter__(self):
        env = {**os.environ, "CORPUS_EXCLUDE_ADDED": "1" if self.exclude_added else "0"}
        load_api_key()
        env["GEMINI_API_KEY"] = os.environ["GEMINI_API_KEY"]
        params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT), env=env)
        self._stdio = stdio_client(params)
        read, write = await self._stdio.__aenter__()
        self._session = ClientSession(read, write)
        self.session = await self._session.__aenter__()
        await self.session.initialize()
        descriptions = {t.name: t.description for t in (await self.session.list_tools()).tools}

        async def search(query: str) -> str:
            text = await self._call("search", {"query": query})
            self.trace["retrieved"].extend(parse_results(text))
            return text

        async def add_document(path: str) -> str:
            if not ask_approval(path):
                self.trace["events"].append(f"add_document({path}) rejected: no approval")
                return "Not run: the user did not approve adding this document."
            self.trace["events"].append(f"add_document({path}) approved")
            return await self._call("add_document", {"path": path})

        tools = [
            StructuredTool.from_function(coroutine=search, name="search", description=descriptions["search"],
                                         args_schema=SearchArgs),
            StructuredTool.from_function(coroutine=add_document, name="add_document",
                                         description=descriptions["add_document"], args_schema=AddArgs),
        ]
        model = ChatGoogleGenerativeAI(model=MODEL, temperature=0, max_retries=2, timeout=120)
        self.agent = create_agent(
            model, tools,
            system_prompt=(ROOT / "AGENTS.md").read_text(encoding="utf-8"),
            middleware=[ToolCallLimitMiddleware(run_limit=MAX_TOOL_CALLS, exit_behavior="continue"),
                        ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS, exit_behavior="end")],
        )
        return self

    async def __aexit__(self, *exc):
        await self._session.__aexit__(*exc)
        await self._stdio.__aexit__(*exc)

    async def _call(self, name: str, args: dict) -> str:
        self.trace["tool_calls"].append({"tool": name, "args": args})
        if self.verbose:
            print(f"  -> {name}({args})", file=sys.stderr)
        res = await self.session.call_tool(name, args)
        return "\n".join(getattr(c, "text", "") for c in res.content)

    async def _invoke(self, messages: list) -> list:
        out = await self.agent.ainvoke({"messages": messages})
        msgs = out["messages"]
        for m in msgs[len(messages):]:
            if isinstance(m, AIMessage) and m.usage_metadata:
                self.trace["input_tokens"] += m.usage_metadata.get("input_tokens", 0)
                self.trace["output_tokens"] += m.usage_metadata.get("output_tokens", 0)
        return msgs

    def check_citations(self, answer: str) -> list[str]:
        """Problems with the answer's citations; empty list means it passes."""
        if is_refusal(answer) and not retrieval.citations(answer):
            return []
        cites = retrieval.citations(answer)
        if not cites:
            return ["the answer makes claims but cites nothing"]
        return [f"[{s}, {l}] is not among the passages search returned"
                for s, l in cites if not retrieval.citation_valid(s, l, self.trace["retrieved"])]

    async def run(self, question: str) -> dict:
        self.trace = {"tool_calls": [], "retrieved": [], "events": [], "input_tokens": 0, "output_tokens": 0}
        started = time.time()
        messages = await self._invoke([HumanMessage(question)])
        answer = last_text(messages)
        problems = self.check_citations(answer)
        if problems:
            self.trace["events"].append("citation guardrail fired: " + "; ".join(problems))
            fix = HumanMessage(
                "Your answer failed the citation check: " + "; ".join(problems) + ". Rewrite it so that every "
                "claim cites a passage exactly as the search results label it, as [SOURCE, location]. "
                f"If the search results do not support an answer, reply: {REFUSAL}")
            messages = await self._invoke(messages + [fix])
            answer = last_text(messages)
            problems = self.check_citations(answer)
            if problems:
                self.trace["events"].append("citation guardrail replaced the answer: " + "; ".join(problems))
                answer = f"{REFUSAL} (An answer was drafted but its citations could not be verified.)"
        self.trace["seconds"] = round(time.time() - started, 2)
        return {"question": question, "answer": answer, **self.trace}


def last_text(messages: list) -> str:
    for m in reversed(messages):
        if isinstance(m, AIMessage) and not m.tool_calls:
            t = m.text if isinstance(m.text, str) else m.text()
            if t.strip():
                return t.strip()
    return REFUSAL


async def ask(question: str, exclude_added: bool = False, verbose: bool = False) -> dict:
    async with Harness(exclude_added=exclude_added, verbose=verbose) as h:
        return await h.run(question)


def main() -> None:
    question = " ".join(sys.argv[1:]).strip()
    if not question:
        raise SystemExit('usage: python agent.py "your question"')
    res = asyncio.run(ask(question, verbose=True))
    print(res["answer"])
    if res["retrieved"]:
        print("\nPassages retrieved:")
        for s, l in dict.fromkeys((r["source"], r["location"]) for r in res["retrieved"]):
            print(f"  [{s}, {l}]")
    for e in res["events"]:
        print(f"\n[guardrail] {e}")
    print(f"\n({res['input_tokens']} in / {res['output_tokens']} out tokens, {res['seconds']}s)")


if __name__ == "__main__":
    main()
