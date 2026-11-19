"""
Assignment 3: build the index (`main.py index`).

  uv run python index.py           download, chunk (both designs), embed what has no vector yet, store
  uv run python index.py --stats   only count words and chunks (no Gemini calls, no quota)

Pipeline per file: extract_pages -> parse_document -> remove_duplicates ->
chunk (fixed or structured) -> embed_and_store. server.py imports chunk_file
and embed_and_store for its add_document tool.

Vectors are saved in index/chroma (ChromaDB) as soon as each batch comes back,
so a crash or the daily quota loses nothing: the next run embeds only what is missing.
"""

import hashlib
import json
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path

import httpx
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"  # git-ignored: the PDFs are downloaded, not committed
INDEX_DIR = ROOT / "index"    # committed: ChromaDB with the saved vectors
CHROMA_DIR = INDEX_DIR / "chroma"

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768       # smaller than the default 3072: near the same quality, a quarter of the size
EMBED_BATCH = 50      # texts per request (each text counts against the daily quota)

EMA_URL = "https://www.ema.europa.eu/en/documents/product-information/{}-epar-product-information_en.pdf"

# The three documents of the corpus.
DOCUMENTS = {name: EMA_URL.format(name) for name in ["eliquis", "xarelto", "pradaxa"]}
# Kept aside on purpose: added later with the add_document tool (task 8).
EXTRA_DOCUMENTS = {"lixiana": EMA_URL.format("lixiana")}

CHUNK_WORDS = 300     # target chunk size, in words (same for both designs, so the comparison is fair)
OVERLAP_WORDS = 50    # overlap between fixed-size chunks
SKIP_PARTS = {"Labelling"}  # carton and blister text: short, repetitive, not useful for questions


# ---------------------------------------------------------------- download and extract

def download(name: str, url: str) -> Path:
    """Download one PDF into corpus/, unless it is already there."""
    path = CORPUS_DIR / f"{name}.pdf"
    if path.exists():
        return path
    CORPUS_DIR.mkdir(exist_ok=True)
    print(f"Downloading {name} ...")
    response = httpx.get(url, follow_redirects=True, timeout=120,
                         headers={"User-Agent": "Mozilla/5.0 (student assignment)"})
    response.raise_for_status()
    path.write_bytes(response.content)
    return path


def clean(text: str) -> str:
    """Fix the usual PDF extraction problems."""
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)    # words split across lines: "antico-\nagulant"
    text = re.sub(r"[ \t]+", " ", text)             # many spaces -> one space
    text = re.sub(r"^\s*\d{1,3}\s*\n", "", text)    # page number on the first line of the page
    text = re.sub(r"\n\s*\d{1,3}\s*\n", "\n", text) # lines holding only a page number
    text = re.sub(r"\n{3,}", "\n\n", text)          # many empty lines -> one
    return text.strip()


def extract_pages(path: Path) -> list[tuple[int, str]]:
    """Return [(page_number, cleaned_text), ...] for one PDF. Pages start at 1."""
    reader = PdfReader(path)
    return [(i + 1, clean(page.extract_text() or "")) for i, page in enumerate(reader.pages)]


# ---------------------------------------------------------------- structure

@dataclass
class Paragraph:
    text: str
    page: int
    part: str        # "SmPC", "Annex II", "Labelling" or "Leaflet"
    product: str     # e.g. "Eliquis 2.5 mg film-coated tablets"
    section: str     # e.g. "4.2"
    title: str       # e.g. "Posology and method of administration"
    is_heading: bool = False


PARTS = [  # a line that starts a new part of the product information
    (re.compile(r"^ANNEX I$"), "SmPC"),
    (re.compile(r"^ANNEX II$"), "Annex II"),
    (re.compile(r"^ANNEX III$"), "Labelling"),
    (re.compile(r"^A\.\s*LABELLING$", re.I), "Labelling"),
    (re.compile(r"^(B\.\s*PACKAGE LEAFLET|Package leaflet\s*:)", re.I), "Leaflet"),
]
# "1. NAME OF THE MEDICINAL PRODUCT", "4.2 Posology and method of administration", "3. How to take Eliquis".
# Top-level numbers need their dot ("5 Patients..." inside a table is not a heading).
HEADING = re.compile(r"^(10(?=\.)|[1-9](?=\.)|[4-6]\.[1-9])\.?\s+([A-Z][^\n]{2,100})$")


def section_key(number: str) -> tuple[int, ...]:
    return tuple(int(n) for n in number.split("."))


def parse_document(pages: list[tuple[int, str]]) -> list[Paragraph]:
    """Walk the pages line by line, tracking part, product and section."""
    paragraphs: list[Paragraph] = []
    part, product, section, title = "Front", "", "", ""
    want_product = False
    lines_buffer: list[str] = []
    buffer_page = 1

    def flush():
        if lines_buffer:
            text = " ".join(lines_buffer).strip()
            if text:
                paragraphs.append(Paragraph(text, buffer_page, part, product, section, title))
            lines_buffer.clear()

    for page, text in pages:
        for raw in text.split("\n"):
            line = raw.strip()
            if not line:                       # blank line = end of a paragraph
                flush()
                continue

            new_part = next((p for rx, p in PARTS if rx.match(line)), None)
            if new_part:
                flush()
                part, section, title = new_part, "", ""
                want_product = new_part == "Leaflet"
                continue

            match = HEADING.match(line)
            # Accept a heading only if its number goes forward (or restarts at 1 for a new product),
            # so numbered lines inside tables are not mistaken for headings.
            if match and (match.group(1) == "1" or not section
                          or section_key(match.group(1)) > section_key(section)):
                flush()
                section, title = match.group(1), match.group(2).strip()
                if title.upper().startswith("NAME OF THE MEDICINAL PRODUCT"):
                    product = ""               # a new product starts here
                paragraphs.append(Paragraph(line, page, part, product, section, title, is_heading=True))
                if title.upper().startswith("NAME OF THE MEDICINAL PRODUCT"):
                    want_product = True
                continue

            if want_product and not line.lower().startswith("information for"):
                product, want_product = line, False

            if not lines_buffer:
                buffer_page = page
            lines_buffer.append(line)
        flush()                                # a paragraph never continues to the next page
    return paragraphs


def remove_duplicates(paragraphs: list[Paragraph]) -> tuple[list[Paragraph], int]:
    """Drop paragraphs that repeat earlier ones (same text for another tablet strength).

    Headings and very short paragraphs are kept: they carry the structure.
    Returns the kept paragraphs and the number of words removed.
    """
    seen, kept, removed = set(), [], 0
    for p in paragraphs:
        key = re.sub(r"\W+", " ", p.text.lower()).strip()
        if not p.is_heading and len(key.split()) >= 8:
            if key in seen:
                removed += len(p.text.split())
                continue
            seen.add(key)
        kept.append(p)
    return kept, removed


# ---------------------------------------------------------------- chunking (two designs)

def location(p: Paragraph) -> str:
    return f"{p.part} {p.section}".strip()


def make_chunk(source: str, design: str, text: str, page: int, locations: list[str], header: str) -> dict:
    chunk_id = hashlib.sha1(f"{design}|{source}|{text}".encode()).hexdigest()[:16]
    return {"id": chunk_id, "source": source, "design": design, "page": page,
            "location": ", ".join(locations), "locations": locations,
            "header": header, "text": text}


def chunk_fixed(source: str, paragraphs: list[Paragraph]) -> list[dict]:
    """Design A: windows of CHUNK_WORDS words with overlap, ignoring the structure."""
    words = [(w, p) for p in paragraphs for w in p.text.split()]
    chunks, step = [], CHUNK_WORDS - OVERLAP_WORDS
    for start in range(0, len(words), step):
        window = words[start:start + CHUNK_WORDS]
        if len(window) < 30 and chunks:        # a tiny tail is already in the previous chunk
            break
        locs = list(dict.fromkeys(location(p) for _, p in window))
        text = " ".join(w for w, _ in window)
        chunks.append(make_chunk(source, "fixed", text, window[0][1].page, locs, ""))
    return chunks


def chunk_structured(source: str, paragraphs: list[Paragraph]) -> list[dict]:
    """Design B: never cross a section; long sections are split at paragraph ends.

    Each chunk starts with a header line saying where it comes from, so the
    embedding also knows the medicine, the part and the section.
    """
    chunks, group, group_words = [], [], 0

    def flush(force: bool = False):
        nonlocal group, group_words
        body_words = sum(len(p.text.split()) for p in group if not p.is_heading)
        if body_words == 0 or (force and body_words < 15 and len(group) < 3):
            # only headings left (their text was a duplicate), or a lone title line
            group, group_words = [], 0
            return
        if body_words < 60 and not force:      # too small on its own: let the next section join it
            return
        first = group[0]
        locations = list(dict.fromkeys(location(p) for p in group))
        titles = list(dict.fromkeys(f"{p.part} {p.section} {p.title}".strip() for p in group))
        header = f"{source.capitalize()} | {first.product} | {'; '.join(titles)}"
        body = "\n".join(p.text for p in group)
        chunks.append(make_chunk(source, "structured", f"{header}\n{body}", first.page, locations, header))
        group, group_words = [], 0

    for p in paragraphs:
        n = len(p.text.split())
        last = group[-1] if group else None
        new_section = last and (p.part, p.product, p.section) != (last.part, last.product, last.section)
        if last and (p.part, p.product) != (last.part, last.product):
            flush(force=True)                  # never mix two products or two parts
        elif new_section or group_words + n > CHUNK_WORDS:
            flush(force=group_words + n > CHUNK_WORDS)
        if n > CHUNK_WORDS:                    # one very long paragraph: cut it by words
            flush(force=True)
            words = p.text.split()
            for i in range(0, len(words), CHUNK_WORDS):
                group = [Paragraph(" ".join(words[i:i + CHUNK_WORDS]), p.page, p.part, p.product, p.section, p.title)]
                group_words = len(group[0].text.split())
                flush(force=True)
            continue
        group.append(p)
        group_words += n
    flush(force=True)
    return chunks


DESIGNS = {"fixed": chunk_fixed, "structured": chunk_structured}


def chunk_file(path: Path, design: str = "structured") -> list[dict]:
    """The whole per-file pipeline: PDF -> chunks with metadata. server.py imports this."""
    source = path.stem.lower()
    paragraphs, _ = remove_duplicates(parse_document(extract_pages(path)))
    paragraphs = [p for p in paragraphs if p.part not in SKIP_PARTS]
    return DESIGNS[design](source, paragraphs)


# ---------------------------------------------------------------- embed and store

class QuotaExhausted(Exception):
    """The Gemini free tier said no more for today."""


_client = None


def gemini():
    global _client
    if _client is None:
        from google import genai
        from api_key import load_api_key
        _client = genai.Client(api_key=load_api_key())
    return _client


def document_text(chunk: dict) -> str:
    # gemini-embedding-2 takes the task as a text prefix (no task_type parameter).
    return f"title: {chunk['source']} | text: {chunk['text']}"


def query_text(query: str) -> str:
    return f"task: search result | query: {query}"


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed a batch. Waits and retries on a per-minute limit; raises QuotaExhausted if it persists."""
    from google.genai import errors, types
    for attempt in range(4):
        try:
            # gemini-embedding-2 is multimodal: a plain list of strings counts as ONE input made
            # of several parts and returns one vector. Each text must be its own Content.
            contents = [types.Content(parts=[types.Part(text=t)]) for t in texts]
            response = gemini().models.embed_content(
                model=EMBED_MODEL, contents=contents, config={"output_dimensionality": EMBED_DIM})
            vectors = [e.values for e in response.embeddings]
            if len(vectors) != len(texts):
                if len(texts) == 1:
                    raise RuntimeError(f"expected 1 vector, got {len(vectors)}")
                # Still merged: embed one text per request instead (same quota, more requests).
                return [v for t in texts for v in embed_texts([t])]
            return vectors
        except errors.APIError as error:
            if error.code != 429:
                raise
            if attempt == 3:
                raise QuotaExhausted(str(error)[:300]) from error
            print(f"  rate limit, waiting 60 s ({attempt + 1}/3) ...", file=sys.stderr)
            time.sleep(60)


def embed_query(query: str) -> list[float]:
    return embed_texts([query_text(query)])[0]


def collection(design: str):
    """The ChromaDB collection holding one design's chunks and vectors."""
    import chromadb
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return client.get_or_create_collection(name=design, metadata={"hnsw:space": "cosine"})


def metadata(chunk: dict) -> dict:
    return {"source": chunk["source"], "page": chunk["page"], "location": chunk["location"],
            "header": chunk["header"]}


def embed_and_store(chunks: list[dict], design: str) -> int:
    """Embed only the chunks without a saved vector, saving each batch at once. Returns how many were embedded."""
    store = collection(design)
    unique = {c["id"]: c for c in chunks}                      # the same text twice -> one vector
    saved = set(store.get(ids=list(unique), include=[])["ids"]) if unique else set()
    missing = [c for cid, c in unique.items() if cid not in saved]
    for start in range(0, len(missing), EMBED_BATCH):
        batch = missing[start:start + EMBED_BATCH]
        vectors = embed_texts([document_text(c) for c in batch])
        store.add(ids=[c["id"] for c in batch], embeddings=vectors,
                  documents=[c["text"] for c in batch], metadatas=[metadata(c) for c in batch])
        print(f"  {design}: saved {start + len(batch)}/{len(missing)} new vectors", flush=True)
    return len(missing)


def remove_stale(chunks: list[dict], design: str, sources: set[str]) -> int:
    """Delete stored chunks of these sources that the current code no longer produces."""
    store = collection(design)
    keep = {c["id"] for c in chunks}
    stored = store.get(include=["metadatas"])
    stale = [cid for cid, meta in zip(stored["ids"], stored["metadatas"])
             if meta["source"] in sources and cid not in keep]
    if stale:
        store.delete(ids=stale)
    return len(stale)


# ---------------------------------------------------------------- main

def stats() -> None:
    """Words and chunks per document, without any Gemini call."""
    print(f"{'document':<10} {'words':>8} {'duplicate':>10} {'labelling':>10} {'kept':>8}")
    for name, url in DOCUMENTS.items():
        paragraphs = parse_document(extract_pages(download(name, url)))
        total = sum(len(p.text.split()) for p in paragraphs)
        paragraphs, duplicate = remove_duplicates(paragraphs)
        labelling = sum(len(p.text.split()) for p in paragraphs if p.part in SKIP_PARTS)
        print(f"{name:<10} {total:>8,} {duplicate:>10,} {labelling:>10,} {total - duplicate - labelling:>8,}")
    for design in DESIGNS:
        n = sum(len(chunk_file(CORPUS_DIR / f"{name}.pdf", design)) for name in DOCUMENTS)
        print(f"{design:<11} {n:>5} chunks")


def main() -> None:
    if "--stats" in sys.argv:
        stats()
        return
    paths = [download(name, url) for name, url in DOCUMENTS.items()]
    # The structured design first: it is the one we expect to keep, so it gets today's quota first.
    for design in ["structured", "fixed"]:
        chunks = [c for path in paths for c in chunk_file(path, design)]
        CORPUS_DIR.joinpath(f"chunks_{design}.jsonl").write_text(
            "".join(json.dumps(c, ensure_ascii=False) + "\n" for c in chunks), encoding="utf-8")
        removed = remove_stale(chunks, design, {p.stem for p in paths})
        print(f"{design}: {len(chunks)} chunks" + (f", removed {removed} stale" if removed else ""))
        try:
            new = embed_and_store(chunks, design)
        except QuotaExhausted as error:
            print(f"\nDaily embedding quota reached. Everything embedded so far is saved.\n"
                  f"Run `uv run python main.py index` again after 09:00 (Spain) to continue.\n({error})")
            return
        print(f"{design}: {new} embedded now, {collection(design).count()} stored in total")
    print("\nIndex complete.")


if __name__ == "__main__":
    main()
