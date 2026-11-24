import hashlib
import sqlite3
import time
from pathlib import Path

from google import genai
from pypdf import PdfReader

from api_key import load_api_key
from chunk_corpus import split_page
from prepare_corpus import clean_page
from vector_store import open_store, store_chunk


def index_document(path):
    pdf = Path(path).expanduser().resolve()

    if not pdf.is_file() or pdf.suffix.lower() != ".pdf":
        raise ValueError("Provide the path to an existing PDF file.")

    digest = hashlib.sha256(pdf.read_bytes()).hexdigest()
    db = open_store()

    try:
        db.execute("""
            CREATE TABLE IF NOT EXISTS added_documents (
                digest TEXT PRIMARY KEY,
                source TEXT NOT NULL,
                chunk_count INTEGER NOT NULL
            )
        """)

        previous = db.execute(
            "SELECT source, chunk_count FROM added_documents WHERE digest = ?",
            (digest,),
        ).fetchone()

        if previous:
            return f"Already indexed: {previous[0]} ({previous[1]} chunks)."

        # The original three guides already have their own reviewed page ranges.
        # Recognise those files even if the caller has renamed a copy.
        corpus_dir = Path(__file__).resolve().parent / "corpus"
        for guide in ("hsg76", "hsg136", "l117"):
            original = corpus_dir / f"{guide}.pdf"
            if original.is_file():
                original_digest = hashlib.sha256(original.read_bytes()).hexdigest()
                if digest == original_digest:
                    return f"Already indexed: {guide.upper()} (original corpus)."

        source = f"{pdf.stem}-{digest[:8]}"
        reader = PdfReader(pdf)
        chunks = []

        for page_number, page in enumerate(reader.pages, start=1):
            text = clean_page(page.extract_text(extraction_mode="layout"))
            if not text:
                text = clean_page(page.extract_text(extraction_mode="plain"))

            for number, passage in enumerate(split_page(text), start=1):
                chunks.append({
                    "id": f"{source}-p{page_number:03d}-c{number:02d}",
                    "source": source,
                    "page": page_number,
                    "text": passage,
                })

        if not chunks:
            raise ValueError("The PDF contains no extractable text.")

        # Prepare vectors separately. The searchable index is updated only
        # after every chunk of the new document has been embedded successfully.
        with sqlite3.connect(":memory:") as staging:
            schema = db.execute(
                "SELECT sql FROM sqlite_master WHERE type='table' AND name='chunks'"
            ).fetchone()[0]
            staging.execute(schema)

            with genai.Client(api_key=load_api_key()) as client:
                for position, chunk in enumerate(chunks, start=1):
                    store_chunk(staging, client, chunk)
                    if position < len(chunks):
                        time.sleep(0.75)

            with db:
                db.execute(
                    "INSERT INTO added_documents VALUES (?, ?, ?)",
                    (digest, source, len(chunks)),
                )
                db.executemany(
                    """INSERT INTO chunks
                       (id, source, page, text, fingerprint, vector)
                       VALUES (?, ?, ?, ?, ?, ?)""",
                    staging.execute(
                        "SELECT id, source, page, text, fingerprint, vector FROM chunks"
                    ),
                )

        return f"Indexed {source}: {len(chunks)} chunks from {len(reader.pages)} PDF pages."

    finally:
        db.close()