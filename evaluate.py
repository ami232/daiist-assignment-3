"""
Assignment 3: evaluation (`main.py evaluate`).

Stage 1, retrieval: hit rate at k = 1, 3, 5 for every chunking design and
search method, on the answerable questions of eval/questions.csv.
Stage 2, end to end: the agent answers every question (saved one by one in
eval/answers.jsonl), code checks (citations exist and were retrieved, refusals),
a grading sheet for the human labels, the LLM judge with eval/rubric.md, and
agreement between judge and eval/human_labels.csv. Tokens and seconds per question.
Stage 3, NIS2 before/after for the questions only NIS2 answers.

Answers, verdicts and hit rates are cached in eval/, so `main.py evaluate`
re-runs without API calls once everything has been computed.

    uv run python evaluate.py                         # everything (cached where possible)
    uv run python evaluate.py --stage retrieval       # recompute hit rates
    uv run python evaluate.py --stage answers         # agent answers + code checks + grading sheet (no judge)
    uv run python evaluate.py --stage judge           # + judge and agreement
    uv run python evaluate.py --stage nis2            # before/after table

A hit for a question = a retrieved chunk from the expected regulation that
covers the expected article/annex (paragraph numbers are ignored: a chunk of
Article 33 counts for "Article 33(1)"). For `multi` questions, the strict hit
needs every expected passage in the top k; the lenient one needs at least one.
"""

import argparse
import asyncio
import csv
import hashlib
import json
import re
import sys
import time
from pathlib import Path

import pandas as pd
from pydantic import BaseModel, Field

from ingest import DESIGNS, collection
from retrieval import METHODS, SERVED_DESIGN, article_key, search

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
KS = (1, 3, 5)

sys.stdout.reconfigure(encoding="utf-8")


def read_questions(path: Path) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if (r.get("question") or "").strip()]
    for r in rows:
        r["kind"] = r["kind"].strip().lower()
        sources = [s.strip() for s in r["expected_source"].split(";") if s.strip()]
        locations = [l.strip() for l in r["expected_location"].split(";") if l.strip()]
        if len(sources) == 1 and len(locations) > 1:
            sources = sources * len(locations)
        r["expected"] = [(s, article_key(l)) for s, l in zip(sources, locations)]
    return rows


def first_rank(hits: list[dict], source: str, key: str) -> int | None:
    """1-based rank of the first hit from `source` that covers `key`, or None."""
    for rank, h in enumerate(hits, 1):
        if h["doc"] == source and key in h["covers"].split("|"):
            return rank
    return None


def retrieval_eval(questions: list[dict]) -> pd.DataFrame:
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    rows, scores = [], []
    for design in DESIGNS:
        for method in METHODS:
            for q in questions:
                hits = search(q["question"], design=design, method=method, k=max(KS))
                if method == "vector":
                    scores.append({"design": design, "id": q["id"], "kind": q["kind"],
                                   "top1_score": hits[0]["score"] if hits else None,
                                   "top1": f"{hits[0]['doc']} {hits[0]['location']}" if hits else ""})
                if q["kind"] == "unanswerable":
                    continue
                ranks = [first_rank(hits, s, key) for s, key in q["expected"]]
                row = {"design": design, "method": method, "id": q["id"], "kind": q["kind"],
                       "ranks": ";".join("-" if r is None else str(r) for r in ranks),
                       "retrieved": " | ".join(f"{h['doc']} {h['location']}" for h in hits)}
                for k in KS:
                    found = [r is not None and r <= k for r in ranks]
                    row[f"hit@{k}"] = int(all(found))
                    row[f"any@{k}"] = int(any(found))
                    row[f"words@{k}"] = sum(h["words"] for h in hits[:k])
                rows.append(row)
            print(f"  {design:9} {method:7} done", file=sys.stderr, flush=True)

    per_q = pd.DataFrame(rows)
    per_q.to_csv(EVAL / "retrieval_per_question.csv", index=False)
    pd.DataFrame(scores).to_csv(EVAL / "retrieval_scores.csv", index=False)

    cols = [f"hit@{k}" for k in KS] + [f"any@{k}" for k in KS] + [f"words@{k}" for k in KS]
    summary = per_q.groupby(["design", "method"])[cols].mean().round(3).reset_index()
    multi = per_q[per_q.kind == "multi"].groupby(["design", "method"])[[f"hit@{k}" for k in KS]].mean().round(3)
    multi.columns = [f"multi_{c}" for c in multi.columns]
    summary = summary.merge(multi.reset_index(), on=["design", "method"], how="left")
    summary.insert(2, "n", len(answerable))
    summary.to_csv(EVAL / "retrieval_summary.csv", index=False)
    return summary


# ================================================================ end to end

ANSWERS = EVAL / "answers.jsonl"            # one agent answer per question (before NIS2 is added)
JUDGMENTS = EVAL / "judgments.jsonl"        # one judge verdict per answer
HUMAN = EVAL / "human_labels.csv"
LABEL_SHEET = EVAL / "to_label.md"
RUBRIC = EVAL / "rubric.md"
NIS2_AFTER = EVAL / "nis2_after.jsonl"
JUDGE_MODEL = "gemini-3.1-flash-lite"       # Phase 6 decision 8: different from the agent's model
NIS2_FILE = "corpus/raw/L_2022333EN.01008001.xml.html"
NIS2_QUESTIONS = ("q28", "q29")


def read_jsonl(path: Path) -> dict[str, dict]:
    if not path.is_file():
        return {}
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return {r["id"]: r for r in rows}


def append_jsonl(path: Path, row: dict) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def deny(tool: str, args: dict) -> bool:
    """The evaluation never approves add_document; NIS2 is added in its own step."""
    return False


def nis2_indexed() -> bool:
    return bool(collection(SERVED_DESIGN).get(where={"doc": "NIS2"}, limit=1, include=[])["ids"])


def collect_answers(questions: list[dict], path: Path = ANSWERS) -> dict[str, dict]:
    """Run the agent on every question without a saved answer; save each one as soon as it arrives."""
    from agent import ask_many
    have = read_jsonl(path)
    todo = [q for q in questions if q["id"] not in have]
    if todo:
        if path == ANSWERS and nis2_indexed():
            raise SystemExit("NIS2 is already in the index: answers for the main evaluation must be collected "
                             "before it is added. Restore index/ from git or keep the saved answers.")
        print(f"  asking the agent {len(todo)} question(s)...", file=sys.stderr, flush=True)
        pending = iter(todo)

        def save(r: dict) -> None:
            q = next(pending)
            row = {"id": q["id"], "kind": q["kind"], **r}
            append_jsonl(path, row)
            print(f"  {q['id']}: {r['seconds']}s, {r['total_tokens']} tokens, refused={r['refused']}",
                  file=sys.stderr, flush=True)

        asyncio.run(ask_many([q["question"] for q in todo], approver=deny, on_result=save))
    return read_jsonl(path)


REF = re.compile(r"^(GDPR|AI Act|Data Act|NIS2) (.+)$")


def split_ref(ref: str) -> tuple[str, str]:
    """'AI Act Annex III' -> ('AI Act', 'Annex III')."""
    m = REF.match(ref)
    return (m.group(1), m.group(2)) if m else ("", ref)


def index_refs() -> set[tuple[str, str]]:
    """Every (regulation, 'Article N' / 'Annex X') present in the served index."""
    got = collection(SERVED_DESIGN).get(include=["metadatas"])
    return {(m["doc"], c) for m in got["metadatas"] for c in m["covers"].split("|")}


def code_checks(questions: list[dict], answers: dict) -> pd.DataFrame:
    """What code can check without interpreting the answer."""
    refs = index_refs()
    rows = []
    for q in questions:
        a = answers[q["id"]]
        cited = {split_ref(c) for c in a["citations"]}
        retrieved = {split_ref(r) for r in a["retrieved"]}
        expected = set(q["expected"])
        answerable = q["kind"] != "unanswerable"
        if answerable:
            outcome = "wrong refusal" if a["refused"] else "answered"
        else:
            outcome = "correct refusal" if a["refused"] else "answered unanswerable"
        rows.append({
            "id": q["id"], "kind": q["kind"], "outcome": outcome,
            "n_citations": len(cited),
            "citations_in_index": int(cited <= refs),
            "citations_retrieved": int(cited <= retrieved),
            "expected_retrieved": int(expected <= retrieved) if answerable else None,
            "expected_cited": round(len(expected & cited) / len(expected), 2) if answerable else None,
            "guardrail_fired": int(any(g["fired"] for g in a["guardrails"] if g["guardrail"] == "citations")),
            "withheld": int("withheld by the citation check" in a["answer"]),
            "tool_calls": a["tool_calls"], "searches": sum(1 for t in a["trace"] if t["tool"] == "search"),
            "input_tokens": a["input_tokens"], "output_tokens": a["output_tokens"],
            "total_tokens": a["total_tokens"], "seconds": a["seconds"],
        })
    df = pd.DataFrame(rows)
    df.to_csv(EVAL / "code_checks.csv", index=False)
    return df


def write_label_sheet(questions: list[dict], answers: dict) -> None:
    """Everything a human needs to grade, and nothing from the judge."""
    lines = ["# Answers to grade by hand",
             "", "Fill eval/human_labels.csv (id, correct, supported, notes) with the rules in eval/rubric.md, "
             "before looking at eval/judgments.jsonl.", ""]
    for q in questions:
        a = answers[q["id"]]
        lines += [f"## {q['id']} ({q['kind']})", "",
                  f"**Question.** {q['question']}", "",
                  f"**Reference.** {q['reference_answer']}"
                  + (f" *(expected: {q['expected_source']} {q['expected_location']})*" if q["expected_source"] else ""), "",
                  "**Agent answer.**", "", a["answer"], "",
                  f"**Cited:** {', '.join(a['citations']) or 'none'}  ",
                  f"**Retrieved:** {', '.join(a['retrieved']) or 'none'}", "",
                  "<details><summary>Retrieved passages (full text)</summary>", "", "```",
                  a["retrieved_text"] or "(no search)", "```", "</details>", "", "---", ""]
    LABEL_SHEET.write_text("\n".join(lines), encoding="utf-8")


# Judge v1 (results kept in eval/*_v1.*) asked for the scores first and a reason after: it gave 1 to
# all 35 answers (kappa 0 vs the human labels). v2 makes the judge reason before scoring: list every
# element of the reference and whether the answer contains it, list claims missing from the passages,
# and only then score. Same rubric, same model.
JUDGE_VERSION = "v2"


class Element(BaseModel):
    element: str = Field(description="one fact, condition, exception or passage required by the reference answer")
    present: bool = Field(description="true only if the assistant answer states it (paraphrase allowed)")


class Verdict(BaseModel):
    reference_elements: list[Element]
    answers_as_if_covered: bool = Field(
        description="unanswerable questions: true if the answer gives a substantive answer instead of only "
                    "saying the corpus does not cover it; false for answerable questions")
    claims_not_in_passages: list[str] = Field(
        description="every claim or citation in the answer that the retrieved passages do not state; empty if none")
    correct_reason: str
    correct: int = Field(description="1 or 0, following the rubric and the lists above")
    supported_reason: str
    supported: int = Field(description="1 if claims_not_in_passages is empty, else 0")


JUDGE_STEPS = """## Procedure (follow in this order)
1. Split the reference answer into its elements (each fact, number, condition, exception; for `multi`
   questions, the content of each passage). For an unanswerable question the single element is
   "says the indexed legislation does not cover the question".
2. For each element, decide whether the assistant answer states it. Missing = present false.
3. Unanswerable questions: set answers_as_if_covered = true if the answer goes on to give a substantive
   answer (rules, obligations, articles) rather than only saying it is not covered and where to look.
4. Read every claim and citation in the assistant answer and list those the retrieved passages do not state.
5. correct = 1 only if every element is present and nothing contradicts the reference; for unanswerable
   questions, only if the answer says it is not covered and answers_as_if_covered is false. Otherwise 0.
6. supported = 1 only if the list from step 4 is empty."""


def judge_one(q: dict, a: dict, rubric: str) -> dict:
    from google.genai import types
    from ingest import _gemini
    prompt = (f"You are grading an answer of a legal question-answering assistant. Be strict.\n\n{rubric}\n\n"
              f"{JUDGE_STEPS}\n\n"
              f"## Item to grade\n\nQuestion kind: {q['kind']}\n\nQuestion: {q['question']}\n\n"
              f"Reference answer: {q['reference_answer']}\n\n"
              f"Retrieved passages:\n<<<\n{a['retrieved_text'] or '(the assistant did not search)'}\n>>>\n\n"
              f"Assistant answer:\n<<<\n{a['answer']}\n>>>")
    for attempt in range(5):
        try:
            r = _gemini().models.generate_content(
                model=JUDGE_MODEL, contents=prompt,
                config=types.GenerateContentConfig(temperature=0, response_mime_type="application/json",
                                                   response_schema=Verdict))
            v = Verdict.model_validate_json(r.text)
            u = r.usage_metadata
            return {**v.model_dump(), "judge_tokens": u.total_token_count}
        except Exception as e:  # noqa: BLE001 - rate limits and the odd malformed reply: wait and retry
            print(f"  judge {q['id']}: {type(e).__name__}, retrying", file=sys.stderr, flush=True)
            time.sleep(15 * (attempt + 1))
    raise RuntimeError(f"Judge failed on {q['id']}")


def run_judge(questions: list[dict], answers: dict) -> dict[str, dict]:
    rubric = RUBRIC.read_text(encoding="utf-8")
    rubric_hash = hashlib.sha256((rubric + JUDGE_VERSION + JUDGE_STEPS).encode()).hexdigest()[:12]
    have = read_jsonl(JUDGMENTS)
    for q in questions:
        a = answers[q["id"]]
        key = hashlib.sha256((a["answer"] + rubric_hash).encode()).hexdigest()[:16]
        if q["id"] in have and have[q["id"]].get("key") == key:
            continue
        v = judge_one(q, a, rubric)
        append_jsonl(JUDGMENTS, {"id": q["id"], "key": key, "model": JUDGE_MODEL, "version": JUDGE_VERSION, **v})
        print(f"  judged {q['id']}: correct={v['correct']} supported={v['supported']}", file=sys.stderr, flush=True)
    return read_jsonl(JUDGMENTS)   # last line per id wins


def kappa(a: list[int], b: list[int]) -> float | None:
    """Cohen's kappa for two binary raters."""
    n = len(a)
    if n == 0:
        return None
    po = sum(x == y for x, y in zip(a, b)) / n
    pa, pb = sum(a) / n, sum(b) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return None if pe == 1 else round((po - pe) / (1 - pe), 3)


def agreement(judgments: dict) -> pd.DataFrame | None:
    if not HUMAN.is_file():
        return None
    human = pd.read_csv(HUMAN, dtype={"id": str}).dropna(subset=["id"])
    human = human[human["id"].str.strip() != ""]
    if human.empty:
        return None
    rows, disagreements = [], []
    for crit in ("correct", "supported"):
        pairs = [(int(h[crit]), int(judgments[h["id"]][crit])) for _, h in human.iterrows()
                 if h["id"] in judgments and pd.notna(h[crit])]
        hs, js = [p[0] for p in pairs], [p[1] for p in pairs]
        rows.append({"criterion": crit, "n": len(pairs),
                     "agreement": round(sum(x == y for x, y in pairs) / len(pairs), 3) if pairs else None,
                     "kappa": kappa(hs, js), "human_rate": round(sum(hs) / len(hs), 3) if hs else None,
                     "judge_rate": round(sum(js) / len(js), 3) if js else None})
        for _, h in human.iterrows():
            j = judgments.get(h["id"])
            if j and pd.notna(h[crit]) and int(h[crit]) != int(j[crit]):
                disagreements.append({"id": h["id"], "criterion": crit, "human": int(h[crit]), "judge": int(j[crit]),
                                      "human_notes": h.get("notes", ""), "judge_reason": j[f"{crit}_reason"]})
    pd.DataFrame(disagreements).to_csv(EVAL / "disagreements.csv", index=False)
    df = pd.DataFrame(rows)
    df.to_csv(EVAL / "agreement.csv", index=False)
    return df


def summarise(checks: pd.DataFrame, judgments: dict) -> pd.DataFrame:
    df = checks.copy()
    df["correct"] = df["id"].map(lambda i: judgments.get(i, {}).get("correct"))
    df["supported"] = df["id"].map(lambda i: judgments.get(i, {}).get("supported"))
    df.to_csv(EVAL / "e2e_per_question.csv", index=False)
    answerable = df[df.kind != "unanswerable"]
    unanswerable = df[df.kind == "unanswerable"]
    summary = {
        "questions": len(df),
        "correct (judge)": f"{int(df.correct.sum())}/{len(df)}" if df.correct.notna().all() else "not judged",
        "correct answerable": f"{int(answerable.correct.sum())}/{len(answerable)}" if df.correct.notna().all() else "",
        "unsupported (judge)": f"{int((df.supported == 0).sum())}/{len(df)}" if df.supported.notna().all() else "not judged",
        "correct refusals": f"{(unanswerable.outcome == 'correct refusal').sum()}/{len(unanswerable)}",
        "wrong refusals": f"{(answerable.outcome == 'wrong refusal').sum()}/{len(answerable)}",
        "answered unanswerable": f"{(unanswerable.outcome == 'answered unanswerable').sum()}/{len(unanswerable)}",
        "citations not retrieved": int((df.citations_retrieved == 0).sum()),
        "citations not in index": int((df.citations_in_index == 0).sum()),
        "citation guardrail fired": int(df.guardrail_fired.sum()),
        "answers withheld": int(df.withheld.sum()),
        "mean tokens / question": round(df.total_tokens.mean()),
        "median tokens / question": round(df.total_tokens.median()),
        "mean seconds / question": round(df.seconds.mean(), 1),
        "median seconds / question": round(df.seconds.median(), 1),
        "mean searches / question": round(df.searches.mean(), 2),
    }
    out = pd.DataFrame(list(summary.items()), columns=["metric", "value"])
    out.to_csv(EVAL / "e2e_summary.csv", index=False)
    return out


def before_after(questions: list[dict], answers: dict) -> None:
    """NIS2 experiment: the saved 'before' answers vs answers after NIS2 was added with add_document."""
    if not nis2_indexed():
        print(f"NIS2 not indexed yet. Add it through the agent (you approve at the prompt):\n"
              f'  uv run python main.py ask "Please add the file {NIS2_FILE} to the index"')
        return
    picked = [q for q in questions if q["id"] in NIS2_QUESTIONS]
    after = collect_answers(picked, NIS2_AFTER)
    first_after = read_jsonl(EVAL / "nis2_after_v1.jsonl")   # before the corpus-description fix
    lines = ["# Before / after adding NIS2 (Directive (EU) 2022/2555) with add_document", "",
             "1. **Before**: index = GDPR, AI Act, Data Act.",
             "2. **After, first try**: NIS2 indexed and retrieved, but the search tool description and AGENTS.md "
             "still listed only three acts, so the agent treated NIS2 passages as outside the corpus.",
             "3. **After the fix**: every search result starts with the acts read from the index, and AGENTS.md says "
             "every listed act is part of the corpus.", ""]
    for q in picked:
        b, a = answers[q["id"]], after[q["id"]]
        lines += [f"## {q['id']}: {q['question']}", "",
                  f"**1. Before** (refused={b['refused']}; retrieved: {', '.join(b['retrieved']) or 'none'})", "",
                  b["answer"], ""]
        if q["id"] in first_after:
            f = first_after[q["id"]]
            lines += [f"**2. After, first try** (refused={f['refused']}; retrieved: {', '.join(f['retrieved']) or 'none'})", "",
                      f["answer"], ""]
        lines += [f"**3. After the fix** (refused={a['refused']}; cited: {', '.join(a['citations']) or 'none'})", "",
                  a["answer"], "", "---", ""]
    (EVAL / "before_after.md").write_text("\n".join(lines), encoding="utf-8")
    for q in picked:
        print(f"  {q['id']}: before refused={answers[q['id']]['refused']} -> after refused={after[q['id']]['refused']}, "
              f"cites {', '.join(after[q['id']]['citations']) or 'none'}")


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    p.add_argument("--stage", choices=["retrieval", "answers", "judge", "nis2", "all"], default="all")
    p.add_argument("--questions", type=Path, default=QUESTIONS)
    p.add_argument("--rerun-retrieval", action="store_true", help="recompute hit rates instead of reusing them")
    a = p.parse_args()

    questions = read_questions(a.questions)
    kinds = pd.Series([q["kind"] for q in questions]).value_counts().to_dict()
    print(f"{len(questions)} questions: {kinds}")

    if a.stage in ("retrieval", "all"):
        print("\n== Retrieval: hit rate at k (strict for multi: every expected passage in top k)")
        saved = EVAL / "retrieval_summary.csv"
        if saved.is_file() and not a.rerun_retrieval and a.stage == "all":
            print("(saved results, measured on the initial corpus before NIS2 was added; --rerun-retrieval to recompute)")
            summary = pd.read_csv(saved)
        else:
            summary = retrieval_eval(questions)
        print(summary.to_string(index=False))

    if a.stage in ("answers", "judge", "all"):
        print(f"\n== End to end: agent answers ({ANSWERS.name})")
        answers = collect_answers(questions)
        checks = code_checks(questions, answers)
        write_label_sheet(questions, answers)
        print(f"Code checks saved; grading sheet for humans: {LABEL_SHEET.relative_to(ROOT)}")
        judgments = {}
        if a.stage in ("judge", "all"):
            print(f"\n== LLM judge ({JUDGE_MODEL}, rubric {RUBRIC.name})")
            judgments = run_judge(questions, answers)
            ag = agreement(judgments)
            print("\n== Judge vs human labels")
            print(ag.to_string(index=False) if ag is not None else "no human labels yet (eval/human_labels.csv)")
        print("\n== Summary")
        print(summarise(checks, judgments).to_string(index=False))

    if a.stage in ("nis2", "all"):
        print("\n== Before / after adding NIS2")
        before_after(questions, read_jsonl(ANSWERS))

    failures = EVAL / "failures.csv"   # human classification of every question I graded 0 (Phase 8)
    if a.stage == "all" and failures.is_file():
        f = pd.read_csv(failures)
        causes = ["retrieval miss", "wrong answer from right passage", "unsupported claim", "wrong refusal", "bad test question"]
        print(f"\n== Failures by cause ({len(f)} questions with correct=0 or supported=0 in my labels)")
        for c in causes:
            ids = ", ".join(f.loc[f.cause == c, "id"])
            print(f"  {c:32} {int((f.cause == c).sum())}  {ids}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
