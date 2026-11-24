"""
Assignment 3: evaluation (`main.py evaluate`).

1. Retrieval: hit rate at k = 1, 3, 5 for every design (fixed / structure chunks) and
   method (vector / hybrid), plus how many words each adds to the prompt.
2. The agent answers every question in eval/questions.csv (through server.py over MCP).
3. Code checks what code can check: citations present and valid, refusals.
4. An LLM judge (a different Gemini model) grades correctness and support with a rubric,
   given the passages the agent actually retrieved as evidence.
5. Agreement between the judge and eval/human_labels.csv.
6. Results, failure causes, and cost per question (tokens, seconds).

Every Gemini result is cached in eval/ (answers.jsonl, judge.jsonl) and index/ (query
vectors), so running it again only spends quota on what is missing: if the daily quota
runs out, run it again after it resets and it carries on.
"""

from __future__ import annotations

import asyncio
import csv
import json
import re
import sys
import time
from collections import Counter
from statistics import mean

import config
import index
import retrieval

EVAL = config.EVAL_DIR
QUESTIONS = EVAL / "questions.csv"
ANSWERS = EVAL / "answers.jsonl"
JUDGE = EVAL / "judge.jsonl"
HUMAN = EVAL / "human_labels.csv"
FAILURE_REVIEW = EVAL / "failures_review.csv"   # optional: id,cause,note to correct the automatic cause
KS = (1, 3, 5)
CAUSES = ["retrieval miss", "wrong answer from the right passage", "unsupported claim", "wrong refusal", "bad test question"]


def load_questions() -> list[dict]:
    with QUESTIONS.open(encoding="utf-8", newline="") as f:
        rows = [r for r in csv.DictReader(f) if r["question"].strip()]
    for r in rows:
        r["kind"] = r["kind"].strip().lower()
        r["expected"] = list(zip(r["expected_source"].split(";"), r["expected_location"].split(";"))) \
            if r["expected_source"].strip() else []
    return rows


def read_jsonl(path) -> dict:
    if not path.exists():
        return {}
    return {d["id"]: d for d in (json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip())}


def append_jsonl(path, record: dict) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def write_csv(path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


# ----------------------------------------------------------------------------------
# 1. Retrieval
# ----------------------------------------------------------------------------------


def evaluate_retrieval(questions: list[dict]) -> list[dict]:
    answerable = [q for q in questions if q["expected"]]
    cache = index.load_query_cache()
    vectors = {q["id"]: index.embed_query(q["question"], cache) for q in answerable}
    per_question, summary = [], []
    for design in config.DESIGNS:
        for method in ("vector", "hybrid"):
            r = retrieval.Retriever(design, method, sources=[d["id"] for d in config.DOCUMENTS])
            rows = []
            for q in answerable:
                hits = r.search(q["question"], vectors[q["id"]], max(KS))
                row = {"design": design, "method": method, "id": q["id"], "kind": q["kind"]}
                for k in KS:
                    top = hits[:k]
                    found = [any(retrieval.hit_matches(h, s, l) for h in top) for s, l in q["expected"]]
                    row[f"hit@{k}"] = int(all(found))         # multi: both passages must be in the top k
                    row[f"any@{k}"] = int(any(found))
                    row[f"words@{k}"] = sum(h["words"] for h in top)
                row["top5"] = " | ".join(retrieval.citation(h) for h in hits)
                rows.append(row)
            per_question += rows
            line = {"design": design, "method": method, "chunks": len(r.ids)}
            for k in KS:
                line[f"hit@{k}"] = round(mean(x[f"hit@{k}"] for x in rows), 3)
            for k in KS:
                line[f"single hit@{k}"] = round(mean(x[f"hit@{k}"] for x in rows if x["kind"] == "single"), 3)
            line["multi both@5"] = round(mean(x["hit@5"] for x in rows if x["kind"] == "multi"), 3)
            line["multi any@5"] = round(mean(x["any@5"] for x in rows if x["kind"] == "multi"), 3)
            for k in KS:
                line[f"words added @{k}"] = round(mean(x[f"words@{k}"] for x in rows))
            summary.append(line)
    write_csv(EVAL / "retrieval_per_question.csv", per_question)
    write_csv(EVAL / "retrieval_summary.csv", summary)
    plot_retrieval(summary)
    return summary


def plot_retrieval(summary: list[dict]) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    fig, ax = plt.subplots(figsize=(7, 4))
    for line in summary:
        ax.plot(KS, [line[f"hit@{k}"] for k in KS], marker="o", label=f"{line['design']} / {line['method']}")
    ax.set_xticks(KS)
    ax.set_xlabel("k (chunks returned)")
    ax.set_ylabel("hit rate (answerable questions)")
    ax.set_ylim(0, 1.02)
    ax.grid(alpha=0.3)
    ax.legend()
    ax.set_title("Retrieval hit rate by design")
    fig.tight_layout()
    fig.savefig(EVAL / "retrieval_hit_rate.png", dpi=150)
    plt.close(fig)


# ----------------------------------------------------------------------------------
# 2. Agent answers
# ----------------------------------------------------------------------------------


def daily_quota_error(error: Exception) -> bool:
    text = str(error)
    return isinstance(error, index.QuotaExhausted) or ("RESOURCE_EXHAUSTED" in text and "PerDay" in text)


async def run_agent(questions: list[dict]) -> dict:
    from agent import Agent

    done = read_jsonl(ANSWERS)
    todo = [q for q in questions if q["id"] not in done or done[q["id"]]["question"] != q["question"]]
    if todo:
        print(f"Agent: {len(todo)} questions to answer ({len(done)} cached)")
        async with Agent() as agent:   # no terminal approver: add_document is always rejected here
            for q in todo:
                try:
                    out = await agent.ask(q["question"])
                except Exception as error:  # noqa: BLE001
                    if daily_quota_error(error):
                        print("Daily quota reached; answers so far are saved. Run evaluate again after the reset.")
                        break
                    print(f"  {q['id']} failed: {type(error).__name__}: {str(error)[:200]}")
                    continue
                out["id"] = q["id"]
                append_jsonl(ANSWERS, out)
                done[q["id"]] = out
                print(f"  {q['id']} answered in {out['seconds']}s ({out['searches']} searches)")
    return done


# ----------------------------------------------------------------------------------
# 3. Code checks
# ----------------------------------------------------------------------------------


def code_checks(q: dict, a: dict) -> dict:
    retrieved = [tuple(x) for x in a["retrieved"]]
    cited = [tuple(x) for x in a["citations"]]
    expected = q["expected"]
    should_refuse = q["kind"] == "unanswerable"

    def covered(pairs, s, l):
        return any(src == s and retrieval.location_matches(loc, l) for src, loc in pairs)

    return {
        "refused": int(a["refused"]),
        "should_refuse": int(should_refuse),
        "refusal_ok": int(a["refused"] == should_refuse),
        "has_citation": int(bool(cited)),
        "citations_valid": int(all(c in retrieved for c in cited)),
        "retrieved_expected": int(all(covered(retrieved, s, l) for s, l in expected)) if expected else None,
        "cited_expected": int(all(covered(cited, s, l) for s, l in expected)) if expected else None,
        "guardrail_fired": int(bool(a.get("guardrail"))),
    }


# ----------------------------------------------------------------------------------
# 4. LLM judge
# ----------------------------------------------------------------------------------

RUBRIC = """You grade answers from a question-answering assistant about EU and Spanish wine rules.
The assistant must answer only from the retrieved passages, cite them, and reply
"El corpus no cubre esta pregunta." when the passages do not contain the answer.

Grade two things, each 1 or 0:

correct = 1 if the answer agrees with the REFERENCE ANSWER on every key fact the question
asks for (numbers, conditions, yes/no). Extra true detail is fine. Missing a key fact,
a wrong number, or a wrong condition (e.g. "blancos" for "tintos") is 0. For an
UNANSWERABLE question, correct = 1 only if the assistant declines (says the corpus does
not cover it) and does not give a substantive answer from elsewhere. For an answerable
question, a refusal is correct = 0.

supported = 1 if every factual claim in the answer is stated in the RETRIEVED PASSAGES
below (paraphrase is fine; a claim that is only in the reference answer or in general
knowledge is not supported). A pure refusal is supported = 1. Judge support only against
the passages, not against what you know.

Return JSON: {"correct": 0 or 1, "supported": 0 or 1, "reason": "one or two sentences"}"""


def judge_prompt(q: dict, a: dict) -> str:
    passages = "\n\n".join(t["output"] for t in a["trace"] if t["tool"] == "search") or "(the assistant did not search)"
    return (f"{RUBRIC}\n\nQUESTION KIND: {q['kind']}\nQUESTION: {q['question']}\n"
            f"REFERENCE ANSWER: {q['reference_answer']}\n\nRETRIEVED PASSAGES:\n{passages[:24000]}\n\n"
            f"ASSISTANT ANSWER:\n{a['answer']}")


_judge_pacer = index.Pacer(tokens_per_min=200_000, requests_per_min=config.CHAT_REQUESTS_PER_MIN)


def call_judge(prompt: str) -> dict:
    """One verdict. The reply is forced into a JSON schema so it always parses. If the judge
    model is overloaded (503), the next model in config.JUDGE_FALLBACKS is tried."""
    from google.genai import errors, types

    schema = types.Schema(
        type=types.Type.OBJECT,
        properties={
            "correct": types.Schema(type=types.Type.INTEGER),
            "supported": types.Schema(type=types.Type.INTEGER),
            "reason": types.Schema(type=types.Type.STRING),
        },
        required=["correct", "supported", "reason"],
    )
    models = [config.JUDGE_MODEL] + config.JUDGE_FALLBACKS
    last_error = ""
    for round_no in range(3):
        for model in models:
            for attempt in range(2):
                _judge_pacer.wait(len(prompt) // 4)
                try:
                    response = index.genai_client().models.generate_content(
                        model=model, contents=prompt,
                        config=types.GenerateContentConfig(response_mime_type="application/json",
                                                           response_schema=schema),
                    )
                    text = (response.text or "").strip()
                    match = re.search(r"\{.*\}", text, re.S)
                    if not match:
                        raise ValueError(f"no JSON in reply: {text[:200]!r}")
                    data = json.loads(match.group(0))
                    return {"correct": int(data["correct"]), "supported": int(data["supported"]),
                            "reason": str(data.get("reason", "")), "judge_model": model,
                            "tokens": getattr(response.usage_metadata, "total_token_count", None)}
                except errors.ClientError as error:
                    last_error = f"{model} {error.code}: {str(error)[:200]}"
                    if error.code == 429 and "PerDay" not in str(error):
                        time.sleep(30)
                        continue
                    print(f"    {last_error}; trying the next model", flush=True)
                    break   # daily quota or a request error on this model: next model
                except errors.ServerError as error:
                    last_error = f"{model} {error.code}: overloaded"
                    print(f"    {last_error}", flush=True)
                    if error.code == 503:
                        break   # overloaded: do not wait, try the next model
                    time.sleep(10)
                except (json.JSONDecodeError, AttributeError, KeyError, ValueError, TypeError) as error:
                    last_error = f"{model} {type(error).__name__}: {str(error)[:200]}"
                    print(f"    {last_error}; retrying", flush=True)
        time.sleep(60 * (round_no + 1))
    raise RuntimeError(f"judge failed on every model; last error: {last_error}")


def run_judge(questions: list[dict], answers: dict) -> dict:
    verdicts = read_jsonl(JUDGE)
    for q in questions:
        a = answers.get(q["id"])
        if not a:
            continue
        key = f"{a['answer']}"
        if q["id"] in verdicts and verdicts[q["id"]].get("answer") == key:
            continue
        try:
            v = call_judge(judge_prompt(q, a))
        except index.QuotaExhausted:
            print("Daily quota reached for the judge; verdicts so far are saved.")
            break
        except Exception as error:  # noqa: BLE001 - skip this one, keep the rest; a rerun retries it
            print(f"  {q['id']} not judged: {error}")
            continue
        v.update({"id": q["id"], "answer": key})
        append_jsonl(JUDGE, v)
        verdicts[q["id"]] = v
        print(f"  judged {q['id']}: correct={v['correct']} supported={v['supported']}")
    return verdicts


# ----------------------------------------------------------------------------------
# 5. Agreement with human labels
# ----------------------------------------------------------------------------------


def cohen_kappa(a: list[int], b: list[int]) -> float | None:
    n = len(a)
    if n == 0:
        return None
    po = sum(x == y for x, y in zip(a, b)) / n
    pa, pb = sum(a) / n, sum(b) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return round((po - pe) / (1 - pe), 3) if pe < 1 else None


def agreement(verdicts: dict) -> dict:
    if not HUMAN.exists():
        return {}
    with HUMAN.open(encoding="utf-8", newline="") as f:
        human = {r["id"].strip(): r for r in csv.DictReader(f) if (r.get("id") or "").strip()}
    rows, out = [], {"n": 0}
    for qid, h in human.items():
        v = verdicts.get(qid)
        if not v or h.get("correct", "").strip() == "":
            continue
        rows.append({"id": qid, "human_correct": int(h["correct"]), "judge_correct": v["correct"],
                     "human_supported": int(h["supported"]), "judge_supported": v["supported"],
                     "human_notes": h.get("notes", ""), "judge_reason": v["reason"]})
    if not rows:
        return out
    write_csv(EVAL / "agreement.csv", rows)
    for field in ("correct", "supported"):
        hs, js = [r[f"human_{field}"] for r in rows], [r[f"judge_{field}"] for r in rows]
        out[f"{field} agreement"] = round(sum(x == y for x, y in zip(hs, js)) / len(rows), 3)
        out[f"{field} kappa"] = cohen_kappa(hs, js)
    out["both agree"] = round(mean(r["human_correct"] == r["judge_correct"] and
                                   r["human_supported"] == r["judge_supported"] for r in rows), 3)
    out["n"] = len(rows)
    out["disagreements"] = [r["id"] for r in rows if r["human_correct"] != r["judge_correct"]
                            or r["human_supported"] != r["judge_supported"]]
    return out


# ----------------------------------------------------------------------------------
# 6. Results and failures
# ----------------------------------------------------------------------------------


def classify(q: dict, checks: dict, verdict: dict) -> str | None:
    """First-pass failure cause, from the code checks and the judge. None if not a failure."""
    if q["kind"] == "unanswerable":
        return None if checks["refused"] else "unsupported claim"
    if verdict["correct"] and verdict["supported"]:
        return None
    if checks["refused"]:
        return "wrong refusal" if checks["retrieved_expected"] else "retrieval miss"
    if not checks["retrieved_expected"]:
        return "retrieval miss"
    if not verdict["supported"]:
        return "unsupported claim"
    return "wrong answer from the right passage"


def results(questions: list[dict], answers: dict, verdicts: dict, retrieval_summary: list[dict]) -> dict:
    review = {}
    if FAILURE_REVIEW.exists():
        with FAILURE_REVIEW.open(encoding="utf-8", newline="") as f:
            review = {r["id"]: r for r in csv.DictReader(f)}
    rows, failures = [], []
    for q in questions:
        a, v = answers.get(q["id"]), verdicts.get(q["id"])
        if not a or not v:
            continue
        c = code_checks(q, a)
        row = {"id": q["id"], "kind": q["kind"], "question": q["question"], "reference_answer": q["reference_answer"],
               "answer": a["answer"], "citations": "; ".join(f"[{s}, {l}]" for s, l in a["citations"]),
               **c, "judge_correct": v["correct"], "judge_supported": v["supported"], "judge_reason": v["reason"],
               "judge_model": v.get("judge_model", v.get("model", config.JUDGE_MODEL)),
               "searches": a["searches"], "model_calls": a["model_calls"],
               "input_tokens": a["tokens"]["input_tokens"], "output_tokens": a["tokens"]["output_tokens"],
               "total_tokens": a["tokens"]["total_tokens"], "seconds": a["seconds"]}
        rows.append(row)
        cause = classify(q, c, v)
        if cause:
            reviewed = review.get(q["id"], {})
            failures.append({"id": q["id"], "kind": q["kind"], "question": q["question"],
                             "auto_cause": cause, "cause": reviewed.get("cause") or cause,
                             "note": reviewed.get("note", ""), "answer": a["answer"], "judge_reason": v["reason"]})
    write_csv(EVAL / "results.csv", rows)
    write_csv(EVAL / "failures.csv", failures)

    answerable = [r for r in rows if r["kind"] != "unanswerable"]
    unanswerable = [r for r in rows if r["kind"] == "unanswerable"]
    summary = {
        "models": {"embedding": config.EMBED_MODEL, "agent": config.AGENT_MODEL, "judge": config.JUDGE_MODEL,
                   "verdicts by judge model": dict(Counter(r["judge_model"] for r in rows))},
        "retrieval_design": f"{config.CHOSEN_DESIGN} / {config.CHOSEN_METHOD}, k={config.TOP_K}",
        "questions_answered": len(rows),
        "answerable": len(answerable),
        "correct (judge)": sum(r["judge_correct"] for r in answerable),
        "unsupported answers (judge, non-refusals)": sum(1 - r["judge_supported"] for r in rows if not r["refused"]),
        "correct refusals": sum(r["refused"] for r in unanswerable),
        "unanswerable answered anyway": sum(1 - r["refused"] for r in unanswerable),
        "wrong refusals": sum(r["refused"] for r in answerable),
        "answers with invalid citations (code)": sum(1 - r["citations_valid"] for r in rows),
        "answerable answers without citation (code)": sum(1 - r["has_citation"] for r in answerable if not r["refused"]),
        "guardrail fired": sum(r["guardrail_fired"] for r in rows),
        "by kind": {k: {"n": sum(1 for r in rows if r["kind"] == k),
                        "correct": sum(r["judge_correct"] for r in rows if r["kind"] == k)}
                    for k in ("single", "multi", "unanswerable")},
        "failures by cause": dict(Counter(f["cause"] for f in failures)),
        "cost per question": {
            "mean total tokens": round(mean(r["total_tokens"] for r in rows)) if rows else None,
            "mean input tokens": round(mean(r["input_tokens"] for r in rows)) if rows else None,
            "mean output tokens": round(mean(r["output_tokens"] for r in rows)) if rows else None,
            "mean seconds": round(mean(r["seconds"] for r in rows), 1) if rows else None,
            "max seconds": max((r["seconds"] for r in rows), default=None),
            "mean model calls": round(mean(r["model_calls"] for r in rows), 2) if rows else None,
            "mean searches": round(mean(r["searches"] for r in rows), 2) if rows else None,
        },
        "judge agreement with human labels": agreement(verdicts),
        "retrieval": retrieval_summary,
    }
    (EVAL / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    write_grading_sheet(questions, answers)
    return summary


def write_grading_sheet(questions: list[dict], answers: dict) -> None:
    """eval/answers_for_grading.md: question, reference, answer and the passages the agent saw,
    to grade by hand into human_labels.csv without looking at the judge."""
    out = ["# Answers to grade by hand\n",
           "Grade into eval/human_labels.csv (id, correct, supported, notes) BEFORE opening judge.jsonl or results.csv.\n"]
    for q in questions:
        a = answers.get(q["id"])
        if not a:
            continue
        out.append(f"\n---\n\n## {q['id']} ({q['kind']})\n\n**Question:** {q['question']}\n\n"
                   f"**Reference:** {q['reference_answer']}\n\n**Agent answer:**\n\n{a['answer']}\n")
        for t in a["trace"]:
            if t["tool"] == "search":
                out.append(f"\n<details><summary>search: {t['args'].get('query', '')}</summary>\n\n{t['output']}\n\n</details>\n")
    (EVAL / "answers_for_grading.md").write_text("".join(out), encoding="utf-8")


def print_summary(s: dict) -> None:
    print("\nRetrieval (answerable questions):")
    for line in s["retrieval"]:
        print(f"  {line['design']:<10} {line['method']:<7} hit@1 {line['hit@1']:.2f}  hit@3 {line['hit@3']:.2f}  "
              f"hit@5 {line['hit@5']:.2f}  words@5 {line['words added @5']}")
    keys = ["questions_answered", "correct (judge)", "unsupported answers (judge, non-refusals)", "correct refusals",
            "unanswerable answered anyway", "wrong refusals", "answers with invalid citations (code)", "guardrail fired"]
    print("\nEnd to end:")
    for k in keys:
        print(f"  {k}: {s[k]}")
    print(f"  failures by cause: {s['failures by cause']}")
    print(f"  cost per question: {s['cost per question']}")
    print(f"  judge vs human: {s['judge agreement with human labels'] or 'no human labels yet'}")


def main() -> None:
    """`main.py evaluate` runs every stage. `python evaluate.py --answers-only` stops before the
    judge, so the answers can be graded by hand (eval/answers_for_grading.md) without seeing
    any verdict first."""
    questions = load_questions()
    print("1/4 Retrieval hit rate per design")
    try:
        retrieval_summary = evaluate_retrieval(questions)
    except index.QuotaExhausted:
        sys.exit("Daily embedding quota reached; query vectors so far are cached. Run again after the reset.")
    print("2/4 Agent answers")
    answers = asyncio.run(run_agent(questions))
    if "--answers-only" in sys.argv:
        write_grading_sheet(questions, answers)
        print(f"\n{len(answers)} answers saved. Grade them from eval/answers_for_grading.md into "
              f"eval/human_labels.csv, then run `main.py evaluate` for the judge and the agreement.")
        return
    print("3/4 Judge")
    verdicts = run_judge(questions, answers)
    print("4/4 Results")
    summary = results(questions, answers, verdicts, retrieval_summary)
    print_summary(summary)
    missing = [q["id"] for q in questions if q["id"] not in answers or q["id"] not in verdicts]
    if missing:
        print(f"\nNot finished yet: {len(missing)} questions without an answer or verdict ({', '.join(missing)}). "
              f"Run `main.py evaluate` again; cached results are reused.")


if __name__ == "__main__":
    main()
