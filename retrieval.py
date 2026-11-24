"""Rank the same passages using dense retrieval alone or dense + BM25."""
import json
import re
import sqlite3
from collections import Counter
from pathlib import Path

import numpy as np

from corpus_data import ROOT
from index import DIM, MODEL, connect, embed

DESIGNS = ("dense", "hybrid")


def selected_design():
    path = ROOT / "index" / "design.json"
    return json.loads(path.read_text())["design"] if path.exists() else "dense"


def query_vector(query):
    folder = ROOT / ".cache"
    folder.mkdir(exist_ok=True)
    prompt = "task: question answering | query: " + query
    key = f"{MODEL}/{DIM}/{prompt}"
    with sqlite3.connect(folder / "queries.sqlite3", timeout=60) as cache:
        cache.execute("CREATE TABLE IF NOT EXISTS queries (key TEXT PRIMARY KEY, vector BLOB NOT NULL)")
        row = cache.execute("SELECT vector FROM queries WHERE key=?", (key,)).fetchone()
        if row:
            return np.frombuffer(row[0], dtype="<f4")
        vector = embed([prompt])[0]
        cache.execute("INSERT OR IGNORE INTO queries VALUES (?,?)", (key, vector.tobytes()))
    return vector


def tokens(text):
    return re.findall(r"[a-z0-9_]+", text.lower())


def lexical_scores(rows, query):
    terms = set(tokens(query))
    documents = [Counter(tokens(r["source"] + " " + r["location"] + " " + r["text"])) for r in rows]
    lengths = np.array([doc.total() for doc in documents])
    scores = np.zeros(len(rows))
    for term in terms:
        frequencies = np.array([d[term] for d in documents])
        present = np.count_nonzero(frequencies)
        idf = np.log1p((len(rows) - present + 0.5) / (present + 0.5))
        scores += idf * frequencies * 2.2 / (frequencies + 1.2 * (0.25 + 0.75 * lengths / lengths.mean()))
    return scores


def search(query, *, design=None, k=5):
    if not query.strip():
        raise ValueError("Search requires a nonempty question")
    design = design or selected_design()
    if design not in DESIGNS:
        raise ValueError(f"Unknown retrieval design {design}")
    with connect() as db:
        rows = db.execute("""SELECT p.id,p.source,p.location,p.url,p.text,v.vector FROM passages p
                             JOIN vectors v ON v.id=p.embedding_id ORDER BY p.id""").fetchall()
    if not rows:
        raise ValueError("Build the PostgreSQL index first")
    matrix = np.stack([np.frombuffer(r["vector"], dtype="<f4") for r in rows])
    dense = np.argsort(-(matrix @ query_vector(query)), kind="stable")
    order = dense
    if design == "hybrid":
        scores = np.zeros(len(rows))
        scores[dense] = 1.0 / (60 + np.arange(1, len(rows) + 1))
        bm25 = lexical_scores(rows, query)
        lexical = np.argsort(-bm25, kind="stable")
        lexical = lexical[bm25[lexical] > 0]
        scores[lexical] += 1.0 / (60 + np.arange(1, len(lexical) + 1))
        order = np.argsort(-scores, kind="stable")
    return [{key: rows[i][key] for key in ("id", "source", "location", "url", "text")} for i in order[:k]]
