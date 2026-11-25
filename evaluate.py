"""
Assignment 3: evaluation (`main.py evaluate`).

Stage 1 - retrieval: hit rate at k = 1, 3, 5 for each chunking design in
index.DESIGNS, using every answerable question in eval/questions.csv.

  A retrieved chunk is a hit for an expected (source, location) when it comes
  from that drug's label and covers that section: location "7" matches 7,
  7.1, 7.2...; "7.3" matches 7.3. Fixed windows can span several sections and
  count for each section they touch.
  single questions: hit@k = the expected passage is in the top k.
  multi questions:  hit@k = ALL expected passages are in the top k (strict),
                    plus "any@k" = at least one of them.

Writes eval/retrieval_results.csv (one row per question and design) and
eval/retrieval_summary.md. Query vectors are cached in index/, so reruns cost
no embedding quota.

Stage 2 - end to end (agent answers, code checks, LLM judge, agreement with
eval/human_labels.csv) is added once agent.py exists.
"""

from __future__ import annotations

import csv
import json
import statistics
import sys
from pathlib import Path

import index

ROOT = Path(__file__).resolve().parent
EVAL_DIR = ROOT / "eval"
QUESTIONS = EVAL_DIR / "questions.csv"
KS = (1, 3, 5)


def log(*args) -> None:
    print(*args, flush=True)


def load_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if (r.get("question") or "").strip()]
    for r in rows:
        r["kind"] = r["kind"].strip().lower()
        sources = [s.strip().lower() for s in r["expected_source"].split(";") if s.strip()]
        locations = [s.strip() for s in r["expected_location"].split(";") if s.strip()]
        r["expected"] = list(zip(sources, locations))
    return rows


def covers(hit: dict, source: str, location: str) -> bool:
    if hit["source"] != source:
        return False
    sections = [s for s in hit["sections"].split(",") if s]
    return any(s == location or s.startswith(location + ".") for s in sections)


def first_rank(hits: list[dict], source: str, location: str) -> int | None:
    """1-based rank of the first hit covering this passage, or None."""
    return next((i for i, h in enumerate(hits, 1) if covers(h, source, location)), None)


# --------------------------------------------------------------------------
# Stage 1: retrieval
# --------------------------------------------------------------------------

def evaluate_retrieval(questions: list[dict]) -> list[dict]:
    rows = []
    kmax = max(KS)
    for design in index.DESIGNS:
        for q in questions:
            hits = index.search(q["question"], k=kmax, design=design)
            row = {
                "design": design,
                "id": q["id"],
                "kind": q["kind"],
                "top1_score": hits[0]["score"] if hits else 0.0,
                "top5_words": sum(h["words"] for h in hits),
                "retrieved": " | ".join(f"{h['source']} {h['location'][:40]} ({h['score']:.2f})" for h in hits),
            }
            if q["kind"] != "unanswerable":
                ranks = [first_rank(hits, s, loc) for s, loc in q["expected"]]
                row["ranks"] = ";".join(str(r) if r else "-" for r in ranks)
                for k in KS:
                    found = [r is not None and r <= k for r in ranks]
                    row[f"hit@{k}"] = int(all(found))
                    row[f"any@{k}"] = int(any(found))
                found_ranks = [r for r in ranks if r]
                row["rr"] = 1 / min(found_ranks) if found_ranks else 0.0
            rows.append(row)
    return rows


def summarize_retrieval(rows: list[dict]) -> str:
    def mean(values):
        values = list(values)
        return statistics.mean(values) if values else float("nan")

    lines = [
        "# Retrieval results",
        "",
        "Hit@k: the expected passage is among the top k chunks (multi: all expected passages).",
        "Any@k (multi only): at least one expected passage in the top k. MRR: mean reciprocal rank of the first hit.",
        "Prompt words: words the top 5 chunks add to the prompt.",
        "",
        "| Design | Questions | Hit@1 | Hit@3 | Hit@5 | MRR | Multi any@5 | Prompt words (top 5) | Top-1 score answerable | Top-1 score unanswerable |",
        "|---|---|---|---|---|---|---|---|---|---|",
    ]
    for design in index.DESIGNS:
        mine = [r for r in rows if r["design"] == design]
        answerable = [r for r in mine if r["kind"] != "unanswerable"]
        multi = [r for r in answerable if r["kind"] == "multi"]
        unanswerable = [r for r in mine if r["kind"] == "unanswerable"]
        cells = [design, str(len(answerable))]
        cells += [f"{mean(r[f'hit@{k}'] for r in answerable):.2f}" for k in KS]
        cells.append(f"{mean(r['rr'] for r in answerable):.2f}")
        cells.append(f"{mean(r['any@5'] for r in multi):.2f}" if multi else "n/a")
        cells.append(f"{mean(r['top5_words'] for r in mine):.0f}")
        cells.append(f"{mean(r['top1_score'] for r in answerable):.3f}")
        cells.append(f"{mean(r['top1_score'] for r in unanswerable):.3f}" if unanswerable else "n/a")
        lines.append("| " + " | ".join(cells) + " |")

    lines += ["", "## By kind", "", "| Design | Kind | n | Hit@1 | Hit@3 | Hit@5 |", "|---|---|---|---|---|---|"]
    for design in index.DESIGNS:
        for kind in ("single", "multi"):
            group = [r for r in rows if r["design"] == design and r["kind"] == kind]
            if group:
                lines.append(f"| {design} | {kind} | {len(group)} | "
                             + " | ".join(f"{mean(r[f'hit@{k}'] for r in group):.2f}" for k in KS) + " |")

    misses = [r for r in rows if r["kind"] != "unanswerable" and not r["hit@5"]]
    lines += ["", "## Misses at k=5", ""]
    lines += [f"- {r['design']} {r['id']} (expected ranks {r['ranks']}): {r['retrieved']}" for r in misses] or ["- none"]
    return "\n".join(lines) + "\n"


def write_csv(path: Path, rows: list[dict]) -> None:
    fields = list(dict.fromkeys(k for r in rows for k in r))
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=fields)
        writer.writeheader()
        writer.writerows(rows)


def main() -> None:
    questions = load_questions()
    kinds = [q["kind"] for q in questions]
    log(f"{len(questions)} questions: " + ", ".join(f"{kinds.count(k)} {k}" for k in sorted(set(kinds))))

    log("\n== Stage 1: retrieval ==")
    rows = evaluate_retrieval(questions)
    write_csv(EVAL_DIR / "retrieval_results.csv", rows)
    summary = summarize_retrieval(rows)
    (EVAL_DIR / "retrieval_summary.md").write_text(summary, encoding="utf-8")
    log(summary)


if __name__ == "__main__":
    sys.exit(main())
