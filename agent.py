import asyncio
import os
import sys
import time
from pathlib import Path

from langchain.agents import create_agent
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from api_key import load_api_key


ROOT = Path(__file__).resolve().parent
CORPUS = (ROOT / "corpus").resolve()
MAX_TOOL_CALLS = 4


async def run_agent(question, *, interactive=False):
    """Return the answer, tool trace, model token usage and elapsed seconds."""
    started = time.perf_counter()
    trace = []
    rules = (ROOT / "AGENTS.md").read_text(encoding="utf-8-sig")
    model = ChatGoogleGenerativeAI(
        model=os.getenv("GEMINI_CHAT_MODEL", "gemini-3.5-flash"),
        api_key=load_api_key(),
    )
    server = StdioServerParameters(
        command=sys.executable,
        args=[str(ROOT / "server.py")],
        cwd=str(ROOT),
    )

    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()

            def record(name, arguments):
                event = {"tool": name, "arguments": arguments}
                trace.append(event)
                return event

            def stop(event, reason):
                event.update(status="blocked", result=reason)
                return reason

            async def call_server(event):
                result = await session.call_tool(event["tool"], event["arguments"])
                text = "\n".join(
                    item.text for item in result.content if hasattr(item, "text")
                )
                failed = getattr(result, "is_error", False) or getattr(
                    result, "isError", False
                )
                event.update(status="error" if failed else "ok", result=text)
                return f"Tool error: {text}" if failed else text

            @tool
            async def search(query: str) -> str:
                """Search the indexed guidance and return passages with citations."""
                event = record("search", {"query": query})
                if len(trace) > MAX_TOOL_CALLS:
                    return stop(event, "Tool-call limit reached. Use existing evidence.")
                return await call_server(event)

            @tool
            async def add_document(path: str) -> str:
                """Ask the user for approval to index a PDF from the corpus folder."""
                candidate = (ROOT / path).resolve()
                event = record("add_document", {"path": str(candidate)})

                if len(trace) > MAX_TOOL_CALLS:
                    return stop(event, "Tool-call limit reached.")
                if not candidate.is_relative_to(CORPUS):
                    return stop(event, "Blocked: the file must be inside corpus/.")
                if candidate.suffix.lower() != ".pdf" or not candidate.is_file():
                    return stop(event, "Blocked: select an existing PDF.")
                if not interactive or not sys.stdin.isatty():
                    return stop(event, "Blocked: interactive approval is required.")

                reply = input(f"\nAdd this PDF to the index?\n{candidate}\nType yes: ")
                if reply.strip().lower() != "yes":
                    return stop(event, "User declined. The document was not added.")

                event["approved"] = True
                return await call_server(event)

            agent = create_agent(
                model=model,
                tools=[search, add_document],
                system_prompt=rules,
            )
            state = await agent.ainvoke(
                {"messages": [{"role": "user", "content": question}]},
                config={"recursion_limit": 16},
            )

    messages = state["messages"]
    final = messages[-1].content
    if isinstance(final, str):
        answer = final
    else:
        answer = "\n".join(
            block if isinstance(block, str) else block.get("text", "")
            for block in final
            if isinstance(block, str)
            or (isinstance(block, dict) and block.get("type") == "text")
        )

    usage = {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}
    for message in messages:
        metadata = getattr(message, "usage_metadata", None) or {}
        for key in usage:
            usage[key] += metadata.get(key, 0)

    return {
        "answer": answer.strip(),
        "trace": trace,
        "model_usage": usage,
        "seconds": round(time.perf_counter() - started, 2),
    }


if __name__ == "__main__":
    question = " ".join(sys.argv[1:]).strip()
    if not question:
        raise SystemExit('Usage: python agent.py "your question"')

    result = asyncio.run(run_agent(question, interactive=True))
    for event in result["trace"]:
        print(f"Tool: {event['tool']} | {event['status']}", file=sys.stderr)
    print(result["answer"])
