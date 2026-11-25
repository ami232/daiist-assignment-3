"""
Assignment 3: the agent (`uv run python main.py ask "question"` runs `python agent.py "question"`).

How it works:
  1. Start server.py as an MCP server and connect to it (like your editor does).
  2. Wrap its two tools (search, add_document) as LangChain tools.
  3. Build a LangChain agent on Gemini with AGENTS.md as the system prompt and 3 guardrails:
       a. APPROVAL: a human must say yes before add_document runs (HumanInTheLoopMiddleware).
       b. CALL LIMIT: at most 6 tool calls per question (ToolCallLimitMiddleware),
          so a confused agent cannot loop forever and burn the quota.
       c. CITATION CHECK (our extra guardrail): after the agent answers, code checks that
          every [SOURCE §x] tag it used was really in the search results. If a tag is
          invented, or the answer has no tag and is not a refusal, the answer is blocked.
  4. Print the answer with its citations.

evaluate.py imports `answer_question()` to get the answer, the tool trace, tokens and time.
"""

import asyncio
import os
import re
import sys
import time

from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware, ToolCallLimitMiddleware
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.tools import StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from api_key import load_api_key
from config import CHAT_MODEL, ROOT

REFUSAL = "The corpus does not cover this."
# A citation looks like [ELIQUIS §2.2]  or  [XARELTO §2.1;2.2]
# A citation is any [...] containing "§": [ELIQUIS §2.2], [XARELTO §2.1;2.2],
# or several in one bracket: [PRADAXA §2.5, PRADAXA §12.3] or [PRADAXA §1.2, §14.2].
CITATION = re.compile(r"\[([^\[\]]*§[^\[\]]*)\]")


# =============================================================================
# Citations: shared by the guardrail here and the code checks in evaluate.py
# =============================================================================

def citations_in(text: str) -> set[tuple[str, str]]:
    """All (source, location) pairs in a text.

    "[X §2.1;2.2]"         -> (X, 2.1), (X, 2.2)
    "[X §2.5, X §12.3]"    -> (X, 2.5), (X, 12.3)
    "[X §1.2, §14.2]"      -> (X, 1.2), (X, 14.2)   a part without a name keeps the previous one
    """
    pairs = set()
    for inside in CITATION.findall(text):
        source = None
        for part in re.split(r"[;,]", inside):
            part = part.strip()
            match = re.match(r"(?:([A-Z][A-Z0-9_-]*)\s*)?§\s*(.+)", part)
            if match:                               # "PRADAXA §2.5" or "§14.2"
                source = match.group(1) or source
                location = match.group(2).strip()
            else:                                   # "2.2" after "XARELTO §2.1;"
                location = part
            if source and location:
                pairs.add((source, location))
    return pairs


def apply_guardrail(raw_answer: str, retrieved_text: str) -> tuple[str, bool, str]:
    """The citation guardrail: returns (final answer, fired?, reason)."""
    ok, reason = check_citations(raw_answer, retrieved_text)
    if ok:
        return raw_answer, False, reason
    final = (f"{REFUSAL} (Guardrail: the draft answer {reason}, so it was withheld. "
             "Please check the full prescribing information.)")
    return final, True, reason


def is_refusal(answer: str) -> bool:
    return "does not cover" in answer.lower()


def check_citations(answer: str, retrieved_text: str) -> tuple[bool, str]:
    """Our extra guardrail. Returns (ok, reason)."""
    cited = citations_in(answer)
    allowed = citations_in(retrieved_text)          # the tags that were in the search results
    invented = cited - allowed
    if invented:
        return False, f"cites passages that were never retrieved: {sorted(invented)}"
    if not cited and not is_refusal(answer):
        return False, "gives an answer without any citation"
    return True, "ok"


# =============================================================================
# The agent
# =============================================================================

def mcp_tool_to_langchain(session: ClientSession, tool) -> StructuredTool:
    """Make one MCP tool usable by LangChain: same name, description and arguments."""
    async def call_tool(**arguments):
        result = await session.call_tool(tool.name, arguments)
        return "\n".join(getattr(part, "text", "") for part in result.content)

    return StructuredTool.from_function(coroutine=call_tool, name=tool.name,
                                        description=tool.description, args_schema=tool.input_schema)


def ask_human(action: dict) -> bool:
    """The approval step: show the tool call and wait for y/n in the terminal."""
    if not sys.stdin.isatty():          # no human there (evaluation, check.py) -> say no
        print(f"[approval] {action['name']} {action['args']} -> rejected (no one to approve)", file=sys.stderr)
        return False
    reply = input(f"\nThe agent wants to run {action['name']}({action['args']}). Allow? [y/N] ")
    return reply.strip().lower() in ("y", "yes")


async def answer_question(question: str, approve=ask_human) -> dict:
    """Run the agent on one question. Returns answer, trace, tokens, seconds."""
    load_api_key()                       # puts GEMINI_API_KEY in the environment for LangChain
    started = time.perf_counter()

    # 1. Start server.py and open an MCP session with it.
    # env=os.environ: pass our environment (incl. GEMINI_API_KEY) to the server.
    # By default MCP only passes a few safe variables like PATH.
    server = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT),
                                   env=dict(os.environ))
    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            # 2. Turn the server's tools into LangChain tools.
            mcp_tools = (await session.list_tools()).tools
            tools = [mcp_tool_to_langchain(session, t) for t in mcp_tools]

            # 3. Build the agent.
            agent = create_agent(
                model=ChatGoogleGenerativeAI(model=CHAT_MODEL),   # this model uses fixed sampling settings
                tools=tools,
                system_prompt=(ROOT / "AGENTS.md").read_text(encoding="utf-8"),
                middleware=[
                    # a. pause before add_document and wait for a human decision
                    HumanInTheLoopMiddleware(interrupt_on={"add_document": True}),
                    # b. no more than 6 tool calls for one question
                    ToolCallLimitMiddleware(run_limit=6),
                ],
                checkpointer=InMemorySaver(),    # needed to pause and resume (approval)
            )
            config = {"configurable": {"thread_id": "one-question"}}

            # Run it. If it pauses for approval, ask the human and resume.
            state = await agent.ainvoke({"messages": [{"role": "user", "content": question}]}, config)
            while state.get("__interrupt__"):
                request = state["__interrupt__"][0].value
                decisions = []
                for action in request["action_requests"]:
                    if approve(action):
                        decisions.append({"type": "approve"})
                    else:
                        decisions.append({"type": "reject", "message": "The user did not approve adding this document."})
                state = await agent.ainvoke(Command(resume={"decisions": decisions}), config)

    # 4. Collect what happened: tool calls, tool outputs, tokens.
    messages = state["messages"]
    trace, retrieved, tokens = [], [], {"input": 0, "output": 0, "total": 0}
    for message in messages:
        if isinstance(message, AIMessage):
            for call in message.tool_calls:
                trace.append({"tool": call["name"], "args": call["args"]})
            usage = message.usage_metadata or {}
            tokens["input"] += usage.get("input_tokens", 0)
            tokens["output"] += usage.get("output_tokens", 0)
            tokens["total"] += usage.get("total_tokens", 0)
        if isinstance(message, ToolMessage) and message.name == "search":
            retrieved.append(message.text)

    raw_answer = messages[-1].text.strip() if isinstance(messages[-1], AIMessage) else ""
    retrieved_text = "\n\n".join(retrieved)

    # c. The citation guardrail. It checks answers built from search results. A run that
    #    only managed documents (add_document, no search) reports the tool's result as it is.
    used_tools = {step["tool"] for step in trace}
    if used_tools and "search" not in used_tools:
        final, fired, reason = raw_answer, False, "document management only: not checked"
    else:
        final, fired, reason = apply_guardrail(raw_answer, retrieved_text)

    return {
        "question": question,
        "answer": final,
        "raw_answer": raw_answer,
        "guardrail_fired": fired,
        "guardrail_reason": reason,
        "trace": trace,
        "retrieved_text": retrieved_text,
        "tokens": tokens,
        "seconds": round(time.perf_counter() - started, 1),
    }


def main() -> None:
    question = " ".join(sys.argv[1:]).strip()
    if not question:
        raise SystemExit('Usage: python agent.py "your question"')

    result = asyncio.run(answer_question(question))

    print(result["answer"])
    cited = sorted(citations_in(result["answer"]))
    if cited:
        print("\nSources: " + ", ".join(f"[{s} §{l}]" for s, l in cited))
    if result["guardrail_fired"]:
        print(f"\n[guardrail fired] {result['guardrail_reason']}\n[draft was] {result['raw_answer']}", file=sys.stderr)
    tools_used = ", ".join(f"{t['tool']}({t['args']})" for t in result["trace"]) or "none"
    print(f"\n(tools: {tools_used} | tokens: {result['tokens']['total']} | {result['seconds']} s)")


if __name__ == "__main__":
    main()
