"""
Assignment 3: build the index (`main.py index`).

1. Download the corpus into corpus/ (git-ignored).
2. Extract the text page by page and clean it.
3. Cut each page into overlapping chunks of about 200 words, keeping the
   document and page number of every chunk.
4. Embed the chunks with Gemini (one request per chunk) and store them in a ChromaDB index in index/.
   Each batch is saved as soon as it is embedded, and chunks that already have
   a vector are skipped, so a crash or the daily limit loses nothing.

The per-file steps are functions (`chunk_file`, `embed_and_store`), so
server.py's add-document tool can import them instead of rewriting them.
"""

import logging
import re
import sys
import time
from pathlib import Path

import chromadb
import httpx
from google import genai
from pypdf import PdfReader

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"
COLLECTION = "eic_chunks"

CHUNK_WORDS = 200  # words per chunk
OVERLAP_WORDS = 40  # words shared with the previous chunk, so a sentence cut at the edge is not lost

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768  # smaller than the default 3072: keeps index/ small, with little loss in quality
BATCH_SIZE = 20  # chunks embedded before each save to index/

# pypdf prints harmless "Ignoring wrong pointing object" warnings for the Work Programme PDF.
logging.getLogger("pypdf").setLevel(logging.ERROR)

# The corpus. `source` is the short name used in chunk metadata and in eval/questions.csv.
DOCUMENTS = [
    {
        "source": "work_programme_2027",
        "title": "EIC Work Programme 2027",
        "url": "https://eic.ec.europa.eu/document/download/ed9ab103-1ffb-4d5f-a6ad-168ac3b36900_en?filename=EIC-2027-Work-Programme.pdf",
        "file": "EIC-2027-Work-Programme.pdf",
    },
    {
        "source": "accelerator_guide",
        "title": "EIC Accelerator Guide for Applicants v6.0",
        "url": "https://eic.ec.europa.eu/document/download/9d96fbf3-4d85-4ad0-9483-c77ce348111d_en?filename=EIC%20Accelerator%20guide%20for%20applicants_WP26.pdf",
        "file": "EIC Accelerator guide for applicants_WP26.pdf",
    },
    {
        "source": "investment_guidelines",
        "title": "EIC Fund Investment Guidelines (August 2026)",
        "url": "https://eic.ec.europa.eu/document/download/6df458e7-fa47-4ace-93fa-86099606bdb0_en?filename=EIC_Fund_Investment_2026_guidelines_f.pdf",
        "file": "EIC_Fund_Investment_2026_guidelines_f.pdf",
    },
]


def download(doc: dict) -> Path:
    """Download one document into corpus/, unless it is already there."""
    CORPUS_DIR.mkdir(exist_ok=True)
    path = CORPUS_DIR / doc["file"]
    if path.exists():
        return path
    print(f"Downloading {doc['title']} ...")
    response = httpx.get(doc["url"], follow_redirects=True, timeout=120)
    response.raise_for_status()
    path.write_bytes(response.content)
    return path


def extract_pages(path: Path) -> list[tuple[int, str]]:
    """Return (page number, raw text) for every page of a PDF. Page numbers start at 1."""
    reader = PdfReader(path)
    return [(i + 1, page.extract_text() or "") for i, page in enumerate(reader.pages)]


# Lines that repeat on every page and carry no content.
HEADER_PATTERNS = [
    re.compile(r"^EIC Accelerator \| Guide for applicants.*\| ?P\d+$"),  # header of the Guide
    re.compile(r"^\d{1,3}$"),  # a page number on its own line
]
TOC_LINE = re.compile(r"\.{5,}\s*\d+\s*$")  # "Introduction ........ 6" in a table of contents


def clean_page(text: str) -> str:
    """Clean the text of one page: drop headers, page numbers and table-of-contents lines,
    repair words that the PDF split with a stray space, and normalise whitespace."""
    lines = []
    for line in text.splitlines():
        line = line.strip()
        if not line or TOC_LINE.search(line):
            continue
        if any(p.match(line) for p in HEADER_PATTERNS):
            continue
        lines.append(line)
    text = "\n".join(lines)
    # "high -risk" -> "high-risk", "co -investment" -> "co-investment"
    text = re.sub(r"(\w) -(\w)", r"\1-\2", text)
    # A word broken across lines with a hyphen: "invest-\nment" -> "investment"
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)
    # Join the lines of a paragraph; keep text compact.
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n+", " ", text)
    return text.strip()


def load_pages(path: Path, source: str, title: str) -> list[dict]:
    """Extract and clean one PDF. Returns one record per page that has real text."""
    pages = []
    for page_number, raw in extract_pages(path):
        text = clean_page(raw)
        if len(text.split()) < 20:  # cover pages, blank pages, pure tables of contents
            continue
        pages.append({"source": source, "title": title, "page": page_number, "text": text})
    return pages


def chunk_pages(pages: list[dict]) -> list[dict]:
    """Cut every page into chunks of CHUNK_WORDS words that overlap by OVERLAP_WORDS.
    A chunk never crosses a page, so its page number is always exact."""
    step = CHUNK_WORDS - OVERLAP_WORDS
    chunks = []
    for page in pages:
        words = page["text"].split()
        starts = range(0, max(len(words) - OVERLAP_WORDS, 1), step)
        for i, start in enumerate(starts):
            piece = words[start:start + CHUNK_WORDS]
            chunks.append({
                "id": f"{page['source']}-p{page['page']:03d}-c{i}",
                "text": " ".join(piece),
                "source": page["source"],
                "title": page["title"],
                "page": page["page"],
                "words": len(piece),
            })
    return chunks


def chunk_file(path: Path, source: str | None = None, title: str | None = None) -> list[dict]:
    """Extract, clean and chunk one PDF file. Used for the corpus and by add_document."""
    path = Path(path)
    source = source or re.sub(r"\W+", "_", path.stem).strip("_").lower()
    title = title or path.stem
    return chunk_pages(load_pages(path, source, title))


def get_collection():
    """Open (or create) the ChromaDB collection stored in index/."""
    client = chromadb.PersistentClient(path=str(INDEX_DIR), settings=chromadb.Settings(anonymized_telemetry=False))
    return client.get_or_create_collection(COLLECTION, metadata={"hnsw:space": "cosine"})


def embed_one(client: genai.Client, text: str) -> list[float]:
    """Embed one text, waiting and retrying if we hit the per-minute rate limit.
    (gemini-embedding-2 merges a list of texts into ONE vector, so we send them one by one.)"""
    for attempt in range(6):
        try:
            result = client.models.embed_content(
                model=EMBED_MODEL, contents=text, config={"output_dimensionality": EMBED_DIM}
            )
            return result.embeddings[0].values
        except genai.errors.ClientError as error:
            if error.code != 429 or attempt == 5:
                raise
            print("  Rate limit reached, waiting 60 seconds ...", file=sys.stderr)
            time.sleep(60)


def embed_texts(client: genai.Client, texts: list[str]) -> list[list[float]]:
    """Embed a batch of texts, one request each."""
    vectors = []
    for text in texts:
        vectors.append(embed_one(client, text))
        time.sleep(0.7)  # stay under the free tier's requests-per-minute limit
    return vectors


def document_text(chunk: dict) -> str:
    """What we embed for a chunk: its title and page, then its text (the format Google suggests)."""
    return f"title: {chunk['title']}, page {chunk['page']} | text: {chunk['text']}"


def embed_and_store(chunks: list[dict], collection=None) -> int:
    """Embed the chunks that are not in the index yet and save them, batch by batch.
    Returns how many chunks were added."""
    collection = collection or get_collection()
    existing = set(collection.get(ids=[c["id"] for c in chunks], include=[])["ids"]) if chunks else set()
    todo = [c for c in chunks if c["id"] not in existing]
    if not todo:
        return 0
    client = genai.Client(api_key=load_api_key())
    added = 0
    for i in range(0, len(todo), BATCH_SIZE):
        batch = todo[i:i + BATCH_SIZE]
        vectors = embed_texts(client, [document_text(c) for c in batch])
        collection.add(
            ids=[c["id"] for c in batch],
            embeddings=vectors,
            documents=[c["text"] for c in batch],
            metadatas=[{k: c[k] for k in ("source", "title", "page", "words")} for c in batch],
        )
        added += len(batch)
        print(f"  embedded and saved {added}/{len(todo)} chunks", file=sys.stderr)  # stderr: stdout is the MCP channel
    return added


def main() -> None:
    collection = get_collection()
    total_chunks = 0
    for doc in DOCUMENTS:
        chunks = chunk_file(download(doc), doc["source"], doc["title"])
        total_chunks += len(chunks)
        print(f"{doc['title']}: {len(chunks)} chunks")
        added = embed_and_store(chunks, collection)
        print(f"  {added} new chunks embedded, {len(chunks) - added} already in the index")
    print(f"Done: {total_chunks} chunks, {collection.count()} in the index.")


if __name__ == "__main__":
    main()
