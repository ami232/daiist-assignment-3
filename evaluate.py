"""
Assignment 3: evaluation (`main.py evaluate`).

Stage 1, retrieval: for every test question and each
retrieval design (structure, fixed, structure-diverse), does the right
passage reach the top k?

    hit@k (single)          a top-k chunk is from the expected page AND holds
                            at least 30 words of the expected section (or all
                            of it, if the section is shorter)
    hit@k (multi, strict)   every expected passage is in the top k
    hit@k (multi, partial)  at least one expected passage is in the top k
    words@k                 words the top k chunks would add to the prompt

Unanswerable questions have no right passage, so they are left out of hit
rate. Instead we compare their best similarity score with the answerable
questions' scores: if they are clearly lower, a score threshold could help
the agent refuse.

Question vectors are cached in index/query_vectors.json, so after the first
run this stage costs no API calls.

Outputs in eval/: retrieval_results.csv (one row per question and design)
and retrieval_summary.json.

Stage 2, answers: agent.py answers every question (add_document is never
approved here). Each answer and its trace go to eval/answers.jsonl as soon as
they exist; saved answers are reused, so a crash or the daily quota loses
nothing and a re-run is free.

Stage 3, code checks: are all citations passages that search returned? Did
the agent refuse? That gives the outcome: correct refusal (unanswerable,
refused), wrong refusal (answerable, refused), answered an unanswerable
question, or answered.

Stage 4, LLM judge: gemini-3.5-flash (a different, stronger model than the
agent's) grades each answer against the reference answer and the retrieved
passages with the rubric in JUDGE_RUBRIC, reasoning before its verdict.
Verdicts go to eval/judge_verdicts.csv, cached per answer.

Stage 5, human agreement: eval/grading_sheet.md shows every answer for the
human grader, who fills eval/human_labels.csv without looking at the judge's
verdicts. Agreement and Cohen's kappa are computed once labels exist.

Stage 6, add-document demo (once): q30's answer before, add_document on the
held-out transit page through the MCP server, q30's answer after. Saved in
eval/add_document_demo.json; the index keeps the page.

Summary: eval/results.csv (one row per question) and eval/summary.json.
"""

import asyncio
import csv
import hashlib
import json
import random
import statistics
import sys
import time
from pathlib import Path

from google import genai
from google.genai import errors as genai_errors
from google.genai import types
from pydantic import BaseModel, Field

import agent as ag
import index as ix
from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
EVAL_DIR = ROOT / "eval"
QUESTIONS = EVAL_DIR / "questions.csv"
RETRIEVAL_RESULTS = EVAL_DIR / "retrieval_results.csv"
RETRIEVAL_SUMMARY = EVAL_DIR / "retrieval_summary.json"

KS = (1, 3, 5)
TOP = max(KS)
MIN_PASSAGE_WORDS = 30  # a chunk must hold this much of a section to count as containing it
DESIGNS = list(ix.RETRIEVAL_DESIGNS)

ANSWERS = EVAL_DIR / "answers.jsonl"
JUDGE_VERDICTS = EVAL_DIR / "judge_verdicts.csv"
HUMAN_LABELS = EVAL_DIR / "human_labels.csv"
GRADING_SHEET = EVAL_DIR / "grading_sheet.md"
DEMO = EVAL_DIR / "add_document_demo.json"
RESULTS = EVAL_DIR / "results.csv"
SUMMARY = EVAL_DIR / "summary.json"

JUDGE_MODEL = "gemini-3.5-flash"
# The free tier allows only a few requests per minute: an answer takes about 2
# model calls, so 10 s per question keeps the agent near 12 calls a minute.
MIN_SECONDS_PER_QUESTION = 10
DEMO_ID = "q30"
DEMO_FILE = "corpus/holdout/general-information-and-resources__employee-resources-policies__transit-benefit.md"


def load_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r["question"].strip()]
    for r in rows:
        r["kind"] = r["kind"].strip().lower()
        sources = [s.strip() for s in r["expected_source"].split(";") if s.strip()]
        locations = [l.strip() for l in r["expected_location"].split(";") if l.strip()]
        if len(sources) != len(locations):
            raise ValueError(f"{r['id']}: expected_source and expected_location must pair up")
        r["expected"] = list(zip(sources, locations))
    return rows


# ============================================================================
# Matching a retrieved chunk against an expected passage
# ============================================================================

_section_totals: dict[str, dict[str, int]] = {}


def within(section: str, location: str) -> bool:
    """The section is the expected location itself or one of its sub-sections."""
    return section == location or section.startswith(location + ix.SEPARATOR)


def words_needed(source: str, location: str) -> int:
    """MIN_PASSAGE_WORDS, or the whole section's size if it is shorter."""
    if source not in _section_totals:
        _section_totals[source] = ix.section_word_totals(ix.local_path(source))
    total = sum(n for s, n in _section_totals[source].items() if within(s, location))
    return max(1, min(MIN_PASSAGE_WORDS, total))


def contains_passage(chunk: dict, source: str, location: str, touch: bool = False) -> bool:
    """True if the chunk is from `source` and holds the section `location`.

    Default rule: the chunk holds at least MIN_PASSAGE_WORDS body words of
    the section (sub-sections included), counted from its `section_words`
    metadata. touch=True is the first, lenient rule: any overlap at all,
    even the last line of a section, counts. It favoured fixed windows,
    which span 2.7 sections on average against 1.1 for structure chunks.
    """
    if chunk["source"] != source:
        return False
    if touch:
        return any(within(s, location) for s in chunk["sections"].split(" | "))
    held = sum(n for s, n in json.loads(chunk["section_words"]).items() if within(s, location))
    return held >= words_needed(source, location)


def first_rank(results: list[dict], source: str, location: str, touch: bool = False) -> int | None:
    """1-based rank of the first chunk containing this passage, or None."""
    for rank, chunk in enumerate(results, start=1):
        if contains_passage(chunk, source, location, touch):
            return rank
    return None


# ============================================================================
# Stage 1: retrieval
# ============================================================================

def retrieval_stage(questions: list[dict]) -> dict:
    rows = []
    for q in questions:
        vector = ix.embed_query(q["question"])  # one embedding per question, cached on disk
        for design in DESIGNS:
            results = ix.retrieve(vector, k=TOP, design=design)
            ranks = [first_rank(results, s, l) for s, l in q["expected"]]
            found = [r for r in ranks if r is not None]
            touch_ranks = [first_rank(results, s, l, touch=True) for s, l in q["expected"]]
            row = {
                "id": q["id"],
                "kind": q["kind"],
                "design": design,
                # rank where the FIRST expected passage appears (partial hit)
                "rank_any": min(found) if found else "",
                # rank where ALL expected passages have appeared (strict hit)
                "rank_all": max(ranks) if ranks and None not in ranks else "",
                # same, with the first lenient rule (kept to show its bias)
                "rank_all_touch": max(touch_ranks) if touch_ranks and None not in touch_ranks else "",
                "top_score": results[0]["score"],
                "top1": f"{results[0]['source']} › {results[0]['location']}",
            }
            for k in KS:
                row[f"words@{k}"] = sum(c["words"] for c in results[:k])
            rows.append(row)

    with RETRIEVAL_RESULTS.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    summary = {d: summarise(rows, d) for d in DESIGNS}
    RETRIEVAL_SUMMARY.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print_summary(summary, len(questions))
    return summary


def hit_rate(rows: list[dict], k: int, column: str) -> float:
    return sum(1 for r in rows if r[column] != "" and r[column] <= k) / len(rows) if rows else float("nan")


def summarise(rows: list[dict], design: str) -> dict:
    mine = [r for r in rows if r["design"] == design]
    answerable = [r for r in mine if r["kind"] != "unanswerable"]
    single = [r for r in mine if r["kind"] == "single"]
    multi = [r for r in mine if r["kind"] == "multi"]
    unanswerable = [r for r in mine if r["kind"] == "unanswerable"]

    def score_stats(group):
        scores = [r["top_score"] for r in group]
        return {"mean": round(statistics.mean(scores), 3), "min": min(scores), "max": max(scores)}

    return {
        "n_answerable": len(answerable),
        "hit": {
            f"@{k}": {
                "all_answerable": round(hit_rate(answerable, k, "rank_all"), 3),
                "single": round(hit_rate(single, k, "rank_all"), 3),
                "multi_strict": round(hit_rate(multi, k, "rank_all"), 3),
                "multi_partial": round(hit_rate(multi, k, "rank_any"), 3),
                "all_answerable_touch_rule": round(hit_rate(answerable, k, "rank_all_touch"), 3),
            }
            for k in KS
        },
        # mean reciprocal rank: 1 if the right chunk is first, 1/2 if second... 0 if not in top 5
        "mrr_single": round(statistics.mean(1 / r["rank_all"] if r["rank_all"] != "" else 0 for r in single), 3),
        "words_added": {f"@{k}": round(statistics.mean(r[f"words@{k}"] for r in mine)) for k in KS},
        "top_score_answerable": score_stats(answerable),
        "top_score_unanswerable": score_stats(unanswerable),
        "misses_at_5": [r["id"] for r in answerable if r["rank_all"] == ""],
    }


def print_summary(summary: dict, n: int) -> None:
    width = 30 + 7 * len(KS) * len(DESIGNS)
    print("=" * width)
    print(f"RETRIEVAL: {n} questions, {summary[DESIGNS[0]]['n_answerable']} answerable")
    print("=" * width)
    print(f"{'':<30}" + "".join(f"{d:^{7 * len(KS)}}" for d in DESIGNS))
    print(f"{'':<30}" + "".join(f"{'@' + str(k):>7}" for _ in DESIGNS for k in KS))
    for label, key in [("hit rate, all answerable", "all_answerable"), ("  single", "single"),
                       ("  multi (both passages)", "multi_strict"), ("  multi (at least one)", "multi_partial"),
                       ("old rule: chunk touches section", "all_answerable_touch_rule")]:
        cells = "".join(f"{summary[d]['hit']['@' + str(k)][key]:>7.0%}" for d in DESIGNS for k in KS)
        print(f"{label:<30}{cells}")
    cells = "".join(f"{summary[d]['words_added']['@' + str(k)]:>7}" for d in DESIGNS for k in KS)
    print(f"{'words added to prompt':<30}{cells}")
    print("=" * width)
    for d in DESIGNS:
        s = summary[d]
        print(f"{d}: MRR (single) {s['mrr_single']:.3f}; best score answerable "
              f"{s['top_score_answerable']['mean']:.3f} (min {s['top_score_answerable']['min']:.3f}), "
              f"unanswerable {s['top_score_unanswerable']['mean']:.3f} "
              f"(max {s['top_score_unanswerable']['max']:.3f}); missed at 5: {', '.join(s['misses_at_5']) or 'none'}")


# ============================================================================
# Stage 2: answers
# ============================================================================

def never_approve(requests: list[dict]) -> list[dict]:
    """The evaluation must not change the index: every add_document is rejected."""
    return [{"type": "reject", "message": "Not approved during evaluation."} for _ in requests]


def load_answers() -> dict[str, dict]:
    if not ANSWERS.exists():
        return {}
    rows = [json.loads(line) for line in ANSWERS.read_text(encoding="utf-8").splitlines() if line.strip()]
    return {r["id"]: r for r in rows}


def answer_with_retry(q: dict) -> dict | None:
    """Answer one question; on a rate limit or overload, wait a minute and try again (3 tries)."""
    for attempt in range(3):
        try:
            return ag.answer(q["question"], approve=never_approve)
        except Exception as error:
            text = str(error)
            busy = any(t in text for t in ("429", "RESOURCE_EXHAUSTED", "503", "UNAVAILABLE"))
            print(f"  {q['id']}: {type(error).__name__}: {text[:120]}", flush=True)
            if not busy or attempt == 2:
                return None
            time.sleep(65)  # the free tier counts requests per minute
    return None


def answers_stage(questions: list[dict]) -> dict[str, dict]:
    """Answer every question that has no saved answer yet (for the same question text)."""
    saved = load_answers()
    todo = [q for q in questions if saved.get(q["id"], {}).get("question") != q["question"]]
    print(f"\nANSWERS: {len(questions) - len(todo)} saved, {len(todo)} to run with {ag.MODEL}", flush=True)
    for n, q in enumerate(todo, start=1):
        started = time.time()
        result = answer_with_retry(q)
        if result is None:  # still failing: keep what we have, finish on the next run
            print("  Run `main.py evaluate` again later to finish.", flush=True)
            break
        saved[q["id"]] = {"id": q["id"], **result}
        with ANSWERS.open("a", encoding="utf-8") as f:
            f.write(json.dumps(saved[q["id"]]) + "\n")
        print(f"  [{n}/{len(todo)}] {q['id']} {result['seconds']:>5.1f}s "
              f"{'refused' if result['refused'] else 'answered'}, guardrail {result['guardrail']}", flush=True)
        time.sleep(max(0.0, MIN_SECONDS_PER_QUESTION - (time.time() - started)))  # stay under the per-minute limit
    # rewrite the file so it holds exactly one, current line per question
    ANSWERS.write_text("".join(json.dumps(saved[q["id"]]) + "\n" for q in questions if q["id"] in saved),
                       encoding="utf-8")
    return saved


# ============================================================================
# Stage 3: code checks
# ============================================================================

def code_checks(q: dict, a: dict) -> dict:
    retrieved = {ag.normalise(c) for block in a["retrieved"] for c in ag.CITATION_LINE.findall(block)}
    cited = [c for c in ag.CITED.findall(a["answer"]) if "@" not in c]
    valid = all(ag.normalise(c) in retrieved for c in cited)
    answerable = q["kind"] != "unanswerable"
    if a["refused"]:
        outcome = "wrong refusal" if answerable else "correct refusal"
    else:
        outcome = "answered" if answerable else "answered an unanswerable question"
    return {"citations": len(cited), "citations_valid": valid, "outcome": outcome}


# ============================================================================
# Stage 4: LLM judge
# ============================================================================

JUDGE_RUBRIC = """You grade answers from an HR assistant for employees of the Technology Transformation
Services (TTS). The assistant must answer only from passages of the TTS Handbook that a search
tool returned, and must say "The handbook does not cover this." when they do not contain the answer.

You get the question, its kind, a reference answer written by a person, the passages the
assistant retrieved, and the assistant's answer. Grade two things.

correct (1 or 0):
- 1 if the answer gives the key facts of the reference answer, with numbers exactly right and
  every part of a multi-part question answered, and says nothing that contradicts the reference.
  Extra correct details are fine.
- 0 if a key fact is missing or wrong, if only part of the question is answered, or if the
  assistant refused although the reference answer gives an answer.
- For a question of kind "unanswerable": 1 if the answer says the handbook does not cover it AND
  does not state the missing fact anyway (for example a percentage or an amount); 0 otherwise.

supported (1 or 0):
- 1 if every factual claim about policy in the answer is stated in the retrieved passages.
- Generic advice needs no support: suggesting People Ops or HR, the note that the handbook is a
  June 2026 snapshot, or saying the handbook does not cover something.
- 0 if any policy claim is not in the passages, even if it is true in general (general knowledge
  does not count as support).

Write your reasoning first: compare the answer with the reference, then check each claim against
the passages. Then give the two grades."""


class Verdict(BaseModel):
    """Field order is deliberate: reasoning is generated before the grades."""

    reasoning: str = Field(description="Compare the answer with the reference, then check each claim against the passages.")
    correct: int = Field(description="1 or 0, as defined in the rubric")
    supported: int = Field(description="1 or 0, as defined in the rubric")


def answer_hash(a: dict) -> str:
    return hashlib.sha1(a["answer"].encode()).hexdigest()[:12]


def judge_one(client: genai.Client, q: dict, a: dict) -> dict:
    passages = "\n\n".join(a["retrieved"]) or "(the assistant did not search)"
    prompt = (f"{JUDGE_RUBRIC}\n\n========\nQUESTION ({q['kind']}): {q['question']}\n\n"
              f"REFERENCE ANSWER: {q['reference_answer']}\n\n"
              f"RETRIEVED PASSAGES:\n{passages}\n\n========\nASSISTANT'S ANSWER:\n{a['answer']}")
    for attempt in range(6):
        try:
            response = client.models.generate_content(
                model=JUDGE_MODEL,
                contents=prompt,
                config=types.GenerateContentConfig(response_mime_type="application/json", response_schema=Verdict),
            )
            verdict = Verdict.model_validate_json(response.text)
            usage = response.usage_metadata
            return {"id": q["id"], "answer_hash": answer_hash(a),
                    "correct": int(verdict.correct == 1), "supported": int(verdict.supported == 1),
                    "reasoning": verdict.reasoning,
                    "judge_input_tokens": usage.prompt_token_count or 0,
                    "judge_output_tokens": (usage.candidates_token_count or 0) + (usage.thoughts_token_count or 0)}
        except (genai_errors.APIError, ValueError) as error:
            code = getattr(error, "code", None)
            if attempt == 5 or (isinstance(error, genai_errors.APIError) and code not in (429, 500, 503)):
                raise
            time.sleep(ix.retry_delay(error, attempt) if code == 429 else min(60, 5 * 2 ** attempt) + random.random())
    raise RuntimeError("unreachable")


def judge_stage(questions: list[dict], answers: dict[str, dict]) -> dict[str, dict]:
    verdicts = {}
    if JUDGE_VERDICTS.exists():
        with JUDGE_VERDICTS.open(newline="", encoding="utf-8") as f:
            verdicts = {r["id"]: r for r in csv.DictReader(f)}
    todo = [q for q in questions if q["id"] in answers
            and verdicts.get(q["id"], {}).get("answer_hash") != answer_hash(answers[q["id"]])]
    print(f"\nJUDGE: {len(verdicts)} cached, {len(todo)} to grade with {JUDGE_MODEL}", flush=True)
    client = genai.Client(api_key=load_api_key())
    for q in todo:
        try:
            verdicts[q["id"]] = judge_one(client, q, answers[q["id"]])
        except Exception as error:
            print(f"  {q['id']}: judge stopped ({type(error).__name__}: {str(error)[:150]}). "
                  f"Run again later to finish.", flush=True)
            break
        print(f"  {q['id']} graded", flush=True)
        write_csv(JUDGE_VERDICTS, [verdicts[x["id"]] for x in questions if x["id"] in verdicts])
    for v in verdicts.values():
        v["correct"], v["supported"] = int(v["correct"]), int(v["supported"])
    return verdicts


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


# ============================================================================
# Stage 5: grading sheet and human agreement
# ============================================================================

def write_grading_sheet(questions: list[dict], answers: dict[str, dict]) -> None:
    """Everything the human grader needs, and nothing from the judge."""
    lines = ["# Grading sheet", "",
             "Grade each answer in `eval/human_labels.csv` (columns `id,correct,supported,notes`, a note for every 0).",
             "Use the same definitions as the judge's rubric (`JUDGE_RUBRIC` in evaluate.py).",
             "Do **not** open `eval/judge_verdicts.csv` or `eval/results.csv` before you finish.", ""]
    for q in questions:
        a = answers.get(q["id"])
        if not a:
            continue
        lines += [f"## {q['id']} ({q['kind']})", "", f"**Question:** {q['question']}", "",
                  f"**Reference answer:** {q['reference_answer']}", "", "**Agent's answer:**", "",
                  *[f"> {line}" for line in a["answer"].splitlines()], "",
                  "<details><summary>Retrieved passages</summary>", "", "```text",
                  "\n\n".join(a["retrieved"]) or "(no search)", "```", "</details>", ""]
    GRADING_SHEET.write_text("\n".join(lines), encoding="utf-8")


def load_human_labels() -> dict[str, dict]:
    if not HUMAN_LABELS.exists():
        return {}
    with HUMAN_LABELS.open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if (r.get("id") or "").strip()]
    labels = {}
    for r in rows:
        try:
            labels[r["id"].strip()] = {"correct": int(r["correct"]), "supported": int(r["supported"]),
                                       "notes": r.get("notes", "")}
        except (TypeError, ValueError):
            continue  # an unfinished row
    return labels


def agreement(human: dict[str, dict], judge: dict[str, dict], field: str) -> dict:
    """Share of answers where human and judge agree, and Cohen's kappa.

    Kappa corrects for chance: if both said 1 to 90% of answers, they would
    agree on most answers even by guessing. kappa = (observed - chance) /
    (1 - chance); 1 is perfect agreement, 0 is no better than chance.
    """
    ids = [i for i in human if i in judge]
    if not ids:
        return {"n": 0}
    h = [human[i][field] for i in ids]
    j = [judge[i][field] for i in ids]
    observed = sum(a == b for a, b in zip(h, j)) / len(ids)
    p_h, p_j = sum(h) / len(ids), sum(j) / len(ids)
    chance = p_h * p_j + (1 - p_h) * (1 - p_j)
    kappa = (observed - chance) / (1 - chance) if chance < 1 else float("nan")
    return {"n": len(ids), "agreement": round(observed, 3), "kappa": round(kappa, 3),
            "disagreements": [i for i, a, b in zip(ids, h, j) if a != b]}


# ============================================================================
# Stage 6: add-document demo
# ============================================================================

async def add_through_mcp(path: str) -> str:
    async with ag.MCPTools() as tools:
        add = next(t for t in tools if t.name == "add_document")
        return await add.ainvoke({"path": path})


def demo_stage(questions: list[dict], answers: dict[str, dict]) -> dict | None:
    if DEMO.exists():
        return json.loads(DEMO.read_text(encoding="utf-8"))
    if len(answers) < len(questions):
        print("\nDEMO: waiting until every question has its answer (the demo changes the index)")
        return None
    q = next(x for x in questions if x["id"] == DEMO_ID)
    print(f"\nDEMO: adding {DEMO_FILE} through the MCP server (approved by the evaluation script)", flush=True)
    added = asyncio.run(add_through_mcp(DEMO_FILE))
    after = ag.answer(q["question"], approve=never_approve)
    demo = {"id": DEMO_ID, "question": q["question"], "before": answers[DEMO_ID]["answer"],
            "add_document": added, "after": after["answer"], "after_trace": after}
    DEMO.write_text(json.dumps(demo, indent=2), encoding="utf-8")
    return demo


# ============================================================================
# Summary
# ============================================================================

def summary_stage(questions, answers, verdicts, human, demo) -> None:
    rows = []
    for q in questions:
        a = answers.get(q["id"])
        if not a:
            continue
        v, h = verdicts.get(q["id"], {}), human.get(q["id"], {})
        rows.append({"id": q["id"], "kind": q["kind"], **code_checks(q, a),
                     "guardrail": a["guardrail"],
                     "judge_correct": v.get("correct", ""), "judge_supported": v.get("supported", ""),
                     "human_correct": h.get("correct", ""), "human_supported": h.get("supported", ""),
                     "model_calls": a["model_calls"], "input_tokens": a["input_tokens"],
                     "output_tokens": a["output_tokens"], "seconds": a["seconds"],
                     "judge_input_tokens": v.get("judge_input_tokens", ""),
                     "judge_output_tokens": v.get("judge_output_tokens", "")})
    write_csv(RESULTS, rows)

    def share(group, test):
        return f"{sum(1 for r in group if test(r))}/{len(group)}"

    judged = [r for r in rows if r["judge_correct"] != ""]
    by_kind = {k: [r for r in judged if r["kind"] == k] for k in ("single", "multi", "unanswerable")}
    outcomes = {o: sum(1 for r in rows if r["outcome"] == o) for o in
                ("answered", "wrong refusal", "correct refusal", "answered an unanswerable question")}

    def stat(field):
        values = [float(r[field]) for r in rows if r[field] != ""]
        return {"mean": round(statistics.mean(values), 1), "median": round(statistics.median(values), 1)} if values else {}

    summary = {
        "agent_model": ag.MODEL, "judge_model": JUDGE_MODEL, "answered_questions": len(rows),
        "outcomes": outcomes,
        "judge": {
            "correct": share(judged, lambda r: r["judge_correct"] == 1),
            "correct_by_kind": {k: share(g, lambda r: r["judge_correct"] == 1) for k, g in by_kind.items()},
            "supported": share(judged, lambda r: r["judge_supported"] == 1),
            "unsupported_answers": [r["id"] for r in judged if r["judge_supported"] == 0],
            "incorrect": [r["id"] for r in judged if r["judge_correct"] == 0],
        },
        "code_checks": {
            "invalid_citations": [r["id"] for r in rows if not r["citations_valid"]],
            "guardrail_retried": [r["id"] for r in rows if r["guardrail"] == "retried"],
            "guardrail_blocked": [r["id"] for r in rows if r["guardrail"] == "blocked"],
        },
        "human_vs_judge": {f: agreement(human, verdicts, f) for f in ("correct", "supported")} if human else
                          "no human labels yet",
        "cost_per_question": {f: stat(f) for f in ("model_calls", "input_tokens", "output_tokens", "seconds",
                                                    "judge_input_tokens", "judge_output_tokens")},
        "add_document_demo": {k: demo[k] for k in ("question", "before", "add_document", "after")} if demo else None,
    }
    SUMMARY.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print("\n" + "=" * 78)
    print(f"END TO END: {len(rows)}/{len(questions)} answered by {ag.MODEL}, judged by {JUDGE_MODEL}")
    print("=" * 78)
    print(f"outcomes (code):   {outcomes}")
    print(f"judge correct:     {summary['judge']['correct']}  by kind {summary['judge']['correct_by_kind']}")
    print(f"judge supported:   {summary['judge']['supported']}")
    print(f"guardrail:         retried {summary['code_checks']['guardrail_retried']}, "
          f"blocked {summary['code_checks']['guardrail_blocked']}; invalid citations "
          f"{summary['code_checks']['invalid_citations']}")
    if human:
        for f in ("correct", "supported"):
            a = summary["human_vs_judge"][f]
            print(f"human vs judge ({f}): {a.get('agreement', 0):.0%} agreement, kappa {a.get('kappa')}, "
                  f"n={a['n']}, disagree on {a.get('disagreements')}")
    else:
        print("human vs judge:    no human labels yet (see eval/grading_sheet.md)")
    c = summary["cost_per_question"]
    print(f"cost per question: {c['model_calls'].get('mean')} model calls, "
          f"{c['input_tokens'].get('mean')} input + {c['output_tokens'].get('mean')} output tokens, "
          f"{c['seconds'].get('mean')}s mean ({c['seconds'].get('median')}s median)")
    if demo:
        print(f"\nadd-document demo ({demo['id']}): {demo['add_document']}")
        print(f"  before: {demo['before'][:160]}")
        print(f"  after:  {demo['after'][:300]}")


def main() -> None:
    questions = load_questions()
    retrieval_stage(questions)
    answers = answers_stage(questions)
    verdicts = judge_stage(questions, answers)
    write_grading_sheet(questions, answers)
    human = load_human_labels()
    demo = demo_stage(questions, answers)
    summary_stage(questions, answers, verdicts, human, demo)


if __name__ == "__main__":
    main()
