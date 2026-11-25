import csv
import hashlib
import json
import math
import os
import re
import statistics
import sys
import time
from collections import Counter
from pathlib import Path

from langchain_google_genai import ChatGoogleGenerativeAI
from pydantic import BaseModel, Field

import index

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
HUMAN_LABELS = EVAL / "human_labels.csv"
QUERY_VECTORS = EVAL / "query_vectors.json"
ANSWERS_CACHE = EVAL / "answers.jsonl"
JUDGE_CACHE = EVAL / "judge.jsonl"

KS = (1, 3, 5)
CORPUS_IDS = [d["doc_id"] for d in index.CORPUS]  # evaluate on the corpus only, not on documents added later
# A stronger model than the agent's gemini-3.5-flash-lite, as in session 10. gemini-3.5-flash
# took ~80 s a call and its free daily quota ran out after 7 verdicts; gemini-3.6-flash takes ~2 s.
JUDGE_MODEL = os.environ.get("JUDGE_MODEL", "gemini-3.6-flash")
FRESH = os.environ.get("EVAL_FRESH") == "1"
PAUSE_BETWEEN_QUESTIONS = 3  # seconds, to stay under the free tier's requests per minute


def log(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


# ---------------------------------------------------------------- test set


def load_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r["question"].strip()]
    for r in rows:
        r["kind"] = r["kind"].strip().lower()
        r["expected"] = expected_passages(r)
    return rows


def expected_passages(row: dict) -> list[dict]:
    """[{doc_id, pages}] from expected_source and expected_location."""
    sources = [s.strip() for s in row["expected_source"].split(";") if s.strip()]
    locations = [s.strip() for s in row["expected_location"].split(";") if s.strip()]
    passages = []
    for i, location in enumerate(locations):
        doc = sources[i] if len(sources) == len(locations) else sources[0]
        m = re.search(r"PDF pages? (\d+)(?:-(\d+))?", location)
        if not m:
            raise ValueError(f"{row['id']}: no 'PDF page' in expected_location {location!r}")
        first = int(m.group(1))
        passages.append({"doc_id": doc, "pages": (first, int(m.group(2) or first)), "label": location})
    return passages


def overlaps(a: tuple[int, int], b: tuple[int, int]) -> bool:
    return a[0] <= b[1] and b[0] <= a[1]


def matches(chunk_meta: dict, passage: dict) -> bool:
    return (chunk_meta["doc_id"] == passage["doc_id"]
            and overlaps((chunk_meta["page_start"], chunk_meta["page_end"]), passage["pages"]))


# ---------------------------------------------------------------- retrieval designs


def load_chunks() -> list[dict]:
    with index.CHUNKS_FILE.open(encoding="utf-8") as f:
        return [c for c in map(json.loads, f) if c["doc_id"] in CORPUS_IDS]


TOKEN = re.compile(r"[a-z0-9]+(?:[-.][0-9]+)*")
STOPWORDS = set("""a an and are as at be by can do does for from has have how i if in is it its my of on or our
should that the their them they this to was we what when which who will with you your must may not""".split())


def tokenize(text: str) -> list[str]:
    return [t for t in TOKEN.findall(text.lower()) if t not in STOPWORDS]


class BM25:
    """Okapi BM25 over the chunk texts (k1 = 1.5, b = 0.75)."""

    def __init__(self, chunks: list[dict], k1: float = 1.5, b: float = 0.75):
        self.chunks, self.k1, self.b = chunks, k1, b
        self.docs = [Counter(tokenize(c["text"])) for c in chunks]
        self.lengths = [sum(d.values()) for d in self.docs]
        self.avg = sum(self.lengths) / len(self.lengths)
        df = Counter(t for d in self.docs for t in d)
        n = len(self.docs)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}

    def search(self, query: str, k: int) -> list[int]:
        terms = tokenize(query)
        scores = []
        for i, (doc, length) in enumerate(zip(self.docs, self.lengths)):
            s = 0.0
            for t in terms:
                f = doc.get(t)
                if f:
                    s += self.idf[t] * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * length / self.avg))
            scores.append((s, i))
        return [i for s, i in sorted(scores, reverse=True)[:k] if s > 0]


def load_query_vectors() -> dict:
    return json.loads(QUERY_VECTORS.read_text(encoding="utf-8")) if QUERY_VECTORS.exists() else {}


def query_vector(question: str, cache: dict) -> list[float]:
    """The question's embedding, from the cache or from Gemini (then saved)."""
    if question not in cache:
        cache[question] = index.embed_query(question)
        QUERY_VECTORS.write_text(json.dumps(cache), encoding="utf-8")
    return cache[question]


def dense_search(collection, vector: list[float], k: int, position: dict, annex3_penalty: float = 0.0) -> list[int]:
    hits = index.ranked_search(collection, vector, k, where={"doc_id": {"$in": CORPUS_IDS}},
                               annex3_penalty=annex3_penalty)
    return [position[h["id"]] for h in hits if h["id"] in position]


def rrf(rankings: list[list[int]], k: int, c: int = 60) -> list[int]:
    """Reciprocal rank fusion: score = sum of 1 / (c + rank) over the rankings."""
    scores: Counter = Counter()
    for ranking in rankings:
        for rank, i in enumerate(ranking, start=1):
            scores[i] += 1 / (c + rank)
    return [i for i, _ in scores.most_common(k)]


def evaluate_retrieval(questions: list[dict]) -> tuple[list[dict], dict]:
    chunks = load_chunks()
    position = {c["id"]: i for i, c in enumerate(chunks)}
    bm25 = BM25(chunks)
    collection = index.get_collection()
    cache = load_query_vectors()
    pool = 50  # candidates from each method before fusion

    rows = []
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    for q in answerable:
        vector = query_vector(q["question"], cache)
        dense = dense_search(collection, vector, pool, position)
        keyword = bm25.search(q["question"], pool)
        rules_first = dense_search(collection, vector, max(KS), position, index.ANNEX3_PENALTY)
        rankings = {"dense": dense[:max(KS)], "bm25": keyword[:max(KS)], "hybrid": rrf([dense, keyword], max(KS)),
                    "dense+rules-first": rules_first}
        for design, ranking in rankings.items():
            row = {"id": q["id"], "kind": q["kind"], "design": design}
            for k in KS:
                found = [any(matches(chunks[i], p) for i in ranking[:k]) for p in q["expected"]]
                row[f"hit@{k}"] = int(any(found))
                row[f"all@{k}"] = int(all(found))
            row["words@5"] = sum(chunks[i]["words"] for i in ranking[:5])
            row["top5"] = " | ".join(f"{chunks[i]['doc_id']} p{chunks[i]['page_start']}-{chunks[i]['page_end']} "
                                     f"{chunks[i]['section'][:40]}" for i in ranking[:5])
            rows.append(row)

    summary = {}
    for design in ("dense", "bm25", "hybrid", "dense+rules-first"):
        rs = [r for r in rows if r["design"] == design]
        multi = [r for r in rs if r["kind"] == "multi"]
        summary[design] = {
            **{f"hit@{k}": round(sum(r[f"hit@{k}"] for r in rs) / len(rs), 3) for k in KS},
            "multi_all@5": round(sum(r["all@5"] for r in multi) / len(multi), 3) if multi else None,
            "words@5": round(statistics.mean(r["words@5"] for r in rs)),
        }
    return rows, summary


# ---------------------------------------------------------------- agent answers


def read_jsonl(path: Path) -> list[dict]:
    if not path.exists():
        return []
    with path.open(encoding="utf-8") as f:
        return [json.loads(line) for line in f if line.strip()]


def append_jsonl(path: Path, record: dict) -> None:
    with path.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")


def never_approve(name: str, args: dict) -> bool:
    return False


def run_agent_on_all(questions: list[dict]) -> dict:
    """{id: agent result}. Uses the cache unless EVAL_FRESH=1; failed runs are retried next time."""
    import agent

    cached = {} if FRESH else {r["id"]: r for r in read_jsonl(ANSWERS_CACHE)
                               if not r.get("error") and r.get("question_text")}
    if FRESH and ANSWERS_CACHE.exists():
        ANSWERS_CACHE.unlink()
    results = {}
    for q in questions:
        hit = cached.get(q["id"])
        if hit and hit["question_text"] == q["question"]:
            results[q["id"]] = hit
            continue
        log(f"[agent] {q['id']}: {q['question']}")
        try:
            r = agent.ask(q["question"], approve=never_approve)
            record = {"id": q["id"], "question_text": q["question"], **{k: r[k] for k in
                      ("answer", "trace", "guardrail", "tokens", "seconds", "model")}}
        except Exception as error:  # noqa: BLE001 - record it, carry on, retry on the next run
            log(f"  failed: {type(error).__name__}: {str(error)[:300]}")
            record = {"id": q["id"], "question_text": q["question"], "error": f"{type(error).__name__}: {error}"}
        append_jsonl(ANSWERS_CACHE, record)
        results[q["id"]] = record
        time.sleep(PAUSE_BETWEEN_QUESTIONS)
    return results


# ---------------------------------------------------------------- code checks

TITLE_KEYS = {"food-code-2026": "Food Code", "haccp-operators-manual": "Operators",
              "haccp-regulators-manual": "Regulators"}


def retrieved_meta(trace: list[dict]) -> list[dict]:
    """doc_id and page range of every passage the agent's searches returned."""
    out = []
    for line in re.findall(r"^\[\d+\] (.+)$", "\n".join(c["output"] for c in trace if c["tool"] == "search"),
                           re.MULTILINE):
        doc = next((d for d, key in TITLE_KEYS.items() if key in line.split("|")[0]), None)
        m = re.search(r"PDF pages? (\d+)(?:-(\d+))?", line)
        if doc and m:
            out.append({"doc_id": doc, "page_start": int(m.group(1)), "page_end": int(m.group(2) or m.group(1))})
    return out


def cited_meta(answer: str) -> list[dict]:
    """doc_id and pages of every citation in the answer."""
    out = []
    for citation in re.findall(r"\(([^()]*\bpages? \d[^()]*)\)", answer):
        doc = next((d for d, key in TITLE_KEYS.items() if key.lower() in citation.lower()), None)
        pages = [int(p) for p in re.findall(r"\d+", citation.split("page", 1)[1])][:2]
        if doc and pages:
            out.append({"doc_id": doc, "page_start": pages[0], "page_end": pages[-1]})
    return out


# "The corpus does not cover this." and the partial refusals rule 4 of AGENTS.md allows
# ("The corpus does not specify a fixed interval...", "does not cover whether...").
REFUSED = re.compile(r"corpus does not (cover|specify|state|say|include|address|contain|give|provide)"
                     r"|not covered (by|in) the corpus", re.IGNORECASE)


def code_checks(q: dict, r: dict) -> dict:
    import agent

    if r.get("error"):
        return {"error": 1}
    answer, trace = r["answer"], r["trace"]
    refused = int(bool(REFUSED.search(answer)))
    retrieved, cited = retrieved_meta(trace), cited_meta(answer)
    checks = {
        "error": 0,
        "searches": sum(c["tool"] == "search" for c in trace),
        "refused": refused,
        "citations": len(cited),
        "citations_valid": int(not agent.check_citations(answer, trace)),
        "guardrail_fired": int(any("citation check failed" in e for e in r["guardrail"])),
        "model_code_note": int("model code" in answer.lower()),
    }
    if q["kind"] != "unanswerable":
        checks["expected_retrieved"] = int(any(matches(m, p) for m in retrieved for p in q["expected"]))
        checks["expected_cited"] = int(any(matches(m, p) for m in cited for p in q["expected"]))
    return checks


# ---------------------------------------------------------------- LLM judge

RUBRIC = """You grade answers from a food-safety assistant for small food businesses. The assistant may only
use the retrieved passages (the evidence) and must cite them. Grade two things, each 1 or 0.

correct
- Answerable question: 1 if the answer gives the key facts of the reference answer (numbers, units,
  times, the main conditions) and states nothing that contradicts the reference or the evidence.
  Leaving out a secondary exception is fine; a missing or wrong key number is 0. A refusal is 0.
- Unanswerable question (the reference says the corpus does not cover it): 1 if the answer says the
  corpus does not cover it and does not give the missing fact from elsewhere. Giving related facts
  that the evidence does support, while saying the main point is not covered, is still 1.

supported
- 1 if every factual claim in the answer is stated in the evidence (paraphrase is fine; a number or
  condition must appear in the evidence). A refusal with no factual claims is 1.
- Ignore the reminder that the Food Code is a model code adopted by states and counties with changes,
  and ignore suggestions to ask the local regulatory authority: they are not claims to check.
- Judge support against the evidence only, not against your own knowledge or the reference.

First write your reasoning, then decide."""


class Verdict(BaseModel):
    """What the judge returns: reasoning first, then the verdict."""
    reasoning: str = Field(description="Two to four sentences checking the answer against the reference "
                                       "and against the evidence, claim by claim.")
    correct: bool = Field(description="The 'correct' criterion of the rubric.")
    supported: bool = Field(description="The 'supported' criterion of the rubric.")
    unsupported_claims: list[str] = Field(default_factory=list,
                                          description="Each claim of the answer that is not in the evidence.")


JUDGE_PROMPT = RUBRIC + """

Question ({kind}): {question}

Reference answer: {reference_answer}

Assistant's answer:
{answer}

Evidence (every passage the search tool returned, recorded by the harness):
{evidence}"""


class JudgeQuotaExhausted(RuntimeError):
    """The judge model's daily free-tier quota is used up; run again after the reset."""


_judge = None


def judge_model():
    global _judge
    if _judge is None:
        from api_key import load_api_key
        load_api_key()
        _judge = ChatGoogleGenerativeAI(model=JUDGE_MODEL, temperature=0, max_retries=1).with_structured_output(Verdict)
    return _judge


def judge(q: dict, r: dict, cache: dict) -> dict:
    """The judge's verdict for one answer, from the cache or from JUDGE_MODEL (then saved)."""
    evidence = "\n\n".join(c["output"] for c in r["trace"] if c["tool"] == "search")
    key = hashlib.sha1(f"{JUDGE_MODEL}|{JUDGE_PROMPT}|{q['question']}|{q['reference_answer']}|{r['answer']}"
                       .encode()).hexdigest()
    if key in cache:
        return cache[key]
    log(f"[judge] {q['id']}")
    prompt = JUDGE_PROMPT.format(kind=q["kind"], question=q["question"], reference_answer=q["reference_answer"],
                                 answer=r["answer"], evidence=evidence or "(no passages were retrieved)")
    for attempt in range(5):
        try:
            verdict = judge_model().invoke(prompt)
            break
        except Exception as error:  # noqa: BLE001 - 429/503 from Gemini, or a malformed verdict
            message = str(error)
            if "429" in message and ("PerDay" in message or "per day" in message.lower()):
                raise JudgeQuotaExhausted(message) from error
            wait = index.retry_delay(message) if "429" in message else 15 * (attempt + 1)
            log(f"  judge error ({message[:120]}), retrying in {wait:.0f}s")
            time.sleep(wait)
    else:
        return {"correct": None, "supported": None, "unsupported_claims": [], "reasoning": "not judged"}
    record = {"key": key, "id": q["id"], "model": JUDGE_MODEL, "reasoning": verdict.reasoning,
              "correct": int(verdict.correct), "supported": int(verdict.supported),
              "unsupported_claims": verdict.unsupported_claims}
    append_jsonl(JUDGE_CACHE, record)
    cache[key] = record
    return record


# ---------------------------------------------------------------- outcomes and failures


def outcome(q: dict, checks: dict, verdict: dict) -> str:
    if checks.get("error"):
        return "error"
    if q["kind"] == "unanswerable":
        return "correct refusal" if checks["refused"] and verdict["correct"] else "answered unanswerable"
    if checks["refused"] and not checks["citations"]:  # a partial refusal still answers
        return "wrong refusal"
    if not verdict["supported"]:
        return "unsupported"
    return "correct" if verdict["correct"] else "incorrect"


def draft_cause(q: dict, checks: dict, result: str) -> str:
    """A first guess at the failure cause, to be checked by hand."""
    if result in ("correct", "correct refusal"):
        return ""
    if result == "error":
        return "error (run failed)"
    if q["kind"] == "unanswerable" or result == "unsupported":
        return "unsupported claim"
    if not checks["expected_retrieved"]:
        return "retrieval miss"
    if result == "wrong refusal":
        return "wrong refusal"
    return "wrong answer from right passage"


# ---------------------------------------------------------------- agreement with human labels


def agreement(results: list[dict]) -> dict:
    if not HUMAN_LABELS.exists():
        return {"n": 0}
    with HUMAN_LABELS.open(newline="", encoding="utf-8") as f:
        labels = {r["id"].strip(): r for r in csv.DictReader(f) if (r.get("id") or "").strip()}
    out = {"n": 0}
    by_id = {r["id"]: r for r in results}
    pairs = [(labels[i], by_id[i]) for i in labels if i in by_id and by_id[i]["judge_correct"] is not None]
    out["n"] = len(pairs)
    if not pairs:
        return out
    for field in ("correct", "supported"):
        human = [int(h[field]) for h, _ in pairs]
        machine = [int(r[f"judge_{field}"]) for _, r in pairs]
        agree = sum(a == b for a, b in zip(human, machine)) / len(pairs)
        # Cohen's kappa: agreement corrected for chance.
        p_yes = (sum(human) / len(human)) * (sum(machine) / len(machine))
        p_no = (1 - sum(human) / len(human)) * (1 - sum(machine) / len(machine))
        expected = p_yes + p_no
        kappa = (agree - expected) / (1 - expected) if expected < 1 else 1.0
        out[field] = {"agreement": round(agree, 3), "kappa": round(kappa, 3),
                      "disagreements": [r["id"] for (h, r), a, b in zip(pairs, human, machine) if a != b]}
    return out


# ---------------------------------------------------------------- output


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        return
    fields = list(dict.fromkeys(k for r in rows for k in r))
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def pct(x) -> str:
    return "-" if x is None else f"{100 * x:.0f}%"


def main() -> None:
    questions = load_questions()
    kinds = Counter(q["kind"] for q in questions)
    log(f"{len(questions)} questions: {dict(kinds)}")

    # 1. Retrieval
    retrieval_rows, retrieval = evaluate_retrieval(questions)
    write_csv(EVAL / "retrieval.csv", retrieval_rows)
    print("\n## Retrieval (answerable questions)\n")
    print("| Design | hit@1 | hit@3 | hit@5 | multi: both passages @5 | words in top 5 |")
    print("|---|---|---|---|---|---|")
    for design, s in retrieval.items():
        print(f"| {design} | {pct(s['hit@1'])} | {pct(s['hit@3'])} | {pct(s['hit@5'])} | "
              f"{pct(s['multi_all@5'])} | {s['words@5']} |")

    # 2-4. Agent, code checks, judge
    answers = run_agent_on_all(questions)
    judge_cache = {r["key"]: r for r in read_jsonl(JUDGE_CACHE)}
    results, blind = [], []
    quota_left = True
    for q in questions:
        r = answers[q["id"]]
        checks = code_checks(q, r)
        verdict = {"correct": None, "supported": None, "unsupported_claims": [],
                   "reasoning": "agent failed" if checks.get("error") else "not judged yet (judge quota)"}
        if not checks.get("error") and quota_left:
            try:
                verdict = judge(q, r, judge_cache)
            except JudgeQuotaExhausted:
                quota_left = False
                log(f"The judge's daily quota ({JUDGE_MODEL}) is used up. Verdicts so far are saved; "
                    f"run again after the reset to judge the rest.")
        result = outcome(q, checks, verdict) if verdict["correct"] is not None or checks.get("error") else "not judged"
        searches = [c["args"].get("query") for c in r.get("trace", []) if c["tool"] == "search"]
        blind.append({"id": q["id"], "kind": q["kind"], "question": q["question"],
                      "reference_answer": q["reference_answer"], "answer": r.get("answer", r.get("error"))})
        results.append({
            "id": q["id"], "kind": q["kind"], "question": q["question"], **checks,
            "judge_correct": verdict["correct"], "judge_supported": verdict["supported"],
            "judge_reasoning": verdict["reasoning"], "unsupported_claims": "; ".join(verdict["unsupported_claims"]),
            "outcome": result, "draft_cause": draft_cause(q, checks, result) if result != "not judged" else "",
            "queries": " || ".join(searches),
            "tokens_in": r.get("tokens", {}).get("input"), "tokens_out": r.get("tokens", {}).get("output"),
            "seconds": r.get("seconds"),
            "guardrail": "; ".join(r.get("guardrail", [])),
        })
    write_csv(EVAL / "answers.csv", blind)
    write_csv(EVAL / "judge.csv", [{"id": r["id"], "correct": r["judge_correct"], "supported": r["judge_supported"],
                                    "reasoning": r["judge_reasoning"], "unsupported_claims": r["unsupported_claims"]}
                                   for r in results])
    write_csv(EVAL / "results.csv", results)

    ran = [r for r in results if r["outcome"] != "error"]  # code checks and cost need no judge
    ok = [r for r in ran if r["outcome"] != "not judged"]
    answerable = [r for r in ok if r["kind"] != "unanswerable"]
    unanswerable = [r for r in ok if r["kind"] == "unanswerable"]
    ran_answerable = [r for r in ran if r["kind"] != "unanswerable"]
    outcomes = Counter(r["outcome"] for r in results)
    cost = {
        "tokens_in_mean": round(statistics.mean(r["tokens_in"] for r in ran)) if ran else None,
        "tokens_out_mean": round(statistics.mean(r["tokens_out"] for r in ran)) if ran else None,
        "seconds_mean": round(statistics.mean(r["seconds"] for r in ran), 1) if ran else None,
        "seconds_median": round(statistics.median(r["seconds"] for r in ran), 1) if ran else None,
        "searches_mean": round(statistics.mean(r["searches"] for r in ran), 2) if ran else None,
    }
    code = {
        "citations_valid": round(statistics.mean(r["citations_valid"] for r in ran), 3) if ran else None,
        "expected_retrieved": round(statistics.mean(r["expected_retrieved"] for r in ran_answerable), 3) if ran_answerable else None,
        "expected_cited": round(statistics.mean(r["expected_cited"] for r in ran_answerable), 3) if ran_answerable else None,
        "refused_unanswerable": sum(r["refused"] for r in ran if r["kind"] == "unanswerable"),
        "refused_answerable_no_citation": sum(r["refused"] and not r["citations"] for r in ran_answerable),
        "guardrail_fired": sum(r["guardrail_fired"] for r in ran),
    }
    agree = agreement(results)
    summary = {"questions": dict(kinds), "retrieval": retrieval, "outcomes": dict(outcomes), "code_checks": code,
               "judge_model": JUDGE_MODEL, "agent_model": next((a.get("model") for a in answers.values()
                                                                if a.get("model")), None),
               "cost_per_question": cost, "agreement": agree,
               "failure_causes": dict(Counter(r["draft_cause"] for r in results if r["draft_cause"]))}
    (EVAL / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

    print("\n## End to end\n")
    print(f"Answerable ({len(answerable)}): " + ", ".join(
        f"{k} {outcomes[k]}" for k in ("correct", "incorrect", "unsupported", "wrong refusal")))
    print(f"Unanswerable ({len(unanswerable)}): correct refusal {outcomes['correct refusal']}, "
          f"answered anyway {outcomes['answered unanswerable']}")
    if outcomes["error"] or outcomes["not judged"]:
        print(f"Not graded: {outcomes['error']} agent errors, {outcomes['not judged']} answers not judged yet "
              f"(run again to retry them)")
    print(f"Code checks: valid citations {pct(code['citations_valid'])}, expected passage retrieved "
          f"{pct(code['expected_retrieved'])}, expected passage cited {pct(code['expected_cited'])}, "
          f"guardrail fired {code['guardrail_fired']}x; refused {code['refused_unanswerable']} of "
          f"{kinds['unanswerable']} unanswerable and {code['refused_answerable_no_citation']} answerable "
          f"(all {len(ran)} answers)")
    print(f"Cost per question: {cost['tokens_in_mean']} input + {cost['tokens_out_mean']} output tokens, "
          f"{cost['seconds_mean']} s mean ({cost['seconds_median']} s median), {cost['searches_mean']} searches")
    if agree["n"]:
        for field in ("correct", "supported"):
            a = agree[field]
            print(f"Judge vs human on {field}: {pct(a['agreement'])} agreement, kappa {a['kappa']} "
                  f"(n = {agree['n']}; disagree on {', '.join(a['disagreements']) or 'none'})")
    else:
        print("Judge vs human: eval/human_labels.csv has no labels yet. Grade eval/answers.csv, "
              "without opening judge.csv or results.csv, then run again.")
    print("\nWritten: eval/retrieval.csv, answers.csv, judge.csv, results.csv, summary.json")


if __name__ == "__main__":
    main()
