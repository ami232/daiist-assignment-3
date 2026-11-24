"""
Assignment 3: build the index (`main.py index`).

Stage 1 (this file, so far): download the corpus into corpus/ and extract it
into sections with source and location metadata. No embeddings yet.

Corpus: four EU public procurement texts from EUR-Lex.
Reuse is allowed under Commission Decision 2011/833/EU.
© European Union, https://eur-lex.europa.eu

Per-file steps are importable functions (server.py's add_document reuses them):
    extract_file(path) -> list of section dicts
"""

from __future__ import annotations

import re
import sys
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
        "eli": "dir/2014/24/oj",
    },
    {
        "doc_id": "reg_2016_7",
        "title": "Implementing Regulation (EU) 2016/7, standard form for the European Single Procurement Document (ESPD)",
        "celex": "32016R0007",
        "eli": "reg_impl/2016/7/oj",
    },
    {
        "doc_id": "dir_89_665",
        "title": "Directive 89/665/EEC on review procedures (Remedies Directive), consolidated version of 17.04.2014",
        "celex": "01989L0665-20140417",
        "eli": "dir/1989/665/2014-04-17",
    },
    {
        "doc_id": "reg_2025_2152",
        "title": "Delegated Regulation (EU) 2025/2152, procurement thresholds for 2026-2027",
        "celex": "32025R2152",
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


def main() -> None:
    sections = load_corpus_sections(verbose=True)
    print("\nWords in the corpus that will be indexed:")
    print_word_table(sections)
    print(f"\nSource and licence: {CREDIT} (reuse under Commission Decision 2011/833/EU).")
    print("Embedding and indexing are not built yet (next step).")


if __name__ == "__main__":
    main()
