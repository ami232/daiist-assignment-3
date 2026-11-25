"""
Assignment 3: evaluation (`main.py evaluate`).

1. Retrieval: hit rate at k = 1, 3, 5 for each design (dense, BM25, hybrid,
   hybrid restricted to articles) and the words each adds to the prompt.
   -> eval/retrieval.csv
2. End to end: the agent answers every question. Answers are cached in
   eval/answers.jsonl (pass --fresh to run them all again).
3. Code checks: refusal on unanswerable questions, wrong refusals, citations
   that match a retrieved passage, expected passage retrieved and cited.
4. LLM judge with a rubric and the retrieved passages as evidence.
   -> eval/judge.csv (cached per answer)
5. Agreement between the judge and eval/human_labels.csv.
6. Before/after: add Regulation (EU) 2018/1807 with the add_document tool to
   a temporary copy of the index and ask the unanswerable question again.
   -> eval/before_after.md (the committed index stays unchanged)
7. Failure causes, cost and latency. -> eval/results.csv, eval/summary.md/json

Grade answers yourself, without seeing the judge, with:
    uv run python evaluate.py --label
"""

from __future__ import annotations

import argparse
import asyncio
import csv
import hashlib
import json
import os
import shutil
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
ANSWERS = EVAL / "answers.jsonl"
JUDGE = EVAL / "judge.csv"
HUMAN = EVAL / "human_labels.csv"
OVERRIDES = EVAL / "failure_overrides.csv"  # optional: id,cause to correct the automatic failure cause
RESULTS = EVAL / "results.csv"
RETRIEVAL = EVAL / "retrieval.csv"
SUMMARY_MD = EVAL / "summary.md"
SUMMARY_JSON = EVAL / "summary.json"
BEFORE_AFTER = EVAL / "before_after.md"

JUDGE_MODEL = os.environ.get("JUDGE_MODEL", os.environ.get("GEMINI_MODEL", "gemini-3.6-flash"))
PRICE_IN, PRICE_OUT = 0.30, 2.50  # USD per million tokens on the paid tier, for the cost estimate
KS = (1, 3, 5)
DESIGNS = {
    "dense": {"mode": "dense"},
    "bm25": {"mode": "bm25"},
    "hybrid": {"mode": "hybrid"},
    "hybrid_articles_only": {"mode": "hybrid", "kind": "article"},
}
ADD_DOC = {
    "name": "FreeFlow",
    "title": "Regulation (EU) 2018/1807 - free flow of non-personal data",
    "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32018R1807",
    "question_id": "q36",
}

RUBRIC = """You are grading an answer from a compliance assistant that must answer only from \
retrieved passages of EU data-protection law.

Question: {question}
Question type: {kind}
Reference answer (written by a person from the law): {reference}

Retrieved passages (the only evidence the assistant had):
{evidence}

Assistant's answer:
{answer}

Grade two things, each 1 or 0.

correct = 1 when
- the question is answerable: the answer states the key facts of the reference (deadline, \
amount, threshold, condition or list) and contradicts none of them. Missing minor detail is fine; \
a wrong number, date, threshold or condition, or missing the main point, is 0. A refusal is 0.
- the question is unanswerable: the answer says the corpus does not cover it and gives no \
substantive answer from outside knowledge. Pointing to the closest related passage is fine.

supported = 1 when every factual claim in the answer is stated in, or follows directly from, the \
retrieved passages above. A claim from outside knowledge is unsupported even if it is true. \
A pure refusal is supported.

Reply with JSON only: {{"correct": 0 or 1, "supported": 0 or 1, "reason": "one sentence"}}"""


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


# ------------------------------------------------------------------ files


def read_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if (r.get("question") or "").strip()]
    for r in rows:
        r["kind"] = r["kind"].strip().lower()
    return rows


def load_jsonl(path: Path) -> dict:
    out = {}
    if path.is_file():
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                item = json.loads(line)
                out[item["id"]] = item
    return out


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    fields = list(rows[0].keys())
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def expected_pairs(row: dict) -> list[tuple[str, str]]:
    sources = [s.strip() for s in row["expected_source"].split(";") if s.strip()]
    locations = [s.strip() for s in row["expected_location"].split(";") if s.strip()]
    if len(sources) == 1 and len(locations) > 1:
        sources = sources * len(locations)
    if len(locations) == 1 and len(sources) > 1:
        locations = locations * len(sources)
    return list(zip(sources, locations))


def same_place(source: str, location: str, pair: tuple[str, str]) -> bool:
    from agent import _same_location

    return source.lower() == pair[0].lower() and _same_location(location, pair[1])


# ------------------------------------------------------------------ 1. retrieval


def evaluate_retrieval(rows: list[dict], store) -> tuple[list[dict], dict]:
    from retrieval import DEFAULT_MODE

    answerable = [r for r in rows if r["kind"] != "unanswerable"]
    multi = [r for r in answerable if r["kind"] == "multi"]
    table, chosen_hits = [], {}
    for name, cfg in DESIGNS.items():
        hits = {k: 0 for k in KS}
        all_found = 0
        added_words = []
        for r in answerable:
            results = store.search(r["question"], k=max(KS), mode=cfg["mode"], kind=cfg.get("kind"))
            pairs = expected_pairs(r)
            for k in KS:
                if any(same_place(h["source"], h["location"], p) for h in results[:k] for p in pairs):
                    hits[k] += 1
            found_all = all(any(same_place(h["source"], h["location"], p) for h in results[:5]) for p in pairs)
            if r["kind"] == "multi" and found_all:
                all_found += 1
            added_words.append(sum(len(h["text"].split()) for h in results[:5]))
            if name == DEFAULT_MODE:
                chosen_hits[r["id"]] = int(any(same_place(h["source"], h["location"], p)
                                              for h in results[:5] for p in pairs))
        n = len(answerable)
        table.append({
            "design": name,
            **{f"hit@{k}": round(hits[k] / n, 3) for k in KS},
            "multi_both_found@5": f"{all_found}/{len(multi)}",
            "avg_words_added_k5": round(sum(added_words) / n),
        })
    write_csv(RETRIEVAL, table)
    return table, chosen_hits


# ------------------------------------------------------------------ 2. agent


def deny(path: str) -> bool:
    log(f"[approval] add_document({path!r}) denied during evaluation")
    return False


def run_agent(rows: list[dict], fresh: bool) -> dict:
    import agent

    if fresh and ANSWERS.exists():
        ANSWERS.unlink()
    answers = load_jsonl(ANSWERS)
    for r in rows:
        if r["id"] in answers or os.environ.get("EVAL_CACHED_ONLY"):  # partial run: only use saved answers
            continue
        log(f"[{r['id']}] {r['question']}")
        try:
            result = agent.answer(r["question"], approve_fn=deny)
        except Exception as error:  # noqa: BLE001 - one failed question should not stop the run
            log(f"  failed: {type(error).__name__}: {error}")
            continue
        result["id"] = r["id"]
        answers[r["id"]] = result
        with ANSWERS.open("a", encoding="utf-8") as f:
            f.write(json.dumps(result, ensure_ascii=False) + "\n")
        time.sleep(25)  # stay under the free-tier requests per minute
    return answers


# ------------------------------------------------------------------ 3. code checks


def code_checks(row: dict, res: dict) -> dict:
    unanswerable = row["kind"] == "unanswerable"
    refused = bool(res.get("refused"))
    pairs = expected_pairs(row)
    retrieved_expected = cited_expected = ""
    if pairs:
        retrieved_expected = int(any(same_place(c["source"], c["location"], p)
                                     for c in res.get("retrieved", []) for p in pairs))
        cited = [c.split(",", 1) for c in res.get("citations", []) if "," in c]
        cited_expected = int(any(same_place(s.strip(), l.strip(), p) for s, l in cited for p in pairs))
    return {
        "refused": int(refused),
        "correct_refusal": int(refused) if unanswerable else "",
        "wrong_refusal": int(refused) if not unanswerable else "",
        "has_valid_citation": int(bool(res.get("citations"))),
        "invalid_citations": len(res.get("invalid_citations", [])),
        "retrieved_expected": retrieved_expected,
        "cited_expected": cited_expected,
        "guardrail": res.get("guardrail") or "",
    }


# ------------------------------------------------------------------ 4. judge


def answer_hash(res: dict) -> str:
    return hashlib.sha1(res["answer"].encode("utf-8")).hexdigest()[:12]


def judge_one(row: dict, res: dict) -> dict:
    from google.genai import errors, types

    from index import gemini

    evidence = "\n\n".join(f"[{c['source']}, {c['location']}]\n{c['text']}" for c in res.get("retrieved", []))
    prompt = RUBRIC.format(question=row["question"], kind=row["kind"], reference=row["reference_answer"],
                           evidence=evidence or "(no passages were retrieved)", answer=res["answer"])
    for attempt in range(1, 6):
        try:
            response = gemini().models.generate_content(
                model=JUDGE_MODEL, contents=prompt,
                config=types.GenerateContentConfig(temperature=0, response_mime_type="application/json"),
            )
            data = json.loads(response.text)
            usage = response.usage_metadata
            return {
                "judge_correct": int(data["correct"]),
                "judge_supported": int(data["supported"]),
                "judge_reason": str(data.get("reason", "")).strip(),
                "judge_tokens": getattr(usage, "total_token_count", 0) or 0,
            }
        except (errors.ClientError, errors.ServerError) as error:
            if error.code in (429, 500, 503):
                log(f"  judge rate limited, waiting {30 * attempt}s")
                time.sleep(30 * attempt)
                continue
            raise
        except (ValueError, KeyError, TypeError):
            continue
    return {"judge_correct": "", "judge_supported": "", "judge_reason": "judge failed", "judge_tokens": 0}


def run_judge(rows: list[dict], answers: dict) -> dict:
    cached = {}
    if JUDGE.is_file():
        with JUDGE.open(newline="", encoding="utf-8") as f:
            cached = {r["id"]: r for r in csv.DictReader(f)}
    verdicts = {}
    for row in rows:
        res = answers.get(row["id"])
        if res is None:
            continue
        h = answer_hash(res)
        old = cached.get(row["id"])
        if old and old.get("answer_hash") == h and old.get("judge_correct") in ("0", "1"):
            verdicts[row["id"]] = {**old, "judge_correct": int(old["judge_correct"]),
                                   "judge_supported": int(old["judge_supported"])}
            continue
        log(f"[judge] {row['id']}")
        verdicts[row["id"]] = {"id": row["id"], "answer_hash": h, **judge_one(row, res)}
    write_csv(JUDGE, [verdicts[r["id"]] for r in rows if r["id"] in verdicts])
    return verdicts


# ------------------------------------------------------------------ 5. agreement


def agreement(verdicts: dict) -> dict:
    if not HUMAN.is_file():
        return {}
    with HUMAN.open(newline="", encoding="utf-8") as f:
        labels = {r["id"].strip(): r for r in csv.DictReader(f) if (r.get("id") or "").strip()}
    out = {}
    for dim in ("correct", "supported"):
        pairs, disagree = [], []
        for qid, label in labels.items():
            human = str(label.get(dim, "")).strip()
            machine = verdicts.get(qid, {}).get(f"judge_{dim}")
            if human in ("0", "1") and machine in (0, 1):
                pairs.append((int(human), machine))
                if int(human) != machine:
                    disagree.append(qid)
        if not pairs:
            continue
        n = len(pairs)
        po = sum(a == b for a, b in pairs) / n
        h1 = sum(a for a, _ in pairs) / n
        j1 = sum(b for _, b in pairs) / n
        pe = h1 * j1 + (1 - h1) * (1 - j1)
        kappa = 1.0 if pe == 1 else (po - pe) / (1 - pe)
        out[dim] = {"n": n, "agreement": round(po, 3), "cohen_kappa": round(kappa, 3), "disagree_on": disagree}
    return out


# ------------------------------------------------------------------ 6. before / after


async def call_tool(name: str, arguments: dict, env: dict) -> str:
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT), env=env)
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool(name, arguments)
            return "\n".join(getattr(c, "text", "") for c in result.content)


def before_after(rows: list[dict], answers: dict, fresh: bool) -> None:
    if BEFORE_AFTER.is_file() and not fresh:
        log("before/after already done (eval/before_after.md); pass --fresh to redo it")
        return
    import agent
    import index as pipeline

    row = next((r for r in rows if r["id"] == ADD_DOC["question_id"]), None)
    if row is None or row["id"] not in answers:
        log("before/after skipped: question or its first answer is missing")
        return
    before = answers[row["id"]]
    path = pipeline.download(ADD_DOC["name"], ADD_DOC["url"])

    tmp = Path(tempfile.mkdtemp(prefix="index-copy-"))
    shutil.copytree(pipeline.INDEX_DIR, tmp, dirs_exist_ok=True)
    env = {**os.environ, "CORPUS_INDEX_DIR": str(tmp)}
    previous = os.environ.get("CORPUS_INDEX_DIR")
    try:
        first = asyncio.run(call_tool("add_document", {"path": str(path)}, env))
        second = asyncio.run(call_tool("add_document", {"path": str(path)}, env))
        os.environ["CORPUS_INDEX_DIR"] = str(tmp)
        after = agent.answer(row["question"], approve_fn=deny)
    finally:
        if previous is None:
            os.environ.pop("CORPUS_INDEX_DIR", None)
        else:
            os.environ["CORPUS_INDEX_DIR"] = previous
        shutil.rmtree(tmp, ignore_errors=True)

    text = f"""# Adding a document: before and after

Question {row['id']}: **{row['question']}**

Document added: {ADD_DOC['title']} ({ADD_DOC['url']}), saved as `{path.relative_to(ROOT)}`, added with \
the server's `add_document` tool to a temporary copy of the index (the committed index is unchanged).

`add_document` result, first call: `{first}`

`add_document` result, second call with the same file: `{second}`

## Before

{before['answer']}

Citations: {', '.join(before.get('citations', [])) or 'none'}

## After

{after['answer']}

Citations: {', '.join(after.get('citations', [])) or 'none'}

Reference answer: {row['reference_answer']}
"""
    BEFORE_AFTER.write_text(text, encoding="utf-8")
    log("wrote eval/before_after.md")


# ------------------------------------------------------------------ 7. failures and summary


def failure_cause(row: dict, checks: dict, verdict: dict) -> str:
    """Automatic first guess; correct it in eval/failure_overrides.csv after reading the answers."""
    if row["kind"] == "unanswerable":
        return "" if checks["correct_refusal"] == 1 else "unsupported claim"
    correct, supported = verdict.get("judge_correct"), verdict.get("judge_supported")
    if checks["wrong_refusal"] == 1:
        return "wrong refusal" if checks["retrieved_expected"] == 1 else "retrieval miss"
    if correct == 1 and supported == 1:
        return ""
    if correct != 1 and checks["retrieved_expected"] != 1:
        return "retrieval miss"
    if supported == 0:
        return "unsupported claim"
    if correct == 0:
        return "wrong answer from right passage"
    return ""


def load_overrides() -> dict:
    if not OVERRIDES.is_file():
        return {}
    with OVERRIDES.open(newline="", encoding="utf-8") as f:
        return {r["id"].strip(): r["cause"].strip() for r in csv.DictReader(f) if (r.get("id") or "").strip()}


def summarise(rows, answers, verdicts, retrieval_table, chosen_hits, agree) -> dict:
    overrides = load_overrides()
    results = []
    for row in rows:
        res = answers.get(row["id"])
        if res is None:
            continue
        checks = code_checks(row, res)
        verdict = verdicts.get(row["id"], {})
        cause = overrides.get(row["id"], failure_cause(row, checks, verdict))
        results.append({
            "id": row["id"],
            "kind": row["kind"],
            "retrieval_hit@5": chosen_hits.get(row["id"], ""),
            **checks,
            "judge_correct": verdict.get("judge_correct", ""),
            "judge_supported": verdict.get("judge_supported", ""),
            "failure": cause,
            "tokens": res["tokens"]["total"],
            "input_tokens": res["tokens"]["input"],
            "output_tokens": res["tokens"]["output"],
            "seconds": res["seconds"],
            "tool_calls": res.get("tool_calls", 0),
            "answer": res["answer"].replace("\n", " ")[:500],
        })
    write_csv(RESULTS, results)

    answerable = [r for r in results if r["kind"] != "unanswerable"]
    unanswerable = [r for r in results if r["kind"] == "unanswerable"]
    n = len(results) or 1
    causes: dict[str, int] = {}
    for r in results:
        if r["failure"]:
            causes[r["failure"]] = causes.get(r["failure"], 0) + 1
    tokens_in = sum(r["input_tokens"] for r in results)
    tokens_out = sum(r["output_tokens"] for r in results)
    summary = {
        "questions_answered": len(results),
        "answerable": len(answerable),
        "unanswerable": len(unanswerable),
        "correct_answerable": sum(r["judge_correct"] == 1 for r in answerable),
        "unsupported_answers": sum(r["judge_supported"] == 0 for r in results),
        "correct_refusals": sum(r["correct_refusal"] == 1 for r in unanswerable),
        "answered_unanswerable": sum(r["correct_refusal"] == 0 for r in unanswerable),
        "wrong_refusals": sum(r["wrong_refusal"] == 1 for r in answerable),
        "answers_with_invalid_citations": sum(r["invalid_citations"] > 0 for r in results),
        "guardrail_fired": sum(bool(r["guardrail"]) for r in results),
        "overall_correct": sum((r["judge_correct"] == 1) for r in results),
        "failures_by_cause": causes,
        "avg_tokens_per_question": round(sum(r["tokens"] for r in results) / n),
        "avg_seconds_per_question": round(sum(r["seconds"] for r in results) / n, 1),
        "est_cost_per_question_usd": round((tokens_in * PRICE_IN + tokens_out * PRICE_OUT) / 1e6 / n, 5),
        "judge_human_agreement": agree,
        "retrieval": retrieval_table,
        "model": next(iter(answers.values()), {}).get("model", ""),
        "judge_model": JUDGE_MODEL,
    }
    SUMMARY_JSON.write_text(json.dumps(summary, indent=2), encoding="utf-8")

    lines = ["# Evaluation summary", "", "## Retrieval (answerable questions)", "",
             "| design | hit@1 | hit@3 | hit@5 | multi: both found @5 | words added (k=5) |",
             "|---|---|---|---|---|---|"]
    for t in retrieval_table:
        lines.append(f"| {t['design']} | {t['hit@1']} | {t['hit@3']} | {t['hit@5']} | "
                     f"{t['multi_both_found@5']} | {t['avg_words_added_k5']} |")
    a, u = summary["answerable"], summary["unanswerable"]
    lines += ["", "## End to end", "",
              f"- Correct on answerable questions (judge): {summary['correct_answerable']}/{a}",
              f"- Correct refusals on unanswerable questions: {summary['correct_refusals']}/{u}",
              f"- Answered an unanswerable question: {summary['answered_unanswerable']}/{u}",
              f"- Wrong refusals on answerable questions: {summary['wrong_refusals']}/{a}",
              f"- Answers with an unsupported claim (judge): {summary['unsupported_answers']}/{len(results)}",
              f"- Answers with an invalid citation: {summary['answers_with_invalid_citations']}",
              f"- Citation guardrail fired: {summary['guardrail_fired']}",
              f"- Average per question: {summary['avg_tokens_per_question']} tokens, "
              f"{summary['avg_seconds_per_question']} s, about ${summary['est_cost_per_question_usd']} at paid-tier prices",
              "", "## Failures by cause", ""]
    lines += [f"- {cause}: {count}" for cause, count in sorted(causes.items())] or ["- none"]
    lines += ["", "## Judge vs your labels", ""]
    if agree:
        for dim, s in agree.items():
            lines.append(f"- {dim}: {s['agreement']:.0%} agreement on {s['n']} answers "
                         f"(Cohen's kappa {s['cohen_kappa']}); disagree on {', '.join(s['disagree_on']) or 'none'}")
    else:
        lines.append("- No human labels yet: run `uv run python evaluate.py --label`.")
    SUMMARY_MD.write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))
    return summary


# ------------------------------------------------------------------ labelling


def label() -> None:
    """Grade answers by hand, without seeing the judge's verdicts."""
    rows = {r["id"]: r for r in read_questions()}
    answers = load_jsonl(ANSWERS)
    if not answers:
        raise SystemExit("No answers yet: run `uv run python main.py evaluate` first.")
    done = set()
    if HUMAN.is_file():
        with HUMAN.open(newline="", encoding="utf-8") as f:
            done = {r["id"] for r in csv.DictReader(f) if (r.get("id") or "").strip()}
        content = HUMAN.read_text(encoding="utf-8")
        if content and not content.endswith("\n"):
            HUMAN.write_text(content + "\n", encoding="utf-8")
    else:
        HUMAN.write_text("id,correct,supported,notes\n", encoding="utf-8")
    print("For each answer type 1 or 0 (s = skip, q = quit). Notes are required for every 0.\n")
    for qid, res in answers.items():
        if qid in done or qid not in rows:
            continue
        row = rows[qid]
        print("=" * 80)
        print(f"{qid} [{row['kind']}] {row['question']}\n\nReference: {row['reference_answer']}\n")
        for c in res.get("retrieved", []):
            print(f"--- [{c['source']}, {c['location']}]\n{c['text'][:700]}\n")
        print(f">>> ANSWER:\n{res['answer']}\n")
        correct = input("correct (1/0, s, q)? ").strip().lower()
        if correct == "q":
            break
        if correct not in ("0", "1"):
            continue
        supported = input("supported (1/0)? ").strip()
        notes = input("notes: ").strip() if "0" in (correct, supported) else input("notes (optional): ").strip()
        with HUMAN.open("a", newline="", encoding="utf-8") as f:
            csv.writer(f).writerow([qid, correct, supported, notes])


# ------------------------------------------------------------------ main


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate retrieval and the agent end to end.")
    parser.add_argument("--fresh", action="store_true", help="ignore cached answers and re-run everything")
    parser.add_argument("--label", action="store_true", help="grade answers by hand into eval/human_labels.csv")
    args = parser.parse_args()
    if args.label:
        label()
        return

    from api_key import load_api_key
    from retrieval import Store

    load_api_key()
    rows = read_questions()
    store = Store()
    log("1/6 retrieval ...")
    retrieval_table, chosen_hits = evaluate_retrieval(rows, store)
    log("2/6 agent answers ...")
    answers = run_agent(rows, args.fresh)
    log("3-4/6 code checks and judge ...")
    verdicts = run_judge(rows, answers)
    log("5/6 agreement with your labels ...")
    agree = agreement(verdicts)
    log("6/6 before/after adding a document ...")
    try:
        before_after(rows, answers, args.fresh)
    except Exception as error:  # noqa: BLE001 - the rest of the evaluation is still useful
        log(f"before/after failed: {type(error).__name__}: {error}")
    summarise(rows, answers, verdicts, retrieval_table, chosen_hits, agree)


if __name__ == "__main__":
    main()
