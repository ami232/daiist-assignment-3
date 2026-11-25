"""
Assignment 3: evaluation (`uv run python main.py evaluate`).

1. Retrieval: hit rate at k = 1, 3, 5 for three search designs on the answerable questions.
2. End to end: the agent (agent.py, same harness as `main.py ask`) answers every question.
3. Code checks: refusal detection, citations returned by search, expected document cited,
   expected passage retrieved during the run.
4. LLM judge (rubric below) grades correctness and support against the retrieved text.
5. Agreement between the judge and my own grades in eval/human_labels.csv.
6. Failure causes, cost (tokens, seconds) per question.
7. Add-document demo: an unanswerable question before and after adding Regulation (EU) 2020/639.

Every step caches its results in eval/ and resumes where it stopped, so a crash or a rate limit never
repeats paid calls. The base evaluation hides documents added later (CORPUS_EXCLUDE_ADDED), so it stays
reproducible after the demo has added a document.
"""

from __future__ import annotations

import csv
import json
import os
import re
import time
from pathlib import Path

os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")

import rag  # noqa: E402

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
ANSWERS = EVAL / "answers.jsonl"
VERDICTS = EVAL / "judge_verdicts.jsonl"
HUMAN = EVAL / "human_labels.csv"
KS = (1, 3, 5)

JUDGE_RUBRIC = """You grade answers of a drone-regulation assistant. You get the QUESTION, the REFERENCE answer
written by the test author, the ANSWER to grade and the EVIDENCE (the passages the assistant retrieved).

correct = 1 if the ANSWER gives the same essential facts as the REFERENCE (numbers, limits, conditions,
yes/no) with nothing that contradicts it. Extra correct detail is fine. Missing the key fact, a wrong number
or a wrong yes/no makes it 0. If the REFERENCE says the corpus does not cover the question, correct = 1 only
if the ANSWER declines to answer.
supported = 1 if every factual claim in the ANSWER can be found in the EVIDENCE (paraphrase is fine). Any
claim not in the EVIDENCE, even if true in the real world, makes it 0. A pure refusal is supported = 1.

Reply with JSON only: {"correct": 0 or 1, "supported": 0 or 1, "reason": "<one sentence>"}"""


# ----------------------------------------------------------------------------- helpers
def read_questions() -> list[dict]:
    with QUESTIONS.open(encoding="utf-8", newline="") as f:
        return [r for r in csv.DictReader(f) if r["question"].strip()]


def read_jsonl(path: Path) -> dict[str, dict]:
    out = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            try:
                row = json.loads(line)
                out[row["id"]] = row
            except (json.JSONDecodeError, KeyError):
                continue  # a line cut by an interrupted run
    return out


def append_jsonl(path: Path, row: dict) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def expected_pairs(q: dict) -> list[tuple[str, str]]:
    if not q["expected_source"].strip():
        return []
    return list(zip(q["expected_source"].split(";"), q["expected_location"].split(";")))


def loc_match(covers: str, expected: str) -> bool:
    """`expected` (e.g. 'Article 4', 'Annex, UAS.OPEN.030') matches a covered location exactly or as a
    prefix followed by a non-digit, so 'Article 4' does not match 'Article 40'."""
    for c in covers.split("; "):
        if c == expected or (c.startswith(expected) and not c[len(expected)].isdigit()):
            return True
    return False


def chunk_hits(chunk: dict, pairs: list[tuple[str, str]]) -> set[int]:
    return {i for i, (s, l) in enumerate(pairs)
            if chunk.get("source") == s and loc_match(chunk.get("covers") or chunk.get("location", ""), l)}


# ----------------------------------------------------------------------------- 1. retrieval
def retrieval_eval(questions: list[dict]) -> dict:
    rows, summary = [], {}
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    for design in rag.SEARCH_DESIGNS:
        hits_all = {k: 0 for k in KS}
        hits_any = {k: 0 for k in KS}
        words = []
        for q in answerable:
            pairs = expected_pairs(q)
            res = rag.search(q["question"], design, k=max(KS), exclude_added=True)
            words.append(sum(len(r["text"].split()) for r in res))
            first_rank = None
            for k in KS:
                found = set().union(*[chunk_hits(r, pairs) for r in res[:k]]) if res else set()
                ok_all = len(found) == len(pairs) if q["kind"] == "multi" else bool(found)
                hits_all[k] += ok_all
                hits_any[k] += bool(found)
                if ok_all and first_rank is None:
                    first_rank = k
            rows.append({"design": design, "id": q["id"], "kind": q["kind"],
                         **{f"hit@{k}": int(bool(set().union(*[chunk_hits(r, pairs) for r in res[:k]])) if q["kind"] != "multi"
                                            else len(set().union(*[chunk_hits(r, pairs) for r in res[:k]])) == len(pairs))
                            for k in KS},
                         "top_ids": " ".join(r["id"] for r in res)})
        n = len(answerable)
        summary[design] = {**{f"hit@{k}": round(hits_all[k] / n, 3) for k in KS},
                           **{f"any@{k}": round(hits_any[k] / n, 3) for k in KS},
                           "multi_hit@5": round(sum(r["hit@5"] for r in rows if r["design"] == design and r["kind"] == "multi")
                                                / max(1, sum(q["kind"] == "multi" for q in answerable)), 3),
                           "mean_words_added_k5": round(sum(words) / len(words), 1), "n": n}
    with (EVAL / "retrieval_results.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    best = max(summary, key=lambda d: (summary[d]["hit@5"], summary[d]["hit@3"], summary[d]["hit@1"]))
    summary["_best_by_numbers"] = best
    summary["_active_design"] = rag.ACTIVE_DESIGN
    (EVAL / "retrieval_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("Retrieval (hit rate; multi = both passages):")
    for d, s in summary.items():
        if not d.startswith("_"):
            print(f"  {d:18s} @1 {s['hit@1']:.2f}  @3 {s['hit@3']:.2f}  @5 {s['hit@5']:.2f}  "
                  f"words added (k=5) {s['mean_words_added_k5']}")
    print(f"  best by the numbers: {best}; active design in rag.py: {rag.ACTIVE_DESIGN}")
    return summary


# ----------------------------------------------------------------------------- 2. answers
def answer_all(questions: list[dict], batch: int = 6) -> dict[str, dict]:
    from agent import run_batch

    done = read_jsonl(ANSWERS)
    todo = [q for q in questions if q["id"] not in done]
    if todo:
        print(f"Agent answering {len(todo)} question(s) ({len(done)} cached) ...", flush=True)
    for i in range(0, len(todo), batch):
        part = todo[i:i + batch]
        for q, r in zip(part, run_batch([q["question"] for q in part], exclude_added=True)):
            row = {"id": q["id"], **{k: v for k, v in r.items() if k != "retrieved"},
                   "retrieved": {k: list(v) for k, v in r["retrieved"].items()}}
            append_jsonl(ANSWERS, row)
            done[q["id"]] = row
            print(f"  {q['id']}: {'REFUSED' if r['refused'] else 'answered'}"
                  f"{' [guardrail]' if r['guardrail'] else ''} ({r['seconds']}s)", flush=True)
    return done


# ----------------------------------------------------------------------------- 3-4. checks + judge
def evidence_text(ans: dict) -> str:
    seen, parts = set(), []
    for t in ans["trace"]:
        if t["tool"] == "search":
            for block in t["result"].split("\n\n---\n\n"):
                head = block.split("\n", 1)[0]
                if head not in seen:
                    seen.add(head)
                    parts.append(block)
    return "\n\n".join(parts)[:24000]


def judge(q: dict, ans: dict) -> dict:
    from google.genai import types

    prompt = (f"{JUDGE_RUBRIC}\n\nQUESTION: {q['question']}\nREFERENCE: {q['reference_answer']}\n"
              f"ANSWER: {ans['answer']}\nEVIDENCE:\n{evidence_text(ans) or '(nothing retrieved)'}")
    model = rag.JUDGE_MODEL
    for attempt in range(8):
        try:
            started = time.time()
            r = rag.client().models.generate_content(
                model=model, contents=prompt,
                config=types.GenerateContentConfig(temperature=0, response_mime_type="application/json",
                                                   thinking_config=types.ThinkingConfig(thinking_level="low")))
            v = json.loads(re.search(r"\{.*\}", r.text, re.S).group(0))
            u = r.usage_metadata
            return {"correct": int(v["correct"]), "supported": int(v["supported"]), "reason": v.get("reason", ""),
                    "judge_model": model,
                    "judge_tokens": (u.total_token_count or 0) if u else 0, "judge_seconds": round(time.time() - started, 2)}
        except Exception as e:  # noqa: BLE001 - retry rate limits and malformed JSON
            if "429" in str(e) and model != rag.JUDGE_FALLBACK and attempt >= 1:
                model = rag.JUDGE_FALLBACK  # daily quota of the main judge exhausted
            wait = 10 * (attempt + 1)
            print(f"  judge retry {attempt + 1} for {q['id']}: {str(e)[:120]} (waiting {wait}s)", flush=True)
            time.sleep(wait)
    raise RuntimeError(f"judge failed for {q['id']}")


def code_checks(q: dict, ans: dict) -> dict:
    pairs = expected_pairs(q)
    retrieved_meta = [{"source": s, "covers": l} for s, l in ans["retrieved"].values()]
    found = set().union(*[chunk_hits(c, pairs) for c in retrieved_meta]) if retrieved_meta and pairs else set()
    cited_sources = {ans["retrieved"][c][0] for c in ans["cited"] if c in ans["retrieved"]}
    return {
        "refused": int(ans["refused"]),
        "citations_valid": int(all(c in ans["retrieved"] for c in ans["cited"])),
        "has_citation": int(bool(ans["cited"])),
        "expected_passage_retrieved": (int(len(found) == len(pairs)) if pairs else None),
        "expected_doc_cited": (int(bool({s for s, _ in pairs} & cited_sources)) if pairs else None),
        "guardrail_fired": int(bool(ans["guardrail"])),
    }


def grade_all(questions: list[dict], answers: dict[str, dict]) -> list[dict]:
    verdicts = read_jsonl(VERDICTS)
    rows = []
    for q in questions:
        ans = answers[q["id"]]
        cc = code_checks(q, ans)
        if q["id"] not in verdicts:
            v = judge(q, ans)
            verdicts[q["id"]] = {"id": q["id"], **v}
            append_jsonl(VERDICTS, verdicts[q["id"]])
            print(f"  judged {q['id']}: correct={v['correct']} supported={v['supported']}", flush=True)
        v = verdicts[q["id"]]
        unans = q["kind"] == "unanswerable"
        # Code decides what code can decide; the judge decides correctness/support of real answers.
        if unans:
            if cc["refused"]:
                # A refusal that still adds facts not in the evidence is a failure for this use case.
                outcome = "correct_refusal" if v["supported"] else "refusal_with_unsupported_claim"
            else:
                outcome = "unsupported" if not v["supported"] else "answered_unanswerable"
        elif cc["refused"]:
            outcome = "wrong_refusal"
        elif not v["supported"]:
            outcome = "unsupported"
        else:
            outcome = "correct" if v["correct"] else "wrong_answer"
        cause = ""
        if outcome == "wrong_refusal" or outcome in ("wrong_answer", "unsupported") and not unans:
            if cc["expected_passage_retrieved"] == 0:
                cause = "retrieval miss"
            elif outcome == "wrong_refusal":
                cause = "wrong refusal"
            elif outcome == "unsupported":
                cause = "unsupported claim"
            else:
                cause = "wrong answer from the right passage"
        elif unans and outcome != "correct_refusal":
            cause = ("unsupported claim" if outcome in ("unsupported", "refusal_with_unsupported_claim")
                     else "answered an unanswerable question")
        rows.append({"id": q["id"], "kind": q["kind"], "outcome": outcome, "auto_cause": cause, **cc,
                     "judge_correct": v["correct"], "judge_supported": v["supported"], "judge_reason": v["reason"],
                     "seconds": ans["seconds"], "tokens": ans["tokens_in"] + ans["tokens_out"],
                     "model_calls": ans["model_calls"], "searches": sum(t["tool"] == "search" for t in ans["trace"]),
                     "judge_tokens": v.get("judge_tokens", 0), "answer": ans["answer"]})
    with (EVAL / "results.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    return rows


# ----------------------------------------------------------------------------- 5. human agreement
def agreement(rows: list[dict]) -> dict:
    if not HUMAN.exists():
        return {"n": 0}
    with HUMAN.open(encoding="utf-8", newline="") as f:
        human = {r["id"].strip(): r for r in csv.DictReader(f) if (r.get("id") or "").strip()}
    by_id = {r["id"]: r for r in rows}
    out = {"n": 0}
    for field, jf in (("correct", "judge_correct"), ("supported", "judge_supported")):
        pairs = []
        for i, h in human.items():
            if i in by_id and str(h.get(field, "")).strip() in {"0", "1"}:
                r = by_id[i]
                judge_val = r[jf]
                if field == "correct" and r["kind"] == "unanswerable":
                    judge_val = int(r["refused"])  # correctness of an unanswerable = it refused (code check)
                if field == "correct" and r["outcome"] == "wrong_refusal":
                    judge_val = 0
                pairs.append((int(h[field]), int(judge_val)))
        if not pairs:
            continue
        n = len(pairs)
        agree = sum(a == b for a, b in pairs) / n
        pa = sum(a for a, _ in pairs) / n
        pb = sum(b for _, b in pairs) / n
        pe = pa * pb + (1 - pa) * (1 - pb)
        kappa = (agree - pe) / (1 - pe) if pe < 1 else 1.0
        out[field] = {"n": n, "agreement": round(agree, 3), "cohen_kappa": round(kappa, 3),
                      "disagreements": [i for i in human if i in by_id and str(human[i].get(field, "")).strip() in {"0", "1"}
                                        and int(human[i][field]) != (int(by_id[i]["refused"]) if field == "correct" and by_id[i]["kind"] == "unanswerable"
                                                                     else 0 if field == "correct" and by_id[i]["outcome"] == "wrong_refusal" else int(by_id[i][jf]))]}
        out["n"] = max(out["n"], n)
    return out


# ----------------------------------------------------------------------------- 7. add-document demo
DEMO_QUESTION_ID = "u01"


def add_document_demo(questions: list[dict], answers: dict[str, dict]) -> dict:
    out_path = EVAL / "add_document_demo.json"
    if out_path.exists():
        return json.loads(out_path.read_text(encoding="utf-8"))
    import asyncio

    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    from agent import run_agent
    from index import LATER_DOCUMENT, download

    q = next(x for x in questions if x["id"] == DEMO_QUESTION_ID)
    before = answers[q["id"]]
    path = download(LATER_DOCUMENT)

    async def call_add(p: str) -> list[str]:
        params = StdioServerParameters(command=os.sys.executable, args=[str(ROOT / "server.py")], cwd=str(ROOT))
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as s:
                await s.initialize()
                first = await s.call_tool("add_document", {"path": p})
                again = await s.call_tool("add_document", {"path": p})
                return ["\n".join(getattr(c, "text", "") for c in r.content) for r in (first, again)]

    rel = str(path.relative_to(ROOT))
    first, again = asyncio.run(call_add(rel))
    after = run_agent(q["question"], exclude_added=False)
    demo = {"question_id": q["id"], "question": q["question"], "document": LATER_DOCUMENT["source"],
            "path": rel, "before": before["answer"], "add_document_result": first,
            "add_document_again": again, "after": after["answer"], "after_cited": after["cited"],
            "after_sources": {c: after["retrieved"][c] for c in after["cited"]}}
    out_path.write_text(json.dumps(demo, indent=2, ensure_ascii=False), encoding="utf-8")
    return demo


# ----------------------------------------------------------------------------- main
def main() -> None:
    questions = read_questions()
    retrieval = retrieval_eval(questions)
    answers = answer_all(questions)
    rows = grade_all(questions, answers)

    counts: dict[str, int] = {}
    for r in rows:
        counts[r["outcome"]] = counts.get(r["outcome"], 0) + 1
    answerable = [r for r in rows if r["kind"] != "unanswerable"]
    unans = [r for r in rows if r["kind"] == "unanswerable"]
    failures = [r for r in rows if r["outcome"] not in ("correct", "correct_refusal")]
    causes: dict[str, int] = {}
    for r in failures:
        causes[r["auto_cause"]] = causes.get(r["auto_cause"], 0) + 1
    n = len(rows)
    summary = {
        "n_questions": n, "outcomes": counts,
        "answerable": {"n": len(answerable), "correct": sum(r["outcome"] == "correct" for r in answerable),
                       "wrong_answer": sum(r["outcome"] == "wrong_answer" for r in answerable),
                       "unsupported": sum(r["outcome"] == "unsupported" for r in answerable),
                       "wrong_refusal": sum(r["outcome"] == "wrong_refusal" for r in answerable)},
        "unanswerable": {"n": len(unans), "correct_refusal": sum(r["outcome"] == "correct_refusal" for r in unans)},
        "by_kind": {k: {"n": sum(r["kind"] == k for r in rows),
                        "ok": sum(r["kind"] == k and r["outcome"] in ("correct", "correct_refusal") for r in rows)}
                    for k in ("single", "multi", "unanswerable")},
        "code_checks": {"citations_valid_rate": round(sum(r["citations_valid"] for r in rows) / n, 3),
                        "guardrail_fired": sum(r["guardrail_fired"] for r in rows),
                        "expected_passage_retrieved_rate": round(sum(r["expected_passage_retrieved"] or 0 for r in answerable) / len(answerable), 3),
                        "expected_doc_cited_rate_when_answered": round(
                            sum(r["expected_doc_cited"] or 0 for r in answerable if not r["refused"])
                            / max(1, sum(not r["refused"] for r in answerable)), 3)},
        "failure_causes_auto": causes,
        "cost": {"mean_tokens": round(sum(r["tokens"] for r in rows) / n), "mean_seconds": round(sum(r["seconds"] for r in rows) / n, 2),
                 "median_seconds": sorted(r["seconds"] for r in rows)[n // 2],
                 "mean_model_calls": round(sum(r["model_calls"] for r in rows) / n, 2),
                 "mean_searches": round(sum(r["searches"] for r in rows) / n, 2),
                 "mean_judge_tokens": round(sum(r["judge_tokens"] for r in rows) / n),
                 "mean_tokens_in": round(sum(a["tokens_in"] for a in answers.values()) / n),
                 "mean_tokens_out": round(sum(a["tokens_out"] for a in answers.values()) / n),
                 # Paid-tier list price of Gemini 3.1 Flash-Lite (USD per 1M tokens: 0.25 in, 1.50 out),
                 # ai.google.dev/gemini-api/docs/pricing; the free tier used here costs nothing.
                 "est_usd_per_question_paid": round(sum(a["tokens_in"] * 0.25e-6 + a["tokens_out"] * 1.5e-6
                                                        for a in answers.values()) / n, 5)},
        "judge_human_agreement": agreement(rows),
        "retrieval": {k: v for k, v in retrieval.items()},
        "models": {"agent": rag.AGENT_MODEL, "judge": rag.JUDGE_MODEL, "embeddings": rag.EMBED_MODEL},
    }
    summary["add_document_demo"] = add_document_demo(questions, answers)
    (EVAL / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({k: summary[k] for k in ("outcomes", "answerable", "unanswerable", "code_checks",
                                              "failure_causes_auto", "cost", "judge_human_agreement")}, indent=2))
    print(f"\nAdd-document demo ({summary['add_document_demo']['question_id']}):\n  before: "
          f"{summary['add_document_demo']['before'][:160]}\n  after : {summary['add_document_demo']['after'][:300]}")


if __name__ == "__main__":
    main()
