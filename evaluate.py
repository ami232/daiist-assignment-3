"""
Assignment 3: evaluation (`main.py evaluate`).

1. Retrieval: hit rate at k = 1, 3, 5 for every chunking design x search mode,
   and how many words the top 5 add to the prompt.          -> eval/retrieval*.csv
2. End to end: the agent answers every question (add_document auto-rejected).
                                                            -> eval/answers.jsonl
3. Code checks: refusal phrase, citations valid (retrieved in this run), expected
   source retrieved / cited.
4. LLM judge with the rubric in eval/judge_rubric.md and the retrieved text as
   evidence: correct and supported, for every answer that is not a refusal.
5. Agreement with your own grades in eval/human_labels.csv. -> eval/agreement.csv
6. Outcomes, suggested failure causes, cost and latency.    -> eval/results.csv, eval/summary.md

Answers and verdicts are cached, so a re-run only spends quota on what changed
(`--fresh` re-asks everything). Other entry points:

    uv run python evaluate.py --only-retrieval
    uv run python evaluate.py --no-judge      # answers only: grade them yourself first
    uv run python evaluate.py --demo-add q33 corpus/new_doc.pdf   # before/after add_document
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
import unicodedata
from pathlib import Path

import rag
from rag import DESIGNS, ROOT, sha

EVAL_DIR = Path(os.environ.get("RAG_EVAL_DIR", ROOT / "eval"))
QUESTIONS = EVAL_DIR / "questions.csv"
HUMAN_LABELS = EVAL_DIR / "human_labels.csv"
ANSWERS = EVAL_DIR / "answers.jsonl"
JUDGE_CACHE = EVAL_DIR / "judge_cache.json"
RUBRIC = EVAL_DIR / "judge_rubric.md"

RETRIEVAL_RUNS = [(design, mode) for design in DESIGNS for mode in ("dense", "hybrid")]
KS = (1, 3, 5)
# The verdicts in eval/judge_cache.json were produced with gemini-3.5-flash-lite: on
# 25 Nov 2026 gemini-3.8-flash and gemini-3.5-flash answered 503 (overloaded) for
# minutes on end. Keeping it as the default lets a re-run reuse the cached verdicts.
JUDGE_MODEL = os.environ.get("JUDGE_MODEL", "gemini-3.5-flash-lite")
# If the preferred judge model is not available on this key, fall back in order.
JUDGE_FALLBACKS = ["gemini-3.5-flash", "gemini-3.8-flash"]
SLEEP_BETWEEN_QUESTIONS = float(os.environ.get("EVAL_SLEEP", "4"))  # free-tier requests per minute


def log(*args) -> None:
    print(*args, flush=True)


# ---------------------------------------------------------------- test set

def norm(text: str) -> str:
    text = "".join(c for c in unicodedata.normalize("NFD", text) if unicodedata.category(c) != "Mn")
    return re.sub(r"\s+", " ", text.casefold()).strip(" .")


def load_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if (r.get("question") or "").strip()]
    for r in rows:
        r["kind"] = r["kind"].strip().lower()
        r["expected"] = expected_pairs(r)
    return rows


def expected_pairs(q: dict) -> list[tuple[str, str]]:
    """(doc_id, location) passages that answer the question.

    `expected_source` and `expected_location` are ';'-separated and paired by
    position; one source with several locations means all in that source.
    """
    sources = [s.strip() for s in (q.get("expected_source") or "").split(";") if s.strip()]
    locations = [s.strip() for s in (q.get("expected_location") or "").split(";") if s.strip()]
    if not sources:
        return []
    if len(sources) == len(locations):
        return list(zip(sources, locations))
    if len(sources) == 1:
        return [(sources[0], loc) for loc in locations] or [(sources[0], "")]
    if len(locations) == 1:
        return [(s, locations[0]) for s in sources]
    raise ValueError(f"{q['id']}: cannot pair {sources} with {locations}")


def matches(doc_id: str, locations: list[str], pair: tuple[str, str]) -> bool:
    """A chunk (or citation) matches an expected passage: same document, same location.
    An empty expected location accepts any location in the document."""
    if doc_id != pair[0]:
        return False
    return not pair[1] or norm(pair[1]) in {norm(loc) for loc in locations}


# ---------------------------------------------------------------- 1. retrieval

def retrieval_eval(questions: list[dict]) -> list[dict]:
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    rows = []
    for design, mode in RETRIEVAL_RUNS:
        if rag.collection(design).count() == 0:
            log(f"  [{design}] collection is empty: run `main.py index` first. Skipped.")
            continue
        for q in answerable:
            results = rag.search(q["question"], k=max(KS), design=design, mode=mode)
            ranks = []
            for pair in q["expected"]:
                hit = next((r["rank"] for r in results
                            if matches(r["doc_id"], r["locations"].split("|"), pair)), None)
                ranks.append(hit)
            found = [r for r in ranks if r is not None]
            row = {"id": q["id"], "kind": q["kind"], "design": design, "mode": mode,
                   "first_rank": min(found) if found else "",
                   "words_top5": sum(r["words"] for r in results[:5])}
            for k in KS:
                row[f"hit@{k}"] = int(bool(found) and min(found) <= k)
                row[f"all@{k}"] = int(len(found) == len(ranks) and max(found) <= k) if found else 0
            row["retrieved"] = " ; ".join(rag.citation(r) for r in results)
            rows.append(row)
    write_csv(EVAL_DIR / "retrieval.csv", rows)

    summary = []
    for design, mode in RETRIEVAL_RUNS:
        sub = [r for r in rows if r["design"] == design and r["mode"] == mode]
        if not sub:
            continue
        multi = [r for r in sub if r["kind"] == "multi"]
        entry = {"design": design, "mode": mode, "questions": len(sub)}
        for k in KS:
            entry[f"hit@{k}"] = round(sum(r[f"hit@{k}"] for r in sub) / len(sub), 3)
        entry["multi_all@5"] = round(sum(r["all@5"] for r in multi) / len(multi), 3) if multi else ""
        entry["avg_words_top5"] = round(sum(r["words_top5"] for r in sub) / len(sub))
        summary.append(entry)
    write_csv(EVAL_DIR / "retrieval_summary.csv", summary)
    log("\nRetrieval (answerable questions):")
    for e in summary:
        log(f"  {e['design']:>6} {e['mode']:>6}  hit@1 {e['hit@1']:.2f}  hit@3 {e['hit@3']:.2f}  "
            f"hit@5 {e['hit@5']:.2f}  multi all@5 {e['multi_all@5']}  words top5 {e['avg_words_top5']}")
    plot_retrieval(summary)
    return rows


def plot_retrieval(summary: list[dict]) -> None:
    if not summary:
        return
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(7, 3.5))
    width = 0.8 / len(summary)
    for i, e in enumerate(summary):
        xs = [k + (i - (len(summary) - 1) / 2) * width for k in range(len(KS))]
        ax.bar(xs, [e[f"hit@{k}"] for k in KS], width, label=f"{e['design']} / {e['mode']}")
    ax.set_xticks(range(len(KS)), [f"k = {k}" for k in KS])
    ax.set_ylim(0, 1)
    ax.set_ylabel("Hit rate")
    ax.legend(frameon=False, fontsize=8)
    ax.spines[["top", "right"]].set_visible(False)
    fig.tight_layout()
    fig.savefig(EVAL_DIR / "retrieval.png", dpi=150)
    plt.close(fig)


# ---------------------------------------------------------------- 2. end to end

def reject_all(requests: list[dict]) -> list[dict]:
    return [{"type": "reject", "message": "Evaluation run: documents are not added."} for _ in requests]


def load_answers() -> dict[str, dict]:
    if not ANSWERS.exists():
        return {}
    answers = {}
    for line in ANSWERS.read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            answers[row["id"]] = row
    return answers


async def answer_all(questions: list[dict], fresh: bool) -> dict[str, dict]:
    from agent import AGENT_MODEL, Harness

    cached = {} if fresh else load_answers()
    todo = [q for q in questions
            if q["id"] not in cached or cached[q["id"]]["question"] != q["question"]
            or cached[q["id"]].get("model") != AGENT_MODEL or cached[q["id"]].get("error")]
    log(f"\nAgent ({AGENT_MODEL}): {len(todo)} questions to answer, {len(questions) - len(todo)} cached.")
    if todo:
        async with Harness(approve=reject_all) as harness:
            for i, q in enumerate(todo, 1):
                try:
                    result = await harness.ask(q["question"])
                except Exception as error:  # noqa: BLE001 - record and carry on
                    result = {"question": q["question"], "answer": "", "error": f"{type(error).__name__}: {error}",
                              "trace": [], "usage": {}, "seconds": 0, "refusal": False,
                              "citations": {"cited": [], "valid": [], "invalid": [], "retrieved": []},
                              "guard_fired": False, "model": AGENT_MODEL}
                result["id"] = q["id"]
                if any("Search unavailable" in step["output"] for step in result.get("trace", [])):
                    # The embedding quota ran out mid-question: the answer is not a real
                    # refusal, so it is marked and asked again on the next run.
                    result["error"] = "embedding quota exhausted during search"
                cached[q["id"]] = result
                log(f"  {q['id']} ({i}/{len(todo)}) {result['seconds']}s "
                    f"{'REFUSAL' if result['refusal'] else ''} {result.get('error', '')}")
                write_answers(cached, questions)
                if i < len(todo):
                    time.sleep(SLEEP_BETWEEN_QUESTIONS)
    return cached


def write_answers(answers: dict[str, dict], questions: list[dict]) -> None:
    order = [q["id"] for q in questions]
    with ANSWERS.open("w", encoding="utf-8") as f:
        for qid in order:
            if qid in answers:
                f.write(json.dumps(answers[qid], ensure_ascii=False) + "\n")


# ---------------------------------------------------------------- 3. code checks

def code_checks(q: dict, res: dict) -> dict:
    cites = res.get("citations") or {}
    retrieved = [tuple(x) for x in cites.get("retrieved", [])]
    valid = [tuple(x) for x in cites.get("valid", [])]
    return {
        "refusal": int(bool(res.get("refusal"))),
        "has_citation": int(bool(cites.get("cited"))),
        "citations_valid": int(not cites.get("invalid")),
        "guard_fired": int(bool(res.get("guard_fired"))),
        "expected_retrieved": int(any(matches(d, [l], p) for d, l in retrieved for p in q["expected"])),
        "expected_cited": int(any(matches(d, [l.split(".")[0].strip()], p) or matches(d, [l], p)
                                  for d, l in valid for p in q["expected"])),
        "error": res.get("error", ""),
    }


# ---------------------------------------------------------------- 4. LLM judge

def evidence(res: dict) -> str:
    texts = [step["output"] for step in res.get("trace", []) if step["tool"] == "search"]
    return "\n\n".join(texts) or "(no passages were retrieved)"


def judge(q: dict, res: dict, checks: dict, cache: dict) -> dict:
    """Refusals are graded in code; everything else by the LLM judge."""
    if checks["error"]:
        return {"correct": 0, "supported": 0, "reason": "agent error", "by": "code"}
    if checks["refusal"]:
        ok = int(q["kind"] == "unanswerable")
        return {"correct": ok, "supported": 1, "reason": "refusal", "by": "code"}
    rubric = RUBRIC.read_text(encoding="utf-8")
    key = sha(f"{JUDGE_MODEL}|{rubric}|{q['question']}|{q['reference_answer']}|{res['answer']}")
    if key in cache:
        return cache[key]
    prompt = (
        f"{rubric}\n\n# Question\n{q['question']}\n\n# Reference answer\n{q['reference_answer']}"
        f"{' (the corpus does not answer this question)' if q['kind'] == 'unanswerable' else ''}\n\n"
        f"# Retrieved passages\n{evidence(res)}\n\n# Assistant's answer\n{res['answer']}\n"
    )
    from google import genai
    from google.genai import types

    from api_key import load_api_key

    # 90 s per request: a call that hangs fails and is retried instead of blocking the run.
    client = genai.Client(api_key=load_api_key(), http_options=types.HttpOptions(timeout=90_000))
    models = [JUDGE_MODEL] + [m for m in JUDGE_FALLBACKS if m != JUDGE_MODEL]
    response, used, last_error = None, None, None
    for model in models:
        for attempt in range(5):
            try:
                response = client.models.generate_content(
                    model=model, contents=prompt,
                    config=types.GenerateContentConfig(temperature=0, response_mime_type="application/json"),
                )
                verdict = json.loads(response.text)
                used = model
                break
            except Exception as error:  # noqa: BLE001
                last_error = error
                message = str(error)
                if "404" in message or "NOT_FOUND" in message:
                    log(f"    judge model {model} not available, trying the next one")
                    break
                if "PerDay" in message or "per day" in message.lower():
                    log(f"    daily quota of {model} used up, trying the next one")
                    break
                wait = 15 * (attempt + 1)
                log(f"    judge {model}: {message[:80]}... retrying in {wait}s")
                time.sleep(wait)
        if used:
            break
    if not used:
        return {"correct": "", "supported": "", "reason": f"judge failed: {last_error}", "by": "error"}
    usage = getattr(response, "usage_metadata", None)
    verdict = {"correct": int(verdict.get("correct", 0)), "supported": int(verdict.get("supported", 0)),
               "reason": verdict.get("reason", ""), "by": used,
               "judge_tokens": getattr(usage, "total_token_count", 0) or 0}
    cache[key] = verdict
    JUDGE_CACHE.write_text(json.dumps(cache, ensure_ascii=False, indent=1), encoding="utf-8")
    return verdict


# ---------------------------------------------------------------- 5. outcomes and failures

def outcome(q: dict, checks: dict, verdict: dict) -> str:
    if q["kind"] == "unanswerable":
        return "correct_refusal" if checks["refusal"] else "answered_unanswerable"
    if checks["refusal"]:
        return "wrong_refusal"
    if verdict["correct"] == 1 and verdict["supported"] == 1:
        return "correct"
    if verdict["correct"] == 1:
        return "correct_but_unsupported"
    return "wrong" if verdict["supported"] == 1 else "wrong_and_unsupported"


def suggest_cause(q: dict, checks: dict, verdict: dict, result: str) -> str:
    """A first guess at the failure cause. The final classification is yours."""
    if result in ("correct", "correct_refusal"):
        return ""
    if result == "answered_unanswerable" or result == "correct_but_unsupported":
        return "unsupported claim"
    if not checks["expected_retrieved"]:
        return "retrieval miss"
    if result == "wrong_refusal":
        return "wrong refusal"
    if verdict["supported"] == 0:
        return "unsupported claim"
    return "wrong answer from right passage"


def agreement(rows: list[dict]) -> dict:
    if not HUMAN_LABELS.exists():
        return {}
    with HUMAN_LABELS.open(newline="", encoding="utf-8") as f:
        human = {r["id"]: r for r in csv.DictReader(f) if (r.get("id") or "").strip()}
    pairs = []
    for row in rows:
        h = human.get(row["id"])
        if not h or row["judge_correct"] == "":
            continue
        pairs.append({"id": row["id"], "human_correct": int(h["correct"]), "judge_correct": int(row["judge_correct"]),
                      "human_supported": int(h["supported"]), "judge_supported": int(row["judge_supported"]),
                      "graded_by": row["graded_by"], "human_notes": h.get("notes", ""),
                      "judge_reason": row["judge_reason"]})
    write_csv(EVAL_DIR / "agreement.csv", pairs)
    if not pairs:
        return {}

    def kappa(a: list[int], b: list[int]) -> float | str:
        n = len(a)
        po = sum(x == y for x, y in zip(a, b)) / n
        pa, pb = sum(a) / n, sum(b) / n
        pe = pa * pb + (1 - pa) * (1 - pb)
        return round((po - pe) / (1 - pe), 3) if pe < 1 else ""

    by_llm = [p for p in pairs if p["graded_by"] not in ("code",)]
    out = {"labelled": len(pairs), "labelled_judged_by_llm": len(by_llm)}
    for field in ("correct", "supported"):
        a = [p[f"human_{field}"] for p in pairs]
        b = [p[f"judge_{field}"] for p in pairs]
        out[f"agree_{field}"] = round(sum(x == y for x, y in zip(a, b)) / len(pairs), 3)
        out[f"kappa_{field}"] = kappa(a, b)
        if by_llm:
            a2 = [p[f"human_{field}"] for p in by_llm]
            b2 = [p[f"judge_{field}"] for p in by_llm]
            out[f"agree_{field}_llm_only"] = round(sum(x == y for x, y in zip(a2, b2)) / len(by_llm), 3)
    return out


# ---------------------------------------------------------------- 6. summary

def summarise(rows: list[dict], agree: dict) -> dict:
    n = len(rows)
    count = lambda k: sum(r["outcome"] == k for r in rows)  # noqa: E731
    answered = [r for r in rows if not r["refusal"] and not r["error"]]
    s = {
        "questions": n,
        "by_kind": {k: sum(r["kind"] == k for r in rows) for k in ("single", "multi", "unanswerable")},
        "correct": count("correct"),
        "correct_but_unsupported": count("correct_but_unsupported"),
        "wrong": count("wrong") + count("wrong_and_unsupported"),
        "unsupported_answers": sum(r["judge_supported"] == 0 for r in answered),
        "correct_refusals": count("correct_refusal"),
        "wrong_refusals": count("wrong_refusal"),
        "answered_unanswerable": count("answered_unanswerable"),
        "guard_fired": sum(r["guard_fired"] for r in rows),
        "invalid_citations": sum(1 - r["citations_valid"] for r in rows),
        "errors": sum(bool(r["error"]) for r in rows),
        "avg_tokens": round(sum(r["total_tokens"] for r in rows) / n) if n else 0,
        "avg_seconds": round(sum(r["seconds"] for r in rows) / n, 1) if n else 0,
        "avg_tool_calls": round(sum(r["tool_calls"] for r in rows) / n, 2) if n else 0,
        "agreement": agree,
    }
    s["accuracy"] = round((s["correct"] + s["correct_refusals"]) / n, 3) if n else 0
    (EVAL_DIR / "summary.json").write_text(json.dumps(s, indent=2), encoding="utf-8")

    lines = [
        "# Evaluation summary", "",
        f"{n} questions ({s['by_kind']['single']} single, {s['by_kind']['multi']} multi, "
        f"{s['by_kind']['unanswerable']} unanswerable).", "",
        "| Outcome | Count |", "|---|---|",
        f"| Correct and supported | {s['correct']} |",
        f"| Correct but unsupported | {s['correct_but_unsupported']} |",
        f"| Wrong answer | {s['wrong']} |",
        f"| Correct refusals | {s['correct_refusals']} |",
        f"| Wrong refusals | {s['wrong_refusals']} |",
        f"| Answered an unanswerable question | {s['answered_unanswerable']} |", "",
        f"Unsupported answers (judge): {s['unsupported_answers']}. Citation guard fired: {s['guard_fired']}. "
        f"Invalid citations: {s['invalid_citations']}. Errors: {s['errors']}.", "",
        f"Cost per question: {s['avg_tokens']} tokens, {s['avg_seconds']} s, {s['avg_tool_calls']} tool calls.",
    ]
    if agree:
        lines += ["", f"Judge vs your labels on {agree['labelled']} answers: correct agreement "
                      f"{agree['agree_correct']:.0%} (kappa {agree['kappa_correct']}), supported agreement "
                      f"{agree['agree_supported']:.0%} (kappa {agree['kappa_supported']})."]
    (EVAL_DIR / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    log("\n" + "\n".join(lines))
    return s


def write_csv(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("", encoding="utf-8")
        return
    fields = list(dict.fromkeys(k for r in rows for k in r))
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def reapply_guard(answers: dict[str, dict]) -> None:
    """Run the current citation guard again on each stored raw answer.

    The guard is deterministic (raw answer + retrieved passages), so a fix to it
    applies to cached answers without asking the model again.
    """
    from agent import citation_guard, is_refusal

    for row in answers.values():
        if row.get("raw_answer") is None or row.get("error"):
            continue
        answer, guard = citation_guard(row["raw_answer"], row.get("trace", []), row.get("approvals"))
        row.update(answer=answer, citations=guard, guard_fired=guard["fired"], refusal=is_refusal(answer))


def end_to_end(questions: list[dict], fresh: bool, judge_answers: bool = True) -> None:
    answers = asyncio.run(answer_all(questions, fresh))
    reapply_guard(answers)
    write_answers(answers, questions)
    # A sheet to grade by hand BEFORE looking at the judge (eval/human_labels.csv).
    write_csv(EVAL_DIR / "to_grade.csv", [
        {"id": q["id"], "kind": q["kind"], "question": q["question"], "reference_answer": q["reference_answer"],
         "answer": answers[q["id"]]["answer"],
         "retrieved": " ; ".join(f"[{d}, {l}]" for d, l in (answers[q["id"]].get("citations") or {}).get("retrieved", []))}
        for q in questions
    ])
    if not judge_answers:
        log("\nAnswers saved. Grade eval/to_grade.csv into eval/human_labels.csv, then run without --no-judge.")
        return
    cache = json.loads(JUDGE_CACHE.read_text(encoding="utf-8")) if JUDGE_CACHE.exists() else {}
    rows = []
    log("\nJudging answers ...")
    for q in questions:
        res = answers[q["id"]]
        checks = code_checks(q, res)
        verdict = judge(q, res, checks, cache)
        log(f"  {q['id']}: correct={verdict['correct']} supported={verdict['supported']} ({verdict['by']})")
        result = outcome(q, checks, verdict) if verdict["correct"] != "" else "not_graded"
        rows.append({
            "id": q["id"], "kind": q["kind"], "question": q["question"], "answer": res["answer"],
            **checks,
            "judge_correct": verdict["correct"], "judge_supported": verdict["supported"],
            "judge_reason": verdict["reason"], "graded_by": verdict["by"],
            "outcome": result, "suggested_cause": suggest_cause(q, checks, verdict, result) if verdict["correct"] != "" else "",
            "total_tokens": (res.get("usage") or {}).get("total_tokens", 0),
            "seconds": res.get("seconds", 0), "tool_calls": len(res.get("trace", [])),
        })
    write_csv(EVAL_DIR / "results.csv", rows)
    summarise(rows, agreement(rows))


# ---------------------------------------------------------------- add-document demo

def demo_add(qid: str, path: str) -> None:
    """Ask a question, add a document (you approve it in the terminal), ask again."""
    from agent import Harness, ask_approval

    q = next(q for q in load_questions() if q["id"] == qid)

    async def go():
        async with Harness(approve=ask_approval) as harness:
            before = await harness.ask(q["question"])
            added = await harness.ask(f"Añade al corpus el documento {Path(path).resolve()}")
        async with Harness(approve=reject_all) as harness:  # fresh server: reloads the index
            after = await harness.ask(q["question"])
        return before, added, after

    before, added, after = asyncio.run(go())
    text = (f"# Adding a document\n\n**Question ({qid}):** {q['question']}\n\n**Document:** `{path}`\n\n"
            f"## Before\n\n{before['answer']}\n\n## Add document\n\nApprovals: {added['approvals']}\n\n"
            f"{added['trace'][-1]['output'] if added['trace'] else added['answer']}\n\n"
            f"## After\n\n{after['answer']}\n")
    (EVAL_DIR / "add_document_demo.md").write_text(text, encoding="utf-8")
    log(text)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Evaluate retrieval and the agent end to end.")
    parser.add_argument("--only-retrieval", action="store_true")
    parser.add_argument("--fresh", action="store_true", help="re-ask every question instead of using cached answers")
    parser.add_argument("--no-judge", action="store_true", help="answer only, so you can grade before seeing the judge")
    parser.add_argument("--demo-add", nargs=2, metavar=("QUESTION_ID", "PATH"))
    args = parser.parse_args()
    if args.demo_add:
        demo_add(*args.demo_add)
        sys.exit(0)
    qs = load_questions()
    if not qs:
        sys.exit("eval/questions.csv has no questions yet.")
    retrieval_eval(qs)
    if not args.only_retrieval:
        end_to_end(qs, args.fresh, judge_answers=not args.no_judge)
