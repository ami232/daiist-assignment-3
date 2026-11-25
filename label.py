"""
Grade the agent's answers yourself: `uv run python label.py`

Shows each question, its reference answer, the agent's answer and the retrieved
passages (NOT the judge's verdict), and writes your grades to eval/human_labels.csv.
Already graded ids are skipped, so you can stop and continue later.
"""

import csv
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent
QUESTIONS = ROOT / "eval" / "questions.csv"
ANSWERS = ROOT / "eval" / "answers.jsonl"
HUMAN = ROOT / "eval" / "human_labels.csv"


def yes_no(prompt: str) -> str:
    while True:
        v = input(prompt).strip()
        if v in ("0", "1"):
            return v


def main() -> None:
    questions = {r["id"]: r for r in csv.DictReader(QUESTIONS.open(encoding="utf-8"))}
    answers = {}
    for line in ANSWERS.read_text(encoding="utf-8").splitlines():
        if line.strip():
            a = json.loads(line)
            if not a.get("error"):
                answers[a["id"]] = a
    done = {}
    if HUMAN.exists():
        done = {r["id"]: r for r in csv.DictReader(HUMAN.open(encoding="utf-8")) if r.get("id", "").strip()}
    todo = [i for i in questions if i in answers and i not in done]
    print(f"{len(done)} graded, {len(todo)} to go. Ctrl+C to stop (progress is saved).\n")
    for i in todo:
        q, a = questions[i], answers[i]
        print("=" * 90)
        print(f"{i} [{q['kind']}]  {q['question']}\n")
        print(f"REFERENCE: {q['reference_answer']}\n")
        print(f"AGENT ANSWER:\n{a['answer']}\n")
        show = input("Show retrieved passages? [y/N] ").strip().lower() == "y"
        if show:
            for t in a["trace"]:
                if t["tool"] == "search":
                    print(f"\n--- search({t['args'].get('query')!r})\n{t['output'][:6000]}")
        correct = yes_no("correct? (1 right vs reference or proper refusal / 0) ")
        supported = yes_no("supported? (1 every claim is in the retrieved text / 0) ")
        notes = input("notes (why, if any 0): ").strip()
        done[i] = {"id": i, "correct": correct, "supported": supported, "notes": notes}
        with HUMAN.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["id", "correct", "supported", "notes"])
            w.writeheader()
            w.writerows(done.values())
    print(f"\nDone: {len(done)} answers graded in {HUMAN}.")


if __name__ == "__main__":
    main()
