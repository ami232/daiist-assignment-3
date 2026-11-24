"""
The agent (`uv run python main.py ask "question"` runs `python agent.py "question"`).

How it works:
    1. Start server.py as an MCP server (stdio) and read its two tools.
    2. Wrap them as LangChain tools. add_document is wrapped with an approval step.
    3. Run a LangChain agent on Gemini Flash with AGENTS.md as system prompt and a
       limit on tool calls.
    4. Guardrail "plazo check": every number or deadline in the answer must appear in
       the text that search returned. If not, the answer is replaced by "no consta".

evaluate.py imports answer(question), which returns the answer and its trace.
"""

import asyncio
import re
import sys
import time
from pathlib import Path

from langchain.agents import create_agent
from langchain.agents.middleware import ToolCallLimitMiddleware
from langchain_core.tools import tool
from langchain_google_genai import ChatGoogleGenerativeAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
SYSTEM_PROMPT = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
MODEL = "gemini-3.5-flash-lite"  # fixed version; Flash free tier only allows 20 requests/day
MAX_TOOL_CALLS = 5
NO_CONSTA = "Esa información no consta en la ficha del trámite; puede consultarla en la sede electrónica:"


# ---------------------------------------------------------------- guardrail

# Numbers ("30", "1", "2015") and written-out deadlines ("un mes", "diez días").
NUMBER = r"\d+(?:[.,]\d+)?"
WRITTEN_PLAZO = (r"\b(?:un|una|dos|tres|cuatro|cinco|seis|siete|ocho|nueve|diez|quince|veinte|treinta)"
                 r"\s+(?:días?|semanas?|mes(?:es)?|años?|horas?)\b")


def plazo_check(answer: str, retrieved: str) -> list[str]:
    """Return the numbers/deadlines in the answer that do NOT appear in the retrieved text.

    Citations [..] and links are removed first: their numbers are not claims.
    An empty list means the answer passes.
    """
    claims = re.sub(r"\[[^\]]*\]|https?://\S+", " ", answer)
    retrieved_lower = retrieved.lower()
    unsupported = []
    for found in re.findall(NUMBER, claims) + re.findall(WRITTEN_PLAZO, claims.lower()):
        if found.lower() not in retrieved_lower:
            unsupported.append(found)
    return unsupported


def first_sede_link(retrieved: str) -> str:
    match = re.search(r"Sede: (https?://\S+)", retrieved)
    return match.group(1) if match else ""


# ---------------------------------------------------------------- tools

def ask_approval(path: str) -> bool:
    """Human in the loop: add_document only runs if a person types 'y'."""
    if not sys.stdin.isatty():  # nobody is there to approve (evaluation, CI): deny
        print(f"[approval] add_document({path!r}) denied: no interactive user.", file=sys.stderr)
        return False
    reply = input(f"\nThe agent wants to run add_document({path!r}). Allow? [y/N] ")
    return reply.strip().lower() in ("y", "yes", "s", "si", "sí")


def make_tools(session: ClientSession, trace: list[dict]):
    """LangChain tools that forward each call to the MCP server and record it in `trace`."""

    async def call_mcp(name: str, arguments: dict) -> str:
        result = await session.call_tool(name, arguments)
        text = "\n".join(getattr(c, "text", "") for c in result.content)
        trace.append({"tool": name, "args": arguments, "result": text})
        return text

    @tool
    async def search(query: str) -> str:
        """Search the trámite fichas of the Ayuntamiento de Santa María de Guía. Query in Spanish.
        Returns 5 passages, each with its citation [slug · section] and its sede link."""
        return await call_mcp("search", {"query": query})

    @tool
    async def add_document(path: str) -> str:
        """Add a ficha JSON file to the index. Needs the user's approval."""
        if not ask_approval(path):
            trace.append({"tool": "add_document", "args": {"path": path}, "result": "DENIED"})
            return "The user did not approve adding this document. Do not retry."
        return await call_mcp("add_document", {"path": path})

    return [search, add_document]


# ---------------------------------------------------------------- agent

async def answer_async(question: str) -> dict:
    start = time.time()
    trace: list[dict] = []
    server = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT))
    async with stdio_client(server) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            agent = create_agent(
                model=ChatGoogleGenerativeAI(model=MODEL, api_key=load_api_key(), temperature=0,
                                             max_retries=6),
                tools=make_tools(session, trace),
                system_prompt=SYSTEM_PROMPT,
                middleware=[ToolCallLimitMiddleware(run_limit=MAX_TOOL_CALLS, exit_behavior="continue")],
            )
            result = await agent.ainvoke({"messages": [{"role": "user", "content": question}]})

    messages = result["messages"]
    text = str(messages[-1].text)  # the final message of the agent is the answer
    tokens = sum((getattr(m, "usage_metadata", None) or {}).get("total_tokens", 0) for m in messages)

    # Guardrail: every number/deadline in the answer must be in what search returned.
    retrieved = "\n".join(step["result"] for step in trace if step["tool"] == "search")
    unsupported = plazo_check(text, retrieved)
    guardrail_fired = bool(unsupported)
    original = text
    if guardrail_fired:
        print(f"[guardrail] unsupported numbers/deadlines {unsupported}: answer replaced.", file=sys.stderr)
        text = f"{NO_CONSTA} {first_sede_link(retrieved)}".strip()

    return {
        "question": question,
        "answer": text,
        "original_answer": original,
        "guardrail_fired": guardrail_fired,
        "unsupported": unsupported,
        "trace": trace,
        "retrieved": retrieved,
        "tokens": tokens,
        "seconds": round(time.time() - start, 1),
    }


def answer(question: str) -> dict:
    """Answer one question. Returns the answer, the tool trace, tokens and seconds."""
    return asyncio.run(answer_async(question))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit('Usage: uv run python agent.py "your question"')
    out = answer(" ".join(sys.argv[1:]))
    print(out["answer"])
    print(f"\n({len(out['trace'])} tool calls, {out['tokens']} tokens, {out['seconds']} s)")
