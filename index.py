"""
Assignment 3: build the index (`main.py index`).

Downloads the corpus into corpus/ (git-ignored), extracts and cleans the text
with its location (GDPR article and paragraph; EDPB numbered paragraph and
page), chunks it with each retrieval design, embeds the chunks with Gemini and
stores them in index/ (ChromaDB). Vectors are saved batch by batch, and a chunk
that already has a saved vector is never embedded again, so a crash or the
daily quota loses nothing: run it again tomorrow and it carries on.

server.py's add_document tool imports this pipeline (`index_file`, which runs `chunk_file` and
`embed_and_store`), so the server has no second copy of the chunking logic.
"""

from __future__ import annotations

import hashlib
import re
import sys
import urllib.request
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import rag
from rag import log

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"

# The corpus. `source` is the short id used in citations and in eval/questions.csv.
DOCS = [
    {
        "source": "GDPR",
        "title": "Regulation (EU) 2016/679 (General Data Protection Regulation)",
        "url": "https://eur-lex.europa.eu/eli/reg/2016/679/oj/eng",
        # EUR-Lex blocks scripted downloads; the EU Publications Office serves the same Official Journal text.
        "download": "http://publications.europa.eu/resource/celex/32016R0679",
        "headers": {"Accept": "application/xhtml+xml", "Accept-Language": "eng"},
        "file": "gdpr.html",
        "date": "2016-04-27",
        "licence": "EU legal acts; reuse authorised (Commission Decision 2011/833/EU), source acknowledged",
    },
    {
        "source": "EDPB 05/2020",
        "title": "EDPB Guidelines 05/2020 on consent under Regulation 2016/679 (v1.1)",
        "url": "https://www.edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-052020-consent-under-regulation-2016679_en",
        "download": "https://www.edpb.europa.eu/system/files/documents/files/file1/edpb_guidelines_202005_consent_en.pdf",
        "file": "edpb_guidelines_05_2020_consent.pdf",
        "date": "2020-05-04",
        "licence": "EDPB: reuse authorised for commercial and non-commercial purposes, source acknowledged",
    },
    {
        "source": "EDPB 9/2022",
        "title": "EDPB Guidelines 9/2022 on personal data breach notification under GDPR (v2.0)",
        "url": "https://www.edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-92022-personal-data-breach-notification-under_en",
        "download": "https://www.edpb.europa.eu/system/files/documents/2023-04/edpb_guidelines_202209_personal_data_breach_notification_v2.0_en.pdf",
        "file": "edpb_guidelines_9_2022_breach.pdf",
        "date": "2023-03-28",
        "licence": "EDPB: reuse authorised for commercial and non-commercial purposes, source acknowledged",
    },
]

# Documents known by file name, so add_document can give them a proper source id and title.
EXTRA_DOCS = [
    {
        "source": "EDPB 07/2020",
        "title": "EDPB Guidelines 07/2020 on the concepts of controller and processor in the GDPR (v2.1)",
        "url": "https://www.edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-072020-concepts-controller-and-processor-gdpr_en",
        "download": "https://www.edpb.europa.eu/system/files/2023-10/EDPB_guidelines_202007_controllerprocessor_final_en.pdf",
        "file": "edpb_guidelines_07_2020_controller_processor.pdf",
        "date": "2021-07-07",
        "licence": "EDPB: reuse authorised for commercial and non-commercial purposes, source acknowledged",
    },
]

# Design "fixed": windows of FIXED_WORDS words, ignoring structure.
FIXED_WORDS, FIXED_OVERLAP = 200, 25
# Design "structure": one chunk per article paragraph / numbered paragraph, small
# neighbours in the same article or section merged, long ones split.
MERGE_UP_TO, SPLIT_ABOVE, SPLIT_SIZE = 250, 350, 250


@dataclass
class Unit:
    """The smallest located piece of text: an article paragraph, a numbered paragraph, an annex example."""
    loc: str                 # "Art. 33(1)", "para. 42", "Annex ex. vi"
    group: str               # what may be merged together: an article, or a section
    section: str             # heading path, for the reader and the embedding title
    text: str
    page: int = -1
    locs: list[str] = field(default_factory=list)   # every location this unit counts as


@dataclass
class Chunk:
    id: str
    design: str
    source: str
    title: str
    url: str
    location: str            # what a citation shows
    locs: list[str]          # every location covered, for hit-rate and citation checks
    page: int
    section: str
    text: str

    def metadata(self, doc_hash: str) -> dict:
        return {
            "source": self.source, "title": self.title, "url": self.url, "location": self.location,
            "locs": "|" + "|".join(self.locs) + "|", "page": self.page, "section": self.section,
            "design": self.design, "doc_hash": doc_hash,
        }


# --------------------------------------------------------------------------- download

def download(doc: dict) -> Path:
    path = CORPUS_DIR / doc["file"]
    if path.is_file() and path.stat().st_size > 0:
        return path
    CORPUS_DIR.mkdir(exist_ok=True)
    log(f"Downloading {doc['source']} from {doc['download']}")
    headers = {"User-Agent": "Mozilla/5.0 (DAIIST assignment 3)", **doc.get("headers", {})}
    with urllib.request.urlopen(urllib.request.Request(doc["download"], headers=headers), timeout=120) as r:
        data = r.read()
    if len(data) < 10_000:
        raise RuntimeError(f"Download of {doc['source']} looks wrong ({len(data)} bytes)")
    path.write_bytes(data)
    return path


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()[:16]


# --------------------------------------------------------------------------- cleaning

def clean(text: str) -> str:
    text = text.replace("\u00a0", " ").replace("\u00ad", "")
    text = re.sub("[\uf0a7\uf0b7\uf0d8\uf0fc\u25aa]", "•", text)   # Symbol-font bullets
    text = re.sub(r"(\w)-\n(\w)", r"\1-\2", text)          # keep hyphen, join the line break
    text = re.sub(r"\s*\n\s*", " ", text)
    text = re.sub(r"\s+([,.;:)])", r"\1", text)
    text = re.sub(r"([(])\s+", r"\1", text)
    return re.sub(r"\s{2,}", " ", text).strip()


def fix_split_words(units: list[Unit]) -> int:
    """PDF text sometimes splits a word ("dat a", "offer ed"). Rejoin two tokens when the
    joined form is a frequent word of the same document and one half is not a word there."""
    vocab: dict[str, int] = {}
    for u in units:
        for w in re.findall(r"[A-Za-z]+", u.text):
            vocab[w.lower()] = vocab.get(w.lower(), 0) + 1
    fixed = 0

    def join(m: re.Match) -> str:
        nonlocal fixed
        a, b = m.group(1), m.group(2)
        joined = (a + b).lower()
        if vocab.get(joined, 0) >= 3 and (vocab.get(a.lower(), 0) <= 1 or vocab.get(b.lower(), 0) <= 1):
            fixed += 1
            return a + b
        return m.group(0)

    for u in units:
        u.text = re.sub(r"\b([A-Za-z]{2,})\s([a-z]{1,4})\b", join, u.text)
    return fixed


# --------------------------------------------------------------------------- GDPR (Official Journal HTML)

def extract_gdpr_html(path: Path) -> list[Unit]:
    """Articles only (recitals left out, see REPORT.md). One unit per numbered paragraph,
    or per point for lists like the Article 4 definitions."""
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    for note in soup.select("span.oj-note-tag, p.oj-note"):
        note.decompose()
    units: list[Unit] = []

    def text_of(el) -> str:
        # points sit in two-cell tables: "(a)" | "text"; join each row on one line
        for table in el.find_all("table"):
            cells = [clean(td.get_text(" ")) for td in table.find_all("td")]
            table.replace_with(soup.new_string(" " + " ".join(cells) + " "))
        return clean(el.get_text(" "))

    for art in soup.find_all("div", class_="eli-subdivision", id=re.compile(r"^art_\d+$")):
        number = art["id"].split("_")[1]
        heading = clean(art.find("p", class_="oj-sti-art").get_text(" "))
        chapter = art.find_parent("div", id=re.compile(r"^cpt_[^.]+$"))
        chapter_title = ""
        if chapter:
            ch = [clean(p.get_text(" ")) for p in chapter.find_all("p", class_=re.compile("oj-ti-section"), limit=2)]
            chapter_title = " – ".join(ch).replace("CHAPTER", "Chapter")
        section = f"{chapter_title} > Article {number} – {heading}".strip(" >")
        article_loc = f"Art. {number}"
        intro = []
        for child in art.find_all(recursive=False):
            cid = child.get("id", "")
            if child.name == "p" and "oj-ti-art" in child.get("class", []):
                continue
            if cid.endswith(".tit_1"):
                continue
            m = re.match(r"^0*(\d+)\.0*(\d+)$", cid)
            if m:  # numbered paragraph
                loc = f"{article_loc}({int(m.group(2))})"
                units.append(Unit(loc, article_loc, section, text_of(child), locs=[article_loc, loc]))
            elif child.name == "table":  # a point directly under the article (Art. 4 definitions)
                cells = [clean(td.get_text(" ")) for td in child.find_all("td")]
                label = cells[0].strip("()") if cells else ""
                loc = f"{article_loc}({label})" if label else article_loc
                units.append(Unit(loc, article_loc, section, " ".join(cells), locs=[article_loc, loc]))
            else:
                t = text_of(child)
                if t:
                    intro.append(t)
        if intro:
            units.insert(len(units), Unit(article_loc, article_loc, section, " ".join(intro), locs=[article_loc]))
    return units


# --------------------------------------------------------------------------- EDPB-style PDFs

FOOTER = re.compile(r"^\s*adopted\s*(\d+)?\s*$", re.I)
# The body starts at the preface; title page, version history and EDPB preamble are skipped.
START = re.compile(r"^(0\s*)?(PREFACE|INTRODUCTION|EXECUTIVE SUMMARY)\b", re.I)
TOC_LEADER = re.compile(r"\.{6,}")
ROMAN = re.compile(r"^(x{0,3}(?:ix|iv|v?i{0,3}))\s+(\S.*)$", re.S)


def heading_level(size: float) -> int:
    """EDPB layout: body 11 pt, headings 12/13/16 pt, footnotes 10 pt, superscript markers 7 pt."""
    if size >= 15:
        return 1
    if size >= 12.5:
        return 2
    if size >= 11.5:
        return 3
    return 0


def annex_table_units(page, page_no: int, section: str, units: list[Unit]) -> None:
    """The breach guidelines' Annex B is a 4-column table of worked examples that runs over
    several pages. Plain text extraction interleaves the columns, so read it as a table and
    assign each cell to a column by its x position; rows that do not start with a roman
    numeral continue the previous example."""
    bounds = [180, 294, 403]
    for table in page.find_tables():
        for row in table.rows:
            values = ["", "", "", ""]
            for cell in row.cells:
                if not cell:
                    continue
                text = clean(page.crop(cell).extract_text(x_tolerance=1) or "")
                if not text:
                    continue
                col = sum((cell[0] + cell[2]) / 2 > b for b in bounds)
                values[col] = (values[col] + " " + text).strip()
            if values[0].startswith("Example") or not any(values):
                continue
            m = ROMAN.match(values[0])
            if m and m.group(1):
                label = m.group(1)
                values[0] = m.group(2)
                units.append(Unit(f"Annex ex. {label}", f"Annex ex. {label}", section, "", page_no, [f"Annex ex. {label}", "Annex"]))
                units[-1].parts = values
            else:   # continues the last example, even if a stray line was saved in between
                last = next((u for u in reversed(units) if hasattr(u, "parts")), None)
                if last is not None:
                    last.parts = [(a + " " + b).strip() for a, b in zip(last.parts, values)]


ANNEX_COLUMNS = ["Notify the supervisory authority?", "Notify the data subjects?", "Notes/recommendations"]


def annex_text(u: Unit) -> str:
    """Built once all pages are read, so a row continued on the next page is complete.
    The example's own label goes in the text, so a passage can be cited precisely."""
    label = u.loc.replace("Annex ex. ", "")
    rest = " ".join(f"{name} {value}" for name, value in zip(ANNEX_COLUMNS, u.parts[1:]) if value)
    return f"Example {label}: {u.parts[0]} {rest}".strip()


def extract_pdf(path: Path, start_anywhere: bool = False) -> list[Unit]:
    """Numbered paragraphs with page and heading path. Footnotes, page footers, the table of
    contents and superscript footnote markers are removed by font size and pattern."""
    import pdfplumber

    units: list[Unit] = []
    headings: list[str] = []            # current heading path, one entry per level
    started = False
    expected = 1                        # next paragraph number
    current: Unit | None = None
    preamble: list[str] = []
    in_annex_table = False

    def section() -> str:
        return " > ".join(h for h in headings if h)

    def flush():
        nonlocal current
        if current and current.text.strip():
            current.text = clean(current.text)
            units.append(current)
        current = None

    with pdfplumber.open(path) as pdf:
        for page_no, page in enumerate(pdf.pages, start=1):
            raw = page.extract_text(x_tolerance=1) or ""
            if len(TOC_LEADER.findall(raw)) >= 5:          # table of contents page
                continue
            body = page.filter(lambda o: o.get("object_type") != "char" or o.get("size", 0) >= 10.5)
            lines = body.extract_text_lines(x_tolerance=1)
            for line in lines:
                text = line["text"].strip()
                sizes = [round(c["size"], 1) for c in line["chars"] if c["text"].strip()]
                size = max(set(sizes), key=sizes.count) if sizes else 11
                if not text or FOOTER.match(text):
                    continue
                level = heading_level(size)
                if level:
                    if level == 1 and (start_anywhere or START.match(text)):
                        started = True
                    if not started:
                        continue
                    flush()
                    # a heading wrapped over two lines continues the same level
                    if len(headings) >= level and getattr(extract_pdf, "_last_heading", None) == (page_no, level):
                        headings[level - 1] += " " + text
                    else:
                        headings[:] = headings[: level - 1] + [""] * max(0, level - 1 - len(headings)) + [text]
                    extract_pdf._last_heading = (page_no, level)
                    in_annex_table = bool(re.search(r"\bexamples?\b", text, re.I)) and "ANNEX" in section().upper()
                    continue
                extract_pdf._last_heading = None
                if not started:
                    continue
                m = re.match(r"^(\d{1,3})\.(?:\s+(.*))?$", text)
                if m and expected <= int(m.group(1)) <= expected + 2:
                    flush()
                    n = int(m.group(1))
                    expected = n + 1
                    current = Unit(f"para. {n}", section(), section(), m.group(2) or "", page_no, [f"para. {n}"])
                elif current is not None:
                    current.text += "\n" + text
                else:   # unnumbered text under a heading (preface, introductions)
                    head = headings[-1] if headings else "Front matter"
                    current = Unit(f"sec. {head[:60]}", section(), section(), text, page_no, [f"sec. {head[:60]}"])
            if in_annex_table:
                flush()
                annex_table_units(page, page_no, section(), units)
        flush()
    for u in units:
        if hasattr(u, "parts"):
            u.text = annex_text(u)
            del u.parts
    if not units and not start_anywhere:     # a PDF without a preface heading
        return extract_pdf(path, start_anywhere=True)
    return units


def extract_text_file(path: Path) -> list[Unit]:
    """Plain text or Markdown: one unit per paragraph block, located by '#' heading."""
    units, heading, n = [], "", 0
    for block in re.split(r"\n\s*\n", path.read_text(encoding="utf-8", errors="replace")):
        block = block.strip()
        if not block:
            continue
        if block.startswith("#"):
            heading = block.lstrip("#").strip()
            continue
        n += 1
        units.append(Unit(f"block {n}", heading, heading, clean(block), locs=[f"block {n}"]))
    return units


def extract(path: Path) -> list[Unit]:
    suffix = path.suffix.lower()
    if suffix in (".html", ".htm", ".xhtml"):
        units = extract_gdpr_html(path)
    elif suffix == ".pdf":
        units = extract_pdf(path)
    elif suffix in (".txt", ".md"):
        units = extract_text_file(path)
    else:
        raise ValueError(f"Unsupported file type {suffix!r}; use .pdf, .html, .txt or .md")
    # drop layout scraps: a lone ".", the annex's stray roman numerals
    units = [u for u in units if len(re.findall(r"[A-Za-z]{3,}", u.text)) >= 2]
    if not units:
        raise ValueError(f"No text could be extracted from {path.name}")
    fixed = fix_split_words(units)
    if fixed:
        log(f"{path.name}: rejoined {fixed} split words")
    return units


# --------------------------------------------------------------------------- chunking

def span(locs: list[str]) -> str:
    """'para. 29', 'para. 30', 'para. 31' -> 'para. 29–31'; 'Art. 33(1)'..'Art. 33(3)' -> 'Art. 33(1)–(3)'."""
    finest = [l for l in locs if not re.fullmatch(r"Art\. \d+|Annex", l)] or locs
    first, last = finest[0], finest[-1]
    if first == last:
        return first
    pattern = r"^(.*?)(\d+|\(\w+\)|(?<=ex\. )[ivx]+)$"
    a, b = re.match(pattern, first), re.match(pattern, last)
    if a and b and a.group(1) == b.group(1):
        return f"{first}–{b.group(2)}"
    return f"{first}–{last}"


def make_chunk(design: str, doc: dict, units: list[Unit], text: str) -> Chunk:
    locs = list(dict.fromkeys(l for u in units for l in u.locs))
    section = units[0].section
    body = text
    title = doc["title"] if design == "fixed" else f"{doc['source']}: {section}"
    cid = hashlib.sha256(f"{design}|{doc['source']}|{title}|{body}".encode()).hexdigest()[:20]
    return Chunk(cid, design, doc["source"], doc["title"], doc["url"], span(locs), locs,
                 units[0].page, section, body)


def chunk_fixed(doc: dict, units: list[Unit]) -> list[Chunk]:
    """Baseline: a sliding window of FIXED_WORDS words over the whole document, ignoring structure.
    Each chunk still records every location its words came from."""
    words = [(w, i) for i, u in enumerate(units) for w in u.text.split()]
    chunks, step = [], FIXED_WORDS - FIXED_OVERLAP
    for start in range(0, len(words), step):
        window = words[start:start + FIXED_WORDS]
        if len(window) < 30 and chunks:
            break
        used = [units[i] for i in dict.fromkeys(i for _, i in window)]
        chunks.append(make_chunk("fixed", doc, used, " ".join(w for w, _ in window)))
        if start + FIXED_WORDS >= len(words):
            break
    return chunks


def chunk_structure(doc: dict, units: list[Unit]) -> list[Chunk]:
    """One chunk per structural unit; neighbours in the same article/section are merged up to
    MERGE_UP_TO words; a unit over SPLIT_ABOVE words is split into SPLIT_SIZE-word pieces."""
    chunks: list[Chunk] = []
    buffer: list[Unit] = []

    def emit():
        if buffer:
            chunks.append(make_chunk("structure", doc, buffer, " ".join(u.text for u in buffer)))
            buffer.clear()

    for u in units:
        n = len(u.text.split())
        if n > SPLIT_ABOVE:
            emit()
            words = u.text.split()
            parts = max(2, round(n / SPLIT_SIZE))
            size = -(-n // parts)
            for p in range(parts):
                piece = " ".join(words[p * size:(p + 1) * size])
                if piece:
                    chunks.append(make_chunk("structure", doc, [u], piece))
            continue
        if buffer and (buffer[0].group != u.group or sum(len(b.text.split()) for b in buffer) + n > MERGE_UP_TO):
            emit()
        buffer.append(u)
    emit()
    return chunks


CHUNKERS = {"fixed": chunk_fixed, "structure": chunk_structure}


def doc_info(path: Path) -> dict:
    """The corpus entry for a file, or a new entry named after the file."""
    for doc in DOCS + EXTRA_DOCS:
        if path.name == doc["file"]:
            return doc
    return {"source": path.stem, "title": path.stem.replace("_", " "), "url": str(path), "file": path.name}


def chunk_file(path: str | Path, design: str = rag.ACTIVE_DESIGN) -> tuple[dict, list[Chunk]]:
    """Extract, clean and chunk one file. Returns its corpus entry and its chunks."""
    path = Path(path).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"No such file: {path}")
    doc = doc_info(path)
    return doc, CHUNKERS[design](doc, extract(path))


# --------------------------------------------------------------------------- embed and store

def embed_and_store(doc: dict, chunks: list[Chunk], doc_hash: str, design: str) -> dict:
    """Store a document's chunks. Only chunks without a saved vector are embedded (chunk ids
    are content hashes), and each batch is written as soon as it comes back. Chunks of this
    source that are no longer produced are removed. Returns counts."""
    col = rag.collection(design)
    old = col.get(where={"source": doc["source"]}, include=[])["ids"]
    new_ids = [c.id for c in chunks]
    stale = sorted(set(old) - set(new_ids))
    have = set(col.get(ids=new_ids, include=[])["ids"]) if new_ids else set()
    todo = [c for c in chunks if c.id not in have]
    # refresh metadata of chunks we keep (e.g. a new file hash)
    kept = [c for c in chunks if c.id in have]
    if kept:
        col.update(ids=[c.id for c in kept], metadatas=[c.metadata(doc_hash) for c in kept])
    for i in range(0, len(todo), rag.EMBED_BATCH):
        batch = todo[i:i + rag.EMBED_BATCH]
        vectors = rag.embed_texts([rag.document_text(embed_title(c), c.text) for c in batch])
        col.add(ids=[c.id for c in batch], embeddings=vectors, documents=[c.text for c in batch],
                metadatas=[c.metadata(doc_hash) for c in batch])
        log(f"  {design}: embedded {min(i + rag.EMBED_BATCH, len(todo))}/{len(todo)} new chunks of {doc['source']}")
    if stale:   # only after every new chunk is stored, so a quota stop never leaves a document half replaced
        col.delete(ids=stale)
    return {"chunks": len(chunks), "embedded": len(todo), "reused": len(kept), "removed": len(stale)}


def embed_title(c: Chunk) -> str:
    return c.title if c.design == "fixed" else f"{c.source}: {c.section}"


def register(doc: dict, path: Path, doc_hash: str, design: str, n_chunks: int) -> None:
    documents = rag.load_documents()
    entry = documents.get(doc["source"], {})
    entry.update({k: doc.get(k, "") for k in ("source", "title", "url", "date", "licence")})
    entry.update({"file": path.name, "file_hash": doc_hash, "words": None})
    entry.setdefault("chunks", {})[design] = n_chunks
    entry["updated"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    documents[doc["source"]] = entry
    rag.save_documents(documents)


def index_file(path: str | Path, design: str = rag.ACTIVE_DESIGN) -> dict:
    """The whole pipeline for one file: chunk, embed what is new, store, register."""
    path = Path(path).expanduser().resolve()
    doc, chunks = chunk_file(path, design)
    h = file_hash(path)
    result = embed_and_store(doc, chunks, h, design)
    register(doc, path, h, design, len(chunks))
    return {"source": doc["source"], **result}


def export_readable(out_dir: Path = CORPUS_DIR / "readable") -> list[Path]:
    """Write each cleaned document as Markdown with its locations, for writing the test set."""
    out_dir.mkdir(parents=True, exist_ok=True)
    written = []
    for doc in DOCS:
        units = extract(download(doc))
        lines = [f"# {doc['title']}", "", f"Source id: `{doc['source']}`  ·  {doc['url']}", ""]
        last = None
        for u in units:
            if u.section != last:
                lines += ["", f"## {u.section}", ""]
                last = u.section
            page = f" (p. {u.page})" if u.page > 0 else ""
            lines.append(f"**[{doc['source']} | {u.loc}]**{page} {u.text}\n")
        path = out_dir / (Path(doc["file"]).stem + ".md")
        path.write_text("\n".join(lines), encoding="utf-8")
        written.append(path)
    return written


def main() -> int:
    if "--export" in sys.argv:
        for p in export_readable():
            log(f"wrote {p}")
        return 0
    paths = [download(doc) for doc in DOCS]
    for doc in EXTRA_DOCS:   # downloaded for the add-document test, not indexed here
        download(doc)
    total_words = 0
    for path in paths:
        units = extract(path)
        words = sum(len(u.text.split()) for u in units)
        total_words += words
        log(f"{path.name}: {len(units)} units, {words} words")
    log(f"Corpus: {len(paths)} documents, {total_words} words")
    try:
        for design in rag.DESIGNS:
            for path in paths:
                result = index_file(path, design)
                log(f"{design:9s} {result['source']:13s} {result['chunks']:4d} chunks "
                    f"({result['embedded']} embedded now, {result['reused']} already saved, {result['removed']} removed)")
    except rag.QuotaExhausted:
        log("\nThe daily embedding quota is used up. Everything embedded so far is saved in index/.\n"
            "Run `uv run python main.py index` again after 09:00 (Spain) to finish.")
        return 1
    for design in rag.DESIGNS:
        log(f"index/ collection corpus_{design}: {rag.collection(design).count()} chunks")
    return 0


if __name__ == "__main__":
    sys.exit(main())
