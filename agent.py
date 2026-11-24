"""
Assignment 3: the agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the tools of server.py over MCP (stdio)
and AGENTS.md as the system prompt.

Guardrails
- Approval: add_document runs only after a human says yes (denied when there is
  no terminal to ask, e.g. during evaluation).
- Call limits: at most MAX_TOOL_CALLS tool calls and MAX_MODEL_CALLS model calls
  per question.
- Verified citations (extra guardrail): every [source | location] in the answer
  must match a passage the search tool actually returned in this run, and an
  answer without citations is only accepted if it is a refusal. Otherwise the
  agent gets one retry with feedback; if it fails again, the answer is withheld.

`CorpusAgent.ask()` returns the answer plus the tool trace, for evaluate.py.
"""

from __future__ import annotations

import asyncio
import re
import sys
import time
from pathlib import Path
from typing import Callable

from pydantic import BaseModel, Field

ROOT = Path(__file__).resolve().parent
MODEL = "gemini-3.5-flash"
MAX_TOOL_CALLS = 6
MAX_MODEL_CALLS = 8

CITATION = re.compile(r"\[([^\[\]|]+?)\s*\|\s*([^\[\]]+?)\]")
RESULT_HEADER = re.compile(r"^### Result \d+\s+\[([^\[\]|]+?)\s*\|\s*([^\[\]]+?)\]", re.M)
REFUSAL = re.compile(r"(don'?t|do not|does not|doesn'?t) cover|not covered|no information|"
                     r"couldn'?t find|could not find|not in the (fda )?documents", re.I)
WITHHELD = ("I couldn't produce an answer backed by valid citations from the FDA documents, "
            "so I won't guess. When in doubt, throw it out, and check foodsafety.gov or the FDA.")


def log(*a) -> None:
    print(*a, file=sys.stderr, flush=True)


def text_of(message) -> str:
    """Message content as plain text (Gemini may return a list of parts)."""
    c = message.content
    if isinstance(c, str):
        return c
    return "".join(p.get("text", "") if isinstance(p, dict) else str(p) for p in c)


def ask_terminal(path: str) -> bool:
    if not sys.stdin.isatty():
        log(f"[approval] add_document({path!r}) denied: no terminal to ask for approval.")
        return False
    answer = input(f"\nThe agent wants to add this document to the index:\n  {path}\nApprove? [y/N] ")
    return answer.strip().lower() in ("y", "yes", "s", "si", "sí")


def check_citations(answer: str, allowed: set[tuple[str, str]]) -> list[str]:
    """Problems with the answer's citations; empty list = passes the guardrail."""
    cited = [(s.strip(), l.strip()) for s, l in CITATION.findall(answer)]
    problems = [f"[{s} | {l}] is not one of the passages returned by search"
                for s, l in cited if (s, l) not in allowed]
    if not cited and not REFUSAL.search(answer):
        problems.append("the answer makes claims without any citation")
    return problems


class SearchArgs(BaseModel):
    query: str = Field(description="What to look up, in English, naming the food and situation.")


class AddArgs(BaseModel):
    path: str = Field(description="Path of a local .pdf, .html, .txt or .md file to add to the index.")


class CorpusAgent:
    """Keeps one MCP session to server.py open for many questions."""

    def __init__(self, approve: Callable[[str], bool] = ask_terminal, model: str = MODEL):
        self.approve, self.model_name = approve, model

    async def __aenter__(self):
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client

        params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT))
        self._stdio = stdio_client(params)
        read, write = await self._stdio.__aenter__()
        self._session_cm = ClientSession(read, write)
        self.session = await self._session_cm.__aenter__()
        await self.session.initialize()
        tools = {t.name: t for t in (await self.session.list_tools()).tools}
        self.agent = self._build_agent(tools)
        return self

    async def __aexit__(self, *exc):
        await self._session_cm.__aexit__(*exc)
        await self._stdio.__aexit__(*exc)

    async def _call_tool(self, name: str, args: dict) -> str:
        result = await self.session.call_tool(name, args)
        return "\n".join(getattr(c, "text", "") for c in result.content).strip()

    def _build_agent(self, mcp_tools: dict):
        from langchain.agents import create_agent
        from langchain.agents.middleware import ModelCallLimitMiddleware, ToolCallLimitMiddleware
        from langchain_core.tools import StructuredTool
        from langchain_google_genai import ChatGoogleGenerativeAI

        from api_key import load_api_key

        load_api_key()

        async def search(query: str) -> str:
            return await self._call_tool("search", {"query": query})

        async def add_document(path: str) -> str:
            if not self.approve(path):
                return "Not added: the user did not approve adding this document."
            return await self._call_tool("add_document", {"path": path})

        tools = [
            StructuredTool.from_function(coroutine=search, name="search",
                                         description=mcp_tools["search"].description, args_schema=SearchArgs),
            StructuredTool.from_function(coroutine=add_document, name="add_document",
                                         description=mcp_tools["add_document"].description, args_schema=AddArgs),
        ]
        model = ChatGoogleGenerativeAI(model=self.model_name, temperature=0, max_retries=6)
        system = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
        return create_agent(
            model, tools, system_prompt=system,
            middleware=[ToolCallLimitMiddleware(run_limit=MAX_TOOL_CALLS),
                        ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS)],
        )

    async def ask(self, question: str) -> dict:
        """Answer one question. Returns answer, trace, citations, guardrail info, tokens, seconds."""
        from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

        started = time.time()
        messages = [HumanMessage(question)]
        guardrail = {"fired": False, "problems": [], "retried": False, "withheld": False}
        for attempt in range(2):
            result = await self.agent.ainvoke({"messages": messages})
            messages = result["messages"]
            allowed = {(s.strip(), l.strip()) for m in messages if isinstance(m, ToolMessage)
                       for s, l in RESULT_HEADER.findall(text_of(m))}
            final = next((m for m in reversed(messages) if isinstance(m, AIMessage) and not m.tool_calls), None)
            answer = text_of(final).strip() if final else ""
            problems = check_citations(answer, allowed)
            if not problems:
                break
            guardrail.update(fired=True, problems=guardrail["problems"] + problems)
            log(f"[guardrail] citation check failed (attempt {attempt + 1}): {problems}")
            if attempt == 0:
                guardrail["retried"] = True
                messages = messages + [HumanMessage(
                    "Your answer failed the citation check: " + "; ".join(problems) + ". Rewrite it. "
                    "Cite only passages returned by search, copying their [source | location] exactly, "
                    "or say the FDA documents don't cover the question.")]
            else:
                guardrail["withheld"] = True
                answer = WITHHELD

        trace, tokens_in, tokens_out = [], 0, 0
        outputs = {m.tool_call_id: text_of(m) for m in messages if isinstance(m, ToolMessage)}
        for m in messages:
            if isinstance(m, AIMessage):
                usage = m.usage_metadata or {}
                tokens_in += usage.get("input_tokens", 0)
                tokens_out += usage.get("output_tokens", 0)
                for call in m.tool_calls:
                    trace.append({"tool": call["name"], "args": call["args"],
                                  "output": outputs.get(call["id"], "")})
        return {
            "question": question,
            "answer": answer,
            "citations": sorted({f"{s.strip()} | {l.strip()}" for s, l in CITATION.findall(answer)}),
            "trace": trace,
            "guardrail": guardrail,
            "tokens_in": tokens_in,
            "tokens_out": tokens_out,
            "seconds": round(time.time() - started, 2),
        }


async def ask_once(question: str) -> dict:
    async with CorpusAgent() as agent:
        return await agent.ask(question)


def main() -> None:
    question = " ".join(sys.argv[1:]).strip()
    if not question:
        raise SystemExit('usage: python agent.py "your question"')
    r = asyncio.run(ask_once(question))
    print(r["answer"])
    if r["citations"]:
        print("\nSources:")
        for c in r["citations"]:
            print(f"  - {c}")
    log(f"\n[{len(r['trace'])} tool calls, {r['tokens_in']}+{r['tokens_out']} tokens, {r['seconds']} s]")


if __name__ == "__main__":
    main()
