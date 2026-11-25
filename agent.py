"""
Assignment 3: your agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the tools of server.py over MCP and
AGENTS.md as the system prompt. Guardrails, all in code:

  1. Approval: add_document never runs without a "yes" from the person at the
     terminal (no terminal, or no answer: it does not run).
  2. Call limit: at most MAX_TOOL_CALLS tool calls per question.
  3. Citation check (the extra guardrail): an answer must cite passages it
     really retrieved, as [Source | Location], or say that the corpus does not
     cover the question. One retry; if it still fails, the answer is replaced
     by a refusal.

Use from code (evaluate.py does):

    async with Harness() as harness:
        result = await harness.ask("question")   # answer, tool trace, retrieved passages, tokens, seconds

    python agent.py "question"            # prints the answer
    python agent.py --list-models         # which Gemini chat models your key can use
    CHAT_MODEL=<name> python agent.py ... # force a model (also settable in .env)
"""

import asyncio
import os
import re
import sys
import time
from pathlib import Path

from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.tools import StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
SYSTEM_PROMPT_FILE = ROOT / "AGENTS.md"

REFUSAL = "The corpus does not cover this."
MAX_TOOL_CALLS = 6  # guardrail 2
# The lite models answer in seconds on the free tier; the larger flash models often time out (504) when Google is busy.
MODEL_PREFERENCE = ["gemini-3.1-flash-lite", "gemini-flash-lite-latest", "gemini-3.5-flash-lite"]

CITATION = re.compile(r"\[([^\[\]|]+?)\s*\|\s*([^\[\]]+?)\]")
RESULT_HEADER = re.compile(r"^\[(\d+)\] (.*?) \| (.*) \(similarity (-?[\d.]+)\)$")


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


# ---------------------------------------------------------------------------
# Model
# ---------------------------------------------------------------------------
def available_chat_models() -> list[str]:
    from google import genai

    client = genai.Client(api_key=load_api_key())
    names = []
    for model in client.models.list():
        if "generateContent" in (getattr(model, "supported_actions", None) or []):
            names.append(model.name.removeprefix("models/"))
    return sorted(names)


def with_timeout(function, seconds: float):
    """Run a blocking call in a thread and stop waiting for it after `seconds` (raises TimeoutError)."""
    from concurrent.futures import ThreadPoolExecutor

    pool = ThreadPoolExecutor(max_workers=1)
    try:
        return pool.submit(function).result(timeout=seconds)
    finally:
        pool.shutdown(wait=False, cancel_futures=True)


def candidate_models() -> list[str]:
    """Plain 'flash' models your key lists, newest version first, then the fallbacks.
    A model can be listed and still refuse new users, so pick_model_name() tries them."""
    log("listing the Gemini models your key can use ...")
    try:
        listed = with_timeout(available_chat_models, 25)
    except Exception as error:  # noqa: BLE001
        log(f"could not list models ({type(error).__name__}: {str(error)[:100]}); trying the built-in names")
        listed = []
    flash = []
    for name in listed:
        match = re.fullmatch(r"gemini-(\d+(?:\.\d+)?)-flash", name)
        if match:
            flash.append((tuple(int(part) for part in match.group(1).split(".")), name))
    ordered = [name for _, name in sorted(flash, reverse=True)]
    return MODEL_PREFERENCE + [name for name in ordered if name not in MODEL_PREFERENCE]


_working_model: str | None = None


def pick_model_name() -> str:
    """The first chat model that really answers (one tiny test call each). Set CHAT_MODEL in .env to force one."""
    global _working_model
    forced = os.environ.get("CHAT_MODEL", "").strip()
    if forced:
        return forced
    if _working_model:
        return _working_model
    load_api_key()
    for name in candidate_models():
        log(f"testing model {name} ...")
        try:
            probe = ChatGoogleGenerativeAI(model=name, temperature=0, max_retries=1, timeout=40)
            with_timeout(lambda: probe.invoke("Reply with the word ok."), 50)
        except TimeoutError:
            log(f"model {name} did not answer within 50 seconds (rate limit or network); trying the next one")
            continue
        except Exception as error:  # noqa: BLE001
            message = str(error)
            if "429" in message or "RESOURCE_EXHAUSTED" in message:  # it exists, it is only busy
                _working_model = name
                return name
            if "NOT_FOUND" in message or "404" in message or "no longer available" in message:
                log(f"model {name} is not available to this key, trying the next one")
                continue
            raise
        _working_model = name
        log(f"using chat model {name}")
        return name
    raise SystemExit("No Gemini chat model worked with your key. Run `uv run python agent.py --list-models` and set CHAT_MODEL=<name> in .env.")


# ---------------------------------------------------------------------------
# Checks (plain code, also used by evaluate.py)
# ---------------------------------------------------------------------------
def parse_search_result(text: str) -> list[dict]:
    """The passages in a search tool result: source, location, similarity, text."""
    passages = []
    for block in re.split(r"\n\n(?=\[\d+\] )", text.strip()):
        header, _, body = block.partition("\n")
        match = RESULT_HEADER.match(header.strip())
        if match:
            passages.append({"source": match.group(2), "location": match.group(3), "similarity": float(match.group(4)), "text": body.strip()})
    return passages


def is_refusal(answer: str) -> bool:
    return REFUSAL.lower().rstrip(".") in answer.strip()[:160].lower()


def citations_of(answer: str) -> list[tuple[str, str]]:
    return [(s.strip(), l.strip()) for s, l in CITATION.findall(answer)]


def citation_problems(answer: str, retrieved: list[dict]) -> list[str]:
    """Why this answer's citations are not acceptable (an empty list: they are)."""
    if is_refusal(answer):
        return []
    cited = citations_of(answer)
    if not cited:
        return ["the answer cites nothing"]
    problems = []
    for source, location in cited:
        found = any(
            p["source"].lower() == source.lower() and (location.lower() in p["location"].lower() or p["location"].lower() in location.lower())
            for p in retrieved
        )
        if not found:
            problems.append(f"[{source} | {location}] is not a passage that search returned")
    return problems


def message_text(message) -> str:
    text = getattr(message, "text", None)  # a str-like property in current langchain
    if isinstance(text, str) and text:
        return str(text)
    content = message.content
    if isinstance(content, str):
        return content
    return "".join(part.get("text", "") if isinstance(part, dict) else str(part) for part in content)


# ---------------------------------------------------------------------------
# Harness
# ---------------------------------------------------------------------------
async def terminal_approval(path: str) -> bool:
    if not sys.stdin or not sys.stdin.isatty():
        log("add_document needs approval but there is no terminal: not run.")
        return False
    answer = await asyncio.to_thread(input, f"\nThe agent wants to add this file to the corpus:\n  {path}\nAllow? [y/N] ")
    return answer.strip().lower() in ("y", "yes")


class Harness:
    """Starts server.py over MCP, builds the agent, answers questions one at a time."""

    def __init__(self, approve=terminal_approval, model=None, server_script: str = "server.py"):
        self.approve = approve
        self._model = model
        self.server_script = server_script
        self.state: dict = {}

    async def __aenter__(self):
        load_api_key()
        log("starting the search server ...")
        self.stack = await _AsyncStack().__aenter__()
        params = StdioServerParameters(command=sys.executable, args=[self.server_script], cwd=str(ROOT))
        read, write = await self.stack.enter(stdio_client(params))
        self.session = await self.stack.enter(ClientSession(read, write))
        await self.session.initialize()
        mcp_tools = (await self.session.list_tools()).tools
        self.tools = [self._wrap(tool) for tool in mcp_tools]
        self.model_name = "custom" if self._model else pick_model_name()
        log(f"tools ready: {', '.join(t.name for t in self.tools)}; chat model: {self.model_name}")
        model = self._model or ChatGoogleGenerativeAI(model=self.model_name, temperature=0, max_retries=2, timeout=60)
        self.agent = create_agent(model, self.tools, system_prompt=SYSTEM_PROMPT_FILE.read_text(encoding="utf-8"))
        return self

    async def __aexit__(self, *exc):
        await self.stack.__aexit__(*exc)

    def _wrap(self, mcp_tool) -> StructuredTool:
        name = mcp_tool.name

        async def run(**arguments) -> str:
            state = self.state
            started = time.time()
            if state["calls"] >= MAX_TOOL_CALLS:  # guardrail 2
                result = "Tool call limit reached. Answer now using only what you have already retrieved, or say that the corpus does not cover the question."
            elif name == "add_document" and not await self.approve(arguments.get("path", "")):  # guardrail 1
                result = "The person did not approve adding this document, so it was not added."
                state["calls"] += 1
            else:
                state["calls"] += 1
                reply = await self.session.call_tool(name, arguments)
                result = "\n".join(getattr(part, "text", "") for part in reply.content).strip()
                if name == "search":
                    state["retrieved"] += parse_search_result(result)
            log(f"  tool {name}({str(arguments)[:90]}) finished in {time.time() - started:.1f}s")
            state["trace"].append({"tool": name, "args": arguments, "result": result, "seconds": round(time.time() - started, 2)})
            return result

        schema = getattr(mcp_tool, "input_schema", None) or getattr(mcp_tool, "inputSchema", None)
        return StructuredTool.from_function(coroutine=run, name=name, description=mcp_tool.description or "", args_schema=schema, infer_schema=False)

    async def _run_agent(self, messages: list) -> list:
        log("asking the model ...")
        try:
            output = await asyncio.wait_for(self.agent.ainvoke({"messages": messages}, {"recursion_limit": 3 * MAX_TOOL_CALLS + 8}), timeout=240)
        except asyncio.TimeoutError as error:
            raise RuntimeError("The model did not answer within 240 seconds (probably the free-tier rate limit). Try again in a minute.") from error
        return output["messages"]

    async def ask(self, question: str) -> dict:
        self.state = {"calls": 0, "trace": [], "retrieved": []}
        started = time.time()
        messages = await self._run_agent([HumanMessage(question)])
        answer = message_text(messages[-1]).strip()
        guardrail = None
        problems = citation_problems(answer, self.state["retrieved"])
        if problems:  # guardrail 3, first chance: ask once for a corrected answer
            guardrail = "citation check failed: " + "; ".join(problems)
            fix = (
                f"Your answer cannot be accepted: {'; '.join(problems)}. Answer again. Cite only passages that search "
                f"returned, as [Source | Location] copied from the result header, or start with: {REFUSAL}"
            )
            messages = await self._run_agent(messages + [HumanMessage(fix)])
            answer = message_text(messages[-1]).strip()
            problems = citation_problems(answer, self.state["retrieved"])
            if problems:  # second failure: replace the answer
                guardrail += " | retry failed, answer replaced"
                answer = f"{REFUSAL} (The draft answer was withheld because its citations could not be verified.)"
        usage = {"input": 0, "output": 0}
        for message in messages:
            if isinstance(message, AIMessage) and message.usage_metadata:
                usage["input"] += message.usage_metadata.get("input_tokens", 0)
                usage["output"] += message.usage_metadata.get("output_tokens", 0)
        return {
            "question": question,
            "answer": answer,
            "refused": is_refusal(answer),
            "citations": citations_of(answer),
            "citations_valid": not citation_problems(answer, self.state["retrieved"]),
            "guardrail": guardrail,
            "tool_trace": self.state["trace"],
            "retrieved": self.state["retrieved"],
            "tokens": {**usage, "total": usage["input"] + usage["output"]},
            "seconds": round(time.time() - started, 2),
            "model": self.model_name,
        }


class _AsyncStack:
    """A tiny AsyncExitStack wrapper (keeps the context managers alive across __aenter__/__aexit__)."""

    def __init__(self):
        from contextlib import AsyncExitStack

        self._stack = AsyncExitStack()

    async def __aenter__(self):
        await self._stack.__aenter__()
        return self

    async def enter(self, manager):
        return await self._stack.enter_async_context(manager)

    async def __aexit__(self, *exc):
        return await self._stack.__aexit__(*exc)


async def ask_async(question: str) -> dict:
    async with Harness() as harness:
        return await harness.ask(question)


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    args = sys.argv[1:]
    if args == ["--list-models"]:
        print("\n".join(available_chat_models()))
        return
    if not args:
        raise SystemExit('Usage: python agent.py "your question"')
    result = asyncio.run(ask_async(" ".join(args)))
    print(result["answer"])
    if result["citations"]:
        print("\nCitations:")
        for source, location in result["citations"]:
            print(f"  - {source} | {location}")
    if result["guardrail"]:
        print(f"\n[guardrail] {result['guardrail']}", file=sys.stderr)
    log(f"[{result['model']}: {result['tokens']['total']} tokens, {result['seconds']}s, {len(result['tool_trace'])} tool calls]")


if __name__ == "__main__":
    main()
