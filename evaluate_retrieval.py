import csv
from pathlib import Path

from retrieval import search


ROOT = Path(__file__).resolve().parent
QUESTIONS = ROOT / "eval" / "questions.csv"
OUTPUT = ROOT / "eval" / "retrieval_dense.csv"
CUTOFFS = (1, 3, 5)


def expected_pages(row):
    sources = [s.strip() for s in row["expected_source"].split(";")]
    pages = [int(p.strip()) for p in row["expected_location"].split(";")]
    return set(zip(sources, pages, strict=True))


def evaluate_question(row, search_fn=search):
    expected = expected_pages(row)
    hits = search_fn(row["question"], k=5)

    result = {
        "id": row["id"],
        "kind": row["kind"],
        "top_5_chunks": ";".join(hit["id"] for hit in hits),
    }

    for k in CUTOFFS:
        retrieved = {(hit["source"], hit["page"]) for hit in hits[:k]}
        result[f"hit_at_{k}"] = int(expected.issubset(retrieved))

    return result


def main():
    with QUESTIONS.open(encoding="utf-8-sig", newline="") as file:
        questions = [
            row for row in csv.DictReader(file)
            if row["kind"] in {"single", "multi"}
        ]

    results = []
    for row in questions:
        result = evaluate_question(row)
        results.append(result)
        print(
            f"{row['id']} | "
            f"@1={result['hit_at_1']} "
            f"@3={result['hit_at_3']} "
            f"@5={result['hit_at_5']}",
            flush=True,
        )

    with OUTPUT.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    for group in ("single", "multi", "all"):
        subset = [r for r in results if group == "all" or r["kind"] == group]
        print(f"\n{group} ({len(subset)} questions)")
        for k in CUTOFFS:
            count = sum(r[f"hit_at_{k}"] for r in subset)
            print(f"  Hit@{k}: {count}/{len(subset)} ({count / len(subset):.1%})")

    print(f"\nSaved results to {OUTPUT.name}")


if __name__ == "__main__":
    main()