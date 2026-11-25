"""
Assignment 3: evaluation (`main.py evaluate`).

  1. Retrieval: hit rate at k = 1, 3, 5 for each chunking design, on the
     answerable questions (query vectors are cached, so re-runs cost nothing).
  2. Agent: answers every question (saved after each one, so a stop or the
     daily limit loses nothing; run again to continue).
  3. Code checks: did it search, are the citations real, did it refuse.
  4. LLM judge with a rubric and the retrieved text as evidence, for the
     answers that are not refusals.
  5. Agreement with eval/human_labels.csv, failures, cost.

Grade yourself BEFORE you read the judge's verdicts: after step 2 the file
eval/answers_for_grading.csv has everything you need. Fill eval/human_labels.csv
(id, correct, supported, notes) from it, then look at judge_verdicts.csv.

    uv run python main.py evaluate                  # everything (continues where it stopped)
    EVAL_FRESH=1 uv run python main.py evaluate     # ignore saved answers and verdicts
    uv run python evaluate.py --demo [q32]          # add-document before/after (see demo())
"""

import asyncio
import csv
import json
import os
import re
import sys
import time
from pathlib import Path

from langchain_google_genai import ChatGoogleGenerativeAI

import agent
import index
from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
HUMAN_LABELS = EVAL / "human_labels.csv"
QUERY_CACHE = EVAL / "query_embeddings.json"
RETRIEVAL_CSV = EVAL / "retrieval_results.csv"
ANSWERS = EVAL / "answers.json"
GRADING_SHEET = EVAL / "answers_for_grading.csv"
JUDGE_JSON = EVAL / "judge_verdicts.json"
JUDGE_CSV = EVAL / "judge_verdicts.csv"
FAILURES_CSV = EVAL / "failures.csv"
SUMMARY = EVAL / "summary.json"
DEMO_JSON = EVAL / "add_document_demo.json"

KS = (1, 3, 5)
PAUSE = float(os.environ.get("EVAL_PAUSE", "8"))  # seconds between questions: the free tier allows only a few requests a minute
FRESH = os.environ.get("EVAL_FRESH") == "1"

JUDGE_RUBRIC = """You grade an answer written by a retrieval assistant. Be strict and literal.

QUESTION:
{question}

REFERENCE ANSWER (what a correct answer says; for an unanswerable question a correct answer says the corpus does not cover it):
{reference}

RETRIEVED PASSAGES (the only evidence the assistant had):
{evidence}

ASSISTANT ANSWER:
{answer}

Rubric:
- correct = 1 if the answer states the same key facts as the reference answer (wording may differ, extra correct detail is fine). correct = 0 if a key fact is missing, wrong or contradicted. For an unanswerable question, correct = 1 only if the answer says the corpus does not cover the question.
- supported = 1 if every factual claim in the answer is stated in the retrieved passages. supported = 0 if any claim is not.

Reply with JSON only, no other text: {{"correct": 0 or 1, "supported": 0 or 1, "reason": "one short sentence"}}"""


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


# ---------------------------------------------------------------------------
# Questions
# ---------------------------------------------------------------------------
def load_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if (r.get("question") or "").strip()]


def expected_pairs(row: dict) -> list[tuple[str, str]]:
    sources = [s.strip() for s in row["expected_source"].split(";") if s.strip()]
    locations = [s.strip() for s in row["expected_location"].split(";") if s.strip()]
    if len(sources) == 1 and len(locations) > 1:
        sources = sources * len(locations)
    if len(locations) == 1 and len(sources) > 1:
        locations = locations * len(sources)
    return list(zip(sources, locations))


def chunk_matches(source: str, location: str, pair: tuple[str, str]) -> bool:
    """A chunk matches if it is from the expected source and its location is the expected page, or contains the expected heading."""
    want_source, want_location = pair
    if source.lower() != want_source.lower():
        return False
    if want_location.startswith("p. "):
        return location.strip() == want_location
    return want_location.lower() in location.lower()


# ---------------------------------------------------------------------------
# 1. Retrieval
# ---------------------------------------------------------------------------
def query_vectors(questions: list[str]) -> dict[str, list[float]]:
    cache = {}
    if QUERY_CACHE.is_file() and not FRESH:
        cache = json.loads(QUERY_CACHE.read_text(encoding="utf-8"))
    missing = [q for q in questions if q not in cache]
    for i in range(0, len(missing), index.EMBED_BATCH):
        batch = missing[i : i + index.EMBED_BATCH]
        for question, vector in zip(batch, index.embed_texts(batch)):
            cache[question] = vector
        QUERY_CACHE.write_text(json.dumps(cache), encoding="utf-8")
        time.sleep(1)
    return cache


def retrieval_stage(rows: list[dict]) -> dict:
    answerable = [r for r in rows if r["kind"].strip().lower() != "unanswerable"]
    vectors = query_vectors([r["question"] for r in answerable])
    results, summary = [], {}
    for design in index.DESIGNS:
        collection = index.get_collection(design)
        per_k = {k: {"strict": 0, "source": 0} for k in KS}
        full_cover, words, multi_n = 0, 0, 0
        for row in answerable:
            found = collection.query(query_embeddings=[vectors[row["question"]]], n_results=max(KS), include=["metadatas", "documents"])
            metas, docs = found["metadatas"][0], found["documents"][0]
            pairs = expected_pairs(row)
            out = {"id": row["id"], "design": design, "kind": row["kind"]}
            for k in KS:
                top = metas[:k]
                strict = any(chunk_matches(m["source"], m["location"], p) for m in top for p in pairs)
                source_only = any(m["source"].lower() == p[0].lower() for m in top for p in pairs)
                per_k[k]["strict"] += strict
                per_k[k]["source"] += source_only
                out[f"hit@{k}"], out[f"source_hit@{k}"] = int(strict), int(source_only)
            if row["kind"].strip().lower() == "multi":
                multi_n += 1
                covered = all(any(chunk_matches(m["source"], m["location"], p) for m in metas) for p in pairs)
                full_cover += covered
                out["multi_all_pairs@5"] = int(covered)
            out["words@5"] = sum(len(d.split()) for d in docs)
            words += out["words@5"]
            results.append(out)
        n = len(answerable)
        summary[design] = {
            "questions": n,
            **{f"hit@{k}": round(per_k[k]["strict"] / n, 3) for k in KS},
            **{f"source_hit@{k}": round(per_k[k]["source"] / n, 3) for k in KS},
            "multi_all_pairs@5": f"{full_cover}/{multi_n}",
            "mean_words_added_to_prompt@5": round(words / n),
        }
    fields = sorted({key for r in results for key in r}, key=lambda s: (s not in ("id", "design", "kind"), s))
    with RETRIEVAL_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(results)
    return summary


# ---------------------------------------------------------------------------
# 2. Agent answers
# ---------------------------------------------------------------------------
def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() and not FRESH else {}


async def deny(_path: str) -> bool:  # the evaluation never adds documents
    return False


async def answers_stage(rows: list[dict]) -> dict:
    answers = load_json(ANSWERS)
    todo = [r for r in rows if r["id"] not in answers or "error" in answers[r["id"]]]
    if todo:
        log(f"asking the agent {len(todo)} question(s) ...")
        async with agent.Harness(approve=deny) as harness:
            for n, row in enumerate(todo, 1):
                try:
                    answers[row["id"]] = await harness.ask(row["question"])
                    log(f"  [{n}/{len(todo)}] {row['id']}: {answers[row['id']]['answer'][:80]!r}")
                except Exception as error:  # noqa: BLE001
                    answers[row["id"]] = {"error": f"{type(error).__name__}: {str(error)[:300]}"}
                    log(f"  [{n}/{len(todo)}] {row['id']} failed: {answers[row['id']]['error']}")
                    if "429" in str(error) or "RESOURCE_EXHAUSTED" in str(error) or "quota" in str(error).lower():
                        ANSWERS.write_text(json.dumps(answers, indent=1), encoding="utf-8")
                        log("Quota or rate limit reached. Run the same command again later; saved answers are kept.")
                        break
                ANSWERS.write_text(json.dumps(answers, indent=1), encoding="utf-8")
                time.sleep(PAUSE)
    write_grading_sheet(rows, answers)
    return answers


def write_grading_sheet(rows: list[dict], answers: dict) -> None:
    with GRADING_SHEET.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "kind", "question", "reference_answer", "agent_answer", "retrieved_passages", "correct", "supported", "notes"])
        for row in rows:
            a = answers.get(row["id"])
            if not a or "error" in a:
                continue
            passages = "\n---\n".join(f"{p['source']} | {p['location']}: {p['text']}" for p in a["retrieved"])
            writer.writerow([row["id"], row["kind"], row["question"], row["reference_answer"], a["answer"], passages, "", "", ""])


# ---------------------------------------------------------------------------
# 3 and 4. Code checks and the LLM judge
# ---------------------------------------------------------------------------
def code_checks(row: dict, a: dict) -> dict:
    searched = any(t["tool"] == "search" for t in a["tool_trace"])
    unanswerable = row["kind"].strip().lower() == "unanswerable"
    return {
        "searched": searched,
        "refused": a["refused"],
        "citations_valid": a["citations_valid"],
        "guardrail_fired": bool(a["guardrail"]),
        "expected_refusal": unanswerable,
        "refusal_ok": a["refused"] == unanswerable,
    }


def parse_judge(text: str) -> dict:
    match = re.search(r"\{.*\}", text, re.S)
    data = json.loads(match.group(0)) if match else {}
    return {"correct": int(data.get("correct", 0)), "supported": int(data.get("supported", 0)), "reason": str(data.get("reason", ""))[:300]}


def judge_stage(rows: list[dict], answers: dict) -> dict:
    verdicts = load_json(JUDGE_JSON)
    llm = None
    asked = 0
    for row in rows:
        a = answers.get(row["id"])
        if not a or "error" in a or row["id"] in verdicts:
            continue
        unanswerable = row["kind"].strip().lower() == "unanswerable"
        if a["refused"]:  # decided in code: a refusal is right exactly when the question is unanswerable
            verdicts[row["id"]] = {"correct": int(unanswerable), "supported": 1, "reason": "refusal (decided in code)", "by": "code"}
            continue
        if llm is None:
            llm = ChatGoogleGenerativeAI(model=agent.pick_model_name(), temperature=0, max_retries=6, timeout=120)
        evidence = "\n\n".join(f"[{p['source']} | {p['location']}] {p['text']}" for p in a["retrieved"]) or "(nothing was retrieved)"
        prompt = JUDGE_RUBRIC.format(question=row["question"], reference=row["reference_answer"], evidence=evidence, answer=a["answer"])
        try:
            verdicts[row["id"]] = {**parse_judge(agent.message_text(llm.invoke(prompt))), "by": "judge"}
        except Exception as error:  # noqa: BLE001
            log(f"  judge failed on {row['id']}: {type(error).__name__}: {str(error)[:150]}")
            if "429" in str(error) or "RESOURCE_EXHAUSTED" in str(error):
                break
            continue
        asked += 1
        JUDGE_JSON.write_text(json.dumps(verdicts, indent=1), encoding="utf-8")
        time.sleep(PAUSE / 2)
    JUDGE_JSON.write_text(json.dumps(verdicts, indent=1), encoding="utf-8")
    with JUDGE_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "correct", "supported", "by", "reason"])
        for row in rows:
            v = verdicts.get(row["id"])
            if v:
                writer.writerow([row["id"], v["correct"], v["supported"], v["by"], v["reason"]])
    return verdicts


# ---------------------------------------------------------------------------
# 5. Agreement, failures, cost
# ---------------------------------------------------------------------------
def agreement(verdicts: dict) -> dict:
    if not HUMAN_LABELS.is_file():
        return {"graded": 0}
    with HUMAN_LABELS.open(newline="", encoding="utf-8") as f:
        human = {r["id"].strip(): r for r in csv.DictReader(f) if (r.get("id") or "").strip()}
    both = [i for i in human if i in verdicts]
    out = {"graded": len(human), "compared": len(both)}
    for field in ("correct", "supported"):
        same = [i for i in both if str(human[i][field]).strip() == str(verdicts[i][field])]
        out[f"{field}_agreement"] = f"{len(same)}/{len(both)}" if both else "n/a"
        out[f"{field}_disagreements"] = [i for i in both if i not in same]
    return out


def failure_class(row: dict, a: dict, v: dict, hit5: bool | None) -> str:
    unanswerable = row["kind"].strip().lower() == "unanswerable"
    if unanswerable:
        return "answered an unanswerable question (unsupported claim)"
    if a["refused"]:
        return "wrong refusal" + (" (after a retrieval miss)" if hit5 is False else " (the passage was retrieved)")
    if hit5 is False:
        return "retrieval miss"
    if v["correct"] == 0:
        return "wrong answer from the right passage"
    return "unsupported claim"


def report(rows: list[dict], answers: dict, verdicts: dict, retrieval: dict) -> dict:
    chosen = index.CHOSEN_DESIGN
    hit5 = {}
    with RETRIEVAL_CSV.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            if r["design"] == chosen:
                hit5[r["id"]] = r["hit@5"] == "1"
    counts = {"answerable_correct": 0, "answerable_total": 0, "unsupported": 0, "correct_refusals": 0, "wrong_refusals": 0, "answered_unanswerable": 0, "unanswerable_total": 0}
    checks = {"no_search": 0, "invalid_citations": 0, "guardrail_fired": 0}
    tokens = seconds = n = 0
    failures = []
    for row in rows:
        a, v = answers.get(row["id"]), verdicts.get(row["id"])
        if not a or "error" in a or not v:
            continue
        n += 1
        tokens += a["tokens"]["total"]
        seconds += a["seconds"]
        c = code_checks(row, a)
        checks["no_search"] += not c["searched"]
        checks["invalid_citations"] += not c["citations_valid"]
        checks["guardrail_fired"] += c["guardrail_fired"]
        counts["unsupported"] += v["supported"] == 0
        if c["expected_refusal"]:
            counts["unanswerable_total"] += 1
            counts["correct_refusals"] += a["refused"]
            counts["answered_unanswerable"] += not a["refused"]
        else:
            counts["answerable_total"] += 1
            counts["answerable_correct"] += v["correct"]
            counts["wrong_refusals"] += a["refused"]
        if v["correct"] == 0 or v["supported"] == 0:
            failures.append({"id": row["id"], "kind": row["kind"], "question": row["question"], "suggested_class": failure_class(row, a, v, hit5.get(row["id"])), "judge_reason": v["reason"], "your_class": "", "your_notes": ""})
    with FAILURES_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "kind", "question", "suggested_class", "judge_reason", "your_class", "your_notes"])
        writer.writeheader()
        writer.writerows(failures)
    summary = {
        "model": next((a["model"] for a in answers.values() if "model" in a), None),
        "chosen_design": chosen,
        "retrieval": retrieval,
        "questions_evaluated": n,
        "results": counts,
        "code_checks": checks,
        "agreement_with_human_labels": agreement(verdicts),
        "failures": len(failures),
        "cost_per_question": {"mean_tokens": round(tokens / max(n, 1)), "mean_seconds": round(seconds / max(n, 1), 1)},
    }
    SUMMARY.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def print_summary(summary: dict) -> None:
    print("\n=== Retrieval (answerable questions) ===")
    print(f"{'design':<11}{'hit@1':>7}{'hit@3':>7}{'hit@5':>7}   {'source@1':>8}{'source@3':>9}{'source@5':>9}   multi:all pairs@5   words/prompt")
    for design, r in summary["retrieval"].items():
        print(f"{design:<11}{r['hit@1']:>7}{r['hit@3']:>7}{r['hit@5']:>7}   {r['source_hit@1']:>8}{r['source_hit@3']:>9}{r['source_hit@5']:>9}   {r['multi_all_pairs@5']:>17}   {r['mean_words_added_to_prompt@5']:>6}")
    print("(hit = right source AND section in the top k; source = right document only)")
    r, c = summary["results"], summary["code_checks"]
    print(f"\n=== End to end ({summary['questions_evaluated']} questions, design '{summary['chosen_design']}', model {summary['model']}) ===")
    print(f"correct answers      : {r['answerable_correct']}/{r['answerable_total']}")
    print(f"unsupported answers  : {r['unsupported']}")
    print(f"correct refusals     : {r['correct_refusals']}/{r['unanswerable_total']}")
    print(f"wrong refusals       : {r['wrong_refusals']}")
    print(f"answered unanswerable: {r['answered_unanswerable']}")
    print(f"code checks          : no search {c['no_search']}, invalid citations {c['invalid_citations']}, guardrail fired {c['guardrail_fired']}")
    print(f"agreement with you   : {summary['agreement_with_human_labels']}")
    print(f"cost per question    : {summary['cost_per_question']}")
    print(f"\nFiles: {SUMMARY.name}, {FAILURES_CSV.name}, {JUDGE_CSV.name}, {RETRIEVAL_CSV.name}, {GRADING_SHEET.name} (all in eval/)")


# ---------------------------------------------------------------------------
# Add-document demo: the answer before and after adding a document
# ---------------------------------------------------------------------------
async def demo(question_id: str) -> None:
    rows = load_questions()
    row = next((r for r in rows if r["id"] == question_id), None)
    if row is None or row["kind"].strip().lower() != "unanswerable":
        raise SystemExit(f"{question_id} is not an unanswerable question in eval/questions.csv")
    path = ROOT / "corpus" / "holdback" / "chapter-22-varicella.html"
    if not path.is_file():
        raise SystemExit("Run `uv run python main.py index` first: it downloads the held-back document.")
    out = {"question": row["question"], "document": str(path.name)}
    async with agent.Harness() as harness:  # the approval prompt appears here: answer y
        out["before"] = await harness.ask(row["question"])
        out["add_request"] = await harness.ask(f"Please add the document at {path} to the corpus.")
        if not any(t["tool"] == "add_document" for t in out["add_request"]["tool_trace"]):
            log("The agent did not call add_document; adding the file directly.")
            out["added_directly"] = index.index_file(path)
        out["after"] = await harness.ask(row["question"])
    DEMO_JSON.write_text(json.dumps(out, indent=2), encoding="utf-8")
    print(f"\nBEFORE: {out['before']['answer']}\n\nAFTER:  {out['after']['answer']}")
    if "--keep" not in sys.argv:  # take the document out again so the committed index stays the one you evaluated
        for design in index.DESIGNS:
            index.get_collection(design).delete(where={"source": path.stem})
        print("\nThe added passages were removed again (use --keep to keep them). Evidence saved in eval/add_document_demo.json")


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    load_api_key()
    if "--demo" in sys.argv:
        rest = [a for a in sys.argv[sys.argv.index("--demo") + 1 :] if not a.startswith("--")]
        asyncio.run(demo(rest[0] if rest else "q32"))
        return
    rows = load_questions()
    log("1/4 retrieval ...")
    retrieval = retrieval_stage(rows)
    log("2/4 agent answers ...")
    answers = asyncio.run(answers_stage(rows))
    log("3/4 code checks and judge ...")
    verdicts = judge_stage(rows, answers)
    log("4/4 report ...")
    summary = report(rows, answers, verdicts, retrieval)
    print_summary(summary)


if __name__ == "__main__":
    main()
