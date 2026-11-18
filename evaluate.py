"""
Assignment 3: evaluation (`main.py evaluate`).

Part 1 (this file so far): retrieval hit rate at k = 1, 3, 5 for every design:
2 chunkings (structure, fixed) x 3 search methods (dense, bm25, hybrid).

A retrieved chunk "hits" a passage when it comes from the expected document and
contains the expected article / disposición / anexo. A `single` question is a hit
at k if any expected passage is in the top k; a `multi` question only if all of
them are. Unanswerable questions have no passage and are left out.

Writes eval/retrieval_per_question.csv and eval/retrieval_summary.csv.
Query vectors are cached in eval/query_vectors.json, so re-runs cost no quota.
"""

import csv
import json
import re
from pathlib import Path

import index
import retrieve

ROOT = Path(__file__).resolve().parent
EVAL_DIR = ROOT / "eval"
QUESTIONS = EVAL_DIR / "questions.csv"
QUERY_CACHE = EVAL_DIR / "query_vectors.json"
DESIGNS = [(s, m) for s in ("structure", "fixed") for m in ("dense", "bm25", "hybrid")]
KS = (1, 3, 5)


def load_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r["question"].strip()]


def query_vectors(questions: list[dict]) -> dict[str, list[float]]:
    """Embed each question once and keep the vectors in eval/query_vectors.json."""
    cache = json.loads(QUERY_CACHE.read_text()) if QUERY_CACHE.exists() else {}
    missing = [q["question"] for q in questions if q["question"] not in cache]
    for i in range(0, len(missing), index.EMBED_BATCH):
        batch = missing[i:i + index.EMBED_BATCH]
        cache.update(zip(batch, index.embed_texts(batch, task_type="RETRIEVAL_QUERY")))
        QUERY_CACHE.write_text(json.dumps(cache))
    return cache


def unit_labels(location: str) -> set[str]:
    """'art. 9 bis.1' -> {'artículo 9 bis'}; 'art. 1.1 y Anexo' -> {'artículo 1', 'anexo'};
    'disposición transitoria segunda.2' -> {'disposición transitoria segunda'}."""
    location = re.sub(r"\(.*?\)", "", location.lower())
    labels = {f"artículo {n}" for n in re.findall(r"art\.?\s*(\d+(?: (?:bis|ter|quater))?)", location)}
    labels |= {f"disposición {d.strip()}" for d in re.findall(
        r"disposición ((?:adicional|transitoria|derogatoria|final)(?: [a-záéíóúñ]+)*)", location)}
    if "anexo" in location:
        labels.add("anexo")
    return labels


def expected_passages(q: dict) -> list[tuple[str, set[str]]]:
    """[(source, acceptable unit labels)] per passage; sources pair with locations by position."""
    sources = [s.strip() for s in q["expected_source"].split(";") if s.strip()]
    locations = [l.strip() for l in q["expected_location"].split(";") if l.strip()]
    passages = []
    for i, location in enumerate(locations):
        labels = unit_labels(location)
        if labels:   # e.g. "encabezado" names no article: nothing to match
            passages.append((sources[min(i, len(sources) - 1)], labels))
    return passages


def chunk_units(metadata: dict) -> set[str]:
    units = metadata.get("articles") or metadata.get("article", "")
    return {u.lower() for u in units.split("|")}


def first_hit_rank(passage: tuple[str, set[str]], results: list[dict]) -> int | None:
    source, labels = passage
    for rank, r in enumerate(results, start=1):
        if r["metadata"]["source"] == source and chunk_units(r["metadata"]) & labels:
            return rank
    return None


def retrieval_eval(questions: list[dict]) -> list[dict]:
    answerable = [q for q in questions if q["kind"].strip() != "unanswerable"]
    vectors = query_vectors(answerable)
    rows, summary = [], []
    for strategy, method in DESIGNS:
        design = f"{strategy}+{method}"
        for q in answerable:
            results = retrieve.search(q["question"], k=max(KS), strategy=strategy, method=method,
                                      query_vector=vectors[q["question"]])
            ranks = [first_hit_rank(p, results) for p in expected_passages(q)]
            # rank at which the question is satisfied: any passage (single) or all (multi)
            if q["kind"].strip() == "multi":
                needed = None if None in ranks else max(ranks)
            else:
                needed = min((r for r in ranks if r), default=None)
            row = {"design": design, "id": q["id"], "kind": q["kind"], "rank": needed or ""}
            row.update({f"hit@{k}": int(needed is not None and needed <= k) for k in KS})
            row["top5"] = " | ".join(r["metadata"]["citation"] for r in results)
            rows.append(row)
        for kind in ("all", "single", "multi"):
            sel = [r for r in rows if r["design"] == design and kind in ("all", r["kind"])]
            summary.append({"design": design, "questions": kind, "n": len(sel),
                            **{f"hit@{k}": round(sum(r[f"hit@{k}"] for r in sel) / len(sel), 3) for k in KS}})

    write_csv(EVAL_DIR / "retrieval_per_question.csv", rows)
    write_csv(EVAL_DIR / "retrieval_summary.csv", summary)
    print("\nRetrieval hit rate (answerable questions)\n")
    print(f"{'design':<20}{'questions':<10}{'n':>4}" + "".join(f"{f'hit@{k}':>8}" for k in KS))
    for s in summary:
        print(f"{s['design']:<20}{s['questions']:<10}{s['n']:>4}" + "".join(f"{s[f'hit@{k}']:>8.2f}" for k in KS))
    return summary


def write_csv(path: Path, rows: list[dict]) -> None:
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    questions = load_questions()
    retrieval_eval(questions)
    # Part 2 (step 8): agent answers, code checks, LLM judge, agreement with human labels.


if __name__ == "__main__":
    main()
