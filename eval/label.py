"""
Grade agent answers yourself, one at a time: `uv run python eval/label.py`

Shows each question, your reference answer, the agent's answer and (on request)
the retrieved passages from eval/grading_sheet.csv. Never shows the judge's
verdicts. Each grade is appended to eval/human_labels.csv immediately, and
questions you already graded are skipped, so you can stop (q) and resume.
"""

import csv
import textwrap
from pathlib import Path

EVAL = Path(__file__).resolve().parent
SHEET = EVAL / "grading_sheet.csv"
LABELS = EVAL / "human_labels.csv"
GOAL = 20


def wrap(text: str) -> str:
    return "\n".join(textwrap.fill(p, 100) for p in text.splitlines() if p.strip())


def ask01(prompt: str) -> str:
    while True:
        value = input(prompt).strip().lower()
        if value in {"0", "1", "q", "s", "p"}:
            return value


def main() -> None:
    rows = list(csv.DictReader(SHEET.open(newline="", encoding="utf-8")))
    with LABELS.open(newline="", encoding="utf-8") as f:
        done = {r["id"] for r in csv.DictReader(f) if (r.get("id") or "").strip()}

    for row in rows:
        if row["id"] in done:
            continue
        print("\n" + "=" * 100)
        print(f"{row['id']} ({row['kind']})   graded so far: {len(done)} (goal {GOAL}+)")
        print(f"\nQUESTION:\n{wrap(row['question'])}")
        print(f"\nREFERENCE:\n{wrap(row['reference_answer'])}")
        print(f"\nAGENT ANSWER:\n{wrap(row['agent_answer'])}")
        print("\n[p] show retrieved passages  [s] skip  [q] quit")

        correct = ask01("correct?   (1 = right vs reference or a proper refusal, 0 = not) ")
        if correct == "p":
            print("\nRETRIEVED PASSAGES:\n" + row["retrieved_passages"])
            correct = ask01("correct?   (1/0) ")
        if correct == "q":
            break
        if correct == "s":
            continue
        supported = ask01("supported? (1 = every claim is in the retrieved text, 0 = not; p = show passages) ")
        if supported == "p":
            print("\nRETRIEVED PASSAGES:\n" + row["retrieved_passages"])
            supported = ask01("supported? (1/0) ")
        if supported == "q":
            break
        if supported == "s":
            continue
        notes = ""
        if "0" in (correct, supported):
            notes = input("notes (why it is 0): ").strip()

        with LABELS.open("a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([row["id"], correct, supported, notes])
        done.add(row["id"])

    print(f"\n{len(done)} answers graded. Run `uv run python evaluate.py` for agreement with the judge.")


if __name__ == "__main__":
    main()
