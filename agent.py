"""
Assignment 3: the drone-rules agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with server.py's tools over MCP and
AGENTS.md as system prompt.

Guardrails
  1. Approval: add_document never runs without a human "yes" (HumanInTheLoop
     middleware). With no terminal to ask (evaluation, CI) it is rejected.
  2. Call limits: at most MAX_TOOL_CALLS tool calls and MAX_MODEL_CALLS model
     calls per question.
  3. Citation check (our extra guardrail): every [source | location] in the
     answer must be one of the passages search returned in this run, and an
     answer that is not a refusal must cite at least once. On failure the agent
     gets one chance to fix it; if it still fails, the answer is withheld and
     replaced by a refusal that lists what was retrieved.

`answer(question)` returns the answer plus a trace (tool calls, retrieved
citations, tokens, seconds, guardrail events) for evaluate.py.
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
# Free tier: gemini-3.8-flash allows only 20 requests/day (one evaluation needs ~130), and the
# flash models often answer 503 "high demand" (one took 113 s to do so). The flash-lite models
# answer in ~1 s and have their own quotas, so we use them, falling back in this order.
MODEL = "gemini-3.5-flash-lite"
FALLBACK_MODELS = ("gemini-flash-lite-latest", "gemini-3.1-flash-lite")
MODEL_TIMEOUT = 60
RUN_BUDGET_SECONDS = 240  # check.py allows 300 s for `main.py ask`


def chat_model(name: str, retries: int = 1, timeout: int = MODEL_TIMEOUT):
    from langchain_google_genai import ChatGoogleGenerativeAI

    return ChatGoogleGenerativeAI(model=name, temperature=0, max_retries=retries, timeout=timeout)


MAX_TOOL_CALLS = 6
MAX_MODEL_CALLS = 8
REFUSAL = "The corpus does not cover this"

CITATION = re.compile(r"\[([a-z0-9][a-z0-9\-]*)\s*\|\s*([^\]\n]+?)\s*\]")
RETRIEVED = re.compile(r"^Citation: \[(.+?) \| (.+)\]\s*$", re.MULTILINE)


def system_prompt() -> str:
    """AGENTS.md, plus today's date so rule 9 (expired transitional provisions) can be applied."""
    from datetime import date

    return (ROOT / "AGENTS.md").read_text(encoding="utf-8") + f"\n\nToday's date: {date.today().isoformat()}.\n"


_QUOTES = str.maketrans({"‘": "'", "’": "'", "“": '"', "”": '"', "–": "-", "—": "-"})


def _norm(s: str) -> str:
    """Compare citations ignoring case, spacing and curly vs straight quotes/dashes."""
    return re.sub(r"\s+", " ", s.replace("\xa0", " ").translate(_QUOTES)).strip().lower()


def is_refusal(text: str) -> bool:
    """A refusal starts with "The corpus does not cover" (rule 4), ignoring markdown such as **.
    (An exact-sentence match missed "The corpus does not cover the specific SORA tables…".)"""
    return re.sub(r"^[^a-z0-9]+", "", _norm(text)).startswith("the corpus does not cover")


_BRACKET = re.compile(r"\[([^\[\]\n]*\|[^\[\]\n]*)\]")
_NEXT_SOURCE = re.compile(r"\s*[;,]\s*(?=[a-z0-9][a-z0-9\-]*\s*\|)")


def parse_citations(answer: str) -> list[list[tuple[str, str]]]:
    """Citations in the answer. Each bracket may hold several, as the model sometimes writes
    "[a | X; b | Y]"; returns one list of (source, location) per citation in the bracket."""
    out = []
    for inner in _BRACKET.findall(answer):
        for part in _NEXT_SOURCE.split(inner.strip()):
            source, _, location = part.partition("|")
            if source.strip() and location.strip():
                out.append((source.strip(), location.strip()))
    return out


def check_citations(answer: str, retrieved: set[tuple[str, str]]) -> list[str]:
    """Problems with the answer's citations; empty list means it passes."""
    cited = parse_citations(answer)
    valid = [(_norm(s), _norm(l)) for s, l in retrieved]

    def found_one(s: str, l: str) -> bool:
        # Exact heading, or the heading's leading rule ID ("UAS.OPEN.010" for
        # "UAS.OPEN.010 General provisions"). An invented sub-point such as
        # "Article 4(1)(c)" matches no retrieved heading and is rejected.
        return any(s == vs and (l == vl or (vl.startswith(l) and not vl[len(l)].isalnum() and vl[len(l)] != "("))
                   for vs, vl in valid)

    def found(source: str, location: str) -> bool:
        s, l = _norm(source), _norm(location)
        if found_one(s, l):
            return True
        # Several locations of one source: "Article 4 and UAS.OPEN.010", "AMC1 X, GM1 Y".
        # Headings themselves contain commas and "and", so find any cut of the text at
        # separators into consecutive pieces that are each a retrieved heading.
        parts = re.split(r"(\s*(?:,|;| and )\s*)", l)  # odd indexes are the separators
        words, seps = parts[0::2], parts[1::2]

        def can(i: int) -> bool:
            if i == len(words):
                return True
            return any(found_one(s, "".join(w + (seps[k] if k < j - 1 else "") for k, w in enumerate(words[i:j], start=i)))
                       and can(j) for j in range(i + 1, len(words) + 1))

        return len(words) > 1 and can(0)

    problems = list(dict.fromkeys(f"[{s} | {l}] is not one of the passages you retrieved"
                                  for s, l in cited if not found(s, l)))
    if not cited and not is_refusal(answer):
        problems.append("the answer makes claims but cites nothing")
    return problems


def _approve_in_terminal(tool_name: str, args: dict) -> bool:
    if not sys.stdin or not sys.stdin.isatty():
        print(f"[approval] {tool_name}({args}) needs approval but there is no terminal: rejected.", file=sys.stderr)
        return False
    try:
        reply = input(f"\nThe agent wants to run {tool_name} with {args}.\nThis embeds and stores a document in the index. Approve? [y/N] ")
    except (EOFError, OSError):
        # Fail closed. (On Windows the NUL device claims to be a terminal, so isatty() is not enough.)
        print(f"[approval] could not read an answer for {tool_name}: rejected.", file=sys.stderr)
        return False
    return reply.strip().lower() in ("y", "yes")


def mcp_tools_as_langchain(session) -> "list":
    """Wrap each MCP tool of an open session as a LangChain tool (name, description, schema from the server)."""
    from langchain_core.tools import StructuredTool

    async def build():
        tools = []
        for t in (await session.list_tools()).tools:
            async def call(_name=t.name, **kwargs):
                result = await session.call_tool(_name, kwargs)
                return "\n".join(getattr(c, "text", "") for c in result.content)
            tools.append(StructuredTool(name=t.name, description=t.description or "", args_schema=t.input_schema,
                                        coroutine=call))
        return tools
    return build()


# National-zones note (fix for v1's main failure: the model wrote this caveat from memory, without
# retrieving Article 15, in 11 of 32 answers). The harness retrieves Article 15 itself and appends a
# fixed note quoting it, so the caveat is always present, identical and supported.
ZONES_QUERY = "Article 15 Operational conditions for UAS geographical zones"
ZONES_SOURCE, ZONES_HEADING = "reg-2019-947", "Article 15 - Operational conditions for UAS geographical zones"
ZONES_QUOTES = ("prohibit certain or all UAS operations, request particular conditions for certain or all UAS "
                "operations or require a prior flight authorisation for certain or all UAS operations",
                "is made publicly available in a common unique digital format")


async def fetch_zones_passage(session) -> str | None:
    """Article 15's search result block, via the search tool; None if it can't be retrieved verbatim."""
    result = await session.call_tool("search", {"query": ZONES_QUERY})
    text = "\n".join(getattr(c, "text", "") for c in result.content)
    for block in text.split("### Result")[1:]:
        if f"Citation: [{ZONES_SOURCE} | {ZONES_HEADING}]" in block and all(q in _norm_ws(block) for q in ZONES_QUOTES):
            return "### Result" + block
    return None


def _norm_ws(s: str) -> str:
    return re.sub(r"\s+", " ", s)


def zones_note() -> str:
    cite = f"[{ZONES_SOURCE} | {ZONES_HEADING}]"
    return (f"\n\n**Check local zones before flying.** In UAS geographical zones, Member States may "
            f"\"{ZONES_QUOTES[0]}\" {cite}. Information on these zones \"{ZONES_QUOTES[1]}\" {cite}; "
            f"check it for the place where you plan to fly.")


async def answer_async(question: str, approve=_approve_in_terminal, verbose: bool = False) -> dict:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    load_api_key()
    # The MCP client passes only a few safe variables to the server by default; pass ours
    # (CORPUS_BASE_ONLY from evaluate.py, and GEMINI_API_KEY on CI where there is no .env).
    params = StdioServerParameters(command=sys.executable, args=[str(ROOT / "server.py")], cwd=str(ROOT),
                                   env=dict(os.environ))
    started, attempt = time.time(), 0
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await mcp_tools_as_langchain(session)
            zones = await fetch_zones_passage(session)
            while True:  # every model busy (503/504/429) or network blip: back off and retry the question
                attempt += 1
                try:
                    trace = await _answer_with_tools(question, tools, approve, verbose, zones)
                    trace["attempts"] = attempt
                    trace["seconds"] = round(time.time() - started, 2)
                    return trace
                except Exception as error:  # noqa: BLE001 - classified below
                    transient = any(s in str(error) for s in ("503", "504", "429", "UNAVAILABLE", "DEADLINE",
                                                              "RESOURCE_EXHAUSTED", "getaddrinfo", "Cannot connect"))
                    wait = 15 * attempt
                    if not transient or time.time() - started + wait > RUN_BUDGET_SECONDS:
                        raise
                    print(f"  [retry] all models failed ({str(error)[:80]}...); retrying in {wait}s", file=sys.stderr)
                    await asyncio.sleep(wait)


async def _answer_with_tools(question: str, tools: list, approve, verbose: bool, zones: str | None = None) -> dict:
    from langchain.agents import create_agent
    from langchain.agents.middleware import (HumanInTheLoopMiddleware, ModelCallLimitMiddleware, ModelFallbackMiddleware,
                                             ToolCallLimitMiddleware)
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langgraph.checkpoint.memory import InMemorySaver
    from langgraph.types import Command

    started = time.time()

    agent = create_agent(
        # Fail fast to the fallback when overloaded.
        model=chat_model(MODEL, retries=0, timeout=30),
        tools=tools,
        system_prompt=system_prompt(),
        middleware=[
            # 503 "high demand" on the free tier: fall back to sibling models instead of failing.
            ModelFallbackMiddleware(*(chat_model(m, retries=2) for m in FALLBACK_MODELS)),
            HumanInTheLoopMiddleware(interrupt_on={"add_document": {"allowed_decisions": ["approve", "reject"]}}),
            ToolCallLimitMiddleware(run_limit=MAX_TOOL_CALLS, exit_behavior="end"),
            ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS, exit_behavior="end"),
        ],
        checkpointer=InMemorySaver(),
    )
    config = {"configurable": {"thread_id": str(uuid.uuid4())}, "recursion_limit": 40}
    events: list[str] = []

    async def run(payload):
        result = await agent.ainvoke(payload, config)
        while result.get("__interrupt__"):  # approval gate for add_document
            decisions = []
            for request in result["__interrupt__"][0].value["action_requests"]:
                ok = approve(request["name"], request["args"])
                events.append(f"approval {'granted' if ok else 'denied'} for {request['name']}({request['args']})")
                decisions.append({"type": "approve"} if ok else
                                 {"type": "reject", "message": "The user did not approve adding this document."})
            result = await agent.ainvoke(Command(resume={"decisions": decisions}), config)
        return result

    result = await run({"messages": [{"role": "user", "content": question}]})
    final = _final_text(result["messages"])
    retrieved = _retrieved(result["messages"])
    # The citation check is for answers about the rules; a turn that only managed the index
    # (add_document, no search) reports what the tool did and has nothing to cite.
    names = {tc["name"] for m in result["messages"] for tc in (getattr(m, "tool_calls", None) or [])}
    index_only = "add_document" in names and "search" not in names
    problems = [] if index_only else check_citations(final, retrieved)
    if problems:
        events.append("citation check failed: " + "; ".join(problems))
        result = await run({"messages": [{"role": "user", "content":
            "Your answer failed the citation check: " + "; ".join(problems) +
            ". Rewrite it citing only passages exactly as they appear in your search results "
            f"(search again if needed), or say '{REFUSAL}.'"}]})
        final = _final_text(result["messages"])
        retrieved = _retrieved(result["messages"])
        problems = check_citations(final, retrieved)
        if problems:
            events.append("citation check failed again: answer withheld")
            listed = "\n".join(f"- [{s} | {l}]" for s, l in sorted(retrieved)) or "- (nothing retrieved)"
            final = (f"{REFUSAL} in a way I could verify, so I am not giving an answer. "
                     f"Passages I looked at:\n{listed}\nCheck them yourself or ask your national aviation authority.")
        else:
            events.append("citation check passed after one retry")

    extra_evidence = []
    if not index_only and not is_refusal(final):
        if zones:
            final += zones_note()
            retrieved.add((ZONES_SOURCE, ZONES_HEADING))
            extra_evidence.append(zones)
            events.append("national-zones note added (Article 15)")
        else:
            events.append("national-zones note skipped: Article 15 could not be retrieved")

    messages = result["messages"]
    tool_calls = [{"name": tc["name"], "args": tc["args"]} for m in messages for tc in (getattr(m, "tool_calls", None) or [])]
    usage = [m.usage_metadata for m in messages if getattr(m, "usage_metadata", None)]
    trace = {
        "question": question,
        "answer": final,
        "tool_calls": tool_calls,
        "retrieved": sorted(retrieved),
        "retrieved_text": [m.content if isinstance(m.content, str) else str(m.content)
                           for m in messages if getattr(m, "type", "") == "tool"] + extra_evidence,
        "refused": is_refusal(final),
        "models": sorted({(getattr(m, "response_metadata", None) or {}).get("model_name", "?")
                          for m in messages if getattr(m, "type", "") == "ai"}),
        "guardrail_events": events,
        "input_tokens": sum(u.get("input_tokens", 0) for u in usage),
        "output_tokens": sum(u.get("output_tokens", 0) for u in usage),
        "seconds": round(time.time() - started, 2),
    }
    if verbose:
        for tc in tool_calls:
            print(f"  -> {tc['name']}({tc['args']})", file=sys.stderr)
        for e in events:
            print(f"  [guardrail] {e}", file=sys.stderr)
    return trace


def _final_text(messages) -> str:
    for m in reversed(messages):
        if getattr(m, "type", "") == "ai":
            text = m.text if isinstance(getattr(m, "text", None), str) else m.content
            if isinstance(text, list):
                text = "".join(p.get("text", "") if isinstance(p, dict) else str(p) for p in text)
            if text and text.strip():
                return text.strip()
    return f"{REFUSAL}: I could not produce an answer within the call limits."


def _retrieved(messages) -> set[tuple[str, str]]:
    found = set()
    for m in messages:
        if getattr(m, "type", "") == "tool":
            content = m.content if isinstance(m.content, str) else " ".join(
                p.get("text", "") if isinstance(p, dict) else str(p) for p in m.content)
            found.update((s.strip(), l.strip()) for s, l in RETRIEVED.findall(content))
    return found


def answer(question: str, **kwargs) -> dict:
    return asyncio.run(answer_async(question, **kwargs))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit('usage: python agent.py "your question"')
    trace = answer(" ".join(sys.argv[1:]), verbose=True)
    print(trace["answer"])
    print(f"\n(model {', '.join(trace['models'])}; {len(trace['tool_calls'])} tool calls,{trace['input_tokens']}+{trace['output_tokens']} tokens, {trace['seconds']}s)")
