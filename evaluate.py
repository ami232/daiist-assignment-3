"""
Assignment 3: evaluation (`main.py evaluate`). Six stages, each writing to eval/:

1. Retrieval: hit rate at k = 1, 3, 5 for each chunking design, plus the words
   the top-k chunks add to the prompt.                       -> retrieval.csv
2. Answers: the agent (agent.py) answers every question.     -> answers.json
3. Code checks: what code can check exactly (searched, citations valid,
   cited at all, refusal phrase, expected passage retrieved).
4. LLM judge with a rubric: refused / correct / supported.  -> verdicts.json
5. Agreement with the human labels in human_labels.csv, outcomes and cost.
                                                -> results.csv, summary.json
6. Adding a document: the agent answers an unanswerable question (q33), adds
   the Package Travel Directive with add_document, answers again; then the
   document is removed so the test set keeps measuring the original corpus.
                                                -> before_after.json

Stages 2 and 4 cache their results: a re-run only does what is missing, and
everything is redone if the agent (model or AGENTS.md) or the judge changes.
`python evaluate.py --answers-only` stops after stage 3 and writes
labeling_sheet.md, so the human labels are given before reading the judge.
"""

import asyncio
import csv
import hashlib
import json
import re
import sys
import time
from contextlib import AsyncExitStack
from pathlib import Path

from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

import agent
import index
from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
EVAL_DIR = ROOT / "eval"
QUESTIONS = EVAL_DIR / "questions.csv"
QUERY_CACHE = EVAL_DIR / "query_vectors.json"
ANSWERS = EVAL_DIR / "answers.json"
VERDICTS = EVAL_DIR / "verdicts.json"
HUMAN_LABELS = EVAL_DIR / "human_labels.csv"
KS = (1, 3, 5)
JUDGE_MODEL = "gemini-3.1-flash-lite"  # gemini-3.5-flash allows only 20 free requests a day; see REPORT
# The 20 answers graded by hand: every unanswerable and multi question, plus 8
# single ones spread over the five documents.
HUMAN_LABEL_IDS = ["q31", "q32", "q33", "q34", "q35", "q36",
                   "q25", "q26", "q27", "q28", "q29", "q30",
                   "q01", "q05", "q08", "q13", "q16", "q20", "q22", "q24"]


def load_questions() -> list[dict]:
    with QUESTIONS.open(newline="") as f:
        return list(csv.DictReader(f))


def load_json(path: Path) -> dict:
    return json.loads(path.read_text()) if path.exists() else {}


def save_json(path: Path, data) -> None:
    path.write_text(json.dumps(data, indent=1, ensure_ascii=False))


# =============================================================================
# 1. Retrieval
# =============================================================================
def query_vectors(questions: list[dict]) -> dict[str, list[float]]:
    cache = load_json(QUERY_CACHE)
    for q in questions:
        if q["question"] not in cache:
            cache[q["question"]] = index.embed_query(q["question"])
            QUERY_CACHE.write_text(json.dumps(cache))  # save each one: a quota stop loses nothing
    return cache


def expected_passages(q: dict) -> list[tuple[str, str]]:
    sources = q["expected_source"].split(";")
    locations = q["expected_location"].split(";")
    if len(sources) == 1:
        sources = sources * len(locations)
    return list(zip(sources, locations))


def touches(chunk: dict, passage: tuple[str, str]) -> bool:
    source, location = passage
    return chunk["source"] == source and location in chunk["locations"].split("|")


def retrieval_eval(questions: list[dict], vectors: dict) -> list[dict]:
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    multi = [q for q in answerable if q["kind"] == "multi"]
    rows = []
    for design in index.DESIGNS:
        hits = {k: 0 for k in KS}
        all_found = {k: 0 for k in KS}
        words = {k: 0 for k in KS}
        for q in answerable:
            top = index.search(q["question"], design, k=max(KS), vector=vectors[q["question"]])
            passages = expected_passages(q)
            for k in KS:
                found = [any(touches(c, p) for c in top[:k]) for p in passages]
                hits[k] += any(found)
                words[k] += sum(c["words"] for c in top[:k])
                if q["kind"] == "multi":
                    all_found[k] += all(found)
        n = len(answerable)
        for k in KS:
            rows.append({
                "design": design, "k": k,
                "hit_rate": round(hits[k] / n, 3),
                "multi_all_passages": round(all_found[k] / len(multi), 3) if multi else "",
                "avg_words_added": round(words[k] / n),
                "questions": n,
            })
    return rows


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


# =============================================================================
# 2. Answers
# =============================================================================
def fingerprint(*parts: str) -> str:
    return hashlib.sha1("|".join(parts).encode()).hexdigest()[:12]


AGENT_VERSION = fingerprint(agent.MODEL, (ROOT / "AGENTS.md").read_text(), (ROOT / "server.py").read_text())


async def with_retry(make_call, what: str):
    """Free-tier rate limits (429), overloads (503) and timeouts (504): wait and try again."""
    for attempt in range(1, 6):
        try:
            return await make_call()
        except Exception as e:  # the Gemini wrappers raise several error types
            if "PerDay" in str(e):  # daily quota: waiting minutes will not help
                raise SystemExit(f"{what}: daily free-tier quota used up. Everything so far is saved in eval/; "
                                 "run the same command again after 09:00 (Spain) to continue.")
            if attempt < 5 and any(s in str(e) for s in ("429", "RESOURCE_EXHAUSTED", "503", "UNAVAILABLE", "504", "DEADLINE_EXCEEDED")):
                print(f"  {what}: rate limited, waiting {30 * attempt} s", file=sys.stderr)
                await asyncio.sleep(30 * attempt)
            else:
                raise


async def run_agent(questions: list[dict]) -> dict:
    cache = load_json(ANSWERS)
    if cache.get("version") != AGENT_VERSION:
        cache = {"version": AGENT_VERSION, "model": agent.MODEL, "answers": {}}
    todo = [q for q in questions if q["id"] not in cache["answers"]]
    if todo:
        async with AsyncExitStack() as stack:
            bot = agent.build_agent(await agent.load_mcp_tools(stack))  # add_document is refused: no one to ask
            for i, q in enumerate(todo, 1):
                out = await with_retry(lambda: agent.ask(bot, q["question"]), q["id"])
                cache["answers"][q["id"]] = out
                save_json(ANSWERS, cache)  # save each one
                print(f"  answered {q['id']} ({i}/{len(todo)}, {out['seconds']} s)")
    return cache["answers"]


# =============================================================================
# 3. Code checks
# =============================================================================
REFUSAL = re.compile(r"do(?:es)? not cover|not covered|no information|cannot find|could not find", re.I)
RESULT_LINE = re.compile(r"^(?:result )?\[\d+\] (.+?)(?: \| |$)", re.MULTILINE)


def code_checks(q: dict, out: dict) -> dict:
    retrieved = {m for line in out["trace"] if line.startswith("result ") for m in RESULT_LINE.findall(line)}
    answerable = q["kind"] != "unanswerable"
    passages = expected_passages(q) if answerable else []
    return {
        "searched": any(line.startswith("call search") for line in out["trace"]),
        "citations_valid": not out["unsupported_citations"],
        "has_citation": bool(out["citations"]),
        "refusal_phrase": bool(REFUSAL.search(out["answer"])),
        "expected_retrieved": (any(f"{s}, {l}" in retrieved for s, l in passages) if answerable else ""),
        "all_expected_retrieved": (all(f"{s}, {l}" in retrieved for s, l in passages) if answerable else ""),
    }


# =============================================================================
# 4. LLM judge
# =============================================================================
class Verdict(BaseModel):
    """The judge returns this structure, not free text, so code can count it.
    Reasoning comes first so the model explains before it decides."""
    reasoning: str = Field(description="Three or four sentences checking the answer against each criterion.")
    refused: bool = Field(description="True if the answer says the documents do not cover the question.")
    correct: bool = Field(description="True only if the answer meets the 'correct' criterion.")
    supported: bool = Field(description="True only if every claim is in the retrieved passages.")


JUDGE_PROMPT = """You grade an assistant that answers travel-agency staff about EU passenger rights. It must answer only from passages returned by its search tool, cite them, and say when the documents do not cover a question.

Criteria:
- refused: the answer says the documents do not cover the question (instead of answering it).
- correct:
  * If the question is answerable: the answer's verdict and its key amount, time limit or condition match the reference answer. Extra details are fine if they do not contradict it. If the question needs two rules (kind "multi"), both parts must be right; one part missing or wrong makes it incorrect. A refusal is incorrect.
  * If the question is unanswerable: correct only if the answer refuses and does not invent the missing answer. Pointing to related rules that are in the passages is fine.
- supported: every factual claim in the answer is stated in the retrieved passages of the tool trace. A citation is not enough: the cited passage must say it. Claims from general knowledge fail. A plain refusal is supported.

Question ({kind}): {question}
Reference answer: {reference_answer}

Tool trace (calls and the passages they returned, recorded by the harness):
{trace}

Answer to grade:
{answer}"""

JUDGE_VERSION = fingerprint(JUDGE_MODEL, JUDGE_PROMPT, json.dumps(Verdict.model_json_schema()))


async def run_judge(questions: list[dict], answers: dict) -> dict:
    cache = load_json(VERDICTS)
    if cache.get("version") != JUDGE_VERSION:
        cache = {"version": JUDGE_VERSION, "model": JUDGE_MODEL, "verdicts": {}}
    judge = ChatGoogleGenerativeAI(model=JUDGE_MODEL, temperature=0, api_key=load_api_key(), max_retries=1, timeout=180) \
        .with_structured_output(Verdict, include_raw=True)
    for q in questions:
        out = answers[q["id"]]
        key = fingerprint(out["answer"])
        if cache["verdicts"].get(q["id"], {}).get("answer_hash") == key:
            continue
        prompt = JUDGE_PROMPT.format(**q, trace="\n".join(out["trace"]) or "(no tool calls)", answer=out["answer"])
        start = time.perf_counter()
        result = await with_retry(lambda: judge.ainvoke(prompt), f"judge {q['id']}")
        usage = result["raw"].usage_metadata or {}
        cache["verdicts"][q["id"]] = {
            **result["parsed"].model_dump(), "answer_hash": key,
            "judge_seconds": round(time.perf_counter() - start, 1),
            "judge_input_tokens": usage.get("input_tokens", 0),
            "judge_output_tokens": usage.get("output_tokens", 0),
        }
        save_json(VERDICTS, cache)
        print(f"  judged {q['id']}")
    return cache["verdicts"]


# =============================================================================
# 5. Outcomes, agreement with the human labels, cost
# =============================================================================
def outcome(q: dict, v: dict) -> str:
    if q["kind"] == "unanswerable":
        return "correct refusal" if v["refused"] else "unsupported"
    if v["refused"]:
        return "wrong refusal"
    if not v["supported"]:
        return "unsupported"
    return "correct" if v["correct"] else "incorrect"


def load_human_labels() -> dict:
    if not HUMAN_LABELS.exists():
        return {}
    with HUMAN_LABELS.open(newline="") as f:
        return {r["id"].strip(): r for r in csv.DictReader(f)
                if r.get("id", "").strip() and r.get("correct", "").strip() and r.get("supported", "").strip()}


def agreement(labels: dict, verdicts: dict) -> dict:
    ids = [i for i in labels if i in verdicts]
    result = {"answers": len(ids)}
    if not ids:
        return result
    for field in ("correct", "supported"):
        same = [i for i in ids if (labels[i][field].strip() == "1") == verdicts[i][field]]
        result[field] = round(len(same) / len(ids), 3)
        result[f"{field}_disagree"] = [i for i in ids if i not in same]
    both = [i for i in ids if i not in result["correct_disagree"] and i not in result["supported_disagree"]]
    result["both"] = round(len(both) / len(ids), 3)
    return result


def write_labeling_sheet(questions: list[dict], answers: dict) -> None:
    """A readable sheet for grading by hand, without the judge's verdicts."""
    lines = ["# Human labels: grade these before reading eval/verdicts.json",
             "",
             "For each answer, write in eval/human_labels.csv: `correct` 1/0 (right against the reference, "
             "or a proper refusal for unanswerable; for multi, both parts must be right), `supported` 1/0 "
             "(every claim is in the retrieved passages), and `notes` saying why for every 0.",
             ""]
    by_id = {q["id"]: q for q in questions}
    for qid in HUMAN_LABEL_IDS:
        q, out = by_id[qid], answers[qid]
        retrieved = [line.split("\n")[0].removeprefix("result ") for line in out["trace"]
                     if line.startswith(("call", "result"))]
        lines += [f"## {qid} ({q['kind']})", "", f"**Question:** {q['question']}", "",
                  f"**Reference:** {q['reference_answer']}", "",
                  "**Agent's searches and top hit of each:**", ""]
        lines += [f"- {r[:200]}" for r in retrieved]
        lines += ["", "**Answer:**", "", out["answer"], "", "---", ""]
    (EVAL_DIR / "labeling_sheet.md").write_text("\n".join(lines))


def summarize(questions, answers, checks, verdicts, labels) -> dict:
    by_kind = {}
    for q in questions:
        o = outcome(q, verdicts[q["id"]])
        by_kind.setdefault(q["kind"], {}).setdefault(o, 0)
        by_kind[q["kind"]][o] += 1
    totals = {}
    for counts in by_kind.values():
        for o, n in counts.items():
            totals[o] = totals.get(o, 0) + n
    n = len(questions)
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    unanswerable = [q for q in questions if q["kind"] == "unanswerable"]
    a = list(answers.values())
    return {
        "agent_model": agent.MODEL, "judge_model": JUDGE_MODEL, "questions": n,
        "outcomes": totals, "outcomes_by_kind": by_kind,
        "rates": {
            "correct_on_answerable": round(totals.get("correct", 0) / len(answerable), 3),
            "unsupported_on_all": round(totals.get("unsupported", 0) / n, 3),
            "correct_refusals_on_unanswerable": round(totals.get("correct refusal", 0) / len(unanswerable), 3),
            "wrong_refusals_on_answerable": round(totals.get("wrong refusal", 0) / len(answerable), 3),
        },
        "code_checks": {
            "searched": sum(c["searched"] for c in checks.values()),
            "citations_valid": sum(c["citations_valid"] for c in checks.values()),
            "answerable_with_citation": sum(checks[q["id"]]["has_citation"] for q in answerable),
            "expected_passage_retrieved": sum(checks[q["id"]]["expected_retrieved"] for q in answerable),
            "refusal_phrase_agrees_with_judge": sum(checks[q["id"]]["refusal_phrase"] == verdicts[q["id"]]["refused"]
                                                    for q in questions),
            "citation_retries": sum(x["citation_retry"] for x in a),
        },
        "human_agreement": agreement(labels, verdicts),
        "cost_per_question": {
            "agent_model_calls": round(sum(x["model_calls"] for x in a) / n, 2),
            "agent_input_tokens": round(sum(x["input_tokens"] for x in a) / n),
            "agent_output_tokens": round(sum(x["output_tokens"] for x in a) / n),
            "agent_seconds": round(sum(x["seconds"] for x in a) / n, 1),
            "judge_input_tokens": round(sum(v["judge_input_tokens"] for v in verdicts.values()) / n),
            "judge_output_tokens": round(sum(v["judge_output_tokens"] for v in verdicts.values()) / n),
        },
    }


# =============================================================================
# 6. Adding a document: before and after
# =============================================================================
ADDED_FOR = "q33"  # package holiday, hotel overbooked: not covered by the transport regulations
ADDED_DOC = {"celex": "32015L2302", "path": index.CORPUS_DIR / "Directive (EU) 2015-2302 (Package Travel).html"}
BEFORE_AFTER = EVAL_DIR / "before_after.json"


async def before_after(questions: list[dict], answers: dict) -> dict:
    cached = load_json(BEFORE_AFTER)
    if cached.get("version") == AGENT_VERSION:
        return cached
    import server  # the design it serves, and its open index
    q = next(q for q in questions if q["id"] == ADDED_FOR)
    path = index.download(ADDED_DOC)
    # Added here, through server.py's own add_document, rather than by the agent: this process
    # also removes it afterwards, so only one process ever writes to the index. (The agent's
    # route to add_document, with its approval prompt, is shown in REPORT.md.)
    added = server.add_document(str(path))
    try:
        async with AsyncExitStack() as stack:  # a fresh server process, which loads the index with it
            bot = agent.build_agent(await agent.load_mcp_tools(stack))
            after = await with_retry(lambda: agent.ask(bot, q["question"]), "after")
    finally:  # remove it again, even if a step failed
        ids = server.store.get(where={"source": path.stem})["ids"]
        if ids:
            server.store.delete(ids=ids)
    before = answers[q["id"]]
    result = {
        "version": AGENT_VERSION, "id": q["id"], "question": q["question"], "document": path.stem,
        "before": {"answer": before["answer"], "citations": before["citations"]},
        "add_document": added,
        "after": {"answer": after["answer"], "citations": after["citations"],
                  "searches": [line for line in after["trace"] if line.startswith("call")]},
    }
    save_json(BEFORE_AFTER, result)
    return result


async def main(answers_only: bool = False) -> None:
    questions = load_questions()

    print("1. Retrieval")
    rows = retrieval_eval(questions, query_vectors(questions))
    write_csv(EVAL_DIR / "retrieval.csv", rows)
    for r in rows:
        print(f"  {r['design']:9} k={r['k']}  hit rate {r['hit_rate']:.3f}  multi all {r['multi_all_passages']}"
              f"  words {r['avg_words_added']}")

    print("2. Answers")
    answers = await run_agent(questions)
    print("3. Code checks")
    checks = {q["id"]: code_checks(q, answers[q["id"]]) for q in questions}
    write_labeling_sheet(questions, answers)
    if answers_only:
        print("  stopped before the judge; grade eval/labeling_sheet.md into eval/human_labels.csv")
        return

    print("4. Judge")
    verdicts = await run_judge(questions, answers)

    print("5. Summary")
    labels = load_human_labels()
    results = []
    for q in questions:
        v, out = verdicts[q["id"]], answers[q["id"]]
        results.append({
            "id": q["id"], "kind": q["kind"], "outcome": outcome(q, v),
            "judge_refused": v["refused"], "judge_correct": v["correct"], "judge_supported": v["supported"],
            **{f"code_{k}": c for k, c in checks[q["id"]].items()},
            "human_correct": labels.get(q["id"], {}).get("correct", ""),
            "human_supported": labels.get(q["id"], {}).get("supported", ""),
            "citations": "; ".join(out["citations"]),
            "seconds": out["seconds"], "input_tokens": out["input_tokens"], "output_tokens": out["output_tokens"],
            "judge_reasoning": v["reasoning"],
        })
    write_csv(EVAL_DIR / "results.csv", results)
    summary = summarize(questions, answers, checks, verdicts, labels)
    save_json(EVAL_DIR / "summary.json", summary)
    print(json.dumps(summary, indent=1))

    print("6. Adding a document")
    demo = await before_after(questions, answers)
    print(f"  {demo['id']}: {demo['question']}\n  BEFORE: {demo['before']['answer']}\n"
          f"  ADD: {demo['add_document']}\n  AFTER: {demo['after']['answer']}")


if __name__ == "__main__":
    asyncio.run(main(answers_only="--answers-only" in sys.argv))
