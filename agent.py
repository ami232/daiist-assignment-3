"""
Assignment 3: the agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the search and add_document tools from server.py over
MCP and AGENTS.md as the system prompt.

Safeguards:
- approval: add_document pauses (HumanInTheLoopMiddleware) until a person approves it in the
  terminal; with no terminal (evaluation, CI) it is rejected;
- call limits: at most MAX_MODEL_CALLS model calls and MAX_TOOL_CALLS tool calls per run;
- guardrail, citation grounding: every [doc_id, location] in the answer must point to a chunk
  retrieved in this run, and a non-refusal answer must cite something. If not, the agent gets one
  chance to fix it; if it still fails, the answer is replaced by the refusal sentence.

`run_agent(question)` returns the answer and the full trace for evaluate.py.
"""

from __future__ import annotations

import asyncio
import os
import sys
import time
import uuid
from pathlib import Path
from typing import Callable

from langchain.agents import create_agent
from langchain.agents.middleware import HumanInTheLoopMiddleware, ModelCallLimitMiddleware, ToolCallLimitMiddleware
from langchain_core.tools import StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
AGENT_MODEL = os.environ.get("AGENT_MODEL", "gemini-3.5-flash")
MAX_MODEL_CALLS = 8
MAX_TOOL_CALLS = 6
SYSTEM_PROMPT = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
GUARDRAIL_NOTE = ("(The draft answer was withheld because its citations could not be matched to the "
                  "passages retrieved for this question.)")

Approver = Callable[[str, dict], bool]


def terminal_approver(tool: str, args: dict) -> bool:
    """Ask in the terminal; refuse when nobody is there to answer."""
    if not sys.stdin.isatty():
        print(f"[approval] {tool}({args}) rejected: no terminal to ask for approval.", file=sys.stderr)
        return False
    reply = input(f"\nThe agent wants to run {tool}({args}).\nApprove? [y/N] ").strip().lower()
    return reply == "y"


def deny_all(tool: str, args: dict) -> bool:
    return False


def _text(message) -> str:
    text = getattr(message, "text", None)
    if isinstance(text, str):  # langchain-core 1.x: a str property
        return str(text)
    content = message.content
    if isinstance(content, str):
        return content
    return "".join(p.get("text", "") if isinstance(p, dict) else str(p) for p in content)


def mcp_tools(session: ClientSession, listed) -> list[StructuredTool]:
    """Wrap the server's MCP tools as LangChain tools that call it over the open session.
    (langchain-mcp-adapters 0.3.1 does not import with mcp 2.x, so this replaces it.)"""
    tools = []
    for t in listed:
        async def call(_name=t.name, **kwargs) -> str:
            res = await session.call_tool(_name, kwargs)
            text = "\n".join(getattr(c, "text", "") for c in res.content)
            if getattr(res, "is_error", False) or getattr(res, "isError", False):
                return f"Tool error: {text}"
            return text
        tools.append(StructuredTool.from_function(
            coroutine=call, name=t.name, description=t.description or "", args_schema=t.input_schema))
    return tools


def _model():
    load_api_key()
    return ChatGoogleGenerativeAI(model=AGENT_MODEL, temperature=0, max_retries=6)


async def _invoke_with_approval(agent, payload, config, approve: Approver, trace: list) -> object:
    result = await agent.ainvoke(payload, config, version="v2")
    while result.interrupts:
        answers = {}
        for intr in result.interrupts:
            value = intr.value
            name = value.get("name") or value.get("action_requests", [{}])[0].get("name", "?")
            args = value.get("args") or value.get("action_requests", [{}])[0].get("args", {})
            ok = approve(name, args)
            trace.append({"approval": name, "args": args, "approved": ok})
            answers[intr.id] = ({"type": "approve"} if ok else
                                {"type": "reject", "message": "The user did not approve this call. Do not retry it."})
        result = await agent.ainvoke(Command(resume=answers), config, version="v2")
    return result


async def run_agent_async(question: str, approve: Approver = terminal_approver, retriever=None) -> dict:
    import retrieval  # loads the index; imported here so `--help`-style use stays light

    started = time.time()
    retriever = retriever or retrieval.Retriever(retrieval.CHOSEN["design"])
    params = StdioServerParameters(command=sys.executable, args=[str(ROOT / "server.py")], cwd=str(ROOT))
    trace: list[dict] = []
    async with stdio_client(params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()
        tools = mcp_tools(session, (await session.list_tools()).tools)
        agent = create_agent(
            _model(),
            tools=tools,
            system_prompt=SYSTEM_PROMPT,
            middleware=[
                HumanInTheLoopMiddleware(
                    interrupt_on={"add_document": {"allowed_decisions": ["approve", "reject"]}},
                    interrupt_mode="per_call",
                ),
                ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS, exit_behavior="end"),
                ToolCallLimitMiddleware(run_limit=MAX_TOOL_CALLS, exit_behavior="continue"),
            ],
            checkpointer=InMemorySaver(),
        )
        config = {"configurable": {"thread_id": str(uuid.uuid4())}}
        result = await _invoke_with_approval(
            agent, {"messages": [{"role": "user", "content": question}]}, config, approve, trace)

        def collect(messages):
            outputs, calls, usage = [], [], {"input_tokens": 0, "output_tokens": 0}
            for m in messages:
                if m.type == "ai":
                    for tc in getattr(m, "tool_calls", []) or []:
                        calls.append({"tool": tc["name"], "args": tc["args"]})
                    u = getattr(m, "usage_metadata", None) or {}
                    usage["input_tokens"] += u.get("input_tokens", 0)
                    usage["output_tokens"] += u.get("output_tokens", 0)
                elif m.type == "tool":
                    outputs.append(_text(m))
            return outputs, calls, usage

        messages = result.value["messages"]
        answer = _text(messages[-1]).strip() if messages[-1].type == "ai" else ""
        outputs, calls, usage = collect(messages)
        check = retrieval.check_citations(answer, retrieval.retrieved_chunk_ids(outputs), retriever)

        guard = {"fired": False, "reason": "", "retried": False, "withheld": False}
        # A reply that reports an add_document result makes no claims about the documents,
        # so it needs no citation; invented citations are still caught.
        reports_add = any(c["tool"] == "add_document" for c in calls)
        problem = ("no answer" if not answer else
                   f"citations not in the retrieved passages: {', '.join(check['invalid'])}" if check["invalid"] else
                   "the answer cites nothing" if (not check["refusal"] and check["n_citations"] == 0
                                                  and not reports_add) else "")
        if problem:
            guard.update(fired=True, reason=problem, retried=True)
            fix = (f"Guardrail check failed: {problem}. Rewrite your answer so that every claim cites a "
                   f"passage you retrieved, copying [doc_id, location] from the search results; search "
                   f"again if needed. If the passages do not answer the question, reply with the refusal "
                   f"sentence from your rules.")
            result = await _invoke_with_approval(
                agent, {"messages": [{"role": "user", "content": fix}]}, config, approve, trace)
            messages = result.value["messages"]
            answer = _text(messages[-1]).strip() if messages[-1].type == "ai" else ""
            outputs, calls, usage = collect(messages)
            check = retrieval.check_citations(answer, retrieval.retrieved_chunk_ids(outputs), retriever)
            if not answer or check["invalid"] or (not check["refusal"] and check["n_citations"] == 0
                                                  and not reports_add):
                guard["withheld"] = True
                answer = f"{retrieval.REFUSAL} {GUARDRAIL_NOTE}"
                check = retrieval.check_citations(answer, [], retriever)

    return {
        "question": question,
        "answer": answer,
        "model": AGENT_MODEL,
        "tool_calls": calls,
        "approvals": trace,
        "retrieved_chunk_ids": retrieval.retrieved_chunk_ids(outputs),
        "citation_check": check,
        "guardrail": guard,
        "usage": usage,
        "seconds": round(time.time() - started, 2),
    }


def run_agent(question: str, approve: Approver = terminal_approver, retriever=None) -> dict:
    return asyncio.run(run_agent_async(question, approve, retriever))


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit('Usage: python agent.py "your question"')
    out = run_agent(" ".join(sys.argv[1:]))
    print(out["answer"])
    print("\nRetrieved passages:")
    for cid in out["retrieved_chunk_ids"]:
        print(f"  - {cid}")
    g = out["guardrail"]
    if g["fired"]:
        print(f"\n[guardrail] {g['reason']}" + ("; answer withheld." if g["withheld"] else "; fixed on retry."))
    u = out["usage"]
    print(f"\n[{out['model']} | {len(out['tool_calls'])} tool calls | "
          f"{u['input_tokens']} in / {u['output_tokens']} out tokens | {out['seconds']} s]")


if __name__ == "__main__":
    main()
