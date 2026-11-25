"""
Assignment 3: build the index (`main.py index`). May be index.ipynb instead.

Download the corpus (into corpus/, git-ignored), extract, clean and chunk it
with source and location metadata, embed with Gemini, and store everything in
index/. Save each vector as you get it and embed only chunks without one.

Write the per-file steps as functions (e.g. `chunk_file(path)`,
`embed_and_store(chunks)`): server.py's add-document tool imports them.
"""

import hashlib
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"
COLLECTION_NAME = "personal_finance_v1"
EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768
CHUNK_WORDS = 350
OVERLAP_WORDS = 50

SOURCES = {
    "money_goals.pdf": "https://files.consumerfinance.gov/f/documents/cfpb_your-money-your-goals_financial-empowerment_toolkit.pdf",
    "behind_on_bills.pdf": "https://files.consumerfinance.gov/f/documents/cfpb_your-money-your-goals_behind-on-bills_booklet_cobrand.pdf",
    "debt_booklet.pdf": "https://files.consumerfinance.gov/f/documents/cfpb_your-money-your-goals_debt_booklet_cobrand.pdf",
    "credit_booklet.pdf": "https://files.consumerfinance.gov/f/documents/cfpb_your-money-your-goals_credit_booklet_cobrand.pdf",
    "home_loan_toolkit.pdf": "https://files.consumerfinance.gov/f/documents/cfpb_your-home-loan-toolkit.pdf",
}


def download_corpus():
    """Get missing default PDFs; downloaded originals are not committed to git."""
    import httpx

    CORPUS_DIR.mkdir(parents=True, exist_ok=True)
    for filename, url in SOURCES.items():
        path = CORPUS_DIR / filename
        if path.exists():
            continue
        print(f"Downloading {filename}...", flush=True)
        with httpx.stream("GET", url, follow_redirects=True, timeout=120) as response:
            response.raise_for_status()
            with path.open("wb") as out:
                for data in response.iter_bytes():
                    out.write(data)


def clean_text(text):
    """Basic cleaning without changing financial figures or punctuation."""
    text = text.replace("\u00a0", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def chunk_file(path):
    """Return chunks with a PDF page citation and stable content-based IDs."""
    from pypdf import PdfReader

    path = Path(path)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()
    reader = PdfReader(str(path))

    for page_no, page in enumerate(reader.pages, start=1):
        text = clean_text(page.extract_text() or "")
        words = text.split()
        if len(words) < 35:  # Skip covers and essentially empty worksheets
            continue

        offset = 0
        part = 0
        while offset < len(words):
            end = min(offset + CHUNK_WORDS, len(words))
            # Avoid tiny final chunks with mostly duplicated words.
            if 0 < len(words) - end < 100:
                end = len(words)
            passage = " ".join(words[offset:end])
            identity = f"{path.name}|{digest}|{page_no}|{part}|{passage}"
            chunk_id = hashlib.sha256(identity.encode("utf-8")).hexdigest()[:32]
            yield {
                "id": chunk_id,
                "text": passage,
                "metadata": {
                    "source": path.name,
                    "page": page_no,
                    "location": f"page {page_no}",
                    "source_url": SOURCES.get(path.name, "local document"),
                    "document_sha256": digest,
                },
            }
            if end == len(words):
                break
            offset = end - OVERLAP_WORDS
            part += 1


def get_collection():
    import chromadb

    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    database = chromadb.PersistentClient(path=str(INDEX_DIR))
    return database.get_or_create_collection(
        name=COLLECTION_NAME,
        embedding_function=None,
    )


def embed_and_store(chunks, collection=None):
    """Persist each vector immediately, so interruptions never lose earlier work."""
    from google import genai
    from google.genai import types
    from api_key import load_api_key

    collection = get_collection() if collection is None else collection
    existing = set(collection.get(include=[])['ids'])
    pending = [chunk for chunk in chunks if chunk['id'] not in existing]
    print(f"Already saved: {len(chunks) - len(pending)} | To embed: {len(pending)}", flush=True)
    if not pending:
        return 0

    client = genai.Client(api_key=load_api_key())
    written = 0
    try:
        for number, chunk in enumerate(pending, start=1):
            title = chunk['metadata']['source']
            # Gemini Embedding 2 uses input prefixes instead of task_type.
            input_text = f"title: {title} | text: {chunk['text']}"
            for retry in range(3):
                try:
                    response = client.models.embed_content(
                        model=EMBED_MODEL,
                        contents=input_text,  # One text per call; no accidental aggregation
                        config=types.EmbedContentConfig(output_dimensionality=EMBED_DIM),
                    )
                    vector = response.embeddings[0].values
                    break
                except Exception as error:
                    if retry == 2 or not any(
                        marker in str(error).lower()
                        for marker in ("429", "resource_exhausted", "rate limit")
                    ):
                        raise RuntimeError(
                            "Embedding failed. Saved vectors are safe; rerun the same "
                            "command when your API quota is available."
                        ) from error
                    time.sleep(35)

            collection.add(
                ids=[chunk['id']],
                embeddings=[vector],
                documents=[chunk['text']],
                metadatas=[chunk['metadata']],
            )
            written += 1
            time.sleep(3)
            if number % 25 == 0 or number == len(pending):
                print(f"Saved {number}/{len(pending)} new embeddings", flush=True)
    finally:
        client.close()
    return written


def index_file(path):
    """Reusable by the MCP add-document tool in a later step."""
    path = Path(path)
    if not path.is_file() or path.suffix.lower() != ".pdf":
        raise ValueError(f"Not a local PDF file: {path}")
    collection = get_collection()
    chunks = list(chunk_file(path))
    if not chunks:
        raise ValueError(f"No useful extractable text in {path}")
    # Do not silently mix old and revised copies of the same filename.
    prior = collection.get(where={"source": path.name}, include=["metadatas"])
    old_hashes = {m.get("document_sha256") for m in prior["metadatas"]}
    if old_hashes and old_hashes != {chunks[0]["metadata"]["document_sha256"]}:
        raise ValueError(f"{path.name} was previously indexed with different content. Rename it before adding.")
    print(f"{path.name}: {len(chunks)} chunks", flush=True)
    return embed_and_store(chunks, collection)


def main():
    download_corpus()
    paths = sorted(CORPUS_DIR.glob("*.pdf"))
    if "--preview" in sys.argv:
        total = 0
        for path in paths:
            chunks = list(chunk_file(path))
            total += len(chunks)
            print(f"{path.name}: {len(chunks)} chunks")
        print(f"TOTAL: {total} chunks; no API calls made.")
    else:
        for path in paths:
            index_file(path)
        collection = get_collection()
        print(f"Done. {collection.count()} chunks saved in index/.")


if __name__ == "__main__":
    main()
