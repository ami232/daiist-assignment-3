"""
Assignment 3: build the index (`main.py index`).

Corpus: the latest annual reports (10-K, fiscal 2025) of four US trucking and
logistics companies, downloaded from SEC EDGAR. We keep three sections of each:
Item 1 (Business), Item 1A (Risk Factors) and Item 7 (MD&A).

Steps, one function each, so server.py can reuse them for one new file:
    download_filing()   EDGAR -> corpus/<file>.htm   (cached, never downloaded twice)
    chunk_file()        file -> list of chunks with source and location metadata
    embed_and_store()   chunks -> Gemini vectors -> ChromaDB in index/
                        (skips chunks that already have a vector, saves batch by batch)

Everything this module prints goes to stderr, because server.py imports it and
stdout belongs to the MCP protocol there.
"""

import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path

import chromadb
import httpx
from bs4 import BeautifulSoup
from chromadb.config import Settings
from google import genai
from google.genai import types

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"
STATS_FILE = INDEX_DIR / "corpus_stats.json"

# ---------------------------------------------------------------- settings

# The filings, pinned by accession number so the corpus never changes under us.
# (ticker, company, form, accession number, primary document, period of report)
FILINGS = [
    ("ODFL", "Old Dominion Freight Line", "10-K", "0001193125-26-067161", "odfl-20251231.htm", "2025-12-31"),
    ("JBHT", "J.B. Hunt Transport Services", "10-K", "0001437749-26-005294", "jbht20251231_10k.htm", "2025-12-31"),
    ("SAIA", "Saia", "10-K", "0001193125-26-067030", "saia-20251231.htm", "2025-12-31"),
    ("KNX", "Knight-Swift Transportation", "10-K", "0001492691-26-000016", "knx-20251231.htm", "2025-12-31"),
]

# Newer quarterly reports (Q3 2026). Downloaded but NOT indexed: they are the
# documents we add later with the add_document tool, for the before/after test.
EXTRA_FILINGS = [
    ("ODFL", "Old Dominion Freight Line", "10-Q", "0000878927-26-000033", "odfl-20260930.htm", "2026-09-30"),
    ("JBHT", "J.B. Hunt Transport Services", "10-Q", "0001437749-26-033365", "jbht20260930_10q.htm", "2026-09-30"),
    ("SAIA", "Saia", "10-Q", "0001193125-26-437866", "saia-20260930.htm", "2026-09-30"),
    ("KNX", "Knight-Swift Transportation", "10-Q", "0001492691-26-000069", "knx-20260930.htm", "2026-09-30"),
]

CIK = {"ODFL": 878927, "JBHT": 728535, "SAIA": 1177702, "KNX": 1492691}

# Which sections we keep from each kind of filing ("item number": name).
SECTIONS = {
    "10-K": {"1": "Business", "1A": "Risk Factors", "7": "MD&A"},
    "10-Q": {"2": "MD&A"},  # in a 10-Q, MD&A is Part I, Item 2
}

CHUNK_WORDS = 150         # target words per chunk
MIN_CHUNK_WORDS = 40      # a smaller leftover is merged into the previous chunk
EMBEDDING_MODEL = "gemini-embedding-2"
EMBED_BATCH = 50          # texts per API call (each text still counts towards the daily limit)
COLLECTION = "filings"


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


# ---------------------------------------------------------------- 1. download

def sec_user_agent() -> str:
    """The SEC asks automated downloads to say who they are (name + email)."""
    return (os.environ.get("SEC_USER_AGENT")
            or read_env_value("SEC_USER_AGENT")
            or "DAIIST Assignment 3 student project contact@example.com")


def read_env_value(name: str) -> str | None:
    env = ROOT / ".env"
    if not env.is_file():
        return None
    for line in env.read_text(encoding="utf-8").splitlines():
        key, sep, value = line.partition("=")
        if sep and key.strip() == name:
            return value.strip().strip('"').strip("'") or None
    return None


def filing_path(ticker: str, form: str, period: str) -> Path:
    return CORPUS_DIR / f"{ticker}_{form}_{period}.htm"


def download_filing(ticker, company, form, accession, document, period) -> Path:
    """Download one filing from EDGAR into corpus/, unless it is already there."""
    path = filing_path(ticker, form, period)
    if path.exists():
        return path
    url = f"https://www.sec.gov/Archives/edgar/data/{CIK[ticker]}/{accession.replace('-', '')}/{document}"
    log(f"Downloading {ticker} {form} from {url}")
    response = httpx.get(url, headers={"User-Agent": sec_user_agent()}, timeout=60, follow_redirects=True)
    response.raise_for_status()
    CORPUS_DIR.mkdir(exist_ok=True)
    path.write_bytes(response.content)
    time.sleep(0.2)  # stay far below the SEC's limit of 10 requests a second
    return path


# ---------------------------------------------------------------- 2. extract

def html_to_lines(html: str) -> list[str]:
    """Turn an EDGAR filing into clean lines of text (one paragraph or table row each)."""
    soup = BeautifulSoup(html, "html.parser")

    # Hidden XBRL data and anything not shown on the page.
    for tag in soup.find_all(["ix:header", "script", "style"]):
        tag.decompose()
    for tag in soup.find_all(style=re.compile(r"display:\s*none", re.I)):
        tag.decompose()

    # Tables: one line per row, cells joined with " | ", empty spacer cells dropped.
    for table in soup.find_all("table"):
        rows = []
        for tr in table.find_all("tr"):
            cells = [td.get_text(" ", strip=True) for td in tr.find_all(["td", "th"])]
            cells = [c for c in cells if c]
            if cells:
                row = " | ".join(cells)
                row = re.sub(r"\$ \| ", "$", row)          # "$ | 1,234"  -> "$1,234"
                row = re.sub(r" \| (%|\))", r"\1", row)    # "12.5 | %"   -> "12.5%"
                rows.append(row)
        table.replace_with("\n" + "\n".join(rows) + "\n")

    # Paragraph-like tags end with a line break.
    for br in soup.find_all("br"):
        br.replace_with("\n")
    for tag in soup.find_all(["p", "div", "li", "h1", "h2", "h3", "h4", "h5", "h6"]):
        tag.append("\n")

    # Join inline pieces WITHOUT adding spaces. Filings write small-caps headings
    # as <span>B</span><span>USINESS</span>; get_text(" ") would give "B USINESS".
    text = soup.get_text("")
    text = text.replace("\xa0", " ").replace("​", "")

    lines = []
    for line in text.split("\n"):
        line = re.sub(r"\s+", " ", line).strip()
        if not line:
            continue
        if re.fullmatch(r"\d{1,3}|table of contents|.{0,60}\|\s*\d{1,3}", line, re.I):
            continue  # page numbers, "Table of Contents" links, page footers
        lines.append(line)

    # Running page headers: a short line printed on top of every page
    # (Knight-Swift repeats "KNIGHT-SWIFT TRANSPORTATION HOLDINGS INC." ~100 times).
    counts = {}
    for line in lines:
        counts[line] = counts.get(line, 0) + 1
    return [l for l in lines if not (counts[l] >= 8 and len(l.split()) <= 15)]


ITEM_HEADING = re.compile(r"^item\s*(\d{1,2}[a-c]?)\s*[.:\-–—]?\s*(.*)$", re.I)


def split_items(lines: list[str], wanted: dict[str, str]) -> dict[str, list[str]]:
    """Find the lines of each wanted Item.

    Every Item heading appears twice: once in the table of contents and once
    where the section really starts. We take, for each Item, the occurrence
    followed by the most text before the next Item heading.
    """
    headings = []  # (line number, item code)
    for i, line in enumerate(lines):
        match = ITEM_HEADING.match(line)
        if match and len(line.split()) <= 15:
            headings.append((i, match.group(1).upper()))

    sections = {}
    for code in wanted:
        best = []
        for n, (start, found) in enumerate(headings):
            if found != code:
                continue
            end = headings[n + 1][0] if n + 1 < len(headings) else len(lines)
            body = lines[start + 1:end]
            if sum(len(l.split()) for l in body) > sum(len(l.split()) for l in best):
                best = body
        sections[code] = best
    return sections


def is_subheading(line: str) -> bool:
    """A short line without a full stop, like 'Results of Operations' or 'Customers'."""
    words = line.split()
    return (
        1 <= len(words) <= 10
        and line[0].isupper()
        and not line.endswith((".", ",", ";", ":"))
        and "|" not in line
        and "(" not in line              # table labels like "Tractors (end of period)"
        and not re.search(r"\d", line)   # and "Years Ended December 31"
    )


# ---------------------------------------------------------------- 3. chunk

def read_filing_metadata(html: str, path: Path) -> dict:
    """Company, form and period from the filing's own XBRL tags (cover page)."""
    soup = BeautifulSoup(html[:2_000_000], "html.parser")

    def tag(name):
        found = soup.find(attrs={"name": name})
        return found.get_text(" ", strip=True) if found else None

    ticker = tag("dei:TradingSymbol")
    form = tag("dei:DocumentType")
    company = tag("dei:EntityRegistrantName")
    year = tag("dei:DocumentFiscalYearFocus")
    period = tag("dei:DocumentFiscalPeriodFocus")  # FY, Q1, Q2, Q3

    # Prefer our own short names for the companies we know.
    for t, name, *_ in FILINGS + EXTRA_FILINGS:
        if ticker and ticker.upper() == t:
            company = name
    if not (ticker and form and year):
        raise ValueError(f"{path.name}: could not read company, form and year from the filing's cover page.")

    label = f"{year}" if form == "10-K" else f"{year}-{period}"
    return {
        "ticker": ticker.upper(),
        "company": company,
        "form": form,
        "period": label,
        "source": f"{ticker.upper()} {form} {label}",  # e.g. "SAIA 10-K 2025"
    }


def make_chunk(meta: dict, item: str, item_name: str, heading: str, words: list[str], n: int) -> dict:
    text = " ".join(words)
    location = f"Item {item}" + (f" > {heading}" if heading else "")
    digest = hashlib.sha1(text.encode()).hexdigest()[:10]
    return {
        "id": f"{meta['source'].replace(' ', '_')}_item{item}_{n:04d}_{digest}",
        "text": text,
        "metadata": {
            "source": meta["source"],
            "company": meta["company"],
            "ticker": meta["ticker"],
            "form": meta["form"],
            "period": meta["period"],
            "item": f"Item {item}",
            "item_name": item_name,
            "heading": heading,
            "location": location,
            "words": len(words),
        },
    }


def chunk_section(meta: dict, item: str, item_name: str, lines: list[str]) -> list[dict]:
    """Cut one Item into ~CHUNK_WORDS-word chunks.

    A chunk never crosses a subheading, so each chunk belongs to one topic and
    its location says which one ("Item 7 > Results of Operations").
    """
    chunks, heading, buffer = [], "", []

    def flush():
        nonlocal buffer
        if buffer:
            if len(buffer) < MIN_CHUNK_WORDS and chunks and chunks[-1]["metadata"]["heading"] == heading:
                prev = chunks.pop()  # merge a small leftover into the previous chunk
                buffer = prev["text"].split() + buffer
            chunks.append(make_chunk(meta, item, item_name, heading, buffer, len(chunks)))
        buffer = []

    for line in lines:
        if is_subheading(line):
            flush()
            heading = line
            continue
        buffer.extend(line.split())
        while len(buffer) >= CHUNK_WORDS:
            # cut at the last sentence end inside the chunk, if there is one
            window = buffer[:CHUNK_WORDS]
            cut = max((i + 1 for i, w in enumerate(window) if w.endswith((".", "!", "?"))
                       and i + 1 >= CHUNK_WORDS // 2), default=CHUNK_WORDS)
            chunks.append(make_chunk(meta, item, item_name, heading, buffer[:cut], len(chunks)))
            buffer = buffer[cut:]
    flush()
    return chunks


def chunk_file(path: str | Path) -> list[dict]:
    """Extract, clean and chunk one filing. Each chunk has its source and location."""
    path = Path(path)
    html = path.read_text(encoding="utf-8", errors="ignore")
    meta = read_filing_metadata(html, path)
    wanted = SECTIONS.get(meta["form"])
    if not wanted:
        raise ValueError(f"{path.name} is a {meta['form']}; only {', '.join(SECTIONS)} are supported.")

    lines = html_to_lines(html)
    chunks = []
    for item, lines_in_item in split_items(lines, wanted).items():
        if not lines_in_item:
            log(f"  WARNING: {meta['source']}: Item {item} not found")
            continue
        chunks += chunk_section(meta, item, wanted[item], lines_in_item)
    return chunks


# ---------------------------------------------------------------- 4. embed and store

def get_collection():
    """The ChromaDB collection saved in index/chroma. We always pass our own Gemini vectors."""
    db = chromadb.PersistentClient(path=str(INDEX_DIR / "chroma"), settings=Settings(anonymized_telemetry=False))
    return db.get_or_create_collection(
        name=COLLECTION,
        configuration={"hnsw": {"space": "cosine"}},
        embedding_function=None,
    )


def document_text(chunk: dict) -> str:
    """What we embed: the chunk plus a title saying whose filing and which section.

    Without the company name in the title, a chunk about "our drivers" in
    Saia's filing and one in J.B. Hunt's would look almost the same.
    """
    m = chunk["metadata"]
    title = f"{m['company']} {m['form']} {m['period']}, {m['location']}"
    return f"title: {title} | text: {chunk['text']}"


def query_text(question: str) -> str:
    return f"task: search result | query: {question}"


_client = None


def gemini_client():
    """One client for the whole run. On a rate limit (429) or an overloaded
    server (5xx) it waits one minute and retries, up to 5 attempts in total."""
    global _client
    if _client is None:
        _client = genai.Client(
            api_key=load_api_key(),
            http_options=types.HttpOptions(
                retry_options=types.HttpRetryOptions(
                    attempts=5, initial_delay=60, max_delay=60, exp_base=1, jitter=0,
                    http_status_codes=[429, 500, 502, 503, 504],
                )
            ),
        )
    return _client


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed already-prefixed texts in one call. One vector per text."""
    result = gemini_client().models.embed_content(
        model=EMBEDDING_MODEL,
        # One Content per text: a plain list of strings is merged into a single vector.
        contents=[types.Content(parts=[types.Part(text=t)]) for t in texts],
    )
    vectors = [e.values for e in result.embeddings]
    if len(vectors) != len(texts):
        raise RuntimeError(f"Asked for {len(texts)} vectors, got {len(vectors)}.")
    return vectors


def embed_query(question: str) -> list[float]:
    return embed_texts([query_text(question)])[0]


def embed_and_store(chunks: list[dict], collection=None) -> int:
    """Embed the chunks that have no saved vector yet and store them. Returns how many were new."""
    collection = collection or get_collection()
    saved = set()
    for i in range(0, len(chunks), 500):
        saved |= set(collection.get(ids=[c["id"] for c in chunks[i:i + 500]], include=[])["ids"])
    todo = [c for c in chunks if c["id"] not in saved]
    if not todo:
        return 0

    for i in range(0, len(todo), EMBED_BATCH):
        batch = todo[i:i + EMBED_BATCH]
        try:
            vectors = embed_texts([document_text(c) for c in batch])
        except genai.errors.APIError as error:
            if error.code == 429:
                raise SystemExit(
                    f"Embedding quota reached after {i} new chunks. They are saved in index/.\n"
                    "If it is the daily limit, run `uv run python main.py index` again after\n"
                    "09:00 (Spain time) and it continues where it stopped."
                ) from error
            raise
        collection.add(  # saved to disk right away, so a crash loses nothing
            ids=[c["id"] for c in batch],
            embeddings=vectors,
            documents=[c["text"] for c in batch],
            metadatas=[c["metadata"] for c in batch],
        )
        log(f"  embedded {min(i + EMBED_BATCH, len(todo))}/{len(todo)}")
    return len(todo)


def source_of(path: str | Path) -> str:
    """The source label a file would get, e.g. 'SAIA 10-Q 2026-Q3'."""
    html = Path(path).read_text(encoding="utf-8", errors="ignore")
    return read_filing_metadata(html, Path(path))["source"]


# ---------------------------------------------------------------- main

def remove_document(source: str) -> int:
    """Retire one document from the index, e.g. 'KNX 10-Q 2026-Q3'. Returns how many chunks were removed.

    The RAG notebook (8.2): when documents change, old versions must be retired
    from the index, or search keeps returning them.
    """
    collection = get_collection()
    ids = collection.get(where={"source": source}, include=[])["ids"]
    if ids:
        collection.delete(ids=ids)
    return len(ids)


def main() -> None:
    if "--remove" in sys.argv:
        # uv run python index.py --remove "KNX 10-Q 2026-Q3"
        source = sys.argv[sys.argv.index("--remove") + 1]
        removed = remove_document(source)
        log(f"Removed {removed} chunks of {source!r}. Index holds {get_collection().count()} chunks.")
        return

    for filing in FILINGS + EXTRA_FILINGS:
        download_filing(*filing)

    all_chunks, stats = [], []
    for ticker, company, form, _, _, period in FILINGS:
        path = filing_path(ticker, form, period)
        chunks = chunk_file(path)
        words = sum(c["metadata"]["words"] for c in chunks)
        by_item = {}
        for c in chunks:
            by_item[c["metadata"]["item"]] = by_item.get(c["metadata"]["item"], 0) + c["metadata"]["words"]
        log(f"{chunks[0]['metadata']['source']}: {len(chunks)} chunks, {words:,} words {by_item}")
        stats.append({"source": chunks[0]["metadata"]["source"], "file": path.name, "chunks": len(chunks),
                      "words": words, "words_by_item": by_item})
        all_chunks += chunks

    total_words = sum(s["words"] for s in stats)
    log(f"Total: {len(all_chunks)} chunks, {total_words:,} words")
    INDEX_DIR.mkdir(exist_ok=True)
    STATS_FILE.write_text(json.dumps({"documents": stats, "chunks": len(all_chunks), "words": total_words}, indent=2))

    if "--no-embed" in sys.argv:
        return
    new = embed_and_store(all_chunks)
    log(f"Embedded {new} new chunks; {len(all_chunks) - new} already had a vector.")
    log(f"Index holds {get_collection().count()} chunks in total.")


if __name__ == "__main__":
    main()
