"""Extract, clean and chunk text. Pure Python (no network, no embeddings) so it can be unit-tested.

Pipeline: file -> lines -> Sections (Article / Annex / heading / page) -> Chunks.
Every Chunk carries doc_id, location ("Article 33", "Annex III", "Article 3 (part 2/5)") and chapter.
"""
from __future__ import annotations

import hashlib
import re
from dataclasses import dataclass, field
from pathlib import Path

from config import CORPUS, FIXED_OVERLAP, FIXED_WORDS, MAX_WORDS

ART = re.compile(r"^Article\s+(\d+[a-z]?)$")
ANX = re.compile(r"^ANNEX(?:\s+([IVXLC]+))?$")
CHAP = re.compile(r"^(CHAPTER|SECTION|TITLE)\s+[IVXLC\d]+$")
MARK = re.compile(r"^(\(\w{1,5}\)|\d{1,3}\.|\w{1,3}\)|[—–-])$")   # lone list markers: "(a)", "1.", "—"
PARA_START = re.compile(r"^(\d{1,3}\.|\(\d{1,3}\))\s")             # numbered paragraph / definition


@dataclass
class Section:
    location: str          # "Article 5", "Annex III", "Page 4", "## Heading"
    title: str = ""
    chapter: str = ""
    lines: list[str] = field(default_factory=list)

    @property
    def text(self) -> str:
        return "\n".join(self.lines)


@dataclass
class Chunk:
    doc_id: str
    doc_title: str
    location: str                  # what is shown in the citation
    base_locs: list[str]           # article-level locations covered (used for hit-rate matching)
    chapter: str
    title: str
    text: str

    @property
    def citation(self) -> str:
        return f"[{self.doc_id}:{self.location}]"

    @property
    def text_hash(self) -> str:
        return hashlib.sha256(self.text.encode()).hexdigest()[:16]


# ---------------------------------------------------------------- extraction / cleaning
def clean(s: str) -> str:
    s = s.replace("\xa0", " ").replace("​", "")
    s = re.sub(r"\s+", " ", s).strip()
    s = re.sub(r"\s+([,.;:)])", r"\1", s)
    s = re.sub(r"\(\s+", "(", s)
    return s


def html_lines(html: str) -> list[str]:
    from bs4 import BeautifulSoup
    soup = BeautifulSoup(html, "lxml")
    for t in soup(["script", "style", "noscript", "nav", "header", "footer"]):
        t.decompose()
    blocks = ["p", "li", "td", "th", "div", "h1", "h2", "h3", "h4", "table"]
    leaves = [e for e in soup.find_all(blocks) if not e.find(blocks)]   # leaf blocks only: no duplicates
    lines = [clean(e.get_text(" ", strip=True)) for e in leaves]
    lines = [l for l in lines if l]
    if len(lines) < 5:                                                 # plain-ish HTML fallback
        lines = [clean(l) for l in soup.get_text("\n").splitlines() if clean(l)]
    return merge_markers(lines)


def merge_markers(lines: list[str]) -> list[str]:
    """EUR-Lex tables put '(a)' and its text in separate cells: glue them back together."""
    out, i = [], 0
    while i < len(lines):
        if MARK.match(lines[i]) and i + 1 < len(lines) and not ART.match(lines[i + 1]):
            out.append(f"{lines[i]} {lines[i + 1]}")
            i += 2
        else:
            out.append(lines[i])
            i += 1
    return out


def text_lines(text: str) -> list[str]:
    return merge_markers([clean(l) for l in text.splitlines() if clean(l)])


def is_title(line: str) -> bool:
    return len(line) < 250 and not PARA_START.match(line) and not line.startswith("(") and not line.endswith(".")


# ---------------------------------------------------------------- structure
def parse_structured(lines: list[str]) -> list[Section]:
    """Split a legal text into Article / Annex sections. Recitals and preamble are dropped
    (everything before the first Article heading). Duplicate headings (e.g. a table of contents)
    keep the longest version."""
    found: list[Section] = []
    cur: Section | None = None
    chapter = ""
    i = 0
    while i < len(lines):
        ln = lines[i]
        m, a = ART.match(ln), ANX.match(ln)
        if m or a:
            loc = f"Article {m.group(1)}" if m else ("Annex " + a.group(1) if a.group(1) else "Annex")
            title = ""
            if i + 1 < len(lines) and is_title(lines[i + 1]):
                title = lines[i + 1]
                i += 1
            cur = Section(loc, title, chapter)
            found.append(cur)
        elif CHAP.match(ln):
            chapter = ln
            if i + 1 < len(lines) and is_title(lines[i + 1]):
                chapter += " – " + lines[i + 1]
                i += 1
            cur = None
        elif ln.startswith("Done at"):
            cur = None
        elif cur is not None:
            cur.lines.append(ln)
        i += 1
    best: dict[str, Section] = {}
    for s in found:
        if s.location not in best or len(s.text) > len(best[s.location].text):
            best[s.location] = s
    return [s for s in best.values() if s.text.strip()]


def parse_headings(lines: list[str]) -> list[Section]:
    secs, cur = [], None
    for ln in lines:
        m = re.match(r"^#{1,4}\s+(.*)", ln)
        if m:
            cur = Section(m.group(1).strip())
            secs.append(cur)
        elif cur is not None:
            cur.lines.append(ln)
    return [s for s in secs if s.text.strip()]


def parse_windows(lines: list[str], label: str = "Section") -> list[Section]:
    """Last resort: ~MAX_WORDS-word sections."""
    secs, cur, n = [], [], 0
    for ln in lines:
        cur.append(ln)
        n += len(ln.split())
        if n >= MAX_WORDS:
            secs.append(Section(f"{label} {len(secs) + 1}", lines=cur))
            cur, n = [], 0
    if cur:
        secs.append(Section(f"{label} {len(secs) + 1}", lines=cur))
    return secs


def parse_file(path: str | Path) -> tuple[str, str, list[Section]]:
    """Return (doc_id, doc_title, sections) for html / txt / md / pdf."""
    p = Path(path)
    doc_id = re.sub(r"[^a-z0-9_]+", "_", p.stem.lower()).strip("_")
    title = CORPUS.get(doc_id, {}).get("title", p.stem)
    ext = p.suffix.lower()
    if ext == ".pdf":
        from pypdf import PdfReader
        secs = []
        for n, page in enumerate(PdfReader(str(p)).pages, 1):
            ls = text_lines(page.extract_text() or "")
            if ls:
                secs.append(Section(f"Page {n}", lines=ls))
        return doc_id, title, secs
    raw = p.read_text(encoding="utf-8", errors="replace")
    if ext in (".html", ".htm"):
        lines = html_lines(raw)
    elif ext in (".txt", ".md"):
        lines = text_lines(raw)
    else:
        raise ValueError(f"unsupported file type: {ext}")
    secs = parse_structured(lines)
    if len(secs) < 3:
        secs = parse_headings(lines) if ext == ".md" else []
    if len(secs) < 3:
        secs = parse_windows(lines)
    return doc_id, title, secs


# ---------------------------------------------------------------- chunking
def _blocks(lines: list[str]) -> list[list[str]]:
    blocks: list[list[str]] = []
    for ln in lines:
        if PARA_START.match(ln) or not blocks:
            blocks.append([ln])
        else:
            blocks[-1].append(ln)
    return blocks


def article_chunks(doc_id: str, doc_title: str, secs: list[Section], max_words: int = MAX_WORDS) -> list[Chunk]:
    """Structure-based: one chunk per Article/Annex; long ones split at paragraph boundaries.
    The embedded text starts with a header so a chunk is self-describing."""
    out: list[Chunk] = []
    for s in secs:
        groups, cur, n = [], [], 0
        for b in _blocks(s.lines):
            w = sum(len(x.split()) for x in b)
            if cur and n + w > max_words:
                groups.append(cur)
                cur, n = [], 0
            cur += b
            n += w
        if cur:
            groups.append(cur)
        for k, g in enumerate(groups, 1):
            loc = s.location if len(groups) == 1 else f"{s.location} (part {k}/{len(groups)})"
            header = f"{doc_title} — {s.location}" + (f": {s.title}" if s.title else "")
            out.append(Chunk(doc_id, doc_title, loc, [s.location], s.chapter, s.title, header + "\n" + "\n".join(g)))
    return out


def fixed_chunks(doc_id: str, doc_title: str, secs: list[Section],
                 size: int = FIXED_WORDS, overlap: int = FIXED_OVERLAP) -> list[Chunk]:
    """Baseline: structure-blind sliding window over the whole document. The citation is the span of
    articles the window touches, so it can still be checked against gold articles."""
    words, owner = [], []
    for s in secs:
        ws = s.text.split()
        words += ws
        owner += [s.location] * len(ws)
    out, step, start = [], max(1, size - overlap), 0
    while start < len(words):
        end = min(len(words), start + size)
        locs = list(dict.fromkeys(owner[start:end]))
        loc = locs[0] if len(locs) == 1 else f"{locs[0]} – {locs[-1]}"
        out.append(Chunk(doc_id, doc_title, loc, locs, "", "", " ".join(words[start:end])))
        if end == len(words):
            break
        start += step
    return out


def make_chunks(kind: str, doc_id: str, title: str, secs: list[Section]) -> list[Chunk]:
    return article_chunks(doc_id, title, secs) if kind == "article" else fixed_chunks(doc_id, title, secs)


def word_count(secs: list[Section]) -> int:
    return sum(len(s.text.split()) for s in secs)
