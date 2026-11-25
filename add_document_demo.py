"""
Assignment 3: add-document demo. `uv run python add_document_demo.py [--model gemini-3.5-flash-lite]`

Adds the held-back Eliquis label through the MCP add_document tool (as the
agent would, after approval), adds it a second time to show what happens when
a document is already indexed, then asks the unanswerable Eliquis questions
again. "Before" answers come from eval/answers.jsonl. Writes
eval/add_document_demo.json and eval/add_document_demo.md.
"""

import asyncio
import csv
import json
import sys
from pathlib import Path

from agent import open_tools, run_agent

ROOT = Path(__file__).resolve().parent
DOCUMENT = "corpus/held_back/eliquis.json"
QUESTION_IDS = ["q40", "q41"]
OUT = ROOT / "eval" / "add_document_demo"


async def main() -> None:
    model = sys.argv[sys.argv.index("--model") + 1] if "--model" in sys.argv else "gemini-3.5-flash-lite"
    with (ROOT / "eval" / "questions.csv").open(newline="", encoding="utf-8") as f:
        questions = {r["id"]: r for r in csv.DictReader(f)}
    before = {r["id"]: r for r in map(json.loads, (ROOT / "eval" / "answers.jsonl").read_text(encoding="utf-8").splitlines())}

    async with open_tools(approve=lambda tool, args: True) as tools:
        add = next(t for t in tools if t.name == "add_document")
        first = await add.ainvoke({"path": DOCUMENT})
        second = await add.ainvoke({"path": DOCUMENT})
        print(f"First add: {first}\nSecond add: {second}", file=sys.stderr)
        after = {}
        for qid in QUESTION_IDS:
            after[qid] = await run_agent(questions[qid]["question"], tools, model)
            print(f"{qid} done", file=sys.stderr)

    result = {"document": DOCUMENT, "model": model, "first_add": first, "second_add": second,
              "questions": {qid: {"question": questions[qid]["question"],
                                  "before": {"model": before[qid]["model"], "answer": before[qid]["answer"]},
                                  "after": {"model": model, **after[qid]}} for qid in QUESTION_IDS}}
    OUT.with_suffix(".json").write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")

    lines = ["# Add-document demo", "", f"Document: `{DOCUMENT}`", "",
             f"- First `add_document`: {first}", f"- Second `add_document` (already indexed): {second}", ""]
    for qid, q in result["questions"].items():
        lines += [f"## {qid}: {q['question']}", "", f"**Before** ({q['before']['model']}):", "", q["before"]["answer"], "",
                  f"**After** ({model}, {q['after']['tokens']['total']} tokens, {q['after']['seconds']} s):", "",
                  q["after"]["answer"], ""]
    OUT.with_suffix(".md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    asyncio.run(main())
