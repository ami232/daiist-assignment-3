"""
Assignment 3: evaluation (`main.py evaluate`). Built from session 10's 07-own-harness/evaluate.py.

Stage 1, retrieval: hit rate at k = 1, 3, 5 per retrieval design on the answerable questions. A
question is a hit at k when one of the top k chunks covers its expected source and location (for
`multi` questions any of its passages; all passages at 5 is reported too).
  -> eval/retrieval.csv, eval/retrieval_summary.csv

Stage 2, end to end: the agent of agent.py answers every question (original corpus only). Code
checks what code can check (refusal, citations valid, expected passage cited); an LLM judge with a
rubric and the retrieved passages as evidence grades correctness and support; each answer gets a
euro cost from the cost model; agreement with eval/human_labels.csv is measured.
  -> eval/answers.jsonl, eval/results.csv, eval/summary.json, eval/grading_sheet.md

Stage 3, adding a document: the unanswerable question q33 (Ghana's risk class) before and after
adding the country benchmarking act with the add_document tool.
  -> eval/add_document_demo.json

Answers are cached in eval/answers.jsonl while the question, AGENTS.md and the model are unchanged;
`--fresh` asks every question again.
"""

import asyncio
import csv
import hashlib
import json
import re
import sys
from contextlib import AsyncExitStack
from pathlib import Path

from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

import agent
import index
import retrieval
from api_key import load_api_key

load_api_key()  # the judge model reads GEMINI_API_KEY from the environment

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
HUMAN_LABELS = EVAL / "human_labels.csv"
ANSWERS = EVAL / "answers.jsonl"
KS = (1, 3, 5)
CALL_TIMEOUT = 120  # seconds per agent run or judge call; a hung call is retried
JUDGE_MODEL = "gemini-3.1-flash-lite"  # lightweight, high free-tier quota, different model from the agent's; stronger flash models were overloaded (503)

# Cost model (REPORT.md, Use case): a medium-sized cocoa importer acting on the answer.
COST_CORRECT = 0.0
COST_DONT_KNOW = 51.60                 # 1 hour of in-house research at €51.6/h (Eurostat 2025, NACE M, euro area)
COST_WRONG = 0.03 * 13 * 3842 / 0.83305  # 3% check rate (Art. 16(8)) x 13 t container x ICE London £/t / ECB £ per €

DEMO_QUESTION = "q33"
DEMO_FILE = index.CORPUS_DIR / "to_add" / "eudr_country_benchmarking_2025-1093.html"

# (name, chunking design, hybrid keyword search?)
DESIGNS = [
    ("fixed", "fixed", False),
    ("fixed+bm25", "fixed", True),
    ("structure", "structure", False),
    ("structure+bm25", "structure", True),
]


# ---------------------------------------------------------------- shared helpers

def load_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r["question"].strip()]


def expected_passages(row: dict) -> list[tuple[str, str]]:
    if not row["expected_source"].strip():
        return []
    return [(s.strip(), l.strip()) for s, l in zip(row["expected_source"].split(";"), row["expected_location"].split(";"))]


def location_matches(location: str, expected: str) -> bool:
    """'Article 25(1)–(2)' matches 'Article 25'; 'Article 25' does not match 'Article 2'; 'Annex III' not 'Annex I'."""
    location, expected = location.strip(), expected.strip()
    return location == expected or (location.startswith(expected) and location[len(expected)] in " (,")


def covers(chunk: dict, passage: tuple[str, str]) -> bool:
    source, expected = passage
    return chunk["source"] == source and any(location_matches(loc, expected) for loc in chunk.get("covers", [chunk["location"]]))


def key_covers(key: str, passage: tuple[str, str]) -> bool:
    """Same test on a citation key such as 'EUDR Article 25(1)–(2)' or 'FAQ 10.2, p. 94'."""
    source, expected = passage
    if not key.startswith(source):
        return False
    location = key if key.startswith(expected) else key[len(source):].strip()
    return location_matches(location, expected)


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def print_table(rows: list[dict]) -> None:
    keys = list(rows[0])
    widths = {k: max(len(k), *(len(str(r[k])) for r in rows)) for k in keys}
    print("  ".join(k.ljust(widths[k]) for k in keys))
    for r in rows:
        print("  ".join(str(r[k]).ljust(widths[k]) for k in keys))


# ---------------------------------------------------------------- stage 1: retrieval

def retrieval_stage(questions: list[dict]) -> list[dict]:
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    vectors = retrieval.embed_queries([q["question"] for q in answerable])  # cached; costs quota only once
    rows, summary = [], []
    for name, design, hybrid in DESIGNS:
        per_k = {k: 0 for k in KS}
        full_recall, multi, words = 0, 0, {k: [] for k in KS}
        for q in answerable:
            results = retrieval.search(q["question"], design, k=max(KS), hybrid=hybrid, vector=vectors[q["question"]])
            passages = expected_passages(q)
            first_hit = next((i + 1 for i, c in enumerate(results) if any(covers(c, p) for p in passages)), None)
            for k in KS:
                per_k[k] += first_hit is not None and first_hit <= k
                words[k].append(sum(c["words"] for c in results[:k]))
            if q["kind"] == "multi":
                multi += 1
                full_recall += all(any(covers(c, p) for c in results) for p in passages)
            rows.append({"design": name, "id": q["id"], "kind": q["kind"], "first_hit_rank": first_hit or "",
                         "retrieved": " || ".join(f"{c['source']} {c['location']}" for c in results)})
        n = len(answerable)
        summary.append({"design": name, **{f"hit@{k}": round(per_k[k] / n, 3) for k in KS},
                        "multi_all_passages@5": f"{full_recall}/{multi}",
                        **{f"words@{k}": round(sum(words[k]) / n) for k in KS}})
    write_csv(EVAL / "retrieval.csv", rows)
    write_csv(EVAL / "retrieval_summary.csv", summary)
    print(f"\nRetrieval on {len(answerable)} answerable questions "
          f"(server uses: {index.DEFAULT_DESIGN}{'+bm25' if index.DEFAULT_HYBRID else ''}):")
    print_table(summary)
    return summary


# ---------------------------------------------------------------- stage 2: end to end

class Verdict(BaseModel):
    reasoning: str = Field(description="Two to four sentences checking the answer against each criterion, before deciding.")
    correct: bool = Field(description="Criterion 1: true only if the answer is right against the reference answer.")
    supported: bool = Field(description="Criterion 2: true only if every factual claim in the answer is stated in the retrieved passages.")


JUDGE_RUBRIC = "v2"  # v1 in eval/judge_v1_*; v2 = criteria judged separately, qualifiers/definitions must be in the passages; refusals' support is decided in code
JUDGE_PROMPT = """You grade the answer of an assistant for the compliance team of an EU cocoa importer. The assistant may only use passages retrieved from a corpus on the EU Deforestation Regulation (EUDR), and must begin with "The corpus does not cover this." when those passages do not answer the question.

Judge the two criteria separately: one does not decide the other.

Criteria:
1. Correct. For an answerable question: the answer states the substance of the reference answer and nothing that contradicts it; missing minor detail is fine, a wrong or missing key fact (date, number, yes/no, obligation) is not; a refusal is NOT correct. For an unanswerable question: a refusal (or an answer that clearly says the corpus does not contain the information) is correct, even if it adds a short pointer to where to look (an authority, a later act, a lawyer); any substantive answer is not correct.
2. Supported. Check each factual claim of the answer against the retrieved passages, one by one. A claim is supported only if a passage states it; this includes qualifiers ("higher", "only", "always"), definitions and conclusions drawn from a definition, which must be in the passages too. A claim from general knowledge fails even if it is true. Disclaimers and advice (e.g. "not legally binding", "consult your authority") are not factual claims. A refusal makes no factual claims, so it is supported even when refusing was the wrong decision: that error belongs to criterion 1 only.

Question ({kind}): {question}
Reference answer: {reference}

Retrieved passages (what the search tool returned in this run):
{evidence}

Assistant's answer:
{answer}"""


def evidence_text(trace: list[dict], limit: int = 24000) -> str:
    text = "\n\n=====\n\n".join(step["text"] for step in trace if step["type"] == "result")
    return (text[:limit] + "\n[...]") if len(text) > limit else (text or "(no search was made)")


def run_fingerprint() -> str:
    return hashlib.sha1((agent.MODEL + (ROOT / "AGENTS.md").read_text(encoding="utf-8")
                         + index.DEFAULT_DESIGN + str(index.DEFAULT_HYBRID)).encode()).hexdigest()[:12]


def load_cached_answers() -> dict:
    if not ANSWERS.exists():
        return {}
    rows = [json.loads(line) for line in ANSWERS.read_text(encoding="utf-8").splitlines() if line.strip()]
    return {r["id"]: r for r in rows}


def retryable(error: Exception) -> bool:
    """Free-tier rate limits (429) and temporary overload (503) are worth waiting for."""
    return any(code in str(error) for code in ("429", "RESOURCE_EXHAUSTED", "503", "UNAVAILABLE"))


async def ask_with_retry(the_agent, question: str) -> dict:
    for attempt in range(5):
        try:
            return await asyncio.wait_for(agent.ask(the_agent, question), CALL_TIMEOUT)
        except Exception as error:  # noqa: BLE001 - free-tier rate limits surface as several error types
            if not (retryable(error) or isinstance(error, TimeoutError)) or attempt == 4:
                raise
            wait = 20 * (attempt + 1)
            print(f"    agent: {type(error).__name__} {str(error)[:80]!r}, retrying in {wait}s", file=sys.stderr, flush=True)
            await asyncio.sleep(wait)


async def judge_with_retry(judge, prompt: str) -> Verdict:
    for attempt in range(5):
        try:
            return await asyncio.wait_for(judge.ainvoke(prompt), CALL_TIMEOUT)
        except Exception as error:  # noqa: BLE001
            if not (retryable(error) or isinstance(error, TimeoutError)) or attempt == 4:
                raise
            wait = 20 * (attempt + 1)
            print(f"    judge: {type(error).__name__} {str(error)[:80]!r}, retrying in {wait}s", file=sys.stderr, flush=True)
            await asyncio.sleep(wait)


def apply_code_rules(r: dict) -> None:
    """What code can decide, it decides: a refusal makes no factual claims, so it is supported."""
    if agent.is_refusal(r["answer"]):
        r["judge"]["supported"] = True


def outcome(q: dict, r: dict) -> str:
    unanswerable = q["kind"] == "unanswerable"
    if agent.is_refusal(r["answer"]):  # what the user sees, after the guardrail
        return "correct refusal" if unanswerable else "wrong refusal"
    return "correct" if r["judge"]["correct"] else "wrong"


def cost(result_outcome: str) -> float:
    return {"correct": COST_CORRECT, "wrong": COST_WRONG}.get(result_outcome, COST_DONT_KNOW)


def proposed_cause(q: dict, r: dict, result_outcome: str) -> str:
    """A first guess at the failure class, from the trace; reviewed by hand in REPORT.md."""
    passages = expected_passages(q)
    keys = agent.retrieved_citations(r["trace"])
    retrieved = all(any(key_covers(k, p) for k in keys) for p in passages) if passages else True
    if result_outcome == "wrong refusal":
        return "wrong refusal" if retrieved else "retrieval miss"
    if result_outcome == "wrong":
        if q["kind"] == "unanswerable":
            return "unsupported claim"
        if not retrieved:
            return "retrieval miss"
        return "unsupported claim" if not r["judge"]["supported"] else "wrong answer from the right passage"
    if result_outcome == "correct" and not r["judge"]["supported"]:
        return "unsupported claim"
    return ""


async def end_to_end_stage(questions: list[dict], fresh: bool) -> list[dict]:
    fingerprint = run_fingerprint()
    cached = {} if fresh else load_cached_answers()
    judge = ChatGoogleGenerativeAI(model=JUDGE_MODEL, temperature=0).with_structured_output(Verdict)
    results = []
    async with AsyncExitStack() as stack:
        the_agent = None
        for q in questions:
            old = cached.get(q["id"])
            if old and old["question"] == q["question"] and old["fingerprint"] == fingerprint and "judge" in old:
                # Re-apply the current citation guardrail to the saved draft; re-judge only if the shown answer changes.
                check = agent.check_citations(old["draft"], old["trace"])
                answer = old["draft"] if check["passed"] else agent.WITHHELD
                if answer != old["answer"] or old.get("judge_rubric") != JUDGE_RUBRIC:
                    old.update({"check": check, "answer": answer, "withheld": answer != old["draft"]})
                    verdict = await judge_with_retry(judge, JUDGE_PROMPT.format(
                        kind=q["kind"], question=q["question"], reference=q["reference_answer"],
                        evidence=evidence_text(old["trace"]), answer=answer))
                    old["judge"] = verdict.model_dump()
                    old["judge_rubric"] = JUDGE_RUBRIC
                    print(f"  {q['id']}: re-judged", file=sys.stderr, flush=True)
                    cached[q["id"]] = old  # save progress, so an overloaded model loses nothing
                    ANSWERS.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in cached.values()), encoding="utf-8")
                else:
                    old["check"] = check
                results.append(old)
                continue
            if the_agent is None:
                the_agent = agent.build_agent(await agent.load_mcp_tools(stack, base_only=True))
            print(f"  {q['id']}: {q['question'][:70]}", file=sys.stderr, flush=True)
            r = await ask_with_retry(the_agent, q["question"])
            verdict = await judge_with_retry(judge, JUDGE_PROMPT.format(
                kind=q["kind"], question=q["question"], reference=q["reference_answer"],
                evidence=evidence_text(r["trace"]), answer=r["answer"]))
            r.update({"id": q["id"], "question": q["question"], "kind": q["kind"], "fingerprint": fingerprint,
                      "judge": verdict.model_dump(), "judge_rubric": JUDGE_RUBRIC})
            results.append(r)
            ANSWERS.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in results)
                               + "".join(json.dumps(x, ensure_ascii=False) + "\n" for k, x in cached.items()
                                         if k not in {y["id"] for y in results}), encoding="utf-8")
    ANSWERS.write_text("".join(json.dumps(x, ensure_ascii=False) + "\n" for x in results), encoding="utf-8")
    return results


def summarise(questions: list[dict], results: list[dict]) -> dict:
    by_id = {q["id"]: q for q in questions}
    rows = []
    for r in results:
        apply_code_rules(r)
        q = by_id[r["id"]]
        o = outcome(q, r)
        passages = expected_passages(q)
        cited_expected = any(key_covers(c, p) for c in r["check"]["cited"] for p in passages) if passages else ""
        rows.append({
            "id": r["id"], "kind": q["kind"], "outcome": o, "cost_eur": round(cost(o), 2),
            "refusal": int(agent.is_refusal(r["answer"])), "citations_valid": int(not r["check"]["invalid"]),
            "cited_expected_passage": int(cited_expected) if passages else "",
            "guardrail_withheld": int(r["withheld"]),
            "judge_correct": int(r["judge"]["correct"]), "judge_supported": int(r["judge"]["supported"]),
            "proposed_cause": proposed_cause(q, r, o),
            "seconds": r["seconds"], "input_tokens": r["input_tokens"], "output_tokens": r["output_tokens"],
            "model_calls": r["model_calls"], "searches": sum(1 for s in r["trace"] if s["type"] == "call" and s["tool"] == "search"),
            "judge_reasoning": r["judge"]["reasoning"],
        })
    write_csv(EVAL / "results.csv", rows)

    n = len(rows)
    count = lambda key, value: sum(1 for x in rows if x[key] == value)  # noqa: E731
    answered = [x for x in rows if not x["refusal"]]
    summary = {
        "questions": n,
        "outcomes": {o: count("outcome", o) for o in ("correct", "wrong", "correct refusal", "wrong refusal")},
        "unsupported_answers": sum(1 for x in answered if not x["judge_supported"]),
        "code_checks": {
            "answers_with_all_citations_valid": f"{sum(x['citations_valid'] for x in rows)}/{n}",
            "answerable_citing_expected_passage": f"{sum(1 for x in rows if x['cited_expected_passage'] == 1)}/"
                                                  f"{sum(1 for x in rows if x['cited_expected_passage'] != '')}",
            "guardrail_withheld": count("guardrail_withheld", 1),
        },
        "error_rate_of_answers": round(sum(1 for x in answered if x["outcome"] == "wrong") / max(len(answered), 1), 3),
        "break_even_error_rate": round((COST_DONT_KNOW - COST_CORRECT) / (COST_WRONG - COST_CORRECT), 3),
        "cost_per_question_eur": round(sum(x["cost_eur"] for x in rows) / n, 2),
        "cost_without_assistant_eur": COST_DONT_KNOW,
        "mean_seconds": round(sum(x["seconds"] for x in rows) / n, 1),
        "mean_input_tokens": round(sum(x["input_tokens"] for x in rows) / n),
        "mean_output_tokens": round(sum(x["output_tokens"] for x in rows) / n),
        "failure_causes": {c: sum(1 for x in rows if x["proposed_cause"] == c) for c in
                           dict.fromkeys(x["proposed_cause"] for x in rows) if c},
        "human_agreement": human_agreement(rows),
    }
    (EVAL / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    write_grading_sheet(questions, results)

    print(f"\nEnd to end on {n} questions:")
    for key, value in summary.items():
        print(f"  {key}: {value}")
    return summary


def human_agreement(rows: list[dict]) -> dict:
    if not HUMAN_LABELS.exists():
        return {"graded": 0}
    with HUMAN_LABELS.open(newline="", encoding="utf-8") as f:
        labels = {r["id"].strip(): r for r in csv.DictReader(f) if (r.get("id") or "").strip()}
    pairs = [(x, labels[x["id"]]) for x in rows if x["id"] in labels]
    if not pairs:
        return {"graded": 0}
    result = {"graded": len(pairs)}
    for name in ("correct", "supported"):
        judge = [x[f"judge_{name}"] for x, _ in pairs]
        human = [int(h[name]) for _, h in pairs]
        agree = sum(a == b for a, b in zip(judge, human)) / len(pairs)
        pj, ph = sum(judge) / len(judge), sum(human) / len(human)
        chance = pj * ph + (1 - pj) * (1 - ph)
        result[name] = {"agreement": round(agree, 3), "cohen_kappa": round((agree - chance) / (1 - chance), 3) if chance < 1 else None,
                        "disagreements": [x["id"] for (x, _), a, b in zip(pairs, judge, human) if a != b]}
    return result


def write_grading_sheet(questions: list[dict], results: list[dict]) -> None:
    """For grading by hand into eval/human_labels.csv: no judge verdicts, so they cannot bias the grades."""
    by_id = {r["id"]: r for r in results}
    lines = ["# Grading sheet", "",
             "Grade each answer into `eval/human_labels.csv` (`id,correct,supported,notes`) before reading "
             "`eval/results.csv`. `correct`: 1 if right against the reference (for unanswerable questions, 1 only for a refusal). "
             "`supported`: 1 if every claim is in the retrieved passages. A note for every 0.", ""]
    for q in questions:
        r = by_id.get(q["id"])
        if not r:
            continue
        lines += [f"## {q['id']} ({q['kind']})", "", f"**Question:** {q['question']}", "",
                  f"**Reference:** {q['reference_answer']}", "", "**Answer:**", "", r["answer"], "",
                  "<details><summary>Retrieved passages</summary>", "", "```", evidence_text(r["trace"], 12000), "```",
                  "", "</details>", ""]
    (EVAL / "grading_sheet.md").write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------- stage 3: adding a document

async def add_document_stage(questions: list[dict], results: list[dict]) -> None:
    path = EVAL / "add_document_demo.json"
    if path.exists():
        demo = json.loads(path.read_text(encoding="utf-8"))
        print(f"\nAdd-document demo (saved): {demo['question']}\n  before: {demo['before'][:160]}\n  after:  {demo['after'][:300]}")
        return
    q = next(q for q in questions if q["id"] == DEMO_QUESTION)
    before = next(r for r in results if r["id"] == DEMO_QUESTION)["answer"]
    import server  # the same function the MCP tool runs
    first = server.add_document(str(DEMO_FILE))
    again = server.add_document(str(DEMO_FILE))  # shows the duplicate rule
    async with AsyncExitStack() as stack:
        the_agent = agent.build_agent(await agent.load_mcp_tools(stack, base_only=False))
        after = await ask_with_retry(the_agent, q["question"])
    demo = {"question": q["question"], "before": before, "add_document": first, "add_again": again,
            "after": after["answer"], "after_trace": after["trace"]}
    path.write_text(json.dumps(demo, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\nAdd-document demo: {q['question']}\n  before: {before[:160]}\n  add:    {first}\n  again:  {again}\n"
          f"  after:  {after['answer'][:300]}")


# ---------------------------------------------------------------- main

async def main(fresh: bool) -> None:
    questions = load_questions()
    try:
        retrieval_stage(questions)
    except index.DailyQuotaExhausted as error:
        print(f"Retrieval stage skipped: daily embedding quota reached (cached vectors are kept). {str(error)[:120]}")
    results = await end_to_end_stage(questions, fresh)
    summarise(questions, results)
    await add_document_stage(questions, results)


if __name__ == "__main__":
    asyncio.run(main(fresh="--fresh" in sys.argv))
