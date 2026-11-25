"""
Assignment 3: the food-safety agent for small restaurants (`uv run python main.py ask "question"`).

Built like session 10's harness.py: LangChain's create_agent on Gemini, the
tools of server.py over MCP, AGENTS.md as the system prompt, and guardrails as
middleware, which the model cannot skip because the harness runs them:

  1. approval: add_document runs only if the person at the keyboard types "y";
  2. call limit: at most 6 model calls per question (stops runaway loops); if it is
     reached, the answer is a refusal, because no cited answer was found in time;
  3. citation check (our extra guardrail): every [label] in the final answer must
     be one the search tool returned in this run, and an answer that is not a
     refusal must cite at least once. On failure the model gets one retry with
     the problem spelled out; if it fails again the answer is withheld.

evaluate.py imports build_agent(), load_tools() and ask().
"""

import asyncio
import sys
import time
import warnings
from contextlib import AsyncExitStack
from pathlib import Path

from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware, after_model, wrap_tool_call
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_google_genai import ChatGoogleGenerativeAI

warnings.filterwarnings("ignore", message=".*langchain.mcp.*beta")  # it works; the warning is noise
from langchain.mcp import MCPAdapter  # noqa: E402

from api_key import load_api_key
from retrieval import cites_in, cites_offered

ROOT = Path(__file__).resolve().parent
MODEL = "gemini-3.5-flash-lite"  # fast, cheap, generous free-tier quota (as in class)
SERVER = ROOT / "server.py"
NEEDS_APPROVAL = {"add_document"}  # changes the index every later answer depends on
MAX_MODEL_CALLS = 6

REFUSAL = "The FDA documents I have do not cover this."  # AGENTS.md asks for exactly this sentence
LIMIT_REACHED = REFUSAL + " (I searched several times without finding a passage that answers it.)"
WITHHELD = (
    "I could not back this answer with citations from the FDA documents, so I am not giving it. "
    "Please check the FDA Food Code directly or ask your local health department."
)


# 1. Tools: start server.py over stdio; MCPAdapter wraps its tools as LangChain tools.
async def load_tools(stack: AsyncExitStack):
    adapter = await stack.enter_async_context(MCPAdapter(SERVER))
    return await adapter.list_tools()


# 2. Approval before add_document. `approve` decides; the default asks at the keyboard.
def ask_at_keyboard(name: str, args: dict) -> bool:
    if not sys.stdin.isatty():
        print(f"  {name}({args}) needs approval, but nobody is at the keyboard: refused.", file=sys.stderr)
        return False
    return input(f"  Allow {name}({args})? [y/N] ").strip().lower() == "y"


def approval_guardrail(approve):
    @wrap_tool_call
    async def ask_before_changing_index(request, handler):
        call = request.tool_call
        if call["name"] in NEEDS_APPROVAL and not approve(call["name"], call["args"]):
            return ToolMessage(
                content="The user refused this tool call. Do not try to change the index another way.",
                tool_call_id=call["id"],
                status="error",
            )
        return await handler(request)

    return ask_before_changing_index


# 3. Citation check on the final answer.
def citation_problems(answer: str, offered: set[str]) -> list[str]:
    """What is wrong with the answer's citations; empty if nothing."""
    if REFUSAL.lower() in answer.lower() and not cites_in(answer):
        return []  # a plain refusal needs no citation
    cited = cites_in(answer)
    if not cited:
        return ["the answer cites nothing"]
    return [f"[{c}] was not returned by the search tool" for c in cited if c not in offered]


def offered_labels(messages) -> set[str]:
    return {label for m in messages if isinstance(m, ToolMessage) for label in cites_offered(m.text)}


@after_model(can_jump_to=["model"])
def citation_guardrail(state, runtime):
    last = state["messages"][-1]
    if not isinstance(last, AIMessage) or last.tool_calls:
        return None  # not the final answer yet
    problems = citation_problems(last.text, offered_labels(state["messages"]))
    if not problems:
        return None
    already_retried = any(getattr(m, "name", None) == "citation_guardrail" for m in state["messages"])
    if not already_retried:
        note = HumanMessage(
            name="citation_guardrail",
            content=(
                "Citation check failed: " + "; ".join(problems) + ". Rewrite the answer: cite every fact "
                "with a label exactly as the search tool gave it, search again if needed, or reply with "
                f'"{REFUSAL}" if the passages do not answer the question.'
            ),
        )
        return {"messages": [note], "jump_to": "model"}
    return {"messages": [AIMessage(content=WITHHELD, name="citation_guardrail")]}


# The agent: model + tools + AGENTS.md + guardrails. create_agent runs the loop.
def build_agent(tools, approve=ask_at_keyboard):
    load_api_key()  # puts GEMINI_API_KEY in the environment for langchain-google-genai
    return create_agent(
        model=ChatGoogleGenerativeAI(model=MODEL),
        tools=tools,
        system_prompt=(ROOT / "AGENTS.md").read_text(encoding="utf-8"),
        middleware=[
            approval_guardrail(approve),
            citation_guardrail,
            ModelCallLimitMiddleware(run_limit=MAX_MODEL_CALLS),
        ],
    )


def tool_trace(messages) -> list[str]:
    """Every tool call and its result, in order: what the harness saw happen."""
    lines = []
    for message in messages:
        if isinstance(message, AIMessage):
            lines += [f"call {c['name']}({c['args']})" for c in message.tool_calls]
        elif isinstance(message, ToolMessage):
            lines.append(f"result {message.text}")
    return lines


async def ask(agent, question: str) -> dict:
    """Run one question. Returns the answer, the tool trace and what it cost."""
    started = time.time()
    result = await agent.ainvoke({"messages": [{"role": "user", "content": question}]})
    messages = result["messages"]
    ai = [m for m in messages if isinstance(m, AIMessage)]
    usage = [m.usage_metadata or {} for m in ai]
    fired = any(getattr(m, "name", None) == "citation_guardrail" for m in messages)
    withheld = isinstance(messages[-1], AIMessage) and messages[-1].name == "citation_guardrail"
    answer = messages[-1].text.strip()
    # ModelCallLimitMiddleware ends the run with its own message ("Model call limits
    # exceeded: ..."); the user must never see that, and there is no cited answer to give.
    limit_hit = answer.startswith("Model call limits exceeded")
    if limit_hit:
        answer = LIMIT_REACHED
    return {
        "answer": answer,
        "call_limit_hit": limit_hit,
        "trace": tool_trace(messages),
        "tool_results": [m.text for m in messages if isinstance(m, ToolMessage)],
        "offered_cites": sorted(offered_labels(messages)),
        "guardrail_fired": fired,
        "guardrail_withheld": withheld,
        "first_answer": next((m.text for m in ai if not m.tool_calls), ""),
        "model_calls": len(ai),
        "input_tokens": sum(u.get("input_tokens", 0) for u in usage),
        "output_tokens": sum(u.get("output_tokens", 0) for u in usage),
        "seconds": round(time.time() - started, 2),
    }


def sources_footer(result: dict) -> str:
    """'Sources:' with the document and location of every label the answer cites."""
    where = {}
    for output in result["tool_results"]:
        for block in output.split("\n\n"):
            lines = block.splitlines()
            if len(lines) >= 2 and lines[0].startswith("[") and "Cite as: [" in lines[0]:
                label = cites_offered(lines[0])[0]
                where.setdefault(label, lines[1].removeprefix("Source: "))
    cited = list(dict.fromkeys(cites_in(result["answer"])))
    if not cited:
        return ""
    return "\nSources:\n" + "\n".join(f"  [{c}] {where.get(c, '')}" for c in cited)


async def main(question: str) -> None:
    async with AsyncExitStack() as stack:
        agent = build_agent(await load_tools(stack))
        result = await ask(agent, question)
    for line in result["trace"]:
        print("  " + (line if len(line) < 160 else line[:157] + "..."))
    if result["call_limit_hit"]:
        print(f"  [call limit of {MAX_MODEL_CALLS} model calls reached: answered with a refusal]")
    if result["guardrail_fired"]:
        print("  [citation guardrail fired" + (": answer withheld]" if result["guardrail_withheld"] else ": retried]"))
    print()
    print(result["answer"])
    print(sources_footer(result))
    print(
        f"\n({result['model_calls']} model calls, {result['input_tokens']:,} input + "
        f"{result['output_tokens']:,} output tokens, {result['seconds']} s)"
    )


if __name__ == "__main__":
    asyncio.run(main(" ".join(sys.argv[1:]) or "What temperature must I keep hot food at until the driver picks it up?"))
