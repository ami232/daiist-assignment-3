"""
Assignment 3: evaluation (`main.py evaluate`).

1. Retrieval: hit rate at k = 1, 3, 5 for every design (article / fixed chunks)
   and method (vector / keyword / hybrid), on the base corpus only.
2. End to end: the agent answers every question (saved to eval/answers.jsonl;
   only questions without a saved answer are run, so re-runs cost nothing).
3. Code checks: citation tags valid, a citation to an expected passage, refusal
   when (and only when) the question is unanswerable.
4. LLM judge with the rubric in eval/rubric.md and the retrieved text as
   evidence (saved to eval/judge.jsonl).
5. Agreement between the judge and eval/human_labels.csv.
6. Summary in eval/summary.json (with the rubric's aggregates); per-question rows in
   eval/results.csv; failures to classify in eval/failures.csv.

    python evaluate.py                    # everything (default for main.py evaluate)
    python evaluate.py --stage answers    # only retrieval + agent answers + grading sheet
    python evaluate.py --fresh            # re-ask the agent and the judge
"""

from __future__ import annotations

import argparse
import asyncio
import csv
import json
import os
import statistics
import sys
import time
from pathlib import Path

import index as ix
import retrieval
from agent import REFUSAL, Agent, check_citations, citations_in, is_refusal, never_approve, normalise, retrieved_in

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
ANSWERS = EVAL / "answers.jsonl"
JUDGE = EVAL / "judge.jsonl"
RUBRIC = EVAL / "rubric.md"
HUMAN = EVAL / "human_labels.csv"
GRADING_SHEET = EVAL / "grading_sheet.md"

JUDGE_MODEL = os.environ.get("JUDGE_MODEL", "gemini-3.1-flash-lite")
KS = (1, 3, 5)
PAUSE = float(os.environ.get("EVAL_PAUSE", "6"))   # seconds between questions (free tier: 15 requests/min)


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


def read_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if (r.get("question") or "").strip()]
    for r in rows:
        r["kind"] = r["kind"].strip().lower()
        sources = [s.strip() for s in r["expected_source"].split(";") if s.strip()]
        locations = [normalise(x) for x in r["expected_location"].split(";") if x.strip()]
        if len(sources) == 1 and len(locations) > 1:
            sources = sources * len(locations)
        if len(locations) == 1 and len(sources) > 1:
            locations = locations * len(sources)
        r["expected"] = list(zip(sources, locations))
    return rows


def read_jsonl(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            out[row["id"]] = row
    return out


def append_jsonl(path: Path, row: dict) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


# ------------------------------------------------------------------- retrieval


def matches(meta: dict, expected: tuple[str, str]) -> bool:
    source, location = expected
    locations = [normalise(x) for x in meta.get("locations", meta["location"]).split(";")]
    return meta["source"] == source and location in locations


def retrieval_eval(questions: list[dict]) -> list[dict]:
    answerable = [q for q in questions if q["kind"] != "unanswerable" and q["expected"]]
    rows, details = [], []
    for design in ix.DESIGNS:
        if ix.collection(design).count() == 0:
            log(f"[retrieval] design '{design}' has no vectors yet; skipped")
            continue
        for method in retrieval.METHODS:
            hit = {k: 0 for k in KS}
            all_hit = {k: 0 for k in KS}
            mrr, words_in_prompt = 0.0, []
            for q in answerable:
                hits = retrieval.search(q["question"], design, method, k=max(KS), base_only=True)
                words_in_prompt.append(sum(h["metadata"]["words"] for h in hits))
                first = next((h["rank"] for h in hits if any(matches(h["metadata"], e) for e in q["expected"])), None)
                mrr += 1 / first if first else 0
                for k in KS:
                    top = [h["metadata"] for h in hits[:k]]
                    found = [any(matches(m, e) for m in top) for e in q["expected"]]
                    hit[k] += any(found)
                    all_hit[k] += all(found)
                details.append({"design": design, "method": method, "id": q["id"], "kind": q["kind"],
                                "first_relevant_rank": first or "",
                                "top5": " | ".join(retrieval.citation(h["metadata"]) for h in hits)})
            n = len(answerable)
            row = {"design": design, "method": method, "questions": n}
            row |= {f"hit@{k}": round(hit[k] / n, 3) for k in KS}
            row |= {f"all@{k}": round(all_hit[k] / n, 3) for k in KS}
            row |= {"mrr@5": round(mrr / n, 3), "avg_words_in_prompt_k5": round(statistics.mean(words_in_prompt))}
            rows.append(row)
            log(f"[retrieval] {design:8s} {method:8s} " + "  ".join(f"hit@{k}={row[f'hit@{k}']:.2f}" for k in KS))
    write_csv(EVAL / "retrieval.csv", rows)
    write_csv(EVAL / "retrieval_details.csv", details)
    return rows


# --------------------------------------------------------------------- answers


async def run_answers(questions: list[dict], fresh: bool) -> dict[str, dict]:
    saved = {} if fresh else read_jsonl(ANSWERS)
    if fresh and ANSWERS.exists():
        ANSWERS.unlink()
    todo = [q for q in questions if q["id"] not in saved]
    if todo:
        log(f"[answers] asking the agent {len(todo)} question(s) ...")
        async with Agent() as agent:
            for i, q in enumerate(todo, start=1):
                try:
                    result = await agent.ask(q["question"], approve=never_approve)
                except Exception as error:  # noqa: BLE001 - record it and go on
                    log(f"  {q['id']}: ERROR {type(error).__name__}: {error}")
                    continue
                row = {"id": q["id"], **result, "config": ix.chosen_design()}
                append_jsonl(ANSWERS, row)
                saved[q["id"]] = row
                log(f"  [{i}/{len(todo)}] {q['id']} {'REFUSED' if row['refusal'] else 'answered'} "
                    f"in {row['seconds']}s, {row['tokens_in']}+{row['tokens_out']} tokens")
                time.sleep(PAUSE)
    return saved


def code_checks(q: dict, a: dict) -> dict:
    retrieved: set[tuple[str, str]] = set()
    for step in a["trace"]:
        if step["tool"] == "search":
            retrieved |= retrieved_in(step.get("output", ""))
    cited = citations_in(a["answer"])
    refused = is_refusal(a["answer"])
    should_refuse = q["kind"] == "unanswerable"
    checks = {
        "refused": int(refused),
        "should_refuse": int(should_refuse),
        "refusal_correct": int(refused == should_refuse),
        "refusal_exact": int(a["answer"].strip() == REFUSAL),
        "n_citations": len(cited),
        "citations_valid": "" if refused else int(check_citations(a["answer"], retrieved) is None),
        "cites_expected": "" if should_refuse else int(any(c in q["expected"] for c in cited)),
        "retrieved_expected": "" if should_refuse else int(any(e in retrieved for e in q["expected"])),
        "guardrail_fired": int(any(e.get("guardrail") == "citation_check" for e in a.get("events", []))),
        "searches": sum(1 for s in a["trace"] if s["tool"] == "search"),
    }
    return checks


# ----------------------------------------------------------------------- judge


def evidence(a: dict, limit: int = 14000) -> str:
    text = "\n\n".join(s.get("output", "") for s in a["trace"] if s["tool"] == "search")
    return text[:limit] or "(the agent did not search)"


def judge_prompt(rubric: str, q: dict, a: dict) -> str:
    return f"""You grade answers from a legal research assistant that must answer only from retrieved passages of EU law.

RUBRIC (follow it exactly):
{rubric}

QUESTION TYPE: {q['kind']}
QUESTION: {q['question']}

EXPECTED ANSWER: {q['reference_answer']}

EXPECTED SOURCE LOCATIONS: {q.get('original_location') or q['expected_location'] or '(none: unanswerable)'}

RETRIEVED PASSAGES (everything the assistant saw):
{evidence(a)}

ASSISTANT'S ANSWER:
{a['answer']}

Return JSON with: correctness (1 or 0), supported (1 or 0), reason (brief)."""


def run_judge(questions: list[dict], answers: dict[str, dict], fresh: bool) -> dict[str, dict]:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from pydantic import BaseModel, Field

    from api_key import load_api_key

    if not RUBRIC.exists() or len(RUBRIC.read_text().strip()) < 50:
        raise SystemExit("eval/rubric.md is missing or empty. Write the judge's rubric first.")
    rubric = RUBRIC.read_text(encoding="utf-8").strip()

    class Verdict(BaseModel):
        correctness: int = Field(description="1 if the answer is correct per the rubric, else 0")
        supported: int = Field(description="1 if every claim is backed by the retrieved passages, else 0")
        reason: str = Field(description="One or two sentences explaining the grades")

    saved = {} if fresh else read_jsonl(JUDGE)
    if fresh and JUDGE.exists():
        JUDGE.unlink()
    todo = [q for q in questions if q["id"] in answers and q["id"] not in saved]
    if todo:
        load_api_key()
        judge = ChatGoogleGenerativeAI(model=JUDGE_MODEL, temperature=0, max_retries=6).with_structured_output(Verdict)
        log(f"[judge] grading {len(todo)} answer(s) with {JUDGE_MODEL} ...")
        for q in todo:
            try:
                v = judge.invoke(judge_prompt(rubric, q, answers[q["id"]]))
            except Exception as error:  # noqa: BLE001
                log(f"  {q['id']}: judge ERROR {type(error).__name__}: {error}")
                continue
            row = {"id": q["id"], "correct": int(v.correctness), "supported": int(v.supported), "reason": v.reason, "model": JUDGE_MODEL}
            append_jsonl(JUDGE, row)
            saved[q["id"]] = row
            time.sleep(PAUSE / 2)
    return saved


# ------------------------------------------------------------------- agreement


def agreement(judge: dict[str, dict]) -> dict:
    if not HUMAN.exists():
        return {"graded": 0}
    with HUMAN.open(newline="", encoding="utf-8") as f:
        human = {r["id"].strip(): r for r in csv.DictReader(f) if (r.get("id") or "").strip()}
    out: dict = {"graded": len(human)}
    rows = []
    for field in ("correct", "supported"):
        pairs = [(int(h[field]), judge[i][field]) for i, h in human.items()
                 if i in judge and str(h.get(field, "")).strip() in ("0", "1")]
        if not pairs:
            continue
        n = len(pairs)
        agree = sum(a == b for a, b in pairs) / n
        p_h, p_j = sum(a for a, _ in pairs) / n, sum(b for _, b in pairs) / n
        chance = p_h * p_j + (1 - p_h) * (1 - p_j)
        # kappa is undefined when both raters give the same single grade to everything
        kappa = round((agree - chance) / (1 - chance), 3) if chance < 1 else None
        out[field] = {"n": n, "agreement": round(agree, 3), "cohen_kappa": kappa,
                      "human_zeros": sum(1 for a, _ in pairs if a == 0), "judge_zeros": sum(1 for _, b in pairs if b == 0)}
    for i, h in human.items():
        if i in judge:
            rows.append({"id": i, "human_correct": h.get("correct"), "judge_correct": judge[i]["correct"],
                         "human_supported": h.get("supported"), "judge_supported": judge[i]["supported"],
                         "human_notes": h.get("notes", ""), "judge_reason": judge[i]["reason"]})
    write_csv(EVAL / "agreement.csv", rows)
    return out


# ------------------------------------------------------------------------ main


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    fields = list(dict.fromkeys(k for r in rows for k in r))
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def write_grading_sheet(questions: list[dict], answers: dict[str, dict]) -> None:
    """Everything needed to grade by hand, and nothing from the judge."""
    lines = ["# Grading sheet (no judge verdicts here)\n",
             "Grade each answer in eval/human_labels.csv: `correct` (1/0) against the reference, "
             "`supported` (1/0) every claim is in the retrieved text, `notes` for every 0.\n"]
    for q in questions:
        a = answers.get(q["id"])
        if not a:
            continue
        lines += [f"\n---\n\n## {q['id']} ({q['kind']})\n", f"**Question:** {q['question']}\n",
                  f"**Reference:** {q['reference_answer']}\n", f"**Expected:** {q['expected_source']} {q['expected_location']}\n",
                  f"**Agent's answer:**\n\n{a['answer']}\n",
                  "<details><summary>Retrieved passages</summary>\n\n```\n" + evidence(a, 8000) + "\n```\n</details>\n"]
    GRADING_SHEET.write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", choices=["retrieval", "answers", "all"], default="all")
    parser.add_argument("--fresh", action="store_true", help="re-ask the agent and the judge")
    args = parser.parse_args()

    questions = read_questions()
    log(f"{len(questions)} questions: " + ", ".join(f"{sum(q['kind'] == k for q in questions)} {k}" for k in ("single", "multi", "unanswerable")))

    retrieval_rows = retrieval_eval(questions)
    if args.stage == "retrieval":
        return

    answers = asyncio.run(run_answers(questions, args.fresh))
    write_grading_sheet(questions, answers)
    if args.stage == "answers":
        log(f"Answers saved. Grade them from {GRADING_SHEET.name} before running the judge.")
        return

    verdicts = run_judge(questions, answers, args.fresh)

    results = []
    for q in questions:
        a = answers.get(q["id"])
        if not a:
            continue
        v = verdicts.get(q["id"], {})
        results.append({"id": q["id"], "kind": q["kind"], **code_checks(q, a),
                        "judge_correct": v.get("correct", ""), "judge_supported": v.get("supported", ""),
                        "judge_reason": v.get("reason", ""), "tokens_in": a["tokens_in"], "tokens_out": a["tokens_out"],
                        "seconds": a["seconds"], "citations": " ".join(a["citations"]), "answer": a["answer"]})
    write_csv(EVAL / "results.csv", results)

    failures = [{"id": r["id"], "kind": r["kind"], "refused": r["refused"], "should_refuse": r["should_refuse"],
                 "retrieved_expected": r["retrieved_expected"], "cites_expected": r["cites_expected"],
                 "judge_correct": r["judge_correct"], "judge_supported": r["judge_supported"],
                 "judge_reason": r["judge_reason"], "failure_cause": ""}
                for r in results if r["judge_correct"] == 0 or r["judge_supported"] == 0 or not r["refusal_correct"]]
    old = {}
    if (EVAL / "failures.csv").exists():   # keep causes you already filled in
        with (EVAL / "failures.csv").open(newline="", encoding="utf-8") as f:
            old = {r["id"]: r.get("failure_cause", "") for r in csv.DictReader(f)}
    for r in failures:
        r["failure_cause"] = old.get(r["id"], "")
    write_csv(EVAL / "failures.csv", failures)

    def share(rows, key):
        vals = [r[key] for r in rows if r[key] != ""]
        return round(sum(vals) / len(vals), 3) if vals else None

    def by_type(rows):
        out = {}
        for kind in ("all", "single", "multi", "unanswerable", "answerable"):
            sub = [r for r in rows if kind == "all" or r["kind"] == kind or (kind == "answerable" and r["kind"] != "unanswerable")]
            graded = [r for r in sub if r["judge_correct"] != ""]
            if graded:
                out[kind] = {"n": len(graded),
                             "mean_correctness": round(sum(r["judge_correct"] for r in graded) / len(graded), 3),
                             "mean_support": round(sum(r["judge_supported"] for r in graded) / len(graded), 3),
                             "strict_pass": round(sum(r["judge_correct"] == 1 and r["judge_supported"] == 1 for r in graded) / len(graded), 3)}
        return out

    answerable = [r for r in results if not r["should_refuse"]]
    unanswerable = [r for r in results if r["should_refuse"]]
    summary = {
        "config": ix.chosen_design(),
        "agent_model": next(iter(answers.values()))["model"] if answers else None,
        "judge_model": JUDGE_MODEL,
        "questions": len(results),
        "retrieval": retrieval_rows,
        "by_type": by_type(results),
        "judge_correct": share(results, "judge_correct"),
        "judge_supported": share(results, "judge_supported"),
        "answerable_correct": share(answerable, "judge_correct"),
        "answerable_unsupported": sum(1 for r in answerable if r["judge_supported"] == 0),
        "correct_refusals": sum(r["refused"] for r in unanswerable),
        "missed_refusals": sum(1 - r["refused"] for r in unanswerable),
        "wrong_refusals": sum(r["refused"] for r in answerable),
        "citations_valid": share([r for r in results if not r["refused"]], "citations_valid"),
        "cites_expected": share(answerable, "cites_expected"),
        "citation_guardrail_fired": sum(r["guardrail_fired"] for r in results),
        "failures": len(failures),
        "agreement": agreement(verdicts),
        "cost": {
            "mean_tokens_in": round(statistics.mean(r["tokens_in"] for r in results)) if results else 0,
            "mean_tokens_out": round(statistics.mean(r["tokens_out"] for r in results)) if results else 0,
            "mean_seconds": round(statistics.mean(r["seconds"] for r in results), 1) if results else 0,
            "median_seconds": round(statistics.median(r["seconds"] for r in results), 1) if results else 0,
            "mean_searches": round(statistics.mean(r["searches"] for r in results), 2) if results else 0,
        },
    }
    (EVAL / "summary.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps({k: v for k, v in summary.items() if k != "retrieval"}, indent=2))


if __name__ == "__main__":
    main()
