import csv
import math
import re
import sqlite3
from collections import Counter

from evaluate_retrieval import QUESTIONS, ROOT, CUTOFFS, evaluate_question
from vector_store import DB_PATH


def tokenize(text):
    return re.findall(r"[a-z0-9]+", text.lower())


class BM25Search:
    def __init__(self):
        db = sqlite3.connect(f"{DB_PATH.as_uri()}?mode=ro", uri=True)
        try:
            rows = db.execute(
                "SELECT id, source, page, text FROM chunks ORDER BY id"
            ).fetchall()
        finally:
            db.close()

        if not rows:
            raise ValueError("The index contains no chunks.")

        self.chunks = []
        self.frequencies = []
        self.lengths = []
        document_frequency = Counter()

        for chunk_id, source, page, text in rows:
            tokens = tokenize(text)
            frequencies = Counter(tokens)
            self.chunks.append({
                "id": chunk_id, "source": source, "page": page, "text": text
            })
            self.frequencies.append(frequencies)
            self.lengths.append(len(tokens))
            document_frequency.update(frequencies.keys())

        count = len(rows)
        self.average_length = sum(self.lengths) / count
        self.idf = {
            term: math.log(1 + (count - frequency + 0.5) / (frequency + 0.5))
            for term, frequency in document_frequency.items()
        }

    def search(self, query, k=5):
        terms = set(tokenize(query))
        k1, b = 1.2, 0.75
        scores = []

        for i, frequencies in enumerate(self.frequencies):
            length_factor = k1 * (
                1 - b + b * self.lengths[i] / self.average_length
            )
            score = 0.0
            for term in terms:
                tf = frequencies[term]
                if tf:
                    score += self.idf[term] * tf * (k1 + 1) / (tf + length_factor)
            if score > 0:
                scores.append((score, i))

        scores.sort(key=lambda item: (-item[0], item[1]))
        return [
            {**self.chunks[i], "score": score}
            for score, i in scores[:k]
        ]


def main():
    retriever = BM25Search()
    with QUESTIONS.open(encoding="utf-8-sig", newline="") as file:
        questions = [
            row for row in csv.DictReader(file)
            if row["kind"] in {"single", "multi"}
        ]

    results = [evaluate_question(q, retriever.search) for q in questions]

    output = ROOT / "eval" / "retrieval_bm25.csv"
    with output.open("w", encoding="utf-8", newline="") as file:
        writer = csv.DictWriter(file, fieldnames=results[0].keys())
        writer.writeheader()
        writer.writerows(results)

    for group in ("single", "multi", "all"):
        subset = [r for r in results if group == "all" or r["kind"] == group]
        print(f"\n{group} ({len(subset)} questions)")
        for k in CUTOFFS:
            hits = sum(r[f"hit_at_{k}"] for r in subset)
            print(f"  Hit@{k}: {hits}/{len(subset)} ({hits / len(subset):.1%})")

    dense_file = ROOT / "eval" / "retrieval_dense.csv"
    with dense_file.open(encoding="utf-8-sig", newline="") as file:
        dense = {row["id"]: int(row["hit_at_5"]) for row in csv.DictReader(file)}

    gained = [r["id"] for r in results if r["hit_at_5"] and not dense[r["id"]]]
    lost = [r["id"] for r in results if dense[r["id"]] and not r["hit_at_5"]]
    print("\nBM25 gains at 5:", ", ".join(gained) or "none")
    print("BM25 losses at 5:", ", ".join(lost) or "none")
    print(f"Saved results to {output.name}")


if __name__ == "__main__":
    main()