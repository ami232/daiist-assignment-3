"""
Assignment 3: the agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the tools of server.py over MCP and
AGENTS.md as the system prompt.

Safeguards
- Approval: add_document runs only if an approver says yes. On the command
  line that is you, at a y/N prompt; without a terminal (check.py,
  evaluate.py) the default is no.
- Call limits: at most 6 model calls and 4 tool calls per run, so a confused
  agent cannot loop and burn the free quota.
- Citation guardrail (the extra one): after the agent answers, code checks
  that every cited id was returned by a search in this run and that a
  non-refusal cites at least one passage. If not, the agent gets one chance
  to fix it; if it still fails, the answer is replaced by a refusal. A made-up
  figure with a made-up citation is the failure analysts can't afford.

evaluate.py uses `CorpusAgent` (one server for many questions) and `answer()`.
"""

from __future__ import annotations

import asyncio
import re
import sys
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

from pydantic import Field, create_model

import index
from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
SYSTEM_PROMPT = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
MODEL = index.setting("GEMINI_MODEL", "gemini-2.5-flash")
MODEL_CALL_LIMIT = 6
TOOL_CALL_LIMIT = 4

CITATION = re.compile(r"\b([A-Za-z0-9_]+_(?:10K|10Q)_[A-Za-z0-9_]+#[a-z]+\d{3}|[A-Za-z0-9_]+#(?:mdna|rf|document)\d{3})\b")
PASSAGE_HEADER = re.compile(r"^\[([A-Za-z0-9_]+#[a-z]+\d{3})\] (.+)$", re.M)
REFUSAL = re.compile(
    r"do(?:es)? not cover|not covered|isn't covered|is not covered|not in the (?:indexed )?(?:filings|corpus|documents)"
    r"|(?:filings|corpus|documents|passages) do(?:es)? not (?:contain|include|provide|mention|disclose|say)"
    r"|cannot (?:find|answer)|can't (?:find|answer)|no information|won't guess", re.I)
REFUSAL_TEXT = ("The indexed filings do not cover this with a passage I can cite, so I won't guess. "
                "(Citation guardrail: the agent's answer cited passages it never retrieved, or none at all.)")


def is_refusal(text: str) -> bool:
    return bool(REFUSAL.search(text))


@dataclass
class Result:
    question: str
    answer: str
    citations: list[str]
    sources: dict[str, str]          # cited id -> where it is
    trace: list[dict] = field(default_factory=list)   # every tool call: name, args, ids, output
    retrieved: list[str] = field(default_factory=list)
    refused: bool = False
    guardrail: str = "pass"          # pass | repaired | blocked
    drafts: list[str] = field(default_factory=list)   # the model's answers before the guardrail
    model_calls: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    seconds: float = 0.0
    error: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


def deny(path: str) -> bool:
    return False


def ask_in_terminal(path: str) -> bool:
    """y/N prompt when a person is at the terminal; otherwise refuse."""
    if not sys.stdin.isatty():
        print(f"[approval] add_document({path!r}) needs approval, and nobody is at a terminal: denied.",
              file=sys.stderr)
        return False
    reply = input(f"\nThe agent wants to add {path!r} to the corpus. Allow? [y/N] ").strip().lower()
    return reply in {"y", "yes"}


class CorpusAgent:
    """One MCP connection to server.py, reused for many questions."""

    def __init__(self, model: str = MODEL):
        self.model_name = model
        self._trace: list[dict] = []
        self.approver = deny

    async def __aenter__(self) -> "CorpusAgent":
        from contextlib import AsyncExitStack
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client

        self.agent = None
        self._stack = AsyncExitStack()
        try:
            self.agent_model = self._model()  # fails fast (no key) before the server starts
            params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT))
            read, write = await self._stack.enter_async_context(stdio_client(params))
            self.session = await self._stack.enter_async_context(ClientSession(read, write))
            await self.session.initialize()
            mcp_tools = (await self.session.list_tools()).tools
            self.tools = [self._wrap(t) for t in mcp_tools]
            self.agent = self._build_agent()
        except BaseException:
            await self._stack.aclose()
            raise
        return self

    async def __aexit__(self, *exc) -> None:
        await self._stack.aclose()

    def _wrap(self, tool):
        """An MCP tool as a LangChain tool that records every call in the trace."""
        from langchain_core.tools import StructuredTool

        schema_json = getattr(tool, "input_schema", None) or getattr(tool, "inputSchema", None) or {}
        props = schema_json.get("properties", {})
        schema = create_model(
            f"{tool.name}_args",
            **{name: (str, Field(description=spec.get("description", name))) for name, spec in props.items()})

        async def call(**kwargs) -> str:
            entry = {"tool": tool.name, "args": kwargs, "ids": [], "output": ""}
            self._trace.append(entry)
            if tool.name == "add_document":
                entry["approved"] = bool(self.approver(kwargs.get("path", "")))
                if not entry["approved"]:
                    entry["output"] = ("The user did not approve adding this document, so it was not added. "
                                       "Do not try again; tell the user.")
                    return entry["output"]
            result = await self.session.call_tool(tool.name, kwargs)
            text = "\n".join(getattr(c, "text", "") for c in result.content)
            if getattr(result, "isError", False) or getattr(result, "is_error", False):
                text = f"Tool error: {text}"
            entry["output"] = text
            entry["ids"] = [m[0] for m in PASSAGE_HEADER.findall(text)]
            return text

        return StructuredTool.from_function(coroutine=call, name=tool.name,
                                            description=tool.description or tool.name, args_schema=schema)

    def _model(self):
        from langchain_google_genai import ChatGoogleGenerativeAI
        extra = {"temperature": 0} if self.model_name.startswith("gemini-2") else {}  # 3.x: fixed sampling
        return ChatGoogleGenerativeAI(model=self.model_name, api_key=load_api_key(),
                                      max_retries=4, timeout=120, **extra)

    def _build_agent(self):
        from langchain.agents import create_agent
        from langchain.agents.middleware import ModelCallLimitMiddleware, ToolCallLimitMiddleware

        return create_agent(
            self.agent_model, self.tools, system_prompt=SYSTEM_PROMPT,
            middleware=[ModelCallLimitMiddleware(run_limit=MODEL_CALL_LIMIT, exit_behavior="end"),
                        ToolCallLimitMiddleware(run_limit=TOOL_CALL_LIMIT, exit_behavior="continue")])

    async def _run(self, messages: list) -> list:
        state = await self.agent.ainvoke({"messages": messages})
        return state["messages"]

    async def ask(self, question: str, approver=None) -> Result:
        from langchain_core.messages import AIMessage, HumanMessage

        self.approver = approver or deny
        self._trace = []
        started = time.time()
        result = Result(question=question, answer="", citations=[], sources={})
        try:
            messages = await self._run([HumanMessage(question)])
            answer = final_text(messages)
            result.drafts.append(answer)
            problem = self._citation_problem(answer)
            if problem:
                result.guardrail = "repaired"
                messages = await self._run(messages + [HumanMessage(
                    f"Guardrail: {problem} Rewrite the answer citing only passage ids that your searches "
                    f"returned, one per factual sentence, or say \"The indexed filings do not cover this.\"")])
                answer = final_text(messages)
                result.drafts.append(answer)
                if self._citation_problem(answer):
                    result.guardrail = "blocked"
                    answer = REFUSAL_TEXT
            ai = [m for m in messages if isinstance(m, AIMessage)]
            result.model_calls = len(ai)
            for m in ai:
                usage = getattr(m, "usage_metadata", None) or {}
                result.input_tokens += usage.get("input_tokens", 0)
                result.output_tokens += usage.get("output_tokens", 0)
            result.answer = answer
        except Exception as error:  # noqa: BLE001 - one bad question must not stop an evaluation
            result.error = f"{type(error).__name__}: {error}"
            result.answer = f"(agent error: {result.error})"
        result.seconds = round(time.time() - started, 2)
        result.trace = self._trace
        result.retrieved = sorted({i for t in self._trace for i in (t.get("ids") or [])})
        result.citations = list(dict.fromkeys(CITATION.findall(result.answer)))
        where = {m[0]: m[1] for t in self._trace for m in PASSAGE_HEADER.findall(t.get("output", ""))}
        result.sources = {c: where.get(c, "not returned by any search") for c in result.citations}
        result.refused = result.guardrail == "blocked" or is_refusal(result.answer)
        return result

    def _citation_problem(self, answer: str) -> str:
        cited = CITATION.findall(answer)
        returned = {i for t in self._trace for i in (t.get("ids") or [])}
        invalid = [c for c in cited if c not in returned]
        if invalid:
            return f"these cited ids were not returned by any search: {', '.join(invalid)}."
        searched = any(t["tool"] == "search" for t in self._trace)
        managed = any(t["tool"] == "add_document" for t in self._trace)
        if not cited and not is_refusal(answer) and (searched or not managed):
            # a reply about adding a document needs no citation; an answer does
            return "the answer states facts but cites no passage."
        if not answer.strip():
            return "the answer is empty."
        return ""


def final_text(messages: list) -> str:
    """Text of the last model message (Gemini may return a list of content blocks)."""
    from langchain_core.messages import AIMessage
    for m in reversed(messages):
        if isinstance(m, AIMessage):
            text = m.text if isinstance(getattr(m, "text", None), str) else ""
            if not text and isinstance(m.content, str):
                text = m.content
            if not text and isinstance(m.content, list):
                text = "".join(b.get("text", "") if isinstance(b, dict) else str(b) for b in m.content
                               if not isinstance(b, dict) or b.get("type") in (None, "text"))
            if text.strip():
                return text.strip()
    return ""


async def answer_async(question: str, approver=None) -> Result:
    async with CorpusAgent() as agent:
        return await agent.ask(question, approver)


def answer(question: str, approver=None) -> Result:
    """The answer, its citations and the tool trace, for one question."""
    return asyncio.run(answer_async(question, approver))


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit('Usage: python agent.py "your question"')
    question = " ".join(sys.argv[1:])
    result = answer(question, approver=ask_in_terminal)
    print(result.answer)
    if result.sources:
        print("\nSources:")
        for cid, where in result.sources.items():
            print(f"  [{cid}] {where}")
    searches = sum(t["tool"] == "search" for t in result.trace)
    if result.guardrail != "pass":
        for n, draft in enumerate(result.drafts, 1):
            print(f"\n[guardrail] draft {n} was: {draft[:600] or '(empty)'}", file=sys.stderr)
    print(f"\n({searches} searches, {result.model_calls} model calls, "
          f"{result.input_tokens + result.output_tokens} tokens, {result.seconds}s; guardrail: {result.guardrail})",
          file=sys.stderr)
    if result.error:
        sys.exit(1)


if __name__ == "__main__":
    main()
