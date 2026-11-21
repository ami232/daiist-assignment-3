"""
Assignment 3: evaluation (`main.py evaluate`; `python evaluate.py [stage ...] [--ids q01,q02] [--fresh]`).

Stages (all cached in eval/, so a re-run spends no API calls unless inputs change):

  retrieval     Hit@1/3/5 per design (vector, bm25, hybrid), by location and by evidence;
                single = any alternative, multi = any group / all groups; words and latency.
  answers       the agent (agent.run) answers every question; answer, tool trace, retrieved
                passages, guardrail events, tokens and seconds -> eval/answers.jsonl.
  checks        code checks, no API: refusal behaviour, citation validity, expected citation,
                evidence retrieved by the agent, figures not found in the retrieved passages,
                reference figures found in the answer -> eval/code_checks.csv.
  facts         ESSENTIAL FACTS of each question, extracted by the judge model from the question
                and the reference answer ONLY (no agent answer is shown) -> eval/essential_facts.json;
                entries reviewed by the student are marked "frozen" and never regenerated.
  judge         LLM judge with the rubric in eval/judge_rubric.md, the essential facts and the
                retrieved passages as evidence -> eval/judge.jsonl. It never reads human labels.
  agreement     human grades (eval/human_labels.csv, done BEFORE reading the judge) vs judge:
                % agreement and Cohen's kappa -> eval/agreement.json.
  before_after  q30 (final price) on a COPY of the index before and after add_document
                (the price notice) -> eval/before_after.json. The committed index is untouched.
  summary       results by kind, failures, tokens and seconds per question -> eval/summary.json.
"""

from __future__ import annotations

import csv
import hashlib
import json
import os
import re
import shutil
import statistics
import sys
import tempfile
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT / "eval"))
import check_questions as cq  # noqa: E402  (annotation format and matching rules)

EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
PATTERNS = EVAL / "evidence_patterns.json"
ANSWERS = EVAL / "answers.jsonl"
CHECKS = EVAL / "code_checks.csv"
RUBRIC = EVAL / "judge_rubric.md"
FACTS = EVAL / "essential_facts.json"
JUDGE = EVAL / "judge.jsonl"
HUMAN = EVAL / "human_labels.csv"
AGREEMENT = EVAL / "agreement.json"
BEFORE_AFTER = EVAL / "before_after.json"
SUMMARY = EVAL / "summary.json"
KS = (1, 3, 5)
STAGES = ("retrieval", "facts", "answers", "checks", "judge", "agreement", "before_after", "summary",
          "before_after_hybrid")  # the last one is an optional sensitivity test, not run by default
JUDGE_MODEL = os.environ.get("GEMINI_JUDGE_MODEL", "gemini-3.1-flash-lite")
PAUSE_BETWEEN_QUESTIONS = float(os.environ.get("EVAL_PAUSE_SECONDS", "4"))
BEFORE_AFTER_QID = "q30"
ADDED_DOCUMENT = ROOT / "corpus" / "after" / "notice-of-price.pdf"
ADDED_DOCUMENT_URL = "https://ipo.anthropic.com/documents/eu/notice-of-price.pdf"


def log(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


def load_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r["question"].strip()]


def sha(*parts: str) -> str:
    return hashlib.sha256("\x1f".join(parts).encode()).hexdigest()[:16]


def read_jsonl(path: Path) -> dict[str, dict]:
    """Latest non-superseded record per id (superseded attempts stay in the file as an audit trail)."""
    out = {}
    if path.is_file():
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                rec = json.loads(line)
                if not rec.get("superseded"):
                    out[rec["id"]] = rec
    return out


def mark_superseded(path: Path, qid: str, reason: str) -> None:
    """Flag every earlier record of qid as superseded, with the reason, before a new one is appended."""
    lines = path.read_text(encoding="utf-8").splitlines() if path.is_file() else []
    out = []
    for line in lines:
        if line.strip():
            rec = json.loads(line)
            if rec["id"] == qid and not rec.get("superseded"):
                rec.update(superseded=True, superseded_reason=reason)
            line = json.dumps(rec, ensure_ascii=False)
        out.append(line)
    path.write_text("\n".join(out) + ("\n" if out else ""), encoding="utf-8")


def append_jsonl(path: Path, record: dict) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def is_daily_quota_error(error: Exception) -> bool:
    text = str(error)
    return "RESOURCE_EXHAUSTED" in text and ("PerDay" in text or "per day" in text.lower())


# --------------------------------------------------------------------------- retrieval metrics

def group_hit_ranks(hits: list, groups: list[list[tuple[str, str]]], patterns: list[str]) -> list[dict]:
    """For each evidence group, the 1-based rank of the first retrieved chunk that
    satisfies it by location and by evidence (None if not retrieved)."""
    out = []
    for group, pattern in zip(groups, patterns):
        loc_rank = next((r for r, h in enumerate(hits, 1)
                         if any(h.source == s and cq.location_matches(l, h.location) for s, l in group)), None)
        ev_rank = next((r for r, h in enumerate(hits, 1) if re.search(pattern, h.text, re.I)), None)
        out.append({"location": loc_rank, "evidence": ev_rank})
    return out


def hits_at(ranks: list[dict], kind: str, k: int, metric: str) -> dict[str, int]:
    found = [r[metric] is not None and r[metric] <= k for r in ranks]
    if kind == "multi":
        return {"any": int(any(found)), "all": int(all(found))}
    return {"any": int(any(found)), "all": int(any(found))}  # single: one group of alternatives


def run_retrieval(designs: tuple[str, ...], search_fn, k_max: int = 5) -> tuple[list[dict], list[dict]]:
    questions = [q for q in load_questions() if q["kind"] != "unanswerable"]
    patterns = json.loads(PATTERNS.read_text(encoding="utf-8"))
    rows = []
    for design in designs:
        for q in questions:
            groups = cq.parse_expected(q)
            started = time.perf_counter()
            hits = search_fn(q["question"], k_max, design)
            seconds = time.perf_counter() - started
            ranks = group_hit_ranks(hits, groups, patterns[q["id"]])
            row = {"design": design, "id": q["id"], "kind": q["kind"], "seconds": round(seconds, 3),
                   "words_top3": sum(len(h.text.split()) for h in hits[:3]),
                   "words_top5": sum(len(h.text.split()) for h in hits[:5]),
                   "retrieved": " || ".join(f"{h.source} | {h.location} | p. {h.page}" for h in hits)}
            for metric in ("location", "evidence"):
                row[f"{metric}_ranks"] = ";".join("-" if r[metric] is None else str(r[metric]) for r in ranks)
                for k in KS:
                    h = hits_at(ranks, q["kind"], k, metric)
                    row[f"{metric}_any@{k}"], row[f"{metric}_all@{k}"] = h["any"], h["all"]
            rows.append(row)
    summary = []
    for design in designs:
        for subset in ("single", "multi", "all answerable"):
            sel = [r for r in rows if r["design"] == design and (subset == "all answerable" or r["kind"] == subset)]
            if not sel:
                continue
            s = {"design": design, "questions": subset, "n": len(sel)}
            for metric in ("location", "evidence"):
                for k in KS:
                    s[f"{metric}_hit@{k}"] = round(statistics.mean(r[f"{metric}_any@{k}"] for r in sel), 3)
                    if subset != "single":
                        s[f"{metric}_hit_all@{k}"] = round(statistics.mean(r[f"{metric}_all@{k}"] for r in sel), 3)
            s["avg_words_top3"] = round(statistics.mean(r["words_top3"] for r in sel))
            s["avg_words_top5"] = round(statistics.mean(r["words_top5"] for r in sel))
            s["median_seconds"] = round(statistics.median(r["seconds"] for r in sel), 3)
            summary.append(s)
    return rows, summary


def write_csv(path: Path, rows: list[dict]) -> None:
    fields = []
    for r in rows:
        fields += [k for k in r if k not in fields]
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=fields)
        w.writeheader()
        w.writerows(rows)


def stage_retrieval() -> None:
    import retrieval

    rows, summary = run_retrieval(retrieval.DESIGNS, retrieval.search)
    write_csv(EVAL / "retrieval_results.csv", rows)
    write_csv(EVAL / "retrieval_summary.csv", summary)
    log("\nRetrieval (answerable questions; hit = any alternative / any group):")
    for s in summary:
        log(f"  {s['design']:7} {s['questions']:15} n={s['n']:2}  "
            f"loc@1/3/5 {s['location_hit@1']:.2f}/{s['location_hit@3']:.2f}/{s['location_hit@5']:.2f}  "
            f"evid@1/3/5 {s['evidence_hit@1']:.2f}/{s['evidence_hit@3']:.2f}/{s['evidence_hit@5']:.2f}  "
            f"words(top5) {s['avg_words_top5']}")


# --------------------------------------------------------------------------- answers

def answer_key(q: dict) -> str:
    import agent
    import server

    return sha(q["question"], agent.MODEL, (ROOT / "AGENTS.md").read_text(encoding="utf-8"), server.SEARCH_DESIGN)


def reject_all(request: dict) -> dict:
    return {"type": "reject", "message": "Evaluation run: documents are never added here."}


def stage_answers(ids: set[str] | None, fresh: bool) -> None:
    import agent

    cache = read_jsonl(ANSWERS)
    todo = [q for q in load_questions() if not ids or q["id"] in ids]
    for n, q in enumerate(todo, 1):
        key = answer_key(q)
        if not fresh and cache.get(q["id"], {}).get("key") == key and not cache[q["id"]].get("error"):
            continue
        log(f"answers: {q['id']} ({n}/{len(todo)})")
        record = {"id": q["id"], "key": key, "kind": q["kind"]}
        if q["id"] in cache:
            mark_superseded(ANSWERS, q["id"], "replaced by a later run (--fresh, error or changed inputs)")
        try:
            record.update(agent.run(q["question"], approve=reject_all))
        except Exception as error:  # noqa: BLE001 - keep going, record the failure
            record.update(error=f"{type(error).__name__}: {str(error)[:500]}")
            append_jsonl(ANSWERS, record)
            if is_daily_quota_error(error):
                log("answers: daily chat quota exhausted; stopping (cached answers are kept)")
                return
            continue
        append_jsonl(ANSWERS, record)
        time.sleep(PAUSE_BETWEEN_QUESTIONS)


# --------------------------------------------------------------------------- code checks

NUMBER_RE = re.compile(r"(?<![\w.])\$?\(?\d[\d,]*(?:\.\d+)?\)?%?")
TRIVIAL_NUMBERS = {"1", "2", "3", "4", "5", "10", "2023", "2024", "2025", "2026", "2027"}


def numbers(text: str) -> set[str]:
    """Figures in a text, normalised ('$(41,965)' -> '41,965'); citations removed first."""
    text = re.sub(r"\[[A-Z][A-Z0-9-]+ \|[^\]]*\]", " ", text)       # answer citations
    text = re.sub(r"\[[A-Z][A-Z0-9-]+,[^\]]*\]", " ", text)         # source notes in the reference
    out = set()
    for raw in NUMBER_RE.findall(text):
        n = raw.strip("$()%").rstrip(".,")
        if n and n not in TRIVIAL_NUMBERS and not re.fullmatch(r"\d", n):
            out.add(n)
    return out


def stage_checks() -> None:
    from langchain_core.messages import ToolMessage

    import agent

    patterns = json.loads(PATTERNS.read_text(encoding="utf-8"))
    answers = read_jsonl(ANSWERS)
    rows = []
    for q in load_questions():
        a = answers.get(q["id"])
        if not a or a.get("error"):
            rows.append({"id": q["id"], "kind": q["kind"], "status": "missing" if not a else "error"})
            continue
        retrieved_text = "\n".join(a.get("retrieved", []))
        retrieved = agent.retrieved_citations(
            [ToolMessage(content=t, tool_call_id=f"stored-{n}", name="search") for n, t in enumerate(a.get("retrieved", []))])
        citation = agent.check_citations(a["answer"], retrieved)
        partial = int(a.get("partial_refusal", bool(re.search(r"(?m)^\s*NOT IN CORPUS:", a["answer"])) and not a["refusal"]))
        row = {"id": q["id"], "kind": q["kind"], "status": "ok", "refusal": int(a["refusal"]), "partial_refusal": partial,
               "citations": len(a.get("citations", [])), "citations_valid": int(citation["ok"] or a["refusal"]),
               "searches": sum(t["tool"] == "search" for t in a.get("tool_calls", [])),
               "guardrail_fired": int(any(e["event"] == "guardrail" for e in a.get("events", [])))}
        answer_numbers = numbers(a["answer"])
        unsupported = sorted(n for n in answer_numbers if n not in retrieved_text)
        row["numbers_in_answer"] = len(answer_numbers)
        row["numbers_not_in_passages"] = ";".join(unsupported)
        if q["kind"] == "unanswerable":
            row["correct_refusal"] = int(a["refusal"])   # a partial answer to an unanswerable question is not a refusal
        else:
            row["wrong_refusal"] = int(a["refusal"])
            groups = cq.parse_expected(q)
            cited = agent.find_citations(a["answer"])
            row["cites_expected_all"] = int(all(any(s == cs and cq.location_matches(l, cl) for s, l in g for cs, cl, _ in cited)
                                                for g in groups))
            row["evidence_retrieved_all"] = int(all(re.search(p, retrieved_text, re.I) for p in patterns[q["id"]]))
            ref = numbers(q["reference_answer"])
            row["reference_numbers_found"] = f"{len([n for n in ref if n in answer_numbers])}/{len(ref)}"
        rows.append(row)
    write_csv(CHECKS, rows)
    log(f"checks: {sum(r['status'] == 'ok' for r in rows)} answers checked -> {CHECKS.name}")


# --------------------------------------------------------------------------- judge

FACTS_TEMPLATE = """You prepare grading criteria for a question about the Anthropic IPO filings.
You see only the question and the evaluator's reference answer; no assistant answer exists yet.

QUESTION:
{question}

QUESTION TYPE: {kind}

REFERENCE ANSWER:
{reference}

List the ESSENTIAL FACTS: the facts the QUESTION explicitly asks for, exactly as the reference
states them (each figure with its unit, period and basis; dates; share classes; parties;
conditions), one short self-contained statement each. Put context and details the question
did not ask for under "secondary". Ignore bracketed source notes. If the question type is
unanswerable, the only essential fact is that the requested information is not in the corpus;
list under "must_not_state" what an answer must not present as the missing fact.

Reply with JSON only: {{"essential": ["..."], "secondary": ["..."], "must_not_state": ["..."]}}"""


def model_text(response) -> str:
    content = response.content
    if isinstance(content, str):
        return content
    return "".join(p.get("text", "") if isinstance(p, dict) else str(p) for p in content)


def stage_facts(ids: set[str] | None, fresh: bool, model=None) -> dict:
    """Answer-blind: the prompt holds only the question and the reference, so the criteria
    cannot be adapted to what the agent answered."""
    cache = json.loads(FACTS.read_text(encoding="utf-8")) if FACTS.is_file() else {}
    model = model or judge_model()
    name = getattr(model, "model", JUDGE_MODEL)
    for q in load_questions():
        if ids and q["id"] not in ids:
            continue
        if cache.get(q["id"], {}).get("frozen"):
            continue  # reviewed and frozen by the student: never regenerated, even with --fresh
        key = sha(q["question"], q["reference_answer"], q["kind"], FACTS_TEMPLATE, name)
        if not fresh and cache.get(q["id"], {}).get("key") == key:
            continue
        log(f"facts: {q['id']}")
        try:
            response = model.invoke(FACTS_TEMPLATE.format(question=q["question"], kind=q["kind"],
                                                          reference=q["reference_answer"]))
            match = re.search(r"\{.*\}", model_text(response), re.S)
            facts = json.loads(match.group(0)) if match else None
            if not facts or not isinstance(facts.get("essential"), list) or not facts["essential"]:
                raise ValueError(f"no essential facts in: {model_text(response)[:200]}")
        except Exception as error:  # noqa: BLE001
            if is_daily_quota_error(error):
                log("facts: daily chat quota exhausted; stopping (cached facts are kept)")
                break
            log(f"facts: {q['id']} failed: {type(error).__name__}: {str(error)[:200]}")
            continue
        cache[q["id"]] = {"key": key, "model": name, "essential": facts["essential"],
                          "secondary": facts.get("secondary", []), "must_not_state": facts.get("must_not_state", [])}
        FACTS.write_text(json.dumps(dict(sorted(cache.items())), indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return cache


def format_facts(entry: dict) -> str:
    lines = [f"- {f}" for f in entry["essential"]]
    if entry.get("must_not_state"):
        lines += ["Must NOT be stated as the answer:"] + [f"- {f}" for f in entry["must_not_state"]]
    if entry.get("secondary"):
        lines += ["Secondary (not required):"] + [f"- {f}" for f in entry["secondary"]]
    return "\n".join(lines)


JUDGE_TEMPLATE = """You are grading an AI assistant's answer about the Anthropic IPO filings.

RUBRIC (follow it exactly):
{rubric}

QUESTION:
{question}

QUESTION TYPE: {kind}

REFERENCE ANSWER (written by the evaluator from the documents):
{reference}

ESSENTIAL FACTS (fixed before any answer was seen):
{facts}

PASSAGES THE ASSISTANT RETRIEVED (the only admissible evidence):
{passages}

ASSISTANT'S ANSWER:
{answer}

Grade the two labels separately, in this order:
1. CORRECT: compare the answer with each essential fact (and the reference). Do not consider
   whether its claims appear in the passages; an extra claim that does not contradict the
   reference does not change CORRECT.
2. SUPPORTED: check every factual claim and citation against the passages. Do not consider
   the reference answer.

Reply with JSON only:
{{"correct_reason": "<one sentence>", "correct": 0 or 1, "supported_reason": "<one sentence>", "supported": 0 or 1}}"""


def judge_model():
    import agent

    # same request limiter and daily budget as the agent; default thinking for grading
    return agent.chat_model(JUDGE_MODEL, reasoning_effort=None)


def parse_verdict(text: str) -> dict:
    match = re.search(r"\{.*\}", text, re.S)
    if not match:
        raise ValueError(f"judge did not return JSON: {text[:200]}")
    verdict = json.loads(match.group(0))
    return {"correct": int(verdict["correct"]), "supported": int(verdict["supported"]),
            "correct_reason": str(verdict.get("correct_reason", ""))[:400],
            "supported_reason": str(verdict.get("supported_reason", ""))[:400]}


def stage_judge(ids: set[str] | None, fresh: bool, model=None) -> None:
    if not RUBRIC.is_file():
        raise SystemExit(f"{RUBRIC.relative_to(ROOT)} is missing: write the judge rubric first.")
    rubric = RUBRIC.read_text(encoding="utf-8")
    answers, cache = read_jsonl(ANSWERS), read_jsonl(JUDGE)
    model = model or judge_model()
    todo = {q["id"] for q in load_questions() if q["id"] in answers and not answers[q["id"]].get("error")}
    facts = stage_facts(ids & todo if ids else todo, fresh=False, model=model)  # cached; answer-blind
    for q in load_questions():
        a = answers.get(q["id"])
        if (ids and q["id"] not in ids) or not a or a.get("error") or q["id"] not in facts:
            continue
        key = sha(a["answer"], q["reference_answer"], json.dumps(facts[q["id"]]["essential"]), rubric,
                  getattr(model, "model", JUDGE_MODEL))
        if not fresh and cache.get(q["id"], {}).get("key") == key:
            continue
        prompt = JUDGE_TEMPLATE.format(rubric=rubric, question=q["question"], kind=q["kind"],
                                       reference=q["reference_answer"], facts=format_facts(facts[q["id"]]),
                                       passages="\n\n".join(a.get("retrieved", [])) or "(none)", answer=a["answer"])
        log(f"judge: {q['id']}")
        started = time.perf_counter()
        try:
            response = model.invoke(prompt)
            record = {"id": q["id"], "key": key, **parse_verdict(model_text(response)),
                      "judge_model": getattr(model, "model", JUDGE_MODEL),
                      "tokens": (response.usage_metadata or {}).get("total_tokens", 0),
                      "seconds": round(time.perf_counter() - started, 2)}
        except Exception as error:  # noqa: BLE001
            if is_daily_quota_error(error):
                log("judge: daily chat quota exhausted; stopping (cached verdicts are kept)")
                return
            log(f"judge: {q['id']} failed: {type(error).__name__}: {str(error)[:200]}")
            continue
        append_jsonl(JUDGE, record)
        time.sleep(PAUSE_BETWEEN_QUESTIONS)


# --------------------------------------------------------------------------- agreement

def cohen_kappa(a: list[int], b: list[int]) -> float | None:
    n = len(a)
    if n == 0:
        return None
    po = sum(x == y for x, y in zip(a, b)) / n
    pa, pb = sum(a) / n, sum(b) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return None if pe == 1 else round((po - pe) / (1 - pe), 3)


def confusion(h: list[int], j: list[int]) -> dict:
    """Rows = human label, columns = judge label."""
    return {f"human_{a}_judge_{b}": sum(x == a and y == b for x, y in zip(h, j)) for a in (1, 0) for b in (1, 0)}


def agreement_block(h: list[int], j: list[int], ids: list[str]) -> dict:
    kappa = cohen_kappa(h, j)
    constant = [name for name, labels in (("human", h), ("judge", j)) if labels and len(set(labels)) == 1]
    note = None
    if constant:  # chance agreement equals observed structure: kappa is 0 or undefined, not a measure of agreement
        note = (f"kappa not interpretable: {' and '.join(constant)} labels have no variance "
                f"(all {h[0] if 'human' in constant else j[0]})")
    return {"n": len(ids),
            "agreement": round(sum(x == y for x, y in zip(h, j)) / len(ids), 3) if ids else None,
            "cohen_kappa": None if constant else kappa,
            "kappa_note": note,
            "confusion": confusion(h, j),
            "human_positive_rate": round(sum(h) / len(h), 3) if h else None,
            "judge_positive_rate": round(sum(j) / len(j), 3) if j else None,
            "disagreements": [i for i, x, y in zip(ids, h, j) if x != y]}


def stage_agreement() -> None:
    """The only stage that reads the human labels (after the judge has run)."""
    if not HUMAN.is_file():
        log("agreement: eval/human_labels.csv not found; skipped")
        return
    with HUMAN.open(newline="", encoding="utf-8") as f:
        human = {r["id"].strip(): r for r in csv.DictReader(f) if (r.get("id") or "").strip()}
    judge = read_jsonl(JUDGE)
    kinds = {q["id"]: q["kind"] for q in load_questions()}
    both = sorted(set(human) & set(judge))
    result = {"n": len(both)}
    for field in ("correct", "supported"):
        h = [int(human[i][field]) for i in both]
        j = [int(judge[i][field]) for i in both]
        result[field] = agreement_block(h, j, both)
        result[field]["by_kind"] = {}
        for kind in ("single", "multi", "unanswerable"):
            sel = [n for n, i in enumerate(both) if kinds[i] == kind]
            result[field]["by_kind"][kind] = {
                "n": len(sel), "agreement": round(sum(h[n] == j[n] for n in sel) / len(sel), 3) if sel else None,
                "human_positive": sum(h[n] for n in sel), "judge_positive": sum(j[n] for n in sel)}
    AGREEMENT.write_text(json.dumps(result, indent=2) + "\n", encoding="utf-8")
    log(f"agreement: n={result['n']}  correct {result['correct']['agreement']} (kappa {result['correct']['cohen_kappa']})  "
        f"supported {result['supported']['agreement']} (kappa {result['supported']['cohen_kappa']}"
        f"{'; ' + result['supported']['kappa_note'] if result['supported']['kappa_note'] else ''})")


# --------------------------------------------------------------------------- before / after

def index_fingerprint(index_dir: Path) -> dict:
    """Content fingerprint of an index (ids, texts, metadata of every stored chunk), read in a
    separate process so this process never opens the original collection for writing."""
    import subprocess

    code = ("import hashlib, json, index as ix; c = ix.collection(); "
            "d = c.get(include=['documents', 'metadatas']); "
            "rows = sorted(zip(d['ids'], d['documents'], [json.dumps(m, sort_keys=True) for m in d['metadatas']])); "
            "print(json.dumps({'vectors': c.count(), 'sha256': hashlib.sha256(json.dumps(rows).encode()).hexdigest(), "
            "'sources': sorted({m['source'] for m in d['metadatas']})}))")
    out = subprocess.run([sys.executable, "-c", code], cwd=ROOT, capture_output=True, text=True, check=True,
                         env={**os.environ, "CORPUS_INDEX_DIR": str(index_dir)})
    return json.loads(out.stdout.strip().splitlines()[-1])


def answer_trace(record: dict) -> dict:
    """What the report needs from one agent run: answer, citations and their validity, and
    the passages each search returned (by citation)."""
    from langchain_core.messages import ToolMessage

    import agent

    retrieved = agent.retrieved_citations(
        [ToolMessage(content=t, tool_call_id=f"r{n}", name="search") for n, t in enumerate(record.get("retrieved", []))])
    check = agent.check_citations(record["answer"], retrieved)
    return {
        "answer": record["answer"], "refusal": record["refusal"], "citations": record.get("citations", []),
        "citations_valid": check["ok"] or record["refusal"], "citation_problem": check["problem"],
        "searches": [t["args"].get("query") for t in record.get("tool_calls", []) if t["tool"] == "search"],
        "retrieved_passages": [[m.group(0) for m in agent.RESULT_RE.finditer(t)] for t in record.get("retrieved", [])],
        "events": record.get("events", []), "model_calls": record.get("model_calls"),
        "input_tokens": record.get("input_tokens"), "output_tokens": record.get("output_tokens"),
        "seconds": record.get("seconds"), "models_used": record.get("models_used"),
    }


def stage_before_after(fresh: bool) -> None:
    """q30 before/after adding the final price notice. BEFORE is the frozen, evaluated answer;
    AFTER re-asks the same question with the same model, AGENTS.md and retrieval design on a
    COPY of the index to which add_document (through the MCP server) added the notice. The
    committed index and eval/answers.jsonl are fingerprinted before and after."""
    import asyncio

    import agent
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    if BEFORE_AFTER.is_file() and not fresh:
        log("before_after: cached result kept (use --fresh to redo)")
        return
    q = next(q for q in load_questions() if q["id"] == BEFORE_AFTER_QID)
    frozen = read_jsonl(ANSWERS).get(q["id"])
    if not frozen or frozen.get("error"):
        raise SystemExit("before_after: run the answers stage first (the frozen q30 answer is the baseline)")
    same_setup = frozen["key"] == answer_key(q)  # same question, model, AGENTS.md and retrieval design
    if not same_setup:
        raise SystemExit("before_after: model, AGENTS.md or retrieval design changed since the frozen answer")
    if not ADDED_DOCUMENT.is_file():
        import httpx

        ADDED_DOCUMENT.parent.mkdir(parents=True, exist_ok=True)
        ADDED_DOCUMENT.write_bytes(httpx.get(ADDED_DOCUMENT_URL, timeout=60, follow_redirects=True).content)

    original_index = ROOT / "index"
    answers_sha = hashlib.sha256(ANSWERS.read_bytes()).hexdigest()
    original_before = index_fingerprint(original_index)
    with tempfile.TemporaryDirectory() as tmp:
        index_copy = Path(tmp) / "index"
        shutil.copytree(original_index, index_copy)
        env = {"CORPUS_INDEX_DIR": str(index_copy)}
        copy_before = index_fingerprint(index_copy)

        async def add_twice() -> list[str]:  # second call shows the duplicate policy
            params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT),
                                           env={**os.environ, **env})
            reports = []
            async with stdio_client(params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    for _ in range(2):
                        res = await session.call_tool("add_document", {"path": str(ADDED_DOCUMENT.relative_to(ROOT))})
                        reports.append("\n".join(getattr(c, "text", "") for c in res.content))
            return reports

        add_report, duplicate_report = asyncio.run(add_twice())
        copy_after = index_fingerprint(index_copy)
        registry = json.loads((index_copy / "added_documents.json").read_text(encoding="utf-8"))
        after = agent.run(q["question"], approve=reject_all, server_env=env)
    original_after = index_fingerprint(original_index)

    after_trace = answer_trace(after)
    after_trace["cites_added_document"] = any(c.startswith("[NOTICE-OF-PRICE") for c in after_trace["citations"])
    after_trace["added_document_retrieved"] = any(c.startswith("[1] [NOTICE-OF-PRICE") or "[NOTICE-OF-PRICE" in c
                                                  for search in after_trace["retrieved_passages"] for c in search)
    result = {
        "question_id": q["id"], "question": q["question"], "reference_answer": q["reference_answer"],
        "setup": {"model": agent.MODEL, "retrieval_design": "vector (server default), k = 5",
                  "agents_md_unchanged_since_frozen_answer": same_setup},
        "document": {"file": str(ADDED_DOCUMENT.relative_to(ROOT)), "url": ADDED_DOCUMENT_URL,
                     "sha256": hashlib.sha256(ADDED_DOCUMENT.read_bytes()).hexdigest(),
                     "bytes": ADDED_DOCUMENT.stat().st_size, "registry_entry": registry},
        "add_document_report": add_report, "add_document_again_report": duplicate_report,
        "index_copy": {"before": copy_before, "after": copy_after},
        "before": {"source": "frozen answer from eval/answers.jsonl (evaluated with the 35 questions)",
                   **answer_trace(frozen)},
        "after": after_trace,
        "originals_unchanged": {"index": original_before == original_after,
                                "answers_jsonl": answers_sha == hashlib.sha256(ANSWERS.read_bytes()).hexdigest(),
                                "index_fingerprint": original_after},
    }
    BEFORE_AFTER.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    log(f"before_after: before refusal={frozen['refusal']}  after refusal={after['refusal']}  "
        f"cites notice={after_trace['cites_added_document']}  originals unchanged={result['originals_unchanged']['index']}")


def _usage_snapshot() -> dict:
    import agent
    import index as ix

    chat = json.loads(agent.CHAT_USAGE_FILE.read_text()) if agent.CHAT_USAGE_FILE.is_file() else {}
    emb = json.loads(ix.USAGE_FILE.read_text()) if ix.USAGE_FILE.is_file() else {}
    return {"chat": {f"{d}/{m}": n for d, ms in chat.items() for m, n in ms.items()}, "embeddings": emb}


def stage_before_after_hybrid(fresh: bool) -> None:
    """Exploratory sensitivity test run AFTER the official before/after and its diagnosis:
    same question, model, AGENTS.md, guardrails and k = 5 on a fresh copy of the index with
    the notice added through add_document; ONLY the retrieval design changes (vector ->
    hybrid). One run, recorded as it comes; the official result is not modified."""
    import asyncio

    import agent
    from mcp import ClientSession, StdioServerParameters
    from mcp.client.stdio import stdio_client

    if not BEFORE_AFTER.is_file():
        raise SystemExit("before_after_hybrid: run the official before_after stage first")
    result = json.loads(BEFORE_AFTER.read_text(encoding="utf-8"))
    if "sensitivity_hybrid" in result and not fresh:
        log("before_after_hybrid: cached result kept (use --fresh to redo)")
        return
    official = json.dumps({k: v for k, v in result.items() if k != "sensitivity_hybrid"}, sort_keys=True)
    q = next(q for q in load_questions() if q["id"] == BEFORE_AFTER_QID)
    usage_before = _usage_snapshot()
    original_index = ROOT / "index"
    original_before = index_fingerprint(original_index)
    with tempfile.TemporaryDirectory() as tmp:
        index_copy = Path(tmp) / "index"
        shutil.copytree(original_index, index_copy)
        env = {"CORPUS_INDEX_DIR": str(index_copy), "CORPUS_SEARCH_DESIGN": "hybrid"}

        async def add() -> str:
            params = StdioServerParameters(command=sys.executable, args=["server.py"], cwd=str(ROOT),
                                           env={**os.environ, **env})
            async with stdio_client(params) as (read, write):
                async with ClientSession(read, write) as session:
                    await session.initialize()
                    res = await session.call_tool("add_document", {"path": str(ADDED_DOCUMENT.relative_to(ROOT))})
                    return "\n".join(getattr(c, "text", "") for c in res.content)

        add_report = asyncio.run(add())
        copy_after = index_fingerprint(index_copy)
        run = agent.run(q["question"], approve=reject_all, server_env=env)
    original_after = index_fingerprint(original_index)
    usage_after = _usage_snapshot()

    trace = answer_trace(run)
    ranks = []
    for search in trace["retrieved_passages"]:
        pos = next((n for n, c in enumerate(search, 1) if "[NOTICE-OF-PRICE |" in c), None)
        ranks.append(pos)
    trace.update(
        retrieval_design_in_results=sorted({m.group(1) for t in run.get("retrieved", [])
                                            for m in re.finditer(r"\(design: (\w+), top", t)}),
        notice_rank_per_search=ranks,
        cites_added_document=any(c.startswith("[NOTICE-OF-PRICE") for c in trace["citations"]),
        states_83=bool(re.search(r"\$\s?83(\.00)?\b", run["answer"])))
    delta = {k: {key: usage_after[k].get(key, 0) - usage_before[k].get(key, 0)
                 for key in usage_after[k] if usage_after[k].get(key, 0) != usage_before[k].get(key, 0)}
             for k in ("chat", "embeddings")}
    result["sensitivity_hybrid"] = {
        "status": "exploratory sensitivity test, run once after the official experiment and its diagnosis; "
                  "does not replace the official result",
        "changed": "retrieval design vector -> hybrid (CORPUS_SEARCH_DESIGN=hybrid); k = 5; everything else as official",
        "add_document_report": add_report, "index_copy_after": copy_after,
        "after_hybrid": trace, "api_usage": delta,
        "originals_unchanged": {"index": original_before == original_after,
                                "answers_jsonl_sha256": hashlib.sha256(ANSWERS.read_bytes()).hexdigest()},
    }
    assert json.dumps({k: v for k, v in result.items() if k != "sensitivity_hybrid"}, sort_keys=True) == official
    BEFORE_AFTER.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    log(f"before_after_hybrid: refusal={run['refusal']}  notice rank per search={ranks}  "
        f"cites notice={trace['cites_added_document']}  $83={trace['states_83']}  usage={delta}")


# --------------------------------------------------------------------------- summary

def stage_summary() -> None:
    answers, judge = read_jsonl(ANSWERS), read_jsonl(JUDGE)
    checks = {r["id"]: r for r in csv.DictReader(CHECKS.open(encoding="utf-8"))} if CHECKS.is_file() else {}
    questions = load_questions()
    done = [q for q in questions if q["id"] in answers and not answers[q["id"]].get("error")]
    by_kind = {}
    for kind in ("single", "multi", "unanswerable"):
        sel = [q["id"] for q in done if q["kind"] == kind]
        judged = [i for i in sel if i in judge]
        entry = {"answered": len(sel), "judged": len(judged),
                 "correct": sum(judge[i]["correct"] for i in judged),
                 "supported": sum(judge[i]["supported"] for i in judged),
                 "refusals": sum(answers[i]["refusal"] for i in sel),
                 "partial_refusals": sum(bool(answers[i].get("partial_refusal")) for i in sel)}
        if kind == "unanswerable":
            entry["correct_refusals"] = entry["refusals"]
        else:
            entry["wrong_refusals"] = entry["refusals"]
            entry["unsupported_numbers"] = sum(bool(checks.get(i, {}).get("numbers_not_in_passages")) for i in sel)
        by_kind[kind] = entry
    rec = [answers[q["id"]] for q in done]
    cost = {
        "questions": len(rec),
        "mean_seconds": round(statistics.mean(r["seconds"] for r in rec), 1) if rec else None,
        "median_seconds": round(statistics.median(r["seconds"] for r in rec), 1) if rec else None,
        "mean_input_tokens": round(statistics.mean(r["input_tokens"] for r in rec)) if rec else None,
        "mean_output_tokens": round(statistics.mean(r["output_tokens"] for r in rec)) if rec else None,
        "mean_model_calls": round(statistics.mean(r["model_calls"] for r in rec), 2) if rec else None,
        "mean_searches": round(statistics.mean(sum(t["tool"] == "search" for t in r["tool_calls"]) for r in rec), 2) if rec else None,
        "models_used": sorted({m for r in rec for m in r.get("models_used", [])}),
        "judge_tokens_total": sum(j.get("tokens", 0) for j in judge.values()),
    }
    summary = {"by_kind": by_kind, "cost_per_question": cost,
               "missing_or_failed": [q["id"] for q in questions if q not in done]}
    SUMMARY.write_text(json.dumps(summary, indent=2) + "\n", encoding="utf-8")
    log("summary: " + json.dumps(summary)[:900])


# --------------------------------------------------------------------------- main

def main() -> None:
    args = sys.argv[1:]
    fresh = "--fresh" in args
    ids = None
    if "--ids" in args:
        ids = set(args[args.index("--ids") + 1].split(","))
    stages = [a for a in args if a in STAGES] or [s for s in STAGES if s != "before_after_hybrid"]
    for stage in stages:
        log(f"\n=== {stage} ===")
        if stage == "retrieval":
            stage_retrieval()
        elif stage == "facts":
            stage_facts(ids, fresh)
        elif stage == "answers":
            stage_answers(ids, fresh)
        elif stage == "checks":
            stage_checks()
        elif stage == "judge":
            stage_judge(ids, fresh)
        elif stage == "agreement":
            stage_agreement()
        elif stage == "before_after":
            stage_before_after(fresh)
        elif stage == "summary":
            stage_summary()
        elif stage == "before_after_hybrid":
            stage_before_after_hybrid(fresh)


if __name__ == "__main__":
    main()
