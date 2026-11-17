"""
Assignment 3: build the index (`main.py index`).

Corpus: open-access research on padel rackets (shape, weight, balance, sweet spot,
vibration) and padel injuries. Steps, per file:

    download_corpus()          PDFs into corpus/ (git-ignored)
    extract_pages(path)        text per page (pypdf / txt / html)
    clean_pages(pages)         fixes hyphenation, ligatures, running headers, drops back matter
    chunk_file(path, design)   "fixed" (150-word windows) or "section" (structure-based) chunks,
                               each with doc_id, title, page_start/page_end and section
    embed_and_store(chunks, design)   embeds only chunks without a saved vector, saves batch by batch

server.py's add_document imports index_file(), which runs the same steps on one file.
"""

from __future__ import annotations

import hashlib
import re
import sys
import unicodedata
from pathlib import Path

import rag
from rag import log

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"

# id, file, url, title, year, licence. Ids are what citations show, so keep them short.
DOCS = [
    {
        "doc_id": "blanes2023",
        "file": "sensors-23-09908.pdf",
        "url": "https://www.mdpi.com/1424-8220/23/24/9908/pdf",
        "mirror": "https://riunet.upv.es/bitstream/10251/201887/1/BlanesCorrecherMartinez-Turegano%20-%20Identifying%20the%20Sweet%20Spot%20of%20Padel%20Rackets%20with%20a%20Robot.pdf",
        "title": "Identifying the Sweet Spot of Padel Rackets with a Robot",
        "authors": "Blanes, Correcher, Martinez-Turegano, Ricolfe-Viala",
        "venue": "Sensors 23(24):9908",
        "year": 2023,
        "licence": "CC BY 4.0",
    },
    {
        "doc_id": "blanes2022",
        "file": "sensors-22-09266.pdf",
        "url": "https://www.mdpi.com/1424-8220/22/23/9266/pdf",
        "title": "Identifying the Inertial Properties of a Padel Racket: An Experimental Maneuverability Proposal",
        "authors": "Blanes, Correcher, Beltran, Mellado",
        "venue": "Sensors 22(23):9266",
        "year": 2022,
        "licence": "CC BY 4.0",
    },
    {
        "doc_id": "munoz2022",
        "file": "ijerph-19-16858.pdf",
        "url": "https://www.mdpi.com/1660-4601/19/24/16858/pdf",
        "title": "Incidence of Upper Body Injuries in Amateur Padel Players",
        "authors": "Munoz, Coronado, Robles-Gil, Martin, Escudero-Tena",
        "venue": "Int. J. Environ. Res. Public Health 19(24):16858",
        "year": 2022,
        "licence": "CC BY 4.0",
    },
    {
        "doc_id": "dahmen2023",
        "file": "e001607.full.pdf",
        "url": "https://bmjopensem.bmj.com/content/bmjosem/9/2/e001607.full.pdf",
        "title": "Incidence, prevalence and nature of injuries in padel: a systematic review",
        "authors": "Dahmen, Emanuel, Fontanellas-Fes, Verhagen, Kerkhoffs, Pluim",
        "venue": "BMJ Open Sport & Exercise Medicine 9(2):e001607",
        "year": 2023,
        "licence": "CC BY-NC 4.0",
    },
    {
        "doc_id": "garcia2022",
        "file": "ijerph-19-04395.pdf",
        "url": "https://www.mdpi.com/1660-4601/19/7/4395/pdf",
        "title": "Performance Outcome Measures in Padel: A Scoping Review",
        "authors": "Garcia-Gimenez, Pradas de la Fuente, Castellar Otin, Carrasco Paez",
        "venue": "Int. J. Environ. Res. Public Health 19(7):4395",
        "year": 2022,
        "licence": "CC BY 4.0",
    },
    {
        "doc_id": "martin2025",
        "file": "sports-13-00075.pdf",
        "url": "https://www.mdpi.com/2075-4663/13/3/75/pdf",
        "title": "Topics of Study in Under-18 Padel Categories: A Scoping Review",
        "authors": "Martin-Miguel, Munoz, Conde-Ripoll, Bustamante-Sanchez, Sanchez-Alcaraz",
        "venue": "Sports 13(3):75",
        "year": 2025,
        "licence": "CC BY 4.0",
    },
    {
        "doc_id": "aguilar2026",
        "file": "applsci-16-02680.pdf",
        "url": "https://www.mdpi.com/2076-3417/16/6/2680/pdf",
        "title": "Epidemiology, Incidence, Prevalence, and Treatment of Injuries in Padel: A Scoping Review",
        "authors": "Aguilar-Nunez, Gonzalez-Romero, Perez-Montilla, Hamed-Hamed, Gonzalez-Munoz, Navarro-Ledesma",
        "venue": "Applied Sciences 16(6):2680",
        "year": 2026,
        "licence": "CC BY 4.0",
    },
    {
        "doc_id": "portugal2025",
        "file": "medicina-61-01707.pdf",
        "url": "https://www.mdpi.com/1648-9144/61/9/1707/pdf",
        "title": "Sport-Related Injuries in Portuguese Padel Practitioners and Their Characteristics",
        "authors": "see article",
        "venue": "Medicina 61(9):1707",
        "year": 2025,
        "licence": "CC BY 4.0",
    },
    {
        "doc_id": "madinah2025",
        "file": "healthcare-13-00367.pdf",
        "url": "https://www.mdpi.com/2227-9032/13/4/367/pdf",
        "title": "Assessing the Spread of the Sport of Padel and the Prevalence and Causes of Injuries Among Padel Players",
        "authors": "see article",
        "venue": "Healthcare 13(4):367",
        "year": 2025,
        "licence": "CC BY 4.0",
    },
]

FIXED_WORDS, FIXED_OVERLAP = 150, 25          # design "fixed"
SECTION_MAX, SECTION_MIN = 260, 60            # design "section": target size and smallest piece kept alone


# --------------------------------------------------------------------------- download

def corpus_path(doc: dict) -> Path:
    """corpus/<file>, also accepting the publisher's versioned names (e.g. sensors-23-09908-v2.pdf)."""
    exact = CORPUS_DIR / doc["file"]
    if exact.is_file():
        return exact
    stem = Path(doc["file"]).stem
    matches = sorted(CORPUS_DIR.glob(f"{stem}*.pdf"))
    return matches[-1] if matches else exact


def download_corpus() -> None:
    """Fetch every missing PDF into corpus/. Some publishers block scripts; then the
    message says which file to save by hand (its name and URL)."""
    import httpx

    CORPUS_DIR.mkdir(exist_ok=True)
    headers = {"User-Agent": "Mozilla/5.0 (academic RAG assignment; padel corpus)"}
    for doc in DOCS:
        target = corpus_path(doc)
        if target.is_file() and target.stat().st_size > 10_000:
            continue
        for url in (doc["url"], doc.get("mirror")):
            if not url:
                continue
            try:
                r = httpx.get(url, headers=headers, follow_redirects=True, timeout=60)
                if r.status_code == 200 and r.content[:4] == b"%PDF":
                    target.write_bytes(r.content)
                    log(f"downloaded {doc['file']}")
                    break
                log(f"  {url} -> HTTP {r.status_code}, not a PDF")
            except httpx.HTTPError as error:
                log(f"  {url} -> {type(error).__name__}")
        else:
            log(f"Could not download {doc['file']}. Save {doc['url']} as corpus/{doc['file']} by hand.")


# --------------------------------------------------------------------------- extract & clean

def extract_pages(path: Path) -> list[str]:
    """Raw text per page. PDFs page by page; .txt/.md/.html as a single 'page'."""
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        from pypdf import PdfReader

        return [page.extract_text() or "" for page in PdfReader(str(path)).pages]
    if suffix in (".html", ".htm"):
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(path.read_text(encoding="utf-8", errors="replace"), "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header", "sup", "table"]):
            tag.decompose()
        return [soup.get_text("\n")]
    if suffix in (".txt", ".md"):
        return [path.read_text(encoding="utf-8", errors="replace")]
    raise ValueError(f"Unsupported file type {suffix!r}; use .pdf, .txt, .md or .html")


# Lines that are page furniture, not content (journal running heads, licence boxes, margins).
_FURNITURE = [
    re.compile(p, re.I)
    for p in (
        r"^(sensors|sports|medicina|healthcare|appl\. sci\.|int\.? j\.? environ\.? res\.? public health|ijerph)\s+\d{4}\s*,\s*\d+\s*,\s*(\d+|x)(\s+(for peer review\s+)?\d+\s+of\s+\d+)?$",
        r"^\d+\s+of\s+\d+$",
        r"^https?://(doi\.org|www\.mdpi\.com)\S*$",
        r"^www\.mdpi\.com/journal/\S+$",
        r"^(citation|academic editor|received|revised|accepted|published|copyright|licensee)\b.*",
        r"^publisher.s note\b.*",
        r"^.{0,60}\bbmj open sport (&|and) exerc(ise)? med\b.*\d{4}.*$",
        r"^bmj open sport & exercise medicine$",
        r"^open access$",
        r"^\d{1,3}$",  # bare page numbers
        r"^downloaded from https?://.*$",
        r"^protected by copyright.*$",
        r"^.*\b(sensors|sports|medicina|healthcare|appl\. sci\.|int\. j\. environ\. res\. public health)\s+\d{4},\s*\d+,\s*\d+\.?\s*https://doi\.org.*$",
        r"^\d{0,2}\s*dahmen j, et al\. bmj open sp ex med.*$",
        r"^bmj open sport & exercise medicine: first published as.*$",
        r"^figure \d+\.?\s.*$",       # figure captions: the figures themselves are not in the text
        r"^.*\bx for peer review\b.*$",  # leftover review-version page headers
        r"^(/gid\d+)+$",               # unmapped font glyphs (journal logo)
    )
]

# Back matter we drop: from the first of these headings near the end of the paper to the end.
_BACKMATTER = re.compile(
    r"^\s*(references|author contributions|funding|institutional review board statement|"
    r"informed consent statement|data availability statement|conflicts? of interest|acknowledg(e)?ments|"
    r"contributors|competing interests|patient consent for publication|provenance and peer review|"
    r"supplementary materials?|author affiliations)\s*(:.*)?$",
    re.I,
)


def _clean_line_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)           # ligatures: "ﬁ" -> "fi"
    text = text.replace("­", "")                     # soft hyphens
    text = re.sub(r"[ \t]+", " ", text)
    return text


def _norm(s: str) -> str:
    return re.sub(r"[^a-z0-9]", "", s.lower())


def _garbled(s: str) -> bool:
    """Equations extracted as private-use / Tamil-looking glyphs, e.g. 'Vൌ ா௡௘௥௚௬'."""
    letters = [c for c in s if not c.isspace()]
    return bool(letters) and sum(ord(c) > 0x2FF for c in letters) / len(letters) > 0.3


def clean_pages(pages: list[str]) -> list[str]:
    """Clean each page and cut the back matter (references, funding...), keeping page numbers.

    Some PDFs (the MDPI '-v2' files) carry the text two or three times in overlapping layers, each
    wrapped differently. A line is dropped when its letters-and-digits-only form already occurs in
    everything kept so far: that comparison ignores where lines break, so re-wrapped copies match.
    """
    cleaned: list[str] = []
    seen = ""                 # normalised text of every line kept so far (whole document)
    seen_headings: set[str] = set()
    cut = False
    for page_no, raw in enumerate(pages, 1):
        if cut:
            cleaned.append("")
            continue
        kept: list[str] = []
        for line in _clean_line_text(raw).split("\n"):
            s = line.strip()
            if not s:
                kept.append("")
                continue
            if any(p.match(s) for p in _FURNITURE) or _garbled(s):
                continue
            # Back matter only counts after the first third of the document (not a "Funding" word in a margin box).
            if _BACKMATTER.match(s) and page_no > max(2, len(pages) // 3):
                cut = True
                break
            n = _norm(s)
            if heading_of(s):
                if n in seen_headings:
                    continue
                seen_headings.add(n)
            elif len(n) >= 15 and n in seen:
                continue
            seen += n
            kept.append(s)
        text = "\n".join(kept)
        # Re-join words hyphenated across line breaks: "manufactur-\ning" -> "manufacturing".
        text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)
        # BMJ's extractor puts a space after hyphens: "fast- paced" -> "fast-paced".
        text = re.sub(r"(\w)- (?=[a-z])", r"\1-", text)
        cleaned.append(text)
    return cleaned


# --------------------------------------------------------------------------- sections

_NUMBERED = re.compile(r"^(\d{1,2}(?:\.\d{1,2}){0,2})\.?\s+([A-Z][A-Za-z0-9 ,:;&()'/\-–]{2,90})$")
_PLAIN = re.compile(
    r"^(abstract|introduction|methods?|materials and methods|results|discussion|conclusions?|"
    r"limitations|strengths and limitations|practical applications|future research|background|"
    r"what is already known on this topic|what this study adds|how this study might affect research, practice or policy)$",
    re.I,
)


def heading_of(line: str) -> str | None:
    """Return a section heading if this line is one, else None."""
    s = line.strip()
    if len(s.split()) > 14 or s.endswith((".", ",", ";")):
        return None
    m = _NUMBERED.match(s)
    if m and not re.search(r"\d{2,}", m.group(2)):   # "3 Results" yes, "2 of 16" / "12 players" no
        return f"{m.group(1)} {m.group(2).strip()}"
    if _PLAIN.match(s):
        return s.title() if s.isupper() else s
    return None


def paragraphs_with_pages(pages: list[str]) -> list[tuple[int, str | None, str]]:
    """(page, heading-or-None, paragraph text). A heading line becomes its own entry."""
    out: list[tuple[int, str | None, str]] = []
    for page_no, text in enumerate(pages, 1):
        buf: list[str] = []

        def flush():
            if buf:
                out.append((page_no, None, " ".join(buf)))
                buf.clear()

        for line in text.split("\n"):
            s = line.strip()
            if not s:
                flush()
                continue
            h = heading_of(s)
            if h:
                flush()
                out.append((page_no, h, ""))
                continue
            buf.append(s)
        flush()
    return out


# --------------------------------------------------------------------------- chunking

def _meta_for(path: Path) -> dict:
    for doc in DOCS:
        if doc["file"] == path.name or path.name.startswith(Path(doc["file"]).stem + "-v"):
            return {**doc, "origin": "corpus"}
    stem = re.sub(r"[^a-z0-9]+", "_", path.stem.lower()).strip("_")[:40] or "document"
    return {"doc_id": stem, "file": path.name, "url": "", "title": path.stem, "authors": "",
            "venue": "", "year": 0, "licence": "unknown (added by user)", "origin": "added"}


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _chunk_id(design: str, doc_id: str, n: int, text: str) -> str:
    return f"{design}:{doc_id}:{n:04d}:{hashlib.sha1(text.encode()).hexdigest()[:10]}"


def chunk_file(path: Path, design: str = rag.PRODUCTION["design"]) -> list[dict]:
    """Extract, clean and chunk one file. Each chunk: id, text, and metadata for citations."""
    path = Path(path)
    meta = _meta_for(path)
    pages = clean_pages(extract_pages(path))
    sha = file_sha256(path)
    base = {
        "doc_id": meta["doc_id"], "title": meta["title"], "year": int(meta["year"] or 0),
        "source_file": path.name, "url": meta["url"], "licence": meta["licence"],
        "origin": meta["origin"], "file_sha256": sha, "design": design,
    }
    if design == "fixed":
        pieces = _fixed_chunks(pages)
    elif design == "section":
        pieces = _section_chunks(pages)
    else:
        raise ValueError(f"unknown design {design!r}")
    chunks = []
    for n, (text, p0, p1, section) in enumerate(pieces):
        chunks.append({
            "id": _chunk_id(design, meta["doc_id"], n, text),
            "text": text,
            "meta": {**base, "page_start": p0, "page_end": p1, "section": section or "front matter",
                     "chunk_index": n, "words": len(text.split())},
        })
    return chunks


def _fixed_chunks(pages: list[str]) -> list[tuple[str, int, int, str]]:
    """Design A: 150-word sliding windows (25-word overlap) over the whole text, ignoring structure."""
    words: list[tuple[str, int, str]] = []  # (word, page, current section)
    section = "front matter"
    for page, heading, para in paragraphs_with_pages(pages):
        if heading:
            section = heading
            words.extend((w, page, section) for w in heading.split())
            continue
        words.extend((w, page, section) for w in para.split())
    out = []
    step = FIXED_WORDS - FIXED_OVERLAP
    for start in range(0, max(len(words) - FIXED_OVERLAP, 1), step):
        window = words[start:start + FIXED_WORDS]
        if not window:
            break
        out.append((" ".join(w for w, _, _ in window), window[0][1], window[-1][1], window[0][2]))
    return out


_SENT = re.compile(r"(?<=[.!?])\s+(?=[A-Z(\[])")


def _section_chunks(pages: list[str]) -> list[tuple[str, int, int, str]]:
    """Design B: split at section headings, then pack whole paragraphs (sentences, if a paragraph
    is too long) up to ~260 words. A chunk never crosses a section boundary."""
    sections: list[tuple[str, list[tuple[int, str]]]] = [("front matter", [])]
    for page, heading, para in paragraphs_with_pages(pages):
        if heading:
            sections.append((heading, []))
        elif para:
            sections[-1][1].append((page, para))

    out: list[tuple[str, int, int, str]] = []
    for name, paras in sections:
        units: list[tuple[int, str]] = []
        for page, para in paras:
            if len(para.split()) <= SECTION_MAX:
                units.append((page, para))
            else:
                units.extend((page, s) for s in _SENT.split(para))
        buf: list[tuple[int, str]] = []
        count = 0
        for page, unit in units:
            n = len(unit.split())
            if buf and count + n > SECTION_MAX:
                out.append((" ".join(u for _, u in buf), buf[0][0], buf[-1][0], name))
                buf, count = [], 0
            buf.append((page, unit))
            count += n
        if buf:
            # A short tail is merged into the previous chunk of the same section instead of standing alone.
            if count < SECTION_MIN and out and out[-1][3] == name:
                text, p0, _, _ = out.pop()
                out.append((text + " " + " ".join(u for _, u in buf), p0, buf[-1][0], name))
            else:
                out.append((" ".join(u for _, u in buf), buf[0][0], buf[-1][0], name))
    return [c for c in out if len(c[0].split()) >= 15]


# --------------------------------------------------------------------------- embed & store

def _embed_input(chunk: dict) -> str:
    m = chunk["meta"]
    body = chunk["text"] if m["design"] == "fixed" else f"{m['section']}\n{chunk['text']}"
    return rag.doc_prompt(m["title"], body)


def embed_and_store(chunks: list[dict], design: str) -> int:
    """Embed the chunks that have no saved vector yet and add them to the design's collection,
    one batch at a time (a crash or the daily quota loses at most one batch). Returns how many were embedded."""
    col = rag.collection(design)
    ids = [c["id"] for c in chunks]
    existing: set[str] = set()
    for i in range(0, len(ids), 500):
        existing.update(col.get(ids=ids[i:i + 500], include=[])["ids"])
    todo = [c for c in chunks if c["id"] not in existing]
    for i in range(0, len(todo), rag.EMBED_BATCH):
        batch = todo[i:i + rag.EMBED_BATCH]
        vectors = rag.embed_texts([_embed_input(c) for c in batch])
        col.add(
            ids=[c["id"] for c in batch],
            embeddings=vectors,
            documents=[c["text"] for c in batch],
            metadatas=[c["meta"] for c in batch],
        )
        log(f"  [{design}] embedded {min(i + rag.EMBED_BATCH, len(todo))}/{len(todo)}")
    return len(todo)


def remove_document(doc_id: str, design: str) -> int:
    col = rag.collection(design)
    old = col.get(where={"doc_id": doc_id}, include=[])["ids"]
    if old:
        col.delete(ids=old)
    return len(old)


def index_file(path: Path, design: str = rag.PRODUCTION["design"]) -> dict:
    """The add-document pipeline for one file (used by server.py).

    Already indexed with identical bytes -> nothing happens.
    Same document id but different bytes (a new version) -> old chunks are replaced.
    """
    path = Path(path).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"No file at {path}")
    sha = file_sha256(path)
    col = rag.collection(design)
    same = col.get(where={"file_sha256": sha}, include=["metadatas"], limit=1)
    if same["ids"]:
        m = same["metadatas"][0]
        n = len(col.get(where={"file_sha256": sha}, include=[])["ids"])
        return {"status": "already_indexed", "doc_id": m["doc_id"], "chunks": n, "embedded": 0}
    chunks = chunk_file(path, design)
    if not chunks:
        raise ValueError(f"No text could be extracted from {path.name}")
    doc_id = chunks[0]["meta"]["doc_id"]
    replaced = remove_document(doc_id, design)
    embedded = embed_and_store(chunks, design)
    registry = rag.load_registry()
    meta = chunks[0]["meta"]
    registry[doc_id] = {
        "title": meta["title"], "file": path.name, "url": meta["url"], "licence": meta["licence"],
        "origin": meta["origin"], "sha256": sha, "words": sum(c["meta"]["words"] for c in chunks),
        "chunks": {design: len(chunks)},
    }
    rag.save_registry(registry)
    return {"status": "replaced" if replaced else "added", "doc_id": doc_id, "chunks": len(chunks),
            "embedded": embedded, "replaced_chunks": replaced}


# --------------------------------------------------------------------------- main

def main() -> None:
    download_corpus()
    registry = rag.load_registry()
    total_words, total_new = 0, 0
    for doc in DOCS:
        path = corpus_path(doc)
        if not path.is_file():
            if doc["doc_id"] in registry:
                log(f"{doc['file']} not in corpus/, but already indexed: keeping the saved chunks.")
                total_words += registry[doc["doc_id"]]["words"]
                continue
            sys.exit(f"Missing corpus/{doc['file']} and it is not indexed yet. Download {doc['url']}")
        counts = {}
        for design in rag.DESIGNS:
            chunks = chunk_file(path, design)
            counts[design] = len(chunks)
            total_new += embed_and_store(chunks, design)
        words = sum(len(p.split()) for p in clean_pages(extract_pages(path)))
        raw_words = sum(len(p.split()) for p in extract_pages(path))
        total_words += words
        registry[doc["doc_id"]] = {
            "title": doc["title"], "file": doc["file"], "url": doc["url"], "licence": doc["licence"],
            "year": doc["year"], "venue": doc["venue"], "origin": "corpus", "sha256": file_sha256(path),
            "words": words, "raw_words": raw_words, "chunks": counts,
        }
        rag.save_registry(registry)
        print(f"{doc['doc_id']:<12} {raw_words:>6} words raw, {words:>6} after cleaning, chunks {counts}")
    print(f"\nCorpus: {len(DOCS)} documents, {total_words} words after cleaning. Newly embedded chunks: {total_new}.")
    for design in rag.DESIGNS:
        print(f"  collection padel_{design}: {rag.collection(design).count()} chunks")


if __name__ == "__main__":
    # Windows consoles (cp1252) can't print characters like "≥" or "χ" from the papers: replace them instead of crashing.
    for _stream in (sys.stdout, sys.stderr):
        try:
            _stream.reconfigure(errors="replace")
        except AttributeError:
            pass
    main()
