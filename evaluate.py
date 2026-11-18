"""
Assignment 3: evaluation (`main.py evaluate`).

1. Retrieval: hit rate at k = 1, 3, 5 for 2 chunkings x 2 search methods  -> eval/retrieval_results.csv
2. End to end: the agent (agent.py) answers every question on the base corpus -> eval/answers.jsonl
3. Code checks: citations valid, expected law cited, refusal detected
4. LLM judge with a rubric and the retrieved text as evidence              -> eval/judge.jsonl
5. Agreement with my own grades in eval/human_labels.csv
6. Failure classification, cost and latency                                 -> eval/results.csv, eval/summary.json
7. Before/after adding a document for one unanswerable question            -> eval/before_after.md

Agent answers and judge verdicts are cached in eval/ (keyed by question, model and
AGENTS.md), so a re-run only calls Gemini for what changed. EVAL_FRESH=1 ignores the cache.
"""

from __future__ import annotations

import asyncio
import csv
import hashlib
import json
import os
import sys
import time
from pathlib import Path

import retrieval
from agent import FALLBACKS, MODEL, SYSTEM_PROMPT, check_citations, corpus_tools, is_refusal, norm_cite, run_async, CITE_RE
from index import genai_client

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
HUMAN = EVAL / "human_labels.csv"
ANSWERS = EVAL / "answers.jsonl"
JUDGE = EVAL / "judge.jsonl"
FRESH = os.environ.get("EVAL_FRESH") == "1"
JUDGE_MODEL = os.environ.get("JUDGE_MODEL", MODEL)
PAUSE = float(os.environ.get("EVAL_PAUSE", "4"))   # seconds between questions (free-tier rate limit)

BEFORE_AFTER_QID = "q30"
ADDED_DOC = ROOT / "docs_to_add" / "BOE-A-2018-7833.html"


def log(*a):
    print(*a, flush=True)


def load_questions() -> list[dict]:
    with QUESTIONS.open(encoding="utf-8", newline="") as f:
        return [r for r in csv.DictReader(f) if r["question"].strip()]


def expected_pairs(q: dict) -> list[tuple[str, str]]:
    srcs = [s.strip() for s in q["expected_source"].split(";")]
    locs = [loc.strip() for loc in q["expected_location"].split(";")]
    if len(srcs) == 1 and len(locs) > 1:
        srcs *= len(locs)
    return [norm_cite(s, l) for s, l in zip(srcs, locs)]


def chunk_pairs(meta: dict) -> set[tuple[str, str]]:
    return {norm_cite(meta["source"], l) for l in meta["locations"].split("|")}


# --------------------------------------------------------------------------- 1. retrieval

def eval_retrieval(questions: list[dict]) -> list[dict]:
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    rows = []
    for design in ("fixed", "structure"):
        for method in ("vector", "hybrid"):
            hits = {1: 0, 3: 0, 5: 0}
            all5 = words = 0
            for q in answerable:
                exp = expected_pairs(q)
                res = retrieval.search(q["question"], k=5, design=design, method=method, base_only=True)
                found = [chunk_pairs(h["metadata"]) for h in res]
                for k in hits:
                    hits[k] += any(set(exp) & f for f in found[:k])
                all5 += all(any(e in f for f in found) for e in exp)
                words += sum(len(h["text"].split()) for h in res)
            n = len(answerable)
            rows.append({"design": design, "method": method, "questions": n,
                         "hit@1": round(hits[1] / n, 3), "hit@3": round(hits[3] / n, 3),
                         "hit@5": round(hits[5] / n, 3), "all_passages@5": round(all5 / n, 3),
                         "words_in_prompt@5": round(words / n)})
            log(f"  {design:9} {method:6}  hit@1 {rows[-1]['hit@1']:.2f}  hit@3 {rows[-1]['hit@3']:.2f}  "
                f"hit@5 {rows[-1]['hit@5']:.2f}  all@5 {rows[-1]['all_passages@5']:.2f}  "
                f"words {rows[-1]['words_in_prompt@5']}")
    with (EVAL / "retrieval_results.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    return rows


# --------------------------------------------------------------------------- cache helpers

def key_for(*parts: str) -> str:
    return hashlib.sha1("|".join(parts).encode()).hexdigest()[:16]


def load_jsonl(path: Path) -> dict:
    if FRESH or not path.exists():
        return {}
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            out[r["key"]] = r
    return out


def append_jsonl(path: Path, row: dict) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


# --------------------------------------------------------------------------- 2. agent answers

AGENT_VERSION = key_for(MODEL, SYSTEM_PROMPT, Path(ROOT / "agent.py").read_text(encoding="utf-8"),
                        retrieval.DEFAULT_DESIGN, retrieval.DEFAULT_METHOD)


async def run_agent_all(questions: list[dict], base_only: bool = True) -> dict[str, dict]:
    cache = load_jsonl(ANSWERS)
    if FRESH and ANSWERS.exists():
        ANSWERS.unlink()
    out = {}
    todo = [q for q in questions if key_for(AGENT_VERSION, q["id"], q["question"], str(base_only)) not in cache]
    for q in questions:
        k = key_for(AGENT_VERSION, q["id"], q["question"], str(base_only))
        if k in cache:
            out[q["id"]] = cache[k]
    if todo:
        async with corpus_tools(base_only=base_only) as tools:
            for i, q in enumerate(todo, 1):
                log(f"  [{i}/{len(todo)}] {q['id']} {q['question'][:70]}")
                try:
                    r = await run_async(q["question"], approver=lambda a: False, tools=tools)
                except Exception as e:  # noqa: BLE001 - one failed question must not stop the run
                    log(f"    error: {type(e).__name__}: {str(e)[:200]}")
                    continue
                r = {"key": key_for(AGENT_VERSION, q["id"], q["question"], str(base_only)), "id": q["id"], **r}
                append_jsonl(ANSWERS, r)
                out[q["id"]] = r
                time.sleep(PAUSE)
    return out


# --------------------------------------------------------------------------- 3. code checks

def code_checks(q: dict, a: dict) -> dict:
    answer = a["answer"]
    offered = {tuple(x.strip("[]").split(", ", 1)) for x in a["offered"]}
    offered = {norm_cite(s, l) for s, l in offered}
    cited = {norm_cite(s, l) for s, l in CITE_RE.findall(answer)}
    refused = is_refusal(answer)
    exp = expected_pairs(q) if q["kind"] != "unanswerable" else []
    return {
        "refused": int(refused),
        "n_citations": len(cited),
        "citations_valid": int(not check_citations(answer, offered)),
        "cites_expected": int(any(e in cited for e in exp)) if exp else "",
        "retrieved_expected": int(any(e in offered for e in exp)) if exp else "",
        "correct_refusal": int(refused) if q["kind"] == "unanswerable" else "",
        "wrong_refusal": int(refused) if q["kind"] != "unanswerable" else "",
    }


# --------------------------------------------------------------------------- 4. judge

RUBRIC = """You grade an assistant that answers questions about Spanish tenancy law from retrieved law text.

You get: the QUESTION, a REFERENCE answer written by the course student from the law, the RETRIEVED
TEXT the assistant saw, and the ANSWER.

correct (1/0):
  1 if the answer gives the same key facts as the reference (numbers, deadlines, yes/no, who) with no
    contradicting fact. Extra correct detail is fine. For a question the reference says the corpus does not
    cover, 1 only if the answer says it cannot answer / the corpus does not cover it (a short pointer to where
    to look is fine) and does not invent the missing fact.
  0 if a key fact is missing, wrong or contradicts the reference, or the answer refuses although the reference
    has an answer, or it invents an answer to a question the corpus does not cover.
supported (1/0):
  1 if every factual claim in the answer is stated in the RETRIEVED TEXT (paraphrase is fine). A refusal is
    supported.
  0 if any claim (a number, deadline, condition, article) is not in the retrieved text.
Judge only against the reference and the retrieved text, not your own knowledge of the law.
Return JSON: {"correct": 0|1, "supported": 0|1, "reason": "<one sentence>"}"""


def judge_one(q: dict, a: dict) -> dict:
    from google.genai import types
    evidence = "\n\n".join(a["retrieved"])[:30000] or "(no text was retrieved)"
    prompt = (f"{RUBRIC}\n\nQUESTION:\n{q['question']}\n\nREFERENCE:\n{q['reference_answer']}\n\n"
              f"RETRIEVED TEXT:\n{evidence}\n\nANSWER:\n{a['answer']}")
    schema = {"type": "object", "properties": {"correct": {"type": "integer"}, "supported": {"type": "integer"},
                                               "reason": {"type": "string"}},
              "required": ["correct", "supported", "reason"]}
    models = [JUDGE_MODEL] + [m for m in FALLBACKS if m != JUDGE_MODEL]
    for attempt in range(6):
        model = models[attempt % len(models)]
        try:
            started = time.time()
            res = genai_client().models.generate_content(
                model=model, contents=prompt,
                config=types.GenerateContentConfig(temperature=0, response_mime_type="application/json",
                                                   response_schema=schema))
            v = json.loads(res.text)
            u = res.usage_metadata
            v["judge_tokens"] = (u.prompt_token_count or 0) + (u.candidates_token_count or 0)
            v["judge_seconds"] = round(time.time() - started, 2)
            v["judge_model"] = model
            return v
        except Exception as e:  # noqa: BLE001
            if attempt == 5:
                raise
            log(f"    judge retry ({type(e).__name__}: {str(e)[:100]})")
            time.sleep(10)
    raise RuntimeError("unreachable")


def judge_all(questions: list[dict], answers: dict) -> dict:
    cache = load_jsonl(JUDGE)
    if FRESH and JUDGE.exists():
        JUDGE.unlink()
    out = {}
    for q in questions:
        a = answers.get(q["id"])
        if not a:
            continue
        k = key_for(JUDGE_MODEL, RUBRIC, q["reference_answer"], a["answer"])
        if k not in cache:
            log(f"  judging {q['id']}")
            v = judge_one(q, a)
            cache[k] = {"key": k, "id": q["id"], **v}
            append_jsonl(JUDGE, cache[k])
            time.sleep(PAUSE / 2)
        out[q["id"]] = cache[k]
    return out


# --------------------------------------------------------------------------- 5. human agreement

def agreement(judge: dict) -> dict:
    if not HUMAN.exists():
        return {}
    with HUMAN.open(encoding="utf-8", newline="") as f:
        human = [r for r in csv.DictReader(f) if r.get("id", "").strip() and r.get("correct", "").strip()]
    res = {"graded_by_human": len(human)}
    for field in ("correct", "supported"):
        pairs = [(int(h[field]), int(judge[h["id"]][field])) for h in human
                 if h["id"] in judge and h.get(field, "").strip() in ("0", "1")]
        if not pairs:
            continue
        n = len(pairs)
        agree = sum(a == b for a, b in pairs) / n
        ph = sum(a for a, _ in pairs) / n
        pj = sum(b for _, b in pairs) / n
        pe = ph * pj + (1 - ph) * (1 - pj)
        kappa = (agree - pe) / (1 - pe) if pe < 1 else 1.0
        res[field] = {"n": n, "agreement": round(agree, 3), "cohen_kappa": round(kappa, 3),
                      "disagreements": [h["id"] for h in human if h["id"] in judge
                                        and h.get(field, "").strip() in ("0", "1")
                                        and int(h[field]) != int(judge[h["id"]][field])]}
    return res


# --------------------------------------------------------------------------- 6. failures

def classify(q: dict, c: dict, v: dict) -> str:
    """First-pass failure cause; I review each one by hand in REPORT.md."""
    if v["correct"] and v["supported"]:
        return ""
    if q["kind"] == "unanswerable":
        return "unsupported claim" if not c["refused"] else "bad test question?"
    if c["refused"]:
        return "wrong refusal" if c["retrieved_expected"] else "retrieval miss"
    if not c["retrieved_expected"]:
        return "retrieval miss"
    if not v["supported"]:
        return "unsupported claim"
    return "wrong answer from right passage"


# --------------------------------------------------------------------------- 7. before / after

async def before_after(questions: list[dict], answers_base: dict) -> None:
    q = next((x for x in questions if x["id"] == BEFORE_AFTER_QID), None)
    col = retrieval.get_collection(retrieval.DEFAULT_DESIGN)
    added = col.get(where={"origin": "added"}, include=[])["ids"]
    lines = [f"# Before / after adding a document\n", f"Question {BEFORE_AFTER_QID}: {q['question']}\n"]
    before = answers_base.get(BEFORE_AFTER_QID)
    lines.append(f"## Before (base corpus only)\n\n{before['answer'] if before else '(not run)'}\n")
    if not added:
        lines.append(f"## After\n\nNo document has been added yet. Run in a terminal:\n\n"
                     f"    uv run python main.py ask \"Add the document {ADDED_DOC.relative_to(ROOT)}\"\n")
    else:
        cache = load_jsonl(ANSWERS)
        k = key_for(AGENT_VERSION, q["id"], q["question"], "False")
        if k in cache:
            after = cache[k]
        else:
            after = await run_async(q["question"], approver=lambda a: False, base_only=False)
            after = {"key": k, "id": q["id"], **after}
            append_jsonl(ANSWERS, after)
        lines.append(f"## After (index includes {len(added)} added chunks)\n\n{after['answer']}\n\n"
                     f"Citations offered by search: {', '.join(after['offered'])}\n")
    (EVAL / "before_after.md").write_text("\n".join(lines), encoding="utf-8")
    log("  wrote eval/before_after.md")


# --------------------------------------------------------------------------- main

def main() -> None:
    questions = load_questions()
    log(f"== 1. Retrieval ({len(questions)} questions)")
    eval_retrieval(questions)

    log(f"== 2. Agent answers ({MODEL}, design={retrieval.DEFAULT_DESIGN}/{retrieval.DEFAULT_METHOD})")
    answers = asyncio.run(run_agent_all(questions, base_only=True))

    log("== 3-4. Code checks and judge")
    verdicts = judge_all(questions, answers)

    rows = []
    for q in questions:
        if q["id"] not in answers or q["id"] not in verdicts:
            continue
        a, v = answers[q["id"]], verdicts[q["id"]]
        c = code_checks(q, a)
        rows.append({"id": q["id"], "kind": q["kind"], **c,
                     "judge_correct": v["correct"], "judge_supported": v["supported"],
                     "failure_cause": classify(q, c, v), "judge_reason": v["reason"],
                     "searches": sum(t["name"] == "search" for t in a["tool_calls"]),
                     "tokens": a["tokens_in"] + a["tokens_out"], "seconds": a["seconds"],
                     "guardrail": " | ".join(a["guardrail_events"]), "answer": a["answer"]})
    with (EVAL / "results.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    ans = [r for r in rows if r["kind"] != "unanswerable"]
    una = [r for r in rows if r["kind"] == "unanswerable"]
    n = len(rows)
    summary = {
        "model": MODEL, "judge_model": JUDGE_MODEL, "design": retrieval.DEFAULT_DESIGN,
        "method": retrieval.DEFAULT_METHOD, "questions": n,
        "correct": sum(r["judge_correct"] for r in rows),
        "correct_answerable": f"{sum(r['judge_correct'] for r in ans)}/{len(ans)}",
        "unsupported": sum(1 - r["judge_supported"] for r in rows),
        "correct_refusals": f"{sum(r['refused'] for r in una)}/{len(una)}",
        "wrong_refusals": f"{sum(r['refused'] for r in ans)}/{len(ans)}",
        "citations_valid": f"{sum(r['citations_valid'] for r in rows)}/{n}",
        "cites_expected_article": f"{sum(r['cites_expected'] for r in ans)}/{len(ans)}",
        "guardrail_fired": sum(bool(r["guardrail"]) for r in rows),
        "failures_by_cause": {},
        "mean_tokens_per_question": round(sum(r["tokens"] for r in rows) / n),
        "mean_seconds_per_question": round(sum(r["seconds"] for r in rows) / n, 1),
        "agreement_with_human": agreement(verdicts),
    }
    for r in rows:
        if r["failure_cause"]:
            summary["failures_by_cause"][r["failure_cause"]] = summary["failures_by_cause"].get(r["failure_cause"], 0) + 1
    (EVAL / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    log(json.dumps(summary, indent=2, ensure_ascii=False))

    log("== 7. Before / after adding a document")
    asyncio.run(before_after(questions, answers))


if __name__ == "__main__":
    main()
