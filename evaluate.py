"""
Assignment 3: evaluation (`main.py evaluate`).

1. Retrieval   hit rate at k = 1, 3, 5 for every indexed design (fixed / structural chunking)
               x search method (dense / hybrid), and the words each adds to the prompt.
2. End to end  the agent answers every question (add_document approvals auto-rejected).
3. Code checks citations returned by search, citation of an expected article, refusals.
4. LLM judge   binary rubric (correct, supported) with the retrieved text as evidence,
               run on a different model than the agent.
5. Agreement   judge vs eval/human_labels.csv.

Writes eval/retrieval.csv, eval/answers.jsonl, eval/judge.csv, eval/summary.json and
eval/summary.md. Answers and verdicts are cached by question, prompt and model, so a
re-run only redoes what changed.
"""

from __future__ import annotations

import csv
import hashlib
import json
import sys
import time
from pathlib import Path

import index as pipeline
import retrieval

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
HUMAN = EVAL / "human_labels.csv"
ANSWERS = EVAL / "answers.jsonl"
JUDGE = EVAL / "judge.csv"

JUDGE_MODEL = "gemini-3.6-flash"  # a different model from the agent's; Pro has no free-tier quota
KS = (1, 3, 5)
METHODS = ("dense", "hybrid")


def log(*args) -> None:
    print(*args, flush=True)


def load_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r["question"].strip()]


def expected_passages(q: dict) -> list[tuple[str, str]]:
    """[(source, 'Article N'), ...]; one source applies to every location."""
    sources = [s.strip() for s in q["expected_source"].split(";") if s.strip()]
    locations = [loc.strip() for loc in q["expected_location"].split(";") if loc.strip()]
    if len(sources) == 1:
        sources = sources * len(locations)
    return list(zip(sources, locations))


# --------------------------------------------------------------------------- 1. retrieval

def covers(hit: dict, passage: tuple[str, str]) -> bool:
    source, article = passage
    return hit["source"] == source and article in hit["articles"].split(";")


def retrieval_eval(questions: list[dict]) -> list[dict]:
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    rows = []
    for design in pipeline.DESIGNS:
        expected_chunks = len(pipeline.corpus_chunks(design))
        r = retrieval.Retriever(design)
        if len(r) < expected_chunks:
            log(f"  {design}: only {len(r)}/{expected_chunks} chunks embedded, skipped (run main.py index)")
            continue
        for method in METHODS:
            found_any = {k: 0 for k in KS}
            found_all = {k: 0 for k in KS}
            words = 0
            for q in answerable:
                hits = r.search(q["question"], k=max(KS), method=method)
                passages = expected_passages(q)
                words += sum(len(h["text"].split()) for h in hits)
                for k in KS:
                    got = [any(covers(h, p) for h in hits[:k]) for p in passages]
                    found_any[k] += any(got)
                    found_all[k] += all(got)
            n = len(answerable)
            row = {"design": design, "method": method, "questions": n,
                   **{f"hit@{k}": round(found_any[k] / n, 3) for k in KS},
                   **{f"all@{k}": round(found_all[k] / n, 3) for k in KS},
                   "words_in_prompt@5": round(words / n)}
            rows.append(row)
            log(f"  {design:10s} {method:6s} " + "  ".join(f"hit@{k}={row[f'hit@{k}']:.2f}" for k in KS)
                + f"  all@5={row['all@5']:.2f}  words@5={row['words_in_prompt@5']}")
    if rows:
        with (EVAL / "retrieval.csv").open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=list(rows[0]))
            w.writeheader()
            w.writerows(rows)
    return rows


# --------------------------------------------------------------------------- 2. answers

def config_hash() -> str:
    import agent

    prompt = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    return hashlib.sha1(f"{agent.MODEL}|{retrieval.ACTIVE_DESIGN}|{retrieval.ACTIVE_METHOD}|{prompt}".encode()).hexdigest()[:12]


def run_agent(questions: list[dict]) -> list[dict]:
    import agent

    cfg = config_hash()
    cached = {}
    if ANSWERS.exists():
        for line in ANSWERS.read_text(encoding="utf-8").splitlines():
            if line.strip():
                a = json.loads(line)
                cached[a["id"]] = a
    results = []
    for q in questions:
        old = cached.get(q["id"])
        if old and old.get("config") == cfg and old["question"] == q["question"] and not old.get("error"):
            results.append(old)
            continue
        log(f"  {q['id']} ...")
        try:
            out = agent.answer(q["question"], approve=lambda action: False)
        except Exception as error:  # noqa: BLE001 - record and continue
            out = {"answer": "", "trace": [], "retrieved": [], "citations": {}, "guardrail_fired": False,
                   "tokens": {"input": 0, "output": 0}, "seconds": 0, "error": f"{type(error).__name__}: {error}"}
            log(f"    error: {out['error'][:200]}")
        results.append({"id": q["id"], "kind": q["kind"], "question": q["question"],
                        "reference_answer": q["reference_answer"], "config": cfg, **out})
        with ANSWERS.open("w", encoding="utf-8") as f:  # save after every question
            done = {r["id"]: r for r in results}
            for qq in questions:
                if qq["id"] in done:
                    f.write(json.dumps(done[qq["id"]], ensure_ascii=False) + "\n")
                elif qq["id"] in cached:
                    f.write(json.dumps(cached[qq["id"]], ensure_ascii=False) + "\n")
    return results


# --------------------------------------------------------------------------- 3. code checks

def code_checks(q: dict, a: dict) -> dict:
    import agent

    check = agent.check_citations(a["answer"], a["retrieved"])
    cited_articles = {(s, agent._article(loc)) for s, loc in
                      ((c.strip("[]").split(", ", 1) + [""])[:2] for c in check["cited"])}
    expected = expected_passages(q) if q["kind"] != "unanswerable" else []
    return {
        "searched": any(t.get("tool") == "search" for t in a["trace"]),
        "refusal": check["refusal"],
        "citations": len(check["cited"]),
        "invalid_citations": len(check["invalid"]),
        "cites_expected": bool(expected) and any(p in cited_articles for p in expected),
        "correct_refusal": q["kind"] == "unanswerable" and check["refusal"],
        "wrong_refusal": q["kind"] != "unanswerable" and check["refusal"],
        "guardrail_fired": a.get("guardrail_fired", False),
    }


# --------------------------------------------------------------------------- 4. judge

RUBRIC = """You grade answers of a compliance assistant for EU banking regulation (CRR, CRD, MiFID II).
You get the question, a reference answer written by an expert, the assistant's answer, and the
passages the assistant retrieved with its search tool (its only allowed evidence).

Grade two criteria, each 1 or 0:

correct
  1 if the answer states the key facts of the reference answer: the same figures, thresholds,
    time limits, conditions and articles, with nothing that contradicts it. Extra correct detail is
    fine. Missing a secondary detail is fine; missing or changing the main figure or rule is not.
  1 if the reference says the corpus does not cover the question and the assistant declines to
    answer (says the corpus does not cover it) without giving a substantive answer from elsewhere.
  0 otherwise, including when the assistant declines although the reference has an answer.

supported
  1 if every factual claim in the answer appears in the retrieved passages (paraphrase allowed;
    figures must match exactly). A refusal that makes no factual claims is supported.
  0 if any claim, figure or cited article is not in the retrieved passages.

Be strict on numbers. Judge only against the reference and the passages, not your own knowledge.
Reply with JSON: {"correct": 0 or 1, "supported": 0 or 1, "reason": "<one sentence>"}."""


def judge_one(q: dict, a: dict) -> dict:
    from google.genai import errors, types

    passages = "\n\n=====\n\n".join(a["retrieved"]) or "(no search results)"
    prompt = (f"QUESTION\n{q['question']}\n\nREFERENCE ANSWER\n{q['reference_answer']}\n\n"
              f"ASSISTANT ANSWER\n{a['answer']}\n\nRETRIEVED PASSAGES\n{passages}")
    config = types.GenerateContentConfig(
        system_instruction=RUBRIC, temperature=0, response_mime_type="application/json",
        response_schema={"type": "object", "properties": {
            "correct": {"type": "integer"}, "supported": {"type": "integer"}, "reason": {"type": "string"}},
            "required": ["correct", "supported", "reason"]},
    )
    for attempt in range(8):
        try:
            response = pipeline.genai_client().models.generate_content(
                model=JUDGE_MODEL, contents=prompt, config=config)
            return json.loads(response.text)
        except (errors.ClientError, errors.ServerError) as error:
            # 429 rate limit, 503 overloaded, 504 deadline: wait and retry
            if error.code not in (429, 500, 503, 504) or attempt == 7:
                raise
            wait = 20 * (attempt + 1)
            log(f"    judge {error.code}, retrying in {wait}s")
            time.sleep(wait)
    raise RuntimeError("judge failed")


def run_judge(questions: list[dict], answers: dict) -> dict:
    cached = {}
    if JUDGE.exists():
        with JUDGE.open(newline="", encoding="utf-8") as f:
            cached = {r["id"]: r for r in csv.DictReader(f)}
    verdicts = {}
    for q in questions:
        a = answers[q["id"]]
        key = hashlib.sha1(f"{JUDGE_MODEL}|{RUBRIC}|{q['reference_answer']}|{a['answer']}".encode()).hexdigest()[:12]
        old = cached.get(q["id"])
        if old and old.get("key") == key:
            verdicts[q["id"]] = old
            continue
        log(f"  judging {q['id']} ...")
        v = judge_one(q, a)
        verdicts[q["id"]] = {"id": q["id"], "correct": str(v["correct"]), "supported": str(v["supported"]),
                             "reason": v["reason"], "key": key}
        with JUDGE.open("w", newline="", encoding="utf-8") as f:
            w = csv.DictWriter(f, fieldnames=["id", "correct", "supported", "reason", "key"])
            w.writeheader()
            w.writerows([verdicts.get(qq["id"]) or cached[qq["id"]] for qq in questions
                         if qq["id"] in verdicts or qq["id"] in cached])
    return verdicts


# --------------------------------------------------------------------------- 5. agreement

def kappa(pairs: list[tuple[int, int]]) -> float | None:
    n = len(pairs)
    if not n:
        return None
    po = sum(a == b for a, b in pairs) / n
    pa = sum(a for a, _ in pairs) / n
    pb = sum(b for _, b in pairs) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return round((po - pe) / (1 - pe), 3) if pe < 1 else None


def agreement(verdicts: dict) -> dict:
    if not HUMAN.exists():
        return {}
    with HUMAN.open(newline="", encoding="utf-8") as f:
        human = {r["id"]: r for r in csv.DictReader(f) if r.get("id")}
    out = {"graded": len(human)}
    for criterion in ("correct", "supported"):
        pairs = [(int(h[criterion]), int(verdicts[i][criterion])) for i, h in human.items()
                 if i in verdicts and h.get(criterion, "").strip() in ("0", "1")]
        out[criterion] = {
            "n": len(pairs),
            "agreement": round(sum(a == b for a, b in pairs) / len(pairs), 3) if pairs else None,
            "kappa": kappa(pairs),
            "disagreements": [i for i, h in human.items() if i in verdicts
                              and h.get(criterion, "").strip() in ("0", "1")
                              and int(h[criterion]) != int(verdicts[i][criterion])],
        }
    return out


# --------------------------------------------------------------------------- main

def main() -> int:
    sys.stdout.reconfigure(encoding="utf-8")
    questions = load_questions()
    log(f"{len(questions)} questions\n\n1. Retrieval (answerable questions)")
    retrieval_rows = retrieval_eval(questions)

    log("\n2. Agent answers")
    answers = {a["id"]: a for a in run_agent(questions)}

    log("\n3. Code checks")
    checks = {q["id"]: code_checks(q, answers[q["id"]]) for q in questions}

    log("\n4. LLM judge")
    verdicts = run_judge(questions, answers)

    log("\n5. Agreement with human labels")
    agree = agreement(verdicts)

    by_kind = {}
    for q in questions:
        k = by_kind.setdefault(q["kind"], {"n": 0, "correct": 0, "supported": 0})
        k["n"] += 1
        k["correct"] += int(verdicts[q["id"]]["correct"])
        k["supported"] += int(verdicts[q["id"]]["supported"])
    n = len(questions)
    answered = [a for a in answers.values() if not a.get("error")]
    summary = {
        "agent_model": __import__("agent").MODEL, "judge_model": JUDGE_MODEL,
        "design": retrieval.ACTIVE_DESIGN, "method": retrieval.ACTIVE_METHOD,
        "retrieval": retrieval_rows,
        "questions": n,
        "correct": sum(int(v["correct"]) for v in verdicts.values()),
        "unsupported": sum(1 for v in verdicts.values() if v["supported"] == "0"),
        "correct_refusals": sum(c["correct_refusal"] for c in checks.values()),
        "unanswerable": sum(q["kind"] == "unanswerable" for q in questions),
        "wrong_refusals": sum(c["wrong_refusal"] for c in checks.values()),
        "answers_with_invalid_citations": sum(c["invalid_citations"] > 0 for c in checks.values()),
        "answerable_citing_expected_article": sum(c["cites_expected"] for c in checks.values()),
        "guardrail_fired": [i for i, c in checks.items() if c["guardrail_fired"]],
        "by_kind": by_kind,
        "errors": [a["id"] for a in answers.values() if a.get("error")],
        "avg_tokens_in": round(sum(a["tokens"]["input"] for a in answered) / max(len(answered), 1)),
        "avg_tokens_out": round(sum(a["tokens"]["output"] for a in answered) / max(len(answered), 1)),
        "avg_seconds": round(sum(a["seconds"] for a in answered) / max(len(answered), 1), 1),
        "agreement": agree,
        "per_question": [{"id": q["id"], "kind": q["kind"], **checks[q["id"]],
                          "judge_correct": int(verdicts[q["id"]]["correct"]),
                          "judge_supported": int(verdicts[q["id"]]["supported"]),
                          "judge_reason": verdicts[q["id"]]["reason"]} for q in questions],
    }
    (EVAL / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    write_markdown(summary)
    log(f"\ncorrect {summary['correct']}/{n}, unsupported {summary['unsupported']}, "
        f"correct refusals {summary['correct_refusals']}/{summary['unanswerable']}, "
        f"wrong refusals {summary['wrong_refusals']}, avg {summary['avg_seconds']}s and "
        f"{summary['avg_tokens_in']}+{summary['avg_tokens_out']} tokens per question")
    for c in ("correct", "supported"):
        if agree.get(c):
            log(f"judge vs you on {c}: {agree[c]['agreement']} agreement over {agree[c]['n']} answers "
                f"(kappa {agree[c]['kappa']})")
    log("Wrote eval/summary.md and eval/summary.json")
    return 0


def write_markdown(s: dict) -> None:
    lines = ["# Evaluation summary", "",
             f"Agent `{s['agent_model']}`, judge `{s['judge_model']}`, design `{s['design']}` + `{s['method']}`.", "",
             "## Retrieval", "", "| design | method | hit@1 | hit@3 | hit@5 | all@5 (multi) | words@5 |",
             "|---|---|---|---|---|---|---|"]
    lines += [f"| {r['design']} | {r['method']} | {r['hit@1']} | {r['hit@3']} | {r['hit@5']} | {r['all@5']} | "
              f"{r['words_in_prompt@5']} |" for r in s["retrieval"]]
    lines += ["", "## End to end", "",
              f"- correct: {s['correct']}/{s['questions']}",
              f"- unsupported: {s['unsupported']}",
              f"- correct refusals: {s['correct_refusals']}/{s['unanswerable']}",
              f"- wrong refusals: {s['wrong_refusals']}",
              f"- answers with invalid citations: {s['answers_with_invalid_citations']}",
              f"- citation guardrail fired on: {', '.join(s['guardrail_fired']) or 'none'}",
              f"- cost per question: {s['avg_tokens_in']} input + {s['avg_tokens_out']} output tokens, {s['avg_seconds']} s",
              "", "| id | kind | judge correct | judge supported | refusal | citations | invalid | cites expected | reason |",
              "|---|---|---|---|---|---|---|---|---|"]
    lines += [f"| {p['id']} | {p['kind']} | {p['judge_correct']} | {p['judge_supported']} | {int(p['refusal'])} | "
              f"{p['citations']} | {p['invalid_citations']} | {int(p['cites_expected'])} | "
              f"{p['judge_reason'].replace('|', '/')} |" for p in s["per_question"]]
    if s["agreement"]:
        lines += ["", "## Judge vs human", ""]
        for c in ("correct", "supported"):
            a = s["agreement"].get(c)
            if a:
                lines.append(f"- {c}: {a['agreement']} agreement over {a['n']} answers, kappa {a['kappa']}; "
                             f"disagreements: {', '.join(a['disagreements']) or 'none'}")
    (EVAL / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    raise SystemExit(main())
