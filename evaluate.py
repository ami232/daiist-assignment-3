"""
Assignment 3: evaluation (`main.py evaluate`). May be evaluate.ipynb instead.

Hit rate at 1/3/5 per retrieval design; agent answers on every question;
code checks; an LLM judge with a rubric and the retrieved text as evidence;
agreement with eval/human_labels.csv. Save results in eval/.

Start from session 10's 07-own-harness/evaluate.py.
"""

from __future__ import annotations

"""Retrieval and end-to-end evaluation for the drug-label corpus."""

import csv
import json
import time
from pathlib import Path

from agent import run_agent
from api_key import load_api_key
from retrieval import DEFAULT_DESIGN, search_chunks

ROOT = Path(__file__).resolve().parent
EVAL_DIR = ROOT / "eval"
QUESTIONS = EVAL_DIR / "questions.csv"
HUMAN = EVAL_DIR / "human_labels.csv"


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def source_hit(hits: list[dict], expected_sources: str) -> bool:
    if not expected_sources:
        return True
    expected = {part.strip() for part in expected_sources.split(";") if part.strip()}
    actual = {h["metadata"].get("source", "") for h in hits}
    return bool(expected & actual)


def hit_rates(rows: list[dict], design: str) -> dict:
    rates = {k: 0 for k in (1, 3, 5)}
    for row in rows:
        if row["kind"].strip().lower() == "unanswerable":
            continue
        hits = search_chunks(row["question"], k=5, design=design)
        for k in (1, 3, 5):
            rates[k] += int(source_hit(hits[:k], row["expected_source"]))
    answerable = sum(r["kind"].strip().lower() != "unanswerable" for r in rows)
    return {str(k): round(rates[k] / answerable, 4) if answerable else 0.0 for k in (1, 3, 5)}


def code_check(answer: str, trace: list[dict]) -> dict:
    lower = answer.lower()
    refusal = "don't know" in lower or "do not know" in lower or "not contain enough evidence" in lower
    has_citation = ("source:" in lower and "location:" in lower) or ("[" in answer and "source" in lower)
    search_used = any(t.get("tool") == "search" for t in trace)
    return {"refusal": refusal, "valid_citation_shape": has_citation, "search_used": search_used}


def judge_answer(question: dict, answer: str, evidence: str) -> dict:
    """Grade with Gemini using a fixed rubric and retrieved passages as evidence."""
    from google import genai

    rubric = (
        "Return JSON only with keys correct, supported, verdict. "
        "correct=1 if the answer matches the reference or properly refuses an unanswerable question; supported=1 only if every substantive claim is in the retrieved evidence. "
        "Otherwise use 0. verdict must be one or two short sentences."
    )
    prompt = (
        f"{rubric}\nQuestion: {question['question']}\nReference: {question['reference_answer']}\n"
        f"Retrieved evidence:\n{evidence}\nAgent answer:\n{answer}"
    )
    try:
        response = genai.Client(api_key=load_api_key()).models.generate_content(model="gemini-3.5-flash-lite", contents=prompt)
        text = response.text.strip()
        if text.startswith("```"):
            text = text.split("```", 2)[1].strip()
            if text.startswith("json"):
                text = text[4:].strip()
        data = json.loads(text)
        return {"correct": int(data["correct"]), "supported": int(data["supported"]), "verdict": str(data["verdict"])}
    except Exception as error:
        return {"correct": 0, "supported": 0, "verdict": f"Judge unavailable: {type(error).__name__}"}


def main() -> int:
    if not QUESTIONS.is_file():
        raise SystemExit("eval/questions.csv is missing")
    rows = read_csv(QUESTIONS)
    if not rows:
        raise SystemExit("eval/questions.csv has no questions")

    retrieval = {}
    for design in ("section", "fixed"):
        retrieval[design] = hit_rates(rows, design)

    answers = []
    started = time.time()

    for row in rows:
        try:
            answer, trace = run_agent(row["question"], approval=lambda prompt: False)
        except Exception as error:
            answer = f"Evaluation interrupted: {type(error).__name__}: {error}"
            trace = [{"tool": "error", "arguments": {}, "result": answer}]
        evidence_parts = []
        for event in trace:
            if event.get("tool") == "search":
                evidence_parts.append(str(event.get("result", "")))
        evidence = "\n\n".join(evidence_parts)
        checked = code_check(answer, trace)
        judge = judge_answer(row, answer, evidence)
        answers.append({"id": row["id"], "question": row["question"], "answer": answer,
                        "trace": trace, "code_check": checked, "judge": judge})

    elapsed = time.time() - started
    human_by_id = {r["id"]: r for r in read_csv(HUMAN)} if HUMAN.is_file() else {}
    agreements = []
    for item in answers:
        human = human_by_id.get(item["id"])
        if human:
            agreements.append((int(human["correct"]), item["judge"]["correct"]))
    agreement = sum(h == j for h, j in agreements) / len(agreements) if agreements else None

    summary = {
        "retrieval_hit_rates": retrieval,
        "chosen_design": DEFAULT_DESIGN,
        "elapsed_seconds": round(elapsed, 2),
        "seconds_per_question": round(elapsed / len(rows), 2),
        "judge_human_agreement_correct": agreement,
        "judge_human_pairs": len(agreements),
        "answers": answers,
    }
    (EVAL_DIR / "results.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    with (EVAL_DIR / "answers.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["id", "question", "answer", "correct", "supported", "verdict"])
        writer.writeheader()
        for item in answers:
            writer.writerow({"id": item["id"], "question": item["question"], "answer": item["answer"],
                             "correct": item["judge"]["correct"], "supported": item["judge"]["supported"],
                             "verdict": item["judge"]["verdict"]})

    print(json.dumps({k: v for k, v in summary.items() if k != "answers"}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
