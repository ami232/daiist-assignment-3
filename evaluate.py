"""
Assignment 3: evaluation (`main.py evaluate`).

1. Retrieval: hit rate at k = 1, 3, 5 for each design (chunking x vector or
   hybrid search), and the words each design adds to the prompt.
2. End to end: the agent answers every question (answers are cached in
   eval/answers.jsonl; set RERUN=1 to ask again).
3. Code checks: refusal or not, citations that search really returned, and
   whether the expected source was cited.
4. LLM judge with a rubric and the retrieved text as evidence.
5. Agreement with my own grades in eval/human_labels.csv.

Writes eval/retrieval.csv, eval/results.csv and eval/summary.json.
"""

import csv
import json
import os
import re
import time
from pathlib import Path

from agent import CITATION, REFUSAL, ask
from index import DESIGNS, collection
from retrieval import search

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
KS = (1, 3, 5)
JUDGE_MODEL = os.environ.get("JUDGE_MODEL", "gemini-3.1-flash-lite")

RUBRIC = """You grade an assistant that answers questions about EU cosmetics law for a
perfume brand. You get the question, a reference answer written by a person,
the passages the assistant retrieved, and the assistant's answer.

correct = 1 if the answer gives the same rule, number and condition as the
  reference answer (other wording is fine; extra correct detail is fine;
  a missing key condition or a different number is 0). For a question the
  corpus cannot answer, correct = 1 only if the assistant says the corpus does
  not cover it. If the assistant refuses a question that has a reference
  answer, correct = 0.
supported = 1 if every factual claim in the answer can be found in the
  retrieved passages; 0 if any claim (a number, a rule, a condition) is not in
  them. A pure refusal is supported = 1.

Reply with JSON only: {"correct": 0 or 1, "supported": 0 or 1, "reason": "<one sentence>"}"""


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


# ------------------------------------------------------------------ retrieval

def expected_pairs(q: dict) -> list[tuple[str, str]]:
    return list(zip(q["expected_source"].split(";"), q["expected_location"].split(";")))


def hits_expected(hit: dict, source: str, location: str) -> bool:
    """Does a retrieved chunk contain the expected passage?

    An annex entry is found if the chunk holds that entry ("ANNEX III entry 84.");
    an article or section if the chunk's location names it (a fixed window can
    span two: "Article 18, ... to Article 19, ...").
    """
    if hit["source"] != source.strip():
        return False
    location = location.strip()
    entry = re.fullmatch(r"(ANNEX [IVX]+), entry (\w+)", location)
    if entry:
        return f"{entry[1]} entry {entry[2]}." in hit["text"]
    # A fixed window spanning two places reads "A to B"; "Exposure to the..." does not split.
    parts = [p.strip() for p in re.split(r" to (?=Article |ANNEX|page |paragraph )", hit["location"])]
    return any(p == location or p.startswith(location + ",") or p.startswith(location + " ") for p in parts)


def retrieval_eval(questions: list[dict]) -> list[dict]:
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    rows = []
    for design in DESIGNS:
        if collection(design).count() == 0:
            print(f"[retrieval] design {design!r} has no vectors yet; skipped")
            continue
        for hybrid in (False, True):
            name = f"{design} + {'hybrid' if hybrid else 'vector'}"
            found = {k: 0 for k in KS}
            all_found = {k: 0 for k in KS}
            words = 0
            for q in answerable:
                hits = search(q["question"], k=max(KS), design=design, hybrid=hybrid)
                words += sum(len(h["text"].split()) for h in hits)
                pairs = expected_pairs(q)
                for k in KS:
                    got = [any(hits_expected(h, s, l) for h in hits[:k]) for s, l in pairs]
                    found[k] += any(got)
                    all_found[k] += all(got)
            n = len(answerable)
            rows.append({"design": name, **{f"hit@{k}": round(found[k] / n, 3) for k in KS},
                         **{f"all@{k}": round(all_found[k] / n, 3) for k in KS},
                         "words_in_prompt@5": round(words / n)})
            print(f"[retrieval] {rows[-1]}")
    return rows


# ------------------------------------------------------------------- answers

def answers(questions: list[dict]) -> dict[str, dict]:
    path = EVAL / "answers.jsonl"
    cached = {}
    if path.exists() and not os.environ.get("RERUN"):
        for line in path.read_text(encoding="utf-8").splitlines():
            a = json.loads(line)
            cached[a["question"]] = a
    out = {}
    with path.open("a" if cached else "w", encoding="utf-8") as f:
        for q in questions:
            if q["question"] in cached:
                out[q["id"]] = cached[q["question"]]
                continue
            for attempt in range(3):
                try:
                    a = ask(q["question"], approve=lambda *_: False)
                    break
                except Exception as error:  # noqa: BLE001 - a 503 or a timeout: wait and retry
                    print(f"[agent] {q['id']} failed ({str(error)[:100]}); retrying")
                    time.sleep(20 * (attempt + 1))
            else:
                a = {"question": q["question"], "answer": "ERROR", "raw_answer": "ERROR", "guardrail": None,
                     "trace": [], "retrieved": "", "tokens": {"input": 0, "output": 0}, "seconds": 0}
            f.write(json.dumps(a, ensure_ascii=False) + "\n")
            f.flush()
            out[q["id"]] = a
            print(f"[agent] {q['id']} {a['seconds']}s: {a['answer'][:90]!r}")
    return out


def code_checks(q: dict, a: dict) -> dict:
    refused = a["answer"].strip().startswith(REFUSAL)
    cited = [(s.strip(), l.strip()) for s, l in CITATION.findall(a["answer"])]
    pairs = expected_pairs(q) if q["kind"] != "unanswerable" else []
    cites_expected = any(hits_expected({"source": s, "location": l, "text": a["retrieved"]}, es, el)
                         for s, l in cited for es, el in pairs)
    return {"refused": int(refused), "n_citations": len(cited),
            "citations_valid": int(a["guardrail"] is None),
            "cites_expected_source": int(cites_expected),
            "correct_refusal": int(refused and q["kind"] == "unanswerable"),
            "wrong_refusal": int(refused and q["kind"] != "unanswerable")}


def judge(q: dict, a: dict) -> dict:
    from google.genai import types
    from index import client
    prompt = (f"{RUBRIC}\n\nQUESTION: {q['question']}\nKIND: {q['kind']}\n"
              f"REFERENCE ANSWER: {q['reference_answer']}\n\nRETRIEVED PASSAGES:\n{a['retrieved'][:12000]}\n\n"
              f"ASSISTANT ANSWER:\n{a['answer']}")
    for attempt in range(4):
        try:
            r = client().models.generate_content(
                model=JUDGE_MODEL, contents=prompt,
                config=types.GenerateContentConfig(temperature=0, response_mime_type="application/json"))
            v = json.loads(r.text)
            return {"judge_correct": int(v["correct"]), "judge_supported": int(v["supported"]),
                    "judge_reason": v.get("reason", "")}
        except Exception as error:  # noqa: BLE001
            print(f"[judge] {q['id']} failed ({str(error)[:100]}); retrying")
            time.sleep(15 * (attempt + 1))
    return {"judge_correct": "", "judge_supported": "", "judge_reason": "judge failed"}


def agreement(results: list[dict]) -> dict:
    human = {r["id"]: r for r in read_csv(EVAL / "human_labels.csv") if r.get("id")}
    both = [r for r in results if r["id"] in human and r["judge_correct"] != ""]
    if not both:
        return {"graded_by_me": 0}
    agree = {m: sum(int(human[r["id"]][m]) == int(r[f"judge_{m}"]) for r in both) / len(both)
             for m in ("correct", "supported")}
    return {"graded_by_me": len(both), **{f"agreement_{m}": round(v, 3) for m, v in agree.items()},
            "disagreements": [r["id"] for r in both
                              if int(human[r["id"]]["correct"]) != int(r["judge_correct"])
                              or int(human[r["id"]]["supported"]) != int(r["judge_supported"])]}


def main() -> None:
    questions = [q for q in read_csv(EVAL / "questions.csv") if q["question"].strip()]
    retrieval_rows = retrieval_eval(questions)
    if retrieval_rows:
        write_csv(EVAL / "retrieval.csv", retrieval_rows)

    got = answers(questions)
    results = []
    for q in questions:
        a = got[q["id"]]
        results.append({"id": q["id"], "kind": q["kind"], "question": q["question"],
                        "answer": a["answer"], "guardrail": a["guardrail"] or "",
                        **code_checks(q, a), **judge(q, a),
                        "tokens": a["tokens"]["input"] + a["tokens"]["output"], "seconds": a["seconds"],
                        "searches": sum(t["tool"] == "search" for t in a["trace"])})
    write_csv(EVAL / "results.csv", results)

    n = len(results)
    answered = [r for r in results if not r["refused"]]
    summary = {
        "questions": n,
        "correct (judge)": sum(r["judge_correct"] == 1 for r in results),
        "answered": len(answered),
        "answered and correct": sum(r["judge_correct"] == 1 for r in answered),
        "unsupported answers": sum(r["judge_supported"] == 0 for r in answered),
        "correct refusals": sum(r["correct_refusal"] for r in results),
        "wrong refusals": sum(r["wrong_refusal"] for r in results),
        "unanswerable answered anyway": sum(r["kind"] == "unanswerable" and not r["refused"] for r in results),
        "guardrail fired": sum(bool(r["guardrail"]) for r in results),
        "avg tokens per question": round(sum(r["tokens"] for r in results) / n),
        "avg seconds per question": round(sum(r["seconds"] for r in results) / n, 1),
        "judge model": JUDGE_MODEL,
        **agreement(results),
        "retrieval": retrieval_rows,
    }
    (EVAL / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    print(json.dumps({k: v for k, v in summary.items() if k != "retrieval"}, indent=2, ensure_ascii=False))


if __name__ == "__main__":
    main()
