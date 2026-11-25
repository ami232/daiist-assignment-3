"""
Assignment 3: evaluation (`uv run python main.py evaluate`).

  1. Retrieval: hit rate at k = 1, 3, 5 for every design (2 chunkings x 3 search
     methods), on the answerable questions of eval/questions.csv.
  2. End to end: the agent of agent.py answers every question (add_document is
     always refused here, so evaluating never changes the index).
  3. Code checks: did it search, are all citations valid, did it refuse?
  4. LLM judge (gemini-3.5-flash) with a rubric and the retrieved passages as
     evidence: is the answer correct, is every claim supported?
  5. Agreement between the judge and your own grades in eval/human_labels.csv.
  6. Outcomes, suggested failure causes, tokens and seconds per question.

Answers and verdicts are cached in eval/answers.jsonl and eval/verdicts.jsonl, so
running this again only calls the models for new or changed questions. Delete
those files (or pass --fresh) to start over.

    uv run python evaluate.py                    # everything
    uv run python evaluate.py --retrieval-only   # step 1 only (no agent, no judge)
    uv run python evaluate.py --answers-only     # steps 1-2 and the grading sheet, no judge:
                                                 # grade by hand before seeing any verdict
    uv run python evaluate.py --fresh            # ignore the caches
"""

from __future__ import annotations

import argparse
import asyncio
import csv
import hashlib
import json
import re
import statistics
import sys
from contextlib import AsyncExitStack
from pathlib import Path

from pydantic import BaseModel, Field

import index as ix
from retrieval import METHODS, Retriever, cites_in, embed_query

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
HUMAN_LABELS = EVAL / "human_labels.csv"
ANSWERS_CACHE = EVAL / "answers.jsonl"
VERDICTS_CACHE = EVAL / "verdicts.jsonl"

JUDGE_MODEL = "gemini-3.5-flash"  # a stronger model than the agent's, as in class
KS = (1, 3, 5)

# Prices in USD per 1M tokens, paid tier, from https://ai.google.dev/gemini-api/docs/pricing
# (checked 24 Nov 2026). Used only for the cost estimate in the summary.
PRICES = {
    "gemini-3.5-flash-lite": {"input": 0.30, "output": 2.50},
    "gemini-3.5-flash": {"input": 1.50, "output": 9.00},
    "gemini-embedding-2": {"input": 0.20},
}


# --------------------------------------------------------------------------- questions

def load_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if (r.get("question") or "").strip()]
    if not rows:
        sys.exit("eval/questions.csv has no questions yet.")
    for r in rows:
        r["kind"] = r["kind"].strip().lower()
        r["expected"] = expected_passages(r)
    return rows


def expected_passages(row: dict) -> list[tuple[str, str]]:
    """[(source, location)] pairs; one source may serve several locations: 'a' + 'x;y'."""
    sources = [s.strip() for s in row["expected_source"].split(";") if s.strip()]
    locations = [l.strip() for l in row["expected_location"].split(";") if l.strip()]
    if not sources:
        return []
    if len(sources) == 1 and len(locations) > 1:
        sources = sources * len(locations)
    if len(locations) == 1 and len(sources) > 1:
        locations = locations * len(sources)
    return list(zip(sources, locations or [""] * len(sources)))


def location_matches(location: str, sections: str, pages: str) -> bool:
    """Does a chunk with these metadata strings ("|3-501.17|", "|72|73|") cover the expected location?

    A Food Code location ("3-501.17", "§3-501.17(A)") is matched on the section; any
    other ("p. 14", "14") on the page. An empty location matches any chunk of the source.
    """
    section = re.search(r"\d-\d{3}\.\d{2,3}", location)
    if section:
        return f"|{section.group(0)}|" in sections
    page = re.search(r"\d+", location)
    if page:
        return f"|{page.group(0)}|" in pages
    return True


def hit_covers(hit: dict, passage: tuple[str, str]) -> bool:
    source, location = passage
    return hit["source"] == source and location_matches(location, hit.get("sections", ""), hit.get("pages", ""))


# --------------------------------------------------------------------------- 1. retrieval

def evaluate_retrieval(questions: list[dict]) -> list[dict]:
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    print(f"Embedding {len(answerable)} questions (cached in index/query_cache.json) ...")
    vectors = {q["id"]: embed_query(q["question"]) for q in answerable}
    corpus_sources = [d["source"] for d in ix.DOCUMENTS]

    rows, per_question = [], []
    for chunking in ix.DESIGNS:
        # Only the original corpus, so a document added later with add_document
        # (which goes into one chunking only) does not skew the comparison.
        retriever = Retriever(chunking, sources=corpus_sources)
        for method in METHODS:
            hits_at = {k: [] for k in KS}
            all_at_5, words_3, words_5, multi_all = [], [], [], []
            for q in answerable:
                hits = retriever.search(q["question"], method, max(KS), query_vector=vectors[q["id"]])
                ranks = [
                    next((r for r, h in enumerate(hits, start=1) if hit_covers(h, p)), None)
                    for p in q["expected"]
                ]
                first = min((r for r in ranks if r), default=None)
                for k in KS:
                    hits_at[k].append(first is not None and first <= k)
                all5 = all(r is not None and r <= 5 for r in ranks)
                all_at_5.append(all5)
                if q["kind"] == "multi":
                    multi_all.append(all5)
                words_3.append(sum(h["words"] for h in hits[:3]))
                words_5.append(sum(h["words"] for h in hits[:5]))
                per_question.append({
                    "design": f"{chunking}/{method}", "id": q["id"], "kind": q["kind"],
                    "first_hit_rank": first or "", "all_passages_in_top5": all5,
                    "top3": " ; ".join(h["cite"] for h in hits[:3]),
                })
            rows.append({
                "design": f"{chunking}/{method}",
                "chunking": chunking,
                "method": method,
                "chunks": len(retriever),
                **{f"hit@{k}": round(statistics.mean(hits_at[k]), 3) for k in KS},
                "multi_all_passages@5": round(statistics.mean(multi_all), 3) if multi_all else "",
                "avg_words_top3": round(statistics.mean(words_3)),
                "avg_words_top5": round(statistics.mean(words_5)),
            })

    write_csv(EVAL / "retrieval.csv", rows)
    write_csv(EVAL / "retrieval_per_question.csv", per_question)
    print(f"\nRetrieval on {len(answerable)} answerable questions "
          f"({sum(q['kind'] == 'multi' for q in answerable)} multi):\n")
    print(f"{'design':<20}{'hit@1':>7}{'hit@3':>7}{'hit@5':>7}{'multi all@5':>13}{'words top3':>12}{'words top5':>12}")
    for r in rows:
        print(f"{r['design']:<20}{r['hit@1']:>7.0%}{r['hit@3']:>7.0%}{r['hit@5']:>7.0%}"
              f"{(r['multi_all_passages@5'] if r['multi_all_passages@5'] != '' else 0):>13.0%}"
              f"{r['avg_words_top3']:>12}{r['avg_words_top5']:>12}")
    return rows


# --------------------------------------------------------------------------- 2. agent answers

def read_jsonl(path: Path) -> dict[str, dict]:
    out = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                record = json.loads(line)
                out[record["key"]] = record
    return out


def append_jsonl(path: Path, record: dict) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def answer_key(question: str) -> str:
    """Changes whenever something that shapes the answer changes, so the cache is never stale."""
    import agent
    import retrieval

    setup = "|".join([
        question, agent.MODEL, (ROOT / "AGENTS.md").read_text(encoding="utf-8"),
        (ROOT / "agent.py").read_text(encoding="utf-8"),
        retrieval.CHOSEN_CHUNKING, retrieval.CHOSEN_METHOD, str(retrieval.TOP_K),
    ])
    return hashlib.sha1(setup.encode()).hexdigest()[:16]


async def run_agent(questions: list[dict], fresh: bool) -> dict[str, dict]:
    from agent import ask, build_agent, load_tools

    cache = {} if fresh else read_jsonl(ANSWERS_CACHE)
    results = {}
    todo = [q for q in questions if answer_key(q["question"]) not in cache]
    print(f"\nAgent: {len(questions) - len(todo)} answers from cache, {len(todo)} to run.")
    if todo:
        async with AsyncExitStack() as stack:
            agent = build_agent(await load_tools(stack), approve=lambda name, args: False)
            for n, q in enumerate(todo, start=1):
                key = answer_key(q["question"])
                try:
                    record = await ask(agent, q["question"])
                except Exception as error:  # noqa: BLE001 - record and go on with the others
                    print(f"  {q['id']}: ERROR {type(error).__name__}: {error}", file=sys.stderr)
                    continue
                record = {"key": key, "id": q["id"], "question": q["question"], **record}
                append_jsonl(ANSWERS_CACHE, record)
                cache[key] = record
                print(f"  [{n}/{len(todo)}] {q['id']} {record['seconds']:.1f}s"
                      + ("  (citation guardrail fired)" if record["guardrail_fired"] else ""))
    for q in questions:
        key = answer_key(q["question"])
        if key in cache:
            results[q["id"]] = cache[key]
    return results


# --------------------------------------------------------------------------- 3. code checks

REFUSAL_RE = re.compile(r"do(?:es)? not cover this|could not back this answer", re.I)


def is_refusal(answer: str) -> bool:
    """A refusal starts with the sentence AGENTS.md prescribes (a short note may follow),
    or says it cannot back an answer, without citing any rule as the answer."""
    from agent import REFUSAL, WITHHELD

    text = answer.strip()
    if text.lower().startswith(REFUSAL.lower()) or text.startswith(WITHHELD):
        return True
    return bool(REFUSAL_RE.search(text)) and not cites_in(text)


def parse_passages(tool_results: list[str]) -> list[dict]:
    """The passages the search tool returned, with source, sections and pages, from its text."""
    by_title = {d["title"]: d["source"] for d in ix.DOCUMENTS}
    passages = []
    for output in tool_results:
        for block in output.split("\n\n"):
            lines = block.splitlines()
            if len(lines) < 2 or "Cite as: [" not in lines[0] or not lines[1].startswith("Source: "):
                continue
            source_line = lines[1].removeprefix("Source: ")
            document = next((t for t in by_title if source_line.startswith(t)), "")
            section = re.search(r"§(\d-\d{3}\.\d{2,3})", source_line)
            pages = re.search(r"pp?\. (\d+)(?:-(\d+))?", source_line)
            first, last = (int(pages.group(1)), int(pages.group(2) or pages.group(1))) if pages else (0, -1)
            passages.append({
                "source": by_title.get(document, ""),
                "sections": f"|{section.group(1)}|" if section else "",
                "pages": "|" + "|".join(str(p) for p in range(first, last + 1)) + "|",
                "text": "\n".join(lines[1:]),
                "cite": re.search(r"Cite as: \[([^\]]+)\]", lines[0]).group(1),
            })
    return passages


def code_checks(q: dict, r: dict) -> dict:
    cited = cites_in(r["answer"])
    offered = set(r["offered_cites"])
    passages = parse_passages(r["tool_results"])
    expected = q["expected"]
    return {
        "searched": any(line.startswith("call search") for line in r["trace"]),
        "refused": is_refusal(r["answer"]),
        "n_citations": len(cited),
        "citations_valid": all(c in offered for c in cited),
        "expected_retrieved": bool(expected) and any(hit_covers(p, e) for e in expected for p in passages),
        "all_expected_retrieved": bool(expected) and all(any(hit_covers(p, e) for p in passages) for e in expected),
        "expected_cited": bool(expected) and any(
            any(hit_covers(p, e) for e in expected) for p in passages if p["cite"] in cited
        ),
        "guardrail_fired": r["guardrail_fired"],
        "guardrail_withheld": r["guardrail_withheld"],
        "call_limit_hit": r.get("call_limit_hit", False),
    }


# --------------------------------------------------------------------------- 4. judge

class Verdict(BaseModel):
    reasoning: str = Field(description="Two to four sentences checking the answer against each criterion.")
    correct: bool = Field(description="True only if the answer meets criterion 1.")
    supported: bool = Field(description="True only if the answer meets criterion 2.")


JUDGE_PROMPT = """You are grading an AI assistant that answers food-safety questions from the owner, manager or cooks of a small restaurant, using only passages from FDA documents. A wrong rule can make customers ill or fail an inspection, so grade strictly.

Criteria:
1. Correct.
   - Answerable question: the answer gives the facts of the reference answer: the same numbers, units, time limits and conditions. Extra correct detail is fine. A missing key number or condition, or anything that contradicts the reference, is not correct. A refusal ("the documents do not cover this") is not correct.
   - Unanswerable question: correct only if the assistant says the documents do not cover it and does not present any rule as the answer.
2. Supported: every factual claim in the answer can be found in the retrieved passages below (wording may differ). A claim that is not in the passages fails even if it is true. A refusal with no claims is supported. Exception: the assistant's rules require it to add that the version of the Food Code adopted by the user's state or city is what applies; that caveat is not a claim to check, so ignore it (but a citation attached to it must still be valid).

Question kind: {kind}
Question: {question}
Reference answer: {reference_answer}

Retrieved passages (what the assistant saw, recorded by the harness):
{passages}

Assistant's answer:
{answer}"""


def verdict_key(q: dict, answer: str, passages: str) -> str:
    return hashlib.sha1(f"{JUDGE_MODEL}|{JUDGE_PROMPT}|{q['question']}|{q['reference_answer']}|{answer}|{passages}".encode()).hexdigest()[:16]


async def judge_all(questions, answers, fresh: bool) -> dict[str, dict]:
    from langchain_google_genai import ChatGoogleGenerativeAI

    from api_key import load_api_key

    load_api_key()
    cache = {} if fresh else read_jsonl(VERDICTS_CACHE)
    judge = ChatGoogleGenerativeAI(model=JUDGE_MODEL, temperature=0).with_structured_output(Verdict, include_raw=True)
    verdicts = {}
    todo = 0
    for q in questions:
        r = answers.get(q["id"])
        if r is None:
            continue
        passages = "\n\n".join(r["tool_results"]) or "(the assistant did not search)"
        key = verdict_key(q, r["answer"], passages)
        if key not in cache:
            todo += 1
            prompt = JUDGE_PROMPT.format(
                kind=q["kind"], question=q["question"], reference_answer=q["reference_answer"],
                passages=passages, answer=r["answer"],
            )
            try:
                out = await judge.ainvoke(prompt)
            except Exception as error:  # noqa: BLE001
                print(f"  judge {q['id']}: ERROR {type(error).__name__}: {error}", file=sys.stderr)
                continue
            usage = out["raw"].usage_metadata or {}
            cache[key] = {
                "key": key, "id": q["id"], **out["parsed"].model_dump(),
                "judge_input_tokens": usage.get("input_tokens", 0),
                "judge_output_tokens": usage.get("output_tokens", 0),
            }
            append_jsonl(VERDICTS_CACHE, cache[key])
        verdicts[q["id"]] = cache[key]
    print(f"Judge: {len(verdicts) - todo} verdicts from cache, {todo} new.")
    return verdicts


# --------------------------------------------------------------------------- 5. outcomes and agreement

def outcome(q: dict, checks: dict, verdict: dict | None) -> str:
    if q["kind"] == "unanswerable":
        return "correct refusal" if checks["refused"] else "answered unanswerable"
    if checks["refused"]:
        return "wrong refusal"
    if verdict is None:
        return "not judged"
    if verdict["correct"] and verdict["supported"]:
        return "correct"
    if verdict["correct"]:
        return "unsupported"  # right, but with claims that are not in the passages
    return "wrong answer"


def suggested_cause(q: dict, result: str, checks: dict) -> str:
    """A first guess from the code checks; you confirm or change it in eval/failures.csv."""
    if result in ("correct", "correct refusal"):
        return ""
    if result == "answered unanswerable":
        return "unsupported claim"
    if result == "unsupported":
        return "unsupported claim"
    if not checks["expected_retrieved"]:
        return "retrieval miss"
    if result == "wrong refusal":
        return "wrong refusal"
    if q["kind"] == "multi" and not checks["all_expected_retrieved"]:
        return "retrieval miss"
    return "wrong answer from right passage"


def load_human_labels() -> dict[str, dict]:
    if not HUMAN_LABELS.exists():
        return {}
    with HUMAN_LABELS.open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if (r.get("id") or "").strip() and (r.get("correct") or "").strip()]
    return {r["id"].strip(): r for r in rows}


def cohen_kappa(a: list[bool], b: list[bool]) -> float | None:
    n = len(a)
    if n == 0:
        return None
    observed = sum(x == y for x, y in zip(a, b)) / n
    pa, pb = sum(a) / n, sum(b) / n
    expected = pa * pb + (1 - pa) * (1 - pb)
    return None if expected == 1 else round((observed - expected) / (1 - expected), 3)


def agreement(verdicts: dict, labels: dict) -> dict:
    rows, stats = [], {}
    ids = [i for i in labels if i in verdicts]
    for field in ("correct", "supported"):
        human = [labels[i][field].strip() == "1" for i in ids]
        judge = [bool(verdicts[i][field]) for i in ids]
        stats[field] = {
            "n": len(ids),
            "agreement": round(sum(h == j for h, j in zip(human, judge)) / len(ids), 3) if ids else None,
            "cohen_kappa": cohen_kappa(human, judge),
        }
    for i in ids:
        h = {f: labels[i][f].strip() == "1" for f in ("correct", "supported")}
        j = {f: bool(verdicts[i][f]) for f in ("correct", "supported")}
        rows.append({
            "id": i, "human_correct": int(h["correct"]), "judge_correct": int(j["correct"]),
            "human_supported": int(h["supported"]), "judge_supported": int(j["supported"]),
            "agree": h == j, "human_notes": labels[i].get("notes", ""), "judge_reasoning": verdicts[i]["reasoning"],
        })
    write_csv(EVAL / "agreement.csv", rows)
    return stats


# --------------------------------------------------------------------------- outputs

def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_grading_sheet(questions, answers) -> None:
    """Everything you need to grade an answer, without the judge's verdict."""
    parts = [
        "# Grading sheet\n",
        "Grade each answer **before** opening eval/results.csv or eval/verdicts.jsonl (they hold the judge's verdicts).",
        "Write your grades in eval/human_labels.csv: `id,correct,supported,notes`.\n",
        "- **correct** = 1 if the answer matches the reference (or, for an unanswerable question, it properly refuses).",
        "- **supported** = 1 if every claim is in the retrieved passages shown below.",
        "- **notes**: why, for every 0.\n",
    ]
    for q in questions:
        r = answers.get(q["id"])
        if r is None:
            continue
        passages = parse_passages(r["tool_results"])
        cited = set(cites_in(r["answer"]))

        def quote(group):
            seen, out = set(), []
            for p in group:
                if p["text"] not in seen:  # the same passage can come back from several searches
                    seen.add(p["text"])
                    out.append("> **[" + p["cite"] + "]** " + p["text"].replace("\n", "\n> "))
            return "\n\n".join(out)

        used = quote([p for p in passages if p["cite"] in cited]) or "> (the answer cites no passage)"
        others = quote([p for p in passages if p["cite"] not in cited]) or "> (none)"
        parts.append(
            f"\n---\n\n## {q['id']} ({q['kind']})\n\n**Question:** {q['question']}\n\n"
            f"**Reference answer:** {q['reference_answer']}\n\n"
            f"**Expected source:** {q['expected_source'] or '-'} {q['expected_location'] or ''}\n\n"
            f"**Agent's answer:**\n\n{r['answer']}\n\n"
            f"**Passages the answer cites:**\n\n{used}\n\n"
            f"<details><summary>Other retrieved passages</summary>\n\n{others}\n\n</details>\n"
        )
    (EVAL / "grading_sheet.md").write_text("\n".join(parts), encoding="utf-8")


def cost_per_question(answers: list[dict], verdicts: list[dict]) -> dict:
    import agent

    def mean(values):
        return round(statistics.mean(values), 1) if values else 0

    agent_in = [a["input_tokens"] for a in answers]
    agent_out = [a["output_tokens"] for a in answers]
    out = {
        "questions": len(answers),
        "agent_model": agent.MODEL,
        "agent_input_tokens_per_question": mean(agent_in),
        "agent_output_tokens_per_question": mean(agent_out),
        "agent_model_calls_per_question": mean([a["model_calls"] for a in answers]),
        "seconds_per_question_mean": mean([a["seconds"] for a in answers]),
        "seconds_per_question_median": round(statistics.median([a["seconds"] for a in answers]), 1) if answers else 0,
        "seconds_per_question_max": max((a["seconds"] for a in answers), default=0),
        "judge_input_tokens_per_question": mean([v.get("judge_input_tokens", 0) for v in verdicts]),
        "judge_output_tokens_per_question": mean([v.get("judge_output_tokens", 0) for v in verdicts]),
    }
    for who, model in (("agent", agent.MODEL), ("judge", JUDGE_MODEL)):
        price = PRICES[model]
        out[f"{who}_usd_per_question"] = round(
            (out[f"{who}_input_tokens_per_question"] * price["input"]
             + out[f"{who}_output_tokens_per_question"] * price["output"]) / 1e6, 6)
    return out


async def end_to_end(questions: list[dict], fresh: bool, answers_only: bool = False) -> None:
    answers = await run_agent(questions, fresh)
    write_grading_sheet(questions, answers)
    if answers_only:
        print(f"\n{len(answers)} answers saved. Grade them in eval/grading_sheet.md -> eval/human_labels.csv,")
        print("then run `uv run python main.py evaluate` for the judge and the agreement.")
        return
    verdicts = await judge_all(questions, answers, fresh)
    labels = load_human_labels()

    rows, failures = [], []
    for q in questions:
        r = answers.get(q["id"])
        if r is None:
            continue
        checks = code_checks(q, r)
        v = verdicts.get(q["id"])
        result = outcome(q, checks, v)
        row = {
            "id": q["id"], "kind": q["kind"], "question": q["question"], "outcome": result,
            **checks,
            "judge_correct": "" if v is None else int(v["correct"]),
            "judge_supported": "" if v is None else int(v["supported"]),
            "human_correct": labels.get(q["id"], {}).get("correct", ""),
            "human_supported": labels.get(q["id"], {}).get("supported", ""),
            "seconds": r["seconds"], "input_tokens": r["input_tokens"], "output_tokens": r["output_tokens"],
            "answer": r["answer"], "judge_reasoning": "" if v is None else v["reasoning"],
        }
        rows.append(row)
        cause = suggested_cause(q, result, checks)
        if cause:
            failures.append({
                "id": q["id"], "kind": q["kind"], "outcome": result, "suggested_cause": cause,
                "your_cause": "", "expected_retrieved": checks["expected_retrieved"],
                "question": q["question"], "answer": r["answer"],
            })
    write_csv(EVAL / "results.csv", rows)
    write_csv(EVAL / "failures.csv", failures)
    if (EVAL / "failures.csv").exists() and not failures:
        (EVAL / "failures.csv").unlink()

    counts = {}
    for row in rows:
        counts[row["outcome"]] = counts.get(row["outcome"], 0) + 1
    by_kind = {}
    for row in rows:
        by_kind.setdefault(row["kind"], {}).setdefault(row["outcome"], 0)
        by_kind[row["kind"]][row["outcome"]] += 1
    answerable = [r for r in rows if r["kind"] != "unanswerable"]
    code = {
        "searched": sum(r["searched"] for r in rows),
        "all_citations_valid": sum(r["citations_valid"] for r in rows),
        "answerable_with_citation": sum(r["n_citations"] > 0 for r in answerable),
        "answerable_citing_expected_passage": sum(r["expected_cited"] for r in answerable),
        "refused": sum(r["refused"] for r in rows),
        "guardrail_fired": sum(r["guardrail_fired"] for r in rows),
        "guardrail_withheld": sum(r["guardrail_withheld"] for r in rows),
        "call_limit_hit": sum(r["call_limit_hit"] for r in rows),
    }
    summary = {
        "questions": len(rows),
        "outcomes": counts,
        "outcomes_by_kind": by_kind,
        "code_checks": code,
        "judge_vs_human": agreement(verdicts, labels),
        "cost": cost_per_question([answers[r["id"]] for r in rows], [verdicts[r["id"]] for r in rows if r["id"] in verdicts]),
    }
    (EVAL / "summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")

    print(f"\nOutcomes on {len(rows)} questions:")
    for name in ("correct", "unsupported", "wrong answer", "wrong refusal", "correct refusal", "answered unanswerable", "not judged"):
        if name in counts:
            print(f"  {name:<24}{counts[name]:>4}")
    print("\nCode checks:", ", ".join(f"{k} {v}" for k, v in code.items()))
    agree = summary["judge_vs_human"]
    if agree["correct"]["n"]:
        print(f"Judge vs your grades on {agree['correct']['n']} answers: "
              f"correct {agree['correct']['agreement']:.0%} agreement (kappa {agree['correct']['cohen_kappa']}), "
              f"supported {agree['supported']['agreement']:.0%} (kappa {agree['supported']['cohen_kappa']})")
    else:
        print("No human grades yet: grade eval/grading_sheet.md into eval/human_labels.csv, then run again.")
    c = summary["cost"]
    print(f"Cost per question: {c['agent_input_tokens_per_question']:.0f} input + "
          f"{c['agent_output_tokens_per_question']:.0f} output tokens, "
          f"{c['agent_model_calls_per_question']} model calls, {c['seconds_per_question_mean']} s on average, "
          f"${c['agent_usd_per_question']:.5f} (judge ${c['judge_usd_per_question']:.5f})")
    if failures:
        print(f"\n{len(failures)} failures with a suggested cause in eval/failures.csv:")
        for f in failures:
            print(f"  {f['id']:<5} {f['outcome']:<22} -> {f['suggested_cause']}")
    print("\nSaved in eval/: retrieval.csv, results.csv, summary.json, grading_sheet.md, agreement.csv, failures.csv")


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate retrieval and the agent.")
    parser.add_argument("--retrieval-only", action="store_true", help="only the hit-rate comparison")
    parser.add_argument("--answers-only", action="store_true", help="agent answers and grading sheet, no judge")
    parser.add_argument("--fresh", action="store_true", help="ignore cached answers and verdicts")
    args = parser.parse_args()

    questions = load_questions()
    kinds = {k: sum(q["kind"] == k for q in questions) for k in ("single", "multi", "unanswerable")}
    print(f"{len(questions)} questions: " + ", ".join(f"{v} {k}" for k, v in kinds.items()) + "\n")
    evaluate_retrieval(questions)
    if not args.retrieval_only:
        asyncio.run(end_to_end(questions, args.fresh, args.answers_only))


if __name__ == "__main__":
    main()
