"""Build and extend a portable, section-cited SQLite vector index."""
import hashlib
import os
import re
import sqlite3
import time
from collections import defaultdict
from pathlib import Path

import numpy as np
from google import genai
from google.genai import errors, types

from api_key import load_api_key
from corpus_data import DOCUMENTS, ROOT, Section, load_corpus, write_reading_copy

MODEL = "gemini-embedding-2"
DIM = 768
WIDTH = 240
OVERLAP = 35


def database():
    return Path(os.environ.get("PG_RAG_DB", ROOT / "index" / "postgres.sqlite3"))


def connect():
    connection = sqlite3.connect(database(), timeout=60)
    connection.row_factory = sqlite3.Row
    return connection


def create_tables(db):
    db.executescript("""
        CREATE TABLE IF NOT EXISTS vectors (id TEXT PRIMARY KEY, vector BLOB NOT NULL);
        CREATE TABLE IF NOT EXISTS passages (
            id TEXT PRIMARY KEY, source TEXT NOT NULL, location TEXT NOT NULL,
            url TEXT NOT NULL, text TEXT NOT NULL, embedding_id TEXT NOT NULL REFERENCES vectors(id)
        );
    """)


def digest(text):
    return hashlib.sha256(text.encode()).hexdigest()


def embed(texts):
    client = genai.Client(api_key=load_api_key())
    try:
        for attempt in range(8):
            try:
                response = client.models.embed_content(
                    model=MODEL, contents=[types.Content(parts=[types.Part(text=t)]) for t in texts],
                    config=types.EmbedContentConfig(output_dimensionality=DIM),
                )
                break
            except errors.APIError as exc:
                if exc.code not in {429, 500, 502, 503, 504} or attempt == 7 or "per day" in str(exc).lower():
                    raise
                delay = re.search(r"retry in ([0-9.]+)s", str(exc), re.I)
                time.sleep(float(delay[1]) + 2 if delay else min(60, 2 ** (attempt + 1)))
    finally:
        client.close()
    if len(response.embeddings) != len(texts):
        raise ValueError("Gemini returned a different number of embeddings than requested")
    vectors = np.asarray([e.values for e in response.embeddings], dtype="<f4")
    if vectors.shape != (len(texts), DIM) or not np.isfinite(vectors).all():
        raise ValueError("Invalid embedding dimensions or values")
    norms = np.linalg.norm(vectors, axis=1, keepdims=True)
    if (norms == 0).any():
        raise ValueError("Zero-length embedding")
    return vectors / norms


def chunk_sections(sections):
    chunks = []
    for section in sections:
        words = section.text.split()
        for start in range(0, len(words), WIDTH - OVERLAP):
            text = " ".join(words[start:start + WIDTH])
            prompt = f"title: {section.source} / {section.location} | text: {text}"
            vector_id = digest(f"{MODEL}/{DIM}\n{prompt}")
            citation = "PG-" + digest(f"{vector_id}/{section.url}/{start}")[:14]
            chunks.append((citation, section.source, section.location, section.url, text, vector_id, prompt))
            if start + WIDTH >= len(words):
                break
    return chunks


def store_document(db, sections):
    chunks = chunk_sections(sections)
    if not chunks:
        raise ValueError("Document contains no indexable text")
    source = sections[0].source
    old = {r[0] for r in db.execute("SELECT id FROM passages WHERE source=?", (source,))}
    if old == {r[0] for r in chunks}:
        return {"source": source, "status": "already indexed", "chunks": len(chunks), "new_vectors": 0}
    prompts = {r[5]: r[6] for r in chunks}
    saved = {r[0] for r in db.execute("SELECT id FROM vectors")}
    missing = [key for key in prompts if key not in saved]
    for start in range(0, len(missing), 24):
        keys = missing[start:start + 24]
        vectors = embed([prompts[key] for key in keys])
        with db:
            db.executemany("INSERT OR IGNORE INTO vectors VALUES (?,?)",
                           [(key, vector.tobytes()) for key, vector in zip(keys, vectors, strict=True)])
    # Publish a complete new version atomically. Past vectors can be reused on retry.
    with db:
        db.execute("DELETE FROM passages WHERE source=?", (source,))
        db.executemany("INSERT INTO passages VALUES (?,?,?,?,?,?)", [c[:6] for c in chunks])
    status = "replaced" if old else "indexed"
    return {"source": source, "status": status, "chunks": len(chunks), "new_vectors": len(missing)}


def add_file(path):
    file = Path(path).expanduser().resolve(strict=True)
    if file.suffix.lower() not in {".md", ".txt"} or not file.is_file():
        raise ValueError("Choose a UTF-8 .md or .txt document")
    if file.stat().st_size > 2_000_000:
        raise ValueError("Additional documents must be under 2 MB")
    source = file.stem
    if source in DOCUMENTS:
        raise ValueError("This name belongs to a pinned PostgreSQL document")
    current = "Document"
    lines = []
    sections = []
    for line in file.read_text(encoding="utf-8").splitlines():
        if re.match(r"^#{1,6}\s+", line):
            if any(s.strip() for s in lines):
                sections.append(Section(source, current, file.name, "\n".join(lines)))
            current = line.lstrip("#").strip()
            lines = []
        else:
            lines.append(line)
    if any(s.strip() for s in lines):
        sections.append(Section(source, current, file.name, "\n".join(lines)))
    with connect() as db:
        create_tables(db)
        return store_document(db, sections)


def main():
    sections = load_corpus()
    write_reading_copy(sections)
    groups = defaultdict(list)
    for section in sections:
        groups[section.source].append(section)
    database().parent.mkdir(parents=True, exist_ok=True)
    with connect() as db:
        create_tables(db)
        for group in groups.values():
            print(store_document(db, group), flush=True)


if __name__ == "__main__":
    main()
