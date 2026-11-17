"""
Assignment 3: evaluation (`main.py evaluate`).

1. Retrieval: hit rate at k = 1, 3, 5 for each design (fixed vs section chunks, dense vs hybrid),
   and the words each design adds to the prompt at k = 5.             -> eval/retrieval.csv
2. End to end: the agent answers every question (original corpus only). -> eval/answers.jsonl
3. Code checks: refusal vs expected, citations valid / present / from the expected paper,
   retrieval hit for the agent's own searches.
4. LLM judge with a rubric and the retrieved text as evidence.          -> eval/judge.jsonl
5. Agreement with eval/human_labels.csv (your own grades).
6. Failure causes and cost (tokens, seconds).                          -> eval/results.csv, eval/summary.md

Every API result is cached in eval/, so a crash or the daily quota loses nothing: run it again
and it continues where it stopped. Delete a cache file to redo that stage.
"""

from __future__ import annotations

import asyncio
import csv
import json
import os
import re
import sys
import time
from pathlib import Path

import rag
from agent import REFUSAL, CorpusAgent, check_grounding, citations_in, retrieved_passages

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
HUMAN = EVAL / "human_labels.csv"
OVERRIDES = EVAL / "failure_overrides.csv"
ANSWERS = EVAL / "answers.jsonl"
JUDGE = EVAL / "judge.jsonl"
JUDGE_MODEL = os.environ.get("JUDGE_MODEL", os.environ.get("GEMINI_MODEL", "gemini-flash-lite-latest"))
SLEEP = float(os.environ.get("EVAL_SLEEP", "4"))   # seconds between agent questions (free-tier RPM)
KS = (1, 3, 5)


# --------------------------------------------------------------------------- helpers

def load_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r["question"].strip()]


def expected_passages(q: dict) -> list[tuple[str, list[tuple[int, int]]]]:
    """One entry per expected passage: (doc, [page ranges where that passage's fact is stated]).

    'munoz2022;dahmen2023' + 'p.5;p.1|p.6' -> [(munoz2022, [(5,5)]), (dahmen2023, [(1,1), (6,6)])].
    `|` lists alternative pages for the same fact (e.g. stated in the abstract and in the results).
    """
    sources = [s.strip() for s in q["expected_source"].split(";") if s.strip()]
    locs = [l.strip() for l in q["expected_location"].split(";") if l.strip()]
    out = []
    for i, src in enumerate(sources):
        loc = locs[i] if i < len(locs) else (locs[-1] if locs else "")
        ranges = []
        for alt in loc.split("|"):
            m = re.search(r"(\d+)(?:\s*-\s*(\d+))?", alt)
            if m:
                ranges.append((int(m.group(1)), int(m.group(2) or m.group(1))))
        out.append((src, ranges or [(0, 10_000)]))
    return out


def matches(doc: str, p0: int, p1: int, expected) -> list[int]:
    """Indices of expected passages that this chunk (doc, pages p0-p1) covers."""
    return [i for i, (d, ranges) in enumerate(expected)
            if d == doc and any(p0 <= e1 and e0 <= p1 for e0, e1 in ranges)]


def read_jsonl(path: Path) -> dict[str, dict]:
    if not path.is_file():
        return {}
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            out[r["id"]] = r
    return out


def append_jsonl(path: Path, record: dict) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


# --------------------------------------------------------------------------- 1. retrieval

def evaluate_retrieval(questions: list[dict]) -> list[dict]:
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    print(f"\n== Retrieval: {len(answerable)} answerable questions (query embeddings cached in index/)")
    qvecs = {q["id"]: rag.embed_query(q["question"]) for q in answerable}
    rows, details = [], []
    for design in rag.DESIGNS:
        searcher = rag.Searcher(design, corpus_only=True)
        for hybrid in (False, True):
            name = f"{design}+{'hybrid' if hybrid else 'dense'}"
            hits = {k: 0 for k in KS}
            all5_multi, n_multi, words = 0, 0, []
            for q in answerable:
                exp = expected_passages(q)
                res = searcher.search(q["question"], k=max(KS), hybrid=hybrid, qvec=qvecs[q["id"]])
                covered_at = []
                for rank, r in enumerate(res, 1):
                    for i in matches(r["doc_id"], r["page_start"], r["page_end"], exp):
                        covered_at.append((rank, i))
                first = min((rank for rank, _ in covered_at), default=None)
                for k in KS:
                    hits[k] += int(first is not None and first <= k)
                if q["kind"] == "multi":
                    n_multi += 1
                    all5_multi += int(len({i for _, i in covered_at}) == len(exp))
                words.append(sum(len(r["text"].split()) for r in res))
                details.append({"design": name, "id": q["id"], "kind": q["kind"], "first_hit_rank": first or "",
                                "top5": " | ".join(f"{r['doc_id']} p.{r['page_start']}-{r['page_end']}" for r in res)})
            n = len(answerable)
            rows.append({
                "design": name, "chunks": len(searcher.ids),
                **{f"hit@{k}": round(hits[k] / n, 3) for k in KS},
                "multi_all@5": round(all5_multi / n_multi, 3) if n_multi else "",
                "words_in_prompt@5": round(sum(words) / len(words)),
            })
    write_csv(EVAL / "retrieval.csv", rows)
    best = max(rows, key=lambda r: (r["hit@5"], r["hit@1"], -r["words_in_prompt@5"]))
    design, method = best["design"].split("+")
    choice = {"design": design, "hybrid": method == "hybrid", "k": 5, "chosen_by": "evaluate.py: max hit@5, then hit@1, then fewest words"}
    rag.PRODUCTION_FILE.write_text(json.dumps(choice, indent=2), encoding="utf-8")
    rag.PRODUCTION.update(choice)
    print(f"  -> production design: {best['design']} (saved in index/production.json)")
    write_csv(EVAL / "retrieval_details.csv", details)
    for r in rows:
        print("  " + "  ".join(f"{k}={v}" for k, v in r.items()))
    return rows


# --------------------------------------------------------------------------- 2. answers

async def run_answers(questions: list[dict]) -> dict[str, dict]:
    done = read_jsonl(ANSWERS)
    todo = [q for q in questions if q["id"] not in done]
    print(f"\n== Agent answers: {len(done)} cached, {len(todo)} to run (model {os.environ.get('GEMINI_MODEL', 'default')})")
    if todo:
        async with CorpusAgent(corpus_only=True, approve=lambda name, args: False) as agent:
            for q in todo:
                try:
                    r = await agent.ask(q["question"])
                except Exception as error:  # noqa: BLE001
                    msg = str(error)
                    if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
                        print(f"  quota reached at {q['id']}; run `main.py evaluate` again later to continue.")
                        break
                    raise
                r["id"] = q["id"]
                append_jsonl(ANSWERS, r)
                done[q["id"]] = r
                flag = "REFUSED " if r["refused"] else ""
                print(f"  {q['id']} {flag}{r['seconds']}s {r['input_tokens']}+{r['output_tokens']} tok :: {r['answer'][:90]!r}")
                time.sleep(SLEEP)
    return done


# --------------------------------------------------------------------------- 3. code checks

def code_checks(q: dict, a: dict) -> dict:
    exp = expected_passages(q) if q["kind"] != "unanswerable" else []
    retrieved = retrieved_passages(a["retrieved"])
    cites = citations_in(a["answer"])
    expected_docs = {d for d, _ in exp}
    return {
        "refused": int(a["refused"]),
        "refusal_ok": int(a["refused"] == (q["kind"] == "unanswerable")),
        "has_citation": int(bool(cites)),
        "citations_valid": int(check_grounding(a["answer"], a["retrieved"]) is None),
        "cites_expected_doc": int(any(d in expected_docs for d, _, _ in cites)) if exp else "",
        "retrieval_hit": int(any(matches(d, p0, p1, exp) for d, p0, p1 in retrieved)) if exp else "",
        "guardrail_fired": int(any(e["event"] == "citation_guardrail" for e in a["events"])),
        "searches": sum(1 for t in a["trace"] if t["tool"] == "search"),
    }


# --------------------------------------------------------------------------- 4. judge

RUBRIC = f"""You grade answers from a padel research assistant that must answer ONLY from retrieved passages.

You get: the question, its kind (single / multi / unanswerable), the reference answer written by the
test author, the passages the assistant retrieved, and the assistant's answer.

correct (1 or 0):
- kind single or multi: 1 if the answer states the key facts of the reference answer (numbers must match
  exactly; wording may differ) and contains nothing that contradicts it. For multi, BOTH parts must be
  answered. A refusal ("{REFUSAL}") is 0. Extra correct detail is fine.
- kind unanswerable: 1 if the assistant refuses or clearly says the corpus does not contain this,
  without inventing the missing fact. 0 if it gives an answer to the question.

supported (1 or 0):
- 1 if every factual claim in the answer is stated in (or directly follows from) the retrieved passages.
  0 if any claim, number or recommendation is not in the passages, even if it is true in the real world.
- A plain refusal is supported (1). Citation tags themselves are not claims.

Be strict about numbers and about turning an association into a cause.
Return JSON: {{"correct": 0 or 1, "supported": 0 or 1, "reason": "<one sentence>"}}"""


JUDGE_FALLBACKS = [JUDGE_MODEL, "gemini-2.5-flash-lite", "gemini-flash-latest", "gemini-2.5-flash"]


def _parse_verdict(text: str) -> dict:
    """Read the judge's JSON, tolerating ```json fences or text around it."""
    m = re.search(r"\{.*\}", text or "", re.S)
    if not m:
        raise ValueError(f"no JSON in judge reply: {text[:200]!r}")
    v = json.loads(m.group(0))
    return {"correct": int(v["correct"]), "supported": int(v["supported"]), "reason": str(v.get("reason", ""))}


def judge_one(q: dict, a: dict) -> dict:
    from google.genai import types

    evidence = "\n\n".join(a["retrieved"])[:30_000] or "(nothing retrieved)"
    prompt = (f"{RUBRIC}\n\n---\nQUESTION: {q['question']}\nKIND: {q['kind']}\n"
              f"REFERENCE ANSWER: {q['reference_answer']}\n\nRETRIEVED PASSAGES:\n{evidence}\n\n"
              f"ASSISTANT ANSWER:\n{a['answer']}\n\nReply with the JSON object only.")
    last_error = None
    for model in dict.fromkeys(JUDGE_FALLBACKS):          # unique, in order
        for attempt in range(4):
            try:
                resp = rag.client().models.generate_content(
                    model=model, contents=prompt,
                    config=types.GenerateContentConfig(temperature=0, response_mime_type="application/json"))
                v = _parse_verdict(resp.text)
                u = resp.usage_metadata
                v["judge_tokens"] = ((u.prompt_token_count or 0) + (u.candidates_token_count or 0)) if u else 0
                v["judge_model"] = model
                return v
            except Exception as error:  # noqa: BLE001
                last_error = error
                msg = str(error)
                if "404" in msg or "NOT_FOUND" in msg:
                    break                                   # model not available: try the next one
                delay = rag._retry_delay(error) or 20 * (attempt + 1)
                print(f"  judge {model}: {type(error).__name__}, waiting {delay:.0f}s")
                time.sleep(delay)
        print(f"  judge: giving up on {model}, trying the next model")
    raise RuntimeError(f"judge kept failing: {last_error}")


def run_judge(questions: list[dict], answers: dict) -> dict[str, dict]:
    done = read_jsonl(JUDGE)
    todo = [q for q in questions if q["id"] in answers and q["id"] not in done]
    print(f"\n== LLM judge ({JUDGE_MODEL}): {len(done)} cached, {len(todo)} to grade")
    for q in todo:
        try:
            v = judge_one(q, answers[q["id"]])
        except RuntimeError:
            print("  judge stopped (quota?); run again later to continue.")
            break
        v["id"] = q["id"]
        append_jsonl(JUDGE, v)
        done[q["id"]] = v
        time.sleep(1)
    return done


# --------------------------------------------------------------------------- 5. human agreement

def human_agreement(judged: dict) -> dict:
    if not HUMAN.is_file():
        return {}
    with HUMAN.open(newline="", encoding="utf-8") as f:
        human = {r["id"]: r for r in csv.DictReader(f) if r.get("id", "").strip() and r.get("correct", "").strip()}
    both = [i for i in human if i in judged]
    out = {"n": len(both)}
    for field in ("correct", "supported"):
        pairs = [(int(human[i][field]), judged[i][field]) for i in both if human[i].get(field, "").strip()]
        if not pairs:
            continue
        agree = sum(h == j for h, j in pairs) / len(pairs)
        ph = sum(h for h, _ in pairs) / len(pairs)
        pj = sum(j for _, j in pairs) / len(pairs)
        pe = ph * pj + (1 - ph) * (1 - pj)
        kappa = (agree - pe) / (1 - pe) if pe < 1 else 1.0
        out[field] = {"agreement": round(agree, 3), "kappa": round(kappa, 3), "n": len(pairs),
                      "disagreements": [i for i in both if human[i].get(field, "").strip()
                                        and int(human[i][field]) != judged[i][field]]}
    return out


def write_grading_sheet(questions: list[dict], answers: dict) -> None:
    """A sheet for grading by hand WITHOUT the judge's verdicts (fill eval/human_labels.csv from it)."""
    rows = []
    for q in questions:
        a = answers.get(q["id"])
        if a:
            rows.append({"id": q["id"], "kind": q["kind"], "question": q["question"],
                         "reference_answer": q["reference_answer"], "agent_answer": a["answer"],
                         "retrieved_passages": " || ".join(t.replace("\n", " ")[:1500] for t in a["retrieved"])})
    write_csv(EVAL / "grading_sheet.csv", rows)


# --------------------------------------------------------------------------- 6. failures & summary

def failure_cause(q: dict, c: dict, j: dict | None) -> str:
    if j is None:
        return "not judged"
    if q["kind"] == "unanswerable":
        if c["refused"]:
            return "" if j["supported"] else "unsupported claim"
        return "unsupported claim"          # answered a question the corpus cannot answer
    if c["refused"]:
        return "retrieval miss" if not c["retrieval_hit"] else "wrong refusal"
    if j["correct"] and j["supported"]:
        return ""
    if not c["retrieval_hit"]:
        return "retrieval miss"
    if not j["supported"]:
        return "unsupported claim"
    return "wrong answer from right passage"


def main() -> None:
    questions = load_questions()
    print(f"{len(questions)} questions: " + ", ".join(
        f"{k}={sum(q['kind'] == k for q in questions)}" for k in ("single", "multi", "unanswerable")))
    retrieval = evaluate_retrieval(questions)
    answers = asyncio.run(run_answers(questions))
    write_grading_sheet(questions, answers)
    judged = run_judge(questions, answers)

    overrides = {}
    if OVERRIDES.is_file():
        with OVERRIDES.open(newline="", encoding="utf-8") as f:
            overrides = {r["id"]: r for r in csv.DictReader(f)}

    rows = []
    for q in questions:
        a = answers.get(q["id"])
        if not a:
            continue
        c = code_checks(q, a)
        j = judged.get(q["id"])
        cause = failure_cause(q, c, j)
        if q["id"] in overrides:
            cause = overrides[q["id"]]["cause"]
        rows.append({
            "id": q["id"], "kind": q["kind"], "question": q["question"], "answer": a["answer"],
            **c,
            "judge_correct": j["correct"] if j else "", "judge_supported": j["supported"] if j else "",
            "judge_reason": j["reason"] if j else "",
            "failure_cause": cause,
            "input_tokens": a["input_tokens"], "output_tokens": a["output_tokens"],
            "model_calls": a["model_calls"], "seconds": a["seconds"],
        })
    write_csv(EVAL / "results.csv", rows)
    agreement = human_agreement(judged)

    ans = [r for r in rows if r["kind"] != "unanswerable"]
    una = [r for r in rows if r["kind"] == "unanswerable"]
    jr = [r for r in rows if r["judge_correct"] != ""]
    n = len(rows) or 1
    causes: dict[str, int] = {}
    for r in rows:
        if r["failure_cause"]:
            causes[r["failure_cause"]] = causes.get(r["failure_cause"], 0) + 1
    summary = {
        "questions_answered": len(rows),
        "correct_answers": sum(1 for r in ans if r["judge_correct"] == 1),
        "answerable": len(ans),
        "unsupported_answers": sum(1 for r in jr if not r["refused"] and r["judge_supported"] == 0),
        "correct_refusals": sum(r["refused"] for r in una),
        "unanswerable": len(una),
        "wrong_refusals": sum(r["refused"] for r in ans),
        "answered_unanswerable": sum(1 - r["refused"] for r in una),
        "citations_valid_rate": round(sum(r["citations_valid"] for r in rows) / n, 3),
        "guardrail_fired": sum(r["guardrail_fired"] for r in rows),
        "judge_correct_rate": round(sum(r["judge_correct"] for r in jr) / len(jr), 3) if jr else None,
        "judge_supported_rate": round(sum(r["judge_supported"] for r in jr) / len(jr), 3) if jr else None,
        "avg_input_tokens": round(sum(r["input_tokens"] for r in rows) / n),
        "avg_output_tokens": round(sum(r["output_tokens"] for r in rows) / n),
        "avg_model_calls": round(sum(r["model_calls"] for r in rows) / n, 2),
        "avg_seconds": round(sum(r["seconds"] for r in rows) / n, 1),
        "max_seconds": max((r["seconds"] for r in rows), default=0),
        "failure_causes": causes,
        "human_vs_judge": agreement,
        "retrieval": retrieval,
        "production_design": rag.PRODUCTION,
    }
    (EVAL / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    lines = ["# Evaluation summary", "", "## Retrieval (answerable questions, original corpus)", "",
             "| design | chunks | hit@1 | hit@3 | hit@5 | multi: both passages @5 | words in prompt @5 |",
             "|---|---|---|---|---|---|---|"]
    lines += [f"| {r['design']} | {r['chunks']} | {r['hit@1']} | {r['hit@3']} | {r['hit@5']} | {r['multi_all@5']} | {r['words_in_prompt@5']} |"
              for r in retrieval]
    lines += ["", "## End to end", "",
              f"- Correct answers (judge): {summary['correct_answers']}/{summary['answerable']} answerable",
              f"- Unsupported answers (judge): {summary['unsupported_answers']}",
              f"- Correct refusals: {summary['correct_refusals']}/{summary['unanswerable']} unanswerable",
              f"- Wrong refusals: {summary['wrong_refusals']}/{summary['answerable']} answerable",
              f"- Valid citations (code check): {summary['citations_valid_rate']:.0%} of answers",
              f"- Citation guardrail fired on {summary['guardrail_fired']} questions",
              f"- Cost per question: {summary['avg_input_tokens']} input + {summary['avg_output_tokens']} output tokens, "
              f"{summary['avg_model_calls']} model calls, {summary['avg_seconds']} s on average (max {summary['max_seconds']} s)",
              "", "## Failures by cause", ""]
    lines += [f"- {k}: {v}" for k, v in sorted(causes.items(), key=lambda kv: -kv[1])] or ["- none"]
    lines += ["", "## Judge vs human", ""]
    if agreement.get("n"):
        for field in ("correct", "supported"):
            if field in agreement:
                a = agreement[field]
                lines.append(f"- {field}: {a['agreement']:.0%} agreement, Cohen's kappa {a['kappa']} "
                             f"(n={a['n']}; disagreements: {', '.join(a['disagreements']) or 'none'})")
    else:
        lines.append("- No human labels yet: grade eval/grading_sheet.csv into eval/human_labels.csv and run again.")
    (EVAL / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n" + "\n".join(lines))


if __name__ == "__main__":
    # Windows consoles (cp1252) can't print characters like "≥" or "χ" from the papers: replace them instead of crashing.
    for _stream in (sys.stdout, sys.stderr):
        try:
            _stream.reconfigure(errors="replace")
        except AttributeError:
            pass
    main()
