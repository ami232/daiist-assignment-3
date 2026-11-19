"""
Assignment 3: evaluation (`main.py evaluate`).

  1. Retrieval: hit rate at k = 1, 3, 5 for each design (fixed, structured, structured + medicine filter).
  2. End to end: the agent answers every question (agent.answer_all).
  3. Code checks: refusals, citation validity, cited source = expected source.
  4. LLM judge with a rubric, the retrieved passages as evidence.
  5. Agreement between the judge and eval/human_labels.csv.
  6. Summary with rates and cost per question.

Everything slow or paid is cached in eval/ and committed, so a rerun only does
what is missing: query vectors (query_vectors.json), agent answers (answers.jsonl),
judge verdicts (verdicts.jsonl). Delete a cache file to redo that step.
"""

import csv
import json
import re
import sys
import time
from pathlib import Path

import index

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
HUMAN = EVAL / "human_labels.csv"
QUERY_VECTORS = EVAL / "query_vectors.json"
ANSWERS = EVAL / "answers.jsonl"
VERDICTS = EVAL / "verdicts.jsonl"
FOR_GRADING = EVAL / "answers_for_grading.md"
RESULTS = EVAL / "results.csv"
SUMMARY = EVAL / "summary.md"

KS = (1, 3, 5)
MEDICINES = {"eliquis": ["eliquis", "apixaban"], "xarelto": ["xarelto", "rivaroxaban"],
             "pradaxa": ["pradaxa", "dabigatran"]}
JUDGE_MODEL = "gemini-3.5-flash-lite"
PAUSE_SECONDS = 12   # between agent questions: the free chat tier allows 15 requests per minute


# ---------------------------------------------------------------- helpers

def read_questions() -> list[dict]:
    with QUESTIONS.open(encoding="utf-8") as f:
        return [{k: (v or "").strip() for k, v in row.items()} for row in csv.DictReader(f)]


def read_jsonl(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return {r["id"]: r for r in rows}


def append_jsonl(path: Path, row: dict) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def expected_pairs(q: dict) -> list[tuple[str, str]]:
    sources = [s.strip().lower() for s in q["expected_source"].split(";") if s.strip()]
    locations = [s.strip() for s in q["expected_location"].split(";") if s.strip()]
    if len(locations) == 1 and len(sources) > 1:
        locations = locations * len(sources)
    return list(zip(sources, locations))


def medicines_in(text: str) -> list[str]:
    text = text.lower()
    return [name for name, words in MEDICINES.items() if any(w in text for w in words)]


# ---------------------------------------------------------------- 1. retrieval

def query_vectors(questions: list[dict]) -> dict[str, list[float]]:
    """Embed each question once and keep the vector, so designs are compared on the same vectors."""
    cache = json.loads(QUERY_VECTORS.read_text()) if QUERY_VECTORS.exists() else {}
    for q in questions:
        if q["id"] not in cache:
            cache[q["id"]] = index.embed_query(q["question"])
            QUERY_VECTORS.write_text(json.dumps(cache))
    return cache


def retrieve(vector: list[float], design: str, question: str, k: int = max(KS)) -> list[dict]:
    collection = "fixed" if design == "fixed" else "structured"
    where = None
    if design == "structured+filter":
        found = medicines_in(question)
        if len(found) == 1:
            where = {"source": found[0]}
        elif len(found) > 1:
            where = {"source": {"$in": found}}
    result = index.collection(collection).query(query_embeddings=[vector], n_results=k, where=where,
                                                include=["metadatas"])
    return result["metadatas"][0]


def is_hit(pair: tuple[str, str], meta: dict) -> bool:
    source, location = pair
    return meta["source"] == source and location in meta["location"].split(", ")


def retrieval_eval(questions: list[dict]) -> tuple[dict, list[dict]]:
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    vectors = query_vectors(answerable)
    designs = ["fixed", "structured", "structured+filter"]
    table, per_question = {}, []
    for design in designs:
        hits = {k: 0 for k in KS}
        for q in answerable:
            top = retrieve(vectors[q["id"]], design, q["question"])
            pairs = expected_pairs(q)
            row = {"id": q["id"], "design": design}
            for k in KS:
                # a multi question is a hit only if every expected passage is in the top k
                hit = all(any(is_hit(p, m) for m in top[:k]) for p in pairs)
                hits[k] += hit
                row[f"hit@{k}"] = int(hit)
            per_question.append(row)
        table[design] = {k: hits[k] / len(answerable) for k in KS}
    return table, per_question


# ---------------------------------------------------------------- 2. agent answers

def agent_answers(questions: list[dict]) -> dict[str, dict]:
    import agent
    done = read_jsonl(ANSWERS)
    for a in done.values():
        # Re-apply the current guardrail to the saved raw answers: a guardrail fix needs no new model calls.
        final, blocked = agent.check_citations(a["raw_answer"], a["trace"])
        a.update(answer=final, guardrail=blocked or "", citations=sorted(agent.labels_in(final)))
    todo = [q for q in questions if q["id"] not in done]
    for i, q in enumerate(todo):
        print(f"  agent {q['id']} ({i + 1}/{len(todo)}) ...", flush=True)
        try:
            result = agent.answer(q["question"])
        except Exception as error:          # keep going; the error is recorded and retried next run
            print(f"    failed: {str(error)[:200]}", file=sys.stderr)
            continue
        result["id"] = q["id"]
        append_jsonl(ANSWERS, result)
        done[q["id"]] = result
        if i < len(todo) - 1:
            time.sleep(PAUSE_SECONDS)
    return done


def write_grading_sheet(questions: list[dict], answers: dict[str, dict]) -> None:
    """A readable sheet for your own grading, with the evidence and WITHOUT the judge's verdicts."""
    parts = ["# Answers to grade by hand\n\nGrade these in eval/human_labels.csv before opening verdicts.jsonl.\n"]
    for q in questions:
        a = answers.get(q["id"])
        if not a:
            continue
        evidence = "\n\n".join(s["output"] for s in a["trace"] if s["tool"] == "search") or "(no search)"
        parts.append(f"\n---\n\n## {q['id']} ({q['kind']})\n\n**Question:** {q['question']}\n\n"
                     f"**Reference:** {q['reference_answer']}\n\n**Agent answer:** {a['answer']}\n\n"
                     f"<details><summary>Retrieved passages</summary>\n\n```\n{evidence}\n```\n</details>\n")
    FOR_GRADING.write_text("".join(parts), encoding="utf-8")


# ---------------------------------------------------------------- 3. code checks

def code_checks(q: dict, a: dict) -> dict:
    import agent
    refused = agent.is_refusal(a["answer"])
    cited_sources = {label.split(" ")[0] for label in a["citations"]}
    expected_sources = {s for s, _ in expected_pairs(q)}
    return {
        "refused": int(refused),
        "refusal_ok": int(refused == (q["kind"] == "unanswerable")),
        "citations_valid": int(not a["guardrail"].startswith("blocked: cited")),
        "cites_expected_source": int(bool(expected_sources) and expected_sources <= cited_sources),
        "guardrail_blocked": int(bool(a["guardrail"])),
    }


# ---------------------------------------------------------------- 4. LLM judge

RUBRIC = """You grade one answer of a pharmacy assistant's RAG system about anticoagulants.
You get the question, the reference answer written by a pharmacist student, the system's answer,
and the passages the system retrieved. Grade two things, each 1 or 0.

correct:
- Answerable question: 1 if the key fact a patient needs is right and nothing in the answer is wrong.
  Missing secondary details from the reference is still 1. A wrong number, a wrong medicine,
  or a refusal is 0.
- Unanswerable question (the reference says the documents do not cover it): 1 only if the system
  refuses AND adds no content of its own. A refusal that also gives advice or facts is 0.
  The system's standard refusal ("...does not cover this; please ask the pharmacist or doctor"),
  "Confirm with the pharmacist or doctor", and saying which medicines are not covered are part
  of a proper refusal, not added content.

supported:
- 1 if every factual claim in the answer appears in the retrieved passages. 0 if any claim is not
  in them (from memory, invented, or about a different medicine). A pure refusal is 1.

Notes: one sentence on why, for every 0. Also note (without failing it) when an answer about a
specific patient does not end by telling them to confirm with the pharmacist or doctor.

Reply only with JSON: {"correct": 0 or 1, "supported": 0 or 1, "notes": "..."}"""


def judge(q: dict, a: dict) -> dict:
    from google.genai import types
    evidence = "\n\n".join(s["output"] for s in a["trace"] if s["tool"] == "search") or "(nothing retrieved)"
    prompt = (f"{RUBRIC}\n\nQUESTION ({q['kind']}): {q['question']}\n\nREFERENCE: {q['reference_answer']}\n\n"
              f"ANSWER: {a['answer']}\n\nRETRIEVED PASSAGES:\n{evidence}")
    for attempt in range(4):
        try:
            response = index.gemini().models.generate_content(
                model=JUDGE_MODEL, contents=prompt,
                config=types.GenerateContentConfig(temperature=0, response_mime_type="application/json"))
            verdict = json.loads(response.text)
            usage = response.usage_metadata
            return {"correct": int(verdict["correct"]), "supported": int(verdict["supported"]),
                    "notes": verdict.get("notes", ""),
                    "judge_tokens": (usage.prompt_token_count or 0) + (usage.candidates_token_count or 0)}
        except Exception as error:
            if attempt == 3:
                raise
            print(f"    judge retry ({error.__class__.__name__}) ...", file=sys.stderr)
            time.sleep(30)


def judge_all(questions: list[dict], answers: dict[str, dict]) -> dict[str, dict]:
    done = read_jsonl(VERDICTS)
    for q in questions:
        if q["id"] in answers and q["id"] not in done:
            print(f"  judge {q['id']} ...", flush=True)
            verdict = {"id": q["id"], **judge(q, answers[q["id"]])}
            append_jsonl(VERDICTS, verdict)
            done[q["id"]] = verdict
            time.sleep(5)
    return done


# ---------------------------------------------------------------- 5. agreement with your grades

def agreement(verdicts: dict[str, dict]) -> dict:
    if not HUMAN.exists():
        return {}
    with HUMAN.open(encoding="utf-8") as f:
        human = [r for r in csv.DictReader(f) if (r.get("correct") or "").strip() in {"0", "1"}]
    pairs = [(h, verdicts[h["id"].strip()]) for h in human if h["id"].strip() in verdicts]
    if not pairs:
        return {}
    out = {"graded": len(pairs)}
    for field in ("correct", "supported"):
        same = sum(int(h[field].strip()) == v[field] for h, v in pairs if (h.get(field) or "").strip() in {"0", "1"})
        out[field] = same / len(pairs)
    out["disagreements"] = [h["id"] for h, v in pairs
                            if int(h["correct"]) != v["correct"] or int(h["supported"]) != v["supported"]]
    return out


# ---------------------------------------------------------------- 6. summary

def pct(x: float) -> str:
    return f"{100 * x:.0f}%"


def main() -> None:
    questions = read_questions()
    print("1/4 Retrieval ...")
    table, per_question = retrieval_eval(questions)

    print("2/4 Agent answers ...")
    answers = agent_answers(questions)
    write_grading_sheet(questions, answers)

    print("3/4 Judge ...")
    verdicts = judge_all(questions, answers)

    print("4/4 Summary ...")
    rows = []
    for q in questions:
        a, v = answers.get(q["id"]), verdicts.get(q["id"], {})
        if not a:
            continue
        rows.append({"id": q["id"], "kind": q["kind"], **code_checks(q, a),
                     "judge_correct": v.get("correct", ""), "judge_supported": v.get("supported", ""),
                     "judge_notes": v.get("notes", ""), "guardrail": a["guardrail"],
                     "tool_calls": len(a["trace"]), "model_calls": a["model_calls"],
                     "tokens": a["input_tokens"] + a["output_tokens"], "seconds": a["seconds"],
                     "failure_type": ""})
    with RESULTS.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    unans = [r for r in rows if r["kind"] == "unanswerable"]
    ans = [r for r in rows if r["kind"] != "unanswerable"]
    judged = [r for r in rows if r["judge_correct"] != ""]
    agree = agreement(verdicts)
    n = len(rows)
    lines = ["# Evaluation summary\n",
             "## Retrieval (answerable questions; a multi question needs every expected passage)\n",
             "| design | hit@1 | hit@3 | hit@5 |", "|---|---|---|---|"]
    lines += [f"| {d} | " + " | ".join(pct(t[k]) for k in KS) + " |" for d, t in table.items()]
    lines += ["", f"## End to end ({n} questions answered)\n",
              f"- Correct (judge): {pct(sum(r['judge_correct'] for r in judged) / max(len(judged), 1))}",
              f"- Supported by retrieved text (judge): {pct(sum(r['judge_supported'] for r in judged) / max(len(judged), 1))}",
              f"- Rightly refused (unanswerable questions refused): {sum(r['refused'] for r in unans)}/{len(unans)}",
              f"- Made things up (unanswerable but answered): {sum(1 - r['refused'] for r in unans)}/{len(unans)}",
              f"- Wrongly refused (answerable but refused): {sum(r['refused'] for r in ans)}/{len(ans)}",
              f"- Cited the expected document (answerable, not refused): "
              f"{sum(r['cites_expected_source'] for r in ans if not r['refused'])}/{sum(1 for r in ans if not r['refused'])}",
              f"- Guardrail blocked an answer: {sum(r['guardrail_blocked'] for r in rows)}/{n}",
              "", "## Cost per question\n",
              f"- Agent tokens: {sum(r['tokens'] for r in rows) / n:.0f} on average",
              f"- Agent time: {sum(r['seconds'] for r in rows) / n:.1f} s on average",
              f"- Model calls: {sum(r['model_calls'] for r in rows) / n:.1f}, tool calls: {sum(r['tool_calls'] for r in rows) / n:.1f} on average",
              f"- Judge tokens: {sum(v.get('judge_tokens', 0) for v in verdicts.values()) / max(len(verdicts), 1):.0f} on average"]
    if agree:
        lines += ["", f"## Judge vs your grades ({agree['graded']} answers)\n",
                  f"- Agreement on correct: {pct(agree['correct'])}",
                  f"- Agreement on supported: {pct(agree['supported'])}",
                  f"- Disagreements: {', '.join(agree['disagreements']) or 'none'}"]
    SUMMARY.write_text("\n".join(lines) + "\n", encoding="utf-8")
    with (EVAL / "retrieval_per_question.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(per_question[0]))
        writer.writeheader()
        writer.writerows(per_question)
    print("\n" + SUMMARY.read_text(encoding="utf-8"))


if __name__ == "__main__":
    main()
