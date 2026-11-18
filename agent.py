"""
Assignment 3: the agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the tools of server.py over MCP (stdio), AGENTS.md as
system prompt, and these guardrails:

  1. Human approval before add_document runs (HumanInTheLoopMiddleware): approve/reject.
  2. Call limits: at most 4 tool calls and 8 model calls per question.
  3. Citation grounding (our own guardrail): every citation in the final answer must point to a
     passage the search tool actually returned in this run, and a non-refusal answer must cite
     something. If not, the model gets one chance to repair the answer; if it still fails, the
     answer is replaced by the refusal. evaluate.py records every time it fires.

evaluate.py imports CorpusAgent: `async with CorpusAgent() as a: result = await a.ask(q)`.
"""

from __future__ import annotations

import asyncio
import os
import re
import sys
import time
import uuid
from pathlib import Path

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
MODEL = os.environ.get("GEMINI_MODEL", "gemini-flash-lite-latest")
REFUSAL = "The corpus does not cover this."
MAX_TOOL_CALLS, MAX_MODEL_CALLS = 4, 8

CITE_IN_ANSWER = re.compile(r"\[([a-z][a-z0-9_]*)\s+p\.\s?(\d+)(?:\s*[-–]\s*(\d+))?\]")
CITE_IN_RESULT = re.compile(r"cite as \[([a-z][a-z0-9_]*) p\.(\d+)(?:-(\d+))?\]")


def is_refusal(answer: str) -> bool:
    return "corpus does not cover" in answer.lower()


def citations_in(answer: str) -> list[tuple[str, int, int]]:
    out = []
    for doc, p0, p1 in CITE_IN_ANSWER.findall(answer):
        out.append((doc, int(p0), int(p1 or p0)))
    return out


def retrieved_passages(tool_outputs: list[str]) -> list[tuple[str, int, int]]:
    out = []
    for text in tool_outputs:
        for doc, p0, p1 in CITE_IN_RESULT.findall(text):
            out.append((doc, int(p0), int(p1 or p0)))
    return out


def citation_is_valid(cite: tuple[str, int, int], retrieved: list[tuple[str, int, int]]) -> bool:
    """A cited page range must overlap a passage that was retrieved for this question."""
    doc, p0, p1 = cite
    return any(d == doc and p0 <= r1 and r0 <= p1 for d, r0, r1 in retrieved)


def check_grounding(answer: str, tool_outputs: list[str]) -> str | None:
    """None if the answer passes the citation guardrail, else the reason it fails."""
    cites = citations_in(answer)
    retrieved = retrieved_passages(tool_outputs)
    if is_refusal(answer):
        bad = [c for c in cites if not citation_is_valid(c, retrieved)]
        return f"it cites passages that were not retrieved: {bad}" if bad else None
    if not retrieved:
        return "it answers without having retrieved any passage"
    if not cites:
        return "it makes claims without any citation"
    bad = [c for c in cites if not citation_is_valid(c, retrieved)]
    if bad:
        return f"it cites passages that were not retrieved: {bad}"
    return None


def _text(message) -> str:
    content = getattr(message, "content", message)
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "".join(part.get("text", "") if isinstance(part, dict) else str(part) for part in content)
    return str(content)


async def mcp_tools_as_langchain(session) -> list:
    """Wrap each tool the MCP server lists as a LangChain tool that calls it over the session.
    (langchain-mcp-adapters does not support the mcp 2.x SDK this course uses.)"""
    from langchain_core.tools import StructuredTool

    def make(tool):
        async def call(**kwargs) -> str:
            result = await session.call_tool(tool.name, kwargs)
            text = "\n".join(getattr(c, "text", "") for c in result.content)
            if getattr(result, "is_error", False) or getattr(result, "isError", False):
                return f"Tool error: {text}"
            return text

        return StructuredTool.from_function(
            coroutine=call, name=tool.name, description=tool.description or "", args_schema=tool.input_schema,
        )

    return [make(t) for t in (await session.list_tools()).tools]


def console_approval(name: str, args: dict) -> bool:
    """Ask the person at the terminal. Without a terminal, only APPROVE_ADD_DOCUMENT=yes approves."""
    if not sys.stdin.isatty():
        ok = os.environ.get("APPROVE_ADD_DOCUMENT", "").lower() == "yes"
        print(f"[approval] {name}({args}) -> {'approved by APPROVE_ADD_DOCUMENT' if ok else 'rejected (no terminal)'}",
              file=sys.stderr)
        return ok
    print(f"\nThe agent wants to run {name} with {args}.", file=sys.stderr)
    return input("Approve? [y/N] ").strip().lower() in ("y", "yes")


class CorpusAgent:
    """One MCP connection to server.py and one LangChain agent, reused across questions."""

    def __init__(self, corpus_only: bool = False, approve=console_approval, model: str = MODEL):
        self.corpus_only = corpus_only
        self.approve = approve
        self.model = model

    async def __aenter__(self):
        from langchain.agents import create_agent
        from langchain.agents.middleware import (
            HumanInTheLoopMiddleware,
            ModelCallLimitMiddleware,
            ToolCallLimitMiddleware,
        )
        from langchain_google_genai import ChatGoogleGenerativeAI
        from langgraph.checkpoint.memory import InMemorySaver
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client

        load_api_key()
        env = {**os.environ, "CORPUS_ONLY": "1" if self.corpus_only else "0"}
        params = StdioServerParameters(command=sys.executable, args=[str(ROOT / "server.py")], cwd=str(ROOT), env=env)
        self._stdio = stdio_client(params)
        read, write = await self._stdio.__aenter__()
        self._session = ClientSession(read, write)
        await self._session.__aenter__()
        await self._session.initialize()
        tools = await mcp_tools_as_langchain(self._session)

        llm = ChatGoogleGenerativeAI(model=self.model, temperature=0, max_retries=6)
        self.agent = create_agent(
            llm,
            tools,
            system_prompt=(ROOT / "AGENTS.md").read_text(encoding="utf-8"),
            middleware=[
                HumanInTheLoopMiddleware(interrupt_on={"add_document": {"allowed_decisions": ["approve", "reject"]}}),
                ToolCallLimitMiddleware(run_limit=MAX_TOOL_CALLS, exit_behavior="continue"),
                ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS, exit_behavior="end"),
            ],
            checkpointer=InMemorySaver(),
        )
        return self

    async def __aexit__(self, *exc):
        await self._session.__aexit__(*exc)
        await self._stdio.__aexit__(*exc)

    async def _run(self, payload, config) -> dict:
        from langgraph.types import Command

        result = await self.agent.ainvoke(payload, config)
        while result.get("__interrupt__"):
            request = result["__interrupt__"][0].value
            decisions = []
            for action in request["action_requests"]:
                ok = self.approve(action["name"], action["args"])
                self.events.append({"event": "approval", "tool": action["name"], "args": action["args"], "approved": ok})
                decisions.append({"type": "approve"} if ok else
                                 {"type": "reject", "message": "The human reviewer did not approve this action."})
            result = await self.agent.ainvoke(Command(resume={"decisions": decisions}), config)
        return result

    async def ask(self, question: str) -> dict:
        """Answer one question. Returns answer, tool trace, retrieved text, tokens, seconds, guardrail events."""
        from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

        started = time.time()
        self.events: list[dict] = []
        config = {"configurable": {"thread_id": str(uuid.uuid4())}}
        result = await self._run({"messages": [HumanMessage(question)]}, config)

        def collect(messages):
            outputs = [_text(m) for m in messages if isinstance(m, ToolMessage) and "cite as [" in _text(m)]
            final = next((_text(m) for m in reversed(messages) if isinstance(m, AIMessage) and _text(m).strip()), "")
            return outputs, final

        outputs, answer = collect(result["messages"])
        asked_to_add = any(getattr(m, "tool_calls", None) and any(c["name"] == "add_document" for c in m.tool_calls)
                           for m in result["messages"])
        # Requests to add a document are answered with the tool's report, not with citations.
        problem = None if (asked_to_add and not outputs) else check_grounding(answer, outputs)
        if problem:
            # Guardrail: one repair attempt, then refuse.
            self.events.append({"event": "citation_guardrail", "stage": "first_answer", "reason": problem})
            feedback = (
                f"GUARDRAIL: your answer was rejected because {problem}. Rewrite it using only the passages "
                f"returned by search, citing each claim with a tag exactly as shown after 'cite as'. "
                f"If they do not contain the answer, reply exactly: {REFUSAL}"
            )
            result = await self._run({"messages": [HumanMessage(feedback)]}, config)
            outputs, answer = collect(result["messages"])
            problem = check_grounding(answer, outputs)
            if problem:
                self.events.append({"event": "citation_guardrail", "stage": "after_repair", "reason": problem})
                answer = f"{REFUSAL} (An answer was drafted but could not be grounded in the retrieved passages.)"

        messages = result["messages"]
        trace = []
        for m in messages:
            if isinstance(m, AIMessage):
                for call in m.tool_calls or []:
                    trace.append({"tool": call["name"], "args": call["args"]})
        usage = {"input_tokens": 0, "output_tokens": 0}
        model_calls = 0
        for m in messages:
            if isinstance(m, AIMessage):
                model_calls += 1
                u = getattr(m, "usage_metadata", None) or {}
                usage["input_tokens"] += u.get("input_tokens", 0)
                usage["output_tokens"] += u.get("output_tokens", 0)
        return {
            "question": question,
            "answer": answer.strip(),
            "refused": is_refusal(answer),
            "citations": ["%s p.%d" % (d, p0) if p0 == p1 else "%s p.%d-%d" % (d, p0, p1) for d, p0, p1 in citations_in(answer)],
            "trace": trace,
            "retrieved": outputs,
            "retrieved_passages": ["%s p.%d-%d" % r for r in retrieved_passages(outputs)],
            "events": self.events,
            "model_calls": model_calls,
            **usage,
            "seconds": round(time.time() - started, 2),
            "model": self.model,
        }


async def ask_once(question: str) -> dict:
    async with CorpusAgent() as agent:
        return await agent.ask(question)


def print_result(r: dict) -> None:
    import rag

    print(r["answer"])
    registry = rag.load_registry()
    if r["citations"]:
        print("\nSources:")
        for cite in dict.fromkeys(r["citations"]):
            doc = cite.split()[0]
            info = registry.get(doc, {})
            print(f"  [{cite}] {info.get('title', doc)} ({info.get('url', '')})")
    for e in r["events"]:
        print(f"[guardrail] {e}", file=sys.stderr)
    print(f"\n[{r['model_calls']} model calls, {len(r['trace'])} tool calls, "
          f"{r['input_tokens']}+{r['output_tokens']} tokens, {r['seconds']} s]", file=sys.stderr)


if __name__ == "__main__":
    # Windows consoles (cp1252) can't print characters like "≥" or "χ" from the papers: replace them instead of crashing.
    for _stream in (sys.stdout, sys.stderr):
        try:
            _stream.reconfigure(errors="replace")
        except AttributeError:
            pass
    if len(sys.argv) < 2:
        sys.exit('usage: python agent.py "your question"')
    print_result(asyncio.run(ask_once(" ".join(sys.argv[1:]))))
