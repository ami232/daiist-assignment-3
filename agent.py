"""
Assignment 3: the agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the tools of server.py over MCP and
AGENTS.md as the system prompt. Adapted from session 10's 07-own-harness/harness.py.

Guardrails (middleware: the harness runs them, so the model cannot skip them):
  1. approval: add_document changes the index, so a person must say yes in the
     terminal first. With no terminal (evaluation, check.py) it is denied.
  2. call limits: at most MAX_SEARCHES searches and MAX_MODEL_CALLS model calls
     per question, so a confused model cannot loop or burn quota.
  3. citation validator (the student's choice, tasks.md 5.4): every [FUENTE, Ubicación]
     in the final answer must be a passage that search returned in this run, and an
     answer that is not the refusal must cite something. If not, the model gets one
     chance to fix it; if it fails again, the answer is replaced by the refusal.

For evaluate.py:
    async with open_agent(approve=deny) as agent:
        result = await ask(agent, "¿…?")   # {answer, citations, trace, tokens, seconds, …}
"""

import asyncio
import re
import sys
import time
import warnings
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Callable

from langchain.agents import create_agent
from langchain.agents.middleware import (
    ModelCallLimitMiddleware,
    ToolCallLimitMiddleware,
    after_model,
    wrap_tool_call,
)
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from api_key import load_api_key
from rag import citations_in

with warnings.catch_warnings():
    warnings.simplefilter("ignore")              # langchain.mcp is in beta and warns on import
    from langchain.mcp import MCPAdapter

ROOT = Path(__file__).resolve().parent
SERVER = ROOT / "server.py"
RULES = ROOT / "AGENTS.md"

MODEL = "gemini-3.5-flash-lite"                  # fast, cheap, generous free tier; checked 2026-11-20
NEEDS_APPROVAL = {"add_document"}                # tools that change the index
MAX_SEARCHES = 4
MAX_MODEL_CALLS = 8
REFUSAL = ("No se ha encontrado contenido relacionado a tu pregunta en los documentos a los que tengo acceso. "
           "Consulte con un técnico especialista.")


# --------------------------------------------------------------------------- #
# Guardrail 1: human approval before the index changes                        #
# --------------------------------------------------------------------------- #

def ask_in_terminal(call: dict) -> bool:
    """Ask the person at the keyboard. No terminal (evaluation, CI) means no."""
    if not sys.stdin.isatty():
        print(f"  [aprobación] {call['name']} denegada: no hay terminal para preguntar.", file=sys.stderr)
        return False
    reply = input(f"\n  ¿Permitir {call['name']}({call['args']})? Modifica el índice. [s/N] ")
    return reply.strip().lower() in {"s", "si", "sí", "y", "yes"}


def deny(call: dict) -> bool:
    return False


def approval_guardrail(approve: Callable[[dict], bool]):
    @wrap_tool_call
    async def approve_index_changes(request, handler):
        call = request.tool_call
        if call["name"] in NEEDS_APPROVAL and not approve(call):
            return ToolMessage(
                content="El usuario no ha autorizado esta llamada: el índice no se ha modificado. "
                        "No intentes conseguir el documento de otra forma; responde con lo que ya tienes.",
                tool_call_id=call["id"],
                name=call["name"],
                status="error",
            )
        return await handler(request)

    return approve_index_changes


# --------------------------------------------------------------------------- #
# Guardrail 3: citation validator                                              #
# --------------------------------------------------------------------------- #

GUARDRAIL = "citation_guardrail"                 # name on the messages this guardrail adds, to find them later


def citation_problems(answer: str, retrieved: set[tuple[str, str]]) -> list[str]:
    """What is wrong with the answer's citations, given the (source, location) pairs search returned."""
    cited = citations_in(answer)
    problems = [f"[{s}, {loc}] no aparece en los resultados de search" for s, loc in cited if (s, loc) not in retrieved]
    if not cited and REFUSAL not in answer:
        problems.append("la respuesta no cita ningún fragmento y no es la frase de rechazo")
    return problems


def retrieved_pairs(messages) -> set[tuple[str, str]]:
    pairs = set()
    for message in messages:
        if isinstance(message, ToolMessage) and message.name == "search" and message.status != "error":
            for citation in sources_in(message.text):
                pairs.update(citations_in(citation))
    return pairs


@after_model(can_jump_to=["model"], name="CitationValidator")
def validate_citations(state, runtime):
    messages = state["messages"]
    last = messages[-1]
    if not isinstance(last, AIMessage) or last.tool_calls:
        return None                              # still searching: nothing to check yet
    problems = citation_problems(last.text, retrieved_pairs(messages))
    if not problems:
        return None
    already_warned = any(isinstance(m, HumanMessage) and m.name == GUARDRAIL for m in messages)
    if already_warned:                           # second failure: refuse instead of showing it
        return {"messages": [AIMessage(content=REFUSAL, name=GUARDRAIL)]}
    feedback = ("Revisión automática de citas: " + "; ".join(problems) + ". Reescribe la respuesta citando solo "
                "fragmentos que devolvió search, copiando [FUENTE, Ubicación] tal cual. Quita lo que no puedas "
                "respaldar; si no queda nada, responde con la frase de rechazo.")
    return {"messages": [HumanMessage(content=feedback, name=GUARDRAIL)], "jump_to": "model"}


# --------------------------------------------------------------------------- #
# Agent                                                                        #
# --------------------------------------------------------------------------- #

def build_agent(tools, approve: Callable[[dict], bool] = ask_in_terminal):
    load_api_key()                               # puts GEMINI_API_KEY in the environment for langchain
    return create_agent(
        model=ChatGoogleGenerativeAI(model=MODEL, max_retries=3),
        tools=tools,
        system_prompt=RULES.read_text(encoding="utf-8"),
        middleware=[
            approval_guardrail(approve),
            ToolCallLimitMiddleware(tool_name="search", run_limit=MAX_SEARCHES, exit_behavior="continue"),
            ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS, exit_behavior="end"),
            validate_citations,
        ],
    )


@asynccontextmanager
async def open_agent(approve: Callable[[dict], bool] = ask_in_terminal):
    """Start server.py over stdio, wrap its tools, and yield a ready agent. One server for many questions."""
    async with MCPAdapter(SERVER) as adapter:
        yield build_agent(await adapter.list_tools(), approve)


def tool_trace(messages) -> list[dict]:
    """Every tool call and its result, in order: what the harness saw happen."""
    trace = []
    for message in messages:
        if isinstance(message, AIMessage):
            trace += [{"call": c["name"], "args": c["args"]} for c in message.tool_calls]
        elif isinstance(message, ToolMessage):
            trace.append({"result": message.name, "status": message.status, "text": message.text})
    return trace


def sources_in(search_output: str) -> dict[str, str]:
    """{"[LETA, Artículo 38 ter]": BOE url} for every passage in a search result."""
    found = {}
    for block in search_output.split("\n---\n"):
        citation = re.search(r"Cita: (\[[^\]]+\])", block)
        url = re.search(r"^BOE: (\S+)", block, re.MULTILINE)
        if citation:
            found[citation.group(1)] = url.group(1) if url else ""
    return found


async def ask(agent, question: str) -> dict:
    """Run one question. Returns the answer, its citations, the trace, retrieved passages, tokens and seconds."""
    started = time.perf_counter()
    result = await agent.ainvoke({"messages": [{"role": "user", "content": question}]})
    seconds = time.perf_counter() - started
    messages = result["messages"]

    tokens = {"input": 0, "output": 0, "total": 0}
    model_calls = 0
    for message in messages:
        if isinstance(message, AIMessage) and message.usage_metadata:
            model_calls += 1
            for key in tokens:
                tokens[key] += message.usage_metadata.get(f"{key}_tokens", 0)

    trace = tool_trace(messages)
    retrieved = [t["text"] for t in trace if t.get("result") == "search" and t["status"] != "error"]
    sources: dict[str, str] = {}
    for text in retrieved:
        sources.update(sources_in(text))

    # A real final answer is a model message (it has token usage) asking for no more tools. Anything
    # else is the call-limit middleware stopping the run: never show a half-finished run as an answer.
    final = messages[-1]
    finished = isinstance(final, AIMessage) and not final.tool_calls and (
        bool(final.usage_metadata) or final.name == GUARDRAIL)
    text = final.text.strip() if finished else ""
    stopped = None if finished else "model_call_limit"
    if not text:
        text = REFUSAL
    warned = any(isinstance(m, HumanMessage) and m.name == GUARDRAIL for m in messages)
    guardrail = ("refused" if final.name == GUARDRAIL else "repaired") if warned else None

    return {
        "question": question,
        "answer": text,
        "citations": [f"[{s}, {loc}]" for s, loc in citations_in(text)],
        "retrieved_citations": list(sources),
        "sources": sources,
        "trace": trace,
        "retrieved": retrieved,
        "searches": sum(1 for t in trace if t.get("call") == "search"),
        "model_calls": model_calls,
        "stopped": stopped,
        "citation_guardrail": guardrail,         # None, "repaired" (fixed after one warning) or "refused"
        "tokens": tokens,
        "seconds": round(seconds, 2),
    }


def answer(question: str, approve: Callable[[dict], bool] = ask_in_terminal) -> dict:
    """Synchronous one-off: start the server, answer one question, stop the server."""
    async def run():
        async with open_agent(approve) as agent:
            return await ask(agent, question)

    return asyncio.run(run())


def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    question = " ".join(sys.argv[1:]).strip()
    if not question:
        raise SystemExit('Uso: uv run python agent.py "tu pregunta"')
    result = answer(question)

    for step in result["trace"]:
        if "call" in step:
            print(f"  → {step['call']}({step['args']})", file=sys.stderr)
    print(result["answer"])
    if result["citations"]:
        print("\nCitas:")
        for citation in result["citations"]:
            url = result["sources"].get(citation)
            print(f"  {citation} {url or '(no aparece en los fragmentos recuperados)'}")
    print(f"\n({result['searches']} búsquedas, {result['tokens']['total']} tokens, {result['seconds']:.1f} s)")


if __name__ == "__main__":
    main()
