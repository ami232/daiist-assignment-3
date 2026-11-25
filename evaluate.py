"""
Assignment 3: evaluation (`main.py evaluate`).

Stages
  1. Retrieval: hit rate at k = 1, 3, 5 for each chunking design (article vs fixed).
  2. Answers: the agent (agent.py) answers every question; answers and tool traces are saved to
     eval/answers.jsonl as they come in, and reused on later runs (FRESH=1 re-asks everything).
     Also writes eval/to_grade.md, the sheet for grading answers by hand.
  3. Checks in code: citation validity (guardrail), refusals, whether the expected passage was
     retrieved. LLM judge (Gemini, rubric below) for correctness and support of answered
     questions; verdicts cached in eval/judge.jsonl.
  4. Agreement between eval/human_labels.csv and the final labels; failure list with a suggested
     category; cost per question. Outputs: eval/results.csv, eval/failures.csv, eval/summary.json

Commands
  uv run python main.py evaluate         all stages (answers are reused if already saved)
  uv run python evaluate.py answers      stages 1-2 only: get answers to grade by hand first
  uv run python evaluate.py before-after add the UCITS V Directive with add_document (approval
                                         asked) and show the answer to q35 before and after
"""
from __future__ import annotations

import csv
import json
import os
import sys
from pathlib import Path

import index as ix

ROOT = Path(__file__).resolve().parent
EVAL_DIR = ROOT / "eval"
ANSWERS_FILE = EVAL_DIR / "answers.jsonl"
JUDGE_FILE = EVAL_DIR / "judge.jsonl"
HUMAN_FILE = EVAL_DIR / "human_labels.csv"
KS = (1, 3, 5)
BATCH = 5  # questions per MCP session; a crash loses at most one batch

BEFORE_AFTER_ID = "q35"
ADDED_DOC = {"celex": "32014L0091", "file": "corpus/ucits_v_directive.html",
             "title": "Directive 2014/91/EU (UCITS V)", "min_words": 5_000}

JUDGE_RUBRIC = """You grade answers of a UCITS rules assistant used by a fund compliance analyst.
You get the question, a reference answer written by the test author, the passages the assistant
retrieved, and the assistant's answer.

correct (1 or 0): 1 if the answer gives the same rule as the reference answer AND every number,
threshold and condition of the reference that matters for the decision is present and matches.
Extra details are fine if the passages do not contradict them. A wrong or missing key number,
limit or condition, or a different conclusion, is 0.

supported (1 or 0): 1 if every factual claim in the answer can be found in the retrieved passages
(paraphrase is fine). 0 if any claim, number or condition is not in the passages.

Reply with JSON only: {"correct": 0 or 1, "supported": 0 or 1, "reason": "one short sentence"}"""


# --------------------------------------------------------------------------- helpers
def load_questions() -> list[dict]:
    with open(EVAL_DIR / "questions.csv", encoding="utf-8-sig") as fh:
        return list(csv.DictReader(fh))


def expected_pairs(q: dict) -> set[tuple[str, str]]:
    if not q["expected_source"].strip():
        return set()
    sources = [s.strip() for s in q["expected_source"].split(";")]
    locations = [l.strip() for l in q["expected_location"].split(";")]
    return set(zip(sources, locations))


def read_jsonl(path: Path) -> dict:
    out = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                row = json.loads(line)
                out[row["id"]] = row
    return out


def append_jsonl(path: Path, row: dict) -> None:
    with open(path, "a", encoding="utf-8") as fh:
        fh.write(json.dumps(row, ensure_ascii=False) + "\n")


def pct(n: int, d: int) -> str:
    return f"{n}/{d} ({n / d:.0%})" if d else "n/a"


# --------------------------------------------------------------------------- stage 1: retrieval
def hit_pairs(hit: dict) -> set[tuple[str, str]]:
    return {(hit["doc_id"], loc) for loc in hit["locations"].split("|")}


def first_rank(hits, expected):
    for rank, hit in enumerate(hits, start=1):
        if hit_pairs(hit) & expected:
            return rank
    return None


def all_rank(hits, expected):
    found = set()
    for rank, hit in enumerate(hits, start=1):
        found |= hit_pairs(hit) & expected
        if found == expected:
            return rank
    return None


def rate(ranks, k):
    return round(sum(1 for r in ranks if r is not None and r <= k) / len(ranks), 3) if ranks else 0.0


def retrieval_eval() -> dict:
    questions = [q for q in load_questions() if q["kind"] != "unanswerable"]
    rows, summary = [], {}
    for design in ix.DESIGNS:
        if ix.collection(design).count() == 0:
            continue
        any_ranks, multi_all, by_kind = [], [], {}
        for q in questions:
            expected = expected_pairs(q)
            hits = ix.search(q["question"], k=max(KS), design=design)
            r_any, r_all = first_rank(hits, expected), all_rank(hits, expected)
            any_ranks.append(r_any)
            by_kind.setdefault(q["kind"], []).append(r_any)
            if q["kind"] == "multi":
                multi_all.append(r_all)
            rows.append({"design": design, "id": q["id"], "kind": q["kind"],
                         "expected": q["expected_source"] + " | " + q["expected_location"],
                         "first_hit_rank": r_any or "", "all_found_rank": r_all or "",
                         "top5": " ; ".join(h["citation"] for h in hits)})
        summary[design] = {"questions": len(any_ranks),
                           **{f"hit@{k}": rate(any_ranks, k) for k in KS},
                           **{f"{kind}_hit@{k}": rate(r, k) for kind, r in by_kind.items() for k in KS},
                           **{f"multi_all@{k}": rate(multi_all, k) for k in KS}}
    with open(EVAL_DIR / "retrieval_results.csv", "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0]) if rows else ["design"])
        writer.writeheader()
        writer.writerows(rows)
    (EVAL_DIR / "retrieval_summary.json").write_text(json.dumps(summary, indent=2))
    print("\n== 1. Retrieval hit rate (answerable questions) ==")
    print(f"{'design':<10}" + "".join(f"{'hit@' + str(k):>9}" for k in KS)
          + "".join(f"{'multi all@' + str(k):>14}" for k in KS))
    for design, s in summary.items():
        print(f"{design:<10}" + "".join(f"{s[f'hit@{k}']:>9.0%}" for k in KS)
              + "".join(f"{s[f'multi_all@{k}']:>14.0%}" for k in KS))
    print(f"design in use: {ix.active_design()}")
    return summary


# --------------------------------------------------------------------------- stage 2: answers
def collect_answers(questions: list[dict]) -> dict:
    import agent

    if os.environ.get("FRESH") == "1" and ANSWERS_FILE.exists():
        ANSWERS_FILE.unlink()
    saved = read_jsonl(ANSWERS_FILE)
    todo = [q for q in questions if q["id"] not in saved or saved[q["id"]]["question"] != q["question"]]
    print(f"\n== 2. Agent answers: {len(questions) - len(todo)} saved, {len(todo)} to ask ==")
    deny = lambda path: False  # nobody approves add_document during the evaluation
    for start in range(0, len(todo), BATCH):
        batch = todo[start:start + BATCH]
        try:
            results = agent.ask_many([q["question"] for q in batch], approve=deny)
        except Exception as exc:  # e.g. every model overloaded: keep going, retry next run
            print(f"  batch {[q['id'] for q in batch]} failed ({str(exc)[:80]}); run again later")
            continue
        for q, r in zip(batch, results):
            row = {"id": q["id"], **r}
            append_jsonl(ANSWERS_FILE, row)
            saved[q["id"]] = row
            print(f"  {q['id']}: {r['seconds']:>5.1f}s  {r['answer'][:70].replace(chr(10), ' ')}...")
    write_grading_sheet(questions, saved)
    return saved


def retrieved_locations(answer_row: dict) -> set:
    import agent

    found = set()
    for step in answer_row.get("trace", []):
        if step["tool"] == "search":
            found |= agent.cited_locations(step["output"])
    return found


def passages_text(answer_row: dict) -> str:
    return "\n\n".join(s["output"] for s in answer_row.get("trace", []) if s["tool"] == "search") \
        or "(no passages retrieved)"


def write_grading_sheet(questions: list[dict], answers: dict) -> None:
    lines = ["# Answers to grade by hand", "",
             "For each answer fill one row in eval/human_labels.csv: id,correct,supported,notes",
             "correct = 1 if right against the reference (or a proper refusal); supported = 1 if every",
             "claim is in the retrieved passages; notes are required for every 0.", ""]
    for q in questions:
        a = answers.get(q["id"])
        if not a:
            continue
        lines += [f"## {q['id']} ({q['kind']})", f"**Question:** {q['question']}",
                  f"**Reference:** {q['reference_answer']}", "", "**Agent answer:**", "",
                  a["answer"], "", "<details><summary>Retrieved passages</summary>", "",
                  "```", passages_text(a)[:6000], "```", "</details>", ""]
    (EVAL_DIR / "to_grade.md").write_text("\n".join(lines), encoding="utf-8")


# --------------------------------------------------------------------------- stage 3: judge
def judge(q: dict, a: dict) -> dict:
    import agent
    from google import genai
    from google.genai import types
    from api_key import load_api_key

    prompt = (f"{JUDGE_RUBRIC}\n\nQUESTION:\n{q['question']}\n\nREFERENCE ANSWER:\n{q['reference_answer']}"
              f"\n\nRETRIEVED PASSAGES:\n{passages_text(a)[:20000]}\n\nASSISTANT ANSWER:\n{a['answer']}")
    client = genai.Client(api_key=load_api_key())
    last = None
    for model in agent.candidate_models():
        try:
            resp = client.models.generate_content(
                model=model, contents=prompt,
                config=types.GenerateContentConfig(response_mime_type="application/json"))
            verdict = json.loads(resp.text)
            usage = resp.usage_metadata
            return {"correct": int(verdict["correct"]), "supported": int(verdict["supported"]),
                    "reason": verdict.get("reason", ""), "judge_model": model,
                    "judge_tokens": (usage.total_token_count or 0) if usage else 0}
        except Exception as exc:
            last = exc
            if not agent.is_overloaded(exc):
                raise
    raise last


def label(q: dict, a: dict, verdicts: dict) -> dict:
    """Final labels: code decides refusals; the judge decides the rest."""
    unanswerable = q["kind"] == "unanswerable"
    refused = a["refusal"]
    expected = expected_pairs(q)
    got_passage = bool(expected & retrieved_locations(a)) if expected else None
    if refused:
        correct, supported, source, reason = (1 if unanswerable else 0), 1, "code", "refusal"
    else:
        v = verdicts[q["id"]]
        correct = 0 if unanswerable else v["correct"]
        supported, source, reason = v["supported"], "judge", v["reason"]
    if correct:
        category = ""
    elif unanswerable:
        category = "unsupported claim"  # answered a question the corpus cannot answer
    elif not got_passage:
        category = "retrieval miss"
    elif refused:
        category = "wrong refusal"
    elif not supported:
        category = "unsupported claim"
    else:
        category = "wrong answer from the right passage"
    return {"id": q["id"], "kind": q["kind"], "correct": correct, "supported": supported,
            "refusal": int(refused), "expected_retrieved": "" if got_passage is None else int(got_passage),
            "guardrail_triggered": int(a["guardrail_triggered"]), "label_source": source,
            "suggested_category": category, "reason": reason,
            "input_tokens": a["input_tokens"], "output_tokens": a["output_tokens"],
            "seconds": a["seconds"], "tool_calls": a["tool_calls"], "model": a["model"]}


# --------------------------------------------------------------------------- stage 4: report
def human_agreement(labels: dict) -> dict:
    if not HUMAN_FILE.exists():
        return {}
    with open(HUMAN_FILE, encoding="utf-8-sig") as fh:
        human = [r for r in csv.DictReader(fh) if r.get("id", "").strip() and r.get("correct", "").strip()]
    rows = [(r, labels[r["id"].strip()]) for r in human if r["id"].strip() in labels]
    if not rows:
        return {}
    out = {"graded": len(rows)}
    for field in ("correct", "supported"):
        same = sum(1 for h, l in rows if int(h[field]) == int(l[field]))
        out[f"{field}_agreement"] = round(same / len(rows), 3)
        judged = [(h, l) for h, l in rows if l["label_source"] == "judge"]
        if judged:
            out[f"{field}_agreement_judge_only"] = round(
                sum(1 for h, l in judged if int(h[field]) == int(l[field])) / len(judged), 3)
    out["disagreements"] = [h["id"] for h, l in rows
                            if int(h["correct"]) != l["correct"] or int(h["supported"]) != l["supported"]]
    return out


def full_eval() -> None:
    retrieval = retrieval_eval()
    questions = load_questions()
    answers = collect_answers(questions)

    verdicts = read_jsonl(JUDGE_FILE)
    to_judge = [q for q in questions if q["id"] in answers and not answers[q["id"]]["refusal"]
                and (q["id"] not in verdicts or verdicts[q["id"]].get("answer") != answers[q["id"]]["answer"])]
    print(f"\n== 3. LLM judge: {len(to_judge)} answer(s) to grade ==")
    for q in to_judge:
        try:
            v = {"id": q["id"], "answer": answers[q["id"]]["answer"], **judge(q, answers[q["id"]])}
        except Exception as exc:
            print(f"  {q['id']}: judge failed ({str(exc)[:80]}); run again later")
            continue
        append_jsonl(JUDGE_FILE, v)
        verdicts[q["id"]] = v
        print(f"  {q['id']}: correct={v['correct']} supported={v['supported']}  {v['reason'][:70]}")

    labels = {q["id"]: label(q, answers[q["id"]], verdicts) for q in questions
              if q["id"] in answers and (answers[q["id"]]["refusal"] or q["id"] in verdicts)}
    rows = list(labels.values())
    if not rows:
        print("No answers yet.")
        return
    with open(EVAL_DIR / "results.csv", "w", newline="", encoding="utf-8") as fh:
        writer = csv.DictWriter(fh, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)
    qtext = {q["id"]: q for q in questions}
    with open(EVAL_DIR / "failures.csv", "w", newline="", encoding="utf-8") as fh:
        writer = csv.writer(fh)
        writer.writerow(["id", "kind", "question", "suggested_category", "final_category", "reason", "answer"])
        for r in rows:
            if not r["correct"]:
                writer.writerow([r["id"], r["kind"], qtext[r["id"]]["question"], r["suggested_category"],
                                 "", r["reason"], answers[r["id"]]["answer"][:500]])

    ans = [r for r in rows if r["kind"] != "unanswerable"]
    una = [r for r in rows if r["kind"] == "unanswerable"]
    answered = [r for r in rows if not r["refusal"]]
    n = len(rows)
    summary = {
        "questions_evaluated": n,
        "answerable_correct": pct(sum(r["correct"] for r in ans), len(ans)),
        "answerable_wrong_refusal": pct(sum(r["refusal"] for r in ans), len(ans)),
        "unanswerable_correct_refusal": pct(sum(r["refusal"] for r in una), len(una)),
        "made_up_answers (unsupported or answered the unanswerable)": pct(
            sum(1 for r in answered if not r["supported"] or r["kind"] == "unanswerable"), len(answered)),
        "overall_correct": pct(sum(r["correct"] for r in rows), n),
        "guardrail_triggered": pct(sum(r["guardrail_triggered"] for r in rows), n),
        "failures_by_category": {c: sum(1 for r in rows if r["suggested_category"] == c)
                                 for c in sorted({r["suggested_category"] for r in rows} - {""})},
        "cost_per_question": {
            "input_tokens": round(sum(r["input_tokens"] for r in rows) / n),
            "output_tokens": round(sum(r["output_tokens"] for r in rows) / n),
            "seconds": round(sum(r["seconds"] for r in rows) / n, 1),
            "tool_calls": round(sum(r["tool_calls"] for r in rows) / n, 1),
        },
        "models": sorted({r["model"] for r in rows}),
        "human_vs_final_labels": human_agreement(labels),
        "retrieval": retrieval,
    }
    (EVAL_DIR / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False))
    print("\n== 4. Summary (also in eval/summary.json) ==")
    for key, value in summary.items():
        if key != "retrieval":
            print(f"  {key}: {value}")
    if not summary["human_vs_final_labels"]:
        print("  (no human grades yet: fill eval/human_labels.csv using eval/to_grade.md)")


# --------------------------------------------------------------------------- before / after
def before_after() -> None:
    import agent
    import httpx

    q = next(q for q in load_questions() if q["id"] == BEFORE_AFTER_ID)
    answers = read_jsonl(ANSWERS_FILE)
    before = answers.get(q["id"]) or agent.ask(q["question"], approve=lambda p: False)
    print(f"\nBEFORE ({q['id']}): {q['question']}\n{before['answer']}\n")

    path = ROOT / ADDED_DOC["file"]
    if not path.exists():
        path.parent.mkdir(exist_ok=True)
        with httpx.Client(follow_redirects=True, timeout=120) as client:
            for url, headers in ix._download_sources(ADDED_DOC["celex"]):
                html, note = ix._fetch(client, url, headers)
                if html and ix._looks_like_the_act(html) and ix._word_count(html) >= ADDED_DOC["min_words"]:
                    path.write_text(html, encoding="utf-8")
                    print(f"Downloaded {ADDED_DOC['title']} ({note})")
                    break
            else:
                raise SystemExit(f"Could not download {ADDED_DOC['title']}; save it as {ADDED_DOC['file']}")

    print("Asking the agent to add it (you will be asked to approve add_document):")
    added = agent.ask(f"Please add the document {ADDED_DOC['file']} to the index.")
    print(added["answer"], "\n")

    after = agent.ask(q["question"], approve=lambda p: False)
    print(f"AFTER ({q['id']}): {q['question']}\n{after['answer']}")
    (EVAL_DIR / "before_after.json").write_text(json.dumps(
        {"id": q["id"], "question": q["question"], "added_document": ADDED_DOC,
         "before": before["answer"], "add_document_trace": added["trace"],
         "after": after["answer"], "after_citations": after["citations"]}, indent=2, ensure_ascii=False))
    print("\nSaved to eval/before_after.json")


def main() -> int:
    command = sys.argv[1] if len(sys.argv) > 1 else "all"
    try:
        if command == "answers":
            retrieval_eval()
            collect_answers(load_questions())
            print("\nNow grade answers by hand: open eval/to_grade.md, fill eval/human_labels.csv")
        elif command == "before-after":
            before_after()
        else:
            full_eval()
    except ix.DailyQuotaReached:
        print("Daily embedding limit reached; everything so far is saved. Run again after 09:00 (Spain).")
    return 0


if __name__ == "__main__":
    sys.exit(main())