"""
Assignment 3: the agent harness (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the tools of server.py over MCP and
AGENTS.md as the system prompt. Guardrails:

1. Approval: add_document never runs without a human "y" (HumanInTheLoopMiddleware).
   With no human at the keyboard (evaluation, piped input with nothing on it) it is rejected.
2. Call limits: at most 6 tool calls and 10 model calls per question.
3. Citation check: every [Source, Location] tag in the answer must come from a
   search result of this run, and an answer that is not a refusal must cite
   something. If not, the agent gets one retry with the problem spelled out;
   if it fails again, the harness answers with the refusal instead.

`ask()` returns the answer with its tool trace, tokens and time, for evaluate.py.
"""

from __future__ import annotations

import asyncio
import json
import os
import re
import sys
import time
import uuid
from contextlib import AsyncExitStack
from pathlib import Path

ROOT = Path(__file__).resolve().parent
AGENTS_MD = ROOT / "AGENTS.md"

AGENT_MODEL = os.environ.get("AGENT_MODEL", "gemini-3.5-flash-lite")
TOOL_CALL_LIMIT = 6
MODEL_CALL_LIMIT = 10

# The sentence that marks a refusal. AGENTS.md tells the model to use it, and
# evaluate.py's code checks look for it. Keep the two in sync.
REFUSAL = "The corpus does not cover this question."

CITATION = re.compile(r"\[([^\[\],]+?),\s*((?:Article|Annex|page|§)[^\[\]]*?)\]")
CITE_AS = re.compile(r"cite as \[([^\[\],]+?),\s*([^\[\]]+?)\]")


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


# ------------------------------------------------------------------- citations


def normalise(location: str) -> str:
    """'Article 6(1)(a)' -> 'Article 6', so a precise pinpoint still matches its article."""
    location = location.strip()
    m = re.match(r"^((?:Article|Annex)\s+[0-9IVXLC]+[a-z]?)\b", location)
    return m.group(1) if m else location


def citations_in(text: str) -> list[tuple[str, str]]:
    return [(s.strip(), normalise(loc)) for s, loc in CITATION.findall(text or "")]


def retrieved_in(tool_output: str) -> set[tuple[str, str]]:
    return {(s.strip(), normalise(loc)) for s, loc in CITE_AS.findall(tool_output or "")}


def is_refusal(text: str) -> bool:
    return REFUSAL.lower().rstrip(".") in (text or "").lower()


def check_citations(answer: str, retrieved: set[tuple[str, str]]) -> str | None:
    """None if the answer passes, else what is wrong with it."""
    cited = citations_in(answer)
    if not cited:
        return None if is_refusal(answer) else "the answer has no citation tags"
    # a pinpoint such as "Article 5 to Article 6" from the fixed design counts if it was retrieved
    bad = [f"[{s}, {loc}]" for s, loc in cited if (s, loc) not in retrieved]
    return f"it cites {', '.join(sorted(set(bad)))}, which no search result of this run contains" if bad else None


# ----------------------------------------------------------------------- tools


async def mcp_tools(stack: AsyncExitStack):
    """Start server.py over stdio and wrap its tools as LangChain tools."""
    from langchain_core.tools import StructuredTool
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT))
    read, write = await stack.enter_async_context(stdio_client(params))
    session = await stack.enter_async_context(ClientSession(read, write))
    await session.initialize()

    def wrap(tool):
        async def call(**kwargs) -> str:
            result = await session.call_tool(tool.name, kwargs)
            return "\n".join(getattr(c, "text", "") for c in result.content)

        return StructuredTool.from_function(
            coroutine=call, name=tool.name, description=tool.description, args_schema=tool.input_schema
        )

    return [wrap(t) for t in (await session.list_tools()).tools]


def terminal_approval(request: dict) -> bool:
    """Ask the person at the keyboard. Anything but 'y' (or no input at all) rejects."""
    print(f"\nThe agent wants to run {request['name']} with {json.dumps(request['args'])}.", flush=True)
    print("Approve? [y/N] ", end="", flush=True)
    try:
        answer = sys.stdin.readline()
    except Exception:  # noqa: BLE001
        answer = ""
    print(answer.strip() or "(no answer)", flush=True)
    return answer.strip().lower() in ("y", "yes")


def never_approve(request: dict) -> bool:
    return False


# ----------------------------------------------------------------------- agent


class Agent:
    """One MCP server and one compiled agent, reused across questions."""

    def __init__(self, system_prompt: str | None = None, model: str = AGENT_MODEL):
        self.system_prompt = system_prompt or load_system_prompt()
        self.model_name = model
        self.stack = AsyncExitStack()

    async def __aenter__(self):
        from langchain.agents import create_agent
        from langchain.agents.middleware import (
            HumanInTheLoopMiddleware,
            ModelCallLimitMiddleware,
            ToolCallLimitMiddleware,
        )
        from langchain_google_genai import ChatGoogleGenerativeAI
        from langgraph.checkpoint.memory import InMemorySaver

        from api_key import load_api_key

        load_api_key()
        self.tools = await mcp_tools(self.stack)
        model = ChatGoogleGenerativeAI(model=self.model_name, temperature=0, max_retries=6)
        self.graph = create_agent(
            model,
            self.tools,
            system_prompt=self.system_prompt,
            middleware=[
                HumanInTheLoopMiddleware(interrupt_on={"add_document": {"allowed_decisions": ["approve", "reject"]}}),
                ToolCallLimitMiddleware(run_limit=TOOL_CALL_LIMIT, exit_behavior="continue"),
                ModelCallLimitMiddleware(run_limit=MODEL_CALL_LIMIT, exit_behavior="end"),
            ],
            checkpointer=InMemorySaver(),
        )
        return self

    async def __aexit__(self, *exc):
        await self.stack.aclose()

    async def _run(self, payload, config, approve) -> dict:
        from langgraph.types import Command

        result = await self.graph.ainvoke(payload, config)
        while result.get("__interrupt__"):
            decisions = []
            for interrupt in result["__interrupt__"]:
                for request in interrupt.value["action_requests"]:
                    ok = approve(request)
                    self.events.append({"guardrail": "approval", "tool": request["name"], "args": request["args"], "approved": ok})
                    decisions.append({"type": "approve"} if ok else
                                     {"type": "reject", "message": "The user did not approve adding this document."})
            result = await self.graph.ainvoke(Command(resume={"decisions": decisions}), config)
        return result

    async def ask(self, question: str, approve=terminal_approval) -> dict:
        from langchain_core.messages import AIMessage, HumanMessage, ToolMessage

        started = time.time()
        self.events: list[dict] = []
        config = {"configurable": {"thread_id": str(uuid.uuid4())}, "recursion_limit": 50}
        result = await self._run({"messages": [HumanMessage(question)]}, config, approve)

        def final_and_retrieved(messages):
            retrieved: set[tuple[str, str]] = set()
            for m in messages:
                if isinstance(m, ToolMessage) and m.name == "search":
                    retrieved |= retrieved_in(m.text)
            last = next((m for m in reversed(messages) if isinstance(m, AIMessage) and m.text.strip()), None)
            return (last.text.strip() if last else ""), retrieved

        answer, retrieved = final_and_retrieved(result["messages"])
        # A request to add a document gets a confirmation, not a legal answer, so it has
        # nothing to cite. (Found in the add-document demo: the check turned the
        # confirmation into a refusal.)
        acted = any(isinstance(m, AIMessage) and any(c["name"] == "add_document" for c in m.tool_calls)
                    for m in result["messages"])
        problem = None if acted else check_citations(answer, retrieved)
        if acted:
            self.events.append({"guardrail": "citation_check", "skipped": "the run added a document"})
        if problem:
            self.events.append({"guardrail": "citation_check", "attempt": 1, "problem": problem, "draft": answer})
            retry = HumanMessage(
                f"Citation check failed: {problem}. Rewrite your answer using only passages returned by the "
                f"search tool, with their exact [Source, Location] tags, searching again if you need to. "
                f"If the search results do not answer the question, reply: {REFUSAL}"
            )
            result = await self._run({"messages": [retry]}, config, approve)
            answer, retrieved = final_and_retrieved(result["messages"])
            problem = check_citations(answer, retrieved)
            if problem:
                self.events.append({"guardrail": "citation_check", "attempt": 2, "problem": problem, "replaced": answer})
                answer = REFUSAL   # the withheld draft stays in the trace (events)

        trace, tokens_in, tokens_out = [], 0, 0
        for m in result["messages"]:
            if isinstance(m, AIMessage):
                usage = m.usage_metadata or {}
                tokens_in += usage.get("input_tokens", 0)
                tokens_out += usage.get("output_tokens", 0)
                for call in m.tool_calls:
                    trace.append({"tool": call["name"], "args": call["args"], "id": call["id"]})
            elif isinstance(m, ToolMessage):
                for step in trace:
                    if step.get("id") == m.tool_call_id:
                        step["output"] = m.text
        return {
            "question": question,
            "answer": answer,
            "citations": [f"[{s}, {loc}]" for s, loc in dict.fromkeys(citations_in(answer))],
            "refusal": is_refusal(answer),
            "trace": trace,
            "events": self.events,
            "tokens_in": tokens_in,
            "tokens_out": tokens_out,
            "seconds": round(time.time() - started, 2),
            "model": self.model_name,
        }


def load_system_prompt() -> str:
    text = AGENTS_MD.read_text(encoding="utf-8")
    body = re.sub(r"<!--.*?-->", "", text, flags=re.S).strip()
    if len(body.splitlines()) < 3:
        raise SystemExit("AGENTS.md has no rules yet. Write them first: it is the agent's system prompt.")
    return body


async def ask(question: str, approve=terminal_approval) -> dict:
    """Answer one question with a fresh server. evaluate.py keeps one Agent open instead."""
    async with Agent() as agent:
        return await agent.ask(question, approve)


def print_answer(result: dict) -> None:
    print(result["answer"])
    if result["citations"]:
        print("\nCitations:")
        for c in result["citations"]:
            print(f"  {c}")
    searches = [s["args"].get("query") for s in result["trace"] if s["tool"] == "search"]
    log(f"\n[{len(searches)} search(es): {searches}; {result['tokens_in']}+{result['tokens_out']} tokens; "
        f"{result['seconds']}s; guardrail events: {result['events'] or 'none'}]")


def main() -> None:
    question = " ".join(sys.argv[1:]).strip()
    if not question:
        raise SystemExit('Usage: python agent.py "your question"')
    print_answer(asyncio.run(ask(question)))


if __name__ == "__main__":
    main()
