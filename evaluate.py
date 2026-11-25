"""
Assignment 3: evaluation (`main.py evaluate`). May be evaluate.ipynb instead.

Hit rate at 1/3/5 per retrieval design; agent answers on every question;
code checks; an LLM judge with a rubric and the retrieved text as evidence;
agreement with eval/human_labels.csv. Save results in eval/.

Start from session 10's 07-own-harness/evaluate.py.
"""

import csv
import hashlib
import json
import math
import re
import time
from collections import Counter, defaultdict
from pathlib import Path

from index import EMBED_DIM, EMBED_MODEL, get_collection

ROOT = Path(__file__).resolve().parent
EVAL_DIR = ROOT / "eval"
QUESTIONS_PATH = EVAL_DIR / "questions.csv"
CACHE_PATH = EVAL_DIR / "query_vectors.json"
RESULTS_PATH = EVAL_DIR / "retrieval_results.csv"
SUMMARY_PATH = EVAL_DIR / "retrieval_summary.json"
TOP_N = 50
KS = (1, 3, 5)

# Use a fixed keyword-search configuration, rather than tuning it on the test set.
STOPWORDS = set("a an and are as at be before by can do does for from how i if in into is it me my of on or our should so that the their them these they this to using was what when where which who why will with you your".split())


def tokenize(text):
    """Simple case-insensitive word tokens for keyword retrieval."""
    return [term for term in re.findall(r"[a-z0-9]+", text.lower()) if term not in STOPWORDS]


def load_questions():
    with QUESTIONS_PATH.open(encoding="utf-8-sig", newline="") as f:
        rows = list(csv.DictReader(f))
    if len(rows) < 30:
        raise ValueError(f"Expected at least 30 questions, found {len(rows)}")
    for row in rows:
        if row["kind"].strip().lower() == "unanswerable":
            continue  # No known correct passage; not counted in retrieval hit rate.
        sources = [v.strip() for v in row["expected_source"].split(";")]
        locations = [v.strip() for v in row["expected_location"].split(";")]
        if not sources or len(sources) != len(locations) or not all(sources + locations):
            raise ValueError(f"Bad evidence fields in {row['id']}")
    return rows


def load_corpus(collection):
    data = collection.get(include=["documents", "metadatas"])
    ids = data["ids"]
    texts = data["documents"]
    metadatas = data["metadatas"]
    if not ids or len(ids) != len(texts) or len(ids) != len(metadatas):
        raise RuntimeError("ChromaDB index is empty or missing documents/metadata")
    return {id_: {"text": t, "meta": m} for id_, t, m in zip(ids, texts, metadatas)}


class BM25:
    """Small in-memory keyword index; no new model calls or extra dependencies."""

    def __init__(self, docs):
        self.tf = {id_: Counter(tokenize(record["text"])) for id_, record in docs.items()}
        self.lengths = {id_: sum(counts.values()) for id_, counts in self.tf.items()}
        self.n = len(docs)
        self.avg_len = sum(self.lengths.values()) / max(1, self.n)
        self.df = Counter()
        self.inverted = defaultdict(list)
        for id_, counts in self.tf.items():
            for word in counts:
                self.df[word] += 1
                self.inverted[word].append(id_)

    def search(self, query, top_n=TOP_N):
        scores = defaultdict(float)
        k1, b = 1.5, 0.75
        for term in set(tokenize(query)):
            df = self.df.get(term, 0)
            if not df:
                continue
            idf = math.log1p((self.n - df + 0.5) / (df + 0.5))
            for id_ in self.inverted[term]:
                tf = self.tf[id_][term]
                length_factor = k1 * (1 - b + b * self.lengths[id_] / max(1, self.avg_len))
                scores[id_] += idf * tf * (k1 + 1) / (tf + length_factor)
        return [id_ for id_, _ in sorted(scores.items(), key=lambda item: (-item[1], item[0]))[:top_n]]


def query_cache():
    if not CACHE_PATH.exists():
        return {"model": EMBED_MODEL, "dimensions": EMBED_DIM, "vectors": {}}
    cache = json.loads(CACHE_PATH.read_text(encoding="utf-8"))
    if cache.get("model") != EMBED_MODEL or cache.get("dimensions") != EMBED_DIM:
        raise ValueError("Saved query vectors were built with a different embedding model/dimension")
    return cache


def save_cache(cache):
    EVAL_DIR.mkdir(exist_ok=True)
    temporary = CACHE_PATH.with_suffix(".tmp")
    temporary.write_text(json.dumps(cache), encoding="utf-8")
    temporary.replace(CACHE_PATH)


def get_query_vectors(questions):
    """One Gemini embedding per *new* question; save every successful query."""
    cache = query_cache()
    vectors = {}
    pending = []
    for row in questions:
        if row["kind"].strip().lower() == "unanswerable":
            continue
        question = row["question"].strip()
        key = hashlib.sha256(question.encode("utf-8")).hexdigest()
        vector = cache["vectors"].get(key)
        if vector is None:
            pending.append((row["id"], question, key))
        else:
            vectors[row["id"]] = vector

    print(f"Query vectors cached: {len(vectors)} | Need embedding: {len(pending)}", flush=True)
    if pending:
        from google import genai
        from google.genai import types
        from api_key import load_api_key

        client = genai.Client(api_key=load_api_key())
        try:
            for num, (qid, question, key) in enumerate(pending, start=1):
                for attempt in range(5):
                    try:
                        response = client.models.embed_content(
                            model=EMBED_MODEL,
                            contents=f"query: {question}",
                            config=types.EmbedContentConfig(output_dimensionality=EMBED_DIM),
                        )
                        vector = response.embeddings[0].values
                        if len(vector) != EMBED_DIM:
                            raise ValueError(f"Embedding dimension mismatch for {qid}")
                        break
                    except Exception as exc:
                        detail = str(exc).lower()
                        if attempt == 4 or not any(x in detail for x in ("429", "resource_exhausted", "rate limit")):
                            raise
                        match = re.search(r"retry in\s+(\d+(?:\.\d+)?)s", detail)
                        wait = max(35.0, float(match.group(1)) + 3) if match else 65.0
                        print(f"Rate limit for {qid}. Retrying after {wait:.0f}s.", flush=True)
                        time.sleep(wait)
                cache["vectors"][key] = vector
                vectors[qid] = vector
                save_cache(cache)
                if num % 5 == 0 or num == len(pending):
                    print(f"Embedded {num}/{len(pending)} new questions", flush=True)
        finally:
            client.close()
    return vectors


def expected_locations(row):
    sources = [s.strip() for s in row["expected_source"].split(";")]
    locations = [l.strip() for l in row["expected_location"].split(";")]
    return set(zip(sources, locations))


def evidence_hits(ranking, docs, expected, k):
    found = {
        (docs[id_]["meta"].get("source"), docs[id_]["meta"].get("location"))
        for id_ in ranking[:k]
    }
    return bool(found & expected), expected.issubset(found)


def reciprocal_rank_fusion(dense_ids, keyword_ids, k=60):
    score = defaultdict(float)
    for ranking in (dense_ids, keyword_ids):
        for rank, id_ in enumerate(ranking, start=1):
            score[id_] += 1 / (k + rank)
    return [id_ for id_, _ in sorted(score.items(), key=lambda item: (-item[1], item[0]))]


def run():
    questions = load_questions()
    answerable = [q for q in questions if q["kind"].strip().lower() != "unanswerable"]
    multi_count = sum(q["kind"].strip().lower() == "multi" for q in answerable)
    collection = get_collection()
    docs = load_corpus(collection)
    print(f"Loaded {len(docs)} indexed chunks. {len(answerable)} answerable questions ({multi_count} multi-passage).")
    if collection.count() != len(docs):
        raise RuntimeError("ChromaDB document count does not match index")
    keyword = BM25(docs)
    vectors = get_query_vectors(questions)
    results = []
    for q in answerable:
        qid = q["id"]
        got = collection.query(
            query_embeddings=[vectors[qid]],
            n_results=min(TOP_N, len(docs)),
            include=["metadatas", "distances"],
        )
        dense = got["ids"][0]
        bm25 = keyword.search(q["question"])
        hybrid = reciprocal_rank_fusion(dense, bm25)
        expected = expected_locations(q)
        for design, ranking in (("semantic", dense), ("hybrid_rrf", hybrid)):
            record = {"id": qid, "kind": q["kind"], "design": design, "question": q["question"]}
            for k in KS:
                any_hit, all_hit = evidence_hits(ranking, docs, expected, k)
                record[f"any_hit_at_{k}"] = int(any_hit)
                record[f"complete_hit_at_{k}"] = int(all_hit)
            record["top5_sources"] = " | ".join(
                f"{docs[id_]['meta'].get('source')}:{docs[id_]['meta'].get('location')}"
                for id_ in ranking[:5]
            )
            results.append(record)

    EVAL_DIR.mkdir(exist_ok=True)
    with RESULTS_PATH.open("w", encoding="utf-8", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(results[0]))
        writer.writeheader()
        writer.writerows(results)

    summary = {
        "notes": [
            "Hit Rate@k uses exact source + PDF page matches (not exact answer spans).",
            "Unanswerable questions are excluded from retrieval hit-rate denominators.",
            "Complete Hit Rate@k requires ALL expected source/page pairs for multi-passage questions.",
            "Hybrid uses reciprocal rank fusion of semantic and BM25 rankings over the same 342 chunks.",
            "This is a small development evaluation set; do not claim independent generalization from these scores.",
        ],
        "indexed_chunks": len(docs),
        "answerable_questions": len(answerable),
        "multi_questions": multi_count,
        "designs": {},
    }
    for design in ("semantic", "hybrid_rrf"):
        group = [r for r in results if r["design"] == design]
        multigroup = [r for r in group if r["kind"].strip().lower() == "multi"]
        stats = {}
        for k in KS:
            stats[f"hit_rate_at_{k}"] = round(sum(r[f"any_hit_at_{k}"] for r in group) / len(group), 4)
            stats[f"complete_hit_rate_at_{k}"] = round(sum(r[f"complete_hit_at_{k}"] for r in group) / len(group), 4)
            stats[f"multi_complete_at_{k}"] = round(sum(r[f"complete_hit_at_{k}"] for r in multigroup) / len(multigroup), 4) if multigroup else None
        summary["designs"][design] = stats

    SUMMARY_PATH.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print("\nRetrieval results (answerable questions only):")
    print("Design          Hit@1   Hit@3   Hit@5   Complete@5   MultiComplete@5")
    for design, stats in summary["designs"].items():
        print(f"{design:<15} {stats['hit_rate_at_1']:.1%}   {stats['hit_rate_at_3']:.1%}   {stats['hit_rate_at_5']:.1%}   {stats['complete_hit_rate_at_5']:.1%}        {stats['multi_complete_at_5']:.1%}")
    print("\nSaved:")
    print(" - eval/retrieval_results.csv")
    print(" - eval/retrieval_summary.json")
    print(" - eval/query_vectors.json (cache; prevents re-embedding on repeated runs)")
    print("\nNOTE: exact source/page hit does not guarantee that the retrieved passage supports the answer.")



# ---------------------------------------------------------------------------
# End-to-end evaluation: append to the existing retrieval benchmark.
# ---------------------------------------------------------------------------
import argparse
from datetime import datetime, timezone

AGENT_RUNS_PATH = EVAL_DIR / "agent_runs.jsonl"
AGENT_RESULTS_PATH = EVAL_DIR / "agent_results.csv"
JUDGE_RUNS_PATH = EVAL_DIR / "judge_runs.jsonl"
JUDGE_RESULTS_PATH = EVAL_DIR / "judge_results.csv"
HUMAN_PATH = EVAL_DIR / "human_labels.csv"
E2E_SUMMARY_PATH = EVAL_DIR / "end_to_end_summary.json"

# Handles both [book.pdf, page 7] and [book.pdf, page 7, 9].
CITE_PATTERN = re.compile(r"([\w.\-]+\.pdf),\s*pages?\s*(\d+(?:\s*,\s*\d+)*)", re.I)
REFUSAL_TERMS = (
    "i don't know", "i do not know", "cannot determine", "can't determine",
    "cannot predict", "can't predict", "cannot tell", "can't tell",
    "not enough information", "not covered by", "do not have access",
    "don't have access", "does not specify", "cannot verify",
    "unable to determine", "unable to predict", "insufficient information",
)


def parse_citations(answer):
    """Expand multi-page citations, e.g. 'guide.pdf, page 8, 13'."""
    citations = set()
    for source, pages in CITE_PATTERN.findall(answer or ""):
        for page in re.findall(r"\d+", pages):
            citations.add((source, f"page {int(page)}"))
    return citations


def evidence_from_trace(trace):
    """Collect the actual MCP passages the agent received as evidence."""
    passages = []
    seen = set()
    for event in trace or []:
        if event.get("tool") != "search":
            continue
        try:
            response = json.loads(event.get("output") or "{}")
        except (ValueError, TypeError):
            continue
        for item in response.get("passages", []):
            key = (item.get("source"), item.get("location"), item.get("text"))
            if key not in seen and item.get("text"):
                seen.add(key)
                passages.append({
                    "source": item.get("source", ""),
                    "location": item.get("location", ""),
                    "text": item.get("text", ""),
                })
    return passages


def read_jsonl(path):
    if not path.exists():
        return {}
    records = {}
    with path.open(encoding="utf-8") as file:
        for line in file:
            if not line.strip():
                continue
            try:
                record = json.loads(line)
            except json.JSONDecodeError:
                print(f"Ignoring incomplete record in {path.name}")
                continue
            records[record["id"]] = record
    return records


def append_jsonl(path, record):
    path.parent.mkdir(exist_ok=True)
    with path.open("a", encoding="utf-8") as file:
        file.write(json.dumps(record, ensure_ascii=False) + "\n")
        file.flush()


def is_transient_error(error):
    """Find 429/503 even when MCP/AnyIO wraps it in ExceptionGroup."""
    stack = [error]
    visited = set()
    while stack:
        current = stack.pop()
        if id(current) in visited:
            continue
        visited.add(id(current))
        content = str(current).lower()
        if any(word in content for word in (
            "429", "503", "resource_exhausted", "unavailable", "high demand",
            "rate limit", "quota exceeded for metric", "deadline_exceeded",
        )):
            return True
        if isinstance(current, BaseExceptionGroup):
            stack.extend(current.exceptions)
        if current.__cause__ is not None:
            stack.append(current.__cause__)
        if current.__context__ is not None:
            stack.append(current.__context__)
    return False


def make_run_key(row, model):
    from agent import SYSTEM_PROMPT
    payload = {
        "question": row["question"],
        "model": model,
        "instructions": SYSTEM_PROMPT.read_text(encoding="utf-8"),
    }
    return hashlib.sha256(json.dumps(payload, sort_keys=True).encode()).hexdigest()


def run_agent_questions(questions, limit=None, refresh=None):
    """Run questions, keeping responses and tool traces across interruptions."""
    from agent import MODEL, ask

    previous = read_jsonl(AGENT_RUNS_PATH)
    refresh = set(refresh or [])
    target = questions[:limit] if limit else questions
    for position, row in enumerate(target, start=1):
        qid = row["id"]
        key = make_run_key(row, MODEL)
        old = previous.get(qid)
        if old and old.get("cache_key") == key and qid not in refresh:
            print(f"[{position}/{len(target)}] {qid}: cached")
            continue
        print(f"[{position}/{len(target)}] {qid}: asking {MODEL}...", flush=True)
        for attempt in range(4):
            try:
                response = ask(row["question"])
                break
            except Exception as exc:
                if attempt == 3 or not is_transient_error(exc):
                    raise RuntimeError(f"Failed on {qid}. Completed answers are saved.") from exc
                duration = 12 * (2 ** attempt)
                print(f"  Transient model/API error for {qid}; retrying after {duration}s.", flush=True)
                time.sleep(duration)
        passages = evidence_from_trace(response.get("tool_trace", []))
        record = {
            "id": qid,
            "cache_key": key,
            "model": MODEL,
            "question": row["question"],
            "kind": row["kind"],
            "answer": response.get("answer", ""),
            "passages": passages,
            "tool_trace": response.get("tool_trace", []),
            "input_tokens": response.get("input_tokens", 0),
            "output_tokens": response.get("output_tokens", 0),
            "seconds": response.get("seconds", 0),
            "created_at": datetime.now(timezone.utc).isoformat(),
        }
        append_jsonl(AGENT_RUNS_PATH, record)
        previous[qid] = record
        print(f"  Saved answer ({record['seconds']}s, {len(passages)} passages)", flush=True)
    return previous


def build_agent_results(questions):
    runs = read_jsonl(AGENT_RUNS_PATH)
    output = []
    for row in questions:
        run = runs.get(row["id"])
        if run is None:
            continue
        answer = run.get("answer", "")
        citations = parse_citations(answer)
        passages = run.get("passages", [])
        evidence = {(p["source"], p["location"]) for p in passages}
        absent = sorted(citations - evidence)
        no_claim_refusal = any(marker in answer.lower() for marker in REFUSAL_TERMS)
        output.append({
            "id": row["id"], "kind": row["kind"], "question": row["question"],
            "answer": answer,
            "searched": int(any(e.get("tool") == "search" for e in run.get("tool_trace", []))),
            "refusal_detected": int(no_claim_refusal),
            "citations_found": len(citations),
            "all_citations_in_retrieved_evidence": int(not absent),
            "missing_citations": "; ".join(f"{s}, {p}" for s, p in absent),
            "input_tokens": run.get("input_tokens", 0),
            "output_tokens": run.get("output_tokens", 0),
            "seconds": run.get("seconds", 0),
        })
    if output:
        with AGENT_RESULTS_PATH.open("w", encoding="utf-8", newline="") as f:
            writer = csv.DictWriter(f, fieldnames=list(output[0]))
            writer.writeheader()
            writer.writerows(output)
    return output


def model_text(message):
    content = getattr(message, "content", "")
    if isinstance(content, str):
        return content
    if isinstance(content, list):
        return "\n".join(
            part.get("text", "") if isinstance(part, dict) else str(part)
            for part in content
        )
    return str(content)


def judge_one(row, run, model):
    """Judge solely from reference answer and passages actually retrieved."""
    from langchain_google_genai import ChatGoogleGenerativeAI
    from api_key import load_api_key

    judge = ChatGoogleGenerativeAI(model=model, api_key=load_api_key(), max_retries=4)
    passages = run.get("passages", [])
    evidence_block = "\n\n".join(
        f"[{p['source']}, {p['location']}]\n{p['text']}"
        for p in passages[:12]
    )[:24000]
    prompt = f"""You are grading a financial-education RAG assistant. Use ONLY the evidence and
reference answer provided below, not your outside knowledge. Score fairly.

QUESTION TYPE: {row['kind']}
QUESTION: {row['question']}
REFERENCE ANSWER: {row['reference_answer']}
ASSISTANT ANSWER: {run['answer']}
RETRIEVED EVIDENCE (empty means no supporting passages):
{evidence_block or '[NO EVIDENCE]'}

Rubric:
correct=1 iff the substantive answer matches the reference; for unanswerable
questions, correctly declining to invent the requested specific answer counts
as correct even if useful general context is given.
supported=1 iff every factual claim in the assistant answer is justified by
retrieved evidence (a refusal to invent an answer is not an unsupported fact).
If the answer makes a specific claim not supported by these passages, supported=0.
Do not treat the mere presence of a formatted citation as proof of support.
Return ONLY a JSON object with exactly: correct (0 or 1), supported (0 or 1),
notes (a brief explanation; state which claims are unsupported if any).
"""
    result = judge.invoke(prompt)
    raw = model_text(result).strip()
    try:
        return json.loads(raw)
    except json.JSONDecodeError:
        match = re.search(r"\{[\s\S]*\}", raw)
        if match:
            return json.loads(match.group(0))
        raise ValueError(f"Judge did not return JSON: {raw[:300]}")



def judge_cache_key(row, run, model):
    """Same cache key as the original one-answer judge; old verdicts still count."""
    return hashlib.sha256(json.dumps({
        "answer": run["answer"], "reference": row["reference_answer"],
        "passages": run["passages"], "judge_model": model,
    }, sort_keys=True).encode()).hexdigest()


def concise_judge_evidence(run, char_budget=5200, per_passage=1600):
    """Prioritize retrieved passages cited in the answer to save input tokens.

    Excerpts are a cost/coverage trade-off. The final report must disclose
    that the judge sees excerpts, not necessarily every retrieved character.
    """
    passages = list(run.get("passages", []))
    cited = parse_citations(run.get("answer", ""))
    passages.sort(key=lambda p: (
        (p.get("source", ""), p.get("location", "")) not in cited,
        p.get("source", ""), p.get("location", ""),
    ))
    excerpts = []
    remaining = char_budget
    for p in passages:
        heading = f"[{p.get('source', '?')}, {p.get('location', '?')}] "
        allowance = min(per_passage, remaining - len(heading))
        if allowance < 100:
            break
        excerpt = heading + str(p.get("text", ""))[:allowance]
        excerpts.append(excerpt)
        remaining -= len(excerpt)
    return excerpts


def judge_batch(entries, model):
    """One model request scores an entire batch using saved answers/evidence."""
    from langchain_google_genai import ChatGoogleGenerativeAI
    from api_key import load_api_key

    cases = [{
        "id": row["id"], "type": row["kind"], "question": row["question"],
        "reference_answer": row["reference_answer"],
        "assistant_answer": run["answer"],
        "retrieved_evidence_excerpts": concise_judge_evidence(run),
    } for row, run in entries]
    prompt = (
        "You are an independent RAG evaluator. Score EACH case separately. "
        "Use ONLY its reference answer and retrieved evidence excerpts, not outside "
        "knowledge or human grades. For unanswerable cases, a refusal to invent "
        "unavailable personal or corpus information is correct=1. "
        "correct=1 only when the substantive answer matches the reference. "
        "supported=1 only if ALL substantive factual claims are justified by "
        "retrieved evidence; a citation alone is not proof. An honest refusal "
        "does not require a citation. If excerpts omit needed context, flag "
        "uncertainty in notes instead of assuming the citation proves support. "
        "Return ONLY a JSON array with one object per case: "
        '{"id":"q01","correct":1,"supported":1,"notes":"brief reason"}. '
        "Keep notes under 18 words. No markdown.\nCASES: "
        + json.dumps(cases, ensure_ascii=False, separators=(",", ":"))
    )
    # Disable SDK-level retries: a daily-limit 429 cannot be fixed by waiting seconds.
    judge = ChatGoogleGenerativeAI(
        model=model,
        api_key=load_api_key(),
        max_retries=0,
        max_output_tokens=4096,
        thinking_level="low",
        response_mime_type="application/json",
    )
    response = judge.invoke(prompt)
    raw = model_text(response).strip()
    raw = re.sub(r"^```(?:json)?\s*", "", raw, flags=re.I)
    raw = re.sub(r"\s*```$", "", raw)
    try:
        verdicts = json.loads(raw)
    except json.JSONDecodeError:
        match = re.search(r"\[[\s\S]*\]", raw)
        if not match:
            raise ValueError(f"Judge returned invalid JSON: {raw[:400]}")
        verdicts = json.loads(match.group(0))
    expected = {row["id"] for row, _ in entries}
    if (not isinstance(verdicts, list) or len(verdicts) != len(entries)
            or not all(isinstance(v, dict) for v in verdicts)
            or {v.get("id") for v in verdicts} != expected):
        raise ValueError(f"Judge response IDs do not match batch: expected {sorted(expected)}")
    for v in verdicts:
        if str(v.get("correct")) not in ("0", "1") or str(v.get("supported")) not in ("0", "1"):
            raise ValueError(f"Invalid judge grade: {v}")
    usage = getattr(response, "usage_metadata", None) or {}
    if usage:
        print(f"  Judge tokens: input={usage.get('input_tokens', '?')}, "
              f"output={usage.get('output_tokens', '?')}", flush=True)
    return verdicts


def save_judge_csv(questions):
    previous = read_jsonl(JUDGE_RUNS_PATH)
    rows = [
        {field: previous[row["id"]][field] for field in ("id", "correct", "supported", "notes")}
        for row in questions if row["id"] in previous
    ]
    if rows:
        with JUDGE_RESULTS_PATH.open("w", encoding="utf-8", newline="") as file:
            writer = csv.DictWriter(file, fieldnames=("id", "correct", "supported", "notes"))
            writer.writeheader()
            writer.writerows(rows)
    return rows


def run_judge(questions, limit=None, refresh=None, batch_size=5, max_batches=None):
    """Judge cached answers in batches; never regenerate agent answers here."""
    from agent import MODEL
    from os import environ

    if not 1 <= batch_size <= 5:
        raise ValueError("batch_size must be between 1 and 5")
    # Optional separate model for judging, only if available to your API key.
    judge_model = environ.get("RAG_JUDGE_MODEL", MODEL)
    target = questions[:limit] if limit else questions
    refresh = set(refresh or [])

    # Require real, already-recorded human judgments to avoid leakage.
    valid_human = set()
    if HUMAN_PATH.exists():
        with HUMAN_PATH.open(encoding="utf-8-sig", newline="") as f:
            valid_human = {
                row["id"] for row in csv.DictReader(f)
                if row.get("id") and row.get("correct") in ("0", "1")
                and row.get("supported") in ("0", "1")
            }
    if len(valid_human) < 20:
        raise RuntimeError(f"Need 20+ independent grades in eval/human_labels.csv; found {len(valid_human)}")

    runs = read_jsonl(AGENT_RUNS_PATH)
    previous = read_jsonl(JUDGE_RUNS_PATH)
    todo = []
    cached_count = 0
    missing_count = 0
    for row in target:
        qid = row["id"]
        run = runs.get(qid)
        if run is None:
            print(f"{qid}: no cached agent answer; skipping (no API call)")
            missing_count += 1
            continue
        key = judge_cache_key(row, run, judge_model)
        old = previous.get(qid)
        if old and old.get("cache_key") == key and qid not in refresh:
            cached_count += 1
            continue
        todo.append((row, run, key))

    print(f"Judge model: {judge_model}; cached={cached_count}; "
          f"missing answers={missing_count}; to judge={len(todo)}; "
          f"batch size={batch_size}.", flush=True)
    batches = [todo[i:i + batch_size] for i in range(0, len(todo), batch_size)]
    if max_batches is not None:
        batches = batches[:max_batches]
    try:
        for number, batch in enumerate(batches, 1):
            ids = ", ".join(row["id"] for row, _, _ in batch)
            print(f"Batch {number}/{len(batches)}: {ids}", flush=True)
            try:
                verdicts = judge_batch([(row, run) for row, run, _ in batch], judge_model)
            except Exception as exc:
                print(f"Judge stopped without retrying. Saved grades are safe. Error: {exc}", flush=True)
                break
            by_id = {v["id"]: v for v in verdicts}
            for row, _run, key in batch:
                verdict = by_id[row["id"]]
                record = {
                    "id": row["id"], "cache_key": key,
                    "correct": int(verdict["correct"]),
                    "supported": int(verdict["supported"]),
                    "notes": str(verdict.get("notes", "")),
                }
                append_jsonl(JUDGE_RUNS_PATH, record)
                previous[row["id"]] = record
            print(f"  Saved {len(batch)} grades.", flush=True)
            if number < len(batches):
                time.sleep(10)  # Avoid back-to-back rate spikes.
    finally:
        rows = save_judge_csv(questions)
        print(f"Saved {len(rows)} judge grades in eval/judge_results.csv.", flush=True)
    return rows


def end_to_end_summary(questions):
    results = build_agent_results(questions)
    graders = read_jsonl(JUDGE_RUNS_PATH)
    human = {}
    if HUMAN_PATH.exists():
        with HUMAN_PATH.open(encoding="utf-8-sig", newline="") as f:
            human = {r["id"]: r for r in csv.DictReader(f) if r.get("id")}
    graded = [r for r in results if r["id"] in graders]
    compared = [r for r in graded if r["id"] in human and human[r["id"]].get("correct") in ("0", "1") and human[r["id"]].get("supported") in ("0", "1")]
    def avg(rows, field):
        return round(sum(float(row[field]) for row in rows) / len(rows), 4) if rows else None
    report = {
        "total_questions": len(questions),
        "answers_completed": len(results),
        "judge_grades_completed": len(graded),
        "human_grades_completed": sum(1 for r in human.values() if r.get("correct") in ("0", "1") and r.get("supported") in ("0", "1")),
        "citation_grounding_rate": avg([r for r in results if r["citations_found"]], "all_citations_in_retrieved_evidence"),
        "average_input_tokens": avg(results, "input_tokens"),
        "average_output_tokens": avg(results, "output_tokens"),
        "average_seconds": avg(results, "seconds"),
        "judge_correct_rate": round(sum(graders[r["id"]]["correct"] for r in graded) / len(graded), 4) if graded else None,
        "judge_supported_rate": round(sum(graders[r["id"]]["supported"] for r in graded) / len(graded), 4) if graded else None,
        "human_judge_compared": len(compared),
        "agreement_correct": round(sum(int(human[r["id"]]["correct"]) == graders[r["id"]]["correct"] for r in compared) / len(compared), 4) if compared else None,
        "agreement_supported": round(sum(int(human[r["id"]]["supported"]) == graders[r["id"]]["supported"] for r in compared) / len(compared), 4) if compared else None,
        "notes": [
            "Code checks only that citations refer to retrieved pages; actual claim support is a judgment task.",
            "Refusal detection is a rough phrase-based heuristic, not a complete semantic assessment.",
            "Human grading must be done independently before looking at LLM-judge results.",
            "Token costs depend on published prices for the actual model and billing plan; not inferred here.",
        ],
    }
    E2E_SUMMARY_PATH.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print("\nEnd-to-end summary:")
    for field, value in report.items():
        if field != "notes":
            print(f"  {field}: {value}")
    print("Saved eval/agent_results.csv, eval/end_to_end_summary.json")
    return report


def cli():
    parser = argparse.ArgumentParser(description="MoneyGuide retrieval and end-to-end evaluation")
    parser.add_argument("--answers-only", action="store_true", help="Collect answers but do not run the LLM judge; grade independently first")
    parser.add_argument("--judge-only", action="store_true", help="Judge saved answers without calling the agent")
    parser.add_argument("--limit", type=int, default=None, help="Pilot the first N questions and cache results")
    parser.add_argument("--refresh", action="append", default=[], help="Re-run a particular question ID, e.g., --refresh q30")
    parser.add_argument("--batch-size", type=int, default=5, help="Answers graded per judge request (1-5; default 5)")
    parser.add_argument("--max-batches", type=int, default=None, help="Only run this many judge batches (1 = one-call pilot)")
    args = parser.parse_args()
    questions = load_questions()
    if not args.judge_only:
        run()  # Original semantic vs hybrid benchmark; reuses cached query embeddings.
        run_agent_questions(questions, limit=args.limit, refresh=args.refresh)
        build_agent_results(questions)
        if args.answers_only:
            print("\nAnswers are in eval/agent_results.csv and detailed evidence is in eval/agent_runs.jsonl.")
            print("Grade 20+ answers yourself in eval/human_labels.csv BEFORE inspecting the LLM judge's verdicts.")
    if not args.answers_only:
        run_judge(questions, limit=args.limit, refresh=args.refresh,
                  batch_size=args.batch_size, max_batches=args.max_batches)
    end_to_end_summary(questions)


if __name__ == "__main__":
    cli()
