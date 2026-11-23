"""Assignment 3: build the index (`main.py index`)."""

import bisect
import re
import sys
import threading
import time
from pathlib import Path

import chromadb
from google import genai
from google.genai import types
from pypdf import PdfReader

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"
VARIANT_MARK = "1. NAME OF THE MEDICINAL PRODUCT"


def smpc_page_count(reader: PdfReader) -> int:
    """How many pages belong to the SmPC (Annex I): those before the first administrative annex."""
    for item in reader.outline:
        if isinstance(item, list):
            continue
        if "MANUFACTURER" in item.title.upper():
            return reader.get_destination_page_number(item)
    return len(reader.pages)


def clean(text: str) -> str:
    """Fix the extraction problems: page number glued to the text, hard line breaks, split words."""
    text = re.sub(r"^\s*\d+\s*\n", "", text)                   # page number at the start
    text = re.sub(r"-\n\s*", "-", text)                        # 'non-\nfatal' -> 'non-fatal'
    text = re.sub(r"[ \t]*\n[ \t]*\n[ \t\n]*", "\n\n", text)   # blank line = paragraph break
    text = re.sub(r"[ \t]*\n[ \t]*", " ", text)                # single line break -> space
    text = re.sub(r"[ \t]{2,}", " ", text)
    return text.strip()


def extract_pages(path) -> list[tuple[int, int, str]]:
    """(page number, SmPC variant number, clean text) for each page of the SmPC.

    One EMA file bundles several SmPCs (one per presentation). Each starts at
    '1. NAME OF THE MEDICINAL PRODUCT'; the variant number goes into the citation.
    """
    reader = PdfReader(path)
    raw = [reader.pages[i].extract_text() or "" for i in range(smpc_page_count(reader))]
    starts = [i for i, t in enumerate(raw) if VARIANT_MARK in t]
    pages = []
    for i, t in enumerate(raw):
        text = clean(t)
        if text:
            pages.append((i + 1, max(1, bisect.bisect_right(starts, i)), text))
    return pages

EMBED_MODEL = "gemini-embedding-2"
BATCH_SIZE = 40
BATCH_PAUSE = 30 
CHUNK_WORDS, OVERLAP_WORDS = 400, 50


def chunk_fixed(path) -> list[dict]:
    """Design A: windows of ~400 words (50 overlap). Location = SmPC variant + page range."""
    source = Path(path).stem
    pages = extract_pages(path)
    total = max(v for _, v, _ in pages)
    words = []  # (word, page, variant)
    for page, variant, text in pages:
        words.extend((w, page, variant) for w in text.split())
    chunks = []
    step = CHUNK_WORDS - OVERLAP_WORDS
    for n, start in enumerate(range(0, len(words), step)):
        window = words[start:start + CHUNK_WORDS]
        if n > 0 and len(window) <= OVERLAP_WORDS:  # tail already covered by the previous chunk
            break
        (_, p1, v1), (_, p2, v2) = window[0], window[-1]
        pages_txt = f"p. {p1}" if p1 == p2 else f"pp. {p1}-{p2}"
        version = f"SmPC {v1}" if v1 == v2 else f"SmPC {v1}-{v2}"
        chunks.append({
            "id": f"fixed400:{source}:{n:04d}",
            "text": " ".join(w for w, _, _ in window),
            "source": source,
            "location": f"{version} of {total}, {pages_txt}",
        })
    return chunks


SECTION_TITLES = {
    "4.1": "Therapeutic", "4.2": "Posology", "4.3": "Contraindications", "4.4": "Special",
    "4.5": "Interaction", "4.6": "Fertility,", "4.7": "Effects", "4.8": "Undesirable",
    "4.9": "Overdose", "5.1": "Pharmacodynamic", "5.2": "Pharmacokinetic", "5.3": "Preclinical",
    "6.1": "List", "6.2": "Incompatibilities", "6.3": "Shelf", "6.4": "Special",
    "6.5": "Nature", "6.6": "Special",
}


def chunk_by_section(path) -> list[dict]:
    """Design B: SmPC variant 1 only; one chunk per section (4.1, 4.2...), long sections cut at 400 words."""
    source = Path(path).stem
    pages = extract_pages(path)
    total = max(v for _, v, _ in pages)
    words = []  # (word, page)
    for page, variant, text in pages:
        if variant == 1:
            words.extend((w, page) for w in text.split())
    order = list(SECTION_TITLES)
    heads, last = [], -1  # (word index, section number); headings must appear in order
    for i in range(len(words) - 1):
        w = words[i][0]
        if w in SECTION_TITLES and words[i + 1][0] == SECTION_TITLES[w] and order.index(w) > last:
            heads.append((i, w))
            last = order.index(w)
    if len(heads) < 10:
        print(f"WARNING: only {len(heads)} section headings found in {source}", file=sys.stderr)
    bounds = [0] + [i for i, _ in heads] + [len(words)]
    labels = ["1-3"] + [n for _, n in heads]
    chunks, n = [], 0
    step = CHUNK_WORDS - OVERLAP_WORDS
    for label, a, b in zip(labels, bounds, bounds[1:]):
        seg = words[a:b]
        for start in range(0, len(seg), step):
            window = seg[start:start + CHUNK_WORDS]
            if start > 0 and len(window) <= OVERLAP_WORDS:
                break
            if len(window) < 15:
                continue
            p1, p2 = window[0][1], window[-1][1]
            pages_txt = f"p. {p1}" if p1 == p2 else f"pp. {p1}-{p2}"
            chunks.append({
                "id": f"section:{source}:{n:04d}",
                "text": f"[Section {label}] " + " ".join(w for w, _ in window),
                "source": source,
                "location": f"SmPC 1 of {total}, {pages_txt} (section {label})",
            })
            n += 1
    return chunks


DESIGNS = {"fixed400": chunk_fixed, "section": chunk_by_section}



def chunk_file(path, design: str = "fixed400") -> list[dict]:
    """One file -> chunks with id, text, source and location. server.py's add_document uses this."""
    return DESIGNS[design](path)


_client = None
_client_lock = threading.Lock()


def get_collection(name: str):
    global _client
    with _client_lock:  # one shared client: Chroma breaks if threads open it at the same time
        if _client is None:
            _client = chromadb.PersistentClient(path=str(INDEX_DIR))
        return _client.get_or_create_collection(
            name, metadata={"hnsw:space": "cosine"}, embedding_function=None
        )

def embed_texts(client, texts: list[str]) -> list[list[float]]:
    # One Content per text: a plain list of strings is merged into a single vector.
    contents = [types.Content(parts=[types.Part(text=t)]) for t in texts]
    for attempt in range(3):
        try:
            result = client.models.embed_content(model=EMBED_MODEL, contents=contents)
            break
        except Exception as error:  # noqa: BLE001
            print(f"embedding failed ({error}); attempt {attempt + 1}/3", file=sys.stderr)
            time.sleep(60 if "429" in str(error) else 10 * (attempt + 1))
    else:
        raise RuntimeError("Embedding failed 3 times (daily limit?). Vectors already saved are kept; run again later.")
    vectors = [e.values for e in result.embeddings]
    if len(vectors) != len(texts):  # stop at once instead of retrying and wasting quota
        raise RuntimeError(f"Got {len(vectors)} vectors for {len(texts)} texts.")
    return vectors


def embed_and_store(chunks: list[dict], design: str = "fixed400", limit: int | None = None) -> int:
    """Embed only the chunks without a saved vector, saving each batch as soon as it arrives."""
    collection = get_collection(design)
    have = set(collection.get(ids=[c["id"] for c in chunks])["ids"])
    existing = [c for c in chunks if c["id"] in have]
    if existing:  # refresh the citations of vectors already saved; no embedding needed
        collection.update(
            ids=[c["id"] for c in existing],
            metadatas=[{"source": c["source"], "location": c["location"]} for c in existing],
        )
    todo = [c for c in chunks if c["id"] not in have]
    if limit is not None:
        todo = todo[:limit]
    client = genai.Client(api_key=load_api_key())
    for i in range(0, len(todo), BATCH_SIZE):
        batch = todo[i:i + BATCH_SIZE]
        vectors = embed_texts(client, [c["text"] for c in batch])
        collection.add(
            ids=[c["id"] for c in batch],
            embeddings=vectors,
            documents=[c["text"] for c in batch],
            metadatas=[{"source": c["source"], "location": c["location"]} for c in batch],
        )
        print(f"{design}: stored {i + len(batch)}/{len(todo)}", file=sys.stderr)
        if i + BATCH_SIZE < len(todo):
            time.sleep(BATCH_PAUSE)
    return len(todo)


def main() -> None:
    for design in DESIGNS:
        chunks = []
        for path in sorted(CORPUS_DIR.glob("*.pdf")):
            chunks.extend(chunk_file(path, design))
        new = embed_and_store(chunks, design)
        print(f"{design}: {len(chunks)} chunks, {new} newly embedded")


if __name__ == "__main__":
    main()