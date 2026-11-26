"""LangChain/Gemini agent using the actual stdio MCP server, not direct retrieval."""

from __future__ import annotations

import asyncio
import inspect
import json
import re
import sys
import time
from collections.abc import Callable
from contextlib import AsyncExitStack
from pathlib import Path

from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware, wrap_model_call
from langchain_core.messages import AIMessage, ToolMessage
from langchain_core.tools import StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_google_genai.chat_models import GoogleAPIError, GoogleRateLimitError
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from api_key import load_api_key
from runtime import (
    ROOT,
    citation_check,
    missing_named_sources,
    normalize_citations,
    read_config,
    read_policy,
)


def terminal_approval(arguments: dict) -> bool:
    """No noninteractive default approval; EOF and denial both block the write."""
    if not sys.stdin.isatty():
        return False
    try:
        return (
            input(
                f"Index {arguments.get('path')!r} and send its text to Gemini? [y/N] "
            )
            .strip()
            .lower()
            == "y"
        )
    except EOFError:
        return False


def refusal(answer: str, policy: dict) -> bool:
    return answer.strip() == policy["refusal_text"].strip()


def enforce_citations(
    answer: str, retrieved: list[dict], policy: dict
) -> tuple[str, dict]:
    """Checks citation identity, not whether cited text entails every claim."""
    answer = normalize_citations(answer)
    check = citation_check(answer, retrieved)
    if refusal(answer, policy):
        return answer, {"triggered": False, "reason": "model_refusal", **check}
    if not check["valid"]:
        return policy["refusal_text"], {
            "triggered": True,
            "reason": "missing_or_invalid_citation",
            **check,
        }
    return answer, {"triggered": False, "reason": None, **check}


class AgentRunner:
    def __init__(
        self, root: Path = ROOT, *, approval: Callable = terminal_approval, model=None
    ):
        self.root = root
        self.approval = approval
        self.policy = read_policy(root)
        self.model = model
        self.trace = []
        self.stack = AsyncExitStack()

    async def __aenter__(self):
        await self.stack.__aenter__()
        try:
            server_key = load_api_key() if self.model is None else None
            params = StdioServerParameters(
                command=sys.executable,
                args=[str(self.root / "server.py")],
                cwd=str(self.root),
                env={"GEMINI_API_KEY": server_key} if server_key else None,
            )
            read, write = await self.stack.enter_async_context(stdio_client(params))
            self.session = await self.stack.enter_async_context(
                ClientSession(read, write)
            )
            await self.session.initialize()
            tools = [
                self.wrap(tool) for tool in (await self.session.list_tools()).tools
            ]
            self.tools = tools
            if {tool.name for tool in tools} != {"search", "add_document"}:
                raise ValueError("Server must expose exactly search and add_document.")
            if self.model is None:
                self.model = ChatGoogleGenerativeAI(
                    model=self.policy["agent_model"],
                    temperature=None,
                    api_key=load_api_key(),
                    max_retries=1,
                )
            prompt = (self.root / "AGENTS.md").read_text()
            prompt += (
                "\n\nWhen evidence is insufficient, return exactly:\n"
                + self.policy["refusal_text"]
            )
            last_model_request = 0.0

            @wrap_model_call
            async def pace_model(request, handler):
                nonlocal last_model_request
                for attempt in range(4):
                    delay = self.policy.get("min_model_interval_seconds", 4.3) - (
                        time.monotonic() - last_model_request
                    )
                    if delay > 0:
                        await asyncio.sleep(delay)
                    last_model_request = time.monotonic()
                    try:
                        return await handler(request)
                    except (GoogleAPIError, GoogleRateLimitError) as error:
                        message = str(error).lower()
                        minute_limit = "429" in message and (
                            "per minute" in message or "perminute" in message
                        )
                        temporary = "503" in message or "unavailable" in message
                        if attempt == 3 or not (minute_limit or temporary):
                            raise
                        match = re.search(r"retrydelay[^0-9]*(\d+)s", message)
                        wait = min(59, max(5, int(match.group(1)) + 1)) if match else 5
                        await asyncio.sleep(wait)

            self.agent = create_agent(
                model=self.model,
                tools=tools,
                system_prompt=prompt,
                middleware=[
                    pace_model,
                    ModelCallLimitMiddleware(
                        run_limit=self.policy["max_model_calls"], exit_behavior="error"
                    ),
                ],
            )
        except BaseException:
            await self.stack.aclose()
            raise
        return self

    async def __aexit__(self, *args):
        await self.stack.__aexit__(*args)

    def wrap(self, tool):
        async def call(**arguments):
            entry = {"tool": tool.name, "arguments": arguments, "status": "pending"}
            self.trace.append(entry)
            if len(self.trace) > self.policy.get("max_tool_calls", 8):
                entry.update(
                    status="denied",
                    result={
                        "error": "Tool-call limit reached. Stop and explain the limitation."
                    },
                )
                return json.dumps(entry["result"])
            if tool.name == "add_document":
                allowed = self.approval(arguments)
                if inspect.isawaitable(allowed):
                    allowed = await allowed
                entry["approval"] = bool(allowed)
                if not allowed:
                    entry.update(
                        status="denied",
                        result={"error": "Human approval denied. No file was indexed."},
                    )
                    return json.dumps(entry["result"])
            result = await self.session.call_tool(tool.name, arguments)
            text = "\n".join(getattr(item, "text", "") for item in result.content)
            is_error = getattr(result, "is_error", False) or getattr(
                result, "isError", False
            )
            try:
                payload = json.loads(text)
            except json.JSONDecodeError:
                payload = {"text": text}
            entry.update(status="error" if is_error else "ok", result=payload)
            return json.dumps({"error": payload}) if is_error else text

        return StructuredTool.from_function(
            coroutine=call,
            name=tool.name,
            description=tool.description or "",
            args_schema=tool.input_schema,
        )

    async def ask(self, question: str) -> dict:
        if not question.strip() or len(question) > 8000:
            raise ValueError("Question must contain 1–8000 characters.")
        self.trace = []
        started = time.perf_counter()
        missing = missing_named_sources(question, read_config(self.root))
        if missing:
            return {
                "question": question,
                "answer": self.policy["refusal_text"],
                "raw_answer": self.policy["refusal_text"],
                "refused": True,
                "trace": [],
                "retrieved": [],
                "guardrail": {
                    "triggered": True,
                    "reason": "explicit_source_missing",
                    "missing_sources": missing,
                    "cited_ids": [],
                    "invalid_ids": [],
                    "malformed": [],
                    "valid": False,
                },
                "usage": {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0},
                "model_calls": 0,
                "seconds": time.perf_counter() - started,
                "agent_model": self.policy["agent_model"],
            }
        search = next(tool for tool in self.tools if tool.name == "search")
        evidence = await search.ainvoke({"query": question})
        # This seed is a harness action, not a model-generated tool call.
        prefetch = AIMessage(
            content="",
            tool_calls=[
                {"name": "search", "args": {"query": question}, "id": "original-query"}
            ],
            additional_kwargs={"harness_prefetch": True},
        )
        result = await self.agent.ainvoke(
            {
                "messages": [
                    {"role": "user", "content": question},
                    prefetch,
                    ToolMessage(
                        content=evidence, tool_call_id="original-query", name="search"
                    ),
                ]
            }
        )
        messages = result["messages"]
        raw_answer = messages[-1].text
        retrieved = [
            chunk
            for call in self.trace
            if call["tool"] == "search" and call["status"] == "ok"
            for chunk in call["result"].get("chunks", [])
        ]
        # Deduplicate repeated search hits without changing order.
        retrieved = list({c["id"]: c for c in retrieved}.values())
        answer, guardrail = enforce_citations(raw_answer, retrieved, self.policy)
        usage = {"input_tokens": 0, "output_tokens": 0, "total_tokens": 0}
        calls = 0
        for message in messages:
            if isinstance(message, AIMessage) and not message.additional_kwargs.get(
                "harness_prefetch"
            ):
                calls += 1
                for key in usage:
                    usage[key] += (message.usage_metadata or {}).get(key, 0)
        return {
            "question": question,
            "answer": answer,
            "raw_answer": raw_answer,
            "refused": refusal(answer, self.policy),
            "trace": list(self.trace),
            "retrieved": retrieved,
            "guardrail": guardrail,
            "usage": usage,
            "model_calls": calls,
            "original_query_prefetched": True,
            "seconds": time.perf_counter() - started,
            "agent_model": self.policy["agent_model"],
        }


async def ask(question: str, root: Path = ROOT, **kwargs) -> dict:
    async with AgentRunner(root, **kwargs) as runner:
        return await runner.ask(question)


async def main(question: str):
    result = await ask(question)
    print(result["answer"])
    cited = set(result["guardrail"]["cited_ids"])
    if not result["refused"]:
        for chunk in result["retrieved"]:
            if chunk["id"] in cited:
                print(f"\n{chunk['citation']} {chunk['source']} — {chunk['location']}")


if __name__ == "__main__":
    if len(sys.argv) < 2:
        raise SystemExit('Usage: python agent.py "question"')
    asyncio.run(main(" ".join(sys.argv[1:])))
