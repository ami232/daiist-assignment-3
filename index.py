"""
Assignment 3: build the index (`main.py index`).

Pipeline, one function per step so server.py's add_document can reuse them:

    download_corpus()          fetch the IEA PDFs into corpus/ (git-ignored)
    extract_paragraphs(path)   PDF -> clean paragraphs with page/chapter/heading
    chunk_paragraphs(paras)    paragraphs -> chunks with source + location metadata
    chunk_file(path)           the two steps above for one file
    embed_and_store(chunks)    embed with Gemini (only missing vectors), store in index/
    build_index()              all of the above for every document and design

Preview the chunking without spending any embeddings:

    uv run python index.py --preview
"""

from __future__ import annotations

import argparse
import json
import re
import statistics
import sys
from collections import Counter
from dataclasses import dataclass, asdict, field
from pathlib import Path

import httpx
import pymupdf

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"

# --------------------------------------------------------------------------
# Corpus definition
# --------------------------------------------------------------------------
# iea.org sits behind a Cloudflare bot check; the same files are served
# directly from IEA's own blob storage, which accepts scripted downloads.
BLOB = "https://iea.blob.core.windows.net/assets"


@dataclass
class Source:
    doc_id: str
    title: str
    year: int
    url: str
    file: str
    pages: list[tuple[int, int]] | None = None  # PDF page ranges to keep, 1-based, inclusive
    publisher: str = "IEA"
    licence: str = "CC BY 4.0"


SOURCES = [
    Source(
        doc_id="GEVO2026",
        title="Global EV Outlook 2026",
        year=2026,
        url=f"{BLOB}/857aa690-2a43-453f-9f12-147cc8f0a1dd/GlobalEVOutlook2026.pdf",
        file="GlobalEVOutlook2026.pdf",
        # Executive summary + ch.1 car markets + ch.2 prices, ch.5 batteries, ch.9 outlook
        pages=[(10, 68), (92, 103), (190, 236)],
    ),
    Source(
        doc_id="GEVO2025",
        title="Global EV Outlook 2025",
        year=2025,
        url=f"{BLOB}/7ea38b60-3033-42a6-9589-71134f4229f4/GlobalEVOutlook2025.pdf",
        file="GlobalEVOutlook2025.pdf",
        # Executive summary + ch.1 car markets + ch.2 car industry
        pages=[(10, 56)],
    ),
    Source(
        doc_id="GCMO2026",
        title="Global Critical Minerals Outlook 2026",
        year=2026,
        url=f"{BLOB}/19c60aa0-ee07-4a20-a138-33c967ac5008/GlobalCriticalMineralsOutlook2026.pdf",
        file="GlobalCriticalMineralsOutlook2026.pdf",
        # Executive summary + outlooks for lithium, nickel, cobalt, graphite
        pages=[(5, 13), (138, 173)],
    ),
]

# Not indexed by `main.py index`: held out for the add_document demo.
EXTRA_SOURCES = [
    Source(
        doc_id="ECMU2026",
        title="Electric Car Markets in a Time of Uncertainty",
        year=2026,
        url=f"{BLOB}/a096b500-9d47-411d-a5db-b297a5d95927/ElectricCarMarketsinaTimeofUncertainty.pdf",
        file="ElectricCarMarketsinaTimeofUncertainty.pdf",
    ),
]


def download_corpus(sources: list[Source] = SOURCES + EXTRA_SOURCES) -> None:
    """Download each PDF into corpus/ unless it is already there."""
    CORPUS_DIR.mkdir(exist_ok=True)
    for src in sources:
        dest = CORPUS_DIR / src.file
        if dest.exists() and dest.stat().st_size > 0:
            continue
        print(f"Downloading {src.file} ...", file=sys.stderr)
        with httpx.stream("GET", src.url, follow_redirects=True, timeout=120,
                          headers={"User-Agent": "Mozilla/5.0"}) as r:
            r.raise_for_status()
            tmp = dest.with_suffix(".part")
            with tmp.open("wb") as f:
                for block in r.iter_bytes():
                    f.write(block)
            tmp.rename(dest)


def source_for(path: Path) -> Source:
    """Metadata for a file: a known source, or a default one for new documents."""
    for src in SOURCES + EXTRA_SOURCES:
        if Path(src.file).name == path.name:
            return src
    with pymupdf.open(path) as doc:
        meta = doc.metadata or {}
    title = meta.get("title") or path.stem
    year = re.search(r"(20\d\d)", f"{path.stem} {title} {meta.get('creationDate', '')[2:6]}")
    return Source(
        doc_id=re.sub(r"[^A-Za-z0-9]+", "", path.stem)[:40] or "doc",
        title=title,
        year=int(year.group(1)) if year else 0,
        url="",
        file=path.name,
        publisher="unknown",
        licence="unknown",
    )


# --------------------------------------------------------------------------
# Extraction and cleaning
# --------------------------------------------------------------------------
# IEA PDFs use font size to separate content from noise:
#   body text ~11 pt; headings 14-26 pt;
#   running headers/footers, chart labels, figure notes and footnotes <= ~9 pt.
# So: find each document's body size, keep blocks at that size (+/- tolerance)
# and headings, drop the rest.
BODY_TOLERANCE = 0.3
HEADING_MIN_SIZE = 13.5
KEEP_NOTES = False  # keep "Note:"/"Source:" lines under figures and footnotes?

_NOISE_RE = re.compile(r"^(IEA\.?\s*CC BY 4\.0\.?|P\s*AGE\s*\|\s*\d+)$")
_NOTE_RE = re.compile(r"^(Notes?|Sources?)\s*:")
_FOOTNOTE_RE = re.compile(r"^\d{1,3}\s+[A-Z]")


@dataclass
class Paragraph:
    text: str
    page: int
    chapter: str
    heading: str
    is_heading: bool = False
    page_end: int = 0

    def __post_init__(self):
        self.page_end = self.page_end or self.page


def _clean_text(text: str) -> str:
    text = (text.replace("‑", "-").replace(" ", " ").replace("­", "")
                .replace("ﬁ", "fi").replace("ﬂ", "fl"))
    text = re.sub(r"-\s+(?=[a-z])", "-", text)  # "plug-  in" -> "plug-in"
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s+([,.;:%)])", r"\1", text)  # "Outlook ." -> "Outlook."
    return text.strip()


def _body_size(doc: pymupdf.Document, pages: list[int]) -> float:
    """Most common font size by characters: the document's body text size."""
    sizes = Counter()
    for pno in pages:
        for b in doc[pno].get_text("dict")["blocks"]:
            for line in b.get("lines", []):
                for s in line["spans"]:
                    sizes[round(s["size"], 1)] += len(s["text"].strip())
    return sizes.most_common(1)[0][0]


def _page_numbers(doc: pymupdf.Document, ranges: list[tuple[int, int]] | None) -> list[int]:
    if not ranges:
        return list(range(doc.page_count))
    return [p - 1 for a, b in ranges for p in range(a, b + 1) if p <= doc.page_count]


def _chapter_lookup(doc: pymupdf.Document) -> dict[int, str]:
    """Page index -> chapter title, from the PDF's table of contents."""
    toc = doc.get_toc()
    if not toc:
        return {}
    level = 2 if sum(1 for e in toc if e[0] == 2) > 3 else 1
    starts = sorted((e[2] - 1, e[1].strip()) for e in toc if e[0] == level and e[2] > 0)
    lookup, current, j = {}, "", 0
    for p in range(doc.page_count):
        while j < len(starts) and starts[j][0] <= p:
            current = starts[j][1]
            j += 1
        lookup[p] = current
    return lookup


def _line_text(spans: list[dict], size: float) -> str:
    """Join a line's spans, dropping footnote markers but keeping subscripts like CO2."""
    parts = []
    for s in spans:
        t = s["text"]
        if s["size"] < size - 2:  # small text inside a line
            prev = "".join(parts)
            if t.strip().isdigit() and re.search(r"(CO|NO|SO|CH|H|N|O)$", prev):
                parts.append(t.strip())  # chemical subscript: CO + 2 -> CO2
            continue  # footnote marker: drop
        parts.append(t)
    return "".join(parts)


def _classify(size: float, body: float) -> str:
    if size >= HEADING_MIN_SIZE:
        return "heading"
    if abs(size - body) <= BODY_TOLERANCE:
        return "body"
    return "small"  # chart labels, captions, notes, footnotes, running headers


def _repeated_lines(prev: str, text: str, min_words: int = 8) -> int:
    """Number of words at the end of `prev` repeated at the start of `text` (0 if fewer than min_words)."""
    a, b = prev.split(), text.split()
    for n in range(min(len(a), len(b)), min_words - 1, -1):
        if a[-n:] == b[:n]:
            return n
    return 0


def extract_paragraphs(path: Path, pages: list[tuple[int, int]] | None = None,
                       keep_notes: bool = KEEP_NOTES) -> list[Paragraph]:
    """Extract clean paragraphs from a PDF, each tagged with page, chapter and heading.

    Works line by line (a PDF block can mix a figure note with body text), uses
    PyMuPDF's native block order (correct for the two-column pages), and joins
    paragraphs that continue across a page or column break.
    """
    doc = pymupdf.open(path)
    page_ids = _page_numbers(doc, pages)
    body = _body_size(doc, page_ids)
    chapters = _chapter_lookup(doc)
    heading = ""
    out: list[Paragraph] = []

    def emit(kind: str, lines: list[str], pno: int) -> None:
        nonlocal heading
        text = _clean_text(" ".join(lines))
        if not text or _NOISE_RE.match(text):
            return
        chapter = chapters.get(pno, "")
        if kind == "heading":
            heading = text
            out.append(Paragraph(text, pno + 1, chapter, heading, True))
        elif kind == "body":
            if len(text.split()) < 4 and not re.search(r"[a-z]{3}", text):
                return  # stray chart label at body size
            prev = out[-1] if out else None
            open_prev = (prev and not prev.is_heading and prev.chapter == chapter
                         and not re.search(r"[.!?:”\")]$", prev.text))
            overlap = _repeated_lines(prev.text, text) if open_prev else 0
            if overlap:
                # the PDF repeats the last lines of a page at the top of the next one
                prev.text = " ".join(prev.text.split()[:-overlap] + [text])
                prev.page_end = pno + 1
            elif open_prev and text[0].islower():
                prev.text += " " + text  # paragraph continues after a page/column break
                prev.page_end = pno + 1
            else:
                out.append(Paragraph(text, pno + 1, chapter, heading))
        elif kind == "small" and keep_notes and len(text.split()) >= 8 \
                and (_NOTE_RE.match(text) or _FOOTNOTE_RE.match(text)):
            out.append(Paragraph(text, pno + 1, chapter, heading))

    for pno in page_ids:
        page = doc[pno]
        height = page.rect.height
        for b in page.get_text("dict")["blocks"]:
            if b["type"] != 0:
                continue
            y0 = b["bbox"][1]
            if y0 < 0.06 * height or y0 > 0.93 * height:  # running header / footer
                continue
            kind, lines = None, []
            for line in b["lines"]:
                spans = [s for s in line["spans"] if s["text"].strip()]
                if not spans:
                    continue
                sizes = Counter()
                for s in spans:
                    sizes[round(s["size"], 1)] += len(s["text"])
                size = sizes.most_common(1)[0][0]
                k = _classify(size, body)
                if k != kind and lines:
                    emit(kind, lines, pno)
                    lines = []
                kind = k
                lines.append(_line_text(spans, size))
            if lines:
                emit(kind, lines, pno)
    doc.close()
    return out


# --------------------------------------------------------------------------
# Chunking: two candidate designs
# --------------------------------------------------------------------------
@dataclass
class Chunk:
    id: str
    text: str  # what gets embedded and shown to the model
    doc_id: str
    title: str
    year: int
    page: int
    page_end: int
    chapter: str
    heading: str
    location: str  # human-readable citation
    n_words: int = field(default=0)


def _location(page: int, page_end: int, chapter: str, heading: str) -> str:
    pages = f"p. {page}" if page == page_end else f"pp. {page}-{page_end}"
    return " · ".join(x for x in (pages, chapter, heading) if x)


def _make_chunk(src: Source, i: int, words: list[str], pages: list[int],
                chapter: str, heading: str, prefix: str = "") -> Chunk:
    body = " ".join(words)
    text = f"{prefix}\n{body}" if prefix else body
    return Chunk(
        id=f"{src.doc_id}-{i:04d}", text=text, doc_id=src.doc_id, title=src.title,
        year=src.year, page=min(pages), page_end=max(pages), chapter=chapter,
        heading=heading, location=_location(min(pages), max(pages), chapter, heading),
        n_words=len(body.split()),
    )


def chunk_fixed(paras: list[Paragraph], src: Source, size: int = 150,
                overlap: int = 30) -> list[Chunk]:
    """Design A: sliding window of `size` words, never crossing a chapter boundary."""
    chunks: list[Chunk] = []
    by_chapter: dict[str, list[Paragraph]] = {}
    for p in paras:
        if not p.is_heading:
            by_chapter.setdefault(p.chapter, []).append(p)
    for chapter, ps in by_chapter.items():
        words, pages, heads = [], [], []
        for p in ps:
            w = p.text.split()
            words += w
            # a paragraph spanning a page break: split its words between the pages
            half = len(w) // 2 if p.page_end != p.page else len(w)
            pages += [p.page] * half + [p.page_end] * (len(w) - half)
            heads += [p.heading] * len(w)
        step = max(1, size - overlap)
        for start in range(0, len(words), step):
            end = min(start + size, len(words))
            if start > 0 and end - start < overlap:  # tail already covered by overlap
                break
            chunks.append(_make_chunk(src, len(chunks), words[start:end], pages[start:end],
                                      chapter, heads[start]))
            if end == len(words):
                break
    return chunks


def chunk_structured(paras: list[Paragraph], src: Source, max_words: int = 250,
                     min_words: int = 60) -> list[Chunk]:
    """Design B: one chunk per heading section, split at paragraph boundaries when long.

    Each chunk starts with its document, chapter and heading, so the embedding
    knows the context ("2026 report, battery prices") even if the text doesn't say it.
    """
    sections: list[tuple[str, str, list[Paragraph]]] = []
    for p in paras:
        if p.is_heading:
            sections.append((p.chapter, p.text, []))
        else:
            if not sections or sections[-1][0] != p.chapter:
                sections.append((p.chapter, p.heading, []))
            sections[-1][2].append(p)

    chunks: list[Chunk] = []
    pending: tuple[str, str, list[Paragraph]] | None = None
    for chapter, heading, ps in sections:
        if not ps:
            continue
        if pending and pending[0] == chapter:  # merge a too-small previous section
            ps = pending[2] + ps
            heading = pending[1]
        elif pending:
            chunks += _split_section(pending, src, len(chunks), max_words)
        pending = None
        if sum(len(p.text.split()) for p in ps) < min_words:
            pending = (chapter, heading, ps)
            continue
        chunks += _split_section((chapter, heading, ps), src, len(chunks), max_words)
    if pending:
        chunks += _split_section(pending, src, len(chunks), max_words)
    for i, c in enumerate(chunks):  # renumber
        c.id = f"{src.doc_id}-{i:04d}"
    return chunks


def _split_section(section, src: Source, start_index: int, max_words: int) -> list[Chunk]:
    chapter, heading, ps = section
    prefix = f"[{src.title} · {chapter} · {heading}]"
    groups: list[list[Paragraph]] = [[]]
    count = 0
    for p in ps:
        n = len(p.text.split())
        if groups[-1] and count + n > max_words:
            groups.append([])
            count = 0
        groups[-1].append(p)
        count += n
    out = []
    for g in groups:
        words = [w for p in g for w in p.text.split()]
        pages = [p.page for p in g] + [p.page_end for p in g]
        out.append(_make_chunk(src, start_index + len(out), words, pages, chapter, heading, prefix))
    return out


CHUNKERS = {"fixed": chunk_fixed, "structured": chunk_structured}
DESIGNS = list(CHUNKERS)  # both are indexed so evaluate.py can compare them
CHUNKING = "structured"  # the design the server uses: chosen from hit rate (eval/retrieval_summary.md)


def chunk_file(path: str | Path, design: str = CHUNKING, **kwargs) -> list[Chunk]:
    """Extract and chunk one file. Known corpus files keep only their selected pages."""
    path = Path(path)
    src = source_for(path)
    paras = extract_paragraphs(path, src.pages)
    return CHUNKERS[design](paras, src, **kwargs)


# --------------------------------------------------------------------------
# Embedding and storage
# --------------------------------------------------------------------------
# index/ holds, per design, chunks_<design>.jsonl (text + metadata) and one
# shared vector cache, vectors.jsonl, keyed by a hash of (model, size, task,
# text). Each vector is appended the moment it arrives, so a crash or the
# free-tier daily limit loses nothing, and re-running embeds only what is
# missing. Question vectors go in the same cache, so evaluations re-use them.
EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768
EMBED_BATCH = 50
VECTORS_FILE = INDEX_DIR / "vectors.jsonl"

_client = None
_cache: dict[str, list[float]] | None = None


def _gemini():
    global _client
    if _client is None:
        from google import genai
        from api_key import load_api_key
        _client = genai.Client(api_key=load_api_key())
    return _client


def vector_key(text: str, task: str) -> str:
    import hashlib
    return hashlib.sha1(f"{EMBED_MODEL}|{EMBED_DIM}|{task}|{text}".encode()).hexdigest()


def load_vectors() -> dict[str, list[float]]:
    global _cache
    if _cache is None:
        _cache = {}
        if VECTORS_FILE.exists():
            with VECTORS_FILE.open() as f:
                for line in f:
                    if line.strip():
                        row = json.loads(line)
                        _cache[row["key"]] = row["vector"]
    return _cache


def embed_texts(texts: list[str], task: str = "RETRIEVAL_DOCUMENT") -> list[list[float]]:
    """Vectors for `texts`, calling Gemini only for those not in the cache."""
    import time
    from google.genai import errors, types

    cache = load_vectors()
    missing = list(dict.fromkeys(t for t in texts if vector_key(t, task) not in cache))
    INDEX_DIR.mkdir(exist_ok=True)
    done = 0
    while done < len(missing):
        batch = missing[done:done + EMBED_BATCH]
        try:
            # One Content per text: a plain list of strings is embedded by
            # gemini-embedding-2 as ONE multi-part input and returns ONE vector.
            resp = _gemini().models.embed_content(
                model=EMBED_MODEL,
                contents=[types.Content(parts=[types.Part(text=t)]) for t in batch],
                config=types.EmbedContentConfig(task_type=task, output_dimensionality=EMBED_DIM),
            )
            if len(resp.embeddings) != len(batch):
                raise RuntimeError(f"Asked for {len(batch)} vectors, got {len(resp.embeddings)}")
        except errors.APIError as e:
            if e.code == 429:
                if "PerDay" in str(e) or "per day" in str(e).lower():
                    raise SystemExit(
                        f"Daily embedding quota reached after {done} new vectors (all saved). "
                        "Run again after the reset (09:00 in Spain)."
                    )
                wait = 60
                m = re.search(r"retry in ([\d.]+)s|'retryDelay': '(\d+)s'", str(e))
                if m:
                    wait = float(m.group(1) or m.group(2)) + 1
                print(f"  rate limit, waiting {wait:.0f}s ...", file=sys.stderr)
                time.sleep(wait)
                continue
            raise
        with VECTORS_FILE.open("a") as f:
            for text, emb in zip(batch, resp.embeddings):
                vec = [round(x, 6) for x in emb.values]
                key = vector_key(text, task)
                cache[key] = vec
                f.write(json.dumps({"key": key, "vector": vec}) + "\n")
            f.flush()
        done += len(batch)
        print(f"  embedded {done}/{len(missing)} new texts", file=sys.stderr)
    return [cache[vector_key(t, task)] for t in texts]


def chunks_file(design: str) -> Path:
    return INDEX_DIR / f"chunks_{design}.jsonl"


def load_chunks(design: str = CHUNKING) -> list[dict]:
    path = chunks_file(design)
    if not path.exists():
        return []
    with path.open() as f:
        return [json.loads(line) for line in f if line.strip()]


def embed_and_store(chunks: list[Chunk], design: str = CHUNKING) -> int:
    """Embed `chunks` (only those without a saved vector) and store them in index/.

    Chunks of a document already in the index replace that document's old
    chunks, so storing the same document twice never duplicates it.
    Returns the number of chunks stored.
    """
    embed_texts([c.text for c in chunks], "RETRIEVAL_DOCUMENT")
    new_docs = {c.doc_id for c in chunks}
    kept = [row for row in load_chunks(design) if row["doc_id"] not in new_docs]
    rows = kept + [asdict(c) for c in chunks]
    tmp = chunks_file(design).with_suffix(".tmp")
    with tmp.open("w") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    tmp.replace(chunks_file(design))
    return len(chunks)


# --------------------------------------------------------------------------
# Document registry and duplicate policy
# --------------------------------------------------------------------------
# index/documents.json records, for every indexed document, a SHA-256 hash of
# the file and its number of chunks per design. Policy when a document is
# indexed (DECISIONS.md, section 9):
#   - same content as a document already indexed -> nothing to do, no embeddings spent
#   - same document (same doc_id), different content -> new version replaces the old one
#   - otherwise -> added
DOCUMENTS_FILE = INDEX_DIR / "documents.json"


def file_hash(path: str | Path) -> str:
    import hashlib
    h = hashlib.sha256()
    with Path(path).open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            h.update(block)
    return h.hexdigest()


def load_documents() -> dict[str, dict]:
    if not DOCUMENTS_FILE.exists():
        return {}
    return json.loads(DOCUMENTS_FILE.read_text(encoding="utf-8"))


def _register(src: Source, sha256: str, design: str, n_chunks: int) -> None:
    docs = load_documents()
    entry = docs.get(src.doc_id, {})
    if entry.get("sha256") != sha256:  # new document or new version: forget old chunk counts
        entry = {"chunks": {}}
    entry.update(title=src.title, year=src.year, file=src.file, publisher=src.publisher,
                 licence=src.licence, sha256=sha256)
    entry["chunks"][design] = n_chunks
    docs[src.doc_id] = entry
    INDEX_DIR.mkdir(exist_ok=True)
    DOCUMENTS_FILE.write_text(json.dumps(docs, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def index_document(path: str | Path, design: str = CHUNKING) -> dict:
    """Index one file under the duplicate policy above (used by server.py's add_document).

    Returns {"status": "unchanged" | "replaced" | "added", "doc_id", "title",
    "chunks", "old_chunks", "pages"}. Chunks are only written once every
    embedding has arrived, so a failure leaves the index as it was.
    """
    path = Path(path)
    sha256 = file_hash(path)
    docs = load_documents()
    for doc_id, entry in docs.items():
        if entry.get("sha256") == sha256 and design in entry.get("chunks", {}):
            return {"status": "unchanged", "doc_id": doc_id, "title": entry["title"],
                    "chunks": entry["chunks"][design], "old_chunks": entry["chunks"][design], "pages": ""}
    src = source_for(path)
    old = docs.get(src.doc_id, {}).get("chunks", {}).get(design)
    chunks = chunk_file(path, design)
    if not chunks:
        raise ValueError(f"No text could be extracted from {path.name} (scanned or empty PDF?)")
    embed_and_store(chunks, design)
    _register(src, sha256, design, len(chunks))
    return {"status": "replaced" if old is not None else "added", "doc_id": src.doc_id,
            "title": src.title, "chunks": len(chunks), "old_chunks": old,
            "pages": f"{min(c.page for c in chunks)}-{max(c.page_end for c in chunks)}"}


def build_index() -> None:
    """`main.py index`: chunk every corpus document with each design, embed, store."""
    for design in DESIGNS:
        per_doc = {s.doc_id: chunk_file(CORPUS_DIR / s.file, design) for s in SOURCES}
        chunks = [c for cs in per_doc.values() for c in cs]
        print(f"[{design}] {len(chunks)} chunks", file=sys.stderr)
        embed_and_store(chunks, design)  # documents added later with add_document are kept
        for s in SOURCES:
            _register(s, file_hash(CORPUS_DIR / s.file), design, len(per_doc[s.doc_id]))
    size_mb = sum(p.stat().st_size for p in INDEX_DIR.iterdir()) / 1e6
    print(f"Index ready in {INDEX_DIR} ({size_mb:.1f} MB)")


# --------------------------------------------------------------------------
# Preview (no embeddings)
# --------------------------------------------------------------------------
def preview(out_dir: Path) -> None:
    out_dir.mkdir(parents=True, exist_ok=True)
    configs = {
        "fixed-100": ("fixed", dict(size=100, overlap=20)),
        "fixed-150": ("fixed", dict(size=150, overlap=30)),
        "fixed-250": ("fixed", dict(size=250, overlap=50)),
        "structured": ("structured", dict(max_words=250, min_words=60)),
    }
    print(f"{'design':12} {'chunks':>6} {'words':>7} {'median':>6} {'min':>4} {'max':>4}")
    for name, (design, kw) in configs.items():
        chunks = [c for s in SOURCES for c in chunk_file(CORPUS_DIR / s.file, design, **kw)]
        n = [c.n_words for c in chunks]
        print(f"{name:12} {len(chunks):>6} {sum(n):>7} {int(statistics.median(n)):>6} "
              f"{min(n):>4} {max(n):>4}")
        with (out_dir / f"chunks_{name}.jsonl").open("w") as f:
            for c in chunks:
                f.write(json.dumps(asdict(c), ensure_ascii=False) + "\n")
    print(f"\nChunks written to {out_dir}")


if __name__ == "__main__":
    ap = argparse.ArgumentParser()
    ap.add_argument("--preview", metavar="DIR", nargs="?", const=str(ROOT / "corpus" / "preview"),
                    help="write candidate chunkings to DIR and print stats; no embeddings")
    args = ap.parse_args()
    download_corpus()
    if args.preview:
        preview(Path(args.preview))
    else:
        build_index()
