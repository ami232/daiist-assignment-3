"""
Assignment 3: evaluation (`main.py evaluate`).

1. Retrieval: hit rate at 1/3/5 for both chunking designs; picks the winner.
2. Agent: answers every question in eval/questions.csv (tools: server.py over MCP).
3. Code checks: citations valid (they appear in what the agent retrieved), refusals.
4. LLM judge: rubric + the retrieved text as evidence -> correct / supported.
5. Agreement with eval/human_labels.csv (your own grades).
6. Cost per question (tokens, seconds).

Results are saved in eval/. Agent answers and judge verdicts are cached in
eval/answers.json and eval/judge.json, so an interrupted run resumes without
spending quota again. Delete those files (or run with --fresh) to redo them.
"""

import argparse
import asyncio
import collections
import csv
import json
import re
import statistics
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
HUMAN = EVAL / "human_labels.csv"
ANSWERS = EVAL / "answers.json"
JUDGE = EVAL / "judge.json"

KS = (1, 3, 5)
# Tried in order; a model out of daily quota is skipped for the rest of the run.
# Starts from the lite / older models so the judge leaves quota to the agent.
JUDGE_MODELS = [
    "gemini-2.5-flash",
    "gemini-3.1-flash-lite",
    "gemini-3.5-flash-lite",
    "gemini-2.5-flash-lite",
    "gemini-3.8-flash",
    "gemini-3.7-flash",
    "gemini-3.5-flash",
]
JUDGE_MODEL = JUDGE_MODELS[0]
REFUSAL = re.compile(r"no consta en los documentos", re.I)
SOURCE = r"(Ley\s+\d+/\d{4}|RD\s+\d+/\d{4})"
LOCATION = (r"(Art[ií]culos?\s+\d+(?:\s*(?:bis|ter))?|Disposici[oó]n\s+\w+\s+\w+|Anexo\s+[IVX]+)")
CITATION = re.compile(SOURCE + r"[\s,.:;()*_]{0,6}" + LOCATION, re.I)


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.replace("Articulo", "Artículo")).strip().lower()


# ----------------------------------------------------------------------- data
def load_questions() -> list[dict]:
    with QUESTIONS.open(encoding="utf-8", newline="") as f:
        rows = [r for r in csv.DictReader(f) if (r.get("id") or "").strip()]
    for r in rows:
        r["expected"] = [(norm(s), norm(l)) for s, l in zip(
            [x for x in r["expected_source"].split(";") if x.strip()],
            [x for x in r["expected_location"].split(";") if x.strip()])]
    return rows


def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return {}


def save_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, ensure_ascii=False, indent=1), encoding="utf-8")


# ------------------------------------------------------------------ retrieval
def retrieval_eval(questions: list[dict]) -> dict:
    """Hit rate at k per design. single: the expected passage is in the top k.
    multi: ALL expected passages are in the top k (strict)."""
    import server

    answerable = [q for q in questions if q["kind"] != "unanswerable" and q["expected"]]
    out = {}
    for design in ("article", "fixed"):
        hits = {k: [] for k in KS}
        rows = []
        for q in answerable:
            res = server.retrieve(q["question"], max(KS), design)
            found = [(norm(h["source"]), norm(h["location"])) for h in res]
            row = {"id": q["id"], "kind": q["kind"]}
            for k in KS:
                ok = all(e in found[:k] for e in q["expected"])
                hits[k].append(ok)
                row[f"hit@{k}"] = int(ok)
            rows.append(row)
        out[design] = {
            "n": len(answerable),
            **{f"hit@{k}": round(sum(v) / max(len(v), 1), 3) for k, v in hits.items()},
            "rows": rows,
        }
    return out


def pick_design(ret: dict) -> str:
    return max(("article", "fixed"), key=lambda d: (ret[d]["hit@5"], ret[d]["hit@3"], ret[d]["hit@1"]))


# ---------------------------------------------------------------------- agent
def run_agent(questions: list[dict], fresh: bool) -> dict:
    import agent

    answers = {} if fresh else load_json(ANSWERS)
    todo = [q for q in questions if q["id"] not in answers or answers[q["id"]].get("error")]
    print(f"agent: {len(questions) - len(todo)} cached, {len(todo)} to run", flush=True)
    for i, q in enumerate(todo, start=1):
        if agent.next_model(agent.AGENT_MODELS, agent._unusable) is None:
            print(f"  every model in AGENT_MODELS is out of daily quota; stopping. "
                  f"{len(todo) - i + 1} question(s) left for the next run.", flush=True)
            break
        r = asyncio.run(agent.ask_many([q["question"]], approve=lambda *_: False))[0]
        answers[q["id"]] = r
        save_json(ANSWERS, answers)  # save after every question
        print(f"  [{i}/{len(todo)}] {q['id']} {r.get('model')} {r['seconds']}s "
              f"{'ERROR ' + r['error'][:60] if r['error'] else ''}", flush=True)
    return answers


def retrieved_pairs(trace: list[dict]) -> set:
    pairs = set()
    for e in trace:
        if e["tool"] != "search" or not e.get("result"):
            continue
        for m in re.finditer(r"^\[\d+\]\s+(.+?),\s+(.+?)\s+\(score", e["result"], re.M):
            pairs.add((norm(m.group(1)), norm(m.group(2))))
    return pairs


def evidence_text(trace: list[dict], limit: int = 14000) -> str:
    return "\n\n".join(e["result"] for e in trace if e["tool"] == "search" and e.get("result"))[:limit]


def code_checks(q: dict, r: dict) -> dict:
    """What code can check: citations are real, refusals are right."""
    answer = r.get("answer", "")
    got = retrieved_pairs(r.get("trace", []))
    cited = []
    for m in CITATION.finditer(answer):
        cited.append((norm(m.group(1)), norm(re.sub(r"Art[ií]culos", "Artículo", m.group(2), flags=re.I))))
    cited = list(dict.fromkeys(cited))
    refused = bool(REFUSAL.search(answer))
    valid = [c for c in cited if c in got]
    expected_retrieved = bool(q["expected"]) and all(e in got for e in q["expected"])
    return {
        "n_citations": len(cited),
        "invalid_citations": [f"{s}, {l}" for s, l in cited if (s, l) not in got],
        "all_citations_valid": len(valid) == len(cited),
        "has_citation": bool(cited),
        "refused": refused,
        "refusal_ok": (refused if q["kind"] == "unanswerable" else not refused),
        "expected_retrieved": expected_retrieved,
        "searches": sum(1 for e in r.get("trace", []) if e["tool"] == "search"),
    }


# ---------------------------------------------------------------------- judge
RUBRIC = """You grade an answer from a legal assistant that must answer ONLY from retrieved passages.

Given: QUESTION, KIND (single / multi / unanswerable), REFERENCE answer, the assistant's ANSWER and the EVIDENCE (the passages it retrieved).

Score two things, each 1 or 0:
- correct: 1 if the answer's substance agrees with the REFERENCE: it contains the key facts and contradicts nothing in it. For an unanswerable question, correct=1 only if the answer says the corpus does not cover it and invents no specific rule, number or deadline. Extra true detail does not matter; a wrong or missing key fact gives 0.
- supported: 1 if EVERY factual claim in the answer is stated in the EVIDENCE. A claim not found there gives 0, even if true in real life. A pure refusal with no claims is supported=1.

Be strict and literal. Reply with ONLY a JSON object: {"correct": 0 or 1, "supported": 0 or 1, "reason": "one short sentence"}"""


def judge_all(questions: list[dict], answers: dict, fresh: bool) -> dict:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from agent import _api_key, _text, model_unusable, next_model

    verdicts = {} if fresh else load_json(JUDGE)
    key = _api_key()
    unusable: set[str] = set()
    todo = [q for q in questions if q["id"] in answers and not answers[q["id"]].get("error")
            and (q["id"] not in verdicts or verdicts[q["id"]].get("correct") is None)]
    print(f"judge: {len(verdicts)} cached, {len(todo)} to run", flush=True)
    for q in todo:
        r = answers[q["id"]]
        prompt = (f"{RUBRIC}\n\nQUESTION: {q['question']}\nKIND: {q['kind']}\n"
                  f"REFERENCE: {q['reference_answer']}\n\nANSWER:\n{r['answer']}\n\n"
                  f"EVIDENCE:\n{evidence_text(r['trace']) or '(nothing was retrieved)'}")
        verdict = None
        if next_model(JUDGE_MODELS, unusable) is None:
            print("  every model in JUDGE_MODELS is out of daily quota; stopping.", flush=True)
            break
        while verdict is None and (name := next_model(JUDGE_MODELS, unusable)) is not None:
            model = ChatGoogleGenerativeAI(model=name, api_key=key, temperature=0, timeout=90, max_retries=1)
            for attempt in range(5):
                try:
                    text = _text(model.invoke(prompt).content)
                    m = re.search(r"\{.*\}", text, re.S)
                    verdict = json.loads(m.group(0))
                    verdict["correct"], verdict["supported"] = int(verdict["correct"]), int(verdict["supported"])
                    verdict["model"] = name
                    break
                except Exception as e:
                    if model_unusable(str(e)):
                        unusable.add(name)
                        print(f"  {name}: daily quota exhausted or unavailable, switching model", flush=True)
                        break
                    if attempt == 4:
                        verdict = {"correct": None, "supported": None, "model": name,
                                   "reason": f"judge failed: {e}"[:200]}
                    else:
                        time.sleep(10 * (attempt + 1))
        if verdict is None:
            print("  every model in JUDGE_MODELS is out of daily quota; stopping.", flush=True)
            break
        verdicts[q["id"]] = verdict
        save_json(JUDGE, verdicts)
    return verdicts


# ------------------------------------------------------------------ agreement
def agreement(verdicts: dict) -> dict:
    try:
        with HUMAN.open(encoding="utf-8", newline="") as f:
            human = [r for r in csv.DictReader(f) if (r.get("id") or "").strip()]
    except Exception:
        human = []
    out = {"n_human_labels": len(human)}
    for col in ("correct", "supported"):
        same, total, diffs = 0, 0, []
        for h in human:
            v = verdicts.get(h["id"])
            if not v or v.get(col) is None or h.get(col, "") == "":
                continue
            total += 1
            if int(h[col]) == v[col]:
                same += 1
            else:
                diffs.append(h["id"])
        out[col] = {"compared": total, "agree": same,
                    "rate": round(same / total, 3) if total else None, "disagreements": diffs}
    return out


def write_grading_sheet(questions: list[dict], answers: dict) -> None:
    """A readable file to grade by hand. It contains NO judge output."""
    lines = ["# Answers to grade (no judge verdicts here)\n",
             "For each: correct = right against the reference (or a proper refusal); "
             "supported = every claim is in the retrieved text.\n"]
    for q in questions:
        r = answers.get(q["id"])
        if not r:
            continue
        lines += [f"\n---\n## {q['id']} ({q['kind']})", f"**Question:** {q['question']}",
                  f"**Reference:** {q['reference_answer']}", f"**Answer:**\n\n{r['answer'] or '(no answer: ' + str(r.get('error')) + ')'}\n",
                  "**Retrieved passages:**\n", evidence_text(r["trace"], 9000) or "(nothing retrieved)"]
    out = EVAL / "answers_for_grading.md"
    out.write_text("\n".join(lines), encoding="utf-8")
    print(f"\nWrote {out}. Grade 20+ answers in eval/human_labels.csv, then run the full evaluation.")


# ----------------------------------------------------------------------- main
def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--fresh", action="store_true", help="ignore cached answers and verdicts")
    ap.add_argument("--skip-agent", action="store_true", help="retrieval only")
    ap.add_argument("--answers-only", action="store_true",
                    help="run the agent only (no judge) and write eval/answers_for_grading.md, "
                         "so you can grade by hand before seeing any judge verdict")
    args = ap.parse_args()

    questions = load_questions()
    kinds = {k: sum(q["kind"] == k for q in questions) for k in ("single", "multi", "unanswerable")}
    print(f"{len(questions)} questions: {kinds}")
    if len(questions) < 30 or kinds["unanswerable"] < 5 or kinds["multi"] < 5:
        print("WARNING: the assignment needs 30+ questions, 5+ multi and 5+ unanswerable.")

    print("\n== Retrieval (hit rate) ==", flush=True)
    ret = retrieval_eval(questions)
    for d, v in ret.items():
        print(f"  {d:8s} n={v['n']}  hit@1={v['hit@1']}  hit@3={v['hit@3']}  hit@5={v['hit@5']}")
    winner = pick_design(ret)
    print(f"  winner by hit@5: {winner}  (server.py DESIGN must be \"{winner}\")")
    save_json(EVAL / "retrieval.json", ret)
    if args.skip_agent:
        return

    print("\n== Agent ==", flush=True)
    answers = run_agent(questions, args.fresh)
    if args.answers_only:
        write_grading_sheet(questions, answers)
        return
    print("\n== Judge ==", flush=True)
    verdicts = judge_all(questions, answers, args.fresh)

    rows, checks = [], {}
    for q in questions:
        r = answers.get(q["id"])
        if not r:
            continue
        c = code_checks(q, r)
        v = verdicts.get(q["id"]) or {}
        checks[q["id"]] = c
        rows.append({"id": q["id"], "kind": q["kind"], "agent_model": r.get("model") or "",
                     "judge_model": v.get("model") or "", "correct_judge": v.get("correct"),
                     "supported_judge": v.get("supported"), "judge_reason": v.get("reason"),
                     "refused": c["refused"], "refusal_ok": c["refusal_ok"],
                     "citations_valid": c["all_citations_valid"], "has_citation": c["has_citation"],
                     "expected_retrieved": c["expected_retrieved"], "invalid_citations": "; ".join(c["invalid_citations"]),
                     "searches": c["searches"], "tokens_in": r["tokens"]["input"],
                     "tokens_out": r["tokens"]["output"], "seconds": r["seconds"], "error": r.get("error") or "",
                     "answer": r["answer"].replace("\n", " ")})
    with (EVAL / "results.csv").open("w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)

    ok = [r for r in rows if not r["error"]]
    def rate(key, subset=None):
        s = [r[key] for r in (subset if subset is not None else ok) if r[key] is not None]
        return round(sum(bool(x) for x in s) / len(s), 3) if s else None
    unans = [r for r in ok if r["kind"] == "unanswerable"]
    answerable = [r for r in ok if r["kind"] != "unanswerable"]
    summary = {
        "agent_models_used": dict(collections.Counter(r["agent_model"] for r in ok)),
        "judge_models_used": dict(collections.Counter(r["judge_model"] for r in ok if r["judge_model"])),
        "design": winner,
        "n_questions": len(rows), "n_errors": len(rows) - len(ok),
        "retrieval": {d: {k: v for k, v in ret[d].items() if k != "rows"} for d in ret},
        "judge_correct": rate("correct_judge"), "judge_supported": rate("supported_judge"),
        "correct_answerable": rate("correct_judge", answerable),
        "proper_refusals_on_unanswerable": rate("refusal_ok", unans),
        "wrong_refusals_on_answerable": round(sum(r["refused"] for r in answerable) / max(len(answerable), 1), 3),
        "all_citations_valid": rate("citations_valid"),
        "answers_without_citation_not_refusal": sum((not r["has_citation"]) and (not r["refused"]) for r in ok),
        "agreement_with_human": agreement(verdicts),
        "cost_per_question": {
            "tokens_in_mean": round(statistics.mean(r["tokens_in"] for r in ok)) if ok else None,
            "tokens_out_mean": round(statistics.mean(r["tokens_out"] for r in ok)) if ok else None,
            "seconds_mean": round(statistics.mean(r["seconds"] for r in ok), 1) if ok else None,
            "seconds_max": max((r["seconds"] for r in ok), default=None)},
    }
    save_json(EVAL / "summary.json", summary)
    print("\n== Summary ==")
    print(json.dumps(summary, ensure_ascii=False, indent=1))
    print("\nFiles: eval/results.csv, eval/summary.json, eval/retrieval.json, eval/answers.json, eval/judge.json")
    print("Failures to classify by hand: rows in results.csv with correct_judge=0, supported_judge=0,")
    print("refusal_ok=False, citations_valid=False or error.")


if __name__ == "__main__":
    main()