"""
Assignment 3: build the index (`main.py index`).

Corpus: the EU rules a drone operator has to check before a flight, as
consolidated texts from EUR-Lex (see CORPUS below). This file does everything
that happens before a question is asked:

    download -> extract -> chunk (two designs) -> embed (Gemini) -> save

and it exposes the per-file steps that server.py imports:

    chunk_file(path, design)        # extract + chunk one file
    embed_and_store(chunks, ...)    # embed only chunks without a saved vector
    Index(...).search(query)        # dense, BM25 or hybrid retrieval
    add_document(path)              # what the add_document tool runs

Vectors are saved the moment they are returned (index/vectors_*.jsonl), so a
crash or the free-tier daily limit never loses work, and re-running this file
embeds only what is missing.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import shutil
import sys
import time
import unicodedata
from collections import Counter
from dataclasses import asdict, dataclass, field
from pathlib import Path

import httpx
import numpy as np
from bs4 import BeautifulSoup, NavigableString, Tag
from bs4.element import PreformattedString   # comments, doctype, CDATA, processing instructions

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
# The index location can be redirected (evaluate.py uses a temporary copy so the
# add-document demo never touches the committed index).
INDEX_DIR = Path(os.environ.get("RAG_INDEX_DIR", ROOT / "index"))

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIMS = 768          # the model supports 128-3072; 768 is a recommended size
EMBED_BATCH = 20          # texts per request (each text counts towards the daily limit)
DAILY_SAFETY_LIMIT = 950  # stop a run after this many new embeddings (free tier ~1,000/day)

DESIGNS = ("fixed", "structure")
# What server.py serves. evaluate.py measures every design x mode and warns if these
# three no longer match its best numbers (see REPORT.md, "Retrieval").
DEFAULT_DESIGN = "structure"
DEFAULT_MODE = "dense"        # 'dense', 'bm25' or 'hybrid'
DEFAULT_K = 5                  # passages the search tool returns
FIXED_WORDS, FIXED_OVERLAP = 250, 50
FIXED_MIN_SHARE = 30           # words of a unit a fixed window must hold before it counts as "from" that unit
STRUCTURE_MAX_WORDS = 300

# Limits for add_document: a file the model names must not be able to burn the daily quota.
ADD_SUFFIXES = (".pdf", ".html", ".htm", ".xhtml", ".txt", ".md")
ADD_MAX_BYTES = 25_000_000
ADD_MAX_CHUNKS = 400


def log(*args) -> None:
    """Progress goes to stderr: the MCP server must keep stdout clean."""
    print(*args, file=sys.stderr, flush=True)


# --------------------------------------------------------------------------- #
# 1. The corpus
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Doc:
    id: str       # file stem and part of every chunk id
    short: str    # how citations name the document
    title: str
    topic: str    # a few words on what it covers; part of the text that is embedded
    celex: str    # EUR-Lex identifier of the consolidated version (a fixed date, so the text never changes)
    version: str


CORPUS = (
    Doc("reg-2019-947", "Reg. 2019/947",
        "Commission Implementing Regulation (EU) 2019/947 on the rules and procedures for the operation of unmanned aircraft",
        "rules for operating drones: open, specific and certified categories, remote pilots, registration",
        "02019R0947-20250501", "consolidated version of 2025-05-01"),
    Doc("reg-2019-945", "Reg. 2019/945",
        "Commission Delegated Regulation (EU) 2019/945 on unmanned aircraft systems and on third-country operators of unmanned aircraft systems",
        "product requirements for drones: classes C0 to C6, remote identification, CE marking, noise",
        "02019R0945-20250624", "consolidated version of 2025-06-24"),
    Doc("reg-2021-664", "Reg. 2021/664",
        "Commission Implementing Regulation (EU) 2021/664 on a regulatory framework for the U-space",
        "U-space airspace and the services drones use in it",
        "02021R0664-20260222", "consolidated version of 2026-02-22"),
    Doc("reg-376-2014", "Reg. 376/2014",
        "Regulation (EU) No 376/2014 on the reporting, analysis and follow-up of occurrences in civil aviation",
        "reporting of accidents and incidents in civil aviation",
        "02014R0376-20180911", "consolidated version of 2018-09-11"),
)
LICENCE = ("Texts (c) European Union, https://eur-lex.europa.eu/, reused under CC BY 4.0 "
           "(Commission Decision 2011/833/EU). Consolidated versions are for documentation only.")


def download_corpus() -> None:
    """Fetch each document once into corpus/ (git-ignored). Existing files are kept."""
    CORPUS_DIR.mkdir(exist_ok=True)
    headers = {
        "Accept": "application/xhtml+xml",
        "Accept-Language": "eng",
        "User-Agent": "daiist-assignment-3 (university course project; contact: student)",
    }
    for doc in CORPUS:
        path = CORPUS_DIR / f"{doc.id}.xhtml"
        if path.is_file() and path.stat().st_size > 10_000:
            continue
        url = f"https://publications.europa.eu/resource/celex/{doc.celex}"
        log(f"Downloading {doc.short} ({doc.celex}) ...")
        last_error = None
        for attempt in range(4):
            try:
                response = httpx.get(url, headers=headers, follow_redirects=True, timeout=120)
                response.raise_for_status()
                if b"eli-subdivision" not in response.content:
                    raise ValueError("response does not look like the legal text")
                path.write_bytes(response.content)
                break
            except Exception as error:  # noqa: BLE001 - retry any network or content problem
                last_error = error
                time.sleep(2 ** attempt)
        else:
            raise RuntimeError(f"Could not download {doc.short} from {url}: {last_error}")


# --------------------------------------------------------------------------- #
# 2. Extraction: HTML or PDF -> a flat list of blocks
# --------------------------------------------------------------------------- #

@dataclass
class Block:
    kind: str    # division | division_title | article | article_title | annex | annex_title | h | text | table
    text: str
    level: int = 0


# Paragraph classes that carry no legal content: amendment marks, tables of
# contents, headers, footnotes (they only hold Official Journal references).
SKIP_CLASSES = {
    "modref", "arrow", "toc-1", "toc-2", "hd-toc-1", "hd-toc-2", "hd-toc-3", "hd-modifiers",
    "title-fam-member-star", "title-doc-oj-reference", "reference", "disclaimer", "footnote",
}
HEADING_CLASSES = {
    "title-division-1": ("division", 0), "title-division-2": ("division_title", 0),
    "title-article-norm": ("article", 0), "stitle-article-norm": ("article_title", 0),
    "title-annex-1": ("annex", 0), "title-annex-2": ("annex_title", 0),
    "title-gr-seq-level-": ("h", 1),
    "title-gr-seq-level-1": ("h", 1), "title-gr-seq-level-2": ("h", 2),
    "title-gr-seq-level-3": ("h", 3), "title-gr-seq-level-4": ("h", 4),
}
AMENDMENT_MARK = re.compile(r"[▼►]\s*[A-Z]\d*|◄")


def clean_text(text: str) -> str:
    text = AMENDMENT_MARK.sub("", text)
    text = unicodedata.normalize("NFC", text.replace("\xa0", " "))
    text = re.sub(r"\s+", " ", text).strip()
    return re.sub(r"\(\s+", "(", re.sub(r"\s+([,;:.)])", r"\1", text))


def _flush(out: list[Block], buffer: list[str]) -> None:
    text = clean_text("".join(buffer))
    buffer.clear()
    if text:
        out.append(Block("text", text))


def _is_noise_anchor(tag: Tag) -> bool:
    """Amendment marks (▼M6, ►M2) and footnote call-outs (a link around a superscript number)."""
    if tag.name != "a":
        return False
    text = tag.get_text("", strip=True)
    return bool(AMENDMENT_MARK.fullmatch(text)) or tag.find("span", class_="superscript") is not None


def _walk(node: Tag, out: list[Block], buffer: list[str]) -> None:
    """Depth-first walk that turns the legal text's nested markup into blocks.

    The consolidated texts do NOT wrap every paragraph in <p>: many are bare text
    inside <div class="norm inline-element">. Walking all text nodes, instead of
    only reading <p> tags, is what keeps them (about 25% of Reg. 2019/945).
    """
    for child in node.children:
        if isinstance(child, PreformattedString):
            continue                      # <!DOCTYPE>, comments: not text
        if isinstance(child, NavigableString):
            buffer.append(str(child))
            continue
        if not isinstance(child, Tag):
            continue
        classes = set(child.get("class", []))
        if child.name in ("script", "style", "head", "title") or classes & SKIP_CLASSES:
            continue
        if _is_noise_anchor(child):
            continue
        if child.name == "table":
            _flush(out, buffer)
            _table(child, out)
            continue
        heading = next((HEADING_CLASSES[c] for c in classes if c in HEADING_CLASSES), None)
        if child.name == "p" and heading:
            _flush(out, buffer)
            text = clean_text(child.get_text(" "))
            if text:
                out.append(Block(heading[0], text, heading[1]))
            continue
        if "grid-container" in classes:
            _flush(out, buffer)
            _list_item(child, out)
            continue
        if child.name in ("span", "a", "em", "i", "b", "strong", "sup", "sub", "small", "u", "abbr") or "inline-element" in classes:
            _walk(child, out, buffer)     # inline: same paragraph
        elif child.name == "br":
            buffer.append(" ")
        else:
            _flush(out, buffer)           # block: its own paragraph(s)
            _walk(child, out, buffer)
            _flush(out, buffer)


def _list_item(div: Tag, out: list[Block]) -> None:
    """'(a)' in one column and the text in the other: put them back on one line."""
    label_node = div.find(class_="grid-list-column-1")
    body_node = div.find(class_="grid-list-column-2")
    label = clean_text(label_node.get_text(" ")) if label_node else ""
    inner: list[Block] = []
    if body_node is not None:
        buffer: list[str] = []
        _walk(body_node, inner, buffer)
        _flush(inner, buffer)
    if inner and inner[0].kind == "text":
        inner[0].text = f"{label} {inner[0].text}".strip()
    elif label:
        inner.insert(0, Block("text", label))
    out.extend(inner)


def _table(table: Tag, out: list[Block]) -> None:
    if table.find("p", class_="arrow"):
        # Layout table: the EUR-Lex converter puts the amendment mark in a side column.
        for cell in table.find_all("td"):
            if not cell.find("p", class_="arrow"):
                buffer: list[str] = []
                _walk(cell, out, buffer)
                _flush(out, buffer)
        return
    rows = []
    for tr in table.find_all("tr"):
        cells = [clean_text(td.get_text(" ")) for td in tr.find_all(["td", "th"])]
        cells = [c for c in cells if c]
        if cells:
            rows.append(" | ".join(cells))
    if rows:
        out.append(Block("table", "\n".join(rows)))


def extract_eurlex(raw: bytes) -> list[Block]:
    soup = BeautifulSoup(raw, "html.parser")
    out: list[Block] = []
    buffer: list[str] = []
    _walk(soup, out, buffer)
    _flush(out, buffer)
    return out


# Generic fallback for other documents (add_document): PDF or plain HTML/text.
# Headings are recognised by their wording (Spanish or English), case-sensitively and only
# when the whole line has the shape of a heading. A wrapped sentence that merely starts with
# "artículo 129 de la Ley ..." must not be taken for one (that bug fragmented the first try).
ARTICLE_LINE = re.compile(r"^(Art[ií]culo|Article)\s+(\d+[A-Za-zº]*)(?:\.\s*(.*))?$")
PROVISION_LINE = re.compile(r"^(Disposici[oó]n\s+(?:adicional|transitoria|derogatoria|final)\s+\w+)\.\s*(.*)$")
DIVISION_LINE = re.compile(r"^(?:CAP[IÍ]TULO|T[IÍ]TULO|CHAPTER|TITLE)\s+[IVXLC\d]+$|^Secci[oó]n\s+\d+\.?ª.*$")
ANNEX_LINE = re.compile(r"^(?:ANEXO|Anexo|ANNEX|Annex|APPENDIX|Appendix)(?:\s+[IVXLC\d]+)?\.?$")
LIST_START = re.compile(r"^(?:\d+\.|\([a-z0-9]+\)|[a-z]\))\s")
# Page furniture of a BOE PDF: the footer is four lines ("BOLETÍN OFICIAL DEL ESTADO",
# "Núm. 136 Miércoles 5 de junio de 2024 Sec. I.   Pág. 65363", "cve: BOE-A-...",
# "Verificable en https://www.boe.es"); the first page also has a banner line.
PAGE_NOISE = re.compile(
    r"^(?:BOLET[ÍI]N OFICIAL DEL ESTADO"
    r"|N[úu]m\.\s*\d+\s.*P[áa]g\.\s*\d+"
    r"|Sec\.\s*[IVX]+\.?\s*P[áa]g\.\s*\d+"
    r"|cve:\s*BOE-.*|Verificable en .*"
    r"|https?://www\.boe\.es.*|D\. ?L\.: .*"
    r"|(?:lunes|martes|mi[ée]rcoles|jueves|viernes|s[áa]bado|domingo)\s+\d+\s+de\s+\w+\s+de\s+\d{4}"
    r"|\d{1,4})$",
    re.IGNORECASE,
)


def extract_pdf(path: Path) -> list[Block]:
    from pypdf import PdfReader

    lines: list[str] = []
    for page in PdfReader(str(path)).pages:
        lines.extend((page.extract_text() or "").splitlines())
    return _blocks_from_lines(lines)


def _blocks_from_lines(lines: list[str]) -> list[Block]:
    """Join wrapped lines into paragraphs and mark headings; drop page headers and footers.
    Produces the same block kinds as the EUR-Lex extractor, so build_units works on both."""
    blocks: list[Block] = []
    current: list[str] = []
    expecting: str | None = None   # the next short line is the title of the heading just seen
    title_open = False             # an article title that wraps onto the next line
    division_open = False          # a chapter or section heading whose title may wrap (the rest starts in lower case)

    def end_paragraph() -> None:
        text = clean_text(" ".join(current))
        current.clear()
        text = re.sub(r"(\w)- (\w)", r"\1\2", text)  # re-join words hyphenated at line ends
        if text:
            blocks.append(Block("text", text))

    for raw_line in lines:
        line = raw_line.strip()
        if not line or PAGE_NOISE.match(line):
            continue
        is_heading = bool(ARTICLE_LINE.match(line) or PROVISION_LINE.match(line)
                          or DIVISION_LINE.match(line) or ANNEX_LINE.match(line))
        if title_open and not is_heading and not LIST_START.match(line) and len(line.split()) <= 12:
            blocks[-1].text = clean_text(f"{blocks[-1].text} {line}").rstrip(".")
            title_open = not line.endswith(".")
            continue
        title_open = False
        if division_open and not is_heading and line[:1].islower() and len(line.split()) <= 15:
            blocks[-1].text = clean_text(f"{blocks[-1].text} {line}")
            continue
        division_open = False
        if expecting and not is_heading and len(line.split()) <= 15:
            blocks.append(Block(expecting, clean_text(line).rstrip(".")))
            division_open = expecting == "division_title"
            expecting = None
            continue
        expecting = None
        if match := ARTICLE_LINE.match(line):
            end_paragraph()
            blocks.append(Block("article", f"{match.group(1)} {match.group(2)}"))
            title = (match.group(3) or "").strip()
            if title:
                blocks.append(Block("article_title", title.rstrip(".")))
                title_open = not title.endswith(".")
            else:
                expecting = "article_title"
        elif match := PROVISION_LINE.match(line):
            end_paragraph()
            blocks.append(Block("article", match.group(1)))
            if match.group(2).strip():
                blocks.append(Block("article_title", match.group(2).strip().rstrip(".")))
        elif DIVISION_LINE.match(line):
            end_paragraph()
            blocks.append(Block("division", clean_text(line)))
            has_title = line.startswith(("Sección", "Seccion"))   # 'Sección 2.ª Title' carries its title
            expecting = None if has_title else "division_title"
            division_open = has_title
        elif ANNEX_LINE.match(line):
            end_paragraph()
            blocks.append(Block("annex", clean_text(line)))
            expecting = "annex_title"
        elif current and LIST_START.match(line):
            end_paragraph()
            current.append(line)
        else:
            current.append(line)
    end_paragraph()
    return blocks


def extract_file(path: Path) -> list[Block]:
    suffix = path.suffix.lower()
    if suffix in (".html", ".htm", ".xhtml"):
        raw = path.read_bytes()
        if b"eli-subdivision" in raw or b"title-article-norm" in raw:
            return extract_eurlex(raw)
        soup = BeautifulSoup(raw, "html.parser")
        for tag in soup(["script", "style", "head"]):
            tag.decompose()
        return _blocks_from_lines(soup.get_text("\n").splitlines())
    if suffix == ".pdf":
        return extract_pdf(path)
    if suffix in (".txt", ".md"):
        return _blocks_from_lines(path.read_text(encoding="utf-8", errors="replace").splitlines())
    raise ValueError(f"Unsupported file type {suffix!r}; use .html, .xhtml, .pdf, .txt or .md")


# --------------------------------------------------------------------------- #
# 3. Structure: blocks -> units (an article, an annex section ...)
# --------------------------------------------------------------------------- #

@dataclass
class Unit:
    keys: list[str]      # most specific first, e.g. ["UAS.OPEN.030", "Annex, Part A", "Annex"]
    display: str         # human-readable location
    texts: list[str] = field(default_factory=list)

    @property
    def key(self) -> str:
        return self.keys[0]

    @property
    def words(self) -> int:
        return sum(len(t.split()) for t in self.texts)


SECTION_CODE = re.compile(r"^([A-Z]{2,}(?:\.[A-Z0-9-]+)+\.\d+)")        # UAS.OPEN.030, UAS.STS-01.020
STRUCTURE_WORD = re.compile(r"^(PART|CHAPTER|SECTION|TITLE|ANNEX|APPENDIX|ATTACHMENT|MODULE)\b\s*([A-Z0-9]{1,4}\b)?", re.I)
NUMBERED_HEADING = re.compile(r"^(\d+(?:\.\d+)*\.?|[A-Z]\.|\([0-9a-z]+\))\s")


def is_code(label: str) -> bool:
    return bool(SECTION_CODE.match(label))


def short_label(text: str) -> str:
    """The short name of a heading, used in citations:
    'PART 3 - Requirements for a class C2 ...' -> 'Part 3'; 'UAS.OPEN.030 ...' -> 'UAS.OPEN.030';
    'CHAPTER I - STS-01 - VLOS over ...' -> 'STS-01'; 'ANNEX III' -> 'Annex III'."""
    text = text.strip()
    if match := SECTION_CODE.match(text):
        return match.group(1)
    if match := re.search(r"\b(STS-\d+)\b", text):
        return match.group(1).upper()
    if match := STRUCTURE_WORD.match(text):
        word, number = match.group(1).capitalize(), match.group(2)
        return f"{word} {number}" if number else word
    if match := NUMBERED_HEADING.match(text):
        return match.group(1).rstrip(".")
    return " ".join(text.split()[:3])


def build_units(blocks: list[Block]) -> list[Unit]:
    """Group blocks into units. Headings with no text of their own (e.g. 'PART A')
    become the path of the next unit instead of empty units of their own."""
    units: list[Unit] = []
    chapter = ""
    article = article_title = ""
    annex = annex_title = appendix = appendix_title = ""
    levels = [""] * 5          # levels[1..4] = gr-seq headings
    current: Unit | None = None
    last_heading_level: tuple[str, int] | None = None

    def start_unit() -> Unit:
        nonlocal current
        if article:
            keys = [article]                            # 'Article 4' (English) or 'Artículo 5' (Spanish)
            display = f"{article} - {article_title}" if article_title else article
        elif not (annex or appendix or any(levels)):
            keys, display = ["Title"], "Title"          # text before the first article: the act's title
        else:
            chain_names = [n for n in (annex, appendix) if n] + [lv for lv in levels[1:] if lv]
            shorts = [short_label(n) for n in chain_names]
            if shorts and not is_code(shorts[-1]):
                # An 'Attachment' that follows a numbered section belongs to the chapter, not to that section.
                shorts = [s for s in shorts if not is_code(s)]
            if appendix and len(shorts) > 1 and shorts[0] == "Annex":
                shorts = shorts[1:]                      # appendices belong to the one Annex: 'Appendix 2'
            deepest = shorts[-1] if shorts else "Annex"
            full = ", ".join(dict.fromkeys(shorts))
            keys = [deepest if is_code(deepest) else full]
            for end in range(len(shorts) - 1, 0, -1):    # shorter paths are aliases: 'Part A', 'Annex'
                alias = ", ".join(dict.fromkeys(shorts[:end]))
                if alias not in keys:
                    keys.append(alias)
            if full not in keys:
                keys.insert(1, full)
            display = " > ".join(dict.fromkeys(chain_names)) or "Annex"
            if appendix_title:
                display += f" ({appendix_title})"
        current = Unit(keys=keys, display=display)
        units.append(current)
        return current

    for block in blocks:
        kind = block.kind
        if kind in ("division", "division_title"):
            chapter = block.text if kind == "division" else f"{chapter} - {block.text}"
            continue
        if kind == "article":
            article, article_title, annex, appendix, levels = block.text, "", "", "", [""] * 5
            current, last_heading_level = None, None
            continue
        if kind == "article_title":
            article_title = block.text
            continue
        if kind == "annex":
            if block.text.lower().startswith("appendix"):
                appendix, appendix_title, levels = block.text, "", [""] * 5
            else:
                annex, annex_title, appendix, appendix_title, levels = block.text, "", "", "", [""] * 5
            article, article_title, current, last_heading_level = "", "", None, None
            continue
        if kind == "annex_title":
            if appendix and not appendix_title:
                appendix_title = block.text
            elif annex and not annex_title:
                annex_title = block.text
            continue
        if kind == "h":
            level = block.level
            if last_heading_level == ("h", level) and levels[level]:
                levels[level] = f"{levels[level]} - {block.text}"   # 'PART A' + its title line
            else:
                levels[level] = block.text
                for deeper in range(level + 1, 5):
                    levels[deeper] = ""
            current, last_heading_level = None, ("h", level)
            continue
        # text or table
        last_heading_level = None
        unit = current or start_unit()
        if unit.keys == ["Title"] and block.text in unit.texts:
            continue                                      # the converter prints the title twice
        unit.texts.append(block.text)
    units = [u for u in units if u.texts]
    if units and units[0].keys == ["Title"] and units[0].words > 150:
        units[0].keys, units[0].display = ["Preamble"], "Preamble"   # a long text before Article 1
    seen: Counter = Counter()
    for unit in units:                                    # keys must be unique within a document
        seen[unit.keys[0]] += 1
        if seen[unit.keys[0]] > 1:
            unit.keys[0] = f"{unit.keys[0]} ({seen[unit.keys[0]]})"
    return units


# --------------------------------------------------------------------------- #
# 4. Chunking: units -> chunks (two designs)
# --------------------------------------------------------------------------- #

@dataclass
class Chunk:
    id: str
    design: str
    source: str            # document name, e.g. "Reg. 2019/947"
    location: str           # human-readable location of the chunk
    cite: str               # the citation label the agent must copy: "Reg. 2019/947, Article 4"
    loc_keys: list[str]     # every location key the chunk touches (used to score retrieval)
    text: str
    words: int
    topic: str = ""         # what the document covers, in a few words

    @property
    def embed_text(self) -> str:
        """What is embedded (and searched by BM25): a title line plus the text.
        gemini-embedding-2 has no task_type; the model expects this document format."""
        name = f"{self.source} ({self.topic})" if self.topic else self.source
        return f"title: {name} - {self.location} | text: {self.text}"


def make_id(design: str, source: str, cite: str, text: str, topic: str = "") -> str:
    """A content hash: the same text in the same place always gets the same id, so a saved vector is reused."""
    return hashlib.sha1(f"{design}|{source}|{topic}|{cite}|{text}".encode("utf-8")).hexdigest()[:16]


def _split_balanced(texts: list[str], max_words: int) -> list[list[str]]:
    """Split paragraphs into the fewest parts of about equal size, each <= max_words
    (a single paragraph longer than max_words is cut at sentence boundaries)."""
    pieces: list[str] = []
    for text in texts:
        if len(text.split()) <= max_words:
            pieces.append(text)
        else:
            sentences = re.split(r"(?<=[.;:])\s+|\n", text)
            buf: list[str] = []
            for sentence in sentences:
                if buf and sum(len(s.split()) for s in buf) + len(sentence.split()) > max_words:
                    pieces.append(" ".join(buf))
                    buf = []
                buf.append(sentence)
            if buf:
                pieces.append(" ".join(buf))
    total = sum(len(p.split()) for p in pieces)
    n_parts = max(1, math.ceil(total / max_words))
    target = total / n_parts
    parts: list[list[str]] = [[]]
    size = 0
    for piece in pieces:
        w = len(piece.split())
        if parts[-1] and size + w > max_words or (parts[-1] and size >= target and len(parts) < n_parts):
            parts.append([])
            size = 0
        parts[-1].append(piece)
        size += w
    return parts


def chunk_structure(units: list[Unit], source: str, topic: str = "") -> list[Chunk]:
    """Design 'structure': one chunk per article / annex section, split only when
    longer than STRUCTURE_MAX_WORDS (at paragraph boundaries)."""
    chunks = []
    for unit in units:
        parts = _split_balanced(unit.texts, STRUCTURE_MAX_WORDS)
        for i, part in enumerate(parts, 1):
            suffix = f", part {i}/{len(parts)}" if len(parts) > 1 else ""
            text = "\n".join(part)
            cite = f"{source}, {unit.key}{suffix}"
            location = unit.display + (f" (part {i}/{len(parts)})" if len(parts) > 1 else "")
            chunks.append(Chunk(make_id("structure", source, cite, text, topic), "structure", source, location, cite,
                                list(unit.keys), text, len(text.split()), topic))
    return chunks


def chunk_fixed(units: list[Unit], source: str, topic: str = "",
                size: int = FIXED_WORDS, overlap: int = FIXED_OVERLAP) -> list[Chunk]:
    """Design 'fixed': windows of `size` words with `overlap`, blind to structure.
    Each word remembers its unit so the chunk can still say where it is from. A window is attributed to a unit
    only if it holds FIXED_MIN_SHARE words of it (or all of a shorter unit): three words of the next article
    at the window's edge do not make the chunk "about" that article, and must not count as a retrieval hit."""
    words: list[str] = []
    owner: list[int] = []
    for index, unit in enumerate(units):
        for text in unit.texts:
            for word in text.split():
                words.append(word)
                owner.append(index)
    chunks = []
    step = size - overlap
    for start in range(0, max(1, len(words)), step):
        window = words[start:start + size]
        if not window or (start > 0 and len(window) <= overlap):
            break
        share = Counter(owner[start:start + len(window)])
        touched = list(dict.fromkeys(owner[start:start + len(window)]))
        touched = [i for i in touched if share[i] >= min(FIXED_MIN_SHARE, units[i].words)] or touched
        first, last = units[touched[0]], units[touched[-1]]
        loc_keys = list(dict.fromkeys(k for t in touched for k in units[t].keys))
        location = first.display if first is last else f"{first.display} ... {last.display}"
        label = first.key if first is last else f"{first.key} ... {last.key}"
        text = " ".join(window)
        cite = f"{source}, {label}, words {start + 1}-{start + len(window)}"
        chunks.append(Chunk(make_id("fixed", source, cite, text, topic), "fixed", source, location, cite,
                            loc_keys, text, len(window), topic))
    return chunks


def chunk_file(path: Path, design: str = DEFAULT_DESIGN, source: str | None = None, topic: str = "") -> list[Chunk]:
    """Extract one file and cut it into chunks. server.py's add_document calls this."""
    if source is None:
        known = {doc.id: doc for doc in CORPUS}.get(path.stem)
        source, topic = (known.short, known.topic) if known else (path.stem, topic)
    units = build_units(extract_file(path))
    return chunk_structure(units, source, topic) if design == "structure" else chunk_fixed(units, source, topic)


def corpus_chunks(design: str) -> list[Chunk]:
    chunks: list[Chunk] = []
    for doc in CORPUS:
        chunks.extend(chunk_file(CORPUS_DIR / f"{doc.id}.xhtml", design, doc.short, doc.topic))
    return chunks


# --------------------------------------------------------------------------- #
# 5. Embeddings (Gemini) and the saved vectors
# --------------------------------------------------------------------------- #

class DailyQuotaExceeded(RuntimeError):
    pass


_client = None


def _gemini():
    global _client
    if _client is None:
        from google import genai
        from api_key import load_api_key

        _client = genai.Client(api_key=load_api_key())
    return _client


def _normalise(vectors: list[list[float]]) -> list[list[float]]:
    out = []
    for vec in vectors:
        arr = np.asarray(vec, dtype=np.float64)
        norm = np.linalg.norm(arr) or 1.0
        out.append([round(float(x), 6) for x in arr / norm])
    return out


def embed_batch(texts: list[str]) -> list[list[float]]:
    """Embed texts with gemini-embedding-2, one vector per text.

    Two things the documentation is explicit about for this model:
    * several strings in one `contents` list give ONE aggregated embedding, so each
      text is wrapped in its own Content to get one vector per text;
    * there is no task_type: the task is part of the text (see Chunk.embed_text and
      embed_query).
    """
    from google.genai import errors, types

    contents = [types.Content(parts=[types.Part.from_text(text=t)]) for t in texts]
    config = types.EmbedContentConfig(output_dimensionality=EMBED_DIMS)
    for attempt in range(6):
        try:
            response = _gemini().models.embed_content(model=EMBED_MODEL, contents=contents, config=config)
            vectors = [list(e.values) for e in response.embeddings]
            if len(vectors) != len(texts) or any(len(v) != EMBED_DIMS for v in vectors):
                raise RuntimeError(f"Expected {len(texts)} vectors of {EMBED_DIMS} numbers, got "
                                   f"{len(vectors)} (sizes {sorted({len(v) for v in vectors})}).")
            return _normalise(vectors)
        except errors.APIError as error:
            message = f"{error}"
            if getattr(error, "code", None) == 429 and re.search(r"per ?day|PerDay|daily", message, re.I):
                raise DailyQuotaExceeded(message) from error
            if getattr(error, "code", None) in (429, 500, 503) and attempt < 5:
                wait = min(60, 4 * 2 ** attempt)
                log(f"  API busy ({getattr(error, 'code', '?')}); retrying in {wait}s ...")
                time.sleep(wait)
                continue
            raise
    raise RuntimeError("unreachable")


QUERY_PREFIX = "task: search result | query: "


def _query_key(query: str) -> str:
    return hashlib.sha1(f"{EMBED_MODEL}|{EMBED_DIMS}|{query}".encode()).hexdigest()


def embed_queries(queries: list[str]) -> list[list[float]]:
    """Embed questions with the 'search result' task prefix (documents use 'title: ... | text: ...').

    Every vector is cached in INDEX_DIR/query_vectors.jsonl, so a question is never embedded twice
    (the free tier counts every text). Only the questions missing from the cache are sent, in batches.
    """
    cache_path = INDEX_DIR / "query_vectors.jsonl"
    cache: dict[str, list[float]] = {}
    if cache_path.is_file():
        for line in cache_path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                record = json.loads(line)
                cache[record["k"]] = record["v"]
    missing = list(dict.fromkeys(q for q in queries if _query_key(q) not in cache))
    if missing:
        INDEX_DIR.mkdir(parents=True, exist_ok=True)
        for start in range(0, len(missing), EMBED_BATCH):
            batch = missing[start:start + EMBED_BATCH]
            vectors = embed_batch([QUERY_PREFIX + q for q in batch])
            with cache_path.open("a", encoding="utf-8", newline="\n") as f:
                for query, vector in zip(batch, vectors):
                    cache[_query_key(query)] = vector
                    f.write(json.dumps({"k": _query_key(query), "q": query, "v": vector}, ensure_ascii=False) + "\n")
    return [cache[_query_key(q)] for q in queries]


def embed_query(query: str) -> list[float]:
    return embed_queries([query])[0]


def _vectors_path(design: str, base: Path | None = None) -> Path:
    return (base or INDEX_DIR) / f"vectors_{design}.jsonl"


def _chunks_path(design: str, base: Path | None = None) -> Path:
    return (base or INDEX_DIR) / f"chunks_{design}.jsonl"


def saved_vectors(path: Path) -> dict[str, list[float]]:
    vectors: dict[str, list[float]] = {}
    if path.is_file():
        for line in path.read_text(encoding="utf-8").splitlines():
            if line.strip():
                record = json.loads(line)
                vectors[record["id"]] = record["v"]
    return vectors


def embed_and_store(chunks: list[Chunk], vectors_path: Path, budget: int | None = None) -> tuple[int, int]:
    """Embed only the chunks that have no saved vector, saving after every batch.
    Returns (embedded now, still missing)."""
    have = saved_vectors(vectors_path)
    missing = [c for c in chunks if c.id not in have]
    todo = missing if budget is None else missing[:budget]
    vectors_path.parent.mkdir(parents=True, exist_ok=True)
    done = 0
    try:
        for start in range(0, len(todo), EMBED_BATCH):
            batch = todo[start:start + EMBED_BATCH]
            vectors = embed_batch([c.embed_text for c in batch])
            with vectors_path.open("a", encoding="utf-8", newline="\n") as f:
                for chunk, vector in zip(batch, vectors):
                    f.write(json.dumps({"id": chunk.id, "v": vector}) + "\n")
            done += len(batch)
            log(f"  embedded {done}/{len(todo)}")
    except DailyQuotaExceeded as error:
        log(f"\nDaily free-tier embedding limit reached after {done} new chunks.\n"
            f"Everything embedded so far is saved. Run this again after 09:00 (Spain) when the quota resets.\n{error}")
    return done, len(missing) - done


def write_chunks(chunks: list[Chunk], path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", encoding="utf-8", newline="\n") as f:
        for chunk in chunks:
            f.write(json.dumps(asdict(chunk), ensure_ascii=False) + "\n")


def read_chunks(path: Path) -> list[Chunk]:
    chunks = []
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            chunks.append(Chunk(**json.loads(line)))
    return chunks


# --------------------------------------------------------------------------- #
# 6. Retrieval: dense, BM25 and hybrid (reciprocal rank fusion)
# --------------------------------------------------------------------------- #

TOKEN = re.compile(r"[a-z0-9]+(?:[._/-][a-z0-9]+)*")


def tokenize(text: str) -> list[str]:
    """Lower-case tokens. Codes like 'uas.open.030' and '2019/947' stay whole AND
    are also split ('uas', 'open', '030'), because users type either form."""
    tokens: list[str] = []
    for tok in TOKEN.findall(text.lower()):
        tokens.append(tok)
        if re.search(r"[._/-]", tok):
            tokens.extend(t for t in re.split(r"[._/-]", tok) if t)
    return tokens


class BM25:
    def __init__(self, documents: list[list[str]], k1: float = 1.5, b: float = 0.75):
        self.k1, self.b = k1, b
        self.tf = [Counter(d) for d in documents]
        self.lengths = np.array([len(d) for d in documents], dtype=float)
        self.avg = float(self.lengths.mean()) if len(documents) else 1.0
        df: Counter = Counter()
        for counts in self.tf:
            df.update(counts.keys())
        n = len(documents)
        self.idf = {t: math.log(1 + (n - c + 0.5) / (c + 0.5)) for t, c in df.items()}

    def scores(self, query_tokens: list[str]) -> np.ndarray:
        out = np.zeros(len(self.tf))
        for token in set(query_tokens):
            idf = self.idf.get(token)
            if idf is None:
                continue
            for i, counts in enumerate(self.tf):
                f = counts.get(token, 0)
                if f:
                    out[i] += idf * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * self.lengths[i] / self.avg))
        return out


@dataclass
class Hit:
    chunk: Chunk
    score: float
    rank: int


class Index:
    """The saved chunks and vectors of one design, loaded into memory.

    Exact cosine search over a few hundred vectors takes microseconds, so no
    vector database is needed; the files in index/ are the whole store.
    """

    def __init__(self, design: str = DEFAULT_DESIGN, index_dir: Path | None = None, include_added: bool = True):
        base = index_dir or INDEX_DIR
        self.design = design
        chunk_files = [(_chunks_path(design, base), _vectors_path(design, base))]
        added = base / "added"
        if include_added and design == DEFAULT_DESIGN and added.is_dir():
            chunk_files += [(p, p.with_name(p.name.replace(".chunks.", ".vectors."))) for p in sorted(added.glob("*.chunks.jsonl"))]
        chunks: list[Chunk] = []
        matrix: list[list[float]] = []
        for chunks_path, vectors_path in chunk_files:
            if not chunks_path.is_file():
                raise FileNotFoundError(f"{chunks_path} is missing. Run `uv run python main.py index` first.")
            vectors = saved_vectors(vectors_path)
            for chunk in read_chunks(chunks_path):
                if chunk.id in vectors:
                    chunks.append(chunk)
                    matrix.append(vectors[chunk.id])
        if not chunks:
            raise RuntimeError("The index holds no embedded chunks. Run `uv run python main.py index`.")
        self.chunks = chunks
        self.matrix = np.asarray(matrix, dtype=np.float32)
        self.bm25 = BM25([tokenize(c.embed_text) for c in chunks])

    def search(self, query: str, k: int = 5, mode: str = "hybrid", query_vector: list[float] | None = None,
               sources: list[str] | None = None) -> list[Hit]:
        """mode: 'dense' (embeddings), 'bm25' (keywords) or 'hybrid' (both, fused).
        `sources` optionally restricts the search to some documents (metadata filter)."""
        allowed = np.ones(len(self.chunks), dtype=bool)
        if sources:
            allowed = np.array([c.source in sources for c in self.chunks])
        rankings: list[list[int]] = []
        if mode in ("dense", "hybrid"):
            vector = np.asarray(query_vector if query_vector is not None else embed_query(query), dtype=np.float32)
            sims = np.where(allowed, self.matrix @ vector, -np.inf)
            rankings.append([int(i) for i in np.argsort(-sims) if np.isfinite(sims[i])])
        if mode in ("bm25", "hybrid"):
            scores = np.where(allowed, self.bm25.scores(tokenize(query)), -np.inf)
            rankings.append([int(i) for i in np.argsort(-scores) if scores[i] > 0])
        fused: dict[int, float] = {}
        for ranking in rankings:
            for position, i in enumerate(ranking[:50]):
                fused[i] = fused.get(i, 0.0) + 1.0 / (60 + position + 1)
        order = sorted(fused, key=lambda i: -fused[i])[:k]
        return [Hit(self.chunks[i], fused[i], rank) for rank, i in enumerate(order, 1)]


def format_hits(query: str, hits: list[Hit]) -> str:
    """What the search tool returns: each chunk with its citation label."""
    if not hits:
        return f'No passages found for "{query}".'
    parts = [f'{len(hits)} passages for "{query}". Cite a passage with the label shown in square brackets.\n']
    for hit in hits:
        c = hit.chunk
        parts.append(f"[{c.cite}]\nLocation: {c.location}\n{c.text}\n")
    return "\n".join(parts)


# --------------------------------------------------------------------------- #
# 7. Adding a document (the add_document tool)
# --------------------------------------------------------------------------- #

def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def add_document(path: str | Path) -> str:
    """Index one more file and make it searchable.

    * same file already indexed (identical bytes) -> nothing is done;
    * same name, different bytes -> the old version is replaced (unchanged
      chunks keep their vectors, because chunk ids are content hashes);
    * a name used by the base corpus is refused, so the corpus cannot be overwritten.
    Only the default design is updated: that is what the server searches.
    Returns a one-line message; it never raises, so the model can read what went wrong.
    """
    path = Path(path).expanduser()
    if not path.is_file() and not path.is_absolute() and (ROOT / path).is_file():
        path = ROOT / path
    if not path.is_file():
        return f"Error: {path} is not a file."
    if path.suffix.lower() not in ADD_SUFFIXES:
        return f"Error: {path.name} has an unsupported type; use one of {', '.join(ADD_SUFFIXES)}."
    if path.stat().st_size > ADD_MAX_BYTES:
        return f"Error: {path.name} is larger than {ADD_MAX_BYTES // 1_000_000} MB."
    try:
        source = path.stem
        if source in {d.id for d in CORPUS} or source in {d.short for d in CORPUS}:
            return f"Error: '{source}' is the name of a base corpus document; rename the file to add it."
        added = INDEX_DIR / "added"
        added.mkdir(parents=True, exist_ok=True)
        registry_path = added / "registry.json"
        registry = json.loads(registry_path.read_text(encoding="utf-8")) if registry_path.is_file() else {}
        sha = file_sha256(path)
        if registry.get(source, {}).get("sha256") == sha:
            return f"'{source}' is already indexed ({registry[source]['chunks']} chunks); nothing to do."
        chunks = chunk_file(path, DEFAULT_DESIGN, source)
        if not chunks:
            return f"Error: no text could be extracted from {path.name}."
        if len(chunks) > ADD_MAX_CHUNKS:
            return (f"Error: {path.name} would need {len(chunks)} chunks (limit {ADD_MAX_CHUNKS}, "
                    f"to protect the daily embedding quota). Split the file and add the parts.")
        replaced = source in registry
        slug = re.sub(r"[^A-Za-z0-9._-]+", "_", source)
        chunks_path = added / f"{slug}.chunks.jsonl"
        vectors_path = added / f"{slug}.vectors.jsonl"
        write_chunks(chunks, chunks_path)
        embedded, missing = embed_and_store(chunks, vectors_path)
        if missing:
            return (f"Partly indexed: {embedded} chunks embedded, {missing} still missing because of the API limit. "
                    f"Call add_document again later.")
        registry[source] = {"sha256": sha, "chunks": len(chunks), "file": path.name}
        registry_path.write_text(json.dumps(registry, indent=2), encoding="utf-8")
        verb = "Replaced the earlier version of" if replaced else "Indexed"
        return (f"{verb} '{source}': {len(chunks)} chunks ({embedded} newly embedded, "
                f"{len(chunks) - embedded} reused). It is searchable now.")
    except Exception as error:  # noqa: BLE001 - report to the model instead of crashing the server
        return f"Error while indexing {path.name}: {type(error).__name__}: {error}"


# --------------------------------------------------------------------------- #
# 8. The index stage
# --------------------------------------------------------------------------- #

def corpus_stats() -> list[dict]:
    rows = []
    for doc in CORPUS:
        units = build_units(extract_file(CORPUS_DIR / f"{doc.id}.xhtml"))
        rows.append({"id": doc.id, "source": doc.short, "title": doc.title, "version": doc.version,
                     "celex": doc.celex, "units": len(units), "words": sum(u.words for u in units)})
    return rows


def build_index(designs: tuple[str, ...] = DESIGNS) -> None:
    download_corpus()
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    stats = corpus_stats()
    total_words = sum(r["words"] for r in stats)
    log(f"Corpus: {len(stats)} documents, {total_words:,} words")
    for row in stats:
        log(f"  {row['source']:<16} {row['words']:>7,} words  {row['units']:>3} units  ({row['version']})")
    manifest = {"model": EMBED_MODEL, "dims": EMBED_DIMS, "licence": LICENCE, "documents": stats,
                "words": total_words, "designs": {}}
    spent = 0
    for design in sorted(designs, key=lambda d: d != DEFAULT_DESIGN):   # default design first
        chunks = corpus_chunks(design)
        write_chunks(chunks, _chunks_path(design))
        budget = max(0, DAILY_SAFETY_LIMIT - spent)
        log(f"\nDesign '{design}': {len(chunks)} chunks "
            f"({sum(c.words for c in chunks) // max(1, len(chunks))} words on average)")
        embedded, missing = embed_and_store(chunks, _vectors_path(design), budget)
        spent += embedded
        manifest["designs"][design] = {"chunks": len(chunks), "embedded_this_run": embedded, "still_missing": missing}
        log(f"  {embedded} new embeddings, {len(chunks) - missing} of {len(chunks)} chunks have a saved vector")
    (INDEX_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False), encoding="utf-8")
    log(f"\nDone. Embeddings spent this run: {spent}.")
    if any(d["still_missing"] for d in manifest["designs"].values()):
        log("Some chunks are not embedded yet (daily limit). Run `uv run python main.py index` again after 09:00 Spain time.")
        sys.exit(2)


def main() -> None:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        sys.stderr.reconfigure(encoding="utf-8", errors="replace")
    parser = argparse.ArgumentParser(description="Build the index: download, chunk, embed, save.")
    parser.add_argument("--design", choices=[*DESIGNS, "all"], default="all")
    parser.add_argument("--stats", action="store_true", help="only print corpus and chunk statistics (no API calls)")
    parser.add_argument("--search", metavar="QUERY",
                        help="print what the search tool returns for QUERY, from the saved index (one embedding)")
    args = parser.parse_args()
    designs = DESIGNS if args.design == "all" else (args.design,)
    if args.search:
        print(format_hits(args.search, Index().search(args.search, k=DEFAULT_K, mode=DEFAULT_MODE)))
        return
    if args.stats:
        download_corpus()
        for row in corpus_stats():
            print(f"{row['source']:<16} {row['words']:>7,} words {row['units']:>3} units")
        for design in designs:
            chunks = corpus_chunks(design)
            print(f"design {design}: {len(chunks)} chunks, mean {sum(c.words for c in chunks) / len(chunks):.0f} words")
        return
    build_index(designs)


if __name__ == "__main__":
    main()
