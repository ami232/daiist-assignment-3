"""Retrieval and end-to-end evaluation for Assignment 3.

Runs dense and hybrid retrieval on the same hand-written test questions and
the same saved chunk embeddings, measures strict evidence hit rate at k=1/3/5,
then runs the LangChain agent on every
question. Code checks citation validity/refusals; Gemini judges correctness and
support using a fixed rubric. Human labels are read only if the student has
actually filled eval/human_labels.csv.
"""

from __future__ import annotations

import csv
import json
import math
import os
import re
import statistics
import time
from pathlib import Path
from typing import Any

import pandas as pd
from google import genai
from google.genai import types

from agent import CITATION_RE, REFUSAL_PHRASE, answer_question
from api_key import load_api_key
from index import RETRIEVAL_DESIGNS, embed_query, load_index_rows, search_with_method, selected_design

ROOT = Path(__file__).resolve().parent
EVAL_DIR = ROOT / "eval"
QUESTIONS_PATH = EVAL_DIR / "questions.csv"
HUMAN_LABELS_PATH = EVAL_DIR / "human_labels.csv"
RETRIEVAL_RESULTS_PATH = EVAL_DIR / "retrieval_results.csv"
RETRIEVAL_SUMMARY_PATH = EVAL_DIR / "retrieval_summary.csv"
ANSWERS_PATH = EVAL_DIR / "answers.csv"
JUDGE_RESULTS_PATH = EVAL_DIR / "judge_results.csv"
FAILURES_PATH = EVAL_DIR / "failures.csv"
SUMMARY_PATH = EVAL_DIR / "summary.json"
JUDGE_MODEL = os.getenv("GEMINI_JUDGE_MODEL", "gemini-3.5-flash-lite")

QUESTION_COLUMNS = [
    "id",
    "question",
    "kind",
    "expected_source",
    "expected_location",
    "reference_answer",
]


JUDGE_RUBRIC = """You are grading a RAG assistant for FAA small-UAS compliance.
Use ONLY the reference answer and retrieved evidence supplied below. Do not use
outside knowledge.

Return JSON with these fields:
- correct: 1 if the final answer is materially correct against the reference answer; otherwise 0.
  For an unanswerable question, a clear corpus-limited refusal is correct.
- supported: 1 only if every substantive factual claim in the final answer is supported by the
  retrieved evidence. A refusal is supported when it does not invent factual claims.
- refusal: 1 if the answer meaningfully refuses because the indexed corpus does not support the
  requested claim; otherwise 0.
- notes: one short explanation identifying the decisive issue.

Be strict: a plausible unsupported statement is not supported. A correct fact with a fabricated or
irrelevant citation is not supported. Do not penalize concise wording that preserves the meaning.
"""


def _load_questions() -> list[dict[str, str]]:
    if not QUESTIONS_PATH.exists():
        raise FileNotFoundError(
            "eval/questions.csv is missing. The assignment requires the student to write this test set personally."
        )
    with QUESTIONS_PATH.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        missing = [c for c in QUESTION_COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            raise ValueError(f"questions.csv missing columns: {missing}")
        rows = [{k: (v or "").strip() for k, v in row.items()} for row in reader if (row.get("question") or "").strip()]
    if len(rows) < 30:
        raise ValueError(f"questions.csv has {len(rows)} questions; assignment requires at least 30")
    return rows


def _split_expected(value: str) -> list[str]:
    # Semicolon separates evidence requirements. A pipe inside one requirement
    # means "any of these manually accepted alternatives is valid".
    return [piece.strip() for piece in (value or "").split(";") if piece.strip()]


def _page_number(value: str) -> int | None:
    match = re.search(r"(?:pdf\s+page|page)\s+(\d+)", value or "", re.IGNORECASE)
    return int(match.group(1)) if match else None


def _match_one_alternative(row: dict[str, Any], source: str, location: str) -> bool:
    source_haystack = f"{row.get('doc_id', '')} {row.get('source_title', '')}".lower()
    if source.strip().lower() not in source_haystack:
        return False

    location = (location or "").strip()
    if not location or location == "*":
        return True

    # PDF extraction/page labels are sometimes shifted by a page because of
    # cover/front-matter pages. Treat +/- 1 PDF page as the same evidence
    # location while still requiring the correct document.
    expected_page = _page_number(location)
    actual_page = int(row.get("page") or 0)
    if expected_page is not None and actual_page:
        return abs(actual_page - expected_page) <= 1

    loc_haystack = f"{row.get('location', '')} {row.get('page', '')}".lower()
    return location.lower() in loc_haystack


def _match_expected_group(row: dict[str, Any], source_group: str, location_group: str) -> bool:
    sources = [x.strip() for x in source_group.split("|") if x.strip()]
    locations = [x.strip() for x in (location_group or "").split("|")]
    while len(locations) < len(sources):
        locations.append("")
    return any(_match_one_alternative(row, src, locations[i]) for i, src in enumerate(sources))


def _strict_hit(results: list[dict[str, Any]], q: dict[str, str], k: int) -> int:
    if q["kind"].lower() == "unanswerable":
        return 0
    source_groups = _split_expected(q["expected_source"])
    location_groups = _split_expected(q["expected_location"])
    if not source_groups:
        return 0
    while len(location_groups) < len(source_groups):
        location_groups.append("")
    top = results[:k]
    return int(
        all(
            any(_match_expected_group(result, source_group, location_groups[i]) for result in top)
            for i, source_group in enumerate(source_groups)
        )
    )


def retrieval_evaluation(questions: list[dict[str, str]]) -> tuple[pd.DataFrame, pd.DataFrame]:
    rows = load_index_rows()
    client = genai.Client(api_key=load_api_key())
    records: list[dict[str, Any]] = []

    for n, q in enumerate(questions, start=1):
        vector = embed_query(client, q["question"])
        for design in RETRIEVAL_DESIGNS:
            top5 = search_with_method(q["question"], vector, k=5, design=design, rows=rows)
            records.append(
                {
                    "id": q["id"],
                    "kind": q["kind"],
                    "design": design,
                    "hit_at_1": _strict_hit(top5, q, 1),
                    "hit_at_3": _strict_hit(top5, q, 3),
                    "hit_at_5": _strict_hit(top5, q, 5),
                    "prompt_words_at_5": sum(int(r.get("word_count", 0)) for r in top5),
                    "top_sources": " | ".join(r.get("doc_id", "") for r in top5),
                    "top_locations": " | ".join(r.get("location", "") for r in top5),
                }
            )
        if n == 1 or n % 5 == 0 or n == len(questions):
            print(f"Retrieval evaluation: {n}/{len(questions)} questions")

    detail = pd.DataFrame(records)
    answerable = detail[detail["kind"].str.lower() != "unanswerable"].copy()
    summary_rows: list[dict[str, Any]] = []
    for design in RETRIEVAL_DESIGNS:
        subset = answerable[answerable["design"] == design]
        all_subset = detail[detail["design"] == design]
        summary_rows.append(
            {
                "design": design,
                "answerable_questions": int(len(subset)),
                "hit_rate_at_1": float(subset["hit_at_1"].mean()) if len(subset) else 0.0,
                "hit_rate_at_3": float(subset["hit_at_3"].mean()) if len(subset) else 0.0,
                "hit_rate_at_5": float(subset["hit_at_5"].mean()) if len(subset) else 0.0,
                "mean_prompt_words_at_5": float(all_subset["prompt_words_at_5"].mean()) if len(all_subset) else 0.0,
            }
        )
    summary = pd.DataFrame(summary_rows)
    detail.to_csv(RETRIEVAL_RESULTS_PATH, index=False)
    summary.to_csv(RETRIEVAL_SUMMARY_PATH, index=False)
    return detail, summary


def _trace_evidence(trace: list[dict[str, Any]]) -> str:
    pieces = []
    for item in trace:
        if "query" in item.get("args", {}):
            pieces.append(str(item.get("result", "")))
    return "\n\n".join(pieces)


def _is_refusal(answer: str) -> bool:
    lower = answer.lower()
    return REFUSAL_PHRASE.lower() in lower or lower.startswith("i don't know") or "corpus does not" in lower


def _valid_citations(answer: str, evidence: str) -> int:
    used = set(CITATION_RE.findall(answer))
    allowed = set(CITATION_RE.findall(evidence))
    if _is_refusal(answer) and not used:
        return 1
    return int(bool(used) and used.issubset(allowed))


def _judge(client: genai.Client, q: dict[str, str], answer: str, evidence: str) -> dict[str, Any]:
    prompt = f"""{JUDGE_RUBRIC}

QUESTION KIND: {q['kind']}
QUESTION: {q['question']}
REFERENCE ANSWER: {q['reference_answer']}

RETRIEVED EVIDENCE:
{evidence[:24000]}

ASSISTANT ANSWER:
{answer}
"""
    response = None
    last_error: Exception | None = None
    for attempt in range(6):
        try:
            response = client.models.generate_content(
                model=JUDGE_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(response_mime_type="application/json"),
            )
            break
        except Exception as exc:  # API may raise ClientError/ServerError depending on status.
            last_error = exc
            message = str(exc).lower()
            transient = any(
                marker in message
                for marker in (
                    "429",
                    "resource_exhausted",
                    "rate limit",
                    "quota",
                    "503",
                    "unavailable",
                    "timeout",
                    "timed out",
                    "deadline",
                    "connection",
                )
            )
            if not transient or attempt == 5:
                raise
            # Respect a rough backoff window instead of hammering Gemini.
            wait = min(60, 12 * (attempt + 1))
            print(f"Judge API busy/rate-limited; retrying in {wait}s (attempt {attempt + 2}/6)...")
            time.sleep(wait)

    if response is None:
        raise RuntimeError(f"Judge failed after retries: {last_error}")

    text = (response.text or "").strip()
    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        match = re.search(r"\{.*\}", text, re.DOTALL)
        if not match:
            raise RuntimeError(f"Judge returned non-JSON: {text[:500]}")
        data = json.loads(match.group(0))
    def binary(value: Any) -> int:
        if isinstance(value, bool):
            return int(value)
        if isinstance(value, (int, float)):
            return int(bool(value))
        return int(str(value).strip().lower() in {"1", "true", "yes"})

    return {
        "correct": binary(data.get("correct", 0)),
        "supported": binary(data.get("supported", 0)),
        "refusal": binary(data.get("refusal", 0)),
        "notes": str(data.get("notes", "")).strip(),
    }


def _human_rows() -> dict[str, dict[str, str]]:
    if not HUMAN_LABELS_PATH.exists():
        return {}
    with HUMAN_LABELS_PATH.open(newline="", encoding="utf-8") as f:
        rows = {}
        for row in csv.DictReader(f):
            qid = (row.get("id") or "").strip()
            correct = (row.get("correct") or "").strip()
            supported = (row.get("supported") or "").strip()
            if qid and correct in {"0", "1"} and supported in {"0", "1"}:
                rows[qid] = row
        return rows


def _failure_class(
    q: dict[str, str],
    retrieval_hit5: int,
    answer: str,
    valid_citations: int,
    judge: dict[str, Any],
    human: dict[str, str] | None,
) -> str:
    if human and "bad test question" in (human.get("notes") or "").lower():
        return "bad test question"
    if q["kind"].lower() != "unanswerable" and not retrieval_hit5:
        return "retrieval miss"
    if q["kind"].lower() != "unanswerable" and _is_refusal(answer):
        return "wrong refusal"
    if not valid_citations or not judge["supported"]:
        return "unsupported claim"
    if not judge["correct"]:
        return "wrong answer from the right passage"
    return "pass"


def end_to_end_evaluation(
    questions: list[dict[str, str]], retrieval_detail: pd.DataFrame
) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame, dict[str, Any]]:
    active_design = selected_design()
    judge_client = genai.Client(api_key=load_api_key())
    human = _human_rows()

    def _load_partial(path: Path) -> list[dict[str, Any]]:
        if not path.exists() or path.stat().st_size == 0:
            return []
        try:
            return pd.read_csv(path).fillna("").to_dict("records")
        except Exception:
            return []

    answers: list[dict[str, Any]] = _load_partial(ANSWERS_PATH)
    judgments: list[dict[str, Any]] = _load_partial(JUDGE_RESULTS_PATH)
    failures: list[dict[str, Any]] = _load_partial(FAILURES_PATH)

    # Only rows that have both an answer and a judge verdict count as completed.
    answer_ids = {str(r.get("id", "")) for r in answers}
    judge_ids = {str(r.get("id", "")) for r in judgments}
    completed_ids = answer_ids & judge_ids
    if completed_ids:
        print(f"Resuming end-to-end evaluation with {len(completed_ids)} completed questions already saved.")

    active_retrieval = retrieval_detail[retrieval_detail["design"] == active_design].set_index("id")

    for n, q in enumerate(questions, start=1):
        if q["id"] in completed_ids:
            if n == 1 or n % 5 == 0 or n == len(questions):
                print(f"End-to-end evaluation: {n}/{len(questions)} questions (resume)")
            continue

        run = answer_question(q["question"], allow_add=False)
        evidence = _trace_evidence(run["trace"])
        answer = run["answer"]
        valid = _valid_citations(answer, evidence)
        refusal = int(_is_refusal(answer))
        judge = _judge(judge_client, q, answer, evidence)
        retrieval_hit5 = int(active_retrieval.loc[q["id"], "hit_at_5"]) if q["id"] in active_retrieval.index else 0
        failure = _failure_class(q, retrieval_hit5, answer, valid, judge, human.get(q["id"]))

        usage = run.get("usage", {})
        answers.append(
            {
                "id": q["id"],
                "kind": q["kind"],
                "question": q["question"],
                "answer": answer,
                "refusal": refusal,
                "valid_citations": valid,
                "guardrail_fired": int(bool(run.get("guardrail", {}).get("fired"))),
                "guardrail_reason": run.get("guardrail", {}).get("reason", ""),
                "input_tokens": int(usage.get("input_tokens", 0)),
                "output_tokens": int(usage.get("output_tokens", 0)),
                "total_tokens": int(usage.get("total_tokens", 0)),
                "elapsed_seconds": float(run.get("elapsed_seconds", 0.0)),
                "retrieved_evidence": evidence,
            }
        )
        judgments.append({"id": q["id"], **judge})
        failures.append(
            {
                "id": q["id"],
                "kind": q["kind"],
                "retrieval_hit_at_5": retrieval_hit5,
                "failure_class": failure,
                "judge_correct": judge["correct"],
                "judge_supported": judge["supported"],
                "refusal": refusal,
                "valid_citations": valid,
            }
        )

        # Checkpoint after every completed question so a rate limit or network
        # interruption never throws away the work already done.
        pd.DataFrame(answers).drop_duplicates("id", keep="last").to_csv(ANSWERS_PATH, index=False)
        pd.DataFrame(judgments).drop_duplicates("id", keep="last").to_csv(JUDGE_RESULTS_PATH, index=False)
        pd.DataFrame(failures).drop_duplicates("id", keep="last").to_csv(FAILURES_PATH, index=False)

        if n == 1 or n % 5 == 0 or n == len(questions):
            print(f"End-to-end evaluation: {n}/{len(questions)} questions")

    answers_df = pd.DataFrame(answers).drop_duplicates("id", keep="last")
    judge_df = pd.DataFrame(judgments).drop_duplicates("id", keep="last")
    failures_df = pd.DataFrame(failures).drop_duplicates("id", keep="last")
    answers_df.to_csv(ANSWERS_PATH, index=False)
    judge_df.to_csv(JUDGE_RESULTS_PATH, index=False)
    failures_df.to_csv(FAILURES_PATH, index=False)

    merged = answers_df.merge(judge_df, on="id", suffixes=("", "_judge"))
    unanswerable = merged[merged["kind"].str.lower() == "unanswerable"]
    answerable = merged[merged["kind"].str.lower() != "unanswerable"]

    agreements: list[int] = []
    correct_agreements: list[int] = []
    supported_agreements: list[int] = []
    for qid, row in human.items():
        match = judge_df[judge_df["id"] == qid]
        if match.empty:
            continue
        judged = match.iloc[0]
        ca = int(int(row["correct"]) == int(judged["correct"]))
        sa = int(int(row["supported"]) == int(judged["supported"]))
        correct_agreements.append(ca)
        supported_agreements.append(sa)
        agreements.append(int(ca and sa))

    failure_counts = failures_df["failure_class"].value_counts().to_dict()
    summary = {
        "active_retrieval_design": active_design,
        "questions": len(questions),
        "judge_correct_rate": float(judge_df["correct"].mean()) if len(judge_df) else 0.0,
        "judge_supported_rate": float(judge_df["supported"].mean()) if len(judge_df) else 0.0,
        "correct_refusal_rate": float(unanswerable["refusal"].mean()) if len(unanswerable) else 0.0,
        "wrong_refusal_rate": float(answerable["refusal"].mean()) if len(answerable) else 0.0,
        "valid_citation_rate": float(answers_df["valid_citations"].mean()) if len(answers_df) else 0.0,
        "guardrail_fire_rate": float(answers_df["guardrail_fired"].mean()) if len(answers_df) else 0.0,
        "mean_agent_seconds": float(answers_df["elapsed_seconds"].mean()) if len(answers_df) else 0.0,
        "mean_agent_total_tokens": float(answers_df["total_tokens"].mean()) if len(answers_df) else 0.0,
        "human_labels_used": len(agreements),
        "human_judge_correct_agreement": float(statistics.mean(correct_agreements)) if correct_agreements else None,
        "human_judge_supported_agreement": float(statistics.mean(supported_agreements)) if supported_agreements else None,
        "human_judge_joint_agreement": float(statistics.mean(agreements)) if agreements else None,
        "failure_counts": failure_counts,
        "judge_model": JUDGE_MODEL,
        "judge_rubric": JUDGE_RUBRIC,
    }
    SUMMARY_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return answers_df, judge_df, failures_df, summary


def main() -> None:
    EVAL_DIR.mkdir(parents=True, exist_ok=True)
    questions = _load_questions()
    print(f"Loaded {len(questions)} student-authored evaluation questions.")

    retrieval_detail, retrieval_summary = retrieval_evaluation(questions)
    print("\nRetrieval design comparison:")
    print(retrieval_summary.to_string(index=False))
    ranked = retrieval_summary.sort_values(
        ["hit_rate_at_3", "hit_rate_at_5", "hit_rate_at_1", "mean_prompt_words_at_5"],
        ascending=[False, False, False, True],
    )
    recommended = ranked.iloc[0]["design"] if len(ranked) else ""
    print(
        f"\nMetric-based recommendation: {recommended}. "
        "The assignment says the design choice is yours: review these numbers and then edit "
        "index/selected_design.json if you choose a different design."
    )

    _, _, _, summary = end_to_end_evaluation(questions, retrieval_detail)
    print("\nEnd-to-end summary:")
    print(json.dumps(summary, indent=2))
    if summary["human_labels_used"] < 20:
        print(
            "\nIMPORTANT: fewer than 20 completed human labels were found. Grade at least 20 answers "
            "yourself in eval/human_labels.csv before submission, without reading judge_results.csv first."
        )


if __name__ == "__main__":
    main()
