"""
Assignment 3: build the index (`main.py index`).

Corpus: selected chapters of three FAA handbooks (US government works, public
domain) for a student-pilot "go / no-go" assistant. See SOURCES below.

Pipeline, per file:
    extract_units(path, pages)   PDF -> text units tagged with page label and section
    chunk_units(units, design)   units -> chunks for one retrieval design
    embed_and_store(chunks)      embeds only chunks without a saved vector

Two retrieval designs are built side by side, each in its own ChromaDB
collection inside index/:
    fixed   - 150-word windows with a 30-word overlap, blind to structure
    section - one chunk per handbook section (split at sentence boundaries
              when longer than MAX_SECTION_WORDS), heading prefixed to the text

server.py imports `add_document`, `search` and friends from here.

    uv run python index.py            # download, chunk, embed what is missing
    uv run python index.py --dry-run  # chunk and report counts, embed nothing
"""

from __future__ import annotations

import hashlib
import logging
import re
import sys
import time
import urllib.request
from collections import Counter
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"

log = logging.getLogger("index")

# --------------------------------------------------------------------------- #
# Corpus
# --------------------------------------------------------------------------- #

FAA = "https://www.faa.gov/sites/faa.gov/files"

# `pages` are 1-based PDF page ranges (inclusive) of the chapters we keep.
SOURCES = [
    {
        "source": "FAA-H-8083-25C",
        "title": "Pilot's Handbook of Aeronautical Knowledge",
        "url": "https://www.faa.gov/regulations_policies/handbooks_manuals/aviation/faa-h-8083-25c.pdf",
        "file": "phak.pdf",
        "chapters": [
            ("Chapter 10: Weight and Balance", (245, 256)),
            ("Chapter 11: Aircraft Performance", (257, 284)),
            ("Chapter 17: Aeromedical Factors", (423, 452)),
        ],
    },
    {
        "source": "FAA-H-8083-3C",
        "title": "Airplane Flying Handbook",
        "url": f"{FAA}/regulations_policies/handbooks_manuals/aviation/airplane_handbook/19_afh_ch18.pdf",
        "file": "afh_ch18.pdf",
        "chapters": [
            ("Chapter 18: Emergency Procedures", (1, 23)),
        ],
    },
    {
        "source": "FAA-H-8083-28B",
        "title": "Aviation Weather Handbook",
        "url": f"{FAA}/FAA-H-8083-28B.pdf",
        "file": "awh.pdf",
        "chapters": [
            ("Chapter 18: Weather and Obstructions to Visibility", (221, 232)),
            ("Chapter 19: Turbulence", (233, 242)),
            ("Chapter 20: Icing", (243, 249)),
            ("Chapter 22: Thunderstorms", (256, 277)),
        ],
    },
]

USER_AGENT = "Mozilla/5.0 (course assignment; corpus download)"


def download(src: dict) -> Path:
    """Download one source PDF into corpus/ unless it is already there."""
    CORPUS_DIR.mkdir(exist_ok=True)
    path = CORPUS_DIR / src["file"]
    if path.is_file() and path.stat().st_size > 0:
        return path
    log.info("downloading %s ...", src["url"])
    request = urllib.request.Request(src["url"], headers={"User-Agent": USER_AGENT})
    tmp = path.with_suffix(".part")
    with urllib.request.urlopen(request, timeout=600) as response, tmp.open("wb") as out:
        while block := response.read(1 << 20):
            out.write(block)
    tmp.replace(path)
    return path


# --------------------------------------------------------------------------- #
# Extraction and cleaning
# --------------------------------------------------------------------------- #

@dataclass
class Unit:
    """A run of body text on one page under one section heading."""
    chapter: str
    section: str
    page: str          # printed page label, e.g. "11-5"; "p<n>" if none found
    text: str


def _font_family(name: str) -> tuple[str, bool]:
    """'XGOTCU+Helvetica-Bold' -> ('helvetica', True); 'TimesNewRomanPS-ItalicMT' -> ('timesnewroman', False)."""
    name = name.lstrip("/").split("+")[-1]
    bold = "bold" in name.lower()
    family = re.split(r"[-,]", name)[0]
    family = re.sub(r"(PSMT|PS|MT)$", "", family)
    return family.lower(), bold


PAGE_LABEL = re.compile(r"^\s*(\d{1,2})\s*[-–]\s*(\d{1,3})\s*$")
# Weather Handbook running header: "Chapter 20, Icing  20-2"
RUNNING_HEADER = re.compile(r"Chapter\s+\d+,\s[^\n]*?(\d{1,2})\s*-\s*(\d{1,3})\s*$", re.M)


def _page_fragments(page) -> list[tuple[str, float, str, bool]]:
    """(text, size, font family, bold) for every text fragment on a page."""
    frags = []

    def visit(text, cm, tm, font_dict, font_size):
        if not text:
            return
        size = round(font_size * abs(tm[0] or 1) * abs(cm[0] or 1), 1)
        family, bold = _font_family((font_dict or {}).get("/BaseFont", "?"))
        frags.append((text, size, family, bold))

    page.extract_text(visitor_text=visit)
    return frags


def clean_text(text: str) -> str:
    """Join the pieces pypdf leaves broken: hyphenated line ends, split words, stray spaces."""
    text = text.replace(" ", " ").replace("�", "'")
    text = re.sub(r"(\w)-\s*\n\s*([a-z])", r"\1\2", text)          # hyphen at line end
    text = re.sub(r"\[\s*Figures?\s[^\]]*\]", "", text)            # "[Figure 11-2]" references
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s+([,.;:!?)])", r"\1", text)
    return text.strip()


def _bare(token: str) -> str:
    return re.sub(r"^[^\w]+|[^\w’']+$", "", token).lower()


def fix_split_words(units: list[Unit]) -> None:
    """Rejoin words pypdf splits apart ("f reezing", "w ith", "containin g", "Pe rsonality").

    Two neighbouring tokens are joined when the joined form is a word found
    elsewhere in the same document and at least one piece is not a word that
    occurs on its own (seen fewer than 3 times). No dictionary needed, and
    real word pairs such as "Earth’s gravitational" are left alone.
    """
    vocab = Counter(_bare(t) for u in units for t in u.text.split())
    known = lambda w: vocab[w] >= 3 or w in {"a", "i"}  # noqa: E731
    for u in units:
        tokens = u.text.split()
        out: list[str] = []
        for token in tokens:
            if out:
                prev = out[-1]
                a, b = _bare(prev), _bare(token)
                joined = _bare(prev + token)
                if (a and b and a.isalpha() and b[:1].isalpha() and not re.search(r"[^\w’']", prev)
                        and vocab[joined] >= 1 and (not known(a) or not known(b))):
                    out[-1] = prev + token
                    continue
            out.append(token)
        u.text = " ".join(out)


def _is_heading_text(text: str) -> bool:
    t = text.strip()
    if not re.search(r"[A-Za-z]{3}", t) or t.lower().startswith("figure"):
        return False
    digits = sum(c.isdigit() for c in t)
    return digits / max(len(t), 1) < 0.3 and len(t.split()) <= 14


def extract_units(path: Path, pages: tuple[int, int] | None = None, chapter: str = "") -> list[Unit]:
    """Extract body text from a PDF page range, tagged with page label and section.

    Uses font size and family rather than plain text so that headings are
    recognised and figure labels, axis numbers, captions and running headers
    are dropped: body text is the most common (family, size); a heading is a
    bold run in another family at body size or above, or the body family set
    larger than body text.
    """
    from pypdf import PdfReader, apply_configuration

    # One page of the Pilot's Handbook (p. 448, a dense figure) exceeds pypdf's
    # default parsing budget and raises LimitReachedError; raise the budget.
    with apply_configuration(stream_parsing_work_maximum_count=50_000_000):
        reader = PdfReader(str(path))
        first, last = pages or (1, len(reader.pages))
        page_frags = []
        for n in range(first, last + 1):
            try:
                page_frags.append((n, _page_fragments(reader.pages[n - 1])))
            except Exception as error:  # noqa: BLE001 - skip one bad page, keep the rest
                log.warning("%s p%d: extraction failed (%s); skipped", path.name, n, error)

    weights = Counter()
    for _, frags in page_frags:
        for text, size, family, _ in frags:
            weights[(family, size)] += len(text.strip())
    body_family, body_size = weights.most_common(1)[0][0]

    units: list[Unit] = []
    section = chapter or path.stem
    for n, frags in page_frags:
        label = None
        page_start = len(units)
        body: list[str] = []
        heading: list[str] = []
        other: list[str] = []   # dropped text (figure labels, page numbers), searched for the page label

        def flush_body():
            nonlocal label
            text = "".join(body)
            m = RUNNING_HEADER.search(text)
            if m:
                label = label or f"{m.group(1)}-{m.group(2)}"
                text = RUNNING_HEADER.sub("", text)
            text = clean_text(text)
            if len(text.split()) >= 3:
                units.append(Unit(chapter, section, label or f"p{n}", text))
            body.clear()

        for text, size, family, bold in frags:
            if not text.strip():
                # The Airplane Flying Handbook sets the spaces between words in a
                # different font from the words; keep whitespace whatever its font.
                (heading if heading else body).append(" " if heading else text)
                continue
            m = PAGE_LABEL.match(text)
            if m and size <= body_size + 1.6:
                label = f"{m.group(1)}-{m.group(2)}"
                continue
            is_body = family == body_family and abs(size - body_size) <= 0.6
            is_heading = (
                (bold and family != body_family and size >= body_size - 0.1)
                or (family == body_family and body_size + 0.6 < size < 20)
            )
            if is_heading and not text.strip():
                continue
            if is_heading:
                heading.append(text)
                continue
            if heading:  # heading run just ended
                title = clean_text(" ".join(heading))
                heading.clear()
                if _is_heading_text(title):
                    flush_body()
                    section = title
            if is_body:
                body.append(text)
            else:
                other.append(text)
        if heading:
            title = clean_text(" ".join(heading))
            if _is_heading_text(title):
                flush_body()
                section = title
        if label is None:   # page number split across fragments, e.g. "18-" + "2"
            m = re.search(r"(?m)^\s*(\d{1,2})\s*[-–]\s*(\d{1,3})\s*$", "".join(other))
            if m:
                label = f"{m.group(1)}-{m.group(2)}"
        flush_body()
        # Labels are often printed at the bottom: give this page's units the label found anywhere on it.
        if label:
            for unit in units[page_start:]:
                if unit.page == f"p{n}":
                    unit.page = label
    return units


def extract_plain_text(path: Path) -> list[Unit]:
    """A .txt or .md file: '#' lines are sections, blank-line paragraphs are units."""
    units, section = [], path.stem
    for i, para in enumerate(re.split(r"\n\s*\n", path.read_text(encoding="utf-8")), start=1):
        para = para.strip()
        if para.startswith("#"):
            first, _, rest = para.partition("\n")
            section = first.lstrip("#").strip()
            para = rest.strip()
        if para:
            units.append(Unit(path.stem, section, f"para {i}", clean_text(para)))
    return units


# --------------------------------------------------------------------------- #
# Chunking
# --------------------------------------------------------------------------- #

DESIGNS = ["fixed", "section"]
CHOSEN_DESIGN = "section"   # set from the retrieval comparison in evaluate.py; see REPORT.md

FIXED_WORDS, FIXED_OVERLAP = 150, 30
MAX_SECTION_WORDS, SECTION_TARGET, MIN_SECTION_WORDS = 350, 250, 40


@dataclass
class Chunk:
    id: str
    text: str            # what is shown and cited
    embed_text: str      # what is embedded (adds the heading for context)
    metadata: dict = field(default_factory=dict)


def _page_span(pages: list[str]) -> str:
    unique = list(dict.fromkeys(pages))
    return unique[0] if len(unique) == 1 else f"{unique[0]} to {unique[-1]}"


def _make_chunk(design, source, title, chapter, section, pages, text, file_hash) -> Chunk:
    words = len(text.split())
    digest = hashlib.sha1(f"{design}|{source}|{chapter}|{text}".encode("utf-8")).hexdigest()[:20]
    metadata = {
        "design": design,
        "source": source,
        "title": title,
        "chapter": chapter,
        "section": section,
        "page": _page_span(pages),
        "pages": "|" + "|".join(dict.fromkeys(pages)) + "|",   # for exact page lookup
        "words": words,
        "file_hash": file_hash,
    }
    embed_text = f"title: {title} - {chapter} - {section} | text: {text}"
    return Chunk(f"{design}-{digest}", text, embed_text, metadata)


def _split_sentences(text: str) -> list[str]:
    return [s for s in re.split(r"(?<=[.!?])\s+(?=[A-Z0-9\"(])", text) if s]


def chunk_units(units: list[Unit], design: str, source: str, title: str, file_hash: str) -> list[Chunk]:
    chunks: list[Chunk] = []
    if design == "fixed":
        # Word stream per chapter, each word remembering its page and section.
        by_chapter: dict[str, list[tuple[str, str, str]]] = {}
        for u in units:
            by_chapter.setdefault(u.chapter, []).extend((w, u.page, u.section) for w in u.text.split())
        step = FIXED_WORDS - FIXED_OVERLAP
        for chapter, words in by_chapter.items():
            for start in range(0, len(words), step):
                window = words[start:start + FIXED_WORDS]
                if len(window) < 30 and start > 0:
                    break
                chunks.append(_make_chunk(
                    design, source, title, chapter, window[0][2], [w[1] for w in window],
                    " ".join(w[0] for w in window), file_hash,
                ))
                if start + FIXED_WORDS >= len(words):
                    break
        return chunks

    if design == "section":
        # Group consecutive units of the same section.
        groups: list[dict] = []
        for u in units:
            if groups and groups[-1]["chapter"] == u.chapter and groups[-1]["section"] == u.section:
                groups[-1]["parts"].append(u)
            else:
                groups.append({"chapter": u.chapter, "section": u.section, "parts": [u]})
        # Merge a very short section into the next one in the same chapter.
        merged: list[dict] = []
        carry = None
        for g in groups:
            if carry and carry["chapter"] == g["chapter"]:
                g = {"chapter": g["chapter"], "section": f"{carry['section']} / {g['section']}",
                     "parts": carry["parts"] + g["parts"]}
            elif carry:
                merged.append(carry)
            carry = None
            if sum(len(p.text.split()) for p in g["parts"]) < MIN_SECTION_WORDS:
                carry = g
            else:
                merged.append(g)
        if carry:
            merged.append(carry)

        for g in merged:
            # Sentences tagged with their page, then packed into pieces.
            sentences = [(s, p.page) for p in g["parts"] for s in _split_sentences(p.text)]
            total = sum(len(s.split()) for s, _ in sentences)
            target = total if total <= MAX_SECTION_WORDS else SECTION_TARGET
            n_pieces = max(1, round(total / target))
            target = total / n_pieces
            piece, count = [], 0
            for s, page in sentences:
                piece.append((s, page))
                count += len(s.split())
                if count >= target and len(chunks) >= 0 and s is not sentences[-1][0]:
                    chunks.append(_make_chunk(design, source, title, g["chapter"], g["section"],
                                              [p for _, p in piece], " ".join(x for x, _ in piece), file_hash))
                    piece, count = [], 0
            if piece:
                chunks.append(_make_chunk(design, source, title, g["chapter"], g["section"],
                                          [p for _, p in piece], " ".join(x for x, _ in piece), file_hash))
        return chunks

    raise ValueError(f"unknown design {design!r}; expected one of {DESIGNS}")


def file_sha256(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        while block := f.read(1 << 20):
            h.update(block)
    return h.hexdigest()


def chunk_file(path: str | Path, design: str = CHOSEN_DESIGN, source: str | None = None,
               title: str | None = None, chapters: list | None = None) -> list[Chunk]:
    """Extract, clean and chunk one file (PDF, .txt or .md) for one design.

    `chapters` is a list of (chapter name, (first page, last page)); by default
    the whole file is one chapter named after the file.
    """
    path = Path(path)
    file_hash = file_sha256(path)
    source = source or path.stem
    title = title or path.stem
    if path.suffix.lower() == ".pdf":
        units = []
        for chapter, pages in chapters or [(path.stem, None)]:
            units += extract_units(path, pages, chapter)
        fix_split_words(units)   # vocabulary from the whole file
    elif path.suffix.lower() in {".txt", ".md"}:
        units = extract_plain_text(path)
    else:
        raise ValueError(f"unsupported file type {path.suffix!r}; use .pdf, .txt or .md")
    return chunk_units(units, design, source, title, file_hash)


# --------------------------------------------------------------------------- #
# Embedding and storage
# --------------------------------------------------------------------------- #

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768
EMBED_BATCH = 50


class QuotaExhausted(RuntimeError):
    """The Gemini free tier refused more embeddings for today."""


_client = None
_chroma = None


def gemini():
    global _client
    if _client is None:
        from google import genai
        from api_key import load_api_key
        _client = genai.Client(api_key=load_api_key())
    return _client


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed a batch, retrying on per-minute limits; raise QuotaExhausted on the daily one."""
    from google.genai import types
    for attempt in range(8):
        try:
            # One Content per text: gemini-embedding-2 merges a plain list of
            # strings into a single embedding instead of one per string.
            result = gemini().models.embed_content(
                model=EMBED_MODEL,
                contents=[types.Content(parts=[types.Part(text=t)]) for t in texts],
                config=types.EmbedContentConfig(output_dimensionality=EMBED_DIM),
            )
            vectors = [list(e.values) for e in result.embeddings]
            if len(vectors) != len(texts):
                raise RuntimeError(f"asked for {len(texts)} embeddings, got {len(vectors)}")
            return vectors
        except Exception as error:  # noqa: BLE001 - inspect the API error
            message = str(error)
            if "429" not in message and "RESOURCE_EXHAUSTED" not in message:
                raise
            if "PerDay" in message or "per day" in message.lower():
                raise QuotaExhausted(message[:300]) from error
            wait = 20 * (attempt + 1)
            log.warning("rate limited; waiting %ds", wait)
            time.sleep(wait)
    raise QuotaExhausted("still rate limited after several retries")


def embed_query(query: str) -> list[float]:
    return embed_texts([f"task: search result | query: {query}"])[0]


def chroma():
    global _chroma
    if _chroma is None:
        import chromadb
        from chromadb.config import Settings
        INDEX_DIR.mkdir(exist_ok=True)
        _chroma = chromadb.PersistentClient(path=str(INDEX_DIR), settings=Settings(anonymized_telemetry=False))
    return _chroma


def collection(design: str = CHOSEN_DESIGN):
    return chroma().get_or_create_collection(
        name=f"faa_{design}", embedding_function=None, metadata={"hnsw:space": "cosine"},
    )


def embed_and_store(chunks: list[Chunk], design: str) -> int:
    """Embed and store only the chunks whose id has no saved vector. Returns how many were embedded."""
    coll = collection(design)
    ids = [c.id for c in chunks]
    existing = set()
    for i in range(0, len(ids), 500):
        existing |= set(coll.get(ids=ids[i:i + 500], include=[])["ids"])
    todo = [c for c in chunks if c.id not in existing]
    done = 0
    for i in range(0, len(todo), EMBED_BATCH):
        batch = todo[i:i + EMBED_BATCH]
        vectors = embed_texts([c.embed_text for c in batch])
        coll.add(ids=[c.id for c in batch], embeddings=vectors,
                 documents=[c.text for c in batch], metadatas=[c.metadata for c in batch])
        done += len(batch)   # saved immediately: a crash or quota stop loses nothing
        log.info("  %s: embedded %d/%d new chunks", design, done, len(todo))
    return done


def remove_stale(design: str, source: str, keep_ids: set[str]) -> int:
    """Delete chunks of `source` that the current chunking no longer produces."""
    coll = collection(design)
    old = set(coll.get(where={"source": source}, include=[])["ids"])
    stale = sorted(old - keep_ids)
    if stale:
        coll.delete(ids=stale)
    return len(stale)


# --------------------------------------------------------------------------- #
# Search and add-document (used by server.py)
# --------------------------------------------------------------------------- #

def search(query: str, k: int = 5, design: str = CHOSEN_DESIGN, query_vector=None) -> list[dict]:
    """Top-k chunks for a query: text, source, title, chapter, section, page, score."""
    coll = collection(design)
    vector = query_vector if query_vector is not None else embed_query(query)
    res = coll.query(query_embeddings=[vector], n_results=k, include=["documents", "metadatas", "distances"])
    hits = []
    for doc, meta, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0]):
        hits.append({**meta, "id": None, "text": doc, "score": round(1 - dist, 4)})
    for hit, cid in zip(hits, res["ids"][0]):
        hit["id"] = cid
    return hits


def add_document(path: str | Path, design: str = CHOSEN_DESIGN) -> dict:
    """Index one file for `design`. Same name and same content: skipped. Same name, new content: replaced."""
    path = Path(path).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"no such file: {path}")
    source = path.stem
    file_hash = file_sha256(path)
    coll = collection(design)
    existing = coll.get(where={"source": source}, include=["metadatas"])
    if existing["ids"] and all(m.get("file_hash") == file_hash for m in existing["metadatas"]):
        return {"status": "already indexed", "source": source, "chunks": len(existing["ids"]), "embedded": 0}
    chunks = chunk_file(path, design=design, source=source, title=source)
    if not chunks:
        return {"status": "no text found", "source": source, "chunks": 0, "embedded": 0}
    embedded = embed_and_store(chunks, design)
    removed = remove_stale(design, source, {c.id for c in chunks})
    status = "replaced" if existing["ids"] else "added"
    return {"status": status, "source": source, "chunks": len(chunks), "embedded": embedded, "removed": removed}


# --------------------------------------------------------------------------- #
# main.py index
# --------------------------------------------------------------------------- #

def build_chunks() -> dict[str, dict[str, list[Chunk]]]:
    """All corpus chunks, by design then source. Each PDF is extracted once for both designs."""
    out = {d: {} for d in DESIGNS}
    for src in SOURCES:
        path = download(src)
        file_hash = file_sha256(path)
        units = [u for chapter, pages in src["chapters"] for u in extract_units(path, pages, chapter)]
        fix_split_words(units)
        for design in DESIGNS:
            out[design][src["source"]] = chunk_units(units, design, src["source"], src["title"], file_hash)
    return out


def main(dry_run: bool = False) -> int:
    logging.basicConfig(level=logging.INFO, format="%(message)s", stream=sys.stderr)
    logging.getLogger("httpx").setLevel(logging.WARNING)
    for name in ("chromadb", "google_genai"):
        logging.getLogger(name).setLevel(logging.WARNING)

    incomplete = False
    chunks = build_chunks()
    # The chosen design first, so it is complete even if the daily quota runs out.
    for design in sorted(DESIGNS, key=lambda d: d != CHOSEN_DESIGN):
        chunks_by_source = chunks[design]
        all_chunks = [c for cs in chunks_by_source.values() for c in cs]
        words = [c.metadata["words"] for c in all_chunks]
        print(f"[{design}] {len(all_chunks)} chunks, {sum(words):,} words, "
              f"{min(words)}-{max(words)} words per chunk (mean {sum(words) / len(words):.0f})")
        for source, cs in chunks_by_source.items():
            print(f"    {source}: {len(cs)} chunks")
        if dry_run:
            continue
        try:
            for source, cs in chunks_by_source.items():
                n = embed_and_store(cs, design)
                stale = remove_stale(design, source, {c.id for c in cs})
                if n or stale:
                    print(f"    {source}: embedded {n} new, removed {stale} stale")
        except QuotaExhausted as error:
            print(f"\nDaily embedding quota reached while building '{design}'. Everything embedded so far "
                  f"is saved; run `main.py index` again tomorrow to finish.\n  {error}", file=sys.stderr)
            incomplete = True
            break
        print(f"    stored: {collection(design).count()} vectors")
    return 1 if incomplete else 0


if __name__ == "__main__":
    raise SystemExit(main(dry_run="--dry-run" in sys.argv))
