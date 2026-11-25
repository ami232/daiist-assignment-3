"""
Assignment 3: evaluation (`main.py evaluate`).

1. Retrieval: hit rate at k = 1, 3, 5 for every design in retrieval.DESIGNS.
   A hit means the expected page AND section is in the top k (for `multi`
   questions, every expected passage must be there).
2. End to end: runs the agent on every question (add_document never approved).
3. Code checks: refusals, citation validity, whether the expected page was
   retrieved and cited.
4. LLM judge (Gemini) with a rubric, using the passages the agent retrieved as
   evidence: correct (0/1) and supported (0/1).
5. Agreement between the judge and eval/human_labels.csv.
6. Failure classification and cost per question (tokens, seconds).

Agent answers and judge verdicts are cached in eval/*.jsonl, so a rerun (or a
crash halfway, or the rate limit) never pays for a question twice. Delete those
files to start over. Results: eval/summary.md and the CSV files next to it.
"""

from __future__ import annotations

import csv
import json
import os
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
HUMAN = EVAL / "human_labels.csv"
ANSWERS = EVAL / "answers.jsonl"
JUDGE = EVAL / "judge.jsonl"
KS = (1, 3, 5)
SLEEP = float(os.environ.get("EVAL_SLEEP", "4"))  # seconds between agent runs (free-tier rate limit)

sys.path.insert(0, str(ROOT))


def log(*a):
    print(*a, flush=True)


def read_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r["question"].strip()]
    for r in rows:
        r["kind"] = r["kind"].strip().lower()
        r["expected"] = list(zip(r["expected_source"].split(";"), r["expected_location"].split(";"))) \
            if r["expected_source"].strip() else []
    return rows


def passage_matches(hit: dict, source: str, location: str) -> bool:
    """Right page, and the chunk covers the expected section (merged chunks list several)."""
    return hit["source"] == source.strip() and location.strip() in [s.strip() for s in hit["section"].split(" / ")]


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def load_jsonl(path: Path) -> dict:
    if not path.exists():
        return {}
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            out[r["id"]] = r
    return out


def append_jsonl(path: Path, record: dict) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


# --------------------------------------------------------------------------- 1. retrieval

def evaluate_retrieval(questions: list[dict]) -> tuple[list[dict], str]:
    from retrieval import DESIGNS, SERVED_DESIGN, search

    answerable = [q for q in questions if q["expected"]]
    per_question, summary = [], []
    for design in DESIGNS:
        hits_at = {k: 0 for k in KS}
        for q in answerable:
            results = search(q["question"], k=max(KS), design=design)
            ranks = []
            for source, location in q["expected"]:
                rank = next((h["rank"] for h in results if passage_matches(h, source, location)), None)
                ranks.append(rank)
            worst = None if None in ranks else max(ranks)  # multi: every passage must be found
            for k in KS:
                hits_at[k] += worst is not None and worst <= k
            per_question.append({"design": design, "id": q["id"], "kind": q["kind"],
                                 "expected": q["expected_source"], "rank": worst or "",
                                 "top5": " | ".join(f"{h['source']} § {h['section']}" for h in results)})
        row = {"design": design, **{f"hit@{k}": round(hits_at[k] / len(answerable), 3) for k in KS},
               "questions": len(answerable)}
        summary.append(row)
        log(f"   {design:16s} " + "  ".join(f"hit@{k} {row[f'hit@{k}']:.2f}" for k in KS))
    write_csv(EVAL / "retrieval_per_question.csv", per_question)
    write_csv(EVAL / "retrieval_summary.csv", summary)
    best = max(summary, key=lambda r: (r["hit@3"], r["hit@5"], r["hit@1"]))["design"]
    if best != SERVED_DESIGN:
        log(f"   NOTE: {best} scores best but the server uses {SERVED_DESIGN}; change SERVED_DESIGN in retrieval.py.")
    _plot(summary)
    return summary, best


def _plot(summary: list[dict]) -> None:
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt
    except ImportError:
        return
    fig, ax = plt.subplots(figsize=(6, 3.2))
    width = 0.8 / len(summary)
    for i, row in enumerate(summary):
        xs = [j + i * width for j in range(len(KS))]
        ax.bar(xs, [row[f"hit@{k}"] for k in KS], width, label=row["design"])
    ax.set_xticks([j + width * (len(summary) - 1) / 2 for j in range(len(KS))], [f"k={k}" for k in KS])
    ax.set_ylim(0, 1)
    ax.set_ylabel("hit rate")
    ax.set_title("Retrieval hit rate by design")
    ax.legend(fontsize=8, loc="lower right")
    fig.tight_layout()
    fig.savefig(EVAL / "hit_rate.png", dpi=150)
    plt.close(fig)


# --------------------------------------------------------------------------- 2. agent

def run_agent(questions: list[dict]) -> dict:
    from agent import ask

    done = load_jsonl(ANSWERS)
    todo = [q for q in questions if q["id"] not in done or done[q["id"]].get("error")]
    log(f"   {len(done) - sum(1 for d in done.values() if d.get('error'))} cached, {len(todo)} to run")
    for i, q in enumerate(todo, 1):
        try:
            r = ask(q["question"], approve=lambda path: False)  # never add documents during evaluation
            record = {"id": q["id"], **r}
        except Exception as e:  # keep going; the failure is recorded and retried next run
            record = {"id": q["id"], "question": q["question"], "error": f"{type(e).__name__}: {e}"}
        append_jsonl(ANSWERS, record)
        done[q["id"]] = record
        status = record.get("error") or f"{len(record['trace'])} tools, {record['seconds']}s"
        log(f"   [{i}/{len(todo)}] {q['id']}: {status}")
        time.sleep(SLEEP)
    return done


# --------------------------------------------------------------------------- 3. code checks

def evidence(record: dict) -> str:
    return "\n\n".join(s["result"] for s in record.get("trace", []) if s["tool"] == "search")


def code_checks(q: dict, r: dict) -> dict:
    from agent import _match, _norm, is_refusal, parse_citations, retrieved_citations

    if r.get("error"):
        return {"refused": "", "citations": 0, "invalid_citations": "", "expected_retrieved": "",
                "expected_cited": "", "refusal_ok": ""}
    raw = r.get("raw_answer", r["answer"])
    allowed = retrieved_citations(r["trace"])
    cited = parse_citations(raw)
    invalid = [c for c in cited if not _match(_norm(c), allowed)]
    ev = evidence(r)
    exp_sources = [s for s, _ in q["expected"]]
    refused = is_refusal(r["answer"])
    return {
        "refused": int(refused),
        "citations": len(cited),
        "invalid_citations": len(invalid),
        "expected_retrieved": int(all(f"cite as: [{s} §" in ev for s in exp_sources)) if exp_sources else "",
        "expected_cited": int(all(any(c.startswith(f"{s} §") for c in cited) for s in exp_sources)) if exp_sources else "",
        # right call on whether to answer: refuse exactly when the corpus cannot answer
        "refusal_ok": int(refused == (q["kind"] == "unanswerable")),
    }


# --------------------------------------------------------------------------- 4. judge

RUBRIC = """You grade answers from a question-answering assistant for players of the video game THE FINALS.
The assistant may only use the EVIDENCE passages (what its search tool returned).

Return JSON: {"correct": 0 or 1, "supported": 0 or 1, "reason": "<one sentence>"}

correct = 1 when:
- the question is answerable and the answer states the key facts of the REFERENCE ANSWER (same numbers,
  same items) without contradicting it. Extra correct detail is fine. Missing a key fact, a wrong number
  or a wrong item gives 0. A refusal gives 0.
- the question is marked unanswerable and the answer says the wiki does not cover it, without inventing
  an answer. Any made-up answer gives 0.

supported = 1 when every factual claim in the answer can be found in the EVIDENCE passages.
A refusal that invents nothing is supported. One claim that is not in the evidence gives 0, even if it is
true in the real game.
"""


def judge(questions: list[dict], answers: dict) -> dict:
    from google import genai
    from google.genai import types

    from agent import MODEL
    from api_key import load_api_key

    client = genai.Client(api_key=load_api_key(), http_options=types.HttpOptions(timeout=60_000))
    done = load_jsonl(JUDGE)
    for q in questions:
        r = answers.get(q["id"])
        if not r or r.get("error") or q["id"] in done:
            continue
        prompt = (f"{RUBRIC}\nQUESTION ({q['kind']}): {q['question']}\n\nREFERENCE ANSWER: {q['reference_answer']}"
                  f"\n\nANSWER TO GRADE:\n{r['answer']}\n\nEVIDENCE:\n{evidence(r) or '(the assistant retrieved nothing)'}")
        for attempt in range(5):
            try:
                resp = client.models.generate_content(
                    model=MODEL, contents=prompt,
                    config=types.GenerateContentConfig(response_mime_type="application/json"))
                verdict = json.loads(resp.text)
                usage = resp.usage_metadata
                record = {"id": q["id"], "correct": int(verdict["correct"]), "supported": int(verdict["supported"]),
                          "reason": verdict.get("reason", ""),
                          "tokens": getattr(usage, "total_token_count", 0) or 0}
                break
            except Exception as e:  # rate limit or a malformed reply: wait and retry
                record = {"id": q["id"], "error": f"{type(e).__name__}: {e}"}
                time.sleep(15 * (attempt + 1))
        if "error" not in record:
            append_jsonl(JUDGE, record)
            done[q["id"]] = record
        log(f"   judged {q['id']}: {record.get('correct', '?')}/{record.get('supported', '?')}")
        time.sleep(SLEEP / 2)
    return done


# --------------------------------------------------------------------------- 5. agreement

def cohen_kappa(a: list[int], b: list[int]) -> float | None:
    n = len(a)
    if n == 0:
        return None
    po = sum(x == y for x, y in zip(a, b)) / n
    pa, pb = sum(a) / n, sum(b) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return None if pe == 1 else round((po - pe) / (1 - pe), 3)


def agreement(verdicts: dict) -> dict:
    if not HUMAN.exists():
        return {}
    with HUMAN.open(newline="", encoding="utf-8") as f:
        labels = [r for r in csv.DictReader(f) if (r.get("id") or "").strip() and r["id"] in verdicts]
    out = {"n": len(labels)}
    for field in ("correct", "supported"):
        pairs = [(int(r[field]), verdicts[r["id"]][field]) for r in labels if (r.get(field) or "").strip()]
        h, j = [p[0] for p in pairs], [p[1] for p in pairs]
        out[field] = {"n": len(pairs), "agreement": round(sum(x == y for x, y in pairs) / len(pairs), 3) if pairs else None,
                      "kappa": cohen_kappa(h, j),
                      "disagreements": [r["id"] for r in labels if (r.get(field) or "").strip()
                                        and int(r[field]) != verdicts[r["id"]][field]]}
    return out


# --------------------------------------------------------------------------- 6. failures

def classify(q: dict, checks: dict, verdict: dict) -> str:
    """First guess at the failure type; review it by hand (a 'bad test question' needs a human)."""
    if not verdict:
        return ""
    if q["kind"] == "unanswerable":
        return "" if checks["refused"] and verdict["correct"] else "unsupported claim"
    if checks["refused"]:
        return "retrieval miss" if not checks["expected_retrieved"] else "wrong refusal"
    if not verdict["correct"]:
        return "retrieval miss" if not checks["expected_retrieved"] else "wrong answer from right passage"
    if not verdict["supported"]:
        return "unsupported claim"
    return ""


# --------------------------------------------------------------------------- main

def main() -> None:
    questions = read_questions()
    log(f"Evaluating {len(questions)} questions from {QUESTIONS.relative_to(ROOT)}")

    log("1/5 Retrieval hit rate")
    retrieval, best = evaluate_retrieval(questions)

    log("2/5 Running the agent on every question")
    answers = run_agent(questions)

    log("3/5 LLM judge")
    verdicts = judge(questions, answers)

    log("4/5 Code checks, failures and cost")
    rows = []
    for q in questions:
        r, v = answers.get(q["id"], {}), verdicts.get(q["id"], {})
        checks = code_checks(q, r) if r else {}
        rows.append({
            "id": q["id"], "kind": q["kind"], "question": q["question"],
            "answer": r.get("answer", ""), "error": r.get("error", ""),
            **checks,
            "judge_correct": v.get("correct", ""), "judge_supported": v.get("supported", ""),
            "judge_reason": v.get("reason", ""),
            "failure": classify(q, checks, v) if checks else "",
            "guardrail": r.get("guardrail") or "",
            "tool_calls": len(r.get("trace", [])), "tokens": r.get("tokens", {}).get("total", ""),
            "judge_tokens": v.get("tokens", ""), "seconds": r.get("seconds", ""),
        })
    write_csv(EVAL / "results.csv", rows)
    write_csv(EVAL / "failures.csv", [{"id": r["id"], "kind": r["kind"], "question": r["question"],
                                        "answer": r["answer"], "auto_class": r["failure"],
                                        "judge_reason": r["judge_reason"], "manual_class": ""}
                                       for r in rows if r["failure"]])
    _grading_sheet(questions, answers)

    log("5/5 Agreement with human labels")
    agree = agreement(verdicts)
    if agree.get("n", 0) < 20:
        log(f"   eval/human_labels.csv grades {agree.get('n', 0)} answers; the brief asks for 20+ (see eval/to_grade.md)")

    _summary(questions, rows, retrieval, best, agree)
    log(f"Done. See {(EVAL / 'summary.md').relative_to(ROOT)}")


def _grading_sheet(questions: list[dict], answers: dict) -> None:
    """Everything a human needs to fill in eval/human_labels.csv, one question per block."""
    parts = ["# Answers to grade\n\nFor each, write a row in `eval/human_labels.csv`: `id,correct,supported,notes` "
             "(1 or 0). Grade before looking at the judge's verdict in results.csv.\n"
             "- **correct**: matches the reference answer (for unanswerable: refuses without inventing).\n"
             "- **supported**: every claim is in the retrieved passages below.\n"]
    for q in questions:
        r = answers.get(q["id"], {})
        if not r or r.get("error"):
            continue
        parts.append(f"\n---\n\n## {q['id']} ({q['kind']})\n\n**Question:** {q['question']}\n\n"
                     f"**Reference:** {q['reference_answer']}\n\n**Agent answer:**\n\n{r['answer']}\n\n"
                     f"<details><summary>Retrieved passages</summary>\n\n```\n{evidence(r)[:6000]}\n```\n</details>\n")
    (EVAL / "to_grade.md").write_text("".join(parts), encoding="utf-8")


def _summary(questions, rows, retrieval, best, agree) -> None:
    ok = [r for r in rows if r["judge_correct"] != ""]
    by_kind = {}
    for kind in ("single", "multi", "unanswerable"):
        k_rows = [r for r in ok if r["kind"] == kind]
        if k_rows:
            by_kind[kind] = (sum(r["judge_correct"] for r in k_rows), len(k_rows))
    answered = [r for r in ok if r["kind"] != "unanswerable"]
    unans = [r for r in ok if r["kind"] == "unanswerable"]
    halluc = sum(1 for r in ok if not r["refused"] and not r["judge_supported"])
    tokens = [r["tokens"] for r in rows if r["tokens"] != ""]
    secs = [r["seconds"] for r in rows if r["seconds"] != ""]
    failures = {}
    for r in rows:
        if r["failure"]:
            failures[r["failure"]] = failures.get(r["failure"], 0) + 1

    lines = ["# Evaluation summary\n", f"{len(questions)} questions; model `{os.environ.get('GEMINI_MODEL', 'gemini-3.5-flash-lite')}`.\n",
             "## Retrieval (hit rate)\n", "| design | hit@1 | hit@3 | hit@5 |", "|---|---|---|---|"]
    lines += [f"| {r['design']} | {r['hit@1']:.2f} | {r['hit@3']:.2f} | {r['hit@5']:.2f} |" for r in retrieval]
    lines += [f"\nBest by hit@3: **{best}**.\n", "## End to end (LLM judge)\n", "| kind | correct |", "|---|---|"]
    lines += [f"| {k} | {c}/{n} ({c / n:.0%}) |" for k, (c, n) in by_kind.items()]
    if ok:
        lines += ["",
                  f"- Correct overall: {sum(r['judge_correct'] for r in ok)}/{len(ok)}",
                  f"- Supported by retrieved text: {sum(r['judge_supported'] for r in ok)}/{len(ok)}",
                  f"- Answered with an unsupported claim (made something up): {halluc}/{len(ok)}",
                  f"- Rightly refused (unanswerable): {sum(r['refused'] for r in unans)}/{len(unans)}",
                  f"- Wrongly refused (answerable): {sum(r['refused'] for r in answered)}/{len(answered)}",
                  f"- Answers with an invalid citation (before the guardrail): {sum(1 for r in ok if r['invalid_citations'])}",
                  f"- Answers changed by the guardrail: {sum(1 for r in ok if r['guardrail'])}"]
    if failures:
        lines += ["\n## Failures (automatic first pass; review in failures.csv)\n"] + [f"- {k}: {v}" for k, v in failures.items()]
    if tokens and secs:
        lines += ["\n## Cost per question\n",
                  f"- Tokens: mean {statistics.mean(tokens):,.0f}, median {statistics.median(tokens):,.0f}, max {max(tokens):,}",
                  f"- Seconds: mean {statistics.mean(secs):.1f}, median {statistics.median(secs):.1f}, max {max(secs):.1f}",
                  f"- Tool calls: mean {statistics.mean([r['tool_calls'] for r in rows]):.1f}"]
    if agree.get("n"):
        lines += [f"\n## Judge vs human ({agree['n']} answers)\n"]
        for field in ("correct", "supported"):
            a = agree[field]
            lines.append(f"- {field}: agreement {a['agreement']}, Cohen's kappa {a['kappa']}, disagreements {a['disagreements']}")
    (EVAL / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
