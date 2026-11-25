"""
Assignment 3: evaluation (`main.py evaluate`).

1. Validate eval/questions.csv against the index (and its frozen hash, if frozen).
2. Retrieval: hit rate at k = 1, 3, 5 for each design, on source AND location.
3. Run the real agent (agent.py, over MCP) on every question, approvals denied.
4. Code checks: citations exist, were returned to the agent, markers, guardrails.
5. LLM judge with a rubric and the retrieved passages as evidence.
6. A blind sheet for human grading, then agreement with eval/human_labels.csv.
7. Provisional failure classes, tokens and latency; everything saved in eval/.

    uv run python main.py evaluate
    uv run python evaluate.py --retrieval-only    # stage 2 only (question embeddings are cached)
    uv run python evaluate.py --freeze            # record the reviewed questions' hash

Answers and verdicts are saved one question at a time and reused on the next
run while the question, agent configuration and answer are unchanged, so an
interrupted run (for example at the daily quota) resumes where it stopped.
"""

import argparse
import asyncio
import csv
import hashlib
import json
import re
import statistics
import sys
from contextlib import AsyncExitStack
from datetime import datetime, timezone
from pathlib import Path

from pydantic import BaseModel, Field

import index

ROOT = Path(__file__).resolve().parent
EVAL_DIR = ROOT / "eval"
QUESTIONS = EVAL_DIR / "questions.csv"
FROZEN = EVAL_DIR / "questions.frozen"
HUMAN_LABELS = EVAL_DIR / "human_labels.csv"
RETRIEVAL_RESULTS = EVAL_DIR / "retrieval.json"
ANSWERS = EVAL_DIR / "answers.jsonl"
VERDICTS = EVAL_DIR / "verdicts.jsonl"
RESULTS = EVAL_DIR / "results.json"
SUMMARY = EVAL_DIR / "summary.json"
TO_GRADE = EVAL_DIR / "to_grade.md"

KS = [1, 3, 5]
JUDGE_MODEL = "gemini-3.5-flash"  # a stronger model than the agent's, as in the teacher's evaluate.py
RUBRIC_VERSION = "v1"
MARKERS = {"NOT IN CORPUS:": "refusal", "NEED DETAILS:": "clarification", "WITHHELD:": "withheld"}


# 1. The test set.

def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read_questions():
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if (r.get("question") or "").strip()]
    for row in rows:
        row["kind"] = row["kind"].strip().lower()
        sources = [s.strip() for s in row["expected_source"].split(";") if s.strip()]
        locations = [s.strip() for s in row["expected_location"].split(";") if s.strip()]
        row["expected"] = [{"source": s, "location": l} for s, l in zip(sources, locations)]
        row["mapping_ok"] = len(sources) == len(locations)
    return rows


def indexed_locations():
    """{source: [(locations list, first page, last page)]} over every chunk of every design."""
    db = index.open_index()
    found = {}
    for design in index.DESIGNS:
        got = index.design_collection(db, design).get(include=["metadatas"])
        for meta in got["metadatas"]:
            found.setdefault(meta["source"], []).append(
                (meta["locations"].split(" | "), meta.get("first_page"), meta.get("last_page")))
    return found


def validate_questions(rows, known):
    """Schema, counts and mappings. Returns a list of problems; empty means valid."""
    problems = []
    kinds = [r["kind"] for r in rows]
    if len(rows) < 30:
        problems.append(f"{len(rows)} questions, need 30")
    if kinds.count("multi") < 5 or kinds.count("unanswerable") < 5:
        problems.append("need at least 5 multi and 5 unanswerable questions")
    if len({r["id"] for r in rows}) != len(rows):
        problems.append("question ids are not unique")
    for r in rows:
        if r["kind"] not in ("single", "multi", "unanswerable"):
            problems.append(f"{r['id']}: unknown kind {r['kind']!r}")
        if r["kind"] == "unanswerable":
            if r["expected_source"].strip() or r["expected_location"].strip():
                problems.append(f"{r['id']}: unanswerable but has an expected source or location")
            continue
        if not r["expected"] or not r["mapping_ok"]:
            problems.append(f"{r['id']}: expected_source and expected_location must pair up one to one")
        if r["kind"] == "multi" and len(r["expected"]) < 2:
            problems.append(f"{r['id']}: multi needs two passages")
        for pair in r["expected"]:
            chunks = known.get(pair["source"], [])
            if not chunks:
                problems.append(f"{r['id']}: source {pair['source']} is not in the index")
            elif not any(location_matches(pair["location"], *c) for c in chunks):
                problems.append(f"{r['id']}: no chunk of {pair['source']} has location {pair['location']!r}")
    return problems


# 2. Retrieval: does a top-k chunk come from the right document AND the right place?

def normalise_location(text):
    text = " ".join(text.split())
    article = re.match(r"^(Annex [IVX]+, )?(?:Art\.?|Article)\s*(\d+[a-z]?)", text)
    if article:
        return f"{article.group(1) or ''}Article {article.group(2)}"
    recital = re.match(r"^Recital\s*\(?(\d+)\)?", text)
    if recital:
        return f"Recital ({recital.group(1)})"
    return text


def location_matches(expected, locations, first_page=None, last_page=None):
    """True if a chunk's locations cover the expected one.

    "Article 7" matches a chunk containing Article 7; "Section 4.4" also matches
    4.4.7 (a part of it); "p. 12" matches a chunk spanning PDF page 12.
    """
    pages = re.match(r"^pp?\.\s*(\d+)(?:\s*-\s*(\d+))?$", expected.strip())
    if pages:
        low, high = int(pages.group(1)), int(pages.group(2) or pages.group(1))
        return first_page is not None and first_page <= high and last_page >= low
    wanted = normalise_location(expected)
    return any(loc == wanted or loc.startswith(wanted + ".") or loc.startswith(wanted + ",") for loc in locations)


def chunk_matches(meta, pair):
    """Source first: the right page or article in the wrong document is not a hit."""
    return meta["source"] == pair["source"] and location_matches(
        pair["location"], meta["locations"].split(" | "), meta.get("first_page"), meta.get("last_page"))


def retrieval_for_design(design, rows, vectors):
    """Top-5 chunks per question for one design, and the hit-rate metrics."""
    collection = index.design_collection(index.open_index(), design)
    result = collection.query(query_embeddings=vectors, n_results=max(KS), include=["metadatas", "documents", "distances"])
    answerable = [i for i, r in enumerate(rows) if r["kind"] != "unanswerable"]
    multi = [i for i, r in enumerate(rows) if r["kind"] == "multi"]
    per_question, metrics = [], {"design": design, "settings": index.DESIGNS[design], "chunks": collection.count()}
    for i, row in enumerate(rows):
        metas, docs, dists = result["metadatas"][i], result["documents"][i], result["distances"][i]
        per_question.append({
            "id": row["id"], "kind": row["kind"],
            "retrieved": [{"id": rid, "source": m["source"], "location": m["location"],
                           "score": round(1 - d, 4), "words": len(doc.split())}
                          for rid, m, doc, d in zip(result["ids"][i], metas, docs, dists)],
            "first_match_rank": next((rank for rank, m in enumerate(metas, start=1)
                                      if any(chunk_matches(m, p) for p in row["expected"])), None),
            "evidence_found_at": {k: [any(chunk_matches(m, p) for m in metas[:k]) for p in row["expected"]] for k in KS},
        })
    for k in KS:
        hits = [per_question[i]["first_match_rank"] is not None and per_question[i]["first_match_rank"] <= k
                for i in answerable]
        all_evidence = [all(per_question[i]["evidence_found_at"][k]) for i in multi]
        words = [sum(r["words"] for r in q["retrieved"][:k]) for q in per_question]
        metrics[f"hit@{k}"] = {"hits": sum(hits), "n": len(hits), "rate": round(sum(hits) / len(hits), 3)}
        metrics[f"multi_all_evidence@{k}"] = {"hits": sum(all_evidence), "n": len(all_evidence),
                                              "rate": round(sum(all_evidence) / len(all_evidence), 3) if multi else None}
        metrics[f"avg_words@{k}"] = round(statistics.mean(words), 1)
    top1 = lambda kind: [q["retrieved"][0]["score"] for q in per_question if (q["kind"] == "unanswerable") == kind]
    metrics["mean_top1_score_answerable"] = round(statistics.mean(top1(False)), 4)
    metrics["mean_top1_score_unanswerable"] = round(statistics.mean(top1(True)), 4)
    metrics["misses@5"] = [{"id": q["id"], "expected": rows[i]["expected"],
                            "top1": f"{q['retrieved'][0]['source']} {q['retrieved'][0]['location']}"}
                           for i, q in enumerate(per_question) if i in answerable and q["first_match_rank"] is None]
    return metrics, per_question


def run_retrieval(rows):
    # The questions are embedded once and cached; expected_* is used only for scoring here.
    vectors = index.embed_queries([r["question"] for r in rows])
    report = {"questions_sha256": file_hash(QUESTIONS), "embedding_model": index.EMBEDDING_MODEL,
              "metric_definitions": METRIC_DEFINITIONS, "designs": {}, "per_question": {}}
    for design in index.DESIGNS:
        metrics, per_question = retrieval_for_design(design, rows, vectors)
        report["designs"][design], report["per_question"][design] = metrics, per_question
    RETRIEVAL_RESULTS.write_text(json.dumps(report, indent=2, ensure_ascii=False))
    print_retrieval(report)
    return report


METRIC_DEFINITIONS = {
    "hit@k": "Share of answerable (single + multi) questions where at least one of the top k chunks comes from an "
             "expected document AND covers its expected location (article/section/recital, or PDF page). "
             "Unanswerable questions are excluded from the denominator.",
    "multi_all_evidence@k": "Share of multi questions where every expected passage is covered by some top-k chunk.",
    "avg_words@k": "Average words in the top k chunks over all questions: what retrieval adds to the prompt.",
    "mean_top1_score": "Mean cosine similarity of the best chunk, for answerable vs unanswerable questions; "
                       "shows whether a score threshold could separate them.",
}


def print_retrieval(report):
    print("\nRetrieval (hit rate on source AND location; unanswerable questions excluded)")
    for design, m in report["designs"].items():
        hits = "  ".join(f"hit@{k} {m[f'hit@{k}']['hits']}/{m[f'hit@{k}']['n']} ({m[f'hit@{k}']['rate']:.0%})" for k in KS)
        multi = "  ".join(f"@{k} {m[f'multi_all_evidence@{k}']['hits']}/{m[f'multi_all_evidence@{k}']['n']}" for k in KS)
        print(f"  design {design}: {m['chunks']} chunks | {hits}")
        print(f"            multi all-evidence {multi} | words in top 3: {m['avg_words@3']}, top 5: {m['avg_words@5']}")
        print(f"            mean top-1 score: answerable {m['mean_top1_score_answerable']}, "
              f"unanswerable {m['mean_top1_score_unanswerable']} | misses@5: {[x['id'] for x in m['misses@5']]}")


# 3. The agent on every question, saved one at a time.

def load_jsonl(path):
    if not path.exists():
        return {}
    return {r["key"]: r for r in (json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line)}


def agent_config():
    """What the answers depend on, so a changed agent never reuses stale answers."""
    import agent

    return {"model": agent.MODEL, "agents_md": file_hash(agent.AGENTS_FILE), "design": index.SEARCH_DESIGN,
            "model_call_limit": agent.MODEL_CALL_LIMIT, "server": file_hash(ROOT / "server.py")}


async def run_agent(rows):
    import agent

    config = agent_config()
    saved = load_jsonl(ANSWERS)
    results, errors = {}, []
    async with AsyncExitStack() as stack:
        built = None
        for row in rows:
            key = hashlib.sha256(json.dumps([row["id"], row["question"], config]).encode()).hexdigest()
            if key in saved:
                results[row["id"]] = saved[key]
                continue
            if built is None:
                built = agent.build_agent(await agent.load_mcp_tools(stack), approve=agent.deny_all)
            print(f"  asking {row['id']} ...", file=sys.stderr)
            try:
                answer = await agent.ask(built, row["question"])
            except Exception as error:  # recorded and reported, never treated as an answer
                errors.append(f"{row['id']}: {type(error).__name__}: {error}")
                print(f"  {row['id']} failed: {type(error).__name__}: {error}", file=sys.stderr)
                continue
            record = {"key": key, "id": row["id"], "config": config,
                      "asked_at": datetime.now(timezone.utc).isoformat(timespec="seconds"), **answer}
            with ANSWERS.open("a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
            results[row["id"]] = record
    return results, errors


# 4. Code checks: what code can establish exactly.

def response_kind(answer):
    for marker, kind in MARKERS.items():
        if answer.lstrip().startswith(marker):
            return kind
    return "answer"


def chunk_metadata_by_id(ids):
    """Metadata of indexed chunks by id, looked up in every design collection."""
    db, found = index.open_index(), {}
    for design in index.DESIGNS:
        got = index.design_collection(db, design).get(ids=list(ids), include=["metadatas"]) if ids else {"ids": []}
        found.update(zip(got["ids"], got.get("metadatas") or []))
    return found


def code_checks(row, record):
    import agent

    kind = response_kind(record["answer"])
    # Re-extract citations with the current parser instead of trusting the ids stored at run time: the first
    # parser skipped `[a, b]` brackets and malformed ids, so the stored `cited_ids` undercount bad citations.
    cited = agent.extract_citations(record["raw_answer"])
    returned = set(record["retrieved"])
    recheck_passed, recheck_reason = agent.check_citations(record["raw_answer"], record["retrieved"])
    meta = chunk_metadata_by_id(set(cited) | returned)
    expected_returned = any(chunk_matches(meta[i], p) for i in returned if i in meta for p in row["expected"])
    return {
        "response_kind": kind,
        "partial": "NOT ESTABLISHED:" in record["answer"],
        "searched": any(s["type"] == "call" and s["name"] == "search" for s in record["trace"]),
        "citations": len(cited),
        "citations_exist_in_index": all(c in meta for c in cited),
        "citations_returned_to_agent": all(c in returned for c in cited),
        "cites_expected_location": any(chunk_matches(meta[c], p) for c in cited if c in meta for p in row["expected"]),
        "expected_evidence_returned": expected_returned,
        "refusal_ok": (kind == "refusal") if row["kind"] == "unanswerable" else kind not in ("refusal", "withheld"),
        "citation_guardrail_passed": record["guardrails"]["citation_check"]["passed"],  # at run time
        "citation_recheck_passed": recheck_passed,  # current guardrail applied to the stored raw answer
        "citation_recheck_reason": recheck_reason,
        "model_call_limit_hit": record["guardrails"]["model_call_limit_hit"],
        "add_document_called": any(s["type"] == "call" and s["name"] == "add_document" for s in record["trace"]),
    }


# 5. The judge: a rubric, the evidence, reasoning before the verdict, structured output.

class Verdict(BaseModel):
    reasoning: str = Field(description="Three to five sentences checking the answer against each criterion, "
                                       "naming any claim that is wrong or not in the passages.")
    correct: bool = Field(description="True only if the answer meets the correctness criterion.")
    supported: bool = Field(description="True only if every factual claim in the answer is stated in the retrieved passages.")


JUDGE_PROMPT = """You are grading an assistant that answers questions about EU passenger-rights texts using only passages returned by a search tool. Rubric {rubric}.

Correctness:
- Answerable question: the answer states the key facts of the reference answer without contradicting them and keeps the conditions or exceptions the reference mentions. Extra correct detail is fine. An answer starting "NEED DETAILS:" is correct only if the missing fact really decides the answer and the rule it states is right. A refusal ("NOT IN CORPUS:") or an answer starting "WITHHELD:" is incorrect.
- Unanswerable question: correct only if the answer says the texts do not establish the answer (normally starting "NOT IN CORPUS:") and does not supply the missing facts from elsewhere.
Support:
- Every factual claim in the answer appears in the retrieved passages below, in substance. Judge against the passages, not your own knowledge, even if the claim is true. A refusal that makes no factual claims is supported.

Question ({kind}): {question}
Reference answer: {reference}

Retrieved passages (exactly what the search tool returned to the assistant):
{passages}

Tool calls the harness recorded:
{calls}

Assistant's answer:
{answer}"""


def judge_input(row, record):
    passages = "\n\n".join(record["retrieved"].values()) or "(no passages were retrieved)"
    calls = "\n".join(f"{s['name']}({s['args']})" for s in record["trace"] if s["type"] == "call") or "(no tool calls)"
    return JUDGE_PROMPT.format(rubric=RUBRIC_VERSION, kind=row["kind"], question=row["question"],
                               reference=row["reference_answer"], passages=passages, calls=calls,
                               answer=record["answer"])


async def run_judge(rows, answers):
    from langchain_google_genai import ChatGoogleGenerativeAI

    from api_key import load_api_key

    load_api_key()
    judge = ChatGoogleGenerativeAI(model=JUDGE_MODEL, temperature=0).with_structured_output(Verdict, include_raw=True)
    saved = load_jsonl(VERDICTS)
    verdicts, errors = {}, []
    for row in rows:
        record = answers.get(row["id"])
        if record is None:
            continue
        key = hashlib.sha256(json.dumps([row["id"], row["reference_answer"], record["answer"],
                                         sorted(record["retrieved"]), JUDGE_MODEL, RUBRIC_VERSION]).encode()).hexdigest()
        if key in saved:
            verdicts[row["id"]] = saved[key]
            continue
        try:
            out = await judge.ainvoke(judge_input(row, record))
        except Exception as error:
            errors.append(f"judge {row['id']}: {type(error).__name__}: {error}")
            continue
        if out["parsed"] is None:
            errors.append(f"judge {row['id']}: unparseable verdict ({out['parsing_error']})")
            continue
        usage = getattr(out["raw"], "usage_metadata", None)
        verdict = {"key": key, "id": row["id"], "judge_model": JUDGE_MODEL, "rubric_version": RUBRIC_VERSION,
                   **out["parsed"].model_dump(),
                   "usage": {k: usage.get(k) for k in ("input_tokens", "output_tokens", "total_tokens")} if usage else None}
        with VERDICTS.open("a", encoding="utf-8") as f:
            f.write(json.dumps(verdict, ensure_ascii=False) + "\n")
        verdicts[row["id"]] = verdict
    return verdicts, errors


# 6. Human grading: a blind sheet, then agreement on the same answers.

def write_grading_sheet(rows, answers):
    lines = ["# Blind grading sheet", "",
             "Grade each answer before opening eval/results.json or eval/verdicts.jsonl (they hold the judge's verdicts).",
             "Write your grades in eval/human_labels.csv as `id,correct,supported,notes` with 1/0, and a note for every 0.",
             "`correct`: right against the reference, or a proper refusal. `supported`: every claim is in the passages below.", ""]
    for row in rows:
        record = answers.get(row["id"])
        if record is None:
            continue
        lines += [f"## {row['id']} ({row['kind']})", "", f"**Question:** {row['question']}", "",
                  f"**Reference:** {row['reference_answer']}", "", "**Answer shown to the user:**", "",
                  "> " + record["answer"].replace("\n", "\n> "), "", "<details><summary>Passages the agent retrieved</summary>", ""]
        lines += [f"```text\n{text}\n```" for text in record["retrieved"].values()] or ["(none)"]
        lines += ["", "</details>", ""]
    TO_GRADE.write_text("\n".join(lines), encoding="utf-8")


def read_human_labels():
    if not HUMAN_LABELS.exists():
        return {}
    with HUMAN_LABELS.open(newline="", encoding="utf-8") as f:
        return {r["id"].strip(): r for r in csv.DictReader(f) if (r.get("id") or "").strip()}


def agreement(labels, verdicts):
    """Judge-human agreement on the answers both graded, with the denominator stated."""
    report = {}
    for field in ("correct", "supported"):
        pairs = [(labels[i][field].strip() == "1", verdicts[i][field]) for i in labels
                 if i in verdicts and labels[i].get(field, "").strip() in ("0", "1")]
        agree = sum(h == j for h, j in pairs)
        report[field] = {"n": len(pairs), "agree": agree, "rate": round(agree / len(pairs), 3) if pairs else None,
                         "human_yes_judge_no": sum(h and not j for h, j in pairs),
                         "human_no_judge_yes": sum(j and not h for h, j in pairs)}
    return report


# 7. Failure classes (provisional: "bad test question" needs a person), cost and summary.

def failure_class(row, checks, verdict):
    if verdict is None:
        return "not judged"
    if row["kind"] == "unanswerable":
        return None if checks["response_kind"] == "refusal" and verdict["correct"] else "unsupported claim"
    if checks["response_kind"] in ("refusal", "withheld"):
        return "wrong refusal" if checks["expected_evidence_returned"] else "retrieval miss"
    if not verdict["correct"]:
        return "wrong answer from the right passage" if checks["expected_evidence_returned"] else "retrieval miss"
    if not verdict["supported"]:
        return "unsupported claim"
    return None


def usage_totals(records):
    """Summed and mean tokens; None (unavailable), never 0, when no usage was reported."""
    reported = [r["usage"] for r in records if r.get("usage")]
    if not reported:
        return {"available_for": 0, "of": len(records), "total_tokens": None, "mean_tokens_per_question": None}
    total = sum(u["total_tokens"] or 0 for u in reported)
    return {"available_for": len(reported), "of": len(records), "input_tokens": sum(u["input_tokens"] or 0 for u in reported),
            "output_tokens": sum(u["output_tokens"] or 0 for u in reported), "total_tokens": total,
            "mean_tokens_per_question": round(total / len(reported), 1)}


def summarise(rows, answers, verdicts, checks, labels, retrieval, errors):
    judged = [r for r in rows if r["id"] in verdicts]
    answerable = [r for r in judged if r["kind"] != "unanswerable"]
    unanswerable = [r for r in judged if r["kind"] == "unanswerable"]
    classes = {r["id"]: failure_class(r, checks[r["id"]], verdicts.get(r["id"])) for r in rows if r["id"] in checks}
    latencies = [answers[i]["latency_s"] for i in answers]
    count = lambda items: sum(1 for x in items if x)
    return {
        "generated_at": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "questions_sha256": file_hash(QUESTIONS),
        "questions_frozen": FROZEN.exists() and FROZEN.read_text().strip() == file_hash(QUESTIONS),
        "agent": agent_config(), "judge_model": JUDGE_MODEL, "rubric_version": RUBRIC_VERSION,
        "index_dir": str(index.INDEX_DIR), "search_design": index.SEARCH_DESIGN,
        "search_design_provisional": index.DESIGN_IS_PROVISIONAL,
        "retrieval": {d: {k: v for k, v in m.items() if k != "misses@5"} for d, m in retrieval["designs"].items()},
        "answered": len(answers), "judged": len(judged), "errors": errors,
        "results": {
            "answerable_correct": f"{count(verdicts[r['id']]['correct'] for r in answerable)}/{len(answerable)}",
            "answerable_supported": f"{count(verdicts[r['id']]['supported'] for r in answerable)}/{len(answerable)}",
            "unsupported_answers": f"{count(not verdicts[r['id']]['supported'] for r in judged)}/{len(judged)}",
            "correct_refusals": f"{count(checks[r['id']]['response_kind'] == 'refusal' for r in unanswerable)}/{len(unanswerable)}",
            "wrong_refusals": f"{count(checks[r['id']]['response_kind'] in ('refusal', 'withheld') for r in answerable)}/{len(answerable)}",
            "clarifications": count(checks[i]["response_kind"] == "clarification" for i in checks),
        },
        "code_checks": {
            "citations_exist_in_index": f"{count(c['citations_exist_in_index'] for c in checks.values())}/{len(checks)}",
            "citations_returned_to_agent": f"{count(c['citations_returned_to_agent'] for c in checks.values())}/{len(checks)}",
            "citation_guardrail_fired": count(not c["citation_guardrail_passed"] for c in checks.values()),
            "citation_recheck_would_withhold": sorted(i for i, c in checks.items() if not c["citation_recheck_passed"]),
            "citation_recheck_changed": sorted(i for i, c in checks.items()
                                               if c["citation_recheck_passed"] != c["citation_guardrail_passed"]),
            "model_call_limit_hit": count(c["model_call_limit_hit"] for c in checks.values()),
            "add_document_called": count(c["add_document_called"] for c in checks.values()),
            "note": "Citation checks prove a cited id is real and was retrieved, not that it supports the claim.",
        },
        "failure_classes_provisional": {c: sorted(i for i, v in classes.items() if v == c)
                                        for c in sorted({v for v in classes.values() if v})},
        "agreement_with_human": agreement(labels, verdicts) if labels else "no human labels yet",
        "agent_cost": {**usage_totals(answers.values()),
                       "mean_latency_s": round(statistics.mean(latencies), 2) if latencies else None,
                       "median_latency_s": round(statistics.median(latencies), 2) if latencies else None},
        "judge_cost": usage_totals(verdicts.values()),
    }


def print_summary(summary, verdicts, checks):
    print("\nEnd to end (agent answers, code checks, judge)")
    for key, value in summary["results"].items():
        print(f"  {key:<24}{value}")
    for key, value in summary["code_checks"].items():
        print(f"  {key:<30}{value}")
    print(f"  failure classes (provisional): {summary['failure_classes_provisional']}")
    print(f"  agreement with human labels: {summary['agreement_with_human']}")
    print(f"  agent cost: {summary['agent_cost']}")
    print(f"  judge cost: {summary['judge_cost']}")
    if summary["errors"]:
        print(f"\n  {len(summary['errors'])} error(s):", *summary["errors"], sep="\n    ")


async def main():
    parser = argparse.ArgumentParser(description="Evaluate retrieval and the agent end to end.")
    parser.add_argument("--retrieval-only", action="store_true")
    parser.add_argument("--freeze", action="store_true", help="record the reviewed questions' hash and stop")
    args = parser.parse_args()

    index.require_index()
    rows = read_questions()
    problems = validate_questions(rows, indexed_locations())
    if problems:
        raise SystemExit("eval/questions.csv is not valid:\n  " + "\n  ".join(problems))
    if args.freeze:
        FROZEN.write_text(file_hash(QUESTIONS) + "\n")
        print(f"Froze {len(rows)} questions: {file_hash(QUESTIONS)}")
        return
    if not FROZEN.exists() or FROZEN.read_text().strip() != file_hash(QUESTIONS):
        print("WARNING: questions.csv is not frozen or changed after freezing (evaluate.py --freeze).")
    print(f"{len(rows)} valid questions.")

    retrieval = run_retrieval(rows)
    if args.retrieval_only:
        return

    answers, agent_errors = await run_agent(rows)
    checks = {r["id"]: code_checks(r, answers[r["id"]]) for r in rows if r["id"] in answers}
    verdicts, judge_errors = await run_judge(rows, answers)
    write_grading_sheet(rows, answers)
    labels = read_human_labels()

    results = [{**{k: r[k] for k in ("id", "question", "kind", "expected_source", "expected_location", "reference_answer")},
                "answer": answers.get(r["id"], {}).get("answer"), "raw_answer": answers.get(r["id"], {}).get("raw_answer"),
                "trace": answers.get(r["id"], {}).get("trace"), "checks": checks.get(r["id"]),
                "verdict": verdicts.get(r["id"]), "usage": answers.get(r["id"], {}).get("usage"),
                "latency_s": answers.get(r["id"], {}).get("latency_s"),
                "failure_class_provisional": failure_class(r, checks[r["id"]], verdicts.get(r["id"])) if r["id"] in checks else None}
               for r in rows]
    RESULTS.write_text(json.dumps(results, indent=2, ensure_ascii=False))
    summary = summarise(rows, answers, verdicts, checks, labels, retrieval, agent_errors + judge_errors)
    SUMMARY.write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    print_summary(summary, verdicts, checks)
    print(f"\nSaved {RESULTS.name}, {SUMMARY.name}, {RETRIEVAL_RESULTS.name}, {TO_GRADE.name} in eval/.")
    if agent_errors or judge_errors:
        raise SystemExit("Some questions could not be answered or judged (see above); run again to resume.")


if __name__ == "__main__":
    asyncio.run(main())
