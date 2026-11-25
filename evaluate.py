"""
Assignment 3: evaluation (`main.py evaluate`).

1. Retrieval: hit rate at k=1/3/5 for both chunking designs (no text model needed).
2. The agent answers every question (saved in eval/answers.jsonl, so a run can resume).
3. Code checks: refusals, valid citations, expected source cited, tool calls.
4. LLM judge with a rubric and the retrieved text as evidence (eval/judge.jsonl).
5. Agreement with my own labels in eval/human_labels.csv (if the file exists).
6. Cost and latency per question. Everything is saved in eval/.
"""

import csv
import json
import sys
from pathlib import Path

from langchain_google_genai import ChatGoogleGenerativeAI

import agent
import retrieval
from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
DESIGNS = ["structure", "fixed"]
KS = [1, 3, 5]
JUDGE_MODEL = agent.MODEL

RUBRIC = """You are a strict grader for a RAG assistant about EU data protection law.
You get a QUESTION, a REFERENCE answer, the RETRIEVED text the assistant saw, and the ANSWER.
Grade two things, each 1 or 0:
- correct: the ANSWER agrees with the REFERENCE. If the question is unanswerable, the only correct
  answer is a refusal saying the corpus does not cover it.
- supported: every claim in the ANSWER is in the RETRIEVED text. A refusal is always supported.
Reply with JSON only: {"correct": 0 or 1, "supported": 0 or 1, "reason": "one short sentence"}"""

def read_questions() -> list[dict]:
    with (EVAL / "questions.csv").open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))

def load_jsonl(path: Path) -> dict:
    rows = {}
    if path.is_file():
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                row = json.loads(line)
                rows[row["id"]] = row
    return rows

def append_jsonl(path: Path, row: dict) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")

def hit_rates(questions: list[dict]) -> dict:
    """Hit rate at k for each design, over the answerable questions."""
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    table = {}
    for design in DESIGNS:
        hits = {k: 0 for k in KS}
        by_kind = {"single": {k: 0 for k in KS}, "multi": {k: 0 for k in KS}}
        for q in answerable:
            results = retrieval.search(q["question"], k=max(KS), design=design)
            for k in KS:
                if retrieval.is_hit(results[:k], q["expected_source"], q["expected_location"]):
                    hits[k] += 1
                    by_kind[q["kind"]][k] += 1
        n = {"single": sum(q["kind"] == "single" for q in answerable),
             "multi": sum(q["kind"] == "multi" for q in answerable)}
        table[design] = {
            "n": len(answerable),
            "all": {k: round(hits[k] / len(answerable), 3) for k in KS},
            "single": {k: round(by_kind["single"][k] / n["single"], 3) for k in KS},
            "multi": {k: round(by_kind["multi"][k] / max(n["multi"], 1), 3) for k in KS},
        }
    return table

def run_agent(q: dict) -> dict:
    """Ask the agent one question; the context it retrieved is kept as evidence for the judge."""
    result = agent.ask(q["question"], approve=lambda path: False)
    retrieved = "\n\n".join(c["result"] for c in result["calls"] if c["name"] == "search")
    return {"id": q["id"], "answer": result["answer"], "refused": result["refused"],
            "cited": result["cited"], "invalid": result["invalid"], "guardrail": result["guardrail"],
            "n_calls": len(result["calls"]), "seconds": result["seconds"],
            "input_tokens": result["input_tokens"], "output_tokens": result["output_tokens"],
            "retrieved": retrieved[:9000]}

def code_checks(q: dict, row: dict) -> dict:
    """Checks written as code: refusal behaviour, valid citations, right source cited."""
    unanswerable = q["kind"] == "unanswerable"
    refusal_ok = row["refused"] if unanswerable else not row["refused"]
    citations_ok = row["refused"] or (bool(row["cited"]) and not row["invalid"])
    expected = [s.strip().lower() for s in q["expected_source"].split(";") if s.strip()]
    cited_sources = [c.strip("[]").split(",")[0].strip().lower() for c in row["cited"]]
    source_ok = True if unanswerable else all(s in cited_sources for s in expected)
    return {"refusal_ok": refusal_ok, "citations_ok": citations_ok, "source_ok": source_ok,
            "pass": refusal_ok and citations_ok and source_ok}

def judge(q: dict, row: dict) -> dict:
    llm = ChatGoogleGenerativeAI(model=JUDGE_MODEL, temperature=0, google_api_key=load_api_key(),
                                 timeout=120, max_retries=2)
    prompt = (f"{RUBRIC}\n\nQUESTION: {q['question']}\nREFERENCE: {q['reference_answer']}\n"
              f"RETRIEVED:\n{row['retrieved'] or '(nothing retrieved)'}\n\nANSWER: {row['answer']}")
    text = agent.text_of(llm.invoke(prompt).content).strip()
    start, end = text.find("{"), text.rfind("}")
    verdict = json.loads(text[start:end + 1])
    return {"id": q["id"], "correct": int(verdict["correct"]), "supported": int(verdict["supported"]),
            "reason": str(verdict.get("reason", ""))}

def agreement(judged: dict) -> dict | None:
    path = EVAL / "human_labels.csv"
    if not path.is_file():
        return None
    with path.open(encoding="utf-8", newline="") as f:
        human = {r["id"]: r for r in csv.DictReader(f) if r.get("correct", "").strip() in ("0", "1")}
    out = {"n": 0}
    for field in ("correct", "supported"):
        pairs = [(int(h[field]), judged[i][field]) for i, h in human.items() if i in judged and h.get(field, "").strip() in ("0", "1")]
        same = sum(a == b for a, b in pairs)
        out[field] = {"n": len(pairs), "agree": same, "rate": round(same / len(pairs), 3) if pairs else None,
                      "disagree_ids": [i for i, h in human.items() if i in judged and h.get(field, "").strip() in ("0", "1") and int(h[field]) != judged[i][field]]}
        out["n"] = len(pairs)
    return out

def main(tag: str = "") -> None:
    """tag: '' for the normal run; 'after' re-runs and saves to eval/*_after files."""
    questions = read_questions()
    summary: dict = {"n_questions": len(questions)}

    print("1/4 retrieval hit rates ...", file=sys.stderr)
    summary["hit_rate"] = hit_rates(questions)
    for design, row in summary["hit_rate"].items():
        print(f"  {design}: " + ", ".join(f"k={k}: {row['all'][k]:.2f}" for k in KS), file=sys.stderr)

    answers_path = EVAL / "answers.jsonl"
    judge_path = EVAL / "judge.jsonl"
    answers, judged = load_jsonl(answers_path), load_jsonl(judge_path)

    print("2/4 agent answers ...", file=sys.stderr)
    for q in questions:
        if q["id"] in answers:
            continue
        try:
            answers[q["id"]] = run_agent(q)
            append_jsonl(answers_path, answers[q["id"]])
            print(f"  {q['id']} done in {answers[q['id']]['seconds']} s", file=sys.stderr)
        except Exception as error:  # noqa: BLE001
            print(f"  {q['id']} failed ({type(error).__name__}); run evaluate again to retry", file=sys.stderr)

    print("3/4 code checks and LLM judge ...", file=sys.stderr)
    checks = {}
    for q in questions:
        row = answers.get(q["id"])
        if not row:
            continue
        checks[q["id"]] = code_checks(q, row)
        if q["id"] not in judged:
            try:
                judged[q["id"]] = judge(q, row)
                append_jsonl(judge_path, judged[q["id"]])
            except Exception as error:  # noqa: BLE001
                print(f"  judge failed on {q['id']} ({type(error).__name__})", file=sys.stderr)

    done = [q for q in questions if q["id"] in answers]
    summary["answered"] = len(done)
    summary["code_checks"] = {name: sum(checks[q["id"]][name] for q in done) for name in ("refusal_ok", "citations_ok", "source_ok", "pass")}
    summary["guardrail_fired"] = [q["id"] for q in done if answers[q["id"]]["guardrail"]]
    summary["code_failures"] = [q["id"] for q in done if not checks[q["id"]]["pass"]]
    scored = [q for q in done if q["id"] in judged]
    summary["judge"] = {"n": len(scored),
                        "correct": sum(judged[q["id"]]["correct"] for q in scored),
                        "supported": sum(judged[q["id"]]["supported"] for q in scored),
                        "wrong_ids": [q["id"] for q in scored if not judged[q["id"]]["correct"]],
                        "unsupported_ids": [q["id"] for q in scored if not judged[q["id"]]["supported"]]}
    for kind in ("single", "multi", "unanswerable"):
        subset = [q for q in scored if q["kind"] == kind]
        summary["judge"][f"correct_{kind}"] = f"{sum(judged[q['id']]['correct'] for q in subset)}/{len(subset)}"

    print("4/4 agreement, cost and latency ...", file=sys.stderr)
    summary["agreement"] = agreement(judged)
    seconds = sorted(answers[q["id"]]["seconds"] for q in done)
    if seconds:
        summary["latency_seconds"] = {"mean": round(sum(seconds) / len(seconds), 1),
                                      "p95": seconds[min(len(seconds) - 1, int(0.95 * len(seconds)))]}
        summary["tokens_per_question"] = {
            "input": round(sum(answers[q["id"]]["input_tokens"] for q in done) / len(done)),
            "output": round(sum(answers[q["id"]]["output_tokens"] for q in done) / len(done))}

    name = f"summary_{tag}.json" if tag else "summary.json"
    (EVAL / name).write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print(json.dumps(summary, indent=2))

if __name__ == "__main__":
    main()
