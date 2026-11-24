"""
Assignment 3: build the index (`uv run python main.py index`).

Corpus: four EU railway acts (original Official Journal text, English), fetched
from the Publications Office "Cellar" endpoint into corpus/ (git-ignored).

Pipeline per file:  extract + clean  ->  chunk (two designs)  ->  embed  ->  ChromaDB

Two chunking designs, one ChromaDB collection each, both in index/:
  fixed    ~200-word windows with 30 words of overlap over the cleaned text.
  article  one chunk per Article / Annex section; anything over 400 words is
           split at paragraph boundaries and every piece keeps the title.

Environment variables:
  DESIGN=fixed|article|all   which design(s) to chunk and embed (default all)
  LIMIT=N                    embed at most N chunks in this run (0 = none)
  PRUNE=1                    delete stored vectors whose chunk no longer exists

server.py imports chunk_file, embed_and_store, get_collection and embed_query.
Nothing here prints to stdout except main(): the MCP server needs stdout clean.
"""

from __future__ import annotations

import datetime
import hashlib
import json
import math
import os
import re
import sys
import time
import unicodedata
from collections import Counter, defaultdict
from itertools import groupby
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
EXTRA_DIR = ROOT / "corpus_extra"  # documents for add_document; git-ignored, never embedded by main.py index
INDEX_DIR = ROOT / "index"
SOURCES_FILE = CORPUS_DIR / "sources.json"
QUERY_CACHE_FILE = INDEX_DIR / "query_cache.json"
PROBLEMS_FILE = INDEX_DIR / "extraction_problems.md"

DOCS = [
    {
        "celex": "32016L0797",
        "doc_id": "Dir_2016_797",
        "doc_title": "Directive (EU) 2016/797 on the interoperability of the rail system within the European Union (recast)",
    },
    {
        "celex": "32016L0798",
        "doc_id": "Dir_2016_798",
        "doc_title": "Directive (EU) 2016/798 on railway safety (recast)",
    },
    {
        "celex": "32014R1299",
        "doc_id": "Reg_1299_2014",
        "doc_title": "Commission Regulation (EU) No 1299/2014, TSI for the 'infrastructure' subsystem (TSI INF)",
    },
    {
        "celex": "32019R0779",
        "doc_id": "Reg_2019_779",
        "doc_title": "Commission Implementing Regulation (EU) 2019/779 on certification of entities in charge of maintenance (ECM)",
    },
]
CELLAR_URL = "https://publications.europa.eu/resource/celex/{celex}"
EURLEX_URL = "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:{celex}"

DESIGNS = ("fixed", "article")
EMBED_ORDER = ("article", "fixed")  # the server's default design gets its vectors first
FIXED_WORDS, FIXED_OVERLAP, FIXED_MIN_TAIL = 200, 30, 80
ARTICLE_MAX_WORDS = 400
MIN_TOTAL_WORDS = 50_000

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768  # the model's default is 3072; 768 keeps the committed index small
EMBED_BATCH = 20
QUERY_TASK = "search result"


def log(*args) -> None:
    """Progress goes to stderr, so importing this from the MCP server is safe."""
    print(*args, file=sys.stderr, flush=True)


def n_words(text: str) -> int:
    return len(text.split())


# ----------------------------------------------------------------------------
# Extraction problems log
# ----------------------------------------------------------------------------

PROBLEM_TEXT = {
    "oj_page_header_removed": ("fixed", "Official Journal page header table (date, 'EN', 'Official Journal of the European Union', page number) removed"),
    "toc_rows_removed": ("fixed", "table-of-contents rows removed (they repeat every section heading plus a page number and would match any query about a heading)"),
    "footnote_markers_removed": ("fixed", "footnote markers '(1)' in running text removed, with the stray space they leave before punctuation"),
    "footnotes_bibliographic_dropped": ("fixed", "footnotes that are only Official Journal references dropped (they sit at the end of the act, far from their anchor)"),
    "footnotes_substantive_attached": ("fixed", "substantive footnotes (e.g. table notes) kept: marker rewritten as '[note N]' and the note text placed right after the paragraph or table that cites it"),
    "footnotes_orphan": ("limitation", "substantive footnotes with no marker pointing at them; dropped"),
    "signature_lines_removed": ("fixed", "signature block lines ('For the Council', 'The President', names) and 'Done at ...' removed"),
    "enacting_formula_removed": ("fixed", "'Whereas:' / 'HAS ADOPTED THIS ...' formula lines removed"),
    "list_items_rejoined": ("fixed", "list items rebuilt: EUR-Lex lays out every '(a) text' item as a two-cell table, which plain text extraction returns as a bare marker followed by an orphaned sentence"),
    "data_tables_linearised": ("fixed", "data tables written one row per line as 'cell | cell | cell'"),
    "span_cells_expanded": ("fixed", "row-spanning / column-spanning cells repeated on every row they cover, so each row is readable alone"),
    "table_notes_rows_removed": ("fixed", "table-note rows taken out of the table body (their text is attached as notes instead)"),
    "figures_not_extracted": ("limitation", "figures / forms that are images: the drawing is lost, replaced by an '[image not extracted]' placeholder"),
    "image_text_kept": ("fixed", "of those images, the ones with a hidden 'Text of image' transcription in the HTML: transcription kept and labelled '[text shown in the image:]'"),
    "formulas_not_extracted": ("limitation", "formulas that exist only as images: replaced by a '[formula not extracted]' placeholder, content lost"),
    "sub_superscripts_fixed": ("fixed", "sub/superscripts kept distinct ('b_qlim', 'm^2') instead of being flattened to 'b qlim', 'm 2'"),
    "nbsp_normalised": ("fixed", "non-breaking spaces normalised to plain spaces (e.g. '1.   Each vehicle')"),
    "thousands_separators_kept": ("note", "numbers written with a space as thousands separator ('1 435 mm') kept as printed; they count as two words"),
    "soft_hyphens_removed": ("fixed", "soft hyphens removed"),
    "hyphenated_linebreaks_joined": ("fixed", "words hyphenated across a line break rejoined (PDF/plain-text path only)"),
    "repeated_page_lines_removed": ("fixed", "running headers/footers repeated on most pages removed, up to three lines at each page edge, e.g. 'BOLETÍN OFICIAL DEL ESTADO / LEGISLACIÓN CONSOLIDADA / Página N' (PDF path only)"),
    "pdf_spanish_headings_found": ("fixed", "Spanish headings recognised in the PDF path ('Artículo N.', 'Disposición adicional ...', 'ANEXO I'): before, only English 'Article N' was, so a Spanish law was chunked by page and a chunk lost its article title"),
    "pdf_toc_lines_removed": ("fixed", "table-of-contents lines with dot leaders ('TÍTULO I. ... ...... 6') removed (PDF path only)"),
    "heading_only_sections": ("note", "sections that are only a heading (parents of sub-sections): no chunk of their own, the heading is kept in the title of their children"),
    "oversize_blocks_split": ("fixed", "single paragraphs over 400 words split at sentence boundaries"),
}


class Problems:
    """Counts of extraction problems per document, with a couple of examples each."""

    def __init__(self) -> None:
        self.counts: dict[str, Counter] = defaultdict(Counter)
        self.examples: dict[str, list[str]] = defaultdict(list)

    def add(self, doc_id: str, key: str, n: int = 1, example: str | None = None) -> None:
        if n:
            self.counts[doc_id][key] += n
        if example and len(self.examples[key]) < 3 and example not in self.examples[key]:
            self.examples[key].append(example)

    def to_markdown(self) -> str:
        doc_ids = list(self.counts)
        lines = [
            "# Extraction problems log",
            "",
            f"Written by index.py on {datetime.date.today().isoformat()}. Counts are per document.",
            "",
            "| Problem | Status | " + " | ".join(doc_ids) + " |",
            "|---|---|" + "---|" * len(doc_ids),
        ]
        for key, (status, text) in PROBLEM_TEXT.items():
            row = [self.counts[d].get(key, 0) for d in doc_ids]
            if any(row):
                lines.append(f"| {text} | {status} | " + " | ".join(str(v) for v in row) + " |")
        shown = [(k, v) for k, v in self.examples.items() if v]
        if shown:
            lines += ["", "## Examples", ""]
            for key, examples in shown:
                lines.append(f"- **{key}**: " + " ;; ".join(f"`{e}`" for e in examples))
        return "\n".join(lines) + "\n"


# ----------------------------------------------------------------------------
# Download
# ----------------------------------------------------------------------------

def _read_sources() -> dict:
    if SOURCES_FILE.is_file():
        try:
            return json.loads(SOURCES_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return {}
    return {}


def _looks_like_html(response) -> bool:
    return response.status_code == 200 and "html" in response.headers.get("content-type", "") and len(response.content) > 10_000


def _download_from_cellar(celex: str) -> tuple[bytes, dict] | None:
    """Fetch the English (X)HTML of one act from the Publications Office. None if it fails."""
    import httpx

    url = CELLAR_URL.format(celex=celex)
    with httpx.Client(follow_redirects=True, timeout=120) as client:
        for accept in ("application/xhtml+xml", "text/html"):
            headers = {"Accept": accept, "Accept-Language": "eng"}
            try:
                response = client.get(url, headers=headers)
                if response.status_code == 300:
                    # Multiple Choices: the body lists the manifestations. English is expression 0006.
                    links = re.findall(r'href="([^"]+)"', response.text) + re.findall(r"<([^>]+)>", response.headers.get("link", ""))
                    links.sort(key=lambda link: (".0006." not in link, "xhtml" not in link.lower()))
                    for link in links[:6]:
                        candidate = client.get(str(response.url.join(link)), headers=headers)
                        if _looks_like_html(candidate):
                            response = candidate
                            break
                if _looks_like_html(response):
                    return response.content, {
                        "source_url": url,
                        "resolved_url": str(response.url),
                        "content_type": response.headers.get("content-type", ""),
                        "bytes": len(response.content),
                        "retrieved": datetime.date.today().isoformat(),
                        "via": "cellar",
                    }
                log(f"  {celex}: Accept {accept} -> HTTP {response.status_code}, {response.headers.get('content-type')}, {len(response.content)} bytes")
            except httpx.HTTPError as error:
                log(f"  {celex}: Accept {accept} -> {type(error).__name__}: {error}")
    return None


def ensure_corpus() -> dict[str, Path]:
    """Make sure corpus/<CELEX>.html exists for every document. Returns {celex: path}.

    A file already in corpus/ is used as it is. Otherwise it is downloaded from
    Cellar. If that fails, say which page to save by hand and exit cleanly.
    """
    CORPUS_DIR.mkdir(exist_ok=True)
    sources = _read_sources()
    paths, missing = {}, []
    for doc in DOCS:
        celex = doc["celex"]
        path = CORPUS_DIR / f"{celex}.html"
        if path.is_file() and path.stat().st_size > 10_000:
            if celex not in sources:  # put there by hand
                sources[celex] = {"source_url": EURLEX_URL.format(celex=celex), "via": "manual save"}
        else:
            log(f"Downloading {celex} from Cellar ...")
            result = _download_from_cellar(celex)
            if result is None:
                missing.append(doc)
                continue
            path.write_bytes(result[0])
            sources[celex] = result[1]
        paths[celex] = path
    SOURCES_FILE.write_text(json.dumps(sources, indent=2), encoding="utf-8")
    if missing:
        print("Could not download these documents. Save each page from your browser as the file shown, then rerun:")
        for doc in missing:
            print(f"  corpus/{doc['celex']}.html  <-  {EURLEX_URL.format(celex=doc['celex'])}")
        sys.exit(0)
    return paths


# ----------------------------------------------------------------------------
# Extraction and cleaning: EUR-Lex / Official Journal HTML
# ----------------------------------------------------------------------------

PAGE_HEADER_CLASSES = {"oj-hd-date", "oj-hd-lg", "oj-hd-ti", "oj-hd-oj"}
BLOCK_TAGS = {"p", "div", "table", "tbody", "tr", "td", "th", "li", "ul", "ol", "figure"}
NUMBERED_HEADING = re.compile(r"^(\d+(?:\.\d+)*\.(?:bis)?)\s+\S")
ROMAN_HEADING = re.compile(r"^([IVX]+)\.\s+\S")
PART_HEADING = re.compile(r"^PART ([A-Z0-9]+)$")
ANNEX_TITLE = re.compile(r"^ANNEX(?: ([IVXLC]+|\d+))?$")
APPENDIX_TITLE = re.compile(r"^Appendix(?: (\S+))?$")
BIBLIOGRAPHIC_NOTE = re.compile(r"\bOJ\s+[LC]\s*\d|Official Journal")
POINT_MARKER = re.compile(r"\((\d+|[a-z]{1,3})\)|(\d+(?:\.\d+)*)\.?")
REMOVED_MARK = "\x00"


def _classes(tag) -> set[str]:
    return set(tag.get("class") or [])


class _OJParser:
    """Turns one Official Journal HTML act into a flat list of text blocks.

    Every block knows its section ("Article 14", "Annex, 4.2.4.2"), the heading
    trail of that section, and its paragraph or point number when it has one.
    """

    def __init__(self, raw: bytes, doc_id: str, problems: Problems) -> None:
        from bs4 import BeautifulSoup

        self.soup = BeautifulSoup(raw, "html.parser")
        self.doc_id = doc_id
        self.problems = problems
        self.blocks: list[dict] = []
        self.title_parts: list[str] = []
        # where we are
        self.part_kind = "front"
        self.part_label = "Preamble"
        self.part_title = ""
        self.annex_label = "Annex"
        self.chapter = ["", ""]
        self.stack: list[tuple[int, str, str]] = []  # (level, label, heading text)
        self.para: str | None = None
        self.para_from_div = False
        self.expect_title = False
        self.in_toc = False
        self.in_final = False
        self.pending_marker = ""
        self.depth = 0
        self.cur_notes: list[str] = []
        self.table_seq = 0
        self.notes: dict[str, tuple[str, str, bool]] = {}
        self.notes_used: set[str] = set()

    def count(self, key: str, n: int = 1, example: str | None = None) -> None:
        self.problems.add(self.doc_id, key, n, example)

    # ---- text of one element -------------------------------------------------

    def inline(self, node) -> str:
        from bs4 import Comment, NavigableString

        out = []
        for child in node.children:
            if isinstance(child, Comment):
                continue
            if isinstance(child, NavigableString):
                out.append(str(child))
                continue
            classes = _classes(child)
            if child.name == "a" and (child.get("href") or "").startswith("#ntr"):
                out.append(self.note_marker(child))
            elif child.name == "span" and "oj-sub" in classes:
                inner = self.inline(child).strip()
                out.append("_" + inner)
                self.count("sub_superscripts_fixed", example=f"subscript {inner!r} -> '_{inner}'")
            elif child.name == "span" and "oj-super" in classes:
                inner = self.inline(child).strip()
                out.append("^" + inner)
                self.count("sub_superscripts_fixed", example=f"superscript {inner!r} -> '^{inner}'")
            elif child.name == "img":
                if "oj-formula" in classes:
                    out.append(" [formula not extracted: image in the source] ")
                    self.count("formulas_not_extracted")
                else:
                    out.append(" [image not extracted] ")
                    self.count("figures_not_extracted")
            elif child.name == "br":
                out.append(" ")
            elif child.name in BLOCK_TAGS:
                out.append(" " + self.inline(child) + " ")
            else:
                out.append(self.inline(child))
        return "".join(out)

    def note_marker(self, anchor) -> str:
        key = (anchor.get("href") or "")[1:]
        note = self.notes.get(key)
        if note is None or note[2]:
            self.count("footnote_markers_removed")
            return REMOVED_MARK
        self.notes_used.add(key)
        self.cur_notes.append(key)
        return f" [note {note[0]}]"

    def clean(self, text: str) -> str:
        text = unicodedata.normalize("NFC", text)
        soft = text.count("­")
        if soft:
            self.count("soft_hyphens_removed", soft)
            text = text.replace("­", "")
        nbsp = len(re.findall(r"[    ]", text))
        if nbsp:
            thousands = re.findall(r"\d \d{3}(?!\d)", text)
            self.count("nbsp_normalised", nbsp)
            if thousands:
                self.count("thousands_separators_kept", len(thousands))
            text = re.sub(r"[    ]", " ", text)
        text = re.sub(r"[​‌‍﻿]", "", text)
        text = re.sub(r"\s*" + REMOVED_MARK + r"\s*(?=[,.;:)])", "", text)
        text = re.sub(r"\s*" + REMOVED_MARK + r"\s*", " ", text)
        return re.sub(r"\s+", " ", text).strip()

    # ---- where a block belongs -----------------------------------------------

    def section(self) -> str:
        if self.part_kind != "annex":
            return self.part_label
        labels = [label for level, label, _ in self.stack if level == 0]
        numeric = [label for level, label, _ in self.stack if level > 0]
        return ", ".join([self.part_label] + labels + numeric[-1:])

    def heading(self) -> str:
        if self.part_kind == "article":
            chapter = ": ".join(part for part in self.chapter if part)
            article = self.part_label + (f": {self.part_title}" if self.part_title else "")
            return f"{chapter} > {article}" if chapter else article
        if self.part_kind == "annex":
            trail = [self.part_label + (f": {self.part_title}" if self.part_title else "")]
            return " > ".join(trail + [text for _, _, text in self.stack])
        return self.part_label

    def emit(self, text: str, kind: str = "text", **extra) -> None:
        if not text:
            return
        if self.pending_marker and kind == "text":
            text = f"{self.pending_marker} {text}"
            self.pending_marker = ""
            self.count("list_items_rejoined")
        if kind != "heading":
            self.expect_title = False
        self.blocks.append({
            "text": text,
            "kind": kind,
            "words": n_words(text),
            "section": self.section(),
            "heading": self.heading(),
            "para": self.para,
            "notes": self.cur_notes,
            **extra,
        })
        self.cur_notes = []

    def new_part(self, kind: str, label: str, title: str = "") -> None:
        self.part_kind, self.part_label, self.part_title = kind, label, title
        self.stack, self.para, self.para_from_div = [], None, False
        self.in_toc, self.in_final, self.pending_marker = False, False, ""
        self.expect_title = kind == "annex"

    # ---- walking the document --------------------------------------------------

    def parse(self) -> list[dict]:
        self.collect_notes()
        self.walk(self.soup.body or self.soup, 0)
        orphans = [key for key, note in self.notes.items() if not note[2] and key not in self.notes_used]
        self.count("footnotes_orphan", len(orphans))
        return self.attach_notes()

    def collect_notes(self) -> None:
        for p in self.soup.find_all("p", class_="oj-note"):
            anchor = p.find("a", id=re.compile(r"^ntr"))
            if anchor is None:
                continue
            label = re.sub(r"[()\s]", "", anchor.get_text())
            key = anchor["id"]
            anchor.extract()
            text = self.clean(self.inline(p))
            bibliographic = not text or bool(BIBLIOGRAPHIC_NOTE.search(text))
            self.notes[key] = (label, text, bibliographic)
            self.count("footnotes_bibliographic_dropped" if bibliographic else "footnotes_substantive_attached")
        self.cur_notes = []

    def attach_notes(self) -> list[dict]:
        """Put each cited substantive note right after the paragraph or table that cites it."""
        out: list[dict] = []
        for _, run in groupby(self.blocks, key=lambda block: block["section"]):
            run = list(run)
            placed, queue = set(), []
            for i, block in enumerate(run):
                out.append(block)
                for key in block["notes"]:
                    if key not in placed:
                        placed.add(key)
                        queue.append(key)
                in_table = block["kind"] == "row" and i + 1 < len(run) and run[i + 1].get("table") == block.get("table")
                if in_table:
                    continue
                for key in queue:
                    label, text, _ = self.notes[key]
                    text = f"Note {label}: {text}"
                    out.append({
                        "text": text, "kind": "note", "words": n_words(text), "section": block["section"],
                        "heading": block["heading"], "para": block["para"], "notes": [],
                    })
                queue = []
        return out

    def walk(self, node, depth: int) -> None:
        from bs4 import Comment, NavigableString

        for child in node.children:
            if isinstance(child, Comment):
                continue
            if isinstance(child, NavigableString):
                self.emit(self.clean(str(child)))
                continue
            name, classes = child.name, _classes(child)
            self.depth = depth
            if name in ("hr", "col", "head", "script", "style"):
                continue
            if name == "a" and (child.get("id") or "").startswith("textofimagelink"):
                self.count("image_text_kept")
                self.emit("[text shown in the image:]")
            elif name == "table":
                if child.find("p", class_=list(PAGE_HEADER_CLASSES)):
                    self.count("oj_page_header_removed")
                elif self.in_toc:
                    self.count("toc_rows_removed", len(child.find_all("tr")))
                elif "oj-table" in classes:
                    self.data_table(child)
                else:
                    self.layout_table(child, depth)
            elif name == "div":
                self.div(child, classes, depth)
            elif name == "p":
                self.paragraph(child, classes)
            elif name in ("tbody", "tr", "td", "th", "figure", "ul", "ol", "li", "body"):
                if name == "figure" or child.find("img"):
                    self.emit(self.clean(self.inline(child)))
                else:
                    self.walk(child, depth)
            else:
                self.emit(self.clean(self.inline(child)))

    def div(self, div, classes: set[str], depth: int) -> None:
        div_id = div.get("id") or ""
        if "oj-signatory" in classes:
            self.count("signature_lines_removed", len(div.find_all("p")))
            return
        if re.fullmatch(r"rct_\d+", div_id):
            saved = (self.part_kind, self.part_label)
            self.part_kind, self.part_label, self.para = "recitals", "Recitals", div_id.split("_")[1]
            self.walk(div, depth)
            (self.part_kind, self.part_label), self.para = saved, None
            return
        if re.fullmatch(r"\d{3}\.\d{3}", div_id):
            self.para, self.para_from_div = str(int(div_id.split(".")[1])), True
        if div_id == "pbl_1" and self.part_kind == "front":
            self.part_kind = "preamble"
        if div_id.startswith("fnp_"):
            self.in_final = True
        self.walk(div, depth)

    def paragraph(self, p, classes: set[str]) -> None:
        if classes & PAGE_HEADER_CLASSES or "oj-note" in classes:
            return
        if "oj-signatory" in classes:
            self.count("signature_lines_removed")
            return
        text = self.clean(self.inline(p))
        if not text:
            self.cur_notes = []
            return

        if "oj-doc-ti" in classes:
            annex, appendix = ANNEX_TITLE.match(text), APPENDIX_TITLE.match(text)
            if annex:
                self.annex_label = f"Annex {annex.group(1)}" if annex.group(1) else "Annex"
                self.new_part("annex", self.annex_label)
            elif appendix:
                self.new_part("annex", f"{self.annex_label}, Appendix" + (f" {appendix.group(1)}" if appendix.group(1) else ""))
            elif text.startswith("Statement by the Commission"):
                self.new_part("statement", "Commission statement")
                self.emit(text)
                return
            elif self.part_kind == "annex" and self.expect_title:
                self.part_title = f"{self.part_title} {text}".strip()
            elif self.part_kind == "front":
                self.title_parts.append(text)
                self.emit(text)
                return
            self.emit(text, "heading")
        elif "oj-ti-section-1" in classes:
            self.chapter = [text[:1] + text[1:].lower().replace(text.split()[-1].lower(), text.split()[-1]) if text.isupper() else text, ""]
            self.emit(text, "heading")
        elif "oj-ti-section-2" in classes:
            self.chapter[1] = text.capitalize() if text.isupper() else text
            self.emit(text, "heading")
        elif "oj-ti-art" in classes:
            self.new_part("article", text)
            self.emit(text, "heading")
        elif "oj-sti-art" in classes:
            self.part_title = text
            self.emit(text, "heading")
        elif "oj-ti-grseq-1" in classes:
            self.in_toc = False
            self.section_heading(text)
        elif "oj-ti-tbl" in classes:
            if text.upper() == "TABLE OF CONTENTS":
                self.in_toc = True
            elif self.blocks and self.blocks[-1]["kind"] == "caption":
                last = self.blocks[-1]
                last["text"] = f"{last['text']} - {text}"
                last["words"] = n_words(last["text"])
            else:
                self.emit(text, "caption")
        elif self.in_final and text.startswith("Done at"):
            self.count("signature_lines_removed")
        elif text == "Whereas:" or re.fullmatch(r"(HAS|HAVE) ADOPTED THIS (DIRECTIVE|REGULATION|DECISION):", text):
            self.count("enacting_formula_removed")
        else:
            numbered = re.match(r"(\d+(?:\.\d+)*)\.\s", text)  # "2. The organisation shall ..." written as plain text
            if numbered and self.depth == 0 and not self.pending_marker and not self.para_from_div and self.part_kind in ("annex", "article"):
                self.para = numbered.group(1)
            self.emit(text)

    def section_heading(self, text: str) -> None:
        numbered, roman, part = NUMBERED_HEADING.match(text), ROMAN_HEADING.match(text), PART_HEADING.match(text)
        if numbered:
            label = numbered.group(1).rstrip(".")
            level = len(re.findall(r"\d+", label))
        elif roman:
            label, level = roman.group(1), 0
        elif part:
            label, level = f"Part {part.group(1)}", 0
        elif self.part_kind == "annex" and self.expect_title and not self.stack:
            self.part_title = f"{self.part_title} {text}".strip()  # an unnumbered line under "ANNEX I" is its title
            self.emit(text, "heading")
            return
        else:
            self.emit(text)  # "P cases", "Figure 1": a label inside the current section
            return
        while self.stack and self.stack[-1][0] >= level:
            self.stack.pop()
        self.stack.append((level, label, text))
        self.para, self.para_from_div, self.expect_title = None, False, False
        self.emit(text, "heading")

    def layout_table(self, table, depth: int) -> None:
        """EUR-Lex writes each list item as a table row: [marker cell][content cell]."""
        for tr in table.find_all("tr"):
            if tr.find_parent("table") is not table:
                continue
            cells = [td for td in tr.find_all(["td", "th"]) if td.find_parent("tr") is tr]
            marker = self.clean(self.inline(cells[0])) if len(cells) == 2 else ""
            if marker and len(marker) <= 12:
                point = POINT_MARKER.fullmatch(marker)
                if depth == 0 and point and not self.para_from_div and self.part_kind in ("annex", "article"):
                    label = point.group(1) or point.group(2)
                    # "(a)" only names the point when no numbered point is open above it
                    if not label.isalpha() or self.para is None or self.para.isalpha():
                        self.para = label
                self.pending_marker = f"{self.pending_marker} {marker}".strip()
                self.walk(cells[1], depth + 1)
                self.pending_marker = ""
            else:
                for cell in cells:
                    self.walk(cell, depth + 1)

    def data_table(self, table) -> None:
        self.table_seq += 1
        self.count("data_tables_linearised")
        caption = self.blocks[-1]["text"] if self.blocks and self.blocks[-1]["kind"] == "caption" else ""
        carry: dict[int, list] = {}
        rows: list[tuple[str, bool, list[str]]] = []
        for tr in table.find_all("tr"):
            if tr.find_parent("table") is not table:
                continue
            if "oj-tblnote" in _classes(tr) or tr.find("p", class_="oj-note"):
                self.count("table_notes_rows_removed")
                continue
            tds = iter([td for td in tr.find_all(["td", "th"]) if td.find_parent("tr") is tr])
            cells, header_flags, col = [], [], 0
            td = next(tds, None)
            while td is not None or col in carry:
                if col in carry:
                    cells.append(carry[col][1])
                    carry[col][0] -= 1
                    if carry[col][0] <= 0:
                        del carry[col]
                    col += 1
                    continue
                text = self.clean(self.inline(td))
                paragraphs = [p for p in td.find_all("p") if p.get_text(strip=True)]
                if text:
                    header_flags.append(bool(paragraphs) and all("oj-tbl-hdr" in _classes(p) for p in paragraphs))
                try:
                    rowspan, colspan = int(td.get("rowspan") or 1), int(td.get("colspan") or 1)
                except ValueError:
                    rowspan, colspan = 1, 1
                if rowspan > 1 or colspan > 1:
                    self.count("span_cells_expanded")
                for offset in range(colspan):
                    cells.append(text if offset == 0 else "")
                    if rowspan > 1:
                        carry[col] = [rowspan - 1, text if offset == 0 else ""]
                    col += 1
                td = next(tds, None)
            notes, self.cur_notes = self.cur_notes, []
            if any(cells):
                rows.append((" | ".join(cells).strip(), bool(header_flags) and all(header_flags), notes))
        leading = []
        for text, is_header, _ in rows:
            if not is_header:
                break
            leading.append(text)
        head = "\n".join(([caption] if caption else []) + leading)
        for i, (text, is_header, notes) in enumerate(rows):
            self.cur_notes = notes
            self.emit(text, "row", table=self.table_seq, table_head=head, table_first=i == 0)


# ----------------------------------------------------------------------------
# Extraction and cleaning: PDF, plain text and other HTML (for add_document)
# ----------------------------------------------------------------------------

SPANISH_HEADING = re.compile(r"^(Artículo \d+(?: (?:bis|ter|quater|quinquies))?|Disposición (?:adicional|transitoria|derogatoria|final) [a-záéíóúñ ]+?)\.(?=\s|$)")
TOC_LEADER = re.compile(r"\.{5,}\s*\d*$")
HEADING_MARK = "\x01"


def _isolate_spanish_headings(text: str) -> tuple[str, int]:
    """Give 'Artículo 107.  Infracciones graves.' its own paragraph and mark it as a heading.

    pypdf returns no blank lines, and the title may wrap onto the next line.
    """
    lines, out, found, i = text.split("\n"), [], 0, 0
    while i < len(lines):
        if SPANISH_HEADING.match(lines[i]):
            title, extra = lines[i].strip(), 0
            while not title.endswith(".") and extra < 2 and i + 1 < len(lines):
                i, extra = i + 1, extra + 1
                title = f"{title} {lines[i].strip()}"
            out += ["", HEADING_MARK + title, ""]
            found += 1
        else:
            out.append(lines[i])
        i += 1
    return "\n".join(out), found


def _plain_blocks(pages: list[str], doc_id: str, problems: Problems, paged: bool) -> list[dict]:
    """Blocks from page texts: strip running headers, rejoin hyphenated words, find Articles."""
    page_lines = [[line.strip() for line in page.splitlines()] for page in pages]
    if paged and len(pages) >= 4:
        edge = Counter()
        for lines in page_lines:
            kept = [line for line in lines if line]
            for line in set(kept[:3] + kept[-3:]):
                edge[re.sub(r"\d+", "#", line)] += 1
        repeated = {line for line, n in edge.items() if n >= len(pages) / 2}
        for lines in page_lines:
            before = len(lines)
            lines[:] = [line for line in lines if re.sub(r"\d+", "#", line) not in repeated]
            problems.add(doc_id, "repeated_page_lines_removed", before - len(lines))

    blocks, section = [], None
    for page_no, lines in enumerate(page_lines, 1):
        if paged:
            before = len(lines)
            lines = [line for line in lines if not TOC_LEADER.search(line)]
            problems.add(doc_id, "pdf_toc_lines_removed", before - len(lines))
        text = "\n".join(lines)
        text, joined = re.subn(r"(\w)-\n([a-z])", r"\1\2", text)
        text = re.sub(r"(?m)^(Article \d+[a-z]?|ANNEX(?: [IVXLC]+)?|ANEXO(?: [IVXLC]+)?)$", r"\n\1\n", text)  # headings get their own paragraph
        text, spanish = _isolate_spanish_headings(text)
        problems.add(doc_id, "pdf_spanish_headings_found", spanish)
        problems.add(doc_id, "hyphenated_linebreaks_joined", joined)
        soft = text.count("­")
        problems.add(doc_id, "soft_hyphens_removed", soft)
        text = text.replace("­", "")
        for paragraph in re.split(r"\n\s*\n", text):
            paragraph = re.sub(r"\s+", " ", unicodedata.normalize("NFC", paragraph)).strip()
            if not paragraph:
                continue
            article = re.match(r"^(Article \d+[a-z]?|ANNEX(?: [IVXLC]+)?|ANEXO(?: [IVXLC]+)?)\b", paragraph)
            is_heading = bool(article) and n_words(paragraph) <= 12
            if is_heading:
                section = article.group(1).replace("ANNEX", "Annex").replace("ANEXO", "Anexo")
            if paragraph.startswith(HEADING_MARK):  # "Artículo 107. Infracciones graves." -> section "Artículo 107"
                paragraph = paragraph[len(HEADING_MARK):]
                is_heading, section = True, paragraph.split(".")[0]
            here = section or (f"p. {page_no}" if paged else "Text")
            blocks.append({
                "text": paragraph, "kind": "heading" if is_heading else "text", "words": n_words(paragraph),
                "section": here, "heading": paragraph if is_heading else here,
                "para": None if section or not paged else None, "notes": [],
            })
    # the heading text of a section is the heading block that opened it
    current = {}
    for block in blocks:
        if block["kind"] == "heading":
            current[block["section"]] = block["text"]
        block["heading"] = current.get(block["section"], block["section"])
    return blocks


def file_hash(path: str | Path) -> str:
    """sha256 of the file's bytes: identifies one exact version of a document."""
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def _doc_info(path: Path) -> dict:
    """Metadata shared by every chunk of a file: the four corpus acts are known, others are derived."""
    stem = path.stem
    sources = _read_sources()
    doc_hash = file_hash(path)
    for doc in DOCS:
        if doc["celex"] == stem:
            source = sources.get(stem, {}).get("source_url") or CELLAR_URL.format(celex=stem)
            return {**doc, "source_url": source, "doc_hash": doc_hash}
    celex = stem if re.fullmatch(r"[0-9EC]\d{4}[A-Z]{1,2}\d{4}(\(\d+\))?", stem) else ""
    try:  # a file without a known URL is cited by its path inside the project, or by its name alone
        local = path.resolve().relative_to(ROOT).as_posix()
    except ValueError:
        local = path.name
    source = sources.get(stem, {}).get("source_url") or (CELLAR_URL.format(celex=celex) if celex else local)
    doc_id = re.sub(r"[^A-Za-z0-9_]+", "_", stem).strip("_") or "document"
    if not doc_id[0].isalpha():  # citations are written [doc_id, location]; keep doc_id an identifier
        doc_id = f"doc_{doc_id}"
    return {"celex": celex, "doc_id": doc_id, "doc_title": "", "source_url": source, "doc_hash": doc_hash}


_EXTRACT_CACHE: dict[tuple, tuple[dict, list[dict]]] = {}


def extract_file(path: str | Path, problems: Problems | None = None) -> tuple[dict, list[dict]]:
    """Extract and clean one file. Returns (document info, list of text blocks)."""
    path = Path(path)
    key = (str(path.resolve()), path.stat().st_mtime_ns)
    if key in _EXTRACT_CACHE:
        return _EXTRACT_CACHE[key]
    problems = problems if problems is not None else Problems()
    info = _doc_info(path)
    suffix = path.suffix.lower()
    title = ""
    if suffix == ".pdf":
        from pypdf import PdfReader

        reader = PdfReader(str(path))
        pages = [page.extract_text() or "" for page in reader.pages]
        title = (reader.metadata.title if reader.metadata else "") or ""
        blocks = _plain_blocks(pages, info["doc_id"], problems, paged=True)
    elif suffix in (".html", ".htm", ".xhtml", ".xml"):
        raw = path.read_bytes()
        if b"oj-normal" in raw or b"oj-doc-ti" in raw:
            parser = _OJParser(raw, info["doc_id"], problems)
            blocks = parser.parse()
            title = " ".join(parser.title_parts)
        else:
            from bs4 import BeautifulSoup

            soup = BeautifulSoup(raw, "html.parser")
            for tag in soup(["script", "style", "nav", "header", "footer"]):
                tag.decompose()
            title = soup.title.get_text(strip=True) if soup.title else ""
            blocks = _plain_blocks([soup.get_text("\n\n")], info["doc_id"], problems, paged=False)
    else:
        blocks = _plain_blocks([path.read_text(encoding="utf-8", errors="replace")], info["doc_id"], problems, paged=False)
    if not info["doc_title"]:
        first = blocks[0]["text"] if blocks else ""
        info["doc_title"] = (title or first or path.stem)[:200]
    _EXTRACT_CACHE[key] = (info, blocks)
    return info, blocks


# ----------------------------------------------------------------------------
# Chunking
# ----------------------------------------------------------------------------

def _loc(section: str, paras: list) -> str:
    """'Article 14', 'Article 14(2)', 'Article 14(2)-(4)', 'Recitals 3-7'."""
    unique = []
    for para in paras:
        if para and para not in unique:
            unique.append(para)
    if section == "Recitals":
        if not unique:
            return "Recitals"
        return f"Recital {unique[0]}" if len(unique) == 1 else f"Recitals {unique[0]}-{unique[-1]}"
    if not unique:
        return section
    first, last = unique[0], unique[-1]
    if "." in first:  # "1.2" under section "Annex I, 1" is written "Annex I, 1.2"
        head, _, tail = section.rpartition(", ")
        start = f"{head}, {first}" if head and first.startswith(tail + ".") else f"{section}, {first}"
    else:
        start = f"{section}({first})"
    if len(unique) == 1:
        return start
    return f"{start}-{last}" if "." in last else f"{start}-({last})"


def _make_chunk(info: dict, design: str, seq: int, location: str, sections: list[str], text: str, embed_text: str, seen: set) -> dict:
    digest = hashlib.sha1(embed_text.encode("utf-8")).hexdigest()[:12]
    chunk_id, n = f"{info['doc_id']}:{design}:{digest}", 1
    while chunk_id in seen:
        n += 1
        chunk_id = f"{info['doc_id']}:{design}:{digest}-{n}"
    seen.add(chunk_id)
    return {
        "id": chunk_id,
        "text": text,
        "embed_text": embed_text,
        "metadata": {
            "doc_id": info["doc_id"],
            "doc_title": info["doc_title"],
            "celex": info["celex"],
            "location": location,
            "design": design,
            "chunk_id": chunk_id,
            "word_count": n_words(text),
            "source_url": info["source_url"],
            "doc_hash": info["doc_hash"],
            "sections": "; ".join(sections),
            "seq": seq,
        },
    }


def _chunk_fixed(info: dict, blocks: list[dict]) -> list[dict]:
    """Windows of FIXED_WORDS words, FIXED_OVERLAP shared with the previous one. Ignores structure."""
    words, owner = [], []
    for i, block in enumerate(blocks):
        block_words = block["text"].split()
        words += block_words
        owner += [i] * len(block_words)
    if not words:
        return []
    step = FIXED_WORDS - FIXED_OVERLAP
    spans = [(start, min(start + FIXED_WORDS, len(words))) for start in range(0, max(len(words) - FIXED_OVERLAP, 1), step)]
    if len(spans) > 1 and spans[-1][1] - spans[-1][0] < FIXED_MIN_TAIL:
        spans[-2] = (spans[-2][0], spans[-1][1])
        spans.pop()

    chunks, seen = [], set()
    for seq, (start, end) in enumerate(spans):
        parts, sections = [], []
        for i in range(start, end):
            parts.append(("\n" if i > start and owner[i] != owner[i - 1] else " " if i > start else "") + words[i])
            section = blocks[owner[i]]["section"]
            if section not in sections:
                sections.append(section)
        text = "".join(parts)
        first, last = blocks[owner[start]], blocks[owner[end - 1]]
        if len(sections) == 1:
            location = _loc(sections[0], [blocks[owner[i]]["para"] for i in range(start, end)])
        else:
            location = f"{_loc(first['section'], [first['para']])} to {_loc(last['section'], [last['para']])}"
        embed_text = f"title: {info['doc_title']} | text: {text}"
        chunks.append(_make_chunk(info, "fixed", seq, location, sections, text, embed_text, seen))
    return chunks


def _pack(units: list[tuple[int, object]], cap: int) -> list[list]:
    """Greedy packing of (words, item) units into pieces of at most `cap` words, evenly sized."""
    total = sum(words for words, _ in units)
    if total <= cap:
        return [[item for _, item in units]]
    target = total / math.ceil(total / cap)
    pieces, current, current_words = [], [], 0
    for words, item in units:
        if current and (current_words + words > cap or current_words >= target):
            pieces.append(current)
            current, current_words = [], 0
        current.append(item)
        current_words += words
    if current:
        pieces.append(current)
    return pieces


def _split_long_block(block: dict, cap: int) -> list[dict]:
    sentences = re.split(r"(?<=[.;])\s+", block["text"])
    units = []
    for sentence in sentences:
        sentence_words = sentence.split()
        for i in range(0, len(sentence_words), cap):  # a "sentence" longer than the cap is cut by words
            piece = " ".join(sentence_words[i:i + cap])
            units.append((n_words(piece), piece))
    out = []
    for group in _pack(units, cap):
        text = " ".join(group)
        out.append({**block, "text": text, "words": n_words(text), "table_first": False if out else block.get("table_first")})
    return out


def _split_section(body: list[dict], doc_id: str, problems: Problems) -> list[tuple[list[str], list[dict]]]:
    """Split one section's blocks into pieces of at most ARTICLE_MAX_WORDS words.

    Numbered paragraphs stay whole when they fit. A paragraph that is itself too
    long is split between its list items, and its lead-in sentence is repeated.
    Returns [(context lines to prepend, blocks)].
    """
    cap = ARTICLE_MAX_WORDS
    if sum(block["words"] for block in body) <= cap:
        return [([], body)]
    units = []
    for _, group in groupby(body, key=lambda block: block["para"]):
        group = list(group)
        group_words = sum(block["words"] for block in group)
        if group_words <= cap:
            units.append((group_words, {"blocks": group, "lead": None}))
            continue
        expanded = []
        for block in group:
            if block["words"] > cap:
                problems.add(doc_id, "oversize_blocks_split")
                expanded += _split_long_block(block, cap)
            else:
                expanded.append(block)
        first = expanded[0]
        lead = first["text"] if first["text"].endswith(":") and first["words"] <= 60 else None
        for i, sub in enumerate(_pack([(block["words"], block) for block in expanded], cap)):
            units.append((sum(block["words"] for block in sub), {"blocks": sub, "lead": lead if i else None}))
    pieces = []
    for packed in _pack(units, cap):
        blocks = [block for unit in packed for block in unit["blocks"]]
        context = []
        if packed[0]["lead"]:
            context.append(f"{packed[0]['lead']} [continued]")
        first = blocks[0]
        if first["kind"] == "row" and first.get("table_head") and not first.get("table_first"):
            context.append(f"{first['table_head']} [table continued]")
        pieces.append((context, blocks))
    return pieces


def _chunk_article(info: dict, blocks: list[dict], problems: Problems) -> list[dict]:
    """One chunk per Article / Annex section, split at paragraph boundaries above 400 words."""
    chunks, seen = [], set()
    for section, run in groupby(blocks, key=lambda block: block["section"]):
        run = list(run)
        body = [block for block in run if block["kind"] != "heading"]
        if not body:
            problems.add(info["doc_id"], "heading_only_sections")
            continue
        title = f"{info['doc_title']} | {run[-1]['heading']}"
        pieces = _split_section(body, info["doc_id"], problems)
        split = len(pieces) > 1
        locations = [_loc(section, [block["para"] for block in piece] if split or section == "Recitals" else []) for _, piece in pieces]
        if len(set(locations)) < len(locations):
            locations = [f"{location} (part {i + 1}/{len(pieces)})" for i, location in enumerate(locations)]
        for (context, piece), location in zip(pieces, locations):
            body_text = "\n".join(context + [block["text"] for block in piece])
            chunks.append(_make_chunk(
                info, "article", len(chunks), location, [section],
                text=f"{title}\n{body_text}",
                embed_text=f"title: {title} | text: {body_text}",
                seen=seen,
            ))
    return chunks


def chunk_file(path: str | Path, design: str = "article", problems: Problems | None = None) -> list[dict]:
    """Extract, clean and chunk one file with the given design ("fixed" or "article").

    Returns a list of {"id", "text", "embed_text", "metadata"}. The metadata holds
    doc_id, doc_title, celex, location, design, chunk_id, word_count, source_url,
    doc_hash (sha256 of the file), sections (every section the chunk touches,
    '; '-separated) and seq.
    """
    if design not in DESIGNS:
        raise ValueError(f"design must be one of {DESIGNS}, not {design!r}")
    problems = problems if problems is not None else Problems()
    info, blocks = extract_file(path, problems)
    return _chunk_fixed(info, blocks) if design == "fixed" else _chunk_article(info, blocks, problems)


# ----------------------------------------------------------------------------
# Embedding and storage
# ----------------------------------------------------------------------------

class QuotaExhausted(RuntimeError):
    """The Gemini API refused with 429 and waiting a little did not help."""


_CLIENT = None
_CHROMA = None


def _genai_client():
    global _CLIENT
    if _CLIENT is None:
        from google import genai

        from api_key import load_api_key

        _CLIENT = genai.Client(api_key=load_api_key())
    return _CLIENT


def get_collection(design: str):
    """The ChromaDB collection of one chunking design ("fixed" or "article"), stored in index/.

    It never embeds anything itself: vectors always come from Gemini via this module.
    """
    global _CHROMA
    if design not in DESIGNS:
        raise ValueError(f"design must be one of {DESIGNS}, not {design!r}")
    if _CHROMA is None:
        import chromadb
        from chromadb.config import Settings

        INDEX_DIR.mkdir(exist_ok=True)
        _CHROMA = chromadb.PersistentClient(path=str(INDEX_DIR), settings=Settings(anonymized_telemetry=False))
    return _CHROMA.get_or_create_collection(name=design, embedding_function=None, metadata={"hnsw:space": "cosine"})


def _embed_once(texts: list[str]) -> list[list[float]]:
    from google.genai import types

    client = _genai_client()
    config = types.EmbedContentConfig(output_dimensionality=EMBED_DIM)
    # gemini-embedding-2 merges a plain list of strings into ONE vector; one Content per text keeps them apart.
    contents = [types.Content(parts=[types.Part.from_text(text=text)]) for text in texts]
    result = client.models.embed_content(model=EMBED_MODEL, contents=contents, config=config)
    vectors = [list(embedding.values) for embedding in result.embeddings]
    if len(vectors) != len(texts):
        raise RuntimeError(f"{EMBED_MODEL} returned {len(vectors)} vectors for {len(texts)} texts; refusing to store them.")
    return vectors


def _embed(texts: list[str]) -> list[list[float]]:
    """Embed texts. Waits out per-minute throttling; raises QuotaExhausted on anything longer."""
    from google.genai import errors

    for attempt in range(4):
        try:
            return _embed_once(texts)
        except errors.APIError as error:
            message = str(error)
            if error.code == 429:
                daily = "PerDay" in message or "per day" in message.lower()
                delay = re.search(r"retry(?:Delay)?['\"]?:?\s*['\"]?(\d+(?:\.\d+)?)s", message) or re.search(r"retry in (\d+(?:\.\d+)?)s", message)
                wait = min(float(delay.group(1)) + 2, 90) if delay else 65
                if daily or attempt == 3:
                    raise QuotaExhausted(message[:400]) from error
                log(f"  429 (rate limit), waiting {wait:.0f}s and retrying ({attempt + 1}/3) ...")
                time.sleep(wait)
            elif error.code in (500, 502, 503, 504) and attempt < 3:
                time.sleep(5 * 2 ** attempt)
            else:
                raise
    raise QuotaExhausted("no answer after retries")


def stored_ids(collection, ids: list[str]) -> set[str]:
    found = set()
    for i in range(0, len(ids), 500):
        found.update(collection.get(ids=ids[i:i + 500], include=[])["ids"])
    return found


def _refresh_metadata(collection, chunks: list[dict]) -> int:
    """Bring the metadata of already-stored chunks up to date. Costs no embedding:
    a chunk id is a hash of its text, so the stored vector is still the right one."""
    changed = 0
    for i in range(0, len(chunks), 500):
        batch = chunks[i:i + 500]
        got = collection.get(ids=[chunk["id"] for chunk in batch], include=["metadatas"])
        stored = dict(zip(got["ids"], got["metadatas"]))
        outdated = [chunk for chunk in batch if stored.get(chunk["id"]) != chunk["metadata"]]
        if outdated:
            collection.update(ids=[chunk["id"] for chunk in outdated], metadatas=[chunk["metadata"] for chunk in outdated])
            changed += len(outdated)
    return changed


def embed_and_store(chunks: list[dict], collection, limit: int | None = None) -> dict:
    """Embed the chunks that have no stored vector yet and save each batch at once.

    `collection` is a ChromaDB collection or a design name. Chunk ids are hashes
    of their content, so a chunk that is already stored is skipped (only its
    metadata is refreshed) and re-adding a document costs nothing. Stops cleanly
    when the quota runs out.
    Returns {"already", "stored", "remaining", "quota_hit"}.
    """
    if isinstance(collection, str):
        collection = get_collection(collection)
    have = stored_ids(collection, [chunk["id"] for chunk in chunks])
    _refresh_metadata(collection, [chunk for chunk in chunks if chunk["id"] in have])
    todo = [chunk for chunk in chunks if chunk["id"] not in have]
    stats = {"already": len(chunks) - len(todo), "stored": 0, "remaining": len(todo), "quota_hit": False, "error": ""}
    if limit is not None:
        todo = todo[:max(limit, 0)]
    for i in range(0, len(todo), EMBED_BATCH):
        batch = todo[i:i + EMBED_BATCH]
        try:
            vectors = _embed([chunk["embed_text"] for chunk in batch])
        except QuotaExhausted as error:
            stats["quota_hit"], stats["error"] = True, str(error)
            log(f"  Quota reached: {error}")
            break
        collection.add(
            ids=[chunk["id"] for chunk in batch],
            embeddings=vectors,
            documents=[chunk["text"] for chunk in batch],
            metadatas=[chunk["metadata"] for chunk in batch],
        )
        stats["stored"] += len(batch)
        stats["remaining"] -= len(batch)
        log(f"  {collection.name}: stored {stats['stored']}/{len(todo)} this run")
    return stats


def embed_query(text: str) -> list[float]:
    """Embedding of a search query, cached in index/query_cache.json so reruns cost no quota."""
    text = text.strip()
    key = hashlib.sha1(f"{EMBED_MODEL}|{EMBED_DIM}|{QUERY_TASK}|{text}".encode("utf-8")).hexdigest()
    cache = {}
    if QUERY_CACHE_FILE.is_file():
        try:
            cache = json.loads(QUERY_CACHE_FILE.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            cache = {}
    if key in cache:
        return cache[key]["vector"]
    vector = [round(value, 6) for value in _embed([f"task: {QUERY_TASK} | query: {text}"])[0]]
    cache[key] = {"query": text, "vector": vector}
    INDEX_DIR.mkdir(exist_ok=True)
    temporary = QUERY_CACHE_FILE.with_suffix(".tmp")
    temporary.write_text(json.dumps(cache), encoding="utf-8")
    temporary.replace(QUERY_CACHE_FILE)
    return vector


# ----------------------------------------------------------------------------
# main.py index
# ----------------------------------------------------------------------------

def main() -> None:
    choice = os.environ.get("DESIGN", "all").strip().lower() or "all"
    if choice not in (*DESIGNS, "all"):
        raise SystemExit(f"DESIGN must be fixed, article or all, not {choice!r}")
    designs = list(DESIGNS) if choice == "all" else [choice]
    limit_text = os.environ.get("LIMIT", "").strip()
    limit = int(limit_text) if limit_text else None

    paths = ensure_corpus()
    sources = _read_sources()
    problems = Problems()

    print("\n== Corpus ==")
    total_words = 0
    for doc in DOCS:
        _, blocks = extract_file(paths[doc["celex"]], problems)
        words = sum(block["words"] for block in blocks)
        total_words += words
        print(f"  {doc['doc_id']:<14} {words:>7,} words   {sources.get(doc['celex'], {}).get('source_url', '')}")
    verdict = "OK" if total_words >= MIN_TOTAL_WORDS else "TOO SMALL"
    print(f"  {'TOTAL':<14} {total_words:>7,} words   (minimum {MIN_TOTAL_WORDS:,}: {verdict})")

    print("\n== Chunks ==")
    chunks = {design: [] for design in designs}
    for design in designs:
        per_doc = []
        for doc in DOCS:
            doc_chunks = chunk_file(paths[doc["celex"]], design, problems)
            chunks[design] += doc_chunks
            per_doc.append(f"{doc['doc_id']} {len(doc_chunks)}")
        sizes = [chunk["metadata"]["word_count"] for chunk in chunks[design]]
        print(f"  {design:<8} {len(sizes):>5} chunks   words/chunk: mean {sum(sizes) / len(sizes):.0f}, min {min(sizes)}, max {max(sizes)}   ({', '.join(per_doc)})")

    print("\n== Embedding ==")
    budget, quota_hit = limit, False
    report = {}
    embed_order = [design for design in EMBED_ORDER if design in designs]
    for position, design in enumerate(embed_order):
        collection = get_collection(design)
        share = None if budget is None else math.ceil(budget / (len(embed_order) - position))
        if quota_hit:
            have = stored_ids(collection, [chunk["id"] for chunk in chunks[design]])
            stats = {"already": len(have), "stored": 0, "remaining": len(chunks[design]) - len(have)}
        else:
            stats = embed_and_store(chunks[design], collection, share)
            quota_hit = stats["quota_hit"]
            if budget is not None:
                budget -= stats["stored"]
        current = {chunk["id"] for chunk in chunks[design]}
        stale = []
        for doc in DOCS:
            stale += [i for i in collection.get(where={"doc_id": doc["doc_id"]}, include=[])["ids"] if i not in current]
        if stale and os.environ.get("PRUNE") == "1":
            collection.delete(ids=stale)
            print(f"  {design}: deleted {len(stale)} stale vectors (their chunks no longer exist)")
            stale = []
        report[design] = (stats, len(stale))

    print("\n== Vectors ==")
    for design in designs:
        stats, stale = report[design]
        stored = stats["already"] + stats["stored"]
        line = f"  {design:<8} {stored:>5} stored / {len(chunks[design])} chunks   {stats['remaining']} missing   ({stats['stored']} embedded in this run)"
        if stale:
            line += f"   {stale} stale vectors from an older chunking: rerun with PRUNE=1 to delete them"
        print(line)
    remaining = sum(stats["remaining"] for stats, _ in report.values())
    if quota_hit:
        print(f"\nStopped on the Gemini quota (429). {remaining} chunks still need a vector; rerun after the quota resets.")
    elif remaining:
        print(f"\n{remaining} chunks still need a vector (LIMIT={limit_text}). Rerun without LIMIT to embed them.")
    else:
        print("\nEvery chunk has a stored vector.")

    # Documents kept for add_document (corpus_extra/) are extracted for the problems log only: never embedded here.
    for path in sorted(EXTRA_DIR.glob("*.*")) if EXTRA_DIR.is_dir() else []:
        extract_file(path, problems)

    INDEX_DIR.mkdir(exist_ok=True)
    PROBLEMS_FILE.write_text(problems.to_markdown(), encoding="utf-8")
    print(f"Extraction problems log: {PROBLEMS_FILE.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
