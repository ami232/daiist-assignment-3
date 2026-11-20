"""
Assignment 3: evaluation (`main.py evaluate`).

1. Retrieval: hit rate at k = 1, 3, 5 for every (chunking design x search method),
   plus words added to the prompt.                       -> eval/retrieval_results.csv
2. End to end: the agent answers every question in eval/questions.csv.
   Saved one by one, so a crash or quota stop resumes.   -> eval/answers.jsonl, eval/answers.csv
3. Code checks: refusal right/wrong, citations valid (all retrieved), expected law cited,
   expected passage retrieved.
4. LLM judge with a rubric and the retrieved text as evidence. -> eval/judge.csv
5. Agreement between the judge and eval/human_labels.csv.
6. Summary: results, failure hints, tokens and seconds.  -> eval/summary.md, eval/summary.json

Grade eval/answers.csv yourself into eval/human_labels.csv BEFORE opening eval/judge.csv.
Flags: --fresh (re-ask every question), --skip-agent (retrieval only).
"""

from __future__ import annotations

import asyncio
import csv
import json
import re
import sys
import time
import unicodedata
from contextlib import AsyncExitStack
from pathlib import Path

import retrieval as rt

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
HUMAN = EVAL / "human_labels.csv"
ANSWERS_JSONL = EVAL / "answers.jsonl"

CONFIGS = [(d, m) for d in ("articles", "fixed200") for m in ("vector", "bm25", "hybrid")]
KS = (1, 3, 5)
JUDGE_MODEL = "gemini-3.5-flash-lite"
JUDGE_FALLBACK = "gemini-flash-lite-latest"
PAUSE = 8.0  # seconds between agent questions: the free tier allows 15 requests/minute per model
RATE_LIMIT_WAIT = 45  # seconds to wait after a 429 before retrying

# ---- the judge's rubric (yours to decide: edit it, and describe it in REPORT.md) ----
# v2: supported is checked claim by claim with a quote (v1 graded the answer as a whole; its verdicts
# are kept in eval/judge_v1.csv for comparison).
JUDGE_RUBRIC_VERSION = "v2"
JUDGE_RUBRIC = """You grade answers from an assistant about Spanish housing law (LAU, LDV, LPH).
You get: the question, its kind, a reference answer written by a human, the assistant's answer,
and EVIDENCE = the exact passages the assistant retrieved. Judge only against these; ignore your own legal knowledge.

correct (1/0):
- answerable question: 1 if the answer gives the same key facts as the reference (numbers, deadlines,
  who must do what, conditions). Extra correct detail is fine. A missing key fact, a wrong number, or a
  refusal = 0. For multi-passage questions, BOTH parts must be answered.
- unanswerable question: 1 only if the assistant says the laws don't cover it and does not give a
  substantive answer anyway. Any guessed answer = 0.

supported (1/0), checked claim by claim:
- First list every factual claim in the answer (each number, deadline, condition, definition, who-does-what).
- For each claim, copy the exact sentence from the EVIDENCE that states it. If you cannot quote a sentence
  that states the claim itself, the claim is unsupported.
- Recommendations to consult someone (a lawyer, a housing office) and statements that the corpus does not
  cover the question are not factual claims and need no quote.
- supported = 1 only if every claim has a quote.

Reply with JSON only:
{"claims": [{"claim": "<short>", "quote": "<exact sentence from the evidence, or empty if none>"}],
 "correct": 0 or 1, "supported": 0 or 1, "reason": "<one sentence; name any unsupported claim>"}"""


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


# ---------------------------------------------------------------- helpers

def norm(text: str) -> str:
    text = unicodedata.normalize("NFKD", text.replace("\xa0", " ").lower())
    text = "".join(c for c in text if not unicodedata.combining(c))
    return re.sub(r"\s+", " ", text).strip().rstrip(".")


def read_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if (r.get("question") or "").strip()]
    for r in rows:
        r["kind"] = r["kind"].strip().lower()
        sources = [s.strip() for s in r["expected_source"].split(";") if s.strip()]
        locs = [l.strip() for l in r["expected_location"].split(";") if l.strip()]
        if len(sources) == 1 and len(locs) > 1:
            sources = sources * len(locs)
        r["expected"] = list(zip(sources, locs)) if locs else [(s, "") for s in sources]
    return rows


def matches(expected: tuple[str, str], meta: dict) -> bool:
    """A chunk matches if it is from the expected law and covers the expected location.

    "Artículo 36.2" or "Artículo 36, apartado 2" matches the chunk "Artículo 36".
    """
    source, loc = expected
    if norm(meta["source"]) != norm(source):
        return False
    if not loc:
        return True
    want = norm(loc)
    for have in meta.get("locations", meta["location"]).split(";"):
        have = norm(have)
        if want == have or re.match(re.escape(have) + r"(?![0-9a-z])", want):
            return True
    return False


def label_matches(expected: tuple[str, str], label: str) -> bool:
    """Same, for a citation label 'LAU, Artículo 36'."""
    src, _, loc = label.partition(",")
    return matches(expected, {"source": src.strip(), "location": loc.strip()})


# ---------------------------------------------------------------- 1. retrieval

def evaluate_retrieval(questions: list[dict]) -> list[dict]:
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    rows = []
    for design, method in CONFIGS:
        hits = {k: 0 for k in KS}
        full5, words = 0, []
        for q in answerable:
            res = rt.search(q["question"], design=design, method=method, k=max(KS))
            words.append(sum(len(h["text"].split()) for h in res[:rt.SEARCH_K]))
            for k in KS:
                if any(matches(e, h["metadata"]) for e in q["expected"] for h in res[:k]):
                    hits[k] += 1
            if all(any(matches(e, h["metadata"]) for h in res[:5]) for e in q["expected"]):
                full5 += 1
        n = len(answerable)
        row = {"design": design, "method": method, "questions": n,
               **{f"hit@{k}": round(hits[k] / n, 3) for k in KS},
               "all_passages@5": round(full5 / n, 3),
               "avg_words_in_prompt@5": round(sum(words) / n)}
        rows.append(row)
        log(f"  {design:9} {method:6} " + "  ".join(f"hit@{k}={row[f'hit@{k}']:.2f}" for k in KS)
            + f"  all@5={row['all_passages@5']:.2f}  words={row['avg_words_in_prompt@5']}")
    write_csv(EVAL / "retrieval_results.csv", rows)
    return rows


def evaluate_retrieval_agent_queries(questions: list[dict], answers: dict[str, dict]) -> list[dict]:
    """Same hit rates, but searching with the query the agent actually sent (its first search).

    The agent rewrites the English question as a Spanish search, so this measures retrieval
    as it happens in use. Uses cached query embeddings, so it costs no quota after a run.
    """
    items = [(q, t["args"]["query"]) for q in questions if q["kind"] != "unanswerable" and q["id"] in answers
             for t in answers[q["id"]]["trace"][:1] if t["tool"] == "search"]
    rows = []
    for design, method in CONFIGS:
        hits = {k: 0 for k in KS}
        for q, query in items:
            res = rt.search(query, design=design, method=method, k=max(KS))
            for k in KS:
                if any(matches(e, h["metadata"]) for e in q["expected"] for h in res[:k]):
                    hits[k] += 1
        n = max(len(items), 1)
        rows.append({"design": design, "method": method, "questions": len(items),
                     **{f"hit@{k}": round(hits[k] / n, 3) for k in KS}})
    write_csv(EVAL / "retrieval_agent_queries.csv", rows)
    return rows


# ---------------------------------------------------------------- 2. agent answers

def load_answers() -> dict[str, dict]:
    if not ANSWERS_JSONL.exists():
        return {}
    out = {}
    for line in ANSWERS_JSONL.read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            out[r["id"]] = r
    return out


async def run_agent(questions: list[dict], fresh: bool) -> dict[str, dict]:
    import agent as ag
    done = {} if fresh else load_answers()
    if fresh and ANSWERS_JSONL.exists():
        ANSWERS_JSONL.unlink()
    todo = [q for q in questions if q["id"] not in done or done[q["id"]].get("question") != q["question"]]
    if not todo:
        log("  all questions already answered (use --fresh to re-ask)")
        return done
    async with AsyncExitStack() as stack:
        agent = await ag.build_agent(stack)
        for i, q in enumerate(todo, 1):
            r = None
            for attempt in range(4):
                try:
                    r = await ag.answer_async(q["question"], agent=agent, interactive=False)
                    break
                except Exception as error:  # noqa: BLE001 - retry rate limits, record anything else
                    if is_rate_limit(error) and attempt < 3:
                        log(f"  {q['id']} rate limited, waiting {RATE_LIMIT_WAIT}s ...")
                        await asyncio.sleep(RATE_LIMIT_WAIT)
                        continue
                    log(f"  {q['id']} ERROR {type(error).__name__}: {str(error)[:200]}")
                    break
            if r is None:
                continue
            r["id"] = q["id"]
            done[q["id"]] = r
            with ANSWERS_JSONL.open("a", encoding="utf-8") as f:
                f.write(json.dumps(r, ensure_ascii=False) + "\n")
            log(f"  [{i}/{len(todo)}] {q['id']} {'REFUSED' if r['refused'] else 'answered'} "
                f"{r['seconds']}s {r['tokens']['input'] + r['tokens']['output']} tok"
                + (" GUARDRAIL" if r["guardrail"] else ""))
            await asyncio.sleep(PAUSE)
    return done


# ---------------------------------------------------------------- 3. code checks

def code_checks(q: dict, a: dict) -> dict:
    unanswerable = q["kind"] == "unanswerable"
    cited, retrieved = a["citations"], a["retrieved"]
    return {
        "refusal_ok": int(a["refused"] == unanswerable),
        "wrong_refusal": int(a["refused"] and not unanswerable),
        "answered_unanswerable": int(unanswerable and not a["refused"]),
        "citations_valid": int(all(c in retrieved for c in cited)),
        "has_citation": int(bool(cited)),
        "expected_cited": "" if unanswerable else int(all(any(label_matches(e, c) for c in cited) for e in q["expected"])),
        "expected_retrieved": "" if unanswerable else int(any(label_matches(e, r) for e in q["expected"] for r in retrieved)),
        "guardrail_fired": int(bool(a.get("guardrail"))),
    }


# ---------------------------------------------------------------- 4. judge

def judge(questions: list[dict], answers: dict[str, dict]) -> dict[str, dict]:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from api_key import load_api_key
    load_api_key()
    model = ChatGoogleGenerativeAI(model=JUDGE_MODEL, temperature=0, timeout=60, max_retries=2).with_fallbacks(
        [ChatGoogleGenerativeAI(model=JUDGE_FALLBACK, temperature=0, timeout=60, max_retries=2)])
    path = EVAL / "judge.csv"
    cached = {}
    if path.exists():
        with path.open(newline="", encoding="utf-8") as f:
            cached = {r["id"]: r for r in csv.DictReader(f)}
    verdicts = {}
    for q in questions:
        a = answers.get(q["id"])
        if not a:
            continue
        c = cached.get(q["id"])
        if c and c.get("answer_hash") == str(hash_answer(a["answer"])) and c.get("rubric") == JUDGE_RUBRIC_VERSION:
            verdicts[q["id"]] = c
            continue
        evidence = "\n\n".join(t["output"] for t in a["trace"] if t["tool"] == "search") or "(nothing retrieved)"
        prompt = (f"{JUDGE_RUBRIC}\n\nQUESTION ({q['kind']}): {q['question']}\n\nREFERENCE ANSWER: "
                  f"{q['reference_answer']}\n\nASSISTANT ANSWER:\n{a['answer']}\n\nEVIDENCE:\n{evidence[:30000]}")
        try:
            raw = invoke_with_retry(model, prompt).content
            raw = raw if isinstance(raw, str) else "".join(p.get("text", "") for p in raw if isinstance(p, dict))
            v = json.loads(re.search(r"\{.*\}", raw, re.S).group(0))
            verdicts[q["id"]] = {"id": q["id"], "correct": int(v["correct"]), "supported": int(v["supported"]),
                                 "reason": v.get("reason", ""), "answer_hash": hash_answer(a["answer"]),
                                 "rubric": JUDGE_RUBRIC_VERSION,
                                 "unsupported_claims": " | ".join(c.get("claim", "") for c in v.get("claims", [])
                                                                  if not (c.get("quote") or "").strip())}
        except Exception as error:  # noqa: BLE001
            log(f"  judge failed on {q['id']}: {str(error)[:150]}")
        time.sleep(4)
    write_csv(path, list(verdicts.values()))
    return verdicts


def is_rate_limit(error: Exception) -> bool:
    return "429" in str(error) or "RESOURCE_EXHAUSTED" in str(error)


def invoke_with_retry(model, prompt, tries: int = 4):
    for attempt in range(tries):
        try:
            return model.invoke(prompt)
        except Exception as error:  # noqa: BLE001
            if not is_rate_limit(error) or attempt == tries - 1:
                raise
            log(f"  judge rate limited, waiting {RATE_LIMIT_WAIT}s ...")
            time.sleep(RATE_LIMIT_WAIT)


def hash_answer(text: str) -> str:
    import hashlib
    return hashlib.sha1(text.encode()).hexdigest()[:12]


# ---------------------------------------------------------------- 5. agreement

def agreement(verdicts: dict[str, dict]) -> dict:
    if not HUMAN.exists():
        return {}
    with HUMAN.open(newline="", encoding="utf-8") as f:
        human = {r["id"]: r for r in csv.DictReader(f) if (r.get("id") or "").strip()}
    out = {}
    for field in ("correct", "supported"):
        pairs = [(int(h[field]), int(verdicts[i][field])) for i, h in human.items()
                 if i in verdicts and str(h.get(field, "")).strip() in ("0", "1")]
        if not pairs:
            continue
        n = len(pairs)
        agree = sum(a == b for a, b in pairs) / n
        p_h, p_j = sum(a for a, _ in pairs) / n, sum(b for _, b in pairs) / n
        expected = p_h * p_j + (1 - p_h) * (1 - p_j)
        kappa = (agree - expected) / (1 - expected) if expected < 1 else 1.0
        out[field] = {"n": n, "agreement": round(agree, 3), "cohen_kappa": round(kappa, 3),
                      "disagreements": [i for i, h in human.items() if i in verdicts
                                        and str(h.get(field, "")).strip() in ("0", "1")
                                        and int(h[field]) != int(verdicts[i][field])]}
    return out


# ---------------------------------------------------------------- 6. summary

def failure_hint(q: dict, a: dict, checks: dict, v: dict | None) -> str:
    """A first guess at the failure cause, for you to confirm by reading the case."""
    if q["kind"] == "unanswerable":
        return "" if a["refused"] else "unsupported claim (answered an unanswerable question)"
    if a["refused"]:
        return "wrong refusal" if checks["expected_retrieved"] else "retrieval miss (then refused)"
    if v is None:
        return ""
    if int(v["correct"]) and int(v["supported"]):
        return ""
    if not checks["expected_retrieved"]:
        return "retrieval miss"
    if not int(v["supported"]):
        return "unsupported claim"
    return "wrong answer from the right passage"


def summarise(questions, answers, verdicts, retrieval_rows, agree, agent_query_rows=()) -> None:
    rows, counts = [], {"correct": 0, "incorrect": 0, "unsupported": 0, "correct_refusals": 0,
                        "wrong_refusals": 0, "answered_unanswerable": 0, "invalid_citations": 0,
                        "guardrail_fired": 0}
    tok, secs = [], []
    for q in questions:
        a = answers.get(q["id"])
        if not a:
            continue
        ch = code_checks(q, a)
        v = verdicts.get(q["id"])
        if q["kind"] == "unanswerable":
            counts["correct_refusals" if a["refused"] else "answered_unanswerable"] += 1
        elif a["refused"]:
            counts["wrong_refusals"] += 1
        elif v:
            counts["correct" if int(v["correct"]) else "incorrect"] += 1
        if v and not int(v["supported"]):
            counts["unsupported"] += 1
        counts["invalid_citations"] += 1 - ch["citations_valid"]
        counts["guardrail_fired"] += ch["guardrail_fired"]
        tok.append(a["tokens"]["input"] + a["tokens"]["output"])
        secs.append(a["seconds"])
        rows.append({"id": q["id"], "kind": q["kind"], "question": q["question"], "answer": a["answer"],
                     "reference_answer": q["reference_answer"], "citations": "; ".join(a["citations"]),
                     **ch, "judge_correct": v["correct"] if v else "", "judge_supported": v["supported"] if v else "",
                     "judge_reason": v["reason"] if v else "", "failure_hint": failure_hint(q, a, ch, v),
                     "tokens": tok[-1], "seconds": a["seconds"], "tool_calls": len(a["trace"])})
    write_csv(EVAL / "results.csv", rows)
    write_csv(EVAL / "answers.csv", [{"id": r["id"], "kind": r["kind"], "question": r["question"],
                                       "answer": r["answer"], "reference_answer": r["reference_answer"]} for r in rows])
    n = len(rows)
    cost = {"questions": n, "avg_tokens": round(sum(tok) / n) if n else 0,
            "avg_seconds": round(sum(secs) / n, 1) if n else 0, "max_seconds": max(secs) if secs else 0}
    hints = {}
    for r in rows:
        if r["failure_hint"]:
            hints[r["failure_hint"]] = hints.get(r["failure_hint"], 0) + 1
    summary = {"counts": counts, "by_kind": by_kind(rows), "cost": cost, "agreement": agree,
               "failure_hints": hints, "retrieval": retrieval_rows,
               "search_config": {"design": rt.SEARCH_DESIGN, "method": rt.SEARCH_METHOD, "k": rt.SEARCH_K}}
    (EVAL / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    md = ["# Evaluation summary", "", "## Retrieval (hit rate on answerable questions)", "",
          "| design | method | hit@1 | hit@3 | hit@5 | all passages@5 | words in prompt |", "|---|---|---|---|---|---|---|"]
    md += [f"| {r['design']} | {r['method']} | {r['hit@1']} | {r['hit@3']} | {r['hit@5']} | {r['all_passages@5']} "
           f"| {r['avg_words_in_prompt@5']} |" for r in retrieval_rows]
    md += ["", "## Retrieval with the agent's own (Spanish) search queries", "",
           "| design | method | hit@1 | hit@3 | hit@5 |", "|---|---|---|---|---|"]
    md += [f"| {r['design']} | {r['method']} | {r['hit@1']} | {r['hit@3']} | {r['hit@5']} |" for r in agent_query_rows]
    md += ["", f"Agent uses: {rt.SEARCH_DESIGN} / {rt.SEARCH_METHOD} / k={rt.SEARCH_K}", "",
           "## End to end", "", "| result | count |", "|---|---|"]
    md += [f"| {k.replace('_', ' ')} | {v} |" for k, v in counts.items()]
    md += ["", "## Judge vs human", ""]
    md += [f"- {f}: {d['agreement']:.0%} agreement over {d['n']} answers (kappa {d['cohen_kappa']}); "
           f"disagree on {', '.join(d['disagreements']) or 'none'}" for f, d in agree.items()] or ["- no human labels yet"]
    md += ["", "## Failure hints (confirm each by reading the case)", ""]
    md += [f"- {k}: {v}" for k, v in hints.items()] or ["- none"]
    md += ["", "## Cost per question", "", f"- {cost['avg_tokens']} tokens, {cost['avg_seconds']} s on average "
           f"(max {cost['max_seconds']} s), {n} questions"]
    (EVAL / "summary.md").write_text("\n".join(md) + "\n", encoding="utf-8")
    log("\n" + "\n".join(md))


def by_kind(rows):
    out = {}
    for r in rows:
        k = out.setdefault(r["kind"], {"n": 0, "judge_correct": 0, "refusal_ok": 0})
        k["n"] += 1
        k["judge_correct"] += int(r["judge_correct"] or 0)
        k["refusal_ok"] += r["refusal_ok"]
    return out


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


# ---------------------------------------------------------------- main

def main() -> None:
    fresh, skip_agent = "--fresh" in sys.argv, "--skip-agent" in sys.argv
    questions = read_questions()
    log(f"{len(questions)} questions\n\n1. Retrieval")
    retrieval_rows = evaluate_retrieval(questions)
    if skip_agent:
        return
    log("\n2. Agent answers")
    answers = asyncio.run(run_agent(questions, fresh))
    log("\n3-4. Code checks and judge")
    agent_query_rows = evaluate_retrieval_agent_queries(questions, answers)
    verdicts = judge(questions, answers)
    log("\n5-6. Agreement and summary")
    summarise(questions, answers, verdicts, retrieval_rows, agreement(verdicts), agent_query_rows)


if __name__ == "__main__":
    main()
