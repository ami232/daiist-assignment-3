"""
Assignment 3: build the index (`main.py index`).

Stage 1 (this file, for now): download the filings from SEC EDGAR, strip the
inline XBRL, turn tables into readable rows, and cut out the sections we use:
Item 1 Business, Item 1A Risk Factors, Item 7 MD&A (10-Q: MD&A only).

Each filing is downloaded once into corpus/ and parsed once; later runs read
the cached files and make no network calls. Delete a file in corpus/ (or pass
--force) to fetch or parse it again.

Run:  uv run python index.py            # download + extract + word counts
      uv run python index.py --force    # re-parse even if cached
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
        "item_1_business": "business",
        "item_1a_risk_factors": "risk factors",
        "item_7_mdna": "management's discussion and analysis of financial condition and results of operations",
    },
    "10-Q": {
        "item_2_mdna": "management's discussion and analysis of financial condition and results of operations",
    },
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
    low = line.lower()
    if low in {"table of contents", "index", "(continued)"}:
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


def extract(doc: dict, force: bool = False) -> dict[str, dict]:
    """Parse the cached HTML once and save the sections; later runs read the JSON."""
    out = sections_path(doc)
    if out.is_file() and not force:
        return json.loads(out.read_text(encoding="utf-8"))

    html = raw_path(doc).read_text(encoding="utf-8", errors="replace")
    log(f"  parse    {doc['doc_id']}  (a 10 MB filing takes up to a minute)")
    text = html_to_text(html)
    (CORPUS / doc["doc_id"] / "full.txt").write_text(text, encoding="utf-8")

    sections = split_sections(text, doc["form"])
    for section_id, section in sections.items():
        (CORPUS / doc["doc_id"] / f"{section_id}.txt").write_text(section["text"], encoding="utf-8")
    out.write_text(json.dumps(sections, indent=1, ensure_ascii=False), encoding="utf-8")
    return sections


def load_document(doc: dict, force: bool = False) -> dict[str, dict]:
    """Download (once) and extract (once). server.py's add_document can reuse this."""
    download(doc)
    return extract(doc, force=force)


# ---------------------------------------------------------------- report

def log(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


def report(results: list[tuple[dict, dict]]) -> None:
    print()
    print(f"{'document':<17} {'section':<22} {'words':>8}   heading found -> ends at")
    print("-" * 100)
    total_indexed = 0
    for doc, sections in results:
        for section_id, s in sections.items():
            print(f"{doc['doc_id']:<17} {section_id:<22} {s['words']:>8,}   "
                  f"{s['heading'][:30]!r} -> {s['ends_at'][:30]!r}")
            if doc["indexed"]:
                total_indexed += s["words"]
        missing = set(WANTED[doc["form"]]) - set(sections)
        for section_id in sorted(missing):
            print(f"{doc['doc_id']:<17} {section_id:<22} {'MISSING':>8}")
    print("-" * 100)
    print(f"Words in the initial index (10-Ks only): {total_indexed:,}")
    for size in (150, 300, 500):
        print(f"  at ~{size} words per chunk: ~{total_indexed // size:,} chunks to embed")
    print("\nCheck by eye: open corpus/<doc_id>/<section>.txt and look at the start and end.")


def main() -> None:
    force = "--force" in sys.argv
    CORPUS.mkdir(exist_ok=True)
    results = [(doc, load_document(doc, force=force)) for doc in DOCUMENTS]
    report(results)
    # Next stages (to build): chunk with source + location metadata, embed with
    # Gemini, save each vector as soon as it arrives, store in index/.


if __name__ == "__main__":
    main()
