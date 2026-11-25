"""
Assignment 3: evaluation. `uv run python main.py evaluate`.

1. Retrieval: hit rate at k = 1, 3, 5 for every chunking design x search mode
   -> eval/retrieval.csv. Question vectors are cached, so this costs one
   embedding per question, once.
2. End to end: the agent answers every question -> eval/answers.jsonl
   (resumable: answered ids are skipped; EVAL_FRESH=1 starts over).
3. Code checks: citations valid, expected source cited, refusal right or wrong.
4. LLM judge with a rubric (correct, supported) -> eval/judge.jsonl.
5. Agreement with your grades in eval/human_labels.csv; until it exists,
   eval/to_grade.csv is written for you to fill in (without opening judge.jsonl).
6. Failure categories -> eval/failures.csv, and eval/summary.md with cost per question.
"""

from __future__ import annotations

import asyncio
import csv
import hashlib
import json
import os
import statistics
from pathlib import Path

import index
from agent import CHAT_MODEL, locations_agree, make_llm, open_agent, run

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
HUMAN = EVAL / "human_labels.csv"
ANSWERS = EVAL / "answers.jsonl"
JUDGE = EVAL / "judge.jsonl"
KS = (1, 3, 5)
MODES = ("dense", "hybrid")
SCOPES = ("all", "articles")


def read_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if (r.get("question") or "").strip()]
    for r in rows:
        r["kind"] = r["kind"].strip().lower()
    return rows


def expected_pairs(row: dict) -> list[tuple[str, str]]:
    sources = [s.strip() for s in row["expected_source"].split(";") if s.strip()]
    locations = [l.strip() for l in row["expected_location"].split(";") if l.strip()]
    if not sources:
        return []
    if len(sources) == len(locations):
        return list(zip(sources, locations))
    if len(sources) == 1:
        return [(sources[0], l) for l in locations] or [(sources[0], "")]
    return [(s, l) for s in sources for l in (locations or [""])]


def matches(source: str, location: str, span: list[str], pair: tuple[str, str]) -> bool:
    exp_source, exp_location = pair
    if source.lower() != exp_source.lower():
        return False
    return not exp_location or any(locations_agree(exp_location, s) for s in span + [location])


def chunk_hits(chunk: dict, pairs) -> set[int]:
    return {i for i, p in enumerate(pairs) if matches(chunk["source"], chunk["location"], chunk.get("span", []), p)}


# ---------------------------------------------------------------- 1. retrieval

def retrieval_eval(store: index.Store, rows: list[dict]) -> tuple[list[dict], dict]:
    answerable = [r for r in rows if r["kind"] != "unanswerable"]
    table, per_question = [], {}
    for design in index.DESIGNS:
        for mode, scope in [(m, sc) for m in MODES for sc in SCOPES]:
            hits = {k: 0 for k in KS}
            full_multi, n_multi = 0, 0
            for r in answerable:
                pairs = expected_pairs(r)
                results = store.search(r["question"], k=max(KS), design=design, mode=mode, scope=scope)
                found = [chunk_hits(c, pairs) for c in results]
                first = next((i for i, f in enumerate(found) if f), None)
                for k in KS:
                    hits[k] += first is not None and first < k
                if r["kind"] == "multi":
                    n_multi += 1
                    full_multi += len(set().union(*found)) == len(pairs) if found else 0
                if (design, mode, scope) == (index.ACTIVE_DESIGN, index.ACTIVE_MODE, index.ACTIVE_SCOPE):
                    per_question[r["id"]] = first
            n = len(answerable) or 1
            table.append({
                "design": design, "mode": mode, "scope": scope,
                **{f"hit@{k}": round(hits[k] / n, 3) for k in KS},
                "multi_all@5": round(full_multi / n_multi, 3) if n_multi else "",
                "chunks": int(store._design(design)[3].sum()) if scope == "articles" else len(store._design(design)[0]),
                "active": "yes" if (design, mode, scope) == (index.ACTIVE_DESIGN, index.ACTIVE_MODE, index.ACTIVE_SCOPE) else "",
            })
    with (EVAL / "retrieval.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(table[0]))
        w.writeheader()
        w.writerows(table)
    return table, per_question


# ---------------------------------------------------------------- 2. end to end

def load_jsonl(path: Path) -> dict:
    return {r["id"]: r for r in index.read_jsonl(path)}


async def answer_all(rows: list[dict]) -> dict:
    if os.environ.get("EVAL_FRESH") == "1":
        ANSWERS.unlink(missing_ok=True)
        JUDGE.unlink(missing_ok=True)
    done = {i: r for i, r in load_jsonl(ANSWERS).items()}
    todo = [r for r in rows if r["id"] not in done or done[r["id"]]["question"] != r["question"]]
    if todo:
        print(f"Answering {len(todo)} question(s) with {CHAT_MODEL}...", flush=True)
        async with open_agent() as agent:
            for r in todo:
                try:
                    res = await run(agent, r["question"])
                except Exception as e:  # noqa: BLE001 - log and move on; rerun to retry
                    print(f"  {r['id']}: FAILED ({type(e).__name__}: {e}); rerun evaluate to retry", flush=True)
                    continue
                res["id"] = r["id"]
                index.append_jsonl(ANSWERS, [res])
                done[r["id"]] = res
                print(f"  {r['id']}: {res['seconds']}s, {'refused' if res['refused'] else 'answered'}", flush=True)
    return done


# ---------------------------------------------------------------- 3. code checks

def code_checks(row: dict, res: dict) -> dict:
    pairs = expected_pairs(row)
    cites = res["citations"]
    unanswerable = row["kind"] == "unanswerable"
    return {
        "refused": res["refused"],
        "refusal_right": res["refused"] == unanswerable,
        "citations_valid": all(c["valid"] for c in cites),
        "n_citations": len(cites),
        "cited_expected": any(matches(c["source"], c["location"], [], p) for c in cites for p in pairs) if pairs else None,
        "retrieved_expected": any(matches(c["source"], c["location"], [], p) for c in res["retrieved"] for p in pairs) if pairs else None,
    }


# ---------------------------------------------------------------- 4. judge

RUBRIC = """You grade one answer from an assistant that must answer only from a document collection.

Question: {question}
Question type: {kind}
Reference answer: {reference}

Passages the assistant retrieved:
{passages}

Assistant answer:
{answer}

Grade two things, each 1 or 0.
correct:
- unanswerable question: 1 only if the assistant says the documents do not answer it and does not offer an answer
  of its own; 0 if it gives any substantive answer.
- otherwise: 1 if the answer states the key facts of the reference answer and contradicts nothing in it (extra correct
  detail is fine; partial answers to a two-part question get 0); 0 for a refusal or a wrong or incomplete answer.
supported:
- 1 if every factual claim in the answer is stated in the retrieved passages (paraphrase is fine; numbers, dates,
  thresholds and conditions must match). A refusal with no claims is supported.
- 0 if any claim is missing from or contradicted by the passages, even if it is true in the real world.
reason: one sentence; for every 0 say which claim or fact is the problem."""


def judge_all(rows: list[dict], answers: dict) -> dict:
    from pydantic import BaseModel, Field

    class Verdict(BaseModel):
        correct: int = Field(description="1 or 0")
        supported: int = Field(description="1 or 0")
        reason: str

    judge = make_llm().with_structured_output(Verdict, include_raw=True)
    verdicts = load_jsonl(JUDGE)
    for r in rows:
        res = answers.get(r["id"])
        if not res:
            continue
        digest = hashlib.sha1(res["answer"].encode()).hexdigest()
        if r["id"] in verdicts and verdicts[r["id"]].get("answer_sha") == digest:
            continue
        passages = "\n\n".join(f"[{c['source']}, {c['location']}]\n{c['text'][:1500]}" for c in res["retrieved"]) or "(none)"
        prompt = RUBRIC.format(question=r["question"], kind=r["kind"], reference=r["reference_answer"],
                               passages=passages, answer=res["answer"])
        try:
            out = judge.invoke(prompt)
        except Exception as e:  # noqa: BLE001
            print(f"  judge {r['id']}: FAILED ({type(e).__name__}); rerun to retry", flush=True)
            continue
        v = out["parsed"]
        if v is None:
            continue
        usage = getattr(out["raw"], "usage_metadata", None) or {}
        verdicts[r["id"]] = {"id": r["id"], "answer_sha": digest, "correct": int(v.correct == 1),
                             "supported": int(v.supported == 1), "reason": v.reason,
                             "tokens": usage.get("total_tokens", 0)}
        index.write_jsonl(JUDGE, list(verdicts.values()))
    return verdicts


# ---------------------------------------------------------------- 5. human agreement

def human_agreement(rows: list[dict], answers: dict, verdicts: dict) -> dict | None:
    if not HUMAN.is_file():
        with (EVAL / "to_grade.csv").open("w", newline="", encoding="utf-8") as f:
            w = csv.writer(f)
            w.writerow(["id", "question", "kind", "reference_answer", "answer", "retrieved", "correct", "supported", "notes"])
            for r in rows:
                res = answers.get(r["id"])
                if res:
                    retrieved = " || ".join(f"[{c['source']}, {c['location']}] {c['text'][:300]}" for c in res["retrieved"])
                    w.writerow([r["id"], r["question"], r["kind"], r["reference_answer"], res["answer"], retrieved, "", "", ""])
        print("\nNo eval/human_labels.csv yet: grade eval/to_grade.csv (20+ rows), keep the columns "
              "id,correct,supported,notes and save it as eval/human_labels.csv.")
        return None
    with HUMAN.open(newline="", encoding="utf-8") as f:
        labels = {r["id"].strip(): r for r in csv.DictReader(f) if (r.get("id") or "").strip()}
    both = [i for i in labels if i in verdicts]
    if not both:
        return None
    out = {"n": len(both), "disagreements": []}
    for field in ("correct", "supported"):
        agree = sum(int(labels[i][field]) == verdicts[i][field] for i in both)
        out[field] = round(agree / len(both), 3)
        out["disagreements"] += [f"{i} {field}: human {labels[i][field]}, judge {verdicts[i][field]} - {verdicts[i]['reason']}"
                                 for i in both if int(labels[i][field]) != verdicts[i][field]]
    out["labels"] = labels
    return out


# ---------------------------------------------------------------- 6. failures and summary

def classify(row: dict, checks: dict, grade: dict, retrieval_rank) -> str | None:
    correct, supported = grade["correct"], grade["supported"]
    # refusals are checked in code first; the judge cannot overrule them
    if row["kind"] == "unanswerable":
        return None if checks["refused"] else "unsupported claim"
    hit = checks["retrieved_expected"] or retrieval_rank is not None
    if checks["refused"]:
        return "wrong refusal" if hit else "retrieval miss"
    if correct and supported:
        return None
    if not supported:
        return "unsupported claim"
    return "wrong answer from right passage" if hit else "retrieval miss"


def mean(values) -> float:
    values = list(values)
    return round(statistics.mean(values), 2) if values else 0.0


def main() -> None:
    rows = read_questions()
    store = index.Store()

    print("== Retrieval (answerable questions) ==", flush=True)
    table, ranks = retrieval_eval(store, rows)
    header = f"{'design':10} {'mode':7} {'scope':9} " + " ".join(f"hit@{k:<3}" for k in KS) + "  multi_all@5  chunks"
    print(header)
    for t in table:
        print(f"{t['design']:10} {t['mode']:7} {t['scope']:9} " + " ".join(f"{t[f'hit@{k}']:<7}" for k in KS)
              + f"  {t['multi_all@5']!s:11}  {t['chunks']}" + ("  <- active" if t["active"] else ""))
    best = max(table, key=lambda t: (t["hit@3"], t["hit@1"], t["hit@5"]))
    print(f"Best by hit@3 (then hit@1): {best['design']} / {best['mode']} / {best['scope']}. "
          f"Active: {index.ACTIVE_DESIGN} / {index.ACTIVE_MODE} / {index.ACTIVE_SCOPE} (set in index.py).")

    print("\n== End to end ==", flush=True)
    answers = asyncio.run(answer_all(rows))
    print("Judging...", flush=True)
    verdicts = judge_all(rows, answers)
    agreement = human_agreement(rows, answers, verdicts)
    human = (agreement or {}).get("labels", {})

    results, failures = [], []
    for r in rows:
        res, v = answers.get(r["id"]), verdicts.get(r["id"])
        if not res or not v:
            continue
        checks = code_checks(r, res)
        grade = ({"correct": int(human[r["id"]]["correct"]), "supported": int(human[r["id"]]["supported"])}
                 if r["id"] in human else v)
        category = classify(r, checks, grade, ranks.get(r["id"]))
        results.append({"row": r, "res": res, "checks": checks, "judge": v, "grade": grade, "category": category})
        if category:
            failures.append({"id": r["id"], "kind": r["kind"], "category": category,
                             "graded_by": "human" if r["id"] in human else "judge",
                             "retrieved_expected": checks["retrieved_expected"], "reason": v["reason"],
                             "question": r["question"], "answer": res["answer"][:400]})

    with (EVAL / "failures.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=["id", "kind", "category", "graded_by", "retrieved_expected", "reason", "question", "answer"])
        w.writeheader()
        w.writerows(failures)

    n = len(results)
    ans = [x for x in results if x["row"]["kind"] != "unanswerable"]
    una = [x for x in results if x["row"]["kind"] == "unanswerable"]
    rate = lambda xs, f: round(sum(1 for x in xs if f(x)) / len(xs), 3) if xs else 0.0  # noqa: E731
    cats = {}
    for x in failures:
        cats[x["category"]] = cats.get(x["category"], 0) + 1

    lines = [
        "# Evaluation summary", "",
        f"Chat model `{CHAT_MODEL}`, embeddings `{index.EMBED_MODEL}` ({index.EMBED_DIM} d), "
        f"active retrieval `{index.ACTIVE_DESIGN}` / `{index.ACTIVE_MODE}` / `{index.ACTIVE_SCOPE}`, top {index.TOP_K}.", "",
        "## Retrieval (answerable questions)", "",
        "| design | mode | scope | " + " | ".join(f"hit@{k}" for k in KS) + " | multi: all passages @5 | chunks |",
        "|---|---|---|" + "---|" * len(KS) + "---|---|",
        *[f"| {t['design']} | {t['mode']} | {t['scope']} | " + " | ".join(str(t[f'hit@{k}']) for k in KS)
          + f" | {t['multi_all@5']} | {t['chunks']} |" for t in table], "",
        f"## End to end ({n} questions graded)", "",
        "| metric | value |", "|---|---|",
        f"| correct (judge) | {rate(results, lambda x: x['judge']['correct'])} |",
        f"| supported by retrieved text (judge) | {rate(results, lambda x: x['judge']['supported'])} |",
        f"| answerable: correct | {rate(ans, lambda x: x['grade']['correct'])} |",
        f"| answerable: wrongly refused | {rate(ans, lambda x: x['checks']['refused'])} |",
        f"| unanswerable: correctly refused (code) | {rate(una, lambda x: x['checks']['refused'])} |",
        f"| made something up (answered an unanswerable, or unsupported claim) | "
        f"{rate(results, lambda x: (x['row']['kind'] == 'unanswerable' and not x['checks']['refused']) or not x['grade']['supported'])} |",
        f"| all citations valid (code) | {rate(results, lambda x: x['checks']['citations_valid'])} |",
        f"| cited the expected source and location (code, answerable) | {rate(ans, lambda x: bool(x['checks']['cited_expected']))} |",
        f"| citation guardrail retried / blocked | {sum(x['res']['guardrail'] == 'retried' for x in results)} / "
        f"{sum(x['res']['guardrail'] == 'blocked' for x in results)} |", "",
        "## Cost per question (agent)", "",
        f"- input tokens: {mean(x['res']['tokens_in'] for x in results)}, output tokens: {mean(x['res']['tokens_out'] for x in results)}",
        f"- seconds: mean {mean(x['res']['seconds'] for x in results)}, "
        f"max {max((x['res']['seconds'] for x in results), default=0)}",
        f"- search calls: {mean(sum(t['tool'] == 'search' for t in x['res']['trace']) for x in results)}",
        f"- judge tokens per question: {mean(v.get('tokens', 0) for v in verdicts.values())}", "",
        "## Judge vs human", "",
    ]
    if agreement:
        lines += [f"{agreement['n']} answers graded by both. Agreement: correct {agreement['correct']}, "
                  f"supported {agreement['supported']}.", ""] + [f"- {d}" for d in agreement["disagreements"]]
    else:
        lines += ["Not computed yet: fill in eval/human_labels.csv."]
    lines += ["", "## Failures (eval/failures.csv)", ""]
    lines += [f"- {c}: {k}" for c, k in sorted(cats.items(), key=lambda kv: -kv[1])] or ["- none"]
    lines += ["", "Check each row by hand and relabel any that are really a bad test question."]
    (EVAL / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n" + "\n".join(lines[lines.index(f"## End to end ({n} questions graded)"):]))
    print(f"\nWrote eval/retrieval.csv, answers.jsonl, judge.jsonl, failures.csv, summary.md.")


if __name__ == "__main__":
    main()
