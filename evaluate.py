"""
Assignment 3: evaluation (`main.py evaluate`).

1. Retrieval: hit rate at k = 1, 3, 5 for each design in index.DESIGNS
   (one query embedding per question, cached and shared by all designs).
2. End to end: the agent (agent.Harness) answers every question; answers are
   cached in eval/answers.jsonl so a rerun spends no quota (EVAL_FRESH=1 redoes them).
3. Code checks: valid citations, citation of the expected source, refusals.
4. LLM judge with a rubric and the retrieved passages as evidence (cached).
5. Agreement between the judge and eval/human_labels.csv.
6. Before/after: one unanswerable question, then a document that answers it
   is added through the agent (approval given programmatically), then asked again.

Writes eval/retrieval.csv, eval/answers.jsonl, eval/judgements.jsonl,
eval/results.csv, eval/before_after.json and eval/summary.json.
"""

from __future__ import annotations

import asyncio
import csv
import json
import os
import re
import sys
import time
from pathlib import Path

import index
import agent

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
HUMAN = EVAL / "human_labels.csv"
QUERY_VECTORS = EVAL / "query_vectors.json"
ANSWERS = EVAL / "answers.jsonl"
JUDGEMENTS = EVAL / "judgements.jsonl"
KS = (1, 3, 5)
# Not the agent's model (less self-preference); gemini-3.5-flash allows only 20 requests a day.
JUDGE_MODEL = os.environ.get("GEMINI_JUDGE_MODEL", "gemini-3.1-flash-lite")
JUDGE_FALLBACKS = ["gemini-3.5-flash-lite", "gemini-flash-lite-latest"]
FRESH = os.environ.get("EVAL_FRESH") == "1"

# Before/after demo: an unanswerable question and the document that answers it.
DEMO_QUESTION_ID = os.environ.get("DEMO_QUESTION_ID", "q29")   # Class D airspace
DEMO_SOURCE = ("phak.pdf", (376, 387))                          # PHAK ch. 15 Airspace
DEMO_FILE = ROOT / "corpus" / "PHAK-ch15-Airspace.pdf"


def read_csv(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return [{k: (v or "").strip() for k, v in r.items()} for r in csv.DictReader(f) if (r.get("id") or "").strip()]


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def load_jsonl(path: Path) -> dict[str, dict]:
    if not path.is_file() or FRESH:
        return {}
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            out[row["id"]] = row
    return out


def append_jsonl(path: Path, row: dict) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def expected_passages(q: dict) -> list[tuple[str, str]]:
    """[(source, page)] from expected_source / expected_location, ';'-separated and aligned."""
    sources = [s.strip() for s in q["expected_source"].split(";") if s.strip()]
    locations = [l.strip() for l in q["expected_location"].split(";") if l.strip()]
    if len(sources) == 1 and len(locations) > 1:
        sources = sources * len(locations)
    return list(zip(sources, locations + [""] * (len(sources) - len(locations))))


def passage_hit(hit: dict, source: str, page: str) -> bool:
    if hit["source"] != source:
        return False
    return not page or f"|{page}|" in hit.get("pages", "")


# --------------------------------------------------------------------------- #
# 1. Retrieval
# --------------------------------------------------------------------------- #

def query_vectors(questions: list[dict]) -> dict[str, list[float]]:
    cache = json.loads(QUERY_VECTORS.read_text(encoding="utf-8")) if QUERY_VECTORS.is_file() else {}
    for q in questions:
        if q["question"] not in cache:
            cache[q["question"]] = index.embed_query(q["question"])
            QUERY_VECTORS.write_text(json.dumps(cache), encoding="utf-8")
    return cache


def evaluate_retrieval(questions: list[dict]) -> list[dict]:
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    vectors = query_vectors(answerable)
    rows = []
    for design in index.DESIGNS:
        hits_any = {k: 0 for k in KS}
        hits_all = {k: 0 for k in KS}
        words, per_q = [], []
        for q in answerable:
            results = index.search(q["question"], k=max(KS), design=design, query_vector=vectors[q["question"]])
            expected = expected_passages(q)
            first = next((i + 1 for i, h in enumerate(results) if any(passage_hit(h, s, p) for s, p in expected)), None)
            for k in KS:
                top = results[:k]
                found = [any(passage_hit(h, s, p) for h in top) for s, p in expected]
                hits_any[k] += any(found)
                hits_all[k] += all(found)
            words.append(sum(h["words"] for h in results[:5]))
            per_q.append(f"{q['id']}:{first or '-'}")
        n = len(answerable)
        row = {"design": design, "chunks": index.collection(design).count(), "questions": n}
        for k in KS:
            row[f"hit@{k}"] = round(hits_any[k] / n, 3)
        for k in KS:
            row[f"all@{k}"] = round(hits_all[k] / n, 3)
        row["words_top5"] = round(sum(words) / n)
        row["first_hit_rank"] = " ".join(per_q)
        rows.append(row)
    write_csv(EVAL / "retrieval.csv", rows)
    return rows


# --------------------------------------------------------------------------- #
# 2-3. Agent answers and code checks
# --------------------------------------------------------------------------- #

async def run_agent(questions: list[dict]) -> dict[str, dict]:
    answers = load_jsonl(ANSWERS)
    if FRESH and ANSWERS.exists():
        ANSWERS.unlink()
    todo = [q for q in questions if q["id"] not in answers]
    if todo:
        async with agent.Harness(approve=lambda action: False) as harness:
            for q in todo:
                print(f"  asking {q['id']}: {q['question'][:70]}", flush=True)
                try:
                    result = await harness.answer(q["question"])
                except Exception as error:  # noqa: BLE001 - record and continue
                    print(f"    failed: {type(error).__name__}: {str(error)[:200]}", flush=True)
                    continue
                result["id"] = q["id"]
                answers[q["id"]] = result
                append_jsonl(ANSWERS, result)
    return answers


def code_checks(q: dict, a: dict) -> dict:
    refused = agent.is_refusal(a["answer"])
    guard = a["citation_check"]
    cited = agent.CITATION.findall(a["answer"])
    expected_sources = {s for s, _ in expected_passages(q)} if q["kind"] != "unanswerable" else set()
    retrieved = agent.retrieved_citations(a["trace"])
    retrieval_hit = any(any(s == rs and (not p or agent.page_in_span(p, rp)) for rs, rp in retrieved)
                        for s, p in expected_passages(q)) if expected_sources else None
    return {
        "refused": int(refused),
        "should_refuse": int(q["kind"] == "unanswerable"),
        "correct_refusal": int(refused and q["kind"] == "unanswerable"),
        "wrong_refusal": int(refused and q["kind"] != "unanswerable"),
        "missed_refusal": int(not refused and q["kind"] == "unanswerable"),
        "n_citations": len(cited),
        "invalid_citations_raw": len(guard["invalid"]),
        "citations_valid": int(not guard["invalid"] and (refused or guard["valid"] > 0)),
        "cites_expected_source": int(any(s in expected_sources for s, _ in cited)) if expected_sources else "",
        "retrieved_expected_passage": "" if retrieval_hit is None else int(retrieval_hit),
        "guardrail_fired": int(guard["fired"]),
        "searches": sum(1 for t in a["trace"] if t["tool"] == "search"),
    }


# --------------------------------------------------------------------------- #
# 4. LLM judge
# --------------------------------------------------------------------------- #

RUBRIC = """You grade answers from a study assistant for student pilots. The assistant may only use
passages retrieved from FAA handbooks. You get the question, the reference answer written by the
test author, the passages the assistant retrieved, and the assistant's answer.

Grade two things, each 1 or 0:

correct
  1 if the answer gives the key facts of the reference answer and nothing that contradicts it.
    Extra detail is fine if it is accurate. Wording does not matter.
  1 if the question is UNANSWERABLE (the reference says the corpus does not cover it) and the
    assistant declines to answer instead of giving facts.
  0 if a key fact is missing or wrong, if it answers an unanswerable question with facts,
    or if it refuses a question the reference answers.

supported
  1 if every factual claim in the answer is stated in, or directly follows from, the retrieved
    passages. A refusal with no factual claims is supported.
  0 if any claim (a number, limit, procedure, cause) is not in the passages, even if it is true.

Return JSON only: {"correct": 0 or 1, "supported": 0 or 1, "reason": "<one sentence>"}"""


def judge_prompt(q: dict, a: dict) -> str:
    passages = "\n\n".join(t["result"] for t in a["trace"] if t["tool"] == "search") or "(none retrieved)"
    return (f"{RUBRIC}\n\nQUESTION ({q['kind']}):\n{q['question']}\n\nREFERENCE ANSWER:\n{q['reference_answer']}\n\n"
            f"RETRIEVED PASSAGES:\n{passages[:30000]}\n\nASSISTANT ANSWER:\n{a['answer']}")


def judge(q: dict, a: dict) -> dict:
    from google.genai import types
    # Free-tier models often answer 503 "high demand": on any error move straight
    # to the next model in the rotation, and only wait once all have failed.
    models = [JUDGE_MODEL, *JUDGE_FALLBACKS]
    for attempt in range(3 * len(models)):
        model = models[attempt % len(models)]
        try:
            r = index.gemini().models.generate_content(
                model=model, contents=judge_prompt(q, a),
                config=types.GenerateContentConfig(temperature=0, response_mime_type="application/json"),
            )
            verdict = json.loads(r.text)
            usage = r.usage_metadata
            return {"id": q["id"], "correct": int(verdict["correct"]), "supported": int(verdict["supported"]),
                    "reason": verdict.get("reason", ""), "judge_tokens": usage.total_token_count or 0,
                    "judge_model": model}
        except Exception as error:  # noqa: BLE001 - retry rate limits and bad JSON
            print(f"    judge {model} failed: {str(error)[:90]}", flush=True)
            if attempt % len(models) == len(models) - 1:
                wait = 20 * (attempt // len(models) + 1)
                print(f"    all judge models failed; waiting {wait}s", flush=True)
                time.sleep(wait)
    raise RuntimeError(f"judge failed on {q['id']}")


def reapply_guardrail(answers: dict[str, dict]) -> list[str]:
    """Re-run the (deterministic) citation check on each saved raw answer.

    When the guardrail code changes, saved answers are updated without asking
    the model again, and their judgements are dropped so the judge re-grades them.
    """
    changed = []
    for qid, a in answers.items():
        text, report = agent.check_citations(a["raw_answer"], a["trace"])
        if text != a["answer"] or report != a["citation_check"]:
            a["answer"], a["citation_check"] = text, report
            changed.append(qid)
    if changed:
        ANSWERS.write_text("".join(json.dumps(a, ensure_ascii=False) + "\n" for a in answers.values()),
                           encoding="utf-8")
        verdicts = load_jsonl(JUDGEMENTS)
        kept = [v for k, v in verdicts.items() if k not in changed]
        JUDGEMENTS.write_text("".join(json.dumps(v, ensure_ascii=False) + "\n" for v in kept), encoding="utf-8")
    return changed


def run_judge(questions: list[dict], answers: dict[str, dict]) -> dict[str, dict]:
    verdicts = load_jsonl(JUDGEMENTS)
    if FRESH and JUDGEMENTS.exists():
        JUDGEMENTS.unlink()
    for q in questions:
        if q["id"] in answers and q["id"] not in verdicts:
            try:
                verdicts[q["id"]] = judge(q, answers[q["id"]])
            except RuntimeError as error:   # skip it; the next run judges it
                print(f"    {error}; skipped", flush=True)
                continue
            append_jsonl(JUDGEMENTS, verdicts[q["id"]])
    return verdicts


# --------------------------------------------------------------------------- #
# 5. Agreement with human labels
# --------------------------------------------------------------------------- #

def cohen_kappa(a: list[int], b: list[int]) -> float | None:
    n = len(a)
    if not n:
        return None
    po = sum(x == y for x, y in zip(a, b)) / n
    pa, pb = sum(a) / n, sum(b) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return None if pe == 1 else round((po - pe) / (1 - pe), 3)


def agreement(verdicts: dict[str, dict]) -> dict:
    labels = read_csv(HUMAN)
    out = {"graded": 0}
    pairs = [(h, verdicts[h["id"]]) for h in labels if h["id"] in verdicts and h.get("correct") in {"0", "1"}]
    out["graded"] = len(pairs)
    for field in ("correct", "supported"):
        hs = [int(h[field]) for h, _ in pairs if h.get(field) in {"0", "1"}]
        js = [v[field] for h, v in pairs if h.get(field) in {"0", "1"}]
        if hs:
            out[f"{field}_agreement"] = round(sum(x == y for x, y in zip(hs, js)) / len(hs), 3)
            out[f"{field}_kappa"] = cohen_kappa(hs, js)
            out[f"{field}_disagreements"] = [h["id"] for h, v in pairs if h.get(field) in {"0", "1"}
                                             and int(h[field]) != v[field]]
    return out


# --------------------------------------------------------------------------- #
# 6. Before / after adding a document
# --------------------------------------------------------------------------- #

def make_demo_file() -> Path:
    """Cut PHAK chapter 15 (Airspace), which is not in the corpus, into its own PDF."""
    from pypdf import PdfReader, PdfWriter
    if not DEMO_FILE.is_file():
        src = index.download(index.SOURCES[0])
        reader, writer = PdfReader(str(src)), PdfWriter()
        first, last = DEMO_SOURCE[1]
        for n in range(first, last + 1):
            writer.add_page(reader.pages[n - 1])
        with DEMO_FILE.open("wb") as f:
            writer.write(f)
    return DEMO_FILE


async def before_after(questions: list[dict], answers: dict[str, dict]) -> dict | None:
    path = EVAL / "before_after.json"
    if path.is_file() and not FRESH:
        return json.loads(path.read_text(encoding="utf-8"))
    q = next((q for q in questions if q["id"] == DEMO_QUESTION_ID), None)
    if q is None:
        print("  skipped: set DEMO_QUESTION_ID to an unanswerable question about airspace")
        return None
    before = answers.get(q["id"])
    demo_file = make_demo_file()
    async with agent.Harness(approve=lambda action: True) as harness:
        if before is None:
            before = await harness.answer(q["question"])
        added = await harness.answer(f"Please add the document at {demo_file} to the corpus.")
        after = await harness.answer(q["question"])
    # Adding the same file again: same name and content, so nothing is embedded.
    duplicate = index.add_document(demo_file)
    result = {
        "id": q["id"], "question": q["question"], "document": demo_file.name,
        "before": before["answer"], "add_step": added["answer"], "approvals": added["approvals"],
        "add_tool_result": [t["result"] for t in added["trace"] if t["tool"] == "add_document"],
        "after": after["answer"], "after_sources": agent.retrieved_citations(after["trace"]),
        "add_again": duplicate,
    }
    path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    return result


# --------------------------------------------------------------------------- #

def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    questions = read_csv(QUESTIONS)
    for q in questions:
        q["kind"] = q["kind"].lower()
    if not questions:
        raise SystemExit("eval/questions.csv has no questions yet.")

    print("== 1. Retrieval")
    retrieval = evaluate_retrieval(questions)
    for r in retrieval:
        print(f"  {r['design']:8} chunks={r['chunks']:4}  " + "  ".join(f"hit@{k}={r[f'hit@{k}']:.2f}" for k in KS)
              + "  " + "  ".join(f"all@{k}={r[f'all@{k}']:.2f}" for k in KS) + f"  words(top5)={r['words_top5']}")

    print(f"== 2. Agent answers ({agent.CHAT_MODEL})")
    answers = asyncio.run(run_agent(questions))
    changed = reapply_guardrail(answers)
    if changed:
        print(f"  citation check changed saved answers {changed}; they will be re-judged")

    print(f"== 3-4. Code checks and judge ({JUDGE_MODEL})")
    verdicts = run_judge(questions, answers)
    rows = []
    for q in questions:
        a = answers.get(q["id"])
        if not a:
            continue
        v = verdicts.get(q["id"], {})
        rows.append({
            "id": q["id"], "kind": q["kind"], "question": q["question"],
            **code_checks(q, a),
            "judge_correct": v.get("correct", ""), "judge_supported": v.get("supported", ""),
            "judge_reason": v.get("reason", ""),
            "tokens": a["tokens"]["total"], "seconds": a["seconds"],
            "answer": a["answer"],
        })
    write_csv(EVAL / "results.csv", rows)

    n = len(rows)
    unans = [r for r in rows if r["kind"] == "unanswerable"]
    ans = [r for r in rows if r["kind"] != "unanswerable"]
    summary = {
        "questions": n, "answered_by_agent": n, "chat_model": agent.CHAT_MODEL, "judge_model": JUDGE_MODEL,
        "retrieval": retrieval,
        "judge_correct": round(sum(r["judge_correct"] == 1 for r in rows) / n, 3),
        "judge_supported": round(sum(r["judge_supported"] == 1 for r in rows) / n, 3),
        "unsupported_answers": sum(r["judge_supported"] == 0 for r in rows),
        "correct_refusals": f"{sum(r['correct_refusal'] for r in unans)}/{len(unans)}",
        "wrong_refusals": f"{sum(r['wrong_refusal'] for r in ans)}/{len(ans)}",
        "missed_refusals": f"{sum(r['missed_refusal'] for r in unans)}/{len(unans)}",
        "citations_valid": round(sum(r["citations_valid"] for r in rows) / n, 3),
        "guardrail_fired": [r["id"] for r in rows if r["guardrail_fired"]],
        "by_kind": {k: {"n": len(g), "judge_correct": round(sum(r["judge_correct"] == 1 for r in g) / len(g), 3)}
                    for k in ("single", "multi", "unanswerable") if (g := [r for r in rows if r["kind"] == k])},
        "mean_tokens": round(sum(r["tokens"] for r in rows) / n),
        "mean_seconds": round(sum(r["seconds"] for r in rows) / n, 1),
        "mean_judge_tokens": round(sum(v.get("judge_tokens", 0) for v in verdicts.values()) / max(len(verdicts), 1)),
        "agreement_with_human": agreement(verdicts),
    }

    print("== 6. Before / after adding a document")
    demo = asyncio.run(before_after(questions, answers))
    if demo:
        summary["before_after"] = {"id": demo["id"], "document": demo["document"]}
        print(f"  {demo['id']} before: {demo['before'][:150]}\n  {demo['id']} after:  {demo['after'][:150]}")

    (EVAL / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print("\n== Summary")
    for key in ("judge_correct", "judge_supported", "unsupported_answers", "correct_refusals", "wrong_refusals",
                "missed_refusals", "citations_valid", "guardrail_fired", "by_kind", "mean_tokens", "mean_seconds",
                "agreement_with_human"):
        print(f"  {key}: {summary[key]}")


if __name__ == "__main__":
    main()
