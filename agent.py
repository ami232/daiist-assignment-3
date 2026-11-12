import asyncio
import json
import re
import sys
from pathlib import Path

from langchain.agents import create_agent
from langchain.mcp import MCPAdapter
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI

from api_key import load_api_key


ROOT = Path(__file__).resolve().parent
SYSTEM_PROMPT = (ROOT / "AGENTS.md").read_text(
    encoding="utf-8"
)

MODEL = "gemini-3.5-flash-lite"
MAX_SEARCH_CALLS = 4

REFUSAL = (
    "I cannot determine this from the available documents."
)


def format_tool_result(result):
    """Convert MCP output into text for the agent."""
    if isinstance(result, str):
        return result
    if isinstance(result, list):
        parts = []
        for item in result:
            if isinstance(item, dict):
                parts.append(item.get("text", json.dumps(item)))
            else:
                parts.append(str(item))
        return "\n".join(parts)
    return str(result)


async def run_agent(question, allow_approval=True):
    """
    Run the RAG agent and return answer and tool trace.

    allow_approval=False is used for automated evaluation.
    """

    load_api_key()

    print("[DEBUG 1] Gemini API key loaded", flush=True)

    trace = []
    search_calls = 0
    evidence_found = False

    async with MCPAdapter(
        ROOT / "server.py"
    ) as adapter:

        mcp_tools = await adapter.list_tools()
        print("[DEBUG 2] MCP tools loaded", flush=True)
        tool_map = {t.name: t for t in mcp_tools}

        if "search" not in tool_map:
            raise RuntimeError("MCP search tool not found.")

        if "add_document" not in tool_map:
            raise RuntimeError(
                "MCP add_document tool not found."
            )

        @tool("search")
        async def search_tool(query: str) -> str:
            """Search EU regulations and return cited passages."""
            nonlocal search_calls, evidence_found

            if search_calls >= MAX_SEARCH_CALLS:
                return (
                    "Search limit reached. Do not call "
                    "search again. Answer only from "
                    "evidence already retrieved."
                )

            search_calls += 1

            result = await tool_map["search"].ainvoke(
                {"query": query}
            )

            content = format_tool_result(result)

            trace.append({
                "tool": "search",
                "query": query,
                "result": content,
            })

            if (
                "[Result 1]" in content
                and "Citation:" in content
            ):
                evidence_found = True

            return content

        @tool("add_document")
        async def add_document_tool(path: str) -> str:
            """Add a PDF to the corpus after explicit user approval."""

            approved = False

            if allow_approval and sys.stdin.isatty():
                print(
                    f"\nAgent requests permission to "
                    f"index: {path}",
                    file=sys.stderr,
                )

                confirmation = input(
                    "Type APPROVE to allow this operation: "
                )

                approved = confirmation == "APPROVE"

            if not approved:
                trace.append({
                    "tool": "add_document",
                    "path": path,
                    "approved": False,
                })

                return (
                    "Document addition denied. "
                    "Explicit user approval is required."
                )

            trace.append({
                "tool": "add_document",
                "path": path,
                "approved": True,
            })

            result = await tool_map["add_document"].ainvoke(
                {"path": path}
            )

            return format_tool_result(result)

        model = ChatGoogleGenerativeAI(
            model=MODEL,
            temperature=0,
            max_retries=2,
        )

        prompt = SYSTEM_PROMPT + """

Additional harness rules:
- Always call search before answering a factual question.
- Search again when a comparison requires more evidence.
- Never call add_document unless the user requests it.
- Cite factual claims using retrieved source information.
- If the evidence is insufficient, explicitly refuse.
"""

        agent = create_agent(
            model=model,
            tools=[search_tool, add_document_tool],
            system_prompt=prompt,
        )

        print("[DEBUG 3] Starting LangChain agent", flush=True)

        result = await agent.ainvoke(
            {
                "messages": [
                    {"role": "user", "content": question}
                ]
            },
            config={"recursion_limit": 12},
        )
        print("[DEBUG 4] LangChain agent finished", flush=True)
        messages = result["messages"]

        final_content = messages[-1].content
        if isinstance(final_content, str):
            answer = final_content
        else:
            answer = format_tool_result(final_content)

        # Deterministic evidence guardrail.
        if not evidence_found:
            answer = REFUSAL
            trace.append({
                "guardrail": "missing_search_evidence",
                "triggered": True,
            })

        # Require at least one source citation for
        # substantive answers.
        has_citation = bool(
            re.search(
                r"\[(?:GDPR|DSA|AI_ACT|AI Act|aepd_2025\.pdf)[^\]]*\]",
                answer,
                flags=re.IGNORECASE,
            )
        )

        if (
            evidence_found
            and REFUSAL not in answer
            and not has_citation
        ):
            answer = REFUSAL
            trace.append({
                "guardrail": "missing_citation",
                "triggered": True,
            })

        return {
            "question": question,
            "answer": answer,
            "tool_trace": trace,
            "search_calls": search_calls,
        }


def main():
    if len(sys.argv) < 2:
        print(
            'Usage: python agent.py "your question"',
            file=sys.stderr,
        )
        sys.exit(1)

    question = " ".join(sys.argv[1:])

    result = asyncio.run(run_agent(question))

    print("\nANSWER:\n")
    print(result["answer"])

    print(
        f"\nSearch calls: {result['search_calls']}"
    )


if __name__ == "__main__":
    main()
