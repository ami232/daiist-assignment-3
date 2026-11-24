"""
Assignment 3: build the index (`main.py index`).

1. download   the three EU legal texts into corpus/ (git-ignored) from the EU
              Publications Office (Cellar), the official machine-readable
              source behind EUR-Lex;
2. extract    the text as lines (HTML, PDF or plain text) and clean it
              (footnotes, amendment markers, running headers, signatures);
3. chunk      it in two designs:
                structured - one chunk per article / clause, long articles split
                             at paragraph boundaries, consecutive recitals grouped;
                fixed      - 400-word windows with 50 words of overlap, ignoring
                             the structure;
              every chunk carries its document, location (article, recital,
              clause, annex; page for PDFs) and a ready-made citation;
4. embed      each chunk with Gemini and store it in index/chroma (ChromaDB),
              saving after every batch and skipping chunks that already have
              a vector, so a crash or the daily quota loses nothing.

server.py's add_document tool imports `add_file` from here.
"""

from __future__ import annotations

import hashlib
import re
import sys
import urllib.request
from pathlib import Path

from rag import DESIGNS, EMBED_BATCH, QuotaExhausted, collection, embed, log

ROOT = Path(__file__).resolve().parent
CORPUS = ROOT / "corpus"

SOURCES = [
    {
        "doc_id": "GDPR",
        "title": "Regulation (EU) 2016/679 (General Data Protection Regulation)",
        "celex": "32016R0679",
        "file": "GDPR_2016_679.html",
        "date": "2016-04-27",
    },
    {
        "doc_id": "ePrivacy",
        "title": "Directive 2002/58/EC (ePrivacy Directive), consolidated text of 19.12.2009",
        "celex": "02002L0058-20091219",
        "file": "ePrivacy_2002_58_consolidated.html",
        "date": "2009-12-19",
    },
    {
        "doc_id": "SCC 2021/914",
        "title": "Commission Implementing Decision (EU) 2021/914 on standard contractual clauses for transfers to third countries",
        "celex": "32021D0914",
        "file": "SCC_transfers_2021_914.html",
        "date": "2021-06-04",
    },
]
CELLAR = "https://publications.europa.eu/resource/celex/{celex}"
EURLEX = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:{celex}"

STRUCT_MAX_WORDS = 350      # split longer articles at paragraph boundaries
RECITAL_GROUP_WORDS = 300   # group consecutive recitals up to this size
FIXED_WORDS, FIXED_OVERLAP = 400, 50


# ================================================================ download

def download_corpus() -> list[Path]:
    CORPUS.mkdir(exist_ok=True)
    paths = []
    for src in SOURCES:
        path = CORPUS / src["file"]
        if not path.is_file() or path.stat().st_size < 10_000:
            log(f"downloading {src['doc_id']} ({src['celex']}) ...")
            request = urllib.request.Request(
                CELLAR.format(celex=src["celex"]),
                headers={"Accept": "application/xhtml+xml", "Accept-Language": "eng", "User-Agent": "daiist-a3-indexer"},
            )
            with urllib.request.urlopen(request, timeout=120) as response:
                path.write_bytes(response.read())
        paths.append(path)
    return paths


def source_for(path: Path) -> dict:
    """Metadata for a file: one of the three SOURCES, or derived from the file name."""
    for src in SOURCES:
        if path.name == src["file"]:
            return src
    stem = path.stem
    match = re.search(r"(20\d\d)_(\d{3,4})", stem)
    doc_id = f"{stem.split('_')[0]} {match.group(1)}/{match.group(2)}" if match else stem
    return {"doc_id": doc_id, "title": stem.replace("_", " "), "celex": "", "file": path.name, "date": ""}


# ================================================================ extract + clean

BLOCK_TAGS = ["p", "td", "h1", "h2", "h3", "h4", "li", "div"]
DROP_CLASSES = re.compile(r"note|footnote|modref|arrow|superscript|oj-super|hd-|signatory|separator|doc-end")
MARKER = re.compile(r"^(\(\d+\)|\([a-z]{1,4}\)|\d+\.|–|—|-|•)$")


def clean_line(text: str) -> str:
    text = text.replace("\xa0", " ").replace(" ", " ")
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"▼\w+|►\w+|◄", "", text).strip()      # amendment markers in consolidated texts
    return text


def extract_html(path: Path) -> list[tuple[str, int | None]]:
    """Lines of text from an EUR-Lex HTML/XHTML file, with footnotes and markers removed."""
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(path.read_text(encoding="utf-8", errors="ignore"), "html.parser")
    for tag in soup(["script", "style", "head"]):
        tag.decompose()
    for tag in soup.find_all(class_=DROP_CLASSES):
        tag.decompose()
    for tag in soup.find_all("a", href=re.compile(r"#(ntr|ntc)")):  # footnote call-outs like "(1)"
        tag.decompose()
    lines = []
    for el in soup.find_all(BLOCK_TAGS):
        if el.find(BLOCK_TAGS):     # only leaf blocks, so nothing is read twice
            continue
        text = clean_line(el.get_text(" "))
        if text:
            lines.append((text, None))
    return lines


RUNNING_HEADER = re.compile(r"(Official Journal of the European Union|^L \d+/\d+$|^EN$|^\d{1,2}\.\d{1,2}\.\d{4}$)")


def extract_pdf(path: Path) -> list[tuple[str, int | None]]:
    """Lines of text from a PDF, each with its page number; running headers dropped."""
    from pypdf import PdfReader

    lines = []
    for page_no, page in enumerate(PdfReader(str(path)).pages, 1):
        for raw in (page.extract_text() or "").splitlines():
            text = clean_line(raw)
            if not text or RUNNING_HEADER.search(text) and len(text.split()) < 14:
                continue
            if re.fullmatch(r"\(\d+\) ?OJ .*", text):   # footnote lines
                continue
            lines.append((text, page_no))
    return lines


def extract_text(path: Path) -> list[tuple[str, int | None]]:
    return [(clean_line(t), None) for t in path.read_text(encoding="utf-8", errors="ignore").splitlines() if t.strip()]


def extract(path: Path) -> list[tuple[str, int | None]]:
    suffix = path.suffix.lower()
    if suffix in (".html", ".htm", ".xhtml", ".xml"):
        lines = extract_html(path)
    elif suffix == ".pdf":
        lines = extract_pdf(path)
    elif suffix in (".txt", ".md"):
        lines = extract_text(path)
    else:
        raise ValueError(f"Unsupported file type {suffix!r}: use .html, .xhtml, .pdf or .txt")
    return merge_markers(lines)


def merge_markers(lines):
    """Join list markers like "(a)" or recital numbers "(12)" that sit in their own table cell
    with the text that follows them, so a point never loses its number."""
    out = []
    pending = None
    for text, page in lines:
        if MARKER.fullmatch(text):
            pending = (text, page) if pending is None else (pending[0] + " " + text, pending[1])
            continue
        if pending:
            text, page = f"{pending[0]} {text}", pending[1] or page
            pending = None
        out.append((text, page))
    return out


# ================================================================ structure

RE_CHAPTER = re.compile(r"^CHAPTER ([IVXLC]+)$", re.I)
RE_SECTION = re.compile(r"^SECTION ([IVX]+|\d+)$", re.I)
RE_ARTICLE = re.compile(r"^Article ?(\d+[a-z]?)$")
RE_ANNEX = re.compile(r"^ANNEX ?([IVX]*)$")
RE_CLAUSE = re.compile(r"^Clause ?(\d+[a-z]?)(?: ?[-–] ?Optional)?$")   # PDFs lose spaces: "Clause7"
RE_MODULE = re.compile(r"^MODULE (ONE|TWO|THREE|FOUR)\b")
RE_RECITAL = re.compile(r"^\((\d+)\) (.+)")
RE_ADOPTED = re.compile(r"(HAVE|HAS) ADOPTED TH(IS|E FOLLOWING)", re.I)
RE_SIGNATURE = re.compile(r"^(Done at|This (Regulation|Decision|Directive) shall be binding|For the (European Parliament|Council|Commission))")


def is_title(text: str) -> bool:
    return len(text.split()) <= 18 and not text.endswith((".", ";", ":")) and not text[:1].isdigit()


def structure(lines) -> list[dict]:
    """Group lines into units (preamble, recital N, article N, annex clause N...) with their headings."""
    units = []
    state = {"chapter": "", "section": "", "annex": "", "zone": "preamble"}
    current = None
    expect_title = None

    def start(kind, number, page):
        nonlocal current
        loc = {
            "recital": f"Recital {number}",
            "article": f"Article {number}",
            "clause": f"{state['annex'] + ', ' if state['annex'] else ''}Clause {number}",
            "annex": state["annex"] or "Annex",
            "preamble": "Preamble",
        }[kind]
        current = {"kind": kind, "number": number, "location": loc, "title": "", "chapter": state["chapter"],
                   "section": state["section"], "lines": [], "page": page}
        units.append(current)

    start("preamble", "", None)
    for text, page in lines:
        if RE_SIGNATURE.match(text):
            state["zone"] = "signature"
            continue
        if state["zone"] == "signature" and not RE_ANNEX.match(text):
            continue                                  # signatures: names of office holders, dropped
        if expect_title:
            heading = any(r.match(text) for r in (RE_CHAPTER, RE_SECTION, RE_ARTICLE, RE_ANNEX, RE_CLAUSE))
            if is_title(text) and not heading:
                if expect_title == "chapter":
                    state["chapter"] += f" – {text}"
                elif expect_title == "section":
                    state["section"] += f" – {text}"
                else:
                    current["title"] = text
                expect_title = None
                continue
            expect_title = None
        if RE_ADOPTED.search(text):
            state["zone"] = "articles"
            continue
        if m := RE_CHAPTER.match(text):
            state.update(chapter=f"Chapter {m.group(1)}", section="")
            expect_title = "chapter"
            continue
        if m := RE_SECTION.match(text):
            state["section"] = f"Section {m.group(1)}"
            expect_title = "section"
            continue
        if m := RE_ANNEX.match(text):
            state.update(zone="annex", annex=f"Annex {m.group(1)}".strip(), chapter="", section="")
            start("annex", m.group(1), page)
            expect_title = "annex"
            continue
        if m := RE_ARTICLE.match(text):
            if state["zone"] == "preamble":
                state["zone"] = "articles"
            start("article", m.group(1), page)
            expect_title = "article"
            continue
        if state["zone"] == "annex" and (m := RE_CLAUSE.match(text)):
            start("clause", m.group(1), page)
            expect_title = "clause"
            continue
        if state["zone"] == "preamble" and (m := RE_RECITAL.match(text)):
            start("recital", m.group(1), page)
            current["lines"].append((m.group(2), page))
            continue
        current["lines"].append((text, page))
    return [u for u in units if u["lines"]]


# ================================================================ chunking

def chunk_id(doc_id: str, design: str, location: str, part: int, text: str) -> str:
    return hashlib.sha1(f"{design}|{doc_id}|{location}|{part}|{text}".encode()).hexdigest()[:20]


def words(text: str) -> int:
    return len(text.split())


def make_chunk(src, design, location, cite, header, text, part, page, extra=None) -> dict:
    meta = {
        "doc_id": src["doc_id"],
        "doc_title": src["title"],
        "file": src["file"],
        "design": design,
        "location": location,
        "cite": cite,
        "header": header,
        "part": part,
        "page": page or 0,
        "words": words(text),
    }
    meta.update(extra or {})
    return {"id": chunk_id(src["doc_id"], design, location, part, text), "text": text, "meta": meta}


def unit_header(src, unit) -> str:
    bits = [src["doc_id"]]
    for key in ("chapter", "section"):
        if unit.get(key):
            bits.append(unit[key])
    bits.append(unit["location"] + (f": {unit['title']}" if unit.get("title") else ""))
    return " | ".join(bits)


def chunk_structured(src: dict, units: list[dict]) -> list[dict]:
    chunks = []
    recital_buffer = []

    def flush_recitals():
        if not recital_buffer:
            return
        first, last = recital_buffer[0]["number"], recital_buffer[-1]["number"]
        location = f"Recital {first}" if first == last else f"Recitals {first}-{last}"
        text = "\n".join(f"({u['number']}) " + " ".join(t for t, _ in u["lines"]) for u in recital_buffer)
        locs = "|".join(f"Recital {u['number']}" for u in recital_buffer)
        chunks.append(make_chunk(src, "structured", location, f"{src['doc_id']}, {location}",
                                 f"{src['doc_id']} | {location}", text, 1, recital_buffer[0]["page"],
                                 {"locations": locs}))
        recital_buffer.clear()

    for unit in units:
        if unit["kind"] == "recital":
            size = sum(words(" ".join(t for t, _ in u["lines"])) for u in recital_buffer)
            if recital_buffer and size + words(" ".join(t for t, _ in unit["lines"])) > RECITAL_GROUP_WORDS:
                flush_recitals()
            recital_buffer.append(unit)
            continue
        flush_recitals()
        header = unit_header(src, unit)
        # split at paragraph boundaries when too long, and always where a new SCC module starts
        parts, current, size, module = [], [], 0, ""
        for text, page in unit["lines"]:
            new_module = RE_MODULE.match(text)
            if current and (size + words(text) > STRUCT_MAX_WORDS or new_module):
                parts.append((module, current))
                current, size = [], 0
            if new_module:
                module = text
            current.append((text, page))
            size += words(text)
        if current:
            parts.append((module, current))
        for n, (module, part) in enumerate(parts, 1):
            label = header + (f" | {module}" if module else "") + (f" (part {n} of {len(parts)})" if len(parts) > 1 else "")
            page = part[0][1]
            cite = f"{src['doc_id']}, {unit['location']}" + (f", p. {page}" if page else "")
            chunks.append(make_chunk(src, "structured", unit["location"], cite, label,
                                     "\n".join(t for t, _ in part), n, page, {"locations": unit["location"]}))
    flush_recitals()
    return chunks


def chunk_fixed(src: dict, units: list[dict]) -> list[dict]:
    """400-word windows over the whole text, ignoring structure (the baseline design)."""
    stream = []   # (word, unit location, page)
    for unit in units:
        for text, page in unit["lines"]:
            for w in text.split():
                stream.append((w, unit["location"], page))
    chunks = []
    step = FIXED_WORDS - FIXED_OVERLAP
    for n, start in enumerate(range(0, max(len(stream) - FIXED_OVERLAP, 1), step), 1):
        window = stream[start:start + FIXED_WORDS]
        locs = list(dict.fromkeys(loc for _, loc, _ in window))
        location = locs[0] if len(locs) == 1 else f"{locs[0]} to {locs[-1]}"
        page = window[0][2]
        cite = f"{src['doc_id']}, {location}" + (f", p. {page}" if page else "")
        chunks.append(make_chunk(src, "fixed", location, cite, f"{src['doc_id']} | {location} (window {n})",
                                 " ".join(w for w, _, _ in window), n, page, {"locations": "|".join(locs)}))
    return chunks


def chunk_file(path: Path, design: str = "structured") -> list[dict]:
    """Extract, clean and chunk one file. Each chunk also records the file's hash."""
    path = Path(path)
    src = source_for(path)
    units = structure(extract(path))
    chunks = chunk_structured(src, units) if design == "structured" else chunk_fixed(src, units)
    digest = hashlib.sha256(path.read_bytes()).hexdigest()[:16]
    for c in chunks:
        c["meta"]["file_sha"] = digest
    return chunks


# ================================================================ embed + store

def embed_and_store(chunks: list[dict], design: str) -> tuple[int, int]:
    """Embed only the chunks without a saved vector; save after every batch.

    Returns (newly embedded, already saved).
    """
    col = collection(design)
    ids = [c["id"] for c in chunks]
    saved = set()
    for i in range(0, len(ids), 500):
        saved.update(col.get(ids=ids[i:i + 500], include=[])["ids"])
    todo = [c for c in chunks if c["id"] not in saved]
    done = 0
    for i in range(0, len(todo), EMBED_BATCH):
        batch = todo[i:i + EMBED_BATCH]
        vectors = embed([c["meta"]["header"] + "\n" + c["text"] for c in batch], "RETRIEVAL_DOCUMENT")
        col.upsert(ids=[c["id"] for c in batch], embeddings=vectors,
                   documents=[c["text"] for c in batch], metadatas=[c["meta"] for c in batch])
        done += len(batch)
        log(f"  {design}: embedded {done}/{len(todo)} new chunks")
    return done, len(saved)


def remove_stale(design: str, keep_ids: set[str], doc_ids: set[str]) -> int:
    """Delete chunks of these documents that the current chunker no longer produces."""
    col = collection(design)
    data = col.get(include=["metadatas"])
    stale = [i for i, m in zip(data["ids"], data["metadatas"]) if m["doc_id"] in doc_ids and i not in keep_ids]
    if stale:
        col.delete(ids=stale)
    return len(stale)


def add_file(path: str | Path, design: str) -> str:
    """add_document's pipeline for one file. Decision on duplicates:
    - same file content already indexed  -> do nothing (no quota spent);
    - same document name, changed content -> replace its old chunks with the new ones;
    - new document                        -> chunk, embed and store.
    """
    path = Path(path).expanduser().resolve()
    if not path.is_file():
        return f"Not added: {path} does not exist."
    chunks = chunk_file(path, design)
    if not chunks:
        return f"Not added: no text could be extracted from {path.name}."
    doc_id, digest = chunks[0]["meta"]["doc_id"], chunks[0]["meta"]["file_sha"]
    col = collection(design)
    existing = col.get(where={"doc_id": doc_id}, include=["metadatas"])
    if existing["ids"]:
        if all(m.get("file_sha") == digest for m in existing["metadatas"]):
            return (f"Already indexed: '{doc_id}' ({len(existing['ids'])} chunks) with identical content. "
                    f"Nothing was re-embedded.")
        col.delete(ids=existing["ids"])
        action = f"Replaced the previous version of '{doc_id}' ({len(existing['ids'])} old chunks removed)."
    else:
        action = f"Added new document '{doc_id}'."
    new, _ = embed_and_store(chunks, design)
    return f"{action} {len(chunks)} chunks, {new} embedded and stored. Cite it as e.g. [{chunks[0]['meta']['cite']}]."


# ================================================================ main

def main() -> None:
    paths = download_corpus()
    total_words = 0
    for path in paths:
        w = words(" ".join(t for t, _ in extract(path)))
        total_words += w
        log(f"{source_for(path)['doc_id']}: {w} words after cleaning")
    log(f"corpus: {len(paths)} documents, {total_words} words")
    for design in DESIGNS:
        all_chunks = [c for path in paths for c in chunk_file(path, design)]
        log(f"{design}: {len(all_chunks)} chunks, "
            f"avg {sum(c['meta']['words'] for c in all_chunks) / len(all_chunks):.0f} words")
        removed = remove_stale(design, {c["id"] for c in all_chunks}, {s["doc_id"] for s in SOURCES})
        if removed:
            log(f"  removed {removed} stale chunks")
        try:
            new, saved = embed_and_store(all_chunks, design)
        except QuotaExhausted as error:
            log(f"\nDaily embedding quota reached; everything embedded so far is saved.\n"
                f"Run `main.py index` again tomorrow to finish. ({error})")
            sys.exit(1)
        log(f"  {design}: {new} newly embedded, {saved} already had a saved vector")


if __name__ == "__main__":
    main()
