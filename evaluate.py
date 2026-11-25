"""
Assignment 3: evaluation (`uv run python main.py evaluate`).

Stages (each one saves its output in eval/ and is skipped if already done, so a rerun after a quota
error continues instead of starting again; delete the file to redo a stage):

  1. retrieval   hit rate at k=1/3/5 for 2 designs x 3 rankings (eval/retrieval_summary.csv)
  2. answers     the agent answers every question (eval/answers.jsonl)
  3. checks      code checks: citations valid, citations point at the expected page, refusals right
  4. judge       an LLM judge (a different model from the agent) grades each answer with a rubric
  5. report      eval/results.csv, eval/summary.json, eval/to_grade.csv for my own blind grading,
                 and agreement between my grades (eval/human_labels.csv) and the judge

Other commands:
  python evaluate.py --retrieval-only       only stage 1 (no agent, no judge)
  python evaluate.py --demo PATH QID        add document PATH, ask question QID before and after
"""

from __future__ import annotations

import asyncio
import csv
import json
import os
import random
import re
import sys
import time
from pathlib import Path

import agent as agent_mod
import index
import retrieval

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
QVECS = EVAL / "query_vectors.json"
ANSWERS = EVAL / "answers.jsonl"
JUDGED = EVAL / "judge.jsonl"
JUDGE_MODEL = os.getenv("GEMINI_JUDGE_MODEL", "gemini-3.8-flash")
KS = (1, 3, 5)
TO_GRADE = 24  # how many answers I grade by hand (the assignment asks for 20+)

RUBRIC = """You are a strict grader of answers from a retrieval assistant about EBA credit-risk guidelines.
You get: the QUESTION, the REFERENCE answer written by a human who read the documents, the EVIDENCE (the passages
the assistant retrieved) and the ANSWER to grade.

Score two things, each 1 or 0.

correct = 1 only if the ANSWER states the key facts of the REFERENCE (numbers, thresholds, dates, conditions) and
contradicts nothing in it. Missing a key fact, or adding a wrong one, is 0. If the REFERENCE says the corpus does not
cover the question, correct = 1 only if the ANSWER refuses (it starts with NOT COVERED) and does not state a rule.
Different wording is fine. Extra true detail is fine.

supported = 1 only if every factual claim in the ANSWER can be found in the EVIDENCE. A claim that is true in the real
world but not in the EVIDENCE counts as 0. A refusal is supported = 1.

Reply with JSON only: {"correct": 0 or 1, "supported": 0 or 1, "reason": "one sentence"}"""


# ------------------------------------------------------------------------------------------------
def read_questions() -> list[dict]:
    with open(QUESTIONS, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def expected_spans(q: dict) -> list[tuple[str, int, int]]:
    """expected_location -> [(source, first page, last page)]. Single questions write 'p. 22';
    multi questions write 'SOURCE: p. 22; SOURCE: p. 51'."""
    sources = [s.strip() for s in q["expected_source"].split(";") if s.strip()]
    spans = []
    for part in q["expected_location"].split(";"):
        part = part.strip()
        if not part:
            continue
        m = re.search(r"p\.\s*(\d+)(?:\s*-\s*(\d+))?", part)
        if not m:
            continue
        src = part.split(":")[0].strip() if ":" in part else sources[0]
        a = int(m.group(1))
        spans.append((src, a, int(m.group(2) or a)))
    return spans


def read_jsonl(path: Path) -> dict[str, dict]:
    out: dict[str, dict] = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                out[r["id"]] = r
    return out


def append_jsonl(path: Path, row: dict) -> None:
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


# ------------------------------------------------------------------------------------------------
# 1. retrieval hit rate
def query_vectors(questions: list[dict]) -> dict[str, list[float]]:
    cache = json.loads(QVECS.read_text()) if QVECS.exists() else {}
    todo = [q["question"] for q in questions if q["question"] not in cache]
    for i in range(0, len(todo), index.EMBED_BATCH):
        batch = todo[i:i + index.EMBED_BATCH]
        vecs = index.embed_batch([f"task: search result | query: {t}" for t in batch])
        cache.update(dict(zip(batch, vecs)))
        QVECS.write_text(json.dumps(cache))
    return cache


def hit_rates(questions: list[dict]) -> list[dict]:
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    qvecs = query_vectors(answerable)
    rows = []
    for design in index.DESIGNS:
        r = retrieval.Retriever(design, require_vectors=False)
        modes = retrieval.MODES
        if r.not_embedded:
            modes = ("bm25",)  # dense and hybrid would be unfair with missing vectors
            print(f"  note: {r.not_embedded} of {len(r.chunks)} '{design}' chunks have no vector yet, so only bm25 is "
                  f"evaluated for it (run main.py index when quota is back, then evaluate again)", file=sys.stderr)
        for mode in modes:
            for kind in ("single", "multi"):
                qs = [q for q in answerable if q["kind"] == kind]
                for k in KS:
                    any_hit = all_hit = 0
                    for q in qs:
                        spans = expected_spans(q)
                        hits = r.search(q["question"], k=k, mode=mode, qvec=qvecs[q["question"]])
                        found = [any(retrieval.page_overlap(h, s, a, b) for h in hits) for s, a, b in spans]
                        any_hit += any(found)
                        all_hit += all(found)
                    rows.append({"design": design, "mode": mode, "kind": kind, "k": k, "n": len(qs),
                                 "any_hit_rate": round(any_hit / len(qs), 3), "all_hit_rate": round(all_hit / len(qs), 3)})
    return rows


def print_retrieval(rows: list[dict]) -> None:
    print("\nHit rate (single questions: the expected page is in the top k; multi: ALL expected pages are in the top k)")
    print(f"{'design':10} {'mode':7} " + " ".join(f"{'single@' + str(k):>9}" for k in KS) + "   " + " ".join(f"{'multi-all@' + str(k):>11}" for k in KS))
    for design in index.DESIGNS:
        for mode in retrieval.MODES:
            if not any(r["design"] == design and r["mode"] == mode for r in rows):
                continue

            def val(kind, k, col):
                return next(r[col] for r in rows if (r["design"], r["mode"], r["kind"], r["k"]) == (design, mode, kind, k))
            print(f"{design:10} {mode:7} " + " ".join(f"{val('single', k, 'any_hit_rate'):9.2f}" for k in KS) + "   "
                  + " ".join(f"{val('multi', k, 'all_hit_rate'):11.2f}" for k in KS))


def stage_retrieval(questions: list[dict]) -> None:
    rows = hit_rates(questions)
    with open(EVAL / "retrieval_summary.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    print_retrieval(rows)
    print(f"\nServing choice in the code: design={index.SERVING_DESIGN}, mode={retrieval.SERVING_MODE}")


# ------------------------------------------------------------------------------------------------
# 2. answers
async def stage_answers(questions: list[dict]) -> None:
    # an answer that failed (for example a 429 per-minute limit) is not an answer: drop it so it is asked again
    done = read_jsonl(ANSWERS)
    failed = {i for i, r in done.items() if r.get("error")}
    if failed:
        ANSWERS.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for i, r in done.items() if i not in failed), encoding="utf-8")
        judged = read_jsonl(JUDGED)
        if judged:
            JUDGED.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for i, r in judged.items() if i not in failed), encoding="utf-8")
        print(f"\nDropped {len(failed)} failed answers ({', '.join(sorted(failed))}); they will be asked again.")
        done = {i: r for i, r in done.items() if i not in failed}
    todo = [q for q in questions if q["id"] not in done]
    if not todo:
        return
    print(f"\nAsking the agent {len(todo)} questions ({len(done)} already answered) ...")
    async with agent_mod.CorpusAgent(approve=lambda name, args: False) as ag:  # evaluation never changes the index
        for q in todo:
            for attempt in range(4):
                res = await ag.ask(q["question"])
                if not res.error or not any(s in res.error for s in ("429", "RESOURCE_EXHAUSTED", "RateLimit", "503", "UNAVAILABLE")):
                    break
                print(f"  {q['id']} rate limit, waiting 65s (attempt {attempt + 1}/4) ...", file=sys.stderr, flush=True)
                await asyncio.sleep(65)
            if res.error:
                print(f"  {q['id']} FAILED: {res.error[:100]} (not saved; run again)")
                continue
            append_jsonl(ANSWERS, {
                "id": q["id"], "answer": res.answer, "raw_answer": res.raw_answer, "guardrail": res.guardrail,
                "guardrail_detail": res.guardrail_detail, "error": res.error, "retrieved": res.retrieved,
                "evidence": res.evidence, "searches": [c["args"].get("query", "") for c in res.tool_calls if c["name"] == "search"],
                "input_tokens": res.input_tokens, "output_tokens": res.output_tokens, "seconds": round(res.seconds, 2),
            })
            print(f"  {q['id']} {res.seconds:5.1f}s {'REFUSED' if res.refused else 'answered'}")
            await asyncio.sleep(4)  # stay under the per-minute limit


# 3. code checks
def code_checks(q: dict, a: dict) -> dict:
    refused = a["answer"].strip().upper().startswith(agent_mod.REFUSAL_PREFIX)
    retrieved = [tuple(x) for x in a["retrieved"]]
    ok_cit, problem = agent_mod.check_citations(a["answer"], retrieved)
    spans = expected_spans(q)
    cited = [(m.group(1), int(m.group(2)), int(m.group(3) or m.group(2))) for m in agent_mod.CITATION.finditer(a["answer"])]
    cites_expected = bool(spans) and any(s == cs and x <= cb and ca <= y for s, x, y in spans for cs, ca, cb in cited)
    retrieved_expected = bool(spans) and any(s == rs and x <= rb and ra <= y for s, x, y in spans for rs, ra, rb in retrieved)
    unanswerable = q["kind"] == "unanswerable"
    return {
        "refused": refused,
        "refusal_ok": refused if unanswerable else not refused,
        "citations_valid": ok_cit,
        "citation_problem": problem,
        "cites_expected_page": cites_expected if not unanswerable else "",
        "retrieved_expected_page": retrieved_expected if not unanswerable else "",
    }


# 4. judge
def judge_one(llm, q: dict, a: dict) -> dict:
    prompt = (f"{RUBRIC}\n\nQUESTION: {q['question']}\n\nREFERENCE: {q['reference_answer']}\n\n"
              f"EVIDENCE:\n{a['evidence'][:12000] or '(no passages retrieved)'}\n\nANSWER: {a['answer']}")
    reply = None
    for attempt in range(8):  # 503 "high demand" is temporary: wait and try again
        try:
            reply = llm.invoke(prompt)
            break
        except Exception as error:  # noqa: BLE001
            if attempt == 7 or not any(s in str(error) for s in ("503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED", "500")):
                raise
            wait = min(15 * (attempt + 1), 90)
            print(f"    judge model busy, waiting {wait}s ...", file=sys.stderr, flush=True)
            time.sleep(wait)
    text = reply.content if isinstance(reply.content, str) else "".join(p.get("text", "") if isinstance(p, dict) else str(p) for p in reply.content)
    m = re.search(r"\{.*\}", text, re.S)
    try:
        data = json.loads(m.group(0))
        return {"correct": int(data["correct"]), "supported": int(data["supported"]), "reason": str(data.get("reason", ""))[:300]}
    except Exception:  # noqa: BLE001
        return {"correct": -1, "supported": -1, "reason": "judge reply could not be parsed: " + text[:150]}


def stage_judge(questions: list[dict]) -> None:
    answers, done = read_jsonl(ANSWERS), read_jsonl(JUDGED)
    todo = [q for q in questions if q["id"] in answers and q["id"] not in done]
    if not todo:
        return
    from api_key import load_api_key
    from langchain_google_genai import ChatGoogleGenerativeAI

    print(f"\nJudging {len(todo)} answers with {JUDGE_MODEL} (the agent uses {agent_mod.AGENT_MODEL}) ...")
    llm = ChatGoogleGenerativeAI(model=JUDGE_MODEL, temperature=0, google_api_key=load_api_key(), max_retries=3)
    for q in todo:
        v = judge_one(llm, q, answers[q["id"]])
        append_jsonl(JUDGED, {"id": q["id"], **v})
        print(f"  {q['id']} correct={v['correct']} supported={v['supported']}")


# 5. report
def classify(q: dict, c: dict, j: dict, a: dict) -> str:
    """Suggested failure class; I check and correct these by hand in REPORT.md."""
    if a["error"]:
        return "agent error"
    unanswerable = q["kind"] == "unanswerable"
    if unanswerable:
        return "ok" if c["refused"] else "answered an unanswerable question"
    if c["refused"]:
        return "wrong refusal (right page retrieved)" if c["retrieved_expected_page"] else "retrieval miss"
    if not c["citations_valid"]:
        return "citation not in retrieved passages"
    if j["supported"] == 0:
        return "unsupported claim"
    if j["correct"] == 0:
        return "wrong answer from retrieved passages" if c["retrieved_expected_page"] else "retrieval miss"
    return "ok"


def stage_report(questions: list[dict]) -> None:
    answers, judged = read_jsonl(ANSWERS), read_jsonl(JUDGED)
    rows = []
    for q in questions:
        a, j = answers.get(q["id"]), judged.get(q["id"])
        if not a or not j:
            continue
        c = code_checks(q, a)
        rows.append({"id": q["id"], "kind": q["kind"], "question": q["question"], "answer": a["answer"],
                     **c, "judge_correct": j["correct"], "judge_supported": j["supported"], "judge_reason": j["reason"],
                     "guardrail": a["guardrail"], "failure_class": classify(q, c, j, a),
                     "searches": " | ".join(a["searches"]), "input_tokens": a["input_tokens"],
                     "output_tokens": a["output_tokens"], "seconds": a["seconds"]})
    if not rows:
        print("nothing to report yet")
        return
    with open(EVAL / "results.csv", "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    n = len(rows)
    ans = [r for r in rows if r["kind"] != "unanswerable"]
    unans = [r for r in rows if r["kind"] == "unanswerable"]
    summary = {
        "questions": n,
        "judge_model": JUDGE_MODEL, "agent_model": agent_mod.AGENT_MODEL,
        "judge_correct_rate": round(sum(r["judge_correct"] == 1 for r in rows) / n, 3),
        "judge_supported_rate": round(sum(r["judge_supported"] == 1 for r in rows) / n, 3),
        "answerable_correct_rate": round(sum(r["judge_correct"] == 1 for r in ans) / max(len(ans), 1), 3),
        "correct_refusal_rate_on_unanswerable": round(sum(r["refused"] for r in unans) / max(len(unans), 1), 3),
        "wrong_refusal_rate_on_answerable": round(sum(r["refused"] for r in ans) / max(len(ans), 1), 3),
        "citations_valid_rate": round(sum(bool(r["citations_valid"]) for r in rows) / n, 3),
        "cites_expected_page_rate_answerable": round(sum(r["cites_expected_page"] is True for r in ans) / max(len(ans), 1), 3),
        "guardrail_repaired": sum(r["guardrail"] == "repaired" for r in rows),
        "guardrail_replaced": sum(r["guardrail"] == "replaced" for r in rows),
        "mean_input_tokens": round(sum(r["input_tokens"] for r in rows) / n),
        "mean_output_tokens": round(sum(r["output_tokens"] for r in rows) / n),
        "mean_seconds": round(sum(r["seconds"] for r in rows) / n, 2),
        "failure_classes": {k: sum(r["failure_class"] == k for r in rows) for k in sorted({r["failure_class"] for r in rows})},
    }

    # sheet for my own blind grading: question, reference, answer, evidence. No judge verdicts in it.
    labelled = {r["id"] for r in csv.DictReader(open(EVAL / "human_labels.csv", newline="", encoding="utf-8"))} if (EVAL / "human_labels.csv").exists() else set()
    ids = [r["id"] for r in rows]
    random.Random(7).shuffle(ids)
    sheet = sorted(ids[:max(TO_GRADE, len(labelled))] if not labelled else list(labelled))
    with open(EVAL / "to_grade.md", "w", encoding="utf-8") as f:
        f.write("# Answers to grade by hand\n\nFill eval/human_labels.csv (id,correct,supported,notes) BEFORE opening judge.jsonl or results.csv.\n"
                "correct = 1 if right against the reference (or a proper refusal); supported = 1 if every claim is in the retrieved text.\n\n")
        for r in rows:
            if r["id"] in sheet:
                q = next(x for x in questions if x["id"] == r["id"])
                f.write(f"## {r['id']} ({q['kind']})\n**Question:** {q['question']}\n\n**Reference:** {q['reference_answer']}\n\n"
                        f"**Answer:** {r['answer']}\n\n<details><summary>Retrieved passages</summary>\n\n{answers[r['id']]['evidence'][:6000]}\n\n</details>\n\n")

    human = {}
    hp = EVAL / "human_labels.csv"
    if hp.exists():
        for h in csv.DictReader(open(hp, newline="", encoding="utf-8")):
            if h.get("correct", "").strip() in ("0", "1") and h.get("supported", "").strip() in ("0", "1"):
                human[h["id"]] = (int(h["correct"]), int(h["supported"]))
    both = [(human[r["id"]], (r["judge_correct"], r["judge_supported"])) for r in rows if r["id"] in human and r["judge_correct"] in (0, 1)]
    if both:
        summary["human_labels"] = len(both)
        for i, name in enumerate(("correct", "supported")):
            agree = sum(h[i] == j[i] for h, j in both)
            summary[f"agreement_{name}"] = round(agree / len(both), 3)
            summary[f"disagreements_{name}"] = [r["id"] for r in rows if r["id"] in human and human[r["id"]][i] != (r["judge_correct"], r["judge_supported"])[i]]
        p_h = sum(h[0] for h, _ in both) / len(both)
        p_j = sum(j[0] for _, j in both) / len(both)
        pe = p_h * p_j + (1 - p_h) * (1 - p_j)
        po = summary["agreement_correct"]
        summary["cohen_kappa_correct"] = round((po - pe) / (1 - pe), 3) if pe < 1 else 1.0
    (EVAL / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print("\n" + json.dumps(summary, indent=2, ensure_ascii=False))
    if not human:
        print(f"\nNext: grade the answers in eval/to_grade.md by hand into eval/human_labels.csv, then run this stage again.")


# ------------------------------------------------------------------------------------------------
# before/after demo: add a document that answers an unanswerable question
async def demo(path: str, qid: str) -> None:
    q = next((x for x in read_questions() if x["id"] == qid), None) or {"question": qid}  # a question id, or free text
    qid = qid if "id" in q else "free text"
    out = EVAL / "before_after.md"
    async with agent_mod.CorpusAgent(approve=lambda name, args: True) as ag:  # I give approval for this one run
        before = await ag.ask(q["question"])
        add = await ag.ask(f"Please add the document {path} to the index.")
        added = [c for c in ag.tool_log if c["name"] == "add_document"]
        after = await ag.ask(q["question"])
    out.write_text(
        f"# Before / after adding {path}\n\n**Question ({qid}):** {q['question']}\n\n"
        f"## Before\n{before.answer}\n\n## add_document\n{added[0]['result'] if added else 'add_document was not called'}\n\n"
        f"## After\n{after.answer}\n", encoding="utf-8")
    print(out.read_text(encoding="utf-8"))


async def redo_after(qid: str) -> None:
    """Ask question QID again and replace only the '## After' part of eval/before_after.md (the document is already added)."""
    q = next(x for x in read_questions() if x["id"] == qid)
    out = EVAL / "before_after.md"
    text = out.read_text(encoding="utf-8")
    async with agent_mod.CorpusAgent(approve=lambda name, args: False) as ag:
        after = await ag.ask(q["question"])
    out.write_text(text.split("## After")[0] + f"## After\n{after.answer}\n", encoding="utf-8")
    print(out.read_text(encoding="utf-8"))


def main() -> int:
    EVAL.mkdir(exist_ok=True)
    args = sys.argv[1:]
    if "--redo-after" in args:
        asyncio.run(redo_after(args[args.index("--redo-after") + 1]))
        return 0
    if "--demo" in args:
        i = args.index("--demo")
        asyncio.run(demo(args[i + 1], args[i + 2]))
        return 0
    questions = read_questions()
    try:
        stage_retrieval(questions)
        if "--retrieval-only" in args:
            return 0
        asyncio.run(stage_answers(questions))
        stage_judge(questions)
        stage_report(questions)
    except index.QuotaExhausted as error:
        print(f"\nDaily embedding quota used up ({str(error)[:120]}). Progress is saved; run again after 09:00 (Spain).")
        return 2
    return 0


if __name__ == "__main__":
    sys.exit(main())
