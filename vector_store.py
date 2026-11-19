import hashlib
import json
import sqlite3
from pathlib import Path

import numpy as np
from google import genai
from google.genai import types

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
DB_PATH = ROOT / "index" / "vectors.sqlite3"
MODEL = "gemini-embedding-2"
DIMENSIONS = 768


def open_store():
    DB_PATH.parent.mkdir(exist_ok=True)
    db = sqlite3.connect(DB_PATH)
    db.execute("""
        CREATE TABLE IF NOT EXISTS chunks (
            id TEXT PRIMARY KEY,
            source TEXT NOT NULL,
            page INTEGER NOT NULL,
            text TEXT NOT NULL,
            fingerprint TEXT NOT NULL,
            vector BLOB NOT NULL
        )
    """)
    return db


def store_chunk(db, client, chunk):
    prompt = f"title: {chunk['source']} | text: {chunk['text']}"
    fingerprint = hashlib.sha256(
        f"{MODEL}\n{DIMENSIONS}\n{prompt}".encode("utf-8")
    ).hexdigest()

    existing = db.execute(
        "SELECT fingerprint, length(vector) FROM chunks WHERE id = ?",
        (chunk["id"],),
    ).fetchone()

    if existing == (fingerprint, DIMENSIONS * 4):
        return "reused"

    result = client.models.embed_content(
        model=MODEL,
        contents=prompt,
        config=types.EmbedContentConfig(output_dimensionality=DIMENSIONS),
    )
    vector = np.asarray(result.embeddings[0].values, dtype="<f4")
    if vector.shape != (DIMENSIONS,) or not np.isfinite(vector).all():
        raise ValueError(f"Invalid embedding for {chunk['id']}")

    with db:
        db.execute(
            "INSERT OR REPLACE INTO chunks VALUES (?, ?, ?, ?, ?, ?)",
            (chunk["id"], chunk["source"], chunk["page"], chunk["text"],
             fingerprint, vector.tobytes()),
        )
    return "saved"


if __name__ == "__main__":
    with (ROOT / "corpus" / "chunks.jsonl").open(encoding="utf-8") as file:
        first_chunk = json.loads(next(file))

    db = open_store()
    try:
        with genai.Client(api_key=load_api_key()) as client:
            status = store_chunk(db, client, first_chunk)
        print(f"{first_chunk['id']}: {status} ({DIMENSIONS} dimensions)")
    finally:
        db.close()