"""
Assignment 3: build the index (`main.py index`).

Corpus: Anthropic, PBC IPO disclosure documents filed on SEC EDGAR, frozen as of
CORPUS_FROZEN_AT (see corpus_manifest.json). Pipeline per document:

    download()        corpus/raw/<file>  (git-ignored, verified against the pinned SHA-256)
    parse_*()         HTML -> Blocks (headings, paragraphs, tables) with printed page numbers
    select + redact   keep the sections in scope; replace personal names by roles
    chunk_blocks()    structure-aware chunks with source + location metadata
    embed_and_store() Gemini embeddings, only for chunks without a saved vector -> index/chroma

`python index.py --survey` builds the chunks and prints counts and the embedding
budget without calling any embedding API.

server.py imports `chunk_file(path)` and `embed_and_store(chunks)` from here.
Everything is logged to stderr, because server.py's stdout carries MCP.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import statistics
import sys
import time
from collections import Counter, deque
from dataclasses import asdict, dataclass, field
from pathlib import Path
from zoneinfo import ZoneInfo

import httpx
from bs4 import BeautifulSoup, NavigableString, Tag

ROOT = Path(__file__).resolve().parent
RAW_DIR = ROOT / "corpus" / "raw"
MANIFEST = ROOT / "corpus_manifest.json"
ENV_FILE = ROOT / ".env"
# CORPUS_INDEX_DIR lets an experiment (e.g. the add-document before/after test)
# run against a copy of the index without touching the committed one.
INDEX_DIR = Path(os.environ.get("CORPUS_INDEX_DIR") or ROOT / "index")
ADDED_REGISTRY = INDEX_DIR / "added_documents.json"
CHROMA_DIR = INDEX_DIR / "chroma"
CHUNKS_FILE = INDEX_DIR / "chunks.jsonl"
USAGE_FILE = ROOT / "corpus" / "embedding_usage.json"  # local quota bookkeeping, git-ignored

CORPUS_FROZEN_AT = "2026-11-19"
EDGAR = "https://www.sec.gov/Archives/edgar/data/2130357"

# Chunking
MAX_WORDS = 400          # target ceiling for a text chunk (tables may exceed it)
TABLE_MAX_TOKENS = 6000  # tables stay whole unless they approach the model's 8,192-token input limit
INTRO_MAX_WORDS = 80     # a short paragraph introducing a table travels with the table

# Embeddings (gemini-embedding-2 has no task_type: the task goes into the text)
EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768          # Google's recommended size; auto-normalised by the model
COLLECTION = "corpus"
# Free-tier limits of the student's project (AI Studio, 2026-11-19), with safety margins
RPM_LIMIT, TPM_LIMIT, DAILY_LIMIT = 100, 30_000, 1_000
RPM_BUDGET, TPM_BUDGET, DAILY_BUDGET = 80, 24_000, 950
BATCH_TEXTS = 20


def log(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


# =========================================================================== sources

@dataclass(frozen=True)
class Source:
    doc_id: str          # used in citations and in eval/questions.csv `expected_source`
    title: str
    url: str
    form: str
    accession: str
    filed: str
    status: str          # "preliminary" | "governing document" | ...
    parser: str          # "workiva" | "text-layer" | "flow"
    role: str = "core"   # "core" documents are indexed by `main.py index`


SOURCES: list[Source] = [
    Source(
        doc_id="US-PROSPECTUS",
        title="Form S-1/A Amendment No. 3 - U.S. preliminary prospectus (filed 2026-11-17)",
        url=f"{EDGAR}/000162828026074338/anthropicpbc-sx1ax3.htm",
        form="S-1/A", accession="0001628280-26-074338", filed="2026-11-17",
        status="preliminary", parser="workiva",
    ),
    Source(
        doc_id="EU-PROSPECTUS",
        title="EEA prospectus approved by BaFin, dated 2026-11-11 (filed on EDGAR as FWP 2026-11-12)",
        url=f"{EDGAR}/000162828026073040/anthropicpbc-fwpxeeaprospea.htm",
        form="FWP", accession="0001628280-26-073040", filed="2026-11-12",
        status="preliminary", parser="text-layer",
    ),
    Source(
        doc_id="CHARTER",
        title="Amended and Restated Certificate of Incorporation, effective at IPO completion (Exhibit 3.3 to Form S-1)",
        url=f"{EDGAR}/000162828026067168/exhibit33-sx1.htm",
        form="S-1 EX-3.3", accession="0001628280-26-067168", filed="2026-10-26",
        status="governing document", parser="flow",
    ),
]

# ---------------------------------------------------------------- scope (corpus B)
# US prospectus: level-1 sections are taken from the document's own table of
# contents. Sections not listed here are excluded; the reason is recorded.
US_INCLUDE = {
    "PROSPECTUS COVER PAGE",
    "SELECT DEFINED TERMS",
    "PROSPECTUS SUMMARY",
    "RISK FACTORS",
    "USE OF PROCEEDS",
    "DIVIDEND POLICY",
    "CAPITALIZATION",
    "DILUTION",
    "MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS",
    "BUSINESS",                       # 76% of its 8-grams are not in Summary/Risk Factors/MD&A
    "OUR GOVERNANCE STRUCTURE AND ITS GOALS",
    "DESCRIPTION OF CAPITAL STOCK",
    "SHARES ELIGIBLE FOR FUTURE SALE",
    "UNDERWRITING",
    "CONCURRENT PRIVATE PLACEMENT",
    "CONSOLIDATED BALANCE SHEETS",
    "CONSOLIDATED STATEMENTS OF OPERATIONS",
    "CONSOLIDATED STATEMENTS OF COMPREHENSIVE LOSS",
    "CONSOLIDATED STATEMENTS OF CASH FLOWS",
}
US_EXCLUDE_REASONS = {
    "MANAGEMENT": "personal data (names, ages, biographies)",
    "EXECUTIVE COMPENSATION": "personal data (individual pay)",
    "CERTAIN RELATIONSHIPS AND RELATED PERSON TRANSACTIONS": "personal data (named individuals' transactions)",
    "PRINCIPAL AND SELLING STOCKHOLDERS": "personal data (individual holdings)",
    "NOTES TO CONSOLIDATED FINANCIAL STATEMENTS": "out of scope / budget (32k words); key figures are in MD&A and primary statements",
}

# EU prospectus: only the EU-specific parts (measured 8-gram overlap with the US
# prospectus: Risk Factors 92%, MD&A 83%, Corporate Governance 88% -> duplicates).
# The text layer gives printed page numbers; ranges follow the prospectus TOC.
EU_PAGE_SECTIONS = [
    ("cover", "Cover Page and Important Notice"),
    ("S", "Summary of the Prospectus"),
    ((87, 94), "2. Persons Responsible, Third-Party Information and Competent Authority Approval"),
    ((198, 198), "6. Working Capital Statement"),
    ((199, 201), "7. Terms and Conditions of the Securities"),
    ((202, 227), "8. Details of the Offer"),
]

# Personal data (README: "no personal data"). Three auditable rules for the
# sections that are kept:
#  1. drop subsections that are biographies or related-person transactions;
#  2. drop paragraphs that are a biography, individual pay or an individual's trades;
#  3. replace every remaining personal name by the role it is mentioned in.
EXCLUDED_SUBSECTIONS = {
    "Our Co-Founders",
    "Certain Relationships and Transactions with the LTBT and its Trustees",
}
PERSONAL_PARAGRAPH_RE = re.compile(
    r"(has served as (?:a |our |the )?(?:Trustee|Chief|President|member)"
    r"|was selected to serve as a Trustee"
    r"|co-founded Anthropic in January 2021 and (?:serves|leads)"
    r"|has been an integral part of Anthropic"
    r"|receives annual cash compensation"
    r"|charitable donation to CNAS"
    r"|Mr\. Rao acquired shares)"
)
REDACTIONS: list[tuple[str, str]] = [   # applied in order, full names before surnames
    # Distinct identifiers keep people apart (who votes the Class F share, which
    # director is the Specified Class T Director...) without naming them.
    (r"Dr\. Neil “Buddy” Shah|Neil “Buddy” Shah|Neil Shah|Dr\.\s+Shah|\bShah\b", "[LTBT Trustee 1 (Chair)]"),
    (r"Richard Fontaine|(?:Mr|Dr)\.\s+Fontaine", "[LTBT Trustee 2]"),
    (r"(?:Dr\. )?Ben S\. Bernanke|(?:Mr|Dr)\.\s+Bernanke", "[LTBT Trustee 3]"),
    (r"(?:Dr\. )?Christopher Stubbs|(?:Mr|Dr)\.\s+Stubbs", "[LTBT Trustee 4]"),
    (r"Dario Amodei|Dr\.\s+Amodei", "[Co-founder 1 (CEO)]"),
    (r"Daniela Amodei|Ms\.\s+Amodei", "[Co-founder 2 (President)]"),
    (r"Tom Brown|Mr\.\s+Brown", "[Co-founder 3]"),
    (r"Jack Clark|Mr\.\s+Clark", "[Co-founder 4]"),
    (r"Jared Kaplan|Dr\.\s+Kaplan", "[Co-founder 5]"),
    (r"Sam McCandlish|Dr\.\s+McCandlish", "[Co-founder 6]"),
    (r"Christopher Olah|Chris Olah|Mr\.\s+Olah", "[Co-founder 7]"),
    (r"Benjamin Mann|Ben Mann|Mr\.\s+Mann", "[Early employee 1 (not a co-founder member of the Founder LLC)]"),
    (r"Krishna Rao|Mr\.\s+Rao", "[CFO]"),
    (r"Reed Hastings|Mr\.\s+Hastings", "[Director A]"),
    (r"Christopher Liddell|Mr\.\s+Liddell", "[Director B]"),
    (r"Vas Narasimhan|Dr\.\s+Narasimhan", "[Director C]"),
    (r"Yasmin Razavi|Ms\.\s+Razavi", "[Director D]"),
]


# =========================================================================== utils

def env_value(name: str) -> str | None:
    """A variable from the environment, else from .env (KEY=value lines)."""
    value = (os.environ.get(name) or "").strip()
    if value:
        return value
    if ENV_FILE.is_file():
        for line in ENV_FILE.read_text(encoding="utf-8").splitlines():
            key, sep, val = line.strip().partition("=")
            if sep and key.strip() == name:
                return val.strip().strip('"').strip("'") or None
    return None


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as f:
        for block in iter(lambda: f.read(1 << 20), b""):
            digest.update(block)
    return digest.hexdigest()


def clean_text(text: str) -> str:
    """Normalise whitespace and the spacing artefacts of the EDGAR HTML."""
    text = text.replace("\xa0", " ").replace("​", "")
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"([“(\[])\s+", r"\1", text)      # “ Corporation ” -> “Corporation”
    text = re.sub(r"\s+([”)\],.;:])", r"\1", text)
    return text


def word_count(text: str) -> int:
    return len(text.split())


def load_manifest() -> dict:
    if MANIFEST.is_file():
        return json.loads(MANIFEST.read_text(encoding="utf-8"))
    return {"frozen_at": CORPUS_FROZEN_AT, "documents": {}}


def save_manifest(manifest: dict) -> None:
    MANIFEST.write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


# =========================================================================== download

def raw_path(source: Source) -> Path:
    return RAW_DIR / source.url.rsplit("/", 1)[-1]


def download(source: Source, manifest: dict) -> Path:
    """Fetch one source into corpus/raw/ unless present, and verify its pinned SHA-256.

    The first download records the hash (that is the freeze); later runs refuse
    a file whose hash changed, so the corpus can never change silently.
    """
    path = raw_path(source)
    pinned = manifest["documents"].get(source.doc_id, {}).get("sha256")
    if not path.is_file():
        agent = env_value("SEC_USER_AGENT")
        if not agent:
            raise SystemExit(
                f"{path.name} is not in corpus/raw/ and SEC_USER_AGENT is not set.\n"
                "  SEC EDGAR rejects anonymous downloads. Add to .env:\n"
                '  SEC_USER_AGENT="<organisation or name> <contact email>"'
            )
        RAW_DIR.mkdir(parents=True, exist_ok=True)
        for attempt in range(4):
            try:
                response = httpx.get(source.url, headers={"User-Agent": agent}, timeout=120, follow_redirects=True)
                response.raise_for_status()
                break
            except httpx.HTTPError as error:
                if attempt == 3:
                    raise SystemExit(f"Could not download {source.url}: {error}")
                time.sleep(2 ** attempt)
        path.write_bytes(response.content)
        time.sleep(0.2)  # SEC fair access: at most 10 requests per second
        log(f"downloaded {path.name} ({len(response.content) / 1e6:.1f} MB)")

    digest = sha256_file(path)
    if pinned and digest != pinned:
        raise SystemExit(
            f"{path.name} does not match the frozen corpus (sha256 {digest[:12]}... != {pinned[:12]}...).\n"
            "  Delete it from corpus/raw/ and run again to re-download the frozen version."
        )
    manifest["documents"].setdefault(source.doc_id, {}).update(
        title=source.title, url=source.url, form=source.form, accession=source.accession,
        filed=source.filed, status=source.status, role=source.role, file=path.name,
        bytes=path.stat().st_size, sha256=digest,
        licence="SEC EDGAR public filing content: free to access and reuse (sec.gov Webmaster FAQ).",
    )
    return path


# =========================================================================== parsing

@dataclass
class Block:
    kind: str            # "heading" | "para" | "table"
    text: str
    level: int = 0       # heading level: 1 section, 2 subsection, 3 item (e.g. one risk factor)
    page: str = ""       # printed page label
    section: str = ""    # level-1 section this block belongs to


def _style(font: Tag) -> tuple[float, bool, bool]:
    style = font.get("style") or ""
    size = re.search(r"font-size:([\d.]+)pt", style)
    bold = "font-weight:bold" in style or "font-weight:700" in style
    return (float(size.group(1)) if size else 0.0, bold, "font-style:italic" in style)


def _top(tag: Tag) -> float | None:
    match = re.search(r"(?:^|;)top:([\d.]+)pt", tag.get("style") or "")
    return float(match.group(1)) if match else None


def _line_text(div: Tag) -> tuple[str, tuple[float, bool, bool]]:
    """Text of one positioned line: its <font> fragments joined WITHOUT spaces
    (Workiva splits words across fragments when justifying: 'o' + 'f ').
    Superscript footnote markers (< 6pt) are dropped. Style = dominant by characters."""
    parts, weight = [], Counter()
    for font in div.find_all("font", recursive=False):
        size, bold, italic = _style(font)
        text = font.get_text()
        if 0 < size < 6:
            continue
        parts.append(text)
        weight[(size, bold, italic)] += len(text.strip())
    style = weight.most_common(1)[0][0] if weight else (0.0, False, False)
    return clean_text("".join(parts)), style


def _table_text(table: Tag) -> str:
    """A table as pipe-separated rows; empty spacer cells dropped, '$' and ')' / '%' re-attached."""
    rows = []
    for tr in table.find_all("tr"):
        cells = []
        for td in tr.find_all(["td", "th"], recursive=False):
            lines = [_line_text(d)[0] for d in td.find_all("div") if d.find("font", recursive=False)]
            text = clean_text(" ".join(lines)) if lines else clean_text(td.get_text(""))
            if not text:
                continue
            if cells and text in {")", "%", ")%", "pp", "x"}:
                cells[-1] += text
            elif cells and cells[-1] in {"$", "€", "(", "$(", "€("}:
                cells[-1] += text
            else:
                cells.append(text)
        if cells:
            rows.append(" | ".join(cells))
    return "\n".join(rows)


def parse_workiva(html: str) -> list[Block]:
    """Workiva 'absolutely positioned' HTML (the S-1/A): every page is a 792pt div,
    every line a div with a `top` offset. Paragraphs are rebuilt from vertical gaps
    and font changes; level-1 sections come from the document's own TOC anchors."""
    soup = BeautifulSoup(html, "html.parser")
    toc: dict[str, str] = {}
    for a in soup.find_all("a", href=True):
        title = clean_text(a.get_text(" "))
        if a["href"].startswith("#") and title and not title.isdigit() and title != "Table of Contents":
            toc.setdefault(a["href"][1:], title.upper())
    pages = [d for d in soup.find_all("div") if "height:792pt" in (d.get("style") or "")]

    blocks: list[Block] = []
    section = "PROSPECTUS COVER PAGE"
    para: dict | None = None  # open paragraph/heading: kind, level, text, size, last_top, page

    def flush() -> None:
        nonlocal para
        if para and para["text"]:
            kind = "heading" if para["level"] else "para"
            blocks.append(Block(kind, para["text"], para["level"], para["page"], section))
        para = None

    def heading_level(style: tuple[float, bool, bool]) -> int:
        size, bold, _ = style
        if bold and size >= 16:
            return 1
        if bold and size >= 11:
            return 2
        if bold and size >= 9:
            return 3
        return 0

    for page in pages:
        label = ""
        for child in page.find_all("div", recursive=False):
            if "top:720pt" in (child.get("style") or ""):
                label = clean_text(child.get_text(""))
        label = label or "cover"
        footnotes: list[str] = []
        first_body_line = True

        def walk(node: Tag) -> None:
            nonlocal para, section, first_body_line
            for child in node.children:
                if not isinstance(child, Tag):
                    continue
                if "top:720pt" in (child.get("style") or "") and child.parent is page:
                    continue  # page-number footer
                anchors = [child] + child.find_all(id=True)
                hit = next((toc[t.get("id")] for t in anchors if t.get("id") in toc and t.get("id")), None)
                if hit and child.find("table") is None:
                    if hit != section:
                        flush()
                        section = hit
                if child.name == "table":
                    flush()
                    text = _table_text(child)
                    if text:
                        kind = "table" if ("|" in text or "\n" in text) else "para"
                        blocks.append(Block(kind, text, 0, label, section))
                    continue
                if child.name == "div" and child.find("font", recursive=False) is not None:
                    text, style = _line_text(child)
                    if not text or text == "Table of Contents":
                        continue
                    top = _top(child)
                    if top is None:  # page-bottom footnote, emitted after the page body
                        footnotes.append(text)
                        continue
                    level = heading_level(style)
                    size = style[0]
                    if first_body_line:
                        first_body_line = False
                        # paragraph continuing from the previous page
                        if (para and not level and not para["level"] and para["size"] == size
                                and not re.search(r"[.!?:;”)]$", para["text"])):
                            para["text"] = _join(para["text"], text)
                            para["last_top"] = top
                            continue
                        flush()
                    if para is not None:
                        gap = top - para["last_top"]
                        same = level == para["level"] and size == para["size"]
                        if same and 0 < gap <= 1.35 * size * 1.2:
                            para["text"] = _join(para["text"], text)
                            para["last_top"] = top
                            continue
                        flush()
                    para = {"level": level, "text": text, "size": size, "last_top": top, "page": label}
                    continue
                walk(child)

        walk(page)
        if footnotes:
            open_para = para
            para = None
            for note in footnotes:
                blocks.append(Block("para", note, 0, label, section))
            para = open_para
    flush()
    return blocks


def _join(left: str, right: str) -> str:
    """Join two lines; a line ending in a hyphen keeps it and takes no space (co-founder)."""
    if left.endswith("-"):
        return left + right
    return f"{left} {right}"


HEADING_RE = re.compile(r"^(\d{1,2}(?:\.\d{1,2}){0,3})\.?\s+([A-Z“][^.]{1,110})$")
SUMMARY_HEADING_RE = re.compile(r"^([A-D](?:\.\d)?)\.?\s+([A-Z][^.]{1,120}\??)$")


def parse_text_layer(html: str) -> list[Block]:
    """The EEA prospectus: a PDF rendered as page images with a hidden 1pt text
    layer per page. Lines are separated by two spaces; headings are numbered
    ('8.1 Terms and Conditions of the Offer'); a paragraph ends on a short line
    ending with punctuation. Only pages in EU_PAGE_SECTIONS are kept."""
    soup = BeautifulSoup(html, "html.parser")
    layers = [f.get_text() for f in soup.find_all("font") if "font-size:1pt" in (f.get("style") or "")]
    blocks: list[Block] = []
    summary_letter = ""
    for index, layer in enumerate(layers):
        lines = [clean_text(x) for x in re.split(r"\s{2,}", layer) if clean_text(x)]
        if not lines:
            continue
        label = lines[0] if re.fullmatch(r"S-\d+|G-\d+|[ivx]+|\d+", lines[0]) else ""
        if label:
            lines = lines[1:]
        section = _eu_section(label, index)
        if section is None:
            continue
        typical = statistics.median(len(x) for x in lines) if lines else 0
        para: list[str] = []
        letter = summary_letter

        def flush() -> None:
            if para:
                blocks.append(Block("para", _join_all(para), 0, label or "cover", section))
                para.clear()

        for line in lines:
            if line in {"S", "Summary of the Prospectus"} and label.startswith("S-"):
                continue
            prev = blocks[-1] if blocks else None
            if (not para and prev and prev.kind == "heading" and prev.page == (label or "cover")
                    and (line[:1].islower() or line.startswith("and ")) and len(line) < 0.6 * typical
                    and not re.match(r"^[a-z]\)", line)):
                prev.text = _join(prev.text, line)  # heading wrapped onto a second line
                continue
            match = HEADING_RE.match(line) or (SUMMARY_HEADING_RE.match(line) if label.startswith("S-") else None)
            # summary pages are full of short table rows, so a relative length test fails there
            short = len(line) < 130 if label.startswith("S-") else len(line) < 0.8 * max(typical, 60)
            if match and short and not line.endswith(","):
                flush()
                number = match.group(1)
                if label.startswith("S-"):
                    # The summary prints "B. Key Information on the Issuer" and then
                    # "1. Who is the issuer...": carry the letter -> "B.1 Who is..."
                    if number[0].isalpha():
                        letter = number[0]
                        level = 2
                    else:
                        line = f"{letter}.{number} {match.group(2)}"
                        level = 3
                else:
                    depth = number.count(".") + 1
                    level = 1 if depth == 1 else min(depth, 3)
                blocks.append(Block("heading", line, level, label or "cover", section))
                continue
            para.append(line)
            if len(line) < 0.85 * typical and re.search(r"[.:;!?”)]$", line):
                flush()
        flush()
        summary_letter = letter
    # merge paragraphs split by page breaks (previous does not end a sentence)
    merged: list[Block] = []
    for block in blocks:
        prev = merged[-1] if merged else None
        if (prev and block.kind == prev.kind == "para" and block.section == prev.section
                and not re.search(r"[.!?:;”)]$", prev.text) and block.text[:1].islower()):
            prev.text = _join(prev.text, block.text)
        else:
            merged.append(block)
    return merged


def _join_all(lines: list[str]) -> str:
    text = lines[0]
    for line in lines[1:]:
        text = _join(text, line)
    return text


def _eu_section(label: str, index: int) -> str | None:
    if index < 2 or label in {"ii"}:
        return "Cover Page and Important Notice"
    if label.startswith("S-"):
        return "Summary of the Prospectus"
    if label.isdigit():
        page = int(label)
        for pages, name in EU_PAGE_SECTIONS:
            if isinstance(pages, tuple) and pages[0] <= page <= pages[1]:
                return name
    return None


def parse_flow(html: str, default_section: str = "Preamble") -> list[Block]:
    """Ordinary flowing HTML (the charter): one <div> per paragraph, 'ARTICLE IV'
    headings, '- 2 -' page footers, numbered sections ('5.1 Definitions.') inline."""
    soup = BeautifulSoup(html, "html.parser")
    blocks: list[Block] = []
    page, section = 1, default_section
    for div in soup.body.find_all("div"):
        if div.find("div"):
            continue
        # fragments are separate tags ("5.1" + "Definitions"): join with spaces;
        # clean_text then removes the spaces inside quotes (“ Acquisition ” -> “Acquisition”)
        text = clean_text(div.get_text(" "))
        if not text:
            continue
        if re.fullmatch(r"-\s*\d+\s*-", text):
            page = int(re.sub(r"\D", "", text)) + 1
            continue
        if text.startswith("IN WITNESS WHEREOF"):
            break  # signature block: personal data, no content
        if re.fullmatch(r"ARTICLE [IVXL]+", text):
            section = "Article " + text.split()[1]
            blocks.append(Block("heading", section, 1, str(page), section))
            continue
        number = re.match(r"^(\d+\.\d+(?:\.\d+)?)\s*([A-Z][^.]{2,80})\.", text)
        if number:
            blocks.append(Block("heading", f"Section {number.group(1)} {number.group(2)}", 2, str(page), section))
        prev = blocks[-1] if blocks else None
        if prev and prev.kind == "para" and text[:1].islower() and not re.search(r"[.;:]$", prev.text):
            prev.text = _join(prev.text, text)  # paragraph continued after a page break
            continue
        blocks.append(Block("para", text, 0, str(page), section))
    return blocks


def parse_pdf(path: Path) -> list[Block]:
    """Text PDFs (e.g. an issuer notice): one paragraph per block of lines; a
    paragraph ends on a short line ending with punctuation. Section = document title."""
    from pypdf import PdfReader

    reader = PdfReader(str(path))
    pages = [(str(n), (p.extract_text() or "")) for n, p in enumerate(reader.pages, start=1)]
    first = next((clean_text(ln) for _, t in pages for ln in t.splitlines() if ln.strip()), path.stem)
    section = _short(first, 120)
    blocks: list[Block] = []
    for label, text in pages:
        lines = [clean_text(x) for x in text.splitlines() if clean_text(x)]
        if not lines:
            continue
        longest = max(len(x) for x in lines)
        para: list[str] = []
        for line in lines:
            para.append(line)
            if len(line) < 0.8 * longest and re.search(r"[.:;!?”)]$", line):
                blocks.append(Block("para", _join_all(para), 0, label, section))
                para = []
        if para:
            blocks.append(Block("para", _join_all(para), 0, label, section))
    return blocks


def parse_plain(text: str, section: str) -> list[Block]:
    """Plain text / Markdown: paragraphs separated by blank lines; '#' lines are headings."""
    blocks: list[Block] = []
    for part in re.split(r"\n\s*\n", text):
        part = part.strip()
        if not part:
            continue
        heading = re.match(r"^(#{1,3})\s+(.+)$", part)
        if heading and "\n" not in part:
            blocks.append(Block("heading", heading.group(2), len(heading.group(1)) + 1, "", section))
        else:
            blocks.append(Block("para", clean_text(part), 0, "", section))
    return blocks


PARSERS = {"workiva": parse_workiva, "text-layer": parse_text_layer, "flow": parse_flow}
ALLOWED_SUFFIXES = {".pdf", ".htm", ".html", ".txt", ".md"}


def doc_id_for(path: Path) -> str:
    return re.sub(r"[^A-Za-z0-9]+", "-", path.stem).strip("-").upper()[:60] or "DOCUMENT"


def chunk_file(path: str | Path, doc_id: str | None = None) -> list[Chunk]:
    """Run ONE file through the same pipeline as the corpus (parse -> redact ->
    structure-aware chunks with source and location). Used by server.py's
    add_document. No API calls."""
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix not in ALLOWED_SUFFIXES:
        raise ValueError(f"unsupported file type {suffix!r}; allowed: {', '.join(sorted(ALLOWED_SUFFIXES))}")
    doc_id = doc_id or doc_id_for(path)
    if suffix == ".pdf":
        blocks, parser = parse_pdf(path), "pdf"
    elif suffix in {".htm", ".html"}:
        html = path.read_text(encoding="utf-8", errors="replace")
        if "height:792pt" in html:
            blocks, parser = parse_workiva(html), "workiva"
        else:
            blocks, parser = parse_flow(html, default_section=path.stem), "flow"
    else:
        blocks, parser = parse_plain(path.read_text(encoding="utf-8", errors="replace"), path.stem), "plain"
    for b in blocks:
        b.text = redact(b.text)
    source = Source(
        doc_id=doc_id, title=path.name, url=path.name, form=suffix.lstrip(".").upper(),
        accession="", filed=dt.date.today().isoformat(), status="added document", parser=parser, role="added",
    )
    return chunk_blocks(source, [b for b in blocks if b.text])


def load_registry() -> dict:
    return json.loads(ADDED_REGISTRY.read_text(encoding="utf-8")) if ADDED_REGISTRY.is_file() else {}


def save_registry(registry: dict) -> None:
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    ADDED_REGISTRY.write_text(json.dumps(registry, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def redact(text: str) -> str:
    for pattern, role in REDACTIONS:
        text = re.sub(pattern, role, text)
    return text


def section_in(section: str, names: set[str]) -> bool:
    """TOC titles can be truncated ('... RESULTS OF'): compare on a common prefix."""
    return any(section == n or (len(section) >= 40 and n.startswith(section)) for n in names)


def select_blocks(source: Source, blocks: list[Block]) -> list[Block]:
    if source.doc_id == "US-PROSPECTUS":
        blocks = [b for b in blocks if section_in(b.section, US_INCLUDE)]
        for b in blocks:  # the TOC truncates this title
            if b.section.startswith("MANAGEMENT’S DISCUSSION"):
                b.section = "MANAGEMENT’S DISCUSSION AND ANALYSIS OF FINANCIAL CONDITION AND RESULTS OF OPERATIONS"
        # The cover section starts with the registration-statement facing page (agent
        # for service, counsel names and addresses): keep from the prospectus cover on.
        start = next((i for i, b in enumerate(blocks) if b.text.startswith("Subject to Completion")), 0)
        blocks = blocks[start:]
        # the level-1 heading line repeats the section name: drop it
        blocks = [b for b in blocks if not (b.kind == "heading" and b.level == 1 and b.text.upper() == b.section)]
    kept, skip_level = [], 0
    for b in blocks:
        if b.kind == "heading" and b.level >= 2:
            if skip_level and b.level > skip_level:
                continue
            skip_level = b.level if b.text in EXCLUDED_SUBSECTIONS else 0
            if skip_level:
                continue
        elif skip_level:
            continue
        if b.kind == "para" and PERSONAL_PARAGRAPH_RE.search(b.text):
            continue
        b.text = redact(b.text)
        kept.append(b)
    return kept


# =========================================================================== chunking

@dataclass
class Chunk:
    id: str
    source: str          # doc_id
    location: str        # "Section > Subsection > Item"
    page: str            # "31" or "31-32"
    text: str            # what search returns and the model reads
    title: str           # what is embedded as `title:` (doc + location)
    kind: str            # "text" | "table"
    words: int
    order: int
    meta: dict = field(default_factory=dict)

    def embed_input(self) -> str:
        return f"title: {self.title} | text: {self.text}"


def _sentences(text: str) -> list[str]:
    return re.split(r"(?<=[.;])\s+(?=[A-Z(“•])", text)


def _split_long(text: str, limit: int) -> list[str]:
    pieces, current = [], ""
    for sentence in _sentences(text):
        if current and word_count(current) + word_count(sentence) > limit:
            pieces.append(current)
            current = sentence
        else:
            current = f"{current} {sentence}".strip()
    if current:
        pieces.append(current)
    # a single sentence longer than the limit is cut by words
    out = []
    for piece in pieces:
        words = piece.split()
        out += [" ".join(words[i:i + limit]) for i in range(0, len(words), limit)]
    return out


def _split_table(text: str, limit: int) -> list[str]:
    rows = text.split("\n")
    header = rows[:2] if len(rows) > 4 else rows[:1]
    parts, current = [], list(header)
    for row in rows[len(header):]:
        if word_count("\n".join(current + [row])) > limit and len(current) > len(header):
            parts.append("\n".join(current))
            current = list(header)
        current.append(row)
    parts.append("\n".join(current))
    return parts


MIN_WORDS = 80           # smaller pieces are merged with a neighbour from the same section


def chunk_blocks(source: Source, blocks: list[Block]) -> list[Chunk]:
    """Structure-aware chunking.

    1. Split: a piece never crosses a heading; paragraphs are packed up to
       MAX_WORDS; a level-3 heading (e.g. a risk factor's bold thesis) opens its
       piece as content; a table stays whole with its short intro paragraph, even
       above MAX_WORDS (split by rows only beyond TABLE_MAX_TOKENS).
    2. Merge: a piece under MIN_WORDS joins its neighbour only if both have the
       same heading path (same section, subsection and item) and the result fits.
    """
    pieces: list[dict] = []
    path = ["", "", ""]
    body: list[str] = []
    pages: list[str] = []

    def emit(texts: list[str], kind: str, page_list: list[str]) -> None:
        text = "\n".join(t for t in texts if t).strip()
        if text:
            pieces.append({"path": list(path), "text": text, "kind": kind,
                           "pages": [p for p in page_list if p] or [""]})

    def flush() -> None:
        nonlocal body, pages
        emit(body, "text", pages)
        body, pages = [], []

    for block in blocks:
        if block.section != path[0]:
            flush()
            path = [block.section, "", ""]
        if block.kind == "heading":
            flush()
            level = max(1, min(block.level, 3))
            if level == 1:
                if block.text.upper() != block.section.upper():
                    path[1], path[2] = block.text, ""
                continue
            path[level - 1] = block.text
            for deeper in range(level, 3):
                path[deeper] = ""
            if level == 3:  # the item heading is content (a risk factor's thesis)
                body, pages = [block.text], [block.page]
            continue

        words = word_count(block.text)
        if block.kind == "table":
            intro = body.pop() if body and word_count(body[-1]) <= INTRO_MAX_WORDS else None
            flush()
            if estimate_tokens(f"{intro or ''} {block.text}") <= TABLE_MAX_TOKENS:
                parts = [block.text]
            else:  # only beyond the model's limit: split by rows, header repeated
                parts = _split_table(block.text, int(TABLE_MAX_TOKENS / 2.2))
            for part in parts:
                emit([intro, part], "table", [block.page])
            continue
        if words > MAX_WORDS:
            flush()
            for piece in _split_long(block.text, MAX_WORDS):
                emit([piece], "text", [block.page])
            continue
        if body and sum(word_count(t) for t in body) + words > MAX_WORDS:
            flush()
        body.append(block.text)
        pages.append(block.page)
    flush()

    merged: list[dict] = []
    for piece in pieces:
        prev = merged[-1] if merged else None
        # merge only inside the same heading path: never across sections,
        # subsections or two different risk factors
        if prev and prev["path"] == piece["path"]:
            small = min(word_count(prev["text"]), word_count(piece["text"])) < MIN_WORDS
            has_table = "table" in (prev["kind"], piece["kind"])
            fits = (estimate_tokens(prev["text"] + piece["text"]) <= TABLE_MAX_TOKENS if has_table
                    else word_count(prev["text"]) + word_count(piece["text"]) <= MAX_WORDS)
            if small and fits:
                prev["text"] += "\n" + piece["text"]
                prev["kind"] = "table" if "table" in (prev["kind"], piece["kind"]) else "text"
                prev["pages"] += piece["pages"]
                continue
        merged.append(piece)

    chunks: list[Chunk] = []
    for piece in merged:
        loc = " > ".join(_short(p) for p in piece["path"] if p)
        pg = [p for p in piece["pages"] if p] or [""]
        page = pg[0] if pg[0] == pg[-1] else f"{pg[0]}-{pg[-1]}"
        title = f"{source.doc_id} ({source.form}, {source.status}) | {loc}"
        digest = hashlib.sha256(f"{title}\n{piece['text']}".encode()).hexdigest()[:16]
        chunks.append(Chunk(
            id=f"{source.doc_id}-{digest}", source=source.doc_id, location=loc, page=page,
            text=piece["text"], title=title, kind=piece["kind"], words=word_count(piece["text"]),
            order=len(chunks), meta={"section": piece["path"][0], "filed": source.filed, "status": source.status},
        ))
    return chunks


def _short(text: str, limit: int = 110) -> str:
    text = text.strip()
    return text if len(text) <= limit else text[: limit - 1].rsplit(" ", 1)[0] + "…"


def build_chunks() -> tuple[list[Chunk], dict]:
    """Download (or verify), parse, select, redact and chunk every core source."""
    manifest = load_manifest()
    all_chunks: list[Chunk] = []
    stats: dict = {}
    for source in SOURCES:
        path = download(source, manifest)
        raw_blocks = PARSERS[source.parser](path.read_text(encoding="utf-8", errors="replace"))
        blocks = select_blocks(source, raw_blocks)
        chunks = chunk_blocks(source, blocks)
        stats[source.doc_id] = {"raw_blocks": raw_blocks, "blocks": blocks, "chunks": chunks}
        all_chunks += chunks
    save_manifest(manifest)
    return all_chunks, stats


def write_chunks(chunks: list[Chunk]) -> None:
    INDEX_DIR.mkdir(exist_ok=True)
    with CHUNKS_FILE.open("w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(json.dumps(asdict(chunk), ensure_ascii=False) + "\n")


def read_chunks(path: Path = CHUNKS_FILE) -> list[Chunk]:
    if not path.is_file():
        return []
    return [Chunk(**json.loads(line)) for line in path.read_text(encoding="utf-8").splitlines() if line.strip()]


# =========================================================================== embeddings

def estimate_tokens(text: str) -> int:
    """Conservative token estimate (≈3.2 characters per token for financial text)."""
    return int(len(text) / 3.2) + 8


class RateLimiter:
    """Keeps requests and tokens inside per-minute budgets (sliding 60 s window)."""

    def __init__(self, rpm: int, tpm: int):
        self.rpm, self.tpm = rpm, tpm
        self.events: deque[tuple[float, int]] = deque()

    def wait(self, tokens: int) -> None:
        while True:
            now = time.monotonic()
            while self.events and now - self.events[0][0] > 60:
                self.events.popleft()
            used = sum(t for _, t in self.events)
            if len(self.events) < self.rpm and used + tokens <= self.tpm:
                self.events.append((now, tokens))
                return
            time.sleep(1.0)


def _pacific_today() -> str:
    return dt.datetime.now(ZoneInfo("America/Los_Angeles")).date().isoformat()  # quota resets at PT midnight


def _usage() -> dict:
    if USAGE_FILE.is_file():
        return json.loads(USAGE_FILE.read_text())
    return {}


def _record_usage(n: int) -> None:
    usage = _usage()
    usage[_pacific_today()] = usage.get(_pacific_today(), 0) + n
    USAGE_FILE.parent.mkdir(parents=True, exist_ok=True)
    USAGE_FILE.write_text(json.dumps(usage, indent=2))


def used_today() -> int:
    return _usage().get(_pacific_today(), 0)


_CLIENT = None
_LIMITER = RateLimiter(RPM_BUDGET, TPM_BUDGET)


def _client():
    global _CLIENT
    if _CLIENT is None:
        from google import genai
        from api_key import load_api_key
        _CLIENT = genai.Client(api_key=load_api_key())
    return _CLIENT


def embed_texts(texts: list[str]) -> list[list[float]]:
    """One embedding per text. Each text goes in its own Content: a plain list of
    strings would return ONE aggregated embedding for gemini-embedding-2."""
    from google.genai import types

    _LIMITER.wait(sum(estimate_tokens(t) for t in texts))
    contents = [types.Content(parts=[types.Part(text=t)]) for t in texts]
    for attempt in range(6):
        try:
            response = _client().models.embed_content(
                model=EMBED_MODEL, contents=contents,
                config=types.EmbedContentConfig(output_dimensionality=EMBED_DIM),
            )
            break
        except Exception as error:  # noqa: BLE001 - retry rate limits and transient errors
            message = str(error)
            if "PerDay" in message or "per day" in message.lower():
                raise SystemExit(f"Daily embedding quota exhausted: {message[:300]}")
            if attempt == 5 or not any(code in message for code in ("429", "500", "503", "RESOURCE_EXHAUSTED", "UNAVAILABLE")):
                raise
            delay = min(60, 5 * 2 ** attempt)
            log(f"  embedding call failed ({message[:120]}); retrying in {delay}s")
            time.sleep(delay)
    _record_usage(len(texts))
    vectors = [list(e.values) for e in response.embeddings]
    if len(vectors) != len(texts):
        raise RuntimeError(f"expected {len(texts)} embeddings, got {len(vectors)}")
    return vectors


def embed_query(question: str) -> list[float]:
    return embed_texts([f"task: question answering | query: {question}"])[0]


def collection():
    import chromadb
    from chromadb.config import Settings

    client = chromadb.PersistentClient(path=str(CHROMA_DIR), settings=Settings(anonymized_telemetry=False))
    return client.get_or_create_collection(COLLECTION, metadata={"hnsw:space": "cosine"})


def _metadata(chunk: Chunk) -> dict:
    meta = {"source": chunk.source, "location": chunk.location, "page": chunk.page,
            "title": chunk.title, "kind": chunk.kind, "words": chunk.words, "order": chunk.order}
    meta.update({k: v for k, v in chunk.meta.items() if isinstance(v, (str, int, float, bool))})
    return meta


def embed_and_store(chunks: list[Chunk], daily_budget: int = DAILY_BUDGET) -> dict:
    """Embed and store only chunks whose id has no saved vector. Saves after every
    batch, so a crash or the daily limit loses nothing. Returns counts."""
    col = collection()
    existing = set()
    ids = [c.id for c in chunks]
    for i in range(0, len(ids), 500):
        existing |= set(col.get(ids=ids[i:i + 500], include=[])["ids"])
    missing = [c for c in chunks if c.id not in existing]
    remaining = max(0, daily_budget - used_today())
    todo = missing[:remaining]
    if len(todo) < len(missing):
        log(f"daily budget: embedding {len(todo)} of {len(missing)} missing chunks today; run again after the reset")
    done = 0
    for i in range(0, len(todo), BATCH_TEXTS):
        batch = todo[i:i + BATCH_TEXTS]
        vectors = embed_texts([c.embed_input() for c in batch])
        col.add(ids=[c.id for c in batch], embeddings=vectors,
                documents=[c.text for c in batch], metadatas=[_metadata(c) for c in batch])
        done += len(batch)
        log(f"  embedded {done}/{len(todo)}")
    return {"already": len(existing), "embedded": done, "pending": len(missing) - done}


def prune_stale(chunks: list[Chunk]) -> int:
    """Delete vectors of core-document chunks that the current pipeline no longer
    produces (e.g. after a parsing fix). Documents added later via add_document
    are never touched."""
    col = collection()
    core = sorted({s.doc_id for s in SOURCES})
    current = {c.id for c in chunks}
    stored = col.get(where={"source": {"$in": core}}, include=[])["ids"]
    stale = [i for i in stored if i not in current]
    for i in range(0, len(stale), 500):
        col.delete(ids=stale[i:i + 500])
    return len(stale)


def delete_source(doc_id: str, keep_ids: set[str] = frozenset()) -> int:
    """Remove the stored chunks of one document (except keep_ids). Returns the count."""
    col = collection()
    ids = [i for i in col.get(where={"source": doc_id}, include=[])["ids"] if i not in keep_ids]
    for i in range(0, len(ids), 500):
        col.delete(ids=ids[i:i + 500])
    return len(ids)


# =========================================================================== report

def survey(chunks: list[Chunk], stats: dict) -> None:
    log(f"\nCorpus frozen at {CORPUS_FROZEN_AT}")
    total_words = 0
    for doc_id, s in stats.items():
        words = Counter()
        for b in s["blocks"]:
            words[b.section] += word_count(b.text)
        doc_words = sum(words.values())
        total_words += doc_words
        n = len(s["chunks"])
        log(f"\n{doc_id}: {doc_words:,} words kept in {len(words)} sections -> {n} chunks")
        for section, w in words.items():
            c = sum(1 for ch in s["chunks"] if ch.meta["section"] == section)
            log(f"   {w:7,d} words {c:4d} chunks  {section[:80]}")
    sizes = [c.words for c in chunks]
    tokens = sum(estimate_tokens(c.embed_input()) for c in chunks)
    log(f"\nTOTAL {total_words:,} words, {len(chunks)} chunks "
        f"({sum(c.kind == 'table' for c in chunks)} tables); words/chunk median {statistics.median(sizes):.0f}, "
        f"p10 {sorted(sizes)[len(sizes) // 10]}, p90 {sorted(sizes)[9 * len(sizes) // 10]}, max {max(sizes)}")
    log(f"embedding input ≈ {tokens:,} tokens -> ≈ {tokens / TPM_BUDGET:.1f} min at {TPM_BUDGET:,} tokens/min")
    log(f"daily quota: {DAILY_LIMIT}, used today (local count): {used_today()}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--survey", action="store_true", help="build chunks and report; no embeddings")
    args = parser.parse_args()

    chunks, stats = build_chunks()
    survey(chunks, stats)
    if args.survey:
        return
    write_chunks(chunks)
    result = embed_and_store(chunks)
    pruned = prune_stale(chunks) if not result["pending"] else 0
    log(f"\nindex: {result['already']} chunks already embedded, {result['embedded']} embedded now, "
        f"{result['pending']} pending, {pruned} stale removed -> {CHROMA_DIR.relative_to(ROOT)}")
    if result["pending"]:
        raise SystemExit("Some chunks are not embedded yet (daily quota). Run `main.py index` again after the reset.")


if __name__ == "__main__":
    main()
