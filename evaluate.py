"""
Assignment 3: evaluation (`main.py evaluate`).

1. Retrieval: hit rate at k = 1, 3, 5 for each chunking design (index.DESIGNS),
   plus the words each design adds to the prompt.
2. End to end: the agent (agent.Harness) answers every question in
   eval/questions.csv, with add_document approvals rejected.
3. Code checks: citations exist in what search returned; refusal when (and only
   when) the question is unanswerable; the answer cites the expected passage.
4. LLM judge: correctness against the reference answer and support by the
   retrieved text, with a written rubric (JUDGE_RUBRIC).
5. Agreement between the judge and eval/human_labels.csv.
6. Add-document demo: an unanswerable question, before and after adding a
   document that answers it (Food Code Chapter 8), through the MCP tool.

Agent answers and judge verdicts are saved and reused when the question (or the
answer) has not changed, so re-running costs no API calls. Set EVAL_FRESH=1 to
answer and judge everything again. EVAL_ONLY=retrieval runs step 1 only;
EVAL_SKIP_DEMO=1 skips the add-document demo.
"""

from __future__ import annotations

import asyncio
import csv
import hashlib
import json
import os
import re
import time
from collections import Counter
from pathlib import Path

import index
from agent import JUDGE_MODEL, MODEL, Harness, check_citations

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
HUMAN_LABELS = EVAL / "human_labels.csv"
ANSWERS = EVAL / "answers.jsonl"
VERDICTS = EVAL / "judge.jsonl"
FRESH = os.environ.get("EVAL_FRESH") == "1"
KS = (1, 3, 5)

DEMO_PAGES = (166, 185)    # Food Code 2022, Chapter 8: Compliance and Enforcement
DEMO_FILE = index.CORPUS_DIR / "food_code_2022_chapter_8.pdf"


def log(*args) -> None:
    print(*args, flush=True)


def read_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r["question"].strip()]


# --------------------------------------------------------------------------- matching passages

def expected_passages(row: dict) -> list[list[tuple[str, str]]]:
    """[[(source, location), alternative, ...], ...]: every inner list is one passage
    that must be found; alternatives are separated by | in expected_location."""
    sources = [s.strip() for s in row["expected_source"].split(";") if s.strip()]
    locations = [l.strip() for l in row["expected_location"].split(";")]
    if not sources:
        return []
    if len(sources) == 1 and len(locations) > 1:
        sources = sources * len(locations)
    return [[(src, alt.strip()) for alt in loc.split("|")] for src, loc in zip(sources, locations)]


def _section_key(section: str) -> tuple[int, ...]:
    m = re.match(r"(\d)-(\d{3})\.(\d+)", section)
    return (int(m[1]), int(m[2]), int(m[3])) if m else (0, 0, 0)


def location_matches(meta: dict, source: str, location: str) -> bool:
    """Does a chunk (its metadata) contain the expected source and location?"""
    if meta.get("source") != source:
        return False
    if location.startswith("p."):
        page = int(re.sub(r"\D", "", location))
        return int(meta["page_start"]) <= page <= int(meta["page_end"])
    return location in str(meta.get("sections", "")).split(";")


def parse_cite(cite: str) -> dict:
    """[food_code_2022, §3-501.16 to 3-501.17, pp. 93-94] -> metadata-like dict."""
    inner = cite.strip("[]")
    source, _, rest = inner.partition(", ")
    pages = re.search(r"pp?\. (\d+)(?:-(\d+))?", rest)
    secs = re.search(r"§([\d.\-]+)(?: to ([\d.\-]+))?", rest)
    meta = {"source": source, "page_start": int(pages[1]) if pages else 0,
            "page_end": int(pages[2] or pages[1]) if pages else 0, "sections": ""}
    if secs:
        meta["range"] = (secs[1], secs[2] or secs[1])
    return meta


def cite_matches(cite: str, source: str, location: str) -> bool:
    meta = parse_cite(cite)
    if meta["source"] != source:
        return False
    if location.startswith("p."):
        return location_matches(meta, source, location)
    if "range" not in meta:
        return False
    low, high = (_section_key(s) for s in meta["range"])
    return low <= _section_key(location) <= high


def passages_found(passages, metas: list[dict]) -> int:
    return sum(any(location_matches(m, s, l) for m in metas for s, l in alts) for alts in passages)


# --------------------------------------------------------------------------- 1. retrieval

def evaluate_retrieval(questions: list[dict]) -> dict:
    rows, summary = [], {}
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    for design in index.DESIGNS:
        hits = {k: 0 for k in KS}
        any_hits = {k: 0 for k in KS}
        words = {k: [] for k in KS}
        top_scores = {"answerable": [], "unanswerable": []}
        for q in questions:
            results = index.search(q["question"], k=max(KS), design=design)
            top_scores["unanswerable" if q["kind"] == "unanswerable" else "answerable"].append(results[0]["score"])
            if q["kind"] == "unanswerable":
                continue
            passages = expected_passages(q)
            row = {"id": q["id"], "design": design, "kind": q["kind"]}
            for k in KS:
                found = passages_found(passages, results[:k])
                hits[k] += found == len(passages)
                any_hits[k] += found > 0
                words[k].append(sum(int(r["words"]) for r in results[:k]))
                row[f"hit@{k}"] = int(found == len(passages))
            row["top5"] = " | ".join(r["cite"] for r in results)
            rows.append(row)
        n = len(answerable)
        summary[design] = {
            "chunks": index.collection(design).count(),
            **{f"hit@{k}": round(hits[k] / n, 3) for k in KS},
            **{f"any_passage@{k}": round(any_hits[k] / n, 3) for k in KS},
            **{f"words_in_prompt@{k}": round(sum(words[k]) / n) for k in KS},
            "mean_top_score_answerable": round(sum(top_scores["answerable"]) / n, 3),
            "mean_top_score_unanswerable": round(sum(top_scores["unanswerable"]) / max(1, len(top_scores["unanswerable"])), 3),
        }
        log(f"  {design:9s} " + "  ".join(f"hit@{k} {summary[design][f'hit@{k}']:.2f}" for k in KS)
            + f"  words@5 {summary[design]['words_in_prompt@5']}")
    with (EVAL / "retrieval.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    return summary


# --------------------------------------------------------------------------- 2. answers

def load_jsonl(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def save_jsonl(path: Path, rows: list[dict]) -> None:
    path.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in rows) + "\n", encoding="utf-8")


def reject(name: str, args: dict) -> bool:
    return False


def api_failure(result: dict) -> str:
    """Why an answer can't be trusted as an answer (API error or exhausted quota), else ''."""
    if result.get("error"):
        return result["error"]
    return next((r["text"][:200] for r in result.get("tool_results", []) if r["text"].startswith("Search failed")), "")


async def answer_all(questions: list[dict]) -> dict[str, dict]:
    saved = {} if FRESH else {a["id"]: a for a in load_jsonl(ANSWERS)}
    answers = {}
    todo = [q for q in questions if saved.get(q["id"], {}).get("question") != q["question"]
            or api_failure(saved[q["id"]])]
    for q in questions:
        if q not in todo:
            answers[q["id"]] = saved[q["id"]]
    log(f"  {len(answers)} saved answer(s) reused, {len(todo)} to run")
    if todo:
        async with Harness(approve=reject) as harness:
            for i, q in enumerate(todo, 1):
                try:
                    result = await harness.ask(q["question"])
                except Exception as error:  # noqa: BLE001 - record it and go on
                    result = {"question": q["question"], "answer": "", "error": f"{type(error).__name__}: {error}",
                              "check": {}, "tool_calls": [], "tool_results": [], "input_tokens": 0,
                              "output_tokens": 0, "seconds": 0, "model_calls": 0, "guardrail": "error"}
                result["id"] = q["id"]
                if api_failure(result):
                    # Never record an API failure as the agent's answer: stop, keep what we have.
                    log(f"  {q['id']}: stopped by an API error, not saved: {api_failure(result)}")
                    break
                answers[q["id"]] = result
                save_jsonl(ANSWERS, [answers[x["id"]] for x in questions if x["id"] in answers])
                log(f"  [{i}/{len(todo)}] {q['id']} {result['seconds']}s, guardrail {result['guardrail']}: "
                    f"{result['answer'][:90]!r}")
    save_jsonl(ANSWERS, [answers[q["id"]] for q in questions if q["id"] in answers])
    return answers


# --------------------------------------------------------------------------- 3. code checks

def code_checks(q: dict, a: dict) -> dict:
    retrieved = {c for r in a.get("tool_results", []) if r["tool"] == "search"
                 for c in re.findall(r"^(\[[a-z0-9_]+, [^\[\]\n]+\]) score=", r["text"], re.M)}
    check = check_citations(a.get("answer", ""), retrieved)
    unanswerable = q["kind"] == "unanswerable"
    passages = expected_passages(q)
    expected_retrieved = sum(any(cite_matches(c, s, l) for c in retrieved for s, l in alts) for alts in passages)
    expected_cited = sum(any(cite_matches(c, s, l) for c in check["cited"] for s, l in alts) for alts in passages)
    return {
        "refused": check["refusal"],
        "refusal_ok": int(check["refusal"] == unanswerable),
        "citations_valid": int(not check["invalid"]),
        "has_citation": int(bool(check["cited"])),
        "expected_passages": len(passages),
        "expected_retrieved": expected_retrieved,
        "expected_cited": expected_cited,
        "searches": sum(1 for c in a.get("tool_calls", []) if c["tool"] == "search"),
    }


# --------------------------------------------------------------------------- 4. judge

JUDGE_RUBRIC = """You grade answers from a food-safety assistant for restaurant operators.
The assistant must answer only from the retrieved passages (the EVIDENCE) and must say
"The documents I have do not cover this" when they do not answer the question.

Grade two things, each 1 or 0.

correct:
- Answerable question (a reference answer is given): 1 if the answer gives the key facts
  of the reference answer (numbers, units, times, conditions that change the rule) and
  says nothing that contradicts it. Missing minor detail or extra correct detail is fine.
  A wrong or missing number, a dropped condition that changes the rule, or a refusal is 0.
- Unanswerable question (the reference says the documents do not cover it): 1 if the
  answer declines and does not answer the question itself; 0 if it answers anyway, even
  partly or "in general". A refusal MAY point the user elsewhere ("consult your local
  health authority", "see the European Commission's guidance") and MAY say what the
  documents do cover nearby: that is still a refusal (1), not an answer.

supported:
- 1 if every factual claim in the answer is stated in, or follows directly from, the
  EVIDENCE. 0 if any claim (a number, a rule, an exception, a risk) is not in the
  EVIDENCE, even if it is true in the real world.
- A pointer to where to look (a health authority, the Food Code, an official body) is
  not a factual claim. A statement about what the documents cover counts as supported
  if the EVIDENCE shows it. Advice that goes beyond a pointer (e.g. emergency or medical
  instructions) is a claim and must be in the EVIDENCE.
- Read all of the EVIDENCE before deciding a claim is missing: one answer may draw on
  several passages. Ignore citation formatting; judge only the content.

Return JSON: {"correct": 0 or 1, "supported": 0 or 1, "explanation": one or two sentences}."""


def _judge_client():
    from google import genai
    from api_key import load_api_key
    return genai.Client(api_key=load_api_key())


def judge_one(client, q: dict, a: dict) -> dict:
    from google.genai import types

    evidence = "\n\n".join(r["text"] for r in a.get("tool_results", []) if r["tool"] == "search")[:30000]
    prompt = (f"QUESTION: {q['question']}\n\nQUESTION TYPE: {q['kind']}\n\nREFERENCE ANSWER: {q['reference_answer']}\n\n"
              f"ASSISTANT ANSWER: {a.get('answer', '')}\n\nEVIDENCE (retrieved passages):\n{evidence or '(none)'}")
    schema = {"type": "object", "properties": {
        "correct": {"type": "integer", "enum": [0, 1]},
        "supported": {"type": "integer", "enum": [0, 1]},
        "explanation": {"type": "string"}}, "required": ["correct", "supported", "explanation"]}
    for attempt in range(5):
        try:
            response = client.models.generate_content(
                model=JUDGE_MODEL, contents=prompt,
                config=types.GenerateContentConfig(system_instruction=JUDGE_RUBRIC,
                                                   response_mime_type="application/json",
                                                   response_json_schema=schema))
            verdict = json.loads(response.text)
            usage = response.usage_metadata
            verdict["judge_tokens"] = (usage.prompt_token_count or 0) + (usage.candidates_token_count or 0) if usage else 0
            return verdict
        except Exception as error:  # noqa: BLE001
            if attempt == 4:
                return {"correct": None, "supported": None, "explanation": f"judge failed: {error}", "judge_tokens": 0}
            time.sleep(15 * (attempt + 1))


def judge_all(questions: list[dict], answers: dict[str, dict]) -> dict[str, dict]:
    saved = {} if FRESH else {v["id"]: v for v in load_jsonl(VERDICTS)}
    client, verdicts = None, {}
    for q in questions:
        a = answers[q["id"]]
        key = hashlib.sha1(f"{JUDGE_RUBRIC}|{JUDGE_MODEL}|{q['question']}|{q['reference_answer']}|"
                           f"{a.get('answer', '')}".encode()).hexdigest()
        if saved.get(q["id"], {}).get("key") == key and saved[q["id"]].get("correct") is not None:
            verdicts[q["id"]] = saved[q["id"]]
            continue
        client = client or _judge_client()
        verdicts[q["id"]] = {"id": q["id"], "key": key, **judge_one(client, q, a)}
        save_jsonl(VERDICTS, list(verdicts.values()))
        log(f"  judged {q['id']}: correct={verdicts[q['id']]['correct']} supported={verdicts[q['id']]['supported']}")
    save_jsonl(VERDICTS, [verdicts[q["id"]] for q in questions])
    return verdicts


# --------------------------------------------------------------------------- 5. agreement

def cohen_kappa(a: list[int], b: list[int]) -> float | None:
    n = len(a)
    if not n:
        return None
    observed = sum(x == y for x, y in zip(a, b)) / n
    pa, pb = sum(a) / n, sum(b) / n
    expected = pa * pb + (1 - pa) * (1 - pb)
    return round((observed - expected) / (1 - expected), 3) if expected < 1 else None


def agreement(verdicts: dict[str, dict]) -> dict:
    if not HUMAN_LABELS.is_file():
        return {"graded": 0}
    with HUMAN_LABELS.open(newline="", encoding="utf-8") as f:
        labels = [r for r in csv.DictReader(f) if r.get("id", "").strip() in verdicts]
    out = {"graded": len(labels), "disagreements": []}
    for field in ("correct", "supported"):
        pairs = [(int(r[field]), int(verdicts[r["id"]][field])) for r in labels
                 if r.get(field, "").strip() in {"0", "1"} and verdicts[r["id"]].get(field) is not None]
        if not pairs:
            continue
        human, judge = zip(*pairs)
        out[field] = {"n": len(pairs), "agreement": round(sum(h == j for h, j in pairs) / len(pairs), 3),
                      "kappa": cohen_kappa(list(human), list(judge)),
                      "human_rate": round(sum(human) / len(pairs), 3), "judge_rate": round(sum(judge) / len(pairs), 3)}
    for r in labels:
        v = verdicts[r["id"]]
        for field in ("correct", "supported"):
            if r.get(field, "").strip() in {"0", "1"} and v.get(field) is not None and int(r[field]) != int(v[field]):
                out["disagreements"].append({"id": r["id"], "field": field, "human": int(r[field]),
                                             "judge": int(v[field]), "human_notes": r.get("notes", ""),
                                             "judge_explanation": v.get("explanation", "")})
    return out


# --------------------------------------------------------------------------- 6. add-document demo

def make_demo_document() -> Path:
    """Cut Food Code Chapter 8 (not in the corpus) out of the downloaded PDF as its own file."""
    from pypdf import PdfReader, PdfWriter

    if not DEMO_FILE.is_file():
        source = index.download(index.CORPUS[0])
        reader, writer = PdfReader(str(source)), PdfWriter()
        for page in range(DEMO_PAGES[0] - 1, DEMO_PAGES[1]):
            writer.add_page(reader.pages[page])
        with DEMO_FILE.open("wb") as f:
            writer.write(f)
    return DEMO_FILE


async def add_document_demo(questions: list[dict]) -> dict:
    out_path = EVAL / "add_document_demo.json"
    q = next((x for x in questions if "permit" in x["question"].lower() and x["kind"] == "unanswerable"), None)
    if q is None:
        return {}
    if out_path.is_file() and not FRESH:
        saved = json.loads(out_path.read_text(encoding="utf-8"))
        if saved.get("question") == q["question"]:
            log("  saved demo reused")
            return saved
    path = make_demo_document()
    source = index.chunk_file(path)[0].source
    index.remove_source(source)                     # make sure "before" really is before
    demo = {"id": q["id"], "question": q["question"], "document": str(path.relative_to(ROOT)), "source": source}
    async with Harness(approve=reject) as harness:
        before = await asyncio.wait_for(harness.ask(q["question"]), 400)
    async with Harness(approve=reject) as harness:
        # the same MCP tool the agent and the editor use
        result = await harness.session.call_tool("add_document", {"path": demo["document"]})
        demo["add_document_result"] = "\n".join(getattr(c, "text", "") for c in result.content)
        if '"status": "error"' in demo["add_document_result"]:
            log(f"  add_document failed, demo not saved (run evaluate again later): {demo['add_document_result']}")
            index.remove_source(source)
            return {}
        again = await harness.session.call_tool("add_document", {"path": demo["document"]})
        demo["add_again_result"] = "\n".join(getattr(c, "text", "") for c in again.content)
    async with Harness(approve=reject) as harness:
        after = await asyncio.wait_for(harness.ask(q["question"]), 400)
    demo["removed_chunks_afterwards"] = index.remove_source(source)   # keep the evaluated index unchanged
    for name, r in (("before", before), ("after", after)):
        demo[name] = {"answer": r["answer"], "cited": r["check"]["cited"], "guardrail": r["guardrail"],
                      "searches": [c["args"] for c in r["tool_calls"] if c["tool"] == "search"]}
    out_path.write_text(json.dumps(demo, indent=2, ensure_ascii=False), encoding="utf-8")
    log(f"  before: {before['answer'][:100]!r}\n  after:  {after['answer'][:100]!r}")
    return demo


DEMO_TIMEOUT = 900   # seconds for the whole demo


def run_demo(questions: list[dict]) -> dict:
    """Run the add-document demo with a time limit; on any failure, skip it and restore the index."""
    if os.environ.get("EVAL_SKIP_DEMO") == "1":
        log("  skipped (EVAL_SKIP_DEMO=1)")
        return {}
    try:
        return asyncio.run(asyncio.wait_for(add_document_demo(questions), DEMO_TIMEOUT))
    except Exception as error:  # noqa: BLE001 - includes TimeoutError
        log(f"  demo not completed ({type(error).__name__}: {error}); the other results are saved. "
            f"Run `main.py evaluate` again later to retry it.")
        return {}
    finally:
        try:
            removed = index.remove_source(index.chunk_file(DEMO_FILE)[0].source) if DEMO_FILE.is_file() else 0
            if removed:
                log(f"  removed {removed} demo chunk(s) so the evaluated index stays the 3-document corpus")
        except Exception:  # noqa: BLE001
            pass


# --------------------------------------------------------------------------- summary

def classify(q: dict, c: dict, v: dict) -> str:
    """First-pass failure cause from the code checks and the judge (reviewed by hand in REPORT.md)."""
    if v.get("correct") == 1 and v.get("supported") == 1:
        return ""
    if q["kind"] == "unanswerable":
        return "answered an unanswerable question (unsupported claim)" if not c["refused"] else "judge disagreement"
    if c["refused"]:
        return "retrieval miss" if c["expected_retrieved"] < c["expected_passages"] else "wrong refusal"
    if v.get("supported") == 0:
        return "unsupported claim"
    if c["expected_retrieved"] < c["expected_passages"]:
        return "retrieval miss"
    return "wrong answer from the right passage"


def main() -> int:
    EVAL.mkdir(exist_ok=True)
    questions = read_questions()
    started = time.time()

    log("\n== 1. Retrieval hit rate per design")
    retrieval = evaluate_retrieval(questions)
    if os.environ.get("EVAL_ONLY") == "retrieval":     # cheap first look: only query embeddings
        (EVAL / "retrieval_summary.json").write_text(json.dumps(retrieval, indent=2), encoding="utf-8")
        return 0

    log("\n== 2. Agent answers")
    answers = asyncio.run(answer_all(questions))
    if len(answers) < len(questions):
        log(f"\n{len(questions) - len(answers)} question(s) still unanswered because of an API limit or error. "
            f"The {len(answers)} saved answers are kept; run `main.py evaluate` again later (after the daily "
            f"reset at 09:00 in Spain) and it continues from there.")
        return 2

    log("\n== 3. Code checks")
    checks = {q["id"]: code_checks(q, answers[q["id"]]) for q in questions}

    log("\n== 4. LLM judge")
    verdicts = judge_all(questions, answers)

    log("\n== 5. Agreement with eval/human_labels.csv")
    agree = agreement(verdicts)
    log(f"  {json.dumps({k: v for k, v in agree.items() if k != 'disagreements'})}")

    demo: dict = {}

    # per-question results
    results = []
    for q in questions:
        a, c, v = answers[q["id"]], checks[q["id"]], verdicts[q["id"]]
        results.append({"id": q["id"], "kind": q["kind"], **c, "judge_correct": v.get("correct"),
                        "judge_supported": v.get("supported"), "guardrail": a.get("guardrail", ""),
                        "tokens": a.get("input_tokens", 0) + a.get("output_tokens", 0), "seconds": a.get("seconds", 0),
                        "auto_cause": classify(q, c, v), "question": q["question"], "answer": a.get("answer", ""),
                        "judge_explanation": v.get("explanation", "")})
    with (EVAL / "results.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(results[0]))
        w.writeheader()
        w.writerows(results)
    # a grading sheet without the judge's verdicts, for eval/human_labels.csv
    with (EVAL / "to_grade.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        w.writerow(["id", "kind", "question", "reference_answer", "answer", "retrieved_passages"])
        for q in questions:
            a = answers[q["id"]]
            w.writerow([q["id"], q["kind"], q["question"], q["reference_answer"], a.get("answer", ""),
                        "\n\n".join(r["text"] for r in a.get("tool_results", []) if r["tool"] == "search")])

    answerable = [r for r in results if r["kind"] != "unanswerable"]
    unanswerable = [r for r in results if r["kind"] == "unanswerable"]
    n = len(results)
    summary = {
        "model": MODEL, "judge_model": JUDGE_MODEL, "embedding_model": index.EMBED_MODEL, "active_design": index.ACTIVE_DESIGN,
        "questions": n, "by_kind": dict(Counter(r["kind"] for r in results)),
        "retrieval": retrieval,
        "end_to_end": {
            "correct_answers": sum(1 for r in answerable if r["judge_correct"] == 1 and not r["refused"]),
            "answerable": len(answerable),
            "unsupported_answers": sum(1 for r in results if r["judge_supported"] == 0),
            "correct_refusals": sum(1 for r in unanswerable if r["refused"]),
            "unanswerable": len(unanswerable),
            "wrong_refusals": sum(1 for r in answerable if r["refused"]),
            "answered_unanswerable": sum(1 for r in unanswerable if not r["refused"]),
            "judge_correct_rate": round(sum(1 for r in results if r["judge_correct"] == 1) / n, 3),
            "judge_supported_rate": round(sum(1 for r in results if r["judge_supported"] == 1) / n, 3),
        },
        "code_checks": {
            "citations_valid": sum(r["citations_valid"] for r in results),
            "refusal_ok": sum(r["refusal_ok"] for r in results),
            "answerable_citing_expected_passage": sum(1 for r in answerable if r["expected_cited"] > 0),
            "answerable_expected_passage_retrieved_by_agent": sum(1 for r in answerable
                                                                  if r["expected_retrieved"] == r["expected_passages"]),
            "guardrail_fired": sum(1 for r in results if r["guardrail"] != "passed"),
        },
        "failures_auto": dict(Counter(r["auto_cause"] for r in results if r["auto_cause"])),
        "cost_per_question": {
            "tokens_mean": round(sum(r["tokens"] for r in results) / n),
            "seconds_mean": round(sum(r["seconds"] for r in results) / n, 1),
            "seconds_max": max(r["seconds"] for r in results),
            "searches_mean": round(sum(r["searches"] for r in results) / n, 2),
            "judge_tokens_mean": round(sum((verdicts[r["id"]].get("judge_tokens") or 0) for r in results) / n),
        },
        "judge_vs_human": agree,
        "add_document_demo": {k: demo.get(k) for k in ("id", "question", "document", "add_document_result",
                                                       "add_again_result", "before", "after")} if demo else {},
        "evaluation_seconds": round(time.time() - started, 1),
    }
    (EVAL / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")

    # The demo runs last, after everything above is saved, so a slow or failed demo
    # (API limits) never costs the evaluation results.
    log("\n== 6. Add-document demo")
    demo = run_demo(questions)
    if demo:
        summary["add_document_demo"] = {k: demo.get(k) for k in ("id", "question", "document", "add_document_result",
                                                                  "add_again_result", "before", "after")}
        (EVAL / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
    e2e, cost = summary["end_to_end"], summary["cost_per_question"]
    log(f"\n== Summary\n  correct {e2e['correct_answers']}/{e2e['answerable']}, correct refusals "
        f"{e2e['correct_refusals']}/{e2e['unanswerable']}, wrong refusals {e2e['wrong_refusals']}, "
        f"unsupported {e2e['unsupported_answers']}\n  {cost['tokens_mean']} tokens and {cost['seconds_mean']}s per "
        f"question\n  Written: eval/retrieval.csv, answers.jsonl, judge.jsonl, results.csv, to_grade.csv, "
        f"summary.json, add_document_demo.json")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
