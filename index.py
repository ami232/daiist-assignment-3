"""
Assignment 3: build the index (`main.py index`).

Downloads the corpus into corpus/, extracts it into sections with source and
location metadata, chunks it in two designs, embeds the chunks with Gemini and
stores them in index/chroma/ (one ChromaDB collection per design).

    uv run python main.py index          # embed what is missing, B first, then A
    uv run python index.py --dry-run     # count chunks and missing vectors, no API calls

Corpus: four EU public procurement texts from EUR-Lex.
Reuse is allowed under Commission Decision 2011/833/EU.
© European Union, https://eur-lex.europa.eu

Per-file steps are importable functions (server.py's add_document reuses them):
    extract_file(path) -> list of section dicts
    chunk_file(path, design) -> list of chunk dicts
    embed_texts(texts, task) -> list of vectors
    embed_and_store(chunks, design) -> how many were added and how many are left
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import time
from collections import defaultdict
from pathlib import Path

import httpx
from bs4 import BeautifulSoup, NavigableString, Tag

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"

CREDIT = "© European Union, https://eur-lex.europa.eu"

# doc_id -> what it is and where it comes from. `url` is the citable EUR-Lex address.
DOCS = [
    {
        "doc_id": "dir_2014_24",
        "title": "Directive 2014/24/EU on public procurement",
        "celex": "32014L0024",
        "short": "Directive 2014/24/EU",
        "eli": "dir/2014/24/oj",
    },
    {
        "doc_id": "reg_2016_7",
        "title": "Implementing Regulation (EU) 2016/7, standard form for the European Single Procurement Document (ESPD)",
        "celex": "32016R0007",
        "short": "Implementing Regulation (EU) 2016/7 (ESPD)",
        "eli": "reg_impl/2016/7/oj",
    },
    {
        "doc_id": "dir_89_665",
        "title": "Directive 89/665/EEC on review procedures (Remedies Directive), consolidated version of 17.04.2014",
        "celex": "01989L0665-20140417",
        "short": "Directive 89/665/EEC (Remedies)",
        "eli": "dir/1989/665/2014-04-17",
    },
    {
        "doc_id": "reg_2025_2152",
        "title": "Delegated Regulation (EU) 2025/2152, procurement thresholds for 2026-2027",
        "celex": "32025R2152",
        "short": "Delegated Regulation (EU) 2025/2152",
        "eli": "reg_del/2025/2152/oj",
    },
]
for _d in DOCS:
    _d["url"] = f"https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:{_d['celex']}"
DOCS_BY_ID = {d["doc_id"]: d for d in DOCS}

# If articles + annexes reach this many words, recitals are dropped.
RECITAL_RULE_WORDS = 52_000

BROWSER_UA = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/130.0 Safari/537.36"
)


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


# --------------------------------------------------------------------------
# Download
# --------------------------------------------------------------------------

def _candidate_urls(doc: dict) -> list[tuple[str, str, dict]]:
    """(suffix, url, headers) to try in order. EUR-Lex first, then its ELI
    address, then the Publications Office store behind EUR-Lex (same file,
    no bot check), then the EUR-Lex PDF."""
    celex = doc["celex"]
    html_accept = {"Accept": "application/xhtml+xml, text/html", "Accept-Language": "en"}
    return [
        (".html", f"https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:{celex}", {}),
        (".html", f"https://eur-lex.europa.eu/eli/{doc['eli']}/eng", {}),
        (".html", f"http://publications.europa.eu/resource/celex/{celex}", html_accept),
        (".pdf", f"https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:{celex}", {}),
        (".pdf", f"http://publications.europa.eu/resource/celex/{celex}",
         {"Accept": "application/pdf", "Accept-Language": "en"}),
    ]


def _looks_like_document(suffix: str, content: bytes) -> bool:
    """A bot-check answer is an empty 202 or a small script page."""
    if suffix == ".pdf":
        return content[:5] == b"%PDF-" and len(content) > 20_000
    return len(content) > 8_000 and b"Article" in content


def download_corpus() -> list[Path]:
    """Fetch each corpus document into corpus/ if it is not there yet."""
    CORPUS_DIR.mkdir(exist_ok=True)
    paths, failed = [], []
    for doc in DOCS:
        existing = [p for p in (CORPUS_DIR / f"{doc['doc_id']}{s}" for s in (".html", ".pdf")) if p.exists()]
        if existing:
            paths.append(existing[0])
            continue
        saved = None
        with httpx.Client(follow_redirects=True, timeout=120, headers={"User-Agent": BROWSER_UA}) as client:
            for suffix, url, headers in _candidate_urls(doc):
                try:
                    response = client.get(url, headers=headers)
                except httpx.HTTPError as error:
                    log(f"  {doc['doc_id']}: {url} failed ({type(error).__name__})")
                    continue
                if response.status_code == 200 and _looks_like_document(suffix, response.content):
                    saved = CORPUS_DIR / f"{doc['doc_id']}{suffix}"
                    saved.write_bytes(response.content)
                    log(f"  {doc['doc_id']}: saved {saved.name} ({len(response.content) / 1e6:.2f} MB) from {url}")
                    break
                log(f"  {doc['doc_id']}: {url} gave HTTP {response.status_code}, "
                    f"{len(response.content)} bytes (bot check or not a document)")
        if saved:
            paths.append(saved)
        else:
            failed.append(doc)
    if failed:
        lines = ["Could not download these documents. Download them by hand in a browser and save them as:"]
        for doc in failed:
            lines.append(
                f"  corpus/{doc['doc_id']}.html  <-  "
                f"https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:{doc['celex']}"
            )
        raise SystemExit("\n".join(lines))
    return paths


# --------------------------------------------------------------------------
# Text cleaning
# --------------------------------------------------------------------------

_SPACES = re.compile(r"[   -​  　﻿\s]+")
# Markers of consolidated texts: ▼B ▼M1 ►M3 ◄ ▲ ▶ ◀ and friends.
_CONSOLIDATION = re.compile(r"[▼►◄▲▶◀]\s*(?:[BMCA]\d*\b)?")


def clean(text: str) -> str:
    text = text.replace("­", "")  # soft hyphen
    text = _CONSOLIDATION.sub(" ", text)
    text = _SPACES.sub(" ", text).strip()
    text = re.sub(r"\s+([,;:.)\]])", r"\1", text)
    text = re.sub(r"([(\[])\s+", r"\1", text)
    return text


def words(text: str) -> int:
    return len(text.split())


# --------------------------------------------------------------------------
# File -> lines. A line is (text, tag); tag is a structural hint or "".
#   art       "Article 58"            art_head  the article's title
#   doc_ti    "ANNEX XII" (or a document title)
#   sub       a sub-heading inside an annex
#   struct    TITLE / CHAPTER / Section headings (dropped)
# --------------------------------------------------------------------------

_CLASS_TAGS = {
    "oj-ti-art": "art", "title-article-norm": "art",
    "oj-sti-art": "art_head", "stitle-article-norm": "art_head",
    "oj-doc-ti": "doc_ti", "title-annex-1": "doc_ti", "title-doc-first": "doc_ti",
    "oj-ti-grseq-1": "sub", "title-gr-seq-level-1": "sub", "title-annex-2": "sub",
    "oj-ti-section-1": "struct", "oj-ti-section-2": "struct",
    "title-division-1": "struct", "title-division-2": "struct",
}
# Whole elements that are not legal text: footnotes, signatures, OJ page
# headers, consolidation markers and the consolidated version's front matter.
_DROP_CLASSES = {
    "oj-note", "footnote", "oj-signatory", "oj-final", "oj-hd-date", "oj-hd-lg", "oj-hd-ti",
    "oj-hd-oj", "oj-hd-coll", "oj-hd-uniq", "oj-image", "modref", "arrow", "disclaimer",
    "reference", "hd-modifiers", "title-fam-member-star", "title-doc-oj-reference",
    "toc-1", "toc-2", "hd-toc-1", "hd-toc-2", "hd-toc-3", "oj-note-tag",
}
_DROP_TAGS = {"script", "style", "head", "img", "figure", "hr", "col", "colgroup", "noscript", "nav"}
_BLOCK_TAGS = {
    "p", "div", "table", "tbody", "thead", "tr", "td", "th", "ul", "ol", "li", "dl", "dt", "dd",
    "h1", "h2", "h3", "h4", "h5", "h6", "section", "article", "blockquote", "body", "html", "br",
    "pre", "header", "footer", "main",
}
_LIST_MARKER = re.compile(r"^(\(?[0-9]{1,3}[.)]|\(?[a-z]{1,4}\)|\(?[ivxlc]+\)|[—–\-•]|\([0-9]{1,3}\))$", re.I)


def _classes(node: Tag) -> set[str]:
    return set(node.get("class") or [])


def _is_footnote_link(node: Tag) -> bool:
    if node.name != "a":
        return False
    href = node.get("href") or ""
    if href.startswith("#ntr") or href.startswith("#src.") or href.startswith("#E0"):
        return True
    if node.get("id", "").startswith("textofimagelink"):  # "Text of image" button
        return True
    return node.find(class_=["oj-note-tag", "superscript"]) is not None


def _render(node, out: list[tuple[str, str]]) -> None:
    """Append the lines of `node` to `out`, keeping reading order."""
    buffer: list[str] = []

    def flush(tag: str = "") -> None:
        text = clean("".join(buffer))
        buffer.clear()
        # "(1)" left behind by a removed footnote link looks like "()" or "( )"
        text = clean(re.sub(r"\(\s*\)", " ", text))
        if text:
            out.append((text, tag))

    def tag_of(el: Tag) -> str:
        for cls in el.get("class") or []:
            if cls in _CLASS_TAGS:
                return _CLASS_TAGS[cls]
        if el.name in ("h1", "h2", "h3", "h4", "h5", "h6"):
            return "sub"
        return ""

    def walk(el, inherited: str) -> None:
        for child in el.children:
            if isinstance(child, NavigableString):
                if type(child) is NavigableString:  # skip comments, doctype
                    buffer.append(str(child))
                continue
            if not isinstance(child, Tag):
                continue
            name, cls = child.name, _classes(child)
            if name in _DROP_TAGS or cls & _DROP_CLASSES or _is_footnote_link(child):
                continue
            if name == "table":
                flush(inherited)
                _render_table(child, out)
                continue
            if "grid-container" in cls:  # list item in consolidated texts
                flush(inherited)
                _render_marker_item(list(child.find_all("div", recursive=False)), out)
                continue
            inline = name not in _BLOCK_TAGS or "inline-element" in cls
            if inline:
                walk(child, inherited)
                continue
            if name == "br":
                flush(inherited)
                continue
            flush(inherited)
            own = tag_of(child) or inherited
            walk(child, own)
            flush(own)

    walk(node, "")
    flush()


def _render_marker_item(cells: list[Tag], out: list[tuple[str, str]]) -> bool:
    """Two cells where the first is a list marker: '(a)' + text -> '(a) text'."""
    if len(cells) != 2:
        return False
    marker = clean(cells[0].get_text(" "))
    if not _LIST_MARKER.match(marker):
        return False
    body: list[tuple[str, str]] = []
    _render(cells[1], body)
    if not body:
        return True
    out.append((f"{marker} {body[0][0]}", ""))
    out.extend(body[1:])
    return True


def _render_table(table: Tag, out: list[tuple[str, str]]) -> None:
    """Layout tables that hold a list become '(a) text' lines.
    Real tables become one line per row with ' | ' between cells."""
    rows = []
    for section in [table] + table.find_all(["tbody", "thead", "tfoot"], recursive=False):
        rows.extend(section.find_all("tr", recursive=False))
    for row in rows:
        cells = row.find_all(["td", "th"], recursive=False)
        if _render_marker_item(cells, out):
            continue
        rendered = []
        for cell in cells:
            lines: list[tuple[str, str]] = []
            _render(cell, lines)
            rendered.append(lines)
        rendered = [r for r in rendered if r]
        if not rendered:
            continue
        if len(rendered) == 1:
            out.extend(rendered[0])  # a one-cell wrapper, keep its lines and tags
        else:
            out.append((" | ".join(" ".join(t for t, _ in lines) for lines in rendered), ""))


def html_to_lines(html: str) -> tuple[list[tuple[str, str]], str]:
    soup = BeautifulSoup(html, "html.parser")
    title = ""
    main = soup.find(class_="eli-main-title")
    if main:
        title = clean(main.get_text(" "))
    elif soup.title:
        title = clean(soup.title.get_text(" "))
    lines: list[tuple[str, str]] = []
    _render(soup.body or soup, lines)
    return lines, title


def pdf_to_lines(path: Path) -> tuple[list[tuple[str, str]], str]:
    from pypdf import PdfReader

    reader = PdfReader(str(path))
    lines: list[tuple[str, str]] = []
    for number, page in enumerate(reader.pages, start=1):
        lines.append((f"Page {number}", "page"))
        text = page.extract_text() or ""
        # Join the lines of one paragraph; keep a break before headings and numbered items.
        paragraph: list[str] = []
        for raw in text.splitlines():
            line = clean(raw)
            starts_new = (
                not line
                or _ARTICLE.match(line) or _ANNEX.match(line) or _STRUCT.match(line)
                or re.match(r"^(\d{1,3}\.|\(\d{1,3}\)|\([a-z]{1,4}\))\s", line)
            )
            if starts_new and paragraph:
                lines.append((clean(" ".join(paragraph)), ""))
                paragraph = []
            if line:
                paragraph.append(line)
                if _ARTICLE.match(line) or _ANNEX.match(line) or _STRUCT.match(line):
                    lines.append((line, ""))
                    paragraph = []
        if paragraph:
            lines.append((clean(" ".join(paragraph)), ""))
    title = clean((reader.metadata.title if reader.metadata and reader.metadata.title else "") or "")
    return lines, title


def text_to_lines(text: str) -> tuple[list[tuple[str, str]], str]:
    lines = []
    for raw in text.splitlines():
        is_heading = raw.lstrip().startswith("#")
        line = clean(raw.lstrip().lstrip("#")) if is_heading else clean(raw)
        if line:
            lines.append((line, "sub" if is_heading else ""))
    title = lines[0][0] if lines else ""
    return lines, title[:200]


# --------------------------------------------------------------------------
# Lines -> sections
# --------------------------------------------------------------------------

_ARTICLE = re.compile(r"^Article\s+(\d+)\s?([a-z])?$", re.I)
_ANNEX = re.compile(r"^ANNEX(?:\s+([IVXLC]+|\d+))?$", re.I)
_STRUCT = re.compile(r"^(TITLE|CHAPTER|SECTION|SUBSECTION|Section|Subsection|PART)\s+([IVXLC]+|\d+)$")
_RECITAL = re.compile(r"^\((\d{1,3})\)\s+(.*)$", re.S)
_PARAGRAPH = re.compile(r"^(\d{1,2})\.\s+(\S.*)$", re.S)
_ANNEX_PART = re.compile(r"^(PART|Part)\s+([IVXLC]+|[A-Z]|\d+)\b[:.]?\s*(.*)$", re.S)
_ENACTING = re.compile(r"^(HAVE|HAS)\s+ADOPTED\s+THIS", re.I)
_SIGN_OFF = re.compile(r"^Done at\s+\w+", re.I)


def _short_heading(text: str) -> bool:
    return words(text) <= 14 and not re.search(r"[.:;,]$", text) and not re.match(r"^[(\d]", text)


def lines_to_sections(lines: list[tuple[str, str]], doc_id: str, title: str) -> list[dict]:
    sections: list[dict] = []
    current: dict | None = None

    def close() -> None:
        nonlocal current
        if current and current["lines"]:
            text = "\n".join(current["lines"])
            sections.append({
                "doc_id": doc_id,
                "title": title,
                "part": current["part"],
                "location": current["location"],
                "heading": current["heading"],
                "paragraph": current["paragraph"],
                "text": text,
                "words": words(text),
            })
        current = None

    def open_section(part: str, location: str, heading: str = "", paragraph: str = "") -> None:
        nonlocal current
        close()
        current = {"part": part, "location": location, "heading": heading, "paragraph": paragraph, "lines": []}

    has_structure = any(_ARTICLE.match(t) or tag == "art" for t, tag in lines)
    mode = "preamble" if has_structure else "body"  # preamble | recitals | article | annex | body
    last_article = (0, "")
    last_paragraph = 0
    article_heading = annex_heading = ""
    expect = ""         # "art_head" or "annex_head": the next line may be a title
    skip_struct_title = False
    page = block = 0

    for text, tag in lines:
        if tag == "page":
            page = int(text.split()[1])
            if mode == "body":
                open_section("body", f"Page {page}")
            continue

        # --- structural headings: TITLE I / CHAPTER II / Section 3 and their titles
        if tag == "struct" or (mode in ("article", "preamble", "recitals") and _STRUCT.match(text)):
            skip_struct_title = tag != "struct"
            expect = ""
            continue
        if skip_struct_title:
            skip_struct_title = False
            if _short_heading(text) and not _ARTICLE.match(text):
                continue

        # --- Article N
        match = _ARTICLE.match(text)
        if match and tag in ("art", "") and mode != "annex":
            number, letter = int(match.group(1)), (match.group(2) or "").lower()
            in_order = tag == "art" or (number, letter) > last_article
            if in_order:
                last_article = (number, letter)
                last_paragraph = 0
                article_heading = ""
                mode = "article"
                open_section("article", f"Article {number}{letter}")
                expect = "art_head"
                continue

        # --- ANNEX X
        match = _ANNEX.match(text)
        if match and tag in ("doc_ti", "") and has_structure:
            mode = "annex"
            annex_heading = ""
            name = (match.group(1) or "").upper()
            open_section("annex", f"Annex {name}".strip())
            expect = "annex_head"
            continue

        if tag == "doc_ti" and mode != "annex":
            continue  # the act's own title lines; `title` already holds it

        # --- titles right after "Article N" / "ANNEX X"
        if expect == "art_head":
            expect = ""
            if tag == "art_head" or (tag == "" and _short_heading(text) and not _PARAGRAPH.match(text)):
                article_heading = text
                current["heading"] = text
                continue
        elif expect == "annex_head":
            if tag in ("sub", "doc_ti") or (tag == "" and _short_heading(text)):
                part = _ANNEX_PART.match(text)
                if not part:
                    annex_heading = text  # only the first line is the annex title
                    current["heading"] = annex_heading
                    expect = ""
                    continue
            expect = ""

        if re.match(r"^(ELI: |ISSN \d)", text):
            continue  # OJ page footer

        if mode == "preamble":
            if text.rstrip(":").strip().lower() == "whereas":
                mode = "recitals"
            continue  # citations ("Having regard to ...") are not kept

        if mode == "recitals":
            if _ENACTING.match(text):
                close()
                mode = "preamble"
                continue
            match = _RECITAL.match(text)
            if match:
                open_section("recital", f"Recital {match.group(1)}", paragraph=match.group(1))
                current["lines"].append(match.group(2))
            elif current:
                current["lines"].append(text)
            continue

        if mode == "article":
            if _SIGN_OFF.match(text):
                close()
                mode = "preamble"
                continue
            match = _PARAGRAPH.match(text)
            if match and int(match.group(1)) == last_paragraph + 1:
                last_paragraph = int(match.group(1))
                location = current["location"] if current else f"Article {last_article[0]}{last_article[1]}"
                if current and not current["lines"]:
                    current["paragraph"] = str(last_paragraph)
                else:
                    open_section("article", location, article_heading, str(last_paragraph))
            if current is None:
                open_section("article", f"Article {last_article[0]}{last_article[1]}", article_heading)
            current["lines"].append(text)
            continue

        if mode == "annex":
            part = _ANNEX_PART.match(text) if (tag == "sub" or _short_heading(text)) else None
            if part:
                location = current["location"]
                label = f"Part {part.group(2)}"
                rest = clean(part.group(3))
                heading = f"{annex_heading}. {label}: {rest}".strip(" .:") if rest else f"{annex_heading}. {label}".strip(" .")
                if current["lines"]:
                    open_section("annex", location, heading, label)
                else:
                    current["heading"], current["paragraph"] = heading, label
                continue
            current["lines"].append(text)
            continue

        # --- body: a document without Article / Annex structure
        if tag == "sub" or current is None:
            block += 1
            location = f"Page {page}" if page else f"Section {block}"
            open_section("body", location, text if tag == "sub" else "")
            if tag == "sub":
                continue
        current["lines"].append(text)

    close()
    return sections


def doc_id_for(path: Path) -> str:
    """corpus/dir_2014_24.html -> dir_2014_24; any other file -> a slug of its name."""
    return re.sub(r"[^a-z0-9]+", "_", path.stem.lower()).strip("_") or "document"


def extract_file(path: str | Path, doc_id: str | None = None, title: str | None = None) -> list[dict]:
    """One file (.html, .htm, .pdf, .txt, .md) -> its sections.

    Each section: doc_id, title, part (recital / article / annex / body),
    location ("Article 58", "Annex XII", "Recital 3"), heading, paragraph, text, words.
    """
    path = Path(path)
    doc_id = doc_id or doc_id_for(path)
    suffix = path.suffix.lower()
    if suffix in (".html", ".htm", ".xhtml"):
        lines, found_title = html_to_lines(path.read_text(encoding="utf-8", errors="replace"))
    elif suffix == ".pdf":
        lines, found_title = pdf_to_lines(path)
    elif suffix in (".txt", ".md"):
        lines, found_title = text_to_lines(path.read_text(encoding="utf-8", errors="replace"))
    else:
        raise ValueError(f"Unsupported file type: {path.suffix} (use .pdf, .html, .htm, .txt or .md)")
    known = DOCS_BY_ID.get(doc_id, {})
    title = title or known.get("title") or found_title or path.stem
    return lines_to_sections(lines, doc_id, title)


# --------------------------------------------------------------------------
# Whole corpus
# --------------------------------------------------------------------------

def corpus_paths() -> list[Path]:
    return download_corpus()


def word_table(sections: list[dict]) -> dict[str, dict[str, int]]:
    table: dict[str, dict[str, int]] = defaultdict(lambda: defaultdict(int))
    for section in sections:
        table[section["doc_id"]][section["part"]] += section["words"]
    return table


def print_word_table(sections: list[dict]) -> None:
    table = word_table(sections)
    parts = ["recital", "article", "annex"]
    print(f"{'document':<16}{'recitals':>10}{'articles':>10}{'annexes':>10}{'total':>10}{'sections':>10}")
    totals = defaultdict(int)
    for doc in DOCS:
        row = table.get(doc["doc_id"], {})
        count = sum(1 for s in sections if s["doc_id"] == doc["doc_id"])
        print(f"{doc['doc_id']:<16}" + "".join(f"{row.get(p, 0):>10,}" for p in parts)
              + f"{sum(row.values()):>10,}{count:>10,}")
        for part in parts:
            totals[part] += row.get(part, 0)
    print(f"{'TOTAL':<16}" + "".join(f"{totals[p]:>10,}" for p in parts)
          + f"{sum(totals.values()):>10,}{len(sections):>10,}")


def load_corpus_sections(verbose: bool = False) -> list[dict]:
    """All sections of the corpus, with the recital rule applied."""
    sections: list[dict] = []
    for path in corpus_paths():
        sections.extend(extract_file(path))
    body_words = sum(s["words"] for s in sections if s["part"] in ("article", "annex"))
    drop = body_words >= RECITAL_RULE_WORDS
    if verbose:
        print("Words extracted (before the recital rule):")
        print_word_table(sections)
        print(f"\nArticles + annexes: {body_words:,} words. Rule: drop recitals at {RECITAL_RULE_WORDS:,} or more "
              f"-> recitals {'DROPPED' if drop else 'KEPT (part=recital)'}.")
    if drop:
        sections = [s for s in sections if s["part"] != "recital"]
    return sections


# --------------------------------------------------------------------------
# Chunking: two designs
#   "fixed"      A: windows of ~250 words with 50 words overlap inside a document
#   "structure"  B: one chunk per article / annex part, long ones split at paragraphs
# --------------------------------------------------------------------------

DESIGNS = ("structure", "fixed")  # build order: B first, then A
FIXED_WORDS, FIXED_OVERLAP = 250, 50
STRUCTURE_MAX_WORDS, STRUCTURE_MIN_WORDS = 400, 40

EMBED_MODEL = "gemini-embedding-2"
EMBED_BATCH = 100
DEFAULT_CONFIG = {"design": "structure", "mode": "vector", "k": 5}


def index_dir() -> Path:
    """index/ by default; INDEX_DIR overrides it (the add-document demo uses a copy)."""
    return Path(os.environ.get("INDEX_DIR") or ROOT / "index").resolve()


def file_sha256(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _chunk_id(design: str, doc_id: str, text: str) -> str:
    return hashlib.sha256(f"{design}\n{doc_id}\n{text}".encode("utf-8")).hexdigest()


def _unique(items: list[str]) -> list[str]:
    return list(dict.fromkeys(i for i in items if i))


def _paragraph_label(paragraphs: list[str]) -> str:
    paragraphs = _unique(paragraphs)
    if len(paragraphs) <= 1:
        return paragraphs[0] if paragraphs else ""
    return f"{paragraphs[0]}-{paragraphs[-1]}"


def _fixed_chunks(sections: list[dict]) -> list[dict]:
    """Design A. The window slides over the document's words and ignores structure."""
    stream: list[tuple[str, int]] = []  # (word, index of its section)
    for number, section in enumerate(sections):
        stream.extend((word, number) for word in section["text"].split())
    pieces, step, start = [], FIXED_WORDS - FIXED_OVERLAP, 0
    while start < len(stream):
        window = stream[start:start + FIXED_WORDS]
        if start > 0 and len(window) <= FIXED_OVERLAP:
            break  # nothing new: these words are already in the previous window
        touched = [sections[n] for n in dict.fromkeys(n for _, n in window)]
        pieces.append({
            "text": " ".join(word for word, _ in window),
            "sections": touched,
        })
        start += step
    return pieces


def _split_long(text: str, limit: int) -> list[str]:
    """Split one long paragraph at line breaks, and a very long line by words."""
    lines: list[str] = []
    for line in text.split("\n"):
        tokens = line.split()
        if len(tokens) <= limit:
            lines.append(line)
        else:
            lines.extend(" ".join(tokens[i:i + limit]) for i in range(0, len(tokens), limit))
    parts, current, count = [], [], 0
    for line in lines:
        size = words(line)
        if current and count + size > limit:
            parts.append("\n".join(current))
            current, count = [], 0
        current.append(line)
        count += size
    if current:
        parts.append("\n".join(current))
    return parts


def _structure_chunks(sections: list[dict]) -> list[dict]:
    """Design B. Sections of one article (or one annex part) stay together when
    they fit in STRUCTURE_MAX_WORDS; otherwise they are packed paragraph by paragraph."""
    groups: dict[tuple, list[dict]] = {}
    for section in sections:
        key = (section["location"], section["paragraph"] if section["part"] != "article" else "")
        groups.setdefault(key, []).append(section)

    pieces = []
    for group in groups.values():
        units: list[tuple[str, dict]] = []  # (text, section it comes from)
        for section in group:
            if section["words"] <= STRUCTURE_MAX_WORDS:
                units.append((section["text"], section))
            else:
                units.extend((part, section) for part in _split_long(section["text"], STRUCTURE_MAX_WORDS))
        packed: list[list[tuple[str, dict]]] = []
        count = 0
        for unit in units:
            size = words(unit[0])
            if packed and count + size <= STRUCTURE_MAX_WORDS:
                packed[-1].append(unit)
                count += size
            else:
                packed.append([unit])
                count = size
        # a tiny tail joins its neighbour from the same article
        if len(packed) > 1 and sum(words(t) for t, _ in packed[-1]) < STRUCTURE_MIN_WORDS:
            packed[-2].extend(packed.pop())
        for units_in_chunk in packed:
            pieces.append({
                "text": "\n".join(text for text, _ in units_in_chunk),
                "sections": list({id(s): s for _, s in units_in_chunk}.values()),
            })
    return pieces


def chunk_sections(sections: list[dict], design: str, url: str = "", sha: str = "") -> list[dict]:
    """Sections of ONE document -> chunks with metadata, for one design."""
    if not sections:
        return []
    if design == "fixed":
        pieces = _fixed_chunks(sections)
    elif design == "structure":
        pieces = _structure_chunks(sections)
    else:
        raise ValueError(f"Unknown design {design!r}; use one of {DESIGNS}")
    doc_id, doc_title = sections[0]["doc_id"], sections[0]["title"]
    short = DOCS_BY_ID.get(doc_id, {}).get("short") or doc_title
    chunks, seen = [], set()
    for piece in pieces:
        touched = piece["sections"]
        first = touched[0]
        locations = _unique([s["location"] for s in touched])
        paragraph = _paragraph_label([s["paragraph"] for s in touched if s["location"] == first["location"]])
        if design == "structure":
            header = ", ".join(x for x in (
                short, first["location"], first["heading"],
                (f"paragraph {paragraph}" if first["part"] == "article" and paragraph else ""),
            ) if x)
        else:
            header = short
        chunk_id = _chunk_id(design, doc_id, piece["text"])
        if chunk_id in seen:
            continue
        seen.add(chunk_id)
        chunks.append({
            "chunk_id": chunk_id,
            "text": piece["text"],
            "header": header,
            "doc_id": doc_id,
            "doc_title": doc_title,
            "part": first["part"],
            "location": first["location"],
            "locations": ";".join(locations),
            "heading": first["heading"],
            "paragraph": paragraph,
            "url": url,
            "file_sha256": sha,
            "words": words(piece["text"]),
            "design": design,
        })
    return chunks


def chunk_file(path: str | Path, design: str, doc_id: str | None = None,
               drop_parts: tuple[str, ...] = ()) -> list[dict]:
    """One file -> chunks for one design ("fixed" or "structure")."""
    path = Path(path)
    sections = [s for s in extract_file(path, doc_id=doc_id) if s["part"] not in drop_parts]
    doc_id = sections[0]["doc_id"] if sections else (doc_id or doc_id_for(path))
    url = DOCS_BY_ID.get(doc_id, {}).get("url", "")
    if not url:
        try:
            url = str(path.resolve().relative_to(ROOT))
        except ValueError:
            url = path.name
    return chunk_sections(sections, design, url=url, sha=file_sha256(path))


def corpus_drop_parts() -> tuple[str, ...]:
    """The recital rule, decided from the corpus word counts."""
    sections = [s for path in corpus_paths() for s in extract_file(path)]
    body_words = sum(s["words"] for s in sections if s["part"] in ("article", "annex"))
    return ("recital",) if body_words >= RECITAL_RULE_WORDS else ()


def chunk_corpus(design: str) -> list[dict]:
    drop = corpus_drop_parts()
    return [chunk for path in corpus_paths() for chunk in chunk_file(path, design, drop_parts=drop)]


# --------------------------------------------------------------------------
# Embedding and storing
# --------------------------------------------------------------------------

class QuotaExceeded(RuntimeError):
    """The Gemini quota is used up; what is already stored stays stored."""


_client = None


def _genai_client():
    global _client
    if _client is None:
        from google import genai

        from api_key import load_api_key

        _client = genai.Client(api_key=load_api_key())
    return _client


def prepare_text(text: str, task: str, title: str | None = None) -> str:
    """gemini-embedding-2 has no task_type parameter: the task goes in the text."""
    if task == "query":
        return f"task: search result | query: {text}"
    if task == "document":
        return f"title: {title or 'none'} | text: {text}"
    raise ValueError("task must be 'document' or 'query'")


def _is_quota_error(error: Exception) -> bool:
    code = getattr(error, "code", None)
    message = str(error)
    return code == 429 or "RESOURCE_EXHAUSTED" in message or "429" in message[:20]


def _is_daily_quota(error: Exception) -> bool:
    message = str(error).lower()
    return "perday" in message or "per day" in message or "daily" in message


def embed_texts(texts: list[str], task: str, titles: list[str] | None = None) -> list[list[float]]:
    """One vector per text. task is "document" or "query".

    Each text goes in its own Content object; a plain list of strings would
    come back as ONE aggregated vector with this model."""
    from google.genai import types

    if not texts:
        return []
    titles = titles or [None] * len(texts)
    prepared = [prepare_text(text, task, title) for text, title in zip(texts, titles)]
    contents = [types.Content(parts=[types.Part.from_text(text=p)]) for p in prepared]
    waits = [20, 45, 65]  # a per-minute limit clears within about a minute
    while True:
        try:
            result = _genai_client().models.embed_content(model=EMBED_MODEL, contents=contents)
            break
        except Exception as error:  # noqa: BLE001 - sorted into quota / other below
            if not _is_quota_error(error):
                raise
            if _is_daily_quota(error) or not waits:
                raise QuotaExceeded(str(error)[:300]) from error
            wait = waits.pop(0)
            log(f"  rate limit (429); waiting {wait}s and trying again")
            time.sleep(wait)
    vectors = [list(e.values) for e in result.embeddings]
    if len(vectors) != len(texts):
        raise RuntimeError(f"Asked for {len(texts)} embeddings, got {len(vectors)}.")
    return vectors


def open_collection(design: str):
    import chromadb

    if design not in DESIGNS:
        raise ValueError(f"Unknown design {design!r}; use one of {DESIGNS}")
    folder = index_dir() / "chroma"
    folder.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(folder))
    return client.get_or_create_collection(design, metadata={"hnsw:space": "cosine"})


def missing_chunks(chunks: list[dict], collection) -> list[dict]:
    if not chunks:
        return []
    stored = set(collection.get(ids=[c["chunk_id"] for c in chunks], include=[])["ids"])
    return [c for c in chunks if c["chunk_id"] not in stored]


_META_KEYS = ("chunk_id", "doc_id", "doc_title", "part", "location", "locations", "heading",
              "paragraph", "url", "file_sha256", "words", "header", "design")


def embed_and_store(chunks: list[dict], design: str, collection=None) -> dict:
    """Embed the chunks that have no vector yet and save each batch at once.

    Returns {"added": n, "left": m, "quota": True if the quota stopped it}."""
    collection = collection if collection is not None else open_collection(design)
    todo = missing_chunks(chunks, collection)
    added = 0
    for start in range(0, len(todo), EMBED_BATCH):
        batch = todo[start:start + EMBED_BATCH]
        try:
            vectors = embed_texts([c["text"] for c in batch], "document", [c["header"] for c in batch])
        except QuotaExceeded as error:
            log(f"  quota: {error}")
            return {"added": added, "left": len(todo) - added, "quota": True}
        collection.upsert(
            ids=[c["chunk_id"] for c in batch],
            embeddings=vectors,
            documents=[c["text"] for c in batch],
            metadatas=[{k: c[k] for k in _META_KEYS} for c in batch],
        )
        added += len(batch)
        log(f"  {design}: saved {added}/{len(todo)}")
    return {"added": added, "left": 0, "quota": False}


def remove_stale(chunks: list[dict], collection) -> int:
    """Delete chunks of corpus documents that the current chunking no longer produces."""
    current = {c["chunk_id"] for c in chunks}
    stale = []
    for doc in DOCS:
        stored = collection.get(where={"doc_id": doc["doc_id"]}, include=[])["ids"]
        stale.extend(i for i in stored if i not in current)
    if stale:
        collection.delete(ids=stale)
    return len(stale)


def ensure_config() -> Path:
    path = index_dir() / "config.json"
    if not path.exists():
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(json.dumps(DEFAULT_CONFIG, indent=2) + "\n", encoding="utf-8")
    return path


def build_index(dry_run: bool = False) -> None:
    sections = load_corpus_sections(verbose=False)
    print("Words in the corpus:")
    print_word_table(sections)
    print()
    stopped = False
    for design in DESIGNS:
        chunks = chunk_corpus(design)
        collection = open_collection(design)
        todo = missing_chunks(chunks, collection)
        sizes = sorted(c["words"] for c in chunks)
        print(f"{design:<10} {len(chunks):>4} chunks, median {sizes[len(sizes) // 2]} words, "
              f"max {sizes[-1]} words; {len(todo)} still missing a vector")
        if dry_run or stopped:
            continue
        removed = remove_stale(chunks, collection)
        if removed:
            print(f"{'':<10} removed {removed} outdated chunk(s)")
        result = embed_and_store(chunks, design, collection)
        print(f"{'':<10} embedded {result['added']} now, {result['left']} left; "
              f"collection holds {collection.count()} chunks")
        if result["quota"]:
            stopped = True
    if dry_run:
        print("\nDry run: no API calls made.")
        return
    ensure_config()
    if stopped:
        print("\nThe embedding quota is used up. Everything embedded so far is saved.\n"
              "Run again after 09:00 Madrid: `uv run python main.py index`.")
    else:
        print(f"\nIndex complete in {index_dir()}.")
    print(f"Source and licence: {CREDIT} (reuse under Commission Decision 2011/833/EU).")


def main() -> None:
    build_index(dry_run="--dry-run" in sys.argv[1:])
    sys.exit(0)


if __name__ == "__main__":
    main()
