"""Assignment 3: the shipwreck-law assistant (`main.py ask "question"`), a LangChain agent on Gemini using server.py's tools over MCP."""

import asyncio
import re
import sys
import time
import uuid
from contextlib import AsyncExitStack
from pathlib import Path

from langchain.agents import create_agent
from langchain.agents.middleware import (
    HumanInTheLoopMiddleware,
    ModelCallLimitMiddleware,
    ModelRetryMiddleware,
    ToolCallLimitMiddleware,
)
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.tools import StructuredTool
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parent
MODEL = "gemini-3.5-flash-lite"
SERVER_COMMAND = [sys.executable, str(ROOT / "server.py")]
MAX_MODEL_CALLS = 8
MAX_SEARCHES = 4
MODEL_RETRIES = 5
RETRY_FIRST_DELAY = 5.0
TRANSIENT = ("429", "500", "502", "503", "504", "UNAVAILABLE", "RESOURCE_EXHAUSTED", "DEADLINE_EXCEEDED")
SOURCES = ("Ley 16/1985", "Ley 14/2014", "UNESCO 2001", "UNCLOS")
REFUSAL = "the documents don't cover"
BLOCKED = (
    "No verified answer: my draft cited passages that the search did not return, "
    "so the citation check blocked it. Please check the official texts or rephrase the question."
)


def chat_model(name: str = MODEL):
    from langchain_google_genai import ChatGoogleGenerativeAI

    from api_key import load_api_key

    return ChatGoogleGenerativeAI(model=name, api_key=load_api_key(), retries=6, request_timeout=120)


def transient(error: Exception) -> bool:
    message = str(error)
    if "PerDay" in message:
        return False
    if any(code in message for code in TRANSIENT):
        print(f"  Gemini is busy ({message[:60]}...); waiting and retrying", file=sys.stderr)
        return True
    return False


def ask_terminal(name: str, args: dict) -> bool:
    if not sys.stdin.isatty():
        print(f"{name}({args}) needs your approval, but there is no terminal to ask: rejected.", file=sys.stderr)
        return False
    print(f"\nThe assistant wants to run {name} with {args}. Allow it? [y/N] ", end="", file=sys.stderr, flush=True)
    return sys.stdin.readline().strip().lower() in ("y", "yes")


def mcp_tool(session: ClientSession, tool) -> StructuredTool:
    async def call(**kwargs) -> str:
        result = await session.call_tool(tool.name, kwargs)
        text = "\n".join(getattr(c, "text", "") for c in result.content).strip()
        return f"Error: {text}" if result.is_error else text

    return StructuredTool.from_function(
        coroutine=call, name=tool.name, description=tool.description, args_schema=tool.input_schema
    )


def normalize(label: str) -> str:
    return re.sub(r"\s+", " ", label).strip().lower()


def retrieved_citations(messages: list) -> dict[str, tuple[str, str]]:
    found = {}
    for m in messages:
        if not (isinstance(m, ToolMessage) and m.name == "search"):
            continue
        for block in str(m.content).split("\n\n---\n\n"):
            cite = re.search(r"^Cite as: (.+)$", block, re.M)
            link = re.search(r"^Link: (.+)$", block, re.M)
            for label in re.findall(r"\[([^\[\]]+)\]", cite.group(1) if cite else ""):
                found[normalize(label)] = (f"[{label.strip()}]", link.group(1).strip() if link else "")
    return found


def cited_labels(answer: str, sources: set[str]) -> dict[str, str]:
    labels = {}
    for inside in re.findall(r"\[([^\[\]]+)\]", answer):
        for part in inside.split(";"):
            key = normalize(part)
            if any(key.startswith(s + ",") for s in sources):
                labels.setdefault(key, f"[{part.strip()}]")
    return labels


def check_citations(answer: str, messages: list) -> dict:
    retrieved = retrieved_citations(messages)
    sources = {normalize(s) for s in SOURCES} | {label.split(",")[0] for label in retrieved}
    cited = cited_labels(answer, sources)
    unverified = [c for c in cited if c not in retrieved]
    refusal = REFUSAL in answer.replace("’", "'").lower()
    if unverified:
        reason = "cites passages the search did not return: " + "; ".join(cited[c] for c in unverified)
    elif not cited and not refusal:
        reason = "makes claims without any citation"
    else:
        reason = ""
    return {"ok": not reason, "reason": reason, "cited": list(cited), "unverified": [cited[c] for c in unverified], "refusal": refusal}


def final_text(messages: list) -> str:
    for m in reversed(messages):
        if isinstance(m, AIMessage) and not m.tool_calls:
            return m.text.strip()
    return ""


def tool_calls(messages: list) -> list[dict]:
    return [{"tool": c["name"], "args": c["args"]} for m in messages if isinstance(m, AIMessage) for c in m.tool_calls]


class Assistant:
    def __init__(self, approve=ask_terminal, model: str = MODEL):
        self.approve = approve
        self.model = model

    async def __aenter__(self):
        self._stack = AsyncExitStack()
        params = StdioServerParameters(command=SERVER_COMMAND[0], args=SERVER_COMMAND[1:], cwd=str(ROOT))
        read, write = await self._stack.enter_async_context(stdio_client(params))
        self.session = await self._stack.enter_async_context(ClientSession(read, write))
        await self.session.initialize()
        tools = [mcp_tool(self.session, t) for t in (await self.session.list_tools()).tools]
        self.agent = create_agent(
            model=chat_model(self.model) if isinstance(self.model, str) else self.model,
            tools=tools,
            system_prompt=(ROOT / "AGENTS.md").read_text(encoding="utf-8"),
            middleware=[
                ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS, exit_behavior="end"),
                ToolCallLimitMiddleware(tool_name="search", run_limit=MAX_SEARCHES),
                ModelRetryMiddleware(
                    max_retries=MODEL_RETRIES, retry_on=transient, on_failure="error",
                    initial_delay=RETRY_FIRST_DELAY, backoff_factor=2.0, max_delay=60.0,
                ),
                HumanInTheLoopMiddleware(interrupt_on={"add_document": {"allowed_decisions": ["approve", "reject"]}}),
            ],
            checkpointer=InMemorySaver(),
        )
        return self

    async def __aexit__(self, *exc):
        await self._stack.aclose()

    async def _run(self, payload, config: dict, approvals: list) -> dict:
        result = await self.agent.ainvoke(payload, config)
        while result.get("__interrupt__"):
            decisions = []
            for interrupt in result["__interrupt__"]:
                for action in interrupt.value["action_requests"]:
                    ok = self.approve(action["name"], action["args"])
                    approvals.append({"tool": action["name"], "args": action["args"], "approved": ok})
                    decisions.append(
                        {"type": "approve"} if ok
                        else {"type": "reject", "message": "The user did not approve this, so nothing was added."}
                    )
            result = await self.agent.ainvoke(Command(resume={"decisions": decisions}), config)
        return result

    async def ask(self, question: str) -> dict:
        started = time.time()
        config = {"configurable": {"thread_id": uuid.uuid4().hex}}
        approvals, guardrail = [], []
        result = await self._run({"messages": [HumanMessage(question)]}, config, approvals)
        answer = final_text(result["messages"])
        check = check_citations(answer, result["messages"])
        if not check["ok"]:
            guardrail.append({"attempt": 1, "answer": answer, **check})
            feedback = (
                f"Your answer {check['reason']}. Rewrite it citing only 'Cite as' labels from your search "
                "results in this conversation, searching again if you need to, or say the documents don't cover it."
            )
            result = await self._run({"messages": [HumanMessage(feedback)]}, config, approvals)
            answer = final_text(result["messages"])
            check = check_citations(answer, result["messages"])
            if not check["ok"]:
                guardrail.append({"attempt": 2, "answer": answer, **check})
                answer = BLOCKED
        messages = result["messages"]
        retrieved = retrieved_citations(messages)
        usage = [m.usage_metadata or {} for m in messages if isinstance(m, AIMessage)]
        return {
            "question": question,
            "answer": answer,
            "citations": [retrieved[c] for c in check["cited"] if c in retrieved] if check["ok"] else [],
            "refusal": check["refusal"] if check["ok"] else True,
            "retrieved": [label for label, _ in retrieved.values()],
            "evidence": [str(m.content) for m in messages if isinstance(m, ToolMessage) and m.name == "search"],
            "tool_calls": tool_calls(messages),
            "approvals": approvals,
            "guardrail": guardrail,
            "blocked": not check["ok"],
            "model_calls": len(usage),
            "input_tokens": sum(u.get("input_tokens", 0) for u in usage),
            "output_tokens": sum(u.get("output_tokens", 0) for u in usage),
            "seconds": round(time.time() - started, 2),
        }


async def answer(question: str, approve=ask_terminal) -> dict:
    async with Assistant(approve) as assistant:
        return await assistant.ask(question)


def print_answer(r: dict) -> None:
    for call in r["tool_calls"]:
        print(f"  tool: {call['tool']}({call['args']})", file=sys.stderr)
    for event in r["guardrail"]:
        print(f"  citation check, attempt {event['attempt']}: answer {event['reason']}", file=sys.stderr)
    print(r["answer"])
    if r["citations"]:
        print("\nSources:")
        for label, link in r["citations"]:
            print(f"- {label} {link}".rstrip())
    tokens = r["input_tokens"] + r["output_tokens"]
    print(f"\n({r['model_calls']} model calls, {tokens:,} tokens, {r['seconds']:.1f}s)", file=sys.stderr)


def main() -> int:
    question = " ".join(sys.argv[1:]).strip()
    if not question:
        print('Usage: uv run python agent.py "your question"', file=sys.stderr)
        return 2
    try:
        result = asyncio.run(answer(question))
    except Exception as error:
        print(f"Gemini could not answer: {str(error)[:300]}", file=sys.stderr)
        print("If it says 503 or high demand, wait a few minutes and run it again.", file=sys.stderr)
        return 1
    print_answer(result)
    return 0


if __name__ == "__main__":
    sys.exit(main())