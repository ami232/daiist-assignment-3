import asyncio
import os
import re
import sys
import time
import uuid
from pathlib import Path

from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware, ModelCallLimitMiddleware, ToolCallLimitMiddleware
from langchain_core.messages import AIMessage
from langchain_core.tools import StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
MODEL = os.environ.get("AGENT_MODEL", "gemini-3.5-flash-lite")  # fast on the free tier; gemini-3.5-flash took ~50 s per call
MAX_SEARCHES = 4
MAX_MODEL_CALLS = 8
REFUSAL = "The corpus does not cover this."


# ---------------------------------------------------------------- MCP tools


def mcp_to_langchain(session: ClientSession, tool, trace: list[dict]) -> StructuredTool:
    """Wrap one MCP tool as a LangChain tool that records every call in trace."""

    async def call(**arguments) -> str:
        result = await session.call_tool(tool.name, arguments)
        text = "\n".join(getattr(part, "text", "") for part in result.content)
        trace.append({"tool": tool.name, "args": arguments, "output": text})
        return text

    return StructuredTool.from_function(coroutine=call, name=tool.name,
                                        description=tool.description, args_schema=tool.input_schema)


# ---------------------------------------------------------------- approval


def ask_in_terminal(name: str, args: dict) -> bool:
    """Ask the person at the keyboard; reject when nobody is there to answer."""
    if not sys.stdin.isatty():
        print(f"[approval] {name}({args}) rejected: no one at the keyboard to approve it.", file=sys.stderr)
        return False
    answer = input(f"\nThe agent wants to run {name}({args}). Allow it? [y/N] ")
    return answer.strip().lower() in ("y", "yes")


# ---------------------------------------------------------------- citation guardrail

SEARCH_LINE = re.compile(r"^\[\d+\] (.+)$", re.MULTILINE)
SECTION = re.compile(r"\b\d-\d{3}\.\d{2}\b")
PAGES = re.compile(r"PDF pages? (\d+)(?:-(\d+))?")
PRINTED = re.compile(r"printed page (\d+)\)")
CITATION = re.compile(r"\(([^()]*\bpages? \d[^()]*)\)")


def retrieved_passages(trace: list[dict]) -> list[dict]:
    """Section numbers and page range of every passage the search tool returned."""
    passages = []
    for call in trace:
        if call["tool"] != "search":
            continue
        for line in SEARCH_LINE.findall(call["output"]):
            pages = PAGES.search(line)
            if pages:
                first, last = int(pages.group(1)), int(pages.group(2) or pages.group(1))
                printed = PRINTED.search(line)
                printed_first = int(printed.group(1)) if printed else None
                passages.append({"line": line, "sections": set(SECTION.findall(line)),
                                 "pages": range(first, last + 1),
                                 # the tool prints the printed number of the first page only
                                 "printed": (range(printed_first, printed_first + last - first + 1)
                                             if printed_first is not None else range(0))})
    return passages


def check_citations(answer: str, trace: list[dict]) -> list[str]:
    """Problems with the answer's citations; an empty list means it passes."""
    citations = CITATION.findall(answer)
    if not citations:
        return [] if REFUSAL.lower() in answer.lower() else ["the answer has no citation and is not a refusal"]
    passages = retrieved_passages(trace)
    problems = []
    for citation in citations:
        # A citation may give the PDF page (preferred) or only the printed page number.
        by_printed = "printed page" in citation.lower() and "pdf page" not in citation.lower()
        pages = [int(p) for p in re.findall(r"\d+", citation.split("page", 1)[1])][:2]
        sections = set(SECTION.findall(citation))
        key = "printed" if by_printed else "pages"
        if not any(any(p in passage[key] for p in pages)
                   and (not sections or sections & passage["sections"]) for passage in passages):
            problems.append(f"({citation}) does not match any passage returned by search")
    return problems


# ---------------------------------------------------------------- agent


def final_text(state: dict) -> str:
    for message in reversed(state["messages"]):
        if isinstance(message, AIMessage) and message.text.strip():
            return message.text.strip()
    return ""


def token_usage(state: dict) -> dict:
    usage = {"input": 0, "output": 0}
    for message in state["messages"]:
        meta = getattr(message, "usage_metadata", None) or {}
        usage["input"] += meta.get("input_tokens", 0)
        usage["output"] += meta.get("output_tokens", 0)
    return usage


async def run_agent(question: str, approve=ask_in_terminal) -> dict:
    started = time.time()
    trace: list[dict] = []
    guardrail: list[str] = []
    params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT))
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = [mcp_to_langchain(session, t, trace) for t in (await session.list_tools()).tools]
            load_api_key()
            agent = create_agent(
                ChatGoogleGenerativeAI(model=MODEL),
                tools=tools,
                system_prompt=(ROOT / "AGENTS.md").read_text(encoding="utf-8"),
                middleware=[
                    HumanInTheLoopMiddleware(interrupt_on={"add_document": {"allowed_decisions": ["approve", "reject"]}}),
                    ToolCallLimitMiddleware(run_limit=MAX_SEARCHES),
                    ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS),
                ],
                checkpointer=InMemorySaver(),
            )
            config = {"configurable": {"thread_id": str(uuid.uuid4())}}

            async def invoke(payload) -> dict:
                """Run the agent, answering approval requests until it finishes."""
                result = await agent.ainvoke(payload, config, version="v2")
                while result.interrupts:
                    decisions = []
                    for request in result.interrupts[0].value["action_requests"]:
                        ok = approve(request["name"], request["args"])
                        guardrail.append(f"approval: {request['name']} {'approved' if ok else 'rejected'}")
                        decisions.append({"type": "approve"} if ok else
                                         {"type": "reject", "message": "The user did not approve adding this document."})
                    result = await agent.ainvoke(Command(resume={"decisions": decisions}), config, version="v2")
                return result.value

            state = await invoke({"messages": [{"role": "user", "content": question}]})
            answer = final_text(state)
            # A reply to an add-document request (approved or not) with no search is a
            # report on an action, not a factual answer, so it needs no citation.
            action_only = (any(e.startswith("approval") for e in guardrail)
                           and not any(c["tool"] == "search" for c in trace))
            problems = [] if action_only else check_citations(answer, trace)
            if problems:
                guardrail.append("citation check failed: " + "; ".join(problems))
                state = await invoke({"messages": [{"role": "user", "content": (
                    "Your answer did not pass the citation check: " + "; ".join(problems) + ". "
                    "Rewrite it citing only passages returned by search, exactly as the tool printed "
                    f"their location, or reply '{REFUSAL}' if they do not answer the question.")}]})
                answer = final_text(state)
                problems = check_citations(answer, trace)
                if problems:
                    guardrail.append("citation check failed again: answer replaced by a refusal")
                    answer = (f"{REFUSAL} I could not find a passage in the corpus that supports an "
                              f"answer, so I will not guess. Please check with your local regulatory authority.")
                else:
                    guardrail.append("citation check passed after one retry")

    return {"question": question, "answer": answer, "trace": trace, "guardrail": guardrail,
            "tokens": token_usage(state), "seconds": round(time.time() - started, 1), "model": MODEL}


def ask(question: str, approve=ask_in_terminal) -> dict:
    """Answer one question. Returns answer, tool trace, guardrail events, tokens and seconds."""
    return asyncio.run(run_agent(question, approve))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit('Usage: python agent.py "your question"')
    result = ask(" ".join(sys.argv[1:]))
    print(result["answer"])
    searches = [c["args"].get("query") for c in result["trace"] if c["tool"] == "search"]
    print(f"\n[{len(searches)} searches: {searches} | {result['tokens']['input']}+{result['tokens']['output']} tokens"
          f" | {result['seconds']} s | {MODEL}]", file=sys.stderr)
    for event in result["guardrail"]:
        print(f"[guardrail] {event}", file=sys.stderr)
