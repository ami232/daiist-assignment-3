"""
Assignment 3: evaluation (`main.py evaluate`).

1. Retrieval: hit rate at k = 1, 3, 5 for each design (chunking x search method).
2. End to end: the agent answers every question in eval/questions.csv.
3. Code checks: refusals, valid citations, expected passage cited.
4. LLM judge with a rubric, with the retrieved text as evidence.
5. Agreement between the judge and eval/human_labels.csv.
6. Failures, classified, and cost per question.

Everything is written to eval/. Agent answers are cached in eval/answers.jsonl
(keyed by question, model, AGENTS.md and index); set RAG_EVAL_FRESH=1 to rerun them.

Grade your 20+ answers from eval/answers.csv BEFORE you open eval/judge_verdicts.csv.
"""

from __future__ import annotations

import asyncio
import csv
import hashlib
import json
import os
import re
import statistics
import sys
import time
from pathlib import Path

import numpy as np

import agent
import index as ix
import retrieval as rt

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
HUMAN = EVAL / "human_labels.csv"
KS = (1, 3, 5)
DESIGN_GRID = [("fixed", "vector"), ("article", "vector"), ("article", "hybrid"), ("fixed", "hybrid")]
# RAG_JUDGE_MODEL may list several models separated by commas: each one has its own daily quota, and the next is used when one runs out.
_env_judges = [m.strip() for m in os.environ.get("RAG_JUDGE_MODEL", "").split(",") if m.strip()]
JUDGE_MODELS = list(dict.fromkeys([*_env_judges, "gemini-3.8-flash", agent.AGENT_MODEL]))


# ------------------------------------------------------------------ inputs ---
def read_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if (r.get("question") or "").strip()]
    for r in rows:
        r["kind"] = r["kind"].strip().lower()
    return rows


def expected_passages(row: dict) -> list[tuple[str, str]]:
    """[(source, location)] the question needs. Several sources / locations are separated by ';'."""
    sources = [s.strip() for s in row["expected_source"].split(";") if s.strip()]
    locations = [l.strip() for l in row["expected_location"].split(";")]
    if not sources:
        return []
    if len(sources) == 1 and len(locations) > 1:
        sources = sources * len(locations)
    locations = (locations + [""] * len(sources))[: len(sources)]
    return list(zip(sources, locations))


def matches(chunk: dict, passage: tuple[str, str]) -> bool:
    source, location = passage
    if rt.norm_source(chunk["source"]) != rt.norm_source(source) and not rt.norm_source(chunk["source"]).startswith(rt.norm_source(source)):
        return False
    return not location or rt.unit_of(location) in rt.units_of(chunk)


def write_csv(path: Path, rows: list[dict], columns: list[str] | None = None) -> None:
    columns = columns or (list(rows[0]) if rows else [])
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=columns, extrasaction="ignore")
        w.writeheader()
        w.writerows(rows)


def pct(n: float, d: float) -> str:
    return f"{100 * n / d:.0f}%" if d else "n/a"


# --------------------------------------------------------------- retrieval ---
def evaluate_retrieval(questions: list[dict]) -> list[dict]:
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    unanswerable = [q for q in questions if q["kind"] == "unanswerable"]
    vectors = {q["id"]: rt.embed_query(q["question"]) for q in questions}  # cached; shared by all designs
    summary, per_question = [], []
    for design, mode in DESIGN_GRID:
        view = rt.IndexView(design)
        if not len(view):
            print(f"  (skipping {design}/{mode}: no vectors for design '{design}')")
            continue
        hit = {k: {"single": [], "multi_all": [], "multi_any": []} for k in KS}
        words, top1_ans, top1_unans = [], [], []
        for q in answerable:
            wanted = expected_passages(q)
            hits = view.search(q["question"], k=max(KS), mode=mode, query_vector=vectors[q["id"]])
            top1_ans.append(hits[0]["similarity"] if hits else 0.0)
            words.append(sum(h["words"] for h in hits[:5]))
            first_rank = next((h["rank"] for h in hits if any(matches(h, p) for p in wanted)), None)
            row = {"id": q["id"], "kind": q["kind"], "design": design, "mode": mode, "first_hit_rank": first_rank or ""}
            for k in KS:
                covered = [any(matches(h, p) for h in hits[:k]) for p in wanted]
                if q["kind"] == "multi":
                    hit[k]["multi_all"].append(all(covered))
                    hit[k]["multi_any"].append(any(covered))
                else:
                    hit[k]["single"].append(any(covered))
                row[f"hit@{k}"] = int(all(covered)) if q["kind"] == "multi" else int(any(covered))
            per_question.append(row)
        for q in unanswerable:
            hits = view.search(q["question"], k=1, mode="vector", query_vector=vectors[q["id"]])
            top1_unans.append(hits[0]["similarity"] if hits else 0.0)
        rec = {"design": design, "mode": mode, "chunks": len(view), "avg_words_top5": round(float(np.mean(words))) if words else 0,
               "top1_sim_answerable": round(float(np.mean(top1_ans)), 3) if top1_ans else "",
               "top1_sim_unanswerable": round(float(np.mean(top1_unans)), 3) if top1_unans else ""}
        for k in KS:
            single, multi_all, multi_any = hit[k]["single"], hit[k]["multi_all"], hit[k]["multi_any"]
            allq = single + multi_all
            rec[f"hit@{k}"] = round(sum(allq) / len(allq), 3) if allq else 0
            rec[f"single@{k}"] = round(sum(single) / len(single), 3) if single else ""
            rec[f"multi_all@{k}"] = round(sum(multi_all) / len(multi_all), 3) if multi_all else ""
            rec[f"multi_any@{k}"] = round(sum(multi_any) / len(multi_any), 3) if multi_any else ""
        summary.append(rec)
    write_csv(EVAL / "retrieval_results.csv", summary)
    write_csv(EVAL / "retrieval_per_question.csv", per_question)
    print("\nRetrieval (answerable questions; multi counts only when ALL its passages are in the top k)")
    print(f"{'design':<9}{'search':<8}{'chunks':>7}{'hit@1':>8}{'hit@3':>8}{'hit@5':>8}{'multi all@5':>13}{'words/top5':>12}")
    for r in summary:
        print(f"{r['design']:<9}{r['mode']:<8}{r['chunks']:>7}{r['hit@1']:>8.2f}{r['hit@3']:>8.2f}{r['hit@5']:>8.2f}{str(r['multi_all@5']):>13}{r['avg_words_top5']:>12}")
    if summary:
        best = max(summary, key=lambda r: (r["hit@5"], r["hit@3"], r["hit@1"], -r["avg_words_top5"]))
        print(f"Best by hit rate: {best['design']}/{best['mode']}. In use: {ix.CHOSEN_DESIGN}/{rt.CHOSEN_MODE} "
              f"(set CHOSEN_DESIGN in index.py and CHOSEN_MODE in retrieval.py to change it).")
    return summary


# ------------------------------------------------------------- end to end ---
def _fingerprint(question: str) -> str:
    manifest = (ix.INDEX_DIR / "manifest.json")
    parts = [question, agent.AGENT_MODEL, (ROOT / "AGENTS.md").read_text(encoding="utf-8"), ix.CHOSEN_DESIGN, rt.CHOSEN_MODE,
             manifest.read_text(encoding="utf-8") if manifest.is_file() else ""]
    return hashlib.sha1("\x1f".join(parts).encode()).hexdigest()


def run_agent_on_all(questions: list[dict]) -> dict[str, dict]:
    path = EVAL / "answers.jsonl"
    cache: dict[str, dict] = {}
    if path.is_file() and not os.environ.get("RAG_EVAL_FRESH"):
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rec = json.loads(line)
                cache[rec["id"]] = rec
    out: dict[str, dict] = {}
    for n, q in enumerate(questions, 1):
        fp = _fingerprint(q["question"])
        if q["id"] in cache and cache[q["id"]].get("fingerprint") == fp and not cache[q["id"]].get("error"):
            out[q["id"]] = cache[q["id"]]
            continue
        print(f"  [{n}/{len(questions)}] {q['id']}: {q['question'][:70]}", file=sys.stderr)
        result = asyncio.run(agent.run_agent(q["question"], approve=agent.deny_all))
        out[q["id"]] = {"id": q["id"], "fingerprint": fp, **result.as_dict()}
        with path.open("w", encoding="utf-8") as f:  # saved after every question
            for rec in (out | {k: v for k, v in cache.items() if k not in out}).values():
                f.write(json.dumps(rec, ensure_ascii=False) + "\n")
    with path.open("w", encoding="utf-8") as f:
        for q in questions:
            f.write(json.dumps(out[q["id"]], ensure_ascii=False) + "\n")
    return out


# ------------------------------------------------------------- code checks ---
def code_checks(q: dict, a: dict) -> dict:
    wanted = expected_passages(q)
    cites = a["citations"]
    retrieved = a["retrieved"]
    cited_ok = [any(rt.norm_source(c[0]) == rt.norm_source(p[0]) and (not p[1] or rt.unit_of(c[1]) == rt.unit_of(p[1])) for c in cites) for p in wanted]
    retrieved_ok = [any(matches(h, p) for h in retrieved) for p in wanted]
    unanswerable = q["kind"] == "unanswerable"
    if a["blocked"]:
        outcome = "blocked"
    elif a["refused"]:
        outcome = "correct_refusal" if unanswerable else "wrong_refusal"
    else:
        outcome = "answered_unanswerable" if unanswerable else "answered"
    return {
        "outcome": outcome,
        "citations_valid": int(not a["invalid_citations"] and (bool(cites) or a["refused"] or a["blocked"])),
        "n_citations": len(cites),
        "expected_cited_all": int(all(cited_ok)) if wanted else "",
        "expected_retrieved_all": int(all(retrieved_ok)) if wanted else "",
        "expected_retrieved_any": int(any(retrieved_ok)) if wanted else "",
    }


# ------------------------------------------------------------------- judge ---
RUBRIC = """You are grading an assistant's answer to a question about EU legislation.

Question type: {kind}
  single       = answered by one passage
  multi        = needs two passages
  unanswerable = the corpus does NOT answer it; the right behaviour is to say so

Question: {question}
Reference answer: {reference}
Passages the reference comes from: {where}

Evidence: the passages the assistant retrieved (its only source of information):
{evidence}

Assistant's answer:
{answer}

Rubric (be strict, grade the content, not the style):
correct (0 or 1)
  1 only if the answer gives the same substantive content as the reference: same rule, same numbers, deadlines and conditions, nothing essential missing (for a multi question, BOTH parts are present).
  0 if it contradicts the reference, leaves out an essential element, or answers confidently a question that is unanswerable.
  Extra detail that is true and relevant does not lower the grade.
supported (0 or 1)
  1 only if EVERY factual claim in the answer (numbers, conditions, actors, article references) is stated in the evidence passages above.
  0 if any claim is not in them, even if it happens to be true. A citation does not make a claim supported.

Reply with JSON only: {{"correct": 0 or 1, "supported": 0 or 1, "reason": "one sentence"}}"""


def _evidence(retrieved: list[dict], limit_words: int = 7000) -> str:
    seen, parts, total = set(), [], 0
    for h in retrieved:
        key = (h["source"], h["location"])
        if key in seen:
            continue
        seen.add(key)
        words = len(h["body"].split())
        if total + words > limit_words:
            break
        total += words
        parts.append(f"[{h['source']} | {h['location']}]\n{h['body']}")
    return "\n\n".join(parts) or "(the assistant retrieved nothing)"


_judge_models: dict = {}
_dead_judges: set = set()   # judge models that cannot be used in this run (not found, or quota used up)
JUDGE_CACHE = EVAL / "judge_cache.json"   # judge replies already paid for; a rerun never asks twice


def _load_judge_cache() -> dict:
    try:
        return json.loads(JUDGE_CACHE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def _judge_call(prompt: str) -> str:
    from langchain_google_genai import ChatGoogleGenerativeAI

    from api_key import load_api_key

    key = hashlib.sha1(prompt.encode("utf-8")).hexdigest()
    cache = _load_judge_cache()
    # older caches were keyed by (first judge model | prompt): still honour them
    for k in [key, *(hashlib.sha1(f"{m}|{prompt}".encode("utf-8")).hexdigest() for m in JUDGE_MODELS)]:
        if k in cache and cache[k]["model"] != agent.AGENT_MODEL:
            _judge_models["used"] = cache[k]["model"]
            return cache[k]["text"]

    last = None
    pause = float(os.environ.get("RAG_JUDGE_PAUSE", "0"))
    if pause:
        time.sleep(pause)
    for name in JUDGE_MODELS:
        if name in _dead_judges:
            continue
        for attempt in range(1, 5):
            try:
                model = _judge_models.setdefault(name, ChatGoogleGenerativeAI(model=name, temperature=0, google_api_key=load_api_key(), max_retries=2))
                reply = model.invoke(prompt)
                _judge_models["used"] = name
                # keep the reply, unless it came from the agent model standing in for an unavailable judge
                if name != agent.AGENT_MODEL or JUDGE_MODELS == [agent.AGENT_MODEL]:
                    cache[key] = {"model": name, "text": reply.text}
                    EVAL.mkdir(exist_ok=True)
                    JUDGE_CACHE.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")
                return reply.text
            except Exception as error:  # noqa: BLE001
                last = error
                text = f"{type(error).__name__} {error}"
                limited = any(t in text for t in ("RateLimit", "429", "RESOURCE_EXHAUSTED"))
                transient = any(t in text for t in ("503", "500", "UNAVAILABLE", "overloaded", "Timeout", "timed out", "DEADLINE"))
                daily = limited and any(t in text.lower() for t in ("perday", "per day", "limit: 0"))
                wait = 40
                m = re.search(r"retry in ([\d.]+)\s*s", text, re.I)
                if m:
                    wait = min(90, float(m.group(1)) + 2)
                retry = (limited or transient) and not daily and attempt < 4
                shown = str(error).replace("\n", " ")[: 600 if attempt == 1 else 160]
                print(f"  judge model {name} failed: {type(error).__name__}: {shown}"
                      + (f" (waiting {wait if limited else 15:.0f} s, try {attempt}/4)" if retry else ""), file=sys.stderr)
                if retry:
                    time.sleep(wait if limited else 15)  # per-minute limit or a temporary glitch: ask the SAME model again
                    continue
                if daily or not transient:
                    _dead_judges.add(name)  # no quota left today / model not found for this key: skip it for the rest of the run
                    print(f"  -> {name} will not be used again in this run"
                          + (" (its quota looks used up; it usually resets at 09:00 Spanish time)" if daily else ""), file=sys.stderr)
                elif limited:
                    _dead_judges.add(name)
                break
    raise RuntimeError(f"No judge model worked: {last}")


def judge(q: dict, a: dict, checks: dict) -> dict:
    """Refusals and blocks are decided in code; only real answers go to the LLM judge."""
    outcome = checks["outcome"]
    if outcome == "correct_refusal":
        return {"correct": 1, "supported": 1, "by": "code", "reason": "unanswerable question, assistant said it does not know"}
    if outcome == "blocked":
        unanswerable = q["kind"] == "unanswerable"
        return {"correct": int(unanswerable), "supported": 1, "by": "code",
                "reason": "citation guardrail blocked the answer" + (" (safe: question is unanswerable)" if unanswerable else " (an answer existed)")}
    if outcome == "wrong_refusal":
        return {"correct": 0, "supported": 1, "by": "code", "reason": "answerable question, assistant said it does not know"}
    prompt = RUBRIC.format(
        kind=q["kind"], question=q["question"], reference=q["reference_answer"],
        where="; ".join(f"{s} | {l}" for s, l in expected_passages(q)) or "none (unanswerable)",
        evidence=_evidence(a["retrieved"]), answer=a["answer"],
    )
    text = _judge_call(prompt)
    m = re.search(r"\{.*\}", text, re.S)
    try:
        data = json.loads(m.group(0)) if m else {}
        return {"correct": int(bool(int(data["correct"]))), "supported": int(bool(int(data["supported"]))),
                "by": f"judge:{_judge_models.get('used', '')}", "reason": str(data.get("reason", ""))[:300]}
    except (KeyError, ValueError, TypeError):
        return {"correct": 0, "supported": 0, "by": "judge:unparsable", "reason": f"unparsable judge reply: {text[:120]!r}"}


# --------------------------------------------------------------- agreement ---
def kappa(a: list[int], b: list[int]) -> float:
    n = len(a)
    if not n:
        return float("nan")
    po = sum(x == y for x, y in zip(a, b)) / n
    pa, pb = sum(a) / n, sum(b) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return float("nan") if pe == 1 else (po - pe) / (1 - pe)


def agreement(verdicts: dict[str, dict]) -> dict:
    if not HUMAN.is_file():
        return {}
    with HUMAN.open(newline="", encoding="utf-8") as f:
        human = {r["id"].strip(): r for r in csv.DictReader(f) if (r.get("id") or "").strip() and (r.get("correct") or "").strip() in {"0", "1"}}
    ids = [i for i in human if i in verdicts]
    if len(ids) < 20:
        print(f"\n{len(ids)} of the required 20 graded answers found in eval/human_labels.csv.")
        print("Grade 20+ from eval/answers.csv BEFORE opening eval/judge_verdicts.csv, then rerun this stage.")
        return {"graded": len(ids)}
    out = {"graded": len(ids)}
    for field in ("correct", "supported"):
        h = [int(human[i][field]) if (human[i].get(field) or "").strip() in {"0", "1"} else verdicts[i][field] for i in ids]
        j = [verdicts[i][field] for i in ids]
        out[f"{field}_agreement"] = round(sum(x == y for x, y in zip(h, j)) / len(ids), 3)
        out[f"{field}_kappa"] = round(kappa(h, j), 3)
        out[f"{field}_disagreements"] = [i for i, x, y in zip(ids, h, j) if x != y]
    both = sum(all(int(human[i][f]) == verdicts[i][f] for f in ("correct", "supported") if (human[i].get(f) or "").strip() in {"0", "1"}) for i in ids)
    out["both_agreement"] = round(both / len(ids), 3)
    print(f"\nAgreement with your {len(ids)} labels: correct {out['correct_agreement']:.0%} (kappa {out['correct_kappa']}), "
          f"supported {out['supported_agreement']:.0%} (kappa {out['supported_kappa']}), both {out['both_agreement']:.0%}")
    print(f"  disagreements on correct: {out['correct_disagreements']}; on supported: {out['supported_disagreements']}")
    return out


# ---------------------------------------------------------------- failures ---
def suggest_cause(q: dict, a: dict, c: dict, v: dict) -> str:
    """First guess for the failure class; you confirm or change it in eval/failures.csv."""
    if c["outcome"] == "wrong_refusal":
        return "wrong_refusal"
    if c["outcome"] == "answered_unanswerable":
        return "unsupported_claim" if not v["supported"] else "bad_test_question?"
    if c["outcome"] == "blocked":
        return "retrieval_miss" if c["expected_retrieved_all"] == 0 else "unsupported_claim"
    if not v["supported"]:
        return "unsupported_claim"
    if c["expected_retrieved_all"] == 0:
        return "retrieval_miss"
    return "wrong_answer_right_passage"


def main() -> None:
    EVAL.mkdir(exist_ok=True)
    questions = read_questions()
    if len(questions) < 30:
        raise SystemExit(f"eval/questions.csv has {len(questions)} questions; at least 30 are required.")
    print(f"{len(questions)} questions: " + ", ".join(f"{sum(q['kind'] == k for q in questions)} {k}" for k in ("single", "multi", "unanswerable")))

    print("\n== 1/4 Retrieval ==")
    evaluate_retrieval(questions)

    print("\n== 2/4 Agent on every question ==")
    answers = run_agent_on_all(questions)
    write_csv(EVAL / "answers.csv", [{
        "id": q["id"], "kind": q["kind"], "question": q["question"], "reference_answer": q["reference_answer"],
        "answer": answers[q["id"]]["answer"],
    } for q in questions])
    print("Answers saved to eval/answers.csv. Grade 20+ of them in eval/human_labels.csv before reading the judge's verdicts.")

    print("\n== 3/4 Code checks and LLM judge ==")
    checks = {q["id"]: code_checks(q, answers[q["id"]]) for q in questions}
    verdicts = {}
    for q in questions:
        verdicts[q["id"]] = judge(q, answers[q["id"]], checks[q["id"]])
    write_csv(EVAL / "judge_verdicts.csv", [{"id": q["id"], "kind": q["kind"], **checks[q["id"]], **verdicts[q["id"]]} for q in questions])

    print("\n== 4/4 Summary ==")
    ans_q = [q for q in questions if q["kind"] != "unanswerable"]
    una_q = [q for q in questions if q["kind"] == "unanswerable"]
    real = [q for q in questions if checks[q["id"]]["outcome"] in {"answered", "answered_unanswerable"}]
    summary = {
        "questions": len(questions), "answerable": len(ans_q), "unanswerable": len(una_q),
        "correct_answers": sum(verdicts[q["id"]]["correct"] for q in ans_q),
        "correct_refusals": sum(checks[q["id"]]["outcome"] == "correct_refusal" for q in una_q),
        "blocked_unanswerable": sum(checks[q["id"]]["outcome"] == "blocked" for q in una_q),
        "unanswerable_answered": sum(checks[q["id"]]["outcome"] == "answered_unanswerable" for q in una_q),
        "wrong_refusals": sum(checks[q["id"]]["outcome"] == "wrong_refusal" for q in ans_q),
        "blocked_answerable": sum(checks[q["id"]]["outcome"] == "blocked" for q in ans_q),
        "unsupported_answers": sum(not verdicts[q["id"]]["supported"] for q in real),
        "answers_given": len(real),
        "citations_valid": sum(checks[q["id"]]["citations_valid"] for q in questions),
        "guardrail_events": {},
    }
    for q in questions:
        for g in answers[q["id"]]["guardrails"]:
            name = g.split(":")[0]
            summary["guardrail_events"][name] = summary["guardrail_events"].get(name, 0) + 1
    secs = [answers[q["id"]]["seconds"] for q in questions]
    toks = [answers[q["id"]]["input_tokens"] + answers[q["id"]]["output_tokens"] for q in questions]
    summary["cost"] = {
        "tokens_mean": round(statistics.mean(toks)), "tokens_p95": round(sorted(toks)[int(0.95 * (len(toks) - 1))]),
        "seconds_mean": round(statistics.mean(secs), 1), "seconds_p95": round(sorted(secs)[int(0.95 * (len(secs) - 1))], 1),
        "model_calls_mean": round(statistics.mean(answers[q["id"]]["model_calls"] for q in questions), 1),
        "agent_model": agent.AGENT_MODEL,
        "judge_model": ", ".join(sorted({v["by"].split(":", 1)[1] for v in verdicts.values() if v["by"].startswith("judge:")})),
    }
    summary["agreement"] = agreement(verdicts)

    failures = []
    for q in questions:
        c, v = checks[q["id"]], verdicts[q["id"]]
        bad = (not v["correct"]) or (not v["supported"] and c["outcome"] in {"answered", "answered_unanswerable"}) or c["outcome"] == "blocked"
        if bad:
            failures.append({"id": q["id"], "kind": q["kind"], "question": q["question"], "outcome": c["outcome"],
                             "suggested_cause": suggest_cause(q, answers[q["id"]], c, v), "final_cause": "",
                             "judge_reason": v["reason"], "my_note": ""})
    write_csv(EVAL / "failures.csv", failures,
              ["id", "kind", "question", "outcome", "suggested_cause", "final_cause", "judge_reason", "my_note"])
    summary["failures"] = len(failures)
    (EVAL / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    s = summary
    print(f"Correct answers      {s['correct_answers']}/{s['answerable']} answerable ({pct(s['correct_answers'], s['answerable'])})")
    print(f"Correct refusals     {s['correct_refusals']}/{s['unanswerable']} unanswerable ({pct(s['correct_refusals'], s['unanswerable'])});"
          f" answered anyway {s['unanswerable_answered']}, blocked by guardrail {s['blocked_unanswerable']}")
    print(f"Wrong refusals       {s['wrong_refusals']}/{s['answerable']} answerable;  blocked by guardrail {s['blocked_answerable']}")
    print(f"Unsupported answers  {s['unsupported_answers']}/{s['answers_given']} answers given")
    print(f"Valid citations      {s['citations_valid']}/{s['questions']}")
    print(f"Guardrail events     {s['guardrail_events'] or 'none'}")
    print(f"Cost per question    {s['cost']['tokens_mean']} tokens (p95 {s['cost']['tokens_p95']}), "
          f"{s['cost']['seconds_mean']}s (p95 {s['cost']['seconds_p95']}s), {s['cost']['model_calls_mean']} model calls")
    judge_used = s["cost"]["judge_model"] or "none (everything decided by code)"
    print(f"Judge model          {judge_used}")
    if s["cost"]["agent_model"] in s["cost"]["judge_model"].split(", "):
        print("WARNING: at least one answer was graded by the agent model itself, so it grades its own work. Check the `by` column of"
              " eval/judge_verdicts.csv, set RAG_JUDGE_MODEL to a different model and rerun (replies from the real judge are kept),"
              " or say this limitation in REPORT.md.")
    print(f"{len(failures)} failures listed in eval/failures.csv: confirm or change `final_cause` for each.")


if __name__ == "__main__":
    main()
