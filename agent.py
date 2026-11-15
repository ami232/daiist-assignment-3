"""
Assignment 3: the Erasmus+ assistant (`main.py ask "question"` runs this file).

LangChain `create_agent` on Gemini, with AGENTS.md as the system prompt and
the tools of server.py over MCP (started as a subprocess, as an editor does).

Guardrails:
- approval: add_document only runs after a person types "y";
- call limits: at most MAX_TOOL_CALLS tool calls and MAX_MODEL_CALLS model
  calls per question;
- citation check (my extra guardrail): every "(Document, p. N)" or
  "(Document, "Section")" in the answer must match a passage that search
  actually returned for this question. Citations that don't match are listed
  and the answer is flagged as unreliable.

evaluate.py imports `answer_question()`, which returns the answer and the trace.
"""

from __future__ import annotations

import asyncio
import os
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path
from typing import Callable

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parent
SYSTEM_PROMPT = (ROOT / "AGENTS.md").read_text(encoding="utf-8")

# gemini-2.5-flash is no longer available to new keys. The preview model is the
# stronger one; the stable lite model takes over if it fails or is overloaded.
MODEL = os.environ.get("AGENT_MODEL", "gemini-3-flash-preview")
FALLBACK_MODEL = "gemini-3.1-flash-lite"
REQUEST_TIMEOUT = 60  # seconds per Gemini request; without it a stuck request waits forever
QUESTION_TIMEOUT = 180  # seconds for a whole question in answer_question()
MAX_TOOL_CALLS = 6
MAX_MODEL_CALLS = 10

# Names the answer uses in citations (AGENTS.md rule 4) -> source ids in the index.
CITATION_NAMES = {
    "programme guide": "programme_guide_2026",
    "eche": "eche_guidelines",
    "learning agreement": "learning_agreement_guidelines",
    "student charter": "student_charter",
}


# --------------------------------------------------------------------------- trace

@dataclass
class Passage:
    source: str
    title: str
    location: str
    url: str
    page: int = 0
    page_end: int = 0
    section: str = ""
    text: str = ""


@dataclass
class Trace:
    tool_calls: list[dict] = field(default_factory=list)
    passages: list[Passage] = field(default_factory=list)


DATE_SUFFIX = re.compile(r", (\d{4}-\d{2}(?:-\d{2})?(?: \(version \d+\))?|\d{1,2} \w+ \d{4})$")


def parse_search_result(text: str) -> list[Passage]:
    """Read the passages back out of server.py's search output.

    Each passage starts with
        [n] <title> — <location>[, <date>]
        source: <id> | url: <url> | relevance: <x>
    where <location> is "p. 54, SECTION", "pp. 69-70, SECTION" or a section path.
    """
    passages = []
    for block in text.split("\n\n---\n\n"):
        # Header and metadata are one line each ([^\n]+); everything after is the
        # passage text. (A greedy ".+" here once swallowed the text into the
        # metadata line, so every passage was saved with an empty text.)
        m = re.match(r"^\[\d+\] ([^\n]+)\nsource: ([^\n]+)\n?(.*)$", block.strip(), re.S)
        if not m:
            continue
        header, meta, body = m.groups()
        title, _, location = header.partition(" — ")
        location = DATE_SUFFIX.sub("", location)
        fields = dict(part.split(": ", 1) for part in ("source: " + meta).split(" | ") if ": " in part)
        p = Passage(source=fields.get("source", ""), title=title, location=location,
                    url=fields.get("url", ""), text=body.strip())
        m = re.match(r"pp?\. (\d+)(?:-(\d+))?(?:, (.*))?$", location)
        if m:
            p.page = int(m.group(1)); p.page_end = int(m.group(2) or m.group(1)); p.section = m.group(3) or ""
        else:
            p.section = location
        passages.append(p)
    return passages


# --------------------------------------------------------------------------- citation check (extra guardrail)

CITATION = re.compile(r"\(([^()]*?(?:Programme Guide|ECHE|Learning Agreement|Student Charter)[^()]*)\)", re.I)


def cited_pages(text: str) -> list[int]:
    """Pages in "p. 54", "pp. 67-68", "pp. 67-69 y 72", "p. 8 and 43".
    Footnote numbers ("p. 54, Note 67") are not pages and are ignored."""
    text = re.sub(r"\b(?:Notes?|Nota|footnote)\s*\d+(?:\s*(?:,|and|y|&)\s*\d+)*", "", text, flags=re.I)
    m = re.search(r"\bpp?\.\s*(.+)$", text)
    if not m:
        return []
    pages = []
    for a, b in re.findall(r"(\d+)(?:\s*[-–]\s*(\d+))?", m.group(1)):
        a, b = int(a), int(b or a)
        pages.extend(range(a, b + 1) if b - a <= 20 else [a, b])
    return pages


def check_citations(answer: str, passages: list[Passage]) -> dict:
    """Compare every citation in the answer with the passages search returned."""
    # One bracket can hold several citations separated by ";":
    # (Programme Guide 2026, p. 54; Learning Agreement guidelines, "Duration").
    # Each part is checked against its own document; a part without a document
    # name ("p. 54; p. 55") belongs to the previous one.
    parts, previous = [], None
    for bracket in CITATION.findall(answer):
        for part in (p.strip() for p in bracket.split(";") if p.strip()):
            lowered = part.lower()
            source = next((sid for name, sid in CITATION_NAMES.items() if name in lowered), previous)
            parts.append((part, source))
            previous = source

    checked, unsupported = [], []
    for raw, source in parts:
        retrieved = [p for p in passages if p.source == source]
        pages = cited_pages(raw)
        quoted = re.findall(r"[\"“”']([^\"“”']{3,})[\"“”']", raw)
        problems = []
        if not retrieved:
            problems.append("no passage from this document was retrieved")
        else:
            for page in pages:
                if not any(p.page and p.page <= page <= p.page_end for p in retrieved):
                    problems.append(f"p. {page} was not retrieved")
            for section in quoted:
                s = section.lower().strip()
                if not any(s in p.section.lower() or (p.section and p.section.lower().split(" > ")[-1] in s)
                           for p in retrieved):
                    problems.append(f'section "{section}" was not retrieved')
        checked.append(raw)
        if problems:
            unsupported.append({"citation": raw, "problems": problems})

    gives_facts = bool(re.search(r"\d", answer))
    refuses = bool(re.search(r"not (?:covered|in the documents)|don't|do not (?:contain|cover|include)|no (?:contienen|incluyen|dicen)|no está|pregunt|ask your", answer, re.I))
    no_citations = not checked and gives_facts and not refuses
    return {
        "citations": checked,
        "unsupported": unsupported,
        "no_citations": no_citations,
        "fired": bool(unsupported) or no_citations,
    }


def guardrail_note(check: dict) -> str:
    if not check["fired"]:
        return ""
    lines = ["⚠️ Citation check: this answer may not be reliable."]
    for item in check["unsupported"]:
        lines.append(f"  - ({item['citation']}): {'; '.join(item['problems'])}")
    if check["no_citations"]:
        lines.append("  - The answer gives facts but cites no document.")
    lines.append("Check these points in the original documents before relying on them.")
    return "\n".join(lines)


# --------------------------------------------------------------------------- approval

def ask_in_terminal(path: str) -> bool:
    if not sys.stdin.isatty():
        print(f"add_document({path!r}) needs approval, but nobody can answer here: refused.", file=sys.stderr)
        return False
    reply = input(f"\nThe assistant wants to add this document to the index:\n  {path}\nAllow? [y/N] ")
    return reply.strip().lower() in {"y", "yes", "s", "si", "sí"}


# --------------------------------------------------------------------------- agent

def content_text(content) -> str:
    """Gemini may return a list of parts; keep the text."""
    if isinstance(content, str):
        return content
    return "".join(part.get("text", "") if isinstance(part, dict) else str(part) for part in content)


def mcp_tools(session: ClientSession, tools, trace: Trace, approve: Callable[[str], bool]):
    """Wrap the server's MCP tools as LangChain tools, recording every call."""
    from langchain_core.tools import StructuredTool

    def make(tool):
        async def call(**kwargs) -> str:
            if tool.name == "add_document":
                if not approve(kwargs.get("path", "")):
                    trace.tool_calls.append({"tool": tool.name, "args": kwargs, "approved": False})
                    return "The user did not approve adding this document. Nothing was added."
            result = await session.call_tool(tool.name, kwargs)
            text = "\n".join(getattr(c, "text", "") for c in result.content)
            trace.tool_calls.append({"tool": tool.name, "args": kwargs, "result_chars": len(text)})
            if tool.name == "search":
                trace.passages.extend(parse_search_result(text))
            return text

        return StructuredTool.from_function(coroutine=call, name=tool.name,
                                            description=tool.description or "", args_schema=tool.input_schema)

    return [make(t) for t in tools]


async def run(question: str, approve: Callable[[str], bool] = ask_in_terminal) -> dict:
    from langchain.agents import create_agent
    from langchain.agents.middleware import ModelCallLimitMiddleware, ModelFallbackMiddleware, ToolCallLimitMiddleware
    from langchain_google_genai import ChatGoogleGenerativeAI

    from api_key import load_api_key

    load_api_key()
    trace = Trace()
    started = time.time()
    params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT))
    errlog = sys.stderr if os.environ.get("AGENT_DEBUG") else open(os.devnull, "w")
    async with stdio_client(params, errlog=errlog) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = mcp_tools(session, (await session.list_tools()).tools, trace, approve)
            agent = create_agent(
                ChatGoogleGenerativeAI(model=MODEL, temperature=0, max_retries=3, timeout=REQUEST_TIMEOUT),
                tools,
                system_prompt=SYSTEM_PROMPT,
                middleware=[
                    ToolCallLimitMiddleware(run_limit=MAX_TOOL_CALLS, exit_behavior="continue"),
                    ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS, exit_behavior="end"),
                    ModelFallbackMiddleware(ChatGoogleGenerativeAI(model=FALLBACK_MODEL, temperature=0, max_retries=3,
                                                                   timeout=REQUEST_TIMEOUT)),
                ],
            )
            result = await agent.ainvoke({"messages": [{"role": "user", "content": question}]})

    answer = content_text(result["messages"][-1].content).strip()
    check = check_citations(answer, trace.passages)
    ai_messages = [m for m in result["messages"] if m.type == "ai"]
    usage = [getattr(m, "usage_metadata", None) or {} for m in ai_messages]
    return {
        "question": question,
        "answer": answer,
        "citation_check": check,
        "tool_calls": trace.tool_calls,
        "passages": [p.__dict__ for p in trace.passages],
        "model_calls": len(ai_messages),
        "input_tokens": sum(u.get("input_tokens", 0) for u in usage),
        "output_tokens": sum(u.get("output_tokens", 0) for u in usage),
        "seconds": round(time.time() - started, 1),
    }


def answer_question(question: str, approve: Callable[[str], bool] = lambda path: False) -> dict:
    """For evaluate.py: answer one question; add_document is refused by default.
    Raises TimeoutError if the whole question takes longer than QUESTION_TIMEOUT."""
    return asyncio.run(asyncio.wait_for(run(question, approve), QUESTION_TIMEOUT))


def print_result(result: dict) -> None:
    print(result["answer"])
    note = guardrail_note(result["citation_check"])
    if note:
        print("\n" + note)
    # List the documents the answer relied on, with links.
    used = {}
    for p in result["passages"]:
        used.setdefault(p["url"], p["title"])
    if used:
        print("\nSources searched:")
        for url, title in used.items():
            print(f"  - {title}: {url}")
    searches = [c["args"].get("query") for c in result["tool_calls"] if c["tool"] == "search"]
    print(f"\n({len(searches)} search(es): {'; '.join(map(str, searches))})")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit('Usage: uv run python agent.py "your question"')
    print_result(asyncio.run(run(" ".join(sys.argv[1:]))))
