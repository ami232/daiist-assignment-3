"""
Assignment 3: our agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the tools of server.py over MCP and
AGENTS.md as system prompt. Guardrails (decisions in DECISIONS.md, section 12):

1. Approval: add_document runs only after the user types "y" in the terminal
   (without a terminal, e.g. under check.py or evaluate.py, it is refused).
2. Call limits: at most 3 searches and 6 model calls per question.
3. Citation check: every (doc_id, p. N) in the answer must point to a page that
   a search returned for this question, and an answer with figures must cite
   them. If not, the agent is asked once to fix its answer; if it still fails,
   the answer is blocked.

For evaluate.py:

    async with CorpusAgent() as agent:
        result = await agent.ask("question")   # AgentResult: answer, trace, tokens, ...

or `ask("question")` for a single question.
"""

from __future__ import annotations

import asyncio
import re
import sys
import time
from contextlib import AsyncExitStack
from dataclasses import dataclass, field
from pathlib import Path

from langchain.agents import create_agent
from langchain.agents.middleware import (AgentMiddleware, ModelCallLimitMiddleware,
                                         ToolCallLimitMiddleware)
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.rate_limiters import InMemoryRateLimiter
from langchain_core.tools import StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
MODEL = "gemini-3.5-flash-lite"
MAX_SEARCHES = 3
MAX_MODEL_CALLS = 6
REFUSAL = "The corpus does not cover this"   # the phrase AGENTS.md asks for
# what counts as a refusal: the model also writes "The corpus does not state / cover which ..."
REFUSAL_START = "the corpus does not"
# The free tier allows 15 requests a minute for gemini-3.5-flash-lite; stay under it. One limiter
# for the whole process, shared by every agent (evaluate.py runs several) and the judge.
RATE_LIMITER = InMemoryRateLimiter(requests_per_second=12 / 60, check_every_n_seconds=0.1, max_bucket_size=1)

# "Source: GEVO2026, pp. 18-19 | ..." in the search tool's output
_SOURCE_RE = re.compile(r"Source: ([A-Za-z0-9]+), pp?\. (\d+)(?:-(\d+))?")
# "(GEVO2026, p. 18)", "(GEVO2025, p. 17; GEVO2026, p. 21)", "GEVO2026, pp. 18-19",
# and several pages of one document: "(GEVO2026, p. 21, pp. 65-66)"
_PAGES = r"pp?\.\s*\d+(?:\s*[-–]\s*\d+)?"
_CITE_RE = re.compile(r"\b([A-Z][A-Za-z0-9]*\d{4}[A-Za-z0-9]*|[A-Z]{3,}[A-Za-z0-9]*),\s*"
                      rf"({_PAGES}(?:\s*(?:,|;|and)\s*{_PAGES})*)")
_PAGE_RE = re.compile(r"pp?\.\s*(\d+)")
# a figure: a number that is not a year (e.g. 44, 28%, 1.2, 4.2 million)
_FIGURE_RE = re.compile(r"(?<![\w.])(?!(?:19|20)\d\d\b)\d+(?:[.,]\d+)?\s*(?:%|percent|million|billion|TWh|GWh)?")


def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


@dataclass
class AgentResult:
    question: str
    answer: str
    citations: list[tuple[str, int]] = field(default_factory=list)   # (doc_id, page) cited in the answer
    retrieved: list[tuple[str, int, int]] = field(default_factory=list)  # (doc_id, page, page_end) returned by search
    trace: list[dict] = field(default_factory=list)  # every tool call: tool, args, result
    guardrail: str = "passed"  # passed | fixed | blocked
    guardrail_notes: list[str] = field(default_factory=list)
    model_calls: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    seconds: float = 0.0

    @property
    def refused(self) -> bool:
        return self.answer.strip().lower().startswith(REFUSAL_START)


# ---------------------------------------------------------------------------
# Guardrail 3: citation check
# ---------------------------------------------------------------------------
def parse_citations(text: str) -> list[tuple[str, int]]:
    """(doc_id, page) for every citation in `text`; a page range gives its first page."""
    return [(m.group(1), int(p)) for m in _CITE_RE.finditer(text) for p in _PAGE_RE.findall(m.group(2))]


def retrieved_pages(trace: list[dict]) -> list[tuple[str, int, int]]:
    out = []
    for call in trace:
        if call["tool"] == "search":
            for m in _SOURCE_RE.finditer(call["result"]):
                start = int(m.group(2))
                out.append((m.group(1), start, int(m.group(3) or start)))
    return out


def check_citations(answer: str, trace: list[dict]) -> list[str]:
    """Problems with the answer's citations (empty list = the answer passes)."""
    pages = retrieved_pages(trace)
    problems = []
    for doc, page in parse_citations(answer):
        if not any(d == doc and p <= page <= e for d, p, e in pages):
            problems.append(f"({doc}, p. {page}) was not returned by any search for this question")
    if not parse_citations(answer) and _FIGURE_RE.search(answer) and REFUSAL_START not in answer.lower():
        problems.append("the answer gives figures but cites no source")
    return problems


# ---------------------------------------------------------------------------
# Guardrail 1: approval before add_document
# ---------------------------------------------------------------------------
def terminal_approval(tool: str, args: dict) -> bool:
    """Ask in the terminal; refuse when there is no one to ask."""
    if not sys.stdin.isatty():
        log(f"[approval] {tool}({args}) refused: no terminal to ask for approval.")
        return False
    log(f"\n[approval] The agent wants to run {tool} with {args}.")
    log("  This adds the file to the shared index and spends embedding quota.")
    try:
        reply = input("  Approve? [y/N] ")
    except EOFError:
        reply = ""
    return reply.strip().lower() in ("y", "yes")


class ApprovalMiddleware(AgentMiddleware):
    """Holds every call to the listed tools until `approve(tool, args)` says yes."""

    # (`tools` and other attribute names are reserved by AgentMiddleware)
    def __init__(self, guarded: tuple[str, ...] = ("add_document",), approver=terminal_approval):
        super().__init__()
        self.guarded = guarded
        self.approver = approver

    def _denied(self, request) -> ToolMessage | None:
        call = request.tool_call
        if call["name"] in self.guarded and not self.approver(call["name"], call["args"]):
            return ToolMessage(
                content=f"The user did not approve {call['name']}. Nothing was changed. "
                        "Tell the user the document was not added.",
                tool_call_id=call["id"], name=call["name"], status="error")
        return None

    def wrap_tool_call(self, request, handler):
        return self._denied(request) or handler(request)

    async def awrap_tool_call(self, request, handler):
        return self._denied(request) or await handler(request)


# ---------------------------------------------------------------------------
# The agent
# ---------------------------------------------------------------------------
class CorpusAgent:
    """Starts server.py over MCP (stdio) once and answers any number of questions."""

    def __init__(self, model: str = MODEL, approve=terminal_approval):
        self.model_name = model
        self.approve = approve
        self._trace: list[dict] = []

    async def __aenter__(self) -> "CorpusAgent":
        self._stack = AsyncExitStack()
        try:
            await self._start()
        except BaseException:
            await self._stack.aclose()  # stop server.py instead of leaving it hanging
            raise
        return self

    async def _start(self) -> None:
        params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT))
        read, write = await self._stack.enter_async_context(stdio_client(params))
        self.session = await self._stack.enter_async_context(ClientSession(read, write))
        await self.session.initialize()
        mcp_tools = (await self.session.list_tools()).tools
        tools = [self._wrap(t) for t in mcp_tools]
        model = ChatGoogleGenerativeAI(model=self.model_name, google_api_key=load_api_key(), max_retries=6,
                                       rate_limiter=RATE_LIMITER)
        self.graph = create_agent(
            model,
            tools,
            system_prompt=(ROOT / "AGENTS.md").read_text(encoding="utf-8"),
            middleware=[
                ApprovalMiddleware(approver=self.approve),
                ToolCallLimitMiddleware(tool_name="search", run_limit=MAX_SEARCHES, exit_behavior="continue"),
                ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS, exit_behavior="end"),
            ],
        )

    async def __aexit__(self, *exc) -> None:
        await self._stack.aclose()

    def _wrap(self, tool) -> StructuredTool:
        """A LangChain tool that calls the MCP tool and records the call in the trace."""
        async def call(**args):
            result = await self.session.call_tool(tool.name, args)
            text = "\n".join(getattr(c, "text", "") for c in result.content).strip()
            if result.is_error:
                text = f"Error: {text}"
            self._trace.append({"tool": tool.name, "args": args, "result": text})
            log(f"[tool] {tool.name}({args}) -> " + (", ".join(
                f"{d} p.{p}" for d, p, _ in retrieved_pages(self._trace[-1:])) or text[:120]))
            return text

        return StructuredTool(name=tool.name, description=tool.description or "",
                              args_schema=tool.input_schema, coroutine=call)

    async def _run(self, messages: list) -> tuple[list, str]:
        state = await self.graph.ainvoke({"messages": messages})
        msgs = state["messages"]
        final = next((m for m in reversed(msgs) if isinstance(m, AIMessage) and not m.tool_calls), None)
        return msgs, _text(final) if final else ""

    async def ask(self, question: str) -> AgentResult:
        self._trace = []
        started = time.time()
        msgs, answer = await self._run([HumanMessage(question)])
        result = AgentResult(question=question, answer=answer)

        problems = check_citations(answer, self._trace)
        if problems:  # one chance to fix the answer
            log("[guardrail] " + "; ".join(problems) + " -> asking the agent to fix it")
            result.guardrail_notes += problems
            fix = HumanMessage(
                "Citation check failed: " + "; ".join(problems) + ". Rewrite your answer citing only "
                "pages returned by your searches, with a citation for every figure. If no passage states "
                f"a figure, remove it, or reply '{REFUSAL}.'")
            msgs, answer = await self._run(msgs + [fix])
            problems = check_citations(answer, self._trace)
            result.guardrail = "fixed"
            if problems:
                result.guardrail = "blocked"
                result.guardrail_notes += problems
                answer = ("Answer blocked by the citation check (" + "; ".join(problems) + "). "
                          "Check the sources by hand.")
        result.answer = answer
        result.citations = parse_citations(answer)
        result.retrieved = retrieved_pages(self._trace)
        result.trace = list(self._trace)
        ais = [m for m in msgs if isinstance(m, AIMessage)]
        result.model_calls = len(ais)
        result.input_tokens = sum((m.usage_metadata or {}).get("input_tokens", 0) for m in ais)
        result.output_tokens = sum((m.usage_metadata or {}).get("output_tokens", 0) for m in ais)
        result.seconds = round(time.time() - started, 1)
        return result


def _text(message: AIMessage) -> str:
    content = message.content
    if isinstance(content, list):  # Gemini may return content blocks
        content = "".join(b.get("text", "") if isinstance(b, dict) else str(b) for b in content)
    return content.strip()


def ask(question: str, approve=terminal_approval) -> AgentResult:
    async def run():
        async with CorpusAgent(approve=approve) as agent:
            return await agent.ask(question)
    return asyncio.run(run())


def format_result(r: AgentResult) -> str:
    """The answer, then each cited passage with its title and location."""
    lines = [r.answer]
    sources = {}
    for call in r.trace:
        if call["tool"] != "search":
            continue
        for block in call["result"].split("\n\n"):
            m = _SOURCE_RE.search(block)
            if m:
                header = block.split("\n", 1)[0]
                start, end = int(m.group(2)), int(m.group(3) or m.group(2))
                for doc, page in r.citations:
                    if doc == m.group(1) and start <= page <= end:
                        sources.setdefault((doc, page), header.split("] Source: ", 1)[1].rsplit(" | relevance", 1)[0])
    if sources:
        lines += ["", "Sources:"] + [f"- {s}" for s in dict.fromkeys(sources.values())]
    lines += ["", f"[{len(r.trace)} tool calls, {r.model_calls} model calls, "
                  f"{r.input_tokens + r.output_tokens} tokens, {r.seconds}s, citation check: {r.guardrail}]"]
    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit('Usage: uv run python agent.py "your question"')
    print(format_result(ask(" ".join(sys.argv[1:]))))
