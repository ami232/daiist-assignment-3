"""
Check eval/questions.csv before you evaluate: `uv run python eval_check.py`.

No API calls. It checks the counts check.py asks for, and one thing check.py
does not: that every expected_source is a real file in corpus/ and every
expected_location exists in that file (a clause number such as "9" or "9.1",
or a label such as "Clause 9"), so a typo in the answer key does not look like
a retrieval miss later.
"""

import csv
import re
import sys
from pathlib import Path

import index

ROOT = Path(__file__).resolve().parent
QUESTIONS = ROOT / "eval" / "questions.csv"


def known_locations() -> dict[str, dict]:
    """source -> {"labels": [chunk location labels], "subclauses": {"9.1", ...}, "clauses": {"9", ...}}"""
    out = {}
    for path in sorted(index.CORPUS_DIR.glob("*.pdf")):
        doc = index.parse_contract(path)
        labels, subs, clauses = [], set(), set()
        for c in index.chunk_clauses(doc):
            labels.append(c["metadata"]["location"].lower())
            subs |= set(re.findall(r"^(\d+\.\d+)\s", c["text"], re.M))
        for c in doc["clauses"]:
            clauses.add(c["id"].lower())
        out[path.name] = {"labels": labels, "subclauses": subs, "clauses": clauses}
    return out


def location_ok(loc: str, info: dict) -> bool:
    loc = loc.strip().lower()
    if not loc:
        return False
    for part in re.split(r"[;,]|\band\b", loc):
        part = part.strip()
        m = re.fullmatch(r"(?:clauses?\s+)?(\d+(?:\.\d+)?)", part)
        if m:
            n = m.group(1)
            if n in info["subclauses"] or n in info["clauses"]:
                continue
            return False
        m = re.fullmatch(r"(schedule\s+\d+)", part)
        if m and m.group(1) in info["clauses"]:
            continue
        if any(part in label for label in info["labels"]):
            continue
        return False
    return True


def main() -> int:
    if not QUESTIONS.is_file():
        print("eval/questions.csv is missing.")
        return 1
    known = known_locations()
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if (r.get("question") or "").strip()]
    problems, warnings = [], []
    kinds = [r["kind"].strip().lower() for r in rows]
    for r in rows:
        qid, kind = r["id"], r["kind"].strip().lower()
        sources = [s.strip() for s in r["expected_source"].split(";") if s.strip()]
        locs = [s.strip() for s in r["expected_location"].split("|")] if "|" in r["expected_location"] else \
               [r["expected_location"].strip()]
        if kind not in ("single", "multi", "unanswerable"):
            problems.append(f"{qid}: kind '{kind}' is not single, multi or unanswerable")
        if kind == "unanswerable":
            if sources or r["expected_location"].strip():
                problems.append(f"{qid}: unanswerable questions have empty expected_source and expected_location")
            if not r["reference_answer"].strip():
                warnings.append(f"{qid}: write in reference_answer what the assistant should say")
            continue
        if kind == "multi" and len(sources) < 2 and len(locs) < 2:
            warnings.append(f"{qid}: kind multi but one source and one location; are there really two passages?")
        for s in sources:
            if s not in known:
                problems.append(f"{qid}: expected_source '{s}' is not a file in corpus/")
        if len(sources) == 1 and sources[0] in known:
            for loc in locs:
                if not location_ok(loc, known[sources[0]]):
                    problems.append(f"{qid}: location '{loc}' not found in {sources[0]}")
        elif len(sources) > 1:
            parts = [p.strip() for p in r["expected_location"].split(";")]
            if len(parts) != len(sources):
                warnings.append(f"{qid}: {len(sources)} sources but {len(parts)} locations; give one location per source, separated by ';'")
            else:
                for s, loc in zip(sources, parts):
                    if s in known and not location_ok(loc, known[s]):
                        problems.append(f"{qid}: location '{loc}' not found in {s}")
        if not r["reference_answer"].strip():
            warnings.append(f"{qid}: empty reference_answer")
    ids = [r["id"] for r in rows]
    if len(set(ids)) != len(ids):
        problems.append("question ids are not unique")
    counts = {k: kinds.count(k) for k in ("single", "multi", "unanswerable")}
    print(f"{len(rows)} questions: {counts}")
    for need, label in ((30, "questions"),):
        if len(rows) < need:
            problems.append(f"{len(rows)} {label}; at least {need} are required")
    if counts["unanswerable"] < 5:
        problems.append(f"{counts['unanswerable']} unanswerable; at least 5 are required")
    if counts["multi"] < 5:
        problems.append(f"{counts['multi']} multi; at least 5 are required")
    for w in warnings:
        print("WARNING:", w)
    for p in problems:
        print("PROBLEM:", p)
    print("OK" if not problems else f"{len(problems)} problem(s)")
    return 1 if problems else 0


if __name__ == "__main__":
    sys.exit(main())
