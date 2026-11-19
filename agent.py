"""
Assignment 3: the agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the tools of server.py reached over MCP
and AGENTS.md as the system prompt. Safety layers, all in code (not in the prompt):

  1. Approval: add_document only runs after the user types "y" at the terminal.
     When there is no terminal (evaluate.py, CI), it is refused automatically.
  2. Call limits: at most MAX_MODEL_CALLS model calls and MAX_TOOL_CALLS tool calls per question.
  3. Citation guardrail: every [label] in the answer must be one the search tool returned.
     An invented citation, or a non-refusal with no citation at all, replaces the
     answer with the standard refusal.

evaluate.py imports `answer_all(questions)`, which returns the answer, the tool trace,
tokens and seconds for each question.
"""

import asyncio
import os
import re
import sys
import time
from contextlib import asynccontextmanager
from pathlib import Path

from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware, ToolCallLimitMiddleware
from langchain_core.messages import AIMessage
from langchain_core.tools import StructuredTool
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
SYSTEM_PROMPT = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
CHAT_MODEL = os.environ.get("GEMINI_CHAT_MODEL", "gemini-3.5-flash-lite")
MAX_MODEL_CALLS = 8
MAX_TOOL_CALLS = 6

REFUSAL = "The product information in the corpus does not cover this; please ask the pharmacist or doctor."
REFUSAL_MARKERS = ["does not cover", "do not cover", "not covered", "no cubre", "no cubren", "no incluye"]
BRACKET = re.compile(r"\[([^\[\]]+)\]")
LABEL = re.compile(r"^\s*([a-z0-9_\-]+) p\.(\d+) (.+?)\s*$", re.IGNORECASE)


# ---------------------------------------------------------------- model

def make_model():
    from langchain_google_genai import ChatGoogleGenerativeAI
    return ChatGoogleGenerativeAI(model=CHAT_MODEL, temperature=0, max_retries=6,
                                  google_api_key=load_api_key())


# ---------------------------------------------------------------- MCP tools, with approval

def approve(path: str) -> bool:
    """Ask the human before the index is changed. No terminal means no approval."""
    if not sys.stdin.isatty():
        return False
    reply = input(f"\nThe agent wants to run add_document({path!r}). This changes the index "
                  f"and uses embedding quota. Approve? [y/N] ")
    return reply.strip().lower() in {"y", "yes", "s", "si", "sí"}


def langchain_tools(session: ClientSession, mcp_tools, trace: list[dict]) -> list[StructuredTool]:
    """Wrap each MCP tool as a LangChain tool that records every call in `trace`."""

    def wrap(tool):
        async def call(**arguments):
            if tool.name == "add_document" and not approve(arguments.get("path", "")):
                output = "Not run: the user did not approve adding this document."
            else:
                result = await session.call_tool(tool.name, arguments)
                output = "\n".join(c.text for c in result.content if getattr(c, "text", None))
            trace.append({"tool": tool.name, "arguments": arguments, "output": output})
            return output

        return StructuredTool.from_function(coroutine=call, name=tool.name,
                                            description=tool.description or tool.name,
                                            args_schema=tool.input_schema)

    return [wrap(t) for t in mcp_tools]


@asynccontextmanager
async def corpus_server():
    """Start server.py once and keep the MCP session open."""
    params = StdioServerParameters(command=sys.executable, args=[str(ROOT / "server.py")], cwd=str(ROOT))
    with open(os.devnull, "w") as quiet:
        async with stdio_client(params, errlog=quiet) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                yield session


# ---------------------------------------------------------------- guardrail

def labels_in(text: str) -> set[str]:
    """Citation labels in a text, normalised. One bracket may hold several, as in
    [eliquis p.12 SmPC 4.5, eliquis p.44 SmPC 4.5]."""
    labels = set()
    for bracket in BRACKET.findall(text):
        for part in re.split(r"[;,]\s*(?=[a-z0-9_\-]+ p\.\d)", bracket, flags=re.IGNORECASE):
            match = LABEL.match(part)
            if match:
                labels.add(f"{match.group(1)} p.{match.group(2)} {match.group(3)}".lower())
    return labels


def is_refusal(text: str) -> bool:
    """A refusal says the corpus does not cover the question and cites nothing.
    ("Pradaxa is not covered" next to a cited answer about Eliquis is not a refusal.)"""
    return not labels_in(text) and any(marker in text.lower() for marker in REFUSAL_MARKERS)


def check_citations(text: str, trace: list[dict]) -> tuple[str, str | None]:
    """Return (answer to show, reason it was blocked or None)."""
    if any(step["tool"] == "add_document" for step in trace):
        return text, None      # an index operation, not a medical answer: report its outcome as it is
    retrieved = set().union(*(labels_in(step["output"]) for step in trace if step["tool"] == "search"))
    cited = labels_in(text)
    invented = sorted(cited - retrieved)
    if invented:
        return REFUSAL, f"blocked: cited passages that search never returned: {', '.join(invented)}"
    if not cited and not is_refusal(text):
        return REFUSAL, "blocked: an answer with no citation"
    return text, None


# ---------------------------------------------------------------- one question

def message_text(message) -> str:
    return str(message.text or "").strip()


async def ask(question: str, session: ClientSession, mcp_tools) -> dict:
    trace: list[dict] = []
    agent = create_agent(
        make_model(),
        tools=langchain_tools(session, mcp_tools, trace),
        system_prompt=SYSTEM_PROMPT,
        middleware=[ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS, exit_behavior="end"),
                    ToolCallLimitMiddleware(run_limit=MAX_TOOL_CALLS, exit_behavior="continue")],
    )
    started = time.time()
    state = await agent.ainvoke({"messages": [{"role": "user", "content": question}]})
    seconds = time.time() - started

    ai_messages = [m for m in state["messages"] if isinstance(m, AIMessage)]
    raw = next((message_text(m) for m in reversed(ai_messages) if message_text(m)), "")
    final, blocked = check_citations(raw, trace)
    usage = [m.usage_metadata or {} for m in ai_messages]
    return {
        "question": question,
        "answer": final,
        "raw_answer": raw,
        "guardrail": blocked or "",
        "citations": sorted(labels_in(final)),
        "trace": trace,
        "model_calls": len(ai_messages),
        "input_tokens": sum(u.get("input_tokens", 0) for u in usage),
        "output_tokens": sum(u.get("output_tokens", 0) for u in usage),
        "seconds": round(seconds, 1),
    }


async def answer_all_async(questions: list[str], pause: float = 0.0) -> list[dict]:
    async with corpus_server() as session:
        mcp_tools = (await session.list_tools()).tools
        results = []
        for i, question in enumerate(questions):
            results.append(await ask(question, session, mcp_tools))
            if pause and i < len(questions) - 1:
                await asyncio.sleep(pause)      # stay under the free tier's requests per minute
        return results


def answer_all(questions: list[str], pause: float = 0.0) -> list[dict]:
    """For evaluate.py: one server for all questions."""
    return asyncio.run(answer_all_async(questions, pause))


def answer(question: str) -> dict:
    return answer_all([question])[0]


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit('Usage: uv run python agent.py "your question"')
    result = answer(" ".join(sys.argv[1:]))
    print(result["answer"])
    print("\nSources:", ", ".join(result["citations"]) or "none")
    if result["guardrail"]:
        print(f"Guardrail: {result['guardrail']}")
    searches = [s["arguments"].get("query") for s in result["trace"] if s["tool"] == "search"]
    print(f"\n({len(result['trace'])} tool calls: {searches}; {result['model_calls']} model calls; "
          f"{result['input_tokens']}+{result['output_tokens']} tokens; {result['seconds']} s)")


if __name__ == "__main__":
    main()
