"""
Assignment 3: evaluation (`main.py evaluate`).

1. Retrieval: hit rate at k = 1, 3, 5 for each design, on answerable questions.
   A hit means a retrieved chunk is from the expected act and covers the expected
   article. A `multi` question counts only when every expected passage is found.
2. End to end: the agent answers every question (add_document never approved).
3. Code checks: refusal right or wrong, every citation returned by search,
   expected article cited, guardrail fired.
4. LLM judge (JUDGE_MODEL) with a rubric and the retrieved text as evidence.
5. Agreement between the judge and eval/human_labels.csv.

Answers and verdicts are cached in eval/ so a re-run does not spend quota again;
set FRESH=1 to redo them. Outputs: eval/retrieval.csv, eval/answers.jsonl,
eval/results.csv, eval/summary.md.
"""

from __future__ import annotations

import csv
import json
import os
import re
import sys
import time
from pathlib import Path

import retrieval as rt

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
ANSWERS = EVAL / "answers.jsonl"
VERDICTS = EVAL / "verdicts.jsonl"
HUMAN = EVAL / "human_labels.csv"
DESIGNS = ["fixed", "article", "article_hybrid", "article_bm25", "article_routed"]
KS = (1, 3, 5)
JUDGE_MODEL = "gemini-3.5-flash-lite"   # gemini-3.5-flash free tier is 20 requests/day; see REPORT
FRESH = os.environ.get("FRESH") == "1"

RUBRIC = """You grade answers from an assistant that answers questions about EU law (GDPR, Digital Services Act, ePrivacy Directive) for the team of a student social app, using only retrieved passages.

You get: the question, its kind, a reference answer written by a human from the law, the assistant's answer, and the passages the assistant retrieved (the evidence).

correct = 1 if:
- kind is single or multi: the answer states the substance of the reference answer (the same obligation, right, condition or exception) and says nothing that contradicts it. Extra true detail is fine. Missing a main condition of the reference, or answering only one of the two parts of a multi question, is 0. A refusal is 0.
- kind is unanswerable: the answer says the corpus does not cover the question and does not then give an answer to it anyway. Pointing to a related rule that is in the corpus is fine.
otherwise correct = 0.

supported = 1 if every factual claim in the answer about what the law says can be found in the evidence passages, with the same meaning. A refusal with no claims is supported. A number, deadline, amount or national rule not in the evidence makes it 0. Generic advice like "check with a lawyer" is not a claim.

Reply with JSON only: {"correct": 0 or 1, "supported": 0 or 1, "reason": "one sentence"}"""


def log(*a):
    print(*a, file=sys.stderr, flush=True)


def read_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if (r.get("question") or "").strip()]
    for r in rows:
        r["kind"] = r["kind"].strip().lower()
        srcs = [s.strip().lower() for s in r["expected_source"].split(";") if s.strip()]
        locs = [l.strip() for l in r["expected_location"].split(";") if l.strip()]
        if len(locs) == 1 and len(srcs) > 1:
            locs = locs * len(srcs)
        if len(srcs) == 1 and len(locs) > 1:
            srcs = srcs * len(locs)
        r["targets"] = [(s, article_number(l)) for s, l in zip(srcs, locs)]
    return rows


def article_number(location: str) -> str:
    m = re.search(r"(\d+[a-z]?)", location.lower().replace("article", ""))
    return m.group(1) if m else location


def covers(chunk: dict, target: tuple[str, str]) -> bool:
    return chunk["source"] == target[0] and target[1] in chunk["articles"]


# ------------------------------------------------------------------ 1. retrieval

def evaluate_retrieval(questions: list[dict]) -> tuple[list[dict], dict]:
    rows, table = [], {}
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    for design in DESIGNS:
        hits = {k: 0 for k in KS}
        words = []
        for q in answerable:
            res = rt.search(q["question"], k=max(KS), design=design)
            words.append(sum(len(c["text"].split()) for c in res))
            rank = None
            for k in KS:
                found = all(any(covers(c, t) for c in res[:k]) for t in q["targets"])
                hits[k] += found
            for i in range(len(res)):
                if all(any(covers(c, t) for c in res[:i + 1]) for t in q["targets"]):
                    rank = i + 1
                    break
            rows.append({"design": design, "id": q["id"], "kind": q["kind"], "rank": rank or "",
                         "top5": " | ".join(rt.cite(c) for c in res)})
        n = len(answerable)
        table[design] = {**{f"hit@{k}": hits[k] / n for k in KS}, "n": n,
                         "words_top5": sum(words) / n,
                         **{f"multi hit@{k}": None for k in ()}}
        for kind in ("single", "multi"):
            ids = {q["id"] for q in answerable if q["kind"] == kind}
            r = [x for x in rows if x["design"] == design and x["id"] in ids]
            table[design][f"{kind} hit@5"] = sum(1 for x in r if x["rank"] != "") / max(len(r), 1)
        log(f"{design:15s} " + "  ".join(f"hit@{k} {table[design][f'hit@{k}']:.2f}" for k in KS))
    with (EVAL / "retrieval.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    return rows, table


# ------------------------------------------------------------------ 2. agent answers

def load_jsonl(path: Path) -> dict:
    out = {}
    if path.exists() and not FRESH:
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                out[r["key"]] = r
    return out


def run_agent(questions: list[dict]) -> dict[str, dict]:
    import agent
    cache = load_jsonl(ANSWERS)
    out = {}
    for q in questions:
        key = q["question"]
        if key not in cache:
            log(f"agent {q['id']}")
            for attempt in range(3):
                try:
                    r = agent.run(q["question"], approver=lambda args: False)
                    break
                except Exception as e:  # noqa: BLE001
                    log(f"  failed ({e}); retrying")
                    time.sleep(30)
            else:
                raise RuntimeError(f"agent failed on {q['id']}")
            cache[key] = {"key": key, "id": q["id"], **r}
            with ANSWERS.open("a", encoding="utf-8") as f:
                f.write(json.dumps(cache[key], ensure_ascii=False) + "\n")
        out[q["id"]] = cache[key]
    return out


# ------------------------------------------------------------------ 3. code checks

def code_checks(q: dict, a: dict) -> dict:
    from agent import is_refusal
    a = {**a, "refusal": is_refusal(a["answer"])}     # recompute, so fixes to the check apply to cached answers
    cited = list(a["citations"])
    chunks = {c["id"]: c for c in rt.get_index("article").chunks}
    cited_chunks = [chunks[c] for c in cited if c in chunks]
    retrieved_chunks = [chunks[c] for c in a["retrieved"] if c in chunks]
    should_refuse = q["kind"] == "unanswerable"
    return {
        "refused": int(a["refusal"]),
        "refusal_ok": int(a["refusal"] == should_refuse),
        "citations_valid": int(all(c in a["retrieved"] for c in cited)),
        "n_citations": len(cited),
        "expected_retrieved": "" if should_refuse else int(all(any(covers(c, t) for c in retrieved_chunks) for t in q["targets"])),
        "expected_cited": "" if should_refuse else int(all(any(covers(c, t) for c in cited_chunks) for t in q["targets"])),
        "guardrail": a.get("guardrail") or "",
    }


# ------------------------------------------------------------------ 4. judge

def evidence(a: dict) -> str:
    chunks = {c["id"]: c for c in rt.get_index("article").chunks}
    ids = list(a["citations"]) + [c for c in a["retrieved"] if c not in a["citations"]]
    parts = [f"[{c}] {rt.cite(chunks[c])}\n{chunks[c]['text']}" for c in ids if c in chunks]
    return "\n\n".join(parts) or "(nothing retrieved)"


def judge(questions: list[dict], answers: dict[str, dict]) -> dict[str, dict]:
    from google import genai
    from api_key import load_api_key
    client = genai.Client(api_key=load_api_key())
    cache = load_jsonl(VERDICTS)
    out = {}
    for q in questions:
        a = answers[q["id"]]
        key = q["question"] + "||" + a["answer"] + "||" + q["reference_answer"]
        if key not in cache:
            log(f"judge {q['id']}")
            prompt = (f"{RUBRIC}\n\nQUESTION ({q['kind']}): {q['question']}\n\nREFERENCE ANSWER: {q['reference_answer']}"
                      f"\n\nASSISTANT ANSWER: {a['answer']}\n\nEVIDENCE PASSAGES:\n{evidence(a)}")
            for attempt in range(4):
                try:
                    text = client.models.generate_content(model=JUDGE_MODEL, contents=prompt).text
                    v = json.loads(re.search(r"\{.*\}", text, re.S).group(0))
                    break
                except Exception as e:  # noqa: BLE001
                    log(f"  judge failed ({str(e)[:120]}); retrying")
                    time.sleep(20)
            else:
                raise RuntimeError(f"judge failed on {q['id']}")
            cache[key] = {"key": key, "id": q["id"], "correct": int(v["correct"]),
                          "supported": int(v["supported"]), "reason": v.get("reason", "")}
            with VERDICTS.open("a", encoding="utf-8") as f:
                f.write(json.dumps(cache[key], ensure_ascii=False) + "\n")
        out[q["id"]] = cache[key]
    return out


# ------------------------------------------------------------------ 5. agreement, failures, summary

def read_human() -> dict[str, dict]:
    if not HUMAN.exists():
        return {}
    with HUMAN.open(newline="", encoding="utf-8") as f:
        return {r["id"].strip(): r for r in csv.DictReader(f) if (r.get("id") or "").strip()}


def failure_cause(q: dict, checks: dict, v: dict) -> str:
    """First guess at the cause; checked by hand in REPORT.md."""
    if q["kind"] == "unanswerable":
        return "" if v["correct"] and checks["refused"] else "answered an unanswerable question (unsupported claim)"
    if v["correct"] and v["supported"]:
        return ""
    if checks["refused"]:
        return "retrieval miss" if not checks["expected_retrieved"] else "wrong refusal"
    if not v["supported"]:
        return "unsupported claim"
    if not checks["expected_retrieved"]:
        return "retrieval miss"
    return "wrong answer from the right passage"


def main() -> None:
    questions = read_questions()
    log(f"{len(questions)} questions")
    _, table = evaluate_retrieval(questions)
    answers = run_agent(questions)
    verdicts = judge(questions, answers)
    human = read_human()

    results = []
    for q in questions:
        a, v = answers[q["id"]], verdicts[q["id"]]
        c = code_checks(q, a)
        h = human.get(q["id"], {})
        results.append({
            "id": q["id"], "kind": q["kind"], **c,
            "judge_correct": v["correct"], "judge_supported": v["supported"], "judge_reason": v["reason"],
            "human_correct": h.get("correct", ""), "human_supported": h.get("supported", ""),
            "cause": failure_cause(q, c, v),
            "tokens_in": a["tokens"]["input"], "tokens_out": a["tokens"]["output"],
            "tool_calls": len(a["trace"]), "seconds": a["seconds"],
        })
    with (EVAL / "results.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(results[0]))
        w.writeheader()
        w.writerows(results)

    n = len(results)
    ans = [r for r in results if r["kind"] != "unanswerable"]
    una = [r for r in results if r["kind"] == "unanswerable"]
    graded = [r for r in results if r["human_correct"] != ""]
    agree_c = sum(int(r["human_correct"]) == r["judge_correct"] for r in graded)
    agree_s = sum(int(r["human_supported"]) == r["judge_supported"] for r in graded)
    causes = {}
    for r in results:
        if r["cause"]:
            causes[r["cause"]] = causes.get(r["cause"], 0) + 1

    lines = ["# Evaluation summary", "", "## Retrieval (answerable questions)", "",
             "| design | hit@1 | hit@3 | hit@5 | single hit@5 | multi hit@5 | words added (top 5) |",
             "|---|---|---|---|---|---|---|"]
    for d, t in table.items():
        lines.append(f"| {d} | {t['hit@1']:.2f} | {t['hit@3']:.2f} | {t['hit@5']:.2f} | "
                     f"{t['single hit@5']:.2f} | {t['multi hit@5']:.2f} | {t['words_top5']:.0f} |")
    lines += ["", f"Served design: {rt.DEFAULT_DESIGN}. Answerable questions: {table[DESIGNS[0]]['n']}.", "",
              "## End to end", "",
              f"- Questions: {n} ({len(ans)} answerable, {len(una)} unanswerable)",
              f"- Correct (judge): {sum(r['judge_correct'] for r in ans)}/{len(ans)} answerable",
              f"- Unsupported answers (judge): {sum(1 - r['judge_supported'] for r in results)}/{n}",
              f"- Correct refusals: {sum(r['refused'] for r in una)}/{len(una)} unanswerable",
              f"- Wrong refusals: {sum(r['refused'] for r in ans)}/{len(ans)} answerable",
              f"- Citations all valid: {sum(r['citations_valid'] for r in results)}/{n}; guardrail fired on {sum(1 for r in results if r['guardrail'])}",
              f"- Expected article retrieved by the agent: {sum(r['expected_retrieved'] for r in ans)}/{len(ans)}; cited: {sum(r['expected_cited'] for r in ans)}/{len(ans)}",
              "", "## Judge vs human", "",
              f"- Graded by hand: {len(graded)}",
              f"- Agreement on correct: {agree_c}/{len(graded)}" if graded else "- No human labels yet",
              f"- Agreement on supported: {agree_s}/{len(graded)}" if graded else "",
              "", "## Failures (first guess by code)", ""]
    lines += [f"- {k}: {v}" for k, v in sorted(causes.items(), key=lambda x: -x[1])] or ["- none"]
    sec = [r["seconds"] for r in results]
    tin = [r["tokens_in"] for r in results]
    tout = [r["tokens_out"] for r in results]
    lines += ["", "## Cost per question", "",
              f"- Mean {sum(tin) / n:.0f} input + {sum(tout) / n:.0f} output tokens, {sum(r['tool_calls'] for r in results) / n:.1f} tool calls",
              f"- Mean {sum(sec) / n:.1f} s, max {max(sec):.1f} s"]
    (EVAL / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
