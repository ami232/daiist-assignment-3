"""
Assignment 3: evaluation (`main.py evaluate`).

Part 1 - retrieval: hit rate at k = 1, 3, 5 for each chunking design on the
answerable questions in eval/questions.csv, plus how many words the top-k
chunks would add to the prompt. Results go to eval/retrieval_*.

(Part 2, the agent evaluation, is added later.)

A retrieved chunk is a hit when it comes from the expected document and
- for a PDF: the expected page is inside the chunk's page range;
- for a web page: the expected section title is part of the chunk's section.
Multi questions have two expected passages: we report whether at least one
was found ("any") and whether both were found ("all").
"""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

import index

ROOT = Path(__file__).resolve().parent
EVAL_DIR = ROOT / "eval"
QUESTIONS = EVAL_DIR / "questions.csv"
QUERY_CACHE = EVAL_DIR / "query_embeddings.json"
KS = (1, 3, 5)


def log(message: str = "") -> None:
    print(message, flush=True)


def load_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r["question"].strip()]


def is_spanish(question: str) -> bool:
    return bool(re.search(r"[¿¡ñáéíóú]", question.lower()))


def expected_passages(row: dict) -> list[tuple[str, str]]:
    """(source, location) pairs. One source with several locations means the
    same document for each; otherwise sources and locations pair up in order."""
    sources = [s.strip() for s in row["expected_source"].split(";") if s.strip()]
    locations = [l.strip() for l in row["expected_location"].split(";") if l.strip()]
    if len(sources) == 1:
        return [(sources[0], loc) for loc in locations] or [(sources[0], "")]
    return list(zip(sources, locations))


def matches(metadata: dict, source: str, location: str) -> bool:
    if metadata["source"] != source:
        return False
    if not location:
        return True
    if location.isdigit():
        return metadata["page"] <= int(location) <= metadata["page_end"]
    return location.lower() in metadata["section"].lower()


# --------------------------------------------------------------------------- query embeddings (cached)

def query_vectors(questions: list[str]) -> dict[str, list[float]]:
    """Embed each question once and keep the vectors in eval/, so re-running
    the evaluation or adding a design costs no extra quota."""
    cache = json.loads(QUERY_CACHE.read_text(encoding="utf-8")) if QUERY_CACHE.is_file() else {}
    key = f"{index.EMBED_MODEL}/{index.EMBED_DIM}"
    cache.setdefault(key, {})
    missing = [q for q in questions if q not in cache[key]]
    for start in range(0, len(missing), index.EMBED_BATCH):
        batch = missing[start:start + index.EMBED_BATCH]
        for q, v in zip(batch, index.embed(batch, "RETRIEVAL_QUERY")):
            cache[key][q] = v
        QUERY_CACHE.write_text(json.dumps(cache), encoding="utf-8")
    if missing:
        log(f"Embedded {len(missing)} new questions (cached in {QUERY_CACHE.relative_to(ROOT)}).")
    return cache[key]


# --------------------------------------------------------------------------- retrieval evaluation

def evaluate_retrieval(designs=index.DESIGNS) -> dict:
    rows = [r for r in load_questions() if r["kind"].strip().lower() != "unanswerable"]
    vectors = query_vectors([r["question"] for r in rows])
    kmax = max(KS)

    per_question, summary = [], {}
    for design in designs:
        col = index.collection(design)
        stats = {"n": len(rows), "hit": {k: 0 for k in KS}, "words": {k: 0 for k in KS},
                 "multi_n": 0, "multi_all": {k: 0 for k in KS},
                 "es_n": 0, "es_hit": {k: 0 for k in KS}, "mrr": 0.0}
        for r in rows:
            result = col.query(query_embeddings=[vectors[r["question"]]], n_results=kmax,
                               include=["metadatas"])
            metas = result["metadatas"][0]
            passages = expected_passages(r)
            # Rank (1-based) at which each expected passage first appears.
            ranks = [next((i + 1 for i, m in enumerate(metas) if matches(m, s, l)), None) for s, l in passages]
            first = min((x for x in ranks if x), default=None)
            spanish = is_spanish(r["question"])
            for k in KS:
                hit = first is not None and first <= k
                stats["hit"][k] += hit
                stats["words"][k] += sum(m["words"] for m in metas[:k])
                if r["kind"] == "multi":
                    stats["multi_all"][k] += all(x is not None and x <= k for x in ranks)
                if spanish:
                    stats["es_hit"][k] += hit
            stats["mrr"] += 1 / first if first else 0
            stats["multi_n"] += r["kind"] == "multi"
            stats["es_n"] += spanish
            per_question.append({
                "design": design, "id": r["id"], "kind": r["kind"], "spanish": int(spanish),
                "first_hit_rank": first or "", "ranks_per_passage": ";".join(str(x or "-") for x in ranks),
                "top5": " | ".join(f"{m['source']} {m['location'][:50]}" for m in metas),
            })

        n = stats["n"]
        summary[design] = {
            "questions": n,
            **{f"hit@{k}": round(stats["hit"][k] / n, 3) for k in KS},
            "mrr": round(stats["mrr"] / n, 3),
            **{f"multi_all@{k}": round(stats["multi_all"][k] / stats["multi_n"], 3) for k in KS if stats["multi_n"]},
            **{f"spanish_hit@{k}": round(stats["es_hit"][k] / stats["es_n"], 3) for k in KS if stats["es_n"]},
            **{f"words@{k}": round(stats["words"][k] / n) for k in KS},
        }

    with (EVAL_DIR / "retrieval_per_question.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(per_question[0]))
        w.writeheader(); w.writerows(per_question)
    (EVAL_DIR / "retrieval_summary.json").write_text(json.dumps(summary, indent=2), encoding="utf-8")
    return summary


def print_retrieval(summary: dict) -> None:
    designs = list(summary)
    first = summary[designs[0]]
    log(f"\nRetrieval on {first['questions']} answerable questions\n")
    log(f"{'metric':<18}" + "".join(f"{d:>12}" for d in designs))
    for metric in first:
        if metric == "questions":
            continue
        log(f"{metric:<18}" + "".join(f"{summary[d].get(metric, ''):>12}" for d in designs))
    log("\nhit@k: an expected passage is in the top k.  multi_all@k: both passages of a multi question are.")
    log("words@k: words the top-k chunks add to the prompt (mean).  Details: eval/retrieval_per_question.csv")


def main() -> None:
    summary = evaluate_retrieval()
    print_retrieval(summary)


if __name__ == "__main__":
    try:
        main()
    except index.DailyQuotaExhausted:
        log("Daily embedding quota reached; cached question vectors are kept. Run again after 09:00 (Spain).")
        sys.exit(2)
