"""
Assignment 3: your agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the tools of server.py over MCP and
AGENTS.md as system prompt.
- Approval: add_document only runs if the human approves (a callback).
- Call limit: at most MAX_TOOL_CALLS tool calls per question.
- Guardrail (my choice): citation check. Every [source, location] citation in the
  answer must come from a chunk the search tool really returned. If not, the
  answer is withdrawn and replaced by a refusal.
`ask(question, approve)` returns the answer and the tool trace (used by evaluate.py).
"""

import asyncio
import re
import sys
import time
from pathlib import Path

from langchain.agents import create_agent
from langchain_core.messages import AIMessage, HumanMessage
from langchain_core.tools import StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
MODEL = "gemini-3.5-flash"
MAX_TOOL_CALLS = 6
MAX_QUESTION_CHARS = 1500
REFUSAL = "I don't know: the corpus does not cover this question."
CITATION = re.compile(r"\[([^\[\]\n]+?),\s*([^\[\]\n]+?)\]")


def system_prompt() -> str:
    return (ROOT / "AGENTS.md").read_text(encoding="utf-8")


def base_location(location: str) -> str:
    """'Section 3.1.1 (p. 8-10) (part 1/4)' -> 'section 3.1.1'; 'Article 33(1)' -> 'article 33'."""
    return re.split(r"\s*\(", location.strip())[0].strip().lower()


def retrieved_citations(calls: list[dict]) -> list[tuple[str, str]]:
    found = []
    for call in calls:
        if call["name"] != "search":
            continue
        for source, location in re.findall(r"Citation: \[([^\[\]\n]+?),\s*([^\[\]\n]+?)\]", call["result"]):
            found.append((source.strip().lower(), location.strip()))
    return found


def check_citations(answer: str, calls: list[dict]) -> tuple[list[str], list[str]]:
    """(cited, invalid): the citations found in the answer and those no search result supports."""
    allowed = set()
    for source, location in retrieved_citations(calls):
        for part in location.split(" to "):
            allowed.add((source, base_location(part)))
    cited, invalid = [], []
    for source, location in CITATION.findall(answer):
        label = f"[{source.strip()}, {location.strip()}]"
        cited.append(label)
        if (source.strip().lower(), base_location(location)) not in allowed:
            invalid.append(label)
    return cited, invalid


def is_refusal(answer: str) -> bool:
    text = answer.lower()
    return text.startswith("i don't know") or "corpus does not cover" in text or "not covered by the corpus" in text


def text_of(content) -> str:
    if isinstance(content, str):
        return content
    return "".join(part.get("text", "") if isinstance(part, dict) else str(part) for part in content)


def ask_human(path: str) -> bool:
    """Default approval: ask in the terminal. Without a terminal the answer is no."""
    if not sys.stdin.isatty():
        return False
    return input(f"\nThe agent wants to add '{path}' to the index. Allow? [y/N] ").strip().lower() == "y"


async def _ask(question: str, approve) -> dict:
    started = time.time()
    calls: list[dict] = []
    if len(question) > MAX_QUESTION_CHARS:
        return {"question": question[:80], "answer": REFUSAL, "calls": calls, "cited": [], "invalid": [],
                "refused": True, "guardrail": "input too long", "seconds": 0.0,
                "input_tokens": 0, "output_tokens": 0}

    params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT))
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            described = {t.name: (t.description or "") for t in (await session.list_tools()).tools}

            async def run_tool(name: str, args: dict) -> str:
                if len(calls) >= MAX_TOOL_CALLS:
                    return f"Tool call limit ({MAX_TOOL_CALLS}) reached. Answer with what you have or say the corpus does not cover it."
                if name == "add_document" and not approve(args.get("path", "")):
                    text = "DENIED: the user did not approve adding this document."
                else:
                    result = await session.call_tool(name, args)
                    text = "\n".join(getattr(c, "text", "") for c in result.content)
                calls.append({"name": name, "args": args, "result": text})
                return text

            async def search(query: str) -> str:
                return await run_tool("search", {"query": query})

            async def add_document(path: str) -> str:
                return await run_tool("add_document", {"path": path})

            tools = [
                StructuredTool.from_function(coroutine=search, name="search", description=described.get("search", "Search the corpus.")),
                StructuredTool.from_function(coroutine=add_document, name="add_document", description=described.get("add_document", "Add a document.")),
            ]
            llm = ChatGoogleGenerativeAI(model=MODEL, temperature=0, google_api_key=load_api_key())
            agent = create_agent(llm, tools, system_prompt=system_prompt())
            state = None
            for attempt in range(4):
                try:
                    calls.clear()
                    state = await agent.ainvoke({"messages": [HumanMessage(question)]}, config={"recursion_limit": 16})
                    break
                except Exception as error:  # noqa: BLE001
                    if ("429" in str(error) or "RESOURCE_EXHAUSTED" in str(error)) and attempt < 3:
                        print(f"  rate limit, waiting {30 * (attempt + 1)} s ...", file=sys.stderr)
                        await asyncio.sleep(30 * (attempt + 1))
                        continue
                    raise

    messages = state["messages"]
    answer = text_of(messages[-1].content).strip()
    in_tokens = out_tokens = 0
    for message in messages:
        if isinstance(message, AIMessage) and message.usage_metadata:
            in_tokens += message.usage_metadata.get("input_tokens", 0)
            out_tokens += message.usage_metadata.get("output_tokens", 0)

    cited, invalid = check_citations(answer, calls)
    guardrail = None
    if not is_refusal(answer) and (not cited or invalid):
        guardrail = "citation check: " + ("no citation" if not cited else "unsupported " + ", ".join(invalid))
        answer = REFUSAL + " (My answer was withdrawn because its citations could not be verified.)"
    return {"question": question, "answer": answer, "calls": list(calls), "cited": cited, "invalid": invalid,
            "refused": is_refusal(answer), "guardrail": guardrail, "seconds": round(time.time() - started, 1),
            "input_tokens": in_tokens, "output_tokens": out_tokens}


def ask(question: str, approve=ask_human) -> dict:
    """Answer one question. Returns answer, tool trace (calls), citations, guardrail and cost."""
    return asyncio.run(_ask(question, approve))


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit('usage: python agent.py "your question"')
    result = ask(" ".join(sys.argv[1:]))
    print(result["answer"])
    sources = sorted(set(result["cited"]))
    if sources:
        print("\nSources: " + "; ".join(sources))
    if result["guardrail"]:
        print(f"[guardrail fired: {result['guardrail']}]")
    print(f"[{result['seconds']} s, {result['input_tokens']} input / {result['output_tokens']} output tokens, "
          f"{len(result['calls'])} tool calls]", file=sys.stderr)
