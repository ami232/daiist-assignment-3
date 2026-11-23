"""
Assignment 3: evaluation (`main.py evaluate`).

Stage 1: retrieval hit rate at k = 1, 3, 5 per retrieval design, scored with the rule in
eval/scoring_rule.md (fixed before any measurement).

Stage 2: end-to-end. The agent answers every question (saved one by one in eval/answers.jsonl, so an
interrupted run resumes), then code checks (citations, refusals, what the agent retrieved, cost), then
eval/label_sheet.md for your own grades. The LLM judge runs only after eval/human_labels.csv has 20+
grades, so you grade before you see any verdict.

  uv run python main.py evaluate            # everything; finished steps are skipped
  uv run python evaluate.py --redo          # throw away answers and verdicts, run the agent again

Designs compared (every design that has an index in index/ is tried):
  dense_<design>   vector search only (Gemini embeddings in ChromaDB)
  hybrid_<design>  vector search + BM25 keyword search, merged with reciprocal rank fusion

All tuning constants are set below, before the first run, and are not changed afterwards.

Writes: eval/retrieval_results.csv (one row per question and design)
        eval/retrieval_summary.json (the table that goes into REPORT.md)
"""

import csv
import json
import math
import os
import random
import re
import statistics
import sys
from collections import Counter, defaultdict
from pathlib import Path

import index

ROOT = Path(__file__).resolve().parent
EVAL_DIR = ROOT / "eval"
QUESTIONS = EVAL_DIR / "questions.csv"
QUERY_CACHE = EVAL_DIR / "query_cache.json"      # query vectors, so a re-run costs no quota (not committed)
RESULTS_CSV = EVAL_DIR / "retrieval_results.csv"
SUMMARY_JSON = EVAL_DIR / "retrieval_summary.json"
ANSWERS = EVAL_DIR / "answers.jsonl"                 # full record per question: answer, tool trace, tokens, seconds
ANSWERS_CSV = EVAL_DIR / "answers.csv"               # the same, one readable row per question, with the code checks
LABEL_SHEET = EVAL_DIR / "label_sheet.md"            # what you read when you grade
HUMAN_LABELS = EVAL_DIR / "human_labels.csv"
RUBRIC = EVAL_DIR / "judge_rubric.md"                # written by you
VERDICTS = EVAL_DIR / "judge_verdicts.csv"
E2E_SUMMARY = EVAL_DIR / "end_to_end_summary.json"

KS = (1, 3, 5)
POOL = 30                 # candidates taken from each ranking before fusion
RRF_K = 60                # reciprocal rank fusion constant
BM25_K1, BM25_B = 1.5, 0.75
MIN_LABELS = 20
LABEL_SEED = 7            # fixes the order of the label sheet (a random order, the same on every run)
JUDGE_MODEL = os.environ.get("JUDGE_MODEL", "gemini-3.5-flash")
# Refusal check in code: a refusal says so up front, so only the start of the answer is searched. A heuristic:
# it is compared with the judge and with your grades, not trusted on its own.
REFUSAL = re.compile(
    r"(?:do(?:es)? not|don't|doesn't|cannot|can't|could not|couldn't|unable to|not able to)\b[^.\n]{0,80}?"
    r"\b(?:cover|address|contain|include|find|provide|specify|mention|answer)"
    r"|\bnot covered\b|\bno (?:relevant )?(?:information|passages?|provisions?)\b|\boutside (?:the )?scope\b",
    re.IGNORECASE,
)
REFUSAL_WINDOW = 400
STOPWORDS = set(
    "a an and are as at be but by for from has have how i if in is it its my of on or our so that the their "
    "them then there these they this to us was we what when where which who will with you your do does can "
    "should must".split()
)


# --------------------------------------------------------------------------
# 1. Labels and the scoring rule
# --------------------------------------------------------------------------

def parse_required(row: dict) -> list[tuple[str, str]]:
    sources = [s.strip() for s in row["expected_source"].split(";") if s.strip()]
    labels = [s.strip() for s in row["expected_location"].split(";") if s.strip()]
    if len(sources) != len(labels):
        raise SystemExit(f"{row['id']}: expected_source and expected_location must list the same number of passages.")
    return list(zip(sources, labels))


def parse_equivalents(row: dict) -> list[tuple[int | None, str, str, bool]]:
    """`[N>][=]source:label`, `;` between several. N = which required passage it stands in for (1-based)."""
    out = []
    for item in (row.get("equivalent_locations") or "").split(";"):
        item = item.strip()
        if not item:
            continue
        m = re.match(r"^(?:(\d+)>)?(=)?([^:]+):(.+)$", item)
        if not m:
            raise SystemExit(f"{row['id']}: cannot read equivalent location {item!r}.")
        number, exact, source, label = m.groups()
        out.append((int(number) if number else None, source.strip(), label.strip(), bool(exact)))
    return out


def matches(chunk: dict, source: str, label: str, exact: bool = False) -> bool:
    """Same document, and the chunk's section is the label or (unless exact) a sub-section of it."""
    if chunk["source"] != source:
        return False
    return chunk["section"] == label or (not exact and chunk["section"].startswith(label + "."))


def outcome(row: dict, ranked: list[dict], k: int) -> str:
    """hit / equivalent / miss for one answerable question, from the top k chunks."""
    top = ranked[:k]
    required, equivalents = parse_required(row), parse_equivalents(row)
    used: set[int] = set()                        # one chunk covers at most one required passage
    covered = [False] * len(required)
    via_equivalent = [False] * len(required)
    for i, (source, label) in enumerate(required):
        for j, chunk in enumerate(top):
            if j not in used and matches(chunk, source, label):
                covered[i] = True
                used.add(j)
                break
    for i in range(len(required)):
        if covered[i]:
            continue
        for number, source, label, exact in equivalents:
            if number not in (None, i + 1):
                continue
            for j, chunk in enumerate(top):
                if j not in used and matches(chunk, source, label, exact):
                    covered[i] = via_equivalent[i] = True
                    used.add(j)
                    break
            if covered[i]:
                break
    if not all(covered):
        return "miss"
    return "equivalent" if any(via_equivalent) else "hit"


# --------------------------------------------------------------------------
# 2. Chunks, BM25, dense search, fusion
# --------------------------------------------------------------------------

def indexed_designs() -> list[str]:
    import chromadb
    from chromadb.config import Settings

    client = chromadb.PersistentClient(path=str(index.INDEX_DIR), settings=Settings(anonymized_telemetry=False))
    names = {c if isinstance(c, str) else c.name for c in client.list_collections()}
    found = []
    for design in index.DESIGNS:
        if f"chunks_{design}" in names and client.get_collection(f"chunks_{design}").count() > 0:
            found.append(design)
    return found


def load_chunks(design: str) -> dict[str, dict]:
    data = index.get_collection(design).get(include=["documents", "metadatas"])
    chunks = {}
    for id_, text, meta in zip(data["ids"], data["documents"], data["metadatas"]):
        chunks[id_] = {"id": id_, "text": text, **meta}
    return chunks


def tokens(text: str) -> list[str]:
    return [t for t in re.findall(r"[a-z0-9]+", text.lower()) if t not in STOPWORDS]


class BM25:
    def __init__(self, chunks: dict[str, dict]):
        self.ids = list(chunks)
        # The heading and location are searchable too, as they are in the embedded text.
        self.docs = [Counter(tokens(f"{c['title']} {c['location']} {c['heading']} {c['text']}")) for c in chunks.values()]
        self.lengths = [sum(d.values()) for d in self.docs]
        self.avg = sum(self.lengths) / len(self.lengths)
        df = Counter(t for d in self.docs for t in d)
        n = len(self.docs)
        self.idf = {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()}

    def rank(self, query: str, pool: int) -> list[str]:
        q = tokens(query)
        scores = []
        for i, doc in enumerate(self.docs):
            s = 0.0
            for t in q:
                f = doc.get(t, 0)
                if f:
                    s += self.idf[t] * f * (BM25_K1 + 1) / (f + BM25_K1 * (1 - BM25_B + BM25_B * self.lengths[i] / self.avg))
            scores.append(s)
        order = sorted(range(len(scores)), key=lambda i: -scores[i])
        return [self.ids[i] for i in order[:pool] if scores[i] > 0]


def dense_rank(design: str, vector: list[float], pool: int) -> list[str]:
    collection = index.get_collection(design)
    return collection.query(query_embeddings=[vector], n_results=min(pool, collection.count()))["ids"][0]


def fuse(rankings: list[list[str]]) -> list[str]:
    score: Counter = Counter()
    for ranking in rankings:
        for position, id_ in enumerate(ranking):
            score[id_] += 1 / (RRF_K + position + 1)
    return [id_ for id_, _ in score.most_common()]


def query_vectors(questions: list[str]) -> dict[str, list[float]]:
    try:
        cache = json.loads(QUERY_CACHE.read_text())
    except (OSError, ValueError):
        cache = {}
    missing = [q for q in questions if q not in cache]
    if missing:
        client = index.gemini_client()
        for n, q in enumerate(missing, 1):
            cache[q] = index.embed_query(q, client)
            index.log(f"  embedded query {n}/{len(missing)}")
            QUERY_CACHE.write_text(json.dumps(cache))     # saved as we go: a quota stop loses nothing
    return {q: cache[q] for q in questions}


# --------------------------------------------------------------------------
# 3. Retrieval stage
# --------------------------------------------------------------------------

def read_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if (r.get("question") or "").strip()]


def retrieval_stage() -> dict:
    rows = [r for r in read_questions() if r["kind"].strip().lower() != "unanswerable"]
    designs = indexed_designs()
    if not designs:
        raise SystemExit("No index found in index/. Run `uv run python main.py index` first.")
    vectors = query_vectors([r["question"] for r in rows])

    results, rankers = [], {}
    for design in designs:
        chunks = load_chunks(design)
        bm25 = BM25(chunks)
        rankers[f"dense_{design}"] = lambda r, d=design, c=chunks: [c[i] for i in dense_rank(d, vectors[r["question"]], POOL)]
        rankers[f"hybrid_{design}"] = lambda r, d=design, c=chunks, b=bm25: [
            c[i] for i in fuse([dense_rank(d, vectors[r["question"]], POOL), b.rank(r["question"], POOL)])
        ]

    for name, ranker in rankers.items():
        for row in rows:
            ranked = ranker(row)
            res = {"design": name, "id": row["id"], "kind": row["kind"].strip().lower()}
            for k in KS:
                res[f"k{k}"] = outcome(row, ranked, k)
            res["top5"] = " | ".join(f"{c['source']}:{c['section']}" for c in ranked[:5])
            results.append(res)

    summary = summarise(results)
    write_outputs(results, summary)
    print_summary(summary, results)
    return summary


def summarise(results: list[dict]) -> dict:
    summary: dict = {}
    for design in dict.fromkeys(r["design"] for r in results):
        mine = [r for r in results if r["design"] == design]
        summary[design] = {}
        for label, subset in (("all", mine), ("single", [r for r in mine if r["kind"] == "single"]),
                              ("multi", [r for r in mine if r["kind"] == "multi"])):
            if not subset:
                continue
            summary[design][label] = {"questions": len(subset)}
            for k in KS:
                hits = sum(r[f"k{k}"] == "hit" for r in subset)
                equivalents = sum(r[f"k{k}"] == "equivalent" for r in subset)
                summary[design][label][f"k{k}"] = {
                    "hit": hits, "equivalent": equivalents,
                    "strict": round(hits / len(subset), 3),
                    "lenient": round((hits + equivalents) / len(subset), 3),
                }
    return summary


def write_outputs(results: list[dict], summary: dict) -> None:
    with RESULTS_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["design", "id", "kind", "k1", "k3", "k5", "top5"])
        writer.writeheader()
        writer.writerows(results)
    SUMMARY_JSON.write_text(json.dumps(summary, indent=2))


def print_summary(summary: dict, results: list[dict]) -> None:
    print("\nRetrieval hit rate (strict = labelled passage retrieved; lenient = strict + equivalent passages)\n")
    print(f"{'design':<22}{'subset':<8}{'n':>3}   " + "   ".join(f"k={k}: strict/lenient" for k in KS))
    for design, subsets in summary.items():
        for label, data in subsets.items():
            cells = "   ".join(f"{data[f'k{k}']['strict']:.2f} / {data[f'k{k}']['lenient']:.2f}".rjust(17) for k in KS)
            print(f"{design:<22}{label:<8}{data['questions']:>3}   {cells}")
    print("\nMisses at k=5 (for the failure analysis):")
    by_design = defaultdict(list)
    for r in results:
        if r["k5"] == "miss":
            by_design[r["design"]].append(r["id"])
    for design in summary:
        print(f"  {design}: {', '.join(by_design[design]) or 'none'}")
    print(f"\nWrote {RESULTS_CSV.relative_to(ROOT)} and {SUMMARY_JSON.relative_to(ROOT)}")

# --------------------------------------------------------------------------
# 4. End-to-end: the agent answers every question
# --------------------------------------------------------------------------

def load_answers() -> dict[str, dict]:
    records: dict[str, dict] = {}
    if ANSWERS.is_file():
        for line in ANSWERS.read_text(encoding="utf-8").splitlines():
            if line.strip():
                record = json.loads(line)
                records[record["id"]] = record       # a later line replaces an earlier one
    return records


def answers_stage(rows: list[dict], redo: bool) -> dict[str, dict]:
    if redo:
        for path in (ANSWERS, VERDICTS):
            path.unlink(missing_ok=True)
    records = load_answers()
    todo = [r for r in rows if r["id"] not in records or records[r["id"]]["question"] != r["question"]]
    if todo:
        import agent

        by_question = {r["question"]: r for r in todo}
        print(f"\nThe agent answers {len(todo)} question(s) ({len(rows) - len(todo)} already saved). "
              "Ctrl+C stops safely; run again to continue.", file=sys.stderr)

        def save(result: dict) -> None:
            row = by_question[result["question"]]
            record = {"id": row["id"], "kind": row["kind"].strip().lower(), **result}
            with ANSWERS.open("a", encoding="utf-8") as f:
                f.write(json.dumps(record, ensure_ascii=False) + "\n")
            records[record["id"]] = record
            print(f"  [{len(records)}/{len(rows)}] {record['id']}: {record['seconds']} s, "
                  f"{len(record['tool_calls'])} tool call(s)", file=sys.stderr)

        # No terminal approval during evaluation: add_document is always refused here.
        agent.ask_many([r["question"] for r in todo], approve=lambda tool, args: False, on_result=save, keep_going=True)
    missing = [r["id"] for r in rows if r["id"] not in records]
    if missing:
        print(f"\nNo answer yet for: {', '.join(missing)}. Run the evaluation again to retry them.", file=sys.stderr)
    return records


# --------------------------------------------------------------------------
# 5. Checks in code
# --------------------------------------------------------------------------

def seen_chunks(retrieved: list) -> list[dict]:
    """What the agent actually retrieved, in the shape outcome() reads: source and section of each passage."""
    import agent

    chunks = []
    for source, location in retrieved:
        refs = agent.references(location)
        if refs:
            kind, ident = refs[0]
            chunks.append({"source": source, "section": f"{kind} {ident}"})
    return chunks


def code_checks(rows: list[dict], records: dict[str, dict]) -> list[dict]:
    checks = []
    for row in rows:
        record = records.get(row["id"])
        if not record:
            continue
        kind = row["kind"].strip().lower()
        valid, invalid = record["valid_citations"], record["invalid_citations"]
        check = {
            "id": row["id"],
            "kind": kind,
            "searches": sum(c["tool"] == "search" for c in record["tool_calls"]),
            "valid_citations": len(valid),
            "invalid_citations": len(invalid),
            "refused": bool(REFUSAL.search(record["raw_answer"][:REFUSAL_WINDOW])),
            "agent_retrieval": "",
            "input_tokens": record["input_tokens"],
            "output_tokens": record["output_tokens"],
            "seconds": record["seconds"],
            "flags": "; ".join(record["flags"]),
        }
        if kind != "unanswerable":
            ranked = seen_chunks(record["retrieved"])
            check["agent_retrieval"] = outcome(row, ranked, max(len(ranked), 1))
        checks.append(check)
    return checks


def write_answers_csv(checks: list[dict], records: dict[str, dict], rows: list[dict]) -> None:
    questions = {r["id"]: r["question"] for r in rows}
    fields = ["id", "kind", "question", "answer", "searches", "valid_citations", "invalid_citations", "refused",
              "agent_retrieval", "input_tokens", "output_tokens", "seconds", "flags"]
    with ANSWERS_CSV.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        for check in checks:
            writer.writerow({**check, "question": questions[check["id"]], "answer": records[check["id"]]["raw_answer"]})


def cost_summary(checks: list[dict]) -> dict:
    def stats(values: list[float]) -> dict:
        ordered = sorted(values)
        return {"mean": round(statistics.mean(values), 1), "median": round(statistics.median(values), 1),
                "p90": round(ordered[min(len(ordered) - 1, math.ceil(0.9 * len(ordered)) - 1)], 1),
                "max": round(max(values), 1)}

    return {
        "questions": len(checks),
        "seconds": stats([c["seconds"] for c in checks]),
        "input_tokens": stats([c["input_tokens"] for c in checks]),
        "output_tokens": stats([c["output_tokens"] for c in checks]),
        "searches": stats([c["searches"] for c in checks]),
        "total_input_tokens": sum(c["input_tokens"] for c in checks),
        "total_output_tokens": sum(c["output_tokens"] for c in checks),
    }


def code_summary(checks: list[dict]) -> dict:
    answerable = [c for c in checks if c["kind"] != "unanswerable"]
    unanswerable = [c for c in checks if c["kind"] == "unanswerable"]
    return {
        "answerable": {
            "questions": len(answerable),
            "answers_with_a_valid_citation_and_no_invalid_one": sum(c["valid_citations"] > 0 and c["invalid_citations"] == 0 for c in answerable),
            "answers_with_an_unverified_citation": sum(c["invalid_citations"] > 0 for c in answerable),
            "answers_without_any_citation": sum(c["valid_citations"] + c["invalid_citations"] == 0 for c in answerable),
            "answers_that_look_like_a_refusal": [c["id"] for c in answerable if c["refused"]],
            "agent_retrieval": {k: sum(c["agent_retrieval"] == k for c in answerable) for k in ("hit", "equivalent", "miss")},
        },
        "unanswerable": {
            "questions": len(unanswerable),
            "refused": sum(c["refused"] for c in unanswerable),
            "not_refused": [c["id"] for c in unanswerable if not c["refused"]],
        },
    }


# --------------------------------------------------------------------------
# 6. Your grades: the sheet you read, the file you fill in
# --------------------------------------------------------------------------

def write_label_sheet(rows: list[dict], records: dict[str, dict]) -> None:
    order = [r for r in rows if r["id"] in records]
    random.Random(LABEL_SEED).shuffle(order)
    parts = [
        "# Label sheet\n",
        "Grade the answers in this order (it is random) in `eval/human_labels.csv`, one line per answer: "
        "`id,correct,supported,notes`. At least 20; more is better. This file shows no judge verdicts.\n",
        "- `correct`: 1 if the answer is right against the reference answer (for an unanswerable question: "
        "a proper refusal), else 0.\n- `supported`: 1 if every claim in the answer is in the retrieved passages "
        "below, else 0.\n- `notes`: why, for every 0.\n",
    ]
    for n, row in enumerate(order, 1):
        record = records[row["id"]]
        searches = [c for c in record["tool_calls"] if c["tool"] == "search"]
        evidence = "\n\n".join(f"Search: {c['args'].get('query', '')}\n\n{c['result']}" for c in searches) or "(no search)"
        parts.append(
            f"\n---\n\n## {n}. {row['id']} ({row['kind'].strip().lower()})\n\n"
            f"**Question:** {row['question']}\n\n**Reference answer:** {row['reference_answer']}\n\n"
            f"**Agent answer:**\n\n```text\n{record['raw_answer']}\n```\n\n"
            f"<details><summary>Passages the agent retrieved</summary>\n\n```text\n{evidence}\n```\n\n</details>\n"
        )
    LABEL_SHEET.write_text("".join(parts), encoding="utf-8")


def load_human_labels(known_ids: set[str]) -> dict[str, dict]:
    labels: dict[str, dict] = {}
    if not HUMAN_LABELS.is_file():
        return labels
    with HUMAN_LABELS.open(newline="", encoding="utf-8") as f:
        for r in csv.DictReader(f):
            id_ = (r.get("id") or "").strip()
            correct, supported = (r.get("correct") or "").strip(), (r.get("supported") or "").strip()
            if id_ in known_ids and correct in ("0", "1") and supported in ("0", "1"):
                labels[id_] = {"correct": int(correct), "supported": int(supported)}
    return labels


# --------------------------------------------------------------------------
# 7. The LLM judge and its agreement with you
# --------------------------------------------------------------------------

def judge_one(judge, rubric: str, row: dict, record: dict) -> dict:
    searches = [c for c in record["tool_calls"] if c["tool"] == "search"]
    evidence = "\n\n".join(f"Search: {c['args'].get('query', '')}\n{c['result']}" for c in searches) or "(no search)"
    unanswerable = row["kind"].strip().lower() == "unanswerable"
    prompt = (
        f"{rubric.strip()}\n\n=== CASE ===\n"
        f"Question: {row['question']}\n"
        f"The documents {'do NOT answer this question' if unanswerable else 'answer this question'}.\n"
        f"Reference answer: {row['reference_answer']}\n\n"
        f"Passages the assistant retrieved:\n{evidence}\n\n"
        f"Assistant's answer:\n{record['raw_answer']}\n\n"
        "=== END OF CASE ===\nGive a short reason first, then correct and supported."
    )
    verdict = judge.invoke(prompt)
    return {"correct": int(bool(verdict.correct)), "supported": int(bool(verdict.supported)), "reason": verdict.reason}


def judge_stage(rows: list[dict], records: dict[str, dict]) -> dict[str, dict]:
    from pydantic import BaseModel, Field

    from langchain_google_genai import ChatGoogleGenerativeAI

    from api_key import load_api_key

    class Verdict(BaseModel):
        reason: str = Field(description="One or two sentences: what decides the two verdicts.")
        correct: bool = Field(description="Right against the reference answer, or a proper refusal.")
        supported: bool = Field(description="Every claim in the answer is in the retrieved passages.")

    verdicts: dict[str, dict] = {}
    if VERDICTS.is_file():
        with VERDICTS.open(newline="", encoding="utf-8") as f:
            for r in csv.DictReader(f):
                verdicts[r["id"]] = {"correct": int(r["correct"]), "supported": int(r["supported"]), "reason": r["reason"]}
    todo = [r for r in rows if r["id"] in records and r["id"] not in verdicts]
    if todo:
        load_api_key()
        judge = ChatGoogleGenerativeAI(model=JUDGE_MODEL, max_retries=6).with_structured_output(Verdict)
        rubric = RUBRIC.read_text(encoding="utf-8")
        print(f"\nThe judge ({JUDGE_MODEL}) grades {len(todo)} answer(s).", file=sys.stderr)
        for row in todo:
            try:
                verdicts[row["id"]] = judge_one(judge, rubric, row, records[row["id"]])
            except Exception as error:
                print(f"  judge failed on {row['id']}: {type(error).__name__}: {str(error)[:200]}", file=sys.stderr)
                continue
            with VERDICTS.open("w", newline="", encoding="utf-8") as f:
                writer = csv.DictWriter(f, fieldnames=["id", "correct", "supported", "reason"])
                writer.writeheader()
                writer.writerows({"id": i, **v} for i, v in verdicts.items())
            print(f"  judged {row['id']}", file=sys.stderr)
    return verdicts


def kappa(pairs: list[tuple[int, int]]) -> float | None:
    n = len(pairs)
    observed = sum(a == b for a, b in pairs) / n
    a1, b1 = sum(a for a, _ in pairs) / n, sum(b for _, b in pairs) / n
    expected = a1 * b1 + (1 - a1) * (1 - b1)
    return None if expected == 1 else round((observed - expected) / (1 - expected), 3)


def agreement(labels: dict[str, dict], verdicts: dict[str, dict]) -> dict:
    shared = sorted(i for i in labels if i in verdicts)
    out: dict = {"answers_graded_by_both": len(shared)}
    for field in ("correct", "supported"):
        pairs = [(labels[i][field], verdicts[i][field]) for i in shared]
        if not pairs:
            continue
        out[field] = {
            "agree": sum(a == b for a, b in pairs),
            "of": len(pairs),
            "rate": round(sum(a == b for a, b in pairs) / len(pairs), 3),
            "cohen_kappa": kappa(pairs),
            "human_1_judge_0": [i for i in shared if labels[i][field] == 1 and verdicts[i][field] == 0],
            "human_0_judge_1": [i for i in shared if labels[i][field] == 0 and verdicts[i][field] == 1],
        }
    return out


def rate(items: list[dict], field: str) -> dict:
    return {"n": len(items), "yes": sum(i[field] for i in items), "rate": round(sum(i[field] for i in items) / len(items), 3)} if items else {"n": 0}


def grade_summary(rows: list[dict], grades: dict[str, dict]) -> dict:
    """Correct and supported rates by kind, for one set of grades (the judge's or yours)."""
    kinds = {r["id"]: r["kind"].strip().lower() for r in rows}
    out = {}
    for label, wanted in (("answerable", lambda k: k != "unanswerable"), ("unanswerable", lambda k: k == "unanswerable")):
        mine = [g for i, g in grades.items() if i in kinds and wanted(kinds[i])]
        out[label] = {"correct": rate(mine, "correct"), "supported": rate(mine, "supported")}
    return out


# --------------------------------------------------------------------------
# 8. Put it together
# --------------------------------------------------------------------------

def end_to_end_stage(redo: bool) -> None:
    rows = read_questions()
    records = answers_stage(rows, redo)
    if not records:
        return
    checks = code_checks(rows, records)
    write_answers_csv(checks, records, rows)
    write_label_sheet(rows, records)
    labels = load_human_labels(set(records))
    summary: dict = {"model": next(iter(records.values()))["model"], "code_checks": code_summary(checks), "cost": cost_summary(checks),
                     "human_graded": len(labels)}
    if labels:
        summary["human_grades"] = grade_summary(rows, labels)

    if len(labels) < MIN_LABELS:
        print(f"\nJudge not run yet: eval/human_labels.csv has {len(labels)} usable grades, {MIN_LABELS} are needed first "
              f"(read eval/label_sheet.md). That way you grade before you see any verdict.")
    elif not RUBRIC.is_file():
        print(f"\nJudge not run yet: write your rubric in {RUBRIC.relative_to(ROOT)} first.")
    else:
        verdicts = judge_stage(rows, records)
        summary["judge_model"] = JUDGE_MODEL
        summary["judge_grades"] = grade_summary(rows, verdicts)
        summary["judge_vs_human"] = agreement(labels, verdicts)
    E2E_SUMMARY.write_text(json.dumps(summary, indent=2))
    print_end_to_end(summary)


def print_end_to_end(summary: dict) -> None:
    code, cost = summary["code_checks"], summary["cost"]
    a, u = code["answerable"], code["unanswerable"]
    print(f"\nEnd-to-end ({summary['model']}, {cost['questions']} questions)")
    print(f"  answerable ({a['questions']}): valid citations only {a['answers_with_a_valid_citation_and_no_invalid_one']}, "
          f"unverified citation {a['answers_with_an_unverified_citation']}, no citation {a['answers_without_any_citation']}, "
          f"look like a refusal {a['answers_that_look_like_a_refusal'] or 'none'}")
    print(f"  what the agent retrieved, answerable: {a['agent_retrieval']}")
    print(f"  unanswerable ({u['questions']}): refused {u['refused']}, not refused {u['not_refused'] or 'none'}")
    print(f"  cost per question: {cost['seconds']['median']} s median ({cost['seconds']['p90']} s p90), "
          f"{cost['input_tokens']['mean']:.0f} tokens in and {cost['output_tokens']['mean']:.0f} out on average, "
          f"{cost['searches']['mean']} searches")
    for key, title in (("judge_grades", "judge"), ("human_grades", "you")):
        if key in summary:
            g = summary[key]
            print(f"  {title}: answerable correct {g['answerable']['correct'].get('yes', 0)}/{g['answerable']['correct']['n']}, "
                  f"unanswerable correct {g['unanswerable']['correct'].get('yes', 0)}/{g['unanswerable']['correct']['n']}, "
                  f"supported {g['answerable']['supported'].get('yes', 0) + g['unanswerable']['supported'].get('yes', 0)}/"
                  f"{g['answerable']['supported']['n'] + g['unanswerable']['supported']['n']}")
    if "judge_vs_human" in summary:
        for field in ("correct", "supported"):
            d = summary["judge_vs_human"].get(field)
            if d:
                print(f"  judge agrees with you on {field}: {d['agree']}/{d['of']} (kappa {d['cohen_kappa']}); "
                      f"you 1 / judge 0: {d['human_1_judge_0'] or 'none'}; you 0 / judge 1: {d['human_0_judge_1'] or 'none'}")
    print(f"\nWrote {ANSWERS.relative_to(ROOT)}, {ANSWERS_CSV.relative_to(ROOT)}, {LABEL_SHEET.relative_to(ROOT)}, "
          f"{E2E_SUMMARY.relative_to(ROOT)}")


def main() -> int:
    retrieval_stage()
    end_to_end_stage(redo="--redo" in sys.argv)
    return 0


if __name__ == "__main__":
    sys.exit(main())
