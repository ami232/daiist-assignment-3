"""
Assignment 3: the agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini. Its tools are the ones server.py lists,
called over MCP (stdio); its system prompt is AGENTS.md.

Guardrails:
  (a) approval      add_document runs only after a y/n in the terminal; when
                    nobody can be asked (no terminal) it is denied.
  (b) call limit    at most MAX_TOOL_CALLS tool calls per question.
  (c) citations     after the answer, code checks that every [doc_id, location]
                    it cites was returned by a search in this same run. If one
                    was not, the answer is replaced with a refusal and logged.

    result = run("What is the nominal track gauge?")   # for evaluate.py
    result["answer"], result["citations"], result["tool_trace"], result["retrieved_chunks"],
    result["guardrail_fired"], result["input_tokens"], result["output_tokens"], result["seconds"]

Environment:
  AGENT_MODEL     Gemini model (default gemini-3.6-flash)
  SEARCH_DESIGN   passed on to server.py (article|fixed)

stdout carries only the answer and its citations; everything else goes to stderr.
"""

from __future__ import annotations

import asyncio
import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MODEL = os.environ.get("AGENT_MODEL", "").strip() or "gemini-3.6-flash"
MAX_TOOL_CALLS = 6
RECURSION_LIMIT = 40  # backstop in graph steps, far above what MAX_TOOL_CALLS allows
APPROVAL_REQUIRED = {"add_document"}

NOT_COVERED = "The corpus does not cover this question."  # the sentence AGENTS.md asks for (rule 3)
CITATION_REFUSAL = (
    "I can't give a verified answer to this question. My draft cited {bad}, which {verb} not among the "
    "passages the search returned, so I have withheld it rather than risk an unsupported claim. "
    "Please check the act itself (consolidated text on EUR-Lex) or ask again more specifically."
)
NO_ANSWER_REFUSAL = (
    "I could not produce an answer from the corpus for this question. "
    "Please check the act itself (consolidated text on EUR-Lex) or ask again more specifically."
)

# One search result as server.py's format_hits() writes it.
RESULT_HEAD = re.compile(
    r"^=== Result (\d+) of \d+ ===\nCitation: \[([^,\]\n]+), ([^\n]+)\]\nDocument: ([^\n]*)\nSource: ([^\n]*)\nSimilarity: (-?[\d.]+)\nText:\n",
    re.M,
)
# "[Dir_2016_798, Article 14(3)]": an identifier, a comma, a location. Locations never contain square brackets.
CITATION = re.compile(r"\[\s*([A-Za-z][A-Za-z0-9_]*)\s*,\s*([^\[\]]+?)\s*\]")


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


# ----------------------------------------------------------------------------
# Guardrail (c): citation check. Pure functions, no API calls.
# ----------------------------------------------------------------------------

def _key(doc_id: str, location: str) -> tuple[str, str]:
    return doc_id.strip().casefold(), re.sub(r"\s+", " ", location).strip().casefold()


def parse_search_results(text: str) -> list[dict]:
    """The passages in one search tool result, as dicts."""
    heads = list(RESULT_HEAD.finditer(text))
    chunks = []
    for i, head in enumerate(heads):
        end = heads[i + 1].start() if i + 1 < len(heads) else len(text)
        chunks.append({
            "rank": int(head.group(1)),
            "doc_id": head.group(2).strip(),
            "location": head.group(3).strip(),
            "doc_title": head.group(4).strip(),
            "source_url": head.group(5).strip(),
            "score": float(head.group(6)),
            "text": text[head.end():end].strip(),
        })
    return chunks


def extract_citations(answer: str, known: set[tuple[str, str]] = frozenset()) -> list[tuple[str, str]]:
    """Every (doc_id, location) the answer cites, in order, without repeats.

    "[A, x; B, y]" counts as two citations when the bracket as a whole is not a known one.
    """
    found = []
    for match in CITATION.finditer(answer):
        pairs = [(match.group(1), match.group(2))]
        if _key(*pairs[0]) not in known and ";" in match.group(2):
            parts = [CITATION.fullmatch(f"[{part.strip()}]") for part in f"{match.group(1)}, {match.group(2)}".split(";")]
            if all(parts):
                pairs = [(part.group(1), part.group(2)) for part in parts]
        for pair in pairs:
            if pair not in found:
                found.append(pair)
    return found


def check_citations(answer: str, retrieved_chunks: list[dict]) -> tuple[list[dict], list[str]]:
    """Returns (valid citations with their source, invalid citations as written)."""
    retrieved = {}
    for chunk in retrieved_chunks:
        retrieved.setdefault(_key(chunk["doc_id"], chunk["location"]), chunk)
    valid, invalid = [], []
    for doc_id, location in extract_citations(answer, set(retrieved)):
        chunk = retrieved.get(_key(doc_id, location))
        if chunk is None:
            invalid.append(f"[{doc_id}, {location}]")
        else:
            valid.append({key: chunk.get(key, "") for key in ("doc_id", "location", "doc_title", "source_url")})
    return valid, invalid


def apply_citation_guardrail(answer: str, retrieved_chunks: list[dict]) -> dict:
    """Guardrail (c). If the answer cites anything this run's searches did not return, refuse instead.

    Returns {"answer", "citations", "invalid_citations", "fired"}.
    """
    valid, invalid = check_citations(answer, retrieved_chunks)
    if not invalid:
        return {"answer": answer, "citations": valid, "invalid_citations": [], "fired": False}
    log(f"[guardrail] citation check FIRED: {', '.join(invalid)} not in this run's {len(retrieved_chunks)} retrieved passages; answer replaced with a refusal.")
    refusal = CITATION_REFUSAL.format(bad=", ".join(invalid), verb="was" if len(invalid) == 1 else "were")
    return {"answer": refusal, "citations": [], "invalid_citations": invalid, "fired": True}


# ----------------------------------------------------------------------------
# Guardrail (a): human approval
# ----------------------------------------------------------------------------

def ask_in_terminal(tool: str, args: dict) -> bool:
    """y/n in the terminal. Denies when there is no terminal to ask in (tests, CI, evaluate)."""
    if not (sys.stdin.isatty() and sys.stderr.isatty()):
        log(f"[guardrail] approval: {tool}({args}) DENIED automatically (not interactive, nobody to ask).")
        return False
    log(f"\nThe agent wants to run {tool} with {args}.\nIt changes the index and spends embedding quota.")
    sys.stderr.write("Allow it? [y/N] ")
    sys.stderr.flush()
    approved = sys.stdin.readline().strip().lower() in ("y", "yes")
    log(f"[guardrail] approval: {tool} {'APPROVED' if approved else 'DENIED'} by the user.")
    return approved


# ----------------------------------------------------------------------------
# The agent
# ----------------------------------------------------------------------------

def _system_prompt() -> str:
    text = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    return re.sub(r"<!--.*?-->", "", text, flags=re.S).strip()


def _as_langchain_tool(session, tool):
    """One MCP tool as a LangChain tool: same name, description and argument schema."""
    from langchain_core.tools import StructuredTool

    async def call(**arguments) -> str:
        result = await session.call_tool(tool.name, arguments)
        text = "\n".join(getattr(content, "text", "") for content in result.content).strip()
        if getattr(result, "is_error", False):
            return f"TOOL ERROR: {tool.name} failed: {text[:500]}"
        return text

    return StructuredTool.from_function(coroutine=call, name=tool.name, description=tool.description or tool.name, args_schema=tool.input_schema)


async def answer_with(model, tools, question: str, approve=None, system_prompt: str | None = None) -> dict:
    """The harness itself: agent loop plus the three guardrails, for any chat model and tool list.

    arun() calls it with Gemini and the MCP tools; the tests call it with a scripted model.
    """
    from langchain.agents import create_agent
    from langchain.agents.middleware import AgentMiddleware, ToolCallLimitMiddleware
    from langchain_core.messages import AIMessage, ToolMessage
    from langgraph.errors import GraphRecursionError

    approve = approve or ask_in_terminal
    trace: list[dict] = []
    retrieved: list[dict] = []
    fired: list[str] = []

    class Harness(AgentMiddleware):
        """Sits around every tool call: guardrail (a) and the tool trace."""

        async def awrap_tool_call(self, request, handler):
            call = request.tool_call
            name, args = call["name"], dict(call.get("args") or {})
            entry = {"tool": name, "args": args, "status": "ok", "seconds": 0.0, "results": []}
            trace.append(entry)
            if name in APPROVAL_REQUIRED and not approve(name, args):
                entry["status"] = "denied"
                if "approval_denied" not in fired:
                    fired.append("approval_denied")
                return ToolMessage(
                    content=f"DENIED: the user did not approve {name}. It was NOT run and nothing was added. Do not try again; tell the user.",
                    tool_call_id=call["id"], name=name, status="error",
                )
            tool_started = time.time()
            result = await handler(request)
            entry["seconds"] = round(time.time() - tool_started, 2)
            content = result.content if isinstance(result, ToolMessage) and isinstance(result.content, str) else str(getattr(result, "content", result))
            if content.startswith(("TOOL ERROR", "SEARCH FAILED", "NOT ADDED", "INCOMPLETE")) or getattr(result, "status", "") == "error":
                entry["status"] = "error"
                entry["message"] = content[:300]
            chunks = parse_search_results(content)
            for chunk in chunks:
                retrieved.append({**chunk, "query": args.get("query", "")})
            entry["results"] = [f"[{chunk['doc_id']}, {chunk['location']}] {chunk['score']:.3f}" for chunk in chunks]
            return result

    agent = create_agent(
        model,
        tools,
        system_prompt=system_prompt if system_prompt is not None else _system_prompt(),
        middleware=[
            ToolCallLimitMiddleware(run_limit=MAX_TOOL_CALLS, exit_behavior="continue"),  # guardrail (b)
            Harness(),
        ],
    )
    state = None
    try:
        async for state in agent.astream(
            {"messages": [{"role": "user", "content": question}]},
            config={"recursion_limit": RECURSION_LIMIT},
            stream_mode="values",
        ):
            pass
    except GraphRecursionError:
        fired.append("step_limit")
        log(f"[guardrail] step limit FIRED: no final answer within {RECURSION_LIMIT} steps.")

    messages = state["messages"] if state else []
    input_tokens = output_tokens = 0
    for message in messages:
        if isinstance(message, AIMessage) and message.usage_metadata:
            input_tokens += message.usage_metadata.get("input_tokens", 0)
            output_tokens += message.usage_metadata.get("output_tokens", 0)
        if isinstance(message, ToolMessage) and str(message.content).startswith("Tool call limit exceeded"):
            trace.append({"tool": message.name or "", "args": {}, "status": "blocked", "seconds": 0.0, "results": []})
            if "tool_call_limit" not in fired:
                fired.append("tool_call_limit")
                log(f"[guardrail] tool-call limit FIRED: more than {MAX_TOOL_CALLS} tool calls were requested; the extra ones were blocked.")

    draft = ""
    if "step_limit" not in fired and messages and isinstance(messages[-1], AIMessage) and not messages[-1].tool_calls:
        draft = str(messages[-1].text or "").strip()
    if draft:
        checked = apply_citation_guardrail(draft, retrieved)  # guardrail (c)
        if checked["fired"]:
            fired.append("citation_check")
    else:
        checked = {"answer": NO_ANSWER_REFUSAL, "citations": [], "invalid_citations": []}
        if "step_limit" not in fired:
            fired.append("empty_answer")
            log("[guardrail] the model returned no text; answer replaced with a refusal.")

    answer = checked["answer"]
    return {
        "question": question,
        "answer": answer,
        "citations": checked["citations"],
        "tool_trace": trace,
        "retrieved_chunks": retrieved,
        "guardrail_fired": fired,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "seconds": 0.0,
        # extras for the evaluation
        "refused": answer != draft or "corpus does not cover" in answer.casefold(),
        "draft_answer": draft,
        "invalid_citations": checked["invalid_citations"],
        "model": getattr(model, "model", "") or type(model).__name__,
    }


async def arun(question: str, approve=None) -> dict:
    """Answer one question with Gemini and server.py's tools over MCP (stdio).

    `approve(tool_name, args) -> bool` replaces the terminal prompt if given.
    """
    from langchain_google_genai import ChatGoogleGenerativeAI
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    from api_key import load_api_key

    started = time.time()
    load_api_key()
    # No temperature: this model uses fixed sampling defaults and ignores it.
    model = ChatGoogleGenerativeAI(model=MODEL, max_retries=4)
    server_env = {name: os.environ[name] for name in ("SEARCH_DESIGN", "GEMINI_API_KEY") if os.environ.get(name)}
    server = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT), env=server_env)
    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = [_as_langchain_tool(session, tool) for tool in (await session.list_tools()).tools]
            result = await answer_with(model, tools, question, approve)
    result["model"] = MODEL
    result["seconds"] = round(time.time() - started, 2)  # includes starting the MCP server
    return result


def run(question: str, approve=None) -> dict:
    """Answer one question and return the answer with everything evaluate.py needs.

    Keys: answer, citations (list of {doc_id, location, doc_title, source_url}),
    tool_trace, retrieved_chunks, guardrail_fired (list of guardrail names, empty
    if none), input_tokens, output_tokens, seconds; plus refused, draft_answer,
    invalid_citations, model, question.
    """
    return asyncio.run(arun(question, approve))


def main() -> int:
    question = " ".join(sys.argv[1:]).strip()
    if not question:
        log('Usage: uv run python main.py ask "your question"')
        return 2
    result = run(question)
    print(result["answer"])
    if result["citations"]:
        print("\nCitations:")
        for citation in result["citations"]:
            print(f"- [{citation['doc_id']}, {citation['location']}] {citation['doc_title']} <{citation['source_url']}>")
    else:
        print("\nCitations: none")
    calls = ", ".join(f"{entry['tool']}:{entry['status']}" for entry in result["tool_trace"]) or "none"
    log(
        f"\n[agent] model={result['model']}  tool calls: {calls}  guardrails fired: {', '.join(result['guardrail_fired']) or 'none'}  "
        f"tokens in/out: {result['input_tokens']}/{result['output_tokens']}  {result['seconds']}s"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
