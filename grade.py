"""
Assignment 3: grade the agent's answers yourself. `uv run python grade.py`

Shows one saved answer at a time (from eval/agent_answers.jsonl) next to the reference answer
and asks you two yes/no questions. Your grades go to eval/human_labels.csv after every answer,
so you can stop any time (type q) and continue later. You do NOT see the judge's verdict, so
your grades stay independent. The brief asks for at least 20 graded answers.

The order mixes the kinds of question, so 20+ answers cover single, multi and unanswerable.
"""

import csv
import json
import random
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent
QUESTIONS = ROOT / "eval" / "questions.csv"
ANSWERS = ROOT / "eval" / "agent_answers.jsonl"
HUMAN = ROOT / "eval" / "human_labels.csv"
COLUMNS = ["id", "correct", "supported", "notes"]
PATTERN = ["single", "single", "multi", "unanswerable"]  # order of kinds, repeated
EVIDENCE_SHOWN = 1800  # characters of each cited passage printed when you ask to see it


def wrap(text: str, indent: str = "  ") -> str:
    return "\n".join(textwrap.fill(line, 96, initial_indent=indent, subsequent_indent=indent)
                     for line in (text or "(empty)").splitlines())


def ask_yes_no(prompt: str) -> str:
    while True:
        reply = input(prompt).strip().lower()
        if reply in ("y", "n", "q", "p", "s"):
            return reply
        print("  Type y (yes), n (no), p (show the cited passages), s (skip this one) or q (quit).")


def load_labels() -> dict[str, dict]:
    if not HUMAN.exists():
        return {}
    with HUMAN.open(newline="", encoding="utf-8") as f:
        return {r["id"]: r for r in csv.DictReader(f) if (r.get("id") or "").strip()}


def save_labels(labels: dict[str, dict]) -> None:
    tmp = HUMAN.with_suffix(".tmp")
    with tmp.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS)
        writer.writeheader()
        for label in labels.values():
            writer.writerow({c: label.get(c, "") for c in COLUMNS})
    tmp.replace(HUMAN)


def cited_passages(record: dict) -> list[str]:
    wanted = {s["id"] for s in record.get("sources", [])}
    out = {}
    for call in record.get("trace", []):
        if call.get("tool") != "search":
            continue
        for block in call.get("result", "").split("\n["):
            for i in wanted:
                if f"id {i}" in block.split("\n", 1)[0]:
                    out.setdefault(i, block if block.startswith("[") else "[" + block)
    return list(out.values())


def order(questions: list[dict]) -> list[dict]:
    rng = random.Random(2026)  # fixed, so the order is the same every time
    queues = {k: [q for q in questions if q["kind"] == k] for k in set(q["kind"] for q in questions)}
    for queue in queues.values():
        rng.shuffle(queue)
    result = []
    while any(queues.values()):
        for kind in PATTERN:
            if queues.get(kind):
                result.append(queues[kind].pop())
    return result


def main() -> None:
    if not ANSWERS.exists():
        sys.exit("No saved answers yet. Run `uv run python main.py evaluate` first.")
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        questions = {r["id"]: r for r in csv.DictReader(f) if r["question"].strip()}
    answers = {r["id"]: r for r in (json.loads(line) for line in ANSWERS.open(encoding="utf-8") if line.strip())}
    labels = load_labels()
    todo = [q for q in order(list(questions.values())) if q["id"] in answers and q["id"] not in labels
            and not answers[q["id"]].get("error")]
    print(f"{len(labels)} answers graded so far, {len(todo)} left. The brief asks for at least 20.")
    print("For each answer: is it CORRECT (same facts as the reference) and SUPPORTED (every claim is in the "
          "cited passages)?\nFor a refusal: correct = the documents really do not cover it; supported = yes.\n")

    for q in todo:
        record = answers[q["id"]]
        print("=" * 100)
        print(f"{q['id']}  ({q['kind']})  [{len(labels) + 1} graded after this one]")
        print(f"QUESTION:\n{wrap(q['question'])}")
        print(f"REFERENCE ANSWER:\n{wrap(q['reference_answer'])}")
        print(f"AGENT'S ANSWER:\n{wrap(record['answer'])}")
        sources = record.get("sources", [])
        if sources:
            print("  Cited: " + "; ".join(f"{s['title']} | {s['location']}" for s in sources))
        print()
        while True:
            correct = ask_yes_no("Correct? (y/n, p = show cited passages, s = skip, q = quit) ")
            if correct == "p":
                for passage in cited_passages(record):
                    print(wrap(passage[:EVIDENCE_SHOWN], "    | "))
                    print()
                continue
            break
        if correct == "q":
            break
        if correct == "s":
            continue
        while True:
            supported = ask_yes_no("Supported by the passages? (y/n, p = show them, q = quit) ")
            if supported == "p":
                for passage in cited_passages(record):
                    print(wrap(passage[:EVIDENCE_SHOWN], "    | "))
                    print()
                continue
            break
        if supported == "q":
            break
        if supported == "s":
            continue
        notes = input("Note (optional, press Enter to skip): ").strip()
        labels[q["id"]] = {"id": q["id"], "correct": 1 if correct == "y" else 0,
                           "supported": 1 if supported == "y" else 0, "notes": notes}
        save_labels(labels)
        print(f"  saved ({len(labels)} graded)\n")

    print(f"\nDone for now: {len(labels)} answers graded, saved in eval/human_labels.csv.")
    if len(labels) < 20:
        print(f"{20 - len(labels)} more needed for the brief. Run this again to continue.")


if __name__ == "__main__":
    main()
