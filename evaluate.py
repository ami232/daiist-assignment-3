"""
Assignment 3: evaluation (`main.py evaluate`).

1. Retrieval: hit rate at k = 1, 3, 5 for each design (dense, hybrid) on the
   answerable questions, plus words each design adds to the prompt (k = 5).
2. End to end: the agent answers every question in eval/questions.csv.
3. Code checks: citations valid (cited passages were really retrieved), cites an
   expected source, refusal detection (right / wrong refusals).
4. LLM judge with a rubric and the retrieved text as evidence: correct, supported.
5. Agreement between the judge and eval/human_labels.csv.

Everything is cached in eval/ (query vectors, answers, verdicts) so a re-run
spends no quota unless the questions, AGENTS.md, the model or the rubric change.

Outputs
  eval/retrieval.csv            hit rates per design and k
  eval/answers.jsonl            agent answers with tool trace
  eval/answers_for_grading.csv  answers WITHOUT verdicts, for your own grading
  eval/verdicts.jsonl           judge verdicts
  eval/results.csv              one row per question: checks + verdict + cost
  eval/summary.json             headline numbers
"""

from __future__ import annotations

import asyncio
import csv
import hashlib
import json
import sys
import time
from pathlib import Path

import agent as agent_mod
import index
import retrieval

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
HUMAN = EVAL / "human_labels.csv"
DESIGNS = ["dense", "hybrid"]
KS = [1, 3, 5]
JUDGE_MODEL = "gemini-3.1-flash-lite"  # different model from the agent, to reduce self-grading bias

# DRAFT rubric: rewrite it in your own words (the brief says the rubric is your decision).
RUBRIC = """You grade answers from a food-safety assistant that must answer only from FDA passages.

You get: the question, its kind (single / multi / unanswerable), a reference answer, the
assistant's answer, and the passages the assistant retrieved (the evidence).

correct = 1 if
  - answerable question: the answer gives the key facts of the reference answer (numbers,
    time limits, yes/no) without contradicting it. Extra correct detail is fine. For "multi"
    questions both parts of the reference must be covered.
  - unanswerable question: the answer clearly says the documents do not cover it and does
    not give a specific answer to the question (general advice like "when in doubt, throw
    it out" is fine).
  otherwise correct = 0. A refusal on an answerable question is correct = 0.

supported = 1 if every factual claim in the answer is stated in the evidence passages
  (paraphrase is fine). A refusal with no claims is supported = 1. Any claim not found in
  the evidence (from general knowledge or invented) gives supported = 0.

Reply with JSON only: {"correct": 0 or 1, "supported": 0 or 1, "reason": "one sentence"}"""


def log(*a) -> None:
    print(*a, file=sys.stderr, flush=True)


def sha(*parts: str) -> str:
    return hashlib.sha1("\n".join(parts).encode()).hexdigest()[:12]


def read_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r["question"].strip()]


def expected_pairs(q: dict) -> list[tuple[str, str]]:
    """[(source, location substring)], paired by position (';'-separated)."""
    srcs = [s.strip() for s in q["expected_source"].split(";") if s.strip()]
    locs = [s.strip() for s in q["expected_location"].split(";")]
    return [(s, locs[i] if i < len(locs) else "") for i, s in enumerate(srcs)]


def matches(hit: dict, pair: tuple[str, str]) -> bool:
    src, loc = pair
    return hit["source"] == src and (not loc or loc.lower() in hit["location"].lower())


def load_jsonl(path: Path) -> dict:
    if not path.exists():
        return {}
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return {r["id"]: r for r in rows}


def save_jsonl(path: Path, rows: dict) -> None:
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows.values()), encoding="utf-8")


# --------------------------------------------------------------------------- #
# 1. Retrieval
# --------------------------------------------------------------------------- #
def query_vectors(questions: list[dict]) -> dict[str, list[float]]:
    """Embed each question once; cached in eval/query_vectors.json."""
    path = EVAL / "query_vectors.json"
    cache = json.loads(path.read_text()) if path.exists() else {}
    for q in questions:
        key = sha(index.EMBED_MODEL, q["question"])
        if key not in cache:
            cache[key] = index.embed_query(q["question"])
            path.write_text(json.dumps(cache))
    return {q["id"]: cache[sha(index.EMBED_MODEL, q["question"])] for q in questions}


def evaluate_retrieval(questions: list[dict]) -> list[dict]:
    answerable = [q for q in questions if q["kind"].strip().lower() != "unanswerable"]
    vecs = query_vectors(answerable)
    r = retrieval.Retriever()
    rows, per_question = [], []
    for design in DESIGNS:
        hits_at = {k: 0 for k in KS}
        all_at5, words = 0, 0
        for q in answerable:
            hits = r.search(q["question"], k=max(KS), design=design, query_vector=vecs[q["id"]])
            pairs = expected_pairs(q)
            first = next((i for i, h in enumerate(hits) if any(matches(h, p) for p in pairs)), None)
            for k in KS:
                hits_at[k] += first is not None and first < k
            all_at5 += all(any(matches(h, p) for h in hits) for p in pairs)
            words += sum(len(h["text"].split()) for h in hits)
            per_question.append({"design": design, "id": q["id"], "kind": q["kind"],
                                 "first_hit_rank": "" if first is None else first + 1,
                                 "top5": " || ".join(f"{h['source']} | {h['location']}" for h in hits)})
        n = len(answerable)
        row = {"design": design, "n": n, **{f"hit@{k}": round(hits_at[k] / n, 3) for k in KS},
               "all_passages@5": round(all_at5 / n, 3), "avg_words_in_prompt@5": round(words / n)}
        rows.append(row)
        log(f"  {design:7s} " + "  ".join(f"hit@{k}={row[f'hit@{k}']:.2f}" for k in KS)
            + f"  all@5={row['all_passages@5']:.2f}  words={row['avg_words_in_prompt@5']}")
    write_csv(EVAL / "retrieval.csv", rows)
    write_csv(EVAL / "retrieval_per_question.csv", per_question)
    return rows


# --------------------------------------------------------------------------- #
# 2. Agent answers
# --------------------------------------------------------------------------- #
async def run_agent(questions: list[dict]) -> dict:
    path = EVAL / "answers.jsonl"
    cache = load_jsonl(path)
    version = sha(agent_mod.MODEL, (ROOT / "AGENTS.md").read_text(), retrieval.DEFAULT_DESIGN)
    todo = [q for q in questions
            if cache.get(q["id"], {}).get("version") != version or cache[q["id"]]["question"] != q["question"]]
    if todo:
        log(f"Agent: answering {len(todo)} question(s) ...")
        async with agent_mod.CorpusAgent(approve=lambda path: False) as ag:
            for q in todo:
                try:
                    r = await ag.ask(q["question"])
                except Exception as e:  # noqa: BLE001 - record and continue
                    log(f"  {q['id']} failed: {type(e).__name__}: {str(e)[:200]}")
                    if "PerDay" in str(e):
                        log("  Daily request quota for the agent model reached; run again tomorrow "
                            "(answers so far are saved).")
                        break
                    continue
                cache[q["id"]] = {"id": q["id"], "version": version, **r}
                save_jsonl(path, cache)
                log(f"  {q['id']} done ({r['seconds']} s, {r['tokens_in'] + r['tokens_out']} tokens)")
    return cache


# --------------------------------------------------------------------------- #
# 3. Code checks
# --------------------------------------------------------------------------- #
def code_checks(q: dict, a: dict) -> dict:
    retrieved = {(s.strip(), l.strip()) for t in a["trace"] if t["tool"] == "search"
                 for s, l in agent_mod.RESULT_HEADER.findall(t["output"])}
    cited = [tuple(c.split(" | ", 1)) for c in a["citations"]]
    refusal = bool(agent_mod.REFUSAL.search(a["answer"])) or a["guardrail"]["withheld"]
    unanswerable = q["kind"].strip().lower() == "unanswerable"
    pairs = expected_pairs(q)
    retrieved_hits = [{"source": s, "location": l} for s, l in retrieved]
    return {
        "n_citations": len(cited),
        "citations_valid": int(all((c[0], agent_mod.PART.sub("", c[1])) in
                                   {(s, agent_mod.PART.sub("", l)) for s, l in retrieved} for c in cited)),
        "cites_expected_source": "" if unanswerable else int(any(
            matches({"source": s, "location": l}, p) for s, l in cited for p in pairs)),
        "expected_retrieved": "" if unanswerable else int(any(
            matches(h, p) for h in retrieved_hits for p in pairs)),
        "refused": int(refusal),
        "right_refusal": int(unanswerable and refusal) if unanswerable else "",
        "wrong_refusal": int(refusal) if not unanswerable else "",
        "guardrail_fired": int(a["guardrail"]["fired"]),
        "withheld": int(a["guardrail"]["withheld"]),
    }


# --------------------------------------------------------------------------- #
# 4. LLM judge
# --------------------------------------------------------------------------- #
def judge(questions: list[dict], answers: dict) -> dict:
    from google.genai import types

    path = EVAL / "verdicts.jsonl"
    cache = load_jsonl(path)
    client = index.genai_client()
    for q in questions:
        a = answers.get(q["id"])
        if not a:
            continue
        evidence = "\n\n".join(t["output"] for t in a["trace"] if t["tool"] == "search") or "(no passages retrieved)"
        version = sha(JUDGE_MODEL, RUBRIC, a["answer"], q["reference_answer"])
        if cache.get(q["id"], {}).get("version") == version:
            continue
        prompt = (f"QUESTION: {q['question']}\nKIND: {q['kind']}\nREFERENCE ANSWER: {q['reference_answer']}\n\n"
                  f"ASSISTANT ANSWER:\n{a['answer']}\n\nEVIDENCE PASSAGES:\n{evidence}")
        for attempt in range(4):
            try:
                r = client.models.generate_content(
                    model=JUDGE_MODEL, contents=prompt,
                    config=types.GenerateContentConfig(system_instruction=RUBRIC, temperature=0,
                                                       response_mime_type="application/json"))
                v = json.loads(r.text)
                break
            except Exception as e:  # noqa: BLE001
                log(f"  judge retry {attempt + 1} for {q['id']}: {str(e)[:150]}")
                time.sleep(20 * (attempt + 1))
        else:
            continue
        cache[q["id"]] = {"id": q["id"], "version": version, "correct": int(v.get("correct", 0)),
                          "supported": int(v.get("supported", 0)), "reason": v.get("reason", "")}
        save_jsonl(path, cache)
    return cache


# --------------------------------------------------------------------------- #
# 5. Agreement with human labels
# --------------------------------------------------------------------------- #
GRADING = EVAL / "grading_sheet.csv"
GRADE_COLS = ["id", "correct", "supported", "notes"]


def make_grading_sheet(questions: list[dict], answers: dict) -> None:
    """Create eval/grading_sheet.csv once (never overwritten): answers without verdicts,
    with empty correct/supported/notes columns for your own grades."""
    if GRADING.exists():
        return
    rows = [{"id": q["id"], "correct": "", "supported": "", "notes": "", "kind": q["kind"],
             "question": q["question"], "reference_answer": q["reference_answer"],
             "agent_answer": answers[q["id"]]["answer"]}
            for q in questions if q["id"] in answers]
    write_csv(GRADING, rows)


def sync_human_labels() -> None:
    """Copy the graded rows of the grading sheet into eval/human_labels.csv (brief's format)."""
    if not GRADING.exists():
        return
    with GRADING.open(newline="", encoding="utf-8-sig") as f:
        graded = [r for r in csv.DictReader(f)
                  if (r.get("correct") or "").strip() in ("0", "1") and (r.get("supported") or "").strip() in ("0", "1")]
    if graded:
        write_csv(HUMAN, [{c: (r.get(c) or "").strip() for c in GRADE_COLS} for r in graded])
# --------------------------------------------------------------------------- #
def agreement(verdicts: dict) -> dict:
    if not HUMAN.exists():
        return {"n": 0}
    with HUMAN.open(newline="", encoding="utf-8") as f:
        labels = [r for r in csv.DictReader(f) if (r.get("id") or "").strip() and r["id"] in verdicts]
    out = {"n": len(labels)}
    for field in ("correct", "supported"):
        pairs = [(int(r[field]), verdicts[r["id"]][field]) for r in labels if r.get(field, "").strip() in ("0", "1")]
        if not pairs:
            continue
        agree = sum(h == j for h, j in pairs) / len(pairs)
        ph, pj = sum(h for h, _ in pairs) / len(pairs), sum(j for _, j in pairs) / len(pairs)
        pe = ph * pj + (1 - ph) * (1 - pj)
        kappa = (agree - pe) / (1 - pe) if pe < 1 else 1.0
        out[field] = {"n": len(pairs), "agreement": round(agree, 3), "cohen_kappa": round(kappa, 3),
                      "disagreements": [r["id"] for r in labels
                                        if r.get(field, "").strip() in ("0", "1")
                                        and int(r[field]) != verdicts[r["id"]][field]]}
    return out


# --------------------------------------------------------------------------- #
def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def main() -> None:
    questions = read_questions()
    log(f"{len(questions)} questions")

    log("1. Retrieval hit rates")
    retrieval_rows = evaluate_retrieval(questions)

    log("2. Agent answers")
    answers = asyncio.run(run_agent(questions))
    write_csv(EVAL / "answers_for_grading.csv", [
        {"id": q["id"], "kind": q["kind"], "question": q["question"], "reference_answer": q["reference_answer"],
         "answer": answers[q["id"]]["answer"],
         "retrieved_passages": " || ".join(sorted({f"{s} | {l}" for t in answers[q["id"]]["trace"]
                                                   if t["tool"] == "search"
                                                   for s, l in agent_mod.RESULT_HEADER.findall(t["output"])}))}
        for q in questions if q["id"] in answers])

    make_grading_sheet(questions, answers)
    sync_human_labels()

    log("3-4. Code checks and LLM judge")
    verdicts = judge(questions, answers)

    results = []
    for q in questions:
        a = answers.get(q["id"])
        if not a:
            continue
        v = verdicts.get(q["id"], {})
        results.append({"id": q["id"], "kind": q["kind"], **code_checks(q, a),
                        "judge_correct": v.get("correct", ""), "judge_supported": v.get("supported", ""),
                        "judge_reason": v.get("reason", ""), "tool_calls": len(a["trace"]),
                        "tokens": a["tokens_in"] + a["tokens_out"], "seconds": a["seconds"]})
    write_csv(EVAL / "results.csv", results)

    ans = [r for r in results if r["kind"].strip().lower() != "unanswerable"]
    una = [r for r in results if r["kind"].strip().lower() == "unanswerable"]
    mean = lambda xs: round(sum(xs) / len(xs), 3) if xs else None  # noqa: E731
    summary = {
        "questions": len(questions), "answered": len(results),
        "retrieval": retrieval_rows,
        "chosen_design": retrieval.DEFAULT_DESIGN,
        "end_to_end": {
            "correct": mean([r["judge_correct"] for r in results if r["judge_correct"] != ""]),
            "correct_answerable": mean([r["judge_correct"] for r in ans if r["judge_correct"] != ""]),
            "supported": mean([r["judge_supported"] for r in results if r["judge_supported"] != ""]),
            "unsupported_count": sum(1 for r in results if r["judge_supported"] == 0),
            "right_refusals": f"{sum(r['right_refusal'] for r in una)}/{len(una)}",
            "wrong_refusals": f"{sum(r['wrong_refusal'] for r in ans)}/{len(ans)}",
            "citations_valid": mean([r["citations_valid"] for r in results]),
            "cites_expected_source": mean([r["cites_expected_source"] for r in ans]),
            "guardrail_fired": sum(r["guardrail_fired"] for r in results),
            "withheld": sum(r["withheld"] for r in results),
        },
        "cost_per_question": {"tokens": mean([r["tokens"] for r in results]),
                              "seconds": mean([r["seconds"] for r in results]),
                              "tool_calls": mean([r["tool_calls"] for r in results])},
        "judge_vs_human": agreement(verdicts),
    }
    (EVAL / "summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
