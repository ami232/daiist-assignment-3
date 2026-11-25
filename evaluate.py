"""Evaluation: (1) retrieval hit rate for each design, (2) end-to-end agent run with code checks + LLM judge,
(3) agreement with your human labels, (4) failure table, (5) add-document before/after experiment.

eval/questions.csv columns: id, question, kind, expected_source, expected_location, reference_answer, addon
  kind              single | multi | unanswerable
  expected_source   doc ids, ';'-separated ("gdpr;ai_act"), empty for unanswerable
  expected_location locations aligned with expected_source ("Article 22;Article 14")
  addon             data_act on the unanswerable questions that the held-out document would answer
eval/human_labels.csv columns: id, correctness (correct|partial|incorrect), supported (yes|no)"""
from __future__ import annotations

import asyncio
import csv
import json
import os
import re
import statistics as st
from pathlib import Path

import hashlib

from config import CHAT_MODEL, DESIGNS, EVAL_DIR, JUDGE_MODEL, NOT_FOUND, get_key, make_llm
from agent import RagAgent, default_approve

Q_PATH = EVAL_DIR / "questions.csv"
ANS_PATH = EVAL_DIR / "answers.jsonl"
KS = (1, 3, 5)


def load_questions() -> list[dict]:
    with open(Q_PATH, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def gold(q: dict) -> set[str]:
    """expected_source and expected_location are ';'-separated and aligned: 'gdpr;ai_act' + 'Article 22;Article 14'."""
    srcs = [x.strip() for x in q["expected_source"].split(";") if x.strip()]
    locs = [x.strip() for x in q["expected_location"].split(";") if x.strip()]
    return {f"{a}:{b}" for a, b in zip(srcs, locs)}


def answerable(q: dict) -> bool:
    return q["kind"].strip().lower() != "unanswerable"


# ------------------------------------------------------------------ 1. retrieval
def retrieval_eval(designs: list[str] | None = None) -> list[dict]:
    from store import collection, retrieve
    qs = [q for q in load_questions() if answerable(q)]
    rows, misses = [], []
    for d in designs or list(DESIGNS):
        if collection(DESIGNS[d][0]).count() == 0:
            print(f"skip {d}: index '{DESIGNS[d][0]}' is empty")
            continue
        res = {k: {"any": [], "all": [], "multi_all": []} for k in KS}
        for q in qs:
            hits = retrieve(q["question"], k=max(KS), design=d)
            g = gold(q)
            for k in KS:
                cov = {f"{h['doc_id']}:{l}" for h in hits[:k] for l in h["locs"]}
                res[k]["any"].append(bool(g & cov))
                res[k]["all"].append(g <= cov)
                if q["kind"].strip().lower() == "multi":
                    res[k]["multi_all"].append(g <= cov)
            if not (g <= {f"{h['doc_id']}:{l}" for h in hits for l in h["locs"]}):
                misses.append(dict(design=d, id=q["id"], gold=q["expected_source"] + " | " + q["expected_location"],
                                   got=" ; ".join(h["citation"] for h in hits)))
        row = dict(design=d, n=len(qs))
        for k in KS:
            row[f"hit@{k}"] = round(st.mean(res[k]["any"]), 3)
            row[f"all@{k}"] = round(st.mean(res[k]["all"]), 3)
            row[f"multi_all@{k}"] = round(st.mean(res[k]["multi_all"]), 3) if res[k]["multi_all"] else ""
        rows.append(row)
    if rows:
        _write_csv(EVAL_DIR / "retrieval_results.csv", rows)
        _write_csv(EVAL_DIR / "retrieval_misses.csv", misses)
        cols = list(rows[0])
        print("| " + " | ".join(cols) + " |\n|" + "---|" * len(cols))
        for r in rows:
            print("| " + " | ".join(str(r[c]) for c in cols) + " |")
        print("\nhit@k = at least one gold passage in top k; all@k = every gold passage in top k.")
    return rows


# ------------------------------------------------------------------ 2. end-to-end
async def run_questions(qs: list[dict], approve=lambda p: False, path: Path = ANS_PATH, fresh: bool = False) -> list[dict]:
    done = {}
    if path.exists() and not fresh:
        recs = [json.loads(l) for l in path.read_text().splitlines() if l.strip()]
        done = {r["id"]: r for r in recs if r.get("guardrail") != "error"}      # never reuse failed calls
    elif path.exists():
        path.unlink()
    out = []
    async with RagAgent(approve) as agent:
        for q in qs:
            if q["id"] in done:
                out.append(done[q["id"]])
                continue
            try:
                for attempt in range(1, 5):                              # transient overloads (503/500): wait and retry
                    try:
                        r = await agent.ask(q["question"])
                        break
                    except Exception as e:                               # noqa: BLE001
                        transient = any(t in str(e) for t in ("503", "UNAVAILABLE", "500 INTERNAL", "overloaded"))
                        if not transient or attempt == 4:
                            raise
                        print(f"{q['id']}: model busy, retry {attempt}/3 in {30 * attempt}s")
                        await asyncio.sleep(30 * attempt)
            except Exception as e:                                     # noqa: BLE001
                if "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e):
                    raise SystemExit(f"\nQuota/rate limit hit at {q['id']}: {str(e)[:300]}\n"
                                     f"Finished answers are saved in {path.name}. Wait for the reset (09:00 Spain), "
                                     f"set LLM_RPM, or use another CHAT_MODEL in .env, then run again.")
                r = dict(question=q["question"], answer=f"ERROR: {e}", refused=False, cited=[], retrieved={},
                         guardrail="error", seconds=0, tokens_in=0, tokens_out=0, searches=0, add_denied=[])
                raise SystemExit(f"\n{q['id']} failed: {str(e)[:200]}\nNothing was scored. Wait a few minutes and run "
                                 f"`main.py evaluate` again; saved answers are reused.")
            r["id"] = q["id"]
            with open(path, "a", encoding="utf-8") as f:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
            print(f"{q['id']}: {'REFUSED' if r['refused'] else 'answered'}  {r['seconds']}s")
            out.append(r)
    return out


def code_checks(q: dict, r: dict) -> dict:
    g, cited = gold(q), set(r["cited"])
    return dict(
        refusal_ok=(r["refused"] if not answerable(q) else not r["refused"]),
        citations_valid=cited <= set(r["retrieved"]),
        has_citation=bool(cited) or r["refused"],
        gold_any=bool(g & cited) if g else None,
        gold_all=(g <= cited) if g else None,
        gold_retrieved=(g <= set(r["retrieved"])) if g else None,
    )


JUDGE_PROMPT = """You grade an answer from a legal-research assistant. Be strict.
QUESTION: {q}
REFERENCE ANSWER (written by the test author from the law): {ref}
PASSAGES THE ASSISTANT CITED:
{passages}
ASSISTANT ANSWER: {a}

Rubric.
correctness: "correct" = every key fact in the reference is stated correctly (numbers, deadlines, amounts exact) and nothing contradicts it;
 "partial" = right direction but a key fact is missing or imprecise; "incorrect" = wrong or contradicts the reference.
supported: true only if EVERY factual claim in the answer is stated in the cited passages above (not just in the reference).
Reply with JSON only: {{"correctness": "...", "supported": true|false, "reason": "<one sentence>"}}"""


def judge(q: dict, r: dict) -> dict:
    """LLM judge. Verdicts are cached in eval/judge_cache.json so a stopped run resumes without repeating calls."""
    cache_path = EVAL_DIR / "judge_cache.json"
    cache = json.loads(cache_path.read_text()) if cache_path.exists() else {}
    key = f"{q['id']}|{hashlib.sha256(r['answer'].encode()).hexdigest()[:10]}"
    if key in cache:
        return cache[key]
    llm = make_llm(JUDGE_MODEL)
    cited = r["cited"] or list(r["retrieved"])[:3]
    passages = "\n\n".join(f"[{c}]\n{r['retrieved'].get(c, '(not retrieved)')[:5000]}" for c in cited)
    msg = JUDGE_PROMPT.format(q=q["question"], ref=q["reference_answer"], passages=passages, a=r["answer"])
    try:
        text = llm.invoke(msg).content
    except Exception as e:                                              # noqa: BLE001
        if "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e):
            raise SystemExit(f"\nJudge hit the quota at {q['id']}. Verdicts so far are cached; set JUDGE_MODEL / "
                             f"LLM_RPM in .env or wait for the reset, then re-run `main.py evaluate`.")
        raise
    text = text if isinstance(text, str) else "".join(b.get("text", "") for b in text)
    m = re.search(r"\{.*\}", text, re.S)
    try:
        verdict = json.loads(m.group(0))
    except Exception:                                                   # noqa: BLE001
        return dict(correctness="error", supported=False, reason=text[:200])
    cache[key] = verdict
    cache_path.write_text(json.dumps(cache, indent=1))
    return verdict


def classify(q: dict, r: dict, c: dict, j: dict | None) -> str:
    """Automatic first guess at the failure category. You review it by hand (bad test question is yours to call)."""
    if r.get("tool_errors"):
        return "tool error (infrastructure, not a model failure)"
    if not answerable(q):
        return "" if r["refused"] else "unsupported claim (answered an unanswerable question)"
    if r["refused"]:
        return "retrieval miss" if not c["gold_retrieved"] else "wrong refusal"
    if not c["citations_valid"]:
        return "unsupported claim (bad citation)"
    if j and j.get("correctness") in ("incorrect", "partial"):
        return "retrieval miss" if not c["gold_retrieved"] else "wrong answer from the right passage"
    if j and j.get("supported") is False:
        return "unsupported claim"
    return ""


def e2e_report(qs: list[dict], results: list[dict]) -> dict:
    by = {r["id"]: r for r in results}
    rows, fails = [], []
    for q in qs:
        r = by.get(q["id"])
        if not r:
            continue
        c = code_checks(q, r)
        j = judge(q, r) if answerable(q) and not r["refused"] else None
        cat = classify(q, r, c, j)
        rows.append(dict(id=q["id"], type=q["kind"], refused=r["refused"], refusal_ok=c["refusal_ok"],
                         citations_valid=c["citations_valid"], has_citation=c["has_citation"], gold_any=c["gold_any"],
                         gold_all=c["gold_all"], judge_correctness=(j or {}).get("correctness", ""),
                         judge_supported=(j or {}).get("supported", ""), judge_reason=(j or {}).get("reason", ""),
                         tool_errors=r.get("tool_errors", 0), seconds=r["seconds"], tokens=r["tokens_in"] + r["tokens_out"], searches=r["searches"],
                         guardrail=r["guardrail"], answer=r["answer"]))
        if cat:
            fails.append(dict(id=q["id"], type=q["kind"], category_auto=cat, category_final="", notes=""))
    _write_csv(EVAL_DIR / "e2e_results.csv", rows)
    _write_csv(EVAL_DIR / "failures.csv", fails)
    _write_csv(EVAL_DIR / "to_label.csv", [dict(id=q["id"], question=q["question"], reference=q["reference_answer"],
               answer=by[q["id"]]["answer"], cited=" ".join(by[q["id"]]["cited"]), correctness="", supported="")
               for q in qs if q["id"] in by and answerable(q) and not by[q["id"]]["refused"]])
    A = [r for r in rows if r["type"] != "unanswerable"]
    U = [r for r in rows if r["type"] == "unanswerable"]
    ok = lambda xs, f: round(sum(map(f, xs)) / len(xs), 3) if xs else None          # noqa: E731
    summ = dict(
        n=len(rows), answerable=len(A), unanswerable=len(U),
        correct_rate=ok(A, lambda r: r["judge_correctness"] == "correct"),
        correct_or_partial=ok(A, lambda r: r["judge_correctness"] in ("correct", "partial")),
        wrong_refusal_rate=ok(A, lambda r: r["refused"]),
        unsupported_rate=ok([r for r in A if not r["refused"]], lambda r: r["judge_supported"] is False),
        correct_refusal_rate=ok(U, lambda r: r["refused"]),
        hallucination_rate_on_unanswerable=ok(U, lambda r: not r["refused"]),
        citations_valid_rate=ok(rows, lambda r: r["citations_valid"]),
        gold_cited_rate=ok(A, lambda r: bool(r["gold_any"])),
        guardrail_triggered=sum(1 for r in rows if r["guardrail"]),
        mean_seconds=round(st.mean(r["seconds"] for r in rows), 1) if rows else None,
        mean_tokens=round(st.mean(r["tokens"] for r in rows)) if rows else None,
        total_tokens=sum(r["tokens"] for r in rows),
    )
    summ["human_agreement"] = human_agreement(rows)
    (EVAL_DIR / "summary.json").write_text(json.dumps(summ, indent=2))
    print(json.dumps(summ, indent=2))
    return summ


def human_agreement(rows: list[dict]) -> dict:
    p = EVAL_DIR / "human_labels.csv"
    if not p.exists():
        return {"note": "eval/human_labels.csv missing: label 20+ answers from eval/to_label.csv"}
    with open(p, newline="", encoding="utf-8") as f:
        hl = {r["id"]: r for r in csv.DictReader(f) if r.get("correctness")}
    pairs = [(hl[r["id"]], r) for r in rows if r["id"] in hl and r["judge_correctness"]]
    if not pairs:
        return {"note": "no overlap between human_labels.csv and judged answers"}
    yes = lambda v: str(v).strip().lower() in ("yes", "true", "1")                  # noqa: E731
    return dict(n=len(pairs),
                correctness_agreement=round(sum(h["correctness"].strip() == r["judge_correctness"] for h, r in pairs) / len(pairs), 3),
                supported_agreement=round(sum(yes(h.get("supported")) == bool(r["judge_supported"]) for h, r in pairs) / len(pairs), 3),
                disagreements=[r["id"] for h, r in pairs if h["correctness"].strip() != r["judge_correctness"]])


# ------------------------------------------------------------------ 5. add-document before/after
async def addon_experiment(path: str, auto_approve: bool = False) -> None:
    qs = [q for q in load_questions() if (q.get("addon") or "").strip()]
    if not qs:
        print("no 'unanswerable_addon' questions in questions.csv")
        return
    before = await run_questions(qs, path=EVAL_DIR / "addon_before.jsonl", fresh=True)
    approve = (lambda p: True) if auto_approve else default_approve
    async with RagAgent(approve) as a:
        msg = await a.ask(f"Please add the document at {path} to the index.")
    print("add_document via agent:", msg["answer"], "| denied:", msg["add_denied"])
    after = await run_questions(qs, path=EVAL_DIR / "addon_after.jsonl", fresh=True)
    out = [dict(id=q["id"], question=q["question"], before=b["answer"], after=a_["answer"],
                before_refused=b["refused"], after_refused=a_["refused"], after_cited=a_["cited"])
           for q, b, a_ in zip(qs, before, after)]
    (EVAL_DIR / "addon_before_after.json").write_text(json.dumps(out, indent=2, ensure_ascii=False))
    for o in out:
        print(f"\n{o['id']}: {o['question']}\n  BEFORE: {o['before']}\n  AFTER:  {o['after']}")


def _write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(exist_ok=True)
    if not rows:
        path.write_text("")
        return
    with open(path, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    import argparse
    ap = argparse.ArgumentParser(description="`main.py evaluate` runs this with no arguments: retrieval + end to end.")
    ap.add_argument("--retrieval-only", action="store_true")
    ap.add_argument("--e2e-only", action="store_true")
    ap.add_argument("--limit", type=int)
    ap.add_argument("--fresh", action="store_true", help="ignore saved answers and re-run the agent")
    ap.add_argument("--addon", help="add-on document for the before/after experiment, e.g. addon/data_act.html")
    ap.add_argument("--approve", action="store_true", help="auto-approve add_document in the experiment")
    run(ap.parse_args())


def run(args) -> None:
    if args.addon:
        asyncio.run(addon_experiment(args.addon, args.approve))
        return
    if not args.e2e_only:
        retrieval_eval()
    if args.retrieval_only:
        return
    qs = load_questions()[: args.limit] if args.limit else load_questions()
    # add-on questions must be refused while the add-on is not indexed, so they stay in the main run
    results = asyncio.run(run_questions(qs, fresh=args.fresh))
    e2e_report(qs, results)


if __name__ == "__main__":
    main()
