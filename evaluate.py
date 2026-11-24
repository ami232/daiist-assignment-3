"""
Assignment 3: evaluation (`main.py evaluate`).

Part 1 - retrieval: hit rate at k = 1, 3, 5 for each chunking design, on the
answerable questions of eval/questions.csv. A retrieved chunk is a hit for an
expected passage when it comes from the expected document and its page range
includes the expected page. `multi` questions are strict (both passages must
be in the top k); the partial score (share of passages found) is also saved.

Part 2 - end to end (decisions in DECISIONS.md, section 13):
  1. agent.py answers every question, 3 at a time (EVAL_WORKERS); answers are
     reused while the question, AGENTS.md and the model are unchanged
     (EVAL_FRESH=1 runs everything again).
  2. Code checks: valid citations, refusals, expected page retrieved and cited,
     and a warning for numbers that are not in the retrieved passages.
  3. eval/answers_to_grade.md is written for blind human grading (no verdicts).
  4. The LLM judge (correct 1/0, supported 1/0) runs only once
     eval/human_labels.csv has 20+ grades, so the human grades come first.
  5. Agreement between the judge and the human grades, cost and latency.
  6. The judge on planted wrong answers (eval/judge_traps.csv), to check that it gives 0s.

Outputs (committed):
    eval/retrieval_results.csv   one row per question and design
    eval/retrieval_summary.md    hit-rate tables per design
    eval/e2e_answers.jsonl       agent answers with their full trace (cache)
    eval/answers_to_grade.md     answers and passages for human grading
    eval/judge_verdicts.jsonl    judge verdicts (cache)
    eval/judge_traps.csv         planted wrong answers with expected grades (input)
    eval/judge_trap_verdicts.jsonl  judge verdicts on them (cache)
    eval/e2e_results.csv         one row per question: checks, verdicts, grades, cost
    eval/e2e_summary.md          results, agreement, cost and latency
"""

from __future__ import annotations

import asyncio
import csv
import hashlib
import json
import os
import re
import statistics
import sys
import time
from dataclasses import asdict
from pathlib import Path

from pydantic import BaseModel, Field

import agent
import index as ix
from retrieval import search

ROOT = Path(__file__).resolve().parent
EVAL_DIR = ROOT / "eval"
QUESTIONS = EVAL_DIR / "questions.csv"
KS = (1, 3, 5)


def load_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r["question"].strip()]


def expected_passages(q: dict) -> list[tuple[str, int]]:
    docs = [d.strip() for d in q["expected_source"].split(";") if d.strip()]
    pages = [int(p) for p in q["expected_location"].split(";") if p.strip()]
    if len(docs) != len(pages):
        raise ValueError(f"{q['id']}: expected_source and expected_location differ in length")
    return list(zip(docs, pages))


def covers(chunk: dict, passage: tuple[str, int]) -> bool:
    doc, page = passage
    return chunk["doc_id"] == doc and chunk["page"] <= page <= chunk["page_end"]


def first_rank(hits: list[dict], passage: tuple[str, int]) -> int | None:
    """1-based rank of the first chunk covering the passage, or None."""
    for rank, chunk in enumerate(hits, start=1):
        if covers(chunk, passage):
            return rank
    return None


def evaluate_retrieval(designs: list[str] = ix.DESIGNS) -> list[dict]:
    questions = load_questions()
    # embed every question once (cached); unanswerable ones are reused later
    ix.embed_texts([q["question"] for q in questions], "RETRIEVAL_QUERY")
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    rows = []
    for design in designs:
        for q in answerable:
            passages = expected_passages(q)
            hits = search(q["question"], k=max(KS), design=design)
            ranks = [first_rank(hits, p) for p in passages]
            row = {
                "design": design, "id": q["id"], "kind": q["kind"],
                "expected": "; ".join(f"{d} p.{p}" for d, p in passages),
                "ranks": "; ".join(str(r) if r else "-" for r in ranks),
                "top1": f"{hits[0]['doc_id']} p.{hits[0]['page']}"
                        + (f"-{hits[0]['page_end']}" if hits[0]["page_end"] != hits[0]["page"] else ""),
            }
            for k in KS:
                found = [r is not None and r <= k for r in ranks]
                row[f"hit@{k}"] = int(all(found))
                row[f"partial@{k}"] = round(sum(found) / len(found), 2)
                row[f"words@{k}"] = sum(len(h["text"].split()) for h in hits[:k])
            rows.append(row)
    return rows


def summarise(rows: list[dict]) -> str:
    def mean(xs):
        return sum(xs) / len(xs) if xs else 0.0

    designs = list(dict.fromkeys(r["design"] for r in rows))
    out = ["# Retrieval evaluation", "",
           "Hit = a top-k chunk from the expected document whose pages include the expected page. "
           "`multi` is strict (both passages in the top k); partial = share of passages found.", ""]

    out += ["## Hit rate (all answerable questions)", "",
            "| Design | n | hit@1 | hit@3 | hit@5 | words@1 | words@3 | words@5 |",
            "|---|---|---|---|---|---|---|---|"]
    for d in designs:
        rs = [r for r in rows if r["design"] == d]
        out.append(f"| {d} | {len(rs)} | " + " | ".join(f"{mean([r[f'hit@{k}'] for r in rs]):.0%}" for k in KS)
                   + " | " + " | ".join(f"{mean([r[f'words@{k}'] for r in rs]):.0f}" for k in KS) + " |")

    out += ["", "## By question kind", "",
            "| Design | kind | n | hit@1 | hit@3 | hit@5 | partial@1 | partial@3 | partial@5 |",
            "|---|---|---|---|---|---|---|---|---|"]
    for d in designs:
        for kind in ("single", "multi"):
            rs = [r for r in rows if r["design"] == d and r["kind"] == kind]
            if rs:
                out.append(f"| {d} | {kind} | {len(rs)} | "
                           + " | ".join(f"{mean([r[f'hit@{k}'] for r in rs]):.0%}" for k in KS) + " | "
                           + " | ".join(f"{mean([r[f'partial@{k}'] for r in rs]):.0%}" for k in KS) + " |")

    out += ["", "## Misses at k = 5", ""]
    for d in designs:
        misses = [r for r in rows if r["design"] == d and not r["hit@5"]]
        out.append(f"- **{d}**: " + (", ".join(f"{r['id']} (expected {r['expected']}, ranks {r['ranks']}, "
                                               f"top-1 {r['top1']})" for r in misses) or "none"))
    return "\n".join(out) + "\n"


def run_retrieval() -> None:
    rows = evaluate_retrieval()
    with (EVAL_DIR / "retrieval_results.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    summary = summarise(rows)
    (EVAL_DIR / "retrieval_summary.md").write_text(summary, encoding="utf-8")
    print(summary)


# ---------------------------------------------------------------------------
# Part 2: end to end
# ---------------------------------------------------------------------------
ANSWERS = EVAL_DIR / "e2e_answers.jsonl"
TO_GRADE = EVAL_DIR / "answers_to_grade.md"
VERDICTS = EVAL_DIR / "judge_verdicts.jsonl"
HUMAN_LABELS = EVAL_DIR / "human_labels.csv"
RESULTS = EVAL_DIR / "e2e_results.csv"
SUMMARY = EVAL_DIR / "e2e_summary.md"
TRAPS = EVAL_DIR / "judge_traps.csv"            # planted wrong answers, graded by Máximo
TRAP_VERDICTS = EVAL_DIR / "judge_trap_verdicts.jsonl"
JUDGE_MODEL = "gemini-3.5-flash-lite"
MIN_HUMAN_LABELS = 20
FRESH = os.environ.get("EVAL_FRESH") == "1"
WORKERS = int(os.environ.get("EVAL_WORKERS", "3"))  # questions asked at the same time
ONLY = [i.strip() for i in os.environ.get("EVAL_IDS", "").split(",") if i.strip()]  # e.g. EVAL_IDS=q01,q27

_BLOCK_SPLIT = re.compile(r"\n\n(?=\[\d+\] Source: )")
_NUMBER = re.compile(r"\d+(?:\.\d+)?")
_THOUSANDS = re.compile(r"(?<=\d)[,   ](?=\d{3}\b)")  # 165,000 / 165 000 -> 165000


def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


def sha(*parts: str) -> str:
    return hashlib.sha1("\x1f".join(parts).encode("utf-8")).hexdigest()


def read_jsonl(path: Path) -> dict[str, dict]:
    if not path.is_file():
        return {}
    with path.open(encoding="utf-8") as f:
        return {r["id"]: r for r in map(json.loads, f) if r}


def write_jsonl(path: Path, records: dict[str, dict]) -> None:
    with path.open("w", encoding="utf-8") as f:
        for key in sorted(records):
            f.write(json.dumps(records[key], ensure_ascii=False) + "\n")


# --- 1. Agent answers -------------------------------------------------------
def answer_key(q: dict) -> str:
    """Changes when the question, the rules or the model change, so the answer is redone."""
    rules = (ROOT / "AGENTS.md").read_text(encoding="utf-8")
    return sha(q["question"], rules, agent.MODEL, str(agent.MAX_SEARCHES), str(agent.MAX_MODEL_CALLS))


async def answer_all(questions: list[dict], cache: dict[str, dict]) -> dict[str, dict]:
    """Ask the questions WORKERS at a time; each worker has its own agent and server.py process,
    so traces do not mix. Parallelism changes only the wall-clock time, not the answers."""
    todo = [q for q in questions if FRESH or cache.get(q["id"], {}).get("key") != answer_key(q)]
    log(f"[eval] {len(questions) - len(todo)} answers reused, {len(todo)} to ask, {WORKERS} at a time")
    if not todo:
        return cache
    queue: asyncio.Queue = asyncio.Queue()
    for q in todo:
        queue.put_nowait(q)
    state = {"done": 0, "failures": 0, "stop": False}

    async def worker(w: int) -> None:
        # no one can approve add_document during the evaluation, so it is always refused
        async with agent.CorpusAgent(approve=lambda tool, args: False) as corpus_agent:
            while not state["stop"] and not queue.empty():
                q = queue.get_nowait()
                log(f"\n[eval w{w}] {q['id']}: {q['question']}")
                try:
                    result = await corpus_agent.ask(q["question"])
                except Exception as e:
                    if "PerMinute" in str(e):  # per-minute limit: wait and ask again, not a failure
                        log(f"[eval w{w}] {q['id']}: per-minute limit, retrying in 60 s")
                        await asyncio.sleep(60)
                        queue.put_nowait(q)
                        continue
                    # e.g. daily quota exhausted: keep what is done, stop after 3 in a row
                    state["failures"] += 1
                    log(f"[eval w{w}] {q['id']} failed: {e!r}")
                    if state["failures"] >= 3:
                        state["stop"] = True
                        log("[eval] 3 failures in a row: stopping. Run again later to finish the rest.")
                    continue
                state["failures"] = 0
                state["done"] += 1
                cache[q["id"]] = {"id": q["id"], "key": answer_key(q), **asdict(result)}
                write_jsonl(ANSWERS, cache)  # save after every question
                log(f"[eval w{w}] {state['done']}/{len(todo)} {q['id']} done in {result.seconds}s: "
                    f"{result.answer[:150]}")

    await asyncio.gather(*(worker(w) for w in range(1, min(WORKERS, len(todo)) + 1)))
    return cache


# --- 2. Code checks ---------------------------------------------------------
def passages(rec: dict) -> list[dict]:
    """Every distinct passage the agent's searches returned."""
    out, seen = [], set()
    for call in rec["trace"]:
        if call["tool"] != "search":
            continue
        for block in _BLOCK_SPLIT.split(call["result"]):
            header, _, body = block.partition("\n")
            m = agent._SOURCE_RE.search(header)
            name = header.split("] ", 1)[-1].rsplit(" | relevance", 1)[0]
            if not m or (name, body) in seen:
                continue
            seen.add((name, body))
            start = int(m.group(2))
            out.append({"doc": m.group(1), "page": start, "page_end": int(m.group(3) or start),
                        "header": name, "text": body.strip()})
    return out


def answer_status(answer: str) -> str:
    a = answer.strip().lower()
    if a.startswith("answer blocked"):
        return "blocked"
    if a.startswith(agent.REFUSAL_START):  # "The corpus does not cover this / state / cover which ..."
        return "refused"
    if "not searched" in a:
        return "not searched"
    if agent.REFUSAL_START in a:
        return "partial"
    return "answered"


def numbers(text: str) -> set[float]:
    return {float(n) for n in _NUMBER.findall(_THOUSANDS.sub("", text))}


def figures_not_in_passages(answer: str, found: list[dict]) -> list[str]:
    """Numbers in the answer (citations and years left out) that no retrieved passage contains.
    A warning only: computed figures such as 28 - 20 = 8 are flagged too."""
    text = re.sub(r"\b[Cc]hapters?\s+\d+", "", agent._CITE_RE.sub("", answer))
    in_answer = {n for n in numbers(text) if not (n.is_integer() and 1900 <= n <= 2100)}
    in_passages = set().union(*(numbers(p["text"]) for p in found)) if found else set()
    return [f"{n:g}" for n in sorted(in_answer - in_passages)]


def code_checks(q: dict, rec: dict) -> dict:
    found = passages(rec)
    status = answer_status(rec["answer"])
    exact = int(rec["answer"].strip().lower().startswith(agent.REFUSAL.lower()))
    if q["kind"] == "unanswerable":
        refusal_ok = int(status == "refused")
        refusal = "correct refusal" if refusal_ok else f"missed refusal ({status})"
    else:
        refusal_ok = int(status != "refused")
        refusal = "wrong refusal" if not refusal_ok else status
    citations_valid = int(rec["guardrail"] != "blocked" and not agent.check_citations(rec["answer"], rec["trace"]))
    row = {"status": status, "refusal_check": refusal, "refusal_ok": refusal_ok,
           "exact_refusal_phrase": exact if status == "refused" else "",
           "citations_valid": citations_valid, "expected_retrieved": "", "expected_cited": ""}
    if q["kind"] != "unanswerable":
        retrieved = [tuple(r) for r in rec["retrieved"]]
        cited = [tuple(c) for c in rec["citations"]]
        exp = expected_passages(q)
        hit = [any(d == doc and s <= page <= e for d, s, e in retrieved) for doc, page in exp]
        # cited = a citation that points into a retrieved chunk which also covers the expected page
        cite = [any(d == doc and s <= page <= e and any(cd == doc and s <= cp <= e for cd, cp in cited)
                    for d, s, e in retrieved) for doc, page in exp]
        row["expected_retrieved"] = f"{sum(hit)}/{len(exp)}"
        row["expected_cited"] = f"{sum(cite)}/{len(exp)}"
    row["figures_not_in_passages"] = " ".join(figures_not_in_passages(rec["answer"], found))
    return row


# --- 3. File for blind human grading ----------------------------------------
def quote(text: str) -> str:
    return "\n".join("> " + line for line in text.splitlines() if line.strip())


def write_to_grade(questions: list[dict], answers: dict[str, dict]) -> None:
    out = ["# Answers to grade", "",
           "Grade at least 20 answers in `eval/human_labels.csv` (`id,correct,supported,notes`) "
           "before the judge runs. The judge does not run until 20 grades are there.", "",
           "- **correct** (1/0): the key figures and facts match the reference (rounding and hedging are fine). "
           "Every part of the question must be answered; a partial answer is 0. "
           "Unanswerable: 1 only if it says the corpus does not cover it and gives no substitute figure.",
           "- **supported** (1/0): every figure and claim is in the retrieved passages below "
           "(not only in the reference or in your memory). A plain refusal is 1.",
           "- **notes**: why, for every 0.", ""]
    for q in questions:
        rec = answers.get(q["id"])
        out += [f"## {q['id']} ({q['kind']})", "", f"**Question:** {q['question']}", "",
                f"**Reference:** {q['reference_answer']}", ""]
        if not rec:
            out += ["*Not answered yet.*", ""]
            continue
        found = passages(rec)
        cited = [tuple(c) for c in rec["citations"]]
        is_cited = [any(d == p["doc"] and p["page"] <= pg <= p["page_end"] for d, pg in cited) for p in found]
        out += ["**Answer:**", "", quote(rec["answer"]), "",
                f"**Cited passages ({sum(is_cited)}):**", ""]
        for p, c in zip(found, is_cited):
            if c:
                out += [f"- `{p['header']}`", "", quote(p["text"]), ""]
        others = [p for p, c in zip(found, is_cited) if not c]
        if others:
            out += [f"<details><summary>Other retrieved passages ({len(others)})</summary>", ""]
            for p in others:
                out += [f"- `{p['header']}`", "", quote(p["text"]), ""]
            out += ["</details>", ""]
    TO_GRADE.write_text("\n".join(out), encoding="utf-8")


def load_human_labels() -> dict[str, dict]:
    if not HUMAN_LABELS.is_file():
        return {}
    with HUMAN_LABELS.open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r.get("correct", "").strip() in ("0", "1")]
    return {r["id"].strip(): {"correct": int(r["correct"]), "supported": int(r["supported"]),
                              "notes": (r.get("notes") or "").strip()} for r in rows}


# --- 4. LLM judge -----------------------------------------------------------
JUDGE_PROMPT = """You grade answers from a research assistant. It answers questions about the electric-vehicle market for a consultant, using only passages retrieved from IEA reports. Grade two criteria, each 1 or 0, and give a one-sentence reason for each before its score.

correct: does the answer give what the reference answer gives?
- 1 if the key figures and facts match the reference. Rounding and hedging words are fine ("almost 30%" = "nearly 30%", "around 44 million" = "44 million"), and so is extra correct detail.
- 0 if a key figure or fact is wrong, missing, or about a different country or region, year or metric (for example a world or EU figure for Europe, 2024 for 2025, sales for sales share, a forecast for an actual value).
- If the question has several parts, 1 only if every part is answered correctly. An answer that covers one part and says the corpus does not cover, or did not search, another part gets 0.
- If the question is unanswerable, 1 only if the answer says the corpus does not cover it and does not present any figure as the answer. Mentioning related information is fine when it is clearly not offered as the answer.
- If the question is answerable and the answer refuses, 0.

supported: is every claim in the answer stated in the retrieved passages below?
- 1 if every figure and factual claim appears in the passages. Simple arithmetic between two passage figures, shown as computed, is fine. A refusal that makes no claims is 1.
- 0 if any figure or claim is not in the passages, even if it is true.
- Judge this only against the passages, not against the reference answer or your own knowledge.

Question (kind: {kind}): {question}

Reference answer: {reference}

Retrieved passages:
{passages}

Answer to grade:
{answer}
"""


class Verdict(BaseModel):
    correct_reason: str = Field(description="one sentence")
    correct: int = Field(description="1 or 0")
    supported_reason: str = Field(description="one sentence")
    supported: int = Field(description="1 or 0")


def judge_prompt(q: dict, rec: dict) -> str:
    found = passages(rec)
    text = "\n\n".join(f"[{p['header']}]\n{p['text']}" for p in found) or "(no passages were retrieved)"
    return JUDGE_PROMPT.format(kind=q["kind"], question=q["question"], reference=q["reference_answer"],
                               passages=text, answer=rec["answer"])


def judge_all(questions: list[dict], answers: dict[str, dict], cache: dict[str, dict],
              path: Path = VERDICTS) -> dict[str, dict]:
    from langchain_google_genai import ChatGoogleGenerativeAI
    judge = ChatGoogleGenerativeAI(model=JUDGE_MODEL, google_api_key=agent.load_api_key(), temperature=0,
                                   max_retries=6, rate_limiter=agent.RATE_LIMITER).with_structured_output(Verdict, include_raw=True)
    for q in questions:
        rec = answers.get(q["id"])
        if not rec:
            continue
        prompt = judge_prompt(q, rec)
        key = sha(prompt, JUDGE_MODEL)
        if not FRESH and cache.get(q["id"], {}).get("key") == key:
            continue
        started = time.time()
        try:
            out = judge.invoke(prompt)
        except Exception as e:
            log(f"[judge] {q['id']} failed: {e!r}")
            continue
        v, usage = out["parsed"], (out["raw"].usage_metadata or {})
        if v is None:
            log(f"[judge] {q['id']}: could not parse the verdict: {out.get('parsing_error')}")
            continue
        cache[q["id"]] = {"id": q["id"], "key": key, "correct": int(v.correct == 1),
                          "supported": int(v.supported == 1), "correct_reason": v.correct_reason,
                          "supported_reason": v.supported_reason,
                          "input_tokens": usage.get("input_tokens", 0),
                          "output_tokens": usage.get("output_tokens", 0),
                          "seconds": round(time.time() - started, 1)}
        write_jsonl(path, cache)
        log(f"[judge] {q['id']}: correct {cache[q['id']]['correct']}, supported {cache[q['id']]['supported']}")
    return cache


# --- 4b. Judge on planted wrong answers -------------------------------------
def load_traps() -> list[dict]:
    if not TRAPS.is_file():
        return []
    with TRAPS.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def judge_traps(questions: list[dict], answers: dict[str, dict]) -> list[dict]:
    """Each planted answer is judged with the passages its base question retrieved, like a real answer.
    Their expected grades are set by construction (the planted error decides them)."""
    traps = load_traps()
    if not traps or any(t["expected_correct"].strip() not in ("0", "1") for t in traps):
        if traps:
            log(f"[eval] Judge on planted answers not run: give every row of {TRAPS.name} its expected grades first.")
        return []
    by_id = {q["id"]: q for q in questions}
    fake_q, fake_a = [], {}
    for t in traps:
        q, base = by_id.get(t["question_id"]), answers.get(t["question_id"])
        if not q or not base:
            continue
        fake_q.append({**q, "id": t["id"]})
        fake_a[t["id"]] = {**base, "answer": t["answer"]}
    verdicts = judge_all(fake_q, fake_a, read_jsonl(TRAP_VERDICTS), TRAP_VERDICTS)
    out = []
    for t in traps:
        v = verdicts.get(t["id"], {})
        out.append({**t, "expected_correct": int(t["expected_correct"]), "expected_supported": int(t["expected_supported"]),
                    "judge_correct": v.get("correct", ""), "judge_supported": v.get("supported", ""),
                    "judge_correct_reason": v.get("correct_reason", ""),
                    "judge_supported_reason": v.get("supported_reason", "")})
    return out


# --- 5. Agreement, results, cost --------------------------------------------
def kappa(pairs: list[tuple[int, int]]) -> float | None:
    """Cohen's kappa for two 1/0 graders (None if undefined)."""
    if not pairs:
        return None
    n = len(pairs)
    po = sum(a == b for a, b in pairs) / n
    pa, pb = sum(a for a, _ in pairs) / n, sum(b for _, b in pairs) / n
    pe = pa * pb + (1 - pa) * (1 - pb)
    return None if pe == 1 else (po - pe) / (1 - pe)


def pct(xs: list) -> str:
    return f"{sum(xs)}/{len(xs)} ({sum(xs) / len(xs):.0%})" if xs else "-"


def stats(xs: list[float]) -> str:
    return f"{statistics.mean(xs):,.0f} | {statistics.median(xs):,.0f} | {max(xs):,.0f}" if xs else "- | - | -"


def summarise_e2e(questions: list[dict], rows: list[dict], verdicts: dict, labels: dict, judged: bool,
                  traps: list[dict] | None = None) -> str:
    kinds = ("single", "multi", "unanswerable")
    out = ["# End-to-end evaluation", "",
           f"Agent: `{agent.MODEL}`, at most {agent.MAX_SEARCHES} searches and {agent.MAX_MODEL_CALLS} model calls "
           f"per question. Judge: `{JUDGE_MODEL}` (the API ignores temperature 0 for it, so verdicts are not fully deterministic; they are saved and reused). {len(rows)} of {len(questions)} questions answered.",
           ""]

    out += ["## Code checks", "",
            "| kind | n | citations valid | refusal check passed | expected page retrieved | expected page cited | "
            "number warnings |", "|---|---|---|---|---|---|---|"]
    for kind in kinds + ("all",):
        rs = [r for r in rows if kind in ("all", r["kind"])]
        ans = [r for r in rs if r["kind"] != "unanswerable"]
        out.append(f"| {kind} | {len(rs)} | {pct([r['citations_valid'] for r in rs])} | "
                   f"{pct([r['refusal_ok'] for r in rs])} | "
                   + (f"{pct([int(r['expected_retrieved'].split('/')[0] == r['expected_retrieved'].split('/')[1]) for r in ans])} | "
                      f"{pct([int(r['expected_cited'].split('/')[0] == r['expected_cited'].split('/')[1]) for r in ans])} | "
                      if ans else "- | - | ")
                   + f"{sum(bool(r['figures_not_in_passages']) for r in rs)} |")
    statuses = {}
    for r in rows:
        statuses.setdefault((r["kind"] == "unanswerable", r["refusal_check"]), []).append(r["id"])
    refused = [r for r in rows if r["status"] == "refused"]
    out += ["", "A refusal is an answer that starts with \"The corpus does not\". Of the "
            f"{len(refused)} refusals, {sum(r['exact_refusal_phrase'] == 1 for r in refused)} use the exact phrase "
            "\"The corpus does not cover this\" asked for in AGENTS.md (format only, not counted as a failure)."]
    out += ["", "Refusals: " + "; ".join(f"{k[1]}: {len(v)} ({', '.join(v)})" for k, v in sorted(statuses.items())),
            "", "Number warnings (numbers in the answer that no retrieved passage contains; computed figures "
            "are flagged too): " + (", ".join(f"{r['id']} [{r['figures_not_in_passages']}]"
                                              for r in rows if r["figures_not_in_passages"]) or "none"), ""]

    if not judged:
        out += ["## Judge", "", f"Not run yet: {len(labels)} human grades in eval/human_labels.csv, "
                f"{MIN_HUMAN_LABELS} needed first (blind grading, see eval/answers_to_grade.md).", ""]
    else:
        out += ["## Results (judge, all questions)", "",
                "| kind | n | correct | supported | correct and supported |", "|---|---|---|---|---|"]
        for kind in kinds + ("all",):
            rs = [r for r in rows if kind in ("all", r["kind"]) and r["judge_correct"] != ""]
            out.append(f"| {kind} | {len(rs)} | {pct([r['judge_correct'] for r in rs])} | "
                       f"{pct([r['judge_supported'] for r in rs])} | "
                       f"{pct([int(r['judge_correct'] and r['judge_supported']) for r in rs])} |")
        out.append("")

    graded = [r for r in rows if r["human_correct"] != ""]
    if graded:
        out += ["## Results (human grades)", "", "| kind | n | correct | supported |", "|---|---|---|---|"]
        for kind in kinds + ("all",):
            rs = [r for r in graded if kind in ("all", r["kind"])]
            out.append(f"| {kind} | {len(rs)} | {pct([r['human_correct'] for r in rs])} | "
                       f"{pct([r['human_supported'] for r in rs])} |")
        out.append("")
    both = [r for r in graded if r["judge_correct"] != ""]
    if both:
        out += ["## Agreement between the judge and the human grades", "",
                "| criterion | n | agreement | Cohen's kappa | both 1 | both 0 | human 1, judge 0 | human 0, judge 1 |",
                "|---|---|---|---|---|---|---|---|"]
        for c in ("correct", "supported"):
            pairs = [(r[f"human_{c}"], r[f"judge_{c}"]) for r in both]
            k = kappa(pairs)
            out.append(f"| {c} | {len(pairs)} | {pct([int(a == b) for a, b in pairs])} | "
                       f"{'-' if k is None else f'{k:.2f}'} | {pairs.count((1, 1))} | {pairs.count((0, 0))} | "
                       f"{pairs.count((1, 0))} | {pairs.count((0, 1))} |")
        out += ["", "Disagreements:", ""]
        for r in both:
            for c in ("correct", "supported"):
                if r[f"human_{c}"] != r[f"judge_{c}"]:
                    out.append(f"- {r['id']} {c}: human {r[f'human_{c}']} ({r['human_notes'] or 'no note'}); "
                               f"judge {r[f'judge_{c}']} ({r[f'judge_{c}_reason']})")
        out.append("")

    if traps:
        judged_traps = [t for t in traps if t["judge_correct"] != ""]
        out += ["## Judge on planted wrong answers", "",
                "Answers written to contain the errors that matter in this use case, judged with the passages "
                "their base question retrieved. The expected grades are set by construction: each answer was written "
                "to fail in a known way (written by Claude at Máximo's request, see DECISIONS.md).", "",
                "| id | base | planted error | expected c/s | judge c/s | agrees |", "|---|---|---|---|---|---|"]
        for t in traps:
            agree = "" if t["judge_correct"] == "" else (
                "yes" if (t["judge_correct"], t["judge_supported"]) == (t["expected_correct"], t["expected_supported"]) else "no")
            out.append(f"| {t['id']} | {t['question_id']} | {t['planted_error']} | {t['expected_correct']}/{t['expected_supported']} | "
                       f"{t['judge_correct']}/{t['judge_supported']} | {agree} |")
        for c in ("correct", "supported"):
            pairs = [(t[f"expected_{c}"], t[f"judge_{c}"]) for t in judged_traps]
            zeros = [p for p in pairs if p[0] == 0]
            out.append(f"\n{c}: agreement {pct([int(a == b) for a, b in pairs])}; expected 0s the judge also gave 0: "
                       f"{pct([int(b == 0) for _, b in zeros])}.")
        both = [r for r in rows if r["human_correct"] != "" and r["judge_correct"] != ""]
        out += ["", "Agreement on real answers (human grades) and planted answers (expected grades) together:", "",
                "| criterion | n | agreement | Cohen's kappa |", "|---|---|---|---|"]
        for c in ("correct", "supported"):
            pairs = [(r[f"human_{c}"], r[f"judge_{c}"]) for r in both] + \
                    [(t[f"expected_{c}"], t[f"judge_{c}"]) for t in judged_traps]
            k = kappa(pairs)
            out.append(f"| {c} | {len(pairs)} | {pct([int(a == b) for a, b in pairs])} | {'-' if k is None else f'{k:.2f}'} |")
        out.append("")

    out += ["## Cost and latency per question", "", "| | mean | median | max |", "|---|---|---|---|",
            f"| agent seconds | {stats([r['seconds'] for r in rows])} |",
            f"| agent input tokens | {stats([r['input_tokens'] for r in rows])} |",
            f"| agent output tokens | {stats([r['output_tokens'] for r in rows])} |",
            f"| agent total tokens | {stats([r['input_tokens'] + r['output_tokens'] for r in rows])} |",
            f"| model calls | {stats([r['model_calls'] for r in rows])} |",
            f"| searches | {stats([r['searches'] for r in rows])} |"]
    vs = [v for v in verdicts.values() if v["id"] in {r["id"] for r in rows}]
    if judged and vs:
        out += [f"| judge total tokens | {stats([v['input_tokens'] + v['output_tokens'] for v in vs])} |",
                f"| judge seconds | {stats([v['seconds'] for v in vs])} |"]
    out += ["", "Token counts are as reported by the Gemini API (free tier, so no money was spent). "
            f"Agent seconds include waiting for the free-tier rate limit (12 requests a minute shared by "
            f"{WORKERS} questions asked at the same time), so they overstate the latency of a single question.", ""]

    failed = [r for r in rows if not r["refusal_ok"] or not r["citations_valid"]
              or r["judge_correct"] == 0 or r["judge_supported"] == 0
              or r["human_correct"] == 0 or r["human_supported"] == 0]
    out += ["## Answers to look at (any check, judge verdict or human grade is 0)", "",
            "| id | kind | status | expected retrieved | expected cited | judge c/s | human c/s | number warnings |",
            "|---|---|---|---|---|---|---|---|"]
    for r in failed:
        out.append(f"| {r['id']} | {r['kind']} | {r['refusal_check']} | {r['expected_retrieved'] or '-'} | "
                   f"{r['expected_cited'] or '-'} | {r['judge_correct']}/{r['judge_supported']} | "
                   f"{r['human_correct']}/{r['human_supported']} | {r['figures_not_in_passages'] or '-'} |")
    return "\n".join(out) + "\n"


def run_end_to_end() -> None:
    questions = load_questions()
    if ONLY:
        questions = [q for q in questions if q["id"] in ONLY]
    answers = asyncio.run(answer_all(questions, read_jsonl(ANSWERS)))
    # only answers from the current rules and model count (older ones stay in the file until redone)
    answers = {q["id"]: answers[q["id"]] for q in load_questions()
               if q["id"] in answers and answers[q["id"]]["key"] == answer_key(q)}
    write_to_grade(load_questions(), answers)
    labels = load_human_labels()
    judged = len(labels) >= MIN_HUMAN_LABELS
    verdicts = read_jsonl(VERDICTS)
    if judged:
        verdicts = judge_all(questions, answers, verdicts)
    else:
        log(f"[eval] Judge not run: {len(labels)} human grades in {HUMAN_LABELS.name}, {MIN_HUMAN_LABELS} needed. "
            f"Grade the answers in {TO_GRADE.relative_to(ROOT)} first.")

    rows = []
    for q in questions:
        rec = answers.get(q["id"])
        if not rec:
            continue
        v = verdicts.get(q["id"], {}) if judged else {}
        h = labels.get(q["id"], {})
        rows.append({"id": q["id"], "kind": q["kind"], **code_checks(q, rec), "guardrail": rec["guardrail"],
                     "judge_correct": v.get("correct", ""), "judge_supported": v.get("supported", ""),
                     "judge_correct_reason": v.get("correct_reason", ""),
                     "judge_supported_reason": v.get("supported_reason", ""),
                     "human_correct": h.get("correct", ""), "human_supported": h.get("supported", ""),
                     "human_notes": h.get("notes", ""),
                     "searches": sum(c["tool"] == "search" for c in rec["trace"]),
                     "model_calls": rec["model_calls"], "input_tokens": rec["input_tokens"],
                     "output_tokens": rec["output_tokens"], "seconds": rec["seconds"], "answer": rec["answer"]})
    if not rows:
        raise SystemExit("No answers yet (see the errors above).")
    with RESULTS.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    traps = judge_traps(load_questions(), answers) if judged else []
    summary = summarise_e2e(questions, rows, verdicts, labels, judged, traps)
    SUMMARY.write_text(summary, encoding="utf-8")
    print(summary)


if __name__ == "__main__":
    run_retrieval()
    run_end_to_end()
