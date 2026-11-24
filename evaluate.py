"""
Assignment 3: evaluation (`main.py evaluate`).

1. Retrieval: hit rate at k = 1, 3, 5 for each design in RETRIEVAL_DESIGNS,
   plus the words each design adds to the prompt.       -> eval/retrieval.csv
2. Agent: runs agent.py on every question (add_document is never approved).
   Answers are cached, so a rerun only asks new questions. -> eval/answers.jsonl
3. Code checks: has citations, citations valid, refusal.
4. LLM judge with RUBRIC, given the retrieved text as evidence. Cached.
                                                          -> eval/judge.jsonl
5. Agreement between the judge and eval/human_labels.csv.
6. Summary and a suggested failure cause per failed question (review it!).
                                                          -> eval/results.csv, eval/summary.json

Delete eval/answers.jsonl / eval/judge.jsonl to re-run the agent / the judge.
"""

from __future__ import annotations

import asyncio
import csv
import json
import os
import re
import time
import sys
from pathlib import Path

import index
from agent import REFUSAL, citations, deny_all, is_refusal, open_agent

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
HUMAN = EVAL / "human_labels.csv"
ANSWERS = EVAL / "answers.jsonl"
JUDGE = EVAL / "judge.jsonl"
JUDGE_MODEL = os.environ.get("JUDGE_MODEL", "gemini-3.1-flash-lite")
JUDGE_FALLBACK = os.environ.get("JUDGE_FALLBACK", JUDGE_MODEL)
KS = (1, 3, 5)

# (chunking design, search mode). Hybrid and metadata filters cost no extra embeddings.
RETRIEVAL_DESIGNS = [(d, "vector") for d in index.DESIGNS] + [(index.DEFAULT_DESIGN, "hybrid")]

RUBRIC = f"""
You grade an assistant's answer to a question about EU investment-services
legislation (MiFID II, its Delegated Regulation, MiFIR, PRIIPs).

CORRECT (0 or 1)
- correct = 1 when the answer covers every key point of the reference answer.
  Small details may be missing.
- If a whole part of a multi-part question is missing, correct = 0.
- Extra detail is fine as long as it is accurate and does not contradict the
  reference.
- Question the corpus cannot answer (the reference says so): correct = 1 only
  if the answer clearly says the corpus does not cover it ("{REFUSAL}"). It may
  add one cited sentence about what the corpus covers nearby.
- An answer that presents a related rule as if it were the answer is correct = 0.
  It is correct = 1 only if it first says the corpus does not cover the question
  and labels the related rule as context, not as the answer.
- A refusal to a question the corpus can answer is always correct = 0.

SUPPORTED (0 or 1)
- supported = 1 when every claim is backed by the evidence passages. A faithful
  paraphrase is fine; exact wording is not needed.
- A claim is unsupported when the answer attributes a passage to a different
  subject, law, authority or date than the passage itself has, even if the
  words appear in the passage.
- A claim is unsupported if the passage it cites does not say it, even when a
  different evidence passage does.
- A refusal makes no factual claims, so it is supported = 1.

Give a one-sentence reason.
"""


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if (r.get("id") or "").strip()]


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def read_jsonl(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    return {r["id"]: r for r in map(json.loads, path.read_text(encoding="utf-8").splitlines()) if r}


def append_jsonl(path: Path, row: dict) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def _norm(s: str) -> str:
    return re.sub(r"\s+", " ", re.sub(r"[^\w\s]", " ", s.lower())).strip()


def _pages(s: str) -> set[int]:
    pages = set()
    for a, b in re.findall(r"pp?\.\s*(\d+)(?:\s*-\s*(\d+))?", s):
        pages |= set(range(int(a), int(b or a) + 1))
    return pages


def location_matches(expected: str, actual: str) -> bool:
    """Page ranges overlap, or the expected location's text appears in the chunk's location."""
    if not expected.strip():
        return True
    e_pages, a_pages = _pages(expected), _pages(actual)
    if e_pages and a_pages and e_pages & a_pages:
        return True
    e_text = _norm(re.sub(r"pp?\.\s*\d+(\s*-\s*\d+)?", "", expected))
    return bool(e_text) and re.search(rf"\b{re.escape(e_text)}\b", _norm(actual)) is not None


def targets(q: dict) -> list[tuple[str, str]]:
    sources = [s.strip() for s in q["expected_source"].split(";") if s.strip()]
    locations = [l.strip() for l in q["expected_location"].split(";")]
    if len(locations) != len(sources):
        locations = [q["expected_location"]] * len(sources)
    return list(zip(sources, locations))


def hit(target: tuple[str, str], hits: list[dict]) -> bool:
    return any(h["source"] == target[0] and location_matches(target[1], h["location"]) for h in hits)


# ---------------------------------------------------------------------------
# 1. Retrieval
# ---------------------------------------------------------------------------

def evaluate_retrieval(questions: list[dict]) -> list[dict]:
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    rows = []
    for design, mode in RETRIEVAL_DESIGNS:
        built = json.loads(index.MANIFEST.read_text()).get("designs", {}) if index.MANIFEST.exists() else {}
        if design not in built:
            print(f"  skipping {design}/{mode}: not fully indexed yet (run main.py index again)")
            continue
        row = {"design": design, "mode": mode}
        # Only the original corpus: documents added later (the add_document demo)
        # exist in one design but not the others, which would skew the comparison.
        corpus = [s["name"] for s in index.SOURCES]
        results = {q["id"]: index.search(q["question"], k=max(KS), design=design, mode=mode, source=corpus)
                   for q in answerable}
        for k in KS:
            any_hits = [any(hit(t, results[q["id"]][:k]) for t in targets(q)) for q in answerable]
            all_hits = [all(hit(t, results[q["id"]][:k]) for t in targets(q)) for q in answerable]
            row[f"hit@{k}"] = round(sum(any_hits) / len(answerable), 3)
            row[f"all@{k}"] = round(sum(all_hits) / len(answerable), 3)   # every expected passage found
            row[f"words@{k}"] = round(sum(sum(len(h["text"].split()) for h in results[q["id"]][:k])
                                          for q in answerable) / len(answerable))
        rows.append(row)
    write_csv(EVAL / "retrieval.csv", rows)
    return rows


# ---------------------------------------------------------------------------
# 2. Agent on every question
# ---------------------------------------------------------------------------

async def run_agent(questions: list[dict]) -> dict[str, dict]:
    done = read_jsonl(ANSWERS)
    todo = [q for q in questions if q["id"] not in done]
    if todo:
        async with open_agent() as harness:
            for q in todo:
                print(f"  {q['id']}: {q['question'][:70]}")
                try:
                    out = await harness.ask(q["question"], approve=deny_all)
                except Exception as error:  # noqa: BLE001 - record it, keep going
                    print(f"    failed: {type(error).__name__}: {error}")
                    continue
                row = {"id": q["id"], **out}
                append_jsonl(ANSWERS, row)
                done[q["id"]] = row
    return done


# ---------------------------------------------------------------------------
# 3-4. Code checks and LLM judge
# ---------------------------------------------------------------------------

def code_checks(q: dict, a: dict) -> dict:
    cited = citations(a["answer"])
    retrieved = {tuple(t) for t in a["retrieved_tags"]}
    refused = is_refusal(a["answer"])
    return {
        "refused": int(refused),
        "has_citation": int(bool(cited)),
        "citations_valid": int(all(c in retrieved for c in cited)),
        "cites_expected": int(any(hit(t, [{"source": s, "location": l} for s, l in cited]) for t in targets(q)))
        if q["kind"] != "unanswerable" else "",
        "searched": int(any(t["tool"] == "search" for t in a["trace"])),
    }


def judge(q: dict, a: dict) -> dict:
    from google.genai import errors, types

    evidence = "\n\n".join(t["output"] for t in a["trace"] if t["tool"] == "search") or "(no passages retrieved)"
    prompt = (f"{RUBRIC}\n\nQUESTION:\n{q['question']}\n\nREFERENCE ANSWER:\n{q['reference_answer']}\n\n"
              f"EVIDENCE PASSAGES:\n{evidence}\n\nASSISTANT ANSWER:\n{a['answer']}")
    schema = {"type": "object", "properties": {
        "correct": {"type": "integer", "enum": [0, 1]},
        "supported": {"type": "integer", "enum": [0, 1]},
        "reason": {"type": "string"}}, "required": ["correct", "supported", "reason"]}
    config = types.GenerateContentConfig(temperature=0, response_mime_type="application/json",
                                         response_json_schema=schema)
    for attempt, model in enumerate((JUDGE_MODEL, JUDGE_MODEL, JUDGE_FALLBACK)):   # retry, then fallback
        try:
            response = index.genai_client().models.generate_content(model=model, contents=prompt, config=config)
            break
        except errors.APIError as error:
            if error.code not in (429, 500, 503) or attempt == 2:
                raise
            time.sleep(10)
    usage = response.usage_metadata
    return {**json.loads(response.text), "judge_model": model,
            "judge_tokens": usage.total_token_count if usage else 0}


def run_judge(questions: list[dict], answers: dict[str, dict]) -> dict[str, dict]:
    verdicts = read_jsonl(JUDGE)
    for q in questions:
        if q["id"] in answers and q["id"] not in verdicts:
            print(f"  judging {q['id']}")
            verdict = {"id": q["id"], **judge(q, answers[q["id"]])}
            append_jsonl(JUDGE, verdict)
            verdicts[q["id"]] = verdict
    return verdicts


# ---------------------------------------------------------------------------
# 5. Agreement with your own labels
# ---------------------------------------------------------------------------

def kappa(a: list[int], b: list[int]) -> float | None:
    n = len(a)
    if not n:
        return None
    observed = sum(x == y for x, y in zip(a, b)) / n
    pa, pb = sum(a) / n, sum(b) / n
    expected = pa * pb + (1 - pa) * (1 - pb)
    return None if expected == 1 else round((observed - expected) / (1 - expected), 3)


def agreement(verdicts: dict[str, dict]) -> dict:
    labels = [r for r in read_csv(HUMAN) if r["id"] in verdicts]
    out = {"n": len(labels)}
    for field in ("correct", "supported"):
        pairs = [(int(r[field]), int(verdicts[r["id"]][field])) for r in labels if r.get(field, "").strip()]
        if pairs:
            human, model = zip(*pairs)
            out[field] = {"agreement": round(sum(h == m for h, m in pairs) / len(pairs), 3),
                          "kappa": kappa(list(human), list(model)),
                          "disagreements": [r["id"] for r in labels if r.get(field, "").strip()
                                            and int(r[field]) != int(verdicts[r["id"]][field])]}
    return out


# ---------------------------------------------------------------------------
# 6. Summary
# ---------------------------------------------------------------------------

def suggest_cause(q: dict, checks: dict, verdict: dict, retrieval_hit: bool) -> str:
    """A first guess only: confirm each one by reading the answer and passages."""
    unanswerable = q["kind"] == "unanswerable"
    if unanswerable:
        return "" if checks["refused"] else "unsupported claim"
    if checks["refused"]:
        return "retrieval miss" if not retrieval_hit else "wrong refusal"
    if not verdict.get("supported", 1) or not checks["citations_valid"]:
        return "unsupported claim"
    if not verdict.get("correct", 1):
        return "wrong answer from right passage" if retrieval_hit else "retrieval miss"
    return ""


def main() -> int:
    questions = [{k: (v or "").strip() for k, v in r.items()} for r in read_csv(QUESTIONS)]
    if not questions:
        print("eval/questions.csv has no questions yet.")
        return 1
    EVAL.mkdir(exist_ok=True)

    print("1. Retrieval hit rate")
    retrieval = evaluate_retrieval(questions)
    for r in retrieval:
        print("   " + "  ".join(f"{k}={v}" for k, v in r.items()))

    print("2. Agent answers")
    answers = asyncio.run(run_agent(questions))

    print("3-4. Code checks and judge")
    verdicts = run_judge(questions, answers)

    rows = []
    for q in questions:
        if q["id"] not in answers:
            continue
        a, v = answers[q["id"]], verdicts.get(q["id"], {})
        checks = code_checks(q, a)
        served = index.search(q["question"], k=5) if q["kind"] != "unanswerable" else []
        retrieval_hit = any(hit(t, served) for t in targets(q)) if served else False
        if q["kind"] == "unanswerable":   # code decides refusals; the judge is not needed for these
            v = {**v, "correct": checks["refused"]}
        rows.append({"id": q["id"], "kind": q["kind"], **checks,
                     "retrieval_hit@5": int(retrieval_hit) if q["kind"] != "unanswerable" else "",
                     "judge_correct": v.get("correct", ""), "judge_supported": v.get("supported", ""),
                     "judge_reason": v.get("reason", ""),
                     "suggested_cause": suggest_cause(q, checks, v, retrieval_hit),
                     "models": " ".join(a.get("models", [])), "judge_model": v.get("judge_model", ""),
                     "tokens": a["tokens"], "seconds": a["seconds"], "tool_calls": len(a["trace"]),
                     "guardrail_fired": int(bool(a["guardrail"])), "answer": a["answer"]})
    write_csv(EVAL / "results.csv", rows)

    n = len(rows)
    answerable = [r for r in rows if r["kind"] != "unanswerable"]
    unanswerable = [r for r in rows if r["kind"] == "unanswerable"]
    summary = {
        "questions": n,
        "correct": sum(r["judge_correct"] == 1 for r in rows),
        "unsupported": sum(r["judge_supported"] == 0 for r in rows),
        "correct_refusals": sum(r["refused"] for r in unanswerable),
        "wrong_refusals": sum(r["refused"] for r in answerable),
        "answered_unanswerable": sum(not r["refused"] for r in unanswerable),
        "invalid_citations": sum(not r["citations_valid"] for r in rows),
        "guardrail_fired": sum(r["guardrail_fired"] for r in rows),
        "by_kind": {k: {"n": len(g), "correct": sum(r["judge_correct"] == 1 for r in g)}
                    for k in sorted({r["kind"] for r in rows}) for g in [[r for r in rows if r["kind"] == k]]},
        "suggested_causes": {c: sum(r["suggested_cause"] == c for r in rows)
                             for c in sorted({r["suggested_cause"] for r in rows} - {""})},
        "mean_tokens": round(sum(r["tokens"] for r in rows) / max(n, 1)),
        "mean_seconds": round(sum(r["seconds"] for r in rows) / max(n, 1), 1),
        "judge_agreement": agreement(verdicts),
        "retrieval": retrieval,
    }
    (EVAL / "summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps({k: v for k, v in summary.items() if k != "retrieval"}, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
