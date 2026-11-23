"""
Assignment 3: evaluation (`main.py evaluate`).

1. Retrieval: hit rate at k = 1, 3, 5 for each design (no chat calls; one cached query
   embedding per question, shared by all designs).
2. End to end: the agent (agent.py) answers every question. Answers are saved in
   eval/answers.jsonl and reused while the question, AGENTS.md and the model are unchanged
   (set EVAL_FRESH=1 to re-ask everything).
3. Code checks: refusals (the fixed refusal sentence) and citations (every citation inside a
   retrieved passage).
4. LLM judge with a rubric and the retrieved text as evidence: correct and supported.
5. eval/grading_sheet.md for my own grades (no judge verdicts in it), agreement with
   eval/human_labels.csv, and eval/failures.csv with a suggested cause per failure.

Outputs in eval/: retrieval_summary.csv, retrieval_per_question.csv, answers.jsonl,
judge.jsonl, results.csv, failures.csv, grading_sheet.md, summary.json.
"""

from __future__ import annotations

import asyncio
import csv
import hashlib
import json
import os
import re
import statistics
import sys
import time
from pathlib import Path

import rag
from rag import log

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
HUMAN = EVAL / "human_labels.csv"
ANSWERS = EVAL / "answers.jsonl"
JUDGE_FILE = EVAL / "judge.jsonl"
JUDGE_MODEL = os.environ.get("JUDGE_MODEL", "gemini-3.1-flash-lite")
KS = (1, 3, 5)
# Free tier of the lite models: 15 requests per minute. Keep every model call >= 4.5 s apart on average.
SECONDS_PER_CALL = float(os.environ.get("EVAL_SECONDS_PER_CALL", "4.5"))

# The design comparison always runs on the original corpus, also after add_document added more.
BASE_SOURCES = ["GDPR", "EDPB 05/2020", "EDPB 9/2022"]

# Retrieval designs compared (REPORT.md, Retrieval). "fixed + hybrid" separates the effect of keyword search from chunking.
CONFIGS = [
    ("A fixed (vector)", "fixed", "vector"),
    ("B structure (vector)", "structure", "vector"),
    ("C structure + hybrid", "structure", "hybrid"),
    ("A fixed + hybrid", "fixed", "hybrid"),
]


# --------------------------------------------------------------------------- questions

def load_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if (r.get("question") or "").strip()]
    for r in rows:
        r["kind"] = r["kind"].strip().lower()
        sources = [s.strip() for s in r["expected_source"].split(";") if s.strip()]
        locations = [l.strip() for l in r["expected_location"].split(";") if l.strip()]
        if len(sources) == 1 and len(locations) > 1:        # one source, several locations
            sources = sources * len(locations)
        if len(locations) == 1 and len(sources) > 1:
            locations = locations * len(sources)
        r["expected"] = list(zip(sources, locations))
    return rows


def overlaps(a: str, b: str) -> bool:
    return rag.location_covered(a, b) or rag.location_covered(b, a)


def fine_locs(locs_field: str) -> list[str]:
    """A chunk's locations without the bare article ('Art. 33') when a paragraph of it is listed,
    so a chunk holding only Art. 33(5) does not count as a hit for Art. 33(1)."""
    locs = [l for l in locs_field.strip("|").split("|") if l]
    articles_with_parts = {re.match(r"Art\. \d+", l).group(0) for l in locs if re.fullmatch(r"Art\. \d+\(\w+\)", l)}
    return [l for l in locs if l not in articles_with_parts and l != "Annex"]


def chunk_matches(chunk: dict, source: str, location: str) -> bool:
    if chunk["source"].lower() != source.lower():
        return False
    return any(rag.location_covered(unit, location) or rag.location_covered(location, unit)
               for unit in fine_locs(chunk["locs"]))


# --------------------------------------------------------------------------- 1. retrieval

def evaluate_retrieval(questions: list[dict]) -> tuple[list[dict], list[dict]]:
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    per_question, summary = [], []
    for name, design, method in CONFIGS:
        firsts, alls, words = [], [], []
        for q in answerable:
            chunks = rag.search(q["question"], k=max(KS), design=design, method=method, sources=BASE_SOURCES)
            hits = [i + 1 for i, c in enumerate(chunks) if any(chunk_matches(c, s, l) for s, l in q["expected"])]
            first = hits[0] if hits else None
            # rank at which ALL expected passages have been seen (multi questions)
            seen, all_rank = set(), None
            for i, c in enumerate(chunks):
                for j, (s, l) in enumerate(q["expected"]):
                    if chunk_matches(c, s, l):
                        seen.add(j)
                if len(seen) == len(q["expected"]):
                    all_rank = i + 1
                    break
            firsts.append(first)
            alls.append(all_rank)
            words.append(sum(len(c["text"].split()) for c in chunks))
            per_question.append({"config": name, "id": q["id"], "kind": q["kind"], "first_hit_rank": first or "",
                                 "all_found_rank": all_rank or "",
                                 "top5": " ; ".join(rag.citation(c) for c in chunks)})
        row = {"config": name, "questions": len(answerable)}
        for k in KS:
            row[f"hit@{k}"] = round(sum(1 for f in firsts if f and f <= k) / len(firsts), 3)
        multi = [a for a, q in zip(alls, answerable) if q["kind"] == "multi"]
        for k in KS:
            row[f"multi_all@{k}"] = round(sum(1 for a in multi if a and a <= k) / len(multi), 3) if multi else ""
        row["mrr@5"] = round(statistics.mean(1 / f if f else 0 for f in firsts), 3)
        row["avg_words_top5"] = round(statistics.mean(words))
        summary.append(row)
    write_csv(EVAL / "retrieval_summary.csv", summary)
    write_csv(EVAL / "retrieval_per_question.csv", per_question)
    return summary, per_question


# --------------------------------------------------------------------------- 2. answers

def answer_key(q: dict, model: str) -> str:
    prompt = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    return hashlib.sha256(f"{q['question']}|{model}|{prompt}|{rag.ACTIVE_DESIGN}|{rag.ACTIVE_METHOD}".encode()).hexdigest()[:16]


def read_jsonl(path: Path) -> dict:
    out = {}
    if path.is_file():
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                row = json.loads(line)
                out[row["id"]] = row
    return out


def write_jsonl(path: Path, rows: dict) -> None:
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows.values()), encoding="utf-8")


async def run_agent(questions: list[dict]) -> dict:
    import agent

    saved = {} if os.environ.get("EVAL_FRESH") else read_jsonl(ANSWERS)
    # re-ask when the question, prompt, model or design changed, or when the last attempt failed
    todo = [q for q in questions if saved.get(q["id"], {}).get("key") != answer_key(q, agent.MODEL)
            or saved[q["id"]].get("error")]
    if todo:
        log(f"Asking the agent {len(todo)} question(s) ({len(questions) - len(todo)} reused from {ANSWERS.name})")
        async with agent.Harness(approve=lambda action: False) as harness:   # nobody approves add_document here
            for i, q in enumerate(todo, 1):
                started = time.time()
                try:
                    result = await harness.ask(q["question"])
                except Exception as error:   # keep going; record the failure
                    result = {"question": q["question"], "answer": "", "error": f"{type(error).__name__}: {error}",
                              "refused": False, "citations": [], "invalid_citations": [], "searches": [],
                              "retrieved": [], "retrieved_text": "", "guardrail_events": [], "model_calls": 0,
                              "input_tokens": 0, "output_tokens": 0, "total_tokens": 0, "seconds": 0,
                              "model": agent.MODEL}
                result.update({"id": q["id"], "key": answer_key(q, agent.MODEL)})
                saved[q["id"]] = result
                write_jsonl(ANSWERS, saved)                 # save after every answer
                if result.get("error"):
                    log(f"  [{i}/{len(todo)}] {q['id']} ERROR: {result['error'][:160]}")
                    if daily_quota(result["error"]):
                        log(f"\nThe daily request quota of {agent.MODEL} is used up. Answers so far are saved; "
                            f"run `main.py evaluate` again after it resets to ask the remaining questions.")
                        break
                else:
                    log(f"  [{i}/{len(todo)}] {q['id']} {'refused' if result['refused'] else 'answered'} "
                        f"in {result['seconds']}s, {result['total_tokens']} tokens")
                # pace to the per-minute limit (the model calls this question made, plus one spare)
                await asyncio.sleep(max(0.0, SECONDS_PER_CALL * (result.get("model_calls", 0) + 1) - (time.time() - started)))
    return saved


def daily_quota(message: str) -> bool:
    return "per day" in message.lower() or "PerDay" in message


# --------------------------------------------------------------------------- 3. code checks

def code_checks(q: dict, a: dict) -> dict:
    unanswerable = q["kind"] == "unanswerable"
    refused = bool(a.get("refused"))
    if unanswerable:
        outcome = "correct refusal" if refused else "missed refusal"
    else:
        outcome = "wrong refusal" if refused else "answered"
    retrieved = [tuple(re.match(r"\[(.+?) \| (.+)\]", r).groups()) for r in a.get("retrieved", [])]
    expected_retrieved = (not unanswerable) and all(
        any(s.lower() == rs.lower() and overlaps(l, rl) for rs, rl in retrieved) for s, l in q["expected"])
    any_expected_retrieved = (not unanswerable) and any(
        any(s.lower() == rs.lower() and overlaps(l, rl) for rs, rl in retrieved) for s, l in q["expected"])
    cited_sources = {re.match(r"\[(.+?) \|", c).group(1).lower() for c in a.get("citations", [])}
    return {
        "outcome": outcome,
        "error": a.get("error", ""),
        "has_citation": bool(a.get("citations")),
        "citations_valid": not a.get("invalid_citations"),
        "cites_expected_source": (not unanswerable) and bool(cited_sources & {s.lower() for s, _ in q["expected"]}),
        "expected_passage_retrieved": expected_retrieved,
        "any_expected_passage_retrieved": any_expected_retrieved,
        "guardrail_fired": any(e["guardrail"] == "citations" for e in a.get("guardrail_events", [])),
    }


# --------------------------------------------------------------------------- 4. judge

RUBRIC = """You are grading one answer of a GDPR assistant for small businesses. The assistant may
only use the retrieved passages shown below. Grade two things, each 1 or 0.

CORRECT (compare with the reference answer):
- 1 only if the answer's conclusion matches the reference answer (same yes/no, same deadline,
  same party to notify) AND it includes every condition, exception and element that the
  reference lists, AND it contradicts the reference on nothing. Extra correct detail is fine.
- 0 if the conclusion differs, a deadline/number/party is wrong, or ANY condition, exception or
  element listed in the reference is missing (for this user, a missed exception can mean a
  missed legal obligation).
- For a question marked UNANSWERABLE: 1 only if the answer says the documents do not cover it
  (a refusal); 0 if it gives a substantive answer.

SUPPORTED (compare with the retrieved passages, not with your own knowledge):
- 1 if every factual claim (obligation, deadline, number, condition, exception, example) is
  stated in or directly follows from the retrieved passages. Paraphrase is fine. Generic advice
  such as "contact your data protection authority or a lawyer" does not need support.
- 0 if any factual claim is not in the passages, even if it is true in reality. List those claims.

Be strict and literal. Reply with JSON only."""

JUDGE_SCHEMA = {
    "type": "object",
    "properties": {
        "correct": {"type": "integer", "enum": [0, 1]},
        "supported": {"type": "integer", "enum": [0, 1]},
        "unsupported_claims": {"type": "array", "items": {"type": "string"}},
        "reason": {"type": "string"},
    },
    "required": ["correct", "supported", "unsupported_claims", "reason"],
}


def judge_one(q: dict, a: dict) -> dict:
    from google.genai import types

    prompt = (f"{RUBRIC}\n\nQUESTION ({q['kind'].upper()}): {q['question']}\n\n"
              f"REFERENCE ANSWER: {q['reference_answer']}\n\n"
              f"RETRIEVED PASSAGES:\n{a.get('retrieved_text') or '(none)'}\n\n"
              f"ASSISTANT'S ANSWER:\n{a.get('answer')}")
    response = rag.client().models.generate_content(
        model=JUDGE_MODEL, contents=prompt,
        config=types.GenerateContentConfig(response_mime_type="application/json", response_json_schema=JUDGE_SCHEMA))
    verdict = json.loads(response.text)
    usage = response.usage_metadata
    verdict["judge_tokens"] = getattr(usage, "total_token_count", 0) or 0
    return verdict


def run_judge(questions: list[dict], answers: dict) -> dict:
    saved = read_jsonl(JUDGE_FILE)
    for q in questions:
        a = answers.get(q["id"])
        if not a or not a.get("answer") or a.get("error"):
            continue
        key = hashlib.sha256(f"{a['answer']}|{q['reference_answer']}|{JUDGE_MODEL}|{RUBRIC}".encode()).hexdigest()[:16]
        if saved.get(q["id"], {}).get("key") == key:
            continue
        if a.get("refused"):   # refusals are graded by code, not by the judge
            verdict = {"correct": int(q["kind"] == "unanswerable"), "supported": 1, "unsupported_claims": [],
                       "reason": "Refusal: graded by code.", "judge_tokens": 0, "by": "code"}
        else:
            verdict = None
            for attempt in range(4):          # the judge model is sometimes overloaded (503)
                try:
                    verdict = {**judge_one(q, a), "by": JUDGE_MODEL}
                    time.sleep(SECONDS_PER_CALL)
                    break
                except Exception as error:
                    message = str(error)
                    if daily_quota(message):
                        log(f"  judge stopped: daily quota of {JUDGE_MODEL} used up; re-run later to finish.")
                        return saved
                    if attempt < 3 and any(code in message for code in ("503", "429", "500", "UNAVAILABLE")):
                        time.sleep(20 * (attempt + 1))
                        continue
                    log(f"  judge failed on {q['id']}: {message[:160]}")
                    break
            if verdict is None:
                continue
        saved[q["id"]] = {"id": q["id"], "key": key, **verdict}
        write_jsonl(JUDGE_FILE, saved)
        log(f"  judged {q['id']}")
    return saved


# --------------------------------------------------------------------------- 5. human grading and agreement

def write_grading_sheet(questions: list[dict], answers: dict) -> None:
    """Everything needed to grade by hand, and nothing from the judge."""
    lines = ["# Grading sheet (my own grades → eval/human_labels.csv)", "",
             "Grade each answer BEFORE opening eval/judge.jsonl or eval/results.csv.",
             "`correct` 1/0: right against the reference (or a proper refusal). "
             "`supported` 1/0: every claim is in the retrieved text. Notes for every 0.", ""]
    for q in questions:
        a = answers.get(q["id"], {})
        lines += [f"## {q['id']} · {q['kind']}", "", f"**Question.** {q['question']}", "",
                  f"**Reference.** {q['reference_answer']}", "",
                  f"**Expected.** {'; '.join(f'[{s} | {l}]' for s, l in q['expected']) or '— (unanswerable)'}", "",
                  "**Answer.**", "", a.get("answer", "(no answer)"), "",
                  f"**Retrieved.** {', '.join(dict.fromkeys(a.get('retrieved', []))) or '(nothing)'}", "",
                  "<details><summary>Retrieved text</summary>", "", "```", a.get("retrieved_text", ""), "```",
                  "", "</details>", "", "---", ""]
    (EVAL / "grading_sheet.md").write_text("\n".join(lines), encoding="utf-8")


def agreement(rows: list[dict]) -> dict:
    if not HUMAN.is_file():
        return {}
    with HUMAN.open(newline="", encoding="utf-8") as f:
        human = {r["id"].strip(): r for r in csv.DictReader(f) if (r.get("id") or "").strip()}
    out = {"graded_by_me": len(human)}
    for field in ("correct", "supported"):
        pairs = [(int(human[r["id"]][field]), int(r[field])) for r in rows
                 if r["id"] in human and str(human[r["id"]].get(field, "")).strip() in ("0", "1") and r[field] != ""]
        if not pairs:
            continue
        agree = sum(h == j for h, j in pairs) / len(pairs)
        ph, pj = sum(h for h, _ in pairs) / len(pairs), sum(j for _, j in pairs) / len(pairs)
        chance = ph * pj + (1 - ph) * (1 - pj)
        # kappa is undefined when both raters gave the same label to every item (no variation)
        kappa = round((agree - chance) / (1 - chance), 3) if chance < 1 else "undefined (no variation)"
        out[field] = {"n": len(pairs), "agreement": round(agree, 3), "cohen_kappa": kappa,
                      "me_1_rate": round(ph, 3), "judge_1_rate": round(pj, 3),
                      "disagreements": [r["id"] for r in rows if r["id"] in human
                                        and str(human[r["id"]].get(field, "")).strip() in ("0", "1")
                                        and r[field] != "" and int(human[r["id"]][field]) != int(r[field])]}
    return out


# --------------------------------------------------------------------------- failures

def suggest_cause(q: dict, r: dict) -> str:
    """A first guess from the checks; the final classification is mine (REPORT.md)."""
    if r["outcome"] == "missed refusal":
        return "unsupported claim" if r["supported"] == 0 else "missed refusal (answered an unanswerable question)"
    # "right passage" only if ALL expected passages were retrieved (a multi question can be half-missed)
    if r["outcome"] == "wrong refusal":
        return "wrong refusal" if r["expected_passage_retrieved"] else "retrieval miss"
    if r["supported"] == 0:
        return "unsupported claim"
    if r["correct"] == 0:
        return "wrong answer from the right passage" if r["expected_passage_retrieved"] else "retrieval miss"
    return ""


# --------------------------------------------------------------------------- main

def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    fields = list(dict.fromkeys(k for r in rows for k in r))
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def print_table(rows: list[dict], columns: list[str]) -> None:
    widths = [max(len(str(c)), *(len(str(r.get(c, ""))) for r in rows)) for c in columns]
    log("  ".join(str(c).ljust(w) for c, w in zip(columns, widths)))
    for r in rows:
        log("  ".join(str(r.get(c, "")).ljust(w) for c, w in zip(columns, widths)))


def main() -> int:
    import warnings
    warnings.filterwarnings("ignore")
    questions = load_questions()
    kinds = {k: sum(q["kind"] == k for q in questions) for k in ("single", "multi", "unanswerable")}
    log(f"{len(questions)} questions: {kinds}")

    log("\n== 1. Retrieval: hit rate at k (answerable questions) ==")
    retrieval, _ = evaluate_retrieval(questions)
    print_table(retrieval, ["config", "hit@1", "hit@3", "hit@5", "multi_all@5", "mrr@5", "avg_words_top5"])
    if os.environ.get("EVAL_ONLY") == "retrieval":
        return 0

    log(f"\n== 2. End to end: agent on every question (design {rag.ACTIVE_DESIGN}, {rag.ACTIVE_METHOD}) ==")
    answers = asyncio.run(run_agent(questions))
    write_grading_sheet(questions, answers)

    log(f"\n== 3-4. Code checks and judge ({JUDGE_MODEL}) ==")
    verdicts = run_judge(questions, answers)
    rows = []
    for q in questions:
        a, v = answers.get(q["id"], {}), verdicts.get(q["id"], {})
        r = {"id": q["id"], "kind": q["kind"], **code_checks(q, a),
             "correct": v.get("correct", ""), "supported": v.get("supported", ""),
             "judge_reason": v.get("reason", ""), "unsupported_claims": " | ".join(v.get("unsupported_claims", [])),
             "searches": len(a.get("searches", [])), "model_calls": a.get("model_calls", 0),
             "total_tokens": a.get("total_tokens", 0), "seconds": a.get("seconds", 0)}
        r["suggested_cause"] = suggest_cause(q, r) if r["correct"] != "" else ""
        rows.append(r)
    write_csv(EVAL / "results.csv", rows)
    # my own classification (my_cause, notes) is kept across re-runs
    mine = {}
    if (EVAL / "failures.csv").is_file():
        with (EVAL / "failures.csv").open(newline="", encoding="utf-8") as f:
            mine = {r["id"]: r for r in csv.DictReader(f)}
    failure_ids = [r["id"] for r in rows if r["suggested_cause"]] + [i for i in mine if mine[i].get("my_cause")]
    by_id = {r["id"]: r for r in rows}
    write_csv(EVAL / "failures.csv", [{"id": i, "kind": by_id[i]["kind"], "outcome": by_id[i]["outcome"],
                                       "correct": by_id[i]["correct"], "supported": by_id[i]["supported"],
                                       "all_expected_retrieved": by_id[i]["expected_passage_retrieved"],
                                       "suggested_cause": by_id[i]["suggested_cause"],
                                       "my_cause": mine.get(i, {}).get("my_cause", ""),
                                       "notes": mine.get(i, {}).get("notes", "")}
                                      for i in dict.fromkeys(failure_ids) if i in by_id])

    answerable = [r for r in rows if r["kind"] != "unanswerable"]
    unanswerable = [r for r in rows if r["kind"] == "unanswerable"]
    answered = [r for r in rows if r["outcome"] in ("answered", "missed refusal") and r["supported"] != ""]
    graded = [r for r in rows if r["correct"] != ""]
    summary = {
        "questions": len(rows), "kinds": kinds, "agent_model": next((a.get("model") for a in answers.values()), ""),
        "judge_model": JUDGE_MODEL, "design": f"{rag.ACTIVE_DESIGN} + {rag.ACTIVE_METHOD}",
        "correct": sum(r["correct"] == 1 for r in graded), "graded": len(graded),
        "answerable_correct": sum(r["correct"] == 1 for r in answerable),
        "answerable": len(answerable),
        "unsupported_answers": sum(r["supported"] == 0 for r in answered), "answers_given": len(answered),
        "correct_refusals": sum(r["outcome"] == "correct refusal" for r in unanswerable),
        "unanswerable": len(unanswerable),
        "missed_refusals": sum(r["outcome"] == "missed refusal" for r in unanswerable),
        "wrong_refusals": sum(r["outcome"] == "wrong refusal" for r in answerable),
        "invalid_citation_answers": sum(not r["citations_valid"] for r in rows),
        "guardrail_fired": sum(r["guardrail_fired"] for r in rows),
        "errors": sum(bool(r["error"]) for r in rows),
        "avg_tokens_per_question": round(statistics.mean(r["total_tokens"] for r in rows)),
        "avg_seconds_per_question": round(statistics.mean(r["seconds"] for r in rows), 1),
        "median_seconds_per_question": round(statistics.median(r["seconds"] for r in rows), 1),
        "retrieval": retrieval,
        "judge_vs_me": agreement(rows),
    }
    (EVAL / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    log("\n== Results ==")
    log(f"Correct: {summary['correct']}/{summary['graded']}   "
        f"(answerable {summary['answerable_correct']}/{summary['answerable']})")
    log(f"Unsupported answers: {summary['unsupported_answers']}/{summary['answers_given']}")
    log(f"Correct refusals: {summary['correct_refusals']}/{summary['unanswerable']}   "
        f"missed refusals: {summary['missed_refusals']}   wrong refusals: {summary['wrong_refusals']}")
    log(f"Answers with an invalid citation: {summary['invalid_citation_answers']}   "
        f"citation guardrail fired: {summary['guardrail_fired']}   errors: {summary['errors']}")
    log(f"Cost: {summary['avg_tokens_per_question']} tokens and {summary['avg_seconds_per_question']} s per question "
        f"(median {summary['median_seconds_per_question']} s)")
    if summary["judge_vs_me"]:
        log(f"Judge vs my grades: {json.dumps({k: v for k, v in summary['judge_vs_me'].items()})}")
    else:
        log("Judge vs my grades: eval/human_labels.csv is empty — grade from eval/grading_sheet.md first.")
    log("\nWrote eval/summary.json, results.csv, failures.csv, grading_sheet.md, retrieval_summary.csv")
    print(json.dumps({k: summary[k] for k in ("correct", "graded", "correct_refusals", "unanswerable",
                                               "wrong_refusals", "unsupported_answers", "answers_given")}))
    return 0


if __name__ == "__main__":
    sys.exit(main())
