"""
Assignment 3: end-to-end evaluation (`uv run python main.py evaluate`).

For every question in eval/questions.csv: run the agent (agent.py), apply code checks, ask an LLM
judge to grade it with my rubric, and (if eval/human_labels.csv exists) measure how often the judge
agrees with my own labels. Everything is written to eval/.

    uv run python evaluate.py --no-judge     # run the agent only, then label by hand
    uv run python evaluate.py --reuse        # reuse eval/results.csv, add the judge and agreement
    uv run python evaluate.py                # everything from scratch

My rubric (the judge receives these exact rules):
  correct   - answerable question: the answer gets the MAIN point of the reference answer
              (it does not have to mention everything).
            - unanswerable question: the answer says the corpus does not cover it / refuses.
              A refusal that also mentions closely related passages, validly cited, is still correct.
  supported - every claim in the answer is based on a passage the answer cites
              (it does not have to be quoted word for word).
"""
from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
from pathlib import Path

from pydantic import BaseModel, Field

import agent as agent_module
from agent import LIMIT_REACHED, UNVERIFIED, find_citations, run_agent

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
RESULTS = EVAL / "results.csv"
TRACES = EVAL / "traces.jsonl"
JUDGE_OUT = EVAL / "judge_labels.csv"
HUMAN = EVAL / "human_labels.csv"
SUMMARY = EVAL / "summary.json"

# USD per million tokens for the model in agent.py (check the Gemini pricing page for your model).
PRICE_IN, PRICE_OUT = 0.30, 2.50
REFUSAL = re.compile(r"does not cover|do not cover|not covered by the corpus", re.I)

RUBRIC = """You grade answers from a question-answering assistant. Apply these rules exactly.

correct:
- If the question is answerable: correct = true when the answer gets the MAIN point of the reference
  answer. It does not have to mention everything. It is false if it contradicts the reference, misses the
  main point, or refuses to answer.
- If the question is unanswerable (the reference says the corpus does not cover it): correct = true only
  if the answer says the corpus does not cover the question, or refuses. A refusal that also mentions
  closely related passages with citations is still correct. It is false if the answer gives an
  answer to the question.

supported:
- true when every claim in the answer is based on one of the passages the answer cites (not necessarily
  quoted word for word). false if any claim is not in the cited passages. A plain refusal is supported."""


class Verdict(BaseModel):
    correct: bool = Field(description="Is the answer correct under the rubric?")
    supported: bool = Field(description="Is every claim supported by the passages it cites?")
    reason: str = Field(description="One short sentence explaining the verdict.")


def with_retry(call, tries: int = 4):
    for attempt in range(1, tries + 1):
        try:
            return call()
        except Exception as error:  # noqa: BLE001
            limited = "429" in str(error) or "RESOURCE_EXHAUSTED" in str(error)
            if not limited or attempt == tries:
                raise
            print(f"  rate limited, waiting {20 * attempt}s", file=sys.stderr)
            time.sleep(20 * attempt)


def yes(value: str) -> str:
    return "yes" if str(value).strip().lower() in {"yes", "y", "1", "true", "si", "sí"} else "no"


def load_questions() -> list[dict]:
    with QUESTIONS.open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def code_checks(question: dict, result: dict) -> dict:
    """Checks that need no LLM: refusal wording, valid citations, expected sources cited."""
    answer = result["answer"]
    expected = [s.strip() for s in question["expected_source"].split(";") if s.strip()]
    cited = sorted({s for s, _ in find_citations(answer)})    
    guardrail = answer in (UNVERIFIED, LIMIT_REACHED)
    refused = bool(REFUSAL.search(answer))
    if expected:  # answerable
        passed = (not refused) and (not guardrail) and set(expected) <= set(cited)
    else:         # unanswerable
        passed = refused
    return {"refused": refused, "guardrail_replaced": guardrail, "cited_sources": ";".join(cited),
            "citations_valid": result["citations_ok"], "code_check_passed": passed}


def judge_answer(question: dict, result: dict, model) -> tuple[Verdict, dict]:
    """Ask the LLM judge. Returns the verdict and the judge's token usage."""
    passages = "\n\n".join(step["result"] for step in result["trace"] if step["tool"] == "search") or "(no search)"
    prompt = (f"{RUBRIC}\n\nQUESTION: {question['question']}\nKIND: {question['kind']}\n"
              f"REFERENCE ANSWER: {question['reference_answer']}\n\n"
              f"PASSAGES RETURNED BY SEARCH:\n{passages}\n\nANSWER TO GRADE:\n{result['answer']}")
    out = with_retry(lambda: model.with_structured_output(Verdict, include_raw=True).invoke(prompt))
    usage = getattr(out["raw"], "usage_metadata", None) or {}
    return out["parsed"], {"judge_in": usage.get("input_tokens", 0), "judge_out": usage.get("output_tokens", 0)}


def run_questions(questions: list[dict]) -> list[dict]:
    rows = []
    TRACES.write_text("", encoding="utf-8")
    for number, q in enumerate(questions, 1):
        print(f"[{number}/{len(questions)}] {q['id']}: {q['question'][:70]}", file=sys.stderr)
        try:
            result = with_retry(lambda: run_agent(q["question"], approve=lambda path: False))
        except Exception as error:  # noqa: BLE001 - one failure must not stop the whole evaluation
            result = {"answer": f"ERROR: {error}", "trace": [], "citations_ok": False,
                      "input_tokens": 0, "output_tokens": 0, "seconds": 0}
        row = {"id": q["id"], "kind": q["kind"], "question": q["question"], "answer": result["answer"],
               "searches": sum(s["tool"] == "search" for s in result["trace"]),
               "input_tokens": result["input_tokens"], "output_tokens": result["output_tokens"],
               "seconds": result["seconds"], **code_checks(q, result)}
        rows.append(row)
        with TRACES.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps({"id": q["id"], "trace": result["trace"]}, ensure_ascii=False) + "\n")
    return rows


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def load_traces() -> dict:
    traces = {}
    if TRACES.exists():
        for line in TRACES.read_text(encoding="utf-8").splitlines():
            item = json.loads(line)
            traces[item["id"]] = item["trace"]
    return traces


def rate(rows: list[dict], key: str, value: str = "yes") -> str:
    return f"{sum(r[key] == value for r in rows)}/{len(rows)}" if rows else "n/a"


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-judge", action="store_true", help="run the agent only (label by hand next)")
    parser.add_argument("--reuse", action="store_true", help="reuse eval/results.csv instead of rerunning the agent")
    args = parser.parse_args()
    EVAL.mkdir(exist_ok=True)
    questions = load_questions()
    by_id = {q["id"]: q for q in questions}

    if args.reuse and RESULTS.exists():
        with RESULTS.open(encoding="utf-8", newline="") as handle:
            rows = list(csv.DictReader(handle))
        for r in rows:
            for key in ("input_tokens", "output_tokens"):
                r[key] = int(r[key])
            r["seconds"] = float(r["seconds"])
        print(f"Reusing {len(rows)} answers from {RESULTS.name}", file=sys.stderr)
    else:
        rows = run_questions(questions)
        write_csv(RESULTS, rows)
        print(f"\nSaved {len(rows)} answers in {RESULTS.relative_to(ROOT)} (tool calls in {TRACES.name})")

    n = len(rows)
    tokens_in = sum(r["input_tokens"] for r in rows)
    tokens_out = sum(r["output_tokens"] for r in rows)
    cost = (tokens_in * PRICE_IN + tokens_out * PRICE_OUT) / 1_000_000
    summary = {
        "questions": n,
        "code_checks_passed": sum(str(r["code_check_passed"]) == "True" for r in rows),
        "avg_input_tokens": round(tokens_in / n), "avg_output_tokens": round(tokens_out / n),
        "avg_seconds": round(sum(r["seconds"] for r in rows) / n, 1),
        "agent_cost_per_question_usd": round(cost / n, 5),
    }
    print(f"\nCode checks passed: {summary['code_checks_passed']}/{n}")
    for kind in sorted({r["kind"] for r in rows}):
        group = [r for r in rows if r["kind"] == kind]
        print(f"  {kind:<13} {sum(str(r['code_check_passed']) == 'True' for r in group)}/{len(group)}")
    print(f"Per question (agent only): {summary['avg_input_tokens']} input + {summary['avg_output_tokens']} output "
          f"tokens, {summary['avg_seconds']} s, about ${summary['agent_cost_per_question_usd']}")

    if not args.no_judge:
        from langchain_google_genai import ChatGoogleGenerativeAI
        from api_key import load_api_key
        model = ChatGoogleGenerativeAI(model=agent_module.MODEL, google_api_key=load_api_key())
        traces = load_traces()
        judged, judge_tokens = [], 0
        for number, r in enumerate(rows, 1):
            print(f"[judge {number}/{n}] {r['id']}", file=sys.stderr)
            verdict, usage = judge_answer(by_id[r["id"]], {"answer": r["answer"], "trace": traces.get(r["id"], [])}, model)
            judge_tokens += usage["judge_in"] + usage["judge_out"]
            judged.append({"id": r["id"], "kind": r["kind"], "correct": "yes" if verdict.correct else "no",
                           "supported": "yes" if verdict.supported else "no", "reason": verdict.reason})
        write_csv(JUDGE_OUT, judged)
        summary["judge_correct"] = rate(judged, "correct")
        summary["judge_supported"] = rate(judged, "supported")
        summary["judge_tokens_per_question"] = round(judge_tokens / n)
        print(f"\nJudge: correct {summary['judge_correct']}, supported {summary['judge_supported']} "
              f"(judge used about {summary['judge_tokens_per_question']} tokens per question)")
        for kind in sorted({r["kind"] for r in judged}):
            group = [r for r in judged if r["kind"] == kind]
            print(f"  {kind:<13} correct {rate(group, 'correct')}, supported {rate(group, 'supported')}")

        if HUMAN.exists():
            with HUMAN.open(encoding="utf-8", newline="") as handle:
                human = {row["id"]: row for row in csv.DictReader(handle)}
            both = [j for j in judged if j["id"] in human]
            if both:
                for field in ("correct", "supported"):
                    agree = sum(yes(human[j["id"]][field]) == j[field] for j in both)
                    summary[f"agreement_{field}"] = f"{agree}/{len(both)}"
                    print(f"Agreement with my labels ({field}): {agree}/{len(both)} = {agree / len(both):.0%}")
                for j in both:
                    for field in ("correct", "supported"):
                        if yes(human[j["id"]][field]) != j[field]:
                            print(f"  disagree {j['id']} {field}: me={yes(human[j['id']][field])} judge={j[field]} ({j['reason']})")
            else:
                print("human_labels.csv has no rows that match the question ids yet.")
        else:
            print("No eval/human_labels.csv yet: label by hand to measure agreement.")

    SUMMARY.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())