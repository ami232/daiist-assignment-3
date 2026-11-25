"""
Assignment 3: evaluation (`main.py evaluate`). Everything is saved in eval/.

Stages (all run by default; EVAL_STAGES=retrieval,answers,judge,demo picks some):

  retrieval  hit rate at k=1,3,5 for the two chunking designs x vector/hybrid,
             with a lenient and a strict hit test, eval/retrieval.csv +
             retrieval.png, and the choice of design (by the strict test:
             best hit@5, then hit@1, then fewer words) written to index/config.json
  answers    the agent on every question with the chosen design, cached in
             eval/answers.jsonl, plus code checks (citations, refusals)
  judge      LLM judge with eval/judge_rubric.md, cached in eval/judge.csv
  demo       add-document demo on a temporary copy of the index
  (always)   agreement with eval/human_labels.csv, eval/failures.csv, cost,
             eval/summary.json

One agent model and one judge model are pinned for a whole run (no fallback).
If a daily quota runs out the run saves what it has and stops; run it again
after 09:00 Madrid and it continues from the caches on the same models.

Environment:
  EVAL_STAGES        comma list of stages, default all
  EVAL_FRESH=1       ignore the answer / judge / demo caches
  EVAL_AGENT_MODEL   default gemini-3.5-flash-lite
  EVAL_JUDGE_MODEL   default gemini-3.8-flash
"""

from __future__ import annotations

import asyncio
import csv
import hashlib
import json
import os
import shutil
import statistics
import sys
import tempfile
import time
import warnings
from pathlib import Path

warnings.filterwarnings("ignore", category=RuntimeWarning)

import agent as agent_module
import index as index_stage
import rag

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
ANSWERS = EVAL / "answers.jsonl"
JUDGE = EVAL / "judge.csv"
RUBRIC = EVAL / "judge_rubric.md"
HUMAN = EVAL / "human_labels.csv"
RETRIEVAL_CSV = EVAL / "retrieval.csv"
RETRIEVAL_DETAIL = EVAL / "retrieval_detail.csv"
RETRIEVAL_PNG = EVAL / "retrieval.png"
FAILURES = EVAL / "failures.csv"
SUMMARY = EVAL / "summary.json"
DEMO_MD = EVAL / "add_document_demo.md"
DEMO_JSON = EVAL / "add_document_demo.json"

ALL_STAGES = ("retrieval", "answers", "judge", "demo")
STAGES = tuple(
    s.strip().lower() for s in os.environ.get("EVAL_STAGES", ",".join(ALL_STAGES)).split(",") if s.strip()
)
FRESH = os.environ.get("EVAL_FRESH", "") not in ("", "0")
AGENT_MODEL = os.environ.get("EVAL_AGENT_MODEL", "gemini-3.5-flash-lite")
JUDGE_MODEL = os.environ.get("EVAL_JUDGE_MODEL", "gemini-3.8-flash")

KS = (1, 3, 5)
CONFIGS = [("fixed", "vector"), ("fixed", "hybrid"), ("structure", "vector"), ("structure", "hybrid")]
DESIGN_LABEL = {"fixed": "A fixed", "structure": "B structure"}

# Paid-tier standard prices in USD per 1 million tokens (input, output incl. thinking),
# from https://ai.google.dev/gemini-api/docs/pricing, read on 2026-11-24.
PRICES = {
    "gemini-3.5-flash-lite": (0.30, 2.50),
    "gemini-3.1-flash-lite": (0.25, 1.50),
    "gemini-3-flash-preview": (0.50, 3.00),
    "gemini-3.8-flash": (0.75, 3.75),
}

DEMO_DOC = {"doc_id": "reg_2025_2151", "celex": "32025R2151", "eli": "reg_del/2025/2151/oj"}
DEMO_QUESTION = "What is the EU threshold for concession contracts from 2026?"


def say(*args) -> None:
    print(*args, flush=True)


def sha(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def read_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if (r.get("question") or "").strip()]
    for row in rows:
        row["kind"] = row["kind"].strip().lower()
        sources = [x.strip() for x in row["expected_source"].split(";") if x.strip()]
        locations = [x.strip() for x in row["expected_location"].split(";") if x.strip()]
        row["expected"] = list(zip(sources, locations))
    return rows


def passage_in(chunks: list[dict], source: str, location: str) -> bool:
    return any(c["doc_id"] == source and location in c["locations"] for c in chunks)


def percent(value: float | None) -> str:
    return "n/a" if value is None else f"{100 * value:.0f}%"


def mean(values: list[float]) -> float | None:
    return sum(values) / len(values) if values else None


# --------------------------------------------------------------------------
# 1 + 2. Retrieval: hit rates and the choice of design
# --------------------------------------------------------------------------

def main_locations(design: str) -> dict[str, str]:
    """chunk_id -> the location with most words in that chunk. Recomputed from
    the chunking (same ids as the index), so it costs no embeddings."""
    return {c["chunk_id"]: c["main_location"] for c in index_stage.chunk_corpus(design)}


def choose(rows: list[dict], prefix: str = "") -> tuple[dict, str]:
    """Best hit@5, then best hit@1, then fewer words in the prompt."""
    h5, h1 = f"{prefix}hit@5", f"{prefix}hit@1"
    best = sorted(rows, key=lambda r: (-r[h5], -r[h1], r["mean_words_k5"]))[0]
    ties_5 = [r for r in rows if r[h5] == best[h5]]
    ties_1 = [r for r in ties_5 if r[h1] == best[h1]]
    if len(ties_5) == 1:
        why = f"it has the best hit@5 ({percent(best[h5])})"
    elif len(ties_1) == 1:
        why = (f"{len(ties_5)} configurations tie on hit@5 ({percent(best[h5])}) and it has the best "
               f"hit@1 among them ({percent(best[h1])})")
    else:
        why = (f"{len(ties_1)} configurations tie on hit@5 ({percent(best[h5])}) and hit@1 "
               f"({percent(best[h1])}) and it adds the fewest words to the prompt ({best['mean_words_k5']})")
    return best, why


def stage_retrieval(questions: list[dict]) -> bool:
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    singles = [q for q in answerable if q["kind"] == "single"]
    multis = [q for q in answerable if q["kind"] == "multi"]
    say(f"\n== Retrieval: {len(answerable)} answerable questions ({len(singles)} single, {len(multis)} multi)")

    # Two hit tests.
    #   lenient: a retrieved chunk of the expected document whose locations INCLUDE the expected one
    #   strict:  ... whose MAIN location (most words in the chunk) IS the expected one
    # They differ only for design A, where a window can span several articles.
    main_of = {design: main_locations(design) for design in index_stage.DESIGNS}
    summary_rows, detail_rows = [], []
    kinds = [q["kind"] for q in answerable]
    try:
        for design, mode in CONFIGS:
            hits = {(test, k): {"all": [], "any": []} for test in ("", "strict_") for k in KS}
            words_at_5 = []
            for q in answerable:
                results = rag.search(q["question"], design=design, k=max(KS), mode=mode)
                words_at_5.append(sum(int(r["words"]) for r in results[:5]))
                ranks = {"": [], "strict_": []}
                for source, location in q["expected"]:
                    ranks[""].append(next((i for i, r in enumerate(results, start=1)
                                           if r["doc_id"] == source and location in r["locations"]), 0))
                    ranks["strict_"].append(next((i for i, r in enumerate(results, start=1)
                                                  if r["doc_id"] == source
                                                  and main_of[design].get(r["chunk_id"], r["location"]) == location), 0))
                for test in ("", "strict_"):
                    for k in KS:
                        found = [0 < rank <= k for rank in ranks[test]]
                        hits[(test, k)]["all"].append(all(found))
                        hits[(test, k)]["any"].append(any(found))
                detail_rows.append({
                    "design": design, "mode": mode, "id": q["id"], "kind": q["kind"],
                    "expected": ";".join(f"{s} | {l}" for s, l in q["expected"]),
                    "ranks": ";".join(str(r) if r else "-" for r in ranks[""]),
                    "strict_ranks": ";".join(str(r) if r else "-" for r in ranks["strict_"]),
                    "top5": "; ".join(f"{r['doc_id']} | {'+'.join(r['locations'])}" for r in results[:5]),
                    "top5_main": "; ".join(main_of[design].get(r["chunk_id"], r["location"]) for r in results[:5]),
                })
            row = {"design": design, "mode": mode, "questions": len(answerable)}
            for test in ("", "strict_"):
                for k in KS:
                    all_hits, any_hits = hits[(test, k)]["all"], hits[(test, k)]["any"]
                    # single: found; multi: all passages found
                    row[f"{test}hit@{k}"] = round(mean(all_hits), 4)
                    row[f"{test}single_hit@{k}"] = round(mean([h for h, kind in zip(all_hits, kinds) if kind == "single"]), 4)
                    row[f"{test}multi_all@{k}"] = round(mean([h for h, kind in zip(all_hits, kinds) if kind == "multi"]), 4)
                    row[f"{test}multi_any@{k}"] = round(mean([h for h, kind in zip(any_hits, kinds) if kind == "multi"]), 4)
            row["mean_words_k5"] = round(mean(words_at_5))
            summary_rows.append(row)
    except index_stage.QuotaExceeded as error:
        say(f"\nSTOPPED: the embedding quota ran out while embedding the questions ({error}).\n"
            "Query vectors embedded so far are cached. Run again after 09:00 Madrid.")
        return False

    with RETRIEVAL_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(summary_rows[0]))
        writer.writeheader()
        writer.writerows(summary_rows)
    with RETRIEVAL_DETAIL.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(detail_rows[0]))
        writer.writeheader()
        writer.writerows(detail_rows)

    for test, title in (("", "Lenient: expected location is among the chunk's locations"),
                        ("strict_", "Strict: expected location is the chunk's main location (most words)")):
        say(f"\n{title}")
        say(f"{'design':<13}{'mode':<8}{'hit@1':>7}{'hit@3':>7}{'hit@5':>7}   "
            f"{'multi all@5':>11}{'multi any@5':>12}{'words@5':>9}")
        for row in summary_rows:
            say(f"{DESIGN_LABEL[row['design']]:<13}{row['mode']:<8}{percent(row[test + 'hit@1']):>7}"
                f"{percent(row[test + 'hit@3']):>7}{percent(row[test + 'hit@5']):>7}   "
                f"{percent(row[test + 'multi_all@5']):>11}{percent(row[test + 'multi_any@5']):>12}"
                f"{row['mean_words_k5']:>9}")
    say("(for multi questions the main number needs both passages in the top k)")

    plot_retrieval(summary_rows)

    # The design is chosen on the STRICT test. The lenient test favours design A:
    # its windows span several articles, and a chunk counts as a hit for an
    # article even when that article is only a small part of the chunk.
    best, why = choose(summary_rows, "strict_")
    lenient_best, lenient_why = choose(summary_rows)
    say(f"\nChosen (strict test): {DESIGN_LABEL[best['design']]} + {best['mode']}, k=5, because {why}.")
    if (lenient_best["design"], lenient_best["mode"]) == (best["design"], best["mode"]):
        say("The lenient test picks the same configuration.")
    else:
        say(f"NOTE: the lenient test would pick {DESIGN_LABEL[lenient_best['design']]} + {lenient_best['mode']} "
            f"instead, because {lenient_why}.")
    config = {"design": best["design"], "mode": best["mode"], "k": 5}
    path = index_stage.index_dir() / "config.json"
    shown = path.relative_to(ROOT) if path.is_relative_to(ROOT) else path
    current = json.loads(path.read_text(encoding="utf-8")) if path.exists() else None
    if current == config:
        say(f"{shown} already holds this choice; not rewritten.")
    else:
        path.write_text(json.dumps(config, indent=2) + "\n", encoding="utf-8")
        say(f"Written to {shown}.")
    return True


def plot_retrieval(rows: list[dict]) -> None:
    import matplotlib

    matplotlib.use("Agg")
    import matplotlib.pyplot as plt

    labels = [f"{DESIGN_LABEL[r['design']]}\n{r['mode']}" for r in rows]
    colors = {1: "#9ecae1", 3: "#4292c6", 5: "#08519c"}
    fig, axes = plt.subplots(1, 2, figsize=(12, 4.6), sharey=True)
    width = 0.26
    panels = (("", "Lenient: expected location among the chunk's locations"),
              ("strict_", "Strict: expected location is the chunk's main location"))
    for ax, (test, title) in zip(axes, panels):
        for offset, k in enumerate(KS):
            xs = [i + (offset - 1) * width for i in range(len(rows))]
            values = [100 * r[f"{test}hit@{k}"] for r in rows]
            bars = ax.bar(xs, values, width, label=f"hit@{k}", color=colors[k])
            for bar, value in zip(bars, values):
                ax.text(bar.get_x() + bar.get_width() / 2, value + 1, f"{value:.0f}", ha="center", fontsize=8)
        ax.set_xticks(range(len(rows)))
        ax.set_xticklabels(labels)
        ax.set_ylim(0, 110)
        ax.set_title(title, fontsize=10)
        for side in ("top", "right"):
            ax.spines[side].set_visible(False)
    axes[0].set_ylabel("hit rate (%)")
    handles, names = axes[0].get_legend_handles_labels()
    fig.legend(handles, names, loc="lower center", ncol=3, frameon=False)
    fig.suptitle(f"Expected passage(s) in the top k, {rows[0]['questions']} answerable questions", fontsize=12)
    fig.tight_layout(rect=(0, 0.06, 1, 0.97))
    fig.savefig(RETRIEVAL_PNG, dpi=150)
    plt.close(fig)


# --------------------------------------------------------------------------
# 3 + 4. Agent answers and code checks
# --------------------------------------------------------------------------

def run_config() -> dict:
    config = rag.load_config()
    return {
        "design": config["design"], "mode": config["mode"], "k": config["k"],
        "agent_model": AGENT_MODEL,
        "agents_md": sha((ROOT / "AGENTS.md").read_text(encoding="utf-8"))[:12],
    }


def config_hash(config: dict) -> str:
    return sha(json.dumps(config, sort_keys=True))[:12]


def answer_key(question: str, chash: str) -> str:
    return sha(f"{chash}\n{question.strip()}")[:16]


def load_answers() -> dict[str, dict]:
    if not ANSWERS.exists():
        return {}
    rows = {}
    for line in ANSWERS.read_text(encoding="utf-8").splitlines():
        if line.strip():
            row = json.loads(line)
            rows[row["key"]] = row
    return rows


def code_checks(question: dict, result: dict) -> dict:
    retrieved = result["retrieved"]
    cited = rag.parse_citations(result["answer"])
    allowed = {(c["doc_id"], loc) for c in retrieved for loc in c["locations"]}
    refused = bool(result["refused"])
    answerable = question["kind"] != "unanswerable"
    return {
        "citations_valid": all(pair in allowed for pair in cited),
        "has_citation_or_refuses": bool(cited) or refused,
        "refused": refused,
        "refusal_correct": refused and not answerable,
        "refusal_wrong": refused and answerable,
        "missed_refusal": (not refused) and not answerable,
        "expected_retrieved": (all(passage_in(retrieved, s, l) for s, l in question["expected"])
                               if answerable else None),
    }


async def stage_answers(questions: list[dict]) -> bool:
    config = run_config()
    chash = config_hash(config)
    cache = {} if FRESH else load_answers()
    todo = [q for q in questions if answer_key(q["question"], chash) not in cache]
    say(f"\n== Answers: {DESIGN_LABEL[config['design']]} + {config['mode']}, k={config['k']}, "
        f"agent model {AGENT_MODEL} (pinned), config {chash}")
    say(f"   {len(questions) - len(todo)} cached, {len(todo)} to run")
    if FRESH and ANSWERS.exists():
        ANSWERS.unlink()
    if not todo:
        return True
    complete = True
    async with agent_module.Agent(interactive=False, model=AGENT_MODEL) as agent:
        for number, q in enumerate(todo, start=1):
            try:
                result = await agent.answer(q["question"])
            except agent_module.DailyQuotaExhausted as error:
                say(f"\nSTOPPED: {error}\n{number - 1} new answers saved. Run again after 09:00 Madrid; "
                    "finished questions are skipped.")
                complete = False
                break
            except index_stage.QuotaExceeded as error:
                say(f"\nSTOPPED: embedding quota used up ({error}). Run again after 09:00 Madrid.")
                complete = False
                break
            except Exception as error:  # noqa: BLE001 - one bad question must not lose the run
                if "QuotaExceeded" in repr(error) or "embedding" in str(error).lower() and "quota" in str(error).lower():
                    say(f"\nSTOPPED: embedding quota used up ({error}). Run again after 09:00 Madrid.")
                    complete = False
                    break
                say(f"   {q['id']} ERROR {type(error).__name__}: {str(error)[:200]} (not cached, will be retried)")
                complete = False
                continue
            row = {
                "key": answer_key(q["question"], chash), "config_hash": chash, "config": config,
                "id": q["id"], "kind": q["kind"], **result, "checks": code_checks(q, result),
            }
            with ANSWERS.open("a", encoding="utf-8") as f:
                f.write(json.dumps(row, ensure_ascii=False) + "\n")
            cache[row["key"]] = row
            flag = "refused" if row["refused"] else f"{len(row['citations'])} citations"
            guard = " guardrail" if row["guardrail_fired"] else ""
            say(f"   {q['id']} {q['kind']:<12} {flag}{guard}  {row['seconds']}s  [{number}/{len(todo)}]")
    return complete


def current_answers(questions: list[dict]) -> list[dict]:
    chash = config_hash(run_config())
    cache = load_answers()
    rows = []
    for q in questions:
        row = cache.get(answer_key(q["question"], chash))
        if row:
            row = dict(row, checks=code_checks(q, row), reference_answer=q["reference_answer"],
                       expected=q["expected"])
            rows.append(row)
    return rows


# --------------------------------------------------------------------------
# 5. LLM judge
# --------------------------------------------------------------------------

JUDGE_COLUMNS = ["id", "key", "judge_model", "rubric", "correct", "supported", "reason"]


def load_judgements() -> dict[tuple, dict]:
    if not JUDGE.exists():
        return {}
    with JUDGE.open(newline="", encoding="utf-8") as f:
        return {(r["key"], r["judge_model"], r["rubric"]): r for r in csv.DictReader(f)}


def judge_prompt(row: dict) -> str:
    evidence = "\n\n".join(
        f"[{c['doc_id']} | {'; '.join(c['locations'])}]\n{c['text']}" for c in row["retrieved"]
    ) or "(the agent retrieved nothing)"
    return (
        f"QUESTION:\n{row['question']}\n\n"
        f"KIND: {row['kind']}\n\n"
        f"REFERENCE ANSWER:\n{row['reference_answer']}\n\n"
        f"AGENT ANSWER:\n{row['answer']}\n\n"
        f"EVIDENCE (the passages the agent retrieved):\n{evidence}\n\n"
        'Reply with JSON only: {"correct": 0 or 1, "supported": 0 or 1, "reason": "one or two sentences"}'
    )


def call_judge(client, rubric: str, prompt: str) -> dict:
    from google.genai import types

    waits = 0
    while True:
        try:
            response = client.models.generate_content(
                model=JUDGE_MODEL, contents=prompt,
                config=types.GenerateContentConfig(
                    system_instruction=rubric, temperature=0, response_mime_type="application/json",
                ),
            )
            data = json.loads(response.text)
            return {"correct": int(bool(int(data["correct"]))), "supported": int(bool(int(data["supported"]))),
                    "reason": " ".join(str(data.get("reason", "")).split())}
        except Exception as error:  # noqa: BLE001 - sorted below
            text = str(error)
            if ("429" in text or "RESOURCE_EXHAUSTED" in text) and "PerDay" in text:
                raise agent_module.DailyQuotaExhausted(f"The daily Gemini quota is used up for {JUDGE_MODEL}.") from error
            retriable = any(x in text for x in ("429", "RESOURCE_EXHAUSTED", "503", "UNAVAILABLE")) or isinstance(
                error, (json.JSONDecodeError, KeyError, ValueError, TypeError))
            if retriable and waits < 6:
                waits += 1
                time.sleep(min(5 * 2 ** (waits - 1), 65))
                continue
            raise


def stage_judge(questions: list[dict]) -> bool:
    from google import genai

    from api_key import load_api_key

    rows = current_answers(questions)
    rubric = RUBRIC.read_text(encoding="utf-8")
    rubric_id = sha(rubric)[:8]
    cache = {} if FRESH else load_judgements()
    todo = [r for r in rows if (r["key"], JUDGE_MODEL, rubric_id) not in cache]
    say(f"\n== Judge: model {JUDGE_MODEL} (pinned), rubric {rubric_id}: "
        f"{len(rows) - len(todo)} cached, {len(todo)} to judge")
    if JUDGE_MODEL == AGENT_MODEL:
        say("   NOTE: the judge is the same model as the agent (limitation: it may share the agent's mistakes).")
    complete = len(rows) == len(questions)
    if todo:
        client = genai.Client(api_key=load_api_key())
        for row in todo:
            try:
                verdict = call_judge(client, rubric, judge_prompt(row))
            except agent_module.DailyQuotaExhausted as error:
                say(f"\nSTOPPED: {error} Run again after 09:00 Madrid; judged answers are kept.")
                complete = False
                break
            cache[(row["key"], JUDGE_MODEL, rubric_id)] = {
                "id": row["id"], "key": row["key"], "judge_model": JUDGE_MODEL, "rubric": rubric_id, **verdict,
            }
            write_judgements(cache)
            say(f"   {row['id']} correct={verdict['correct']} supported={verdict['supported']}")
    return complete


def write_judgements(cache: dict) -> None:
    with JUDGE.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=JUDGE_COLUMNS)
        writer.writeheader()
        for row in sorted(cache.values(), key=lambda r: (r["id"], r["judge_model"], r["rubric"])):
            writer.writerow({c: row[c] for c in JUDGE_COLUMNS})


def current_judgements(rows: list[dict]) -> dict[str, dict]:
    if not RUBRIC.exists():
        return {}
    rubric_id = sha(RUBRIC.read_text(encoding="utf-8"))[:8]
    cache = load_judgements()
    found = {}
    for row in rows:
        verdict = cache.get((row["key"], JUDGE_MODEL, rubric_id))
        if verdict:
            found[row["id"]] = {"correct": int(verdict["correct"]), "supported": int(verdict["supported"]),
                                "reason": verdict["reason"]}
    return found


# --------------------------------------------------------------------------
# 6. Agreement with the human labels
# --------------------------------------------------------------------------

def cohen_kappa(a: list[int], b: list[int]) -> float | None:
    n = len(a)
    if n == 0:
        return None
    observed = sum(x == y for x, y in zip(a, b)) / n
    p_a, p_b = sum(a) / n, sum(b) / n
    expected = p_a * p_b + (1 - p_a) * (1 - p_b)
    if expected == 1:
        return None  # both always give the same single label: kappa is undefined
    return (observed - expected) / (1 - expected)


def agreement(verdicts: dict[str, dict]) -> dict | None:
    if not HUMAN.exists():
        return None
    with HUMAN.open(newline="", encoding="utf-8") as f:
        human = {r["id"].strip(): r for r in csv.DictReader(f) if (r.get("id") or "").strip()}
    both = [i for i in human if i in verdicts]
    if not both:
        return {"human_labels": len(human), "compared": 0}
    out = {"human_labels": len(human), "compared": len(both), "disagreements": []}
    for field in ("correct", "supported"):
        mine = [int(human[i][field]) for i in both]
        judge = [verdicts[i][field] for i in both]
        kappa = cohen_kappa(mine, judge)
        out[field] = {
            "agreement": round(sum(x == y for x, y in zip(mine, judge)) / len(both), 4),
            "kappa": None if kappa is None else round(kappa, 4),
        }
        for i, x, y in zip(both, mine, judge):
            if x != y:
                out["disagreements"].append({
                    "id": i, "field": field, "human": x, "judge": y,
                    "human_notes": human[i].get("notes", ""), "judge_reason": verdicts[i]["reason"],
                })
    return out


# --------------------------------------------------------------------------
# 7. Failures
# --------------------------------------------------------------------------

def failures(rows: list[dict], verdicts: dict[str, dict]) -> list[dict]:
    out = []
    for row in rows:
        checks, verdict = row["checks"], verdicts.get(row["id"])
        correct = verdict["correct"] if verdict else None
        supported = verdict["supported"] if verdict else None
        answerable = row["kind"] != "unanswerable"
        failed = (
            correct == 0 or supported == 0 or not checks["citations_valid"]
            or checks["refusal_wrong"] or checks["missed_refusal"] or not checks["has_citation_or_refuses"]
        )
        if not failed:
            continue
        if answerable and checks["refused"]:
            cause = "wrong refusal" if checks["expected_retrieved"] else "retrieval miss"
        elif answerable and correct == 0:
            cause = "wrong answer from right passage" if checks["expected_retrieved"] else "retrieval miss"
        elif not answerable and checks["missed_refusal"]:
            cause = "unsupported claim"
        else:
            cause = "unsupported claim"
        out.append({
            "id": row["id"], "kind": row["kind"], "question": row["question"],
            "suggested_cause": cause,
            "final_cause": "",  # for the human: confirm, or change (e.g. to "bad test question")
            "expected": ";".join(f"{s} | {l}" for s, l in row["expected"]),
            "expected_retrieved": checks["expected_retrieved"],
            "refused": checks["refused"], "citations_valid": checks["citations_valid"],
            "judge_correct": correct, "judge_supported": supported,
            "judge_reason": verdict["reason"] if verdict else "",
            "guardrail_fired": row["guardrail_fired"],
            "answer": " ".join(row["answer"].split())[:600],
        })
    return out


def write_failures(rows: list[dict]) -> None:
    columns = ["id", "kind", "question", "suggested_cause", "final_cause", "expected", "expected_retrieved",
               "refused", "citations_valid", "judge_correct", "judge_supported", "judge_reason",
               "guardrail_fired", "answer"]
    previous = {}
    if FAILURES.exists():  # keep causes the human already filled in
        with FAILURES.open(newline="", encoding="utf-8") as f:
            previous = {r["id"]: r.get("final_cause", "") for r in csv.DictReader(f)}
    with FAILURES.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        for row in rows:
            row["final_cause"] = previous.get(row["id"], "")
            writer.writerow(row)


# --------------------------------------------------------------------------
# 8. Cost
# --------------------------------------------------------------------------

def p90(values: list[float]) -> float:
    ordered = sorted(values)
    return ordered[min(len(ordered) - 1, int(round(0.9 * (len(ordered) - 1))))]


def cost(rows: list[dict]) -> dict | None:
    if not rows:
        return None
    tokens_in = [r["input_tokens"] for r in rows]
    tokens_out = [r["output_tokens"] for r in rows]
    seconds = [r["seconds"] for r in rows]
    price_in, price_out = PRICES.get(AGENT_MODEL, (None, None))
    usd = None
    if price_in is not None:
        usd = statistics.mean(tokens_in) / 1e6 * price_in + statistics.mean(tokens_out) / 1e6 * price_out
    return {
        "model": AGENT_MODEL,
        "models_seen": sorted({r["model"] for r in rows}),
        "input_tokens": {"mean": round(statistics.mean(tokens_in)), "p90": round(p90(tokens_in))},
        "output_tokens": {"mean": round(statistics.mean(tokens_out)), "p90": round(p90(tokens_out))},
        "seconds": {"mean": round(statistics.mean(seconds), 1), "p90": round(p90(seconds), 1)},
        "model_calls_mean": round(statistics.mean(r["model_calls"] for r in rows), 2),
        "price_usd_per_million_tokens": {"input": price_in, "output": price_out},
        "usd_per_question": None if usd is None else round(usd, 6),
        "usd_per_1000_questions": None if usd is None else round(1000 * usd, 2),
        "note": "seconds include waits on free-tier rate limits; prices are the paid standard tier",
    }


# --------------------------------------------------------------------------
# 9. Add-document demo, on a copy of the index
# --------------------------------------------------------------------------

async def stage_demo() -> bool:
    config = run_config()
    doc_path = index_stage.download_document(DEMO_DOC, ROOT / "docs_to_add")
    if doc_path is None:
        say("\n== Demo: could not download Regulation 2025/2151; skipped.")
        return False
    demo_key = sha(json.dumps([config, index_stage.file_sha256(doc_path), DEMO_QUESTION], sort_keys=True))[:12]
    if not FRESH and DEMO_JSON.exists() and json.loads(DEMO_JSON.read_text(encoding="utf-8")).get("key") == demo_key:
        say("\n== Demo: cached (eval/add_document_demo.md)")
        return True
    say(f"\n== Demo: add {doc_path.relative_to(ROOT)} to a temporary copy of the index")
    temp = Path(tempfile.mkdtemp(prefix="index_demo_"))
    previous = os.environ.get("INDEX_DIR")
    try:
        shutil.copytree(index_stage.index_dir(), temp / "index")
        os.environ["INDEX_DIR"] = str(temp / "index")
        async with agent_module.Agent(interactive=False, model=AGENT_MODEL) as agent:
            before = await agent.answer(DEMO_QUESTION)
            added = await agent._session.call_tool("add_document", {"path": str(doc_path.relative_to(ROOT))})
            added_text = "\n".join(getattr(c, "text", "") for c in added.content).strip()
            again = await agent._session.call_tool("add_document", {"path": str(doc_path.relative_to(ROOT))})
            again_text = "\n".join(getattr(c, "text", "") for c in again.content).strip()
            after = await agent.answer(DEMO_QUESTION)
    except (agent_module.DailyQuotaExhausted, index_stage.QuotaExceeded) as error:
        say(f"STOPPED: {error} Run again after 09:00 Madrid.")
        return False
    finally:
        if previous is None:
            os.environ.pop("INDEX_DIR", None)
        else:
            os.environ["INDEX_DIR"] = previous
        shutil.rmtree(temp, ignore_errors=True)

    def block(result: dict) -> str:
        sources = ", ".join(result["citations"]) or "none"
        top = ", ".join(f"[{c['doc_id']} | {c['location']}]" for c in result["retrieved"][:5]) or "none"
        searches = "; ".join(f"`{c['args'].get('query', '')}`" for c in result["tool_calls"] if c["name"] == "search")
        guard = "; ".join(f"{e['reason']} -> {e['action']}" for e in result["guardrail_events"]) or "did not fire"
        return (f"> {result['answer'].strip().replace(chr(10), chr(10) + '> ')}\n\n"
                f"- Searches: {searches or 'none'}\n- Retrieved: {top}\n- Citations: {sources}\n"
                f"- Refused: {result['refused']}\n- Citation guardrail: {guard}")

    def record(result: dict) -> dict:
        return {
            "answer": result["answer"], "raw_answer": result["raw_answer"], "refused": result["refused"],
            "citations": result["citations"], "guardrail_events": result["guardrail_events"],
            "searches": [c["args"].get("query", "") for c in result["tool_calls"] if c["name"] == "search"],
            "retrieved": [f"[{c['doc_id']} | {c['location']}]" for c in result["retrieved"]],
            "model": result["model"],
        }

    text = (
        "# Add-document demo\n\n"
        f"Question: **{DEMO_QUESTION}**\n\n"
        f"Document added: `{doc_path.relative_to(ROOT)}` (Delegated Regulation (EU) 2025/2151, "
        "concession threshold for 2026-2027, CELEX 32025R2151, © European Union).\n\n"
        f"Run on a temporary copy of `index/` (INDEX_DIR), so the committed index is unchanged and the main "
        f"evaluation still counts this question as unanswerable. Design {config['design']}, mode {config['mode']}, "
        f"k={config['k']}, agent model {AGENT_MODEL}.\n\n"
        f"## Before\n\n{block(before)}\n\n"
        f"## add_document\n\nFirst call: `{added_text}`\n\nSecond call with the same file: `{again_text}`\n\n"
        f"## After\n\n{block(after)}\n"
    )
    DEMO_MD.write_text(text, encoding="utf-8")
    DEMO_JSON.write_text(json.dumps({
        "key": demo_key, "config": config, "question": DEMO_QUESTION, "add_document": added_text,
        "add_document_again": again_text,
        "before": record(before),
        "after": record(after),
    }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    say(f"   before: refused={before['refused']}   add: {added_text}   after: refused={after['refused']}, "
        f"citations {', '.join(after['citations']) or 'none'}")
    return True


# --------------------------------------------------------------------------
# 10. Summary
# --------------------------------------------------------------------------

def summarise(questions: list[dict], complete: dict[str, bool]) -> dict:
    rows = current_answers(questions)
    verdicts = current_judgements(rows)
    answerable = [r for r in rows if r["kind"] != "unanswerable"]
    unanswerable = [r for r in rows if r["kind"] == "unanswerable"]
    judged = [r for r in rows if r["id"] in verdicts]
    failed = failures(rows, verdicts)
    if rows:
        write_failures(failed)
    causes: dict[str, int] = {}
    for f in failed:
        causes[f["suggested_cause"]] = causes.get(f["suggested_cause"], 0) + 1

    retrieval = []
    if RETRIEVAL_CSV.exists():
        with RETRIEVAL_CSV.open(newline="", encoding="utf-8") as f:
            retrieval = list(csv.DictReader(f))

    summary = {
        "generated": time.strftime("%Y-%m-%d %H:%M:%S"),
        "config": run_config(),
        "judge_model": JUDGE_MODEL,
        "judge_same_as_agent": JUDGE_MODEL == AGENT_MODEL,
        "stages_run": list(STAGES),
        "complete": complete,
        "questions": {"total": len(questions), "answered": len(rows), "judged": len(judged)},
        "retrieval": retrieval,
        "end_to_end": None,
        "agreement": agreement(verdicts),
        "failures_by_suggested_cause": causes,
        "cost": cost(rows),
        "add_document_demo": json.loads(DEMO_JSON.read_text(encoding="utf-8")) if DEMO_JSON.exists() else None,
    }
    if rows:
        summary["end_to_end"] = {
            "correct": sum(verdicts[r["id"]]["correct"] for r in judged),
            "correct_rate": mean([verdicts[r["id"]]["correct"] for r in judged]),
            "unsupported": sum(1 - verdicts[r["id"]]["supported"] for r in judged),
            "unsupported_rate": mean([1 - verdicts[r["id"]]["supported"] for r in judged]),
            "correct_answerable_rate": mean([verdicts[r["id"]]["correct"] for r in judged if r["kind"] != "unanswerable"]),
            "correct_refusals": sum(r["checks"]["refusal_correct"] for r in unanswerable),
            "unanswerable": len(unanswerable),
            "wrong_refusals": sum(r["checks"]["refusal_wrong"] for r in answerable),
            "answerable": len(answerable),
            "invalid_citations": sum(not r["checks"]["citations_valid"] for r in rows),
            "no_citation_and_no_refusal": sum(not r["checks"]["has_citation_or_refuses"] for r in rows),
            "expected_passage_retrieved_by_agent": sum(bool(r["checks"]["expected_retrieved"]) for r in answerable),
            "guardrail_fired": sum(r["guardrail_fired"] for r in rows),
            "failures": len(failed),
        }
    SUMMARY.write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return summary


def print_summary(summary: dict) -> None:
    say("\n" + "=" * 72)
    config = summary["config"]
    say(f"SUMMARY  design {config['design']}, mode {config['mode']}, k={config['k']}, "
        f"agent {config['agent_model']}, judge {summary['judge_model']}")
    q = summary["questions"]
    say(f"Questions: {q['total']} total, {q['answered']} answered, {q['judged']} judged")
    for row in summary["retrieval"]:
        say(f"  retrieval {row['design']:<10}{row['mode']:<7} hit@1 {percent(float(row['hit@1']))}  "
            f"hit@3 {percent(float(row['hit@3']))}  hit@5 {percent(float(row['hit@5']))}  | strict "
            f"{percent(float(row['strict_hit@1']))} / {percent(float(row['strict_hit@3']))} / "
            f"{percent(float(row['strict_hit@5']))}  words@5 {row['mean_words_k5']}")
    e = summary["end_to_end"]
    if e:
        say(f"Correct (judge): {e['correct']}/{q['judged']} ({percent(e['correct_rate'])})   "
            f"Unsupported (judge): {e['unsupported']}/{q['judged']}")
        say(f"Correct refusals: {e['correct_refusals']}/{e['unanswerable']}   "
            f"Wrong refusals: {e['wrong_refusals']}/{e['answerable']}   "
            f"Invalid citations: {e['invalid_citations']}   Guardrail fired: {e['guardrail_fired']}")
        say(f"Failures: {e['failures']}  by suggested cause: {summary['failures_by_suggested_cause']}")
    else:
        say("End-to-end: not run yet.")
    a = summary["agreement"]
    if a and a.get("compared"):
        say(f"Agreement with my labels ({a['compared']} answers): correct {percent(a['correct']['agreement'])} "
            f"(kappa {a['correct']['kappa']}), supported {percent(a['supported']['agreement'])} "
            f"(kappa {a['supported']['kappa']}); {len(a['disagreements'])} disagreements")
    else:
        say("Agreement: no human labels to compare yet (run grade.py).")
    c = summary["cost"]
    if c:
        say(f"Per question: {c['input_tokens']['mean']} tokens in (p90 {c['input_tokens']['p90']}), "
            f"{c['output_tokens']['mean']} out (p90 {c['output_tokens']['p90']}), "
            f"{c['seconds']['mean']}s (p90 {c['seconds']['p90']}s), "
            f"${c['usd_per_question']} at paid prices (${c['usd_per_1000_questions']} per 1,000)")
    incomplete = [stage for stage, done in summary["complete"].items() if not done]
    if incomplete:
        say(f"INCOMPLETE stages: {', '.join(incomplete)}. Run `uv run python main.py evaluate` again to continue.")
    say("=" * 72)


def main() -> None:
    unknown = [s for s in STAGES if s not in ALL_STAGES]
    if unknown:
        raise SystemExit(f"Unknown stage(s) in EVAL_STAGES: {', '.join(unknown)}. Use: {', '.join(ALL_STAGES)}")
    EVAL.mkdir(exist_ok=True)
    questions = read_questions()
    complete: dict[str, bool] = {}
    if "retrieval" in STAGES:
        complete["retrieval"] = stage_retrieval(questions)
    if "answers" in STAGES:
        complete["answers"] = asyncio.run(stage_answers(questions))
    if "judge" in STAGES:
        complete["judge"] = stage_judge(questions)
    if "demo" in STAGES:
        complete["demo"] = asyncio.run(stage_demo())
    print_summary(summarise(questions, complete))


if __name__ == "__main__":
    main()
