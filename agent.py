"""
Assignment 3: your agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with tools from server.py over MCP and
AGENTS.md as system prompt. Ask for approval before add_document runs; add a
call limit and one guardrail of your choice. Print the answer with citations.

Guardrails: (1) approval by the user before add_document runs, (2) a limit of
MAX_TOOL_CALLS tool calls per question, (3) add_document may only read files
inside this project folder.

For evaluate.py: `ask_many(questions)` / `ask(question)` return, per question,
the answer, the tool trace (with the full text returned by the tools), tokens
and seconds.
"""

import asyncio
import os
import sys
import time
from pathlib import Path

from langchain.agents import create_agent
from langchain_core.tools import StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parent
# Free tier: about 20 requests per day per model. When a model runs out of its
# daily quota (or is not available to this key) the next one in the list is used.
AGENT_MODELS = [
    "gemini-3.5-flash",
    "gemini-3.5-flash-lite",
    "gemini-3.1-flash-lite",
    "gemini-2.5-flash-lite",
    "gemini-flash-lite-latest",
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-2.5-flash",
]
MODEL = AGENT_MODELS[0]  # kept for scripts that report "the" model
MAX_TOOL_CALLS = 6
RETRY_DELAYS = (10, 20, 30)  # seconds (max 30), for 503 / 429 from the model API
MODEL_TIMEOUT = 90  # seconds per model call; the client's own retries are off (max_retries=1)
TRANSIENT = ("503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED", "overloaded", "high demand",
             "timeout", "Timeout", "DEADLINE_EXCEEDED")
APPROVAL_TOOLS = {"add_document"}
DAILY_QUOTA = ("PerDay", "per day", "limit: 0", "NOT_FOUND")
_unusable: set[str] = set()  # models out of daily quota in this process


def model_unusable(error: str) -> bool:
    """True if the error means this model cannot be used again today (daily quota
    exhausted, no free quota at all, or model not found). Per-minute 429s are not."""
    return any(t in error for t in DAILY_QUOTA)


def next_model(models: list[str], unusable: set[str]) -> str | None:
    return next((m for m in models if m not in unusable), None)


def _api_key() -> str:
    from api_key import resolve_api_key

    key, _ = resolve_api_key()
    if not key:
        raise SystemExit("No Gemini API key found (see SETUP.md).")
    return key


def ask_user_approval(tool_name: str, args: dict) -> bool:
    """Default approval: ask on the terminal; deny when nobody can answer."""
    if not sys.stdin.isatty():
        print(f"[denied] {tool_name}({args}): no terminal to ask for approval", file=sys.stderr)
        return False
    reply = input(f"\nThe agent wants to run {tool_name}({args}). Allow? [y/N] ")
    return reply.strip().lower() in ("y", "yes", "s", "si", "sí")


def _text(content) -> str:
    """Gemini may return a string or a list of content blocks."""
    if isinstance(content, str):
        return content
    parts = []
    for block in content or []:
        parts.append(block if isinstance(block, str) else block.get("text", ""))
    return "".join(parts)


def _inside_project(path_str: str) -> bool:
    try:
        p = Path(path_str).expanduser().resolve()
        return p == ROOT or ROOT in p.parents
    except Exception:
        return False


def _wrap_tools(mcp_tools, session, trace: list, approve) -> list:
    """Wrap the MCP tools so every call is traced, limited and guarded."""
    calls = {"n": 0}
    wrapped = []
    for t in mcp_tools:
        name = t.name

        async def run(_name=name, **kwargs) -> str:
            entry = {"tool": _name, "args": kwargs, "result": None, "blocked": None}
            trace.append(entry)
            if calls["n"] >= MAX_TOOL_CALLS:
                entry["blocked"] = "call limit"
                entry["result"] = ("Tool call limit reached. Answer now with what you already have, "
                                   "or say the corpus does not cover the question.")
                return entry["result"]
            calls["n"] += 1
            if _name == "add_document" and not _inside_project(str(kwargs.get("path", ""))):
                entry["blocked"] = "path outside project"
                entry["result"] = "Blocked: add_document may only read files inside the project folder."
                return entry["result"]
            if _name in APPROVAL_TOOLS and not approve(_name, kwargs):
                entry["blocked"] = "not approved"
                entry["result"] = "The user did not approve this action. Do not retry it."
                return entry["result"]
            res = await session.call_tool(_name, kwargs)
            entry["result"] = "".join(getattr(c, "text", "") for c in res.content)
            return entry["result"]

        wrapped.append(StructuredTool.from_function(
            coroutine=run, name=name, description=t.description or name, args_schema=getattr(t, "input_schema", None) or t.inputSchema))
    return wrapped


async def ask_many(questions: list[str], approve=ask_user_approval) -> list[dict]:
    """Answer several questions with one server process. Returns one dict each."""
    system_prompt = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    key = _api_key()
    params = StdioServerParameters(command=sys.executable, args=[str(ROOT / "server.py")],
                                   cwd=str(ROOT), env=dict(os.environ))
    results = []
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            mcp_tools = (await session.list_tools()).tools
            for question in questions:
                start = time.time()
                answer, error, tokens, trace = "", None, {"input": 0, "output": 0}, []
                used, tried = None, []
                while (name := next_model(AGENT_MODELS, _unusable)) is not None:
                    used = name
                    tried.append(name)
                    model = ChatGoogleGenerativeAI(model=name, api_key=key, temperature=0,
                                                   timeout=MODEL_TIMEOUT, max_retries=1)
                    switch = False
                    for attempt in range(len(RETRY_DELAYS) + 1):
                        trace = []  # a retry starts from a clean trace and a fresh call counter
                        agent = create_agent(model, _wrap_tools(mcp_tools, session, trace, approve),
                                             system_prompt=system_prompt)
                        try:
                            out = await agent.ainvoke({"messages": [("user", question)]},
                                                      config={"recursion_limit": 25})
                            msgs = out["messages"]
                            answer = _text(msgs[-1].content).strip()
                            usage = [getattr(m, "usage_metadata", None) or {} for m in msgs]
                            tokens = {"input": sum(u.get("input_tokens", 0) for u in usage),
                                      "output": sum(u.get("output_tokens", 0) for u in usage)}
                            error = None
                            break
                        except Exception as e:  # keep going: one failure must not stop an evaluation
                            error = f"{type(e).__name__}: {e}"
                            if model_unusable(error):
                                _unusable.add(name)
                                print(f"{name}: daily quota exhausted or unavailable, switching model",
                                      file=sys.stderr)
                                switch = True
                                break
                            if attempt < len(RETRY_DELAYS) and any(t in error for t in TRANSIENT):
                                print(f"{name} busy, retrying in {RETRY_DELAYS[attempt]}s", file=sys.stderr)
                                await asyncio.sleep(RETRY_DELAYS[attempt])
                                continue
                            break
                    if not switch:
                        break
                if used is None:
                    error = "all models in AGENT_MODELS are out of daily quota"
                results.append({"question": question, "answer": answer, "trace": trace,
                                "tokens": tokens, "seconds": round(time.time() - start, 1),
                                "model": used, "models_tried": tried, "error": error})
    return results


def ask(question: str, approve=ask_user_approval) -> dict:
    return asyncio.run(ask_many([question], approve))[0]


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit('usage: python agent.py "your question"')
    r = ask(" ".join(sys.argv[1:]))
    if r["error"]:
        raise SystemExit(f"Agent failed: {r['error']}")
    print(r["answer"])
    searched = [e["args"].get("query") for e in r["trace"] if e["tool"] == "search"]
    print(f"\n[{r['model']}; {len(r['trace'])} tool call(s); searches: {searched}; "
          f"{r['tokens']['input']}+{r['tokens']['output']} tokens; {r['seconds']} s]")


if __name__ == "__main__":
    main()