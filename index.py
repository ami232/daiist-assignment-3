"""
Assignment 3: build the index (`main.py index`).

Corpus (public health, vaccination guidance for clinicians):
  - seven chapters of the CDC "Pink Book" (CDC content is public domain),
  - two ECDC measles documents (ECDC content is CC BY 4.0 unless stated).
One more Pink Book chapter is downloaded but NOT indexed: it is the document
you add later with the add_document tool.

Pipeline: download -> extract blocks (text + location) -> chunk (two designs)
-> embed with Gemini -> store in index/ (ChromaDB). Every vector is saved as
soon as it is returned, and only chunks without a saved vector are embedded,
so a crash or the daily free-tier limit loses nothing: run it again later.

    uv run python main.py index                      # download, chunk, embed
    uv run python index.py --no-embed                # dry run: no quota used
    INDEX_DESIGNS=structure uv run python main.py index   # one design only

server.py imports chunk_file, embed_and_store, index_file and search_chunks
from this file. Everything a library function reports goes to stderr, because
stdout carries the MCP protocol when the server runs.
"""

import hashlib
import json
import os
import re
import sys
import time
from collections import Counter
from dataclasses import dataclass
from datetime import date
from pathlib import Path

import chromadb
import httpx
from bs4 import BeautifulSoup
from chromadb.config import Settings
from google import genai
from pypdf import PdfReader

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"  # git-ignored
HOLDBACK_DIR = CORPUS_DIR / "holdback"
INDEX_DIR = ROOT / "index"  # committed
CHROMA_DIR = INDEX_DIR / "chroma"
MANIFEST = INDEX_DIR / "manifest.json"

EMBED_MODEL = "gemini-embedding-2"
EMBED_BATCH = 16  # texts per API call (each text counts against the daily limit)
MIN_WORDS_TOTAL = 50_000

# ---------------------------------------------------------------------------
# Decisions that are yours. Change them, then re-run the retrieval comparison.
# ---------------------------------------------------------------------------
DESIGNS = ("structure", "fixed")
CHOSEN_DESIGN = "structure"  # the design the server and the agent use; set it from your hit rates
FIXED_WORDS, FIXED_STRIDE = 200, 150  # design "fixed": 200-word windows, 50 words of overlap
STRUCT_MAX, STRUCT_MIN = 300, 60  # design "structure": pack paragraphs of a section up to 300 words

# ---------------------------------------------------------------------------
# Corpus
# ---------------------------------------------------------------------------
PINK = "https://www.cdc.gov/pinkbook/hcp/table-of-contents/"
ECDC_DOCS = "https://www.ecdc.europa.eu/sites/default/files/documents/"
CDC_LICENCE = "Public domain (CDC; attribute CDC, no endorsement implied)"
ECDC_LICENCE = "CC BY 4.0 (ECDC; attribute ECDC)"


@dataclass(frozen=True)
class Source:
    name: str  # used as the `source` in chunk metadata and in citations
    url: str
    licence: str


SOURCES = [
    Source("Pink Book ch.2 General Best Practice Guidance", PINK + "chapter-2-general-best-practice-guidance.html", CDC_LICENCE),
    Source("Pink Book ch.4 Vaccine Safety", PINK + "chapter-4-vaccine-safety.html", CDC_LICENCE),
    Source("Pink Book ch.10 Hepatitis B", PINK + "chapter-10-hepatitis-b.html", CDC_LICENCE),
    Source("Pink Book ch.13 Measles", PINK + "chapter-13-measles.html", CDC_LICENCE),
    Source("Pink Book ch.15 Mumps", PINK + "chapter-15-mumps.html", CDC_LICENCE),
    Source("Pink Book ch.16 Pertussis", PINK + "chapter-16-pertussis.html", CDC_LICENCE),
    Source("Pink Book ch.20 Rubella", PINK + "chapter-20-rubella.html", CDC_LICENCE),
    Source("ECDC Measles threat assessment brief (Feb 2024)", ECDC_DOCS + "measles-eu-threat-assessment-brief-february-2024.pdf", ECDC_LICENCE),
    Source(
        "ECDC Measles and rubella elimination: communicating the importance of vaccination (2014)",
        "https://www.ecdc.europa.eu/sites/portal/files/media/en/publications/Publications/Measles-rubella-elimination-communicating-importance-vaccination.pdf",
        ECDC_LICENCE,
    ),
]

# Downloaded to corpus/holdback/ but not indexed: the document for the add_document demo.
HOLDBACK = [Source("Pink Book ch.22 Varicella", PINK + "chapter-22-varicella.html", CDC_LICENCE)]

HEADERS = {
    "User-Agent": "Mozilla/5.0 (compatible; university-assignment-3; educational use)",
    "Accept": "text/html,application/pdf;q=0.9,*/*;q=0.5",
}


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


# ---------------------------------------------------------------------------
# Download
# ---------------------------------------------------------------------------
def download(source: Source, folder: Path = CORPUS_DIR) -> Path:
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / source.url.rsplit("/", 1)[-1]
    if path.is_file() and path.stat().st_size > 1000:
        return path
    log(f"downloading {source.url}")
    try:
        response = httpx.get(source.url, headers=HEADERS, follow_redirects=True, timeout=60)
        response.raise_for_status()
    except httpx.HTTPError as error:
        raise SystemExit(
            f"Could not download {source.url}\n  {error}\n"
            f"  Open it in your browser and save it as:\n  {path}\n"
            f"  (a web page: Save as > 'Webpage, HTML only'; a PDF: download it), then run again."
        ) from error
    path.write_bytes(response.content)
    return path


# ---------------------------------------------------------------------------
# Extraction: a file becomes a list of Blocks (location + text)
# ---------------------------------------------------------------------------
@dataclass
class Block:
    location: str
    text: str


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\xa0", " ")).strip()


JUNK_HEADING = re.compile(r"^(on this page|related (pages|links)|contact us|share|print)\b", re.I)
JUNK_LINE = re.compile(r"^(page last reviewed|content source|source:|cdc twitter|print|share|email|feedback)\b", re.I)
REFERENCES = re.compile(r"^((selected )?references?\b|acknowledg)", re.I)  # citations and thank-yous, not guidance
REFERENCE_ENTRY = re.compile(r"^\(?\d{1,3}[).]\s+[A-Z]")  # "(14) Markowitz LE, ..." or "3. World Health ..."


def extract_html(path: Path) -> list[Block]:
    soup = BeautifulSoup(path.read_text(encoding="utf-8", errors="ignore"), "html.parser")
    root = soup.find("main") or soup.find("article") or soup.body or soup
    for tag in root(["script", "style", "nav", "footer", "header", "aside", "form", "noscript", "svg", "button", "iframe"]):
        tag.decompose()
    headings: list[str] = []
    blocks: list[Block] = []
    for el in root.find_all(["h2", "h3", "h4", "p", "li", "tr"]):
        if el.name[0] == "h":
            text = clean(el.get_text(" "))
            if not text or JUNK_HEADING.match(text):
                continue
            if REFERENCES.match(text):
                break
            level = int(el.name[1]) - 2
            headings = headings[:level] + [text]
            continue
        if el.find_parent(["li", "tr", "p"]):
            continue  # its parent already contains this text
        if el.name == "tr":
            text = " | ".join(t for t in (clean(c.get_text(" ")) for c in el.find_all(["th", "td"])) if t)
        else:
            text = clean(el.get_text(" "))
        if len(text.split()) < 3 or JUNK_LINE.match(text):
            continue
        blocks.append(Block(" > ".join(headings) or "Introduction", text))
    return blocks


def extract_pdf(path: Path) -> list[Block]:
    pages = [(page.extract_text() or "") for page in PdfReader(str(path)).pages]
    lines_by_page = [[clean(line) for line in text.splitlines() if clean(line)] for text in pages]
    n = len(pages)

    def key(line: str) -> str:  # ignore digits, so a running header with a page number still matches
        return re.sub(r"[^a-z]+", "", line.lower())

    counts = Counter(key(line) for lines in lines_by_page for line in set(lines))
    repeated = {k for k, c in counts.items() if c >= max(3, 0.25 * n) and k}  # running headers and footers
    blocks: list[Block] = []
    for i, lines in enumerate(lines_by_page):
        entries = sum(1 for line in lines if REFERENCE_ENTRY.match(line))
        has_heading = i >= n // 2 and any(line.lower().rstrip(":") in ("references", "reference list") for line in lines)
        if not has_heading and entries >= 3 and entries / len(lines) >= 0.15:
            continue  # a page of numbered references in the middle of the document
        kept: list[str] = []
        stop = False
        for line in lines:
            if (key(line) in repeated and len(line) < 120) or re.fullmatch(r"\d{1,3}", line):
                continue
            if i >= n // 2 and line.lower().rstrip(":") in ("references", "reference list"):
                stop = True
                break
            if re.match(r"^\(?1[).]\s+[A-Z]", line) and kept:
                break  # a numbered reference list starts here; the rest of the page is citations
            kept.append(line)
        text = ""
        for line in kept:  # re-join hard-wrapped lines and hyphenated words
            text = text[:-1] + line if text.endswith("-") and line[:1].islower() else (text + " " + line).strip()
        if len(text.split()) >= 5:
            blocks.append(Block(f"p. {i + 1}", text))
        if stop:
            break
    return blocks


def extract_text(path: Path) -> list[Block]:
    paragraphs = re.split(r"\n\s*\n", path.read_text(encoding="utf-8", errors="ignore"))
    return [Block("text", clean(p)) for p in paragraphs if len(p.split()) >= 3]


def extract_blocks(path: Path) -> list[Block]:
    suffix = Path(path).suffix.lower()
    if suffix == ".pdf":
        return extract_pdf(Path(path))
    if suffix in (".html", ".htm"):
        return extract_html(Path(path))
    if suffix in (".txt", ".md"):
        return extract_text(Path(path))
    raise ValueError(f"Unsupported file type {suffix!r}: use .pdf, .html, .htm, .txt or .md")


# ---------------------------------------------------------------------------
# Chunking: two designs, both carry source and location
# ---------------------------------------------------------------------------
@dataclass
class Chunk:
    id: str
    design: str
    source: str
    location: str
    text: str  # what the model reads and what is cited
    embed_text: str  # what is embedded

    @property
    def words(self) -> int:
        return len(self.text.split())


def make_chunk(design: str, source: str, location: str, text: str, embed_text: str | None = None) -> Chunk:
    digest = hashlib.sha1(f"{design}|{source}|{location}|{text}".encode("utf-8")).hexdigest()[:24]
    return Chunk(digest, design, source, location, text, embed_text or text)


SENTENCE = re.compile(r"(?<=[.!?])\s+(?=[A-Z0-9(\[])")


def split_long(text: str, max_words: int) -> list[str]:
    """Cut a long block into pieces of at most max_words, at sentence ends where possible."""
    if len(text.split()) <= max_words:
        return [text]
    pieces: list[str] = []
    current: list[str] = []
    n = 0
    for sentence in SENTENCE.split(text):
        w = len(sentence.split())
        if w > max_words:
            if current:
                pieces.append(" ".join(current))
                current, n = [], 0
            words = sentence.split()
            pieces += [" ".join(words[i : i + max_words]) for i in range(0, len(words), max_words)]
            continue
        if n + w > max_words and current:
            pieces.append(" ".join(current))
            current, n = [], 0
        current.append(sentence)
        n += w
    if current:
        pieces.append(" ".join(current))
    return pieces


def chunk_fixed(source: str, blocks: list[Block]) -> list[Chunk]:
    """Design 'fixed': sliding windows of FIXED_WORDS words, ignoring structure."""
    words = [(w, b.location) for b in blocks for w in b.text.split()]
    chunks: list[Chunk] = []
    i = 0
    while i < len(words):
        window = words[i : i + FIXED_WORDS]
        chunks.append(make_chunk("fixed", source, window[0][1], " ".join(w for w, _ in window)))
        if i + FIXED_WORDS >= len(words):
            break
        i += FIXED_STRIDE
    return chunks


def chunk_structure(source: str, blocks: list[Block]) -> list[Chunk]:
    """Design 'structure': keep a section's paragraphs together (up to STRUCT_MAX words) and
    put the source and section heading in front of the embedded text."""
    chunks: list[Chunk] = []
    current: list[str] = []
    n = 0
    location = ""

    def flush() -> None:
        nonlocal current, n
        if current:
            text = "\n".join(current)
            chunks.append(make_chunk("structure", source, location, text, f"{source} | {location}\n{text}"))
        current, n = [], 0

    for block in blocks:
        for piece in split_long(block.text, STRUCT_MAX):
            w = len(piece.split())
            if current and (n + w > STRUCT_MAX or (block.location != location and n >= STRUCT_MIN)):
                flush()
            if not current:
                location = block.location
            current.append(piece)
            n += w
    flush()
    return chunks


CHUNKERS = {"structure": chunk_structure, "fixed": chunk_fixed}


def chunk_file(path, source_name: str | None = None, design: str = CHOSEN_DESIGN) -> list[Chunk]:
    """Extract and chunk one file. server.py's add_document uses this."""
    path = Path(path)
    return CHUNKERS[design](source_name or path.stem, extract_blocks(path))


# ---------------------------------------------------------------------------
# Embedding and storage
# ---------------------------------------------------------------------------
class QuotaExhausted(Exception):
    pass


_client = None
_chroma = None


def get_client() -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client(api_key=load_api_key())
    return _client


def embed_texts(texts: list[str]) -> list[list[float]]:
    for attempt in range(6):
        try:
            response = get_client().models.embed_content(model=EMBED_MODEL, contents=texts)
            vectors = [list(e.values) for e in response.embeddings]
            if len(vectors) != len(texts):  # a batch came back as one vector: embed one text at a time
                return [embed_texts([t])[0] for t in texts]
            return vectors
        except Exception as error:  # noqa: BLE001
            message = str(error)
            if "429" in message or "RESOURCE_EXHAUSTED" in message:
                if re.search(r"per ?day|daily", message, re.I):
                    raise QuotaExhausted(message) from error
                wait = 20 * (attempt + 1)
                log(f"rate limited, waiting {wait}s ...")
                time.sleep(wait)
                continue
            raise
    raise QuotaExhausted("still rate limited after several waits")


def get_collection(design: str):
    global _chroma
    if _chroma is None:
        CHROMA_DIR.mkdir(parents=True, exist_ok=True)
        _chroma = chromadb.PersistentClient(path=str(CHROMA_DIR), settings=Settings(anonymized_telemetry=False))
    return _chroma.get_or_create_collection(f"chunks_{design}", metadata={"hnsw:space": "cosine"})


def embed_and_store(chunks: list[Chunk], design: str) -> dict:
    """Embed the chunks that have no saved vector yet and store them. Safe to re-run."""
    collection = get_collection(design)
    unique = {c.id: c for c in chunks}
    ids = list(unique)
    existing: set[str] = set()
    for i in range(0, len(ids), 500):
        existing.update(collection.get(ids=ids[i : i + 500])["ids"])
    todo = [unique[i] for i in ids if i not in existing]
    added, quota_hit = 0, False
    for i in range(0, len(todo), EMBED_BATCH):
        batch = todo[i : i + EMBED_BATCH]
        try:
            vectors = embed_texts([c.embed_text for c in batch])
        except QuotaExhausted as error:
            log(f"Daily embedding limit reached: {str(error)[:200]}")
            quota_hit = True
            break
        collection.add(
            ids=[c.id for c in batch],
            embeddings=vectors,
            documents=[c.text for c in batch],
            metadatas=[{"source": c.source, "location": c.location, "design": c.design, "words": c.words} for c in batch],
        )
        added += len(batch)
        log(f"  [{design}] embedded {added}/{len(todo)}")
        time.sleep(1)
    return {"design": design, "chunks": len(unique), "already_indexed": len(existing), "added": added, "left": len(todo) - added, "quota_hit": quota_hit}


def stale_ids(chunks: list[Chunk], design: str, source_names: set[str]) -> list[str]:
    """Saved chunks of these sources that the current extraction no longer produces
    (for example after you improved the cleaning). Chunks of other sources, such as
    documents added later with add_document, are never touched."""
    collection = get_collection(design)
    keep = {c.id for c in chunks}
    stored = collection.get(include=["metadatas"])
    return [i for i, m in zip(stored["ids"], stored["metadatas"]) if m["source"] in source_names and i not in keep]


def index_file(path, designs=(CHOSEN_DESIGN,)) -> list[dict]:
    """Run one file through the pipeline. Re-adding a file that is already indexed adds nothing,
    because a chunk's id is a hash of its design, source, location and text."""
    path = Path(path).expanduser()
    if not path.is_file():
        raise FileNotFoundError(f"No such file: {path}")
    return [embed_and_store(chunk_file(path, design=design), design) for design in designs]


def search_chunks(query: str, k: int = 5, design: str = CHOSEN_DESIGN) -> list[dict]:
    collection = get_collection(design)
    if collection.count() == 0:
        return []
    vector = embed_texts([query])[0]
    result = collection.query(query_embeddings=[vector], n_results=min(k, collection.count()), include=["documents", "metadatas", "distances"])
    return [
        {"source": m["source"], "location": m["location"], "text": d, "distance": dist}
        for d, m, dist in zip(result["documents"][0], result["metadatas"][0], result["distances"][0])
    ]


def format_results(results: list[dict]) -> str:
    if not results:
        return "No results."
    return "\n\n".join(f"[{i}] {r['source']} | {r['location']}\n{r['text']}" for i, r in enumerate(results, 1))


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    dry_run = "--no-embed" in sys.argv
    designs = [d.strip() for d in os.environ.get("INDEX_DESIGNS", ",".join(DESIGNS)).split(",") if d.strip()]
    unknown = [d for d in designs if d not in CHUNKERS]
    if unknown:
        raise SystemExit(f"Unknown design(s) {unknown}; choose from {list(CHUNKERS)}")
    if not dry_run:
        load_api_key()

    manifest = {"retrieved": date.today().isoformat(), "embed_model": EMBED_MODEL, "documents": []}
    chunks_by_design: dict[str, list[Chunk]] = {d: [] for d in designs}
    total_words = 0
    print(f"{'document':<62}{'words':>8}")
    for source in SOURCES:
        path = download(source)
        blocks = extract_blocks(path)
        words = sum(len(b.text.split()) for b in blocks)
        total_words += words
        entry = {"name": source.name, "url": source.url, "licence": source.licence, "file": path.name, "words": words, "chunks": {}}
        for design in designs:
            chunks = CHUNKERS[design](source.name, blocks)
            chunks_by_design[design] += chunks
            entry["chunks"][design] = len(chunks)
        manifest["documents"].append(entry)
        print(f"{source.name[:60]:<62}{words:>8}")
        if blocks:
            print(f"    first: {blocks[0].location} | {blocks[0].text[:90]}")
            print(f"    last : {blocks[-1].location} | {blocks[-1].text[:90]}")
    for source in HOLDBACK:
        path = download(source, HOLDBACK_DIR)
        print(f"(held back for add_document, not indexed: {path})")

    print(f"\nTotal: {total_words} words in {len(SOURCES)} documents (the brief requires {MIN_WORDS_TOTAL}+ words, 3+ documents).")
    if total_words < MIN_WORDS_TOTAL:
        print(f"WARNING: below {MIN_WORDS_TOTAL} words. Add a document to SOURCES.")
    for design in designs:
        chunks = chunks_by_design[design]
        print(f"Design {design!r}: {len(chunks)} chunks, mean {sum(c.words for c in chunks) / max(len(chunks), 1):.0f} words")
    manifest["total_words"] = total_words
    INDEX_DIR.mkdir(exist_ok=True)
    MANIFEST.write_text(json.dumps(manifest, indent=2), encoding="utf-8")

    names = {s.name for s in SOURCES}
    if dry_run:
        print("\nAgainst the saved index:")
        for design in designs:
            chunks = chunks_by_design[design]
            ids = {c.id for c in chunks}
            collection = get_collection(design)
            saved = set(collection.get(ids=list(ids))["ids"]) if ids else set()
            print(f"  {design}: {len(saved)} saved, {len(ids) - len(saved)} would be embedded, {len(stale_ids(chunks, design, names))} stale would be removed")
        print("\nDry run: nothing embedded, no quota used.")
        return
    print("\nEmbedding (the free tier allows about 1,000 texts a day; saved vectors are never re-embedded) ...")
    quota_hit = False
    for design in designs:
        result = embed_and_store(chunks_by_design[design], design)
        print(f"  {design}: {result['already_indexed']} already saved, {result['added']} added, {result['left']} left")
        if result["quota_hit"]:
            quota_hit = True
            break
        stale = stale_ids(chunks_by_design[design], design, names)
        for i in range(0, len(stale), 500):
            get_collection(design).delete(ids=stale[i : i + 500])
        if stale:
            print(f"  {design}: removed {len(stale)} stale chunks from an earlier extraction")
    if quota_hit:
        print("\nDaily limit reached. Run the same command again after 09:00 (Spain time); it continues where it stopped.")
    else:
        print(f"\nDone. Commit the index/ folder. Manifest: {MANIFEST.name}")


if __name__ == "__main__":
    main()
