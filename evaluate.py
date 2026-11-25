"""
Assignment 3: evaluation (`main.py evaluate`).

Stages:
 1. Retrieval: hit rate at k=1/3/5 for each chunking design.
A question is a HIT at k if at least one of the top-k chunks contains an expected
section (expected_location in eval/questions.csv). For multi-passage questions we also
report FULL coverage: every expected section is found in the top-k.
Unanswerable questions are skipped (they have no expected section).

    (a question is a HIT at k if an expected section is in the top-k chunks)
 2. Agent: every question goes through agent.py's agent; answer, tool trace, seconds and
    tokens are saved in eval/answers.json (reused on a re-run; --redo asks again).
    add_document is DENIED during evaluation: nobody is there to approve, and an unattended
    run must never change the index.
 3. Code checks (exact things code can verify): did it call search, does every cited section
    appear in the retrieved text, did it try add_document, did retrieval bring an expected section.
 4. LLM judge with a rubric and the retrieved text as evidence: correct / supported / refused.
 5. Agreement of the judge with your own grades in eval/human_labels.csv.

Order that keeps your grading honest: run `uv run evaluate.py --answers-only`, grade 20+
answers in eval/human_labels.csv from eval/answers_for_grading.csv, THEN run the full evaluation.
Results are saved in eval/.
"""

import asyncio
import csv
import json
import re
import sys
import time
from contextlib import AsyncExitStack
from pathlib import Path

from langchain_core.messages import AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

import index
from agent import build_agent, load_mcp_tools, tool_trace
from api_key import load_api_key

ROOT = Path(__file__).parent
QUESTIONS = ROOT / "eval" / "questions.csv"
KS = (1, 3, 5)
SECTION = re.compile(r"§ ?\d+\.\d+")


def load_questions():
    with open(QUESTIONS, encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def expected_sections(row):
    return {"§ " + m.group(0).lstrip("§ ") for m in SECTION.finditer(row["expected_location"])}


def chunk_sections(hit):
    return {s.strip() for s in str(hit.get("sections", "")).split(";") if s.strip()}


def retrieval_eval(designs=None):
    designs = designs or list(index.DESIGNS)
    rows = [r for r in load_questions() if r["kind"] != "unanswerable"]
    results = {}
    details = []
    for design in designs:
        counts = {k: 0 for k in KS}
        full = {k: 0 for k in KS}
        multi = [r for r in rows if r["kind"] == "multi"]
        for row in rows:
            expected = expected_sections(row)
            hits = index.retrieve(row["question"], k=max(KS), design=design)
            for k in KS:
                found = set().union(*(chunk_sections(h) for h in hits[:k])) if hits else set()
                got = bool(expected & found)
                counts[k] += got
                if row["kind"] == "multi":
                    full[k] += expected <= found
            ranks = [i + 1 for i, h in enumerate(hits) if expected & chunk_sections(h)]
            details.append({"design": design, "id": row["id"], "kind": row["kind"],
                            "expected": ";".join(sorted(expected)),
                            "first_hit_rank": ranks[0] if ranks else "",
                            "top1": hits[0]["location"] if hits else ""})
        n = len(rows)
        results[design] = {
            "questions": n,
            **{f"hit@{k}": round(counts[k] / n, 3) for k in KS},
            **{f"multi_full@{k}": f"{full[k]}/{len(multi)}" for k in KS},
            "chunks": index.get_collection(design).count(),
        }
    return results, details



EVAL = ROOT / "eval"
JUDGE_MODEL = "gemini-3.5-flash"  # a stronger model than the agent's
CONCURRENCY = 3  # questions asked at the same time (free-tier rate limits)
JUDGE_CONCURRENCY = 1  # the judge model has a smaller free quota: one at a time

# ---------------------------------------------------------------------------
# YOUR RUBRIC. This is the judge's definition of "good". Read it, change it to
# what YOU think is right, and be ready to explain every line.
# ---------------------------------------------------------------------------
JUDGE_RUBRIC = """\
For a question that the corpus CAN answer:
- correct: the answer states the same essential facts as the reference answer (same numbers,
  same conditions, same exceptions). Extra detail is fine if it is true to the retrieved text.
  A missing key fact, a wrong number or a wrong condition makes it NOT correct.
- supported: every claim in the answer is stated in the retrieved passages. A claim that is not
  in the retrieved passages is unsupported, even if it happens to be true in real life.
- refused: the answer says the documents do not cover the question or declines to answer.
For a question that the corpus CAN NOT answer:
- refused: the answer clearly says the documents do not cover it (it may suggest asking HR or the
  Wage and Hour Division). Giving a specific answer from memory is NOT a refusal.
- supported: nothing in the answer goes beyond the retrieved passages.
"""

JUDGE_PROMPT = """You are grading the answer of a RAG assistant about US federal workplace rules (29 CFR Parts 825, 785, 531).

Rubric:
{rubric}

Question: {question}
Kind: {kind}  ("unanswerable" means the corpus does not contain the answer)
Reference answer: {reference}

Retrieved passages and tool calls (what really happened, recorded by the harness):
{trace}

Assistant's answer:
{answer}
"""


class Verdict(BaseModel):
    # The reasoning comes first, so the model explains before it decides.
    reasoning: str = Field(description="Two or three sentences checking the answer against the rubric.")
    correct: bool = Field(description="Matches the reference answer (answerable questions only; false otherwise).")
    supported: bool = Field(description="Every claim is stated in the retrieved passages.")
    refused: bool = Field(description="The answer says the documents do not cover the question.")


CITED = re.compile(r"\b(?:785|825|531|778)\.\d+\b")
RETRIEVED = re.compile(r"^\[\d+\] (29 CFR Part \d+), (§ [\d.]+)", re.M)
REFUSAL_WORDS = ("do not cover", "does not cover", "not covered", "do not contain", "does not contain",
                 "not stated", "cannot find", "can't find", "no information", "not address", "not specif")


def retrieved_sections(trace):
    return {m.group(2) for line in trace if line.startswith("result ") for m in RETRIEVED.finditer(line.removeprefix("result "))}


def code_checks(row, answer, trace):
    """Exact checks that need no model. The refusal check is only a keyword heuristic."""
    retrieved = retrieved_sections(trace)
    cited = {"§ " + c for c in CITED.findall(answer)}
    expected = expected_sections(row)
    return {
        "searched": any(line.startswith("call search(") for line in trace),
        "tried_add_document": any(line.startswith("call add_document(") for line in trace),
        "citations_valid": cited <= retrieved,
        "cited_not_retrieved": sorted(cited - retrieved),
        "retrieval_ok": bool(expected & retrieved) if expected else None,
        "refusal_words": any(w in answer.lower() for w in REFUSAL_WORDS),
    }


def tokens_used(messages):
    total = 0
    for message in messages:
        if isinstance(message, AIMessage) and message.usage_metadata:
            total += message.usage_metadata.get("total_tokens", 0)
    return total


async def run_one(agent, row, semaphore):
    async with semaphore:
        started = time.time()
        for attempt in (1, 2):
            try:
                result = await agent.ainvoke({"messages": [{"role": "user", "content": row["question"]}]})
                answer, trace = result["messages"][-1].text, tool_trace(result["messages"])
                tokens = tokens_used(result["messages"])
                break
            except Exception as error:  # noqa: BLE001 - one bad question must not stop the run
                answer, trace, tokens = f"ERROR: {type(error).__name__}: {str(error)[:200]}", [], 0
                await asyncio.sleep(10)
        print(f"  asked {row['id']} ({time.time() - started:.0f}s)", flush=True)
        return {"id": row["id"], "answer": answer, "trace": trace,
                "seconds": round(time.time() - started, 1), "tokens": tokens}


async def collect_answers(rows, redo):
    path = EVAL / "answers.json"
    saved = {} if redo or not path.exists() else {a["id"]: a for a in json.loads(path.read_text(encoding="utf-8"))}
    todo = [r for r in rows if r["id"] not in saved or saved[r["id"]]["answer"].startswith("ERROR")]
    print(f"Agent: {len(saved) - sum(1 for r in todo if r['id'] in saved)} answers reused, {len(todo)} to ask.")
    if todo:
        semaphore = asyncio.Semaphore(CONCURRENCY)
        async with AsyncExitStack() as stack:
            agent = build_agent(await load_mcp_tools(stack), approval="deny")
            for answer in await asyncio.gather(*(run_one(agent, r, semaphore) for r in todo)):
                saved[answer["id"]] = answer
    answers = [saved[r["id"]] for r in rows]
    path.write_text(json.dumps(answers, indent=2, ensure_ascii=False), encoding="utf-8")
    with open(EVAL / "answers_for_grading.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.writer(f)
        w.writerow(["id", "kind", "question", "reference_answer", "agent_answer"])
        for r, a in zip(rows, answers):
            w.writerow([r["id"], r["kind"], r["question"], r["reference_answer"], a["answer"]])
    return answers


def is_judge_error(verdict):
    return verdict["reasoning"].startswith("JUDGE ERROR")


def cached_verdicts(redo):
    """Verdicts from an earlier run that worked, so a re-run only judges what failed."""
    path = EVAL / "judge_verdicts.json"
    if redo or not path.exists():
        return {}
    old = json.loads(path.read_text(encoding="utf-8"))
    return {f["id"]: f["verdict"] for f in old if not is_judge_error(f["verdict"])}


async def judge_all(rows, answers, redo=False, judge_model=JUDGE_MODEL):
    judge = ChatGoogleGenerativeAI(model=judge_model, temperature=0, google_api_key=load_api_key()).with_structured_output(Verdict)
    semaphore = asyncio.Semaphore(JUDGE_CONCURRENCY)
    cache = cached_verdicts(redo)
    print(f"Judge ({judge_model}): {len(cache)} verdicts reused, {len(rows) - len(cache)} to judge.")

    async def one(row, answer):
        if row["id"] in cache:
            return cache[row["id"]]
        async with semaphore:
            prompt = JUDGE_PROMPT.format(rubric=JUDGE_RUBRIC, question=row["question"], kind=row["kind"],
                                         reference=row["reference_answer"],
                                         trace="\n".join(answer["trace"]) or "(no tool calls)", answer=answer["answer"])
            last = ""
            for attempt in range(1, 6):
                try:
                    verdict = (await judge.ainvoke(prompt)).model_dump()
                    print(f"  judged {row['id']}", flush=True)
                    return verdict
                except Exception as error:  # noqa: BLE001
                    last = f"{type(error).__name__}: {str(error)[:150]}"
                    await asyncio.sleep(20 * attempt)  # wait longer each time: quota resets per minute
            print(f"  judge FAILED {row['id']}", flush=True)
            return {"reasoning": f"JUDGE ERROR {last}", "correct": False, "supported": False, "refused": False}

    return await asyncio.gather(*(one(r, a) for r, a in zip(rows, answers)))


def outcome(kind, verdict):
    """One label per question, computed in code from the judge's three booleans."""
    if is_judge_error(verdict):
        return "judge_error"
    if kind == "unanswerable":
        return "correct_refusal" if verdict["refused"] else "hallucination"
    if verdict["refused"]:
        return "wrong_refusal"
    if not verdict["supported"]:
        return "unsupported_claim"
    return "correct" if verdict["correct"] else "wrong_answer"


GOOD = {"correct", "correct_refusal"}


def agreement(rows, finals):
    path = EVAL / "human_labels.csv"
    if not path.exists():
        return None
    labels = [r for r in csv.DictReader(open(path, encoding="utf-8", newline="")) if r.get("correct") in ("0", "1")]
    if not labels:
        return None
    by_id = {r["id"]: f for r, f in zip(rows, finals)}
    same_correct = same_supported = 0
    disagreements = []
    for label in labels:
        final = by_id.get(label["id"])
        if final is None:
            continue
        if final["outcome"] == "judge_error":
            continue
        judge_correct = final["outcome"] in GOOD
        agree_c = (label["correct"] == "1") == judge_correct
        agree_s = (label.get("supported", "") == "1") == final["verdict"]["supported"]
        same_correct += agree_c
        same_supported += agree_s
        if not agree_c or not agree_s:
            disagreements.append(label["id"])
    n = len([l for l in labels if by_id.get(l["id"]) and by_id[l["id"]]["outcome"] != "judge_error"])
    return {"graded": n, "agree_correct": f"{same_correct}/{n}", "agree_supported": f"{same_supported}/{n}",
            "disagreements": disagreements}


def main(argv):
    redo = "--redo" in argv
    EVAL.mkdir(exist_ok=True)
    # 1. retrieval
    results, details = retrieval_eval()
    (EVAL / "retrieval_results.json").write_text(json.dumps(results, indent=2), encoding="utf-8")
    with open(EVAL / "retrieval_details.csv", "w", encoding="utf-8", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(details[0])); w.writeheader(); w.writerows(details)
    print(f"{'design':<8} {'chunks':>6} " + " ".join(f"hit@{k:<3}" for k in KS) + "  multi_full@1/3/5")
    for d, r in results.items():
        print(f"{d:<8} {r['chunks']:>6} " + " ".join(f"{r[f'hit@{k}']:<6.2f}" for k in KS)
              + f"  {r['multi_full@1']} {r['multi_full@3']} {r['multi_full@5']}")
    print(f"(the agent uses design: {index.ACTIVE_DESIGN})\n")

    # 2. agent answers
    rows = load_questions()
    answers = asyncio.run(collect_answers(rows, redo))
    if "--answers-only" in argv:
        print("\nAnswers saved. Grade 20+ in eval/human_labels.csv (use eval/answers_for_grading.csv), "
              "BEFORE running the full evaluation.")
        return

    # 3 + 4. code checks and judge
    judge_model = next((a.split("=", 1)[1] for a in argv if a.startswith("--judge-model=")), JUDGE_MODEL)
    verdicts = asyncio.run(judge_all(rows, answers, redo, judge_model))
    finals = []
    for row, answer, verdict in zip(rows, answers, verdicts):
        finals.append({"id": row["id"], "kind": row["kind"], "question": row["question"],
                       "answer": answer["answer"], "seconds": answer["seconds"], "tokens": answer["tokens"],
                       "checks": code_checks(row, answer["answer"], answer["trace"]),
                       "verdict": verdict, "outcome": outcome(row["kind"], verdict)})
    (EVAL / "judge_verdicts.json").write_text(json.dumps(finals, indent=2, ensure_ascii=False), encoding="utf-8")

    # summary
    print("\nOutcome per question kind:")
    for kind in ("single", "multi", "unanswerable"):
        group = [f for f in finals if f["kind"] == kind and f["outcome"] != "judge_error"]
        counts = {}
        for f in group:
            counts[f["outcome"]] = counts.get(f["outcome"], 0) + 1
        print(f"  {kind:<13} n={len(group):<3} {counts}")
    judge_errors = [f["id"] for f in finals if f["outcome"] == "judge_error"]
    if judge_errors:
        print(f"\nWARNING: the judge failed on {judge_errors} (quota). They are NOT counted below; run again later.")
    finals_ok = [f for f in finals if f["outcome"] != "judge_error"]
    answerable = [f for f in finals_ok if f["kind"] != "unanswerable"]
    unanswerable = [f for f in finals_ok if f["kind"] == "unanswerable"]
    summary = {
        "correct_answerable": f"{sum(f['outcome'] == 'correct' for f in answerable)}/{len(answerable)}",
        "correct_refusals": f"{sum(f['outcome'] == 'correct_refusal' for f in unanswerable)}/{len(unanswerable)}",
        "judge_errors": judge_errors,
        "unsupported_or_hallucinated": sum(f["outcome"] in ("unsupported_claim", "hallucination") for f in finals_ok),
        "citations_valid": f"{sum(f['checks']['citations_valid'] for f in finals)}/{len(finals)}",
        "searched_before_answering": f"{sum(f['checks']['searched'] for f in finals)}/{len(finals)}",
        "tried_add_document": sum(f["checks"]["tried_add_document"] for f in finals),
        "avg_seconds": round(sum(f["seconds"] for f in finals) / len(finals), 1),
        "avg_tokens": round(sum(f["tokens"] for f in finals) / len(finals)),
        "judge_vs_code_refusal_mismatch": [f["id"] for f in finals if f["verdict"]["refused"] != f["checks"]["refusal_words"]],
        "judge_vs_you": agreement(rows, finals),
        "retrieval": results,
    }
    (EVAL / "results.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print("\nSummary:")
    for key, value in summary.items():
        if key != "retrieval":
            print(f"  {key}: {value}")
    print("\nNot good (look at each by hand):")
    for f in finals:
        if f["outcome"] not in GOOD and f["outcome"] != "judge_error":
            print(f"  {f['id']} {f['outcome']:<18} {f['question'][:70]}")
            print(f"       judge: {f['verdict']['reasoning'][:200]}")
    print("\nSaved eval/answers.json, eval/judge_verdicts.json, eval/results.json")


if __name__ == "__main__":
    main(sys.argv[1:])