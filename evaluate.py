"""
Assignment 3: evaluation (`uv run python main.py evaluate`).

    uv run python evaluate.py                 # retrieval + end-to-end (resumes saved answers)
    uv run python evaluate.py --fresh         # re-ask every question
    uv run python evaluate.py --before-after  # step 8: add the held-back document (on a copy)

Part 1, retrieval: hit rate at k = 1, 3, 5 for every design in index.DESIGNS, on
the answerable questions of eval/questions.csv.
Part 2, end-to-end: the agent answers every question; code checks what code can
check; an LLM judge grades the rest against a rubric; agreement with
eval/human_labels.csv is reported once you have graded.

Hit definition. A retrieved chunk is correct when it comes from the expected
document AND matches the expected location:
  - "Art. 33.2"          -> chunk's section is Article 33, or its text contains "33.2."
  - "III.3.1 ..." "IV.2" -> chunk's section is III.3 / IV.2, or its text contains the number
  - "(p. 3)"             -> chunk's pages include page 3
  - a section name       -> chunk heading is part of the name, or the name's first
                            words appear in the chunk's section or text
  - for 4 questions whose heading was lost in extraction, a chunk containing the
    key fact of the reference answer (EVIDENCE below)
A single question is a hit at k if any of the top-k chunks is correct.
A multi question has one part per document (";" with no space separates parts):
  hit@k  = at least one part found in the top k
  full@k = every part found in the top k

Query vectors are cached in eval/query_vectors.json, so re-runs cost no embeddings.
Outputs: eval/retrieval_per_question.csv, eval/retrieval_summary.csv.
"""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import index as ix  # noqa: E402

EVAL_DIR = ROOT / "eval"
QUESTIONS = EVAL_DIR / "questions.csv"
QUERY_CACHE = EVAL_DIR / "query_vectors.json"
KS = (1, 3, 5)

# Names used in questions.csv -> `source` in the chunk metadata.
SOURCE_ALIASES = {
    "attendance policy bachelor degrees 2026-2027": "Attendance Policy, Bachelor Programs",
    "general academic regulations for bachelor degree programmes": "Academic Regulations for Bachelor Degree Programmes",
    "general academic regulations for master degree programmes": "Academic Regulations for Master Degree Programmes",
    "the student code of conduct": "The IE Student Code of Conduct",
    "student guidelines for appropriate use of ai": "Student Guidelines on AI (v4)",
    "code for the prevention of harassment in the workplace": "Code for the Prevention of Harassment",
    "ie equal opportunities and diversity plan": "Equal Opportunities and Diversity Plan",
    "ie university environmental policy": "Environmental Policy",
    "climate and sustainability plan": "Climate and Sustainability Plan (CASP v3)",
}


def canonical_source(name: str) -> str:
    name = name.strip()
    titles = {d["title"] for d in ix.CORPUS}
    if name in titles:
        return name
    key = name.lower()
    if key not in SOURCE_ALIASES:
        raise ValueError(f"Unknown expected_source {name!r}: add it to SOURCE_ALIASES in evaluate.py")
    return SOURCE_ALIASES[key]


# ---------------------------------------------------------------------------
# Expected passages
# ---------------------------------------------------------------------------
ART = re.compile(r"Art\.?\s*(\d+)(?:\.(\d+))?")
ROMAN = re.compile(r"\b([IVX]+\.\d+)((?:\.\d+)*)")
PAGE = re.compile(r"\(p\.\s*(\d+)\)")


def parse_parts(row: dict) -> list[dict]:
    """One part per expected document, each with the location strings that count."""
    sources = [s for s in re.split(r";(?! )", row["expected_source"]) if s.strip()]
    locations = [l for l in re.split(r";(?! )", row["expected_location"]) if l.strip()]
    if len(sources) == 1:
        locations = [" ; ".join(locations)]
    if len(locations) != len(sources):
        raise ValueError(f"{row['id']}: {len(sources)} sources but {len(locations)} locations")
    return [
        {"qid": row["id"], "source": canonical_source(s), "location": l.strip()} for s, l in zip(sources, locations)
    ]


def _norm(text: str) -> str:
    text = unicodedata_normalise(text).lower()
    return re.sub(r"[^a-z0-9.]+", " ", text).strip()


def unicodedata_normalise(text: str) -> str:
    import unicodedata

    return unicodedata.normalize("NFKC", text).replace("’", "'")


def location_matches(location: str, meta: dict, text: str) -> bool:
    section, heading = meta.get("section", ""), meta.get("heading", "")
    arts, romans, pages = ART.findall(location), ROMAN.findall(location), PAGE.findall(location)

    if arts or romans or pages:
        for art, sub in arts:
            if re.search(rf"\bArticle {art}\.", section) or (sub and f"{art}.{sub}." in text):
                return True
        for prefix, rest in romans:
            if f"{prefix}." in section or f"{prefix}{rest}" in text:
                return True
        for page in pages:
            if meta["page_start"] <= int(page) <= meta["page_end"]:
                return True
        return False

    # named section: any "; "-separated piece may match
    for piece in re.split(r";\s*", location):
        piece_n = _norm(piece)
        if not piece_n:
            continue
        heading_n = _norm(heading)
        if heading_n and len(heading_n) >= 4 and heading_n in piece_n:
            return True
        lead = " ".join(piece_n.split()[:3])
        if lead and (lead in _norm(section) or lead in _norm(text)):
            return True
    return False


# Where the expected location names a heading the PDF extraction lost or mangled
# (CASP's headings, the harassment code's categories, "CLASS ATTENDANCE"), the
# label cannot match any chunk metadata. For those questions a chunk from the right
# document that contains the key fact of the reference answer also counts.
EVIDENCE = {
    "q01": r"below 80%",
    "q43": r"at least once a week",
    "q45": r"grew by 64%",
    "q46": r"60% of suppliers",
}


def is_relevant(part: dict, meta: dict, text: str) -> bool:
    if meta["source"] != part["source"]:
        return False
    if location_matches(part["location"], meta, text):
        return True
    pattern = EVIDENCE.get(part.get("qid", ""))
    return bool(pattern and re.search(pattern, text))


# ---------------------------------------------------------------------------
# Retrieval
# ---------------------------------------------------------------------------
def load_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def query_vectors(questions: list[dict]) -> dict[str, list[float]]:
    """Embed each question once and cache it; changing designs costs nothing."""
    cache = json.loads(QUERY_CACHE.read_text()) if QUERY_CACHE.exists() else {}
    key = lambda q: f"{ix.EMBED_MODEL}|{ix.EMBED_DIM}|{q}"  # noqa: E731
    missing = [q["question"] for q in questions if key(q["question"]) not in cache]
    for start in range(0, len(missing), ix.EMBED_BATCH):
        batch = missing[start : start + ix.EMBED_BATCH]
        for q, v in zip(batch, ix.embed_texts(batch, task_type="RETRIEVAL_QUERY")):
            cache[key(q)] = v
        QUERY_CACHE.write_text(json.dumps(cache))
    return {q["question"]: cache[key(q["question"])] for q in questions}


def first_hit_rank(part: dict, results: list[tuple[dict, str]]) -> int | None:
    for rank, (meta, text) in enumerate(results, start=1):
        if is_relevant(part, meta, text):
            return rank
    return None


def evaluate_retrieval() -> list[dict]:
    questions = [q for q in load_questions() if q["kind"] != "unanswerable"]
    vectors = query_vectors(load_questions())  # embed all, the agent eval reuses them
    k_max = max(KS)
    rows, summary = [], []

    for design in ix.DESIGNS:
        collection = ix.get_collection(design)
        everything = collection.get(include=["metadatas", "documents"])
        for q in questions:
            parts = parse_parts(q)
            gold = sum(
                1
                for m, d in zip(everything["metadatas"], everything["documents"])
                if any(is_relevant(p, m, d) for p in parts)
            )
            res = collection.query(query_embeddings=[vectors[q["question"]]], n_results=k_max)
            results = list(zip(res["metadatas"][0], res["documents"][0]))
            ranks = [first_hit_rank(p, results) for p in parts]
            found = [r for r in ranks if r is not None]
            row = {
                "design": design,
                "id": q["id"],
                "kind": q["kind"],
                "gold_chunks": gold,
                "first_hit_rank": min(found) if found else "",
                "all_parts_rank": max(ranks) if all(r is not None for r in ranks) else "",
                "top1": f"{results[0][0]['source']} | {results[0][0]['location']}",
            }
            for k in KS:
                row[f"hit@{k}"] = int(bool(found) and min(found) <= k)
                row[f"full@{k}"] = int(all(r is not None and r <= k for r in ranks))
            for k in (3, 5):
                row[f"words@{k}"] = sum(len(d.split()) for _, d in results[:k])
            rows.append(row)

        mine = [r for r in rows if r["design"] == design]
        for kind in ("all", "single", "multi"):
            sel = mine if kind == "all" else [r for r in mine if r["kind"] == kind]
            line = {"design": design, "questions": kind, "n": len(sel)}
            for k in KS:
                line[f"hit@{k}"] = round(sum(r[f"hit@{k}"] for r in sel) / len(sel), 3)
            if kind == "multi":
                for k in KS:
                    line[f"full@{k}"] = round(sum(r[f"full@{k}"] for r in sel) / len(sel), 3)
            for k in (3, 5):
                line[f"avg_words@{k}"] = round(sum(r[f"words@{k}"] for r in sel) / len(sel))
            summary.append(line)

    write_csv(EVAL_DIR / "retrieval_per_question.csv", rows)
    write_csv(EVAL_DIR / "retrieval_summary.csv", summary)
    print_summary(summary)
    no_gold = sorted({(r["id"], r["design"]) for r in rows if r["gold_chunks"] == 0})
    if no_gold:
        print(f"\nWARNING: no chunk matches the expected location for: {no_gold}")
    return summary


def write_csv(path: Path, rows: list[dict]) -> None:
    fields = list(dict.fromkeys(k for r in rows for k in r))
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def print_summary(summary: list[dict]) -> None:
    print("\nRetrieval hit rate (answerable questions)")
    print(f"{'design':12} {'questions':9} {'n':>3}  {'hit@1':>6} {'hit@3':>6} {'hit@5':>6}  {'full@5':>6}  {'words@3':>7} {'words@5':>7}")
    for s in summary:
        full = f"{s['full@5']:.2f}" if "full@5" in s else ""
        print(
            f"{s['design']:12} {s['questions']:9} {s['n']:>3}  {s['hit@1']:>6.2f} {s['hit@3']:>6.2f} {s['hit@5']:>6.2f}"
            f"  {full:>6}  {s['avg_words@3']:>7} {s['avg_words@5']:>7}"
        )


# ===========================================================================
# Part 2: end-to-end
# ===========================================================================
ANSWERS = EVAL_DIR / "answers.jsonl"  # one agent result per line, saved as it comes
VERDICTS = EVAL_DIR / "judge_verdicts.jsonl"
RESULTS = EVAL_DIR / "end_to_end.csv"
SUMMARY = EVAL_DIR / "end_to_end_summary.json"
GRADING_SHEET = EVAL_DIR / "grading_sheet.csv"
HUMAN_LABELS = EVAL_DIR / "human_labels.csv"
AGREEMENT = EVAL_DIR / "judge_agreement.json"
BEFORE_AFTER = EVAL_DIR / "before_after.json"

JUDGE_MODEL = "gemini-3.5-flash-lite"  # not the agent's model, to avoid grading its own answers

JUDGE_RUBRIC = """\
You grade answers from an assistant that answers IE University students' questions
using only official IE documents. A wrong answer can cost a student a course;
saying "I can't find this" only costs a few minutes.

Grade two things, each 0 or 1.

correct
- Answerable question (kind single or multi): 1 if the answer gives the key facts of
  the reference answer (numbers, deadlines, percentages, conditions, who decides,
  where to submit) and says nothing that contradicts it. A missing minor detail is
  fine; a missing key fact, a wrong fact, or a refusal is 0. For a multi question,
  both parts must be answered.
- Unanswerable question: 1 if the assistant says it cannot find the answer (or
  declines the specific point) and does not state the missing fact as true.
  Giving a definite answer to the missing point is 0.

supported
- 1 if every factual claim in the answer is stated in the retrieved passages below
  (paraphrase is fine). 0 if any claim is not in them, even if it happens to be true.
- A refusal that adds no claims is supported.

Reply with JSON only: {"correct": 0 or 1, "supported": 0 or 1, "reason": "one sentence"}
"""


def read_jsonl(path: Path) -> dict[str, dict]:
    if not path.exists():
        return {}
    rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]
    return {r["id"]: r for r in rows}


def append_jsonl(path: Path, row: dict) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


class SearchFailed(RuntimeError):
    pass


async def run_agent(questions: list[dict], fresh: bool = False) -> dict[str, dict]:
    """Ask every question once; results are appended to answers.jsonl as they arrive."""
    import asyncio

    from agent import CorpusAgent

    if fresh and ANSWERS.exists():
        ANSWERS.unlink()
    done = read_jsonl(ANSWERS)
    todo = [q for q in questions if q["id"] not in done]
    if not todo:
        return done
    print(f"\nAsking the agent {len(todo)} question(s) ({len(done)} already saved) ...", flush=True)
    async with CorpusAgent(approve=lambda name, args: False) as agent:
        for q in todo:
            for attempt in range(3):
                try:
                    result = await agent.ask(q["question"])
                    break
                except Exception as exc:  # model overloaded / rate limited: wait and retry
                    if attempt == 2:
                        raise
                    print(f"  {q['id']}: {type(exc).__name__}, retrying in 30s", flush=True)
                    await asyncio.sleep(30)
            # a failed search (e.g. daily embedding quota) would look like a refusal: stop instead
            if any(str(t.get("output", "")).startswith("ERROR") for t in result["trace"] if t["tool"] == "search"):
                raise SearchFailed(f"{q['id']}: the search tool failed ({result['trace']}). Run again later.")
            result.update({"id": q["id"], "kind": q["kind"]})
            append_jsonl(ANSWERS, result)
            done[q["id"]] = result
            print(f"  {q['id']} [{result['guardrail']}] {result['seconds']}s {result['answer'][:90]!r}", flush=True)
    return done


def cited_sources(answer: str) -> set[str]:
    titles = [d["title"] for d in ix.CORPUS]
    return {t for t in titles if t.lower() in answer.lower()}


def code_checks(q: dict, r: dict) -> dict:
    """What code can check without judging meaning."""
    unanswerable = q["kind"] == "unanswerable"
    checks = {
        "refused": int(r["is_refusal"]),
        "refusal_ok": int(r["is_refusal"] == unanswerable),
        "citations_valid": int(r["guardrail"] in {"ok", "refusal"} and not r["invalid_citations"]),
        "guardrail_fired": int(r["guardrail"].startswith("blocked")),
    }
    if not unanswerable:
        expected = {p["source"] for p in parse_parts(q)}
        checks["cites_expected_source"] = int(bool(expected & cited_sources(r["answer"])))
    return checks


def judge(q: dict, r: dict) -> dict:
    """LLM judge with the rubric above; the retrieved passages are the evidence."""
    import time

    from google.genai import errors, types

    passages = "\n\n".join(r["search_outputs"])[:24000] or "(no search was made)"
    prompt = (
        f"{JUDGE_RUBRIC}\n"
        f"Question kind: {q['kind']}\n"
        f"Question: {q['question']}\n"
        f"Reference answer: {q['reference_answer']}\n\n"
        f"Assistant answer:\n{r['answer']}\n\n"
        f"Retrieved passages:\n{passages}\n"
    )
    config = types.GenerateContentConfig(response_mime_type="application/json")
    for attempt in range(5):
        try:
            resp = ix.genai_client().models.generate_content(model=JUDGE_MODEL, contents=prompt, config=config)
            verdict = json.loads(resp.text)
            return {
                "correct": int(verdict["correct"]),
                "supported": int(verdict["supported"]),
                "reason": verdict.get("reason", ""),
                "judge_tokens": getattr(resp.usage_metadata, "total_token_count", 0) or 0,
            }
        except (errors.APIError, json.JSONDecodeError, KeyError) as exc:
            if attempt == 4:
                raise
            print(f"  judge {q['id']}: {type(exc).__name__}, retrying", flush=True)
            time.sleep(20 * (attempt + 1))
    raise RuntimeError("unreachable")


def run_judge(questions: list[dict], answers: dict[str, dict], fresh: bool = False) -> dict[str, dict]:
    if fresh and VERDICTS.exists():
        VERDICTS.unlink()
    verdicts = read_jsonl(VERDICTS)
    for q in questions:
        r = answers[q["id"]]
        # re-judge if the answer changed since the verdict was saved
        if q["id"] in verdicts and verdicts[q["id"]].get("answer") == r["answer"]:
            continue
        v = {"id": q["id"], "answer": r["answer"], **judge(q, r)}
        append_jsonl(VERDICTS, v)
        verdicts[q["id"]] = v
    return verdicts


def classify(q: dict, checks: dict, verdict: dict) -> str:
    unanswerable = q["kind"] == "unanswerable"
    if unanswerable:
        return "correct refusal" if checks["refused"] else "answered unanswerable"
    if checks["refused"]:
        return "wrong refusal"
    if not verdict["supported"]:
        return "unsupported"
    return "correct" if verdict["correct"] else "incorrect"


def write_grading_sheet(questions: list[dict], answers: dict[str, dict]) -> None:
    """For your own grades: everything you need, but NOT the judge's verdicts."""
    rows = []
    for q in questions:
        r = answers[q["id"]]
        rows.append(
            {
                "id": q["id"],
                "kind": q["kind"],
                "question": q["question"],
                "reference_answer": q["reference_answer"],
                "agent_answer": r["answer"],
                "retrieved_passages": "\n\n".join(r["search_outputs"])[:6000],
            }
        )
    write_csv(GRADING_SHEET, rows)


def human_agreement(rows: list[dict]) -> dict | None:
    if not HUMAN_LABELS.exists():
        return None
    with HUMAN_LABELS.open(newline="", encoding="utf-8") as f:
        labels = {r["id"].strip(): r for r in csv.DictReader(f) if (r.get("id") or "").strip()}
    by_id = {r["id"]: r for r in rows}
    pairs = [(labels[i], by_id[i]) for i in labels if i in by_id]
    if not pairs:
        return None
    result = {"graded": len(pairs)}
    for field in ("correct", "supported"):
        both = [(int(h[field]), int(j[f"judge_{field}"])) for h, j in pairs if h.get(field, "").strip() in {"0", "1"}]
        agree = sum(1 for a, b in both if a == b)
        result[f"{field}_agreement"] = round(agree / len(both), 3) if both else None
        result[f"{field}_disagreements"] = [h["id"] for h, j in pairs if h.get(field, "").strip() in {"0", "1"} and int(h[field]) != int(j[f"judge_{field}"])]
    AGREEMENT.write_text(json.dumps(result, indent=2))
    return result


def evaluate_end_to_end(fresh: bool = False) -> dict:
    import asyncio

    questions = load_questions()
    answers = asyncio.run(run_agent(questions, fresh))
    verdicts = run_judge(questions, answers, fresh)

    rows = []
    for q in questions:
        r, v = answers[q["id"]], verdicts[q["id"]]
        checks = code_checks(q, r)
        rows.append(
            {
                "id": q["id"],
                "kind": q["kind"],
                "outcome": classify(q, checks, v),
                **checks,
                "judge_correct": v["correct"],
                "judge_supported": v["supported"],
                "judge_reason": v["reason"],
                "guardrail": r["guardrail"],
                "searches": r["searches"],
                "tokens": r["tokens"]["total"],
                "seconds": r["seconds"],
                "answer": r["answer"],
            }
        )
    write_csv(RESULTS, rows)
    write_grading_sheet(questions, answers)

    n = len(rows)
    answerable = [r for r in rows if r["kind"] != "unanswerable"]
    unanswerable = [r for r in rows if r["kind"] == "unanswerable"]
    count = lambda rs, outcome: sum(1 for r in rs if r["outcome"] == outcome)  # noqa: E731
    summary = {
        "questions": n,
        "agent_model": answers[questions[0]["id"]]["model"],
        "judge_model": JUDGE_MODEL,
        "answerable": len(answerable),
        "correct": count(answerable, "correct"),
        "incorrect": count(answerable, "incorrect"),
        "unsupported": count(answerable, "unsupported"),
        "wrong_refusals": count(answerable, "wrong refusal"),
        "unanswerable": len(unanswerable),
        "correct_refusals": count(unanswerable, "correct refusal"),
        "answered_unanswerable": count(unanswerable, "answered unanswerable"),
        "citations_valid_rate": round(sum(r["citations_valid"] for r in rows) / n, 3),
        "guardrail_fired": sum(r["guardrail_fired"] for r in rows),
        "cites_expected_source_rate": round(
            sum(r["cites_expected_source"] for r in answerable) / len(answerable), 3
        ),
        "avg_tokens_per_question": round(sum(r["tokens"] for r in rows) / n),
        "avg_seconds_per_question": round(sum(r["seconds"] for r in rows) / n, 1),
        "avg_searches_per_question": round(sum(r["searches"] for r in rows) / n, 2),
    }
    agreement = human_agreement(rows)
    if agreement:
        summary["human_agreement"] = agreement
    SUMMARY.write_text(json.dumps(summary, indent=2))

    print("\nEnd-to-end results")
    for k, v in summary.items():
        print(f"  {k}: {v}")
    if not agreement:
        print(f"\nGrade 20+ answers in {HUMAN_LABELS.name} (use {GRADING_SHEET.name}), then run again for agreement.")
    return summary


# ===========================================================================
# Step 8: add a held-back document and ask again (on a copy of the index)
# ===========================================================================
HELD_BACK = ROOT / "extra" / "Attendance_Policy_Master_Programs.pdf"
HELD_BACK_URL = "https://docs.ie.edu/documents/Attendance_Policy_Master_Programs.pdf"
BEFORE_AFTER_IDS = ["q36", "q37", "q38", "q39", "q40"]  # the master's attendance questions


def before_after() -> None:
    """Add the master's attendance policy with the add_document tool and re-ask.

    It runs on a copy of index/, so the committed index (and the main evaluation)
    stays the original corpus. "Before" answers come from eval/answers.jsonl.
    """
    import asyncio
    import os
    import shutil
    import tempfile

    import httpx

    from agent import CorpusAgent

    if not HELD_BACK.exists():
        HELD_BACK.parent.mkdir(exist_ok=True)
        HELD_BACK.write_bytes(httpx.get(HELD_BACK_URL, follow_redirects=True, timeout=120).content)
    before = read_jsonl(ANSWERS)
    questions = {q["id"]: q for q in load_questions()}

    with tempfile.TemporaryDirectory() as tmp:
        copy = Path(tmp) / "chroma"
        shutil.copytree(ix.CHROMA_DIR, copy)
        os.environ["CORPUS_INDEX_DIR"] = str(copy)

        async def run() -> dict:
            async with CorpusAgent(approve=lambda name, args: True) as agent:
                added = await agent.ask(f"Please add the document {HELD_BACK.relative_to(ROOT)} to the corpus.")
                after = {i: await agent.ask(questions[i]["question"]) for i in BEFORE_AFTER_IDS}
            return {"add_document": added, "after": after}

        out = asyncio.run(run())

    report = {
        "document": HELD_BACK.name,
        "add_document_trace": out["add_document"]["trace"],
        "approvals": out["add_document"]["approvals"],
        "questions": [
            {
                "id": i,
                "question": questions[i]["question"],
                "before": before.get(i, {}).get("answer"),
                "after": out["after"][i]["answer"],
                "after_guardrail": out["after"][i]["guardrail"],
            }
            for i in BEFORE_AFTER_IDS
        ],
    }
    BEFORE_AFTER.write_text(json.dumps(report, indent=2, ensure_ascii=False))
    for item in report["questions"]:
        print(f"\n=== {item['id']}: {item['question']}\nBEFORE: {item['before']}\nAFTER:  {item['after']}")


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("--fresh", action="store_true", help="re-ask and re-judge every question")
    parser.add_argument("--before-after", action="store_true", help="add the held-back document (on a copy) and re-ask")
    args = parser.parse_args()
    if args.before_after:
        before_after()
        return
    evaluate_retrieval()
    evaluate_end_to_end(fresh=args.fresh)


if __name__ == "__main__":
    main()
