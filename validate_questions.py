"""
Assignment 3: check eval/questions.csv before running anything on it.
`uv run python validate_questions.py`

Checks what check.py checks (columns, counts, unique ids, empty sources for
unanswerable questions) and also that every expected_source and
expected_location exists in the index's chunk metadata, so a typo does not
show up later as a retrieval miss. A location may be written as the section
title ("Dosage and Administration") or the openFDA field name
("dosage_and_administration"); both are in the chunk metadata. No API calls.
"""

import csv
import sys
from collections import defaultdict
from pathlib import Path

from download import LABELS, label_path
from index import chunk_file

ROOT = Path(__file__).resolve().parent
QUESTIONS = ROOT / "eval" / "questions.csv"
COLUMNS = ["id", "question", "kind", "expected_source", "expected_location", "reference_answer"]
KINDS = {"single", "multi", "unanswerable"}
MINIMUMS = {"total": 30, "unanswerable": 5, "multi": 5}


def split(value: str) -> list[str]:
    return [v.strip() for v in value.split(";") if v.strip()]


def main() -> int:
    locations = defaultdict(set)  # indexed source -> its locations, as titles and field names
    held_back = set()
    for entry in LABELS:
        if entry.get("held_back"):
            held_back.add(entry["file"])
            continue
        for chunk in chunk_file(label_path(entry)):
            meta = chunk["metadata"]
            locations[meta["source"]].update((meta["location"], meta["field"]))

    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        missing = [c for c in COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            print(f"Missing column(s): {', '.join(missing)}")
            return 1
        rows = [r for r in reader if (r.get("question") or "").strip()]

    problems = []
    for r in rows:
        qid, kind = r["id"].strip(), r["kind"].strip().lower()
        sources, locs = split(r["expected_source"]), split(r["expected_location"])
        if kind not in KINDS:
            problems.append(f"{qid}: kind {kind!r} is not one of {sorted(KINDS)}")
            continue
        if not r["reference_answer"].strip():
            problems.append(f"{qid}: no reference_answer")
        if kind == "unanswerable":
            if sources or locs:
                problems.append(f"{qid}: unanswerable questions need empty expected_source and expected_location")
            continue
        if not sources:
            problems.append(f"{qid}: no expected_source")
        if not locs:
            problems.append(f"{qid}: no expected_location")
        for s in sources:
            if s in held_back:
                problems.append(f"{qid}: {s!r} is held back, so the starting index cannot answer this; mark it unanswerable")
            elif s not in locations:
                problems.append(f"{qid}: unknown source {s!r}; use one of {sorted(locations)}")
        if kind == "multi" and len(sources) < 2 and len(locs) < 2:
            problems.append(f"{qid}: multi questions need two passages (two sources or two locations)")
        # Locations pair with sources by position; a single source may list several locations.
        pairs = (list(zip(sources, locs)) if len(sources) == len(locs)
                 else [(s, l) for s in sources[:1] for l in locs] if len(sources) == 1
                 else None)
        if pairs is None:
            problems.append(f"{qid}: give one location per source (or one source with several locations)")
            continue
        for s, l in pairs:
            if s in locations and l not in locations[s]:
                problems.append(f"{qid}: {s!r} has no location {l!r}; it has {sorted(locations[s])}")

    kinds = [r["kind"].strip().lower() for r in rows]
    ids = [r["id"].strip() for r in rows]
    if len(rows) < MINIMUMS["total"]:
        problems.append(f"{len(rows)} questions; at least {MINIMUMS['total']} are required")
    for kind in ("unanswerable", "multi"):
        if kinds.count(kind) < MINIMUMS[kind]:
            problems.append(f"{kinds.count(kind)} {kind} questions; at least {MINIMUMS[kind]} are required")
    if len(set(ids)) != len(ids):
        problems.append("question ids are not unique")

    covered = {s for r in rows for s in split(r["expected_source"])}
    print(f"{len(rows)} questions: " + ", ".join(f"{kinds.count(k)} {k}" for k in sorted(KINDS)))
    print(f"Labels covered: {len(covered & set(locations))}/{len(locations)}"
          + (f" (not yet: {', '.join(sorted(set(locations) - covered))})" if set(locations) - covered else ""))
    for p in problems:
        print(f"  PROBLEM {p}")
    print("OK" if not problems else f"{len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
