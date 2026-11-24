"""Check eval/questions.csv: same rules as check.py's read_questions, plus
every expected (source, location) pair must exist in the extracted corpus.

    uv run python eval/validate_questions.py
"""

import csv
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
QUESTIONS = ROOT / "eval" / "questions.csv"
COLUMNS = ["id", "question", "kind", "expected_source", "expected_location", "reference_answer"]
MIN_QUESTIONS, MIN_UNANSWERABLE, MIN_MULTI = 30, 5, 5


def main() -> None:
    import index

    known = {(s["doc_id"], s["location"]) for s in index.load_corpus_sections()}
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        problems = [f"missing column {c}" for c in COLUMNS if c not in (reader.fieldnames or [])]
        rows = [r for r in reader if (r.get("question") or "").strip()]
    kinds = [r["kind"].strip().lower() for r in rows]
    if len(rows) < MIN_QUESTIONS:
        problems.append(f"{len(rows)} questions, need {MIN_QUESTIONS}")
    if kinds.count("unanswerable") < MIN_UNANSWERABLE:
        problems.append("too few unanswerable")
    if kinds.count("multi") < MIN_MULTI:
        problems.append("too few multi")
    if len({r["id"] for r in rows}) != len(rows):
        problems.append("ids not unique")
    if rows and kinds[0] != "single":
        problems.append("first row must be a single question (check.py asks it)")
    for r, kind in zip(rows, kinds):
        sources = [x.strip() for x in r["expected_source"].split(";") if x.strip()]
        locations = [x.strip() for x in r["expected_location"].split(";") if x.strip()]
        if kind not in ("single", "multi", "unanswerable"):
            problems.append(f"{r['id']}: unknown kind {kind!r}")
        if not r["reference_answer"].strip():
            problems.append(f"{r['id']}: no reference answer")
        if kind == "unanswerable":
            if sources or locations:
                problems.append(f"{r['id']}: unanswerable but has a source or location")
            continue
        expected = {"single": 1, "multi": 2}.get(kind)
        if len(sources) != expected or len(locations) != expected:
            problems.append(f"{r['id']}: {kind} needs {expected} source(s) and location(s)")
        for pair in zip(sources, locations):
            if pair not in known:
                problems.append(f"{r['id']}: {pair} is not a (doc_id, location) in the corpus")
    counts = ", ".join(f"{kinds.count(k)} {k}" for k in ("single", "multi", "unanswerable"))
    print(f"{len(rows)} questions: {counts}")
    if problems:
        sys.exit("PROBLEMS:\n  " + "\n  ".join(problems))
    print("questions.csv is valid.")


if __name__ == "__main__":
    main()
