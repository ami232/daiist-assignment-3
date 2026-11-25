"""
Assignment 3: evaluation (`main.py evaluate`).

1. Retrieval: hit rate at k = 1, 3, 5 for each chunking design (article, fixed) on the answerable
   questions. A hit means the top-k contains the expected passage(s): same source and, for the
   article design, the same location; for the fixed design, a chunk whose pages overlap the pages
   of the expected article (the article design tells us where each article is). For `multi`
   questions ALL expected passages must be in the top-k.
2. Agent: runs agent.py on every question (approval is denied: evaluation never adds documents).
3. Code checks: citations exist in the retrieved text, refusal behaviour, cited the expected source.
4. LLM judge: rubric + the retrieved text as evidence -> correct / supported.
5. Agreement with eval/human_labels.csv (your own grades).

Everything is saved in eval/. Answers are saved one by one and reused on a re-run (quota!);
`--redo` re-runs them. Extra mode for the report:
    uv run python evaluate.py --before-after q27 path/to/new_document.pdf
"""

import argparse
import csv
import json
import os
import sys
from pathlib import Path

import numpy as np

import index as ix
import retrieval

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
ANSWERS = EVAL / "answers.jsonl"
JUDGEMENTS = EVAL / "judgements.jsonl"
QUERY_VECTORS = EVAL / "query_vectors.json"
KS = (1, 3, 5)

RUBRIC = """You grade an answer from a legal question-answering assistant. You get the question, the
reference answer, the passages the assistant retrieved (the ONLY allowed evidence) and the assistant's answer.

correct (0 or 1):
  - answerable question: 1 only if the answer agrees with the reference answer on every fact that matters
    (numbers, durations, who must do what). Missing the key fact, or a wrong one, is 0.
  - unanswerable question: 1 only if the assistant says the documents do not cover it and gives no invented
    answer. Any confident answer is 0.
supported (0 or 1): 1 only if EVERY factual claim in the answer appears in the retrieved passages.
  A refusal with no claims is supported (1). Claims from general knowledge not in the passages: 0.
Reply with a short reason."""


# ------------------------------------------------------------------ files

def read_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if (r.get("question") or "").strip()]


def split(value: str) -> list[str]:
    return [v.strip() for v in (value or "").split(";") if v.strip()]


def query_vectors(questions: list[dict]) -> dict[str, list[float]]:
    """Embed each question once and keep the vectors (a re-run costs no quota)."""
    cache = json.loads(QUERY_VECTORS.read_text()) if QUERY_VECTORS.exists() else {}
    for q in questions:
        if q["question"] not in cache:
            cache[q["question"]] = [float(x) for x in retrieval.embed_query(q["question"])]
            QUERY_VECTORS.write_text(json.dumps(cache))
    return cache


# ------------------------------------------------------------------ 1. retrieval

def gold_pages(article_chunks: list[dict]) -> dict[tuple[str, str], set[int]]:
    """(source, location) -> pages, taken from the article design's metadata."""
    pages: dict[tuple[str, str], set[int]] = {}
    for c in article_chunks:
        first, _, last = c["pages"].partition("-")
        pages.setdefault((c["source"], c["location"]), set()).update(range(int(first), int(last or first) + 1))
    return pages


def is_hit(results: list[dict], source: str, location: str, gold: dict) -> bool:
    for r in results:
        if r["source"] != source:
            continue
        if r["design"] == "article" and r["location"] == location:
            return True
        if r["design"] == "fixed":
            first, _, last = r["pages"].partition("-")
            if set(range(int(first), int(last or first) + 1)) & gold.get((source, location), set()):
                return True
    return False


def evaluate_retrieval(questions: list[dict], vectors: dict) -> dict:
    answerable = [q for q in questions if q["kind"].strip().lower() != "unanswerable"]
    article = retrieval.Retriever("article", embedder=None)
    gold = gold_pages(article.chunks)
    report = {}
    for design in ix.DESIGNS:
        retriever = article if design == "article" else retrieval.Retriever(design, embedder=None)
        hits = {k: 0 for k in KS}
        words_in_prompt = {k: 0 for k in KS}
        for q in answerable:
            sources, locations = split(q["expected_source"]), split(q["expected_location"])
            expected = list(zip(sources, locations)) if len(sources) == len(locations) else [(sources[0], locations[0])]
            top = retriever.search_vector(np.array(vectors[q["question"]], dtype=np.float32), k=max(KS))
            for k in KS:
                results = top[:k]
                words_in_prompt[k] += sum(ix.words(r["text"]) for r in results)
                hits[k] += all(is_hit(results, s, l, gold) for s, l in expected)
        n = len(answerable)
        report[design] = {"chunks": len(retriever.chunks), "questions": n,
                          **{f"hit@{k}": round(hits[k] / n, 3) for k in KS},
                          **{f"words@{k}": round(words_in_prompt[k] / n) for k in KS}}
    return report


# ------------------------------------------------------------------ 2. agent answers + 3. code checks

def load_answers() -> dict[str, dict]:
    if not ANSWERS.exists():
        return {}
    with ANSWERS.open(encoding="utf-8") as f:
        return {r["id"]: r for r in map(json.loads, filter(str.strip, f))}


def run_agent_on(questions: list[dict], redo: bool) -> dict[str, dict]:
    import agent

    answers = {} if redo else load_answers()
    for q in questions:
        if q["id"] in answers:
            continue
        try:
            out = agent.ask(q["question"], approve=lambda path: False)
        except Exception as error:  # noqa: BLE001 - quota or network: keep what we have
            print(f"stopped at {q['id']}: {error}", file=sys.stderr)
            break
        row = {"id": q["id"], **out}
        answers[q["id"]] = row
        with ANSWERS.open("a", encoding="utf-8") as f:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
        print(f"  {q['id']} answered ({out['seconds']}s, {out['tool_calls']} tool calls)", file=sys.stderr)
    return answers


def code_checks(q: dict, a: dict) -> dict:
    """What code can check: valid citations, refusal behaviour, expected source cited."""
    import agent

    check = agent.check_citations(a["answer"], a["trace"])
    unanswerable = q["kind"].strip().lower() == "unanswerable"
    cited_sources = {s for s, _ in check["cited"]}
    expected = set(split(q["expected_source"]))
    return {"citations_valid": not check["invalid"], "invalid_citations": len(check["invalid"]),
            "refused": check["refusal"] and not check["cited"] or a.get("guardrail") == "replaced_by_refusal",
            "should_refuse": unanswerable,
            "refusal_ok": (check["refusal"] or a.get("guardrail") == "replaced_by_refusal") if unanswerable else None,
            "wrong_refusal": (not unanswerable) and (check["refusal"] and not check["cited"]),
            "cited_expected_source": bool(expected & cited_sources) if expected else None}


# ------------------------------------------------------------------ 4. judge

def judge(q: dict, a: dict) -> dict:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from pydantic import BaseModel, Field

    from api_key import load_api_key
    import agent

    class Verdict(BaseModel):
        correct: int = Field(description="0 or 1")
        supported: int = Field(description="0 or 1")
        reason: str

    evidence = "\n\n".join(c["result"] for c in a["trace"] if c["tool"] == "search") or "(nothing retrieved)"
    model = ChatGoogleGenerativeAI(model=os.environ.get("JUDGE_MODEL", agent.MODEL),
                                   google_api_key=load_api_key(), temperature=0)
    prompt = (f"{RUBRIC}\n\nQUESTION ({q['kind']}): {q['question']}\nREFERENCE ANSWER: {q['reference_answer']}\n\n"
              f"RETRIEVED PASSAGES:\n{evidence}\n\nASSISTANT ANSWER:\n{a['answer']}")
    verdict = model.with_structured_output(Verdict).invoke(prompt)
    return {"judge_correct": int(verdict.correct), "judge_supported": int(verdict.supported),
            "judge_reason": verdict.reason}


# ------------------------------------------------------------------ 5. agreement

def agreement(rows: list[dict]) -> dict:
    path = EVAL / "human_labels.csv"
    if not path.exists():
        return {}
    with path.open(newline="", encoding="utf-8") as f:
        human = {r["id"]: r for r in csv.DictReader(f) if (r.get("id") or "").strip() and r.get("correct", "") != ""}
    by_id = {r["id"]: r for r in rows}
    shared = [i for i in human if i in by_id and "judge_correct" in by_id[i]]
    out = {"graded_by_you": len(human), "compared": len(shared)}
    for field in ("correct", "supported"):
        pairs = [(int(human[i][field]), by_id[i][f"judge_{field}"]) for i in shared if human[i].get(field, "") != ""]
        if pairs:
            agree = sum(h == j for h, j in pairs) / len(pairs)
            p_h, p_j = np.mean([h for h, _ in pairs]), np.mean([j for _, j in pairs])
            chance = p_h * p_j + (1 - p_h) * (1 - p_j)
            out[f"{field}_agreement"] = round(agree, 3)
            out[f"{field}_kappa"] = round((agree - chance) / (1 - chance), 3) if chance < 1 else None
    return out


# ------------------------------------------------------------------ main

def main(redo: bool = False) -> None:
    questions = read_questions()
    vectors = query_vectors(questions)

    retrieval_report = evaluate_retrieval(questions, vectors)
    print("Retrieval:", json.dumps(retrieval_report, indent=2), file=sys.stderr)

    answers = run_agent_on(questions, redo)
    judged = {} if redo or not JUDGEMENTS.exists() else {
        r["id"]: r for r in map(json.loads, filter(str.strip, JUDGEMENTS.open(encoding="utf-8")))}
    rows = []
    for q in questions:
        a = answers.get(q["id"])
        if not a:
            continue
        if q["id"] not in judged:
            try:
                verdict = judge(q, a)
            except Exception as error:  # noqa: BLE001 - quota: keep verdicts so far, resume later
                print(f"judge stopped at {q['id']}: {str(error)[:200]}", file=sys.stderr)
                break
            judged[q["id"]] = {"id": q["id"], **verdict}
            with JUDGEMENTS.open("a", encoding="utf-8") as f:
                f.write(json.dumps(judged[q["id"]], ensure_ascii=False) + "\n")
        row = {"id": q["id"], "kind": q["kind"], "question": q["question"], "answer": a["answer"],
               "tool_calls": a["tool_calls"], "seconds": a["seconds"], "guardrail": a.get("guardrail"),
               **a["tokens"], **code_checks(q, a)}
        row.update({k: v for k, v in judged[q["id"]].items() if k != "id"})
        rows.append(row)
    if len(rows) < len(questions):
        print(f"\nNOT FINISHED: {len(rows)} of {len(questions)} questions answered and judged. "
              "Run the same command again later (or with another GEMINI_MODEL / JUDGE_MODEL); "
              "it resumes where it stopped.", file=sys.stderr)

    EVAL.mkdir(exist_ok=True)
    if rows:
        with (EVAL / "results.csv").open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(rows[0]))
            writer.writeheader()
            writer.writerows(rows)

    answerable = [r for r in rows if r["kind"] != "unanswerable"]
    unanswerable = [r for r in rows if r["kind"] == "unanswerable"]
    summary = {
        "retrieval": retrieval_report,
        "questions_answered": len(rows),
        "correct_answers": sum(r["judge_correct"] for r in answerable),
        "answerable": len(answerable),
        "correct_refusals": sum(r["judge_correct"] for r in unanswerable),
        "unanswerable": len(unanswerable),
        "wrong_refusals": sum(bool(r["wrong_refusal"]) for r in answerable),
        "unsupported_answers": sum(1 - r["judge_supported"] for r in rows),
        "invalid_citation_answers": sum(1 - r["citations_valid"] for r in rows),
        "guardrail_fired": sum(bool(r["guardrail"]) for r in rows),
        "avg_seconds": round(float(np.mean([r["seconds"] for r in rows])), 1) if rows else None,
        "avg_input_tokens": round(float(np.mean([r["input_tokens"] for r in rows]))) if rows else None,
        "avg_output_tokens": round(float(np.mean([r["output_tokens"] for r in rows]))) if rows else None,
        "agreement_with_judge": agreement(rows),
    }
    (EVAL / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(summary, indent=2, ensure_ascii=False))


def before_after(question_id: str, path: str) -> None:
    """Answer an unanswerable question, add a document that covers it (approved), answer again."""
    import agent

    q = next(r for r in read_questions() if r["id"] == question_id)
    before = agent.ask(q["question"], approve=lambda p: False)
    added = agent.ask(f"Add this document to the corpus: {path}", approve=lambda p: True)
    after = agent.ask(q["question"], approve=lambda p: False)
    result = {"question": q, "before": before["answer"], "added": added["trace"], "after": after["answer"],
              "after_citations": after["citations"]["cited"]}
    (EVAL / "before_after.json").write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps(result, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--redo", action="store_true", help="re-run the agent on every question")
    parser.add_argument("--before-after", nargs=2, metavar=("QUESTION_ID", "DOCUMENT"))
    args = parser.parse_args()
    if args.before_after:
        before_after(*args.before_after)
    else:
        main(redo=args.redo)
