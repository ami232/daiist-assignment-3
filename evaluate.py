"""
Assignment 3: evaluation (`main.py evaluate`).

1. Retrieval: hit rate at 1/3/5 for each chunking design (a = structure, b = fixed), and
   the top similarity score of answerable vs unanswerable questions.
2. End to end: the agent (agent.py) answers every question in eval/questions.csv.
3. Code checks: refusal where expected, citations valid (retrieved in this run), cites the
   expected source/location, expected passage retrieved at all.
4. LLM judge with a rubric, the retrieved text as evidence: correct (1/0), supported (1/0).
5. Agreement between the judge and eval/human_labels.csv.
6. Add-document demo: on a copy of the index, add Regulation (EU) 2026/2202 (with approval)
   and ask the demo question again, before vs after.

Agent answers and judge verdicts are cached in eval/*.jsonl so a rerun only spends quota
on new or changed questions (--fresh reruns everything). Results are written to eval/.

    uv run python main.py evaluate                # everything
    uv run python evaluate.py --limit 3 --skip-demo   # quick try
"""

import argparse
import asyncio
import csv
import hashlib
import json
import shutil
import statistics
import sys
import time
from pathlib import Path

import index

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
HUMAN_LABELS = EVAL / "human_labels.csv"
ANSWERS = EVAL / "agent_answers.jsonl"
VERDICTS = EVAL / "judge_verdicts.jsonl"
KS = (1, 3, 5)

JUDGE_MODELS = ["gemini-3.5-flash", "gemini-3.5-flash-lite"]  # stronger judge first; fallback if overloaded
_JUDGE_MISSES: dict[str, int] = {}
DEMO_QUESTION_ID = "q35"
DEMO_CELEX = "32026R2202"
DEMO_CHROMA = index.INDEX_DIR / "chroma_with_reg_2026_2202"


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


def load_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def split(cell: str) -> list[str]:
    return [x.strip() for x in cell.split(";") if x.strip()]


def unanswerable(q: dict) -> bool:
    return q["kind"].strip().lower() == "unanswerable"


def digest(*parts: str) -> str:
    return hashlib.sha1("\x1f".join(parts).encode()).hexdigest()[:16]


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def read_jsonl(path: Path) -> dict:
    if not path.exists():
        return {}
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return {r["key"]: r for r in rows}


def append_jsonl(path: Path, row: dict) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


# --------------------------------------------------------------------------- 1. retrieval

def matches(chunk: dict, sources: list[str], locations: list[str]) -> set[str]:
    """The expected locations this chunk covers (empty set = not a hit).
    A chunk covers a location when it comes from one of the expected documents and
    that label is among the sections the chunk contains (metadata 'locations')."""
    meta = chunk["metadata"]
    if meta["doc_id"] not in sources:
        return set()
    return set(meta["locations"].split("; ")) & set(locations)


def retrieval_eval(questions: list[dict]) -> tuple[list[dict], dict]:
    rows, summary = [], {}
    answerable = [q for q in questions if not unanswerable(q)]
    for design in index.DESIGNS:
        hits = {k: [] for k in KS}  # any expected location in top k
        full = {k: [] for k in KS}  # every expected location in top k (differs only for multi)
        labels_per_hit = []
        top_answerable, top_unanswerable = [], []
        for q in questions:
            results = index.search(q["question"], design, k=max(KS))
            top = f'{results[0]["metadata"]["doc_id"]} | {results[0]["metadata"]["location"]}'
            if unanswerable(q):
                top_unanswerable.append(results[0]["score"])
                rows.append({"design": design, "id": q["id"], "kind": q["kind"], "first_hit_rank": "",
                             "top_score": results[0]["score"], "top_location": top})
                continue
            top_answerable.append(results[0]["score"])
            sources, locations = split(q["expected_source"]), split(q["expected_location"])
            covered_by_rank = [matches(r, sources, locations) for r in results]
            first = next((i + 1 for i, c in enumerate(covered_by_rank) if c), None)
            for k in KS:
                covered = set().union(*covered_by_rank[:k])
                hits[k].append(bool(covered))
                full[k].append(covered == set(locations))
            if first:
                labels_per_hit.append(len(results[first - 1]["metadata"]["locations"].split("; ")))
            rows.append({"design": design, "id": q["id"], "kind": q["kind"], "first_hit_rank": first or "miss",
                         "top_score": results[0]["score"], "top_location": top})
        summary[design] = {
            "name": index.DESIGNS[design],
            **{f"hit@{k}": round(sum(hits[k]) / len(answerable), 3) for k in KS},
            **{f"all_locations@{k}": round(sum(full[k]) / len(answerable), 3) for k in KS},
            "sections_per_hit_chunk": round(statistics.mean(labels_per_hit), 2) if labels_per_hit else None,
            "top_score_answerable_median": round(statistics.median(top_answerable), 3),
            "top_score_unanswerable_median": round(statistics.median(top_unanswerable), 3),
            "top_score_unanswerable_max": round(max(top_unanswerable), 3),
            "top_score_answerable_min": round(min(top_answerable), 3),
        }
    return rows, summary


# --------------------------------------------------------------------------- 2. agent

async def ask_with_retry(h, q: dict, waits=(20, 60, 120)) -> dict:
    """Gemini models are sometimes overloaded (503): wait and ask the same question again."""
    for wait in (*waits, None):
        try:
            return await h.ask(q["question"])
        except Exception as e:  # noqa: BLE001
            if wait is None or not any(s in str(e) for s in ("503", "UNAVAILABLE", "429", "500")):
                raise
            log(f"agent: {q['id']} got {str(e)[:60]}...; retrying in {wait} s")
            await asyncio.sleep(wait)


async def run_agent(questions: list[dict], fresh: bool) -> dict:
    """id -> agent result, answering only questions not cached yet."""
    import agent

    cache = {} if fresh else read_jsonl(ANSWERS)
    if fresh and ANSWERS.exists():
        ANSWERS.unlink()
    results, todo = {}, []
    for q in questions:
        key = digest(q["id"], q["question"], agent.MODEL, agent.SYSTEM_PROMPT)
        if key in cache:
            results[q["id"]] = cache[key]["result"]
        else:
            todo.append((q, key))
    log(f"agent: {len(results)} answers cached, {len(todo)} to run")
    if not todo:
        return results
    failures = 0
    async with agent.Harness(approve=lambda name, args: False) as h:
        for n, (q, key) in enumerate(todo, 1):
            try:
                result = await ask_with_retry(h, q)
            except Exception as e:  # noqa: BLE001 - record it, keep the rest of the run
                failures += 1
                log(f"agent: {q['id']} failed: {type(e).__name__}: {str(e)[:200]}")
                if failures >= 3:
                    log("agent: 3 failures in a row (quota or outage?); stopping, rerun later to continue")
                    break
                continue
            failures = 0
            results[q["id"]] = result
            append_jsonl(ANSWERS, {"key": key, "id": q["id"], "result": result})
            log(f"agent: {n}/{len(todo)} {q['id']} {result['seconds']} s, {result['searches']} searches, "
                f"refusal={result['refusal']}, citations={result['guardrail']}")
    return results


# --------------------------------------------------------------------------- 3. code checks

def code_checks(q: dict, r: dict) -> dict:
    from agent import base_label, retrieved_passages

    expected_refusal = unanswerable(q)
    retrieved = set(retrieved_passages(r["trace"]))
    expected = {(s, base_label(loc)) for s in split(q["expected_source"]) for loc in split(q["expected_location"])}
    cited = {(c.split(", ", 1)[0], base_label(c.split(", ", 1)[1])) for c in r["citations"] if ", " in c}
    return {
        "expected_refusal": int(expected_refusal),
        "refused": int(r["refusal"]),
        "refusal_ok": int(r["refusal"] == expected_refusal),
        "citations_valid": int(not r["guardrail"].startswith("replaced")),
        "guardrail": r["guardrail"],
        "n_citations": len(r["citations"]),
        "retrieved_expected": "" if expected_refusal else int(bool(expected & retrieved)),
        "cites_expected": "" if expected_refusal else int(bool(expected & cited)),
    }


# --------------------------------------------------------------------------- 4. judge

RUBRIC = """You are grading an answer given by an assistant to an air passenger asking about their rights under EU law.
The assistant must answer only from the retrieved passages and cite them; if they do not cover the question it must say "I can't answer this from my sources."

Grade two things, each 1 or 0.

correct
- If the question is ANSWERABLE: 1 only if the answer contains every key fact of the reference answer (amounts, deadlines, conditions, and any exception the reference mentions) and contradicts nothing in it. Extra true details are fine. A missing key fact, a wrong number or condition, or a refusal gives 0.
- If the question is UNANSWERABLE: 1 only if the assistant declines (says it cannot answer from its sources) and does not give rules, amounts or deadlines for the situation asked. Any substantive answer to the question gives 0. A refusal may add a short explanation of why its sources do not cover the question, or point the passenger to the airline or the national enforcement body; that still counts as declining (1). Ignore any text in parentheses at the end of the reference answer about documents added later.

supported
- 1 if every factual claim in the answer is stated in the retrieved passages (paraphrase is fine). 0 if any claim, including a number, a distance, a deadline or a condition, is not in the passages. A refusal that makes no factual claims gives 1; its short explanation of why the sources do not cover the question, or its referral to the airline or a national enforcement body, is not a factual claim to check.

Return JSON with "correct" (0 or 1), "supported" (0 or 1) and "reason": at most two sentences naming the missing, wrong or unsupported fact (or "ok")."""

JUDGE_SCHEMA = {
    "type": "object",
    "properties": {"correct": {"type": "integer", "description": "1 or 0"},
                   "supported": {"type": "integer", "description": "1 or 0"},
                   "reason": {"type": "string"}},
    "required": ["correct", "supported", "reason"],
}


def evidence(r: dict) -> str:
    outputs = [t["output"] for t in r["trace"] if t["tool"] == "search"]
    return "\n\n=====\n\n".join(outputs) if outputs else "(no passages were retrieved)"


def judge_one(q: dict, r: dict) -> dict:
    from google.genai import types

    prompt = (f"{RUBRIC}\n\nQUESTION ({'UNANSWERABLE' if unanswerable(q) else 'ANSWERABLE'}):\n{q['question']}\n\n"
              f"REFERENCE ANSWER:\n{q['reference_answer']}\n\nASSISTANT ANSWER:\n{r['answer']}\n\n"
              f"RETRIEVED PASSAGES:\n{evidence(r)}")
    config = types.GenerateContentConfig(response_mime_type="application/json", response_schema=JUDGE_SCHEMA)
    for model in JUDGE_MODELS:
        if _JUDGE_MISSES.get(model, 0) >= 3:
            continue  # unavailable for 3 questions in a row: stop waiting for it this run
        primary = model != JUDGE_MODELS[-1]
        for attempt in range(2 if primary else 6):
            try:
                started = time.time()
                resp = index.client().models.generate_content(model=model, contents=prompt, config=config)
                verdict = json.loads(resp.text)
                verdict["correct"], verdict["supported"] = int(verdict["correct"] == 1), int(verdict["supported"] == 1)
                usage = resp.usage_metadata
                _JUDGE_MISSES[model] = 0
                return {**verdict, "judge_model": model, "judge_seconds": round(time.time() - started, 1),
                        "judge_tokens": (usage.total_token_count or 0) if usage else 0}
            except Exception as e:  # noqa: BLE001
                msg = str(e)
                if "per day" in msg.lower() or "PerDay" in msg:
                    break  # daily quota for this model: try the next one
                if any(code in msg for code in ("429", "500", "503", "UNAVAILABLE", "RESOURCE_EXHAUSTED")) or \
                        isinstance(e, json.JSONDecodeError):
                    time.sleep(min(60, 5 * 2 ** attempt))
                    continue
                raise
        _JUDGE_MISSES[model] = _JUDGE_MISSES.get(model, 0) + 1
        log(f"judge: {model} unavailable for {q['id']}"
            + (" (3 in a row: skipping it for the rest of this run)" if _JUDGE_MISSES[model] >= 3 else ""))
    raise RuntimeError(f"no judge model available for {q['id']}")


def run_judge(questions: list[dict], answers: dict, fresh: bool) -> dict:
    cache = {} if fresh else read_jsonl(VERDICTS)
    if fresh and VERDICTS.exists():
        VERDICTS.unlink()
    verdicts = {}
    # Human-graded questions first: the primary judge model has a small daily quota (20 requests on the
    # free tier), so it goes to the answers whose verdicts are compared with the human labels.
    graded = {row["id"] for row in read_human_labels()}
    for q in sorted(questions, key=lambda q: q["id"] not in graded):
        r = answers.get(q["id"])
        if r is None:
            continue
        key = digest(q["id"], q["question"], q["reference_answer"], r["answer"], RUBRIC)
        if key in cache:
            verdicts[q["id"]] = cache[key]["verdict"]
            continue
        try:
            v = judge_one(q, r)
        except Exception as e:  # noqa: BLE001
            log(f"judge: {q['id']} failed: {type(e).__name__}: {str(e)[:200]}")
            continue
        verdicts[q["id"]] = v
        append_jsonl(VERDICTS, {"key": key, "id": q["id"], "verdict": v})
        log(f"judge: {q['id']} correct={v['correct']} supported={v['supported']} ({v['judge_model']})")
    return verdicts


# --------------------------------------------------------------------------- 5. agreement

def kappa(a: list[int], b: list[int]) -> float | None:
    n = len(a)
    if n == 0:
        return None
    po = sum(x == y for x, y in zip(a, b)) / n
    pa, pb = sum(a) / n, sum(b) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return round((po - pe) / (1 - pe), 3) if pe < 1 else None


def read_human_labels() -> list[dict]:
    if not HUMAN_LABELS.exists():
        return []
    with HUMAN_LABELS.open(newline="", encoding="utf-8") as f:
        return [{**r, "id": (r.get("id") or "").strip()} for r in csv.DictReader(f) if (r.get("id") or "").strip()]


def agreement(verdicts: dict) -> dict:
    if not HUMAN_LABELS.exists():
        return {"graded": 0}
    labels = [r for r in read_human_labels() if r["id"] in verdicts]
    out = {"graded": len(labels)}
    for field in ("correct", "supported"):
        pairs = [(int(r[field]), int(verdicts[r["id"]][field])) for r in labels if r[field].strip() in {"0", "1"}]
        human, judge = [p[0] for p in pairs], [p[1] for p in pairs]
        out[field] = {
            "n": len(pairs),
            "agreement": round(sum(h == j for h, j in pairs) / len(pairs), 3) if pairs else None,
            "cohen_kappa": kappa(human, judge),
            "disagreements": [r["id"] for r in labels if r[field].strip() in {"0", "1"}
                              and int(r[field]) != int(verdicts[r["id"]][field])],
        }
    return out


# --------------------------------------------------------------------------- 6. add-document demo

async def demo(questions: list[dict], answers: dict) -> dict | None:
    import agent

    q = next((q for q in questions if q["id"] == DEMO_QUESTION_ID), None)
    if q is None or q["id"] not in answers:
        log("demo: no demo question or no 'before' answer; skipped")
        return None
    source = index.CORPUS_DIR / f"{DEMO_CELEX}.html"
    if not source.exists():
        index.download(DEMO_CELEX)
    if not DEMO_CHROMA.exists():  # a copy, so the committed base index keeps matching the test set
        shutil.copytree(index.CHROMA_DIR, DEMO_CHROMA)
    approvals = []

    def approve(name: str, args: dict) -> bool:
        approvals.append(f"{name}({args}) -> approved by evaluate.py for the demo")
        return True

    async with agent.Harness(approve=approve, server_env={"CORPUS_CHROMA_DIR": str(DEMO_CHROMA)}) as h:
        added = await h.ask(f"Please add the document {source.relative_to(ROOT)} to the corpus.")
        after = await h.ask(q["question"])
    before = answers[q["id"]]
    add_output = next((t["output"] for t in added["trace"] if t["tool"] == "add_document"), "(not called)")
    lines = [
        "# Add-document demo",
        "",
        f"Question {q['id']} (unanswerable with the base corpus): {q['question']}",
        "",
        "## Before (base index)",
        "", before["answer"], "",
        f"Citations: {', '.join(before['citations']) or 'none'}",
        "",
        f"## Adding {source.name} (on a copy of the index: {DEMO_CHROMA.relative_to(ROOT)})",
        "", *(f"- approval: {a}" for a in approvals), "", "```", add_output, "```",
        "",
        "## After",
        "", after["answer"], "",
        f"Citations: {', '.join(after['citations']) or 'none'}",
        f"Citation check: {after['guardrail']}",
    ]
    (EVAL / "add_document_demo.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    return {"question": q["id"], "before_refused": before["refusal"], "after_refused": after["refusal"],
            "after_citations": after["citations"], "approvals": approvals}


# --------------------------------------------------------------------------- report

def failure_hint(q: dict, c: dict, v: dict | None) -> str:
    """A first guess at the failure type for the analysis; the final classification is manual."""
    if v is None:
        return "not judged"
    if v["correct"] and v["supported"] and c["refusal_ok"]:
        return ""
    if unanswerable(q):
        return "" if c["refused"] else "answered an unanswerable question (unsupported claim?)"
    if c["refused"]:
        return "wrong refusal" + ("" if c["retrieved_expected"] else " after a retrieval miss")
    if not c["retrieved_expected"]:
        return "retrieval miss (or bad test question)"
    if not v["supported"]:
        return "unsupported claim"
    return "wrong answer from the right passage (or bad test question)"


def retrieved_list(r: dict) -> list[str]:
    """'source_id | location' of every passage the agent's searches returned, in order, no repeats."""
    from agent import HEADER_RE

    seen = []
    for t in r["trace"]:
        if t["tool"] == "search":
            for line in t["output"].splitlines():
                if (m := HEADER_RE.match(line)) and f"{m[1]} | {m[2]}" not in seen:
                    seen.append(f"{m[1]} | {m[2]}")
    return seen


def rate(values: list) -> float | None:
    values = [int(x) for x in values if x != ""]
    return round(sum(values) / len(values), 3) if values else None


def main() -> int:
    parser = argparse.ArgumentParser(description="Assignment 3 evaluation")
    parser.add_argument("--fresh", action="store_true", help="ignore cached answers and verdicts")
    parser.add_argument("--limit", type=int, help="only the first N questions (for a quick try)")
    parser.add_argument("--skip-demo", action="store_true", help="skip the add-document demo")
    parser.add_argument("--retrieval-only", action="store_true")
    args = parser.parse_args()

    questions = load_questions()
    try:
        rows, retrieval = retrieval_eval(questions)
    except index.QuotaExhausted as e:
        log(f"Embedding quota exhausted: {e}")
        return 1
    write_csv(EVAL / "retrieval_results.csv", rows)
    (EVAL / "retrieval_summary.json").write_text(json.dumps(retrieval, indent=2))
    print("Retrieval hit rate (answerable questions):")
    for d, s in retrieval.items():
        print(f"  design {d} ({s['name']}): @1 {s['hit@1']:.1%}  @3 {s['hit@3']:.1%}  @5 {s['hit@5']:.1%}")
    if args.retrieval_only:
        return 0

    selected = questions[:args.limit] if args.limit else questions
    answers = asyncio.run(run_agent(selected, args.fresh))
    verdicts = run_judge(selected, answers, args.fresh)

    results, grading = [], []
    for q in selected:
        r = answers.get(q["id"])
        if r is None:
            continue
        c = code_checks(q, r)
        v = verdicts.get(q["id"])
        results.append({
            "id": q["id"], "kind": q["kind"], **c,
            "judge_correct": v["correct"] if v else "", "judge_supported": v["supported"] if v else "",
            "judge_reason": v["reason"] if v else "", "failure_hint": failure_hint(q, c, v),
            "searches": r["searches"], "model_calls": r["model_calls"],
            "input_tokens": r["input_tokens"], "output_tokens": r["output_tokens"], "seconds": r["seconds"],
            "answer": r["answer"],
        })
        grading.append({"id": q["id"], "kind": q["kind"], "question": q["question"],
                        "reference_answer": q["reference_answer"], "answer": r["answer"],
                        "citations": "; ".join(r["citations"]),
                        "retrieved": "; ".join(retrieved_list(r))})
    if not results:
        log("No agent answers yet; nothing to summarise.")
        return 1
    write_csv(EVAL / "results.csv", results)
    write_csv(EVAL / "grading_sheet.csv", grading)

    ans = [x for x in results if not x["expected_refusal"]]
    una = [x for x in results if x["expected_refusal"]]
    secs = [x["seconds"] for x in results]
    tokens = [x["input_tokens"] + x["output_tokens"] for x in results]
    judge_tokens = [v.get("judge_tokens", 0) for v in verdicts.values()]
    summary = {
        "questions": len(results),
        "answerable": {
            "n": len(ans),
            "judge_correct": rate([x["judge_correct"] for x in ans]),
            "judge_supported": rate([x["judge_supported"] for x in ans]),
            "wrong_refusals": sum(x["refused"] for x in ans),
            "cites_expected_source_location": rate([x["cites_expected"] for x in ans]),
            "expected_passage_retrieved": rate([x["retrieved_expected"] for x in ans]),
        },
        "unanswerable": {
            "n": len(una),
            "correct_refusals": sum(x["refused"] for x in una),
            "answered_anyway": sum(1 - x["refused"] for x in una),
            "judge_correct": rate([x["judge_correct"] for x in una]),
        },
        "citations": {
            "answers_with_valid_citations": rate([x["citations_valid"] for x in results]),
            "guardrail": {g: sum(1 for x in results if x["guardrail"].split(" ")[0] == g)
                          for g in ("passed", "corrected", "replaced", "skipped")},
        },
        "cost_per_question": {
            "seconds_mean": round(statistics.mean(secs), 1),
            "seconds_median": round(statistics.median(secs), 1),
            "agent_tokens_mean": round(statistics.mean(tokens)),
            "agent_tokens_median": round(statistics.median(tokens)),
            "judge_tokens_mean": round(statistics.mean(judge_tokens)) if judge_tokens else None,
            "searches_mean": round(statistics.mean(x["searches"] for x in results), 2),
        },
        "judge_models": {m: sum(1 for v in verdicts.values() if v.get("judge_model") == m)
                         for m in sorted({v.get("judge_model") for v in verdicts.values()})},
        "judge_vs_human": agreement(verdicts),
        "failure_hints": {h: sum(1 for x in results if x["failure_hint"] == h)
                          for h in sorted({x["failure_hint"] for x in results}) if h},
    }
    if not args.skip_demo and not args.limit:
        summary["add_document_demo"] = asyncio.run(demo(questions, answers))
    (EVAL / "summary.json").write_text(json.dumps(summary, indent=2))
    print("\nEnd-to-end:")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
