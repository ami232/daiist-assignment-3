"""
Assignment 3: the agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the tools of server.py over MCP and
AGENTS.md as system prompt.

Guardrails:
  - Human approval before add_document runs (HumanInTheLoopMiddleware). When
    there is no terminal to ask (evaluation, CI) the call is rejected.
  - Call limits: at most MAX_MODEL_CALLS model calls and MAX_TOOL_CALLS tool
    calls per question.
  - Citation check (own guardrail): every [citation] in the answer must match
    a passage the search tool returned in this run, and a non-refusal answer
    must cite at least once. On failure the agent gets one retry with the
    problem spelled out; if it fails again, the answer is replaced by a refusal.

run(question) returns the answer and the trace, for evaluate.py.
"""

from __future__ import annotations

import asyncio
import os
import re
import sys
import time
import uuid
from pathlib import Path

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
MODEL = "gemini-3.1-flash-lite"
FALLBACK_MODELS = ("gemini-flash-lite-latest", "gemini-3.5-flash-lite")
MAX_MODEL_CALLS = 8
MAX_TOOL_CALLS = 5
REFUSAL = "El corpus no cubre esta pregunta."

CITATION_RE = re.compile(r"\[([^\[\]]+?,\s*(?:Art[íi]culo|Disposici[óo]n|P[áa]gina|Texto|Anexo)[^\[\]]*)\]")
CITE_AS_RE = re.compile(r"CITE AS: \[([^\]]+)\]")


def system_prompt() -> str:
    return (ROOT / "AGENTS.md").read_text(encoding="utf-8")


def _text(content) -> str:
    """Message content may be a string or a list of content blocks."""
    if isinstance(content, str):
        return content
    return "\n".join(b.get("text", "") if isinstance(b, dict) else str(b) for b in content or [])


def _norm_cite(c: str) -> str:
    return re.sub(r"\s+", " ", c.strip().lower())


def check_citations(answer: str, retrieved: set[str]) -> tuple[bool, str]:
    """(ok, problem). Citations must be among the retrieved CITE AS strings.

    A citation of a whole article ("…, Artículo 49") is accepted when a part of
    it ("…, Artículo 49, apdo. 1") was retrieved.
    """
    if answer.strip().startswith(REFUSAL):
        cites = CITATION_RE.findall(answer)
    else:
        cites = CITATION_RE.findall(answer)
        if not cites:
            return False, "the answer makes claims without any [citation]"
    norm = {_norm_cite(r) for r in retrieved}
    bad = [c for c in cites
           if _norm_cite(c) not in norm and not any(r.startswith(_norm_cite(c) + ",") or
                                                    r.startswith(_norm_cite(c) + " (") for r in norm)]
    if bad:
        return False, "these citations were not returned by search: " + "; ".join(bad)
    return True, ""


def ask_human(requests: list[dict], interactive: bool) -> list[dict]:
    decisions = []
    for req in requests:
        if not interactive:
            decisions.append({"type": "reject", "message": "No human available to approve add_document."})
            continue
        print(f"\nThe agent wants to run {req['name']} with {req['args']}.", file=sys.stderr)
        answer = input("Approve? [y/N] ").strip().lower()
        decisions.append({"type": "approve"} if answer in {"y", "yes", "s", "si", "sí"}
                         else {"type": "reject", "message": "The user did not approve adding this document."})
    return decisions


async def mcp_tools(session) -> list:
    """Wrap every tool the MCP server lists as a LangChain tool (one shared session)."""
    from langchain_core.tools import StructuredTool

    def make(tool):
        async def call(**kwargs) -> str:
            result = await session.call_tool(tool.name, kwargs)
            text = "\n".join(getattr(c, "text", "") for c in result.content)
            return f"Error: {text}" if (getattr(result, "is_error", False) or getattr(result, "isError", False)) else text
        return StructuredTool.from_function(coroutine=call, name=tool.name,
                                            description=tool.description or "",
                                            args_schema=tool.input_schema)
    return [make(t) for t in (await session.list_tools()).tools]


def build_model(name: str):
    from langchain_google_genai import ChatGoogleGenerativeAI
    return ChatGoogleGenerativeAI(model=name, temperature=0, max_retries=2)


async def _run(question: str, interactive: bool) -> dict:
    from langchain.agents import create_agent
    from langchain.agents.middleware import (HumanInTheLoopMiddleware, ModelCallLimitMiddleware,
                                             ModelFallbackMiddleware, ModelRetryMiddleware,
                                             ToolCallLimitMiddleware)
    from langgraph.checkpoint.memory import InMemorySaver
    from langgraph.types import Command
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    load_api_key()
    params = StdioServerParameters(command=sys.executable, args=[str(ROOT / "server.py")], cwd=str(ROOT),
                                    env=dict(os.environ))
    started = time.time()
    async with stdio_client(params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()
        tools = await mcp_tools(session)
        agent = create_agent(
            build_model(MODEL), tools=tools, system_prompt=system_prompt(),
            middleware=[
                HumanInTheLoopMiddleware(interrupt_on={"add_document": {"allowed_decisions": ["approve", "reject"]}}),
                ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS, exit_behavior="end"),
                ToolCallLimitMiddleware(run_limit=MAX_TOOL_CALLS, exit_behavior="continue"),
                ModelRetryMiddleware(max_retries=3, initial_delay=5),
                ModelFallbackMiddleware(*(build_model(m) for m in FALLBACK_MODELS)),
            ],
            checkpointer=InMemorySaver(),
        )
        config = {"configurable": {"thread_id": str(uuid.uuid4())}}
        payload = {"messages": [{"role": "user", "content": question}]}
        guardrail = None
        for attempt in range(2):
            while True:
                result = await agent.ainvoke(payload, config)
                interrupts = result.get("__interrupt__")
                if not interrupts:
                    break
                requests = interrupts[0].value["action_requests"]
                payload = Command(resume={"decisions": ask_human(requests, interactive)})
            messages = result["messages"]
            retrieved = {c for m in messages if m.type == "tool"
                         for c in CITE_AS_RE.findall(_text(m.content))}
            answer = _text(messages[-1].content).strip()
            ok, problem = check_citations(answer, retrieved)
            if ok:
                break
            guardrail = {"attempt": attempt + 1, "problem": problem, "rejected_answer": answer}
            print(f"[guardrail] citation check failed: {problem}", file=sys.stderr)
            if attempt == 0:
                payload = {"messages": [{"role": "user", "content":
                           f"Your answer failed the citation check: {problem}. Rewrite it following the "
                           f"rules: cite only the CITE AS text of passages search returned, search again "
                           f"if needed, or reply '{REFUSAL}' if the results do not support an answer."}]}
            else:
                answer = (f"{REFUSAL} (La respuesta generada no superó la comprobación de citas, "
                          f"así que no se muestra.)")

    trace, tokens = [], {"input": 0, "output": 0}
    for m in messages:
        if m.type == "ai":
            for tc in getattr(m, "tool_calls", []) or []:
                trace.append({"tool": tc["name"], "args": tc["args"]})
            usage = getattr(m, "usage_metadata", None) or {}
            tokens["input"] += usage.get("input_tokens", 0)
            tokens["output"] += usage.get("output_tokens", 0)
        elif m.type == "tool":
            trace.append({"tool_result": m.name, "cited": CITE_AS_RE.findall(_text(m.content)),
                          "text": _text(m.content)})
    return {"question": question, "answer": answer, "trace": trace, "retrieved": sorted(retrieved),
            "guardrail": guardrail, "tokens": tokens, "seconds": round(time.time() - started, 1)}


def run(question: str, interactive: bool = False) -> dict:
    """Answer one question. Returns answer, tool trace, tokens and seconds."""
    return asyncio.run(_run(question, interactive))


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit('usage: python agent.py "question"')
    out = run(" ".join(sys.argv[1:]), interactive=sys.stdin.isatty())
    print(out["answer"])
    if out["retrieved"]:
        print("\nFuentes consultadas:")
        for c in out["retrieved"]:
            print(f"  - {c}")
    print(f"\n({out['tokens']['input']} input + {out['tokens']['output']} output tokens, "
          f"{out['seconds']} s)", file=sys.stderr)


if __name__ == "__main__":
    main()
