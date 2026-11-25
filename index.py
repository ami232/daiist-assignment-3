from api_key import load_api_key

import os
import hashlib
import fitz
import chromadb

from pathlib import Path
from google import genai
from google.genai import types

ROOT = Path(__file__).resolve().parent
CORPUS = ROOT / "corpus"
INDEX = ROOT / "index"

MODEL = "gemini-embedding-2"
CHUNK_SIZE = 400
OVERLAP = 50

def get_client():
    return genai.Client(
        api_key=load_api_key()
    )

def get_collection():
    db = chromadb.PersistentClient(path=str(INDEX))
    return db.get_or_create_collection(
        name="aviation_safety_selected",
        metadata={"hnsw:space": "cosine"}
    )

def extract_chunks(path):
    path = Path(path)
    chunks = []

    with fitz.open(path) as pdf:
        for page_number, page in enumerate(pdf, start=1):

            text = " ".join(page.get_text(sort=True).split())
            words = text.split()

            for start in range(0, len(words), CHUNK_SIZE - OVERLAP):

                content = " ".join(
                    words[start:start + CHUNK_SIZE]
                )

                if not content:
                    continue

                chunk_id = hashlib.sha256(
                    f"{path.name}:{page_number}:{start}:{content}".encode()
                ).hexdigest()

                chunks.append({
                    "id": chunk_id,
                    "text": content,
                    "source": path.name,
                    "page": page_number
                })

                if start + CHUNK_SIZE >= len(words):
                    break

    return chunks

def embed_texts(texts):
    import time

    client = get_client()
    vectors = []

    for text in texts:
        for attempt in range(8):
            try:
                result = client.models.embed_content(
                    model=MODEL,
                    contents=text,
                    config=types.EmbedContentConfig(
                        output_dimensionality=768
                    )
                )

                vectors.append(result.embeddings[0].values)
                time.sleep(1.5)
                break

            except Exception as e:
                print("EMBEDDING ERROR:", repr(e), flush=True)

                if attempt == 7:
                    raise

                time.sleep(30)

    return vectors


def add_document(path, max_new=None):
    collection = get_collection()
    chunks = extract_chunks(path)

    existing = set(collection.get(include=[])["ids"])

    pending = [
        chunk for chunk in chunks
        if chunk["id"] not in existing
    ]

    if max_new is not None:
        pending = pending[:max_new]

    print(f"{Path(path).name}:")
    print(f"Total chunks: {len(chunks)}")
    print(f"New chunks this run: {len(pending)}")

    saved = 0

    for start in range(0, len(pending), 1):
        batch = pending[start:start + 1]

        vectors = embed_texts(
            [chunk["text"] for chunk in batch]
        )

        collection.add(
            ids=[chunk["id"] for chunk in batch],
            documents=[chunk["text"] for chunk in batch],
            embeddings=vectors,
            metadatas=[
                {
                    "source": chunk["source"],
                    "page": chunk["page"]
                }
                for chunk in batch
            ]
        )

        saved += len(batch)
        print(f"Saved {saved}/{len(pending)}", flush=True)

    return saved

def build_index():
    remaining = int(os.getenv("MAX_NEW_EMBEDDINGS", "900"))

    for path in sorted(CORPUS.glob("*.pdf")):
        saved = add_document(path, max_new=remaining)
        remaining -= saved

        if remaining <= 0:
            print("Embedding budget reached.")
            break

    print("Indexed chunks:", get_collection().count())


# SELECTED CORPUS
_original_extract_chunks = extract_chunks

def extract_chunks(path):
    import json

    chunks = _original_extract_chunks(path)

    selected = json.loads(
        (ROOT / "corpus_selection.json").read_text()
    )

    pages = selected.get(Path(path).name)

    if pages is None:
        return chunks

    return [
        c for c in chunks
        if c["page"] in pages
    ]


if __name__ == "__main__":
    build_index()
