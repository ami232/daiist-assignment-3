"""
Assignment 3: evaluation (`main.py evaluate`).

1. Retrieval: hit rate at k = 1, 3, 5 for each design (vector vs hybrid search
   over the same section chunks), and the words each k adds to the prompt.
2. End to end: the agent answers every question in eval/questions.csv.
3. Code checks: refusal or not, citations valid (each one was retrieved),
   expected source cited.
4. LLM judge (rubric below) grades every non-refusal answer against the
   reference answer, with the retrieved text as evidence.
5. Agreement between the judge and my own grades in eval/human_labels.csv.

Answers, query vectors and verdicts are cached in eval/, so re-running only
spends quota on questions that are new or changed.
"""

import csv
import json
import os
import re
import statistics
import sys
import time
from pathlib import Path

os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")

from langchain_google_genai import ChatGoogleGenerativeAI  # noqa: E402

import agent  # noqa: E402
from api_key import load_api_key  # noqa: E402
import index  # noqa: E402
import retrieval  # noqa: E402

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
HUMAN = EVAL / "human_labels.csv"
QUERY_VECTORS = EVAL / "query_vectors.json"
ANSWERS = EVAL / "answers.jsonl"
VERDICTS = EVAL / "verdicts.jsonl"
KS = [1, 3, 5]
MODES = ["vector", "hybrid"]
JUDGE_MODEL = "gemini-3.5-flash"  # a stronger model than the agent grades the answers

RUBRIC = """You grade answers from an assistant for school-district and county emergency
managers. The assistant must answer only from official NWS winter weather documents.

You get the question, a reference answer written by a person who read the documents,
the assistant's answer, and the passages the assistant retrieved (the evidence).

correct = 1 if the answer gives the same facts as the reference answer (wording can
differ; extra true detail is fine); 0 if any key fact is wrong or missing, or if it
answers a different question.

supported = 1 if every claim in the answer can be found in the retrieved passages;
0 if any claim (a number, a product name, a criterion, an office) is not in them,
even if it happens to be true.

Reply with JSON only: {"correct": 0 or 1, "supported": 0 or 1, "reason": "one sentence"}"""


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if (r.get("id") or "").strip()]


def load_jsonl(path: Path) -> dict:
    if not path.exists():
        return {}
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return {r["id"]: r for r in rows}


def append_jsonl(path: Path, row: dict) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


# ---------------------------------------------------------------- 1. retrieval

def expected_passages(q: dict) -> list[tuple[str, str]]:
    sources = [s.strip() for s in q["expected_source"].split(";") if s.strip()]
    locations = [s.strip() for s in q["expected_location"].split(";") if s.strip()]
    if len(sources) == 1 and len(locations) > 1:
        sources = sources * len(locations)
    if len(locations) == 1 and len(sources) > 1:
        locations = locations * len(sources)
    return list(zip(sources, locations)) if locations else [(s, "") for s in sources]


def matches(chunk: dict, source: str, location: str) -> bool:
    """A chunk holds an expected passage if the source matches and it covers the
    expected section (or a subsection of it), or the expected page ("p7")."""
    if chunk["source"] != source:
        return False
    if not location:
        return True
    if re.fullmatch(r"p\.? ?\d+", location):
        return f"|{re.sub(r'[^0-9]', '', location)}|" in chunk["pages"]
    sections = chunk["sections"].strip("|").split("|")
    return any(s == location or s.startswith(location + ".") for s in sections)


def query_vector(question: str, cache: dict) -> list[float]:
    if question not in cache:
        cache[question] = index.embed_query(question)
        QUERY_VECTORS.write_text(json.dumps(cache))
    return cache[question]


def evaluate_retrieval(questions: list[dict]) -> list[dict]:
    cache = json.loads(QUERY_VECTORS.read_text()) if QUERY_VECTORS.exists() else {}
    rows = []
    answerable = [q for q in questions if q["kind"].strip() != "unanswerable"]
    for mode in MODES:
        for q in answerable:
            top = retrieval.search(q["question"], k=max(KS), mode=mode, query_vector=query_vector(q["question"], cache))
            passages = expected_passages(q)
            row = {"id": q["id"], "kind": q["kind"], "mode": mode}
            for k in KS:
                found = [any(matches(c, s, loc) for c in top[:k]) for s, loc in passages]
                row[f"hit@{k}"] = int(all(found))
                row[f"words@{k}"] = sum(c["words"] for c in top[:k])
            row["first_hit_rank"] = next((r for r, c in enumerate(top, 1)
                                          if any(matches(c, s, loc) for s, loc in passages)), "")
            rows.append(row)
    write_csv(EVAL / "retrieval.csv", rows)
    return rows


# ---------------------------------------------------------------- 2-4. answers, code checks, judge

def is_refusal(answer: str) -> bool:
    return agent.is_refusal(answer)


def code_checks(q: dict, a: dict) -> dict:
    cited = agent.citations(a["answer"])
    retrieved = set(re.findall(r"^\[\d+\] \((.+)\)$", a["retrieved_text"], flags=re.M))
    expected = {s for s, _ in expected_passages(q)} if q["kind"].strip() != "unanswerable" else set()
    return {
        "refused": int(is_refusal(a["answer"])),
        "citations": len(cited),
        "citations_valid": int(all(c in retrieved for c in cited)),
        "expected_source_cited": int(bool(expected) and expected <= {c.split(",")[0] for c in cited}),
    }


def judge(q: dict, a: dict, model) -> dict:
    prompt = (f"{RUBRIC}\n\nQUESTION: {q['question']}\n\nREFERENCE ANSWER: {q['reference_answer']}\n\n"
              f"ASSISTANT ANSWER: {a['answer']}\n\nRETRIEVED PASSAGES:\n{a['retrieved_text'][:30000]}")
    reply = model.invoke(prompt).text
    verdict = json.loads(re.search(r"\{.*\}", reply, flags=re.S).group(0))
    return {"correct": int(verdict["correct"]), "supported": int(verdict["supported"]), "reason": verdict.get("reason", "")}


def outcome(q: dict, checks: dict, verdict: dict | None) -> str:
    unanswerable = q["kind"].strip() == "unanswerable"
    if checks["refused"]:
        return "correct refusal" if unanswerable else "wrong refusal"
    if unanswerable:
        return "answered unanswerable"
    if verdict is None:
        return "not judged yet"
    if not verdict["supported"]:
        return "unsupported"
    return "correct" if verdict["correct"] else "wrong"


def out_of_quota(error: Exception) -> bool:
    text = str(error)
    return "RESOURCE_EXHAUSTED" in text and ("PerDay" in text or "per day" in text.lower())


def evaluate_answers(questions: list[dict]) -> tuple[list[dict], list[str]]:
    """Pass 1: the agent answers every question. Pass 2: the judge grades them.
    Both are cached; if the daily free-tier quota runs out, the pass stops and the
    next run picks up where it left off."""
    answers, verdicts = load_jsonl(ANSWERS), load_jsonl(VERDICTS)
    pending = []

    for q in questions:
        a = answers.get(q["id"])
        if a is None or a["question"] != q["question"]:
            print(f"  asking {q['id']} ...", file=sys.stderr, flush=True)
            try:
                a = {"id": q["id"], **agent.answer(q["question"])}
            except Exception as error:  # noqa: BLE001
                if not any(out_of_quota(e) for e in getattr(error, "exceptions", [error])) and not out_of_quota(error):
                    raise
                pending.append(f"answers stopped at {q['id']}: daily quota reached")
                break
            append_jsonl(ANSWERS, a)
            answers[q["id"]] = a

    model = ChatGoogleGenerativeAI(model=JUDGE_MODEL, temperature=0, max_retries=2)
    judge_open = True
    rows = []
    for q in questions:
        a = answers.get(q["id"])
        if a is None or a["question"] != q["question"]:
            continue
        checks = code_checks(q, a)
        verdict = None
        if not checks["refused"] and q["kind"].strip() != "unanswerable":
            v = verdicts.get(q["id"])
            if (v is None or v.get("answer") != a["answer"] or v.get("rubric") != RUBRIC) and judge_open:
                try:
                    v = {"id": q["id"], "answer": a["answer"], "rubric": RUBRIC, **judge(q, a, model)}
                    append_jsonl(VERDICTS, v)
                    verdicts[q["id"]] = v
                except Exception as error:  # noqa: BLE001
                    if not out_of_quota(error):
                        raise
                    pending.append(f"judging stopped at {q['id']}: daily quota reached")
                    judge_open = False
            if v is not None and v.get("answer") == a["answer"] and v.get("rubric") == RUBRIC:
                verdict = v
        rows.append({
            "id": q["id"], "kind": q["kind"], **checks,
            "judge_correct": "" if verdict is None else verdict["correct"],
            "judge_supported": "" if verdict is None else verdict["supported"],
            "judge_reason": "" if verdict is None else verdict["reason"],
            "outcome": outcome(q, checks, verdict),
            "guardrail": a.get("guardrail") or "",
            "tool_calls": len(a["trace"]),
            "input_tokens": a["input_tokens"], "output_tokens": a["output_tokens"], "seconds": a["seconds"],
            "answer": a["answer"],
        })
    write_csv(EVAL / "results.csv", rows)
    return rows, pending


# ---------------------------------------------------------------- 5. agreement with my grades

def system_grades(row: dict) -> tuple[int, int]:
    """The judge's grades, or the code's for refusals (a refusal is supported; it is
    correct only when the question is unanswerable)."""
    if row["refused"] or row["kind"].strip() == "unanswerable":
        right = int(row["outcome"] == "correct refusal")
        return right, int(row["refused"])  # a refusal makes no claim; an answer to an unanswerable question is made up
    return int(row["judge_correct"]), int(row["judge_supported"])


def agreement(results: list[dict]) -> dict:
    by_id = {r["id"]: r for r in results}
    pairs = [(h, by_id[h["id"]]) for h in read_csv(HUMAN)
             if h["id"] in by_id and by_id[h["id"]]["outcome"] != "not judged yet"]
    if not pairs:
        return {"graded": 0}
    same_correct = sum(int(h["correct"]) == system_grades(r)[0] for h, r in pairs)
    same_supported = sum(int(h["supported"]) == system_grades(r)[1] for h, r in pairs)
    disagreements = [h["id"] for h, r in pairs if (int(h["correct"]), int(h["supported"])) != system_grades(r)]
    return {"graded": len(pairs),
            "agree_correct": round(same_correct / len(pairs), 3),
            "agree_supported": round(same_supported / len(pairs), 3),
            "disagreements": disagreements}


# ---------------------------------------------------------------- summary

def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    started = time.time()
    load_api_key()  # also needed when every answer comes from the cache
    questions = read_csv(QUESTIONS)
    if not questions:
        raise SystemExit("eval/questions.csv has no questions yet.")

    retrieval_rows = evaluate_retrieval(questions)
    hit_rates = {}
    for mode in MODES:
        rows = [r for r in retrieval_rows if r["mode"] == mode]
        hit_rates[mode] = {f"hit@{k}": round(statistics.mean(r[f"hit@{k}"] for r in rows), 3) for k in KS}
        hit_rates[mode].update({f"words@{k}": round(statistics.mean(r[f"words@{k}"] for r in rows)) for k in KS})

    results, pending = evaluate_answers(questions)
    counts = {}
    for r in results:
        counts[r["outcome"]] = counts.get(r["outcome"], 0) + 1
    summary = {
        "questions": len(questions),
        "kinds": {k: sum(q["kind"].strip() == k for q in questions) for k in ("single", "multi", "unanswerable")},
        "retrieval": hit_rates,
        "search_design": json.loads(index.CONFIG_FILE.read_text()) if index.CONFIG_FILE.exists() else {},
        "outcomes": counts,
        "citations_valid": round(statistics.mean(r["citations_valid"] for r in results), 3),
        "guardrail_fired": sum(bool(r["guardrail"]) for r in results),
        "agreement_with_my_grades": agreement(results),
        "per_question": {
            "mean_input_tokens": round(statistics.mean(r["input_tokens"] for r in results)),
            "mean_output_tokens": round(statistics.mean(r["output_tokens"] for r in results)),
            "mean_seconds": round(statistics.mean(r["seconds"] for r in results), 1),
            "mean_tool_calls": round(statistics.mean(r["tool_calls"] for r in results), 2),
        },
        "evaluation_seconds": round(time.time() - started),
        "answered": len(results),
        "incomplete": pending,
    }
    (EVAL / "summary.json").write_text(json.dumps(summary, indent=2))
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
