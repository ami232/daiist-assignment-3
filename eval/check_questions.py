"""
Check eval/questions.csv while you write it. Embeds nothing, calls no API.

    uv run python eval/check_questions.py            # validate every row, show counts
    uv run python eval/check_questions.py q07 q12    # also print the label text each question points to

Checks: columns, unique ids, kind, expected_source is an indexed drug,
expected_location is a real section of that drug's label, multi questions
name two passages, unanswerable questions leave source/location empty, and
whether a question copies the label's own wording (which inflates retrieval).
"""

import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))

import index  # noqa: E402

QUESTIONS = ROOT / "eval" / "questions.csv"
COLUMNS = ["id", "question", "kind", "expected_source", "expected_location", "reference_answer"]
KINDS = {"single", "multi", "unanswerable"}
MINIMUM = {"total": 30, "multi": 5, "unanswerable": 5}
COPY_RUN = 7  # this many consecutive words shared with the label = copied wording


def load_sections() -> dict[str, dict[str, str]]:
    """{drug: {section number: full text}} for every indexed label."""
    sections: dict[str, dict[str, str]] = {}
    for name in index.LABELS:
        doc = index.extract_label(index.CORPUS_DIR / f"{name}.xml")
        drug = sections.setdefault(doc["source"], {})
        for block in doc["blocks"]:
            drug[block["number"]] = (drug.get(block["number"], "") + "\n" + block["text"]).strip()
    return sections


def matching_sections(drug: dict[str, str], location: str) -> list[str]:
    """'7' matches 7, 7.1, 7.2...; '7.3' matches 7.3 and 7.3.x; 'MG' matches MG."""
    location = location.strip()
    return [n for n in drug if n == location or n.startswith(location + ".")]


def words(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def copied_run(question: str, label_text: str) -> str | None:
    q, label = words(question), " ".join(words(label_text))
    for i in range(len(q) - COPY_RUN + 1):
        run = " ".join(q[i:i + COPY_RUN])
        if f" {run} " in f" {label} ":
            return run
    return None


def main() -> None:
    if not QUESTIONS.exists():
        sys.exit("eval/questions.csv not found")
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        missing = [c for c in COLUMNS if c not in (reader.fieldnames or [])]
        if missing:
            sys.exit(f"missing column(s): {', '.join(missing)}")
        rows = [r for r in reader if (r.get("question") or "").strip()]

    sections = load_sections()
    all_text = "\n".join(t for drug in sections.values() for t in drug.values())
    problems, warnings, seen = [], [], set()
    for r in rows:
        qid, kind = r["id"].strip(), r["kind"].strip().lower()
        sources = [s.strip().lower() for s in r["expected_source"].split(";") if s.strip()]
        locations = [s.strip() for s in r["expected_location"].split(";") if s.strip()]
        where = f"{qid or '(no id)'}:"
        if not qid or qid in seen:
            problems.append(f"{where} id missing or repeated")
        seen.add(qid)
        if kind not in KINDS:
            problems.append(f"{where} kind '{r['kind']}' is not one of {', '.join(sorted(KINDS))}")
        if not r["reference_answer"].strip():
            problems.append(f"{where} reference_answer is empty")
        if kind == "unanswerable":
            if sources or locations:
                problems.append(f"{where} unanswerable questions leave expected_source and expected_location empty")
        elif kind in KINDS:
            if not sources:
                problems.append(f"{where} needs an expected_source")
            if len(locations) != len(sources):
                problems.append(f"{where} {len(sources)} source(s) but {len(locations)} location(s); give one location per source, ';'-separated")
            if kind == "multi" and len(sources) < 2:
                problems.append(f"{where} multi questions need two passages: 'warfarin;amiodarone' and '7.1;7'")
            if kind == "single" and len(sources) > 1:
                warnings.append(f"{where} single question with {len(sources)} sources; should it be multi?")
            for source, location in zip(sources, locations):
                if source not in sections:
                    problems.append(f"{where} '{source}' is not an indexed drug ({', '.join(sorted(sections))})")
                elif not matching_sections(sections[source], location):
                    problems.append(f"{where} {source} has no section '{location}' (see eval/section_map.md)")
            if kind == "multi" and len(set(zip(sources, locations))) < 2:
                problems.append(f"{where} multi question points at the same passage twice")
        run = copied_run(r["question"], all_text)
        if run:
            warnings.append(f"{where} copies label wording \"{run}\"; rephrase as a caregiver would ask")

    kinds = [r["kind"].strip().lower() for r in rows]
    print(f"{len(rows)} questions: " + ", ".join(f"{kinds.count(k)} {k}" for k in sorted(KINDS)))
    todo = []
    if len(rows) < MINIMUM["total"]:
        todo.append(f"{MINIMUM['total'] - len(rows)} more questions")
    for kind in ("multi", "unanswerable"):
        if kinds.count(kind) < MINIMUM[kind]:
            todo.append(f"{MINIMUM[kind] - kinds.count(kind)} more {kind}")
    drugs = sorted({s.strip().lower() for r in rows for s in r["expected_source"].split(";") if s.strip()})
    print(f"drugs covered: {', '.join(drugs) or 'none'}; not yet: {', '.join(sorted(set(sections) - set(drugs))) or 'none'}")
    print("still needed: " + ("; ".join(todo) if todo else "nothing, minimums met"))
    for p in problems:
        print(f"PROBLEM  {p}")
    for w in warnings:
        print(f"warning  {w}")
    if not problems:
        print("format OK")

    for qid in sys.argv[1:]:
        row = next((r for r in rows if r["id"].strip() == qid), None)
        if row is None:
            print(f"\n{qid}: not found")
            continue
        print(f"\n=== {qid} [{row['kind']}] {row['question']}\n    reference: {row['reference_answer']}")
        for source, location in zip(row["expected_source"].split(";"), row["expected_location"].split(";")):
            source, location = source.strip().lower(), location.strip()
            for number in matching_sections(sections.get(source, {}), location):
                print(f"\n--- {source} {number}\n{sections[source][number]}")
    sys.exit(1 if problems else 0)


if __name__ == "__main__":
    main()
