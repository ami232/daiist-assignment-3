"""
Assignment 3: the agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the tools from server.py over MCP and
AGENTS.md as the system prompt. Guardrails:

1. Approval: add_document never runs without a human "yes" (HumanInTheLoopMiddleware).
   In a non-interactive run (evaluation, check.py) the call is rejected.
2. Call limits: at most MAX_TOOL_CALLS tool calls and MAX_MODEL_CALLS model calls per question.
3. Citation guard (extra guardrail): every citation in the answer must match a passage
   that search actually returned in this run. An answer with an invented citation, or a
   substantive answer with no citation, is replaced by a refusal.

`Harness` keeps one MCP session open for many questions (evaluate.py uses it);
`run_agent(question)` is the one-shot version. Both return the answer and the trace.
"""

from __future__ import annotations

import asyncio
import contextlib
import os
import re
import sys
import time
import uuid
from pathlib import Path

from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware, ModelCallLimitMiddleware, ToolCallLimitMiddleware
from langchain_core.tools import StructuredTool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
AGENT_MODEL = os.environ.get("AGENT_MODEL", "gemini-3.5-flash-lite")
MAX_TOOL_CALLS = 6
MAX_MODEL_CALLS = 10
# DECISION (Jesús): "block" replaces answers that fail the citation check with a refusal;
# "flag" keeps them but marks them in the trace.
CITATION_GUARD = os.environ.get("CITATION_GUARD", "block")

REFUSAL_MARKER = "El corpus no cubre esta pregunta"
BRACKET_RE = re.compile(r"\[([^\[\]]+)\]")
DOC_LOC_RE = re.compile(r"^\s*([A-Z0-9][A-Z0-9\-]+),\s*(.+?)\s*$")
LOCATION_WORDS = ("Artículo", "Pregunta", "Disposición", "Preámbulo", "Considerandos", "Página", "Introducción", "Inicio")


def parse_citations(answer: str) -> list[tuple[str, str]]:
    """(doc_id, location) for every citation in the answer.

    Handles one passage per bracket, [RD1066-2007, Artículo 23], and the compound
    forms models also write: [RD571-2023, Preámbulo; Artículo 14] or
    [LEY19-2003, Artículo 7 bis; RD571-2023, Artículo 11].
    """
    found = []
    for content in BRACKET_RE.findall(answer):
        doc = None
        for part in content.split(";"):
            match = DOC_LOC_RE.match(part)
            if match:
                doc = match.group(1)
                found.append((doc, match.group(2)))
            elif doc and part.strip().startswith(LOCATION_WORDS):
                found.append((doc, part.strip()))
    return found
RESULT_CITE_RE = re.compile(r"cite as \[([^,\]]+),\s*([^\]]+)\]")


def system_prompt() -> str:
    return (ROOT / "AGENTS.md").read_text(encoding="utf-8")


def is_refusal(answer: str) -> bool:
    return REFUSAL_MARKER.lower() in answer.lower()


def retrieved_citations(trace: list[dict]) -> set[tuple[str, str]]:
    """(doc_id, location) of every passage search returned in this run."""
    found = set()
    for step in trace:
        if step["tool"] == "search":
            found |= {(d.strip(), loc.strip()) for d, loc in RESULT_CITE_RE.findall(step["output"])}
    return found


def check_citations(answer: str, trace: list[dict]) -> dict:
    """Which citations in the answer point to a passage that was actually retrieved.

    A citation may be more specific than the chunk ('Artículo 23.2' for a chunk
    'Artículo 23'), so a cited location only has to start with a retrieved one.
    """
    retrieved = retrieved_citations(trace)
    cited = parse_citations(answer)

    def ok(doc_id: str, loc: str) -> bool:
        return any(doc_id == d and (loc == l or loc.startswith(l + " ") or loc.startswith(l + "."))
                   for d, l in retrieved)

    valid = [c for c in cited if ok(*c)]
    invalid = [c for c in cited if not ok(*c)]
    return {"cited": cited, "valid": valid, "invalid": invalid, "retrieved": sorted(retrieved)}


def citation_guard(answer: str, trace: list[dict], approvals: list[dict] | None = None) -> tuple[str, dict]:
    """The extra guardrail. Returns the (possibly replaced) answer and what it found.

    It only checks research answers: a reply about an add_document request that
    never searched is a confirmation, not a claim about the rules.
    """
    report = check_citations(answer, trace)
    report["fired"] = False
    searched = any(step["tool"] == "search" for step in trace)
    add_request = bool(approvals) or any(step["tool"] == "add_document" for step in trace)
    if is_refusal(answer) or (not searched and not report["cited"] and add_request):
        return answer, report
    reason = None
    if report["invalid"]:
        reason = "cita pasajes que la búsqueda no devolvió: " + ", ".join(f"[{d}, {l}]" for d, l in report["invalid"])
    elif not report["cited"]:
        reason = "no incluye ninguna cita"
    if reason:
        report["fired"], report["reason"] = True, reason
        if CITATION_GUARD == "block":
            answer = (
                f"{REFUSAL_MARKER} con citas verificables: la respuesta generada {reason}. "
                "Revisa la normativa directamente o consulta con el abogado del deal."
            )
    return answer, report


def _text(content) -> str:
    if isinstance(content, str):
        return content
    return "".join(part.get("text", "") if isinstance(part, dict) else str(part) for part in content)


def ask_approval(requests: list[dict]) -> list[dict]:
    """Show each gated call and ask for a yes in the terminal. No terminal means no."""
    decisions = []
    for req in requests:
        print(f"\nThe agent wants to run {req['name']} with {req['args']}.", file=sys.stderr)
        if not sys.stdin.isatty():
            print("Non-interactive run: rejected.", file=sys.stderr)
            decisions.append({"type": "reject", "message": "Rejected: no human available to approve."})
            continue
        answer = input("Approve? [y/N] ").strip().lower()
        decisions.append({"type": "approve"} if answer in ("y", "yes", "s", "si", "sí")
                         else {"type": "reject", "message": "The user did not approve adding this document."})
    return decisions


class Harness:
    """One MCP session to server.py and one LangChain agent, reused across questions."""

    def __init__(self, approve=ask_approval, model: str = AGENT_MODEL):
        self.approve = approve
        self.model_name = model
        self.trace: list[dict] = []

    async def __aenter__(self) -> "Harness":
        params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT),
                                       env=dict(os.environ))
        self._stack = contextlib.AsyncExitStack()
        try:
            read, write = await self._stack.enter_async_context(stdio_client(params))
            self.session = await self._stack.enter_async_context(ClientSession(read, write))
            await self.session.initialize()
            await self._build_agent()
        except BaseException:
            await self._stack.aclose()  # never leave the server process hanging
            raise
        return self

    async def _build_agent(self) -> None:
        def wrap(tool):
            async def call(**kwargs):
                started = time.time()
                result = await self.session.call_tool(tool.name, kwargs)
                text = "\n".join(getattr(c, "text", "") for c in result.content)
                self.trace.append({"tool": tool.name, "args": kwargs, "output": text,
                                   "seconds": round(time.time() - started, 2)})
                return text

            return StructuredTool.from_function(coroutine=call, name=tool.name,
                                                description=tool.description, args_schema=tool.input_schema)

        tools = [wrap(t) for t in (await self.session.list_tools()).tools]
        if not isinstance(self.model_name, str):  # a ready chat model (offline tests)
            model = self.model_name
        else:
            from langchain_google_genai import ChatGoogleGenerativeAI

            load_api_key()
            model = ChatGoogleGenerativeAI(model=self.model_name, temperature=0, max_retries=6)
        self.agent = create_agent(
            model,
            tools=tools,
            system_prompt=system_prompt(),
            middleware=[
                HumanInTheLoopMiddleware(interrupt_on={"add_document": {"allowed_decisions": ["approve", "reject"]}}),
                ToolCallLimitMiddleware(run_limit=MAX_TOOL_CALLS, exit_behavior="continue"),
                ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS, exit_behavior="end"),
            ],
            checkpointer=InMemorySaver(),
        )

    async def __aexit__(self, *exc) -> None:
        await self._stack.aclose()

    async def ask(self, question: str) -> dict:
        self.trace = []
        config = {"configurable": {"thread_id": str(uuid.uuid4())}}
        started = time.time()
        payload = {"messages": [{"role": "user", "content": question}]}
        approvals = []
        while True:
            result = await self.agent.ainvoke(payload, config, version="v2")
            interrupts = getattr(result, "interrupts", None) or []
            if not interrupts:
                break
            requests = interrupts[0].value["action_requests"]
            decisions = self.approve(requests)
            approvals.extend({"tool": r["name"], "args": r["args"], "decision": d["type"]}
                             for r, d in zip(requests, decisions))
            payload = Command(resume={"decisions": decisions})
        state = getattr(result, "value", result)
        messages = state["messages"]
        raw = _text(messages[-1].content).strip() if messages else ""
        answer, guard = citation_guard(raw, self.trace, approvals)
        usage = {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}
        model_calls = 0
        for m in messages:
            meta = getattr(m, "usage_metadata", None)
            if meta:
                model_calls += 1
                for k in usage:
                    usage[k] += meta.get(k, 0) or 0
        return {
            "question": question,
            "answer": answer,
            "raw_answer": raw,
            "refusal": is_refusal(answer),
            "citations": guard,
            "guard_fired": guard["fired"],
            "trace": self.trace,
            "approvals": approvals,
            "model_calls": model_calls,
            "tool_calls": len(self.trace),
            "usage": usage,
            "seconds": round(time.time() - started, 2),
            "model": self.model_name if isinstance(self.model_name, str) else type(self.model_name).__name__,
        }


def run_agent(question: str, approve=ask_approval) -> dict:
    async def go():
        async with Harness(approve=approve) as harness:
            return await harness.ask(question)

    return asyncio.run(go())


def sources_block(result: dict) -> str:
    """Human-readable list of the sources the answer cites."""
    import rag

    titles = {}
    try:
        titles = {k: v.get("title", k) for k, v in rag.load_registry().items()}
    except Exception:  # noqa: BLE001 - the list is a convenience
        pass
    lines = [f"- [{d}, {loc}] {titles.get(d, '')}".rstrip() for d, loc in dict.fromkeys(result["citations"]["valid"])]
    return "Fuentes:\n" + "\n".join(lines) if lines else ""


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit('Usage: python agent.py "your question"')
    out = run_agent(" ".join(sys.argv[1:]))
    print(out["answer"])
    block = sources_block(out)
    if block:
        print("\n" + block)
    if out["guard_fired"]:
        print(f"\n[citation guard] {out['citations']['reason']}", file=sys.stderr)
    print(
        f"\n[{out['tool_calls']} tool calls, {out['model_calls']} model calls, "
        f"{out['usage']['total_tokens']} tokens, {out['seconds']}s]",
        file=sys.stderr,
    )
