"""Grade the agent's answers by hand, one at a time, in the terminal.

Shows the question, the reference answer and the agent's answer, asks for `correct` and
`supported` (1/0) and a note for every 0, and appends the row to eval/human_labels.csv right
away (already graded ids are skipped).
Order: all multi and unanswerable questions first, then the single ones.
Run: uv run python eval/grade.py
"""
import csv
import json
import textwrap
from pathlib import Path

EVAL = Path(__file__).resolve().parent
HUMAN = EVAL / "human_labels.csv"

questions = list(csv.DictReader((EVAL / "questions.csv").open(encoding="utf-8-sig")))
answers = {}
for line in (EVAL / "answers.jsonl").read_text(encoding="utf-8").splitlines():
    if line.strip():
        row = json.loads(line)
        answers[row["id"]] = row

done = set()
if HUMAN.exists() and HUMAN.read_text(encoding="utf-8").strip():
    done = {r["id"] for r in csv.DictReader(HUMAN.open(encoding="utf-8-sig")) if r.get("id")}
else:
    HUMAN.write_text("id,correct,supported,notes\n", encoding="utf-8")

order = {"multi": 0, "unanswerable": 1, "single": 2}
todo = sorted((q for q in questions if q["id"] in answers and q["id"] not in done),
              key=lambda q: (order.get(q["kind"], 3), q["id"]))
print(f"{len(done)} graded so far, {len(todo)} left. Aim for at least 20. Ctrl+C to stop.\n")


def ask01(prompt: str) -> str:
    while True:
        value = input(prompt).strip()
        if value in ("0", "1"):
            return value
        print("  please type 1 or 0")


def wrap(text: str) -> str:
    return "\n".join(textwrap.fill(p, 100) for p in text.splitlines())


for q in todo:
    a = answers[q["id"]]
    print("=" * 100)
    print(f"{q['id']} ({q['kind']})  graded so far: {len(done)}")
    print(f"QUESTION:  {q['question']}")
    print(f"REFERENCE: {q['reference_answer']}")
    print("-" * 100)
    print(wrap(a["answer"]))
    print("-" * 100)
    if input("Show retrieved passages? [y/N] ").strip().lower() == "y":
        for step in a.get("trace", []):
            if step["tool"] == "search":
                print(f"\n[search: {step['args'].get('query', '')}]\n{wrap(step['output'])[:4000]}")
        print("-" * 100)
    correct = ask01("correct?   1 = right against the reference (or a proper refusal), 0 = not: ")
    supported = ask01("supported? 1 = every claim is in the retrieved passages, 0 = not: ")
    notes = ""
    while (correct == "0" or supported == "0") and not notes:
        notes = input("notes (required for a 0, say why): ").strip()
    if not notes:
        notes = input("notes (optional): ").strip()
    with HUMAN.open("a", newline="", encoding="utf-8") as fh:
        csv.writer(fh).writerow([q["id"], correct, supported, notes])
    done.add(q["id"])
    print(f"saved. ({len(done)} graded)\n")

print(f"Done: {len(done)} answers graded in eval/human_labels.csv")
