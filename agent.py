"""
Assignment 3: my agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the two tools from server.py over MCP
and AGENTS.md as the system prompt. Guardrails:
1. approval: add_document only runs after a person types "y" (refused when nobody can answer);
2. call limits: at most 4 tool calls and 6 model calls per question;
3. citation check: every citation in the answer must be one the search tool
   actually returned in this run. If not, the agent gets one chance to fix it,
   and otherwise the answer is replaced by a refusal.

answer(question) returns the answer, the tool trace, tokens and seconds, for evaluate.py.
"""

import asyncio
import os
import re
import sys
import time
from pathlib import Path

os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")

from langchain.agents import create_agent  # noqa: E402
from langchain.agents.middleware import (  # noqa: E402
    ModelCallLimitMiddleware,
    ModelFallbackMiddleware,
    ToolCallLimitMiddleware,
    wrap_tool_call,
)
from langchain_core.messages import AIMessage, ToolMessage  # noqa: E402
from langchain_core.tools import StructuredTool  # noqa: E402
from langchain_google_genai import ChatGoogleGenerativeAI  # noqa: E402
from mcp import ClientSession, StdioServerParameters  # noqa: E402
from mcp.client.stdio import stdio_client  # noqa: E402

from api_key import load_api_key  # noqa: E402

ROOT = Path(__file__).resolve().parent
MODEL = "gemini-3.5-flash-lite"   # the free tier allows only 20 requests a day on gemini-3.5-flash
FALLBACK_MODEL = "gemini-3.1-flash-lite"  # used when the main model is overloaded or out of quota
MAX_TOOL_CALLS = 4
MAX_MODEL_CALLS = 6
REFUSAL = "The corpus does not cover this"
CITATION = re.compile(r"^\S+, (?:section [^,]+, )?pp?\. [\d-]+$")  # "NWSI-10-513, section 6.3, p. 7"


def system_prompt() -> str:
    return (ROOT / "AGENTS.md").read_text(encoding="utf-8")


def ask_person(path: str) -> bool:
    """Approval step for add_document. With no person at the keyboard, the answer is no."""
    if not sys.stdin.isatty():
        return False
    reply = input(f"\nThe agent wants to add {path!r} to the index. Allow? [y/N] ")
    return reply.strip().lower() == "y"


@wrap_tool_call
async def approve_add_document(request, handler):
    call = request.tool_call
    if call["name"] == "add_document" and not ask_person(call["args"].get("path", "")):
        return ToolMessage(content="Not run: the user did not approve adding this document.",
                           tool_call_id=call["id"], name=call["name"])
    return await handler(request)


def mcp_tools(session: ClientSession, listed) -> list[StructuredTool]:
    """Wrap each MCP tool from server.py as a LangChain tool."""
    tools = []
    for tool in listed:
        async def call(_name=tool.name, **kwargs) -> str:
            result = await session.call_tool(_name, kwargs)
            return "\n".join(getattr(c, "text", "") for c in result.content)
        schema = getattr(tool, "input_schema", None) or getattr(tool, "inputSchema", None)
        tools.append(StructuredTool(name=tool.name, description=tool.description or "",
                                    args_schema=schema, coroutine=call))
    return tools


def final_text(messages) -> str:
    for message in reversed(messages):
        if isinstance(message, AIMessage) and message.text.strip():
            return message.text.strip()
    return ""


def is_refusal(answer: str) -> bool:
    """A refusal starts with "The corpus does not cover" (models sometimes go on with "the specific ...")."""
    return answer.strip().lower().startswith(REFUSAL.lower()[:-len(" this")])


def citations(answer: str) -> list[str]:
    """Every citation in square brackets; one bracket may hold several, separated by ';' or ','."""
    found = []
    for bracket in re.findall(r"\[([^\[\]]+)\]", answer):
        parts = re.split(r";\s*|(?<=p\. \d),\s*|(?<=p\. \d\d),\s*|(?<=p\. \d\d\d),\s*|(?<=\d-\d),\s*|(?<=\d-\d\d),\s*", bracket)
        found += [part.strip() for part in parts if CITATION.match(part.strip())]
    return found


def check_citations(answer: str, retrieved: set[str]) -> tuple[bool, list[str]]:
    """True when the answer is a refusal, or cites at least once and only cites retrieved passages."""
    cited = citations(answer)
    if is_refusal(answer) and not cited:
        return True, []
    bad = [c for c in cited if c not in retrieved]
    return bool(cited) and not bad, bad


def retrieved_citations(messages) -> set[str]:
    return {c for m in messages if isinstance(m, ToolMessage)
            for c in re.findall(r"^\[\d+\] \((.+)\)$", m.text, flags=re.M)}


async def answer_async(question: str) -> dict:
    started = time.time()
    load_api_key()
    params = StdioServerParameters(command=sys.executable, args=[str(ROOT / "server.py")], cwd=str(ROOT),
                                   env=dict(os.environ))  # pass the API key and network settings on
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = mcp_tools(session, (await session.list_tools()).tools)
            agent = create_agent(
                ChatGoogleGenerativeAI(model=MODEL, temperature=0, max_retries=4),
                tools,
                system_prompt=system_prompt(),
                middleware=[
                    approve_add_document,
                    ToolCallLimitMiddleware(run_limit=MAX_TOOL_CALLS),
                    ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS),
                    ModelFallbackMiddleware(ChatGoogleGenerativeAI(model=FALLBACK_MODEL, temperature=0, max_retries=4)),
                ],
            )
            result = await agent.ainvoke({"messages": [{"role": "user", "content": question}]})
            messages = result["messages"]
            answer = final_text(messages)

            ok, bad = check_citations(answer, retrieved_citations(messages))
            guardrail = None
            if not ok:
                guardrail = "citation check failed (" + ("no citation" if not bad else "not retrieved: " + "; ".join(bad)) + ")"
                retry = messages + [{"role": "user", "content": (
                    "Your answer breaks the citation rule. Cite only passages the search tool returned, "
                    "in square brackets, copied exactly from the citation line above each passage. "
                    f"If the passages do not answer the question, reply starting with '{REFUSAL}'.")}]
                messages = (await agent.ainvoke({"messages": retry}))["messages"]
                answer = final_text(messages)
                ok, _ = check_citations(answer, retrieved_citations(messages))
                if ok:
                    guardrail += "; fixed after one retry"
                else:
                    answer = f"{REFUSAL}: I could not give an answer supported by the retrieved passages."
                    guardrail += "; replaced by a refusal after one retry"

    usage = [m.usage_metadata or {} for m in messages if isinstance(m, AIMessage)]
    return {
        "question": question,
        "answer": answer,
        "trace": [{"tool": c["name"], "args": c["args"]} for m in messages if isinstance(m, AIMessage) for c in m.tool_calls],
        "retrieved_text": "\n\n".join(m.text for m in messages if isinstance(m, ToolMessage)),
        "guardrail": guardrail,
        "input_tokens": sum(u.get("input_tokens", 0) for u in usage),
        "output_tokens": sum(u.get("output_tokens", 0) for u in usage),
        "seconds": round(time.time() - started, 1),
    }


def answer(question: str) -> dict:
    return asyncio.run(answer_async(question))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit('usage: python agent.py "your question"')
    out = answer(" ".join(sys.argv[1:]))
    print(out["answer"])
    if out["guardrail"]:
        print(f"\n(guardrail: {out['guardrail']})")
    print(f"\n[{len(out['trace'])} tool call(s), {out['input_tokens']}+{out['output_tokens']} tokens, {out['seconds']}s]")
