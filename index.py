"""
Assignment 3: build the index (`main.py index`).

Corpus: the FY2025 Form 10-K annual reports of Tesla, Ford and General Motors,
downloaded from SEC EDGAR. Only Item 1 (Business), Item 1A (Risk Factors) and
Item 7 (MD&A) are kept: they hold what an analyst asks about, and they fit the
free embedding quota.

Pipeline, one function per step (server.py's add_document imports them):

    download_filing(filing)  -> raw .htm in corpus/
    chunk_file(path)         -> list of chunks with source and location metadata
                                (also writes the cleaned text to corpus/clean/)
    embed_and_store(chunks)  -> Gemini embeddings saved in ChromaDB under index/

Embeddings are saved batch by batch, and chunks whose id is already in the
index are never embedded again.

    uv run python index.py            # download, clean, chunk, embed, store
    uv run python index.py --dry-run  # everything except embedding

SEC EDGAR asks automated clients to name a contact in the User-Agent. Put
SEC_USER_AGENT="Your Name your@email" in .env (or the environment); without it a
generic client name is used.
"""

from __future__ import annotations

import os
import re
import sys
import time
import unicodedata
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
CLEAN_DIR = CORPUS_DIR / "clean"
INDEX_DIR = ROOT / "index"

COLLECTION = "tenk_fy2025"
EMBED_MODEL = "gemini-embedding-2"
EMBED_BATCH = 50
MAX_WORDS = 250  # upper bound of words per chunk body
MIN_WORDS = 50  # a section shorter than this is merged with the next one

ITEMS_KEPT = ["1", "1A", "7"]

FILINGS = [
    {
        "company": "Tesla",
        "source": "tesla_10k_fy2025",
        "cik": 1318605,
        "accession": "0001628280-26-003952",
        "document": "tsla-20251231.htm",
        "filed": "2026-01-29",
    },
    {
        "company": "Ford",
        "source": "ford_10k_fy2025",
        "cik": 37996,
        "accession": "0000037996-26-000015",
        "document": "f-20251231.htm",
        "filed": "2026-02-11",
    },
    {
        "company": "GM",
        "source": "gm_10k_fy2025",
        "cik": 1467858,
        "accession": "0001467858-26-000013",
        "document": "gm-20251231.htm",
        "filed": "2026-01-27",
    },
]


def log(*args) -> None:
    """Progress goes to stderr: server.py imports this module and stdout carries MCP."""
    print(*args, file=sys.stderr, flush=True)


# --------------------------------------------------------------------------- download


def sec_user_agent() -> str:
    """SEC_USER_AGENT from the environment or .env, else a generic client name."""
    value = os.environ.get("SEC_USER_AGENT", "").strip()
    env_file = ROOT / ".env"
    if not value and env_file.is_file():
        for line in env_file.read_text(encoding="utf-8").splitlines():
            name, _, rest = line.partition("=")
            if name.strip() == "SEC_USER_AGENT":
                value = rest.strip().strip('"').strip("'")
    return value or "daiist-assignment3 educational project"


def filing_url(filing: dict) -> str:
    folder = filing["accession"].replace("-", "")
    return f"https://www.sec.gov/Archives/edgar/data/{filing['cik']}/{folder}/{filing['document']}"


def download_filing(filing: dict, folder: Path = CORPUS_DIR) -> Path:
    """Download one 10-K into corpus/ unless it is already there."""
    import httpx

    path = folder / filing["document"]
    if path.exists() and path.stat().st_size > 100_000:
        return path
    folder.mkdir(parents=True, exist_ok=True)
    log(f"Downloading {filing_url(filing)}")
    response = httpx.get(filing_url(filing), headers={"User-Agent": sec_user_agent()}, timeout=60, follow_redirects=True)
    response.raise_for_status()
    if b"Undeclared Automated Tool" in response.content[:3000]:
        raise RuntimeError(
            "SEC EDGAR refused the download: it wants a contact in the User-Agent. "
            'Add SEC_USER_AGENT="Your Name your@email" to .env and run again.'
        )
    path.write_bytes(response.content)
    time.sleep(0.5)  # SEC fair-access policy: stay well under 10 requests a second
    return path


# --------------------------------------------------------------------------- extract

BLOCK_TAGS = ["p", "div", "li", "h1", "h2", "h3", "h4", "h5", "h6"]
TABLE = "\x00T"  # prefix that marks a line as a table row


def table_rows(table) -> list[str]:
    """One line per table row, cells joined by ' | ', with '%' and ')' glued back on."""
    rows = []
    for tr in table.find_all("tr"):
        cells: list[str] = []
        for cell in tr.find_all(["td", "th"]):
            text = " ".join(cell.get_text(" ", strip=True).split())
            if not text or text == "$":
                continue
            if cells and text in {"%", ")", "%)", "pts", "ppts"}:
                cells[-1] += text
            else:
                cells.append(text)
        if cells:
            rows.append(" | ".join(cells))
    return rows


def html_to_lines(path: Path) -> list[str]:
    """Visible text of an EDGAR .htm file, one line per paragraph or table row."""
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(path.read_bytes(), "html.parser")
    for tag in soup(["script", "style", "head"]):
        tag.decompose()
    for tag in soup.find_all(style=re.compile(r"display:\s*none", re.I)):
        tag.decompose()  # the hidden inline-XBRL header
    for table in soup.find_all("table"):
        if table.find_parent("table"):
            continue
        holder = soup.new_tag("div")
        for row in table_rows(table):
            line = soup.new_tag("div")
            line.string = TABLE + row
            holder.append(line)
        table.replace_with(holder)

    lines = []
    for block in soup.find_all(BLOCK_TAGS):
        if block.find(BLOCK_TAGS):
            continue  # only leaf blocks, so no text is read twice
        text = block.get_text("")
        if not text.strip():
            continue
        lead = bold_lead_in(block)
        if lead and len(lead.split()) <= 12 and text.strip() != lead:
            # "Overview Our vision is..." -> a heading line, then the paragraph
            lines.append(lead)
            text = text.strip()[len(lead) :]
        lines.append(text)
    return lines


BOLD = re.compile(r"font-weight:\s*(bold|[6-9]00)", re.I)


def bold_lead_in(block) -> str:
    """Text of the bold spans a paragraph starts with (an inline heading), or ''."""
    lead = ""
    for child in block.children:
        text = child.get_text("") if hasattr(child, "get_text") else str(child)
        if not text.strip():
            lead += text
            continue
        if hasattr(child, "get") and BOLD.search(child.get("style", "")):
            lead += text
        else:
            break
    return lead.strip()


# --------------------------------------------------------------------------- clean

QUOTES = str.maketrans(
    {"’": "'", "‘": "'", "“": '"', "”": '"', "–": "-", "—": "-", "◦": "•"}
)
PAGE_NUMBER = re.compile(r"^\d{1,3}$")
RUNNING_HEADER = re.compile(r"^item\s*\d+[a-c]?\..*\(continued\)$", re.I)
DROP = re.compile(r"^(table of contents|_{3,}|general motors company and subsidiaries)$", re.I)
BULLET = {"•", "●", "▪", "-"}


def normalise(text: str) -> str:
    text = unicodedata.normalize("NFKC", text).translate(QUOTES)
    return " ".join(text.split())


def clean_lines(raw: list[str]) -> list[dict]:
    """Drop page furniture and give every remaining line its page number.

    Returns [{"text", "page", "table"}]. A page number printed at the bottom of
    a page closes that page, so the lines before it get that number.
    """
    entries: list[dict] = []
    open_page: list[dict] = []
    last_page = 0
    pending_bullet = False

    for line in raw:
        table = line.startswith(TABLE)
        text = normalise(line.removeprefix(TABLE))
        if not text:
            continue
        if not table and PAGE_NUMBER.match(text):
            last_page = int(text)
            for entry in open_page:
                entry["page"] = last_page
            open_page = []
            continue
        if DROP.match(text) or RUNNING_HEADER.match(text):
            continue
        if not table and text in BULLET:
            pending_bullet = True
            continue
        if pending_bullet:
            text, pending_bullet = f"• {text}", False

        previous = entries[-1] if entries else None
        continues_sentence = (
            previous is not None
            and not table
            and not previous["table"]
            and text[0].islower()
            and not previous["text"].endswith((".", ":", ";", "?", "!"))
        )
        if continues_sentence:  # a paragraph split by a page break
            previous["text"] += " " + text
            continue

        entry = {"text": text, "page": None, "table": table}
        entries.append(entry)
        open_page.append(entry)

    for entry in open_page:
        entry["page"] = last_page + 1
    return entries


# --------------------------------------------------------------------------- structure

ITEM_HEADING = re.compile(r"^item\s*(\d+[a-c]?)\b\.?\s*(.*)$", re.I)


def find_items(entries: list[dict]) -> dict[str, tuple[int, int, str]]:
    """Locate each kept Item: {"1A": (start, end, title)}.

    The table of contents repeats every heading, so for each Item we keep the
    occurrence followed by the most text before the next Item heading.
    """
    headings = []
    for i, entry in enumerate(entries):
        match = ITEM_HEADING.match(entry["text"])
        if match and len(entry["text"]) < 160:
            headings.append((i, match.group(1).upper(), match.group(2)))

    items: dict[str, tuple] = {}
    for n, (start, item, rest) in enumerate(headings):
        if item not in ITEMS_KEPT:
            continue
        end = next((h[0] for h in headings[n + 1 :] if h[1] != item), len(entries))
        words = sum(len(e["text"].split()) for e in entries[start + 1 : end])
        if item not in items or words > items[item][3]:
            title = rest.split(" | ")[0].strip(" .") or entries[start + 1]["text"].split(" | ")[0].strip(" .")
            items[item] = (start, end, title, words)
    return {k: (s, e, t) for k, (s, e, t, _) in items.items()}


def is_heading(entry: dict) -> bool:
    """A short, title-cased line that is not a table row: a section heading."""
    text = entry["text"]
    words = text.split()
    if entry["table"] or not words or len(words) > 12:
        return False
    if not text[0].isupper() or text.endswith((",", ";", ":")) or text.startswith("•"):
        return False
    if text.endswith(".") and len(words) > 8:
        return False
    long_words = [w for w in words if len(w) > 3]
    if not long_words:
        return len(words) <= 3
    return sum(w[0].isupper() for w in long_words) / len(long_words) >= 0.75


# --------------------------------------------------------------------------- chunk


def split_long(text: str, limit: int = MAX_WORDS) -> list[str]:
    """Split a paragraph longer than `limit` words at sentence ends (or rows, for tables)."""
    if "\n" in text:
        units, joiner = text.split("\n"), "\n"
    else:
        units, joiner = re.split(r"(?<=[.!?])\s+(?=[A-Z(•])", text), " "
        # a "sentence" that is still too long (a list joined by semicolons): cut at
        # semicolons, then, as a last resort, every `limit` words
        units = [part for unit in units for part in re.split(r"(?<=;)\s+", unit)]
        units = [
            " ".join(words[i : i + limit])
            for unit in units
            for words in [unit.split()]
            for i in range(0, len(words), limit)
        ]
    pieces, current = [], []
    for unit in units:
        if current and len(joiner.join(current + [unit]).split()) > limit:
            pieces.append(joiner.join(current))
            current = []
        current.append(unit)
    if current:
        pieces.append(joiner.join(current))
    return pieces


def chunk_item(entries: list[dict], meta: dict, item: str, title: str) -> list[dict]:
    """Structure-based chunks: one section (heading) at a time, at most MAX_WORDS words each."""
    chunks: list[dict] = []
    section = title
    buffer: list[tuple[str, int]] = []  # (paragraph, page)

    def words_in_buffer() -> int:
        return sum(len(p.split()) for p, _ in buffer)

    def flush() -> None:
        if not buffer:
            return
        body = "\n".join(p for p, _ in buffer)
        pages = [p for _, p in buffer]
        page_start, page_end = min(pages), max(pages)
        header = f"{meta['company']} 10-K FY{meta['fiscal_year']} | Item {item}. {title} | {section}"
        chunks.append(
            {
                "id": f"{meta['source']}:item{item}:{len(chunks) + 1:03d}",
                "text": f"{header}\n{body}",
                "metadata": {
                    "source": meta["source"],
                    "company": meta["company"],
                    "fiscal_year": meta["fiscal_year"],
                    "item": f"Item {item}",
                    "item_title": title,
                    "section": section,
                    "page_start": page_start,
                    "page_end": page_end,
                    "location": f"Item {item}, p. {page_start}" + (f"-{page_end}" if page_end != page_start else ""),
                    "words": len(body.split()),
                    "url": meta.get("url", ""),
                },
            }
        )
        buffer.clear()

    # consecutive table rows become one paragraph
    paragraphs: list[list] = []
    for entry in entries:
        kind = "table" if entry["table"] else ("heading" if is_heading(entry) else "text")
        if kind == "table" and paragraphs and paragraphs[-1][2] == "table":
            paragraphs[-1][0] += "\n" + entry["text"]
        else:
            paragraphs.append([entry["text"], entry["page"], kind])

    for text, page, kind in paragraphs:
        if kind == "heading":
            heading = text.rstrip(".")
            if words_in_buffer() >= MIN_WORDS:
                flush()
                section = heading
            elif buffer:  # too little text so far: keep it with the next section
                section = f"{section} / {heading}"
            else:
                section = heading
            continue
        for piece in split_long(text):
            if buffer and words_in_buffer() + len(piece.split()) > MAX_WORDS:
                flush()
            buffer.append((piece, page))
    flush()
    return chunks


def write_clean_text(meta: dict, entries: list[dict], items: dict) -> Path:
    """Readable cleaned copy of the kept Items, with headings and page markers."""
    CLEAN_DIR.mkdir(parents=True, exist_ok=True)
    out = [f"# {meta['company']} Form 10-K, fiscal year {meta['fiscal_year']}", f"Source: {meta.get('url', '')}", ""]
    for item in ITEMS_KEPT:
        if item not in items:
            continue
        start, end, title = items[item]
        out += [f"## Item {item}. {title}", ""]
        page = None
        for entry in entries[start + 1 : end]:
            if entry["page"] != page:
                page = entry["page"]
                out += [f"[p. {page}]"]
            out += [("### " if is_heading(entry) else "") + entry["text"]]
        out += [""]
    path = CLEAN_DIR / f"{meta['source']}.md"
    path.write_text("\n".join(out), encoding="utf-8")
    return path


def meta_for(path: Path, entries: list[dict], company: str | None = None) -> dict:
    """Metadata for a file: from FILINGS if it is one of ours, else from the 10-K cover page.

    The cover page names the company on the line before "(Exact name of
    registrant ...)"; the fiscal year comes from the EDGAR file name (xxx-20251231.htm).
    """
    for filing in FILINGS:
        if path.name == filing["document"]:
            return {**filing, "fiscal_year": 2025, "url": filing_url(filing)}
    if not company:
        for i, entry in enumerate(entries[:200]):
            if "exact name of registrant" in entry["text"].lower() and i > 0:
                company = entries[i - 1]["text"].split(",")[0].split()[0]
                break
    company = company or path.stem
    year = re.search(r"(20\d\d)\d{4}", path.stem)
    fiscal_year = int(year.group(1)) if year else 0
    slug = re.sub(r"[^a-z0-9]+", "_", company.lower()).strip("_")
    return {"company": company, "source": f"{slug}_10k_fy{fiscal_year}", "fiscal_year": fiscal_year, "url": str(path)}


def chunk_file(path: str | Path, company: str | None = None) -> list[dict]:
    """Extract, clean and chunk one 10-K .htm file, keeping Items 1, 1A and 7.

    Every chunk: {"id", "text", "metadata"} with source, company, item, section,
    pages and a `location` string ("Item 1A, p. 15").
    """
    path = Path(path)
    if path.suffix.lower() not in {".htm", ".html"}:
        raise ValueError(f"{path.name}: only EDGAR .htm/.html filings are supported")
    entries = clean_lines(html_to_lines(path))
    meta = meta_for(path, entries, company)
    items = find_items(entries)
    if not items:
        raise ValueError(f"{path.name}: no Item 1, 1A or 7 heading found; is it a 10-K?")
    write_clean_text(meta, entries, items)
    chunks = []
    for item in ITEMS_KEPT:
        if item in items:
            start, end, title = items[item]
            chunks += chunk_item(entries[start + 1 : end], meta, item, title)
    return chunks


# --------------------------------------------------------------------------- embed and store


def get_collection():
    import chromadb

    client = chromadb.PersistentClient(path=str(INDEX_DIR))
    return client.get_or_create_collection(COLLECTION, metadata={"hnsw:space": "cosine"})


def embed_texts(texts: list[str], task_type: str = "RETRIEVAL_DOCUMENT") -> list[list[float]]:
    """Gemini embeddings for a batch of texts, retrying when the rate limit hits."""
    from google import genai
    from google.genai import types

    from api_key import load_api_key

    client = genai.Client(api_key=load_api_key())
    for attempt in range(6):
        try:
            # gemini-embedding-2 is multimodal: a plain list of strings is read as ONE
            # input (one vector), so each text goes in its own Content
            contents = [types.Content(parts=[types.Part(text=t)]) for t in texts]
            result = client.models.embed_content(
                model=EMBED_MODEL, contents=contents, config=types.EmbedContentConfig(task_type=task_type)
            )
            if len(result.embeddings) != len(texts):
                raise RuntimeError(f"Asked for {len(texts)} embeddings, got {len(result.embeddings)}")
            return [e.values for e in result.embeddings]
        except Exception as error:  # noqa: BLE001
            if "429" not in str(error) and "RESOURCE_EXHAUSTED" not in str(error):
                raise
            wait = 20 * (attempt + 1)
            log(f"Rate limited (free tier: 100 embeddings a minute); waiting {wait}s")
            time.sleep(wait)
    raise RuntimeError("Embedding quota exhausted; run again later, saved vectors are kept.")


def embed_and_store(chunks: list[dict], collection=None) -> int:
    """Embed the chunks not yet in the index and save each batch as soon as it returns."""
    collection = collection or get_collection()
    ids = [c["id"] for c in chunks]
    existing = set(collection.get(ids=ids, include=[])["ids"]) if ids else set()
    todo = [c for c in chunks if c["id"] not in existing]
    log(f"{len(chunks)} chunks, {len(existing)} already embedded, {len(todo)} to embed")
    for i in range(0, len(todo), EMBED_BATCH):
        batch = todo[i : i + EMBED_BATCH]
        vectors = embed_texts([c["text"] for c in batch])
        collection.add(
            ids=[c["id"] for c in batch],
            embeddings=vectors,
            documents=[c["text"] for c in batch],
            metadatas=[c["metadata"] for c in batch],
        )
        log(f"  saved {i + len(batch)}/{len(todo)}")
    return len(todo)


# --------------------------------------------------------------------------- main


def build_chunks() -> list[dict]:
    chunks = []
    collection = get_collection()
    for filing in FILINGS:
        path = CORPUS_DIR / filing["document"]
        if not path.exists() and collection.get(where={"source": filing["source"]}, limit=1, include=[])["ids"]:
            # fresh clone: the committed index already holds this report, so there
            # is nothing to embed and no need to download it again
            log(f"{filing['company']}: already in the committed index; not downloaded")
            continue
        path = download_filing(filing)
        file_chunks = chunk_file(path)
        words = sum(c["metadata"]["words"] for c in file_chunks)
        log(f"{filing['company']}: {len(file_chunks)} chunks, {words} words")
        chunks += file_chunks
    return chunks


def main() -> None:
    chunks = build_chunks()
    log(f"Total: {len(chunks)} chunks, {sum(c['metadata']['words'] for c in chunks)} words")
    if "--dry-run" in sys.argv:
        return
    embed_and_store(chunks)
    log(f"Index in {INDEX_DIR}: {get_collection().count()} chunks")


if __name__ == "__main__":
    main()
