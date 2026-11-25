"""
Assignment 3: the agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, tools from server.py over MCP, AGENTS.md as the
system prompt. Harness controls (all in code, not in the prompt):
  - approval: add_document only runs after the user types y (denied when there is
    no terminal, unless AGENT_AUTO_APPROVE=1 is set);
  - call limit: at most MAX_TOOL_CALLS tool calls and a recursion limit per question;
  - guardrail (citations): every section the answer cites must appear in the
    passages the search tool returned; otherwise the answer is flagged and, if it
    cites nothing valid, replaced by a refusal. An answer given without any
    search is also replaced.

`ask(question)` returns {answer, raw_answer, trace, guardrail, tokens, seconds}
for evaluate.py.
"""

import asyncio
import json
import os
import re
import sys
import time
from pathlib import Path

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
MODEL = os.environ.get("AGENT_MODEL", "gemini-3.5-flash")
MAX_TOOL_CALLS = 6
RECURSION_LIMIT = 20
REFUSAL = "The corpus does not cover this."

SECTION = re.compile(r"§\s*(\d{1,3}\.\d+[a-z]?)")


def _text(content) -> str:
    if isinstance(content, str):
        return content
    return "".join(b.get("text", "") if isinstance(b, dict) else str(b) for b in content)


def default_approval(tool: str, args: dict) -> bool:
    if os.environ.get("AGENT_AUTO_APPROVE") == "1":
        return True
    if not sys.stdin.isatty():
        return False
    print(f"\nThe agent wants to run {tool} with {json.dumps(args)}", file=sys.stderr)
    return input("Approve? [y/N] ").strip().lower() == "y"


def check_citations(answer: str, trace: list[dict]) -> tuple[str, dict]:
    """Guardrail: cited sections must come from retrieved passages."""
    retrieved = "\n".join(t["result"] for t in trace if t["tool"] == "search")
    retrieved_sections = set(SECTION.findall(retrieved))
    cited = set(SECTION.findall(answer))
    info = {"cited": sorted(cited), "invalid": sorted(cited - retrieved_sections), "fired": False, "reason": ""}
    refused = answer.strip().lower().startswith(REFUSAL.lower()[:30])
    if not any(t["tool"] == "search" for t in trace) and not refused:
        info.update(fired=True, reason="answer given without searching")
        return f"{REFUSAL} (The assistant did not consult the corpus, so the answer was withheld.)", info
    if info["invalid"]:
        info.update(fired=True, reason=f"cites sections not in the retrieved passages: {info['invalid']}")
        if not (cited & retrieved_sections):
            return f"{REFUSAL} (The draft answer cited sections that were not retrieved, so it was withheld.)", info
        answer += f"\n\nWARNING: unverified citation(s) {info['invalid']} were not in the retrieved passages."
    return answer, info


async def _ask(question: str, approve=default_approval) -> dict:
    from langchain.agents import create_agent
    from langchain_core.tools import StructuredTool
    from langchain_google_genai import ChatGoogleGenerativeAI
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    load_api_key()
    started = time.time()
    trace: list[dict] = []
    params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT))
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            mcp_tools = (await session.list_tools()).tools

            def wrap(tool):
                async def call(**kwargs) -> str:
                    if len(trace) >= MAX_TOOL_CALLS:
                        return "Tool call limit reached. Answer now from what you have, or say the corpus does not cover it."
                    if tool.name == "add_document" and not approve(tool.name, kwargs):
                        trace.append({"tool": tool.name, "args": kwargs, "result": "DENIED by user"})
                        return "The user did not approve this call. Do not retry it."
                    res = await session.call_tool(tool.name, kwargs)
                    text = "\n".join(getattr(c, "text", "") for c in res.content)
                    trace.append({"tool": tool.name, "args": kwargs, "result": text})
                    return text

                return StructuredTool.from_function(
                    coroutine=call, name=tool.name, description=tool.description or "", args_schema=tool.input_schema
                )

            agent = create_agent(
                model=ChatGoogleGenerativeAI(model=MODEL, temperature=0),
                tools=[wrap(t) for t in mcp_tools],
                system_prompt=(ROOT / "AGENTS.md").read_text(encoding="utf-8"),
            )
            result = await agent.ainvoke(
                {"messages": [{"role": "user", "content": question}]},
                config={"recursion_limit": RECURSION_LIMIT},
            )

    messages = result["messages"]
    raw = _text(messages[-1].content).strip()
    tokens = {"input": 0, "output": 0}
    for m in messages:
        usage = getattr(m, "usage_metadata", None) or {}
        tokens["input"] += usage.get("input_tokens", 0)
        tokens["output"] += usage.get("output_tokens", 0)
    answer, guard = check_citations(raw, trace)
    return {
        "question": question,
        "answer": answer,
        "raw_answer": raw,
        "trace": trace,
        "guardrail": guard,
        "tokens": tokens,
        "seconds": round(time.time() - started, 1),
    }


def ask(question: str, approve=default_approval) -> dict:
    return asyncio.run(_ask(question, approve))


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit('usage: python agent.py "question"')
    out = ask(" ".join(sys.argv[1:]))
    print(out["answer"])
    cited = out["guardrail"]["cited"]
    if cited:
        print("\nCitations checked against retrieved passages:", ", ".join(f"§ {c}" for c in cited))
    if out["guardrail"]["fired"]:
        print(f"[guardrail fired: {out['guardrail']['reason']}]")
    print(
        f"\n[{len(out['trace'])} tool call(s), {out['tokens']['input']}+{out['tokens']['output']} tokens, {out['seconds']}s]",
        file=sys.stderr,
    )


if __name__ == "__main__":
    main()
