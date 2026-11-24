"""
Assignment 3: evaluation (`main.py evaluate`).

Stage 1, retrieval: hit rate at k = 1, 3, 5 for each retrieval design.
Stage 2, end to end:
  a. the agent answers every question  -> eval/answers.jsonl (one line per answer,
     saved as soon as it arrives; a rerun only asks the missing questions)
  b. code checks: refusals, citations that exist and were retrieved, figure check
  c. LLM judge with the rubric in eval/judge_rubric.md -> eval/judge_verdicts.csv
  d. agreement with your grades in eval/human_labels.csv
  -> eval/answers_for_labeling.csv (to grade by hand, without the judge's verdicts)
  -> eval/e2e_results.csv and eval/e2e_summary.json

Query embeddings, answers and verdicts are all saved, so running this again
costs no quota unless something is missing.
"""

from __future__ import annotations

import csv
import json
import re
import statistics
from pathlib import Path

import retrieval

ROOT = Path(__file__).resolve().parent
EVAL_DIR = ROOT / "eval"
QUESTIONS = EVAL_DIR / "questions.csv"
QUERY_VECTORS = EVAL_DIR / "query_vectors.json"

DESIGNS = ["plain", "filter"]  # design B and design C, see retrieval.py
KS = [1, 3, 5]


def load_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if (r.get("question") or "").strip()]


def query_vectors(questions: list[dict]) -> dict[str, list[float]]:
    """One embedding per question, saved as soon as it is made."""
    vectors = json.loads(QUERY_VECTORS.read_text(encoding="utf-8")) if QUERY_VECTORS.exists() else {}
    for q in questions:
        if q["question"] not in vectors:
            vectors[q["question"]] = retrieval.embed_query(q["question"])
            QUERY_VECTORS.write_text(json.dumps(vectors), encoding="utf-8")
    return vectors


def expected_passages(q: dict) -> list[tuple[str, int | None]]:
    """[(source, page)] from expected_source and expected_location, paired in order."""
    sources = [s.strip() for s in q["expected_source"].split(";") if s.strip()]
    locations = [l.strip() for l in q["expected_location"].split(";")]
    passages = []
    for i, source in enumerate(sources):
        location = locations[i] if i < len(locations) else ""
        page = re.search(r"p\.?\s*(\d+)", location)
        passages.append((source, int(page.group(1)) if page else None))
    return passages


def found(passage: tuple[str, int | None], hits: list[dict]) -> bool:
    """A hit: a chunk from the right document whose pages include the expected page."""
    source, page = passage
    for hit in hits:
        m = hit["metadata"]
        if m["source"] == source and (page is None or m["page_start"] <= page <= m["page_end"]):
            return True
    return False


def evaluate_retrieval() -> list[dict]:
    questions = [q for q in load_questions() if q["kind"].strip().lower() != "unanswerable"]
    if not questions:
        print("eval/questions.csv has no answerable questions yet.")
        return []
    vectors = query_vectors(questions)

    rows = []
    for design in DESIGNS:
        for q in questions:
            hits = retrieval.retrieve(q["question"], k=max(KS), design=design, vector=vectors[q["question"]])
            passages = expected_passages(q)
            row = {"design": design, "id": q["id"], "kind": q["kind"]}
            for k in KS:
                top = hits[:k]
                row[f"hit@{k}"] = int(all(found(p, top) for p in passages))  # every expected passage
                row[f"any@{k}"] = int(any(found(p, top) for p in passages))  # at least one
                row[f"words@{k}"] = sum(h["metadata"]["words"] for h in top)
            row["retrieved"] = "; ".join(f"{h['metadata']['source']} {h['metadata']['location']}" for h in hits)
            rows.append(row)

    with (EVAL_DIR / "retrieval_results.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    summary = []
    for design in DESIGNS:
        for kind in ["all", "single", "multi"]:
            subset = [r for r in rows if r["design"] == design and (kind == "all" or r["kind"] == kind)]
            if not subset:
                continue
            line = {"design": design, "questions": kind, "n": len(subset)}
            for k in KS:
                line[f"hit@{k}"] = round(statistics.mean(r[f"hit@{k}"] for r in subset), 3)
            line["words_added@5"] = round(statistics.mean(r["words@5"] for r in subset))
            summary.append(line)

    with (EVAL_DIR / "retrieval_summary.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary[0]))
        writer.writeheader()
        writer.writerows(summary)

    print("Retrieval hit rate (multi: every expected passage must be retrieved)")
    print(f"{'design':8} {'questions':9} {'n':>3} " + " ".join(f"{'hit@' + str(k):>6}" for k in KS) + "  words@5")
    for s in summary:
        print(
            f"{s['design']:8} {s['questions']:9} {s['n']:>3} "
            + " ".join(f"{s[f'hit@{k}']:>6.2f}" for k in KS)
            + f"  {s['words_added@5']:>7}"
        )
    return rows


# =========================================================================== end to end

ANSWERS = EVAL_DIR / "answers.jsonl"
FOR_LABELING = EVAL_DIR / "answers_for_labeling.csv"
RUBRIC = EVAL_DIR / "judge_rubric.md"
VERDICTS = EVAL_DIR / "judge_verdicts.csv"
HUMAN_LABELS = EVAL_DIR / "human_labels.csv"
E2E_RESULTS = EVAL_DIR / "e2e_results.csv"
E2E_SUMMARY = EVAL_DIR / "e2e_summary.json"

REFUSAL = "the reports in the corpus do not cover this"  # AGENTS.md rule 8
CITATION = re.compile(r"\[([a-z0-9_]+_10k_fy\d{4}),\s*(Item [0-9A-C]+, p\. [\d\-]+)\]")
RETRIEVED = re.compile(r"^Result \d+ \[([a-z0-9_]+), ([^\]]+)\]", re.M)
JUDGE_MODEL = "gemini-3.5-flash-lite"


def load_answers() -> dict[str, dict]:
    if not ANSWERS.exists():
        return {}
    answers = {}
    for line in ANSWERS.read_text(encoding="utf-8").splitlines():
        if line.strip():
            record = json.loads(line)
            answers[record["id"]] = record
    return answers


def run_agent_on_questions(questions: list[dict]) -> dict[str, dict]:
    """Ask the agent every question not answered yet; append each answer as soon as it arrives."""
    import agent

    answers = load_answers()
    todo = [q for q in questions if q["id"] not in answers]
    print(f"\nEnd to end: {len(answers)} answers saved, {len(todo)} to ask")
    for n, q in enumerate(todo, 1):
        try:
            result = agent.answer_question(q["question"], approve=lambda path: False)
        except Exception as error:  # noqa: BLE001 - keep going, retry this one next run
            while isinstance(error, BaseExceptionGroup) and error.exceptions:
                error = error.exceptions[0]  # the real cause inside the MCP task group
            print(f"  {q['id']} failed ({type(error).__name__}: {str(error)[:160]}); will retry next run")
            if "PerDay" in str(error):
                print("  Daily quota spent: stopping here. Run again after it resets (09:00 in Spain).")
                break
            continue
        record = {"id": q["id"], **result}
        with ANSWERS.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record) + "\n")
        answers[q["id"]] = record
        print(f"  [{n}/{len(todo)}] {q['id']} {result['seconds']}s, {result['tool_calls']} searches")
    return answers


def code_checks(q: dict, a: dict) -> dict:
    """What code can check without judgement."""
    answer = a["answer"]
    unanswerable = q["kind"].strip().lower() == "unanswerable"
    refused = REFUSAL in " ".join(answer.lower().split())
    cited = {(s, l) for s, l in CITATION.findall(answer)}
    retrieved = {(s, l.strip()) for s, l in RETRIEVED.findall(a.get("evidence", ""))}
    invalid = sorted(f"{s}, {l}" for s, l in cited - retrieved)
    expected = {s.strip() for s in q["expected_source"].split(";") if s.strip()}
    return {
        "refused": int(refused),
        "correct_refusal": int(unanswerable and refused),
        "wrong_refusal": int(not unanswerable and refused),
        "missed_refusal": int(unanswerable and not refused),
        "n_citations": len(cited),
        "invalid_citations": "; ".join(invalid),
        "citations_valid": int(not invalid),
        "uncited_answer": int(not unanswerable and not refused and not cited),
        "expected_sources_cited": int(expected <= {s for s, _ in cited}) if expected else "",
        "figure_check_fired": int(bool(a["guardrail"]["first_unsupported"])),
        "figures_still_unsupported": "; ".join(a["guardrail"]["still_unsupported"]),
    }


def write_for_labeling(questions: list[dict], answers: dict[str, dict]) -> None:
    """Answers to grade by hand: no judge verdicts, so they cannot sway you."""
    with FOR_LABELING.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "kind", "question", "reference_answer", "agent_answer", "retrieved_passages"])
        for q in questions:
            if q["id"] in answers:
                a = answers[q["id"]]
                writer.writerow([q["id"], q["kind"], q["question"], q["reference_answer"], a["answer"],
                                 "; ".join(f"{s}, {l}" for s, l in RETRIEVED.findall(a.get("evidence", "")))])


def rubric_text() -> str | None:
    if not RUBRIC.exists():
        return None
    text = RUBRIC.read_text(encoding="utf-8")
    return None if "TODO" in text else text


def judge(q: dict, a: dict, rubric: str) -> dict:
    """One verdict from the LLM judge: {"correct": 0/1, "supported": 0/1, "reason": "..."}."""
    from google import genai
    from google.genai import types

    from api_key import load_api_key

    prompt = (
        f"{rubric}\n\n"
        f"## Question ({q['kind']})\n{q['question']}\n\n"
        f"## Reference answer\n{q['reference_answer']}\n\n"
        f"## Retrieved passages (the only evidence the assistant had)\n{a.get('evidence') or '(none)'}\n\n"
        f"## Assistant's answer\n{a['answer']}\n\n"
        'Reply with JSON only: {"correct": 0 or 1, "supported": 0 or 1, "reason": "one or two sentences"}'
    )
    client = genai.Client(api_key=load_api_key())
    for attempt in range(12):
        try:
            response = client.models.generate_content(
                model=JUDGE_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(temperature=0, response_mime_type="application/json"),
            )
            verdict = json.loads(response.text)
            return {
                "correct": int(verdict["correct"]),
                "supported": int(verdict["supported"]),
                "reason": str(verdict.get("reason", "")),
            }
        except Exception as error:  # noqa: BLE001
            if "PerDay" in str(error) or not any(
                code in str(error) for code in ("429", "503", "RESOURCE_EXHAUSTED", "UNAVAILABLE")
            ):
                raise
            wait = min(15 * (attempt + 1), 120)
            print(f"  judge busy ({str(error)[:40]}); waiting {wait}s")
            import time

            time.sleep(wait)
    raise RuntimeError("Judge unavailable; run again later, saved verdicts are kept.")


def judge_answers(questions: list[dict], answers: dict[str, dict], rubric: str) -> dict[str, dict]:
    """Judge every answer not judged yet with this rubric; save after each verdict."""
    import hashlib

    rubric_id = hashlib.sha1(rubric.encode()).hexdigest()[:8]
    verdicts = {}
    if VERDICTS.exists():
        with VERDICTS.open(newline="", encoding="utf-8") as f:
            verdicts = {r["id"]: r for r in csv.DictReader(f) if r["rubric"] == rubric_id}
    for q in questions:
        if q["id"] in answers and q["id"] not in verdicts:
            try:
                verdict = judge(q, answers[q["id"]], rubric)
            except Exception as error:  # noqa: BLE001 - Gemini down or quota spent: keep what we have
                print(f"  Judge stopped at {q['id']} ({str(error)[:80]}); run again later for the rest.")
                break
            verdicts[q["id"]] = {"id": q["id"], "rubric": rubric_id, **verdict}
            with VERDICTS.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["id", "rubric", "correct", "supported", "reason"])
                writer.writeheader()
                writer.writerows(verdicts.values())
    return verdicts


def agreement(verdicts: dict[str, dict]) -> dict:
    """How often your grades and the judge's agree, per criterion."""
    if not HUMAN_LABELS.exists():
        return {}
    with HUMAN_LABELS.open(newline="", encoding="utf-8") as f:
        labels = [r for r in csv.DictReader(f) if r.get("id", "").strip() in verdicts]
    result = {"n": len(labels)}
    for criterion in ("correct", "supported"):
        pairs = [(int(r[criterion]), int(verdicts[r["id"]][criterion])) for r in labels if r.get(criterion, "").strip()]
        if pairs:
            result[criterion] = round(sum(h == j for h, j in pairs) / len(pairs), 3)
            result[f"{criterion}_disagreements"] = [
                r["id"] for r in labels if r.get(criterion, "").strip() and int(r[criterion]) != int(verdicts[r["id"]][criterion])
            ]
    return result


def evaluate_end_to_end() -> None:
    questions = load_questions()
    answers = run_agent_on_questions(questions)
    write_for_labeling(questions, answers)

    rubric = rubric_text()
    verdicts = judge_answers(questions, answers, rubric) if rubric else {}
    if not rubric:
        print("No judge rubric yet (eval/judge_rubric.md); skipping the LLM judge.")

    rows = []
    for q in questions:
        if q["id"] not in answers:
            continue
        a = answers[q["id"]]
        v = verdicts.get(q["id"], {})
        rows.append({
            "id": q["id"], "kind": q["kind"],
            **code_checks(q, a),
            "judge_correct": v.get("correct", ""), "judge_supported": v.get("supported", ""),
            "judge_reason": v.get("reason", ""),
            "tool_calls": a["tool_calls"], "model_calls": a["model_calls"],
            "input_tokens": a["input_tokens"], "output_tokens": a["output_tokens"], "seconds": a["seconds"],
        })
    if not rows:
        return
    with E2E_RESULTS.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    def rate(key, subset=rows):
        values = [int(r[key]) for r in subset if r[key] != ""]
        return round(statistics.mean(values), 3) if values else None

    answerable = [r for r in rows if r["kind"] != "unanswerable"]
    unanswerable = [r for r in rows if r["kind"] == "unanswerable"]
    summary = {
        "answered": len(rows),
        "judge_correct": rate("judge_correct"),
        "judge_supported": rate("judge_supported"),
        "correct_refusals": f"{sum(r['correct_refusal'] for r in unanswerable)}/{len(unanswerable)}",
        "wrong_refusals": f"{sum(r['wrong_refusal'] for r in answerable)}/{len(answerable)}",
        "citations_valid": rate("citations_valid"),
        "expected_sources_cited": rate("expected_sources_cited", answerable),
        "figure_check_fired": sum(r["figure_check_fired"] for r in rows),
        "mean_tokens": round(statistics.mean(r["input_tokens"] + r["output_tokens"] for r in rows)),
        "mean_seconds": round(statistics.mean(r["seconds"] for r in rows), 1),
        "median_seconds": round(statistics.median(r["seconds"] for r in rows), 1),
        "agreement_with_human": agreement(verdicts) if verdicts else {},
    }
    E2E_SUMMARY.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("\nEnd-to-end summary")
    for key, value in summary.items():
        print(f"  {key}: {value}")


def main() -> None:
    evaluate_retrieval()
    evaluate_end_to_end()


if __name__ == "__main__":
    main()
