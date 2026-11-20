"""
Human grading of agent answers: `uv run python eval/grade.py`

Shows, one at a time, the question, the reference answer, its essential facts (the same
criteria the judge gets, fixed before any answer existed: eval/essential_facts.json), the
agent's answer and the passages the agent cited (taken from its own search results). It
never reads the LLM judge's verdicts (eval/judge.jsonl), so the human grade is independent.
Grade with the rubric in eval/judge_rubric.md.
Appends to eval/human_labels.csv (id, correct, supported, notes); already graded ids
are skipped, so you can stop with Ctrl+C and resume later.

  correct   1/0  every essential fact right, nothing contradicts the reference (or a proper refusal)
  supported 1/0  every claim is in the retrieved passages and each citation contains its claim
  notes          why, for every 0
"""

import csv
import json
import random
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUESTIONS = ROOT / "eval" / "questions.csv"
ANSWERS = ROOT / "eval" / "answers.jsonl"
HUMAN = ROOT / "eval" / "human_labels.csv"
FACTS = ROOT / "eval" / "essential_facts.json"
FIELDS = ["id", "correct", "supported", "notes"]


def latest_answers() -> dict:
    out = {}
    for line in ANSWERS.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rec = json.loads(line)
            if not rec.get("superseded"):  # earlier attempts kept only as an audit trail
                out[rec["id"]] = rec
    return out


def cited_passages(answer: dict) -> list[str]:
    """The retrieved passages whose citation appears in the answer."""
    text = re.sub(r"\s*[,;]\s*(?=[A-Z][A-Z0-9-]+ \| [^\]|]+ \| p\. )", "] [", answer["answer"])  # merged citations
    cited = set(re.findall(r"\[([A-Z][A-Z0-9-]+ \| [^\]]+?)\]", text))
    blocks = []
    for text in answer.get("retrieved", []):
        for block in re.split(r"\n(?=\[\d+\] \[)", text):
            head = re.match(r"\[\d+\] \[([^\]]+)\]", block)
            if head and any(c.split(" | p. ")[0] in head.group(1) for c in cited):
                blocks.append(block.strip())
    return list(dict.fromkeys(blocks))


def ask(prompt: str, allowed: set[str]) -> str:
    while True:
        value = input(prompt).strip()
        if value in allowed:
            return value


def main() -> None:
    questions = {r["id"]: r for r in csv.DictReader(QUESTIONS.open(encoding="utf-8"))}
    answers = {k: v for k, v in latest_answers().items() if not v.get("error")}
    facts = json.loads(FACTS.read_text(encoding="utf-8")) if FACTS.is_file() else {}
    done = set()
    if HUMAN.is_file():
        done = {r["id"].strip() for r in csv.DictReader(HUMAN.open(encoding="utf-8")) if (r.get("id") or "").strip()}
    todo = [i for i in sorted(answers) if i not in done]
    random.Random(7).shuffle(todo)  # fixed shuffle: mixes kinds, reproducible
    if not HUMAN.is_file() or not HUMAN.read_text(encoding="utf-8").strip():
        with HUMAN.open("w", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow(FIELDS)
    print(f"{len(done)} graded, {len(todo)} to go. Ctrl+C to stop; progress is saved after each answer.\n")
    for n, qid in enumerate(todo, 1):
        q, a = questions[qid], answers[qid]
        print("=" * 100)
        print(f"[{n}/{len(todo)}] {qid} ({q['kind']})\nQUESTION:  {q['question']}\n")
        print(f"REFERENCE: {q['reference_answer']}\n")
        if qid in facts:
            print("ESSENTIAL FACTS (required for correct = 1):")
            for fact in facts[qid]["essential"]:
                print(f"  - {fact}")
            for fact in facts[qid].get("must_not_state", []):
                print(f"  - must NOT be stated: {fact}")
            print()
        print(f"ANSWER:\n{a['answer']}\n")
        passages = cited_passages(a)
        print(f"CITED PASSAGES ({len(passages)}):")
        for p in passages:
            print(f"  {p[:1500]}\n")
        correct = ask("correct? [1/0] ", {"0", "1"})
        supported = ask("supported? [1/0] ", {"0", "1"})
        notes = input("notes (required if any 0): ").strip()
        while (correct == "0" or supported == "0") and not notes:
            notes = input("  please explain the 0: ").strip()
        with HUMAN.open("a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([qid, correct, supported, notes])
    print("Done.")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        sys.exit("\nStopped; graded answers are saved.")
