"""LangChain answering harness with MCP tools, approval and a citation gate."""
from __future__ import annotations

import argparse
import asyncio
from datetime import datetime
import inspect
import json
import os
from pathlib import Path
import sys
import time
from zoneinfo import ZoneInfo

from langchain.agents import create_agent
from langchain.agents.middleware import ModelCallLimitMiddleware
from langchain.agents.structured_output import ToolStrategy
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_core.tools import StructuredTool
from langchain_google_genai import ChatGoogleGenerativeAI
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

from answer_guardrails import AnswerDraft, guard_answer, retrieved_passages
from api_key import load_api_key
from index import ROOT, chunk_file

MAX_TOOL_CALLS = 3
MAX_PRIMARY_MODEL_CALLS = 5


class ToolBridge:
    def __init__(self, session, approval=None, allowed_root=ROOT / "corpus", max_calls=MAX_TOOL_CALLS):
        self.session, self.approval = session, approval
        self.allowed_root = Path(allowed_root).resolve()
        self.max_calls, self.calls, self.trace = max_calls, 0, []

    async def invoke(self, name, arguments):
        event = {"tool": name, "arguments": arguments, "status": "error"}
        started = time.perf_counter()
        if self.calls >= self.max_calls:
            event.update(status="call_limit", result={"error": "Tool-call limit reached; use the evidence already retrieved."})
        elif name not in {"search", "add_document"}:
            event["result"] = {"error": "Unknown tool"}
        else:
            self.calls += 1
            try:
                approved = True
                if name == "add_document":
                    path = Path(arguments["path"]).expanduser().resolve(strict=True)
                    if not path.is_relative_to(self.allowed_root):
                        raise ValueError("Document must be inside the corpus directory")
                    source, fingerprint, chunks = chunk_file(path)
                    review = {"path": str(path), "name": path.name, "bytes": path.stat().st_size,
                              "sha256": fingerprint, "source": source, "chunks": len(chunks)}
                    approved = False
                    if self.approval is not None:
                        decision = self.approval(review)
                        approved = bool(await decision if inspect.isawaitable(decision) else decision)
                    event["approval_granted"] = approved
                if not approved:
                    event.update(status="approval_denied", result={"error": "User approval was not granted; the document was not added."})
                else:
                    response = await self.session.call_tool(name, arguments)
                    if getattr(response, "is_error", False) or getattr(response, "isError", False):
                        raise RuntimeError("MCP tool returned an error")
                    result = getattr(response, "structured_content", None)
                    if result is None:
                        result = getattr(response, "structuredContent", None)
                    if result is None:
                        text = "".join(item.text for item in response.content if hasattr(item, "text"))
                        result = json.loads(text)
                    if not isinstance(result, dict):
                        raise ValueError("Expected an object in the MCP result")
                    event.update(status="success", result=result)
            except Exception as error:
                event["result"] = {"error": f"Tool failed ({type(error).__name__}); check the saved index or the document path."}
        event["seconds"] = time.perf_counter()-started
        self.trace.append(event)
        return json.dumps(event["result"], ensure_ascii=False)

    def tools(self, remote_tools):
        descriptions = {tool.name: tool.description for tool in remote_tools}
        if set(descriptions) != {"search", "add_document"}:
            raise RuntimeError("Expected exactly the corpus search and add_document MCP tools")

        async def search(query: str) -> str:
            return await self.invoke("search", {"query": query})

        async def add_document(path: str) -> str:
            return await self.invoke("add_document", {"path": path})

        return [StructuredTool.from_function(coroutine=search, name="search", description=descriptions["search"]),
                StructuredTool.from_function(coroutine=add_document, name="add_document", description=descriptions["add_document"])]


def usage_totals(messages):
    reported = [getattr(message, "usage_metadata", None) for message in messages]
    reported = [value for value in reported if value]
    if not reported:
        return {"input_tokens": None, "output_tokens": None, "total_tokens": None, "reported_model_calls": 0}
    return {**{name: sum(value.get(name, 0) for value in reported) for name in ("input_tokens", "output_tokens", "total_tokens")},
            "reported_model_calls": len(reported)}


async def run_agent(question, design=None, approval=None, model=None, as_of=None):
    if not question.strip() or len(question) > 10_000:
        raise ValueError("Provide a nonempty question under 10,000 characters")
    settings = json.loads((ROOT / "project_config.json").read_text())
    design = design or os.environ.get("RETRIEVAL_DESIGN") or settings.get("selected_retrieval_design") or "dense"
    if design not in {"dense", "hybrid"}:
        raise ValueError("Design must be dense or hybrid")
    key = load_api_key()
    model_name = os.environ.get("GEMINI_MODEL") or settings.get("agent_model", "gemini-3.1-flash-lite")
    model = model or ChatGoogleGenerativeAI(model=model_name, api_key=key, max_tokens=1800, max_retries=1, timeout=60)
    prompt = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    prompt += ("\n\nCurrent date: " + (as_of or datetime.now(ZoneInfo("Europe/Madrid")).date().isoformat())
               + f". You have at most {MAX_TOOL_CALLS} MCP calls. Search before answering."
               "\nReturn the AnswerDraft schema. Put every factual explanation or formula in a cited claim."
               " Use missing_information only to identify absent evidence, not for uncited background."
               " If the requested current company facts are absent, mark unanswerable, leave answer_claims empty,"
               " and optionally place cited concepts in general_background. Do not browse or use outside knowledge.")
    parameters = StdioServerParameters(command=sys.executable, args=[str(ROOT / "server.py")], cwd=str(ROOT),
                                     env={"RETRIEVAL_DESIGN": design, "GEMINI_API_KEY": key})
    started, messages, runtime_error, runtime_error_detail = time.perf_counter(), [], None, None
    async with stdio_client(parameters) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            bridge = ToolBridge(session, approval=approval)
            tools = bridge.tools((await session.list_tools()).tools)
            graph = create_agent(model, tools=tools, system_prompt=prompt,
                         response_format=ToolStrategy(AnswerDraft, handle_errors=False),
                         middleware=[ModelCallLimitMiddleware(run_limit=MAX_PRIMARY_MODEL_CALLS, exit_behavior="error")])
            draft = None
            try:
                response = await graph.ainvoke({"messages": [HumanMessage(content=question)]}, config={"recursion_limit": 20})
                messages.extend(response.get("messages", []))
                draft = response.get("structured_response")
                if draft is not None and not isinstance(draft, AnswerDraft):
                    draft = AnswerDraft.model_validate(draft)
            except Exception as error:
                runtime_error = type(error).__name__
                runtime_error_detail = str(error).replace(key, "[hidden]")[:1600]

            async def repair(previous, issues):
                # Correction has no tools: it cannot exceed the shared MCP budget.
                correction = model.with_structured_output(AnswerDraft, method="json_schema", include_raw=True)
                request = {"question": question, "previous_draft": previous.model_dump() if previous else None,
                           "citation_issues": issues, "retrieved_passages": retrieved_passages(bridge.trace)}
                result = await correction.ainvoke([SystemMessage(content=prompt + "\nMake your single allowed correction using only the supplied passages."),
                                                   HumanMessage(content=json.dumps(request, ensure_ascii=False))])
                if result.get("raw") is not None:
                    messages.append(result["raw"])
                if result.get("parsed") is None:
                    raise ValueError("Correction did not produce a valid AnswerDraft")
                return result["parsed"]

            final = await guard_answer(draft, bridge.trace, repair)
    return {"question": question, "design": design, "model": model_name, **final,
            "trace": bridge.trace, "usage": usage_totals(messages),
            "primary_runtime_error": runtime_error, "primary_runtime_error_detail": runtime_error_detail,
            "usage_complete": runtime_error is None, "seconds": time.perf_counter()-started,
            "usage_note": "Embedding tokens are not reported by the embedding API; these are generation-model usage counts. Failed primary graph calls may have unavailable usage."}


def console_approval(review):
    if not sys.stdin.isatty():
        return False
    print(f"\nAdd {review['name']} to the reference collection? {review['chunks']} passages, {review['bytes']:,} bytes.\nFile: {review['path']}", file=sys.stderr)
    return input("Approve this addition? [y/N] ").strip().lower() in {"y", "yes"}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("question", nargs="+")
    parser.add_argument("--design", choices=["dense", "hybrid"])
    parser.add_argument("--json", action="store_true", help="Include tool trace, usage and guardrail events")
    args = parser.parse_args()
    result = asyncio.run(run_agent(" ".join(args.question), design=args.design, approval=console_approval))
    print(json.dumps(result, ensure_ascii=False, indent=2) if args.json else result["answer"])


if __name__ == "__main__":
    main()
