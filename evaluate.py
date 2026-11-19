"""
Assignment 3: evaluation (`main.py evaluate`).

Part 1 (this part): retrieval. For every answerable question in
eval/questions.csv, run each retrieval design and check whether a chunk from
the expected document and page is in the top 1, 3 and 5 results (hit rate).
Results are saved in eval/retrieval_results.csv and eval/retrieval_summary.csv.

Later parts add the end-to-end evaluation of the agent.
"""

import csv
from pathlib import Path

from retrieval import DESIGNS, search

ROOT = Path(__file__).resolve().parent
EVAL_DIR = ROOT / "eval"
QUESTIONS = EVAL_DIR / "questions.csv"
KS = (1, 3, 5)


def load_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r["question"].strip()]


def expected_passages(row: dict) -> set[tuple[str, int]]:
    """(source, page) pairs that answer the question. Sources and locations are paired in order;
    a single source can be paired with several pages."""
    sources = [s.strip() for s in row["expected_source"].split(";") if s.strip()]
    pages = [int(p.strip().lstrip("p")) for p in row["expected_location"].split(";") if p.strip()]
    if len(sources) == 1:
        sources = sources * len(pages)
    return set(zip(sources, pages))


def evaluate_retrieval(questions: list[dict]) -> list[dict]:
    answerable = [q for q in questions if q["kind"].strip() != "unanswerable"]
    rows = []
    for design in DESIGNS:
        for q in answerable:
            expected = expected_passages(q)
            results = search(q["question"], k=max(KS), design=design)
            found = [(r["source"], r["page"]) for r in results]
            row = {"design": design, "id": q["id"], "kind": q["kind"]}
            for k in KS:
                top = set(found[:k])
                row[f"hit@{k}"] = int(bool(top & expected))  # at least one expected passage found
                row[f"all@{k}"] = int(expected <= top)  # every expected passage found (matters for multi)
            row["first_hit_rank"] = next((i + 1 for i, p in enumerate(found) if p in expected), "")
            row["words_top5"] = sum(len(r["text"].split()) for r in results)
            row["retrieved"] = "; ".join(f"{s} p{p}" for s, p in found)
            rows.append(row)
    return rows


def summarise(rows: list[dict]) -> list[dict]:
    summary = []
    for design in DESIGNS:
        mine = [r for r in rows if r["design"] == design]
        multi = [r for r in mine if r["kind"] == "multi"]
        line = {"design": design, "questions": len(mine)}
        for k in KS:
            line[f"hit@{k}"] = round(sum(r[f"hit@{k}"] for r in mine) / len(mine), 3)
        line["multi_all@5"] = round(sum(r["all@5"] for r in multi) / len(multi), 3) if multi else ""
        line["avg_words_added_top5"] = round(sum(r["words_top5"] for r in mine) / len(mine))
        summary.append(line)
    return summary


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    questions = load_questions()
    rows = evaluate_retrieval(questions)
    summary = summarise(rows)
    write_csv(EVAL_DIR / "retrieval_results.csv", rows)
    write_csv(EVAL_DIR / "retrieval_summary.csv", summary)
    print("Retrieval hit rate (answerable questions):")
    for line in summary:
        print(f"  {line['design']:>7}: " + "  ".join(f"hit@{k}={line[f'hit@{k}']:.2f}" for k in KS)
              + f"  multi all@5={line['multi_all@5']}  ~{line['avg_words_added_top5']} words in top 5")


if __name__ == "__main__":
    main()
