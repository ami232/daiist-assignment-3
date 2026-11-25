"""
Assignment 3: the agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini. Its tools come from server.py over MCP
(stdio), exactly as an editor would use them. System prompt = AGENTS.md.

Guardrails
  1. Approval: add_document only runs after the user types "y" (in a
     non-interactive run, e.g. the evaluation, it is refused by default).
  2. Call limits: at most 8 model calls and 6 tool calls per question.
  3. Citation check (the guardrail of my choice): after the model answers,
     code verifies that every [ID] it cites was really returned by a search
     in this turn, and that a non-refusal cites at least one passage. If not,
     the model gets one retry with the problem spelled out; if it still fails,
     the answer is replaced by a refusal. Every firing is logged in
     eval/guardrail_log.jsonl.

`Harness.ask()` returns the answer plus the tool trace, token counts and time,
which evaluate.py uses.
"""

from __future__ import annotations

import asyncio
import json
import os
import sys
import time
from contextlib import AsyncExitStack
from pathlib import Path
from typing import Awaitable, Callable

from pydantic import Field, create_model

from settings import CHAT_MODEL, EVAL_DIR, REFUSAL, ROOT
from retrieval import CITATION, parse_results

SYSTEM_PROMPT = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
MAX_MODEL_CALLS, MAX_TOOL_CALLS = 8, 6
GUARDRAIL_LOG = EVAL_DIR / "guardrail_log.jsonl"

Approver = Callable[[str], Awaitable[bool]]


async def ask_in_terminal(path: str) -> bool:
    """Default approval step: ask the person at the terminal."""
    if not sys.stdin or not sys.stdin.isatty():
        print(f"[approval] add_document({path!r}) refused: no one at the terminal to approve it.", file=sys.stderr)
        return False
    prompt = f"\nThe agent wants to add the document {path!r} to the index. Approve? [y/N] "
    answer = await asyncio.to_thread(input, prompt)
    return answer.strip().lower() in {"y", "yes"}


async def always_deny(path: str) -> bool:
    return False


def message_text(message) -> str:
    """Gemini can return content as a list of parts; keep only the text."""
    content = message.content
    if isinstance(content, str):
        return content
    return "".join(p.get("text", "") if isinstance(p, dict) else str(p) for p in content)


def is_refusal(answer: str) -> bool:
    return answer.strip().lstrip("*_ ").lower().startswith(REFUSAL.lower())


class Harness:
    """Start server.py once, then answer any number of questions with it."""

    def __init__(self, approver: Approver = ask_in_terminal, model: str = CHAT_MODEL, log_guardrail: bool = True):
        self.approver, self.model_name, self.log_guardrail = approver, model, log_guardrail
        self.stack = AsyncExitStack()
        self.trace: list[dict] = []

    async def __aenter__(self) -> "Harness":
        try:
            return await self._start()
        except BaseException:
            await self.stack.aclose()   # never leave the server process hanging
            raise

    async def _start(self) -> "Harness":
        from langchain.agents import create_agent
        from langchain.agents.middleware import ModelCallLimitMiddleware, ToolCallLimitMiddleware
        from langchain_google_genai import ChatGoogleGenerativeAI
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client

        from api_key import load_api_key

        load_api_key()
        params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT), env=dict(os.environ))
        read, write = await self.stack.enter_async_context(stdio_client(params))
        self.session = await self.stack.enter_async_context(ClientSession(read, write))
        await self.session.initialize()
        mcp_tools = (await self.session.list_tools()).tools
        self.tools = {t.name: t for t in mcp_tools}
        model = ChatGoogleGenerativeAI(model=self.model_name)
        self.agent = create_agent(
            model,
            tools=[self._wrap(t) for t in mcp_tools],
            system_prompt=SYSTEM_PROMPT,
            middleware=[
                ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS, exit_behavior="end"),
                ToolCallLimitMiddleware(run_limit=MAX_TOOL_CALLS, exit_behavior="continue"),
            ],
        )
        return self

    async def __aexit__(self, *exc) -> None:
        await self.stack.aclose()

    def _wrap(self, tool):
        """Turn one MCP tool into a LangChain tool that calls the server."""
        from langchain_core.tools import StructuredTool

        types = {"string": str, "integer": int, "number": float, "boolean": bool}
        schema = getattr(tool, "input_schema", None) or getattr(tool, "inputSchema", None) or {}
        required = set(schema.get("required", []))
        fields = {}
        for name, spec in schema.get("properties", {}).items():
            kind = types.get(spec.get("type"), str)
            default = ... if name in required else spec.get("default")
            fields[name] = (kind if name in required else kind | None, Field(default, description=spec.get("description", "")))
        args_model = create_model(f"{tool.name}_args", **fields)

        async def call(**kwargs):
            kwargs = {k: v for k, v in kwargs.items() if v is not None}
            started = time.time()
            if tool.name == "add_document":
                approved = await self.approver(kwargs.get("path", ""))
                if not approved:
                    text = "DENIED: the user did not approve adding this document. Nothing was added."
                    self.trace.append({"tool": tool.name, "args": kwargs, "approved": False, "result": text})
                    return text
            result = await self.session.call_tool(tool.name, kwargs)
            text = "\n".join(getattr(c, "text", "") for c in result.content)
            self.trace.append({"tool": tool.name, "args": kwargs, "result": text,
                               "ids": [r["id"] for r in parse_results(text)], "seconds": round(time.time() - started, 2),
                               **({"approved": True} if tool.name == "add_document" else {})})
            return text

        return StructuredTool.from_function(coroutine=call, name=tool.name, description=tool.description or "",
                                            args_schema=args_model)

    async def _run(self, messages: list) -> tuple[str, list, dict]:
        result = await self.agent.ainvoke({"messages": messages})
        new = result["messages"][len(messages):]
        usage = {"input_tokens": 0, "output_tokens": 0, "model_calls": 0}
        for m in new:
            meta = getattr(m, "usage_metadata", None)
            if m.type == "ai":
                usage["model_calls"] += 1
            if meta:
                usage["input_tokens"] += meta.get("input_tokens", 0)
                usage["output_tokens"] += meta.get("output_tokens", 0)
        final = next((m for m in reversed(result["messages"]) if m.type == "ai" and message_text(m).strip()), None)
        return (message_text(final).strip() if final else ""), result["messages"], usage

    def _check_citations(self, answer: str) -> str | None:
        """None if the answer passes; otherwise what is wrong."""
        retrieved = {i for call in self.trace for i in call.get("ids", [])}
        cited = CITATION.findall(answer)
        unknown = sorted(set(cited) - retrieved)
        if not answer:
            return "the answer is empty"
        if any(c["tool"] == "add_document" for c in self.trace) and not cited:
            return None   # a request to add a file, not a question: nothing to cite
        if unknown:
            return f"it cites IDs that no search returned in this conversation: {', '.join(unknown)}"
        if not is_refusal(answer) and not cited:
            return "it makes claims without citing any retrieved passage"
        if not self.trace or not any(c["tool"] == "search" for c in self.trace):
            return "it answers without having searched the corpus"
        return None

    async def ask(self, question: str) -> dict:
        from langchain_core.messages import HumanMessage

        self.trace = []
        started = time.time()
        messages = [HumanMessage(question)]
        answer, history, usage = await self._run(messages)
        guardrail = None
        problem = self._check_citations(answer)
        if problem:
            guardrail = {"fired": True, "reason": problem, "first_answer": answer}
            feedback = HumanMessage(
                f"Your answer cannot be shown because {problem}. Rewrite it citing only passage IDs "
                f"returned by the search tool (search again if needed), or start with '{REFUSAL}.' "
                "if the passages do not answer the question."
            )
            retry_answer, history, retry_usage = await self._run(history + [feedback])
            for key in usage:
                usage[key] += retry_usage[key]
            second = self._check_citations(retry_answer)
            if second:
                guardrail["action"] = "replaced with refusal"
                guardrail["second_reason"] = second
                answer = (f"{REFUSAL}. I could not produce an answer that is fully supported by "
                          "cited passages, so please check with your compliance officer.")
            else:
                guardrail["action"] = "retried and passed"
                answer = retry_answer
            if self.log_guardrail:
                GUARDRAIL_LOG.parent.mkdir(exist_ok=True)
                with GUARDRAIL_LOG.open("a", encoding="utf-8") as out:
                    out.write(json.dumps({"time": time.strftime("%Y-%m-%d %H:%M:%S"), "question": question,
                                          "final_answer": answer, **guardrail}) + "\n")

        cited = list(dict.fromkeys(CITATION.findall(answer)))
        located = {r["id"]: r for call in self.trace for r in parse_results(call.get("result", ""))}
        return {
            "question": question,
            "answer": answer,
            "refused": is_refusal(answer),
            "citations": [located.get(c, {"id": c, "title": "?", "location": "?"}) for c in cited],
            "trace": self.trace,
            "retrieved_ids": list(dict.fromkeys(i for c in self.trace for i in c.get("ids", []))),
            "searches": sum(1 for c in self.trace if c["tool"] == "search"),
            "guardrail": guardrail,
            "seconds": round(time.time() - started, 2),
            "model": self.model_name,
            **usage,
        }


def render(result: dict) -> str:
    lines = [result["answer"], ""]
    if result["citations"]:
        lines.append("Sources:")
        lines += [f"  [{c['id']}] {c['title']} | {c['location']}" for c in result["citations"]]
    if result["guardrail"]:
        lines.append(f"\n(citation guardrail fired: {result['guardrail']['reason']}; {result['guardrail']['action']})")
    lines.append(f"\n({result['searches']} searches, {result['model_calls']} model calls, "
                 f"{result['input_tokens'] + result['output_tokens']} tokens, {result['seconds']}s)")
    return "\n".join(lines)


async def main(question: str) -> None:
    async with Harness() as harness:
        result = await harness.ask(question)
    print(render(result))


if __name__ == "__main__":
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")   # answers contain "§"
    if len(sys.argv) < 2:
        raise SystemExit('usage: python agent.py "your question"')
    asyncio.run(main(" ".join(sys.argv[1:])))
