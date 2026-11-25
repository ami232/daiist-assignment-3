"""
Assignment 3: evaluation (`main.py evaluate`).

Stages, each saving to eval/ and resuming from what is already saved, so a
crash or the daily quota loses nothing (re-running costs nothing once done):

  1. retrieval  hit rate @1/3/5 for four designs   -> eval/retrieval.csv, retrieval_summary.json
  2. answers    agent.py on every question          -> eval/answers.jsonl
  3. checks     code checks (citations, refusals)   -> inside eval/results.csv
  4. judge      LLM judge with rubric + evidence    -> eval/judge.jsonl
  5. agreement  judge vs eval/human_labels.csv      -> eval/summary.json
  6. add-doc    before/after adding the ITV decree  -> eval/add_document_demo.json

`uv run python evaluate.py --stage retrieval` runs one stage.
"""

from __future__ import annotations

import argparse
import csv
import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
HUMAN = EVAL / "human_labels.csv"
TRANSLATIONS = EVAL / "translations.json"
RETRIEVAL_CSV = EVAL / "retrieval.csv"
RETRIEVAL_SUMMARY = EVAL / "retrieval_summary.json"
ANSWERS = EVAL / "answers.jsonl"
JUDGE = EVAL / "judge.jsonl"
RESULTS = EVAL / "results.csv"
SUMMARY = EVAL / "summary.json"
ADD_DEMO = EVAL / "add_document_demo.json"

KS = (1, 3, 5)
DESIGNS = {
    "A_dense_en": ("dense", "en"),     # English question, Gemini vectors only
    "B_dense_es": ("dense", "es"),     # question rewritten as Spanish legal query
    "C_bm25_es": ("bm25", "es"),       # keyword search on the Spanish query
    "D_hybrid_es": ("hybrid", "es"),   # RRF of B and C
    "E_dense_en+bm25_es": ("fuse:dense/en+bm25/es", "both"),   # RRF of A and C
    "F_dense_en+dense_es": ("fuse:dense/en+dense/es", "both"),  # RRF of A and B
    "G_dense_en_e001": ("dense", "en", "gemini-embedding-001"),  # as A, other embedding model
    "H_dense_es_e001": ("dense", "es", "gemini-embedding-001"),  # as B, other embedding model
}
E2 = "gemini-embedding-2"
CHOSEN = "G_dense_en_e001"  # only design with every expected passage in the top 5 (the k the tool returns); see REPORT.md


def log(*a):
    print(*a, flush=True)


def load_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r["question"].strip()]


def expected_pairs(q: dict) -> list[tuple[str, str]]:
    srcs = [s.strip() for s in q["expected_source"].split(";")]
    locs = [s.strip() for s in q["expected_location"].split(";")]
    return [(s, l) for s, l in zip(srcs, locs) if s]


def norm(s: str) -> str:
    from retrieval import fold
    return " ".join(fold(s).split())


def read_jsonl(p: Path) -> dict[str, dict]:
    if not p.exists():
        return {}
    return {r["id"]: r for r in map(json.loads, p.read_text(encoding="utf-8").splitlines()) if r}


def append_jsonl(p: Path, row: dict) -> None:
    with p.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


# ===================================================================== 1. retrieval

def spanish_queries(questions: list[dict]) -> dict[str, str]:
    from llm import to_spanish_query
    cache = json.loads(TRANSLATIONS.read_text(encoding="utf-8")) if TRANSLATIONS.exists() else {}
    for q in questions:
        if q["id"] not in cache:
            cache[q["id"]] = to_spanish_query(q["question"])[0]
            TRANSLATIONS.write_text(json.dumps(cache, ensure_ascii=False, indent=1), encoding="utf-8")
    return cache


def fuse(ix, spec: str, en: str, es: str, k: int) -> list[dict]:
    """Reciprocal rank fusion of two rankings, e.g. 'dense/en+bm25/es'."""
    from collections import Counter
    from retrieval import RRF_K
    fused: Counter = Counter()
    for part in spec.split("+"):
        method, lang = part.split("/")
        for rank, r in enumerate(ix.search(en if lang == "en" else es, k=20, method=method)):
            fused[r["id"]] += 1 / (RRF_K + rank + 1)
    return [{**ix.by_id[i], "score": s} for i, s in fused.most_common(k)]


def stage_retrieval() -> dict:
    from retrieval import Index
    indexes = {}
    qs = [q for q in load_questions() if q["kind"] != "unanswerable"]
    es = spanish_queries(qs)
    rows, summary = [], {}
    for name, (method, lang, *model) in DESIGNS.items():
        model = model[0] if model else E2
        ix = indexes.setdefault(model, Index(model))
        hits = {k: 0 for k in KS}
        hits_any = {k: 0 for k in KS}
        words = {k: 0 for k in KS}
        for q in qs:
            query = q["question"] if lang == "en" else es[q["id"]]
            if method.startswith("fuse:"):
                query = f"{q['question']} || {es[q['id']]}"
                res = fuse(ix, method[5:], q["question"], es[q["id"]], max(KS))
            else:
                res = ix.search(query, k=max(KS), method=method)
            got = [(r["metadata"]["source"], norm(r["metadata"]["location"])) for r in res]
            want = [(s, norm(l)) for s, l in expected_pairs(q)]
            first_rank = {w: (got.index(w) + 1 if w in got else None) for w in set(want)}
            for k in KS:
                found = [w for w in set(want) if first_rank[w] and first_rank[w] <= k]
                hits[k] += len(found) == len(set(want))      # all needed passages
                hits_any[k] += bool(found)                     # at least one
                words[k] += sum(r["metadata"]["words"] for r in res[:k])
            rows.append({"design": name, "id": q["id"], "kind": q["kind"], "query": query,
                         "ranks": json.dumps({f"{s}|{l}": first_rank[(s, norm(l))] for s, l in expected_pairs(q)},
                                             ensure_ascii=False),
                         "top5": " ; ".join(f"{r['metadata']['source']}|{r['metadata']['location']}" for r in res)})
        n = len(qs)
        summary[name] = {
            **{f"hit@{k}": round(hits[k] / n, 3) for k in KS},
            **{f"any@{k}": round(hits_any[k] / n, 3) for k in KS},
            **{f"words@{k}": round(words[k] / n) for k in KS},
            "n": n,
        }
        multi = [q for q in qs if q["kind"] == "multi"]
        summary[name]["multi_hit@5"] = round(
            sum(1 for r in rows if r["design"] == name and r["kind"] == "multi"
                and all(v and v <= 5 for v in json.loads(r["ranks"]).values())) / max(len(multi), 1), 3)
    with RETRIEVAL_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    RETRIEVAL_SUMMARY.write_text(json.dumps(summary, indent=1), encoding="utf-8")
    log("\nRetrieval (answerable questions; hit = every expected passage in top k)")
    log(f"{'design':<22}" + "".join(f"{'hit@'+str(k):>8}" for k in KS) + f"{'multi@5':>9}{'words@5':>9}")
    for name, s in summary.items():
        log(f"{name:<22}" + "".join(f"{s['hit@'+str(k)]:>8.2f}" for k in KS)
            + f"{s['multi_hit@5']:>9.2f}{s['words@5']:>9}")
    return summary


# ===================================================================== 2. answers

class InfraError(RuntimeError):
    """A tool or API failure (quota, network): never saved as an answer."""


def stage_answers() -> None:
    import agent
    done = read_jsonl(ANSWERS)
    qs = load_questions()
    todo = [q for q in qs if q["id"] not in done]
    log(f"{len(done)} answers saved, {len(todo)} to go")
    for q in todo:
        t = time.time()
        r = agent.ask(q["question"], approve_add=False)
        bad = [x for x in r["trace"] if x["result"].startswith(("Error", "NOTE: keyword search only"))]
        if bad or not r["answer"]:
            raise InfraError(f"{q['id']}: tool/API failure ({bad[0]['result'][:200] if bad else 'empty answer'}). "
                             "Not saved; re-run `main.py evaluate` later (the daily embedding quota resets at 09:00 in Spain).")
        r["id"] = q["id"]
        append_jsonl(ANSWERS, r)
        log(f"  {q['id']} {time.time() - t:5.1f}s  {'REFUSAL' if r['refusal'] else 'answer '}  {r['answer'][:90]!r}")


# ===================================================================== 3. code checks

def code_checks(q: dict, r: dict) -> dict:
    from agent import REFUSAL, citation_ok, parse_citations, retrieved_citations
    cited = set(parse_citations(r["answer"]))
    retrieved = retrieved_citations(r["trace"])
    want = {(s, l) for s, l in expected_pairs(q)}
    nw = {(s, norm(l)) for s, l in want}
    refusal = r["answer"].strip().startswith(REFUSAL)
    return {
        "refusal": int(refusal),
        "should_refuse": int(q["kind"] == "unanswerable"),
        "has_citation": int(bool(cited)),
        "citations_valid": int(all(citation_ok(c, retrieved) for c in cited)),  # every citation was retrieved
        "expected_retrieved": int(nw <= {(s, norm(l)) for s, l in retrieved}) if want else "",
        "expected_cited": int(all(any(cs == s and citation_ok((cs, norm(cl)), {(s, norm(l))}) for cs, cl in cited)
                                  for s, l in want)) if want else "",
        "n_searches": sum(1 for t in r["trace"] if t["tool"] == "search"),
    }


# ===================================================================== 3b. grading sheet

GRADING_SHEET = EVAL / "grading_sheet.md"


def stage_grading_sheet() -> None:
    """Everything a human grader needs and nothing from the judge: question,
    reference, answer, and the passages the agent retrieved."""
    answers = read_jsonl(ANSWERS)
    out = ["# Grading sheet (for eval/human_labels.csv)\n",
           "Grade each answer *before* opening eval/judge.jsonl or eval/results.csv. "
           "correct = right against the reference (or a proper refusal); supported = every claim is in "
           "the retrieved passages below. Write a note for every 0.\n"]
    for q in load_questions():
        r = answers.get(q["id"])
        if not r:
            continue
        out += [f"\n---\n\n## {q['id']} ({q['kind']})\n", f"**Question:** {q['question']}\n",
                f"**Reference:** {q['reference_answer']}\n", f"**Answer:**\n\n{r['answer']}\n",
                "<details><summary>Retrieved passages</summary>\n\n```\n" + evidence_text(r, 8000) + "\n```\n</details>\n"]
    GRADING_SHEET.write_text("\n".join(out), encoding="utf-8")
    log(f"Wrote {GRADING_SHEET.relative_to(ROOT)} ({len(answers)} answers)")


# ===================================================================== 4. judge

JUDGE_SYSTEM = """You grade answers from an assistant about Spanish traffic law. You are strict
and literal. Judge only against the reference answer and the retrieved passages given to you,
not against your own knowledge of the law."""

JUDGE_RUBRIC = """Question: {question}
Question type: {kind}
Reference answer (written by the test author): {reference}

Retrieved passages (the only evidence the assistant had):
<<<
{evidence}
>>>

Assistant's answer:
<<<
{answer}
>>>

Grade with this rubric.

correct (1/0):
- answerable question: 1 if the answer gives the reference's key facts (numbers, units,
  who it applies to) without contradicting it. Extra true details are fine. 0 if a key fact is
  wrong or missing, if it answers a different case (e.g. general limit when asked about novices),
  or if it refuses.
- unanswerable question: 1 if it says the corpus does not cover it and does not supply the
  missing answer anyway. 0 if it gives an answer (even hedged) to the part the corpus lacks.

supported (1/0): 1 if every factual claim in the answer (numbers, conditions, names of laws or
documents, article references) can be found in the retrieved passages. A refusal that only
says the corpus does not cover it and points to a generic place to check (DGT, city council)
is supported. 0 if any claim is not in the passages, e.g. a decree number or a figure from
memory. List those claims.

Return JSON only:
{{"correct": 0 or 1, "supported": 0 or 1, "unsupported_claims": ["..."], "reason": "one sentence"}}"""


def evidence_text(r: dict, limit: int = 14000) -> str:
    text = "\n\n=====\n\n".join(t["result"] for t in r["trace"] if t["tool"] == "search")
    return text[:limit] or "(no passages retrieved)"


def stage_judge() -> None:
    from llm import JUDGE_MODEL, generate
    answers = read_jsonl(ANSWERS)
    done = read_jsonl(JUDGE)
    qs = {q["id"]: q for q in load_questions()}
    todo = [i for i in answers if i not in done and i in qs]
    log(f"{len(done)} verdicts saved, {len(todo)} to go (judge: {JUDGE_MODEL})")
    for i in todo:
        q, r = qs[i], answers[i]
        prompt = JUDGE_RUBRIC.format(question=q["question"], kind=q["kind"], reference=q["reference_answer"],
                                     evidence=evidence_text(r), answer=r["answer"])
        t = time.time()
        text, usage = generate(prompt, model=JUDGE_MODEL, system=JUDGE_SYSTEM, json_mode=True)
        try:
            v = json.loads(re.search(r"\{.*\}", text, re.S).group(0))
            v = {"correct": int(v["correct"]), "supported": int(v["supported"]),
                 "unsupported_claims": v.get("unsupported_claims", []), "reason": v.get("reason", "")}
        except Exception:  # noqa: BLE001
            raise InfraError(f"{i}: judge returned unparseable output: {text[:300]}")
        append_jsonl(JUDGE, {"id": i, **v, "usage": usage, "seconds": round(time.time() - t, 1)})
        log(f"  {i} correct={v['correct']} supported={v['supported']}  {v['reason'][:90]}")


# ===================================================================== 5. results + agreement

def classify(q: dict, c: dict, v: dict) -> tuple[str, str]:
    """(outcome, suggested failure cause). 'bad test question' needs a human."""
    if q["kind"] == "unanswerable":
        if c["refusal"] and v["supported"]:
            return "correct_refusal", ""
        if c["refusal"]:
            return "correct_refusal_unsupported", "unsupported claim"
        return "missed_refusal", "unsupported claim"
    if c["refusal"]:
        return "wrong_refusal", "retrieval miss" if not c["expected_retrieved"] else "wrong refusal"
    if v["correct"] and v["supported"]:
        return "correct", ""
    if v["correct"]:
        return "correct_unsupported", "unsupported claim"
    if not c["expected_retrieved"]:
        return "wrong", "retrieval miss"
    return "wrong", "wrong answer from right passage" if v["supported"] else "unsupported claim"


def cohen_kappa(a: list[int], b: list[int]) -> float | None:
    n = len(a)
    if not n:
        return None
    po = sum(x == y for x, y in zip(a, b)) / n
    pa, pb = sum(a) / n, sum(b) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return round((po - pe) / (1 - pe), 3) if pe < 1 else 1.0


def stage_results() -> dict:
    qs = load_questions()
    answers, verdicts = read_jsonl(ANSWERS), read_jsonl(JUDGE)
    rows = []
    for q in qs:
        r, v = answers.get(q["id"]), verdicts.get(q["id"])
        if not r or not v:
            continue
        c = code_checks(q, r)
        outcome, cause = classify(q, c, v)
        rows.append({"id": q["id"], "kind": q["kind"], **c,
                     "judge_correct": v["correct"], "judge_supported": v["supported"],
                     "outcome": outcome, "suggested_cause": cause,
                     "tokens_in": r["tokens"]["input"], "tokens_out": r["tokens"]["output"],
                     "seconds": r["seconds"], "guardrail": r["guardrail"]["action"],
                     "judge_reason": v["reason"], "unsupported_claims": " | ".join(v["unsupported_claims"])})
    if not rows:
        log("No answers + verdicts yet.")
        return {}
    with RESULTS.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    n = len(rows)
    count = lambda o: sum(1 for r in rows if r["outcome"] == o)  # noqa: E731
    ans = [r for r in rows if r["kind"] != "unanswerable"]
    una = [r for r in rows if r["kind"] == "unanswerable"]
    judge_tokens = sum(v["usage"]["input_tokens"] + v["usage"]["output_tokens"] for v in verdicts.values())
    summary = {
        "questions": n,
        "outcomes": {o: count(o) for o in ["correct", "correct_unsupported", "wrong", "wrong_refusal",
                                            "correct_refusal", "correct_refusal_unsupported", "missed_refusal"]},
        "answerable": {"n": len(ans),
                       "correct_and_supported": sum(r["outcome"] == "correct" for r in ans),
                       "judge_correct": sum(r["judge_correct"] for r in ans),
                       "wrong_refusals": sum(r["outcome"] == "wrong_refusal" for r in ans)},
        "unanswerable": {"n": len(una), "refused": sum(r["refusal"] for r in una),
                         "refused_and_supported": sum(r["outcome"] == "correct_refusal" for r in una)},
        "code_checks": {"citations_valid": sum(r["citations_valid"] for r in rows),
                        "answers_with_citation": sum(r["has_citation"] for r in ans if not r["refusal"]),
                        "non_refusal_answers": sum(1 for r in ans if not r["refusal"]),
                        "expected_passage_retrieved": sum(r["expected_retrieved"] == 1 for r in ans),
                        "expected_passage_cited": sum(r["expected_cited"] == 1 for r in ans),
                        "guardrail_fired": sum(r["guardrail"] != "none" for r in rows)},
        "suggested_causes": {c: sum(r["suggested_cause"] == c for r in rows)
                             for c in sorted({r["suggested_cause"] for r in rows} - {""})},
        "cost_per_question": {"agent_tokens_in": round(sum(r["tokens_in"] for r in rows) / n),
                              "agent_tokens_out": round(sum(r["tokens_out"] for r in rows) / n),
                              "seconds_mean": round(sum(r["seconds"] for r in rows) / n, 1),
                              "seconds_max": max(r["seconds"] for r in rows),
                              "judge_tokens": round(judge_tokens / max(len(verdicts), 1))},
    }

    # agreement with the human labels
    human = []
    if HUMAN.exists():
        with HUMAN.open(newline="", encoding="utf-8") as f:
            human = [h for h in csv.DictReader(f) if h.get("id", "").strip() and h.get("correct", "").strip()]
    pairs = [(h, verdicts[h["id"]]) for h in human if h["id"] in verdicts]
    if pairs:
        agree = {}
        for col in ("correct", "supported"):
            a = [int(h[col]) for h, _ in pairs]
            b = [int(v[col]) for _, v in pairs]
            agree[col] = {"n": len(a), "agreement": round(sum(x == y for x, y in zip(a, b)) / len(a), 3),
                          "cohen_kappa": cohen_kappa(a, b),
                          "disagreements": [h["id"] for (h, v) in pairs if int(h[col]) != int(v[col])]}
        summary["judge_vs_human"] = agree
    else:
        summary["judge_vs_human"] = "eval/human_labels.csv has no grades yet"
    SUMMARY.write_text(json.dumps(summary, indent=1, ensure_ascii=False), encoding="utf-8")
    log(json.dumps(summary, indent=1, ensure_ascii=False))
    return summary


# ===================================================================== 6. add a document

ADD_QUESTION = "q31"  # "My car is 6 years old. How often does it need to pass the ITV inspection?"


def stage_add_document() -> None:
    import agent
    import index as idx
    from server import add_document_impl
    demo = json.loads(ADD_DEMO.read_text(encoding="utf-8")) if ADD_DEMO.exists() else {}
    if demo.get("after"):
        log("Add-document demo already done (eval/add_document_demo.json).")
        return
    answers = read_jsonl(ANSWERS)
    q = next(x for x in load_questions() if x["id"] == ADD_QUESTION)
    if ADD_QUESTION not in answers:
        raise InfraError("Run the answers stage first: the 'before' answer comes from it.")
    before = answers[ADD_QUESTION]
    source, (boe_id, title) = "ITV", idx.EXTRA_DOCUMENTS["ITV"]
    path = idx.download(source, boe_id)
    first = add_document_impl(str(path))
    if first["status"] == "error":
        raise InfraError(first["message"])
    again = add_document_impl(str(path))   # second call: shows the already-indexed policy
    after = agent.ask(q["question"], approve_add=False)
    if any(t["result"].startswith(("Error", "NOTE: keyword search only")) for t in after["trace"]):
        raise InfraError("search failed after adding the document; re-run later")
    demo = {"question": q["question"], "document": {"source": source, "boe_id": boe_id, "title": title,
                                                    "path": str(path.relative_to(ROOT))},
            "before": {"answer": before["answer"], "citations": before["citations"]},
            "add_document": first, "add_document_again": again,
            "after": {"answer": after["answer"], "citations": after["citations"],
                      "searches": [t["args"] for t in after["trace"] if t["tool"] == "search"]}}
    ADD_DEMO.write_text(json.dumps(demo, indent=1, ensure_ascii=False), encoding="utf-8")
    log(f"BEFORE: {before['answer']}\n\nADD: {first}\nAGAIN: {again}\n\nAFTER: {after['answer']}")


STAGES = {"retrieval": stage_retrieval, "answers": stage_answers, "grading-sheet": stage_grading_sheet,
          "judge": stage_judge,
          "results": stage_results, "add-document": stage_add_document}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--stage", choices=[*STAGES, "all"], default="all")
    a = ap.parse_args()
    for name, fn in STAGES.items():
        if a.stage in (name, "all"):
            log(f"\n===== {name}")
            try:
                fn()
            except InfraError as e:
                log(f"\nSTOPPED at {name}: {e}")
                # results are saved up to here; report what exists and exit cleanly
                if name != "results":
                    stage_results()
                return


if __name__ == "__main__":
    sys.path.insert(0, str(ROOT))
    main()
