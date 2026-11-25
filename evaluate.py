"""
Assignment 3: evaluation (`main.py evaluate`).

1. Retrieval: hit rate at k = 1, 3, 5 for every design in retrieval.DESIGNS,
   plus the words each design adds to the prompt. `python evaluate.py
   --retrieval-only` stops here, so the search design can be chosen before
   the agent's answers are generated (they are cached per design).
2. End to end: the agent (agent.Harness) answers every question.
3. Code checks: refusal or not, citations present, citations valid (point to a
   retrieved passage), expected passage retrieved.
4. LLM judge with the rubric in eval/rubric.md and the retrieved text as
   evidence, for answers code cannot grade (non-refusals).
5. Agreement between the judge and eval/human_labels.csv.
6. Failure signals with a heuristic suggested cause (you confirm the cause).
7. Before/after: if eval/add_document.json names a question and a file, the
   question is asked, the file is added (approved), and it is asked again.

Everything expensive is cached in eval/ (answers.jsonl, judge.jsonl) and query
vectors in index/, so a re-run only does what is missing.
"""

from __future__ import annotations

import asyncio
import csv
import json
import os
import re
import statistics
import sys
import time
from pathlib import Path

os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")

import index
import retrieval

ROOT = Path(__file__).resolve().parent
EVAL = Path(os.environ.get("EVAL_DIR", ROOT / "eval"))   # override only for testing
QUESTIONS = EVAL / "questions.csv"
HUMAN = EVAL / "human_labels.csv"
RUBRIC = EVAL / "rubric.md"
ANSWERS = EVAL / "answers.jsonl"
JUDGE = EVAL / "judge.jsonl"
ADD_DOC = EVAL / "add_document.json"
# A different model family from the agent (Gemini): less self-preference, and its own quota.
# Fallback to the smaller Gemma when the first is overloaded (503) or out of quota.
JUDGE_MODELS = ["gemma-4-31b-it", "gemma-4-26b-a4b-it", "gemini-3.5-flash-lite"]   # flash-lite = backup when Gemma is overloaded (same model family as the agent: self-grading bias)
JUDGE_TOKENS_PER_MINUTE = 14_000   # under the free tier's 16K, with margin
KS = (1, 3, 5)
MIN_SECONDS_PER_QUESTION = 15   # keeps the agent under the free tier's 15 requests per minute


def say(*a):
    print(*a, flush=True)


# --------------------------------------------------------------------------- questions

def source_name(value: str) -> str:
    """Accept the source as in chunk metadata ("AI Act") or as the file name ("ai_act.pdf")."""
    meta = index.DOCUMENTS.get(value.strip())
    return meta["source"] if meta else value.strip()


def load_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if (r.get("question") or "").strip()]
    for r in rows:
        r["kind"] = r["kind"].strip().lower()
        srcs = [s.strip() for s in r["expected_source"].split(";") if s.strip()]
        locs = [l.strip() for l in r["expected_location"].split(";") if l.strip()]
        srcs = [source_name(x) for x in srcs]
        if len(srcs) == 1 and len(locs) > 1:
            srcs = srcs * len(locs)
        r["expected"] = list(zip(srcs, locs))   # [(source, location)], empty if unanswerable
    return rows


# --------------------------------------------------------------------------- retrieval hit rate

def ngrams(text: str, n: int = 8) -> set[tuple[str, ...]]:
    w = re.findall(r"\w+", text.lower())
    return {tuple(w[i:i + n]) for i in range(len(w) - n + 1)}


class Grader:
    """Is a retrieved chunk the expected passage?

    Structure chunks: same source and same article / recital / annex.
    Fixed windows (only know their pages): the window shares at least
    min(40, half) of the expected unit's 8-word sequences, i.e. it contains a
    substantial piece of that article's text.
    """

    def __init__(self):
        self.structure = [json.loads(l) for l in (index.INDEX_DIR / "chunks_structure.jsonl").open(encoding="utf-8")]
        self._grams: dict = {}

    def unit_grams(self, source: str, location: str) -> set:
        key = (source, location)
        if key not in self._grams:
            want = retrieval.units(location)
            text = " ".join(c["text"].split("\n", 1)[-1] for c in self.structure
                            if c["source"] == source and retrieval.units(c["location"]) & want)
            self._grams[key] = ngrams(text)
        return self._grams[key]

    def is_hit(self, chunk: dict, source: str, location: str) -> bool:
        if chunk["source"] != source:
            return False
        if chunk["kind"] != "window":
            return bool(retrieval.units(chunk["location"]) & retrieval.units(location))
        expected = self.unit_grams(source, location)
        if not expected:
            return False
        shared = len(ngrams(chunk["text"]) & expected)
        return shared >= min(40, len(expected) // 2)


def evaluate_retrieval(questions: list[dict]) -> list[dict]:
    grader = Grader()
    answerable = [q for q in questions if q["expected"]]
    available = {d for d in retrieval.DESIGNS
                 if index.collection("fixed" if d == "fixed" else "structure").count() > 0}
    rows, summary = [], []
    for design in retrieval.DESIGNS:
        if design not in available:
            say(f"  {design}: collection empty, skipped (run main.py index)")
            continue
        hits = {k: 0 for k in KS}
        all_hits = {k: 0 for k in KS}
        n_multi = 0
        words = []
        for q in answerable:
            chunks = retrieval.search(q["question"], k=max(KS), design=design)
            words.append(sum(len(c["text"].split()) for c in chunks))
            # rank (1-based) of the first chunk matching each expected passage
            ranks = []
            for src, loc in q["expected"]:
                r = next((i + 1 for i, c in enumerate(chunks) if grader.is_hit(c, src, loc)), None)
                ranks.append(r)
            first = min([r for r in ranks if r], default=None)
            for k in KS:
                hits[k] += bool(first and first <= k)
                if q["kind"] == "multi":
                    all_hits[k] += all(r and r <= k for r in ranks)
            n_multi += q["kind"] == "multi"
            rows.append({"design": design, "id": q["id"], "kind": q["kind"],
                         "first_hit_rank": first or "", "ranks_per_expected": ";".join(str(r or "-") for r in ranks),
                         "retrieved": " | ".join(retrieval.citation(c) for c in chunks)})
        n = len(answerable)
        summary.append({
            "design": design, "questions": n,
            **{f"hit@{k}": round(hits[k] / n, 3) for k in KS},
            **{f"multi_all@{k}": round(all_hits[k] / n_multi, 3) if n_multi else "" for k in KS},
            "avg_words_top5": round(statistics.mean(words)),
        })
    write_csv(EVAL / "retrieval_results.csv", rows)
    write_csv(EVAL / "retrieval_summary.csv", summary)
    return summary


# --------------------------------------------------------------------------- end to end

def load_jsonl(path: Path) -> dict[str, dict]:
    out = {}
    if path.exists():
        for line in path.open(encoding="utf-8"):
            try:
                row = json.loads(line)
            except json.JSONDecodeError:
                continue
            out[row["key"]] = row
    return out


def append_jsonl(path: Path, row: dict) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def answer_key(q: dict) -> str:
    """Cached answers are reused only for the same question, search design and AGENTS.md rules."""
    import hashlib
    rules = hashlib.sha256((ROOT / "AGENTS.md").read_bytes().replace(b"\r\n", b"\n")).hexdigest()[:12]   # same key on a Windows (CRLF) checkout
    return f"{q['id']}|{q['question']}|{retrieval.SEARCH_DESIGN}|{rules}"


async def run_agent_on(questions: list[dict]) -> dict[str, dict]:
    from agent import Harness
    cached = load_jsonl(ANSWERS)
    todo = [q for q in questions if answer_key(q) not in cached]
    if todo:
        say(f"  agent: {len(todo)} new answers ({len(questions) - len(todo)} cached)")
        async with Harness(approve=lambda name, args: False) as h:
            for i, q in enumerate(todo, 1):
                started = time.monotonic()
                try:
                    res = await h.ask(q["question"])
                except Exception as e:   # one bad question must not lose the others
                    say(f"    {q['id']}: ERROR {type(e).__name__}: {str(e)[:200]}")
                    continue
                row = {"key": answer_key(q), "id": q["id"], **res}
                append_jsonl(ANSWERS, row)
                cached[row["key"]] = row
                say(f"    [{i}/{len(todo)}] {q['id']} {res['seconds']}s {res['tokens']['total']} tok"
                    f"{' REFUSED' if retrieval.is_refusal(res['answer']) else ''}")
                # Pace the run: ~3 model calls per question, free tier allows 15 per minute.
                await asyncio.sleep(max(0.0, MIN_SECONDS_PER_QUESTION - (time.monotonic() - started)))
    return {q["id"]: cached[answer_key(q)] for q in questions if answer_key(q) in cached}


def code_checks(q: dict, a: dict, sources: set[str]) -> dict:
    retrieved = [tuple(x) for x in a["retrieved"]]
    sources = set(sources) | {src for src, _ in retrieved}
    cites = retrieval.cited(a["answer"], sources)
    refused = retrieval.is_refusal(a["answer"])
    expected_found = any(retrieval.citation_valid(e, retrieved) for e in q["expected"]) if q["expected"] else ""
    return {
        "refused": int(refused),
        "n_citations": len(cites),
        "citations_valid": int(all(retrieval.citation_valid(c, retrieved) for c in cites)) if cites else "",
        "expected_retrieved": int(expected_found) if q["expected"] else "",
        "searches": sum(1 for t in a["trace"] if t.get("tool") == "search"),
        "guardrail_fired": int(any(e.get("guardrail") == "citations" for e in a["guardrail_events"])),
    }


# --------------------------------------------------------------------------- judge

JUDGE_PROMPT = """You grade answers from a compliance assistant that must answer only from retrieved EU law passages.

RUBRIC
{rubric}

QUESTION
{question}

REFERENCE ANSWER (written by a human from the regulation)
{reference}

RETRIEVED PASSAGES (the only evidence the assistant had)
{evidence}

ASSISTANT ANSWER
{answer}

Return JSON: {{"correct": 0 or 1, "supported": 0 or 1, "reason": "<one or two sentences>"}}"""


def judge(q: dict, a: dict) -> dict:
    """LLM judge for one answer (cached by question, answer and rubric text)."""
    import hashlib
    import time
    from google.genai import types
    cached = load_jsonl(JUDGE)
    digest = lambda t: hashlib.sha256(t.encode("utf-8")).hexdigest()[:16]   # stable across runs, unlike hash()
    key = f"{answer_key(q)}|{digest(a['answer'])}|{digest(RUBRIC.read_text(encoding='utf-8'))}"
    if key in cached:
        return cached[key]
    # Each retrieved passage once, even if several searches returned it.
    blocks = [b.strip() for t in a["trace"] if t.get("tool_result") == "search"
              for b in re.split(r"\n\n(?=\[\d+\] CITE AS:)", t["text"])]
    unique = {re.sub(r"^\[\d+\] ", "", b): None for b in blocks if b}   # same passage, different rank number
    evidence = "\n\n".join(unique) or "(none)"
    prompt = JUDGE_PROMPT.format(rubric=RUBRIC.read_text(encoding="utf-8"), question=q["question"],
                                 reference=q["reference_answer"], evidence=evidence[:45000], answer=a["answer"])
    started = time.monotonic()
    for attempt in range(6):
        model = JUDGE_MODELS[attempt % len(JUDGE_MODELS)]
        try:
            resp = index.gemini().models.generate_content(
                model=model, contents=prompt,
                config=types.GenerateContentConfig(temperature=0, response_mime_type="application/json"))
            verdict = json.loads(re.search(r"\{.*\}", resp.text, re.S).group(0))
            break
        except Exception as e:  # noqa: BLE001 - rate limits / overload: wait and retry
            if attempt == 5:
                raise
            say(f"    judge retry ({model}: {type(e).__name__}: {str(e)[:60]})")
            time.sleep(10 * (attempt + 1))
    row = {"key": key, "id": q["id"], "correct": int(verdict["correct"]), "supported": int(verdict["supported"]),
           "reason": verdict["reason"], "judge_model": model, "tokens": resp.usage_metadata.total_token_count or 0}
    append_jsonl(JUDGE, row)
    # Pace by tokens: Gemma's free tier allows 16K tokens per minute.
    time.sleep(max(0.0, row["tokens"] / JUDGE_TOKENS_PER_MINUTE * 60 - (time.monotonic() - started)))
    return row


def grade(q: dict, a: dict, checks: dict) -> dict:
    """Code grades refusals of answerable questions (always wrong, makes no claims);
    the judge grades everything else, including refusals of unanswerable questions,
    because the rubric also requires that a refusal doesn't state the missing fact."""
    if checks["refused"] and q["kind"] != "unanswerable":
        return {"correct": 0, "supported": 1, "graded_by": "code", "reason": "wrong refusal", "judge_tokens": 0}
    try:
        v = judge(q, a)
    except Exception as e:  # noqa: BLE001 - quota/overload: leave ungraded, a re-run fills it in
        say(f"    {q['id']}: judge unavailable ({type(e).__name__}); left ungraded")
        return {"correct": "", "supported": "", "graded_by": "ungraded", "reason": str(e)[:200], "judge_tokens": 0}
    return {"correct": v["correct"], "supported": v["supported"], "graded_by": "judge",
            "reason": v["reason"], "judge_tokens": v["tokens"]}


def suggested_cause(q: dict, r: dict) -> str:
    """Heuristic first guess at a failure's cause; confirm or correct it by hand."""
    if q["kind"] == "unanswerable":
        if r["correct"] and r["supported"]:
            return ""
        return ("unsupported claim (refused but stated the missing fact)" if r["refused"]
                else "unsupported claim (answered an unanswerable question)")
    if r["correct"] and r["supported"] and r["citations_valid"] != 0:
        return ""
    if r["refused"]:
        return "wrong refusal" if r["expected_retrieved"] else "retrieval miss"
    if not r["correct"]:
        return "wrong answer from the right passage" if r["expected_retrieved"] else "retrieval miss"
    return "unsupported claim"


# --------------------------------------------------------------------------- human agreement

def agreement(results: list[dict]) -> dict:
    if not HUMAN.exists():
        return {}
    with HUMAN.open(newline="", encoding="utf-8") as f:
        human = {r["id"].strip(): r for r in csv.DictReader(f)
                 if (r.get("id") or "").strip() and (r.get("correct") or "").strip() in ("0", "1")}
    by_id = {r["id"]: r for r in results if r["graded_by"] != "ungraded"}
    out = {"graded_by_you": len(human)}
    disagreements = []
    for field in ("correct", "supported"):
        pairs = [(int(h[field]), int(by_id[i][field])) for i, h in human.items()
                 if i in by_id and str(h.get(field, "")).strip() in ("0", "1")]
        if not pairs:
            continue
        agree = sum(a == b for a, b in pairs) / len(pairs)
        # Cohen's kappa: agreement corrected for chance
        p_h = sum(a for a, _ in pairs) / len(pairs)
        p_j = sum(b for _, b in pairs) / len(pairs)
        pe = p_h * p_j + (1 - p_h) * (1 - p_j)
        kappa = (agree - pe) / (1 - pe) if pe < 1 else 1.0
        out[field] = {"n": len(pairs), "agreement": round(agree, 3), "kappa": round(kappa, 3)}
        disagreements += [{"id": i, "field": field, "you": h[field], "pipeline": by_id[i][field],
                           "graded_by": by_id[i]["graded_by"], "reason": by_id[i]["reason"]}
                          for i, h in human.items() if i in by_id and str(h.get(field, "")).strip() in ("0", "1")
                          and int(h[field]) != int(by_id[i][field])]
    write_csv(EVAL / "disagreements.csv", disagreements)
    return out


# --------------------------------------------------------------------------- before / after

async def before_after(questions: list[dict], answers: dict) -> dict | None:
    """eval/add_document.json: {"question_id": "q31", "path": "sources/added/xyz.pdf"}"""
    if not ADD_DOC.exists():
        return None
    out_path = EVAL / "before_after.json"
    if out_path.exists():
        return json.loads(out_path.read_text(encoding="utf-8"))
    cfg = json.loads(ADD_DOC.read_text(encoding="utf-8"))
    q = next(q for q in questions if q["id"] == cfg["question_id"])
    before = answers.get(q["id"])
    from agent import Harness
    async with Harness(approve=lambda name, args: True) as h:
        if before is None:
            before = await h.ask(q["question"])
        add = await h.session.call_tool("add_document", {"path": cfg["path"]})
        add_text = "\n".join(getattr(c, "text", "") for c in add.content)
        say(f"  add_document: {add_text}")
        if add_text.startswith("Not added"):
            say("  document not added; before/after will be retried on the next run")
            return None
        after = await h.ask(q["question"])
    result = {"question_id": q["id"], "question": q["question"], "document": cfg["path"],
              "add_document_result": add_text,
              "before": {"answer": before["answer"], "retrieved": before["retrieved"]},
              "after": {"answer": after["answer"], "retrieved": after["retrieved"]}}
    out_path.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    return result


# --------------------------------------------------------------------------- main

def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    fields = list(dict.fromkeys(k for r in rows for k in r))
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def main() -> int:
    from api_key import load_api_key
    load_api_key()
    questions = load_questions()
    if not questions:
        say("eval/questions.csv has no questions yet. Write them first (see eval/README.md).")
        return 1
    if not RUBRIC.exists():
        say("eval/rubric.md is missing: write the judge's rubric first.")
        return 1
    say(f"{len(questions)} questions: " + ", ".join(f"{sum(q['kind'] == k for q in questions)} {k}"
                                                   for k in sorted({q['kind'] for q in questions})))

    say("\n== Retrieval")
    summary = evaluate_retrieval(questions)
    for s in summary:
        say("  " + "  ".join(f"{k}={v}" for k, v in s.items()))
    if "--retrieval-only" in sys.argv:
        say("\nRetrieval only: choose SEARCH_DESIGN in retrieval.py from eval/retrieval_summary.csv,\n"
            "then run `main.py evaluate` for the end-to-end part.")
        return 0

    say(f"\n== End to end (search design: {retrieval.SEARCH_DESIGN})")
    answers = asyncio.run(run_agent_on(questions))
    sources = retrieval.known_sources()
    results = []
    for q in questions:
        a = answers.get(q["id"])
        if not a:
            continue
        checks = code_checks(q, a, sources)
        g = grade(q, a, checks)
        r = {"id": q["id"], "kind": q["kind"], "question": q["question"], **checks, **g,
             "tokens": a["tokens"]["total"], "seconds": a["seconds"], "answer": a["answer"]}
        r["suggested_cause"] = suggested_cause(q, r) if g["graded_by"] != "ungraded" else ""
        results.append(r)
    ungraded = [r["id"] for r in results if r["graded_by"] == "ungraded"]
    graded = [r for r in results if r["graded_by"] != "ungraded"]
    write_csv(EVAL / "results.csv", results)
    old_causes = {}                       # keep causes already filled in by hand across re-runs
    if (EVAL / "failures.csv").exists():
        with (EVAL / "failures.csv").open(newline="", encoding="utf-8") as f:
            old_causes = {x["id"]: x.get("cause", "") for x in csv.DictReader(f)}
    failures = [{"id": r["id"], "kind": r["kind"], "question": r["question"], "refused": r["refused"],
                 "expected_retrieved": r["expected_retrieved"], "correct": r["correct"],
                 "supported": r["supported"], "citations_valid": r["citations_valid"],
                 "suggested_cause": r["suggested_cause"], "cause": old_causes.get(r["id"], ""),
                 "reason": r["reason"]}
                for r in results if r["suggested_cause"]]
    write_csv(EVAL / "failures.csv", failures)

    ans = [r for r in graded if r["kind"] != "unanswerable"]
    una = [r for r in graded if r["kind"] == "unanswerable"]
    e2e = {
        "questions": len(questions),
        "answered_questions": len(results),
        "ungraded": ungraded,
        "correct": sum(r["correct"] for r in graded),
        "answerable_correct": sum(r["correct"] for r in ans),
        "answerable_total": len(ans),
        "unsupported": sum(1 for r in graded if not r["supported"]),
        "correct_refusals": sum(r["refused"] for r in una),
        "unanswerable_total": len(una),
        "wrong_refusals": sum(r["refused"] for r in ans),
        "invalid_citations": sum(1 for r in results if r["citations_valid"] == 0),
        "guardrail_fired": sum(r["guardrail_fired"] for r in results),
        "agent_tokens_mean": round(statistics.mean(r["tokens"] for r in results)) if results else 0,
        "judge_tokens_mean": round(statistics.mean(r["judge_tokens"] for r in results)) if results else 0,
        "seconds_mean": round(statistics.mean(r["seconds"] for r in results), 1) if results else 0,
        "seconds_median": round(statistics.median(r["seconds"] for r in results), 1) if results else 0,
    }
    say("  " + json.dumps(e2e, indent=2).replace("\n", "\n  "))

    say("\n== Judge vs your labels")
    agree = agreement(results)
    say("  " + (json.dumps(agree) if agree.get("graded_by_you") else "eval/human_labels.csv is empty"))

    say("\n== Before / after adding a document")
    ba = asyncio.run(before_after(questions, answers))
    say("  " + ("see eval/before_after.json" if ba else "eval/add_document.json not set up yet"))

    (EVAL / "summary.json").write_text(json.dumps(
        {"retrieval": summary, "end_to_end": e2e, "judge_agreement": agree,
         "search_design": retrieval.SEARCH_DESIGN, "before_after": bool(ba)}, indent=2), encoding="utf-8")
    say("\nWrote eval/retrieval_summary.csv, retrieval_results.csv, results.csv, failures.csv, summary.json")
    return 0


if __name__ == "__main__":
    try:
        sys.exit(main())
    except index.QuotaExhausted:
        say("\nDaily Gemini embedding quota reached. Everything done so far is saved in eval/ and index/;\n"
            "run `main.py evaluate` again after the reset (09:00 in Spain) to continue.")
        sys.exit(2)
