"""
Human grading helper: `uv run python grade.py`

Shows one saved agent answer at a time (question, reference answer, the agent's answer
and the passages it retrieved) and asks you two yes/no questions. It never shows the LLM
judge's verdict, so your grade is independent. Writes eval/human_labels.csv after every
answer, so you can stop with Ctrl+C and continue later; graded questions are skipped.
"""

import csv
import json
import random
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ANSWERS = ROOT / "eval" / "answers.jsonl"
QUESTIONS = ROOT / "eval" / "questions.csv"
LABELS = ROOT / "eval" / "human_labels.csv"
TARGET = 20


def ask_yes_no(prompt: str) -> int:
    while True:
        reply = input(f"{prompt} [y/n] ").strip().lower()
        if reply in ("y", "yes", "1"):
            return 1
        if reply in ("n", "no", "0"):
            return 0
        print("  Please type y or n.")


def wrap(text: str, indent: str = "    ") -> str:
    return "\n".join(textwrap.fill(line, 100, initial_indent=indent, subsequent_indent=indent) or indent
                     for line in text.splitlines())


def main() -> None:
    questions = {r["id"]: r for r in csv.DictReader(QUESTIONS.open(encoding="utf-8"))}
    answers = [json.loads(line) for line in ANSWERS.read_text(encoding="utf-8").splitlines() if line.strip()]
    labels = []
    if LABELS.is_file():
        labels = [r for r in csv.DictReader(LABELS.open(encoding="utf-8")) if r.get("id")]
    done = {r["id"] for r in labels}
    todo = [a for a in answers if a["id"] not in done]
    random.Random(7).shuffle(todo)  # a fixed mix of single, multi and unanswerable questions
    print(f"{len(done)} answers graded so far; {TARGET} needed. Ctrl+C stops (your grades are saved).\n")
    for a in todo:
        q = questions[a["id"]]
        evidence = "\n".join(t["result"] for t in a["trace"] if t["tool"] == "search")
        print("=" * 100)
        print(f"{a['id']}  ({q['kind']})   graded {len(labels)}/{TARGET}\n")
        print(f"QUESTION:\n{wrap(q['question'])}\n")
        print(f"REFERENCE ANSWER (what a correct answer must say):\n{wrap(q['reference_answer'])}\n")
        print(f"AGENT'S ANSWER:\n{wrap(a['answer'])}\n")
        if input("Press Return to grade, or type p + Return to first see the passages it retrieved: ").strip() == "p":
            print(wrap(evidence[:6000] or "(nothing retrieved)"))
        correct = ask_yes_no("1) Is the answer CORRECT against the reference (or a proper 'not covered' refusal)?")
        supported = ask_yes_no("2) Is EVERY claim in it backed by the retrieved passages?")
        notes = ""
        if not (correct and supported):
            notes = input("   Why? (a few words): ").strip()
        labels.append({"id": a["id"], "correct": correct, "supported": supported, "notes": notes})
        with LABELS.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=["id", "correct", "supported", "notes"])
            writer.writeheader()
            writer.writerows(labels)
        if len(labels) == TARGET:
            more = input(f"\nYou have graded {TARGET}. That is enough. Continue anyway? [y/n] ").strip().lower()
            if more not in ("y", "yes"):
                break
    print(f"\nSaved {len(labels)} grades to eval/human_labels.csv. Thank you!")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nStopped. Your grades so far are saved in eval/human_labels.csv.")
