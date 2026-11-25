"""
Assignment 3: the agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the tools from server.py over MCP (stdio) and AGENTS.md as the
system prompt. Guardrails:

1. Approval: add_document only runs after a human types "y". With no terminal (evaluation, CI) it is denied.
2. Call limits: at most 4 tool calls (ToolCallLimitMiddleware) and 6 model calls per question.
3. Citation check (the extra guardrail): every [citation] in the answer must match, at article level,
   a passage that search actually returned in this run, and a non-refusal answer must cite something
   (except a reply that only reports an approved add_document, which makes no legal claim).
   If not, the agent gets one chance to fix it; if it still fails, the answer is withheld and replaced
   by a refusal that names the unverified citations.

`Harness` keeps one MCP connection open for many questions; `ask(question)` returns the answer plus the
trace (tool calls, retrieved passages, citations, tokens, seconds) for evaluate.py.
"""

from __future__ import annotations

import asyncio
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware, ToolCallLimitMiddleware
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.tools import StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
SYSTEM_PROMPT = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
MODEL = "gemini-3.5-flash-lite"   # free tier: gemini-3.5-flash allows only 20 requests/day
MAX_TOOL_CALLS, MAX_MODEL_CALLS = 4, 6
REFUSAL = "The corpus does not cover this"

AGREEMENTS = ["GATT 1994", "GATT", "GATS", "TRIPS", "SPS", "DSU"]   # longest first for prefix matching
RE_BRACKET = re.compile(r"\[([^\[\]]{3,120})\]")
RE_ARTICLE = re.compile(r"^(Ad Art\.|Ad Articles|Art\.|Annex|Appendix|Preamble|para\.)\s*"
                        r"(on .*|To .*|(?<=Annex )[0-9A-Z]{1,3}\b|(?<=Appendix )[0-9]+|[0-9IVXL]+(?:\s*bis)?)?", re.I)


# --------------------------------------------------------------------------- citations

def citation_key(citation: str, extra: tuple[str, ...] = ()) -> tuple[str, str] | None:
    """'GATT Art. III:2' -> ('GATT', 'Art. III'); 'SPS Annex A, para. 3' -> ('SPS', 'Annex A'). None if not a citation.

    `extra` are names of documents added later with add_document (e.g. "WTO Annex 1A Note")."""
    c = citation.strip()
    names = sorted(set(AGREEMENTS) | set(extra), key=len, reverse=True)
    agreement = next((a for a in names if c == a or c.startswith(a + " ") or c.startswith(a + ",")), None)
    if not agreement:
        return None
    rest = c[len(agreement):].lstrip(" ,")
    if not rest:
        return (agreement, "")
    m = RE_ARTICLE.match(rest)
    if not m:
        return None
    kind, number = m.group(1), (m.group(2) or "")
    if kind.lower() == "para.":            # GATT 1994 has no articles: any paragraph of it is one unit
        return (agreement, "para")
    if number.lower().startswith(("on ", "to ")):    # named annex: drop ", para. 1" after the name
        number = re.split(r",\s*paras?\.", number)[0].strip()
    else:
        number = re.split(r"[:.(,\-]", number.strip())[0].strip()
    return (agreement, f"{kind} {number}".strip())


def extra_agreements(retrieved: dict) -> tuple[str, ...]:
    """Document names in retrieved citations that are not one of the six corpus agreements."""
    out = set()
    for c in retrieved:
        if citation_key(c) is None:
            out.add(re.split(r",| Art\.| Annex| Appendix| para\.", c)[0].strip())
    return tuple(out)


def cited_in(answer: str, extra: tuple[str, ...] = ()) -> list[str]:
    """All citations in square brackets; '[GATT Art. I; GATS Art. II]' counts as two."""
    out = []
    for group in RE_BRACKET.findall(answer):
        for part in re.split(r";|\s+and\s+", group):
            if citation_key(part, extra):
                out.append(part.strip())
    return out


def is_refusal(answer: str) -> bool:
    return REFUSAL.lower() in answer.lower()


# --------------------------------------------------------------------------- trace

@dataclass
class Trace:
    question: str
    answer: str = ""
    tool_calls: list[dict] = field(default_factory=list)   # {"tool", "args", "citations"}
    retrieved: dict[str, dict] = field(default_factory=dict)  # citation -> {"url", "text"}
    cited: list[str] = field(default_factory=list)
    invalid_citations: list[str] = field(default_factory=list)
    guardrail: str = ""          # "", "fixed_on_retry", "blocked", "approval_denied"
    first_draft: str = ""        # the answer the citation check rejected, if it fired
    first_draft_problems: list[str] = field(default_factory=list)
    refused: bool = False
    input_tokens: int = 0
    output_tokens: int = 0
    seconds: float = 0.0
    error: str = ""


def parse_search_result(text: str) -> dict[str, dict]:
    """Pull Citation / URL / passage text out of server.py's formatted search result."""
    out = {}
    for block in text.split("\n\n---\n\n"):
        cite = re.search(r"^\[\d+\] Citation: (.+)$", block, re.M)
        url = re.search(r"^URL: (.+)$", block, re.M)
        body = block.split("\n\n", 1)[1] if "\n\n" in block else block
        if cite:
            out[cite.group(1).strip()] = {"url": url.group(1).strip() if url else "", "text": body}
    return out


# --------------------------------------------------------------------------- harness

def terminal_approval(tool: str, args: dict) -> bool:
    if not sys.stdin.isatty():
        print(f"[approval] {tool}({args}) denied: no terminal to ask a human.", file=sys.stderr)
        return False
    reply = input(f"\nThe agent wants to run {tool}({args}). This changes the shared index. Approve? [y/N] ")
    return reply.strip().lower() in {"y", "yes"}


class Harness:
    def __init__(self, model: str = MODEL, approve=terminal_approval):
        load_api_key()
        self.model_name = model
        self.approve = approve
        self._stack = None

    async def __aenter__(self) -> "Harness":
        from contextlib import AsyncExitStack

        self._stack = AsyncExitStack()
        params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT))
        read, write = await self._stack.enter_async_context(stdio_client(params))
        self.session = await self._stack.enter_async_context(ClientSession(read, write))
        await self.session.initialize()
        self.mcp_tools = (await self.session.list_tools()).tools
        return self

    async def __aexit__(self, *exc) -> None:
        await self._stack.aclose()

    def _tools(self, trace: Trace) -> list[StructuredTool]:
        """Wrap each MCP tool as a LangChain tool that records the call in `trace`."""
        tools = []
        for t in self.mcp_tools:
            async def call(_name=t.name, **kwargs) -> str:
                if _name == "add_document" and not self.approve(_name, kwargs):
                    trace.guardrail = trace.guardrail or "approval_denied"
                    trace.tool_calls.append({"tool": _name, "args": kwargs, "citations": [], "denied": True})
                    return "The user did not approve add_document. Do not retry it; answer from search results."
                result = await self.session.call_tool(_name, kwargs)
                text = "\n".join(getattr(c, "text", "") for c in result.content)
                found = parse_search_result(text) if _name == "search" else {}
                trace.retrieved.update(found)
                trace.tool_calls.append({"tool": _name, "args": kwargs, "citations": list(found)})
                return text
            tools.append(StructuredTool(name=t.name, description=t.description or "", args_schema=t.input_schema,
                                        coroutine=call))
        return tools

    def _agent(self, trace: Trace):
        llm = ChatGoogleGenerativeAI(model=self.model_name, temperature=0, max_retries=6)
        return create_agent(
            llm, tools=self._tools(trace), system_prompt=SYSTEM_PROMPT,
            middleware=[ToolCallLimitMiddleware(run_limit=MAX_TOOL_CALLS),
                        ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS, exit_behavior="end")],
        )

    async def _run(self, agent, messages: list, trace: Trace) -> tuple[str, list]:
        state = await agent.ainvoke({"messages": messages})
        msgs = state["messages"]
        for m in msgs[len(messages):]:
            if isinstance(m, AIMessage) and m.usage_metadata:
                trace.input_tokens += m.usage_metadata.get("input_tokens", 0)
                trace.output_tokens += m.usage_metadata.get("output_tokens", 0)
        final = next((m for m in reversed(msgs) if isinstance(m, AIMessage) and not m.tool_calls), None)
        return (final.text.strip() if final else ""), msgs

    def _check(self, answer: str, trace: Trace) -> list[str]:
        """Citations in the answer that no search in this run returned (article level)."""
        extra = extra_agreements(trace.retrieved)
        allowed = {citation_key(c, extra) for c in trace.retrieved}
        cited = cited_in(answer, extra)
        trace.cited = cited
        bad = [c for c in cited if citation_key(c, extra) not in allowed]
        searched = any(c["tool"] == "search" for c in trace.tool_calls)
        added = any(c["tool"] == "add_document" and not c.get("denied") for c in trace.tool_calls)
        if not cited and not is_refusal(answer) and not (added and not searched):
            bad.append("(no citation)")   # a reply that only reports an approved add_document needs none
        return bad

    async def ask(self, question: str) -> Trace:
        trace = Trace(question=question)
        start = time.time()
        try:
            agent = self._agent(trace)
            answer, msgs = await self._run(agent, [HumanMessage(question)], trace)
            bad = self._check(answer, trace)
            if bad:   # guardrail: one chance to fix
                trace.first_draft, trace.first_draft_problems = answer, bad
                retrieved = ", ".join(trace.retrieved) or "none"
                fix = HumanMessage(
                    f"Your answer cites {', '.join(bad)}, which did not come from your search results "
                    f"(retrieved: {retrieved}). Rewrite the answer citing only retrieved passages, search again if "
                    f"you need another provision, or reply '{REFUSAL}' if the passages do not answer the question.")
                answer, _ = await self._run(agent, msgs + [fix], trace)
                bad = self._check(answer, trace)
                trace.guardrail = "blocked" if bad else "fixed_on_retry"
                if bad:
                    trace.invalid_citations = bad
                    answer = (f"{REFUSAL} with verified citations: the draft answer relied on "
                              f"{', '.join(bad)}, which the search results did not support.")
            trace.answer = answer
            trace.refused = is_refusal(answer)
        except Exception as error:  # noqa: BLE001 - surface the failure in the trace, keep evaluating
            trace.error = f"{type(error).__name__}: {error}"
            trace.answer = trace.answer or f"[error] {trace.error}"
        trace.seconds = round(time.time() - start, 2)
        return trace


def render(trace: Trace) -> str:
    lines = [trace.answer.strip(), ""]
    exact = [c for c in trace.retrieved if c in trace.cited]
    extra = extra_agreements(trace.retrieved)
    sources = exact or [c for c in trace.retrieved
                        if citation_key(c, extra) in {citation_key(x, extra) for x in trace.cited}]
    if sources:
        lines.append("Sources:")
        lines += [f"  - {c}: {trace.retrieved[c]['url']}" for c in sources]
    if trace.guardrail:
        lines.append(f"\n[guardrail: {trace.guardrail}]")
    lines.append(f"[{len(trace.tool_calls)} tool calls, {trace.input_tokens + trace.output_tokens} tokens, {trace.seconds}s]")
    return "\n".join(lines)


async def ask_many(questions: list[str], **kw) -> list[Trace]:
    async with Harness(**kw) as h:
        return [await h.ask(q) for q in questions]


def ask(question: str, **kw) -> Trace:
    return asyncio.run(ask_many([question], **kw))[0]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit('usage: python agent.py "your question"')
    t = ask(" ".join(sys.argv[1:]))
    print(render(t))
    if t.error:
        sys.exit(1)
