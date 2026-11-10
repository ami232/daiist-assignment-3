
"""
Assignment 3 — End-to-End Answer Collection

Runs the LangChain agent on all evaluation questions.

Saves each completed answer immediately so that
API errors or Codespaces disconnections do not
lose previous results.

Human grading and LLM judging are separate stages.
"""

import argparse
import asyncio
import csv
import json
import os
import time
from pathlib import Path

from agent import run_agent

QUESTIONS_PATH = Path("eval/questions.csv")
OUTPUT_PATH = Path("eval/agent_answers.jsonl")


def load_questions():
    with QUESTIONS_PATH.open(
        encoding="utf-8", newline=""
    ) as f:
        return list(csv.DictReader(f))


def load_completed():
    if not OUTPUT_PATH.exists():
        return {}

    completed = {}

    with OUTPUT_PATH.open(encoding="utf-8") as f:
        for line in f:
            if line.strip():
                record = json.loads(line)
                completed[record["id"]] = record

    return completed


def save_result(record):
    OUTPUT_PATH.parent.mkdir(
        parents=True, exist_ok=True
    )

    with OUTPUT_PATH.open(
        "a", encoding="utf-8"
    ) as f:
        f.write(
            json.dumps(record, ensure_ascii=False)
            + "\n"
        )
        f.flush()
        os.fsync(f.fileno())


async def collect_answers(limit=None):
    questions = load_questions()
    completed = load_completed()

    print(f"Total questions: {len(questions)}")
    print(f"Already completed: {len(completed)}")

    processed = 0

    for question in questions:
        qid = question["id"]

        if qid in completed:
            continue

        if limit is not None and processed >= limit:
            break

        print(
            f"\nRunning {qid}: {question['question']}",
            flush=True
        )

        started = time.perf_counter()

        try:
            result = await run_agent(
                question["question"],
                allow_approval=False
            )

        except Exception as error:
            print(
                f"\nFailed on {qid}: {error}",
                flush=True
            )
            print(
                "Completed answers remain saved. "
                "Run again to resume."
            )
            return

        elapsed = time.perf_counter() - started

        record = {
            "id": qid,
            "question": question["question"],
            "kind": question["kind"],
            "expected_source": question["expected_source"],
            "expected_location": question["expected_location"],
            "reference_answer": question["reference_answer"],
            "answer": result["answer"],
            "search_calls": result["search_calls"],
            "tool_trace": result["tool_trace"],
            "seconds": round(elapsed, 3),
        }

        save_result(record)

        processed += 1

        print(f"Saved {qid}")
        print(f"Time: {elapsed:.2f}s")
        print(f"Search calls: {result['search_calls']}")
        print(f"Answer: {result['answer'][:250]}")

        await asyncio.sleep(1)

    total = len(load_completed())

    print("\n================================")
    print(f"Completed answers: {total}/{len(questions)}")
    print(f"Output: {OUTPUT_PATH}")
    print("================================")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--limit",
        type=int,
        default=None,
        help="Maximum new answers to generate"
    )

    args = parser.parse_args()

    asyncio.run(
        collect_answers(limit=args.limit)
    )