"""
Assignment 3: the agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the tools of server.py over MCP and
AGENTS.md as system prompt.

Guardrails
- approval: add_document pauses for a yes/no from the user; with no user at the
  keyboard (evaluation), it is refused.
- limits: at most 6 tool calls and 8 model calls per question.
- quote and citation check (our extra guardrail): every quoted passage must appear
  word for word in the text the search returned, and every (Chapter, ¶) citation
  must point to a returned passage. On failure the agent gets one chance to fix
  its answer; if it still fails, the answer is printed with a warning.

`ask(question)` returns the answer and its trace, for evaluate.py.
"""

import asyncio
import warnings
import re
import sys
import time
from pathlib import Path

from langchain.agents import create_agent
from langchain.agents.middleware import (
    HumanInTheLoopMiddleware,
    ModelCallLimitMiddleware,
    ModelFallbackMiddleware,
    ModelRetryMiddleware,
    ToolCallLimitMiddleware,
)
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_core.tools import StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.types import Command
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from api_key import load_api_key

warnings.filterwarnings("ignore", message=".*uses fixed sampling defaults.*")

ROOT = Path(__file__).resolve().parent
SYSTEM_PROMPT = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
# The first model answers; the fallback is used when it is overloaded (503). Newer Flash
# models were returning 503 "high demand" on 23 Nov 2026.
MODELS = ["gemini-3.5-flash", "gemini-3.5-flash-lite"]
MAX_TOOL_CALLS = 6
MAX_MODEL_CALLS = 8


# --------------------------------------------------------------------------- the quote and citation check

QUOTE_MARKS = str.maketrans({"“": '"', "”": '"', "‘": "'", "’": "'", "«": '"', "»": '"'})
HIT = re.compile(r"^\[\d+\] (?P<source>[^|\n]+) \| (?P<chapter>Chapter [IVXLC]+)[^\n]*?, ¶(?P<paras>[\d–-]+) \(similarity", re.M)


def normalise(text: str) -> str:
    """Compare text ignoring quote-mark style, case, spacing and the quote marks themselves."""
    text = text.translate(QUOTE_MARKS).lower().replace('"', "").replace("'", "")
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", text)).strip()


def parse_hits(search_output: str) -> list[dict]:
    """Split a search result into passages: source, chapter, paragraph range, text."""
    hits = []
    starts = list(HIT.finditer(search_output))
    for n, match in enumerate(starts):
        end = starts[n + 1].start() if n + 1 < len(starts) else len(search_output)
        first, _, last = match["paras"].replace("–", "-").partition("-")
        hits.append({
            "source": match["source"].strip(), "chapter": match["chapter"],
            "first": int(first), "last": int(last or first),
            "heading": search_output[match.start():search_output.index("\n", match.start())],
            "text": search_output[search_output.index("\n", match.start()) + 1:end].strip(),
        })
    return hits


def quotes_in(answer: str) -> list[str]:
    """Quoted passages of 3+ words. A quote with an ellipsis is checked piece by piece."""
    quotes = re.findall(r"[“\"]([^”\"]{8,}?)[”\"]", answer)
    pieces = []
    for quote in quotes:
        for piece in re.split(r"\s*(?:\.\.\.|…)\s*", quote):
            if len(piece.split()) >= 3:
                pieces.append(piece)
    return pieces


def citations_in(answer: str) -> list[tuple[str, str, int]]:
    """(text of the citation, chapter, first paragraph) for every 'Chapter X, ¶n' in the answer."""
    found = []
    for match in re.finditer(r"([^()\n]{0,80}?)\bChapter ([IVXLC]+)[^()\n¶]{0,160}?¶\s*(\d+)", answer):
        found.append((match.group(0).strip(), f"Chapter {match.group(2)}", int(match.group(3))))
    return found


def check_answer(answer: str, hits: list[dict]) -> list[str]:
    """Problems with quotes and citations, as sentences the model can act on. Empty = all verified."""
    problems = []
    corpus = " ".join(normalise(h["text"]) for h in hits)
    for quote in quotes_in(answer):
        if normalise(quote) not in corpus:
            problems.append(f'The quote "{quote}" is not word for word in any passage the search returned.')
    authors = {h["source"].split(",")[0].lower() for h in hits}
    for text, chapter, paragraph in citations_in(answer):
        author = next((a for a in authors if a in text.lower()), "")
        ok = any(
            h["chapter"] == chapter and h["first"] <= paragraph <= h["last"]
            and (not author or author in h["source"].lower())
            for h in hits
        )
        if not ok:
            problems.append(f"The citation '{text}' does not match any passage the search returned.")
    return problems


# --------------------------------------------------------------------------- the agent

async def load_mcp_tools(session: ClientSession) -> list[StructuredTool]:
    """Wrap each MCP tool as a LangChain tool that calls the server over this session.

    (langchain-mcp-adapters does not support mcp 2.x yet, so this small adapter replaces it.)
    """
    tools = []
    for tool in (await session.list_tools()).tools:
        async def call(_name=tool.name, **arguments) -> str:
            result = await session.call_tool(_name, arguments)
            return "\n".join(getattr(part, "text", "") for part in result.content)

        tools.append(StructuredTool(
            name=tool.name, description=tool.description or "",
            args_schema=tool.input_schema, coroutine=call,
        ))
    return tools


def is_temporary(error: BaseException) -> bool:
    """Overloaded or slow model (503, 500, timeout): worth waiting and retrying."""
    text = str(error)
    return any(sign in text for sign in ("503", "UNAVAILABLE", "500", "INTERNAL", "imed out", "DEADLINE"))


def make_model():
    load_api_key()
    models = [ChatGoogleGenerativeAI(model=m, temperature=0, max_retries=1, timeout=45) for m in MODELS]
    return models[0], models[1:]


def console_approval(call: dict) -> bool:
    if not sys.stdin.isatty():
        return False
    reply = input(f"\nThe agent wants to run {call['name']}({call['args']}). Allow? [y/N] ")
    return reply.strip().lower() in ("y", "yes")


async def ask_async(question: str, approve=console_approval) -> dict:
    """Answer one question. Returns answer, tool calls, guardrail events, tokens and seconds."""
    started = time.time()
    params = StdioServerParameters(command=sys.executable, args=[str(ROOT / "server.py")], cwd=str(ROOT))
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            tools = await load_mcp_tools(session)
            model, fallbacks = make_model()
            agent = create_agent(
                model=model,
                tools=tools,
                system_prompt=SYSTEM_PROMPT,
                checkpointer=InMemorySaver(),
                middleware=[
                    # Gemini models are often busy (503): retry with waits, then try the fallback model.
                    ModelRetryMiddleware(max_retries=3, initial_delay=5, backoff_factor=2, on_failure="error", retry_on=is_temporary),
                    ModelFallbackMiddleware(*fallbacks),
                    HumanInTheLoopMiddleware(interrupt_on={"add_document": True}),
                    ToolCallLimitMiddleware(run_limit=MAX_TOOL_CALLS),
                    ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS),
                ],
            )
            config = {"configurable": {"thread_id": "ask"}}
            events = []

            async def run(payload):
                result = await agent.ainvoke(payload, config)
                while result.get("__interrupt__"):  # add_document is waiting for approval
                    decisions = []
                    for request in result["__interrupt__"][0].value["action_requests"]:
                        allowed = approve(request)
                        events.append(f"approval: {request['name']} {'approved' if allowed else 'refused'}")
                        decisions.append({"type": "approve"} if allowed else
                                         {"type": "reject", "message": "The user did not approve adding this document."})
                    result = await agent.ainvoke(Command(resume={"decisions": decisions}), config)
                return result

            result = await run({"messages": [HumanMessage(question)]})
            hits = hits_from(result["messages"])
            answer = final_text(result["messages"])
            problems = check_answer(answer, hits)
            if problems:
                events.append("quote check: " + " | ".join(problems))
                retry = ("Your answer failed the automatic quote and citation check:\n- " + "\n- ".join(problems)
                         + "\nRewrite the answer. Quote only text that appears word for word in the passages, "
                           "cite only passages you received, or remove the quote. You may search again.")
                result = await run({"messages": [HumanMessage(retry)]})
                hits = hits_from(result["messages"])
                answer = final_text(result["messages"])
                problems = check_answer(answer, hits)
                if problems:
                    events.append("quote check failed again: answer flagged")
                    answer += "\n\n⚠ Could not verify in the course texts:\n- " + "\n- ".join(problems)
                else:
                    events.append("quote check passed after rewrite")

    messages = result["messages"]
    usage = [m.usage_metadata for m in messages if isinstance(m, AIMessage) and m.usage_metadata]
    return {
        "question": question,
        "answer": answer,
        "tool_calls": [{"name": c["name"], "args": c["args"]} for m in messages if isinstance(m, AIMessage) for c in m.tool_calls],
        "retrieved": [h["heading"] for h in hits],
        "retrieved_text": "\n\n".join(f"{h['heading']}\n{h['text']}" for h in hits),
        "guardrail_events": events,
        "input_tokens": sum(u.get("input_tokens", 0) for u in usage),
        "output_tokens": sum(u.get("output_tokens", 0) for u in usage),
        "model_calls": len(usage),
        "models": sorted({m.response_metadata.get("model_name", "?") for m in messages if isinstance(m, AIMessage)}),
        "seconds": round(time.time() - started, 1),
    }


def hits_from(messages) -> list[dict]:
    hits = []
    for m in messages:
        if isinstance(m, ToolMessage) and m.name == "search":
            hits.extend(parse_hits(content_text(m.content)))
    return hits


def content_text(content) -> str:
    if isinstance(content, str):
        return content
    return "".join(part.get("text", "") if isinstance(part, dict) else str(part) for part in content)


def final_text(messages) -> str:
    for m in reversed(messages):
        if isinstance(m, AIMessage) and not m.tool_calls:
            text = content_text(m.content).strip()
            if text:
                return text
    return "No answer: the agent stopped before answering (tool or model call limit)."


def ask(question: str, approve=console_approval) -> dict:
    return asyncio.run(ask_async(question, approve))


def main() -> None:
    if len(sys.argv) < 2:
        sys.exit('usage: python agent.py "your question"')
    result = ask(" ".join(sys.argv[1:]))
    print(result["answer"])
    if result["retrieved"]:
        print("\nSources retrieved:")
        for heading in dict.fromkeys(result["retrieved"]):
            print(f"  {heading}")
    for event in result["guardrail_events"]:
        print(f"[guardrail] {event}", file=sys.stderr)
    print(f"\n({result['model_calls']} model calls, {result['input_tokens']}+{result['output_tokens']} tokens, "
          f"{result['seconds']}s, {', '.join(result['models'])})", file=sys.stderr)


if __name__ == "__main__":
    main()
