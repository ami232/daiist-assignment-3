"""
Assignment 3: evaluation (`main.py evaluate`).

Stages, each saved in eval/ so a re-run only does what is missing (`--fresh` redoes it):

  1. retrieval   hit rate @1/@3/@5 for each chunking design      -> retrieval_*.csv, .png
  2. answers     the agent answers every question               -> answers.jsonl, answers.md
  3. checks      what code can check (citations, refusals)      -> checks.csv
  4. judge       an LLM judge with a rubric and the evidence    -> judge_verdicts.csv
  5. agreement   judge vs my own grades (human_labels.csv)      -> agreement.json
  6. experiment  one unanswerable question before/after add_document -> experiment.json
  7. failures    a first classification of every failure        -> failures.csv
  8. summary     numbers for REPORT.md                          -> summary.json

My own grades must be written BEFORE I open judge_verdicts.csv: answers.md has the
answers without any verdict, for that purpose.

    uv run python main.py evaluate
    uv run python evaluate.py --only retrieval          # one stage
    uv run python evaluate.py --limit 5 --only answers  # a quick test
"""

import argparse
import csv
import json
import os
import re
import shutil
import statistics
import sys
import tempfile
import time
from pathlib import Path

import rag

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
HUMAN = EVAL / "human_labels.csv"
HOLDOUT = "holdout/guidelines_gpai_C2025-7719.pdf"
EXPERIMENT_MARKER = "10^23"  # the unanswerable question that the held-out document answers
HITS = (1, 3, 5)
JUDGE_MODELS = [m for m in [os.environ.get("JUDGE_MODEL"), "gemini-3.1-flash-lite"] if m]
CITE_USED = re.compile(r"\[([^\[\]|]+\|[^\[\]]+)\]")
REFUSAL = re.compile(
    r"(indexed [^.]{0,60}?(do|does) not (cover|state|specify|contain|give|mention|provide|include)|documents? (do(es)? )?not cover|do(es)? not cover (this|that|the)|not covered (by|in) the|"
    r"corpus does not|cannot answer|can't answer|unable to answer|no (relevant )?information (on|about|in)|"
    r"not (contain|include|address|mention)ed? in the (indexed )?(documents|corpus|search))",
    re.I,
)


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


def read_csv(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict], fields: list[str] | None = None) -> None:
    fields = fields or (list(rows[0]) if rows else [])
    with path.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def append_jsonl(path: Path, row: dict) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def questions() -> list[dict]:
    return read_csv(QUESTIONS)


def expected_pairs(q: dict) -> list[tuple[str, str]]:
    sources = [s.strip() for s in q["expected_source"].split(";") if s.strip()]
    locations = [s.strip() for s in q["expected_location"].split(";") if s.strip()]
    return list(zip(sources, locations))


def pct(x: float) -> str:
    return f"{100 * x:.1f}%"


# --------------------------------------------------------------------------- #
# 1. Retrieval: hit rate at 1, 3 and 5 for each design
# --------------------------------------------------------------------------- #


def stage_retrieval() -> dict:
    rows, summary = [], []
    answerable = [q for q in questions() if q["kind"] != "unanswerable"]
    for design in rag.DESIGNS:
        try:
            store = rag.load_store(design, refresh=True)
        except RuntimeError as error:
            log(f"[retrieval] skipping design '{design}': {error}")
            continue
        per_q = []
        for q in answerable:
            hits = rag.search_vector(rag.embed_query(q["question"]), k=max(HITS), store=store)
            ranks = []
            for source, location in expected_pairs(q):
                found = [r for r, h in enumerate(hits, 1) if rag.chunk_covers(h, source, location)]
                ranks.append(found[0] if found else None)
            row = {"id": q["id"], "kind": q["kind"], "design": design,
                   "ranks": ";".join(str(r) if r else "-" for r in ranks)}
            for k in HITS:  # a question is a hit at k when EVERY expected passage is in the top k
                row[f"hit@{k}"] = int(all(r is not None and r <= k for r in ranks))
            rows.append(row)
            per_q.append(row)
        for kind in ("all", "single", "multi"):
            subset = [r for r in per_q if kind == "all" or r["kind"] == kind]
            if subset:
                summary.append({"design": design, "kind": kind, "n": len(subset),
                                **{f"hit@{k}": round(sum(r[f"hit@{k}"] for r in subset) / len(subset), 3) for k in HITS}})
    write_csv(EVAL / "retrieval_per_question.csv", rows)
    write_csv(EVAL / "retrieval_summary.csv", summary)
    print("\nRetrieval hit rate (a question is a hit when all its expected passages are in the top k):")
    for s in summary:
        print(f"  {s['design']:<10} {s['kind']:<7} n={s['n']:<3} " + "  ".join(f"@{k}: {pct(s[f'hit@{k}'])}" for k in HITS))
    try:
        import matplotlib
        matplotlib.use("Agg")
        import matplotlib.pyplot as plt

        fig, ax = plt.subplots(figsize=(6, 3.5))
        alls = [s for s in summary if s["kind"] == "all"]
        width = 0.8 / max(len(alls), 1)
        for i, s in enumerate(alls):
            ax.bar([j + i * width for j in range(len(HITS))], [100 * s[f"hit@{k}"] for k in HITS], width, label=s["design"])
        ax.set_xticks([j + width * (len(alls) - 1) / 2 for j in range(len(HITS))], [f"hit@{k}" for k in HITS])
        ax.set_ylabel("% of questions")
        ax.set_ylim(0, 100)
        ax.legend()
        ax.set_title("Retrieval hit rate by chunking design")
        fig.tight_layout()
        fig.savefig(EVAL / "retrieval_hit_rate.png", dpi=150)
    except Exception as error:  # noqa: BLE001 - the chart is optional
        log(f"[retrieval] chart skipped: {error}")
    return {"summary": summary}


# --------------------------------------------------------------------------- #
# 2. Answers: the agent on every question
# --------------------------------------------------------------------------- #


def stage_answers(fresh: bool, limit: int | None) -> None:
    from agent import Agent

    path = EVAL / "answers.jsonl"
    if fresh and path.exists():
        path.write_text("", encoding="utf-8")
    done = {r["id"] for r in read_jsonl(path) if not r.get("error")}
    todo = [q for q in questions() if q["id"] not in done]
    if limit:
        todo = todo[:limit]
    if not todo:
        log("[answers] all questions already answered (use --fresh to redo)")
    else:
        # evaluation has nobody to approve add_document, so it is denied here (agent default)
        with Agent(approve=lambda _path: False, verbose=False) as agent:
            for n, q in enumerate(todo, 1):
                result = None
                for attempt in range(3):
                    try:
                        result = agent.ask(q["question"])
                        break
                    except Exception as error:  # noqa: BLE001 - keep going, record the failure
                        log(f"[answers] {q['id']} attempt {attempt + 1} failed: {str(error)[:150]}")
                        time.sleep(20 * (attempt + 1))
                if result is None:
                    result = {"answer": "", "citations": [], "trace": [], "tool_calls": 0, "guardrail": "error",
                              "input_tokens": 0, "output_tokens": 0, "seconds": 0, "error": True}
                result = {"id": q["id"], "design": rag.get_design(), **result}
                append_jsonl(path, result)
                log(f"[answers] {n}/{len(todo)} {q['id']} ({result['seconds']} s, {result['tool_calls']} tool calls)")
    # one record per question, last attempt wins
    latest = {r["id"]: r for r in read_jsonl(path)}
    ordered = [latest[q["id"]] for q in questions() if q["id"] in latest]
    path.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in ordered), encoding="utf-8")
    lines = ["# Agent answers (no verdicts here: grade these first, in eval/human_labels.csv)\n"]
    by_id = {q["id"]: q for q in questions()}
    for r in ordered:
        q = by_id[r["id"]]
        lines.append(f"## {r['id']} ({q['kind']})\n\n**Question:** {q['question']}\n\n"
                     f"**Reference:** {q['reference_answer']}\n\n**Answer:**\n\n{r['answer']}\n")
    (EVAL / "answers.md").write_text("\n".join(lines), encoding="utf-8")


# --------------------------------------------------------------------------- #
# 3. Code checks
# --------------------------------------------------------------------------- #


def retrieved_chunks(answer: dict) -> list[dict]:
    """The chunks that the searches of this answer returned, found again in the store."""
    store = rag.load_store(answer.get("design"))
    by_citation = {rag.citation(c).strip("[]").lower(): c for c in store.chunks}
    found = []
    for step in answer["trace"]:
        if step["tool"] != "search":
            continue
        for cite in re.findall(r"cite as \[([^\]]+)\]", step["output"]):
            chunk = by_citation.get(re.sub(r"\s+", " ", cite).strip().lower())
            if chunk:
                found.append(chunk)
    return found


def stage_checks() -> list[dict]:
    from agent import is_offered

    by_id = {q["id"]: q for q in questions()}
    rows = []
    for a in read_jsonl(EVAL / "answers.jsonl"):
        q = by_id[a["id"]]
        pairs = expected_pairs(q)
        retrieved = retrieved_chunks(a)
        offered = {re.sub(r"\s+", " ", rag.citation(c).strip("[]")).lower() for c in retrieved}
        cited = [re.sub(r"\s+", " ", c).strip() for c in CITE_USED.findall(a["answer"])]
        cited_chunks = [c for c in retrieved if any(
            is_offered(x, {re.sub(r"\s+", " ", rag.citation(c).strip("[]")).lower()}) for x in cited)]
        refused = bool(REFUSAL.search(a["answer"]))
        row = {
            "id": a["id"], "kind": q["kind"],
            "searched": int(any(s["tool"] == "search" for s in a["trace"])),
            "citations_valid": int(all(is_offered(c, offered) for c in cited)),
            "n_citations": len(cited),
            "refused": int(refused),
            "refusal_ok": int(refused if q["kind"] == "unanswerable" else not refused),
            "retrieved_expected": "" if not pairs else int(all(any(rag.chunk_covers(c, s, l) for c in retrieved) for s, l in pairs)),
            "cites_expected": "" if not pairs else int(all(any(rag.chunk_covers(c, s, l) for c in cited_chunks) for s, l in pairs)),
            "guardrail": a["guardrail"],
        }
        if q["kind"] == "unanswerable":
            row["has_citation_ok"] = int(not cited or refused)  # a refusal may mention what the documents DO cover
        else:
            row["has_citation_ok"] = int(bool(cited))
        rows.append(row)
    write_csv(EVAL / "checks.csv", rows)
    return rows


# --------------------------------------------------------------------------- #
# 4. LLM judge
# --------------------------------------------------------------------------- #

RUBRIC = """You grade an answer from a retrieval-augmented assistant about the EU AI Act.
You get: the question, the question kind, a reference answer written by a person, the
assistant's answer, and the EVIDENCE (the passages the assistant retrieved).

correct (1 or 0):
- kind single/multi: 1 only if the answer states every key fact of the reference answer
  and does not contradict it. Extra correct detail is fine. A missing key fact, a wrong
  number or date, or a refusal is 0.
- kind unanswerable: 1 only if the answer clearly says the documents do not cover the
  question and does not give an invented answer. Mentioning related content that is in the
  evidence is fine. Answering the question itself is 0.
supported (1 or 0): 1 only if EVERY factual claim in the answer is stated in the EVIDENCE.
Ignore the closing sentence about consulting a legal professional. A refusal is supported.
A claim that is true in reality but absent from the EVIDENCE makes supported 0.
Do not reward length or confidence. Judge only against the reference and the evidence.
Reply as JSON: {"correct": 0 or 1, "supported": 0 or 1, "reason": "one short sentence"}"""


def judge_one(client, q: dict, a: dict, evidence: str) -> dict:
    from google.genai import types

    prompt = (
        f"{RUBRIC}\n\nQUESTION KIND: {q['kind']}\nQUESTION: {q['question']}\n"
        f"REFERENCE ANSWER: {q['reference_answer']}\n\nASSISTANT ANSWER:\n{a['answer']}\n\nEVIDENCE:\n{evidence}"
    )
    last = None
    for model in list(JUDGE_MODELS):
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=model, contents=prompt,
                    config=types.GenerateContentConfig(response_mime_type="application/json", temperature=0),
                )
                data = json.loads(response.text)
                return {"correct": int(data["correct"]), "supported": int(data["supported"]),
                        "reason": str(data.get("reason", "")), "judge_model": model}
            except Exception as error:  # noqa: BLE001 - try again, then the next model
                last = error
                if "503" in str(error) or "UNAVAILABLE" in str(error):
                    if model in JUDGE_MODELS and len(JUDGE_MODELS) > 1:
                        JUDGE_MODELS.remove(model)  # overloaded: do not waste time on it again
                    break
                time.sleep(10 * (attempt + 1))
    raise RuntimeError(f"judge failed: {last}")


def stage_judge(fresh: bool) -> list[dict]:
    from api_key import load_api_key
    from google import genai

    path = EVAL / "judge_verdicts.csv"
    old = {r["id"]: r for r in read_csv(path)} if path.exists() and not fresh else {}
    by_id = {q["id"]: q for q in questions()}
    client = genai.Client(api_key=load_api_key())
    rows = []
    for a in read_jsonl(EVAL / "answers.jsonl"):
        if a["id"] in old:
            rows.append(old[a["id"]])
            continue
        if a.get("error"):
            continue
        evidence = "\n\n".join(dict.fromkeys(s["output"] for s in a["trace"] if s["tool"] == "search"))[:30000]
        verdict = judge_one(client, by_id[a["id"]], a, evidence or "(no passages were retrieved)")
        rows.append({"id": a["id"], **verdict})
        log(f"[judge] {a['id']} done")
        write_csv(path, rows, ["id", "correct", "supported", "reason", "judge_model"])  # resumable
    write_csv(path, rows, ["id", "correct", "supported", "reason", "judge_model"])
    return rows


# --------------------------------------------------------------------------- #
# 5. Agreement with my own grades
# --------------------------------------------------------------------------- #


def stage_agreement(judge_rows: list[dict]) -> dict:
    if not HUMAN.exists():
        return {"status": "no human_labels.csv"}
    human = {r["id"]: r for r in read_csv(HUMAN) if r.get("correct", "").strip() in ("0", "1")}
    judge = {r["id"]: r for r in judge_rows}
    ids = [i for i in human if i in judge]
    if len(ids) < 20:
        result = {"status": f"only {len(ids)} human labels with a judge verdict; 20+ needed", "n": len(ids)}
        (EVAL / "agreement.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
        return result
    result = {"n": len(ids)}
    for field in ("correct", "supported"):
        pairs = [(int(human[i][field]), int(judge[i][field])) for i in ids if human[i].get(field, "").strip() in ("0", "1")]
        if not pairs:
            continue
        agree = sum(h == j for h, j in pairs) / len(pairs)
        p_h, p_j = sum(h for h, _ in pairs) / len(pairs), sum(j for _, j in pairs) / len(pairs)
        expected = p_h * p_j + (1 - p_h) * (1 - p_j)
        result[field] = {
            "n": len(pairs), "agreement": round(agree, 3),
            "cohen_kappa": round((agree - expected) / (1 - expected), 3) if expected < 1 else None,
            "disagreements": [i for i in ids if human[i].get(field, "").strip() in ("0", "1")
                              and int(human[i][field]) != int(judge[i][field])],
        }
    (EVAL / "agreement.json").write_text(json.dumps(result, indent=2), encoding="utf-8")
    return result


# --------------------------------------------------------------------------- #
# 6. Before / after adding a document
# --------------------------------------------------------------------------- #


def stage_experiment(fresh: bool) -> dict:
    from agent import Agent

    out = EVAL / "experiment.json"
    if out.exists() and not fresh:
        return json.loads(out.read_text(encoding="utf-8"))
    target = next((q for q in questions() if q["kind"] == "unanswerable" and EXPERIMENT_MARKER in q["question"]), None)
    if target is None or not (ROOT / HOLDOUT).exists():
        log("[experiment] skipped: question or held-out document not found")
        return {}
    snapshot = Path(tempfile.mkdtemp()) / "index"
    shutil.copytree(rag.INDEX_DIR, snapshot)  # the experiment changes index/, which is restored afterwards
    ask_add = f"Please add the file {HOLDOUT} to the corpus."
    try:
        with Agent(approve=lambda _p: False, verbose=False) as agent:
            before = agent.ask(target["question"])
            denied = agent.ask(ask_add)  # the harness denies it: nobody approved
        with Agent(approve=lambda _p: True, verbose=False) as agent:  # approval simulated for the experiment
            added = agent.ask(ask_add)
            after = agent.ask(target["question"])
    finally:
        for extra in rag.INDEX_DIR.iterdir():  # files the experiment created
            if not (snapshot / extra.name).exists():
                try:
                    extra.unlink()
                except OSError:
                    pass
        shutil.copytree(snapshot, rag.INDEX_DIR, dirs_exist_ok=True)  # put every original file back
        shutil.rmtree(snapshot.parent, ignore_errors=True)
    new_source = Path(HOLDOUT).stem

    def tool_out(r, name):
        return [s["output"] for s in r["trace"] if s["tool"] == name]

    result = {
        "question_id": target["id"], "question": target["question"], "document": HOLDOUT,
        "before": {"answer": before["answer"], "citations": before["citations"]},
        "add_denied": {"tool_output": tool_out(denied, "add_document"), "answer": denied["answer"]},
        "add_approved": {"tool_output": tool_out(added, "add_document"), "answer": added["answer"]},
        "after": {"answer": after["answer"], "citations": after["citations"],
                  "cites_new_document": any(new_source in c for c in after["citations"])},
        "before_refused": bool(REFUSAL.search(before["answer"])),
    }
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False), encoding="utf-8")
    print("\nExperiment (question %s):\n  before: %s\n  after:  %s" % (target["id"], before["answer"][:300], after["answer"][:300]))
    return result


# --------------------------------------------------------------------------- #
# 7. Failures and 8. summary
# --------------------------------------------------------------------------- #


def stage_failures(checks: list[dict], judge_rows: list[dict]) -> list[dict]:
    """A first classification by rule. I review it and fix it by hand in REPORT.md."""
    by_id = {q["id"]: q for q in questions()}
    judge = {r["id"]: r for r in judge_rows}
    failures = []
    for c in checks:
        j = judge.get(c["id"])
        if j is None:
            continue
        q = by_id[c["id"]]
        if int(j["correct"]) and int(j["supported"]) and c["citations_valid"]:
            continue
        if q["kind"] == "unanswerable":
            category = "unsupported_claim (answered an unanswerable question)" if not c["refused"] else "check_judge_or_test_question"
        elif c["refused"]:
            category = "wrong_refusal"
        elif c["retrieved_expected"] == 0:
            category = "retrieval_miss"
        elif not int(j["supported"]):
            category = "unsupported_claim"
        elif not int(j["correct"]):
            category = "wrong_answer_from_right_passage"
        else:
            category = "citation_problem"
        failures.append({"id": c["id"], "kind": q["kind"], "auto_category": category,
                         "correct": j["correct"], "supported": j["supported"], "judge_reason": j["reason"]})
    write_csv(EVAL / "failures.csv", failures, ["id", "kind", "auto_category", "correct", "supported", "judge_reason"])
    return failures


def stage_summary(retrieval: dict, checks: list[dict], judge_rows: list[dict], agreement: dict, failures: list[dict]) -> dict:
    answers = read_jsonl(EVAL / "answers.jsonl")
    summary: dict = {"agent_model": os.environ.get("AGENT_MODEL", "gemini-3.5-flash-lite"), "design": rag.get_design(),
                     "n_questions": len(answers), "retrieval": retrieval.get("summary", [])}
    if judge_rows:
        by_id = {q["id"]: q for q in questions()}
        for kind in ("all", "single", "multi", "unanswerable"):
            rows = [r for r in judge_rows if kind == "all" or by_id[r["id"]]["kind"] == kind]
            if rows:
                summary.setdefault("judge", {})[kind] = {
                    "n": len(rows),
                    "correct": round(sum(int(r["correct"]) for r in rows) / len(rows), 3),
                    "supported": round(sum(int(r["supported"]) for r in rows) / len(rows), 3),
                }
    if checks:
        for field in ("searched", "citations_valid", "refusal_ok", "has_citation_ok"):
            summary.setdefault("code_checks", {})[field] = round(sum(int(c[field]) for c in checks) / len(checks), 3)
        guard = {}
        for c in checks:
            guard[c["guardrail"]] = guard.get(c["guardrail"], 0) + 1
        summary["guardrail_outcomes"] = guard
    if answers:
        secs = [a["seconds"] for a in answers]
        toks = [a["input_tokens"] + a["output_tokens"] for a in answers]
        summary["cost_per_question"] = {
            "tokens_mean": round(statistics.mean(toks)), "tokens_median": round(statistics.median(toks)),
            "seconds_mean": round(statistics.mean(secs), 1), "seconds_median": round(statistics.median(secs), 1),
            "tool_calls_mean": round(statistics.mean(a["tool_calls"] for a in answers), 2),
            "total_tokens": sum(toks),
        }
    summary["agreement_with_human"] = agreement
    summary["failures"] = {"count": len(failures), "by_category": {}}
    for f in failures:
        cat = f["auto_category"]
        summary["failures"]["by_category"][cat] = summary["failures"]["by_category"].get(cat, 0) + 1
    (EVAL / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print("\nSummary saved in eval/summary.json")
    print(json.dumps({k: v for k, v in summary.items() if k != "retrieval"}, indent=2, ensure_ascii=False))
    return summary


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--only", choices=["retrieval", "answers", "judge", "experiment"], help="run one stage")
    parser.add_argument("--fresh", action="store_true", help="redo the selected stages from scratch")
    parser.add_argument("--limit", type=int, help="answer only this many questions (testing)")
    args = parser.parse_args()
    EVAL.mkdir(exist_ok=True)
    want = lambda s: args.only in (None, s)  # noqa: E731

    retrieval = stage_retrieval() if want("retrieval") else {}
    if args.only == "retrieval":
        return
    if want("answers"):
        stage_answers(args.fresh, args.limit)
    if args.only == "answers":
        return
    checks = stage_checks()
    judge_rows = stage_judge(args.fresh) if want("judge") else []
    if args.only == "judge":
        return
    agreement = stage_agreement(judge_rows)
    if want("experiment"):
        stage_experiment(args.fresh)
    failures = stage_failures(checks, judge_rows)
    stage_summary(retrieval, checks, judge_rows, agreement, failures)


if __name__ == "__main__":
    main()
