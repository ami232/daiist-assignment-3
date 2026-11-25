"""
Assignment 3: evaluation (`main.py evaluate`).

Stage 1 - retrieval: hit rate at k = 1, 3, 5 for each chunking design in
index.DESIGNS, using every answerable question in eval/questions.csv.

  A retrieved chunk is a hit for an expected (source, location) when it comes
  from that drug's label and covers that section: location "7" matches 7,
  7.1, 7.2...; "7.3" matches 7.3. Fixed windows can span several sections and
  count for each section they touch.
  single questions: hit@k = the expected passage is in the top k.
  multi questions:  hit@k = ALL expected passages are in the top k (strict),
                    plus "any@k" = at least one of them.

Writes eval/retrieval_results.csv (one row per question and design) and
eval/retrieval_summary.md. Query vectors are cached in index/, so reruns cost
no embedding quota.

Stage 2 - end to end:
  2a  run agent.py on every question (cached in eval/agent_runs.jsonl, keyed by
      question + AGENTS.md + model settings + index size, so reruns and the
      grader's run cost nothing; a run that hits the daily quota stops cleanly
      and the next run continues). Errors go to eval/agent_errors.csv.
  2b  code checks: citations (document exists, section exists, passage was
      retrieved), refusals (exact sentence / refusal phrases), uncited
      sentences, whether the expected passage was retrieved at all.
  2c  LLM judge with the rubric in JUDGE_RUBRIC (cached in eval/judge_cache.json).
  2d  blind grading sheet eval/human_grading_sheet.csv (no judge scores in it)
      and agreement with eval/human_labels.csv once you have graded.
  2e  failure categories (automatic proposal, for you to review) and cost.
Outputs: eval/agent_answers.csv, judge_results.csv, failure_analysis.csv,
evaluation_summary.md. questions.csv and human_labels.csv are only read.

    uv run python main.py evaluate                       # everything
    uv run python evaluate.py --limit 3                  # first 3 questions only
    uv run python evaluate.py --retrieval-only
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import statistics
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

import index

ROOT = Path(__file__).resolve().parent
EVAL_DIR = ROOT / "eval"
QUESTIONS = EVAL_DIR / "questions.csv"
HUMAN_LABELS = EVAL_DIR / "human_labels.csv"
RUNS = EVAL_DIR / "agent_runs.jsonl"
JUDGE_CACHE = EVAL_DIR / "judge_cache.json"
KS = (1, 3, 5)
REFUSAL_SENTENCE = "The labels I have do not cover this."
JUDGE_MODELS = ("gemini-3.5-flash", "gemini-3.6-flash", "gemini-3.5-flash-lite", "gemini-3.1-flash-lite",
                "gemini-3.7-flash", "gemini-3.8-flash")
JUDGE_BATCH = 4  # answers per judge call: the free tier allows only 20 calls per model per day
FAILURE_CAUSES = ("retrieval miss", "wrong answer from the right passage", "unsupported claim",
                  "wrong refusal", "bad test question")


def log(*args) -> None:
    print(*args, flush=True)


def load_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if (r.get("question") or "").strip()]
    for r in rows:
        r["kind"] = r["kind"].strip().lower()
        sources = [s.strip().lower() for s in r["expected_source"].split(";") if s.strip()]
        locations = [s.strip() for s in r["expected_location"].split(";") if s.strip()]
        r["expected"] = list(zip(sources, locations))
    return rows


def covers(hit: dict, source: str, location: str) -> bool:
    if hit["source"] != source:
        return False
    sections = [s for s in hit["sections"].split(",") if s]
    return any(s == location or s.startswith(location + ".") for s in sections)


def first_rank(hits: list[dict], source: str, location: str) -> int | None:
    """1-based rank of the first hit covering this passage, or None."""
    return next((i for i, h in enumerate(hits, 1) if covers(h, source, location)), None)


# --------------------------------------------------------------------------
# Stage 1: retrieval
# --------------------------------------------------------------------------

def evaluate_retrieval(questions: list[dict]) -> list[dict]:
    rows = []
    kmax = max(KS)
    for design in index.DESIGNS:
        for q in questions:
            hits = index.search(q["question"], k=kmax, design=design)
            row = {
                "design": design,
                "id": q["id"],
                "kind": q["kind"],
                "top1_score": hits[0]["score"] if hits else 0.0,
                "top5_words": sum(h["words"] for h in hits),
                "retrieved": " | ".join(f"{h['source']} {h['location'][:40]} ({h['score']:.2f})" for h in hits),
            }
            if q["kind"] != "unanswerable":
                ranks = [first_rank(hits, s, loc) for s, loc in q["expected"]]
                row["ranks"] = ";".join(str(r) if r else "-" for r in ranks)
                for k in KS:
                    found = [r is not None and r <= k for r in ranks]
                    row[f"hit@{k}"] = int(all(found))
                    row[f"any@{k}"] = int(any(found))
                found_ranks = [r for r in ranks if r]
                row["rr"] = 1 / min(found_ranks) if found_ranks else 0.0
            rows.append(row)
    return rows


def summarize_retrieval(rows: list[dict]) -> str:
    def mean(values):
        values = list(values)
        return statistics.mean(values) if values else float("nan")

    lines = [
        "# Retrieval results",
        "",
        "Hit@k: the expected passage is among the top k chunks (multi: all expected passages).",
        "Any@k (multi only): at least one expected passage in the top k. MRR: mean reciprocal rank of the first hit.",
        "Prompt words: words the top 5 chunks add to the prompt.",
        "",
        "| Design | Questions | Hit@1 | Hit@3 | Hit@5 | MRR | Multi any@5 | Prompt words (top 5) | Top-1 score answerable | Top-1 score unanswerable |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for design in index.DESIGNS:
        mine = [r for r in rows if r["design"] == design]
        answerable = [r for r in mine if r["kind"] != "unanswerable"]
        multi = [r for r in answerable if r["kind"] == "multi"]
        unanswerable = [r for r in mine if r["kind"] == "unanswerable"]
        cells = [design, str(len(answerable))]
        cells += [f"{mean(r[f'hit@{k}'] for r in answerable):.2f}" for k in KS]
        cells.append(f"{mean(r['rr'] for r in answerable):.2f}")
        cells.append(f"{mean(r['any@5'] for r in multi):.2f}" if multi else "n/a")
        cells.append(f"{mean(r['top5_words'] for r in mine):.0f}")
        cells.append(f"{mean(r['top1_score'] for r in answerable):.3f}")
        cells.append(f"{mean(r['top1_score'] for r in unanswerable):.3f}" if unanswerable else "n/a")
        lines.append("| " + " | ".join(cells) + " |")

    lines += ["", "## By kind", "", "| Design | Kind | n | Hit@1 | Hit@3 | Hit@5 |", "|---|---|---|---|---|---|"]
    for design in index.DESIGNS:
        for kind in ("single", "multi"):
            group = [r for r in rows if r["design"] == design and r["kind"] == kind]
            if group:
                lines.append(f"| {design} | {kind} | {len(group)} | "
                             + " | ".join(f"{mean(r[f'hit@{k}'] for r in group):.2f}" for k in KS) + " |")

    misses = [r for r in rows if r["kind"] != "unanswerable" and not r["hit@5"]]
    lines += ["", "## Misses at k=5", ""]
    lines += [f"- {r['design']} {r['id']} (expected ranks {r['ranks']}): {r['retrieved']}" for r in misses] or ["- none"]
    return "\n".join(lines) + "\n"


def write_csv(path: Path, rows: list[dict]) -> None:
    fields = list(dict.fromkeys(k for r in rows for k in r))
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


# --------------------------------------------------------------------------
# Stage 2a: agent runs (cached, resumable)
# --------------------------------------------------------------------------

def is_quota_error(error: Exception) -> bool:
    text = str(error)
    return "RESOURCE_EXHAUSTED" in text or "429" in text


def load_runs() -> dict[str, dict]:
    runs = {}
    if RUNS.exists():
        for line in RUNS.read_text(encoding="utf-8").splitlines():
            if line.strip():
                run = json.loads(line)
                runs[run["key"]] = run
    return runs


def run_key(question: str, settings: str) -> str:
    return hashlib.sha1(f"{settings}\n{question}".encode("utf-8")).hexdigest()


def agent_settings() -> str:
    """Everything that changes an answer: rules, models, retrieval design, index size."""
    import agent

    rules = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    size = index.get_collection(index.DEFAULT_DESIGN).count()
    return json.dumps([rules, agent.MODEL, agent.FALLBACK_MODELS, agent.MAX_MODEL_CALLS,
                       agent.MAX_SEARCHES, index.DEFAULT_DESIGN, size])


def run_agent_on_all(questions: list[dict]) -> tuple[dict[str, dict], list[dict]]:
    """{question id: agent result} for every question that has (or now gets) an answer."""
    import agent

    settings = agent_settings()
    runs = load_runs()
    results, errors = {}, []
    quota_hit = False
    for q in questions:
        key = run_key(q["question"], settings)
        if key in runs:
            results[q["id"]] = runs[key]
            continue
        if quota_hit:
            errors.append({"id": q["id"], "error": "not run: daily quota exhausted earlier in this run"})
            continue
        log(f"  agent {q['id']}: {q['question'][:70]}")
        try:
            result = agent.run_agent(q["question"], approve=agent.deny)
        except Exception as error:  # noqa: BLE001 - recorded, never silently skipped
            message = f"{type(error).__name__}: {str(error)[:300]}"
            errors.append({"id": q["id"], "error": message})
            log(f"    ERROR {message[:150]}")
            if is_quota_error(error):
                quota_hit = True
                log("    daily quota exhausted on every model; the remaining questions run next time")
            continue
        result.update({"key": key, "id": q["id"], "timestamp": datetime.now(timezone.utc).isoformat()})
        with RUNS.open("a", encoding="utf-8") as f:
            f.write(json.dumps(result, ensure_ascii=False) + "\n")
        results[q["id"]] = result
        log(f"    {result['model']}, {result['seconds']}s, "
            f"{result['tokens']['input'] + result['tokens']['output']} tokens"
            + (f", guardrail fired: {result['guardrail']}" if result["guardrail"] else ""))
    return results, errors


# --------------------------------------------------------------------------
# Stage 2b: code checks
# --------------------------------------------------------------------------

def parse_passages(trace: list[dict]) -> dict[tuple[str, str], dict]:
    """Every passage the agent's searches returned: {(drug, section): {header, text}}."""
    passages = {}
    for step in trace:
        if step["tool"] != "search" or step["error"]:
            continue
        for block in step["output"].split("--- Result ")[1:]:
            match = re.search(r"cite as \[([a-z]+) ([^\]]+)\].*\nSource: (.*?)\n(.*)", block, re.S)
            if match:
                drug, section, header, text = match.groups()
                entry = passages.setdefault((drug, section.strip()), {"header": header, "text": ""})
                if text.strip() not in entry["text"]:
                    entry["text"] = (entry["text"] + "\n" + text.strip()).strip()
    return passages


def section_ok(cited: str, have: str) -> bool:
    return cited == have or have.startswith(cited + ".") or cited.startswith(have + ".")


def uncited_sentences(answer: str) -> list[str]:
    """Heuristic: sentences of 6+ words that state something but carry no [citation]."""
    found = []
    for line in answer.splitlines():
        line = line.strip(" -*•\t")
        if not line or line.endswith(":"):
            continue
        for sentence in re.split(r"(?<=[.!?])\s+", line):
            words = re.findall(r"[A-Za-z]+", sentence)
            if len(words) < 6 or "[" in sentence or REFUSAL_SENTENCE.lower() in sentence.lower():
                continue
            if re.search(r"\b(consult|talk to|ask|contact|speak with)\b.*\b(doctor|pharmacist|healthcare|provider|prescriber)", sentence, re.I):
                continue  # referral advice, not a label claim
            found.append(sentence.strip())
    return found


def code_checks(q: dict, result: dict, sections: dict) -> dict:
    import agent

    shown, raw = result["answer"], result["raw_answer"]
    passages = parse_passages(result["trace"])
    citations = agent.cited(raw)
    bad_doc = [f"[{d} {s}]" for d, s in citations if d not in sections]
    bad_loc = [f"[{d} {s}]" for d, s in citations
               if d in sections and not any(section_ok(s, n) for n in sections[d])]
    not_retrieved = [f"[{d} {s}]" for d, s in citations
                     if not any(d == pd and section_ok(s, ps) for pd, ps in passages)]
    refused = REFUSAL_SENTENCE.lower() in shown.lower() or agent.is_refusal(shown)
    blocked = bool(result["guardrail"])
    expected_found = [any(d == s and (ps == loc or ps.startswith(loc + ".")) for d, ps in passages)
                      for s, loc in q["expected"]]
    searches = [t for t in result["trace"] if t["tool"] == "search"]
    return {
        "citations": " ".join(f"[{d} {s}]" for d, s in citations),
        "n_citations": len(citations),
        "invalid_document": " ".join(bad_doc),
        "invalid_location": " ".join(bad_loc),
        "cited_not_retrieved": " ".join(not_retrieved),
        "uncited_sentences": len(uncited_sentences(raw)),
        "refused": int(refused and not blocked),
        "exact_refusal_sentence": int(REFUSAL_SENTENCE.lower() in raw.lower()),
        "guardrail_blocked": int(blocked),
        "expected_retrieved": "" if q["kind"] == "unanswerable" else int(all(expected_found)),
        "searches": len(searches),
        "search_queries": " || ".join(t["args"].get("query", "") for t in searches),
        "retrieved": " ".join(f"[{d} {s}]" for d, s in passages),
    }


# --------------------------------------------------------------------------
# Stage 2c: LLM judge
# --------------------------------------------------------------------------

JUDGE_RUBRIC = """You grade answers from a medication-label assistant. Use ONLY the retrieved label
passages and the reference answer given for each item. Never use outside medical knowledge.

Score each dimension 2, 1 or 0:
- correctness: is the answer factually consistent with the reference answer?
- evidence_support: is every factual claim supported by the retrieved passages?
- citation_quality: do the [citations] point to the passages that support each claim?
- refusal_quality: was refusing (or answering) the right choice given the evidence?
- completeness: does the answer include the essential information in the reference?
Scale: 2 = fully correct and supported; 1 = partially correct or incomplete;
0 = incorrect, unsupported, or an inappropriate refusal.

Question kinds: "single" and "multi" questions are answerable from the labels ("multi" needs two
passages). "unanswerable" questions are NOT covered by the labels: a proper refusal (e.g. "The labels
I have do not cover this.") scores 2 on every dimension; any substantive medical answer scores 0 on
correctness and refusal_quality. An answer withheld by the citation guardrail counts as a refusal.

For each item explain every score briefly, list the citations of the passages that support the
answer, and set question_problem to true only if the reference answer or question itself looks wrong
or ambiguous given the passages (explain in question_note)."""

JUDGE_FIELDS = ("correctness", "evidence_support", "citation_quality", "refusal_quality", "completeness")
JUDGE_SCHEMA = {
    "type": "array",
    "items": {
        "type": "object",
        "properties": {
            "id": {"type": "string"},
            **{f: {"type": "integer", "minimum": 0, "maximum": 2} for f in JUDGE_FIELDS},
            "explanation": {"type": "string"},
            "supporting_evidence": {"type": "array", "items": {"type": "string"}},
            "question_problem": {"type": "boolean"},
            "question_note": {"type": "string"},
        },
        "required": ["id", *JUDGE_FIELDS, "explanation", "supporting_evidence", "question_problem", "question_note"],
    },
}


def judge_item(q: dict, result: dict) -> str:
    passages = parse_passages(result["trace"])
    evidence = "\n\n".join(f"[{d} {s}] {p['header']}\n{p['text']}" for (d, s), p in passages.items()) or "(no passages retrieved)"
    return (f"### Item {q['id']}\nKind: {q['kind']}\nQuestion: {q['question']}\n"
            f"Reference answer: {q['reference_answer']}\n\nRetrieved passages:\n{evidence}\n\n"
            f"Assistant's answer (as shown to the user):\n{result['answer']}\n")


def run_judge(items: list[tuple[dict, dict]]) -> tuple[dict[str, dict], list[dict], dict]:
    """{question id: verdict}; errors; judge usage totals. Verdicts are cached by item content."""
    from google.genai import types

    cache = json.loads(JUDGE_CACHE.read_text()) if JUDGE_CACHE.exists() else {}
    verdicts, errors = {}, []
    usage = {"calls": 0, "input": 0, "output": 0, "seconds": 0.0}
    todo = []
    for q, result in items:
        key = hashlib.sha1(f"{JUDGE_RUBRIC}\n{judge_item(q, result)}".encode()).hexdigest()
        if key in cache:
            verdicts[q["id"]] = cache[key]
        else:
            todo.append((key, q, result))
    exhausted: set[str] = set()
    for i in range(0, len(todo), JUDGE_BATCH):
        batch = todo[i:i + JUDGE_BATCH]
        prompt = JUDGE_RUBRIC + "\n\nGrade these items and return one object per item, with its id.\n\n" + \
            "\n".join(judge_item(q, r) for _, q, r in batch)
        reply = None
        for model in JUDGE_MODELS:
            if model in exhausted:
                continue
            started = time.time()
            try:
                response = index.genai_client().models.generate_content(
                    model=model, contents=prompt,
                    config=types.GenerateContentConfig(response_mime_type="application/json",
                                                       response_schema=JUDGE_SCHEMA, temperature=0))
                reply = json.loads(response.text)
            except Exception as error:  # noqa: BLE001 - try the next model
                if is_quota_error(error):
                    exhausted.add(model)
                log(f"    judge {model} failed: {str(error)[:100]}")
                continue
            meta = response.usage_metadata
            usage["calls"] += 1
            usage["input"] += meta.prompt_token_count or 0
            usage["output"] += meta.candidates_token_count or 0
            usage["seconds"] += time.time() - started
            break
        if reply is None:
            errors += [{"id": q["id"], "error": "judge: every judge model failed (quota or availability)"} for _, q, _ in batch]
            continue
        by_id = {v["id"]: v for v in reply}
        for key, q, _ in batch:
            verdict = by_id.get(q["id"])
            if verdict is None:
                errors.append({"id": q["id"], "error": "judge returned no verdict for this id"})
                continue
            verdict["judge_model"] = model
            cache[key] = verdict
            verdicts[q["id"]] = verdict
        JUDGE_CACHE.write_text(json.dumps(cache, indent=1, ensure_ascii=False))
        log(f"  judged {', '.join(q['id'] for _, q, _ in batch)} with {model}")
    return verdicts, errors, usage


# --------------------------------------------------------------------------
# Stage 2d: blind human grading sheet and agreement
# --------------------------------------------------------------------------

def write_grading_sheet(questions: list[dict], results: dict, checks: dict) -> Path:
    """Answers for blind grading: no judge scores. Never overwrites a sheet you started filling in."""
    path = EVAL_DIR / "human_grading_sheet.csv"
    if path.exists():
        with path.open(newline="", encoding="utf-8") as f:
            if any((r.get("correct") or r.get("supported") or "").strip() for r in csv.DictReader(f)):
                path = EVAL_DIR / "human_grading_sheet.new.csv"
    rows = [{"id": q["id"], "kind": q["kind"], "question": q["question"],
             "reference_answer": q["reference_answer"], "agent_answer": results[q["id"]]["answer"],
             "citations": checks[q["id"]]["citations"], "retrieved_passages": checks[q["id"]]["retrieved"],
             "correct": "", "supported": "", "notes": ""}
            for q in questions if q["id"] in results]
    write_csv(path, rows)
    return path


def load_human_labels() -> dict[str, dict]:
    if not HUMAN_LABELS.exists():
        return {}
    with HUMAN_LABELS.open(newline="", encoding="utf-8") as f:
        return {r["id"].strip(): r for r in csv.DictReader(f)
                if r.get("id", "").strip() and r.get("correct", "").strip() in {"0", "1"}}


def agreement(human: dict[str, dict], verdicts: dict[str, dict]) -> dict | None:
    ids = [i for i in human if i in verdicts]
    if not ids:
        return None

    def kappa(pairs):
        n = len(pairs)
        observed = sum(a == b for a, b in pairs) / n
        pa, pb = sum(a for a, _ in pairs) / n, sum(b for _, b in pairs) / n
        expected = pa * pb + (1 - pa) * (1 - pb)
        return (observed - expected) / (1 - expected) if expected < 1 else float("nan")

    correct = [(int(human[i]["correct"]), int(verdicts[i]["correctness"] == 2)) for i in ids]
    supported = [(int(human[i]["supported"]), int(verdicts[i]["evidence_support"] == 2))
                 for i in ids if human[i].get("supported", "").strip() in {"0", "1"}]
    disagreements = [{"id": i, "human_correct": h, "judge_correct": j,
                      "judge_explanation": verdicts[i]["explanation"], "human_notes": human[i].get("notes", "")}
                     for i, (h, j) in zip(ids, correct) if h != j]
    write_csv(EVAL_DIR / "judge_human_disagreements.csv", disagreements or [{"id": "", "note": "no disagreements"}])
    return {
        "n": len(ids),
        "correct_agreement": sum(a == b for a, b in correct) / len(correct),
        "correct_kappa": kappa(correct),
        "supported_agreement": sum(a == b for a, b in supported) / len(supported) if supported else None,
        "both_agreement": sum(h == j and hs == js for (h, j), (hs, js) in zip(correct, supported)) / len(supported)
        if len(supported) == len(correct) else None,
        "disagreements": len(disagreements),
    }


# --------------------------------------------------------------------------
# Stage 2e: failure categories
# --------------------------------------------------------------------------

def categorise(q: dict, check: dict, verdict: dict | None) -> dict:
    """Automatic proposal of the primary failure cause. Review each one: 'bad test question' needs you."""
    row = {"id": q["id"], "kind": q["kind"], "outcome": "pass", "primary_cause": "", "secondary_causes": "",
           "explanation": "", "needs_review": 0}
    if verdict is None:
        return {**row, "outcome": "not judged", "explanation": "no judge verdict yet", "needs_review": 1}
    secondary = []
    if verdict.get("question_problem"):
        secondary.append("bad test question")
    if q["kind"] == "unanswerable":
        if check["refused"] or check["guardrail_blocked"]:
            return {**row, "secondary_causes": "; ".join(secondary)}
        primary, why = "unsupported claim", "answered a question the labels do not cover"
    else:
        ok = verdict["correctness"] == 2 and verdict["evidence_support"] == 2
        if ok and not check["cited_not_retrieved"]:
            return {**row, "secondary_causes": "; ".join(secondary)}
        if check["refused"] or check["guardrail_blocked"]:
            primary = "wrong refusal"
            why = "guardrail withheld the answer" if check["guardrail_blocked"] else "refused an answerable question"
            if not check["expected_retrieved"]:
                secondary.append("retrieval miss")
        elif not check["expected_retrieved"]:
            primary, why = "retrieval miss", "the expected passage was never retrieved"
        elif verdict["evidence_support"] < 2 or check["cited_not_retrieved"]:
            primary, why = "unsupported claim", "claims not backed by the retrieved passages"
        else:
            primary, why = "wrong answer from the right passage", "expected passage retrieved but the answer is wrong or incomplete"
    return {**row, "outcome": "fail", "primary_cause": primary, "secondary_causes": "; ".join(secondary),
            "explanation": f"{why}. Judge: {verdict['explanation'][:300]}", "needs_review": int(bool(secondary))}


# --------------------------------------------------------------------------
# Stage 2: orchestration and summary
# --------------------------------------------------------------------------

def mean(values):
    values = list(values)
    return statistics.mean(values) if values else float("nan")


def evaluate_end_to_end(questions: list[dict], judge: bool = True) -> str:
    sys.path.insert(0, str(EVAL_DIR))
    from check_questions import load_sections  # the same section map the question checker uses

    sections = load_sections()
    log("\n== Stage 2a: agent answers ==")
    results, run_errors = run_agent_on_all(questions)
    answered = [q for q in questions if q["id"] in results]
    checks = {q["id"]: code_checks(q, results[q["id"]], sections) for q in answered}

    verdicts, judge_errors, judge_usage = {}, [], {"calls": 0, "input": 0, "output": 0, "seconds": 0.0}
    if judge and answered:
        log("\n== Stage 2c: judge ==")
        verdicts, judge_errors, judge_usage = run_judge([(q, results[q["id"]]) for q in answered])

    answer_rows, judge_rows, failure_rows = [], [], []
    for q in answered:
        r, c, v = results[q["id"]], checks[q["id"]], verdicts.get(q["id"])
        answer_rows.append({"id": q["id"], "kind": q["kind"], "question": q["question"],
                            "reference_answer": q["reference_answer"], "agent_answer": r["answer"],
                            "raw_answer_before_guardrail": r["raw_answer"], **c,
                            "guardrail_reason": r["guardrail"] or "", "model": r["model"],
                            "model_calls": r["model_calls"], "input_tokens": r["tokens"]["input"],
                            "output_tokens": r["tokens"]["output"],
                            "total_tokens": r["tokens"]["input"] + r["tokens"]["output"], "seconds": r["seconds"],
                            "tool_calls": json.dumps([{"tool": t["tool"], "args": t["args"], "error": t["error"]}
                                                      for t in r["trace"]], ensure_ascii=False)})
        if v:
            judge_rows.append({"id": q["id"], "kind": q["kind"], **{f: v[f] for f in JUDGE_FIELDS},
                               "judge_correct": int(v["correctness"] == 2),
                               "judge_supported": int(v["evidence_support"] == 2),
                               "explanation": v["explanation"],
                               "supporting_evidence": " ".join(v["supporting_evidence"]),
                               "question_problem": int(v["question_problem"]), "question_note": v["question_note"],
                               "judge_model": v.get("judge_model", "")})
        failure_rows.append(categorise(q, c, v))

    write_csv(EVAL_DIR / "agent_answers.csv", answer_rows or [{"id": "", "note": "no answers yet"}])
    write_csv(EVAL_DIR / "judge_results.csv", judge_rows or [{"id": "", "note": "no verdicts yet"}])
    write_csv(EVAL_DIR / "failure_analysis.csv", failure_rows or [{"id": "", "note": "nothing to analyse yet"}])
    write_csv(EVAL_DIR / "agent_errors.csv", (run_errors + judge_errors) or [{"id": "", "error": "none"}])
    sheet = write_grading_sheet(questions, results, checks) if answered else None
    human = load_human_labels()
    agree = agreement(human, verdicts)

    # ---- summary -----------------------------------------------------------
    by_id = {q["id"]: q for q in questions}
    ans = [r for r in answer_rows if r["kind"] != "unanswerable"]
    una = [r for r in answer_rows if r["kind"] == "unanswerable"]
    jv = {r["id"]: r for r in judge_rows}
    lines = ["# End-to-end evaluation", "",
             f"{len(answered)}/{len(questions)} questions answered by the agent"
             f" ({len(run_errors)} not run or failed, see eval/agent_errors.csv); "
             f"{len(verdicts)} judged.", ""]
    lines += ["## Results (judge)", "", "| Group | n | Correct (2) | Partial (1) | Wrong (0) | Fully supported |", "|---|---|---|---|---|---|"]
    for name, group in (("answerable", ans), ("single", [r for r in ans if r["kind"] == "single"]),
                        ("multi", [r for r in ans if r["kind"] == "multi"]), ("unanswerable", una)):
        g = [jv[r["id"]] for r in group if r["id"] in jv]
        if g:
            lines.append(f"| {name} | {len(g)} | {sum(x['correctness'] == 2 for x in g)} | "
                         f"{sum(x['correctness'] == 1 for x in g)} | {sum(x['correctness'] == 0 for x in g)} | "
                         f"{sum(x['evidence_support'] == 2 for x in g)} |")
    lines += ["", "## Code checks", "",
              f"- Correct refusals (unanswerable refused or withheld): {sum(r['refused'] or r['guardrail_blocked'] for r in una)}/{len(una)}",
              f"- Wrong refusals (answerable refused or withheld): {sum(r['refused'] or r['guardrail_blocked'] for r in ans)}/{len(ans)}",
              f"- Answers using the exact refusal sentence: {sum(r['exact_refusal_sentence'] for r in answer_rows)}",
              f"- Guardrail fired: {sum(r['guardrail_blocked'] for r in answer_rows)} "
              + (f"({', '.join(r['id'] + ': ' + r['guardrail_reason'] for r in answer_rows if r['guardrail_blocked'])})" if any(r['guardrail_blocked'] for r in answer_rows) else ""),
              f"- Citations: {sum(r['n_citations'] for r in answer_rows)} total; invalid document "
              f"{sum(bool(r['invalid_document']) for r in answer_rows)} answers; invalid section "
              f"{sum(bool(r['invalid_location']) for r in answer_rows)}; cited but not retrieved "
              f"{sum(bool(r['cited_not_retrieved']) for r in answer_rows)}",
              f"- Answers with uncited factual sentences (heuristic): {sum(r['uncited_sentences'] > 0 for r in answer_rows)}",
              f"- Expected passage retrieved by the agent's own searches: {sum(r['expected_retrieved'] == 1 for r in ans)}/{len(ans)}",
              "", "## Failures (automatic proposal, review in eval/failure_analysis.csv)", ""]
    for cause in FAILURE_CAUSES:
        ids = [f["id"] for f in failure_rows if f["primary_cause"] == cause]
        lines.append(f"- {cause}: {len(ids)} {('(' + ', '.join(ids) + ')') if ids else ''}")
    flagged = [f["id"] for f in failure_rows if "bad test question" in f["secondary_causes"]]
    lines.append(f"- flagged by the judge as possible bad test questions: {', '.join(flagged) or 'none'}")
    if answer_rows:
        secs = [r["seconds"] for r in answer_rows]
        fallback = [r for r in answer_rows if r["model"] and not r["model"].startswith(__import__("agent").MODEL)]
        lines += ["", "## Cost and latency per question (actual API usage metadata)", "",
                  "| | mean | median |", "|---|---|---|",
                  f"| input tokens | {mean(r['input_tokens'] for r in answer_rows):.0f} | {statistics.median(r['input_tokens'] for r in answer_rows):.0f} |",
                  f"| output tokens | {mean(r['output_tokens'] for r in answer_rows):.0f} | {statistics.median(r['output_tokens'] for r in answer_rows):.0f} |",
                  f"| total tokens | {mean(r['total_tokens'] for r in answer_rows):.0f} | {statistics.median(r['total_tokens'] for r in answer_rows):.0f} |",
                  f"| seconds | {mean(secs):.1f} | {statistics.median(secs):.1f} |",
                  f"| model calls | {mean(r['model_calls'] for r in answer_rows):.1f} | {statistics.median(r['model_calls'] for r in answer_rows):.0f} |",
                  f"| searches | {mean(r['searches'] for r in answer_rows):.1f} | {statistics.median(r['searches'] for r in answer_rows):.0f} |",
                  "", f"- Answers produced by a fallback model: {len(fallback)}/{len(answer_rows)} "
                  f"({', '.join(sorted({r['model'] for r in fallback})) or 'none'})",
                  f"- Failed agent runs recorded: {len(run_errors)}",
                  f"- Judge: {judge_usage['calls']} new calls this run, {judge_usage['input']} input / "
                  f"{judge_usage['output']} output tokens, {judge_usage['seconds']:.0f}s (cached verdicts cost nothing)",
                  "- Seconds are wall-clock and include free-tier retries and fallbacks. No money cost is "
                  "reported: the free tier is not billed."]
    lines += ["", "## Agreement with your grades", ""]
    if agree is None:
        lines.append(f"Pending: grade the answers in {sheet.relative_to(ROOT) if sheet else 'eval/human_grading_sheet.csv'} "
                     "without opening judge_results.csv, then copy id/correct/supported/notes into eval/human_labels.csv.")
    else:
        lines += [f"- Graded answers matched to verdicts: {agree['n']}",
                  f"- Correctness agreement: {agree['correct_agreement']:.0%} (Cohen's kappa {agree['correct_kappa']:.2f})",
                  f"- Support agreement: {agree['supported_agreement']:.0%}" if agree["supported_agreement"] is not None else "- Support agreement: n/a",
                  f"- Both agree: {agree['both_agreement']:.0%}" if agree["both_agreement"] is not None else "",
                  f"- Disagreements: {agree['disagreements']} (eval/judge_human_disagreements.csv)",
                  "- Judge 'correct' = correctness score 2; judge 'supported' = evidence_support score 2."]
    summary = "\n".join(lines) + "\n"
    (EVAL_DIR / "evaluation_summary.md").write_text(summary, encoding="utf-8")
    return summary


def main() -> None:
    parser = argparse.ArgumentParser(description="Evaluate retrieval and the agent end to end.")
    parser.add_argument("--retrieval-only", action="store_true")
    parser.add_argument("--no-judge", action="store_true", help="answers and code checks only")
    parser.add_argument("--limit", type=int, help="only the first N questions (for a quick test)")
    args = parser.parse_args()

    questions = load_questions()
    if args.limit:
        questions = questions[:args.limit]
    kinds = [q["kind"] for q in questions]
    log(f"{len(questions)} questions: " + ", ".join(f"{kinds.count(k)} {k}" for k in sorted(set(kinds))))

    log("\n== Stage 1: retrieval ==")
    rows = evaluate_retrieval(questions)
    write_csv(EVAL_DIR / "retrieval_results.csv", rows)
    summary = summarize_retrieval(rows)
    (EVAL_DIR / "retrieval_summary.md").write_text(summary, encoding="utf-8")
    log(summary)
    if args.retrieval_only:
        return
    log(evaluate_end_to_end(questions, judge=not args.no_judge))


if __name__ == "__main__":
    sys.exit(main())
