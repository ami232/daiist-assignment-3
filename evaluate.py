"""
Assignment 3: evaluation (`main.py evaluate`).

1. Hit rate at k = 1, 3, 5 for both chunking designs.
2. Run the agent on every question in eval/questions.csv.
3. Code checks: citations present, refusals match unanswerable label.
4. LLM judge with rubric.
5. Agreement with eval/human_labels.csv.
6. Save results and summary to eval/.
"""

import csv
import json
import sys
import time
from pathlib import Path

from google import genai

from api_key import load_api_key
from index import search_index

ROOT = Path(__file__).resolve().parent
EVAL_DIR = ROOT / "eval"
QUESTIONS_FILE = EVAL_DIR / "questions.csv"
RESULTS_FILE = EVAL_DIR / "results.csv"
SUMMARY_FILE = EVAL_DIR / "summary.json"
HUMAN_LABELS_FILE = EVAL_DIR / "human_labels.csv"

JUDGE_MODEL = "gemini-3.5-flash"

JUDGE_RUBRIC = """\
You are evaluating an AI assistant's answer about music copyright law.

Given the question, the reference answer, the assistant's answer and the
retrieved passages, choose exactly ONE verdict:

  correct          – factually right, matches the reference.
  partially_correct – partly right but misses key details or has minor errors.
  incorrect        – wrong or contradicts the reference.
  correct_refusal  – the question is unanswerable and the assistant correctly
                     refused or said it does not know.
  wrong_refusal    – the question IS answerable but the assistant refused.
  unsupported_claim – the answer makes claims not grounded in the passages.

Also assess:
  has_citations  (true / false) – does the answer cite sources?
  correct_jurisdiction (true / false) – is the jurisdiction (US / EU / UK)
      correctly identified, or N/A for refusals?

Respond with ONLY a JSON object (no markdown fences):
{"verdict":"…","has_citations":true,"correct_jurisdiction":true,"explanation":"…"}
"""


# ---------------------------------------------------------------------------
# helpers
# ---------------------------------------------------------------------------

def _load_questions() -> list[dict]:
    rows: list[dict] = []
    with QUESTIONS_FILE.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if (r.get("question") or "").strip():
                rows.append(r)
    return rows


def _load_human_labels() -> dict[str, dict]:
    labels: dict[str, dict] = {}
    if HUMAN_LABELS_FILE.is_file():
        with HUMAN_LABELS_FILE.open(newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                if r.get("id"):
                    labels[r["id"]] = r
    return labels


# ---------------------------------------------------------------------------
# 1  Retrieval hit rate
# ---------------------------------------------------------------------------

def _hit_rate(questions: list[dict], collection: str) -> dict[int, float]:
    """Fraction of answerable questions where at least one expected source
    appears in the top-k results."""
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    if not answerable:
        return {1: 0, 3: 0, 5: 0}

    ks = [1, 3, 5]
    hits = {k: 0 for k in ks}

    for q in answerable:
        expected = {s.strip() for s in q["expected_source"].split(";") if s.strip()}
        results = search_index(q["question"], k=max(ks), collection_name=collection)
        for k in ks:
            sources_at_k = {r["source"] for r in results[:k]}
            if sources_at_k & expected:
                hits[k] += 1
        time.sleep(0.3)

    return {k: round(hits[k] / len(answerable), 4) for k in ks}


# ---------------------------------------------------------------------------
# 2  Run agent
# ---------------------------------------------------------------------------

def _run_agent(questions: list[dict]) -> list[dict]:
    from agent import ask

    results: list[dict] = []
    for i, q in enumerate(questions):
        print(f"  [{i + 1}/{len(questions)}] {q['id']}: {q['question'][:60]}", file=sys.stderr)
        t0 = time.time()
        try:
            r = ask(q["question"], interactive=False)
            elapsed = time.time() - t0
            results.append(
                {
                    "id": q["id"],
                    "question": q["question"],
                    "kind": q["kind"],
                    "expected_source": q.get("expected_source", ""),
                    "reference_answer": q.get("reference_answer", ""),
                    "agent_answer": r["answer"],
                    "refused": r.get("refused", False),
                    "guardrail": r.get("guardrail", ""),
                    "chunks": r.get("chunks", []),
                    "tool_calls": r.get("tool_calls", []),
                    "time_s": round(elapsed, 1),
                }
            )
        except Exception as exc:
            results.append(
                {
                    "id": q["id"],
                    "question": q["question"],
                    "kind": q["kind"],
                    "expected_source": q.get("expected_source", ""),
                    "reference_answer": q.get("reference_answer", ""),
                    "agent_answer": f"ERROR: {exc}",
                    "refused": False,
                    "chunks": [],
                    "tool_calls": [],
                    "time_s": round(time.time() - t0, 1),
                }
            )
        time.sleep(1.0)   # rate-limit
    return results


# ---------------------------------------------------------------------------
# 3  Code checks
# ---------------------------------------------------------------------------

def _code_checks(results: list[dict], questions: list[dict]) -> dict:
    q_map = {q["id"]: q for q in questions}
    checks = {
        "citation_present": 0,
        "citation_missing": 0,
        "correct_refusal": 0,
        "wrong_refusal": 0,
        "missed_refusal": 0,
    }
    refusal_phrases = ("don't have enough", "i don't know", "does not cover", "corpus does not")

    for r in results:
        q = q_map.get(r["id"])
        if not q:
            continue
        is_unans = q["kind"] == "unanswerable"
        was_refused = r.get("refused", False) or any(
            p in r["agent_answer"].lower() for p in refusal_phrases
        )
        if is_unans:
            checks["correct_refusal" if was_refused else "missed_refusal"] += 1
        elif was_refused:
            checks["wrong_refusal"] += 1
        else:
            # check for any source mention in the answer
            sources = [s.strip() for s in q.get("expected_source", "").split(";") if s.strip()]
            has_cite = any(src in r["agent_answer"] for src in sources) or "[" in r["agent_answer"]
            checks["citation_present" if has_cite else "citation_missing"] += 1
    return checks


# ---------------------------------------------------------------------------
# 4  LLM judge
# ---------------------------------------------------------------------------

def _judge(question: str, reference: str, answer: str, chunks_text: str) -> dict:
    client = genai.Client(api_key=load_api_key())
    prompt = (
        f"Question: {question}\n\n"
        f"Reference answer: {reference}\n\n"
        f"Assistant's answer: {answer}\n\n"
        f"Retrieved passages:\n{chunks_text[:3000]}\n\n"
        f"{JUDGE_RUBRIC}"
    )
    for attempt in range(3):
        try:
            resp = client.models.generate_content(model=JUDGE_MODEL, contents=prompt)
            text = resp.text.strip()
            # Try to extract JSON from various formats
            if "```" in text:
                for block in text.split("```"):
                    block = block.strip()
                    if block.startswith("json"):
                        block = block[4:].strip()
                    if block.startswith("{"):
                        return json.loads(block)
            if text.startswith("{"):
                return json.loads(text)
            # Try to find JSON object anywhere in the text
            import re
            match = re.search(r'\{[^{}]*"verdict"[^{}]*\}', text)
            if match:
                return json.loads(match.group())
        except Exception as exc:
            if attempt < 2:
                wait = 5 * (attempt + 1)
                print(f"    Judge retry {attempt+1} in {wait}s: {exc.__class__.__name__}", file=sys.stderr)
                time.sleep(wait)
                continue
            return {"verdict": "error", "explanation": str(exc)}
    return {"verdict": "error", "explanation": "failed after 3 attempts"}


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------

def run_evaluation() -> None:
    questions = _load_questions()
    if not questions:
        print("ERROR: eval/questions.csv is empty.", file=sys.stderr)
        sys.exit(1)
    print(f"Loaded {len(questions)} questions.\n", file=sys.stderr)

    # 1. Retrieval comparison ---------------------------------------------------
    print("=== Retrieval hit rate ===", file=sys.stderr)
    hit_rates: dict[str, dict] = {}
    for col in ("fixed_chunks", "structure_chunks"):
        try:
            hr = _hit_rate(questions, col)
            hit_rates[col] = hr
            print(f"  {col}:  k=1 {hr[1]:.0%}  k=3 {hr[3]:.0%}  k=5 {hr[5]:.0%}", file=sys.stderr)
        except Exception as exc:
            print(f"  {col}: error – {exc}", file=sys.stderr)

    # 2. Agent answers ----------------------------------------------------------
    print("\n=== Running agent on all questions ===", file=sys.stderr)
    results = _run_agent(questions)

    # 3. Code checks ------------------------------------------------------------
    q_map = {q["id"]: q for q in questions}
    print("\n=== Code checks ===", file=sys.stderr)
    checks = _code_checks(results, questions)
    for k, v in checks.items():
        print(f"  {k}: {v}", file=sys.stderr)

    # 4. LLM judge --------------------------------------------------------------
    print("\n=== LLM judge ===", file=sys.stderr)
    verdicts: dict[str, dict] = {}
    for r in results:
        print(f"  Judging {r['id']} …", file=sys.stderr)
        ctx = "\n\n".join(
            f"[{c['source']}, {c['location']}] {c['text'][:500]}"
            for c in r.get("chunks", [])
        )
        v = _judge(r["question"], r["reference_answer"], r["agent_answer"], ctx)
        verdicts[r["id"]] = v
        time.sleep(3.0)

    # 5. Save results.csv -------------------------------------------------------
    with RESULTS_FILE.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(
            f,
            fieldnames=[
                "id", "question", "kind", "agent_answer", "refused",
                "verdict", "has_citations", "correct_jurisdiction", "time_s",
            ],
        )
        w.writeheader()
        for r in results:
            v = verdicts.get(r["id"], {})
            w.writerow(
                {
                    "id": r["id"],
                    "question": r["question"],
                    "kind": r["kind"],
                    "agent_answer": r["agent_answer"][:800],
                    "refused": r.get("refused", False),
                    "verdict": v.get("verdict", "unknown"),
                    "has_citations": v.get("has_citations", ""),
                    "correct_jurisdiction": v.get("correct_jurisdiction", ""),
                    "time_s": r.get("time_s", ""),
                }
            )

    # 6. Human-label agreement --------------------------------------------------
    human = _load_human_labels()
    agreement = None
    if human:
        agree = total = 0
        for qid, lab in human.items():
            v = verdicts.get(qid, {})
            judge_ok = 1 if v.get("verdict") in ("correct", "correct_refusal") else 0
            human_ok = int(lab.get("correct", 0))
            if judge_ok == human_ok:
                agree += 1
            total += 1
        agreement = round(agree / total, 4) if total else None
        print(f"\n  Human-judge agreement: {agree}/{total} = {agreement:.0%}", file=sys.stderr)

    # 7. Failure classification ---------------------------------------------------
    #    Categories from README: retrieval miss, wrong answer from right passage,
    #    unsupported claim, wrong refusal, bad test question.
    print("\n=== Failure classification ===", file=sys.stderr)
    failures: dict[str, list[str]] = {
        "retrieval_miss": [],
        "wrong_answer_right_passage": [],
        "unsupported_claim": [],
        "wrong_refusal": [],
    }
    for r in results:
        q = q_map.get(r["id"])
        if not q:
            continue
        v = verdicts.get(r["id"], {})
        verdict = v.get("verdict", "unknown")
        if verdict in ("correct", "correct_refusal"):
            continue  # not a failure

        expected = {s.strip() for s in q.get("expected_source", "").split(";") if s.strip()}
        retrieved = {c["source"] for c in r.get("chunks", [])}
        hit = bool(retrieved & expected)

        if verdict == "wrong_refusal":
            failures["wrong_refusal"].append(r["id"])
        elif verdict == "unsupported_claim":
            failures["unsupported_claim"].append(r["id"])
        elif not hit and q["kind"] != "unanswerable":
            failures["retrieval_miss"].append(r["id"])
        else:
            failures["wrong_answer_right_passage"].append(r["id"])

    failure_counts = {k: len(v) for k, v in failures.items()}
    for k, ids in failures.items():
        if ids:
            print(f"  {k}: {len(ids)} — {', '.join(ids)}", file=sys.stderr)

    # 8. Summary ----------------------------------------------------------------
    verdict_counts: dict[str, int] = {}
    for v in verdicts.values():
        vt = v.get("verdict", "unknown")
        verdict_counts[vt] = verdict_counts.get(vt, 0) + 1

    avg_time = round(
        sum(r.get("time_s", 0) for r in results) / max(len(results), 1), 1
    )
    total_time = round(sum(r.get("time_s", 0) for r in results), 1)

    summary = {
        "total_questions": len(questions),
        "hit_rates": hit_rates,
        "verdict_counts": verdict_counts,
        "code_checks": checks,
        "failure_classification": failure_counts,
        "avg_time_seconds": avg_time,
        "total_time_seconds": total_time,
        "human_judge_agreement": agreement,
    }
    with SUMMARY_FILE.open("w", encoding="utf-8") as f:
        json.dump(summary, f, indent=2)

    print("\n=== Summary ===", file=sys.stderr)
    print(json.dumps(summary, indent=2), file=sys.stderr)
    # Also stdout so main.py can capture it
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    run_evaluation()
