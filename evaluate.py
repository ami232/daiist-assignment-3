"""
Assignment 3: evaluation (`main.py evaluate`).

1. Retrieval: for every answerable question, run each retrieval design and check
   whether a chunk from the expected document and page is in the top 1, 3 and 5
   results (hit rate). -> eval/retrieval_results.csv, eval/retrieval_summary.csv

2. End to end: run the agent on every question. -> eval/answers.csv
   Code checks what code can check: did it refuse, are its citations valid (every
   cited page was retrieved), does it cite an expected page.

3. LLM judge, with a rubric, on the answers that are not refusals: is the answer
   correct against the reference, and is every claim supported by the retrieved
   passages? -> eval/judge_verdicts.csv (kept separate, so the human grading in
   eval/human_labels.csv can be done without seeing the verdicts)

4. Summary: correct, unsupported, correct refusals, wrong refusals, cost per
   question, and agreement with eval/human_labels.csv. -> eval/summary.csv

Each answer and verdict is saved as soon as it exists; re-running skips what is
already done, so a crash or a rate limit loses nothing.
"""

import csv
import json
import re
import sys
import time
from pathlib import Path

from google import genai

from api_key import load_api_key
from index import DOCUMENTS
from retrieval import DESIGNS, search

ROOT = Path(__file__).resolve().parent
EVAL_DIR = ROOT / "eval"
QUESTIONS = EVAL_DIR / "questions.csv"
KS = (1, 3, 5)


def load_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r["question"].strip()]


def expected_passages(row: dict) -> set[tuple[str, int]]:
    """(source, page) pairs that answer the question. Sources and locations are paired in order;
    a single source can be paired with several pages."""
    sources = [s.strip() for s in row["expected_source"].split(";") if s.strip()]
    pages = [int(p.strip().lstrip("p")) for p in row["expected_location"].split(";") if p.strip()]
    if len(sources) == 1:
        sources = sources * len(pages)
    return set(zip(sources, pages))


def evaluate_retrieval(questions: list[dict]) -> list[dict]:
    answerable = [q for q in questions if q["kind"].strip() != "unanswerable"]
    rows = []
    for design in DESIGNS:
        for q in answerable:
            expected = expected_passages(q)
            results = search(q["question"], k=max(KS), design=design)
            found = [(r["source"], r["page"]) for r in results]
            row = {"design": design, "id": q["id"], "kind": q["kind"]}
            for k in KS:
                top = set(found[:k])
                row[f"hit@{k}"] = int(bool(top & expected))  # at least one expected passage found
                row[f"all@{k}"] = int(expected <= top)  # every expected passage found (matters for multi)
            row["first_hit_rank"] = next((i + 1 for i, p in enumerate(found) if p in expected), "")
            row["words_top5"] = sum(len(r["text"].split()) for r in results)
            row["retrieved"] = "; ".join(f"{s} p{p}" for s, p in found)
            rows.append(row)
    return rows


def summarise(rows: list[dict]) -> list[dict]:
    summary = []
    for design in DESIGNS:
        mine = [r for r in rows if r["design"] == design]
        multi = [r for r in mine if r["kind"] == "multi"]
        line = {"design": design, "questions": len(mine)}
        for k in KS:
            line[f"hit@{k}"] = round(sum(r[f"hit@{k}"] for r in mine) / len(mine), 3)
        line["multi_all@5"] = round(sum(r["all@5"] for r in multi) / len(multi), 3) if multi else ""
        line["avg_words_added_top5"] = round(sum(r["words_top5"] for r in mine) / len(mine))
        summary.append(line)
    return summary


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


# ---------- 2. end to end: run the agent ----------

ANSWERS = EVAL_DIR / "answers.csv"
ANSWER_COLUMNS = ["id", "kind", "question", "answer", "refused", "has_citation", "citations_valid",
                  "cites_expected", "guardrail", "cited", "retrieved", "searches", "model_calls",
                  "input_tokens", "output_tokens", "seconds", "draft_answer"]
TITLE_TO_SOURCE = {d["title"]: d["source"] for d in DOCUMENTS}


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def append_row(path: Path, columns: list[str], row: dict) -> None:
    new = not path.exists()
    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        if new:
            writer.writeheader()
        writer.writerow({c: row.get(c, "") for c in columns})


def source_of(title: str) -> str:
    """Map a cited title to its source name (loose match, like the agent's guardrail)."""
    from agent import same_document
    return next((src for t, src in TITLE_TO_SOURCE.items() if same_document(title, t)), title)


def run_agent_on_all(questions: list[dict]) -> None:
    from agent import REFUSAL, answer_question, citations_in

    done = {r["id"] for r in read_csv(ANSWERS)}
    todo = [q for q in questions if q["id"] not in done]
    print(f"\nAgent: {len(done)} questions already answered, {len(todo)} to go.")
    for n, q in enumerate(todo, start=1):
        result = answer_question(q["question"])  # add_document is never approved here
        answer = result["answer"]
        cited = citations_in(answer)
        retrieved = sorted({p for call in result["trace"] if call["tool"] == "search" for p in call["passages"]})
        expected = expected_passages(q) if q["kind"] != "unanswerable" else set()
        row = {
            "id": q["id"], "kind": q["kind"], "question": q["question"], "answer": answer,
            "refused": int(answer.strip().startswith(REFUSAL)),
            "has_citation": int(bool(cited)),
            "citations_valid": int(not result["guardrail"]),
            "cites_expected": int(any((source_of(t), p) in expected for t, p in cited)),
            "guardrail": result["guardrail"],
            "cited": "; ".join(f"{t} p{p}" for t, p in dict.fromkeys(cited)),
            "retrieved": "; ".join(f"{t} p{p}" for t, p in retrieved),
            "searches": sum(1 for call in result["trace"] if call["tool"] == "search"),
            "model_calls": result["model_calls"],
            "input_tokens": result["input_tokens"], "output_tokens": result["output_tokens"],
            "seconds": result["seconds"], "draft_answer": result["draft_answer"],
        }
        append_row(ANSWERS, ANSWER_COLUMNS, row)
        print(f"  [{n}/{len(todo)}] {q['id']} ({q['kind']}): "
              f"{'REFUSED' if row['refused'] else 'answered'} in {row['seconds']}s")
        time.sleep(3)  # stay under the free tier's requests-per-minute limit


# ---------- 3. LLM judge ----------

VERDICTS = EVAL_DIR / "judge_verdicts.csv"
JUDGE_COLUMNS = ["id", "correct", "supported", "reason"]
JUDGE_MODELS = ["gemini-flash-latest", "gemini-flash-lite-latest"]  # a stronger model first, if available

RUBRIC = """You are grading an assistant that answers founders' questions about the EIC Accelerator
using only passages retrieved from official EIC documents.

Question: {question}

Reference answer (written by the test author): {reference}

Passages the assistant retrieved:
{passages}

Assistant's answer:
{answer}

Grade two things:
1. correct (1 or 0): 1 if the answer gives the same key facts as the reference answer (numbers, dates,
   conditions) with nothing that contradicts it. Extra correct detail is fine. Missing the main point,
   a wrong number, or a contradiction is 0. If the reference says the documents do not cover the
   question, the answer is correct only if it says so too.
2. supported (1 or 0): 1 if every factual claim in the answer is stated in the passages above. If any
   claim (a number, date, rule or condition) is not in the passages, it is 0, even if it is true.

Reply only with JSON: {{"correct": 0 or 1, "supported": 0 or 1, "reason": "one short sentence"}}"""


def judge(client, question: dict, answer_row: dict, passages: str) -> dict:
    prompt = RUBRIC.format(question=question["question"], reference=question["reference_answer"],
                           passages=passages or "(none)", answer=answer_row["answer"])
    for attempt in range(8):
        model = JUDGE_MODELS[attempt % len(JUDGE_MODELS)]
        try:
            reply = client.models.generate_content(
                model=model, contents=prompt,
                config={"response_mime_type": "application/json", "temperature": 0},
            )
            data = json.loads(reply.text)
            return {"correct": int(data["correct"]), "supported": int(data["supported"]),
                    "reason": str(data.get("reason", ""))[:300]}
        except (genai.errors.APIError, json.JSONDecodeError, KeyError, ValueError) as error:
            print(f"    judge retry ({model}): {str(error)[:80]}", file=sys.stderr)
            time.sleep(5 * (attempt + 1))
    raise RuntimeError(f"The judge failed on {question['id']}")


def run_judge(questions: list[dict]) -> None:
    from retrieval import get_collection

    by_id = {q["id"]: q for q in questions}
    answers = read_csv(ANSWERS)
    done = {r["id"] for r in read_csv(VERDICTS)}
    todo = [a for a in answers if a["id"] not in done and a["refused"] == "0"]
    print(f"\nJudge: {len(done)} verdicts already, {len(todo)} to go (refusals are graded in code).")
    if not todo:
        return
    collection = get_collection()
    client = genai.Client(api_key=load_api_key())
    for n, a in enumerate(todo, start=1):
        pages = [re.match(r"(.+) p(\d+)$", x.strip()) for x in a["retrieved"].split(";") if x.strip()]
        texts = []
        for m in pages:
            title, page = m.group(1), int(m.group(2))
            got = collection.get(where={"$and": [{"title": title}, {"page": page}]}, include=["documents"])
            texts.append(f"[{title}, p. {page}]\n" + "\n".join(got["documents"]))
        verdict = judge(client, by_id[a["id"]], a, "\n\n".join(texts))
        append_row(VERDICTS, JUDGE_COLUMNS, {"id": a["id"], **verdict})
        print(f"  [{n}/{len(todo)}] {a['id']}: correct={verdict['correct']} supported={verdict['supported']}")
        time.sleep(3)


# ---------- 4. summary ----------

def final_grades(answers: list[dict], verdicts: dict) -> list[dict]:
    """One grade per question: refusals are graded in code, everything else by the judge."""
    grades = []
    for a in answers:
        refused, unanswerable = a["refused"] == "1", a["kind"] == "unanswerable"
        if refused:
            correct, supported = int(unanswerable), 1  # a refusal makes no claims
        else:
            v = verdicts.get(a["id"], {})
            correct = 0 if unanswerable else int(v.get("correct", 0))
            supported = int(v.get("supported", 0))
        grades.append({"id": a["id"], "kind": a["kind"], "refused": int(refused), "correct": correct,
                       "supported": supported})
    return grades


def summarise_end_to_end(questions: list[dict]) -> None:
    answers = read_csv(ANSWERS)
    if not answers:
        return
    verdicts = {v["id"]: v for v in read_csv(VERDICTS)}
    grades = final_grades(answers, verdicts)
    answerable = [g for g in grades if g["kind"] != "unanswerable"]
    unanswerable = [g for g in grades if g["kind"] == "unanswerable"]
    n = len(answers)
    summary = {
        "questions": n,
        "correct (all kinds)": sum(g["correct"] for g in grades),
        "correct answers (answerable)": sum(g["correct"] for g in answerable),
        "answerable questions": len(answerable),
        "unsupported answers (claim not in passages)": sum(1 for g in grades if not g["refused"] and not g["supported"]),
        "correct refusals (unanswerable)": sum(g["refused"] for g in unanswerable),
        "unanswerable questions": len(unanswerable),
        "wrong refusals (answerable)": sum(g["refused"] for g in answerable),
        "guardrail fired": sum(1 for a in answers if a["guardrail"]),
        "answers citing an expected page": sum(int(a["cites_expected"]) for a in answers if a["kind"] != "unanswerable"),
        "avg searches per question": round(sum(int(a["searches"]) for a in answers) / n, 2),
        "avg input tokens per question": round(sum(int(a["input_tokens"] or 0) for a in answers) / n),
        "avg output tokens per question": round(sum(int(a["output_tokens"] or 0) for a in answers) / n),
        "avg seconds per question": round(sum(float(a["seconds"]) for a in answers) / n, 1),
    }
    human = [h for h in read_csv(EVAL_DIR / "human_labels.csv") if h.get("correct", "").strip() in ("0", "1")]
    by_id = {g["id"]: g for g in grades}
    both = [h for h in human if h["id"] in by_id]
    if both:
        summary["human-graded answers"] = len(both)
        summary["agreement with human: correct"] = round(sum(int(h["correct"]) == by_id[h["id"]]["correct"] for h in both) / len(both), 2)
        summary["agreement with human: supported"] = round(
            sum(int(h["supported"]) == by_id[h["id"]]["supported"] for h in both if h.get("supported", "").strip() in ("0", "1"))
            / max(1, sum(1 for h in both if h.get("supported", "").strip() in ("0", "1"))), 2)
    write_csv(EVAL_DIR / "grades.csv", grades)
    write_csv(EVAL_DIR / "summary.csv", [{"metric": k, "value": v} for k, v in summary.items()])
    print("\nEnd-to-end summary:")
    for k, v in summary.items():
        print(f"  {k}: {v}")


def main() -> None:
    questions = load_questions()
    rows = evaluate_retrieval(questions)
    summary = summarise(rows)
    write_csv(EVAL_DIR / "retrieval_results.csv", rows)
    write_csv(EVAL_DIR / "retrieval_summary.csv", summary)
    print("Retrieval hit rate (answerable questions):")
    for line in summary:
        print(f"  {line['design']:>7}: " + "  ".join(f"hit@{k}={line[f'hit@{k}']:.2f}" for k in KS)
              + f"  multi all@5={line['multi_all@5']}  ~{line['avg_words_added_top5']} words in top 5")
    run_agent_on_all(questions)
    run_judge(questions)
    summarise_end_to_end(questions)


if __name__ == "__main__":
    main()
