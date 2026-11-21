"""
Assignment 3: evaluation (`main.py evaluate`).

Part 1 - retrieval: hit rate at k = 1, 3, 5 for each chunking design, on the
answerable questions of eval/questions.csv. A retrieved chunk is a hit for an
expected passage when it comes from the expected document and its page range
includes the expected page. `multi` questions are strict (both passages must
be in the top k); the partial score (share of passages found) is also saved.

Part 2 - end to end (agent answers, code checks, LLM judge, agreement with
eval/human_labels.csv): to be added once agent.py exists.

Outputs (committed):
    eval/retrieval_results.csv   one row per question and design
    eval/retrieval_summary.md    hit-rate tables per design
"""

from __future__ import annotations

import csv
from pathlib import Path

import index as ix
from retrieval import search

ROOT = Path(__file__).resolve().parent
EVAL_DIR = ROOT / "eval"
QUESTIONS = EVAL_DIR / "questions.csv"
KS = (1, 3, 5)


def load_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r["question"].strip()]


def expected_passages(q: dict) -> list[tuple[str, int]]:
    docs = [d.strip() for d in q["expected_source"].split(";") if d.strip()]
    pages = [int(p) for p in q["expected_location"].split(";") if p.strip()]
    if len(docs) != len(pages):
        raise ValueError(f"{q['id']}: expected_source and expected_location differ in length")
    return list(zip(docs, pages))


def covers(chunk: dict, passage: tuple[str, int]) -> bool:
    doc, page = passage
    return chunk["doc_id"] == doc and chunk["page"] <= page <= chunk["page_end"]


def first_rank(hits: list[dict], passage: tuple[str, int]) -> int | None:
    """1-based rank of the first chunk covering the passage, or None."""
    for rank, chunk in enumerate(hits, start=1):
        if covers(chunk, passage):
            return rank
    return None


def evaluate_retrieval(designs: list[str] = ix.DESIGNS) -> list[dict]:
    questions = load_questions()
    # embed every question once (cached); unanswerable ones are reused later
    ix.embed_texts([q["question"] for q in questions], "RETRIEVAL_QUERY")
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    rows = []
    for design in designs:
        for q in answerable:
            passages = expected_passages(q)
            hits = search(q["question"], k=max(KS), design=design)
            ranks = [first_rank(hits, p) for p in passages]
            row = {
                "design": design, "id": q["id"], "kind": q["kind"],
                "expected": "; ".join(f"{d} p.{p}" for d, p in passages),
                "ranks": "; ".join(str(r) if r else "-" for r in ranks),
                "top1": f"{hits[0]['doc_id']} p.{hits[0]['page']}"
                        + (f"-{hits[0]['page_end']}" if hits[0]["page_end"] != hits[0]["page"] else ""),
            }
            for k in KS:
                found = [r is not None and r <= k for r in ranks]
                row[f"hit@{k}"] = int(all(found))
                row[f"partial@{k}"] = round(sum(found) / len(found), 2)
                row[f"words@{k}"] = sum(len(h["text"].split()) for h in hits[:k])
            rows.append(row)
    return rows


def summarise(rows: list[dict]) -> str:
    def mean(xs):
        return sum(xs) / len(xs) if xs else 0.0

    designs = list(dict.fromkeys(r["design"] for r in rows))
    out = ["# Retrieval evaluation", "",
           "Hit = a top-k chunk from the expected document whose pages include the expected page. "
           "`multi` is strict (both passages in the top k); partial = share of passages found.", ""]

    out += ["## Hit rate (all answerable questions)", "",
            "| Design | n | hit@1 | hit@3 | hit@5 | words@1 | words@3 | words@5 |",
            "|---|---|---|---|---|---|---|---|"]
    for d in designs:
        rs = [r for r in rows if r["design"] == d]
        out.append(f"| {d} | {len(rs)} | " + " | ".join(f"{mean([r[f'hit@{k}'] for r in rs]):.0%}" for k in KS)
                   + " | " + " | ".join(f"{mean([r[f'words@{k}'] for r in rs]):.0f}" for k in KS) + " |")

    out += ["", "## By question kind", "",
            "| Design | kind | n | hit@1 | hit@3 | hit@5 | partial@1 | partial@3 | partial@5 |",
            "|---|---|---|---|---|---|---|---|---|"]
    for d in designs:
        for kind in ("single", "multi"):
            rs = [r for r in rows if r["design"] == d and r["kind"] == kind]
            if rs:
                out.append(f"| {d} | {kind} | {len(rs)} | "
                           + " | ".join(f"{mean([r[f'hit@{k}'] for r in rs]):.0%}" for k in KS) + " | "
                           + " | ".join(f"{mean([r[f'partial@{k}'] for r in rs]):.0%}" for k in KS) + " |")

    out += ["", "## Misses at k = 5", ""]
    for d in designs:
        misses = [r for r in rows if r["design"] == d and not r["hit@5"]]
        out.append(f"- **{d}**: " + (", ".join(f"{r['id']} (expected {r['expected']}, ranks {r['ranks']}, "
                                               f"top-1 {r['top1']})" for r in misses) or "none"))
    return "\n".join(out) + "\n"


def run_retrieval() -> None:
    rows = evaluate_retrieval()
    with (EVAL_DIR / "retrieval_results.csv").open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    summary = summarise(rows)
    (EVAL_DIR / "retrieval_summary.md").write_text(summary, encoding="utf-8")
    print(summary)


if __name__ == "__main__":
    run_retrieval()
    print("End-to-end evaluation: not written yet (needs agent.py).")
