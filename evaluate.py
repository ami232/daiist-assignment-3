"""
Assignment 3: evaluation (`main.py evaluate`).

Stage 1, retrieval (this file so far): for every test question and each
retrieval design (structure, fixed, structure-diverse), does the right
passage reach the top k?

    hit@k (single)          a top-k chunk is from the expected page AND holds
                            at least 30 words of the expected section (or all
                            of it, if the section is shorter)
    hit@k (multi, strict)   every expected passage is in the top k
    hit@k (multi, partial)  at least one expected passage is in the top k
    words@k                 words the top k chunks would add to the prompt

Unanswerable questions have no right passage, so they are left out of hit
rate. Instead we compare their best similarity score with the answerable
questions' scores: if they are clearly lower, a score threshold could help
the agent refuse.

Question vectors are cached in index/query_vectors.json, so after the first
run this stage costs no API calls.

Outputs in eval/: retrieval_results.csv (one row per question and design)
and retrieval_summary.json.
"""

import csv
import json
import statistics
from pathlib import Path

import index as ix

ROOT = Path(__file__).resolve().parent
EVAL_DIR = ROOT / "eval"
QUESTIONS = EVAL_DIR / "questions.csv"
RETRIEVAL_RESULTS = EVAL_DIR / "retrieval_results.csv"
RETRIEVAL_SUMMARY = EVAL_DIR / "retrieval_summary.json"

KS = (1, 3, 5)
TOP = max(KS)
MIN_PASSAGE_WORDS = 30  # a chunk must hold this much of a section to count as containing it
DESIGNS = list(ix.RETRIEVAL_DESIGNS)


def load_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        rows = [r for r in csv.DictReader(f) if r["question"].strip()]
    for r in rows:
        r["kind"] = r["kind"].strip().lower()
        sources = [s.strip() for s in r["expected_source"].split(";") if s.strip()]
        locations = [l.strip() for l in r["expected_location"].split(";") if l.strip()]
        if len(sources) != len(locations):
            raise ValueError(f"{r['id']}: expected_source and expected_location must pair up")
        r["expected"] = list(zip(sources, locations))
    return rows


# ============================================================================
# Matching a retrieved chunk against an expected passage
# ============================================================================

_section_totals: dict[str, dict[str, int]] = {}


def within(section: str, location: str) -> bool:
    """The section is the expected location itself or one of its sub-sections."""
    return section == location or section.startswith(location + ix.SEPARATOR)


def words_needed(source: str, location: str) -> int:
    """MIN_PASSAGE_WORDS, or the whole section's size if it is shorter."""
    if source not in _section_totals:
        _section_totals[source] = ix.section_word_totals(ix.local_path(source))
    total = sum(n for s, n in _section_totals[source].items() if within(s, location))
    return max(1, min(MIN_PASSAGE_WORDS, total))


def contains_passage(chunk: dict, source: str, location: str, touch: bool = False) -> bool:
    """True if the chunk is from `source` and holds the section `location`.

    Default rule: the chunk holds at least MIN_PASSAGE_WORDS body words of
    the section (sub-sections included), counted from its `section_words`
    metadata. touch=True is the first, lenient rule: any overlap at all,
    even the last line of a section, counts. It favoured fixed windows,
    which span 2.7 sections on average against 1.1 for structure chunks.
    """
    if chunk["source"] != source:
        return False
    if touch:
        return any(within(s, location) for s in chunk["sections"].split(" | "))
    held = sum(n for s, n in json.loads(chunk["section_words"]).items() if within(s, location))
    return held >= words_needed(source, location)


def first_rank(results: list[dict], source: str, location: str, touch: bool = False) -> int | None:
    """1-based rank of the first chunk containing this passage, or None."""
    for rank, chunk in enumerate(results, start=1):
        if contains_passage(chunk, source, location, touch):
            return rank
    return None


# ============================================================================
# Stage 1: retrieval
# ============================================================================

def retrieval_stage(questions: list[dict]) -> dict:
    rows = []
    for q in questions:
        vector = ix.embed_query(q["question"])  # one embedding per question, cached on disk
        for design in DESIGNS:
            results = ix.retrieve(vector, k=TOP, design=design)
            ranks = [first_rank(results, s, l) for s, l in q["expected"]]
            found = [r for r in ranks if r is not None]
            touch_ranks = [first_rank(results, s, l, touch=True) for s, l in q["expected"]]
            row = {
                "id": q["id"],
                "kind": q["kind"],
                "design": design,
                # rank where the FIRST expected passage appears (partial hit)
                "rank_any": min(found) if found else "",
                # rank where ALL expected passages have appeared (strict hit)
                "rank_all": max(ranks) if ranks and None not in ranks else "",
                # same, with the first lenient rule (kept to show its bias)
                "rank_all_touch": max(touch_ranks) if touch_ranks and None not in touch_ranks else "",
                "top_score": results[0]["score"],
                "top1": f"{results[0]['source']} › {results[0]['location']}",
            }
            for k in KS:
                row[f"words@{k}"] = sum(c["words"] for c in results[:k])
            rows.append(row)

    with RETRIEVAL_RESULTS.open("w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0]))
        writer.writeheader()
        writer.writerows(rows)

    summary = {d: summarise(rows, d) for d in DESIGNS}
    RETRIEVAL_SUMMARY.write_text(json.dumps(summary, indent=2), encoding="utf-8")
    print_summary(summary, len(questions))
    return summary


def hit_rate(rows: list[dict], k: int, column: str) -> float:
    return sum(1 for r in rows if r[column] != "" and r[column] <= k) / len(rows) if rows else float("nan")


def summarise(rows: list[dict], design: str) -> dict:
    mine = [r for r in rows if r["design"] == design]
    answerable = [r for r in mine if r["kind"] != "unanswerable"]
    single = [r for r in mine if r["kind"] == "single"]
    multi = [r for r in mine if r["kind"] == "multi"]
    unanswerable = [r for r in mine if r["kind"] == "unanswerable"]

    def score_stats(group):
        scores = [r["top_score"] for r in group]
        return {"mean": round(statistics.mean(scores), 3), "min": min(scores), "max": max(scores)}

    return {
        "n_answerable": len(answerable),
        "hit": {
            f"@{k}": {
                "all_answerable": round(hit_rate(answerable, k, "rank_all"), 3),
                "single": round(hit_rate(single, k, "rank_all"), 3),
                "multi_strict": round(hit_rate(multi, k, "rank_all"), 3),
                "multi_partial": round(hit_rate(multi, k, "rank_any"), 3),
                "all_answerable_touch_rule": round(hit_rate(answerable, k, "rank_all_touch"), 3),
            }
            for k in KS
        },
        # mean reciprocal rank: 1 if the right chunk is first, 1/2 if second... 0 if not in top 5
        "mrr_single": round(statistics.mean(1 / r["rank_all"] if r["rank_all"] != "" else 0 for r in single), 3),
        "words_added": {f"@{k}": round(statistics.mean(r[f"words@{k}"] for r in mine)) for k in KS},
        "top_score_answerable": score_stats(answerable),
        "top_score_unanswerable": score_stats(unanswerable),
        "misses_at_5": [r["id"] for r in answerable if r["rank_all"] == ""],
    }


def print_summary(summary: dict, n: int) -> None:
    width = 30 + 7 * len(KS) * len(DESIGNS)
    print("=" * width)
    print(f"RETRIEVAL: {n} questions, {summary[DESIGNS[0]]['n_answerable']} answerable")
    print("=" * width)
    print(f"{'':<30}" + "".join(f"{d:^{7 * len(KS)}}" for d in DESIGNS))
    print(f"{'':<30}" + "".join(f"{'@' + str(k):>7}" for _ in DESIGNS for k in KS))
    for label, key in [("hit rate, all answerable", "all_answerable"), ("  single", "single"),
                       ("  multi (both passages)", "multi_strict"), ("  multi (at least one)", "multi_partial"),
                       ("old rule: chunk touches section", "all_answerable_touch_rule")]:
        cells = "".join(f"{summary[d]['hit']['@' + str(k)][key]:>7.0%}" for d in DESIGNS for k in KS)
        print(f"{label:<30}{cells}")
    cells = "".join(f"{summary[d]['words_added']['@' + str(k)]:>7}" for d in DESIGNS for k in KS)
    print(f"{'words added to prompt':<30}{cells}")
    print("=" * width)
    for d in DESIGNS:
        s = summary[d]
        print(f"{d}: MRR (single) {s['mrr_single']:.3f}; best score answerable "
              f"{s['top_score_answerable']['mean']:.3f} (min {s['top_score_answerable']['min']:.3f}), "
              f"unanswerable {s['top_score_unanswerable']['mean']:.3f} "
              f"(max {s['top_score_unanswerable']['max']:.3f}); missed at 5: {', '.join(s['misses_at_5']) or 'none'}")


def main() -> None:
    questions = load_questions()
    retrieval_stage(questions)


if __name__ == "__main__":
    main()
