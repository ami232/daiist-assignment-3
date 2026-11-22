"""
Assignment 3: evaluation (`uv run python main.py evaluate`).

1. Retrieval: hit rate at 1/3/5 for design a and design b on the answerable questions,
   plus the words each design adds to the prompt (top 5 passages).
2. Agent: runs agent.py on every question (answers are saved in eval/agent_answers.json,
   so a re-run only does what is missing; use --force to redo everything).
3. Code checks: citations present and valid, refusal detected, expected passage cited.
4. LLM judge: rubric + question + reference answer + the retrieved passages as evidence.
5. Human labels: agreement with eval/human_labels.csv (your own grades).
6. Before/after: adds one document that answers an unanswerable question, asks again.
7. Failure candidates, cost per question, and a summary in eval/summary.md.

Results land in eval/. Run the stages again at any time: finished work is reused.
"""

import argparse
import csv
import json
import os
import re
import statistics
import sys
import time
from pathlib import Path

import index
from agent import _normalise, _numbers, retrieved_locations, run_agent
from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
HUMAN_LABELS = EVAL / "human_labels.csv"
ANSWERS = EVAL / "agent_answers.json"
VERDICTS = EVAL / "judge_verdicts.json"
BEFORE_AFTER = EVAL / "before_after.json"
JUDGE_MODEL = os.environ.get("JUDGE_MODEL", "gemini-3.5-flash-lite")

# The document added in the before/after test, and the unanswerable question it answers.
ADDED_DOC = ROOT / "corpus" / "edpb_video_devices.pdf"
ADDED_URL = "https://www.edpb.europa.eu/sites/default/files/files/file1/edpb_guidelines_201903_video_devices_en_0.pdf"
BEFORE_AFTER_QUESTION = "q19"

CITE_RE = re.compile(r"\[([a-z_0-9]+),\s*([^\]]+)\]")
REFUSAL_RE = re.compile(
    r"((corpus|documents?|passages?|guidelines|texts?) (does|do|did) (not|n't) "
    r"(cover|contain|include|address|mention|provide|specify|discuss|say|answer))"
    r"|((is|are) not (covered|addressed|mentioned) (in|by) the (corpus|documents?|passages?|guidelines))"
    r"|cannot (answer|be answered)|can't answer|unable to (find|answer)"
    r"|no (relevant )?(information|passages?) (is |are |was |were )?(found|available|provided)"
    r"|(is|are) not (part of|in) the (corpus|documents?)",
    re.I,
)

RUBRIC = """You are grading an answer from a question-answering assistant that may only use a
small corpus of EU data-protection documents (the GDPR, EDPB Guidelines 9/2022 on breach
notification, EDPB Guidelines 07/2020 on controller and processor). You get the question, its
kind, a reference answer written by the test author, the passages the assistant retrieved
(the only evidence it was allowed to use) and the assistant's answer.

Grade two things, each 1 or 0.

correct
- Answerable question (kind single or multi): 1 if the answer gives the key facts of the
  reference answer and nothing in it contradicts the reference. Extra correct detail is fine.
  0 if a key fact is missing (for a multi question, if one of the two required parts is
  missing), if it contradicts the reference, or if it refuses although the corpus covers it.
- Unanswerable question (kind unanswerable): 1 if the answer clearly says the documents do
  not cover the question and does not present anything from outside the documents as the
  answer. Mentioning a related provision is fine if it is clearly presented as only related.
  0 if the answer treats the question as answered.

supported
- 1 if every factual claim in the answer is stated in the retrieved passages and every
  citation points to a retrieved passage. A refusal that makes no factual claim is 1.
- 0 if any claim relies on knowledge that is not in the retrieved passages, or a citation
  points to something that was not retrieved.

Important rules
- An answer that says "the corpus does not mention / cover this" is a refusal, whatever else it adds.
  For an answerable question (single or multi) a refusal is ALWAYS correct = 0: the test author
  guarantees the answer is in the corpus (see WHERE THE ANSWER IS).
- For an unanswerable question, an answer that gives a substantive answer (even a "general
  principle") instead of saying the documents do not cover it is correct = 0.
- Compare the key facts of the answer with the reference answer one by one before deciding.
- Do not reward length or confidence. Judge only what is written.

Reply with JSON only, writing the reasoning FIRST:
{"reason": "compare the answer with the reference, fact by fact, in one or two sentences",
 "correct": 0 or 1, "supported": 0 or 1}"""


# ---------------------------------------------------------------- small helpers

def load_json(path: Path) -> dict:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def save_json(path: Path, data) -> None:
    path.parent.mkdir(exist_ok=True)
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False), encoding="utf-8")


def read_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if (r.get("id") or "").strip()]


def expected_pairs(row: dict) -> list[tuple[str, str]]:
    """[(source, location)] a question needs, from the ;-separated columns."""
    sources = [s.strip() for s in row["expected_source"].split(";") if s.strip()]
    locations = [s.strip() for s in row["expected_location"].split(";") if s.strip()]
    if not sources:
        return []
    if len(sources) == 1 and len(locations) > 1:
        sources = sources * len(locations)
    if len(locations) == 1 and len(sources) > 1:
        locations = locations * len(sources)
    return list(zip(sources, locations))


def loc_match(exp_source: str, exp_loc: str, source: str, loc: str) -> bool:
    """Same source and the same place.
    'para 33 (p.11)' matches 'paras 31-33 (p.11)' (design b) and also a chunk labelled only
    'p.11' or 'p.10 to p.11' (design a on PDFs); 'Article 33' matches 'Article 33 part 2'."""
    if exp_source != source:
        return False
    chunk = _normalise(loc)
    if chunk.startswith("p."):                      # chunk labelled by page only
        pages = [int(n) for n in re.findall(r"p\.(\d+)", chunk)]
        page = re.search(r"\(p\.(\d+)", _normalise(exp_loc))
        return bool(pages and page and min(pages) <= int(page.group(1)) <= max(pages))
    if _normalise(exp_loc).startswith("article") != chunk.startswith("article"):
        return False
    wanted = _numbers(exp_loc)
    return (not wanted) or bool(wanted & _numbers(loc))


def covers(pairs: list[tuple[str, str]], found: list[tuple[str, str]]) -> bool:
    """Every expected (source, location) is matched by something in `found`."""
    return bool(pairs) and all(any(loc_match(es, el, s, l) for s, l in found) for es, el in pairs)


def mean(values) -> float:
    values = list(values)
    return sum(values) / len(values) if values else 0.0


# ---------------------------------------------------------------- 1. retrieval

def retrieval_eval(rows: list[dict]) -> dict:
    answerable = [r for r in rows if r["kind"].strip().lower() != "unanswerable"]
    out = {}
    per_question = []
    for design in index.DESIGNS:
        collection = index.get_collection(design)
        if collection.count() == 0:
            print(f"  design {design}: empty index, skipped")
            continue
        hits = {1: 0, 3: 0, 5: 0}
        by_kind: dict[str, dict[int, int]] = {}
        words = []
        for row in answerable:
            vector = index.embed_query(row["question"])
            result = collection.query(query_embeddings=[vector], n_results=5, include=["documents", "metadatas"])
            found = [(m["source"], m["location"]) for m in result["metadatas"][0]]
            words.append(sum(len(d.split()) for d in result["documents"][0]))
            pairs = expected_pairs(row)
            kind = by_kind.setdefault(row["kind"], {1: 0, 3: 0, 5: 0, "n": 0})
            kind["n"] += 1
            record = {"design": design, "id": row["id"], "kind": row["kind"]}
            for k in (1, 3, 5):
                hit = covers(pairs, found[:k])
                hits[k] += hit
                kind[k] += hit
                record[f"hit@{k}"] = int(hit)
            record["top5"] = " | ".join(f"{s}:{l}" for s, l in found)
            per_question.append(record)
        n = len(answerable)
        out[design] = {
            "chunks": collection.count(),
            "questions": n,
            "hit@1": hits[1] / n,
            "hit@3": hits[3] / n,
            "hit@5": hits[5] / n,
            "avg_words_in_prompt_top5": round(mean(words)),
            "by_kind": {k: {"n": v["n"], **{f"hit@{j}": v[j] / v["n"] for j in (1, 3, 5)}} for k, v in by_kind.items()},
        }
    with (EVAL / "retrieval_per_question.csv").open("w", newline="", encoding="utf-8") as f:
        fields = ["design", "id", "kind", "hit@1", "hit@3", "hit@5", "top5"]
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(per_question)
    return out


# ---------------------------------------------------------------- 2. agent answers

def answer_all(rows: list[dict], force: bool) -> dict:
    """Answer every question. Done answers are kept; failed ones are retried in later rounds
    (the Gemini API sometimes answers 503 'high demand' for a few minutes)."""
    answers = {} if force else load_json(ANSWERS)
    for round_number in range(1, 6):
        missing = [r for r in rows if r["id"] not in answers]
        if not missing:
            break
        if round_number > 1:
            print(f"  round {round_number}: {len(missing)} question(s) left; waiting 60 s before retrying", flush=True)
            time.sleep(60)
        for row in missing:
            print(f"  {row['id']} ({row['kind']}): {row['question'][:70]}", flush=True)
            try:
                answers[row["id"]] = run_agent(row["question"], approve=lambda tool, args: False)
            except Exception as error:  # keep going; the next round retries this question
                print(f"    failed: {type(error).__name__}: {str(error)[:120]}", flush=True)
                continue
            save_json(ANSWERS, answers)
    for row in rows:
        if row["id"] not in answers:
            print(f"  WARNING {row['id']} has no answer yet. Run the evaluation again later to finish it.")
    return answers


# ---------------------------------------------------------------- 3. code checks

def code_checks(row: dict, result: dict) -> dict:
    answer = result.get("answer", "")
    cites = CITE_RE.findall(answer)
    pairs = expected_pairs(row)
    retrieved = list(retrieved_locations(result.get("trace", [])))
    searched = any(s["tool"] == "search" and s["status"] == "ok" for s in result.get("trace", []))
    refused = bool(REFUSAL_RE.search(answer))
    valid = "unsupported_citation" not in result.get("flags", [])
    check = {
        "searched": searched,
        "has_citation": bool(cites),
        "citations_valid": valid,
        "refused": refused,
        "expected_retrieved": covers(pairs, retrieved) if pairs else None,
        "expected_cited": covers(pairs, cites) if pairs else None,
    }
    if row["kind"].strip().lower() == "unanswerable":
        check["code_pass"] = refused
    else:
        check["code_pass"] = bool(cites and valid and not refused and check["expected_cited"])
    return check


# ---------------------------------------------------------------- 4. LLM judge

JUDGE_FALLBACKS = ["gemini-3.1-flash-lite", "gemini-flash-lite-latest", "gemini-3.8-flash"]


def judge_call(prompt: str) -> str:
    from google import genai
    from google.genai import types

    client = genai.Client(api_key=load_api_key())
    last_error = None
    for model in [JUDGE_MODEL, *[m for m in JUDGE_FALLBACKS if m != JUDGE_MODEL]]:
        for attempt in range(3):
            try:
                response = client.models.generate_content(
                    model=model,
                    contents=prompt,
                    config=types.GenerateContentConfig(temperature=0, response_mime_type="application/json"),
                )
                return response.text
            except Exception as error:
                last_error = error
                text = str(error)
                if not any(word in text for word in ("429", "503", "504", "UNAVAILABLE", "DEADLINE")):
                    raise
                delay = re.search(r"'retryDelay': '(\d+)s'", text)
                if "RESOURCE_EXHAUSTED" in text and delay and int(delay.group(1)) > 300:
                    break                      # daily quota used up: next model
                time.sleep(10 * (attempt + 1))
    raise last_error


def evidence_text(result: dict) -> str:
    parts = [s["result"] for s in result.get("trace", []) if s["tool"] == "search" and s["status"] == "ok"]
    text = "\n\n".join(parts) or "(no passages were retrieved)"
    return text[:16000]


def parse_verdict(text: str) -> dict:
    match = re.search(r"\{.*\}", text or "", re.S)
    data = json.loads(match.group()) if match else {}
    return {
        "correct": int(bool(int(data.get("correct", 0)))),
        "supported": int(bool(int(data.get("supported", 0)))),
        "reason": str(data.get("reason", ""))[:400],
    }


def judge_all(rows: list[dict], answers: dict, force: bool) -> dict:
    verdicts = {} if force else load_json(VERDICTS)
    for row in rows:
        qid = row["id"]
        if qid in verdicts or qid not in answers:
            continue
        result = answers[qid]
        prompt = (
            f"{RUBRIC}\n\n--- QUESTION ---\n{row['question']}\n\n--- KIND ---\n{row['kind']}\n\n"
            f"--- REFERENCE ANSWER ---\n{row['reference_answer']}\n\n"
            f"--- WHERE THE ANSWER IS (test author) ---\n{row['expected_source'] or 'nowhere: the corpus cannot answer this'} {row['expected_location']}\n\n"
            f"--- RETRIEVED PASSAGES (evidence) ---\n{evidence_text(result)}\n\n"
            f"--- ASSISTANT ANSWER ---\n{result['answer']}\n"
        )
        try:
            verdicts[qid] = parse_verdict(judge_call(prompt))
        except Exception as error:
            print(f"  WARNING judge failed on {qid}: {type(error).__name__}: {str(error)[:150]}")
            continue
        save_json(VERDICTS, verdicts)
    return verdicts


# ---------------------------------------------------------------- 5. human agreement

def kappa(a: list[int], b: list[int]) -> float | None:
    n = len(a)
    if n == 0:
        return None
    observed = sum(x == y for x, y in zip(a, b)) / n
    expected = sum((a.count(v) / n) * (b.count(v) / n) for v in (0, 1))
    return None if expected == 1 else (observed - expected) / (1 - expected)


def human_agreement(verdicts: dict) -> dict:
    labels = {}
    if HUMAN_LABELS.is_file():
        with HUMAN_LABELS.open(newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                qid = (r.get("id") or "").strip()
                if qid and (r.get("correct") or "").strip() in ("0", "1") and (r.get("supported") or "").strip() in ("0", "1"):
                    labels[qid] = (int(r["correct"]), int(r["supported"]))
    both = [q for q in labels if q in verdicts]
    out = {"graded_by_you": len(labels), "compared": len(both)}
    if both:
        for i, name in enumerate(("correct", "supported")):
            human = [labels[q][i] for q in both]
            judge = [verdicts[q][name] for q in both]
            out[f"agreement_{name}"] = sum(h == j for h, j in zip(human, judge)) / len(both)
            out[f"kappa_{name}"] = kappa(human, judge)
        out["agreement_both"] = mean(
            labels[q] == (verdicts[q]["correct"], verdicts[q]["supported"]) for q in both
        )
        out["disagreements"] = [q for q in both if labels[q] != (verdicts[q]["correct"], verdicts[q]["supported"])]
    return out


PASSAGE_RE = re.compile(r"\[(\d+)\] source: (\S+) \| location: ([^|\n]+?) \| distance: ([\d.]+)\n(.*?)(?=\n\n\[\d+\] source: |\Z)", re.S)


def write_grading_sheet(rows: list[dict], answers: dict) -> None:
    """A sheet for grading by hand. It has no judge verdicts, so you grade before seeing them."""
    lines = [
        "# Grade these answers yourself",
        "",
        "Fill `eval/human_labels.csv` (columns id, correct, supported, notes) for at least 20 of them,",
        "**before** looking at `eval/judge_verdicts.json`.",
        "- `correct` = 1 if the answer matches the reference answer (or is a proper refusal for an unanswerable question), else 0.",
        "- `supported` = 1 if every claim is in the retrieved passages shown below, else 0. Explain every 0 in `notes`.",
        "",
    ]
    for row in rows:
        result = answers.get(row["id"])
        if not result:
            continue
        retrieved = []
        for step in result["trace"]:
            if step["tool"] == "search" and step["status"] == "ok":
                retrieved += [(m[1], m[2].strip(), m[4].strip()) for m in PASSAGE_RE.findall(step["result"])]
        cited = CITE_RE.findall(result["answer"])
        shown = [(s, l, t) for s, l, t in retrieved if any(loc_match(cs, cl, s, l) for cs, cl in cited)]
        lines += [
            f"## {row['id']} ({row['kind']})",
            f"**Question:** {row['question']}",
            f"**Reference answer:** {row['reference_answer']}",
            f"**Agent answer:** {result['answer']}",
            f"**Searches:** {[s['args'].get('query') for s in result['trace'] if s['tool'] == 'search']}",
            f"**All retrieved locations:** {sorted({f'{s}: {l}' for s, l, _ in retrieved})}",
            "**Full text of the retrieved passages the answer cites:**" if shown else "**The answer cites no retrieved passage.**",
        ]
        for s, l, t in shown[:4]:
            lines.append(f"> **{s}, {l}**: {t[:1500]}")
            lines.append("")
        lines.append("")
    (EVAL / "grading_sheet.md").write_text("\n".join(lines), encoding="utf-8")


# ---------------------------------------------------------------- 6. before / after

def ensure_added_document() -> None:
    if ADDED_DOC.is_file():
        return
    import httpx

    ADDED_DOC.parent.mkdir(exist_ok=True)
    response = httpx.get(ADDED_URL, follow_redirects=True, timeout=120,
                         headers={"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) university-assignment"})
    response.raise_for_status()
    ADDED_DOC.write_bytes(response.content)


def before_after(rows: list[dict], answers: dict, force: bool) -> dict:
    existing = load_json(BEFORE_AFTER)
    if existing and not force:
        return existing
    row = next((r for r in rows if r["id"] == BEFORE_AFTER_QUESTION), None)
    if row is None or row["id"] not in answers:
        print("  before/after skipped: the question has no answer yet.")
        return {}
    ensure_added_document()
    import server

    source = ADDED_DOC.stem
    collection = index.get_collection(server.DESIGN)
    collection.delete(where={"source": source})  # start from the corpus without the document
    approvals = []

    def approve(tool, args):
        approvals.append({"tool": tool, "args": args})
        return True

    before = run_agent(row["question"], approve=lambda tool, args: False)
    added = run_agent(f"Please add the document at {ADDED_DOC.relative_to(ROOT)} to the corpus.", approve=approve)
    after = run_agent(row["question"], approve=lambda tool, args: False)
    collection.delete(where={"source": source})  # leave the committed index as it was
    data = {
        "question_id": row["id"],
        "question": row["question"],
        "document": str(ADDED_DOC.relative_to(ROOT)),
        "before": {"answer": before["answer"], "flags": before["flags"]},
        "add_request": {"answer": added["answer"], "approvals_asked": approvals,
                        "tool_results": [s["result"] for s in added["trace"] if s["tool"] == "add_document"]},
        "after": {"answer": after["answer"], "flags": after["flags"],
                  "searches": [s["args"] for s in after["trace"] if s["tool"] == "search"]},
    }
    save_json(BEFORE_AFTER, data)
    return data


# ---------------------------------------------------------------- 7. summary

def failure_candidates(rows, answers, verdicts, checks) -> list[dict]:
    failures = []
    for row in rows:
        qid = row["id"]
        if qid not in answers or qid not in verdicts:
            continue
        verdict, check = verdicts[qid], checks[qid]
        if verdict["correct"] and verdict["supported"]:
            continue
        answerable = row["kind"].strip().lower() != "unanswerable"
        if answerable and check["expected_retrieved"] is False:
            category = "retrieval miss"
        elif answerable and check["refused"]:
            category = "wrong refusal"
        elif not verdict["supported"] or not answerable:
            category = "unsupported claim"
        else:
            category = "wrong answer from right passage"
        failures.append({"id": qid, "kind": row["kind"], "auto_category": category,
                         "judge_reason": verdict["reason"], "final_category": "", "notes": ""})
    with (EVAL / "failures.csv").open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["id", "kind", "auto_category", "judge_reason", "final_category", "notes"])
        writer.writeheader()
        writer.writerows(failures)
    return failures


def summarise(rows, retrieval, answers, verdicts, checks, agreement, ba, failures) -> str:
    unanswerable = [r["id"] for r in rows if r["kind"].strip().lower() == "unanswerable"]
    answerable = [r["id"] for r in rows if r["id"] not in unanswerable]
    judged = [q for q in verdicts if q in answers]
    seconds = [answers[q]["seconds"] for q in answers]
    tokens_in = [answers[q]["tokens"]["input"] for q in answers]
    tokens_out = [answers[q]["tokens"]["output"] for q in answers]
    lines = ["# Evaluation summary", "", "## Retrieval (answerable questions)", "",
             "| design | chunks | hit@1 | hit@3 | hit@5 | words in prompt (top 5) |", "|---|---|---|---|---|---|"]
    for design, r in retrieval.items():
        lines.append(f"| {design} | {r['chunks']} | {r['hit@1']:.2f} | {r['hit@3']:.2f} | {r['hit@5']:.2f} | {r['avg_words_in_prompt_top5']} |")
    for design, r in retrieval.items():
        for kind, v in r["by_kind"].items():
            lines.append(f"- design {design}, {kind} (n={v['n']}): hit@1 {v['hit@1']:.2f}, hit@3 {v['hit@3']:.2f}, hit@5 {v['hit@5']:.2f}")
    lines += ["", f"## End to end ({len(answers)} of {len(rows)} questions answered, {len(judged)} judged)", ""]
    correct = [q for q in judged if q in answerable and verdicts[q]["correct"] and verdicts[q]["supported"]]
    unsupported = [q for q in judged if not verdicts[q]["supported"]]
    right_refusals = [q for q in judged if q in unanswerable and verdicts[q]["correct"]]
    wrong_refusals = [q for q in answers if q in answerable and checks[q]["refused"]]
    lines += [f"- correct and supported answers: {len(correct)} of {len([q for q in judged if q in answerable])} answerable",
              f"- unsupported answers (judge): {len(unsupported)}",
              f"- correct refusals: {len(right_refusals)} of {len([q for q in judged if q in unanswerable])} unanswerable",
              f"- wrong refusals (code check, answerable questions refused): {len(wrong_refusals)}",
              f"- code checks passed: {sum(checks[q]['code_pass'] for q in checks)} of {len(checks)}",
              f"- guardrail flags: " + (", ".join(f"{q}: {','.join(answers[q]['flags'])}" for q in answers if answers[q]["flags"]) or "none")]
    lines += ["", "## Agreement with your grades", ""]
    if agreement.get("compared"):
        lines += [f"- compared on {agreement['compared']} answers (you graded {agreement['graded_by_you']})",
                  f"- agreement on `correct`: {agreement['agreement_correct']:.2f}, on `supported`: {agreement['agreement_supported']:.2f}, on both: {agreement['agreement_both']:.2f}",
                  f"- disagreements: {', '.join(agreement['disagreements']) or 'none'}"]
        if agreement["graded_by_you"] < 20:
            lines.append(f"- WARNING: only {agreement['graded_by_you']} graded; the brief asks for 20+.")
    else:
        lines.append(f"- no usable grades found in eval/human_labels.csv yet. Grade with eval/grading_sheet.md.")
    lines += ["", "## Cost per question", "",
              f"- seconds: mean {mean(seconds):.1f}, median {statistics.median(seconds) if seconds else 0:.1f}",
              f"- tokens in / out: mean {mean(tokens_in):.0f} / {mean(tokens_out):.0f} (agent only; the judge adds one call per question)"]
    lines += ["", "## Failure candidates (check them by hand and fill final_category in eval/failures.csv)", ""]
    counts: dict[str, int] = {}
    for f in failures:
        counts[f["auto_category"]] = counts.get(f["auto_category"], 0) + 1
    lines += [f"- {k}: {v}" for k, v in sorted(counts.items())] or ["- none"]
    if ba:
        lines += ["", "## Before / after adding a document", "",
                  f"- question {ba['question_id']}: {ba['question']}", f"- document added: {ba['document']}",
                  f"- BEFORE: {ba['before']['answer'][:500]}", f"- AFTER: {ba['after']['answer'][:700]}"]
    return "\n".join(lines) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate the RAG system.")
    parser.add_argument("--force", action="store_true", help="redo agent answers, verdicts and before/after")
    parser.add_argument("--rejudge", action="store_true", help="grade the saved answers again with the judge (keeps the answers)")
    parser.add_argument("--retrieval-only", action="store_true", help="only the hit rate comparison")
    args = parser.parse_args()

    load_api_key()
    rows = read_questions()
    print(f"{len(rows)} questions.\n1. Retrieval hit rate")
    retrieval = retrieval_eval(rows)
    for design, r in retrieval.items():
        print(f"  design {design}: hit@1 {r['hit@1']:.2f}  hit@3 {r['hit@3']:.2f}  hit@5 {r['hit@5']:.2f}  words in prompt {r['avg_words_in_prompt_top5']}")
    save_json(EVAL / "retrieval.json", retrieval)
    if args.retrieval_only:
        return

    print("2. Agent answers")
    answers = answer_all(rows, args.force)
    write_grading_sheet(rows, answers)
    checks = {r["id"]: code_checks(r, answers[r["id"]]) for r in rows if r["id"] in answers}
    save_json(EVAL / "code_checks.json", checks)
    print("3. LLM judge")
    verdicts = judge_all(rows, answers, args.force or args.rejudge)
    agreement = human_agreement(verdicts)
    print("4. Before / after")
    try:
        ba = before_after(rows, answers, args.force)
    except Exception as error:
        print(f"  WARNING before/after failed ({type(error).__name__}: {str(error)[:150]}). Run again later.")
        ba = {}
    failures = failure_candidates(rows, answers, verdicts, checks)
    summary = summarise(rows, retrieval, answers, verdicts, checks, agreement, ba, failures)
    (EVAL / "summary.md").write_text(summary, encoding="utf-8")
    save_json(EVAL / "results.json", {"retrieval": retrieval, "agreement": agreement,
                                      "answered": len(answers), "judged": len(verdicts)})
    print("\n" + summary)


if __name__ == "__main__":
    main()
