"""Compare retrieval only, after the student has completed the test set.

This is imported by the eventual end-to-end evaluation stage. It deliberately
does not select a winner or run a benchmark on a partially authored question set.
"""
import csv
import hashlib
import json
from pathlib import Path
import time

from retrieval import ROOT, Store, search

FIELDS = ["id", "question", "kind", "expected_source", "expected_location", "reference_answer"]


def expected_evidence(question):
    sources = [s.strip() for s in question["expected_source"].split(";") if s.strip()]
    locations = [s.strip() for s in question["expected_location"].split(";") if s.strip()]
    if not sources and not locations:
        return set()
    if len(sources) == 1:
        return {(sources[0], location) for location in locations}
    if len(sources) != len(locations):
        raise ValueError("Use one source for multiple locations, or matching source/location lists")
    return set(zip(sources, locations))


def load_questions(path=ROOT / "eval" / "questions.csv", store=None, require_complete=True):
    with Path(path).open(newline="", encoding="utf-8") as stream:
        reader = csv.DictReader(stream)
        if any(field not in (reader.fieldnames or []) for field in FIELDS):
            raise ValueError("Question columns must include: " + ", ".join(FIELDS))
        questions = [dict(row) for row in reader if (row.get("question") or "").strip()]
    problems, ids = [], set()
    known = set()
    if store is not None:
        for chunk in store.chunks():
            known.add((chunk["source"], chunk["location"]))
            known.add((chunk["source"], f"{chunk['location']}@{chunk['word_start']}:{chunk['word_end']}"))
    for question in questions:
        identifier = question["id"].strip()
        if not identifier or identifier in ids:
            problems.append(f"Missing or duplicate question ID: {identifier}")
        ids.add(identifier)
        if not question["reference_answer"].strip():
            problems.append(f"{identifier}: missing student reference answer")
        kind = question["kind"].strip()
        if kind not in {"single", "multi", "unanswerable"}:
            problems.append(f"{identifier}: invalid kind")
        try:
            evidence = expected_evidence(question)
        except ValueError as error:
            problems.append(f"{identifier}: {error}")
            continue
        if kind == "unanswerable":
            if question["expected_source"].strip() or question["expected_location"].strip():
                problems.append(f"{identifier}: unanswerable questions must have no source/location")
        elif not evidence:
            problems.append(f"{identifier}: missing source/location evidence")
        if kind == "multi" and len(evidence) < 2:
            problems.append(f"{identifier}: identify at least two evidence passages")
        if store is not None:
            for reference in evidence-known:
                problems.append(f"{identifier}: unknown source/location {reference}")
    if require_complete:
        kinds = [question["kind"].strip() for question in questions]
        if len(questions) < 30 or kinds.count("multi") < 5 or kinds.count("unanswerable") < 5:
            problems.append(f"Test set is still being authored: {len(questions)}/30 questions, "
                            f"{kinds.count('multi')}/5 multi, {kinds.count('unanswerable')}/5 unanswerable. "
                            "Finish it before running retrieval evaluation.")
    if problems:
        raise ValueError("\n".join(problems))
    return questions


def coverage_at_k(question, results, k):
    expected = expected_evidence(question)
    if not expected:
        return {"hit_any": None, "hit_all": None, "evidence_recall": None}
    found = set()
    for result in results[:k]:
        for source, location in expected:
            if source == result["source"] and location in {result["location"], result["passage_location"]}:
                found.add((source, location))
    return {"hit_any": int(bool(found)), "hit_all": int(found == expected),
            "evidence_recall": len(found)/len(expected)}


def evaluate_retrieval(questions_path=ROOT / "eval" / "questions.csv", store=None, embedder=None, output_dir=ROOT / "eval"):
    store = store or Store(create=False)
    questions = load_questions(questions_path, store, require_complete=True)
    if store.status()["pending_chunks"]:
        raise RuntimeError("Finish the saved index before evaluating")
    output_dir = Path(output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)
    fingerprint = hashlib.sha256(Path(questions_path).read_bytes()).hexdigest()
    records, rows = [], []
    started = time.perf_counter()
    for question in questions:
        for design in ("dense", "hybrid"):
            result = search(question["question"], design=design, k=5, store=store, embedder=embedder)
            records.append({"id": question["id"], **result})
            for k in (1, 3, 5):
                rows.append({"id": question["id"], "kind": question["kind"], "design": design, "k": k,
                             **coverage_at_k(question, result["results"], k),
                             "context_words": sum(hit["word_count"] for hit in result["results"][:k]),
                             "search_seconds": result["seconds"],
                             "query_embedding_seconds": result["query_embedding_seconds"],
                             "retrieval_seconds": result["retrieval_seconds"],
                             "query_embedding_cache_hit": result["query_embedding_cache_hit"]})
    if hashlib.sha256(Path(questions_path).read_bytes()).hexdigest() != fingerprint:
        raise RuntimeError("Question set changed during evaluation; run again with the fixed set")
    summary = {"run_kind": "retrieval_only", "questions_sha256": fingerprint,
               "question_count": len(questions), "seconds": time.perf_counter()-started,
               "winner": None, "metrics": [],
               "notes": ["Unanswerable questions are excluded from hit-rate denominators.",
                         "hit_all requires all annotated passages for multi-passage questions.",
                         "The designs share query embeddings. Compare retrieval_seconds; common query embedding time is recorded separately."]}
    for design in ("dense", "hybrid"):
        for k in (1, 3, 5):
            subset = [r for r in rows if r["design"] == design and r["k"] == k and r["hit_any"] is not None]
            summary["metrics"].append({"design": design, "k": k, "answerable_questions": len(subset),
                    **{metric: sum(r[metric] for r in subset)/len(subset) if subset else None
                       for metric in ("hit_any", "hit_all", "evidence_recall")}})
    with (output_dir / "retrieval_metrics.csv").open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=list(rows[0]), lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)
    (output_dir / "retrieval_results.jsonl").write_text("".join(json.dumps(r, ensure_ascii=False)+"\n" for r in records), encoding="utf-8")
    (output_dir / "retrieval_summary.json").write_text(json.dumps(summary, indent=2)+"\n")
    return summary


if __name__ == "__main__":
    print(json.dumps(evaluate_retrieval(), indent=2))
