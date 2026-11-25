
import asyncio
import sys
import os
import re
import time
import json

from pathlib import Path
from api_key import load_api_key
from langchain.agents import create_agent
from langchain_core.tools import StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_mcp_adapters.client import MultiServerMCPClient

ROOT = Path(__file__).resolve().parent

REFUSAL = "I don't know based on the available documents."

async def ask(question, approve=None):

    started = time.perf_counter()
    key = load_api_key()

    client = MultiServerMCPClient({
        "corpus": {
            "command": sys.executable,
            "args": [str(ROOT / "server.py")],
            "transport": "stdio",
            "env": dict(os.environ)
        }
    })

    tools = await client.get_tools()

    original_search = next(
        t for t in tools if t.name == "search"
    )

    original_add = next(
        t for t in tools if t.name == "add_document"
    )

    evidence = []

    async def safe_search(query: str):
        """Search the indexed documents for cited evidence."""

        result = await original_search.ainvoke({
            "query": query
        })

        evidence.append(str(result))
        return result

    async def approved_add(path: str):
        """Add a PDF only after explicit human approval."""

        if approve is None or not approve(path):
            return "Permission denied. Human approval required."

        return await original_add.ainvoke({
            "path": path
        })

    safe_tools = [
        StructuredTool.from_function(
            coroutine=safe_search,
            name="search"
        ),
        StructuredTool.from_function(
            coroutine=approved_add,
            name="add_document"
        )
    ]

    model = ChatGoogleGenerativeAI(
        model=os.getenv("GEMINI_CHAT_MODEL", "gemini-flash-latest"),
        google_api_key=key,
        temperature=0,
        max_retries=3
    )

    agent = create_agent(
        model=model,
        tools=safe_tools,
        system_prompt=(ROOT / "AGENTS.md").read_text()
    )

    result = await agent.ainvoke(
        {"messages": [
            {"role": "user", "content": question}
        ]},
        config={"recursion_limit": 16}
    )

    messages = result["messages"]
    final = messages[-1]
    answer = final.content

    if isinstance(answer, list):
        answer = " ".join(
            block.get("text", "")
            for block in answer
            if isinstance(block, dict)
            and block.get("type") == "text"
        )

    citations = re.findall(
        r"\[[^\[\]]+\.pdf, p\. \d+\]",
        answer
    )

    valid_citations = bool(citations) and all(
        citation in " ".join(evidence)
        for citation in citations
    )

    # Additional guardrail: reject answers with
    # missing or fabricated citations.

    if not valid_citations:
        answer = REFUSAL

    input_tokens = 0
    output_tokens = 0

    for message in messages:
        usage = getattr(message, "usage_metadata", None) or {}
        input_tokens += usage.get("input_tokens", 0)
        output_tokens += usage.get("output_tokens", 0)

    return {
        "question": question,
        "answer": answer,
        "valid_citations": valid_citations,
        "evidence": evidence,
        "input_tokens": input_tokens,
        "output_tokens": output_tokens,
        "seconds": round(time.perf_counter() - started, 3)
    }

def request_approval(path):
    if not sys.stdin.isatty():
        return False

    response = input(
        f"Approve indexing {path}? Type YES: "
    )

    return response.strip() == "YES"

if __name__ == "__main__":

    question = " ".join(sys.argv[1:])

    result = asyncio.run(
        ask(question, approve=request_approval)
    )

    print(json.dumps(result, indent=2))
