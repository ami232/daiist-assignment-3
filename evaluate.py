"""
Assignment 3: evaluation (`main.py evaluate`).

Stages (all run by default; results of each are cached in eval/, so a second run is free):

  retrieval  hit rate at k = 1, 3, 5 for both chunking designs        -> eval/retrieval.csv
  answers    the agent answers every question (add_document denied)   -> eval/answers.jsonl, eval/answers.csv
  judge      code checks + LLM judge with the rubric in eval/rubric.md -> eval/verdicts.csv
  report     agreement with eval/human_labels.csv, failures, cost      -> eval/summary.md, eval/failures.csv

Do this in order the first time:
  1. uv run python evaluate.py retrieval answers
  2. Grade 20+ answers yourself in eval/human_labels.csv, reading eval/answers.csv only.
  3. uv run python main.py evaluate         (judge + report)

Options: --ids q07,q08   only those questions (a cheap trial run)
         --refresh       redo the answers and verdicts of the selected questions
"""

import argparse
import csv
import json
import os
import re
import statistics
import sys
import time
from pathlib import Path

os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")

import index

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
HUMAN = EVAL / "human_labels.csv"
RUBRIC = EVAL / "rubric.md"
ANSWERS = EVAL / "answers.jsonl"
KS = (1, 3, 5)
JUDGE_MODEL = os.environ.get("JUDGE_MODEL", os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite"))
EVIDENCE_CHARS = 14000

DEFAULT_RUBRIC = """\
DRAFT RUBRIC: replace it with your own criteria before you submit, and explain it in REPORT.md.

correct (1/0)
- Question with an answer: 1 if the answer gives every key fact of the reference answer (parties, amounts,
  periods, who must do what) and contradicts none. Extra correct detail is fine. A missing or wrong figure,
  or the right clause of the wrong contract, is 0. An answer that refuses is 0.
- Question the corpus cannot answer: 1 only if the answer says the corpus does not state it (it may mention the
  nearest related fact, as long as it says clearly that the asked fact is missing). Any invented figure,
  period or party is 0.

supported (1/0)
- 1 if every factual claim in the answer is stated in the retrieved passages (the evidence). 0 if any claim,
  number or contract name is not there, even if it happens to be true. A refusal that adds no claim is 1.
"""


# --------------------------------------------------------------------------
# Helpers
# --------------------------------------------------------------------------

def load_questions(ids: list[str] | None) -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if (r.get("question") or "").strip()]
    for r in rows:
        r["kind"] = r["kind"].strip().lower()
    return [r for r in rows if not ids or r["id"] in ids]


def expected_pairs(row: dict) -> list[tuple[str, list[str]]]:
    """[(source, [clause numbers or 'Schedule n'])] for an answerable question."""
    sources = [s.strip() for s in row["expected_source"].split(";") if s.strip()]
    locs = [l.strip() for l in row["expected_location"].split(";") if l.strip()]
    if len(sources) == len(locs):
        pairs = list(zip(sources, locs))
    elif len(sources) == 1:
        pairs = [(sources[0], l) for l in locs]
    else:
        pairs = [(s, locs[i] if i < len(locs) else "") for i, s in enumerate(sources)]
    out = []
    for source, loc in pairs:
        keys = re.findall(r"schedule\s+\d+|\d+(?:\.\d+)?", loc, re.I)
        out.append((source, [k.title() if k.lower().startswith("schedule") else k for k in keys]))
    return out


def text_has(text: str, key: str) -> bool:
    """Does a passage contain this clause? Works on both designs (sub-clause numbers are tokens)."""
    if key.lower().startswith("schedule"):
        return re.search(re.escape(key).replace(r"\ ", r"\s+"), text, re.I) is not None
    if "." in key:
        return re.search(rf"(?<!\S){re.escape(key)}(?!\S)", text) is not None
    return re.search(rf"(?<!\S){re.escape(key)}\.(?!\S)|(?<!\S){re.escape(key)}\.\d+(?!\S)", text) is not None


def passage_matches(source: str, text: str, pair: tuple[str, list[str]]) -> bool:
    exp_source, keys = pair
    return source == exp_source and (not keys or any(text_has(text, k) for k in keys))


def all_pairs_found(passages: list[tuple[str, str]], pairs) -> bool:
    return all(any(passage_matches(s, t, p) for s, t in passages) for p in pairs)


def parse_search_result(result: str) -> list[tuple[str, str]]:
    """(source, text) for each passage of a `search` tool result."""
    out = []
    for block in re.split(r"\n\n(?=\[\d+\] \[)", result):
        m = re.match(r"\[\d+\] \[(CONTRACT_\d{3}\.pdf) \|[^\n]*\n(.*)", block, re.S)
        if m:
            out.append((m.group(1), m.group(2)))
    return out


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def read_jsonl(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    return {j["id"]: j for j in (json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip())}


def write_jsonl(path: Path, records: dict[str, dict]) -> None:
    path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in records.values()) + "\n", encoding="utf-8")


def is_refusal(answer: str) -> bool:
    return re.sub(r"^[\W_]+", "", answer.strip()).upper().startswith("NOT IN CORPUS")


def pct(n: int, d: int) -> str:
    return f"{n}/{d} ({100 * n / d:.0f}%)" if d else "n/a"


def rate_limited(error: Exception) -> str | None:
    """'minute' or 'day' if the error is a Gemini quota error, else None."""
    text = str(error)
    if "429" in text or "RESOURCE_EXHAUSTED" in text or "quota" in text.lower():
        return "day" if ("PerDay" in text or "per day" in text.lower()) else "minute"
    return None


# --------------------------------------------------------------------------
# Stage 1: retrieval
# --------------------------------------------------------------------------

def stage_retrieval(questions: list[dict]) -> None:
    rows, dist = [], {"answerable": [], "unanswerable": []}
    words_top5: dict[str, list[int]] = {d: [] for d in index.DESIGNS}
    for q in questions:
        pairs = expected_pairs(q) if q["kind"] != "unanswerable" else []
        for design in index.DESIGNS:
            try:
                hits = index.retrieve(q["question"], k=max(KS), design=design)
            except index.QuotaExhausted as error:
                raise SystemExit(f"Daily embedding quota reached during retrieval ({q['id']}). Run again later.\n{str(error)[:200]}")
            if hits:
                words_top5[design].append(sum(h["metadata"]["words"] for h in hits))
                if design == index.ACTIVE_DESIGN:
                    dist["unanswerable" if q["kind"] == "unanswerable" else "answerable"].append(hits[0]["distance"])
            if not pairs:
                continue
            passages = [(h["metadata"]["source"], h["text"]) for h in hits]
            rank = next((k for k in range(1, len(passages) + 1) if all_pairs_found(passages[:k], pairs)), 0)
            any_rank = next((k for k in range(1, len(passages) + 1)
                             if any(passage_matches(s, t, p) for s, t in passages[:k] for p in pairs)), 0)
            row = {"id": q["id"], "kind": q["kind"], "design": design, "rank_all": rank or "", "rank_any": any_rank or ""}
            for k in KS:
                row[f"hit@{k}"] = int(0 < rank <= k)
            rows.append(row)
    write_csv(EVAL / "retrieval.csv", rows, ["id", "kind", "design", "rank_all", "rank_any"] + [f"hit@{k}" for k in KS])

    lines = ["| design | questions | " + " | ".join(f"hit@{k}" for k in KS) + " | avg words in top 5 |", "|---|---|" + "---|" * (len(KS) + 1)]
    summary = {}
    for design in index.DESIGNS:
        for label, kinds in (("all answerable", ("single", "multi")), ("single", ("single",)), ("multi (all passages)", ("multi",))):
            rs = [r for r in rows if r["design"] == design and r["kind"] in kinds]
            if not rs:
                continue
            cells = [pct(sum(r[f"hit@{k}"] for r in rs), len(rs)) for k in KS]
            summary[f"{design}/{label}"] = {f"hit@{k}": sum(r[f"hit@{k}"] for r in rs) / len(rs) for k in KS}
            w = statistics.mean(words_top5[design]) if words_top5[design] else 0
            lines.append(f"| {design}: {label} | {len(rs)} | " + " | ".join(cells) + f" | {w:.0f} |")
    d_a, d_u = dist["answerable"], dist["unanswerable"]
    lines.append("")
    if d_a and d_u:
        lines.append(f"Distance of the top result ({index.ACTIVE_DESIGN} design): answerable questions mean {statistics.mean(d_a):.3f}, "
                     f"unanswerable mean {statistics.mean(d_u):.3f} (lower is closer).")
    (EVAL / "retrieval.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


# --------------------------------------------------------------------------
# Stage 2: answers
# --------------------------------------------------------------------------

def stage_answers(questions: list[dict], refresh: bool) -> None:
    import agent

    done = read_jsonl(ANSWERS)
    todo = [q for q in questions if refresh or q["id"] not in done]
    if todo:
        print(f"Running the agent on {len(todo)} questions ({len(questions) - len(todo)} cached) ...", file=sys.stderr)
        server = agent.McpServer()
        try:
            from langchain_google_genai import ChatGoogleGenerativeAI
            from api_key import load_api_key
            model = ChatGoogleGenerativeAI(model=agent.MODEL, google_api_key=load_api_key())
            for n, q in enumerate(todo, 1):
                out = None
                for attempt in range(6):
                    try:
                        out = agent.ask(q["question"], approve=lambda *a: False, server=server, model=model)
                        break
                    except Exception as error:  # noqa: BLE001
                        kind = rate_limited(error)
                        if kind == "day":
                            write_jsonl(ANSWERS, done)
                            raise SystemExit(f"Daily Gemini quota reached at {q['id']}. Everything so far is saved; run again later.")
                        if kind == "minute":
                            wait = 30 * (attempt + 1)
                            print(f"  rate limit, waiting {wait}s ...", file=sys.stderr)
                            time.sleep(wait)
                            continue
                        out = {"answer": f"[ERROR: {type(error).__name__}: {str(error)[:300]}]", "trace": [], "events": ["error"],
                               "input_tokens": 0, "output_tokens": 0, "seconds": 0.0}
                        break
                if out is None:
                    write_jsonl(ANSWERS, done)
                    raise SystemExit(f"Gemini kept refusing at {q['id']}; saved progress. Run again.")
                for step in out["trace"]:
                    step["result"] = step["result"][:7000]
                done[q["id"]] = {"id": q["id"], **out}
                write_jsonl(ANSWERS, done)
                print(f"  [{n}/{len(todo)}] {q['id']}: {len(out['trace'])} tool calls, {out['seconds']:.1f}s", file=sys.stderr)
        finally:
            server.close()
    # A file to grade from: answers only, no verdicts, so grading stays independent of the judge.
    rows = []
    for q in load_questions(None):
        a = done.get(q["id"])
        if a:
            rows.append({"id": q["id"], "kind": q["kind"], "question": q["question"],
                         "reference_answer": q["reference_answer"], "agent_answer": a["answer"],
                         "tool_calls": len(a["trace"])})
    write_csv(EVAL / "answers.csv", rows, ["id", "kind", "question", "reference_answer", "agent_answer", "tool_calls"])


# --------------------------------------------------------------------------
# Stage 3: code checks + LLM judge
# --------------------------------------------------------------------------

def numbers_in(text: str) -> set[str]:
    return {n.replace(",", "").rstrip(".") for n in re.findall(r"\d[\d,]*(?:\.\d+)?", text)}


def code_checks(q: dict, a: dict) -> dict:
    """What code can check: refusal, citations, expected sources and numbers."""
    import agent

    answer = a["answer"]
    refused = is_refusal(answer)
    problems = agent.check_citations(answer, a["trace"])
    cited = set(agent.SOURCE_RE.findall(answer))
    row = {
        "refused": int(refused),
        "citations_valid": int(not problems),
        "refusal_ok": int(refused == (q["kind"] == "unanswerable")),
        "guardrails": ",".join(a["events"]),
    }
    if q["kind"] == "unanswerable":
        row.update({"cites_expected": "", "numbers_ok": ""})
    else:
        pairs = expected_pairs(q)
        row["cites_expected"] = int(all(p[0] in cited for p in pairs)) if not refused else 0
        ref_numbers = numbers_in(q["reference_answer"])
        row["numbers_ok"] = int(ref_numbers <= numbers_in(answer)) if not refused else 0
    return row


def make_judge():
    from langchain_google_genai import ChatGoogleGenerativeAI
    from pydantic import BaseModel
    from api_key import load_api_key

    class Verdict(BaseModel):
        correct: bool
        supported: bool
        reason: str

    return ChatGoogleGenerativeAI(model=JUDGE_MODEL, google_api_key=load_api_key()).with_structured_output(Verdict)


def judge_one(judge, rubric: str, q: dict, a: dict) -> dict:
    evidence = "\n\n".join(s["result"] for s in a["trace"] if s["tool"] == "search")[:EVIDENCE_CHARS] or "(the agent retrieved nothing)"
    prompt = (
        "You grade an answer given by a contract assistant. Follow the rubric exactly.\n\n"
        f"RUBRIC\n{rubric}\n\n"
        f"QUESTION ({'the corpus can answer it' if q['kind'] != 'unanswerable' else 'the corpus CANNOT answer it'})\n{q['question']}\n\n"
        f"REFERENCE ANSWER\n{q['reference_answer']}\n\n"
        f"EVIDENCE (the passages the assistant retrieved)\n{evidence}\n\n"
        f"ANSWER TO GRADE\n{a['answer']}\n\n"
        "Return correct, supported and a one-sentence reason."
    )
    for attempt in range(6):
        try:
            v = judge.invoke(prompt)
            return {"judge_correct": int(v.correct), "judge_supported": int(v.supported), "judge_reason": v.reason}
        except Exception as error:  # noqa: BLE001
            kind = rate_limited(error)
            if kind == "day":
                raise SystemExit("Daily Gemini quota reached while judging. Run again later; verdicts so far are saved.")
            time.sleep(30 * (attempt + 1) if kind else 5)
    return {"judge_correct": "", "judge_supported": "", "judge_reason": "judge failed"}


def stage_judge(questions: list[dict], refresh: bool) -> list[dict]:
    answers = read_jsonl(ANSWERS)
    path = EVAL / "verdicts.csv"
    old = {}
    if path.exists():
        with path.open(newline="", encoding="utf-8") as f:
            old = {r["id"]: r for r in csv.DictReader(f)}
    if not RUBRIC.exists():
        RUBRIC.write_text(DEFAULT_RUBRIC, encoding="utf-8")
        print("Wrote a DRAFT rubric to eval/rubric.md: make it yours.", file=sys.stderr)
    rubric = RUBRIC.read_text(encoding="utf-8")
    judge, rows = None, []
    for q in load_questions(None):
        a = answers.get(q["id"])
        if not a:
            continue
        selected = any(q["id"] == s["id"] for s in questions)
        row = {"id": q["id"], "kind": q["kind"], **code_checks(q, a)}
        prev = old.get(q["id"])
        if prev and prev.get("judge_correct") != "" and not (refresh and selected):
            row.update({k: prev[k] for k in ("judge_correct", "judge_supported", "judge_reason")})
        elif selected:
            judge = judge or make_judge()
            row.update(judge_one(judge, rubric, q, a))
            print(f"  judged {q['id']}: correct={row['judge_correct']} supported={row['judge_supported']}", file=sys.stderr)
        else:
            row.update({"judge_correct": "", "judge_supported": "", "judge_reason": ""})
        rows.append(row)
        write_csv(path, rows, FIELDS_VERDICT)
    write_csv(path, rows, FIELDS_VERDICT)
    return rows


FIELDS_VERDICT = ["id", "kind", "refused", "citations_valid", "refusal_ok", "cites_expected", "numbers_ok",
                  "guardrails", "judge_correct", "judge_supported", "judge_reason"]


# --------------------------------------------------------------------------
# Stage 4: report
# --------------------------------------------------------------------------

def stage_report() -> None:
    questions = {q["id"]: q for q in load_questions(None)}
    answers = read_jsonl(ANSWERS)
    with (EVAL / "verdicts.csv").open(newline="", encoding="utf-8") as f:
        verdicts = [r for r in csv.DictReader(f) if r["judge_correct"] != ""]
    if not verdicts:
        print("No verdicts yet; run the judge stage.")
        return
    by_id = {v["id"]: v for v in verdicts}
    lines = ["# Evaluation summary", ""]

    # end to end
    ans = [v for v in verdicts if v["kind"] != "unanswerable"]
    una = [v for v in verdicts if v["kind"] == "unanswerable"]
    correct = sum(int(v["judge_correct"]) for v in ans)
    wrong_refusal = sum(int(v["refused"]) for v in ans)
    unsupported = sum(1 for v in ans if v["judge_supported"] == "0" and not int(v["refused"]))
    made_up = sum(1 for v in una if not int(v["refused"]))
    right_refusal = sum(int(v["refused"]) for v in una)
    lines += [
        "## End to end", "",
        f"- Questions with an answer: correct {pct(correct, len(ans))}; wrong refusals {pct(wrong_refusal, len(ans))}; "
        f"answers with an unsupported claim {pct(unsupported, len(ans))}.",
        f"- Questions without an answer: correct refusals {pct(right_refusal, len(una))}; answered anyway (made up) {pct(made_up, len(una))}.",
        f"- Valid citations in non-refusal answers: {pct(sum(int(v['citations_valid']) for v in verdicts if not int(v['refused'])), sum(1 for v in verdicts if not int(v['refused'])))}.",
        f"- Answers that cite the expected contract(s): {pct(sum(int(v['cites_expected'] or 0) for v in ans), len(ans))}; "
        f"key numbers of the reference present: {pct(sum(int(v['numbers_ok'] or 0) for v in ans), len(ans))}.",
        "",
    ]
    for kind in ("single", "multi"):
        vs = [v for v in ans if v["kind"] == kind]
        if vs:
            lines.append(f"- {kind}: correct {pct(sum(int(v['judge_correct']) for v in vs), len(vs))}")
    guard = [v for v in verdicts if v["guardrails"]]
    lines += ["", f"Guardrails that fired: {len(guard)} questions (" + ", ".join(f"{v['id']}: {v['guardrails']}" for v in guard[:12]) + ")" if guard else "Guardrails that fired: none.", ""]

    # cost
    toks_in = [a["input_tokens"] for a in answers.values()]
    toks_out = [a["output_tokens"] for a in answers.values()]
    secs = [a["seconds"] for a in answers.values()]
    calls = [len(a["trace"]) for a in answers.values()]
    if secs:
        lines += ["## Cost per question (agent only)", "",
                  f"- Tokens: {statistics.mean(toks_in):.0f} in + {statistics.mean(toks_out):.0f} out on average (max {max(toks_in)} in).",
                  f"- Seconds: mean {statistics.mean(secs):.1f}, median {statistics.median(secs):.1f}, max {max(secs):.1f}.",
                  f"- Tool calls: mean {statistics.mean(calls):.1f}. Judge adds about one call per question.", ""]

    # agreement with the human
    lines += ["## Agreement with your grades", ""]
    if HUMAN.exists():
        with HUMAN.open(newline="", encoding="utf-8") as f:
            human = [r for r in csv.DictReader(f) if r.get("correct", "").strip() in ("0", "1")]
        pairs = [(h, by_id[h["id"]]) for h in human if h["id"] in by_id]
        lines.append(f"You graded {len(human)} answers ({len(pairs)} also judged).")
        for field, jfield in (("correct", "judge_correct"), ("supported", "judge_supported")):
            valid = [(h, v) for h, v in pairs if h.get(field, "").strip() in ("0", "1")]
            if valid:
                agree = sum(1 for h, v in valid if h[field].strip() == v[jfield])
                lines.append(f"- {field}: agreement {pct(agree, len(valid))}")
        dis = [(h["id"], h.get("correct"), v["judge_correct"]) for h, v in pairs if h.get("correct", "").strip() != v["judge_correct"]]
        if dis:
            lines.append("- Disagreements on `correct` (id, you, judge): " + "; ".join(f"{i} ({h}/{j})" for i, h, j in dis))
        if len(human) < 20:
            lines.append(f"- WARNING: the brief asks for at least 20 graded answers; you have {len(human)}.")
    else:
        lines.append("eval/human_labels.csv not found.")
    lines.append("")

    # failures
    failures = []
    for qid, v in by_id.items():
        q, a = questions[qid], answers[qid]
        refused = int(v["refused"])
        if q["kind"] == "unanswerable":
            ok = refused and v["judge_correct"] == "1"
            cause = "" if ok else "unsupported claim (answered, should have refused)" if not refused else "judge says the refusal is wrong: check"
        else:
            pairs = expected_pairs(q)
            passages = [p for s in a["trace"] if s["tool"] == "search" for p in parse_search_result(s["result"])]
            found = all_pairs_found(passages, pairs) if passages else False
            if v["judge_correct"] == "1" and v["judge_supported"] != "0":
                cause = ""
            elif not found:
                cause = "retrieval miss"
            elif refused:
                cause = "wrong refusal"
            elif v["judge_supported"] == "0":
                cause = "unsupported claim"
            else:
                cause = "wrong answer from the right passage"
        if cause:
            failures.append({"id": qid, "kind": q["kind"], "question": q["question"], "auto_cause": cause,
                             "judge_reason": v["judge_reason"], "your_cause": "", "your_notes": ""})
    write_csv(EVAL / "failures.csv", failures, ["id", "kind", "question", "auto_cause", "judge_reason", "your_cause", "your_notes"])
    lines += ["## Failures (automatic first guess; confirm each in eval/failures.csv)", ""]
    causes: dict[str, int] = {}
    for fl in failures:
        causes[fl["auto_cause"]] = causes.get(fl["auto_cause"], 0) + 1
    lines += [f"- {c}: {n}" for c, n in sorted(causes.items(), key=lambda x: -x[1])] or ["- none"]
    lines += ["", "Cause list for your own classification: retrieval miss, wrong answer from the right passage, "
              "unsupported claim, wrong refusal, bad test question."]
    retrieval = EVAL / "retrieval.md"
    if retrieval.exists():
        lines += ["", "## Retrieval", "", retrieval.read_text(encoding="utf-8")]
    (EVAL / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


# --------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("stages", nargs="*", choices=["retrieval", "answers", "judge", "report"])
    parser.add_argument("--ids", default="")
    parser.add_argument("--refresh", action="store_true")
    args = parser.parse_args()
    stages = args.stages or ["retrieval", "answers", "judge", "report"]
    ids = [i.strip() for i in args.ids.split(",") if i.strip()]
    questions = load_questions(ids or None)
    if not questions:
        raise SystemExit("No questions found in eval/questions.csv.")
    if "retrieval" in stages:
        stage_retrieval(questions)
    if "answers" in stages:
        stage_answers(questions, args.refresh)
    if "judge" in stages:
        stage_judge(questions, args.refresh)
    if "report" in stages:
        stage_report()


if __name__ == "__main__":
    main()
