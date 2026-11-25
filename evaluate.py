"""
Assignment 3: evaluation (`uv run python main.py evaluate`).

Steps:
  1. RETRIEVAL: hit rate at k = 1, 3, 5 for each design (fixed, sections, sections_hybrid).
  2. ANSWERS:   run the agent on every question in eval/questions.csv.
  3. CODE CHECKS: refusal? citations valid? (no LLM needed for these)
  4. LLM JUDGE: grades correctness and support, with a rubric and the retrieved text.
  5. AGREEMENT: compare the judge with your own grades in eval/human_labels.csv.
  6. SUMMARY:   counts, failure hints, cost (tokens, seconds) -> files in eval/.

Everything expensive is SAVED AS WE GO (question vectors, answers, verdicts), so
re-running only does the missing work. To redo a step, delete its file in eval/.
"""

import asyncio
import json
import time

import pandas as pd
from google.genai import types

from agent import answer_question, apply_guardrail, check_citations, is_refusal
from config import CHAT_MODEL, CHOSEN_DESIGN, DESIGNS, EVAL_DIR
from index import embed_queries, get_client
from retrieve import search

QUESTIONS = EVAL_DIR / "questions.csv"
VECTORS = EVAL_DIR / "query_vectors.json"      # cache: question -> embedding
ANSWERS = EVAL_DIR / "answers.jsonl"           # cache: one agent answer per line
VERDICTS = EVAL_DIR / "judge.jsonl"            # cache: one judge verdict per line
HUMAN = EVAL_DIR / "human_labels.csv"
CRITERIA = EVAL_DIR / "grading_criteria.csv"   # my per-question criteria, given to the judge


# =============================================================================
# Small helpers
# =============================================================================

def load_jsonl(path) -> dict:
    """Read a .jsonl cache into {question id: record}."""
    if not path.exists():
        return {}
    records = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return {r["id"]: r for r in records}


def append_jsonl(path, record: dict) -> None:
    """Add one record to a .jsonl cache immediately (so a crash loses nothing)."""
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record) + "\n")


def expected_passages(row) -> list[tuple[str, str]]:
    """'ELIQUIS;XARELTO' + '2.4;2.5' -> [('ELIQUIS','2.4'), ('XARELTO','2.5')].
    One source with several locations -> that source for each location."""
    sources = [s.strip() for s in row["expected_source"].split(";") if s.strip()]
    locations = [l.strip() for l in row["expected_location"].split(";") if l.strip()]
    if len(sources) == 1:
        sources = sources * len(locations)
    return list(zip(sources, locations))


def chunk_matches(chunk: dict, source: str, location: str) -> bool:
    """Does this chunk hold the expected passage? "8" matches 8, 8.1, 8.6...; "8.6" matches only 8.6."""
    if chunk["source"] != source:
        return False
    return any(loc == location or loc.startswith(location + ".") for loc in chunk["location"].split(";"))


def is_hit(expected: list, chunks: list[dict]) -> bool:
    """Hit rate as in class: at least one of the chunks covers a correct passage."""
    return any(chunk_matches(c, s, l) for c in chunks for s, l in expected)


def all_found(expected: list, chunks: list[dict]) -> bool:
    """Stricter, for 'multi' questions: EVERY expected passage is among the chunks."""
    return all(any(chunk_matches(c, s, l) for c in chunks) for s, l in expected)


# =============================================================================
# 1. RETRIEVAL
# =============================================================================

def question_vectors(questions: pd.DataFrame) -> dict:
    """Embed every question once and keep the vectors in eval/query_vectors.json."""
    cache = json.loads(VECTORS.read_text()) if VECTORS.exists() else {}
    missing = [q for q in questions["question"] if q not in cache]
    for i in range(0, len(missing), 10):
        batch = missing[i:i + 10]
        for q, v in zip(batch, embed_queries(batch)):
            cache[q] = v
        VECTORS.write_text(json.dumps(cache))           # save after every batch
    return cache


def evaluate_retrieval(questions: pd.DataFrame, vectors: dict) -> pd.DataFrame:
    answerable = questions[questions["kind"] != "unanswerable"]
    rows, per_question = [], []
    for design in DESIGNS:
        hits = {1: [], 3: [], 5: []}
        multi_all = []          # multi questions: were BOTH passages in the top 5?
        prompt_words = []
        for _, q in answerable.iterrows():
            top5 = search(q["question"], design=design, k=5, query_vector=vectors[q["question"]])
            expected = expected_passages(q)
            for k in hits:
                hits[k].append(is_hit(expected, top5[:k]))
            if q["kind"] == "multi":
                multi_all.append(all_found(expected, top5))
            prompt_words.append(sum(len(c["text"].split()) for c in top5))
            per_question.append({"id": q["id"], "design": design, "hit@5": is_hit(expected, top5),
                                 "retrieved": " | ".join(f"{c['source']} §{c['location']}" for c in top5)})
        rows.append({"design": design,
                     "hit@1": round(sum(hits[1]) / len(hits[1]), 3),
                     "hit@3": round(sum(hits[3]) / len(hits[3]), 3),
                     "hit@5": round(sum(hits[5]) / len(hits[5]), 3),
                     "multi_both_found@5": round(sum(multi_all) / len(multi_all), 3) if multi_all else None,
                     "words_in_prompt_top5": round(sum(prompt_words) / len(prompt_words))})
    pd.DataFrame(per_question).to_csv(EVAL_DIR / "retrieval_per_question.csv", index=False)
    table = pd.DataFrame(rows)
    table.to_csv(EVAL_DIR / "retrieval_results.csv", index=False)
    return table


# =============================================================================
# 2. ANSWERS (agent on every question)
# =============================================================================

def run_agent_on_all(questions: pd.DataFrame) -> dict:
    answers = load_jsonl(ANSWERS)
    # The guardrail is plain code, so re-apply the CURRENT version to saved answers (free, no API call).
    for a in answers.values():
        a["answer"], a["guardrail_fired"], a["guardrail_reason"] = apply_guardrail(a["raw_answer"], a["retrieved_text"])
    for _, q in questions.iterrows():
        if q["id"] in answers:                          # already answered in an earlier run
            continue
        print(f"  asking {q['id']}: {q['question'][:70]}")
        try:
            # approve=lambda ...: False -> the agent may never add documents during evaluation
            result = asyncio.run(answer_question(q["question"], approve=lambda action: False))
        except Exception as error:
            print(f"  stopped at {q['id']}: {str(error)[:200]}\n  (probably the rate limit: run evaluate again later)")
            break
        result["id"] = q["id"]
        append_jsonl(ANSWERS, result)
        answers[q["id"]] = result
        time.sleep(5)                                   # be gentle with the free tier
    return answers


# =============================================================================
# 4. LLM JUDGE
# =============================================================================

# The judge's rubric. Two separate grades, because they catch different failures:
#   correct   = same key facts as my reference answer (a wrong number or missing condition fails)
#   supported = every claim can be found in the retrieved text (catches answers from memory)
RUBRIC = """You grade an assistant that answers clinicians' questions from FDA drug labels.

You get: the QUESTION, a REFERENCE answer written by a human, the EVIDENCE (label passages
the assistant retrieved) and the ANSWER.

correct = 1 if the ANSWER gives the same key facts as the REFERENCE: same drug, same
numbers with the same units and conditions (doses, CrCl thresholds, hours). Extra true
detail is fine. A missing key condition, a wrong number, or the wrong drug = 0.
If the REFERENCE says the corpus does not cover the question, correct = 1 only if the
ANSWER says it does not cover it.

supported = 1 if EVERY factual claim in the ANSWER can be found in the EVIDENCE
(paraphrase is fine). Any claim not in the EVIDENCE = 0. A pure refusal = 1.

Reply with JSON only: {"correct": 0 or 1, "supported": 0 or 1, "reason": "one sentence"}"""


def judge(client, question: str, reference: str, evidence: str, answer: str, criteria: str = "") -> dict:
    prompt = (f"QUESTION: {question}\n\nREFERENCE: {reference}\n\n"
              f"{criteria}"
              f"EVIDENCE:\n{evidence or '(nothing retrieved)'}\n\nANSWER: {answer}")
    response = client.models.generate_content(
        model=CHAT_MODEL,
        contents=prompt,
        config=types.GenerateContentConfig(
            system_instruction=RUBRIC,
            response_mime_type="application/json",               # forces a JSON reply
            thinking_config=types.ThinkingConfig(thinking_level="low"),
        ),
    )
    return json.loads(response.text)


def grade_all(questions: pd.DataFrame, answers: dict) -> dict:
    """Code checks for what code can check, the judge for the rest."""
    client = get_client()          # the same client (with retries) as index.py
    # My criteria for each question: what makes THIS answer correct and grounded.
    criteria = {}
    if CRITERIA.exists():
        for _, c in pd.read_csv(CRITERIA, dtype=str).fillna("").iterrows():
            criteria[c["id"]] = (f"WHAT 'correct' MEANS FOR THIS QUESTION: {c['correctness_criterion']}\n"
                                 f"WHAT 'supported' MEANS FOR THIS QUESTION: {c['groundedness_criterion']}\n\n")
    verdicts = load_jsonl(VERDICTS)
    for _, q in questions.iterrows():
        if q["id"] not in answers:
            continue
        old = verdicts.get(q["id"])
        if old and old.get("answer", answers[q["id"]]["answer"]) == answers[q["id"]]["answer"]:
            continue                       # already graded, and the answer has not changed since
        a = answers[q["id"]]
        refused = is_refusal(a["answer"])
        citations_ok, _ = check_citations(a["raw_answer"], a["retrieved_text"])
        record = {"id": q["id"], "refused": refused, "citations_valid": citations_ok, "answer": a["answer"]}

        # 3. CODE CHECKS decide the clear cases without calling the judge:
        if refused:
            # A refusal is correct only for unanswerable questions; it claims nothing.
            record.update(correct=int(q["kind"] == "unanswerable"), supported=1, graded_by="code",
                          reason="refused")
        else:
            try:
                verdict = judge(client, q["question"], q["reference_answer"], a["retrieved_text"], a["answer"],
                                criteria.get(q["id"], ""))
            except Exception as error:
                print(f"  judge stopped at {q['id']}: {str(error)[:200]}")
                break
            record.update(correct=int(verdict["correct"]), supported=int(verdict["supported"]),
                          graded_by="judge", reason=verdict.get("reason", ""))
            if q["kind"] == "unanswerable":   # answering an unanswerable question is wrong, by code
                record["correct"] = 0
            if not citations_ok:              # an invented citation is never "supported", by code
                record["supported"] = 0
        append_jsonl(VERDICTS, record)
        verdicts[q["id"]] = record
        time.sleep(3)
    return verdicts


# =============================================================================
# 5 + 6. AGREEMENT AND SUMMARY
# =============================================================================

def failure_hint(q, v, hit) -> str:
    """A first guess at the failure cause. YOU confirm or change it in the report."""
    if v["correct"] == 1 and v["supported"] == 1:
        return ""
    if q["kind"] == "unanswerable":
        return "unsupported claim (answered an unanswerable question)"
    if v["refused"]:
        return "wrong refusal" if hit else "retrieval miss"
    if v["supported"] == 0:
        return "unsupported claim"
    return "wrong answer from the right passage" if hit else "retrieval miss"


def load_labels(question_ids: list[str]) -> pd.DataFrame | None:
    """Read eval/human_labels.csv and keep only VALID rows. Problems are printed, never hidden:
    a missing or invalid grade is left out of the agreement, not turned into a 0."""
    if not HUMAN.exists():
        print("   no eval/human_labels.csv yet: agreement skipped")
        return None
    labels = pd.read_csv(HUMAN, dtype=str).fillna("")
    labels["id"] = labels["id"].str.strip()
    labels = labels[labels["id"] != ""]

    duplicated = sorted(set(labels.loc[labels["id"].duplicated(), "id"]))
    unknown = sorted(set(labels["id"]) - set(question_ids))
    valid_value = labels["correct"].str.strip().isin(["0", "1"]) & labels["supported"].str.strip().isin(["0", "1"])
    invalid = labels.loc[~valid_value, "id"].tolist()
    missing = [i for i in question_ids if i not in set(labels["id"])]
    for name, ids in [("duplicate ids (all copies ignored)", duplicated), ("unknown ids", unknown),
                      ("grades that are not 0 or 1", invalid), ("questions without a label", missing)]:
        if ids:
            print(f"   labels: {name}: {', '.join(ids)}")

    labels = labels[valid_value & ~labels["id"].isin(duplicated) & ~labels["id"].isin(unknown)].copy()
    labels["correct"] = labels["correct"].astype(int)
    labels["supported"] = labels["supported"].astype(int)
    return labels


def cohen_kappa(a: pd.Series, b: pd.Series) -> float | None:
    """Agreement corrected for chance: 1 = perfect, 0 = no better than chance.
    kappa = (observed agreement - chance agreement) / (1 - chance agreement)."""
    observed = (a == b).mean()
    chance = a.mean() * b.mean() + (1 - a.mean()) * (1 - b.mean())   # both say 1, or both say 0, by chance
    if chance == 1:
        return None          # both graders gave the same single value to everything: kappa undefined
    return round((observed - chance) / (1 - chance), 3)


def main() -> None:
    questions = pd.read_csv(QUESTIONS, dtype=str).fillna("")

    print("\n1. Retrieval")
    vectors = question_vectors(questions)
    retrieval = evaluate_retrieval(questions, vectors)
    print(retrieval.to_string(index=False))
    print(f"   (the server uses CHOSEN_DESIGN = '{CHOSEN_DESIGN}' from config.py)")

    print("\n2. Agent answers")
    answers = run_agent_on_all(questions)

    print("\n3-4. Code checks and LLM judge")
    verdicts = grade_all(questions, answers)

    # One table with everything per question -> eval/results.csv
    hits = pd.read_csv(EVAL_DIR / "retrieval_per_question.csv")
    hits = hits[hits["design"] == CHOSEN_DESIGN].set_index("id")["hit@5"].to_dict()
    rows = []
    for _, q in questions.iterrows():
        if q["id"] not in verdicts:
            continue
        a, v = answers[q["id"]], verdicts[q["id"]]
        hit = bool(hits.get(q["id"], False))
        rows.append({"id": q["id"], "kind": q["kind"], "question": q["question"],
                     "reference_answer": q["reference_answer"], "answer": a["answer"],
                     "refused": v["refused"], "citations_valid": v["citations_valid"],
                     "guardrail_fired": a["guardrail_fired"], "retrieval_hit@5": hit,
                     "judge_correct": v["correct"], "judge_supported": v["supported"],
                     "graded_by": v["graded_by"], "judge_reason": v["reason"],
                     "failure_hint": failure_hint(q, v, hit), "failure_cause": "",
                     "tokens": a["tokens"]["total"], "seconds": a["seconds"]})
    results = pd.DataFrame(rows)
    if results.empty:
        print("No graded answers yet.")
        return
    results.to_csv(EVAL_DIR / "results.csv", index=False)
    # The same answers WITHOUT the judge's verdicts: grade these yourself, before looking at results.csv.
    results[["id", "kind", "question", "reference_answer", "answer"]].to_csv(
        EVAL_DIR / "answers_for_grading.csv", index=False)

    answerable = results[results["kind"] != "unanswerable"]
    unanswerable = results[results["kind"] == "unanswerable"]
    summary = {
        "questions_graded": len(results),
        "answerable_correct": int(answerable["judge_correct"].sum()),
        "answerable_total": len(answerable),
        "unsupported_answers": int((results["judge_supported"] == 0).sum()),
        "correct_refusals": int(unanswerable["refused"].sum()),
        "unanswerable_total": len(unanswerable),
        "wrong_refusals": int(answerable["refused"].sum()),
        "guardrail_fired": int(results["guardrail_fired"].sum()),
        "avg_tokens_per_question": round(results["tokens"].mean()),
        "avg_seconds_per_question": round(results["seconds"].mean(), 1),
    }

    summary["questions_in_test_set"] = len(questions)
    summary["abstention_accuracy_unanswerable"] = (
        round(unanswerable["refused"].mean(), 3) if len(unanswerable) else None)

    # Results per question type (single / multi / unanswerable) -> eval/results_by_kind.csv
    by_kind = results.groupby("kind").agg(
        questions=("id", "count"),
        correct_rate=("judge_correct", "mean"),
        supported_rate=("judge_supported", "mean"),
        refused=("refused", "sum"),
    ).round(3)
    by_kind.loc["ALL"] = [len(results), round(results["judge_correct"].mean(), 3),
                          round(results["judge_supported"].mean(), 3), int(results["refused"].sum())]
    by_kind.to_csv(EVAL_DIR / "results_by_kind.csv")

    # 5. Agreement between the judge and the labels in eval/human_labels.csv,
    #    computed ONLY on questions that have both a judge verdict and a valid label.
    print("\n5. Agreement with eval/human_labels.csv")
    labels = load_labels(questions["id"].tolist())
    if labels is not None:
        both = labels.merge(results, on="id")
        summary["labels_valid"] = len(labels)
        summary["labels_compared_with_judge"] = len(both)
        if len(both):
            for grade in ["correct", "supported"]:
                summary[f"agreement_{grade}"] = round((both[grade] == both[f"judge_{grade}"]).mean(), 3)
                summary[f"kappa_{grade}"] = cohen_kappa(both[grade], both[f"judge_{grade}"])
            disagree = both[(both["correct"] != both["judge_correct"]) |
                            (both["supported"] != both["judge_supported"])]
            disagree[["id", "kind", "correct", "judge_correct", "supported", "judge_supported",
                      "notes", "judge_reason"]].to_csv(EVAL_DIR / "disagreements.csv", index=False)
            print(f"   {len(disagree)} disagreement(s) written to eval/disagreements.csv")

    (EVAL_DIR / "summary.json").write_text(json.dumps(summary, indent=2))
    print("\n6. Summary (also in eval/summary.json)")
    for key, value in summary.items():
        print(f"   {key:34} {value}")
    print("\nBy question type (also in eval/results_by_kind.csv):")
    print(by_kind.to_string())
    print("\nFailures with a first-guess cause:")
    print(results[results["failure_hint"] != ""][["id", "kind", "failure_hint"]].to_string(index=False))


if __name__ == "__main__":
    main()
