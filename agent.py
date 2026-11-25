"""
Assignment 3: your agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with tools from server.py over MCP and
AGENTS.md as system prompt. Asks for approval before add_document runs, has a
call limit, a citation guardrail and a refusal guardrail. Prints the answer
with citations.

`answer_question(question)` returns the answer and the tool trace, for evaluate.py.
"""

import asyncio
import re
import sys
import time
import warnings
from pathlib import Path

from langchain.agents import create_agent
from langchain_core.tools import StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from api_key import load_api_key

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)

ROOT = Path(__file__).resolve().parent
# Tried in order; the next one is used if a model is overloaded (503), retired (404), out of quota (429) or too slow.
MODELS = ["gemini-3.5-flash-lite", "gemini-3.1-flash-lite", "gemini-3.5-flash",
          "gemini-3.8-flash", "gemini-3.7-flash", "gemini-3.6-flash"]
TRY_NEXT = ("503", "UNAVAILABLE", "504", "DEADLINE", "404", "NOT_FOUND", "429", "RESOURCE_EXHAUSTED", "Timeout", "timed out")
MODEL_TIMEOUT = 25        # seconds a single model request may take
COOLDOWN_SECONDS = 90     # a model that failed is skipped for this long (within one process)
MODEL_STATE = {"last_good": None, "cooldown": {}}
MAX_TOOL_CALLS = 8        # call limit: tool calls allowed per question
RECURSION_LIMIT = 30      # hard stop for the agent loop
REFUSAL = "I don't know based on the documents"

CITATION = re.compile(r"\[([^\[\]|]+?)\s*\|\s*([^\[\]|]+?)\s*\|\s*p\.\s*(\d+)\s*\]")
HEADER = re.compile(r"^\[\d+\] source: (.+?) \| location: (.+?) \| page: (\d+) \| relevance: (-?[\d.]+)", re.M)


# ---------- helpers ----------

def norm(text):
    return " ".join(text.lower().split())


def parse_passages(search_result):
    """The passages a search returned, read from their header lines."""
    return [{"source": s.strip(), "location": loc.strip(), "page": int(p), "relevance": float(r)}
            for s, loc, p, r in HEADER.findall(search_result)]


def text_of(message):
    """The text of a model message (Gemini may return a list of content blocks)."""
    content = message.content
    if isinstance(content, str):
        return content
    return "".join(part if isinstance(part, str) else part.get("text", "") for part in content)


def pick_models():
    """Models to try now: skip the ones that failed recently, try the last good one first."""
    now = time.time()
    ready = [m for m in MODELS if MODEL_STATE["cooldown"].get(m, 0) <= now]
    order = ready or list(MODELS)
    good = MODEL_STATE["last_good"]
    if good in order:
        order = [good] + [m for m in order if m != good]
    return order


# ---------- guardrail 1: approval before add_document ----------

def default_approve(path):
    """Ask the person. Without a terminal to ask in (e.g. during evaluation) the answer is no."""
    if not sys.stdin.isatty():
        return False
    reply = input(f"\nThe agent wants to add this file to the index:\n  {path}\n"
                  f"This changes the index and uses embedding quota. Allow? [y/N] ")
    return reply.strip().lower() in ("y", "yes")


# ---------- guardrail 2: citation check ----------

def check_citations(answer, passages):
    """Every citation must match a passage that a search really returned. Returns (ok, reason)."""
    text = answer.strip()
    if not text:
        return False, "the model gave no answer"
    cited = CITATION.findall(text)
    if not cited:
        return False, "the answer has no citation"
    known = {(norm(p["source"]), norm(p["location"]), p["page"]) for p in passages}
    bad = [c for c in cited if (norm(c[0]), norm(c[1]), int(c[2])) not in known]
    if bad:
        return False, "citation not among the retrieved passages: " + "; ".join(f"[{a} | {b} | p.{c}]" for a, b, c in bad)
    return True, "ok"


# ---------- guardrail 3: a refusal stays a refusal ----------

def is_refusal(text):
    return text.strip().lower().startswith(REFUSAL.lower())


def clean_refusal(text):
    """Keep only the first paragraph (at most 2 sentences). If that still contains numbers or citations,
    fall back to the plain refusal: a number from a nearby case can be dangerous."""
    paragraphs = [p.strip() for p in text.strip().split("\n\n") if p.strip()]
    first = paragraphs[0] if paragraphs else text.strip()
    first = " ".join(re.split(r"(?<=[.!?])\s+", first)[:2])
    if re.search(r"\d", first) or "[" in first:
        return REFUSAL + ". The documents do not cover this question."
    return first


# ---------- tools: the MCP server's tools, wrapped for LangChain ----------

async def call_server(session, state, name, arguments):
    """One tool call on the MCP server, with the call limit and the trace."""
    if state["calls"] >= MAX_TOOL_CALLS:
        return ("TOOL CALL LIMIT REACHED. Do not call more tools: answer from the passages you "
                "already have, or say you do not know.")
    state["calls"] += 1
    result = await session.call_tool(name, arguments)
    text = "\n".join(getattr(part, "text", "") for part in result.content)
    state["trace"].append({"tool": name, "args": arguments, "result": text})
    if name == "search":
        state["passages"] += parse_passages(text)
    return text


def build_tools(session, descriptions, state):
    async def search(query: str) -> str:
        return await call_server(session, state, "search", {"query": query})

    async def add_document(path: str) -> str:
        if not state["approve"](path):
            state["trace"].append({"tool": "add_document", "args": {"path": path}, "result": "DENIED: the user did not approve"})
            return "The user did not approve adding this document. Nothing was added. Tell the user it was not added."
        return await call_server(session, state, "add_document", {"path": path})

    return [StructuredTool.from_function(coroutine=fn, name=fn.__name__, description=descriptions[fn.__name__])
            for fn in (search, add_document)]


# ---------- the agent ----------

async def _answer(question, approve):
    load_api_key()   # puts the key into the environment for langchain-google-genai
    system_prompt = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    params = StdioServerParameters(command=sys.executable, args=[str(ROOT / "server.py")], cwd=str(ROOT))
    state = {"calls": 0, "trace": [], "passages": [], "approve": approve}

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            listed = await session.list_tools()
            descriptions = {t.name: t.description for t in listed.tools}
            tools = build_tools(session, descriptions, state)

            result, used_model, errors = None, None, []
            started = time.time()
            for _round in range(3):   # up to 3 rounds over the models, to ride out busy periods
                for name in pick_models():
                    state.update(calls=0, trace=[], passages=[])
                    try:
                        agent = create_agent(
                            ChatGoogleGenerativeAI(model=name, temperature=0, max_retries=0, timeout=MODEL_TIMEOUT),
                            tools, system_prompt=system_prompt)
                        result = await agent.ainvoke({"messages": [{"role": "user", "content": question}]},
                                                     config={"recursion_limit": RECURSION_LIMIT})
                        used_model = name
                        MODEL_STATE["last_good"] = name
                        break
                    except Exception as error:  # noqa: BLE001
                        text = f"{type(error).__name__}: {error}"
                        if any(code in text for code in TRY_NEXT):
                            errors.append(f"{name}: {text[:90]}")
                            MODEL_STATE["cooldown"][name] = time.time() + COOLDOWN_SECONDS
                            print(f"  (model {name} unavailable, trying the next one)", file=sys.stderr)
                            continue
                        raise
                if result is not None:
                    break
                await asyncio.sleep(10)
            seconds = time.time() - started

    if result is None:
        raise RuntimeError("No Gemini model was available after 3 rounds. Last errors: " + " | ".join(errors[-3:]))

    messages = result["messages"]
    final = next((m for m in reversed(messages) if m.type == "ai" and not m.tool_calls), None)
    draft = text_of(final).strip() if final else ""

    guardrail, kind = None, None
    if is_refusal(draft):
        answer = clean_refusal(draft)
        if answer != draft:
            guardrail, kind = "refusal trimmed: the draft had extra paragraphs, numbers or citations after the refusal", "refusal_trim"
    else:
        ok, reason = check_citations(draft, state["passages"])
        if ok:
            answer = draft
        else:
            answer = f"{REFUSAL}. (An answer was drafted but withheld by the citation check: {reason}.)"
            guardrail, kind = reason, "citation"

    usage = [getattr(m, "usage_metadata", None) or {} for m in messages if m.type == "ai"]
    return {
        "question": question,
        "answer": answer,
        "draft_answer": draft,
        "guardrail": guardrail,
        "guardrail_kind": kind,
        "model": used_model,
        "tool_calls": [{"tool": t["tool"], "args": t["args"]} for t in state["trace"]],
        "trace": state["trace"],
        "passages": state["passages"],
        "input_tokens": sum(u.get("input_tokens", 0) for u in usage),
        "output_tokens": sum(u.get("output_tokens", 0) for u in usage),
        "seconds": round(seconds, 1),
    }


def answer_question(question, approve=default_approve):
    """Answer one question. Returns the answer, the tool trace, tokens and seconds."""
    return asyncio.run(_answer(question, approve))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit('usage: python agent.py "your question"')
    out = answer_question(" ".join(sys.argv[1:]))
    print(out["answer"])
    print("\n" + "-" * 60)
    print("model:", out["model"])
    print("tool calls:", [(c["tool"], c["args"]) for c in out["tool_calls"]])
    print(f"tokens: {out['input_tokens']} in / {out['output_tokens']} out | {out['seconds']} s")
    if out["guardrail"]:
        print("GUARDRAIL FIRED:", out["guardrail"])
        print("draft answer was:", out["draft_answer"])