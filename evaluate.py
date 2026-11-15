"""
Assignment 3: evaluation (`main.py evaluate`).

1. Retrieval: hit rate at k = 1, 3, 5 for both designs (vector, hybrid) on the
   answerable questions, and the words each design adds to the prompt.
2. End to end: the agent answers every question (answers are saved and reused,
   so a re-run spends no tokens on questions already answered).
3. Code checks: refusals, citations of passages that were not retrieved,
   whether the expected passage was retrieved and cited.
4. LLM judge with a rubric (correct, supported), shown the retrieved text.
5. Agreement between the judge and eval/human_labels.csv.

Writes to eval/:
    retrieval_results.csv   one row per question and design
    answers.jsonl           agent answers with tool traces (no verdicts)
    answers_for_grading.md  the same, readable, for grading by hand
    judge_verdicts.jsonl    the judge's verdicts
    results.csv             one row per question: code checks + verdicts
    failures.csv            the questions that failed, with a `cause` to fill in
    summary.json            all the numbers

`python evaluate.py --retrieval-only` runs step 1 alone.
"""

from __future__ import annotations

import asyncio
import csv
import json
import sys
import time
from pathlib import Path

import index
from agent import MODEL, REFUSAL, ask_many

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
KS = (1, 3, 5)
JUDGE_MODEL = "gemini-3.1-flash-lite"   # not the agent's model; free tier: 3-flash-preview allows only 20 requests/day

RUBRIC = """You are grading an assistant that answers questions about EU law (AI Act, GDPR, DSA)
for startup founders, using only passages retrieved from the official texts.

Grade two things, each 1 or 0.

correct:
- Answerable question (a reference answer is given): 1 if the answer reaches the same conclusion
  as the reference and includes all of its key points (conditions, numbers, deadlines, exceptions).
  Extra correct detail is fine. 0 if the conclusion differs, a key point is missing or wrong,
  or the assistant refused or said the corpus does not cover it.
- Unanswerable question (the reference says the corpus does not cover it): 1 if the assistant
  says the corpus does not cover it (it may mention related passages it found); 0 if it
  answers the question anyway.

supported:
- 1 if every claim the answer makes about what the law says is stated in the RETRIEVED
  PASSAGES below (paraphrase is fine), and each citation points to a passage that says it.
- 0 if any such claim is not in the passages, goes beyond them, or is cited to the wrong
  passage. Judge only against the passages, not your own knowledge of the law.
- A refusal that makes no claims about the law is supported (1). General advice such as
  "confirm with a lawyer" is not a claim about the law.

Give a one-sentence reason, naming the missing or unsupported point when you give a 0."""


# --------------------------------------------------------------------------- helpers

def read_questions() -> list[dict]:
    with (EVAL / "questions.csv").open(newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r["question"].strip()]


def expected(row: dict) -> set[str]:
    sources = [s.strip() for s in row["expected_source"].split(";")]
    locations = [l.strip() for l in row["expected_location"].split(";")]
    if len(sources) == 1 and len(locations) > 1:
        sources = sources * len(locations)
    return {f"{s}, {l}" for s, l in zip(sources, locations) if s and l}


def read_jsonl(path: Path) -> dict[str, dict]:
    if not path.is_file():
        return {}
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return {r["id"]: r for r in rows}


def write_jsonl(path: Path, rows: dict[str, dict], order: list[str]) -> None:
    path.write_text("".join(json.dumps(rows[i], ensure_ascii=False) + "\n" for i in order if i in rows),
                    encoding="utf-8")


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def pct(n: int | float, d: int) -> float:
    return round(100 * n / d, 1) if d else 0.0


# --------------------------------------------------------------------------- 1. retrieval

def evaluate_retrieval(questions: list[dict]) -> dict:
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    rows, summary = [], {}
    for mode in index.MODES:
        hits = {k: 0 for k in KS}
        all_found, words = 0, []
        for q in answerable:
            want = expected(q)
            results = index.search(q["question"], k=max(KS), mode=mode)
            got = [f"{r['source']}, {r['location']}" for r in results]
            first = next((rank for rank, g in enumerate(got, start=1) if g in want), None)
            for k in KS:
                hits[k] += first is not None and first <= k
            all_found += want <= set(got)
            words.append(sum(len(r["text"].split()) for r in results))
            rows.append({"id": q["id"], "kind": q["kind"], "mode": mode, "expected": "; ".join(sorted(want)),
                         "first_hit_rank": first or "", "top5": "; ".join(got)})
        summary[mode] = {
            **{f"hit@{k}": pct(hits[k], len(answerable)) for k in KS},
            "all_expected@5": pct(all_found, len(answerable)),
            "avg_words_added@5": round(sum(words) / len(words)),
        }
    write_csv(EVAL / "retrieval_results.csv", rows)
    print("\nRetrieval (hit rate %, answerable questions: "
          f"{len(answerable)}; multi questions count as a hit if any expected passage is found)")
    print(f"{'design':<8} " + " ".join(f"{'hit@' + str(k):>7}" for k in KS) + f" {'all@5':>7} {'words@5':>8}")
    for mode, s in summary.items():
        print(f"{mode:<8} " + " ".join(f"{s[f'hit@{k}']:>7}" for k in KS)
              + f" {s['all_expected@5']:>7} {s['avg_words_added@5']:>8}")
    print(f"(the server uses: {index.DEFAULT_MODE})")
    return summary


# --------------------------------------------------------------------------- 2. agent answers

def run_agent(questions: list[dict]) -> dict[str, dict]:
    path = EVAL / "answers.jsonl"
    answers = read_jsonl(path)
    todo = [q for q in questions if q["id"] not in answers or answers[q["id"]].get("error")
            or answers[q["id"]].get("model") != MODEL]          # re-run answers from another model
    print(f"\nAgent ({MODEL}): {len(questions) - len(todo)} answers saved, {len(todo)} to run")
    for q in todo:
        for attempt in range(3):
            try:
                result = asyncio.run(ask_many([q["question"]], approve=lambda args: False))[0]
                break
            except Exception as error:  # noqa: BLE001 - rate limits and timeouts: wait, retry, then record
                result = {"question": q["question"], "error": f"{type(error).__name__}: {str(error)[:300]}"}
                print(f"  {q['id']}: {result['error'][:120]} (attempt {attempt + 1})")
                time.sleep(30 * (attempt + 1))
        answers[q["id"]] = {"id": q["id"], "kind": q["kind"], "model": MODEL, **result}
        write_jsonl(path, answers, [x["id"] for x in questions])        # save after every question
        print(f"  {q['id']}: {result.get('seconds', '-')}s, {result.get('tokens', '-')} tokens"
              + (" [guardrail]" if result.get("guardrail") else ""))
    write_grading_sheet(questions, answers)
    return answers


def write_grading_sheet(questions: list[dict], answers: dict[str, dict]) -> None:
    """Readable answers for grading by hand. No judge verdicts in here."""
    lines = ["# Agent answers for grading\n",
             "Grade in eval/human_labels.csv (id, correct, supported, notes) before opening judge_verdicts.jsonl.\n"]
    for q in questions:
        a = answers.get(q["id"], {})
        lines += [f"## {q['id']} ({q['kind']})\n", f"**Question:** {q['question']}\n",
                  f"**Reference:** {q['reference_answer']}\n",
                  f"**Expected:** {'; '.join(sorted(expected(q))) or '(none)'}\n",
                  f"**Answer:**\n\n{a.get('answer') or a.get('error', '(missing)')}\n"]
        if a.get("guardrail"):
            lines.append(f"**Guardrail fired:** {a['guardrail']}\n\n**Withheld draft:**\n\n{a.get('draft', '')}\n")
        lines.append(f"**Retrieved:** {'; '.join(a.get('retrieved', [])) or '(nothing)'}\n")
        for step in a.get("trace", []):
            if step["tool"] == "search":
                lines.append(f"<details><summary>search: {step['args'].get('query')}</summary>\n\n"
                             f"```\n{step['result']}\n```\n</details>\n")
        lines.append("---\n")
    (EVAL / "answers_for_grading.md").write_text("\n".join(lines), encoding="utf-8")


# --------------------------------------------------------------------------- 3. code checks

def code_checks(q: dict, a: dict) -> dict:
    refused = bool(a.get("refused"))
    unanswerable = q["kind"] == "unanswerable"
    want = expected(q)
    return {
        "refused": int(refused),
        "correct_refusal": int(unanswerable and refused) if unanswerable else "",
        "wrong_refusal": int(refused) if not unanswerable else "",
        "guardrail_fired": int(bool(a.get("guardrail"))),
        "expected_retrieved": int(bool(want & set(a.get("retrieved", [])))) if want else "",
        "expected_cited": int(bool(want & set(a.get("cited", [])))) if want else "",
        "searches": sum(1 for t in a.get("trace", []) if t["tool"] == "search"),
    }


# --------------------------------------------------------------------------- 4. judge

def judge_one(q: dict, a: dict) -> dict:
    from google.genai import types

    passages = "\n\n".join(t["result"] for t in a.get("trace", []) if t["tool"] == "search") or "(none)"
    reference = q["reference_answer"] if q["kind"] != "unanswerable" else \
        f"(UNANSWERABLE: the corpus does not cover it) {q['reference_answer']}"
    prompt = (f"{RUBRIC}\n\nQUESTION:\n{q['question']}\n\nREFERENCE ANSWER:\n{reference}\n\n"
              f"ASSISTANT ANSWER:\n{a.get('answer', '')}\n\nRETRIEVED PASSAGES:\n{passages}")
    schema = {"type": "object", "properties": {
        "correct": {"type": "integer", "enum": [0, 1]},
        "supported": {"type": "integer", "enum": [0, 1]},
        "reason": {"type": "string"}}, "required": ["correct", "supported", "reason"]}
    for attempt in range(3):
        try:
            response = index.genai_client().models.generate_content(
                model=JUDGE_MODEL, contents=prompt,
                config=types.GenerateContentConfig(temperature=0, response_mime_type="application/json",
                                                   response_json_schema=schema))
            verdict = json.loads(response.text)
            usage = response.usage_metadata
            return {"id": q["id"], **verdict, "judge_tokens": usage.total_token_count if usage else 0}
        except Exception as error:  # noqa: BLE001
            print(f"  judge {q['id']}: {str(error)[:120]} (attempt {attempt + 1})")
            time.sleep(30 * (attempt + 1))
    return {"id": q["id"], "error": "judge failed"}


def run_judge(questions: list[dict], answers: dict[str, dict]) -> dict[str, dict]:
    path = EVAL / "judge_verdicts.jsonl"
    verdicts = read_jsonl(path)
    for q in questions:
        a = answers.get(q["id"], {})
        old = verdicts.get(q["id"], {})
        stale = old.get("answer") != a.get("answer")      # verdicts from an earlier judge model are kept
        if a.get("answer") and (q["id"] not in verdicts or "error" in verdicts[q["id"]] or stale):
            verdicts[q["id"]] = {**judge_one(q, a), "judge_model": JUDGE_MODEL, "answer": a["answer"]}
            write_jsonl(path, verdicts, [x["id"] for x in questions])
    return verdicts


# --------------------------------------------------------------------------- 5. agreement

def agreement(verdicts: dict[str, dict]) -> dict:
    path = EVAL / "human_labels.csv"
    with path.open(newline="", encoding="utf-8") as f:
        labels = [r for r in csv.DictReader(f) if (r.get("id") or "").strip() and r.get("correct", "").strip()]
    result = {"graded": len(labels)}
    for field in ("correct", "supported"):
        pairs = [(int(r[field]), verdicts[r["id"]][field]) for r in labels
                 if r.get(field, "").strip() and r["id"] in verdicts and field in verdicts[r["id"]]]
        if not pairs:
            continue
        agree = sum(h == j for h, j in pairs)
        po = agree / len(pairs)                       # Cohen's kappa: agreement beyond chance
        ph, pj = sum(h for h, _ in pairs) / len(pairs), sum(j for _, j in pairs) / len(pairs)
        pe = ph * pj + (1 - ph) * (1 - pj)
        result[field] = {"n": len(pairs), "agreement_%": pct(agree, len(pairs)),
                         "kappa": round((po - pe) / (1 - pe), 2) if pe < 1 else None,
                         "human_1_judge_0": sum(h == 1 and j == 0 for h, j in pairs),
                         "human_0_judge_1": sum(h == 0 and j == 1 for h, j in pairs)}
    return result


# --------------------------------------------------------------------------- main

def main() -> None:
    questions = read_questions()
    retrieval = evaluate_retrieval(questions)
    if "--retrieval-only" in sys.argv:
        return

    answers = run_agent(questions)
    verdicts = run_judge(questions, answers)

    rows, failures = [], []
    for q in questions:
        a, v = answers.get(q["id"], {}), verdicts.get(q["id"], {})
        row = {"id": q["id"], "kind": q["kind"], **code_checks(q, a),
               "judge_correct": v.get("correct", ""), "judge_supported": v.get("supported", ""),
               "judge_reason": v.get("reason", ""), "tokens": a.get("tokens", ""), "seconds": a.get("seconds", "")}
        rows.append(row)
        if row["judge_correct"] == 0 or row["judge_supported"] == 0 or a.get("error"):
            failures.append({"id": q["id"], "kind": q["kind"], "question": q["question"],
                             "expected_retrieved": row["expected_retrieved"], "refused": row["refused"],
                             "judge_correct": row["judge_correct"], "judge_supported": row["judge_supported"],
                             "judge_reason": row["judge_reason"],
                             "cause": "",   # fill in: retrieval miss | wrong answer from right passage |
                             })             # unsupported claim | wrong refusal | bad test question
    write_csv(EVAL / "results.csv", rows)
    if failures:
        old = {}
        if (EVAL / "failures.csv").is_file():                           # keep causes already filled in
            with (EVAL / "failures.csv").open(newline="", encoding="utf-8") as f:
                old = {r["id"]: r.get("cause", "") for r in csv.DictReader(f)}
        for f_ in failures:
            f_["cause"] = old.get(f_["id"], "")
        write_csv(EVAL / "failures.csv", failures)

    answered = [r for r in rows if r["judge_correct"] != ""]
    unans = [r for r in answered if r["kind"] == "unanswerable"]
    ans = [r for r in answered if r["kind"] != "unanswerable"]
    non_refusals = [r for r in answered if not r["refused"]]
    done = [a for a in answers.values() if not a.get("error")]
    end_to_end = {
        "questions": len(questions), "answered": len(done),
        "correct_%": pct(sum(r["judge_correct"] for r in answered), len(answered)),
        "correct_answerable_%": pct(sum(r["judge_correct"] for r in ans), len(ans)),
        "unsupported_answers": sum(r["judge_supported"] == 0 for r in non_refusals),
        "unsupported_%_of_non_refusals": pct(sum(r["judge_supported"] == 0 for r in non_refusals), len(non_refusals)),
        "correct_refusals": f"{sum(r['refused'] for r in unans)}/{len(unans)}",
        "wrong_refusals": f"{sum(r['refused'] for r in ans)}/{len(ans)}",
        "guardrail_fired": sum(r["guardrail_fired"] for r in answered),
        "expected_passage_retrieved_%": pct(sum(r["expected_retrieved"] == 1 for r in ans), len(ans)),
        "expected_passage_cited_%": pct(sum(r["expected_cited"] == 1 for r in ans), len(ans)),
        "avg_tokens_per_question": round(sum(a["tokens"] for a in done) / len(done)) if done else 0,
        "avg_seconds_per_question": round(sum(a["seconds"] for a in done) / len(done), 1) if done else 0,
        "avg_judge_tokens": round(sum(v.get("judge_tokens", 0) for v in verdicts.values()) / max(len(verdicts), 1)),
    }
    judges = {}
    for v in verdicts.values():
        judges[v.get("judge_model", "?")] = judges.get(v.get("judge_model", "?"), 0) + 1
    summary = {"agent_model": MODEL, "judge_models": judges, "search_mode": index.DEFAULT_MODE,
               "retrieval": retrieval, "end_to_end": end_to_end, "judge_vs_human": agreement(verdicts)}
    (EVAL / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print("\nEnd to end:")
    for key, value in end_to_end.items():
        print(f"  {key:<32} {value}")
    print("\nJudge vs your labels:", json.dumps(summary["judge_vs_human"]))
    print(f"\nFailures to classify: {len(failures)} in eval/failures.csv. Results in eval/.")


if __name__ == "__main__":
    main()
