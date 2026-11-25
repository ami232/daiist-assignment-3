"""
Assignment 3: evaluation (`main.py evaluate`).

1. Retrieval: hit rate at k = 1, 3, 5 for each design, on the answerable questions.
2. End to end: the agent answers every question (eval/answers.jsonl).
3. Code checks: refusals (fixed phrase from AGENTS.md rule 3), citations that
   point to passages the search really returned, expected article cited.
4. LLM judge with a rubric, the reference answer and the retrieved passages as
   evidence, for every answer that isn't a refusal (eval/judged.csv).
5. Agreement between the judge and my own grades in eval/human_labels.csv.
6. Cost: tokens and seconds per question (eval/summary.json).

Question vectors (eval/query_vectors.json) and agent answers (eval/answers.jsonl)
are saved as they arrive and reused on later runs to save API quota; run
`python evaluate.py --fresh` to ask the agent again.
"""

import csv
import json
import re
import sys
import time
from pathlib import Path

import pandas as pd
from langchain_google_genai import ChatGoogleGenerativeAI

from agent import REFUSAL, ask, citations, retrieved_passages, _law_key, _place_key
from api_key import load_api_key
from index import embed_query, search

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
VECTOR_CACHE = EVAL / "query_vectors.json"
ANSWERS = EVAL / "answers.jsonl"
HUMAN = EVAL / "human_labels.csv"
JUDGE_MODEL = "gemini-flash-lite-latest"  # a different model from the agent's main one

DESIGNS = {  # name -> (chunking design, hybrid search?)
    "fixed 300 words, vector": ("fixed", False),
    "one chunk per article, vector": ("article", False),
    "one chunk per article, hybrid": ("article", True),
}
KS = [1, 3, 5]


def load_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def query_vectors(questions: list[dict]) -> dict:
    cache = json.loads(VECTOR_CACHE.read_text()) if VECTOR_CACHE.exists() else {}
    for q in questions:
        if q["question"] not in cache:
            cache[q["question"]] = embed_query(q["question"])
            VECTOR_CACHE.write_text(json.dumps(cache))  # save each one as it arrives
    return cache


def expected(q: dict) -> list[tuple[str, str]]:
    return list(zip([s.strip() for s in q["expected_source"].split(";")],
                    [l.strip() for l in q["expected_location"].split(";")]))


def is_hit(chunk: dict, source: str, location: str) -> bool:
    """The chunk comes from the expected law and contains the expected article."""
    return chunk["source"] == source and location in [a.strip() for a in chunk["articles"].split(";")]


def retrieval_eval(questions: list[dict], vectors: dict) -> pd.DataFrame:
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    rows, per_question = [], []
    for name, (design, hybrid) in DESIGNS.items():
        results = {q["id"]: search(q["question"], design, k=max(KS), hybrid=hybrid,
                                   query_vector=vectors[q["question"]]) for q in answerable}
        row = {"design": name}
        for k in KS:
            any_hit, all_hit, words = [], [], []
            for q in answerable:
                top, exp = results[q["id"]][:k], expected(q)
                found = [any(is_hit(c, s, l) for c in top) for s, l in exp]
                any_hit.append(any(found))
                if q["kind"] == "multi":
                    all_hit.append(all(found))
                words.append(sum(len(c["text"].split()) for c in top))
            row[f"hit@{k}"] = round(sum(any_hit) / len(any_hit), 3)
            row[f"multi_both@{k}"] = round(sum(all_hit) / len(all_hit), 3)
            row[f"words@{k}"] = round(sum(words) / len(words))
        rows.append(row)
        for q in answerable:
            per_question.append({"design": name, "id": q["id"], "kind": q["kind"],
                                 "top5": " | ".join(f"{c['source'].split()[0]} {c['source'].split()[1]} {c['location']}"
                                                    for c in results[q["id"]]),
                                 "rank_of_first_hit": next((c["rank"] for c in results[q["id"]]
                                                            if any(is_hit(c, s, l) for s, l in expected(q))), None)})
    pd.DataFrame(per_question).to_csv(EVAL / "retrieval_per_question.csv", index=False)
    table = pd.DataFrame(rows)
    table.to_csv(EVAL / "retrieval_results.csv", index=False)
    return table


# ---------------------------------------------------------------------------
# End to end
# ---------------------------------------------------------------------------
def run_agent(questions: list[dict], fresh: bool) -> dict:
    done = {}
    if ANSWERS.exists() and not fresh:
        done = {r["id"]: r for r in map(json.loads, ANSWERS.read_text(encoding="utf-8").splitlines())}
    elif ANSWERS.exists():
        ANSWERS.unlink()
    for q in questions:
        if q["id"] in done:
            continue
        print(f"  asking {q['id']} ...", file=sys.stderr, flush=True)
        for attempt in range(5):  # Gemini's free tier sometimes answers 503 "high demand" or 429
            try:
                out = ask(q["question"], approve=lambda path: False)  # never add documents during evaluation
                break
            except Exception as error:  # noqa: BLE001
                if attempt == 4 or not re.search(r"503|429|UNAVAILABLE|RESOURCE_EXHAUSTED", str(error)):
                    raise
                print(f"  {q['id']}: Gemini busy, retrying in {30 * (attempt + 1)}s", file=sys.stderr, flush=True)
                time.sleep(30 * (attempt + 1))
        out["id"] = q["id"]
        done[q["id"]] = out
        with ANSWERS.open("a", encoding="utf-8") as f:  # save each answer as it arrives
            f.write(json.dumps(out, ensure_ascii=False) + "\n")
        time.sleep(2)  # stay under the free tier's per-minute limit
    return done


def code_checks(q: dict, out: dict) -> dict:
    trace = out["trace"]
    retrieved = retrieved_passages(trace)
    expected = {(_law_key(s), _place_key(l)) for s, l in expected_pairs(q)}
    cited = set(citations(out["answer"]))
    return {
        "refused": out["answer"].strip().startswith(REFUSAL),
        "guardrail_fired": bool(out["guardrail"]),
        "searches": sum(t["tool"] == "search" for t in trace),
        "n_citations": len(cited),
        "citations_valid": all(c in retrieved for c in cited),
        "expected_retrieved": bool(expected) and expected <= retrieved,
        "expected_cited": bool(expected) and expected <= cited,
        "tokens": out["tokens"]["input"] + out["tokens"]["output"],
        "seconds": out["seconds"],
    }


def expected_pairs(q: dict) -> list[tuple[str, str]]:
    return expected(q) if q["kind"] != "unanswerable" else []


RUBRIC = """You grade answers of an assistant about Spanish sports law. You get the question,
a reference answer written by a person, the passages the assistant retrieved, and the
assistant's answer. Grade two things, each 1 or 0:

correct = 1 if the answer gives the key facts of the reference answer (numbers, periods,
  who decides, yes/no) and contradicts none of them. Extra correct detail is fine. If the
  question has two parts and the answer gets only one right, correct = 0. If the
  reference says the laws don't cover the question, correct = 1 only if the answer says
  it isn't covered and doesn't invent the missing information.
supported = 1 if every factual claim about the law in the answer can be found in the
  retrieved passages. Any claim about the law that is not in the passages, even if it is
  true in reality, makes supported = 0. Advice on where to look ("consult a lawyer",
  "the federation's rules") is not a claim about the law.

Reply with JSON only: {"correct": 0 or 1, "supported": 0 or 1, "reason": "<one sentence>"}"""


def judge(q: dict, out: dict, llm) -> dict:
    passages = "\n\n".join(t["result"] for t in out["trace"] if t["tool"] == "search") or "(no passages)"
    prompt = (f"{RUBRIC}\n\nQUESTION:\n{q['question']}\n\nREFERENCE ANSWER:\n{q['reference_answer']}\n\n"
              f"RETRIEVED PASSAGES:\n{passages[:30000]}\n\nASSISTANT'S ANSWER:\n{out['answer']}")
    for attempt in range(4):
        try:
            reply = llm.invoke(prompt).content
            reply = "".join(p.get("text", "") if isinstance(p, dict) else str(p) for p in reply) \
                if isinstance(reply, list) else reply
            verdict = json.loads(re.search(r"\{.*\}", reply, re.S).group(0))
            return {"judge_correct": int(verdict["correct"]), "judge_supported": int(verdict["supported"]),
                    "judge_reason": verdict.get("reason", "")}
        except Exception as error:  # noqa: BLE001 - retry rate limits and malformed JSON
            print(f"  judge retry {q['id']}: {str(error)[:80]}", file=sys.stderr)
            time.sleep(10 * (attempt + 1))
    return {"judge_correct": None, "judge_supported": None, "judge_reason": "judge failed"}


def outcome(q: dict, row: dict) -> str:
    """One label per question, decided by code where it can and by the judge otherwise."""
    if q["kind"] == "unanswerable":
        if row["refused"]:
            return "correct refusal"
        return "answered an unanswerable question" if row["judge_correct"] == 0 else "correct (partial coverage)"
    if row["refused"]:
        return "wrong refusal"
    if row["judge_supported"] == 0:
        return "unsupported claim"
    return "correct" if row["judge_correct"] == 1 else "wrong answer"


def agreement(judged: pd.DataFrame) -> dict:
    if not HUMAN.exists():
        return {}
    human = pd.read_csv(HUMAN, dtype={"id": str}).dropna(subset=["correct"])
    if human.empty:
        return {}
    m = human.merge(judged, on="id")
    # For refusals the code decides correctness; compare the human with the system's final verdict
    system_correct = m["outcome"].isin(["correct", "correct refusal", "correct (partial coverage)"]).astype(int)
    system_supported = m["judge_supported"].fillna(1).astype(int)  # refusals make no claims
    out = {"n": int(len(m)),
           "agree_correct": round(float((m["correct"].astype(int) == system_correct).mean()), 3),
           "agree_supported": round(float((m["supported"].astype(int) == system_supported).mean()), 3)}
    out["disagreements"] = [
        {"id": r.id, "human_correct": int(r.correct), "system_correct": int(c), "human_supported": int(r.supported),
         "system_supported": int(sp), "human_notes": r.notes if isinstance(r.notes, str) else "",
         "judge_reason": r.judge_reason if isinstance(r.judge_reason, str) else ""}
        for r, c, sp in zip(m.itertuples(), system_correct, system_supported)
        if int(r.correct) != c or int(r.supported) != sp]
    return out


def end_to_end(questions: list[dict], fresh: bool) -> dict:
    load_api_key()
    answers = run_agent(questions, fresh)
    llm = ChatGoogleGenerativeAI(model=JUDGE_MODEL, temperature=0)
    rows = []
    for q in questions:
        out = answers[q["id"]]
        row = {"id": q["id"], "kind": q["kind"], **code_checks(q, out)}
        if row["refused"]:
            row.update({"judge_correct": None, "judge_supported": None, "judge_reason": "refusal: decided in code"})
        else:
            row.update(judge(q, out, llm))
        row["outcome"] = outcome(q, row)
        row["answer"] = out["answer"]
        rows.append(row)
    judged = pd.DataFrame(rows)
    judged.to_csv(EVAL / "judged.csv", index=False)

    # Grading sheet for my own labels: question, reference and answer, WITHOUT the judge's verdict
    sheet = pd.DataFrame([{"id": q["id"], "kind": q["kind"], "question": q["question"],
                           "reference_answer": q["reference_answer"], "agent_answer": answers[q["id"]]["answer"],
                           "retrieved": "; ".join(f"{s} {l}" for s, l in sorted(retrieved_passages(answers[q["id"]]["trace"])))}
                          for q in questions])
    sheet.to_csv(EVAL / "grading_sheet.csv", index=False)

    summary = {
        "questions": len(judged),
        "outcomes": judged["outcome"].value_counts().to_dict(),
        "answered_correct_rate": round(float((judged["outcome"] == "correct").sum()
                                             / max((judged["kind"] != "unanswerable").sum(), 1)), 3),
        "citations_valid_rate": round(float(judged.loc[~judged["refused"], "citations_valid"].mean()), 3),
        "expected_cited_rate": round(float(judged.loc[judged["kind"] != "unanswerable", "expected_cited"].mean()), 3),
        "guardrail_fired": judged.loc[judged["guardrail_fired"], "id"].tolist(),
        "tokens_per_question": {"mean": round(float(judged["tokens"].mean())), "median": round(float(judged["tokens"].median()))},
        "seconds_per_question": {"mean": round(float(judged["seconds"].mean()), 1),
                                 "median": round(float(judged["seconds"].median()), 1)},
        "agreement_with_my_labels": agreement(judged),
    }
    (EVAL / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    return summary


if __name__ == "__main__":
    questions = load_questions()
    vectors = query_vectors(questions)
    table = retrieval_eval(questions, vectors)
    print("\nRetrieval (answerable questions, n =", sum(q["kind"] != "unanswerable" for q in questions), ")")
    print(table.to_string(index=False))
    if "--retrieval-only" in sys.argv:
        raise SystemExit(0)
    summary = end_to_end(questions, fresh="--fresh" in sys.argv)
    print("\nEnd to end:")
    print(json.dumps({k: v for k, v in summary.items() if k != "agreement_with_my_labels"}, indent=2, ensure_ascii=False))
    print("Agreement with my labels:", json.dumps(summary["agreement_with_my_labels"], ensure_ascii=False)[:600])
