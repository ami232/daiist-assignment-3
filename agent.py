"""
Assignment 3: the corpus agent. `main.py ask "question"` runs `python agent.py "question"`.

LangChain `create_agent` on Gemini. Its tools are server.py's tools, reached over MCP
(stdio) exactly as an editor reaches them, and its system prompt is AGENTS.md.

Safeguards, enforced in code rather than asked for in the prompt:
- approval: add_document pauses until a person approves it (HumanInTheLoopMiddleware).
  With no terminal to ask (check.py, evaluate.py), the call is rejected.
- call limits per question: MAX_SEARCHES searches, MAX_ADDS add_document calls and
  MAX_MODEL_CALLS model calls.
- guardrail (the author's choice): citation check. Every [SOURCE, location] the answer
  cites must be among the passages search returned for this question, and an answer that
  is not a refusal must cite at least one. If not, the answer is blocked: the team sees a
  "could not verify" message instead (kept in `blocked_answer` for evaluation).

Gemini's free tier often answers 503 "high demand", and which models answer changes from
minute to minute. So each model call goes down a chain of Gemini models at once (no slow
per-model retries), and if the whole chain fails it waits and tries the chain again. The
model that answered is recorded with every answer.

evaluate.py uses `CorpusAgent` (one MCP server for many questions) or `ask(question)`;
both return the answer, the tool trace, citations, tokens and seconds.
"""

import asyncio
import os
import re
import sys
import time
import uuid
import warnings
from contextlib import AsyncExitStack
from pathlib import Path

os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")
# google-genai's error path leaves an un-awaited coroutine; the warning is noise, not a bug here.
warnings.filterwarnings("ignore", message="coroutine 'ClientResponse.json' was never awaited")
# Flash-Lite models ignore temperature (fixed sampling), so answers can vary between runs.
warnings.filterwarnings("ignore", message=".*uses fixed sampling defaults.*")

from langchain.agents import create_agent
from langchain.agents.middleware import (
    HumanInTheLoopMiddleware,
    ModelCallLimitMiddleware,
    ModelFallbackMiddleware,
    ModelRetryMiddleware,
    ToolCallLimitMiddleware,
)
from langchain_core.tools import StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
SYSTEM_PROMPT = (ROOT / "AGENTS.md").read_text(encoding="utf-8")

# Pinned model names, not "-latest" aliases: an alias can change model mid-evaluation.
MODEL = os.environ.get("AGENT_MODEL", "gemini-3.5-flash-lite")
FALLBACK_MODELS = ["gemini-3.5-flash", "gemini-3.8-flash", "gemini-3.1-flash-lite"]
MAX_SEARCHES = 6      # a two-part question needs 2-4; more means the agent is flailing
MAX_ADDS = 1
MAX_MODEL_CALLS = 10

BLOCKED_MESSAGE = ("I cannot give this answer: its sources could not be verified against the corpus "
                   "({reason}). Please check the regulation directly or ask a regulatory expert.")

# Phrases that mark a refusal ("the corpus does not cover this"); evaluate.py reuses is_refusal.
REFUSAL_RE = re.compile(
    r"(corpus|documents?|passages?|search results?|sources?) (do|does|did)(\s+not|n['’]?t) (cover|contain|"
    r"include|address|answer|specify|establish|provide|mention|say)|not covered|cannot (give|answer|confirm|"
    r"determine|find)|can['’]t (give|answer|confirm|determine|find)|could not (find|finish|verify|confirm)|"
    r"unable to (answer|find|confirm|determine)|no (information|passage)s? (on|about|in)|"
    r"not (in|within) the corpus|outside (the )?(scope|corpus)",
    re.IGNORECASE)

# "[REG_1169_2011, Article 21]", "[ALLERGEN_NOTICE_2017, Section 3.1 (part 2)]", and two in
# one bracket, which the model sometimes writes: "[REG_1169_2011, Article 21; QA_NOTICE_2018, Section 2.1]"
BRACKET_RE = re.compile(r"\[([^\[\]]+)\]")
CITATION_RE = re.compile(r"^\s*([A-Z][A-Z0-9_]+),\s*(.+?)\s*$")


def base_location(location: str) -> str:
    """'Section 3.1 (part 2)' -> 'Section 3.1': long sections are split into parts."""
    return location.split(" (part")[0].strip()


def citations_in(text: str) -> list[tuple[str, str]]:
    """Every (source, location) cited in the text, in order."""
    found = []
    for inside in BRACKET_RE.findall(text):
        for piece in inside.split(";"):
            m = CITATION_RE.match(piece)
            if m:
                found.append((m.group(1), base_location(m.group(2))))
    return found


def chat_model(name: str) -> ChatGoogleGenerativeAI:
    # temperature 0: the same question should get the same answer, which evaluation needs.
    # max_retries=0: on a 503 move on to the next model now; ModelRetryMiddleware waits.
    return ChatGoogleGenerativeAI(model=name, temperature=0, max_retries=0, timeout=60,
                                  google_api_key=load_api_key())


def terminal_approval(name: str, args: dict) -> bool:
    """Ask the person at the terminal; without one (check.py, evaluate.py), refuse."""
    if not sys.stdin.isatty():
        print(f"[approval] {name}({args}) needs a person's approval; none available, so rejected.",
              file=sys.stderr)
        return False
    reply = input(f"\nThe agent wants to run {name} with {args}.\nAllow it? [y/N] ")
    return reply.strip().lower() in {"y", "yes", "s", "si", "sí"}


def is_refusal(answer: str) -> bool:
    """Does the answer say the corpus does not cover the question (fully or in part)?"""
    return bool(REFUSAL_RE.search(answer))


def retrieved_labels(trace: list[dict]) -> set[tuple[str, str]]:
    return {(r["source"], base_location(r["location"]))
            for step in trace for r in step.get("results", [])}


def guardrail(question: str, answer: str, trace: list[dict]) -> tuple[str, str | None]:
    """Citation check. Returns (answer to show, reason it fired or None)."""
    retrieved = retrieved_labels(trace)
    invalid = [f"[{s}, {loc}]" for s, loc in dict.fromkeys(citations_in(answer)) if (s, loc) not in retrieved]
    # A reply about adding a document ("Added X: 12 chunks") is not a corpus answer to cite.
    adding = any(step["tool"] == "add_document" for step in trace)
    if invalid:
        reason = "cited but not retrieved: " + ", ".join(invalid)
    elif not citations_in(answer) and not is_refusal(answer) and not adding:
        reason = "the answer cites no source"
    else:
        return answer, None
    return BLOCKED_MESSAGE.format(reason=reason), reason


class CorpusAgent:
    """One MCP connection to server.py and one agent, reused for many questions."""

    def __init__(self, approve=terminal_approval, model=None):
        self.approve = approve
        self.model = model  # a LangChain chat model; tests pass a fake one
        self.trace: list[dict] = []
        self._stack = AsyncExitStack()

    async def __aenter__(self):
        params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT))
        read, write = await self._stack.enter_async_context(stdio_client(params))
        self.session = await self._stack.enter_async_context(ClientSession(read, write))
        await self.session.initialize()
        tools = [self._as_langchain_tool(t) for t in (await self.session.list_tools()).tools]
        middleware = [
            HumanInTheLoopMiddleware(interrupt_on={"add_document": True}),
            ToolCallLimitMiddleware(tool_name="search", run_limit=MAX_SEARCHES, exit_behavior="continue"),
            ToolCallLimitMiddleware(tool_name="add_document", run_limit=MAX_ADDS, exit_behavior="continue"),
            ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS, exit_behavior="end"),
        ]
        if self.model is None:
            # Order matters: the retry wraps the fallback, so a retry re-runs the whole chain.
            middleware += [
                ModelRetryMiddleware(max_retries=4, initial_delay=10.0, max_delay=60.0, on_failure="error"),
                ModelFallbackMiddleware(*[chat_model(m) for m in FALLBACK_MODELS]),
            ]
        self.agent = create_agent(self.model or chat_model(MODEL), tools, system_prompt=SYSTEM_PROMPT,
                                  middleware=middleware, checkpointer=InMemorySaver())
        return self

    async def __aexit__(self, *exc):
        await self._stack.aclose()

    def _as_langchain_tool(self, mcp_tool) -> StructuredTool:
        """Wrap an MCP tool so LangChain can call it, logging every call in self.trace."""
        async def run(**args):
            started = time.perf_counter()
            result = await self.session.call_tool(mcp_tool.name, args)
            text = "\n".join(getattr(c, "text", "") for c in result.content)
            labels = re.findall(r"cite as \[([^,\]]+), ([^\]]+)\] \| similarity ([\d.]+)", text)
            self.trace.append({
                "tool": mcp_tool.name, "args": args, "seconds": round(time.perf_counter() - started, 2),
                "results": [{"source": s, "location": loc, "similarity": float(sim)} for s, loc, sim in labels],
                "output": text,
            })
            return text

        return StructuredTool(name=mcp_tool.name, description=mcp_tool.description,
                              args_schema=mcp_tool.input_schema, coroutine=run)

    async def ask(self, question: str) -> dict:
        """Answer one question. Returns answer, trace, citations, tokens and seconds."""
        self.trace = []
        config = {"configurable": {"thread_id": str(uuid.uuid4())}}
        started = time.perf_counter()
        try:
            result = await self.agent.ainvoke({"messages": [{"role": "user", "content": question}]},
                                              config, version="v2")
            while result.interrupts:  # add_document is waiting for a decision
                decisions = []
                for request in result.interrupts[0].value["action_requests"]:
                    approved = self.approve(request["name"], request["args"])
                    self.trace.append({"tool": request["name"], "args": request["args"], "approved": approved})
                    decisions.append({"type": "approve"} if approved else
                                     {"type": "reject", "message": "The user did not approve this call."})
                result = await self.agent.ainvoke(Command(resume={"decisions": decisions}), config,
                                                  version="v2")
        except Exception as error:  # every model in the chain failed, even after waiting
            return {"question": question, "answer": "", "blocked_answer": None, "refusal": False,
                    "error": f"{type(error).__name__}: {str(error)[:300]}",
                    "guardrail": None, "citations": [], "trace": self.trace, "models": [],
                    "searches": sum(step["tool"] == "search" for step in self.trace), "model_calls": 0,
                    "input_tokens": 0, "output_tokens": 0, "seconds": round(time.perf_counter() - started, 1)}

        messages = result.value["messages"]
        final = messages[-1]
        answer = final.text.strip() if final.type == "ai" else ""
        if not answer:
            answer = ("I could not finish: the call limit was reached before an answer. "
                      "The corpus may not cover this question.")
        shown, fired = guardrail(question, answer, self.trace)

        usage = [m.usage_metadata for m in messages if m.type == "ai" and m.usage_metadata]
        retrieved = retrieved_labels(self.trace)
        cited = citations_in(answer)  # of the model's answer, even if the guardrail blocked it
        models = sorted({m.response_metadata.get("model_name", "?") for m in messages if m.type == "ai"})
        return {
            "question": question,
            "answer": shown,
            "blocked_answer": answer if fired else None,
            "refusal": is_refusal(shown),
            "error": None,
            "guardrail": fired,
            "models": models,
            "citations": [{"source": s, "location": loc, "retrieved": (s, loc) in retrieved}
                          for s, loc in dict.fromkeys(cited)],
            "trace": self.trace,
            "searches": sum(step["tool"] == "search" for step in self.trace),
            "model_calls": len([m for m in messages if m.type == "ai"]),
            "input_tokens": sum(u["input_tokens"] for u in usage),
            "output_tokens": sum(u["output_tokens"] for u in usage),
            "seconds": round(time.perf_counter() - started, 1),
        }


async def ask_async(question: str, approve=terminal_approval) -> dict:
    async with CorpusAgent(approve=approve) as agent:
        return await agent.ask(question)


def ask(question: str, approve=terminal_approval) -> dict:
    """One question, one server: for main.py ask. evaluate.py should reuse a CorpusAgent."""
    return asyncio.run(ask_async(question, approve))


def print_result(r: dict) -> None:
    if r["error"]:
        print(f"No answer: the language model failed ({r['error']}). "
              "Gemini's free tier is often overloaded; try again in a few minutes.")
        return
    print(r["answer"])
    if r["citations"] and not r["guardrail"]:
        print("\nCitations:")
        for c in r["citations"]:
            note = "" if c["retrieved"] else "  <- NOT in the retrieved passages"
            print(f"  [{c['source']}, {c['location']}]{note}")
    if r["guardrail"]:
        print(f"\n[guardrail fired: {r['guardrail']}]")
    queries = [step["args"].get("query") for step in r["trace"] if step["tool"] == "search"]
    print(f"\n({r['searches']} searches: {queries}; {r['model_calls']} model calls on "
          f"{', '.join(r['models'])}; {r['input_tokens']}+{r['output_tokens']} tokens; {r['seconds']} s)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit('usage: python agent.py "your question"')
    result = ask(" ".join(sys.argv[1:]))
    print_result(result)
    sys.exit(1 if result["error"] else 0)
