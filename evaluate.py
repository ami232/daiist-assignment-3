"""
Assignment 3: evaluation (`main.py evaluate`).

Part 1, retrieval: hit rate at 1/3/5 for each chunking design (a = structure, b = fixed),
plus the top similarity score of answerable vs unanswerable questions.
Later parts (agent run, code checks, LLM judge, agreement with human labels) are added below.

Results go to eval/.
"""

import csv
import json
import statistics
import sys
from pathlib import Path

import index

ROOT = Path(__file__).resolve().parent
EVAL = ROOT / "eval"
QUESTIONS = EVAL / "questions.csv"
KS = (1, 3, 5)


def load_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def split(cell: str) -> list[str]:
    return [x.strip() for x in cell.split(";") if x.strip()]


def matches(chunk: dict, sources: list[str], locations: list[str]) -> set[str]:
    """The expected locations this chunk covers (empty set = not a hit).
    A chunk covers a location when it comes from one of the expected documents and
    that label is among the sections the chunk contains (metadata 'locations')."""
    meta = chunk["metadata"]
    if meta["doc_id"] not in sources:
        return set()
    return set(meta["locations"].split("; ")) & set(locations)


def retrieval_eval(questions: list[dict]) -> tuple[list[dict], dict]:
    rows, summary = [], {}
    answerable = [q for q in questions if q["kind"].strip().lower() != "unanswerable"]
    for design in index.DESIGNS:
        hits = {k: [] for k in KS}  # any expected location in top k
        full = {k: [] for k in KS}  # every expected location in top k (differs only for multi)
        labels_per_hit = []
        top_answerable, top_unanswerable = [], []
        for q in questions:
            results = index.search(q["question"], design, k=max(KS))
            if q["kind"].strip().lower() == "unanswerable":
                top_unanswerable.append(results[0]["score"])
                rows.append({"design": design, "id": q["id"], "kind": q["kind"], "first_hit_rank": "",
                             "top_score": results[0]["score"],
                             "top_location": f'{results[0]["metadata"]["doc_id"]} | {results[0]["metadata"]["location"]}'})
                continue
            top_answerable.append(results[0]["score"])
            sources, locations = split(q["expected_source"]), split(q["expected_location"])
            covered_by_rank = [matches(r, sources, locations) for r in results]
            first = next((i + 1 for i, c in enumerate(covered_by_rank) if c), None)
            for k in KS:
                covered = set().union(*covered_by_rank[:k])
                hits[k].append(bool(covered))
                full[k].append(covered == set(locations))
            if first:
                labels_per_hit.append(len(results[first - 1]["metadata"]["locations"].split("; ")))
            rows.append({"design": design, "id": q["id"], "kind": q["kind"], "first_hit_rank": first or "miss",
                         "top_score": results[0]["score"],
                         "top_location": f'{results[0]["metadata"]["doc_id"]} | {results[0]["metadata"]["location"]}'})
        summary[design] = {
            "name": index.DESIGNS[design],
            **{f"hit@{k}": round(sum(hits[k]) / len(answerable), 3) for k in KS},
            **{f"all_locations@{k}": round(sum(full[k]) / len(answerable), 3) for k in KS},
            "sections_per_hit_chunk": round(statistics.mean(labels_per_hit), 2) if labels_per_hit else None,
            "top_score_answerable_median": round(statistics.median(top_answerable), 3),
            "top_score_unanswerable_median": round(statistics.median(top_unanswerable), 3),
            "top_score_unanswerable_max": round(max(top_unanswerable), 3),
            "top_score_answerable_min": round(min(top_answerable), 3),
        }
    return rows, summary


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)


def main() -> int:
    questions = load_questions()
    try:
        rows, summary = retrieval_eval(questions)
    except index.QuotaExhausted as e:
        print(f"Embedding quota exhausted: {e}", file=sys.stderr)
        return 1
    write_csv(EVAL / "retrieval_results.csv", rows)
    (EVAL / "retrieval_summary.json").write_text(json.dumps(summary, indent=2))
    print("Retrieval (answerable questions):")
    print(json.dumps(summary, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
