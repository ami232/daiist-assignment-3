"""
Assignment 3: build the index (`uv run python main.py index`).

Pipeline, one function per step so server.py's add_document can reuse it:

    download_corpus()            CORPUS URLs -> corpus/*.pdf (skips files already there)
    extract_pages(path)          PDF / txt / md / html -> list of (page_number, text)
    clean_pages(pages)           normalise, drop boilerplate and duplicated text layers
    to_units(pages)              -> sentences, each with its page and section heading
    chunk_units(units, design)   -> chunks of text + metadata (source, page, section)
    embed_and_store(chunks, ...) embeds only chunks without a saved vector, stores in index/
    index_file(path, ...)        all of the above for one file (what add_document calls)

Usage:
    uv run python index.py                  # download, chunk, embed every design
    uv run python index.py --dry-run        # chunk only, print stats, no API calls
    uv run python index.py --design structured

All logging goes to stderr, because server.py imports this module and stdout
carries the MCP protocol there.
"""

from __future__ import annotations

import argparse
import hashlib
import os
import re
import sys
import time
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"
# CORPUS_INDEX_DIR lets the before/after test in evaluate.py work on a copy of the index
CHROMA_DIR = Path(os.environ.get("CORPUS_INDEX_DIR") or INDEX_DIR / "chroma")

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768
EMBED_BATCH = 50

# ---------------------------------------------------------------------------
# Corpus. Keep a document out of this list (and in another folder) if you want
# to add it later through the add_document tool for step 8.
# ---------------------------------------------------------------------------
CORPUS = [
    {
        "title": "Attendance Policy, Bachelor Programs",
        "file": "Attendance_Policy_Bachelor_Programs.pdf",
        "url": "https://docs.ie.edu/documents/Attendance_Policy_Bachelor_Programs.pdf",
    },
    {
        "title": "Academic Regulations for Bachelor Degree Programmes",
        "file": "IEU_ACADEMIC_REGULATIONS_FOR_BACHELOR_DEGREE_PROGRAMMES.pdf",
        "url": "https://docs.ie.edu/www.ie.edu/university/IEU_ACADEMIC%20REGULATIONS%20FOR%20BACHELOR%20DEGREE%20PROGRAMMES.pdf",
    },
    {
        "title": "Academic Regulations for Master Degree Programmes",
        "file": "IEU_ACADEMIC_REGULATIONS_FOR_MASTER_DEGREE_PROGRAMMES_2025.pdf",
        "url": "https://docs.ie.edu/IEU_ACADEMIC%20REGULATIONS%20FOR%20MASTER%20%20DEGREE%20PROGRAMMES%202025.pdf",
    },
    {
        "title": "The IE Student Code of Conduct",
        "file": "The_IE_Student_Code_of_Conduct.pdf",
        "url": "https://docs.ie.edu/documents/The%20IE%20Student%20Code%20of%20Conduct.pdf",
    },
    {
        "title": "Student Guidelines on AI (v4)",
        "file": "Student_Guidelines_on_AI_v4.pdf",
        "url": "https://docs.ie.edu/Student%20Guidelines%20on%20AI_v4.pdf",
    },
    {
        "title": "Code for the Prevention of Harassment",
        "file": "Code-for-the-Prevention-of-Harassment.pdf",
        "url": "https://docs.ie.edu/sustainability/resources/Code-for-the-Prevention-of-Harassment.pdf",
    },
    {
        "title": "Equal Opportunities and Diversity Plan",
        "file": "IE-Equal-Opportunities-and-Diversity-Plan.pdf",
        "url": "https://docs.ie.edu/sustainability/resources/IE-Equal-Opportunities-and-Diversity-Plan.pdf",
    },
    {
        "title": "Environmental Policy",
        "file": "Environmental-Policy-2025.pdf",
        "url": "https://docs.ie.edu/sustainability/resources-2021/Environmental-Policy-2025.pdf",
    },
    {
        "title": "Climate and Sustainability Plan (CASP v3)",
        "file": "CASP_v3.pdf",
        "url": "https://docs.ie.edu/sustainability/resources-2021/CASP%20v3.pdf",
    },
]

# ---------------------------------------------------------------------------
# Chunking designs. Step 5 compares them; DEFAULT_DESIGN is what search uses.
#   structured: never crosses a section/article boundary, breaks at sentences.
#   fixed:      sliding window of N words over the whole document.
# ---------------------------------------------------------------------------
DESIGNS = {
    "structured": {"mode": "structured", "size": 200, "overlap": 40},
    "fixed": {"mode": "fixed", "size": 150, "overlap": 30},
}
DEFAULT_DESIGN = "structured"


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


# ---------------------------------------------------------------------------
# 1. Download
# ---------------------------------------------------------------------------
def download_corpus(docs: list[dict] = CORPUS) -> None:
    """Fetch every document into corpus/, skipping files already downloaded."""
    import httpx

    CORPUS_DIR.mkdir(exist_ok=True)
    for doc in docs:
        target = CORPUS_DIR / doc["file"]
        if target.exists() and target.stat().st_size > 0:
            continue
        log(f"downloading {doc['file']} ...")
        resp = httpx.get(doc["url"], follow_redirects=True, timeout=120)
        resp.raise_for_status()
        target.write_bytes(resp.content)


# ---------------------------------------------------------------------------
# 2. Extract
# ---------------------------------------------------------------------------
def extract_pages(path: Path) -> list[tuple[int, str]]:
    """Return (page_number, raw_text) pairs. Non-PDF files count as one page."""
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        import logging

        from pypdf import PdfReader

        logging.getLogger("pypdf").setLevel(logging.ERROR)
        reader = PdfReader(path)
        return [(i + 1, page.extract_text() or "") for i, page in enumerate(reader.pages)]
    if suffix in {".html", ".htm"}:
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(path.read_text(encoding="utf-8", errors="ignore"), "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        return [(1, soup.get_text("\n"))]
    if suffix in {".txt", ".md"}:
        return [(1, path.read_text(encoding="utf-8", errors="ignore"))]
    raise ValueError(f"Unsupported file type: {path.suffix} (use .pdf, .txt, .md or .html)")


# ---------------------------------------------------------------------------
# 3. Clean
# ---------------------------------------------------------------------------
BOILERPLATE = [
    re.compile(r"^\d{1,3}$"),  # bare page numbers
    re.compile(r"^Docusign Envelope ID:", re.I),  # e-signature stamp on every page
]


def normalise(line: str) -> str:
    # NFKC turns ligatures (ﬁ -> fi) and odd spaces into plain text.
    line = unicodedata.normalize("NFKC", line)
    return re.sub(r"\s+", " ", line).strip()


def clean_pages(pages: list[tuple[int, str]]) -> list[tuple[int, list[str]]]:
    """Normalise lines, drop boilerplate and text repeated from earlier pages.

    Some PDFs (the Harassment Code, the Equal Opportunities Plan) carry the
    text of earlier pages again on later pages, so a naive extraction repeats
    whole paragraphs up to six times. Any line of 4+ words already seen on an
    earlier page is dropped, so each passage is kept once, on its first page.
    Blank lines are kept as "" because they mark paragraph breaks.
    """
    seen: set[str] = set()
    cleaned = []
    for number, text in pages:
        lines = []
        for raw in text.splitlines():
            line = normalise(raw)
            if not line:
                lines.append("")
                continue
            if any(p.search(line) for p in BOILERPLATE):
                continue
            if len(line.split()) >= 4:
                if line in seen:
                    continue
                seen.add(line)
            lines.append(line)
        if is_table_of_contents(lines):
            continue
        cleaned.append((number, lines))
    return cleaned


# ---------------------------------------------------------------------------
# Headings. Level 0 = title/part/annex, 1 = chapter/subsection, 2 = article.
# ---------------------------------------------------------------------------
HEADING_PATTERNS = [
    (0, re.compile(r"^(?:[IVX]+\.\s+)?TITLE\s+[IVX]+\b.*", re.I)),  # "V. TITLE V: PERFORMANCE..."
    (0, re.compile(r"^ANNEX\s+[IVX\d]+\b.*", re.I)),  # "ANNEX I", "Annex II: ..."
    (0, re.compile(r"^[IVX]+\.\s+[A-Z][a-z].*")),  # "II. Ethical Standards ..." (Code of Conduct)
    (1, re.compile(r"^CHAPTER\s+\d+\b.*", re.I)),  # "CHAPTER 2: GRADING"
    (1, re.compile(r"^[IVX]+\.\d+\.\s+[A-Z]{2,}.*")),  # "II.1. ETHICAL STANDARDS: ..."
    (2, re.compile(r"^Article\s+\d+\.\s+\S.*")),  # 'Article 9. "Internships"'
]
TOC_LINE = re.compile(r"\s\d{1,3}$")  # heading followed by a page number


def match_heading(line: str) -> int | None:
    if len(line.split()) > 20:
        return None
    for level, pattern in HEADING_PATTERNS:
        if pattern.match(line):
            return level
    return None


def is_table_of_contents(lines: list[str]) -> bool:
    """A page that is mostly headings (or 'heading .... 12' lines) is an index, not content."""
    text_lines = [l for l in lines if l]
    if not text_lines:
        return False
    hits = sum(1 for l in text_lines if match_heading(l) is not None or TOC_LINE.search(l) and len(l.split()) <= 12)
    ratio = hits / len(text_lines)
    return (hits >= 6 and ratio >= 0.4) or (hits >= 4 and ratio >= 0.6)


def looks_like_plain_heading(line: str, prev: str) -> bool:
    """Short title line in documents without numbered articles."""
    words = line.split()
    return (
        1 <= len(words) <= 8
        and line[0].isupper()
        and not re.search(r"[.,;:]$", line)
        and "," not in line
        and not re.match(r"^[•\-–]", line)
        and (prev == "" or re.search(r"[.!?:;]$", prev) is not None)
    )


# ---------------------------------------------------------------------------
# 4. Units: sentences carrying page + section
# ---------------------------------------------------------------------------
@dataclass
class Unit:
    text: str
    page: int
    section: str  # full path, "TITLE V > CHAPTER 2 > Article 22. ..."
    heading: str  # most specific heading, used as the location label


BULLET = re.compile(r"^(?:[•\-–▪●]|[a-z]\)|[ivx]+\)|\d+(?:\.\d+)+\.?)\s")
SENTENCE_END = re.compile(r"(?<=[.!?;])\s+(?=[A-Z“\"(•\d])")


def join_lines(lines: list[str]) -> str:
    text = ""
    for line in lines:
        if text.endswith("-") and line[:1].islower():
            text = text[:-1] + line  # "compe-" + "tences" -> "competences"
        else:
            text = f"{text} {line}" if text else line
    return text


def to_units(pages: list[tuple[int, list[str]]]) -> list[Unit]:
    numbered = sum(1 for _, lines in pages for l in lines if match_heading(l) is not None) >= 3
    stack: list[tuple[int, str]] = []  # (level, heading)
    units: list[Unit] = []
    para: list[str] = []
    para_page = pages[0][0] if pages else 1
    plain_heading = ""  # merges consecutive plain heading lines
    open_heading = False  # last heading ended with ":" ("TITLE I:" / "GENERAL PROVISIONS")

    def section() -> tuple[str, str]:
        if not stack:
            return "", ""
        return " > ".join(h for _, h in stack), stack[-1][1]

    def flush() -> None:
        nonlocal para
        if para:
            sec, head = section()
            for sentence in SENTENCE_END.split(join_lines(para)):
                if sentence.strip():
                    units.append(Unit(sentence.strip(), para_page, sec, head))
        para = []

    def push(level: int, heading: str) -> None:
        while stack and stack[-1][0] >= level:
            stack.pop()
        stack.append((level, heading))

    for number, lines in pages:
        prev = ""
        for line in lines:
            if not line:
                flush()
                prev, plain_heading = "", ""
                continue
            level = match_heading(line)
            if open_heading and level is None and len(line.split()) <= 10:
                stack[-1] = (stack[-1][0], f"{stack[-1][1]} {line}")
                open_heading = False
                prev = line
                continue
            open_heading = False
            if level is not None:
                flush()
                push(level, line)
                plain_heading = ""
                open_heading = line.endswith(":")
            elif not numbered and (plain_heading or looks_like_plain_heading(line, prev)) and looks_like_plain_heading(line, ""):
                flush()
                plain_heading = f"{plain_heading} {line}".strip() if plain_heading else line
                stack[:] = [(0, plain_heading)]
            else:
                plain_heading = ""
                if BULLET.match(line):
                    flush()
                if not para:
                    para_page = number
                para.append(line)
            prev = line
        # paragraphs may run across a page break; keep them, labelled with the start page
    flush()
    return units


# ---------------------------------------------------------------------------
# 5. Chunk
# ---------------------------------------------------------------------------
@dataclass
class Chunk:
    text: str
    meta: dict = field(default_factory=dict)
    id: str = ""


def _make_chunk(doc: dict, design: str, units: list[Unit], index: int) -> Chunk:
    pages = sorted({u.page for u in units})
    first, last = pages[0], pages[-1]
    page_label = f"p. {first}" if first == last else f"pp. {first}-{last}"
    heading = units[0].heading
    text = " ".join(u.text for u in units)
    meta = {
        "source": doc["title"],
        "file": doc["file"],
        "url": doc.get("url", ""),
        "page_start": first,
        "page_end": last,
        "section": units[0].section,
        "heading": heading,
        "location": f"{page_label}, {heading}" if heading else page_label,
        "design": design,
        "chunk_index": index,
    }
    digest = hashlib.sha1(f"{doc['title']}|{design}|{text}".encode()).hexdigest()[:16]
    return Chunk(text=text, meta=meta, id=f"{design}-{digest}")


def _split_long(units: list[Unit], size: int) -> list[Unit]:
    """Break sentences longer than a chunk (lists without full stops) into pieces."""
    out = []
    for u in units:
        words = u.text.split()
        if len(words) <= size:
            out.append(u)
            continue
        for i in range(0, len(words), size):
            out.append(Unit(" ".join(words[i : i + size]), u.page, u.section, u.heading))
    return out


def chunk_units(units: list[Unit], doc: dict, design: str = DEFAULT_DESIGN) -> list[Chunk]:
    cfg = DESIGNS[design]
    size, overlap = cfg["size"], cfg["overlap"]
    chunks: list[Chunk] = []

    if cfg["mode"] == "fixed":
        words = [(w, u) for u in units for w in u.text.split()]
        step = size - overlap
        for start in range(0, max(len(words) - overlap, 1), step):
            window = words[start : start + size]
            # one pseudo-unit per window keeps page range and starting section
            first_unit = window[0][1]
            pieces = [Unit(" ".join(w for w, _ in window), first_unit.page, first_unit.section, first_unit.heading)]
            last_page = window[-1][1].page
            if last_page != first_unit.page:
                pieces.append(Unit("", last_page, first_unit.section, first_unit.heading))
            chunk = _make_chunk(doc, design, pieces, len(chunks))
            chunk.text = chunk.text.strip()
            chunks.append(chunk)
        return chunks

    # structured: group consecutive units by section, pack sentences, never cross a section
    groups: list[list[Unit]] = []
    for u in _split_long(units, size):
        if groups and groups[-1][0].section == u.section:
            groups[-1].append(u)
        else:
            groups.append([u])

    packed: list[list[Unit]] = []
    carry: list[Unit] = []  # sections too short to stand alone join the next one
    for group in groups:
        group = carry + group
        carry = []
        if sum(len(u.text.split()) for u in group) < 30 and group is not groups[-1]:
            carry = group
            continue
        current: list[Unit] = []
        count = 0
        for u in group:
            n = len(u.text.split())
            if current and count + n > size:
                packed.append(current)
                tail: list[Unit] = []
                tail_words = 0
                for prev in reversed(current):
                    w = len(prev.text.split())
                    if tail_words + w > overlap:
                        break
                    tail.insert(0, prev)
                    tail_words += w
                current, count = tail, tail_words
            current.append(u)
            count += n
        if current:
            packed.append(current)
    if carry:
        packed.append(carry)

    # a fragment under 15 words (e.g. a closing date line) is merged into the chunk before it
    merged: list[list[Unit]] = []
    for units_ in packed:
        if merged and sum(len(u.text.split()) for u in units_) < 15:
            merged[-1] = merged[-1] + units_
        else:
            merged.append(units_)
    return [_make_chunk(doc, design, units_, i) for i, units_ in enumerate(merged)]


def chunk_file(path: Path, doc: dict | None = None, design: str = DEFAULT_DESIGN) -> list[Chunk]:
    """Extract, clean and chunk one file. `doc` gives title/url; defaults to the file name."""
    path = Path(path)
    doc = doc or {"title": path.stem.replace("_", " ").replace("-", " "), "file": path.name, "url": ""}
    pages = clean_pages(extract_pages(path))
    chunks, seen = [], set()
    for chunk in chunk_units(to_units(pages), doc, design):
        if chunk.id not in seen:  # identical text twice in one document: keep the first
            seen.add(chunk.id)
            chunks.append(chunk)
    return chunks


# ---------------------------------------------------------------------------
# 6. Embed and store
# ---------------------------------------------------------------------------
_client = None


def genai_client():
    global _client
    if _client is None:
        from google import genai

        sys.path.insert(0, str(ROOT))
        from api_key import load_api_key

        _client = genai.Client(api_key=load_api_key())
    return _client


def embed_texts(texts: list[str], task_type: str = "RETRIEVAL_DOCUMENT") -> list[list[float]]:
    """Embed a batch with Gemini, retrying on per-minute rate limits."""
    from google.genai import errors, types

    config = types.EmbedContentConfig(task_type=task_type, output_dimensionality=EMBED_DIM)
    # gemini-embedding-2 is multimodal: a plain list of strings is read as the parts of ONE
    # input and returns a single vector. Each text must be its own Content.
    contents = [types.Content(parts=[types.Part(text=t)]) for t in texts]
    for attempt in range(6):
        try:
            resp = genai_client().models.embed_content(model=EMBED_MODEL, contents=contents, config=config)
            vectors = [e.values for e in resp.embeddings]
            if len(vectors) != len(texts):
                raise RuntimeError(f"Asked for {len(texts)} embeddings, got {len(vectors)}.")
            return vectors
        except errors.ClientError as exc:
            if exc.code != 429:
                raise
            if "PerDay" in str(exc) or "per day" in str(exc).lower():
                raise DailyQuotaExceeded(str(exc)) from exc
            wait = 15 * (attempt + 1)
            log(f"rate limited, waiting {wait}s ...")
            time.sleep(wait)
    raise RuntimeError("Gemini kept rate-limiting; try again later.")


def embed_query(query: str) -> list[float]:
    return embed_texts([query], task_type="RETRIEVAL_QUERY")[0]


class DailyQuotaExceeded(RuntimeError):
    pass


def get_collection(design: str = DEFAULT_DESIGN):
    """The ChromaDB collection holding one design's chunks and vectors."""
    import chromadb
    from chromadb.config import Settings

    client = chromadb.PersistentClient(path=str(CHROMA_DIR), settings=Settings(anonymized_telemetry=False))
    return client.get_or_create_collection(name=f"chunks_{design}", metadata={"hnsw:space": "cosine"})


def embedding_input(chunk: Chunk) -> str:
    """What gets embedded: the text plus its document and section, which often name the topic."""
    header = chunk.meta["source"]
    if chunk.meta["section"]:
        header += f" | {chunk.meta['section']}"
    return f"{header}\n\n{chunk.text}"


def embed_and_store(chunks: list[Chunk], design: str = DEFAULT_DESIGN, source: str | None = None) -> dict:
    """Store chunks, embedding only those without a saved vector.

    Chunk ids hash the text, so an unchanged document costs no embeddings.
    If `source` is given, that document's stale chunks (from an older version
    of the file) are deleted, so re-adding a changed document replaces it.
    """
    collection = get_collection(design)
    ids = [c.id for c in chunks]
    existing = set(collection.get(ids=ids, include=[])["ids"]) if ids else set()
    todo = [c for c in chunks if c.id not in existing]

    stale = []
    if source:
        old = collection.get(where={"source": source}, include=[])["ids"]
        stale = [i for i in old if i not in set(ids)]
        if stale:
            collection.delete(ids=stale)

    for start in range(0, len(todo), EMBED_BATCH):
        batch = todo[start : start + EMBED_BATCH]
        vectors = embed_texts([embedding_input(c) for c in batch])
        # saved immediately, so a crash or the daily limit loses nothing
        collection.add(
            ids=[c.id for c in batch],
            documents=[c.text for c in batch],
            metadatas=[c.meta for c in batch],
            embeddings=vectors,
        )
        log(f"  [{design}] embedded {min(start + EMBED_BATCH, len(todo))}/{len(todo)}")

    return {"chunks": len(chunks), "already_indexed": len(existing), "embedded": len(todo), "removed_stale": len(stale)}


def index_file(path: Path, doc: dict | None = None, designs: list[str] | None = None) -> dict:
    """Run one file through the whole pipeline for each design. Used by add_document."""
    path = Path(path)
    doc = doc or {"title": path.stem.replace("_", " ").replace("-", " "), "file": path.name, "url": ""}
    report = {}
    for design in designs or [DEFAULT_DESIGN]:
        chunks = chunk_file(path, doc, design)
        if not chunks:
            raise ValueError(f"No text could be extracted from {path.name}.")
        report[design] = embed_and_store(chunks, design, source=doc["title"])
    return report


# ---------------------------------------------------------------------------
# main
# ---------------------------------------------------------------------------
def main() -> None:
    parser = argparse.ArgumentParser(description="Build the index in index/.")
    parser.add_argument("--design", choices=list(DESIGNS), help="only this design (default: all)")
    parser.add_argument("--dry-run", action="store_true", help="chunk and report; no embeddings")
    parser.add_argument("--show", type=int, default=0, help="with --dry-run, print N sample chunks per document")
    args = parser.parse_args()
    designs = [args.design] if args.design else list(DESIGNS)

    download_corpus()
    INDEX_DIR.mkdir(exist_ok=True)

    for design in designs:
        log(f"\n=== design: {design} {DESIGNS[design]}")
        total_chunks = total_words = 0
        for doc in CORPUS:
            chunks = chunk_file(CORPUS_DIR / doc["file"], doc, design)
            words = sum(len(c.text.split()) for c in chunks)
            total_chunks += len(chunks)
            total_words += words
            if args.dry_run:
                log(f"{doc['title'][:55]:55} {len(chunks):4} chunks {words:6} words")
                for c in chunks[: args.show]:
                    log(f"    [{c.meta['location']}] {c.text[:160]}...")
                continue
            try:
                result = embed_and_store(chunks, design, source=doc["title"])
            except DailyQuotaExceeded:
                log("\nDaily embedding quota reached. Vectors so far are saved; run again after the reset.")
                sys.exit(1)
            log(f"{doc['title'][:55]:55} {result}")
        log(f"total: {total_chunks} chunks, {total_words} words (incl. overlap)")
        if not args.dry_run:
            log(f"collection chunks_{design}: {get_collection(design).count()} chunks stored")


if __name__ == "__main__":
    main()
