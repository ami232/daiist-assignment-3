"""
Assignment 3: build the index (`main.py index`).

Pipeline: extract -> clean -> chunk (with source, page and section) -> embed -> store in index/.

    uv run python main.py index                 # build everything, embed only what has no vector
    uv run python index.py --dry-run            # chunk and count, no API calls (free)

What is stored in index/ (all plain text, all committed):
    chunks_structure.jsonl   chunks cut at headings / numbered paragraphs (design 1)
    chunks_fixed.jsonl       chunks cut every N words, ignoring structure (design 2)
    vectors.jsonl            one saved vector per distinct embedded text, appended as we go
    documents.json           which files are indexed (hash, pages, words, chunks)

The corpus is described in corpus/manifest.json (title, reference, URL, licence and the
page range we index). Per-file steps are plain functions (`chunk_file`, `embed_and_store`,
`index_file`): server.py's add_document tool imports them instead of re-implementing them.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import statistics
import sys
import time
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"
MANIFEST_FILE = CORPUS_DIR / "manifest.json"
VECTORS_FILE = INDEX_DIR / "vectors.jsonl"
DOCUMENTS_FILE = INDEX_DIR / "documents.json"

# --- settings you can defend in the report --------------------------------------------
EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768            # Google recommends 768 / 1536 / 3072; 768 keeps index/ small
EMBED_BATCH = 16           # texts per API call (every text counts against the daily quota)
DESIGNS = ("structure", "fixed")   # order = embedding priority if the daily quota runs out
SERVING_DESIGN = "structure"       # which design server.py searches (set it by the numbers)
STRUCT_TARGET, STRUCT_MAX = 250, 330   # words per structure-based chunk (aim / hard limit)
FIXED_WORDS, FIXED_STRIDE = 250, 225   # fixed design: window and step (25 words overlap)
MAX_NEW_CHUNKS_PER_DOCUMENT = 400      # guard for add_document: protects the free quota
ALLOWED_SUFFIXES = {".pdf", ".txt", ".md", ".html", ".htm"}


class QuotaExhausted(RuntimeError):
    """The daily embedding quota is used up. Everything embedded so far is already saved."""


# --- data ------------------------------------------------------------------------------
@dataclass
class Chunk:
    id: str
    source: str           # short document id used in citations, e.g. EBA-GL-2017-16
    title: str
    design: str
    section: str          # nearest numbered heading above the chunk ("" if none)
    page_start: int
    page_end: int
    paras: str            # numbered paragraphs inside the chunk, e.g. "26-29" ("" if none)
    text: str
    embed_text: str = field(default="", repr=False)

    @property
    def vec_key(self) -> str:
        return hashlib.sha1(self.embed_text.encode("utf-8")).hexdigest()

    def to_record(self) -> dict:
        d = asdict(self)
        d.pop("embed_text")
        d["vec_key"] = self.vec_key
        d["embed_text"] = self.embed_text
        return d


# --- 1. extract ------------------------------------------------------------------------
def extract_pages(path: Path) -> list[tuple[int, str]]:
    """(page number, raw text) per page. PDF page number = printed page number for these documents."""
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        from pypdf import PdfReader

        reader = PdfReader(str(path), strict=False)
        return [(i + 1, page.extract_text() or "") for i, page in enumerate(reader.pages)]
    raw = path.read_text(encoding="utf-8", errors="replace")
    if suffix in {".html", ".htm"}:
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(raw, "html.parser")
        for tag in soup(["script", "style", "nav", "footer", "header"]):
            tag.decompose()
        raw = soup.get_text("\n")
    if "\f" in raw:
        return [(i + 1, part) for i, part in enumerate(raw.split("\f"))]
    return [(1, raw)]  # not paged: location is the section only


# --- 2. clean --------------------------------------------------------------------------
_NUM = re.compile(r"\d+")


def fix_spacing(line: str) -> str:
    """pypdf leaves gaps such as "institution ’s", "risk -taking", "a  credit": close them."""
    line = line.replace(" ", " ").replace("‑", "-").replace("­", "")
    line = re.sub(r"\s+", " ", line).strip()
    line = re.sub(r"\s+([,.;:)\]’'])", r"\1", line)
    line = re.sub(r"([(\[])\s+", r"\1", line)
    line = re.sub(r"(?<=\w) -(?=\w)", "-", line)   # "risk -taking" -> "risk-taking"
    line = re.sub(r"(?<=\w)- (?=[a-z])", "-", line)  # "non- compliant" -> "non-compliant"
    return line


def clean_pages(pages: list[tuple[int, str]]) -> list[tuple[int, list[str]]]:
    """Per page: non-empty lines without running headers/footers and bare page numbers."""
    split = [(n, [fix_spacing(l) for l in text.split("\n")]) for n, text in pages]
    split = [(n, [l for l in lines if l]) for n, lines in split]
    repeated: set[str] = set()
    if len(split) >= 6:
        counts: dict[str, int] = {}
        for _, lines in split:
            for l in set(lines[:4] + lines[-3:]):
                counts[_NUM.sub("#", l.lower())] = counts.get(_NUM.sub("#", l.lower()), 0) + 1
        repeated = {k for k, c in counts.items() if c >= max(4, 0.25 * len(split))}
    out = []
    for n, lines in split:
        keep = []
        for i, l in enumerate(lines):
            edge = i < 4 or i >= len(lines) - 3
            if edge and _NUM.sub("#", l.lower()) in repeated:
                continue
            if edge and re.fullmatch(r"\d{1,3}", l):
                continue
            keep.append(l)
        out.append((n, keep))
    return out


# --- 3. structure: headings and numbered paragraphs ---------------------------------------
_H_MULTI = re.compile(r"^\d{1,2}(?:\.\d{1,2}){1,4}\.?\s+[A-Z(]")
_H_ONE = re.compile(r"^\d{1,2}\.\s+[A-Z]")
_H_WORD = re.compile(r"^(Title\s+[IVX]+|Annex\s*\d*|Section\s+\d+)\s*[\u2013\u2014:-]\s*\S")
_H_NODOT = re.compile(r"^(\d{1,2})\s+[A-Z][a-z]")
_PARA = re.compile(r"^(\d{1,3})\.\s+\S")


def _norm(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", " ", text.lower()).strip()


def toc_headings(cleaned: list[tuple[int, list[str]]], before_page: int) -> set[str]:
    """Headings listed in the document's own Contents pages (lines ending in a page number).

    The Contents list is the reliable source of what is a heading: numbered list items in the
    annexes ("12. Information on the collateral") look like headings but are not in it."""
    keys = set()
    for n, lines in cleaned:
        if n >= before_page:
            continue
        for line in lines:
            m = re.match(r"^(.*?\S)\s*\.{0,}\s+(\d{1,3})$", line)
            if m and len(m.group(1)) >= 4:
                keys.add(_norm(m.group(1)))
    return keys


def classify_line(line: str, nxt: str | None, toc: set[str] | None = None) -> str:
    """'heading', 'para' (a numbered paragraph starts) or 'text'."""
    words = len(line.split())
    ends_sentence = line.rstrip().endswith((".", ";", ":", ","))
    continues = bool(nxt) and nxt[0].islower()
    if toc:
        k = _norm(line)
        if len(k) >= 6 and words <= 24 and not ends_sentence and (k in toc or (len(k) >= 18 and any(t.startswith(k) for t in toc))):
            return "heading"
    if _H_WORD.match(line) and words <= 14 and not ends_sentence:
        return "heading"
    if _H_MULTI.match(line) and words <= 18 and len(line) <= 115 and not ends_sentence and not continues:
        return "heading"
    if not toc and _H_ONE.match(line) and words <= 12 and len(line) <= 80 and not ends_sentence and not continues:
        return "heading"  # only without a Contents list to check against
    if _PARA.match(line):
        return "para"
    if _H_NODOT.match(line) and words <= 12 and len(line) <= 80 and not ends_sentence and not continues:
        return "heading?"   # "5 PD estimation": accepted below only if it is the next number in sequence
    return "text"


@dataclass
class Stream:
    """The included pages as a stream of words, each tagged with page, section and structure."""
    words: list[str] = field(default_factory=list)
    pages: list[int] = field(default_factory=list)
    sections: list[str] = field(default_factory=list)
    paras: list[int] = field(default_factory=list)       # numbered paragraph the word belongs to (0 = none)
    starts: list[str] = field(default_factory=list)      # "", "para" or "heading" before the word
    headings: list[tuple[int, str]] = field(default_factory=list)  # (page, heading)


def build_stream(cleaned: list[tuple[int, list[str]]], pages: tuple[int, int] | None = None,
                 skip_heading_pages: list | tuple = ()) -> Stream:
    s = Stream()
    section, para = "", 0
    flat = [(n, l) for n, lines in cleaned if pages is None or pages[0] <= n <= pages[1] for l in lines]
    toc = toc_headings(cleaned, pages[0]) if pages else set()
    kinds = [classify_line(line, flat[i + 1][1] if i + 1 < len(flat) else None, toc) for i, (_, line) in enumerate(flat)]
    expected = 1
    for i, k in enumerate(kinds):
        if k == "heading?":
            number = int(_H_NODOT.match(flat[i][1]).group(1))
            kinds[i] = "heading" if number == expected else "text"
            expected = number + 1 if number == expected else expected
    for i, (n, _) in enumerate(flat):
        if kinds[i] == "heading" and any(a <= n <= b for a, b in skip_heading_pages):
            kinds[i] = "text"
    i = 0
    while i < len(kinds):  # three or more "headings" in a row are a list of cross-references, not headings
        if kinds[i] == "heading":
            j = i
            while j < len(kinds) and kinds[j] == "heading":
                j += 1
            if j - i >= 3:
                kinds[i:j] = ["text"] * (j - i)
            i = j
        else:
            i += 1
    for (n, line), kind in zip(flat, kinds):
        if kind == "heading":
            section, para = line, 0
            s.headings.append((n, line))
        elif kind == "para":
            para = int(_PARA.match(line).group(1))
        first = True
        for w in line.split():
            s.words.append(w)
            s.pages.append(n)
            s.sections.append(section)
            s.paras.append(para)
            s.starts.append(kind if first and kind in ("heading", "para") else "")
            first = False
    return s


def _para_label(paras: list[int]) -> str:
    nums = sorted({p for p in paras if p})
    if not nums:
        return ""
    return str(nums[0]) if nums[0] == nums[-1] else f"{nums[0]}-{nums[-1]}"


def _text(words: list[str]) -> str:
    return fix_spacing(" ".join(words))


# --- 4. chunk --------------------------------------------------------------------------
_NOT_A_STOP = re.compile(r"^(?:[a-zA-Z]{1,2}|\(?[ivx]+\)?|\d{1,3}|e\.g|i\.e|etc|no|art|para|paras|p|pp)\.$", re.I)


def _sentence_cuts(words: list[str]) -> list[int]:
    """Indexes where a new sentence or list item starts (previous word ends with . ; : ? !).

    List labels ("a.", "(ii).", "12.") and abbreviations ("e.g.", "Art.") are not sentence ends."""
    cuts = []
    for i in range(1, len(words)):
        prev = words[i - 1]
        if prev.endswith((".", ";", ":", "?", "!")) and not _NOT_A_STOP.match(prev):
            cuts.append(i)
    return cuts


def _split_long(lo: int, hi: int, s: Stream, hard_max: int) -> list[tuple[int, int]]:
    """Split a very long unit into equal-sized pieces (each <= hard_max) at sentence boundaries."""
    n = hi - lo
    pieces = max(1, -(-n // hard_max))  # ceil
    if pieces == 1:
        return [(lo, hi)]
    cuts = [c + lo for c in _sentence_cuts(s.words[lo:hi])]
    out, start = [], lo
    for k in range(1, pieces):
        ideal = lo + round(k * n / pieces)
        near = [c for c in cuts if abs(c - ideal) <= 0.3 * n / pieces and start < c < hi]
        best = min(near, key=lambda c: abs(c - ideal), default=ideal)
        out.append((start, best))
        start = best
    out.append((start, hi))
    return out


def chunk_structure(s: Stream, target: int = STRUCT_TARGET, hard_max: int = STRUCT_MAX) -> list[tuple[int, int]]:
    """Chunk boundaries (word index ranges) that never cross a heading and prefer paragraph edges."""
    n = len(s.words)
    # blocks = text between headings; units = numbered paragraphs inside a block
    block_starts = [i for i in range(n) if s.starts[i] == "heading"]
    if not block_starts or block_starts[0] != 0:
        block_starts = [0] + block_starts
    block_starts.append(n)
    # a heading followed at once by another heading (parent title) joins the block below it
    block_starts = [b for k, b in enumerate(block_starts[:-1]) if block_starts[k + 1] - b >= 15] + [n]
    if block_starts[0] != 0:
        block_starts = [0] + block_starts
    chunks: list[tuple[int, int]] = []
    for b in range(len(block_starts) - 1):
        lo, hi = block_starts[b], block_starts[b + 1]
        unit_starts = [i for i in range(lo, hi) if s.starts[i] == "para" or i == lo]
        units = [(unit_starts[k], unit_starts[k + 1] if k + 1 < len(unit_starts) else hi) for k in range(len(unit_starts))]
        flat: list[tuple[int, int]] = []
        for a, z in units:
            flat.extend(_split_long(a, z, s, hard_max) if z - a > hard_max else [(a, z)])
        cur: tuple[int, int] | None = None
        for a, z in flat:
            if cur is None:
                cur = (a, z)
                continue
            cur_len, add = cur[1] - cur[0], z - a
            if cur_len + add > hard_max or (cur_len >= target * 0.6 and cur_len + add > target):
                chunks.append(cur)
                cur = (a, z)
            else:
                cur = (cur[0], z)
        if cur:
            if chunks and chunks[-1][1] == cur[0] and cur[1] - cur[0] < 60 and (cur[1] - chunks[-1][0]) <= hard_max + 40:
                chunks[-1] = (chunks[-1][0], cur[1])  # do not leave a tiny orphan chunk
            else:
                chunks.append(cur)
    return chunks


def chunk_fixed(s: Stream, size: int = FIXED_WORDS, stride: int = FIXED_STRIDE) -> list[tuple[int, int]]:
    n = len(s.words)
    out, i = [], 0
    while i < n:
        out.append((i, min(i + size, n)))
        if i + size >= n:
            break
        i += stride
    return out


def make_chunks(s: Stream, ranges: list[tuple[int, int]], source: str, title: str, design: str) -> list[Chunk]:
    chunks = []
    for k, (a, z) in enumerate(ranges):
        text = _text(s.words[a:z])
        section = s.sections[a]
        if design == "structure":
            # the heading goes in front of the text: it is the context a lone paragraph lacks
            embed_text = f"title: {title} | {section} | text: {text}" if section else f"title: {title} | text: {text}"
        else:
            embed_text = f"title: none | text: {text}"
        chunks.append(Chunk(
            id=f"{source}:{design}:{k:04d}", source=source, title=title, design=design,
            section=section, page_start=s.pages[a], page_end=s.pages[z - 1],
            paras=_para_label(s.paras[a:z]), text=text, embed_text=embed_text,
        ))
    return chunks


# --- manifest, documents -----------------------------------------------------------------
def load_manifest() -> list[dict]:
    if not MANIFEST_FILE.is_file():
        return []
    return json.loads(MANIFEST_FILE.read_text(encoding="utf-8"))["documents"]


def resolve_file(entry: dict) -> Path | None:
    hits = sorted(CORPUS_DIR.glob(entry["file_glob"]))
    return hits[0] if hits else None


def manifest_entry_for(path: Path) -> dict | None:
    for e in load_manifest():
        if resolve_file(e) and resolve_file(e).resolve() == path.resolve():
            return e
    return None


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_documents() -> dict:
    if DOCUMENTS_FILE.is_file():
        return json.loads(DOCUMENTS_FILE.read_text(encoding="utf-8"))
    return {}


def save_documents(docs: dict) -> None:
    INDEX_DIR.mkdir(exist_ok=True)
    DOCUMENTS_FILE.write_text(json.dumps(docs, indent=1, sort_keys=True), encoding="utf-8")


_CLEAN_CACHE: dict[tuple[str, float], list] = {}


def cleaned_pages(path: Path) -> list[tuple[int, list[str]]]:
    """extract + clean, remembered per file so the second design does not read the PDF again."""
    key = (str(path), path.stat().st_mtime)
    if key not in _CLEAN_CACHE:
        _CLEAN_CACHE[key] = clean_pages(extract_pages(path))
    return _CLEAN_CACHE[key]


def chunk_file(path: Path, entry: dict | None = None, design: str = "structure") -> tuple[list[Chunk], dict]:
    """Extract, clean and chunk one file. No API calls. Returns (chunks, stats)."""
    path = Path(path)
    entry = entry or manifest_entry_for(path) or {}
    source = entry.get("id") or re.sub(r"[^A-Za-z0-9._-]+", "-", path.stem).strip("-")
    title = entry.get("short_title") or path.stem
    page_range = tuple(entry["pages"]) if entry.get("pages") else None
    cleaned = cleaned_pages(path)
    stream = build_stream(cleaned, page_range, entry.get("skip_heading_pages", ()))
    ranges = chunk_structure(stream) if design == "structure" else chunk_fixed(stream)
    chunks = make_chunks(stream, ranges, source, title, design)
    sizes = [len(c.text.split()) for c in chunks] or [0]
    stats = {
        "source": source, "design": design, "pages_indexed": len({p for p in stream.pages}),
        "words": len(stream.words), "chunks": len(chunks), "headings": len(stream.headings),
        "words_per_chunk": {"min": min(sizes), "median": int(statistics.median(sizes)), "max": max(sizes)},
    }
    return chunks, stats


# --- chunk + vector stores -----------------------------------------------------------------
def chunks_path(design: str) -> Path:
    return INDEX_DIR / f"chunks_{design}.jsonl"


def read_chunks(design: str) -> list[dict]:
    p = chunks_path(design)
    if not p.is_file():
        return []
    return [json.loads(l) for l in p.read_text(encoding="utf-8").splitlines() if l.strip()]


def write_chunks(design: str, records: list[dict]) -> None:
    INDEX_DIR.mkdir(exist_ok=True)
    tmp = chunks_path(design).with_suffix(".tmp")
    tmp.write_text("\n".join(json.dumps(r, ensure_ascii=False) for r in records) + "\n", encoding="utf-8")
    tmp.replace(chunks_path(design))


def load_vectors() -> dict[str, list[float]]:
    vecs: dict[str, list[float]] = {}
    if VECTORS_FILE.is_file():
        with VECTORS_FILE.open(encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    r = json.loads(line)
                    vecs[r["k"]] = r["v"]
    return vecs


def append_vectors(items: dict[str, list[float]]) -> None:
    """Append and flush right away: a crash or the daily limit loses nothing already embedded."""
    INDEX_DIR.mkdir(exist_ok=True)
    with VECTORS_FILE.open("a", encoding="utf-8") as f:
        for k, v in items.items():
            f.write(json.dumps({"k": k, "v": [round(x, 5) for x in v]}) + "\n")
        f.flush()
        os.fsync(f.fileno())


# --- 5. embed ----------------------------------------------------------------------------
USAGE = {"embedded_texts": 0, "embed_calls": 0}
_client = None


def _get_client():
    global _client
    if _client is None:
        from google import genai
        from api_key import load_api_key

        _client = genai.Client(api_key=load_api_key())
    return _client


def embed_batch(texts: list[str]) -> list[list[float]]:
    """Embed texts with Gemini, one vector per text. Retries per-minute limits; stops on the daily one."""
    from google.genai import types

    # gemini-embedding-2 returns ONE aggregated vector for a plain list of strings.
    # Wrapping every text in its own Content gives one vector per text.
    contents = [types.Content(parts=[types.Part(text=t)]) for t in texts]
    config = types.EmbedContentConfig(output_dimensionality=EMBED_DIM)
    delay = 5.0
    for attempt in range(6):
        try:
            res = _get_client().models.embed_content(model=EMBED_MODEL, contents=contents, config=config)
        except Exception as error:  # noqa: BLE001
            message = str(error)
            code = getattr(error, "code", None)
            if code == 429 or "RESOURCE_EXHAUSTED" in message or "429" in message[:20]:
                if re.search(r"per\s*day|PerDay|daily", message, re.I):
                    raise QuotaExhausted(message[:300]) from error
                if attempt < 5:
                    print(f"  rate limit, waiting {delay:.0f}s ...", file=sys.stderr, flush=True)
                    time.sleep(delay)
                    delay = min(delay * 2, 60)
                    continue
                raise QuotaExhausted("rate limit kept failing: " + message[:300]) from error
            if attempt < 3 and (code in (500, 503) or "503" in message[:20]):
                time.sleep(delay)
                continue
            raise
        vectors = [list(e.values) for e in res.embeddings]
        if len(vectors) != len(texts):
            raise RuntimeError(f"asked for {len(texts)} embeddings, got {len(vectors)}")
        USAGE["embedded_texts"] += len(texts)
        USAGE["embed_calls"] += 1
        return vectors
    raise RuntimeError("unreachable")


def embed_query(text: str) -> list[float]:
    return embed_batch([f"task: search result | query: {text}"])[0]


def embed_and_store(chunks: list[Chunk], limit: int | None = None) -> dict:
    """Embed the chunks that have no saved vector yet and append them to index/vectors.jsonl.

    Returns {"cached": n, "embedded": n, "missing": n}. Raises QuotaExhausted (after saving what it got)."""
    vecs = load_vectors()
    todo, seen = [], set()
    for c in chunks:
        if c.vec_key not in vecs and c.vec_key not in seen:
            seen.add(c.vec_key)
            todo.append(c)
    cached = len({c.vec_key for c in chunks}) - len(todo)
    if limit is not None:
        todo = todo[:limit]
    done = 0
    try:
        for i in range(0, len(todo), EMBED_BATCH):
            batch = todo[i:i + EMBED_BATCH]
            vectors = embed_batch([c.embed_text for c in batch])
            append_vectors({c.vec_key: v for c, v in zip(batch, vectors)})
            done += len(batch)
            print(f"  embedded {done}/{len(todo)}", file=sys.stderr, flush=True)
            time.sleep(0.4)
    except QuotaExhausted:
        remaining = len({c.vec_key for c in chunks if c.vec_key not in load_vectors()})
        return {"cached": cached, "embedded": done, "missing": remaining, "quota_exhausted": True}
    remaining = len({c.vec_key for c in chunks if c.vec_key not in load_vectors()})
    return {"cached": cached, "embedded": done, "missing": remaining, "quota_exhausted": False}


# --- 6. whole-corpus build and single-file add -------------------------------------------------
def _record_with_vec_key(chunks: list[Chunk]) -> list[dict]:
    return [c.to_record() for c in chunks]


def build_all(dry_run: bool = False, designs: tuple[str, ...] = DESIGNS, show_headings: bool = False) -> int:
    """Chunk every document in the manifest and embed what is missing. Returns a process exit code."""
    manifest = load_manifest()
    if not manifest:
        print("corpus/manifest.json is missing or empty.", file=sys.stderr)
        return 1
    docs = load_documents()
    all_chunks: dict[str, list[Chunk]] = {d: [] for d in designs}
    keep_extra: dict[str, list[dict]] = {}
    manifest_ids = {e["id"] for e in manifest}
    for design in designs:  # documents added later with add_document stay in the index
        keep_extra[design] = [r for r in read_chunks(design) if r["source"] not in manifest_ids]
    total_words = 0
    print(f"{'document':16} {'design':10} {'pages':>5} {'words':>7} {'chunks':>6} {'words/chunk (min/med/max)':>26}")
    for entry in manifest:
        path = resolve_file(entry)
        if path is None:
            print(f"  missing file for {entry['id']}: put a PDF matching '{entry['file_glob']}' in corpus/", file=sys.stderr)
            return 1
        for design in designs:
            chunks, st = chunk_file(path, entry, design)
            all_chunks[design].extend(chunks)
            w = st["words_per_chunk"]
            print(f"{st['source']:16} {design:10} {st['pages_indexed']:>5} {st['words']:>7} {st['chunks']:>6} "
                  f"{w['min']:>10}/{w['median']}/{w['max']}")
            if design == designs[0]:
                total_words += st["words"]
                docs[entry["id"]] = {"sha256": file_sha256(path), "file": path.name, "words": st["words"],
                                     "pages": entry.get("pages"), "via": "manifest"}
                if show_headings:
                    s = build_stream(cleaned_pages(path), tuple(entry["pages"]) if entry.get("pages") else None, entry.get("skip_heading_pages", ()))
                    for pg, h in s.headings:
                        print(f"      p.{pg:<3} {h[:90]}")
    print(f"\nIndexed words: {total_words:,}  ({'≥' if total_words >= 50000 else '<'} 50,000 required)")
    if dry_run:
        vecs = load_vectors()
        for design in designs:
            need = len({c.vec_key for c in all_chunks[design] if c.vec_key not in vecs})
            print(f"  {design}: {len(all_chunks[design])} chunks, {need} still need an embedding")
        sample = all_chunks[designs[0]][len(all_chunks[designs[0]]) // 2]
        print(f"\nSample chunk {sample.id}  [{sample.source}, p. {sample.page_start}-{sample.page_end}, "
              f"paras {sample.paras or '-'}, section: {sample.section or '-'}]\n{sample.text[:700]}")
        return 0
    exit_code = 0
    for design in designs:
        write_chunks(design, keep_extra[design] + _record_with_vec_key(all_chunks[design]))
    save_documents(docs)
    for design in designs:
        print(f"\nEmbedding design '{design}' ...", file=sys.stderr)
        result = embed_and_store(all_chunks[design])
        print(f"{design}: {result['cached']} already saved, {result['embedded']} newly embedded, {result['missing']} missing")
        if result["quota_exhausted"]:
            print("\nThe free daily embedding quota is used up. Nothing is lost: every vector so far is saved.\n"
                  "Run `uv run python main.py index` again after 09:00 (Spain), when the quota resets.", file=sys.stderr)
            exit_code = 2
            break
    write_meta()
    return exit_code


def write_meta() -> None:
    vecs = load_vectors()
    meta = {"embed_model": EMBED_MODEL, "embed_dim": EMBED_DIM, "serving_design": SERVING_DESIGN,
            "updated": datetime.now(timezone.utc).isoformat(timespec="seconds"), "vectors": len(vecs),
            "chunks": {d: len(read_chunks(d)) for d in DESIGNS}}
    (INDEX_DIR / "meta.json").write_text(json.dumps(meta, indent=1), encoding="utf-8")


def index_file(path: str | Path, replace: bool = True, design: str = SERVING_DESIGN) -> dict:
    """The add-document pipeline: validate -> chunk -> embed -> store. Used by server.py.

    If the file (same bytes) is already indexed nothing is done and no API call is made.
    If a *different* file has the same source id it is treated as a new version and replaces
    the old chunks (unchanged chunks keep their saved vector, so they cost nothing)."""
    path = Path(path).expanduser().resolve()
    if not path.is_file():
        return {"status": "error", "message": f"File not found: {path}"}
    if path.suffix.lower() not in ALLOWED_SUFFIXES:
        return {"status": "error", "message": f"Unsupported file type {path.suffix}. Allowed: {sorted(ALLOWED_SUFFIXES)}"}
    digest = file_sha256(path)
    docs = load_documents()
    for src, info in docs.items():
        if info.get("sha256") == digest:
            return {"status": "already_indexed", "source": src, "message": f"{path.name} is already indexed as {src}; nothing changed, no embeddings used."}
    chunks, stats = chunk_file(path, None, design)
    if not chunks:
        return {"status": "error", "message": "No text could be extracted from this file."}
    existing = read_chunks(design)
    old_vecs = load_vectors()
    new_needed = len({c.vec_key for c in chunks if c.vec_key not in old_vecs})
    if new_needed > MAX_NEW_CHUNKS_PER_DOCUMENT:
        return {"status": "error", "message": f"{new_needed} new chunks to embed; the limit per document is "
                f"{MAX_NEW_CHUNKS_PER_DOCUMENT} (free-tier quota)."}
    replaced = [r for r in existing if r["source"] == stats["source"]]
    result = embed_and_store(chunks)
    if result["missing"]:
        return {"status": "error", "message": "Embedding quota exhausted; the document was NOT added. Try again later."}
    write_chunks(design, [r for r in existing if r["source"] != stats["source"]] + _record_with_vec_key(chunks))
    docs[stats["source"]] = {"sha256": digest, "file": path.name, "words": stats["words"], "pages": None,
                             "via": "add_document", "added": datetime.now(timezone.utc).isoformat(timespec="seconds")}
    save_documents(docs)
    write_meta()
    return {"status": "replaced_version" if replaced else "added", "source": stats["source"],
            "chunks": stats["chunks"], "words": stats["words"], "replaced_chunks": len(replaced),
            "new_embeddings": result["embedded"], "reused_vectors": result["cached"]}


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the index. Embeds only chunks without a saved vector.")
    parser.add_argument("--dry-run", action="store_true", help="chunk and count; no API calls, nothing written")
    parser.add_argument("--designs", nargs="+", choices=DESIGNS, default=list(DESIGNS))
    parser.add_argument("--show-headings", action="store_true", help="print the headings detected in each document")
    args = parser.parse_args()
    return build_all(dry_run=args.dry_run, designs=tuple(args.designs), show_headings=args.show_headings)


if __name__ == "__main__":
    sys.exit(main())
