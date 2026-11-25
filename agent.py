"""Assignment 3: the corpus agent (`main.py ask "question"` runs `python agent.py "question"`).

Built like the lab's 07-own-harness/harness.py: Gemini through LangChain's create_agent, the tools of
our MCP server (server.py) through MCPAdapter, AGENTS.md as system prompt, and guardrails as middleware:
  - approval before add_document (it changes the shared index), auto-approved only for evaluation;
  - ModelCallLimitMiddleware against runaway loops;
  - an output check: every location the answer cites must be covered by a chunk retrieved in this run.
    If not, the agent is asked once to fix it; if it still fails, the answer is flagged. Every firing
    is logged to stderr and eval/guardrail_log.jsonl.
ask() returns the answer and the tool trace, plus tokens, seconds and the guardrail outcome for evaluate.py.
"""

import asyncio
import json
import os
import re
import sys
import time
from contextlib import AsyncExitStack
from datetime import datetime, timezone
from pathlib import Path

from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware, wrap_tool_call
from langchain_core.messages import AIMessage, HumanMessage, ToolMessage
from langchain_google_genai import ChatGoogleGenerativeAI

from langchain.mcp import MCPAdapter  # langchain.mcp is in beta and warns on import
from fastmcp.client.transports import PythonStdioTransport

from api_key import load_api_key
from evaluate import covers, parse_location
import index

ROOT = Path(__file__).resolve().parent
MODEL = "gemini-3.8-flash"
SERVER = ROOT / "server.py"
NEEDS_APPROVAL = {"add_document"}  # changes the shared index
MODEL_CALL_LIMIT = 10  # a three-part question needs ~4 calls (3 searches + answer); 10 leaves room, stops loops
GUARDRAIL_LOG = ROOT / "eval" / "guardrail_log.jsonl"


# 1. Tools: start our MCP server; MCPAdapter wraps its tools as LangChain tools (as .mcp.json does for the editor).
async def load_mcp_tools(stack):
    adapter = await stack.enter_async_context(MCPAdapter(PythonStdioTransport(SERVER, env=dict(os.environ))))
    return await adapter.list_tools()


# 2. Guardrail around the tools: ask the person at the keyboard before add_document changes the index.
#    The model cannot skip it, because the harness runs it, not the model.
def approval_guardrail(auto_approve, auto_deny=False):
    @wrap_tool_call
    async def ask_before_changing_index(request, handler):
        call = request.tool_call
        if call["name"] in NEEDS_APPROVAL:
            if auto_deny:  # evaluation: the index must not change, and nobody is at the keyboard
                print(f"  [approval] {call['name']} denied automatically (evaluation)", file=sys.stderr, flush=True)
                return ToolMessage(
                    content="Adding documents is disabled in this session. Do not try to add the document another way.",
                    tool_call_id=call["id"],
                    status="error",
                )
            if auto_approve:
                print(f"  [approval] {call['name']}({call['args']}) approved automatically", file=sys.stderr, flush=True)
            else:
                answer = input(f"  Allow {call['name']}({call['args']})? [y/N] ")
                if answer.strip().lower() != "y":
                    return ToolMessage(
                        content="The user refused this tool call. Do not try to add the document another way.",
                        tool_call_id=call["id"],
                        status="error",
                    )
        return await handler(request)

    return ask_before_changing_index


# 3. The agent: model + tools + standing rules + guardrails. create_agent runs the loop.
def build_agent(tools, auto_approve=False, auto_deny=False):
    load_api_key()  # puts GEMINI_API_KEY into the environment for langchain-google-genai
    return create_agent(
        model=ChatGoogleGenerativeAI(model=MODEL),
        tools=tools,
        system_prompt=(ROOT / "AGENTS.md").read_text(encoding="utf-8"),
        middleware=[
            approval_guardrail(auto_approve, auto_deny),
            ModelCallLimitMiddleware(run_limit=MODEL_CALL_LIMIT),
        ],
    )


def tool_trace(messages):
    """Every tool call and its result, in order: what the harness saw happen."""
    lines = []
    for message in messages:
        if isinstance(message, AIMessage):
            lines += [f"call {c['name']}({c['args']})" for c in message.tool_calls]
        elif isinstance(message, ToolMessage):
            lines.append(f"result {message.text}")
    return lines


# 4. Output guardrail: are the cited locations in the chunks this run retrieved?

STATUTES = "BGB|BetrKV|HeizkostenV|CO2KostAufG"
RN_LIST = r"\d+(?:\s*[–-]\s*\d+)?(?:\s*,\s*\d+(?:\s*[–-]\s*\d+)?)*"
CITATION = re.compile(
    rf"BGH VIII ZR \d+/\d+,\s*(?:Leitsatz|Rn\.\s*{RN_LIST})"
    rf"|(?:§§?\s*\d+[a-z]?(?:\s*[–-]\s*\d+[a-z]?)?(?:\s+Abs\.\s*\d+[a-z]?)?(?:\s+(?:Satz|S\.)\s*\d+)?(?:\s+Halbs\.\s*\d+)?"
    rf"(?:\s+Nr\.\s*\d+[a-z]?(?:\s*[–-]\s*\d+[a-z]?)?)?(?:\s+[a-c](?=\s))?|Anlage|Anhang EV)\s+(?:{STATUTES})\b"
)
CASE = re.compile(r"VIII ZR \d+/\d+")


def tool_texts(messages) -> list[str]:
    return [m.text for m in messages if isinstance(m, ToolMessage)]


def retrieved_locations(texts: list[str]) -> list[str]:
    """Locations of the chunks returned by search ('[1] BGH VIII ZR 62/19, Leitsatz'), in order, without repeats."""
    return list(dict.fromkeys(m.group(1).strip() for t in texts for m in re.finditer(r"^\[\d+\] (.+)$", t, re.M)))


def chunk_lookup() -> dict[str, dict]:
    """Every stored chunk by location: its metadata plus 'text'."""
    got = index.get_collection().get(include=["metadatas", "documents"])
    return {m["location"]: {**m, "text": d} for m, d in zip(got["metadatas"], got["documents"])}


def _rns(spec: str) -> set[str]:
    out = set()
    for part in spec.split(","):
        a, _, b = part.strip().replace("–", "-").partition("-")
        out |= {str(n) for n in range(int(a), int(b or a) + 1)}
    return out


def citation_ok(cited: str, chunks: list[dict]) -> bool:
    cited = " ".join(cited.split())
    if any(c["location"] == cited for c in chunks):
        return True
    if m := re.match(r"(BGH VIII ZR \d+/\d+),\s*(Leitsatz|Rn\.\s*(.+))$", cited):
        keys = {k for c in chunks if c["doc_id"] == m.group(1) for k in c["covers"].strip("|").split("|")}
        needed = {"Leitsatz"} if m.group(2) == "Leitsatz" else {f"Rn. {n}" for n in _rns(m.group(3))}
        return needed <= keys
    simple = re.sub(r"\s+(?:Satz|S\.|Halbs\.)\s*\d+", "", cited)  # chunks never split below Abs./Nr.
    simple = re.sub(r"(Nr\.\s*\d+[a-z]?)\s+[a-c](?=\s)", r"\1", simple)  # Nr. 15 b -> Nr. 15
    try:
        target = parse_location(simple)
    except ValueError:
        return False
    return any(covers(c, target) for c in chunks)


def check_citations(answer: str, messages) -> list[str]:
    return check_citations_in(answer, tool_texts(messages))


def check_citations_in(answer: str, texts: list[str], lookup: dict | None = None) -> list[str]:
    """Cited locations (and bare case numbers) not backed by a chunk the search tool returned (texts = tool results)."""
    lookup = lookup if lookup is not None else chunk_lookup()
    chunks = [lookup[loc] for loc in retrieved_locations(texts) if loc in lookup]
    problems = [c for c in dict.fromkeys(m.group(0) for m in CITATION.finditer(answer)) if not citation_ok(c, chunks)]
    retrieved_cases = {c["doc_id"].removeprefix("BGH ") for c in chunks}
    problems += [f"BGH {case} (not retrieved)" for case in dict.fromkeys(CASE.findall(answer))
                 if case not in retrieved_cases and not any(case in p for p in problems)]
    return problems


def log_guardrail(question, stage, problems):
    entry = {"time": datetime.now(timezone.utc).isoformat(timespec="seconds"), "question": question,
             "stage": stage, "unverified": problems}
    print(f"  [citation guardrail] {stage}: {problems}", file=sys.stderr, flush=True)
    GUARDRAIL_LOG.parent.mkdir(exist_ok=True)
    with GUARDRAIL_LOG.open("a", encoding="utf-8") as f:
        f.write(json.dumps(entry, ensure_ascii=False) + "\n")


def usage(messages) -> dict:
    calls = [m for m in messages if isinstance(m, AIMessage)]
    meta = [m.usage_metadata or {} for m in calls]
    return {"model_calls": len(calls), "input_tokens": sum(u.get("input_tokens", 0) for u in meta),
            "output_tokens": sum(u.get("output_tokens", 0) for u in meta)}


async def ask(agent, question):
    """Run one question. Returns (answer, tool trace, stats) where stats holds tokens, seconds and the guardrail."""
    started = time.time()
    result = await agent.ainvoke({"messages": [{"role": "user", "content": question}]})
    messages, answer = result["messages"], result["messages"][-1].text
    guardrail = {"fired": False, "fixed": None, "unverified": []}

    problems = check_citations(answer, messages)
    if problems:
        guardrail["fired"] = True
        log_guardrail(question, "fired, asking the agent to fix", problems)
        fix = HumanMessage(
            "Citation check failed: these citations are not covered by the passages the search tool returned in "
            f"this conversation: {'; '.join(problems)}. Rewrite the answer citing only locations exactly as "
            "search returned them. Search again if you need a passage, or drop the claim."
        )
        result = await agent.ainvoke({"messages": messages + [fix]})
        messages, answer = result["messages"], result["messages"][-1].text
        problems = check_citations(answer, messages)
        guardrail["fixed"] = not problems
        if problems:
            guardrail["unverified"] = problems
            log_guardrail(question, "still unverified after one retry, answer flagged", problems)
            answer += ("\n\n⚠ Citation check: these citations could not be matched to the retrieved passages, "
                       f"verify them before relying on this answer: {'; '.join(problems)}")
        else:
            log_guardrail(question, "fixed on retry", [])

    stats = {**usage(messages), "seconds": round(time.time() - started, 1), "guardrail": guardrail}
    return answer, tool_trace(messages), stats


def short(line: str) -> str:
    """Trace line for the terminal: search results reduced to the German query and the cited locations."""
    if line.startswith("result German search query:"):
        query = line.splitlines()[0].removeprefix("result ")
        locations = re.findall(r"^\[\d+\] (.+)$", line, re.M)
        return f"result {query}\n         " + " | ".join(locations)
    return line if len(line) < 400 else line[:400] + " …"


async def main(question, auto_approve=False):
    async with AsyncExitStack() as stack:
        agent = build_agent(await load_mcp_tools(stack), auto_approve=auto_approve)
        answer, trace, stats = await ask(agent, question)
    print("\n".join(f"  {short(line)}" for line in trace))
    print(f"  ({stats['model_calls']} model calls, {stats['input_tokens']:,} input + {stats['output_tokens']:,} "
          f"output tokens, {stats['seconds']} s)\n")
    print(answer)


if __name__ == "__main__":
    asyncio.run(main(" ".join(sys.argv[1:]) or "Can I pass the cost of felling a rotten tree on to my tenants?"))
