"""
Assignment 3: build the index (`main.py index`). May be index.ipynb instead.

Download the corpus (into corpus/, git-ignored), extract, clean and chunk it
with source and location metadata, embed with Gemini, and store everything in
index/. Save each vector as you get it and embed only chunks without one.

Write the per-file steps as functions (e.g. `chunk_file(path)`,
`embed_and_store(chunks)`): server.py's add-document tool imports them.
"""
import hashlib
import os
import re
import sqlite3
import sys
from pathlib import Path
from urllib.request import Request, urlopen
import numpy as np
from bs4 import BeautifulSoup
from google import genai
from google.genai import types
from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
CORPUS = ROOT / "corpus"
INDEX = Path(os.environ.get("RAG_INDEX_DIR", ROOT / "index"))
MODEL = "gemini-embedding-2"
SIZE = 450
OVERLAP = 60
DIM = 768
BOOKS = {"bagehot": (4359, "Lombard Street", 1873),
        "peace": (15776, "The Economic Consequences of the Peace", 1919),
        "tract": (65278, "A Tract on Monetary Reform", 1923),}
BASE = ("bagehot", "peace", "tract")

# 1. DATABASE
def connect():
    INDEX.mkdir(exist_ok=True, parents=True)

    db = sqlite3.connect(INDEX / "corpus.sqlite", timeout=60)
    db.row_factory = sqlite3.Row

    db.executescript("""
        CREATE TABLE IF NOT EXISTS chunks (
            id TEXT PRIMARY KEY,
            source TEXT,
            location TEXT,
            text TEXT,
            document_hash TEXT,
            vector BLOB);

        CREATE TABLE IF NOT EXISTS documents (
            source TEXT PRIMARY KEY,
            hash TEXT,
            words INTEGER,
            chunks INTEGER);

        CREATE TABLE IF NOT EXISTS queries (
            id TEXT PRIMARY KEY,
            vector BLOB);

        CREATE TABLE IF NOT EXISTS settings (
            key TEXT PRIMARY KEY,
            value TEXT);""")

    signature = f"{MODEL}:{DIM}:{SIZE}:{OVERLAP}:v1"

    saved = db.execute("SELECT value FROM settings WHERE key='index_signature'").fetchone()

    if saved and saved["value"] != signature:
        db.close()
        raise RuntimeError("Index settings have changed.")

    db.execute("INSERT OR IGNORE INTO settings VALUES (?, ?)", ("index_signature", signature))

    db.commit()
    return db

# 2. DOWNLOAD
def download(key):
    number, title, _ = BOOKS[key]
    CORPUS.mkdir(exist_ok=True)
    path = CORPUS / f"{key}.html"
    if path.exists() and path.stat().st_size > 10000:
        print(f"Already downloaded: {title}")
        return path

    urls = [
        f"https://www.gutenberg.org/cache/epub/{number}/pg{number}-images.html",
        f"https://dev.gutenberg.org/cache/epub/{number}/pg{number}-images.html",
        f"https://gutenberg-test.ibiblio.org/cache/epub/{number}/pg{number}-images.html",
        f"https://www.gutenberg.org/files/{number}/{number}-h/{number}-h.htm",]

    for url in urls:
        try:
            print(f"Downloading {title}...")
            print(f"Trying: {url}")
            request = Request(url,headers={"User-Agent": "Academic RAG Project"})
            with urlopen(request, timeout=30) as response:
                data = response.read()
            if len(data) < 10000:
                raise ValueError("Document too short")
            soup = BeautifulSoup(data, "html.parser")
            if title.lower() not in soup.get_text(" ", strip=True).lower():
                raise ValueError("Unexpected document content")
            temporary = path.with_suffix(".tmp")
            temporary.write_bytes(data)
            temporary.replace(path)
            print(f"Successfully downloaded: {title}")
            return path
        except Exception as error:
            print(f"Download failed: {error}")
    raise RuntimeError(f"All download sources failed for {title}")

# 3. CLEANING
def clean(text):
    text = re.sub(r"\[Pg\s+[ivxlcdm\d]+\]", "", text, flags=re.I)
    return re.sub(r"\s+", " ", text).strip()

# 4. SECTION EXTRACTION
def sections(path):
    path = Path(path)

    if path.suffix.lower() == ".pdf":
        from pypdf import PdfReader
        return [(f"Page {i}", clean(page.extract_text() or "")) for i, page in enumerate(PdfReader(path).pages, 1)]

    if path.suffix.lower() in (".txt", ".md"):
        return [("Section 1", clean(path.read_text(encoding="utf-8-sig")))]

    if path.suffix.lower() not in (".html", ".htm"):
        raise ValueError("Unsupported file format")
    soup = BeautifulSoup(path.read_bytes(), "html.parser")
    for node in soup.select("script, style, nav, .pagenum, .pgheader, .pgfooter, ""#pg-header, #pg-footer, #pg-start-separator, ""#pg-end-separator"):
        node.decompose()
    output = []
    parts = []
    location = None

    for node in soup.body.find_all(["h1", "h2", "h3", "h4", "p", "blockquote", "table", "pre", "div"]):
        if node.name == "div" and node.find(["h1", "h2", "h3", "h4", "p", "blockquote", "table", "pre", "div"]):
            continue

        if node.find_parent(["table", "blockquote", "pre", "p", "h1", "h2", "h3", "h4"]):
            continue

        if node.find_parent(class_=re.compile(r"(^|[-_ ])toc($|[-_ ])|contents", re.I)):
            continue

        text = clean(node.get_text(" ", strip=True))
        if not text:
            continue

        if re.search(r"END OF (THE |THIS )?PROJECT GUTENBERG", text, re.I):
            break
        match = re.match(r"^chapter\s+([ivxlcdm]+|\d+)\b", text, re.I)

        if match and node.name in ("h1", "h2", "h3", "h4"):
            if location and parts:
                output.append((location, " ".join(parts)))
            location = "Chapter " + match.group(1).upper()
            parts = [text]
        elif location:
            parts.append(text)
    if location and parts:
        output.append((location, " ".join(parts)))
    if output:
        longest = {}
        for location, text in output:
            if len(text) > len(longest.get(location, "")):
                longest[location] = text
        return [(location, text) for location, text in longest.items() if len(text.split()) >= 30]

    return [("Section 1", clean(soup.get_text(" ", strip=True)))]

# 5. CHUNKING AND METADATA
def chunk_file(path):
    path = Path(path)
    source = path.stem

    if not re.fullmatch(r"[A-Za-z0-9_-]+", source):
        raise ValueError("Invalid source filename")

    document_hash = hashlib.sha256(path.read_bytes()).hexdigest()
    document_sections = sections(path)

    words = sum(len(text.split()) for _, text in document_sections)
    chunks = []

    for location, text in document_sections:

        tokens = text.split()

        for start in range(0, len(tokens), SIZE - OVERLAP):
            window = tokens[start:start + SIZE]
            if not window:
                break
            number = 1 + start // (SIZE - OVERLAP)
            chunk_id = f"{source}|{location}|{number:03d}"
            chunks.append((chunk_id, source, location, " ".join(window), document_hash))
            if start + SIZE >= len(tokens):
                break

    if not chunks:
        raise ValueError(f"No extractable text: {path}")

    if source in BOOKS and len(document_sections) < 4:
        raise ValueError(f"Chapter extraction failed for {source}")
    return chunks, words, document_hash

# 6. EMBEDDINGS
def embed(text, query=False, title="none"):
    import time
    from google.genai.errors import ClientError
    client = genai.Client(api_key=load_api_key())
    if query:
        content = f"task: search result | query: {text}"
    else:
        content = f"title: {title} | text: {text}"
    for attempt in range(10):
        try:
            response = client.models.embed_content(model=MODEL, contents=content, config=types.EmbedContentConfig(output_dimensionality=DIM))
            break

        except ClientError as error:
            if error.code != 429 or attempt == 9:
                raise
            message = str(error)
            if "per day" in message.lower():
                raise

            match = re.search(r"retry in ([\d.]+)s", message)
            wait = float(match.group(1)) + 2 if match else 65

            print(f"Rate limit reached. Retrying in {wait:.1f}s...", flush=True)
            time.sleep(wait)

    vector = np.asarray(response.embeddings[0].values, dtype=np.float32)
    norm = np.linalg.norm(vector)
    if len(vector) != DIM or not np.isfinite(norm) or norm == 0:
        raise ValueError("Invalid embedding")
    return vector / norm

# 7. INCREMENTAL INDEXING
def embed_and_store(path):
    chunks, words, document_hash = chunk_file(path)
    source = chunks[0][1]

    with connect() as db:
        existing = db.execute("SELECT hash FROM documents WHERE source=?", (source,)).fetchone()

        if existing and existing["hash"] != document_hash:
            raise ValueError("A different document has the same source name.")

        db.execute("INSERT OR IGNORE INTO documents VALUES (?, ?, ?, ?)", (source, document_hash, words, len(chunks)))

        db.executemany("""
            INSERT OR IGNORE INTO chunks
            (id, source, location, text, document_hash)
            VALUES (?, ?, ?, ?, ?)
        """, chunks)

        db.commit()

        pending = db.execute("""
            SELECT id, text
            FROM chunks
            WHERE source=? AND vector IS NULL
            ORDER BY id
        """, (source,)).fetchall()
        print(f"\n{source}: {len(pending)} new embeddings needed.", flush=True)
        title = BOOKS.get(source, (0, source, 0))[1]
        for i, row in enumerate(pending, 1):
            vector = embed(row["text"], title=title)
            db.execute("UPDATE chunks SET vector=? WHERE id=?", (vector.tobytes(), row["id"]))
            db.commit()
            print(f"{source}: {i}/{len(pending)} embeddings saved", flush=True)
    return {"source": source, "words": words, "chunks": len(chunks), "new_vectors": len(pending), "status": "indexed" if pending else "already indexed"}

#8. QUERY EMBEDDING CACHE
def query_vector(query):
    key = hashlib.sha256(f"{MODEL}:{DIM}:{query}".encode()).hexdigest()

    with connect() as db:
        existing = db.execute("SELECT vector FROM queries WHERE id=?",(key,)).fetchone()

        if existing:
            return np.frombuffer(existing["vector"], dtype=np.float32)
        vector = embed(query, query=True)
        db.execute("INSERT OR IGNORE INTO queries VALUES (?, ?)", (key, vector.tobytes()))
        db.commit()
        return vector

#9. MAIN PIPELINE
def main():
    # Reuse the complete committed index.
    if "--preview" not in sys.argv:
        with connect() as db:
            complete = True

            for key in BASE:
                doc = db.execute(
                    "SELECT chunks, hash FROM documents WHERE source=?",
                    (key,)
                ).fetchone()

                count, valid = db.execute(
                    "SELECT COUNT(*), "
                    "SUM(CASE WHEN length(vector)=? "
                    "AND document_hash=? THEN 1 ELSE 0 END) "
                    "FROM chunks WHERE source=?",
                    (DIM * 4, doc["hash"] if doc else "", key)
                ).fetchone()

                if (
                    not doc
                    or count == 0
                    or count != doc["chunks"]
                    or valid != count
                ):
                    complete = False
                    break

            if complete:
                print("Base corpus already indexed; 0 new embeddings needed.")
                return

    paths = [download(key) for key in BASE]
    prepared = [chunk_file(path) for path in paths]
    total_words = sum(item[1] for item in prepared)
    total_chunks = sum(len(item[0]) for item in prepared)

    for path, (chunks, words, _) in zip(paths, prepared):
        print(f"{path.stem}: {words:,} words, {len(chunks)} chunks")
    print(f"\nTotal words: {total_words:,}")
    print(f"Total chunks: {total_chunks}")

    if total_words < 50000:
        raise ValueError("Corpus must have at least 50,000 words")
    if "--preview" in sys.argv:
        print("\nPreview complete. No API calls made.")
        return
    for path in paths:
        print(embed_and_store(path))
    print("\nIndex built successfully.")

if __name__ == "__main__":
    main()
