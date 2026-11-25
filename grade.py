"""Hand-grading helper: shows question, reference answer and the agent's answer; you type the verdict.

    uv run python grade.py          # grades up to 24 answers (12 single, 6 multi, 6 unanswerable)
    uv run python grade.py --all    # every answer

Writes eval/human_labels.csv (id,correct,supported,notes). Safe to stop with q and resume later.
It never reads the judge's verdicts.
"""

import csv
import json
import random
import sys
from pathlib import Path

EVAL = Path(__file__).resolve().parent / "eval"
LABELS = EVAL / "human_labels.csv"
FIELDS = ["id", "correct", "supported", "notes"]
MIX = {"single": 12, "multi": 6, "unanswerable": 6}


def load_labels() -> dict[str, dict]:
    if not LABELS.exists():
        return {}
    with LABELS.open(newline="", encoding="utf-8") as f:
        return {r["id"]: r for r in csv.DictReader(f) if (r.get("id") or "").strip() and r.get("correct", "") != ""}


def save_labels(rows: dict[str, dict]) -> None:
    with LABELS.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=FIELDS, quoting=csv.QUOTE_MINIMAL)
        writer.writeheader()
        for r in sorted(rows.values(), key=lambda r: r["id"]):
            writer.writerow({k: r.get(k, "") for k in FIELDS})


def ask01(prompt: str) -> str | None:
    while True:
        value = input(prompt).strip().lower()
        if value in {"1", "0"}:
            return value
        if value in {"q", "s"}:
            return value
        print("  type 1, 0, s (skip) or q (quit and save)")


def main() -> None:
    with (EVAL / "questions.csv").open(newline="", encoding="utf-8-sig") as f:
        questions = {r["id"]: r for r in csv.DictReader(f)}
    answers = {r["id"]: r for r in map(json.loads, filter(str.strip, (EVAL / "answers.jsonl").open(encoding="utf-8")))}
    labels = load_labels()

    ids = [i for i in questions if i in answers]
    if "--all" not in sys.argv:
        rng = random.Random(7)
        chosen = []
        for kind, n in MIX.items():
            pool = [i for i in ids if questions[i]["kind"].strip().lower() == kind]
            chosen += rng.sample(pool, min(n, len(pool)))
        ids = sorted(chosen)

    todo = [i for i in ids if i not in labels]
    print(f"{len(labels)} graded so far; {len(todo)} to go in this round. Need at least 20 in total.\n")
    for n, qid in enumerate(todo, 1):
        q, a = questions[qid], answers[qid]
        print("=" * 78)
        print(f"[{n}/{len(todo)}] {qid}  ({q['kind']})   expected: {q['expected_source']} {q['expected_location']}")
        print(f"QUESTION: {q['question']}")
        print(f"REFERENCE: {q['reference_answer']}\n")
        print(f"AGENT ANSWER:\n{a['answer']}\n")
        print("correct   = 1 if it matches the reference (or refuses properly when it should), else 0")
        print("supported = 1 if every claim is in the retrieved text / cited articles, else 0")
        correct = ask01("correct (1/0, s skip, q quit)? ")
        if correct == "q":
            break
        if correct == "s":
            continue
        supported = ask01("supported (1/0)? ")
        if supported == "q":
            break
        if supported == "s":
            continue
        notes = input("notes (required if any 0; Enter to skip otherwise): ").strip()
        while "0" in (correct, supported) and not notes:
            notes = input("  explain the 0: ").strip()
        labels[qid] = {"id": qid, "correct": correct, "supported": supported, "notes": notes}
        save_labels(labels)

    save_labels(labels)
    print(f"\nSaved {len(labels)} grades to {LABELS}.")
    if len(labels) < 20:
        print("You still need at least 20; run this again.")


if __name__ == "__main__":
    main()
