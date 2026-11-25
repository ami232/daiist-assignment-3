"""
Grade the agent's answers yourself: `uv run python grade.py`

Shows each answer from eval/answers.jsonl (written by `main.py evaluate`) with the
question, the reference answer and the passages the agent retrieved, asks for
`correct` and `supported` (1/0) and a note, and appends to eval/human_labels.csv.

It never shows the judge's verdicts (those are in eval/judge.csv): grade first.
Stop any time with q; running it again continues where you left off.
`uv run python grade.py q02 q09` deletes those labels and grades them again.
"""

import csv
import json
import random
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ANSWERS = ROOT / "eval" / "answers.jsonl"
LABELS = ROOT / "eval" / "human_labels.csv"
FIELDS = ["id", "correct", "supported", "notes"]


def wrap(text: str, indent: str = "  ") -> str:
    return "\n".join(textwrap.fill(line, 100, initial_indent=indent, subsequent_indent=indent) if line else ""
                     for line in text.splitlines())


def ask(prompt: str, allowed: tuple[str, ...]) -> str:
    while True:
        value = input(prompt).strip().lower()
        if value in allowed:
            return value
        print(f"  Please type one of: {', '.join(allowed)}")


def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    if not ANSWERS.exists():
        print("No eval/answers.jsonl yet: run `uv run python main.py evaluate` first.")
        return 1
    answers = [json.loads(line) for line in ANSWERS.read_text(encoding="utf-8").splitlines() if line.strip()]

    redo = set(sys.argv[1:])
    if redo and LABELS.exists():
        with LABELS.open(newline="", encoding="utf-8") as f:
            kept = [r for r in csv.DictReader(f) if r.get("id") and r["id"] not in redo]
        with LABELS.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, FIELDS)
            w.writeheader()
            w.writerows(kept)

    graded = set()
    if LABELS.exists():
        with LABELS.open(newline="", encoding="utf-8") as f:
            graded = {r["id"] for r in csv.DictReader(f) if r.get("id")}
    else:
        with LABELS.open("w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(FIELDS)

    todo = [a for a in answers if a["id"] not in graded]
    random.Random(0).shuffle(todo)  # mixed kinds, same order every run
    print(f"{len(graded)} graded so far, {len(todo)} to go (20+ needed). Type q to stop.\n")

    for n, a in enumerate(todo, len(graded) + 1):
        print("=" * 100)
        print(f"[{n}] {a['id']}  ({a['kind']})")
        print(f"\nQUESTION\n{wrap(a['question'])}")
        print(f"\nREFERENCE ANSWER\n{wrap(a['reference_answer'])}")
        print(f"\nAGENT ANSWER\n{wrap(a['answer'])}")
        passages = a.get("retrieved") or []
        print(f"\nRETRIEVED PASSAGES ({len(passages)} search calls, every passage in full)")
        for s_n, p in enumerate(passages, 1):
            print(f"  --- search {s_n} ---")
            print(wrap(p, "    "))
            print("    " + "-" * 60)
        print()
        correct = ask("correct?   1 = right (or a proper refusal), 0 = wrong, q = quit: ", ("1", "0", "q"))
        if correct == "q":
            break
        supported = ask("supported? 1 = every claim is in the passages, 0 = not, q = quit: ", ("1", "0", "q"))
        if supported == "q":
            break
        notes = ""
        if "0" in (correct, supported):
            while not notes:
                notes = input("notes (why the 0?): ").strip()
        else:
            notes = input("notes (optional, Enter to skip): ").strip()
        with LABELS.open("a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([a["id"], correct, supported, notes])
        print(f"  saved ({n} graded)\n")

    with LABELS.open(newline="", encoding="utf-8") as f:
        total = sum(1 for r in csv.DictReader(f) if r.get("id"))
    print(f"\n{total} answers graded in eval/human_labels.csv" + ("" if total >= 20 else f" ({20 - total} more needed)."))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
