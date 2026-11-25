import asyncio
import json
import math
import re
import sys
import time
from contextlib import AsyncExitStack
from pathlib import Path

from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware, wrap_tool_call
from langchain_core.messages import AIMessage, ToolMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from api_key import load_api_key
from index import SOURCES, collection
from retrieval import DESIGN
from langchain.mcp import MCPAdapter

MODEL = "gemini-3.5-flash-lite"
SERVER = Path("server.py")
NEEDS_APPROVAL = {"add_document"}  # changes the index
MAX_MODEL_CALLS = 6  # stops loops
FIT_TEMPERATURE = 0.02

# quote and its [chunk_id]
QUOTE = re.compile(r'"((?:[^"\n\\]|\\.)+)"\s*(\[[\w-]+\])?')

BASE_COVERS = (
    "Mill, On Liberty ch. I-II; Marx and Engels, Communist Manifesto; Paine, Agrarian Justice; "
    "Bastiat, That Which Is Seen, and That Which Is Not Seen; Smith, Wealth of Nations Book I ch. II and Book IV ch. II"
)


def covers():
    base = {s["id"] for s in SOURCES if not s.get("held_back")}
    added = {m["source"]: f"{m['author']}, {m['work']}" for m in collection(DESIGN).get(include=["metadatas"])["metadatas"] if m["source"] not in base}
    return BASE_COVERS + "".join(f"; {work}" for work in sorted(added.values()))


def refusal():
    return f"- **Verdict:** not in these texts\n- **Answer:** No passage in the corpus addresses this. The corpus covers only {covers()}."


async def load_mcp_tools(stack):
    adapter = await stack.enter_async_context(MCPAdapter(SERVER))
    return await adapter.list_tools()


# guardrail: approve add_document
def approval_guardrail(auto_approve):
    @wrap_tool_call
    async def ask_before_adding(request, handler):
        call = request.tool_call
        if call["name"] in NEEDS_APPROVAL and not auto_approve:
            try:
                answer = input(f"  Allow {call['name']}({call['args']})? [y/N] ")
            except EOFError:  # nobody at keyboard: refuse
                answer = ""
            if answer.strip().lower() != "y":
                return ToolMessage(
                    content="The user refused this tool call. Do not try to add the document another way.",
                    tool_call_id=call["id"],
                    status="error",
                )
        return await handler(request)

    return ask_before_adding


def build_agent(tools, auto_approve=False):
    load_api_key()
    return create_agent(
        model=ChatGoogleGenerativeAI(model=MODEL),
        tools=tools,
        system_prompt=Path("AGENTS.md").read_text(encoding="utf-8"),
        middleware=[approval_guardrail(auto_approve), ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS)],
    )


def passages_of(messages):
    found = {}
    for message in messages:
        if isinstance(message, ToolMessage) and message.name == "search":
            try:
                found.update({p["chunk_id"]: p for p in json.loads(message.text)})
            except (json.JSONDecodeError, TypeError):
                pass
    return found


def tool_trace(messages):
    lines = []
    for message in messages:
        if isinstance(message, AIMessage):
            lines += [f"call {c['name']}({c['args']})" for c in message.tool_calls]
        elif isinstance(message, ToolMessage):
            try:
                lines.append("result " + ", ".join(p["chunk_id"] for p in json.loads(message.text)))
            except (json.JSONDecodeError, TypeError, KeyError):
                lines.append(f"result {message.text[:200]}")
    return lines


def words(text):
    return " ".join(re.findall(r"[a-z0-9]+", text.lower()))


# guardrail: quotes word for word
def check_quotes(answer, passages):
    removed = []

    def check(match):
        quote, cited = match.group(1), (match.group(2) or "").strip("[]")
        titles = {words(p["work"]) for p in passages.values()}
        if not cited and (len(quote.split()) < 5 or words(quote) in titles):
            return match.group(0)
        text = words(passages.get(cited, {}).get("text", ""))
        # each piece around ... must match
        pieces = [words(p) for p in re.split(r"\.\.\.|…", quote) if words(p)]
        if text and all(piece in text for piece in pieces):
            return match.group(0)
        removed.append(match.group(0))
        return f"[quote removed: not found word for word in {cited or 'a cited passage'}]"

    return QUOTE.sub(check, answer), removed


def is_refusal(answer):
    return bool(re.search(r"verdict:?\**\s*not in these texts", answer, re.IGNORECASE))


def fit_scores(passages):
    best = {}
    for p in passages.values():
        best[p["author"]] = max(best.get(p["author"], 0), p["similarity"])
    top = sorted(best.items(), key=lambda item: -item[1])[:2]
    weights = {author: math.exp(similarity / FIT_TEMPERATURE) for author, similarity in top}
    return {author: round(100 * w / sum(weights.values())) for author, w in weights.items()}


async def ask(agent, question):
    started = time.time()
    result = await agent.ainvoke({"messages": [{"role": "user", "content": question}]})
    messages = result["messages"]
    passages = passages_of(messages)
    model_answer = messages[-1].text
    answer, removed = check_quotes(model_answer, passages)
    if is_refusal(answer):
        answer = refusal()  # model cannot add memory
    usage = [m.usage_metadata or {} for m in messages if isinstance(m, AIMessage)]
    return {
        "answer": answer,
        "model_answer": model_answer,
        "removed_quotes": removed,
        "trace": tool_trace(messages),
        "passages": passages,
        "fit": fit_scores(passages),
        "tokens": sum(u.get("total_tokens", 0) for u in usage),
        "seconds": round(time.time() - started, 1),
    }


async def main(question):
    async with AsyncExitStack() as stack:
        agent = build_agent(await load_mcp_tools(stack))
        result = await ask(agent, question)
    print("\n".join(f"  {line}" for line in result["trace"]))
    print()
    print(result["answer"])
    if result["fit"] and not is_refusal(result["answer"]):
        shares = " / ".join(f"{author} {share}%" for author, share in result["fit"].items())
        print(f"\nFit: {shares} (closeness to the passages, not who is right)")
    if result["removed_quotes"]:
        print(f"Guardrail: removed {len(result['removed_quotes'])} quote(s) not found word for word: {result['removed_quotes']}")
    if is_refusal(result["answer"]) and result["answer"] != result["model_answer"]:
        print(f"\nGuardrail: refusal written by the harness. The model had written:\n{result['model_answer']}")
    print(f"({result['tokens']} tokens, {result['seconds']} s)")


if __name__ == "__main__":
    asyncio.run(main(" ".join(sys.argv[1:]) or "Did Adam Smith say that greed is good?"))
