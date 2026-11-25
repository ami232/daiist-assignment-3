"""
Assignment 3: evaluation (`main.py evaluate`).

1. Retrieval: hit rate at k = 1, 3, 5 for every design and search method available in index/
   (vector, BM25, hybrid, hybrid + routing filter), and the words each adds to the prompt.
2. End to end: the agent on every question (add_document always refused), code checks
   (refusals, citation validity, expected source cited, guardrail), an LLM judge with the
   rubric in eval/judge_rubric.md and the retrieved text as evidence, a no-retrieval baseline,
   agreement with eval/human_labels.csv, and tokens and seconds per question.

Agent answers, judge verdicts and baseline answers are cached in eval/*.jsonl, keyed by
everything that affects them, so a re-run only spends quota on what changed.
Outputs: eval/retrieval.csv, eval/results.csv, eval/summary.json, eval/summary.md.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import index  # noqa: E402
import retrieval  # noqa: E402

EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
HUMAN = EVAL / "human_labels.csv"
RUBRIC = EVAL / "judge_rubric.md"
ANSWERS = EVAL / "answers.jsonl"
VERDICTS = EVAL / "verdicts.jsonl"
BASELINE = EVAL / "baseline.jsonl"
KS = (1, 3, 5)
JUDGE_MODEL = os.environ.get("JUDGE_MODEL", "gemini-3.8-flash")
EVIDENCE_CHARS = 60000  # 21 chunks x ~1.7k chars; must hold every retrieved passage


def log(*a):
    print(*a, flush=True)


def sha(*parts) -> str:
    return hashlib.sha256("|".join(str(p) for p in parts).encode()).hexdigest()[:16]


def load_jsonl(path: Path) -> dict:
    out = {}
    if path.exists():
        for line in path.read_text().splitlines():
            if line.strip():
                row = json.loads(line)
                out[row["key"]] = row
    return out


def append_jsonl(path: Path, row: dict) -> None:
    with path.open("a") as f:
        f.write(json.dumps(row) + "\n")


def read_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r["question"].strip()]


def targets(row: dict) -> list[tuple[str, str]]:
    """[(doc_id, location)] for an answerable row; one source may cover several locations."""
    srcs = [s.strip() for s in row["expected_source"].split(";") if s.strip()]
    locs = [s.strip() for s in row["expected_location"].split(";") if s.strip()]
    if len(srcs) == 1:
        srcs = srcs * len(locs)
    return list(zip(srcs, locs))


def is_hit(meta: dict, doc_id: str, loc: str) -> bool:
    """The hit rule: same document, and the identifier is in the chunk or the page range overlaps it."""
    if meta["doc_id"] != doc_id:
        return False
    m = re.fullmatch(r"p(\d+)(?:-(\d+))?", loc)
    if m:
        a, b = int(m.group(1)), int(m.group(2) or m.group(1))
        return a <= meta["page_end"] and b >= meta["page_start"]
    return loc in meta["identifiers"].split(";")


# ------------------------------------------------------------------ 1. retrieval
def evaluate_retrieval(rows: list[dict]) -> list[dict]:
    answerable = [r for r in rows if r["kind"] != "unanswerable"]
    designs = []
    for design in index.DESIGNS:
        # Only the original documents: a document added later (the demo) would change BM25's statistics.
        r = retrieval.Retriever(design, only_docs=[d.doc_id for d in index.INDEXED])
        if len(r):
            designs.append((design, r))
    if not designs:
        raise SystemExit("index/ has no embedded chunks. Run `uv run python main.py index` first.")

    new = index.missing([index._embed_input(r["question"], "query") for r in answerable])
    log(f"Retrieval: {len(answerable)} answerable questions; {len(new)} question embeddings not cached yet.")

    configs = []
    for design, r in designs:
        for method in retrieval.METHODS:
            configs.append((design, r, method, False))
        configs.append((design, r, "hybrid", True))

    results = []
    for design, r, method, use_route in configs:
        name = f"{design} {method}" + (" + route" if use_route else "")
        hits = {k: {"single": 0, "multi": 0} for k in KS}
        counts = {"single": 0, "multi": 0}
        words = []
        original = [d.doc_id for d in index.INDEXED]  # documents added later don't change these numbers
        for row in answerable:
            routed = [d for d in retrieval.route(row["question"]) if d in original] if use_route else []
            got = r.search(row["question"], k=max(KS), method=method, doc_ids=routed or original)
            words.append(sum(h.meta["word_count"] for h in got))
            counts[row["kind"]] += 1
            for k in KS:
                top = got[:k]
                if all(any(is_hit(h.meta, d, l) for h in top) for d, l in targets(row)):
                    hits[k][row["kind"]] += 1
        res = {"config": name, "design": design, "method": method, "route": use_route,
               "words_in_prompt_k5": round(sum(words) / len(words))}
        for k in KS:
            total = hits[k]["single"] + hits[k]["multi"]
            res[f"hit@{k}"] = round(total / len(answerable), 3)
            res[f"single_hit@{k}"] = round(hits[k]["single"] / max(counts["single"], 1), 3)
            res[f"multi_hit@{k}"] = round(hits[k]["multi"] / max(counts["multi"], 1), 3)
        results.append(res)
        log(f"  {name:<24} hit@1 {res['hit@1']:.2f}  hit@3 {res['hit@3']:.2f}  hit@5 {res['hit@5']:.2f}  "
            f"(multi, both passages: {res['multi_hit@5']:.2f} at 5)  ~{res['words_in_prompt_k5']} words at k=5")

    with (EVAL / "retrieval.csv").open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(results[0]))
        w.writeheader()
        w.writerows(results)
    return results


# ------------------------------------------------------------------ 2. end to end
def root_cause(e: BaseException) -> str:
    """The innermost error text; MCP/anyio wrap failures in nested ExceptionGroups."""
    while True:
        inner = getattr(e, "exceptions", None)
        if inner:
            e = inner[0]
        elif e.__cause__ is not None:
            e = e.__cause__
        else:
            return f"{type(e).__name__}: {e}"


def run_answers(rows: list[dict], retriever: retrieval.Retriever) -> dict:
    import agent

    cache = load_jsonl(ANSWERS)
    prompt_hash = sha((ROOT / "AGENTS.md").read_text(), json.dumps(retrieval.CHOSEN, sort_keys=True))
    out = {}
    todo = [r for r in rows if sha(r["id"], r["question"], agent.AGENT_MODEL, prompt_hash) not in cache]
    log(f"\nAgent ({agent.AGENT_MODEL}): {len(rows) - len(todo)} answers cached, {len(todo)} to run.")
    for r in rows:
        key = sha(r["id"], r["question"], agent.AGENT_MODEL, prompt_hash)
        if key not in cache:
            log(f"  {r['id']} ...")
            try:
                res = agent.run_agent(r["question"], approve=agent.deny_all, retriever=retriever)
            except Exception as e:  # a failed run is a result, not a crash of the evaluation
                cause = root_cause(e)
                log(f"  {r['id']} failed: {cause[:300]}")
                if "per day" in cause.lower() or "PerDay" in cause:
                    log("  Daily request quota exhausted: stopping. Cached answers are kept; re-run later.")
                    break
                continue
            cache[key] = {"key": key, "id": r["id"], **res}
            append_jsonl(ANSWERS, cache[key])
        out[r["id"]] = cache[key]
    return out


def evidence(chunk_ids: list[str], retriever: retrieval.Retriever) -> str:
    parts = []
    for cid in chunk_ids:
        i = retriever.by_id.get(cid)
        if i is not None:
            m = retriever.metas[i]
            # Same header facts the search tool showed the agent (title, version, printed page, section).
            parts.append(f"[{m['doc_id']}, {retrieval.page_ref(m)}; identifiers: {m['identifiers'] or 'none'}]\n"
                         f"Document: {m['doc_title']} (version {m['doc_version']}) | printed page {m['page_label']}"
                         + (f" | section: {m['section']}" if m["section"] else "") + "\n"
                         f"{retriever.texts[i]}")
    text = "\n\n".join(parts) or "(no passages retrieved)"
    return text[:EVIDENCE_CHARS]


def judge_model():
    from langchain_google_genai import ChatGoogleGenerativeAI
    from pydantic import BaseModel, Field

    from api_key import load_api_key

    class Verdict(BaseModel):
        correct: int = Field(description="1 or 0, per the rubric")
        supported: int = Field(description="1 or 0, per the rubric")
        reason: str = Field(description="one sentence")

    load_api_key()
    return ChatGoogleGenerativeAI(model=JUDGE_MODEL, temperature=0, max_retries=6).with_structured_output(Verdict)


def run_judge(rows: list[dict], answers: dict, retriever: retrieval.Retriever) -> dict:
    rubric = RUBRIC.read_text(encoding="utf-8")
    cache = load_jsonl(VERDICTS)
    model, out = None, {}
    for r in rows:
        a = answers.get(r["id"])
        if not a:
            continue
        ev = evidence(a["retrieved_chunk_ids"], retriever)
        key = sha(r["id"], r["reference_answer"], a["answer"], ev, rubric, JUDGE_MODEL)
        if key not in cache:
            model = model or judge_model()
            msg = (f"{rubric}\n\n# Item\nQuestion: {r['question']}\nKind: {r['kind']}\n"
                   f"Reference answer: {r['reference_answer']}\n\nAssistant answer:\n{a['answer']}\n\n"
                   f"Retrieved passages:\n{ev}")
            v = model.invoke(msg)
            cache[key] = {"key": key, "id": r["id"], "judge": JUDGE_MODEL,
                          "correct": int(v.correct), "supported": int(v.supported), "reason": v.reason}
            append_jsonl(VERDICTS, cache[key])
        out[r["id"]] = cache[key]
    return out


def run_baseline(rows: list[dict]) -> dict:
    """The same model without retrieval, to show what the index adds over what the model already knows."""
    import agent
    from langchain_google_genai import ChatGoogleGenerativeAI

    rubric = RUBRIC.read_text(encoding="utf-8")
    cache = load_jsonl(BASELINE)
    system = ("Answer questions about NIST AI 100-1, NIST AI 600-1, NIST SP 800-61r3 and NIST SP 800-218 "
              "from your own knowledge, briefly. If you do not know, reply exactly: "
              f"\"{retrieval.REFUSAL}\"")
    model = judge = None
    out = {}
    for r in rows:
        key = sha("baseline", r["id"], r["question"], agent.AGENT_MODEL, JUDGE_MODEL, rubric)
        if key not in cache:
            model = model or agent._model()
            judge = judge or judge_model()
            ans = model.invoke([("system", system), ("user", r["question"])])
            text = agent._text(ans).strip()
            v = judge.invoke(f"{rubric}\n\nFor this item no passages were retrieved: grade `correct` only, "
                             f"and set `supported` to 0.\n\n# Item\nQuestion: {r['question']}\nKind: {r['kind']}\n"
                             f"Reference answer: {r['reference_answer']}\n\nAssistant answer:\n{text}")
            cache[key] = {"key": key, "id": r["id"], "answer": text, "correct": int(v.correct),
                          "refusal": text.startswith(retrieval.REFUSAL), "reason": v.reason}
            append_jsonl(BASELINE, cache[key])
        out[r["id"]] = cache[key]
    return out


def agreement(results: list[dict]) -> dict:
    if not HUMAN.exists():
        return {"n": 0}
    with HUMAN.open(newline="", encoding="utf-8") as f:
        human = {r["id"].strip(): r for r in csv.DictReader(f) if (r.get("id") or "").strip()}
    pairs = {"correct": [], "supported": []}
    for res in results:
        h = human.get(res["id"])
        if not h or res.get("judge_correct") == "":
            continue
        for k in pairs:
            if (h.get(k) or "").strip() in ("0", "1"):
                pairs[k].append((int(h[k]), int(res[f"judge_{k}"])))

    def stats(p):
        if not p:
            return {"n": 0}
        agree = sum(a == b for a, b in p) / len(p)
        pa = sum(a for a, _ in p) / len(p)
        pb = sum(b for _, b in p) / len(p)
        pe = pa * pb + (1 - pa) * (1 - pb)
        kappa = (agree - pe) / (1 - pe) if pe < 1 else 1.0
        return {"n": len(p), "agreement": round(agree, 3), "cohen_kappa": round(kappa, 3)}
    out = {k: stats(v) for k, v in pairs.items()}
    out["disagreements"] = [res["id"] for res in results if res["id"] in human and any(
        (human[res["id"]].get(k) or "").strip() in ("0", "1") and res.get(f"judge_{k}") != ""
        and int(human[res["id"]][k]) != int(res[f"judge_{k}"]) for k in ("correct", "supported"))]
    return out


def failure_hint(row: dict, a: dict, v: dict, retriever: retrieval.Retriever) -> str:
    """A first guess at the failure category, from code; the final classification is done by hand."""
    unans = row["kind"] == "unanswerable"
    refused = a["citation_check"]["refusal"]
    if v["correct"] and v["supported"]:
        return ""
    if unans:
        return "answered an unanswerable question" if not refused else "judge disagreement (refusal)"
    retrieved = [retriever.metas[retriever.by_id[c]] for c in a["retrieved_chunk_ids"] if c in retriever.by_id]
    found = all(any(is_hit(m, d, l) for m in retrieved) for d, l in targets(row))
    if refused:
        return "wrong refusal" + ("" if found else " (retrieval miss)")
    if not found:
        return "retrieval miss"
    if not v["supported"]:
        return "unsupported claim"
    return "wrong answer from the right passage"


def write_grading_sheet(rows: list[dict], answers: dict, retriever: retrieval.Retriever) -> Path:
    """Answers and their evidence, for grading eval/human_labels.csv before seeing the judge."""
    path = EVAL / "answers_for_grading.md"
    out = ["# Answers to grade (fill eval/human_labels.csv before reading eval/verdicts.jsonl)", ""]
    for r in rows:
        a = answers.get(r["id"])
        if not a:
            continue
        out += [f"## {r['id']} ({r['kind']})", f"**Question:** {r['question']}", "",
                f"**Reference:** {r['reference_answer']}", "", f"**Answer:**\n\n{a['answer']}", "",
                "<details><summary>Retrieved passages</summary>\n", "```", evidence(a["retrieved_chunk_ids"], retriever),
                "```", "</details>", ""]
    path.write_text("\n".join(out))
    return path


def main() -> None:
    answers_only = "--answers-only" in sys.argv
    rows = read_questions()
    log("=" * 80 + "\n1. Retrieval\n" + "=" * 80)
    ret = evaluate_retrieval(rows)

    log("\n" + "=" * 80 + "\n2. End to end\n" + "=" * 80)
    retriever = retrieval.Retriever(retrieval.CHOSEN["design"])
    log(f"Served configuration: {retrieval.CHOSEN}")
    answers = run_answers(rows, retriever)
    if answers_only:
        log(f"\nAnswers only: wrote {write_grading_sheet(rows, answers, retriever).relative_to(ROOT)}. "
            "Grade eval/human_labels.csv, then run `main.py evaluate` for the judge.")
        return
    verdicts = run_judge(rows, answers, retriever)
    baseline = run_baseline(rows)

    results = []
    for r in rows:
        a, v, b = answers.get(r["id"]), verdicts.get(r["id"]), baseline.get(r["id"], {})
        if not a or not v:
            results.append({"id": r["id"], "kind": r["kind"], "status": "not run"})
            continue
        chk = retrieval.check_citations(a["answer"], a["retrieved_chunk_ids"], retriever)  # current checker
        srcs = {d for d, _ in targets(r)} if r["kind"] != "unanswerable" else set()
        results.append({
            "id": r["id"], "kind": r["kind"], "status": "ok",
            "refusal": int(chk["refusal"]),
            "correct_refusal": int(r["kind"] == "unanswerable" and chk["refusal"]),
            "wrong_refusal": int(r["kind"] != "unanswerable" and chk["refusal"]),
            "n_citations": chk["n_citations"], "invalid_citations": len(chk["invalid"]),
            "cites_expected_sources": int(bool(srcs) and srcs <= set(chk["cited_docs"])),
            "guardrail_fired": int(a["guardrail"]["fired"]), "guardrail_withheld": int(a["guardrail"]["withheld"]),
            "judge_correct": v["correct"], "judge_supported": v["supported"], "judge_reason": v["reason"],
            "baseline_correct": b.get("correct", ""), "baseline_refusal": int(b.get("refusal", False)),
            "tool_calls": len(a["tool_calls"]), "input_tokens": a["usage"]["input_tokens"],
            "output_tokens": a["usage"]["output_tokens"], "seconds": a["seconds"],
            "failure_hint": failure_hint(r, a, v, retriever),
            "answer": a["answer"],
        })
    with (EVAL / "results.csv").open("w", newline="") as f:
        fields = sorted({k for res in results for k in res}, key=lambda k: list(results[0]).index(k)
                        if k in results[0] else 99)
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(results)

    done = [x for x in results if x["status"] == "ok"]
    n = len(done) or 1
    unans = [x for x in done if x["kind"] == "unanswerable"]
    answerable = [x for x in done if x["kind"] != "unanswerable"]
    non_refusals = [x for x in done if not x["refusal"]]
    summary = {
        "served_config": retrieval.CHOSEN,
        "agent_model": answers[next(iter(answers))]["model"] if answers else None,
        "judge_model": JUDGE_MODEL,
        "questions": len(rows), "evaluated": len(done),
        "retrieval": ret,
        "correct": round(sum(x["judge_correct"] for x in done) / n, 3),
        "supported": round(sum(x["judge_supported"] for x in done) / n, 3),
        "unsupported_answers": sum(1 for x in non_refusals if not x["judge_supported"]),
        "correct_refusals": f"{sum(x['correct_refusal'] for x in unans)}/{len(unans)}",
        "wrong_refusals": f"{sum(x['wrong_refusal'] for x in answerable)}/{len(answerable)}",
        "answered_unanswerable": f"{sum(1 for x in unans if not x['refusal'])}/{len(unans)}",
        "answers_with_invalid_citations": sum(1 for x in done if x["invalid_citations"]),
        "guardrail_fired": sum(x["guardrail_fired"] for x in done),
        "guardrail_withheld": sum(x["guardrail_withheld"] for x in done),
        "baseline_correct": round(sum(x["baseline_correct"] or 0 for x in done) / n, 3),
        "per_question": {
            "input_tokens": round(sum(x["input_tokens"] for x in done) / n),
            "output_tokens": round(sum(x["output_tokens"] for x in done) / n),
            "seconds": round(sum(x["seconds"] for x in done) / n, 1),
            "tool_calls": round(sum(x["tool_calls"] for x in done) / n, 2),
        },
        "failures": {h: [x["id"] for x in done if x["failure_hint"] == h]
                     for h in sorted({x["failure_hint"] for x in done if x["failure_hint"]})},
        "judge_tags": {t: [x["id"] for x in done if t in x["judge_reason"]]
                       for t in ("PARTIAL:", "RETRIEVAL-MISS", "WRONG-REFUSAL", "CITATION-MISMATCH")},
        "human_agreement": agreement(done),
    }
    (EVAL / "summary.json").write_text(json.dumps(summary, indent=2))

    md = ["# Evaluation summary", "", f"Served: `{retrieval.CHOSEN}` | agent `{summary['agent_model']}` | "
          f"judge `{JUDGE_MODEL}`", "", "## Retrieval (hit rate, answerable questions; multi = both passages)", "",
          "| config | hit@1 | hit@3 | hit@5 | multi hit@5 | words at k=5 |", "|---|---|---|---|---|---|"]
    md += [f"| {x['config']} | {x['hit@1']} | {x['hit@3']} | {x['hit@5']} | {x['multi_hit@5']} | "
           f"{x['words_in_prompt_k5']} |" for x in ret]
    md += ["", "## End to end", ""] + [f"- **{k}**: {summary[k]}" for k in (
        "evaluated", "correct", "supported", "unsupported_answers", "correct_refusals", "wrong_refusals",
        "answered_unanswerable", "answers_with_invalid_citations", "guardrail_fired", "guardrail_withheld",
        "baseline_correct")]
    md += [f"- **per question**: {summary['per_question']}", f"- **failure hints**: {summary['failures']}",
           f"- **judge tags**: {summary['judge_tags']}",
           f"- **human vs judge**: {summary['human_agreement']}"]
    (EVAL / "summary.md").write_text("\n".join(md) + "\n")
    log("\n" + "\n".join(md))


if __name__ == "__main__":
    main()
