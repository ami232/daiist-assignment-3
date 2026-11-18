"""
Assignment 3: evaluation (`main.py evaluate`).

1. Retrieval: hit rate at k = 1, 3, 5 for every chunking x method, and the
   words each adds to the prompt.            -> eval/retrieval_*.csv
2. End to end: the agent answers every question (resumable; delete
   eval/answers.jsonl to rerun from scratch).  -> eval/answers.jsonl
3. Code checks: refusal, citation present, citations valid.
4. LLM judge with the rubric in eval/judge_rubric.md and the retrieved text
   as evidence.                               -> eval/judge.jsonl
5. Agreement with your grades in eval/human_labels.csv.
6. Results, a failure list to classify, cost. -> eval/results.csv,
   eval/failures.csv, eval/summary.md

Answers and verdicts are cached, so rerunning costs nothing unless you
delete those files.
"""

import csv
import itertools
import json
import os
import sys
import time
from pathlib import Path

import config as C
from agent import CITE, answer, check_citations, is_refusal, retrieved_citations
from index import collection
from retrieval import Retriever

Q_FILE = C.EVAL_DIR / "questions.csv"
HUMAN = C.EVAL_DIR / "human_labels.csv"
RUBRIC = C.EVAL_DIR / "judge_rubric.md"
ANSWERS = C.EVAL_DIR / "answers.jsonl"
JUDGE = C.EVAL_DIR / "judge.jsonl"
PAUSE = float(os.environ.get("EVAL_PAUSE", "6"))       # seconds between questions (free-tier RPM)
KS = (1, 3, 5)


def log(*a):
    print(*a, flush=True)


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return [{k: (v or "").strip() for k, v in r.items()} for r in csv.DictReader(f) if (r.get("id") or "").strip()]


def write_csv(path: Path, rows: list[dict], fields: list[str] | None = None) -> None:
    if not rows and not fields:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields or list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def read_jsonl(path: Path) -> dict:
    out = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                out[r["id"]] = r
    return out


def append_jsonl(path: Path, row: dict) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def split(v: str) -> list[str]:
    return [x.strip() for x in v.split(";") if x.strip()]


def expected_pairs(q: dict) -> list[tuple[str, str | None]]:
    """[(doc_id, page or None)] the question needs."""
    srcs, locs = split(q["expected_source"]), split(q["expected_location"])
    if not locs:
        return [(s, None) for s in srcs]
    if len(srcs) == len(locs):
        return list(zip(srcs, locs))
    return list(itertools.product(srcs, locs))


def covers(meta: dict, pair: tuple[str, str | None]) -> bool:
    doc, page = pair
    return meta["doc_id"] == doc and (page is None or page in meta["pages"].split(","))


# ---------------------------------------------------------------------------
# 1. Retrieval
# ---------------------------------------------------------------------------
def retrieval_eval(questions: list[dict]) -> list[dict]:
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    per_q, summary = [], []
    for chunking in C.CHUNKINGS:
        if collection(chunking).count() == 0:
            log(f"  {chunking}: no chunks in the index, skipped")
            continue
        for method in C.METHODS:
            r = Retriever(chunking, method)
            hits = {k: 0 for k in KS}
            all_hits = {k: 0 for k in KS}
            words = {k: 0 for k in KS}
            for q in answerable:
                res = r.search(q["question"], max(KS))
                pairs = expected_pairs(q)
                row = {"id": q["id"], "kind": q["kind"], "chunking": chunking, "method": method}
                for k in KS:
                    top = [h["metadata"] for h in res[:k]]
                    any_hit = any(covers(m, p) for m in top for p in pairs)
                    every = all(any(covers(m, p) for m in top) for p in pairs)
                    hits[k] += any_hit
                    all_hits[k] += every
                    words[k] += sum(len(h["text"].split()) for h in res[:k])
                    row[f"hit@{k}"] = int(any_hit)
                    row[f"all@{k}"] = int(every)
                row["top5"] = " ".join(f"{m['doc_id']}:{m['page']}" for m in (h["metadata"] for h in res))
                per_q.append(row)
            n = len(answerable)
            s = {"chunking": chunking, "method": method, "questions": n}
            for k in KS:
                s[f"hit@{k}"] = round(hits[k] / n, 3)
            for k in KS:
                s[f"all_passages@{k}"] = round(all_hits[k] / n, 3)
            for k in KS:
                s[f"words_in_prompt@{k}"] = round(words[k] / n)
            summary.append(s)
            log(f"  {chunking:8s} {method:6s} hit@1 {s['hit@1']:.2f}  hit@3 {s['hit@3']:.2f}  "
                f"hit@5 {s['hit@5']:.2f}  words@5 {s['words_in_prompt@5']}")
    write_csv(C.EVAL_DIR / "retrieval_results.csv", per_q)
    write_csv(C.EVAL_DIR / "retrieval_summary.csv", summary)
    return summary


# ---------------------------------------------------------------------------
# 2-3. End to end + code checks
# ---------------------------------------------------------------------------
def run_agent(questions: list[dict]) -> dict:
    done = read_jsonl(ANSWERS)
    for i, q in enumerate(questions, 1):
        if q["id"] in done:
            continue
        log(f"  [{i}/{len(questions)}] {q['id']}: {q['question'][:70]}")
        try:
            r = answer(q["question"], interactive=False)
        except Exception as e:  # noqa: BLE001 - record and move on
            log(f"    error: {type(e).__name__}: {e}")
            continue
        row = {"id": q["id"], "design": f"{C.ACTIVE_CHUNKING}/{C.ACTIVE_METHOD}", "model": C.CHAT_MODEL, **r}
        append_jsonl(ANSWERS, row)
        done[q["id"]] = row
        time.sleep(PAUSE)
    return done


def code_checks(q: dict, a: dict) -> dict:
    refused = is_refusal(a["answer"])
    cited = CITE.findall(a["answer"])
    problem = check_citations(a["answer"], a["trace"])
    got = retrieved_citations(a["trace"])
    pairs = expected_pairs(q)
    retrieved_expected = any((d, p) in got if p else any(g[0] == d for g in got) for d, p in pairs) if pairs else None
    return {"refused": int(refused), "n_citations": len(cited),
            "citations_valid": int(problem is None), "retrieved_expected": retrieved_expected}


# ---------------------------------------------------------------------------
# 4. Judge
# ---------------------------------------------------------------------------
def evidence(a: dict) -> str:
    return "\n\n".join(f"(query: {t['input']})\n{t['output']}" for t in a["trace"] if t["tool"] == "search") or "(no search)"


def judge(questions: list[dict], answers: dict) -> dict:
    rubric = RUBRIC.read_text(encoding="utf-8") if RUBRIC.exists() else ""
    if not rubric.strip() or "TODO" in rubric:
        log("  eval/judge_rubric.md is not written yet: judge skipped. Write your rubric and run again.")
        return {}
    from google.genai import types
    from pydantic import BaseModel

    from index import gemini

    class Verdict(BaseModel):
        correct: int
        supported: int
        explanation: str

    done = read_jsonl(JUDGE)
    for q in questions:
        a = answers.get(q["id"])
        if not a or q["id"] in done or is_refusal(a["answer"]):
            continue
        prompt = (f"{rubric}\n\n# Question ({q['kind']})\n{q['question']}\n\n"
                  f"# Reference answer\n{q['reference_answer']}\n\n# Assistant answer\n{a['answer']}\n\n"
                  f"# Retrieved passages (the only evidence the assistant had)\n{evidence(a)}\n\n"
                  "Return JSON: correct (1/0), supported (1/0), explanation (one or two sentences).")
        for attempt in range(5):
            try:
                resp = gemini().models.generate_content(
                    model=C.JUDGE_MODEL, contents=prompt,
                    config=types.GenerateContentConfig(temperature=0, response_mime_type="application/json",
                                                       response_schema=Verdict))
                v = resp.parsed or Verdict.model_validate_json(resp.text)
                u = resp.usage_metadata
                row = {"id": q["id"], "correct": int(v.correct), "supported": int(v.supported),
                       "explanation": v.explanation,
                       "tokens": (u.prompt_token_count or 0) + (u.candidates_token_count or 0) if u else 0}
                append_jsonl(JUDGE, row)
                done[q["id"]] = row
                break
            except Exception as e:  # noqa: BLE001
                if "429" in str(e) or "RESOURCE_EXHAUSTED" in str(e):
                    time.sleep(20 * (attempt + 1))
                    continue
                log(f"    judge error on {q['id']}: {e}")
                break
        time.sleep(PAUSE / 2)
    return done


# ---------------------------------------------------------------------------
# 5-6. Combine, agreement, summary
# ---------------------------------------------------------------------------
def outcome(q: dict, chk: dict, v: dict | None) -> tuple[str, int | None, int | None]:
    """(outcome, correct, supported). Refusals are graded in code, the rest by the judge."""
    unans = q["kind"] == "unanswerable"
    if chk["refused"]:
        return ("correct refusal", 1, 1) if unans else ("wrong refusal", 0, 1)
    if not chk["citations_valid"]:                 # checked in code: no or invented citations
        return ("answered unanswerable" if unans else "unsupported", v["correct"] if v else 0, 0)
    if v is None:
        return ("not judged", None, None)
    if unans:
        return ("answered unanswerable", 0, v["supported"])
    if not v["supported"] or not chk["citations_valid"]:
        return ("unsupported", v["correct"], 0)
    return ("correct", 1, 1) if v["correct"] else ("incorrect", 0, 1)


def kappa(a: list[int], b: list[int]) -> float | None:
    n = len(a)
    if not n:
        return None
    po = sum(x == y for x, y in zip(a, b)) / n
    pa, pb = sum(a) / n, sum(b) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return round((po - pe) / (1 - pe), 3) if pe < 1 else None


def agreement(results: list[dict]) -> dict:
    human = {h["id"]: h for h in read_csv(HUMAN)}
    out = {"graded_by_you": len(human)}
    for field in ("correct", "supported"):
        pairs = [(int(human[r["id"]][field]), int(r[field])) for r in results
                 if r["id"] in human and human[r["id"]].get(field) in ("0", "1") and r[field] is not None]
        if pairs:
            out[f"{field}_n"] = len(pairs)
            out[f"{field}_agreement"] = round(sum(h == j for h, j in pairs) / len(pairs), 3)
            out[f"{field}_kappa"] = kappa([h for h, _ in pairs], [j for _, j in pairs])
    out["disagreements"] = [r["id"] for r in results if r["id"] in human and any(
        human[r["id"]].get(f) in ("0", "1") and r[f] is not None and int(human[r["id"]][f]) != r[f]
        for f in ("correct", "supported"))]
    return out


def auto_hint(q: dict, chk: dict, oc: str) -> str:
    """A first guess at the cause. Check every one yourself and fill in `cause`."""
    if oc == "answered unanswerable":
        return "unsupported claim (or bad test question: is it really unanswerable?)"
    if chk["retrieved_expected"] is False:
        return "retrieval miss"
    if oc == "wrong refusal":
        return "wrong refusal (right passage was retrieved)"
    if oc == "unsupported":
        return "unsupported claim"
    if oc == "incorrect":
        return "wrong answer from the right passage (or bad test question)"
    return ""


def main() -> int:
    questions = read_csv(Q_FILE)
    if not questions:
        raise SystemExit("eval/questions.csv is empty. Write your test set first (see eval/README.md).")
    log(f"{len(questions)} questions. Active design: {C.ACTIVE_CHUNKING}/{C.ACTIVE_METHOD}, model {C.CHAT_MODEL}\n")

    log("1. Retrieval")
    retrieval_eval(questions)

    log("\n2. Agent answers")
    answers = run_agent(questions)

    # A sheet for your own grades, without the judge's verdicts (grade these first).
    write_csv(C.EVAL_DIR / "to_grade.csv", [
        {"id": q["id"], "kind": q["kind"], "question": q["question"], "reference_answer": q["reference_answer"],
         "answer": answers[q["id"]]["answer"], "retrieved": evidence(answers[q["id"]])}
        for q in questions if q["id"] in answers])

    log("\n3-4. Code checks and judge")
    verdicts = judge(questions, answers)

    results, failures = [], []
    for q in questions:
        a = answers.get(q["id"])
        if not a:
            continue
        chk = code_checks(q, a)
        oc, correct, supported = outcome(q, chk, verdicts.get(q["id"]))
        v = verdicts.get(q["id"], {})
        row = {"id": q["id"], "kind": q["kind"], "outcome": oc, "correct": correct, "supported": supported,
               **chk, "guardrail": a.get("guardrail") or "", "tool_calls": a["tool_calls"],
               "tokens": a["input_tokens"] + a["output_tokens"], "seconds": a["seconds"],
               "judge_explanation": v.get("explanation", ""), "question": q["question"],
               "answer": a["answer"].replace("\n", " ")}
        results.append(row)
        if oc not in ("correct", "correct refusal", "not judged"):
            failures.append({"id": q["id"], "kind": q["kind"], "outcome": oc,
                             "auto_hint": auto_hint(q, chk, oc), "cause": "", "notes": "",
                             "question": q["question"], "answer": row["answer"],
                             "reference_answer": q["reference_answer"]})
    write_csv(C.EVAL_DIR / "results.csv", results)
    # Keep your own classification if you already filled in failures.csv
    old = {r["id"]: r for r in read_csv(C.EVAL_DIR / "failures.csv")}
    for f in failures:
        if f["id"] in old:
            f["cause"], f["notes"] = old[f["id"]].get("cause", ""), old[f["id"]].get("notes", "")
    write_csv(C.EVAL_DIR / "failures.csv", failures,
              ["id", "kind", "outcome", "auto_hint", "cause", "notes", "question", "answer", "reference_answer"])

    counts = {}
    for r in results:
        counts[r["outcome"]] = counts.get(r["outcome"], 0) + 1
    n = len(results) or 1
    agree = agreement(results)
    cost = {"mean_tokens": round(sum(r["tokens"] for r in results) / n),
            "mean_seconds": round(sum(r["seconds"] for r in results) / n, 1),
            "mean_tool_calls": round(sum(r["tool_calls"] for r in results) / n, 2),
            "judge_tokens_mean": round(sum(v.get("tokens", 0) for v in verdicts.values()) / max(len(verdicts), 1))}
    summary = {"questions": len(questions), "answered": len(results), "outcomes": counts,
               "guardrail_fired": [r["id"] for r in results if r["guardrail"]],
               "invalid_citations": [r["id"] for r in results if not r["citations_valid"]],
               "agreement_with_you": agree, "cost_per_question": cost,
               "design": f"{C.ACTIVE_CHUNKING}/{C.ACTIVE_METHOD}", "model": C.CHAT_MODEL}
    (C.EVAL_DIR / "summary.json").write_text(json.dumps(summary, indent=2))

    md = ["# Evaluation summary", "", f"Design {summary['design']}, model {C.CHAT_MODEL}, "
          f"{len(results)}/{len(questions)} questions answered.", "", "| Outcome | Count |", "|---|---|"]
    md += [f"| {k} | {v} |" for k, v in sorted(counts.items())]
    md += ["", f"Agreement with your grades: {json.dumps({k: v for k, v in agree.items() if k != 'disagreements'})}",
           f"Disagreements: {', '.join(agree['disagreements']) or 'none'}", "",
           f"Cost per question: {cost['mean_tokens']} tokens, {cost['mean_seconds']} s, "
           f"{cost['mean_tool_calls']} tool calls (judge: {cost['judge_tokens_mean']} tokens).",
           f"Guardrail fired on: {', '.join(summary['guardrail_fired']) or 'none'}"]
    (C.EVAL_DIR / "summary.md").write_text("\n".join(md) + "\n")
    log("\n" + "\n".join(md))
    return 0


if __name__ == "__main__":
    sys.exit(main())
