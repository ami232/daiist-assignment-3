"""
Assignment 3: evaluation (`main.py evaluate`).

Retrieval matching is defined here; the evaluation run itself comes later.

expected_location in eval/questions.csv names ONE Rn. or § per passage, `;` between passages:
    "BGH VIII ZR 107/20, Rn. 18"   "BGH VIII ZR 107/20, Leitsatz"
    "§ 2 Nr. 10 BetrKV"            "§ 556 Abs. 3 BGB"   "§ 7 HeizkostenV"   "Anlage CO2KostAufG"
A retrieved chunk is a hit when it comes from that document and covers that Rn./§ (chunk
metadata `covers`, written by index.py). Matching never looks at chunk ids or location strings,
so hit rates stay comparable across chunking designs.
"""

from __future__ import annotations

import csv
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parent
QUESTIONS = ROOT / "eval" / "questions.csv"
CHUNKS_FILE = ROOT / "index" / "chunks.jsonl"
KS = (1, 3, 5)

STATUTES = ("BGB", "BetrKV", "HeizkostenV", "CO2KostAufG")
_JUDGMENT = re.compile(r"^(BGH VIII ZR \d+/\d+),\s*(?:Rn\.?\s*(\d+)|(Leitsatz))$")
_STATUTE = re.compile(
    r"^(§\s*\d+[a-z]?|Anlage|Anhang EV)"
    r"(?:\s+Abs\.\s*(\d+[a-z]?))?(?:\s+(?:Satz|S\.)\s*\d+)?"
    r"(?:\s+Nr\.\s*(\d+[a-z]?))?(?:\s+(?:Satz|S\.)\s*\d+)?"
    rf"\s+({'|'.join(STATUTES)})$"
)


def parse_location(location: str) -> dict:
    """One expected location -> {doc_id, rn | leitsatz | para, abs, nr}. Raises ValueError if unparseable."""
    loc = " ".join(location.replace("§§", "§").split())
    if m := _JUDGMENT.match(loc):
        return {"doc_id": m.group(1), "rn": m.group(2), "leitsatz": bool(m.group(3))}
    if m := _STATUTE.match(loc):
        para = re.sub(r"§\s*", "§ ", m.group(1))
        return {"doc_id": m.group(4), "para": para, "abs": m.group(2), "nr": m.group(3)}
    raise ValueError(
        f"Can't parse expected_location {location!r}. Use one Rn. or § per passage, e.g. "
        f"'BGH VIII ZR 107/20, Rn. 18' or '§ 2 Nr. 10 BetrKV'."
    )


def covers(meta: dict, target: dict) -> bool:
    """Does a chunk (its metadata) cover this target passage?"""
    if meta.get("doc_id") != target["doc_id"]:
        return False
    keys = set(meta.get("covers", "").strip("|").split("|"))
    if "rn" in target:
        return "Leitsatz" in keys if target["leitsatz"] else f"Rn. {target['rn']}" in keys
    para, abs_, nr = target["para"], target["abs"], target["nr"]
    if para in keys:  # the whole § is in this chunk
        return True
    if abs_ and nr:
        qualified = f"{para} Abs. {abs_} Nr. {nr}"
        abs_has_items = any(k.startswith(f"{para} Abs. {abs_} Nr. ") for k in keys)
        return qualified in keys or (f"{para} Abs. {abs_}" in keys and not abs_has_items)
    if abs_:
        return f"{para} Abs. {abs_}" in keys
    if nr:
        return f"{para} Nr. {nr}" in keys or any(k.startswith(f"{para} Abs. ") and k.endswith(f" Nr. {nr}") for k in keys)
    return f"{para}*" in keys  # expected the whole §, chunk holds part of it


def targets_of(expected_location: str) -> list[dict]:
    return [parse_location(part) for part in expected_location.split(";") if part.strip()]


def hits_at_k(retrieved: list[dict], expected_location: str, ks=KS) -> dict:
    """Hit at each k for one question, given the retrieved chunks' metadata in rank order.

    'all': every expected passage is covered within the top k (the headline number; for
    single questions it equals 'any'). 'any': at least one is.
    """
    targets = targets_of(expected_location)
    found_at = [next((rank for rank, meta in enumerate(retrieved, 1) if covers(meta, t)), None) for t in targets]
    return {
        k: {
            "all": all(r is not None and r <= k for r in found_at),
            "any": any(r is not None and r <= k for r in found_at),
        }
        for k in ks
    }


def load_chunks(path: Path = CHUNKS_FILE) -> list[dict]:
    return [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


def validate_test_set(questions: Path = QUESTIONS, chunks_file: Path = CHUNKS_FILE) -> list[str]:
    """Problems with eval/questions.csv locations: unparseable, wrong source, or covered by no chunk."""
    chunks = load_chunks(chunks_file)
    problems = []
    with questions.open(newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            if row["kind"].strip().lower() == "unanswerable":
                continue
            sources = {s.strip() for s in row["expected_source"].split(";") if s.strip()}
            try:
                targets = targets_of(row["expected_location"])
            except ValueError as error:
                problems.append(f"{row['id']}: {error}")
                continue
            if not targets:
                problems.append(f"{row['id']}: no expected_location")
            for t in targets:
                if t["doc_id"] not in sources:
                    problems.append(f"{row['id']}: location in {t['doc_id']} but expected_source is {sorted(sources)}")
                if not any(covers(c, t) for c in chunks):
                    problems.append(f"{row['id']}: no indexed chunk covers {t} (dropped Tatbestand / part I, or a typo?)")
    return problems


def main() -> None:
    if QUESTIONS.is_file():
        problems = validate_test_set()
        print("test set locations OK" if not problems else "\n".join(problems))
    raise NotImplementedError("Retrieval and end-to-end evaluation not written yet.")


if __name__ == "__main__":
    main()
