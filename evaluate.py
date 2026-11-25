"""
Assignment 3: evaluation (`main.py evaluate`).

Part 1, retrieval: hit rate at k = 1, 3, 5 for each design in retrieval.py,
on every answerable question. -> eval/retrieval_results.csv, retrieval_summary.csv

Part 2, answers: the agent (agent.py) answers every question; add_document is
always refused. Each answer is saved as it arrives in eval/answers.jsonl, and a
re-run only asks the questions that have no saved answer.

Part 3, code checks: refusal, quotes word for word in the retrieved text,
citations pointing to retrieved passages, retrieval hit of the expected passage.

Part 4, LLM judge: a rubric, the reference answer and the retrieved text as
evidence -> correct and supported, with a reason. Cached in eval/judge.jsonl.

Part 5: agreement with eval/human_labels.csv, a suggested failure category for
each failed question, and cost. -> eval/results.csv, eval/summary.md

    uv run python evaluate.py                 # everything (what main.py evaluate runs)
    uv run python evaluate.py --answers-only  # parts 2-3 and the grading sheet, no judge
"""

import argparse
import csv
import hashlib
import json
import re
import statistics
import sys
import time
from pathlib import Path

import agent
import index as ix
import retrieval

ROOT = Path(__file__).resolve().parent
EVAL_DIR = ROOT / "eval"
QUESTIONS = EVAL_DIR / "questions.csv"
ANSWERS = EVAL_DIR / "answers.jsonl"
JUDGE = EVAL_DIR / "judge.jsonl"
HUMAN = EVAL_DIR / "human_labels.csv"
KS = (1, 3, 5)
EVAL_MODELS = agent.MODELS[:1]  # the main model only, so every answer comes from the same model


def load_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r["question"].strip()]


def expected_passages(row: dict) -> list[tuple[str, str, int]]:
    """[(source, 'Chapter XIII', 9), …] from expected_source / expected_location."""
    sources = [s.strip() for s in row["expected_source"].split(";")]
    locations = [loc.strip() for loc in row["expected_location"].split(";")]
    if len(sources) == 1:
        sources *= len(locations)
    passages = []
    for source, location in zip(sources, locations):
        match = re.fullmatch(r"(Chapter [IVXLC]+), ¶(\d+)", location)
        if not match:
            raise ValueError(f"{row['id']}: cannot read location {location!r}")
        passages.append((source, match.group(1), int(match.group(2))))
    return passages


def covers(hit: dict, passage: tuple[str, str, int]) -> bool:
    """Does this retrieved chunk contain the expected paragraph?"""
    source, chapter, paragraph = passage
    first, _, last = hit["paragraphs"].partition("-")
    return (hit["source"] == source
            and hit["chapter"].split(":")[0] == chapter
            and int(first) <= paragraph <= int(last or first))


def found_rank(hits: list[dict], passage) -> int | None:
    return next((rank for rank, hit in enumerate(hits, 1) if covers(hit, passage)), None)


def evaluate_retrieval(questions: list[dict]) -> list[dict]:
    searcher = retrieval.get_searcher()
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    results, summary = [], []
    for design in retrieval.DESIGNS:
        for q in answerable:
            hits = searcher.search(q["question"], k=max(KS), design=design)
            ranks = [found_rank(hits, p) for p in expected_passages(q)]
            results.append({
                "id": q["id"], "kind": q["kind"], "design": design,
                "ranks": ";".join(str(r) if r else "-" for r in ranks),
                **{f"all@{k}": int(all(r and r <= k for r in ranks)) for k in KS},
                **{f"any@{k}": int(any(r and r <= k for r in ranks)) for k in KS},
                "words@3": sum(len(h["text"].split()) for h in hits[:3]),
                "words@5": sum(len(h["text"].split()) for h in hits[:5]),
                "top_hit": f"{hits[0]['source']} | {hits[0]['location']}",
            })
        rows = [r for r in results if r["design"] == design]
        multi = [r for r in rows if r["kind"] == "multi"]
        summary.append({
            "design": design,
            **{f"hit@{k}": round(sum(r[f"all@{k}"] for r in rows) / len(rows), 3) for k in KS},
            **{f"multi_both@{k}": round(sum(r[f"all@{k}"] for r in multi) / len(multi), 3) for k in KS},
            **{f"multi_any@{k}": round(sum(r[f"any@{k}"] for r in multi) / len(multi), 3) for k in KS},
            "avg_words@3": round(sum(r["words@3"] for r in rows) / len(rows)),
            "avg_words@5": round(sum(r["words@5"] for r in rows) / len(rows)),
        })

    write_csv(EVAL_DIR / "retrieval_results.csv", results)
    write_csv(EVAL_DIR / "retrieval_summary.csv", summary)
    print(f"\nRetrieval on {len(answerable)} answerable questions "
          f"(hit = every expected passage in the top k; multi_any = at least one)\n")
    print_table(summary)
    return summary


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def print_table(rows: list[dict]) -> None:
    columns = list(rows[0])
    widths = [max(len(c), *(len(str(r[c])) for r in rows)) for c in columns]
    print("  ".join(c.ljust(w) for c, w in zip(columns, widths)))
    for r in rows:
        print("  ".join(str(r[c]).ljust(w) for c, w in zip(columns, widths)))


# --------------------------------------------------------------------------- part 2: answers

def read_jsonl(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return {r["id"]: r for r in rows}


def run_answers(questions: list[dict]) -> dict[str, dict]:
    """Ask the agent every question that has no saved answer; save each one as it arrives."""
    answers = read_jsonl(ANSWERS)
    todo = [q for q in questions if q["id"] not in answers]
    print(f"\n=== Part 2: answers ({len(answers)} saved, {len(todo)} to ask)", file=sys.stderr)
    for n, q in enumerate(todo, 1):
        try:
            # One model for the whole evaluation (no fallback), retried patiently when busy.
            result = agent.ask(q["question"], approve=lambda call: False, models=EVAL_MODELS, retries=5)
        except Exception as error:  # noqa: BLE001 - keep going; a re-run retries this one
            print(f"  {q['id']} failed ({type(error).__name__}: {str(error)[:120]}); re-run to retry", file=sys.stderr)
            continue
        result["id"] = q["id"]
        with ANSWERS.open("a", encoding="utf-8") as f:
            f.write(json.dumps(result, ensure_ascii=False) + "\n")
        answers[q["id"]] = result
        print(f"  [{n}/{len(todo)}] {q['id']} {result['seconds']}s {result['models']}", file=sys.stderr)
    return answers


# --------------------------------------------------------------------------- part 3: code checks

REFUSAL = re.compile(
    r"(don['’]t|do not|does not|doesn['’]t) (cover|address|discuss|contain|mention)"
    r"|not (covered|included|discussed|addressed|mentioned) in"
    r"|(can['’]t|cannot|unable to) (answer|find)", re.I)
WARNING = "⚠ Could not verify in the course texts"


def code_checks(question: dict, answer: dict) -> dict:
    text = answer["answer"]
    body = text.split(WARNING)[0]
    hits = agent.parse_hits(answer["retrieved_text"])
    problems = agent.check_answer(body, hits)
    quotes = agent.quotes_in(body)
    citations = agent.citations_in(body)
    refused = bool(REFUSAL.search(body)) and not quotes
    expected = expected_passages(question) if question["kind"] != "unanswerable" else []
    retrieved = [{"source": h["source"], "chapter": h["chapter"], "paragraphs": f"{h['first']}-{h['last']}"} for h in hits]
    found = [any(covers(h, p) for h in retrieved) for p in expected]
    return {
        "refused": int(refused),
        "quotes": len(quotes),
        "quotes_ok": int(not any("quote" in p for p in problems)),
        "citations": len(citations),
        "citations_ok": int(not any("citation" in p for p in problems)),
        "flagged": int(WARNING in text),
        "retrieval_hit": int(all(found)) if expected else "",
        "retrieval_any": int(any(found)) if expected else "",
        "searches": sum(1 for c in answer["tool_calls"] if c["name"] == "search"),
    }


# --------------------------------------------------------------------------- part 4: LLM judge

# The judges are full flash models, not the model that wrote the answers (flash-lite), so it does
# not grade itself. Each allows only 20 requests a day on the free tier, so the next one takes over
# when one runs out. On 25 Nov 2026 gemini-3-flash-preview judged q01-q21, then it ran out and
# gemini-3.5-flash was overloaded (503) for hours, so flash-lite, the last resort, judged q22-q35
# (see REPORT.md). Each verdict records its judge; when all are used up the run stops and the next
# run continues where it stopped (verdicts are saved in eval/judge.jsonl).
JUDGE_MODELS = ["gemini-3-flash-preview", "gemini-3.5-flash", "gemini-3.5-flash-lite"]
used_up: set[str] = set()  # judges whose daily limit ran out during this run
RUBRIC = """You grade answers from a revision assistant for A-level Politics students. The assistant
must answer only from passages of Hobbes (Leviathan), Locke (Second Treatise) and Mill (On Liberty)
returned by its search tool, and must say so when they do not cover the question.

Grade two things, each 1 or 0.

correct
  Answerable question: 1 if the answer states the main point of the reference answer (wording may
  differ; extra true detail is fine) and contradicts nothing in it; 0 if it misses the main point,
  gets it wrong, or refuses.
  Unanswerable question: 1 if the answer says the course texts do not cover it and does not go on to
  answer from general knowledge; 0 if it answers the question anyway.

supported
  1 if every factual claim and every quotation in the answer can be found in the RETRIEVED PASSAGES
  (a refusal that only describes what the corpus contains counts as supported); 0 if any claim,
  name, date, section number or quotation is not in them, even if it is true.

Reply with JSON: {"correct": 0 or 1, "supported": 0 or 1, "reason": "one sentence"}."""


def judge_one(question: dict, answer: dict) -> dict:
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=agent.load_api_key())
    prompt = (f"{RUBRIC}\n\nQUESTION ({question['kind']}): {question['question']}\n\n"
              f"REFERENCE ANSWER: {question['reference_answer']}\n\n"
              f"RETRIEVED PASSAGES:\n{answer['retrieved_text'] or '(none)'}\n\n"
              f"ANSWER TO GRADE:\n{answer['answer']}")
    config = types.GenerateContentConfig(temperature=0, response_mime_type="application/json")
    for attempt in range(4):  # busy models (503): a few patient tries (failed tries seem to count against the daily limit)
        available = [m for m in JUDGE_MODELS if m not in used_up]
        if not available:
            raise ix.QuotaExhausted("every judge model reached its daily limit")
        model = available[0]
        try:
            response = client.models.generate_content(model=model, contents=prompt, config=config)
            verdict = json.loads(response.text)
            usage = response.usage_metadata
            return {"correct": int(verdict["correct"]), "supported": int(verdict["supported"]),
                    "reason": verdict.get("reason", ""), "judge_model": model,
                    "judge_tokens": (usage.prompt_token_count or 0) + (usage.candidates_token_count or 0)}
        except Exception as error:  # noqa: BLE001 - overloaded model or bad JSON: wait and retry
            if "PerDay" in str(error) or "per day" in str(error).lower():
                used_up.add(model)  # daily limit: switch to the next judge
                continue
            if "429" in str(error):  # per-minute limit: wait for the next minute
                time.sleep(60)
                continue
            if not agent.is_temporary(error) and not isinstance(error, (json.JSONDecodeError, KeyError)):
                raise
            time.sleep(60)
    raise RuntimeError(f"judge failed for {question['id']}")


def run_judge(questions: list[dict], answers: dict[str, dict]) -> dict[str, dict]:
    """Judge every answer; a verdict is reused while the answer it graded is unchanged."""
    verdicts = read_jsonl(JUDGE)
    print("\n=== Part 4: LLM judge", file=sys.stderr)
    for q in questions:
        if q["id"] not in answers:
            continue
        digest = hashlib.sha1(answers[q["id"]]["answer"].encode()).hexdigest()[:12]
        if verdicts.get(q["id"], {}).get("answer_sha") == digest:
            continue
        try:
            verdict = judge_one(q, answers[q["id"]]) | {"id": q["id"], "answer_sha": digest}
        except ix.QuotaExhausted:
            print(f"  Daily limit of every judge model reached: {len(verdicts)} of {len(answers)} judged. "
                  "Run again tomorrow to judge the rest.", file=sys.stderr)
            break
        verdicts[q["id"]] = verdict
        JUDGE.write_text("".join(json.dumps(v, ensure_ascii=False) + "\n" for v in verdicts.values()), encoding="utf-8")
        print(f"  {q['id']} correct={verdict['correct']} supported={verdict['supported']}", file=sys.stderr)
    return verdicts


# --------------------------------------------------------------------------- part 5: results

def suggest_failure(q: dict, checks: dict, verdict: dict) -> str:
    """A first guess at the cause; the final category is decided by hand in REPORT.md."""
    if q["kind"] == "unanswerable":
        return "" if checks["refused"] and verdict.get("correct", 1) else "unsupported claim (answered from memory)"
    if checks["refused"]:
        return "wrong refusal" + ("" if checks["retrieval_any"] else " (after retrieval miss)")
    if not verdict.get("correct", 1):
        return "wrong answer from the right passage" if checks["retrieval_any"] else "retrieval miss"
    if not verdict.get("supported", 1) or not checks["quotes_ok"] or not checks["citations_ok"]:
        return "unsupported claim"
    return ""


def read_human() -> dict[str, dict]:
    if not HUMAN.exists():
        return {}
    with HUMAN.open(newline="", encoding="utf-8") as f:
        return {r["id"].strip(): r for r in csv.DictReader(f)
                if (r.get("id") or "").strip() and (r.get("correct") or "").strip() in ("0", "1")}


def kappa(pairs: list[tuple[int, int]]) -> float | None:
    """Cohen's kappa: agreement corrected for the agreement expected by chance."""
    n = len(pairs)
    if not n:
        return None
    observed = sum(a == b for a, b in pairs) / n
    p_a, p_b = sum(a for a, _ in pairs) / n, sum(b for _, b in pairs) / n
    expected = p_a * p_b + (1 - p_a) * (1 - p_b)
    return round((observed - expected) / (1 - expected), 2) if expected < 1 else 1.0


def summarise(questions, answers, verdicts) -> None:
    human = read_human()
    rows = []
    for q in questions:
        if q["id"] not in answers:
            continue
        a, v = answers[q["id"]], verdicts.get(q["id"], {})
        checks = code_checks(q, a)
        h = human.get(q["id"], {})
        rows.append({
            "id": q["id"], "kind": q["kind"], **checks,
            "judge_correct": v.get("correct", ""), "judge_supported": v.get("supported", ""),
            "human_correct": h.get("correct", ""), "human_supported": h.get("supported", ""),
            "suggested_failure": suggest_failure(q, checks, v) if v else "",
            "judge_reason": v.get("reason", ""),
            "input_tokens": a["input_tokens"], "output_tokens": a["output_tokens"],
            "model_calls": a["model_calls"], "seconds": a["seconds"], "models": " ".join(a["models"]),
            "guardrail": " | ".join(a["guardrail_events"]),
        })
    write_csv(EVAL_DIR / "results.csv", rows)

    answerable = [r for r in rows if r["kind"] != "unanswerable"]
    unanswerable = [r for r in rows if r["kind"] == "unanswerable"]
    judged = [r for r in rows if r["judge_correct"] != ""]
    lines = ["# Evaluation summary", "",
             f"{len(rows)} answers ({len(answerable)} answerable, {len(unanswerable)} unanswerable), "
             f"{len(judged)} judged, {len(human)} graded by hand.", "",
             "## Code checks", "",
             f"- Correct refusals (unanswerable refused): {sum(r['refused'] for r in unanswerable)}/{len(unanswerable)}",
             f"- Wrong refusals (answerable refused): {sum(r['refused'] for r in answerable)}/{len(answerable)}",
             f"- Answers with every quote verbatim in the retrieved text: {sum(r['quotes_ok'] for r in rows)}/{len(rows)} "
             f"({sum(r['quotes'] for r in rows)} quotes)",
             f"- Answers with every citation pointing to a retrieved passage: {sum(r['citations_ok'] for r in rows)}/{len(rows)}",
             f"- Answerable answers with no citation: {sum(1 for r in answerable if not r['refused'] and not r['citations'])}",
             f"- Answers flagged by the quote guardrail: {sum(r['flagged'] for r in rows)}; "
             f"guardrail asked for a rewrite: {sum(1 for r in rows if 'quote check:' in r['guardrail'])}",
             f"- Expected passage(s) retrieved by the agent: {sum(r['retrieval_hit'] for r in answerable)}/{len(answerable)} "
             f"(at least one: {sum(r['retrieval_any'] for r in answerable)})", ""]
    if judged:
        ja = [r for r in judged if r["kind"] != "unanswerable"]
        ju = [r for r in judged if r["kind"] == "unanswerable"]
        lines += ["## LLM judge", "",
                  f"- Answerable, correct: {sum(r['judge_correct'] for r in ja)}/{len(ja)}",
                  f"- Answerable, unsupported (a claim not in the retrieved text): {sum(1 - r['judge_supported'] for r in ja)}/{len(ja)}",
                  f"- Unanswerable, correct refusal: {sum(r['judge_correct'] for r in ju)}/{len(ju)}",
                  f"- All answers, correct and supported: {sum(r['judge_correct'] and r['judge_supported'] for r in judged)}/{len(judged)}", ""]
        both = [r for r in judged if r["human_correct"] != ""]
        if both:
            pc = [(int(r["human_correct"]), r["judge_correct"]) for r in both]
            ps = [(int(r["human_supported"]), r["judge_supported"]) for r in both if r["human_supported"] != ""]
            lines += ["## Judge vs human", "",
                      f"- correct: agree on {sum(a == b for a, b in pc)}/{len(pc)} ({sum(a == b for a, b in pc) / len(pc):.0%}), Cohen's kappa {kappa(pc)}",
                      f"- supported: agree on {sum(a == b for a, b in ps)}/{len(ps)} ({sum(a == b for a, b in ps) / max(len(ps), 1):.0%}), Cohen's kappa {kappa(ps)}",
                      "- Disagreements: " + (", ".join(f"{r['id']} (human {r['human_correct']}/{r['human_supported']}, "
                                                        f"judge {r['judge_correct']}/{r['judge_supported']})"
                                                        for r in both if (int(r["human_correct"]), int(r["human_supported"] or -1))
                                                        != (r["judge_correct"], r["judge_supported"])) or "none"), ""]
        failures = [r for r in judged if r["suggested_failure"]]
        lines += ["## Failures (suggested cause)", ""] + [f"- {r['id']} ({r['kind']}): {r['suggested_failure']}. {r['judge_reason']}" for r in failures] + [""]
    seconds = [r["seconds"] for r in rows]
    tokens = [r["input_tokens"] + r["output_tokens"] for r in rows]
    lines += ["## Cost per question", "",
              f"- Tokens: mean {statistics.mean(tokens):,.0f} (input {statistics.mean(r['input_tokens'] for r in rows):,.0f}, "
              f"output {statistics.mean(r['output_tokens'] for r in rows):,.0f}), max {max(tokens):,}",
              f"- Seconds: median {statistics.median(seconds):.1f}, mean {statistics.mean(seconds):.1f}, max {max(seconds):.1f}",
              f"- Model calls: mean {statistics.mean(r['model_calls'] for r in rows):.1f}; searches: mean {statistics.mean(r['searches'] for r in rows):.1f}",
              f"- Judge tokens per answer: mean {statistics.mean(v.get('judge_tokens', 0) for v in verdicts.values()):,.0f}" if verdicts else "", ""]
    (EVAL_DIR / "summary.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n" + "\n".join(lines))


def grading_sheet(questions, answers) -> None:
    """A Markdown sheet for grading by hand, without the judge's verdicts."""
    out = ["# Grading sheet", "",
           "Grade each answer in eval/human_labels.csv before looking at eval/judge.jsonl or eval/results.csv.",
           "correct = 1 if it states the reference's main point (unanswerable: it declines without answering from memory).",
           "supported = 1 if every claim and quote is in the retrieved passages below it.", ""]
    for q in questions:
        a = answers.get(q["id"])
        if not a:
            continue
        out += [f"## {q['id']} ({q['kind']})", "", f"**Question:** {q['question']}", "",
                f"**Reference:** {q['reference_answer']}", "", "**Agent's answer:**", "",
                "\n".join("> " + line for line in a["answer"].splitlines()), "",
                "<details><summary>Retrieved passages</summary>", "", "```", a["retrieved_text"] or "(none)", "```",
                "", "</details>", ""]
    (EVAL_DIR / "grading_sheet.md").write_text("\n".join(out), encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate retrieval and the agent end to end.")
    parser.add_argument("--answers-only", action="store_true", help="answers and code checks only, no judge")
    args = parser.parse_args()
    questions = load_questions()
    print("=== Part 1: retrieval", file=sys.stderr)
    evaluate_retrieval(questions)
    answers = run_answers(questions)
    grading_sheet(questions, answers)
    verdicts = {} if args.answers_only else run_judge(questions, answers)
    summarise(questions, answers, verdicts)


if __name__ == "__main__":
    main()
