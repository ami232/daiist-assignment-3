"""Format checks for eval/questions.csv (task 2.3). `uv run pytest tests/test_questions.py`

Only the format is checked here: columns, kinds and minimums, and that every
expected source/location exists in index/outline.csv. The content is the student's.
"""

import csv
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
QUESTIONS = ROOT / "eval" / "questions.csv"
OUTLINE = ROOT / "index" / "outline.csv"
COLUMNS = ["id", "question", "kind", "expected_source", "expected_location", "reference_answer"]
KINDS = {"single", "multi", "unanswerable"}


def read(path: Path) -> list[dict]:
    with path.open(encoding="utf-8", newline="") as f:
        return list(csv.DictReader(f))


@pytest.fixture(scope="module")
def rows():
    return read(QUESTIONS)


@pytest.fixture(scope="module")
def locations():
    return {(r["source"], r["location"]) for r in read(OUTLINE) if r["held_out"] == "0"}


def pairs(row):
    sources = [s.strip() for s in row["expected_source"].split(";") if s.strip()]
    places = [p.strip() for p in row["expected_location"].split(";") if p.strip()]
    return sources, places


def test_columns_and_ids(rows):
    with QUESTIONS.open(encoding="utf-8", newline="") as f:
        assert next(csv.reader(f)) == COLUMNS
    ids = [r["id"] for r in rows]
    assert len(ids) == len(set(ids))
    assert all(r["question"].strip() for r in rows)


def test_minimums(rows):
    kinds = [r["kind"] for r in rows]
    assert set(kinds) <= KINDS, set(kinds) - KINDS
    assert len(rows) >= 30
    assert kinds.count("multi") >= 5
    assert kinds.count("unanswerable") >= 5


def test_expected_locations_exist(rows, locations):
    for r in rows:
        sources, places = pairs(r)
        if r["kind"] == "unanswerable":
            assert not sources and not places, r["id"]
            continue
        assert sources and len(sources) == len(places), f"{r['id']}: sources and locations must pair up"
        for pair in zip(sources, places):
            assert pair in locations, f"{r['id']}: {pair} is not in index/outline.csv"
        if r["kind"] == "multi":
            assert len(set(zip(sources, places))) >= 2, f"{r['id']}: a multi question needs two passages"


def test_reference_answers_written(rows):
    missing = [r["id"] for r in rows if not r["reference_answer"].strip()]
    assert not missing, f"reference_answer still empty for: {', '.join(missing)}"
