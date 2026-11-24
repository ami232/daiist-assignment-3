"""
Assignment 3: the agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the tools of server.py reached over MCP (stdio,
exactly as an editor starts it) and AGENTS.md as the system prompt.

Guardrails:
- Approval: add_document never runs without a person approving it at the terminal
  (HumanInTheLoopMiddleware). With no terminal (evaluation, CI) it is rejected.
- Call limits: at most MAX_TOOL_CALLS searches and MAX_MODEL_CALLS model calls per question.
- Citation check (the extra guardrail): every [source, location] in the final answer must
  be one the search tool actually returned in this run, and a non-refusal answer must cite
  something. If not, the model gets one chance to fix it; if it fails again, the answer
  is replaced by the refusal sentence. A made-up citation looks exactly like a real one
  to the user, so it is checked in code rather than trusted.

evaluate.py uses `Agent` to get the answer and the tool trace for every question.
"""

from __future__ import annotations

import asyncio
import re
import sys
import time
import uuid
from contextlib import AsyncExitStack

import config
from api_key import load_api_key

CITATION = re.compile(r"\[([a-z0-9_]+),\s*([^\[\]]+?)\]")
RETURNED = re.compile(r"cite as \[([a-z0-9_]+), ([^\[\]]+?)\]")


def citations_in(text: str) -> list[tuple[str, str]]:
    return list(dict.fromkeys((s, l.strip()) for s, l in CITATION.findall(text or "")))


def is_refusal(text: str) -> bool:
    return (text or "").strip().startswith(config.REFUSAL)


def terminal_approver(name: str, args: dict) -> bool:
    """Ask the person at the terminal. No terminal means no approval."""
    if not sys.stdin.isatty():
        print(f"[approval] {name}({args}) needs approval, but there is no terminal: rejected.", file=sys.stderr)
        return False
    answer = input(f"\nThe agent wants to run {name} with {args}.\nApprove? [y/N] ").strip().lower()
    return answer in {"y", "yes", "s", "si", "sí"}


class Agent:
    """One MCP connection to server.py and one compiled LangChain agent, reused across questions."""

    def __init__(self, approver=terminal_approver):
        self.approver = approver
        self.trace: list[dict] = []

    async def __aenter__(self) -> "Agent":
        from langchain.agents import create_agent
        from langchain.agents.middleware import (
            HumanInTheLoopMiddleware,
            ModelCallLimitMiddleware,
            ToolCallLimitMiddleware,
        )
        from langchain_core.rate_limiters import InMemoryRateLimiter
        from langchain_core.tools import StructuredTool
        from langchain_google_genai import ChatGoogleGenerativeAI
        from langgraph.checkpoint.memory import InMemorySaver
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client

        load_api_key()
        self._stack = AsyncExitStack()
        params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(config.ROOT))
        read, write = await self._stack.enter_async_context(stdio_client(params))
        self.session = await self._stack.enter_async_context(ClientSession(read, write))
        await self.session.initialize()

        tools = []
        for tool in (await self.session.list_tools()).tools:
            tools.append(StructuredTool.from_function(
                coroutine=self._caller(tool.name), name=tool.name,
                description=tool.description, args_schema=tool.input_schema,
            ))

        model = ChatGoogleGenerativeAI(
            model=config.AGENT_MODEL, max_retries=6,   # this model ignores temperature (fixed sampling)
            rate_limiter=InMemoryRateLimiter(requests_per_second=config.CHAT_REQUESTS_PER_MIN / 60,
                                             check_every_n_seconds=0.2, max_bucket_size=1),
        )
        self.agent = create_agent(
            model,
            tools=tools,
            system_prompt=(config.ROOT / "AGENTS.md").read_text(encoding="utf-8"),
            middleware=[
                HumanInTheLoopMiddleware(interrupt_on={"add_document": {"allowed_decisions": ["approve", "reject"]}}),
                ToolCallLimitMiddleware(tool_name="search", run_limit=config.MAX_TOOL_CALLS, exit_behavior="continue"),
                ModelCallLimitMiddleware(run_limit=config.MAX_MODEL_CALLS, exit_behavior="end"),
            ],
            checkpointer=InMemorySaver(),
        )
        return self

    async def __aexit__(self, *exc) -> None:
        await self._stack.aclose()

    def _caller(self, name: str):
        async def call(**kwargs) -> str:
            started = time.time()
            result = await self.session.call_tool(name, kwargs)
            text = "\n".join(getattr(c, "text", "") for c in result.content).strip()
            self.trace.append({"tool": name, "args": kwargs, "output": text, "seconds": round(time.time() - started, 2)})
            return text
        return call

    async def _run(self, payload, cfg) -> dict:
        """Invoke the agent, answering approval interrupts until it finishes."""
        from langgraph.types import Command

        result = await self.agent.ainvoke(payload, cfg)
        while result.get("__interrupt__"):
            decisions = []
            for interrupt in result["__interrupt__"]:
                for request in interrupt.value.get("action_requests", []):
                    approved = self.approver(request["name"], request["args"])
                    self.trace.append({"tool": "approval", "args": request, "output": "approved" if approved else "rejected"})
                    decisions.append({"type": "approve"} if approved else
                                     {"type": "reject", "message": "The user did not approve adding this document."})
            result = await self.agent.ainvoke(Command(resume={"decisions": decisions}), cfg)
        return result

    async def ask(self, question: str) -> dict:
        from langchain_core.messages import AIMessage

        self.trace = []
        cfg = {"configurable": {"thread_id": str(uuid.uuid4())}}
        started = time.time()
        result = await self._run({"messages": [{"role": "user", "content": question}]}, cfg)
        answer = final_text(result)
        guardrail = []

        problem = self.citation_problem(answer)
        if problem:
            guardrail.append({"fired": True, "attempt": 1, "problem": problem, "answer": answer})
            fix = (f"Tu respuesta no pasa la comprobación de citas: {problem} Reescríbela usando solo citas "
                   f"[source, location] que aparezcan en los resultados de search, o responde exactamente "
                   f"'{config.REFUSAL}'")
            result = await self._run({"messages": [{"role": "user", "content": fix}]}, cfg)
            answer = final_text(result)
            problem = self.citation_problem(answer)
            if problem:
                guardrail.append({"fired": True, "attempt": 2, "problem": problem, "answer": answer})
                answer = f"{config.REFUSAL} (Respuesta retirada: {problem})"

        usage = {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}
        model_calls = 0
        for message in result["messages"]:
            if isinstance(message, AIMessage):
                model_calls += 1
                for key in usage:
                    usage[key] += (message.usage_metadata or {}).get(key, 0)
        return {
            "question": question,
            "answer": answer,
            "citations": citations_in(answer),
            "retrieved": self.retrieved(),
            "refused": is_refusal(answer),
            "trace": self.trace,
            "guardrail": guardrail,
            "tokens": usage,
            "model_calls": model_calls,
            "searches": sum(1 for t in self.trace if t["tool"] == "search"),
            "seconds": round(time.time() - started, 1),
        }

    def retrieved(self) -> list[tuple[str, str]]:
        found = []
        for t in self.trace:
            if t["tool"] == "search":
                found += RETURNED.findall(t["output"])
        return list(dict.fromkeys((s, l.strip()) for s, l in found))

    def citation_problem(self, answer: str) -> str | None:
        """Why this answer fails the citation check, or None if it passes. Only answers about
        the corpus are checked: a refusal, or the report of an add_document request, cites nothing."""
        if is_refusal(answer) or any(t["tool"] in {"add_document", "approval"} for t in self.trace):
            return None
        cited = citations_in(answer)
        if not cited:
            return "no cita ninguna fuente."
        returned = set(self.retrieved())
        invalid = [c for c in cited if c not in returned]
        if invalid:
            return "cita fuentes que la búsqueda no devolvió: " + ", ".join(f"[{s}, {l}]" for s, l in invalid) + "."
        return None


def final_text(result: dict) -> str:
    from langchain_core.messages import AIMessage

    for message in reversed(result["messages"]):
        if isinstance(message, AIMessage) and not message.tool_calls:
            return (message.text or "").strip()
    return config.REFUSAL + " (El agente agotó el límite de llamadas sin responder.)"


async def ask_once(question: str) -> dict:
    async with Agent() as agent:
        return await agent.ask(question)


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit('usage: python agent.py "your question"')
    out = asyncio.run(ask_once(" ".join(sys.argv[1:])))
    print(out["answer"])
    if out["citations"]:
        print("\nFuentes citadas:")
        for source, location in out["citations"]:
            print(f"- {source}, {location}")
    for event in out["guardrail"]:
        print(f"\n[guardrail] citation check fired (attempt {event['attempt']}): {event['problem']}", file=sys.stderr)
    print(f"\n({out['searches']} searches, {out['model_calls']} model calls, "
          f"{out['tokens']['total_tokens']} tokens, {out['seconds']} s)")


if __name__ == "__main__":
    main()
