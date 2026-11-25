"""
Assignment 3: your agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with tools from server.py over MCP and
AGENTS.md as system prompt. Ask for approval before add_document runs; add a
call limit and one guardrail of your choice. Print the answer with citations.

Start from session 10's 07-own-harness/harness.py. Expose a function that
returns the answer and the tool trace, for evaluate.py.
"""

from __future__ import annotations

import asyncio
import json
import re
import sys
import time
from pathlib import Path

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
SYSTEM_PROMPT = ROOT / "AGENTS.md"
MODEL = "gemini-3.6-flash"
MAX_TOOL_CALLS = 4
CITATION = re.compile(r"([\w.\-]+\.pdf),\s*page\s*(\d+)", re.IGNORECASE)
REFUSAL_MARKERS = (
    "i don't know", "i do not know", "cannot determine", "can't determine",
    "not enough information", "not covered", "does not specify",
    "do not have sufficient", "don't have sufficient",
)


def _text_from_content(content) -> str:
    """Gemini/LangChain messages may contain a string or structured text blocks."""
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(
            item.get("text", "") if isinstance(item, dict) else str(item)
            for item in content
        ).strip()
    return str(content or "")


def _refusal(answer: str) -> bool:
    return any(marker in answer.lower() for marker in REFUSAL_MARKERS)


def _verify_answer(answer: str, evidence: set[tuple[str, int]], searched: bool,
                   add_succeeded: bool, add_attempted: bool) -> str:
    """Fail closed when a substantive answer has no valid retrieved citations."""
    if not searched:
        if add_succeeded:
            return answer
        if add_attempted:
            return "The document was not added because approval was not granted or indexing failed."
        return "I don't know based on the documents in this collection."

    if _refusal(answer) and not CITATION.search(answer):
        return answer

    citations = {(name, int(page)) for name, page in CITATION.findall(answer)}
    if not citations or not citations.issubset(evidence):
        return (
            "I don't know based on the documents in this collection. "
            "I could not verify the source citations for the generated answer."
        )
    return answer


async def answer_with_trace(question: str) -> dict:
    """Return answer, MCP tool trace and model token usage for evaluation."""
    from langchain.agents import create_agent
    from langchain.tools import tool
    from langchain_google_genai import ChatGoogleGenerativeAI
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    started = time.monotonic()
    trace: list[dict] = []
    allowed_citations: set[tuple[str, int]] = set()
    searches = 0
    successful_add = False
    add_attempted = False
    call_count = 0

    if not SYSTEM_PROMPT.exists():
        raise FileNotFoundError("Missing AGENTS.md system prompt")
    if not question.strip():
        raise ValueError("Please provide a question")

    params = StdioServerParameters(
        command=sys.executable, args=["server.py"], cwd=str(ROOT)
    )
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            advertised = {t.name for t in (await session.list_tools()).tools}
            if not {"search", "add_document"}.issubset(advertised):
                raise RuntimeError("MCP server must expose search and add_document")

            @tool("search")
            async def search_tool(query: str) -> str:
                """Search CFPB financial education PDFs, returning source-page passages."""
                nonlocal call_count, searches
                if call_count >= MAX_TOOL_CALLS:
                    return "Tool-call limit reached. Use existing evidence or refuse."
                call_count += 1
                searches += 1
                response = await session.call_tool("search", {"query": query})
                body = "\n".join(
                    getattr(item, "text", "") for item in response.content
                )
                trace.append({"tool": "search", "input": query, "output": body})
                if getattr(response, "isError", False):
                    return f"Search error: {body}"
                try:
                    payload = json.loads(body)
                    for passage in payload.get("passages", []):
                        source = passage.get("source", "")
                        location = passage.get("location", "")
                        match = re.fullmatch(r"page\s+(\d+)", str(location))
                        if source and match:
                            allowed_citations.add((source, int(match.group(1))))
                except (ValueError, TypeError, AttributeError):
                    pass
                return body

            @tool("add_document")
            async def add_document_tool(path: str) -> str:
                """Add a local PDF to the indexed corpus; requires human approval."""
                nonlocal call_count, successful_add, add_attempted
                add_attempted = True
                if call_count >= MAX_TOOL_CALLS:
                    return "Tool-call limit reached. Document was not added."
                call_count += 1
                if not sys.stdin.isatty():
                    trace.append({"tool": "add_document", "input": path,
                                  "approved": False, "reason": "non-interactive"})
                    return "APPROVAL REQUIRED: no interactive terminal; document not added."

                print(f"\nApprove adding the PDF to the knowledge base? {path}",
                      file=sys.stderr, flush=True)
                decision = await asyncio.to_thread(input, "Type YES to approve: ")
                if decision.strip() != "YES":
                    trace.append({"tool": "add_document", "input": path,
                                  "approved": False})
                    return "User denied approval. Document was not added."

                result = await session.call_tool("add_document", {"path": path})
                body = "\n".join(
                    getattr(item, "text", "") for item in result.content
                )
                trace.append({"tool": "add_document", "input": path,
                              "approved": True, "output": body})
                if not getattr(result, "isError", False):
                    try:
                        data = json.loads(body)
                        successful_add = "error" not in data
                    except (ValueError, TypeError):
                        pass
                return body

            model = ChatGoogleGenerativeAI(
                model=MODEL, api_key=load_api_key(), max_retries=6,
            )
            agent = create_agent(
                model=model,
                tools=[search_tool, add_document_tool],
                system_prompt=SYSTEM_PROMPT.read_text(encoding="utf-8"),
            )
            result = await agent.ainvoke(
                {
                    "messages": [{
                    "role": "user",
                    "content": (
                        question
                        + "\n\nAnswer in no more than 100 words. "
                        "Be direct and include only information necessary to answer "
                        "the question. Use a maximum of 3 short bullet points. "
                        "Cite every factual claim using [filename.pdf, page N]. "
                        "If the documents do not contain the answer, explicitly "
                        "say so instead of guessing."
                    ),
                }]
            },
            config={"recursion_limit": 12},
        )

    messages = result.get("messages", [])
    answer = _text_from_content(messages[-1].content) if messages else ""
    answer = _verify_answer(
        answer, allowed_citations, searches > 0, successful_add, add_attempted
    )
    input_tokens = output_tokens = 0
    for message in messages:
        usage = getattr(message, "usage_metadata", None) or {}
        input_tokens += int(usage.get("input_tokens") or 0)
        output_tokens += int(usage.get("output_tokens") or 0)

    return {
        "answer": answer,
        "tool_trace": trace,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "seconds": round(time.monotonic() - started, 2),
    }


def ask(question: str) -> dict:
    """Synchronous entry point used by the later evaluate.py agent evaluation."""
    return asyncio.run(answer_with_trace(question))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit('Usage: uv run python main.py ask "your question"')
    response = ask(" ".join(sys.argv[1:]))
    print(response["answer"])

