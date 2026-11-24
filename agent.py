"""LangChain harness for the FAA Part 107 RAG assistant.

`uv run python main.py ask "question"` starts this script. It uses LangChain's
`create_agent`, but its tools are thin wrappers around server.py over MCP stdio.
The add-document wrapper requires explicit terminal approval before the MCP tool
is allowed to run. A tool-call budget and citation-integrity post-check provide
additional guardrails.
"""

from __future__ import annotations

import asyncio
import os
import re
import sys
import time
from pathlib import Path
from typing import Any

from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
SERVER = ROOT / "server.py"
AGENT_RULES = ROOT / "AGENTS.md"
CHAT_MODEL = os.getenv("GEMINI_CHAT_MODEL", "gemini-3.5-flash-lite")
MAX_TOOL_CALLS = int(os.getenv("AGENT_MAX_TOOL_CALLS", "5"))
CITATION_RE = re.compile(r"\[FAA:[^\]]+\]")
REFUSAL_PHRASE = "I don't know from the indexed FAA corpus."

_TRACE: list[dict[str, Any]] = []
_TOOL_CALLS = 0
_ALLOW_ADD = False


def _reset_run(*, allow_add: bool) -> None:
    global _TRACE, _TOOL_CALLS, _ALLOW_ADD
    _TRACE = []
    _TOOL_CALLS = 0
    _ALLOW_ADD = allow_add


def _explicit_add_request(question: str) -> bool:
    q = question.lower()
    return bool(
        re.search(r"\b(add|index|ingest|import)\b", q)
        and re.search(r"\b(document|file|pdf|markdown|html|txt)\b", q)
    )


def _consume_budget(tool_name: str) -> str | None:
    global _TOOL_CALLS
    _TOOL_CALLS += 1
    if _TOOL_CALLS > MAX_TOOL_CALLS:
        return (
            f"TOOL_CALL_LIMIT: run limit of {MAX_TOOL_CALLS} tool calls reached. "
            "Stop searching and answer only from evidence already retrieved; otherwise refuse."
        )
    return None


async def _mcp_call(argument_name: str, value: str) -> tuple[str, str]:
    """Start server.py over stdio, locate a tool by required argument, call it."""
    params = StdioServerParameters(command=sys.executable, args=[str(SERVER)], cwd=str(ROOT))
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = (await session.list_tools()).tools
            selected = None
            for candidate in tools:
                schema = candidate.input_schema or {}
                props = schema.get("properties", {})
                if argument_name in schema.get("required", []) and props.get(argument_name, {}).get("type") == "string":
                    selected = candidate
                    break
            if selected is None:
                names = ", ".join(t.name for t in tools)
                raise RuntimeError(f"No MCP tool with required string argument {argument_name!r}. Tools: {names}")
            result = await session.call_tool(selected.name, {argument_name: value})
            text = "\n".join(getattr(part, "text", "") for part in result.content).strip()
            if getattr(result, "is_error", False) or getattr(result, "isError", False):
                raise RuntimeError(text or f"MCP tool {selected.name} failed")
            return selected.name, text


def _call_mcp(argument_name: str, value: str) -> tuple[str, str]:
    return asyncio.run(_mcp_call(argument_name, value))


@tool
def search(query: str) -> str:
    """Search the official indexed FAA small-UAS corpus and return citable passages."""
    limited = _consume_budget("search")
    if limited:
        _TRACE.append({"tool": "search", "args": {"query": query}, "result": limited})
        return limited
    try:
        name, result = _call_mcp("query", query)
    except Exception as exc:
        result = f"ERROR: {type(exc).__name__}: {exc}"
        name = "search"
    _TRACE.append({"tool": name, "args": {"query": query}, "result": result})
    return result


@tool
def add_document(path: str) -> str:
    """Add one local document to the index, only after explicit user approval."""
    limited = _consume_budget("add_document")
    if limited:
        _TRACE.append({"tool": "add_document", "args": {"path": path}, "result": limited})
        return limited

    if not _ALLOW_ADD:
        result = (
            "ADD_DOCUMENT_BLOCKED: the user did not explicitly ask to add/index a document "
            "in this request. Do not call this tool again."
        )
        _TRACE.append({"tool": "add_document", "args": {"path": path}, "result": result})
        return result

    if not sys.stdin.isatty():
        result = "ADD_DOCUMENT_BLOCKED: interactive human approval is required before this tool can run."
        _TRACE.append({"tool": "add_document", "args": {"path": path}, "result": result})
        return result

    print(f"\nAgent wants to add this document to the corpus:\n  {path}", file=sys.stderr)
    decision = input("Approve add_document? [y/N]: ").strip().lower()
    if decision not in {"y", "yes"}:
        result = "ADD_DOCUMENT_REJECTED: user did not approve the index change."
        _TRACE.append({"tool": "add_document", "args": {"path": path}, "result": result})
        return result

    try:
        name, result = _call_mcp("path", path)
    except Exception as exc:
        result = f"ERROR: {type(exc).__name__}: {exc}"
        name = "add_document"
    _TRACE.append({"tool": name, "args": {"path": path}, "result": result})
    return result


def _message_text(message: Any) -> str:
    content = getattr(message, "content", "")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        parts: list[str] = []
        for item in content:
            if isinstance(item, str):
                parts.append(item)
            elif isinstance(item, dict) and isinstance(item.get("text"), str):
                parts.append(item["text"])
        return "\n".join(parts).strip()
    text = getattr(message, "text", "")
    return text if isinstance(text, str) else str(text or "")


def _usage(messages: list[Any]) -> dict[str, int]:
    totals = {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}
    for message in messages:
        usage = getattr(message, "usage_metadata", None)
        if isinstance(usage, dict):
            totals["input_tokens"] += int(usage.get("input_tokens") or 0)
            totals["output_tokens"] += int(usage.get("output_tokens") or 0)
            totals["total_tokens"] += int(usage.get("total_tokens") or 0)
    if totals["total_tokens"] == 0:
        totals["total_tokens"] = totals["input_tokens"] + totals["output_tokens"]
    return totals


def _citation_parts(label: str) -> tuple[str, int | None]:
    """Return a tolerant (source, page) key for an FAA citation.

    The model sometimes writes the same citation as `PDF page 267`, `page 267`,
    or `p. 267`. Those are formatting differences, not invented evidence.
    """
    inner = label.strip()[1:-1].strip()
    if inner.lower().startswith("faa:"):
        inner = inner[4:]
    source, _, location = inner.partition("|")
    source_key = re.sub(r"[^a-z0-9]+", "", source.lower())
    nums = re.findall(r"\d+", location)
    page = int(nums[-1]) if nums else None
    return source_key, page


def _citation_matches(used: str, allowed: str) -> bool:
    used_source, used_page = _citation_parts(used)
    allowed_source, allowed_page = _citation_parts(allowed)
    source_ok = (
        used_source == allowed_source
        or (used_source and allowed_source and (used_source in allowed_source or allowed_source in used_source))
    )
    page_ok = used_page == allowed_page if (used_page is not None or allowed_page is not None) else True
    return source_ok and page_ok


def _citation_guardrail(answer: str, trace: list[dict[str, Any]]) -> tuple[str, dict[str, Any]]:
    """Reject unsupported citations while tolerating harmless citation formatting differences."""
    evidence_text = "\n".join(
        item["result"] for item in trace if "query" in item.get("args", {}) and isinstance(item.get("result"), str)
    )
    allowed_raw = set(CITATION_RE.findall(evidence_text))
    used_raw = set(CITATION_RE.findall(answer))
    invalid = sorted(
        used for used in used_raw
        if not any(_citation_matches(used, allowed) for allowed in allowed_raw)
    )
    refused = REFUSAL_PHRASE.lower() in answer.lower() or answer.lower().startswith("i don't know")

    guardrail = {
        "allowed_citations": sorted(allowed_raw),
        "used_citations": sorted(used_raw),
        "invalid_citations": invalid,
        "fired": False,
        "reason": "",
    }
    if invalid:
        guardrail["fired"] = True
        guardrail["reason"] = "final answer contained citation labels not returned by search"
    elif not used_raw and not refused:
        guardrail["fired"] = True
        guardrail["reason"] = "factual answer contained no corpus citation"

    if guardrail["fired"]:
        replacement = (
            f"{REFUSAL_PHRASE} The draft answer failed the citation-integrity guardrail "
            f"({guardrail['reason']})."
        )
        return replacement, guardrail
    return answer, guardrail


def answer_question(question: str, *, allow_add: bool | None = None) -> dict[str, Any]:
    """Run the LangChain agent and return answer, tool trace, usage and timing."""
    question = question.strip()
    if not question:
        raise ValueError("Question must not be empty")
    if allow_add is None:
        allow_add = _explicit_add_request(question)
    _reset_run(allow_add=allow_add)

    rules = AGENT_RULES.read_text(encoding="utf-8")
    system_prompt = (
        rules
        + "\n\nOperational instruction: For any factual corpus question, call search before answering. "
        + "Copy the exact short [FAA:source|location] labels from search results as inline citations. "
        + "If one search is insufficient, you may reformulate and search again within the tool-call limit."
    )
    model = ChatGoogleGenerativeAI(
        model=CHAT_MODEL,
        api_key=load_api_key(),
    )
    graph = create_agent(model=model, tools=[search, add_document], system_prompt=system_prompt)

    started = time.perf_counter()
    all_messages: list[Any] = []
    raw_attempts: list[str] = []
    final = ""
    guardrail: dict[str, Any] = {}
    guarded_answer = ""

    # First normal agent pass, then up to two automatic citation-repair passes.
    # This prevents a correct answer being thrown away just because Gemini slightly
    # reformatted or invented one citation label in an otherwise supported draft.
    for attempt in range(3):
        if attempt == 0:
            user_content = question
        else:
            evidence_text = "\n".join(
                item["result"] for item in _TRACE
                if "query" in item.get("args", {}) and isinstance(item.get("result"), str)
            )
            allowed = sorted(set(CITATION_RE.findall(evidence_text)))
            allowed_text = ", ".join(allowed) if allowed else "(none)"
            user_content = (
                question
                + "\n\nCITATION REPAIR: The previous draft failed the citation-integrity guardrail. "
                + "Answer the question again from the corpus evidence. Copy ONLY these exact citation labels "
                + "when they support a claim: " + allowed_text + ". "
                + "Do not invent, shorten, alter, or substitute citation labels. "
                + "If the evidence is insufficient, use the exact refusal phrase instead."
            )

        result = graph.invoke({"messages": [{"role": "user", "content": user_content}]})
        messages = list(result.get("messages", []))
        all_messages.extend(messages)
        final = _message_text(messages[-1]) if messages else ""
        raw_attempts.append(final)
        guarded_answer, guardrail = _citation_guardrail(final, _TRACE)
        if not guardrail.get("fired"):
            break

    elapsed = time.perf_counter() - started
    guardrail["attempts"] = len(raw_attempts)
    guardrail["repaired"] = len(raw_attempts) > 1 and not guardrail.get("fired", False)
    return {
        "question": question,
        "answer": guarded_answer,
        "raw_answer": final,
        "raw_attempts": raw_attempts,
        "trace": list(_TRACE),
        "guardrail": guardrail,
        "usage": _usage(all_messages),
        "elapsed_seconds": elapsed,
        "model": CHAT_MODEL,
    }


def main() -> None:
    if len(sys.argv) < 2:
        raise SystemExit('Usage: python agent.py "your question"')
    question = " ".join(sys.argv[1:]).strip()
    result = answer_question(question)
    print(result["answer"])


if __name__ == "__main__":
    main()
