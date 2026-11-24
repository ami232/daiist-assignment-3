"""
Drone-rules agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain create_agent on Gemini, tools from server.py over MCP, AGENTS.md as
system prompt. Guardrails:
  - approval before add_document runs (denied when nobody can answer);
  - call limits on the model and on search;
  - citation check: every [source, location] must match a passage that search
    actually returned in this run. One retry with feedback, then a refusal.

run(question) returns the answer, citations, tool trace, tokens and seconds,
which is what evaluate.py uses.
"""

import asyncio
import os
import re
import sys
import time
from pathlib import Path

from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware, ToolCallLimitMiddleware, wrap_tool_call
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.tools import StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

import index
from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
MODEL = os.environ.get("GEMINI_MODEL", "gemini-3.1-flash-lite")  # 2.5-flash free tier is only 20 requests/day
REFUSAL = "The corpus does not cover this."
REFUSED_PREFIX = "The corpus does not cover"  # also catches "...does not cover the specific fines"
BRACKET = re.compile(r"\[([^\[\]]+)\]")
PASSAGE_HEADER = re.compile(  # what search returns: v1 "[1] source, location (score s)",
    r"^(?:\[\d+\] (.+?), (.+?) \(score [\d.\-]+\)$"  # v2 "Passage 1 (score s). Cite as: [source, location]."
    r"|Passage \d+ \(score [\d.\-]+\)\. Cite as: \[(.+?), (.+?)\]\.)", re.MULTILINE)


def citations_in(answer: str) -> list[tuple[str, str]]:
    """Every [source, location] in the answer; one bracket may hold several, separated by ';'."""
    out = []
    for inside in BRACKET.findall(answer):
        for part in inside.split(";"):
            if ", " in part:
                source, location = part.split(", ", 1)
                out.append((source.strip(), location.strip()))
    return out


def passages_in(text: str) -> list[tuple[str, str]]:
    """(source, location) of every passage in a search result, in either output format."""
    return [(m[0] or m[2], m[1] or m[3]) for m in PASSAGE_HEADER.findall(text)]


def ask_user(name: str, args: dict) -> bool:
    """Ask in the terminal; with no terminal (evaluation, check.py) the answer is no."""
    if not sys.stdin.isatty():
        return False
    reply = input(f"\nThe agent wants to run {name}({args}). Allow? [y/N] ")
    return reply.strip().lower() in {"y", "yes"}


def mcp_tools(session: ClientSession, listed) -> list[StructuredTool]:
    """Wrap the server's MCP tools as LangChain tools."""
    def make(tool):
        async def call(**kwargs):
            result = await session.call_tool(tool.name, kwargs)
            return "\n".join(getattr(c, "text", "") for c in result.content)
        return StructuredTool.from_function(coroutine=call, name=tool.name,
                                            description=tool.description, args_schema=tool.input_schema)
    return [make(t) for t in listed.tools]


def check_citations(answer: str, passages: list[tuple[str, str]]) -> list[str]:
    """Problems with the answer's citations; empty list means it passes."""
    if answer.strip().startswith(REFUSED_PREFIX):
        return []
    cited = citations_in(answer)
    if not cited:
        return ["the answer has no [source, location] citations"]
    bad = [f"[{s}, {l}]" for s, l in cited
           if not any(s.strip() == ps and index.loc_match(l, pl) for ps, pl in passages)]
    return [f"{c} does not match any passage search returned" for c in bad]


def text_of(msg) -> str:
    c = msg.content
    if isinstance(c, list):  # Gemini can return content blocks
        c = "".join(b.get("text", "") if isinstance(b, dict) else str(b) for b in c)
    return c.strip()


async def run(question: str, approve=ask_user) -> dict:
    started = time.time()
    params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT))
    async with stdio_client(params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()
        tools = mcp_tools(session, await session.list_tools())

        @wrap_tool_call
        async def approval(request, handler):
            call = request.tool_call
            if call["name"] == "add_document" and not approve(call["name"], call["args"]):
                return ToolMessage(content="The user did not approve adding this document.", tool_call_id=call["id"])
            return await handler(request)

        agent = create_agent(
            ChatGoogleGenerativeAI(model=MODEL, api_key=load_api_key(), temperature=0),
            tools,
            system_prompt=(ROOT / "AGENTS.md").read_text(encoding="utf-8"),
            middleware=[
                approval,
                ModelCallLimitMiddleware(run_limit=6, exit_behavior="end"),
                ToolCallLimitMiddleware(tool_name="search", run_limit=3, exit_behavior="continue"),
            ],
        )

        messages = [HumanMessage(question)]
        guardrail = "passed"
        for attempt in range(2):
            messages = (await agent.ainvoke({"messages": messages}))["messages"]
            passages = [p for t in messages if isinstance(t, ToolMessage) for p in passages_in(text_of(t))]
            answer = text_of(messages[-1]) if isinstance(messages[-1], AIMessage) else ""
            problems = check_citations(answer, passages)
            if not problems:
                break
            if attempt == 0:
                guardrail = "retried: " + "; ".join(problems)
                messages.append(HumanMessage(
                    "Your answer failed the citation check: " + "; ".join(problems)
                    + ". Rewrite it citing only passages returned by search, copying source and location exactly,"
                    f" or reply '{REFUSAL}'"))
            else:
                guardrail = "blocked: " + "; ".join(problems)
                answer = f"{REFUSAL} (The draft answer was withheld because its citations could not be verified.)"

    usage = [m.usage_metadata for m in messages if isinstance(m, AIMessage) and m.usage_metadata]
    return {
        "question": question,
        "answer": answer,
        "citations": citations_in(answer),
        "passages": passages,
        "retrieved_text": "\n\n".join(text_of(m) for m in messages if isinstance(m, ToolMessage)),
        "tool_calls": [(c["name"], c["args"]) for m in messages if isinstance(m, AIMessage) for c in m.tool_calls],
        "searches_blocked": sum(text_of(m).startswith("Tool call limit exceeded")
                                for m in messages if isinstance(m, ToolMessage)),
        "guardrail": guardrail,
        "input_tokens": sum(u.get("input_tokens", 0) for u in usage),
        "output_tokens": sum(u.get("output_tokens", 0) for u in usage),
        "seconds": round(time.time() - started, 1),
    }


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit('usage: python agent.py "your question"')
    r = asyncio.run(run(" ".join(sys.argv[1:])))
    print(r["answer"])
    if r["passages"]:
        print("\nRetrieved:")
        for s, l in dict.fromkeys(r["passages"]):
            print(f"  - {s}, {l}")
    print(f"\n[{r['input_tokens']}+{r['output_tokens']} tokens, {r['seconds']}s, citation check: {r['guardrail']}]")
