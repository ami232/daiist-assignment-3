"""
Assignment 3: evaluation (`uv run python main.py evaluate`).

1. Retrieval: hit rate at k = 1, 3, 5 for each chunking design.
2. End to end: the agent answers every question in eval/questions.csv.
3. Code checks: valid citations, refusal when (and only when) it should refuse.
4. LLM judge with a rubric, using the retrieved text as evidence.
5. Agreement between the judge and my own grades (eval/human_labels.csv).
6. add_document demo: an unanswerable question before and after adding a document.

Everything that costs API calls is cached in eval/ (answers.jsonl, judge.jsonl,
add_document_demo.json), so running this again is fast and free.
Delete a cache file to recompute it.
"""

import csv
import json
import os
import shutil
import sys
import tempfile
import time
from pathlib import Path

from pydantic import BaseModel, Field

import index
from api_key import load_api_key
from agent import MODEL, apply_citation_guardrail, ask, is_refusal, parse_citations
from server import retrieve

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
KS = [1, 3, 5]
JUDGE_MODEL = "gemini-3.1-flash-lite"   # a different model from the agent, so it does not grade itself
DEMO_QUESTION_ID = "q31"   # "airline lost my suitcase" -> answered by Regulation 889/2002
DEMO_FILE = index.EXTRA_DIR / "air-liability-889-2002.html"


def read_csv(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def expected_passages(q: dict) -> list[tuple[str, str]]:
    """'air-261-2004' + 'Article 4;Article 7' -> [(air-261-2004, Article 4), (air-261-2004, Article 7)]."""
    locations = q["expected_location"].split(";")
    sources = q["expected_source"].split(";")
    if len(sources) == 1:
        sources = sources * len(locations)
    return list(zip(sources, locations))


def chunk_matches(chunk: dict, passage: tuple[str, str]) -> bool:
    """A chunk contains a passage if it has the same source and touches that location."""
    return chunk["source"] == passage[0] and passage[1] in chunk["locations"].split(" | ")


def pct(x: float) -> str:
    return f"{100 * x:.0f}%"


# ---------------------------------------------------------------- 1. retrieval

def evaluate_retrieval(questions: list[dict]) -> tuple[list[dict], list[dict]]:
    """Hit@k = share of questions with at least one expected passage in the top k.
    For multi questions we also report 'both@5': all expected passages in the top 5.
    Returns (one row per design, one row per question with the rank of the first hit)."""
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    rows, per_question = [], {q["id"]: {"id": q["id"], "kind": q["kind"]} for q in answerable}
    for design in index.DESIGNS:
        hits = {k: 0 for k in KS}
        both, n_multi, words = 0, 0, 0
        for q in answerable:
            top = retrieve(q["question"], design, k=max(KS))
            passages = expected_passages(q)
            ranks = [i for i, c in enumerate(top, start=1) if any(chunk_matches(c, p) for p in passages)]
            per_question[q["id"]][f"first_hit_rank_{design}"] = ranks[0] if ranks else "miss"
            for k in KS:
                if any(chunk_matches(c, p) for c in top[:k] for p in passages):
                    hits[k] += 1
            if q["kind"] == "multi":
                n_multi += 1
                both += all(any(chunk_matches(c, p) for c in top) for p in passages)
            words += sum(len(c["text"].split()) for c in top)
        rows.append({
            "design": design,
            **{f"hit@{k}": round(hits[k] / len(answerable), 3) for k in KS},
            "multi_both@5": round(both / n_multi, 3),
            "words_in_prompt_top5": round(words / len(answerable)),
        })
    return rows, list(per_question.values())


# ---------------------------------------------------------------- 2. answers (cached)

def load_jsonl(path: Path) -> dict:
    if not path.exists():
        return {}
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return {r["key"]: r for r in rows}


def append_jsonl(path: Path, row: dict) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def get_answers(questions: list[dict]) -> dict:
    cache_path = EVAL / "answers.jsonl"
    cache = load_jsonl(cache_path)
    answers = {}
    for q in questions:
        key = f"{q['id']}|{q['question']}"
        if key not in cache:
            print(f"  asking {q['id']} ...", flush=True)
            out = ask(q["question"], approve=lambda path: False)   # never add documents during evaluation
            cache[key] = {"key": key, "id": q["id"], **out}
            append_jsonl(cache_path, cache[key])
        a = dict(cache[key])
        # re-apply the current citation guardrail to the cached draft (pure code, no API call)
        a["answer"], a["guardrail_fired"], check = apply_citation_guardrail(a["draft"], [a["retrieved"]])
        a["citations"], a["invalid_citations"] = check["cited"], check["invalid"]
        answers[q["id"]] = a
    return answers


# ---------------------------------------------------------------- 4. judge (cached)

RUBRIC = """You grade the answer of an assistant about EU passenger rights.

You get: the question, a reference answer written by a human, the passages the
assistant retrieved (its only evidence), and the assistant's answer.

correct (1 or 0):
- 1 if the answer gives the same key facts as the reference: the amount, percentage,
  deadline or yes/no, and the main condition. Extra details are fine if they are not wrong.
- If the reference says the corpus does not cover the question, 1 only if the assistant
  declines to answer (says the corpus does not cover it). Any attempted answer is 0.
- If the assistant declines but the reference gives an answer, 0.
- 0 if any key fact contradicts the reference or is missing.

supported (1 or 0):
- 1 if every factual claim in the answer (amounts, deadlines, conditions) is stated in
  the retrieved passages. A refusal counts as supported.
- 0 if any claim is not in the passages, even if it is true in reality.

Give a one-sentence reason."""


class Verdict(BaseModel):
    correct: int = Field(description="1 or 0")
    supported: int = Field(description="1 or 0")
    reason: str = Field(description="one sentence")


def judge_answers(questions: list[dict], answers: dict) -> dict:
    from langchain_google_genai import ChatGoogleGenerativeAI
    cache_path = EVAL / "judge.jsonl"
    cache = load_jsonl(cache_path)
    judge = None
    verdicts = {}
    for q in questions:
        a = answers[q["id"]]
        key = f"{q['id']}|{a['answer']}"
        if key not in cache:
            if judge is None:
                judge = ChatGoogleGenerativeAI(model=JUDGE_MODEL, temperature=0, max_retries=6).with_structured_output(Verdict)
            print(f"  judging {q['id']} ...", flush=True)
            prompt = (f"{RUBRIC}\n\nQUESTION:\n{q['question']}\n\nREFERENCE ANSWER:\n{q['reference_answer']}"
                      f"\n\nRETRIEVED PASSAGES:\n{a['retrieved'] or '(none)'}\n\nASSISTANT ANSWER:\n{a['answer']}")
            v = judge.invoke(prompt)
            time.sleep(5)   # free tier: at most 15 requests per minute
            cache[key] = {"key": key, "id": q["id"], "correct": int(v.correct), "supported": int(v.supported),
                          "reason": v.reason}
            append_jsonl(cache_path, cache[key])
        verdicts[q["id"]] = cache[key]
    return verdicts


# ---------------------------------------------------------------- 3 + 5. checks and outcomes

def outcome(q: dict, refused: bool, verdict: dict) -> str:
    if q["kind"] == "unanswerable":
        return "correct refusal" if refused else "answered unanswerable"
    if refused:
        return "wrong refusal"
    if verdict["correct"] and verdict["supported"]:
        return "correct"
    return "wrong or unsupported"


def likely_cause(q: dict, a: dict, result: str) -> str:
    """First guess at the failure cause, from the trace. I review every one by hand in REPORT.md."""
    if result in ("correct", "correct refusal"):
        return ""
    if result == "answered unanswerable":
        return "unsupported claim"
    found = any(p in parse_citations(a["retrieved"]) for p in expected_passages(q))
    if not found:
        return "retrieval miss"
    if result == "wrong refusal":
        return "wrong refusal"
    return "wrong answer from right passage"


def agreement(verdicts: dict) -> dict | None:
    path = EVAL / "human_labels.csv"
    labels = [r for r in read_csv(path) if r.get("id", "").strip()] if path.exists() else []
    if not labels:
        return None
    same_correct = sum(int(r["correct"]) == verdicts[r["id"]]["correct"] for r in labels)
    same_supported = sum(int(r["supported"]) == verdicts[r["id"]]["supported"] for r in labels)
    disagreements = [r["id"] for r in labels
                     if int(r["correct"]) != verdicts[r["id"]]["correct"]
                     or int(r["supported"]) != verdicts[r["id"]]["supported"]]
    return {"n": len(labels), "correct": same_correct / len(labels),
            "supported": same_supported / len(labels), "disagreements": disagreements}


# ---------------------------------------------------------------- 6. add_document demo (cached)

def add_document_demo(questions: list[dict], answers: dict) -> dict:
    path = EVAL / "add_document_demo.json"
    if path.exists():
        return json.loads(path.read_text(encoding="utf-8"))
    import server
    question = next(q["question"] for q in questions if q["id"] == DEMO_QUESTION_ID)
    tmp = Path(tempfile.mkdtemp())
    shutil.copytree(index.INDEX_DIR, tmp / "index")      # work on a copy: the committed index stays as it is
    index.INDEX_DIR = tmp / "index"
    os.environ["CORPUS_INDEX_DIR"] = str(tmp / "index")   # the server started by ask() uses the copy too
    try:
        first = server.add_document(str(DEMO_FILE))
        second = server.add_document(str(DEMO_FILE))       # what happens if it is already indexed
        after = ask(question, approve=lambda p: False)
    finally:
        os.environ.pop("CORPUS_INDEX_DIR")
        index.INDEX_DIR = ROOT / "index"
        shutil.rmtree(tmp, ignore_errors=True)
    demo = {"question": question, "before": answers[DEMO_QUESTION_ID]["answer"],
            "add_document_first_call": first, "add_document_second_call": second,
            "after": after["answer"], "after_citations": after["citations"]}
    path.write_text(json.dumps(demo, indent=2, ensure_ascii=False), encoding="utf-8")
    return demo


# ---------------------------------------------------------------- main

def main() -> None:
    sys.stdout.reconfigure(encoding="utf-8")
    load_api_key()
    questions = read_csv(EVAL / "questions.csv")

    print("1. Retrieval")
    retrieval, retrieval_per_question = evaluate_retrieval(questions)
    write_csv(EVAL / "retrieval.csv", retrieval)
    write_csv(EVAL / "retrieval_per_question.csv", retrieval_per_question)
    for r in retrieval:
        print("  ", r)

    print("2. Agent answers")
    answers = get_answers(questions)

    print("3. LLM judge")
    verdicts = judge_answers(questions, answers)

    results = []
    for q in questions:
        a, v = answers[q["id"]], verdicts[q["id"]]
        refused = is_refusal(a["answer"])
        result = outcome(q, refused, v)
        results.append({
            "id": q["id"], "kind": q["kind"], "question": q["question"],
            "answer": a["answer"],
            "searches": sum(t["tool"] == "search" for t in a["trace"]),
            "citations_valid": int(not a["invalid_citations"] and (refused or bool(a["citations"]))),
            "refusal_ok": int(refused == (q["kind"] == "unanswerable")),
            "guardrail_fired": int(a["guardrail_fired"]),
            "judge_correct": v["correct"], "judge_supported": v["supported"], "judge_reason": v["reason"],
            "outcome": result,
            "likely_cause": likely_cause(q, a, result),
            "tokens": a["tokens"], "seconds": a["seconds"],
        })
    write_csv(EVAL / "results.csv", results)

    # grading sheet for my own labels: answers and evidence, but no judge verdicts
    write_csv(EVAL / "grading_sheet.csv", [
        {"id": q["id"], "question": q["question"], "reference_answer": q["reference_answer"],
         "answer": answers[q["id"]]["answer"], "retrieved": answers[q["id"]]["retrieved"]}
        for q in questions])

    print("4. add_document demo")
    demo = add_document_demo(questions, answers)

    agree = agreement(verdicts)
    n = len(results)
    count = lambda name: sum(r["outcome"] == name for r in results)
    lines = [
        "# Evaluation summary", "",
        f"Agent model: {MODEL}. Judge model: {JUDGE_MODEL}. Questions: {n}.", "",
        "## Retrieval (answerable questions)", "",
        "| design | hit@1 | hit@3 | hit@5 | multi: both passages in top 5 | words added to prompt (top 5) |",
        "|---|---|---|---|---|---|",
        *[f"| {r['design']} | {pct(r['hit@1'])} | {pct(r['hit@3'])} | {pct(r['hit@5'])} | "
          f"{pct(r['multi_both@5'])} | {r['words_in_prompt_top5']} |" for r in retrieval],
        "", "## End to end", "",
        "| outcome | count |", "|---|---|",
        *[f"| {name} | {count(name)} |" for name in
          ["correct", "wrong or unsupported", "wrong refusal", "correct refusal", "answered unanswerable"]],
        "",
        f"- Code check, citations valid: {sum(r['citations_valid'] for r in results)}/{n}",
        f"- Code check, refusal when (and only when) expected: {sum(r['refusal_ok'] for r in results)}/{n}",
        f"- Citation guardrail fired: {sum(r['guardrail_fired'] for r in results)} times",
        f"- Judge: correct {sum(r['judge_correct'] for r in results)}/{n}, "
        f"supported {sum(r['judge_supported'] for r in results)}/{n}",
        f"- Cost per question: {sum(r['tokens'] for r in results) / n:.0f} tokens, "
        f"{sum(r['seconds'] for r in results) / n:.1f} s on average",
        "", "## Judge vs. my own grades", "",
    ]
    if agree is None or agree["n"] < 20:
        lines.append(f"Pending: eval/human_labels.csv has {0 if agree is None else agree['n']} grades (20 needed). "
                     "Grade the answers in eval/grading_sheet.csv first.")
    if agree:
        lines.append(f"On {agree['n']} answers: same 'correct' grade {pct(agree['correct'])}, "
                     f"same 'supported' grade {pct(agree['supported'])}. Disagreements: "
                     f"{', '.join(agree['disagreements']) or 'none'}.")
    lines += ["", "## Failures (first guess, checked by hand in REPORT.md)", "",
              "| id | outcome | likely cause |", "|---|---|---|",
              *[f"| {r['id']} | {r['outcome']} | {r['likely_cause']} |" for r in results if r["likely_cause"]],
              "", "## add_document demo", "",
              f"Question: {demo['question']}", "", f"Before: {demo['before']}", "",
              f"add_document: {demo['add_document_first_call']}", "",
              f"Again (already indexed): {demo['add_document_second_call']}", "",
              f"After: {demo['after']}", ""]
    (EVAL / "summary.md").write_text("\n".join(lines), encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
