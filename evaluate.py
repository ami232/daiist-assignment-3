"""
Assignment 3: evaluation (`main.py evaluate`).

1. Retrieval: hit rate at k = 1, 3, 5 for each design (A_fixed, B_structure,
   B_structure + hybrid BM25), and the words each adds to the prompt.
   A hit is a retrieved chunk from the expected filing and section whose line
   range overlaps the expected lines in eval/questions.csv. For `multi`
   questions both passages must be retrieved ("all"); "any" is reported too.
2. End to end: the agent answers every question (answers cached in
   eval/answers.jsonl, so a run stopped by the daily quota resumes).
3. Code checks: citations present and valid, refusals, whether the expected
   passage was among what the agent retrieved.
4. LLM judge with a rubric and the retrieved text as evidence (eval/judge.jsonl).
5. Agreement between the judge and eval/human_labels.csv.
6. Before/after: add the Q3 2026 10-Q through the agent (approved here in
   code, and logged) and ask the question it answers again.
7. Failure classification, cost per question, eval/summary.md.

Settings (env or .env): GEMINI_MODEL, JUDGE_MODEL, EVAL_PAUSE (seconds
between questions, default 4), EVAL_FRESH=1 to ignore cached answers.
"""

from __future__ import annotations

import asyncio
import csv
import hashlib
import json
import re
import statistics
import sys
import time
from pathlib import Path

import index
from agent import MODEL, CorpusAgent, is_refusal

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
HELDOUT = EVAL / "heldout_questions.csv"   # questions on the 10-Q, a filing never used to build or tune anything
HUMAN = EVAL / "human_labels.csv"
OVERRIDES = EVAL / "failure_overrides.csv"
ANSWERS = EVAL / "answers.jsonl"
JUDGE_CACHE = EVAL / "judge.jsonl"

JUDGE_MODEL = index.setting("JUDGE_MODEL", MODEL)
PAUSE = float(index.setting("EVAL_PAUSE", "4"))
FRESH = index.setting("EVAL_FRESH", "0") == "1"
ANSWERS_ONLY = index.setting("EVAL_ANSWERS_ONLY", "0") == "1"   # stop before the judge, to grade blind
KS = (1, 3, 5)
INITIAL_DOCS = [d["doc_id"] for d in index.DOCUMENTS if d["indexed"]]
DEMO = {"question_id": "q27", "doc_id": "GS_10Q_Q3_2026", "path": "corpus/GS_10Q_Q3_2026/raw.htm"}
CATEGORIES = ["retrieval miss", "wrong answer from the right passage", "unsupported claim",
              "wrong refusal", "bad test question"]


def log(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


# ================================================================ test set

LOCATION = re.compile(r"^\s*(?P<section>[a-z0-9_]+)\s*>.*\(L(?P<a>\d+)-(?P<b>\d+)\)\s*$")


def load_questions(path: Path = QUESTIONS) -> list[dict]:
    if not path.is_file():
        return []
    with path.open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if (r.get("question") or "").strip()]
    for r in rows:
        r["kind"] = r["kind"].strip().lower()
        sources = [s.strip() for s in r["expected_source"].split(";") if s.strip()]
        locations = [s.strip() for s in r["expected_location"].split(";") if s.strip()]
        r["expected"] = []
        for src, loc in zip(sources, locations):
            # one passage per ';'; ' | ' separates the places where the filing
            # states the same fact (a summary and a detail section, a table
            # printed twice); retrieving any of them counts
            alts = []
            for alt in loc.split(" | "):
                m = LOCATION.match(alt)
                if not m:
                    raise SystemExit(f"{r['id']}: can't read location {alt!r} (expected 'section > label (La-b)')")
                alts.append({"section": m["section"], "a": int(m["a"]), "b": int(m["b"])})
            r["expected"].append({"doc_id": src, "alts": alts})
    return rows


def covers(chunk: dict, exp: dict) -> bool:
    return chunk["doc_id"] == exp["doc_id"] and any(
        chunk["section"] == alt["section"] and int(chunk["start_line"]) <= alt["b"] and int(chunk["end_line"]) >= alt["a"]
        for alt in exp["alts"])


def found_passages(chunks: list[dict], expected: list[dict]) -> list[bool]:
    return [any(covers(c, e) for c in chunks) for e in expected]


NUMBER = re.compile(r"\d[\d,]*\.?\d*")


def key_numbers(reference: str) -> set[str]:
    """Figures in the reference answer that identify the passage: '58.28',
    '4,127', '64.4'. Years and numbers under three digits (too common to
    identify anything) are left out."""
    out = set()
    for n in NUMBER.findall(reference):
        n = n.rstrip(".,")
        if re.fullmatch(r"20\d\d|19\d\d", n) or len(n.replace(",", "").replace(".", "")) < 3:
            continue
        out.add(n)
    return out


def found_by_content(chunks: list[dict], q: dict) -> bool | None:
    """Second, independent hit test: for every expected filing, some retrieved
    chunk from that filing contains one of the reference answer's figures.
    It counts the same fact found at another place in the filing (summary vs
    detail section, a table printed twice). None if the reference has no figures."""
    numbers = key_numbers(q["reference_answer"])
    if not numbers:
        return None
    docs = {e["doc_id"] for e in q["expected"]}
    return all(any(c["doc_id"] == d and any(n in c["text"] for n in numbers) for c in chunks) for d in docs)


# ================================================================ 1. retrieval

def retrieval(questions: list[dict]) -> tuple[list[dict], list[dict]]:
    cache = index.EmbeddingCache()
    designs = [(d, False) for d in index.DESIGNS] + [("B_structure", True)]
    per_question, summary = [], []
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    for design, hybrid in designs:
        name = design + ("+hybrid" if hybrid else "")
        if index.collection(design).count() == 0:
            log(f"  {name}: not built, skipped")
            continue
        hits = {k: [] for k in KS}
        hits_any = {k: [] for k in KS}
        hits_content = {k: [] for k in KS}
        words = {k: [] for k in KS}
        for q in answerable:
            top = index.search(q["question"], design=design, k=max(KS), hybrid=hybrid,
                               doc_ids=INITIAL_DOCS, cache=cache)
            row = {"id": q["id"], "kind": q["kind"], "design": name}
            for k in KS:
                found = found_passages(top[:k], q["expected"])
                hits[k].append(all(found))
                hits_any[k].append(any(found))
                words[k].append(sum(int(c["words"]) for c in top[:k]))
                row[f"hit@{k}"] = int(all(found))
                by_content = found_by_content(top[:k], q)
                if by_content is not None:  # location hit OR the figure found in the right filing
                    hits_content[k].append(all(found) or by_content)
                    row[f"content_hit@{k}"] = int(all(found) or by_content)
            row["top5"] = " ".join(c["id"] for c in top)
            per_question.append(row)
        n = len(answerable)
        multi = [i for i, q in enumerate(answerable) if q["kind"] == "multi"]
        single = [i for i, q in enumerate(answerable) if q["kind"] == "single"]
        entry = {"design": name, "questions": n}
        for k in KS:
            entry[f"hit@{k}"] = round(sum(hits[k]) / n, 3)
            entry[f"single hit@{k}"] = round(sum(hits[k][i] for i in single) / len(single), 3)
            entry[f"multi all@{k}"] = round(sum(hits[k][i] for i in multi) / len(multi), 3)
            entry[f"multi any@{k}"] = round(sum(hits_any[k][i] for i in multi) / len(multi), 3)
            entry[f"words@{k}"] = round(statistics.mean(words[k]))
            entry[f"figure hit@{k}"] = round(sum(hits_content[k]) / len(hits_content[k]), 3) if hits_content[k] else None
        summary.append(entry)
        log(f"  {name:<20} hit@1 {entry['hit@1']:.2f}  hit@3 {entry['hit@3']:.2f}  hit@5 {entry['hit@5']:.2f}  "
            f"words@5 {entry['words@5']}  | figure-in-filing hit@1 {entry['figure hit@1']:.2f} "
            f"@3 {entry['figure hit@3']:.2f} @5 {entry['figure hit@5']:.2f} "
            f"({len(hits_content[1])} questions with figures)")
    log(f"  query embeddings sent to the API: {cache.api_calls} (the rest were cached)")
    write_csv(EVAL / "retrieval_hits.csv", per_question)
    write_csv(EVAL / "retrieval_summary.csv", summary)
    return per_question, summary


def best_design(summary: list[dict]) -> dict:
    return max(summary, key=lambda e: (e["hit@5"], e["hit@3"], e["hit@1"], -e["words@5"]))


# ================================================================ 2. agent answers

def cache_key(q: dict) -> str:
    config = index.load_config()
    raw = f"{q['id']}|{q['question']}|{MODEL}|{config['design']}|{config['k']}|{config['hybrid']}"
    return hashlib.sha256(raw.encode()).hexdigest()[:16]


def read_jsonl(path: Path) -> dict[str, dict]:
    if not path.is_file():
        return {}
    out = {}
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            item = json.loads(line)
            out[item["key"]] = item
    return out


def append_jsonl(path: Path, item: dict) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(item, ensure_ascii=False) + "\n")


def quota_error(text: str) -> bool:
    return bool(re.search(r"RESOURCE_EXHAUSTED|429|quota", text, re.I))


async def run_agent(questions: list[dict]) -> dict[str, dict]:
    cached = {} if FRESH else read_jsonl(ANSWERS)
    answers: dict[str, dict] = {}
    todo = []
    for q in questions:
        item = cached.get(cache_key(q))
        tool_failed = item and any(t.get("output", "").startswith("Tool error") for t in item["result"]["trace"])
        if item and not item["result"]["error"] and not tool_failed:
            answers[q["id"]] = item["result"]
        else:
            todo.append(q)
    log(f"  {len(answers)} answers cached, {len(todo)} to run with {MODEL}")
    if not todo:
        return answers
    async with CorpusAgent() as agent:
        for n, q in enumerate(todo, 1):
            result = (await agent.ask(q["question"])).to_dict()
            if result["error"]:
                log(f"  {q['id']}: ERROR {result['error'][:200]}")
                if quota_error(result["error"]):
                    log("  Stopping: the model quota is used up. Answers so far are saved; "
                        "run `main.py evaluate` again later to continue.")
                    break
            else:
                append_jsonl(ANSWERS, {"key": cache_key(q), "id": q["id"], "result": result})
                log(f"  {q['id']} ({n}/{len(todo)}) {result['seconds']}s "
                    f"{'refused' if result['refused'] else 'answered'}, guardrail {result['guardrail']}")
            answers[q["id"]] = result
            time.sleep(PAUSE)
    return answers


# ================================================================ 3. code checks

RETRIEVED = re.compile(r"^\[(?P<id>([A-Za-z0-9_]+)#[a-z]+\d{3})\] .*lines (?P<a>\d+)-(?P<b>\d+) of (?P<section>[a-z0-9_]+)\.txt$", re.M)


def retrieved_chunks(r: dict) -> list[dict]:
    """Every passage the agent's searches returned, with filing, section and
    lines, read from the search output itself (so it also works for documents
    added during the run)."""
    out = {}
    for t in r["trace"]:
        if t["tool"] != "search":
            continue
        for m in RETRIEVED.finditer(t.get("output", "")):
            out[m["id"]] = {"id": m["id"], "doc_id": m[2], "section": m["section"],
                            "start_line": int(m["a"]), "end_line": int(m["b"])}
    return list(out.values())


def code_checks(q: dict, r: dict) -> dict:
    retrieved = set(r["retrieved"])
    cited = r["citations"]
    checks = {
        "searched": int(any(t["tool"] == "search" for t in r["trace"])),
        "has_citation": int(bool(cited)),
        "citations_valid": int(all(c in retrieved for c in cited)),
        "refused": int(bool(r["refused"])),
        "refusal_correct": int(bool(r["refused"]) == (q["kind"] == "unanswerable")),
    }
    if q["kind"] != "unanswerable":
        found = found_passages(retrieved_chunks(r), q["expected"])
        checks["expected_retrieved"] = int(all(found)) if found else 0
        cited_docs = {c.split("#")[0] for c in cited}
        checks["cites_expected_doc"] = int(bool(cited_docs & {e["doc_id"] for e in q["expected"]}))
    else:
        checks["expected_retrieved"] = ""
        checks["cites_expected_doc"] = ""
    return checks


# ================================================================ 4. judge

RUBRIC = """You grade one answer from a financial-filings assistant. Analysts copy its figures into their notes, so precision matters.

QUESTION ({kind}): {question}
REFERENCE ANSWER (written by the analyst from the filing): {reference}
ASSISTANT ANSWER: {answer}

EVIDENCE (every passage the assistant's searches returned; nothing else counts as support):
{evidence}

Grade two things, each 1 or 0.

correct:
- For an answerable question: 1 if the answer states the reference's key facts (figures equal to the reference allowing only rounding, the right firm, period, segment and basis such as GAAP vs as adjusted) and says nothing that contradicts it. Missing a fact the question asks for, a wrong number, or the wrong period/firm/basis is 0. A refusal is 0.
- For an unanswerable question: 1 if the answer declines (says the filings do not cover it) and does not assert an answer; mentioning related figures that are cited is fine. Giving an answer or an estimate is 0.

supported:
- 1 if every factual claim in the answer can be found in the EVIDENCE (numbers must match). 0 if any claim is not in the evidence, even if it is true. A refusal that asserts nothing is 1.

Reply with JSON only: {{"correct": 0 or 1, "supported": 0 or 1, "reason": "one or two sentences"}}"""


def evidence_text(r: dict, limit_words: int = 6000) -> str:
    text = "\n\n".join(t["output"] for t in r["trace"] if t["tool"] == "search")
    words = text.split()
    return " ".join(words[:limit_words]) + (" [...]" if len(words) > limit_words else "") if words else "(no search was run)"


def judge(questions: list[dict], answers: dict[str, dict]) -> dict[str, dict]:
    from google.genai import errors, types
    cached = read_jsonl(JUDGE_CACHE)
    client = None
    verdicts = {}
    for q in questions:
        r = answers.get(q["id"])
        if not r or r["error"]:
            continue
        key = hashlib.sha256(f"{JUDGE_MODEL}|{q['id']}|{q['reference_answer']}|{r['answer']}".encode()).hexdigest()[:16]
        if key in cached:
            verdicts[q["id"]] = cached[key]["verdict"]
            continue
        client = client or index.gemini_client()
        prompt = RUBRIC.format(kind=q["kind"], question=q["question"], reference=q["reference_answer"],
                               answer=r["answer"], evidence=evidence_text(r))
        verdict = None
        for attempt in range(6):
            try:
                started = time.time()
                resp = client.models.generate_content(
                    model=JUDGE_MODEL, contents=prompt,
                    config=types.GenerateContentConfig(temperature=0, response_mime_type="application/json"))
                verdict = json.loads(resp.text)
                usage = resp.usage_metadata
                verdict["judge_tokens"] = (usage.prompt_token_count or 0) + (usage.candidates_token_count or 0)
                verdict["judge_seconds"] = round(time.time() - started, 2)
                break
            except errors.APIError as error:
                text = str(error)
                daily = re.search(r"per.?day|PerDay", text, re.I)
                busy = getattr(error, "code", 0) in (500, 502, 503, 504) or "UNAVAILABLE" in text
                if attempt < 5 and ((quota_error(text) and not daily) or busy):
                    wait = 30 * (attempt + 1)
                    log(f"  judge: {'model busy' if busy else 'rate limited'} at {q['id']}, retrying in {wait}s")
                    time.sleep(wait)
                    continue
                log(f"  judge stopped at {q['id']}: {text[:200]}. Verdicts so far are saved; run again to continue.")
                return verdicts
            except (json.JSONDecodeError, ValueError):
                time.sleep(2)
        if verdict is None:
            continue
        verdict = {"correct": int(verdict.get("correct", 0)), "supported": int(verdict.get("supported", 0)),
                   "reason": verdict.get("reason", ""), "judge_tokens": verdict.get("judge_tokens", 0),
                   "judge_seconds": verdict.get("judge_seconds", 0)}
        append_jsonl(JUDGE_CACHE, {"key": key, "id": q["id"], "verdict": verdict})
        verdicts[q["id"]] = verdict
        log(f"  judged {q['id']}: correct {verdict['correct']}, supported {verdict['supported']}")
        time.sleep(PAUSE / 2)
    return verdicts


# ================================================================ 5. agreement

def read_human() -> dict[str, dict]:
    if not HUMAN.is_file():
        return {}
    with HUMAN.open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if (r.get("id") or "").strip()]
    out = {}
    for r in rows:
        try:
            out[r["id"].strip()] = {"correct": int(r["correct"]), "supported": int(r["supported"]),
                                    "notes": r.get("notes", "")}
        except (KeyError, ValueError):
            continue
    return out


def kappa(a: list[int], b: list[int]) -> float | None:
    n = len(a)
    if not n:
        return None
    po = sum(x == y for x, y in zip(a, b)) / n
    pa, pb = sum(a) / n, sum(b) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return None if pe == 1 else round((po - pe) / (1 - pe), 3)


def agreement(human: dict[str, dict], verdicts: dict[str, dict]) -> dict:
    ids = [i for i in human if i in verdicts]
    out = {"graded_by_you": len(human), "compared": len(ids)}
    for field in ("correct", "supported"):
        h = [human[i][field] for i in ids]
        j = [verdicts[i][field] for i in ids]
        out[f"{field} agreement"] = round(sum(x == y for x, y in zip(h, j)) / len(ids), 3) if ids else None
        out[f"{field} kappa"] = kappa(h, j)
        out[f"{field} disagreements"] = [i for i in ids if human[i][field] != verdicts[i][field]]
    return out


# ================================================================ 6. before / after

async def before_after(questions: list[dict], answers: dict[str, dict]) -> dict:
    q = next(x for x in questions if x["id"] == DEMO["question_id"])
    before = answers.get(q["id"])
    approvals = []

    def approve(path: str) -> bool:
        approvals.append(f"evaluate.py approved add_document({path!r}) for the before/after demo")
        return True

    async with CorpusAgent() as agent:
        added = await agent.ask(f"Please add the document at {DEMO['path']} to the corpus.", approver=approve)
        via = "agent"
        if not any(t["tool"] == "add_document" and t.get("approved") for t in added.trace):
            # the model didn't call the tool: call it through the same server, still logged
            result = await agent.session.call_tool("add_document", {"path": DEMO["path"]})
            approvals.append("agent did not call add_document; evaluate.py called it directly, approved")
            added_text = "\n".join(getattr(c, "text", "") for c in result.content)
            via = "direct call"
        else:
            added_text = next(t["output"] for t in added.trace if t["tool"] == "add_document")
        after = (await agent.ask(q["question"])).to_dict()
        heldout = {}
        cached = {} if FRESH else read_jsonl(ANSWERS)
        for h in load_questions(HELDOUT):
            item = cached.get(cache_key(h))
            if item and not item["result"]["error"]:
                heldout[h["id"]] = item["result"]
                continue
            result = (await agent.ask(h["question"])).to_dict()
            if not result["error"]:
                append_jsonl(ANSWERS, {"key": cache_key(h), "id": h["id"], "result": result})
            heldout[h["id"]] = result
            log(f"  held-out {h['id']} {result['seconds']}s {'refused' if result['refused'] else 'answered'}")
            time.sleep(PAUSE)
    return {"question": q, "before": before, "after": after, "add_result": added_text,
            "added_via": via, "approvals": approvals, "heldout": heldout}


# ================================================================ 7. failures, cost, report

def classify(q: dict, r: dict, checks: dict, final: dict) -> str:
    if final["correct"] and final["supported"]:
        return ""
    if q["kind"] == "unanswerable":  # it answered (or half-answered) something the filings don't cover
        return "unsupported claim"
    if r["refused"]:
        return "wrong refusal" if checks["expected_retrieved"] else "retrieval miss"
    if not final["correct"]:
        return "wrong answer from the right passage" if checks["expected_retrieved"] else "retrieval miss"
    return "unsupported claim"


def read_overrides() -> dict[str, dict]:
    if not OVERRIDES.is_file():
        return {}
    with OVERRIDES.open(newline="", encoding="utf-8") as f:
        return {r["id"].strip(): r for r in csv.DictReader(f) if (r.get("id") or "").strip()}


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    fields = list(dict.fromkeys(k for r in rows for k in r))
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def pct(x: float | None) -> str:
    return "n/a" if x is None else f"{100 * x:.0f}%"


def report(questions, retrieval_summary, answers, verdicts, human, agree, demo) -> None:
    overrides = read_overrides()
    rows = []
    for q in questions:
        r = answers.get(q["id"])
        if not r or r["error"]:
            continue
        checks = code_checks(q, r)
        v = verdicts.get(q["id"], {})
        h = human.get(q["id"])
        final = h or v or {"correct": "", "supported": ""}
        category = classify(q, r, checks, final) if (v or h) else "not judged"
        if q["id"] in overrides and overrides[q["id"]].get("category"):
            category = overrides[q["id"]]["category"].strip()
        rows.append({
            "id": q["id"], "kind": q["kind"], "question": q["question"], "answer": r["answer"],
            "citations": " ".join(r["citations"]), **checks, "guardrail": r["guardrail"],
            "judge_correct": v.get("correct", ""), "judge_supported": v.get("supported", ""),
            "judge_reason": v.get("reason", ""),
            "human_correct": h["correct"] if h else "", "human_supported": h["supported"] if h else "",
            "final_correct": final.get("correct", ""), "final_supported": final.get("supported", ""),
            "failure": category, "model_calls": r["model_calls"], "searches": checks["searched"] and
            sum(t["tool"] == "search" for t in r["trace"]),
            "input_tokens": r["input_tokens"], "output_tokens": r["output_tokens"], "seconds": r["seconds"],
        })
    write_csv(EVAL / "results.csv", rows)

    answerable = [x for x in rows if x["kind"] != "unanswerable"]
    unanswerable = [x for x in rows if x["kind"] == "unanswerable"]
    judged_answerable = [x for x in answerable if x["final_correct"] != ""]

    def rate(items, key):
        vals = [int(x[key]) for x in items if x[key] != ""]
        return sum(vals) / len(vals) if vals else None

    best = best_design(retrieval_summary) if retrieval_summary else None
    config = index.load_config()
    lines = ["# Evaluation summary", "",
             f"Agent model `{MODEL}`, judge model `{JUDGE_MODEL}`, server design "
             f"`{config['design']}{'+hybrid' if config['hybrid'] else ''}` with k={config['k']}.", "",
             "## Retrieval (answerable questions; multi = both passages retrieved)", "",
             "| design | hit@1 | hit@3 | hit@5 | single hit@5 | multi all@5 | multi any@5 | words@3 | words@5 |",
             "|---|---|---|---|---|---|---|---|---|"]
    for e in retrieval_summary:
        lines.append(f"| {e['design']} | {pct(e['hit@1'])} | {pct(e['hit@3'])} | {pct(e['hit@5'])} | "
                     f"{pct(e['single hit@5'])} | {pct(e['multi all@5'])} | {pct(e['multi any@5'])} | "
                     f"{e['words@3']} | {e['words@5']} |")
    lines += ["", "Cross-check on questions whose reference contains figures: a hit if the expected lines "
              "were retrieved OR a retrieved chunk from the right filing contains the reference figure "
              "(the same fact printed in another place).", "",
              "| design | figure hit@1 | figure hit@3 | figure hit@5 |", "|---|---|---|---|"]
    for e in retrieval_summary:
        lines.append(f"| {e['design']} | {pct(e['figure hit@1'])} | {pct(e['figure hit@3'])} | {pct(e['figure hit@5'])} |")
    if best:
        lines += ["", f"Best by hit@5, then hit@3, hit@1 and fewer words: **{best['design']}**."]
    lines += ["", "## End to end", "",
              f"- Answered questions: {len(rows)} of {len(questions)}",
              f"- Graded (by you or the judge): {sum(1 for x in rows if x['final_correct'] != '')} of {len(rows)}",
              f"- Answerable, correct: {pct(rate(answerable, 'final_correct'))} "
              f"({sum(int(x['final_correct'] or 0) for x in judged_answerable)}/{len(judged_answerable)} graded)",
              f"- Answerable, every claim supported: {pct(rate(answerable, 'final_supported'))}",
              f"- Unanswerable, correctly refused: {sum(x['refused'] for x in unanswerable)}/{len(unanswerable)}",
              f"- Answerable but refused (wrong refusals or misses): {sum(x['refused'] for x in answerable)}/{len(answerable)}",
              f"- Graded answers with an unsupported claim: {sum(1 for x in rows if x['final_supported'] == 0)}",
              f"- Citations valid (code check): {pct(rate(rows, 'citations_valid'))}; "
              f"expected passage retrieved by the agent: {pct(rate(answerable, 'expected_retrieved'))}",
              f"- Guardrail: {sum(x['guardrail'] == 'repaired' for x in rows)} repaired, "
              f"{sum(x['guardrail'] == 'blocked' for x in rows)} blocked", "",
              "Final grades use your label where you graded the answer, else the judge's.", "",
              "## Judge vs your grades", ""]
    if agree["compared"]:
        lines += [f"- Compared on {agree['compared']} answers.",
                  f"- correct: agreement {pct(agree['correct agreement'])}, Cohen's kappa {agree['correct kappa']}; "
                  f"disagreements: {', '.join(agree['correct disagreements']) or 'none'}",
                  f"- supported: agreement {pct(agree['supported agreement'])}, Cohen's kappa {agree['supported kappa']}; "
                  f"disagreements: {', '.join(agree['supported disagreements']) or 'none'}"]
    else:
        lines += ["- eval/human_labels.csv has no grades yet."]
    lines += ["", "## Failures", "", "| category | count | questions |", "|---|---|---|"]
    for c in CATEGORIES:
        ids = [x["id"] for x in rows if x["failure"] == c]
        lines.append(f"| {c} | {len(ids)} | {', '.join(ids)} |")
    other = [x["id"] for x in rows if x["failure"] not in CATEGORIES + [""]]
    if other:
        lines.append(f"| other / not judged | {len(other)} | {', '.join(other)} |")
    lines += ["", "Auto-classified from the code checks; override in eval/failure_overrides.csv "
              "(columns id, category, note).", "", "## Cost per question", ""]
    if rows:
        tokens = [x["input_tokens"] + x["output_tokens"] for x in rows]
        secs = [x["seconds"] for x in rows]
        calls = [x["model_calls"] for x in rows]
        judge_tokens = [v.get("judge_tokens", 0) for v in verdicts.values()]
        lines += [f"- Agent: mean {statistics.mean(tokens):,.0f} tokens (median {statistics.median(tokens):,.0f}, "
                  f"max {max(tokens):,}), mean {statistics.mean(secs):.1f}s (median {statistics.median(secs):.1f}s, "
                  f"max {max(secs):.1f}s), mean {statistics.mean(calls):.1f} model calls.",
                  f"- Input tokens are {100 * sum(x['input_tokens'] for x in rows) / max(sum(tokens), 1):.0f}% "
                  f"of the total (the retrieved passages dominate).",
                  f"- Judge: mean {statistics.mean(judge_tokens) if judge_tokens else 0:,.0f} tokens per question.",
                  f"- One question end to end, agent plus judge: about "
                  f"{statistics.mean(tokens) + (statistics.mean(judge_tokens) if judge_tokens else 0):,.0f} tokens; "
                  f"plus 1 query embedding."]
    if demo:
        b, a = demo["before"], demo["after"]
        lines += ["", "## Before and after adding a document", "",
                  f"Question {demo['question']['id']}: {demo['question']['question']}", "",
                  f"**Before** ({'refused' if b and b['refused'] else 'answered'}): {b['answer'] if b else '(not run)'}", "",
                  f"**Added** {DEMO['path']} via {demo['added_via']}: {demo['add_result']}", "",
                  f"Approval log: {'; '.join(demo['approvals'])}", "",
                  f"**After** ({'refused' if a['refused'] else 'answered'}): {a['answer']}", "",
                  "Sources after: " + "; ".join(f"[{k}] {w}" for k, w in a["sources"].items())]
        heldout_qs = load_questions(HELDOUT)
        if heldout_qs and demo.get("heldout"):
            hrows = []
            for h in heldout_qs:
                r = demo["heldout"].get(h["id"])
                if not r:
                    continue
                checks = code_checks(h, r)
                v = verdicts.get(h["id"], {})
                hrows.append({"id": h["id"], "kind": h["kind"], "question": h["question"], "answer": r["answer"],
                              **checks, "judge_correct": v.get("correct", ""),
                              "judge_supported": v.get("supported", ""), "judge_reason": v.get("reason", ""),
                              "seconds": r["seconds"], "tokens": r["input_tokens"] + r["output_tokens"]})
            write_csv(EVAL / "heldout_results.csv", hrows)
            lines += ["", "## Held-out filing (Goldman Q3 2026 10-Q, never used to build or tune)", "",
                      "Asked after the 10-Q was added, with nothing changed.", "",
                      "| id | kind | refused | expected passage retrieved | judge correct | judge supported |",
                      "|---|---|---|---|---|---|"]
            for x in hrows:
                lines.append(f"| {x['id']} | {x['kind']} | {x['refused']} | {x['expected_retrieved']} | "
                             f"{x['judge_correct']} | {x['judge_supported']} |")
            ok = [x for x in hrows if x["judge_correct"] == 1]
            judged = [x for x in hrows if x["judge_correct"] != ""]
            lines.append(f"\n{len(ok)}/{len(judged)} judged correct" + ("" if judged else " (not judged yet)") + ".")
        (EVAL / "before_after.json").write_text(json.dumps(demo, indent=1, ensure_ascii=False, default=str),
                                                encoding="utf-8")
    (EVAL / "summary.md").write_text("\n".join(lines) + "\n", encoding="utf-8")
    print("\n".join(lines))


def write_grading_sheet(questions: list[dict], answers: dict[str, dict]) -> None:
    """eval/to_grade.md: each answer with the reference and the passages it
    cited, and no judge verdicts, so the human grades are blind."""
    out = ["# Answers to grade", "",
           "For each: `correct` 1/0 (matches the reference, or a proper refusal for unanswerable) and "
           "`supported` 1/0 (every claim is in the cited/retrieved passages). Write them into "
           "eval/human_labels.csv as `id,correct,supported,notes`, with a note for every 0.", ""]
    for q in questions:
        r = answers.get(q["id"])
        if not r or r["error"]:
            continue
        cited = {}
        for t in r["trace"]:
            for block in re.split(r"\n(?=\[[A-Za-z0-9_]+#[a-z]+\d{3}\] )", t.get("output", "")):
                m = re.match(r"\[([A-Za-z0-9_]+#[a-z]+\d{3})\] ", block)
                if m and m[1] in r["citations"]:
                    cited[m[1]] = block.strip()
        out += [f"## {q['id']} ({q['kind']})", "", f"**Question:** {q['question']}", "",
                f"**Reference:** {q['reference_answer']}", "", f"**Answer:** {r['answer']}", "",
                f"Searches: {[t['args'].get('query') for t in r['trace'] if t['tool'] == 'search']}", ""]
        for cid, block in cited.items():
            out += ["```", block[:2500], "```", ""]
    (EVAL / "to_grade.md").write_text("\n".join(out), encoding="utf-8")


# ================================================================ main

async def main_async() -> None:
    questions = load_questions()
    log(f"{len(questions)} questions")

    log("\n1. Retrieval")
    _, retrieval_summary = retrieval(questions)

    log("\n2. Agent answers (the demo document is removed first so 'before' is honest)")
    removed = index.remove_document(DEMO["doc_id"])
    if removed:
        log(f"  removed {removed} passages of {DEMO['doc_id']} left from an earlier run")
    answers = await run_agent(questions)

    write_grading_sheet(questions, answers)
    if ANSWERS_ONLY:
        log("\nStopped before the judge (EVAL_ANSWERS_ONLY=1). Grade eval/to_grade.md into "
            "eval/human_labels.csv, then run `main.py evaluate` again.")
        return

    demo = None
    complete = all(q["id"] in answers and not answers[q["id"]]["error"] for q in questions)
    if complete:
        log("\n3. Before/after: adding the Q3 2026 10-Q through the agent")
        demo = await before_after(questions, answers)
    else:
        log("\n3. Before/after skipped until every question has an answer")

    log("\n4. Judge")
    heldout_qs = load_questions(HELDOUT)
    all_answers = dict(answers)
    if demo:
        all_answers.update(demo["heldout"])
    verdicts = judge(questions + heldout_qs, all_answers)

    human = read_human()
    agree = agreement(human, verdicts)
    log(f"\n5. Human labels: {len(human)} graded, {agree['compared']} compared with the judge")

    report(questions, retrieval_summary, answers, verdicts, human, agree, demo)


def main() -> None:
    asyncio.run(main_async())


if __name__ == "__main__":
    main()
