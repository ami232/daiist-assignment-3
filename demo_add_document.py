"""
Add-document demo: answer an unanswerable question, add the law that answers
it through the MCP add_document tool, answer again. Also calls add_document a
second time to show what happens when the document is already indexed.

    uv run python demo_add_document.py

Writes eval/add_document_demo.json. The "before" answer is taken from
eval/answers.jsonl (the evaluation run, made before the document was added).
"""

import asyncio
import json
import os
import sys
from pathlib import Path

import agent
import index

ROOT = Path(__file__).resolve().parent
QUESTION_ID = "u02"
BOE_ID = "BOE-A-2021-11472"  # Ley 10/2021, de 9 de julio, de trabajo a distancia


async def call_add_document(path: str) -> str:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    params = StdioServerParameters(command=sys.executable, args=[str(ROOT / "server.py")],
                                   cwd=str(ROOT), env=dict(os.environ))
    async with stdio_client(params) as (read, write), ClientSession(read, write) as session:
        await session.initialize()
        result = await session.call_tool("add_document", {"path": path})
        return "\n".join(getattr(c, "text", "") for c in result.content)


def main() -> None:
    answers = {r["id"]: r for r in map(json.loads, (ROOT / "eval/answers.jsonl").read_text().splitlines())}
    before = answers[QUESTION_ID]
    path = index.download(BOE_ID)
    first = asyncio.run(call_add_document(str(path)))
    second = asyncio.run(call_add_document(str(path)))
    after = agent.run(before["question"], interactive=False)
    out = {"question": before["question"], "document": f"{index.KNOWN_TITLES[BOE_ID]} ({index.BOE_URL.format(id=BOE_ID)})",
           "before": before["answer"], "add_document": first, "add_document_again": second,
           "after": after["answer"], "after_retrieved": after["retrieved"]}
    (ROOT / "eval/add_document_demo.json").write_text(json.dumps(out, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps(out, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
