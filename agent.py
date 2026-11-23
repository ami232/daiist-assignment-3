"""
Assignment 3: the agent (`main.py ask "question"` runs `python agent.py "question"`).

Built from session 10's 07-own-harness/harness.py: LangChain create_agent on
Gemini, the two tools of server.py over MCP, and AGENTS.md as system prompt.

Guardrails (all run by the harness, so the model cannot skip them):
  1. Approval: add_document only runs if a person types "y". With nobody at the
     keyboard (e.g. during evaluation) it is refused.
  2. Call limit: at most 8 model calls per question, against runaway loops.
  3. Citation check: every [source, location] in the answer must have appeared
     in a search result during this question. If one did not, the agent gets one
     chance to fix its answer; if it still fails, the answer is flagged.

ask() returns the answer, the tool trace, the citation check and the token use,
so evaluate.py can grade and cost every answer.
"""

import asyncio
import re
import sys
import time
from contextlib import AsyncExitStack
from pathlib import Path

from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware, wrap_tool_call
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain.mcp import MCPAdapter  # beta; warns on import
from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
MODEL = "gemini-3.5-flash-lite"  # fast, cheap, generous free-tier quota (same as the class harness)
SERVER = ROOT / "server.py"
NEEDS_APPROVAL = {"add_document"}  # changes the index every later answer depends on
MAX_MODEL_CALLS = 8


# 1. Tools: start server.py and wrap its MCP tools as LangChain tools.
async def load_mcp_tools(stack: AsyncExitStack) -> list:
    adapter = await stack.enter_async_context(MCPAdapter(SERVER))
    return await adapter.list_tools()


# 2. Guardrail: a person approves add_document before it runs.
def approval_guardrail(auto_approve: bool):
    @wrap_tool_call
    async def ask_before_adding(request, handler):
        call = request.tool_call
        if call["name"] in NEEDS_APPROVAL and not auto_approve:
            if sys.stdin.isatty():
                answer = input(f"  Allow {call['name']}({call['args']})? [y/N] ")
            else:
                answer = ""  # nobody to ask: refuse rather than add silently
            if answer.strip().lower() != "y":
                return ToolMessage(
                    content="The user refused this tool call. Do not add the document another way.",
                    tool_call_id=call["id"],
                    status="error",
                )
        return await handler(request)

    return ask_before_adding


# 3. The agent: model + tools + AGENTS.md + guardrails.
def build_agent(tools: list, auto_approve: bool = False):
    return create_agent(
        model=ChatGoogleGenerativeAI(model=MODEL, api_key=load_api_key()),
        tools=tools,
        system_prompt=(ROOT / "AGENTS.md").read_text(),
        middleware=[
            approval_guardrail(auto_approve),
            ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS),
        ],
    )


# 4. Guardrail: check the citations against what search actually returned.
RESULT_LINE = re.compile(r"^\[\d+\] (.+?)(?: \| |$)", re.MULTILINE)  # "[1] <source>, <location> | ..."
CITATION = re.compile(r"\[([^\[\]]+?, [^\[\]]+?)\]")                    # "[<source>, <location>]"


def retrieved_citations(messages: list) -> set[str]:
    """Every '<source>, <location>' that a search result showed in this conversation."""
    return {m for msg in messages if isinstance(msg, ToolMessage) for m in RESULT_LINE.findall(msg.text)}


def answer_citations(answer: str, sources: set[str]) -> list[str]:
    """Citations in the answer. A bracket holding several ('[A, Art 5, B, Section 4]' or
    '[A, Art 5; B, Section 4]') is split where a known source name starts."""
    cited = []
    for bracket in CITATION.findall(answer):
        for part in bracket.split(";"):
            for source in sources:
                part = part.replace(f", {source}, ", f"\n{source}, ")
            cited += [p.strip() for p in part.split("\n") if p.strip()]
    return list(dict.fromkeys(cited))


SUBDIVISION = re.compile(r"(\(\w+\))*")  # "(1)(b)" after "Article 7"


def supported(cited: str, retrieved: set[str]) -> bool:
    """True if the citation is a retrieved one, or narrows it to a paragraph:
    'Article 7(1)(b)' is fine when 'Article 7' was retrieved; 'Article 70' is not."""
    return any(cited == r or (cited.startswith(r) and SUBDIVISION.fullmatch(cited[len(r):]))
               for r in retrieved)


def check_citations(answer: str, messages: list) -> dict:
    retrieved = retrieved_citations(messages)
    cited = answer_citations(answer, {r.rsplit(", ", 1)[0] for r in retrieved})
    bad = [c for c in cited if not supported(c, retrieved)]
    return {"cited": cited, "unsupported": bad}


def tool_trace(messages: list) -> list[str]:
    """Every tool call and its result, in order: what the harness saw happen."""
    lines = []
    for message in messages:
        if isinstance(message, AIMessage):
            lines += [f"call {c['name']}({c['args']})" for c in message.tool_calls]
        elif isinstance(message, ToolMessage):
            lines.append(f"result {message.text}")
    return lines


def token_use(messages: list) -> dict:
    usage = [m.usage_metadata for m in messages if isinstance(m, AIMessage) and m.usage_metadata]
    return {"model_calls": len(usage),
            "input_tokens": sum(u.get("input_tokens", 0) for u in usage),
            "output_tokens": sum(u.get("output_tokens", 0) for u in usage)}


async def ask(agent, question: str) -> dict:
    """Run one question. Returns answer, tool trace, citation check, tokens and seconds."""
    start = time.perf_counter()
    result = await agent.ainvoke({"messages": [HumanMessage(question)]})
    messages = result["messages"]
    check = check_citations(messages[-1].text, messages)
    retried = False
    first_unsupported = check["unsupported"]
    if check["unsupported"]:  # one chance to repair, then flag
        retried = True
        fix = HumanMessage(
            "Citation check failed. These citations did not appear in any search result: "
            + "; ".join(check["unsupported"])
            + ". Rewrite your answer citing only [source, location] copied from search results "
              "(search again if you need to), or drop the claims you cannot support.")
        result = await agent.ainvoke({"messages": messages + [fix]})
        messages = result["messages"]
        check = check_citations(messages[-1].text, messages)
    answer = messages[-1].text
    if check["unsupported"]:
        answer += "\n\nWARNING: these citations could not be verified: " + "; ".join(check["unsupported"])
    return {
        "answer": answer,
        "trace": tool_trace(messages),
        "citations": check["cited"],
        "unsupported_citations": check["unsupported"],
        "citation_retry": retried,
        "first_unsupported": first_unsupported,  # what the guardrail caught before the retry
        "seconds": round(time.perf_counter() - start, 1),
        **token_use(messages),
    }


async def main(question: str) -> None:
    async with AsyncExitStack() as stack:
        agent = build_agent(await load_mcp_tools(stack))
        out = await ask(agent, question)
    for line in out["trace"]:
        print("  " + line.splitlines()[0][:160])  # first line of each step: the call, or the top hit
    status = "all verified" if not out["unsupported_citations"] else "UNVERIFIED citations"
    print(f"  citations: {len(out['citations'])}, {status}"
          f"{' (after one retry)' if out['citation_retry'] else ''}"
          f" | {out['model_calls']} model calls, {out['input_tokens']}+{out['output_tokens']} tokens,"
          f" {out['seconds']} s\n")
    print(out["answer"])


if __name__ == "__main__":
    asyncio.run(main(" ".join(sys.argv[1:]) or "How much compensation for a cancelled 1,200 km flight?"))
