"""
Assignment 3: evaluation (`main.py evaluate`).

1. Retrieval: hit rate at k = 1, 3, 5 for each design (structured vs fixed chunks) and
   search mode (dense, keyword BM25, hybrid), on the answerable questions. The best one
   by the numbers is written to index/config.json, which server.py uses.
2. End to end: the agent (agent.py, through server.py over MCP) answers every question on
   the base corpus. Answers are saved to eval/answers.jsonl as they come, and re-runs only
   ask the questions that have no saved answer, so this stage is repeatable on the free tier.
3. Code checks: citations valid (every cited source was returned by search), refusals
   detected (the exact refusal sentence), and whether the expected article was cited.
4. LLM judge with a rubric and the retrieved passages as evidence (eval/judge.jsonl, cached).
5. Agreement between the judge and the human grades in eval/human_labels.csv.
6. Failure classes and cost per question.
7. Add-document demo: answer an unanswerable question, add a document through the MCP
   add_document tool, answer again (eval/add_document_demo.json).

Writes eval/retrieval.csv, eval/results.csv, eval/summary.json and eval/summary.md.
"""

from __future__ import annotations

import asyncio
import csv
import json
import re
import sys
import time
from pathlib import Path

from agent import CorpusAgent, REFUSAL, check_citations
from api_key import load_api_key
from rag import CONFIG_FILE, DESIGNS, Searcher, log

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
ANSWERS = EVAL / "answers.jsonl"
JUDGE = EVAL / "judge.jsonl"
HUMAN = EVAL / "human_labels.csv"
OVERRIDES = EVAL / "failure_overrides.csv"
DEMO = EVAL / "add_document_demo.json"
ADDED_DOC = ROOT / "docs_to_add" / "SCC_2021_915.pdf"
ADDED_DOC_ID = "SCC 2021/915"
DEMO_QUESTION_ID = "u01"
MODES = ("dense", "bm25", "hybrid")
KS = (1, 3, 5)
JUDGE_MODELS = ["gemini-3.1-flash-lite"]  # one judge for every answer; a different model version from the agent (3.5-flash-lite); bigger models allow only 20 free requests a day


def load_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r["question"].strip()]


def expected(q: dict) -> list[tuple[str, str]]:
    sources = [s.strip() for s in q["expected_source"].split(";")]
    locations = [s.strip() for s in q["expected_location"].split(";")]
    if len(sources) == 1 and len(locations) > 1:
        sources = sources * len(locations)
    return list(zip(sources, locations))


def chunk_matches(meta: dict, source: str, location: str) -> bool:
    return meta["doc_id"] == source and location in meta.get("locations", meta["location"]).split("|")


def read_jsonl(path: Path) -> dict:
    if not path.is_file():
        return {}
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return {r["id"]: r for r in rows}


def append_jsonl(path: Path, row: dict) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


# ================================================================ 1. retrieval

def retrieval(questions: list[dict]) -> tuple[list[dict], dict]:
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    rows = []
    import os
    os.environ["CORPUS_EXCLUDE"] = ADDED_DOC_ID   # measure the base corpus, not the document added in the demo
    for design in DESIGNS:
        searcher = Searcher(design)
        if not searcher.ids:
            log(f"retrieval: design {design} has no chunks in index/, skipped")
            continue
        for mode in MODES:
            hits = {k: 0 for k in KS}
            all_hits = {k: 0 for k in KS}
            multi = [q for q in answerable if q["kind"] == "multi"]
            prompt_words = []
            for q in answerable:
                results = searcher.search(q["question"], k=max(KS), mode=mode)
                prompt_words.append(sum(r["words"] for r in results))
                for k in KS:
                    found = [any(chunk_matches(r, s, l) for r in results[:k]) for s, l in expected(q)]
                    hits[k] += any(found)
                    if q["kind"] == "multi":
                        all_hits[k] += all(found)
            n = len(answerable)
            rows.append({
                "design": design, "mode": mode, "chunks": len(searcher.ids),
                **{f"hit@{k}": round(hits[k] / n, 3) for k in KS},
                **{f"multi_both@{k}": round(all_hits[k] / max(len(multi), 1), 3) for k in KS},
                "avg_words_in_prompt@5": round(sum(prompt_words) / n),
            })
            log(f"retrieval {design:10s} {mode:6s} " + "  ".join(f"hit@{k}={rows[-1][f'hit@{k}']:.2f}" for k in KS))
    os.environ.pop("CORPUS_EXCLUDE", None)
    with (EVAL / "retrieval.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    # choose by the numbers: hit@5, then hit@3, then hit@1, then fewer words in the prompt
    best = max(rows, key=lambda r: (r["hit@5"], r["hit@3"], r["hit@1"], -r["avg_words_in_prompt@5"]))
    config = {"design": best["design"], "mode": best["mode"], "k": 5}
    CONFIG_FILE.write_text(json.dumps(config, indent=2) + "\n")
    log(f"chosen: {config}")
    return rows, config


# ================================================================ 2. answers

async def answer_all(questions: list[dict]) -> dict:
    saved = read_jsonl(ANSWERS)
    todo = [q for q in questions if q["id"] not in saved]
    if todo:
        log(f"agent: answering {len(todo)} questions ({len(saved)} already saved)")
        async with CorpusAgent(approve=lambda path: False, server_env={"CORPUS_EXCLUDE": ADDED_DOC_ID}) as agent:
            for q in todo:
                try:
                    for attempt in range(3):   # Gemini sometimes answers 503 "high demand"; wait and retry
                        try:
                            result = await agent.ask(q["question"])
                            break
                        except Exception as error:  # noqa: BLE001
                            if "503" not in str(error) or attempt == 2:
                                raise
                            await asyncio.sleep(30)
                except Exception as error:  # noqa: BLE001 - keep going, record the failure
                    log(f"  {q['id']}: error {type(error).__name__}: {str(error)[:200]}")
                    if "RESOURCE_EXHAUSTED" in str(error) and "PerDay" in str(error):
                        log("  daily model quota reached; run evaluate again later to finish")
                        break
                    continue
                result["id"] = q["id"]
                append_jsonl(ANSWERS, result)
                saved[q["id"]] = result
                log(f"  {q['id']}: {result['seconds']}s, guardrail {result['guardrail']}: {result['answer'][:90]!r}")
    return saved


# ================================================================ 4. judge

RUBRIC = """You grade answers from a legal research assistant for EU data-protection law.
You get the question, a reference answer written from the source texts, the passages the
assistant retrieved (the only evidence it was allowed to use), and its answer.

Grade two things, each 0 or 1:

correct
  1 = the answer gives the key facts of the reference answer (numbers, deadlines, conditions)
      without contradicting it. Extra correct detail is fine; a missing minor detail is fine;
      a missing or wrong key condition, number or deadline is 0.
  For a question the reference marks as not covered by the corpus: 1 only if the answer says
      the corpus does not cover it (it may add cited, related context); 0 if it answers as
      if the corpus covered it.
  A refusal ("The corpus does not cover this.") to a question the reference answers is 0.

supported
  1 = every factual claim in the answer is stated in the retrieved passages (paraphrase is
      fine). 0 = at least one claim is not in the passages, even if it is true in reality.
      A pure refusal is supported (1).

Reply with JSON only: {"correct": 0 or 1, "supported": 0 or 1, "reason": "one sentence"}"""


def evidence_of(answer: dict, limit: int = 12000) -> str:
    text = "\n\n".join(t["result"] for t in answer["trace"] if t["tool"] == "search")
    return text[:limit] or "(nothing retrieved)"


def judge_all(questions: list[dict], answers: dict) -> dict:
    from google import genai
    from google.genai import types

    saved = read_jsonl(JUDGE)
    todo = [q for q in questions if q["id"] in answers and q["id"] not in saved]
    if not todo:
        return saved
    client = genai.Client(api_key=load_api_key())
    log(f"judge: grading {len(todo)} answers")
    for q in todo:
        a = answers[q["id"]]
        prompt = (f"QUESTION:\n{q['question']}\n\nREFERENCE ANSWER:\n{q['reference_answer']}\n\n"
                  f"RETRIEVED PASSAGES:\n{evidence_of(a)}\n\nASSISTANT'S ANSWER:\n{a['answer']}")
        for attempt in range(9):
            model = JUDGE_MODELS[min(attempt // 3, len(JUDGE_MODELS) - 1)]
            try:
                response = client.models.generate_content(
                    model=model, contents=prompt,
                    config=types.GenerateContentConfig(system_instruction=RUBRIC, temperature=0,
                                                       response_mime_type="application/json"))
                verdict = json.loads(response.text)
                usage = response.usage_metadata
                break
            except Exception as error:  # noqa: BLE001
                if attempt == 8:
                    raise
                log(f"  judge {model}: {str(error)[:80]}")
                time.sleep(5 if ("503" in str(error) or "404" in str(error) or "PerDay" in str(error)) else 20)
        row = {"id": q["id"], "correct": int(verdict["correct"]), "supported": int(verdict["supported"]),
               "reason": verdict.get("reason", ""), "judge_model": model,
               "judge_tokens": (usage.prompt_token_count or 0) + (usage.candidates_token_count or 0)}
        append_jsonl(JUDGE, row)
        saved[q["id"]] = row
        log(f"  {q['id']}: correct={row['correct']} supported={row['supported']}  {row['reason'][:80]}")
    return saved


# ================================================================ 3 + 6. code checks, outcomes, failures

def outcome(q: dict, a: dict, j: dict) -> tuple[str, dict]:
    check = check_citations(a["answer"], set(a["retrieved_cites"]))
    retrieved = set(re.findall(r"document: (.+?) \| covers: (.+)", evidence_of(a, limit=10**9)))
    retrieved_locs = {(doc, loc.strip()) for doc, locs in retrieved for loc in locs.split(";")}
    exp = expected(q) if q["kind"] != "unanswerable" else []
    retrieved_expected = [(s, l) in retrieved_locs for s, l in exp]
    cited_locs = {(doc, loc) for c in check["citations"] for doc, loc in [cited_units(c)] for loc in loc}
    cited_expected = any((s, l) in cited_locs for s, l in exp)
    codes = {
        "refusal": check["refusal"],
        "citations_valid": not check["invalid"],
        "uncited": check["uncited"],
        "expected_retrieved": all(retrieved_expected) if exp else None,
        "expected_cited": cited_expected if exp else None,
    }
    if q["kind"] == "unanswerable":
        result = "correct refusal" if check["refusal"] else "answered unanswerable"
    elif check["refusal"]:
        result = "wrong refusal"
    elif not j["supported"] or check["invalid"]:
        result = "unsupported"
    elif j["correct"]:
        result = "correct"
    else:
        result = "incorrect"
    return result, codes


def cited_units(cite: str) -> tuple[str, set[str]]:
    """'GDPR, Recitals 26-28' -> ('GDPR', {'Recital 26', 'Recital 27', 'Recital 28'});
    'GDPR, Article 33(1)' -> ('GDPR', {'Article 33'})."""
    doc, _, rest = cite.partition(",")
    rest = re.sub(r",? p\. \d+$", "", rest.strip())
    if m := re.fullmatch(r"Recitals? (\d+)(?:-(\d+))?", rest):
        first, last = int(m.group(1)), int(m.group(2) or m.group(1))
        return doc.strip(), {f"Recital {n}" for n in range(first, last + 1)}
    return doc.strip(), {re.sub(r"(\(\w{1,4}\))+$", "", rest).strip()}


def failure_cause(q: dict, result: str, codes: dict) -> str:
    if result in ("correct", "correct refusal"):
        return ""
    if result == "answered unanswerable":
        return "unsupported claim"
    if not codes["expected_retrieved"]:
        return "retrieval miss"
    return {"wrong refusal": "wrong refusal", "unsupported": "unsupported claim",
            "incorrect": "wrong answer from the right passage"}[result]


def overrides() -> dict:
    if not OVERRIDES.is_file():
        return {}
    with OVERRIDES.open(newline="", encoding="utf-8") as f:
        return {r["id"]: r for r in csv.DictReader(f) if r.get("id")}


# ================================================================ 5. agreement

def agreement(judge: dict) -> dict:
    if not HUMAN.is_file():
        return {"graded": 0}
    with HUMAN.open(newline="", encoding="utf-8") as f:
        human = [r for r in csv.DictReader(f) if r.get("id") and str(r.get("correct", "")).strip() in ("0", "1")]
    pairs = [(r, judge[r["id"]]) for r in human if r["id"] in judge]
    out = {"graded": len(pairs)}
    for field in ("correct", "supported"):
        h = [int(r[field]) for r, _ in pairs if str(r.get(field, "")).strip() in ("0", "1")]
        jv = [j[field] for r, j in pairs if str(r.get(field, "")).strip() in ("0", "1")]
        if not h:
            continue
        agree = sum(a == b for a, b in zip(h, jv)) / len(h)
        pe = (sum(h) / len(h)) * (sum(jv) / len(jv)) + (1 - sum(h) / len(h)) * (1 - sum(jv) / len(jv))
        kappa = (agree - pe) / (1 - pe) if pe < 1 else 1.0
        out[field] = {"agreement": round(agree, 3), "kappa": round(kappa, 3),
                      "disagreements": [r["id"] for (r, j) in pairs if str(r.get(field, "")).strip() in ("0", "1")
                                        and int(r[field]) != j[field]]}
    return out


# ================================================================ 7. add-document demo

async def add_document_demo(questions: list[dict]) -> dict:
    if DEMO.is_file():
        return json.loads(DEMO.read_text())
    question = next(q for q in questions if q["id"] == DEMO_QUESTION_ID)["question"]
    log("demo: answering before the document is added")
    async with CorpusAgent(approve=lambda p: False, server_env={"CORPUS_EXCLUDE": ADDED_DOC_ID}) as agent:
        before = await agent.ask(question)
    log("demo: adding the document through the MCP add_document tool")
    async with CorpusAgent(approve=lambda p: False) as agent:
        first = await agent.session.call_tool("add_document", {"path": str(ADDED_DOC.relative_to(ROOT))})
        again = await agent.session.call_tool("add_document", {"path": str(ADDED_DOC.relative_to(ROOT))})
        after = await agent.ask(question)
    demo = {
        "question_id": DEMO_QUESTION_ID, "question": question, "document": str(ADDED_DOC.relative_to(ROOT)),
        "before": {k: before[k] for k in ("answer", "retrieved_cites", "guardrail")},
        "add_document_result": first.content[0].text,
        "add_document_again_result": again.content[0].text,
        "after": {k: after[k] for k in ("answer", "retrieved_cites", "guardrail")},
    }
    DEMO.write_text(json.dumps(demo, indent=2, ensure_ascii=False))
    return demo


# ================================================================ main

def pct(x: float) -> str:
    return f"{100 * x:.0f}%"


def main() -> None:
    questions = load_questions()
    by_id = {q["id"]: q for q in questions}
    retrieval_rows, config = retrieval(questions)

    answers = asyncio.run(answer_all(questions))
    judge = judge_all(questions, answers)
    over = overrides()

    results = []
    for q in questions:
        if q["id"] not in answers or q["id"] not in judge:
            continue
        a, j = answers[q["id"]], judge[q["id"]]
        result, codes = outcome(q, a, j)
        cause = failure_cause(q, result, codes)
        note = ""
        if q["id"] in over:
            cause, note = over[q["id"]]["cause"], over[q["id"]].get("note", "")
        results.append({
            "id": q["id"], "kind": q["kind"], "result": result, "failure_cause": cause, "note": note,
            "judge_correct": j["correct"], "judge_supported": j["supported"], "judge_reason": j["reason"],
            **codes, "guardrail": a["guardrail"], "tool_calls": a["tool_calls"],
            "tokens": a["input_tokens"] + a["output_tokens"], "seconds": a["seconds"],
            "question": q["question"], "answer": a["answer"],
        })
    if results:
        with (EVAL / "results.csv").open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(results[0]))
            writer.writeheader()
            writer.writerows(results)

    demo = asyncio.run(add_document_demo(questions)) if len(results) == len(questions) else None

    n = len(results)
    count = lambda key, value: sum(1 for r in results if r[key] == value)  # noqa: E731
    answerable = [r for r in results if r["kind"] != "unanswerable"]
    unanswerable = [r for r in results if r["kind"] == "unanswerable"]
    summary = {
        "questions": len(questions), "answered": n, "chosen_config": config,
        "retrieval": retrieval_rows,
        "outcomes": {k: count("result", k) for k in
                     ("correct", "incorrect", "unsupported", "wrong refusal", "correct refusal", "answered unanswerable")},
        "code_checks": {
            "citations_valid": sum(r["citations_valid"] for r in results),
            "uncited_non_refusals": sum(r["uncited"] for r in results),
            "expected_article_cited": sum(bool(r["expected_cited"]) for r in answerable),
            "answerable": len(answerable), "unanswerable": len(unanswerable),
            "guardrail": {g: count("guardrail", g) for g in ("passed", "repaired", "blocked")},
        },
        "judge": {"correct": sum(r["judge_correct"] for r in results), "supported": sum(r["judge_supported"] for r in results)},
        "failures": {},
        "agreement": agreement(judge),
        "cost": {
            "avg_tokens": round(sum(r["tokens"] for r in results) / max(n, 1)),
            "avg_seconds": round(sum(r["seconds"] for r in results) / max(n, 1), 1),
            "avg_tool_calls": round(sum(r["tool_calls"] for r in results) / max(n, 1), 2),
            "avg_judge_tokens": round(sum(judge[r["id"]]["judge_tokens"] for r in results) / max(n, 1)),
        },
        "add_document_demo": demo,
    }
    for r in results:
        if r["failure_cause"]:
            summary["failures"].setdefault(r["failure_cause"], []).append(r["id"])
    (EVAL / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    write_markdown(summary, results)
    print(f"\nEvaluated {n}/{len(questions)} questions with design={config['design']} mode={config['mode']}.")
    for k, v in summary["outcomes"].items():
        print(f"  {k:24s} {v}")
    print(f"  agreement with human grades: {summary['agreement']}")
    print(f"  avg {summary['cost']['avg_tokens']} tokens, {summary['cost']['avg_seconds']}s per question")
    print("Details: eval/summary.md")
    if n < len(questions):
        sys.exit(f"Only {n}/{len(questions)} questions are evaluated; run `main.py evaluate` again to finish.")


def write_markdown(s: dict, results: list[dict]) -> None:
    lines = ["# Evaluation summary", "", "## Retrieval (answerable questions)", "",
             "| design | mode | chunks | hit@1 | hit@3 | hit@5 | both passages@5 (multi) | words in prompt (k=5) |",
             "|---|---|---|---|---|---|---|---|"]
    for r in s["retrieval"]:
        lines.append(f"| {r['design']} | {r['mode']} | {r['chunks']} | {pct(r['hit@1'])} | {pct(r['hit@3'])} | "
                     f"{pct(r['hit@5'])} | {pct(r['multi_both@5'])} | {r['avg_words_in_prompt@5']} |")
    lines += ["", f"Chosen: **{s['chosen_config']['design']} + {s['chosen_config']['mode']}**, k = 5.", "",
              "## End to end", "", "| outcome | count |", "|---|---|"]
    lines += [f"| {k} | {v} |" for k, v in s["outcomes"].items()]
    lines += ["", "## Code checks", "", "```", json.dumps(s["code_checks"], indent=2), "```", "",
              "## Judge agreement with human grades", "", "```", json.dumps(s["agreement"], indent=2), "```", "",
              "## Failures", "", "| cause | count | questions |", "|---|---|---|"]
    lines += [f"| {k} | {len(v)} | {', '.join(v)} |" for k, v in s["failures"].items()]
    lines += ["", "## Cost per question", "", "```", json.dumps(s["cost"], indent=2), "```", "",
              "## Every answer", "", "| id | kind | result | cause | judge reason |", "|---|---|---|---|---|"]
    lines += [f"| {r['id']} | {r['kind']} | {r['result']} | {r['failure_cause']} | {r['judge_reason'].replace('|', '/')} |"
              for r in results]
    (EVAL / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


if __name__ == "__main__":
    main()
