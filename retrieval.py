
import math
import re
from collections import Counter

import numpy as np

from index import BOOKS, connect, query_vector

def tokens(text):
    return re.findall(r"[a-z0-9]+", text.lower())

def rank(query, design="dense", k=5):
    with connect() as db:
        rows = db.execute("""
            SELECT id, source, location, text, vector
            FROM chunks
            WHERE vector IS NOT NULL
            ORDER BY id
        """).fetchall()

    if not rows:
        raise RuntimeError("Index is empty. Run index.py first.")

    matrix = np.stack([np.frombuffer(row["vector"], dtype=np.float32) for row in rows])
    q_vector = query_vector(query)
    dense = matrix @ q_vector
    order = np.argsort(-dense, kind="stable")

    if design == "hybrid":
        documents = [Counter(tokens(BOOKS.get(row["source"], (0, row["source"], 0))[1] + " " + row["location"]+ " "+ row["text"])) for row in rows]

        lengths = np.array([sum(document.values()) for document in documents])
        average_length = lengths.mean()
        bm25 = np.zeros(len(rows))
        for term in set(tokens(query)):
            tf = np.array([document[term] for document in documents])
            df = np.count_nonzero(tf)
            idf = math.log(1 + (len(rows) - df + 0.5) / (df + 0.5))

            bm25 += (idf * tf * 2.5 / (tf + 1.5 *(0.25 + 0.75 * lengths / average_length)))
        lexical = np.argsort(-bm25, kind="stable")
        scores = np.zeros(len(rows))
        scores[order] += (1 / (60 + np.arange(1, len(rows) + 1)))
        positive = lexical[bm25[lexical] > 0]
        scores[positive] += (1 / (60 + np.arange(1, len(positive) + 1)))
        order = np.argsort(-scores, kind="stable")
    elif design != "dense":
        raise ValueError("Unknown retrieval design")

    results = []
    for i in order[:k]:
        results.append({
            "id": rows[i]["id"],
            "source": rows[i]["source"],
            "location": rows[i]["location"],
            "text": rows[i]["text"],
            "cosine": round(float(dense[i]), 5)})
    return results

def selected_design():
    with connect() as db:
        row = db.execute("""
            SELECT value FROM settings
            WHERE key='design'
        """).fetchone()
        return row["value"] if row else "dense"

def set_design(design):
    if design not in ("dense", "hybrid"):
        raise ValueError("Unknown retrieval design")
    with connect() as db:
        db.execute("INSERT OR REPLACE INTO settings VALUES (?, ?)", ("design", design))
        db.commit()

if __name__ == "__main__":
    query = "What should a central bank do during a banking panic?"
    for design in ("dense", "hybrid"):
        print(f"\n--- {design.upper()} ---")
        results = rank(query, design=design, k=5)
        for i, result in enumerate(results, 1):
            print(f"\nRank: {i}")
            print(f"Source: {result['source']}")
            print(f"Location: {result['location']}")
            print(f"Cosine: {result['cosine']}")
            print(f"Text: {result['text'][:250]}...")
