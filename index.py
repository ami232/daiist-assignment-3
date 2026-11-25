"""
Assignment 3: build the index (`main.py index`).

Corpus: five NIST publications on cybersecurity and AI risk management (US
federal government works, public domain). The index stage

  1. downloads them into corpus/ (git-ignored),
  2. extracts and cleans the text of every page,
  3. cuts it into ~220-word chunks that carry source, page and section,
  4. embeds the chunks with Gemini and stores them in index/ (ChromaDB).

Every embedding is saved the moment it comes back, and only chunks without a
stored vector are embedded, so a crash or the free-tier daily limit loses
nothing: run `main.py index` again tomorrow and it continues.

server.py imports chunk_file() and embed_and_store() from here for its
add_document tool.

    uv run python main.py index
    uv run python index.py --chunk-only   # no API calls: just print the chunk statistics
    uv run python index.py --reset        # wipe index/ and start again
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import sys
import time
import unicodedata
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"
CHROMA_DIR = INDEX_DIR / "chroma"
MANIFEST_FILE = INDEX_DIR / "manifest.json"
COLLECTION = "corpus"

EMBED_MODEL = os.environ.get("EMBED_MODEL", "gemini-embedding-2")
EMBED_DIM = 768          # smaller vectors keep index/ tiny; we re-normalise them ourselves
EMBED_BATCH = 50         # every text in a batch counts against the daily free-tier quota
CHUNK_WORDS = 220
OVERLAP_WORDS = 40
SNAP_WORDS = 35          # try to end a chunk on a sentence boundary this close to the target

LICENCE = "US federal government work, not subject to copyright (17 U.S.C. 105)"

# Public documents. `date` is the publication date printed on the cover.
SOURCES = [
    {
        "id": "nist-ai-rmf-1.0",
        "title": "NIST AI 100-1: Artificial Intelligence Risk Management Framework (AI RMF 1.0)",
        "url": "https://nvlpubs.nist.gov/nistpubs/ai/nist.ai.100-1.pdf",
        "date": "2023-01",
    },
    {
        "id": "nist-ai-600-1",
        "title": "NIST AI 600-1: AI RMF Generative AI Profile",
        "url": "https://nvlpubs.nist.gov/nistpubs/ai/NIST.AI.600-1.pdf",
        "date": "2024-07",
    },
    {
        "id": "nist-csf-2.0",
        "title": "NIST CSWP 29: The NIST Cybersecurity Framework (CSF) 2.0",
        "url": "https://nvlpubs.nist.gov/nistpubs/CSWP/NIST.CSWP.29.pdf",
        "date": "2024-02",
    },
    {
        "id": "nist-sp-800-61r3",
        "title": "NIST SP 800-61 Rev. 3: Incident Response Recommendations and Considerations for Cybersecurity Risk Management",
        "url": "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-61r3.pdf",
        "date": "2025-04",
    },
    {
        "id": "nist-sp-800-218",
        "title": "NIST SP 800-218: Secure Software Development Framework (SSDF) Version 1.1",
        "url": "https://nvlpubs.nist.gov/nistpubs/SpecialPublications/NIST.SP.800-218.pdf",
        "date": "2022-02",
    },
]
FILENAMES = {s["id"]: f"{s['id']}.pdf" for s in SOURCES}


def log(*args) -> None:
    """Log to stderr: server.py imports this module and stdout carries the MCP protocol."""
    print(*args, file=sys.stderr, flush=True)


# --------------------------------------------------------------------------
# Extraction and cleaning
# --------------------------------------------------------------------------

HEADING_RE = re.compile(
    r"^(?:(?:Appendix|Annex)\s+[A-Z]\b.{0,90}|\d{1,2}(?:\.\d{1,2}){0,3}\.?\s+[A-Z][^.]{2,100})$"
)
LEADER_RE = re.compile(r"\.{5,}|(?:\. ){5,}")          # table-of-contents leader dots
PAGE_NUMBER_RE = re.compile(r"^(?:page\s+)?(?:\d{1,3}|[ivxlc]{1,6})$", re.IGNORECASE)
WEAK_ENDINGS = {"and", "or", "the", "of", "a", "an", "to", "for", "in", "that", "with", "by", "is", "are"}


def is_heading(line: str) -> bool:
    """A numbered or appendix heading, not a numbered list item that happens to start a sentence."""
    words = line.split()
    if not HEADING_RE.match(line) or len(words) > 14:
        return False
    if line.endswith((".", ",", ";")) and not re.fullmatch(r"[\d.]+", words[-1]):
        return False
    if words[-1].lower() in WEAK_ENDINGS:
        return False
    body = [w for w in words[1:] if len(w) > 3]
    return not body or sum(w[0].isupper() for w in body) / len(body) >= 0.5


@dataclass
class Chunk:
    id: str
    doc_id: str
    title: str
    url: str
    section: str
    page_start: int
    page_end: int
    unit: str            # "p." for PDF pages, "part" for text files
    text: str
    n_words: int

    @property
    def location(self) -> str:
        if self.page_start == self.page_end:
            return f"{self.unit} {self.page_start}"
        plural = "pp." if self.unit == "p." else f"{self.unit}s"
        return f"{plural} {self.page_start}-{self.page_end}"

    @property
    def sha(self) -> str:
        return hashlib.sha256(self.embedding_text.encode("utf-8")).hexdigest()[:16]

    @property
    def embedding_text(self) -> str:
        """What gets embedded: the passage with its document and section as context."""
        head = f"title: {self.title}"
        if self.section:
            head += f" | section: {self.section}"
        return f"{head} | text: {self.text}"

    def metadata(self) -> dict:
        return {
            "source": self.doc_id,
            "title": self.title,
            "url": self.url,
            "section": self.section,
            "page_start": self.page_start,
            "page_end": self.page_end,
            "location": self.location,
            "n_words": self.n_words,
            "sha": self.sha,
        }


def normalise(text: str) -> str:
    """NFKC turns ligatures (fi, fl) into plain letters; drop soft hyphens and control characters."""
    text = unicodedata.normalize("NFKC", text).replace("­", "")
    return re.sub(r"[\x00-\x08\x0b-\x1f]", " ", text)


def extract_pdf_pages(path: Path) -> list[str]:
    from pypdf import PdfReader

    reader = PdfReader(str(path))
    return [normalise(page.extract_text() or "") for page in reader.pages]


def extract_text_pages(path: Path) -> list[str]:
    """.txt / .md / .html: split into ~400-word 'parts' so that every chunk still has a location."""
    raw = path.read_text(encoding="utf-8", errors="replace")
    if path.suffix.lower() in {".html", ".htm"}:
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(raw, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        raw = soup.get_text("\n")
    raw = normalise(raw)
    lines, parts, current, count = raw.splitlines(), [], [], 0
    for line in lines:
        current.append(line)
        count += len(line.split())
        if count >= 400:
            parts.append("\n".join(current))
            current, count = [], 0
    if current:
        parts.append("\n".join(current))
    return parts or [""]


def strip_running_lines(pages: list[list[str]]) -> list[list[str]]:
    """Remove running headers and footers (a line that repeats on many pages),
    page numbers and table-of-contents leader lines."""
    if len(pages) >= 8:
        seen = Counter()
        for lines in pages:
            for key in {re.sub(r"\d+", "#", ln.lower()) for ln in lines if 0 < len(ln) <= 110}:
                seen[key] += 1
        repeated = {k for k, n in seen.items() if n >= 0.3 * len(pages)}
    else:
        repeated = set()
    cleaned = []
    for lines in pages:
        kept = []
        for ln in lines:
            if not ln or PAGE_NUMBER_RE.match(ln) or LEADER_RE.search(ln):
                continue
            if re.sub(r"\d+", "#", ln.lower()) in repeated:
                continue
            kept.append(ln)
        cleaned.append(kept)
    return cleaned


def join_hyphenated(lines_by_page: list[list[str]]) -> list[list[str]]:
    """Justified PDFs break words across lines ("re-" / "quires"). Rejoin them, but keep the
    hyphen when the document itself uses the hyphenated compound ("high-risk")."""
    vocab = Counter()
    for lines in lines_by_page:
        for ln in lines:
            vocab.update(w.lower() for w in re.findall(r"[A-Za-z]+(?:-[A-Za-z]+)*", ln))

    def fix(left: str, right: str) -> tuple[str, str]:
        m = re.search(r"([A-Za-z]+)-$", left)
        n = re.match(r"([a-z]+)(.*)$", right)
        if not (m and n):
            return left, right
        a, b = m.group(1), n.group(1)
        hyphenated, joined = f"{a}-{b}".lower(), f"{a}{b}".lower()
        if vocab[joined] > vocab[hyphenated]:
            word = f"{a}{b}"
        elif vocab[hyphenated] > 0:
            word = f"{a}-{b}"
        elif vocab[a.lower()] >= 2 and vocab[b.lower()] >= 2:   # two real words: a compound ("relevant-context")
            word = f"{a}-{b}"
        else:                                                   # a word split by justification ("re-" "quires")
            word = f"{a}{b}"
        return left[: m.start()] + word, n.group(2).lstrip()

    out = []
    for lines in lines_by_page:
        lines = list(lines)
        for i in range(len(lines) - 1):
            if lines[i].endswith("-") and lines[i + 1][:1].islower():
                lines[i], lines[i + 1] = fix(lines[i], lines[i + 1])
        out.append(lines)
    return out


def page_texts_to_words(raw_pages: list[str]) -> list[tuple[str, int, str]]:
    """Clean the pages and return one (word, page number, section) tuple per word."""
    pages = [[ln.strip() for ln in text.splitlines()] for text in raw_pages]
    pages = strip_running_lines(pages)
    pages = join_hyphenated(pages)
    words: list[tuple[str, int, str]] = []
    section = ""
    for number, lines in enumerate(pages, start=1):
        for ln in lines:
            if is_heading(ln):
                section = ln
            words.extend((w, number, section) for w in ln.split())
    return words


# --------------------------------------------------------------------------
# Chunking
# --------------------------------------------------------------------------

def slugify(text: str) -> str:
    return re.sub(r"[^a-z0-9.]+", "-", text.lower()).strip("-") or "document"


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def source_for(path: Path) -> dict:
    """Metadata for a file: from SOURCES when it is part of the corpus, otherwise derived."""
    for s in SOURCES:
        if path.name == FILENAMES[s["id"]]:
            return s
    return {"id": slugify(path.stem), "title": path.stem.replace("_", " "), "url": f"file://{path.name}", "date": ""}


def read_words(path: Path) -> tuple[list[tuple[str, int, str]], str]:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        raw_pages, unit = extract_pdf_pages(path), "p."
    elif suffix in {".txt", ".md", ".html", ".htm"}:
        raw_pages, unit = extract_text_pages(path), "part"
    else:
        raise ValueError(f"Unsupported file type {suffix!r}; use .pdf, .txt, .md or .html")
    return page_texts_to_words(raw_pages), unit


def chunk_file(path: str | Path, source: dict | None = None) -> list[Chunk]:
    """Extract, clean and chunk one file. Pure function: no network, no API calls."""
    path = Path(path)
    source = source or source_for(path)
    words, unit = read_words(path)
    chunks: list[Chunk] = []
    start = 0
    while start < len(words):
        end = min(start + CHUNK_WORDS, len(words))
        if end < len(words):                       # snap the end to a sentence boundary if one is close
            for cut in range(end, max(end - SNAP_WORDS, start + CHUNK_WORDS // 2), -1):
                if words[cut - 1][0].endswith((".", "?", "!", ":")):
                    end = cut
                    break
        window = words[start:end]
        text = " ".join(w for w, _, _ in window)
        if len(window) >= 25:                      # ignore stray crumbs at the end of a file
            chunks.append(
                Chunk(
                    id=f"{source['id']}-{len(chunks):04d}",
                    doc_id=source["id"],
                    title=source["title"],
                    url=source["url"],
                    section=window[0][2],
                    page_start=window[0][1],
                    page_end=window[-1][1],
                    unit=unit,
                    text=text,
                    n_words=len(window),
                )
            )
        if end >= len(words):
            break
        start = max(end - OVERLAP_WORDS, start + 1)
    return chunks


# --------------------------------------------------------------------------
# Embedding and storage
# --------------------------------------------------------------------------

class QuotaExhausted(RuntimeError):
    """The free-tier daily embedding quota is used up. Progress is saved; run again tomorrow."""


_client = None
_use_dimensions = True


def genai_client():
    global _client
    if _client is None:
        from google import genai

        from api_key import load_api_key

        _client = genai.Client(api_key=load_api_key())
    return _client


def _retry_delay(message: str) -> float:
    m = re.search(r"retry in ([\d.]+)s", message, re.IGNORECASE) or re.search(r"'retryDelay': '(\d+)s'", message)
    return float(m.group(1)) + 1 if m else 20.0


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed a list of texts (one API call), retrying on per-minute limits."""
    global _use_dimensions
    import numpy as np
    from google.genai import types

    for attempt in range(6):
        try:
            config = types.EmbedContentConfig(output_dimensionality=EMBED_DIM) if _use_dimensions else None
            # gemini-embedding-2 treats a list of plain strings as parts of ONE content (one vector back);
            # wrapping each text in its own Content gives one vector per text.
            contents = [types.Content(parts=[types.Part(text=t)]) for t in texts]
            response = genai_client().models.embed_content(model=EMBED_MODEL, contents=contents, config=config)
            if len(response.embeddings) != len(texts):
                raise RuntimeError(f"Expected {len(texts)} embeddings, got {len(response.embeddings)}")
            vectors = np.array([e.values for e in response.embeddings], dtype="float32")
            vectors /= np.linalg.norm(vectors, axis=1, keepdims=True)    # truncated dims are not unit length
            return vectors.tolist()
        except Exception as error:  # noqa: BLE001 - classify by message, the SDK has several error types
            message = str(error)
            if "output_dimensionality" in message and _use_dimensions:
                _use_dimensions = False
                log("Model rejected output_dimensionality; using its default size.")
                continue
            if "PerDay" in message or "per day" in message.lower():
                raise QuotaExhausted(message) from error
            if "429" in message or "RESOURCE_EXHAUSTED" in message or "503" in message or "UNAVAILABLE" in message:
                delay = min(_retry_delay(message) * (attempt + 1), 90)
                log(f"Rate limited; waiting {delay:.0f}s (attempt {attempt + 1}/6)")
                time.sleep(delay)
                continue
            raise
    raise RuntimeError("Embedding kept failing after 6 attempts")


def get_collection(reset: bool = False):
    import chromadb
    from chromadb.config import Settings

    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR), settings=Settings(anonymized_telemetry=False))
    if reset:
        try:
            client.delete_collection(COLLECTION)
        except Exception:  # noqa: BLE001 - nothing to delete
            pass
    return client.get_or_create_collection(COLLECTION, metadata={"hnsw:space": "cosine"})


def embed_and_store(chunks: list[Chunk], embedder=None, collection=None) -> int:
    """Embed the chunks that have no stored vector yet (or whose text changed) and store them.
    Each batch is written as soon as it returns. Returns how many texts were embedded."""
    embedder = embedder or embed_texts            # looked up at call time so tests can swap it
    collection = collection or get_collection()
    ids = [c.id for c in chunks]
    stored = {}
    for i in range(0, len(ids), 500):
        got = collection.get(ids=ids[i : i + 500], include=["metadatas"])
        stored.update({id_: (meta or {}).get("sha") for id_, meta in zip(got["ids"], got["metadatas"])})
    todo = [c for c in chunks if stored.get(c.id) != c.sha]
    done = 0
    for i in range(0, len(todo), EMBED_BATCH):
        batch = todo[i : i + EMBED_BATCH]
        vectors = embedder([c.embedding_text for c in batch])
        collection.upsert(
            ids=[c.id for c in batch],
            embeddings=vectors,
            documents=[c.text for c in batch],
            metadatas=[c.metadata() for c in batch],
        )
        done += len(batch)
        log(f"  embedded {done}/{len(todo)} new chunks")
    return done


def remove_document(doc_id: str, collection=None) -> int:
    collection = collection or get_collection()
    found = collection.get(where={"source": doc_id}, include=[])["ids"]
    if found:
        collection.delete(ids=found)
    return len(found)


def load_manifest() -> dict:
    if MANIFEST_FILE.is_file():
        return json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))
    return {}


def save_manifest(manifest: dict) -> None:
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    MANIFEST_FILE.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def record_document(source: dict, path: Path, chunks: list[Chunk], words: int | None = None) -> None:
    manifest = load_manifest()
    manifest[source["id"]] = {
        "title": source["title"],
        "url": source["url"],
        "date": source.get("date", ""),
        "licence": LICENCE,
        "file": path.name,
        "sha256": file_sha256(path),
        "words": words if words is not None else sum(c.n_words for c in chunks),   # chunks overlap, so pass the true count
        "chunks": len(chunks),
    }
    save_manifest(manifest)


# --------------------------------------------------------------------------
# Guardrail shared by server.py and agent.py: which files add_document may read
# --------------------------------------------------------------------------

ALLOWED_SUFFIXES = {".pdf", ".txt", ".md", ".html", ".htm"}
# add_document only reads from these folders, so a prompt injected through a retrieved
# passage cannot make the agent index ~/.ssh, .env or anything else private.
ALLOWED_DIRS = [CORPUS_DIR.resolve(), (ROOT / "extra").resolve()]


def check_add_path(path: str) -> Path:
    """Resolve `path` and refuse anything outside the allowed folders or of the wrong type."""
    p = Path(path).expanduser()
    if not p.is_absolute():
        p = ROOT / p
    p = p.resolve()
    if not any(p.is_relative_to(d) for d in ALLOWED_DIRS):
        allowed = ", ".join(f"{d.relative_to(ROOT)}/" for d in ALLOWED_DIRS)
        raise ValueError(f"Refused: add_document only reads files inside {allowed} (got {path!r}).")
    if p.suffix.lower() not in ALLOWED_SUFFIXES:
        raise ValueError(f"Refused: unsupported file type {p.suffix!r}. Use one of {sorted(ALLOWED_SUFFIXES)}.")
    if not p.is_file():
        raise ValueError(f"File not found: {path!r}.")
    return p


# --------------------------------------------------------------------------
# Download and main
# --------------------------------------------------------------------------

def download_corpus() -> list[Path]:
    import httpx

    CORPUS_DIR.mkdir(exist_ok=True)
    paths = []
    for source in SOURCES:
        target = CORPUS_DIR / FILENAMES[source["id"]]
        if not target.exists():
            log(f"Downloading {source['url']}")
            response = httpx.get(source["url"], follow_redirects=True, timeout=120, headers={"User-Agent": "daiist-assignment-3"})
            response.raise_for_status()
            if not response.content.startswith(b"%PDF"):
                raise RuntimeError(f"{source['url']} did not return a PDF")
            target.write_bytes(response.content)
        paths.append(target)
    return paths


def print_stats(rows: list[tuple[str, int, int, int]]) -> None:
    print(f"{'document':<22}{'pages':>7}{'words':>9}{'chunks':>8}")
    for doc_id, pages, words, chunks in rows:
        print(f"{doc_id:<22}{pages:>7}{words:>9}{chunks:>8}")
    print(f"{'TOTAL':<22}{'':>7}{sum(r[2] for r in rows):>9}{sum(r[3] for r in rows):>8}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the index.")
    parser.add_argument("--chunk-only", action="store_true", help="download and chunk, but call no API")
    parser.add_argument("--reset", action="store_true", help="delete index/ first")
    args = parser.parse_args()

    if args.reset and INDEX_DIR.exists():
        shutil.rmtree(CHROMA_DIR, ignore_errors=True)
        MANIFEST_FILE.unlink(missing_ok=True)

    paths = download_corpus()
    all_chunks: dict[str, list[Chunk]] = {}
    true_words: dict[str, int] = {}
    for source, path in zip(SOURCES, paths):
        all_chunks[source["id"]] = chunk_file(path, source)
        true_words[source["id"]] = len(read_words(path)[0])
    rows = [(d, max(c.page_end for c in cs), true_words[d], len(cs)) for d, cs in all_chunks.items()]
    print_stats(rows)

    if args.chunk_only:
        return

    collection = get_collection()
    embedded = 0
    try:
        for source, path in zip(SOURCES, paths):
            log(f"Indexing {source['id']} ({len(all_chunks[source['id']])} chunks)")
            embedded += embed_and_store(all_chunks[source["id"]], collection=collection)
            record_document(source, path, all_chunks[source["id"]], true_words[source["id"]])
    except QuotaExhausted as error:
        log(f"\nDaily embedding quota reached. Everything embedded so far is saved; run this again after "
            f"09:00 (Spain time) to finish.\n{str(error)[:300]}")
        raise SystemExit(1) from error
    print(f"\nEmbedded {embedded} new chunks; the index holds {collection.count()} chunks.")


if __name__ == "__main__":
    main()
