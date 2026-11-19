"""
Assignment 3: the agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini. The tools come from server.py over MCP (stdio),
and AGENTS.md is the system prompt.

Guardrails:
  1. Approval: add_document only runs after a person types "y" in the terminal.
     With no terminal (evaluation, check.py) it is refused automatically.
  2. Call limits: at most 6 model calls and 4 tool calls per question.
     (Plus reliability: each model call is retried on errors such as 503 "overloaded",
     and if the main model keeps failing a fallback Gemini model is used.)
  3. Citation check (our extra guardrail): after the model answers, code checks that
     every cited id was really returned by the search tool in this run. If the answer
     cites an id that was never retrieved, or states facts with no citation at all,
     it is blocked and replaced by the refusal message.

`run(question)` returns the answer, citations, tool trace, tokens and seconds, for evaluate.py.
"""

import asyncio
import re
import sys
import time
from pathlib import Path

from langchain.agents import create_agent
from langchain.agents.middleware import (ModelCallLimitMiddleware, ModelFallbackMiddleware,
                                         ModelRetryMiddleware, ToolCallLimitMiddleware)
from langchain_core.tools import StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
CHAT_MODEL = "gemini-3.1-flash-lite"
# Used only if the main model stays overloaded (503) after the retries.
FALLBACK_MODELS = ["gemini-3.5-flash-lite", "gemini-3.8-flash"]
SYSTEM_PROMPT = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
REFUSAL = "The corpus does not cover this."
CITATION_ID = re.compile(r"[a-z0-9_]+:[a-z0-9_]+(?::[0-9]+)?")
CHUNK_ID = re.compile(r"^\[([a-z0-9_]+:[a-z0-9_]+(?::[0-9]+)?)\]", re.M)


def ask_approval(path: str) -> bool:
    """Human approval before add_document. No terminal means no approval."""
    if not sys.stdin.isatty():
        print(f"[approval] add_document({path!r}) refused: no one at the terminal to approve it.", file=sys.stderr)
        return False
    answer = input(f"\nThe agent wants to ADD a document to the index:\n  {path}\nApprove? [y/N] ")
    return answer.strip().lower() in {"y", "yes"}


def text_of(message) -> str:
    content = message.content
    if isinstance(content, str):
        return content
    return "".join(part.get("text", "") if isinstance(part, dict) else str(part) for part in content)


def find_citations(text: str) -> list[str]:
    """Citation ids in square brackets: [id] or several in one bracket, [id1, id2]."""
    ids = []
    for group in re.findall(r"\[([^\[\]]+)\]", text):
        for part in re.split(r"[,;]", group):
            part = part.strip()
            if CITATION_ID.fullmatch(part):
                ids.append(part)
    return ids


def check_citations(answer: str, retrieved: set[str]) -> tuple[str, str | None]:
    """Our extra guardrail. Returns (final answer, reason it fired or None)."""
    cited = find_citations(answer)
    invalid = [c for c in cited if c not in retrieved]
    if answer.strip().startswith(REFUSAL):
        return answer, None
    if invalid:
        return (f"{REFUSAL} (An answer was drafted but blocked: it cited passages that were not retrieved: "
                f"{', '.join(invalid)}.)"), f"invalid citation {invalid}"
    if not cited:
        return (f"{REFUSAL} (An answer was drafted but blocked because it had no citations.)"), "no citations"
    return answer, None


async def run(question: str, approve=ask_approval, model: str = CHAT_MODEL) -> dict:
    load_api_key()
    started = time.time()
    trace: list[dict] = []
    params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT))

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            mcp_tools = (await session.list_tools()).tools

            def make_tool(spec):
                async def call(**kwargs):
                    if spec.name == "add_document" and not approve(kwargs.get("path", "")):
                        result = "Not added: the user did not approve adding this document."
                    else:
                        out = await session.call_tool(spec.name, kwargs)
                        result = "\n".join(getattr(c, "text", "") for c in out.content)
                    trace.append({"tool": spec.name, "args": kwargs, "result": result})
                    return result
                return StructuredTool.from_function(coroutine=call, name=spec.name,
                                                    description=spec.description, args_schema=spec.input_schema)

            tools = [make_tool(t) for t in mcp_tools]
            def llm(name):
                return ChatGoogleGenerativeAI(model=name, temperature=0, api_key=load_api_key())
            agent = create_agent(
                llm(model), tools, system_prompt=SYSTEM_PROMPT,
                middleware=[ModelCallLimitMiddleware(run_limit=6, exit_behavior="end"),
                            ToolCallLimitMiddleware(run_limit=4),
                            ModelFallbackMiddleware(*[llm(m) for m in FALLBACK_MODELS]),
                            ModelRetryMiddleware(max_retries=3, initial_delay=5, on_failure="error")],
            )
            state = await agent.ainvoke({"messages": [{"role": "user", "content": question}]})

    messages = state["messages"]
    final = next((text_of(m) for m in reversed(messages) if m.type == "ai" and text_of(m).strip()), "")
    tokens_in = sum((getattr(m, "usage_metadata", None) or {}).get("input_tokens", 0) for m in messages if m.type == "ai")
    tokens_out = sum((getattr(m, "usage_metadata", None) or {}).get("output_tokens", 0) for m in messages if m.type == "ai")

    models_used = sorted({(m.response_metadata or {}).get("model_name", "") for m in messages if m.type == "ai"} - {""})
    retrieved = {cid for step in trace if step["tool"] == "search" for cid in CHUNK_ID.findall(step["result"])}
    if not final.strip():
        final = f"{REFUSAL} (No answer was produced within the call limits.)"
    only_added = any(s["tool"] == "add_document" for s in trace) and not retrieved
    if only_added:          # a reply to "add this file" states no facts from the labels
        answer, fired = final, None
    else:
        answer, fired = check_citations(final, retrieved)
    return {
        "question": question,
        "answer": answer,
        "draft": final,
        "guardrail": fired,
        "citations": sorted(set(find_citations(answer))),
        "retrieved": sorted(retrieved),
        "trace": trace,
        "models": models_used,
        "tokens_in": tokens_in,
        "tokens_out": tokens_out,
        "seconds": round(time.time() - started, 2),
    }


def print_result(result: dict) -> None:
    print(result["answer"])
    if result["citations"]:
        print("\nSources:")
        texts = {}
        for step in result["trace"]:
            for block in step["result"].split("\n\n---\n\n"):
                m = CHUNK_ID.match(block)
                if m:
                    texts[m.group(1)] = block.split("\n", 1)[0]
        for cid in result["citations"]:
            print(f"  {texts.get(cid, '[' + cid + ']')}")
    if result["guardrail"]:
        print(f"\n[guardrail fired: {result['guardrail']}]", file=sys.stderr)
    print(f"\n({result['tokens_in'] + result['tokens_out']} tokens, {result['seconds']} s)")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit('usage: python agent.py "your question"')
    print_result(asyncio.run(run(" ".join(sys.argv[1:]))))
