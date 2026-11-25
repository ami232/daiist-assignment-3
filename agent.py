"""
Assignment 3: your agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the tools of server.py over MCP and
AGENTS.md as the system prompt.

Guardrails (every one is logged in the result, so evaluate.py can count them):
  1. approval  - add_document never runs without a yes from the person.
  2. call limit - at most MAX_TOOL_CALLS tool calls per question.
  3. citation check - an answer must cite only sources the agent actually
     retrieved. If it does not, the agent gets ONE chance to rewrite it, and
     if it still does not, the answer is returned with a warning.

`ask(question)` returns the answer and the tool trace, for evaluate.py.
"""

import asyncio
import os
import re
import sys
import threading
import time
from concurrent.futures import Future
from pathlib import Path

os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")

ROOT = Path(__file__).resolve().parent
MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite")
MAX_TOOL_CALLS = 6
SOURCE_RE = re.compile(r"CONTRACT_\d{3}\.pdf")
REFUSAL_PREFIX = "NOT IN CORPUS"      # AGENTS.md tells the model to start refusals with this


# --------------------------------------------------------------------------
# MCP client: starts server.py over stdio once and keeps the session open
# --------------------------------------------------------------------------

class McpServer:
    """server.py as a subprocess, spoken to over MCP, callable from synchronous code."""

    def __init__(self) -> None:
        self._loop = asyncio.new_event_loop()
        self._thread = threading.Thread(target=self._loop.run_forever, daemon=True)
        self._thread.start()
        self._ready: Future = Future()
        self._stop: asyncio.Event | None = None
        self.tools: list = []
        self._session = None
        asyncio.run_coroutine_threadsafe(self._main(), self._loop)
        self._ready.result(timeout=120)

    async def _main(self) -> None:
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client

        params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT))
        try:
            async with stdio_client(params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    self.tools = (await session.list_tools()).tools
                    self._session = session
                    self._stop = asyncio.Event()
                    self._ready.set_result(True)
                    await self._stop.wait()
        except Exception as error:  # noqa: BLE001
            if not self._ready.done():
                self._ready.set_exception(error)

    def call(self, name: str, arguments: dict) -> str:
        async def _call() -> str:
            result = await self._session.call_tool(name, arguments)
            return "\n".join(getattr(c, "text", "") for c in result.content).strip()
        return asyncio.run_coroutine_threadsafe(_call(), self._loop).result(timeout=300)

    def close(self) -> None:
        if self._stop is not None:
            self._loop.call_soon_threadsafe(self._stop.set)
        time.sleep(0.2)


# --------------------------------------------------------------------------
# Guardrails
# --------------------------------------------------------------------------

def interactive_approval(tool: str, arguments: dict) -> bool:
    """Ask the person in the terminal. Without a terminal (evaluation, CI) the answer is no."""
    if not sys.stdin.isatty():
        return False
    print(f"\nThe agent wants to run {tool}({arguments}). It will change the index.", file=sys.stderr)
    return input("Approve? [y/N] ").strip().lower() in ("y", "yes", "s", "si", "sí")


def check_citations(answer: str, trace: list[dict]) -> list[str]:
    """Problems with the citations of an answer; [] when it is fine."""
    if answer.strip().upper().startswith(REFUSAL_PREFIX):
        return []
    retrieved = set()
    for step in trace:
        if step["tool"] in ("search", "add_document"):      # add_document names the file it just indexed
            retrieved |= set(SOURCE_RE.findall(step["result"]))
    cited = set(SOURCE_RE.findall(answer))
    if not cited:
        return ["the answer cites no source"]
    return [f"{c} was cited but never retrieved" for c in sorted(cited - retrieved)]


# --------------------------------------------------------------------------
# The agent
# --------------------------------------------------------------------------

def build_tools(server: McpServer, trace: list[dict], approve, events: list[str]):
    """LangChain tools for the MCP tools, with the approval and the call limit around them."""
    from langchain_core.tools import StructuredTool

    def make(tool):
        def run(**arguments) -> str:
            if len(trace) >= MAX_TOOL_CALLS:
                events.append("call_limit")
                result = (f"TOOL-CALL LIMIT REACHED ({MAX_TOOL_CALLS}). Do not call more tools: answer with "
                          f"what you have, or say {REFUSAL_PREFIX}.")
            elif tool.name == "add_document" and not approve(tool.name, arguments):
                events.append("add_document_denied")
                result = "DENIED: the person did not approve add_document. Tell them nothing was added."
            else:
                if tool.name == "add_document":
                    events.append("add_document_approved")
                result = server.call(tool.name, arguments)
            trace.append({"tool": tool.name, "arguments": arguments, "result": result})
            return result

        return StructuredTool.from_function(
            func=run, name=tool.name, description=tool.description or tool.name, args_schema=tool.input_schema,
        )

    return [make(t) for t in server.tools]


def message_text(message) -> str:
    text = getattr(message, "text", None)
    if isinstance(text, str):
        return text
    content = message.content
    return content if isinstance(content, str) else "".join(p.get("text", "") for p in content if isinstance(p, dict))


def ask(question: str, approve=interactive_approval, server: McpServer | None = None, model=None) -> dict:
    """Answer one question. Returns {"answer", "trace", "events", "input_tokens", "output_tokens", "seconds"}."""
    from langchain.agents import create_agent
    from langchain_core.messages import HumanMessage
    from api_key import load_api_key

    started = time.time()
    own_server = server is None
    server = server or McpServer()
    trace: list[dict] = []
    events: list[str] = []
    try:
        if model is None:
            from langchain_google_genai import ChatGoogleGenerativeAI
            model = ChatGoogleGenerativeAI(model=MODEL, google_api_key=load_api_key())
        agent = create_agent(
            model, build_tools(server, trace, approve, events),
            system_prompt=(ROOT / "AGENTS.md").read_text(encoding="utf-8"),
        )
        messages = [HumanMessage(question)]
        result = agent.invoke({"messages": messages})
        answer = message_text(result["messages"][-1])

        problems = check_citations(answer, trace)
        if problems:                                            # guardrail 3: one chance to fix it
            events.append("citation_retry")
            retry = result["messages"] + [HumanMessage(
                "Your answer breaks the citation rule: " + "; ".join(problems) + ". Rewrite it citing only "
                f"passages you retrieved as [CONTRACT_xxx.pdf | clause], or start with '{REFUSAL_PREFIX}:' "
                "if the corpus does not say.")]
            result = agent.invoke({"messages": retry})
            answer = message_text(result["messages"][-1])
            problems = check_citations(answer, trace)
            if problems:
                events.append("citation_failed")
                answer = f"[WARNING: unverified citations: {'; '.join(problems)}]\n{answer}"

        usage = [m.usage_metadata for m in result["messages"] if getattr(m, "usage_metadata", None)]
        return {
            "answer": answer, "trace": trace, "events": events,
            "input_tokens": sum(u.get("input_tokens", 0) for u in usage),
            "output_tokens": sum(u.get("output_tokens", 0) for u in usage),
            "seconds": time.time() - started,
        }
    finally:
        if own_server:
            server.close()


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit('usage: python agent.py "your question"')
    out = ask(" ".join(sys.argv[1:]))
    print(out["answer"])
    print(f"\n[{len(out['trace'])} tool calls, {out['input_tokens']}+{out['output_tokens']} tokens, "
          f"{out['seconds']:.1f}s{', guardrails: ' + ', '.join(out['events']) if out['events'] else ''}]",
          file=sys.stderr)
