"""
Assignment 3: build the index (`main.py index`).

Corpus: EASA "Easy Access Rules for Unmanned Aircraft Systems" (revision June
2026, machine-readable XML), which consolidates every amendment to the EU drone
rules. We split it into three documents and leave out the SORA risk-assessment
method (AMC/GM to Article 11), which is out of scope for hobby and freelance
pilots:

    reg-2019-947   Commission Implementing Regulation (EU) 2019/947 (consolidated)
    reg-2019-945   Commission Delegated Regulation (EU) 2019/945 (consolidated)
    easa-amc-gm    EASA AMC & GM to Regulation (EU) 2019/947 (without SORA)

Every chunk carries `source` (one of the ids above, or a file name for added
documents) and `location` (the rule's own heading, e.g. "UAS.OPEN.020
Operations in subcategory A1", or "p. 4" for PDFs).

Two chunking designs are stored as separate Chroma collections in index/:

    section   one chunk per rule/AMC/GM topic; long topics split at paragraph
              boundaries, every piece prefixed with its heading
    fixed     250-word sliding windows (50-word overlap) over each document,
              ignoring structure (baseline)

Vectors are written batch by batch and chunk ids are content hashes, so a
re-run (or a run after hitting the daily quota) only embeds what is missing.

server.py imports `chunk_file` and `embed_and_store` from here.
"""

from __future__ import annotations

import hashlib
import io
import re
import sys
import time
import xml.etree.ElementTree as ET
import zipfile
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"

EASA_URL = "https://www.easa.europa.eu/en/downloads/137111/en"
EASA_ZIP = CORPUS_DIR / "easa-uas-easy-access-rules-2026-06.zip"

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768
EMBED_BATCH = 50

DESIGNS = ("section", "fixed")
SECTION_MAX_WORDS = 350     # a topic longer than this is split...
SECTION_TARGET_WORDS = 250  # ...into pieces of about this size
FIXED_WINDOW, FIXED_OVERLAP = 250, 50

DOCS = {
    "reg-2019-947": "Commission Implementing Regulation (EU) 2019/947 (consolidated, EASA Easy Access Rules June 2026)",
    "reg-2019-945": "Commission Delegated Regulation (EU) 2019/945 (consolidated, EASA Easy Access Rules June 2026)",
    "easa-amc-gm": "EASA Acceptable Means of Compliance and Guidance Material to Regulation (EU) 2019/947 (June 2026, SORA excluded)",
}

W = "{http://schemas.openxmlformats.org/wordprocessingml/2006/main}"
ER = "{http://www.easa.europa.eu/erules-export}"


def log(*args) -> None:
    """Log to stderr: server.py imports this module and stdout carries MCP."""
    print(*args, file=sys.stderr, flush=True)


@dataclass
class Section:
    source: str            # document id
    location: str          # heading of the rule / page / HTML section
    paragraphs: list[str]
    meta: dict = field(default_factory=dict)

    @property
    def words(self) -> int:
        return sum(len(p.split()) for p in self.paragraphs)


@dataclass
class Chunk:
    id: str
    text: str
    metadata: dict


# --------------------------------------------------------------------------
# Download
# --------------------------------------------------------------------------

def download_corpus() -> Path:
    if EASA_ZIP.is_file():
        return EASA_ZIP
    import httpx

    CORPUS_DIR.mkdir(exist_ok=True)
    log(f"Downloading {EASA_URL} ...")
    response = httpx.get(EASA_URL, follow_redirects=True, timeout=120, headers={"User-Agent": "Mozilla/5.0"})
    response.raise_for_status()
    if not response.content.startswith(b"PK"):
        raise RuntimeError(f"Expected a zip from {EASA_URL}, got {response.headers.get('content-type')}")
    EASA_ZIP.write_bytes(response.content)
    return EASA_ZIP


# --------------------------------------------------------------------------
# Extraction and cleaning
# --------------------------------------------------------------------------

def clean(text: str) -> str:
    text = text.replace("\xa0", " ").replace("‑", "-").replace("­", "")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def _paragraph_text(p: ET.Element) -> str:
    parts = []
    for el in p.iter():
        if el.tag == W + "t" and el.text:
            parts.append(el.text)
        elif el.tag in (W + "tab", W + "br"):
            parts.append(" ")
    return clean("".join(parts))


def _blocks(el: ET.Element) -> list[str]:
    """Paragraphs in reading order; a table row becomes one 'a | b | c' line.

    Without this, table cells came out as one word stream with no row or
    column boundaries (e.g. the class-marking tables in 2019/945).
    """
    out: list[str] = []
    for child in el:
        if child.tag == W + "p":
            text = _paragraph_text(child)
            if text:
                out.append(text)
        elif child.tag == W + "tbl":
            for row in child.iter(W + "tr"):
                cells = [" ".join(_blocks(cell)) for cell in row.findall(W + "tc")]
                cells = [c for c in cells if c]
                if cells:
                    out.append(" | ".join(cells))
        else:
            out.extend(_blocks(child))
    return out


def _doc_for(content_type: str, title: str) -> str | None:
    """Which of our three documents a topic belongs to, or None to skip it."""
    if content_type.startswith("IR"):
        return "reg-2019-947"
    if content_type.startswith("DR"):
        return "reg-2019-945"
    if content_type.startswith(("AMC", "GM")):
        if re.search(r"\bArticle 11\b", title):  # SORA: out of scope
            return None
        return "easa-amc-gm"
    return None  # front matter: disclaimer, revision list, editor's note


def sections_from_easa_xml(data: bytes) -> list[Section]:
    root = ET.parse(io.BytesIO(data)).getroot()
    toc = {t.get("sdt-id"): t for t in root.iter(ER + "topic")}
    sections, seen = [], set()
    for sdt in root.iter(W + "sdt"):
        props = sdt.find(W + "sdtPr")
        sdt_id = props.find(W + "id") if props is not None else None
        topic = toc.get(sdt_id.get(W + "val")) if sdt_id is not None else None
        if topic is None:
            continue
        title = clean(topic.get("source-title") or "")
        content_type = topic.get("TypeOfContent") or ""
        source = _doc_for(content_type, title)
        content = sdt.find(W + "sdtContent")
        if source is None or content is None:
            continue
        paragraphs = _blocks(content)
        if paragraphs and clean(paragraphs[0]) == title:
            paragraphs = paragraphs[1:]  # heading repeated as first paragraph
        legal_source = clean(topic.get("RegulatorySource") or "")
        while paragraphs and (paragraphs[0] == legal_source or re.fullmatch(
                r"(Regulation \(EU\) ?\d{4}/\d+|ED Decision \d{4}/\d+/R)( ?;.*)?", paragraphs[0])):
            paragraphs = paragraphs[1:]  # EASA's amendment marker: kept as metadata, not text
        body = "\n".join(paragraphs)
        digest = hashlib.sha1(f"{title}\n{body}".encode()).hexdigest()
        if not paragraphs or digest in seen:  # the XML repeats some SORA-annex topics verbatim
            continue
        seen.add(digest)
        sections.append(Section(
            source=source,
            location=title,
            paragraphs=paragraphs,
            meta={
                "type": content_type.split("(")[0].strip(" ;"),
                "legal_source": clean(topic.get("RegulatorySource") or ""),
                "parent_rule": clean(topic.get("ParentIR") or ""),
                "doc_title": DOCS[source],
            },
        ))
    return sections


def sections_from_pdf(path: Path, source: str) -> list[Section]:
    from pypdf import PdfReader

    sections = []
    for number, page in enumerate(PdfReader(path).pages, start=1):
        lines = [clean(line) for line in (page.extract_text() or "").splitlines()]
        # Re-join lines broken mid-sentence; keep blank-ish lines as paragraph breaks.
        paragraphs, current = [], []
        for line in lines:
            if not line:
                if current:
                    paragraphs.append(" ".join(current))
                    current = []
                continue
            current.append(line)
            if line.endswith((".", ":", ";")):
                paragraphs.append(" ".join(current))
                current = []
        if current:
            paragraphs.append(" ".join(current))
        paragraphs = [p.replace("- ", "") if p.endswith("-") else p for p in paragraphs if p]
        if paragraphs:
            sections.append(Section(source, f"p. {number}", paragraphs, {"type": "PDF", "doc_title": path.name}))
    return sections


def sections_from_html(data: bytes, source: str, name: str) -> list[Section]:
    """Split at headings. EUR-Lex/Publications Office acts use 'Article N' titles."""
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(data, "html.parser")
    for tag in soup(["script", "style", "nav", "header", "footer"]):
        tag.decompose()
    sections: list[Section] = []
    location, paragraphs = "Preamble", []

    def flush():
        if paragraphs:
            sections.append(Section(source, location, list(paragraphs), {"type": "HTML", "doc_title": name}))
            paragraphs.clear()

    for el in soup.find_all(["h1", "h2", "h3", "h4", "p", "li", "tr"]):
        if el.find_parent(["li", "tr"]) and el.name in ("p", "li"):
            continue  # already taken as part of its list item / table row
        if el.name == "tr":
            text = " | ".join(clean(td.get_text(" ")) for td in el.find_all(["td", "th"]))
        else:
            text = clean(el.get_text(" "))
        if not text:
            continue
        classes = set(el.get("class", []))
        if classes & {"oj-sti-art", "sti-art"}:  # article subtitle (check first: its class contains "ti-art")
            if not paragraphs:
                location = f"{location} - {text}"[:160]
            continue
        heading = el.name.startswith("h") or bool(classes & {"oj-ti-art", "ti-art", "oj-ti-section-1", "ti-section-1"})
        if heading or re.fullmatch(r"(Article \d+[a-z]?|ANNEX [IVX]+|PART [A-Z0-9]+)", text):
            flush()
            location = text[:120]
        else:
            paragraphs.append(text)
    flush()
    return sections


def sections_from_text(path: Path, source: str) -> list[Section]:
    text = path.read_text(encoding="utf-8", errors="replace")
    sections: list[Section] = []
    location, paragraphs = "Start", []
    for block in re.split(r"\n\s*\n", text):
        block = clean(block)
        if not block:
            continue
        if block.startswith("#"):
            if paragraphs:
                sections.append(Section(source, location, paragraphs, {"type": "text", "doc_title": path.name}))
            location, paragraphs = block.lstrip("# ")[:120], []
        else:
            paragraphs.append(block)
    if paragraphs:
        sections.append(Section(source, location, paragraphs, {"type": "text", "doc_title": path.name}))
    return sections


def source_id_for(path: Path) -> str:
    return re.sub(r"[^a-z0-9]+", "-", path.stem.lower()).strip("-")


def sections_from_file(path: Path) -> list[Section]:
    """Extract sections from any supported file (the add-document entry point)."""
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix == ".zip":
        with zipfile.ZipFile(path) as zf:
            name = next(n for n in zf.namelist() if n.lower().endswith(".xml"))
            return sections_from_easa_xml(zf.read(name))
    source = source_id_for(path)
    if suffix == ".xml":
        data = path.read_bytes()
        if b"erules-export" in data[:5000]:
            return sections_from_easa_xml(data)
        return sections_from_html(data, source, path.name)
    if suffix == ".pdf":
        return sections_from_pdf(path, source)
    if suffix in (".html", ".htm", ".xhtml"):
        return sections_from_html(path.read_bytes(), source, path.name)
    if suffix in (".txt", ".md"):
        return sections_from_text(path, source)
    raise ValueError(f"Unsupported file type {suffix!r}: use .pdf, .html, .xml, .txt, .md or an EASA eRules .zip")


# --------------------------------------------------------------------------
# Chunking
# --------------------------------------------------------------------------

def _chunk_id(design: str, source: str, location: str, text: str) -> str:
    return f"{design}-" + hashlib.sha1(f"{source}|{location}|{text}".encode()).hexdigest()[:20]


def _split_paragraphs(paragraphs: list[str], target: int) -> list[list[str]]:
    """Greedy split at paragraph boundaries; an over-long paragraph is split by sentences."""
    units: list[str] = []
    for p in paragraphs:
        if len(p.split()) <= target:
            units.append(p)
        else:
            sentence, buf = re.split(r"(?<=[.;:])\s+", p), []
            for s in sentence:
                if buf and len(" ".join(buf + [s]).split()) > target:
                    units.append(" ".join(buf))
                    buf = []
                buf.append(s)
            if buf:
                units.append(" ".join(buf))
    pieces, current, words = [], [], 0
    for unit in units:
        n = len(unit.split())
        if current and words + n > target:
            pieces.append(current)
            current, words = [], 0
        current.append(unit)
        words += n
    if current:
        pieces.append(current)
    return pieces


def chunk_sections(sections: list[Section], design: str = "section") -> list[Chunk]:
    chunks: list[Chunk] = []
    if design == "section":
        for sec in sections:
            pieces = [sec.paragraphs] if sec.words <= SECTION_MAX_WORDS else _split_paragraphs(sec.paragraphs, SECTION_TARGET_WORDS)
            for i, piece in enumerate(pieces, start=1):
                part = f" (part {i}/{len(pieces)})" if len(pieces) > 1 else ""
                text = f"{sec.location}{part}\n" + "\n".join(piece)
                meta = {**sec.meta, "source": sec.source, "location": sec.location, "locations": sec.location,
                        "part": i, "parts": len(pieces), "words": len(text.split())}
                chunks.append(Chunk(_chunk_id(design, sec.source, sec.location, text), text, meta))
    elif design == "fixed":
        by_source: dict[str, list[tuple[str, Section]]] = {}
        for sec in sections:  # one word stream per document, remembering each word's section
            by_source.setdefault(sec.source, []).extend((w, sec) for p in [sec.location, *sec.paragraphs] for w in p.split())
        for source, words in by_source.items():
            step = FIXED_WINDOW - FIXED_OVERLAP
            for start in range(0, max(len(words) - FIXED_OVERLAP, 1), step):
                window = words[start:start + FIXED_WINDOW]
                text = " ".join(w for w, _ in window)
                secs = list({id(s): s for _, s in window}.values())
                meta = {**secs[0].meta, "source": source, "location": secs[0].location,
                        "locations": " || ".join(s.location for s in secs), "words": len(window)}
                chunks.append(Chunk(_chunk_id(design, source, str(start), text), text, meta))
    else:
        raise ValueError(f"Unknown design {design!r}")
    return chunks


def chunk_file(path: Path, design: str = "section") -> list[Chunk]:
    """Extract, clean and chunk one file. Used by server.py's add_document."""
    return chunk_sections(sections_from_file(Path(path)), design)


# --------------------------------------------------------------------------
# Embedding and storage
# --------------------------------------------------------------------------

_client = None


def genai_client():
    global _client
    if _client is None:
        from google import genai
        from api_key import load_api_key
        _client = genai.Client(api_key=load_api_key())
    return _client


class QuotaExhausted(RuntimeError):
    pass


def embed_texts(texts: list[str], task_type: str, titles: list[str] | None = None) -> list[list[float]]:
    """Embed with retries on per-minute limits; raise QuotaExhausted on the daily one."""
    from google.genai import types, errors

    delay = 20
    for attempt in range(6):
        try:
            # gemini-embedding-2 is multimodal: a plain list of strings is read as the parts of
            # ONE input and comes back as a single vector. One Content per text = one vector each.
            result = genai_client().models.embed_content(
                model=EMBED_MODEL,
                contents=[types.Content(parts=[types.Part(text=t)]) for t in texts],
                config=types.EmbedContentConfig(task_type=task_type, output_dimensionality=EMBED_DIM),
            )
            vectors = [e.values for e in result.embeddings]
            if len(vectors) != len(texts):
                raise RuntimeError(f"Asked for {len(texts)} embeddings, got {len(vectors)}")
            return vectors
        except errors.APIError as error:
            message = str(error)
            if error.code == 429 and ("PerDay" in message or "per day" in message.lower()):
                raise QuotaExhausted(message) from error
            if error.code in (429, 500, 503) and attempt < 5:
                log(f"  embedding API said {error.code}; retrying in {delay}s")
                time.sleep(delay)
                delay *= 2
                continue
            raise
    raise RuntimeError("unreachable")


def get_collection(design: str = "section"):
    import chromadb

    INDEX_DIR.mkdir(exist_ok=True)
    client = chromadb.PersistentClient(path=str(INDEX_DIR))
    return client.get_or_create_collection(name=design, metadata={"hnsw:space": "cosine"}, embedding_function=None)


def embed_and_store(chunks: list[Chunk], design: str = "section") -> int:
    """Embed the chunks that have no stored vector yet and store them. Returns how many were embedded."""
    collection = get_collection(design)
    existing = set()
    ids = [c.id for c in chunks]
    for i in range(0, len(ids), 500):
        existing.update(collection.get(ids=ids[i:i + 500], include=[])["ids"])
    todo = [c for c in chunks if c.id not in existing]
    if not todo:
        return 0
    done = 0
    for i in range(0, len(todo), EMBED_BATCH):
        batch = todo[i:i + EMBED_BATCH]
        vectors = embed_texts([c.text for c in batch], "RETRIEVAL_DOCUMENT")
        collection.add(ids=[c.id for c in batch], documents=[c.text for c in batch],
                       metadatas=[c.metadata for c in batch], embeddings=vectors)
        done += len(batch)
        log(f"  [{design}] embedded {done}/{len(todo)}")
    return done


def remove_stale(chunks: list[Chunk], design: str, sources: set[str]) -> int:
    """Delete stored chunks of these sources that the current chunking no longer produces."""
    collection = get_collection(design)
    keep = {c.id for c in chunks}
    stale = []
    for source in sources:
        stale += [i for i in collection.get(where={"source": source}, include=[])["ids"] if i not in keep]
    if stale:
        collection.delete(ids=stale)
    return len(stale)


def main() -> None:
    archive = download_corpus()
    sections = sections_from_file(archive)
    for source in DOCS:
        secs = [s for s in sections if s.source == source]
        log(f"{source}: {len(secs)} sections, {sum(s.words for s in secs):,} words")
    log(f"total: {sum(s.words for s in sections):,} words")

    for design in DESIGNS:
        chunks = chunk_sections(sections, design)
        removed = remove_stale(chunks, design, set(DOCS))
        sizes = sorted(c.metadata["words"] for c in chunks)
        log(f"[{design}] {len(chunks)} chunks (median {sizes[len(sizes)//2]} words, max {sizes[-1]}); removed {removed} stale")
        try:
            embedded = embed_and_store(chunks, design)
        except QuotaExhausted:
            log("Daily embedding quota reached. Vectors so far are saved; run `main.py index` again after the reset (09:00 Spain).")
            sys.exit(1)
        log(f"[{design}] embedded {embedded} new chunks; collection now holds {get_collection(design).count()}")


if __name__ == "__main__":
    main()
