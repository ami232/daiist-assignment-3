"""
Assignment 3: evaluation (`main.py evaluate`).

1. Retrieval: hit rate at k = 1, 3, 5 for each chunking design (no LLM, only embeddings).
2. The agent answers every question in eval/questions.csv (answers.jsonl).
3. Code checks on each answer: refusal, citations, expected source and location.
4. An LLM judge grades each answer with the rubric below, using the retrieved text as evidence (judge.jsonl).
5. Agreement between the judge and your own grades in eval/human_labels.csv.
Results: eval/retrieval.csv, eval/results.csv, eval/summary.json (+ answers.jsonl, judge.jsonl).

Environment variables:
  EVAL_RESUME=1   keep answers and verdicts already saved (use after a quota error); default is a full fresh run
  JUDGE_MODEL=... model of the judge (default: gemini-3.5-flash-lite, the same model as the agent (a known limitation))
  EVAL_PAUSE=6    seconds to wait between questions (free-tier request limit)
"""

from __future__ import annotations

import csv
import json
import os
import re
import statistics
import sys
import time
from collections import Counter
from pathlib import Path

import agent
import index

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS, HUMAN = EVAL / "questions.csv", EVAL / "human_labels.csv"
ANSWERS, JUDGED = EVAL / "answers.jsonl", EVAL / "judge.jsonl"
RETRIEVAL, RESULTS, SUMMARY = EVAL / "retrieval.csv", EVAL / "results.csv", EVAL / "summary.json"
KS = (1, 3, 5)
JUDGE_MODEL = os.environ.get("JUDGE_MODEL", "gemini-3.5-flash-lite")
RESUME = os.environ.get("EVAL_RESUME") == "1"
PAUSE = float(os.environ.get("EVAL_PAUSE", "6"))  # seconds between questions, to stay under the free-tier request limit

RUBRIC = EVAL / "judge_rubric.md"  # the judge's instructions: yours to write and edit


def load_rubric() -> str:
    if not RUBRIC.is_file():
        raise SystemExit("eval/judge_rubric.md is missing: it holds the rubric the judge follows.")
    lines = [l for l in RUBRIC.read_text(encoding="utf-8").splitlines() if not l.lstrip().startswith("#")]
    text = "\n".join(lines).strip()
    if not text:
        raise SystemExit("eval/judge_rubric.md is empty.")
    return text


def log(*parts) -> None:
    print(*parts, file=sys.stderr, flush=True)


# --------------------------------------------------------------------------
# Questions and expectations
# --------------------------------------------------------------------------
def read_questions() -> list[dict]:
    if not QUESTIONS.is_file():
        raise SystemExit("eval/questions.csv is missing.")
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if (r.get("question") or "").strip()]
    for r in rows:
        r["kind"] = r["kind"].strip().lower()
    if not rows:
        raise SystemExit("eval/questions.csv has no questions.")
    return rows


def expected_pairs(row: dict) -> list[tuple[str, str]]:
    """The (source, location) pairs that answer a question; none if it is unanswerable."""
    if row["kind"] == "unanswerable":
        return []
    sources = [s.strip() for s in row["expected_source"].split(";") if s.strip()]
    places = [s.strip() for s in row["expected_location"].split(";") if s.strip()]
    if len(sources) == len(places):
        return list(zip(sources, places))
    if len(sources) == 1:
        return [(sources[0], p) for p in places]
    return [(s, places[0]) for s in sources] if len(places) == 1 else list(zip(sources, places))


def matched_pairs(hit: dict, pairs: list[tuple[str, str]]) -> set[int]:
    """Which expected pairs a retrieved chunk covers: same document, and the location is one of its sections."""
    sections = [s.strip() for s in hit["sections"].split(";")]
    return {i for i, (source, place) in enumerate(pairs) if hit["source"] == source and place in sections}


# --------------------------------------------------------------------------
# 1. Retrieval hit rate per design
# --------------------------------------------------------------------------
def retrieval_eval(rows: list[dict]) -> dict:
    answerable = [r for r in rows if r["kind"] != "unanswerable"]
    records, summary = [], {}
    for design in index.DESIGNS:
        words_in_prompt = []
        hits_by_row = {}
        for r in answerable:
            hits = index.search_chunks(r["question"], k=max(KS), design=design)
            hits_by_row[r["id"]] = hits
            words_in_prompt.append(sum(len(h["text"].split()) for h in hits))
        summary[design] = {"words_in_prompt_k5": round(statistics.mean(words_in_prompt), 1) if words_in_prompt else 0}
        for k in KS:
            any_hits, all_hits = [], []
            for r in answerable:
                pairs = expected_pairs(r)
                matched = set().union(*(matched_pairs(h, pairs) for h in hits_by_row[r["id"]][:k]))
                ranks = [i for i, h in enumerate(hits_by_row[r["id"]], 1) if matched_pairs(h, pairs)]
                any_hits.append(bool(matched))
                all_hits.append(len(matched) == len(pairs))
                records.append(
                    {"design": design, "k": k, "id": r["id"], "kind": r["kind"], "hit_any": int(bool(matched)),
                     "hit_all": int(len(matched) == len(pairs)), "first_rank": ranks[0] if ranks else 0}
                )
            n = len(answerable)
            summary[design][f"hit@{k}"] = round(sum(any_hits) / n, 3) if n else 0
            summary[design][f"hit_all@{k}"] = round(sum(all_hits) / n, 3) if n else 0
    with RETRIEVAL.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["design", "k", "id", "kind", "hit_any", "hit_all", "first_rank"])
        writer.writeheader()
        writer.writerows(records)
    return summary


# --------------------------------------------------------------------------
# 2. The agent answers every question
# --------------------------------------------------------------------------
def read_jsonl(path: Path) -> dict:
    if not (RESUME and path.is_file()):
        return {}
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            rec = json.loads(line)
            if not rec.get("error"):
                out[rec["id"]] = rec
    return out


def append_jsonl(path: Path, rec: dict) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def passages_text(outcome: dict) -> str:
    return "\n\n".join(s["result"] for s in outcome["trace"] if s["tool"] == "search" and not s["blocked"])


def answer_all(rows: list[dict]) -> dict:
    done = read_jsonl(ANSWERS)
    if not RESUME:
        ANSWERS.write_text("")
    else:
        ANSWERS.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in done.values()))
    for n, r in enumerate(rows, 1):
        if r["id"] in done:
            continue
        log(f"[{n}/{len(rows)}] {r['id']} ({r['kind']}): {r['question'][:70]}")
        try:
            out = agent.ask(r["question"], approve=lambda name, args: False)
            rec = {
                "id": r["id"], "answer": out["answer"], "raw_answer": out["raw_answer"], "refused": out["refused"],
                "retrieved": out["retrieved"], "passages": passages_text(out), "guardrails": out["guardrails"],
                "tools": [s["tool"] for s in out["trace"]], "tool_calls": out["tool_calls"], "model_calls": out["model_calls"],
                "input_tokens": out["input_tokens"], "output_tokens": out["output_tokens"], "seconds": out["seconds"],
                "model": out["model"],
            }
        except (Exception, BaseExceptionGroup) as error:  # noqa: BLE001 - keep going, report at the end
            log(f"   ERROR: {agent.error_text(error)[:200]}")
            rec = {"id": r["id"], "error": agent.error_text(error)[:300]}
        append_jsonl(ANSWERS, rec)
        done[r["id"]] = rec if not rec.get("error") else done.get(r["id"], rec)
        time.sleep(PAUSE)
    return done


# --------------------------------------------------------------------------
# 3. Code checks
# --------------------------------------------------------------------------
def location_matches(location: str, expected: str) -> bool:
    """Does a cited/retrieved location ("Article 4, p. 7", "p. 12-13 (part 2)") point at the expected one?"""
    if expected.startswith("p. "):
        want = re.match(r"p\. (\d+)", expected)
        span = re.search(r"p\. (\d+)(?:-(\d+))?", location.split(", p. ")[-1] if ", p. " in location else location)
        if not (want and span):
            return False
        lo, hi = int(span.group(1)), int(span.group(2) or span.group(1))
        return lo <= int(want.group(1)) <= hi
    label = re.sub(r" \(part \d+\)$", "", location.split(", p. ")[0].strip())
    return label == expected


def code_checks(row: dict, rec: dict) -> dict:
    pairs = expected_pairs(row)
    retrieved = [tuple(p) for p in rec["retrieved"]]
    cited = [(s.strip(), l.strip()) for s, l in agent.CITATION.findall(rec["answer"])]
    cites_valid = bool(cited) and agent.cites_retrieved(rec["answer"], retrieved)
    cites_expected = any(cs == es and location_matches(cl, el) for cs, cl in cited for es, el in pairs)
    expected_in_retrieved = any(rs == es and location_matches(rl, el) for rs, rl in retrieved for es, el in pairs)
    return {
        "refused": bool(rec["refused"]),
        "cites_valid": cites_valid,
        "cites_expected": cites_expected,
        "expected_in_retrieved": expected_in_retrieved,
    }


# --------------------------------------------------------------------------
# 4. LLM judge
# --------------------------------------------------------------------------
_client = None


def call_judge(prompt: str) -> dict:
    global _client
    from google import genai
    from google.genai import types

    from api_key import load_api_key

    _client = _client or genai.Client(api_key=load_api_key(), http_options=types.HttpOptions(timeout=60_000))
    schema = {
        "type": "OBJECT",
        "properties": {"correct": {"type": "INTEGER"}, "supported": {"type": "INTEGER"}, "reason": {"type": "STRING"}},
        "required": ["correct", "supported", "reason"],
    }
    config = types.GenerateContentConfig(response_mime_type="application/json", response_schema=schema)
    for attempt in range(1, 8):
        try:
            response = _client.models.generate_content(model=JUDGE_MODEL, contents=prompt, config=config)
            data = json.loads(response.text)
            return {"correct": int(bool(int(data["correct"]))), "supported": int(bool(int(data["supported"]))), "reason": str(data["reason"])[:400]}
        except Exception as error:  # noqa: BLE001
            message = str(error)
            retryable = "imeout" in type(error).__name__ or "timed out" in message.lower() or any(c in message for c in ("429", "500", "503", "504", "RESOURCE_EXHAUSTED", "UNAVAILABLE")) or isinstance(error, (ValueError, KeyError))
            if attempt == 7 or not retryable:
                raise
            hint = re.search(r"retryDelay\W+(\d+)", message)
            wait = int(hint.group(1)) + 3 if hint else 15 * attempt
            if 'PerDay' in message or wait > 120:  # a used-up daily quota: waiting will not help
                raise
            log(f"   judge retry {attempt}/6 in {wait}s: {message[:80]}")
            time.sleep(wait)
    raise AssertionError("unreachable")


def judge_prompt(row: dict, rec: dict) -> str:
    return f"""You grade the answer of a retrieval-based assistant. Follow the rubric exactly.

Question: {row['question']}
Question kind: {row['kind']}
Reference answer (for an unanswerable question: what the assistant should say): {row['reference_answer']}

Retrieved passages (the only evidence the assistant had):
<<<
{rec['passages'][:14000] or '(nothing was retrieved)'}
>>>

Assistant's answer:
<<<
{rec['answer']}
>>>

Rubric:
{load_rubric()}

Reply with JSON: {{"correct": 0 or 1, "supported": 0 or 1, "reason": "one sentence"}}"""


def judge_all(rows: list[dict], answers: dict) -> dict:
    done = read_jsonl(JUDGED)
    JUDGED.write_text("".join(json.dumps(r, ensure_ascii=False) + "\n" for r in done.values()) if RESUME else "")
    for n, r in enumerate(rows, 1):
        rec = answers.get(r["id"])
        if r["id"] in done or not rec or rec.get("error"):
            continue
        log(f"[judge {n}/{len(rows)}] {r['id']}")
        try:
            verdict = {"id": r["id"], **call_judge(judge_prompt(r, rec))}
        except Exception as error:  # noqa: BLE001
            log(f"   JUDGE ERROR: {type(error).__name__}: {str(error)[:200]}")
            verdict = {"id": r["id"], "error": f"{type(error).__name__}: {str(error)[:300]}"}
        append_jsonl(JUDGED, verdict)
        time.sleep(PAUSE)
        if not verdict.get("error"):
            done[r["id"]] = verdict
    return done


# --------------------------------------------------------------------------
# 5. Results, failure causes, agreement with the human labels
# --------------------------------------------------------------------------
def cause(row: dict, checks: dict, verdict: dict | None) -> str:
    """A first, mechanical classification. Your Failures section refines it by reading the answers."""
    if verdict is None:
        return "not graded"
    if row["kind"] == "unanswerable":
        return "ok" if checks["refused"] and verdict["correct"] else "answered an unanswerable question"
    if checks["refused"]:
        return "wrong refusal: retrieval miss" if not checks["expected_in_retrieved"] else "wrong refusal: passages were retrieved"
    if not verdict["correct"]:
        return "wrong answer: retrieval miss" if not checks["expected_in_retrieved"] else "wrong answer: generation"
    if not verdict["supported"]:
        return "unsupported claim"
    if not checks["cites_valid"]:
        return "no valid citation"
    return "ok"


def read_human() -> dict:
    if not HUMAN.is_file():
        return {}
    with HUMAN.open(newline="", encoding="utf-8") as f:
        return {r["id"].strip(): r for r in csv.DictReader(f) if (r.get("id") or "").strip()}


def pct(a: int, b: int) -> float:
    return round(100 * a / b, 1) if b else 0.0


def main() -> None:
    rows = read_questions()
    EVAL.mkdir(exist_ok=True)
    summary: dict = {"questions": len(rows), "agent_model": agent.MODEL, "judge_model": JUDGE_MODEL, "design": index.DEFAULT_DESIGN}
    summary["judge_rubric"] = load_rubric()

    log("== 1/4 retrieval hit rate per design ==")
    summary["retrieval"] = retrieval_eval(rows)
    for design, s in summary["retrieval"].items():
        log(f"  {design:<10} " + "  ".join(f"hit@{k}={s[f'hit@{k}']:.2f}" for k in KS) + f"   words in prompt (top 5): {s['words_in_prompt_k5']}")
    log(f"  (the agent uses design {index.DEFAULT_DESIGN!r}: DEFAULT_DESIGN in index.py)")

    log("== 2/4 the agent answers every question ==")
    answers = answer_all(rows)
    log("== 3/4 the judge grades every answer ==")
    verdicts = judge_all(rows, answers)

    log("== 4/4 results ==")
    human = read_human()
    table, errors = [], []
    for r in rows:
        rec, verdict = answers.get(r["id"]), verdicts.get(r["id"])
        if not rec or rec.get("error"):
            errors.append(r["id"])
            continue
        checks = code_checks(r, rec)
        h = human.get(r["id"], {})
        table.append(
            {
                "id": r["id"], "kind": r["kind"], "question": r["question"], "expected_source": r["expected_source"],
                "expected_location": r["expected_location"], "answer": rec["answer"], **checks,
                "judge_correct": verdict["correct"] if verdict else "", "judge_supported": verdict["supported"] if verdict else "",
                "judge_reason": verdict["reason"] if verdict else "", "guardrails": "; ".join(rec["guardrails"]),
                "tool_calls": rec["tool_calls"], "model_calls": rec["model_calls"], "input_tokens": rec["input_tokens"],
                "output_tokens": rec["output_tokens"], "seconds": rec["seconds"], "cause": cause(r, checks, verdict),
                "human_correct": h.get("correct", ""), "human_supported": h.get("supported", ""),
            }
        )
    if table:
        with RESULTS.open("w", newline="", encoding="utf-8") as f:
            writer = csv.DictWriter(f, fieldnames=list(table[0]))
            writer.writeheader()
            writer.writerows(table)

    graded = [t for t in table if t["judge_correct"] != ""]
    answerable = [t for t in graded if t["kind"] != "unanswerable"]
    unanswerable = [t for t in graded if t["kind"] == "unanswerable"]
    summary["answered_without_error"] = len(table)
    summary["errors"] = errors
    summary["answerable"] = {
        "n": len(answerable),
        "correct": sum(t["judge_correct"] for t in answerable),
        "correct_and_supported": sum(1 for t in answerable if t["judge_correct"] and t["judge_supported"]),
        "unsupported": sum(1 for t in answerable if not t["refused"] and not t["judge_supported"]),
        "wrong_refusals": sum(1 for t in answerable if t["refused"]),
        "no_valid_citation": sum(1 for t in answerable if not t["refused"] and not t["cites_valid"]),
    }
    summary["unanswerable"] = {
        "n": len(unanswerable),
        "correct_refusals": sum(1 for t in unanswerable if t["refused"] and t["judge_correct"]),
        "answered_anyway": sum(1 for t in unanswerable if not t["refused"]),
    }
    summary["causes"] = dict(Counter(t["cause"] for t in table))
    secs = [t["seconds"] for t in table]
    if secs:
        summary["per_question"] = {
            "seconds_mean": round(statistics.mean(secs), 1), "seconds_max": round(max(secs), 1),
            "input_tokens_mean": round(statistics.mean(t["input_tokens"] for t in table)),
            "output_tokens_mean": round(statistics.mean(t["output_tokens"] for t in table)),
            "tool_calls_mean": round(statistics.mean(t["tool_calls"] for t in table), 2),
        }
    both = [t for t in graded if t["human_correct"] != ""]
    agree = {}
    for name in ("correct", "supported"):
        pairs = [(int(t[f"human_{name}"]), int(t[f"judge_{name}"])) for t in both if t[f"human_{name}"] != "" and t[f"human_{name}"] in ("0", "1")]
        agree[name] = {"n": len(pairs), "agree": sum(1 for h, j in pairs if h == j), "agreement_pct": pct(sum(1 for h, j in pairs if h == j), len(pairs))}
    agree["disagreements"] = [
        {"id": t["id"], "human_correct": t["human_correct"], "judge_correct": t["judge_correct"],
         "human_supported": t["human_supported"], "judge_supported": t["judge_supported"], "judge_reason": t["judge_reason"]}
        for t in both
        if str(t["human_correct"]) != str(t["judge_correct"]) or str(t["human_supported"]) != str(t["judge_supported"])
    ]
    summary["agreement_with_human_labels"] = agree
    SUMMARY.write_text(json.dumps(summary, indent=2, ensure_ascii=False))

    a, u = summary["answerable"], summary["unanswerable"]
    log(f"\nAnswerable ({a['n']}): correct {a['correct']}, correct and supported {a['correct_and_supported']}, "
        f"unsupported {a['unsupported']}, wrong refusals {a['wrong_refusals']}")
    log(f"Unanswerable ({u['n']}): correct refusals {u['correct_refusals']}, answered anyway {u['answered_anyway']}")
    log(f"Causes: {summary['causes']}")
    if "per_question" in summary:
        log(f"Per question: {summary['per_question']}")
    log(f"Human vs judge: correct {agree['correct']}, supported {agree['supported']}")
    if len(human) < 20:
        log(f"WARNING: eval/human_labels.csv has {len(human)} graded answers; the brief asks for at least 20.")
    log("Saved: eval/retrieval.csv, results.csv, summary.json, answers.jsonl, judge.jsonl")
    if errors:
        raise SystemExit(f"\n{len(errors)} question(s) could not be answered or graded: {', '.join(errors)}. "
                         "Run again with EVAL_RESUME=1 to redo only those.")


if __name__ == "__main__":
    main()