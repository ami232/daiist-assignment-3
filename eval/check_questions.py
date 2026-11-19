"""
Offline check of eval/questions.csv (no API calls): `uv run python eval/check_questions.py`

Annotation format for expected_source / expected_location (decided 2026-11-19):

  single  `;` (or `|`) separates ALTERNATIVE locations; any one of them is a hit.
          Each alternative must contain the complete answer.
  multi   `;` separates REQUIRED pieces of evidence (groups); `|` separates
          alternative locations for the same piece of evidence. Metrics:
          hit-any@k (at least one group retrieved) and hit-all@k (every group).

expected_source mirrors expected_location: one source for everything, one
source per `;` group (applies to that group's alternatives), or one per location.

A location matches a chunk when the chunk has that source and the location's
heading segments ('A > B') match a contiguous run of the chunk's heading path,
segment by segment (case-insensitive; exact, or a prefix for headings of 30+
characters), e.g. "USE OF PROCEEDS", "8.1.1 Eligible Retail Investors",
"Article V > Section 5.5 Rights of Class T Common Stock".

Anti-inflation checks: a location matching more than BROAD chunks is flagged;
in a multi question, two evidence groups that can be satisfied by the same chunk
are an error (one passage would answer it, so it is not really multi-passage).
"""

import csv
import json
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QUESTIONS = ROOT / "eval" / "questions.csv"
CHUNKS = ROOT / "index" / "chunks.jsonl"
COLUMNS = ["id", "question", "kind", "expected_source", "expected_location", "reference_answer"]
KINDS = {"single", "multi", "unanswerable"}
BROAD = 25  # a location matching more chunks than this makes Hit@k too easy


PREFIX_MIN = 30  # long headings (e.g. a risk factor's title) may be given by their beginning


def _segment_matches(expected: str, actual: str) -> bool:
    e, a = expected.strip().lower(), actual.strip().lower()
    if a.endswith("…"):  # heading truncated in the chunk metadata
        a = a[:-1].rstrip()
        if len(a) >= PREFIX_MIN and e.startswith(a):
            return True
    return e == a or (len(e) >= PREFIX_MIN and a.startswith(e))


def location_matches(location: str, chunk_location: str) -> bool:
    """The expected location is one or more heading segments ('A > B') that must
    match a contiguous run of the chunk's heading path, segment by segment
    (case-insensitive, exact; a prefix is accepted only for headings of 30+
    characters). 'Article V' does not match 'Article VII', and 'CONCURRENT PRIVATE
    PLACEMENT' does not match '... > Concurrent Private Placement Shares'."""
    expected = [s for s in location.split(">") if s.strip()]
    path = chunk_location.split(" > ")
    return any(all(_segment_matches(e, path[i + j]) for j, e in enumerate(expected))
               for i in range(len(path) - len(expected) + 1))


def _structure(value: str, kind: str) -> list[list[str]]:
    value = (value or "").strip()
    if not value:
        return []
    if kind == "multi":
        return [[a.strip() for a in group.split("|") if a.strip()] for group in value.split(";") if group.strip()]
    return [[a.strip() for a in re.split(r"[;|]", value) if a.strip()]]  # single: one group of alternatives


def parse_expected(row: dict) -> list[list[tuple[str, str]]]:
    """Evidence groups, each a list of alternative (source, location) pairs.
    Raises ValueError if expected_source and expected_location do not line up."""
    kind = row["kind"].strip().lower()
    sources, locations = _structure(row["expected_source"], kind), _structure(row["expected_location"], kind)
    flat_sources = [s for g in sources for s in g]
    if not locations:
        return [[(s, "") for s in group] for group in sources]
    if len(flat_sources) == 1:
        return [[(flat_sources[0], loc) for loc in group] for group in locations]
    if len(sources) != len(locations) or any(len(gs) not in (1, len(gl)) for gs, gl in zip(sources, locations)):
        raise ValueError(
            f"expected_source {[len(g) for g in sources]} and expected_location {[len(g) for g in locations]} "
            "have a different ';'/'|' structure; give one source overall, one per group, or one per location"
        )
    return [[(gs[0] if len(gs) == 1 else s, loc) for s, loc in zip(gs * len(gl) if len(gs) == 1 else gs, gl)]
            for gs, gl in zip(sources, locations)]


def chunk_ids_for(chunks: list[dict], source: str, location: str) -> set[int]:
    return {i for i, c in enumerate(chunks)
            if c["source"] == source and (not location or location_matches(location, c["location"]))}


def main() -> int:
    chunks = [json.loads(line) for line in CHUNKS.read_text(encoding="utf-8").splitlines() if line.strip()]
    sources = {c["source"] for c in chunks}
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        missing = [c for c in COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            print(f"ERROR: missing columns {missing}")
            return 1
        rows = [r for r in reader if (r.get("question") or "").strip()]

    errors, warnings = [], []
    coverage = Counter()
    for dup in [i for i, n in Counter(r["id"].strip() for r in rows).items() if n > 1]:
        errors.append(f"duplicate id {dup}")
    for r in rows:
        qid, kind = r["id"].strip(), r["kind"].strip().lower()
        if not re.fullmatch(r"q\d{2,3}", qid):
            warnings.append(f"{qid}: ids should look like q01, q02...")
        if kind not in KINDS:
            errors.append(f"{qid}: kind '{kind}' is not one of {sorted(KINDS)}")
            continue
        if not r["reference_answer"].strip():
            errors.append(f"{qid}: empty reference_answer")
        if kind == "unanswerable":
            if r["expected_source"].strip() or r["expected_location"].strip():
                errors.append(f"{qid}: unanswerable questions must leave expected_source/location empty")
            continue
        try:
            groups = parse_expected(r)
        except ValueError as error:
            errors.append(f"{qid}: {error}")
            continue
        if not groups:
            errors.append(f"{qid}: answerable question without expected_source")
            continue
        if kind == "multi" and len(groups) < 2:
            errors.append(f"{qid}: 'multi' needs at least two ';'-separated evidence groups")
        group_hits = []
        for group in groups:
            hits = set()
            for source, location in group:
                coverage[f"{source} | {location.split(' > ')[0][:60]}"] += 1
                if source not in sources:
                    errors.append(f"{qid}: unknown source '{source}' (valid: {', '.join(sorted(sources))})")
                    continue
                if not location:
                    warnings.append(f"{qid}: no expected_location for {source}; Hit@k could only check the document")
                ids = chunk_ids_for(chunks, source, location)
                if not ids:
                    errors.append(f"{qid}: location '{location}' matches no chunk of {source}")
                elif len(ids) > BROAD:
                    warnings.append(f"{qid}: location '{location}' matches {len(ids)} chunks of {source}; too broad, Hit@k would be inflated")
                hits |= ids
            group_hits.append(hits)
        for i in range(len(group_hits)):
            for j in range(i + 1, len(group_hits)):
                if group_hits[i] & group_hits[j]:
                    errors.append(f"{qid}: evidence groups {i + 1} and {j + 1} can be satisfied by the same chunk; not really multi-passage")

    kinds = Counter(r["kind"].strip().lower() for r in rows)
    print(f"{len(rows)} questions: " + ", ".join(f"{kinds[k]} {k}" for k in sorted(kinds)))
    for name, count, minimum in [("total", len(rows), 30), ("multi", kinds["multi"], 5), ("unanswerable", kinds["unanswerable"], 5)]:
        if count < minimum:
            errors.append(f"{name}: {count} < required {minimum}")
    print("coverage by source | top-level location:")
    for key, n in sorted(coverage.items()):
        print(f"  {n:2d}  {key}")
    for w in warnings:
        print(f"WARNING {w}")
    for e in errors:
        print(f"ERROR   {e}")
    print("OK" if not errors else f"{len(errors)} error(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
