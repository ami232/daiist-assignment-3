"""
Assignment 3: build the index (`main.py index`). server.py imports this module.

Pipeline, one function per step:
  1. download   SEC EDGAR filing, once, into corpus/<doc_id>/raw.htm
  2. extract    HTML -> text (inline XBRL stripped, tables as "a | b | c" rows),
                cut to Item 1A Risk Factors + the results part of MD&A (TRIM),
                saved as corpus/<doc_id>/<section>.txt (committed)
  3. chunk      two designs (DESIGNS): fixed 300-word windows, or one chunk per
                subsection / risk factor. Every chunk keeps doc, section,
                heading and the line range in its section file.
  4. embed      gemini-embedding-2 at 768 dimensions. Every vector is cached in
                index/embeddings.sqlite the moment it arrives, keyed by the
                exact text, so nothing is ever embedded twice.
  5. store      one ChromaDB collection per design in index/chroma.

Run:  uv run python index.py             # build or top up the index
      uv run python index.py --dry-run   # chunk and count only, no API calls
      uv run python index.py --force     # redo text extraction from raw.htm
"""

from __future__ import annotations

import json
import os
import re
import sys
import time
from pathlib import Path

import httpx
from bs4 import BeautifulSoup, NavigableString

ROOT = Path(__file__).resolve().parent
CORPUS = ROOT / "corpus"

# SEC refuses requests without a User-Agent naming a person and an email.
# Set SEC_USER_AGENT in .env or the environment, e.g. "Constantin Hatecke you@example.com".
DEFAULT_USER_AGENT = "Constantin Hatecke daiist-assignment-3 (set SEC_USER_AGENT)"

# The corpus. `indexed=False` keeps a document out of the initial index: it is
# the one we add later through the add_document tool.
DOCUMENTS = [
    {
        "doc_id": "GS_10K_FY2025",
        "company": "Goldman Sachs",
        "form": "10-K",
        "period": "2025-12-31",
        "url": "https://www.sec.gov/Archives/edgar/data/886982/000088698226000091/gs-20251231.htm",
        "indexed": True,
    },
    {
        "doc_id": "MS_10K_FY2025",
        "company": "Morgan Stanley",
        "form": "10-K",
        "period": "2025-12-31",
        "url": "https://www.sec.gov/Archives/edgar/data/895421/000089542126000086/ms-20251231.htm",
        "indexed": True,
    },
    {
        "doc_id": "BLK_10K_FY2025",
        "company": "BlackRock",
        "form": "10-K",
        "period": "2025-12-31",
        "url": "https://www.sec.gov/Archives/edgar/data/2012383/000119312526071966/blk-20251231.htm",
        "indexed": True,
    },
    {
        "doc_id": "GS_10Q_Q3_2026",
        "company": "Goldman Sachs",
        "form": "10-Q",
        "period": "2026-09-30",
        "url": "https://www.sec.gov/Archives/edgar/data/886982/000088698226000532/gs-20260930.htm",
        "indexed": False,
    },
]

# Sections we keep, by form. Keys are our section ids; values are the titles
# as they appear in the filing (matched case-insensitively, with or without
# an "Item 1A." prefix, because Morgan Stanley drops the item numbers).
WANTED = {
    "10-K": {
        "item_1a_risk_factors": "risk factors",
        "item_7_mdna": "management's discussion and analysis of financial condition and results of operations",
    },
    "10-Q": {
        "item_2_mdna": "management's discussion and analysis of financial condition and results of operations",
    },
}

# Inside MD&A we keep the results part only. Headings are matched as whole
# lines, case-insensitively. `stop_at`: the section ends at the first of these
# headings. `skip`: drop everything from the first heading up to (not
# including) the second.
TRIM = {
    "GS_10K_FY2025": {"item_7_mdna": {
        "stop_at": ["Balance Sheet and Funding Sources"],
        "skip": [("Critical Accounting Policy", "Results of Operations")],
    }},
    "MS_10K_FY2025": {"item_7_mdna": {
        "stop_at": ["Supplemental Financial Information"],
    }},
    "BLK_10K_FY2025": {"item_7_mdna": {
        "stop_at": ["Statement of financial condition Overview"],
    }},
    "GS_10Q_Q3_2026": {"item_2_mdna": {
        "stop_at": ["Balance Sheet and Funding Sources"],
        "skip": [("Critical Accounting Policy", "Results of Operations")],
    }},
}

# Running headers repeated on every page of a section (whole lines, any case).
RUNNING_HEADERS = {
    "the goldman sachs group, inc. and subsidiaries",
    "management's discussion and analysis",
    "management's discussion and analysis (continued)",
    "risk factors (continued)",
}

# Every top-level heading that can follow one of our sections. A section runs
# from its heading to the next heading in this list.
BOUNDARY_TITLES = [
    "business",
    "risk factors",
    "unresolved staff comments",
    "cybersecurity",
    "properties",
    "legal proceedings",
    "mine safety disclosures",
    "market for registrant's common equity, related stockholder matters and issuer purchases of equity securities",
    "selected financial data",
    "[reserved]",
    "reserved",
    "management's discussion and analysis of financial condition and results of operations",
    "quantitative and qualitative disclosures about market risk",
    "quantitative and qualitative disclosures about risk",
    "financial statements and supplementary data",
    "changes in and disagreements with accountants on accounting and financial disclosure",
    "controls and procedures",
    "other information",
    "disclosure regarding foreign jurisdictions that prevent inspections",
    "directors, executive officers and corporate governance",
    "executive compensation",
    "exhibits and financial statement schedules",
    "exhibits, financial statement schedules",
    "form 10-k summary",
    "signatures",
    "financial statements",
    "unregistered sales of equity securities and use of proceeds",
    "defaults upon senior securities",
    "exhibits",
]

BLOCK_TAGS = [
    "p", "div", "br", "li", "ul", "ol", "h1", "h2", "h3", "h4", "h5", "h6",
    "section", "article", "header", "footer", "blockquote", "pre", "hr",
]


# ---------------------------------------------------------------- download

def user_agent() -> str:
    agent = os.environ.get("SEC_USER_AGENT", "").strip()
    if not agent:
        env_file = ROOT / ".env"
        if env_file.is_file():
            for line in env_file.read_text(encoding="utf-8").splitlines():
                name, _, value = line.partition("=")
                if name.strip() == "SEC_USER_AGENT":
                    agent = value.strip().strip('"').strip("'")
    return agent or DEFAULT_USER_AGENT


def raw_path(doc: dict) -> Path:
    return CORPUS / doc["doc_id"] / "raw.htm"


def download(doc: dict) -> Path:
    """Fetch the filing once. If corpus/<doc_id>/raw.htm exists, do nothing."""
    path = raw_path(doc)
    if path.is_file() and path.stat().st_size > 0:
        log(f"  cached   {doc['doc_id']}  ({path.stat().st_size / 1e6:.1f} MB)")
        return path

    path.parent.mkdir(parents=True, exist_ok=True)
    log(f"  download {doc['doc_id']}  {doc['url']}")
    headers = {"User-Agent": user_agent(), "Accept-Encoding": "gzip, deflate"}
    response = httpx.get(doc["url"], headers=headers, timeout=60, follow_redirects=True)
    if response.status_code == 403:
        raise SystemExit(
            "SEC returned 403. Put SEC_USER_AGENT=\"Your Name your@email.com\" in .env "
            "(SEC blocks requests without a real name and email)."
        )
    response.raise_for_status()
    tmp = path.with_suffix(".part")
    tmp.write_bytes(response.content)
    tmp.replace(path)  # only a complete download ever counts as cached
    time.sleep(0.5)  # SEC allows 10 requests a second; stay far below
    return path


# ---------------------------------------------------------------- html -> text

def clean_cell(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\xa0", " ")).strip()


def table_to_text(table) -> str:
    """One line per row, cells joined by ' | '. Keeps numbers next to their labels."""
    lines = []
    for row in table.find_all("tr"):
        cells = [clean_cell(c.get_text(" ")) for c in row.find_all(["td", "th"])]
        cells = [c for c in cells if c]
        if not cells:
            continue
        line = " | ".join(cells)
        # Filings put "$", "%" and ")" in their own cells: glue them back on.
        line = re.sub(r"\$ \| ", "$", line)
        line = re.sub(r" \| (%|\))", r"\1", line)
        line = re.sub(r"\( \| ", "(", line)
        lines.append(line)
    return "\n".join(lines)


def html_to_text(html: str) -> str:
    soup = BeautifulSoup(html, "html.parser")

    # Inline XBRL keeps a hidden header full of machine-readable facts. Drop it,
    # plus anything else hidden, scripts and styles.
    for tag in soup.find_all(["ix:header", "script", "style", "head"]):
        tag.decompose()
    for tag in soup.find_all(style=re.compile(r"display\s*:\s*none", re.I)):
        tag.decompose()

    # Tables become plain rows. Innermost first, so nested tables survive.
    for table in reversed(soup.find_all("table")):
        table.replace_with(NavigableString("\n" + table_to_text(table) + "\n"))

    # Line breaks only at block elements: iXBRL wraps single numbers in inline
    # tags, and a newline there would split "$12.3 billion" across lines.
    for tag in soup.find_all(BLOCK_TAGS):
        tag.insert_after(NavigableString("\n"))

    text = soup.get_text("")
    text = text.replace("\xa0", " ").replace("’", "'").replace("‘", "'")
    text = text.replace("“", '"').replace("”", '"')

    lines = []
    for line in text.splitlines():
        line = re.sub(r"[ \t]+", " ", line).strip()
        if not line or is_page_furniture(line):
            continue
        lines.append(line)
    return "\n".join(lines)


def is_page_furniture(line: str) -> bool:
    """Page numbers, running headers and 'Table of Contents' links."""
    low = line.lower().replace("\u2019", "'")
    if low in {"table of contents", "index", "(continued)"} or low in RUNNING_HEADERS:
        return True
    if re.fullmatch(r"\d{1,3}", line):
        return True
    # e.g. "Goldman Sachs 2025 Form 10-K | 23", "24 | December 2025 Form 10-K"
    if re.fullmatch(r"(\d{1,3}\s*\|\s*)?[\w .&,]*form 10-[kq]( \| \d{1,3})?", low):
        return True
    return False


# ---------------------------------------------------------------- sections

def normalise(line: str) -> str:
    return re.sub(r"\s+", " ", line.lower().replace("’", "'")).strip(" .:|")


ITEM_PREFIX = r"(?:part\s+i{1,3}v?[\s.,:|\-]*)?(?:item\s+\d{1,2}[a-c]?[\s.:|\-–—]*)?"


def heading_pattern(title: str) -> re.Pattern:
    return re.compile(ITEM_PREFIX + re.escape(title) + r"\.?")


BOUNDARY_PATTERNS = [heading_pattern(t) for t in BOUNDARY_TITLES]


def is_boundary(line: str) -> bool:
    norm = normalise(line)
    return len(norm) < 160 and any(p.fullmatch(norm) for p in BOUNDARY_PATTERNS)


def candidate_spans(lines: list[str], title: str) -> list[tuple[int, int]]:
    """Every (start, end) where `title` is a heading and end is the next boundary."""
    pattern = heading_pattern(title)
    boundaries = [i for i, line in enumerate(lines) if is_boundary(line)]
    spans = []
    for i, line in enumerate(lines):
        if len(line) < 160 and pattern.fullmatch(normalise(line)):
            end = next((b for b in boundaries if b > i), len(lines))
            spans.append((i, end))
    return spans


def span_words(lines: list[str], span: tuple[int, int]) -> int:
    return sum(len(line.split()) for line in lines[span[0] + 1 : span[1]])


def split_sections(text: str, form: str) -> dict[str, dict]:
    """Pick, for each wanted section, the longest span in document order.

    The table of contents lists every heading too, but there each heading is
    followed almost immediately by the next one, so its span is tiny. The real
    section is the longest span, and the sections must come in filing order
    (Business, then Risk Factors, then MD&A).
    """
    lines = text.splitlines()
    sections = {}
    floor = -1
    for section_id, title in WANTED[form].items():
        spans = [s for s in candidate_spans(lines, title) if s[0] > floor]
        if not spans:
            log(f"    ! no heading found for {section_id} ({title!r})")
            continue
        start, end = max(spans, key=lambda s: span_words(lines, s))
        floor = start
        body = "\n".join(lines[start + 1 : end]).strip()
        sections[section_id] = {
            "heading": lines[start],
            "text": body,
            "words": len(body.split()),
            "first_line": lines[start + 1] if start + 1 < end else "",
            "last_line": lines[end - 1] if end - 1 > start else "",
            "ends_at": lines[end] if end < len(lines) else "<end of document>",
        }
    return sections


# ---------------------------------------------------------------- per file

def sections_path(doc: dict) -> Path:
    return CORPUS / doc["doc_id"] / "sections.json"


def same_heading(line: str, heading: str) -> bool:
    return normalise(line) == normalise(heading)


def trim(text: str, rules: dict) -> str:
    """Apply TRIM rules to one section's text (see TRIM above)."""
    lines = text.splitlines()
    for start, until in rules.get("skip", []):
        i = next((n for n, line in enumerate(lines) if same_heading(line, start)), None)
        if i is None:
            log(f"    ! skip: heading {start!r} not found, nothing skipped")
            continue
        j = next((n for n in range(i + 1, len(lines)) if same_heading(lines[n], until)), None)
        if j is None:
            log(f"    ! skip: heading {until!r} not found after {start!r}, nothing skipped")
            continue
        lines = lines[:i] + lines[j:]
    for heading in rules.get("stop_at", []):
        k = next((n for n, line in enumerate(lines) if same_heading(line, heading)), None)
        if k is None:
            log(f"    ! stop_at: heading {heading!r} not found, section kept whole")
            continue
        lines = lines[:k]
    return "\n".join(lines).strip()


def full_text(doc: dict, force: bool = False) -> str:
    """HTML -> text, the slow step, cached in corpus/<doc_id>/full.txt."""
    path = CORPUS / doc["doc_id"] / "full.txt"
    if path.is_file() and not force:
        text = path.read_text(encoding="utf-8")
    else:
        log(f"  parse    {doc['doc_id']}  (a 10 MB filing takes up to a minute)")
        html = raw_path(doc).read_text(encoding="utf-8", errors="replace")
        text = html_to_text(html)
        path.write_text(text, encoding="utf-8")
    # Cheap clean-up, rerun every time so rule changes apply to cached text.
    return "\n".join(line for line in text.splitlines() if not is_page_furniture(line))


def extract(doc: dict, force: bool = False) -> dict[str, dict]:
    """Cut the sections out of the cached text and save them. Takes seconds."""
    folder = CORPUS / doc["doc_id"]
    for old in folder.glob("item_*.txt"):  # sections we no longer use
        old.unlink()

    sections = split_sections(full_text(doc, force=force), doc["form"])
    for section_id, section in sections.items():
        rules = TRIM.get(doc["doc_id"], {}).get(section_id)
        if rules:
            section["text"] = trim(section["text"], rules)
            section["words"] = len(section["text"].split())
            section["trimmed"] = True
        (folder / f"{section_id}.txt").write_text(section["text"], encoding="utf-8")
    sections_path(doc).write_text(json.dumps(sections, indent=1, ensure_ascii=False), encoding="utf-8")
    return sections


def load_document(doc: dict, force: bool = False) -> dict[str, dict]:
    """Sections of one filing.

    With the filing on disk (raw.htm or full.txt) the sections are re-cut from
    it, which takes seconds. On a fresh clone only the committed section files
    exist, and those are used as they are: no download, no parsing.
    """
    folder = CORPUS / doc["doc_id"]
    have_source = raw_path(doc).is_file() or (folder / "full.txt").is_file()
    if not have_source and sections_path(doc).is_file() and not force:
        return json.loads(sections_path(doc).read_text(encoding="utf-8"))
    download(doc)
    return extract(doc, force=force)


# ================================================================ settings

def setting(name: str, default: str) -> str:
    """An environment variable, else a NAME=value line in .env, else default."""
    value = os.environ.get(name, "").strip()
    if not value and (ROOT / ".env").is_file():
        for line in (ROOT / ".env").read_text(encoding="utf-8").splitlines():
            key, sep, val = line.partition("=")
            if sep and key.strip() == name:
                value = val.strip().strip('"').strip("'")
    return value or default


INDEX = ROOT / "index"
CACHE_DB = INDEX / "embeddings.sqlite"
CHROMA_DIR = INDEX / "chroma"
CONFIG = INDEX / "config.json"

EMBED_MODEL = setting("EMBED_MODEL", "gemini-embedding-2")
EMBED_DIM = 768        # Matryoshka truncation: 4x smaller than 3072, little loss
EMBED_BATCH = 50       # texts per request; each text counts against the quota

# The two chunking designs compared in evaluate.py. Hybrid search (vectors +
# BM25 keywords) is a third design that reuses B's vectors at no embedding cost.
DESIGNS = {
    "A_fixed": {"chunker": "fixed", "size": 300, "overlap": 50},
    "B_structure": {"chunker": "structure", "target": 300, "max": 450, "min": 40},
}
DEFAULT_CONFIG = {"design": "B_structure", "k": 5, "hybrid": False}

SECTION_NAMES = {
    "item_1a_risk_factors": "Risk Factors",
    "item_7_mdna": "MD&A",
    "item_2_mdna": "MD&A",
    "document": "Document",
}
SECTION_SHORT = {"item_1a_risk_factors": "rf", "item_7_mdna": "mdna", "item_2_mdna": "mdna"}


def load_config() -> dict:
    config = dict(DEFAULT_CONFIG)
    if CONFIG.is_file():
        config.update(json.loads(CONFIG.read_text(encoding="utf-8")))
    return config


# ================================================================ headings

TABLE_CAPTION = re.compile(
    r"^(year ended|years ended|as of|three months|nine months|six months|average for|\$ in|"
    r"in the table|\(in millions|\(\$|in millions|in billions|for the year|at december|"
    r"\d{4}( versus | vs\.? )\d{4})", re.I)


def is_heading(line: str) -> bool:
    """A subsection title: short, no table pipes, no sentence punctuation."""
    words = line.split()
    return (
        0 < len(words) <= 10 and len(line) < 80 and "|" not in line
        and line[:1].isupper() and not re.search(r"[.;:,]$", line)
        and not TABLE_CAPTION.match(line) and not line.startswith("•")
        and not re.fullmatch(r"[\d\W]+", line)
    )


def is_risk_title(lines: list[str], i: int) -> bool:
    """A risk factor's title: one sentence, followed by a longer paragraph."""
    line = lines[i]
    words = len(line.split())
    if not (6 <= words <= 60) or not line.endswith(".") or line.startswith("•") or "|" in line:
        return False
    nxt = lines[i + 1] if i + 1 < len(lines) else ""
    return len(nxt.split()) > max(words, 40)


def heading_flags(section: str, lines: list[str]) -> list[bool]:
    if section == "item_1a_risk_factors":
        return [is_heading(l) or is_risk_title(lines, i) for i, l in enumerate(lines)]
    return [is_heading(l) for l in lines]


def heading_path(lines: list[str], flags: list[bool], i: int) -> str:
    """'Parent > Title' for line i: the nearest heading at or above it, plus
    the short heading above that if the nearest one is a risk-factor title."""
    j = next((n for n in range(i, -1, -1) if flags[n]), None)
    if j is None:
        return ""
    title = lines[j] if len(lines[j]) <= 140 else lines[j][:137] + "..."
    if is_heading(lines[j]):
        return title
    parent = next((lines[n] for n in range(j - 1, -1, -1) if flags[n] and is_heading(lines[n])), "")
    return f"{parent} > {title}" if parent else title


# ================================================================ chunking

def units_of(lines: list[str], size: int) -> list[tuple[int, str]]:
    """(line number, text) pieces. Lines longer than `size` words are cut into
    `size`-word pieces that keep their line number."""
    units = []
    for n, line in enumerate(lines, start=1):
        words = line.split()
        if len(words) <= size:
            units.append((n, line))
        else:
            for k in range(0, len(words), size):
                units.append((n, " ".join(words[k:k + size])))
    return units


YEAR_HEADER = re.compile(r"(\b(19|20)\d\d\b.*){2,}|^\$ in |^\(in millions|year ended|three months ended|nine months ended", re.I)


def table_header(lines: list[str], first: int, units: list[tuple[int, str]]) -> str:
    """The column-header row of a table the chunk starts inside.

    A chunk that begins mid-table holds rows like 'ROE | 16.6% | 14.0% | 9.4%'
    without saying which column is which year. The nearest header row above
    (one naming two years, or '$ in millions') is prepended as context; the
    chunk's line range is unchanged."""
    head = [u[1] for u in units[:3]]
    if not any("|" in h for h in head) or any(YEAR_HEADER.search(h) for h in head):
        return ""
    for i in range(first - 1, max(-1, first - 41), -1):
        if YEAR_HEADER.search(lines[i]):
            return lines[i]
    return ""


def make_chunk(doc: dict, section: str, units: list[tuple[int, str]], heading: str, number: int,
               lines: list[str] | None = None) -> dict:
    text = "\n".join(u[1] for u in units)
    header = table_header(lines, units[0][0] - 1, units) if lines else ""
    if header:
        text = f"(columns: {header})\n{text}"
    return {
        "id": f"{doc['doc_id']}#{SECTION_SHORT.get(section, section)}{number:03d}",
        "doc_id": doc["doc_id"],
        "company": doc.get("company", doc["doc_id"]),
        "form": doc.get("form", ""),
        "period": doc.get("period", ""),
        "url": doc.get("url", ""),
        "section": section,
        "section_name": SECTION_NAMES.get(section, section),
        "heading": heading,
        "start_line": units[0][0],
        "end_line": units[-1][0],
        "words": len(text.split()),
        "text": text,
    }


def chunk_fixed(doc: dict, section: str, text: str, size: int, overlap: int) -> list[dict]:
    """Design A: windows of about `size` words, `overlap` words shared with the
    previous window, cut at line boundaries (table rows stay whole)."""
    lines = text.splitlines()
    flags = heading_flags(section, lines)
    units = units_of(lines, size // 2)  # long paragraphs in halves, so windows stay near `size`
    chunks, start = [], 0
    while start < len(units):
        end, words = start, 0
        while end < len(units) and (words < size or end == start):
            words += len(units[end][1].split())
            end += 1
        piece = units[start:end]
        chunks.append(make_chunk(doc, section, piece, heading_path(lines, flags, piece[0][0] - 1), len(chunks), lines))
        if end >= len(units):
            break
        back, kept = end, 0
        while back - 1 > start and kept < overlap:
            back -= 1
            kept += len(units[back][1].split())
        start = back if back > start else end
    return chunks


def chunk_structure(doc: dict, section: str, text: str, target: int, max_words: int, min_words: int) -> list[dict]:
    """Design B: one chunk per subsection (MD&A) or per risk factor (Risk
    Factors). Tiny pieces merge into the next one; long ones split at line
    boundaries into ~`target`-word parts that keep the same heading."""
    lines = text.splitlines()
    flags = heading_flags(section, lines)
    units = units_of(lines, target)
    # 1. segments start at headings
    segments, current = [], []
    for unit in units:
        if flags[unit[0] - 1] and current and unit[1] == lines[unit[0] - 1]:
            segments.append(current)
            current = []
        current.append(unit)
    if current:
        segments.append(current)
    # 2. merge segments too small to stand alone (e.g. a title right above a subtitle)
    merged = []
    for seg in segments:
        if merged and sum(len(u[1].split()) for u in merged[-1]) < min_words:
            merged[-1] = merged[-1] + seg
        else:
            merged.append(seg)
    # 3. split long segments
    chunks = []
    for seg in merged:
        heading = heading_path(lines, flags, seg[0][0] - 1)
        total = sum(len(u[1].split()) for u in seg)
        if total <= max_words:
            chunks.append(make_chunk(doc, section, seg, heading, len(chunks), lines))
            continue
        parts = max(2, round(total / target))
        per = total / parts
        pieces, piece, words = [], [], 0
        for unit in seg:
            piece.append(unit)
            words += len(unit[1].split())
            if words >= per:
                pieces.append(piece)
                piece, words = [], 0
        if piece:
            if words < min_words and pieces:
                pieces[-1] = pieces[-1] + piece
            else:
                pieces.append(piece)
        for piece in pieces:
            chunks.append(make_chunk(doc, section, piece, heading, len(chunks), lines))
    return chunks


def chunk_sections(doc: dict, sections: dict[str, dict], design: str) -> list[dict]:
    spec = DESIGNS[design]
    chunks = []
    for section, data in sections.items():
        if section.startswith("_"):
            continue
        if spec["chunker"] == "fixed":
            part = chunk_fixed(doc, section, data["text"], spec["size"], spec["overlap"])
        else:
            part = chunk_structure(doc, section, data["text"], spec["target"], spec["max"], spec["min"])
        chunks.extend(part)
    return chunks


def embedding_text(chunk: dict) -> str:
    """What gets embedded: the document format gemini-embedding-2 expects,
    with firm, filing, section and heading as the title. Without the firm name
    'net revenues increased 12%' would look the same for all three banks."""
    year = chunk["period"][:4]
    title = " · ".join(x for x in (f"{chunk['company']} {chunk['form']} {year}".strip(),
                                   chunk["section_name"], chunk["heading"]) if x)
    return f"title: {title} | text: {chunk['text']}"


def query_text(query: str) -> str:
    return f"task: question answering | query: {query}"


# ================================================================ embeddings

class QuotaExhausted(RuntimeError):
    pass


class EmbeddingCache:
    """Vectors keyed by sha256(model, dimension, exact text), in SQLite.

    Each batch is committed as soon as it arrives, so a crash or the daily
    limit loses nothing, and the same text is never embedded twice: not on a
    rebuild, not when a document is removed and added again, not for a query
    that was asked before."""

    def __init__(self, path: Path = CACHE_DB):
        import sqlite3
        path.parent.mkdir(parents=True, exist_ok=True)
        # check_same_thread=False: the MCP server runs tools in worker threads
        self.db = sqlite3.connect(path, check_same_thread=False, timeout=30)
        self.db.execute("CREATE TABLE IF NOT EXISTS vectors (key TEXT PRIMARY KEY, vector BLOB NOT NULL)")
        self.db.commit()
        self.api_calls = 0      # texts actually sent to Gemini in this process
        import threading
        # the agent can search twice at once (one search per firm), and SQLite
        # refuses two threads on one connection at the same moment
        self.lock = threading.RLock()

    @staticmethod
    def key(text: str) -> str:
        import hashlib
        return hashlib.sha256(f"{EMBED_MODEL}|{EMBED_DIM}|{text}".encode("utf-8")).hexdigest()

    def lookup(self, texts: list[str]) -> dict[str, list[float]]:
        with self.lock:
            return self._lookup(texts)

    def _lookup(self, texts: list[str]) -> dict[str, list[float]]:
        import numpy as np
        found = {}
        keys = [self.key(t) for t in texts]
        for k in range(0, len(keys), 500):
            batch = keys[k:k + 500]
            rows = self.db.execute(
                f"SELECT key, vector FROM vectors WHERE key IN ({','.join('?' * len(batch))})", batch)
            for key, blob in rows:
                found[key] = np.frombuffer(blob, dtype=np.float32).tolist()
        return found

    def missing(self, texts: list[str]) -> list[str]:
        have = self.lookup(texts)
        seen, out = set(), []
        for t in texts:
            k = self.key(t)
            if k not in have and k not in seen:
                seen.add(k)
                out.append(t)
        return out

    def embed(self, texts: list[str], label: str = "") -> list[list[float]]:
        with self.lock:
            return self._embed(texts, label)

    def _embed(self, texts: list[str], label: str = "") -> list[list[float]]:
        import numpy as np
        todo = self.missing(texts)
        if todo:
            client = gemini_client()
            for k in range(0, len(todo), EMBED_BATCH):
                batch = todo[k:k + EMBED_BATCH]
                vectors = embed_batch(client, batch)
                self.db.executemany(
                    "INSERT OR REPLACE INTO vectors (key, vector) VALUES (?, ?)",
                    [(self.key(t), np.asarray(v, dtype=np.float32).tobytes()) for t, v in zip(batch, vectors)])
                self.db.commit()
                self.api_calls += len(batch)
                if label:
                    log(f"    {label}: embedded {min(k + EMBED_BATCH, len(todo))}/{len(todo)} new texts")
        have = self.lookup(texts)
        return [have[self.key(t)] for t in texts]


def gemini_client():
    from google import genai
    from api_key import load_api_key
    return genai.Client(api_key=load_api_key())


def embed_batch(client, batch: list[str]) -> list[list[float]]:
    """One API call for up to EMBED_BATCH texts, with retries on rate limits."""
    from google.genai import errors, types
    config = types.EmbedContentConfig(output_dimensionality=EMBED_DIM)
    for attempt in range(6):
        try:
            # One Content per text. A plain list of strings is merged into a single
            # multimodal input by gemini-embedding-2 and comes back as ONE vector.
            contents = [types.Content(role="user", parts=[types.Part(text=t)]) for t in batch]
            result = client.models.embed_content(model=EMBED_MODEL, contents=contents, config=config)
            vectors = [e.values for e in result.embeddings]
            if len(vectors) != len(batch):  # never silently mix up vectors
                raise RuntimeError(f"asked for {len(batch)} embeddings, got {len(vectors)}")
            return vectors
        except errors.APIError as error:
            message = str(error)
            if getattr(error, "code", None) == 429 or "RESOURCE_EXHAUSTED" in message:
                if re.search(r"per.?day|PerDay|daily", message, re.I):
                    raise QuotaExhausted(
                        "Daily embedding quota used up. Everything embedded so far is saved; "
                        "run the same command again after 09:00 (Spain) to continue.") from error
                wait = 20 * (attempt + 1)
                log(f"    rate limited, waiting {wait}s ({message[:120]})")
                time.sleep(wait)
                continue
            if getattr(error, "code", 0) and error.code >= 500 and attempt < 5:
                time.sleep(10 * (attempt + 1))
                continue
            raise
    raise QuotaExhausted("Still rate limited after several retries; run the command again later.")


# ================================================================ vector store

_CHROMA = None
import threading as _threading
_CHROMA_LOCK = _threading.Lock()


def chroma():
    global _CHROMA
    with _CHROMA_LOCK:
        return _chroma()


def _chroma():
    global _CHROMA
    if _CHROMA is None:
        import chromadb
        from chromadb.config import Settings
        CHROMA_DIR.mkdir(parents=True, exist_ok=True)
        _CHROMA = chromadb.PersistentClient(path=str(CHROMA_DIR), settings=Settings(anonymized_telemetry=False))
    return _CHROMA


def collection(design: str):
    return chroma().get_or_create_collection(name=design, metadata={"hnsw:space": "cosine"})


META_KEYS = ["doc_id", "company", "form", "period", "url", "section", "section_name",
             "heading", "start_line", "end_line", "words", "content_hash"]


def store(design: str, chunks: list[dict], vectors: list[list[float]]) -> None:
    col = collection(design)
    for k in range(0, len(chunks), 200):
        part = chunks[k:k + 200]
        col.upsert(
            ids=[c["id"] for c in part],
            embeddings=vectors[k:k + 200],
            documents=[c["text"] for c in part],
            metadatas=[{m: c.get(m, "") for m in META_KEYS} for c in part],
        )


def doc_ids_in(design: str) -> dict[str, str]:
    """doc_id -> content hash, for every document in a design's collection."""
    got = collection(design).get(include=["metadatas"])
    return {m["doc_id"]: m.get("content_hash", "") for m in got["metadatas"]}


def remove_document(doc_id: str, design: str | None = None) -> int:
    design = design or load_config()["design"]
    col = collection(design)
    ids = col.get(where={"doc_id": doc_id})["ids"]
    if ids:
        col.delete(ids=ids)
    _BM25.pop(design, None)
    return len(ids)


def content_hash(sections: dict[str, dict]) -> str:
    import hashlib
    joined = "\n".join(f"{k}\n{v['text']}" for k, v in sorted(sections.items()) if not k.startswith("_"))
    return hashlib.sha256(joined.encode("utf-8")).hexdigest()[:16]


def index_document(doc: dict, sections: dict[str, dict], design: str, cache: EmbeddingCache) -> dict:
    """Chunk, embed (cached) and store one document; replaces its old chunks."""
    chunks = chunk_sections(doc, sections, design)
    digest = content_hash(sections)
    for c in chunks:
        c["content_hash"] = digest
    before = cache.api_calls
    vectors = cache.embed([embedding_text(c) for c in chunks], label=f"{doc['doc_id']} / {design}")
    col = collection(design)
    current = col.get(where={"doc_id": doc["doc_id"]}, include=["metadatas"])
    old = set(current["ids"])
    unchanged = old == {c["id"] for c in chunks} and all(
        m.get("content_hash") == digest for m in current["metadatas"])
    if not unchanged:  # rewriting identical chunks only bloats the committed index
        store(design, chunks, vectors)
    stale = old - {c["id"] for c in chunks}
    if stale:
        col.delete(ids=sorted(stale))
    _BM25.pop(design, None)
    return {"doc_id": doc["doc_id"], "chunks": len(chunks), "newly_embedded": cache.api_calls - before,
            "words": sum(c["words"] for c in chunks), "content_hash": digest}


# ================================================================ search

_BM25: dict[str, dict] = {}


def tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+(?:[.,][0-9]+)*", text.lower())


def bm25_index(design: str) -> dict:
    """Keyword index over a design's chunks, built in memory from ChromaDB."""
    if design not in _BM25:
        import math
        from collections import Counter
        got = collection(design).get(include=["documents", "metadatas"])
        docs = [tokens(f"{m['company']} {m['section_name']} {m['heading']} {d}")
                for d, m in zip(got["documents"], got["metadatas"])]
        df = Counter(t for d in docs for t in set(d))
        n = max(len(docs), 1)
        _BM25[design] = {
            "ids": got["ids"], "metas": got["metadatas"], "texts": got["documents"],
            "tf": [Counter(d) for d in docs], "len": [len(d) for d in docs],
            "avg": sum(len(d) for d in docs) / n,
            "idf": {t: math.log(1 + (n - f + 0.5) / (f + 0.5)) for t, f in df.items()},
        }
    return _BM25[design]


def bm25_search(design: str, query: str, n: int, allowed: set[str] | None = None) -> list[str]:
    bm = bm25_index(design)
    q = set(tokens(query))
    scores = []
    for i, tf in enumerate(bm["tf"]):
        if allowed is not None and bm["metas"][i]["doc_id"] not in allowed:
            continue
        s = 0.0
        for t in q:
            if t in tf:
                f = tf[t]
                s += bm["idf"][t] * f * 2.2 / (f + 1.2 * (0.25 + 0.75 * bm["len"][i] / bm["avg"]))
        if s > 0:
            scores.append((s, bm["ids"][i]))
    return [i for _, i in sorted(scores, reverse=True)[:n]]


def search(query: str, design: str | None = None, k: int | None = None, hybrid: bool | None = None,
           doc_ids: list[str] | None = None, cache: EmbeddingCache | None = None) -> list[dict]:
    """Top-k chunks for a query. Used by server.py and evaluate.py alike."""
    config = load_config()
    design = design or config["design"]
    k = k or config["k"]
    hybrid = config["hybrid"] if hybrid is None else hybrid
    cache = cache or EmbeddingCache()
    col = collection(design)
    if col.count() == 0:
        raise RuntimeError(f"The index has no '{design}' collection yet. Run: uv run python main.py index")
    vector = cache.embed([query_text(query)])[0]
    where = {"doc_id": {"$in": doc_ids}} if doc_ids else None
    pool = max(k, 30) if hybrid else k
    res = col.query(query_embeddings=[vector], n_results=min(pool, col.count()), where=where,
                    include=["documents", "metadatas", "distances"])
    ids = res["ids"][0]
    found = {i: {"id": i, "text": d, **m, "score": round(1 - dist, 4)}
             for i, d, m, dist in zip(ids, res["documents"][0], res["metadatas"][0], res["distances"][0])}
    if not hybrid:
        return [found[i] for i in ids[:k]]
    keyword_ids = bm25_search(design, query, pool, set(doc_ids) if doc_ids else None)
    fused: dict[str, float] = {}
    for ranking in (ids, keyword_ids):  # reciprocal rank fusion
        for rank, i in enumerate(ranking):
            fused[i] = fused.get(i, 0.0) + 1.0 / (60 + rank)
    top = sorted(fused, key=fused.get, reverse=True)[:k]
    missing = [i for i in top if i not in found]
    if missing:
        got = col.get(ids=missing, include=["documents", "metadatas"])
        for i, d, m in zip(got["ids"], got["documents"], got["metadatas"]):
            found[i] = {"id": i, "text": d, **m, "score": None}
    return [found[i] for i in top]


def format_results(query: str, results: list[dict]) -> str:
    """Search results as the model sees them: a citation id and location per chunk."""
    if not results:
        return f"No passages found for: {query}"
    out = [f"{len(results)} passages for: {query}",
           "Cite a passage by its id in square brackets, e.g. [" + results[0]["id"] + "]."]
    for r in results:
        where = " · ".join(x for x in (f"{r['company']} {r['form']} {str(r['period'])[:4]}",
                                       r["section_name"], r["heading"]) if x)
        out.append(f"\n[{r['id']}] {where} · lines {r['start_line']}-{r['end_line']} of {r['section']}.txt")
        out.append(r["text"])
    return "\n".join(out)


# ================================================================ add a file

def resolve_inside_repo(path: str) -> Path:
    p = Path(path).expanduser()
    p = (ROOT / p).resolve() if not p.is_absolute() else p.resolve()
    if ROOT.resolve() not in p.parents:
        raise ValueError(f"{path} is outside the project folder; only files inside it can be added.")
    if not p.is_file():
        raise FileNotFoundError(f"No file at {path}.")
    return p


def sections_for_file(p: Path) -> tuple[dict, dict[str, dict]]:
    """(document metadata, sections) for any supported file.

    A filing listed in DOCUMENTS goes through the same extract-and-trim path
    as the corpus. Other HTML, text, Markdown and PDF files become one
    'document' section (PDF: one line per page break kept as a marker)."""
    for doc in DOCUMENTS:
        if p == raw_path(doc).resolve():
            return doc, extract(doc)
    doc_id = re.sub(r"[^A-Za-z0-9_]+", "_", p.stem).strip("_") or "document"
    doc = {"doc_id": doc_id, "company": doc_id, "form": p.suffix.lstrip(".").upper(), "period": "", "url": ""}
    suffix = p.suffix.lower()
    if suffix in {".htm", ".html"}:
        text = "\n".join(l for l in html_to_text(p.read_text(encoding="utf-8", errors="replace")).splitlines()
                         if not is_page_furniture(l))
    elif suffix == ".pdf":
        from pypdf import PdfReader
        pages = [page.extract_text() or "" for page in PdfReader(str(p)).pages]
        text = "\n".join(f"Page {n}\n{t.strip()}" for n, t in enumerate(pages, start=1))
    elif suffix in {".txt", ".md"}:
        text = p.read_text(encoding="utf-8", errors="replace")
    else:
        raise ValueError(f"Unsupported file type {suffix}; use .htm, .html, .pdf, .txt or .md.")
    text = "\n".join(l.strip() for l in text.splitlines() if l.strip())
    return doc, {"document": {"text": text, "words": len(text.split())}}


def add_file(path: str, design: str | None = None) -> dict:
    """Run one file through the pipeline into the active design's collection.

    Already indexed with the same content: nothing happens (no embeddings
    spent). Same document id with changed content: its old chunks are replaced."""
    design = design or load_config()["design"]
    p = resolve_inside_repo(path)
    doc, sections = sections_for_file(p)
    digest = content_hash(sections)
    existing = doc_ids_in(design).get(doc["doc_id"])
    if existing == digest:
        n = len(collection(design).get(where={"doc_id": doc["doc_id"]})["ids"])
        return {"status": "already indexed, unchanged", "doc_id": doc["doc_id"], "chunks": n, "newly_embedded": 0}
    result = index_document(doc, sections, design, EmbeddingCache())
    result["status"] = "replaced (content changed)" if existing else "added"
    return result


# ================================================================ build

def log(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


def corpus_documents(force: bool = False) -> list[tuple[dict, dict]]:
    CORPUS.mkdir(exist_ok=True)
    return [(doc, load_document(doc, force=force)) for doc in DOCUMENTS]


def build(dry_run: bool = False, force: bool = False) -> None:
    docs = corpus_documents(force=force)
    indexed = [(d, s) for d, s in docs if d["indexed"]]

    print(f"\n{'document':<17} {'section':<22} {'words':>8}")
    print("-" * 50)
    for doc, sections in docs:
        for sid, sec in sections.items():
            tag = "" if doc["indexed"] else "  (held back for add_document)"
            print(f"{doc['doc_id']:<17} {sid:<22} {sec['words']:>8,}{tag}")
    total = sum(s["words"] for d, secs in indexed for s in secs.values())
    print(f"Words in the index: {total:,}\n")

    plan = {}
    for design in DESIGNS:
        chunks = [c for d, s in indexed for c in chunk_sections(d, s, design)]
        plan[design] = chunks
        sizes = sorted(c["words"] for c in chunks)
        print(f"{design:<12} {len(chunks):>4} chunks, words per chunk: median {sizes[len(sizes)//2]}, "
              f"min {sizes[0]}, max {sizes[-1]}")

    if dry_run:
        cache = EmbeddingCache()
        need = sum(len(cache.missing([embedding_text(c) for c in plan[d]])) for d in DESIGNS)
        print(f"\nDry run: {need} chunks have no saved vector yet (that many embeddings to build).")
        return

    INDEX.mkdir(exist_ok=True)
    if not CONFIG.is_file():
        CONFIG.write_text(json.dumps(DEFAULT_CONFIG, indent=1), encoding="utf-8")
    cache = EmbeddingCache()
    active = load_config()["design"]
    order = [active] + [d for d in DESIGNS if d != active]  # the one the server uses first
    try:
        for design in order:
            for doc, sections in indexed:
                index_document(doc, sections, design, cache)
            print(f"{design:<12} stored: {collection(design).count()} chunks in ChromaDB")
    except QuotaExhausted as error:
        print(f"\nStopped: {error}")
        print(f"Embedded {cache.api_calls} new texts in this run; all saved.")
        sys.exit(2)
    print(f"\nEmbedded {cache.api_calls} new texts in this run (the rest came from index/embeddings.sqlite).")
    size = sum(p.stat().st_size for p in INDEX.rglob("*") if p.is_file()) / 1e6
    print(f"index/ is {size:.1f} MB. Server design: {load_config()}")


def main() -> None:
    build(dry_run="--dry-run" in sys.argv, force="--force" in sys.argv)


if __name__ == "__main__":
    main()
