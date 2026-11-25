"""
Assignment 3: the agent harness (`main.py ask "question"` runs `python agent.py "question"`).

LangChain create_agent on Gemini, with search and add_document loaded from
server.py over MCP and AGENTS.md as system prompt. Three guardrails, all run
by the harness, so the model cannot skip them:
  1. approval: add_document runs only if the person at the keyboard types y;
  2. a model-call limit per question, against runaway loops;
  3. a citation check on the final answer: every [id] must be a passage search
     returned in this run, or the answer is withheld.

    uv run python agent.py "My flight was cancelled. What can I get?"
    uv run python agent.py --index-dir demo_index "..."      # serve a copy of the index
    uv run python agent.py --model-call-limit 1 "..."        # watch the call limit fire

evaluate.py imports load_mcp_tools, build_agent and ask.
"""

import argparse
import asyncio
import re
import sys
import time
import warnings
from contextlib import AsyncExitStack
from pathlib import Path

from fastmcp.client.transports import PythonStdioTransport
from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware, wrap_tool_call
from langchain_core.messages import AIMessage, ToolMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from api_key import load_api_key

with warnings.catch_warnings():
    warnings.simplefilter("ignore")  # langchain.mcp is in beta and warns on import
    from langchain.mcp import MCPAdapter

ROOT = Path(__file__).resolve().parent
MODEL = "gemini-3.5-flash-lite"  # assigned in the brief
SERVER = ROOT / "server.py"
INDEX_DIR = ROOT / "index"
AGENTS_FILE = ROOT / "AGENTS.md"
NEEDS_APPROVAL = {"add_document"}  # changes the index for everyone
MODEL_CALL_LIMIT = 8  # model calls per question; a normal answer needs 2 to 4

BRACKET = re.compile(r"\[([^\[\]]+)\]")
# A bracket token is a citation attempt if it starts like a CELEX number (e.g. 32004R0261, 52024XC05687) or a
# passage id; malformed attempts ("w16:1", a bare CELEX, "A:article-8") count, so they are checked, not skipped.
CITATION_LIKE = re.compile(r"^(?:\d{5}[A-Z]{1,2}\d{3,5}|[0-9A-Za-z]+:[A-Z]:)")
MARKERS = ("NOT IN CORPUS:", "NEED DETAILS:")
LIMIT_MESSAGE = "Model call limits exceeded"
DENIED_MESSAGE = "Not added: the user declined. Do not try another way."


# 1. Tools: start server.py over stdio; MCPAdapter wraps its tools as LangChain tools.
async def load_mcp_tools(stack, index_dir=INDEX_DIR):
    transport = PythonStdioTransport(
        SERVER, args=["--index-dir", str(index_dir)], cwd=str(ROOT),
        # the MCP client starts servers with a stripped env, so pass the key on
        env={"GEMINI_API_KEY": load_api_key()},
    )
    adapter = await stack.enter_async_context(MCPAdapter(transport))
    return await adapter.list_tools()


# 2. Guardrail 1: ask the person at the keyboard before add_document changes the index.
def ask_person(call):
    """Show the file and ask. No terminal, no answer, or anything but 'y' means no."""
    path = Path(str(call["args"].get("path", ""))).expanduser()
    shown = path if path.is_absolute() else ROOT / path
    print(f"\n  The agent wants to add this file to the index:\n    {shown}", file=sys.stderr)
    if not sys.stdin.isatty():
        print("  No terminal to ask for approval: denied.", file=sys.stderr)
        return False
    try:
        answer = input("  Allow add_document? [y/N] ")
    except EOFError:
        return False
    return answer.strip().lower() == "y"


def deny_all(call):
    """Approval policy for unattended runs such as evaluate.py: never add anything."""
    print(f"  add_document({call['args']}) denied: unattended run.", file=sys.stderr)
    return False


def approval_guardrail(approve):
    @wrap_tool_call
    async def ask_before_adding(request, handler):
        call = request.tool_call
        if call["name"] in NEEDS_APPROVAL and not approve(call):
            return ToolMessage(content=DENIED_MESSAGE, tool_call_id=call["id"], name=call["name"], status="error")
        return await handler(request)

    return ask_before_adding


# 3. The agent: model + tools + AGENTS.md + guardrails 1 and 2. create_agent runs the loop.
def build_agent(tools, approve=ask_person, model_call_limit=MODEL_CALL_LIMIT, model=None):
    return create_agent(
        model=model or ChatGoogleGenerativeAI(model=MODEL),
        tools=tools,
        system_prompt=AGENTS_FILE.read_text(encoding="utf-8"),  # sent on every model call
        middleware=[
            approval_guardrail(approve),
            ModelCallLimitMiddleware(run_limit=model_call_limit),  # hard stop for runaway loops
        ],
    )


def tool_trace(messages):
    """Every tool call and its result, in order: what the harness saw happen."""
    trace = []
    for message in messages:
        if isinstance(message, AIMessage):
            trace += [{"type": "call", "name": c["name"], "args": c["args"]} for c in message.tool_calls]
        elif isinstance(message, ToolMessage):
            trace.append({"type": "result", "name": message.name, "status": message.status, "text": message.text})
    return trace


def returned_passages(trace):
    """{passage id: passage text} for every passage search actually returned in this run."""
    passages = {}
    for step in trace:
        if step["type"] == "result" and step["name"] == "search" and step["status"] != "error":
            for block in step["text"].split("\n\n---\n\n"):
                match = re.match(r"^\[([^\]]+)\] ", block)
                if match:
                    passages[match.group(1)] = block
    return passages


# 4. Guardrail 3: an answer may only cite passages this run retrieved.
def extract_citations(answer):
    """Every citation attempt in the answer, in order: each id in each bracket, `[a, b]` and `[a; b]` included.

    The first version matched only a bracket holding exactly one well-formed id, so `[a, b]` brackets and
    malformed ids were silently skipped (found in the evaluation: q06 wrongly withheld; q11, q20, q27 let through).
    """
    cited = []
    for inside in BRACKET.findall(answer):
        for token in re.split(r"[,;]", inside):
            token = token.strip().strip("`'\"").strip()
            if CITATION_LIKE.match(token):
                cited.append(token)
    return list(dict.fromkeys(cited))


def check_citations(answer, passages):
    """(passed, reason). Code can check that citations are real; not that they support the claim."""
    cited = extract_citations(answer)
    unknown = [c for c in cited if c not in passages]
    if unknown:
        return False, f"it cites passages that search did not return: {', '.join(unknown)}"
    if not cited:
        if answer.lstrip().startswith(MARKERS):
            return True, "no citations, but a refusal or clarification marker"
        return False, "it makes claims without citing any retrieved passage"
    return True, "every citation is a passage returned in this run"


def token_usage(messages):
    """Summed token counts of the agent's model calls, or None if the provider reported none."""
    reports = [m.usage_metadata for m in messages if isinstance(m, AIMessage) and m.usage_metadata]
    if not reports:
        return None
    return {key: sum(r.get(key, 0) for r in reports) for key in ("input_tokens", "output_tokens", "total_tokens")}


async def ask(agent, question):
    """Run one question. Returns the answer shown to the user, the raw answer, trace, guardrails, usage, latency."""
    started = time.time()
    result = await agent.ainvoke({"messages": [{"role": "user", "content": question}]})
    messages = result["messages"]
    raw_answer = messages[-1].text.strip()
    trace = tool_trace(messages)
    passages = returned_passages(trace)
    passed, reason = check_citations(raw_answer, passages)
    answer = raw_answer if passed else f"WITHHELD: the harness blocked this answer because {reason}."
    return {
        "question": question,
        "answer": answer,
        "raw_answer": raw_answer,
        "trace": trace,
        "retrieved": passages,
        "cited_ids": extract_citations(raw_answer),
        "guardrails": {
            "citation_check": {"passed": passed, "reason": reason},
            "model_call_limit_hit": raw_answer.startswith(LIMIT_MESSAGE),
            "add_document_denied": any(s["type"] == "result" and s["text"] == DENIED_MESSAGE for s in trace),
        },
        "model_calls": sum(isinstance(m, AIMessage) for m in messages),
        "usage": token_usage(messages),
        "latency_s": round(time.time() - started, 2),
        "model": MODEL,
    }


def print_result(result):
    for step in result["trace"]:
        if step["type"] == "call":
            print(f"  call {step['name']}({step['args']})")
        else:
            ids = re.findall(r"^\[([^\]]+)\] ", step["text"], flags=re.M)
            print(f"  result {step['name']}: {', '.join(ids) if ids else step['text'][:200]}")
    for name, event in result["guardrails"].items():
        fired = event is True or (isinstance(event, dict) and not event["passed"])
        if fired:
            print(f"  guardrail fired: {name} {event if isinstance(event, dict) else ''}")
    print(f"\n{result['answer']}\n")
    if result["cited_ids"] and not result["answer"].startswith("WITHHELD"):
        print("Sources:")
        for cited in result["cited_ids"]:
            header = result["retrieved"][cited].split("\n")[:2]
            print(f"  [{cited}] {header[0].split('] ', 1)[1]} | {header[1].split(' | ')[0]}")


async def main(question, index_dir, model_call_limit):
    async with AsyncExitStack() as stack:
        agent = build_agent(await load_mcp_tools(stack, index_dir), model_call_limit=model_call_limit)
        result = await ask(agent, question)
    print_result(result)
    usage = result["usage"] or "unavailable"
    print(f"\n({result['model_calls']} model calls, {result['latency_s']} s, tokens: {usage})")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Ask the agent one question.")
    parser.add_argument("question", nargs="+")
    parser.add_argument("--index-dir", default=str(INDEX_DIR))
    parser.add_argument("--model-call-limit", type=int, default=MODEL_CALL_LIMIT)
    args = parser.parse_args()
    asyncio.run(main(" ".join(args.question), Path(args.index_dir).resolve(), args.model_call_limit))
