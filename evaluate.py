"""
Assignment 3: evaluation (`main.py evaluate`).

1. Retrieval: hit rate at k = 1, 3, 5 for three designs (dense, bm25, hybrid) on the
   answerable questions. A "hit" means every expected (document, regulation) is in the top k.
2. Agent: runs agent.py on every question (resumes if interrupted) and saves answers.
3. Code checks: valid citations, refusals, expected regulation cited.
4. LLM judge with a rubric and the retrieved text as evidence.
5. Agreement with your own grades in eval/human_labels.csv (if you have written them).
6. Failure classes, cost per question, and eval/summary.md.

Everything is saved in eval/. Re-running is cheap: finished answers and verdicts are reused.
"""

import csv
import json
import re
import sys
import time
from pathlib import Path

import agent
import retrieval

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
ANSWERS = EVAL / "agent_answers.csv"
JUDGE = EVAL / "judge_verdicts.csv"
HUMAN = EVAL / "human_labels.csv"
DESIGNS = ["dense", "bm25", "hybrid"]
ANSWER_FIELDS = ["id", "kind", "answer", "tool_calls", "retrieved", "guard", "model", "input_tokens", "output_tokens", "seconds", "evidence"]
JUDGE_FIELDS = ["id", "correct", "supported", "reason"]
REG = re.compile(r"regulation (\d+[A-Za-z]*)")

RUBRIC = """You are grading an answer from a retrieval assistant about three UK regulations.
You get the QUESTION, the REFERENCE answer (written from the regulations), the ASSISTANT ANSWER and the EVIDENCE
(the passages the assistant retrieved).

Give two grades, each 1 or 0:
- correct: 1 if the assistant answer matches the reference in substance (minor wording differences are fine; extra
  true detail is fine). For a question the corpus cannot answer, the reference says what the assistant should do:
  correct = 1 only if the assistant clearly says the corpus does not cover it (or that it does not know) and does NOT
  present an answer as fact. Missing a key element of the reference, or contradicting it, is 0.
- supported: 1 if every factual claim in the assistant answer appears in the EVIDENCE. A refusal with no claims
  is 1. Any claim not found in the evidence (even if true in real life) makes it 0.

Reply with JSON only: {"correct": 0 or 1, "supported": 0 or 1, "reason": "one short sentence"}"""


# ----------------------------------------------------------------------------- helpers
def read_csv(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def expected_pairs(q: dict) -> set[tuple[str, str]]:
    sources = [s.strip() for s in q["expected_source"].split(";") if s.strip()]
    locs = [REG.search(l).group(1) for l in q["expected_location"].split(";") if REG.search(l)]
    return set(zip(sources, locs))


def hit_pairs(hits: list[dict]) -> set[tuple[str, str]]:
    return {(h["source"], m.group(1)) for h in hits if (m := REG.search(h["location"]))}


def pct(n: int, d: int) -> str:
    return f"{100 * n / d:.0f}%" if d else "n/a"


# ----------------------------------------------------------------------------- 1. retrieval
def evaluate_retrieval(questions: list[dict]) -> tuple[list[str], list[dict]]:
    answerable = [q for q in questions if q["kind"].strip().lower() != "unanswerable"]
    per_q, lines = [], ["| design | hit@1 | hit@3 | hit@5 | words in prompt (k=5) |", "|---|---|---|---|---|"]
    summary = {}
    for design in DESIGNS:
        hits_at = {1: 0, 3: 0, 5: 0}
        words = 0
        for q in answerable:
            top = retrieval.retrieve(q["question"], k=5, mode=design)
            words += sum(len(h["text"].split()) for h in top)
            need = expected_pairs(q)
            row = {"id": q["id"], "design": design}
            for k in (1, 3, 5):
                ok = need <= hit_pairs(top[:k])
                hits_at[k] += ok
                row[f"hit@{k}"] = int(ok)
            per_q.append(row)
        n = len(answerable)
        summary[design] = hits_at
        lines.append(f"| {design} | {pct(hits_at[1], n)} | {pct(hits_at[3], n)} | {pct(hits_at[5], n)} | {words // n} |")
    best = max(DESIGNS, key=lambda d: (summary[d][5], summary[d][3], summary[d][1]))
    lines.append(f"\nBest by hit@5 (ties broken by hit@3, hit@1): **{best}** (retrieval.DEFAULT_MODE is "
                 f"`{retrieval.DEFAULT_MODE}`; change it if they differ).")
    write_csv(EVAL / "retrieval_by_question.csv", per_q, ["id", "design", "hit@1", "hit@3", "hit@5"])
    return lines, per_q


# ----------------------------------------------------------------------------- 2. agent runs
def run_agent_on_all(questions: list[dict]) -> list[dict]:
    done = {r["id"]: r for r in read_csv(ANSWERS)}
    rerun: set[str] = set()
    for i, q in enumerate(questions, 1):
        old = done.get(q["id"])
        if old and not old["guard"].startswith("call limit or error"):
            continue
        rerun.add(q["id"])
        print(f"[{i}/{len(questions)}] {q['id']}: {q['question'][:70]}", file=sys.stderr)
        r = agent.ask(q["question"])
        done[q["id"]] = {
            "id": q["id"], "kind": q["kind"], "answer": r["answer"],
            "tool_calls": json.dumps(r["tool_calls"]), "retrieved": ";".join(sorted(set(r["retrieved"]))),
            "guard": r["guard"], "model": r.get("model", ""), "input_tokens": r["input_tokens"],
            "output_tokens": r["output_tokens"], "seconds": r["seconds"], "evidence": r.get("evidence", "")[:8000],
        }
        write_csv(ANSWERS, [done[x["id"]] for x in questions if x["id"] in done], ANSWER_FIELDS)
    return [done[q["id"]] for q in questions], rerun


# ----------------------------------------------------------------------------- 3. code checks
def code_checks(q: dict, a: dict) -> dict:
    refused = agent.REFUSAL.lower() in a["answer"].lower()
    retrieved = set(a["retrieved"].split(";")) if a["retrieved"] else set()
    cited = [(s, r) for s, r in agent.CITATION.findall(a["answer"])]
    valid = all(f"{s}|{r}" in retrieved for s, r in cited)
    need = expected_pairs(q)
    cited_pairs = {(s, REG.search(r).group(1)) for s, r in cited if REG.search(r)}
    return {
        "refused": refused,
        "valid_citations": valid and (bool(cited) or refused),
        "cited_expected": need <= cited_pairs if need else None,
    }


# ----------------------------------------------------------------------------- 4. LLM judge
def judge_one(q: dict, a: dict) -> dict:
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=agent.load_api_key())
    prompt = (f"{RUBRIC}\n\nQUESTION: {q['question']}\nREFERENCE: {q['reference_answer']}\n"
              f"ASSISTANT ANSWER: {a['answer']}\nEVIDENCE:\n{a['evidence'] or '(nothing retrieved)'}")
    last = None
    for model in agent.pick_models()[:4]:
        for attempt in range(2):
            try:
                resp = client.models.generate_content(
                    model=model, contents=prompt,
                    config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0))
                data = json.loads(resp.text)
                return {"id": q["id"], "correct": int(data["correct"]), "supported": int(data["supported"]),
                        "reason": str(data.get("reason", ""))[:300]}
            except Exception as error:  # noqa: BLE001
                last = error
                time.sleep(5)
    raise SystemExit(f"Judge failed: {last}")


def run_judge(questions: list[dict], answers: list[dict], rerun: set[str] = frozenset()) -> dict[str, dict]:
    done = {r["id"]: r for r in read_csv(JUDGE) if r["id"] not in rerun}  # re-run answers get a fresh verdict
    for q, a in zip(questions, answers):
        if q["id"] in done:
            continue
        print(f"judging {q['id']}", file=sys.stderr)
        done[q["id"]] = judge_one(q, a)
        write_csv(JUDGE, list(done.values()), JUDGE_FIELDS)
    return done


# ----------------------------------------------------------------------------- 5/6. report
def classify(q: dict, a: dict, chk: dict, verdict: dict, retr: dict) -> str:
    if a["guard"].startswith("call limit or error"):
        return "infrastructure error (Google API quota/overload), not a system failure: re-run"
    unanswerable = q["kind"].strip().lower() == "unanswerable"
    if unanswerable:
        return "" if int(verdict["correct"]) and int(verdict["supported"]) else "unsupported claim (answered an unanswerable question)"
    if int(verdict["correct"]) and int(verdict["supported"]):
        return ""
    if chk["refused"]:
        return "wrong refusal" if retr.get("hit@5") == 1 else "retrieval miss"
    if retr.get("hit@5") == 0:
        return "retrieval miss"
    if not int(verdict["supported"]):
        return "unsupported claim"
    return "wrong answer from the right passage"


def main() -> None:
    EVAL.mkdir(exist_ok=True)
    questions = read_csv(QUESTIONS)
    if not questions:
        raise SystemExit("eval/questions.csv is empty.")
    md = ["# Evaluation summary", "", "## Retrieval (answerable questions)", ""]

    lines, per_q = evaluate_retrieval(questions)
    md += lines
    print("\n".join(lines))
    retr_default = {r["id"]: r for r in per_q if r["design"] == retrieval.DEFAULT_MODE}

    answers, rerun = run_agent_on_all(questions)
    verdicts = run_judge(questions, answers, rerun)

    rows, failures = [], []
    for q, a in zip(questions, answers):
        chk = code_checks(q, a)
        v = verdicts[q["id"]]
        cause = classify(q, a, chk, v, retr_default.get(q["id"], {}))
        rows.append((q, a, chk, v, cause))
        if cause:
            failures.append({"id": q["id"], "kind": q["kind"], "cause": cause, "judge_reason": v["reason"], "question": q["question"]})
    write_csv(EVAL / "failures.csv", failures, ["id", "kind", "cause", "judge_reason", "question"])

    ans = [r for r in rows if r[0]["kind"].strip().lower() != "unanswerable"]
    una = [r for r in rows if r[0]["kind"].strip().lower() == "unanswerable"]
    n = len(rows)
    stats = {
        "correct": sum(int(r[3]["correct"]) for r in rows),
        "supported": sum(int(r[3]["supported"]) for r in rows),
        "valid_citations": sum(r[2]["valid_citations"] for r in rows),
        "correct_refusals": sum(r[2]["refused"] and int(r[3]["correct"]) for r in una),
        "wrong_refusals": sum(r[2]["refused"] for r in ans),
        "answered_unanswerable": sum(not r[2]["refused"] for r in una),
        "cited_expected": sum(bool(r[2]["cited_expected"]) for r in ans),
        "guard_fired": sum(bool(r[1]["guard"]) for r in rows),
    }
    in_tok = sum(int(r[1]["input_tokens"]) for r in rows)
    out_tok = sum(int(r[1]["output_tokens"]) for r in rows)
    secs = sum(float(r[1]["seconds"]) for r in rows)
    md += ["", "## End to end (judge + code checks)", "",
           f"- Questions: {n} ({len(ans)} answerable, {len(una)} unanswerable)",
           f"- Judged correct: {stats['correct']}/{n} ({pct(stats['correct'], n)})",
           f"- Judged supported (no unsupported claims): {stats['supported']}/{n} ({pct(stats['supported'], n)})",
           f"- Valid citations (code check): {stats['valid_citations']}/{n}",
           f"- Answerable questions citing the expected regulation(s) (code check): {stats['cited_expected']}/{len(ans)}",
           f"- Correct refusals on unanswerable: {stats['correct_refusals']}/{len(una)}",
           f"- Wrong refusals on answerable: {stats['wrong_refusals']}/{len(ans)}",
           f"- Unanswerable questions that were answered anyway: {stats['answered_unanswerable']}/{len(una)}",
           f"- Guardrail fired: {stats['guard_fired']} times",
           f"- Cost per question: {in_tok // n} input + {out_tok // n} output tokens, {secs / n:.1f}s on average",
           "", "## Failures by cause", ""]
    causes: dict[str, int] = {}
    for f in failures:
        causes[f["cause"]] = causes.get(f["cause"], 0) + 1
    md += [f"- {c}: {k}" for c, k in sorted(causes.items(), key=lambda x: -x[1])] or ["- none"]
    md.append("\nSee eval/failures.csv. The causes are automatic guesses: check each one by hand "
              "(a failure can also be a bad test question).")

    # agreement with your own grades
    human = {r["id"]: r for r in read_csv(HUMAN) if (r.get("id") or "").strip()}
    both = [i for i in human if i in verdicts]
    md += ["", "## Agreement between you and the judge", ""]
    if len(both) < 20:
        md.append(f"Only {len(both)} graded answers in eval/human_labels.csv (need 20+). Grade them BEFORE opening "
                  f"eval/judge_verdicts.csv, then run evaluate again.")
    if both:
        for col in ("correct", "supported"):
            agree = sum(int(human[i][col]) == int(verdicts[i][col]) for i in both)
            md.append(f"- `{col}`: agree on {agree}/{len(both)} ({pct(agree, len(both))})")
        disagreements = [i for i in both if int(human[i]["correct"]) != int(verdicts[i]["correct"])]
        md.append(f"- Disagreements on `correct`: {', '.join(disagreements) or 'none'}")

    (EVAL / "summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    print("\n" + "\n".join(md[md.index("## End to end (judge + code checks)"):]))
    print("\nSaved: eval/summary.md, agent_answers.csv, judge_verdicts.csv, failures.csv, retrieval_by_question.csv")


if __name__ == "__main__":
    main()
