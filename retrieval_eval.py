import csv
import json
import statistics
from pathlib import Path

from index import connect
from retrieval import rank, set_design

OUT = Path("eval")


def read_questions():
    with (OUT / "questions.csv").open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


def required(q):
    if q["kind"] == "unanswerable":
        return set()

    sources = q["expected_source"].split(";")
    locations = q["expected_location"].split(";")

    if len(sources) != len(locations):
        raise ValueError(f"Invalid references: {q['id']}")

    return set(zip(sources, locations))


def retrieved(passages):
    return {
        (p["source"], p["location"])
        for p in passages}


def retrieval_eval(questions):
    answerable = [
        q for q in questions
        if q["kind"] != "unanswerable"]

    results = {}
    per_question = []

    with connect() as db:
        available = {
            (r["source"], r["location"])
            for r in db.execute(
                "SELECT DISTINCT source, location "
                "FROM chunks WHERE vector IS NOT NULL")}

        missing_vectors = db.execute(
            "SELECT COUNT(*) FROM chunks WHERE vector IS NULL").fetchone()[0]

    if missing_vectors:
        raise RuntimeError("Index is incomplete")

    for q in answerable:
        missing = required(q) - available

        if missing:
            raise ValueError(f"{q['id']}: references not found: {missing}")

    for design in ("dense", "hybrid"):
        rows = []

        print(f"\nEvaluating {design.upper()}")

        for q in answerable:
            passages = rank(q["question"], design, k=5)
            gold = required(q)

            row = {
                "id": q["id"],
                "kind": q["kind"],
                "design": design,
                "ids": [p["id"] for p in passages]}

            for k in (1, 3, 5):
                have = retrieved(passages[:k])

                row[f"hit@{k}"] = int(bool(gold & have))
                row[f"all@{k}"] = int(gold <= have)

            rows.append(row)

            print(
                f"{q['id']}: "
                f"Hit@5={row['hit@5']} "
                f"All@5={row['all@5']}",
                flush=True)

        metrics = {}

        for k in (1, 3, 5):
            for metric in ("hit", "all"):
                key = f"{metric}@{k}"

                metrics[key] = statistics.mean(
                    row[key] for row in rows)

        multi = [
            row for row in rows
            if row["kind"] == "multi"]

        metrics["multi_all@5"] = statistics.mean(row["all@5"] for row in multi)

        results[design] = metrics
        per_question.extend(rows)

    chosen = max(
        results,
        key=lambda d: (
            results[d]["all@5"],
            results[d]["hit@1"]))

    set_design(chosen)

    output = {
        "designs": results,
        "selected": chosen,
        "per_question": per_question}

    (OUT / "retrieval.json").write_text(
        json.dumps(output, indent=2),
        encoding="utf-8")

    print("\n--- FINAL RESULTS ---")

    for design, metrics in results.items():
        print(f"\n{design.upper()}")

        for metric, value in metrics.items():
            print(f"{metric}: {value:.1%}")

    print(f"\nSelected design: {chosen}")

    return chosen

if __name__ == "__main__":
    retrieval_eval(read_questions())
