"""
Before/after demo for the add_document tool (REPORT.md, "Adding a document").

1. Ask the agent an unanswerable question (q29, Bono Alquiler Joven) and save the answer.
2. Download Real Decreto 42/2022 from the BOE and add it through the MCP server's
   add_document tool, exactly as an editor would call it.
3. Ask the same question again and save the answer.

Results go to eval/add_document_demo.json and eval/add_document_demo.md.
Re-runnable: the "before" answer is kept once saved, and add_document only embeds
chunks that are not stored yet (so if the daily quota stops it, run it again tomorrow).
"""

import asyncio
import json
import sys
from contextlib import AsyncExitStack
from pathlib import Path

import httpx

import agent as ag
import index as ix

ROOT = Path(__file__).resolve().parent
OUT_JSON = ROOT / "eval" / "add_document_demo.json"
OUT_MD = ROOT / "eval" / "add_document_demo.md"
QUESTION_ID = "q29"
QUESTION = "How much is the Bono Alquiler Joven (youth rent subsidy) and how do I apply?"
DOC = {"boe_id": "BOE-A-2022-802",
       "title": "Real Decreto 42/2022, por el que se regula el Bono Alquiler Joven y el Plan Estatal para el acceso a la vivienda 2022-2025"}


def download() -> Path:
    path = ix.CORPUS_DIR / f"{DOC['boe_id']}.xml"
    if not path.exists():
        ix.CORPUS_DIR.mkdir(exist_ok=True)
        r = httpx.get(ix.BOE_API.format(boe_id=DOC["boe_id"]), headers={"Accept": "application/xml"}, timeout=120)
        r.raise_for_status()
        path.write_bytes(r.content)
    return path


async def ask() -> dict:
    async with AsyncExitStack() as stack:
        agent = await ag.build_agent(stack)
        return await ag.answer_async(QUESTION, agent=agent, interactive=False)


async def add(path: Path) -> str:
    async with AsyncExitStack() as stack:
        tools = {t.name: t for t in await ag.open_tools(stack)}
        return await tools["add_document"].ainvoke({"path": str(path.relative_to(ROOT))})


def main() -> None:
    state = json.loads(OUT_JSON.read_text(encoding="utf-8")) if OUT_JSON.exists() else {}
    if "before" not in state:
        print("1. Asking before adding the document ...", file=sys.stderr)
        state["before"] = asyncio.run(ask())
        OUT_JSON.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")

    print("2. add_document ...", file=sys.stderr)
    state["add_document_result"] = asyncio.run(add(download()))
    print("   " + state["add_document_result"], file=sys.stderr)
    OUT_JSON.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")
    if state["add_document_result"].startswith("Error"):
        raise SystemExit("add_document did not finish; run this script again (e.g. after the quota resets).")

    print("3. Asking again ...", file=sys.stderr)
    state["after"] = asyncio.run(ask())
    OUT_JSON.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")

    md = [f"# add_document: before and after ({QUESTION_ID})", "", f"**Question:** {QUESTION}", "",
          f"**Document added:** {DOC['title']} ({DOC['boe_id']}, https://www.boe.es/buscar/act.php?id={DOC['boe_id']})", "",
          "## Before", "", state["before"]["answer"], "",
          f"_Retrieved: {', '.join(state['before']['retrieved'])}_", "",
          "## add_document result", "", state["add_document_result"], "",
          "## After", "", state["after"]["answer"], "",
          f"_Retrieved: {', '.join(state['after']['retrieved'])}_", ""]
    OUT_MD.write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


if __name__ == "__main__":
    main()
