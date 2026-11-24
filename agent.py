"""
Assignment 3: the agent (`main.py ask "question"` runs `python agent.py "question"`).

A LangChain `create_agent` on Gemini. It starts server.py over MCP and uses its
two tools (search, add_document), with AGENTS.md as the system prompt.

Harness:
- Approval: add_document never runs without a person approving it
  (HumanInTheLoopMiddleware). When nobody can be asked, as in the evaluation,
  the answer is "no".
- Call limits: at most MAX_TOOL_CALLS tool calls and MAX_MODEL_CALLS model calls
  per question, so a confused agent cannot loop and burn quota.
- Guardrail (my choice): citation check. Every (document, p. N) in the answer
  must be a page the search actually returned in this run. If the answer cites
  a page that was never retrieved, or makes claims without any citation, it is
  replaced by a refusal.

`answer_question(question)` returns the answer and the tool trace, for evaluate.py.
"""

import asyncio
import re
import sys
import time
from pathlib import Path

from langchain.agents import create_agent
from langchain.agents.middleware import (
    HumanInTheLoopMiddleware,
    ModelCallLimitMiddleware,
    ModelFallbackMiddleware,
    ModelRetryMiddleware,
    ToolCallLimitMiddleware,
)
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.tools import StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
SYSTEM_PROMPT = (ROOT / "AGENTS.md").read_text(encoding="utf-8")

MODEL = "gemini-flash-lite-latest"  # answered fastest in model_check.py; flash-latest kept returning 503
FALLBACK_MODEL = "gemini-flash-latest"  # used if the main model is overloaded (503) or rate-limited
MAX_TOOL_CALLS = 4  # enough for two searches per part of a two-part question
MAX_MODEL_CALLS = 6
REFUSAL = "The EIC documents I have do not cover this."


# ---------- MCP tools as LangChain tools ----------

def passages_in(text: str) -> list[tuple[str, int]]:
    """(title, page) of every passage in a search result, from lines like '[1] Title, p. 79'."""
    return [(t.strip(), int(p)) for t, p in re.findall(r"^\[\d+\] (.+), p\. (\d+)$", text, re.M)]


def make_tool(session: ClientSession, tool, trace: list) -> StructuredTool:
    """Wrap one MCP tool so LangChain can call it; every call is recorded in `trace`."""

    async def call(**kwargs) -> str:
        result = await session.call_tool(tool.name, kwargs)
        text = "\n".join(getattr(c, "text", "") for c in result.content).strip()
        trace.append({"tool": tool.name, "args": kwargs, "passages": passages_in(text), "result": text})
        return text

    return StructuredTool.from_function(
        coroutine=call, name=tool.name, description=tool.description or "", args_schema=tool.input_schema,
    )


# ---------- guardrail: citations must point to retrieved pages ----------

CITATION = re.compile(r"([A-Z][^;()\n]*?),\s*pp?\.\s*(\d+)")


def citations_in(answer: str) -> list[tuple[str, int]]:
    """(title, page) of every citation inside parentheses, e.g. (EIC Work Programme 2027, p. 88)."""
    found = []
    for group in re.findall(r"\(([^()]*\bp\.\s*\d+[^()]*)\)", answer):
        found += [(t.strip(), int(p)) for t, p in CITATION.findall(group)]
    return found


def same_document(cited: str, retrieved: str) -> bool:
    """Loose title match, so 'Guide for Applicants v6.0' matches 'EIC Accelerator Guide for Applicants v6.0'."""
    words = lambda s: {w for w in re.findall(r"[a-z0-9]+", s.lower()) if w not in {"eic", "the", "for", "of"}}
    a, b = words(cited), words(retrieved)
    return bool(a) and (a <= b or b <= a or len(a & b) >= 2)


def check_citations(answer: str, trace: list) -> tuple[str, str]:
    """Return (answer to show, guardrail note). The note is empty when the answer passes."""
    if answer.strip().startswith(REFUSAL):
        return answer, ""
    retrieved = {p for call in trace if call["tool"] == "search" for p in call["passages"]}
    cited = citations_in(answer)
    if not cited:
        return f"{REFUSAL} (The draft answer had no citations, so it was withheld.)", "no citations"
    unknown = [c for c in cited if not any(c[1] == page and same_document(c[0], title) for title, page in retrieved)]
    if unknown:
        listed = "; ".join(f"{t}, p. {p}" for t, p in unknown)
        return (f"{REFUSAL} (The draft answer cited pages the search never returned: {listed}.)",
                f"cited pages not retrieved: {listed}")
    return answer, ""


# ---------- the agent ----------

def ask_terminal(name: str, args: dict) -> bool:
    """Approval step for a person at the terminal."""
    print(f"\nThe agent wants to run {name} with {args}.", file=sys.stderr)
    try:
        reply = input("Approve? [y/N] ")
    except EOFError:  # no terminal to ask (e.g. a script): treat as "no"
        return False
    return reply.strip().lower() in {"y", "yes"}


def text_of(message: AIMessage) -> str:
    content = message.content
    if isinstance(content, list):
        content = "".join(part.get("text", "") if isinstance(part, dict) else str(part) for part in content)
    return content.strip()


async def run(question: str, approve) -> dict:
    trace: list = []
    started = time.time()
    params = StdioServerParameters(command=sys.executable, args=[str(ROOT / "server.py")], cwd=str(ROOT))
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = [make_tool(session, t, trace) for t in (await session.list_tools()).tools]
            key = load_api_key()
            model = ChatGoogleGenerativeAI(model=MODEL, api_key=key, temperature=0, max_retries=2)
            fallback = ChatGoogleGenerativeAI(model=FALLBACK_MODEL, api_key=key, temperature=0, max_retries=2)
            agent = create_agent(
                model,
                tools,
                system_prompt=SYSTEM_PROMPT,
                middleware=[
                    HumanInTheLoopMiddleware(interrupt_on={"add_document": True}),
                    ToolCallLimitMiddleware(run_limit=MAX_TOOL_CALLS, exit_behavior="end"),
                    ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS, exit_behavior="end"),
                    ModelFallbackMiddleware(fallback),  # if the main model keeps failing, use the lighter one
                    ModelRetryMiddleware(max_retries=3, initial_delay=5, on_failure="error"),  # wait and retry busy errors
                ],
                checkpointer=InMemorySaver(),
            )
            config = {"configurable": {"thread_id": "1"}}
            state = await agent.ainvoke({"messages": [HumanMessage(question)]}, config)
            while state.get("__interrupt__"):  # paused before add_document: ask for approval
                decisions = []
                for pause in state["__interrupt__"]:
                    for request in pause.value["action_requests"]:
                        if approve(request["name"], request["args"]):
                            decisions.append({"type": "approve"})
                        else:
                            decisions.append({"type": "reject", "message": "The user did not approve adding this document."})
                state = await agent.ainvoke(Command(resume={"decisions": decisions}), config)

    ai_messages = [m for m in state["messages"] if isinstance(m, AIMessage)]
    draft = next((text_of(m) for m in reversed(ai_messages) if text_of(m)), "") or REFUSAL
    answer, guardrail = check_citations(draft, trace)
    usage = [m.usage_metadata or {} for m in ai_messages]
    return {
        "question": question,
        "answer": answer,
        "draft_answer": draft,
        "guardrail": guardrail,
        "trace": trace,
        "model_calls": len(ai_messages),
        "input_tokens": sum(u.get("input_tokens", 0) for u in usage),
        "output_tokens": sum(u.get("output_tokens", 0) for u in usage),
        "seconds": round(time.time() - started, 1),
    }


def answer_question(question: str, approve=None) -> dict:
    """Answer one question. `approve(name, args) -> bool` decides on add_document; default: never."""
    return asyncio.run(run(question, approve or (lambda name, args: False)))


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit('Usage: python agent.py "your question"')
    result = answer_question(" ".join(sys.argv[1:]), approve=ask_terminal)
    print(result["answer"])
    cited = list(dict.fromkeys(citations_in(result["answer"])))
    if cited:
        print("\nSources:")
        for title, page in cited:
            print(f"- {title}, p. {page}")
    if result["guardrail"]:
        print(f"\n[guardrail] {result['guardrail']}", file=sys.stderr)


if __name__ == "__main__":
    main()
