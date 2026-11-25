"""
Assignment 3: evaluation (`main.py evaluate`).

1. Retrieval: hit rate at k = 1, 3, 5 for each design (chunking x search method)
   and the words each adds to the prompt          -> eval/retrieval.csv
2. End to end: the agent answers every question  -> eval/answers.jsonl
3. Code checks: citations valid, expected source cited, refusal right/wrong
4. LLM judge with a rubric, retrieved text as evidence -> eval/judgements.jsonl
5. Agreement between the judge and eval/human_labels.csv
6. Failure classification and cost per question  -> eval/results.csv, eval/summary.md

Answers and verdicts are cached in eval/ and reused on re-runs (delete the
file, or pass --fresh, to redo them), so a quota hiccup loses nothing.
"""

from __future__ import annotations

import argparse
import csv
import json
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
HUMAN = EVAL / "human_labels.csv"
ANSWERS = EVAL / "answers.jsonl"
JUDGEMENTS = EVAL / "judgements.jsonl"

KS = (1, 3, 5)
RETRIEVAL_DESIGNS = [("fixed", "dense"), ("section", "dense"), ("section", "bm25"), ("fixed", "hybrid"), ("section", "hybrid")]
# A different (larger) model than the agent's flash-lite, to limit self-preference; falls back
# when the free tier is busy or its daily limit is reached. Each verdict records its model.
JUDGE_MODELS = ("gemini-3.5-flash", "gemini-3.6-flash", "gemini-flash-lite-latest", "gemini-3.1-flash-lite")

JUDGE_RUBRIC = """You grade answers of an assistant on EU drone rules. You get the question, the
reference answer written by an expert, the assistant's answer and the passages the assistant
retrieved (the only evidence it was allowed to use).

correct = 1 if the answer agrees with the reference answer on every point the reference makes:
  the same yes/no, the same numbers (mass, height, distance, age, dates) and the same conditions.
  Extra details are fine if they are not wrong. Missing a condition that the reference states
  makes it 0. If the reference says the corpus cannot answer, correct = 1 only if the assistant
  says the corpus does not cover the question and does not give a substantive answer anyway.
  If the question is answerable but the assistant refuses, correct = 0.
supported = 1 if every factual claim in the answer can be found in the retrieved passages
  (paraphrase is fine; numbers must match exactly). A refusal with no claims is supported = 1.
  Any claim not in the passages, even if true in reality, makes it 0.

Be strict on numbers and conditions, lenient on wording. Give a one-sentence reason."""


def read_csv(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if (r.get("id") or "").strip()]


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def load_jsonl(path: Path) -> dict[str, dict]:
    if not path.is_file():
        return {}
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return {r["id"]: r for r in rows}


def append_jsonl(path: Path, row: dict) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def split(value: str) -> list[str]:
    return [v.strip() for v in (value or "").split(";") if v.strip()]


def expected_pairs(q: dict) -> list[tuple[str, str]]:
    """(source, location) passages a question needs. Sources and locations pair up by position;
    a single source applies to every location."""
    sources, locations = split(q["expected_source"]), split(q["expected_location"])
    if len(sources) == 1:
        return [(sources[0], loc) for loc in locations] or [(sources[0], "")]
    if len(sources) == len(locations):
        return list(zip(sources, locations))
    return [(s, loc) for s in sources for loc in locations]


# --------------------------------------------------------------------------
# 1. Retrieval
# --------------------------------------------------------------------------

def evaluate_retrieval(questions: list[dict]) -> list[dict]:
    import rag

    answerable = [q for q in questions if q["kind"].strip().lower() != "unanswerable"]
    rows, per_question = [], []
    for design, method in RETRIEVAL_DESIGNS:
        retriever = rag.Retriever(design)
        base = {s: 1 for s in ("reg-2019-947", "reg-2019-945", "easa-amc-gm")}
        hits_any = {k: 0 for k in KS}
        hits_all = {k: 0 for k in KS}
        words5 = []
        for q in answerable:
            results = [h for h in retriever.search(q["question"], k=max(KS), method=method) if h["source"] in base]
            pairs = expected_pairs(q)
            words5.append(sum(rag.words(h["text"]) for h in results[:5]))
            first_rank = {}
            for p_i, (src, loc) in enumerate(pairs):
                for rank, h in enumerate(results, start=1):
                    if rag.is_hit(h, [src], [loc]):
                        first_rank[p_i] = rank
                        break
            for k in KS:
                found = [r for r in first_rank.values() if r <= k]
                hits_any[k] += bool(found)
                hits_all[k] += len(found) == len(pairs)
            per_question.append({"design": f"{design}+{method}", "id": q["id"], "kind": q["kind"],
                                 "ranks": json.dumps(first_rank), "top1": results[0]["location"] if results else ""})
        n = len(answerable)
        rows.append({
            "design": f"{design}+{method}", "chunks": retriever.collection.count(), "questions": n,
            **{f"hit@{k}": round(hits_any[k] / n, 3) for k in KS},
            **{f"all@{k}": round(hits_all[k] / n, 3) for k in KS},
            "words_top5": round(sum(words5) / n),
        })
        print(f"  {rows[-1]}", flush=True)
    write_csv(EVAL / "retrieval.csv", rows)
    write_csv(EVAL / "retrieval_per_question.csv", per_question)
    return rows


# --------------------------------------------------------------------------
# 2-3. Agent answers and code checks
# --------------------------------------------------------------------------

def run_agent(questions: list[dict], fresh: bool) -> dict[str, dict]:
    import os
    import agent

    # Evaluate on the base corpus only: documents added later (e.g. the U-space regulation in
    # the add-document demo) would turn unanswerable test questions into answerable ones.
    os.environ["CORPUS_BASE_ONLY"] = "1"

    if fresh:
        ANSWERS.unlink(missing_ok=True)
    done = load_jsonl(ANSWERS)
    for i, q in enumerate(questions, start=1):
        if q["id"] in done:
            continue
        print(f"  [{i}/{len(questions)}] {q['id']}: {q['question'][:70]}", flush=True)
        for attempt in range(3):
            try:
                trace = agent.answer(q["question"], approve=lambda *_: False)
                break
            except Exception as error:  # noqa: BLE001 - rate limits etc.; retry, then record
                print(f"    error ({type(error).__name__}: {str(error)[:150]}); retrying in 60s", flush=True)
                time.sleep(60)
        else:
            continue  # not recorded: retried on the next run
        row = {"id": q["id"], **trace}
        append_jsonl(ANSWERS, row)
        done[q["id"]] = row
    return done


def code_checks(q: dict, a: dict) -> dict:
    import agent

    unanswerable = q["kind"].strip().lower() == "unanswerable"
    retrieved = {tuple(r) for r in a["retrieved"]}
    cited = agent.parse_citations(a["answer"])
    valid = not agent.check_citations(a["answer"], retrieved)
    expected_sources = set(split(q["expected_source"]))
    cites_expected = any(s in expected_sources for s, _ in cited) if not unanswerable else None
    return {
        "citations": len(cited),
        "citations_valid": int(valid),
        "cites_expected_source": "" if cites_expected is None else int(cites_expected),
        "refused": int(a["refused"]),
        "correct_refusal": int(unanswerable and a["refused"]),
        "wrong_refusal": int((not unanswerable) and a["refused"]),
        "search_fallback": int(any("KEYWORD FALLBACK" in t for t in a["retrieved_text"])),
        "guardrail_fired": int(bool(a.get("guardrail_events")) and any("citation" in e for e in a["guardrail_events"])),
    }


# --------------------------------------------------------------------------
# 4. LLM judge
# --------------------------------------------------------------------------

def judge(questions: list[dict], answers: dict[str, dict], fresh: bool) -> dict[str, dict]:
    from google.genai import types
    from pydantic import BaseModel
    import index

    class Verdict(BaseModel):
        correct: int
        supported: int
        reason: str

    if fresh:
        JUDGEMENTS.unlink(missing_ok=True)
    done = load_jsonl(JUDGEMENTS)
    client = index.genai_client()
    for q in questions:
        a = answers.get(q["id"])
        if a is None or q["id"] in done:
            continue
        evidence = "\n\n".join(a["retrieved_text"])[:40000] or "(nothing retrieved)"
        prompt = (f"QUESTION:\n{q['question']}\n\nREFERENCE ANSWER:\n{q['reference_answer']}\n\n"
                  f"ASSISTANT ANSWER:\n{a['answer']}\n\nRETRIEVED PASSAGES:\n{evidence}")
        verdict, used = None, None
        for attempt in range(3):
            for model in JUDGE_MODELS:
                try:
                    response = client.models.generate_content(
                        model=model, contents=prompt,
                        config=types.GenerateContentConfig(
                            system_instruction=JUDGE_RUBRIC, temperature=0, response_mime_type="application/json",
                            response_schema=Verdict, http_options=types.HttpOptions(timeout=60000)))
                    verdict, used = Verdict.model_validate_json(response.text), model
                    break
                except Exception as error:  # noqa: BLE001
                    print(f"    judge {model} failed on {q['id']} ({str(error)[:80]})", flush=True)
            if verdict:
                break
            time.sleep(30)
        if verdict is None:
            continue
        row = {"id": q["id"], "judge_correct": int(verdict.correct), "judge_supported": int(verdict.supported),
               "judge_reason": verdict.reason, "judge_model": used}
        append_jsonl(JUDGEMENTS, row)
        done[q["id"]] = row
    return done


# --------------------------------------------------------------------------
# 5. Agreement
# --------------------------------------------------------------------------

def kappa(pairs: list[tuple[int, int]]) -> float | None:
    n = len(pairs)
    if not n:
        return None
    po = sum(a == b for a, b in pairs) / n
    pa, pb = sum(a for a, _ in pairs) / n, sum(b for _, b in pairs) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return round((po - pe) / (1 - pe), 3) if pe < 1 else 1.0


def agreement(judgements: dict[str, dict]) -> dict:
    human = {r["id"]: r for r in read_csv(HUMAN)}
    out = {"graded": 0}
    for field in ("correct", "supported"):
        pairs = [(int(h[field]), judgements[i][f"judge_{field}"]) for i, h in human.items()
                 if i in judgements and str(h.get(field, "")).strip() in ("0", "1")]
        out["graded"] = max(out["graded"], len(pairs))
        out[f"{field}_agreement"] = round(sum(a == b for a, b in pairs) / len(pairs), 3) if pairs else None
        out[f"{field}_kappa"] = kappa(pairs)
        out[f"{field}_disagreements"] = [i for i, h in human.items() if i in judgements
                                         and str(h.get(field, "")).strip() in ("0", "1")
                                         and int(h[field]) != judgements[i][f"judge_{field}"]]
    return out


# --------------------------------------------------------------------------
# 6. Failures and summary
# --------------------------------------------------------------------------

def classify(q: dict, checks: dict, verdict: dict, retrieved_hit: bool) -> str:
    """First-pass failure cause; 'bad test question' is assigned by hand in the report."""
    if not verdict:
        return "not judged"  # no verdict (judge models unavailable): not counted as a failure
    unanswerable = q["kind"].strip().lower() == "unanswerable"
    if unanswerable:
        # The grader's verdict decides; the phrase-based refusal check misses reworded refusals (q29).
        if verdict["judge_correct"] == 1 and verdict["judge_supported"] == 1:
            return ""
        return "unsupported claim" if checks["refused"] or verdict["judge_correct"] == 1 else "wrong answer (no refusal)"
    if verdict.get("judge_correct") == 1 and verdict.get("judge_supported", 1) == 1:
        return ""
    if checks["wrong_refusal"]:
        return "retrieval miss" if not retrieved_hit else "wrong refusal"
    if not retrieved_hit:
        return "retrieval miss"
    if verdict.get("judge_supported") == 0:
        return "unsupported claim"
    return "wrong answer from right passage"


GRADING_SHEET = EVAL / "grading_sheet.md"


def write_grading_sheet(questions: list[dict], answers: dict[str, dict]) -> None:
    """Everything a human grader needs, without the judge's verdicts."""
    out = ["# Grading sheet", "",
           "For each answer fill a row in eval/human_labels.csv: `correct` (1/0: matches the reference, "
           "or is a proper refusal), `supported` (1/0: every claim is in the retrieved passages below), "
           "`notes` (why, for every 0).", ""]
    for q in questions:
        a = answers.get(q["id"])
        if a is None:
            continue
        out += [f"---", "", f"## {q['id']} ({q['kind']})", "", f"**Question:** {q['question']}", "",
                f"**Reference:** {q['reference_answer']}", "", "**Agent answer:**", "", a["answer"], "",
                f"**Guardrail:** {'; '.join(a.get('guardrail_events') or []) or 'none'}", "",
                "<details><summary>Retrieved passages</summary>", ""]
        out += [t.replace("### Result", "#### Result") for t in a["retrieved_text"]]
        out += ["", "</details>", ""]
    GRADING_SHEET.write_text("\n".join(out), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fresh", action="store_true", help="re-run the agent and the judge instead of reusing eval/ caches")
    parser.add_argument("--retrieval-only", action="store_true")
    parser.add_argument("--answers-only", action="store_true",
                        help="stop after the agent's answers and the grading sheet (grade them before the judge runs)")
    args = parser.parse_args()

    import rag

    questions = read_csv(QUESTIONS)
    if not questions:
        sys.exit("eval/questions.csv has no questions yet.")
    kinds = {k: sum(q["kind"] == k for q in questions) for k in ("single", "multi", "unanswerable")}
    print(f"{len(questions)} questions: {kinds}")

    print("\n== 1. Retrieval: hit rate at k per design")
    retrieval = evaluate_retrieval(questions)
    if args.retrieval_only:
        return

    print(f"\n== 2. Agent answers ({rag.SERVED_DESIGN}+{rag.SERVED_METHOD}, k={rag.SERVED_K})")
    answers = run_agent(questions, args.fresh)
    write_grading_sheet(questions, answers)
    if args.answers_only:
        print(f"\nAnswers saved; grading sheet in {GRADING_SHEET.relative_to(ROOT)}. Judge not run.")
        return

    print("\n== 3-4. Code checks and LLM judge")
    judgements = judge(questions, answers, args.fresh)

    human = {r["id"]: r for r in read_csv(HUMAN)}
    results = []
    for q in questions:
        a = answers.get(q["id"])
        if a is None:
            continue
        checks = code_checks(q, a)
        v = judgements.get(q["id"], {})
        h = human.get(q["id"], {})
        h_verdict = ({"judge_correct": int(h["correct"]), "judge_supported": int(h["supported"])}
                     if str(h.get("correct", "")).strip() in ("0", "1") else {})
        pairs = expected_pairs(q) if q["kind"] != "unanswerable" else []
        retrieved_hit = any(rag.location_matches(loc, l) and s == src
                            for src, loc in pairs for s, l in a["retrieved"])
        results.append({
            "id": q["id"], "kind": q["kind"], **checks,
            "retrieved_expected": int(retrieved_hit) if pairs else "",
            "judge_correct": v.get("judge_correct", ""), "judge_supported": v.get("judge_supported", ""),
            "human_correct": h_verdict.get("judge_correct", ""), "human_supported": h_verdict.get("judge_supported", ""),
            "failure": classify(q, checks, v, retrieved_hit),
            "failure_human": classify(q, checks, h_verdict, retrieved_hit) if h_verdict else "",
            "tool_calls": len(a["tool_calls"]), "input_tokens": a["input_tokens"],
            "output_tokens": a["output_tokens"], "seconds": a["seconds"],
            "judge_model": v.get("judge_model", ""),
            "judge_reason": v.get("judge_reason", ""), "human_notes": h.get("notes", ""),
        })
    write_csv(EVAL / "results.csv", results)

    print("\n== 5. Agreement with human labels")
    agree = agreement(judgements)
    print(f"  {agree}")

    n = len(results)
    answerable = [r for r in results if r["kind"] != "unanswerable"]
    unanswerable = [r for r in results if r["kind"] == "unanswerable"]
    failures: dict[str, int] = {}
    failures_human: dict[str, int] = {}
    for r in results:
        if r["failure"] and r["failure"] != "not judged":
            failures[r["failure"]] = failures.get(r["failure"], 0) + 1
        if r["failure_human"]:
            failures_human[r["failure_human"]] = failures_human.get(r["failure_human"], 0) + 1
    graded = [r for r in results if r["human_correct"] != ""]
    summary = {
        "questions": n,
        "judged answers": sum(r["judge_correct"] != "" for r in results),
        "correct (judge)": sum(r["judge_correct"] == 1 for r in results),
        "answerable correct": sum(r["judge_correct"] == 1 for r in answerable),
        "answerable": len(answerable),
        "unsupported (judge)": sum(r["judge_supported"] == 0 for r in results),
        "correct refusals": sum(r["correct_refusal"] for r in unanswerable),
        "unanswerable": len(unanswerable),
        "wrong refusals": sum(r["wrong_refusal"] for r in answerable),
        "invalid citations": sum(1 - r["citations_valid"] for r in results),
        "citation guardrail fired": sum(r["guardrail_fired"] for r in results),
        "failures by cause (judge)": failures,
        "human-graded answers": len(graded),
        "correct (human)": sum(r["human_correct"] == 1 for r in graded),
        "unsupported (human)": sum(r["human_supported"] == 0 for r in graded),
        "failures by cause (human)": failures_human,
        "judge models": {m: sum(r["judge_model"] == m for r in results) for m in sorted({r["judge_model"] for r in results})},
        "mean tokens per question": round(sum(r["input_tokens"] + r["output_tokens"] for r in results) / max(n, 1)),
        "mean input tokens": round(sum(r["input_tokens"] for r in results) / max(n, 1)),
        "mean output tokens": round(sum(r["output_tokens"] for r in results) / max(n, 1)),
        "mean seconds per question": round(sum(r["seconds"] for r in results) / max(n, 1), 1),
        "mean tool calls": round(sum(r["tool_calls"] for r in results) / max(n, 1), 2),
        "judge agreement": agree,
    }
    (EVAL / "summary.json").write_text(json.dumps({"retrieval": retrieval, "end_to_end": summary}, indent=2), encoding="utf-8")

    lines = ["# Evaluation summary", "", "## Retrieval (answerable questions)", "",
             "| design | chunks | hit@1 | hit@3 | hit@5 | all@5 (multi: both passages) | words in top 5 |", "|---|---|---|---|---|---|---|"]
    lines += [f"| {r['design']} | {r['chunks']} | {r['hit@1']} | {r['hit@3']} | {r['hit@5']} | {r['all@5']} | {r['words_top5']} |" for r in retrieval]
    lines += ["", "## End to end", ""] + [f"- **{k}**: {v}" for k, v in summary.items()]
    lines += ["", "## Failures (by human labels where graded, else judge)", "",
              "| id | kind | cause (human) | cause (judge) | human notes | judge reason |", "|---|---|---|---|---|---|"]
    lines += [f"| {r['id']} | {r['kind']} | {r['failure_human']} | {r['failure']} | {r['human_notes']} | {r['judge_reason']} |"
              for r in results if r["failure"] or r["failure_human"]]
    (EVAL / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n" + "\n".join(lines))


if __name__ == "__main__":
    main()
