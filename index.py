"""
Assignment 3: build the index (`main.py index`).

Corpus: three FDA documents for people running a restaurant kitchen
(US federal government works, public domain). The pipeline:

    download  ->  extract (pypdf, page by page)  ->  clean  ->  chunk (two designs)
              ->  embed (Gemini, cached per text)  ->  store (ChromaDB in index/)

Every vector is written to index/embedding_cache.sqlite as soon as Gemini returns
it, and a text is only sent to Gemini when it is not in that cache. So a crash, or
the free tier's daily limit, loses nothing: run `main.py index` again tomorrow
and it carries on where it stopped. The same cache holds query vectors, so asking
the same question twice costs one embedding, not two.

server.py imports `chunk_file`, `embed_and_store`, `search` and friends from here.
"""

from __future__ import annotations

import hashlib
import json
import re
import sqlite3
import sys
import threading
import time
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"          # downloaded PDFs (git-ignored)
INDEX_DIR = ROOT / "index"            # committed
CHROMA_DIR = INDEX_DIR / "chroma"
CACHE_PATH = INDEX_DIR / "embedding_cache.sqlite"

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768                       # Matryoshka truncation of the 3072-d default: 4x smaller index
EMBED_BATCH = 50                      # texts per request; each text counts toward the daily quota

# The two retrieval designs compared in evaluate.py. ACTIVE_DESIGN is the one
# server.py and agent.py search; it was chosen from the hit rates (see REPORT.md).
DESIGNS = ("fixed", "structure")
ACTIVE_DESIGN = "structure"

FIXED_WORDS, FIXED_OVERLAP = 250, 50  # design "fixed": 250-word windows, 50 words shared
STRUCT_MIN, STRUCT_MAX = 80, 350      # design "structure": merge below 80 words, split above 350


def log(*args) -> None:
    """Log to stderr: stdout belongs to the MCP protocol when server.py imports this."""
    print(*args, file=sys.stderr, flush=True)


# --------------------------------------------------------------------------- corpus

@dataclass(frozen=True)
class Document:
    source: str          # id used in metadata, citations and eval/questions.csv
    title: str
    url: str
    date: str
    pages: tuple[int, int] | None = None   # 1-based PDF page range to keep, None = all
    kind: str = "pages"                    # "food_code" gets section-aware parsing

    @property
    def path(self) -> Path:
        return CORPUS_DIR / f"{self.source}.pdf"


CORPUS = [
    Document(
        source="food_code_2022",
        title="FDA Food Code 2022 (Chapters 1-7)",
        url="https://www.fda.gov/media/164194/download",
        date="2022-12-28",
        pages=(22, 165),   # Chapter 1 to the end of Chapter 7; front matter, Ch. 8 and annexes left out
        kind="food_code",
    ),
    Document(
        source="employee_health_handbook",
        title="FDA Employee Health and Personal Hygiene Handbook (2020)",
        url="https://www.fda.gov/media/77065/download",
        date="2020",
        pages=(3, 45),     # skip cover and table of contents
    ),
    Document(
        source="haccp_operators_manual",
        title="FDA Managing Food Safety: A Manual for the Voluntary Use of HACCP Principles for Operators of Food Service and Retail Establishments",
        url="https://www.fda.gov/media/71976/download",
        date="2006-04",
        pages=(5, 86),     # skip cover and the four table-of-contents pages
    ),
]


def download(doc: Document) -> Path:
    """Fetch a corpus PDF into corpus/ unless it is already there."""
    import httpx

    if doc.path.is_file() and doc.path.read_bytes()[:5] == b"%PDF-":
        return doc.path
    CORPUS_DIR.mkdir(exist_ok=True)
    log(f"Downloading {doc.source} from {doc.url}")
    response = httpx.get(doc.url, follow_redirects=True, timeout=180,
                         headers={"User-Agent": "Mozilla/5.0 (course assignment; RAG corpus)"})
    response.raise_for_status()
    if response.content[:5] != b"%PDF-":
        raise RuntimeError(f"{doc.url} did not return a PDF")
    doc.path.write_bytes(response.content)
    return doc.path


# --------------------------------------------------------------------------- extract + clean

FOOD_CODE_HEADER = re.compile(r"^\s*FDA Food Code 2022\b.*$", re.M)
FOOD_CODE_FOOTER = re.compile(r"^\s*Chapter \d+ - \d+\s*$", re.M)
PAGE_NUMBER_LINE = re.compile(r"^\s*(?:[ivxlc]+|\d{1,3})\s*$", re.M)
DOT_LEADER_LINE = re.compile(r"^.*\.{5,}.*$", re.M)          # table-of-contents lines
# Food Code priority markers after a requirement: "... above the floor. P" / "...; Pf and"
PRIORITY_AT_EOL = re.compile(r"(?<=\S)\s+(?:P|Pf)\s*$", re.M)
PRIORITY_INLINE = re.compile(r"(?<=[;:,.])\s+(?:P|Pf)(?=\s)")


def clean_text(text: str, food_code: bool) -> str:
    """Turn one page of pypdf output into readable text.

    Problems fixed (see REPORT.md, Ingestion):
    - running headers/footers and bare page numbers repeat on every page;
    - section numbers broken over two lines ("7-301.\\n11 Separation." and
      "4-\\n204.13"), which hid section headings and cross-references;
    - the Food Code's P / Pf priority markers glued to the end of requirements;
    - ligatures ("speciﬁc"), URLs split as "https:/ /", and degree signs
      extracted as a letter o ("54oC (130oF)");
    - words hyphenated across lines.
    """
    text = unicodedata.normalize("NFKC", text).replace(" ", " ")
    if food_code:
        text = FOOD_CODE_HEADER.sub("", text)
        text = FOOD_CODE_FOOTER.sub("", text)
        text = re.sub(r"(\d-\d{3}\.)\s*\n\s*(\d{2,3}\b)", r"\1\2", text)   # 7-301.\n11 -> 7-301.11
        text = re.sub(r"(\d-)\s*\n\s*(\d{3}\.\d)", r"\1\2", text)         # 4-\n204.13 -> 4-204.13
        text = PRIORITY_AT_EOL.sub("", text)
        text = PRIORITY_INLINE.sub("", text)
        text = re.sub(r"([.;:,])(?:P|Pf)(?=\s|$)", r"\1", text, flags=re.M)  # "clean.P" -> "clean."
        text = re.sub(r"[ \t]+(?:P|Pf)(?=[;,.]?(?:\s|$))", "", text, flags=re.M)  # "or less Pf; or" -> "or less; or"
    text = DOT_LEADER_LINE.sub("", text)
    text = PAGE_NUMBER_LINE.sub("", text)
    text = text.replace(":/ /", "://").replace("°Š", "°")
    text = re.sub(r"(\d)\s?o([CF])\b", "\\1°\\2", text)                   # 54oC (130oF) -> 54°C (130°F)
    text = re.sub(r"([a-z])-\n\s*([a-z])", r"\1-\2", text)               # self-\nservice -> self-service
    text = re.sub(r"[ \t]+", " ", text)
    lines = [line.strip() for line in text.splitlines()]
    return "\n".join(line for line in lines if line)


@dataclass
class Block:
    """A piece of one page, inside at most one Food Code section."""
    source: str
    page: int                 # 1-based PDF page
    text: str
    section: str = ""         # Food Code section number, e.g. "3-501.16"
    section_title: str = ""
    subpart: str = ""         # e.g. "3-501"
    chapter: str = ""


SECTION = re.compile(r"^(\d)-(\d{3})\.(\d{2,3})\s+([A-Z][A-Za-z].*)$")
SUBPART = re.compile(r"^(\d)-(\d{3})\s+([A-Z].*)$")


def extract_blocks(doc: Document, path: Path | None = None) -> list[Block]:
    """Extract and clean a PDF into blocks: one per page, split at Food Code sections."""
    from pypdf import PdfReader

    reader = PdfReader(str(path or doc.path))
    first, last = doc.pages or (1, len(reader.pages))
    blocks: list[Block] = []
    food_code = doc.kind == "food_code"
    section = title = subpart = ""
    last_key: tuple[int, ...] = (0, 0, 0)
    for page_no in range(first, min(last, len(reader.pages)) + 1):
        text = clean_text(reader.pages[page_no - 1].extract_text() or "", food_code)
        if not food_code:
            if text.strip():
                blocks.append(Block(doc.source, page_no, text))
            continue
        current: list[str] = []
        lines = text.splitlines()
        for i, line in enumerate(lines):
            m = SECTION.match(line)
            key = tuple(int(g) for g in m.groups()[:3]) if m else None
            # A real heading increases the section number within the same (or the
            # next) chapter; a cross-reference that happens to start a line, such
            # as "8-201.14 (C) and (D) ..." or "3-401.15 Pf, or", does not.
            if (m and key > last_key and (last_key[0] == 0 or key[0] in (last_key[0], last_key[0] + 1))
                    and not re.match(r"(?:P|Pf)\b", m.group(4))):
                if current:
                    blocks.append(Block(doc.source, page_no, "\n".join(current), section, title, subpart, section[:1]))
                    current = []
                section = f"{key[0]}-{key[1]:03d}.{m.group(3)}"
                title = m.group(4).strip()
                nxt = lines[i + 1] if i + 1 < len(lines) else ""
                if not title.endswith(".") and len(nxt.split()) <= 8 and nxt.endswith("."):
                    title += " " + nxt          # heading wrapped onto a second line
                title = title.rstrip(".")
                subpart = f"{key[0]}-{key[1]:03d}"
                last_key = key
            current.append(line)
        if current:
            blocks.append(Block(doc.source, page_no, "\n".join(current), section, title, subpart, section[:1]))
    return blocks


# --------------------------------------------------------------------------- chunk

@dataclass
class Chunk:
    source: str
    title: str                # document title
    text: str
    page_start: int
    page_end: int
    sections: list[str] = field(default_factory=list)
    heading: str = ""         # section title(s) used as the embedding title
    design: str = ""
    origin: str = "corpus"    # "corpus" or "added" (by the add_document tool)
    url: str = ""

    @property
    def location(self) -> str:
        pages = f"p. {self.page_start}" if self.page_start == self.page_end else f"pp. {self.page_start}-{self.page_end}"
        if not self.sections:
            return pages
        secs = self.sections[0] if len(self.sections) == 1 else f"{self.sections[0]} to {self.sections[-1]}"
        return f"§{secs}, {pages}"

    @property
    def cite(self) -> str:
        """The exact citation the agent must copy, e.g. [food_code_2022, §3-501.16, p. 86]."""
        return f"[{self.source}, {self.location}]"

    @property
    def id(self) -> str:
        key = f"{self.design}|{self.source}|{self.location}|{self.text}"
        return hashlib.sha1(key.encode()).hexdigest()[:20]

    def embed_input(self) -> str:
        """Document side of Gemini Embedding 2's asymmetric retrieval format."""
        title = f"{self.title}: {self.heading}" if self.heading else self.title
        return f"title: {title} | text: {self.text}"

    def metadata(self) -> dict:
        return {
            "source": self.source, "title": self.title, "url": self.url,
            "page_start": self.page_start, "page_end": self.page_end,
            "sections": ";".join(self.sections), "heading": self.heading,
            "location": self.location, "cite": self.cite,
            "design": self.design, "origin": self.origin, "words": len(self.text.split()),
        }


def _words_with_positions(blocks: list[Block]) -> list[tuple[str, int, str]]:
    return [(w, b.page, b.section) for b in blocks for w in b.text.split()]


def chunk_fixed(blocks: list[Block], doc: Document) -> list[Chunk]:
    """Design 'fixed': 250-word windows with 50 words of overlap, ignoring structure."""
    words = _words_with_positions(blocks)
    chunks, step = [], FIXED_WORDS - FIXED_OVERLAP
    for start in range(0, len(words), step):
        window = words[start:start + FIXED_WORDS]
        if start and len(window) < FIXED_OVERLAP + 20:   # tail already covered by the previous window
            break
        sections = list(dict.fromkeys(s for _, _, s in window if s))
        chunks.append(Chunk(doc.source, doc.title, " ".join(w for w, _, _ in window),
                            window[0][1], window[-1][1], sections, "", "fixed", url=doc.url))
    return chunks


def _words(lines: list[tuple[str, int]]) -> int:
    return sum(len(text.split()) for text, _ in lines)


def _split_long(lines: list[tuple[str, int]], limit: int) -> list[list[tuple[str, int]]]:
    """Split lines into roughly equal groups of at most ~limit words, at line boundaries."""
    total = _words(lines)
    if total <= limit:
        return [lines]
    pieces = -(-total // 300)                 # ceil: pieces of about 300 words
    target = total / pieces
    groups, current, count = [], [], 0
    for line in lines:
        n = len(line[0].split())
        if current and count + n > target and len(groups) < pieces - 1:
            groups.append(current)
            current, count = [], 0
        current.append(line)
        count += n
    if current:
        groups.append(current)
    return groups


def chunk_structure(blocks: list[Block], doc: Document) -> list[Chunk]:
    """Design 'structure': one Food Code section per chunk; one page per chunk elsewhere.

    Sections over 350 words are split at line breaks into near-equal pieces that
    all keep the section number. Sections under 80 words are merged with a
    neighbouring section of the same Food Code Part (e.g. 4-7, Sanitization), so
    a one-line rule does not become a near-empty chunk.
    """
    # 1. group blocks into units: a Food Code section, or a page
    units: list[dict] = []
    for b in blocks:
        key = b.section if doc.kind == "food_code" else f"page {b.page}"
        if units and units[-1]["key"] == key:
            units[-1]["lines"] += [(line, b.page) for line in b.text.splitlines()]
            units[-1]["page_end"] = b.page
        else:
            units.append({"key": key, "lines": [(line, b.page) for line in b.text.splitlines()], "page_start": b.page, "page_end": b.page,
                          "sections": [b.section] if b.section else [],
                          "titles": [b.section_title] if b.section_title else [],
                          "part": b.section[:3] if doc.kind == "food_code" else doc.source})

    def absorb(into: dict, other: dict) -> None:
        into["lines"] += other["lines"]
        into["page_start"] = min(into["page_start"], other["page_start"])
        into["page_end"] = max(into["page_end"], other["page_end"])
        for sec, title in zip(other["sections"], other["titles"]):
            if sec not in into["sections"]:
                into["sections"].append(sec)
                into["titles"].append(title)

    # 2. merge short units forward, then any short leftover backward, within one Part
    merged: list[dict] = []
    for u in units:
        prev = merged[-1] if merged else None
        if prev and _words(prev["lines"]) < STRUCT_MIN and _words(prev["lines"]) + _words(u["lines"]) <= STRUCT_MAX \
                and (prev["part"] == u["part"] or not prev["sections"]):
            prev["part"] = u["part"]
            absorb(prev, u)
        else:
            merged.append(u)
    final: list[dict] = []
    for u in merged:
        prev = final[-1] if final else None
        if prev and _words(u["lines"]) < STRUCT_MIN and prev["part"] == u["part"] \
                and _words(prev["lines"]) + _words(u["lines"]) <= STRUCT_MAX + 50:
            absorb(prev, u)
        else:
            final.append(u)
    merged = final

    # 3. split long units
    chunks = []
    for u in merged:
        heading = "; ".join(f"{s} {t}" for s, t in zip(u["sections"], u["titles"]))[:300]
        for part in _split_long(u["lines"], STRUCT_MAX):
            # each piece cites the pages its own lines came from, not the whole section's
            chunks.append(Chunk(doc.source, doc.title, "\n".join(t for t, _ in part), part[0][1], part[-1][1],
                                list(u["sections"]), heading, "structure", url=doc.url))
    return chunks


CHUNKERS = {"fixed": chunk_fixed, "structure": chunk_structure}


def chunk_file(path: str | Path, design: str = ACTIVE_DESIGN, source: str | None = None,
               title: str | None = None, url: str = "") -> list[Chunk]:
    """Extract, clean and chunk one file (PDF, .txt, .md or .html) with the given design.

    Used by the add_document tool for files outside the built-in corpus. A file
    whose name matches a corpus document reuses that document's settings.
    """
    path = Path(path).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"No file at {path}")
    known = {d.path.resolve(): d for d in CORPUS}
    doc = known.get(path) or Document(
        source=source or re.sub(r"[^a-z0-9]+", "_", path.stem.lower()).strip("_"),
        title=title or path.stem.replace("_", " ").replace("-", " "),
        url=url or path.as_uri(), date="", pages=None)
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        if doc.kind != "food_code" and path not in known:
            from pypdf import PdfReader
            first_page = PdfReader(str(path)).pages[0].extract_text() or ""
            if "FDA Food Code" in first_page:      # another part of the Food Code: parse its sections
                doc = Document(doc.source, doc.title, doc.url, doc.date, None, "food_code")
        blocks = extract_blocks(doc, path)
    elif suffix in {".txt", ".md", ".html", ".htm"}:
        raw = path.read_text(encoding="utf-8", errors="replace")
        if suffix in {".html", ".htm"}:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(raw, "html.parser")
            for tag in soup(["script", "style", "nav", "header", "footer"]):
                tag.decompose()
            raw = soup.get_text("\n")
        text = clean_text(raw, food_code=False)
        # text files have no pages: count every ~400 words as a "page" so citations still locate.
        # Very long lines (a paragraph per line) are broken into sentences so chunks can split.
        words = [piece for line in text.split("\n")
                 for piece in (re.split(r"(?<=[.!?])\s+", line) if len(line.split()) > 100 else [line])]
        blocks, page, buf, n = [], 1, [], 0
        for line in words:
            buf.append(line)
            n += len(line.split())
            if n >= 400:
                blocks.append(Block(doc.source, page, "\n".join(buf)))
                page, buf, n = page + 1, [], 0
        if buf:
            blocks.append(Block(doc.source, page, "\n".join(buf)))
    else:
        raise ValueError(f"Unsupported file type {suffix!r}: use .pdf, .txt, .md or .html")
    if not blocks:
        raise ValueError(f"No text could be extracted from {path.name} (scanned PDF?)")
    return CHUNKERS[design](blocks, doc)


# --------------------------------------------------------------------------- embed (cached)

class QuotaExhausted(RuntimeError):
    """The free tier's daily embedding limit is used up; run again after it resets."""


def _cache() -> sqlite3.Connection:
    INDEX_DIR.mkdir(exist_ok=True)
    con = sqlite3.connect(CACHE_PATH)
    con.execute("CREATE TABLE IF NOT EXISTS vectors (key TEXT PRIMARY KEY, dim INTEGER, vector BLOB)")
    return con


def _key(text: str) -> str:
    return hashlib.sha1(f"{EMBED_MODEL}|{EMBED_DIM}|{text}".encode()).hexdigest()


_client = None


def _gemini():
    global _client
    if _client is None:
        from google import genai
        from api_key import load_api_key
        _client = genai.Client(api_key=load_api_key())
    return _client


def _embed_batch(texts: list[str]) -> list[np.ndarray]:
    """One Gemini call; retries on per-minute limits, raises QuotaExhausted on the daily one."""
    from google.genai import errors, types

    # Each text must be its own Content: a plain list of strings is merged by the SDK
    # into ONE content with several parts, and gemini-embedding-2 then returns a single
    # aggregated vector for the whole batch.
    contents = [types.Content(parts=[types.Part(text=t)]) for t in texts]
    for attempt in range(6):
        try:
            response = _gemini().models.embed_content(
                model=EMBED_MODEL, contents=contents,
                config=types.EmbedContentConfig(output_dimensionality=EMBED_DIM))
            vectors = [np.asarray(e.values, dtype=np.float32) for e in response.embeddings]
            if len(vectors) != len(texts):
                raise RuntimeError(f"asked for {len(texts)} embeddings, got {len(vectors)}")
            # truncated Matryoshka vectors are not unit length: normalise for cosine search
            return [v / (np.linalg.norm(v) or 1.0) for v in vectors]
        except errors.APIError as error:
            message = str(error)
            if error.code == 429 and ("PerDay" in message or "per day" in message.lower()):
                raise QuotaExhausted(message) from error
            if error.code == 429 and attempt == 5:          # still limited after ~5 minutes of retries
                raise QuotaExhausted(message) from error
            if error.code in (429, 500, 503) and attempt < 5:
                wait = 20 * (attempt + 1)
                log(f"  Gemini said {error.code}; waiting {wait}s and retrying")
                time.sleep(wait)
                continue
            raise
    raise RuntimeError("unreachable")


def embed_texts(texts: list[str]) -> list[np.ndarray]:
    """Vectors for texts, from the cache where possible; new vectors are saved per batch."""
    con = _cache()
    keys = [_key(t) for t in texts]
    found: dict[str, np.ndarray] = {}
    for i in range(0, len(keys), 500):
        part = keys[i:i + 500]
        rows = con.execute(f"SELECT key, vector FROM vectors WHERE key IN ({','.join('?' * len(part))})", part)
        found.update({k: np.frombuffer(v, dtype=np.float32) for k, v in rows})
    missing = list(dict.fromkeys(k for k in keys if k not in found))
    if missing:
        by_key = dict(zip(keys, texts))
        log(f"  embedding {len(missing)} new text(s) with {EMBED_MODEL} ({len(found)} cached)")
        for i in range(0, len(missing), EMBED_BATCH):
            batch = missing[i:i + EMBED_BATCH]
            vectors = _embed_batch([by_key[k] for k in batch])
            con.executemany("INSERT OR REPLACE INTO vectors VALUES (?, ?, ?)",
                            [(k, EMBED_DIM, v.tobytes()) for k, v in zip(batch, vectors)])
            con.commit()                       # saved now: a later failure loses nothing
            found.update(zip(batch, vectors))
            log(f"    {min(i + EMBED_BATCH, len(missing))}/{len(missing)} embedded and saved")
    con.close()
    return [found[k] for k in keys]


def embed_query(query: str) -> np.ndarray:
    """Query side of the asymmetric retrieval format."""
    return embed_texts([f"task: question answering | query: {query.strip()}"])[0]


def cached_count(texts: list[str]) -> int:
    con = _cache()
    keys = [_key(t) for t in texts]
    n = sum(1 for k in keys if con.execute("SELECT 1 FROM vectors WHERE key=?", (k,)).fetchone())
    con.close()
    return n


# --------------------------------------------------------------------------- store + search

_chroma_client = None
_chroma_lock = threading.RLock()


def _chroma():
    """One ChromaDB client per process, created once under a lock.

    The MCP server runs tool calls in worker threads. When a subagent sent several
    searches at once, each one built its own PersistentClient and they collided
    (KeyError on the path, "Could not connect to tenant default_tenant").
    """
    global _chroma_client
    with _chroma_lock:
        if _chroma_client is None:
            import chromadb
            from chromadb.config import Settings
            _chroma_client = chromadb.PersistentClient(path=str(CHROMA_DIR),
                                                       settings=Settings(anonymized_telemetry=False))
        return _chroma_client


def collection(design: str = ACTIVE_DESIGN):
    with _chroma_lock:
        return _chroma().get_or_create_collection(f"food_safety_{design}", metadata={"hnsw:space": "cosine"},
                                                  embedding_function=None)


def embed_and_store(chunks: list[Chunk], design: str | None = None) -> int:
    """Embed chunks (cache first) and upsert them into the design's collection. Returns how many."""
    if not chunks:
        return 0
    design = design or chunks[0].design
    col = collection(design)
    existing = set(col.get(include=[])["ids"])
    chunks = [c for c in chunks if c.id not in existing]   # unchanged chunks stay as they are
    if not chunks:
        return 0
    vectors = embed_texts([c.embed_input() for c in chunks])
    for i in range(0, len(chunks), 200):
        part = chunks[i:i + 200]
        col.upsert(ids=[c.id for c in part], documents=[c.text for c in part],
                   embeddings=[v.tolist() for v in vectors[i:i + 200]],
                   metadatas=[c.metadata() for c in part])
    return len(chunks)


def search(query: str, k: int = 5, design: str = ACTIVE_DESIGN, source: str | None = None) -> list[dict]:
    """Top-k chunks for a query: text, metadata and cosine similarity."""
    col = collection(design)
    if col.count() == 0:
        raise RuntimeError(f"The {design!r} collection in index/ is empty. Run `uv run python main.py index`.")
    vector = embed_query(query).tolist()
    with _chroma_lock:          # queries from parallel tool calls run one at a time (each takes milliseconds)
        result = col.query(query_embeddings=[vector], n_results=k,
                           where={"source": source} if source else None,
                           include=["documents", "metadatas", "distances"])
    return [{"text": doc, **meta, "score": round(1 - dist, 4)}
            for doc, meta, dist in zip(result["documents"][0], result["metadatas"][0], result["distances"][0])]


def source_status(source: str, design: str = ACTIVE_DESIGN) -> dict:
    """What the index holds for a source: chunk count and the file hash it was built from."""
    got = collection(design).get(where={"source": source}, include=["metadatas"])
    hashes = {m.get("file_sha256", "") for m in got["metadatas"]}
    return {"chunks": len(got["ids"]), "file_sha256": next(iter(hashes), "") if len(hashes) == 1 else "", "ids": got["ids"]}


def file_sha256(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def add_file(path: str | Path, design: str = ACTIVE_DESIGN, title: str | None = None) -> dict:
    """The add-document pipeline: chunk, embed and store one file, deduplicated.

    - same file content already indexed under this source -> nothing happens;
    - same source name but different content (a new version) -> old chunks are
      replaced by the new ones, so search never mixes two versions;
    - otherwise the chunks are added.
    """
    path = Path(path).expanduser().resolve()
    digest = file_sha256(path)
    chunks = chunk_file(path, design, title=title)
    for c in chunks:
        c.origin = "added" if c.source not in {d.source for d in CORPUS} else "corpus"
    source = chunks[0].source
    status = source_status(source, design)
    if status["chunks"] and status["file_sha256"] == digest:
        return {"status": "already_indexed", "source": source, "chunks": status["chunks"]}
    col = collection(design)
    if status["ids"]:
        col.delete(ids=status["ids"])
    vectors = embed_texts([c.embed_input() for c in chunks])
    col.upsert(ids=[c.id for c in chunks], documents=[c.text for c in chunks],
               embeddings=[v.tolist() for v in vectors],
               metadatas=[{**c.metadata(), "file_sha256": digest} for c in chunks])
    return {"status": "replaced" if status["ids"] else "added", "source": source, "chunks": len(chunks),
            "pages": f"{chunks[0].page_start}-{chunks[-1].page_end}"}


def remove_source(source: str, design: str = ACTIVE_DESIGN) -> int:
    ids = source_status(source, design)["ids"]
    if ids:
        collection(design).delete(ids=ids)
    return len(ids)


# --------------------------------------------------------------------------- main

def build_chunks() -> dict[str, list[Chunk]]:
    chunks: dict[str, list[Chunk]] = {d: [] for d in DESIGNS}
    for doc in CORPUS:
        path = download(doc)
        blocks = extract_blocks(doc, path)
        words = sum(len(b.text.split()) for b in blocks)
        log(f"{doc.source}: {len(blocks)} blocks, {words:,} words")
        for design in DESIGNS:
            chunks[design] += CHUNKERS[design](blocks, doc)
    return chunks


def main() -> int:
    all_chunks = build_chunks()
    # Fill the active design first: the server needs it, the other is only for comparison.
    order = [ACTIVE_DESIGN] + [d for d in DESIGNS if d != ACTIVE_DESIGN]
    for design in order:
        chunks = all_chunks[design]
        sizes = [len(c.text.split()) for c in chunks]
        log(f"\nDesign {design!r}: {len(chunks)} chunks, {np.mean(sizes):.0f} words on average "
            f"(min {min(sizes)}, max {max(sizes)}); {cached_count([c.embed_input() for c in chunks])} already embedded")
        try:
            embed_and_store(chunks, design)
        except QuotaExhausted:
            log("\nThe Gemini free tier's daily embedding limit is used up. Everything embedded so far is "
                "saved in index/. Run `uv run python main.py index` again after the reset (09:00 in Spain).")
            return 2
        # drop corpus chunks that no longer exist (e.g. after a cleaning change); keep added documents
        col = collection(design)
        keep = {c.id for c in chunks}
        stale = [i for i, m in zip(*(lambda g: (g["ids"], g["metadatas"]))(col.get(include=["metadatas"])))
                 if m.get("origin") == "corpus" and i not in keep]
        if stale:
            col.delete(ids=stale)
            log(f"  removed {len(stale)} stale chunk(s)")
        log(f"  collection food_safety_{design}: {col.count()} chunks stored")
        (INDEX_DIR / f"chunks_{design}.jsonl").write_text(
            "\n".join(json.dumps({"id": c.id, **c.metadata(), "text": c.text}) for c in chunks), encoding="utf-8")
    size = sum(p.stat().st_size for p in INDEX_DIR.rglob("*") if p.is_file()) / 1e6
    log(f"\nindex/ is {size:.1f} MB. Commit it.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
