"""
Assignment 3: evaluation (`main.py evaluate`).

1. Retrieval: hit rate at k = 1, 3, 5 for four designs
   (fixed / structure chunking x dense / hybrid search)        -> eval/retrieval_results.csv
2. End to end: the agent answers every question                 -> eval/answers.jsonl
3. Code checks: refusal or not, citations valid, citations hit the expected source
4. LLM judge (Gemini, rubric below, retrieved text as evidence) -> eval/judgments.csv
5. Agreement between the judge and eval/human_labels.csv
6. Failure classification and cost                              -> eval/results.csv, eval/summary.md

Everything expensive is cached in eval/ (query vectors, answers, verdicts), so running
it again only spends quota on questions that have no saved result yet.
Use `python evaluate.py --fresh` to re-run the agent and judge on every question.
"""

import asyncio
import csv
import json
import statistics
import sys
import time
from pathlib import Path

from google.genai import types

import index as pipeline
import retrieval
from agent import REFUSAL, check_citations, find_citations, run as run_agent

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
QUERY_CACHE = EVAL / "query_vectors.json"
ANSWERS = EVAL / "answers.jsonl"
JUDGMENTS = EVAL / "judgments.csv"
HUMAN = EVAL / "human_labels.csv"
OVERRIDES = EVAL / "failure_overrides.csv"   # my manual verdicts, e.g. "bad test question"
JUDGE_MODEL = "gemini-3.5-flash-lite"   # newer and larger than the agent's model; the bigger
# flash models (3.8, 3.7, 3.5) were returning 503 "high demand" all day on 18 Nov 2026
JUDGE_FALLBACKS = ["gemini-3.8-flash", "gemini-3.7-flash"]  # only if it stays overloaded (503)
FRESH = "--fresh" in sys.argv

RUBRIC = """You are grading an answer from a drug-label assistant used by nurses.
You get the question, a reference answer written by the test author, the passages the
assistant retrieved (its only allowed evidence), and the assistant's answer.

Grade two things, each 1 or 0:

correct:
  1 = the answer gives the same key facts as the reference answer (doses, numbers, drug
      names, yes/no) and nothing that contradicts it. Extra correct detail is fine.
      If the reference says the corpus cannot answer, 1 only if the assistant refuses.
  0 = a key fact is missing, wrong or contradicts the reference; or it refuses although
      the reference gives an answer; or it answers although the reference says it cannot.

supported:
  1 = every factual claim in the answer can be found in the retrieved passages
      (a refusal counts as supported).
  0 = at least one claim (a number, a dose, a condition) is not in the passages.

Reply with JSON only: {"correct": 0 or 1, "supported": 0 or 1, "reason": "<one sentence>"}"""


# --------------------------------------------------------------------------- helpers

def read_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r["question"].strip()]


def expected_pairs(q: dict) -> list[tuple[str, str]]:
    """(source, section) pairs that answer the question. ';' separates several."""
    sources = [s.strip() for s in q["expected_source"].split(";") if s.strip()]
    locations = [s.strip() for s in q["expected_location"].split(";") if s.strip()]
    if len(locations) == 1 and len(sources) > 1:
        locations = locations * len(sources)
    if len(sources) == 1 and len(locations) > 1:
        sources = sources * len(locations)
    return list(zip(sources, locations))


def chunk_hits(row: dict, pair: tuple[str, str]) -> bool:
    source, section = pair
    covered = [s.strip().lower() for s in row["sections"].split(";")]
    return row["source"] == source and section.lower() in covered


def query_vectors(questions: list[dict]) -> dict:
    cache = json.loads(QUERY_CACHE.read_text()) if QUERY_CACHE.exists() else {}
    missing = [q["question"] for q in questions if q["question"] not in cache]
    for i in range(0, len(missing), 20):
        batch = missing[i:i + 20]
        for text, vec in zip(batch, pipeline.embed_texts(batch, task="RETRIEVAL_QUERY")):
            cache[text] = vec
        QUERY_CACHE.write_text(json.dumps(cache))
    return cache


# --------------------------------------------------------------------------- 1. retrieval

def evaluate_retrieval(questions: list[dict]) -> list[dict]:
    vectors = query_vectors(questions)
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    results = []
    for design in pipeline.DESIGNS:
        for method in ("dense", "hybrid"):
            hits = {1: 0, 3: 0, 5: 0}
            all_hits = {1: 0, 3: 0, 5: 0}
            words = []
            multi = [q for q in answerable if q["kind"] == "multi"]
            for q in answerable:
                rows = retrieval.retrieve(q["question"], vectors[q["question"]], design, method, 5)
                pairs = expected_pairs(q)
                for k in (1, 3, 5):
                    found = [any(chunk_hits(r, p) for r in rows[:k]) for p in pairs]
                    hits[k] += any(found)
                    if q["kind"] == "multi":
                        all_hits[k] += all(found)
                words.append(sum(r["words"] for r in rows))
            n = len(answerable)
            results.append({
                "design": f"{design} + {method}",
                "chunks": pipeline.collection(design).count(),
                "hit@1": round(hits[1] / n, 3), "hit@3": round(hits[3] / n, 3), "hit@5": round(hits[5] / n, 3),
                "multi_both@5": round(all_hits[5] / max(len(multi), 1), 3),
                "words_in_prompt@5": round(statistics.mean(words)),
            })
    with (EVAL / "retrieval_results.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(results[0]))
        w.writeheader(); w.writerows(results)
    return results


# --------------------------------------------------------------------------- 2. answers

def load_answers() -> dict:
    if FRESH or not ANSWERS.exists():
        return {}
    return {a["id"]: a for a in map(json.loads, ANSWERS.read_text(encoding="utf-8").splitlines()) if a}


def run_answers(questions: list[dict]) -> dict:
    answers = load_answers()
    for a in answers.values():   # re-apply the citation guardrail to saved drafts (no API calls)
        a["answer"], a["guardrail"] = check_citations(a["draft"], set(a["retrieved"]))
        a["citations"] = sorted(set(find_citations(a["answer"])))
    for q in questions:
        if q["id"] in answers and answers[q["id"]]["question"] == q["question"]:
            continue
        print(f"  agent: {q['id']} {q['question'][:70]}", flush=True)
        for attempt in range(4):
            try:
                result = asyncio.run(run_agent(q["question"], approve=lambda _path: False))
                break
            except Exception as error:  # noqa: BLE001
                print(f"    error ({error}); retrying in 30 s", flush=True)
                time.sleep(30)
        else:
            raise RuntimeError(f"agent kept failing on {q['id']}")
        answers[q["id"]] = {"id": q["id"], **result}
        with ANSWERS.open("w", encoding="utf-8") as f:
            for qid in sorted(answers):
                f.write(json.dumps(answers[qid]) + "\n")
    return answers


# --------------------------------------------------------------------------- 3. code checks

def code_checks(q: dict, a: dict) -> dict:
    refused = REFUSAL.lower() in a["answer"].lower()
    cited = a["citations"]
    valid = all(c in a["retrieved"] for c in cited)
    sources_cited = {c.split(":")[0] for c in cited}
    expected_sources = {s for s, _ in expected_pairs(q)}
    pairs = expected_pairs(q)
    retrieved_rows = []
    for step in a["trace"]:
        if step["tool"] == "search":
            for block in step["result"].split("\n\n---\n\n"):
                head = block.split("\n", 1)[0]
                if head.startswith("["):
                    cid = head[1:head.index("]")]
                    section = head.split("Section: ", 1)[-1]
                    retrieved_rows.append({"source": cid.split(":")[0], "sections": section})
    retrieval_hit = any(chunk_hits(r, p) for r in retrieved_rows for p in pairs) if pairs else None
    return {
        "refused": int(refused),
        "has_citation": int(bool(cited)),
        "citations_valid": int(valid),
        "cites_expected_source": int(bool(sources_cited & expected_sources)) if expected_sources else None,
        "agent_retrieval_hit": None if retrieval_hit is None else int(retrieval_hit),
        "searches": sum(1 for s in a["trace"] if s["tool"] == "search"),
    }


# --------------------------------------------------------------------------- 4. judge

def load_judgments() -> dict:
    if FRESH or not JUDGMENTS.exists():
        return {}
    with JUDGMENTS.open(newline="", encoding="utf-8") as f:
        return {r["id"]: r for r in csv.DictReader(f)}


def judge(q: dict, a: dict) -> dict:
    evidence = "\n\n".join(s["result"] for s in a["trace"] if s["tool"] == "search") or "(nothing retrieved)"
    prompt = (f"{RUBRIC}\n\nQUESTION:\n{q['question']}\n\nREFERENCE ANSWER:\n{q['reference_answer']}\n\n"
              f"RETRIEVED PASSAGES:\n{evidence}\n\nASSISTANT ANSWER:\n{a['answer']}")
    models = [JUDGE_MODEL, JUDGE_MODEL] + JUDGE_FALLBACKS + [JUDGE_MODEL] + JUDGE_FALLBACKS * 2
    for attempt, model in enumerate(models):
        try:
            response = pipeline.gemini().models.generate_content(
                model=model, contents=prompt,
                config=types.GenerateContentConfig(temperature=0, response_mime_type="application/json"),
            )
            verdict = json.loads(response.text)
            return {"id": q["id"], "judge_correct": int(verdict["correct"]),
                    "judge_supported": int(verdict["supported"]), "judge_reason": verdict.get("reason", ""),
                    "judge_model": model}
        except Exception as error:  # noqa: BLE001
            print(f"    judge error ({error}); retrying", flush=True)
            time.sleep(5 + 5 * attempt)
    raise RuntimeError(f"judge kept failing on {q['id']}")


def run_judge(questions: list[dict], answers: dict) -> dict:
    verdicts = load_judgments()
    for q in questions:
        if q["id"] in verdicts:
            continue
        print(f"  judge: {q['id']}", flush=True)
        verdicts[q["id"]] = judge(q, answers[q["id"]])
        with JUDGMENTS.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["id", "judge_correct", "judge_supported", "judge_reason", "judge_model"])
            w.writeheader(); w.writerows(verdicts[i] for i in sorted(verdicts))
    return verdicts


# --------------------------------------------------------------------------- 5. human agreement

def agreement(verdicts: dict) -> dict | None:
    if not HUMAN.exists():
        return None
    with HUMAN.open(newline="", encoding="utf-8") as f:
        labels = [r for r in csv.DictReader(f) if (r.get("id") or "").strip()]
    labels = [r for r in labels if r["id"] in verdicts and r["correct"].strip() and r["supported"].strip()]
    if not labels:
        return None
    out = {"n": len(labels)}
    for col in ("correct", "supported"):
        same = sum(int(r[col]) == int(verdicts[r["id"]][f"judge_{col}"]) for r in labels)
        out[col] = round(same / len(labels), 3)
    out["disagreements"] = [r["id"] for r in labels
                            if int(r["correct"]) != int(verdicts[r["id"]]["judge_correct"])
                            or int(r["supported"]) != int(verdicts[r["id"]]["judge_supported"])]
    return out


# --------------------------------------------------------------------------- 6. outcome + failures

def outcome(q: dict, checks: dict, v: dict) -> tuple[str, str]:
    """(outcome, failure cause). Cause is '' when the answer is fine."""
    unanswerable = q["kind"] == "unanswerable"
    if unanswerable:
        return ("correct refusal", "") if checks["refused"] else ("answered unanswerable", "unsupported claim")
    if checks["refused"]:
        return "wrong refusal", ("wrong refusal" if checks["agent_retrieval_hit"] else "retrieval miss")
    if not int(v["judge_supported"]):
        return "unsupported", "unsupported claim"
    if not int(v["judge_correct"]):
        return "wrong", ("wrong answer from right passage" if checks["agent_retrieval_hit"] else "retrieval miss")
    return "correct", ""


def main() -> None:
    EVAL.mkdir(exist_ok=True)
    questions = read_questions()

    print("1/4 retrieval ...", flush=True)
    retrieval_rows = evaluate_retrieval(questions)
    for r in retrieval_rows:
        print("   ", r)

    pipeline._chroma = None   # close our handle on the index before the agent's server opens it
    import gc; gc.collect()
    print("2/4 agent answers ...", flush=True)
    answers = run_answers(questions)

    print("3/4 judge ...", flush=True)
    verdicts = run_judge(questions, answers)

    print("4/4 summary ...", flush=True)
    overrides = {}
    if OVERRIDES.exists():
        with OVERRIDES.open(newline="", encoding="utf-8") as f:
            overrides = {r["id"]: r for r in csv.DictReader(f)}
    rows = []
    for q in questions:
        a, v = answers[q["id"]], verdicts[q["id"]]
        checks = code_checks(q, a)
        result, cause = outcome(q, checks, v)
        if q["id"] in overrides and cause:          # a failure I reviewed by hand
            cause = overrides[q["id"]]["cause"]
        rows.append({"id": q["id"], "kind": q["kind"], "outcome": result, "failure_cause": cause, **checks,
                     "judge_correct": v["judge_correct"], "judge_supported": v["judge_supported"],
                     "guardrail": a.get("guardrail") or "", "tokens": a["tokens_in"] + a["tokens_out"],
                     "seconds": a["seconds"], "answer": a["answer"].replace("\n", " ")})
    with (EVAL / "results.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader(); w.writerows(rows)

    count = lambda key, val: sum(1 for r in rows if r[key] == val)  # noqa: E731
    answerable = [r for r in rows if r["kind"] != "unanswerable"]
    agree = agreement(verdicts)
    lines = [
        "# Evaluation summary", "",
        f"Questions: {len(rows)} ({len(answerable)} answerable, {len(rows) - len(answerable)} unanswerable)", "",
        "## Retrieval (answerable questions)", "",
        "| design | chunks | hit@1 | hit@3 | hit@5 | multi: both passages @5 | words in prompt @5 |",
        "|---|---|---|---|---|---|---|",
        *[f"| {r['design']} | {r['chunks']} | {r['hit@1']} | {r['hit@3']} | {r['hit@5']} | {r['multi_both@5']} | {r['words_in_prompt@5']} |"
          for r in retrieval_rows],
        "", "## End to end", "",
        "| outcome | count |", "|---|---|",
        *[f"| {o} | {count('outcome', o)} |" for o in
          ("correct", "wrong", "unsupported", "wrong refusal", "correct refusal", "answered unanswerable")],
        "", "## Code checks", "",
        f"- answers with at least one citation (answerable, not refused): "
        f"{sum(r['has_citation'] for r in answerable if not r['refused'])}/{sum(1 for r in answerable if not r['refused'])}",
        f"- all citations valid (cited id was retrieved): {sum(r['citations_valid'] for r in rows)}/{len(rows)}",
        f"- cites the expected document (answerable, not refused): "
        f"{sum(r['cites_expected_source'] or 0 for r in answerable if not r['refused'])}/{sum(1 for r in answerable if not r['refused'])}",
        f"- guardrail fired: {sum(1 for r in rows if r['guardrail'])} ({', '.join(r['id'] for r in rows if r['guardrail']) or 'none'})",
        "", "## Judge vs human", "",
        (f"- {agree['n']} answers graded by hand. Agreement: correct {agree['correct']:.0%}, supported {agree['supported']:.0%}. "
         f"Disagreements: {', '.join(agree['disagreements']) or 'none'}" if agree else
         "- eval/human_labels.csv has no grades yet."),
        "", "## Failures by cause", "",
        "| cause | count | questions |", "|---|---|---|",
        *[f"| {c} | {count('failure_cause', c)} | {', '.join(r['id'] for r in rows if r['failure_cause'] == c)} |"
          for c in ("retrieval miss", "wrong answer from right passage", "unsupported claim", "wrong refusal", "bad test question")],
        "", "## Cost per question", "",
        f"- tokens: mean {statistics.mean(r['tokens'] for r in rows):.0f}, max {max(r['tokens'] for r in rows)}",
        f"- seconds: mean {statistics.mean(r['seconds'] for r in rows):.1f}, max {max(r['seconds'] for r in rows):.1f}",
        f"- searches per question: mean {statistics.mean(r['searches'] for r in rows):.2f}",
    ]
    (EVAL / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


if __name__ == "__main__":
    main()
