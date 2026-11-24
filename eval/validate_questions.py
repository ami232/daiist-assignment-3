"""
Check eval/questions.csv against the built index, without calling any API.

    uv run python eval/validate_questions.py          # list problems
    uv run python eval/validate_questions.py --show   # also print each expected passage

The reference answers were drafted from memory of the regulation, so read every one
against the passage it points to (use --show) and fix anything that does not match
before you trust the evaluation. A question whose expected location is missing from
the index is a bad test question, or a sign the section numbers differ in your snapshot.
"""

import csv
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import rag  # noqa: E402


def main() -> int:
    show = "--show" in sys.argv
    with (ROOT / "eval" / "questions.csv").open(newline="", encoding="utf-8") as handle:
        rows = [r for r in csv.DictReader(handle) if (r.get("question") or "").strip()]
    data = rag.get_collection().get(include=["documents", "metadatas"])
    by_pair = {}
    for text, meta in zip(data["documents"], data["metadatas"]):
        by_pair.setdefault(rag.normalise_label(meta["source"], meta["location"]), []).append(text)

    kinds = Counter(r["kind"].strip().lower() for r in rows)
    print(f"{len(rows)} questions: {dict(kinds)}; index has {len(data['ids'])} chunks in {len(by_pair)} sections")
    if len({r['id'] for r in rows}) != len(rows):
        print("PROBLEM: question ids are not unique")

    problems = 0
    for row in rows:
        if row["kind"].strip().lower() == "unanswerable":
            continue
        sources = [s.strip() for s in row["expected_source"].split(";")]
        locations = [l.strip() for l in row["expected_location"].split(";")]
        for source, location in zip(sources, locations):
            key = rag.normalise_label(source, location)
            if key not in by_pair:
                problems += 1
                print(f"MISSING {row['id']}: [{source} | {location}] is not in the index")
            elif show:
                print(f"\n{row['id']}  {row['question']}\n  reference: {row['reference_answer']}\n  passage [{source} | {location}]:")
                print("    " + "\n    ".join("\n".join(by_pair[key]).splitlines()))
    print(f"\n{problems} expected passages missing" if problems else "\nEvery expected passage exists in the index.")
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
