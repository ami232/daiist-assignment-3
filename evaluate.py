"""
Assignment 3: evaluation (`main.py evaluate`).

1. Retrieval: hit rate at 1/3/5 for three designs (vector, bm25, hybrid) on the
   answerable questions; writes eval/retrieval_results.csv and the chosen design to
   index/config.json (the server uses it). No extra embeddings: only query vectors.
2. Agent: runs agent.ask on every question (resumable: eval/answers.jsonl).
3. Code checks: valid citations, cites the expected section, correct refusal / wrong refusal.
4. LLM judge: rubric, retrieved text as evidence -> correct / supported.
5. Agreement with eval/human_labels.csv; writes eval/summary.json, summary.md, failures.csv.

Hit definition: a retrieved chunk is a hit when its source equals an expected source and its
location starts with an expected location (section number). For `multi` questions all
expected (source, location) pairs must be present in the top k.
"""

import csv
import json
import os
import re
import sys
import time
from pathlib import Path

import index as pipeline
from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
HUMAN = EVAL / "human_labels.csv"
ANSWERS = EVAL / "answers.jsonl"
JUDGEMENTS = EVAL / "judgements.jsonl"
JUDGE_BATCH = 5
JUDGE_MODEL = os.environ.get("JUDGE_MODEL", "gemini-3.8-flash")
KS = (1, 3, 5)
PAUSE_BETWEEN_QUESTIONS = 5
DESIGNS = ("vector", "bm25", "hybrid")

RUBRIC = """You grade an assistant's answer about US aviation regulations.
You get: the QUESTION, the REFERENCE answer (or what the assistant should say if the corpus cannot answer), the ASSISTANT answer and the EVIDENCE (the passages the assistant retrieved).
Grade two things, each 1 or 0:
- correct: 1 if the answer agrees with the reference on every point that matters (numbers, conditions, exceptions). For a question the corpus cannot answer, 1 only if the assistant says the corpus does not cover it and does not invent a rule. 0 if it contradicts the reference, omits a key condition, or refuses an answerable question.
- supported: 1 if every factual claim in the answer is stated in the EVIDENCE. 0 if any claim (including a number or a section) is not in the evidence. A proper refusal is supported = 1.
Return only JSON: {"correct": 0 or 1, "supported": 0 or 1, "reason": "one sentence"}"""


def read_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if (r.get("question") or "").strip()]


def sec(location: str) -> str:
    m = re.search(r"(\d{1,3}\.\d+[a-z]?)", location or "")
    return m.group(1) if m else (location or "").strip()


def expected_pairs(q: dict) -> list[tuple[str, str]]:
    sources = [s.strip() for s in q["expected_source"].split(";") if s.strip()]
    locations = [s.strip() for s in q["expected_location"].split(";") if s.strip()]
    if len(locations) == 1 and len(sources) > 1:
        locations = locations * len(sources)
    return [(s, sec(l)) for s, l in zip(sources, locations)]


def is_hit(results, pairs) -> bool:
    got = {(c["source"], sec(c["location"])) for _, c in results}
    return bool(pairs) and all((src, loc) in got for src, loc in pairs)


def retrieval_eval(questions: list[dict]) -> str:
    idx = pipeline.Index()
    answerable = [q for q in questions if q["kind"].strip().lower() != "unanswerable"]
    rows, best = [], None
    for design in DESIGNS:
        hits = {k: 0 for k in KS}
        words = 0
        for q in answerable:
            res = idx.search(q["question"], k=max(KS), mode=design)
            words += sum(len(c["text"].split()) for _, c in res)
            for k in KS:
                hits[k] += is_hit(res[:k], expected_pairs(q))
        n = len(answerable)
        row = {"design": design, **{f"hit@{k}": round(hits[k] / n, 3) for k in KS}, "words_in_prompt_k5": round(words / n)}
        rows.append(row)
        key = (row["hit@5"], row["hit@3"], row["hit@1"])
        if best is None or key > best[0]:
            best = (key, design)
    with (EVAL / "retrieval_results.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    pipeline.CONFIG_FILE.write_text(json.dumps({"mode": best[1]}))
    print("Retrieval (answerable questions):")
    for r in rows:
        print("  ", r)
    print(f"chosen design: {best[1]}")
    return best[1]


def _root_cause(e: BaseException) -> BaseException:
    """Unwrap ExceptionGroup / chained errors to the real error."""
    while True:
        if isinstance(e, BaseExceptionGroup) and e.exceptions:
            e = e.exceptions[0]
        elif e.__cause__ is not None:
            e = e.__cause__
        else:
            return e


def _ask_with_retry(question: str, attempts: int = 6) -> dict:
    """Retry on rate limits / overload, waiting as long as the API asks. Stop on a daily quota."""
    from agent import ask

    for attempt in range(1, attempts + 1):
        try:
            return ask(question, approve=lambda *_: False)
        except Exception as e:  # noqa: BLE001
            msg = str(_root_cause(e))
            if "per day" in msg.lower() or "PerDay" in msg:
                raise SystemExit(f"Daily Gemini quota reached. Run this command again tomorrow.\n{msg[:300]}")
            transient = any(k in msg for k in ("429", "503", "RESOURCE_EXHAUSTED", "UNAVAILABLE", "timed out"))
            if not transient or attempt == attempts:
                raise RuntimeError(msg[:400]) from e
            m = re.search(r"retry in ([\d.]+)s", msg)
            wait = float(m.group(1)) + 3 if m else 30 * attempt
            print(f"  transient error ({msg[:90]}...); waiting {wait:.0f}s, attempt {attempt}/{attempts}", file=sys.stderr)
            time.sleep(wait)


def run_agent_on_all(questions: list[dict]) -> list[dict]:
    done = {}
    if ANSWERS.exists():
        for line in ANSWERS.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                done[r["id"]] = r
    for q in questions:
        if q["id"] in done:
            continue
        try:
            out = _ask_with_retry(q["question"])
        except SystemExit as e:  # daily quota: keep what we have and go on to the judge
            print(f"{e}\nStopping the agent here; judging the answers already saved.", file=sys.stderr)
            break
        except RuntimeError as e:
            print(f"{q['id']} failed: {e}", file=sys.stderr)
            continue
        out["id"] = q["id"]
        done[q["id"]] = out
        with ANSWERS.open("a", encoding="utf-8") as f:
            f.write(json.dumps(out) + "\n")
        print(f"{q['id']} answered in {out['seconds']}s")
        time.sleep(PAUSE_BETWEEN_QUESTIONS)
    return [done[q["id"]] for q in questions if q["id"] in done]


def is_refusal(text: str) -> bool:
    return text.strip().lower().startswith("the corpus does not cover")


def code_checks(q: dict, a: dict) -> dict:
    answerable = q["kind"].strip().lower() != "unanswerable"
    refused = is_refusal(a["answer"])
    pairs = expected_pairs(q)
    cited = set(a["guardrail"]["cited"])
    return {
        "valid_citations": not a["guardrail"]["invalid"],
        "refused": refused,
        "correct_refusal": (not answerable) and refused,
        "wrong_refusal": answerable and refused,
        "cites_expected": answerable and all(l in cited for _, l in pairs) if pairs else False,
        "expected_retrieved": answerable and is_hit(
            [(0, {"source": s, "location": l}) for s, l in _retrieved_pairs(a)], pairs
        ),
    }


def _retrieved_pairs(a: dict):
    out = []
    for t in a["trace"]:
        if t["tool"] == "search":
            for m in re.finditer(r"^\[\d+\] (.+?) — (.+)$", t["result"], re.M):
                out.append((m.group(1), m.group(2)))
    return out


def _judge_batch_once(items: list[tuple[dict, dict]]) -> dict:
    """Judge several answers in ONE request. Returns {id: verdict}."""
    from google import genai
    from google.genai import types

    blocks = []
    for q, a in items:
        evidence = "\n\n".join(t["result"] for t in a["trace"] if t["tool"] == "search")[:4000] or "(no passages retrieved)"
        blocks.append(
            f"### ITEM {a['id']}\nQUESTION: {q['question']}\nREFERENCE: {q['reference_answer']}\n"
            f"ASSISTANT: {a['answer']}\nEVIDENCE:\n{evidence}"
        )
    prompt = (
        f"{RUBRIC}\n\nYou receive several items. Grade each one independently of the others.\n"
        'Return only a JSON array with one object per item: [{"id": "<item id>", "correct": 0 or 1, '
        '"supported": 0 or 1, "reason": "one sentence"}]\n\n' + "\n\n".join(blocks)
    )
    client = genai.Client(api_key=load_api_key())
    res = client.models.generate_content(
        model=JUDGE_MODEL, contents=prompt,
        config=types.GenerateContentConfig(temperature=0, response_mime_type="application/json"),
    )
    out = {}
    try:
        for v in json.loads(res.text):
            out[str(v["id"])] = {"correct": int(v["correct"]), "supported": int(v["supported"]), "reason": str(v.get("reason", ""))}
    except Exception:  # noqa: BLE001
        pass
    return out


def _judge_batch(items: list[tuple[dict, dict]], attempts: int = 6) -> dict:
    """One batched request, waiting and retrying on rate limits; stop on a daily quota."""
    for attempt in range(1, attempts + 1):
        try:
            return _judge_batch_once(items)
        except Exception as e:  # noqa: BLE001
            msg = str(e)
            if "per day" in msg.lower() or "PerDay" in msg:
                raise SystemExit(
                    "Daily quota reached for the judge model. Run this command again later "
                    f"(verdicts already made are saved).\n{msg[:300]}"
                )
            transient = any(k in msg for k in ("429", "503", "RESOURCE_EXHAUSTED", "UNAVAILABLE", "timed out"))
            if not transient or attempt == attempts:
                raise
            m = re.search(r"retry in ([\d.]+)s", msg)
            wait = float(m.group(1)) + 3 if m else 30 * attempt
            print(f"  judge transient error ({JUDGE_MODEL}); waiting {wait:.0f}s, attempt {attempt}/{attempts}\n"
                  f"    cause: {msg[:350]}", file=sys.stderr)
            time.sleep(wait)


def judge_all(questions_by_id: dict, answers: list[dict]) -> dict:
    """Judge in batches of JUDGE_BATCH answers per request. Verdicts are saved one by one
    to eval/judgements.jsonl, so a stop never loses them and a rerun only does what is missing."""
    done = {}
    if JUDGEMENTS.exists():
        for line in JUDGEMENTS.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                if r["verdict"]["correct"] != -1:
                    done[r["id"]] = r["verdict"]
    pending = [a for a in answers if a["id"] not in done]
    for i in range(0, len(pending), JUDGE_BATCH):
        group = pending[i:i + JUDGE_BATCH]
        got = _judge_batch([(questions_by_id[a["id"]], a) for a in group])
        for a in group:
            v = got.get(a["id"]) or {"correct": -1, "supported": -1, "reason": "judge returned no verdict for this item"}
            done[a["id"]] = v
            with JUDGEMENTS.open("a", encoding="utf-8") as f:
                f.write(json.dumps({"id": a["id"], "judge_model": JUDGE_MODEL, "verdict": v}) + "\n")
        print(f"judged {', '.join(a['id'] for a in group)}")
    return done


def main() -> None:
    load_api_key()
    questions = read_questions()
    if len(questions) < 30:
        raise SystemExit("eval/questions.csv needs 30+ questions first (see eval/README.md).")
    retrieval_eval(questions)
    answers = run_agent_on_all(questions)
    if len(answers) < len(questions):
        print(f"WARNING: {len(answers)} of {len(questions)} questions answered; the summary is PARTIAL. "
              "Run the command again later to finish.", file=sys.stderr)
    by_id = {q["id"]: q for q in questions}

    verdicts = judge_all(by_id, answers)
    results = []
    for a in answers:
        q = by_id[a["id"]]
        checks = code_checks(q, a)
        v = verdicts[a["id"]]
        results.append({"id": a["id"], "kind": q["kind"], **checks, **{f"judge_{k}": x for k, x in v.items()},
                        "seconds": a["seconds"], "tokens_in": a["tokens"]["input"], "tokens_out": a["tokens"]["output"],
                        "guardrail_fired": a["guardrail"]["fired"]})
    with (EVAL / "results.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(results[0]))
        w.writeheader()
        w.writerows(results)

    n = len(results)
    ans = [r for r in results if r["kind"].strip().lower() != "unanswerable"]
    una = [r for r in results if r["kind"].strip().lower() == "unanswerable"]
    summary = {
        "questions": n,
        "correct": sum(r["judge_correct"] == 1 for r in results),
        "unsupported": sum(r["judge_supported"] == 0 for r in results),
        "correct_refusals": sum(r["correct_refusal"] for r in una),
        "unanswerable": len(una),
        "wrong_refusals": sum(r["wrong_refusal"] for r in ans),
        "invalid_citations": sum(not r["valid_citations"] for r in results),
        "guardrail_fired": sum(r["guardrail_fired"] for r in results),
        "avg_seconds": round(sum(r["seconds"] for r in results) / n, 1),
        "avg_tokens_in": round(sum(r["tokens_in"] for r in results) / n),
        "avg_tokens_out": round(sum(r["tokens_out"] for r in results) / n),
    }
    if HUMAN.exists():
        human = {r["id"]: r for r in csv.DictReader(HUMAN.open(encoding="utf-8")) if r.get("id")}
        both = [(human[r["id"]], r) for r in results if r["id"] in human]
        if both:
            summary["human_graded"] = len(both)
            summary["agree_correct"] = round(sum(int(h["correct"]) == r["judge_correct"] for h, r in both) / len(both), 3)
            summary["agree_supported"] = round(sum(int(h["supported"]) == r["judge_supported"] for h, r in both) / len(both), 3)
    (EVAL / "summary.json").write_text(json.dumps(summary, indent=2))
    (EVAL / "summary.md").write_text("\n".join(f"- **{k}**: {v}" for k, v in summary.items()) + "\n")

    # failures with a first-guess cause; confirm or correct the `cause` column by hand
    with (EVAL / "failures.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "kind", "suggested_cause", "judge_reason", "cause"])
        for r in results:
            if r["judge_correct"] == 1 and r["judge_supported"] == 1:
                continue
            if r["wrong_refusal"]:
                cause = "retrieval miss" if not r["expected_retrieved"] else "wrong refusal"
            elif r["judge_supported"] == 0:
                cause = "unsupported claim"
            elif not r["expected_retrieved"] and r["kind"].strip().lower() != "unanswerable":
                cause = "retrieval miss"
            else:
                cause = "wrong answer from the right passage"
            w.writerow([r["id"], r["kind"], cause, r["judge_reason"], ""])
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
