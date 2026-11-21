"""
Assignment 3: your agent (`main.py ask "question"` runs `python agent.py "question"`).

A LangChain agent on Gemini. Its tools come from server.py over MCP. AGENTS.md is its
system prompt. Three guardrails, all enforced in code, not left to the model:

  1. APPROVAL    add_document never runs until a human types "y" (and never in non-interactive runs)
  2. CALL LIMIT  at most MAX_TOOL_CALLS tool calls per question
  3. NEUTRALITY  questions that ask who to vote for, or which party is better, are refused
                 before the model is called (see ASKS_FOR_VOTE_ADVICE)

run_agent(question) returns the answer and the tool trace, for evaluate.py.
"""

import asyncio
import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SYSTEM_PROMPT_FILE = ROOT / "AGENTS.md"

MAX_TOOL_CALLS = 4  # a question needs 1 search, or 1 per party when comparing; more means the agent is flailing

# Guardrail 3: neutrality. Clear requests for voting advice or a verdict on which party is better.
# It is a regular expression, so it is easy to explain and easy to test, and also easy to get around
# with different wording: the rules in AGENTS.md are the second line of defence.
ASKS_FOR_VOTE_ADVICE = re.compile(
    r"should\s+i\s+vote"
    r"|recommend(?:s|ed)?\s+(?:that\s+)?(?:i|me\s+to)\s+vote"
    r"|who\s+(?:to|should\s+i|do\s+you\s+recommend\s+i)\s+vote"
    r"|who\s+(?:do|would)\s+you\s+(?:recommend|vote\s+for|choose|pick|support)"
    r"|(?:which|what)\s+(?:party|candidate|programme|program|platform)\s+(?:is|are|was)\s+(?:the\s+)?(?:best|better|worse|worst|good|bad)"
    r"|(?:best|better|worst|worse)\s+(?:party|candidate)"
    r"|vote\s+for\s+(?:whom|who|which)"
    r"|(?:which|what)\s+(?:party|candidate)\s+(?:do\s+you|would\s+you)\s+(?:recommend|choose|pick|support)",
    re.IGNORECASE,
)
NEUTRALITY_REPLY = (
    "I can't tell you who to vote for or which party is better. I can tell you what each programme "
    "proposes on a topic, with page citations, and you can compare them yourself. "
    "Which topic would you like to look at?"
)


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


# ---------------------------------------------------------------- the model
DEFAULT_MODEL = "gemini-3.6-flash"  # tested on 2026-11-21: answered in 7 s; 2.5-flash is closed to new users,
#                                     3.5/3.7/3.8-flash timed out or returned 503 "high demand"
MAX_ATTEMPTS = 6  # Google sometimes answers 503 "high demand"; we wait and try the same question again


def choose_model() -> str:
    """GEMINI_MODEL if set, else DEFAULT_MODEL."""
    return os.environ.get("GEMINI_MODEL") or DEFAULT_MODEL


def is_transient(error: BaseException) -> bool:
    """True for errors that go away by themselves (503 high demand, 504 timeout, 429 rate limit)."""
    parts = getattr(error, "exceptions", None)
    if parts:
        return any(is_transient(p) for p in parts)
    text = f"{type(error).__name__} {error}"
    if error.__cause__ is not None:
        text += f" {error.__cause__}"
    return any(word in text for word in ("503", "504", "429", "UNAVAILABLE", "DEADLINE", "RESOURCE_EXHAUSTED",
                                         "Timeout", "timed out", "ReadError", "ConnectError"))


def make_model():
    from langchain_google_genai import ChatGoogleGenerativeAI

    from api_key import load_api_key

    name = choose_model()
    log(f"[agent] model: {name}")
    return ChatGoogleGenerativeAI(model=name, api_key=load_api_key(), temperature=0, timeout=90, max_retries=1), name


# ---------------------------------------------------------------- guardrail 1: approval
def approve_add_document(path: str, interactive: bool) -> bool:
    """A human must say yes. Non-interactive runs (evaluate.py, pipes) always say no."""
    if not interactive:
        return False
    log(f"\n[approval] The agent wants to add this document to the index: {path}")
    log("[approval] This embeds new passages and uses embedding quota.")
    try:
        return input("[approval] Allow it? (y/N) ").strip().lower() in ("y", "yes")
    except EOFError:
        return False


# ---------------------------------------------------------------- the tools, wrapped
def wrap_tools(session, specs, trace: list, state: dict, interactive: bool) -> list:
    """Turn the MCP tools into LangChain tools that enforce the approval step and the call limit."""
    from langchain_core.tools import StructuredTool

    def make(spec):
        async def call(**arguments) -> str:
            started = time.time()
            if state["calls"] >= MAX_TOOL_CALLS:
                text = (f"Tool-call limit reached ({MAX_TOOL_CALLS}). Do not call any more tools. "
                        f"Answer now from the passages you already have, or say the programmes do not cover it.")
                state["limit_hit"] = True
            else:
                state["calls"] += 1
                if spec.name == "add_document" and not approve_add_document(str(arguments.get("path")), interactive):
                    text = ("The user did not approve adding this document, so it was NOT added. "
                            "Do not try again. Tell the user it was not added.")
                    state["add_denied"] = True
                else:
                    result = await session.call_tool(spec.name, arguments)
                    text = "\n".join(getattr(c, "text", "") for c in result.content).strip()
                    if getattr(result, "is_error", False):
                        text = f"Tool error: {text}"
            trace.append({"tool": spec.name, "args": arguments, "result": text, "seconds": round(time.time() - started, 2)})
            return text

        return StructuredTool(name=spec.name, description=spec.description or "",
                              args_schema=spec.input_schema, coroutine=call)

    return [make(s) for s in specs]


# ---------------------------------------------------------------- running a question
def message_text(message) -> str:
    return str(message.text or "")


async def ask(question: str, interactive: bool = False) -> dict:
    """Answer one question. Returns answer, tool trace, token counts, seconds and which guardrail fired."""
    if ASKS_FOR_VOTE_ADVICE.search(question):
        return {"answer": NEUTRALITY_REPLY, "tool_calls": [], "tokens": {"input": 0, "output": 0, "total": 0},
                "seconds": 0.0, "guardrail": "neutrality", "model": None}

    from langchain.agents import create_agent
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    model, model_name = make_model()
    # env=os.environ: by default the MCP client hides your environment (and your key) from server.py.
    params = StdioServerParameters(command=sys.executable, args=[str(ROOT / "server.py")],
                                   cwd=str(ROOT), env=dict(os.environ))
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            specs = (await session.list_tools()).tools
            trace: list = []
            state = {"calls": 0, "limit_hit": False, "add_denied": False}
            tools = wrap_tools(session, specs, trace, state, interactive)
            agent = create_agent(model, tools, system_prompt=SYSTEM_PROMPT_FILE.read_text(encoding="utf-8"))
            started = time.time()
            result = await agent.ainvoke(
                {"messages": [{"role": "user", "content": question}]},
                config={"recursion_limit": 2 * MAX_TOOL_CALLS + 8},
            )
            seconds = round(time.time() - started, 2)

    messages = result["messages"]
    usage = {"input": 0, "output": 0, "total": 0}
    for message in messages:
        meta = getattr(message, "usage_metadata", None) or {}
        usage["input"] += meta.get("input_tokens", 0)
        usage["output"] += meta.get("output_tokens", 0)
        usage["total"] += meta.get("total_tokens", 0)
    guardrail = "call_limit" if state["limit_hit"] else "approval_denied" if state["add_denied"] else None
    return {"answer": message_text(messages[-1]).strip(), "tool_calls": trace, "tokens": usage,
            "seconds": seconds, "guardrail": guardrail, "model": model_name}


def run_agent(question: str, interactive: bool = False) -> dict:
    """Synchronous wrapper used by evaluate.py. Retries temporary Google errors (503, timeouts, 429)."""
    for attempt in range(1, MAX_ATTEMPTS + 1):
        try:
            return asyncio.run(ask(question, interactive=interactive))
        except BaseException as error:  # noqa: BLE001 - ExceptionGroup from the MCP task group
            if isinstance(error, KeyboardInterrupt) or attempt == MAX_ATTEMPTS or not is_transient(error):
                raise
            wait = min(10 * attempt, 40)
            log(f"[agent] Google is busy (attempt {attempt}/{MAX_ATTEMPTS}). Trying again in {wait}s...")
            time.sleep(wait)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit('usage: python agent.py "your question"')
    outcome = run_agent(" ".join(sys.argv[1:]), interactive=sys.stdin.isatty())
    print(outcome["answer"])
    note = f" | guardrail: {outcome['guardrail']}" if outcome["guardrail"] else ""
    log(f"\n[agent] {len(outcome['tool_calls'])} tool call(s), {outcome['tokens']['total']} tokens, "
        f"{outcome['seconds']}s{note}")


