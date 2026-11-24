"""
Assignment 3: the agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the tools of server.py over MCP (stdio)
and AGENTS.md as the system prompt.

Safeguards:
- approval before add_document runs (HumanInTheLoopMiddleware + checkpointer);
  without a terminal the call is rejected automatically;
- call limits: 6 model calls and 4 searches per run;
- citation guardrail: every [doc_id | location] in the final answer must match a
  chunk retrieved in this run, and a non-refusal answer must cite something.
  One retry with a correction, then the answer is replaced by the refusal.

For evaluate.py:

    async with Agent() as agent:          # one MCP session for many questions
        result = await agent.answer("...")
    result = await answer("...")           # one-off
"""

from __future__ import annotations

import asyncio
import os
import warnings
import re
import sys
import time
import uuid
from pathlib import Path

from langchain.agents import create_agent
from langchain.agents.middleware import (
    AgentMiddleware,
    HumanInTheLoopMiddleware,
    ModelCallLimitMiddleware,
    ToolCallLimitMiddleware,
)
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.tools import StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from pydantic import BaseModel, Field

import rag
from api_key import load_api_key

warnings.filterwarnings("ignore", category=RuntimeWarning)
warnings.filterwarnings("ignore", message=".*fixed sampling defaults.*")  # noise from the SDK when a call is retried

ROOT = Path(__file__).resolve().parent
REFUSAL = "The corpus does not cover this."

# Free-tier limits decide the model: the full Flash models allow 20 requests a
# day, the Flash-Lite models 500. An evaluation run needs about 150. If a model's
# daily quota is used up, the next one in the list takes over.
MODELS = [m.strip() for m in os.environ.get(
    "AGENT_MODELS", "gemini-3.5-flash-lite,gemini-3.1-flash-lite,gemini-3-flash-preview"
).split(",") if m.strip()]
MAX_MODEL_CALLS = 6
MAX_SEARCHES = 4
RATE_LIMIT_RETRIES = 5


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


# --------------------------------------------------------------------------
# Model, with backoff on per-minute limits and fallback on daily limits
# --------------------------------------------------------------------------

_models: dict[str, ChatGoogleGenerativeAI] = {}
_active_model = 0  # index in MODELS; moves forward when a daily quota is used up
_used_models: list[str] = []  # the model behind each successful call


def chat_model(name: str) -> ChatGoogleGenerativeAI:
    if name not in _models:
        _models[name] = ChatGoogleGenerativeAI(
            model=name, temperature=0, google_api_key=load_api_key(), max_retries=1,
        )
    return _models[name]


def current_model_name() -> str:
    return MODELS[min(_active_model, len(MODELS) - 1)]


def _is_rate_limit(error: Exception) -> bool:
    text = str(error)
    return "429" in text or "RESOURCE_EXHAUSTED" in text


def _is_overloaded(error: Exception) -> bool:
    text = str(error)
    return "503" in text or "UNAVAILABLE" in text or "overloaded" in text.lower()


def _is_daily(error: Exception) -> bool:
    return "PerDay" in str(error)


def _retry_delay(error: Exception, attempt: int) -> float:
    match = re.search(r"retry in ([0-9.]+)s|retryDelay['\"]?: ['\"]?([0-9.]+)s", str(error))
    if match:
        return min(float(match.group(1) or match.group(2)) + 2, 70)
    return min(10 * 2 ** attempt, 70)


class QuotaAwareModel(AgentMiddleware):
    """Wait and retry on per-minute 429s and 503s; switch model on a daily 429."""

    async def awrap_model_call(self, request, handler):
        global _active_model
        waits = overloads = 0
        detour = 0  # for this call only: step past a model that is overloaded right now
        while True:
            name = MODELS[min(_active_model + detour, len(MODELS) - 1)]
            try:
                response = await handler(request.override(model=chat_model(name)))
                _used_models.append(name)
                return response
            except Exception as error:  # noqa: BLE001 - sorted below
                if _is_rate_limit(error) and _is_daily(error):
                    if _active_model + 1 >= len(MODELS):
                        raise RuntimeError(
                            f"The daily Gemini quota is used up for all of: {', '.join(MODELS)}. "
                            "Try again after 09:00 Madrid."
                        ) from error
                    _active_model += 1
                    detour = 0
                    log(f"  daily quota used up for {name}; switching to {current_model_name()}")
                    continue
                if _is_overloaded(error) and overloads < 6:
                    overloads += 1
                    if overloads % 2 == 0 and _active_model + detour + 1 < len(MODELS):
                        detour += 1
                        log(f"  {name} is overloaded (503); using {MODELS[_active_model + detour]} for this call")
                    else:
                        await asyncio.sleep(3 * overloads)
                    continue
                if _is_rate_limit(error) and waits < RATE_LIMIT_RETRIES:
                    wait = _retry_delay(error, waits)
                    waits += 1
                    log(f"  {name}: per-minute limit; waiting {wait:.0f}s (try {waits}/{RATE_LIMIT_RETRIES})")
                    await asyncio.sleep(wait)
                    continue
                raise


# --------------------------------------------------------------------------
# Citation guardrail
# --------------------------------------------------------------------------

def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().lower()


def is_refusal(answer: str) -> bool:
    return _norm(REFUSAL.rstrip(".")) in _norm(answer)


def check_citations(answer: str, retrieved: list[dict]) -> str:
    """'' if the answer passes, else the reason it fails."""
    allowed = {(_norm(c["doc_id"]), _norm(loc)) for c in retrieved for loc in c["locations"]}
    cited = rag.parse_citations(answer)
    unknown = [f"[{doc} | {loc}]" for doc, loc in cited if (_norm(doc), _norm(loc)) not in allowed]
    if unknown:
        return "cites passages that were not retrieved: " + ", ".join(unknown)
    if not cited and not is_refusal(answer):
        return "makes claims without any citation"
    return ""


def _allowed_tags(retrieved: list[dict]) -> str:
    tags = dict.fromkeys(f"[{c['doc_id']} | {loc}]" for c in retrieved for loc in c["locations"])
    return ", ".join(tags) or "none (nothing was retrieved)"


# --------------------------------------------------------------------------
# The agent
# --------------------------------------------------------------------------

class SearchArgs(BaseModel):
    query: str = Field(description="Short description of the rule you are looking for, in English.")


class AddDocumentArgs(BaseModel):
    path: str = Field(description="Path of a .pdf, .html, .htm, .txt or .md file inside the repository.")


def _message_text(message) -> str:
    content = message.content
    if isinstance(content, str):
        return content.strip()
    parts = []
    for part in content or []:
        if isinstance(part, str):
            parts.append(part)
        elif isinstance(part, dict) and part.get("type") == "text":
            parts.append(part.get("text", ""))
    return "".join(parts).strip()


class Agent:
    """Keeps one MCP session to server.py open and answers questions with it."""

    def __init__(self, interactive: bool = False) -> None:
        self.interactive = interactive
        self._stack = None
        self._session: ClientSession | None = None
        self._graph = None
        self._trace: list[dict] = []

    async def __aenter__(self) -> "Agent":
        from contextlib import AsyncExitStack

        self._stack = AsyncExitStack()
        params = StdioServerParameters(
            command=sys.executable, args=["server.py"], cwd=str(ROOT), env=dict(os.environ),
        )
        read, write = await self._stack.enter_async_context(stdio_client(params))
        self._session = await self._stack.enter_async_context(ClientSession(read, write))
        await self._session.initialize()
        listed = {tool.name: tool for tool in (await self._session.list_tools()).tools}
        tools = [
            StructuredTool.from_function(
                coroutine=self._caller(name), name=name,
                description=listed[name].description or name, args_schema=schema,
            )
            for name, schema in (("search", SearchArgs), ("add_document", AddDocumentArgs))
            if name in listed
        ]
        self._graph = create_agent(
            chat_model(current_model_name()),
            tools,
            system_prompt=(ROOT / "AGENTS.md").read_text(encoding="utf-8"),
            middleware=[
                ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS, exit_behavior="end"),
                ToolCallLimitMiddleware(tool_name="search", run_limit=MAX_SEARCHES, exit_behavior="continue"),
                HumanInTheLoopMiddleware(
                    interrupt_on={"add_document": {"allowed_decisions": ["approve", "reject"]}},
                    description_prefix="add_document changes the index and needs approval",
                ),
                QuotaAwareModel(),
            ],
            checkpointer=InMemorySaver(),
        )
        return self

    async def __aexit__(self, *exc) -> None:
        if self._stack is not None:
            await self._stack.aclose()
        self._stack = self._session = self._graph = None

    def _caller(self, name: str):
        async def call(**kwargs) -> str:
            result = await self._session.call_tool(name, kwargs)
            text = "\n".join(getattr(c, "text", "") for c in result.content).strip()
            self._trace.append({"name": name, "args": kwargs, "output": text})
            return text

        return call

    # ---- approval ---------------------------------------------------------

    def _decide(self, request: dict, interactive: bool) -> dict:
        path = (request.get("args") or {}).get("path", "?")
        self._trace.append({"name": "approval_request", "args": {"tool": request.get("name"), "path": path}, "output": ""})
        if interactive and sys.stdin.isatty():
            print(f"\nThe assistant wants to add a document to the index:\n  path: {path}")
            try:
                reply = input("Approve? [y/N] ").strip().lower()
            except EOFError:
                reply = ""
            approved = reply in ("y", "yes")
        else:
            approved = False
            log(f"  add_document({path}) needs approval and no terminal is attached: rejected.")
        self._trace[-1]["output"] = "approved" if approved else "rejected"
        if approved:
            return {"type": "approve"}
        return {"type": "reject", "message": "The user did not approve adding this document. Do not retry."}

    async def _run(self, payload, config: dict, interactive: bool) -> dict:
        state = await self._graph.ainvoke(payload, config)
        while state.get("__interrupt__"):
            decisions = []
            for interrupt in state["__interrupt__"]:
                for request in interrupt.value.get("action_requests", []):
                    decisions.append(self._decide(request, interactive))
            state = await self._graph.ainvoke(Command(resume={"decisions": decisions}), config)
        return state

    # ---- one question -------------------------------------------------------

    async def answer(self, question: str, interactive: bool | None = None) -> dict:
        interactive = self.interactive if interactive is None else interactive
        started = time.time()
        self._trace = []
        first_call = len(_used_models)
        config = {"configurable": {"thread_id": uuid.uuid4().hex}, "recursion_limit": 40}

        state = await self._run({"messages": [HumanMessage(question)]}, config, interactive)

        def collect() -> tuple[str, list[dict]]:
            final = next((m for m in reversed(state["messages"]) if isinstance(m, AIMessage)), None)
            retrieved: dict[str, dict] = {}
            for call in self._trace:
                if call["name"] == "search":
                    for chunk in rag.parse_results(call["output"]):
                        retrieved.setdefault(chunk["chunk_id"], chunk)
            return (_message_text(final) if final else ""), list(retrieved.values())

        text, retrieved = collect()
        raw_answer = text
        events: list[dict] = []
        wants_to_add = any(c["name"] in ("add_document", "approval_request") for c in self._trace)

        if not wants_to_add:  # an add-document reply states no facts from the corpus
            problem = check_citations(text, retrieved)
            if problem:
                events.append({"reason": problem, "action": "retry", "answer": text})
                correction = (
                    f"Your answer {problem}. Rewrite it using only the search results of this conversation. "
                    f"Every claim needs a tag copied exactly from this list: {_allowed_tags(retrieved)}. "
                    f"If the results do not answer the question, reply exactly: {REFUSAL}"
                )
                state = await self._run({"messages": [HumanMessage(correction)]}, config, interactive)
                text, retrieved = collect()
                problem = check_citations(text, retrieved)
                if problem:
                    events.append({"reason": problem, "action": "replaced", "answer": text})
                    text = REFUSAL

        usage_in = usage_out = model_calls = 0
        for message in state["messages"]:
            usage = getattr(message, "usage_metadata", None) if isinstance(message, AIMessage) else None
            if usage:
                model_calls += 1
                usage_in += usage.get("input_tokens", 0)
                usage_out += usage.get("output_tokens", 0)

        return {
            "question": question,
            "answer": text,
            "raw_answer": raw_answer,
            "refused": is_refusal(text),
            "citations": [f"[{doc} | {loc}]" for doc, loc in rag.parse_citations(text)],
            "retrieved": [
                {k: c[k] for k in ("chunk_id", "doc_id", "doc_title", "location", "locations", "score", "text")}
                for c in retrieved
            ],
            "tool_calls": [
                {"name": c["name"], "args": c["args"], "output_chars": len(c["output"]),
                 **({"output": c["output"]} if c["name"] != "search" else {})}
                for c in self._trace
            ],
            "model": ",".join(dict.fromkeys(_used_models[first_call:])) or current_model_name(),
            "model_calls": model_calls,
            "input_tokens": usage_in,
            "output_tokens": usage_out,
            "seconds": round(time.time() - started, 2),
            "guardrail_fired": bool(events),
            "guardrail_events": events,
        }


async def answer(question: str, interactive: bool = False) -> dict:
    """Answer one question with a fresh MCP session. For many questions use `Agent`."""
    async with Agent(interactive=interactive) as agent:
        return await agent.answer(question)


def format_sources(result: dict) -> str:
    cited = rag.parse_citations(result["answer"])
    if not cited:
        return "Sources: none."
    titles = {}
    for chunk in result["retrieved"]:
        for location in chunk["locations"]:
            titles[(chunk["doc_id"], location)] = chunk["doc_title"]
    lines = ["Sources:"]
    for doc, loc in cited:
        lines.append(f"  [{doc} | {loc}]  {titles.get((doc, loc), '')}".rstrip())
    return "\n".join(lines)


def main() -> None:
    question = " ".join(sys.argv[1:]).strip()
    if not question:
        raise SystemExit('Usage: python agent.py "your question"')
    result = asyncio.run(answer(question, interactive=True))
    print(result["answer"])
    print()
    print(format_sources(result))
    for event in result["guardrail_events"]:
        log(f"[guardrail] answer {event['reason']} -> {event['action']}")
    log(f"[{result['model']}: {result['model_calls']} model calls, "
        f"{sum(1 for c in result['tool_calls'] if c['name'] == 'search')} searches, "
        f"{result['input_tokens']} tokens in, {result['output_tokens']} out, {result['seconds']}s]")


if __name__ == "__main__":
    main()
