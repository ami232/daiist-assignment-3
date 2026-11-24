"""
Assignment 3: evaluation (`main.py evaluate` runs `python evaluate.py`).

Each stage saves what it produces in eval/ and reuses it on the next run, so a re-run
spends no quota unless something changed, and anyone can reproduce the reported numbers
from the committed files.

 1. retrieval: embed every question once (eval/question_vectors.json) and compute hit rate
    at k = 1, 3, 5 for both chunk designs, plus the words each adds to the prompt.
 2. answers: run the agent on every question (eval/answers.jsonl), check in code what code
    can check (refusals, citations, guardrail) and write eval/grading_sheet.md, the answers
    with their retrieved passages, for grading by hand (no judge verdicts in it).
 3. judge: an LLM grades each answer with the author's rubric (eval/judge_rubric.md), with
    the passages the agent retrieved as evidence (eval/verdicts.jsonl).
 4. agreement with eval/human_labels.csv, failure categories, cost and latency:
    eval/results.csv, eval/summary.md, eval/summary.json.

    python evaluate.py              # all stages
    python evaluate.py --retrieval  # stage 1 only
    python evaluate.py --answers    # stages 1-2: grade the sheet before the judge runs
    python evaluate.py --rerun      # ignore saved answers and verdicts (spends quota)
"""

import argparse
import asyncio
import csv
import hashlib
import json
import os
import re
import statistics
import sys
import time
from collections import Counter
from pathlib import Path

os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")

import agent
import index

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
HUMAN_LABELS = EVAL / "human_labels.csv"
RUBRIC = EVAL / "judge_rubric.md"
VECTORS = EVAL / "question_vectors.json"
ANSWERS = EVAL / "answers.jsonl"
VERDICTS = EVAL / "verdicts.jsonl"
GRADING_SHEET = EVAL / "grading_sheet.md"
RESULTS = EVAL / "results.csv"
SUMMARY_MD = EVAL / "summary.md"
SUMMARY_JSON = EVAL / "summary.json"

KS = (1, 3, 5)
DESIGNS = index.DESIGNS
PRECISE_MAX_CHUNKS = 2  # an expected location with at most this many chunks is "precise"
JUDGE_MODELS = ["gemini-3.5-flash", "gemini-3.8-flash", "gemini-3.5-flash-lite"]

RESULT_RE = re.compile(r"--- Result \d+ \| cite as \[([^,\]]+), ([^\]]+)\] \| similarity ([\d.]+)\n"
                       r"Document: [^\n]*\n(.*?)(?=\n\n--- Result \d+ \||\Z)", re.S)


def sha(*parts: str) -> str:
    return hashlib.sha1("\x1f".join(parts).encode()).hexdigest()[:16]


def read_jsonl(path: Path) -> dict:
    if not path.is_file():
        return {}
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return {r["id"]: r for r in rows}


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")


def load_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if (r.get("question") or "").strip()]
    for r in rows:
        r["kind"] = r["kind"].strip().lower()
        sources = [s.strip() for s in r["expected_source"].split(";") if s.strip()]
        locations = [s.strip() for s in r["expected_location"].split(";") if s.strip()]
        r["expected"] = list(zip(sources, locations))
    return rows


def pct(n: int, d: int) -> str:
    return f"{100 * n / d:.0f}% ({n}/{d})" if d else "n/a"


# ---------------------------------------------------------------- 1. retrieval

def question_vectors(questions: list[dict]) -> dict[str, list[float]]:
    """One embedding per question text, saved as soon as it arrives and reused afterwards."""
    saved = json.loads(VECTORS.read_text(encoding="utf-8")) if VECTORS.is_file() else {}
    todo = [q["question"] for q in questions if q["question"] not in saved]
    if todo:
        print(f"Embedding {len(todo)} questions (each counts against the daily quota) ...")
        for text, vector in zip(todo, index.embed_queries(todo)):
            saved[text] = [round(x, 6) for x in vector]
        VECTORS.write_text(json.dumps(saved), encoding="utf-8")
    return saved


def location_sizes() -> Counter:
    """How many structure chunks each (source, location) has: a 55-chunk Annex counts any hit."""
    metas = index.collection("structure").get(include=["metadatas"])["metadatas"]
    return Counter((m["source"], agent.base_location(m["location"])) for m in metas)


def evaluate_retrieval(questions: list[dict]) -> tuple[list[dict], dict]:
    vectors = question_vectors(questions)
    sizes = location_sizes()
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    rows = []
    for design in DESIGNS:
        col = index.collection(design)
        for q in answerable:
            res = col.query(query_embeddings=[vectors[q["question"]]], n_results=max(KS), include=["metadatas"])
            metas = res["metadatas"][0]
            row = {"id": q["id"], "kind": q["kind"], "design": design,
                   "expected": "; ".join(f"[{s}, {l}]" for s, l in q["expected"]),
                   "precise": max(sizes[e] for e in q["expected"]) <= PRECISE_MAX_CHUNKS,
                   "retrieved": "; ".join(f"[{m['source']}, {m['location']}]" for m in metas)}
            for k in KS:
                found = {(m["source"], c) for m in metas[:k] for c in m["covers"].split("|")}
                hits = [e in found for e in q["expected"]]
                row[f"any@{k}"], row[f"all@{k}"] = any(hits), all(hits)
                row[f"words@{k}"] = sum(m["words"] for m in metas[:k])
            rows.append(row)

    summary = {}
    for design in DESIGNS:
        mine = [r for r in rows if r["design"] == design]
        multi = [r for r in mine if r["kind"] == "multi"]
        s = {"questions": len(mine)}
        for k in KS:
            s[f"hit@{k}"] = sum(r[f"any@{k}"] for r in mine) / len(mine)
            s[f"multi_all@{k}"] = sum(r[f"all@{k}"] for r in multi) / len(multi) if multi else None
            s[f"words@{k}"] = statistics.mean(r[f"words@{k}"] for r in mine)
            for group, flag in (("precise", True), ("broad", False)):
                g = [r for r in mine if r["precise"] == flag]
                s[f"{group}_hit@{k}"] = sum(r[f"any@{k}"] for r in g) / len(g) if g else None
                s[f"{group}_n"] = len(g)
        summary[design] = s

    with (EVAL / "retrieval.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    return rows, summary


# ---------------------------------------------------------------- 2. answers

def passages(trace: list[dict]) -> dict[str, str]:
    """Every distinct passage the agent's searches returned: '[SOURCE, location]' -> text."""
    found = {}
    for step in trace:
        for source, location, _, body in RESULT_RE.findall(step.get("output") or ""):
            found.setdefault(f"[{source}, {location}]", body.strip())
    return found


async def run_agent(questions: list[dict], rerun: bool) -> dict:
    prompt_sha = sha(agent.SYSTEM_PROMPT)
    saved = {} if rerun else read_jsonl(ANSWERS)
    stale = [i for i, a in saved.items() if a.get("agents_md_sha") != prompt_sha]
    if stale:
        print(f"WARNING: {len(stale)} saved answers were produced with another AGENTS.md "
              f"({', '.join(stale[:5])}...). Run with --rerun to answer them again.")
    todo = [q for q in questions if q["id"] not in saved or saved[q["id"]]["question"] != q["question"]]
    if todo:
        print(f"Asking the agent {len(todo)} questions (one MCP server for all) ...")
        async with agent.CorpusAgent(approve=lambda name, args: False) as bot:
            for n, q in enumerate(todo, 1):
                r = await bot.ask(q["question"])
                status = "ERROR " + r["error"][:80] if r["error"] else (
                    "refusal" if r["refusal"] else "answer") + (" [guardrail]" if r["guardrail"] else "")
                print(f"  {n}/{len(todo)} {q['id']}: {status} ({r['seconds']} s)", flush=True)
                if r["error"]:
                    continue  # not saved, so the next run asks again
                saved[q["id"]] = {"id": q["id"], "agents_md_sha": prompt_sha, **r}
                write_jsonl(ANSWERS, [saved[k] for k in sorted(saved)])  # save as we go
    saved = {k: recheck(a) for k, a in saved.items()}
    write_jsonl(ANSWERS, [saved[k] for k in sorted(saved)])
    return saved


def recheck(a: dict) -> dict:
    """Apply the current guardrail and citation parsing to a saved answer, without asking the
    model again (the model's own answer is kept: in blocked_answer if it was blocked)."""
    raw = a["blocked_answer"] or a["answer"]
    shown, fired = agent.guardrail(a["question"], raw, a["trace"])
    retrieved = agent.retrieved_labels(a["trace"])
    a.update(answer=shown, blocked_answer=raw if fired else None, guardrail=fired,
             refusal=agent.is_refusal(shown),
             citations=[{"source": s, "location": loc, "retrieved": (s, loc) in retrieved}
                        for s, loc in dict.fromkeys(agent.citations_in(raw))])
    return a


def code_checks(q: dict, a: dict) -> dict:
    """Refusal: blocked, or says the corpus does not cover it and cites nothing.
    Partial: cites sources and also says which part the corpus does not cover (AGENTS.md rule 4)."""
    retrieved = agent.retrieved_labels(a["trace"])
    cited = {(c["source"], c["location"]) for c in a["citations"]}
    answerable = q["kind"] != "unanswerable"
    refusal = bool(a["guardrail"]) or (a["refusal"] and not cited)
    partial = a["refusal"] and bool(cited) and not a["guardrail"]
    if answerable:
        outcome = "wrong refusal" if refusal else "answered, partly covered" if partial else "answered"
    else:
        outcome = "correct refusal" if refusal else "partial answer" if partial else "answered unanswerable"
    return {
        "refusal": refusal,
        "partial": partial,
        "outcome": outcome,
        "citations_valid": all(c["retrieved"] for c in a["citations"]),
        "cites_expected": bool(cited & set(q["expected"])) if answerable else None,
        "retrieved_expected": bool(retrieved & set(q["expected"])) if answerable else None,
        "guardrail": a["guardrail"] or "",
    }


def write_grading_sheet(questions: list[dict], answers: dict) -> None:
    out = ["# Grading sheet", "",
           "Grade each answer in eval/human_labels.csv (id, correct, supported, notes) before reading",
           "the judge's verdicts. correct: right against the reference, or a proper refusal.",
           "supported: every claim is in the retrieved passages below.", ""]
    for q in questions:
        a = answers.get(q["id"])
        if not a:
            continue
        out += [f"## {q['id']} ({q['kind']})", "", f"**Question:** {q['question']}", "",
                f"**Reference:** {q['reference_answer']}", "",
                f"**Expected:** {'; '.join(f'[{s}, {l}]' for s, l in q['expected']) or '-'}", "",
                "**Answer shown to the user:**", "", a["answer"], ""]
        if a["blocked_answer"]:
            out += [f"*(guardrail blocked the model's answer: {a['guardrail']})*", "",
                    "Blocked answer:", "", a["blocked_answer"], ""]
        queries = [s["args"].get("query") for s in a["trace"] if s["tool"] == "search"]
        out += [f"**Searches:** {queries}", "", "<details><summary>Retrieved passages</summary>", ""]
        for label, text in passages(a["trace"]).items():
            out += [f"**{label}** {text}", ""]
        out += ["</details>", "", "---", ""]
    GRADING_SHEET.write_text("\n".join(out), encoding="utf-8")


# ---------------------------------------------------------------- 3. judge

def judge_prompt(rubric: str, q: dict, a: dict) -> str:
    evidence = "\n\n".join(f"{label}\n{text}" for label, text in passages(a["trace"]).items()) or "(none)"
    return f"""{rubric}

---
Grade the assistant's answer below with the rubric above. Decide "supported" only from the
retrieved passages, not from your own knowledge.

Question ({q['kind']}): {q['question']}

Reference answer: {q['reference_answer']}

Assistant's answer:
{a['answer']}

Retrieved passages (the only evidence):
{evidence}

Return JSON: {{"correct": 0 or 1, "supported": 0 or 1, "reason": "one or two sentences"}}.
correct = right against the reference answer (or a proper refusal); supported = every claim in
the answer is in the retrieved passages."""


def call_judge(prompt: str) -> dict:
    from google import genai
    from google.genai import types
    client = index.gemini()
    config = types.GenerateContentConfig(
        temperature=0, response_mime_type="application/json",
        response_schema={"type": "object", "required": ["correct", "supported", "reason"],
                         "properties": {"correct": {"type": "integer"}, "supported": {"type": "integer"},
                                        "reason": {"type": "string"}}})
    last = None
    for wait in (0, 15, 30, 60):  # the whole chain again after a pause, as in agent.py
        time.sleep(wait)
        for model in JUDGE_MODELS:
            try:
                r = client.models.generate_content(model=model, contents=prompt, config=config)
                verdict = json.loads(r.text)
                u = r.usage_metadata
                return {"correct": int(verdict["correct"]), "supported": int(verdict["supported"]),
                        "reason": verdict["reason"], "judge_model": model,
                        "judge_tokens": (u.prompt_token_count or 0) + (u.candidates_token_count or 0)}
            except genai.errors.APIError as error:
                last = error
                if error.code not in (429, 500, 503, 504):
                    raise
            except (json.JSONDecodeError, KeyError, ValueError) as error:
                last = error
    raise RuntimeError(f"judge failed on every model: {last}")


def run_judge(questions: list[dict], answers: dict, rerun: bool) -> dict | None:
    if not RUBRIC.is_file():
        print(f"No {RUBRIC.relative_to(ROOT)} yet: the judge is skipped.")
        return None
    rubric = RUBRIC.read_text(encoding="utf-8")
    saved = {} if rerun else read_jsonl(VERDICTS)
    todo = []
    for q in questions:
        a = answers.get(q["id"])
        if a:
            key = sha(rubric, q["question"], q["reference_answer"], a["answer"])
            if saved.get(q["id"], {}).get("key") != key:
                todo.append((q, a, key))
    if todo:
        print(f"Judging {len(todo)} answers ...")
    for n, (q, a, key) in enumerate(todo, 1):
        try:
            verdict = call_judge(judge_prompt(rubric, q, a))
        except Exception as error:  # noqa: BLE001 - leave it for the next run
            print(f"  {q['id']}: judge failed ({str(error)[:100]}); try again later")
            continue
        saved[q["id"]] = {"id": q["id"], "key": key, **verdict}
        write_jsonl(VERDICTS, [saved[k] for k in sorted(saved)])
        print(f"  {n}/{len(todo)} {q['id']}: correct={verdict['correct']} supported={verdict['supported']}",
              flush=True)
    return saved


# ---------------------------------------------------------------- 4. agreement, failures, summary

def kappa(a: list[int], b: list[int]) -> float | None:
    if not a:
        return None
    po = sum(x == y for x, y in zip(a, b)) / len(a)
    pa, pb = sum(a) / len(a), sum(b) / len(b)
    pe = pa * pb + (1 - pa) * (1 - pb)
    return 1.0 if pe == 1 else (po - pe) / (1 - pe)


def human_labels() -> dict:
    if not HUMAN_LABELS.is_file():
        return {}
    with HUMAN_LABELS.open(newline="", encoding="utf-8") as f:
        return {r["id"].strip(): r for r in csv.DictReader(f) if (r.get("id") or "").strip()
                and (r.get("correct") or "").strip() in ("0", "1")}


def auto_category(q: dict, checks: dict, verdict: dict | None) -> str:
    """A first guess at the failure cause, for the author to review (bad test questions are theirs to spot)."""
    correct = verdict["correct"] if verdict else None
    supported = verdict["supported"] if verdict else None
    if q["kind"] == "unanswerable":
        if correct == 0 or (correct is None and not (checks["refusal"] or checks["partial"])):
            return "unsupported claim (answered an unanswerable question)"
        return "unsupported claim" if supported == 0 else ""
    if checks["refusal"]:
        reason = "retrieval miss" if not checks["retrieved_expected"] else "wrong refusal"
        return reason + (" (guardrail blocked)" if checks["guardrail"] else "")
    if correct == 0:
        return "retrieval miss" if not checks["retrieved_expected"] else "wrong answer from the right passage"
    if supported == 0:
        return "unsupported claim"
    return ""


def summarise(questions, retrieval, answers, verdicts) -> dict:
    labels = human_labels()
    rows = []
    for q in questions:
        a = answers.get(q["id"])
        if not a:
            continue
        checks = code_checks(q, a)
        v = (verdicts or {}).get(q["id"])
        h = labels.get(q["id"])
        rows.append({
            "id": q["id"], "kind": q["kind"], **checks,
            "judge_correct": v["correct"] if v else "", "judge_supported": v["supported"] if v else "",
            "human_correct": h["correct"] if h else "", "human_supported": (h.get("supported") or "").strip() if h else "",
            "auto_category": auto_category(q, checks, v),
            "searches": a["searches"], "input_tokens": a["input_tokens"], "output_tokens": a["output_tokens"],
            "seconds": a["seconds"], "model": ", ".join(a["models"]), "judge_reason": v["reason"] if v else "",
        })
    if rows:
        with RESULTS.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)

    answerable = [r for r in rows if r["kind"] != "unanswerable"]
    unanswerable = [r for r in rows if r["kind"] == "unanswerable"]
    judged = [r for r in rows if r["judge_correct"] != ""]
    both = [r for r in judged if r["human_correct"] != ""]
    hc = [int(r["human_correct"]) for r in both]
    jc = [int(r["judge_correct"]) for r in both]
    sup = [r for r in both if r["human_supported"] in ("0", "1")]
    hs = [int(r["human_supported"]) for r in sup]
    js = [int(r["judge_supported"]) for r in sup]
    tokens = [r["input_tokens"] + r["output_tokens"] for r in rows]
    seconds = [r["seconds"] for r in rows]
    return {
        "retrieval": retrieval,
        "answers": len(rows),
        "answerable": len(answerable), "unanswerable": len(unanswerable),
        "wrong_refusals": [r["id"] for r in answerable if r["refusal"]],
        "correct_refusals": [r["id"] for r in unanswerable if r["refusal"]],
        "partial_unanswerable": [r["id"] for r in unanswerable if r["partial"]],
        "answered_unanswerable": [r["id"] for r in unanswerable if not r["refusal"] and not r["partial"]],
        "partly_covered_answerable": [r["id"] for r in answerable if r["partial"]],
        "citations_valid": sum(r["citations_valid"] for r in rows),
        "cites_expected": sum(bool(r["cites_expected"]) for r in answerable if not r["refusal"]),
        "answered_answerable": sum(not r["refusal"] for r in answerable),
        "guardrail_fired": {r["id"]: r["guardrail"] for r in rows if r["guardrail"]},
        "judged": len(judged),
        "judge_correct": sum(int(r["judge_correct"]) for r in judged),
        "judge_supported": sum(int(r["judge_supported"]) for r in judged),
        "human_graded": len(both),
        "agree_correct": sum(x == y for x, y in zip(hc, jc)), "kappa_correct": kappa(hc, jc),
        "agree_supported": sum(x == y for x, y in zip(hs, js)), "kappa_supported": kappa(hs, js),
        "supported_graded": len(sup),
        "disagreements": [r["id"] for r in both if r["human_correct"] != str(r["judge_correct"])
                          or (r["human_supported"] in ("0", "1") and r["human_supported"] != str(r["judge_supported"]))],
        "failures": {cat: [r["id"] for r in rows if r["auto_category"] == cat]
                     for cat in sorted({r["auto_category"] for r in rows if r["auto_category"]})},
        "cost": {"mean_tokens": statistics.mean(tokens) if tokens else 0,
                 "median_tokens": statistics.median(tokens) if tokens else 0,
                 "mean_seconds": statistics.mean(seconds) if seconds else 0,
                 "median_seconds": statistics.median(seconds) if seconds else 0,
                 "searches": sum(r["searches"] for r in rows),
                 "models": dict(Counter(r["model"] for r in rows))},
    }


def write_summary(s: dict) -> str:
    lines = ["# Evaluation summary", "", "## Retrieval (answerable questions)", "",
             "| design | hit@1 | hit@3 | hit@5 | multi, both passages @1/@3/@5 | words added @1/@3/@5 |",
             "|---|---|---|---|---|---|"]
    for design, r in s["retrieval"].items():
        multi = " / ".join(f"{r[f'multi_all@{k}']:.0%}" for k in KS if r[f"multi_all@{k}"] is not None)
        words = " / ".join(f"{r[f'words@{k}']:.0f}" for k in KS)
        lines.append(f"| {design} | " + " | ".join(f"{r[f'hit@{k}']:.0%}" for k in KS) + f" | {multi} | {words} |")
    lines += ["", f"Hit = an expected passage is among the top k (for multi: at least one). Precise = "
              f"expected location has at most {PRECISE_MAX_CHUNKS} chunks; broad = more (any chunk counts).", "",
              "| design | precise hit@1/@3/@5 | broad hit@1/@3/@5 |", "|---|---|---|"]
    for design, r in s["retrieval"].items():
        cell = lambda g: " / ".join(f"{r[f'{g}_hit@{k}']:.0%}" for k in KS) + f" (n={r[f'{g}_n']})"
        lines.append(f"| {design} | {cell('precise')} | {cell('broad')} |")
    if s["answers"]:
        lines += ["", "## End to end (agent)", "",
                  f"- Answerable answered: {pct(s['answered_answerable'], s['answerable'])} "
                  f"(of which say part is not covered: {s['partly_covered_answerable']}); "
                  f"wrong refusals: {len(s['wrong_refusals'])} {s['wrong_refusals']}",
                  f"- Unanswerable: refused {s['correct_refusals']}; partial answer that says what is not "
                  f"covered {s['partial_unanswerable']}; answered anyway {s['answered_unanswerable']}",
                  f"- Citations valid (code check, model's own answer): {pct(s['citations_valid'], s['answers'])}",
                  f"- Answers that cite an expected passage: {pct(s['cites_expected'], s['answered_answerable'])}",
                  f"- Guardrail fired: {len(s['guardrail_fired'])} {s['guardrail_fired']}"]
        if s["judged"]:
            lines += [f"- Judge: correct {pct(s['judge_correct'], s['judged'])}, "
                      f"supported {pct(s['judge_supported'], s['judged'])}"]
        if s["human_graded"]:
            k = lambda x: f"{x:.2f}" if x is not None else "n/a"
            lines += [f"- Agreement with your grades: correct {pct(s['agree_correct'], s['human_graded'])} "
                      f"(kappa {k(s['kappa_correct'])}), supported {pct(s['agree_supported'], s['supported_graded'])} "
                      f"(kappa {k(s['kappa_supported'])}); disagreements: {s['disagreements']}"]
        lines += ["", "## Failures (automatic first guess; review them and spot bad test questions)", ""]
        lines += [f"- {cat}: {len(ids)} {ids}" for cat, ids in s["failures"].items()] or ["- none"]
        c = s["cost"]
        lines += ["", "## Cost and latency per question", "",
                  f"- tokens: mean {c['mean_tokens']:.0f}, median {c['median_tokens']:.0f}",
                  f"- seconds: mean {c['mean_seconds']:.1f}, median {c['median_seconds']:.1f}",
                  f"- searches (one embedding each): {c['searches']} in total; models: {c['models']}"]
    text = "\n".join(lines) + "\n"
    SUMMARY_MD.write_text(text, encoding="utf-8")
    SUMMARY_JSON.write_text(json.dumps(s, indent=2, default=str), encoding="utf-8")
    return text


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate retrieval and the agent.")
    parser.add_argument("--retrieval", action="store_true", help="stage 1 only")
    parser.add_argument("--answers", action="store_true", help="stages 1-2, no judge")
    parser.add_argument("--rerun", action="store_true", help="ignore saved answers and verdicts")
    args = parser.parse_args()

    questions = load_questions()
    _, retrieval = evaluate_retrieval(questions)
    answers, verdicts = {}, None
    if not args.retrieval:
        answers = asyncio.run(run_agent(questions, args.rerun))
        write_grading_sheet(questions, answers)
        if not args.answers:
            verdicts = run_judge(questions, answers, args.rerun)
    summary = summarise(questions, retrieval, answers, verdicts if not args.answers else None)
    print("\n" + write_summary(summary))
    missing = [q["id"] for q in questions if q["id"] not in answers] if not args.retrieval else []
    if missing:
        print(f"WARNING: no saved answer for {missing}; run again to retry them.", file=sys.stderr)


if __name__ == "__main__":
    main()
