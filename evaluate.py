"""
Assignment 3: evaluation (`uv run python main.py evaluate`).

Stages (run all with no argument; or `python evaluate.py --stage <name>`):
  retrieval  hit rate at k = 1, 3, 5 for every design x method          -> eval/retrieval_results.csv
  answers    run the agent on every question (resumable)                -> eval/answers.jsonl
             and write eval/for_labeling.md (NO judge verdicts in it: grade from this first)
  judge      code checks + LLM judge, then agreement with human labels  -> eval/results.csv, eval/judge_verdicts.csv
  report     summary, failure table, cost                               -> eval/summary.json, eval/failures.csv
  addoc      before/after for an unanswerable question                  -> eval/before_after.md
             python evaluate.py --stage addoc --question q31 --doc path/to/new.pdf

Judge and report refuse to run until eval/human_labels.csv has >= 20 graded answers (the brief
asks you to grade before reading the judge). `--no-label-gate` overrides that.
"""

from __future__ import annotations

import argparse
import asyncio
import csv
import json
import os
import re
import sys
import time
from dataclasses import asdict
from pathlib import Path

import pandas as pd

import rag
from agent import CorpusAgent, Result, deny_all, ask_many, check_citations, is_refusal
from api_key import load_api_key
from rag import CITATION_RE, covers

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
HUMAN = EVAL / "human_labels.csv"
ANSWERS = EVAL / "answers.jsonl"
MIN_HUMAN = 20
JUDGE_MODEL = os.environ.get("JUDGE_MODEL", os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite"))
METHODS = ("dense", "bm25", "hybrid")

# >>> EDIT: this rubric is YOUR decision. Rewrite it in your own words and defend it in REPORT.md. <<<
RUBRIC = """You grade an answer from a document-search assistant. You see the question, a reference
answer written by the test author, the passages the assistant retrieved (the only evidence it
had), and the assistant's answer.

correct (0 or 1)
  1 if the answer states the same substance as the reference answer. Extra correct detail is fine.
  0 if a key fact, number, condition or exception from the reference is missing or contradicted,
  or if it answers a different question than the one asked.
supported (0 or 1)
  1 only if EVERY factual claim in the answer is stated in the retrieved passages.
  0 if any claim (a number, date, rule, name or condition) is not in them, even if it is true in
  the real world. Judge only against the passages, not against your own knowledge.

Be strict. When unsure, give 0. Explain in one or two sentences, naming the claim that failed."""


# ------------------------------------------------------------------ helpers
def load_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if (r.get("question") or "").strip()]
    for r in rows:
        r["kind"] = r["kind"].strip().lower()
    return rows


def load_answers() -> dict[str, dict]:
    out: dict[str, dict] = {}
    if ANSWERS.exists():
        for line in ANSWERS.read_text(encoding="utf-8").splitlines():
            if line.strip():
                row = json.loads(line)
                out[row["id"]] = row
    return out


def human_label_count() -> int:
    if not HUMAN.exists():
        return 0
    with HUMAN.open(newline="", encoding="utf-8") as f:
        return sum(1 for r in csv.DictReader(f) if (r.get("id") or "").strip())


def label_gate(args) -> bool:
    n = human_label_count()
    if n >= MIN_HUMAN or args.no_label_gate:
        return True
    print(
        f"\neval/human_labels.csv has {n} graded answers; at least {MIN_HUMAN} are needed before the judge runs.\n"
        "Open eval/for_labeling.md, grade 20+ answers into eval/human_labels.csv\n"
        "(id,correct,supported,notes), then run this again.",
    )
    return False


# ---------------------------------------------------------------- retrieval
def stage_retrieval(rows: list[dict]) -> pd.DataFrame:
    answerable = [r for r in rows if r["kind"] != "unanswerable"]
    records = []
    for design in rag.DESIGNS:
        if rag.get_collection(design).count() == 0:
            print(f"design '{design}' is empty: run `main.py index` first", file=sys.stderr)
            continue
        for method in METHODS:
            hits_at = {1: [], 3: [], 5: []}
            by_kind = {"single": {1: [], 3: [], 5: []}, "multi": {1: [], 3: [], 5: []}}
            words = []
            for r in answerable:
                top = rag.search(r["question"], design, method, 5)
                words.append(sum(len(h["text"].split()) for h in top))
                for k in (1, 3, 5):
                    ok = covers(r["expected_source"], r["expected_location"], top[:k])
                    hits_at[k].append(ok)
                    by_kind[r["kind"]][k].append(ok)
            rate = lambda xs: round(sum(xs) / len(xs), 3) if xs else float("nan")
            records.append(
                {
                    "design": design,
                    "method": method,
                    "hit@1": rate(hits_at[1]),
                    "hit@3": rate(hits_at[3]),
                    "hit@5": rate(hits_at[5]),
                    "single_hit@5": rate(by_kind["single"][5]),
                    "multi_hit@5": rate(by_kind["multi"][5]),
                    "words_in_prompt@5": round(sum(words) / len(words)) if words else 0,
                    "n_questions": len(answerable),
                }
            )
    df = pd.DataFrame(records)
    EVAL.mkdir(exist_ok=True)
    df.to_csv(EVAL / "retrieval_results.csv", index=False)
    print("\nRETRIEVAL (answerable questions only)\n")
    print(df.to_string(index=False))
    if len(df):
        best = df.sort_values(["hit@3", "hit@5", "words_in_prompt@5"], ascending=[False, False, True]).iloc[0]
        print(
            f"\nBest by hit@3 (then hit@5, then fewer words): design={best['design']}, method={best['method']}.\n"
            f"Current CHOSEN in rag.py: {rag.CHOSEN}. Decide yourself, then update CHOSEN."
        )
    return df


# ------------------------------------------------------------------ answers
def stage_answers(rows: list[dict], fresh: bool) -> dict[str, dict]:
    EVAL.mkdir(exist_ok=True)
    done = {} if fresh else {k: v for k, v in load_answers().items() if not v.get("error")}
    if fresh and ANSWERS.exists():
        ANSWERS.unlink()
    todo = [r for r in rows if r["id"] not in done]
    if done and not fresh:  # rewrite without failed rows
        ANSWERS.write_text("".join(json.dumps(v, ensure_ascii=False) + "\n" for v in done.values()), encoding="utf-8")
    print(f"\nANSWERS: {len(done)} already saved, {len(todo)} to run (agent model: see agent.MODEL)")
    by_question = {r["question"]: r for r in todo}

    def save(res: Result) -> None:
        row = by_question[res.question]
        record = {"id": row["id"], "kind": row["kind"], **asdict(res)}
        with ANSWERS.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False) + "\n")
        flag = "ERROR " + res.error[:80] if res.error else f"{res.seconds}s, {len(res.tool_calls)} tool calls"
        print(f"  {row['id']}: {flag}", flush=True)

    if todo:
        ask_many([r["question"] for r in todo], approve=deny_all, on_result=save)
    answers = load_answers()
    failed = [i for i, a in answers.items() if a.get("error")]
    if failed:
        print(f"{len(failed)} question(s) failed (rate limit?): {failed}. Run again to retry only those.")
    write_labeling_sheet(rows, answers)
    return answers


def write_labeling_sheet(rows: list[dict], answers: dict[str, dict]) -> None:
    lines = [
        "# Answers to grade by hand",
        "",
        "Grade 20+ of these into `eval/human_labels.csv` (`id,correct,supported,notes`) BEFORE you read the judge.",
        "`correct` = right against the reference (or a proper refusal); `supported` = every claim is in the retrieved text.",
        "",
    ]
    for r in rows:
        a = answers.get(r["id"])
        if not a:
            continue
        lines += [f"## {r['id']} ({r['kind']})", f"**Question:** {r['question']}", "", f"**Reference:** {r['reference_answer']}", ""]
        lines += [f"**Agent answer:** {a['answer'] or '(none)'}", "", "**Retrieved:**"]
        for p in a["retrieved"][:8]:
            lines.append(f"- [{p['source']} | {p['location']}] {p['text'][:350]}...")
        lines.append("")
    (EVAL / "for_labeling.md").write_text("\n".join(lines), encoding="utf-8")
    print("Wrote eval/for_labeling.md (no judge verdicts in it).")


# -------------------------------------------------------------------- judge
def code_checks(row: dict, a: dict) -> dict:
    answer = a["answer"]
    refused = is_refusal(answer)
    problems = check_citations(answer, a["retrieved"]) if answer else ["no answer"]
    cited_sources = {s.strip() for s, _ in CITATION_RE.findall(answer)}
    expected = [s.strip() for s in row["expected_source"].split(";") if s.strip()]
    return {
        "refused": refused,
        "valid_citations": not problems,
        "citation_problems": "; ".join(problems),
        "cites_expected_source": bool(expected) and all(e in cited_sources for e in expected),
        "retrieved_expected": covers(row["expected_source"], row["expected_location"], a["retrieved"]) if expected else None,
        "tool_calls": len(a["tool_calls"]),
        "guardrail_fired": a["guardrail_fired"],
    }


def judge_one(client, row: dict, a: dict):
    from google.genai import types
    from pydantic import BaseModel

    class Verdict(BaseModel):
        correct: int
        supported: int
        reason: str

    evidence = "\n\n".join(f"[{p['source']} | {p['location']}]\n{p['text']}" for p in a["retrieved"]) or "(nothing retrieved)"
    prompt = (
        f"{RUBRIC}\n\nQUESTION:\n{row['question']}\n\nREFERENCE ANSWER:\n{row['reference_answer']}\n\n"
        f"RETRIEVED PASSAGES (the only evidence):\n{evidence[:14000]}\n\nASSISTANT ANSWER:\n{a['answer']}"
    )
    delay = 5.0
    for attempt in range(5):
        try:
            res = client.models.generate_content(
                model=JUDGE_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(temperature=0, response_mime_type="application/json", response_schema=Verdict),
            )
            v = res.parsed
            return int(v.correct), int(v.supported), v.reason
        except Exception as error:  # noqa: BLE001
            if ("429" in str(error) or "RESOURCE_EXHAUSTED" in str(error)) and attempt < 4:
                time.sleep(delay)
                delay *= 2
                continue
            return -1, -1, f"judge error: {type(error).__name__}: {error}"
    return -1, -1, "judge error: retries exhausted"


def kappa(a: list[int], b: list[int]) -> float:
    n = len(a)
    if n == 0:
        return float("nan")
    po = sum(x == y for x, y in zip(a, b)) / n
    pe = sum((a.count(v) / n) * (b.count(v) / n) for v in (0, 1))
    return round((po - pe) / (1 - pe), 3) if pe != 1 else 1.0


def stage_judge(rows: list[dict]) -> pd.DataFrame:
    from google import genai

    answers = load_answers()
    client = genai.Client(api_key=load_api_key())
    out = []
    for r in rows:
        a = answers.get(r["id"])
        if not a or a.get("error"):
            continue
        c = code_checks(r, a)
        unanswerable = r["kind"] == "unanswerable"
        if c["refused"]:
            # code decides refusals: right for unanswerable, wrong for answerable
            correct, supported, reason = (1 if unanswerable else 0), 1, "refusal (decided in code)"
        else:
            correct, supported, reason = judge_one(client, r, a)
            if unanswerable and correct != -1:
                correct, reason = 0, f"answered an unanswerable question. Judge: {reason}"
        out.append({"id": r["id"], "kind": r["kind"], **c, "correct": correct, "supported": supported, "reason": reason})
        print(f"  {r['id']}: correct={correct} supported={supported}", flush=True)
    df = pd.DataFrame(out)
    df.to_csv(EVAL / "results.csv", index=False)
    df[["id", "correct", "supported", "reason"]].to_csv(EVAL / "judge_verdicts.csv", index=False)
    return df


def agreement(df: pd.DataFrame) -> dict:
    if not HUMAN.exists():
        return {}
    h = pd.read_csv(HUMAN, dtype=str, keep_default_na=False)
    h = h[h["id"].str.strip() != ""]
    m = h.merge(df[["id", "correct", "supported"]], on="id", suffixes=("_human", "_judge"))
    m = m[(m["correct_judge"] >= 0) & (m["supported_judge"] >= 0)]
    if m.empty:
        return {}
    res = {"n_labeled": int(len(m))}
    for col in ("correct", "supported"):
        hu = m[f"{col}_human"].astype(int).tolist()
        ju = m[f"{col}_judge"].astype(int).tolist()
        res[f"{col}_agreement"] = round(sum(x == y for x, y in zip(hu, ju)) / len(hu), 3)
        res[f"{col}_kappa"] = kappa(hu, ju)
    disagree = m[(m["correct_human"].astype(int) != m["correct_judge"]) | (m["supported_human"].astype(int) != m["supported_judge"])]
    res["disagreements"] = disagree["id"].tolist()
    return res


# ------------------------------------------------------------------- report
def suggest_cause(r: pd.Series) -> str:
    if r["kind"] == "unanswerable":
        return "unsupported claim"  # it answered when it should have refused
    if r["refused"]:
        return "wrong refusal"
    if r["retrieved_expected"] is False:
        return "retrieval miss"
    if r["supported"] == 0:
        return "unsupported claim"
    return "wrong answer from right passage"


def stage_report(rows: list[dict], df: pd.DataFrame) -> None:
    answers = load_answers()
    ans = df[df["kind"] != "unanswerable"]
    una = df[df["kind"] == "unanswerable"]
    judged = df[(df["correct"] >= 0)]
    non_refused = judged[~judged["refused"]]
    cost = [(a["input_tokens"], a["output_tokens"], a["seconds"]) for a in answers.values() if not a.get("error")]
    n = max(len(cost), 1)
    summary = {
        "questions_answered": len(df),
        "answerable": {
            "n": len(ans),
            "correct": int(((ans["correct"] == 1) & (~ans["refused"])).sum()),
            "wrong_refusals": int(ans["refused"].sum()),
            "incorrect_answers": int(((ans["correct"] == 0) & (~ans["refused"])).sum()),
            "unsupported_among_answers": int(((ans["supported"] == 0) & (~ans["refused"])).sum()),
        },
        "unanswerable": {
            "n": len(una),
            "correct_refusals": int(una["refused"].sum()),
            "answered_instead_of_refusing": int((~una["refused"]).sum()),
        },
        "all_answers_unsupported": int((non_refused["supported"] == 0).sum()),
        "code_checks": {
            "valid_citations_rate": round(float(df["valid_citations"].mean()), 3),
            "cites_expected_source_rate_answerable": round(float(ans["cites_expected_source"].mean()), 3) if len(ans) else None,
            "guardrail_fired": int(df["guardrail_fired"].sum()),
        },
        "cost_per_question": {
            "mean_input_tokens": round(sum(c[0] for c in cost) / n),
            "mean_output_tokens": round(sum(c[1] for c in cost) / n),
            "mean_seconds": round(sum(c[2] for c in cost) / n, 1),
            "mean_tool_calls": round(float(df["tool_calls"].mean()), 2),
        },
        "judge_model": JUDGE_MODEL,
        "agreement_with_human_labels": agreement(df),
        "retrieval_config": rag.CHOSEN,
    }
    (EVAL / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    bad = df[(df["correct"] == 0) | (df["supported"] == 0)].copy()
    if len(bad):
        bad["suggested_cause"] = bad.apply(suggest_cause, axis=1)
        bad["cause_final"] = ""  # YOU fill this: retrieval miss | wrong answer from right passage |
        bad["notes"] = ""  # unsupported claim | wrong refusal | bad test question
        bad[["id", "kind", "suggested_cause", "cause_final", "notes", "reason", "retrieved_expected", "refused"]].to_csv(
            EVAL / "failures.csv", index=False
        )
    print("\nSUMMARY\n" + json.dumps(summary, indent=2))
    print("\nWrote eval/summary.json and eval/failures.csv. Review failures.csv by hand: "
          "'suggested_cause' is only a first guess, and 'bad test question' is yours to spot.")


# -------------------------------------------------------------------- addoc
def stage_addoc(rows: list[dict], question_id: str, doc: str) -> None:
    row = next((r for r in rows if r["id"] == question_id), None)
    if row is None or row["kind"] != "unanswerable":
        sys.exit(f"--question must be the id of an `unanswerable` question; got {question_id!r}")

    async def run():
        async with CorpusAgent(deny_all) as agent:
            before = await agent.ask(row["question"])
            first = await agent.session.call_tool("add_document", {"path": doc})
            again = await agent.session.call_tool("add_document", {"path": doc})  # duplicate policy
            after = await agent.ask(row["question"])
            text = lambda r: "\n".join(getattr(c, "text", "") for c in r.content)
            return before, text(first), text(again), after

    before, first, again, after = asyncio.run(run())
    md = [
        f"# Before / after adding `{doc}`", "", f"**Question ({row['id']}):** {row['question']}", "",
        f"**Reference:** {row['reference_answer']}", "", "## Before", before.answer or before.error, "",
        "## add_document, first call", "```", first, "```", "",
        "## add_document, same file again (duplicate policy)", "```", again, "```", "",
        "## After", after.answer or after.error, "",
        "Passages retrieved after:", *[f"- [{p['source']} | {p['location']}]" for p in after.retrieved],
    ]
    (EVAL / "before_after.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


# --------------------------------------------------------------------- main
def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--stage", default="all", choices=["all", "retrieval", "answers", "judge", "report", "addoc"])
    parser.add_argument("--fresh", action="store_true", help="discard saved answers and re-run every question")
    parser.add_argument("--no-label-gate", action="store_true")
    parser.add_argument("--question")
    parser.add_argument("--doc")
    args = parser.parse_args()

    rows = load_questions()
    if args.stage in ("all", "retrieval"):
        stage_retrieval(rows)
    if args.stage in ("all", "answers"):
        stage_answers(rows, args.fresh)
    if args.stage == "addoc":
        if not (args.question and args.doc):
            sys.exit("addoc needs --question <unanswerable id> and --doc <path>")
        stage_addoc(rows, args.question, args.doc)
        return
    if args.stage in ("all", "judge", "report"):
        if not label_gate(args):
            return
        df = stage_judge(rows) if args.stage in ("all", "judge") else pd.read_csv(EVAL / "results.csv", keep_default_na=False)
        if args.stage == "report":
            for col in ("refused", "valid_citations", "cites_expected_source", "guardrail_fired"):
                df[col] = df[col].astype(str).str.lower() == "true"
            df["retrieved_expected"] = df["retrieved_expected"].astype(str).map({"True": True, "False": False})
        if args.stage in ("all", "report"):
            stage_report(rows, df)
        else:
            print("Judge done: eval/results.csv. Now run --stage report.")


if __name__ == "__main__":
    main()
