"""
Assignment 3: add a document that answers an unanswerable question and show the
answer before and after.  `uv run python demo_add_document.py [--yes]`

q33 ("¿Puede el casero negarse a que me empadrone en el piso?") is not answered by
the three housing laws. The BOE resolution with the technical instructions to town
halls on the Padrón municipal (BOE-A-2020-4784) answers it in its section 2.3.

1. Ask q33 (before).
2. Ask the agent to add the document. add_document waits for approval: you are
   asked in the terminal, or --yes approves it for a recorded run.
3. Ask q33 again (after).
4. Ask to add the same file again: it is already indexed, so nothing is embedded.

It runs on a temporary copy of index/, so the committed index (and the evaluation)
stays the three-law corpus and q33 remains unanswerable there.

The steps and answers are written to eval/add_document_demo.md.
"""

import asyncio
import os
import shutil
import sys
import tempfile
from pathlib import Path

import httpx

import agent
import index

DOC_URL = "https://www.boe.es/buscar/pdf/2020/BOE-A-2020-4784-consolidado.pdf"
DOC = index.CORPUS_DIR / "Padron.pdf"
QUESTION = "¿Puede el casero negarse a que me empadrone en el piso?"
ADD_REQUEST = f"Añade al corpus el documento {DOC}"


def download() -> None:
    if not DOC.exists():
        DOC.parent.mkdir(exist_ok=True)
        response = httpx.get(DOC_URL, follow_redirects=True, timeout=120,
                             headers={"User-Agent": "Mozilla/5.0 (course RAG assignment)"})
        response.raise_for_status()
        DOC.write_bytes(response.content)


def section(title: str, result: dict) -> str:
    tools = "\n".join(f"- `{r['name']}` returned: {r['text'][:300]}" for r in result["tool_results"]
                      if r["name"] == "add_document") or "- (no add_document call)"
    queries = [c["args"].get("query") for c in result["tool_calls"] if c["name"] == "search"]
    guard = (f"\n**Guardrail fired** ({result['guardrail']}). The model had written:\n\n> "
             + result["raw_answer"].replace("\n", "\n> ") + "\n") if result["guardrail"] else ""
    return (f"## {title}\n\nTool calls: {[c['name'] for c in result['tool_calls']]}\n\n"
            f"Search queries: {queries}\n\n{tools}\n{guard}\n"
            f"**Answer:**\n\n{result['answer']}\n\n"
            f"_({result['model_calls']} model calls, {result['seconds']} s)_\n")


async def main(auto_approve: bool) -> None:
    download()
    approvals = []

    def approve(action: dict) -> bool:
        approvals.append(f"{action['name']}({action['args']})")
        return True if auto_approve else agent.approve_in_terminal(action)

    work = Path(tempfile.mkdtemp(prefix="index-copy-")) / "index"
    shutil.copytree(index.INDEX_DIR, work)  # the demo never touches the committed index
    async with agent.mcp_tools(env={**os.environ, "RAG_INDEX_DIR": str(work)}) as tools:
        graph = agent.build_agent(tools)
        before = await agent.ask(QUESTION, graph)
        added = await agent.ask(ADD_REQUEST, graph, approve=approve)
        after = await agent.ask(QUESTION, graph)
        again = await agent.ask(ADD_REQUEST, graph, approve=approve)

    report = "\n".join([
        "# Adding a document: before and after\n",
        f"Question (q33): **{QUESTION}**\n",
        f"Document: Resolución de 17 de febrero de 2020 (INE / Dirección General de Cooperación Autonómica "
        f"y Local), instrucciones técnicas a los Ayuntamientos sobre la gestión del Padrón municipal, "
        f"BOE-A-2020-4784, consolidated text: {DOC_URL}\n",
        f"Approval requests shown to the user: {approvals} "
        f"({'approved with --yes' if auto_approve else 'answered in the terminal'})\n",
        section("1. Before adding the document", before),
        section(f"2. Request: {ADD_REQUEST}", added),
        section("3. After adding the document", after),
        section("4. Adding the same document again", again),
    ])
    (agent.ROOT / "eval" / "add_document_demo.md").write_text(report, encoding="utf-8")
    print(report)


if __name__ == "__main__":
    asyncio.run(main(auto_approve="--yes" in sys.argv))
