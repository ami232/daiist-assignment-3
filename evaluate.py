"""
Assignment 3: evaluation (`main.py evaluate`).

Part 1 - retrieval: hit rate at k = 1, 3, 5 for each chunking design on the
answerable questions in eval/questions.csv, plus how many words the top-k
chunks would add to the prompt. Results go to eval/retrieval_*.

(Part 2, the agent evaluation, is added later.)

A retrieved chunk is a hit when it comes from the expected document and
- for a PDF: the expected page is inside the chunk's page range;
- for a web page: the expected section title is part of the chunk's section.
Multi questions have two expected passages: we report whether at least one
was found ("any") and whether both were found ("all").
"""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

import index

ROOT = Path(__file__).resolve().parent
EVAL_DIR = ROOT / "eval"
QUESTIONS = EVAL_DIR / "questions.csv"
QUERY_CACHE = EVAL_DIR / "query_embeddings.json"
KS = (1, 3, 5)


def log(message: str = "") -> None:
    print(message, flush=True)


def load_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r["question"].strip()]


def is_spanish(question: str) -> bool:
    return bool(re.search(r"[¿¡ñáéíóú]", question.lower()))


def expected_passages(row: dict) -> list[tuple[str, str]]:
    """(source, location) pairs. One source with several locations means the
    same document for each; otherwise sources and locations pair up in order."""
    sources = [s.strip() for s in row["expected_source"].split(";") if s.strip()]
    locations = [l.strip() for l in row["expected_location"].split(";") if l.strip()]
    if len(sources) == 1:
        return [(sources[0], loc) for loc in locations] or [(sources[0], "")]
    return list(zip(sources, locations))


def matches(metadata: dict, source: str, location: str) -> bool:
    if metadata["source"] != source:
        return False
    if not location:
        return True
    if location.isdigit():
        return metadata["page"] <= int(location) <= metadata["page_end"]
    return location.lower() in metadata["section"].lower()


# --------------------------------------------------------------------------- query embeddings (cached)

def query_vectors(questions: list[str]) -> dict[str, list[float]]:
    """Embed each question once and keep the vectors in eval/, so re-running
    the evaluation or adding a design costs no extra quota."""
    cache = json.loads(QUERY_CACHE.read_text(encoding="utf-8")) if QUERY_CACHE.is_file() else {}
    key = f"{index.EMBED_MODEL}/{index.EMBED_DIM}"
    cache.setdefault(key, {})
    missing = [q for q in questions if q not in cache[key]]
    for start in range(0, len(missing), index.EMBED_BATCH):
        batch = missing[start:start + index.EMBED_BATCH]
        for q, v in zip(batch, index.embed(batch, "RETRIEVAL_QUERY")):
            cache[key][q] = v
        QUERY_CACHE.write_text(json.dumps(cache), encoding="utf-8")
    if missing:
        log(f"Embedded {len(missing)} new questions (cached in {QUERY_CACHE.relative_to(ROOT)}).")
    return cache[key]


# --------------------------------------------------------------------------- retrieval evaluation

def evaluate_retrieval(designs=index.DESIGNS) -> dict:
    rows = [r for r in load_questions() if r["kind"].strip().lower() != "unanswerable"]
    vectors = query_vectors([r["question"] for r in rows])
    kmax = max(KS)

    per_question, summary = [], {}
    for design in designs:
        col = index.collection(design)
        stats = {"n": len(rows), "hit": {k: 0 for k in KS}, "words": {k: 0 for k in KS},
                 "multi_n": 0, "multi_all": {k: 0 for k in KS},
                 "es_n": 0, "es_hit": {k: 0 for k in KS}, "mrr": 0.0}
        for r in rows:
            result = col.query(query_embeddings=[vectors[r["question"]]], n_results=kmax,
                               include=["metadatas"])
            metas = result["metadatas"][0]
            passages = expected_passages(r)
            # Rank (1-based) at which each expected passage first appears.
            ranks = [next((i + 1 for i, m in enumerate(metas) if matches(m, s, l)), None) for s, l in passages]
            first = min((x for x in ranks if x), default=None)
            spanish = is_spanish(r["question"])
            for k in KS:
                hit = first is not None and first <= k
                stats["hit"][k] += hit
                stats["words"][k] += sum(m["words"] for m in metas[:k])
                if r["kind"] == "multi":
                    stats["multi_all"][k] += all(x is not None and x <= k for x in ranks)
                if spanish:
                    stats["es_hit"][k] += hit
            stats["mrr"] += 1 / first if first else 0
            stats["multi_n"] += r["kind"] == "multi"
            stats["es_n"] += spanish
            per_question.append({
                "design": design, "id": r["id"], "kind": r["kind"], "spanish": int(spanish),
                "first_hit_rank": first or "", "ranks_per_passage": ";".join(str(x or "-") for x in ranks),
                "top5": " | ".join(f"{m['source']} {m['location'][:50]}" for m in metas),
            })

        n = stats["n"]
        summary[design] = {
            "questions": n,
            **{f"hit@{k}": round(stats["hit"][k] / n, 3) for k in KS},
            "mrr": round(stats["mrr"] / n, 3),
            **{f"multi_all@{k}": round(stats["multi_all"][k] / stats["multi_n"], 3) for k in KS if stats["multi_n"]},
            **{f"spanish_hit@{k}": round(stats["es_hit"][k] / stats["es_n"], 3) for k in KS if stats["es_n"]},
            **{f"words@{k}": round(stats["words"][k] / n) for k in KS},
        }

    with (EVAL_DIR / "retrieval_per_question.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(per_question[0]))
        w.writeheader(); w.writerows(per_question)
    (EVAL_DIR / "retrieval_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def print_retrieval(summary: dict) -> None:
    designs = list(summary)
    first = summary[designs[0]]
    log(f"\nRetrieval on {first['questions']} answerable questions\n")
    log(f"{'metric':<18}" + "".join(f"{d:>12}" for d in designs))
    for metric in first:
        if metric == "questions":
            continue
        log(f"{metric:<18}" + "".join(f"{summary[d].get(metric, ''):>12}" for d in designs))
    log("\nhit@k: an expected passage is in the top k.  multi_all@k: both passages of a multi question are.")
    log("words@k: words the top-k chunks add to the prompt (mean).  Details: eval/retrieval_per_question.csv")


# =========================================================================== Part 2: the agent

ANSWERS = EVAL_DIR / "agent_answers.jsonl"
JUDGE = EVAL_DIR / "judge.jsonl"
HUMAN_LABELS = EVAL_DIR / "human_labels.csv"
GRADING_SHEET = EVAL_DIR / "grading_sheet.md"
SUMMARY = EVAL_DIR / "summary.json"
JUDGE_MODEL, JUDGE_FALLBACK = "gemini-3-flash-preview", "gemini-3.1-flash-lite"

# 20 answers for the human grading: every unanswerable and multi question, and 7 single ones.
TO_GRADE = ["u01", "u02", "u03", "u04", "u06", "u07",
            "m01", "m02", "m03", "m04", "m05", "m06", "m07",
            "q01", "q03", "q08", "q12", "q13", "q16", "q18"]

REFUSAL = re.compile(
    r"I (?:do not|don't|cannot|can't) (?:know|find|answer|say)|"
    r"(?:not|isn't|is not) (?:covered|included|specified|mentioned|available|stated|found) in|"
    r"documents? (?:do(?:es)? not|don't) (?:contain|cover|include|specify|say|mention|provide|state)|"
    r"no (?:sé|lo sé|puedo (?:responder|saber|indicar))|"
    r"no (?:aparece|figura|se especifica|se menciona|está (?:disponible|en los documentos))|"
    r"los documentos no (?:contienen|incluyen|cubren|dicen|especifican|mencionan|indican|recogen)",
    re.I,
)


def code_refused(answer: str) -> bool:
    """A refusal says it doesn't know near the start. Answerable answers often
    end with "the exact amount is set by SEPIE", which must not count."""
    return bool(REFUSAL.search(answer[:350]))


def read_jsonl(path: Path) -> dict[str, dict]:
    if not path.is_file():
        return {}
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return {r["id"]: r for r in rows}


def append_jsonl(path: Path, row: dict) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def run_answers() -> dict[str, dict]:
    """Ask the agent every question once; answers are saved as they come, so
    a crash or a quota stop loses nothing and a re-run only asks what's missing."""
    import time as _time
    from agent import Passage, answer_question, check_citations

    done = read_jsonl(ANSWERS)
    # Re-run the current citation check and refusal check on saved answers, so a
    # fix to either check applies without asking the agent again.
    for row in done.values():
        row["citation_check"] = check_citations(row["answer"], [Passage(**p) for p in row["passages"]])
        row["code_refused"] = code_refused(row["answer"])
    questions = load_questions()
    todo = [q for q in questions if q["id"] not in done]
    for n, q in enumerate(todo, 1):
        log(f"[{n}/{len(todo)}] {q['id']}: {q['question'][:70]}")
        try:
            result = answer_question(q["question"])
        except Exception as error:  # noqa: BLE001 - keep going, record the failure
            log(f"   failed: {type(error).__name__}: {str(error)[:200]}")
            continue
        row = {"id": q["id"], "kind": q["kind"], **result,
               "code_refused": code_refused(result["answer"])}
        append_jsonl(ANSWERS, row)
        done[q["id"]] = row
        _time.sleep(10)  # stay under the free tier's requests-per-minute limit
    return done


def code_checks(answers: dict[str, dict]) -> dict:
    """What code can check without a judge: refusals and citations."""
    questions = {q["id"]: q for q in load_questions()}
    answerable = [a for i, a in answers.items() if questions[i]["kind"] != "unanswerable"]
    unanswerable = [a for i, a in answers.items() if questions[i]["kind"] == "unanswerable"]
    return {
        "answered": len(answers),
        "correct_refusals": sum(a["code_refused"] for a in unanswerable),
        "unanswerable": len(unanswerable),
        "wrong_refusals": sum(a["code_refused"] for a in answerable),
        "answerable": len(answerable),
        "answers_with_citations": sum(bool(a["citation_check"]["citations"]) for a in answerable),
        "citation_check_fired": [a["id"] for a in answers.values() if a["citation_check"]["fired"]],
        "mean_searches": round(sum(sum(c["tool"] == "search" for c in a["tool_calls"]) for a in answers.values()) / len(answers), 2),
        "mean_seconds": round(sum(a["seconds"] for a in answers.values()) / len(answers), 1),
        "mean_model_calls": round(sum(a["model_calls"] for a in answers.values()) / len(answers), 2),
        "mean_input_tokens": round(sum(a["input_tokens"] for a in answers.values()) / len(answers)),
        "mean_output_tokens": round(sum(a["output_tokens"] for a in answers.values()) / len(answers)),
    }


def write_grading_sheet(answers: dict[str, dict]) -> None:
    """A readable file for the human grading: question, reference, answer and
    what was retrieved. It deliberately shows no judge verdicts."""
    questions = {q["id"]: q for q in load_questions()}
    lines = ["# Grading sheet", "",
             "Grade each answer **before** looking at the judge's verdicts. For each one, add a row to "
             "`eval/human_labels.csv`: `id,correct,supported,notes`.", "",
             "- **correct** = 1 if the answer is right against the reference answer (for unanswerable "
             "questions: 1 if it properly says it doesn't know and points to the right place), else 0.",
             "- **supported** = 1 if every claim in the answer is in the retrieved passages, else 0.",
             "- **notes**: why, for every 0.", ""]
    for qid in TO_GRADE:
        a, q = answers.get(qid), questions[qid]
        if not a:
            continue
        lines += [f"---", "", f"## {qid} ({q['kind']})", "", f"**Question:** {q['question']}", "",
                  f"**Reference answer:** {q['reference_answer']}", "",
                  f"**Expected location:** {q['expected_source'] or '—'} {q['expected_location']}", "",
                  "**Assistant's answer:**", "", *[f"> {line}" if line else ">" for line in a["answer"].splitlines()], "",
                  "**Retrieved passages** (click to open the text the assistant saw):", ""]
        for n, p in enumerate(a["passages"], 1):
            lines += [f"<details><summary>[{n}] {p['title']} — {p['location']}</summary>", "",
                      p["text"], "", "</details>", ""]
    GRADING_SHEET.write_text("\n".join(lines), encoding="utf-8")


# --------------------------------------------------------------------------- LLM judge

RUBRIC = """You are grading an assistant that answers students' questions about Erasmus+ grants
using only official European Commission documents. You get the question, the reference
answer written by the test author, the passages the assistant retrieved, and its answer.

Grade two things, each 1 or 0:

correct
- Answerable question: 1 if the answer gives the key facts of the reference answer
  (numbers, durations, conditions) and contradicts none of them. Extra correct detail is
  fine. Missing a key fact, a wrong number, or refusing to answer = 0.
- Unanswerable question (the reference says the documents do not cover it): 1 if the
  answer clearly says it does not know / the documents don't cover it and does not invent
  the missing information; pointing the student to the right place is expected. Giving a
  specific answer anyway (e.g. a date or an exact amount) = 0.

supported
- 1 if every factual claim in the answer can be found in the retrieved passages (a
  translation into Spanish is fine). 0 if any claim (a number, a rule, an example) is not
  in the passages, even if it happens to be true. A plain refusal with no claims = 1.

Reply with JSON only: {"correct": 0 or 1, "supported": 0 or 1, "reason": "one sentence"}"""


def judge_one(q: dict, a: dict) -> dict:
    from google import genai
    from google.genai import types
    from api_key import load_api_key

    passages = "\n\n".join(f"[{p['title']} — {p['location']}]\n{p['text']}" for p in a["passages"]) or "(none)"
    prompt = (f"{RUBRIC}\n\nQUESTION ({q['kind']}): {q['question']}\n\n"
              f"REFERENCE ANSWER: {q['reference_answer']}\n\nRETRIEVED PASSAGES:\n{passages}\n\n"
              f"ASSISTANT'S ANSWER:\n{a['answer']}")
    import time as _time

    client = genai.Client(api_key=load_api_key(), http_options=types.HttpOptions(timeout=60_000))
    config = types.GenerateContentConfig(temperature=0, response_mime_type="application/json")
    last_error = None
    # Wait before retrying: an instant retry hits the same overloaded moment.
    for wait, model in ((0, JUDGE_MODEL), (15, JUDGE_MODEL), (45, JUDGE_FALLBACK)):
        _time.sleep(wait)
        try:
            verdict = json.loads(client.models.generate_content(model=model, contents=prompt, config=config).text)
            return {"correct": int(verdict["correct"]), "supported": int(verdict["supported"]),
                    "reason": verdict.get("reason", ""), "judge_model": model}
        except Exception as error:  # noqa: BLE001 - retry, then fall back
            last_error = error
    raise RuntimeError(f"judge failed: {last_error}")


def run_judge(answers: dict[str, dict]) -> dict[str, dict]:
    questions = {q["id"]: q for q in load_questions()}
    done = read_jsonl(JUDGE)
    for qid, a in answers.items():
        if qid in done:
            continue
        try:
            verdict = {"id": qid, **judge_one(questions[qid], a)}
        except RuntimeError as error:
            log(f"  skipped {qid} ({str(error)[:80]}); run again to judge it")
            continue
        append_jsonl(JUDGE, verdict)
        done[qid] = verdict
        log(f"  judged {qid}: correct={verdict['correct']} supported={verdict['supported']}")
    return done


def agreement(verdicts: dict[str, dict]) -> dict:
    if not HUMAN_LABELS.is_file():
        return {}
    with HUMAN_LABELS.open(newline="", encoding="utf-8") as f:
        human = {r["id"].strip(): r for r in csv.DictReader(f) if (r.get("id") or "").strip()}
    both = [i for i in human if i in verdicts]
    if not both:
        return {"graded_by_you": len(human)}
    result = {"graded_by_you": len(human), "compared": len(both)}
    for key in ("correct", "supported"):
        same = sum(int(human[i][key]) == verdicts[i][key] for i in both)
        result[f"{key}_agreement"] = round(same / len(both), 3)
        result[f"{key}_disagreements"] = [i for i in both if int(human[i][key]) != verdicts[i][key]]
    return result


def results(answers: dict[str, dict], verdicts: dict[str, dict]) -> dict:
    questions = {q["id"]: q for q in load_questions()}
    answerable = [i for i in answers if questions[i]["kind"] != "unanswerable"]
    unanswerable = [i for i in answers if questions[i]["kind"] == "unanswerable"]
    judged = [i for i in answerable if i in verdicts]
    return {
        "correct_answers": sum(verdicts[i]["correct"] for i in judged),
        "answerable_judged": len(judged),
        "unsupported_answers": sum(1 - verdicts[i]["supported"] for i in answers if i in verdicts),
        "correct_refusals": sum(answers[i]["code_refused"] for i in unanswerable),
        "unanswerable": len(unanswerable),
        "wrong_refusals": sum(answers[i]["code_refused"] for i in answerable),
        "by_kind": {kind: {"n": sum(questions[i]["kind"] == kind for i in verdicts),
                           "correct": sum(verdicts[i]["correct"] for i in verdicts if questions[i]["kind"] == kind)}
                    for kind in ("single", "multi", "unanswerable")},
    }


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser(description="Evaluate retrieval and the agent.")
    parser.add_argument("--stage", choices=["all", "retrieval", "answers", "judge"], default="all",
                        help="answers: run the agent and code checks only (no judge), for human grading first")
    args = parser.parse_args()

    summary = {}
    if args.stage in ("all", "retrieval"):
        summary["retrieval"] = evaluate_retrieval()
        print_retrieval(summary["retrieval"])
    if args.stage in ("all", "answers", "judge"):
        answers = run_answers()
        summary["code_checks"] = code_checks(answers)
        write_grading_sheet(answers)
        log(f"\nCode checks: {json.dumps(summary['code_checks'], indent=1)}")
        log(f"Grading sheet for your 20 answers: {GRADING_SHEET.relative_to(ROOT)}")
    if args.stage in ("all", "judge"):
        verdicts = run_judge(answers)
        summary["results"] = results(answers, verdicts)
        summary["agreement_with_human"] = agreement(verdicts)
        log(f"\nResults: {json.dumps(summary['results'], indent=1)}")
        log(f"Agreement with your labels: {json.dumps(summary['agreement_with_human'], indent=1)}")
    previous = json.loads(SUMMARY.read_text(encoding="utf-8")) if SUMMARY.is_file() else {}
    SUMMARY.write_text(json.dumps({**previous, **summary}, indent=2, ensure_ascii=False), encoding="utf-8")


if __name__ == "__main__":
    try:
        main()
    except index.DailyQuotaExhausted:
        log("Daily embedding quota reached; everything done so far is saved. Run again after 09:00 (Spain).")
        sys.exit(2)
