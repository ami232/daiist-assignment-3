"""
Assignment 3: evaluation (`main.py evaluate`).

Stage 1, retrieval: Hit@1/3/5, recall@5 and words added to the prompt for every
retrieval design in rag.RETRIEVAL_DESIGNS, over the answerable questions of
eval/questions.csv -> eval/retrieval.csv (per question) and
eval/retrieval_summary.csv (per design). Query vectors are cached, so a re-run
embeds nothing new.

Stage 2, end to end: the agent (agent.py, add_document always denied so the
shipped index never changes) answers every question -> eval/answers.jsonl,
resumable: ids already there are skipped. Then code checks on each answer
(refusal phrase, citations present in that run's search results, expected
source cited, BOE notice) -> eval/checks.csv.

Stage 3, judge: gemini-3.5-flash (stronger than the agent) grades each answer
with the student's rubric (eval/judge_rubric.md), given the question, its kind,
the reference answer and the full text of every retrieved fragment ->
eval/judge.csv (resumable). Then agreement with eval/human_labels.csv (% and
Cohen's kappa per column) and the totals -> eval/summary.json.

Stage 4, failure review: every question that failed a code check, or that you or
the judge graded 0, plus multi questions citing only part of what was expected
-> eval/failures.csv (`cause` and `why` filled in by hand, kept on re-runs) and
eval/failures.md (counts by cause, answer, grades, notes and retrieved fragments).

Started from session 10's 07-own-harness/evaluate.py.
"""

import asyncio
import csv
import json
import logging
import sys
import time
from pathlib import Path

import index as ix
import rag

ROOT = Path(__file__).resolve().parent
EVAL_DIR = ROOT / "eval"
QUESTIONS = EVAL_DIR / "questions.csv"
RETRIEVAL_CSV = EVAL_DIR / "retrieval.csv"
RETRIEVAL_SUMMARY = EVAL_DIR / "retrieval_summary.csv"
ANSWERS = EVAL_DIR / "answers.jsonl"
CHECKS_CSV = EVAL_DIR / "checks.csv"
RUBRIC = EVAL_DIR / "judge_rubric.md"
JUDGE_CSV = EVAL_DIR / "judge.csv"
HUMAN_LABELS = EVAL_DIR / "human_labels.csv"
SUMMARY_JSON = EVAL_DIR / "summary.json"
FAILURES_CSV = EVAL_DIR / "failures.csv"
FAILURES_MD = EVAL_DIR / "failures.md"
CAUSES = ("retrieval miss", "wrong answer from the right passage", "unsupported claim",
          "wrong refusal", "bad test question", "not a failure")
JUDGE_MODEL = "gemini-3.5-flash"   # a stronger model than the agent's, so it doesn't share its blind spots
KS = (1, 3, 5)
PAUSE = 4            # seconds between questions: stays under the free tier's requests-per-minute


def read_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r["question"].strip()]


def expected_pairs(row: dict) -> list[tuple[str, str]]:
    """[(source, location)] from the `;`-separated columns (one source may apply to every location)."""
    sources = [s.strip() for s in row["expected_source"].split(";") if s.strip()]
    locations = [loc.strip() for loc in row["expected_location"].split(";") if loc.strip()]
    if len(sources) == 1:
        sources *= len(locations)
    if len(sources) != len(locations):
        raise ValueError(f"{row['id']}: {len(sources)} sources but {len(locations)} locations")
    return list(zip(sources, locations))


def evaluate_retrieval(questions: list[dict]) -> list[dict]:
    answerable = [q for q in questions if q["kind"].strip() != "unanswerable"]
    rows = []
    for design, (chunking, mode) in rag.RETRIEVAL_DESIGNS.items():
        if ix.open_collection(chunking).count() == 0:
            print(f"  {design}: collection {chunking!r} is empty, skipped (run `main.py index`).")
            continue
        for q in answerable:
            pairs = expected_pairs(q)
            hits = rag.retrieve(q["question"], design, k=max(KS))
            found = [any(h.covers(s, loc) for s, loc in pairs) for h in hits]
            row = {"design": design, "chunking": chunking, "mode": mode, "id": q["id"], "kind": q["kind"]}
            for k in KS:
                row[f"hit@{k}"] = int(any(found[:k]))
            row["recall@5"] = round(sum(any(h.covers(s, loc) for h in hits) for s, loc in pairs) / len(pairs), 3)
            row["first_hit_rank"] = found.index(True) + 1 if any(found) else ""
            for k in KS:
                row[f"words@{k}"] = sum(h.meta["n_words"] for h in hits[:k])
            row["expected"] = "; ".join(f"[{s}, {loc}]" for s, loc in pairs)
            row["retrieved"] = "; ".join(h.citation for h in hits)
            rows.append(row)
    return rows


def summarise(rows: list[dict]) -> list[dict]:
    summary = []
    for design in dict.fromkeys(r["design"] for r in rows):
        mine = [r for r in rows if r["design"] == design]
        line = {"design": design, "chunking": mine[0]["chunking"], "mode": mine[0]["mode"], "questions": len(mine)}
        for k in KS:
            line[f"hit@{k}"] = round(sum(r[f"hit@{k}"] for r in mine) / len(mine), 3)
        line["recall@5"] = round(sum(r["recall@5"] for r in mine) / len(mine), 3)
        multi = [r for r in mine if r["kind"] == "multi"]
        line["multi_recall@5"] = round(sum(r["recall@5"] for r in multi) / len(multi), 3) if multi else ""
        for k in KS:
            line[f"words@{k}"] = round(sum(r[f"words@{k}"] for r in mine) / len(mine))
        summary.append(line)
    return summary


# --------------------------------------------------------------------------- #
# End to end: answers                                                          #
# --------------------------------------------------------------------------- #

def read_answers() -> dict[str, dict]:
    if not ANSWERS.is_file():
        return {}
    rows = [json.loads(line) for line in ANSWERS.read_text(encoding="utf-8").splitlines() if line.strip()]
    return {r["id"]: r for r in rows}


async def run_answers(questions: list[dict]) -> int:
    """Answer every question not yet in answers.jsonl, appending one line each. Returns how many are missing."""
    import agent

    done = read_answers()
    todo = [q for q in questions if q["id"] not in done]
    if not todo:
        return 0
    print(f"  {len(done)} already answered, {len(todo)} to go (model {agent.MODEL})")
    async with agent.open_agent(approve=agent.deny) as runner:
        for n, q in enumerate(todo, 1):
            for attempt in range(1, 4):
                try:
                    result = await agent.ask(runner, q["question"])
                    break
                except Exception as error:  # noqa: BLE001 - quota or network: wait, then keep what we have
                    per_minute = "429" in str(error) and "PerDay" not in str(error)
                    if per_minute and attempt < 3:
                        print(f"  {q['id']}: requests-per-minute limit, waiting 65s")
                        await asyncio.sleep(65)
                        continue
                    print(f"  {q['id']}: stopped ({type(error).__name__}: {str(error)[:200]}). Re-run to resume.")
                    return len(todo) - n + 1
            with ANSWERS.open("a", encoding="utf-8") as f:
                f.write(json.dumps({"id": q["id"], "kind": q["kind"], **result}, ensure_ascii=False) + "\n")
            flag = " guardrail:" + result["citation_guardrail"] if result["citation_guardrail"] else ""
            print(f"  {q['id']} {q['kind']:<12} {result['searches']} searches  {result['tokens']['total']:>6} tokens  "
                  f"{result['seconds']:>5.1f}s{flag}")
            if n < len(todo):
                time.sleep(PAUSE)
    return 0


# --------------------------------------------------------------------------- #
# End to end: code checks                                                      #
# --------------------------------------------------------------------------- #

def code_checks(q: dict, a: dict) -> dict:
    """What code can check exactly about one answer."""
    import agent

    text = a["answer"]
    cited = rag.citations_in(text)
    retrieved = {pair for c in a["retrieved_citations"] for pair in rag.citations_in(c)}
    invalid = [f"[{s}, {loc}]" for s, loc in cited if (s, loc) not in retrieved]
    refused = agent.REFUSAL in text
    answerable = q["kind"] != "unanswerable"
    expected = expected_pairs(q) if answerable else []
    hit = [pair for pair in expected if pair in cited]

    if not answerable:
        outcome = "correct_refusal" if refused and not cited else ("partial_on_unanswerable" if refused else "answered_unanswerable")
    elif refused and not cited:
        outcome = "wrong_refusal"
    else:
        outcome = "answered_partial" if refused else "answered"

    return {
        "id": q["id"],
        "kind": q["kind"],
        "outcome": outcome,
        "refused": int(refused),
        "n_citations": len(cited),
        "citations_valid": int(not invalid),
        "invalid_citations": "; ".join(invalid),
        "expected_cited": round(len(hit) / len(expected), 3) if expected else "",
        "any_expected_cited": (int(bool(hit)) if expected else ""),
        "boe_notice": int(rag.BOE_NOTICE in text) if cited else "",
        "searches": a["searches"],
        "guardrail": a["citation_guardrail"] or "",
        "stopped": a["stopped"] or "",
        "tokens": a["tokens"]["total"],
        "seconds": a["seconds"],
    }


def summarise_checks(rows: list[dict]) -> dict:
    n = len(rows)
    answerable = [r for r in rows if r["kind"] != "unanswerable"]
    answered = [r for r in answerable if r["outcome"] != "wrong_refusal"]
    with_citations = [r for r in rows if r["n_citations"]]
    count = lambda outcome: sum(r["outcome"] == outcome for r in rows)  # noqa: E731
    return {
        "questions": n,
        "answered": len(answered),
        "wrong_refusals": count("wrong_refusal"),
        "correct_refusals": count("correct_refusal"),
        "answered_unanswerable": count("answered_unanswerable") + count("partial_on_unanswerable"),
        "all_citations_valid": round(sum(r["citations_valid"] for r in rows) / n, 3),
        "expected_source_cited": round(sum(r["any_expected_cited"] for r in answered) / max(len(answered), 1), 3),
        "boe_notice_when_citing": round(sum(r["boe_notice"] for r in with_citations) / max(len(with_citations), 1), 3),
        "guardrail_fired": sum(bool(r["guardrail"]) for r in rows),
        "mean_tokens": round(sum(r["tokens"] for r in rows) / n),
        "mean_seconds": round(sum(r["seconds"] for r in rows) / n, 1),   # includes waits on rate limits
        "median_seconds": round(sorted(r["seconds"] for r in rows)[n // 2], 1),
        "mean_searches": round(sum(r["searches"] for r in rows) / n, 2),
    }


# --------------------------------------------------------------------------- #
# Judge                                                                        #
# --------------------------------------------------------------------------- #

def evidence(answer: dict) -> str:
    """Every passage the agent's searches returned, once each, labelled [SOURCE, Location]; BOE notice dropped."""
    passages: dict[str, str] = {}
    for output in answer["retrieved"]:
        for block in output.split("\n\n---\n\n"):
            block = block.strip()
            if not block.startswith("[") or "Cita: " not in block:
                continue                            # the BOE notice, or "no results"
            head, _, rest = block.partition("\n")
            label = head.split("Cita: ", 1)[1]      # "[LETA, Artículo 1] · Ley 20/2007 … · texto consolidado a …"
            text = f"{label}\n{rest}"               # whole text as key: parts of one article share label and path
            passages.setdefault(text, text)
    return "\n\n---\n\n".join(passages.values()) or "(no fragments were retrieved)"


JUDGE_INPUT = """# Inputs

Question id: {id}
Category: {kind}

Question:
{question}

Reference answer:
{reference}

Retrieved fragments (everything the agent's searches returned):
{evidence}

Agent's answer:
{answer}"""


def judge_answers(questions: list[dict], answers: dict[str, dict]) -> dict[str, dict]:
    """Grade every answered question not yet in judge.csv. Returns all verdicts, by id."""
    from langchain_google_genai import ChatGoogleGenerativeAI
    from pydantic import BaseModel, Field

    from api_key import load_api_key

    class Verdict(BaseModel):
        # notes first, so the model gives its reasons before the scores
        id: str = Field(description="The question id.")
        notes: str = Field(description="The reason: wrong or unsupported claims, missing reference items, "
                                       "rule 3/4 phrasing problems. One or two sentences.")
        correct: int = Field(ge=0, le=1, description="1 or 0, per the 'correct' section of the rubric.")
        supported: int = Field(ge=0, le=1, description="1 or 0, per the 'supported' section of the rubric.")

    done = read_csv(JUDGE_CSV)
    todo = [q for q in questions if q["id"] in answers and q["id"] not in done]
    if todo:
        load_api_key()
        judge = ChatGoogleGenerativeAI(model=JUDGE_MODEL, temperature=0, max_retries=2).with_structured_output(Verdict)
        rubric = RUBRIC.read_text(encoding="utf-8")
        print(f"  {len(done)} already judged, {len(todo)} to go (model {JUDGE_MODEL})")
        for n, q in enumerate(todo, 1):
            a = answers[q["id"]]
            prompt = rubric + "\n\n" + JUDGE_INPUT.format(
                id=q["id"], kind=q["kind"], question=q["question"], reference=q["reference_answer"],
                evidence=evidence(a), answer=a["answer"])
            for attempt in range(1, 4):
                try:
                    verdict = judge.invoke(prompt)
                    break
                except Exception as error:  # noqa: BLE001 - rate limit, overload or network: wait, else resume later
                    per_day = "PerDay" in str(error) or "per day" in str(error).lower()
                    if attempt < 3 and not per_day:   # a daily quota won't clear by waiting: stop and resume tomorrow
                        wait = 65 if any(code in str(error) for code in ("429", "503")) else 10
                        print(f"  {q['id']}: {type(error).__name__}: {str(error)[:60]}… waiting {wait}s")
                        time.sleep(wait)
                        continue
                    print(f"  {q['id']}: judge stopped ({type(error).__name__}: {str(error)[:200]}). Re-run to resume.")
                    return done
            done[q["id"]] = {"id": q["id"], "kind": q["kind"], "correct": str(verdict.correct),
                             "supported": str(verdict.supported), "notes": verdict.notes}
            write_csv(JUDGE_CSV, [done[x["id"]] for x in questions if x["id"] in done])
            print(f"  {q['id']} {q['kind']:<12} correct {verdict.correct}  supported {verdict.supported}")
            if n < len(todo):
                time.sleep(PAUSE)
    return done


def cohen_kappa(a: list[int], b: list[int]) -> float | None:
    """Agreement beyond chance between two raters on the same items (None when chance agreement is total)."""
    n = len(a)
    observed = sum(x == y for x, y in zip(a, b)) / n
    expected = sum((a.count(c) / n) * (b.count(c) / n) for c in set(a) | set(b))
    return None if expected == 1 else round((observed - expected) / (1 - expected), 3)


def agreement(human: dict[str, dict], judge: dict[str, dict]) -> dict:
    ids = [i for i in human if i in judge]
    result = {"n": len(ids)}
    for column in ("correct", "supported"):
        h = [int(human[i][column]) for i in ids]
        j = [int(judge[i][column]) for i in ids]
        result[column] = {
            "agreement": round(sum(x == y for x, y in zip(h, j)) / len(ids), 3) if ids else None,
            "kappa": cohen_kappa(h, j) if ids else None,
            "human_1s": sum(h), "judge_1s": sum(j),
            "disagree": [f"{i} (human {x}, judge {y})" for i, x, y in zip(ids, h, j) if x != y],
        }
    return result


# --------------------------------------------------------------------------- #
# Failure review                                                               #
# --------------------------------------------------------------------------- #

def failure_reasons(check: dict, judge: dict | None, human: dict | None) -> list[str]:
    """Why one answer goes into the failure review (empty list: it doesn't)."""
    reasons = []
    if check["outcome"] == "wrong_refusal":
        reasons.append("refused an answerable question")
    if check["outcome"] == "answered_unanswerable":
        reasons.append("answered an unanswerable question without the refusal phrase")
    if str(check["citations_valid"]) == "0":
        reasons.append("cites a passage that was not retrieved")
    if check.get("stopped"):
        reasons.append(f"stopped ({check['stopped']})")
    if check.get("guardrail"):
        reasons.append(f"guardrail ({check['guardrail']})")
    if check["outcome"] == "answered" and str(check.get("any_expected_cited")) == "0":
        reasons.append("cites none of the expected sources")
    elif (check["outcome"] == "answered" and check["kind"] == "multi"
          and check.get("expected_cited") not in ("", None) and float(check["expected_cited"]) < 1):
        reasons.append(f"cites {float(check['expected_cited']):.0%} of the expected passages")
    for who, grades in (("human", human), ("judge", judge)):
        for column, label in (("correct", "incorrect"), ("supported", "unsupported")):
            if grades and grades.get(column) == "0":
                reasons.append(f"{who}: {label}")
    return reasons


def write_failure_review(questions: list[dict], answers: dict[str, dict], checks: list[dict],
                         verdicts: dict[str, dict], human: dict[str, dict]) -> list[dict]:
    """eval/failures.csv (one row per failure) and eval/failures.md (counts by cause, then the evidence).

    The `cause` and `why` columns are filled in by hand; a re-run keeps them for every id still in the review.
    """
    by_id = {c["id"]: c for c in checks}
    previous = read_csv(FAILURES_CSV)
    rows, details = [], []
    for q in questions:
        if q["id"] not in by_id:
            continue
        a, c = answers[q["id"]], by_id[q["id"]]
        reasons = failure_reasons(c, verdicts.get(q["id"]), human.get(q["id"]))
        if not reasons:
            continue
        expected = [f"[{s}, {loc}]" for s, loc in expected_pairs(q)] if q["kind"] != "unanswerable" else []
        retrieved = set(a["retrieved_citations"])
        h, j, old = human.get(q["id"], {}), verdicts.get(q["id"], {}), previous.get(q["id"], {})
        rows.append({
            "id": q["id"], "kind": q["kind"], "reasons": "; ".join(reasons),
            "human_correct": h.get("correct", ""), "human_supported": h.get("supported", ""),
            "judge_correct": j.get("correct", ""), "judge_supported": j.get("supported", ""),
            "outcome": c["outcome"],
            "expected": "; ".join(expected),
            "expected_retrieved": "; ".join(e for e in expected if e in retrieved),
            "expected_not_retrieved": "; ".join(e for e in expected if e not in retrieved),
            "cited": "; ".join(a["citations"]),
            "searches": c["searches"], "cause": old.get("cause", ""), "why": old.get("why", ""),
        })
        r = rows[-1]
        details += [
            f'<a id="{q["id"]}"></a>', "", f"## {q['id']} ({q['kind']}): {q['question']}", "",
            f"**Reasons:** {r['reasons']}  ",
            f"**Cause:** {r['cause'] or '(to classify)'}  ",
            f"**Why:** {r['why'] or '—'}", "",
            f"**Expected:** {r['expected'] or '(no answer in the corpus)'}  ",
            f"**Retrieved by the agent ({c['searches']} searches):** {', '.join(a['retrieved_citations']) or '(none)'}  ",
            f"**Expected but not retrieved:** {r['expected_not_retrieved'] or '(none)'}  ",
            f"**Cited:** {r['cited'] or '(none)'}", "",
            "**Searches:** " + "; ".join(f"`{s['args'].get('query', '')}`" for s in a["trace"]
                                         if s.get("call") == "search"), "",
            f"**Reference answer (Spanish, as in the test set):** {q['reference_answer']}", "",
            "**Agent's answer (Spanish):**", "", *[f"> {line}" for line in a["answer"].splitlines()], "",
            "| | correct | supported | notes |", "|---|---|---|---|",
            f"| Human | {h.get('correct', '')} | {h.get('supported', '')} | {h.get('notes', '').replace('|', '/')} |",
            f"| Judge | {j.get('correct', '')} | {j.get('supported', '')} | {j.get('notes', '').replace('|', '/')} |", "",
            "<details><summary>Retrieved fragments</summary>", "", "```text", evidence(a), "```", "",
            "</details>", "", "---", ""]
    if not rows:
        return rows
    write_csv(FAILURES_CSV, rows)
    unclassified = [r["id"] for r in rows if r["cause"] not in CAUSES]
    by_cause = ["| cause | count | ids |", "|---|---|---|",
                *[f"| {cause} | {sum(r['cause'] == cause for r in rows)} | "
                  f"{', '.join(r['id'] for r in rows if r['cause'] == cause)} |" for cause in CAUSES]]
    if unclassified:
        by_cause.append(f"| (not classified yet) | {len(unclassified)} | {', '.join(unclassified)} |")
    table = ["| id | kind | reasons | expected but not retrieved | cause |", "|---|---|---|---|---|",
             *[f"| [{r['id']}](#{r['id']}) | {r['kind']} | {r['reasons']} | {r['expected_not_retrieved'] or '—'} "
               f"| {r['cause']} |" for r in rows]]
    head = ["# Failure review", "",
            f"Generated by `evaluate.py` from `checks.csv`, `judge.csv` and `human_labels.csv`: {len(rows)} "
            "questions. A question is included if it fails a code check, if the human or the judge graded it 0, "
            "or if it is a `multi` question that cites only part of the expected passages.", "",
            "`cause` and `why` are filled in by hand in `eval/failures.csv`, with one of: "
            + ", ".join(f"*{c}*" for c in CAUSES) + ". A re-run keeps them.", "",
            "\"Retrieved by the agent\" means the citations its own searches returned in that run, not those in "
            "`retrieval.csv` (which searches with the literal question text). Questions, reference answers, "
            "agent answers and the human notes stay in Spanish, the language of the use case.", "",
            "## Failures by cause", "", *by_cause, "", "## All failures", ""]
    FAILURES_MD.write_text("\n".join(head + table + ["", "---", ""] + details), encoding="utf-8")
    return rows


def read_csv(path: Path) -> dict[str, dict]:
    if not path.is_file():
        return {}
    with path.open(newline="", encoding="utf-8") as f:
        return {r["id"]: r for r in csv.DictReader(f) if (r.get("id") or "").strip()}


def write_grading_sheet(questions: list[dict], answers: dict[str, dict]) -> None:
    """eval/answers.md: question, reference and answer side by side, for grading by hand (no judge verdicts)."""
    lines = ["# Agent answers, for grading by hand",
             "", "Grade in `eval/human_labels.csv` (id, correct, supported, notes) **before** opening "
             "`eval/judge.csv`. Generated by `evaluate.py`. Questions, reference answers and agent answers are in "
             "Spanish, the language of the use case.", ""]
    for q in questions:
        a = answers.get(q["id"])
        if not a:
            continue
        lines += [f"## {q['id']} ({q['kind']}): {q['question']}", "",
                  f"**Expected:** {q['expected_source']} {q['expected_location']}".rstrip(), "",
                  f"**Reference answer:** {q['reference_answer']}", "",
                  f"**Retrieved fragments:** {', '.join(a['retrieved_citations']) or '(none)'}", "",
                  "**Answer:**", "", *[f"> {line}" for line in a["answer"].splitlines()], "", "---", ""]
    (EVAL_DIR / "answers.md").write_text("\n".join(lines), encoding="utf-8")


def read_retrieval() -> list[dict]:
    """eval/retrieval.csv with numbers back as numbers, for summarise()."""
    with RETRIEVAL_CSV.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        for key in r:
            if key.startswith(("hit@", "words@")):
                r[key] = int(r[key])
            elif key == "recall@5":
                r[key] = float(r[key])
    return rows


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    logging.basicConfig(level=logging.WARNING, stream=sys.stderr, format="%(name)s: %(message)s")
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    questions = read_questions()

    print("=== Retrieval: hit rate per design ===\n")
    rows = evaluate_retrieval(questions)
    if not rows:
        raise SystemExit("No design could be evaluated: the index is empty.")
    write_csv(RETRIEVAL_CSV, rows)
    summary = summarise(rows)
    write_csv(RETRIEVAL_SUMMARY, summary)
    columns = list(summary[0])
    print("  ".join(f"{c:>16}" if i == 0 else f"{c:>9}" for i, c in enumerate(columns)))
    for line in summary:
        print("  ".join(f"{str(line[c]):>16}" if i == 0 else f"{str(line[c]):>9}" for i, c in enumerate(columns)))
    print(f"\nPer question: {RETRIEVAL_CSV.relative_to(ROOT)}; per design: {RETRIEVAL_SUMMARY.relative_to(ROOT)}")
    print(f"Shipped design (rag.SHIPPED): {rag.SHIPPED}, k={rag.SHIPPED_K}")

    print("\n=== End to end: agent answers ===\n")
    missing = asyncio.run(run_answers(questions))
    answers = read_answers()
    rows = [code_checks(q, answers[q["id"]]) for q in questions if q["id"] in answers]
    write_csv(CHECKS_CSV, rows)
    write_grading_sheet(questions, answers)
    print(f"\n=== End to end: code checks ({len(rows)}/{len(questions)} answered) ===\n")
    for key, value in summarise_checks(rows).items():
        print(f"  {key:<24} {value}")
    print(f"\nPer answer: {CHECKS_CSV.relative_to(ROOT)}; answers and traces: {ANSWERS.relative_to(ROOT)}")
    checks = summarise_checks(rows)

    print("\n=== Judge ===\n")
    verdicts = judge_answers(questions, answers)
    judged = [verdicts[q["id"]] for q in questions if q["id"] in verdicts]
    human = read_csv(HUMAN_LABELS)
    agree = agreement(human, verdicts)
    print(f"\n=== Judge vs your grades ({agree['n']} answers graded by both) ===\n")
    for column in ("correct", "supported"):
        a = agree[column]
        print(f"  {column:<10} agreement {a['agreement']}  kappa {a['kappa']}  "
              f"(1s: you {a['human_1s']}, judge {a['judge_1s']})")
        for line in a["disagree"]:
            print(f"    disagree: {line}")

    by_id = {r["id"]: r for r in rows}
    summary = {
        "agent_model": __import__("agent").MODEL,
        "judge_model": JUDGE_MODEL,
        "shipped_design": rag.SHIPPED, "k": rag.SHIPPED_K,
        "retrieval": next((s for s in summarise(read_retrieval()) if s["design"] == rag.SHIPPED), None),
        "code_checks": checks,
        "judge": {
            "judged": len(judged),
            "correct": sum(v["correct"] == "1" for v in judged),
            "supported": sum(v["supported"] == "1" for v in judged),
            "unsupported": sum(v["supported"] == "0" for v in judged),
            "correct_and_supported": sum(v["correct"] == "1" and v["supported"] == "1" for v in judged),
            "correct_answerable": sum(v["correct"] == "1" for v in judged if v["kind"] != "unanswerable"),
            "correct_refusals": sum(by_id[v["id"]]["outcome"] == "correct_refusal" and v["correct"] == "1"
                                    for v in judged if v["id"] in by_id),
            "wrong_refusals": sum(by_id[v["id"]]["outcome"] == "wrong_refusal" for v in judged if v["id"] in by_id),
        },
        "human": {
            "graded": len(human),
            "correct": sum(h["correct"] == "1" for h in human.values()),
            "supported": sum(h["supported"] == "1" for h in human.values()),
        },
        "agreement": agree,
    }
    SUMMARY_JSON.write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n=== Summary ({SUMMARY_JSON.relative_to(ROOT)}) ===\n")
    for key, value in summary["judge"].items():
        print(f"  {key:<24} {value}")
    print(f"  {'mean_tokens':<24} {checks['mean_tokens']}")
    print(f"  {'median_seconds':<24} {checks['median_seconds']}")

    failures = write_failure_review(questions, answers, rows, verdicts, human)
    print(f"\n=== Failure review ({FAILURES_MD.relative_to(ROOT)}, {FAILURES_CSV.relative_to(ROOT)}) ===\n")
    for r in failures:
        print(f"  {r['id']} {r['kind']:<12} {r['reasons']}")
    if missing:
        raise SystemExit(f"\n{missing} questions still unanswered (quota or network). Run `main.py evaluate` again.")


if __name__ == "__main__":
    main()
