"""
Assignment 3: your agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with its tools coming from server.py over MCP and AGENTS.md
as the system prompt. Three safeguards:

  1. approval  : add_document never runs unless the user says yes (callback `approve`).
  2. call limit: at most MAX_TOOL_CALLS tool calls per question (ToolCallLimitMiddleware).
  3. citation guardrail (my own): every [SOURCE, p. N] in the answer must match a passage that the
     search really returned. If not, the model gets ONE chance to repair; if it still cites
     something it did not retrieve, the answer is replaced by "NOT COVERED: ...".

`ask(question)` returns an AgentResult (answer, tool trace, tokens, seconds) for evaluate.py.
"""

from __future__ import annotations

import asyncio
import os
import re
import sys
import time
from contextlib import AsyncExitStack
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent
AGENT_MODEL = os.getenv("GEMINI_AGENT_MODEL", "gemini-3.5-flash-lite")
MAX_TOOL_CALLS = 6
REFUSAL_PREFIX = "NOT COVERED"

CITATION = re.compile(r"\[([A-Za-z0-9][A-Za-z0-9_.-]*),\s*p\.\s*(\d+)(?:\s*-\s*(\d+))?\]")
PASSAGE_HEADER = re.compile(r"^\[\d+\]\s+\[([A-Za-z0-9][A-Za-z0-9_.-]*),\s*p\.\s*(\d+)(?:-(\d+))?\]", re.M)


@dataclass
class AgentResult:
    question: str
    answer: str                       # what the user sees (after the guardrail)
    raw_answer: str                   # what the model wrote first
    tool_calls: list[dict] = field(default_factory=list)   # {name, args, result}
    retrieved: list[tuple[str, int, int]] = field(default_factory=list)  # (source, first page, last page)
    input_tokens: int = 0
    output_tokens: int = 0
    seconds: float = 0.0
    guardrail: str = ""               # "" | "repaired" | "replaced"
    guardrail_detail: str = ""
    error: str = ""

    @property
    def refused(self) -> bool:
        return self.answer.strip().upper().startswith(REFUSAL_PREFIX)

    @property
    def evidence(self) -> str:
        """All passages the model saw, for the judge."""
        return "\n\n".join(c["result"] for c in self.tool_calls if c["name"] == "search")


def system_prompt() -> str:
    return (ROOT / "AGENTS.md").read_text(encoding="utf-8")


# --- citation guardrail -------------------------------------------------------------------
def parse_retrieved(tool_text: str) -> list[tuple[str, int, int]]:
    out = []
    for m in PASSAGE_HEADER.finditer(tool_text):
        a = int(m.group(2))
        out.append((m.group(1), a, int(m.group(3)) if m.group(3) else a))
    return out


def check_citations(answer: str, retrieved: list[tuple[str, int, int]]) -> tuple[bool, str]:
    """(ok, problem). A citation is valid if some retrieved passage is from that source and its
    pages overlap the cited pages. An answer that is not a refusal must cite something."""
    cites = [(m.group(1), int(m.group(2)), int(m.group(3) or m.group(2))) for m in CITATION.finditer(answer)]
    if answer.strip().upper().startswith(REFUSAL_PREFIX):
        return True, ""
    if not cites:
        return False, "the answer has no citation"
    bad = [f"[{s}, p. {a}{'-' + str(b) if b != a else ''}]" for s, a, b in cites
           if not any(s == rs and a <= re_ and rs_a <= b for rs, rs_a, re_ in retrieved)]
    if bad:
        return False, "these citations are not in the search results: " + ", ".join(bad)
    return True, ""


# --- MCP tools -> LangChain tools -----------------------------------------------------------
def default_approve(tool_name: str, args: dict) -> bool:
    """Ask on the terminal. With nobody to ask (no TTY) the answer is no."""
    if not sys.stdin or not sys.stdin.isatty():
        return False
    print(f"\nThe agent wants to run {tool_name}({args}). This changes the index.", file=sys.stderr)
    return input("Approve? [y/N] ").strip().lower() in ("y", "yes", "s", "si", "sí")


class CorpusAgent:
    """Starts server.py over stdio, builds the LangChain agent and answers questions."""

    def __init__(self, approve=default_approve, model: str | None = None, server_script: Path | None = None,
                 llm=None):
        self.approve = approve
        self.model = model or AGENT_MODEL
        self.server_script = Path(server_script or ROOT / "server.py")
        self._llm = llm
        self._stack: AsyncExitStack | None = None
        self.approvals: list[dict] = []

    async def __aenter__(self) -> "CorpusAgent":
        from langchain.agents import create_agent
        from langchain.agents.middleware import ToolCallLimitMiddleware
        from langchain_core.tools import StructuredTool
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client

        self._stack = AsyncExitStack()
        params = StdioServerParameters(command=sys.executable, args=[str(self.server_script)], cwd=str(ROOT))
        read, write = await self._stack.enter_async_context(stdio_client(params))
        self._session = await self._stack.enter_async_context(ClientSession(read, write))
        await self._session.initialize()
        mcp_tools = (await self._session.list_tools()).tools
        self.tool_log: list[dict] = []
        tools = [self._wrap(StructuredTool, t) for t in mcp_tools]
        if self._llm is None:
            from api_key import load_api_key
            from langchain_google_genai import ChatGoogleGenerativeAI

            self._llm = ChatGoogleGenerativeAI(model=self.model, temperature=0, google_api_key=load_api_key(), max_retries=3)
        self.graph = create_agent(
            self._llm, tools=tools, system_prompt=system_prompt(),
            middleware=[ToolCallLimitMiddleware(run_limit=MAX_TOOL_CALLS, exit_behavior="continue")],
        )
        return self

    async def __aexit__(self, *exc) -> None:
        if self._stack:
            await self._stack.aclose()

    def _wrap(self, StructuredTool, tool):
        name = tool.name

        async def call(**kwargs) -> str:
            if name == "add_document":
                approved = bool(self.approve(name, kwargs))
                self.approvals.append({"tool": name, "args": kwargs, "approved": approved})
                if not approved:
                    result = "NOT RUN: the user did not approve add_document. Tell the user the document was not added."
                    self.tool_log.append({"name": name, "args": kwargs, "result": result})
                    return result
            res = await self._session.call_tool(name, kwargs)
            text = "\n".join(getattr(c, "text", "") for c in res.content).strip()
            self.tool_log.append({"name": name, "args": kwargs, "result": text})
            return text

        return StructuredTool.from_function(coroutine=call, name=name, description=tool.description or name,
                                            args_schema=tool.input_schema)

    async def ask(self, question: str) -> AgentResult:
        from langchain_core.messages import AIMessage, HumanMessage

        started = time.time()
        self.tool_log = []
        result = AgentResult(question=question, answer="", raw_answer="")
        messages = [HumanMessage(question)]
        try:
            out = await self.graph.ainvoke({"messages": messages})
            msgs = out["messages"]
            raw = _final_text(msgs)
            retrieved = _retrieved(self.tool_log)
            ok, problem = check_citations(raw, retrieved)
            answer = raw
            if not ok:
                result.guardrail_detail = problem
                repair = (f"Your answer cannot be shown: {problem}. Rewrite it using only the passages the search returned, "
                          f"citing them exactly as [SOURCE, p. N]. If they do not answer the question, reply "
                          f"'{REFUSAL_PREFIX}: ...' instead.")
                out2 = await self.graph.ainvoke({"messages": msgs + [HumanMessage(repair)]})
                msgs = out2["messages"]
                answer = _final_text(msgs)
                retrieved = _retrieved(self.tool_log)
                ok2, problem2 = check_citations(answer, retrieved)
                if ok2:
                    result.guardrail = "repaired"
                else:
                    result.guardrail = "replaced"
                    result.guardrail_detail = problem2
                    answer = f"{REFUSAL_PREFIX}: I could not produce an answer whose citations match the passages I retrieved."
            result.raw_answer, result.answer, result.retrieved = raw, answer, retrieved
            for m in msgs:
                if isinstance(m, AIMessage) and m.usage_metadata:
                    result.input_tokens += m.usage_metadata.get("input_tokens", 0)
                    result.output_tokens += m.usage_metadata.get("output_tokens", 0)
        except Exception as error:  # noqa: BLE001 - one failed question must not stop an evaluation
            result.error = f"{type(error).__name__}: {str(error)[:300]}"
            result.answer = f"{REFUSAL_PREFIX}: the agent failed ({type(error).__name__})."
        result.tool_calls = list(self.tool_log)
        result.seconds = time.time() - started
        return result


def _final_text(messages) -> str:
    for m in reversed(messages):
        if m.type == "ai" and not getattr(m, "tool_calls", None):
            c = m.content
            if isinstance(c, list):
                c = "".join(p.get("text", "") if isinstance(p, dict) else str(p) for p in c)
            return (c or "").strip()
    return ""


def _retrieved(tool_log: list[dict]) -> list[tuple[str, int, int]]:
    out: list[tuple[str, int, int]] = []
    for c in tool_log:
        if c["name"] == "search":
            out.extend(parse_retrieved(c["result"]))
    return out


async def ask_once(question: str, approve=default_approve) -> AgentResult:
    async with CorpusAgent(approve=approve) as agent:
        return await agent.ask(question)


def main() -> int:
    if len(sys.argv) < 2:
        print('usage: python agent.py "your question"', file=sys.stderr)
        return 2
    result = asyncio.run(ask_once(" ".join(sys.argv[1:])))
    print(result.answer)
    if result.retrieved:
        seen = []
        for s, a, b in result.retrieved:
            tag = f"[{s}, p. {a}]" if a == b else f"[{s}, p. {a}-{b}]"
            if tag not in seen:
                seen.append(tag)
        print("\nPassages retrieved: " + " ".join(seen))
    note = f" | guardrail: {result.guardrail}" if result.guardrail else ""
    print(f"({result.input_tokens} input + {result.output_tokens} output tokens, {result.seconds:.1f}s{note})", file=sys.stderr)
    return 1 if result.error else 0


if __name__ == "__main__":
    sys.exit(main())
