"""
Assignment 3: build the index (`uv run python main.py index`).

Download the corpus into corpus/ (git-ignored), extract, clean and chunk it with source
and location metadata, embed with Gemini and store everything in index/ (ChromaDB).
Vectors are saved as they arrive and only chunks without a saved vector are embedded.

The per-file steps are plain functions (`chunk_file`, `embed_and_store`, `index_file`):
server.py's add_document tool imports them, so the pipeline exists only once.

Two chunking designs are built so that evaluate.py can compare them:
  fixed      sliding window of ~WINDOW words with OVERLAP words of overlap
  structure  paragraphs merged inside one section, up to MAX_WORDS, never across a heading
"""

from __future__ import annotations

import hashlib
import json
import re
import statistics
import sys
from dataclasses import dataclass
from pathlib import Path

import rag
from rag import Chunk

# --------------------------------------------------------------------------- corpus
# >>> EDIT: one entry per document (>= 3 documents, >= 50,000 words in total). <<<
# `name` is the file name in corpus/ and is also what `expected_source` in
# eval/questions.csv must say. Public documents only, with a licence that allows this use.
CORPUS: list[dict] = [
    {"name": "lau.pdf", "url": "https://boe.es/buscar/pdf/1994/BOE-A-1994-26003-consolidado.pdf", "date": "2026-11-21", "licence": "BOE, reuse with attribution"},
    {"name": "ley_vivienda.pdf", "url": "https://www.boe.es/buscar/pdf/2023/BOE-A-2023-12203-consolidado.pdf", "date": "2026-11-21", "licence": "BOE, reuse with attribution"},
    {"name": "lph.pdf", "url": "https://www.boe.es/buscar/pdf/1960/BOE-A-1960-10906-consolidado.pdf", "date": "2026-11-21", "licence": "BOE, reuse with attribution"},
]

ALLOWED_SUFFIXES = {".pdf", ".html", ".htm", ".txt", ".md"}
MAX_FILE_MB = 50

# ------------------------------------------------------------------ chunk settings
WINDOW = 200  # fixed design: words per window
OVERLAP = 40  # fixed design: words shared by consecutive windows
MAX_WORDS = 250  # structure design: soft cap per chunk
MIN_WORDS = 40  # structure design: a smaller trailing piece is merged into the previous chunk

HEADING_RE = re.compile(
    r"^(?:(?i:art[ií]culo|art\.|article|cap[ií]tulo|chapter|secci[oó]n|section|t[ií]tulo|title|"
    r"parte|part|anexo|annex|disposici[oó]n|recital)\s+[\dIVXLCivxlc\.]+[^\n]{0,80}"
    r"|\d{1,2}(?:\.\d{1,2}){0,3}\.?\s+[A-ZÁÉÍÓÚÑ¿][^\n]{2,80}"
    r"|[A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ0-9 ,:;\-–()/]{6,80})$"
)


# --------------------------------------------------------------------- extraction
@dataclass
class Para:
    text: str
    page: int | None  # None for HTML / text
    section: str


def file_sha1(path: Path) -> str:
    return hashlib.sha1(path.read_bytes()).hexdigest()


def _clean(text: str) -> str:
    text = text.replace("­", "")  # soft hyphen
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)  # re-join words hyphenated at line ends
    text = re.sub(r"[ \t ]+", " ", text)
    return text


def _is_heading(line: str) -> bool:
    line = line.strip()
    return 3 <= len(line) <= 100 and bool(HEADING_RE.match(line))


def _lines_to_paras(lines: list[str], page: int | None, section: str) -> tuple[list[Para], str]:
    """Group visual lines into paragraphs and track the current section heading.

    A paragraph ends at a blank line, before a heading, or after a line that ends a sentence
    and is clearly shorter than a full line (the last line of a wrapped paragraph).
    """
    lengths = [len(l) for l in lines if len(l.strip()) > 20]
    typical = statistics.median(lengths) if lengths else 80
    paras: list[Para] = []
    buf: list[str] = []

    def flush():
        if buf:
            text = " ".join(buf).strip()
            if text:
                paras.append(Para(text, page, section))
            buf.clear()

    for raw in lines:
        line = raw.strip()
        if not line:
            flush()
            continue
        if _is_heading(line):
            flush()
            section = line
            continue
        buf.append(line)
        if line.endswith((".", ":", ";")) and len(line) < 0.75 * typical:
            flush()
    flush()
    return paras, section


def _extract_pdf(path: Path) -> list[Para]:
    from pypdf import PdfReader

    reader = PdfReader(str(path))
    pages = [(_clean(p.extract_text() or "")).split("\n") for p in reader.pages]
    # Repeated headers/footers ("Ley 29/1994 ... BOE núm. 282 ...") pollute chunks: drop short
    # lines that appear (digits ignored) on at least 40% of the pages, and bare page numbers.
    if len(pages) >= 5:
        counts: dict[str, int] = {}
        for lines in pages:
            for key in {re.sub(r"\d+", "#", l.strip()) for l in lines if 0 < len(l.strip()) < 100}:
                counts[key] = counts.get(key, 0) + 1
        boiler = {k for k, c in counts.items() if c >= 0.4 * len(pages)}
    else:
        boiler = set()
    paras: list[Para] = []
    section = ""
    for number, lines in enumerate(pages, 1):
        kept = [
            l
            for l in lines
            if re.sub(r"\d+", "#", l.strip()) not in boiler
            and not re.fullmatch(r"\s*(?:page|página|pág\.?)?\s*\d+(?:\s*(?:of|de|/)\s*\d+)?\s*", l, re.IGNORECASE)
        ]
        page_paras, section = _lines_to_paras(kept, number, section)
        paras.extend(page_paras)
    return paras


def _extract_html(path: Path) -> list[Para]:
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(path.read_bytes(), "html.parser")
    for tag in soup(["script", "style", "nav", "header", "footer", "aside", "form", "noscript"]):
        tag.decompose()
    root = soup.find("main") or soup.body or soup
    paras: list[Para] = []
    section = ""
    for el in root.find_all(["h1", "h2", "h3", "h4", "p", "li", "blockquote", "td"]):
        text = _clean(el.get_text(" ", strip=True)).strip()
        if not text:
            continue
        if el.name.startswith("h"):
            section = text[:100]
        elif len(text.split()) >= 5:
            paras.append(Para(text, None, section))
    return paras


def _extract_text(path: Path) -> list[Para]:
    text = _clean(path.read_text(encoding="utf-8", errors="replace"))
    paras: list[Para] = []
    section = ""
    for block in re.split(r"\n\s*\n", text):
        lines = [l for l in block.split("\n") if l.strip()]
        if not lines:
            continue
        first = lines[0].strip()
        if first.startswith("#") or _is_heading(first):
            section = first.lstrip("# ").strip()[:100]
            lines = lines[1:]
        body = " ".join(l.strip() for l in lines).strip()
        if body:
            paras.append(Para(body, None, section))
    return paras


def extract_paragraphs(path: Path) -> list[Para]:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return _extract_pdf(path)
    if suffix in {".html", ".htm"}:
        return _extract_html(path)
    if suffix in {".txt", ".md"}:
        return _extract_text(path)
    raise ValueError(f"Unsupported file type {suffix!r}. Allowed: {', '.join(sorted(ALLOWED_SUFFIXES))}")


# ------------------------------------------------------------------------ chunking
def _location(page_start: int | None, page_end: int | None, section: str) -> str:
    if page_start is not None:
        return f"p.{page_start}" if page_end in (None, page_start) else f"p.{page_start}-{page_end}"
    return section or "document"


def _make_chunk(design: str, source: str, idx: int, text: str, ps, pe, section: str, sha: str) -> Chunk:
    cid = hashlib.sha1(f"{design}|{source}|{idx}|{text}".encode("utf-8")).hexdigest()[:20]
    return Chunk(cid, design, source, _location(ps, pe, section), section, text, ps, pe, sha)


def _chunks_fixed(paras: list[Para], source: str, sha: str) -> list[Chunk]:
    words: list[tuple[str, int | None, str]] = []
    for p in paras:
        words.extend((w, p.page, p.section) for w in p.text.split())
    chunks: list[Chunk] = []
    step = max(WINDOW - OVERLAP, 1)
    for idx, start in enumerate(range(0, len(words), step)):
        window = words[start : start + WINDOW]
        if len(window) < MIN_WORDS and chunks:  # tiny tail: already covered by the overlap
            break
        pages = [p for _, p, _ in window if p is not None]
        ps, pe = (min(pages), max(pages)) if pages else (None, None)
        text = " ".join(w for w, _, _ in window)
        chunks.append(_make_chunk("fixed", source, idx, text, ps, pe, window[0][2], sha))
        if start + WINDOW >= len(words):
            break
    return chunks


def _split_long(text: str) -> list[str]:
    """A paragraph longer than MAX_WORDS is cut at sentence ends."""
    sentences = re.split(r"(?<=[.!?;])\s+", text)
    pieces, cur = [], []
    for s in sentences:
        if cur and sum(len(x.split()) for x in cur) + len(s.split()) > MAX_WORDS:
            pieces.append(" ".join(cur))
            cur = []
        cur.append(s)
    if cur:
        pieces.append(" ".join(cur))
    return pieces


def _chunks_structure(paras: list[Para], source: str, sha: str) -> list[Chunk]:
    groups: list[list[Para]] = []
    for p in paras:
        for piece in _split_long(p.text) if len(p.text.split()) > MAX_WORDS else [p.text]:
            part = Para(piece, p.page, p.section)
            n = len(piece.split())
            if (
                groups
                and groups[-1][-1].section == part.section
                and sum(len(x.text.split()) for x in groups[-1]) + n <= MAX_WORDS
            ):
                groups[-1].append(part)
            else:
                groups.append([part])
    # merge a tiny group into the previous one when they share a section
    merged: list[list[Para]] = []
    for g in groups:
        size = sum(len(x.text.split()) for x in g)
        if merged and size < MIN_WORDS and merged[-1][-1].section == g[0].section:
            merged[-1].extend(g)
        else:
            merged.append(g)
    chunks = []
    for idx, g in enumerate(merged):
        pages = [x.page for x in g if x.page is not None]
        ps, pe = (min(pages), max(pages)) if pages else (None, None)
        chunks.append(_make_chunk("structure", source, idx, " ".join(x.text for x in g), ps, pe, g[0].section, sha))
    return chunks


def chunk_file(path: str | Path, design: str, sha: str | None = None) -> list[Chunk]:
    """Extract, clean and chunk one file. No API calls."""
    path = Path(path)
    sha = sha or file_sha1(path)
    paras = extract_paragraphs(path)
    if design == "fixed":
        return _chunks_fixed(paras, path.name, sha)
    if design == "structure":
        return _chunks_structure(paras, path.name, sha)
    raise ValueError(f"unknown design {design!r}")


# ------------------------------------------------------------------ embed and store
def embed_and_store(chunks: list[Chunk], design: str) -> int:
    """Embed chunks that have no saved vector, upsert everything into Chroma. Returns new embeddings."""
    if not chunks:
        return 0
    before = rag.EMBEDDED_THIS_RUN
    col = rag.get_collection(design)
    for start in range(0, len(chunks), 100):  # save to Chroma in slices: a crash keeps the finished ones
        part = chunks[start : start + 100]
        vectors = rag.embed_texts([rag.doc_prompt(c.text) for c in part], "doc")
        col.upsert(
            ids=[c.id for c in part],
            embeddings=vectors.tolist(),
            documents=[c.text for c in part],
            metadatas=[c.metadata() for c in part],
        )
    return rag.EMBEDDED_THIS_RUN - before


def validate_path(path: str | Path) -> Path:
    p = Path(path).expanduser()
    if not p.is_absolute():
        p = rag.ROOT / p
    p = p.resolve()
    if not p.is_file():
        raise ValueError(f"No such file: {path}")
    if p.suffix.lower() not in ALLOWED_SUFFIXES:
        raise ValueError(f"Unsupported file type {p.suffix!r}. Allowed: {', '.join(sorted(ALLOWED_SUFFIXES))}")
    if p.stat().st_size > MAX_FILE_MB * 1_000_000:
        raise ValueError(f"File is larger than {MAX_FILE_MB} MB.")
    return p


def index_file(path: str | Path, designs: tuple[str, ...] = rag.DESIGNS) -> str:
    """The whole pipeline for one file, with the duplicate policy:

    - identical content already indexed (under any name)  -> skip, nothing is embedded;
    - same file name, different content                   -> replace: old chunks are deleted first;
    - otherwise                                           -> add.
    """
    p = validate_path(path)
    sha = file_sha1(p)
    report = []
    for design in designs:
        col = rag.get_collection(design)
        same = col.get(where={"doc_sha1": sha}, limit=1, include=["metadatas"])
        if same["ids"]:
            report.append(
                f"[{design}] already indexed as '{same['metadatas'][0]['source']}' (identical content): nothing changed."
            )
            continue
        replaced = bool(col.get(where={"source": p.name}, limit=1)["ids"])
        if replaced:
            col.delete(where={"source": p.name})
        chunks = chunk_file(p, design, sha)
        if not chunks:
            report.append(f"[{design}] no text could be extracted from '{p.name}'; nothing added.")
            continue
        new = embed_and_store(chunks, design)
        words = sum(len(c.text.split()) for c in chunks)
        report.append(
            f"[{design}] {'replaced' if replaced else 'added'} '{p.name}': {len(chunks)} chunks, "
            f"{words} words, {new} new embeddings."
        )
    return "\n".join(report)


# ------------------------------------------------------------------------- stage
def download_corpus() -> None:
    import httpx

    rag.CORPUS_DIR.mkdir(exist_ok=True)
    for doc in CORPUS:
        target = rag.CORPUS_DIR / doc["name"]
        if target.exists():
            continue
        rag.log(f"downloading {doc['url']}")
        r = httpx.get(doc["url"], follow_redirects=True, timeout=120, headers={"User-Agent": "Mozilla/5.0 (course project)"})
        r.raise_for_status()
        target.write_bytes(r.content)


def dry_run(files: list[Path]) -> None:
    """Chunk counts per design WITHOUT calling the API: tune WINDOW/MAX_WORDS here, not on the quota."""
    totals = {d: 0 for d in rag.DESIGNS}
    for f in files:
        words = sum(len(p.text.split()) for p in extract_paragraphs(f))
        counts = {d: len(chunk_file(f, d)) for d in rag.DESIGNS}
        for d in rag.DESIGNS:
            totals[d] += counts[d]
        print(f"{f.name}: {words:,} words, chunks {counts}")
    print(f"total chunks (= texts to embed, quota ~1,000/day): {totals}")


def main() -> None:
    download_corpus()
    files = sorted(p for p in rag.CORPUS_DIR.glob("*") if p.suffix.lower() in ALLOWED_SUFFIXES)
    if not files:
        sys.exit("corpus/ is empty. Fill CORPUS in index.py (or drop files into corpus/) and run again.")
    if "--dry-run" in sys.argv:
        return dry_run(files)
    manifest, total_words = [], 0
    meta = {d["name"]: d for d in CORPUS}
    try:
        for f in files:
            print(f"\n{f.name}")
            print(index_file(f, rag.DESIGNS))
            words = sum(len(p.text.split()) for p in extract_paragraphs(f))
            total_words += words
            manifest.append({**meta.get(f.name, {"name": f.name}), "words": words, "sha1": file_sha1(f)})
    except rag.QuotaExhausted as error:
        sys.exit(f"\nStopped: {error}")
    (rag.INDEX_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"\n{len(files)} documents, {total_words:,} words in total (target: >= 3 documents, >= 50,000 words).")
    for design in rag.DESIGNS:
        n = rag.get_collection(design).count()
        print(f"design '{design}': {n} chunks")
    print(f"texts sent to the embedding API in this run: {rag.EMBEDDED_THIS_RUN}")
    if len(files) < 3 or total_words < 50_000:
        print("WARNING: the corpus is below the minimum size of the brief.")


if __name__ == "__main__":
    main()
