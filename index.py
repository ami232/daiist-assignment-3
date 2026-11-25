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
from collections import Counter
from pathlib import Path

import chromadb
import pypdf
from google import genai
from google.genai import types

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
CORPUS = ROOT / "corpus"
INDEX_DIR = ROOT / "index"
EMBED_MODEL = "gemini-embedding-2"

# The parts of each PDF we use. Pages are PDF page numbers (1 = first page).
SOURCES = [
    {"doc": "FDA Food Code 2022", "kind": "food_code", "file": "fda_food_code_2022.pdf", "first": 44, "last": 106},
    {"doc": "FDA Bad Bug Book (2nd ed.)", "kind": "bad_bug", "file": "bad_bug_book.pdf", "first": 11, "last": 110},
    {"doc": "USDA FSIS Safe Temperature Chart", "kind": "chart", "file": "fsis_safe_temperature_chart.pdf", "first": 1, "last": 99},
]

# The two chunking designs we compare.
DESIGNS = {
    "A": {"max_words": 150, "respect_sections": False},  # fixed size
    "B": {"max_words": 250, "respect_sections": True},   # follows the document structure
}
MIN_WORDS = 40  # in design B, smaller leftovers are merged into the previous chunk


# ---------- 1. Extract ----------

def extract_pages(source):
    """Return a list of (pdf_page_number, raw_text) for the pages we use."""
    reader = pypdf.PdfReader(CORPUS / source["file"])
    last = min(source["last"], len(reader.pages))
    return [(n, reader.pages[n - 1].extract_text() or "") for n in range(source["first"], last + 1)]


# ---------- 2. Clean ----------

def shape(line):
    """A line with every number replaced by '#', so 'page 12' and 'page 13' look the same."""
    return re.sub(r"\d+", "#", line)


def find_repeated_lines(pages, share=0.3):
    """Shapes of lines that appear on at least 30% of the pages: running headers, footers, page numbers."""
    counts = Counter()
    for _, text in pages:
        counts.update({shape(ln.strip()) for ln in text.splitlines() if ln.strip()})
    limit = max(3, share * len(pages))
    return {s for s, n in counts.items() if n >= limit}


def clean_pages(pages):
    """Drop the repeated header/footer lines. Return [(pdf_page_number, [clean lines])]."""
    repeated = find_repeated_lines(pages)
    cleaned = []
    for number, text in pages:
        lines = [ln.strip() for ln in text.splitlines() if ln.strip()]
        cleaned.append((number, [ln for ln in lines if shape(ln) not in repeated]))
    return cleaned


# ---------- 3. Label every line with its location ----------

FOOD_CODE_SECTION = re.compile(r"^(\d-\d{3}\.\d{2})\s+[A-Z]")   # e.g. "3-401.11 Raw Animal Foods."
BAD_BUG_MARK = re.compile(r"For Consumers:\s+A Snapshot")         # every organism chapter has this line
TITLE_FIXES = {"Bacil lus": "Bacillus"}                           # a word the PDF itself splits in two


def bad_bug_title(lines, i):
    """Organism name: the lines above the marker (top of the page) plus the text before it on its own line."""
    match = BAD_BUG_MARK.search(lines[i])
    head = lines[i][:match.start()].strip()
    title = " ".join(lines[:i] + ([head] if head else []))
    for wrong, right in TITLE_FIXES.items():
        title = title.replace(wrong, right)
    if len(title.split()) > 12:   # too long to be a title: something else is above the marker
        title = head or title
    return title


def label_lines(source, cleaned):
    """Turn cleaned pages into (location, pdf_page, line) triples.
    Location = Food Code section number, Bad Bug Book organism, or the chart's name."""
    location = "Safe Minimum Internal Temperature Chart" if source["kind"] == "chart" else source["doc"]
    units = []
    for page, lines in cleaned:
        if source["kind"] == "bad_bug":
            marks = [i for i, ln in enumerate(lines) if BAD_BUG_MARK.search(ln)]
            if marks and marks[0] <= 4:   # a new organism chapter starts at the top of this page
                location = bad_bug_title(lines, marks[0])
        for line in lines:
            if source["kind"] == "food_code":
                match = FOOD_CODE_SECTION.match(line)
                if match and len(line) < 120:
                    location = "§" + match.group(1)
            units.append((location, page, line))
    return units


# ---------- 4. Chunk ----------

def chunk_id(doc, location, text):
    """A fingerprint of the chunk, so we can tell later whether it already has a vector."""
    return hashlib.sha1(f"{doc}|{location}|{text}".encode()).hexdigest()[:12]


def make_chunks(source, units, max_words, respect_sections):
    """Group lines into chunks of at most max_words. If respect_sections, never mix two locations."""
    chunks, buffer = [], []

    def flush():
        if not buffer:
            return
        text = " ".join(line for _, _, line in buffer)
        location, page = buffer[0][0], buffer[0][1]
        chunks.append({"id": chunk_id(source["doc"], location, text), "doc": source["doc"],
                       "location": location, "page": page, "text": text, "words": len(text.split())})
        buffer.clear()

    count = 0
    for unit in units:
        n = len(unit[2].split())
        if buffer and (count + n > max_words or (respect_sections and unit[0] != buffer[0][0])):
            flush()
            count = 0
        buffer.append(unit)
        count += n
    flush()
    return chunks


def merge_tiny(chunks, min_words=MIN_WORDS):
    """Merge a very small chunk into the previous one if both belong to the same location."""
    merged = []
    for chunk in chunks:
        if merged and chunk["words"] < min_words and merged[-1]["location"] == chunk["location"]:
            previous = merged[-1]
            previous["text"] += " " + chunk["text"]
            previous["words"] = len(previous["text"].split())
            previous["id"] = chunk_id(previous["doc"], previous["location"], previous["text"])
        else:
            merged.append(chunk)
    return merged


def chunk_file(source, max_words=150, respect_sections=False):
    """The whole path from PDF to chunks (without embeddings)."""
    cleaned = clean_pages(extract_pages(source))
    chunks = make_chunks(source, label_lines(source, cleaned), max_words, respect_sections)
    return merge_tiny(chunks) if respect_sections else chunks


# ---------- 5. Embed and store ----------

_client = None
EMBEDDED_THIS_RUN = 0     # how many texts we sent to Gemini in this run (each one counts against the daily limit)
BATCHING_WORKS = True     # set to False if Gemini merges a batch into a single vector


def _embed_call(contents, retries=4):
    """One request to Gemini. Waits and retries if Google says 'too many requests'."""
    global _client, EMBEDDED_THIS_RUN
    if _client is None:
        _client = genai.Client(api_key=load_api_key())
    for attempt in range(retries):
        try:
            result = _client.models.embed_content(model=EMBED_MODEL, contents=contents)
            EMBEDDED_THIS_RUN += len(contents)
            return [e.values for e in result.embeddings]
        except Exception as error:  # noqa: BLE001
            limited = "429" in str(error) or "RESOURCE_EXHAUSTED" in str(error)
            if limited and attempt < retries - 1:
                wait = 20 * (attempt + 1)
                print(f"  Google says slow down; waiting {wait}s and retrying...")
                time.sleep(wait)
                continue
            raise


def embed_texts(texts):
    """One vector per text. Each text is wrapped as its own piece of content, so Gemini does not merge them."""
    global BATCHING_WORKS
    contents = [types.Content(parts=[types.Part(text=t)]) for t in texts]
    if BATCHING_WORKS:
        vectors = _embed_call(contents)
        if len(vectors) == len(texts):
            return vectors
        BATCHING_WORKS = False
        print(f"  Got {len(vectors)} vectors for {len(texts)} texts; switching to one text per request.")
    return [_embed_call([c])[0] for c in contents]


def get_collection(design):
    """The ChromaDB collection for one chunking design ('A' -> design_a)."""
    db = chromadb.PersistentClient(path=str(INDEX_DIR))
    return db.get_or_create_collection(name=f"design_{design.lower()}", metadata={"hnsw:space": "cosine"})


def stored_ids(collection, ids):
    """Which of these chunk ids already have a saved vector?"""
    found = set()
    for i in range(0, len(ids), 500):
        found.update(collection.get(ids=ids[i:i + 500])["ids"])
    return found


def embed_and_store(chunks, collection, batch_size=20):
    """Embed only the chunks without a saved vector, saving after every batch. Returns how many were new."""
    unique = list({c["id"]: c for c in chunks}.values())
    have = stored_ids(collection, [c["id"] for c in unique])
    new = [c for c in unique if c["id"] not in have]
    for start in range(0, len(new), batch_size):
        batch = new[start:start + batch_size]
        vectors = embed_texts([c["text"] for c in batch])
        collection.add(
            ids=[c["id"] for c in batch],
            embeddings=vectors,
            documents=[c["text"] for c in batch],
            metadatas=[{"doc": c["doc"], "location": c["location"], "page": c["page"], "words": c["words"]} for c in batch],
        )
        print(f"  saved {min(start + batch_size, len(new))}/{len(new)} new chunks")
    return len(new)


def build_design(name):
    """Chunk every source with one design and make sure all its chunks have a saved vector."""
    chunks = []
    for source in SOURCES:
        chunks += chunk_file(source, **DESIGNS[name])
    collection = get_collection(name)
    print(f"Design {name}: {len(chunks)} chunks, {collection.count()} already have a vector")
    embed_and_store(chunks, collection)


if __name__ == "__main__":
    # `uv run python index.py A` builds only design A; with no letters it builds every design.
    wanted = [a.upper() for a in sys.argv[1:]] or list(DESIGNS)
    try:
        for name in wanted:
            build_design(name)
    except Exception as error:  # noqa: BLE001
        print("\nStopped early:", error)
        print("Everything embedded so far is saved. Run the same command again later to continue.")
    print("\nEmbeddings sent to Gemini in this run:", EMBEDDED_THIS_RUN)
    for name in DESIGNS:
        print(f"Design {name}: {get_collection(name).count()} chunks stored")