"""
Assignment 3: your agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the tools of server.py over MCP and
AGENTS.md as system prompt.

Safeguards:
  * approval   a person must approve every add_document call (HumanInTheLoopMiddleware).
  * limits     at most MAX_MODEL_CALLS model calls and MAX_TOOL_CALLS tool calls per question.
  * citations  (the extra guardrail) the answer is checked in code: every citation
               [source | location] must be a passage the agent retrieved in this run, and an
               answer that is not a refusal must have citations. One repair attempt; if it
               still fails, the answer is replaced by a notice instead of being shown.
  * input      empty or oversized questions are rejected before any model call.

`run_agent` returns an AgentResult (answer, tool trace, tokens, seconds) for evaluate.py.
"""

from __future__ import annotations

import asyncio
import os
import re
import sys
import time
import uuid
from contextlib import asynccontextmanager
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Callable

ROOT = Path(__file__).resolve().parent

AGENT_MODEL = os.environ.get("RAG_AGENT_MODEL", "gemini-3.5-flash-lite")
AGENT_TEMPERATURE = float(os.environ.get("RAG_AGENT_TEMPERATURE", "0"))   # 0: repeatable evaluation
MAX_MODEL_CALLS = 8
MAX_TOOL_CALLS = 6
MAX_QUESTION_CHARS = 1500
REFUSAL_PHRASE = "i don't know based on the indexed documents"
BLOCKED_MESSAGE = (
    "I could not produce an answer whose citations I can verify against the passages I retrieved, "
    "so I am not giving one. Please rephrase the question or ask about a specific article."
)
SERVER_ARGS = ["server.py"]  # tests replace this

_CITATION = re.compile(r"\[([^\[\]|\n]{1,60}?)\s*\|\s*([^\[\]\n]{1,120}?)\]")


# ----------------------------------------------------------------- results ---
@dataclass
class AgentResult:
    question: str
    answer: str = ""
    refused: bool = False
    blocked: bool = False
    citations: list[list[str]] = field(default_factory=list)
    invalid_citations: list[str] = field(default_factory=list)
    tool_calls: list[dict] = field(default_factory=list)
    retrieved: list[dict] = field(default_factory=list)
    guardrails: list[str] = field(default_factory=list)
    model_calls: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    seconds: float = 0.0
    error: str = ""

    @property
    def total_tokens(self) -> int:
        return self.input_tokens + self.output_tokens

    def as_dict(self) -> dict:
        d = asdict(self)
        d["total_tokens"] = self.total_tokens
        return d


# ---------------------------------------------------------- approval hooks ---
def deny_all(requests: list[dict]) -> list[dict]:
    return [{"type": "reject", "message": "No person was available to approve this call."} for _ in requests]


def approve_all(requests: list[dict]) -> list[dict]:
    return [{"type": "approve"} for _ in requests]


def ask_in_terminal(requests: list[dict]) -> list[dict]:
    """Show each gated call and wait for a yes. Without a terminal the answer is no."""
    decisions = []
    for req in requests:
        print(f"\nThe agent wants to run {req['name']}({req['args']}).", file=sys.stderr)
        print("This adds a document to the index and uses embedding quota.", file=sys.stderr)
        if not sys.stdin.isatty():
            print("No terminal to ask on: rejected.", file=sys.stderr)
            decisions.append({"type": "reject", "message": "No person was available to approve this call."})
            continue
        answer = input("Approve? [y/N] ").strip().lower()
        decisions.append({"type": "approve"} if answer in {"y", "yes", "s", "si", "sí"} else
                         {"type": "reject", "message": "The user rejected this call."})
    return decisions


# ------------------------------------------------------------------- tools ---
def _clean_schema(schema: dict) -> dict:
    """Keep what Gemini function declarations accept; the MCP schema carries extra keywords."""
    keep = {"type", "description", "enum", "items", "properties", "required"}
    out = {k: v for k, v in schema.items() if k in keep}
    if "properties" in out:
        out["properties"] = {name: _clean_schema(p) for name, p in out["properties"].items()}
    if "items" in out and isinstance(out["items"], dict):
        out["items"] = _clean_schema(out["items"])
    return out


def _wrap_tool(session, tool):
    from langchain_core.tools import StructuredTool

    async def call(**kwargs):
        result = await session.call_tool(tool.name, {k: v for k, v in kwargs.items() if v is not None})
        text = "\n".join(getattr(c, "text", "") for c in result.content).strip()
        return f"Error: {text}" if getattr(result, "is_error", False) else text

    return StructuredTool.from_function(
        coroutine=call, name=tool.name, description=tool.description or tool.name,
        args_schema=_clean_schema(tool.input_schema or {"type": "object", "properties": {}}),
    )


@asynccontextmanager
async def mcp_tools(server_env: dict | None = None):
    """Start server.py over stdio, as an editor would, and yield its tools as LangChain tools."""
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    params = StdioServerParameters(
        command=sys.executable, args=SERVER_ARGS, cwd=str(ROOT), env={**os.environ, **(server_env or {})}
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = (await session.list_tools()).tools
            yield [_wrap_tool(session, t) for t in tools]


# ------------------------------------------------------------ verification ---
def extract_citations(answer: str) -> list[tuple[str, str]]:
    return [(m.group(1).strip(), m.group(2).strip()) for m in _CITATION.finditer(answer)]


def is_refusal(answer: str) -> bool:
    return answer.strip().lower().replace("’", "'").startswith(REFUSAL_PHRASE)


def check_citations(citations: list[tuple[str, str]], retrieved: list[dict]) -> list[str]:
    """Citations that do not match any retrieved passage (same source, same article / annex / recital)."""
    import retrieval as rt

    seen = [(rt.norm_source(h["source"]), rt.unit_of(h["location"])) for h in retrieved]
    bad = []
    for source, location in citations:
        if (rt.norm_source(source), rt.unit_of(location)) not in seen:
            bad.append(f"[{source} | {location}]")
    return bad


def _message_text(message) -> str:
    try:
        return (message.text or "").strip()
    except AttributeError:
        content = getattr(message, "content", "")
        return content.strip() if isinstance(content, str) else ""


def _collect(result: AgentResult, messages: list) -> None:
    """Fill trace, retrieved passages and token counts from the message history."""
    import retrieval as rt
    from langchain_core.messages import AIMessage, ToolMessage

    result.tool_calls, result.retrieved = [], []
    result.model_calls = result.input_tokens = result.output_tokens = 0
    names: dict[str, dict] = {}
    for m in messages:
        if isinstance(m, AIMessage):
            result.model_calls += 1
            usage = getattr(m, "usage_metadata", None) or {}
            result.input_tokens += int(usage.get("input_tokens", 0))
            result.output_tokens += int(usage.get("output_tokens", 0))
            for call in m.tool_calls or []:
                entry = {"name": call["name"], "args": call["args"], "result": ""}
                names[call["id"]] = entry
                result.tool_calls.append(entry)
        elif isinstance(m, ToolMessage):
            entry = names.get(m.tool_call_id)
            text = m.content if isinstance(m.content, str) else str(m.content)
            if entry is not None:
                entry["result"] = text
                if text.startswith("Tool call limit exceeded"):
                    entry["refused_by_limit"] = True
                    if "call_limit" not in result.guardrails:
                        result.guardrails.append("call_limit")
                elif entry["name"] == "search":
                    result.retrieved.extend(rt.parse_hits(text))


# ------------------------------------------------------------------- agent ---
def build_model():
    from langchain_google_genai import ChatGoogleGenerativeAI

    from api_key import load_api_key

    return ChatGoogleGenerativeAI(model=AGENT_MODEL, temperature=AGENT_TEMPERATURE, google_api_key=load_api_key(), max_retries=6)


async def run_agent(
    question: str,
    approve: Callable[[list[dict]], list[dict]] = deny_all,
    model=None,
    server_env: dict | None = None,
) -> AgentResult:
    """Answer one question. `approve` decides add_document calls; `model` lets tests inject a fake."""
    from langchain.agents import create_agent
    from langchain.agents.middleware import HumanInTheLoopMiddleware, ModelCallLimitMiddleware, ToolCallLimitMiddleware
    from langchain_core.messages import HumanMessage
    from langgraph.checkpoint.memory import InMemorySaver
    from langgraph.types import Command

    result = AgentResult(question=question)
    started = time.time()
    question = (question or "").strip()
    if not question or len(question) > MAX_QUESTION_CHARS:
        result.answer = "Please ask a question of up to %d characters." % MAX_QUESTION_CHARS
        result.guardrails.append("input_rejected")
        return result

    system_prompt = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    async with mcp_tools(server_env) as tools:
        agent = create_agent(
            model or build_model(),
            tools,
            system_prompt=system_prompt,
            middleware=[
                HumanInTheLoopMiddleware(
                    interrupt_on={"add_document": {"allowed_decisions": ["approve", "reject"]}},
                    description_prefix="Adding a document needs approval",
                    interrupt_mode="batched",
                ),
                ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS, exit_behavior="end"),
                ToolCallLimitMiddleware(run_limit=MAX_TOOL_CALLS, exit_behavior="continue"),
            ],
            checkpointer=InMemorySaver(),
        )
        config = {"configurable": {"thread_id": str(uuid.uuid4())}}

        async def turn(payload) -> dict:
            """One invocation, answering approval requests until the agent is done."""
            state = await agent.ainvoke(payload, config)
            while state.get("__interrupt__"):
                requests = [r for intr in state["__interrupt__"] for r in intr.value["action_requests"]]
                result.guardrails.extend(f"approval_requested:{r['name']}" for r in requests)
                decisions = approve(requests)
                result.guardrails.extend(f"approval_{d['type']}" for d in decisions)
                state = await agent.ainvoke(Command(resume={"decisions": decisions}), config)
            return state

        try:
            state = await turn({"messages": [HumanMessage(question)]})
            _collect(result, state["messages"])
            answer = _message_text(state["messages"][-1])
            if "limits exceeded" in answer.lower() and "call_limit" not in result.guardrails:
                result.guardrails.append("call_limit")

            # Guardrail: citations must be real, and an answer needs them.
            for attempt in range(2):
                result.refused = is_refusal(answer)
                cites = extract_citations(answer)
                bad = check_citations(cites, result.retrieved)
                result.citations, result.invalid_citations = [list(c) for c in cites], bad
                added = any(c["name"] == "add_document" and not c.get("refused_by_limit") for c in result.tool_calls) and not result.retrieved
                if result.refused or (cites and not bad) or (added and not bad):
                    break
                if attempt == 0:
                    result.guardrails.append("citation_repair")
                    problem = (f"These citations are not in the passages you retrieved: {', '.join(bad)}." if bad
                               else "Your answer has no citations.")
                    state = await turn({"messages": [HumanMessage(
                        f"{problem} Use search if you need passages, then answer again using only retrieved passages "
                        f"cited as [source | location], or reply that you don't know according to the rules.")]})
                    _collect(result, state["messages"])
                    answer = _message_text(state["messages"][-1])
                else:
                    result.guardrails.append("citation_blocked")
                    result.blocked = True
                    answer = BLOCKED_MESSAGE
            result.answer = answer
        except Exception as error:  # noqa: BLE001 - evaluate.py must keep going; the error is recorded
            result.error = f"{type(error).__name__}: {error}"
            result.answer = result.answer or f"(agent error: {type(error).__name__})"
    result.seconds = round(time.time() - started, 2)
    return result


def format_answer(result: AgentResult) -> str:
    lines = [result.answer.strip()]
    if result.citations and not result.blocked:
        lines.append("\nSources:")
        shown = dict.fromkeys(tuple(c) for c in result.citations)
        lines.extend(f"  - {s} | {loc}" for s, loc in shown)
    return "\n".join(lines)


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit('usage: python agent.py "your question"')
    question = " ".join(sys.argv[1:])
    result = asyncio.run(run_agent(question, approve=ask_in_terminal))
    print(format_answer(result))
    ran = [c for c in result.tool_calls if not c.get("refused_by_limit")]
    calls = ", ".join(f"{c['name']}({c['args'].get('query') or c['args'].get('path', '')})" for c in ran)
    print(f"\n[{result.model_calls} model calls, {len(ran)} tool calls: {calls or 'none'}; "
          f"{result.total_tokens} tokens; {result.seconds:.1f}s; guardrails: {', '.join(result.guardrails) or 'none'}]",
          file=sys.stderr)
    if result.error:
        raise SystemExit(f"Agent failed: {result.error}")


if __name__ == "__main__":
    main()
