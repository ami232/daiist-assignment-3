"""
Assignment 3: the agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the tools of server.py over MCP and
AGENTS.md as system prompt.

Guardrails
- Approval: HumanInTheLoopMiddleware pauses before every add_document call;
  the harness asks a person (y/N on the terminal; refused when nobody can answer).
- Call limits: at most 4 search calls, 1 add_document and 8 model calls per question.
- Citation check (my extra guardrail): every [label] in the answer must be a
  label the search tool actually returned in this run, and a non-refusal answer
  must cite at least once. If not, the model gets one chance to fix it; if it
  still fails, the answer is replaced by a refusal instead of shown to the user.
  A paragraph-level citation ("Article 11(1)", "Article 8, paragraph 2") counts
  as the retrieved article ("Article 11"); the act and article number must match.
- Number check (flag only): every number with a unit in the answer ("3 mg",
  "15 %") must appear in the passages retrieved in this run. Numbers that do not
  are listed in `unsupported_numbers` and in the guardrail events, for the
  human reviewer. It does not trigger a repair: a correct calculation (e.g.
  15 % of 80 mg = 12 mg) is also flagged, and a person should look at it.

`ask(question)` returns the answer, the tool trace, tokens and seconds for evaluate.py.
"""

from __future__ import annotations

import asyncio
import os
import re
import sys
import time
import uuid
from pathlib import Path
from typing import Callable

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
CHAT_MODEL = os.environ.get("CHAT_MODEL", "gemini-flash-lite-latest")
REFUSAL = "The corpus does not cover this."
CITATION = re.compile(r"\[((?:Reg|Dir) [^\[\]]+?)\]")
LABEL_LINE = re.compile(r"^\[((?:Reg|Dir|[^\]\n]+?), [^\]\n]+)\]$", re.M)


# ----------------------------------------------------------------------------- citations

def _expand(location: str) -> set[str]:
    """'Annex (A; B)' -> {Annex (A), Annex (B)}; 'Recitals 3-5' -> {Recital 3..5}."""
    loc = location.strip()
    out = {loc}
    if m := re.fullmatch(r"(Annex(?: [IVXLC]+)?) \((.+)\)", loc):
        out |= {f"{m.group(1)} ({x.strip()})" for x in m.group(2).split(";")}
    if m := re.fullmatch(r"Recitals (\d+)-(\d+)", loc):
        out |= {f"Recital {n}" for n in range(int(m.group(1)), int(m.group(2)) + 1)}
    if " - " in loc:
        out |= {p.strip() for p in loc.split(" - ")}
    return out


def split_label(label: str) -> tuple[str, str]:
    source, _, location = label.partition(", ")
    return source.strip(), location.strip()


PARAGRAPH = re.compile(r"^(Article \d+[a-z]?)(?:\(\d+[a-z]?\)(?:\([a-z]{1,4}\))*|,\s*paragraph\s+\d+(?:\([a-z]{1,4}\))*)$",
                       re.IGNORECASE)


def article_of(location: str) -> str:
    """'Article 11(1)' / 'Article 10(2)(a)' / 'Article 8, Paragraph 2' -> 'Article 11' etc.
    Anything else (e.g. 'Annex', 'Article 8(1), Article 8(2)(b)') is returned unchanged."""
    m = PARAGRAPH.match(location.strip())
    return m.group(1) if m else location.strip()


def citation_valid(cite: str, retrieved_labels: set[str]) -> bool:
    """A citation is valid if it names a passage that was retrieved in this run
    (exactly, or one part of a retrieved chunk that spans several sections).
    A paragraph of a retrieved article counts as that article; a label that is
    more general than what was retrieved ('Annex' when 'Annex (Magnesium)' was
    retrieved) does not."""
    if cite in retrieved_labels:
        return True
    src, loc = split_label(cite)
    loc = article_of(loc)
    for label in retrieved_labels:
        s, l = split_label(label)
        if s == src and (loc in _expand(l) or _expand(loc) & _expand(l) == _expand(loc)):
            return True
    return False


def is_refusal(answer: str) -> bool:
    return answer.strip().lower().startswith(REFUSAL.lower().rstrip("."))


def check_citations(answer: str, retrieved_labels: set[str]) -> tuple[list[str], list[str]]:
    cites = CITATION.findall(answer)
    bad = [c for c in cites if not citation_valid(c, retrieved_labels)]
    return cites, bad


NUMBER = re.compile(r"(?<![\w.,])(\d+(?:[.,]\d+)?)\s*(%|mg|µg|μg|g|kg|ml|mL|l|kcal|kJ|mm|cm²|cm2|cm 2|"
                    r"months?|years?|days?|weeks?|hours?|minutes?)(?![\w])")


def _norm_number(value: str, unit: str) -> str:
    unit = {"μg": "µg", "mL": "ml", "cm2": "cm²", "cm 2": "cm²"}.get(unit, unit)
    unit = re.sub(r"s$", "", unit) if unit.endswith(("months", "years", "days", "weeks", "hours", "minutes")) else unit
    return f"{value.replace(',', '.')} {unit}"


def numbers_in(text: str) -> set[str]:
    """Numbers with a unit, normalised: '1,2 mm' -> '1.2 mm', '250 mg' -> '250 mg'."""
    text = text.replace("\u00a0", " ")
    return {_norm_number(v, u) for v, u in NUMBER.findall(text)}


def _in_table(number: str, sentence: str, passages: str) -> bool:
    """Tables put the unit in the row label: 'Vitamin C (mg) | 80' supports '80 mg',
    but only if that row label ('Vitamin C') is named in the same sentence of the answer."""
    value, unit = number.split(" ", 1)
    units = {"µg": "[µμ]g", "ml": "m[lL]", "cm²": "cm(?:²|2| 2)"}.get(unit, re.escape(unit))
    val = re.escape(value).replace("\\.", "[.,]")
    pattern = rf"(?:^|\|)\s*([^|\n]{{2,60}}?)\s*\({units}[^)]*\)\s*\|\s*{val}(?![\d.,])"
    for m in re.finditer(pattern, passages.replace("\u00a0", " "), re.M):
        if m.group(1).strip().lower() in sentence.lower():
            return True
    return False


def check_numbers(answer: str, passages: str, question: str = "") -> list[str]:
    """Numbers (with unit) in the answer that are neither in the retrieved passages
    nor in the user's question. Text inside [citation labels] is ignored."""
    plain = CITATION.sub("", answer)
    known = numbers_in(passages) | numbers_in(question)
    missing = set()
    for sentence in re.split(r"(?<!\d)[.;](?!\d)|\n", plain):
        for n in numbers_in(sentence) - known:
            if not _in_table(n, sentence, passages):
                missing.add(n)
    return sorted(missing)


# ----------------------------------------------------------------------------- MCP tools -> LangChain

async def _mcp_tools(session, trace: list[dict]):
    from langchain_core.tools import StructuredTool
    from pydantic import create_model

    tools = []
    for t in (await session.list_tools()).tools:
        props = (t.input_schema or {}).get("properties", {})
        Args = create_model(f"{t.name}_args", **{p: (str, ...) for p in props})

        def make(name):
            async def call(**kwargs):
                print(f"  [tool] {name}({kwargs})", file=sys.stderr, flush=True)
                started = time.time()
                res = await session.call_tool(name, kwargs)
                text = "\n".join(getattr(c, "text", "") for c in res.content)
                trace.append({"tool": name, "args": kwargs, "output": text,
                              "labels": LABEL_LINE.findall(text) if name == "search" else [],
                              "seconds": round(time.time() - started, 2)})
                return text
            return call

        tools.append(StructuredTool.from_function(coroutine=make(t.name), name=t.name,
                                                  description=t.description or "", args_schema=Args))
    return tools


def cli_approver(name: str, args: dict) -> bool:
    """Ask the person at the terminal. No terminal (e.g. evaluation) = no approval."""
    if not sys.stdin.isatty():
        print(f"[approval] {name}({args}) refused: nobody to approve it.", file=sys.stderr)
        return False
    reply = input(f"\nThe agent wants to run {name} with {args}. Allow? [y/N] ").strip().lower()
    return reply in ("y", "yes")


# ----------------------------------------------------------------------------- the agent

def _text(message) -> str:
    content = message.content
    if isinstance(content, list):
        return "".join(p.get("text", "") if isinstance(p, dict) else str(p) for p in content).strip()
    return str(content).strip()


def candidate_models() -> list[str]:
    """CHAT_MODEL first, then other Flash models this key can use (newest first),
    so a busy (503) or retired (404) model does not stop the run."""
    names = [CHAT_MODEL]
    try:
        from index import genai_client

        found = []
        for m in genai_client().models.list():
            name = m.name.removeprefix("models/")
            actions = getattr(m, "supported_actions", None) or []
            if "flash" in name and "generateContent" in actions and not any(
                    x in name for x in ("image", "tts", "audio", "live", "embedding", "exp", "omni")):
                found.append(name)
        names += sorted(found, reverse=True)
    except Exception as e:  # noqa: BLE001
        print(f"  [agent] could not list models: {e}", file=sys.stderr)
    return list(dict.fromkeys(names))


async def ask_async(question: str, approver: Callable[[str, dict], bool] = cli_approver,
                    corpus_only: bool = False) -> dict:
    """Ask with CHAT_MODEL; on 'overloaded' (503/429) retry, then fall back to another model."""
    last = None
    for model_name in candidate_models()[:6]:
        for attempt in range(2):
            try:
                out = await _ask_once(question, approver, corpus_only, model_name)
                out["model"] = model_name
                return out
            except BaseException as e:  # noqa: BLE001 - ExceptionGroup from the MCP task group
                msg = repr(e)
                if isinstance(e, KeyboardInterrupt):
                    raise
                last = e
                short = re.sub(r"\s+", " ", re.findall(r"(\d{3} [A-Z_]+[^\n]{0,160})", msg)[-1]
                               if re.findall(r"\d{3} [A-Z_]+", msg) else msg[-200:])
                print(f"  [agent] error from {model_name}: {short}", file=sys.stderr, flush=True)
                busy = any(c in msg for c in ("500", "502", "503", "504", "UNAVAILABLE", "DEADLINE",
                                              "INTERNAL", "overloaded", "high demand"))
                no_model = any(c in msg for c in ("429", "RESOURCE_EXHAUSTED", "404", "NOT_FOUND"))
                if busy and attempt == 0:
                    print(f"  [agent] {model_name} is busy or slow, retrying in 20s...", file=sys.stderr, flush=True)
                    await asyncio.sleep(20)
                    continue
                if busy or no_model:
                    why = "no free quota" if "429" in msg else ("not available" if "404" in msg else "busy")
                    print(f"  [agent] {model_name}: {why}, trying another model...", file=sys.stderr, flush=True)
                    break
                raise
    raise RuntimeError(f"No Gemini model answered. Last error: {last!r}"[:2000])


async def _ask_once(question: str, approver, corpus_only: bool, model_name: str) -> dict:
    from langchain.agents import create_agent
    from langchain.agents.middleware import (HumanInTheLoopMiddleware, ModelCallLimitMiddleware,
                                             ToolCallLimitMiddleware)
    from langchain_google_genai import ChatGoogleGenerativeAI
    from langgraph.checkpoint.memory import InMemorySaver
    from langgraph.types import Command
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    load_api_key()
    started = time.time()
    env = {**os.environ, "CORPUS_ONLY": "1" if corpus_only else "0"}
    params = StdioServerParameters(command=sys.executable, args=[str(ROOT / "server.py")], cwd=str(ROOT), env=env)
    trace: list[dict] = []
    events: list[str] = []

    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await _mcp_tools(session, trace)
            model = ChatGoogleGenerativeAI(model=model_name, temperature=0, max_retries=2)
            print(f"  [agent] thinking with {model_name} (can take up to a minute)...", file=sys.stderr, flush=True)
            agent = create_agent(
                model, tools,
                system_prompt=(ROOT / "AGENTS.md").read_text(encoding="utf-8"),
                middleware=[
                    HumanInTheLoopMiddleware(interrupt_on={"add_document": True, "search": False}),
                    ToolCallLimitMiddleware(tool_name="search", run_limit=4),
                    ToolCallLimitMiddleware(tool_name="add_document", run_limit=1),
                    ModelCallLimitMiddleware(run_limit=8),
                ],
                checkpointer=InMemorySaver(),
            )
            config = {"configurable": {"thread_id": str(uuid.uuid4())}}

            async def run(payload):
                result = await agent.ainvoke(payload, config)
                while result.get("__interrupt__"):          # approval step
                    decisions = []
                    for req in result["__interrupt__"][0].value["action_requests"]:
                        ok = approver(req["name"], req["args"])
                        events.append(f"approval {req['name']}: {'approved' if ok else 'rejected'}")
                        decisions.append({"type": "approve"} if ok else
                                         {"type": "reject", "message": "The user did not approve adding this document."})
                    result = await agent.ainvoke(Command(resume={"decisions": decisions}), config)
                return result

            result = await run({"messages": [{"role": "user", "content": question}]})
            answer = _text(result["messages"][-1])

            # Citation guardrail: one repair attempt, then refuse.
            labels = {l for t in trace for l in t["labels"]}
            cites, bad = check_citations(answer, labels)
            needs_fix = bad or (not cites and not is_refusal(answer))
            if needs_fix:
                events.append(f"citation check failed: bad={bad} cited={len(cites)}")
                fix = ("Your answer failed the citation check: "
                       + (f"these citations were not returned by search: {bad}. " if bad else "")
                       + ("it has no citations. " if not cites else "")
                       + f"Valid labels are: {sorted(labels)}. Rewrite the answer citing only those labels, "
                         f"or start with '{REFUSAL}' if they do not answer the question.")
                result = await run({"messages": [{"role": "user", "content": fix}]})
                answer = _text(result["messages"][-1])
                labels = {l for t in trace for l in t["labels"]}
                cites, bad = check_citations(answer, labels)
                if bad or (not cites and not is_refusal(answer)):
                    events.append("citation check failed again: answer replaced by a refusal")
                    answer = (f"{REFUSAL} I could not produce an answer whose citations match the "
                              f"retrieved passages, so I am not giving one. Please check the legal text "
                              f"or ask a regulatory consultant.")
                    cites = []
                else:
                    events.append("citation check passed after repair")

            # Number check: flag numbers that are not in the retrieved passages (no repair).
            passages = "\n".join(t["output"] for t in trace if t["tool"] == "search")
            unsupported_numbers = check_numbers(answer, passages, question)
            if unsupported_numbers:
                events.append(f"number check: not in the retrieved passages: {unsupported_numbers}")

            usage = {"input": 0, "output": 0}
            for m in result["messages"]:
                u = getattr(m, "usage_metadata", None) or {}
                usage["input"] += u.get("input_tokens", 0)
                usage["output"] += u.get("output_tokens", 0)

    return {
        "question": question,
        "answer": answer,
        "citations": cites,
        "refusal": is_refusal(answer),
        "trace": trace,
        "retrieved_labels": sorted({l for t in trace for l in t["labels"]}),
        "guardrail_events": events,
        "unsupported_numbers": unsupported_numbers,
        "tokens_in": usage["input"],
        "tokens_out": usage["output"],
        "seconds": round(time.time() - started, 1),
    }


def ask(question: str, **kw) -> dict:
    return asyncio.run(ask_async(question, **kw))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit('usage: python agent.py "your question"')
    try:
        out = ask(" ".join(sys.argv[1:]))
    except RuntimeError as e:
        print(f"\nCould not get an answer from Gemini right now: {str(e)[:600]}", file=sys.stderr)
        print(f"Models tried: {candidate_models()[:6]}", file=sys.stderr)
        raise SystemExit(1)
    print(out["answer"])
    print("\nSources:")
    for c in dict.fromkeys(out["citations"]):
        print(f"  - {c}")
    if not out["citations"]:
        print("  (none)")
    for e in out["guardrail_events"]:
        print(f"[guardrail] {e}", file=sys.stderr)
    print(f"\n({out['tokens_in']}+{out['tokens_out']} tokens, {out['seconds']}s)", file=sys.stderr)
