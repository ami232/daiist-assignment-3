"""
Assignment 3: evaluation (`main.py evaluate`).

Stages (all resumable: results are saved as they come, so the free-tier daily
limits never lose work; set RAG_EVAL_FRESH=1 to redo answers and verdicts):

  1. retrieval  hit rate at k = 1, 3, 5 for every design x method, words added
                to the prompt; the best combination is written to
                index/config.json and used by the search tool from then on.
  2. answers    the agent (agent.py) answers every question in eval/questions.csv
                -> eval/answers.jsonl, and eval/to_grade.csv for human grading
                (answers WITHOUT the judge's verdicts).
  3. checks     code checks: searched, citations valid, refusal or not.
  4. judge      LLM judge with a rubric and the retrieved text as evidence
                -> eval/judge.jsonl
  5. report     agreement with eval/human_labels.csv, failure classification
                (eval/failures.csv), cost per question, eval/summary.md

Run only some stages with RAG_EVAL_STAGES=retrieval,report (comma-separated).
"""

from __future__ import annotations

import asyncio
import csv
import json
import os
import statistics
import sys
import time
from pathlib import Path

from settings import DESIGNS, EVAL_DIR, INDEX_DIR, JUDGE_MODEL, METHODS, REFUSAL, RETRIEVAL_CONFIG, retrieval_config

QUESTIONS = EVAL_DIR / "questions.csv"
ANSWERS = EVAL_DIR / "answers.jsonl"
JUDGE = EVAL_DIR / "judge.jsonl"
HUMAN = EVAL_DIR / "human_labels.csv"
FRESH = os.environ.get("RAG_EVAL_FRESH") == "1"
STAGES = set((os.environ.get("RAG_EVAL_STAGES") or "retrieval,answers,judge,report").split(","))
KS = (1, 3, 5)


def log(*args) -> None:
    print(*args, flush=True)


def load_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r["question"].strip()]
    for r in rows:
        r["kind"] = r["kind"].strip().lower()
        sources = [s.strip() for s in r["expected_source"].split(";") if s.strip()]
        locations = [l.strip() for l in r["expected_location"].split(";") if l.strip()]
        if len(sources) == 1 and len(locations) > 1:
            sources *= len(locations)
        r["expected"] = list(zip(sources, locations))
    return rows


def matches(chunk: dict, expected: tuple[str, str]) -> bool:
    source, section = expected
    return chunk["source"] == source and section in chunk.get("sections", [chunk["section"]])


def read_jsonl(path: Path) -> dict[str, dict]:
    if not path.is_file() or FRESH:
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


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


# ---------------------------------------------------------------- 1. retrieval

def stage_retrieval(questions: list[dict]) -> list[dict]:
    import retrieval

    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    per_question, summary = [], []
    for design in DESIGNS:
        for method in METHODS:
            hits = {k: 0 for k in KS}
            both5, multi = 0, 0
            words = {k: [] for k in KS}
            for q in answerable:
                results = retrieval.search(q["question"], k=max(KS), design=design, method=method)
                first = next((r["rank"] for r in results if any(matches(r, e) for e in q["expected"])), None)
                for k in KS:
                    hits[k] += first is not None and first <= k
                    words[k].append(sum(r["words"] for r in results[:k]))
                if q["kind"] == "multi":
                    multi += 1
                    both5 += all(any(matches(r, e) for r in results) for e in q["expected"])
                per_question.append({"id": q["id"], "kind": q["kind"], "design": design, "method": method,
                                     "first_hit_rank": first or "", "top5": " ".join(r["id"] for r in results)})
            n = len(answerable)
            summary.append({
                "design": design, "method": method,
                **{f"hit@{k}": round(hits[k] / n, 3) for k in KS},
                "multi_both@5": round(both5 / multi, 3) if multi else "",
                **{f"words@{k}": round(statistics.mean(words[k])) for k in KS},
                "chunks": len(retrieval.get_index(design).chunks),
            })
            log(f"  {design:9} {method:6} " + "  ".join(f"hit@{k}={summary[-1][f'hit@{k}']:.2f}" for k in KS)
                + f"  words@5={summary[-1]['words@5']}")
    write_csv(EVAL_DIR / "retrieval_per_question.csv", per_question)
    write_csv(EVAL_DIR / "retrieval_results.csv", summary)

    # choose by the numbers: hit@5, then hit@3, then hit@1, then fewer words in the prompt
    best = max(summary, key=lambda s: (s["hit@5"], s["hit@3"], s["hit@1"], -s["words@5"]))
    config = {"design": best["design"], "method": best["method"], "k": 5,
              "chosen_by": "evaluate.py: highest hit@5, ties broken by hit@3, hit@1, fewer words",
              "chosen_on": time.strftime("%Y-%m-%d")}
    RETRIEVAL_CONFIG.write_text(json.dumps(config, indent=2), encoding="utf-8")
    log(f"  chosen: {best['design']} + {best['method']} -> {RETRIEVAL_CONFIG.relative_to(INDEX_DIR.parent)}")
    return summary


# ------------------------------------------------------------------ 2. answers

async def stage_answers(questions: list[dict]) -> dict[str, dict]:
    from agent import Harness, always_deny

    done = read_jsonl(ANSWERS)
    if FRESH and ANSWERS.exists():
        ANSWERS.unlink()
    todo = [q for q in questions if q["id"] not in done]
    log(f"  {len(done)} answers saved, {len(todo)} to go")
    if todo:
        async with Harness(approver=always_deny) as harness:
            for q in todo:
                for attempt in range(3):
                    try:
                        result = await harness.ask(q["question"])
                        break
                    except Exception as error:  # rate limits and transient API errors
                        message = f"{type(error).__name__}: {error}"
                        if "429" in message or "RESOURCE_EXHAUSTED" in message:
                            if "PerDay" in message or attempt == 2:
                                log(f"  daily limit reached at {q['id']}; saved answers are kept, run again later")
                                return {**done, **read_jsonl(ANSWERS)}
                            time.sleep(60)
                        elif attempt == 2:
                            log(f"  {q['id']} failed: {message}")
                            result = None
                        else:
                            time.sleep(10)
                if result is None:
                    continue
                row = {"id": q["id"], "config": retrieval_config(), **result}
                append_jsonl(ANSWERS, row)
                done[q["id"]] = row
                log(f"  {q['id']} {'REFUSED ' if result['refused'] else ''}{result['seconds']}s "
                    f"{result['input_tokens'] + result['output_tokens']} tok")
                time.sleep(2)  # stay under the free tier's requests per minute
    return done


def write_to_grade(questions: list[dict], answers: dict[str, dict]) -> None:
    """Answers for YOUR grading, without the judge's verdicts."""
    rows = []
    for q in questions:
        a = answers.get(q["id"])
        if not a:
            continue
        rows.append({"id": q["id"], "kind": q["kind"], "question": q["question"],
                     "reference_answer": q["reference_answer"], "answer": a["answer"],
                     "cited": "; ".join(f"[{c['id']}] {c['location']}" for c in a["citations"]),
                     "retrieved": " ".join(a["retrieved_ids"])})
    write_csv(EVAL_DIR / "to_grade.csv", rows)


# ------------------------------------------------------------------- 3. checks

def code_checks(q: dict, a: dict, chunk_by_id: dict) -> dict:
    retrieved = set(a["retrieved_ids"])
    cited = [c["id"] for c in a["citations"]]
    expected_retrieved = (any(any(matches(chunk_by_id[i], e) for e in q["expected"]) for i in retrieved if i in chunk_by_id)
                          if q["expected"] else None)
    checks = {
        "searched": a["searches"] > 0,
        "has_citation": bool(cited),
        "citations_valid": all(c in retrieved for c in cited),
        "refused": a["refused"],
        "expected_passage_retrieved": expected_retrieved,
        "guardrail_fired": bool(a.get("guardrail")),
    }
    unanswerable = q["kind"] == "unanswerable"
    checks["correct_refusal"] = a["refused"] if unanswerable else ""
    checks["wrong_refusal"] = "" if unanswerable else a["refused"]
    return checks


# -------------------------------------------------------------------- 4. judge

RUBRIC = """You grade answers from a compliance assistant for an SEC-registered investment adviser.
The assistant may only use the retrieved passages (EVIDENCE). Grade two things, 1 or 0 each:

correct
  1 if the answer gives the same substance as the REFERENCE ANSWER: the key rule, number,
    condition or exception is right and nothing important is wrong or missing. Extra correct
    detail is fine. Wording does not matter.
  For a question the corpus cannot answer (KIND = unanswerable): 1 only if the answer clearly
    says the corpus does not contain the information (it may explain what the corpus does say),
    and does NOT supply the missing fact (no invented figures or rules).
  0 otherwise, including an answer that is right in part but wrong or missing the key point.

supported
  1 if EVERY factual claim in the answer can be found in, or directly follows from, the EVIDENCE.
  0 if any claim (a number, a condition, a rule, an example) is not in the EVIDENCE, even if
    it is true in the real world. A refusal with no claims is supported.

Return JSON: {"correct": 0 or 1, "supported": 0 or 1, "explanation": "one or two sentences;
for any 0 say exactly which part is wrong or unsupported"}."""


def evidence_text(a: dict, chunk_by_id: dict) -> str:
    seen, parts = set(), []
    for call in a["trace"]:
        for i in call.get("ids", []):
            if i in seen:
                continue
            seen.add(i)
            chunk = chunk_by_id.get(i)
            if chunk:
                parts.append(f"[{i}] {chunk['location']}\n{chunk['text']}")
    return "\n\n".join(parts) or "(no passages retrieved)"


def judge_one(client, q: dict, a: dict, chunk_by_id: dict) -> dict:
    from google.genai import types
    from pydantic import BaseModel

    class Verdict(BaseModel):
        correct: int
        supported: int
        explanation: str

    prompt = (f"{RUBRIC}\n\nKIND: {q['kind']}\nQUESTION: {q['question']}\n"
              f"REFERENCE ANSWER: {q['reference_answer']}\n\nEVIDENCE:\n{evidence_text(a, chunk_by_id)}\n\n"
              f"ANSWER TO GRADE:\n{a['answer']}")
    for attempt in range(4):
        try:
            started = time.time()
            response = client.models.generate_content(
                model=JUDGE_MODEL, contents=prompt,
                config=types.GenerateContentConfig(response_mime_type="application/json", response_schema=Verdict),
            )
            verdict = Verdict.model_validate_json(response.text)
            usage = response.usage_metadata
            return {"correct": int(bool(verdict.correct)), "supported": int(bool(verdict.supported)),
                    "explanation": verdict.explanation, "judge_model": JUDGE_MODEL,
                    "judge_tokens": (usage.total_token_count or 0) if usage else 0,
                    "judge_seconds": round(time.time() - started, 2)}
        except Exception as error:
            if attempt == 3:
                raise
            time.sleep(30 if "429" in str(error) else 5)


def stage_judge(questions: list[dict], answers: dict[str, dict], chunk_by_id: dict) -> dict[str, dict]:
    from google import genai
    from api_key import load_api_key

    verdicts = read_jsonl(JUDGE)
    if FRESH and JUDGE.exists():
        JUDGE.unlink()
    client = genai.Client(api_key=load_api_key())
    for q in questions:
        a = answers.get(q["id"])
        if not a or q["id"] in verdicts:
            continue
        checks = code_checks(q, a, chunk_by_id)
        if checks["refused"]:
            # code decides refusals: right for unanswerable questions, wrong otherwise
            verdict = {"correct": int(q["kind"] == "unanswerable"), "supported": 1,
                       "explanation": "refusal (decided by code check, not the judge)", "judge_model": "code",
                       "judge_tokens": 0, "judge_seconds": 0}
        else:
            try:
                verdict = judge_one(client, q, a, chunk_by_id)
            except Exception as error:
                log(f"  judge stopped at {q['id']}: {error}; run again later to finish")
                break
            time.sleep(2)
        row = {"id": q["id"], **verdict}
        append_jsonl(JUDGE, row)
        verdicts[q["id"]] = row
    log(f"  {len(verdicts)} verdicts")
    return verdicts


# ------------------------------------------------------------------- 5. report

def kappa(a: list[int], b: list[int]) -> float | None:
    n = len(a)
    if not n:
        return None
    po = sum(x == y for x, y in zip(a, b)) / n
    pa, pb = sum(a) / n, sum(b) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return round((po - pe) / (1 - pe), 2) if pe < 1 else None


def classify(q: dict, a: dict, checks: dict, v: dict) -> str:
    if q["kind"] != "unanswerable" and checks["refused"]:
        return "wrong refusal"
    if q["kind"] != "unanswerable" and not checks["expected_passage_retrieved"]:
        return "retrieval miss"
    if not v["supported"]:
        return "unsupported claim"
    return "wrong answer from the right passage"


def table(rows: list[dict]) -> str:
    if not rows:
        return "(none)\n"
    keys = list(rows[0].keys())
    out = ["| " + " | ".join(keys) + " |", "|" + "---|" * len(keys)]
    out += ["| " + " | ".join(str(r[k]) for k in keys) + " |" for r in rows]
    return "\n".join(out) + "\n"


def stage_report(questions, answers, verdicts, chunk_by_id, retrieval_summary) -> None:
    rows, failures = [], []
    for q in questions:
        a, v = answers.get(q["id"]), verdicts.get(q["id"])
        if not a or not v:
            continue
        checks = code_checks(q, a, chunk_by_id)
        rows.append({"id": q["id"], "kind": q["kind"], **checks, "correct": v["correct"], "supported": v["supported"],
                     "tokens": a["input_tokens"] + a["output_tokens"], "seconds": a["seconds"],
                     "judge_tokens": v["judge_tokens"], "searches": a["searches"], "explanation": v["explanation"]})
        if not (v["correct"] and v["supported"]):
            failures.append({"id": q["id"], "kind": q["kind"], "auto_cause": classify(q, a, checks, v),
                             "manual_cause": "", "question": q["question"], "answer": a["answer"][:600],
                             "judge": v["explanation"]})
    write_csv(EVAL_DIR / "results.csv", rows)
    manual = {}
    old = EVAL_DIR / "failures.csv"
    if old.is_file():  # keep causes you already corrected by hand
        with old.open(newline="", encoding="utf-8") as f:
            manual = {r["id"]: r.get("manual_cause", "") for r in csv.DictReader(f)}
    for f_ in failures:
        f_["manual_cause"] = manual.get(f_["id"], "")
    write_csv(old, failures)

    n = len(rows)
    ans = [r for r in rows if r["kind"] != "unanswerable"]
    una = [r for r in rows if r["kind"] == "unanswerable"]
    pct = lambda x, d: f"{x}/{d} ({100 * x / d:.0f}%)" if d else "0/0"
    e2e = [
        {"metric": "correct (all questions)", "value": pct(sum(r["correct"] for r in rows), n)},
        {"metric": "correct on answerable", "value": pct(sum(r["correct"] for r in ans), len(ans))},
        {"metric": "supported (every claim in retrieved text)", "value": pct(sum(r["supported"] for r in rows), n)},
        {"metric": "unsupported answers", "value": pct(sum(1 - r["supported"] for r in rows), n)},
        {"metric": "correct refusals (unanswerable refused)", "value": pct(sum(bool(r["correct_refusal"]) for r in una), len(una))},
        {"metric": "unanswerable judged correct (refused or said not covered)", "value": pct(sum(r["correct"] for r in una), len(una))},
        {"metric": "wrong refusals (answerable refused)", "value": pct(sum(bool(r["wrong_refusal"]) for r in ans), len(ans))},
        {"metric": "searched before answering", "value": pct(sum(r["searched"] for r in rows), n)},
        {"metric": "all citations valid", "value": pct(sum(r["citations_valid"] for r in rows), n)},
        {"metric": "citation guardrail fired", "value": pct(sum(r["guardrail_fired"] for r in rows), n)},
        {"metric": "expected passage among agent's retrieved (answerable)",
         "value": pct(sum(bool(r["expected_passage_retrieved"]) for r in ans), len(ans))},
    ]
    by_kind = []
    for kind in ("single", "multi", "unanswerable"):
        group = [r for r in rows if r["kind"] == kind]
        if group:
            by_kind.append({"kind": kind, "n": len(group), "correct": sum(r["correct"] for r in group),
                            "supported": sum(r["supported"] for r in group)})

    # agreement with your own grades
    agreement_rows = []
    human = {}
    if HUMAN.is_file():
        with HUMAN.open(newline="", encoding="utf-8") as f:
            human = {r["id"]: r for r in csv.DictReader(f) if (r.get("id") or "").strip()}
    judged = {r["id"]: r for r in rows}
    common = [i for i in human if i in judged and human[i].get("correct", "").strip() in {"0", "1"}]
    disagreements = []
    for field in ("correct", "supported"):
        h = [int(human[i][field]) for i in common if human[i].get(field, "").strip() in {"0", "1"}]
        j = [judged[i][field] for i in common if human[i].get(field, "").strip() in {"0", "1"}]
        if h:
            agreement_rows.append({"field": field, "n": len(h),
                                   "agreement": f"{100 * sum(x == y for x, y in zip(h, j)) / len(h):.0f}%",
                                   "cohen_kappa": kappa(h, j)})
    for i in common:
        for field in ("correct", "supported"):
            if human[i].get(field, "").strip() in {"0", "1"} and int(human[i][field]) != judged[i][field]:
                disagreements.append({"id": i, "field": field, "human": human[i][field], "judge": judged[i][field],
                                      "human_notes": human[i].get("notes", ""), "judge_explanation": judged[i]["explanation"]})

    causes = {}
    for f_ in failures:
        cause = f_["manual_cause"] or f_["auto_cause"]
        causes[cause] = causes.get(cause, 0) + 1

    tokens = [r["tokens"] for r in rows]
    seconds = [r["seconds"] for r in rows]
    cost = [{"measure": "agent tokens per question (input+output)", "mean": round(statistics.mean(tokens)) if tokens else "",
             "median": round(statistics.median(tokens)) if tokens else "", "max": max(tokens) if tokens else ""},
            {"measure": "agent seconds per question", "mean": round(statistics.mean(seconds), 1) if seconds else "",
             "median": round(statistics.median(seconds), 1) if seconds else "", "max": max(seconds) if seconds else ""},
            {"measure": "judge tokens per judged question",
             "mean": round(statistics.mean([r["judge_tokens"] for r in rows if r["judge_tokens"]] or [0])), "median": "", "max": ""},
            {"measure": "searches per question", "mean": round(statistics.mean([r["searches"] for r in rows]), 1) if rows else "",
             "median": "", "max": max((r["searches"] for r in rows), default="")}]

    config = retrieval_config()
    md = [
        "# Evaluation summary\n",
        f"Generated {time.strftime('%Y-%m-%d %H:%M')} by `main.py evaluate`. "
        f"Agent model: `{next(iter(answers.values()))['model'] if answers else '?'}`, judge model: `{JUDGE_MODEL}`. "
        f"Retrieval used by the agent: design `{config['design']}`, method `{config['method']}`, k = {config['k']}.\n",
        "## Retrieval (answerable questions)\n",
        table(retrieval_summary) if retrieval_summary else "(retrieval stage not run in this invocation; see retrieval_results.csv)\n",
        "## End to end\n", table(e2e), "\n### By kind\n", table(by_kind),
        "## Judge vs. your grades\n",
        (table(agreement_rows) if agreement_rows else "eval/human_labels.csv has no grades yet: grade eval/to_grade.csv first.\n"),
        "\n### Disagreements\n", table(disagreements),
        "## Failures by cause\n", table([{"cause": c, "count": k} for c, k in sorted(causes.items(), key=lambda x: -x[1])]),
        "\nDetails in eval/failures.csv (fill `manual_cause` where the automatic cause is wrong, e.g. `bad test question`).\n",
        "## Cost per question\n", table(cost),
    ]
    (EVAL_DIR / "summary.md").write_text("\n".join(md), encoding="utf-8")
    log(f"  wrote eval/summary.md, results.csv, failures.csv ({len(failures)} failures)")


def main() -> None:
    questions = load_questions()
    log(f"{len(questions)} questions")
    summary = []
    if "retrieval" in STAGES:
        log("1. Retrieval")
        summary = stage_retrieval(questions)
    elif (EVAL_DIR / "retrieval_results.csv").is_file():
        with (EVAL_DIR / "retrieval_results.csv").open(newline="", encoding="utf-8") as f:
            summary = list(csv.DictReader(f))

    import retrieval
    chunk_by_id = {c["id"]: c for design in DESIGNS for c in retrieval.get_index(design).chunks}

    answers = read_jsonl(ANSWERS)
    if "answers" in STAGES:
        log("2. Agent answers")
        answers = asyncio.run(stage_answers(questions))
        write_to_grade(questions, answers)
    verdicts = read_jsonl(JUDGE)
    if "judge" in STAGES:
        log("3-4. Code checks and LLM judge")
        verdicts = stage_judge(questions, answers, chunk_by_id)
    if "report" in STAGES:
        log("5. Report")
        stage_report(questions, answers, verdicts, chunk_by_id, summary)


if __name__ == "__main__":
    main()
