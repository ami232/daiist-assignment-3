"""
Assignment 3: your agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the tools of server.py over MCP and
AGENTS.md as system prompt.

Harness features
  * approval: add_document only runs if `approve(tool, args)` says yes
    (default: ask in the terminal; with no terminal the answer is no)
  * call limit: at most RUN_LIMIT tool calls per question (ToolCallLimitMiddleware)
  * guardrail: every citation `[Source, Location]` in the answer is checked in
    code against the passages the search tool really returned; unverified
    citations are reported and flagged in the answer
  * `ask(question)` / `Harness.ask(question)` return the answer AND the tool
    trace (plus tokens and seconds) for evaluate.py

stdout: only the answer. Everything else goes to stderr.
"""

import asyncio
import os
import re
import sys
import time
from contextlib import AsyncExitStack
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MODEL = os.environ.get("AGENT_MODEL", "gemini-3.5-flash-lite")  # gemini-3.5-flash timed out (504) on the free tier
RUN_LIMIT = int(os.environ.get("RUN_LIMIT", "6"))
GUARDED_TOOL = "add_document"


def log(*args) -> None:
    if not os.environ.get("AGENT_QUIET"):
        print(*args, file=sys.stderr, flush=True)


# --------------------------------------------------------------------------
# Pure functions (no API): citation guardrail
# --------------------------------------------------------------------------
_CITATION = re.compile(r"\[([^\[\]|]+?),\s*((?:Article|Annex)\s+[^\[\]|]+?)\]")
_PASSAGE_HEAD = re.compile(r"^\[\d+\]\s+(.+?)\s+\|\s+(.+?)\s+\|", re.MULTILINE)
_UNIT = re.compile(r"(Article|Annex)\s+([0-9]+|[IVXLC]+)")


def _unit(location: str) -> str | None:
    m = _UNIT.search(location)
    return f"{m.group(1)} {m.group(2)}" if m else None


def retrieved_units(trace: list[dict]) -> set[tuple[str, str]]:
    """(source, 'Article N') pairs the search results really contained."""
    found = set()
    for call in trace:
        if call["tool"] != "search":
            continue
        for source, location in _PASSAGE_HEAD.findall(call["result"]):
            if (u := _unit(location)):
                found.add((source.strip(), u))
    return found


def check_citations(answer: str, trace: list[dict]) -> tuple[list[str], list[str]]:
    """Return (all citations, those not backed by a retrieved passage)."""
    have = retrieved_units(trace)
    cited, bad = [], []
    for source, location in _CITATION.findall(answer):
        label = f"[{source.strip()}, {location.strip()}]"
        cited.append(label)
        if (source.strip(), _unit(location) or "") not in have:
            bad.append(label)
    return cited, bad


def flag_answer(answer: str, bad: list[str]) -> str:
    if not bad:
        return answer
    return (answer.rstrip() + "\n\n[guardrail] These citations do not match any retrieved passage; "
            "do not rely on them: " + ", ".join(dict.fromkeys(bad)))


def default_approve(tool: str, args: dict) -> bool:
    """Ask the person in the terminal. Without a terminal, refuse."""
    if not sys.stdin.isatty():
        log(f"[approval] {tool}({args}) needs approval and there is no terminal: refused")
        return False
    log(f"\n[approval] The agent wants to run {tool} with {args}. It changes the index.")
    return input("Allow? [y/N] ").strip().lower() in ("y", "yes", "s", "si", "sí")


def _text(message) -> str:
    return str(message.text)


# --------------------------------------------------------------------------
# Harness
# --------------------------------------------------------------------------
class Harness:
    """Starts server.py over stdio and builds the agent. Use as `async with Harness() as h`."""

    def __init__(self, approve=default_approve, model: str = MODEL, run_limit: int = RUN_LIMIT):
        self.approve, self.model, self.run_limit = approve, model, run_limit
        self.trace: list[dict] = []

    async def __aenter__(self):
        self._stack = AsyncExitStack()
        try:
            return await self._start()
        except BaseException:
            await self._stack.aclose()  # stop server.py, otherwise shutdown hangs and hides the error
            raise

    async def _start(self):
        from langchain.agents import create_agent
        from langchain.agents.middleware.tool_call_limit import ToolCallLimitMiddleware
        from langchain_core.tools import StructuredTool
        from langchain_google_genai import ChatGoogleGenerativeAI
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client

        from api_key import load_api_key

        params = StdioServerParameters(
            command=sys.executable, args=[str(ROOT / "server.py")], cwd=str(ROOT), env=dict(os.environ),
        )
        log("[harness] starting server.py ...")
        read, write = await self._stack.enter_async_context(stdio_client(params))
        self._session = await self._stack.enter_async_context(ClientSession(read, write))
        await self._session.initialize()
        mcp_tools = (await self._session.list_tools()).tools
        log("[harness] server tools:", ", ".join(t.name for t in mcp_tools))

        def wrap(t):
            async def run(**kwargs) -> str:
                entry = {"tool": t.name, "args": kwargs, "approved": None, "result": ""}
                self.trace.append(entry)
                log(f"[tool call] {t.name}({kwargs})")
                if t.name == GUARDED_TOOL:
                    entry["approved"] = bool(await asyncio.to_thread(self.approve, t.name, kwargs))
                    if not entry["approved"]:
                        entry["result"] = ("The approval prompt was declined, so the document was NOT added and the index is unchanged. "
                                           "Tell the user it was not added because the approval was declined. Do not retry.")
                        return entry["result"]
                result = await self._session.call_tool(t.name, kwargs)
                entry["result"] = "\n".join(getattr(c, "text", "") for c in result.content).strip()
                return entry["result"]

            return StructuredTool(
                name=t.name, description=t.description or "", args_schema=t.input_schema, coroutine=run,
            )

        log("[harness] building model ...")
        llm = ChatGoogleGenerativeAI(model=self.model, api_key=load_api_key(), max_retries=2, timeout=60)
        log("[harness] building agent ...")
        self.agent = create_agent(
            llm, [wrap(t) for t in mcp_tools],
            system_prompt=(ROOT / "AGENTS.md").read_text(encoding="utf-8"),
            middleware=[ToolCallLimitMiddleware(run_limit=self.run_limit, exit_behavior="end")],
        )
        log("[harness] ready")
        return self

    async def __aexit__(self, *exc):
        await self._stack.aclose()

    async def ask(self, question: str) -> dict:
        """Return {question, answer, trace, citations, unverified_citations, tokens, seconds, limit_hit}."""
        self.trace = []
        started = time.time()
        state = None
        log("[harness] asking the model ...")
        async for state in self.agent.astream(
            {"messages": [{"role": "user", "content": question}]}, stream_mode="values"
        ):
            last = state["messages"][-1]
            log(f"[step] {type(last).__name__} ({time.time() - started:.1f}s)")
        seconds = time.time() - started
        tokens = {"input": 0, "output": 0}
        for m in state["messages"]:
            usage = getattr(m, "usage_metadata", None)
            if usage:
                tokens["input"] += usage.get("input_tokens", 0)
                tokens["output"] += usage.get("output_tokens", 0)
        raw = _text(state["messages"][-1]).strip()
        cited, bad = check_citations(raw, self.trace)
        return {
            "question": question, "answer": flag_answer(raw, bad), "raw_answer": raw,
            "trace": self.trace, "citations": cited, "unverified_citations": bad,
            "tokens": tokens, "seconds": round(seconds, 1),
            "limit_hit": len(self.trace) >= self.run_limit,
        }


async def ask_async(question: str, approve=default_approve) -> dict:
    async with Harness(approve=approve) as h:
        return await h.ask(question)


def ask(question: str, approve=default_approve) -> dict:
    """Synchronous helper: answer + tool trace."""
    return asyncio.run(ask_async(question, approve))


def main() -> None:
    if os.environ.get("AGENT_DEBUG"):
        import faulthandler

        faulthandler.dump_traceback_later(40, exit=False)  # where is it waiting?
    if len(sys.argv) < 2:
        raise SystemExit('usage: python agent.py "your question"')
    result = ask(" ".join(sys.argv[1:]))
    log(f"[{result['tokens']['input']} in / {result['tokens']['output']} out tokens, {result['seconds']}s]")
    print(result["answer"])


if __name__ == "__main__":
    main()
