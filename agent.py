"""
Assignment 3: the agent harness (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the tools of server.py over MCP and
AGENTS.md as the system prompt.

Guardrails:
  1. Approval: add_document never runs without a human "yes" (HumanInTheLoopMiddleware).
     With no terminal to ask (evaluation, check.py), it is rejected.
  2. Call limits: at most 6 tool calls and 10 model calls per question.
  3. Citation check (my extra guardrail): every [citation] in the answer must match
     a passage that search actually returned in this run. An answer with no
     citations, or with a citation to something never retrieved, is withheld and
     replaced by a refusal that points the student to Program Management.

For evaluate.py:
    async with CorpusAgent() as agent:
        result = await agent.ask("question")   # dict: answer, citations, trace, tokens, seconds...
or, for one question:  answer_question("question").
"""

from __future__ import annotations

import asyncio
import os
import re
import sys
import time
import uuid
from contextlib import AsyncExitStack
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from api_key import load_api_key  # noqa: E402

# gemini-3.5-flash timed out and the flash models were often overloaded (503) on the
# free tier; flash-lite answers in a few seconds. The fallback is used if it fails.
MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.1-flash-lite")
FALLBACK_MODEL = "gemini-3.5-flash-lite"
MODEL_TIMEOUT = 60  # seconds per model call, so a busy model fails instead of hanging
SYSTEM_PROMPT = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
TOOL_CALL_LIMIT = 6
MODEL_CALL_LIMIT = 10

REFUSAL = "I can't find this in the IE documents."
GUARDRAIL_REFUSAL = (
    f"{REFUSAL} I found related passages but could not back every part of the answer "
    "with a citation from them, so I am not giving one. Please ask Program Management "
    "through the Virtual Help Desk."
)


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


# ---------------------------------------------------------------------------
# MCP tools -> LangChain tools (one server process for the whole session)
# ---------------------------------------------------------------------------
def _mcp_text(result) -> str:
    text = "\n".join(getattr(c, "text", "") for c in result.content).strip()
    if getattr(result, "is_error", False):
        return f"ERROR: {text}"
    return text


def to_langchain_tool(session, tool):
    from langchain_core.tools import StructuredTool

    async def call(**kwargs) -> str:
        return _mcp_text(await session.call_tool(tool.name, kwargs))

    return StructuredTool.from_function(
        coroutine=call,
        name=tool.name,
        description=tool.description or tool.name,
        args_schema=tool.input_schema,
    )


# ---------------------------------------------------------------------------
# Citation guardrail
# ---------------------------------------------------------------------------
HEADER = re.compile(r"^\[\d+\] (.+?), ((?:pp?)\. [\d\-]+)(?:, (.+))?$", re.M)
CITATION = re.compile(r"\[([^\[\]]{8,})\]")


def retrieved_passages(search_outputs: list[str]) -> list[dict]:
    """(source, pages, heading) of every passage search returned in this run."""
    passages = []
    for output in search_outputs:
        for source, pages, heading in HEADER.findall(output):
            passages.append({"source": source, "pages": pages, "heading": heading or ""})
    return passages


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("“", '"').replace("”", '"').replace("’", "'")).strip().lower()


CITED_PAGES = re.compile(r"pp?\.\s*(\d+)(?:\s*-\s*(\d+))?")


def _section_key(heading: str) -> str | None:
    """'Article 42. Ordinary...' -> 'article 42'; 'III.3. PROCEDURES...' -> 'iii.3'; 'ANNEX II' -> 'annex ii'."""
    for pattern in (r"^(Article \d+)", r"^([IVX]+(?:\.\d+)+)\.", r"^([IVX]+)\.\s", r"^(ANNEX [IVX\d]+)"):
        m = re.match(pattern, heading, re.I)
        if m:
            return m.group(1).lower()
    return None


def citation_is_valid(citation: str, passages: list[dict]) -> bool:
    """Valid if it names a retrieved document AND a page, article/section or heading of
    a passage retrieved from that document. Citing "Article 42.7" of a retrieved
    Article 42 passage is fine; citing a document or article never retrieved is not."""
    c = _norm(citation)
    cited_pages = [(int(a), int(b or a)) for a, b in CITED_PAGES.findall(c)]
    for p in passages:
        if _norm(p["source"]) not in c:
            continue
        page_numbers = [int(x) for x in re.findall(r"\d+", p["pages"])]
        lo, hi = page_numbers[0], page_numbers[-1]
        if any(a <= hi and b >= lo for a, b in cited_pages):
            return True
        heading = p["heading"]
        key = _section_key(heading) if heading else None
        if key and re.search(rf"{re.escape(key)}(?![\d])", c):
            return True
        if heading and _norm(heading)[:25] in c:
            return True
    return False


def check_citations(answer: str, search_outputs: list[str], document_request: bool = False) -> dict:
    passages = retrieved_passages(search_outputs)
    citations = CITATION.findall(answer)
    invalid = [c for c in citations if not citation_is_valid(c, passages)]
    is_refusal = answer.strip().startswith(REFUSAL)
    if is_refusal:
        verdict = "refusal"
    elif document_request and not search_outputs:
        verdict = "document request"  # a reply about adding a file, not a claim about the rules
    elif not search_outputs:
        verdict = "blocked: answered without searching"
    elif not citations:
        verdict = "blocked: no citations"
    elif invalid:
        verdict = "blocked: citation not in retrieved passages"
    else:
        verdict = "ok"
    return {"verdict": verdict, "citations": citations, "invalid": invalid, "is_refusal": is_refusal}


# ---------------------------------------------------------------------------
# Agent
# ---------------------------------------------------------------------------
def ask_in_terminal(name: str, args: dict) -> bool:
    """Approval prompt for add_document. No terminal (evaluation, CI) means no."""
    if not sys.stdin.isatty():
        log(f"[approval] {name}({args}) rejected: no terminal to ask for approval.")
        return False
    print(f"\nThe agent wants to run {name} with {args}.", file=sys.stderr)
    reply = input("Approve? [y/N] ").strip().lower()
    return reply in {"y", "yes"}


class CorpusAgent:
    def __init__(self, approve: Callable[[str, dict], bool] = ask_in_terminal, model: str = MODEL):
        self.approve = approve
        self.model_name = model
        self._stack = AsyncExitStack()

    async def __aenter__(self) -> "CorpusAgent":
        from langchain.agents import create_agent
        from langchain.agents.middleware import (
            HumanInTheLoopMiddleware,
            ModelCallLimitMiddleware,
            ModelFallbackMiddleware,
            ToolCallLimitMiddleware,
        )
        from langchain_google_genai import ChatGoogleGenerativeAI
        from langgraph.checkpoint.memory import InMemorySaver
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client

        load_api_key()
        # pass the environment on, so CORPUS_INDEX_DIR (before/after test) reaches the server
        params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT), env=dict(os.environ))
        read, write = await self._stack.enter_async_context(stdio_client(params))
        session = await self._stack.enter_async_context(ClientSession(read, write))
        await session.initialize()
        tools = [to_langchain_tool(session, t) for t in (await session.list_tools()).tools]

        def chat_model(name: str):
            return ChatGoogleGenerativeAI(model=name, temperature=0, timeout=MODEL_TIMEOUT, max_retries=2)

        self.agent = create_agent(
            chat_model(self.model_name),
            tools=tools,
            system_prompt=SYSTEM_PROMPT,
            middleware=[
                ModelFallbackMiddleware(chat_model(FALLBACK_MODEL)),
                HumanInTheLoopMiddleware(
                    interrupt_on={"add_document": {"allowed_decisions": ["approve", "reject"]}},
                    description_prefix="Adding a document changes the corpus",
                ),
                ToolCallLimitMiddleware(run_limit=TOOL_CALL_LIMIT, exit_behavior="end"),
                ModelCallLimitMiddleware(run_limit=MODEL_CALL_LIMIT, exit_behavior="end"),
            ],
            checkpointer=InMemorySaver(),  # needed to pause for approval and resume
        )
        return self

    async def __aexit__(self, *exc) -> None:
        await self._stack.aclose()

    async def ask(self, question: str) -> dict[str, Any]:
        from langgraph.types import Command

        config = {"configurable": {"thread_id": str(uuid.uuid4())}}
        started = time.time()
        state = await self.agent.ainvoke({"messages": [{"role": "user", "content": question}]}, config)

        approvals = []
        while state.get("__interrupt__"):
            decisions = []
            for interrupt in state["__interrupt__"]:
                for request in interrupt.value["action_requests"]:
                    ok = self.approve(request["name"], request["args"])
                    approvals.append({"tool": request["name"], "args": request["args"], "approved": ok})
                    decisions.append(
                        {"type": "approve"}
                        if ok
                        else {"type": "reject", "message": "The user did not approve adding this document."}
                    )
            state = await self.agent.ainvoke(Command(resume={"decisions": decisions}), config)

        return self._result(question, state["messages"], approvals, time.time() - started)

    def _result(self, question: str, messages: list, approvals: list, seconds: float) -> dict[str, Any]:
        trace, search_outputs = [], []
        tokens = {"input": 0, "output": 0, "total": 0}
        for m in messages:
            usage = getattr(m, "usage_metadata", None)
            if usage:
                tokens["input"] += usage.get("input_tokens", 0)
                tokens["output"] += usage.get("output_tokens", 0)
                tokens["total"] += usage.get("total_tokens", 0)
            for call in getattr(m, "tool_calls", None) or []:
                trace.append({"tool": call["name"], "args": call["args"]})
            if m.type == "tool":
                content = m.content if isinstance(m.content, str) else str(m.content)
                if m.name == "search":
                    search_outputs.append(content)
                if trace:
                    trace[-1].setdefault("output", content)

        final = messages[-1]
        raw_answer = final.text if final.type == "ai" else ""
        if not raw_answer:
            raw_answer = f"{REFUSAL} I stopped before finding an answer (call limit reached)."
        document_request = any(t["tool"] == "add_document" for t in trace)
        check = check_citations(raw_answer, search_outputs, document_request)
        answer = raw_answer if check["verdict"] in {"ok", "refusal", "document request"} else GUARDRAIL_REFUSAL
        if answer is GUARDRAIL_REFUSAL:
            log(f"[guardrail] {check['verdict']}; invalid citations: {check['invalid']}")

        return {
            "question": question,
            "answer": answer,
            "raw_answer": raw_answer,
            "guardrail": check["verdict"],
            "citations": check["citations"],
            "invalid_citations": check["invalid"],
            "is_refusal": answer.strip().startswith(REFUSAL),
            "search_outputs": search_outputs,
            "trace": trace,
            "approvals": approvals,
            "searches": sum(1 for t in trace if t["tool"] == "search"),
            "tokens": tokens,
            "seconds": round(seconds, 2),
            "model": self.model_name,
        }


async def _answer(question: str, approve=ask_in_terminal) -> dict[str, Any]:
    async with CorpusAgent(approve=approve) as agent:
        return await agent.ask(question)


def answer_question(question: str, approve=ask_in_terminal) -> dict[str, Any]:
    return asyncio.run(_answer(question, approve))


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit('usage: python agent.py "your question"')
    result = answer_question(" ".join(sys.argv[1:]))
    print(result["answer"])
    if result["citations"] and result["guardrail"] == "ok":
        print("\nSources:")
        for c in dict.fromkeys(result["citations"]):
            print(f"  - {c}")
    print(
        f"\n({result['searches']} search(es), {result['tokens']['total']} tokens, "
        f"{result['seconds']}s, guardrail: {result['guardrail']})"
    )


if __name__ == "__main__":
    main()
