"""
Assignment 3: evaluation (`main.py evaluate`).

Part 1. Retrieval hit rate at k = 1, 3, 5 for every design:
2 chunkings (structure, fixed) x 3 search methods (dense, bm25, hybrid).
A retrieved chunk "hits" a passage when it comes from the expected document and
contains the expected article / disposición / anexo. A `single` question is a hit
at k if any expected passage is in the top k; a `multi` question only if all are.
Writes eval/retrieval_per_question.csv and eval/retrieval_summary.csv.

Part 2. End to end: run agent.py on every question, check in code what code can
check (refusal, valid citations, expected passage retrieved), then ask a judge model
to grade correctness and support against a rubric. Compares the judge with
eval/human_labels.csv, and shows the answer to one unanswerable question before
and after adding a document. Writes eval/results.json (resumable), eval/answers.csv,
eval/summary.json and eval/before_after.json.
"""

import asyncio
import csv
import json
import re
from contextlib import AsyncExitStack
from pathlib import Path

from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

import agent
import index
import retrieve
from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
EVAL_DIR = ROOT / "eval"
QUESTIONS = EVAL_DIR / "questions.csv"
QUERY_CACHE = EVAL_DIR / "query_vectors.json"
DESIGNS = [(s, m) for s in ("structure", "fixed") for m in ("dense", "bm25", "hybrid")]
KS = (1, 3, 5)

RESULTS = EVAL_DIR / "results.json"
HUMAN_LABELS = EVAL_DIR / "human_labels.csv"
JUDGE_MODEL = "gemini-3.1-flash-lite"   # a different model from the agent's (3.5-flash allows only 20 calls/day)
ADD_QUESTION = "q36"               # unanswerable question the new document answers
ADD_DOCUMENT = ROOT / "new_documents" / "BOE-A-2026-6642.pdf"   # Ley 2/2026, tourist-tax rates


def load_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r["question"].strip()]


def query_vectors(questions: list[dict]) -> dict[str, list[float]]:
    """Embed each question once and keep the vectors in eval/query_vectors.json."""
    cache = json.loads(QUERY_CACHE.read_text()) if QUERY_CACHE.exists() else {}
    missing = [q["question"] for q in questions if q["question"] not in cache]
    for i in range(0, len(missing), index.EMBED_BATCH):
        batch = missing[i:i + index.EMBED_BATCH]
        cache.update(zip(batch, index.embed_texts(batch, task_type="RETRIEVAL_QUERY")))
        QUERY_CACHE.write_text(json.dumps(cache))
    return cache


def unit_labels(location: str) -> set[str]:
    """'art. 9 bis.1' -> {'artículo 9 bis'}; 'art. 1.1 y Anexo' -> {'artículo 1', 'anexo'};
    'disposición transitoria segunda.2' -> {'disposición transitoria segunda'}."""
    location = re.sub(r"\(.*?\)", "", location.lower())
    labels = {f"artículo {n}" for n in re.findall(r"art\.?\s*(\d+(?: (?:bis|ter|quater))?)", location)}
    labels |= {f"disposición {d.strip()}" for d in re.findall(
        r"disposición ((?:adicional|transitoria|derogatoria|final)(?: [a-záéíóúñ]+)*)", location)}
    if "anexo" in location:
        labels.add("anexo")
    return labels


def expected_passages(q: dict) -> list[tuple[str, set[str]]]:
    """[(source, acceptable unit labels)] per passage; sources pair with locations by position."""
    sources = [s.strip() for s in q["expected_source"].split(";") if s.strip()]
    locations = [l.strip() for l in q["expected_location"].split(";") if l.strip()]
    passages = []
    for i, location in enumerate(locations):
        labels = unit_labels(location)
        if labels:   # e.g. "encabezado" names no article: nothing to match
            passages.append((sources[min(i, len(sources) - 1)], labels))
    return passages


def chunk_units(metadata: dict) -> set[str]:
    units = metadata.get("articles") or metadata.get("article", "")
    return {u.lower() for u in units.split("|")}


def first_hit_rank(passage: tuple[str, set[str]], results: list[dict]) -> int | None:
    source, labels = passage
    for rank, r in enumerate(results, start=1):
        if r["metadata"]["source"] == source and chunk_units(r["metadata"]) & labels:
            return rank
    return None


def retrieval_eval(questions: list[dict]) -> list[dict]:
    answerable = [q for q in questions if q["kind"].strip() != "unanswerable"]
    vectors = query_vectors(answerable)
    rows, summary = [], []
    for strategy, method in DESIGNS:
        design = f"{strategy}+{method}"
        for q in answerable:
            results = retrieve.search(q["question"], k=max(KS), strategy=strategy, method=method,
                                      query_vector=vectors[q["question"]])
            ranks = [first_hit_rank(p, results) for p in expected_passages(q)]
            # rank at which the question is satisfied: any passage (single) or all (multi)
            if q["kind"].strip() == "multi":
                needed = None if None in ranks else max(ranks)
            else:
                needed = min((r for r in ranks if r), default=None)
            row = {"design": design, "id": q["id"], "kind": q["kind"], "rank": needed or ""}
            row.update({f"hit@{k}": int(needed is not None and needed <= k) for k in KS})
            row["top5"] = " | ".join(r["metadata"]["citation"] for r in results)
            rows.append(row)
        for kind in ("all", "single", "multi"):
            sel = [r for r in rows if r["design"] == design and kind in ("all", r["kind"])]
            summary.append({"design": design, "questions": kind, "n": len(sel),
                            **{f"hit@{k}": round(sum(r[f"hit@{k}"] for r in sel) / len(sel), 3) for k in KS}})

    write_csv(EVAL_DIR / "retrieval_per_question.csv", rows)
    write_csv(EVAL_DIR / "retrieval_summary.csv", summary)
    print("\nRetrieval hit rate (answerable questions)\n")
    print(f"{'design':<20}{'questions':<10}{'n':>4}" + "".join(f"{f'hit@{k}':>8}" for k in KS))
    for s in summary:
        print(f"{s['design']:<20}{s['questions']:<10}{s['n']:>4}" + "".join(f"{s[f'hit@{k}']:>8.2f}" for k in KS))
    return summary


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


# ---------------------------------------------------------------- Part 2: end to end

# The judge returns this structure, not free text, so the program can count.
# The reasoning comes first so the model explains before it decides.
class Verdict(BaseModel):
    reasoning: str = Field(description="Two or three sentences checking the answer against each criterion.")
    correct: bool = Field(description="True if the answer matches the reference answer (or is a proper refusal).")
    supported: bool = Field(description="True if every claim in the answer is in the retrieved passages.")


JUDGE_PROMPT = """You are grading an assistant that answers questions about Spanish and Catalan rental law
using only passages retrieved from the LAU, Llei 18/2007 and Decret-llei 3/2023.

Criteria:
1. Correct: the answer gives the key facts of the reference answer (figures, deadlines, conditions)
   without contradicting it. Extra detail is fine. If the reference says the corpus does not cover
   the question, the answer is correct only if it says so and does not answer from general knowledge.
2. Supported: every legal claim in the answer appears in the retrieved passages below. A claim that
   is plausible but not in the passages is unsupported. A plain refusal is supported.

Question: {question}
Reference answer: {reference}
Retrieved passages (what the search tool really returned, recorded by the harness):
{passages}
Answer:
{answer}"""

REFUSAL = re.compile(r"no (cubre|cubren|contiene|contienen|incluye|incluyen)|no se encuentra|"
                     r"do(?:es)? not (cover|contain|include)|not covered", re.I)
CITATION = re.compile(r"(LAU|Llei [\d/]+|Decret-llei [\d/]+),\s*(art|disposici|anexo|pre[áa]mbulo)", re.I)
RE_PASSAGE = re.compile(r"^\[\d+\] [^,]+, ([^,(]+).*\(source: ([^)]+)\)$", re.M)


def refused(answer: str) -> bool:
    return bool(REFUSAL.search(answer))


def retrieved_expected(q: dict, trace: list[dict]) -> bool:
    """Code check: did any search return every expected passage?"""
    found = {(unit.strip().lower(), source) for t in trace if t["tool"] == "search"
             for unit, source in RE_PASSAGE.findall(t["output"])}
    return all(any(src == source and unit in labels for unit, src in found)
               for source, labels in expected_passages(q))


def outcome(q: dict, r: dict) -> str:
    if q["kind"] == "unanswerable":
        return "correct refusal" if r["refused"] else "unsupported"
    if r["refused"] and not CITATION.search(r["answer"]):   # a cited partial answer is not a refusal
        return "wrong refusal"
    if not (r["supported"] and r["citations_ok"]):
        return "unsupported"
    return "correct" if r["correct"] else "incorrect"


def failure_cause(q: dict, r: dict) -> str:
    """First guess at the cause of a failure; check it by hand (bad test questions only a person can spot)."""
    o = r["outcome"]
    if o in ("correct", "correct refusal"):
        return ""
    if q["kind"] == "unanswerable":
        return "unsupported claim"
    if not r["retrieved_expected"]:
        return "retrieval miss"
    return {"wrong refusal": "wrong refusal", "unsupported": "unsupported claim"}.get(
        o, "wrong answer from right passage")


async def grade(judge, q: dict, r: dict) -> dict:
    passages = "\n\n".join(t["output"] for t in r["trace"] if t["tool"] == "search") or "(no search)"
    verdict = await judge.ainvoke(JUDGE_PROMPT.format(
        question=q["question"], reference=q["reference_answer"], passages=passages, answer=r["answer"]))
    r.update(verdict.model_dump(), refused=refused(r["answer"]), retrieved_expected=retrieved_expected(q, r["trace"]))
    r["outcome"] = outcome(q, r)
    r["failure_cause"] = failure_cause(q, r)
    return r


async def agent_eval(questions: list[dict]) -> dict:
    """Run and grade every question; results.json is saved after each one, so a rerun resumes."""
    results = json.loads(RESULTS.read_text()) if RESULTS.exists() else {}
    judge = ChatGoogleGenerativeAI(model=JUDGE_MODEL, api_key=load_api_key(), temperature=0,
                                   timeout=120, max_retries=2).with_structured_output(Verdict)
    async with AsyncExitStack() as stack:
        tools = await agent.load_tools(stack)
        bot = agent.build_agent(tools)
        for q in questions:
            try:   # answer and verdict are saved separately, so a judge failure keeps the answer
                if q["id"] not in results:
                    results[q["id"]] = await agent.ask(bot, q["question"])
                    RESULTS.write_text(json.dumps(results, indent=1, ensure_ascii=False))
                if "outcome" not in results[q["id"]]:
                    await grade(judge, q, results[q["id"]])
                    RESULTS.write_text(json.dumps(results, indent=1, ensure_ascii=False))
                    print(f"  {q['id']} {results[q['id']]['outcome']}")
            except Exception as e:   # API overloaded or quota hit: skip, the next run picks it up
                print(f"  {q['id']} skipped: {type(e).__name__}: {str(e)[:120]}")
        await before_after(tools, results, questions)
    return results


async def before_after(tools: list, results: dict, questions: list[dict]) -> None:
    """Add a document that answers one unanswerable question; ask it again."""
    out = EVAL_DIR / "before_after.json"
    if out.exists() or not ADD_DOCUMENT.exists() or not all("outcome" in results.get(q["id"], {}) for q in questions):
        return
    q = next(q for q in questions if q["id"] == ADD_QUESTION)
    add = next(t for t in tools if t.name == "add_document")
    added = await add.ainvoke({"path": str(ADD_DOCUMENT)})
    after = await agent.ask(agent.build_agent(tools), q["question"])
    out.write_text(json.dumps({"question": q["question"], "document": ADD_DOCUMENT.name, "add_document": added,
                               "before": results[ADD_QUESTION]["answer"], "after": after["answer"],
                               "after_trace": after["trace"]}, indent=1, ensure_ascii=False))
    print(f"\nBefore/after for {ADD_QUESTION} written to {out.relative_to(ROOT)}")


def summarise(questions: list[dict], results: dict) -> None:
    rows = [{"id": q["id"], "kind": q["kind"], "question": q["question"], "answer": r["answer"],
             "outcome": r["outcome"], "failure_cause": r["failure_cause"], "refused": int(r["refused"]),
             "citations_ok": int(r["citations_ok"]), "retrieved_expected": int(r["retrieved_expected"]),
             "judge_correct": int(r["correct"]), "judge_supported": int(r["supported"]),
             "judge_reasoning": r["reasoning"], "tokens": r["tokens"], "seconds": r["seconds"]}
            for q in questions if "outcome" in (r := results.get(q["id"], {}))]
    write_csv(EVAL_DIR / "answers.csv", rows)

    counts = {o: sum(r["outcome"] == o for r in rows)
              for o in ("correct", "incorrect", "unsupported", "correct refusal", "wrong refusal")}
    causes = {c: sum(r["failure_cause"] == c for r in rows) for c in {r["failure_cause"] for r in rows} if c}
    summary = {"answered": len(rows), "outcomes": counts, "failure_causes": causes,
               "avg_tokens": round(sum(r["tokens"] for r in rows) / len(rows)),
               "avg_seconds": round(sum(r["seconds"] for r in rows) / len(rows), 1),
               "agreement": agreement(rows)}
    (EVAL_DIR / "summary.json").write_text(json.dumps(summary, indent=1, ensure_ascii=False))
    print("\nEnd-to-end results\n")
    print(json.dumps(summary, indent=1, ensure_ascii=False))


def agreement(rows: list[dict]) -> dict:
    """How often the judge agrees with my own grades in eval/human_labels.csv."""
    with HUMAN_LABELS.open(newline="", encoding="utf-8") as f:
        human = {h["id"]: h for h in csv.DictReader(f) if h["correct"].strip()}
    pairs = [(human[r["id"]], r) for r in rows if r["id"] in human]
    if not pairs:
        return {"n": 0}
    return {"n": len(pairs),
            "correct": round(sum(int(h["correct"]) == r["judge_correct"] for h, r in pairs) / len(pairs), 2),
            "supported": round(sum(int(h["supported"]) == r["judge_supported"] for h, r in pairs) / len(pairs), 2)}


def main() -> None:
    questions = load_questions()
    retrieval_eval(questions)
    results = asyncio.run(agent_eval(questions))
    summarise(questions, results)


if __name__ == "__main__":
    main()
