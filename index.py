import json
import re
import time
from pathlib import Path
import hashlib
import pymupdf
import chromadb
from google import genai
from google.genai import types

from api_key import load_api_key


# --------------------------------------------------
# CONFIGURATION
# --------------------------------------------------

CHUNKS_PATH = Path("data/processed/chunks.json")
INDEX_DIR = Path("index")

MODEL = "gemini-embedding-2"
DIMENSIONS = 768
COLLECTION_NAME = "eu_regulations"

REQUEST_DELAY = 1.5
MAX_RETRIES = 5


# --------------------------------------------------
# DATABASE
# --------------------------------------------------

def get_collection():
    """Open or create the persistent ChromaDB collection."""

    INDEX_DIR.mkdir(parents=True, exist_ok=True)

    db = chromadb.PersistentClient(
        path=str(INDEX_DIR)
    )

    collection = db.get_or_create_collection(
        name=COLLECTION_NAME,
        metadata={"hnsw:space": "cosine"},
    )

    return collection


# --------------------------------------------------
# EMBEDDINGS
# --------------------------------------------------

def embed_document(client, chunk):
    """Generate a Gemini embedding for one document chunk."""

    content = (
        f"Document: {chunk['source']}\n"
        f"Article: {chunk['article']}\n"
        f"{chunk['text']}"
    )

    response = client.models.embed_content(
        model=MODEL,
        contents=content,
        config=types.EmbedContentConfig(
            output_dimensionality=DIMENSIONS
        ),
    )

    return response.embeddings[0].values


def embed_with_retry(client, chunk):
    """
    Generate an embedding with automatic retry handling.

    If Gemini returns a temporary 429 rate-limit error,
    wait and retry. Other errors are raised immediately.
    """

    for attempt in range(1, MAX_RETRIES + 1):

        try:
            return embed_document(client, chunk)

        except Exception as error:

            message = str(error)

            if "429" not in message:
                raise

            # A daily quota exhaustion should not trigger
            # repeated retries.
            if (
                "PerDay" in message
                or "per day" in message.lower()
                or "daily" in message.lower()
            ):
                print(
                    "\nDaily Gemini quota exhausted. "
                    "Resume when your quota resets.",
                    flush=True,
                )
                raise

            if attempt == MAX_RETRIES:
                print(
                    "\nMaximum retry attempts reached.",
                    flush=True,
                )
                raise

            # Extract the retry delay provided by Gemini.
            match = re.search(
                r"retry in ([\d.]+)s",
                message,
                re.IGNORECASE
            )

            if not match:
                match = re.search(
                    r"'retryDelay': '([\d.]+)s'",
                    message
                )

            wait_seconds = (
                float(match.group(1)) + 5
                if match
                else min(60 * attempt, 180)
            )

            print(
                f"\nRate limit reached (attempt "
                f"{attempt}/{MAX_RETRIES}). "
                f"Waiting {wait_seconds:.0f} seconds...",
                flush=True,
            )

            time.sleep(wait_seconds)

    raise RuntimeError("Embedding failed after retries.")


# --------------------------------------------------
# INDEXING
# --------------------------------------------------

def embed_and_store(chunks, collection=None):
    """
    Embed chunks and save them to ChromaDB.

    Existing chunk IDs are skipped to prevent unnecessary
    API calls and duplicate embeddings.
    """

    if collection is None:
        collection = get_collection()

    # Retrieve identifiers already stored in ChromaDB.
    existing_ids = set(
        collection.get(include=[])["ids"]
    )

    pending = [
        chunk
        for chunk in chunks
        if chunk["id"] not in existing_ids
    ]

    print(f"Total chunks supplied: {len(chunks)}")
    print(f"Already indexed: {len(chunks) - len(pending)}")
    print(f"Remaining: {len(pending)}", flush=True)

    if not pending:
        print("Index is already up to date.")
        return collection

    client = genai.Client(
        api_key=load_api_key()
    )

    for i, chunk in enumerate(pending, start=1):

        try:
            # Generate embedding with rate-limit handling.
            vector = embed_with_retry(client, chunk)

            # Store metadata for traceable citations.
            metadata = {
                "source": chunk["source"],
                "article": chunk["article"],
                "page_start": chunk["page_start"],
                "page_end": chunk["page_end"],
                "location": chunk["location"],
            }

            # Save immediately after successful embedding.
            collection.upsert(
                ids=[chunk["id"]],
                embeddings=[vector],
                documents=[chunk["text"]],
                metadatas=[metadata],
            )

            if i % 10 == 0 or i == len(pending):
                print(
                    f"Saved {i}/{len(pending)} new vectors. "
                    f"Total in database: {collection.count()}",
                    flush=True,
                )

        except Exception as error:

            print(
                f"\nIndexing interrupted at "
                f"pending chunk {i}.",
                flush=True,
            )

            print(f"Error: {error}", flush=True)

            print(
                "\nAll previously completed embeddings "
                "remain saved in ChromaDB."
            )

            print(
                "Run the indexing command again "
                "to resume."
            )

            raise

        # Reduce request frequency.
        time.sleep(REQUEST_DELAY)

    print("\nIndexing complete!")
    print(f"Total vectors: {collection.count()}")

    return collection


# --------------------------------------------------
# MAIN PIPELINE
# --------------------------------------------------

def build_index():
    """
    Build the persistent vector index from chunks.json.

    Called by main.py index.
    """

    if not CHUNKS_PATH.exists():
        raise FileNotFoundError(
            f"Chunks file not found: {CHUNKS_PATH}. "
            "Run the ingestion and chunking stages first."
        )

    with CHUNKS_PATH.open(
        "r", encoding="utf-8"
    ) as file:
        chunks = json.load(file)

    print("\n===================================")
    print("EU REGULATIONS — RAG INDEXING")
    print("===================================")
    print(f"Embedding model: {MODEL}")
    print(f"Vector dimensions: {DIMENSIONS}")
    print(f"Chunks loaded: {len(chunks)}")
    print("===================================\n")

    collection = get_collection()

    embed_and_store(chunks, collection)

    print("\nIndex status:")
    print(f"Stored vectors: {collection.count()}")
    print(f"Index directory: {INDEX_DIR.resolve()}")

    return collection


# --------------------------------------------------
# ADD NEW DOCUMENTS
# --------------------------------------------------

def chunk_file(path):
    """
    Extract and chunk an additional PDF document.

    Each chunk retains its source filename and page.
    Uses the same chunk size and overlap as our
    original corpus.
    """
    from chunking import CHUNK_SIZE, OVERLAP

    pdf_path = Path(path).resolve()

    if not pdf_path.is_file():
        raise FileNotFoundError(f"File not found: {pdf_path}")

    if pdf_path.suffix.lower() != ".pdf":
        raise ValueError("Only PDF documents are supported.")

    file_hash = hashlib.sha256(
        pdf_path.read_bytes()
    ).hexdigest()

    chunks = []

    with pymupdf.open(pdf_path) as pdf:
        for page_number, page in enumerate(pdf, start=1):
            text = page.get_text("text", sort=True)
            text = re.sub(r"\s+", " ", text).strip()

            if not text:
                continue

            words = text.split()
            step = CHUNK_SIZE - OVERLAP

            for start in range(0, len(words), step):
                end = min(start + CHUNK_SIZE, len(words))

                chunk_text = " ".join(words[start:end])

                # Stable ID makes re-indexing safe.
                chunk_id = hashlib.sha256(
                    f"{file_hash}:{page_number}:{start}".encode()
                ).hexdigest()[:16]

                chunks.append({
                    "id": chunk_id,
                    "source": pdf_path.name,
                    "article": 0,
                    "page_start": page_number,
                    "page_end": page_number,
                    "location": f"Page {page_number}",
                    "text": chunk_text,
                })

                if end == len(words):
                    break

    if not chunks:
        raise ValueError(
            "The PDF contains no extractable text."
        )

    return chunks


def add_document_to_index(path):
    """
    Add a PDF to the existing ChromaDB index.

    Reuses embed_and_store() and skips any chunks
    that have already been indexed.
    """
    chunks = chunk_file(path)
    collection = get_collection()

    before = collection.count()

    embed_and_store(chunks, collection)

    after = collection.count()

    return {
        "document": Path(path).name,
        "chunks_found": len(chunks),
        "chunks_added": after - before,
        "total_vectors": after,
    }

if __name__ == "__main__":
    build_index()