"""
Assignment 3: evaluation (`uv run python main.py evaluate`).

1. Retrieval: hit rate at k = 1, 3, 5 for each design (fixed windows vs
   section-aware chunks, each with dense-only and hybrid BM25+dense search),
   plus the words each design adds to the prompt.
2. End to end: the agent (agent.py) answers every question in eval/questions.csv
   on the frozen 3-report corpus (RAG_DOCS), with add_document denied.
3. Code checks: citations valid (point to retrieved pages), expected page cited,
   refusal when it should refuse, no refusal when it should answer.
4. LLM judge (Gemini) with a rubric and the retrieved passages as evidence.
5. Agreement between the judge and eval/human_labels.csv.
6. Failure classes, cost (tokens) and latency per question.
7. Before/after for the added document, if one was added (index registry).

Results are cached in eval/ (answers.jsonl, judge.jsonl) keyed by question,
prompt and model, so a re-run only spends quota on what changed.
EVAL_FRESH=1 ignores the caches.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import sys
import time
from collections import Counter
from pathlib import Path

import index as ix

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
HUMAN = EVAL / "human_labels.csv"
ANSWERS = EVAL / "answers.jsonl"
JUDGE = EVAL / "judge.jsonl"
FRESH = os.environ.get("EVAL_FRESH") == "1"
# A different model from the one that answers, so the judge does not grade its own output.
JUDGE_MODEL = os.environ.get("JUDGE_MODEL", "gemini-3.1-flash-lite")
KS = (1, 3, 5)
BASE_ENV = {"RAG_DOCS": ",".join(ix.BASE_DOC_IDS)}


def log(*a):
    print(*a, flush=True)


def load_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        srcs = [s.strip() for s in r["expected_source"].split(";") if s.strip()]
        locs = [l.strip() for l in r["expected_location"].split(";") if l.strip()]
        r["expected"] = [(s, int(l)) for s, l in zip(srcs, locs)]
    return rows


def covers(hit: dict, doc: str, page: int) -> bool:
    return hit["doc_id"] == doc and hit["page_start"] <= page <= hit["page_end"]


# --------------------------------------------------------------------------- 1. retrieval

def retrieval(questions: list[dict]) -> dict:
    reg = ix.load_registry()
    results = {}
    answerable = [q for q in questions if q["expected"]]
    for design in ix.DESIGNS:
        complete = all(reg.get(d, {}).get("complete", {}).get(design) for d in ix.BASE_DOC_IDS)
        if not complete:
            log(f"  design '{design}': not fully embedded yet, skipped (run main.py index after the quota resets)")
            continue
        for hybrid in (False, True):
            name = f"{design}{'+hybrid' if hybrid else ''}"
            hits_at = {k: 0 for k in KS}
            passage_recall5 = []
            words = []
            per_q = {}
            for q in answerable:
                hits = ix.search(q["question"], k=max(KS), design=design, doc_ids=ix.BASE_DOC_IDS, hybrid=hybrid)
                words.append(sum(h["words"] for h in hits))
                for k in KS:
                    if all(any(covers(h, d, p) for h in hits[:k]) for d, p in q["expected"]):
                        hits_at[k] += 1
                found = [any(covers(h, d, p) for h in hits[:5]) for d, p in q["expected"]]
                passage_recall5.append(sum(found) / len(found))
                per_q[q["id"]] = next((r + 1 for r in range(len(hits)) if all(any(covers(h, d, p) for h in hits[:r + 1]) for d, p in q["expected"])), None)
            n = len(answerable)
            results[name] = {
                **{f"hit@{k}": round(hits_at[k] / n, 3) for k in KS},
                "passage_recall@5": round(sum(passage_recall5) / n, 3),
                "avg_words_in_prompt@5": round(sum(words) / n),
                "chunks": sum(reg[d].get(f"chunks_{design}", 0) for d in ix.BASE_DOC_IDS),
                "rank_of_first_full_hit": per_q,
            }
            log(f"  {name:18s} " + "  ".join(f"hit@{k}={results[name][f'hit@{k}']:.2f}" for k in KS)
                + f"  passages@5={results[name]['passage_recall@5']:.2f}  words@5={results[name]['avg_words_in_prompt@5']}")
    return results


# --------------------------------------------------------------------------- 2. end to end

def _key(*parts) -> str:
    return hashlib.sha1("\x1f".join(map(str, parts)).encode()).hexdigest()[:16]


def _read_jsonl(path: Path) -> dict:
    if FRESH or not path.exists():
        return {}
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            out[r["key"]] = r
    return out


def _append_jsonl(path: Path, row: dict) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def run_agent_on_all(questions: list[dict]) -> dict:
    import agent
    cache = _read_jsonl(ANSWERS)
    if FRESH and ANSWERS.exists():
        ANSWERS.unlink()
    out = {}
    for q in questions:
        key = _key(q["question"], agent.SYSTEM_PROMPT, agent.MODEL, ix.CHOSEN_DESIGN)
        if key in cache and not cache[key].get("error"):
            out[q["id"]] = cache[key]
            continue
        log(f"  {q['id']}: asking the agent ...")
        try:
            r = agent.answer(q["question"], approve=lambda p: False, env=BASE_ENV)
            r.update(key=key, id=q["id"])
        except Exception as e:  # noqa: BLE001 - record and carry on; re-run retries it
            r = {"key": key, "id": q["id"], "question": q["question"], "error": f"{type(e).__name__}: {e}"[:500]}
            log(f"    error: {r['error']}")
        _append_jsonl(ANSWERS, r)
        out[q["id"]] = r
    return out


# --------------------------------------------------------------------------- 3. code checks

def code_checks(q: dict, r: dict) -> dict:
    import agent
    if r.get("error"):
        return {"error": True}
    ans = r["answer"]
    cites = ix.parse_citations(ans)
    retrieved = [c for s in r["trace"] if s["tool"] == "search" for c in ix.parse_citations(s["result"])]
    withheld = ans.startswith("[Answer withheld")
    valid = not agent.check_citations(ans, r["trace"]) and not withheld
    expected_retrieved = all(any(d == rd and ra <= p <= rb for rd, ra, rb in retrieved) for d, p in q["expected"])
    expected_cited = all(any(d == cd and ca - 1 <= p <= cb + 1 for cd, ca, cb in cites) for d, p in q["expected"])
    unanswerable = q["kind"] == "unanswerable"
    refused = agent.is_refusal(ans)  # recomputed, so a fix to the detector applies to cached answers
    return {
        "n_citations": len(cites),
        "citations_valid": valid,
        "withheld": withheld,
        "refused": refused,
        "correct_refusal": unanswerable and refused,
        "missed_refusal": unanswerable and not refused,
        "wrong_refusal": (not unanswerable) and (refused or withheld),
        "expected_retrieved": expected_retrieved if not unanswerable else None,
        "expected_cited": expected_cited if not unanswerable else None,
    }


# --------------------------------------------------------------------------- 4. judge

RUBRIC = """You grade answers from an assistant that helps airline safety analysts write pilot-training
briefings from NTSB accident reports. Grade strictly; a wrong detail in a briefing is costly.

You get: the question, its kind (single / multi / unanswerable), a reference answer written from the
report, the assistant's answer, and the passages the assistant retrieved (its only allowed evidence).

correct (1/0):
- answerable question: 1 if the answer states the key facts of the reference answer without
  contradicting it. Extra true detail is fine. Missing a key element (for a multi question, either
  accident) or any factual error = 0. Calling a contributing factor the probable cause (or the reverse),
  or presenting an NTSB recommendation as a regulation/requirement, = 0.
- unanswerable question: 1 only if the answer clearly says the reports do not cover it and does not
  invent the missing fact. A partial guess = 0.
supported (1/0): 1 if EVERY factual claim in the answer appears in the retrieved passages (paraphrase
is fine). Any claim from outside knowledge, or a number not in the passages, = 0. A pure refusal = 1.
failure (only when correct = 0 or supported = 0), one of:
- retrieval_miss: the passages needed for the reference answer were not retrieved
- wrong_from_right_passage: the needed passage was retrieved but the answer misread or omitted it
- unsupported_claim: the answer adds claims not in the passages
- wrong_refusal: the assistant refused although the passages contained the answer
- bad_question: the reference answer or question itself is wrong or ambiguous
Otherwise failure = "none". Give a one-sentence reason."""


def judge_all(questions: list[dict], answers: dict) -> dict:
    from google import genai
    from google.genai import types
    from pydantic import BaseModel
    from typing import Literal

    class Verdict(BaseModel):
        correct: int
        supported: int
        failure: Literal["none", "retrieval_miss", "wrong_from_right_passage", "unsupported_claim", "wrong_refusal", "bad_question"]
        reason: str

    client = genai.Client(api_key=ix.load_api_key())
    cache = _read_jsonl(JUDGE)
    if FRESH and JUDGE.exists():
        JUDGE.unlink()
    out = {}
    for q in questions:
        r = answers.get(q["id"])
        if not r or r.get("error"):
            continue
        evidence = "\n\n=====\n\n".join(s["result"] for s in r["trace"] if s["tool"] == "search") or "(no passages retrieved)"
        key = _key(r["answer"], q["reference_answer"], RUBRIC, JUDGE_MODEL, evidence)
        if key in cache:
            out[q["id"]] = cache[key]
            continue
        prompt = (f"QUESTION ({q['kind']}): {q['question']}\n\nREFERENCE ANSWER: {q['reference_answer']}\n\n"
                  f"ASSISTANT ANSWER:\n{r['answer']}\n\nRETRIEVED PASSAGES:\n{evidence}")
        for attempt in range(6):
            try:
                resp = client.models.generate_content(
                    model=JUDGE_MODEL, contents=prompt,
                    config=types.GenerateContentConfig(system_instruction=RUBRIC, temperature=0,
                                                       response_mime_type="application/json", response_schema=Verdict))
                v = Verdict.model_validate_json(resp.text).model_dump()
                break
            except Exception as e:  # noqa: BLE001
                if "per day" in str(e) or "PerDay" in str(e):
                    log(f"  judge stopped at {q['id']}: daily quota of {JUDGE_MODEL} used up; re-run after the reset")
                    return out
                if attempt == 5:
                    log(f"  judge failed on {q['id']}: {e}")
                    v = None
                else:
                    time.sleep(15 * (attempt + 1))
        if v is None:
            continue
        v.update(key=key, id=q["id"])
        _append_jsonl(JUDGE, v)
        out[q["id"]] = v
    return out


# --------------------------------------------------------------------------- 5. agreement

def agreement(judged: dict) -> dict:
    if not HUMAN.exists():
        return {"n": 0}
    with HUMAN.open(newline="", encoding="utf-8") as f:
        human = [r for r in csv.DictReader(f) if r.get("id", "").strip() and r.get("correct", "").strip()]
    pairs = {"correct": [], "supported": []}
    disagreements = []
    for h in human:
        j = judged.get(h["id"].strip())
        if not j:
            continue
        for field in pairs:
            hv, jv = int(h[field]), int(j[field])
            pairs[field].append((hv, jv))
            if hv != jv:
                disagreements.append({"id": h["id"], "field": field, "human": hv, "judge": jv, "judge_reason": j["reason"]})
    out = {"n": len(pairs["correct"]), "disagreements": disagreements}
    for field, ps in pairs.items():
        if not ps:
            continue
        agree = sum(a == b for a, b in ps) / len(ps)
        pa = sum(a for a, _ in ps) / len(ps)
        pb = sum(b for _, b in ps) / len(ps)
        pe = pa * pb + (1 - pa) * (1 - pb)
        out[field] = {"agreement": round(agree, 3), "cohen_kappa": round((agree - pe) / (1 - pe), 3) if pe < 1 else None}
    return out


# --------------------------------------------------------------------------- 7. before / after

def before_after() -> dict | None:
    import agent
    reg = ix.load_registry()
    added = [d for d, e in reg.items() if d not in ix.BASE_DOC_IDS and e.get("complete", {}).get(ix.CHOSEN_DESIGN)]
    if not added:
        return None
    path = EVAL / "before_after.json"
    q = next(r for r in load_questions() if r["id"] == "q26")
    if path.exists() and not FRESH:
        old = json.loads(path.read_text())
        if old.get("question") == q["question"] and old.get("added") == added:
            return old
    log(f"  asking {q['id']} without and with {added} ...")
    before = agent.answer(q["question"], approve=lambda p: False, env=BASE_ENV)
    after = agent.answer(q["question"], approve=lambda p: False, env={"RAG_DOCS": ""})
    out = {"id": q["id"], "question": q["question"], "added": added,
           "before": {"answer": before["answer"], "refused": before["refused"]},
           "after": {"answer": after["answer"], "refused": after["refused"]}}
    path.write_text(json.dumps(out, indent=2, ensure_ascii=False))
    return out


# --------------------------------------------------------------------------- main

def main() -> int:
    EVAL.mkdir(exist_ok=True)
    questions = load_questions()
    log("== 1. Retrieval hit rate")
    ret = retrieval(questions)

    log("== 2. Agent answers")
    answers = run_agent_on_all(questions)

    log("== 3. Code checks")
    checks = {q["id"]: code_checks(q, answers[q["id"]]) for q in questions}

    log("== 4. LLM judge")
    judged = judge_all(questions, answers)

    log("== 5. Agreement with human labels")
    agree = agreement(judged)

    log("== 7. Before/after the added document")
    ba = before_after()

    # results table
    rows = []
    for q in questions:
        r, c, j = answers[q["id"]], checks[q["id"]], judged.get(q["id"], {})
        rows.append({
            "id": q["id"], "kind": q["kind"],
            "correct": j.get("correct", ""), "supported": j.get("supported", ""), "failure": j.get("failure", ""),
            "refused": c.get("refused", ""), "citations_valid": c.get("citations_valid", ""),
            "expected_retrieved": c.get("expected_retrieved", ""), "expected_cited": c.get("expected_cited", ""),
            "guardrail_fired": (r.get("guardrail") or {}).get("fired", ""),
            "tool_calls": r.get("tool_calls", ""), "input_tokens": r.get("input_tokens", ""),
            "output_tokens": r.get("output_tokens", ""), "seconds": r.get("seconds", ""),
            "judge_reason": j.get("reason", ""), "error": r.get("error", ""),
        })
    with (EVAL / "results.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    # A sheet for grading by hand, WITHOUT the judge's verdicts (grade before reading them).
    with (EVAL / "to_grade.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "kind", "question", "reference_answer", "agent_answer", "retrieved_citations"])
        for q in questions:
            r = answers[q["id"]]
            tags = sorted({f"{d} p.{a}-{b}" for s in r.get("trace", []) if s["tool"] == "search" for d, a, b in ix.parse_citations(s["result"])})
            w.writerow([q["id"], q["kind"], q["question"], q["reference_answer"], r.get("answer", r.get("error")), "; ".join(tags)])

    ok = [r for r in rows if r["correct"] != ""]
    answerable = [r for r in ok if r["kind"] != "unanswerable"]
    unans = [r for r in ok if r["kind"] == "unanswerable"]
    done = [answers[q["id"]] for q in questions if not answers[q["id"]].get("error")]
    summary = {
        "model": done[0]["model"] if done else None, "judge_model": JUDGE_MODEL, "design": ix.CHOSEN_DESIGN,
        "questions": len(questions), "answered_without_error": len(done), "judged": len(ok),
        "retrieval": {k: {m: v for m, v in d.items() if m != "rank_of_first_full_hit"} for k, d in ret.items()},
        "end_to_end": {
            "correct": sum(int(r["correct"]) for r in ok),
            "correct_rate": round(sum(int(r["correct"]) for r in ok) / max(len(ok), 1), 3),
            "answerable_correct": f"{sum(int(r['correct']) for r in answerable)}/{len(answerable)}",
            "unsupported": sum(1 - int(r["supported"]) for r in ok),
            "correct_refusals": f"{sum(1 for r in unans if r['refused'] is True)}/{len(unans)}",
            "wrong_refusals": sum(1 for r in answerable if checks[r['id']].get('wrong_refusal')),
            "citations_valid": f"{sum(1 for r in rows if r['citations_valid'] is True)}/{len(rows)}",
            "expected_page_cited": f"{sum(1 for r in rows if r['expected_cited'] is True)}/{sum(1 for r in rows if r['kind'] != 'unanswerable')}",
            "guardrail_fired": sum(1 for r in rows if r["guardrail_fired"] is True),
        },
        "failures": dict(Counter(r["failure"] for r in ok if r["failure"] not in ("", "none"))),
        "judge_vs_human": agree,
        "cost_per_question": {
            "input_tokens": round(sum(a["input_tokens"] for a in done) / max(len(done), 1)),
            "output_tokens": round(sum(a["output_tokens"] for a in done) / max(len(done), 1)),
            "seconds": round(sum(a["seconds"] for a in done) / max(len(done), 1), 1),
            "tool_calls": round(sum(a["tool_calls"] for a in done) / max(len(done), 1), 1),
        },
        "before_after": ba,
    }
    (EVAL / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    log("\n== Summary")
    log(json.dumps({k: v for k, v in summary.items() if k != "before_after"}, indent=2))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
