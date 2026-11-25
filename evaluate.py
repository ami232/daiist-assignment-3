"""
Assignment 3: evaluation (`main.py evaluate`). Built from session 10's 07-own-harness/evaluate.py.

1. Retrieval: hit rate at k = 1, 3, 5 for each design (structure, fixed, hybrid), and the words each
   design adds to the prompt; the best design is written to index/config.json.
2. End to end: the agent answers every question in eval/questions.csv.
3. Code checks: citations valid (the guardrail), refusals where the corpus has no answer, wrong
   refusals where it has one, and whether the expected source was cited.
4. LLM judge (a stronger model than the agent) with a rubric and the retrieved text as evidence.
5. Agreement between the judge and my own grades in eval/human_labels.csv.
6. Adding a document: one unanswerable question asked before and after add_document.

Results go to eval/: retrieval.csv, answers.jsonl, results.csv, summary.json, add_document_demo.json.
Agent answers are cached in answers.jsonl, so re-running costs no quota; set EVAL_FRESH=1 to redo them.
"""

import asyncio
import csv
import json
import os
import re
import sys
import time
from contextlib import AsyncExitStack
from pathlib import Path

from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

import index as pipeline
from agent import REFUSAL, REFUSED, ask, build_agent, check_citations, load_mcp_tools, parse_citations
from api_key import load_api_key
from retrieve import BASE_ONLY, CONFIG, QueryEmbedder, Searcher

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
JUDGE_MODEL = "gemini-3.5-flash"   # stronger than the agent's model, so it does not share its blind spots
DESIGNS = ["structure", "fixed", "hybrid"]
KS = [1, 3, 5]
DEMO_QUESTION = "q41"              # unanswerable until the simplified-treatment notice is added
DEMO_DOC = {"source": "STN", "celex": "52023XC0505(01)"}


def read_questions() -> list[dict]:
    with (EVAL / "questions.csv").open(newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r["question"].strip()]


def expected(q: dict) -> list[tuple[str, str]]:
    if q["kind"] == "unanswerable":
        return []
    return list(zip(q["expected_source"].split(";"), q["expected_location"].split(";")))


def covers(chunk: dict, source: str, location: str) -> bool:
    return chunk["source"] == source and location in chunk["units"]


# --------------------------------------------------------------------------- 1. retrieval

def evaluate_retrieval(questions: list[dict]) -> dict:
    embedder = QueryEmbedder()  # shared: each question is embedded once for all designs
    rows, summary = [], {}
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    for design in DESIGNS:
        searcher = Searcher(design, embedder)
        hits = {k: 0 for k in KS}
        words = []
        for q in answerable:
            results = searcher.search(q["question"], k=max(KS))
            words.append(sum(len(r["text"].split()) for r in results))
            row = {"design": design, "id": q["id"], "kind": q["kind"]}
            for k in KS:
                top = results[:k]
                # a hit needs every expected passage in the top k (both, for multi questions)
                hit = all(any(covers(c, s, l) for c in top) for s, l in expected(q))
                hits[k] += hit
                row[f"hit@{k}"] = int(hit)
            row["top5"] = " | ".join(f"{r['source']} {r['location']}" for r in results)
            rows.append(row)
        n = len(answerable)
        summary[design] = {**{f"hit@{k}": round(hits[k] / n, 3) for k in KS},
                           "words_in_prompt_top5": round(sum(words) / n),
                           "chunks": len(searcher.chunks)}
        pipeline.log(design, summary[design])
    with (EVAL / "retrieval.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    # choose by hit@5, then hit@3, then hit@1, then fewer words in the prompt
    best = max(DESIGNS, key=lambda d: (summary[d]["hit@5"], summary[d]["hit@3"], summary[d]["hit@1"],
                                       -summary[d]["words_in_prompt_top5"]))
    CONFIG.write_text(json.dumps({"design": best}, indent=2))
    return {"designs": summary, "chosen": best}


# --------------------------------------------------------------------------- 2-3. agent and code checks

def load_answers() -> dict:
    path = EVAL / "answers.jsonl"
    if os.environ.get("EVAL_FRESH") or not path.exists():
        return {}
    return {r["id"]: r for r in map(json.loads, path.read_text(encoding="utf-8").splitlines()) if r}


def recheck(a: dict) -> dict:
    """Apply the current citation guardrail to a cached raw answer (no model call needed)."""
    ok, reason = check_citations(a["raw_answer"], a["trace"])
    shown = a["raw_answer"] if ok else (f"Answer withheld by the citation guardrail ({reason}). "
                                        f"{REFUSAL} Please check with counsel or rephrase the question.")
    return {**a, "answer": shown, "guardrail_ok": ok, "guardrail_reason": reason}


async def run_agent(questions: list[dict]) -> dict:
    answers = {k: recheck(v) for k, v in load_answers().items()}
    if answers:  # save the re-checked versions, so every file shows what the associate would see now
        (EVAL / "answers.jsonl").write_text(
            "".join(json.dumps(a, ensure_ascii=False) + "\n" for a in answers.values()), encoding="utf-8")
    todo = [q for q in questions if q["id"] not in answers]
    if todo:
        BASE_ONLY.touch()  # the server ignores documents added later, so the test set means the same
        async with AsyncExitStack() as stack:
            agent = build_agent(await load_mcp_tools(stack), auto_approve=False)
            for q in todo:
                for attempt in range(3):
                    try:
                        out = await ask(agent, q["question"])
                        break
                    except Exception as error:  # noqa: BLE001 - rate limits: wait and retry
                        pipeline.log(f"{q['id']}: {error}; retrying")
                        time.sleep(30 * (attempt + 1))
                else:
                    out = {"answer": "", "raw_answer": "", "trace": [], "guardrail_ok": False,
                           "guardrail_reason": "agent error", "tokens": {"input": 0, "output": 0}, "seconds": 0}
                answers[q["id"]] = {"id": q["id"], **out}
                with (EVAL / "answers.jsonl").open("a", encoding="utf-8") as f:
                    f.write(json.dumps(answers[q["id"]], ensure_ascii=False) + "\n")
                pipeline.log(f"{q['id']} answered in {out['seconds']}s")
        BASE_ONLY.unlink(missing_ok=True)
    return answers


def code_checks(q: dict, a: dict) -> dict:
    cited = set(parse_citations(a["answer"]))
    refused = a["answer"].strip() == "" or (bool(REFUSED.search(a["answer"])) and not cited)
    cited_sources = {c.split(" ")[0] for c in cited}
    exp_sources = {s for s, _ in expected(q)}
    return {
        "citations_valid": a["guardrail_ok"],
        "refused": refused,
        "correct_refusal": q["kind"] == "unanswerable" and refused,
        "wrong_refusal": q["kind"] != "unanswerable" and refused,
        "cites_expected_source": bool(exp_sources) and exp_sources <= cited_sources,
        "searched": any(line.startswith("call search") for line in a["trace"]),
    }


# --------------------------------------------------------------------------- 4. judge

class Verdict(BaseModel):
    reasoning: str = Field(description="Two to four sentences checking the answer against each criterion.")
    correct: bool = Field(description="True if the answer agrees with the reference answer (or properly refuses when the reference says the documents do not cover it).")
    supported: bool = Field(description="True only if every factual claim in the answer appears in the retrieved passages.")


JUDGE_HEADER = """You are grading an assistant that answers M&A associates' questions about EU merger control and FDI screening, using only passages retrieved from legal texts. Grade every item below separately, using only that item's own reference answer and retrieved passages, and return one grade per item with its id.

Criteria:
1. Correct: the answer gives the same substance as the reference answer (numbers, deadlines, conditions). Extra correct detail is fine; a missing key condition or a wrong number fails. If the reference says the documents do not cover the question, the answer is correct only if it clearly says the documents do not cover it and does not answer from general knowledge. If the answer refuses but the reference has an answer, it is not correct.
2. Supported: every factual claim in the answer appears in the item's retrieved passages. Anything not in them is unsupported, even if it is true. A pure refusal counts as supported.

"""

JUDGE_ITEM = """Question: {question}
Reference answer: {reference}
Retrieved passages (what the search tool really returned, recorded by the harness):
{evidence}

Answer shown to the associate:
{answer}"""


def evidence(trace: list[str], limit: int = 16000) -> str:
    text = "\n".join(line.removeprefix("result ") for line in trace if line.startswith("result "))
    return text[:limit] or "(no passages retrieved)"


class GradedItem(Verdict):
    id: str = Field(description="The question id, copied exactly.")


class Grades(BaseModel):
    grades: list[GradedItem]


JUDGE_BATCH = 6   # the judge model's free tier allows only 20 requests a day, so several answers go in one call


async def judge_all(questions: list[dict], answers: dict) -> dict:
    """Grade every answer, JUDGE_BATCH at a time, keeping each answer's own rubric and evidence.
    Verdicts are saved as they come; if the daily quota runs out the rest are graded on the next run."""
    path = EVAL / "verdicts.jsonl"
    verdicts = {} if os.environ.get("EVAL_FRESH") or not path.exists() else \
        {r["id"]: r for r in map(json.loads, path.read_text(encoding="utf-8").splitlines()) if r}
    judge = ChatGoogleGenerativeAI(model=JUDGE_MODEL, temperature=0).with_structured_output(Grades)
    todo = [q for q in questions if q["id"] not in verdicts]
    for i in range(0, len(todo), JUDGE_BATCH):
        batch = todo[i:i + JUDGE_BATCH]
        prompt = JUDGE_HEADER + "\n\n".join(
            f"=== Item {q['id']} ===\n" + JUDGE_ITEM.format(
                question=q["question"], reference=q["reference_answer"],
                evidence=evidence(answers[q["id"]]["trace"], limit=16000),
                answer=answers[q["id"]]["answer"] or "(empty)") for q in batch)
        grades = None
        for attempt in range(3):
            try:
                grades = (await judge.ainvoke(prompt)).grades
                break
            except Exception as error:  # noqa: BLE001
                if "PerDay" in str(error) or "per day" in str(error).lower():
                    pipeline.log("judge: daily quota reached; run evaluate again tomorrow to grade the rest")
                    return verdicts
                pipeline.log(f"judge: {str(error)[:120]}; retrying")
                time.sleep(30 * (attempt + 1))
        if grades is None:
            pipeline.log("judge: giving up for now; run evaluate again later")
            return verdicts
        wanted = {q["id"] for q in batch}
        with path.open("a", encoding="utf-8") as f:
            for g in grades:
                if g.id in wanted and g.id not in verdicts:
                    verdicts[g.id] = g.model_dump()
                    f.write(json.dumps(verdicts[g.id], ensure_ascii=False) + "\n")
    return verdicts


# --------------------------------------------------------------------------- 5. agreement

def agreement(verdicts: dict) -> dict:
    path = EVAL / "human_labels.csv"
    if not path.exists():
        return {"graded": 0}
    with path.open(newline="", encoding="utf-8") as f:
        labels = [r for r in csv.DictReader(f) if (r.get("id") or "").strip() and r.get("correct", "").strip() != ""]
    both = [r for r in labels if r["id"] in verdicts]
    if not both:
        return {"graded": 0}
    out = {"graded": len(both)}
    for field in ("correct", "supported"):
        same = [int(r[field]) == int(verdicts[r["id"]][field]) for r in both if r.get(field, "").strip() != ""]
        out[f"{field}_agreement"] = round(sum(same) / len(same), 3) if same else None
        out[f"{field}_disagree_ids"] = [r["id"] for r in both if r.get(field, "").strip() != ""
                                        and int(r[field]) != int(verdicts[r["id"]][field])]
    return out


# --------------------------------------------------------------------------- 6. adding a document

async def add_document_demo(questions: list[dict], answers: dict) -> dict:
    path = EVAL / "add_document_demo.json"
    if path.exists() and not os.environ.get("EVAL_FRESH"):
        return json.loads(path.read_text(encoding="utf-8"))
    q = next(x for x in questions if x["id"] == DEMO_QUESTION)
    doc = pipeline.CORPUS / f"{DEMO_DOC['source']}.html"
    if not doc.exists():
        import httpx
        r = httpx.get(pipeline.URL.format(celex=DEMO_DOC["celex"]), follow_redirects=True, timeout=60)
        doc.write_bytes(r.content)
    async with AsyncExitStack() as stack:
        tools = await load_mcp_tools(stack)
        agent = build_agent(tools, auto_approve=True)
        add = next(t for t in tools if t.name == "add_document")
        added = await add.ainvoke({"path": str(doc)})
        after = await ask(agent, q["question"])
        added_again = await add.ainvoke({"path": str(doc)})  # the "already indexed" case
    demo = {"question": q["question"], "document": f"{DEMO_DOC['source']} (CELEX {DEMO_DOC['celex']})",
            "before": answers[q["id"]]["answer"], "add_document": str(added),
            "after": after["answer"], "after_trace": after["trace"], "add_again": str(added_again)}
    path.write_text(json.dumps(demo, indent=2, ensure_ascii=False), encoding="utf-8")
    return demo


def guardrail_test(answers: dict) -> dict:
    """The agent cited correctly on every question, so to show the citation guardrail catching a
    real problem I take a real answer and add one citation the search never returned (as a model
    remembering an article from training would), plus the same answer with its citations removed."""
    a = answers["q03"]
    invented = a["raw_answer"] + " Fines for this are set out in [EUMR Art. 21(4)]."
    uncited = re.sub(r"\s*\[[^\]]+\]", "", a["raw_answer"])
    return {"question": "q03",
            "invented_citation": dict(zip(("ok", "reason"), check_citations(invented, a["trace"]))),
            "no_citations": dict(zip(("ok", "reason"), check_citations(uncited, a["trace"]))),
            "original": dict(zip(("ok", "reason"), check_citations(a["raw_answer"], a["trace"])))}


# --------------------------------------------------------------------------- main

async def main():
    load_api_key()
    questions = read_questions()
    retrieval = evaluate_retrieval(questions)
    print(json.dumps(retrieval, indent=2))

    answers = await run_agent(questions)
    verdicts = await judge_all(questions, answers)

    rows = []
    for q in questions:
        a = answers[q["id"]]
        v = verdicts.get(q["id"], {"correct": None, "supported": None, "reasoning": "not graded yet"})
        rows.append({"id": q["id"], "kind": q["kind"], **code_checks(q, a),
                     "judge_correct": v["correct"], "judge_supported": v["supported"],
                     "tokens_in": a["tokens"]["input"], "tokens_out": a["tokens"]["output"], "seconds": a["seconds"],
                     "guardrail_reason": a["guardrail_reason"], "judge_reasoning": v["reasoning"]})
    with (EVAL / "results.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    ans = [r for r in rows if r["kind"] != "unanswerable"]
    una = [r for r in rows if r["kind"] == "unanswerable"]
    n = len(rows)
    summary = {
        "retrieval": retrieval,
        "questions": {"total": n, "answerable": len(ans), "unanswerable": len(una)},
        "end_to_end": {
            "judged": sum(r["judge_correct"] is not None for r in rows),
            "correct": sum(bool(r["judge_correct"]) for r in rows),
            "correct_answerable": sum(bool(r["judge_correct"]) for r in ans),
            "unsupported": sum(r["judge_supported"] is False for r in rows),
            "correct_refusals": sum(r["correct_refusal"] for r in una),
            "wrong_refusals": sum(r["wrong_refusal"] for r in ans),
            "answered_unanswerable": sum(not r["refused"] for r in una),
            "citation_guardrail_fired": sum(not r["citations_valid"] for r in rows),
            "cites_expected_source": sum(r["cites_expected_source"] for r in ans),
        },
        "cost_per_question": {
            "tokens_in": round(sum(r["tokens_in"] for r in rows) / n),
            "tokens_out": round(sum(r["tokens_out"] for r in rows) / n),
            "seconds": round(sum(r["seconds"] for r in rows) / n, 1),
        },
        "human_vs_judge": agreement(verdicts),
    }
    summary["guardrail_test"] = guardrail_test(answers)
    summary["add_document_demo"] = await add_document_demo(questions, answers)
    (EVAL / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k != "add_document_demo"}, indent=2))
    print("\nAdding a document:", summary["add_document_demo"]["add_document"])
    print("Before:", summary["add_document_demo"]["before"][:300])
    print("After: ", summary["add_document_demo"]["after"][:500])


if __name__ == "__main__":
    asyncio.run(main())
