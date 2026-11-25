"""
Assignment 3: the add-document demonstration, run by a person at the keyboard.

    uv run python demo_add_document.py

1. Copies the baseline index/ to demo_index/ (git-ignored), so the baseline
   that evaluate.py measures is never touched.
2. Asks the bus question through the real agent, serving demo_index/.
3. Asks the agent to add the held-out bus regulation; the harness asks YOU to
   approve the add_document call (type y).
4. Asks the same question again, then asks to add the same file a second time
   to show the duplicate rule.
Everything, including which index each answer used, goes to eval/add_document_demo.json.
"""

import asyncio
import csv
import json
import shutil
from contextlib import AsyncExitStack
from datetime import datetime, timezone
from pathlib import Path

import agent
import index

ROOT = Path(__file__).resolve().parent
DEMO_INDEX = ROOT / "demo_index"
HOLDOUT_FILE = "corpus/holdout/32011R0181.html"
QUESTION_ID = "q28"  # the bus question the core corpus cannot answer
OUTPUT = ROOT / "eval" / "add_document_demo.json"


def question_text(question_id):
    with (ROOT / "eval" / "questions.csv").open(newline="", encoding="utf-8") as f:
        return next(r["question"] for r in csv.DictReader(f) if r["id"] == question_id)


def collection_state(index_dir):
    """Chunk count and a fingerprint of ids, to show what changed (or did not)."""
    collection = index.design_collection(index.open_index(index_dir), index.SEARCH_DESIGN)
    ids = sorted(collection.get(include=[])["ids"])
    sources = sorted({i.split(":")[0] for i in ids})
    return {"index_dir": str(index_dir), "design": index.SEARCH_DESIGN, "chunks": len(ids), "sources": sources}


def summary(result):
    return {k: result[k] for k in ("question", "answer", "cited_ids", "trace", "guardrails", "latency_s", "usage")}


async def main():
    question = question_text(QUESTION_ID)
    baseline_before = collection_state(index.INDEX_DIR)

    # 1. A fresh copy of the baseline index: the demo writes only there.
    if DEMO_INDEX.exists():
        shutil.rmtree(DEMO_INDEX)
    shutil.copytree(index.INDEX_DIR, DEMO_INDEX)
    record = {"run_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), "question_id": QUESTION_ID,
              "baseline_index_before": baseline_before, "demo_index_before": collection_state(DEMO_INDEX)}

    async with AsyncExitStack() as stack:
        tools = await agent.load_mcp_tools(stack, DEMO_INDEX)
        unattended = agent.build_agent(tools, approve=agent.deny_all)
        attended = agent.build_agent(tools, approve=agent.ask_person)

        # 2. Before: the core corpus alone.
        print(f"\n=== Before adding: {question}")
        before = await agent.ask(unattended, question)
        agent.print_result(before)
        record["before"] = summary(before)

        # 3. Add the held-out document; the harness asks the person at the keyboard.
        print(f"\n=== Asking the agent to add {HOLDOUT_FILE}")
        added = await agent.ask(attended, f"Please add the document at {HOLDOUT_FILE} to the index.")
        agent.print_result(added)
        record["add"] = summary(added)
        record["demo_index_after_add"] = collection_state(DEMO_INDEX)

        # 4. After: the same question, then the same file again.
        print(f"\n=== After adding: {question}")
        after = await agent.ask(unattended, question)
        agent.print_result(after)
        record["after"] = summary(after)

        print(f"\n=== Asking to add {HOLDOUT_FILE} a second time (duplicate rule)")
        again = await agent.ask(attended, f"Please add the document at {HOLDOUT_FILE} to the index.")
        agent.print_result(again)
        record["add_again"] = summary(again)
        record["demo_index_after_second_add"] = collection_state(DEMO_INDEX)

    record["baseline_index_after"] = collection_state(index.INDEX_DIR)
    record["baseline_unchanged"] = record["baseline_index_after"] == baseline_before
    OUTPUT.write_text(json.dumps(record, indent=2, ensure_ascii=False))
    print(f"\nChunks in demo index: {record['demo_index_before']['chunks']} -> "
          f"{record['demo_index_after_add']['chunks']} -> {record['demo_index_after_second_add']['chunks']}; "
          f"baseline unchanged: {record['baseline_unchanged']}. Saved {OUTPUT.relative_to(ROOT)}.")


if __name__ == "__main__":
    asyncio.run(main())
