"""
Assignment 3: our own agent harness (`main.py ask "question"` runs `python agent.py "question"`).

    LangChain create_agent on Gemini
    tools        search and add_document, taken from server.py over MCP (stdio),
                 exactly as an editor gets them
    system       AGENTS.md
    approval     add_document pauses for a human yes/no (HumanInTheLoopMiddleware);
                 with nobody at the keyboard it is rejected
    limits       at most 8 model calls and 4 searches per run
    guardrail    citation check: every [Page › Section] the answer cites must be a
                 passage that search returned in this conversation, and an answer
                 that is not a refusal must cite something. On failure the model
                 gets one retry, then the answer is replaced by a safe refusal.

answer(question) returns the answer and its full trace (tool calls, retrieved
passages, tokens, seconds, guardrail outcome) for evaluate.py.
"""

import asyncio
import json
import re
import sys
import time
import uuid
from contextlib import AsyncExitStack
from pathlib import Path

from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware, ModelCallLimitMiddleware, ToolCallLimitMiddleware
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.tools import StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
MODEL = "gemini-3.1-flash-lite"  # stable release; gemini-3.5-flash-lite was overloaded (503) when we built this
MODEL_CALL_LIMIT = 8
SEARCH_CALL_LIMIT = 4
REFUSAL = "The handbook does not cover this."
SAFE_REFUSAL = (
    f"{REFUSAL} I could not give an answer that is fully supported by the handbook passages I found, "
    "so I am not answering rather than risk a wrong one. Please ask People Ops (TTS-PeopleOps@gsa.gov)."
)

CITATION_LINE = re.compile(r"^\[\d+\] (.+)$", re.MULTILINE)  # "[1] Leave types › Sick leave" in search results
CITED = re.compile(r"\[([^\[\]\n]+)\]")  # "[Leave types › Sick leave]" in an answer


# ============================================================================
# MCP tools: start server.py and wrap its tools for LangChain
# ============================================================================

class MCPTools:
    """Start server.py over stdio and expose its tools as LangChain tools.

    The same thing an editor does: launch the server as a subprocess, ask it
    which tools it has (name, description, JSON schema of the arguments), and
    forward every call over the MCP session. Use as `async with MCPTools() as tools:`.
    """

    async def __aenter__(self) -> list[StructuredTool]:
        self._stack = AsyncExitStack()
        try:
            params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT))
            read, write = await self._stack.enter_async_context(stdio_client(params))
            self.session = await self._stack.enter_async_context(ClientSession(read, write))
            await self.session.initialize()
            listed = (await self.session.list_tools()).tools
            return [self._wrap(t) for t in listed]
        except BaseException:
            # __aexit__ is not called when __aenter__ fails: close the server
            # connection here, or the error turns into a silent hang at exit.
            await self._stack.aclose()
            raise

    async def __aexit__(self, *exc) -> None:
        await self._stack.aclose()

    def _wrap(self, tool) -> StructuredTool:
        session = self.session

        async def call(**arguments) -> str:
            result = await session.call_tool(tool.name, arguments)
            text = "\n".join(getattr(c, "text", "") for c in result.content)
            return f"Tool error: {text}" if getattr(result, "is_error", False) else text

        return StructuredTool.from_function(
            coroutine=call,
            name=tool.name,
            description=tool.description or "",
            args_schema=tool.input_schema,  # the JSON schema the server announced (MCP 2.x name)
        )


# ============================================================================
# Citation guardrail
# ============================================================================

def normalise(citation: str) -> str:
    return re.sub(r"\s+", " ", citation).strip().lower()


def check_citations(answer: str, retrieved: set[str]) -> list[str]:
    """Problems with the answer's citations; an empty list means it passes.

    `retrieved` holds the normalised citation lines of every passage search
    returned in this conversation.
    """
    cited = [c for c in CITED.findall(answer) if "@" not in c]
    refusal = REFUSAL.lower() in answer.lower()
    problems = [f"[{c}] is not one of the passages returned by search" for c in cited if normalise(c) not in retrieved]
    if not cited and not refusal:
        problems.append("the answer makes claims without citing any passage")
    return problems


# ============================================================================
# The agent
# ============================================================================

def build_agent(tools: list[StructuredTool]):
    # timeout: never hang on a slow call; max_retries: ride out short 429/503 spikes (with backoff)
    model = ChatGoogleGenerativeAI(model=MODEL, api_key=load_api_key(), timeout=60, max_retries=4)
    return create_agent(
        model,
        tools=tools,
        system_prompt=(ROOT / "AGENTS.md").read_text(encoding="utf-8"),
        middleware=[
            HumanInTheLoopMiddleware(interrupt_on={"add_document": True}),
            ModelCallLimitMiddleware(run_limit=MODEL_CALL_LIMIT, exit_behavior="end"),
            ToolCallLimitMiddleware(tool_name="search", run_limit=SEARCH_CALL_LIMIT, exit_behavior="continue"),
        ],
        checkpointer=InMemorySaver(),  # needed to pause for approval and resume
    )


def ask_human(requests: list[dict]) -> list[dict]:
    """One decision per paused tool call. Without a person at the keyboard, reject."""
    decisions = []
    for request in requests:
        args = json.dumps(request.get("args", {}))
        if sys.stdin.isatty():
            reply = input(f"\nThe agent wants to call {request['name']}({args}). Approve? [y/N] ").strip().lower()
            approved = reply in {"y", "yes"}
        else:
            print(f"(no human available to approve {request['name']}({args}): rejected)", file=sys.stderr)
            approved = False
        decisions.append({"type": "approve"} if approved else
                         {"type": "reject", "message": "The user did not approve this call. Do not retry it."})
    return decisions


async def run_turn(agent, config: dict, message, approve) -> None:
    """Run the agent until it finishes, answering approval pauses on the way."""
    result = await agent.ainvoke(message, config, version="v2")
    while getattr(result, "interrupts", None):
        requests = [r for i in result.interrupts for r in i.value["action_requests"]]
        decisions = approve(requests)
        result = await agent.ainvoke(Command(resume={"decisions": decisions}), config, version="v2")


async def answer_async(question: str, approve=ask_human) -> dict:
    started = time.perf_counter()
    async with MCPTools() as tools:
        agent = build_agent(tools)
        config = {"configurable": {"thread_id": str(uuid.uuid4())}}
        await run_turn(agent, config, {"messages": [{"role": "user", "content": question}]}, approve)

        messages = agent.get_state(config).values["messages"]
        final = final_text(messages)
        guardrail, problems = "pass", check_citations(final, retrieved_citations(messages))
        if any(c["name"] == "add_document" for m in messages if isinstance(m, AIMessage) for c in m.tool_calls):
            # The reply reports an action (added, or not approved), not a policy
            # answer, so there is nothing to cite.
            guardrail, problems = "not applicable", []
        if problems:
            # One retry: tell the model exactly what was wrong.
            guardrail = "retried"
            feedback = ("Your answer broke the citation rules: " + "; ".join(problems) + ". "
                        "Rewrite it using only the passages returned by search, citing each claim with a "
                        f"citation line copied exactly, or reply \"{REFUSAL}\" if they do not contain the answer.")
            await run_turn(agent, config, {"messages": [{"role": "user", "content": feedback}]}, approve)
            messages = agent.get_state(config).values["messages"]
            final = final_text(messages)
            problems = check_citations(final, retrieved_citations(messages))
            if problems:
                guardrail, final = "blocked", SAFE_REFUSAL

    ai = [m for m in messages if isinstance(m, AIMessage)]
    usage = [m.usage_metadata or {} for m in ai]
    searches = [m for m in messages if isinstance(m, ToolMessage) and m.name == "search"]
    return {
        "question": question,
        "answer": final,
        "refused": REFUSAL.lower() in final.lower(),
        "guardrail": guardrail,
        "guardrail_problems": problems,
        "tool_calls": [{"name": c["name"], "args": c["args"]} for m in ai for c in m.tool_calls],
        "retrieved": [m.text for m in searches],  # the evidence the judge reads
        "model_calls": len(ai),
        "input_tokens": sum(u.get("input_tokens", 0) for u in usage),
        "output_tokens": sum(u.get("output_tokens", 0) for u in usage),
        "seconds": round(time.perf_counter() - started, 2),
    }


def final_text(messages: list) -> str:
    for m in reversed(messages):
        if isinstance(m, AIMessage) and not m.tool_calls and m.text.strip():
            return m.text.strip()
    return SAFE_REFUSAL  # the call limit ended the run before a final answer


def retrieved_citations(messages: list) -> set[str]:
    found = set()
    for m in messages:
        if isinstance(m, ToolMessage) and m.name == "search":
            found.update(normalise(c) for c in CITATION_LINE.findall(m.text))
    return found


def answer(question: str, approve=ask_human) -> dict:
    """Answer one question. Returns the answer and its trace (see answer_async)."""
    return asyncio.run(answer_async(question, approve))


def sources(result: dict) -> list[str]:
    """'citation: url' for each passage the answer cites, from the search results."""
    urls = {}
    for block in result["retrieved"]:
        for match in re.finditer(r"^\[\d+\] (.+)\nsource: \S+ \| url: (\S+)", block, re.MULTILINE):
            urls[normalise(match.group(1))] = (match.group(1), match.group(2))
    out = []
    for cited in dict.fromkeys(CITED.findall(result["answer"])):
        if normalise(cited) in urls:
            name, url = urls[normalise(cited)]
            out.append(f"{name}: {url}")
    return out


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit('usage: python agent.py "your question"')
    result = answer(" ".join(sys.argv[1:]))
    print(result["answer"])
    cited = sources(result)
    if cited:
        print("\nSources:")
        for line in cited:
            print(f"- {line}")
    print(f"\n({result['model_calls']} model calls, {result['input_tokens']} + {result['output_tokens']} tokens, "
          f"{result['seconds']}s, citation check: {result['guardrail']})", file=sys.stderr)
