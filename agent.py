import asyncio
import json
import os
import re
import sys
import time
from pathlib import Path

from api_key import load_api_key
from index import ROOT

REFUSAL = "INSUFFICIENT EVIDENCE"

MODEL = os.getenv(
    "RAG_CHAT_MODEL", "gemini-3.5-flash-lite"
)

CITATION = re.compile(r"\[([^\[\]\n]+\|[^\[\]\n]+\|\d+)\]")

MAX_CALLS = 3


def decode_result(result):
    if getattr(result, "is_error", False) or getattr(
        result, "isError", False
    ):
        raise RuntimeError(str(result.content))

    text = "\n".join(
        getattr(c, "text", "") for c in result.content)

    value = json.loads(text)

    if isinstance(value, str):
        value = json.loads(value)

    return value


def validate_answer(answer, trace):

    valid_ids = {
        passage["id"]
        for item in trace
        if item["tool"] == "search"
        for passage in item["passages"]
    }

    cited = CITATION.findall(answer)

    if answer.strip().rstrip(".") == REFUSAL:
        return REFUSAL, None

    if not cited or not set(cited).issubset(valid_ids):
        return REFUSAL, "invalid_or_missing_citations"

    return answer, None


async def run_agent(question, interactive=False):

    from langchain.agents import create_agent
    from langchain_core.tools import tool
    from langchain_google_genai import ChatGoogleGenerativeAI

    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    key = load_api_key()
    started = time.perf_counter()

    trace = []
    guardrails = []
    calls = 0

    requested_path = None

    if question.lower().startswith("add document:"):
        requested_path = question.split(":", 1)[1].strip()

    params = StdioServerParameters(
        command=sys.executable,
        args=[str(ROOT / "server.py")],
        cwd=str(ROOT),
        env=dict(os.environ)
    )

    async with stdio_client(params) as (read, write):

        async with ClientSession(read, write) as session:

            await session.initialize()

            @tool
            async def search(query: str) -> str:
                """Retrieve five historical macroeconomic passages with exact citation IDs."""

                nonlocal calls

                if calls >= MAX_CALLS:
                    guardrails.append("call_limit")
                    return "Tool call limit reached."

                calls += 1

                result = await session.call_tool(
                    "search", {"query": query}
                )

                passages = decode_result(result)

                trace.append({
                    "tool": "search",
                    "query": query,
                    "passages": passages
                })

                return json.dumps(
                    passages, ensure_ascii=False
                )

            @tool
            async def add_document(path: str) -> str:
                """Add a document only after explicit human approval."""

                nonlocal calls

                if calls >= MAX_CALLS:
                    guardrails.append("call_limit")
                    return "Tool call limit reached."

                calls += 1

                if (
                    not requested_path
                    or not interactive
                    or not sys.stdin.isatty()
                    or Path(path).resolve()
                    != Path(requested_path).resolve()
                ):
                    guardrails.append("write_denied")
                    return "Denied: no explicit authorization."

                approval = input(
                    f"Approve adding {path}? Type YES: "
                )

                if approval != "YES":
                    guardrails.append("write_denied")
                    return "User denied the operation."

                result = await session.call_tool(
                    "add_document", {"path": path}
                )

                value = decode_result(result)

                trace.append({
                    "tool": "add_document",
                    "path": path,
                    "result": value
                })

                return json.dumps(value)

            model = ChatGoogleGenerativeAI(
                model=MODEL,
                google_api_key=key,
                temperature=0
            )

            agent = create_agent(
                model=model,
                tools=[search, add_document],
                system_prompt=(ROOT / "AGENTS.md").read_text()
            )

            result = await agent.ainvoke(
                {
                    "messages": [
                        {"role": "user", "content": question}
                    ]
                },
                config={"recursion_limit": 12}
            )

    messages = result["messages"]

    raw_answer = messages[-1].content

    if isinstance(raw_answer, list):
        raw_answer = "\n".join(
            b.get("text", "")
            if isinstance(b, dict) else str(b)
            for b in raw_answer
        )

    tokens = {
        "input_tokens": 0,
        "output_tokens": 0,
        "total_tokens": 0
    }

    for message in messages:
        usage = getattr(message, "usage_metadata", None) or {}

        for field in tokens:
            tokens[field] += usage.get(field, 0)

    write_completed = any(
        item["tool"] == "add_document"
        for item in trace
    )

    if requested_path and write_completed:
        answer = raw_answer
        guard = None
    else:
        answer, guard = validate_answer(
            raw_answer, trace
        )

    if guard:
        guardrails.append(guard)

    return {
        "answer": answer,
        "raw_answer": raw_answer,
        "trace": trace,
        "guardrails": guardrails,
        "tokens": tokens,
        "seconds": round(
            time.perf_counter() - started, 3
        )
    }


if __name__ == "__main__":

    question = " ".join(sys.argv[1:])

    result = asyncio.run(
        run_agent(question, interactive=True)
    )

    print(result["answer"])
