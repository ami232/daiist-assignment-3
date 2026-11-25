"""
Grade the agent's answers yourself: `uv run python grade.py` (a helper, not part of the pipeline).

Run it after `main.py evaluate`. For each question it shows the question, the reference answer, the passages the
agent retrieved and the agent's answer, then asks for your two grades. It never shows the judge's verdict.
Grades are saved in eval/human_labels.csv (id, correct, supported, notes). Questions you already graded are
skipped, and q at any prompt stops and saves, so you can come back later.
"""

import csv
import json
import random
import textwrap
from pathlib import Path

EVAL = Path(__file__).resolve().parent / "eval"
QUESTIONS, ANSWERS, HUMAN, RUBRIC = EVAL / "questions.csv", EVAL / "answers.jsonl", EVAL / "human_labels.csv", EVAL / "judge_rubric.md"
FIELDS = ["id", "correct", "supported", "notes"]


def wrap(text, indent="    "):
    return "\n".join(textwrap.fill(p, 110, initial_indent=indent, subsequent_indent=indent) for p in text.splitlines() if p.strip())


def ask01(prompt):
    while True:
        reply = input(prompt).strip().lower()
        if reply in ("0", "1", "q"):
            return reply
        print("    type 1, 0 or q")


def main():
    questions = {r["id"]: r for r in csv.DictReader(QUESTIONS.open(encoding="utf-8"))}
    answers = {}
    for line in ANSWERS.read_text(encoding="utf-8").splitlines():
        rec = json.loads(line) if line.strip() else {}
        if rec and not rec.get("error"):
            answers[rec["id"]] = rec
    done = set()
    if HUMAN.is_file():
        done = {r["id"] for r in csv.DictReader(HUMAN.open(encoding="utf-8")) if r.get("id")}
    else:
        HUMAN.write_text(",".join(FIELDS) + "\n", encoding="utf-8")
    todo = [i for i in questions if i in answers and i not in done]
    random.Random(1).shuffle(todo)  # a fixed random order, so the graded sample mixes kinds
    rubric = "\n".join(l for l in RUBRIC.read_text(encoding="utf-8").splitlines() if not l.lstrip().startswith("#")).strip()
    print(f"\nYour definitions:\n{rubric}\n\n{len(done)} graded, {len(todo)} to go. Type q at a prompt to stop.\n")
    for n, qid in enumerate(todo, 1):
        q, a = questions[qid], answers[qid]
        print("=" * 100)
        print(f"{qid}  ({q['kind']})   [{n}/{len(todo)}]")
        print(f"QUESTION:\n{wrap(q['question'])}")
        print(f"REFERENCE ANSWER:\n{wrap(q['reference_answer'])}")
        print(f"PASSAGES THE AGENT SAW:\n{wrap(a['passages'])}")
        print(f"AGENT'S ANSWER:\n{wrap(a['answer'])}\n")
        correct = ask01("correct   (1 = yes, 0 = no, q = stop): ")
        if correct == "q":
            break
        supported = ask01("supported (1 = yes, 0 = no, q = stop): ")
        if supported == "q":
            break
        notes = input("notes (optional, Enter to skip): ").strip()
        with HUMAN.open("a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([qid, correct, supported, notes])
        done.add(qid)
    print(f"\nSaved. {len(done)} answers graded in eval/human_labels.csv (the brief asks for at least 20).")


main()