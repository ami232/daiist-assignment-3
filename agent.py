"""
Assignment 3: your agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with tools from server.py over MCP and
AGENTS.md as system prompt. Guardrails:
  1. approval: add_document never runs without the user's yes (asked in the terminal;
     evaluation runs deny it);
  2. call limits: at most MAX_MODEL_CALLS model calls and MAX_TOOL_CALLS tool calls per question;
  3. citation guard (my own choice): every [Source, Location] in the answer must be a passage
     that search really returned; an answer with an invalid citation, or with claims and no
     citation, is sent back once for repair and otherwise replaced by a refusal.

Import `run(questions)` to get answers plus the tool trace (used by evaluate.py).
"""

import asyncio
import os
import re
import sys
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware, ToolCallLimitMiddleware
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.tools import StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from pydantic import BaseModel, Field

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
AGENT_MODEL = os.environ.get("GEMINI_AGENT_MODEL", "gemini-3.5-flash-lite")
MAX_MODEL_CALLS = 8
MAX_TOOL_CALLS = 6
REFUSAL = "No puedo responder con los documentos disponibles."

CITATION_RE = re.compile(r"\[([^\[\]]+?),\s*([^\[\]]+?)\]")
RETRIEVED_RE = re.compile(r"CITATION: \[([^\[\]]+?),\s*([^\[\]]+?)\]")


# ------------------------------------------------------------------ results

@dataclass
class Result:
    question: str
    answer: str = ""
    refused: bool = False
    citations: list = field(default_factory=list)        # [source, location] in the answer
    invalid_citations: list = field(default_factory=list)
    retrieved: list = field(default_factory=list)        # [source, location] returned by search
    tool_trace: list = field(default_factory=list)       # {tool, args, output}
    guard: str = ""                                       # "", "repaired" or "replaced"
    first_answer: str = ""                                # answer the guard rejected (when it fired)
    first_invalid: list = field(default_factory=list)     # its citations that search never returned
    model_calls: int = 0
    input_tokens: int = 0
    output_tokens: int = 0
    seconds: float = 0.0
    error: str = ""

    def to_dict(self) -> dict:
        return asdict(self)


# -------------------------------------------------------------------- tools

class SearchArgs(BaseModel):
    query: str = Field(description="Search query, in Spanish")
    k: int = Field(default=5, description="Number of passages to return (1-10)")


class AddArgs(BaseModel):
    path: str = Field(description="Path of the file to add to the index")


async def deny_all(path: str) -> bool:
    return False


async def ask_user_approval(path: str) -> bool:
    """Guardrail 1: the user must say yes in the terminal before add_document runs."""
    prompt = f"\nThe assistant wants to add this document to the index:\n  {path}\nApprove? [y/N] "
    try:
        reply = await asyncio.to_thread(input, prompt)
    except EOFError:        # no terminal to ask: treat as "no"
        return False
    return reply.strip().lower() in {"y", "yes", "s", "si", "sí"}


def build_tools(tool_defs, call_tool, approve) -> list:
    """LangChain tools that forward to the MCP server; descriptions come from the server."""
    desc = {t.name: (t.description or "") for t in tool_defs}

    async def search(query: str, k: int = 5) -> str:
        return await call_tool("search", {"query": query, "k": k})

    async def add_document(path: str) -> str:
        if not await approve(path):
            return "NOT ADDED: the user did not approve adding this document."
        return await call_tool("add_document", {"path": path})

    return [
        StructuredTool.from_function(coroutine=search, name="search", description=desc.get("search", "search"),
                                     args_schema=SearchArgs),
        StructuredTool.from_function(coroutine=add_document, name="add_document",
                                     description=desc.get("add_document", "add a document"),
                                     args_schema=AddArgs),
    ]


def build_agent(tool_defs, call_tool, approve=deny_all, model=None):
    model = model or ChatGoogleGenerativeAI(
        model=AGENT_MODEL, google_api_key=load_api_key(), max_retries=3)
    return create_agent(
        model,
        build_tools(tool_defs, call_tool, approve),
        system_prompt=(ROOT / "AGENTS.md").read_text(encoding="utf-8"),
        middleware=[
            ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS, exit_behavior="end"),
            ToolCallLimitMiddleware(run_limit=MAX_TOOL_CALLS, exit_behavior="continue"),
        ],
    )


# ------------------------------------------------------------------ answers

def _text(content) -> str:
    return content if isinstance(content, str) else " ".join(
        b.get("text", "") if isinstance(b, dict) else str(b) for b in content)


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace("\xa0", " ")).strip().lower()


def _inspect(messages) -> dict:
    """Pull answer, trace, retrieved passages and token counts out of a message list."""
    outputs = {m.tool_call_id: _text(m.content) for m in messages if isinstance(m, ToolMessage)}
    trace, retrieved, calls, tin, tout, answer = [], [], 0, 0, 0, ""
    for m in messages:
        if isinstance(m, AIMessage):
            calls += 1
            usage = m.usage_metadata or {}
            tin += usage.get("input_tokens", 0)
            tout += usage.get("output_tokens", 0)
            for tc in m.tool_calls:
                out = outputs.get(tc["id"], "")
                trace.append({"tool": tc["name"], "args": tc["args"], "output": out})
                if tc["name"] == "search":
                    retrieved += [[s.strip(), l.strip()] for s, l in RETRIEVED_RE.findall(out)]
            if not m.tool_calls:
                answer = m.text.strip() if hasattr(m, "text") else _text(m.content).strip()
    return {"answer": answer, "trace": trace, "retrieved": retrieved, "calls": calls, "tin": tin, "tout": tout}


def _check(answer: str, retrieved: list) -> tuple[bool, list, list]:
    """Return (answer is acceptable, citations, invalid citations)."""
    known = {(_norm(s), _norm(l)) for s, l in retrieved}
    cites = [[s.strip(), l.strip()] for s, l in CITATION_RE.findall(answer)]
    invalid = [c for c in cites if (_norm(c[0]), _norm(c[1])) not in known]
    refused = _norm(answer).startswith(_norm(REFUSAL))
    ok = not invalid and (refused or bool(cites))
    return ok, cites, invalid


REPAIR = ("Your answer cannot be accepted: every claim needs a citation [Source, Location] copied exactly from a "
          "CITATION line returned by the search tool in this conversation{why}. Search again if needed. Rewrite "
          "the answer using only retrieved passages, or, if they do not answer the question, start with exactly "
          f"'{REFUSAL}'")


async def answer(agent, question: str) -> Result:
    """Run the agent on one question and apply the citation guard (guardrail 3)."""
    res = Result(question=question)
    started = time.time()
    try:
        out = await agent.ainvoke({"messages": [HumanMessage(question)]})
        info = _inspect(out["messages"])
        if info["trace"] and all(t["tool"] == "add_document" for t in info["trace"]):
            ok, cites, invalid = True, [], []     # a report on adding a document has no legal claims to cite
        else:
            ok, cites, invalid = _check(info["answer"], info["retrieved"])
        if not ok:
            why = f" (invalid: {invalid})" if invalid else " (your answer had no citation)"
            res.first_answer, res.first_invalid = info["answer"], invalid
            out = await agent.ainvoke({"messages": out["messages"] + [HumanMessage(REPAIR.format(why=why))]})
            info = _inspect(out["messages"])
            ok, cites, invalid = _check(info["answer"], info["retrieved"])
            res.guard = "repaired"
        if not ok:
            res.guard = "replaced"
            info["answer"] = (f"{REFUSAL} No he podido respaldar una respuesta con citas válidas de los "
                              "documentos recuperados.")
            cites, invalid = [], []
        res.answer, res.citations, res.invalid_citations = info["answer"], cites, invalid
        res.retrieved, res.tool_trace = info["retrieved"], info["trace"]
        res.model_calls, res.input_tokens, res.output_tokens = info["calls"], info["tin"], info["tout"]
        res.refused = _norm(res.answer).startswith(_norm(REFUSAL))
    except Exception as error:  # noqa: BLE001 - report it, keep evaluating other questions
        res.error = f"{type(error).__name__}: {str(error)[:300]}"
        res.answer = f"{REFUSAL} (error: {res.error})"
        res.refused = True
    res.seconds = round(time.time() - started, 2)
    return res


# ---------------------------------------------------------------------- run

async def run_async(questions: list[str], approve=deny_all, model=None, pause: float = 0) -> list[Result]:
    """Start server.py over MCP, answer every question with one agent, return Results."""
    params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT),
                                   env=dict(os.environ))
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tool_defs = (await session.list_tools()).tools

            async def call_tool(name: str, args: dict) -> str:
                result = await session.call_tool(name, args)
                text = "\n".join(getattr(c, "text", "") for c in result.content).strip()
                return f"ERROR: {text}" if getattr(result, "is_error", False) or getattr(result, "isError", False) else text

            agent = build_agent(tool_defs, call_tool, approve, model)
            results = []
            for q in questions:
                results.append(await answer(agent, q))
                if pause:
                    await asyncio.sleep(pause)      # stay under the free-tier request limits
            return results


def run(questions: list[str], approve=deny_all, model=None, pause: float = 0) -> list[Result]:
    """Synchronous entry point for evaluate.py. `approve` is an async callable(path) -> bool."""
    return asyncio.run(run_async(questions, approve, model, pause))

def ask(question: str, approve=ask_user_approval) -> Result:
    return run([question], approve)[0]


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit('usage: python agent.py "your question"')
    result = ask(" ".join(sys.argv[1:]))
    print(result.answer)
    sources = sorted({f"[{s}, {l}]" for s, l in result.citations})
    if sources:
        print("\nSources: " + "; ".join(sources))
    print(f"\n({result.model_calls} model calls, {len(result.tool_trace)} tool calls, "
          f"{result.input_tokens}+{result.output_tokens} tokens, {result.seconds}s"
          f"{', guard: ' + result.guard if result.guard else ''})", file=sys.stderr)
    if result.guard:
        print(f"\n[guard {result.guard}] first answer was rejected. Invalid citations: {result.first_invalid or 'none (no citation at all)'}"
              f"\nFirst answer:\n{result.first_answer}", file=sys.stderr)
    if result.error:
        raise SystemExit(f"agent error: {result.error}")