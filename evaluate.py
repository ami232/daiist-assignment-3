"""
Assignment 3: evaluation (`main.py evaluate`). May be evaluate.ipynb instead.

Stage 1: retrieval hit rate at k = 1, 3, 5 for each chunking
design, computed from eval/questions.csv. The question embeddings are cached in
eval/query_cache.json, so re-running (or evaluating a second design) costs no
embedding quota for questions that were already embedded.

Stage 2: the agent (agent.py) answers every question; code checks; failure causes; cost.
Stage 3: LLM judge with a rubric; agreement with eval/human_labels.csv.
Stage 4: add a document that answers an unanswerable question (before / after),
         on a throwaway COPY of the index so the committed index stays clean.

Environment
  DESIGNS=fixed,structure   retrieval designs to compare (default: both indexed ones)
  STAGE=all|retrieval|answers|judge|demo   default all. Do `STAGE=answers` first, grade
                            eval/grading_sheet.md by hand, THEN run `STAGE=judge`.
  FRESH=1                   ignore cached answers / verdicts and ask again
Answers and verdicts are cached in eval/*.json, so a re-run only asks what is missing.
"""

import csv
import hashlib
import json
import os
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
QUERY_CACHE = EVAL / "query_cache.json"
RETRIEVAL_RESULTS = EVAL / "retrieval_results.json"
KS = (1, 3, 5)


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


# --------------------------------------------------------------------------
# Pure functions (no API calls): easy to test
# --------------------------------------------------------------------------
def load_questions(path: Path = QUESTIONS) -> list[dict]:
    with open(path, newline="", encoding="utf-8") as f:
        rows = list(csv.DictReader(f))
    for r in rows:
        r["expected"] = list(zip(
            [s for s in r["expected_source"].split(";") if s],
            [l for l in r["expected_location"].split(";") if l],
        ))
    return rows


def passages_found(expected: list[tuple[str, str]], retrieved: list[dict]) -> int:
    """How many of the expected (source, article) passages appear in the retrieved chunks."""
    got = {(m["source"], m["article"]) for m in retrieved}
    return sum(1 for e in expected if e in got)


def is_hit(expected: list[tuple[str, str]], retrieved: list[dict]) -> bool:
    """Hit = ALL expected passages are among the retrieved chunks (strict for 'multi')."""
    return bool(expected) and passages_found(expected, retrieved) == len(expected)


def hit_rates(questions: list[dict], retrieved: dict[str, list[dict]]) -> dict:
    """retrieved[id] = ranked chunk metadata dicts (with 'words'). Unanswerable questions are skipped."""
    out = {}
    for k in KS:
        entry = {}
        for label, kinds in (("all", ("single", "multi")), ("single", ("single",)), ("multi", ("multi",))):
            qs = [q for q in questions if q["kind"] in kinds]
            hits = [is_hit(q["expected"], retrieved[q["id"]][:k]) for q in qs]
            entry[label] = {"n": len(qs), "hits": sum(hits), "rate": sum(hits) / len(qs) if qs else None}
        multi = [q for q in questions if q["kind"] == "multi"]
        entry["multi_coverage"] = (
            sum(passages_found(q["expected"], retrieved[q["id"]][:k]) / len(q["expected"]) for q in multi) / len(multi)
            if multi else None
        )
        allq = list(questions)
        entry["words_in_prompt"] = sum(sum(m["words"] for m in retrieved[q["id"]][:k]) for q in allq) / len(allq)
        out[k] = entry
    return out


# --------------------------------------------------------------------------
# Retrieval (needs the index and, for new questions, the Gemini API)
# --------------------------------------------------------------------------
def _cache_key(question: str) -> str:
    from index import EMBED_DIM, EMBED_MODEL

    return hashlib.sha1(f"{EMBED_MODEL}|{EMBED_DIM}|{question}".encode()).hexdigest()


def query_vectors(questions: list[str]) -> list[list[float]]:
    """Embed each question once; later runs read eval/query_cache.json."""
    from index import QUERY_PREFIX, embed_texts

    cache = json.loads(QUERY_CACHE.read_text()) if QUERY_CACHE.exists() else {}
    missing = [q for q in dict.fromkeys(questions) if _cache_key(q) not in cache]
    if missing:
        log(f"embedding {len(missing)} new question(s) ({len(questions) - len(missing)} cached)")
        for i in range(0, len(missing), 50):
            batch = missing[i:i + 50]
            for q, vec in zip(batch, embed_texts([QUERY_PREFIX + q for q in batch])):
                cache[_cache_key(q)] = vec
            QUERY_CACHE.write_text(json.dumps(cache))
    return [cache[_cache_key(q)] for q in questions]


def retrieve(design: str, questions: list[dict], n: int = max(KS)) -> dict[str, list[dict]]:
    from index import get_collection

    col = get_collection(design)
    vectors = query_vectors([q["question"] for q in questions])
    result = {}
    for q, vec in zip(questions, vectors):
        res = col.query(query_embeddings=[vec], n_results=n, include=["metadatas", "documents", "distances"])
        result[q["id"]] = [
            {**meta, "id": cid, "distance": dist, "text": doc}
            for cid, meta, doc, dist in zip(res["ids"][0], res["metadatas"][0], res["documents"][0], res["distances"][0])
        ]
    return result


def print_table(design: str, rates: dict) -> None:
    print(f"\n=== retrieval, design: {design}")
    print(f"{'k':>2}  {'all':>12}  {'single':>12}  {'multi (all found)':>18}  {'multi coverage':>14}  {'words in prompt':>15}")
    for k, e in rates.items():
        fmt = lambda x: f"{x['hits']}/{x['n']} = {x['rate']:.0%}"
        print(f"{k:>2}  {fmt(e['all']):>12}  {fmt(e['single']):>12}  {fmt(e['multi']):>18}  "
              f"{e['multi_coverage']:>14.0%}  {e['words_in_prompt']:>15.0f}")


def retrieval_stage() -> dict:
    from index import DESIGNS, get_collection

    questions = load_questions()
    wanted = [d for d in os.environ.get("DESIGNS", ",".join(DESIGNS)).split(",") if d]
    results = {}
    for design in wanted:
        if get_collection(design).count() == 0:
            log(f"[{design}] not indexed yet, skipping")
            continue
        retrieved = retrieve(design, questions)
        rates = hit_rates(questions, retrieved)
        print_table(design, rates)
        results[design] = {
            "hit_rates": rates,
            "top5": {qid: [{k: m[k] for k in ("source", "article", "location", "words", "distance")} for m in ms]
                     for qid, ms in retrieved.items()},
        }
    previous = json.loads(RETRIEVAL_RESULTS.read_text()) if RETRIEVAL_RESULTS.exists() else {}
    previous.update(results)
    RETRIEVAL_RESULTS.write_text(json.dumps(previous, indent=1))
    return results


# --------------------------------------------------------------------------
# Stage 2-3 helpers (pure functions: no API calls, unit-tested)
# --------------------------------------------------------------------------
ANSWERS = EVAL / "agent_answers.json"
VERDICTS = EVAL / "judge_verdicts.json"
HUMAN_LABELS = EVAL / "human_labels.csv"
GRADING_SHEET = EVAL / "grading_sheet.md"
SUMMARY = EVAL / "evaluation_summary.json"
DEMO = EVAL / "add_document_demo.json"
REFUSAL_PHRASE = "the corpus does not cover this"
JUDGE_MODEL = os.environ.get("JUDGE_MODEL", "gemini-3.5-flash-lite")
DEMO_QUESTION_ID = "q29"
DEMO_DOCUMENT = "corpus/ai_act_annex_iii.html"

JUDGE_RUBRIC = """You grade an answer from a question-answering assistant about three EU regulations
(AI Act, GDPR, Data Act). You see the question, the reference answer, the passages the assistant
retrieved, and the assistant's answer. Grade two things, each 1 or 0.

correct
  - Answerable question: 1 if the answer gives the same substance as the reference answer: the
    key rule and its main condition or exception, with no statement that contradicts the
    reference. Missing minor details is fine. A refusal ("the corpus does not cover this") is 0.
  - Unanswerable question (the reference says what the assistant should say): 1 only if the
    assistant clearly declines because the corpus does not cover it and does not assert an
    answer as fact. Mentioning a nearby article is fine if it is not presented as the answer.
supported
  - 1 if every factual claim in the answer can be found in the retrieved passages. A proper
    refusal is supported. 0 if any claim (number, date, duty, exception, article) is not in the
    passages, even if it happens to be true in reality.

Reply with JSON only: {"correct": 0 or 1, "supported": 0 or 1, "reason": "one short sentence"}"""


def is_refusal(answer: str) -> bool:
    return REFUSAL_PHRASE in answer.lower().replace("*", "")[:160]


def code_checks(q: dict, r: dict) -> dict:
    """Checks that code can do: did it search, refuse, cite, and cite real passages."""
    from agent import retrieved_units

    if r.get("error"):
        return {"error": r["error"]}
    got = retrieved_units(r["trace"])
    cited = {(s, u) for s, u in
             ((c.strip("[]").split(", ", 1)[0], _unit_of(c)) for c in r["citations"]) if u}
    exp = [(s, a) for s, a in q["expected"]]
    return {
        "searched": any(c["tool"] == "search" for c in r["trace"]),
        "refused": is_refusal(r["raw_answer"]),
        "has_citation": bool(r["citations"]),
        "citations_valid": not r["unverified_citations"],
        "retrieved_expected": bool(exp) and all(e in got for e in exp),
        "cited_expected": bool(exp) and all(e in cited for e in exp),
        "limit_hit": r["limit_hit"],
    }


def _unit_of(citation: str) -> str | None:
    from agent import _unit

    return _unit(citation)


def classify_failure(q: dict, checks: dict, verdict: dict | None) -> str | None:
    """One cause per failed question (None = no failure). Order matters: first match wins."""
    if checks.get("error"):
        return "tool or model error"
    unans = q["kind"] == "unanswerable"
    correct = verdict.get("correct") if verdict and "correct" in verdict else None
    supported = verdict.get("supported") if verdict and "supported" in verdict else None
    if not checks["searched"]:
        return "answered without searching"
    if not checks["citations_valid"]:
        return "citation not in retrieved passages"
    if unans and not checks["refused"]:
        return "answered an unanswerable question"
    if not unans and checks["refused"]:
        return "wrong refusal (passages retrieved)" if checks["retrieved_expected"] else "wrong refusal (retrieval missed)"
    if supported == 0:
        return "claim not supported by the passages"
    if correct == 0 and not unans:
        return "answer wrong or incomplete (passages retrieved)" if checks["retrieved_expected"] else "answer wrong (retrieval missed)"
    if correct == 0:
        return "refusal judged wrong"
    return None


def summarize(questions: list[dict], answers: dict, verdicts: dict) -> dict:
    n = {"answerable": 0, "unanswerable": 0}
    out = {"correct": 0, "unsupported": 0, "correct_refusals": 0, "wrong_refusals": 0,
           "answered_unanswerable": 0, "judged": 0, "errors": 0, "limit_hit": 0}
    causes: dict[str, list[str]] = {}
    tokens_in = tokens_out = seconds = tool_calls = answered = 0
    for q in questions:
        r = answers.get(q["id"])
        if r is None or r.get("error"):
            out["errors"] += 1
            causes.setdefault("tool or model error", []).append(q["id"])
            continue
        checks = code_checks(q, r)
        v = verdicts.get(q["id"])
        v = v if v and "correct" in v else None
        unans = q["kind"] == "unanswerable"
        n["unanswerable" if unans else "answerable"] += 1
        answered += 1
        tokens_in += r["tokens"]["input"]; tokens_out += r["tokens"]["output"]
        seconds += r["seconds"]; tool_calls += len(r["trace"])
        out["limit_hit"] += bool(checks["limit_hit"])
        if checks["refused"]:
            out["correct_refusals" if unans else "wrong_refusals"] += 1
        elif unans:
            out["answered_unanswerable"] += 1
        if v:
            out["judged"] += 1
            out["correct"] += v["correct"]
            out["unsupported"] += 1 - v["supported"]
        cause = classify_failure(q, checks, v)
        if cause:
            causes.setdefault(cause, []).append(q["id"])
    out.update(n)
    out["failures_by_cause"] = {k: {"count": len(v), "ids": v} for k, v in sorted(causes.items(), key=lambda kv: -len(kv[1]))}
    out["cost_per_question"] = {
        "questions": answered,
        "input_tokens": round(tokens_in / answered) if answered else None,
        "output_tokens": round(tokens_out / answered) if answered else None,
        "seconds": round(seconds / answered, 1) if answered else None,
        "tool_calls": round(tool_calls / answered, 1) if answered else None,
    }
    return out


def agreement(labels: list[dict], verdicts: dict) -> dict:
    """How often the judge and the human agree, on the answers the human graded."""
    rows = [(l, verdicts[l["id"]]) for l in labels
            if l["id"] in verdicts and "correct" in verdicts[l["id"]] and l["correct"] in ("0", "1") and l["supported"] in ("0", "1")]
    if not rows:
        return {"graded": 0}
    same = lambda key: sum(int(l[key]) == v[key] for l, v in rows)
    both = sum(int(l["correct"]) == v["correct"] and int(l["supported"]) == v["supported"] for l, v in rows)
    return {"graded": len(rows),
            "correct_agreement": same("correct") / len(rows),
            "supported_agreement": same("supported") / len(rows),
            "both_agreement": both / len(rows),
            "disagreements": [l["id"] for l, v in rows
                              if int(l["correct"]) != v["correct"] or int(l["supported"]) != v["supported"]]}


def parse_verdict(text: str) -> dict:
    import re

    m = re.search(r"\{.*\}", text, re.DOTALL)
    if not m:
        raise ValueError(f"no JSON in judge reply: {text[:120]!r}")
    d = json.loads(m.group(0))
    return {"correct": int(bool(int(d["correct"]))), "supported": int(bool(int(d["supported"]))),
            "reason": str(d.get("reason", ""))[:300]}


def grading_ids(questions: list[dict]) -> list[str]:
    """24 answers to grade by hand: all unanswerable, all multi, every other single."""
    singles = [q["id"] for q in questions if q["kind"] == "single"]
    pick = set(singles[::2]) | {singles[-1]}
    return [q["id"] for q in questions if q["kind"] != "single" or q["id"] in pick]


def _passages(r: dict, limit: int = 30000) -> str:
    seen, out = set(), []
    for c in r["trace"]:
        if c["tool"] != "search":
            continue
        for block in c["result"].split("\n\n"):
            head = block.split("\n", 1)[0]
            if head not in seen:
                seen.add(head)
                out.append(block)
    return "\n\n".join(out)[:limit]


def write_grading_sheet(questions: list[dict], answers: dict) -> None:
    ids = grading_ids(questions)
    lines = ["# Grade these answers by hand (do NOT open judge_verdicts.json first)", "",
             "For each answer write one line in `eval/human_labels.csv`:  `id,correct,supported,notes`",
             "(header: `id,correct,supported,notes`). correct = 1 if it matches the reference answer or is a proper",
             "refusal on an unanswerable question; supported = 1 if every claim is in the passages shown;",
             "notes = why, required for every 0.", ""]
    for q in questions:
        r = answers.get(q["id"])
        if q["id"] not in ids or not r or r.get("error"):
            continue
        lines += [f"## {q['id']} ({q['kind']})", f"**Question:** {q['question']}", "",
                  f"**Reference / what it should say:** {q['reference_answer']}", "",
                  f"**Agent answer:** {r['raw_answer']}", "", "**Passages it retrieved:**", ""]
        lines += ["> " + p[:900].replace("\n", " ") for p in _passages(r, 6000).split("\n\n")] + [""]
    GRADING_SHEET.write_text("\n".join(lines), encoding="utf-8")


# --------------------------------------------------------------------------
# Stage 2: run the agent on every question
# --------------------------------------------------------------------------
def _slim(result: dict) -> dict:
    keep = ("question", "answer", "raw_answer", "citations", "unverified_citations", "tokens", "seconds", "limit_hit")
    out = {k: result[k] for k in keep}
    out["trace"] = [{k: c[k] for k in ("tool", "args", "approved", "result")} for c in result["trace"]]
    return out


def _load(path: Path) -> dict:
    return json.loads(path.read_text()) if path.exists() and not os.environ.get("FRESH") else {}


async def answers_stage(questions: list[dict]) -> dict:
    from agent import Harness

    os.environ["AGENT_QUIET"] = "1"
    answers = _load(ANSWERS)
    todo = [q for q in questions if q["id"] not in answers or answers[q["id"]].get("error")]
    log(f"agent answers: {len(questions) - len(todo)} cached, {len(todo)} to ask")
    if todo:
        # evaluation is unattended: add_document is always refused here (the demo stage approves it on purpose)
        async with Harness(approve=lambda tool, args: False) as h:
            for i, q in enumerate(todo, 1):
                try:
                    answers[q["id"]] = _slim(await h.ask(q["question"]))
                    r = answers[q["id"]]
                    log(f"  [{i}/{len(todo)}] {q['id']} {r['seconds']}s, {len(r['trace'])} tool calls")
                except Exception as e:
                    answers[q["id"]] = {"error": f"{type(e).__name__}: {str(e)[:300]}"}
                    log(f"  [{i}/{len(todo)}] {q['id']} ERROR {answers[q['id']]['error']}")
                ANSWERS.write_text(json.dumps(answers, indent=1))
    write_grading_sheet(questions, answers)
    return answers


# --------------------------------------------------------------------------
# Stage 3: LLM judge
# --------------------------------------------------------------------------
async def judge_stage(questions: list[dict], answers: dict) -> dict:
    from langchain_google_genai import ChatGoogleGenerativeAI

    from api_key import load_api_key

    verdicts = _load(VERDICTS)
    todo = [q for q in questions if q["id"] in answers and not answers[q["id"]].get("error")
            and "correct" not in verdicts.get(q["id"], {})]
    log(f"judge ({JUDGE_MODEL}): {len(verdicts)} cached, {len(todo)} to grade")
    llm = ChatGoogleGenerativeAI(model=JUDGE_MODEL, api_key=load_api_key(), max_retries=3, timeout=90)
    for i, q in enumerate(todo, 1):
        r = answers[q["id"]]
        prompt = (f"{JUDGE_RUBRIC}\n\nQUESTION ({q['kind']}): {q['question']}\n\nREFERENCE ANSWER / WHAT IT SHOULD SAY: "
                  f"{q['reference_answer']}\n\nRETRIEVED PASSAGES:\n{_passages(r) or '(none)'}\n\nASSISTANT ANSWER:\n{r['raw_answer']}")
        for attempt in (1, 2):
            try:
                verdicts[q["id"]] = parse_verdict(str((await llm.ainvoke(prompt)).text))
                break
            except Exception as e:
                verdicts[q["id"]] = {"error": f"{type(e).__name__}: {str(e)[:200]}"}
        log(f"  [{i}/{len(todo)}] {q['id']} -> {verdicts[q['id']]}")
        VERDICTS.write_text(json.dumps(verdicts, indent=1))
    return verdicts


def read_human_labels() -> list[dict]:
    if not HUMAN_LABELS.exists():
        return []
    with open(HUMAN_LABELS, newline="", encoding="utf-8") as f:
        return [{k: (v or "").strip() for k, v in r.items()} for r in csv.DictReader(f) if (r.get("id") or "").strip()]


def report_stage(questions: list[dict], answers: dict, verdicts: dict) -> dict:
    s = summarize(questions, answers, verdicts)
    s["agreement_with_human"] = agreement(read_human_labels(), verdicts)
    SUMMARY.write_text(json.dumps(s, indent=1))
    print("\n=== end-to-end evaluation")
    print(f"questions: {s['answerable']} answerable + {s['unanswerable']} unanswerable ({s['errors']} errors)")
    print(f"judged correct: {s['correct']}/{s['judged']}   unsupported answers: {s['unsupported']}")
    print(f"correct refusals: {s['correct_refusals']}/{s['unanswerable']}   wrong refusals: {s['wrong_refusals']}/{s['answerable']}"
          f"   unanswerable answered anyway: {s['answered_unanswerable']}")
    ag = s["agreement_with_human"]
    if ag["graded"]:
        print(f"judge vs your labels ({ag['graded']} graded): correct {ag['correct_agreement']:.0%}, "
              f"supported {ag['supported_agreement']:.0%}, both {ag['both_agreement']:.0%}")
    else:
        print("judge vs your labels: no graded answers yet (eval/human_labels.csv)")
    for cause, d in s["failures_by_cause"].items():
        print(f"  failure: {cause}: {d['count']} {d['ids']}")
    c = s["cost_per_question"]
    print(f"cost per question: {c['input_tokens']} input + {c['output_tokens']} output tokens, "
          f"{c['seconds']}s, {c['tool_calls']} tool calls")
    return s


# --------------------------------------------------------------------------
# Stage 4: add a document that answers an unanswerable question
# --------------------------------------------------------------------------
async def demo_stage(questions: list[dict], answers: dict) -> dict:
    import shutil
    import tempfile

    from agent import Harness
    from index import INDEX_DIR

    q = next(x for x in questions if x["id"] == DEMO_QUESTION_ID)
    scratch = Path(tempfile.mkdtemp(prefix="index_copy_")) / "index"
    shutil.copytree(INDEX_DIR, scratch)  # the committed index is never modified
    os.environ["INDEX_DIR"] = str(scratch)  # server.py (started by Harness) inherits it
    os.environ["AGENT_QUIET"] = "1"
    log(f"add-document demo on a copy of the index: {scratch}")
    try:
        async with Harness(approve=lambda tool, args: True) as h:
            before = await h.ask(q["question"])
            added = await h.ask(f"Please add the file {DEMO_DOCUMENT} to the corpus.")
            after = await h.ask(q["question"])
            added_again = await h.ask(f"Please add the file {DEMO_DOCUMENT} to the corpus.")
    finally:
        os.environ.pop("INDEX_DIR", None)
        shutil.rmtree(scratch.parent, ignore_errors=True)
    demo = {"question": q, "document": DEMO_DOCUMENT,
            "before": _slim(before), "adding": _slim(added), "after": _slim(after), "adding_again": _slim(added_again)}
    DEMO.write_text(json.dumps(demo, indent=1, default=str))
    print("\n=== add-document demo")
    print("QUESTION:", q["question"])
    print("BEFORE:", before["answer"][:700])
    print("ADD:", [c["result"] for c in added["trace"] if c["tool"] == "add_document"])
    print("AFTER:", after["answer"][:900])
    print("ADD AGAIN:", [c["result"] for c in added_again["trace"] if c["tool"] == "add_document"])
    return demo


def main() -> None:
    import asyncio

    stage = os.environ.get("STAGE", "all")
    if stage not in ("all", "retrieval", "answers", "judge", "demo"):
        raise SystemExit("STAGE must be all, retrieval, answers, judge or demo")
    questions = load_questions()
    if stage in ("all", "retrieval"):
        retrieval_stage()
    if stage in ("all", "answers", "judge"):
        answers = asyncio.run(answers_stage(questions))
        if stage == "answers":
            s = summarize(questions, answers, {})
            c = s["cost_per_question"]
            print(f"\nanswers saved to {ANSWERS.name}; now grade {GRADING_SHEET.name} by hand "
                  f"(24 answers) into eval/human_labels.csv, then run: STAGE=judge uv run python main.py evaluate")
            print(f"answered {c['questions']}/{len(questions)}; refusals: {s['correct_refusals']}/{s['unanswerable']} on unanswerable, "
                  f"{s['wrong_refusals']} wrong")
        else:
            verdicts = asyncio.run(judge_stage(questions, answers))
            report_stage(questions, answers, verdicts)
    if stage in ("all", "demo"):
        asyncio.run(demo_stage(questions, _load(ANSWERS)))


if __name__ == "__main__":
    main()
