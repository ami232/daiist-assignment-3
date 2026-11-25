"""
Assignment 3: the food-safety agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the tools of server.py reached over MCP
(stdio, exactly as an editor would start it) and AGENTS.md as the system prompt.

Safeguards in this harness:
- approval: add_document never runs without a human "yes" (HumanInTheLoopMiddleware);
  with no terminal to ask, the call is rejected;
- call limits: at most 6 tool calls and 8 model calls per question;
- extra guardrail, citation check: every citation in the answer must be one that a
  search actually returned, and a non-refusal must cite at least once. A failing
  answer gets one rewrite request; if it still fails, it is replaced by a refusal.

`Harness` (async context manager) keeps one server session for many questions;
evaluate.py uses it. `ask(question)` is the one-shot version.
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

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
SYSTEM_PROMPT = (ROOT / "AGENTS.md").read_text(encoding="utf-8")


def _setting(name: str, default: str) -> str:
    """A setting from the environment, else from a NAME=value line in .env, else the default."""
    if os.environ.get(name):
        return os.environ[name]
    env = ROOT / ".env"
    if env.is_file():
        for line in env.read_text(encoding="utf-8").splitlines():
            key, sep, value = line.strip().partition("=")
            if sep and key.strip() == name and value.strip():
                return value.strip().strip('"').strip("'")
    return default


# Chat model for the agent and the judge. Free-tier daily limits differ a lot per model
# (some Flash models allow only 20 requests a day); a Flash-Lite model allows far more.
MODEL = _setting("GEMINI_MODEL", "gemini-flash-lite-latest")
JUDGE_MODEL = _setting("JUDGE_MODEL", MODEL)
MAX_TOOL_CALLS, MAX_MODEL_CALLS = 6, 8

REFUSAL_OPENING = "The documents I have do not cover this"
SAFE_REFUSAL = (REFUSAL_OPENING + " reliably: I could not support an answer with a citation from the "
                "FDA documents I search. Please check the FDA Food Code or ask your local health authority.")
CITATION = re.compile(r"\[[a-z0-9_]+, [^\[\]\n]+\]")
RESULT_CITATION = re.compile(r"^(\[[a-z0-9_]+, [^\[\]\n]+\]) score=", re.M)
REFUSAL_PATTERNS = re.compile(
    r"do(?:es)? not cover|don't cover|not covered|cannot find|can't find|could not find|no information|"
    r"not (?:in|addressed in|mentioned in) the (?:documents|corpus|passages)", re.I)


def is_refusal(answer: str) -> bool:
    return bool(REFUSAL_PATTERNS.search(answer[:400]))


def check_citations(answer: str, retrieved: set[str]) -> dict:
    """The guardrail's test, also used as a code check in evaluate.py."""
    cited = list(dict.fromkeys(CITATION.findall(answer)))
    invalid = [c for c in cited if c not in retrieved]
    refusal = is_refusal(answer)
    ok = not invalid and (refusal or bool(cited))
    reason = ("" if ok else f"citations not returned by search: {invalid}" if invalid
              else "no citation in a non-refusal answer")
    return {"cited": cited, "invalid": invalid, "refusal": refusal, "ok": ok, "reason": reason}


def _text(message) -> str:
    """Plain text of a message (Gemini 3 returns content as a list of parts)."""
    return str(message.text)


def terminal_approval(name: str, args: dict) -> bool:
    """Ask the person at the terminal. No terminal (e.g. check.py, evaluate.py): reject."""
    if not sys.stdin.isatty():
        print(f"[approval] {name}({args}) rejected: no one at a terminal to approve it.", file=sys.stderr)
        return False
    reply = input(f"\nThe agent wants to run {name} with {args}.\nThis embeds the file and changes the index. "
                  f"Approve? [y/N] ")
    return reply.strip().lower() in {"y", "yes"}


class Harness:
    """One MCP session to server.py and one agent, reused across questions."""

    def __init__(self, approve=terminal_approval, model: str = MODEL):
        self.approve = approve
        self.model_name = model

    async def __aenter__(self) -> "Harness":
        from langchain.agents import create_agent
        from langchain.agents.middleware import (HumanInTheLoopMiddleware, ModelCallLimitMiddleware,
                                                 ToolCallLimitMiddleware)
        from langchain_core.tools import StructuredTool
        from langchain_google_genai import ChatGoogleGenerativeAI
        from langgraph.checkpoint.memory import InMemorySaver
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client

        load_api_key()
        params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT))
        self._stack = AsyncExitStack()
        try:
            read, write = await self._stack.enter_async_context(stdio_client(params))
            self.session = await self._stack.enter_async_context(ClientSession(read, write))
            await self.session.initialize()
        except BaseException:
            await self._stack.aclose()
            raise

        def wrap(tool):
            async def call(**kwargs) -> str:
                result = await self.session.call_tool(tool.name, kwargs)
                return "\n".join(getattr(c, "text", "") for c in result.content)
            return StructuredTool(name=tool.name, description=tool.description or "",
                                  args_schema=tool.input_schema, coroutine=call)

        self.tools = [wrap(t) for t in (await self.session.list_tools()).tools]
        model = ChatGoogleGenerativeAI(model=self.model_name, max_retries=6)
        self.agent = create_agent(
            model, self.tools, system_prompt=SYSTEM_PROMPT, checkpointer=InMemorySaver(),
            middleware=[
                HumanInTheLoopMiddleware(interrupt_on={"add_document": {"allowed_decisions": ["approve", "reject"]}}),
                ToolCallLimitMiddleware(run_limit=MAX_TOOL_CALLS),
                ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS, exit_behavior="end"),
            ])
        return self

    async def __aexit__(self, *exc) -> None:
        await self._stack.aclose()

    async def _run(self, payload, config: dict, trace: dict) -> None:
        """Invoke the agent, answering approval interrupts until it finishes."""
        from langgraph.types import Command

        await self.agent.ainvoke(payload, config)
        while (state := await self.agent.aget_state(config)).interrupts:
            decisions = []
            for request in state.interrupts[0].value["action_requests"]:
                approved = self.approve(request["name"], request["args"])
                trace["approvals"].append({"tool": request["name"], "args": request["args"], "approved": approved})
                decisions.append({"type": "approve"} if approved else
                                 {"type": "reject", "message": "The user did not approve this. Do not retry it."})
            await self.agent.ainvoke(Command(resume={"decisions": decisions}), config)

    async def ask(self, question: str) -> dict:
        """Answer one question. Returns the answer and its full trace for evaluate.py."""
        config = {"configurable": {"thread_id": str(uuid.uuid4())}}
        trace = {"question": question, "approvals": [], "guardrail": "passed"}
        started = time.time()
        await self._run({"messages": [{"role": "user", "content": question}]}, config, trace)
        answer, retrieved = self._answer_and_results(await self.agent.aget_state(config))
        check = check_citations(answer, retrieved)
        state = await self.agent.aget_state(config)
        action_only = not retrieved and any(
            c["name"] == "add_document" for m in state.values["messages"] if m.type == "ai" for c in (m.tool_calls or []))
        if action_only and not check["invalid"]:
            # A reply that reports an add_document action makes no claims about the corpus,
            # so it needs no citation (found when a confirmation was turned into a refusal).
            check = {**check, "ok": True, "reason": ""}
            trace["guardrail"] = "not applicable (document action, no search)"
        if not check["ok"]:
            # Guardrail, step 1: one rewrite request that names the problem.
            trace["guardrail"] = f"rewrite requested ({check['reason']})"
            await self._run({"messages": [{"role": "user", "content": (
                f"Your answer failed the citation check: {check['reason']}. Rewrite it citing only "
                f"citations exactly as the search results printed them, or reply "
                f"'{REFUSAL_OPENING}.' if the results do not support an answer.")}]}, config, trace)
            answer, retrieved = self._answer_and_results(await self.agent.aget_state(config))
            check = check_citations(answer, retrieved)
            if not check["ok"]:
                # Step 2: never show an answer we cannot back with a passage.
                trace["guardrail"] = f"blocked ({check['reason']})"
                trace["blocked_answer"] = answer
                answer = SAFE_REFUSAL
                check = check_citations(answer, retrieved)
        messages = (await self.agent.aget_state(config)).values["messages"]
        trace.update(self._usage(messages))
        trace.update(answer=answer, check=check, seconds=round(time.time() - started, 2))
        return trace

    @staticmethod
    def _answer_and_results(state) -> tuple[str, set[str]]:
        messages = state.values["messages"]
        answer = next((_text(m) for m in reversed(messages) if m.type == "ai" and _text(m).strip()), "")
        retrieved = {c for m in messages if m.type == "tool" and m.name == "search"
                     for c in RESULT_CITATION.findall(_text(m))}
        return answer.strip(), retrieved

    @staticmethod
    def _usage(messages) -> dict:
        tool_calls = [{"tool": c["name"], "args": c["args"]} for m in messages if m.type == "ai"
                      for c in (m.tool_calls or [])]
        results = [{"tool": m.name, "text": _text(m)} for m in messages if m.type == "tool"]
        usage = [m.usage_metadata or {} for m in messages if m.type == "ai"]
        return {
            "tool_calls": tool_calls,
            "tool_results": results,
            "model_calls": len(usage),
            "input_tokens": sum(u.get("input_tokens", 0) for u in usage),
            "output_tokens": sum(u.get("output_tokens", 0) for u in usage),
        }


async def ask_async(question: str, approve=terminal_approval) -> dict:
    async with Harness(approve=approve) as harness:
        return await harness.ask(question)


def ask(question: str, approve=terminal_approval) -> dict:
    return asyncio.run(ask_async(question, approve))


def main() -> int:
    if len(sys.argv) < 2:
        print('usage: python agent.py "your question"', file=sys.stderr)
        return 1
    result = ask(" ".join(sys.argv[1:]))
    print(result["answer"])
    if result["check"]["cited"]:
        print("\nSources:")
        for cite in result["check"]["cited"]:
            print(f"  {cite}")
    searches = sum(1 for c in result["tool_calls"] if c["tool"] == "search")
    print(f"\n({searches} search(es), {result['model_calls']} model call(s), "
          f"{result['input_tokens'] + result['output_tokens']} tokens, {result['seconds']}s; "
          f"citation guardrail: {result['guardrail']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
