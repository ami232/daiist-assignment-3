"""
Assignment 3, evaluation stage (`uv run python main.py evaluate`).

1. Retrieval: hit rate at k = 1, 3, 5 for three designs (vector, bm25, hybrid)
   over the answerable questions. Needs no LLM calls, only cached query vectors.
2. Agent: runs agent.py's agent on every question, saves answer and tool trace.
3. Code checks: citations valid, refusals where expected, expected passage
   retrieved and cited, numbers in the answer that appear nowhere in the evidence.
4. LLM judge: Gemini with a rubric and the retrieved text as evidence.
5. Agreement between the judge and eval/human_labels.csv.

Everything is written to eval/. Answers are cached in eval/answers.jsonl and
judgements in eval/judgements.jsonl, so a second run only does what is missing.

Environment switches:
    EVAL_FRESH=1       ignore cached answers and judgements
    EVAL_SKIP_JUDGE=1  stop after the answers (grade them yourself first)
    EVAL_LIMIT=5       only the first 5 questions (a quick trial)
"""

from __future__ import annotations

import csv
import json
import os
import re
import sys
import time
from pathlib import Path

import rag

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
HUMAN = EVAL / "human_labels.csv"
ANSWERS = EVAL / "answers.jsonl"
JUDGEMENTS = EVAL / "judgements.jsonl"
KS = (1, 3, 5)

RUBRIC = """You are grading an answer from a question answering assistant that may only use retrieved passages.

For an ANSWERABLE question:
- correct: the answer states the key facts of the reference answer (numbers, units and conditions) and contradicts none of them. Extra correct detail is fine. A refusal is NOT correct.
- supported: every factual claim in the answer can be found in the EVIDENCE passages. Judge only against the evidence, never against your own knowledge. Citation labels are not claims.
For an UNANSWERABLE question (the corpus does not contain the answer):
- correct: the answer clearly says the corpus does not cover it (it starts with NOT IN CORPUS) and does not give the missing fact anyway.
- supported: no factual claim about the regulations goes beyond the evidence. Statements about which subparts the corpus covers, or that a topic is missing, are not claims about the regulations and are fine. Naming a section number that does not appear in the evidence is not supported.
Be strict about numbers. A wrong number or a dropped condition makes the answer incorrect.
Check the answer against the REFERENCE and the EVIDENCE carefully. Decide first, then write the reason in one or two sentences. Do not think out loud in the reason."""


# --------------------------------------------------------------------- loading

def read_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as handle:
        rows = [r for r in csv.DictReader(handle) if (r.get("question") or "").strip()]
    limit = int(os.environ.get("EVAL_LIMIT", "0") or 0)
    return rows[:limit] if limit else rows


def expected_pairs(row: dict) -> set[str]:
    sources = [s.strip() for s in row["expected_source"].split(";") if s.strip()]
    locations = [l.strip() for l in row["expected_location"].split(";") if l.strip()]
    if len(sources) == 1 and len(locations) > 1:
        sources = sources * len(locations)
    return {rag.normalise_label(s, l) for s, l in zip(sources, locations)}


def read_jsonl(path: Path) -> dict[str, dict]:
    if not path.is_file() or os.environ.get("EVAL_FRESH"):
        return {}
    records = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            record = json.loads(line)
            records[record["id"]] = record
    return records


def append_jsonl(path: Path, record: dict) -> None:
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


# ------------------------------------------------------------------- retrieval

def evaluate_retrieval(questions: list[dict]) -> list[dict]:
    index = rag.Index()
    answerable = [q for q in questions if q["kind"].strip().lower() != "unanswerable"]
    rows = []
    detail = []
    for design in rag.DESIGNS:
        hits_at = {k: 0 for k in KS}
        complete_at = {k: 0 for k in KS}
        multi_total = sum(1 for q in answerable if q["kind"].strip().lower() == "multi")
        words = []
        failures = 0
        for question in answerable:
            wanted = expected_pairs(question)
            try:
                ranked = index.search(question["question"], k=max(KS), design=design)
            except Exception as error:  # noqa: BLE001
                failures += 1
                print(f"  {design}: {question['id']} failed ({type(error).__name__}: {str(error)[:100]})")
                continue
            keys = [rag.normalise_label(h.source, h.location) for h in ranked]
            words.append(sum(len(h.text.split()) for h in ranked))
            first = next((i + 1 for i, key in enumerate(keys) if key in wanted), None)
            detail.append({"design": design, "id": question["id"], "first_hit_rank": first or "",
                           "expected": ";".join(sorted(wanted)), "top5": ";".join(keys)})
            for k in KS:
                found = wanted & set(keys[:k])
                hits_at[k] += bool(found)
                if question["kind"].strip().lower() == "multi":
                    complete_at[k] += wanted <= set(keys[:k])
        total = len(answerable) - failures
        for k in KS:
            rows.append({
                "design": design, "k": k, "questions": total,
                "hit_rate": round(hits_at[k] / total, 3) if total else "",
                "multi_complete_rate": round(complete_at[k] / multi_total, 3) if multi_total else "",
                "avg_words_in_prompt": round(sum(words) / len(words) * k / max(KS)) if words else "",
            })
    with (EVAL / "retrieval.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    with (EVAL / "retrieval_detail.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(detail[0]))
        writer.writeheader()
        writer.writerows(detail)
    return rows


# ---------------------------------------------------------------------- agent

def run_agent(questions: list[dict]) -> dict[str, dict]:
    import agent

    cached = read_jsonl(ANSWERS)
    todo = [q for q in questions if q["id"] not in cached]
    print(f"\nAgent: {len(cached)} answers cached, {len(todo)} to run")
    if todo:
        by_text = {q["question"]: q for q in todo}

        failed: list[str] = []

        def save(result: dict) -> None:
            row = by_text[result["question"]]
            if result.get("error"):
                # A service error is not an answer. Do not cache it, so the next run retries it.
                failed.append(row["id"])
                print(f"  {row['id']}: FAILED ({result['error'][:100]}). Not saved, run again to retry it.", flush=True)
                return
            record = {
                "id": row["id"], "question": result["question"], "answer": result["answer"],
                "refused": result["refused"], "citations": result["citations"],
                "invalid_citations": result["invalid_citations"], "guardrail": result["guardrail"],
                "searches": [t["args"].get("query", "") for t in result["tool_calls"] if t["tool"] == "search"],
                "retrieved": [{"source": p["source"], "location": p["location"], "text": p["text"]}
                              for p in result["retrieved"]],
                "input_tokens": result["input_tokens"], "output_tokens": result["output_tokens"],
                "seconds": result["seconds"], "model": result["model"], "error": result.get("error", ""),
            }
            append_jsonl(ANSWERS, record)
            cached[row["id"]] = record
            tag = "refused" if record["refused"] else f"{len(record['citations'])} citations"
            print(f"  {row['id']} ({row['kind']}): {tag}, {record['seconds']}s", flush=True)

        # Never let the evaluation add documents: the index must stay as committed.
        agent.ask_many([q["question"] for q in todo], approve=lambda tool, args: False, on_result=save)
        if failed:
            print(f"\n{len(failed)} questions failed because of service errors: {', '.join(failed)}. "
                  f"Run the command again in a few minutes. Answers already saved are kept.")

    # A plain file for grading by hand, with no judge verdicts in it.
    with (EVAL / "answers_for_grading.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(["id", "kind", "question", "reference_answer", "agent_answer"])
        for row in questions:
            writer.writerow([row["id"], row["kind"], row["question"], row["reference_answer"],
                             cached.get(row["id"], {}).get("answer", "")])
    return cached


# ----------------------------------------------------------------- code checks

NUMBER = re.compile(r"\d[\d,]*(?:\.\d+)?")


def code_checks(row: dict, record: dict) -> dict:
    wanted = expected_pairs(row)
    unanswerable = row["kind"].strip().lower() == "unanswerable"
    retrieved_keys = {rag.normalise_label(p["source"], p["location"]) for p in record["retrieved"]}
    cited_keys = set()
    for label in record["citations"]:
        source, location = [part.strip() for part in label.strip("[]").split("|", 1)]
        cited_keys.add(rag.normalise_label(source, location))
    refused = bool(record["refused"])

    evidence = " ".join(p["text"] for p in record["retrieved"])
    evidence_numbers = {n.rstrip(",.") for n in NUMBER.findall(evidence)}
    body = re.sub(r"\[[^\[\]|]+\|[^\[\]]+\]", "", record["answer"])   # citation labels are not claims
    answer_numbers = {n.rstrip(",.") for n in NUMBER.findall(body)}
    stray = sorted(n for n in answer_numbers if n not in evidence_numbers)

    return {
        "refused": refused,
        "citations_valid": (not record["invalid_citations"]) and (refused or bool(record["citations"])),
        "expected_retrieved": bool(wanted & retrieved_keys) if wanted else "",
        "expected_cited": bool(wanted & cited_keys) if wanted else "",
        "correct_refusal": refused if unanswerable else "",
        "wrong_refusal": refused if not unanswerable else "",
        "answered_unanswerable": (not refused) if unanswerable else "",
        "numbers_not_in_evidence": ";".join(stray),
    }


# ----------------------------------------------------------------------- judge

def judge_all(questions: list[dict], answers: dict[str, dict]) -> dict[str, dict]:
    from pydantic import BaseModel, Field

    import agent

    class Verdict(BaseModel):
        correct: bool = Field(description="Matches the reference answer (or is a proper refusal for an unanswerable question).")
        supported: bool = Field(description="Every claim in the answer is found in the evidence.")
        reason: str = Field(description="One or two plain sentences explaining the verdict.")

    cached = read_jsonl(JUDGEMENTS)
    todo = [q for q in questions if q["id"] not in cached and q["id"] in answers]
    print(f"\nJudge: {len(cached)} verdicts cached, {len(todo)} to run")
    if todo:
        judge = agent.build_model().with_structured_output(Verdict)
        for row in todo:
            record = answers[row["id"]]
            evidence = "\n\n".join(f"[{p['source']} | {p['location']}]\n{p['text']}" for p in record["retrieved"])[:60000]
            prompt = (
                f"{RUBRIC}\n\nKIND: {row['kind']}\nQUESTION: {row['question']}\n"
                f"REFERENCE ANSWER: {row['reference_answer']}\n\nANSWER TO GRADE:\n{record['answer']}\n\n"
                f"EVIDENCE (the only text the assistant was allowed to use):\n{evidence or '(nothing was retrieved)'}"
            )
            verdict = None
            for attempt in range(3):
                try:
                    verdict = judge.invoke(prompt)
                    if verdict is not None:
                        break
                except Exception as error:  # noqa: BLE001
                    print(f"  judge retry for {row['id']} ({type(error).__name__}: {str(error)[:100]})")
                    time.sleep(5 * (attempt + 1))
            if verdict is None:
                continue
            result = {"id": row["id"], "correct": bool(verdict.correct), "supported": bool(verdict.supported),
                      "reason": verdict.reason}
            append_jsonl(JUDGEMENTS, result)
            cached[row["id"]] = result
            print(f"  {row['id']}: correct={result['correct']} supported={result['supported']}", flush=True)
    return cached


# ------------------------------------------------------------------- agreement

def kappa(a: list[int], b: list[int]) -> float | None:
    n = len(a)
    if not n:
        return None
    observed = sum(x == y for x, y in zip(a, b)) / n
    pa, pb = sum(a) / n, sum(b) / n
    expected = pa * pb + (1 - pa) * (1 - pb)
    return None if expected == 1 else round((observed - expected) / (1 - expected), 3)


def agreement(judgements: dict[str, dict]) -> dict:
    if not HUMAN.is_file():
        return {"graded": 0}
    with HUMAN.open(newline="", encoding="utf-8") as handle:
        labels = [r for r in csv.DictReader(handle) if (r.get("id") or "").strip()]
    out: dict = {"graded": 0, "disagreements": []}
    pairs = {"correct": ([], []), "supported": ([], [])}
    for label in labels:
        verdict = judgements.get(label["id"].strip())
        if not verdict:
            continue
        out["graded"] += 1
        for field in pairs:
            human, machine = int(label[field]), int(verdict[field])
            pairs[field][0].append(human)
            pairs[field][1].append(machine)
            if human != machine:
                out["disagreements"].append({"id": label["id"], "field": field, "human": human,
                                             "judge": machine, "judge_reason": verdict["reason"],
                                             "human_note": label.get("notes", "")})
    for field, (human, machine) in pairs.items():
        out[f"{field}_agreement"] = round(sum(h == m for h, m in zip(human, machine)) / len(human), 3) if human else None
        out[f"{field}_kappa"] = kappa(human, machine)
    return out


# -------------------------------------------------------------- results tables

def failure_cause(row: dict, checks: dict, verdict: dict | None) -> str:
    """A first guess at the cause. Check each one by hand and mark bad test questions yourself."""
    unanswerable = row["kind"].strip().lower() == "unanswerable"
    refused = checks["refused"]
    if verdict is None:
        return ""
    if unanswerable:
        if verdict["correct"] and verdict["supported"]:
            return ""
        if refused:
            return "refused, but added a detail from outside the evidence"
        return "answered an unanswerable question"
    if verdict["correct"] and verdict["supported"]:
        return ""
    if checks["expected_retrieved"] is False:
        return "retrieval miss"
    if refused:
        return "wrong refusal"
    if not verdict["supported"]:
        return "unsupported claim"
    return "wrong answer from the right passage"


def build_results(questions, answers, judgements) -> tuple[list[dict], dict]:
    rows = []
    for question in questions:
        record = answers.get(question["id"])
        if not record:
            continue
        checks = code_checks(question, record)
        verdict = judgements.get(question["id"])
        rows.append({
            "id": question["id"], "kind": question["kind"], "question": question["question"],
            "answer": record["answer"], **checks,
            "judge_correct": verdict["correct"] if verdict else "",
            "judge_supported": verdict["supported"] if verdict else "",
            "judge_reason": verdict["reason"] if verdict else "",
            "failure_cause": failure_cause(question, checks, verdict),
            "guardrail": record["guardrail"] or "", "searches": len(record["searches"]),
            "input_tokens": record["input_tokens"], "output_tokens": record["output_tokens"],
            "seconds": record["seconds"],
        })
    with (EVAL / "results.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    failures = [r for r in rows if r["failure_cause"]]
    with (EVAL / "failures.csv").open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=["id", "kind", "question", "answer", "failure_cause",
                                                    "judge_reason", "your_call"])
        writer.writeheader()
        for r in failures:
            writer.writerow({k: r[k] for k in ("id", "kind", "question", "answer", "failure_cause", "judge_reason")} | {"your_call": ""})

    answerable = [r for r in rows if r["kind"].strip().lower() != "unanswerable"]
    unanswerable = [r for r in rows if r["kind"].strip().lower() == "unanswerable"]
    judged = [r for r in rows if r["judge_correct"] != ""]
    n = max(len(rows), 1)
    summary = {
        "questions": len(rows),
        "judged": len(judged),
        "correct": sum(1 for r in judged if r["judge_correct"]),
        "unsupported": sum(1 for r in judged if not r["judge_supported"]),
        "answerable_correct": sum(1 for r in answerable if r["judge_correct"] is True),
        "answerable": len(answerable),
        "correct_refusals": sum(1 for r in unanswerable if r["correct_refusal"] is True),
        "unanswerable": len(unanswerable),
        "wrong_refusals": sum(1 for r in answerable if r["wrong_refusal"] is True),
        "answered_unanswerable": sum(1 for r in unanswerable if r["answered_unanswerable"] is True),
        "invalid_citation_answers": sum(1 for r in rows if not r["citations_valid"]),
        "answers_with_numbers_not_in_evidence": sum(1 for r in rows if r["numbers_not_in_evidence"]),
        "guardrail_fired": sum(1 for r in rows if r["guardrail"]),
        "expected_passage_retrieved": sum(1 for r in answerable if r["expected_retrieved"] is True),
        "avg_seconds": round(sum(r["seconds"] for r in rows) / n, 1),
        "avg_input_tokens": round(sum(r["input_tokens"] for r in rows) / n),
        "avg_output_tokens": round(sum(r["output_tokens"] for r in rows) / n),
        "failure_causes": {},
    }
    for r in failures:
        summary["failure_causes"][r["failure_cause"]] = summary["failure_causes"].get(r["failure_cause"], 0) + 1
    return rows, summary


def write_summary(summary: dict, retrieval: list[dict], human: dict) -> None:
    (EVAL / "summary.json").write_text(json.dumps({**summary, "human_agreement": human}, indent=2), encoding="utf-8")
    lines = ["# Evaluation summary", "", "## Retrieval (answerable questions)", "",
             "| design | k | hit rate | multi complete | words in prompt |", "|---|---|---|---|---|"]
    for r in retrieval:
        lines.append(f"| {r['design']} | {r['k']} | {r['hit_rate']} | {r['multi_complete_rate']} | {r['avg_words_in_prompt']} |")
    lines += ["", "## End to end", ""]
    for key in ("questions", "correct", "unsupported", "answerable_correct", "answerable", "correct_refusals",
                "unanswerable", "wrong_refusals", "answered_unanswerable", "invalid_citation_answers",
                "answers_with_numbers_not_in_evidence", "guardrail_fired", "expected_passage_retrieved",
                "avg_seconds", "avg_input_tokens", "avg_output_tokens"):
        lines.append(f"- {key.replace('_', ' ')}: {summary[key]}")
    lines += ["", "## Failures by cause", ""]
    lines += [f"- {cause}: {count}" for cause, count in summary["failure_causes"].items()] or ["- none"]
    lines += ["", "## Judge against my grades", ""]
    if human.get("graded"):
        lines += [f"- graded answers compared: {human['graded']}",
                  f"- agreement on correct: {human['correct_agreement']} (kappa {human['correct_kappa']})",
                  f"- agreement on supported: {human['supported_agreement']} (kappa {human['supported_kappa']})"]
        for d in human["disagreements"]:
            lines.append(f"- {d['id']} {d['field']}: I said {d['human']}, judge said {d['judge']}. Judge: {d['judge_reason']}")
    else:
        lines.append("- no graded answers found in eval/human_labels.csv yet")
    (EVAL / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


# ------------------------------------------------------------------------ main

def main() -> int:
    questions = read_questions()
    print(f"{len(questions)} questions")

    print("\nRetrieval")
    retrieval = evaluate_retrieval(questions)
    for r in retrieval:
        print(f"  {r['design']:7} k={r['k']}: hit rate {r['hit_rate']}, multi complete {r['multi_complete_rate']}")

    answers = run_agent(questions)
    if os.environ.get("EVAL_SKIP_JUDGE"):
        print("\nEVAL_SKIP_JUDGE is set. Grade eval/answers_for_grading.csv in eval/human_labels.csv, then run again.")
        return 0

    judgements = judge_all(questions, answers)
    rows, summary = build_results(questions, answers, judgements)
    human = agreement(judgements)
    write_summary(summary, retrieval, human)

    print("\nSummary")
    print(json.dumps(summary, indent=2))
    if human.get("graded"):
        print(f"\nJudge vs you on {human['graded']} answers: correct {human['correct_agreement']}, supported {human['supported_agreement']}")
    else:
        print("\nNo graded answers in eval/human_labels.csv yet, so there is no agreement figure.")
    print("\nWrote eval/retrieval.csv, results.csv, failures.csv, summary.md and summary.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
