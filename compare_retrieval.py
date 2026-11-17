"""
Step 5: compare retrieval designs on the test set (eval/questions.csv).

For every answerable question we know which article(s) answer it. A search is a
HIT AT k if the right passage is among the k best chunks it returns. For a
`multi` question, both passages must be there ("all"); we also show "any".

Designs compared (all search the same embeddings; no extra embedding cost):
  A  fixed windows of 150 words        B  one chunk per article/section
  each with: vector search, and hybrid (vector + keywords).  B+keywords alone is a reference.

Question vectors are saved in eval/question_vectors.jsonl, so only new or edited
questions are ever embedded.   Run:  uv run python compare_retrieval.py
"""

import csv
import hashlib
import json
import statistics

import numpy as np

import index as ix
from retrieval import Retriever

QUESTIONS = ix.ROOT / "eval" / "questions.csv"
QUESTION_VECTORS = ix.ROOT / "eval" / "question_vectors.jsonl"
RESULTS_CSV = ix.ROOT / "eval" / "retrieval_results.csv"
SUMMARY_JSON = ix.ROOT / "eval" / "retrieval_summary.json"
TOP = 10  # ranks looked at; hit@5 is the largest k reported
CONFIGS = [  # (label, design, mode)
    ("A fixed + vector", "A", "vector"),
    ("B sections + vector", "B", "vector"),
    ("A fixed + hybrid", "A", "hybrid"),
    ("B sections + hybrid", "B", "hybrid"),
    ("B sections + keywords only", "B", "bm25"),
]


def read_questions() -> list[dict]:
    with QUESTIONS.open(newline="", encoding="utf-8") as f:
        return [r for r in csv.DictReader(f) if r["question"].strip()]


def question_key(text: str) -> str:
    return hashlib.sha1(f"{ix.EMBED_MODEL}|{ix.EMBED_DIM}|{ix.query_input(text)}".encode()).hexdigest()[:16]


def load_question_vectors(questions: list[dict], client=None) -> dict[str, np.ndarray]:
    """question text -> unit vector; embeds (and saves at once) only the ones not saved yet."""
    saved = {}
    if QUESTION_VECTORS.exists():
        for line in QUESTION_VECTORS.open(encoding="utf-8"):
            try:
                r = json.loads(line)
                saved[r["key"]] = r["vector"]
            except (json.JSONDecodeError, KeyError):
                continue
    missing = [q["question"] for q in questions if question_key(q["question"]) not in saved]
    if missing:
        print(f"  embedding {len(missing)} question(s) ({len(questions) - len(missing)} already saved)")
        client = client or ix.make_client()
        with QUESTION_VECTORS.open("a", encoding="utf-8") as f:
            if f.tell() > 0 and not QUESTION_VECTORS.read_bytes().endswith(b"\n"):
                f.write("\n")
            for i in range(0, len(missing), ix.EMBED_BATCH):
                batch = missing[i:i + ix.EMBED_BATCH]
                vectors = ix.embed_texts([ix.query_input(t) for t in batch], client)
                for text, vector in zip(batch, vectors):
                    saved[question_key(text)] = ix._encode(vector)
                    f.write(json.dumps({"key": question_key(text), "question": text,
                                        "vector": ix._encode(vector)}, ensure_ascii=False) + "\n")
                f.flush()
    return {q["question"]: ix._decode(saved[question_key(q["question"])]) for q in questions}


def expected_pairs(row: dict) -> list[tuple[str, str]]:
    """[(source, location), ...] the answer needs; 'convenio' + two locations means both are convenio."""
    sources = [s.strip() for s in row["expected_source"].split(";") if s.strip()]
    places = [p.strip() for p in row["expected_location"].split(";") if p.strip()]
    if len(sources) == 1 and len(places) > 1:
        sources = sources * len(places)
    return list(zip(sources, places))


def matches(chunk: dict, pair: tuple[str, str]) -> bool:
    return chunk["source"] == pair[0] and pair[1] in chunk.get("locations", [chunk["location"]])


def pair_ranks(results: list[dict], pairs: list[tuple[str, str]]) -> list[int | None]:
    """For each wanted passage: the 1-based rank of the first chunk that holds it, or None."""
    return [next((r + 1 for r, item in enumerate(results) if matches(item["chunk"], p)), None)
            for p in pairs]


def hit(ranks: list[int | None], k: int, need_all: bool = True) -> bool:
    found = [r is not None and r <= k for r in ranks]
    return all(found) if need_all else any(found)


def pct(n: int, total: int) -> str:
    return f"{100 * n / total:3.0f}%" if total else "  - "


def main(client=None) -> None:
    questions = read_questions()
    answerable = [q for q in questions if q["kind"] != "unanswerable"]
    unanswerable = [q for q in questions if q["kind"] == "unanswerable"]
    print(f"{len(questions)} questions: {len(answerable)} answerable, {len(unanswerable)} unanswerable\n")
    vectors = load_question_vectors(questions, client)
    retrievers = {d: Retriever(d) for d in ("A", "B")}
    for d, r in retrievers.items():
        print(f"design {d}: {len(r.chunks)} chunks")

    rows, summary, per_question = [], {}, {}
    for label, design, mode in CONFIGS:
        retriever = retrievers[design]
        ranks_by_q, words5, words3, top1 = {}, [], [], {}
        for q in questions:
            results = retriever.search(q["question"], vectors[q["question"]], mode, TOP)
            words5.append(sum(i["chunk"]["words"] for i in results[:5]))
            words3.append(sum(i["chunk"]["words"] for i in results[:3]))
            top1[q["id"]] = results[0]["cosine"]
            if q["kind"] != "unanswerable":
                ranks = pair_ranks(results, expected_pairs(q))
                ranks_by_q[q["id"]] = ranks
                rows.append({"config": label, "id": q["id"], "kind": q["kind"],
                             "ranks_of_right_passages": ";".join(str(r) if r else "miss" for r in ranks),
                             **{f"hit@{k}": int(hit(ranks, k)) for k in (1, 3, 5)}})
        per_question[label] = ranks_by_q
        single = [q["id"] for q in answerable if q["kind"] == "single"]
        multi = [q["id"] for q in answerable if q["kind"] == "multi"]
        s = {"questions": len(answerable),
             **{f"hit@{k}": sum(hit(ranks_by_q[i], k) for i in ranks_by_q) for k in (1, 3, 5)},
             "single@5": sum(hit(ranks_by_q[i], 5) for i in single), "single_n": len(single),
             "multi_all@5": sum(hit(ranks_by_q[i], 5) for i in multi),
             "multi_any@5": sum(hit(ranks_by_q[i], 5, need_all=False) for i in multi), "multi_n": len(multi),
             "words_top3": round(statistics.mean(words3)), "words_top5": round(statistics.mean(words5)),
             "top1_cosine_answerable": [round(top1[q["id"]], 3) for q in answerable],
             "top1_cosine_unanswerable": [round(top1[q["id"]], 3) for q in unanswerable]}
        summary[label] = s

    n = len(answerable)
    print(f"\nHIT RATE on the {n} answerable questions (right passage among the top k chunks)\n")
    print(f"{'design':<28}{'hit@1':>7}{'hit@3':>7}{'hit@5':>7}   {'single@5':>9}{'multi@5 all/any':>17}   {'words in prompt (top 3 / top 5)':>32}")
    for label, s in summary.items():
        print(f"{label:<28}{pct(s['hit@1'], n):>7}{pct(s['hit@3'], n):>7}{pct(s['hit@5'], n):>7}   "
              f"{s['single@5']:>3}/{s['single_n']:<5}{s['multi_all@5']:>8}/{s['multi_any@5']}/{s['multi_n']:<4}"
              f"{s['words_top3']:>14}{s['words_top5']:>18}")

    print("\nMISSES at k=5 (right passage not in the top 5):")
    for label, _, _ in CONFIGS:
        missed = [q for q in answerable if not hit(per_question[label][q["id"]], 5)]
        print(f"  {label}: {len(missed)} -> " + (", ".join(
            f"{q['id']}({'/'.join(str(r) if r else 'x' for r in per_question[label][q['id']])})" for q in missed) or "none"))
    print("  (in brackets: the rank of each wanted passage, x = not in the top 10)")

    print("\nCan the search tell that a question is NOT covered? Top-1 cosine similarity (vector designs):")
    for label in ("A fixed + vector", "B sections + vector"):
        a, u = summary[label]["top1_cosine_answerable"], summary[label]["top1_cosine_unanswerable"]
        print(f"  {label}: answerable {min(a):.3f}-{max(a):.3f} (median {statistics.median(a):.3f}) | "
              f"unanswerable {min(u):.3f}-{max(u):.3f} | answerable below the best unanswerable: "
              f"{sum(x <= max(u) for x in a)}/{len(a)}")

    with RESULTS_CSV.open("w", newline="", encoding="utf-8") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0]))
        w.writeheader()
        w.writerows(rows)
    SUMMARY_JSON.write_text(json.dumps(summary, ensure_ascii=False, indent=1), encoding="utf-8")
    print(f"\nsaved: {RESULTS_CSV.relative_to(ix.ROOT)}, {SUMMARY_JSON.relative_to(ix.ROOT)}")


if __name__ == "__main__":
    main()
