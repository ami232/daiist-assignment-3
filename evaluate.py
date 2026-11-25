"""Assignment 3: evaluation (`main.py evaluate`): retrieval hit rates per design, the agent on every question,
code checks, an LLM judge with a rubric, and agreement with eval/human_labels.csv. Results go to eval/."""

import argparse
import asyncio
import csv
import hashlib
import json
import re
import statistics
import sys
import time
from datetime import date
from pathlib import Path

from pydantic import BaseModel, Field

import agent
import index

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
HUMAN_LABELS = EVAL / "human_labels.csv"
ANSWERS = EVAL / "answers.jsonl"
JUDGE_CACHE = EVAL / "judge_cache.jsonl"
RETRIEVAL = EVAL / "retrieval.csv"
VERDICTS = EVAL / "verdicts.csv"
TO_GRADE = EVAL / "to_grade.md"
SUMMARY = EVAL / "summary.md"
KS = (1, 3, 5)
JUDGE_MODEL = "gemini-3.5-flash-lite"
EVIDENCE_CHARS = 15000
MIN_HUMAN_LABELS = 20

RUBRIC = """You grade answers from an assistant that answers questions about Spanish and international law
on shipwrecks and underwater finds, using only passages it retrieved from four legal texts in Spanish.
You get the question, a reference answer written by a person, the evidence (every passage the
assistant's searches returned) and the assistant's answer.

correct = 1 only if the answer states every key fact of the reference answer and contradicts none of them.
Wording may differ and extra detail is allowed, but a missing or wrong key fact (a number, a deadline,
an owner, a yes/no) makes it 0. For a question with several parts, every part must be right.
If the reference says the documents don't cover the question, correct = 1 only if the answer says so
and does not answer it anyway.

supported = 1 only if every factual claim in the answer can be found in the evidence. A claim that is
not in the evidence makes it 0, even if it is true. Faithful translations of the Spanish text count as
found. The closing line "This is information from the legal texts, not legal advice..." and statements
that the documents don't cover something are not claims.

Write the reason first: what the answer claims and how it compares with the reference and the evidence."""


class JudgeQuotaExhausted(RuntimeError):
    pass


class Verdict(BaseModel):
    reason: str = Field(description="One or two sentences: what the answer claims, compared with the reference and the evidence.")
    correct: int = Field(description="1 or 0, by the rubric.")
    supported: int = Field(description="1 or 0, by the rubric.")


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


def digest(*parts) -> str:
    return hashlib.sha256("\x1f".join(str(p) for p in parts).encode("utf-8")).hexdigest()[:20]


def norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip().strip("[]").strip().lower()


def label_pair(label: str) -> tuple[str, str]:
    source, _, article = norm(label).partition(",")
    return source.strip(), article.strip()


def load_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if (r.get("id") or "").strip()]
    for r in rows:
        r["kind"] = r["kind"].strip().lower()
    return rows


def expected_pairs(row: dict) -> list[tuple[str, str]]:
    sources = [norm(s) for s in row["expected_source"].split(";") if s.strip()]
    locations = [norm(s) for s in row["expected_location"].split(";") if s.strip()]
    if not sources or not locations:
        return []
    if len(sources) == len(locations):
        return list(zip(sources, locations))
    if len(sources) == 1:
        return [(sources[0], loc) for loc in locations]
    return [(s, loc) for s in sources for loc in locations]


def result_pairs(results: list[dict]) -> set[tuple[str, str]]:
    return {(norm(r["source"]), norm(a)) for r in results for a in str(r.get("articles") or r["article"]).split("; ")}


def evaluate_retrieval(rows: list[dict]) -> tuple[list[dict], dict]:
    answerable = [r for r in rows if r["kind"] != "unanswerable"]
    table, first_hit = [], {}
    for design in index.DESIGNS:
        hits = {k: 0 for k in KS}
        both, multi, words = 0, 0, []
        for r in answerable:
            results = index.search(r["question"], k=max(KS), design=design)
            expected = expected_pairs(r)
            for k in KS:
                if any(p in result_pairs(results[:k]) for p in expected):
                    hits[k] += 1
            if r["kind"] == "multi":
                multi += 1
                both += all(p in result_pairs(results) for p in expected)
            words.append(sum(int(x.get("words", 0)) for x in results))
            if design == index.DEFAULT_DESIGN:
                ranks = [i for i, x in enumerate(results, start=1) if any(p in result_pairs([x]) for p in expected)]
                first_hit[r["id"]] = ranks[0] if ranks else None
        row = {"design": design, "questions": len(answerable)}
        row.update({f"hit@{k}": round(hits[k] / len(answerable), 3) for k in KS})
        row["multi_both@5"] = round(both / multi, 3) if multi else ""
        row["words_top5"] = round(statistics.mean(words)) if words else 0
        table.append(row)
        log(f"retrieval [{design}]: " + ", ".join(f"hit@{k} {row[f'hit@{k}']:.2f}" for k in KS))
    return table, first_hit


def load_jsonl(path: Path) -> dict:
    rows = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                row = json.loads(line)
                rows[row["key"]] = row
    return rows


def append_jsonl(path: Path, row: dict) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def answer_key(row: dict) -> str:
    rules = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    return digest(row["id"], row["question"], agent.MODEL, rules)


async def run_agent(rows: list[dict], fresh: bool) -> dict:
    cache = {} if fresh else load_jsonl(ANSWERS)
    results = {r["id"]: cache[answer_key(r)] for r in rows if "evidence" in cache.get(answer_key(r), {})}
    todo = [r for r in rows if r["id"] not in results]
    log(f"agent: {len(results)} answers saved from an earlier run, {len(todo)} to ask")
    if not todo:
        return results
    async with agent.Assistant(approve=lambda name, args: False) as assistant:
        for i, r in enumerate(todo, start=1):
            log(f"agent {i}/{len(todo)}: {r['id']} {r['question'][:70]}")
            try:
                result = await assistant.ask(r["question"])
            except Exception as error:
                log(f"  {r['id']} failed: {str(error)[:200]} (it will be asked again on the next run)")
                continue
            result.update({"key": answer_key(r), "id": r["id"]})
            append_jsonl(ANSWERS, result)
            results[r["id"]] = result
    return results


def code_checks(row: dict, result: dict) -> dict:
    retrieved = {label_pair(x) for x in result["retrieved"]}
    cited = {label_pair(label) for label, _ in result["citations"]}
    expected = expected_pairs(row)
    return {
        "pure_refusal": bool(result["blocked"] or (result["refusal"] and not cited)),
        "blocked": bool(result["blocked"]),
        "citations_valid": int(not result["blocked"] and cited <= retrieved),
        "expected_retrieved": int(any(p in retrieved for p in expected)) if expected else "",
        "cites_expected": int(any(p in cited for p in expected)) if expected else "",
        "guardrail_fired": len(result["guardrail"]),
    }


def judge_call(prompt: str) -> tuple[Verdict, int]:
    from google.genai import types

    config = types.GenerateContentConfig(response_mime_type="application/json", response_schema=Verdict)
    for attempt in range(6):
        try:
            response = index.genai_client().models.generate_content(model=JUDGE_MODEL, contents=prompt, config=config)
            verdict = response.parsed if isinstance(response.parsed, Verdict) else Verdict.model_validate_json(response.text)
            return verdict, int(getattr(response.usage_metadata, "total_token_count", 0) or 0)
        except Exception as error:
            if "PerDay" in str(error):
                raise JudgeQuotaExhausted(f"The daily quota for {JUDGE_MODEL} is used up.") from error
            if attempt == 5 or not agent.transient(error):
                raise
            time.sleep(min(60, 5 * 2 ** attempt))
    raise RuntimeError("unreachable")


def judge(row: dict, result: dict, cache: dict, fresh: bool) -> dict:
    evidence = "\n\n=====\n\n".join(result.get("evidence") or [])[:EVIDENCE_CHARS] or "(no passages retrieved)"
    key = digest(JUDGE_MODEL, RUBRIC, row["question"], row["reference_answer"], result["answer"], evidence)
    if key in cache and not fresh:
        return cache[key]
    if judge.stopped:
        raise JudgeQuotaExhausted("skipped: the judge's daily quota is used up")
    prompt = (
        f"{RUBRIC}\n\nQuestion:\n{row['question']}\n\nReference answer:\n{row['reference_answer']}\n\n"
        f"Evidence (passages the assistant retrieved, in Spanish):\n{evidence}\n\n"
        f"Assistant's answer:\n{result['answer']}\n"
    )
    log(f"judge: grading {row['id']}")
    try:
        verdict, tokens = judge_call(prompt)
    except JudgeQuotaExhausted:
        judge.stopped = True
        raise
    row_out = {"key": key, "correct": int(verdict.correct == 1), "supported": int(verdict.supported == 1),
               "reason": verdict.reason.strip(), "judge_tokens": tokens}
    append_jsonl(JUDGE_CACHE, row_out)
    cache[key] = row_out
    return row_out


judge.stopped = False


def grade(row: dict, result: dict, checks: dict, cache: dict, fresh: bool) -> dict:
    if row["kind"] == "unanswerable":
        if checks["pure_refusal"]:
            return {"correct": 1, "supported": 1, "graded_by": "code", "reason": "Said the documents don't cover it, as expected.", "judge_tokens": 0}
        verdict = judge(row, result, cache, fresh)
        return {**verdict, "correct": 0, "graded_by": "code+judge",
                "reason": "Answered a question the documents don't cover. Judge: " + verdict["reason"]}
    if checks["pure_refusal"]:
        reason = "Blocked by the citation check." if checks["blocked"] else "Said the documents don't cover a question they answer."
        return {"correct": 0, "supported": 1, "graded_by": "code", "reason": reason, "judge_tokens": 0}
    return {**judge(row, result, cache, fresh), "graded_by": "judge"}


def suggested_cause(row: dict, checks: dict, verdict: dict) -> str:
    if verdict["correct"] and verdict["supported"]:
        return ""
    if row["kind"] == "unanswerable":
        return "bad test question?" if verdict["supported"] else "unsupported claim"
    if checks["pure_refusal"]:
        return "wrong refusal" if checks["expected_retrieved"] else "retrieval miss"
    if not verdict["correct"]:
        return "wrong answer from the right passage" if checks["expected_retrieved"] else "retrieval miss"
    return "unsupported claim"


def human_agreement(verdicts: list[dict]) -> dict:
    if not HUMAN_LABELS.exists():
        return {"n": 0}
    with HUMAN_LABELS.open(newline="", encoding="utf-8") as f:
        labels = {r["id"].strip(): r for r in csv.DictReader(f) if (r.get("id") or "").strip()}
    pairs = []
    for v in verdicts:
        h = labels.get(v["id"])
        if h and h.get("correct", "").strip() in ("0", "1") and h.get("supported", "").strip() in ("0", "1"):
            pairs.append((v, int(h["correct"]), int(h["supported"]), h.get("notes", "")))
    if not pairs:
        return {"n": 0}
    judged = [p for p in pairs if "judge" in p[0]["graded_by"]]

    def rate(items, field, index_):
        return round(sum(p[0][field] == p[index_] for p in items) / len(items), 3) if items else ""

    return {
        "n": len(pairs), "n_judged": len(judged),
        "correct": rate(pairs, "correct", 1), "supported": rate(pairs, "supported", 2),
        "judge_correct": rate(judged, "correct", 1), "judge_supported": rate(judged, "supported", 2),
        "disagreements": [
            {"id": p[0]["id"], "field": field, "you": p[i], "graded": p[0][field], "by": p[0]["graded_by"], "notes": p[3]}
            for p in pairs for field, i in (("correct", 1), ("supported", 2)) if p[0][field] != p[i]
        ],
    }


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def write_to_grade(rows: list[dict], results: dict) -> None:
    lines = [
        "# Answers to grade",
        "",
        "Grade at least 20 of these in eval/human_labels.csv (id, correct, supported, notes) "
        "BEFORE opening eval/verdicts.csv, using the same rubric as the judge.",
        "",
    ]
    for r in rows:
        res = results.get(r["id"])
        if not res:
            continue
        lines += [
            f"## {r['id']} ({r['kind']})",
            "",
            f"**Question:** {r['question']}",
            "",
            f"**Reference answer:** {r['reference_answer']}",
            "",
            f"**Expected:** {r['expected_source']} {r['expected_location']}".rstrip(),
            "",
            "**Assistant's answer:**",
            "",
            "> " + res["answer"].replace("\n", "\n> "),
            "",
            f"**Retrieved:** {', '.join(res['retrieved']) or 'nothing'}",
            "",
        ]
    TO_GRADE.write_text("\n".join(lines), encoding="utf-8")


def pct(part: int, whole: int) -> str:
    return f"{part}/{whole} ({part / whole:.0%})" if whole else "0/0"


def write_summary(retrieval: list[dict], verdicts: list[dict], results: dict, agreement: dict, rows: list[dict]) -> str:
    done = [v for v in verdicts if v["graded_by"]]
    answerable = [v for v in done if v["kind"] != "unanswerable"]
    unanswerable = [v for v in done if v["kind"] == "unanswerable"]
    best = max(retrieval, key=lambda r: (r["hit@5"], r["hit@3"], r["hit@1"], -r["words_top5"]))
    ran = [results[v["id"]] for v in done]
    lines = [
        "# Evaluation summary",
        "",
        f"{date.today().isoformat()} · agent `{agent.MODEL}` · judge `{JUDGE_MODEL}` · search design `{index.DEFAULT_DESIGN}`",
        "",
        "## Retrieval",
        "",
        f"Answerable questions: {retrieval[0]['questions']}. A hit means an expected article is among the top k results.",
        "",
        "| Design | hit@1 | hit@3 | hit@5 | multi: both passages in top 5 | words added (top 5) |",
        "|---|---|---|---|---|---|",
    ]
    lines += [f"| {r['design']} | {r['hit@1']:.2f} | {r['hit@3']:.2f} | {r['hit@5']:.2f} | {r['multi_both@5']} | {r['words_top5']} |" for r in retrieval]
    lines += ["", f"Highest hit@5 (ties broken by hit@3, hit@1, fewer words): **{best['design']}**.", ""]
    lines += [
        "## End to end",
        "",
        f"Questions answered: {len(done)} of {len(rows)}.",
        "",
        "| Result | Count |",
        "|---|---|",
        f"| Correct (all questions) | {pct(sum(v['correct'] for v in done), len(done))} |",
        f"| Supported (all questions) | {pct(sum(v['supported'] for v in done), len(done))} |",
        f"| Correct answers to answerable questions | {pct(sum(v['correct'] for v in answerable), len(answerable))} |",
        f"| Unsupported answers | {sum(1 - v['supported'] for v in done)} |",
        f"| Correct refusals (unanswerable) | {pct(sum(v['correct'] for v in unanswerable), len(unanswerable))} |",
        f"| Wrong refusals (answerable) | {sum(1 for v in answerable if v['pure_refusal'])} |",
        f"| Blocked by the citation check | {sum(1 for v in done if v['blocked'])} |",
        f"| Citation check fired (incl. fixed on retry) | {sum(1 for v in done if v['guardrail_fired'])} |",
        "",
        "| Kind | n | Correct | Supported |",
        "|---|---|---|---|",
    ]
    for kind in ("single", "multi", "unanswerable"):
        group = [v for v in done if v["kind"] == kind]
        lines.append(f"| {kind} | {len(group)} | {sum(v['correct'] for v in group)} | {sum(v['supported'] for v in group)} |")
    if ran:
        tokens = [r["input_tokens"] + r["output_tokens"] for r in ran]
        seconds = [r["seconds"] for r in ran]
        judge_tokens = [v["judge_tokens"] for v in done if v["judge_tokens"]]
        lines += [
            "",
            "## Cost per question",
            "",
            "| | Mean | Median | Max |",
            "|---|---|---|---|",
            f"| Agent tokens | {statistics.mean(tokens):,.0f} | {statistics.median(tokens):,.0f} | {max(tokens):,} |",
            f"| Agent model calls | {statistics.mean(r['model_calls'] for r in ran):.1f} | {statistics.median(r['model_calls'] for r in ran):.0f} | {max(r['model_calls'] for r in ran)} |",
            f"| Seconds | {statistics.mean(seconds):.1f} | {statistics.median(seconds):.1f} | {max(seconds):.1f} |",
            f"| Judge tokens (judged answers) | {statistics.mean(judge_tokens) if judge_tokens else 0:,.0f} | {statistics.median(judge_tokens) if judge_tokens else 0:,.0f} | {max(judge_tokens) if judge_tokens else 0:,} |",
        ]
    lines += ["", "## Agreement with your grades", ""]
    if agreement["n"]:
        lines += [
            f"You graded {agreement['n']} answers; {agreement['n_judged']} of them were graded by the judge.",
            "",
            "| | All your grades | Judge-graded only |",
            "|---|---|---|",
            f"| Correct | {agreement['correct']:.0%} | {agreement['judge_correct'] if agreement['judge_correct'] == '' else format(agreement['judge_correct'], '.0%')} |",
            f"| Supported | {agreement['supported']:.0%} | {agreement['judge_supported'] if agreement['judge_supported'] == '' else format(agreement['judge_supported'], '.0%')} |",
            "",
        ]
        lines += [f"- {d['id']} {d['field']}: you {d['you']}, {d['by']} {d['graded']}. {d['notes']}".rstrip() for d in agreement["disagreements"]] or ["No disagreements."]
    else:
        lines.append("No grades yet in eval/human_labels.csv.")
    failures = [v for v in done if v["suggested_cause"]]
    lines += ["", "## Failures by suggested cause (check each one yourself)", ""]
    causes = sorted({v["suggested_cause"] for v in failures})
    lines += [f"- {c}: {sum(v['suggested_cause'] == c for v in failures)} ({', '.join(v['id'] for v in failures if v['suggested_cause'] == c)})" for c in causes] or ["No failures."]
    fired = [(v["id"], g["reason"]) for v in done for g in results[v["id"]]["guardrail"]]
    lines += ["", "## Citation check firings", ""]
    lines += [f"- {i}: answer {reason}" for i, reason in fired] or ["None."]
    text = "\n".join(lines) + "\n"
    SUMMARY.write_text(text, encoding="utf-8")
    return text


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--fresh", action="store_true", help="ask the agent every question again (spends quota)")
    parser.add_argument("--rejudge", action="store_true", help="grade every answer again with the judge")
    parser.add_argument("--retrieval-only", action="store_true", help="only measure retrieval hit rates")
    args = parser.parse_args()

    rows = load_questions()
    retrieval, first_hit = evaluate_retrieval(rows)
    write_csv(RETRIEVAL, retrieval)
    if args.retrieval_only:
        print(RETRIEVAL.read_text(encoding="utf-8"))
        return 0

    results = asyncio.run(run_agent(rows, args.fresh))
    write_to_grade(rows, results)
    log(f"Answers to grade are in {TO_GRADE.relative_to(ROOT)}. Judging now; Ctrl+C is safe, the next run continues.")
    cache = load_jsonl(JUDGE_CACHE)
    verdicts = []
    for r in rows:
        result = results.get(r["id"])
        base = {"id": r["id"], "kind": r["kind"]}
        if not result:
            verdicts.append({**base, "graded_by": "", "correct": "", "supported": "", "reason": "not answered (error)"})
            continue
        checks = code_checks(r, result)
        try:
            verdict = grade(r, result, checks, cache, args.rejudge)
        except JudgeQuotaExhausted:
            verdicts.append({**base, **checks, "graded_by": "", "correct": "", "supported": "", "reason": "waiting for the judge's quota"})
            continue
        except Exception as error:
            log(f"judge failed on {r['id']}: {str(error)[:200]}")
            verdicts.append({**base, **checks, "graded_by": "", "correct": "", "supported": "", "reason": "judge error"})
            continue
        verdicts.append({
            **base, **checks,
            "first_hit_rank": first_hit.get(r["id"], ""),
            "correct": verdict["correct"], "supported": verdict["supported"], "graded_by": verdict["graded_by"],
            "suggested_cause": suggested_cause(r, checks, verdict),
            "reason": verdict["reason"], "judge_tokens": verdict["judge_tokens"],
            "agent_tokens": result["input_tokens"] + result["output_tokens"], "seconds": result["seconds"],
        })
    fields = ["id", "kind", "correct", "supported", "graded_by", "suggested_cause", "pure_refusal", "blocked",
              "citations_valid", "expected_retrieved", "cites_expected", "first_hit_rank", "guardrail_fired",
              "agent_tokens", "judge_tokens", "seconds", "reason"]
    write_csv(VERDICTS, [{f: v.get(f, "") for f in fields} for v in verdicts])
    graded = [v for v in verdicts if v["graded_by"]]
    agreement = human_agreement(graded)
    summary = write_summary(retrieval, graded, results, agreement, rows)
    if agreement["n"] >= MIN_HUMAN_LABELS:
        print(summary)
    else:
        print(RETRIEVAL.read_text(encoding="utf-8"))
        print(
            f"The assistant's answers are in {TO_GRADE.relative_to(ROOT)}. Grade at least {MIN_HUMAN_LABELS} of them in "
            f"{HUMAN_LABELS.relative_to(ROOT)} before opening {VERDICTS.relative_to(ROOT)} or {SUMMARY.relative_to(ROOT)}, "
            "then run `uv run python main.py evaluate` again: it reuses the saved answers and verdicts, so it costs no quota."
        )
    missing = len(rows) - len(graded)
    if judge.stopped:
        log(f"The judge's daily quota for {JUDGE_MODEL} ran out, so {missing} answer(s) still need the judge. "
            "Run `uv run python main.py evaluate` again after 09:00 Spanish time: it continues where it stopped.")
    elif missing:
        log(f"{missing} question(s) have no grade yet; run `uv run python main.py evaluate` again to finish them.")
    return 0


if __name__ == "__main__":
    sys.exit(main())