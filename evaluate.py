"""
Assignment 3: evaluation (`main.py evaluate`).

What it does, in order:
  1. Retrieval: hit rate at 1/3/5 for each retrieval design (from compare_retrieval.py).
  2. Answers: runs your agent on EVERY question in eval/questions.csv (add_document is always
     refused here). Answers are saved in eval/agent_answers.jsonl, so a second run only does the
     missing ones. Use `--fresh` to throw them away and ask everything again.
  3. Code checks: citations are real, refusals use the fixed sentence, the right article was
     retrieved, tool calls, time, tokens.
  4. LLM judge: another model reads the question, the reference answer, the passages the agent
     retrieved and the agent's answer, and gives two verdicts (rubric below). Saved in
     eval/judge_results.jsonl.
  5. Agreement with you: compares the judge with eval/human_labels.csv (made with grade.py).
  6. Results: eval/evaluation_results.csv (one row per question) and eval/evaluation_summary.json.

Options: --fresh (ask everything again), --limit N (only the first N questions), --skip-retrieval.
"""

import argparse
import contextlib
import csv
import hashlib
import io
import json
import os
import re
import statistics
import sys
import time
from collections import Counter
from dataclasses import asdict
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import agent  # noqa: E402  (your agent: ask(), REFUSAL, CITED_ID, PASSAGE)

EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
ANSWERS = EVAL / "agent_answers.jsonl"
JUDGE = EVAL / "judge_results.jsonl"
HUMAN = EVAL / "human_labels.csv"
RESULTS_CSV = EVAL / "evaluation_results.csv"
SUMMARY_JSON = EVAL / "evaluation_summary.json"
RETRIEVAL_JSON = EVAL / "retrieval_summary.json"

JUDGE_MODELS = [os.environ["JUDGE_MODEL"]] if os.environ.get("JUDGE_MODEL") else [
    "gemini-3.5-flash-lite", "gemini-3.1-flash-lite"]
JUDGE_WAITS = (5, 15, 30)       # seconds to wait between tries of one judge model
PAUSE = 2                       # seconds between questions, to be kind to the rate limit
EVIDENCE_CHARS = 60000          # most text of retrieved passages shown to the judge

RUBRIC = """You are a strict grader of a question-answering assistant about Spanish labour law
(a collective agreement for the glass, ceramics and extractive industries, the 2026 minimum wage
decree, and key articles of the Estatuto de los Trabajadores).

You get: the QUESTION, the REFERENCE answer (written and checked by a person), the PASSAGES the
assistant retrieved (the only evidence it had), and the assistant's ANSWER. Give two verdicts.

correct
  * Answerable question: true only if the main facts of the ANSWER (numbers, durations, conditions,
    the right group, the right year) agree with the REFERENCE and nothing in it contradicts the
    REFERENCE. Extra correct detail is fine. A missing main fact, a wrong number or a wrong group
    is false. Pay figures given for a year other than the one in the REFERENCE are wrong; if the
    question names no year, the REFERENCE year (2026) is the right one. A refusal ("No encuentro
    esto en los documentos") to an answerable question is false.
  * Unanswerable question (the REFERENCE says what the documents do not contain): true only if the
    ANSWER says the documents do not cover it and does NOT state the missing figure or rule as a
    fact. Saying what the documents do cover is fine. Guessing or computing the missing figure is false.

supported
  * true only if every factual claim in the ANSWER can be found in the PASSAGES. A claim that is
    true in real life but not in the PASSAGES is NOT supported. Wrong or missing citations do not
    matter here; judge the content. A plain refusal is supported.

Be literal and do not give the benefit of the doubt. Write "reason" as one short sentence in
English naming the specific fact that decided each verdict."""


# ---------------------------------------------------------------- small helpers

def read_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r["question"].strip()]


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    rows = []
    for line in path.open(encoding="utf-8"):
        try:
            rows.append(json.loads(line))
        except json.JSONDecodeError:
            continue  # a half-written last line from an interrupted run
    return rows


def write_jsonl(path: Path, rows) -> None:
    tmp = path.with_suffix(".tmp")
    tmp.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in rows), encoding="utf-8")
    tmp.replace(path)


def answer_key(question: dict, answer: str) -> str:
    text = f"{question['question']}|{question['reference_answer']}|{answer}"
    return hashlib.sha1(text.encode()).hexdigest()[:16]


def as_bool(value) -> bool | None:
    value = str(value).strip().lower()
    if value in ("1", "y", "yes", "true", "s", "si", "sí", "t"):
        return True
    if value in ("0", "n", "no", "false", "f"):
        return False
    return None


def evidence_passages(record: dict) -> list[tuple[str, str]]:
    """Every passage the agent's searches returned: [(id, text)], each once."""
    seen: dict[str, str] = {}
    for call in record.get("trace", []):
        if call.get("tool") != "search" or call.get("status") != "ok":
            continue
        text = call.get("result", "")
        found = list(agent.PASSAGE.finditer(text))
        for n, m in enumerate(found):
            end = found[n + 1].start() if n + 1 < len(found) else len(text)
            seen.setdefault(m["id"], text[m.start():end].strip())
    return list(seen.items())


# ---------------------------------------------------------------- 1. retrieval

def run_retrieval() -> dict:
    """Hit rates per design. Re-computed by compare_retrieval.py (no cost: question vectors are saved)."""
    try:
        import compare_retrieval
        with contextlib.redirect_stdout(io.StringIO()):
            compare_retrieval.main()
    except Exception as error:  # noqa: BLE001
        print(f"  (could not recompute; using the saved eval/retrieval_summary.json: {type(error).__name__}: {error})")
    return json.loads(RETRIEVAL_JSON.read_text(encoding="utf-8")) if RETRIEVAL_JSON.exists() else {}


def print_retrieval(summary: dict) -> None:
    if not summary:
        print("  no retrieval summary found; run compare_retrieval.py")
        return
    print(f"  {'design':<28}{'hit@1':>7}{'hit@3':>7}{'hit@5':>7}   words in prompt (top 5)")
    for label, s in summary.items():
        n = s["questions"]
        print(f"  {label:<28}{100 * s['hit@1'] / n:>6.0f}%{100 * s['hit@3'] / n:>6.0f}%"
              f"{100 * s['hit@5'] / n:>6.0f}%   {s['words_top5']}")


# ---------------------------------------------------------------- 2. answers

def never_approve(tool_name: str, args: dict) -> bool:
    return False  # the evaluation never adds documents


def collect_answers(questions: list[dict], fresh: bool) -> dict[str, dict]:
    saved = {} if fresh else {r["id"]: r for r in read_jsonl(ANSWERS)}
    todo = [q for q in questions
            if not (q["id"] in saved and saved[q["id"]]["question"] == q["question"]
                    and not saved[q["id"]].get("error"))]
    print(f"  {len(questions) - len(todo)} answers already saved, {len(todo)} to ask")
    for n, q in enumerate(todo, 1):
        print(f"  [{n}/{len(todo)}] {q['id']}: {q['question']}", flush=True)
        result = agent.ask(q["question"], approve=never_approve)
        saved[q["id"]] = {"id": q["id"], **asdict(result)}
        note = f"error: {result.error[:100]}" if result.error else (
            "refused" if result.refused else f"answered, {len(result.sources)} source(s)")
        print(f"      -> {note}; {result.tool_calls} tool call(s), {result.seconds}s, "
              f"citation check: {result.guardrail}", flush=True)
        write_jsonl(ANSWERS, [saved[x["id"]] for x in questions if x["id"] in saved])
        time.sleep(PAUSE)
    return saved


# ---------------------------------------------------------------- 3. code checks

def load_chunks() -> dict[str, dict]:
    from retrieval import Retriever
    return {c["chunk_id"]: c for c in Retriever("B").chunks}


def expected_found(question: dict, passage_ids, chunks: dict[str, dict]) -> bool | None:
    """Did the searches return every article the answer needs? None for unanswerable questions."""
    if question["kind"] == "unanswerable":
        return None
    import compare_retrieval as cr
    retrieved = [chunks[i] for i in passage_ids if i in chunks]
    return all(any(cr.matches(c, pair) for c in retrieved) for pair in cr.expected_pairs(question))


def code_checks(question: dict, record: dict, chunks: dict[str, dict]) -> dict:
    retrieved_ids = [i for i, _ in evidence_passages(record)]
    cited = list(dict.fromkeys(agent.CITED_ID.findall(record.get("answer", ""))))
    refused = bool(record.get("refused"))
    return {
        "errored": bool(record.get("error")),
        "refused": refused,
        "cited_ids": len(cited),
        "invalid_citations": [i for i in cited if i not in retrieved_ids],
        "searched": any(c.get("tool") == "search" for c in record.get("trace", [])),
        "expected_retrieved": expected_found(question, retrieved_ids, chunks),
        "limit_hit": any(c.get("status") == "limit_reached" for c in record.get("trace", [])),
    }


# ---------------------------------------------------------------- 4. judge

def judge_prompt(question: dict, record: dict) -> str:
    passages, total = [], 0
    for _, text in evidence_passages(record):
        if total + len(text) > EVIDENCE_CHARS:
            break
        passages.append(text)
        total += len(text)
    return (f"{RUBRIC}\n\nQUESTION kind: {question['kind']}\nQUESTION: {question['question']}\n\n"
            f"REFERENCE answer: {question['reference_answer']}\n\n"
            f"PASSAGES the assistant retrieved:\n" + ("\n\n".join(passages) or "(none)") +
            f"\n\nANSWER to grade:\n{record['answer']}\n")


def judge_one(question: dict, record: dict) -> dict:
    """One verdict {correct, supported, reason, model}. Tries each judge model, with waits between tries."""
    from google import genai
    from google.genai import types
    from pydantic import BaseModel

    from api_key import load_api_key

    class Verdict(BaseModel):
        correct: bool
        supported: bool
        reason: str

    client = genai.Client(api_key=load_api_key())
    prompt, last = judge_prompt(question, record), None
    for model in JUDGE_MODELS:
        for wait in (0,) + JUDGE_WAITS:
            time.sleep(wait)
            try:
                response = client.models.generate_content(
                    model=model, contents=prompt,
                    config=types.GenerateContentConfig(response_mime_type="application/json",
                                                       response_schema=Verdict))
                verdict = Verdict.model_validate_json(response.text)
                return {"correct": verdict.correct, "supported": verdict.supported,
                        "reason": verdict.reason.strip(), "model": model}
            except Exception as error:  # noqa: BLE001 - busy model, quota, bad JSON: try again
                last = f"{type(error).__name__}: {str(error)[:150]}"
                print(f"      judge {model}: {last}", file=sys.stderr, flush=True)
    return {"correct": None, "supported": None, "reason": f"judge failed: {last}", "model": ""}


def collect_judgements(questions: list[dict], answers: dict[str, dict]) -> dict[str, dict]:
    saved = {r["id"]: r for r in read_jsonl(JUDGE)}
    todo = []
    for q in questions:
        rec = answers.get(q["id"])
        if not rec or rec.get("error"):
            continue
        old = saved.get(q["id"])
        if not (old and old.get("key") == answer_key(q, rec["answer"]) and old.get("correct") is not None):
            todo.append(q)
    print(f"  {len(saved)} verdicts saved, {len(todo)} to judge")
    for n, q in enumerate(todo, 1):
        verdict = judge_one(q, answers[q["id"]])
        saved[q["id"]] = {"id": q["id"], "key": answer_key(q, answers[q["id"]]["answer"]), **verdict}
        print(f"  [{n}/{len(todo)}] {q['id']}: correct={verdict['correct']} supported={verdict['supported']}",
              flush=True)
        write_jsonl(JUDGE, [saved[x["id"]] for x in questions if x["id"] in saved])
    return saved


# ---------------------------------------------------------------- 5. agreement with the person

def read_human() -> dict[str, dict]:
    if not HUMAN.exists():
        return {}
    labels = {}
    with HUMAN.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            correct, supported = as_bool(r.get("correct", "")), as_bool(r.get("supported", ""))
            if (r.get("id") or "").strip() and correct is not None and supported is not None:
                labels[r["id"].strip()] = {"correct": correct, "supported": supported, "notes": r.get("notes", "")}
    return labels


def cohen_kappa(a: list[bool], b: list[bool]) -> float | None:
    n = len(a)
    if n == 0:
        return None
    observed = sum(x == y for x, y in zip(a, b)) / n
    pa, pb = sum(a) / n, sum(b) / n
    expected = pa * pb + (1 - pa) * (1 - pb)
    return None if expected == 1 else (observed - expected) / (1 - expected)


def agreement(human: dict[str, dict], judged: dict[str, dict]) -> dict:
    ids = [i for i in human if i in judged and judged[i].get("correct") is not None]
    out = {"graded": len(ids)}
    for field in ("correct", "supported"):
        h, j = [human[i][field] for i in ids], [judged[i][field] for i in ids]
        out[field] = {"agree": sum(x == y for x, y in zip(h, j)), "of": len(ids),
                      "kappa": None if cohen_kappa(h, j) is None else round(cohen_kappa(h, j), 2)}
    out["disagreements"] = [
        {"id": i, "human_correct": human[i]["correct"], "judge_correct": judged[i]["correct"],
         "human_supported": human[i]["supported"], "judge_supported": judged[i]["supported"],
         "judge_reason": judged[i]["reason"], "human_notes": human[i]["notes"]}
        for i in ids if (human[i]["correct"], human[i]["supported"]) != (judged[i]["correct"], judged[i]["supported"])]
    return out


# ---------------------------------------------------------------- 6. outcome per question

def outcome(question: dict, record: dict | None, checks: dict | None, verdict: dict | None) -> tuple[str, str]:
    """(outcome, failure_guess). Outcomes: correct, unsupported, incorrect, wrong_refusal,
    correct_refusal, answered_anyway, blocked, error, not_judged."""
    if not record or record.get("error"):
        return "error", "agent error (no answer; run evaluate again to retry it)"
    if record.get("guardrail") == "blocked":
        return "blocked", "citation guardrail blocked the answer"
    if not verdict or verdict.get("correct") is None:
        return "not_judged", ""
    if question["kind"] == "unanswerable":
        if checks["refused"] and verdict["correct"]:
            return "correct_refusal", ""
        return "answered_anyway", "answered a question the documents do not cover"
    if checks["refused"]:
        return "wrong_refusal", ("retrieval miss" if checks["expected_retrieved"] is False
                                 else "refused although the right passage was retrieved")
    if verdict["correct"] and verdict["supported"]:
        return "correct", ""
    if not verdict["supported"]:
        return "unsupported", ("retrieval miss" if checks["expected_retrieved"] is False
                               else "claim not in the retrieved passages")
    return "incorrect", ("retrieval miss" if checks["expected_retrieved"] is False
                         else "wrong answer although the right passage was retrieved")


def share(n: int, total: int) -> str:
    return f"{n}/{total} ({100 * n / total:.0f}%)" if total else "0/0"


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate the agent on eval/questions.csv.")
    parser.add_argument("--fresh", action="store_true", help="ask every question again (replaces saved answers)")
    parser.add_argument("--limit", type=int, help="only the first N questions")
    parser.add_argument("--skip-retrieval", action="store_true")
    args = parser.parse_args()

    questions = read_questions()[:args.limit] if args.limit else read_questions()
    n_un = sum(q["kind"] == "unanswerable" for q in questions)
    print(f"{len(questions)} questions: {len(questions) - n_un} answerable, {n_un} unanswerable\n")

    print("== 1/5  Retrieval: hit rate per design ==")
    retrieval = {} if args.skip_retrieval else run_retrieval()
    if args.skip_retrieval and RETRIEVAL_JSON.exists():
        retrieval = json.loads(RETRIEVAL_JSON.read_text(encoding="utf-8"))
    print_retrieval(retrieval)

    print("\n== 2/5  Agent answers ==")
    answers = collect_answers(questions, args.fresh)

    print("\n== 3/5  Code checks ==")
    chunks = load_chunks()
    checks = {q["id"]: code_checks(q, answers[q["id"]], chunks) for q in questions if q["id"] in answers}

    print("\n== 4/5  LLM judge ==")
    judged = collect_judgements(questions, answers)

    print("\n== 5/5  Agreement with your grades ==")
    human = read_human()
    agree = agreement(human, judged) if human else {"graded": 0}
    if human:
        print(f"  {agree['graded']} answers graded by you")
        for field in ("correct", "supported"):
            a = agree[field]
            print(f"  {field:<10}: judge agrees with you on {share(a['agree'], a['of'])}, Cohen's kappa {a['kappa']}")
        for d in agree["disagreements"]:
            print(f"    {d['id']}: you correct={d['human_correct']} supported={d['human_supported']} | judge "
                  f"correct={d['judge_correct']} supported={d['judge_supported']}: {d['judge_reason']}")
    else:
        print("  eval/human_labels.csv has no graded answers yet. Run `uv run python grade.py`.")

    # ---- results
    rows, counts = [], Counter()
    for q in questions:
        rec, chk, ver = answers.get(q["id"]), checks.get(q["id"]), judged.get(q["id"])
        result, guess = outcome(q, rec, chk, ver)
        counts[(q["kind"], result)] += 1
        counts[("all", result)] += 1
        hum = human.get(q["id"], {})
        rows.append({
            "id": q["id"], "kind": q["kind"], "outcome": result, "failure_guess": guess,
            "judge_correct": ver.get("correct") if ver else "", "judge_supported": ver.get("supported") if ver else "",
            "human_correct": hum.get("correct", ""), "human_supported": hum.get("supported", ""),
            "refused": chk["refused"] if chk else "", "expected_retrieved": chk["expected_retrieved"] if chk else "",
            "cited_ids": chk["cited_ids"] if chk else "", "invalid_citations": ";".join(chk["invalid_citations"]) if chk else "",
            "guardrail": rec["guardrail"] if rec else "", "tool_calls": rec["tool_calls"] if rec else "",
            "seconds": rec["seconds"] if rec else "",
            "tokens": (rec["input_tokens"] + rec["output_tokens"]) if rec else "",
            "model": rec["model"] if rec else "", "judge_reason": ver["reason"] if ver else "",
            "question": q["question"], "answer": (rec["answer"] if rec else "").replace("\n", " ")})
    with RESULTS_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    unanswerable = [q for q in questions if q["kind"] == "unanswerable"]
    c = lambda kind, name: counts[(kind, name)]  # noqa: E731
    ans_all = lambda name: sum(c(k, name) for k in ("single", "multi"))  # noqa: E731
    print("\n" + "=" * 72)
    print("RESULTS (judge's verdicts; see eval/evaluation_results.csv for every question)")
    print("=" * 72)
    print(f"Answerable questions ({len(answerable)}):")
    for name, text in (("correct", "correct and supported"), ("unsupported", "claims not in the passages"),
                       ("incorrect", "supported but wrong"), ("wrong_refusal", "refused although answerable"),
                       ("blocked", "blocked by the citation guardrail"), ("error", "agent error")):
        print(f"  {text:<36}{share(ans_all(name), len(answerable))}")
    print(f"  by kind: single {share(c('single', 'correct'), sum(q['kind'] == 'single' for q in answerable))} "
          f"correct, multi {share(c('multi', 'correct'), sum(q['kind'] == 'multi' for q in answerable))} correct")
    print(f"Unanswerable questions ({len(unanswerable)}):")
    for name, text in (("correct_refusal", "correct refusals"), ("answered_anyway", "answered anyway"),
                       ("blocked", "blocked by the citation guardrail"), ("error", "agent error")):
        print(f"  {text:<36}{share(c('unanswerable', name), len(unanswerable))}")

    misses = [q["id"] for q in answerable if checks.get(q["id"]) and not checks[q["id"]]["errored"]
              and checks[q["id"]]["expected_retrieved"] is False]
    print(f"\nRight article(s) not among the 5 passages the agent retrieved: {share(len(misses), len(answerable))}"
          + (f" -> {', '.join(misses)}" if misses else ""))
    problems = [i for i, k in checks.items() if k["invalid_citations"]]
    print(f"Answers citing an id that search never returned: {len(problems)}")
    print(f"Answers whose citation check fired: "
          f"{sum(1 for r in answers.values() if r.get('guardrail') in ('fixed_on_retry', 'blocked'))} "
          f"(fixed on retry {sum(1 for r in answers.values() if r.get('guardrail') == 'fixed_on_retry')}, "
          f"blocked {sum(1 for r in answers.values() if r.get('guardrail') == 'blocked')})")

    recs = [answers[q["id"]] for q in questions if q["id"] in answers and not answers[q["id"]].get("error")]
    seconds = [r["seconds"] for r in recs]
    tokens = [r["input_tokens"] + r["output_tokens"] for r in recs]
    calls = Counter(r["tool_calls"] for r in recs)
    summary = {
        "questions": len(questions), "answered": len(recs),
        "outcomes": {f"{k}/{o}": n for (k, o), n in sorted(counts.items())},
        "retrieval": retrieval, "agreement": agree,
        "tool_calls_distribution": {str(k): v for k, v in sorted(calls.items())},
        "limit_hit": sum(1 for k in checks.values() if k["limit_hit"]),
        "seconds_mean": round(statistics.mean(seconds), 1) if seconds else None,
        "seconds_median": round(statistics.median(seconds), 1) if seconds else None,
        "seconds_max": max(seconds) if seconds else None,
        "tokens_mean": round(statistics.mean(tokens)) if tokens else None,
        "input_tokens_total": sum(r["input_tokens"] for r in recs),
        "output_tokens_total": sum(r["output_tokens"] for r in recs),
        "models": dict(Counter(r["model"] for r in recs)),
        "judge_models": dict(Counter(v.get("model", "") for v in judged.values())),
    }
    SUMMARY_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    if recs:
        print(f"\nPer question: {summary['seconds_mean']}s on average (median {summary['seconds_median']}s, "
              f"slowest {summary['seconds_max']}s), {summary['tokens_mean']} tokens on average.")
        print("Tool calls per question: " + ", ".join(f"{k} call(s): {v}" for k, v in sorted(calls.items()))
              + f"; limit of {agent.MAX_TOOL_CALLS} reached in {summary['limit_hit']} question(s).")
    print("\nNote: the model has no fixed temperature, so another run can give slightly different "
          "answers. Your grades in eval/human_labels.csv belong to the answers saved in "
          "eval/agent_answers.jsonl; do not use --fresh after grading unless you grade again.")
    print(f"\nsaved: {RESULTS_CSV.relative_to(ROOT)}, {SUMMARY_JSON.relative_to(ROOT)}, "
          f"{ANSWERS.relative_to(ROOT)}, {JUDGE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
