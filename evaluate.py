"""
Assignment 3: evaluation (`main.py evaluate`).

1. Retrieval: hit rate at k = 1, 3, 5 for four designs (fixed-size or structure-based
   chunks, vector or hybrid search). The best one is written to index/config.json,
   which the server reads.
2. End to end: agent.py answers every question in eval/questions.csv.
3. Code checks: citations point to retrieved passages; refusals on unanswerable
   questions; refusals on answerable ones.
4. LLM judge with a rubric and the retrieved text as evidence.
5. Agreement with your grades in eval/human_labels.csv.
6. Add-document demo: the Commission's prohibited-practices guidelines are added
   through the real tool and one unanswerable question is asked before and after.
7. Failure classes, cost and latency.

Everything is saved in eval/. Answers are cached in eval/answers.json: a rerun only
asks the questions it has no answer for (use --fresh to ask them all again).

    uv run python evaluate.py [--fresh] [--redo-demo]
"""

import argparse
import asyncio
import csv
import json
import os
import re
import statistics
import sys
import time
from pathlib import Path

import index as ix
from agent import CITE_RE, check_citations, corpus_agent, unit_of

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
KS = (1, 3, 5)
DEMO_QUESTION_ID = "q34"
# A different model from the agent's (override: JUDGE_MODEL=...).
JUDGE_MODEL = os.environ.get("JUDGE_MODEL", "gemma-4-26b-a4b-it")

REFUSAL_RE = re.compile(
    r"(do(es)? not|don't|doesn't|cannot|can't|could not|couldn't|no) "
    r"(cover|contain|include|address|specify|state|say|provide|mention|name|list|answer|find|have|"
    r"information|indicate|define)|not (covered|contained|included|addressed|specified|mentioned|available)|"
    r"outside (the|of) (the )?(scope|indexed|documents|corpus)|"
    r"(indexed )?(documents|corpus|texts) (do|does) not|is not in the (indexed )?(documents|corpus|texts)",
    re.I)


# --------------------------------------------------------------------------
# helpers
# --------------------------------------------------------------------------

def read_questions() -> list[dict]:
    with (EVAL / "questions.csv").open(newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r["question"].strip()]


def expected_pairs(q: dict) -> list[tuple[str, str]]:
    """[(source, unit)] a good answer needs; one source may serve several locations."""
    sources = [s.strip() for s in q["expected_source"].split(";") if s.strip()]
    locs = [unit_of(x) for x in q["expected_location"].split(";") if x.strip()]
    return [(sources[i] if i < len(sources) else sources[-1], loc) for i, loc in enumerate(locs)]


def chunk_covers(meta: dict, pair: tuple[str, str]) -> bool:
    return meta["source"] == pair[0] and pair[1] in meta["units"].split(";")


def save_json(path: Path, obj) -> None:
    path.write_text(json.dumps(obj, indent=2, ensure_ascii=False))


def log(*a):
    print(*a, flush=True)


# --------------------------------------------------------------------------
# 1. retrieval
# --------------------------------------------------------------------------

def retrieval_eval(questions: list[dict]) -> list[dict]:
    rows = []
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    for design in ix.DESIGNS:
        for method in ("vector", "hybrid"):
            hits = {k: 0 for k in KS}
            hits_any = {k: 0 for k in KS}
            words = {k: [] for k in KS}
            for q in answerable:
                res = ix.retrieve(q["question"], 5, design, method)
                pairs = expected_pairs(q)
                for k in KS:
                    top = [r["meta"] for r in res[:k]]
                    found = [any(chunk_covers(m, p) for m in top) for p in pairs]
                    hits[k] += all(found)
                    hits_any[k] += any(found)
                    words[k].append(sum(m["n_words"] for m in top))
            n = len(answerable)
            row = {"design": design, "method": method, "questions": n}
            for k in KS:
                row[f"hit@{k}"] = round(hits[k] / n, 3)
            for k in KS:
                row[f"any@{k}"] = round(hits_any[k] / n, 3)
            for k in KS:
                row[f"words@{k}"] = round(statistics.mean(words[k]))
            rows.append(row)
    with (EVAL / "retrieval_results.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    return rows


def choose_design(rows: list[dict]) -> dict:
    """Highest hit@5, then hit@3, hit@1, then fewer words in the prompt."""
    best = sorted(rows, key=lambda r: (-r["hit@5"], -r["hit@3"], -r["hit@1"], r["words@5"]))[0]
    ix.CONFIG_FILE.write_text(json.dumps({"design": best["design"], "method": best["method"]}))
    return best


# --------------------------------------------------------------------------
# 2-3. agent answers and code checks
# --------------------------------------------------------------------------

def deny(path: str) -> bool:
    return False


async def run_agent(questions: list[dict], cache: dict, parallel: int = 1) -> dict:
    todo = [q for q in questions if q["id"] not in cache]
    if not todo:
        return cache
    sem = asyncio.Semaphore(parallel)
    done = 0

    async def one(agent, q):
        nonlocal done
        async with sem:
            for attempt in range(3):
                try:
                    res = await agent.ask(q["question"])
                    break
                except Exception as e:  # noqa: BLE001
                    log(f"   {q['id']} attempt {attempt + 1} failed: {type(e).__name__}: {str(e)[:120]}")
                    await asyncio.sleep(10 * (attempt + 1))
            else:
                return
            cache[q["id"]] = res
            save_json(EVAL / "answers.json", cache)
            done += 1
            log(f"   [{done}/{len(todo)}] {q['id']} {res['seconds']}s, {res['searches']} searches, "
                f"{res['tokens_in']}+{res['tokens_out']} tokens")

    async with corpus_agent(approve=deny) as agent:
        await asyncio.gather(*(one(agent, q) for q in todo))
    return cache


def code_checks(q: dict, res: dict) -> dict:
    answer = res["answer"]
    retrieved = {tuple(x) for x in res["retrieved"]}
    cites = CITE_RE.findall(answer)
    invalid = check_citations(answer, retrieved)
    refused = bool(REFUSAL_RE.search(answer))
    out = {"has_citation": bool(cites), "invalid_citations": len(invalid), "refusal_detected": refused}
    if q["kind"] == "unanswerable":
        out["refusal_ok"] = refused
    else:
        pairs = expected_pairs(q)
        out["expected_retrieved"] = all(any(chunk_covers_pair(r, p) for r in retrieved) for p in pairs)
        out["expected_cited"] = all(
            any((s, unit_of(loc)) == p for s, loc in cites) for p in pairs)
        out["wrong_refusal"] = refused and not cites
    return out


def chunk_covers_pair(retrieved_pair: tuple[str, str], pair: tuple[str, str]) -> bool:
    return retrieved_pair == pair


# --------------------------------------------------------------------------
# 4. LLM judge
# --------------------------------------------------------------------------

RUBRIC = """You grade answers of a retrieval assistant that answers questions about the EU AI Act, the GDPR and
Commission guidelines, only from passages it retrieved. You get the question, its kind, a reference answer,
the retrieved passages (the only evidence) and the assistant's answer.

Grade two things, each 0 or 1.

correct
- Answerable question (single or multi): 1 if the answer states the key facts of the reference answer and
  contradicts none of them. Missing a secondary detail is fine; missing or changing a core fact (a number,
  a condition, who is obliged, which article) is 0. A refusal is 0.
- Unanswerable question: 1 only if the answer says that the indexed documents do not cover the question
  (it may mention nearby rules the documents do contain). 0 if it gives a specific answer as if the
  documents covered it.

supported
- 1 if every factual claim in the answer is stated in the retrieved passages. 0 if any claim (a number,
  a condition, a duty, an example) is not in them, even if it happens to be true. A refusal that makes no
  unsupported claims is 1. Closing lines such as "this is not legal advice" do not count as claims.

Reply with JSON only: {"correct": 0 or 1, "supported": 0 or 1, "reason": "one sentence"}"""


def judge(q: dict, res: dict) -> dict:
    from google.genai import types

    prompt = (f"{RUBRIC}\n\nQUESTION KIND: {q['kind']}\nQUESTION: {q['question']}\n"
              f"REFERENCE ANSWER: {q['reference_answer']}\n\nRETRIEVED PASSAGES:\n{res['passages'][:90000]}\n\n"
              f"ASSISTANT'S ANSWER:\n{res['answer']}")
    for attempt in range(5):
        try:
            r = ix.genai_client().models.generate_content(
                model=JUDGE_MODEL, contents=prompt,
                config=types.GenerateContentConfig(temperature=0))
            v = json.loads(re.search(r"\{.*\}", r.text, re.S).group(0))
            return {"judge_correct": int(v["correct"]), "judge_supported": int(v["supported"]),
                    "judge_reason": str(v.get("reason", ""))}
        except Exception as e:  # noqa: BLE001
            time.sleep(5 * (attempt + 1))
            err = str(e)[:150]
    return {"judge_correct": -1, "judge_supported": -1, "judge_reason": f"judge failed: {err}"}


# --------------------------------------------------------------------------
# 5. agreement with the human labels
# --------------------------------------------------------------------------

def agreement(rows: list[dict]) -> dict:
    path = EVAL / "human_labels.csv"
    if not path.exists():
        return {"graded": 0}
    with path.open(newline="", encoding="utf-8") as f:
        human = {r["id"]: r for r in csv.DictReader(f) if (r.get("id") or "").strip()
                 and r.get("correct", "").strip() in ("0", "1") and r.get("supported", "").strip() in ("0", "1")}
    by_id = {r["id"]: r for r in rows}
    out = {"graded": 0}
    for field in ("correct", "supported"):
        pairs = [(int(h[field]), by_id[i][f"judge_{field}"]) for i, h in human.items()
                 if i in by_id and by_id[i][f"judge_{field}"] in (0, 1)]
        if not pairs:
            continue
        n = len(pairs)
        agree = sum(a == b for a, b in pairs) / n
        pe = sum((sum(1 for a, _ in pairs if a == v) / n) * (sum(1 for _, b in pairs if b == v) / n) for v in (0, 1))
        kappa = (agree - pe) / (1 - pe) if pe < 1 else 1.0
        out[field] = {"n": n, "agreement": round(agree, 3), "kappa": round(kappa, 3),
                      "disagreements": [i for i, h in human.items() if i in by_id and
                                        int(h[field]) != by_id[i][f"judge_{field}"]]}
        out["graded"] = n
    return out


# --------------------------------------------------------------------------
# 6. add-document demo
# --------------------------------------------------------------------------

def remove_in_subprocess(source: str) -> None:
    """Remove a document in a fresh process, so no stale handle to the index survives."""
    import subprocess

    subprocess.run([sys.executable, "-c", f"import index; index.remove_document({source!r})"],
                   cwd=ROOT, check=True)


async def add_document_demo(q: dict, redo: bool) -> dict:
    path = EVAL / "add_document_demo.json"
    if path.exists() and not redo:
        return json.loads(path.read_text())
    source = "prohibited_practices_guidelines"
    remove_in_subprocess(source)                                # start from the baseline index
    extra = ix.download_corpus(ix.EXTRA, ix.EXTRA_DIR)[0]
    async with corpus_agent(approve=deny) as agent:
        before = await agent.ask(q["question"])
    async with corpus_agent(approve=lambda p: True) as agent:   # the person approves here
        added = await agent.ask(f"Please add the document at {extra} to the index.")
        after = await agent.ask(q["question"])
    demo = {"question": q["question"], "document": source, "words": ix.load_registry().get(source, {}).get("words"),
            "chunks": ix.load_registry().get(source, {}).get("chunks"),
            "add_trace": added["trace"], "add_answer": added["answer"],
            "before": before["answer"], "before_retrieved": before["retrieved"],
            "after": after["answer"], "after_retrieved": after["retrieved"]}
    # second add of the very same file: nothing should happen
    async with corpus_agent(approve=lambda p: True) as agent:
        again = await agent.ask(f"Please add the document at {extra} to the index.")
    demo["add_again_trace"] = again["trace"]
    save_json(path, demo)
    remove_in_subprocess(source)                                # back to the 3-document baseline
    return demo


# --------------------------------------------------------------------------
# 7. failures
# --------------------------------------------------------------------------

def classify(q: dict, row: dict) -> str | None:
    """Automatic first guess; a person should confirm it (bad test questions need a human)."""
    ok = row["judge_correct"] == 1 and row["judge_supported"] == 1 and row["invalid_citations"] == 0
    if ok:
        return None
    if q["kind"] == "unanswerable":
        return "unsupported claim (answered an unanswerable question)" if row["judge_correct"] == 0 else "unsupported claim"
    if row["refusal_detected"] and not row["has_citation"]:
        return "wrong refusal"
    if not row["expected_retrieved"]:
        return "retrieval miss"
    if row["judge_correct"] == 0:
        return "wrong answer from the right passage"
    return "unsupported claim"


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    keys = list(dict.fromkeys(k for r in rows for k in r))
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=keys)
        w.writeheader()
        w.writerows(rows)


# --------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--fresh", action="store_true", help="ask every question again")
    ap.add_argument("--redo-demo", action="store_true", help="run the add-document demo again")
    args = ap.parse_args()
    EVAL.mkdir(exist_ok=True)
    questions = read_questions()
    log(f"{len(questions)} questions")

    log("\n== 1. Retrieval")
    rows = retrieval_eval(questions)
    for r in rows:
        log(f"   {r['design']:9s} {r['method']:6s} hit@1/3/5 = {r['hit@1']:.2f} {r['hit@3']:.2f} {r['hit@5']:.2f}"
            f"   words in prompt (k=5): {r['words@5']}")
    best = choose_design(rows)
    log(f"   chosen: {best['design']} + {best['method']}")

    log("\n== 2. Agent answers")
    cache = {} if args.fresh else (json.loads((EVAL / "answers.json").read_text())
                                   if (EVAL / "answers.json").exists() else {})
    cache = asyncio.run(run_agent(questions, cache))

    log("\n== 3-4. Code checks and LLM judge")
    results = []
    for q in questions:
        res = cache.get(q["id"])
        if not res:
            continue
        row = {"id": q["id"], "kind": q["kind"], "question": q["question"], "answer": res["answer"],
               "searches": res["searches"], "guardrail": res["guardrail"] or "",
               "tokens_in": res["tokens_in"], "tokens_out": res["tokens_out"], "seconds": res["seconds"]}
        row.update(code_checks(q, res))
        row.update(judge(q, res))
        row["failure"] = classify(q, row) or ""
        results.append(row)
    write_csv(EVAL / "results.csv", results)
    # for grading by hand BEFORE looking at the judge: no verdicts in this file
    write_csv(EVAL / "answers_for_grading.csv",
              [{"id": r["id"], "question": r["question"],
                "reference_answer": next(q["reference_answer"] for q in questions if q["id"] == r["id"]),
                "answer": r["answer"]} for r in results])

    n = len(results)
    unans = [r for r in results if r["kind"] == "unanswerable"]
    ans = [r for r in results if r["kind"] != "unanswerable"]
    summary = {
        "questions": n,
        "retrieval_chosen": {"design": best["design"], "method": best["method"]},
        "correct": sum(r["judge_correct"] == 1 for r in results),
        "supported": sum(r["judge_supported"] == 1 for r in results),
        "unsupported": sum(r["judge_supported"] == 0 or r["invalid_citations"] > 0 for r in results),
        "correct_refusals": sum(r["refusal_ok"] and r["judge_correct"] == 1 for r in unans),
        "unanswerable": len(unans),
        "wrong_refusals": sum(bool(r["wrong_refusal"]) for r in ans),
        "answerable": len(ans),
        "answerable_correct": sum(r["judge_correct"] == 1 for r in ans),
        "invalid_citation_answers": sum(r["invalid_citations"] > 0 for r in results),
        "guardrail_fired": sum(bool(r["guardrail"]) for r in results),
        "mean_tokens_in": round(statistics.mean(r["tokens_in"] for r in results)),
        "mean_tokens_out": round(statistics.mean(r["tokens_out"] for r in results)),
        "mean_seconds": round(statistics.mean(r["seconds"] for r in results), 1),
        "p90_seconds": round(sorted(r["seconds"] for r in results)[int(0.9 * (n - 1))], 1),
        "failures_by_class": {},
        "human_agreement": agreement(results),
    }
    for r in results:
        if r["failure"]:
            summary["failures_by_class"][r["failure"]] = summary["failures_by_class"].get(r["failure"], 0) + 1
    write_csv(EVAL / "failures.csv", [{k: r[k] for k in ("id", "kind", "question", "answer", "failure", "judge_reason")}
                                      for r in results if r["failure"]])

    log("\n== 5. Add-document demo")
    demo_q = next((q for q in questions if q["id"] == DEMO_QUESTION_ID), None)
    if demo_q:
        demo = asyncio.run(add_document_demo(demo_q, args.redo_demo))
        summary["add_document_demo"] = {"question": demo["question"], "chunks_added": demo.get("chunks")}
        log("   before:", demo["before"][:300].replace("\n", " "))
        log("   after: ", demo["after"][:300].replace("\n", " "))

    save_json(EVAL / "summary.json", summary)
    log("\n== Summary")
    log(json.dumps(summary, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
