"""
Assignment 3: your agent (`main.py ask "question"` runs `python agent.py "question"`).

A LangChain `create_agent` on Gemini. Its tools come from server.py over MCP and AGENTS.md is
its system prompt. Around the model there is a small harness:

  1. approval    add_document pauses for the user's yes/no before it runs;
  2. call limits at most MAX_MODEL_CALLS model calls and MAX_SEARCHES searches per question;
  3. guardrail   the citation verifier: an answer may cite only passages that the search tool
                 really returned in this conversation, and must cite at least one unless it
                 starts with "NOT COVERED:". A bad answer goes back to the model once; what is
                 still unverifiable afterwards is reported, not hidden.

`ask(question)` (or `async with CorpusAgent() as agent: await agent.ask(question)` for many
questions) returns a dict with the answer, the tool trace and what the question cost; that is
what evaluate.py uses. Progress and logs go to stderr; stdout carries only the answer.
"""

from __future__ import annotations

import asyncio
import functools
import json
import os
import re
import sys
import time
import uuid
from contextlib import AsyncExitStack
from pathlib import Path
from typing import Any, Callable

from langchain.agents import create_agent
from langchain.agents.middleware import (
    AgentState,
    HumanInTheLoopMiddleware,
    InterruptOnConfig,
    ModelCallLimitMiddleware,
    ToolCallLimitMiddleware,
    after_model,
)
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.tools import StructuredTool, ToolException
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.runtime import Runtime
from langgraph.types import Command
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent

# The cheap model answers; a stronger, different one judges (evaluate.py). The first name that
# exists for your key is used; AGENT_MODEL / JUDGE_MODEL override the choice.
# Names from https://ai.google.dev/gemini-api/docs/models (stable models, November 2026).
AGENT_MODELS = ("gemini-3.5-flash-lite", "gemini-3.1-flash-lite")
JUDGE_MODELS = ("gemini-3.8-flash", "gemini-3.6-flash")

MAX_MODEL_CALLS = 8          # per question: search, maybe search again, answer, one citation retry
MAX_SEARCHES = 5
MAX_CITATION_RETRIES = 1
QUESTION_TIMEOUT = 240       # seconds
REFUSAL = re.compile(r"^\W*NOT COVERED\b", re.IGNORECASE)

# A passage label in a search result: "[Reg. 2019/947, UAS.OPEN.030]" alone on a line, then "Location: ...".
PASSAGE_LABEL = re.compile(r"^\[([^\[\]\n]+)\]\n(?=Location: )", re.MULTILINE)
# A citation in an answer: square brackets with a comma, i.e. "[source, location]" (; separates several).
CITATION = re.compile(r"\[([^\[\]\n]*,[^\[\]\n]*)\]")
PART_SUFFIX = re.compile(r", part \d+/\d+$")


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


# --------------------------------------------------------------------------- #
# Models
# --------------------------------------------------------------------------- #

@functools.lru_cache(maxsize=None)
def resolve_model_name(candidates: tuple[str, ...], env_var: str) -> str:
    """The model to use: the env var if set, else the first candidate this API key can see."""
    forced = os.environ.get(env_var, "").strip()
    if forced:
        return forced
    from google import genai

    client = genai.Client(api_key=load_api_key())
    for name in candidates:
        try:
            client.models.get(model=name)
            return name
        except Exception as error:  # noqa: BLE001
            if getattr(error, "code", None) in (400, 404):
                log(f"model {name} is not available for this key; trying the next one")
                continue
            return name   # a network or quota hiccup says nothing about the model: keep the preferred one
    raise RuntimeError(f"None of {', '.join(candidates)} is available for this API key. Set {env_var} to a model "
                       f"from https://ai.google.dev/gemini-api/docs/models")


def make_chat_model(role: str = "agent", **options: Any):
    from langchain_google_genai import ChatGoogleGenerativeAI

    key = load_api_key()
    candidates, env_var = (AGENT_MODELS, "AGENT_MODEL") if role == "agent" else (JUDGE_MODELS, "JUDGE_MODEL")
    return ChatGoogleGenerativeAI(model=resolve_model_name(candidates, env_var), api_key=key, timeout=120, **options)


# --------------------------------------------------------------------------- #
# Reading what the model and the tools said
# --------------------------------------------------------------------------- #

def message_text(message: Any) -> str:
    text = getattr(message, "text", None)      # a property (a str) in langchain-core 1.x
    if isinstance(text, str):
        return str(text)
    content = getattr(message, "content", "")
    if isinstance(content, str):
        return content
    return "".join(part.get("text", "") if isinstance(part, dict) else str(part) for part in content)


def retrieved_labels(messages: list) -> list[str]:
    """Labels of every passage that a search returned in this conversation, in order, without repeats."""
    seen: dict[str, None] = {}
    for message in messages:
        if isinstance(message, ToolMessage) and message.name == "search":
            for label in PASSAGE_LABEL.findall(message_text(message)):
                seen.setdefault(label, None)
    return list(seen)


def cited_labels(answer: str) -> list[str]:
    labels = []
    for inner in CITATION.findall(answer):
        for part in inner.split(";"):
            part = re.sub(r"\s+", " ", part).strip()
            if part:
                labels.append(part)
    return labels


def is_refusal(answer: str) -> bool:
    return bool(REFUSAL.match(answer))


def citation_problems(answer: str, retrieved: list[str]) -> list[str]:
    """Why this answer cannot be accepted (empty list: it can)."""
    known = set(retrieved) | {PART_SUFFIX.sub("", label) for label in retrieved}
    cites = cited_labels(answer)
    invalid = [c for c in cites if c not in known]
    problems = []
    if not retrieved:
        problems.append("you have not searched the corpus yet")
    if invalid:
        problems.append("these labels were not returned by any search: " + "; ".join(invalid))
    if not is_refusal(answer) and not [c for c in cites if c in known]:
        problems.append("the answer cites no passage")
    return problems


# --------------------------------------------------------------------------- #
# The guardrail (a middleware: it runs after every model call)
# --------------------------------------------------------------------------- #

def _only_added_a_file(messages: list) -> bool:
    """True when, since the user's last message, the agent called add_document and did not search:
    its answer then reports what happened to the file and has no rule to cite."""
    start = max((i for i, m in enumerate(messages)
                 if isinstance(m, HumanMessage) and not m.additional_kwargs.get("guardrail")), default=0)
    called = [call["name"] for m in messages[start:] if isinstance(m, AIMessage) for call in m.tool_calls]
    return "add_document" in called and "search" not in called


@after_model(can_jump_to=["model"])
def citation_verifier(state: AgentState, runtime: Runtime) -> dict[str, Any] | None:
    messages = state["messages"]
    last = messages[-1]
    if not isinstance(last, AIMessage) or last.tool_calls:
        return None                                   # still working: only final answers are checked
    if _only_added_a_file(messages):
        return None                                   # reports an action, not a rule: nothing to cite
    retries = sum(1 for m in messages if isinstance(m, HumanMessage) and m.additional_kwargs.get("guardrail"))
    problems = citation_problems(message_text(last), retrieved_labels(messages))
    if not problems or retries >= MAX_CITATION_RETRIES:
        return None
    labels = retrieved_labels(messages)
    note = (f"Your answer cannot be accepted yet: {'; '.join(problems)}. "
            f"Labels returned by searches so far: {', '.join(f'[{x}]' for x in labels) or 'none'}. "
            "Search again if you need to, then answer with every claim cited by a label copied exactly "
            "from a search result, or begin with 'NOT COVERED:' if the passages do not answer the question.")
    return {"messages": [HumanMessage(content=note, additional_kwargs={"guardrail": "citation_verifier"})],
            "jump_to": "model"}


# --------------------------------------------------------------------------- #
# Approval before add_document
# --------------------------------------------------------------------------- #

Approver = Callable[[str, dict], bool]


def ask_user_approval(name: str, args: dict) -> bool:
    """Interactive yes/no. Without a terminal nobody can answer, so the answer is no."""
    if not sys.stdin or not sys.stdin.isatty():
        log(f"(no terminal to ask on, so {name} {json.dumps(args, ensure_ascii=False)} was NOT run)")
        return False
    print(f"\nThe agent wants to call {name} with {json.dumps(args, ensure_ascii=False)}", file=sys.stderr)
    return input("Allow it? [y/N] ").strip().lower() in ("y", "yes", "s", "si", "sí")


def _approval_description(tool_call: dict, state: Any, runtime: Any) -> str:
    return f"Add this file to the corpus: {tool_call['args'].get('path')}"


# --------------------------------------------------------------------------- #
# The agent
# --------------------------------------------------------------------------- #

def _plain_schema(schema: Any) -> Any:
    """The MCP tool's JSON schema without 'title' keys, which Gemini's function schema does not take."""
    if isinstance(schema, dict):
        return {k: _plain_schema(v) for k, v in schema.items() if k != "title"}
    if isinstance(schema, list):
        return [_plain_schema(v) for v in schema]
    return schema


def _langchain_tool(session: ClientSession, tool: Any) -> StructuredTool:
    """Wrap one MCP tool as a LangChain tool that calls the server over the open session."""

    async def call(**arguments: Any) -> str:
        result = await session.call_tool(tool.name, arguments)
        text = "\n".join(getattr(part, "text", "") for part in result.content).strip()
        if result.is_error:
            raise ToolException(text or f"{tool.name} failed")
        return text

    return StructuredTool(name=tool.name, description=tool.description or "", coroutine=call,
                          args_schema=_plain_schema(tool.input_schema), handle_tool_error=True)


def build_agent(model: Any, tools: list):
    system_prompt = (ROOT / "AGENTS.md").read_text(encoding="utf-8").strip()
    if not system_prompt:
        raise RuntimeError("AGENTS.md is empty; it is the agent's system prompt.")
    return create_agent(
        model, tools, system_prompt=system_prompt, checkpointer=InMemorySaver(),
        middleware=[
            HumanInTheLoopMiddleware(interrupt_on={"add_document": InterruptOnConfig(
                allowed_decisions=["approve", "reject"], description=_approval_description)}),
            ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS, exit_behavior="end"),
            ToolCallLimitMiddleware(tool_name="search", run_limit=MAX_SEARCHES),
            citation_verifier,
        ],
    )


class CorpusAgent:
    """One server.py process and one agent. Use `async with`; ask() may be called many times."""

    def __init__(self, approve: Approver | None = None, index_dir: str | Path | None = None, model: Any = None):
        self.approve = approve or ask_user_approval
        self.index_dir = index_dir
        self.model = model
        self.approvals: list[dict] = []

    async def __aenter__(self) -> "CorpusAgent":
        self._stack = AsyncExitStack()
        env = dict(os.environ)
        if self.index_dir:
            env["RAG_INDEX_DIR"] = str(self.index_dir)     # evaluate.py points this at a throw-away copy
        params = StdioServerParameters(command=sys.executable, args=[str(ROOT / "server.py")], cwd=str(ROOT), env=env)
        try:
            read, write = await self._stack.enter_async_context(stdio_client(params))
            session = await self._stack.enter_async_context(ClientSession(read, write))
            await session.initialize()
            self.session = session
            tools = [_langchain_tool(session, t) for t in (await session.list_tools()).tools]
            self.tool_names = [t.name for t in tools]
            self.agent = build_agent(self.model or make_chat_model("agent"), tools)
        except BaseException:
            await self._stack.aclose()
            raise
        return self

    async def __aexit__(self, *exc_info: Any) -> None:
        await self._stack.aclose()

    async def call_tool(self, name: str, arguments: dict) -> str:
        """Call a server tool directly, without the model (evaluate.py uses it for the duplicate-add check)."""
        result = await self.session.call_tool(name, arguments)
        return "\n".join(getattr(part, "text", "") for part in result.content).strip()

    async def _run(self, question: str, thread: dict) -> list:
        state = await self.agent.ainvoke({"messages": [HumanMessage(content=question)]}, thread)
        while state.get("__interrupt__"):                  # the harness paused: add_document needs a yes/no
            decisions = []
            for interrupt in state["__interrupt__"]:
                for request in interrupt.value["action_requests"]:
                    allowed = await asyncio.to_thread(self.approve, request["name"], request["args"])
                    self.approvals.append({"tool": request["name"], "args": request["args"], "approved": bool(allowed)})
                    decisions.append({"type": "approve"} if allowed else
                                      {"type": "reject", "message": "The user declined, so the file was not added."})
            state = await self.agent.ainvoke(Command(resume={"decisions": decisions}), thread)
        return state["messages"]

    async def ask(self, question: str, *, raise_errors: bool = False) -> dict:
        """Answer one question on a fresh thread. Never raises unless raise_errors (evaluate.py wants to go on)."""
        started = time.perf_counter()
        # recursion_limit is only a safety net: each model call passes through ~6 graph steps (middleware
        # included), and the model-call limit above is what normally ends a runaway loop.
        thread = {"configurable": {"thread_id": uuid.uuid4().hex}, "recursion_limit": 14 * MAX_MODEL_CALLS}
        before = len(self.approvals)
        try:
            messages = await asyncio.wait_for(self._run(question, thread), timeout=QUESTION_TIMEOUT)
            error = None
        except Exception as exc:  # noqa: BLE001
            if raise_errors:
                raise
            error = f"{type(exc).__name__}: {exc}"
            try:                                           # keep what happened before the failure (trace, tokens)
                messages = (await self.agent.aget_state(thread)).values.get("messages") or [HumanMessage(content=question)]
            except Exception:  # noqa: BLE001
                messages = [HumanMessage(content=question)]
        return summarise(question, messages, time.perf_counter() - started, self.approvals[before:], error)


def summarise(question: str, messages: list, seconds: float, approvals: list[dict], error: str | None = None) -> dict:
    """Turn the final message list into the record evaluate.py stores: answer, trace, tokens, guardrail."""
    answer = ""
    for message in reversed(messages):
        if isinstance(message, AIMessage) and not message.tool_calls:
            answer = message_text(message).strip()
            break
    results = {m.tool_call_id: message_text(m) for m in messages if isinstance(m, ToolMessage)}
    trace = [{"tool": call["name"], "args": call["args"], "result": results.get(call["id"], "")}
             for m in messages if isinstance(m, AIMessage) for call in m.tool_calls]
    usage = [m.usage_metadata or {} for m in messages if isinstance(m, AIMessage)]
    retrieved = retrieved_labels(messages)
    known = set(retrieved) | {PART_SUFFIX.sub("", label) for label in retrieved}
    cites = cited_labels(answer)
    return {
        "question": question,
        "answer": answer,
        "refused": is_refusal(answer),
        "citations": [c for c in dict.fromkeys(cites) if c in known],
        "invalid_citations": [c for c in dict.fromkeys(cites) if c not in known],
        "retrieved": retrieved,
        "trace": trace,
        "searches": sum(1 for t in trace if t["tool"] == "search"),
        "model_calls": sum(1 for u in usage if u) or len(usage),   # the limit notice is an AIMessage without usage
        "tokens": {"input": sum(u.get("input_tokens", 0) for u in usage),
                   "output": sum(u.get("output_tokens", 0) for u in usage),
                   "total": sum(u.get("total_tokens", 0) for u in usage)},
        "seconds": round(seconds, 2),
        "approvals": approvals,
        "guardrail": {"citation_retries": sum(1 for m in messages if isinstance(m, HumanMessage)
                                              and m.additional_kwargs.get("guardrail")),
                      "call_limit_hit": "call limit" in answer.lower() and not cites},
        "error": error,
    }


def ask(question: str, approve: Approver | None = None, index_dir: str | Path | None = None) -> dict:
    """One question, one server process. For many questions use CorpusAgent."""

    async def run() -> dict:
        async with CorpusAgent(approve=approve, index_dir=index_dir) as agent:
            return await agent.ask(question, raise_errors=True)

    return asyncio.run(run())


def main() -> int:
    for stream in (sys.stdout, sys.stderr):
        if hasattr(stream, "reconfigure"):
            stream.reconfigure(encoding="utf-8", errors="replace")
    question = " ".join(sys.argv[1:]).strip()
    if not question:
        print('usage: python agent.py "your question"   (or: uv run python main.py ask "your question")', file=sys.stderr)
        return 2
    try:
        result = ask(question)
    except Exception as error:  # noqa: BLE001
        print(f"The agent failed: {type(error).__name__}: {error}", file=sys.stderr)
        return 1
    print(result["answer"] or "(the agent produced no answer)")
    if result["citations"]:
        print("\nSources:")
        for label in result["citations"]:
            print(f"  [{label}]")
    if result["invalid_citations"]:
        print("\nWARNING: these citations were not returned by any search and cannot be trusted: "
              + "; ".join(f"[{c}]" for c in result["invalid_citations"]))
    tokens = result["tokens"]
    log(f"\n({result['searches']} search(es), {result['model_calls']} model call(s), {tokens['total']} tokens, "
        f"{result['seconds']} s, citation retries: {result['guardrail']['citation_retries']})")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
