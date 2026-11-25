"""
Assignment 3: build the index (`uv run python main.py index`).

Corpus: the PDFs in corpus/ (credits and licences in corpus/sources.json).

Pipeline, one function per step so server.py's add_document can import them:

    extract_pages / clean_pages  -> lines with page number and "amended" flag
    parse_units                  -> articles, annexes or numbered paragraphs
    chunk_file(path, design)     -> chunks with source, location, page
    embed_and_store(chunks)      -> embeds ONLY chunks without a saved vector
    add_document(path)           -> what server.py's add_document tool calls

Two chunking designs are built so evaluate.py can compare them:

    fixed      windows of 300 words with 50 overlap that ignore the structure
               (the naive baseline; embedded with just the document title)
    structure  one chunk per legal unit: an article, an annex or a numbered
               paragraph of the guidelines. Units above MAX_WORDS are split at
               their own sub-structure (paragraph, definition, point (a)); small
               neighbours are packed up to TARGET_WORDS. Embedded with a header
               (document - location - title) so the vector knows where it is from.

Usage:
    uv run python main.py index                  # both designs, all of corpus/
    uv run python index.py --dry-run             # chunk counts, no API calls
    uv run python index.py --design structure    # one design only
    uv run python index.py --limit 400           # stop after 400 new embeddings
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import statistics
import sys
import time
from collections import Counter, namedtuple
from datetime import datetime, timezone
from pathlib import Path

import rag
from rag import log

ROOT = rag.ROOT
CORPUS_DIR = ROOT / "corpus"
SOURCES_FILE = CORPUS_DIR / "sources.json"

TARGET_WORDS = 300  # structure design: pack neighbouring pieces up to this many words
MAX_WORDS = 380  # structure design: a piece longer than this is split further
FIXED_WORDS, FIXED_OVERLAP = 300, 50
SUPPORTED = (".pdf", ".txt", ".md")

Line = namedtuple("Line", "text page amended indent")


class Unit:
    """A legal unit: an article, an annex, a numbered paragraph or a page."""

    def __init__(self, kind, label, num, title="", heading=""):
        self.kind, self.label, self.num, self.title, self.heading = kind, label, num, title, heading
        self.lines: list[Line] = []

    @property
    def lead(self) -> str:
        """How the unit's number appears in running text (used by the fixed design)."""
        if self.kind == "paragraph":
            return f"({self.num})"
        return f"{self.label}. {self.title}." if self.title else f"{self.label}."

    @property
    def words(self) -> int:
        return sum(len(line.text.split()) for line in self.lines)


# --------------------------------------------------------------------------- #
# 1. Extraction and cleaning
# --------------------------------------------------------------------------- #

HEADER_RE = re.compile(r"^\d{5}[A-Z]\d{4}\s+—\s+EN\s+—.*—\s*\d+\s*$")  # 02024R1689 — EN — 27.07.2026 — 001.001 — 41
MARKER_RE = re.compile(r"^▼(B|M\d+|C\d+)$")  # ▼B = original text, ▼M1 = amended by Regulation 2026/1744
BARE_NUMBER_RE = re.compile(r"^(\d{1,3}|[IVXL]{1,6})$")
PARA_RE = re.compile(r"^\((\d{1,3})\)\s+\S")
FOOTNOTE_RE = re.compile(r"^(\d{1,3})\s+[A-Z‘“(]")
HEADING_RE = re.compile(r"^((?:\d{1,2}\.)+\d*|[IVX]{1,4}\.)\s+[A-Z‘“]")  # "3.2. Title", "3. Title", "I. Title"


def read_pages(path: Path) -> list[list[tuple[str, int]]]:
    """Raw text of each page as (normalised line, indent). `layout` mode keeps words whole."""
    if path.suffix.lower() in (".txt", ".md"):
        raw_pages = [path.read_text(encoding="utf-8", errors="replace")]
    else:
        from pypdf import PdfReader

        raw_pages = [(p.extract_text(extraction_mode="layout") or "") for p in PdfReader(str(path)).pages]
    pages = []
    for raw in raw_pages:
        # soft hyphens split words over two lines ("tech­" / "niques"): rejoin them
        raw = re.sub("­[ \t]*\n[ \t]*", "", raw).replace("­", "")
        rows = []
        for line in raw.splitlines():
            text = " ".join(line.split())
            if text:
                rows.append((text, len(line) - len(line.lstrip(" "))))
        pages.append(rows)
    return pages


def detect_kind(pages) -> str:
    """'law' (Article headings), 'guidelines' (numbered paragraphs) or 'plain'."""
    headings = sum(1 for rows in pages for t, ind in rows if ind >= 25 and re.fullmatch(r"Article \d+[a-z]?", t))
    paragraphs = sum(1 for rows in pages for t, ind in rows if PARA_RE.match(t) and ind <= 8)
    if headings >= 5:
        return "law"
    return "guidelines" if paragraphs >= 10 else "plain"


def strip_footnotes(rows, prev_fn):
    """Cut the footnote block at the bottom of a guideline page.

    A block is a trailing run of lines starting 1 2 3 ... "41 See also ...", in
    the lower part of the page, with no paragraph marker after it, whose first
    number continues the previous page's. Returns (body rows, last footnote number).
    """
    cands = [(i, int(m.group(1))) for i, (t, _) in enumerate(rows) if (m := FOOTNOTE_RE.match(t))]
    if not cands:
        return rows, prev_fn
    run = [cands[-1]]
    for i, n in reversed(cands[:-1]):
        if n == run[0][1] - 1:
            run.insert(0, (i, n))
        else:
            break
    start, first_n = run[0]
    lower_part = start >= len(rows) * 0.45
    continues = prev_fn is None or first_n in (prev_fn, prev_fn + 1) or start >= len(rows) * 0.7
    no_paragraph_after = not any(PARA_RE.match(t) for t, _ in rows[start:])
    if lower_part and continues and no_paragraph_after and first_n <= 400:
        return rows[:start], run[-1][1]
    return rows, prev_fn


def clean_pages(pages, kind: str) -> list[Line]:
    """Pages -> one list of lines with page number and amended flag; headers, footnotes, TOC removed."""
    lines: list[Line] = []
    amended, prev_fn = False, None
    for pno, rows in enumerate(pages, 1):
        rows = list(rows)
        if rows and BARE_NUMBER_RE.match(rows[0][0]):  # page number printed first
            rows.pop(0)
        if rows and HEADER_RE.match(rows[0][0]):  # EUR-Lex running header
            rows.pop(0)
        if rows and BARE_NUMBER_RE.match(rows[-1][0]):  # printed page number last
            rows.pop()
        rows = [(t, i) for t, i in rows if t != "EN EN" and not HEADER_RE.match(t)]
        if sum(1 for t, _ in rows if re.search(r"\.{5,}", t)) >= 4:  # table of contents page
            continue
        if kind != "law":
            rows, prev_fn = strip_footnotes(rows, prev_fn)
        for text, indent in rows:
            marker = MARKER_RE.match(text)
            if marker:
                amended = marker.group(1).startswith("M")
                continue
            text = re.sub(r"[►◄]\s?[BM]?\d*\s?", "", text).strip()
            if kind == "guidelines":  # footnote call-numbers glued after punctuation: "notion.42 In"
                text = re.sub(r"(?<=[.,;:’”)])\d{1,3}(?=\s|$)", "", text)
            if text:
                lines.append(Line(text, pno, amended, indent))
    return lines


# --------------------------------------------------------------------------- #
# 2. Structure: articles / annexes / numbered paragraphs
# --------------------------------------------------------------------------- #


HEADING_LINE_RE = re.compile(r"^(Article \d+[a-z]?|ANNEX [IVXLC]+|CHAPTER [IVXLC]+|SECTION \d+)$")


def _centered_title(lines, i, limit=3):
    """Collect the centred title lines after a heading at lines[i]; return (title, next index).

    Stops at the next heading: "CHAPTER II / PROHIBITED AI PRACTICES / Article 5" must not
    swallow Article 5 as part of the chapter title.
    """
    parts, j = [], i + 1
    while j < len(lines) and len(parts) < limit and not HEADING_LINE_RE.match(lines[j].text):
        if parts and lines[j].indent < 25:  # first line always counts; wrapped lines are centred
            break
        parts.append(lines[j].text)
        j += 1
    return " ".join(parts).strip("'’ "), j


def parse_law(lines) -> list[Unit]:
    units, cur, chapter, i = [], None, "", 0
    while i < len(lines):
        ln = lines[i]
        t, centered = ln.text, ln.indent >= 25
        if centered and (re.fullmatch(r"Article \d+[a-z]?", t) or re.fullmatch(r"ANNEX [IVXLC]+", t)):
            title, j = _centered_title(lines, i)
            if t.startswith("Article"):
                cur = Unit("article", t, t.split()[1], title, chapter)
            else:
                cur = Unit("annex", f"Annex {t.split()[1]}", t.split()[1], title, "")
            units.append(cur)
            i = j
            continue
        if centered and re.fullmatch(r"CHAPTER [IVXLC]+", t):
            title, i = _centered_title(lines, i, 2)
            name = re.sub(r"\b(ai|eu)\b", lambda m: m.group(1).upper(), title.capitalize())
            chapter = f"Chapter {t.split()[1]} - {name}"
            continue
        if centered and re.fullmatch(r"SECTION \d+", t):
            _, i = _centered_title(lines, i, 2)
            continue
        if cur is not None:
            cur.lines.append(ln)
        i += 1
    return units


def parse_guidelines(lines) -> list[Unit]:
    units, cur, last, heading = [], None, 0, ""
    # PDF layout indentation is relative to the page: some pages start their text at column 16
    base: dict[int, int] = {}
    for ln in lines:
        base[ln.page] = min(base.get(ln.page, ln.indent), ln.indent)
    for ln in lines:
        m = PARA_RE.match(ln.text)
        if m and ln.indent <= base[ln.page] + 8:
            n = int(m.group(1))
            if n == last + 1 or (last > 0 and last + 1 < n <= last + 3):
                cur = Unit("paragraph", f"paragraph ({n})", n, "", heading)
                cur.lines.append(Line(re.sub(r"^\(\d{1,3}\)\s+", "", ln.text), ln.page, ln.amended, ln.indent))
                units.append(cur)
                last = n
                continue
        if (
            HEADING_RE.match(ln.text)
            and len(ln.text) <= 110
            and not ln.text.endswith((".", ";", ",", ":"))
            and not PARA_RE.match(ln.text)
        ):
            heading = ln.text
            continue
        if cur is not None:
            cur.lines.append(ln)
    return units


def parse_plain(lines) -> list[Unit]:
    by_page: dict[int, Unit] = {}
    for ln in lines:
        unit = by_page.setdefault(ln.page, Unit("page", f"page {ln.page}", ln.page))
        unit.lines.append(ln)
    return list(by_page.values())


def parse_units(lines, kind: str) -> list[Unit]:
    return {"law": parse_law, "guidelines": parse_guidelines}.get(kind, parse_plain)(lines)


# --------------------------------------------------------------------------- #
# 3. Chunking
# --------------------------------------------------------------------------- #

LEVELS = [  # sub-structure inside an article, from the largest piece to the smallest
    re.compile(r"^(\d{1,2}[a-z]?)\.\s+\S"),  # numbered paragraph: "1. The following ...", "1a. ..." (added in 2026)
    re.compile(r"^\((\d{1,3})\)\s+\S"),  # definition / list item: "(1) 'AI system' means ..."
    re.compile(r"^\(([a-z]{1,2})\)\s+\S"),  # point: "(a) the placing on the market ..."
]


class Seg:
    """A piece of a unit that carries its own label, e.g. 'Article 5(1)(c)'."""

    def __init__(self, unit: Unit, label: str, lines: list[Line]):
        self.unit, self.label, self.lines = unit, label, lines
        self.text = "\n".join(l.text for l in lines)
        self.words = len(self.text.split())


def split_lines(unit: Unit, lines: list[Line], label: str, level: int = 0) -> list[Seg]:
    if sum(len(l.text.split()) for l in lines) <= MAX_WORDS or level >= len(LEVELS):
        return [Seg(unit, label, lines)]
    idxs = [i for i, l in enumerate(lines) if LEVELS[level].match(l.text)]
    if idxs:
        smallest = min(lines[i].indent for i in idxs)
        idxs = [i for i in idxs if lines[i].indent <= smallest + 2]
    if len(idxs) < 2:
        return split_lines(unit, lines, label, level + 1)
    segs: list[Seg] = []
    if idxs[0] > 0:
        segs += split_lines(unit, lines[: idxs[0]], label, level + 1)
    for a, b in zip(idxs, idxs[1:] + [len(lines)]):
        ident = LEVELS[level].match(lines[a].text).group(1)
        segs += split_lines(unit, lines[a:b], f"{label}({ident})", level + 1)
    return segs


def window_split(seg: Seg) -> list[Seg]:
    """A piece with no sub-structure left that is still too long: overlapping windows."""
    words = seg.text.split()
    if len(words) <= MAX_WORDS:
        return [seg]
    out, start, step = [], 0, TARGET_WORDS - 40
    while start < len(words):
        end = min(len(words), start + TARGET_WORDS)
        amended = any(l.amended for l in seg.lines)
        piece = Seg(seg.unit, seg.label, [Line(" ".join(words[start:end]), seg.lines[0].page, amended, 0)])
        piece.page_to = seg.lines[-1].page  # the window may run onto the piece's last page
        out.append(piece)
        if end == len(words):
            break
        start += step
    return out


def make_segments(unit: Unit) -> list[Seg]:
    if unit.kind in ("article", "annex"):
        segs = split_lines(unit, unit.lines, unit.label)
    else:
        segs = [Seg(unit, unit.label, unit.lines)]
    return [piece for s in segs for piece in window_split(s)]


def pack(segs: list[Seg]) -> list[list[Seg]]:
    """Greedily join neighbouring pieces up to TARGET_WORDS; never across articles or headings."""
    groups: list[list[Seg]] = []
    cur: list[Seg] = []
    total = 0
    for s in segs:
        boundary = cur and (cur[-1].unit.kind in ("article", "annex") and cur[-1].unit is not s.unit)
        boundary = boundary or (cur and cur[-1].unit.heading != s.unit.heading)
        if cur and (boundary or total + s.words > TARGET_WORDS):
            groups.append(cur)
            cur, total = [], 0
        cur.append(s)
        total += s.words
    if cur:
        groups.append(cur)
    return groups


def range_label(first: str, last: str, kind: str) -> str:
    if first == last:
        return first
    if kind == "paragraph":  # paragraph (46) ... paragraph (49) -> paragraphs (46)-(49)
        return f"paragraphs {first.split(' ', 1)[1]}–{last.split(' ', 1)[1]}"
    head = first.split(" ", 1)[0]
    return f"{first}–{last.split(' ', 1)[1]}" if last.startswith(head) else f"{first}–{last}"


def _metadata(units: list[Unit], pages: list[int], amended: bool) -> dict:
    nums = [u.num for u in units if u.kind == "paragraph"]
    return {
        "articles": sorted({u.num for u in units if u.kind == "article"}, key=lambda a: (int(re.match(r"\d+", a).group()), a)),
        "annexes": sorted({u.num for u in units if u.kind == "annex"}),
        "para_from": min(nums) if nums else None,
        "para_to": max(nums) if nums else None,
        "page_from": min(pages),
        "page_to": max(pages),
        "page": str(min(pages)) if min(pages) == max(pages) else f"{min(pages)}–{max(pages)}",
        "amended": amended,
    }


def structure_chunks(units: list[Unit], doc: str) -> list[dict]:
    segs = [s for u in units for s in make_segments(u)]
    chunks = []
    for group in pack(segs):
        first, last = group[0], group[-1]
        kind = first.unit.kind
        location = range_label(first.label, last.label, kind)
        pages = [l.page for s in group for l in s.lines] + [getattr(s, "page_to", 0) for s in group]
        pages = [p for p in pages if p]
        context = first.unit.title if first.unit.kind in ("article", "annex") else first.unit.heading
        title = f"{doc} — {location}" + (f" — {context}" if context else "")
        chunks.append(
            {
                "doc": doc,
                "location": location,
                "title": title[:220],
                "text": "\n".join(s.text for s in group),
                **_metadata(list({id(s.unit): s.unit for s in group}.values()), pages, any(l.amended for s in group for l in s.lines)),
            }
        )
    return chunks


def fixed_chunks(units: list[Unit], doc: str) -> list[dict]:
    """Naive baseline: windows over the running text, boundaries ignore articles and paragraphs."""
    words, owner = [], []  # owner = (unit index, page, amended) per word
    for ui, u in enumerate(units):
        for w in u.lead.split():
            words.append(w)
            owner.append((ui, u.lines[0].page if u.lines else 0, False))
        for ln in u.lines:
            for w in ln.text.split():
                words.append(w)
                owner.append((ui, ln.page, ln.amended))
    chunks, start, step = [], 0, FIXED_WORDS - FIXED_OVERLAP
    while start < len(words):
        end = min(len(words), start + FIXED_WORDS)
        own = owner[start:end]
        uis = sorted({o[0] for o in own})
        covered = [units[i] for i in uis]
        a, b = covered[0], covered[-1]
        chunks.append(
            {
                "doc": doc,
                "location": range_label(a.label, b.label, a.kind),
                "title": doc,
                "text": " ".join(words[start:end]),
                **_metadata(covered, [o[1] for o in own if o[1]] or [1], any(o[2] for o in own)),
            }
        )
        if end == len(words):
            break
        start += step
    return chunks


def doc_info(stem: str) -> dict:
    try:
        for d in json.loads(SOURCES_FILE.read_text(encoding="utf-8"))["documents"]:
            if Path(d["file"]).stem == stem:
                return d
    except (OSError, ValueError, KeyError):
        pass
    return {"short_title": stem}


def parse_file(path: Path) -> tuple[list[Unit], str, int]:
    pages = read_pages(path)
    kind = detect_kind(pages)
    return parse_units(clean_pages(pages, kind), kind), kind, len(pages)


def chunk_units(units: list[Unit], path: Path, design: str) -> list[dict]:
    stem = path.stem
    doc = doc_info(stem)["short_title"]
    chunks = structure_chunks(units, doc) if design == "structure" else fixed_chunks(units, doc)
    for n, c in enumerate(chunks):
        c.update({"id": f"{design}:{stem}:{n:04d}", "design": design, "source": stem, "words": len(c["text"].split())})
        c["key"] = rag.vector_key(rag.chunk_embed_text(c))
    return chunks


def chunk_file(path, design: str) -> list[dict]:
    """Extract, clean and chunk one file. Metadata on every chunk: source, location, page."""
    path = Path(path)
    units, _, _ = parse_file(path)
    return chunk_units(units, path, design)


# --------------------------------------------------------------------------- #
# 4. Embedding and storage
# --------------------------------------------------------------------------- #


def embed_and_store(chunks: list[dict], limit: int | None = None, deadline: float | None = None) -> tuple[int, bool]:
    """Embed the chunks that have no saved vector and save each batch at once.

    Returns (new vectors embedded, whether the daily quota ran out).
    """
    cache = rag.load_vector_cache()
    todo: dict[str, dict] = {}
    for c in chunks:
        if c["key"] not in cache:
            todo.setdefault(c["key"], c)
    todo_list = list(todo.values())
    if limit is not None:
        todo_list = todo_list[:limit]
    done = 0
    for i in range(0, len(todo_list), rag.BATCH_SIZE):
        if deadline is not None and time.monotonic() > deadline:
            log("Time budget reached; run again to continue (saved vectors are kept).")
            break
        batch = todo_list[i : i + rag.BATCH_SIZE]
        try:
            vectors = rag.embed_batch([rag.chunk_embed_text(c) for c in batch])
        except rag.QuotaExhausted as error:
            log(f"Daily embedding quota exhausted after {done} new vectors (they are saved). {error}")
            return done, True
        rag.save_vectors([c["key"] for c in batch], vectors)
        done += len(batch)
        log(f"  embedded {done}/{len(todo_list)}")
    return done, False


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_registry() -> dict:
    try:
        return json.loads(rag.REGISTRY_FILE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def save_registry(registry: dict) -> None:
    rag.INDEX_DIR.mkdir(parents=True, exist_ok=True)
    rag.REGISTRY_FILE.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def corpus_files() -> list[Path]:
    return sorted(p for p in CORPUS_DIR.iterdir() if p.suffix.lower() in SUPPORTED) if CORPUS_DIR.is_dir() else []


def describe(chunks: list[dict]) -> str:
    w = [c["words"] for c in chunks]
    return f"{len(chunks)} chunks, words min/median/max = {min(w)}/{int(statistics.median(w))}/{max(w)}"


def build_index(designs=rag.DESIGNS, limit: int | None = None, dry_run: bool = False, samples: int = 0, max_seconds: float | None = None) -> bool:
    """Index everything in corpus/. Returns True when every chunk has a saved vector."""
    files = corpus_files()
    if not files:
        raise SystemExit(f"No documents in {CORPUS_DIR}. Put the PDFs there (see corpus/sources.json).")
    registry = load_registry()
    parsed = {}
    for path in files:
        units, kind, n_pages = parse_file(path)
        parsed[path] = (units, kind, n_pages)
        words = sum(u.words for u in units)
        extra = ""
        if kind == "law":
            arts = [u.num for u in units if u.kind == "article"]
            nums = [int(re.match(r"\d+", a).group()) for a in arts]
            out_of_order = [arts[i] for i in range(1, len(nums)) if nums[i] < nums[i - 1]]
            extra = f", {len(arts)} articles, {len(units) - len(arts)} annexes, out-of-order: {out_of_order or 'none'}"
        elif kind == "guidelines":
            nums = [u.num for u in units]
            gaps = [n for n in range(1, max(nums) + 1) if n not in nums] if nums else []
            extra = f", paragraphs 1-{max(nums) if nums else 0}, missing: {gaps or 'none'}"
        log(f"{path.name}: {n_pages} pages, kind={kind}, {len(units)} units, {words} words{extra}")

    corpus_stems = {p.stem for p in files}
    deadline = time.monotonic() + max_seconds if max_seconds else None
    complete = True
    for design in designs:
        chunks = []
        for path, (units, _, _) in parsed.items():
            chunks += chunk_units(units, path, design)
        kept = [c for c in rag.read_chunks(design) if c["source"] not in corpus_stems]  # documents added with add_document
        log(f"design '{design}': {describe(chunks)}" + (f" (+{len(kept)} chunks of added documents kept)" if kept else ""))
        for c in chunks[: samples]:
            log(f"--- {c['id']} | {c['location']} | p.{c['page']} | {c['words']} words | amended={c['amended']}\n    title: {c['title']}\n    {c['text'][:300]!r}")
        cache = rag.load_vector_cache()
        missing = len({c["key"] for c in chunks if c["key"] not in cache})
        log(f"  vectors to embed: {missing} (saved already: {len(chunks) - missing})")
        if dry_run:
            continue
        rag.write_chunks(design, chunks + kept)
        done, exhausted = embed_and_store(chunks, limit, deadline)
        if limit is not None:
            limit -= done
        complete &= not exhausted and missing - done == 0
        for path, (units, kind, n_pages) in parsed.items():
            entry = registry.setdefault(path.stem, {})
            entry.update({"file": str(path.relative_to(ROOT)), "sha256": file_sha256(path), "kind": kind, "pages": n_pages})
            entry.setdefault("designs", {})[design] = sum(1 for c in chunks if c["source"] == path.stem)
        if limit is not None and limit <= 0:
            log("Embedding limit reached; run again to continue.")
            complete = False
            break
    if not dry_run:
        save_registry(registry)
        if not rag.CONFIG_FILE.is_file():
            rag.CONFIG_FILE.write_text(json.dumps({"design": rag.DEFAULT_DESIGN}, indent=2) + "\n", encoding="utf-8")
    return complete


# --------------------------------------------------------------------------- #
# 5. add_document: what server.py's tool calls
# --------------------------------------------------------------------------- #


def add_document(path: str, design: str | None = None) -> dict:
    """Index one more file with the same pipeline.

    Already indexed (same file hash): nothing is embedded, the answer says so.
    Same name but different content: the old chunks are replaced (new version).
    Returns a summary dict; raises ValueError for a missing or unsupported file.
    """
    design = design or rag.get_design()
    p = Path(path).expanduser()
    if not p.is_absolute():
        p = ROOT / p
    if not p.is_file():
        raise ValueError(f"File not found: {path}")
    if p.suffix.lower() not in SUPPORTED:
        raise ValueError(f"Unsupported file type '{p.suffix}'. Supported: {', '.join(SUPPORTED)}")
    sha = file_sha256(p)
    registry = load_registry()
    entry = registry.get(p.stem)
    if entry and entry.get("sha256") == sha and design in entry.get("designs", {}):
        return {"status": "already_indexed", "source": p.stem, "chunks": entry["designs"][design], "new_embeddings": 0}
    units, kind, n_pages = parse_file(p)
    chunks = chunk_units(units, p, design)
    if not chunks:
        raise ValueError("No text could be extracted from this file (a scanned PDF needs OCR first).")
    replaced = bool(entry and entry.get("sha256") != sha)
    others = [c for c in rag.read_chunks(design) if c["source"] != p.stem]
    done, exhausted = embed_and_store(chunks)
    if exhausted:
        raise rag.QuotaExhausted("Daily embedding quota exhausted; nothing was added. Try again after 09:00 (Spain).")
    rag.write_chunks(design, others + chunks)
    registry[p.stem] = {
        "file": str(p), "sha256": sha, "kind": kind, "pages": n_pages,
        "added": datetime.now(timezone.utc).isoformat(timespec="seconds"),
        "designs": {**(entry or {}).get("designs", {}), design: len(chunks)},
    }
    save_registry(registry)
    rag.load_store(design, refresh=True)
    return {"status": "replaced_previous_version" if replaced else "added", "source": p.stem, "chunks": len(chunks), "new_embeddings": done}


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the index from corpus/.")
    parser.add_argument("--dry-run", action="store_true", help="count chunks; no files written, no API calls")
    parser.add_argument("--design", action="append", choices=rag.DESIGNS, help="only this design (repeatable)")
    parser.add_argument("--limit", type=int, help="stop after this many NEW embeddings")
    parser.add_argument("--samples", type=int, default=0, help="print this many example chunks per design")
    parser.add_argument("--max-seconds", type=float, help="stop starting new embedding batches after this long")
    args = parser.parse_args()
    complete = build_index(tuple(args.design or rag.DESIGNS), args.limit, args.dry_run, args.samples, args.max_seconds)
    if not args.dry_run:
        print("Index complete." if complete else "Index NOT complete: run `uv run python main.py index` again (daily quota or --limit).")
        if not complete and not (args.limit or args.max_seconds):
            sys.exit(1)


if __name__ == "__main__":
    main()
