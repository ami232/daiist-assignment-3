"""
Assignment 3: evaluation (`main.py evaluate`).

Built like session 10's 07-own-harness/evaluate.py. Steps:
  1. Retrieval: hit rate at k = 1, 3, 5 for each design in retrieve.py.
  2. Agent: run agent.py on every question in eval/questions.csv.
  3. Code checks: did it search, refuse, cite only passages it really retrieved.
  4. LLM judge: correct? supported? with a rubric and the retrieved text as evidence.
  5. Agreement between the judge and your own grades in eval/human_labels.csv.
  6. Noise: bootstrap 95% intervals, because 30 questions is a small sample and
     "a difference smaller than the noise is not a result" (MLOps session).
  7. Run log: one row per run in eval/runs.csv with the versions that produced it
     (prompt, models, retrieval design, index, test set) and its metrics.

Results go to eval/. Answers and verdicts are saved as they come and reused on
the next run (delete eval/answers.json or eval/judge.json to redo them), so a
rate limit or a crash costs nothing and re-runs are cheap.

    uv run python main.py evaluate                     # the main run, in eval/
    uv run python evaluate.py --judge-only             # finish judging, skip retrieval
    uv run python evaluate.py --rejudge                # judge again (new rubric), skip retrieval
    uv run python evaluate.py --run v2 --note "..."    # a new prompt version on the same test
                                                       # cases, saved in eval/runs/v2/ and
                                                       # compared with the main run
"""

import asyncio
import csv
import json
import random
import re
import sys
from contextlib import AsyncExitStack
from datetime import datetime, timezone
from pathlib import Path

from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

from agent import MODEL as AGENT_MODEL
from agent import ask, build_agent, load_mcp_tools, prompt_version, short_hash
from api_key import load_api_key
from index import CHUNK_WORDS, EMBEDDING_MODEL, embed_texts, get_collection, query_text
from retrieve import DESIGN, TOP_K, Retriever

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"


def arg(name):
    """Value after a command-line flag, e.g. --run v2."""
    return sys.argv[sys.argv.index(name) + 1] if name in sys.argv[:-1] else None


RUN_NAME = arg("--run")                                  # None = the main run
OUT = EVAL / "runs" / RUN_NAME if RUN_NAME else EVAL     # where this run's files go
JUDGE_MODEL = "gemini-3.5-flash"  # a stronger model than the agent's
DESIGNS = ["dense", "dense+filter", "hybrid", "hybrid+filter"]
KS = [1, 3, 5]
REFUSAL = "the filings i have do not cover"  # how AGENTS.md tells the agent to start a refusal


def read_csv(path):
    if not path.is_file():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if (r.get("id") or "").strip()]


def write_csv(path, rows):
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def load_json(path, default):
    return json.loads(path.read_text()) if path.is_file() else default


def save_json(path, data):
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False))


def split(value):
    return [v.strip() for v in (value or "").split(";") if v.strip()]


def expected_passages(q):
    """[(source, location), ...]. One location applies to all sources if only one is given."""
    sources, locations = split(q["expected_source"]), split(q["expected_location"])
    if len(locations) == len(sources):
        return list(zip(sources, locations))
    return [(s, loc) for s in sources for loc in (locations or [""])]


def matches(source, location, passage):
    exp_source, exp_location = passage
    return source == exp_source and location.startswith(exp_location)


# ---------------------------------------------------------------- 1. retrieval

def query_vectors(questions):
    """Embed each test question once and keep the vectors in eval/, to save quota."""
    path = EVAL / "query_vectors.json"
    cache = load_json(path, {})
    todo = [q["question"] for q in questions if q["question"] not in cache]
    for i in range(0, len(todo), 50):
        batch = todo[i:i + 50]
        for text, vector in zip(batch, embed_texts([query_text(t) for t in batch])):
            cache[text] = vector
        save_json(path, cache)
    return cache


def evaluate_retrieval(questions, retriever, vectors):
    """Hit rate per design and k. Returns per-question hits, for the bootstrap."""
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    rows, misses, per_question = [], [], {}
    for design in DESIGNS:
        row = {"design": design}
        for k in KS:
            any_hit, all_hit, words = [], [], []
            for q in answerable:
                chunks = retriever.search(q["question"], k=k, design=design, query_vector=vectors[q["question"]])
                found = [any(matches(c["metadata"]["source"], c["metadata"]["location"], p) for c in chunks)
                         for p in expected_passages(q)]
                any_hit.append(any(found))
                all_hit.append(all(found))
                words.append(sum(len(c["text"].split()) for c in chunks))
                if k == 5 and design == DESIGN and not any(found):
                    misses.append({"id": q["id"], "question": q["question"],
                                   "expected": q["expected_source"] + " / " + q["expected_location"],
                                   "got": "; ".join(f"{c['metadata']['source']}, {c['metadata']['location']}" for c in chunks[:3])})
            per_question[(design, k)] = any_hit
            row[f"hit@{k}"] = round(sum(any_hit) / len(any_hit), 3)
            multi = [a for a, q in zip(all_hit, answerable) if q["kind"] == "multi"]
            row[f"all_passages@{k}"] = round(sum(multi) / len(multi), 3) if multi else ""
            row[f"words@{k}"] = round(sum(words) / len(words))
        rows.append(row)

    write_csv(EVAL / "retrieval.csv", rows)
    (EVAL / "retrieval_misses.csv").unlink(missing_ok=True)  # an old file must not outlive a run with no misses
    write_csv(EVAL / "retrieval_misses.csv", misses)
    print(f"Retrieval on {len(answerable)} answerable questions (hit = an expected passage in the top k)")
    print(f"{'design':<15}" + "".join(f"{'hit@' + str(k):>8}" for k in KS) + f"{'multi all@5':>13}{'words@5':>9}")
    for r in rows:
        print(f"{r['design']:<15}" + "".join(f"{r[f'hit@{k}']:>8.0%}" for k in KS)
              + f"{r['all_passages@5'] if r['all_passages@5'] == '' else format(r['all_passages@5'], '.0%'):>13}"
              + f"{r['words@5']:>9}")
    print(f"(search tool uses {DESIGN!r}; {len(misses)} questions missed at k=5, see eval/retrieval_misses.csv)\n")
    return per_question


# ---------------------------------------------------------------- 2. agent

async def run_agent(questions):
    path = OUT / "answers.json"
    answers = load_json(path, {})
    todo = [q for q in questions if q["id"] not in answers]
    if todo:
        print(f"Running the agent on {len(todo)} question(s)...")
        async with AsyncExitStack() as stack:
            agent = build_agent(await load_mcp_tools(stack), approval="deny")  # never add documents here
            for q in todo:
                try:
                    answer, trace, stats = await ask(agent, q["question"])
                except Exception as error:  # noqa: BLE001
                    if quota_error(error):  # don't save a quota error as if it were an answer
                        print(f"Agent quota reached. {len(answers)} answers are saved; "
                              "run the same command again tomorrow to finish.")
                        break
                    answer, trace, stats = f"ERROR: {type(error).__name__}: {error}", [], {}  # record it, move on
                answers[q["id"]] = {"answer": answer, "trace": trace, "stats": stats}
                save_json(path, answers)  # saved after every question
                print(f"  {q['id']} {stats.get('seconds', '?')}s")
    return answers


# ---------------------------------------------------------------- 3. code checks

CITATION = re.compile(r"\[([A-Z]{2,5} 10-[KQ] [0-9]{4}(?:-Q[1-4])?), ([^\]]+)\]")


def retrieved_citations(trace):
    return {(m.group(1), m.group(2).strip())
            for line in trace if line.startswith("result ")
            for m in CITATION.finditer(line)}


def cited_in(answer):
    """Citations in the answer. The model sometimes puts two in one bracket:
    [SAIA 10-K 2025, Item 1A > Risks, Item 7 > Outlook] or
    [ODFL 10-K 2025, Item 1 > Competition; ODFL 10-K 2025, Item 1 > Overview].
    Both are split into separate citations. A location that merges two headings
    ("JBI Segment and Operating Revenue by Segment") is not split: it names no real passage."""
    found = set()
    for inside in re.findall(r"\[([^\]]+)\]", answer):
        source = None
        for part in re.split(r";\s*", inside):
            m = re.match(r"([A-Z]{2,5} 10-[KQ] [0-9]{4}(?:-Q[1-4])?),\s*(.+)", part.strip())
            if m:
                source, rest = m.group(1), m.group(2)
            elif source:
                rest = part
            else:
                continue  # a bracket that is not a citation
            for location in re.split(r",\s*(?=Item \d)", rest):
                found.add((source, location.strip()))
    return found


def code_checks(q, run):
    answer, trace = run["answer"], run["trace"]
    retrieved = retrieved_citations(trace)
    cited = cited_in(answer)
    refused = answer.strip().lower().startswith(REFUSAL)
    withheld = answer.startswith("Answer withheld")
    checks = {
        "searched": any(line.startswith("call search") for line in trace),
        "refused": refused,
        "withheld_by_guardrail": withheld,
        "cites_something": bool(cited),
        "citations_valid": all(c in retrieved for c in cited),
        # was an expected passage among what the agent's own searches returned?
        "expected_passage_retrieved": any(matches(s, loc, p) for (s, loc) in retrieved for p in expected_passages(q))
        if q["kind"] != "unanswerable" else "",
    }
    if q["kind"] == "unanswerable":
        checks["code_pass"] = refused
    else:
        checks["code_pass"] = (not refused and not withheld and checks["cites_something"]
                               and checks["citations_valid"])
    return checks


# ---------------------------------------------------------------- 4. judge

# The judge returns this structure, not free text, so the program can count.
# The reasoning comes first so the model explains before it decides.
class Verdict(BaseModel):
    id: str = Field(description="The id of the answer being graded, e.g. q07.")
    reasoning: str = Field(description="Two or three sentences checking the answer against each criterion.")
    correct: bool = Field(description="True only if criterion 1 is met.")
    supported: bool = Field(description="True only if criterion 2 is met.")


class Verdicts(BaseModel):
    verdicts: list[Verdict] = Field(description="One verdict per answer, in the order given.")


# The free tier allows gemini-3.5-flash only 20 requests a day, so the judge
# grades several answers per request. Each answer is still graded on its own.
JUDGE_BATCH = 5


# The rubric (Allan's).
JUDGE_PROMPT = """You are grading answers from an AI assistant that helps sellers prepare for meetings with trucking companies. The companies are Old Dominion, J.B. Hunt, Saia and Knight-Swift. The answers should come from SEC filings. Your job is to check if the assistant gave the right information and did not make anything up or hallucinate. A wrong answer could lead to a seller giving incorrect information to a client, so accuracy of response is crucial.

Criteria:
1. Correct: Compare the answer with the reference answer. To get a 1, it must include every point in the reference, even if the question doesn't directly ask for all of them. If even one point is missing, give it a 0. The wording doesn't need to be identical, but the meaning and figures must match. Wrong numbers, company names or reporting periods also get a 0. Extra information is fine as long as it's correct.
If the reference says the information isn't available, the assistant should refuse to answer rather than guess. A correct refusal gets a 1. If the assistant says "Answer withheld" when the reference has an answer, give it a 0. Partly correct answers also get a 0.
2. Supported: Check whether everything the assistant says can be found in the retrieved passages. Give it a 1 only if all facts and numbers are supported and the citations point to the right passages. If it adds information that isn't there, give it a 0, even if the information might be true. A refusal or "Answer withheld" gets a 1 for Supported, since no unsupported answer was given.
Grade Correct and Supported separately. An answer can be supported by the filings but still be incorrect because it missed something from the reference.
Grade each of the answers below on its own, against its own reference answer and its own retrieved passages. Return one verdict per answer, with its id.
{items}"""

ITEM = """=== Answer {id} ===
Question: {question}
Reference answer: {reference_answer}
Retrieved passages (recorded by the harness):
{evidence}
Answer to grade:
{answer}
"""


def quota_error(error):
    return "RESOURCE_EXHAUSTED" in str(error) or "429" in str(error)


async def run_judge(questions, answers):
    path = OUT / "judge.json"
    verdicts = load_json(path, {})
    todo = [q for q in questions if q["id"] not in verdicts and q["id"] in answers]
    if todo:
        print(f"Judging {len(todo)} answer(s), {JUDGE_BATCH} per request...")
        judge = ChatGoogleGenerativeAI(model=JUDGE_MODEL, temperature=0).with_structured_output(Verdicts)
        for i in range(0, len(todo), JUDGE_BATCH):
            batch = todo[i:i + JUDGE_BATCH]
            items = []
            for q in batch:
                run = answers[q["id"]]
                evidence = "\n\n".join(line.removeprefix("result ") for line in run["trace"]
                                       if line.startswith("result ")) or "(no passages retrieved)"
                items.append(ITEM.format(id=q["id"], question=q["question"], reference_answer=q["reference_answer"],
                                         evidence=evidence, answer=run["answer"]))
            try:
                result = await judge.ainvoke(JUDGE_PROMPT.format(items="\n".join(items)))
            except Exception as error:  # noqa: BLE001
                if quota_error(error):
                    print(f"Judge quota reached after {len(verdicts)} verdicts. They are saved; after 09:00 "
                          "Spain time run the same command again to finish.")
                    break
                raise
            wanted = {q["id"] for q in batch}
            for v in result.verdicts:
                if v.id in wanted:  # ignore anything the judge invents
                    verdicts[v.id] = v.model_dump(exclude={"id"})
            save_json(path, verdicts)
            print(f"  judged {len(verdicts)}/{len(questions)}")
    return verdicts


# ---------------------------------------------------------------- 5. report

def agreement(verdicts, labels):
    rows = []
    for label in labels:
        v = verdicts.get(label["id"])
        if v and label.get("correct", "").strip() in ("0", "1"):
            rows.append((label, v))
    if not rows:
        print("No grades in eval/human_labels.csv yet: grade 20+ answers from eval/for_grading.csv.\n")
        return {}
    result = {"graded": len(rows)}
    for field in ("correct", "supported"):
        pairs = [(int(l[field]), int(v[field])) for l, v in rows if l.get(field, "").strip() in ("0", "1")]
        result[f"agreement_{field}"] = round(sum(a == b for a, b in pairs) / len(pairs), 3) if pairs else None
        result[f"disagree_{field}"] = [l["id"] for l, v in rows
                                       if l.get(field, "").strip() in ("0", "1") and int(l[field]) != int(v[field])]
    print(f"Judge vs your grades on {len(rows)} answers: correct agree {result['agreement_correct']:.0%}, "
          f"supported agree {result['agreement_supported']:.0%}")
    print(f"  disagree on correct: {result['disagree_correct'] or 'none'}; "
          f"on supported: {result['disagree_supported'] or 'none'}\n")
    return result


# ---------------------------------------------------------------- 6. noise

def bootstrap_ci(values, n=1000, seed=0):
    """95% interval for the mean of 0/1 values: resample the questions with replacement
    1,000 times and take the 2.5th and 97.5th percentiles (data pipelines session)."""
    if not values:
        return None
    rng = random.Random(seed)  # fixed seed, so the interval is reproducible
    means = sorted(sum(rng.choices(values, k=len(values))) / len(values) for _ in range(n))
    return round(means[int(0.025 * n)], 3), round(means[int(0.975 * n) - 1], 3)


def paired_diff_ci(a, b, n=1000, seed=0):
    """95% interval for mean(a) - mean(b) on the same questions (paired bootstrap)."""
    if not a:
        return None
    rng = random.Random(seed)
    idx = range(len(a))
    diffs = sorted(sum(a[i] - b[i] for i in s) / len(a)
                   for s in (rng.choices(idx, k=len(a)) for _ in range(n)))
    return round(diffs[int(0.025 * n)], 3), round(diffs[int(0.975 * n) - 1], 3)


def fmt_ci(ci):
    return f"{ci[0]:.0%} to {ci[1]:.0%}" if ci else "n/a"


# ---------------------------------------------------------------- 7. run log

RUN_FIELDS = [
    "time", "run", "note", "prompt_version", "agent_model", "judge_model", "rubric_version",
    "embedding_model", "retrieval_design", "top_k", "chunk_words", "index_chunks", "test_set_version",
    "questions", "judged", "judge_correct", "judge_correct_ci", "human_correct", "human_correct_ci",
    "unsupported", "correct_refusals", "wrong_refusals", "withheld", "coverage", "accuracy_on_covered",
    "invalid_citations", f"hit@3_{DESIGN}", "mean_seconds", "mean_tokens",
]


def versions(answers):
    """Everything that decides an answer (MLOps session: 'Tracking an LLM application')."""
    stamped = {a.get("stats", {}).get("prompt_version") for a in answers.values()} - {None}
    return {
        # the prompt version recorded on the answers themselves, not today's AGENTS.md
        "prompt_version": ", ".join(sorted(stamped)) if stamped else "not recorded (answers from before tracking)",
        "agent_model": AGENT_MODEL,
        "judge_model": JUDGE_MODEL,
        "rubric_version": short_hash(JUDGE_PROMPT),
        "embedding_model": EMBEDDING_MODEL,
        "retrieval_design": DESIGN,
        "top_k": TOP_K,
        "chunk_words": CHUNK_WORDS,
        "index_chunks": get_collection().count(),
        "test_set_version": short_hash((EVAL / "questions.csv").read_text(encoding="utf-8")),
    }


def log_run(row):
    path = EVAL / "runs.csv"
    new = not path.is_file()
    with path.open("a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=RUN_FIELDS, extrasaction="ignore")
        if new:
            writer.writeheader()
        writer.writerow(row)


def compare_with_main(questions, verdicts):
    """A prompt change is a new version: compare it with the main run on the same test cases."""
    main_verdicts = load_json(EVAL / "judge.json", {})
    common = [q["id"] for q in questions if q["id"] in verdicts and q["id"] in main_verdicts]
    if not common:
        return None
    new = [int(verdicts[i]["correct"]) for i in common]
    old = [int(main_verdicts[i]["correct"]) for i in common]
    result = {
        "questions_compared": len(common),
        "main_correct": sum(old), "this_run_correct": sum(new),
        "difference_ci": paired_diff_ci(new, old),
        "fixed": [i for i, a, b in zip(common, new, old) if a > b],
        "broken": [i for i, a, b in zip(common, new, old) if a < b],
    }
    ci = result["difference_ci"]
    verdict = ("better, beyond the noise" if ci[0] > 0 else
               "worse, beyond the noise" if ci[1] < 0 else "within the noise: cannot tell")
    result["verdict"] = verdict
    print(f"Compared with the main run on {len(common)} questions (judge): "
          f"{sum(old)} -> {sum(new)} correct; 95% interval of the difference "
          f"{ci[0]:+.0%} to {ci[1]:+.0%}: {verdict}.")
    print(f"  fixed: {result['fixed'] or 'none'}; broken: {result['broken'] or 'none'}\n")
    return result


def main():
    load_api_key()
    questions = read_csv(EVAL / "questions.csv")
    if not questions:
        raise SystemExit("eval/questions.csv has no questions yet.")

    OUT.mkdir(parents=True, exist_ok=True)
    per_question_hits = None
    if RUN_NAME:
        # A new prompt version: retrieval does not depend on the prompt, so it is not re-run.
        print(f"Run {RUN_NAME!r}: answers and verdicts go to {OUT.relative_to(ROOT)}/.\n")
    elif "--rejudge" in sys.argv or "--judge-only" in sys.argv:
        # Judge the saved answers without re-running the retrieval test, so its saved
        # numbers in eval/retrieval.csv stay as they were.
        #   --rejudge     start over (e.g. after changing the rubric)
        #   --judge-only  only judge the answers that have no verdict yet
        if "--rejudge" in sys.argv:
            save_json(EVAL / "judge.json", {})
        print("Judging saved answers only; retrieval numbers are kept from the last full run.\n")
    else:
        retriever = Retriever()
        per_question_hits = evaluate_retrieval(questions, retriever, query_vectors(questions))

    answers = asyncio.run(run_agent(questions))
    verdicts = asyncio.run(run_judge(questions, answers))

    missing = [q["id"] for q in questions if q["id"] not in answers]
    if missing:
        print(f"Not answered yet: {', '.join(missing)}. Results below cover the rest.\n")
        questions = [q for q in questions if q["id"] in answers]

    table, grading = [], []
    for q in questions:
        run, v = answers[q["id"]], verdicts.get(q["id"], {})
        checks = code_checks(q, run)
        stats = run.get("stats") or {}
        table.append({"id": q["id"], "kind": q["kind"], "question": q["question"],
                      **checks, "judge_correct": v.get("correct"), "judge_supported": v.get("supported"),
                      "judge_reasoning": v.get("reasoning"),
                      "guardrail": json.dumps(stats.get("guardrail")) if stats.get("guardrail") else "",
                      "seconds": stats.get("seconds"),
                      "tokens": (stats.get("input_tokens") or 0) + (stats.get("output_tokens") or 0),
                      "failure_cause": ""})  # TODO (Allan): fill in for each failure
        grading.append({"id": q["id"], "question": q["question"], "reference_answer": q["reference_answer"],
                        "answer": run["answer"],
                        "retrieved": "; ".join(f"{s}, {l}" for s, l in sorted(retrieved_citations(run["trace"])))})
    write_csv(OUT / "results.csv", table)
    if not RUN_NAME:
        write_csv(EVAL / "for_grading.csv", grading)  # no verdicts in it: grade blind

    answerable = [r for r in table if r["kind"] != "unanswerable"]
    unanswerable = [r for r in table if r["kind"] == "unanswerable"]
    n = len(table)

    # Three answers, not two (vision API notebook): answer, refuse, or escalate to a person
    # (the guardrail's "Answer withheld"). Coverage = answerable questions answered without
    # escalation or refusal; accuracy on covered = how many of those the judge marked correct.
    covered = [r for r in answerable if not r["refused"] and not r["withheld_by_guardrail"]]
    judged_covered = [r for r in covered if r["judge_correct"] is not None]

    judged = [r for r in table if r["judge_correct"] is not None]
    judge_values = [int(bool(r["judge_correct"])) for r in judged]
    labels = {l["id"]: l for l in read_csv(EVAL / "human_labels.csv")} if not RUN_NAME else {}
    human_values = [int(labels[r["id"]]["correct"]) for r in table
                    if r["id"] in labels and labels[r["id"]].get("correct", "").strip() in ("0", "1")]

    noise = {
        "judge_correct_rate": round(sum(judge_values) / len(judge_values), 3) if judge_values else None,
        "judge_correct_ci": bootstrap_ci(judge_values),
        "human_correct_rate": round(sum(human_values) / len(human_values), 3) if human_values else None,
        "human_correct_ci": bootstrap_ci(human_values),
    }
    if per_question_hits:
        for k in KS:
            hits = [int(h) for h in per_question_hits[(DESIGN, k)]]
            noise[f"hit@{k}_{DESIGN}_ci"] = bootstrap_ci(hits)
        for other in DESIGNS:
            if other != DESIGN:
                a = [int(h) for h in per_question_hits[(DESIGN, 3)]]
                b = [int(h) for h in per_question_hits[(other, 3)]]
                noise[f"hit@3 {DESIGN} minus {other}"] = paired_diff_ci(a, b)

    summary = {
        "questions": n,
        "judged": sum(r["judge_correct"] is not None for r in table),
        "correct (judge)": sum(bool(r["judge_correct"]) for r in table),
        "answerable correct (judge)": sum(bool(r["judge_correct"]) for r in answerable),
        "unsupported (judge)": sum(r["judge_supported"] is False for r in table),
        "correct refusals": sum(r["refused"] for r in unanswerable),
        "answered an unanswerable question": sum(not r["refused"] for r in unanswerable),
        "wrong refusals": sum(r["refused"] for r in answerable),
        "withheld by numbers guardrail": sum(r["withheld_by_guardrail"] for r in table),
        "code checks passed": sum(r["code_pass"] for r in table),
        "invalid citations": sum(not r["citations_valid"] for r in table),
        "mean seconds per question": round(sum(r["seconds"] or 0 for r in table) / n, 1),
        "mean tokens per question": round(sum(r["tokens"] for r in table) / n),
        "coverage (answerable answered, not refused or withheld)": f"{len(covered)}/{len(answerable)}",
        "accuracy on covered (judge)": f"{sum(bool(r['judge_correct']) for r in judged_covered)}/{len(judged_covered)}",
        "judge_agreement": agreement(verdicts, read_csv(EVAL / "human_labels.csv")) if not RUN_NAME else {},
        "noise_95ci": noise,
        "versions": versions(answers),
    }
    if RUN_NAME:
        summary["compared_with_main_run"] = compare_with_main(questions, verdicts)
    save_json(OUT / "summary.json", summary)
    for key, value in summary.items():
        if key not in ("judge_agreement", "noise_95ci", "versions", "compared_with_main_run"):
            print(f"{key:<36} {value}")

    print("\nNoise (bootstrap 95% intervals over the questions):")
    print(f"  judge correct      {noise['judge_correct_rate'] if noise['judge_correct_rate'] is None else format(noise['judge_correct_rate'], '.0%')}"
          f"  ({fmt_ci(noise['judge_correct_ci'])})")
    if human_values:
        print(f"  your grades        {noise['human_correct_rate']:.0%}  ({fmt_ci(noise['human_correct_ci'])})")
    for key, ci in noise.items():
        if " minus " in key and ci:
            print(f"  {key:<34} {ci[0]:+.0%} to {ci[1]:+.0%}")
        elif key.startswith("hit@") and ci:
            print(f"  {key:<34} {fmt_ci(ci)}")

    v = summary["versions"]
    log_run({
        "time": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "run": RUN_NAME or "main", "note": arg("--note") or "", **v,
        "questions": n, "judged": len(judged),
        "judge_correct": sum(judge_values), "judge_correct_ci": noise["judge_correct_ci"],
        "human_correct": sum(human_values) if human_values else "", "human_correct_ci": noise["human_correct_ci"] or "",
        "unsupported": summary["unsupported (judge)"], "correct_refusals": summary["correct refusals"],
        "wrong_refusals": summary["wrong refusals"], "withheld": summary["withheld by numbers guardrail"],
        "coverage": summary["coverage (answerable answered, not refused or withheld)"],
        "accuracy_on_covered": summary["accuracy on covered (judge)"],
        "invalid_citations": summary["invalid citations"],
        f"hit@3_{DESIGN}": (round(sum(per_question_hits[(DESIGN, 3)]) / len(per_question_hits[(DESIGN, 3)]), 3)
                            if per_question_hits else ""),
        "mean_seconds": summary["mean seconds per question"], "mean_tokens": summary["mean tokens per question"],
    })
    where = OUT.relative_to(ROOT)
    print(f"\nPer question: {where}/results.csv. Run logged in eval/runs.csv."
          + ("" if RUN_NAME else " For your own grades: eval/for_grading.csv."))


if __name__ == "__main__":
    sys.exit(main())
