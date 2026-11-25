"""SQLite vector persistence; exact cosine search; BM25 + reciprocal rank fusion.

Both retrieval designs use the same passages and saved Gemini vectors.
Loading or searching the index never embeds documents.
"""
from __future__ import annotations

from collections import Counter
from contextlib import contextmanager
import hashlib
import math
from pathlib import Path
import re
import sqlite3
import time

import numpy as np

ROOT = Path(__file__).resolve().parent
INDEX_PATH = ROOT / "index" / "corpus.sqlite3"
MODEL, DIMENSIONS = "gemini-embedding-2", 768
STOP_WORDS = set("a an and are as at be been but by can do does for from how i in is it its of on or that the their them these they this to was were what when which why will with you your".split())


def tokens(text):
    return [word for word in re.findall(r"[a-z0-9]+", text.lower()) if word not in STOP_WORDS]


def embedding_input(text, title=None, role="document"):
    if role == "query":
        return f"task: search result | query: {text}"
    if role != "document":
        raise ValueError("Role must be query or document")
    return f"title: {title or 'none'} | text: {text}"


def embedding_key(text, title=None, role="document"):
    value = f"{MODEL}|{DIMENSIONS}|{role}|{embedding_input(text, title, role)}"
    return hashlib.sha256(value.encode()).hexdigest()


def normalized(vector):
    array = np.asarray(vector, dtype=np.float32)
    if array.ndim != 1 or len(array) != DIMENSIONS or not np.isfinite(array).all():
        raise ValueError(f"Expected {DIMENSIONS} finite embedding values")
    norm = float(np.linalg.norm(array))
    if norm == 0:
        raise ValueError("Embedding cannot be zero")
    return array / norm


class Store:
    def __init__(self, path=INDEX_PATH, create=True):
        self.path = Path(path)
        if create:
            self.path.parent.mkdir(parents=True, exist_ok=True)
            with self.connection() as db:
                db.executescript("""
                    CREATE TABLE IF NOT EXISTS vectors (
                        key TEXT PRIMARY KEY, model TEXT NOT NULL, dimensions INTEGER NOT NULL,
                        role TEXT NOT NULL, vector BLOB NOT NULL, input_tokens INTEGER NOT NULL,
                        created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP);
                    CREATE TABLE IF NOT EXISTS chunks (
                        id TEXT PRIMARY KEY, source TEXT NOT NULL, location TEXT NOT NULL,
                        title TEXT NOT NULL, url TEXT NOT NULL, text TEXT NOT NULL,
                        word_start INTEGER NOT NULL, word_end INTEGER NOT NULL,
                        word_count INTEGER NOT NULL, license TEXT NOT NULL, embedding_key TEXT NOT NULL);
                    CREATE INDEX IF NOT EXISTS chunks_source ON chunks(source);
                    CREATE TABLE IF NOT EXISTS documents (
                        source TEXT PRIMARY KEY, fingerprint TEXT NOT NULL, kind TEXT NOT NULL, name TEXT NOT NULL);
                """)
        elif not self.path.is_file():
            raise RuntimeError("No saved index. Run main.py index first.")

    @contextmanager
    def connection(self):
        db = sqlite3.connect(self.path, timeout=30)
        db.row_factory = sqlite3.Row
        try:
            with db:
                yield db
        finally:
            db.close()

    def vector(self, key):
        with self.connection() as db:
            row = db.execute("SELECT * FROM vectors WHERE key=?", (key,)).fetchone()
        if row is None:
            return None
        if row["model"] != MODEL or row["dimensions"] != DIMENSIONS:
            raise RuntimeError("Saved embedding configuration does not match")
        return normalized(np.frombuffer(row["vector"], dtype="<f4").copy())

    def save_vector(self, key, vector, role, input_tokens=-1):
        vector = normalized(vector)
        # Each successful response commits immediately, preserving partial runs.
        with self.connection() as db:
            db.execute("INSERT OR IGNORE INTO vectors(key,model,dimensions,role,vector,input_tokens) VALUES(?,?,?,?,?,?)",
                       (key, MODEL, DIMENSIONS, role, vector.astype("<f4").tobytes(), input_tokens))

    def put_document(self, source, fingerprint, name, chunks, kind="base"):
        if not chunks or any(chunk["source"] != source for chunk in chunks):
            raise ValueError("Document must contain chunks with one source identifier")
        columns = ("id", "source", "location", "title", "url", "text", "word_start", "word_end", "word_count", "license", "embedding_key")
        with self.connection() as db:
            db.execute("DELETE FROM chunks WHERE source=?", (source,))
            db.executemany(f"INSERT INTO chunks({','.join(columns)}) VALUES({','.join('?' for _ in columns)})",
                           [tuple(chunk[column] for column in columns) for chunk in chunks])
            db.execute("INSERT OR REPLACE INTO documents VALUES(?,?,?,?)", (source, fingerprint, kind, name))

    def document_for_fingerprint(self, fingerprint):
        with self.connection() as db:
            row = db.execute("SELECT * FROM documents WHERE fingerprint=?", (fingerprint,)).fetchone()
        return dict(row) if row else None

    def chunks(self, source=None):
        with self.connection() as db:
            rows = db.execute("SELECT * FROM chunks WHERE source=? ORDER BY id", (source,)).fetchall() if source else db.execute("SELECT * FROM chunks ORDER BY id").fetchall()
        return [dict(row) for row in rows]

    def status(self):
        with self.connection() as db:
            total = db.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
            ready = db.execute("SELECT COUNT(*) FROM chunks c JOIN vectors v ON c.embedding_key=v.key").fetchone()[0]
            sources = db.execute("SELECT COUNT(DISTINCT source) FROM chunks").fetchone()[0]
            queries = db.execute("SELECT COUNT(*) FROM vectors WHERE role='query'").fetchone()[0]
        return {"documents": sources, "chunks": total, "embedded_chunks": ready, "pending_chunks": total-ready,
                "cached_query_vectors": queries, "model": MODEL, "dimensions": DIMENSIONS, "bytes": self.path.stat().st_size}


class GeminiEmbedder:
    def __init__(self):
        from api_key import load_api_key
        from google import genai
        self.client = genai.Client(api_key=load_api_key())

    def __call__(self, text, title=None, role="document"):
        from google.genai import types
        # Embedding 2 aggregates lists; send one passage per call. Its task
        # instruction is a text prefix, not the older task_type parameter.
        response = self.client.models.embed_content(model=MODEL, contents=embedding_input(text, title, role),
                    config=types.EmbedContentConfig(output_dimensionality=DIMENSIONS))
        if not response.embeddings or len(response.embeddings) != 1:
            raise RuntimeError("Gemini did not return exactly one embedding")
        # The current Gemini embedding response does not report token usage.
        # Store -1 for unavailable, rather than presenting zero as measured cost.
        return normalized(response.embeddings[0].values), -1


def cached_embedding(store, text, title=None, role="document", embedder=None):
    key = embedding_key(text, title, role)
    vector = store.vector(key)
    if vector is not None:
        return vector, True
    vector, input_tokens = (embedder or GeminiEmbedder())(text, title=title, role=role)
    store.save_vector(key, vector, role, input_tokens)
    return normalized(vector), False


def bm25_scores(query, chunks, k1=1.5, b=0.75):
    documents = [Counter(tokens(chunk["title"] + " " + chunk["text"])) for chunk in chunks]
    lengths = [sum(document.values()) for document in documents]
    average = sum(lengths)/len(lengths) if lengths else 1.0
    scores = np.zeros(len(chunks), dtype=np.float64)
    for term in set(tokens(query)):
        frequency = sum(term in document for document in documents)
        if not frequency:
            continue
        idf = math.log(1+(len(documents)-frequency+0.5)/(frequency+0.5))
        for i, document in enumerate(documents):
            tf = document[term]
            if tf:
                scores[i] += idf*tf*(k1+1)/(tf+k1*(1-b+b*lengths[i]/(average or 1.0)))
    return scores


def search(query, design="dense", k=5, store=None, embedder=None):
    if design not in {"dense", "hybrid"}:
        raise ValueError("Design must be dense or hybrid")
    if not query.strip() or len(query) > 10_000 or not 1 <= k <= 20:
        raise ValueError("Provide a nonempty question under 10,000 characters and k between 1 and 20")
    started = time.perf_counter()
    store = store or Store(create=False)
    chunks = store.chunks()
    if not chunks or store.status()["pending_chunks"]:
        raise RuntimeError("Index is incomplete. Run main.py index to finish pending embeddings.")
    embedding_started = time.perf_counter()
    query_vector, cache_hit = cached_embedding(store, query.strip(), role="query", embedder=embedder)
    embedding_seconds = time.perf_counter()-embedding_started
    matrix = np.stack([store.vector(chunk["embedding_key"]) for chunk in chunks])
    dense = matrix @ query_vector
    dense_order = sorted(range(len(chunks)), key=lambda i: (-float(dense[i]), chunks[i]["id"]))
    lexical = bm25_scores(query, chunks) if design == "hybrid" else np.zeros(len(chunks))
    if design == "hybrid":
        # Equal-weight RRF combines rankings, not incompatible raw score scales.
        # Freeze these defaults until the student-authored test set is complete.
        fused = np.zeros(len(chunks))
        lexical_order = sorted((i for i in range(len(chunks)) if lexical[i] > 0), key=lambda i: (-float(lexical[i]), chunks[i]["id"]))
        for ranking in (dense_order[:50], lexical_order[:50]):
            for rank, i in enumerate(ranking, 1):
                fused[i] += 1/(60+rank)
        order = sorted(range(len(chunks)), key=lambda i: (-float(fused[i]), chunks[i]["id"]))
    else:
        fused, order = dense, dense_order
    results = []
    for i in order[:k]:
        chunk = chunks[i]
        results.append({**{name: chunk[name] for name in ("id", "source", "location", "title", "url", "text", "word_start", "word_end", "word_count")},
                        "passage_location": f"{chunk['location']}@{chunk['word_start']}:{chunk['word_end']}",
                        "citation": f"[{chunk['source']} | {chunk['location']}]",
                        "score": float(fused[i]), "semantic_score": float(dense[i]), "keyword_score": float(lexical[i])})
    seconds = time.perf_counter()-started
    return {"query": query, "design": design, "query_embedding_cache_hit": cache_hit,
            "query_embedding_seconds": embedding_seconds, "retrieval_seconds": seconds-embedding_seconds,
            "seconds": seconds, "results": results}
