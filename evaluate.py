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


def covers_holding(meta: dict, target: dict) -> bool:
    """'Holding' match: the exact passage, or the Leitsatz of the expected judgment (statutes: exact only)."""
    if covers(meta, target):
        return True
    return "rn" in target and meta.get("doc_id") == target["doc_id"] and "|Leitsatz|" in meta.get("covers", "")


def targets_of(expected_location: str) -> list[dict]:
    return [parse_location(part) for part in expected_location.split(";") if part.strip()]


def hits_at_k(retrieved: list[dict], expected_location: str, ks=KS, match=covers) -> dict:
    """Hit at each k for one question, given the retrieved chunks' metadata in rank order.

    'all': every expected passage is covered within the top k (the headline number; for
    single questions it equals 'any'). 'any': at least one is. `match` is covers (exact
    passage) or covers_holding (passage or the judgment's Leitsatz).
    """
    targets = targets_of(expected_location)
    found_at = [next((rank for rank, meta in enumerate(retrieved, 1) if match(meta, t)), None) for t in targets]
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


# ---------------------------------------------------------------- retrieval evaluation

CACHE_DIR = ROOT / "eval" / "cache"
RETRIEVAL_JSON = ROOT / "eval" / "retrieval_results.json"
RETRIEVAL_MD = ROOT / "eval" / "retrieval_results.md"
DESIGNS = {"A": "baseline (EN → dense)", "B": "translated (DE → dense)", "C": "hybrid (DE → BM25 + dense, RRF)",
           "D": "hybrid, max 2 chunks/doc"}
METRICS = {"exact": "exact passage", "holding": "holding (passage or Leitsatz)"}


def load_questions(path: Path = QUESTIONS) -> list[dict]:
    with path.open(newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r["question"].strip()]


def _rate(flags: list[bool]) -> float:
    return sum(flags) / len(flags) if flags else float("nan")


def evaluate_retrieval() -> dict:
    import retrieval  # needs the API key; imported here so the matching helpers work without it

    questions = [q for q in load_questions() if q["kind"].strip().lower() != "unanswerable"]
    corpus = retrieval.Corpus()
    translations = retrieval.JsonCache(CACHE_DIR / "translations.json")
    embeddings = retrieval.JsonCache(CACHE_DIR / "query_embeddings.json")

    per_question: dict[str, list[dict]] = {d: [] for d in DESIGNS}
    for design in DESIGNS:
        for q in questions:
            res = retrieval.search(corpus, q["question"], design, k=max(KS),
                                   translations=translations, embeddings=embeddings)
            chunks = res["chunks"]
            per_question[design].append({
                "id": q["id"], "kind": q["kind"], "question": q["question"], "query": res["query"],
                "expected": q["expected_location"],
                "hits": hits_at_k(chunks, q["expected_location"]),
                "hits_holding": hits_at_k(chunks, q["expected_location"], match=covers_holding),
                "words": {k: sum(len(c["text"].split()) for c in chunks[:k]) for k in KS},
                "retrieved": [c["location"] for c in chunks],
            })

    summary = {}
    for design, rows in per_question.items():
        single = [r for r in rows if r["kind"] == "single"]
        multi = [r for r in rows if r["kind"] == "multi"]
        summary[design] = {"words": {k: sum(r["words"][k] for r in rows) / len(rows) for k in KS}}
        for metric, field in (("exact", "hits"), ("holding", "hits_holding")):
            summary[design][metric] = {
                "overall": {k: _rate([r[field][k]["all"] for r in rows]) for k in KS},
                "single": {k: _rate([r[field][k]["all"] for r in single]) for k in KS},
                "multi_all": {k: _rate([r[field][k]["all"] for r in multi]) for k in KS},
                "multi_any": {k: _rate([r[field][k]["any"] for r in multi]) for k in KS},
            }

    calls = [translations.get(retrieval._key(retrieval.TRANSLATE_MODEL, "thinking=low", retrieval.TRANSLATE_PROMPT, q["question"]))
             for q in questions]
    translation_cost = {
        "model": retrieval.TRANSLATE_MODEL,
        "questions": len(calls),
        "input_tokens_avg": sum(c["input_tokens"] for c in calls) / len(calls),
        "output_tokens_avg": sum(c["output_tokens"] for c in calls) / len(calls),
        "seconds_avg": sum(c["seconds"] for c in calls) / len(calls),
        "seconds_max": max(c["seconds"] for c in calls),
    }
    result = {
        "n": {"answerable": len(questions), "single": sum(q["kind"] == "single" for q in questions),
              "multi": sum(q["kind"] == "multi" for q in questions)},
        "summary": summary, "translation": translation_cost, "per_question": per_question,
    }
    RETRIEVAL_JSON.write_text(json.dumps(result, ensure_ascii=False, indent=1), encoding="utf-8")
    RETRIEVAL_MD.write_text(retrieval_report(result), encoding="utf-8")
    return result


def retrieval_report(result: dict) -> str:
    n, s = result["n"], result["summary"]
    pct = lambda x: f"{100 * x:.0f}%"  # noqa: E731
    lines = [
        f"# Retrieval evaluation\n\n{n['answerable']} answerable questions ({n['single']} single, {n['multi']} multi). "
        "Multi (all) = every expected passage within top k; (any) = at least one. "
        "Exact = a chunk covers the expected Rn./§. Holding = that, or the expected judgment's Leitsatz "
        "(statute targets: exact only).\n",
        "| Design | k | Exact: overall | single | multi all | multi any | Holding: overall | single | multi all | multi any | Words added |",
        "|---|---|---|---|---|---|---|---|---|---|---|",
    ]
    for d, name in DESIGNS.items():
        for k in KS:
            e, h = s[d]["exact"], s[d]["holding"]
            cells = [pct(m[c][k]) for m in (e, h) for c in ("overall", "single", "multi_all", "multi_any")]
            lines.append(f"| {d} {name} | {k} | " + " | ".join(cells) + f" | {s[d]['words'][k]:.0f} |")
    lines.append(
        "\nChosen design: B at k=5 (retrieval.DEFAULT_DESIGN), on the holding metric: the agent can answer and cite "
        "from a judgment's Leitsatz, and B leads there with fewer words than C. A, C and D are kept as compared designs."
    )
    t = result["translation"]
    lines.append(
        f"\nTranslation step (B, C): {t['model']}, avg {t['input_tokens_avg']:.0f} input + {t['output_tokens_avg']:.0f} "
        f"output tokens, avg {t['seconds_avg']:.1f} s (max {t['seconds_max']:.1f} s) per question, measured on the first "
        "uncached call. BM25 + RRF run locally (milliseconds)."
    )
    return "\n".join(lines) + "\n"


def misses(result: dict, design: str, k: int = max(KS)) -> str:
    out = []
    for r in result["per_question"][design]:
        if r["hits"][k]["all"]:
            continue
        partial = " (partial: one of two found)" if r["hits"][k]["any"] else ""
        out.append(f"{r['id']} [{r['kind']}]{partial} {r['question']}\n"
                   f"   expected : {r['expected']}\n   query    : {r['query']}\n"
                   + "\n".join(f"   #{i} {loc}" for i, loc in enumerate(r["retrieved"], 1)))
    return "\n\n".join(out) or "none"


def main() -> None:
    problems = validate_test_set()
    print("test set locations OK" if not problems else "\n".join(problems))
    result = evaluate_retrieval()
    print("\n" + retrieval_report(result))
    best = max(DESIGNS, key=lambda d: tuple(result["summary"][d]["exact"]["overall"][k] for k in sorted(KS, reverse=True)))
    print(f"Exact-passage misses at k={max(KS)} for the design with the highest exact hit rate at k=5 "
          f"(ties: k=3, k=1): {best}\n")
    print(misses(result, best))
    print("\nEnd-to-end evaluation (agent answers, judge, human agreement) is not written yet.")


if __name__ == "__main__":
    main()
