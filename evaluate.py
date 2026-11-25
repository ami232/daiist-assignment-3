"""
Assignment 3: evaluation (`main.py evaluate`). May be evaluate.ipynb instead.

Hit rate at 1/3/5 per retrieval design; agent answers on every question;
code checks; an LLM judge with a rubric and the retrieved text as evidence;
agreement with eval/human_labels.csv. Save results in eval/.

Start from session 10's 07-own-harness/evaluate.py.
"""

import csv
import json
import statistics
import sys
import time
from pathlib import Path

from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel

import agent
import index
import server
from api_key import load_api_key

EVAL = Path(__file__).resolve().parent / "eval"
ANSWERS = EVAL / "answers.json"       # agent answers and judge verdicts, saved after every question
DEMO_QUESTION = "q28"                 # the unanswerable question that the extra document answers
PAUSE = 5                             # seconds between questions (free-tier rate limit)

RUBRIC = """You grade one answer of a question-answering assistant over a corpus of EU data law.
correct: for kind "single" or "multi", true only if the answer states the key facts of the reference answer
(numbers, deadlines, conditions) and contradicts none; a missing half of a "multi" answer or a refusal is false.
For kind "unanswerable", true only if the answer says the corpus does not cover the question and does not
answer it anyway.
supported: true only if every factual claim in the answer appears in the retrieved passages (ignore the
reference here). A refusal with no claims is supported.
reason: one sentence."""


class Verdict(BaseModel):
    correct: bool
    supported: bool
    reason: str


def read_csv(path):
    with path.open(newline="", encoding="utf-8-sig") as file:
        return [row for row in csv.DictReader(file) if row.get("id")]


def write_csv(path, rows):
    with path.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def save(answers):
    ANSWERS.write_text(json.dumps(answers, indent=1, ensure_ascii=False), encoding="utf-8")


def expected_tags(q):
    """["[gdpr | Article 33]", ...] from the two `;`-separated columns of questions.csv."""
    sources, locations = q["expected_source"].split(";"), q["expected_location"].split(";")
    return [f"[{s.strip()} | {l.strip()}]" for s, l in zip(sources, locations) if s.strip()]


def table(rows):
    head = list(rows[0])
    lines = ["| " + " | ".join(head) + " |", "|" + "---|" * len(head)]
    return "\n".join(lines + ["| " + " | ".join(str(r[h]) for h in head) + " |" for r in rows])


def never_approve(tool, args):
    return False


def ask(question):
    try:
        return agent.ask(question, approve=never_approve)
    except Exception as error:
        raise SystemExit(f"STOPPED: the model call failed ({str(error)[:200]}). Answers so far are saved; "
                         "run `uv run python main.py evaluate` again later and it continues.")


def classify(q, a):
    """Outcome of one question and, if it failed, the cause (the brief's categories)."""
    found = all(tag in a["retrieved"] for tag in expected_tags(q))
    if q["kind"] == "unanswerable":
        ok = a["refused"] and a["judge"]["correct"]
        return ("correct refusal", "") if ok else ("answered an unanswerable question", "unsupported claim")
    if a["refused"]:
        return "wrong refusal", ("wrong refusal" if found else "retrieval miss")
    if not a["judge"]["supported"]:
        return "unsupported", "unsupported claim"
    if a["judge"]["correct"]:
        return "correct", ""
    return "wrong", ("wrong answer from the right passage" if found else "retrieval miss")


def main():
    sys.stdout.reconfigure(errors="replace")
    questions = read_csv(EVAL / "questions.csv")
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    answers = json.loads(ANSWERS.read_text(encoding="utf-8")) if ANSWERS.exists() else {}

    # 1. Run the agent on every question (already saved answers are kept).
    for q in questions:
        if answers.get(q["id"], {}).get("question") != q["question"]:
            answers[q["id"]] = ask(q["question"])
            save(answers)
            print(f"{q['id']}: {answers[q['id']]['answer'][:80]}", flush=True)
            time.sleep(PAUSE)

    # 2. Add a document that answers one unanswerable question; show the answer before and after.
    demo = next(q for q in questions if q["id"] == DEMO_QUESTION)
    if "demo" not in answers:
        path = index.download(index.EXTRA_DOCUMENT)
        try:
            first = server.add_document(str(path))
            second = server.add_document(str(path))        # what happens if it is already indexed
            index.close_store()
            after = ask(demo["question"])
        finally:
            index.remove_document(index.EXTRA_DOCUMENT["source"])      # the committed index stays the base corpus
        answers["demo"] = {"question": demo["question"], "first_call": first, "second_call": second,
                           "before": answers[DEMO_QUESTION]["answer"], "after": after["answer"]}
        save(answers)

    # 3. Retrieval: hit rate at k = 1, 3, 5 for each design.
    retrieval = []
    for design in index.DESIGNS:
        hits = {1: 0, 3: 0, 5: 0}
        prompt_words = []
        for q in answerable:
            results = index.search(q["question"], k=5, design=design)
            wanted = expected_tags(q)
            ranks = [rank for rank, r in enumerate(results, start=1)
                     if any(f"[{r['source']} | {loc}]" in wanted for loc in r["locations"].split("|"))]
            for k in hits:
                hits[k] += 1 if ranks and ranks[0] <= k else 0
            prompt_words.append(sum(r["words"] for r in results))
        retrieval.append({"design": design, **{f"hit@{k}": f"{hits[k] / len(answerable):.2f}" for k in hits},
                          "words added to the prompt (k=5)": round(statistics.mean(prompt_words))})
    write_csv(EVAL / "retrieval.csv", retrieval)

    # 4. LLM judge: correct and supported, with the retrieved passages as evidence.
    judge = ChatGoogleGenerativeAI(model=agent.CHAT_MODEL, api_key=load_api_key()).with_structured_output(Verdict)
    for q in questions:
        a = answers[q["id"]]
        if "judge" not in a:
            verdict = judge.invoke(f"{RUBRIC}\n\nQUESTION ({q['kind']}): {q['question']}\n\nREFERENCE ANSWER: "
                                   f"{q['reference_answer']}\n\nRETRIEVED PASSAGES:\n{a['passages']}\n\nANSWER:\n{a['answer']}")
            a["judge"] = verdict.model_dump()
            save(answers)
            time.sleep(PAUSE)

    # 5. Code checks, outcome and failure cause per question.
    results = []
    for q in questions:
        a = answers[q["id"]]
        outcome, cause = classify(q, a)
        results.append({
            "id": q["id"], "kind": q["kind"], "outcome": outcome, "cause": cause,
            "refused": int(a["refused"]),                                            # code check
            "citations_valid": int(all(c in a["retrieved"] for c in a["citations"])),  # code check
            "cites_expected": int(any(c in expected_tags(q) for c in a["citations"])),  # code check
            "guardrail_fired": int(a["blocked"]),
            "judge_correct": int(a["judge"]["correct"]), "judge_supported": int(a["judge"]["supported"]),
            "tokens": a["tokens"], "seconds": a["seconds"]})
    write_csv(EVAL / "results.csv", results)

    # 6. A sheet for grading 20 answers by hand (no judge verdicts in it).
    sample = ([q for q in questions if q["kind"] == "unanswerable"] + [q for q in questions if q["kind"] == "multi"]
              + [q for q in questions if q["kind"] == "single"])[:20]
    sheet = ["# Answers to grade by hand", "", "Add one row per answer to eval/human_labels.csv: id,correct,supported,notes", ""]
    for q in sample:
        a = answers[q["id"]]
        sheet += [f"## {q['id']} ({q['kind']})", f"**Question:** {q['question']}", "", f"**Reference:** {q['reference_answer']}",
                  "", f"**Answer:** {a['answer']}", "", "**Retrieved passages:**", "", "```", a["passages"], "```", ""]
    (EVAL / "answers_to_grade.md").write_text("\n".join(sheet), encoding="utf-8")

    # 7. Agreement between the judge and my own labels.
    labels = [l for l in read_csv(EVAL / "human_labels.csv") if l["id"] in answers]
    agreement = []
    for field in ("correct", "supported"):
        same = sum(1 for l in labels if (l[field].strip() == "1") == answers[l["id"]]["judge"][field])
        agreement.append({"grade": field, "answers I graded": len(labels), "judge agrees with me": same})

    # 8. Summary for the report.
    def count(rows, outcome):
        return sum(1 for r in rows if r["outcome"] == outcome)

    can = [r for r in results if r["kind"] != "unanswerable"]
    cannot = [r for r in results if r["kind"] == "unanswerable"]
    headline = [
        {"measure": "correct (answerable questions)", "value": f"{count(can, 'correct')} of {len(can)}"},
        {"measure": "unsupported (answer has a claim that is not in the passages)", "value": f"{count(can, 'unsupported')} of {len(can)}"},
        {"measure": "wrong refusals (answerable questions refused)", "value": f"{count(can, 'wrong refusal')} of {len(can)}"},
        {"measure": "correct refusals (unanswerable questions)", "value": f"{count(cannot, 'correct refusal')} of {len(cannot)}"},
        {"measure": "citations valid (code check)", "value": f"{sum(r['citations_valid'] for r in results)} of {len(results)}"},
        {"measure": "guardrail fired", "value": f"{sum(r['guardrail_fired'] for r in results)} of {len(results)}"},
    ]
    failures = [{"id": r["id"], "kind": r["kind"], "outcome": r["outcome"], "cause": r["cause"],
                 "judge's reason": answers[r["id"]]["judge"]["reason"]} for r in results if r["cause"]]
    cost = [{"per question": "tokens", "mean": round(statistics.mean(r["tokens"] for r in results)), "max": max(r["tokens"] for r in results)},
            {"per question": "seconds", "mean": round(statistics.mean(r["seconds"] for r in results), 1), "max": max(r["seconds"] for r in results)}]
    d = answers["demo"]
    summary = ["# Evaluation summary", "", f"Model: {agent.CHAT_MODEL}. The agent searches the `{index.CHOSEN}` design.", "",
               "## Retrieval", "", table(retrieval), "", "## Results", "", table(headline), "",
               "## Agreement with my labels", "", table(agreement), "",
               "## Failures", "", table(failures) if failures else "No failed questions.", "",
               "## Cost per question", "", table(cost), "",
               "## Adding a document", "", f"Question {DEMO_QUESTION}: {d['question']}", "",
               f"- add_document, first call: {d['first_call']}", f"- add_document, second call: {d['second_call']}", "",
               f"**Before:** {d['before']}", "", f"**After:** {d['after']}", ""]
    (EVAL / "summary.md").write_text("\n".join(summary), encoding="utf-8")
    print("\n".join(summary))


if __name__ == "__main__":
    main()
