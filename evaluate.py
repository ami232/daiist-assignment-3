"""
Assignment 3: evaluation (`main.py evaluate`).

Stages, run in this order by default (`python evaluate.py answers judge` runs only those):

  retrieval     hit rate at k = 1, 3, 5 for every search variant      -> eval/retrieval_*.csv/json
  answers       the agent (agent.py) on every question                -> eval/answers.jsonl
  checks        what code can check: refusals and citation validity   -> eval/checks.csv
  judge         LLM judge with a rubric, retrieved text as evidence   -> eval/judge.csv
  labeling      a reading sheet to grade answers by hand              -> eval/labeling_sheet.md
  agreement     human labels (eval/human_labels.csv) vs judge         -> eval/agreement.json
  failures      each failure classified                               -> eval/failures.csv
  before_after  add the held-out document through the MCP tool and
                ask its unanswerable question again                   -> eval/before_after.md
  summary       headline numbers, cost per question                   -> eval/summary.json

Every stage saves as it goes and skips work already saved, so a crash, a 503 or the daily quota
costs nothing: run it again.
"""

from __future__ import annotations

import asyncio
import csv
import json
import re
import sys
import time
from pathlib import Path

import index

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
KS = (1, 3, 5)
ANSWERS = EVAL / "answers.jsonl"
JUDGE = EVAL / "judge.csv"
HELD_OUT_SOURCES = ("LISTA_2026",)
BEFORE_AFTER_QID = "q30"            # salbutamol: answered by the held-out Lista 2026
JUDGE_MODELS = ["gemini-3.1-flash-lite", "gemini-3.5-flash-lite"]   # a different model than the agent first


# --------------------------------------------------------------------------- helpers

def load_questions() -> list[dict]:
    with (EVAL / "questions.csv").open(encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r["question"].strip()]


def expected_passages(row: dict) -> list[tuple[str, str]]:
    sources = [s.strip() for s in row["expected_source"].split(";") if s.strip()]
    locs = [l.strip() for l in row["expected_location"].split(";") if l.strip()]
    if len(sources) == 1 and len(locs) > 1:
        sources = sources * len(locs)
    return list(zip(sources, locs))


def matches(chunk: dict, passage: tuple[str, str]) -> bool:
    source, location = passage
    return chunk["source"] == source and location in chunk["covers"].split("|")


def load_answers() -> dict[str, dict]:
    if not ANSWERS.exists():
        return {}
    out = {}
    for line in ANSWERS.read_text(encoding="utf-8").splitlines():
        if line.strip():
            r = json.loads(line)
            out[r["id"]] = r
    return out


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def retrieved_pairs(answer: dict) -> set[tuple[str, str]]:
    from agent import RETRIEVED_RE
    return {(s, l.strip()) for s, l, _ in RETRIEVED_RE.findall(answer.get("passages", ""))}


# --------------------------------------------------------------------------- retrieval

def stage_retrieval() -> dict:
    questions = [q for q in load_questions() if q["kind"] != "unanswerable"]
    summary, rows = {}, []
    for design in index.SEARCH_VARIANTS:
        hits = {k: 0 for k in KS}
        partial = {k: 0.0 for k in KS}
        for q in questions:
            results = index.search(q["question"], k=max(KS), design=design, exclude_sources=HELD_OUT_SOURCES)
            passages = expected_passages(q)
            first_rank = next((rank for rank, c in enumerate(results, 1)
                               if any(matches(c, p) for p in passages)), None)
            row = {"design": design, "id": q["id"], "kind": q["kind"], "first_rank": first_rank or ""}
            for k in KS:
                found = [any(matches(c, p) for c in results[:k]) for p in passages]
                row[f"hit@{k}"] = int(all(found))
                row[f"partial@{k}"] = round(sum(found) / len(found), 2)
                hits[k] += int(all(found))
                partial[k] += sum(found) / len(found)
            row["top5"] = " ; ".join(f"{c['source']}:{c['location']}" for c in results)
            rows.append(row)
        n = len(questions)
        s = {"questions": n}
        s.update({f"hit@{k}": round(hits[k] / n, 3) for k in KS})
        s.update({f"partial@{k}": round(partial[k] / n, 3) for k in KS})
        for kind in ("single", "multi"):
            kn = sum(1 for q in questions if q["kind"] == kind)
            for k in KS:
                s[f"hit@{k}_{kind}"] = round(sum(r[f"hit@{k}"] for r in rows
                                                 if r["design"] == design and r["kind"] == kind) / kn, 3)
        summary[design] = s
    write_csv(EVAL / "retrieval_results.csv", rows)
    (EVAL / "retrieval_summary.json").write_text(json.dumps(summary, indent=2))
    print(f"{'design':17s} " + " ".join(f"hit@{k:<3d}" for k in KS) + "  (single / multi @5)")
    for d, s in summary.items():
        print(f"{d:17s} " + " ".join(f"{s[f'hit@{k}']:<7.2f}" for k in KS)
              + f"  {s['hit@5_single']:.2f} / {s['hit@5_multi']:.2f}")
    return summary


# --------------------------------------------------------------------------- answers

def stage_answers() -> None:
    from agent import ask
    done = load_answers()
    questions = load_questions()
    todo = [q for q in questions if q["id"] not in done]
    print(f"{len(done)} answers saved, {len(todo)} to go")
    for q in todo:
        try:
            r = ask(q["question"], interactive=False)
        except Exception as error:  # noqa: BLE001 - keep going, rerun picks it up
            root = error
            while isinstance(root, BaseExceptionGroup) and root.exceptions:
                root = root.exceptions[0]
            msg = str(root)
            quota_id = re.search(r"quotaId['\"]?:\s*['\"]([^'\"]+)", msg)
            print(f"  {q['id']}: FAILED ({type(root).__name__}: {msg[:200]}"
                  f"{' | ' + quota_id.group(1) if quota_id else ''}); rerun later")
            if "PerDay" in msg or "Daily" in msg:
                print("  Daily quota reached: stopping. Run the same command again after 09:00.")
                return
            if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
                print("  Per-minute limit: waiting 60 s ...")
                time.sleep(60)
            continue
        r["id"] = q["id"]
        with ANSWERS.open("a", encoding="utf-8") as f:
            f.write(json.dumps(r, ensure_ascii=False) + "\n")
        print(f"  {q['id']} {q['kind']:12s} {'REFUSED' if r['refused'] else 'answered'} "
              f"{len(r['valid_citations'])} valid / {len(r['invalid_citations'])} invalid citations, "
              f"{r['seconds']}s")


# --------------------------------------------------------------------------- code checks

def stage_checks() -> list[dict]:
    answers = load_answers()
    rows = []
    for q in load_questions():
        a = answers.get(q["id"])
        if not a:
            continue
        expected = expected_passages(q)
        got = retrieved_pairs(a)
        from agent import check_citations
        valid, invalid = check_citations(a["answer"], got)     # recomputed with the current parser
        a["valid_citations"], a["invalid_citations"] = valid, invalid
        cited = {tuple(c.split(", ", 1)) for c in valid}
        should_refuse = q["kind"] == "unanswerable"
        rows.append({
            "id": q["id"], "kind": q["kind"],
            "refused": int(a["refused"]),
            "refusal_ok": int(a["refused"] == should_refuse),
            "n_valid_citations": len(a["valid_citations"]),
            "n_invalid_citations": len(a["invalid_citations"]),
            "citations_ok": int(a["refused"] or (a["valid_citations"] and not a["invalid_citations"])),
            "expected_retrieved": "" if should_refuse else int(all(p in got for p in expected)),
            "expected_cited": "" if should_refuse else int(all(p in cited for p in expected)),
            "guardrail": a.get("guardrail") or "",
        })
    write_csv(EVAL / "checks.csv", rows)
    n = len(rows)
    if n:
        print(f"refusal correct: {sum(r['refusal_ok'] for r in rows)}/{n}   "
              f"citations ok: {sum(r['citations_ok'] for r in rows)}/{n}   "
              f"guardrail fired: {sum(1 for r in rows if r['guardrail'])}")
    return rows


# --------------------------------------------------------------------------- LLM judge

JUDGE_PROMPT = """You are grading an anti-doping legal assistant for athletes in Spain. Be strict.

Question: {question}
Question type: {kind}  (unanswerable = the corpus does not contain the answer)
Reference answer: {reference}

Retrieved passages the assistant saw (the ONLY allowed evidence):
<<<
{passages}
>>>

Assistant's answer:
<<<
{answer}
>>>

Rubric
- correct = 1 if the answer agrees with the reference on the key facts (numbers, periods, who decides,
  conditions) and does not contradict it; extra correct detail is fine; a missing key condition that
  changes the practical advice makes it 0. For an unanswerable question, correct = 1 only if the
  assistant says the corpus does not cover it and does not guess. A refusal to an answerable
  question is correct = 0.
- supported = 1 if every factual claim in the answer is stated in the retrieved passages (a refusal
  that makes no claims is supported = 1). Any claim not found in the passages makes it 0.
- failure: if correct = 0 or supported = 0, choose one of: retrieval_miss (the needed passage is not
  in the retrieved text), wrong_from_right_passage (the passage is there but the answer misreads it),
  unsupported_claim (adds facts not in the passages), wrong_refusal (refuses although the passages
  answer it), bad_test_question (the reference itself is wrong or ambiguous). Otherwise "none".

Reply with JSON only: {{"correct": 0 or 1, "supported": 0 or 1, "failure": "...", "reason": "one sentence"}}"""


def _judge_call(prompt: str) -> dict:
    from google.genai import types
    last = None
    for model in JUDGE_MODELS:
        for attempt in range(3):
            try:
                res = index.gemini().models.generate_content(
                    model=model, contents=prompt,
                    config=types.GenerateContentConfig(temperature=0, response_mime_type="application/json"))
                data = json.loads(re.search(r"\{.*\}", res.text, re.S).group(0))
                usage = res.usage_metadata
                data["judge_tokens"] = (usage.prompt_token_count or 0) + (usage.candidates_token_count or 0)
                data["judge_model"] = model
                return data
            except Exception as error:  # noqa: BLE001
                last = error
                if "503" in str(error) or "429" in str(error) or "UNAVAILABLE" in str(error):
                    time.sleep(10 * (attempt + 1))
                    continue
                break
    raise RuntimeError(f"judge failed: {last}")


def stage_judge() -> list[dict]:
    answers = load_answers()
    rows = read_csv(JUDGE)
    done = {r["id"] for r in rows}
    for q in load_questions():
        a = answers.get(q["id"])
        if not a or q["id"] in done:
            continue
        prompt = JUDGE_PROMPT.format(question=q["question"], kind=q["kind"], reference=q["reference_answer"],
                                     passages=a.get("passages") or "(no passages retrieved)", answer=a["answer"])
        try:
            v = _judge_call(prompt)
        except Exception as error:  # noqa: BLE001
            print(f"  {q['id']}: judge failed ({str(error)[:120]}); rerun later")
            continue
        rows.append({"id": q["id"], "kind": q["kind"], "correct": int(v["correct"]),
                     "supported": int(v["supported"]), "failure": v.get("failure", ""),
                     "reason": v.get("reason", ""), "judge_model": v["judge_model"],
                     "judge_tokens": v["judge_tokens"]})
        write_csv(JUDGE, rows)
        print(f"  {q['id']} correct={v['correct']} supported={v['supported']} {v.get('failure', '')}")
    return rows


# --------------------------------------------------------------------------- human labels

def stage_labeling() -> None:
    """A sheet to read while grading by hand. It deliberately shows no judge verdicts."""
    answers = load_answers()
    out = ["# Labeling sheet (grade BEFORE reading eval/judge.csv)\n",
           "Write your grades in eval/human_labels.csv: id,correct,supported,notes\n"]
    for q in load_questions():
        a = answers.get(q["id"])
        if not a:
            continue
        out += [f"\n---\n\n## {q['id']} ({q['kind']})\n", f"**Question:** {q['question']}\n",
                f"**Reference:** {q['reference_answer']}\n", f"**Answer:**\n\n{a['answer']}\n",
                "<details><summary>Retrieved passages</summary>\n\n```\n"
                + (a.get("passages") or "(none)") + "\n```\n</details>\n"]
    (EVAL / "labeling_sheet.md").write_text("\n".join(out), encoding="utf-8")
    print("wrote eval/labeling_sheet.md")


def stage_agreement() -> dict:
    human = {r["id"]: r for r in read_csv(EVAL / "human_labels.csv") if r.get("id", "").strip()}
    judge = {r["id"]: r for r in read_csv(JUDGE)}
    both = sorted(set(human) & set(judge))
    result = {"n": len(both)}
    for field in ("correct", "supported"):
        pairs = [(int(human[i][field]), int(judge[i][field])) for i in both
                 if str(human[i].get(field, "")).strip() in {"0", "1"}]
        if not pairs:
            continue
        agree = sum(h == j for h, j in pairs) / len(pairs)
        ph = sum(h for h, _ in pairs) / len(pairs)
        pj = sum(j for _, j in pairs) / len(pairs)
        pe = ph * pj + (1 - ph) * (1 - pj)
        kappa = (agree - pe) / (1 - pe) if pe < 1 else 1.0
        result[field] = {"agreement": round(agree, 3), "cohen_kappa": round(kappa, 3), "n": len(pairs),
                         "disagreements": [i for i in both if str(human[i][field]).strip() in {"0", "1"}
                                           and int(human[i][field]) != int(judge[i][field])]}
    (EVAL / "agreement.json").write_text(json.dumps(result, indent=2))
    print(json.dumps(result))
    return result


# --------------------------------------------------------------------------- failures

def stage_failures() -> list[dict]:
    """One row per failed answer. Uses the human label when there is one, else the judge.

    The category comes from code where code can decide (retrieval miss, wrong refusal, answering
    an unanswerable question), and from the judge's category otherwise."""
    questions = {q["id"]: q for q in load_questions()}
    answers = load_answers()
    checks = {r["id"]: r for r in read_csv(EVAL / "checks.csv")}
    judge = {r["id"]: r for r in read_csv(JUDGE)}
    human = {r["id"]: r for r in read_csv(EVAL / "human_labels.csv") if r.get("id", "").strip()}
    rows = []
    for qid, q in questions.items():
        if qid not in judge or qid not in answers:
            continue
        grader = human.get(qid) or judge[qid]
        correct, supported = int(grader["correct"]), int(grader["supported"])
        flagged_bad = "bad_test_question" in (human.get(qid) or {}).get("notes", "")
        if correct and supported and not flagged_bad:
            continue
        c = checks.get(qid, {})
        refused = answers[qid]["refused"]
        retrieved = str(c.get("expected_retrieved")) != "0"
        if q["kind"] == "unanswerable" and not refused:
            category = "unsupported_claim"            # answered what the corpus cannot answer
        elif q["kind"] != "unanswerable" and refused:
            category = "wrong_refusal" if retrieved else "retrieval_miss"
        elif not correct and not retrieved:
            category = "retrieval_miss"               # the needed passage never reached the model
        elif not correct:
            category = "wrong_from_right_passage"     # passage was there, the answer got it wrong
        else:
            category = "unsupported_claim"            # right answer, plus a claim not in the passages
        if flagged_bad or (judge[qid].get("failure") == "bad_test_question" and qid not in human):
            category = "bad_test_question"            # the reference, not the agent, was wrong
        rows.append({"id": qid, "kind": q["kind"], "graded_by": "human" if qid in human else "judge",
                     "correct": correct, "supported": supported, "category": category,
                     "note": (human.get(qid) or {}).get("notes") or judge[qid].get("reason", "")})
    write_csv(EVAL / "failures.csv", rows) if rows else (EVAL / "failures.csv").write_text(
        "id,kind,graded_by,correct,supported,category,note\n")
    from collections import Counter
    print(dict(Counter(r["category"] for r in rows)))
    return rows


# --------------------------------------------------------------------------- before / after

async def _add_via_mcp(path: str) -> str:
    """Call the server's add_document tool, as a client would. Running this stage is the approval."""
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client
    params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT))
    async with stdio_client(params) as (read, write):
        async with ClientSession(read, write) as session:
            await session.initialize()
            result = await session.call_tool("add_document", {"path": path})
            return "\n".join(getattr(c, "text", "") for c in result.content)


def stage_before_after() -> None:
    from agent import ask
    from corpus_sources import HELD_OUT, download
    out_file = EVAL / "before_after.json"
    missing = [q["id"] for q in load_questions() if q["id"] not in load_answers()]
    if missing and not out_file.exists():
        print(f"Skipped: answer every question first (missing {missing}); adding the document "
              f"changes the index the main evaluation must run on.")
        return
    state = json.loads(out_file.read_text()) if out_file.exists() else {}
    q = next(q for q in load_questions() if q["id"] == BEFORE_AFTER_QID)
    if "before" not in state:
        before = load_answers().get(BEFORE_AFTER_QID) or ask(q["question"])
        state["before"] = {k: before[k] for k in ("answer", "refused", "valid_citations")}
        out_file.write_text(json.dumps(state, indent=2, ensure_ascii=False))
    if "add_report" not in state:
        meta = HELD_OUT["LISTA_2026"]
        path = download("LISTA_2026", meta["boe_id"])
        state["add_report"] = asyncio.run(_add_via_mcp(str(path.relative_to(ROOT))))
        state["add_again_report"] = asyncio.run(_add_via_mcp(str(path.relative_to(ROOT))))  # idempotency
        out_file.write_text(json.dumps(state, indent=2, ensure_ascii=False))
    if "after" not in state:
        after = ask(q["question"])
        state["after"] = {k: after[k] for k in ("answer", "refused", "valid_citations")}
        out_file.write_text(json.dumps(state, indent=2, ensure_ascii=False))
    md = [f"# Before / after adding the Lista 2026\n", f"**Question ({q['id']}):** {q['question']}\n",
          f"## Before\n\n{state['before']['answer']}\n",
          f"## add_document report\n\n```\n{state['add_report']}\n```\n",
          f"Adding the same file again:\n\n```\n{state['add_again_report']}\n```\n",
          f"## After\n\n{state['after']['answer']}\n"]
    (EVAL / "before_after.md").write_text("\n".join(md), encoding="utf-8")
    print("\n".join(md))


# --------------------------------------------------------------------------- summary

def stage_summary() -> dict:
    questions = load_questions()
    answers = load_answers()
    judge_only = {r["id"]: r for r in read_csv(JUDGE)}
    human = {r["id"]: r for r in read_csv(EVAL / "human_labels.csv") if r.get("id", "").strip()}
    # final grade: the human label where there is one, else the judge's
    judge = {i: {**r, **{k: human[i][k] for k in ("correct", "supported")}} if i in human else r
             for i, r in judge_only.items()}
    checks = {r["id"]: r for r in read_csv(EVAL / "checks.csv")}
    ids = [q["id"] for q in questions if q["id"] in answers and q["id"] in judge]
    kind = {q["id"]: q["kind"] for q in questions}
    ans = [i for i in ids if kind[i] != "unanswerable"]
    una = [i for i in ids if kind[i] == "unanswerable"]
    rate = lambda xs, n: round(len(xs) / n, 3) if n else None  # noqa: E731
    s = {
        "grades": f"human label for {sum(1 for i in ids if i in human)} questions, LLM judge for the rest",
        "answered_questions": len(ids),
        "judge_only_correct": rate([i for i in ids if judge_only[i]["correct"] == "1"], len(ids)),
        "judge_only_supported": rate([i for i in ids if judge_only[i]["supported"] == "1"], len(ids)),
        "supported_overall": rate([i for i in ids if judge[i]["supported"] == "1"], len(ids)),
        "correct_overall": rate([i for i in ids if judge[i]["correct"] == "1"], len(ids)),
        "answerable": {
            "n": len(ans),
            "correct": rate([i for i in ans if judge[i]["correct"] == "1"], len(ans)),
            "wrong_refusal": rate([i for i in ans if answers[i]["refused"]], len(ans)),
            "made_up_or_unsupported": rate([i for i in ans if not answers[i]["refused"]
                                            and judge[i]["supported"] == "0"], len(ans)),
        },
        "unanswerable": {
            "n": len(una),
            "rightly_refused": rate([i for i in una if answers[i]["refused"]], len(una)),
            "made_up": rate([i for i in una if not answers[i]["refused"]], len(una)),
        },
        "citations_ok": rate([i for i in ids if checks.get(i, {}).get("citations_ok") == "1"], len(ids)),
        "guardrail_fired": sum(1 for i in ids if answers[i].get("guardrail")),
        "cost_per_question": {
            "agent_tokens_in": round(sum(answers[i]["tokens_in"] for i in ids) / max(1, len(ids))),
            "agent_tokens_out": round(sum(answers[i]["tokens_out"] for i in ids) / max(1, len(ids))),
            "judge_tokens": round(sum(int(judge[i]["judge_tokens"]) for i in ids) / max(1, len(ids))),
            "seconds_mean": round(sum(answers[i]["seconds"] for i in ids) / max(1, len(ids)), 1),
            "seconds_median": sorted(answers[i]["seconds"] for i in ids)[len(ids) // 2] if ids else None,
            "searches_mean": round(sum(answers[i]["searches"] for i in ids) / max(1, len(ids)), 2),
        },
    }
    (EVAL / "summary.json").write_text(json.dumps(s, indent=2))
    print(json.dumps(s, indent=2))
    return s


STAGES = {
    "retrieval": stage_retrieval, "answers": stage_answers, "checks": stage_checks,
    "judge": stage_judge, "labeling": stage_labeling, "agreement": stage_agreement,
    "failures": stage_failures, "before_after": stage_before_after, "summary": stage_summary,
}

if __name__ == "__main__":
    wanted = sys.argv[1:] or list(STAGES)
    for name in wanted:
        print(f"\n=== {name} ===", flush=True)
        STAGES[name]()
