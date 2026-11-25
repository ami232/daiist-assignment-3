"""
Assignment 3: evaluation (`main.py evaluate`). May be evaluate.ipynb instead.

Part 1: retrieval hit rate at k = 1, 3, 5 for each chunking design (query vectors are cached).
Part 2: end to end. The agent answers every question (saved after each one, so a stop or a crash loses
nothing), code checks what code can check (refusals, valid citations, expected sections), an LLM judge
grades the rest with a rubric, and the verdicts are compared with your human labels.

    uv run python evaluate.py answers         # only run the agent and write the sheet to grade by hand
    uv run python evaluate.py answers fresh   # same, but forget saved answers and verdicts first
    uv run python main.py evaluate            # everything; saved answers and verdicts are reused
"""

import csv
import hashlib
import json
import re
import statistics
import sys
import time
import warnings
from collections import Counter
from pathlib import Path

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)

from langchain_google_genai import ChatGoogleGenerativeAI  # noqa: E402

import agent  # noqa: E402
import index  # noqa: E402
from api_key import load_api_key  # noqa: E402

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
CACHE = EVAL / "query_vectors.json"
DETAILS = EVAL / "retrieval_details.csv"
SUMMARY = EVAL / "retrieval_summary.json"
ANSWERS = EVAL / "agent_answers.jsonl"
VERDICTS = EVAL / "judge_verdicts.jsonl"
RESULTS = EVAL / "end_to_end_results.csv"
E2E_SUMMARY = EVAL / "end_to_end_summary.json"
SHEET = EVAL / "answers_for_grading.md"
HUMAN = EVAL / "human_labels.csv"
KS = (1, 3, 5)

BLOCK_SPLIT = re.compile(r"\n\n(?=\[\d+\] source: )")


# ======================= Part 1: retrieval =======================

def load_questions():
    with open(QUESTIONS, newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def query_vectors(texts):
    """Embed each question once and remember the vector on disk, so re-running costs nothing."""
    cache = json.loads(CACHE.read_text()) if CACHE.exists() else {}
    missing = [t for t in texts if t not in cache]
    for start in range(0, len(missing), 20):
        batch = missing[start:start + 20]
        for text, vector in zip(batch, index.embed_texts(batch)):
            cache[text] = vector
        CACHE.write_text(json.dumps(cache))
    return [cache[t] for t in texts]


def search(collection, vector, k=5):
    """The k chunks closest to the question vector, best first."""
    found = collection.query(query_embeddings=[vector], n_results=k)
    return [{"location": m["location"], "words": m["words"]} for m in found["metadatas"][0]]


def is_hit(results, expected_locations, k):
    """A hit = every expected location appears in the top k (for 'multi' questions that means both)."""
    got = {r["location"] for r in results[:k]}
    return all(loc in got for loc in expected_locations)


def retrieval_eval():
    rows = [r for r in load_questions() if r["kind"] != "unanswerable"]
    vectors = query_vectors([r["question"] for r in rows])
    details, summary = [], {}

    for design in index.DESIGNS:
        collection = index.get_collection(design)
        hits = {kind: {k: 0 for k in KS} for kind in ("single", "multi")}
        total = {"single": 0, "multi": 0}
        words = {k: 0 for k in KS}

        for row, vector in zip(rows, vectors):
            results = search(collection, vector, max(KS))
            expected = row["expected_location"].split(";")
            total[row["kind"]] += 1
            line = {"design": design, "id": row["id"], "kind": row["kind"],
                    "expected": row["expected_location"],
                    "top5": " | ".join(r["location"] for r in results)}
            for k in KS:
                ok = is_hit(results, expected, k)
                hits[row["kind"]][k] += ok
                words[k] += sum(r["words"] for r in results[:k])
                line[f"hit@{k}"] = int(ok)
            details.append(line)

        n = sum(total.values())
        summary[design] = {
            "questions": n,
            "hit_rate": {k: {"single": hits["single"][k] / total["single"],
                             "multi": hits["multi"][k] / total["multi"],
                             "all": (hits["single"][k] + hits["multi"][k]) / n} for k in KS},
            "avg_words_in_prompt": {k: round(words[k] / n) for k in KS},
        }

        print(f"\nDesign {design}: {n} answerable questions ({total['single']} single, {total['multi']} multi)")
        print("  k   single   multi     all   avg words added to prompt")
        for k in KS:
            h = summary[design]["hit_rate"][k]
            print(f"  {k}   {h['single']:6.0%}  {h['multi']:6.0%}  {h['all']:6.0%}   {summary[design]['avg_words_in_prompt'][k]}")

    with open(DETAILS, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(details[0]))
        writer.writeheader()
        writer.writerows(details)
    SUMMARY.write_text(json.dumps(summary, indent=2))

    print("\nQuestions missed at k=5:")
    for d in details:
        if not d["hit@5"]:
            print(f"  Design {d['design']} {d['id']}: wanted {d['expected']} | got {d['top5']}")


# ======================= Part 2: end to end =======================

def read_jsonl(path):
    rows = {}
    if path.exists():
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                row = json.loads(line)
                rows[row["id"]] = row   # a later line replaces an earlier one
    return rows


def append_jsonl(path, row):
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def run_agent_on_questions(questions):
    """The agent answers every question that has no saved answer yet. add_document is always refused here."""
    answers = read_jsonl(ANSWERS)
    todo = [q for q in questions if q["id"] not in answers]
    print(f"\nAgent answers: {len(answers)} saved, {len(todo)} to run", flush=True)
    failures = 0
    for number, q in enumerate(todo, 1):
        try:
            out = agent.answer_question(q["question"], approve=lambda path: False)
        except Exception as error:  # noqa: BLE001
            failures += 1
            print(f"  {q['id']} FAILED ({type(error).__name__}: {str(error)[:120]})", flush=True)
            if failures >= 2:
                print("Two failures in a row: stopping. Run the same command later to continue; nothing is lost.")
                break
            continue
        failures = 0
        row = {"id": q["id"], "question": q["question"], "kind": q["kind"],
               "answer": out["answer"], "draft_answer": out["draft_answer"],
               "guardrail": out["guardrail"], "guardrail_kind": out["guardrail_kind"],
               "model": out["model"], "tool_calls": out["tool_calls"], "passages": out["passages"],
               "search_results": [s["result"] for s in out["trace"] if s["tool"] == "search"],
               "input_tokens": out["input_tokens"], "output_tokens": out["output_tokens"], "seconds": out["seconds"]}
        append_jsonl(ANSWERS, row)
        state = "refused " if agent.is_refusal(out["answer"]) else "answered"
        print(f"  {q['id']} {q['kind']:<12} {state} | {out['seconds']:>6} s | {out['model']} | {number}/{len(todo)}", flush=True)
    return read_jsonl(ANSWERS)


# ---------- code checks ----------

def code_checks(q, a):
    answer = a["answer"]
    refused = agent.is_refusal(answer)
    retrieved = {agent.norm(p["location"]) for p in a["passages"]}
    cited = {agent.norm(c[1]) for c in agent.CITATION.findall(answer)}
    expected = [agent.norm(x) for x in q["expected_location"].split(";") if x.strip()]
    draft = a["draft_answer"]
    draft_ok = True if agent.is_refusal(draft) else agent.check_citations(draft, a["passages"])[0]
    return {
        "refused": refused,
        "citations_valid": True if refused else agent.check_citations(answer, a["passages"])[0],
        "draft_citations_valid": draft_ok,
        "expected_retrieved": all(e in retrieved for e in expected) if expected else None,
        "expected_cited": (all(e in cited for e in expected) if (expected and not refused) else None),
    }


# ---------- LLM judge ----------

JUDGE_MODELS = ["gemini-3.8-flash", "gemini-3.7-flash", "gemini-3.5-flash", "gemini-3.6-flash", "gemini-3.5-flash-lite"]
JUDGE_COOLDOWN = {}


def ask_model(prompt):
    """One judge call, falling back to other models when one is busy, retired or too slow."""
    load_api_key()
    last = ""
    for _round in range(3):
        now = time.time()
        order = [m for m in JUDGE_MODELS if JUDGE_COOLDOWN.get(m, 0) <= now] or JUDGE_MODELS
        for name in order:
            try:
                reply = ChatGoogleGenerativeAI(model=name, temperature=0, max_retries=0, timeout=40).invoke(prompt)
                return name, agent.text_of(reply)
            except Exception as error:  # noqa: BLE001
                text = f"{type(error).__name__}: {error}"
                last = text[:120]
                if any(code in text for code in agent.TRY_NEXT):
                    JUDGE_COOLDOWN[name] = time.time() + agent.COOLDOWN_SECONDS
                    continue
                raise
        time.sleep(10)
    raise RuntimeError("no judge model available: " + last)


def parse_verdict(text):
    match = re.search(r"\{.*\}", text, re.S)
    if not match:
        return None
    try:
        data = json.loads(match.group(0))
        return {"correct": int(data["correct"]), "supported": int(data["supported"]),
                "reason": str(data.get("reason", ""))[:200]}
    except Exception:  # noqa: BLE001
        return None


def judge_answer(q, a):
    context = "\n\n".join(a["search_results"])[:14000] or "(no passages were retrieved)"
    prompt = f"""You are a strict grader of answers from a food-safety assistant that must answer only from retrieved passages.

QUESTION:
{q['question']}

REFERENCE ANSWER (what a correct answer says):
{q['reference_answer']}

ASSISTANT'S ANSWER:
{a['answer']}

RETRIEVED PASSAGES (the only evidence the assistant had):
{context}

Grade two things, each 1 or 0:
- correct: 1 only if the answer gives the same facts as the reference answer: every key number, unit and condition matches (extra correct detail is fine). 0 if a key number or fact is wrong or missing, or the answer is about something else.
- supported: 1 only if every factual claim in the answer is stated in the retrieved passages. 0 if any claim goes beyond them, for example a rule for one category applied to another, or facts that come from general knowledge.

Reply with JSON only, no other text: {{"correct": 0 or 1, "supported": 0 or 1, "reason": "one short sentence"}}"""
    for _try in range(2):
        model, text = ask_model(prompt)
        verdict = parse_verdict(text)
        if verdict:
            verdict["judge_model"] = model
            return verdict
    return {"correct": 0, "supported": 0, "reason": "the judge reply could not be parsed", "judge_model": "none"}


def judge_all(questions, answers):
    """Judge every answer that is not a refusal (code decides refusals). Verdicts are saved and reused."""
    verdicts = read_jsonl(VERDICTS)
    for q in questions:
        a = answers.get(q["id"])
        if not a or agent.is_refusal(a["answer"]):
            continue
        digest = hashlib.sha1(a["answer"].encode()).hexdigest()[:10]
        if q["id"] in verdicts and verdicts[q["id"]].get("digest") == digest:
            continue
        try:
            verdict = judge_answer(q, a)
        except Exception as error:  # noqa: BLE001
            print(f"  judge stopped at {q['id']} ({str(error)[:100]}); run again later to finish", flush=True)
            break
        verdict.update(id=q["id"], digest=digest)
        append_jsonl(VERDICTS, verdict)
        verdicts[q["id"]] = verdict
        print(f"  judged {q['id']}: correct={verdict['correct']} supported={verdict['supported']} ({verdict['judge_model']})", flush=True)
    return verdicts


def final_verdict(q, a, checks, judged):
    """Code decides for refusals; the judge decides for the rest."""
    if checks["refused"]:
        return {"correct": int(q["kind"] == "unanswerable"), "supported": 1, "by": "code"}
    correct = 0 if q["kind"] == "unanswerable" else judged["correct"]
    return {"correct": correct, "supported": judged["supported"], "by": "judge"}


def suggest_cause(q, checks, final):
    """A first guess at the failure class. Whether the question itself is bad is your call."""
    if q["kind"] == "unanswerable":
        return "" if final["correct"] else "unsupported claim (answered an unanswerable question)"
    if final["correct"] and final["supported"]:
        return ""
    if checks["refused"]:
        return "wrong refusal" if checks["expected_retrieved"] else "retrieval miss (refused)"
    if not checks["expected_retrieved"]:
        return "retrieval miss"
    if not final["supported"]:
        return "unsupported claim"
    return "wrong answer from the right passage"


# ---------- sheet for grading by hand ----------

def write_sheet(questions, answers):
    lines = ["# Answers to grade by hand",
             "",
             "Fill eval/human_labels.csv: for each answer give correct = 1 or 0 and supported = 1 or 0, and say why in notes for every 0.",
             "- correct: same key facts as the reference answer (for unanswerable questions: a proper refusal).",
             "- supported: every claim in the answer is stated in the passages shown.",
             ""]
    for q in questions:
        a = answers.get(q["id"])
        if not a:
            continue
        blocks = [b for s in a["search_results"] for b in BLOCK_SPLIT.split(s)]
        cited = {(agent.norm(c[0]), agent.norm(c[1])) for c in agent.CITATION.findall(a["answer"])}
        shown = []
        for b in blocks:
            m = agent.HEADER.match(b)
            if m and (agent.norm(m.group(1)), agent.norm(m.group(2))) in cited:
                shown.append(b[:1500])
        if not shown:
            shown = [b[:500] for b in blocks[:2]]
        lines += [f"## {q['id']} ({q['kind']})",
                  f"**Question:** {q['question']}",
                  f"**Reference answer:** {q['reference_answer']}",
                  f"**Agent answer:** {a['answer']}",
                  "",
                  "Passages (the cited ones, or the top 2 retrieved if nothing is cited):",
                  ""]
        lines += [f"> {b}" for b in shown]
        lines.append("")
    SHEET.write_text("\n".join(lines), encoding="utf-8")


def prefill_human_labels(questions):
    """Create the empty rows to fill. Never overwrites a file you have already started to fill in."""
    if HUMAN.exists():
        with open(HUMAN, newline="", encoding="utf-8") as f:
            rows = list(csv.DictReader(f))
        if any((r.get("correct") or "").strip() or (r.get("supported") or "").strip() for r in rows):
            return
    with open(HUMAN, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "correct", "supported", "notes"])
        for q in questions:
            writer.writerow([q["id"], "", "", ""])


def read_human():
    rows = {}
    if HUMAN.exists():
        with open(HUMAN, newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                c, s = (r.get("correct") or "").strip(), (r.get("supported") or "").strip()
                if c in ("0", "1") and s in ("0", "1"):
                    rows[r["id"].strip()] = {"correct": int(c), "supported": int(s), "notes": r.get("notes") or ""}
    return rows


# ---------- the report ----------

def end_to_end_report(questions, answers, verdicts):
    rows, not_judged = [], []
    for q in questions:
        a = answers.get(q["id"])
        if not a:
            continue
        checks = code_checks(q, a)
        if not checks["refused"] and q["id"] not in verdicts:
            not_judged.append(q["id"])
            continue
        final = final_verdict(q, a, checks, verdicts.get(q["id"]) or {})
        rows.append({"q": q, "a": a, "checks": checks, "final": final, "cause": suggest_cause(q, checks, final)})

    print("\n" + "=" * 70)
    print(f"END-TO-END: {len(rows)} questions graded, {len(questions) - len(answers)} without an answer yet, {len(not_judged)} not judged yet")
    print("Final verdict: code decides refusals, the LLM judge decides the rest")
    print("  kind          n  refused  correct  supported  valid citations")
    for kind in ("single", "multi", "unanswerable"):
        sel = [r for r in rows if r["q"]["kind"] == kind]
        if sel:
            print(f"  {kind:<12} {len(sel):>3}  {sum(r['checks']['refused'] for r in sel):>7}  "
                  f"{sum(r['final']['correct'] for r in sel):>7}  {sum(r['final']['supported'] for r in sel):>9}  "
                  f"{sum(r['checks']['citations_valid'] for r in sel):>15}")

    ans = [r for r in rows if r["q"]["kind"] != "unanswerable"]
    unans = [r for r in rows if r["q"]["kind"] == "unanswerable"]
    counts = {
        "answerable": len(ans),
        "correct_and_supported": sum(1 for r in ans if r["final"]["correct"] and r["final"]["supported"]),
        "wrong_refusals": sum(1 for r in ans if r["checks"]["refused"]),
        "unsupported_claims": sum(1 for r in ans if not r["checks"]["refused"] and not r["final"]["supported"]),
        "wrong_answers": sum(1 for r in ans if not r["checks"]["refused"] and r["final"]["supported"] and not r["final"]["correct"]),
        "unanswerable": len(unans),
        "correct_refusals": sum(1 for r in unans if r["checks"]["refused"]),
        "made_up_answers": sum(1 for r in unans if not r["checks"]["refused"]),
    }
    print(f"\n  answerable: {counts['answerable']} -> correct and supported {counts['correct_and_supported']}, "
          f"wrong refusals {counts['wrong_refusals']}, answered with unsupported claims {counts['unsupported_claims']}, "
          f"answered wrong {counts['wrong_answers']}")
    print(f"  unanswerable: {counts['unanswerable']} -> correct refusals {counts['correct_refusals']}, made-up answers {counts['made_up_answers']}")

    fired = Counter(a["guardrail_kind"] for a in answers.values() if a.get("guardrail_kind"))
    bad_drafts = sum(1 for r in rows if not r["checks"]["draft_citations_valid"])
    print(f"  guardrails fired: citation check {fired.get('citation', 0)}, refusal trim {fired.get('refusal_trim', 0)}; "
          f"drafts with an invalid citation: {bad_drafts}")

    seconds = [a["seconds"] for a in answers.values()]
    tin = [a["input_tokens"] for a in answers.values()]
    tout = [a["output_tokens"] for a in answers.values()]
    cost = {}
    if seconds:
        cost = {"avg_input_tokens": round(statistics.mean(tin)), "avg_output_tokens": round(statistics.mean(tout)),
                "median_seconds": round(statistics.median(seconds), 1), "mean_seconds": round(statistics.mean(seconds), 1),
                "max_seconds": max(seconds), "models": dict(Counter(a["model"] for a in answers.values()))}
        print(f"\n  cost per question: {cost['avg_input_tokens']} input + {cost['avg_output_tokens']} output tokens, "
              f"median {cost['median_seconds']} s (mean {cost['mean_seconds']}, max {cost['max_seconds']}); models used: {cost['models']}")

    print("\nFAILURES (suggested cause; whether a question itself is bad is for you to decide)")
    for r in rows:
        if r["cause"]:
            print(f"  {r['q']['id']} [{r['q']['kind']}] {r['cause']} | {r['a']['answer'][:100].replace(chr(10), ' ')}")

    human = read_human()
    agreement = {}
    shared = [r for r in rows if r["q"]["id"] in human]
    if shared:
        c = sum(1 for r in shared if human[r["q"]["id"]]["correct"] == r["final"]["correct"])
        s = sum(1 for r in shared if human[r["q"]["id"]]["supported"] == r["final"]["supported"])
        both = sum(1 for r in shared if human[r["q"]["id"]]["correct"] == r["final"]["correct"]
                   and human[r["q"]["id"]]["supported"] == r["final"]["supported"])
        n = len(shared)
        agreement = {"answers_compared": n, "correct_agree": c, "supported_agree": s, "both_agree": both}
        print(f"\nHUMAN vs FINAL VERDICT on {n} answers you graded: correct agrees {c}/{n} ({c / n:.0%}), "
              f"supported agrees {s}/{n} ({s / n:.0%}), both {both}/{n} ({both / n:.0%})")
        for r in shared:
            h, f = human[r["q"]["id"]], r["final"]
            if h["correct"] != f["correct"] or h["supported"] != f["supported"]:
                print(f"  {r['q']['id']}: you {h['correct']}/{h['supported']} vs final {f['correct']}/{f['supported']} ({f['by']}) | {h['notes'][:80]}")
    else:
        print("\nHUMAN vs FINAL VERDICT: no graded rows found in eval/human_labels.csv yet")

    with open(RESULTS, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["id", "kind", "refused", "correct", "supported", "decided_by", "citations_valid",
                         "draft_citations_valid", "guardrail_kind", "expected_retrieved", "expected_cited",
                         "model", "input_tokens", "output_tokens", "seconds", "suggested_cause", "answer"])
        for r in rows:
            q, a, c, fin = r["q"], r["a"], r["checks"], r["final"]
            writer.writerow([q["id"], q["kind"], int(c["refused"]), fin["correct"], fin["supported"], fin["by"],
                             int(c["citations_valid"]), int(c["draft_citations_valid"]), a.get("guardrail_kind") or "",
                             c["expected_retrieved"], c["expected_cited"], a["model"], a["input_tokens"],
                             a["output_tokens"], a["seconds"], r["cause"], a["answer"]])
    E2E_SUMMARY.write_text(json.dumps({"counts": counts, "cost": cost, "agreement_with_human": agreement}, indent=2))


def main(argv):
    questions = load_questions()
    if "fresh" in argv:
        for path in (ANSWERS, VERDICTS):
            path.unlink(missing_ok=True)
    if "answers" in argv:
        answers = run_agent_on_questions(questions)
        write_sheet(questions, answers)
        prefill_human_labels(questions)
        print(f"\nDone: {len(answers)}/{len(questions)} answers saved.")
        print("Next: read eval/answers_for_grading.md and fill eval/human_labels.csv BEFORE running `main.py evaluate`.")
        return
    retrieval_eval()
    answers = run_agent_on_questions(questions)
    write_sheet(questions, answers)
    prefill_human_labels(questions)
    verdicts = judge_all(questions, answers)
    end_to_end_report(questions, answers, verdicts)


if __name__ == "__main__":
    main(sys.argv[1:])