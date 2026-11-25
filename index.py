"""
Assignment 3: build the index (`main.py index`).

Corpus: three EU regulations a startup compliance officer needs to decide
whether an AI product is high-risk and what that triggers.

    AI Act  Regulation (EU) 2024/1689
    GDPR    Regulation (EU) 2016/679
    DSA     Regulation (EU) 2022/2065

Pipeline, one function per step (server.py's add_document imports them):

    extract_lines(path)   PDF -> body-text lines with page numbers
                          (footnotes and page headers/footers removed)
    parse_units(lines)    lines -> legal units: recitals, articles, annexes
    chunk_file(path)      units -> chunks, each with source + location metadata
    embed_and_store(...)  embed only chunks without a saved vector, store in Chroma

Vectors are cached in index/embeddings.jsonl, keyed by a hash of the chunk
text, and appended one batch at a time, so a crash or the free-tier daily
limit loses nothing and a re-run only embeds what is missing.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent
SOURCES_DIR = ROOT / "sources"          # committed PDFs (EUR-Lex reuse licence)
INDEX_DIR = ROOT / "index"
CACHE_FILE = INDEX_DIR / "embeddings.jsonl"
CHROMA_DIR = INDEX_DIR / "chroma"

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768             # truncated (Matryoshka) vectors keep index/ small
BATCH_SIZE = 50
MAX_WORDS = 350             # structure chunks are split at paragraph breaks above this

# Known documents: file name -> short source name used in citations.
DOCUMENTS = {
    "ai_act.pdf": {"source": "AI Act", "title": "Regulation (EU) 2024/1689 (Artificial Intelligence Act)",
                   "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=OJ:L_202401689"},
    "gdpr.pdf": {"source": "GDPR", "title": "Regulation (EU) 2016/679 (General Data Protection Regulation)",
                 "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32016R0679"},
    "dsa.pdf": {"source": "DSA", "title": "Regulation (EU) 2022/2065 (Digital Services Act)",
                "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32022R2065"},
}


def log(*args) -> None:
    """Log to stderr: server.py imports this module and stdout carries MCP."""
    print(*args, file=sys.stderr, flush=True)


# --------------------------------------------------------------------------- extract

BODY_MIN_FONT = 9.0   # body text is 9.6pt; footnotes 8.5pt; footnote markers ~5pt

HEADER_FOOTER = [
    re.compile(r"^(EN\s+)?OJ L,\s*\d{1,2}\.\d{1,2}\.\d{4}(\s+EN)?$"),
    re.compile(r"^(\d+/\d+\s+)?ELI: http://data\.europa\.eu/eli/\S+(\s+\d+/\d+)?$"),
    re.compile(r"^(EN\s+)?Official Journal of the European Union.*$"),
    re.compile(r"^\d{1,2}\.\d{1,2}\.\d{4}\s+L \d+/\d+\s+Official Journal.*$"),
    re.compile(r"^L \d+/\d+\s+(EN\s+)?Official Journal.*$"),
    re.compile(r"^EN$"),
]


def is_header_footer(line: str) -> bool:
    return any(p.match(line) for p in HEADER_FOOTER)


# Structural markers the Official Journal sets in the same small font as footnotes.
SMALL_FONT_KEEP = re.compile(
    r"^(CHAPTER [IVXLC]+|SECTION \d+|HAVE ADOPTED THIS REGULATION:?|ANNEX [IVXLC]+|\(\d+\)|Whereas:?)$"
)


def extract_lines(path: Path) -> list[tuple[int, str]]:
    """Return (page, line) pairs of body text only.

    Footnotes look like recitals ("(12) Regulation ...") so a regex on the
    text cannot tell them apart; their font size can: body text is 9.6pt,
    footnotes 8.5pt, footnote reference markers ~5pt. But the Official
    Journal also sets structural markers (recital numbers, CHAPTER headings,
    "HAVE ADOPTED THIS REGULATION") at 8.5pt, so small text is dropped unless
    it is one of those markers. Then the running headers/footers are removed.
    """
    if path.suffix.lower() in (".txt", ".md"):
        return [(1, re.sub(r"\s+", " ", l).strip()) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]

    from pypdf import PdfReader

    out: list[tuple[int, str]] = []
    for page_no, page in enumerate(PdfReader(path).pages, start=1):
        parts: list[str] = []

        def keep_body(text, cm, tm, _font_dict, font_size):
            size = abs(font_size * tm[3] * cm[3])
            stripped = text.strip()
            all_caps_heading = len(stripped) > 3 and stripped.upper() == stripped and re.search(r"[A-Z]{3}", stripped)
            if size >= BODY_MIN_FONT or SMALL_FONT_KEEP.match(stripped) or all_caps_heading:
                parts.append(text)
            elif "\n" in text:
                parts.append("\n")   # keep line breaks of dropped text

        page.extract_text(visitor_text=keep_body)
        for line in "".join(parts).splitlines():
            line = re.sub(r"\(\s*\)", "", line)        # "Council ()" left by a removed footnote marker
            line = re.sub(r"\s+", " ", line).strip()
            if line and not is_header_footer(line):
                out.append((page_no, line))
    return out


# --------------------------------------------------------------------------- structure

@dataclass
class Unit:
    """One legal unit: a recital, an article or an annex."""
    kind: str                  # recital | article | annex
    number: str                # "53", "6", "III"
    title: str = ""
    chapter: str = ""
    lines: list[tuple[int, str]] = field(default_factory=list)


RE_RECITAL = re.compile(r"^\((\d+)\)\s+(.*)$")
RE_ARTICLE = re.compile(r"^Article (\d+[a-z]?)$")
RE_CHAPTER = re.compile(r"^CHAPTER ([IVXLC]+)$")
RE_SECTION = re.compile(r"^SECTION (\d+)$", re.I)
RE_ANNEX = re.compile(r"^ANNEX ([IVXLC]+)$")
RE_END_ENACTING = re.compile(r"^(Done at|This Regulation shall be binding in its entirety)")


def parse_units(lines: list[tuple[int, str]]) -> list[Unit]:
    """Split the regulation into recitals, articles and annexes.

    The order of an EU regulation is fixed: preamble, "Whereas:", recitals,
    "HAVE ADOPTED THIS REGULATION:", chapters and articles, "Done at ...",
    signatures, then annexes. We walk the lines once with that state machine.
    """
    units: list[Unit] = []
    state = "preamble"
    chapter = ""
    current: Unit | None = None
    pending_title_for: Unit | None = None   # article/annex/chapter whose title is the next line
    pending_chapter = False

    def close():
        nonlocal current
        if current and current.lines:
            units.append(current)
        current = None

    for page, line in lines:
        if state == "preamble":
            if line.startswith("Whereas"):
                state = "recitals"
            continue

        if state == "recitals":
            if line.startswith("HAVE ADOPTED THIS REGULATION"):
                close()
                state = "articles"
                continue
            m = RE_RECITAL.match(line)
            expected = str(int(current.number) + 1) if current else "1"
            if m and m.group(1) == expected:
                close()
                current = Unit("recital", m.group(1), lines=[(page, m.group(2))])
            elif current:
                current.lines.append((page, line))
            continue

        if state == "articles":
            if RE_END_ENACTING.match(line) and current and current.kind == "article":
                close()
                state = "signatures"
                continue
            m = RE_CHAPTER.match(line)
            if m:
                close()
                chapter = f"Chapter {m.group(1)}"
                pending_chapter = True
                continue
            if pending_chapter and not RE_ARTICLE.match(line) and not RE_SECTION.match(line):
                chapter = f"{chapter} {line}"
                pending_chapter = False
                continue
            pending_chapter = False
            if RE_SECTION.match(line):
                continue
            m = RE_ARTICLE.match(line)
            if m:
                close()
                current = Unit("article", m.group(1), chapter=chapter)
                pending_title_for = current
                continue
            if pending_title_for is not None:
                pending_title_for.title = line
                pending_title_for = None
                continue
            if current:
                current.lines.append((page, line))
            continue

        # signatures, then annexes (only the AI Act has annexes in this corpus)
        m = RE_ANNEX.match(line)
        if m:
            close()
            state = "annexes"
            current = Unit("annex", m.group(1))
            pending_title_for = current
            continue
        if state == "annexes":
            if pending_title_for is not None:
                pending_title_for.title = line
                pending_title_for = None
                continue
            if current:
                current.lines.append((page, line))
    close()
    return units


# --------------------------------------------------------------------------- chunk

def join_lines(lines: list[str]) -> str:
    """Join PDF lines into flowing text, repairing words hyphenated at line ends."""
    text = ""
    for line in lines:
        if text.endswith("-") and line[:1].islower():
            text = text[:-1] + line
        else:
            text = f"{text} {line}" if text else line
    return text


def split_paragraphs(unit: Unit) -> list[tuple[str, list[tuple[int, str]]]]:
    """Group a unit's lines into numbered paragraphs ("1.", "2." ...).

    Returns (paragraph label, lines). Text before the first number is label "".
    """
    marker = re.compile(r"^(\d+)\.\s")
    groups: list[tuple[str, list[tuple[int, str]]]] = [("", [])]
    expected = 1
    for page, line in unit.lines:
        m = marker.match(line)
        if m and int(m.group(1)) == expected:
            groups.append((m.group(1), []))
            expected += 1
        groups[-1][1].append((page, line))
    return [g for g in groups if g[1]]


def unit_location(unit: Unit) -> str:
    return {"recital": "Recital", "article": "Article", "annex": "Annex"}[unit.kind] + f" {unit.number}"


def make_chunk(meta: dict, unit: Unit, lines: list[tuple[int, str]], location: str) -> dict:
    pages = sorted({p for p, _ in lines})
    body = join_lines([l for _, l in lines])
    heading = f"{meta['source']}, {location}" + (f" ({unit.title})" if unit.title else "")
    if unit.chapter:
        heading += f" [{unit.chapter}]"
    return {
        # The heading is part of the embedded text: it tells the embedding which
        # law and article the passage belongs to, which body text often doesn't.
        "text": f"{heading}\n{body}",
        "source": meta["source"],
        "location": location,
        "kind": unit.kind,
        "article": unit.number if unit.kind == "article" else "",
        "title": unit.title,
        "chapter": unit.chapter,
        "page_start": pages[0],
        "page_end": pages[-1],
        "words": len(body.split()),
    }


def chunk_units(meta: dict, units: list[Unit], max_words: int = MAX_WORDS) -> list[dict]:
    """Structure-based chunks.

    - articles and annexes: one chunk per unit; if longer than max_words, split
      at numbered paragraph boundaries and labelled e.g. "Article 6(1)-(2)";
    - recitals: consecutive recitals packed together up to max_words,
      labelled e.g. "Recitals 52-53".
    """
    chunks: list[dict] = []

    recital_buf: list[Unit] = []

    def flush_recitals():
        if not recital_buf:
            return
        first, last = recital_buf[0].number, recital_buf[-1].number
        loc = f"Recital {first}" if first == last else f"Recitals {first}-{last}"
        lines = [(p, f"({u.number}) {l}" if i == 0 else l)
                 for u in recital_buf for i, (p, l) in enumerate(u.lines)]
        merged = Unit("recital", first if first == last else f"{first}-{last}")
        chunks.append(make_chunk(meta, merged, lines, loc))
        recital_buf.clear()

    for unit in units:
        words = sum(len(l.split()) for _, l in unit.lines)
        if unit.kind == "recital":
            buf_words = sum(len(l.split()) for u in recital_buf for _, l in u.lines)
            if recital_buf and buf_words + words > max_words:
                flush_recitals()
            recital_buf.append(unit)
            continue
        flush_recitals()

        base = unit_location(unit)
        if words <= max_words:
            chunks.append(make_chunk(meta, unit, unit.lines, base))
            continue

        # Long article/annex: pack consecutive numbered paragraphs up to max_words.
        paragraphs = split_paragraphs(unit)
        group: list[tuple[str, list[tuple[int, str]]]] = []

        def flush_group():
            if not group:
                return
            labels = [lab for lab, _ in group if lab]
            if not labels:
                loc = base
            elif len(labels) == 1:
                loc = f"{base}({labels[0]})" if unit.kind == "article" else f"{base}, point {labels[0]}"
            else:
                loc = (f"{base}({labels[0]})-({labels[-1]})" if unit.kind == "article"
                       else f"{base}, points {labels[0]}-{labels[-1]}")
            chunks.append(make_chunk(meta, unit, [x for _, ls in group for x in ls], loc))
            group.clear()

        for label, plines in paragraphs:
            pw = sum(len(l.split()) for _, l in plines)
            gw = sum(len(l.split()) for _, ls in group for _, l in ls)
            if group and gw + pw > max_words:
                flush_group()
            if pw > max_words * 2:
                # A single huge paragraph (e.g. Article 3 definitions): cut by lines.
                flush_group()
                piece: list[tuple[int, str]] = []
                for pl in plines:
                    piece.append(pl)
                    if sum(len(l.split()) for _, l in piece) >= max_words:
                        group.append((label, piece))
                        flush_group()
                        piece = []
                if piece:
                    group.append((label, piece))
                    flush_group()
                continue
            group.append((label, plines))
        flush_group()
    flush_recitals()
    return chunks


def chunk_fixed(meta: dict, lines: list[tuple[int, str]], size: int = 300, overlap: int = 50) -> list[dict]:
    """Baseline design: fixed windows of `size` words with `overlap`, ignoring
    structure. Location is the page range, the only thing a window knows."""
    words: list[tuple[int, str]] = [(p, w) for p, l in lines for w in l.split()]
    chunks = []
    step = size - overlap
    for start in range(0, len(words), step):
        window = words[start:start + size]
        if len(window) < 30:
            break
        pages = sorted({p for p, _ in window})
        loc = f"p. {pages[0]}" if pages[0] == pages[-1] else f"pp. {pages[0]}-{pages[-1]}"
        chunks.append({
            "text": f"{meta['source']}, {loc}\n" + " ".join(w for _, w in window),
            "source": meta["source"], "location": loc, "kind": "window", "article": "",
            "title": "", "chapter": "", "page_start": pages[0], "page_end": pages[-1],
            "words": len(window),
        })
    return chunks


def document_meta(path: Path) -> dict:
    """Known corpus file -> its metadata. Any other file: a sidecar JSON with the
    same name (e.g. code.pdf + code.json = {"source": ..., "title": ..., "url": ...})
    if there is one, else a name made from the file name."""
    meta = DOCUMENTS.get(path.name)
    if meta:
        return dict(meta)
    sidecar = path.with_suffix(".json")
    if sidecar.is_file():
        return {"source": path.stem, "title": path.stem, "url": "", **json.loads(sidecar.read_text(encoding="utf-8"))}
    return {"source": path.stem.replace("_", " "), "title": path.stem, "url": ""}


def chunk_file(path: str | Path, design: str = "structure") -> list[dict]:
    """PDF -> list of chunk dicts with text and citation metadata.

    design="structure" (one chunk per recital / article paragraph group / annex
    point) or "fixed" (300-word windows, used for documents that are not EU
    regulations, e.g. an added code of practice).
    """
    path = Path(path)
    meta = document_meta(path)
    lines = extract_lines(path)
    if design == "fixed":
        chunks = chunk_fixed(meta, lines)
    else:
        # Recital/article parsing only makes sense for an EU regulation; anything
        # else (guidance, codes of practice) gets page-cited fixed windows.
        is_regulation = any(l.startswith("HAVE ADOPTED THIS REGULATION") for _, l in lines)
        units = parse_units(lines) if is_regulation else []
        if not units:
            log(f"{path.name}: not structured as an EU regulation, using fixed-size chunks")
            chunks = chunk_fixed(meta, lines)
        else:
            chunks = chunk_units(meta, units)
    file_hash = hashlib.sha256(path.read_bytes()).hexdigest()
    for i, c in enumerate(chunks):
        c["file"] = path.name
        c["file_hash"] = file_hash
        c["design"] = design
        c["id"] = f"{design}:{path.stem}:{i:04d}"
    return chunks



# --------------------------------------------------------------------------- embed

class QuotaExhausted(RuntimeError):
    """The free tier's daily embedding quota is used up; re-run tomorrow."""


_client = None


def gemini():
    global _client
    if _client is None:
        from google import genai
        from api_key import load_api_key
        _client = genai.Client(api_key=load_api_key())
    return _client


def cache_key(text: str, task: str) -> str:
    return hashlib.sha256(f"{EMBED_MODEL}|{EMBED_DIM}|{task}|{text}".encode()).hexdigest()


def load_cache() -> dict[str, list[float]]:
    cache: dict[str, list[float]] = {}
    if CACHE_FILE.exists():
        with CACHE_FILE.open(encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                try:
                    row = json.loads(line)
                except json.JSONDecodeError:   # a torn last line from a crash
                    continue
                cache[row["key"]] = row["vector"]
    return cache


def append_cache(rows: list[tuple[str, list[float]]]) -> None:
    INDEX_DIR.mkdir(exist_ok=True)
    with CACHE_FILE.open("a", encoding="utf-8") as f:
        for key, vec in rows:
            f.write(json.dumps({"key": key, "vector": [round(x, 6) for x in vec]}) + "\n")


def embed_texts(texts: list[str], task: str, cache: dict | None = None) -> list[list[float]]:
    """Embed texts, using and extending the on-disk cache.

    Only texts without a saved vector are sent, in batches; each batch is saved
    as soon as it returns. Per-minute rate limits are waited out; the daily
    limit raises QuotaExhausted with everything so far already saved.
    """
    from google.genai import types, errors

    cache = load_cache() if cache is None else cache
    keys = [cache_key(t, task) for t in texts]
    todo = [i for i, k in enumerate(keys) if k not in cache]
    todo = list(dict.fromkeys(todo))
    for start in range(0, len(todo), BATCH_SIZE):
        batch = todo[start:start + BATCH_SIZE]
        for attempt in range(6):
            try:
                resp = gemini().models.embed_content(
                    model=EMBED_MODEL,
                    # One Content per text: a plain list of strings is read by
                    # gemini-embedding-2 as ONE multi-part input -> one vector.
                    contents=[types.Content(parts=[types.Part(text=texts[i])]) for i in batch],
                    config=types.EmbedContentConfig(task_type=task, output_dimensionality=EMBED_DIM),
                )
                break
            except errors.APIError as e:
                msg = str(e)
                if e.code == 429 and ("PerDay" in msg or "per day" in msg.lower()):
                    raise QuotaExhausted(msg[:300]) from e
                if e.code in (429, 500, 503) and attempt < 5:
                    wait = 15 * (attempt + 1)
                    log(f"  rate limited / server busy ({e.code}); waiting {wait}s")
                    time.sleep(wait)
                    continue
                raise
        if len(resp.embeddings) != len(batch):
            raise RuntimeError(f"asked for {len(batch)} embeddings, got {len(resp.embeddings)}")
        rows = [(keys[i], list(emb.values)) for i, emb in zip(batch, resp.embeddings)]
        append_cache(rows)
        cache.update(rows)
        log(f"  embedded {min(start + BATCH_SIZE, len(todo))}/{len(todo)} new texts")
    return [cache[k] for k in keys]


_query_cache: dict | None = None


def embed_query(query: str) -> list[float]:
    """Embed a search query. Query vectors are cached on disk too, so the same
    question asked again (in evaluation, by the agent) costs no quota."""
    global _query_cache
    if _query_cache is None:
        _query_cache = load_cache()
    return embed_texts([query.strip()], "RETRIEVAL_QUERY", _query_cache)[0]


# --------------------------------------------------------------------------- store

def collection(design: str = "structure"):
    import chromadb
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return client.get_or_create_collection(f"corpus_{design}", metadata={"hnsw:space": "cosine"})


METADATA_FIELDS = ["source", "location", "kind", "article", "title", "chapter",
                   "page_start", "page_end", "words", "file", "file_hash", "design"]


def embed_and_store(chunks: list[dict], design: str = "structure", cache: dict | None = None) -> int:
    """Embed chunks that have no saved vector, then upsert all into Chroma.
    Returns the number of chunks stored."""
    if not chunks:
        return 0
    vectors = embed_texts([c["text"] for c in chunks], "RETRIEVAL_DOCUMENT", cache)
    col = collection(design)
    for start in range(0, len(chunks), 500):
        part = chunks[start:start + 500]
        col.upsert(
            ids=[c["id"] for c in part],
            documents=[c["text"] for c in part],
            embeddings=vectors[start:start + 500],
            metadatas=[{k: c[k] for k in METADATA_FIELDS} for c in part],
        )
    return len(chunks)


def add_document(path: str | Path, design: str = "structure") -> dict:
    """Index one more file (what server.py's add_document tool calls).

    Policy for documents already in the index, decided by file content hash
    and file name:
      - same content already indexed      -> do nothing (no embedding spent);
      - same file name, different content -> a new version: its old chunks are
                                             deleted and the new ones stored;
      - otherwise                         -> chunk, embed and add.
    """
    path = Path(path).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"No such file: {path}")
    if path.suffix.lower() not in (".pdf", ".txt", ".md"):
        raise ValueError(f"Unsupported file type {path.suffix!r}; use .pdf, .txt or .md")
    col = collection(design)
    file_hash = hashlib.sha256(path.read_bytes()).hexdigest()
    if col.get(where={"file_hash": file_hash}, limit=1)["ids"]:
        return {"status": "already_indexed", "file": path.name, "chunks_added": 0}
    replaced = len(col.get(where={"file": path.name})["ids"])
    if replaced:
        col.delete(where={"file": path.name})
    chunks = chunk_file(path, design)
    stored = embed_and_store(chunks, design)
    return {"status": "replaced" if replaced else "added", "file": path.name,
            "source": chunks[0]["source"] if chunks else "", "chunks_added": stored,
            "chunks_removed": replaced}


# --------------------------------------------------------------------------- build

# Only one chunking is embedded: designs are compared on the search method
# (dense, hybrid, metadata filter), which costs no extra embeddings.
DESIGNS = ("structure",)


def build(designs=DESIGNS) -> None:
    cache = load_cache()
    log(f"{len(cache)} saved vectors in {CACHE_FILE.relative_to(ROOT)}")
    for design in designs:
        chunks = [c for name in DOCUMENTS for c in chunk_file(SOURCES_DIR / name, design)]
        (INDEX_DIR / f"chunks_{design}.jsonl").write_text(
            "".join(json.dumps(c, ensure_ascii=False) + "\n" for c in chunks), encoding="utf-8")
        log(f"[{design}] {len(chunks)} chunks, {sum(c['words'] for c in chunks)} words")
        # Drop chunks from an older chunking of the corpus files so the
        # collection matches what we just built (added documents are kept).
        col = collection(design)
        stale = set(col.get(where={"file": {"$in": list(DOCUMENTS)}})["ids"]) - {c["id"] for c in chunks}
        if stale:
            col.delete(ids=list(stale))
        embed_and_store(chunks, design, cache)
        log(f"[{design}] stored {col.count()} chunks")


if __name__ == "__main__" and "--dry-run" in sys.argv:
    for name in DOCUMENTS:
        p = SOURCES_DIR / name
        for design in DESIGNS:
            cs = chunk_file(p, design)
            ws = [c["words"] for c in cs]
            print(f"{name:12} {design:9} {len(cs):4} chunks, {sum(ws):6} words, "
                  f"max {max(ws)}, median {sorted(ws)[len(ws)//2]}")
    sys.exit(0)

if __name__ == "__main__":
    wanted = [d for d in DESIGNS if d in sys.argv[1:]] or list(DESIGNS)
    try:
        build(wanted)
    except QuotaExhausted as e:
        log(f"\nDaily embedding quota reached. Everything embedded so far is saved;\n"
            f"run `main.py index` again after the reset to continue.\n  ({e})")
        sys.exit(2)
