"""
Assignment 3: my agent (`main.py ask "question"` runs `python agent.py "question"`).

A LangChain `create_agent` on Gemini. The tools come from server.py over MCP, so the
agent uses exactly the tools an editor would. AGENTS.md is the system prompt.

Three controls sit between the model and the tools (the "harness"):
  1. Approval: `add_document` changes the index, so a person must approve each call.
     Without a person (evaluation, pipes) the call is denied.
  2. Call limit: at most MAX_TOOL_CALLS tool calls per question, so a confused model
     cannot loop and spend quota.
  3. Citation guardrail (my own): every `[source | location]` in the answer must be a
     citation that a search result in THIS run offered. A wrong citation gets one repair
     turn; if it is still wrong it is removed and the answer is marked. An answer given
     without any search gets one turn to search first.

`evaluate.py` imports `Agent` and reads the answer, the citations and the tool trace.
"""

import asyncio
import os
import re
import sys
import threading
import time
from pathlib import Path

from langchain.agents import create_agent
from langchain_core.tools import StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import Field, create_model
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
MODEL = os.environ.get("AGENT_MODEL", "gemini-3.5-flash-lite")
MAX_TOOL_CALLS = 6
RECURSION_LIMIT = 25
PROMPT_FILE = ROOT / "AGENTS.md"

CITE_OFFERED = re.compile(r"cite as \[([^\]]+)\]")  # in search results
CITE_USED = re.compile(r"\[([^\[\]|]+\|[^\[\]]+)\]")  # in answers: [source | location]


def log(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


def norm(citation: str) -> str:
    """Compare citations without caring about spaces or case."""
    return re.sub(r"\s+", " ", citation).strip().lower()


def parse_location(citation: str):
    """('source', kind, value): lets 'Article 4(1)' count as inside an offered 'Article 4'."""
    source, _, location = (part.strip() for part in citation.partition("|"))
    m = re.match(r"(?i)article\s+(\d+[a-z]?)", location)
    if m:
        return source.lower(), "article", m.group(1).lower()
    m = re.match(r"(?i)annex\s+([ivxl]+)", location)
    if m:
        return source.lower(), "annex", m.group(1).lower()
    numbers = [int(n) for n in re.findall(r"\((\d+)\)", location)]
    if location.lower().startswith("paragraph") and numbers:
        return source.lower(), "paragraphs", (min(numbers), max(numbers))
    return source.lower(), "text", norm(location)


def is_offered(cited: str, offered: set[str]) -> bool:
    """A citation is valid if a search result of this run covers it (same article, annex or paragraph)."""
    if norm(cited) in offered:
        return True
    source, kind, value = parse_location(cited)
    for other in offered:
        o_source, o_kind, o_value = parse_location(other)
        if o_source != source or o_kind != kind:
            continue
        if kind == "paragraphs" and o_value[0] <= value[0] and value[1] <= o_value[1]:
            return True
        if kind in ("article", "annex") and o_value == value:
            return True
    return False


class McpBridge:
    """Runs server.py as a subprocess and lets synchronous code call its tools."""

    def __init__(self) -> None:
        self.loop = asyncio.new_event_loop()
        self.session: ClientSession | None = None
        self.tools = []
        self._ready = threading.Event()
        self._stop: asyncio.Event | None = None
        self._error: BaseException | None = None
        self.thread = threading.Thread(target=self._run, daemon=True)
        self.thread.start()
        self._ready.wait(timeout=120)
        if self._error:
            raise RuntimeError(f"Could not start server.py: {self._error}") from self._error
        if self.session is None:
            raise RuntimeError("server.py did not start within 120 seconds")

    def _run(self) -> None:
        asyncio.set_event_loop(self.loop)
        self.loop.run_until_complete(self._main())

    async def _main(self) -> None:
        self._stop = asyncio.Event()
        params = StdioServerParameters(
            command=sys.executable,
            args=[str(ROOT / "server.py")],
            cwd=ROOT,
            env=dict(os.environ),
        )
        try:
            async with stdio_client(params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    self.tools = (await session.list_tools()).tools
                    self.session = session
                    self._ready.set()
                    await self._stop.wait()
        except BaseException as error:  # noqa: BLE001 - reported to the caller
            self._error = error
            self._ready.set()

    def call(self, name: str, arguments: dict) -> str:
        future = asyncio.run_coroutine_threadsafe(
            self.session.call_tool(name, arguments), self.loop
        )
        result = future.result(timeout=600)
        text = "\n".join(getattr(part, "text", "") for part in result.content)
        return f"Error: {text}" if (getattr(result, "is_error", False) or getattr(result, "isError", False)) else text

    def close(self) -> None:
        if self._stop is not None:
            self.loop.call_soon_threadsafe(self._stop.set)
        self.thread.join(timeout=15)


def ask_person(path: str) -> bool:
    """Default approval: ask on the terminal; deny when nobody can answer."""
    if not sys.stdin or not sys.stdin.isatty():
        log(f"[approval] add_document({path!r}) denied: no person to ask.")
        return False
    answer = input(f"\nThe agent wants to add this document to the index: {path}\nAllow? [y/N] ")
    return answer.strip().lower() in ("y", "yes", "s", "si", "sí")


class Agent:
    """One MCP server, one LangChain agent, many questions."""

    def __init__(self, approve=ask_person, model: str = MODEL, verbose: bool = True) -> None:
        self.approve = approve
        self.verbose = verbose
        self.bridge = McpBridge()
        self.trace: list[dict] = []
        self.offered: set[str] = set()  # citations offered by searches in this run
        self.calls = 0
        llm = ChatGoogleGenerativeAI(
            model=model, api_key=load_api_key(), temperature=0, max_retries=6
        )
        self.agent = create_agent(
            llm, self._make_tools(), system_prompt=PROMPT_FILE.read_text(encoding="utf-8")
        )

    # -- tools -------------------------------------------------------------
    def _make_tools(self) -> list:
        tools = []
        for spec in self.bridge.tools:
            props = spec.input_schema.get("properties", {})
            arg = next(iter(props), "query")
            # The model sees the MCP tool's own argument name and description.
            schema = create_model(
                f"{spec.name}_args", **{arg: (str, Field(description=props.get(arg, {}).get("description", arg)))}
            )
            tools.append(
                StructuredTool.from_function(
                    func=self._wrap(spec.name, arg),
                    name=spec.name,
                    description=spec.description or spec.name,
                    args_schema=schema,
                )
            )
        return tools

    def _wrap(self, name: str, arg: str):
        def run(**kwargs) -> str:
            value = kwargs[arg]
            started = time.time()
            self.calls += 1
            if self.calls > MAX_TOOL_CALLS:
                output = (
                    f"Tool call limit reached ({MAX_TOOL_CALLS}). Answer now with what you "
                    "already have, or say that the indexed documents do not cover it."
                )
            elif name == "add_document" and not self.approve(value):
                output = "The user did not approve adding this document. Do not retry."
            else:
                output = self.bridge.call(name, {arg: value})
                if name == "search":
                    self.offered.update(norm(c) for c in CITE_OFFERED.findall(output))
            self.trace.append(
                {"tool": name, "args": {arg: value}, "output": output,
                 "seconds": round(time.time() - started, 2)}
            )
            if self.verbose:
                log(f"[tool] {name}({value!r}) -> {len(output)} characters")
            return output

        return run

    # -- one question ------------------------------------------------------
    def _invoke(self, messages: list) -> tuple[list, str]:
        result = self.agent.invoke(
            {"messages": messages}, config={"recursion_limit": RECURSION_LIMIT}
        )
        messages = result["messages"]
        return messages, str(messages[-1].text).strip()

    @staticmethod
    def _usage(messages: list) -> tuple[int, int]:
        tokens_in = tokens_out = 0
        for message in messages:
            usage = getattr(message, "usage_metadata", None) or {}
            tokens_in += usage.get("input_tokens", 0)
            tokens_out += usage.get("output_tokens", 0)
        return tokens_in, tokens_out

    def ask(self, question: str) -> dict:
        self.trace, self.offered, self.calls = [], set(), 0
        started = time.time()
        guardrail = "ok"
        messages = [{"role": "user", "content": question}]
        messages, answer = self._invoke(messages)

        searched = any(step["tool"] == "search" for step in self.trace)
        invalid = [c for c in CITE_USED.findall(answer) if not is_offered(c, self.offered)]
        if not searched or invalid:
            if not searched:
                feedback = "You answered without calling `search`. Call `search` first and answer only from its results."
                guardrail = "repaired_no_search"
            else:
                feedback = (
                    "These citations were not in the search results: "
                    + "; ".join(f"[{c}]" for c in invalid)
                    + ". Rewrite the answer using only citations exactly as given after 'cite as' "
                    "in the results, and drop any claim you cannot support."
                )
                guardrail = "repaired_citations"
            messages.append({"role": "user", "content": feedback})
            messages, answer = self._invoke(messages)
            invalid = [c for c in CITE_USED.findall(answer) if not is_offered(c, self.offered)]
            if invalid or not any(step["tool"] == "search" for step in self.trace):
                for citation in invalid:
                    answer = answer.replace(f"[{citation}]", "[citation removed: not in search results]")
                guardrail = "citations_removed"

        tokens_in, tokens_out = self._usage(messages)
        return {
            "question": question,
            "answer": answer,
            "citations": [c.strip() for c in CITE_USED.findall(answer)],
            "trace": list(self.trace),
            "tool_calls": self.calls,
            "guardrail": guardrail,
            "input_tokens": tokens_in,
            "output_tokens": tokens_out,
            "seconds": round(time.time() - started, 1),
        }

    def close(self) -> None:
        self.bridge.close()

    def __enter__(self) -> "Agent":
        return self

    def __exit__(self, *exc) -> None:
        self.close()


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    question = " ".join(sys.argv[1:]).strip()
    if not question:
        raise SystemExit('Usage: python agent.py "your question"')
    with Agent() as agent:
        result = agent.ask(question)
    print(result["answer"])
    log(
        f"\n[{result['tool_calls']} tool calls, guardrail: {result['guardrail']}, "
        f"{result['input_tokens']}+{result['output_tokens']} tokens, {result['seconds']} s]"
    )


if __name__ == "__main__":
    main()
