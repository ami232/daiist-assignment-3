"""
Assignment 3: the agent (`main.py ask "question"` runs `python agent.py "question"`).

LangChain `create_agent` on Gemini, with the tools of server.py over MCP (stdio) and
AGENTS.md as system prompt.

Harness:
- approval: add_document pauses for a human decision (HumanInTheLoopMiddleware);
  without an interactive terminal it is rejected.
- call limit: at most MAX_SEARCHES search calls per question (ToolCallLimitMiddleware).
- guardrail (citation check): every [source_id, location] in the answer must match a
  passage that search actually returned in this run. An answer with an invented or
  missing citation is sent back once with the problem; if it still fails, it is
  replaced by a refusal.

For evaluate.py:  `async with Harness() as h: result = await h.ask(question)`, or
`run(question)` for a single question. Both return the answer, the tool trace,
citations, token counts and seconds.
"""

from __future__ import annotations

import asyncio
import os
import re
import sys
import time
import uuid
from contextlib import AsyncExitStack
from pathlib import Path

ROOT = Path(__file__).resolve().parent
MODEL = os.environ.get("GEMINI_CHAT_MODEL", "gemini-3.5-flash-lite")
MAX_SEARCHES = 4
REFUSAL = "I can't answer this from my sources."
SYSTEM_PROMPT = (ROOT / "AGENTS.md").read_text(encoding="utf-8")

CITATION_RE = re.compile(r"\[([a-z0-9_]+),\s*([^\]]+?)\]")
HEADER_RE = re.compile(r"^\[\d+\] source_id: (\S+) \| location: (.+?) \| similarity: [\d.]+$")
BASE_LABEL_RE = re.compile(r"^(Preamble|Article \d+[a-z]?|Recital \(\d+\)|Section \d+(?:\.\d+)*|Annex(?: [IVX]+)?)",
                           re.IGNORECASE)


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


# --------------------------------------------------------------------------- citations

def base_label(label: str) -> str:
    """'Article 7(1)(b)' -> 'article 7', 'Article 5 (part 1/2)' -> 'article 5'."""
    label = " ".join(label.split())
    m = BASE_LABEL_RE.match(label)
    return (m.group(1) if m else label).lower()


def retrieved_passages(trace: list[dict]) -> dict[tuple[str, str], str]:
    """(source_id, base section label) -> url, for every passage search returned."""
    allowed = {}
    for call in trace:
        if call["tool"] != "search":
            continue
        source = url = None
        for line in call["output"].splitlines():
            if m := HEADER_RE.match(line):
                source, location = m.groups()
                allowed[(source, base_label(location))] = ""
                allowed[(source, location.lower())] = ""
            elif source and line.startswith("sections: "):
                for label in line[len("sections: "):].split("; "):
                    allowed[(source, base_label(label))] = ""
            elif source and line.startswith("url: "):
                url = line[len("url: "):].strip()
                for key in allowed:
                    if key[0] == source and not allowed[key]:
                        allowed[key] = url
    return allowed


def check_citations(answer: str, trace: list[dict]) -> dict:
    """Code check of the answer: is it a refusal, which citations does it make, are they all retrieved?"""
    allowed = retrieved_passages(trace)
    cited = [(s, loc.strip()) for s, loc in CITATION_RE.findall(answer)]
    invalid = [c for c in cited
               if (c[0], c[1].lower()) not in allowed and (c[0], base_label(c[1])) not in allowed]
    refusal = answer.strip().startswith(REFUSAL)
    problems = []
    if invalid:
        problems.append("these citations are not in the passages you retrieved: "
                        + ", ".join(f"[{s}, {loc}]" for s, loc in invalid))
    if not cited and not refusal:
        problems.append("the answer has no citations")
    return {"refusal": refusal, "citations": cited, "invalid": invalid, "problems": problems,
            "urls": {f"{s}, {loc}": allowed.get((s, base_label(loc)), "") for s, loc in cited}}


# --------------------------------------------------------------------------- MCP tools

def mcp_tools(session, tools) -> list:
    """Wrap the MCP server's tools as LangChain tools that call it over the open session."""
    from langchain_core.tools import StructuredTool

    def make(tool):
        async def call(**kwargs) -> str:
            result = await session.call_tool(tool.name, kwargs)
            return "\n".join(getattr(c, "text", "") for c in result.content)
        return StructuredTool(name=tool.name, description=tool.description or "",
                              args_schema=tool.input_schema, coroutine=call)

    return [make(t) for t in tools]


def cli_approve(name: str, args: dict) -> bool:
    """Ask the person at the terminal; with no terminal (check.py, evaluate.py) say no."""
    if not sys.stdin.isatty():
        log(f"[approval] {name}({args}) rejected: no interactive terminal to ask.")
        return False
    sys.stderr.write(f"\nThe agent wants to run {name} with {args}.\nAllow it? [y/N] ")
    sys.stderr.flush()
    return sys.stdin.readline().strip().lower() in {"y", "yes", "s", "si", "sí"}


# --------------------------------------------------------------------------- harness

class Harness:
    def __init__(self, approve=cli_approve, model: str = MODEL, server_env: dict | None = None):
        self.approve = approve
        self.model_name = model
        self.server_env = server_env or {}

    async def __aenter__(self) -> "Harness":
        from langchain.agents import create_agent
        from langchain.agents.middleware import HumanInTheLoopMiddleware, ToolCallLimitMiddleware
        from langchain_google_genai import ChatGoogleGenerativeAI
        from langgraph.checkpoint.memory import InMemorySaver
        from mcp import ClientSession, StdioServerParameters
        from mcp.client.stdio import get_default_environment, stdio_client

        from api_key import load_api_key

        load_api_key()
        self._stack = AsyncExitStack()
        try:
            params = StdioServerParameters(command=sys.executable, args=[str(ROOT / "server.py")], cwd=str(ROOT),
                                            env={**get_default_environment(), **self.server_env})
            read, write = await self._stack.enter_async_context(stdio_client(params))
            session = await self._stack.enter_async_context(ClientSession(read, write))
            await session.initialize()
            tools = mcp_tools(session, (await session.list_tools()).tools)
            model = ChatGoogleGenerativeAI(model=self.model_name, max_retries=6)
            self.agent = create_agent(
                model,
                tools=tools,
                system_prompt=SYSTEM_PROMPT,
                middleware=[
                    HumanInTheLoopMiddleware(
                        interrupt_on={"add_document": {"allowed_decisions": ["approve", "reject"]}}),
                    ToolCallLimitMiddleware(tool_name="search", run_limit=MAX_SEARCHES),
                ],
                checkpointer=InMemorySaver(),
            )
        except BaseException:
            await self._stack.aclose()  # stop the server process, or the error turns into a hang
            raise
        return self

    async def __aexit__(self, *exc) -> None:
        await self._stack.aclose()

    async def _invoke(self, payload, config: dict) -> None:
        """Run the agent until it finishes, answering approval pauses on the way."""
        from langgraph.types import Command

        await self.agent.ainvoke(payload, config)
        while True:
            state = await self.agent.aget_state(config)
            if not state.interrupts:
                return
            decisions = []
            for request in state.interrupts[0].value["action_requests"]:
                ok = self.approve(request["name"], request["args"])
                decisions.append({"type": "approve"} if ok else
                                 {"type": "reject", "message": "The user did not approve adding this document."})
            await self.agent.ainvoke(Command(resume={"decisions": decisions}), config)

    async def ask(self, question: str) -> dict:
        from langchain_core.messages import AIMessage, ToolMessage

        config = {"configurable": {"thread_id": str(uuid.uuid4())}}
        started = time.time()
        await self._invoke({"messages": [{"role": "user", "content": question}]}, config)
        answer, trace, check = self._read(await self.agent.aget_state(config), AIMessage, ToolMessage)
        guardrail = "passed"
        rejected = []  # drafts the citation check sent back, with the reason (for the report)
        if any(t["tool"] == "add_document" for t in trace):
            guardrail = "skipped (add_document request, not a question to answer from sources)"
        elif check["problems"]:
            rejected.append({"draft": answer, "problems": check["problems"]})
            log(f"[guardrail] {'; '.join(check['problems'])}. Asking for a corrected answer.")
            feedback = (f"Your answer was rejected by the citation check: {'; '.join(check['problems'])}. "
                        f"Rewrite it citing only [source_id, section] pairs from your search results, "
                        f"or start with '{REFUSAL}' if they do not answer the question.")
            await self._invoke({"messages": [{"role": "user", "content": feedback}]}, config)
            answer, trace, check = self._read(await self.agent.aget_state(config), AIMessage, ToolMessage)
            guardrail = "corrected"
            if check["problems"]:
                rejected.append({"draft": answer, "problems": check["problems"]})
                guardrail = "replaced"
                answer = f"{REFUSAL} (A draft answer was withheld because its citations could not be verified.)"
                check = check_citations(answer, trace)
        messages = (await self.agent.aget_state(config)).values["messages"]
        usage = [m.usage_metadata for m in messages if isinstance(m, AIMessage) and m.usage_metadata]
        return {
            "question": question,
            "answer": answer,
            "refusal": check["refusal"],
            "citations": [f"{s}, {loc}" for s, loc in check["citations"]],
            "urls": check["urls"],
            "guardrail": guardrail,
            "rejected_drafts": rejected,
            "trace": trace,
            "searches": sum(1 for t in trace if t["tool"] == "search"),
            "input_tokens": sum(u.get("input_tokens", 0) for u in usage),
            "output_tokens": sum(u.get("output_tokens", 0) for u in usage),
            "model_calls": len(usage),
            "seconds": round(time.time() - started, 1),
        }

    @staticmethod
    def _read(state, AIMessage, ToolMessage):
        """Final answer, tool trace and citation check from the conversation so far."""
        messages = state.values["messages"]
        calls = {}
        trace = []
        for m in messages:
            if isinstance(m, AIMessage):
                for c in m.tool_calls:
                    calls[c["id"]] = c
            elif isinstance(m, ToolMessage):
                call = calls.get(m.tool_call_id, {})
                trace.append({"tool": m.name or call.get("name", ""), "args": call.get("args", {}),
                              "output": m.text if hasattr(m, "text") else str(m.content)})
        last = next((m for m in reversed(messages) if isinstance(m, AIMessage) and not m.tool_calls), None)
        answer = (last.text if last is not None else "").strip()
        return answer, trace, check_citations(answer, trace)


def run(question: str, approve=cli_approve) -> dict:
    async def go():
        async with Harness(approve=approve) as h:
            return await h.ask(question)
    return asyncio.run(go())


def main() -> int:
    if len(sys.argv) < 2:
        print('Usage: python agent.py "your question"', file=sys.stderr)
        return 2
    result = run(" ".join(sys.argv[1:]))
    print(result["answer"])
    if result["citations"]:
        print("\nSources:")
        for c in dict.fromkeys(result["citations"]):
            url = result["urls"].get(c, "")
            print(f"- [{c}] {url}".rstrip())
    log(f"\n[{result['searches']} searches, {result['model_calls']} model calls, "
        f"{result['input_tokens']}+{result['output_tokens']} tokens, {result['seconds']} s, "
        f"citation check: {result['guardrail']}]")
    return 0


if __name__ == "__main__":
    sys.exit(main())
