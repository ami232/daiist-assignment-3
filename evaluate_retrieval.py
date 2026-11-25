
import csv
import json

from retrieval import search
from pathlib import Path

def evaluate_retrieval():

    with open("eval/questions.csv") as f:
        questions = list(csv.DictReader(f))

    answerable = [
        q for q in questions
        if q["kind"] != "unanswerable"
    ]

    if not answerable:
        raise ValueError("Complete questions.csv first.")

    summary = {}

    for design in ["semantic", "hybrid"]:

        hits = {1: 0, 3: 0, 5: 0}

        for q in answerable:

            results = search(
                q["question"],
                k=5,
                design=design
            )

            sources = q["expected_source"].split(";")
            pages = q["expected_location"].split(";")

            if len(sources) == 1:
                sources *= len(pages)

            if len(sources) != len(pages):
                raise ValueError(q["id"])

            expected = set(
                (s.strip(), p.strip())
                for s, p in zip(sources, pages)
            )

            for k in [1, 3, 5]:

                retrieved = {
                    (r["source"], str(r["page"]))
                    for r in results[:k]
                }

                if expected.issubset(retrieved):
                    hits[k] += 1

            print(design, q["id"], flush=True)

        summary[design] = {
            f"hit_rate@{k}": round(
                hits[k] / len(answerable), 4
            )
            for k in [1, 3, 5]
        }

    best_design = max(
        summary,
        key=lambda d: (
            summary[d]["hit_rate@5"],
            summary[d]["hit_rate@3"],
            summary[d]["hit_rate@1"]
        )
    )

    output = {
        "questions": len(answerable),
        "results": summary,
        "best_design": best_design
    }

    Path("eval/retrieval_results.json").write_text(
        json.dumps(output, indent=2)
    )

    print(json.dumps(output, indent=2))

    return output

if __name__ == "__main__":
    evaluate_retrieval()
