"""Regenerate eval/questions.csv from corpus/test_set_worksheet.md (the human-edited source)."""
import csv
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
WORKSHEET = ROOT / "corpus" / "test_set_worksheet.md"
OUT = ROOT / "eval" / "questions.csv"
COLUMNS = ["id", "question", "kind", "expected_source", "expected_location", "reference_answer"]


def parse(text: str) -> list[dict]:
    rows = []
    for block in re.split(r"\n(?=## q\d+ )", text)[1:]:
        head = re.match(r"## (q\d+) · (single|multi|unanswerable)", block)
        if not head:
            raise SystemExit(f"bad header: {block.splitlines()[0]!r}")
        meta = re.search(r"<!--\s*source=(.*?)\s*\|\s*location=(.*?)\s*-->", block)
        q = re.search(r"\*\*Question:\*\*\s*(.+)", block)
        a = re.search(r"\*\*(?:Reference answer|What the assistant should say):\*\*\s*(.+)", block)
        if not (meta and q and a):
            raise SystemExit(f"{head.group(1)}: missing metadata, question or answer")
        rows.append({
            "id": head.group(1), "question": q.group(1).strip(), "kind": head.group(2),
            "expected_source": meta.group(1).strip(), "expected_location": meta.group(2).strip(),
            "reference_answer": a.group(1).strip(),
        })
    return rows


def validate(rows: list[dict]) -> list[str]:
    from index import CORPUS_DIR, SOURCES, parse_units

    known = {}
    for key, s in SOURCES.items():
        html = (CORPUS_DIR / f"{key}.html").read_text(encoding="utf-8", errors="replace")
        known[s["name"]] = {u["label"] for u in parse_units(html, s["name"])}
    problems = []
    for r in rows:
        srcs = [s for s in r["expected_source"].split(";") if s]
        locs = [l for l in r["expected_location"].split(";") if l]
        if r["kind"] == "unanswerable":
            if srcs or locs:
                problems.append(f"{r['id']}: unanswerable must have empty source/location")
            continue
        if len(srcs) != len(locs) or not srcs:
            problems.append(f"{r['id']}: source/location mismatch {srcs} {locs}")
        if r["kind"] == "single" and len(srcs) != 1:
            problems.append(f"{r['id']}: single needs exactly 1 passage")
        if r["kind"] == "multi" and len(srcs) < 2:
            problems.append(f"{r['id']}: multi needs 2+ passages")
        for s, l in zip(srcs, locs):
            if l not in known.get(s, set()):
                problems.append(f"{r['id']}: {s} / {l} does not exist in the corpus")
    return problems


if __name__ == "__main__":
    rows = parse(WORKSHEET.read_text(encoding="utf-8"))
    problems = validate(rows)
    for p in problems:
        print("PROBLEM:", p)
    if problems:
        raise SystemExit(1)
    with open(OUT, "w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=COLUMNS)
        w.writeheader()
        w.writerows(rows)
    kinds = {k: sum(r["kind"] == k for r in rows) for k in ("single", "multi", "unanswerable")}
    print(f"wrote {len(rows)} questions to {OUT.name}: {kinds}")
