"""
Assignment 3: evaluation (`main.py evaluate`).

    uv run python main.py evaluate                     # everything
    uv run python evaluate.py --retrieval-only         # hit rates only (cheap)

Stages, all written to eval/ and resume-safe (rerun after a crash or quota stop):
  1. retrieval hit rate at k=1,3,5 per design   -> retrieval.csv (+ query_cache.json)
  2. the agent on every question                -> answers.jsonl
  3. code checks (valid citations, refusals)    -> in verdicts.csv
  4. LLM judge with a rubric + retrieved text   -> verdicts.csv
  5. agreement with human_labels.csv
  6. summary                                    -> summary.md

Pattern from session 10's 07-own-harness/evaluate.py: the judge returns a
structured verdict (reasoning first, then the scores) and exact things are
checked in code, not by the judge.
"""

import argparse
import csv
import json
import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
EVAL_DIR = Path(os.environ.get("EVAL_DIR", ROOT / "eval"))
QUESTIONS = Path(os.environ.get("EVAL_QUESTIONS", EVAL_DIR / "questions.csv"))
KS = (1, 3, 5)

JUDGE_MODEL = "gemini-3.5-flash"  # a stronger model than the agent's; change if unavailable

# Edit this rubric to change how the judge grades. {placeholders} are filled per answer.
JUDGE_RUBRIC = """You are grading the answer of a support assistant for Chedar, a production-management
software. The assistant answers from help-centre articles it retrieved.

Give two scores, each 0 or 1.

correct: does the answer agree with the reference answer?
  - 1 if it states the same facts as the reference answer (wording may differ, extra correct detail is fine).
  - 1 for an unanswerable question only if the assistant clearly says the help centre does not
    cover it (or asks to add a document) and does not invent an answer.
  - 0 if it misses a key fact, contradicts the reference, answers an unanswerable question,
    or refuses a question that has a reference answer.

supported: is every claim in the answer backed by the retrieved text below?
  - 1 if each factual claim (steps, names, numbers, menu paths) appears in the retrieved text.
  - 0 if any claim is not in the retrieved text, even if it is true in general.
  - A refusal with no factual claims is supported (1).

Question: {question}
Question type: {kind}
Reference answer: {reference}

Retrieved text (the only evidence allowed):
{evidence}

Assistant answer:
{answer}

Reply with JSON only: {{"reasoning": "two or three sentences", "correct": 0 or 1, "supported": 0 or 1}}"""

# Phrases that signal "I can't answer this from the help centre".
REFUSAL_PATTERNS = [
    r"\bi (?:could not|couldn't|can't|cannot|can not|was unable to) find\b",
    r"\bi (?:don't|do not) (?:have|know|see)\b",
    r"\bno (?:relevant |matching )?(?:information|article|document|results?|mention)\b",
    r"\b(?:not|isn't|is not|aren't|are not) (?:covered|documented|mentioned|available|included|in the (?:help|documentation|articles))\b",
    r"\b(?:does not|doesn't|do not|don't) (?:cover|mention|contain|include|say|specify)\b",
    r"\bunable to (?:answer|find|confirm)\b",
    r"\bnot able to (?:answer|find|confirm)\b",
    r"\bno answer\b",
]

URL_RE = re.compile(r"https?://[^\s)\]>\"'`,]+")


# ---------------------------------------------------------------- small helpers

def norm_url(url: str) -> str:
    """Compare article URLs without trailing punctuation, slash, .md or #fragment."""
    url = url.strip().split("#")[0].rstrip(".,;:)/")
    return url[:-3] if url.endswith(".md") else url


def read_csv(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def write_csv(path: Path, rows: list[dict], fields: list[str]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def load_questions() -> list[dict]:
    rows = [r for r in read_csv(QUESTIONS) if (r.get("question") or "").strip()]
    if not rows:
        sys.exit(f"No questions in {QUESTIONS}. Write your test questions first (see eval/README.md).")
    for r in rows:
        r["kind"] = r["kind"].strip().lower()
        r["expected"] = {norm_url(s) for s in (r.get("expected_source") or "").split(";") if s.strip()}
    return rows


def pct(n: int, total: int) -> str:
    return f"{100 * n / total:.0f}%" if total else "n/a"


def table(header: list[str], rows: list[list]) -> str:
    """Plain markdown table, also fine in a terminal."""
    lines = ["| " + " | ".join(header) + " |", "|" + "|".join("---" for _ in header) + "|"]
    lines += ["| " + " | ".join(str(c) for c in row) + " |" for row in rows]
    return "\n".join(lines)


# ---------------------------------------------------------------- 1. retrieval

def cache_query_embeddings():
    """Wrap index.embed_texts so a query is embedded once, ever (saved in query_cache.json).

    Needs search_index to call embed_texts through the index module, which a plain call does.
    """
    import index

    path = EVAL_DIR / "query_cache.json"
    cache = json.loads(path.read_text(encoding="utf-8")) if path.exists() else {}
    original = index.embed_texts

    def cached(texts, task):
        keys = [f"{task}|{t}" for t in texts]
        missing = [t for t, k in zip(texts, keys) if k not in cache]
        if missing:
            for t, vec in zip(missing, original(missing, task)):
                cache[f"{task}|{t}"] = vec
            path.write_text(json.dumps(cache), encoding="utf-8")
        return [cache[k] for k in keys]

    index.embed_texts = cached


def words(text: str) -> int:
    return len(text.split())


def retrieval_eval(questions: list[dict]) -> list[dict]:
    from index import DESIGNS, search_index

    answerable = [q for q in questions if q["kind"] != "unanswerable" and q["expected"]]
    rows = []
    for design in DESIGNS:
        # search once at the largest k, slice for the smaller ones (results are ranked)
        found = {q["id"]: search_index(q["question"], k=max(KS), design=design) for q in answerable}
        for k in KS:
            hits_any = hits_all = n_multi = multi_all = 0
            added = []
            for q in answerable:
                top = found[q["id"]][:k]
                sources = {norm_url(c["source"]) for c in top}
                added.append(sum(words(c["text"]) for c in top))
                any_hit = bool(q["expected"] & sources)
                hits_any += any_hit
                if q["kind"] == "multi":
                    n_multi += 1
                    multi_all += q["expected"] <= sources
                hits_all += q["expected"] <= sources
            rows.append({
                "design": design, "k": k, "questions": len(answerable),
                "hit_rate_any": round(hits_any / len(answerable), 3) if answerable else "",
                "multi_questions": n_multi,
                "multi_hit_any": round(sum(
                    bool(q["expected"] & {norm_url(c["source"]) for c in found[q["id"]][:k]})
                    for q in answerable if q["kind"] == "multi") / n_multi, 3) if n_multi else "",
                "multi_hit_all": round(multi_all / n_multi, 3) if n_multi else "",
                "avg_words_added": round(sum(added) / len(added)) if added else "",
            })
    fields = ["design", "k", "questions", "hit_rate_any", "multi_questions", "multi_hit_any",
              "multi_hit_all", "avg_words_added"]
    write_csv(EVAL_DIR / "retrieval.csv", rows, fields)
    return rows


def retrieval_table(rows: list[dict]) -> str:
    header = ["design", "k", "hit rate (any source)", "multi: any", "multi: all", "avg words in prompt"]
    body = [[r["design"], r["k"], pct_val(r["hit_rate_any"]), pct_val(r["multi_hit_any"]),
             pct_val(r["multi_hit_all"]), r["avg_words_added"]] for r in rows]
    return table(header, body)


def pct_val(x) -> str:
    return "n/a" if x == "" else f"{100 * float(x):.0f}%"


# ---------------------------------------------------------------- 2. agent answers

def never_approve(tool_name, args) -> bool:
    """The evaluation must not change the index: every add_document request is denied."""
    return False


def run_answers(questions: list[dict]) -> list[dict]:
    from agent import run_agent

    path = EVAL_DIR / "answers.jsonl"
    done = {r["id"] for r in read_jsonl(path)}
    todo = [q for q in questions if q["id"] not in done]
    print(f"Agent: {len(done)} answers already saved, {len(todo)} to run.")
    for q in todo:
        try:
            result = run_agent(q["question"], approve=never_approve)
        except Exception as e:  # keep going; failed questions are retried on the next run
            print(f"  {q['id']}: agent failed ({type(e).__name__}: {e}), will retry next run")
            continue
        record = {"id": q["id"], "question": q["question"], "answer": result["answer"],
                  "trace": result["trace"], "tokens": result["tokens"], "seconds": result["seconds"]}
        with path.open("a", encoding="utf-8") as f:
            f.write(json.dumps(record, ensure_ascii=False, default=str) + "\n")
        print(f"  {q['id']}: {result['seconds']:.1f}s, {result['tokens']} tokens")
    return read_jsonl(path)


# ---------------------------------------------------------------- 3. code checks

def trace_text(trace) -> str:
    """Everything the tools returned, as one string (used as judge evidence and for URLs)."""
    parts = []
    for step in trace:
        if isinstance(step, dict):
            parts.append(str(step.get("result", step.get("output", ""))))
        else:
            parts.append(str(step))
    return "\n".join(parts)


def retrieved_urls(trace) -> set[str]:
    return {norm_url(u) for u in URL_RE.findall(trace_text(trace))}


def cited_urls(answer: str) -> set[str]:
    return {norm_url(u) for u in URL_RE.findall(answer)}


def is_refusal(answer: str) -> bool:
    low = answer.lower()
    return any(re.search(p, low) for p in REFUSAL_PATTERNS)


def code_checks(question: dict, record: dict) -> dict:
    cited, retrieved = cited_urls(record["answer"]), retrieved_urls(record["trace"])
    refused = is_refusal(record["answer"])
    unanswerable = question["kind"] == "unanswerable"
    return {
        "n_cited": len(cited),
        "citations_valid": int(bool(cited) and cited <= retrieved),
        "invalid_citations": " ".join(sorted(cited - retrieved)),
        "refused": int(refused),
        "correct_refusal": int(unanswerable and refused),
        "wrong_refusal": int(not unanswerable and refused),
    }


# ---------------------------------------------------------------- 4. LLM judge

def judge_answer(question: dict, record: dict) -> dict:
    """Ask Gemini for {'reasoning', 'correct', 'supported'}. Tests replace this function."""
    from langchain_google_genai import ChatGoogleGenerativeAI
    from pydantic import BaseModel, Field

    from api_key import load_api_key

    class Verdict(BaseModel):
        reasoning: str = Field(description="Two or three sentences checking the answer against the rubric.")
        correct: int = Field(description="1 if correct against the reference answer, else 0.")
        supported: int = Field(description="1 if every claim is in the retrieved text, else 0.")

    load_api_key()
    judge = ChatGoogleGenerativeAI(model=JUDGE_MODEL, temperature=0).with_structured_output(Verdict)
    prompt = JUDGE_RUBRIC.format(
        question=question["question"], kind=question["kind"],
        reference=question.get("reference_answer", ""),
        evidence=trace_text(record["trace"]) or "(nothing was retrieved)",
        answer=record["answer"],
    )
    return judge.invoke(prompt).model_dump()


VERDICT_FIELDS = ["id", "kind", "correct", "supported", "reason", "n_cited", "citations_valid",
                  "invalid_citations", "refused", "correct_refusal", "wrong_refusal"]


def run_judge(questions: list[dict], answers: list[dict]) -> list[dict]:
    path = EVAL_DIR / "verdicts.csv"
    rows = read_csv(path)
    done = {r["id"] for r in rows}
    by_id = {q["id"]: q for q in questions}
    todo = [a for a in answers if a["id"] in by_id and a["id"] not in done]
    print(f"Judge: {len(done)} verdicts already saved, {len(todo)} to grade.")
    for record in todo:
        q = by_id[record["id"]]
        try:
            verdict = judge_answer(q, record)
        except Exception as e:
            print(f"  {q['id']}: judge failed ({type(e).__name__}: {e}), will retry next run")
            continue
        rows.append({"id": q["id"], "kind": q["kind"], "correct": int(verdict["correct"]),
                     "supported": int(verdict["supported"]), "reason": verdict["reasoning"].replace("\n", " "),
                     **code_checks(q, record)})
        write_csv(path, rows, VERDICT_FIELDS)  # save as we go
        print(f"  {q['id']}: correct={verdict['correct']} supported={verdict['supported']}")
    return rows


# ---------------------------------------------------------------- 5. agreement

def agreement(verdicts: list[dict]) -> tuple[str, list[str]]:
    human = {r["id"]: r for r in read_csv(EVAL_DIR / "human_labels.csv") if r.get("id")}
    judge = {r["id"]: r for r in verdicts}
    shared = sorted(set(human) & set(judge))
    if not shared:
        return "No human labels yet (eval/human_labels.csv is empty).", []
    lines, disagreements = [], []
    for field in ("correct", "supported"):
        same = [i for i in shared if str(human[i][field]).strip() == str(judge[i][field]).strip()]
        lines.append(f"- {field}: {pct(len(same), len(shared))} agreement ({len(same)}/{len(shared)})")
        for i in shared:
            if i not in same:
                disagreements.append(f"- {i} {field}: human={human[i][field]} judge={judge[i][field]}; "
                                     f"judge reason: {judge[i]['reason']}")
    return "\n".join(lines), disagreements


# ---------------------------------------------------------------- 6. summary

def write_summary(retrieval_rows, answers, verdicts, questions) -> str:
    n = len(verdicts)
    out = ["# Evaluation summary", "", f"Questions: {len(questions)}; answers: {len(answers)}; judged: {n}.", ""]
    out += ["## Retrieval", "", retrieval_table(retrieval_rows) if retrieval_rows else "(not run)", ""]
    if verdicts:
        def total(field):
            return sum(int(v[field]) for v in verdicts)

        unans = [v for v in verdicts if v["kind"] == "unanswerable"]
        ans = [v for v in verdicts if v["kind"] != "unanswerable"]
        out += ["## Answers", "", table(["measure", "count"], [
            ["correct (judge)", f"{total('correct')}/{n}"],
            ["unsupported (judge)", f"{n - total('supported')}/{n}"],
            ["correct refusals (code)", f"{total('correct_refusal')}/{len(unans)} unanswerable"],
            ["wrong refusals (code)", f"{total('wrong_refusal')}/{len(ans)} answerable"],
            ["answers with all citations valid (code)", f"{sum(int(v['citations_valid']) for v in ans)}/{len(ans)} answerable"],
        ]), ""]
        agree, disagreements = agreement(verdicts)
        out += ["## Judge vs human labels", "", agree, ""]
        if disagreements:
            out += ["Disagreements:", ""] + disagreements + [""]
    if answers:
        ids = {v["id"] for v in verdicts} or {a["id"] for a in answers}
        used = [a for a in answers if a["id"] in ids] or answers
        out += ["## Cost and latency", "",
                f"- mean tokens per question: {sum(a['tokens'] for a in used) / len(used):.0f}",
                f"- mean seconds per question: {sum(a['seconds'] for a in used) / len(used):.1f}", ""]
    text = "\n".join(out)
    (EVAL_DIR / "summary.md").write_text(text, encoding="utf-8")
    return text


def update_summary_retrieval(rows: list[dict]) -> None:
    """Replace only the retrieval table in an existing summary.md; keep the answer sections."""
    path = EVAL_DIR / "summary.md"
    if path.exists():
        text = path.read_text(encoding="utf-8")
        pattern = r"(## Retrieval\n\n).*?(\n\n(?:## |\Z))"
        new = re.sub(pattern, lambda m: m.group(1) + retrieval_table(rows) + m.group(2),
                     text, count=1, flags=re.S)
        path.write_text(new, encoding="utf-8")


# ---------------------------------------------------------------- main

def main() -> None:
    global QUESTIONS
    parser = argparse.ArgumentParser(description="Evaluate retrieval and the agent.")
    parser.add_argument("--retrieval-only", action="store_true", help="only the hit-rate tables (cheap)")
    parser.add_argument("--questions", help="questions CSV (default eval/questions.csv)")
    args = parser.parse_args()
    if args.questions:
        QUESTIONS = Path(args.questions)

    questions = load_questions()
    EVAL_DIR.mkdir(exist_ok=True)

    cache_query_embeddings()
    retrieval_rows = retrieval_eval(questions)
    print("\nRetrieval\n" + retrieval_table(retrieval_rows) + "\n")
    if args.retrieval_only:
        update_summary_retrieval(retrieval_rows)
        return

    answers = run_answers(questions)
    verdicts = run_judge(questions, answers)
    print("\n" + write_summary(retrieval_rows, answers, verdicts, questions))


if __name__ == "__main__":
    main()
