"""
Assignment 3: your agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the tools of server.py over MCP and
AGENTS.md as system prompt.

Safeguards:
  * approval: add_document never runs without a human "yes" (HumanInTheLoopMiddleware);
  * call limit: at most MAX_MODEL_CALLS model calls per question (ModelCallLimitMiddleware);
  * guardrail: add_document paths are checked BEFORE a human is even asked. Anything outside
    corpus/ or extra/ (or of the wrong type) is blocked, so a path planted in a retrieved
    passage never reaches the approval prompt, let alone the index.

Other code gets the answer and the tool trace from `AgentSession.ask()` / `ask_once()`.
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
from typing import Callable

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

from api_key import load_api_key  # noqa: E402
from index import check_add_path  # noqa: E402

AGENT_MODEL = os.environ.get("AGENT_MODEL", "gemini-3.5-flash-lite")
MAX_MODEL_CALLS = 8
CITATION_RE = re.compile(r"\[([a-z0-9.\-]+), ((?:pp?\.|parts?) [\d\-, ]+?)\]")
RESULT_CITE_RE = re.compile(r"cite as \[([^,\]]+), ([^\]]+)\]")

Approver = Callable[[str, dict], "bool | str"]   # (tool name, args) -> True / False / reason to reject


def system_prompt() -> str:
    return (ROOT / "AGENTS.md").read_text(encoding="utf-8")


def cli_approver(name: str, args: dict) -> bool | str:
    """Ask on the terminal. Without a terminal (evaluation, CI) the answer is no."""
    if not sys.stdin.isatty():
        return "No human is available to approve this action."
    print(f"\nThe agent wants to run {name}({args}).", file=sys.stderr)
    return input("Approve? [y/N] ").strip().lower() in {"y", "yes", "s", "si", "sí"}


def message_text(message) -> str:
    text = getattr(message, "text", None)      # a str subclass in current langchain-core
    if isinstance(text, str):
        return str(text)
    content = message.content
    if isinstance(content, str):
        return content
    return "".join(part.get("text", "") if isinstance(part, dict) else str(part) for part in content)


class AgentSession:
    """One MCP connection to server.py and one agent on top of it; ask() can be called many times."""

    def __init__(self, approver: Approver | None = None, model=None, tools=None):
        self.approver = approver or cli_approver
        self._model, self._tools = model, tools
        self._stack = AsyncExitStack()

    async def __aenter__(self) -> "AgentSession":
        from langchain.agents import create_agent
        from langchain.agents.middleware import HumanInTheLoopMiddleware, ModelCallLimitMiddleware
        from langgraph.checkpoint.memory import InMemorySaver

        if self._tools is None:
            self._tools = await self._connect_mcp()
        if self._model is None:
            from langchain_google_genai import ChatGoogleGenerativeAI

            load_api_key()
            self._model = ChatGoogleGenerativeAI(model=AGENT_MODEL, temperature=0, max_retries=6)
        self.agent = create_agent(
            self._model,
            self._tools,
            system_prompt=system_prompt(),
            middleware=[
                ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS, exit_behavior="end"),
                HumanInTheLoopMiddleware(interrupt_on={"add_document": True}),
            ],
            checkpointer=InMemorySaver(),
        )
        return self

    async def __aexit__(self, *exc) -> None:
        await self._stack.aclose()

    async def _connect_mcp(self):
        from langchain_core.tools import StructuredTool
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client

        params = StdioServerParameters(command=sys.executable, args=[str(ROOT / "server.py")], cwd=str(ROOT))
        read, write = await self._stack.enter_async_context(stdio_client(params))
        session = await self._stack.enter_async_context(ClientSession(read, write))
        await session.initialize()

        def wrap(tool):
            async def call(**kwargs) -> str:
                result = await session.call_tool(tool.name, kwargs)
                text = "\n".join(getattr(c, "text", "") for c in result.content).strip()
                return f"Error: {text}" if getattr(result, "is_error", False) or getattr(result, "isError", False) else text

            return StructuredTool(name=tool.name, description=tool.description or "", args_schema=tool.input_schema, coroutine=call)

        return [wrap(t) for t in (await session.list_tools()).tools]

    # ---- one question ------------------------------------------------------
    async def ask(self, question: str) -> dict:
        from langgraph.types import Command

        started = time.time()
        config = {"configurable": {"thread_id": str(uuid.uuid4())}}
        trace: dict = {"approvals": [], "guardrail_blocks": []}
        state = await self.agent.ainvoke({"messages": [("user", question)]}, config)
        while state.get("__interrupt__"):                       # the agent paused before add_document
            decisions = []
            for request in state["__interrupt__"][0].value["action_requests"]:
                name, args = request["name"], request.get("args", {})
                try:
                    check_add_path(str(args.get("path", "")))     # GUARDRAIL: before any human is asked
                except ValueError as error:
                    trace["guardrail_blocks"].append({"tool": name, "args": args, "reason": str(error)})
                    decisions.append({"type": "reject", "message": f"Blocked by guardrail. {error}"})
                    continue
                verdict = self.approver(name, args)
                trace["approvals"].append({"tool": name, "args": args, "approved": verdict is True})
                if verdict is True:
                    decisions.append({"type": "approve"})
                else:
                    reason = verdict if isinstance(verdict, str) else "The user did not approve."
                    decisions.append({"type": "reject", "message": f"Not run. {reason}"})
            state = await self.agent.ainvoke(Command(resume={"decisions": decisions}), config)
        return self._summarise(question, state["messages"], trace, time.time() - started)

    @staticmethod
    def _summarise(question: str, messages: list, trace: dict, seconds: float) -> dict:
        calls, results = {}, []
        for m in messages:
            for c in getattr(m, "tool_calls", None) or []:
                calls[c["id"]] = {"name": c["name"], "args": c["args"], "result": None}
            if m.type == "tool" and m.tool_call_id in calls:
                calls[m.tool_call_id]["result"] = message_text(m)
        tool_calls = list(calls.values())
        retrieved_text = "\n\n".join(c["result"] or "" for c in tool_calls if c["name"] == "search")
        usage = [getattr(m, "usage_metadata", None) or {} for m in messages if m.type == "ai"]
        last_ai = next((m for m in reversed(messages) if m.type == "ai" and not getattr(m, "tool_calls", None)), None)
        answer = message_text(last_ai).strip() if last_ai else ""
        hit_limit = not answer or "limit" in answer.lower() and "model call" in answer.lower()
        return {
            "question": question,
            "answer": answer or "(no answer: the call limit was reached)",
            "tool_calls": tool_calls,
            "retrieved_text": retrieved_text,
            "retrieved_citations": sorted({f"[{s}, {l}]" for s, l in RESULT_CITE_RE.findall(retrieved_text)}),
            "cited": sorted({f"[{s}, {l.strip()}]" for s, l in CITATION_RE.findall(answer)}),
            "model_calls": sum(1 for m in messages if m.type == "ai"),
            "input_tokens": sum(u.get("input_tokens", 0) for u in usage),
            "output_tokens": sum(u.get("output_tokens", 0) for u in usage),
            "seconds": round(seconds, 2),
            "hit_call_limit": bool(hit_limit),
            **trace,
        }


async def ask_once(question: str, approver: Approver | None = None) -> dict:
    async with AgentSession(approver) as session:
        return await session.ask(question)


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit('usage: python agent.py "your question"')
    result = asyncio.run(ask_once(" ".join(sys.argv[1:])))
    print(result["answer"])
    if result["cited"]:
        print("\nCitations: " + "; ".join(result["cited"]))
    for block in result["guardrail_blocks"]:
        print(f"\n[guardrail] {block['reason']}", file=sys.stderr)
    print(f"\n[{result['model_calls']} model calls, {len(result['tool_calls'])} tool calls, "
          f"{result['input_tokens']}+{result['output_tokens']} tokens, {result['seconds']}s]", file=sys.stderr)


if __name__ == "__main__":
    main()
