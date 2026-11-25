"""
Assignment 3: evaluation (`main.py evaluate`).

  1. Retrieval: hit rate at k = 1, 3, 5 for three designs (dense, bm25, hybrid) on the
     answerable questions. Needs only the stored vectors and one cached embedding per question.
  2. Agent: every question goes through agent.py (real MCP server, real tools).
     Answers are saved in eval/answers.jsonl as they arrive, so a crash or a rate limit loses
     nothing; a re-run only asks the questions that have no answer yet (--fresh to redo all).
  3. Code checks on every answer: searched, cited, citations really retrieved, expected passage
     retrieved, refused, call limit.
  4. LLM judge (a stronger model than the agent) with a rubric and the RETRIEVED TEXT as evidence.
  5. Agreement between the judge and your own grades in eval/human_labels.csv.

Order of work, so your grades stay independent of the judge:

    uv run python evaluate.py --answers-only    # steps 1-3 + eval/grading_sheet.md (no judge)
    ... grade 20+ answers into eval/human_labels.csv ...
    uv run python main.py evaluate              # everything, incl. judge and agreement

Writes into eval/: retrieval.csv, answers.jsonl, results.csv, failures.csv, summary.json, grading_sheet.md
"""

from __future__ import annotations

import argparse
import asyncio
import csv
import json
import os
import re
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
sys.path.insert(0, str(ROOT))

JUDGE_MODEL = os.environ.get("JUDGE_MODEL", "gemini-3.8-flash")
DESIGNS = ("dense", "bm25", "hybrid")
KS = (1, 3, 5)
REFUSAL_RE = re.compile(r"^\W*the corpus does not cover", re.IGNORECASE)

JUDGE_RUBRIC = """You grade answers from a RAG assistant that may only use retrieved passages.

You get: the QUESTION, the REFERENCE answer (what a correct answer says, or, for an unanswerable
question, that the corpus does not cover it), the EVIDENCE (the passages the assistant retrieved)
and the ANSWER to grade. Judge only against these; do not use your own knowledge of the topic.

Return:
- refused: true if the ANSWER says the corpus/documents do not cover the question (fully or for the
  whole of what was asked) and gives no substantive answer of its own.
- supported: true if EVERY factual claim in the ANSWER is stated in the EVIDENCE. A claim that is only
  in the REFERENCE, or that is true in the real world but absent from the EVIDENCE, is NOT supported.
  A pure refusal makes no claims, so it is supported.
- correct: for an answerable question, true if the ANSWER contains the key points of the REFERENCE
  (wording may differ; extra supported detail is fine; a missing key point or a contradiction makes it
  false). For an unanswerable question, true only if the ANSWER refuses and does not present an answer.
- reason: one sentence naming the missing, wrong or unsupported part, or "ok".
"""


def read_csv(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


# --------------------------------------------------------------------------
# Expected passages
# --------------------------------------------------------------------------

def pages_of(spec: str) -> set[int]:
    pages: set[int] = set()
    for a, b in re.findall(r"(\d+)(?:\s*-\s*(\d+))?", spec):
        pages.update(range(int(a), int(b or a) + 1))
    return pages


def expected_passages(q: dict) -> list[tuple[str, set[int]]]:
    sources = [s.strip() for s in q["expected_source"].split(";") if s.strip()]
    locations = [s.strip() for s in q["expected_location"].split(";")]
    locations += [locations[-1]] * (len(sources) - len(locations))
    return [(s, pages_of(loc)) for s, loc in zip(sources, locations)]


def found(passages: list[tuple[str, set[int]]], retrieved: list[tuple[str, set[int]]]) -> bool:
    """True when every expected passage overlaps some retrieved chunk of the same source."""
    return all(any(src == rs and pages & rp for rs, rp in retrieved) for src, pages in passages)


# --------------------------------------------------------------------------
# 1. Retrieval
# --------------------------------------------------------------------------

def evaluate_retrieval(questions: list[dict]) -> list[dict]:
    from retrieval import Retriever

    retriever = Retriever()
    answerable = [q for q in questions if q["kind"].strip().lower() != "unanswerable"]
    rows = []
    for design in DESIGNS:
        for k in KS:
            hits_ok = {"single": 0, "multi": 0}
            totals = {"single": 0, "multi": 0}
            words = []
            for q in answerable:
                kind = q["kind"].strip().lower()
                hits = retriever.search(q["question"], k=k, mode=design)
                retrieved = [(h.source, set(range(h.page_start, h.page_end + 1))) for h in hits]
                totals[kind] += 1
                hits_ok[kind] += found(expected_passages(q), retrieved)
                words.append(sum(len(h.text.split()) for h in hits))
            n, ok = sum(totals.values()), sum(hits_ok.values())
            rows.append({
                "design": design, "k": k, "hits": ok, "questions": n, "hit_rate": round(ok / n, 3),
                "single": f"{hits_ok['single']}/{totals['single']}", "multi": f"{hits_ok['multi']}/{totals['multi']}",
                "avg_words_in_prompt": round(sum(words) / len(words)),
            })
    write_csv(EVAL / "retrieval.csv", rows, list(rows[0]))
    print("\nRetrieval hit rate (all expected passages found in the top k)")
    print(f"{'design':<8}" + "".join(f"{'@' + str(k):>8}" for k in KS) + f"{'words@5':>10}")
    for design in DESIGNS:
        sel = {r["k"]: r for r in rows if r["design"] == design}
        print(f"{design:<8}" + "".join(f"{sel[k]['hit_rate']:>8.2f}" for k in KS) + f"{sel[5]['avg_words_in_prompt']:>10}")
    return rows


# --------------------------------------------------------------------------
# 2. Agent answers
# --------------------------------------------------------------------------

def load_answers() -> dict[str, dict]:
    path = EVAL / "answers.jsonl"
    if not path.is_file():
        return {}
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            out[row["id"]] = row
    return out


async def collect_answers(questions: list[dict], fresh: bool, pause: float) -> dict[str, dict]:
    from agent import AgentSession

    answers = {} if fresh else {k: v for k, v in load_answers().items() if not v.get("error")}
    todo = [q for q in questions if q["id"] not in answers]
    if not todo:
        print(f"\nAll {len(questions)} answers already in eval/answers.jsonl (use --fresh to redo).")
        return answers
    print(f"\nAsking the agent {len(todo)} questions ({len(answers)} already answered)")
    deny = lambda name, args: "Evaluation run: no human is available to approve changes to the index."  # noqa: E731
    async with AgentSession(approver=deny) as session:
        for q in todo:
            try:
                result = await session.ask(q["question"])
                result["error"] = None
            except Exception as error:  # noqa: BLE001 - keep going, record the failure, retry on the next run
                result = {"question": q["question"], "answer": "", "tool_calls": [], "retrieved_text": "",
                          "retrieved_citations": [], "cited": [], "model_calls": 0, "input_tokens": 0,
                          "output_tokens": 0, "seconds": 0, "hit_call_limit": False, "approvals": [],
                          "guardrail_blocks": [], "error": f"{type(error).__name__}: {str(error)[:300]}"}
            result["id"] = q["id"]
            answers[q["id"]] = result
            with (EVAL / "answers.jsonl").open("w", encoding="utf-8") as f:       # rewrite: keeps one row per id
                for row in answers.values():
                    f.write(json.dumps(row, ensure_ascii=False) + "\n")
            status = "ERROR " + result["error"] if result["error"] else f"{result['seconds']}s, {result['input_tokens']}+{result['output_tokens']} tokens"
            print(f"  {q['id']} [{q['kind']}] {status}")
            await asyncio.sleep(pause)
    return answers


# --------------------------------------------------------------------------
# 3. Code checks
# --------------------------------------------------------------------------

def retrieved_passages(answer: dict) -> list[tuple[str, set[int]]]:
    out = []
    for source, location in re.findall(r"\[([^,\]]+), ([^\]]+)\]", " ".join(answer.get("retrieved_citations", []))):
        out.append((source, pages_of(location)))
    return out


def code_checks(q: dict, a: dict) -> dict:
    refused = bool(REFUSAL_RE.match(a.get("answer", "")))
    cited, retrieved = a.get("cited", []), set(a.get("retrieved_citations", []))
    searched = any(c["name"] == "search" for c in a.get("tool_calls", []))
    answerable = q["kind"].strip().lower() != "unanswerable"
    return {
        "searched": searched,
        "refused_code": refused,
        "has_citation": bool(cited) or refused,
        "citations_valid": all(c in retrieved for c in cited),
        "expected_retrieved": found(expected_passages(q), retrieved_passages(a)) if answerable else None,
        "within_call_limit": not a.get("hit_call_limit", False),
    }


# --------------------------------------------------------------------------
# 4. Judge
# --------------------------------------------------------------------------

def judge_all(questions: list[dict], answers: dict[str, dict], pause: float) -> dict[str, dict]:
    from pydantic import BaseModel, Field

    from api_key import load_api_key
    from langchain_google_genai import ChatGoogleGenerativeAI

    class Verdict(BaseModel):
        refused: bool = Field(description="The answer says the corpus does not cover the question")
        supported: bool = Field(description="Every claim in the answer is stated in the evidence")
        correct: bool = Field(description="Matches the reference answer (or properly refuses if unanswerable)")
        reason: str = Field(description="One sentence")

    load_api_key()
    judge = ChatGoogleGenerativeAI(model=JUDGE_MODEL, temperature=0, max_retries=6).with_structured_output(Verdict)
    cache_path = EVAL / "judge_verdicts.json"
    cache = json.loads(cache_path.read_text()) if cache_path.is_file() else {}
    for q in questions:
        a = answers[q["id"]]
        key = q["id"]
        if key in cache and cache[key].get("answer_sha") == hash_text(a["answer"]):
            continue
        prompt = (
            f"{JUDGE_RUBRIC}\nQUESTION: {q['question']}\nKIND: {q['kind']}\nREFERENCE: {q['reference_answer']}\n\n"
            f"EVIDENCE:\n{a.get('retrieved_text') or '(nothing was retrieved)'}\n\nANSWER:\n{a['answer']}"
        )
        verdict = judge.invoke(prompt)
        cache[key] = {**verdict.model_dump(), "answer_sha": hash_text(a["answer"])}
        cache_path.write_text(json.dumps(cache, indent=1), encoding="utf-8")
        print(f"  judged {q['id']}: correct={verdict.correct} supported={verdict.supported} refused={verdict.refused}")
        time.sleep(pause)
    return cache


def hash_text(text: str) -> str:
    import hashlib

    return hashlib.sha256(text.encode()).hexdigest()[:12]


def outcome_of(q: dict, verdict: dict) -> str:
    answerable = q["kind"].strip().lower() != "unanswerable"
    if verdict["refused"]:
        return "wrong_refusal" if answerable else "correct_refusal"
    if not answerable:
        return "unsupported"                      # it answered a question the corpus cannot answer
    if not verdict["supported"]:
        return "unsupported"
    return "correct" if verdict["correct"] else "incorrect"


def failure_cause(outcome: str, checks: dict, answerable: bool) -> str:
    """First guess at the cause; confirm it by reading the answer (and check for a bad test question)."""
    if outcome in {"correct", "correct_refusal"}:
        return ""
    if not answerable:
        return "answered an unanswerable question"
    if checks["expected_retrieved"] is False:
        return "retrieval miss"
    return {"wrong_refusal": "wrong refusal", "unsupported": "unsupported claim", "incorrect": "wrong answer from the right passage"}[outcome]


# --------------------------------------------------------------------------
# 5. Agreement with the human grades
# --------------------------------------------------------------------------

def cohen_kappa(a: list[int], b: list[int]) -> float | None:
    n = len(a)
    if not n:
        return None
    po = sum(x == y for x, y in zip(a, b)) / n
    pa, pb = sum(a) / n, sum(b) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return None if pe == 1 else round((po - pe) / (1 - pe), 3)


def agreement(rows: list[dict]) -> dict:
    labels = {r["id"]: r for r in read_csv(EVAL / "human_labels.csv") if (r.get("id") or "").strip()}
    out = {"graded": 0}
    pairs = {"correct": ([], []), "supported": ([], [])}
    disagreements = []
    for r in rows:
        h = labels.get(r["id"])
        if not h or h.get("correct", "").strip() not in {"0", "1"}:
            continue
        out["graded"] += 1
        judge_correct = int(r["outcome"] in {"correct", "correct_refusal"})
        for name, judge_val in (("correct", judge_correct), ("supported", int(r["judge_supported"]))):
            human_val = int(h[name])
            pairs[name][0].append(human_val)
            pairs[name][1].append(judge_val)
            if human_val != judge_val:
                disagreements.append(f"{r['id']}:{name} (you {human_val}, judge {judge_val})")
    for name, (human, judge) in pairs.items():
        out[f"{name}_agreement"] = round(sum(x == y for x, y in zip(human, judge)) / len(human), 3) if human else None
        out[f"{name}_kappa"] = cohen_kappa(human, judge)
    out["disagreements"] = disagreements
    return out


# --------------------------------------------------------------------------
# Grading sheet and main
# --------------------------------------------------------------------------

def write_grading_sheet(questions: list[dict], answers: dict[str, dict]) -> None:
    lines = [
        "# Grading sheet (no judge verdicts here, on purpose)",
        "",
        "For 20+ questions fill `eval/human_labels.csv` (`id,correct,supported,notes`):",
        "`correct` = right against the reference (or a proper refusal); `supported` = every claim is in the retrieved text.",
        "Write a note for every 0.", "",
    ]
    for q in questions:
        a = answers[q["id"]]
        lines += [
            f"## {q['id']} ({q['kind']})", f"**Question:** {q['question']}", "",
            f"**Reference:** {q['reference_answer']}", "", f"**Agent answer:** {a['answer']}", "",
            f"Retrieved: {', '.join(a.get('retrieved_citations', [])) or 'nothing'}", "",
            "<details><summary>Retrieved text</summary>", "", a.get("retrieved_text", ""), "", "</details>", "",
        ]
    (EVAL / "grading_sheet.md").write_text("\n".join(lines), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate the RAG system.")
    parser.add_argument("--answers-only", action="store_true", help="stop before the judge (grade by hand first)")
    parser.add_argument("--fresh", action="store_true", help="ask every question again")
    parser.add_argument("--limit", type=int, default=0, help="only the first N questions (smoke test)")
    parser.add_argument("--pause", type=float, default=3.0, help="seconds between model calls (free-tier rate limit)")
    args = parser.parse_args()

    EVAL.mkdir(exist_ok=True)
    questions = read_csv(EVAL / "questions.csv")
    if args.limit:
        questions = questions[: args.limit]
    retrieval_rows = evaluate_retrieval(questions)
    answers = asyncio.run(collect_answers(questions, args.fresh, args.pause))
    failed = [q["id"] for q in questions if answers[q["id"]].get("error")]
    if failed:
        print(f"\n{len(failed)} questions errored ({', '.join(failed)}); run again to retry them.")
    questions = [q for q in questions if not answers[q["id"]].get("error")]
    write_grading_sheet(questions, answers)
    if args.answers_only:
        print("\nAnswers saved. Grade 20+ of them in eval/human_labels.csv (see eval/grading_sheet.md), then run main.py evaluate.")
        return

    print("\nJudging")
    verdicts = judge_all(questions, answers, args.pause)
    rows = []
    for q in questions:
        a, v = answers[q["id"]], verdicts[q["id"]]
        checks = code_checks(q, a)
        outcome = outcome_of(q, v)
        rows.append({
            "id": q["id"], "kind": q["kind"], "question": q["question"], "answer": a["answer"], "outcome": outcome,
            "judge_correct": int(v["correct"]), "judge_supported": int(v["supported"]), "judge_refused": int(v["refused"]),
            "judge_reason": v["reason"], **{f"check_{k}": v_ for k, v_ in checks.items()},
            "model_calls": a["model_calls"], "input_tokens": a["input_tokens"], "output_tokens": a["output_tokens"],
            "seconds": a["seconds"], "cause": failure_cause(outcome, checks, q["kind"].strip().lower() != "unanswerable"),
        })
    fields = list(rows[0])
    write_csv(EVAL / "results.csv", rows, fields)
    failures = [r for r in rows if r["cause"]]
    write_csv(EVAL / "failures.csv", [{**r, "manual_cause": ""} for r in failures], ["id", "kind", "question", "answer", "outcome", "cause", "manual_cause", "judge_reason"])

    n = len(rows)
    outcomes = Counter(r["outcome"] for r in rows)
    summary = {
        "questions": n,
        "outcomes": dict(outcomes),
        "causes": dict(Counter(r["cause"] for r in failures)),
        "code_checks": {k: sum(1 for r in rows if r[f"check_{k}"] is True) for k in ("searched", "has_citation", "citations_valid", "within_call_limit")},
        "judge_model": JUDGE_MODEL,
        "avg_input_tokens": round(sum(r["input_tokens"] for r in rows) / n),
        "avg_output_tokens": round(sum(r["output_tokens"] for r in rows) / n),
        "avg_model_calls": round(sum(r["model_calls"] for r in rows) / n, 2),
        "avg_seconds": round(sum(r["seconds"] for r in rows) / n, 1),
        "retrieval": retrieval_rows,
        "human_agreement": agreement(rows),
    }
    (EVAL / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(f"\n{n} questions: " + ", ".join(f"{k} {v}" for k, v in sorted(outcomes.items())))
    print("Failure causes: " + (", ".join(f"{k} {v}" for k, v in summary["causes"].items()) or "none"))
    print(f"Per question: {summary['avg_model_calls']} model calls, {summary['avg_input_tokens']} input + "
          f"{summary['avg_output_tokens']} output tokens, {summary['avg_seconds']}s")
    h = summary["human_agreement"]
    if h["graded"]:
        print(f"Agreement with your {h['graded']} grades: correct {h['correct_agreement']} (kappa {h['correct_kappa']}), "
              f"supported {h['supported_agreement']} (kappa {h['supported_kappa']})")
    else:
        print("No human grades found in eval/human_labels.csv: fill it in and run again.")


if __name__ == "__main__":
    main()
