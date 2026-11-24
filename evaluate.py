"""
Assignment 3: evaluation (`main.py evaluate`).

1. Retrieval: hit rate at k = 1, 3, 5 for two chunking designs (250 and 400
   words). A question is a hit if the top k chunks cover every
   (company, section) in its expected_source / expected_location.
2. Agent: run agent.py's agent on every question.
3. Code checks: refusals, citations (invalid ones are withheld by agent.py).
4. LLM judge with a rubric, the tool trace as evidence, and a stronger model
   than the agent's.
5. Agreement with eval/human_labels.csv, if you have filled it in.

Writes eval/results.json and eval/answers_to_grade.csv (answers without the
judge's verdicts, so you can grade them blind).
"""

import asyncio
import csv
import json
import statistics
import time
import warnings
from contextlib import AsyncExitStack
from pathlib import Path

warnings.filterwarnings("ignore")

import chromadb
from langchain_core.messages import AIMessage
from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

import agent as agent_mod
import index
from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
HUMAN = EVAL / "human_labels.csv"
RESULTS = EVAL / "results.json"
TO_GRADE = EVAL / "answers_to_grade.csv"
QUERY_CACHE = EVAL / "query_vectors.json"

DESIGNS = [250, 400]  # chunk size in words; overlap is one fifth
KS = (1, 3, 5)
JUDGE_MODEL = "gemini-3.5-flash"  # stronger than the agent's flash-lite
REFUSAL = "the corpus does not cover this"


# ---------- questions ----------

def read_questions():
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r["question"].strip()]


def is_unanswerable(row):
    return row["kind"].strip().lower() == "unanswerable"


def expected_pairs(row):
    sources = [s.strip() for s in row["expected_source"].split(";") if s.strip()]
    sections = [s.strip() for s in row["expected_location"].split(";") if s.strip()]
    return list(zip(sources, sections))


# ---------- 1. retrieval ----------

def query_vectors(questions):
    """Embed each question once and keep the vector, so reruns cost nothing."""
    cache = json.loads(QUERY_CACHE.read_text()) if QUERY_CACHE.exists() else {}
    missing = [q for q in questions if q not in cache]
    if missing:
        client = index.get_client()
        for start in range(0, len(missing), 20):
            batch = missing[start:start + 20]
            vectors = index.embed_texts(client, [index.query_text(q) for q in batch])
            cache.update(dict(zip(batch, vectors)))
            QUERY_CACHE.write_text(json.dumps(cache))
    return cache


def design_collection(size):
    db = chromadb.PersistentClient(path=str(index.INDEX_DIR))
    return db.get_or_create_collection(
        name=f"tenk_w{size}", configuration={"hnsw": {"space": "cosine"}}, embedding_function=None)


def ensure_design(size):
    """Build the index for this chunk size if it is missing (only new chunks are embedded)."""
    collection = design_collection(size)
    for ticker in index.CORPUS:
        chunks = index.chunk_file(index.download(ticker), ticker, size=size)
        index.embed_and_store(chunks, collection)
    return collection


def retrieval_eval(rows, vectors):
    answerable = [r for r in rows if not is_unanswerable(r)]
    report = {}
    for size in DESIGNS:
        collection = ensure_design(size)
        hits = {k: [] for k in KS}
        words, misses = [], []
        for r in answerable:
            res = collection.query(query_embeddings=[vectors[r["question"]]], n_results=max(KS))
            metas, docs = res["metadatas"][0], res["documents"][0]
            words.append(sum(len(d.split()) for d in docs[:3]))
            for k in KS:
                got = {(m["ticker"], m["section"]) for m in metas[:k]}
                hits[k].append(all(p in got for p in expected_pairs(r)))
            if not hits[5][-1]:
                misses.append(r["id"])
        report[size] = {
            "chunks": collection.count(),
            "questions": len(answerable),
            "hit_rate": {k: round(statistics.mean(hits[k]), 3) for k in KS},
            "avg_words_top3": round(statistics.mean(words)),
            "misses_at_5": misses,
        }
    return report


# ---------- 2-3. agent and code checks ----------

def code_checks(row, answer, trace):
    refused = REFUSAL in answer.lower()
    withheld = answer.startswith("Answer withheld")
    n_citations = len(agent_mod.CITED.findall(answer))
    searched = any(line.startswith("call search") for line in trace)
    if is_unanswerable(row):
        ok = refused
    else:  # invalid citations were withheld by agent.py, so a kept answer has valid ones
        ok = (not refused) and (not withheld) and n_citations > 0 and searched
    pairs = expected_pairs(row)
    got = {(t, s) for t, s, _ in agent_mod.retrieved_citations(trace)}
    return {
        "refused": refused, "withheld": withheld, "n_citations": n_citations,
        "searched": searched, "code_ok": ok,
        "retrieved_expected": (all(p in got for p in pairs) if pairs else None),
    }


async def run_agent(rows):
    results = []
    async with AsyncExitStack() as stack:
        agent = agent_mod.build_agent(await agent_mod.load_mcp_tools(stack), auto_approve=True)
        for n, row in enumerate(rows, start=1):
            result, error, seconds = None, None, 0.0
            for attempt in range(2):
                try:
                    started = time.perf_counter()
                    result = await agent.ainvoke({"messages": [{"role": "user", "content": row["question"]}]})
                    seconds = time.perf_counter() - started
                    break
                except Exception as e:  # noqa: BLE001
                    error = str(e)[:200]
                    if attempt == 0:
                        await asyncio.sleep(60)  # most likely a rate limit
            if result is None:
                answer, trace, tokens = "", [], 0
            else:
                messages = result["messages"]
                trace = agent_mod.tool_trace(messages)
                answer = agent_mod.apply_guardrail(messages[-1].text, trace)
                tokens = sum((m.usage_metadata or {}).get("total_tokens", 0)
                             for m in messages if isinstance(m, AIMessage))
            results.append({**row, "answer": answer, "trace": trace, "seconds": round(seconds, 1),
                            "tokens": tokens, "error": error, **code_checks(row, answer, trace)})
            print(f"  [{n}/{len(rows)}] {row['id']}  {seconds:.1f}s  code_ok={results[-1]['code_ok']}", flush=True)
    return results


# ---------- 4. judge ----------

class Verdict(BaseModel):
    reasoning: str = Field(description="Two or three sentences checking the answer against each criterion.")
    grounded: bool = Field(description="True only if every fact and number in the answer appears in the retrieved passages of the trace.")
    correct: bool = Field(description="True only if the answer matches the reference answer (or, for an unanswerable question, correctly says the corpus does not cover it).")
    passed: bool = Field(description="True only if grounded and correct.")


JUDGE_PROMPT = """You are grading an assistant that answers questions about the 10-K annual reports of Ralph Lauren, PVH and Tapestry, using a search tool. The tool trace shows what really happened.

Criteria:
1. Grounded: every fact, figure and date in the answer appears in a retrieved passage in the trace. Anything not in the trace is a guess and fails. A refusal ("The corpus does not cover this.") is grounded.
2. Correct: the answer contains the key facts and numbers of the reference answer. Extra correct detail is fine. A wrong or missing key figure fails. If the question is unanswerable, the answer is correct only if it says the corpus does not cover it and gives no figure or guess.
3. Passed: grounded and correct.

Kind of question: {kind}
Question: {question}
Reference answer: {reference}
Tool trace:
{trace}
Assistant's answer:
{answer}"""


async def judge_all(results, save=lambda: None):
    judge = ChatGoogleGenerativeAI(model=JUDGE_MODEL, temperature=0).with_structured_output(Verdict)
    for n, r in enumerate(results, start=1):
        if r.get("passed") is not None:
            continue  # already judged in an earlier run
        prompt = JUDGE_PROMPT.format(
            kind=r["kind"], question=r["question"], reference=r["reference_answer"],
            trace="\n".join(r["trace"]) or "(no tool calls)", answer=r["answer"] or "(no answer)")
        verdict = None
        for attempt in range(4):
            try:
                verdict = await judge.ainvoke(prompt)
                r.pop("judge_error", None)
                break
            except Exception as e:  # noqa: BLE001
                r["judge_error"] = str(e)[:300]
                print(f"    judge error on {r['id']} (try {attempt + 1}/4): {r['judge_error'][:150]}", flush=True)
                await asyncio.sleep(45)  # most likely the free tier's requests-per-minute limit
        r.update(verdict.model_dump() if verdict else {"reasoning": "", "grounded": None, "correct": None, "passed": None})
        r["suggested_cause"] = suggested_cause(r)
        print(f"  judge [{n}/{len(results)}] {r['id']}  passed={r['passed']}", flush=True)
        save()  # keep progress if the run is interrupted
        await asyncio.sleep(7)  # stay under the free tier's requests per minute


def suggested_cause(r):
    """A first guess to help your own classification of failures. You decide."""
    if r.get("passed") and r["code_ok"]:
        return None
    if is_unanswerable(r):
        return "unsupported claim (answered an unanswerable question)" if not r["refused"] else "check manually"
    if r["refused"]:
        return "wrong refusal" + (" (retrieval miss?)" if r["retrieved_expected"] is False else "")
    if r["retrieved_expected"] is False:
        return "retrieval miss"
    if r.get("grounded") is False:
        return "unsupported claim"
    if r.get("correct") is False:
        return "wrong answer from the right passage"
    return "check manually (code check failed or judge error)"


# ---------- 5. agreement with your grades ----------

def human_agreement(results):
    """Your grades (correct, supported) against the judge's (correct, grounded, passed)."""
    if not HUMAN.exists():
        return None
    with HUMAN.open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if (r.get("id") or "").strip()]
    if not rows:
        return None
    by_id = {r["id"]: r for r in results}

    def flag(value):
        value = (value or "").strip().lower()
        return True if value in {"1", "true", "yes", "y"} else False if value in {"0", "false", "no", "n"} else None

    pairs = {"correct": [], "supported": [], "passed": []}
    disagreements = []
    for row in rows:
        r = by_id.get(row["id"].strip())
        mine_c, mine_s = flag(row.get("correct")), flag(row.get("supported"))
        if r is None or mine_c is None or mine_s is None or r.get("passed") is None:
            continue
        pairs["correct"].append((mine_c, r["correct"]))
        pairs["supported"].append((mine_s, r["grounded"]))
        pairs["passed"].append((mine_c and mine_s, r["passed"]))
        if (mine_c and mine_s) != r["passed"]:
            disagreements.append(row["id"].strip())
    report = {"compared": len(pairs["passed"]), "disagreements": disagreements}
    for name, items in pairs.items():
        report[f"agreement_{name}"] = round(sum(a == b for a, b in items) / len(items), 3) if items else None
    return report


# ---------- main ----------

def summarise(results):
    answerable = [r for r in results if not is_unanswerable(r)]
    unanswerable = [r for r in results if is_unanswerable(r)]
    return {
        "questions": len(results),
        "code_ok": sum(r["code_ok"] for r in results),
        "judge_passed": sum(bool(r.get("passed")) for r in results),
        "correct": sum(bool(r.get("passed")) for r in answerable),
        "answerable": len(answerable),
        "unsupported": sum(r.get("grounded") is False for r in results),
        "correct_refusals": sum(r["refused"] for r in unanswerable),
        "unanswerable": len(unanswerable),
        "wrong_refusals": sum(r["refused"] for r in answerable),
        "avg_seconds": round(statistics.mean(r["seconds"] for r in results), 1),
        "avg_tokens": round(statistics.mean(r["tokens"] for r in results)),
    }


async def amain():
    load_api_key()
    rows = read_questions()

    print("1/4 Retrieval (builds the second index the first time, ~330 embeddings)")
    vectors = query_vectors([r["question"] for r in rows if not is_unanswerable(r)])
    retrieval = retrieval_eval(rows, vectors)
    for size, rep in retrieval.items():
        print(f"  {size}-word chunks: {rep['chunks']} chunks, hit rate "
              + ", ".join(f"@{k} {rep['hit_rate'][k]:.0%}" for k in KS)
              + f", {rep['avg_words_top3']} words in the prompt (top 3), misses at 5: {rep['misses_at_5']}")

    previous = json.loads(RESULTS.read_text()) if RESULTS.exists() else None
    if previous and len(previous.get("results", [])) == len(rows):
        print("\n2/4 Reusing the agent's answers from eval/results.json (delete that file to run the agent again)")
        results = previous["results"]
    else:
        print("\n2/4 Running the agent on every question")
        results = await run_agent(rows)

    def save():
        RESULTS.write_text(json.dumps({"retrieval": retrieval, "results": results},
                                      indent=2, ensure_ascii=False))
    save()  # the agent's answers are never lost again

    with TO_GRADE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "question", "kind", "reference_answer", "answer"])
        for r in results:
            writer.writerow([r["id"], r["question"], r["kind"], r["reference_answer"], r["answer"]])

    print("\n3/4 Judging")
    await judge_all(results, save)

    print("\n4/4 Agreement with your grades")
    agreement = human_agreement(results)
    summary = summarise(results)
    RESULTS.write_text(json.dumps(
        {"retrieval": retrieval, "summary": summary, "agreement": agreement, "results": results},
        indent=2, ensure_ascii=False))

    print("\n" + "=" * 60)
    for key, value in summary.items():
        print(f"  {key}: {value}")
    print(f"  human agreement: {agreement}")
    print("\nFailures (suggested cause, you decide):")
    for r in results:
        if r.get("suggested_cause"):
            print(f"  {r['id']}: {r['suggested_cause']}  | {r.get('reasoning', '')[:150]}")
    print(f"\nSaved {RESULTS.relative_to(ROOT)} and {TO_GRADE.relative_to(ROOT)}")


if __name__ == "__main__":
    asyncio.run(amain())