"""
Grade the agent's answers yourself: `uv run python grade.py`.

Shows one answer at a time (question, reference answer, the agent's answer) WITHOUT the judge's verdict,
and writes your grades to eval/human_labels.csv. Stop any time with q; run it again to continue.

  correct   1 if the answer matches the reference (for an unanswerable question: if it correctly says the
            corpus does not state it); 0 otherwise.
  supported 1 if every claim in the answer is backed by the passages the agent retrieved (press e to see
            them); 0 if it adds something that is not there.
"""

import csv
import json
import random
from pathlib import Path

ROOT = Path(__file__).resolve().parent
QUESTIONS = ROOT / "eval" / "questions.csv"
ANSWERS = ROOT / "eval" / "answers.jsonl"
LABELS = ROOT / "eval" / "human_labels.csv"
TARGET = {"single": 8, "multi": 7, "unanswerable": 5}      # 20 in total; more is fine


def load():
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        questions = {r["id"]: r for r in csv.DictReader(f) if r["question"].strip()}
    answers = {}
    for line in ANSWERS.read_text(encoding="utf-8").splitlines():
        if line.strip():
            a = json.loads(line)
            answers[a["id"]] = a
    done = {}
    if LABELS.exists():
        with LABELS.open(newline="", encoding="utf-8") as f:
            done = {r["id"]: r for r in csv.DictReader(f) if r.get("id")}
    return questions, answers, done


def pick(questions, answers, done):
    """A fixed random sample (same every run), by kind, then everything else if you want more."""
    rng = random.Random(3)
    order = []
    for kind, n in TARGET.items():
        ids = sorted(i for i, q in questions.items() if q["kind"].strip().lower() == kind and i in answers)
        rng.shuffle(ids)
        order += ids[:n]
    rest = [i for i in sorted(questions) if i in answers and i not in order]
    rng.shuffle(rest)
    return order + rest


def ask01(prompt):
    while True:
        value = input(prompt).strip().lower()
        if value in ("0", "1", "q", "e"):
            return value
        print("  type 1, 0, e (show retrieved passages) or q (quit)")


def save(done):
    with LABELS.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["id", "correct", "supported", "notes"])
        w.writeheader()
        w.writerows(done.values())


def main():
    questions, answers, done = load()
    todo = [i for i in pick(questions, answers, done) if i not in done]
    print(f"{len(done)} graded so far. The brief asks for at least 20. Type q to stop.\n")
    for qid in todo:
        if len(done) >= 20 and input(f"You have {len(done)} grades. Continue? [y/N] ").strip().lower() != "y":
            break
        q, a = questions[qid], answers[qid]
        print("=" * 90)
        print(f"{qid}  ({q['kind']})")
        print(f"QUESTION:  {q['question']}")
        print(f"REFERENCE: {q['reference_answer']}")
        print(f"\nAGENT ANSWER:\n{a['answer']}\n")
        correct = ask01("correct? [1/0] ")
        while correct == "e":
            for s in a["trace"]:
                if s["tool"] == "search":
                    print("\n--- retrieved ---\n" + s["result"][:3500])
            correct = ask01("correct? [1/0] ")
        if correct == "q":
            break
        supported = ask01("supported by the retrieved passages? [1/0] ")
        while supported == "e":
            for s in a["trace"]:
                if s["tool"] == "search":
                    print("\n--- retrieved ---\n" + s["result"][:3500])
            supported = ask01("supported? [1/0] ")
        if supported == "q":
            break
        note = input("note (optional, Enter to skip): ").strip()
        done[qid] = {"id": qid, "correct": correct, "supported": supported, "notes": note}
        save(done)
    print(f"\nSaved {len(done)} grades in eval/human_labels.csv.")


if __name__ == "__main__":
    main()
