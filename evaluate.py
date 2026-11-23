"""
Assignment 3: evaluation (`main.py evaluate`).

Stages (each saves to eval/ and is resumable, so a rate limit loses nothing):
  1. Retrieval: hit rate at k = 1, 3, 5 for each design (articles vs fixed200),
     plus words added to the prompt.                      -> eval/retrieval.csv
  2. Agent: run agent.py on every question.               -> eval/answers.jsonl
  3. Code checks: citations valid, refusals right/wrong, expected source cited.
  4. LLM judge with a rubric, retrieved text as evidence. -> eval/judge.jsonl
  5. Agreement judge vs eval/human_labels.csv (if graded).
  6. Before/after demo: add the LPH with add_document and re-ask the question it
     answers (run once; result kept).                     -> eval/add_document_demo.md
  7. Summary with failure categories, tokens and seconds.  -> eval/summary.md, eval/results.csv
"""

from __future__ import annotations

import asyncio
import csv
import json
import os
import sys
import time
from pathlib import Path

import index
from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
ANSWERS = EVAL / "answers.jsonl"
JUDGE = EVAL / "judge.jsonl"
HUMAN = EVAL / "human_labels.csv"
DEMO = EVAL / "add_document_demo.md"
KS = (1, 3, 5)
JUDGE_MODELS = [m for m in os.environ.get("JUDGE_MODELS", "gemini-3-flash-preview,gemini-3.8-flash").split(",") if m]
DEMO_QUESTION_ID = "q34"           # "¿Puede votar en la junta un propietario que debe cuotas de comunidad?"
DEMO_DOC = "BOE-A-1960-10906"      # Ley de Propiedad Horizontal, not in the initial corpus
# retrieval is always measured on the initial corpus, even after documents were added
INITIAL_CORPUS = {"doc_id": {"$in": list(index.DOCUMENTS)}}


def log(*a):
    print(*a, flush=True)


def load_questions() -> list[dict]:
    with QUESTIONS.open(encoding="utf-8", newline="") as f:
        return [r for r in csv.DictReader(f) if r["question"].strip()]


def expected_pairs(q: dict) -> list[tuple[str, str]]:
    srcs = [s.strip() for s in q["expected_source"].split(";") if s.strip()]
    locs = [l.strip() for l in q["expected_location"].split(";") if l.strip()]
    if len(srcs) == 1 and len(locs) > 1:
        srcs = srcs * len(locs)
    return list(zip(srcs, locs))


def key(location: str) -> str:
    return location.lower().split(" [")[0].split(".")[0].strip()


def matches(hit: dict, pair: tuple[str, str]) -> bool:
    return hit["source"] == pair[0] and key(hit["location"]) == key(pair[1])


def read_jsonl(path: Path) -> dict:
    if not path.exists():
        return {}
    return {r["id"]: r for r in (json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip())}


def append_jsonl(path: Path, row: dict) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


# --------------------------------------------------------------------------- 1. retrieval

def retrieval(questions: list[dict]) -> list[dict]:
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    rows = []
    for design in index.DESIGNS:
        hits_any = {k: 0 for k in KS}
        hits_all = {k: 0 for k in KS}
        words, per_q = 0, []
        for q in answerable:
            res = index.search(q["question"], k=max(KS), design=design, where=INITIAL_CORPUS)  # query vectors are cached
            words += sum(len(r["text"].split()) for r in res)
            pairs = expected_pairs(q)
            first = next((i + 1 for i, r in enumerate(res) if any(matches(r, p) for p in pairs)), None)
            per_q.append({"id": q["id"], "design": design, "first_relevant_rank": first})
            for k in KS:
                top = res[:k]
                found = [any(matches(r, p) for r in top) for p in pairs]
                hits_any[k] += any(found)
                hits_all[k] += all(found)
        n = len(answerable)
        row = {"design": design, "questions": n,
               **{f"hit@{k}": round(hits_any[k] / n, 3) for k in KS},
               **{f"all_passages@{k}": round(hits_all[k] / n, 3) for k in KS},
               "words_in_prompt@5": round(words / n)}
        rows.append(row)
        (EVAL / f"retrieval_ranks_{design}.json").write_text(json.dumps(per_q, ensure_ascii=False, indent=1))
    with (EVAL / "retrieval.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    for r in rows:
        log(f"  {r['design']:9s} hit@1 {r['hit@1']:.2f}  hit@3 {r['hit@3']:.2f}  hit@5 {r['hit@5']:.2f}  "
            f"all@5 {r['all_passages@5']:.2f}  words@5 {r['words_in_prompt@5']}")
    return rows


# --------------------------------------------------------------------------- 2. agent

def run_agent(questions: list[dict]) -> dict:
    import agent
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    done = read_jsonl(ANSWERS)
    todo = [q for q in questions if q["id"] not in done]
    if not todo:
        return done

    async def go():
        params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT),
                                       env={**os.environ, "GEMINI_API_KEY": load_api_key()})
        async with stdio_client(params) as (r, w):
            async with ClientSession(r, w) as s:
                await s.initialize()
                for q in todo:
                    try:
                        res = await agent.answer_async(q["question"], s)
                    except Exception as e:  # noqa: BLE001 - keep going, record the failure
                        log(f"  {q['id']} FAILED: {type(e).__name__}: {str(e)[:200]}")
                        continue
                    res["id"] = q["id"]
                    append_jsonl(ANSWERS, res)
                    done[q["id"]] = res
                    log(f"  {q['id']} {res['seconds']:5.1f}s  guard={res['guard']:7s} refusal={res['refusal']}  "
                        f"{res['answer'][:70]!r}")
                    time.sleep(2)

    asyncio.run(go())
    return done


# --------------------------------------------------------------------------- 3. code checks

def code_checks(q: dict, a: dict) -> dict:
    pairs = expected_pairs(q)
    unanswerable = q["kind"] == "unanswerable"
    retrieved_expected = any(matches(h, p) for h in a["hits"] for p in pairs) if pairs else None
    cited_expected = (any(p[0].lower() in c.lower() and key(p[1]) in c.lower()
                          for c in a["valid_citations"] for p in pairs) if pairs else None)
    return {
        "citations_ok": a["refusal"] or (bool(a["valid_citations"]) and not a["invalid_citations"]),
        "correct_refusal": unanswerable and a["refusal"],
        "wrong_refusal": (not unanswerable) and a["refusal"],
        "answered_unanswerable": unanswerable and not a["refusal"],
        "retrieved_expected": retrieved_expected,
        "cited_expected": cited_expected,
    }


# --------------------------------------------------------------------------- 4. judge

RUBRIC = """You grade answers of a legal assistant about Spanish residential rental law.
You get: the QUESTION, the REFERENCE answer written by the test author, the assistant's ANSWER,
and the EVIDENCE (the passages the assistant retrieved). Judge ONLY against the reference and the evidence,
never against your own knowledge of the law.

correct (1/0):
  1 = the answer's main conclusion agrees with the reference and it states no claim that contradicts it.
      Missing minor details is fine; missing a condition that changes the outcome for the user is not.
  1 = for an UNANSWERABLE reference: the answer says the corpus does not cover it and does not
      give a substantive answer anyway.
  0 = wrong or contradicting conclusion, a refusal when the reference has an answer, or a substantive
      answer when the reference says the corpus cannot answer.
supported (1/0):
  1 = every factual legal claim in the answer is stated in the EVIDENCE (paraphrase is fine).
      A pure refusal counts as supported. Generic advice like "consult a lawyer" is not a claim.
  0 = at least one claim is not in the evidence (invented numbers, deadlines, conditions or articles).
Return JSON: {"correct": 0 or 1, "supported": 0 or 1, "reason": "<one sentence; for any 0 say which claim>"}"""


def judge_one(q: dict, a: dict) -> dict:
    from google.genai import types
    evidence = "\n\n".join(a.get("evidence", []))[:30000] or "(nothing retrieved)"
    prompt = (f"QUESTION ({q['kind']}): {q['question']}\n\nREFERENCE: {q['reference_answer']}\n\n"
              f"ANSWER:\n{a['answer']}\n\nEVIDENCE:\n{evidence}")
    config = types.GenerateContentConfig(system_instruction=RUBRIC, temperature=0,
                                         response_mime_type="application/json")
    last = None
    for model in JUDGE_MODELS:
        for attempt in range(4):
            try:
                resp = index.genai_client().models.generate_content(model=model, contents=prompt, config=config)
                v = json.loads(resp.text)
                u = resp.usage_metadata
                return {"correct": int(v["correct"]), "supported": int(v["supported"]),
                        "reason": v.get("reason", ""), "judge_model": model,
                        "judge_tokens": (u.prompt_token_count or 0) + (u.candidates_token_count or 0)}
            except Exception as e:  # noqa: BLE001
                last = e
                if "503" in str(e) or "UNAVAILABLE" in str(e):
                    break  # model overloaded: fall back to the next one
                time.sleep(10 * (attempt + 1))
    raise RuntimeError(f"judge failed: {last}")


def run_judge(questions: list[dict], answers: dict) -> dict:
    done = read_jsonl(JUDGE)
    for q in questions:
        if q["id"] in done or q["id"] not in answers:
            continue
        try:
            v = judge_one(q, answers[q["id"]])
        except Exception as e:  # noqa: BLE001
            log(f"  {q['id']} judge FAILED: {str(e)[:200]}")
            continue
        v["id"] = q["id"]
        append_jsonl(JUDGE, v)
        done[q["id"]] = v
        log(f"  {q['id']} correct={v['correct']} supported={v['supported']} ({v['judge_model']}) {v['reason'][:80]}")
    return done


# --------------------------------------------------------------------------- 5. agreement

def kappa(a: list[int], b: list[int]) -> float | None:
    n = len(a)
    if not n:
        return None
    po = sum(x == y for x, y in zip(a, b)) / n
    pa, pb = sum(a) / n, sum(b) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return round((po - pe) / (1 - pe), 3) if pe < 1 else None


def agreement(verdicts: dict) -> dict:
    if not HUMAN.exists():
        return {}
    with HUMAN.open(encoding="utf-8", newline="") as f:
        human = [r for r in csv.DictReader(f) if r.get("id", "").strip() and r["id"] in verdicts]
    out = {"graded": len(human)}
    for field in ("correct", "supported"):
        h = [int(r[field]) for r in human if r.get(field, "").strip() in ("0", "1")]
        j = [verdicts[r["id"]][field] for r in human if r.get(field, "").strip() in ("0", "1")]
        if h:
            out[field] = {"n": len(h), "agreement": round(sum(x == y for x, y in zip(h, j)) / len(h), 3),
                          "kappa": kappa(h, j),
                          "disagreements": [r["id"] for r, x, y in zip(
                              [r for r in human if r.get(field, "").strip() in ("0", "1")], h, j) if x != y]}
    return out


# --------------------------------------------------------------------------- 6. add-document demo

def remove_demo_doc() -> int:
    """Delete the demo document's chunks from every design (makes the demo repeatable)."""
    n = 0
    for design in index.DESIGNS:
        coll = index.collection(design)
        ids = coll.get(where={"doc_id": DEMO_DOC}, include=[])["ids"]
        if ids:
            coll.delete(ids=ids)
            n += len(ids)
    return n


def add_document_demo(questions: list[dict], answers: dict) -> None:
    if DEMO.exists():
        log("  already done (eval/add_document_demo.md); delete it to redo")
        return
    import agent
    q = next(q for q in questions if q["id"] == DEMO_QUESTION_ID)
    removed = remove_demo_doc()  # start from the initial corpus, so "before" cannot see the document
    if removed:
        log(f"  removed {removed} chunks of {DEMO_DOC} left from an earlier demo")
    before = answers.get(q["id"]) if not removed else None
    before = before or agent.answer(q["question"])
    path = index.download(DEMO_DOC)
    t0 = time.time()
    first = index.index_file(path, designs=(index.DEFAULT_DESIGN,))[index.DEFAULT_DESIGN]
    second = index.index_file(path, designs=(index.DEFAULT_DESIGN,))[index.DEFAULT_DESIGN]  # already indexed
    after = agent.answer(q["question"])
    DEMO.write_text(f"""# Adding a document: before and after

**Question ({q['id']}, unanswerable in the initial corpus):** {q['question']}

**Document added:** {index.EXTRA_DOCUMENTS[DEMO_DOC]} — `corpus/{DEMO_DOC}.xml`
(https://www.boe.es/buscar/act.php?id={DEMO_DOC}), through the same pipeline as `add_document`.

- First add: {first['chunks']} chunks, {first['embedded']} embedded ({time.time() - t0:.0f}s incl. second call).
- Adding it again: {second['embedded']} embedded, {second['removed']} removed — already indexed and unchanged, so nothing is re-embedded.

## Before

{before['answer']}

*Tool calls: {len(before['trace'])}; citation guard: {before['guard']}*

## After

{after['answer']}

*Tool calls: {len(after['trace'])}; citation guard: {after['guard']}; valid citations: {after['valid_citations']}*
""", encoding="utf-8")
    log(f"  wrote {DEMO.relative_to(ROOT)}")


# --------------------------------------------------------------------------- 7. summary

def failure_cause(q, a, c, v) -> str:
    """Suggested category; the final classification is done by hand in REPORT.md."""
    if v is None:
        return "not judged"
    if v["correct"] and v["supported"]:
        return ""
    if c["wrong_refusal"]:
        return "wrong refusal" if c["retrieved_expected"] else "retrieval miss (then refused)"
    if q["kind"] == "unanswerable":
        return "unsupported claim (answered an unanswerable question)"
    if not v["supported"]:
        return "unsupported claim"
    return "wrong answer from the right passage" if c["retrieved_expected"] else "retrieval miss"


def summary(questions, retrieval_rows, answers, verdicts, agree) -> None:
    rows = []
    for q in questions:
        a, v = answers.get(q["id"]), verdicts.get(q["id"])
        if a is None:
            continue
        c = code_checks(q, a)
        rows.append({"id": q["id"], "kind": q["kind"], **c,
                     "judge_correct": v["correct"] if v else "", "judge_supported": v["supported"] if v else "",
                     "judge_reason": v["reason"] if v else "", "guard": a["guard"],
                     "tool_calls": len(a["trace"]), "tokens": a["tokens"]["input"] + a["tokens"]["output"],
                     "seconds": a["seconds"], "suggested_failure": failure_cause(q, a, c, v)})
    if not rows:
        return
    with (EVAL / "results.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)

    n = len(rows)
    ans = [r for r in rows if r["kind"] != "unanswerable"]
    una = [r for r in rows if r["kind"] == "unanswerable"]
    judged = [r for r in rows if r["judge_correct"] != ""]
    s = lambda rs, k: sum(1 for r in rs if r[k] in (True, 1))  # noqa: E731
    fails = {}
    for r in rows:
        if r["suggested_failure"]:
            fails.setdefault(r["suggested_failure"], []).append(r["id"])
    toks = sum(r["tokens"] for r in rows) / n
    secs = sum(r["seconds"] for r in rows) / n
    lines = [
        "# Evaluation summary", "",
        f"Agent model: `{os.environ.get("AGENT_MODEL", "gemini-3.5-flash-lite")}` · judge: `{', '.join(JUDGE_MODELS)}` (fallback order) · "
        f"embeddings: `{index.EMBED_MODEL}` ({index.EMBED_DIM} d) · design served: `{index.DEFAULT_DESIGN}`", "",
        "## Retrieval (answerable questions)", "",
        "| design | hit@1 | hit@3 | hit@5 | all passages@5 (multi) | words in prompt @5 |", "|---|---|---|---|---|---|",
        *[f"| {r['design']} | {r['hit@1']} | {r['hit@3']} | {r['hit@5']} | {r['all_passages@5']} | {r['words_in_prompt@5']} |"
          for r in retrieval_rows], "",
        f"## End to end ({n} questions: {len(ans)} answerable, {len(una)} unanswerable)", "",
        "| metric | value |", "|---|---|",
        f"| judged correct | {s(judged, 'judge_correct')}/{len(judged)} |",
        f"| judged supported | {s(judged, 'judge_supported')}/{len(judged)} |",
        f"| correct refusals (code) | {s(una, 'correct_refusal')}/{len(una)} |",
        f"| answered an unanswerable question (code) | {s(una, 'answered_unanswerable')}/{len(una)} |",
        f"| wrong refusals (code) | {s(ans, 'wrong_refusal')}/{len(ans)} |",
        f"| citations valid (code) | {s(rows, 'citations_ok')}/{n} |",
        f"| expected passage retrieved by the agent (code) | {s(ans, 'retrieved_expected')}/{len(ans)} |",
        f"| expected passage cited (code) | {s(ans, 'cited_expected')}/{len(ans)} |",
        f"| citation guard retried / blocked | {sum(r['guard'] == 'retried' for r in rows)} / {sum(r['guard'] == 'blocked' for r in rows)} |",
        f"| mean tokens per question | {toks:.0f} |",
        f"| mean seconds per question | {secs:.1f} |", "",
        "## Suggested failure causes (check each by hand)", "",
        *([f"- **{k}** ({len(v)}): {', '.join(v)}" for k, v in sorted(fails.items())] or ["- none"]), "",
        "## Judge vs human", "",
    ]
    if agree.get("graded"):
        for field in ("correct", "supported"):
            if field in agree:
                g = agree[field]
                lines.append(f"- **{field}**: {g['agreement']:.0%} agreement on {g['n']} answers "
                             f"(Cohen's κ = {g['kappa']}); disagreements: {', '.join(g['disagreements']) or 'none'}")
    else:
        lines.append("- eval/human_labels.csv has no grades yet.")
    (EVAL / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    (EVAL / "summary.json").write_text(json.dumps({"retrieval": retrieval_rows, "agreement": agree,
                                                    "failures": fails, "mean_tokens": toks,
                                                    "mean_seconds": secs}, ensure_ascii=False, indent=1))
    log("\n" + "\n".join(lines))


def main() -> None:
    EVAL.mkdir(exist_ok=True)
    questions = load_questions()
    log(f"1. Retrieval ({len(questions)} questions)")
    retrieval_rows = retrieval(questions)
    log("2. Agent answers")
    answers = run_agent(questions)
    if "--no-judge" in sys.argv:  # grade by hand first, without the judge's verdicts
        log("3-4. Code checks (LLM judge skipped: --no-judge)")
        verdicts = read_jsonl(JUDGE)
    else:
        log("3-4. Code checks and LLM judge")
        verdicts = run_judge(questions, answers)
    log("5. Agreement with human labels")
    agree = agreement(verdicts)
    if "--demo" in sys.argv or os.environ.get("RUN_ADD_DEMO") == "1":
        log("6. Add-document demo")
        add_document_demo(questions, answers)
    log("7. Summary")
    summary(questions, retrieval_rows, answers, verdicts, agree)


if __name__ == "__main__":
    main()
