"""
Assignment 3: the agent harness (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the tools of server.py over MCP and AGENTS.md as the
system prompt. Built from session 10's 07-own-harness/harness.py. Guardrails, all run by the
harness, so the model cannot skip them:

1. approval: add_document runs only after the person at the keyboard types "y"
2. call limits: at most 6 model calls and 4 tool calls per question (runaway loops)
3. citation check (the extra guardrail): every [citation] in the answer must be one that a search
   in this run returned, and an answer that is not a refusal must cite at least one passage.
   Otherwise the answer is withheld and replaced by a refusal. A wrong answer costs ~35 times a
   refusal (REPORT.md), so an answer that cannot show where it comes from is not worth showing.
   Runs that called add_document are exempt: the reply then reports the tool's own result.

evaluate.py imports build_agent(), load_mcp_tools() and ask().
"""

import asyncio
import os
import re
import sys
import time
import warnings
from contextlib import AsyncExitStack
from pathlib import Path

warnings.filterwarnings("ignore")  # beta and deprecation notices of langchain.mcp / langchain-google-genai

from langchain.agents import create_agent  # noqa: E402
from langchain.agents.middleware import ModelCallLimitMiddleware, ToolCallLimitMiddleware, wrap_tool_call  # noqa: E402
with warnings.catch_warnings():  # langchain.mcp re-enables its beta warning on import
    warnings.simplefilter("ignore")
    from langchain.mcp import MCPAdapter  # noqa: E402
    from fastmcp.client.transports import PythonStdioTransport  # noqa: E402
from langchain_core.messages import AIMessage, ToolMessage  # noqa: E402
from langchain_google_genai import ChatGoogleGenerativeAI  # noqa: E402

from api_key import load_api_key  # noqa: E402

ROOT = Path(__file__).resolve().parent
MODEL = "gemini-3.5-flash-lite"   # fast, cheap, generous free-tier quota (as in session 10)
SERVER = ROOT / "server.py"
NEEDS_APPROVAL = {"add_document"}  # changes the index everyone searches
REFUSAL = "The corpus does not cover this."
DECLINED = "The user refused this tool call. Do not try to add the document another way."
REFUSAL_PREFIX = "The corpus does not cover"  # also accepts "The corpus does not cover whether ..."
WITHHELD = (f"{REFUSAL} An answer was drafted, but it could not be traced to the passages the search "
            "returned, so it was withheld. Check the cited sources or ask the competent authority.")


# 1. Tools: start server.py over stdio and wrap its tools as LangChain tools.
async def load_mcp_tools(stack: AsyncExitStack, base_only: bool = False):
    """base_only: search only the original corpus (evaluate.py), not documents added later."""
    env = {**os.environ, "EUDR_BASE_ONLY": "1" if base_only else "0"}
    transport = PythonStdioTransport(SERVER, env=env, cwd=str(ROOT), python_cmd=sys.executable)
    adapter = await stack.enter_async_context(MCPAdapter(transport))
    return await adapter.list_tools()


# 2. Approval before add_document. Without a keyboard (check.py, evaluation) the answer is no.
def approval_guardrail(auto_approve: bool):
    @wrap_tool_call
    async def ask_before_adding(request, handler):
        call = request.tool_call
        if call["name"] in NEEDS_APPROVAL and not auto_approve:
            allowed = False
            if sys.stdin.isatty():
                try:
                    answer = input(f"  Allow {call['name']}({call['args']})? [y/N] ")
                except (EOFError, KeyboardInterrupt):  # Ctrl+D / Ctrl+C at the prompt counts as "no"
                    print(file=sys.stderr)
                    answer = ""
                allowed = answer.strip().lower() == "y"
            if not allowed:
                return ToolMessage(content=DECLINED, name=call["name"], tool_call_id=call["id"], status="error")
        return await handler(request)

    return ask_before_adding


def build_agent(tools, auto_approve: bool = False):
    load_api_key()
    return create_agent(
        model=ChatGoogleGenerativeAI(model=MODEL, temperature=0),
        tools=tools,
        system_prompt=(ROOT / "AGENTS.md").read_text(encoding="utf-8"),
        middleware=[
            approval_guardrail(auto_approve),
            ModelCallLimitMiddleware(run_limit=6, exit_behavior="end"),
            ToolCallLimitMiddleware(run_limit=4, exit_behavior="continue"),
        ],
    )


# 3. The citation check, on the final answer.
CITATION = re.compile(r"\[([^\[\]]{3,120})\]")


def retrieved_citations(trace: list[dict]) -> set[str]:
    return {key for step in trace if step["type"] == "result" for key in re.findall(r"Cite as: \[([^\]]+)\]", step["text"])}


def is_refusal(answer: str) -> bool:
    return answer.strip().startswith(REFUSAL_PREFIX)


def split_citations(bracket: str, sources: set[str]) -> list[str]:
    """'[Guidance §9; FAQ 1.3, p. 13]' -> ['Guidance §9', 'FAQ 1.3, p. 13']. Brackets naming no corpus
    document ('[HS 1806]') are not citations and are ignored."""
    starts = "|".join(re.escape(s) for s in sorted(sources, key=len, reverse=True))
    if not starts or not re.match(rf"\s*({starts})\b", bracket):
        return []
    parts = []
    for part in re.split(rf"[;,]\s*(?=(?:{starts})\b)", bracket):
        part = part.strip(" ,;`")
        # "EUDR Article 4(2), 12(1)–(2)": the bare number reuses the prefix ("EUDR Article ") of the first part
        pieces = re.split(r",\s*(?=\d)", part)
        prefix = re.match(r"^(.*?)\d", pieces[0])
        parts += [pieces[0]] + [(prefix.group(1) if prefix else "") + p for p in pieces[1:]]
    return [p for p in parts if p]


def normalise(citation: str) -> str:
    """Drop what the model may leave out: '(part 2/3)' labels and sub-points after a paragraph,
    'Article 2(13)(a)' -> 'Article 2(13)', 'FAQ 5.20 (part 1/2), p. 70' -> 'FAQ 5.20, p. 70'."""
    citation = re.sub(r"\s*\(part \d+/\d+\)", "", citation)
    citation = re.sub(r"(\(\d+[a-z]?\))(\([a-z]+\)|\([ivx]+\))+", r"\1", citation)
    return re.sub(r"\s+", " ", citation).strip(" `")


PARAGRAPHS = re.compile(r"^(.*?)\((\d+)\)(?:[–-]\((\d+)\))?$")


def is_retrieved(citation: str, allowed: set[str]) -> bool:
    """Is the citation one of the retrieved passages? Accepted forms of a retrieved key:
    exact; shortened ('FAQ 1.3' for 'FAQ 1.3, p. 13', 'EUDR Article 25' for 'EUDR Article 25(1)–(2)',
    but not 'EUDR Article 2'); a paragraph of a retrieved article ('EUDR Article 12(3)' for
    'EUDR Article 12' or for 'EUDR Article 12(1)–(4)')."""
    citation = normalise(citation)
    for key in {normalise(k) for k in allowed}:
        if key == citation or (key.startswith(citation) and key[len(citation)] in " (,"):
            return True
        if citation.startswith(key + "("):
            return True
        cited, held = PARAGRAPHS.match(citation), PARAGRAPHS.match(key)
        if cited and held and cited.group(1) == held.group(1):
            low, high = int(held.group(2)), int(held.group(3) or held.group(2))
            if low <= int(cited.group(2)) <= high and (cited.group(3) is None or int(cited.group(3)) <= high):
                return True
    return False


def check_citations(answer: str, trace: list[dict]) -> dict:
    """What the guardrail sees: is it a refusal, which citations are valid, which are not."""
    allowed = retrieved_citations(trace)
    sources = {key.split()[0] for key in allowed} | {"EUDR", "Guidance", "FAQ"}
    cited = [c for bracket in CITATION.findall(answer) for c in split_citations(bracket, sources)]
    invalid = [c for c in cited if not is_retrieved(c, allowed)]
    refusal = is_refusal(answer)
    passed = refusal and not invalid or (not refusal and cited and not invalid)
    return {"refusal": refusal, "cited": cited, "invalid": invalid, "passed": bool(passed)}


def tool_trace(messages) -> list[dict]:
    """Every tool call and its result, in order."""
    trace = []
    for message in messages:
        if isinstance(message, AIMessage):
            trace += [{"type": "call", "tool": c["name"], "args": c["args"]} for c in message.tool_calls]
        elif isinstance(message, ToolMessage):
            trace.append({"type": "result", "tool": message.name, "text": message.text})
    return trace


def add_document_report(trace: list[dict]) -> str:
    """What add_document did in this run, in plain words, straight from the tool (not from the model).
    The citation rule is for answers about the EUDR; an upload reply has nothing to cite."""
    lines = []
    for step in trace:
        if step["type"] == "result" and step["tool"] == "add_document":
            lines.append("Not added: you declined the add_document call." if step["text"].startswith(DECLINED)
                         else step["text"].strip())
    return "\n".join(lines)


def usage(messages) -> dict:
    totals = {"input_tokens": 0, "output_tokens": 0, "model_calls": 0}
    for message in messages:
        if isinstance(message, AIMessage) and message.usage_metadata:
            totals["input_tokens"] += message.usage_metadata.get("input_tokens", 0)
            totals["output_tokens"] += message.usage_metadata.get("output_tokens", 0)
            totals["model_calls"] += 1
    return totals


async def ask(agent, question: str, guardrail: bool = True) -> dict:
    """Run one question. Returns the final answer, the draft, the trace, the check, tokens and seconds."""
    started = time.time()
    result = await agent.ainvoke({"messages": [{"role": "user", "content": question}]})
    messages = result["messages"]
    draft = messages[-1].text if isinstance(messages[-1], AIMessage) else ""
    trace = tool_trace(messages)
    check = check_citations(draft, trace)
    answer = draft if (check["passed"] or not guardrail) else WITHHELD
    report = add_document_report(trace)
    if report:  # an upload run: show the tool's own result; keep the draft only if it is a cited answer
        answer = f"{report}\n\n{draft}" if check["passed"] and not check["refusal"] else report
    return {"answer": answer, "draft": draft, "trace": trace, "check": check,
            "withheld": answer == WITHHELD, "seconds": round(time.time() - started, 1), **usage(messages)}


def print_result(result: dict) -> None:
    for step in result["trace"]:
        if step["type"] == "call":
            print(f"  call {step['tool']}({step['args']})", file=sys.stderr)
    print(result["answer"])
    sources = [c for c in dict.fromkeys(result["check"]["cited"]) if c not in result["check"]["invalid"]]
    if sources and not result["withheld"]:
        print("\nSources:\n" + "\n".join(f"  [{c}]" for c in sources))
    if result["withheld"]:
        print(f"\n(Citation guardrail: draft withheld; invalid citations {result['check']['invalid'] or 'none'}, "
              f"cited {result['check']['cited'] or 'nothing'}.)", file=sys.stderr)
    print(f"\n({result['seconds']} s, {result['input_tokens']} input + {result['output_tokens']} output tokens, "
          f"{result['model_calls']} model calls)", file=sys.stderr)


async def main(question: str) -> None:
    async with AsyncExitStack() as stack:
        agent = build_agent(await load_mcp_tools(stack))
        result = await ask(agent, question)
    print_result(result)


if __name__ == "__main__":
    asyncio.run(main(" ".join(sys.argv[1:]) or "Which cocoa products fall under the EUDR?"))
