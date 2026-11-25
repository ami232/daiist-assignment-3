"""
Assignment 3: evaluation (`uv run python main.py evaluate`).

1. Retrieval: hit rate at k = 1, 3, 5 for three designs, and the words each adds to the
   prompt. The best design by the numbers is written to index/config.json for the server.
2. End to end: the agent answers every question (the add-document tool is never approved
   and documents added later are hidden, so the test always measures the same corpus).
3. Code checks: refusals, and whether every citation points to a passage search returned.
4. LLM judge with a rubric, given the retrieved passages as evidence.
5. Agreement with my own grades in eval/human_labels.csv.
6. Failures by cause, cost and latency per question.

Every agent answer and judge verdict is saved as soon as it arrives (eval/*.jsonl), so a
crash or the daily limit loses nothing: run it again and it continues. Delete those files
to start over.
"""

import asyncio
import csv
import json
import time
from pathlib import Path

import pandas as pd
from pydantic import BaseModel, Field

import agent
import rag

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
DESIGNS = [("fixed", "vector"), ("sections", "vector"), ("sections", "hybrid")]
KS = [1, 3, 5]
ANSWERS = EVAL / "answers.jsonl"
VERDICTS = EVAL / "judge.jsonl"

RUBRIC = """You grade answers of a web-security assistant against a reference answer.

correct = 1 if the answer gives the key facts of the reference answer (values, settings, the
yes/no conclusion) and nothing that contradicts it. Extra details are fine if they are true.
A two-part question with one part missing or wrong is 0. Wording does not matter.

supported = 1 if every factual claim in the answer can be found in the retrieved passages
(paraphrase is fine). Any claim, number or setting that is not in the passages makes it 0,
even if it is true in general.

Give a one-sentence reason. Be strict: when unsure, give 0."""


class Verdict(BaseModel):
    correct: int = Field(description="1 or 0, per the rubric")
    supported: int = Field(description="1 or 0, per the rubric")
    reason: str = Field(description="one sentence")


def load_questions() -> list[dict]:
    with (EVAL / "questions.csv").open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r["question"].strip()]
    for r in rows:
        r["kind"] = r["kind"].strip().lower()
        r["expected"] = list(zip(r["expected_source"].split(";"), r["expected_location"].split(";"))) \
            if r["expected_source"].strip() else []
    return rows


def is_expected(chunk: dict, source: str, location: str) -> bool:
    return chunk["source"] == source.strip() and any(location.strip().lower() in p.lower() for p in chunk["sections"])


def found(chunks: list[dict], expected: list[tuple[str, str]]) -> list[bool]:
    return [any(is_expected(c, s, loc) for c in chunks) for s, loc in expected]


# ---------------------------------------------------------------- 1. retrieval
def evaluate_retrieval(questions: list[dict]) -> pd.DataFrame:
    rows = []
    answerable = [q for q in questions if q["expected"]]
    for design, method in DESIGNS:
        index = rag.Index(design, include_added=False)
        for q in answerable:
            hits = index.search(q["question"], k=max(KS), method=method)
            row = {"design": f"{design}+{method}", "id": q["id"], "kind": q["kind"],
                   "words_top5": sum(c["words"] for c in hits)}
            for k in KS:
                passages = found(hits[:k], q["expected"])
                row[f"hit@{k}"] = int(any(passages))          # at least one expected passage
                row[f"all@{k}"] = int(all(passages))          # every expected passage (multi)
            rows.append(row)
    detail = pd.DataFrame(rows)
    detail.to_csv(EVAL / "retrieval.csv", index=False)
    summary = detail.groupby("design", sort=False).agg(
        **{f"hit@{k}": (f"hit@{k}", "mean") for k in KS},
        **{"multi_all@5": ("all@5", lambda s: s[detail.loc[s.index, "kind"] == "multi"].mean())},
        words_added_k5=("words_top5", "mean")).round(3).reset_index()
    summary.to_csv(EVAL / "retrieval_summary.csv", index=False)
    return summary


def choose_design(summary: pd.DataFrame) -> dict:
    # best hit@5 (the agent sees 5 passages), then hit@3, then hit@1, then fewer words in the prompt
    best = summary.sort_values(["hit@5", "hit@3", "hit@1", "words_added_k5"],
                               ascending=[False, False, False, True]).iloc[0]
    design, method = best["design"].split("+")
    config = {"design": design, "search": method, "k": 5}
    rag.CONFIG.write_text(json.dumps(config, indent=2))
    return config


# ---------------------------------------------------------------- 2. answers
def read_jsonl(path: Path) -> dict:
    if not path.is_file():
        return {}
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return {r["key"]: r for r in rows}


def append_jsonl(path: Path, row: dict) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def run_agent(questions: list[dict], config: dict) -> dict[str, dict]:
    saved = read_jsonl(ANSWERS)
    results = {}
    for q in questions:
        key = f"{q['id']}|{q['question']}|{config['design']}+{config['search']}"
        if key not in saved:
            print(f"asking {q['id']} ...", flush=True)
            for attempt in range(3):                  # Gemini's free tier is sometimes overloaded (503)
                try:
                    result = asyncio.run(agent.run(q["question"], approve=lambda request: False, base_only=True))
                    break
                except Exception as error:  # noqa: BLE001
                    print(f"  {q['id']} failed: {str(error)[:150]} - retrying in 30s", flush=True)
                    time.sleep(30)
            else:
                print(f"  skipping {q['id']} for now: run evaluate again later to fill it in", flush=True)
                continue
            result.pop("trace")
            saved[key] = {"key": key, "id": q["id"], **result}
            append_jsonl(ANSWERS, saved[key])
        results[q["id"]] = saved[key]
    print(f"{len(results)} of {len(questions)} questions answered", flush=True)
    return results


# ---------------------------------------------------------------- 3-4. checks and judge
def judge(q: dict, answer: dict, chunks: dict, model) -> dict:
    saved = read_jsonl(VERDICTS)
    key = f"{q['id']}|{answer['answer']}"
    if key in saved:
        return saved[key]
    evidence = "\n\n---\n\n".join(f"[{i}] {chunks[i]['text']}" for i in answer["retrieved"] if i in chunks)
    prompt = (f"{RUBRIC}\n\nQUESTION: {q['question']}\n\nREFERENCE ANSWER: {q['reference_answer']}\n\n"
              f"RETRIEVED PASSAGES:\n{evidence or '(none)'}\n\nANSWER TO GRADE:\n{answer['answer']}")
    started = time.time()
    message = model.invoke(prompt)
    verdict = message["parsed"]
    usage = message["raw"].usage_metadata or {}
    row = {"key": key, "id": q["id"], **verdict.model_dump(),
           "judge_tokens": usage.get("total_tokens", 0), "judge_seconds": round(time.time() - started, 1)}
    append_jsonl(VERDICTS, row)
    return row


def grade(questions: list[dict], answers: dict, config: dict) -> pd.DataFrame:
    chunks = {c["id"]: c for c in rag.read_chunks(config["design"])}
    model = agent.make_model().with_structured_output(Verdict, include_raw=True)
    rows = []
    for q in [q for q in questions if q["id"] in answers]:
        a = answers[q["id"]]
        retrieved = [chunks[i] for i in a["retrieved"] if i in chunks]
        row = {"id": q["id"], "kind": q["kind"], "question": q["question"], "answer": a["answer"],
               "refusal": int(a["refusal"]), "guardrail_fired": int(bool(a["guardrail"])),
               "citations_valid": int(set(a["cited"]) <= set(a["retrieved"]) and (a["refusal"] or bool(a["cited"]))),
               "expected_retrieved": int(any(found(retrieved, q["expected"]))) if q["expected"] else None,
               "tokens": a["input_tokens"] + a["output_tokens"], "seconds": a["seconds"],
               "model_calls": a["model_calls"]}
        if a["refusal"]:                   # code can grade refusals: right only if unanswerable
            row.update(correct=int(q["kind"] == "unanswerable"), supported=1, judge="code",
                       reason="correct refusal" if q["kind"] == "unanswerable" else "refused an answerable question")
        else:
            v = judge(q, a, chunks, model)
            correct = v["correct"] if q["kind"] != "unanswerable" else 0   # answering the unanswerable is wrong
            row.update(correct=correct, supported=v["supported"], judge="llm", reason=v["reason"],
                       judge_tokens=v["judge_tokens"])
        row["cause"] = failure_cause(row, q)
        rows.append(row)
    return pd.DataFrame(rows)


# ---------------------------------------------------------------- 5-6. causes, agreement, summary
def failure_cause(row: dict, q: dict) -> str:
    if row["correct"] and row["supported"]:
        return ""
    if q["kind"] == "unanswerable":
        return "unsupported claim"                     # it answered something the corpus does not say
    if row["refusal"]:
        return "wrong refusal" if row["expected_retrieved"] else "retrieval miss"
    if not row["correct"]:
        return "wrong answer from right passage" if row["expected_retrieved"] else "retrieval miss"
    return "unsupported claim"


def apply_overrides(graded: pd.DataFrame) -> pd.DataFrame:
    """eval/failure_overrides.csv (id,cause,note) lets me correct a cause after reading the failure,
    e.g. 'bad test question'."""
    path = EVAL / "failure_overrides.csv"
    if path.is_file():
        overrides = pd.read_csv(path, dtype=str).fillna("")
        for _, o in overrides.iterrows():
            graded.loc[graded.id == o["id"], ["cause", "cause_note"]] = [o["cause"], o.get("note", "")]
    return graded


def agreement(graded: pd.DataFrame) -> dict:
    path = EVAL / "human_labels.csv"
    human = pd.read_csv(path, dtype={"id": str}) if path.is_file() else pd.DataFrame()
    if human.empty:
        return {"graded_by_me": 0}
    both = human.merge(graded[["id", "correct", "supported", "judge"]], on="id", suffixes=("_me", "_judge"))
    both = both[both.judge == "llm"]                     # refusals are graded by code, not by the judge
    out = {"graded_by_me": int(len(human)), "compared_with_judge": int(len(both))}
    for col in ["correct", "supported"]:
        same = both[f"{col}_me"].astype(int) == both[f"{col}_judge"].astype(int)
        out[f"agree_{col}"] = round(float(same.mean()), 3) if len(both) else None
        out[f"disagree_{col}_ids"] = both.loc[~same, "id"].tolist()
    return out


def write_grading_sheet(questions: list[dict], answers: dict, config: dict) -> None:
    """eval/to_grade.md: question, reference, answer and cited passages, WITHOUT the judge's verdict,
    so I can fill eval/human_labels.csv before looking at eval/graded.csv."""
    chunks = {c["id"]: c for c in rag.read_chunks(config["design"])}
    lines = ["# Answers to grade by hand (judge verdicts are not shown here)\n"]
    for q in [q for q in questions if q["id"] in answers]:
        a = answers[q["id"]]
        lines += [f"## {q['id']} ({q['kind']})", f"**Question:** {q['question']}",
                  f"**Reference:** {q['reference_answer']}", f"**Answer:** {a['answer']}", "**Retrieved passages:**"]
        lines += [f"- [{i}] {rag.cite(chunks[i])}: {chunks[i]['text'][:400]}..." for i in a["retrieved"] if i in chunks]
        lines.append("")
    (EVAL / "to_grade.md").write_text("\n".join(lines), encoding="utf-8")


def judge_tokens(graded: pd.DataFrame) -> int:
    tokens = graded["judge_tokens"].dropna() if "judge_tokens" in graded else pd.Series(dtype=float)
    return round(float(tokens.mean())) if len(tokens) else 0


def main() -> None:
    questions = load_questions()
    print("== 1. retrieval")
    summary = evaluate_retrieval(questions)
    print(summary.to_string(index=False))
    config = choose_design(summary)
    print(f"chosen: {config}")

    print("\n== 2. agent answers (saved as they arrive)")
    answers = run_agent(questions, config)
    write_grading_sheet(questions, answers, config)

    print("\n== 3-4. code checks and LLM judge")
    graded = apply_overrides(grade(questions, answers, config))
    graded.to_csv(EVAL / "graded.csv", index=False)

    answerable = graded[graded.kind != "unanswerable"]
    unanswerable = graded[graded.kind == "unanswerable"]
    failures = graded[graded.cause != ""]
    result = {
        "config": config,
        "questions": len(graded),
        "correct": int(graded.correct.sum()),
        "correct_answerable": int(answerable.correct.sum()), "answerable": len(answerable),
        "unsupported_answers": int(((graded.supported == 0) & (graded.refusal == 0)).sum()),
        "correct_refusals": int(unanswerable.refusal.sum()), "unanswerable": len(unanswerable),
        "wrong_refusals": int(answerable.refusal.sum()),
        "invalid_citations": int((graded.citations_valid == 0).sum()),
        "guardrail_fired": int(graded.guardrail_fired.sum()),
        "failures_by_cause": failures.cause.value_counts().to_dict(),
        "agent_tokens_per_question": round(float(graded.tokens.mean())),
        "agent_seconds_per_question": round(float(graded.seconds.mean()), 1),
        "judge_tokens_per_graded_answer": judge_tokens(graded),
        "agreement_with_me": agreement(graded),
    }
    (EVAL / "summary.json").write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))
    print("\nwrote eval/retrieval.csv, retrieval_summary.csv, answers.jsonl, judge.jsonl, graded.csv, "
          "summary.json and to_grade.md")


if __name__ == "__main__":
    main()
