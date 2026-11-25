"""
Assignment 3: evaluation (`main.py evaluate`).

Stages (results in eval/; expensive stages are cached so reruns cost no quota):
  1. Retrieval: hit rate at k = 1, 3, 5 for each design, words added to the
     prompt; picks the best design and writes it to index/config.json.
  2. Agent: runs agent.py on every question (cache: eval/answers.json) and
     writes eval/answers_for_grading.csv for your own blind grading.
  3. Code checks: valid citations, refusals, expected source cited.
  4. LLM judge with a rubric and the retrieved text as evidence (cache: eval/judge.json).
  5. Agreement between the judge and eval/human_labels.csv.
  6. Add-document demo: Lixiana question before and after adding the Lixiana PDF.
  7. Failure causes (first-pass, for you to review) and a summary.

    uv run python evaluate.py            # use caches
    uv run python evaluate.py --rerun    # re-ask the agent and judge everything
"""

import argparse
import asyncio
import csv
import json
import statistics
import sys
import time
import warnings
from contextlib import AsyncExitStack
from pathlib import Path

warnings.filterwarnings("ignore")

from pydantic import BaseModel, Field  # noqa: E402

import index  # noqa: E402
import retrieval  # noqa: E402

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
JUDGE_MODEL = "gemma-4-31b-it"  # different model family from the agent (avoids self-preference); gemini-3.5-flash allows only 20 requests/day on the free tier
CONFIGS = [("fixed", "dense"), ("section", "dense"), ("fixed", "hybrid"), ("section", "hybrid")]
KS = (1, 3, 5)
DEMO_FILE = ROOT / "corpus" / "lixiana.pdf"


def load_questions() -> list[dict]:
    with open(EVAL / "questions.csv", newline="") as f:
        return list(csv.DictReader(f))


def expected_pairs(q: dict) -> list[list[tuple[str, str, str]]]:
    """One entry per expected passage; each entry lists acceptable (source, part, number)."""
    pairs = []
    for source, locations in zip(q["expected_source"].split(";"), q["expected_location"].split(";")):
        options = []
        for loc in locations.split("|"):
            part, number = loc.strip().split()
            options.append((source.strip(), part, number))
        pairs.append(options)
    return pairs


def matches(meta: dict, option: tuple[str, str, str]) -> bool:
    source, part, number = option
    section_number = meta["section"].split()[0].rstrip(".")
    return meta["source"] == source and meta["doc_part"] == part and section_number == number


def found_all(metas: list[dict], q: dict) -> bool:
    return all(any(matches(m, o) for m in metas for o in options) for options in expected_pairs(q))


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


# ---------------------------------------------------------------- 1. retrieval


def evaluate_retrieval(questions: list[dict]) -> dict:
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    rows, table = [], {}
    for design, method in CONFIGS:
        name = f"{design}+{method}"
        hits = {k: 0 for k in KS}
        words = []
        for q in answerable:
            top = retrieval.search(q["question"], k=max(KS), design=design, method=method)
            metas = [c["metadata"] for c in top]
            words.append(sum(len(c["text"].split()) for c in top))
            for k in KS:
                hit = found_all(metas[:k], q)
                hits[k] += hit
                rows.append({"config": name, "id": q["id"], "kind": q["kind"], "k": k, "hit": int(hit)})
        table[name] = {f"hit@{k}": round(hits[k] / len(answerable), 3) for k in KS}
        table[name]["words_in_prompt@5"] = round(statistics.mean(words))
        table[name]["chunks_in_index"] = index.collection(design).count()
    write_csv(EVAL / "retrieval_hits.csv", rows)

    best = max(table, key=lambda n: (table[n]["hit@5"], table[n]["hit@3"], table[n]["hit@1"],
                                     -table[n]["words_in_prompt@5"]))
    design, method = best.split("+")
    config = index.config() | {"active_design": design, "method": method,
                               "embedding_model": index.EMBED_MODEL, "dimensions": index.EMBED_DIM}
    index.CONFIG_FILE.write_text(json.dumps(config, indent=2))
    print(f"\n1. Retrieval over {len(answerable)} answerable questions "
          f"(multi questions count as a hit only if every expected passage is retrieved)")
    print(f"   {'config':16} {'hit@1':>6} {'hit@3':>6} {'hit@5':>6} {'words@5':>8} {'chunks':>7}")
    for name, r in table.items():
        print(f"   {name:16} {r['hit@1']:6.2f} {r['hit@3']:6.2f} {r['hit@5']:6.2f} "
              f"{r['words_in_prompt@5']:8} {r['chunks_in_index']:7}" + ("   <- chosen" if name == best else ""))
    return {"table": table, "chosen": best}


# ---------------------------------------------------------------- 2. agent


async def run_agent(questions: list[dict], rerun: bool) -> dict:
    import agent
    path = EVAL / "answers.json"
    answers = {} if rerun or not path.exists() else json.loads(path.read_text())
    # Re-ask a question if it is new or its wording changed since it was answered.
    todo = [q for q in questions if answers.get(q["id"], {}).get("question") != q["question"]]
    if todo:
        async with AsyncExitStack() as stack:
            bot = agent.build_agent(await agent.load_tools(stack), auto_approve=False)
            for i, q in enumerate(todo, 1):
                for attempt in range(3):
                    try:
                        result = await agent.run_question(bot, q["question"])
                        break
                    except Exception as error:  # rate limits: wait and retry
                        print(f"   {q['id']}: {type(error).__name__}, retrying", file=sys.stderr)
                        time.sleep(30 * (attempt + 1))
                else:
                    raise SystemExit(f"Agent failed on {q['id']}; rerun later (answers so far are saved).")
                answers[q["id"]] = result
                path.write_text(json.dumps(answers, indent=2, ensure_ascii=False))
                print(f"   agent {i}/{len(todo)} {q['id']} ({result['seconds']} s)", file=sys.stderr)
                time.sleep(2)
    # Blind grading sheet: question, reference, answer, evidence. No judge verdicts here.
    write_csv(EVAL / "answers_for_grading.csv", [
        {"id": q["id"], "kind": q["kind"], "question": q["question"],
         "reference_answer": q["reference_answer"], "agent_answer": answers[q["id"]]["answer"],
         "retrieved_text": answers[q["id"]]["retrieved"][:3000]}
        for q in questions])
    return answers


# ---------------------------------------------------------------- 3. code checks


def code_checks(q: dict, a: dict) -> dict:
    unanswerable = q["kind"] == "unanswerable"
    cited_sources = {c.strip("[]").split(" | ")[0] for c in a["cited"]}
    expected = set(filter(None, q["expected_source"].split(";")))
    return {
        "citations_valid": not a["invalid_citations"],
        "has_citation": bool(a["cited"]),
        "refused": a["refused"] or a["guardrail_fired"],
        "correct_refusal": unanswerable and (a["refused"] or a["guardrail_fired"]),
        "wrong_refusal": (not unanswerable) and (a["refused"] or a["guardrail_fired"]),
        "cites_expected_source": (not unanswerable) and expected <= cited_sources,
        "guardrail_fired": a["guardrail_fired"],
    }


# ---------------------------------------------------------------- 4. judge


class Verdict(BaseModel):
    reasoning: str = Field(description="Two to four sentences checking the answer against each criterion.")
    correct: bool = Field(description="Criterion 1.")
    supported: bool = Field(description="Criterion 2.")


RUBRIC = """You grade an assistant that answers family caregivers' questions about blood thinners
(Eliquis, Xarelto, Pradaxa) using only passages from the official EU product information.

Criteria:
1. correct: the answer agrees with the reference answer on every point that matters for the caregiver's
   decision (doses, times, yes/no, what to do). Extra correct detail is fine; a missing safety-critical
   point or any contradiction is not. If the question is unanswerable, correct means the assistant said
   the documents do not cover it and did not give a substantive answer.
2. supported: every factual claim in the answer is stated in the retrieved passages below. A claim that
   is plausible but not in the passages is unsupported. A pure refusal is supported.

Question kind: {kind}
Question: {question}
Reference answer: {reference_answer}

Retrieved passages (all the assistant saw):
{retrieved}

Assistant's answer:
{answer}"""


async def judge_answers(questions, answers, rerun: bool) -> dict:
    from langchain_google_genai import ChatGoogleGenerativeAI
    from api_key import load_api_key
    path = EVAL / "judge.json"
    verdicts = {} if rerun or not path.exists() else json.loads(path.read_text())
    judge = ChatGoogleGenerativeAI(model=JUDGE_MODEL, api_key=load_api_key()).with_structured_output(Verdict)
    for q in questions:
        a = answers[q["id"]]
        key = f"{q['id']}|{a['answer']}"
        if verdicts.get(q["id"], {}).get("key") == key:
            continue
        prompt = RUBRIC.format(kind=q["kind"], question=q["question"],
                               reference_answer=q["reference_answer"],
                               retrieved=a["retrieved"] or "(no passages retrieved)", answer=a["answer"])
        for attempt in range(3):
            try:
                v = await judge.ainvoke(prompt)
                break
            except Exception as error:
                print(f"   judge {q['id']}: {type(error).__name__}, retrying", file=sys.stderr)
                time.sleep(30 * (attempt + 1))
        else:
            raise SystemExit("Judge failed; rerun later (verdicts so far are saved).")
        verdicts[q["id"]] = {"key": key, **v.model_dump()}
        path.write_text(json.dumps(verdicts, indent=2, ensure_ascii=False))
    return verdicts


# ---------------------------------------------------------------- 5. agreement


def agreement(verdicts: dict) -> dict:
    path = EVAL / "human_labels.csv"
    with open(path, newline="") as f:
        labels = [r for r in csv.DictReader(f) if r.get("id") and r.get("correct", "").strip()]
    rows = []
    for r in labels:
        v = verdicts.get(r["id"])
        if not v:
            continue
        human_c, human_s = r["correct"].strip() == "1", r.get("supported", "").strip() == "1"
        rows.append({"id": r["id"], "human_correct": int(human_c), "judge_correct": int(v["correct"]),
                     "human_supported": int(human_s), "judge_supported": int(v["supported"]),
                     "agree_correct": int(human_c == v["correct"]),
                     "agree_supported": int(human_s == v["supported"])})
    write_csv(EVAL / "agreement.csv", rows)
    if not rows:
        return {"graded": 0}
    n = len(rows)
    return {"graded": n,
            "agree_correct": round(sum(r["agree_correct"] for r in rows) / n, 3),
            "agree_supported": round(sum(r["agree_supported"] for r in rows) / n, 3),
            "disagreements": [r["id"] for r in rows if not (r["agree_correct"] and r["agree_supported"])]}


# ---------------------------------------------------------------- 6. add-document demo


async def add_document_demo(questions, answers) -> dict:
    import agent
    path = EVAL / "add_document_demo.json"
    if path.exists():
        return json.loads(path.read_text())
    # The unanswerable question about Lixiana/edoxaban, which the added document should answer.
    q = next(q for q in questions if q["kind"] == "unanswerable"
             and any(w in q["question"].lower() for w in ("lixiana", "edoxaban")))
    before = answers[q["id"]]
    async with AsyncExitStack() as stack:
        tools = await agent.load_tools(stack)
        add = next(t for t in tools if t.name == "add_document")
        added = await add.ainvoke({"path": str(DEMO_FILE.relative_to(ROOT))})
        bot = agent.build_agent(tools)
        after = await agent.run_question(bot, q["question"])
    demo = {"id": q["id"], "question": q["question"], "document": DEMO_FILE.name, "add_document_result": str(added),
            "before": before["answer"], "after": after["answer"], "after_citations": after["cited"]}
    path.write_text(json.dumps(demo, indent=2, ensure_ascii=False))
    return demo


# ---------------------------------------------------------------- 7. failures and summary


def classify(q, a, checks, verdict) -> str:
    """First-pass failure cause. Review these by hand; 'bad test question' needs a human."""
    if q["kind"] == "unanswerable":
        return "" if checks["correct_refusal"] and verdict["correct"] else "unsupported claim"
    if verdict["correct"] and verdict["supported"]:
        return ""
    retrieved = [{"source": c.strip("[]").split(" | ")[0],
                  "doc_part": "leaflet" if " | Package leaflet | " in c else "smpc",
                  "section": c.strip("[]").split(" | ")[3]}
                 for c in retrieval_citations(a["retrieved"])]
    if not found_all(retrieved, q):
        return "retrieval miss"
    if checks["wrong_refusal"]:
        return "wrong refusal"
    if not verdict["correct"]:
        return "wrong answer from right passage"
    return "unsupported claim"


def retrieval_citations(text: str) -> list[str]:
    import agent
    return agent.CITATION.findall(text)


def summarise(questions, answers, verdicts, retrieval_result, agree, demo) -> dict:
    rows = []
    for q in questions:
        a, v = answers[q["id"]], verdicts[q["id"]]
        checks = code_checks(q, a)
        rows.append({"id": q["id"], "kind": q["kind"], **{k: int(x) for k, x in checks.items()},
                     "judge_correct": int(v["correct"]), "judge_supported": int(v["supported"]),
                     "auto_failure_cause": classify(q, a, checks, v),
                     "input_tokens": a["tokens"]["input"], "output_tokens": a["tokens"]["output"],
                     "seconds": a["seconds"], "judge_reasoning": v["reasoning"]})
    write_csv(EVAL / "results.csv", rows)

    ans = [r for r in rows if r["kind"] != "unanswerable"]
    una = [r for r in rows if r["kind"] == "unanswerable"]
    causes: dict[str, int] = {}
    for r in rows:
        if r["auto_failure_cause"]:
            causes[r["auto_failure_cause"]] = causes.get(r["auto_failure_cause"], 0) + 1
    summary = {
        "questions": len(rows),
        "retrieval": retrieval_result,
        "answerable": {"n": len(ans),
                       "correct": sum(r["judge_correct"] for r in ans),
                       "correct_and_supported": sum(r["judge_correct"] and r["judge_supported"] for r in ans),
                       "unsupported": sum(1 - r["judge_supported"] for r in ans),
                       "wrong_refusals": sum(r["wrong_refusal"] for r in ans),
                       "cites_expected_source": sum(r["cites_expected_source"] for r in ans)},
        "unanswerable": {"n": len(una), "correct_refusals": sum(r["correct_refusal"] for r in una)},
        "citations_valid": sum(r["citations_valid"] for r in rows),
        "guardrail_fired": [r["id"] for r in rows if r["guardrail_fired"]],
        "failure_causes_auto": causes,
        "judge_vs_human": agree,
        "cost_per_question": {
            "mean_input_tokens": round(statistics.mean(r["input_tokens"] for r in rows)),
            "mean_output_tokens": round(statistics.mean(r["output_tokens"] for r in rows)),
            "mean_seconds": round(statistics.mean(r["seconds"] for r in rows), 1),
            "median_seconds": round(statistics.median(r["seconds"] for r in rows), 1)},
        "add_document_demo": demo,
    }
    (EVAL / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    return summary


async def main(rerun: bool) -> None:
    questions = load_questions()
    retrieval_result = evaluate_retrieval(questions)

    print(f"\n2. Agent on {len(questions)} questions", file=sys.stderr)
    answers = await run_agent(questions, rerun)
    verdicts = await judge_answers(questions, answers, rerun)
    agree = agreement(verdicts)
    demo = await add_document_demo(questions, answers)
    s = summarise(questions, answers, verdicts, retrieval_result, agree, demo)

    a, u, c = s["answerable"], s["unanswerable"], s["cost_per_question"]
    print(f"\n2-4. End to end ({s['questions']} questions)")
    print(f"   answerable {a['n']}: correct {a['correct']}, correct and supported {a['correct_and_supported']}, "
          f"unsupported {a['unsupported']}, wrong refusals {a['wrong_refusals']}")
    print(f"   unanswerable {u['n']}: correct refusals {u['correct_refusals']}")
    print(f"   valid citations {s['citations_valid']}/{s['questions']}; citation guardrail fired on {s['guardrail_fired']}")
    print(f"   failure causes (auto, review by hand): {s['failure_causes_auto']}")
    print(f"5. Judge vs your labels: {agree}")
    print(f"6. Add document: {demo['document']}\n   before: {demo['before'][:200]}\n   after:  {demo['after'][:300]}")
    print(f"7. Cost per question: {c['mean_input_tokens']} input + {c['mean_output_tokens']} output tokens, "
          f"{c['mean_seconds']} s mean")
    print("\nFiles: eval/retrieval_hits.csv, answers.json, answers_for_grading.csv, judge.json, "
          "agreement.csv, results.csv, add_document_demo.json, summary.json")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--rerun", action="store_true", help="ignore cached agent answers and verdicts")
    asyncio.run(main(parser.parse_args().rerun))
