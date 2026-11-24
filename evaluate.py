"""
Evaluation (`uv run python main.py evaluate`).

    1. Retrieval: hit rate at k = 1, 3, 5 for both chunking designs.
    2. End to end: run the agent on every question in eval/questions.csv.
    3. Code checks: are the citations real? did it refuse when it should (and only then)?
    4. LLM judge (Gemini Flash) with a rubric, using the retrieved text as evidence.
    5. Agreement between the judge and my own grades (eval/human_labels.csv).
    6. Demo: an unanswerable question, before and after adding the held-out ficha.

Results go to eval/: retrieval.csv, answers.csv, verdicts.csv, add_document_demo.json, summary.json.
Agent answers and judge verdicts are cached in answers.csv / verdicts.csv, so running this again
only processes new questions (delete those files to start from scratch).
"""

import csv
import json
import re
import time
from pathlib import Path

from google.genai import types

import index
from agent import MODEL, NO_CONSTA, answer

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
HUMAN_LABELS = EVAL / "human_labels.csv"
HELD_OUT = ROOT / "data" / "extra" / "matrimonio-civil.json"
DEMO_QUESTION = "¿Qué tengo que hacer para casarme por lo civil en el Ayuntamiento de Guía?"
KS = [1, 3, 5]


def read_csv(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def split(value: str) -> list[str]:
    return [v.strip() for v in (value or "").split(";") if v.strip()]


def is_refusal(text: str) -> bool:
    return NO_CONSTA.lower() in text.lower() or "solo puedo ayudar" in text.lower()


# ---------------------------------------------------------------- 1. retrieval

def is_hit(hit: dict, sources: list[str], locations: list[str]) -> bool:
    """A retrieved chunk is a hit if it comes from an expected ficha and covers an expected section."""
    if hit["source"] not in sources:
        return False
    if not locations:
        return True
    return any(loc in hit["sections"].split(",") for loc in locations)


def evaluate_retrieval(questions: list[dict]) -> dict:
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    # Embed each question once and reuse the vector for both designs (saves quota).
    vectors = {q["id"]: index.embed_query(q["question"]) for q in answerable}
    rows, summary = [], {}
    for design in index.DESIGNS:
        hits_at = {k: 0 for k in KS}
        words = []
        for q in answerable:
            results = index.search(q["question"], k=max(KS), design=design, query_vector=vectors[q["id"]])
            words.append(sum(len(r["text"].split()) for r in results))
            sources, locations = split(q["expected_source"]), split(q["expected_location"])
            first_hit = next((i + 1 for i, r in enumerate(results) if is_hit(r, sources, locations)), None)
            for k in KS:
                hits_at[k] += first_hit is not None and first_hit <= k
            rows.append({"design": design, "id": q["id"], "first_hit_rank": first_hit or "",
                         "top1": f"{results[0]['source']} · {results[0]['location']}"})
        n = len(answerable)
        summary[design] = {f"hit@{k}": round(hits_at[k] / n, 3) for k in KS}
        summary[design]["avg_words_added_k5"] = round(sum(words) / n)
    write_csv(EVAL / "retrieval.csv", rows)
    best = max(index.DESIGNS, key=lambda d: (summary[d]["hit@3"], summary[d]["hit@5"]))
    summary["best_design_by_hit@3"] = best
    summary["design_used_by_server"] = index.CHOSEN_DESIGN
    return summary


# ---------------------------------------------------------------- 2-3. agent + code checks

def citations_valid(text: str) -> bool:
    """Every [slug · location] in the answer must point to a chunk that exists in the index.

    The location can be the exact one of a chunk ("palabras 0-200") or section names
    of that ficha ("plazo_resolucion"), in case the model cites the section instead.
    """
    collection = index.get_collection(index.CHOSEN_DESIGN)
    for slug, location in re.findall(r"\[([\w-]+)\s*·\s*([^\]]+)\]", text):
        found = collection.get(where={"source": slug})
        if not found["ids"]:
            return False
        locations = {m["location"] for m in found["metadatas"]}
        sections = {s for m in found["metadatas"] for s in m["sections"].split(",")}
        location = location.strip()
        if location not in locations and not set(re.split(r"\s*[+,]\s*", location)) <= sections:
            return False
    return True


def run_agent(questions: list[dict]) -> list[dict]:
    cached = {row["id"]: row for row in read_csv(EVAL / "answers.csv")}
    rows = []
    for q in questions:
        if q["id"] in cached and cached[q["id"]]["question"] == q["question"]:
            rows.append(cached[q["id"]])
            continue
        print(f"  agent: {q['id']} {q['question'][:60]}")
        out = answer(q["question"])
        searched = [s["args"].get("query", "") for s in out["trace"] if s["tool"] == "search"]
        rows.append({
            "id": q["id"], "kind": q["kind"], "question": q["question"], "answer": out["answer"],
            "has_citation": int(bool(re.search(r"\[[\w-]+\s*·", out["answer"]))),
            "citations_valid": int(citations_valid(out["answer"])),
            "refused": int(is_refusal(out["answer"])),
            "guardrail_fired": int(out["guardrail_fired"]),
            "original_answer": out["original_answer"] if out["guardrail_fired"] else "",
            "retrieved_sources": ";".join(sorted(set(re.findall(r"^\[([\w-]+) ·", out["retrieved"], re.M)))),
            "searches": " | ".join(searched),
            "tokens": out["tokens"], "seconds": out["seconds"],
            "retrieved": out["retrieved"],  # full text: the judge must see everything the agent saw
        })
        write_csv(EVAL / "answers.csv", rows + [r for i, r in cached.items() if i not in {x["id"] for x in rows}])
    write_csv(EVAL / "answers.csv", rows)
    return rows


# ---------------------------------------------------------------- 4. judge

RUBRIC = """You grade answers of a Spanish municipal-procedures assistant (Ayuntamiento de Guía).
You get the question, the reference answer written by a human, the assistant's answer and the
passages the assistant retrieved. Grade two things, each 1 or 0:

correct:
  1 = the answer gives the same key facts as the reference (deadlines, documents, who, how),
      possibly with more detail; OR the question is unanswerable and the assistant says the
      information "no consta" / refuses.
  0 = a key fact is missing or wrong, or it refuses a question that the reference answers,
      or it answers an unanswerable question with invented facts.
supported:
  1 = every factual claim in the answer appears in the retrieved passages (a refusal is supported).
  0 = at least one claim (especially a number, deadline, fee or document) is not in the passages.

Reply only with JSON: {"correct": 0 or 1, "supported": 0 or 1, "reason": "one short sentence"}"""


def judge(q: dict, a: dict) -> dict:
    prompt = (f"{RUBRIC}\n\nQUESTION: {q['question']}\nKIND: {q['kind']}\n"
              f"REFERENCE ANSWER: {q['reference_answer']}\n\nASSISTANT ANSWER: {a['answer']}\n\n"
              f"RETRIEVED PASSAGES:\n{a['retrieved'] or '(none)'}")
    for attempt in range(6):  # Gemini sometimes answers 503 (busy) or 429 (rate limit): wait and retry
        try:
            response = index.gemini().models.generate_content(
                model=MODEL, contents=prompt,
                config=types.GenerateContentConfig(temperature=0, response_mime_type="application/json"))
            return json.loads(response.text)
        except Exception as error:
            if attempt == 5 or not any(code in str(error) for code in ("503", "429")):
                raise
            print(f"  judge: Gemini busy, retrying in 30 s", flush=True)
            time.sleep(30)


def run_judge(questions: list[dict], answers: list[dict]) -> list[dict]:
    cached = {row["id"]: row for row in read_csv(EVAL / "verdicts.csv")}
    by_id = {a["id"]: a for a in answers}
    rows = []
    for q in questions:
        a = by_id[q["id"]]
        if q["id"] in cached and cached[q["id"]]["answer"] == a["answer"]:
            rows.append(cached[q["id"]])
            continue
        verdict = judge(q, a)
        rows.append({"id": q["id"], "kind": q["kind"], "answer": a["answer"],
                     "judge_correct": int(verdict["correct"]), "judge_supported": int(verdict["supported"]),
                     "judge_reason": verdict.get("reason", ""),
                     "failure_hint": failure_hint(q, a, verdict)})
    write_csv(EVAL / "verdicts.csv", rows)
    return rows


def failure_hint(q: dict, a: dict, verdict: dict) -> str:
    """A first guess at the failure cause, to be checked by hand in REPORT.md."""
    if int(verdict["correct"]) and int(verdict["supported"]):
        return ""
    if q["kind"] == "unanswerable":
        return "unsupported claim" if not int(a["refused"]) else "check by hand"
    if int(a["refused"]):
        retrieved = set(split(a["retrieved_sources"]))
        return "wrong refusal" if retrieved & set(split(q["expected_source"])) else "retrieval miss"
    if not set(split(a["retrieved_sources"])) & set(split(q["expected_source"])):
        return "retrieval miss"
    if not int(verdict["supported"]):
        return "unsupported claim"
    return "wrong answer from the right passage"


# ---------------------------------------------------------------- 5. agreement

def agreement(verdicts: list[dict]) -> dict:
    human = {row["id"]: row for row in read_csv(HUMAN_LABELS) if row.get("correct", "").strip()}
    judged = {row["id"]: row for row in verdicts}
    common = [i for i in human if i in judged]
    if not common:
        return {"graded_by_human": 0}
    same_correct = sum(int(human[i]["correct"]) == int(judged[i]["judge_correct"]) for i in common)
    same_supported = sum(int(human[i]["supported"]) == int(judged[i]["judge_supported"]) for i in common)
    return {"graded_by_human": len(common),
            "agreement_correct": round(same_correct / len(common), 3),
            "agreement_supported": round(same_supported / len(common), 3),
            "disagreements": [i for i in common if int(human[i]["correct"]) != int(judged[i]["judge_correct"])]}


# ---------------------------------------------------------------- 6. add-document demo

def add_document_demo() -> dict:
    """Ask about matrimonio civil without its ficha, add the ficha, ask again."""
    demo_file = EVAL / "add_document_demo.json"
    if demo_file.is_file():
        return json.loads(demo_file.read_text(encoding="utf-8"))
    collection = index.get_collection(index.CHOSEN_DESIGN)
    old = collection.get(where={"source": "matrimonio-civil"})
    if old["ids"]:
        collection.delete(ids=old["ids"])  # make sure we really start "before"
    before = answer(DEMO_QUESTION)["answer"]
    add_result = index.add_file(str(HELD_OUT))
    again = index.add_file(str(HELD_OUT))  # second time: should be skipped
    after = answer(DEMO_QUESTION)["answer"]
    demo = {"question": DEMO_QUESTION, "before": before, "add_document": add_result,
            "add_document_again": again, "after": after}
    demo_file.write_text(json.dumps(demo, ensure_ascii=False, indent=2), encoding="utf-8")
    return demo


# ---------------------------------------------------------------- main

def main() -> None:
    questions = read_csv(QUESTIONS)
    print(f"{len(questions)} questions")

    # The held-out ficha must not be in the index while we evaluate (it is added in the demo).
    if not (EVAL / "add_document_demo.json").is_file():
        collection = index.get_collection(index.CHOSEN_DESIGN)
        old = collection.get(where={"source": "matrimonio-civil"})
        if old["ids"]:
            collection.delete(ids=old["ids"])

    print("1. retrieval")
    retrieval = evaluate_retrieval(questions)
    print(json.dumps(retrieval, indent=2))

    print("2-3. agent and code checks")
    answers = run_agent(questions)

    print("4. judge")
    verdicts = run_judge(questions, answers)

    print("6. add-document demo")
    demo = add_document_demo()

    unanswerable = [a for a in answers if a["kind"] == "unanswerable"]
    answerable = [a for a in answers if a["kind"] != "unanswerable"]
    n = len(answers)
    summary = {
        "questions": n,
        "retrieval": retrieval,
        "judge_correct": round(sum(int(v["judge_correct"]) for v in verdicts) / n, 3),
        "judge_supported": round(sum(int(v["judge_supported"]) for v in verdicts) / n, 3),
        "correct_refusals": f"{sum(int(a['refused']) for a in unanswerable)}/{len(unanswerable)}",
        "wrong_refusals": f"{sum(int(a['refused']) for a in answerable)}/{len(answerable)}",
        "citations_valid": round(sum(int(a["citations_valid"]) for a in answers) / n, 3),
        "answerable_with_citation": f"{sum(int(a['has_citation']) for a in answerable)}/{len(answerable)}",
        "guardrail_fired": sum(int(a["guardrail_fired"]) for a in answers),
        "failure_hints": {h: sum(v["failure_hint"] == h for v in verdicts)
                          for h in sorted({v["failure_hint"] for v in verdicts if v["failure_hint"]})},
        "avg_tokens_per_question": round(sum(int(a["tokens"]) for a in answers) / n),
        "avg_seconds_per_question": round(sum(float(a["seconds"]) for a in answers) / n, 1),
        "human_vs_judge": agreement(verdicts),
        "add_document_demo": demo,
    }
    (EVAL / "summary.json").write_text(json.dumps(summary, ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k != "add_document_demo"}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
