"""
Assignment 3: evaluation (`uv run python main.py evaluate`).

Part 1, retrieval (this file, now): hit rate at k = 1, 3, 5 for every design in
index.DESIGNS, on the answerable questions of eval/questions.csv.
Part 2, end-to-end: TODO (agent answers, code checks, LLM judge, human agreement).

Hit definition. A retrieved chunk is correct when it comes from the expected
document AND matches the expected location:
  - "Art. 33.2"          -> chunk's section is Article 33, or its text contains "33.2."
  - "III.3.1 ..." "IV.2" -> chunk's section is III.3 / IV.2, or its text contains the number
  - "(p. 3)"             -> chunk's pages include page 3
  - a section name       -> chunk heading is part of the name, or the name's first
                            words appear in the chunk's section or text
  - for 4 questions whose heading was lost in extraction, a chunk containing the
    key fact of the reference answer (EVIDENCE below)
A single question is a hit at k if any of the top-k chunks is correct.
A multi question has one part per document (";" with no space separates parts):
  hit@k  = at least one part found in the top k
  full@k = every part found in the top k

Query vectors are cached in eval/query_vectors.json, so re-runs cost no embeddings.
Outputs: eval/retrieval_per_question.csv, eval/retrieval_summary.csv.
"""

from __future__ import annotations

import csv
import json
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
sys.path.insert(0, str(ROOT))

import index as ix  # noqa: E402

EVAL_DIR = ROOT / "eval"
QUESTIONS = EVAL_DIR / "questions.csv"
QUERY_CACHE = EVAL_DIR / "query_vectors.json"
KS = (1, 3, 5)

# Names used in questions.csv -> `source` in the chunk metadata.
SOURCE_ALIASES = {
    "attendance policy bachelor degrees 2026-2027": "Attendance Policy, Bachelor Programs",
    "general academic regulations for bachelor degree programmes": "Academic Regulations for Bachelor Degree Programmes",
    "general academic regulations for master degree programmes": "Academic Regulations for Master Degree Programmes",
    "the student code of conduct": "The IE Student Code of Conduct",
    "student guidelines for appropriate use of ai": "Student Guidelines on AI (v4)",
    "code for the prevention of harassment in the workplace": "Code for the Prevention of Harassment",
    "ie equal opportunities and diversity plan": "Equal Opportunities and Diversity Plan",
    "ie university environmental policy": "Environmental Policy",
    "climate and sustainability plan": "Climate and Sustainability Plan (CASP v3)",
}


def canonical_source(name: str) -> str:
    name = name.strip()
    titles = {d["title"] for d in ix.CORPUS}
    if name in titles:
        return name
    key = name.lower()
    if key not in SOURCE_ALIASES:
        raise ValueError(f"Unknown expected_source {name!r}: add it to SOURCE_ALIASES in evaluate.py")
    return SOURCE_ALIASES[key]


# ---------------------------------------------------------------------------
# Expected passages
# ---------------------------------------------------------------------------
ART = re.compile(r"Art\.?\s*(\d+)(?:\.(\d+))?")
ROMAN = re.compile(r"\b([IVX]+\.\d+)((?:\.\d+)*)")
PAGE = re.compile(r"\(p\.\s*(\d+)\)")


def parse_parts(row: dict) -> list[dict]:
    """One part per expected document, each with the location strings that count."""
    sources = [s for s in re.split(r";(?! )", row["expected_source"]) if s.strip()]
    locations = [l for l in re.split(r";(?! )", row["expected_location"]) if l.strip()]
    if len(sources) == 1:
        locations = [" ; ".join(locations)]
    if len(locations) != len(sources):
        raise ValueError(f"{row['id']}: {len(sources)} sources but {len(locations)} locations")
    return [
        {"qid": row["id"], "source": canonical_source(s), "location": l.strip()} for s, l in zip(sources, locations)
    ]


def _norm(text: str) -> str:
    text = unicodedata_normalise(text).lower()
    return re.sub(r"[^a-z0-9.]+", " ", text).strip()


def unicodedata_normalise(text: str) -> str:
    import unicodedata

    return unicodedata.normalize("NFKC", text).replace("’", "'")


def location_matches(location: str, meta: dict, text: str) -> bool:
    section, heading = meta.get("section", ""), meta.get("heading", "")
    arts, romans, pages = ART.findall(location), ROMAN.findall(location), PAGE.findall(location)

    if arts or romans or pages:
        for art, sub in arts:
            if re.search(rf"\bArticle {art}\.", section) or (sub and f"{art}.{sub}." in text):
                return True
        for prefix, rest in romans:
            if f"{prefix}." in section or f"{prefix}{rest}" in text:
                return True
        for page in pages:
            if meta["page_start"] <= int(page) <= meta["page_end"]:
                return True
        return False

    # named section: any "; "-separated piece may match
    for piece in re.split(r";\s*", location):
        piece_n = _norm(piece)
        if not piece_n:
            continue
        heading_n = _norm(heading)
        if heading_n and len(heading_n) >= 4 and heading_n in piece_n:
            return True
        lead = " ".join(piece_n.split()[:3])
        if lead and (lead in _norm(section) or lead in _norm(text)):
            return True
    return False


# Where the expected location names a heading the PDF extraction lost or mangled
# (CASP's headings, the harassment code's categories, "CLASS ATTENDANCE"), the
# label cannot match any chunk metadata. For those questions a chunk from the right
# document that contains the key fact of the reference answer also counts.
EVIDENCE = {
    "q01": r"below 80%",
    "q43": r"at least once a week",
    "q45": r"grew by 64%",
    "q46": r"60% of suppliers",
}


def is_relevant(part: dict, meta: dict, text: str) -> bool:
    if meta["source"] != part["source"]:
        return False
    if location_matches(part["location"], meta, text):
        return True
    pattern = EVIDENCE.get(part.get("qid", ""))
    return bool(pattern and re.search(pattern, text))


# ---------------------------------------------------------------------------
# Retrieval
# ---------------------------------------------------------------------------
def load_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))


def query_vectors(questions: list[dict]) -> dict[str, list[float]]:
    """Embed each question once and cache it; changing designs costs nothing."""
    cache = json.loads(QUERY_CACHE.read_text()) if QUERY_CACHE.exists() else {}
    key = lambda q: f"{ix.EMBED_MODEL}|{ix.EMBED_DIM}|{q}"  # noqa: E731
    missing = [q["question"] for q in questions if key(q["question"]) not in cache]
    for start in range(0, len(missing), ix.EMBED_BATCH):
        batch = missing[start : start + ix.EMBED_BATCH]
        for q, v in zip(batch, ix.embed_texts(batch, task_type="RETRIEVAL_QUERY")):
            cache[key(q)] = v
        QUERY_CACHE.write_text(json.dumps(cache))
    return {q["question"]: cache[key(q["question"])] for q in questions}


def first_hit_rank(part: dict, results: list[tuple[dict, str]]) -> int | None:
    for rank, (meta, text) in enumerate(results, start=1):
        if is_relevant(part, meta, text):
            return rank
    return None


def evaluate_retrieval() -> list[dict]:
    questions = [q for q in load_questions() if q["kind"] != "unanswerable"]
    vectors = query_vectors(load_questions())  # embed all, the agent eval reuses them
    k_max = max(KS)
    rows, summary = [], []

    for design in ix.DESIGNS:
        collection = ix.get_collection(design)
        everything = collection.get(include=["metadatas", "documents"])
        for q in questions:
            parts = parse_parts(q)
            gold = sum(
                1
                for m, d in zip(everything["metadatas"], everything["documents"])
                if any(is_relevant(p, m, d) for p in parts)
            )
            res = collection.query(query_embeddings=[vectors[q["question"]]], n_results=k_max)
            results = list(zip(res["metadatas"][0], res["documents"][0]))
            ranks = [first_hit_rank(p, results) for p in parts]
            found = [r for r in ranks if r is not None]
            row = {
                "design": design,
                "id": q["id"],
                "kind": q["kind"],
                "gold_chunks": gold,
                "first_hit_rank": min(found) if found else "",
                "all_parts_rank": max(ranks) if all(r is not None for r in ranks) else "",
                "top1": f"{results[0][0]['source']} | {results[0][0]['location']}",
            }
            for k in KS:
                row[f"hit@{k}"] = int(bool(found) and min(found) <= k)
                row[f"full@{k}"] = int(all(r is not None and r <= k for r in ranks))
            for k in (3, 5):
                row[f"words@{k}"] = sum(len(d.split()) for _, d in results[:k])
            rows.append(row)

        mine = [r for r in rows if r["design"] == design]
        for kind in ("all", "single", "multi"):
            sel = mine if kind == "all" else [r for r in mine if r["kind"] == kind]
            line = {"design": design, "questions": kind, "n": len(sel)}
            for k in KS:
                line[f"hit@{k}"] = round(sum(r[f"hit@{k}"] for r in sel) / len(sel), 3)
            if kind == "multi":
                for k in KS:
                    line[f"full@{k}"] = round(sum(r[f"full@{k}"] for r in sel) / len(sel), 3)
            for k in (3, 5):
                line[f"avg_words@{k}"] = round(sum(r[f"words@{k}"] for r in sel) / len(sel))
            summary.append(line)

    write_csv(EVAL_DIR / "retrieval_per_question.csv", rows)
    write_csv(EVAL_DIR / "retrieval_summary.csv", summary)
    print_summary(summary)
    no_gold = sorted({(r["id"], r["design"]) for r in rows if r["gold_chunks"] == 0})
    if no_gold:
        print(f"\nWARNING: no chunk matches the expected location for: {no_gold}")
    return summary


def write_csv(path: Path, rows: list[dict]) -> None:
    fields = list(dict.fromkeys(k for r in rows for k in r))
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def print_summary(summary: list[dict]) -> None:
    print("\nRetrieval hit rate (answerable questions)")
    print(f"{'design':12} {'questions':9} {'n':>3}  {'hit@1':>6} {'hit@3':>6} {'hit@5':>6}  {'full@5':>6}  {'words@3':>7} {'words@5':>7}")
    for s in summary:
        full = f"{s['full@5']:.2f}" if "full@5" in s else ""
        print(
            f"{s['design']:12} {s['questions']:9} {s['n']:>3}  {s['hit@1']:>6.2f} {s['hit@3']:>6.2f} {s['hit@5']:>6.2f}"
            f"  {full:>6}  {s['avg_words@3']:>7} {s['avg_words@5']:>7}"
        )


def main() -> None:
    evaluate_retrieval()
    # TODO part 2: end-to-end evaluation of agent answers.


if __name__ == "__main__":
    main()
