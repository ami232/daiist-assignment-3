"""
Assignment 3: evaluation (`main.py evaluate`). Everything it writes goes to eval/.

1. Retrieval: hit rate at k = 1, 3, 5 for each chunking design in index.DESIGNS.
   A chunk is a hit when it comes from the expected law and contains the expected
   article (or, for text before the first article, starts on the expected page).
2. Answers: the agent answers every question (answers.jsonl, reused on later runs).
   to_grade.csv lists them for your own grading, without the judge's verdicts.
3. Code checks: refusal sentence, partial-answer line, guardrail, expected passage
   retrieved. An exact refusal is graded in code; everything else goes to the judge.
4. LLM judge: eval/judge_rubric.md + question + reference + retrieved text + answer
   -> correct (0/1), supported (0/1), reason  (judgements.jsonl, reused).
5. Agreement between the judge and eval/human_labels.csv; results.csv; summary.json.

Unanswerable questions (decision 2B): correct if the agent refuses, or if it answers
only what the corpus covers, marks the rest with "Parte no cubierta por el corpus:"
and the judge finds every claim supported.
"""

from __future__ import annotations

import asyncio
import csv
import hashlib
import json
import re
import statistics
from pathlib import Path

import agent
import index
import retrieval

ROOT = Path(__file__).resolve().parent
EVAL_DIR = ROOT / "eval"
ANSWERS, JUDGEMENTS = EVAL_DIR / "answers.jsonl", EVAL_DIR / "judgements.jsonl"
RUBRIC = EVAL_DIR / "judge_rubric.md"
# Not the agent's model, so it does not grade itself. (gemini-3-flash-preview, the first choice,
# allows only 20 requests a day on the free tier.)
JUDGE_MODEL = "gemma-4-31b-it"
JUDGE_PARALLEL = 4  # judge calls at a time: the judge is slow (~1 min per answer)
KS = (1, 3, 5)


def read_questions() -> list[dict]:
    with (EVAL_DIR / "questions.csv").open(newline="", encoding="utf-8") as f:
        return [row for row in csv.DictReader(f) if row["question"].strip()]


def is_unanswerable(question: dict) -> bool:
    return question["kind"].strip().lower() == "unanswerable"


# ---------------------------------------------------------------------------
# 1. Retrieval
# ---------------------------------------------------------------------------

def expected_passages(row: dict) -> list[tuple[str, str]]:
    """("LAU", "Artículo 36") pairs; one source may serve several locations."""
    sources = [s.strip() for s in row["expected_source"].split(";")]
    locations = [loc.strip() for loc in row["expected_location"].split(";")]
    if len(sources) == 1:
        sources = sources * len(locations)
    return list(zip(sources, locations))


def matches(chunk: dict, source: str, location: str) -> bool:
    """Same law, and the expected article is one of the articles in the chunk."""
    if chunk["source"] != source:
        return False
    articles = [a for a in chunk.get("articles", "").split(" | ") if a]
    return location in articles or (not articles and chunk["location"].endswith(location))


def hit_at_k(chunks: list[dict], expected: list[tuple[str, str]], k: int) -> bool:
    """At least one expected passage is among the first k chunks."""
    return any(matches(c, s, loc) for c in chunks[:k] for s, loc in expected)


def evaluate_retrieval(questions: list[dict]) -> dict:
    """Hit rate at each k per design, over the answerable questions."""
    answerable = [q for q in questions if not is_unanswerable(q)]
    results = {}
    for design in index.DESIGNS:
        rows, words = [], []
        for q in answerable:
            chunks = retrieval.search(q["question"], design=design, k=max(KS))
            rows.append({k: hit_at_k(chunks, expected_passages(q), k) for k in KS})
            words.append(sum(len(c["text"].split()) for c in chunks))
        results[design] = {f"hit@{k}": round(sum(r[k] for r in rows) / len(rows), 3) for k in KS}
        results[design]["avg_words_added_to_prompt"] = round(sum(words) / len(words))
        print(f"  {design:10s} " + "  ".join(f"hit@{k} {results[design][f'hit@{k}']:.2f}" for k in KS)
              + f"  ({results[design]['avg_words_added_to_prompt']} words in the prompt)")
    return results


# ---------------------------------------------------------------------------
# 2. Answers (cached: a question already answered is not asked again)
# ---------------------------------------------------------------------------

def read_jsonl(path: Path) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()] if path.exists() else []


def append_jsonl(path: Path, row: dict) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def config_signature() -> str:
    """What the answers depend on: chunking design, chat model and AGENTS.md."""
    rules = hashlib.sha1((ROOT / "AGENTS.md").read_bytes()).hexdigest()[:8]
    return f"{index.CHOSEN_DESIGN}|{agent.MODEL}|{rules}"


def needs_answer(question: dict, rec: dict | None) -> bool:
    """Ask again if never asked, or if the question or the configuration changed."""
    return rec is None or rec["question"] != question["question"] or rec.get("config") != config_signature()


def error_text(error: BaseException) -> str:
    """The message of an error, including errors wrapped in an ExceptionGroup."""
    if isinstance(error, BaseExceptionGroup):
        return " ".join(error_text(e) for e in error.exceptions)
    return f"{type(error).__name__}: {error}"


async def with_retry(call, attempts: int = 4, wait: int = 60, sleep=asyncio.sleep):
    """Run `call()`, retrying while Gemini is briefly busy (503, or 429 per minute).

    The daily free-tier quota does not come back by waiting, so that stops at once;
    every answer and verdict so far is already saved, and the next run resumes.
    """
    for attempt in range(1, attempts + 1):
        try:
            return await call()
        except Exception as error:  # noqa: BLE001 - classified below, re-raised if not transient
            text = error_text(error)
            if "PerDay" in text:
                raise SystemExit("Daily Gemini quota used up. Progress is saved: run "
                                 "`main.py evaluate` again tomorrow to continue.") from error
            busy = any(code in text for code in ("503", "UNAVAILABLE", "429", "RESOURCE_EXHAUSTED"))
            if not busy or attempt == attempts:
                raise
            print(f"  Gemini is busy, waiting {wait * attempt}s before retrying ...")
            await sleep(wait * attempt)


async def answer_all(questions: list[dict]) -> dict[str, dict]:
    answers = {r["id"]: r for r in read_jsonl(ANSWERS)}  # the last line per id wins
    todo = [q for q in questions if needs_answer(q, answers.get(q["id"]))]
    if todo:
        async with agent.mcp_tools() as tools:
            graph = agent.build_agent(tools)
            for n, q in enumerate(todo, start=1):
                rec = await with_retry(lambda: agent.ask(q["question"], graph, approve=lambda action: False))  # never add documents
                rec.update(id=q["id"], question=q["question"], config=config_signature())
                append_jsonl(ANSWERS, rec)
                answers[q["id"]] = rec
                print(f"  [{n}/{len(todo)}] {q['id']} answered in {rec['seconds']}s")
    return answers


def write_to_grade(questions: list[dict], answers: dict[str, dict]) -> None:
    """What you grade yourself, before looking at the judge (no verdicts here)."""
    with (EVAL_DIR / "to_grade.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "kind", "question", "reference_answer", "answer", "retrieved"])
        for q in questions:
            a = answers[q["id"]]
            w.writerow([q["id"], q["kind"], q["question"], q["reference_answer"], a["answer"], a["retrieved"]])


# ---------------------------------------------------------------------------
# 3. Code checks
# ---------------------------------------------------------------------------

def passage_retrieved(source: str, location: str, retrieved: str) -> bool:
    """The expected article appears in a search result from the expected law
    (in its header "[LAU, Artículo 36, p. 25]" or as a heading "Artículo 36." inside it)."""
    for block in re.split(r"(?=Result \d+ \[)", retrieved):
        header = re.match(r"Result \d+ \[([^,\]]+),", block)
        if header and header.group(1) == source and re.search(rf"{re.escape(location)}[.,]", block):
            return True
    return False


def code_checks(question: dict, rec: dict) -> dict:
    expected = None if is_unanswerable(question) else any(
        passage_retrieved(s, loc, rec["retrieved"]) for s, loc in expected_passages(question))
    return {
        "refused": rec["answer"].strip() == agent.REFUSAL,
        "partial": agent.PARTIAL_PREFIX in rec["answer"],
        "guardrail_fired": bool(rec["guardrail"]),
        "searched": any(c["name"] == "search" for c in rec["tool_calls"]),
        "expected_retrieved": expected,
    }


def refusal_verdict(question: dict) -> dict:
    """An exact refusal needs no judge: right if unanswerable, wrong otherwise."""
    return {"correct": int(is_unanswerable(question)), "supported": 1, "reason": "refusal (code check)"}


# ---------------------------------------------------------------------------
# 4. LLM judge (cached per question, answer and rubric)
# ---------------------------------------------------------------------------

def judge_model():
    """The judge's chat model. It loads the API key itself: when every answer is
    cached, the agent never runs and nothing else would load it."""
    from langchain_google_genai import ChatGoogleGenerativeAI

    from api_key import load_api_key

    load_api_key()
    return ChatGoogleGenerativeAI(model=JUDGE_MODEL, temperature=0, max_retries=2)  # with_retry handles the rest


async def judge(question: dict, rec: dict, rubric: str) -> dict:
    from pydantic import BaseModel, Field

    class Verdict(BaseModel):
        correct: int = Field(description="1 if the answer is right against the reference, else 0")
        supported: int = Field(description="1 if every claim is in the retrieved passages, else 0")
        reason: str = Field(description="one sentence explaining the grades")

    answer = rec["answer"].replace(agent.DISCLAIMER, "").strip()  # the fixed disclaimer is not a claim
    prompt = (f"{rubric}\n\n## Question ({question['kind']})\n{question['question']}\n\n"
              f"## Reference answer\n{question['reference_answer']}\n\n"
              f"## Retrieved passages (the only evidence)\n{rec['retrieved'] or '(none)'}\n\n"
              f"## Answer to grade\n{answer}")
    model = judge_model()
    verdict = await model.with_structured_output(Verdict).ainvoke(prompt)
    return {"correct": int(verdict.correct), "supported": int(verdict.supported), "reason": verdict.reason}


async def run_limited(calls: list, limit: int) -> list:
    """Await every call, at most `limit` at a time; results keep the calls' order."""
    gate = asyncio.Semaphore(limit)

    async def one(call):
        async with gate:
            return await call()

    return await asyncio.gather(*(one(c) for c in calls))


async def judge_all(questions: list[dict], answers: dict, checks: dict) -> dict[str, dict]:
    if not RUBRIC.exists():
        print("  eval/judge_rubric.md is missing: only refusals are graded (in code).")
        return {q["id"]: refusal_verdict(q) for q in questions if checks[q["id"]]["refused"]}
    rubric = RUBRIC.read_text(encoding="utf-8")
    rubric_hash = hashlib.sha1((JUDGE_MODEL + rubric).encode()).hexdigest()[:8]  # new judge or rubric -> judge again
    cached = {(r["id"], r["answer"], r["rubric"]): r["verdict"] for r in read_jsonl(JUDGEMENTS)}
    verdicts, todo = {}, []
    for q in questions:
        rec = answers[q["id"]]
        key = (q["id"], rec["answer"], rubric_hash)
        if checks[q["id"]]["refused"]:
            verdicts[q["id"]] = refusal_verdict(q)
        elif key in cached:
            verdicts[q["id"]] = cached[key]
        else:
            todo.append((q, rec))

    def judge_one(q: dict, rec: dict):
        async def call():
            verdict = await with_retry(lambda: judge(q, rec, rubric), attempts=6)  # Gemma is often busy (503)
            append_jsonl(JUDGEMENTS, {"id": q["id"], "answer": rec["answer"], "rubric": rubric_hash, "verdict": verdict})
            print(f"  judged {q['id']}", flush=True)
            return verdict
        return call

    results = await run_limited([judge_one(q, rec) for q, rec in todo], limit=JUDGE_PARALLEL)
    verdicts.update({q["id"]: v for (q, _), v in zip(todo, results)})
    return verdicts


# ---------------------------------------------------------------------------
# 5. Outcomes, failure causes, agreement, summary
# ---------------------------------------------------------------------------

def outcome(question: dict, checks: dict, verdict: dict) -> str:
    if is_unanswerable(question):
        if checks["refused"]:
            return "correct refusal"
        if checks["partial"] and verdict.get("supported") == 1:
            return "correct partial"
        return "answered unanswerable"
    if checks["refused"]:
        return "wrong refusal"
    if not verdict:
        return "not judged"
    if verdict["supported"] == 0:
        return "unsupported"
    return "correct" if verdict["correct"] == 1 else "incorrect"


def suggested_cause(result: str, checks: dict) -> str | None:
    """A first guess at the failure cause; you confirm it (or say "bad test question")."""
    if result in {"correct", "correct refusal", "correct partial", "not judged"}:
        return None
    if result in {"unsupported", "answered unanswerable"}:
        return "unsupported claim"
    if not checks["expected_retrieved"]:
        return "retrieval miss"
    return "wrong refusal" if result == "wrong refusal" else "wrong answer from right passage"


def read_human_labels() -> dict[str, dict]:
    path = EVAL_DIR / "human_labels.csv"
    with path.open(newline="", encoding="utf-8") as f:
        return {r["id"].strip(): r for r in csv.DictReader(f) if (r.get("id") or "").strip()}


def agreement(judge_verdicts: dict, human: dict) -> dict:
    both = [i for i in human if i in judge_verdicts]
    if not both:
        return {"n": 0}
    share = lambda field: round(sum(int(human[i][field]) == judge_verdicts[i][field] for i in both) / len(both), 3)  # noqa: E731
    return {"n": len(both), "correct": share("correct"), "supported": share("supported")}


def main(retrieval_only: bool = False) -> None:
    questions = read_questions()
    print(f"1. Retrieval over {len(questions)} questions")
    summary = {"models": {"agent": agent.MODEL, "judge": JUDGE_MODEL, "design": index.CHOSEN_DESIGN},
               "retrieval": evaluate_retrieval(questions)}
    if retrieval_only:  # `python evaluate.py --retrieval-only`: compare designs before choosing one
        (EVAL_DIR / "retrieval.json").write_text(json.dumps(summary["retrieval"], indent=2))
        return

    print(f"2. Agent answers (model {agent.MODEL})")
    answers = asyncio.run(answer_all(questions))
    write_to_grade(questions, answers)

    print("3-4. Code checks and judge")
    checks = {q["id"]: code_checks(q, answers[q["id"]]) for q in questions}
    verdicts = asyncio.run(judge_all(questions, answers, checks))

    rows = []
    for q in questions:
        a, c, v = answers[q["id"]], checks[q["id"]], verdicts.get(q["id"], {})
        result = outcome(q, c, v)
        rows.append({"id": q["id"], "kind": q["kind"], "outcome": result, "suggested_cause": suggested_cause(result, c),
                     **c, "judge_correct": v.get("correct"), "judge_supported": v.get("supported"),
                     "judge_reason": v.get("reason"), "guardrail": a["guardrail"],
                     "input_tokens": a["input_tokens"], "output_tokens": a["output_tokens"],
                     "model_calls": a["model_calls"], "seconds": a["seconds"]})
    with (EVAL_DIR / "results.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    outcomes = [r["outcome"] for r in rows]
    summary["outcomes"] = {o: outcomes.count(o) for o in sorted(set(outcomes))}
    summary["guardrail_fired"] = sum(r["guardrail_fired"] for r in rows)
    summary["suggested_causes"] = {c: [r["id"] for r in rows if r["suggested_cause"] == c]
                                   for c in sorted({r["suggested_cause"] for r in rows if r["suggested_cause"]})}
    summary["cost_per_question"] = {
        "tokens_mean": round(statistics.mean(r["input_tokens"] + r["output_tokens"] for r in rows)),
        "seconds_mean": round(statistics.mean(r["seconds"] for r in rows), 1),
        "model_calls_mean": round(statistics.mean(r["model_calls"] for r in rows), 1),
    }
    summary["judge_vs_human"] = agreement(verdicts, read_human_labels())
    (EVAL_DIR / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    print("5. Summary")
    print(json.dumps({k: v for k, v in summary.items() if k != "retrieval"}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    import sys

    main(retrieval_only="--retrieval-only" in sys.argv)
