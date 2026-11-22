"""
Assignment 3: evaluation (`main.py evaluate`).

Stage 1, retrieval (this file so far): for every test question and both
chunking designs, does the right passage reach the top k?

    hit@k (single)          a top-k chunk is from the expected page AND
                            contains the expected section
    hit@k (multi, strict)   every expected passage is in the top k
    hit@k (multi, partial)  at least one expected passage is in the top k
    words@k                 words the top k chunks would add to the prompt

Unanswerable questions have no right passage, so they are left out of hit
rate. Instead we compare their best similarity score with the answerable
questions' scores: if they are clearly lower, a score threshold could help
the agent refuse.

Question vectors are cached in index/query_vectors.json, so after the first
run this stage costs no API calls.

Outputs in eval/: retrieval_results.csv (one row per question and design)
and retrieval_summary.json.
"""

import csv
import json
import statistics
from pathlib import Path

import index as ix

ROOT = Path(__file__).resolve().parent
EVAL_DIR = ROOT / "eval"
QUESTIONS = EVAL_DIR / "questions.csv"
RETRIEVAL_RESULTS = EVAL_DIR / "retrieval_results.csv"
RETRIEVAL_SUMMARY = EVAL_DIR / "retrieval_summary.json"

KS = (1, 3, 5)
TOP = max(KS)


def load_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r["question"].strip()]
    for r in rows:
        r["kind"] = r["kind"].strip().lower()
        sources = [s.strip() for s in r["expected_source"].split(";") if s.strip()]
        locations = [l.strip() for l in r["expected_location"].split(";") if l.strip()]
        if len(sources) != len(locations):
            raise ValueError(f"{r['id']}: expected_source and expected_location must pair up")
        r["expected"] = list(zip(sources, locations))
    return rows


# ============================================================================
# Matching a retrieved chunk against an expected passage
# ============================================================================

def contains_passage(chunk: dict, source: str, location: str) -> bool:
    """True if the chunk is from `source` and covers the section `location`.

    A chunk's `sections` field lists every heading path inside it. It covers
    the expected section if one of those paths is the section itself or one
    of its sub-sections (expected "Types of leave › Annual leave" is covered
    by a chunk holding "Types of leave › Annual leave › Use or Lose").
    """
    if chunk["source"] != source:
        return False
    for section in chunk["sections"].split(" | "):
        if section == location or section.startswith(location + ix.SEPARATOR):
            return True
    return False


def first_rank(results: list[dict], source: str, location: str) -> int | None:
    """1-based rank of the first chunk containing this passage, or None."""
    for rank, chunk in enumerate(results, start=1):
        if contains_passage(chunk, source, location):
            return rank
    return None


# ============================================================================
# Stage 1: retrieval
# ============================================================================

def retrieval_stage(questions: list[dict]) -> dict:
    rows = []
    for q in questions:
        vector = ix.embed_query(q["question"])  # one embedding per question, cached on disk
        for design in ix.DESIGNS:
            results = ix.retrieve(vector, k=TOP, design=design)
            ranks = [first_rank(results, s, l) for s, l in q["expected"]]
            found = [r for r in ranks if r is not None]
            row = {
                "id": q["id"],
                "kind": q["kind"],
                "design": design,
                # rank where the FIRST expected passage appears (partial hit)
                "rank_any": min(found) if found else "",
                # rank where ALL expected passages have appeared (strict hit)
                "rank_all": max(ranks) if ranks and None not in ranks else "",
                "top_score": results[0]["score"],
                "top1": f"{results[0]['source']} › {results[0]['location']}",
            }
            for k in KS:
                row[f"words@{k}"] = sum(c["words"] for c in results[:k])
            rows.append(row)

    with RETRIEVAL_RESULTS.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    summary = {d: summarise(rows, d) for d in ix.DESIGNS}
    RETRIEVAL_SUMMARY.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print_summary(summary, len(questions))
    return summary


def hit_rate(rows: list[dict], k: int, column: str) -> float:
    return sum(1 for r in rows if r[column] != "" and r[column] <= k) / len(rows) if rows else float("nan")


def summarise(rows: list[dict], design: str) -> dict:
    mine = [r for r in rows if r["design"] == design]
    answerable = [r for r in mine if r["kind"] != "unanswerable"]
    single = [r for r in mine if r["kind"] == "single"]
    multi = [r for r in mine if r["kind"] == "multi"]
    unanswerable = [r for r in mine if r["kind"] == "unanswerable"]

    def score_stats(group):
        scores = [r["top_score"] for r in group]
        return {"mean": round(statistics.mean(scores), 3), "min": min(scores), "max": max(scores)}

    return {
        "n_answerable": len(answerable),
        "hit": {
            f"@{k}": {
                "all_answerable": round(hit_rate(answerable, k, "rank_all"), 3),
                "single": round(hit_rate(single, k, "rank_all"), 3),
                "multi_strict": round(hit_rate(multi, k, "rank_all"), 3),
                "multi_partial": round(hit_rate(multi, k, "rank_any"), 3),
            }
            for k in KS
        },
        # mean reciprocal rank: 1 if the right chunk is first, 1/2 if second... 0 if not in top 5
        "mrr_single": round(statistics.mean(1 / r["rank_all"] if r["rank_all"] != "" else 0 for r in single), 3),
        "words_added": {f"@{k}": round(statistics.mean(r[f"words@{k}"] for r in mine)) for k in KS},
        "top_score_answerable": score_stats(answerable),
        "top_score_unanswerable": score_stats(unanswerable),
        "misses_at_5": [r["id"] for r in answerable if r["rank_all"] == ""],
    }


def print_summary(summary: dict, n: int) -> None:
    print("=" * 78)
    print(f"RETRIEVAL: {n} questions, {summary[ix.DESIGNS[0]]['n_answerable']} answerable")
    print("=" * 78)
    header = f"{'':<26}" + "".join(f"{d + ' @' + str(k):>13}" for d in ix.DESIGNS for k in KS)
    print(header)
    for label, key in [("hit rate, all answerable", "all_answerable"), ("  single", "single"),
                       ("  multi (both passages)", "multi_strict"), ("  multi (at least one)", "multi_partial")]:
        cells = "".join(f"{summary[d]['hit']['@' + str(k)][key]:>13.0%}" for d in ix.DESIGNS for k in KS)
        print(f"{label:<26}{cells}")
    cells = "".join(f"{summary[d]['words_added']['@' + str(k)]:>13}" for d in ix.DESIGNS for k in KS)
    print(f"{'words added to prompt':<26}{cells}")
    print("=" * 78)
    for d in ix.DESIGNS:
        s = summary[d]
        print(f"{d}: MRR (single) {s['mrr_single']:.3f}; best score answerable "
              f"{s['top_score_answerable']['mean']:.3f} (min {s['top_score_answerable']['min']:.3f}), "
              f"unanswerable {s['top_score_unanswerable']['mean']:.3f} "
              f"(max {s['top_score_unanswerable']['max']:.3f}); missed at 5: {', '.join(s['misses_at_5']) or 'none'}")


def main() -> None:
    questions = load_questions()
    retrieval_stage(questions)


if __name__ == "__main__":
    main()
