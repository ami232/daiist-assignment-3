"""
Evaluation (`main.py evaluate`). Writes everything to eval/.

1. Retrieval: hit@k, all@k (every expected passage) and MRR@5 per design and
   question kind, for w150, w400, BM25 alone and a w150 BM25+dense hybrid -> eval/retrieval.csv
2. Agent on every question (cached, so reruns are cheap)    -> eval/answers.jsonl
3. Code checks: citations valid, refusals right or wrong
4. LLM judge with a rubric, retrieved text as evidence      -> eval/judge.jsonl
5. Agreement with my grades in eval/human_labels.csv, and a grading sheet
   for the answers I haven't graded                         -> eval/grading_sheet.md
6. Optional: add a document and re-ask one unanswerable question -> eval/add_document_demo.md
Totals and the analysis (rates with 95% intervals, refusals, cost...) go to eval/summary.json;
failed questions to eval/failures.csv. Nothing calls Gemini when every answer, verdict and
query vector is already cached.

Options: `--rejudge` judges every answer again (eval/judge_rerun.jsonl) to measure how stable
the judge is; EVAL_DIR=eval/v2 writes a complete second run into another folder.
"""

import asyncio
import csv
import json
import math
import os
import re
import statistics
import sys
import time
from collections import Counter
from pathlib import Path

import httpx
from google.genai import errors, types

import agent
import index

ROOT = Path(__file__).resolve().parent
DATA = ROOT / "eval"                              # test set and saved query vectors, shared by every run
EVAL = ROOT / os.environ.get("EVAL_DIR", "eval")  # run outputs; EVAL_DIR=eval/v2 for the v2 experiment
PRIMARY = EVAL.resolve() == DATA.resolve()        # the v1 run that my labels and the demo refer to
QUESTIONS = DATA / "questions.csv"
QUERY_VECS = DATA / "query_vectors.json"
ANSWERS = EVAL / "answers.jsonl"
JUDGE = EVAL / "judge.jsonl"
JUDGE_RERUN = EVAL / "judge_rerun.jsonl"          # second, independent judge pass (`--rejudge`)
KS = (1, 3, 5)

# Cost: USD per 1M tokens, paid tier of the Gemini Developer API (ai.google.dev/pricing, checked 23 Nov 2026).
# The free tier used for this project costs nothing; these prices show what the same traffic would cost.
PRICE_USD = {"agent_input": 0.25, "agent_output": 1.50, "embedding_input": 0.20}
USD_PER_EUR = 1.0990       # ECB euro reference rate, 20 Nov 2026
TOKENS_PER_WORD_MAX = 2    # assumed upper bound to price query embeddings, whose tokens are not logged
SLOW_RUN_S = 100           # runs slower than this are counted as rate-limit waits when estimating latency

REFUSAL_WORDS = re.compile(r"\b(?:does not|doesn't|do not) (?:cover|specify|mention|contain|provide|define)\b", re.IGNORECASE)
VERSION_NOTE = re.compile(r"(?:based on|according to)[^.\n]{0,60}\b20(?:19|20|22)\b|\b20(?:19|20|22) (?:consolidated|EASA)",
                          re.IGNORECASE)

# Before/after demo: an unanswerable question and a file that answers it.
# Leave as None until both are chosen.
DEMO_ID = "q31"  # U-space services: not in the corpus
DEMO_FILE = "eval/extra/reg_2021_664_u-space.html"  # Regulation (EU) 2021/664

RUBRIC = """You grade answers from an EU drone-rules assistant.

Question: {question}
Reference answer: {reference}
Retrieved passages (the only evidence the assistant had):
<<<
{evidence}
>>>
Assistant's answer:
<<<
{answer}
>>>

Grade two things, each 1 or 0:
- correct: 1 if the answer states the same rule as the reference (wording may differ;
  extra correct detail is fine). 0 if it contradicts the reference, misses its key point,
  or refuses although the reference gives an answer.
- supported: 1 if every factual claim in the answer appears in the retrieved passages.
  0 if any claim (a number, condition, exception) is not in them, even if it is true.

Reply with JSON only: {{"correct": 0 or 1, "supported": 0 or 1, "reason": "one sentence"}}"""


def read_csv(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if (r.get("id") or "").strip()]


def read_jsonl(path: Path) -> dict:
    if not path.is_file():
        return {}
    rows = [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]
    return {r["id"]: r for r in rows}


def append_jsonl(path: Path, row: dict) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def expected(q: dict) -> list[tuple[str, str]]:
    """(source, location) pairs; ';' separates several in both columns."""
    srcs = [s.strip() for s in q["expected_source"].split(";")]
    locs = [l.strip() for l in q["expected_location"].split(";")]
    if len(srcs) == 1 and len(locs) > 1:
        srcs *= len(locs)
    return list(zip(srcs, locs + [""] * (len(srcs) - len(locs))))


def is_hit(hit: dict, exp: list[tuple[str, str]]) -> bool:
    return any(hit["source"] == s and index.loc_match(l, hit["location"]) for s, l in exp)


# ---------- 1. retrieval ----------

def query_vectors(questions: list[dict]) -> dict:
    """One embedding per question text, saved to disk and shared by all designs."""
    vecs = json.loads(QUERY_VECS.read_text()) if QUERY_VECS.is_file() else {}
    todo = [q for q in questions if q["question"] not in vecs]
    for i in range(0, len(todo), index.BATCH):
        batch = todo[i:i + index.BATCH]
        for q, v in zip(batch, index.embed([q["question"] for q in batch], task="RETRIEVAL_QUERY")):
            vecs[q["question"]] = v
        QUERY_VECS.write_text(json.dumps(vecs))
    return vecs


CORPUS = [s["source"] for s in index.SOURCES]  # what the test set was written for; added documents are left out


def retrievers() -> dict:
    """Design name -> search(question, query_vec), over the corpus documents only, so every design
    searches the same text. BM25 needs no vectors; the hybrid reuses the stored w150 ones."""
    designs = {d: (lambda q, v, d=d: index.retrieve(q, d, k=max(KS), query_vec=v, sources=CORPUS))
               for d in index.DESIGNS}
    designs["bm25"] = lambda q, v: index.retrieve_bm25(q, "w150", k=max(KS), sources=CORPUS)
    designs["w150+bm25"] = lambda q, v: index.retrieve_hybrid(q, "w150", k=max(KS), query_vec=v, sources=CORPUS)
    return designs


def retrieval(questions: list[dict]) -> list[dict]:
    """One row per design and question kind (all / single / multi):
    hit@k = any expected passage in the top k; all@k = every expected passage in the top k;
    mrr@5 = mean of 1 / rank of the first expected passage (0 if not in the top 5)."""
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    vecs = query_vectors(answerable)
    rows = []
    for design, search in retrievers().items():
        per_q = []
        for q in answerable:
            hits, exp = search(q["question"], vecs[q["question"]]), expected(q)
            rank = next((r for r, h in enumerate(hits, start=1) if is_hit(h, exp)), None)
            per_q.append({"kind": q["kind"], "rank": rank, "words": sum(len(h["text"].split()) for h in hits),
                          "all": {k: all(any(is_hit(h, [e]) for h in hits[:k]) for e in exp) for k in KS}})
        for kind in ("all", "single", "multi"):
            sel = [p for p in per_q if kind == "all" or p["kind"] == kind]
            n = len(sel)
            if not n:
                continue
            rows.append({"design": design, "questions": kind, "n": n,
                         **{f"hit@{k}": round(sum(p["rank"] is not None and p["rank"] <= k for p in sel) / n, 3)
                            for k in KS},
                         **{f"all@{k}": round(sum(p["all"][k] for p in sel) / n, 3) for k in KS},
                         "mrr@5": round(sum(1 / p["rank"] for p in sel if p["rank"]) / n, 3),
                         "avg_words_top5": round(sum(p["words"] for p in sel) / n)})
    with (EVAL / "retrieval.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]), lineterminator="\n")
        w.writeheader()
        w.writerows(rows)
    return rows


# ---------- 2-4. agent, code checks, judge ----------

def answer_all(questions: list[dict]) -> dict:
    done = read_jsonl(ANSWERS)
    for q in questions:
        if q["id"] in done:
            continue
        print(f"  asking {q['id']}", file=sys.stderr)
        try:
            r = asyncio.run(agent.run(q["question"], approve=lambda *_: False))
        except Exception as e:
            # MCP wraps errors in exception groups; dig out the real one
            while getattr(e, "exceptions", None):
                e = e.exceptions[0]
            if "RESOURCE_EXHAUSTED" in str(e) or "429" in str(e):
                raise SystemExit(f"Gemini quota exhausted at {q['id']}. Answers so far are saved; rerun later to continue.")
            raise
        done[q["id"]] = {"id": q["id"], **r}
        append_jsonl(ANSWERS, done[q["id"]])  # saved one by one so a rerun resumes here
    return done


def code_checks(q: dict, a: dict) -> dict:
    refused = a["answer"].strip().startswith(agent.REFUSED_PREFIX)
    passages = [tuple(p) for p in a["passages"]]
    return {
        "refused": refused,
        "citations_valid": not agent.check_citations(a["answer"], passages),
        "retrieved_expected": q["kind"] == "unanswerable"
        or any(is_hit({"source": s, "location": l}, expected(q)) for s, l in passages),
    }


def judge(q: dict, a: dict) -> dict:
    prompt = RUBRIC.format(question=q["question"], reference=q["reference_answer"],
                           evidence=a["retrieved_text"][:20000] or "(nothing retrieved)", answer=a["answer"])
    for attempt in range(10):  # the free tier can answer 503 "high demand" for a while; retry often, up to ~7 min
        try:
            res = index.client().models.generate_content(
                model=agent.MODEL, contents=prompt,
                config=types.GenerateContentConfig(temperature=0, response_mime_type="application/json"))
            break
        except (errors.ServerError, errors.ClientError, httpx.TransportError) as e:
            # retry rate limits, "high demand" and dropped connections; anything else is a real error
            if getattr(e, "code", 503) not in (429, 503) or attempt == 9:
                raise
            time.sleep(min(10 * 2 ** attempt, 60))
    v = json.loads(res.text)
    return {"id": q["id"], "correct": int(v["correct"]), "supported": int(v["supported"]), "reason": v.get("reason", "")}


def grade_all(questions: list[dict], answers: dict) -> list[dict]:
    verdicts = read_jsonl(JUDGE)
    results = []
    for q in questions:
        a, c = answers[q["id"]], code_checks(q, answers[q["id"]])
        if q["kind"] == "unanswerable" or c["refused"]:
            # refusals are graded in code: right if unanswerable, wrong otherwise
            v = {"correct": int((q["kind"] == "unanswerable") == c["refused"]), "supported": 1, "reason": "graded in code"}
        else:
            if q["id"] not in verdicts:
                verdicts[q["id"]] = judge(q, a)
                append_jsonl(JUDGE, verdicts[q["id"]])
            v = verdicts[q["id"]]
        results.append({"id": q["id"], "kind": q["kind"], **c, "correct": v["correct"],
                        "supported": v["supported"], "reason": v["reason"], "guardrail": a["guardrail"],
                        "tokens": a["input_tokens"] + a["output_tokens"], "seconds": a["seconds"]})
    return results


def outcome(r: dict) -> str:
    if r["kind"] == "unanswerable":
        return "correct refusal" if r["refused"] else "answered unanswerable"
    if r["refused"]:
        return "wrong refusal"
    if not r["supported"]:
        return "unsupported"
    return "correct" if r["correct"] else "wrong"


# ---------- 4b. analysis of a run (no API calls) ----------

def wilson(k: int, n: int, z: float = 1.96) -> list[float]:
    """95% Wilson score interval for k successes out of n."""
    p, d = k / n, 1 + z * z / n
    centre, half = (p + z * z / (2 * n)) / d, z * math.sqrt(p * (1 - p) / n + z * z / (4 * n * n)) / d
    return [round(max(0.0, centre - half), 3), round(min(1.0, centre + half), 3)]


def guardrail_patterns(note: str) -> list[str]:
    """Why a first draft failed the citation check, from the guardrail note."""
    if "has no [source, location] citations" in note:
        return ["no citations (refusal without the exact phrase)"]
    found = set()
    for cited in re.findall(r"\[([^\[\]]+)\] does not match", note):
        if re.match(r"\d+, ", cited):
            found.add("passage number as source")
        elif ";" in cited:
            found.add("two citations in one bracket")
        elif cited.count(", ") >= 2:
            found.add("two locations after one source")
        elif re.search(r"\(\d", cited.split(", ", 1)[-1]):
            found.add("location finer than the stored one")
        else:
            found.add("other")
    return sorted(found)


def agent_retrieval(questions: list[dict], answers: dict) -> dict:
    """Did the agent's own searches return the expected passages? (answerable questions)"""
    rows = []
    for q in questions:
        if q["kind"] == "unanswerable":
            continue
        got = [{"source": s, "location": loc} for s, loc in answers[q["id"]]["passages"]]
        found = [any(is_hit(h, [e]) for h in got) for e in expected(q)]
        rows.append({"id": q["id"], "kind": q["kind"], "any": any(found), "all": all(found)})
    return {"answerable": len(rows), "any_expected": sum(r["any"] for r in rows),
            "all_expected": sum(r["all"] for r in rows),
            "multi_with_all_expected": [r["id"] for r in rows if r["kind"] == "multi" and r["all"]],
            "missed_an_expected_passage": [r["id"] for r in rows if not r["all"]],
            "missed_every_expected_passage": [r["id"] for r in rows if not r["any"]]}


def analysis(results: list[dict], answers: dict) -> dict:
    """Breakdowns for the report: outcomes by kind, 95% intervals, refusals, the version note,
    guardrail patterns, tokens, latency and cost. Everything comes from the cached run."""
    n = len(results)
    answerable = [r for r in results if r["kind"] != "unanswerable"]
    unanswerable = [r for r in results if r["kind"] == "unanswerable"]
    rates = {"handled_correctly": (sum(r["outcome"] in ("correct", "correct refusal") for r in results), n),
             "correct_of_answerable": (sum(r["outcome"] == "correct" for r in answerable), len(answerable)),
             "unsupported_of_answerable": (sum(r["outcome"] == "unsupported" for r in answerable), len(answerable)),
             "refused_of_unanswerable": (sum(r["outcome"] == "correct refusal" for r in unanswerable),
                                         len(unanswerable)),
             "citations_valid": (sum(r["citations_valid"] for r in results), n)}
    text = {r["id"]: answers[r["id"]]["answer"] for r in results}
    prefix = sorted(i for i, t in text.items() if t.strip().startswith(agent.REFUSED_PREFIX))
    other_words = sorted(i for i, t in text.items() if i not in prefix and REFUSAL_WORDS.search(t.split("\n")[0]))
    partial = sorted(i for i, t in text.items() if i not in prefix + other_words and REFUSAL_WORDS.search(t))
    verdicts = read_jsonl(JUDGE)
    note = sorted(i for i, t in text.items() if VERSION_NOTE.search(t))
    fired = {r["id"]: guardrail_patterns(r["guardrail"]) for r in results if r["guardrail"] != "passed"}
    tokens = [answers[i]["input_tokens"] + answers[i]["output_tokens"] for i in text]
    seconds = [answers[i]["seconds"] for i in text]
    slow = sorted(i for i in text if answers[i]["seconds"] > SLOW_RUN_S)
    mean_in = statistics.mean(answers[i]["input_tokens"] for i in text)
    mean_out = statistics.mean(answers[i]["output_tokens"] for i in text)
    searches = [c[1].get("query", "") for i in text for c in answers[i]["tool_calls"] if c[0] == "search"]
    blocked = sum(answers[i]["retrieved_text"].count("Tool call limit exceeded") for i in text)
    embed_tokens_max = TOKENS_PER_WORD_MAX * sum(len(q.split()) for q in searches) / n
    usd = {"agent": (mean_in * PRICE_USD["agent_input"] + mean_out * PRICE_USD["agent_output"]) / 1e6,
           "query_embeddings_max": embed_tokens_max * PRICE_USD["embedding_input"] / 1e6}
    eur = sum(usd.values()) / USD_PER_EUR
    return {
        "outcomes_by_kind": {k: dict(Counter(r["outcome"] for r in results if r["kind"] == k))
                             for k in ("single", "multi", "unanswerable")},
        "rates_wilson95": {k: {"k": a, "n": b, "rate": round(a / b, 3), "ci": wilson(a, b)}
                           for k, (a, b) in rates.items() if b},
        "refusals": {"exact_prefix": prefix, "refusal_in_other_words": other_words,
                     "partly_refused_answers": partial},
        "version_note": {"answers": len(note), "of": n, "judged_with_note": sum(i in verdicts for i in note),
                         "judged": len(verdicts),
                         "judged_with_note_unsupported": sorted(i for i in note if i in verdicts
                                                                and verdicts[i]["supported"] == 0)},
        "guardrail": {"fired": len(fired), "patterns": dict(Counter(p for ps in fired.values() for p in ps)),
                      "by_question": fired},
        "searches": {"requested": len(searches), "blocked": blocked, "executed": len(searches) - blocked},
        "tokens": {"mean": round(statistics.mean(tokens)), "median": statistics.median(tokens),
                   "mean_input": round(mean_in), "mean_output": round(mean_out)},
        "seconds": {"mean": round(statistics.mean(seconds), 1), "median": statistics.median(seconds),
                    f"mean_without_runs_over_{SLOW_RUN_S}s": round(statistics.mean(
                        answers[i]["seconds"] for i in text if i not in slow), 1),
                    "runs_over": slow},
        "cost_paid_tier": {"usd_per_question_agent": round(usd["agent"], 6),
                           "usd_per_question_query_embeddings_max": round(usd["query_embeddings_max"], 7),
                           "eur_per_question": round(eur, 6), "eur_per_1000_questions": round(eur * 1000, 2),
                           "usd_per_eur": USD_PER_EUR},
    }


# ---------- 5. agreement ----------

def kappa(pairs: list[tuple[int, int]]) -> float | None:
    """Cohen's kappa for 0/1 pairs; None when chance agreement is 1 (no variance), where it is undefined."""
    n = len(pairs)
    observed = sum(a == b for a, b in pairs) / n
    p_a, p_b = sum(a for a, _ in pairs) / n, sum(b for _, b in pairs) / n
    chance = p_a * p_b + (1 - p_a) * (1 - p_b)
    return None if chance == 1 else round((observed - chance) / (1 - chance), 3)


def agreement(results: list[dict]) -> dict:
    """Judge (or code) verdicts vs my grades, for however many rows human_labels.csv has.
    Rows without a 0/1 in both columns are skipped."""
    labelled = lambda h: all(str(h.get(f, "")).strip() in ("0", "1") for f in ("correct", "supported"))
    human = {h["id"]: h for h in read_csv(EVAL / "human_labels.csv") if labelled(h)}
    pairs = [(r, human[r["id"]]) for r in results if r["id"] in human]
    if not pairs:
        return {"graded_by_me": 0}
    out = {"graded_by_me": len(pairs)}
    for f in ("correct", "supported"):
        both = [(int(h[f]), r[f]) for r, h in pairs]
        out[f"agree_{f}"] = round(sum(a == b for a, b in both) / len(both), 3)
        out[f"kappa_{f}"] = kappa(both)
    out["disagreements"] = sorted(r["id"] for r, h in pairs
                                  if int(h["correct"]) != r["correct"] or int(h["supported"]) != r["supported"])
    return out


def rejudge(questions: list[dict], answers: dict) -> None:
    """Judge every judged answer a second time, cached in judge_rerun.jsonl. Opt-in, it spends quota."""
    first, again = read_jsonl(JUDGE), read_jsonl(JUDGE_RERUN)
    for q in questions:
        if q["id"] in first and q["id"] not in again:
            print(f"  re-judging {q['id']}", file=sys.stderr)
            again[q["id"]] = judge(q, answers[q["id"]])
            append_jsonl(JUDGE_RERUN, again[q["id"]])


def judge_stability() -> dict:
    """How often the second judge pass disagrees with the first."""
    first, again = read_jsonl(JUDGE), read_jsonl(JUDGE_RERUN)
    both = [i for i in first if i in again]
    if not both:
        return {"rejudged": 0}
    flips = {f: sorted(i for i in both if first[i][f] != again[i][f]) for f in ("correct", "supported")}
    return {"rejudged": len(both), "flips_correct": flips["correct"], "flips_supported": flips["supported"],
            "flip_rate": round(len(set(flips["correct"]) | set(flips["supported"])) / len(both), 3)}


# ---------- 5b. grading sheet for the answers I haven't graded ----------

PASSAGE_LINE = re.compile(r"^(?:\[\d+\] .+? \(score [\d.\-]+\)|Passage \d+ \(score [\d.\-]+\)\. Cite as: .+)$", re.MULTILINE)


def split_passages(retrieved_text: str) -> list[tuple[str, str]]:
    """(header, text) for each distinct passage the searches returned, in order."""
    heads = list(PASSAGE_LINE.finditer(retrieved_text))
    out, seen = [], set()
    for i, h in enumerate(heads):
        body = retrieved_text[h.end():heads[i + 1].start() if i + 1 < len(heads) else len(retrieved_text)]
        body = body.split("Tool call limit exceeded")[0].strip()
        key = (re.sub(r"^\[\d+\] |\(score [\d.\-]+\)", "", h.group(0)), body[:80])
        if key not in seen:
            seen.add(key)
            out.append((h.group(0), body))
    return out


def write_grading_sheet(questions: list[dict], answers: dict) -> None:
    """eval/grading_sheet.md: every answer not yet in human_labels.csv, with no judge verdicts."""
    graded = {h["id"] for h in read_csv(EVAL / "human_labels.csv")}
    todo = [q for q in questions if q["id"] not in graded]
    lines = ["# Grading sheet", "",
             "Answers not yet in `eval/human_labels.csv`, generated by `main.py evaluate`. No judge verdicts here:",
             "grade each one before looking at `eval/judge.jsonl`, then add a row to `human_labels.csv`.", "",
             ("- **correct** = 1 if the answer states the same rule as the reference, or properly says the corpus "
              "does not cover it."),
             "- **supported** = 1 if every claim is in the retrieved passages.",
             "- **notes**: why, for every 0.", ""]
    if not todo:
        lines.append("Every answer is graded.")
    for q in todo:
        a = answers[q["id"]]
        expected_text = "; ".join(f"{s}, {loc}" for s, loc in expected(q)) if q["expected_source"].strip() else "none"
        searches = ", ".join(f"`{c[1].get('query', '')}`" for c in a["tool_calls"] if c[0] == "search") or "none"
        lines += [f"## {q['id']} ({q['kind']})", "", f"**Question:** {q['question']}", "",
                  f"**Reference answer:** {q['reference_answer']}", "", f"**Expected passages:** {expected_text}", "",
                  f"**Searches:** {searches}", "", "**Retrieved passages:**", ""]
        for head, body in split_passages(a["retrieved_text"]):
            lines += [f"<details><summary>{head}</summary>", "", body, "", "</details>", ""]
        lines += ["**Agent's answer:**", ""] + [f"> {ln}" if ln else ">" for ln in a["answer"].split("\n")]
        lines += ["", f"**My grade:** `{q['id']},correct,supported,notes` → `{q['id']},_,_,_`", ""]
    (EVAL / "grading_sheet.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


# ---------- 6. add-document demo ----------

def add_document_demo(questions: list[dict], answers: dict) -> None:
    if not (DEMO_ID and DEMO_FILE):
        return
    q = next(q for q in questions if q["id"] == DEMO_ID)
    out = EVAL / "add_document_demo.md"
    if out.is_file():
        return  # done already; delete the file to redo it
    import server  # same code path the MCP tool uses
    added = server.add_document(str(ROOT / DEMO_FILE))
    after = asyncio.run(agent.run(q["question"], approve=lambda *_: False))
    out.write_text(
        f"# Add-document demo\n\n**Question ({q['id']}):** {q['question']}\n\n"
        f"## Before\n\n{answers[q['id']]['answer']}\n\n"
        f"## add_document\n\n{added}\n\n## After\n\n{after['answer']}\n", encoding="utf-8")


def main() -> None:
    questions = read_csv(QUESTIONS)
    if not questions:
        raise SystemExit("eval/questions.csv has no questions yet.")
    EVAL.mkdir(parents=True, exist_ok=True)

    print("Retrieval (hit rate):")
    for row in retrieval(questions):
        print("  ", row)

    print("\nAnswering every question with the agent...")
    answers = answer_all(questions)
    results = grade_all(questions, answers)
    if "--rejudge" in sys.argv:
        rejudge(questions, answers)

    for r in results:
        r["outcome"] = outcome(r)
    counts = {o: sum(r["outcome"] == o for r in results) for o in
              ["correct", "wrong", "unsupported", "wrong refusal", "correct refusal", "answered unanswerable"]}
    n = len(results)
    summary = {
        "questions": n,
        "outcomes": counts,
        "citations_valid": round(sum(r["citations_valid"] for r in results) / n, 3),
        "guardrail_fired": sum(r["guardrail"] != "passed" for r in results),
        "avg_tokens": round(sum(r["tokens"] for r in results) / n),
        "avg_seconds": round(sum(r["seconds"] for r in results) / n, 1),
        "judge_vs_me": agreement(results),
        "judge_stability": judge_stability(),
        "analysis": {**analysis(results, answers), "agent_retrieval": agent_retrieval(questions, answers)},
    }
    (EVAL / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    failed = [r for r in results if r["outcome"] not in ("correct", "correct refusal")]
    # `cause` is filled in by hand; keep what is already there when this reruns
    causes = {r["id"]: r.get("cause", "") for r in read_csv(EVAL / "failures.csv")}
    with (EVAL / "failures.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["id", "kind", "outcome", "retrieved_expected", "reason", "cause"],
                           lineterminator="\n")
        w.writeheader()
        for r in failed:
            w.writerow({**{k: r.get(k, "") for k in w.fieldnames}, "cause": causes.get(r["id"], "")})

    if PRIMARY:  # the demo and my grades belong to the v1 run
        add_document_demo(questions, answers)
        write_grading_sheet(questions, answers)
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
