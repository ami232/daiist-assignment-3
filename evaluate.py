"""
Assignment 3: evaluation (`main.py evaluate`).

Stage 1, retrieval: hit rate at k = 1, 3, 5 for every retrieval design on every answerable question.
    -> eval/retrieval_per_question.csv, eval/retrieval_summary.csv

Stage 2, end to end: the agent (agent.py) answers every question.
    - code checks: refusal vs. expected refusal, every citation valid against what was retrieved,
      answer cites the expected article, expected passage retrieved;
    - LLM judge (rubric below, retrieved passages as evidence) grades correct / supported for answered,
      answerable questions; refusals are graded by code;
    - agreement between the final verdicts and your grades in eval/human_labels.csv;
    - a suggested failure cause for every failed question (you confirm it in REPORT.md).
    -> eval/answers.jsonl (cache: answers are reused unless EVAL_FRESH=1), eval/answers_for_grading.csv
       (no verdicts, for grading by hand), eval/judged.csv, eval/summary.json

A retrieved chunk is a hit when its agreement equals an expected_source and its article equals the
article in expected_location (paragraphs are ignored: "Article III:2" matches any chunk of Article III).
For `multi` questions, `hit` means at least one expected passage was retrieved and `all` that every
expected passage was.
"""

from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

import retrieval

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
KS = (1, 3, 5)

# (name, chunking design, search method)
DESIGNS = [
    ("fixed-vector", "fixed", "vector"),
    ("structured-vector", "structured", "vector"),
    ("fixed-hybrid", "fixed", "hybrid"),
    ("structured-hybrid", "structured", "hybrid"),
]

RE_ARTICLE_KEY = re.compile(r"^((?:Ad\s+)?(?:Article|Annex|Appendix)\s+[0-9IVXL]+[A-Z]?(?:\s+bis)?)", re.I)


def log(*args) -> None:
    print(*args, flush=True)


def read_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r["question"].strip()]


def article_key(location: str) -> str:
    """'Article III:2' -> 'Article III', 'Article 12.8-12.9' -> 'Article 12', 'Annex A para. 3' -> 'Annex A'."""
    m = RE_ARTICLE_KEY.match(location.strip())
    return re.sub(r"\s+", " ", m.group(1)) if m else location.strip()


def expected_passages(row: dict) -> list[tuple[str, str]]:
    """[(agreement, article)] from the ';'-separated columns; one source applies to every location."""
    sources = [s.strip() for s in row["expected_source"].split(";") if s.strip()]
    locations = [l.strip() for l in row["expected_location"].split(";") if l.strip()]
    if len(sources) == 1:
        sources = sources * len(locations)
    return [(s, article_key(l)) for s, l in zip(sources, locations)]


def chunk_articles(meta: dict) -> set[str]:
    """Articles a chunk covers: one for structured chunks, possibly several for fixed windows."""
    arts = {meta.get("article", "")}
    if meta.get("articles"):
        arts |= {a.strip() for a in meta["articles"].split("|")}
    return arts


def matches(meta: dict, passage: tuple[str, str]) -> bool:
    source, article = passage
    return meta.get("agreement") == source and article in chunk_articles(meta)


def retrieval_stage(questions: list[dict]) -> list[dict]:
    answerable = [q for q in questions if q["kind"].strip() != "unanswerable"]
    retrieval.embed_queries([q["question"] for q in answerable])   # one batched call; cached afterwards

    per_question, summary = [], []
    for name, design, method in DESIGNS:
        totals = {f"{t}@{k}": 0 for k in KS for t in ("hit", "all")}
        words_at = {k: 0 for k in KS}
        multi_n = 0
        for q in answerable:
            passages = expected_passages(q)
            hits = retrieval.search(q["question"], k=max(KS), design=design, method=method)
            row = dict(design=name, id=q["id"], kind=q["kind"], expected=" ; ".join(f"{s} {a}" for s, a in passages),
                       top5=" | ".join(h.citation for h in hits))
            for k in KS:
                found = [any(matches(h.metadata, p) for h in hits[:k]) for p in passages]
                row[f"hit@{k}"] = int(any(found))
                row[f"all@{k}"] = int(all(found))
                totals[f"hit@{k}"] += row[f"hit@{k}"]
                if q["kind"] == "multi":
                    totals[f"all@{k}"] += row[f"all@{k}"]
                words_at[k] += sum(len(h.text.split()) for h in hits[:k])
            multi_n += q["kind"] == "multi"
            per_question.append(row)

        n = len(answerable)
        s = dict(design=name, questions=n)
        for k in KS:
            s[f"hit@{k}"] = round(totals[f"hit@{k}"] / n, 3)
        for k in KS:
            s[f"multi_all@{k}"] = round(totals[f"all@{k}"] / multi_n, 3) if multi_n else ""
        for k in KS:
            s[f"words@{k}"] = round(words_at[k] / n)
        summary.append(s)

    write_csv(EVAL / "retrieval_per_question.csv", per_question)
    write_csv(EVAL / "retrieval_summary.csv", summary)
    log(f"\nRetrieval hit rate on {len(answerable)} answerable questions "
        f"({sum(q['kind'] == 'multi' for q in answerable)} multi):\n")
    cols = ["design"] + [f"hit@{k}" for k in KS] + [f"multi_all@{k}" for k in KS] + [f"words@{k}" for k in KS]
    log(" | ".join(f"{c:>17}" if i == 0 else f"{c:>11}" for i, c in enumerate(cols)))
    for s in summary:
        log(" | ".join(f"{str(s[c]):>17}" if i == 0 else f"{str(s[c]):>11}" for i, c in enumerate(cols)))
    return summary


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


# --------------------------------------------------------------------------- stage 2: end to end

ANSWERS = EVAL / "answers.jsonl"
FOR_GRADING = EVAL / "answers_for_grading.csv"
JUDGED = EVAL / "judged.csv"
SUMMARY = EVAL / "summary.json"
HUMAN = EVAL / "human_labels.csv"
JUDGE_MODEL = "gemini-3.1-flash-lite"   # a different model from the agent, so it does not grade itself

JUDGE_RUBRIC = """You grade answers from a legal research assistant that must answer ONLY from WTO treaty
passages it retrieved. You get the question, a reference answer written by a trade-law student, the
passages the assistant retrieved, and the assistant's answer.

correct = 1 if the answer gives the same legal outcome as the reference answer and does not omit a
  condition, time limit or exception the reference treats as essential. Extra correct detail is fine.
  Different wording is fine. Answering only part of a two-part question, a wrong number, a wrong
  article, or the opposite conclusion -> 0.
supported = 1 if every legal claim in the answer is stated in, or follows directly from, the retrieved
  passages. A claim that relies on case law, outside knowledge or a passage that was not retrieved -> 0,
  even if it is true. Citations pointing to the wrong passage for a claim -> 0.

Judge supported against the passages, not against the reference answer.
Return JSON only: {"correct": 0 or 1, "supported": 0 or 1, "reason": "<one sentence>"}"""


def run_agent(questions: list[dict]) -> dict[str, dict]:
    """Answer every question (reusing cached answers), return {id: trace dict}."""
    import asyncio
    import json
    import os
    from dataclasses import asdict

    import agent

    cache = {}
    if ANSWERS.exists() and os.environ.get("EVAL_FRESH") != "1":
        for line in ANSWERS.read_text(encoding="utf-8").splitlines():
            r = json.loads(line)
            if not r.get("error") and r.get("model") == agent.MODEL:   # reuse only this model's answers
                cache[r["id"]] = r
    todo = [q for q in questions if q["id"] not in cache or cache[q["id"]]["question"] != q["question"]]
    log(f"\nAgent: {len(questions) - len(todo)} cached answers, {len(todo)} to run (model {agent.MODEL})")

    async def go():
        async with agent.Harness(approve=lambda tool, args: False) as h:   # evaluation never adds documents
            for i, q in enumerate(todo, 1):
                t = await h.ask(q["question"])
                cache[q["id"]] = dict(id=q["id"], model=agent.MODEL, **asdict(t))
                log(f"  [{i}/{len(todo)}] {q['id']} {t.seconds:>5}s refused={t.refused} "
                    f"guardrail={t.guardrail or '-'}{' ERROR ' + t.error[:80] if t.error else ''}")
                ANSWERS.write_text("\n".join(json.dumps(cache[x["id"]], ensure_ascii=False)
                                             for x in questions if x["id"] in cache) + "\n", encoding="utf-8")

    if todo:
        asyncio.run(go())
    return cache


def judge(q: dict, t: dict) -> dict:
    import json

    from google import genai
    from google.genai import types

    from api_key import load_api_key

    evidence = "\n\n".join(f"[{c}]\n{v['text']}" for c, v in t["retrieved"].items()) or "(nothing retrieved)"
    prompt = (f"{JUDGE_RUBRIC}\n\nQUESTION:\n{q['question']}\n\nREFERENCE ANSWER:\n{q['reference_answer']}\n\n"
              f"RETRIEVED PASSAGES:\n{evidence}\n\nASSISTANT'S ANSWER:\n{t['answer']}")
    client = genai.Client(api_key=load_api_key())
    for attempt in range(4):
        try:
            r = client.models.generate_content(
                model=JUDGE_MODEL, contents=prompt,
                config=types.GenerateContentConfig(temperature=0, response_mime_type="application/json"))
            v = json.loads(r.text)
            usage = r.usage_metadata
            return dict(correct=int(v["correct"]), supported=int(v["supported"]), reason=v.get("reason", ""),
                        judge_tokens=(usage.total_token_count or 0) if usage else 0)
        except Exception as error:  # noqa: BLE001
            last = error
            import time
            time.sleep(15 * (attempt + 1))
    return dict(correct="", supported="", reason=f"judge failed: {last}", judge_tokens=0)


def code_checks(q: dict, t: dict) -> dict:
    import agent

    unanswerable = q["kind"] == "unanswerable"
    passages = expected_passages(q) if not unanswerable else []
    allowed = {agent.citation_key(c) for c in t["retrieved"]}
    cited_keys = {agent.citation_key(c) for c in t["cited"]}
    exp_keys = {(s, a.replace("Article ", "Art. ")) for s, a in passages}   # "Article III" -> "Art. III"
    return dict(
        refused=int(t["refused"]),
        refusal_correct=int(t["refused"] == unanswerable),
        citations_valid=int(all(agent.citation_key(c) in allowed for c in t["cited"])),
        n_citations=len(t["cited"]),
        cites_expected=int(bool(cited_keys & exp_keys)) if passages else "",
        retrieved_expected=int(any(agent.citation_key(c) in exp_keys for c in t["retrieved"])) if passages else "",
    )


def outcome(q: dict, row: dict) -> str:
    if q["kind"] == "unanswerable":
        return "correct_refusal" if row["refused"] else "answered_unanswerable"
    if row["refused"]:
        return "wrong_refusal"
    if row["correct"] == 1 and row["supported"] == 1:
        return "correct"
    if row["correct"] == 1:
        return "correct_but_unsupported"
    return "unsupported" if row["supported"] == 0 else "incorrect"


def suggested_cause(q: dict, row: dict) -> str:
    """A first guess at the failure cause; confirm or change it yourself (it may be a bad test question)."""
    o = row["outcome"]
    if o in ("correct", "correct_refusal"):
        return ""
    if o == "answered_unanswerable":
        return "unsupported claim"
    if o == "wrong_refusal":
        return "wrong refusal" if row["retrieved_expected"] == 1 else "retrieval miss"
    if row["retrieved_expected"] == 0:
        return "retrieval miss"
    if row["supported"] == 0:
        return "unsupported claim"
    return "wrong answer from the right passage"


def read_human() -> dict[str, dict]:
    if not HUMAN.exists():
        return {}
    with HUMAN.open(newline="", encoding="utf-8") as f:
        return {r["id"].strip(): r for r in csv.DictReader(f) if r.get("id", "").strip() and r.get("correct", "").strip()}


def end_to_end_stage(questions: list[dict]) -> dict:
    import json

    traces = run_agent(questions)

    # for hand grading: the answers and evidence, no verdicts
    write_csv(FOR_GRADING, [dict(id=q["id"], kind=q["kind"], question=q["question"],
                                 reference_answer=q["reference_answer"], answer=traces[q["id"]]["answer"],
                                 retrieved=" | ".join(traces[q["id"]]["retrieved"]))
                            for q in questions])

    old = {}
    if JUDGED.exists():
        with JUDGED.open(newline="", encoding="utf-8") as f:
            old = {r["id"]: r for r in csv.DictReader(f)}

    rows = []
    for q in questions:
        t = traces[q["id"]]
        row = dict(id=q["id"], kind=q["kind"], **code_checks(q, t))
        prev = old.get(q["id"])
        if q["kind"] == "unanswerable" or row["refused"]:
            # refusals are graded by code; correct = refused when it should, supported = nothing claimed
            row.update(correct=row["refusal_correct"], supported=1, reason="graded by code (refusal)", judge_tokens=0)
        elif prev and prev.get("answer") == t["answer"] and prev.get("correct") not in ("", None):
            row.update(correct=int(prev["correct"]), supported=int(prev["supported"]), reason=prev["reason"],
                       judge_tokens=int(prev.get("judge_tokens") or 0))
        else:
            row.update(judge(q, t))
        if q["kind"] == "unanswerable" and not row["refused"]:
            row["supported"] = 0    # it answered something the corpus does not contain
        row["outcome"] = outcome(q, row)
        row["suggested_cause"] = suggested_cause(q, row)
        row.update(guardrail=t["guardrail"], tool_calls=len(t["tool_calls"]),
                   tokens=t["input_tokens"] + t["output_tokens"], seconds=t["seconds"], answer=t["answer"])
        rows.append(row)
    write_csv(JUDGED, rows)

    n = len(rows)
    counts = {k: sum(r["outcome"] == k for r in rows) for k in
              ("correct", "correct_but_unsupported", "incorrect", "unsupported", "wrong_refusal",
               "correct_refusal", "answered_unanswerable")}
    human = read_human()
    agree = {}
    for col in ("correct", "supported"):
        pairs = [(int(human[r["id"]][col]), int(r[col])) for r in rows if r["id"] in human and r[col] != ""]
        agree[col] = dict(n=len(pairs), agreement=round(sum(a == b for a, b in pairs) / len(pairs), 3) if pairs else None)
    summary = dict(
        questions=n, model=__import__("agent").MODEL, judge_model=JUDGE_MODEL, outcomes=counts,
        code_checks=dict(
            citations_valid=f"{sum(r['citations_valid'] for r in rows)}/{n}",
            refusal_correct=f"{sum(r['refusal_correct'] for r in rows)}/{n}",
            cites_expected=f"{sum(r['cites_expected'] == 1 for r in rows)}/{sum(r['cites_expected'] != '' for r in rows)}",
        ),
        guardrail_fired={g: sum(r["guardrail"] == g for r in rows) for g in ("fixed_on_retry", "blocked") },
        human_agreement=agree,
        cost=dict(mean_tokens=round(sum(r["tokens"] for r in rows) / n),
                  mean_judge_tokens=round(sum(int(r["judge_tokens"] or 0) for r in rows) / n),
                  mean_seconds=round(sum(float(r["seconds"]) for r in rows) / n, 1),
                  mean_tool_calls=round(sum(r["tool_calls"] for r in rows) / n, 2)),
        failures={c: sum(r["suggested_cause"] == c for r in rows) for c in
                  ("retrieval miss", "wrong answer from the right passage", "unsupported claim", "wrong refusal")},
    )
    SUMMARY.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    log("\nEnd-to-end results:\n" + json.dumps(summary, indent=2))
    if not human:
        log(f"\nGrade 20+ answers in {HUMAN.relative_to(ROOT)} (from {FOR_GRADING.relative_to(ROOT)}, before "
            f"reading {JUDGED.relative_to(ROOT)}) to get judge agreement.")
    return summary


def main() -> None:
    import os

    questions = read_questions()
    retrieval_stage(questions)
    only = [x.strip() for x in os.environ.get("EVAL_ONLY", "").split(",") if x.strip()]   # e.g. EVAL_ONLY=q02,q26
    end_to_end_stage([q for q in questions if q["id"] in only] if only else questions)


if __name__ == "__main__":
    sys.exit(main())
