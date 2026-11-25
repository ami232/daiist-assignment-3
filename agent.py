"""
Assignment 3: the agent (`main.py ask "question"` runs `python agent.py "question"`).

A LangChain `create_agent` on Gemini. Its tools come from server.py over MCP
(stdio) and AGENTS.md is its system prompt. Guardrails, in the order they act:

  1. Approval: add_document pauses until a person approves or rejects it
     (HumanInTheLoopMiddleware). With nobody at the keyboard (evaluate.py,
     check.py) it is rejected.
  2. Call limits: at most MAX_TOOL_CALLS tool calls and MAX_MODEL_CALLS model
     calls per question.
  3. Citation check (the extra guardrail): the final answer may only cite, as
     [source, location], passages that search returned in this run, and must
     cite something unless it refuses. Otherwise the answer is replaced by the
     refusal sentence; the blocked draft is kept in the trace.

`CorpusAgent` keeps one server and one agent for many questions (evaluate.py);
`answer(question)` does one. Both return the answer with its trace: tool calls,
retrieved chunks, citations, tokens, seconds and guardrail events.

From the command line the agent prints what it is doing (on stderr), stops
after ASK_DEADLINE seconds with the reason, and falls back to FALLBACK_MODELS
if MODEL fails. Evaluation runs are "patient": one model, no deadline, and
longer waits on rate limits.

    uv run python agent.py "Can I work during my master's?"
    uv run python agent.py --test-models      # which Gemini models answer for your key
    uv run python agent.py --list-models      # every Gemini model your key can see
"""

import asyncio
import json
import os
import re
import sys
import time
import uuid
import warnings
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SERVER = ROOT / "server.py"
AGENTS_MD = ROOT / "AGENTS.md"

# A fixed Gemini version, so evaluation results can be reproduced. Flash-Lite
# because the free tier allows it 500 requests a day; the full Flash models allow
# 20, and one evaluation needs about 150. (On 25 Nov 2026 the alias
# gemini-flash-latest also timed out on Google's side.) GEMINI_MODEL overrides it;
# `--test-models` shows which models answer.
MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite")
# Tried in order when MODEL fails during `main.py ask` (no free quota, retired,
# overloaded). Evaluation never falls back, so every graded answer comes from MODEL.
FALLBACK_MODELS = ("gemini-3.1-flash-lite", "gemini-3.6-flash")
MAX_TOOL_CALLS = 6    # per question
MAX_MODEL_CALLS = 8   # per question

# YOUR decision: the exact sentence the assistant uses when the documents don't
# answer the question. Your AGENTS.md must tell the model to use it word for
# word: evaluate.py counts refusals by looking for it, and the citation check
# puts it in place of a blocked answer.
REFUSAL = "I can't find this in the documents I have."

# The citation check also blocks answers that cite nothing (they can't be
# checked against the documents). Set to False to block only invented citations.
BLOCK_UNCITED = True

# `main.py ask` stops after ASK_DEADLINE seconds and says why (check.py allows
# 300). A tool call that takes longer than TOOL_TIMEOUT is abandoned and the model
# is told it failed. Evaluation runs have no deadline and allow tools 5 minutes.
ASK_DEADLINE = 150
TOOL_TIMEOUT = 60
VERBOSE = False  # agent.py's command line turns on progress messages (on stderr)
LAST_STEP = ""   # the latest progress message, to say where a run got stuck


def say(message: str) -> None:
    global LAST_STEP
    LAST_STEP = message.strip().rstrip(". ")
    if VERBOSE:
        print(message, file=sys.stderr, flush=True)


# The Gemini library leaves this coroutine unawaited when Google returns an error;
# the error itself is still raised and handled, so the warning is only noise.
warnings.filterwarnings("ignore", message="coroutine 'ClientResponse.json' was never awaited")

BRACKET = re.compile(r"\[([^\[\]]+)\]")
CITATION = re.compile(r"([a-z0-9][a-z0-9-]*),\s*(.+)", re.S)
# Two citations written in one bracket, "[a-b, X, c-d, Y]" or "[a-b, X; c-d, Y]":
# split before a source name (lower case with a hyphen) that is followed by a comma.
SECOND_SOURCE = re.compile(r"\s*[;,]\s*(?=[a-z0-9]+(?:-[a-z0-9]+)+\s*,)")
_QUOTES = str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"'})


# ==========================================================================
# Citations (also used by evaluate.py)
# ==========================================================================
def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", (text or "").translate(_QUOTES)).strip().strip(".,;:").lower()


def is_refusal(answer: str) -> bool:
    return _norm(REFUSAL) in _norm(answer)


def citations(answer: str) -> list[tuple[str, str]]:
    """Every [source, location] in an answer, in order, without repeats. Two
    citations in one bracket count as two."""
    found = []
    for inside in BRACKET.findall(answer or ""):
        for part in SECOND_SOURCE.split(inside.strip()):
            cited = CITATION.fullmatch(part.strip())
            if cited:
                found.append((cited.group(1), cited.group(2).strip()))
    return list(dict.fromkeys(found))


def cited_chunk(source: str, location: str, retrieved: list[dict]) -> dict | None:
    """The passage search returned in this run that a citation points to, if any.
    Tolerant of case, quote style and sub-paragraphs: [appendix-student, ST 1.2(d)]
    matches a chunk with ST 1.2."""
    loc = _norm(location)
    for r in retrieved:
        if r.get("source") != source:
            continue
        names = {_norm(r.get("location"))}
        for field in ("rules", "sections", "paths"):
            names |= {_norm(x) for x in (r.get(field) or "").split(" | ") if x}
        if loc in names:
            return r
        for rule in (r.get("rules") or "").split(" | "):
            rule = _norm(rule)
            if rule and loc.startswith(rule) and not re.match(r"[a-z0-9.]", loc[len(rule):len(rule) + 1]):
                return r
    return None


def citation_ok(source: str, location: str, retrieved: list[dict]) -> bool:
    """Did search return this passage in this run?"""
    return cited_chunk(source, location, retrieved) is not None


def citation_problem(answer: str, retrieved: list[dict], added_document: bool = False) -> str | None:
    """Why the citation check blocks this answer, or None if it passes."""
    bad = [f"[{s}, {loc}]" for s, loc in citations(answer) if not citation_ok(s, loc, retrieved)]
    if bad:
        return f"cites passages that search did not return: {', '.join(bad)}"
    if BLOCK_UNCITED and not added_document and not citations(answer) and not is_refusal(answer):
        return "answers without citing any passage"
    return None


# ==========================================================================
# Trace helpers
# ==========================================================================
def retrieved_chunks(messages) -> list[dict]:
    """Chunks returned by search in this run (from the tool's structured output)."""
    from langchain_core.messages import ToolMessage

    seen, chunks = set(), []
    for m in messages:
        if isinstance(m, ToolMessage) and m.name == "search" and isinstance(m.artifact, dict):
            for r in m.artifact.get("results", []):
                if r["id"] not in seen:
                    seen.add(r["id"])
                    chunks.append(r)
    return chunks


def _called(messages, tool: str) -> bool:
    from langchain_core.messages import AIMessage
    return any(isinstance(m, AIMessage) and any(c["name"] == tool for c in m.tool_calls) for m in messages)


def system_prompt() -> str:
    """AGENTS.md without its HTML comments, plus today's date (rules mention dates)."""
    text = AGENTS_MD.read_text(encoding="utf-8") if AGENTS_MD.is_file() else ""
    rules = re.sub(r"<!--.*?-->", "", text, flags=re.S).strip()
    if len(rules.splitlines()) <= 1:
        print("WARNING: AGENTS.md has no rules yet; the agent runs without them.", file=sys.stderr)
    return f"{rules}\n\nToday's date: {date.today().isoformat()}."


# ==========================================================================
# The citation-check guardrail
# ==========================================================================
def citation_check_middleware():
    from langchain.agents.middleware import AgentMiddleware
    from langchain_core.messages import AIMessage

    class CitationCheck(AgentMiddleware):
        """Runs once, after the agent's final answer."""

        def after_agent(self, state, runtime):
            messages = state["messages"]
            last = messages[-1] if messages else None
            if not isinstance(last, AIMessage) or last.tool_calls:
                return None
            problem = citation_problem(last.text, retrieved_chunks(messages), _called(messages, "add_document"))
            if problem is None:
                return None
            # Same id, so it replaces the draft in the conversation.
            return {"messages": [AIMessage(
                id=last.id, content=REFUSAL, usage_metadata=last.usage_metadata,
                response_metadata={**last.response_metadata,
                                   "citation_check": {"reason": problem, "blocked_answer": last.text}},
            )]}

    return CitationCheck()


# ==========================================================================
# MCP tools as LangChain tools
# ==========================================================================
def _as_langchain_tool(session, tool, timeout: float | None):
    from langchain_core.tools import StructuredTool

    async def call(**arguments):
        say(f"  searching: {arguments.get('query', '')}" if tool.name == "search"
            else f"  {tool.name}: {json.dumps(arguments)}")
        try:
            result = await session.call_tool(tool.name, arguments, read_timeout_seconds=timeout)
        except Exception as error:  # noqa: BLE001 - e.g. a timeout: tell the model, which can then refuse
            say(f"  {tool.name} failed: {error}")
            return f"The {tool.name} tool failed: {error}", {"error": str(error)}
        text = "\n".join(getattr(c, "text", "") for c in result.content)
        if result.is_error:
            say(f"  {tool.name} failed: {text[:300]}")
            return f"The {tool.name} tool failed: {text}", {"error": text}
        return text, result.structured_content  # the model sees text; the trace keeps the data

    return StructuredTool(name=tool.name, description=tool.description or "", args_schema=tool.input_schema,
                          coroutine=call, response_format="content_and_artifact")


# ==========================================================================
# Gemini: errors in plain English, retries, fallback models
# ==========================================================================
class DeadlineExceeded(TimeoutError):
    """The whole run took longer than its deadline."""


class ModelsFailed(RuntimeError):
    """Every model tried for one step failed; the message says why for each."""


HINT = "Run `uv run python agent.py --test-models` to see which Gemini models answer for your key."


def out_of_quota(error: BaseException) -> bool:
    """No point retrying today: no free quota for this model, or the daily one is used up."""
    text = str(error)
    return "limit: 0" in text or "PerDay" in text or "per day" in text.lower()


def reason(error: BaseException) -> str:
    """Why a Gemini call failed, in a few words."""
    text = str(error)
    if isinstance(error, TimeoutError):
        return "no reply in time"
    if "limit: 0" in text:
        return "your key has no free quota for this model"
    if "PerDay" in text or "per day" in text.lower():
        return "its daily free quota is used up (it resets at 09:00 in Spain)"
    if "RESOURCE_EXHAUSTED" in text or "429" in text:
        return "rate-limited: too many requests this minute"
    if "NOT_FOUND" in text or "404" in text:
        return "not available to your key (unknown or retired model)"
    if "DEADLINE_EXCEEDED" in text or "504" in text:
        return "timed out on Google's side (overloaded or too slow right now)"
    if "UNAVAILABLE" in text or "503" in text or "overloaded" in text.lower():
        return "overloaded right now, on Google's side"
    if "INTERNAL" in text or "500 " in text:
        return "a server error on Google's side"
    first = text.strip().splitlines()[0] if text.strip() else ""
    return f"{type(error).__name__}: {first[:300]}"


def explain(error: BaseException) -> str:
    """A plain-English reason for a failed run, and what to do about it."""
    if isinstance(error, DeadlineExceeded):
        if LAST_STEP.startswith("starting server"):
            advice = "server.py did not start in time: run `uv run server.py` on its own to see why."
        else:
            advice = f"Gemini may be slow or refusing requests. {HINT}"
        return f"{error} (last step: {LAST_STEP or 'starting'}). {advice}"
    if isinstance(error, ModelsFailed):
        return f"{error}\n{HINT}"
    why = reason(error)
    if not why.startswith(f"{type(error).__name__}: "):  # a Gemini problem reason() recognised
        return f"{MODEL}: {why}. {HINT}"
    if "Connection closed" in str(error):
        return f"{why}. server.py stopped; run `uv run server.py` on its own to see its error."
    return why


def _retryable(error: Exception) -> bool:
    """Retry Gemini's per-minute limits and server errors; not the daily quota,
    and not a model your key has no quota for at all ("limit: 0")."""
    text = str(error)
    if out_of_quota(error):
        return False
    retry = any(s in text for s in ("429", "RESOURCE_EXHAUSTED", "500", "503", "UNAVAILABLE", "INTERNAL"))
    if retry:
        say(f"  Gemini: {reason(error)}; retrying ...")
    return retry


def gemini_model(model: str = MODEL, patient: bool = False):
    """Quick by default (45-second timeout, no retries inside the SDK, so a failing
    model is left quickly); patient for unattended evaluation."""
    from langchain_google_genai import ChatGoogleGenerativeAI
    from api_key import load_api_key
    return ChatGoogleGenerativeAI(model=model, google_api_key=load_api_key(),
                                  timeout=120 if patient else 45, max_retries=6 if patient else 1)


def model_name(model) -> str:
    return str(getattr(model, "model", None) or type(model).__name__).removeprefix("models/")


def model_middleware(fallbacks: list):
    """Says which model it is asking, and if that model fails, tries the
    `fallbacks` (chat models) in order. A fallback that works is tried first
    for the rest of the run."""
    from langchain.agents.middleware import AgentMiddleware
    from langchain_core.messages import AIMessage
    from langgraph.errors import GraphBubbleUp

    class ModelChoice(AgentMiddleware):
        def __init__(self):
            super().__init__()
            self.preferred = None

        async def awrap_model_call(self, request, handler):
            step = sum(isinstance(m, AIMessage) for m in request.messages) + 1
            models = [request.model, *fallbacks]
            models.sort(key=lambda m: m is not self.preferred)  # stable: otherwise in order
            failures = []
            for model in models:
                name = model_name(model)
                say(f"  asking {name} (step {step}) ...")
                try:
                    response = await handler(request if model is request.model else request.override(model=model))
                except GraphBubbleUp:
                    raise
                except Exception as error:  # noqa: BLE001 - try the next model
                    if not fallbacks:
                        raise
                    say(f"  {name} failed: {reason(error)}")
                    failures.append(f"  {name}: {reason(error)}")
                    continue
                self.preferred = model if model is not request.model else None
                return response
            raise ModelsFailed("every Gemini model failed:\n" + "\n".join(failures))

    return ModelChoice()


class CorpusAgent:
    """One MCP server and one agent, reused across questions.

        async with CorpusAgent() as agent:
            result = await agent.ask("...")
    """

    def __init__(self, model=None, interactive: bool | None = None, server: Path | None = None,
                 patient: bool = False):
        self.model = model
        self.server = server or SERVER
        self.patient = patient  # evaluation: wait out rate limits instead of giving up quickly
        self.deadline = None    # set by answer(); paused while a person decides on an approval
        # A person can approve only if both ends are a terminal (check.py captures stdout).
        self.interactive = sys.stdin.isatty() and sys.stdout.isatty() if interactive is None else interactive

    async def __aenter__(self):
        from contextlib import AsyncExitStack

        self._stack = AsyncExitStack()
        try:
            await self._start()
        except BaseException:
            await self._stack.aclose()  # stop the server even if starting failed or was cancelled
            raise
        return self

    async def _start(self):
        from langchain.agents import create_agent
        from langchain.agents.middleware import (HumanInTheLoopMiddleware, ModelCallLimitMiddleware,
                                                 ModelRetryMiddleware, ToolCallLimitMiddleware)
        from langgraph.checkpoint.memory import InMemorySaver
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import stdio_client

        say("  starting server.py ...")
        # The whole environment: by default MCP passes only a few variables, which
        # would hide GEMINI_API_KEY from the server when it is not in .env.
        params = StdioServerParameters(command=sys.executable, args=[str(self.server)], cwd=str(ROOT),
                                       env=dict(os.environ))
        read, write = await self._stack.enter_async_context(stdio_client(params))
        session = await self._stack.enter_async_context(ClientSession(read, write))
        await session.initialize()
        tool_timeout = 300 if self.patient else TOOL_TIMEOUT
        tools = [_as_langchain_tool(session, t, tool_timeout) for t in (await session.list_tools()).tools]
        say(f"  server started; tools: {', '.join(t.name for t in tools)}")

        # Fall back to other models only in quick runs with the default Gemini model.
        fallbacks = [] if self.patient or self.model is not None else \
            [gemini_model(m) for m in dict.fromkeys(FALLBACK_MODELS) if m != MODEL]
        self.agent = create_agent(
            self.model or gemini_model(patient=self.patient),
            tools,
            system_prompt=system_prompt(),
            middleware=[
                model_middleware(fallbacks),
                HumanInTheLoopMiddleware(interrupt_on={"add_document": {
                    "allowed_decisions": ["approve", "reject"],
                    "description": "Adding a document changes what every later answer is based on.",
                }}),
                ToolCallLimitMiddleware(run_limit=MAX_TOOL_CALLS),
                ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS, exit_behavior="end"),
                ModelRetryMiddleware(max_retries=4 if self.patient else 1, retry_on=_retryable,
                                     initial_delay=15.0 if self.patient else 5.0,
                                     max_delay=60.0 if self.patient else 10.0, on_failure="error"),
                citation_check_middleware(),
            ],
            checkpointer=InMemorySaver(),  # needed to pause for approval and resume
        )

    async def __aexit__(self, *exc):
        await self._stack.aclose()

    def decide(self, action: dict) -> dict:
        """Approval for one gated tool call."""
        if not self.interactive:
            return {"type": "reject",
                    "message": "No person is available to approve this, so the document was not added."}
        print(f"\nThe agent wants to run {action['name']} with {json.dumps(action['args'])}.\n"
              f"{action.get('description', '')}", file=sys.stderr)
        print("Allow it? [y/N] ", end="", file=sys.stderr, flush=True)
        if sys.stdin.readline().strip().lower() in ("y", "yes"):
            return {"type": "approve"}
        return {"type": "reject", "message": "The user did not approve adding this document."}

    async def ask(self, question: str) -> dict:
        from langgraph.types import Command

        config = {"configurable": {"thread_id": uuid.uuid4().hex}}  # a fresh conversation per question
        started = time.time()
        decisions = []
        state = await self.agent.ainvoke({"messages": [{"role": "user", "content": question}]}, config)
        while state.get("__interrupt__"):
            request = state["__interrupt__"][0].value
            asked = time.monotonic()
            made = [self.decide(a) for a in request["action_requests"]]
            if self.deadline is not None and self.deadline.when() is not None and not self.deadline.expired():
                self.deadline.reschedule(self.deadline.when() + time.monotonic() - asked)
            decisions += [{"tool": a["name"], "args": a["args"], "decision": d["type"]}
                          for a, d in zip(request["action_requests"], made)]
            state = await self.agent.ainvoke(Command(resume={"decisions": made}), config)
        return summarise(question, state["messages"], time.time() - started, decisions)


def summarise(question: str, messages, seconds: float, decisions: list) -> dict:
    from langchain_core.messages import AIMessage, ToolMessage

    ai = [m for m in messages if isinstance(m, AIMessage)]
    final = ai[-1] if ai else None
    answer = final.text if final else ""
    retrieved = retrieved_chunks(messages)
    outputs = {m.tool_call_id: m for m in messages if isinstance(m, ToolMessage)}
    tool_calls = []
    for m in ai:
        for call in m.tool_calls:
            out = outputs.get(call["id"])
            tool_calls.append({"tool": call["name"], "args": call["args"],
                               "output": (out.text[:2000] if out else None)})
    usage = [m.usage_metadata for m in ai if m.usage_metadata]
    check = (final.response_metadata or {}).get("citation_check") if final else None
    return {
        "question": question,
        "answer": answer,
        "refused": is_refusal(answer),
        "citations": [{"label": f"[{s}, {loc}]", "valid": citation_ok(s, loc, retrieved)}
                      for s, loc in citations(answer)],
        "guardrail": check,                 # set when the citation check blocked a draft
        "approvals": decisions,
        "tool_calls": tool_calls,
        "tool_errors": [m.artifact["error"] for m in messages if isinstance(m, ToolMessage)
                        and isinstance(m.artifact, dict) and m.artifact.get("error")],
        "retrieved": retrieved,
        "model": next((m.response_metadata.get("model_name") for m in reversed(ai)
                       if m.response_metadata.get("model_name")), MODEL),
        "model_calls": len(usage),
        "input_tokens": sum(u.get("input_tokens", 0) for u in usage),
        "output_tokens": sum(u.get("output_tokens", 0) for u in usage),
        "seconds": round(seconds, 2),
    }


async def _ask_one(question: str, deadline: float | None = None, **kwargs) -> dict:
    scope = asyncio.timeout(deadline)  # None: no deadline
    try:
        async with scope:  # at the deadline the run is cancelled, which also stops the server
            async with CorpusAgent(**kwargs) as agent:
                agent.deadline = scope
                return await agent.ask(question)
    except TimeoutError:
        if scope.expired():
            raise DeadlineExceeded(f"no answer within {deadline} s") from None
        raise


def answer(question: str, deadline: float | None = None, **kwargs) -> dict:
    """One question, start to finish (starts and stops the server). With a
    `deadline` in seconds, raises DeadlineExceeded when it passes."""
    return asyncio.run(_ask_one(question, deadline, **kwargs))


def print_answer(result: dict) -> None:
    print(result["answer"])
    cited = [(s, loc) for s, loc in citations(result["answer"]) if citation_ok(s, loc, result["retrieved"])]
    if cited:
        print("\nSources:")
        for source, location in cited:
            r = cited_chunk(source, location, result["retrieved"])
            print(f"  [{source}, {location}] {r['title']} > {r['heading_path']}, {r['url']}")
    if result["guardrail"]:
        print(f"\n[citation check] blocked the draft answer: it {result['guardrail']['reason']}.", file=sys.stderr)
    searches = sum(1 for c in result["tool_calls"] if c["tool"] == "search")
    plural = lambda n, word: f"{n} {word}{'' if n == 1 else ('es' if word.endswith('h') else 's')}"  # noqa: E731
    print(f"\n({plural(result['model_calls'], 'model call')}, {plural(searches, 'search')}, "
          f"{result['input_tokens'] + result['output_tokens']:,} tokens, {result['seconds']} s, {result['model']})")


def list_models() -> None:
    from google import genai
    from api_key import load_api_key
    client = genai.Client(api_key=load_api_key())
    for m in client.models.list():
        actions = getattr(m, "supported_actions", None) or []
        if "generateContent" in actions:
            print(m.name.removeprefix("models/"))


def test_models(limit: int = 12) -> None:
    """Send one tiny request to each Gemini Flash model your key lists (aliases
    and newest first), to see which actually answer. No retries; 30 s each."""
    from google import genai
    from google.genai import types
    from api_key import load_api_key

    def version(name: str) -> float:
        found = re.search(r"gemini-(\d+(?:\.\d+)?)", name)
        return float(found.group(1)) if found else 0.0

    client = genai.Client(api_key=load_api_key(), http_options=types.HttpOptions(
        timeout=30_000, retry_options=types.HttpRetryOptions(attempts=1)))
    skip = ("image", "tts", "audio", "live", "embedding", "native", "thinking", "-exp")
    names = sorted({m.name.removeprefix("models/") for m in client.models.list()
                    if "generateContent" in (getattr(m, "supported_actions", None) or [])
                    and "flash" in m.name and not any(s in m.name for s in skip)},
                   key=lambda n: (not n.endswith("-latest"), -version(n), n))[:limit]
    print(f"Main model: {MODEL}; fallbacks: {', '.join(FALLBACK_MODELS)}.\n"
          f"Trying {len(names)} Flash models, one short request each ...\n")
    working = []
    for name in names:
        started = time.time()
        try:
            client.models.generate_content(model=name, contents="Reply with just: OK")
            working.append(name)
            print(f"  OK    {name:40s} {time.time() - started:5.1f} s", flush=True)
        except Exception as error:  # noqa: BLE001 - report every failure and keep going
            print(f"  FAIL  {name:40s} {time.time() - started:5.1f} s  {reason(error)}", flush=True)
    if working:
        suggest = next((n for n in working if "lite" not in n), working[0])
        print(f"\nAnswered: {', '.join(working)}\n"
              f'To use one in this PowerShell window: $env:GEMINI_MODEL = "{suggest}"\n'
              f"To change the default for everyone, edit MODEL in agent.py.")
    else:
        print("\nNo model answered. See your limits at https://aistudio.google.com/rate-limit")


def main() -> int:
    global VERBOSE
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(errors="replace")
    args = sys.argv[1:]
    if args in (["--list-models"], ["--test-models"]):
        try:
            list_models() if args == ["--list-models"] else test_models()
        except Exception as error:  # noqa: BLE001
            print(f"Could not list Gemini models: {reason(error)}", file=sys.stderr)
            return 1
        return 0
    if not args:
        print('Usage: uv run python agent.py "your question"', file=sys.stderr)
        return 2
    VERBOSE = True
    say(f"Starting (gives up after {ASK_DEADLINE} s) ...")
    try:
        result = answer(" ".join(args), deadline=ASK_DEADLINE)
    except KeyboardInterrupt:
        print("\nStopped.", file=sys.stderr)
        return 130
    except Exception as error:  # noqa: BLE001 - a plain reason instead of a traceback
        print(f"\nThe agent stopped: {explain(error)}", file=sys.stderr)
        return 1
    print_answer(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())
