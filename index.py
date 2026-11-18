"""
Assignment 3: build the index (`main.py index`).

Step 1 (this part): download the corpus into corpus/ (git-ignored), extract the
text page by page and clean it. Later steps add chunking and embedding.

The per-file steps are functions, so server.py's add-document tool can import
them instead of rewriting them.
"""

import logging
import re
from pathlib import Path

import httpx
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"

# pypdf prints harmless "Ignoring wrong pointing object" warnings for the Work Programme PDF.
logging.getLogger("pypdf").setLevel(logging.ERROR)

# The corpus. `source` is the short name used in chunk metadata and in eval/questions.csv.
DOCUMENTS = [
    {
        "source": "work_programme_2027",
        "title": "EIC Work Programme 2027",
        "url": "https://eic.ec.europa.eu/document/download/ed9ab103-1ffb-4d5f-a6ad-168ac3b36900_en?filename=EIC-2027-Work-Programme.pdf",
        "file": "EIC-2027-Work-Programme.pdf",
    },
    {
        "source": "accelerator_guide",
        "title": "EIC Accelerator Guide for Applicants v6.0",
        "url": "https://eic.ec.europa.eu/document/download/9d96fbf3-4d85-4ad0-9483-c77ce348111d_en?filename=EIC%20Accelerator%20guide%20for%20applicants_WP26.pdf",
        "file": "EIC Accelerator guide for applicants_WP26.pdf",
    },
    {
        "source": "investment_guidelines",
        "title": "EIC Fund Investment Guidelines (August 2026)",
        "url": "https://eic.ec.europa.eu/document/download/6df458e7-fa47-4ace-93fa-86099606bdb0_en?filename=EIC_Fund_Investment_2026_guidelines_f.pdf",
        "file": "EIC_Fund_Investment_2026_guidelines_f.pdf",
    },
]


def download(doc: dict) -> Path:
    """Download one document into corpus/, unless it is already there."""
    CORPUS_DIR.mkdir(exist_ok=True)
    path = CORPUS_DIR / doc["file"]
    if path.exists():
        return path
    print(f"Downloading {doc['title']} ...")
    response = httpx.get(doc["url"], follow_redirects=True, timeout=120)
    response.raise_for_status()
    path.write_bytes(response.content)
    return path


def extract_pages(path: Path) -> list[tuple[int, str]]:
    """Return (page number, raw text) for every page of a PDF. Page numbers start at 1."""
    reader = PdfReader(path)
    return [(i + 1, page.extract_text() or "") for i, page in enumerate(reader.pages)]


# Lines that repeat on every page and carry no content.
HEADER_PATTERNS = [
    re.compile(r"^EIC Accelerator \| Guide for applicants.*\| ?P\d+$"),  # header of the Guide
    re.compile(r"^\d{1,3}$"),  # a page number on its own line
]
TOC_LINE = re.compile(r"\.{5,}\s*\d+\s*$")  # "Introduction ........ 6" in a table of contents


def clean_page(text: str) -> str:
    """Clean the text of one page: drop headers, page numbers and table-of-contents lines,
    repair words that the PDF split with a stray space, and normalise whitespace."""
    lines = []
    for line in text.splitlines():
        line = line.strip()
        if not line or TOC_LINE.search(line):
            continue
        if any(p.match(line) for p in HEADER_PATTERNS):
            continue
        lines.append(line)
    text = "\n".join(lines)
    # "high -risk" -> "high-risk", "co -investment" -> "co-investment"
    text = re.sub(r"(\w) -(\w)", r"\1-\2", text)
    # A word broken across lines with a hyphen: "invest-\nment" -> "investment"
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)
    # Join the lines of a paragraph; keep text compact.
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r"\n+", " ", text)
    return text.strip()


def load_document(doc: dict) -> list[dict]:
    """Download, extract and clean one document. Returns one record per non-empty page."""
    path = download(doc)
    pages = []
    for page_number, raw in extract_pages(path):
        text = clean_page(raw)
        if len(text.split()) < 20:  # cover pages, blank pages, pure tables of contents
            continue
        pages.append({"source": doc["source"], "title": doc["title"], "page": page_number, "text": text})
    return pages


def main() -> None:
    total_words = 0
    for doc in DOCUMENTS:
        pages = load_document(doc)
        words = sum(len(p["text"].split()) for p in pages)
        total_words += words
        print(f"{doc['title']}: {len(pages)} pages kept, {words:,} words")
    print(f"Total: {total_words:,} words")


if __name__ == "__main__":
    main()
