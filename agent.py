"""
Assignment 3: your agent. `main.py ask "question"` runs `python agent.py "question"`.

A LangChain agent on Gemini. Its tools come from server.py over MCP, and AGENTS.md is
its system prompt. The harness around the model adds:

  * approval  : add_document only runs if a person says yes (default: no);
  * a limit   : at most MAX_TOOL_CALLS tool calls per question;
  * guardrail : a citation check. Every [id] in the answer must be a passage that
                `search` really returned, and an answer that is not a refusal must
                cite something. A bad answer gets ONE retry with feedback; if it is
                still bad it is replaced by a safe message instead of being shown.

`ask()` returns the answer together with the tool trace, for evaluate.py.
"""

import asyncio
import os
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.tools import StructuredTool
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from pydantic import Field, create_model

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
SERVER_SCRIPT = ROOT / "server.py"
# Chosen with try_models.py: fast and able to call tools with this key. The second is used only if
# the first is unavailable (Gemini answers 503/504 when a model is busy). CHAT_MODEL=name overrides both.
CHAT_MODELS = [os.environ["CHAT_MODEL"]] if os.environ.get("CHAT_MODEL") else [
    "gemini-3.5-flash-lite", "gemini-3.1-flash-lite"]
MODEL_TIMEOUT = 60        # seconds one model call may take; MODEL_RETRIES quick retries on top
MODEL_RETRIES = 1
UNAVAILABLE = ("503", "504", "429", "404", "UNAVAILABLE", "DEADLINE", "NOT_FOUND", "RESOURCE_EXHAUSTED", "Timeout")
MAX_TOOL_CALLS = 6        # per question, add_document included
RECURSION_LIMIT = 30      # backstop on the agent's own loop; MAX_TOOL_CALLS normally stops it first
REFUSAL = "No encuentro esto en los documentos"
BLOCKED_ANSWER = ("No puedo mostrar una respuesta verificada: la respuesta generada no pasó la "
                  "comprobación de citas. Prueba a reformular la pregunta o consulta los documentos.")
LIMIT_MESSAGE = (f"Tool call limit reached ({MAX_TOOL_CALLS} per question). Do not call any more tools: "
                 f"answer now with the passages you already have, or say the documents do not cover it.")

PASSAGE = re.compile(r"^\[\d+\] (?P<title>.+?) \| (?P<location>.+?) \| (?P<pages>pp?\. [\d-]+) \| id (?P<id>\S+)$",
                     re.MULTILINE)
CITED_ID = re.compile(r"[AB]-[A-Za-z0-9_]+(?:-[A-Za-z0-9_]+)*-\d{4}")


@dataclass
class AgentResult:
    question: str
    answer: str                     # what the user sees (after the guardrail)
    raw_answer: str                 # what the model wrote
    sources: list[dict]             # the cited passages: id, title, location, pages
    trace: list[dict]               # every tool call: tool, args, result, seconds, status
    guardrail: str                  # "ok", "fixed_on_retry", "blocked" or "error"
    model: str = ""                 # the model that wrote the answer
    problems: list[str] = field(default_factory=list)
    refused: bool = False
    tool_calls: int = 0
    seconds: float = 0.0
    input_tokens: int = 0
    output_tokens: int = 0
    error: str | None = None


# ---------------------------------------------------------------- approval

def ask_in_terminal(tool_name: str, args: dict) -> bool:
    """Ask a person. Anything but an explicit yes means no, and so does having nobody to ask."""
    if not sys.stdin.isatty():
        return False
    print(f"\nThe assistant wants to run {tool_name} with {args}.", file=sys.stderr)
    return input("Allow adding this file? [y/N] ").strip().lower() in ("y", "yes", "s", "si", "sí")


# ---------------------------------------------------------------- tools

class Run:
    """The state of one question: tool-call count, trace, and the passages search has returned."""

    def __init__(self, approve):
        self.approve = approve
        self.trace: list[dict] = []
        self.retrieved: dict[str, dict] = {}
        self.calls = 0
        self.searches = 0


def langchain_tool(session: ClientSession, tool, run: Run) -> StructuredTool:
    """Wrap one MCP tool as a LangChain tool, with the call limit, the approval and the trace."""
    properties = (tool.input_schema or {}).get("properties", {})
    schema = create_model(f"{tool.name}_input", **{
        name: (str, Field(description=spec.get("description", name))) for name in properties
        for spec in [properties[name]]})

    async def call(**arguments) -> str:
        started = time.time()
        run.calls += 1
        print(f"  [{tool.name}] {arguments}", file=sys.stderr, flush=True)
        status = "ok"
        if run.calls > MAX_TOOL_CALLS:
            text, status = LIMIT_MESSAGE, "limit_reached"
        elif tool.name == "add_document" and not run.approve(tool.name, arguments):
            text, status = "The user did not approve adding this file. It was NOT added.", "not_approved"
        else:
            result = await session.call_tool(tool.name, arguments)
            text = "\n".join(getattr(c, "text", "") for c in result.content).strip()
            if getattr(result, "is_error", False) or getattr(result, "isError", False):
                text, status = f"Tool error: {text}", "error"
            elif tool.name == "search":
                run.searches += 1
                for m in PASSAGE.finditer(text):
                    run.retrieved[m["id"]] = {"id": m["id"], "title": m["title"],
                                              "location": m["location"], "pages": m["pages"]}
        run.trace.append({"tool": tool.name, "args": arguments, "result": text,
                          "seconds": round(time.time() - started, 2), "status": status})
        return text

    return StructuredTool(name=tool.name, description=tool.description or tool.name,
                          args_schema=schema, coroutine=call)


# ---------------------------------------------------------------- guardrail

def is_refusal(answer: str) -> bool:
    return answer.lstrip().startswith(REFUSAL)


def check_answer(answer: str, run: Run) -> list[str]:
    """What is wrong with this answer, in words the model can act on. Empty list = fine."""
    problems = []
    cited = list(dict.fromkeys(CITED_ID.findall(answer)))
    if run.searches == 0:
        problems.append("You did not call `search`. Always search before answering.")
    invented = [i for i in cited if i not in run.retrieved]
    if invented:
        problems.append(f"You cited passage ids that `search` did not return: {', '.join(invented)}. "
                        f"Cite only ids from the search results.")
    if not cited and not is_refusal(answer):
        problems.append(f"Your answer cites no passage. Cite the [id] of the passage behind each claim, "
                        f"or, if the documents do not contain the answer, begin with \"{REFUSAL}.\"")
    return problems


def final_text(messages) -> str:
    for message in reversed(messages):
        if isinstance(message, AIMessage) and not message.tool_calls:
            return str(message.text).strip()
    return ""


def token_usage(messages) -> tuple[int, int]:
    used = [m.usage_metadata for m in messages if isinstance(m, AIMessage) and m.usage_metadata]
    return sum(u.get("input_tokens", 0) for u in used), sum(u.get("output_tokens", 0) for u in used)


# ---------------------------------------------------------------- the agent

def build_model(name: str):
    from langchain_google_genai import ChatGoogleGenerativeAI
    # No temperature: these models use fixed sampling settings, so the same question can get
    # slightly different answers on different runs.
    return ChatGoogleGenerativeAI(model=name, max_retries=MODEL_RETRIES,
                                  timeout=MODEL_TIMEOUT, google_api_key=load_api_key())


async def ask_async(question: str, approve=None, model=None) -> AgentResult:
    """Answer one question. approve(tool_name, args) -> bool decides add_document; default: ask in the terminal.

    Tries each model of CHAT_MODELS in turn while the failure is "unavailable" (busy, timeout, quota).
    A model object can be passed instead (the tests do this).
    """
    started = time.time()
    names = [None] if model is not None else CHAT_MODELS
    for position, name in enumerate(names):
        result = await _ask_once(question, approve, model if model is not None else build_model(name),
                                 name or "given model")
        if not result.error or position == len(names) - 1 or not any(w in result.error for w in UNAVAILABLE):
            break
        print(f"  model {name} unavailable ({result.error[:80]}); trying {names[position + 1]}",
              file=sys.stderr, flush=True)
    result.seconds = round(time.time() - started, 1)
    return result


async def _ask_once(question: str, approve, model, model_name: str) -> AgentResult:
    started = time.time()
    run = Run(approve or ask_in_terminal)
    system_prompt = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    params = StdioServerParameters(command=sys.executable, args=[str(SERVER_SCRIPT)], cwd=str(ROOT))
    answer, problems, guardrail, messages, error = "", [], "ok", [], None
    try:
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                tools = [langchain_tool(session, t, run) for t in (await session.list_tools()).tools]
                agent = create_agent(model, tools, system_prompt=system_prompt)
                config = {"recursion_limit": RECURSION_LIMIT}
                messages = (await agent.ainvoke({"messages": [HumanMessage(question)]}, config))["messages"]
                answer = final_text(messages)
                problems = check_answer(answer, run)
                if problems:  # one retry, with the problems spelled out
                    feedback = "Your answer did not pass the citation check:\n- " + "\n- ".join(problems)
                    messages = (await agent.ainvoke({"messages": messages + [HumanMessage(feedback)]},
                                                    config))["messages"]
                    answer = final_text(messages)
                    guardrail = "blocked" if check_answer(answer, run) else "fixed_on_retry"
    except Exception as exc:  # noqa: BLE001 - a model or network failure is a result, not a crash
        while getattr(exc, "exceptions", None):  # unwrap the groups the MCP client wraps errors in
            exc = exc.exceptions[0]
        error = f"{type(exc).__name__}: {exc}"
    raw = answer
    if error:
        shown, guardrail = "", "error"
    elif guardrail == "blocked":
        shown = BLOCKED_ANSWER
    else:
        shown = answer
    cited = [run.retrieved[i] for i in dict.fromkeys(CITED_ID.findall(shown)) if i in run.retrieved]
    tokens_in, tokens_out = token_usage(messages)
    return AgentResult(
        question=question, answer=shown, raw_answer=raw, sources=cited, trace=run.trace,
        guardrail=guardrail, problems=problems, refused=is_refusal(shown),
        tool_calls=run.calls,
        seconds=round(time.time() - started, 1), input_tokens=tokens_in, output_tokens=tokens_out,
        error=error, model=model_name)


def ask(question: str, approve=None, model=None) -> AgentResult:
    return asyncio.run(ask_async(question, approve, model))


def render(result: AgentResult) -> str:
    """The answer followed by the passages it cites."""
    lines = [result.answer]
    if result.sources:
        lines += ["", "Fuentes:"] + [f"- [{s['id']}] {s['title']} | {s['location']} | {s['pages']}"
                                      for s in result.sources]
    return "\n".join(lines)


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit('usage: python agent.py "your question"')
    outcome = ask(" ".join(sys.argv[1:]))
    if outcome.error:
        sys.exit(f"The agent failed: {outcome.error}")
    print(render(outcome))
    print(f"\n[{outcome.model}, {outcome.tool_calls} tool call(s), {outcome.seconds}s, "
          f"{outcome.input_tokens + outcome.output_tokens} tokens, citation check: {outcome.guardrail}]",
          file=sys.stderr)
