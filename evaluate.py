"""
Assignment 3: evaluation (`main.py evaluate`).

1. Retrieval: hit rate at k = 1, 3, 5 for each design, and words added to the prompt.
2. End to end: the agent answers every question (corpus as built, added documents
   excluded), with tokens and seconds per question.
3. Code checks: citations present and valid, refusal on unanswerable, no refusal
   on answerable, whether the agent's own searches found the expected passage.
4. LLM judge with the rubric in eval/rubric.md and the retrieved text as evidence.
5. Agreement between the judge and eval/human_labels.csv.
6. Before/after: add the held-out document and re-ask one unanswerable question.
7. Failure list with a suggested cause, for you to confirm.

Answers and verdicts are cached in eval/*.jsonl so a re-run spends no quota on
questions already done. Set EVAL_FRESH=1 to redo them.
"""

from __future__ import annotations

import asyncio
import csv
import json
import os
import re
import sys
import time
from pathlib import Path

import index as ix
import retrieval
from agent import MODEL, REFUSAL, Harness, is_refusal

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
DESIGNS = ["fixed", "structure", "structure_hybrid"]
KS = (1, 3, 5)
SLEEP = float(os.environ.get("EVAL_SLEEP", "4"))      # free tier: stay under requests-per-minute
FRESH = os.environ.get("EVAL_FRESH") == "1"
JUDGE_MODEL = os.environ.get("JUDGE_MODEL", "gemini-3.5-flash")
# If the judge model is overloaded (503) or out of quota, try these in order.
JUDGE_FALLBACKS = ["gemini-3.8-flash", "gemini-3.1-flash-lite"]

# Before/after: the unanswerable question that the held-out document answers.
BEFORE_AFTER_ID = os.environ.get("BEFORE_AFTER_ID", "q29")  # simplified procedure question


def log(msg: str) -> None:
    print(msg, flush=True)


def load_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r["question"].strip()]


def expected_pairs(q: dict) -> list[tuple[str, str]]:
    """(source, location) pairs a question needs. One source with several
    locations is repeated; otherwise sources and locations pair up in order."""
    srcs = [s.strip() for s in q["expected_source"].split(";") if s.strip()]
    locs = [l.strip() for l in q["expected_location"].split(";") if l.strip()]
    if not srcs:
        return []
    if len(srcs) == 1:
        return [(srcs[0], l) for l in locs] or [(srcs[0], "")]
    if len(locs) == 1:
        return [(s, locs[0]) for s in srcs]
    return list(zip(srcs, locs))


def covers(results: list[dict], pair: tuple[str, str]) -> bool:
    src, loc = pair
    if not loc:
        return any(r["source"] == src for r in results)
    return retrieval.citation_valid(src, loc, results) or any(
        r["source"] == src and set(retrieval.norm_unit(loc)) & retrieval.chunk_units(r) for r in results)


# ---------------------------------------------------------------------------
# 1. Retrieval
# ---------------------------------------------------------------------------
def eval_retrieval(questions: list[dict]) -> list[dict]:
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    rows = []
    for design in DESIGNS:
        hits = {k: 0 for k in KS}
        any_hits = {k: 0 for k in KS}
        words = []
        per_q = []
        for q in answerable:
            res = retrieval.search(q["question"], design=design, k=max(KS), exclude_added=True)
            pairs = expected_pairs(q)
            words.append(sum(len(r["text"].split()) for r in res))
            first = None
            for k in KS:
                found = [covers(res[:k], p) for p in pairs]
                hits[k] += all(found)
                any_hits[k] += any(found)
            for rank in range(1, len(res) + 1):
                if all(covers(res[:rank], p) for p in pairs):
                    first = rank
                    break
            per_q.append({"design": design, "id": q["id"], "kind": q["kind"], "first_full_hit_rank": first or "",
                          "top5": " ; ".join(f"{r['source']} {r['location']}" for r in res)})
        n = len(answerable)
        row = {"design": design, "questions": n,
               **{f"hit@{k}": round(hits[k] / n, 3) for k in KS},
               **{f"any@{k}": round(any_hits[k] / n, 3) for k in KS},
               "words_in_prompt@5": round(sum(words) / n), "chunks": len(retrieval.store(design.removesuffix('_hybrid')).chunks)}
        rows.append(row)
        log(f"  {design:<17} " + "  ".join(f"hit@{k}={row[f'hit@{k}']:.2f}" for k in KS)
            + f"  words@5={row['words_in_prompt@5']}")
        write_csv(EVAL / f"retrieval_{design}.csv", per_q)
    write_csv(EVAL / "retrieval.csv", rows)
    plot_retrieval(rows)
    return rows


def plot_retrieval(rows: list[dict]) -> None:
    import matplotlib
    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(6, 3.5))
    w = 0.25
    for i, r in enumerate(rows):
        ax.bar([x + i * w for x in range(len(KS))], [r[f"hit@{k}"] for k in KS], w, label=r["design"])
    ax.set_xticks([x + w for x in range(len(KS))], [f"k={k}" for k in KS])
    ax.set_ylim(0, 1)
    ax.set_ylabel("hit rate (all expected passages)")
    ax.legend(frameon=False, fontsize=8)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(EVAL / "retrieval.png", dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------------------
# 2. Agent answers (cached)
# ---------------------------------------------------------------------------
def read_jsonl(path: Path) -> dict:
    if FRESH or not path.exists():
        return {}
    out = {}
    for line in path.read_text().splitlines():
        if line.strip():
            rec = json.loads(line)
            out[rec["id"]] = rec
    return out


def append_jsonl(path: Path, rec: dict) -> None:
    with path.open("a") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


async def run_agent(questions: list[dict]) -> dict:
    path = EVAL / "answers.jsonl"
    if FRESH and path.exists():
        path.unlink()
    done = read_jsonl(path)
    todo = [q for q in questions if q["id"] not in done or done[q["id"]]["question"] != q["question"]]
    if todo:
        async with Harness(exclude_added=True) as h:
            for i, q in enumerate(todo, 1):
                for attempt in range(3):
                    try:
                        res = await h.run(q["question"])
                        break
                    except Exception as e:  # quota or transient error: wait and retry
                        log(f"  {q['id']}: {type(e).__name__}: {str(e)[:200]}")
                        if "PerDay" in str(e) or "per day" in str(e).lower():
                            raise SystemExit("Daily Gemini quota reached; answers so far are saved. Re-run tomorrow.")
                        time.sleep(30 * (attempt + 1))
                else:
                    continue
                rec = {"id": q["id"], **res}
                append_jsonl(path, rec)
                done[q["id"]] = rec
                log(f"  [{i}/{len(todo)}] {q['id']} {res['seconds']:.1f}s "
                    f"{'REFUSED' if is_refusal(res['answer']) else 'answered'}")
                time.sleep(SLEEP)
    return done


# ---------------------------------------------------------------------------
# 3. Code checks
# ---------------------------------------------------------------------------
def code_checks(q: dict, a: dict) -> dict:
    ans = a["answer"]
    refused = is_refusal(ans)
    cites = retrieval.citations(ans)
    valid = [retrieval.citation_valid(s, l, a["retrieved"]) for s, l in cites]
    pairs = expected_pairs(q)
    unans = q["kind"] == "unanswerable"
    return {
        "refused": int(refused),
        "n_citations": len(cites),
        "citations_valid": int(all(valid)) if cites else int(refused),
        "correct_refusal": int(unans and refused) if unans else "",
        "wrong_refusal": int((not unans) and refused) if not unans else "",
        "agent_retrieval_hit": int(all(covers(a["retrieved"], p) for p in pairs)) if pairs else "",
        "guardrail_fired": int(any("guardrail" in e for e in a["events"])),
    }


# ---------------------------------------------------------------------------
# 4. LLM judge
# ---------------------------------------------------------------------------
JUDGE_PROMPT = """{rubric}

QUESTION:
{question}

REFERENCE ANSWER (written by the course student from the documents):
{reference}

QUESTION TYPE: {kind}

RETRIEVED PASSAGES (the only evidence the assistant had):
{evidence}

ASSISTANT ANSWER:
{answer}

Reply with JSON only: {{"correct": 0 or 1, "supported": 0 or 1, "reason": "one sentence"}}"""


def judge(questions: list[dict], answers: dict) -> dict:
    from google import genai
    from api_key import load_api_key

    rubric = (EVAL / "rubric.md").read_text(encoding="utf-8")
    path = EVAL / "judge.jsonl"
    if FRESH and path.exists():
        path.unlink()
    done = read_jsonl(path)
    client = genai.Client(api_key=load_api_key())
    for q in questions:
        a = answers.get(q["id"])
        if not a or (q["id"] in done and done[q["id"]].get("answer") == a["answer"]):
            continue
        evidence = "\n\n".join(f"[{r['source']}, {r['location']}]\n{r['text']}" for r in a["retrieved"]) or "(none)"
        prompt = JUDGE_PROMPT.format(rubric=rubric, question=q["question"], reference=q["reference_answer"],
                                     kind=q["kind"], evidence=evidence[:30000], answer=a["answer"])
        verdict, used = None, None
        for attempt, model in enumerate([JUDGE_MODEL, JUDGE_MODEL] + JUDGE_FALLBACKS):
            try:
                resp = client.models.generate_content(
                    model=model, contents=prompt,
                    config={"temperature": 0, "response_mime_type": "application/json"})
                verdict = json.loads(re.search(r"\{.*\}", resp.text, re.S).group(0))
                used = model
                break
            except Exception as e:
                log(f"  judge {q['id']} ({model}): {type(e).__name__}: {str(e)[:120]}")
                time.sleep(10)
        if verdict is None:
            continue
        rec = {"id": q["id"], "answer": a["answer"], "correct": int(verdict["correct"]),
               "supported": int(verdict["supported"]), "reason": verdict.get("reason", ""), "judge_model": used}
        append_jsonl(path, rec)
        done[q["id"]] = rec
        time.sleep(SLEEP)
    return done


# ---------------------------------------------------------------------------
# 5. Agreement with human labels
# ---------------------------------------------------------------------------
def agreement(verdicts: dict) -> dict:
    path = EVAL / "human_labels.csv"
    with path.open(newline="", encoding="utf-8") as f:
        human = [r for r in csv.DictReader(f) if r.get("id", "").strip() and r.get("correct", "").strip()]
    out = {"n_human_labels": len(human)}
    for col in ("correct", "supported"):
        pairs = [(int(h[col]), verdicts[h["id"]][col]) for h in human
                 if h["id"] in verdicts and h.get(col, "").strip() in ("0", "1")]
        if not pairs:
            continue
        agree = sum(a == b for a, b in pairs) / len(pairs)
        # Cohen's kappa: agreement beyond what chance would give
        p_h = sum(a for a, _ in pairs) / len(pairs)
        p_j = sum(b for _, b in pairs) / len(pairs)
        pe = p_h * p_j + (1 - p_h) * (1 - p_j)
        kappa = (agree - pe) / (1 - pe) if pe < 1 else 1.0
        out[col] = {"n": len(pairs), "agreement": round(agree, 3), "kappa": round(kappa, 3),
                    "disagreements": [h["id"] for h in human if h["id"] in verdicts and h.get(col, "").strip() in ("0", "1")
                                      and int(h[col]) != verdicts[h["id"]][col]]}
    return out


# ---------------------------------------------------------------------------
# 6. Before / after adding a document
# ---------------------------------------------------------------------------
async def before_after(questions: list[dict]) -> dict | None:
    q = next((q for q in questions if q["id"] == BEFORE_AFTER_ID), None)
    if q is None:
        log("  skipped: set BEFORE_AFTER_ID in evaluate.py to the unanswerable question the new document answers")
        return None
    path = EVAL / "before_after.json"
    if path.exists() and not FRESH:
        saved = json.loads(path.read_text())
        if saved.get("question") == q["question"]:
            return saved
    doc = ix.download(ix.HELD_OUT)
    add = ix.add_document(doc)
    retrieval.store.cache_clear()
    async with Harness(exclude_added=True) as h:
        before = await h.run(q["question"])
    time.sleep(SLEEP)
    async with Harness(exclude_added=False) as h:
        after = await h.run(q["question"])
    rec = {"id": q["id"], "question": q["question"], "document": ix.HELD_OUT["title"], "add_result": add,
           "before": before["answer"], "after": after["answer"],
           "after_citations": retrieval.citations(after["answer"])}
    path.write_text(json.dumps(rec, indent=2, ensure_ascii=False))
    return rec


# ---------------------------------------------------------------------------
# 7. Failures
# ---------------------------------------------------------------------------
def suggest_cause(q: dict, chk: dict, v: dict | None) -> str:
    if q["kind"] == "unanswerable":
        return "" if chk["refused"] else "answered an unanswerable question (unsupported claim)"
    if chk["refused"]:
        return "retrieval miss" if not chk["agent_retrieval_hit"] else "wrong refusal"
    if v is None:
        return "not judged"
    if v["correct"] and v["supported"]:
        return ""
    if not chk["agent_retrieval_hit"]:
        return "retrieval miss"
    if not v["supported"]:
        return "unsupported claim"
    return "wrong answer from the right passage"


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    keys = list(dict.fromkeys(k for r in rows for k in r))
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    questions = load_questions()
    log(f"{len(questions)} questions\n\n1/6 Retrieval hit rate per design")
    retrieval_rows = eval_retrieval(questions)

    log("\n2/6 Agent answers (added documents excluded)")
    answers = asyncio.run(run_agent(questions))

    log("\n3/6 LLM judge")
    verdicts = judge(questions, answers)

    log("\n4/6 Code checks and results")
    rows = []
    for q in questions:
        a = answers.get(q["id"])
        if not a:
            continue
        chk = code_checks(q, a)
        v = verdicts.get(q["id"])
        rows.append({"id": q["id"], "kind": q["kind"], "question": q["question"],
                     "reference_answer": q["reference_answer"], "answer": a["answer"],
                     "cited": " ; ".join(f"[{s}, {l}]" for s, l in retrieval.citations(a["answer"])),
                     "retrieved": " ; ".join(dict.fromkeys(f"{r['source']} {r['location']}" for r in a["retrieved"])),
                     **chk,
                     "judge_correct": v["correct"] if v else "", "judge_supported": v["supported"] if v else "",
                     "judge_reason": v["reason"] if v else "",
                     "suggested_cause": suggest_cause(q, chk, v),
                     "input_tokens": a["input_tokens"], "output_tokens": a["output_tokens"],
                     "seconds": a["seconds"], "tool_calls": len(a["tool_calls"]), "events": " | ".join(a["events"])})
    write_csv(EVAL / "results.csv", rows)
    # A blind sheet for your own grading: no judge columns.
    write_csv(EVAL / "to_grade.csv", [{k: r[k] for k in ("id", "kind", "question", "reference_answer", "answer", "retrieved")}
                                      for r in rows])
    write_csv(EVAL / "failures.csv", [{k: r[k] for k in ("id", "kind", "question", "answer", "suggested_cause",
                                                         "judge_reason")} | {"cause_confirmed": ""}
                                      for r in rows if r["suggested_cause"]])

    unans = [r for r in rows if r["kind"] == "unanswerable"]
    ans = [r for r in rows if r["kind"] != "unanswerable"]
    judged = [r for r in ans if r["judge_correct"] != ""]
    n = len(rows) or 1
    summary = {
        "model": MODEL, "judge_model": JUDGE_MODEL, "questions": len(rows),
        "retrieval": retrieval_rows,
        "answerable": len(ans),
        "correct_and_supported": sum(1 for r in judged if r["judge_correct"] and r["judge_supported"]),
        "correct": sum(1 for r in judged if r["judge_correct"]),
        "unsupported": sum(1 for r in judged if not r["judge_supported"] and not r["refused"]),
        "wrong_refusals": sum(r["wrong_refusal"] for r in ans),
        "unanswerable": len(unans),
        "correct_refusals": sum(r["correct_refusal"] for r in unans),
        "answered_unanswerable": sum(1 - r["correct_refusal"] for r in unans),
        "invalid_citation_answers": sum(1 for r in rows if not r["citations_valid"]),
        "guardrail_fired": sum(r["guardrail_fired"] for r in rows),
        "failures_by_cause": {},
        "avg_input_tokens": round(sum(r["input_tokens"] for r in rows) / n),
        "avg_output_tokens": round(sum(r["output_tokens"] for r in rows) / n),
        "avg_seconds": round(sum(r["seconds"] for r in rows) / n, 1),
        "max_seconds": max((r["seconds"] for r in rows), default=0),
    }
    for r in rows:
        if r["suggested_cause"]:
            summary["failures_by_cause"][r["suggested_cause"]] = summary["failures_by_cause"].get(r["suggested_cause"], 0) + 1

    log("\n5/6 Agreement with your labels")
    summary["agreement"] = agreement(verdicts)
    log(f"  {json.dumps(summary['agreement'])}")

    log("\n6/6 Before/after adding a document")
    summary["before_after"] = asyncio.run(before_after(questions))
    if summary["before_after"]:
        log(f"  BEFORE: {summary['before_after']['before'][:300]}\n  AFTER:  {summary['before_after']['after'][:300]}")

    (EVAL / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    log("\nSummary:")
    for k in ("correct_and_supported", "correct", "unsupported", "wrong_refusals", "correct_refusals",
              "answered_unanswerable", "invalid_citation_answers", "guardrail_fired", "failures_by_cause",
              "avg_input_tokens", "avg_output_tokens", "avg_seconds"):
        log(f"  {k}: {summary[k]}")
    log("\nWrote eval/results.csv, eval/to_grade.csv, eval/failures.csv, eval/retrieval*.csv, eval/retrieval.png, eval/summary.json")


if __name__ == "__main__":
    main()
