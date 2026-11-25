"""
Grade the agent's answers by hand: `uv run python grade.py`

Shows one answer at a time (question, your reference answer, the agent's answer and the passages it
retrieved) and asks for your two grades. It never shows the judge's verdicts, so grade before you open
eval/judged.csv. Each grade is appended to eval/human_labels.csv immediately; quit any time with q and
run it again later to continue where you stopped.

    correct   1 = right against the reference answer (or a proper refusal), 0 = not
    supported 1 = every claim is in the retrieved passages, 0 = something is not
"""

import csv
import json
import random
import sys
import textwrap
from pathlib import Path

ROOT = Path(__file__).resolve().parent
ANSWERS = ROOT / "eval" / "answers.jsonl"
QUESTIONS = ROOT / "eval" / "questions.csv"
LABELS = ROOT / "eval" / "human_labels.csv"
TARGET = 20


def ask(prompt: str, allowed: set[str]) -> str:
    while True:
        reply = input(prompt).strip().lower()
        if reply in allowed:
            return reply
        print(f"  please type one of: {', '.join(sorted(allowed))}")


def wrap(text: str, indent: str = "    ") -> str:
    return "\n".join(textwrap.fill(line, 100, initial_indent=indent, subsequent_indent=indent) if line.strip() else ""
                     for line in text.splitlines())


def main() -> None:
    if not ANSWERS.exists():
        sys.exit("No answers yet. Run `uv run python main.py evaluate` first.")
    questions = {r["id"]: r for r in csv.DictReader(QUESTIONS.open(encoding="utf-8"))}
    answers = [json.loads(l) for l in ANSWERS.read_text(encoding="utf-8").splitlines() if l.strip()]
    answers = [a for a in answers if not a.get("error") and a["id"] in questions]

    if not LABELS.exists() or not LABELS.read_text().strip():
        LABELS.write_text("id,correct,supported,notes\n", encoding="utf-8")
    done = {r["id"] for r in csv.DictReader(LABELS.open(encoding="utf-8")) if r.get("id")}
    todo = [a for a in answers if a["id"] not in done]
    random.Random(0).shuffle(todo)   # a fixed mix of kinds, so 20 grades are not all the same type
    print(f"{len(done)} graded, {len(todo)} left (aim for at least {TARGET}). Type q to stop.\n")

    for a in todo:
        q = questions[a["id"]]
        print("=" * 100)
        print(f"{a['id']}  ({q['kind']})   graded so far: {len(done)}")
        print(f"\nQUESTION\n{wrap(q['question'])}")
        print(f"\nYOUR REFERENCE ANSWER\n{wrap(q['reference_answer'])}")
        print(f"\nAGENT'S ANSWER\n{wrap(a['answer'])}")
        if a["retrieved"]:
            see = ask(f"\nShow the {len(a['retrieved'])} retrieved passages to check 'supported'? [y/n/q] ", {"y", "n", "q"})
            if see == "q":
                break
            if see == "y":
                for cite, v in a["retrieved"].items():
                    print(f"\n  --- {cite}\n{wrap(v['text'], '      ')}")
        else:
            print("\n(no passages retrieved)")

        correct = ask("\ncorrect?   1 = right against the reference (or proper refusal), 0 = wrong, q = quit: ", {"0", "1", "q"})
        if correct == "q":
            break
        supported = ask("supported? 1 = every claim is in the passages, 0 = not, q = quit: ", {"0", "1", "q"})
        if supported == "q":
            break
        notes = input("notes (why, required for every 0; Enter to skip): ").strip()
        while "0" in (correct, supported) and not notes:
            notes = input("  a reason is needed for a 0: ").strip()
        with LABELS.open("a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([a["id"], correct, supported, notes])
        done.add(a["id"])
        print(f"saved ({len(done)} graded)\n")

    print(f"\n{len(done)} answers graded in {LABELS.relative_to(ROOT)}.")
    if len(done) >= TARGET:
        print("Now run `uv run python main.py evaluate` to compute agreement with the judge.")


if __name__ == "__main__":
    main()
