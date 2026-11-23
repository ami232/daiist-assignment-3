"""
Assignment 3: evaluation (`main.py evaluate`).

Part 1, retrieval: hit rate at k = 1, 3, 5 for each design in retrieval.py,
on every answerable question in eval/questions.csv. Writes
eval/retrieval_results.csv (one row per question and design) and
eval/retrieval_summary.csv.
"""

import csv
import re
import sys
from pathlib import Path

import retrieval

ROOT = Path(__file__).resolve().parent
EVAL_DIR = ROOT / "eval"
QUESTIONS = EVAL_DIR / "questions.csv"
KS = (1, 3, 5)


def load_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r["question"].strip()]


def expected_passages(row: dict) -> list[tuple[str, str, int]]:
    """[(source, 'Chapter XIII', 9), …] from expected_source / expected_location."""
    sources = [s.strip() for s in row["expected_source"].split(";")]
    locations = [loc.strip() for loc in row["expected_location"].split(";")]
    if len(sources) == 1:
        sources *= len(locations)
    passages = []
    for source, location in zip(sources, locations):
        match = re.fullmatch(r"(Chapter [IVXLC]+), ¶(\d+)", location)
        if not match:
            raise ValueError(f"{row['id']}: cannot read location {location!r}")
        passages.append((source, match.group(1), int(match.group(2))))
    return passages


def covers(hit: dict, passage: tuple[str, str, int]) -> bool:
    """Does this retrieved chunk contain the expected paragraph?"""
    source, chapter, paragraph = passage
    first, _, last = hit["paragraphs"].partition("-")
    return (hit["source"] == source
            and hit["chapter"].split(":")[0] == chapter
            and int(first) <= paragraph <= int(last or first))


def found_rank(hits: list[dict], passage) -> int | None:
    return next((rank for rank, hit in enumerate(hits, 1) if covers(hit, passage)), None)


def evaluate_retrieval(questions: list[dict]) -> list[dict]:
    searcher = retrieval.get_searcher()
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    results, summary = [], []
    for design in retrieval.DESIGNS:
        for q in answerable:
            hits = searcher.search(q["question"], k=max(KS), design=design)
            ranks = [found_rank(hits, p) for p in expected_passages(q)]
            results.append({
                "id": q["id"], "kind": q["kind"], "design": design,
                "ranks": ";".join(str(r) if r else "-" for r in ranks),
                **{f"all@{k}": int(all(r and r <= k for r in ranks)) for k in KS},
                **{f"any@{k}": int(any(r and r <= k for r in ranks)) for k in KS},
                "words@3": sum(len(h["text"].split()) for h in hits[:3]),
                "words@5": sum(len(h["text"].split()) for h in hits[:5]),
                "top_hit": f"{hits[0]['source']} | {hits[0]['location']}",
            })
        rows = [r for r in results if r["design"] == design]
        multi = [r for r in rows if r["kind"] == "multi"]
        summary.append({
            "design": design,
            **{f"hit@{k}": round(sum(r[f"all@{k}"] for r in rows) / len(rows), 3) for k in KS},
            **{f"multi_both@{k}": round(sum(r[f"all@{k}"] for r in multi) / len(multi), 3) for k in KS},
            **{f"multi_any@{k}": round(sum(r[f"any@{k}"] for r in multi) / len(multi), 3) for k in KS},
            "avg_words@3": round(sum(r["words@3"] for r in rows) / len(rows)),
            "avg_words@5": round(sum(r["words@5"] for r in rows) / len(rows)),
        })

    write_csv(EVAL_DIR / "retrieval_results.csv", results)
    write_csv(EVAL_DIR / "retrieval_summary.csv", summary)
    print(f"\nRetrieval on {len(answerable)} answerable questions "
          f"(hit = every expected passage in the top k; multi_any = at least one)\n")
    print_table(summary)
    return summary


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def print_table(rows: list[dict]) -> None:
    columns = list(rows[0])
    widths = [max(len(c), *(len(str(r[c])) for r in rows)) for c in columns]
    print("  ".join(c.ljust(w) for c, w in zip(columns, widths)))
    for r in rows:
        print("  ".join(str(r[c]).ljust(w) for c, w in zip(columns, widths)))


def main() -> None:
    questions = load_questions()
    print("=== Part 1: retrieval", file=sys.stderr)
    evaluate_retrieval(questions)


if __name__ == "__main__":
    main()
