"""
Assignment 3: build the index (`main.py index`).

Extract, clean and chunk PDFs from docs/, embed with Gemini, store in ChromaDB.
Two chunking designs for comparison: fixed-size and structure-based.
Functions are importable by server.py's add-document tool.
"""

import hashlib
import re
import sys
import time
from pathlib import Path

import chromadb
from google import genai
from pypdf import PdfReader

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
DOCS_DIR = ROOT / "docs"
INDEX_DIR = ROOT / "index"
CHROMA_DIR = INDEX_DIR / "chroma"

EMBEDDING_MODEL = "gemini-embedding-2"
EMBED_BATCH_SIZE = 50  # chunks to store per ChromaDB add() call
EMBED_DELAY = 0.5     # seconds between individual embed calls


# ---------------------------------------------------------------------------
# PDF extraction
# ---------------------------------------------------------------------------

def extract_pdf(path: Path) -> list[dict]:
    """Extract text page by page. Returns [{"page": int, "text": str}, ...]."""
    reader = PdfReader(path)
    pages = []
    for i, page in enumerate(reader.pages):
        text = page.extract_text() or ""
        if text.strip():
            pages.append({"page": i + 1, "text": text})
    return pages


def clean_text(text: str) -> str:
    """Remove boilerplate, excessive whitespace, standalone page numbers."""
    text = re.sub(r"\n{3,}", "\n\n", text)
    text = re.sub(r" {2,}", " ", text)
    # Copyright Office footer
    text = re.sub(
        r"(?i)copyright\.gov\s*$", "", text, flags=re.MULTILINE
    )
    # Standalone page numbers
    text = re.sub(r"^\s*\d{1,3}\s*$", "", text, flags=re.MULTILINE)
    # Federal Register header lines (page range)
    text = re.sub(
        r"^\d{4,6}\s+Federal Register.*$", "", text, flags=re.MULTILINE
    )
    return text.strip()


def source_name(path: Path) -> str:
    """Short, stable source name from a filename."""
    return path.stem


# ---------------------------------------------------------------------------
# Chunking — Design 1: fixed size
# ---------------------------------------------------------------------------

def chunk_fixed(
    pages: list[dict],
    source: str,
    chunk_words: int = 375,
    overlap_words: int = 50,
) -> list[dict]:
    """Fixed-size chunks of ~500 tokens with overlap."""
    all_words: list[str] = []
    word_pages: list[int] = []
    for p in pages:
        cleaned = clean_text(p["text"])
        for w in cleaned.split():
            all_words.append(w)
            word_pages.append(p["page"])

    chunks: list[dict] = []
    i = 0
    num = 0
    while i < len(all_words):
        end = min(i + chunk_words, len(all_words))
        text = " ".join(all_words[i:end])
        sp = word_pages[i]
        ep = word_pages[end - 1]
        loc = f"p.{sp}" if sp == ep else f"p.{sp}-{ep}"
        num += 1
        chunks.append(
            {
                "chunk_id": f"{source}__fixed__{num:03d}",
                "text": text,
                "source": source,
                "location": loc,
                "design": "fixed",
                "content_hash": hashlib.sha256(text.encode()).hexdigest()[:16],
            }
        )
        i += max(chunk_words - overlap_words, 1)
    return chunks


# ---------------------------------------------------------------------------
# Chunking — Design 2: structure-based
# ---------------------------------------------------------------------------

_HEADING_RE = [
    re.compile(r"^Article\s+\d+", re.IGNORECASE),
    re.compile(r"^§\s*\d+"),
    re.compile(r"^(CHAPTER|TITLE|PART)\s+", re.IGNORECASE),
    re.compile(r"^Section\s+\d+", re.IGNORECASE),
]


def _is_heading(line: str) -> bool:
    """Heuristic: does *line* look like a section heading?"""
    line = line.strip()
    if not line or len(line) > 120 or len(line) < 3:
        return False
    for pat in _HEADING_RE:
        if pat.match(line):
            return True
    # Short title-case line without trailing period
    if len(line) < 80 and not line.endswith((".", ",")):
        words = line.split()
        if len(words) >= 2 and words[0][0].isupper():
            caps = sum(
                1
                for w in words
                if w[0].isupper()
                or w.lower()
                in ("a", "an", "the", "of", "in", "for", "and", "or", "to", "with", "by", "on", "vs", "from")
            )
            if caps >= len(words) * 0.6:
                return True
    return False


def chunk_structure(
    pages: list[dict],
    source: str,
    max_words: int = 600,
    min_words: int = 40,
) -> list[dict]:
    """Structure-based: split on detected headings, prefix each chunk."""
    lines: list[dict] = []
    for p in pages:
        cleaned = clean_text(p["text"])
        for raw_line in cleaned.split("\n"):
            lines.append({"text": raw_line, "page": p["page"]})

    # Group into sections
    sections: list[dict] = []
    cur_heading = source
    cur_lines: list[str] = []
    cur_page = pages[0]["page"] if pages else 1

    for item in lines:
        line = item["text"].strip()
        if not line:
            if cur_lines:
                cur_lines.append("")
            continue
        if _is_heading(line) and cur_lines:
            text = "\n".join(cur_lines).strip()
            if text:
                sections.append({"heading": cur_heading, "text": text, "page": cur_page})
            cur_heading = line
            cur_lines = []
            cur_page = item["page"]
        else:
            if not cur_lines:
                cur_page = item["page"]
            cur_lines.append(line)

    if cur_lines:
        text = "\n".join(cur_lines).strip()
        if text:
            sections.append({"heading": cur_heading, "text": text, "page": cur_page})

    # Build chunks, splitting long sections
    chunks: list[dict] = []
    num = 0

    for sec in sections:
        heading = sec["heading"]
        text = sec["text"]
        page = sec["page"]
        words = text.split()

        if len(words) < min_words and chunks:
            # merge tiny section into previous
            prev = chunks[-1]
            prev["text"] += f"\n\n{heading}\n{text}"
            prev["content_hash"] = hashlib.sha256(prev["text"].encode()).hexdigest()[:16]
            continue

        if len(words) <= max_words:
            prefixed = f"{heading}\n\n{text}" if heading != source else text
            num += 1
            chunks.append(
                {
                    "chunk_id": f"{source}__struct__{num:03d}",
                    "text": prefixed,
                    "source": source,
                    "location": f"p.{page}, {heading}",
                    "design": "structure",
                    "content_hash": hashlib.sha256(prefixed.encode()).hexdigest()[:16],
                }
            )
        else:
            for start in range(0, len(words), max_words):
                sub = " ".join(words[start : start + max_words])
                prefixed = f"{heading}\n\n{sub}"
                num += 1
                chunks.append(
                    {
                        "chunk_id": f"{source}__struct__{num:03d}",
                        "text": prefixed,
                        "source": source,
                        "location": f"p.{page}, {heading}",
                        "design": "structure",
                        "content_hash": hashlib.sha256(prefixed.encode()).hexdigest()[:16],
                    }
                )
    return chunks


def chunk_file(path: Path, design: str = "structure") -> list[dict]:
    """Chunk a single PDF.  Importable by server.py's add-document tool."""
    pages = extract_pdf(path)
    src = source_name(path)
    if design == "fixed":
        return chunk_fixed(pages, src)
    return chunk_structure(pages, src)


# ---------------------------------------------------------------------------
# Embedding & storage
# ---------------------------------------------------------------------------

def load_db() -> chromadb.ClientAPI:
    """Return a persistent ChromaDB client rooted in index/chroma."""
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(CHROMA_DIR))


def get_collection(db: chromadb.ClientAPI, name: str) -> chromadb.Collection:
    return db.get_or_create_collection(name=name, metadata={"hnsw:space": "cosine"})


def _embed_texts(texts: list[str], client: genai.Client) -> list[list[float]]:
    """Embed each text individually (the Gemini API concatenates lists)."""
    embeddings: list[list[float]] = []
    for i, text in enumerate(texts):
        result = client.models.embed_content(model=EMBEDDING_MODEL, contents=text)
        embeddings.append(result.embeddings[0].values)
        if i < len(texts) - 1:
            time.sleep(EMBED_DELAY)
    return embeddings


def embed_and_store(chunks: list[dict], collection_name: str = "structure_chunks") -> int:
    """Embed new chunks and add them to ChromaDB.  Returns count of newly stored chunks."""
    if not chunks:
        return 0

    db = load_db()
    collection = get_collection(db, collection_name)

    existing_ids: set[str] = set()
    try:
        existing_ids = set(collection.get()["ids"])
    except Exception:
        pass

    new_chunks = [c for c in chunks if c["chunk_id"] not in existing_ids]
    if not new_chunks:
        print(f"  All {len(chunks)} chunks already in '{collection_name}'.", file=sys.stderr)
        return 0

    print(f"  Embedding {len(new_chunks)} new chunks for '{collection_name}' …", file=sys.stderr)
    client = genai.Client(api_key=load_api_key())
    embedded = 0

    for i in range(0, len(new_chunks), EMBED_BATCH_SIZE):
        batch = new_chunks[i : i + EMBED_BATCH_SIZE]
        texts = [c["text"] for c in batch]
        embeddings = _embed_texts(texts, client)

        collection.add(
            ids=[c["chunk_id"] for c in batch],
            embeddings=embeddings,
            documents=texts,
            metadatas=[
                {
                    "source": c["source"],
                    "location": c["location"],
                    "design": c["design"],
                    "content_hash": c["content_hash"],
                }
                for c in batch
            ],
        )
        embedded += len(batch)
        print(f"    {embedded}/{len(new_chunks)}", file=sys.stderr)

    return embedded


# ---------------------------------------------------------------------------
# Search (used by server.py and agent.py)
# ---------------------------------------------------------------------------

def search_index(
    query: str, k: int = 5, collection_name: str = "structure_chunks"
) -> list[dict]:
    """Return the *k* most relevant chunks for *query*."""
    db = load_db()
    try:
        collection = db.get_collection(collection_name)
    except Exception:
        return []
    if collection.count() == 0:
        return []

    client = genai.Client(api_key=load_api_key())
    qvec = client.models.embed_content(model=EMBEDDING_MODEL, contents=[query])
    query_emb = qvec.embeddings[0].values

    results = collection.query(
        query_embeddings=[query_emb], n_results=min(k, collection.count())
    )

    out: list[dict] = []
    for i in range(len(results["ids"][0])):
        dist = results["distances"][0][i] if results["distances"] else 0.0
        out.append(
            {
                "chunk_id": results["ids"][0][i],
                "text": results["documents"][0][i],
                "source": results["metadatas"][0][i]["source"],
                "location": results["metadatas"][0][i]["location"],
                "score": round(1 - dist, 4),
            }
        )
    return out


# ---------------------------------------------------------------------------
# File-level content hash (for add-document dedup)
# ---------------------------------------------------------------------------

def file_content_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


# ---------------------------------------------------------------------------
# Main: build index from docs/
# ---------------------------------------------------------------------------

def build_index() -> None:
    if not DOCS_DIR.is_dir():
        print(f"ERROR: {DOCS_DIR} not found.", file=sys.stderr)
        sys.exit(1)

    pdfs = sorted(DOCS_DIR.glob("*.pdf"))
    if not pdfs:
        print(f"ERROR: no PDFs in {DOCS_DIR}.", file=sys.stderr)
        sys.exit(1)

    print(f"Found {len(pdfs)} PDFs in {DOCS_DIR}.", file=sys.stderr)

    all_fixed: list[dict] = []
    all_struct: list[dict] = []

    for pdf in pdfs:
        print(f"\n--- {pdf.name} ---", file=sys.stderr)
        fc = chunk_file(pdf, "fixed")
        sc = chunk_file(pdf, "structure")
        print(f"  fixed={len(fc)}  structure={len(sc)}", file=sys.stderr)
        all_fixed.extend(fc)
        all_struct.extend(sc)

    total = len(all_fixed) + len(all_struct)
    print(f"\nChunks: {len(all_fixed)} fixed + {len(all_struct)} structure = {total}", file=sys.stderr)
    if total > 950:
        print("WARNING: may approach daily embedding limit (~1 000).", file=sys.stderr)

    n1 = embed_and_store(all_fixed, "fixed_chunks")
    n2 = embed_and_store(all_struct, "structure_chunks")

    print(f"\nNewly embedded: {n1} fixed + {n2} structure = {n1 + n2}", file=sys.stderr)
    print(f"Index stored in {INDEX_DIR}/", file=sys.stderr)


if __name__ == "__main__":
    build_index()
