"""
Assignment 3: build the index (`main.py index`).

Corpus: EU food-labelling law and the Commission's official guidance on it.
Pipeline per document:  download -> extract lines -> clean -> sections -> chunks
                        -> embed with Gemini -> store in ChromaDB (index/).

Two chunking designs are built so they can be compared in evaluate.py:
  * "structure": one chunk per article / annex / guidance section (long ones split)
  * "fixed":     fixed windows of 200 words with 40 words of overlap

Each vector is saved as soon as it arrives, and only chunks without a saved
vector are embedded, so a crash or the daily quota never loses work.

server.py imports `chunk_file`, `embed_and_store`, `embed_query`, `search`.

Usage:
    uv run python index.py              # download, chunk and embed both designs
    uv run python index.py --no-embed   # only download + chunk, print stats (free)
    uv run python index.py --design structure
"""

import argparse
import hashlib
import re
import sys
import time
from pathlib import Path

import chromadb
import httpx
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768          # smaller than the 3072 default: keeps index/ well under 90 MB
BATCH_SIZE = 20          # texts per embedding request

# Chunking parameters
STRUCT_MAX_WORDS = 350   # sections longer than this are split...
STRUCT_WINDOW = 300      # ...into windows of this many words
STRUCT_OVERLAP = 50
FIXED_WINDOW = 200
FIXED_OVERLAP = 40

DESIGNS = ["structure", "fixed"]
CHOSEN_DESIGN = "structure"   # chosen from eval/summary.md: higher hit rate at k = 1, 3, 5

EURLEX = "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:{}"

# source = short id used in citations and in eval/questions.csv `expected_source`
DOCUMENTS = [
    {"source": "REG_1169_2011", "kind": "regulation", "celex": "32011R1169",
     "title": "Regulation (EU) No 1169/2011 on the provision of food information to consumers"},
    {"source": "REG_1924_2006", "kind": "regulation", "celex": "32006R1924",
     "title": "Regulation (EC) No 1924/2006 on nutrition and health claims made on foods"},
    {"source": "REG_432_2012", "kind": "regulation", "celex": "32012R0432",
     "title": "Commission Regulation (EU) No 432/2012 establishing a list of permitted health claims made on foods"},
    {"source": "QA_NOTICE_2018", "kind": "notice", "celex": "52018XC0608(01)",
     "title": "Commission Notice on questions and answers on the application of Regulation (EU) No 1169/2011 (2018/C 196/01)"},
    {"source": "ALLERGEN_NOTICE_2017", "kind": "notice", "celex": "52017XC1213(01)",
     "title": "Commission Notice on information on substances or products causing allergies or intolerances (2017/C 428/01)"},
    {"source": "QUID_NOTICE_2017", "kind": "notice", "celex": "52017XC1121(01)",
     "title": "Commission Notice on the application of the principle of quantitative ingredients declaration (QUID) (2017/C 393/05)"},
]


def log(*args) -> None:
    """Log to stderr: server.py imports this module and stdout carries MCP."""
    print(*args, file=sys.stderr, flush=True)


# ---------------------------------------------------------------- download

def download(doc: dict) -> Path:
    """Fetch a document from EUR-Lex into corpus/, unless it is already there."""
    CORPUS_DIR.mkdir(exist_ok=True)
    path = CORPUS_DIR / f"{doc['source']}.html"
    if path.exists() and path.stat().st_size > 10_000:
        return path
    url = EURLEX.format(doc["celex"])
    log(f"Downloading {doc['source']} from {url}")
    headers = {"User-Agent": "Mozilla/5.0 (student project; assignment 3)", "Accept-Language": "en"}
    response = httpx.get(url, headers=headers, follow_redirects=True, timeout=60)
    response.raise_for_status()
    if len(response.text) < 10_000:
        raise RuntimeError(
            f"EUR-Lex did not return the document for {doc['source']} (maybe a bot check).\n"
            f"Open {url} in your browser and save the page as {path}, then run again."
        )
    path.write_text(response.text, encoding="utf-8")
    return path


# ---------------------------------------------------------------- extraction + cleaning

NOISE_CLASSES = {"note", "oj-note", "hd-date", "hd-lg", "hd-ti", "hd-oj", "arrow", "modref"}
CHAPTER_RE = re.compile(r"^(CHAPTER|SECTION|TITLE)\s+[IVXLC\d]+$")


def html_to_lines(html: str) -> list[str]:
    """Turn EUR-Lex HTML into clean text lines, one per paragraph or table row.

    Extraction problem fixed here: EUR-Lex lays out lettered points such as
    "(a) the name of the food" as two-cell table rows. A plain get_text() puts
    "(a)" and its text on separate lines, so the letter loses its content.
    We merge every table row into one line before reading the paragraphs.
    """
    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "head", "nav"]):
        tag.decompose()
    for tag in soup.find_all(class_=lambda c: c and set(c.split() if isinstance(c, str) else c) & NOISE_CLASSES):
        tag.decompose()  # footnotes and page headers
    for tag in soup.find_all("a", href=lambda h: h and h.startswith("#ntr")):
        tag.decompose()  # footnote markers like "(1)" in old-format documents
    for tag in soup.find_all("span", class_="oj-note-tag"):
        tag.decompose()  # footnote markers in new-format documents

    for row in reversed(soup.find_all("tr")):  # innermost rows first
        cells = [c.get_text(" ", strip=True) for c in row.find_all(["td", "th"], recursive=False)]
        new = soup.new_tag("p")
        new.string = " ".join(c for c in cells if c)
        row.replace_with(new)

    lines, previous = [], None
    for block in soup.find_all(["p", "h1", "h2", "h3", "h4", "li"]):
        if block.find(["p", "li"]):  # a container; its children are read on their own
            continue
        text = clean(block.get_text(" ", strip=True))
        if text and text != previous:
            lines.append(text)
            previous = text
    return lines


def clean(text: str) -> str:
    text = text.replace("\xa0", " ").replace(" ", " ").replace(" ", " ")
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s+([,.;:)])", r"\1", text)
    return text


# ---------------------------------------------------------------- sections

ARTICLE_RE = re.compile(r"^Article\s+(\d+[a-z]?)$")
ANNEX_RE = re.compile(r"^ANNEX(?:\s+([IVXLC]+))?\b")
NOTICE_HEAD_RE = re.compile(r"^(\d+(?:\.\d+)*)\.?\s+(.+)$")
TOC_ENTRY_RE = re.compile(r"^\d+(?:\.\d+)*\.?\s+.+\s\d{1,3}$")  # "2.1. Legibility 4"


def is_notice_heading(line: str) -> re.Match | None:
    """A numbered heading or question in Commission guidance ("2.1. Legibility",
    "3.2.4. Can ...?"). Numbered paragraphs are long and end with a full stop."""
    m = NOTICE_HEAD_RE.match(line)
    if not m:
        return None
    words = len(line.split())
    if line.endswith("?") and words <= 80:
        return m
    if words <= 30 and not line.endswith((".", ";", ",", ":")):
        return m
    return None


def lines_to_sections(lines: list[str], kind: str) -> list[dict]:
    """Group lines into sections, each with a `location` used for citations."""
    sections = [{"location": "Preamble", "heading": "", "lines": []}]
    started = False  # notices: headings count only from the first "1." onwards
    i = 0
    while i < len(lines):
        line = lines[i]
        if kind == "regulation":
            if CHAPTER_RE.match(line):
                i += 2  # chapter number + its title are layout, not content
                continue
            art = ARTICLE_RE.match(line)
            annex = ANNEX_RE.match(line) if len(line.split()) <= 6 else None
            if art or annex:
                if art:
                    location = f"Article {art.group(1)}"
                else:
                    location = f"Annex {annex.group(1)}" if annex.group(1) else "Annex"
                heading = lines[i + 1] if i + 1 < len(lines) and len(lines[i + 1].split()) <= 20 else ""
                sections.append({"location": location, "heading": heading, "lines": []})
                i += 2 if heading else 1
                continue
        else:
            # Skip the table of contents: its entries look like headings but end
            # with a page number, and would pull the next text into a wrong section.
            if line.upper() == "TABLE OF CONTENTS" or TOC_ENTRY_RE.match(line) and len(line.split()) <= 30:
                i += 1
                continue
            m = is_notice_heading(line)
            # Headings count from the first "1." on, which drops look-alikes in the
            # title block. A table of contents at the top gives empty sections,
            # which are removed at the end, so the numbering may restart after it.
            if m and (started or m.group(1) == "1"):
                started = True
                sections.append({"location": f"Section {m.group(1)}", "heading": m.group(2), "lines": []})
                i += 1
                continue
        sections[-1]["lines"].append(line)
        i += 1
    return [s for s in sections if s["lines"]]


# ---------------------------------------------------------------- chunks

def windows(words: list[str], size: int, overlap: int) -> list[tuple[int, int]]:
    spans, start = [], 0
    while start < len(words):
        end = min(start + size, len(words))
        spans.append((start, end))
        if end == len(words):
            break
        start = end - overlap
    return spans


def make_chunk(doc: dict, design: str, location: str, heading: str, text: str, part: int | None,
               covers: list[str] | None = None) -> dict:
    loc = location if part is None else f"{location} (part {part})"
    header = f"{doc['source']}, {loc}" + (f": {heading}" if heading else "")
    chunk_id = hashlib.sha1(f"{design}|{doc['source']}|{loc}|{text}".encode()).hexdigest()[:20]
    return {
        "id": chunk_id,
        "text": f"[{header}]\n{text}",
        "metadata": {
            "source": doc["source"], "title": doc["title"], "url": doc.get("url", ""),
            "location": loc, "heading": heading, "design": design, "words": len(text.split()),
            # every section the chunk's words come from; a fixed window labelled
            # "Article 20 to Article 22" also covers Article 21. Not part of the id.
            "covers": "|".join(covers or [location]),
        },
    }


def chunk_sections(doc: dict, sections: list[dict], design: str) -> list[dict]:
    chunks = []
    if design == "structure":
        for s in sections:
            words = " ".join(s["lines"]).split()
            if len(words) <= STRUCT_MAX_WORDS:
                chunks.append(make_chunk(doc, design, s["location"], s["heading"], " ".join(words), None))
            else:
                for n, (a, b) in enumerate(windows(words, STRUCT_WINDOW, STRUCT_OVERLAP), 1):
                    chunks.append(make_chunk(doc, design, s["location"], s["heading"], " ".join(words[a:b]), n))
    elif design == "fixed":
        # one stream of words for the whole document, each word remembering its section
        words, owner = [], []
        for s in sections:
            w = " ".join(s["lines"]).split()
            words += w
            owner += [s["location"]] * len(w)
        for a, b in windows(words, FIXED_WINDOW, FIXED_OVERLAP):
            first, last = owner[a], owner[b - 1]
            location = first if first == last else f"{first} to {last}"
            covers = list(dict.fromkeys(owner[a:b]))
            chunks.append(make_chunk(doc, design, location, "", " ".join(words[a:b]), None, covers))
    else:
        raise ValueError(f"unknown design {design!r}")
    return chunks


def read_sections(path: Path, kind: str = "auto") -> list[dict]:
    """Sections of any supported file: EUR-Lex style .html, .pdf (by page), .txt/.md."""
    suffix = path.suffix.lower()
    if suffix in (".html", ".htm"):
        lines = html_to_lines(path.read_text(encoding="utf-8", errors="replace"))
        if kind == "auto":
            kind = "regulation" if sum(bool(ARTICLE_RE.match(l)) for l in lines) >= 3 else "notice"
        return lines_to_sections(lines, kind)
    if suffix == ".pdf":
        from pypdf import PdfReader
        sections = []
        for n, page in enumerate(PdfReader(str(path)).pages, 1):
            text = clean(page.extract_text() or "")
            if text:
                sections.append({"location": f"Page {n}", "heading": "", "lines": [text]})
        return sections
    if suffix in (".txt", ".md"):
        paragraphs = [clean(p) for p in re.split(r"\n\s*\n", path.read_text(encoding="utf-8"))]
        lines = [p for p in paragraphs if p]
        return lines_to_sections(lines, "notice" if kind == "auto" else kind)
    raise ValueError(f"Unsupported file type {suffix!r}; use .html, .pdf, .txt or .md")


def chunk_file(path: str | Path, design: str = CHOSEN_DESIGN, doc: dict | None = None) -> list[dict]:
    """Extract, clean and chunk one file. Used by server.py's add_document (build() runs
    the same steps with the metadata in DOCUMENTS)."""
    path = Path(path)
    if doc is None:
        source = re.sub(r"[^A-Za-z0-9]+", "_", path.stem).strip("_").upper()
        known = next((d for d in DOCUMENTS if d["source"] == source), None)
        if known:
            # A corpus file added again: reuse its kind, title and url so it is chunked
            # exactly as in build() and add_document finds the chunks already saved.
            # (Guessing the kind fails for REG_432_2012: only 2 articles -> "notice".)
            doc = {**known, "url": EURLEX.format(known["celex"])}
        else:
            doc = {"source": source, "title": path.stem, "url": "", "kind": "auto"}
    return chunk_sections(doc, read_sections(path, doc.get("kind", "auto")), design)


# ---------------------------------------------------------------- embeddings + storage

_client = None


def gemini():
    global _client
    if _client is None:
        from google import genai
        from api_key import load_api_key
        _client = genai.Client(api_key=load_api_key())
    return _client


class DailyQuotaExceeded(RuntimeError):
    pass


def _embed(texts: list[str]) -> list[list[float]]:
    """Embed texts, one Content per text (a plain list would be averaged into one vector)."""
    from google.genai import types
    contents = [types.Content(parts=[types.Part.from_text(text=t)]) for t in texts]
    config = types.EmbedContentConfig(output_dimensionality=EMBED_DIM)
    for attempt in range(6):
        try:
            result = gemini().models.embed_content(model=EMBED_MODEL, contents=contents, config=config)
            return [e.values for e in result.embeddings]
        except Exception as error:  # noqa: BLE001
            message = str(error)
            if "429" not in message and "RESOURCE_EXHAUSTED" not in message:
                raise
            if "PerDay" in message or "per day" in message.lower():
                raise DailyQuotaExceeded(message) from error
            wait = 30 * (attempt + 1)
            log(f"  rate limited, waiting {wait}s ...")
            time.sleep(wait)
    raise RuntimeError("Still rate limited after several retries.")


def embed_query(query: str) -> list[float]:
    return _embed([f"task: search result | query: {query}"])[0]


def embed_queries(queries: list[str]) -> list[list[float]]:
    """Many queries, BATCH_SIZE per request (each still counts against the daily quota)."""
    vectors = []
    for start in range(0, len(queries), BATCH_SIZE):
        vectors += _embed([f"task: search result | query: {q}" for q in queries[start:start + BATCH_SIZE]])
    return vectors


def embed_documents(chunks: list[dict]) -> list[list[float]]:
    texts = [f"title: {c['metadata']['source']} {c['metadata']['location']} | text: {c['text']}" for c in chunks]
    return _embed(texts)


def collection(design: str = CHOSEN_DESIGN):
    INDEX_DIR.mkdir(exist_ok=True)
    db = chromadb.PersistentClient(path=str(INDEX_DIR))
    return db.get_or_create_collection(name=design, metadata={"hnsw:space": "cosine"})


def embed_and_store(chunks: list[dict], design: str = CHOSEN_DESIGN) -> int:
    """Embed only chunks whose id has no saved vector; save each batch immediately.
    Returns how many chunks were newly embedded."""
    col = collection(design)
    ids = [c["id"] for c in chunks]
    existing = set(col.get(ids=ids, include=[])["ids"]) if ids else set()
    todo = [c for c in chunks if c["id"] not in existing]
    for start in range(0, len(todo), BATCH_SIZE):
        batch = todo[start:start + BATCH_SIZE]
        vectors = embed_documents(batch)
        col.add(ids=[c["id"] for c in batch], embeddings=vectors,
                documents=[c["text"] for c in batch], metadatas=[c["metadata"] for c in batch])
        log(f"  saved {min(start + BATCH_SIZE, len(todo))}/{len(todo)} new vectors")
    return len(todo)


def refresh_metadata(chunks: list[dict], design: str) -> None:
    """Rewrite the metadata of chunks already stored (e.g. a new field). No embedding."""
    col = collection(design)
    stored = set(col.get(ids=[c["id"] for c in chunks], include=[])["ids"])
    keep = [c for c in chunks if c["id"] in stored]
    if keep:
        col.update(ids=[c["id"] for c in keep], metadatas=[c["metadata"] for c in keep])


def remove_stale(source: str, keep_ids: set[str], design: str) -> int:
    """Delete a document's chunks that its current chunking no longer produces
    (e.g. after a parsing fix), so the index never holds two versions of it."""
    col = collection(design)
    old = set(col.get(where={"source": source}, include=[])["ids"])
    stale = sorted(old - keep_ids)
    if stale:
        col.delete(ids=stale)
    return len(stale)


def search(query: str, k: int = 5, design: str = CHOSEN_DESIGN, source: str | None = None) -> list[dict]:
    """Top-k chunks for a query: text, source, location, similarity."""
    col = collection(design)
    where = {"source": source} if source else None
    res = col.query(query_embeddings=[embed_query(query)], n_results=k, where=where,
                    include=["documents", "metadatas", "distances"])
    return [
        {"text": doc, "source": meta["source"], "location": meta["location"],
         "title": meta["title"], "score": round(1 - dist, 3)}
        for doc, meta, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0])
    ]


# ---------------------------------------------------------------- main

def build(designs: list[str], embed: bool = True) -> None:
    total_words = 0
    for doc in DOCUMENTS:
        doc["url"] = EURLEX.format(doc["celex"])
        path = download(doc)
        sections = read_sections(path, doc["kind"])
        words = sum(len(" ".join(s["lines"]).split()) for s in sections)
        total_words += words
        log(f"\n{doc['source']}: {len(sections)} sections, {words:,} words")
        log("  first locations: " + ", ".join(s["location"] for s in sections[:8]))
        for design in designs:
            chunks = chunk_sections(doc, sections, design)
            log(f"  {design}: {len(chunks)} chunks")
            if embed:
                removed = remove_stale(doc["source"], {c["id"] for c in chunks}, design)
                if removed:
                    log(f"  {design}: removed {removed} outdated chunks")
                new = embed_and_store(chunks, design)
                refresh_metadata(chunks, design)
                log(f"  {design}: {new} newly embedded, {len(chunks) - new} already saved")
    log(f"\nCorpus total: {total_words:,} words")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--no-embed", action="store_true", help="download and chunk only; print stats")
    parser.add_argument("--design", choices=DESIGNS, help="build only this design")
    args = parser.parse_args()
    try:
        build([args.design] if args.design else DESIGNS, embed=not args.no_embed)
    except DailyQuotaExceeded:
        log("\nDaily embedding quota reached. Everything embedded so far is saved;"
            "\nrun `main.py index` again after 09:00 (Spain) to embed the rest.")
        sys.exit(1)