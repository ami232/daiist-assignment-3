"""
Assignment 3: evaluation (`main.py evaluate`).

1. Retrieval: hit rate at k = 1, 3, 5 for each design (chunking x search mode),
   words added to the prompt, choice of the best design -> index/config.json.
2. End to end: the agent (agent.py) answers every question in eval/questions.csv
   with only the base corpus visible (documents added later are hidden).
3. Code checks: refusal, citations present, citations valid (returned by search),
   expected source cited.
4. LLM judge with a rubric, given the retrieved passages as evidence.
5. Agreement between the judge and eval/human_labels.csv.
6. Failure causes (automatic first guess, to review by hand).
7. Before/after: add a document that answers one unanswerable question.
8. Cost: tokens and seconds per question.

Agent answers and judge verdicts are cached in eval/ (answers.jsonl, judge.jsonl)
so re-running costs no quota; delete those files to start fresh.
To redo only some questions (uses quota for those only):
  EVAL_RERUN=q25 uv run python main.py evaluate      # ask the agent again (and re-judge)
  EVAL_REJUDGE=m02 uv run python main.py evaluate    # keep the answer, judge it again
"""

from __future__ import annotations

import csv
import json
import os
import re
import sys
import time
from pathlib import Path

import index
from agent import ask, check_numbers, citation_valid, is_refusal, split_label

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
HUMAN = EVAL / "human_labels.csv"
ANSWERS = EVAL / "answers.jsonl"
JUDGE = EVAL / "judge.jsonl"
JUDGE_MODEL = os.environ.get("JUDGE_MODEL", os.environ.get("CHAT_MODEL", "gemini-flash-lite-latest"))
SLEEP = float(os.environ.get("EVAL_SLEEP", "4"))     # seconds between agent calls (free-tier RPM)
RERUN = {x.strip() for x in os.environ.get("EVAL_RERUN", "").split(",") if x.strip()}
REJUDGE = {x.strip() for x in os.environ.get("EVAL_REJUDGE", "").split(",") if x.strip()} | RERUN

# the unanswerable question used for the before/after demo, and the document that answers it
ADD_DEMO_ID = "u01"
ADD_DEMO_FILE = index.EXTRA_DIR / f"{index.EXTRA_DOCUMENTS['Reg 2022/860']}.html"

RETRIEVAL_DESIGNS = [("fixed", "vector"), ("structure", "vector"), ("structure", "bm25"),
                     ("structure", "hybrid"), ("fixed", "hybrid")]


def load_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r["question"].strip()]


def expected_pairs(q: dict) -> list[tuple[str, str]]:
    """'A; B' sources with 'locA; locB' locations, paired by position."""
    srcs = [s.strip() for s in q["expected_source"].split(";") if s.strip()]
    locs = [l.strip() for l in q["expected_location"].split(";") if l.strip()]
    if len(srcs) == len(locs):
        return list(zip(srcs, locs))
    if len(srcs) == 1:
        return [(srcs[0], l) for l in locs] or [(srcs[0], "")]
    return [(s, l) for s in srcs for l in (locs or [""])]


def norm(s: str) -> str:
    return re.sub(r"\s+", " ", s.strip().lower().replace("art.", "article"))


def loc_match(expected: str, section: str) -> bool:
    e, s = norm(expected), norm(section)
    if not e or e == s:
        return True
    if e.startswith("annex (") and s.startswith("annex"):      # health-claim rows: match by nutrient
        inner_e, inner_s = e[e.index("(") + 1:].rstrip(")"), s[s.find("(") + 1:].rstrip(")")
        return inner_e in inner_s
    return False


def chunk_hits(chunk: dict, pair: tuple[str, str]) -> bool:
    src, loc = pair
    return chunk["source"] == src and any(loc_match(loc, s) for s in chunk["sections"].split("|"))


# ----------------------------------------------------------------------------- 1. retrieval

def evaluate_retrieval(questions: list[dict]) -> tuple[list[dict], dict]:
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    rows, per_q = [], []
    for design, mode in RETRIEVAL_DESIGNS:
        if index.collection(design).count() == 0:
            print(f"  skipping {design}: not indexed")
            continue
        hits = {1: 0, 3: 0, 5: 0}
        all_hits = {1: 0, 3: 0, 5: 0}
        words5 = []
        for q in answerable:
            res = index.search(q["question"], k=5, design=design, mode=mode, corpus_only=True)
            pairs = expected_pairs(q)
            words5.append(sum(r["words"] for r in res))
            first = None
            for k in (1, 3, 5):
                found = [any(chunk_hits(c, p) for c in res[:k]) for p in pairs]
                hits[k] += any(found)
                all_hits[k] += all(found)
            for rank, c in enumerate(res, 1):
                if any(chunk_hits(c, p) for p in pairs):
                    first = rank
                    break
            per_q.append({"design": f"{design}/{mode}", "id": q["id"], "first_hit_rank": first or "",
                          "top5": " || ".join(r["cite"] for r in res)})
        n = len(answerable)
        multi = sum(1 for q in answerable if q["kind"] == "multi")
        rows.append({"design": f"{design}/{mode}", "chunking": index.DESIGNS[design], "search": mode,
                     "hit@1": round(hits[1] / n, 3), "hit@3": round(hits[3] / n, 3), "hit@5": round(hits[5] / n, 3),
                     "all_passages@5": round(all_hits[5] / n, 3),
                     "avg_words_top5": round(sum(words5) / n), "questions": n, "multi": multi})
    best = max(rows, key=lambda r: (r["hit@3"], r["hit@5"], r["hit@1"], -r["avg_words_top5"]))
    design, mode = best["design"].split("/")
    config = {"design": design, "mode": mode, "k": 5, "chosen_by": "highest hit@3, then hit@5, hit@1, fewer words"}
    index.CONFIG_FILE.write_text(json.dumps(config, indent=2))
    write_csv(EVAL / "retrieval.csv", rows)
    write_csv(EVAL / "retrieval_per_question.csv", per_q)
    return rows, config


# ----------------------------------------------------------------------------- 2. answers

def read_jsonl(path: Path) -> dict:
    if not path.exists():
        return {}
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            out[r["id"]] = r
    return out


def append_jsonl(path: Path, row: dict) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def run_agent(questions: list[dict]) -> dict:
    cached = read_jsonl(ANSWERS)
    for q in questions:
        if q["id"] in cached and not cached[q["id"]].get("error") and q["id"] not in RERUN:
            continue
        print(f"  asking {q['id']}: {q['question'][:70]}")
        try:
            out = ask(q["question"], approver=lambda n, a: False, corpus_only=True)
            row = {"id": q["id"], **out}
        except Exception as e:  # noqa: BLE001
            row = {"id": q["id"], "question": q["question"], "error": f"{type(e).__name__}: {str(e)[:300]}"}
            print(f"    error: {row['error']}")
            if "PerDay" in str(e) or "per day" in str(e).lower():
                print("  daily quota reached: stopping here, cached answers are kept. Run again tomorrow.")
                append_jsonl(ANSWERS, row)
                break
        append_jsonl(ANSWERS, row)
        cached[q["id"]] = row
        time.sleep(SLEEP)
    return read_jsonl(ANSWERS)


# ----------------------------------------------------------------------------- 3. code checks

def code_checks(q: dict, a: dict) -> dict:
    labels = set(a.get("retrieved_labels", []))
    cites = a.get("citations", [])
    refused = is_refusal(a.get("answer", ""))
    pairs = expected_pairs(q) if q["kind"] != "unanswerable" else []
    retrieved_expected = any(
        split_label(l)[0] == s and any(loc_match(loc, x) for x in _sections(split_label(l)[1]))
        for l in labels for s, loc in pairs)
    cited_expected = any(
        split_label(c)[0] == s and any(loc_match(loc, x) for x in _sections(split_label(c)[1]))
        for c in cites for s, loc in pairs)
    return {
        "refused": int(refused),
        "has_citation": int(bool(cites)),
        "citations_valid": int(all(citation_valid(c, labels) for c in cites)),
        "searched": int(any(t["tool"] == "search" for t in a.get("trace", []))),
        "retrieved_expected": int(retrieved_expected),
        "cited_expected": int(cited_expected),
    }


def _sections(location: str) -> list[str]:
    from agent import _expand
    return list(_expand(location))


# ----------------------------------------------------------------------------- 4. judge

RUBRIC = """You grade answers of a regulatory assistant about EU food-supplement law.
You get: the question, a reference answer written by an expert, the passages the assistant
retrieved (its only allowed evidence), and the assistant's answer.

Return JSON: {"correct": 0 or 1, "supported": 0 or 1, "reason": "<one sentence>"}

correct = 1 when the answer gives the same key facts as the reference: the same yes/no,
the same numbers, units, dates and authorised wording, and for two-part questions both parts.
Extra correct detail is fine. Missing a key fact, a wrong number, or a contradiction = 0.
An answer that refuses ("The corpus does not cover this") when the reference has an answer = 0.
If it answers part and correctly says the rest is not covered, judge only whether the key
facts of the reference are there.

supported = 1 when every factual statement in the answer can be found in the retrieved
passages (paraphrase is fine). Any fact, number or rule that is not in the passages = 0,
even if it is true. A refusal is supported.

Be strict: a confident wrong answer is the costliest error for this user."""


def judge_one(q: dict, a: dict) -> dict:
    from google.genai import types

    evidence = "\n\n".join(t["output"] for t in a.get("trace", []) if t["tool"] == "search")[:30000]
    prompt = (f"{RUBRIC}\n\nQUESTION:\n{q['question']}\n\nREFERENCE ANSWER:\n{q['reference_answer']}\n\n"
              f"RETRIEVED PASSAGES:\n{evidence or '(none)'}\n\nASSISTANT ANSWER:\n{a['answer']}")
    from agent import candidate_models

    models = [JUDGE_MODEL] + [m for m in candidate_models() if m != JUDGE_MODEL]
    for attempt in range(8):
        model = models[min(attempt // 2, len(models) - 1)]     # switch model after 2 failures
        try:
            res = index.genai_client().models.generate_content(
                model=model, contents=prompt,
                config=types.GenerateContentConfig(temperature=0, response_mime_type="application/json"))
            v = json.loads(res.text)
            u = res.usage_metadata
            return {"correct": int(v["correct"]), "supported": int(v["supported"]), "reason": v.get("reason", ""),
                    "judge_tokens": (u.prompt_token_count or 0) + (u.candidates_token_count or 0) if u else 0}
        except Exception as e:  # noqa: BLE001
            if any(c in str(e) for c in ("429", "RESOURCE_EXHAUSTED", "503", "UNAVAILABLE", "404")):
                if "PerDay" in str(e):
                    raise
                time.sleep(15)
                continue
            if attempt < 2:
                continue
            raise
    raise RuntimeError("judge kept failing")


def grade(questions, answers) -> list[dict]:
    verdicts = read_jsonl(JUDGE)
    rows = []
    for q in questions:
        a = answers.get(q["id"])
        if not a or a.get("error"):
            continue
        checks = code_checks(q, a)
        if q["kind"] == "unanswerable":       # code decides: a refusal is correct
            v = {"correct": checks["refused"], "supported": checks["refused"],
                 "reason": "code: refusal" if checks["refused"] else "code: answered an unanswerable question"}
        elif checks["refused"]:
            v = {"correct": 0, "supported": 1, "reason": "code: refused an answerable question"}
        else:
            if q["id"] not in verdicts or q["id"] in REJUDGE:
                try:
                    v = judge_one(q, a)
                except Exception as e:  # noqa: BLE001
                    print(f"  judge failed on {q['id']}: {e}")
                    continue
                append_jsonl(JUDGE, {"id": q["id"], **v})
                time.sleep(SLEEP / 2)
            v = read_jsonl(JUDGE)[q["id"]]
        if checks["has_citation"] and not checks["citations_valid"]:
            v = {**v, "supported": 0, "reason": v["reason"] + " | code: invalid citation"}
        # number check (flag only); computed here too so cached answers from older runs get it
        passages = "\n".join(t["output"] for t in a.get("trace", []) if t["tool"] == "search")
        numbers = a.get("unsupported_numbers", check_numbers(a["answer"], passages, q["question"]))
        rows.append({"id": q["id"], "kind": q["kind"], **checks, "correct": v["correct"],
                     "supported": v["supported"], "judge_reason": v["reason"],
                     "tokens": a.get("tokens_in", 0) + a.get("tokens_out", 0), "seconds": a.get("seconds", 0),
                     "guardrail": "; ".join(a.get("guardrail_events", [])),
                     "unsupported_numbers": "; ".join(numbers), "model": a.get("model", ""),
                     "answer": a["answer"].replace("\n", " ")[:600]})
    return rows


# ----------------------------------------------------------------------------- 5. agreement

def agreement(rows) -> dict:
    if not HUMAN.exists():
        return {}
    with HUMAN.open(newline="", encoding="utf-8") as f:
        human = {r["id"]: r for r in csv.DictReader(f) if r.get("id", "").strip() and r.get("correct", "").strip()}
    judged = {r["id"]: r for r in rows}
    out = {}
    for field in ("correct", "supported"):
        pairs = [(int(human[i][field]), int(judged[i][field])) for i in human if i in judged and human[i].get(field, "").strip()]
        if not pairs:
            continue
        agree = sum(h == j for h, j in pairs) / len(pairs)
        ph = sum(h for h, _ in pairs) / len(pairs)
        pj = sum(j for _, j in pairs) / len(pairs)
        pe = ph * pj + (1 - ph) * (1 - pj)
        kappa = (agree - pe) / (1 - pe) if pe < 1 else 1.0
        out[field] = {"n": len(pairs), "agreement": round(agree, 3), "cohen_kappa": round(kappa, 3),
                      "disagree_ids": [i for i in human if i in judged and human[i].get(field, "").strip()
                                       and int(human[i][field]) != int(judged[i][field])]}
    return out


# ----------------------------------------------------------------------------- 6. failures

def classify(rows) -> list[dict]:
    fails = []
    for r in rows:
        if r["correct"] and r["supported"]:
            continue
        if r["kind"] == "unanswerable":
            cause = "unsupported claim"                  # answered instead of refusing
        elif r["refused"]:
            cause = "wrong refusal" if r["retrieved_expected"] else "retrieval miss"
        elif not r["retrieved_expected"]:
            cause = "retrieval miss"
        elif not r["correct"]:
            cause = "wrong answer from right passage"
        else:
            cause = "unsupported claim"
        fails.append({"id": r["id"], "kind": r["kind"], "auto_cause": cause, "manual_cause": "",
                      "correct": r["correct"], "supported": r["supported"], "judge_reason": r["judge_reason"]})
    manual = EVAL / "failures.csv"
    if manual.exists():                                   # keep causes reviewed by hand
        with manual.open(newline="", encoding="utf-8") as f:
            old = {r["id"]: r.get("manual_cause", "") for r in csv.DictReader(f)}
        for x in fails:
            x["manual_cause"] = old.get(x["id"], "")
    write_csv(manual, fails or [{"id": "", "kind": "", "auto_cause": "", "manual_cause": ""}])
    return fails


# ----------------------------------------------------------------------------- 7. before/after

def before_after(questions, answers) -> dict:
    q = next((x for x in questions if x["id"] == ADD_DEMO_ID), None)
    if q is None or not ADD_DEMO_FILE.exists():
        return {}
    out_file = EVAL / "before_after.json"
    if out_file.exists():
        return json.loads(out_file.read_text())
    before = answers.get(ADD_DEMO_ID, {})
    # Add the document through the agent, approving the add_document call as the operator.
    add = ask(f"Please add the document at {ADD_DEMO_FILE} to the corpus.", approver=lambda n, a: True)
    after = ask(q["question"], approver=lambda n, a: False, corpus_only=False)
    result = {"question": q["question"], "document": "Commission Regulation (EU) 2022/860 (monacolins from red yeast rice)",
              "before": before.get("answer"), "before_citations": before.get("citations"),
              "add_step": add["answer"], "add_trace": [{k: t[k] for k in ("tool", "args", "output")} for t in add["trace"]],
              "after": after["answer"], "after_citations": after["citations"]}
    out_file.write_text(json.dumps(result, indent=2, ensure_ascii=False))
    return result


# ----------------------------------------------------------------------------- main

def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)


def wilson(x: int, n: int, z: float = 1.96) -> list[float]:
    """95 % Wilson score interval for x successes out of n."""
    if not n:
        return [0.0, 0.0]
    p = x / n
    centre = (p + z * z / (2 * n)) / (1 + z * z / n)
    half = z * ((p * (1 - p) / n + z * z / (4 * n * n)) ** 0.5) / (1 + z * z / n)
    return [round(centre - half, 3), round(centre + half, 3)]


def pct(x, n):
    return f"{x}/{n} ({100 * x / n:.0f}%)" if n else "0/0"


def main() -> None:
    questions = load_questions()
    print("\n=== 1. Retrieval")
    rows, config = evaluate_retrieval(questions)
    for r in rows:
        print(f"  {r['design']:<18} hit@1 {r['hit@1']:.2f}  hit@3 {r['hit@3']:.2f}  hit@5 {r['hit@5']:.2f}"
              f"  all@5 {r['all_passages@5']:.2f}  words@5 {r['avg_words_top5']}")
    print(f"  chosen: {config['design']}/{config['mode']}")

    print("\n=== 2. Agent answers")
    answers = run_agent(questions)

    print("\n=== 3-4. Code checks and judge")
    graded = grade(questions, answers)
    write_csv(EVAL / "results.csv", graded)

    ans = [r for r in graded if r["kind"] != "unanswerable"]
    una = [r for r in graded if r["kind"] == "unanswerable"]
    summary = {
        "chat_model": os.environ.get("CHAT_MODEL", "gemini-flash-lite-latest"), "judge_model": JUDGE_MODEL,
        "retrieval_design": config, "graded": len(graded), "of_questions": len(questions),
        "answerable": {
            "n": len(ans),
            "correct": sum(r["correct"] for r in ans),
            "correct_and_supported": sum(r["correct"] and r["supported"] for r in ans),
            "unsupported": sum(1 - r["supported"] for r in ans),
            "wrong_refusals": sum(r["refused"] for r in ans),
        },
        "unanswerable": {"n": len(una), "correct_refusals": sum(r["refused"] for r in una),
                         "made_up_answers": sum(1 - r["refused"] for r in una)},
        "code_checks": {
            "answers_with_citation": sum(r["has_citation"] for r in graded),
            "all_citations_valid": sum(r["citations_valid"] for r in graded),
            "cited_expected_passage": sum(r["cited_expected"] for r in ans),
            "guardrail_fired": [r["id"] for r in graded if r["guardrail"]],
            "citation_repair_turns": [r["id"] for r in graded if "citation check failed" in r["guardrail"]],
            "replaced_by_refusal": [r["id"] for r in graded if "failed again" in r["guardrail"]],
            "number_check_flagged": {r["id"]: r["unsupported_numbers"] for r in graded if r["unsupported_numbers"]},
        },
        "answered_by_model": {m: sum(1 for r in graded if r["model"] == m)
                              for m in sorted({r["model"] for r in graded})},
        "cost_per_question": {
            "tokens_mean": round(sum(r["tokens"] for r in graded) / max(len(graded), 1)),
            "seconds_mean": round(sum(r["seconds"] for r in graded) / max(len(graded), 1), 1),
            "seconds_max": max((r["seconds"] for r in graded), default=0),
        },
    }
    a, u = summary["answerable"], summary["unanswerable"]
    summary["wilson_95"] = {"answerable_correct": wilson(a["correct"], a["n"]),
                            "unanswerable_correct_refusals": wilson(u["correct_refusals"], u["n"])}
    print(f"  answerable: correct {pct(a['correct'], a['n'])}, unsupported {a['unsupported']}, "
          f"wrong refusals {a['wrong_refusals']}")
    print(f"  unanswerable: correct refusals {pct(u['correct_refusals'], u['n'])}, made up {u['made_up_answers']}")
    print(f"  cost: {summary['cost_per_question']}")
    print(f"  95% Wilson: {summary['wilson_95']}")
    print(f"  citation repair turns: {summary['code_checks']['citation_repair_turns']}")
    print(f"  replaced by refusal: {summary['code_checks']['replaced_by_refusal']}")
    print(f"  number check flagged: {summary['code_checks']['number_check_flagged']}")
    print(f"  answered by model: {summary['answered_by_model']}")

    print("\n=== 5. Judge vs human labels")
    summary["judge_agreement"] = agreement(graded)
    print(f"  {summary['judge_agreement'] or 'eval/human_labels.csv has no labels yet'}")

    print("\n=== 6. Failures")
    fails = classify(graded)
    counts = {}
    for f in fails:
        c = f["manual_cause"] or f["auto_cause"]
        counts[c] = counts.get(c, 0) + 1
    summary["failures"] = counts
    print(f"  {counts}")

    print("\n=== 7. Adding a document (before/after)")
    try:
        ba = before_after(questions, answers)
        summary["before_after"] = {k: ba.get(k) for k in ("question", "before", "after")}
        print(json.dumps(summary["before_after"], indent=2, ensure_ascii=False)[:1500])
    except Exception as e:  # noqa: BLE001
        print(f"  skipped: {e}")

    (EVAL / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    print("\nSaved eval/retrieval.csv, results.csv, failures.csv, summary.json")


if __name__ == "__main__":
    main()
