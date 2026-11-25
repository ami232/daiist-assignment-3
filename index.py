"""
Assignment 3: build the index (`main.py index`).

Corpus: EMA product information (EPAR) for three blood thinners (DOACs).
Each PDF holds, for every strength, a Summary of Product Characteristics
(SmPC, Annex I), Annex II, the box labelling (Annex IIIA) and a package
leaflet (Annex IIIB). Pipeline, per file:

    extract_pages -> parse_sections -> deduplicate -> chunk -> embed_and_store

server.py's add_document tool imports `index_file(path)` from here.

    uv run python index.py              # download, chunk, embed what is missing
    uv run python index.py --dry-run    # chunk and print stats, no embeddings
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

import httpx
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"
CHROMA_DIR = INDEX_DIR / "chroma"
CONFIG_FILE = INDEX_DIR / "config.json"
QUERY_CACHE_FILE = INDEX_DIR / "query_cache.json"

EMA = "https://www.ema.europa.eu/en/documents/product-information/{}-epar-product-information_en.pdf"
CORPUS = {  # source id -> (brand, active substance, URL)
    "eliquis": ("Eliquis", "apixaban", EMA.format("eliquis")),
    "xarelto": ("Xarelto", "rivaroxaban", EMA.format("xarelto")),
    "pradaxa": ("Pradaxa", "dabigatran etexilate", EMA.format("pradaxa")),
}
# Downloaded but NOT indexed: added later through the add_document tool.
HELD_OUT = {"lixiana": ("Lixiana", "edoxaban", EMA.format("lixiana"))}

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768          # Gemini Embedding 2 normalises truncated vectors itself
EMBED_BATCH = 20         # texts per request; each text counts toward the daily quota

# Retrieval designs compared in evaluate.py. Both use the same cleaned text.
DESIGNS = {
    "fixed": "300-word windows (50 overlap) over each document part, ignoring section boundaries",
    "section": "one chunk per SmPC/leaflet section, split at <=250 words, heading prepended",
}
DEFAULT_DESIGN = "section"


# ---------------------------------------------------------------- download


def download_corpus(sources: dict = CORPUS | HELD_OUT) -> None:
    """Download each PDF into corpus/ once. EMA answers bursts with HTTP 429."""
    CORPUS_DIR.mkdir(exist_ok=True)
    for source, (_, _, url) in sources.items():
        path = CORPUS_DIR / f"{source}.pdf"
        if path.exists() and path.read_bytes()[:5] == b"%PDF-":
            continue
        for wait in (0, 15, 45, 90):
            time.sleep(wait)
            response = httpx.get(url, follow_redirects=True, timeout=120,
                                 headers={"User-Agent": "Mozilla/5.0 (course assignment)"})
            if response.status_code == 200 and response.content[:5] == b"%PDF-":
                path.write_bytes(response.content)
                log(f"downloaded {path.name} ({len(response.content) / 1e6:.1f} MB)")
                break
            log(f"{source}: HTTP {response.status_code}, retrying")
        else:
            raise SystemExit(f"Could not download {url}. Try again in a few minutes.")
        time.sleep(5)


# ---------------------------------------------------------------- extract and clean


def extract_pages(path: Path) -> list[tuple[int, list[str]]]:
    """Return (page number, lines) per page, without the page-number header."""
    pages = []
    for number, page in enumerate(PdfReader(path).pages, start=1):
        lines = [line.rstrip() for line in (page.extract_text() or "").splitlines()]
        if lines and lines[0].strip() == str(number):  # EMA prints the page number first
            lines = lines[1:]
        pages.append((number, lines))
    return pages


def join_lines(lines: list[str]) -> str:
    """Join wrapped PDF lines into one paragraph, mending words split at a hyphen."""
    text = ""
    for line in (l.strip() for l in lines):
        if not line:
            continue
        if text.endswith("-") and line[:1].islower():
            text += line
        else:
            text += (" " if text else "") + line
    return re.sub(r"\s+", " ", text).strip()


# ---------------------------------------------------------------- parse structure

SMPC_START = re.compile(r"^1\.\s+NAME OF THE MEDICINAL PRODUCT\s*$")
SMPC_TOP = re.compile(r"^(\d{1,2})\.\s+([A-Z][A-Z0-9 ,()/'’\-]{3,})$")
SMPC_SUB = re.compile(r"^(\d{1,2})\.(\d{1,2})\s+([A-Z][^.]{2,120})$")
LEAFLET_START = re.compile(r"^Package leaflet: Information for the (user|patient)", re.I)
LEAFLET_HEAD = re.compile(r"^([1-6])\.\s+(What|How|Possible|Contents)\b.*$")
SKIP_START = re.compile(r"^(ANNEX II|ANNEX III|A\. LABELLING)\s*$")
# Leaflet section 6 ends with pages of country-by-country company contacts.
LEAFLET_CONTACTS = re.compile(r"^For any information about this medicine, please contact", re.I)

# SmPC sections a caregiver's questions can touch. Dropped: 5.x (clinical
# trial and pharmacology data, ~44k words) and 7-10 (marketing authorisation).
SMPC_KEEP = re.compile(r"^(1\.|2\.|3\.|4\.\d|6\.[3-6] )")


@dataclass
class Paragraph:
    text: str
    page: int


@dataclass
class Section:
    source: str
    doc_part: str          # "smpc" or "leaflet"
    product: str           # e.g. "Eliquis 5 mg film-coated tablets"
    heading: str           # e.g. "4.5 Interaction with other medicinal products ..."
    paragraphs: list[Paragraph] = field(default_factory=list)

    @property
    def words(self) -> int:
        return sum(len(p.text.split()) for p in self.paragraphs)


def parse_sections(source: str, pages: list[tuple[int, list[str]]]) -> list[Section]:
    """Walk the PDF line by line and cut it into SmPC and leaflet sections.

    Skipped: Annex II and the box labelling (batch-release addresses, carton
    text), the leaflet's list of national company contacts, and SmPC
    sections outside SMPC_KEEP. None of it answers a caregiver's question.
    """
    sections: list[Section] = []
    part = None            # None (skipping), "smpc" or "leaflet"
    product = ""
    want_product = False   # the line after a document start is the product name
    top_num = 0            # current SmPC section number / leaflet section number
    in_toc = False         # leaflet "What is in this leaflet" list
    buffer: list[str] = []
    buffer_page = 0

    def flush() -> None:
        nonlocal buffer
        text = join_lines(buffer)
        buffer = []
        if text and part and sections:
            sections[-1].paragraphs.append(Paragraph(text, buffer_page))

    def start(heading: str) -> None:
        flush()
        sections.append(Section(source, part, product, heading))

    for page_no, lines in pages:
        for raw in lines:
            line = raw.strip()
            if SMPC_START.match(line) and part != "skip-to-leaflet":
                flush()
                part, top_num, want_product = "smpc", 1, True
                sections.append(Section(source, part, "", "1. Name of the medicinal product"))
                continue
            if LEAFLET_START.match(line):
                flush()
                part, top_num, want_product, in_toc = "leaflet", 0, True, False
                sections.append(Section(source, part, "", "Introduction"))
                continue
            if SKIP_START.match(line):
                flush()
                part = "skip-to-leaflet" if "III" in line or "LABELLING" in line else None
                continue
            if part == "leaflet" and LEAFLET_CONTACTS.match(line):
                flush()
                part = "skip-to-leaflet"
                continue
            if part in (None, "skip-to-leaflet"):
                continue
            if want_product and line:
                product = line
                sections[-1].product = product
                want_product = False
                continue

            if part == "smpc":
                top, sub = SMPC_TOP.match(line), SMPC_SUB.match(line)
                if top and int(top.group(1)) in (top_num, top_num + 1):
                    top_num = int(top.group(1))
                    start(f"{top_num}. {top.group(2).strip().capitalize()}")
                    continue
                if sub and int(sub.group(1)) == top_num:
                    start(f"{sub.group(1)}.{sub.group(2)} {sub.group(3).strip()}")
                    continue
            else:
                if line.lower().startswith("what is in this leaflet"):
                    flush()
                    in_toc = True
                    continue
                head = LEAFLET_HEAD.match(line)
                if head:
                    if in_toc:
                        in_toc = head.group(1) != "6"
                        continue
                    top_num = int(head.group(1))
                    start(line)
                    continue
                if in_toc:
                    continue

            if not line:
                flush()
            else:
                if not buffer:
                    buffer_page = page_no
                buffer.append(line)
        flush()  # a paragraph never spans pages, so the page number stays exact
    for s in sections:
        s.product = s.product or source.capitalize()
    return [s for s in sections if s.paragraphs
            and (s.doc_part == "leaflet" or SMPC_KEEP.match(s.heading))]


def deduplicate(sections: list[Section]) -> tuple[list[Section], int]:
    """Drop paragraphs repeated word for word elsewhere in the same document part.

    The PDF repeats the SmPC and leaflet for every strength (2.5 mg, 5 mg,
    15 mg...). Removing exact repeats keeps every sentence that differs, e.g.
    strength-specific doses, while cutting the corpus to a fraction.
    """
    seen: set[tuple[str, str, str]] = set()
    removed = 0
    kept = []
    for section in sections:
        paragraphs = []
        for p in section.paragraphs:
            key = (section.source, section.doc_part, re.sub(r"\W+", " ", p.text.lower()).strip())
            if key in seen:
                removed += len(p.text.split())
                continue
            seen.add(key)
            paragraphs.append(p)
        if paragraphs:
            kept.append(Section(section.source, section.doc_part, section.product,
                                section.heading, paragraphs))
    return kept, removed


# ---------------------------------------------------------------- chunk


def chunk_sections(sections: list[Section], design: str, file_hash: str = "") -> list[dict]:
    """Turn sections into chunks: {"id", "text", "embed_text", "metadata"}."""
    chunks = []

    def add(section: Section, text: str, page: int, title: str) -> None:
        meta = {
            "source": section.source,
            "doc_part": section.doc_part,
            "product": section.product,
            "section": section.heading,
            "page": page,
            "design": design,
            "file_hash": file_hash,
            "words": len(text.split()),
        }
        meta["citation"] = cite(meta)
        uid = hashlib.sha1(f"{design}|{section.source}|{meta['citation']}|{text}".encode()).hexdigest()[:20]
        chunks.append({"id": uid, "text": text, "metadata": meta,
                       "embed_text": f"title: {title} | text: {text}"})

    if design == "fixed":
        size, overlap = 300, 50
        groups: dict[tuple[str, str], list[tuple[Section, Paragraph]]] = {}
        for s in sections:
            groups.setdefault((s.source, s.doc_part), []).extend((s, p) for p in s.paragraphs)
        for (source, _), items in groups.items():
            words = [(w, s, p.page) for s, p in items for w in p.text.split()]
            for begin in range(0, len(words), size - overlap):
                window = words[begin:begin + size]
                if len(window) < 30 and begin > 0:
                    break
                _, s, page = window[0]
                add(s, " ".join(w for w, _, _ in window), page, s.source.capitalize())
        return chunks

    if design == "section":
        limit = 250
        for s in sections:
            title = f"{s.product} - {'package leaflet' if s.doc_part == 'leaflet' else 'SmPC'} - {s.heading}"
            piece: list[str] = []
            page = s.paragraphs[0].page
            for p in s.paragraphs:
                words = p.text.split()
                while words:
                    room = limit - len(piece)
                    if room <= 0 or (piece and len(words) > room and len(words) <= limit):
                        add(s, " ".join(piece), page, title)
                        piece, page = [], p.page
                        continue
                    if not piece:
                        page = p.page
                    piece.extend(words[:room])
                    words = words[room:]
            if piece:
                add(s, " ".join(piece), page, title)
        return chunks

    raise ValueError(f"Unknown design {design!r}; choose from {list(DESIGNS)}")


def cite(meta: dict) -> str:
    """Human-readable location, used as the citation the agent must quote."""
    part = "Package leaflet" if meta["doc_part"] == "leaflet" else "SmPC"
    return f"[{meta['source']} | {part} | {meta['product']} | {meta['section']} | p. {meta['page']}]"


def chunk_file(path: Path, design: str) -> tuple[list[dict], dict]:
    """Full text pipeline for one PDF. Returns chunks and statistics."""
    path = Path(path)
    source = re.sub(r"[^a-z0-9_-]", "", path.stem.lower())
    file_hash = hashlib.sha256(path.read_bytes()).hexdigest()
    pages = extract_pages(path)
    raw_words = sum(len(" ".join(lines).split()) for _, lines in pages)
    sections = parse_sections(source, pages)
    parsed_words = sum(s.words for s in sections)
    sections, removed = deduplicate(sections)
    chunks = chunk_sections(sections, design, file_hash)
    stats = {"source": source, "pages": len(pages), "raw_words": raw_words,
             "parsed_words": parsed_words, "duplicate_words_removed": removed,
             "kept_words": sum(s.words for s in sections), "sections": len(sections),
             "chunks": len(chunks), "file_hash": file_hash}
    return chunks, stats


# ---------------------------------------------------------------- embed and store


class QuotaExhausted(RuntimeError):
    """The free tier's daily embedding quota is used up."""


_client = None


def gemini():
    global _client
    if _client is None:
        from google import genai
        from api_key import load_api_key
        _client = genai.Client(api_key=load_api_key())
    return _client


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed each text separately (one Content per text, not one merged vector)."""
    from google.genai import types
    contents = [types.Content(parts=[types.Part(text=t)]) for t in texts]
    for attempt in range(6):
        try:
            result = gemini().models.embed_content(
                model=EMBED_MODEL, contents=contents,
                config=types.EmbedContentConfig(output_dimensionality=EMBED_DIM))
            vectors = [e.values for e in result.embeddings]
            if len(vectors) != len(texts):
                raise RuntimeError(f"asked for {len(texts)} embeddings, got {len(vectors)}")
            return vectors
        except Exception as error:  # the SDK raises ClientError for 429s
            message = str(error)
            if "429" not in message and "RESOURCE_EXHAUSTED" not in message:
                raise
            if "PerDay" in message or "per day" in message.lower() or attempt == 5:
                raise QuotaExhausted(message) from error
            wait = 20 * (attempt + 1)
            log(f"rate limited, waiting {wait}s")
            time.sleep(wait)
    raise QuotaExhausted("rate limited")


def embed_query(query: str) -> list[float]:
    """Embed a search query, cached on disk so evaluation reruns cost nothing."""
    cache = json.loads(QUERY_CACHE_FILE.read_text()) if QUERY_CACHE_FILE.exists() else {}
    key = f"{EMBED_MODEL}|{EMBED_DIM}|{query}"
    if key not in cache:
        cache[key] = embed_texts([f"task: search result | query: {query}"])[0]
        QUERY_CACHE_FILE.write_text(json.dumps(cache))
    return cache[key]


def collection(design: str = None):
    """The ChromaDB collection for a design (default: the one chosen in config)."""
    import chromadb
    design = design or active_design()
    client = chromadb.PersistentClient(path=str(CHROMA_DIR),
                                       settings=chromadb.Settings(anonymized_telemetry=False))
    return client.get_or_create_collection(f"chunks_{design}", metadata={"hnsw:space": "cosine"})


def config() -> dict:
    """index/config.json: the design and search method chosen by evaluate.py."""
    return json.loads(CONFIG_FILE.read_text()) if CONFIG_FILE.exists() else {}


def active_design() -> str:
    return config().get("active_design", DEFAULT_DESIGN)


def active_method() -> str:
    return config().get("method", "dense")


def embed_and_store(chunks: list[dict], design: str) -> int:
    """Embed only chunks without a saved vector; save each batch as it arrives.

    Returns how many chunks were embedded. Raises QuotaExhausted after saving
    everything embedded so far, so a rerun tomorrow carries on from there.
    """
    col = collection(design)
    ids = [c["id"] for c in chunks]
    existing = set(col.get(ids=ids, include=[])["ids"]) if ids else set()
    todo = [c for c in chunks if c["id"] not in existing]
    for i in range(0, len(todo), EMBED_BATCH):
        batch = todo[i:i + EMBED_BATCH]
        vectors = embed_texts([c["embed_text"] for c in batch])
        col.upsert(ids=[c["id"] for c in batch], embeddings=vectors,
                   documents=[c["text"] for c in batch],
                   metadatas=[c["metadata"] for c in batch])
        log(f"  {design}: embedded {min(i + EMBED_BATCH, len(todo))}/{len(todo)}")
    return len(todo)


def remove_stale(source: str, keep_ids: set[str], design: str) -> int:
    """Delete chunks of `source` that the current chunking no longer produces."""
    col = collection(design)
    old = set(col.get(where={"source": source}, include=[])["ids"])
    stale = list(old - keep_ids)
    if stale:
        col.delete(ids=stale)
    return len(stale)


def index_file(path: Path, design: str = None) -> dict:
    """Chunk, embed and store one PDF in one design's collection (used by add_document)."""
    design = design or active_design()
    chunks, stats = chunk_file(path, design)
    stats["embedded"] = embed_and_store(chunks, design)
    stats["stale_removed"] = remove_stale(stats["source"], {c["id"] for c in chunks}, design)
    return stats


def log(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


# ---------------------------------------------------------------- main


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[1])
    parser.add_argument("--dry-run", action="store_true", help="chunk and report; no embeddings")
    parser.add_argument("--design", choices=list(DESIGNS), action="append",
                        help="design(s) to build (default: all)")
    args = parser.parse_args()
    designs = args.design or list(DESIGNS)

    download_corpus()
    INDEX_DIR.mkdir(exist_ok=True)
    if not CONFIG_FILE.exists():
        CONFIG_FILE.write_text(json.dumps({"active_design": DEFAULT_DESIGN,
                                           "embedding_model": EMBED_MODEL,
                                           "dimensions": EMBED_DIM}, indent=2))

    report = {}
    try:
        for design in designs:
            for source in CORPUS:
                path = CORPUS_DIR / f"{source}.pdf"
                if args.dry_run:
                    _, stats = chunk_file(path, design)
                else:
                    stats = index_file(path, design)
                report.setdefault(design, []).append(stats)
                print(f"{design:8} {source:8} {stats['pages']:4} pages  "
                      f"{stats['raw_words']:7,} raw words  {stats['kept_words']:6,} kept  "
                      f"{stats['chunks']:4} chunks"
                      + ("" if args.dry_run else f"  {stats['embedded']} newly embedded"))
    except QuotaExhausted:
        print("\nDaily embedding quota reached. Everything embedded so far is saved in "
              "index/; run `uv run python main.py index` again after 09:00 (Spain).")
        sys.exit(2)

    for design, rows in report.items():
        words = sum(r["kept_words"] for r in rows)
        print(f"{design}: {sum(r['chunks'] for r in rows)} chunks, {words:,} words "
              f"(from {sum(r['raw_words'] for r in rows):,} raw)")
    if not args.dry_run:
        (INDEX_DIR / "stats.json").write_text(json.dumps(report, indent=2))


if __name__ == "__main__":
    main()
