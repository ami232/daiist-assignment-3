"""Compare the retrieval designs: hit rate @1, @3 and @5 on eval/questions.csv.

    uv run python retrieval_eval.py

Only retrieval is measured here (no LLM): for each answerable question, do the top-k chunks
contain the passage we expected? Unanswerable questions have no expected passage, so they are
left out (they are tested end to end later, in evaluate.py).

Hit rule (decide it, defend it):
  * single question  -> a top-k chunk has the expected source AND the expected location
  * multi question   -> ALL expected (source, location) pairs are in the top-k chunks
Costs: one embedding per question (cached in index/query_cache.json, shared by both designs).
"""
from __future__ import annotations

import csv
import sys
from pathlib import Path

from index import DESIGNS
from retrieval import retrieve

ROOT = Path(__file__).resolve().parent
QUESTIONS = ROOT / "eval" / "questions.csv"
OUT = ROOT / "eval" / "retrieval_results.csv"
KS = (1, 3, 5)


def norm(text: str) -> str:
    return " ".join(text.lower().split())


def load_questions() -> list[dict]:
    with QUESTIONS.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))
    for row in rows:
        sources = [s.strip() for s in row["expected_source"].split(";") if s.strip()]
        locations = [l.strip() for l in row["expected_location"].split(";") if l.strip()]
        if len(sources) != len(locations):
            sys.exit(f"{row['id']}: {len(sources)} sources but {len(locations)} locations "
                     "(separate both with ';', same order)")
        row["expected"] = list(zip(sources, [norm(l) for l in locations]))
    return rows


def first_rank(hits: list[dict], source: str, location: str) -> int | None:
    """1-based position of the first chunk matching (source, location), or None."""
    for rank, hit in enumerate(hits, 1):
        if hit["source"] == source and norm(hit["location"]) == location:
            return rank
    return None


def main() -> None:
    questions = [q for q in load_questions() if q["expected"]]
    print(f"{len(questions)} answerable questions "
          f"({sum(len(q['expected']) > 1 for q in questions)} need two passages)\n")
    results = []  # one row per (design, question)
    summary = {}
    for design in DESIGNS:
        hit_counts = {k: 0 for k in KS}
        for q in questions:
            hits = retrieve(q["question"], k=max(KS), design=design)
            ranks = [first_rank(hits, s, l) for s, l in q["expected"]]
            # worst rank among the expected passages (None = at least one is missing from the top 5)
            worst = None if any(r is None for r in ranks) else max(ranks)
            for k in KS:
                if worst is not None and worst <= k:
                    hit_counts[k] += 1
            results.append({"design": design, "id": q["id"], "kind": q["kind"], "worst_rank": worst or "",
                            "top1": f"{hits[0]['source']} | {hits[0]['location']}" if hits else ""})
        summary[design] = {k: hit_counts[k] / len(questions) for k in KS}

    print(f"{'design':<12}" + "".join(f"{'hit@' + str(k):>9}" for k in KS))
    print("-" * (12 + 9 * len(KS)))
    for design, rates in summary.items():
        print(f"{design:<12}" + "".join(f"{rates[k]:>9.2f}" for k in KS))

    OUT.parent.mkdir(exist_ok=True)
    with OUT.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.DictWriter(handle, fieldnames=["design", "id", "kind", "worst_rank", "top1"])
        writer.writeheader()
        writer.writerows(results)

    print("\nMisses at @5 (look at these one by one for your failure analysis):")
    for design in DESIGNS:
        missed = [r["id"] for r in results if r["design"] == design and r["worst_rank"] == ""]
        print(f"  {design}: {', '.join(missed) if missed else 'none'}")
    print(f"\nPer-question detail saved in {OUT.relative_to(ROOT)}")
    print("Now set ACTIVE_DESIGN in index.py to the design you choose, and justify it with these numbers.")


if __name__ == "__main__":
    main()