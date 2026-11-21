"""
Assignment 3: evaluation (`main.py evaluate`).

Stages, in order (each saves its results in eval/, so a crash loses nothing):
  1. retrieval     hit rate at 1/3/5 for two designs: A plain vector search, B party filter
  2. agent         the agent answers every question          -> eval/agent_answers.jsonl
  3. grading sheet answers and evidence, WITHOUT any verdict -> eval/answers_for_grading.md
  4. code checks   citations valid? refusals correct?        -> eval/code_checks.csv
  5. judge         an LLM grades with eval/rubric.md         -> eval/judge_verdicts.jsonl
  6. agreement     the judge against YOUR eval/human_labels.csv
  7. summary       eval/summary.md and eval/failures.csv

Grade your 20+ answers by hand from the grading sheet BEFORE you read the judge's verdicts:
    uv run python evaluate.py --answers-only     # stages 1-3, no judge
    ... write eval/human_labels.csv ...
    uv run python main.py evaluate               # everything (finished stages are not repeated)
Options: --retrieval-only, --answers-only, --fresh (forget saved agent answers and verdicts).
"""

import argparse
import csv
import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
HUMAN_LABELS = EVAL / "human_labels.csv"
RUBRIC = EVAL / "rubric.md"
ANSWERS = EVAL / "agent_answers.jsonl"
VERDICTS = EVAL / "judge_verdicts.jsonl"

KS = (1, 3, 5)
PAUSE_SECONDS = 6          # between agent questions, to stay under the free tier's requests-per-minute limit
RETRIEVED_CHARS = 14000    # how much retrieved text the judge sees

PARTY_WORDS = {            # design B: which party does the question name?
    "PSOE": r"\bpsoe\b|socialist",
    "PP": r"\bpp\b|popular party|people'?s party|partido popular",
    "SUMAR": r"\bsumar\b",
    "VOX": r"\bvox\b",
}
CITATION = re.compile(r"\[([A-Za-z0-9_]+),\s*(pp?\.\s*\d+(?:\s*[-–]\s*\d+)?)\]")


# ============================================================================
# Reading the test set
# ============================================================================
def pages_of(text: str) -> tuple[int, int] | None:
    numbers = [int(n) for n in re.findall(r"\d+", text or "")]
    return (min(numbers), max(numbers)) if numbers else None


def load_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if (r.get("question") or "").strip()]
    for row in rows:
        row["kind"] = row["kind"].strip().lower()
        sources = [s.strip() for s in row["expected_source"].split(";") if s.strip()]
        locations = row["expected_location"].split(";")
        row["expected"] = [(s, pages_of(locations[i]) if i < len(locations) else None) for i, s in enumerate(sources)]
    return rows


def overlaps(pages: tuple[int, int] | None, start: int, end: int) -> bool:
    return pages is None or (start <= pages[1] and end >= pages[0])


def detect_parties(question: str) -> list[str]:
    return [party for party, pattern in PARTY_WORDS.items() if re.search(pattern, question, re.IGNORECASE)]


def write_csv(path: Path, rows: list[dict], columns: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(rows)


def read_jsonl(path: Path) -> dict:
    if not path.is_file():
        return {}
    records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return {r["id"]: r for r in records}


def append_jsonl(path: Path, record: dict) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


# ============================================================================
# Stage 1: retrieval
# ============================================================================
def retrieval_stage(questions: list[dict]) -> dict:
    """Hit rate at k: the share of answerable questions whose expected passage(s) are in the top k.

    A `multi` question counts as a hit only if ALL its expected passages are in the top k.
    """
    from index import retrieve

    designs = {
        "A plain vector search": lambda q: retrieve(q, k=max(KS)),
        "B party filter": lambda q: retrieve(q, k=max(KS), parties=detect_parties(q) or None),
    }
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    detail, summary = [], {}
    for name, search in designs.items():
        per_question = []
        for q in answerable:
            hits = search(q["question"])
            ranks = []
            for source, pages in q["expected"]:
                rank = next((i for i, h in enumerate(hits, start=1)
                             if h["source"] == source and overlaps(pages, h["page_start"], h["page_end"])), None)
                ranks.append(rank)
            row = {"id": q["id"], "kind": q["kind"], "design": name,
                   "ranks": ";".join(str(r) for r in ranks),
                   "words_in_top5": sum(h["n_words"] for h in hits[:5])}
            for k in KS:
                row[f"hit@{k}"] = int(bool(ranks) and all(r is not None and r <= k for r in ranks))
            per_question.append(row)
        detail += per_question
        summary[name] = {}
        for label, wanted in (("all", None), ("single", "single"), ("multi", "multi")):
            rows = [r for r in per_question if wanted is None or r["kind"] == wanted]
            if rows:
                summary[name][label] = {"n": len(rows), **{f"hit@{k}": round(sum(r[f"hit@{k}"] for r in rows) / len(rows), 3) for k in KS},
                                        "avg_words_in_top5": round(sum(r["words_in_top5"] for r in rows) / len(rows))}
    write_csv(EVAL / "retrieval_per_question.csv", detail,
              ["id", "kind", "design", "ranks", "hit@1", "hit@3", "hit@5", "words_in_top5"])
    (EVAL / "retrieval_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("\n=== Retrieval: hit rate (answerable questions only) ===")
    print(f"{'design':<24}{'questions':<12}{'hit@1':>7}{'hit@3':>7}{'hit@5':>7}   words in top 5")
    for name, groups in summary.items():
        for label, s in groups.items():
            print(f"{name:<24}{label + ' (' + str(s['n']) + ')':<12}{s['hit@1']:>7.2f}{s['hit@3']:>7.2f}{s['hit@5']:>7.2f}   {s['avg_words_in_top5']}")
    return summary


# ============================================================================
# Stage 2: the agent answers every question
# ============================================================================
def agent_stage(questions: list[dict], fresh: bool) -> dict:
    from agent import run_agent

    if fresh and ANSWERS.is_file():
        ANSWERS.unlink()
    done = read_jsonl(ANSWERS)
    todo = [q for q in questions if q["id"] not in done]
    print(f"\n=== Agent: {len(done)} answers saved, {len(todo)} to go ===")
    for number, q in enumerate(todo, start=1):
        record = None
        for attempt in range(3):
            try:
                outcome = run_agent(q["question"], interactive=False)
                record = {"id": q["id"], "question": q["question"], "kind": q["kind"], **outcome}
                break
            except Exception as error:  # noqa: BLE001 - e.g. a rate limit: wait and try again
                if type(error).__name__ == "AllModelsExhausted":
                    raise SystemExit(f"\nSTOP: {error}\nYour {len(done)} saved answers are kept. Run the command again later or with more models.")
                print(f"  {q['id']}: attempt {attempt + 1} failed ({type(error).__name__}: {str(error)[:120]})")
                time.sleep(20 * (attempt + 1))
        if record is None:
            print(f"  {q['id']}: giving up for now; run the command again to retry it.")
            continue
        append_jsonl(ANSWERS, record)
        done[q["id"]] = record
        print(f"  {q['id']} ({number}/{len(todo)}): {record['tokens']['total']} tokens, {record['seconds']}s, "
              f"{len(record['tool_calls'])} tool call(s)")
        time.sleep(PAUSE_SECONDS)
    return done


def retrieved_text(record: dict) -> str:
    return "\n\n".join(c["result"] for c in record["tool_calls"] if c["tool"] == "search")


# ============================================================================
# Stage 3: the grading sheet (no verdicts in it)
# ============================================================================
def grading_sheet(questions: list[dict], answers: dict) -> None:
    lines = ["# Answers to grade by hand",
             "",
             "For at least 20 of these, write a row in `eval/human_labels.csv`: `id,correct,supported,notes`.",
             "- `correct` = 1 if the answer matches the reference, or if it properly refuses an unanswerable question.",
             "- `supported` = 1 if every claim in the answer is in the retrieved passages below.",
             "- `notes` = why, for every 0.",
             "",
             "Do this BEFORE looking at the judge's verdicts.", ""]
    for q in questions:
        a = answers.get(q["id"])
        if not a:
            continue
        lines += [f"## {q['id']} ({q['kind']})", f"**Question:** {q['question']}",
                  f"**Reference answer:** {q['reference_answer']}",
                  f"**Expected:** {q['expected_source'] or '-'} {q['expected_location'] or ''}", "",
                  "**Agent answer:**", "", a["answer"], "", "**Retrieved passages:**", ""]
        for passage in retrieved_text(a).split("\n\nPassage ")[:6]:
            if passage.strip():
                lines.append("> " + passage.strip().replace("\n", " ")[:900])
                lines.append("")
        lines.append("")
    (EVAL / "answers_for_grading.md").write_text("\n".join(lines), encoding="utf-8")
    template = EVAL / "human_labels_template.csv"
    if not template.is_file():
        write_csv(template, [{"id": q["id"], "correct": "", "supported": "", "notes": ""} for q in questions],
                  ["id", "correct", "supported", "notes"])
    print(f"\nGrading sheet written: {EVAL / 'answers_for_grading.md'}")


# ============================================================================
# Stage 4: checks that code can do
# ============================================================================
def citations_in(text: str) -> list[tuple[str, tuple[int, int]]]:
    return [(source, pages_of(location)) for source, location in CITATION.findall(text)]


def code_checks(questions: list[dict], answers: dict) -> dict:
    rows = {}
    for q in questions:
        a = answers.get(q["id"])
        if not a:
            continue
        answer = a["answer"]
        refused = answer.strip().upper().startswith("NOT COVERED") or a.get("guardrail") == "neutrality"
        retrieved = citations_in(retrieved_text(a))
        cited = citations_in(answer)
        valid = all(any(src == s and pg and r and pg[0] <= r[1] and pg[1] >= r[0] for s, r in retrieved) for src, pg in cited)
        expected_found = bool(q["expected"]) and all(
            any(src == s and overlaps(pg, r[0], r[1]) for s, r in retrieved if r) for src, pg in q["expected"])
        unanswerable = q["kind"] == "unanswerable"
        rows[q["id"]] = {
            "id": q["id"], "kind": q["kind"], "refused": int(refused),
            "refusal_ok": int(refused) if unanswerable else int(not refused),
            "n_citations": len(cited), "citations_valid": int(valid) if cited else "",
            "cites_when_answering": "" if refused else int(bool(cited)),
            "expected_passage_retrieved": "" if unanswerable else int(expected_found),
            "guardrail": a.get("guardrail") or "",
        }
    write_csv(EVAL / "code_checks.csv", list(rows.values()), list(next(iter(rows.values())).keys()) if rows else ["id"])
    return rows


# ============================================================================
# Stage 5: the LLM judge
# ============================================================================
def call_judge(prompt: str) -> dict:
    """Ask Gemini for a JSON verdict. JUDGE_MODEL overrides the model; default: the agent's model chain.

    When a model has used up its free daily requests, the next model in the chain is used.
    """
    import os

    from google import genai
    from google.genai import types

    from agent import choose_model, is_daily_quota, mark_exhausted
    from api_key import load_api_key

    client = genai.Client(api_key=load_api_key())
    config = types.GenerateContentConfig(temperature=0, response_mime_type="application/json")
    attempt = 0
    while attempt < 6:
        model = os.environ.get("JUDGE_MODEL") or choose_model()
        try:
            reply = client.models.generate_content(model=model, contents=prompt, config=config)
            verdict = json.loads(reply.text)
            verdict["judge_model"] = model
            return verdict
        except Exception as error:  # noqa: BLE001 - rate limits and the odd malformed reply
            if is_daily_quota(error):
                mark_exhausted(model)
                print(f"  judge: {model} has used up its free requests for today. Switching model...")
                if os.environ.get("JUDGE_MODEL"):
                    raise SystemExit(f"JUDGE_MODEL={model} is out of free requests. Unset it or choose another model.")
                continue
            attempt += 1
            print(f"  judge attempt {attempt} failed ({type(error).__name__}: {str(error)[:100]})")
            time.sleep(15 * attempt)
    raise RuntimeError("the judge failed 6 times in a row")


def judge_prompt(q: dict, a: dict) -> str:
    return (f"{RUBRIC.read_text(encoding='utf-8')}\n\n---\n\n"
            f"Question kind: {q['kind']}\nQuestion: {q['question']}\n"
            f"Reference answer: {q['reference_answer']}\n\n"
            f"Retrieved passages:\n{retrieved_text(a)[:RETRIEVED_CHARS] or '(none: the assistant retrieved nothing)'}\n\n"
            f"Assistant's answer:\n{a['answer']}\n")


def judge_stage(questions: list[dict], answers: dict, fresh: bool) -> dict:
    if fresh and VERDICTS.is_file():
        VERDICTS.unlink()
    done = read_jsonl(VERDICTS)
    todo = [q for q in questions if q["id"] in answers and q["id"] not in done]
    print(f"\n=== Judge: {len(done)} verdicts saved, {len(todo)} to go ===")
    for q in todo:
        verdict = call_judge(judge_prompt(q, answers[q["id"]]))
        record = {"id": q["id"], "correct": int(verdict["correct"]), "supported": int(verdict["supported"]),
                  "refused": int(verdict.get("refused", 0)), "reason": str(verdict.get("reason", "")),
                  "judge_model": verdict.get("judge_model")}
        append_jsonl(VERDICTS, record)
        done[q["id"]] = record
        time.sleep(PAUSE_SECONDS)
    return done


# ============================================================================
# Stage 6: does the judge agree with you?
# ============================================================================
def kappa(a: list[int], b: list[int]) -> float:
    n = len(a)
    observed = sum(x == y for x, y in zip(a, b)) / n
    expected = sum((a.count(v) / n) * (b.count(v) / n) for v in (0, 1))
    return 1.0 if expected == 1 else round((observed - expected) / (1 - expected), 3)


def agreement(verdicts: dict) -> dict:
    if not HUMAN_LABELS.is_file():
        return {}
    with HUMAN_LABELS.open(newline="", encoding="utf-8") as f:
        human = {r["id"].strip(): r for r in csv.DictReader(f) if (r.get("id") or "").strip()}
    shared = [i for i in human if i in verdicts and str(human[i]["correct"]).strip() in ("0", "1")
              and str(human[i]["supported"]).strip() in ("0", "1")]
    if not shared:
        return {}
    result = {"n": len(shared)}
    lines = ["# Judge vs. human grades", ""]
    for field in ("correct", "supported"):
        h = [int(human[i][field]) for i in shared]
        j = [verdicts[i][field] for i in shared]
        result[field] = {"agree": sum(x == y for x, y in zip(h, j)), "rate": round(sum(x == y for x, y in zip(h, j)) / len(shared), 3),
                         "kappa": kappa(h, j)}
        lines.append(f"- **{field}**: agree on {result[field]['agree']}/{len(shared)} ({result[field]['rate']:.0%}), Cohen's kappa {result[field]['kappa']}")
    lines += ["", "## Disagreements", ""]
    for i in shared:
        for field in ("correct", "supported"):
            if int(human[i][field]) != verdicts[i][field]:
                lines.append(f"- **{i} / {field}**: you said {human[i][field]}, judge said {verdicts[i][field]}. "
                             f"Your note: {human[i].get('notes', '')!r}. Judge's reason: {verdicts[i]['reason']!r}")
    (EVAL / "judge_agreement.md").write_text("\n".join(lines), encoding="utf-8")
    result["graded_by_hand"] = len(shared)
    return result


# ============================================================================
# Stage 7: summary and failure sheet
# ============================================================================
def auto_cause(q: dict, check: dict, verdict: dict) -> str:
    """A first guess for the failure class. YOU decide the final one in the `your_cause` column."""
    unanswerable = q["kind"] == "unanswerable"
    if unanswerable and not check["refused"]:
        return "unsupported claim (answered an unanswerable question)"
    if not unanswerable and check["refused"]:
        return "wrong refusal"
    if not verdict["supported"]:
        return "unsupported claim"
    if not unanswerable and not verdict["correct"]:
        return "retrieval miss" if check["expected_passage_retrieved"] == 0 else "wrong answer from the right passage"
    return ""


def summary_stage(questions, answers, checks, verdicts, agree, retrieval) -> None:
    n = len(answers)
    by_id = {q["id"]: q for q in questions}
    answerable = [i for i in answers if by_id[i]["kind"] != "unanswerable"]
    unanswerable = [i for i in answers if by_id[i]["kind"] == "unanswerable"]

    def pct(count: int, total: int) -> str:
        return f"{count}/{total} ({count / total:.0%})" if total else "n/a"

    cited = [c for c in checks.values() if c["citations_valid"] != ""]
    lines = ["# Evaluation summary", "",
             f"Questions answered: {n}. Agent model: {next(iter(answers.values()))['model']}. "
             f"Judge model: {next(iter(verdicts.values()))['judge_model']}.", "",
             "## Results (judge)", "",
             f"- Correct, answerable questions: {pct(sum(verdicts[i]['correct'] for i in answerable), len(answerable))}",
             f"- Correct refusals, unanswerable questions: {pct(sum(checks[i]['refused'] for i in unanswerable), len(unanswerable))}",
             f"- Wrong refusals, answerable questions: {pct(sum(checks[i]['refused'] for i in answerable), len(answerable))}",
             f"- Answers with every claim supported: {pct(sum(v['supported'] for v in verdicts.values()), len(verdicts))}",
             "", "## Code checks", "",
             f"- Answers whose citations all match a retrieved passage: {pct(sum(c['citations_valid'] for c in cited), len(cited))}",
             f"- Non-refusals that cite something: {pct(sum(c['cites_when_answering'] for c in checks.values() if c['cites_when_answering'] != ''), sum(1 for c in checks.values() if c['cites_when_answering'] != ''))}",
             f"- Expected passage retrieved by the agent: {pct(sum(checks[i]['expected_passage_retrieved'] for i in answerable), len(answerable))}", ""]
    if agree:
        lines += ["## Judge vs. your grades", "",
                  f"- Graded by hand: {agree['graded_by_hand']} answers",
                  f"- `correct`: agree on {agree['correct']['agree']}/{agree['n']} ({agree['correct']['rate']:.0%}), kappa {agree['correct']['kappa']}",
                  f"- `supported`: agree on {agree['supported']['agree']}/{agree['n']} ({agree['supported']['rate']:.0%}), kappa {agree['supported']['kappa']}", ""]
    else:
        lines += ["## Judge vs. your grades", "", "- No usable rows in eval/human_labels.csv yet.", ""]
    totals = [a["tokens"] for a in answers.values()]
    lines += ["## Cost per question", "",
              f"- Tokens: {sum(t['input'] for t in totals) / n:.0f} in + {sum(t['output'] for t in totals) / n:.0f} out "
              f"= {sum(t['total'] for t in totals) / n:.0f} total (average over {n} questions)",
              f"- Seconds: {sum(a['seconds'] for a in answers.values()) / n:.1f} on average, "
              f"{max(a['seconds'] for a in answers.values()):.1f} at most (agent only; the judge is extra)",
              f"- Tool calls: {sum(len(a['tool_calls']) for a in answers.values()) / n:.1f} on average",
              f"- Embeddings: one per distinct question (cached in index/query_cache.json)", ""]
    (EVAL / "summary.md").write_text("\n".join(lines), encoding="utf-8")
    (EVAL / "summary.json").write_text(json.dumps({"retrieval": retrieval, "agreement": agree}, indent=2), encoding="utf-8")

    failures = []
    for i, q in by_id.items():
        if i in answers and i in verdicts:
            cause = auto_cause(q, checks[i], verdicts[i])
            if cause or not verdicts[i]["correct"]:
                failures.append({"id": i, "kind": q["kind"], "question": q["question"], "auto_cause": cause,
                                 "judge_reason": verdicts[i]["reason"], "your_cause": ""})
    write_csv(EVAL / "failures.csv", failures, ["id", "kind", "question", "auto_cause", "judge_reason", "your_cause"])
    print("\n" + "\n".join(lines))
    print(f"Failures to classify yourself: {len(failures)} -> eval/failures.csv (fill in `your_cause`)")


# ============================================================================
def main() -> int:
    parser = argparse.ArgumentParser(description="Evaluate the system.")
    parser.add_argument("--retrieval-only", action="store_true")
    parser.add_argument("--answers-only", action="store_true", help="stages 1-3: no judge, so you can grade first")
    parser.add_argument("--fresh", action="store_true", help="discard saved agent answers and judge verdicts")
    args = parser.parse_args()

    questions = load_questions()
    print(f"{len(questions)} questions: " + ", ".join(f"{sum(q['kind'] == k for q in questions)} {k}" for k in ("single", "multi", "unanswerable")))
    retrieval = retrieval_stage(questions)
    if args.retrieval_only:
        return 0
    answers = agent_stage(questions, args.fresh)
    grading_sheet(questions, answers)
    if args.answers_only:
        print("Now grade 20+ answers in eval/human_labels.csv, then run: uv run python main.py evaluate")
        return 0
    if not HUMAN_LABELS.is_file() or sum(1 for _ in HUMAN_LABELS.open()) < 21:
        print("\nWARNING: eval/human_labels.csv has fewer than 20 graded answers. Grade them BEFORE reading the judge's verdicts.")
    checks = code_checks(questions, answers)
    verdicts = judge_stage(questions, answers, args.fresh)
    agree = agreement(verdicts)
    summary_stage(questions, answers, checks, verdicts, agree, retrieval)
    return 0


if __name__ == "__main__":
    sys.exit(main())

