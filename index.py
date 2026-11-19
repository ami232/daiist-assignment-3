"""
Assignment 3: build the index (`main.py index`).

Pipeline: download the corpus into corpus/ -> extract and clean the text ->
chunk it with source and location metadata -> embed with Gemini -> store in
index/ (ChromaDB). Vectors are saved batch by batch and only chunks without a
saved vector are embedded, so a crash or the daily quota loses nothing.

Two chunking designs are built so they can be compared by hit rate:
  design "a": fixed-size windows of CHUNK_WORDS words (structure ignored)
  design "b": structure-based (GDPR article / numbered paragraphs of the guidelines)

Per-file functions used by server.py's add-document tool:
  chunk_file(path, design) -> list[Chunk]
  embed_and_store(chunks, design) -> dict with counts
  embed_query(text) -> vector

Usage:
  uv run python index.py                 # download, chunk, embed designs a and b
  uv run python index.py a               # only design a
  uv run python index.py --dry-run       # chunk only: no API calls, shows counts
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import time
from dataclasses import dataclass
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"
QUERY_CACHE = INDEX_DIR / "query_cache.json"

EMBED_MODEL = "gemini-embedding-2"
EMBED_BATCH = 10          # texts embedded between saves to index/ (each text counts against the quota)
DESIGNS = ("a", "b")

# ---- chunking settings (these are your design decisions: change and re-index) ----
CHUNK_WORDS = 150         # design a: window size in words
CHUNK_OVERLAP = 0         # design a: words shared between neighbouring windows
B_MAX_WORDS = 220         # design b: a chunk groups paragraphs up to about this size
MIN_CHUNK_WORDS = 40      # design b: a smaller leftover is merged into the previous chunk
INCLUDE_RECITALS = False  # GDPR recitals (173 explanatory paragraphs before the articles)

BROWSER = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) university-assignment"}
CORPUS = {
    "gdpr": {
        "url": "http://publications.europa.eu/resource/celex/32016R0679",
        "headers": {**BROWSER, "Accept": "application/xhtml+xml", "Accept-Language": "eng"},
        "ext": "html",
    },
    "edpb_breach_notification": {
        "url": "https://www.edpb.europa.eu/system/files/documents/2023-04/edpb_guidelines_202209_personal_data_breach_notification_v2.0_en.pdf",
        "headers": BROWSER,
        "ext": "pdf",
    },
    "edpb_controller_processor": {
        "url": "https://www.edpb.europa.eu/system/files/2023-10/edpb_guidelines_202007_controllerprocessor_final_en.pdf",
        "headers": BROWSER,
        "ext": "pdf",
    },
}


@dataclass
class Chunk:
    id: str
    source: str       # document name, as in eval/questions.csv `expected_source`
    location: str     # page, article or paragraph range, as in `expected_location`
    text: str
    design: str

    @property
    def words(self) -> int:
        return len(self.text.split())


class DailyQuotaReached(Exception):
    pass


# --------------------------------------------------------------------------- download

def download_corpus() -> None:
    """Download any corpus document that is not in corpus/ yet."""
    import httpx

    CORPUS_DIR.mkdir(exist_ok=True)
    with httpx.Client(follow_redirects=True, timeout=90) as client:
        for name, spec in CORPUS.items():
            path = CORPUS_DIR / f"{name}.{spec['ext']}"
            if path.exists() and path.stat().st_size > 20000:
                continue
            r = client.get(spec["url"], headers=spec["headers"])
            if r.status_code != 200 or len(r.content) < 20000:
                raise RuntimeError(f"Could not download {name}: HTTP {r.status_code}, {len(r.content)} bytes")
            path.write_bytes(r.content)
            print(f"downloaded {path.name}")


# --------------------------------------------------------------------------- cleaning

def normalise(text: str) -> str:
    """Collapse whitespace and repair line-break hyphenation."""
    text = text.replace("\u00ad", "").replace("\u00a0", " ")
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)   # "inform-\nation" -> "information"
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def split_sentences(text: str) -> list[str]:
    return re.split(r"(?<=[.!?;:])\s+(?=[A-Z0-9\u201c\"(\u2018])", text)


def split_long(text: str, max_words: int) -> list[str]:
    """Split a long text on sentence boundaries into pieces of at most ~max_words."""
    pieces, current = [], []
    for sentence in split_sentences(text):
        n = len(sentence.split())
        if current and sum(len(s.split()) for s in current) + n > max_words:
            pieces.append(" ".join(current))
            current = []
        current.append(sentence)
    if current:
        pieces.append(" ".join(current))
    return pieces


# --------------------------------------------------------------------------- extraction

HEADER_RE = re.compile(r"^Adopted(?: - After public consultation)?\s+\d+\s*$")
LEADER_RE = re.compile(r"\.{5,}\s*\d+\s*$")


def read_pdf_pages(path: Path) -> list[tuple[int, list[str]]]:
    """Return [(page number, cleaned lines)].

    Extraction problems fixed here: the running header ("Adopted ... 12") that
    pypdf puts at the top of every page, and the table-of-contents pages (lines
    ending in dotted leaders), which would otherwise be indexed as if they were
    content.
    """
    from pypdf import PdfReader

    pages = []
    for number, page in enumerate(PdfReader(str(path)).pages, start=1):
        lines = [ln.strip() for ln in (page.extract_text() or "").splitlines()]
        lines = [ln for ln in lines if ln and not HEADER_RE.match(ln)]
        if sum(1 for ln in lines if LEADER_RE.search(ln)) >= 4:
            continue  # table of contents
        if lines:
            pages.append((number, lines))
    return pages


def read_gdpr_html(path: Path) -> list[tuple[str, str, list[str]]]:
    """Return [(location label, title, [paragraph texts])] for each article (and recital)."""
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(path.read_bytes(), "html.parser")
    units = []
    for div in soup.find_all("div", class_="eli-subdivision"):
        div_id = div.get("id", "")
        if div_id.startswith("rct_") and INCLUDE_RECITALS:
            label = f"Recital {div_id[4:]}"
        elif div_id.startswith("art_"):
            label = f"Article {div_id[4:]}"
        else:
            continue
        paragraphs = []
        title = div.find("p", class_="oj-sti-art")
        title_text = normalise(title.get_text(" ")) if title else ""
        for child in div.children:
            if getattr(child, "name", None) is None:
                continue
            classes = child.get("class", [])
            if "oj-ti-art" in classes or "oj-sti-art" in classes or "eli-title" in classes:
                continue
            text = normalise(child.get_text(" "))
            if text:
                paragraphs.append(text)
        if paragraphs or title_text:
            units.append((label, title_text, paragraphs or [title_text]))
    return units


def read_plain_text(path: Path) -> list[tuple[str, str, list[str]]]:
    """Generic fallback for .txt / .md / .html files added later."""
    raw = path.read_bytes().decode("utf-8", errors="ignore")
    if path.suffix.lower() in (".html", ".htm"):
        from bs4 import BeautifulSoup

        raw = BeautifulSoup(raw, "html.parser").get_text("\n")
    blocks = [normalise(b) for b in re.split(r"\n\s*\n", raw)]
    blocks = [b for b in blocks if b]
    return [(f"paragraph {i}", "", [b]) for i, b in enumerate(blocks, start=1)]


# --------------------------------------------------------------------------- chunking

def make_chunk(design: str, source: str, location: str, text: str) -> Chunk:
    digest = hashlib.sha1(f"{design}|{source}|{location}|{text}".encode()).hexdigest()[:20]
    return Chunk(id=digest, source=source, location=location, text=text, design=design)


def units_for_design_a(path: Path) -> list[tuple[str, str]]:
    """[(location label, text)] with structure kept only as a label."""
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return [(f"p.{n}", normalise("\n".join(lines))) for n, lines in read_pdf_pages(path)]
    if path.name.startswith("gdpr") and suffix in (".html", ".htm"):
        return [(label, " ".join([title] + paras if title else paras)) for label, title, paras in read_gdpr_html(path)]
    return [(label, " ".join(paras)) for label, _, paras in read_plain_text(path)]


def chunks_design_a(path: Path) -> list[Chunk]:
    """Fixed-size windows over the whole document; the location is where each window starts."""
    source = path.stem
    words, labels = [], []
    for label, text in units_for_design_a(path):
        for word in text.split():
            words.append(word)
            labels.append(label)
    stride = max(CHUNK_WORDS - CHUNK_OVERLAP, 1)
    chunks = []
    for start in range(0, len(words), stride):
        window = words[start:start + CHUNK_WORDS]
        if len(window) < 20 and chunks:      # too small to stand alone: drop the tiny tail
            break
        first, last = labels[start], labels[start + len(window) - 1]
        location = first if first == last else f"{first} to {last}"
        chunks.append(make_chunk("a", source, location, " ".join(window)))
        if start + CHUNK_WORDS >= len(words):
            break
    return chunks


PARA_RE = re.compile(r"^(\d{1,3})\.\s+(\S.*)$")


def numbered_paragraphs(path: Path) -> list[tuple[str, int, str]]:
    """Parse a guideline PDF into [(label, page, text)] using its numbered paragraphs.

    A line "29. Article 33(1) ..." starts paragraph 29 only if 29 is the next
    expected number; this keeps numbered lists and footnotes from splitting it.
    Text before paragraph 1 is returned with label "0".
    """
    paragraphs: list[list] = [["0", None, []]]    # [label, page, lines]
    expected = 1
    for page, lines in read_pdf_pages(path):
        for line in lines:
            match = PARA_RE.match(line)
            if match and int(match.group(1)) == expected:
                paragraphs.append([str(expected), page, [line]])
                expected += 1
            else:
                if paragraphs[-1][1] is None:
                    paragraphs[-1][1] = page
                paragraphs[-1][2].append(line)
    return [(label, page, normalise("\n".join(lines))) for label, page, lines in paragraphs if lines]


def group_paragraphs(items: list[tuple[str, int, str]], max_words: int) -> list[list[tuple[str, int, str]]]:
    """Group consecutive items up to max_words; a tiny leftover group joins the previous one."""
    groups, current, size = [], [], 0
    for item in items:
        n = len(item[2].split())
        if current and size + n > max_words:
            groups.append(current)
            current, size = [], 0
        current.append(item)
        size += n
    if current:
        groups.append(current)
    merged: list[list[tuple[str, int, str]]] = []
    for group in groups:
        words = sum(len(t.split()) for _, _, t in group)
        if merged and words < MIN_CHUNK_WORDS:
            merged[-1].extend(group)
        else:
            merged.append(group)
    return merged


def chunks_design_b(path: Path) -> list[Chunk]:
    """Structure-based chunks: whole GDPR articles, or groups of numbered guideline paragraphs."""
    source = path.stem
    suffix = path.suffix.lower()
    chunks: list[Chunk] = []

    if suffix == ".pdf":
        items = numbered_paragraphs(path)
        if sum(1 for label, _, _ in items if label != "0") >= 10:
            # split any single huge paragraph first; all its pieces keep the paragraph number
            expanded = []
            for label, page, text in items:
                for piece in split_long(text, B_MAX_WORDS):
                    expanded.append((label, page, piece))
            front = [item for item in expanded if item[0] == "0"]
            body = [item for item in expanded if item[0] != "0"]
            for group in group_paragraphs(front, B_MAX_WORDS):
                chunks.append(make_chunk("b", source, f"front matter (p.{group[0][1]})", " ".join(t for _, _, t in group)))
            for group in group_paragraphs(body, B_MAX_WORDS):
                first, last = group[0], group[-1]
                if first[0] == last[0]:
                    location = f"para {first[0]} (p.{first[1]})"
                else:
                    location = f"paras {first[0]}-{last[0]} (p.{first[1]})"
                chunks.append(make_chunk("b", source, location, " ".join(t for _, _, t in group)))
            return chunks
        # no numbered paragraphs: fall back to page-sized pieces
        for page, lines in read_pdf_pages(path):
            for k, piece in enumerate(split_long(normalise("\n".join(lines)), B_MAX_WORDS), start=1):
                chunks.append(make_chunk("b", source, f"p.{page}" + (f" part {k}" if k > 1 else ""), piece))
        return chunks

    if path.name.startswith("gdpr") and suffix in (".html", ".htm"):
        units = read_gdpr_html(path)
    else:
        units = read_plain_text(path)
    for label, title, paragraphs in units:
        items = []
        for paragraph in paragraphs:
            match = re.match(r"^(\d{1,3})\.\s", paragraph)
            number = match.group(1) if match else ""
            for piece in split_long(paragraph, B_MAX_WORDS):
                items.append((number, 0, piece))        # every piece keeps its paragraph's number
        groups = group_paragraphs(items, B_MAX_WORDS)
        for g, group in enumerate(groups, start=1):
            if len(groups) == 1:
                location = label
            else:
                numbers = list(dict.fromkeys(n for n, _, _ in group if n))
                if not numbers:
                    location = f"{label} part {g}"
                elif len(numbers) == 1:
                    location = f"{label}({numbers[0]})"
                else:
                    location = f"{label}({numbers[0]})-({numbers[-1]})"
            text = " ".join(t for _, _, t in group)
            if g == 1 and title:
                text = f"{title}. {text}"             # keep the article title with its first chunk
            chunks.append(make_chunk("b", source, location, text))
    return chunks


def chunk_file(path: str | Path, design: str = "b") -> list[Chunk]:
    """Extract, clean and chunk one file. Also used by server.py's add-document tool."""
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"No such file: {path}")
    if path.suffix.lower() not in (".pdf", ".html", ".htm", ".txt", ".md"):
        raise ValueError(f"Unsupported file type {path.suffix!r}; use .pdf, .html, .txt or .md")
    chunks = chunks_design_a(path) if design == "a" else chunks_design_b(path)
    # identical text twice in one file would collide on the id: keep the first
    seen, unique = set(), []
    for chunk in chunks:
        if chunk.id not in seen:
            seen.add(chunk.id)
            unique.append(chunk)
    return unique


def corpus_files() -> list[Path]:
    return [CORPUS_DIR / f"{name}.{spec['ext']}" for name, spec in CORPUS.items()]


# --------------------------------------------------------------------------- embedding

def get_client():
    from google import genai

    from api_key import load_api_key

    return genai.Client(api_key=load_api_key())


def embed_one(text: str, client) -> list[float]:
    """Embed one text. Retries per-minute limits; raises DailyQuotaReached on the daily limit."""
    delay = 20
    for attempt in range(8):
        try:
            response = client.models.embed_content(model=EMBED_MODEL, contents=text)
            if len(response.embeddings) != 1:
                raise RuntimeError(f"Expected 1 embedding for 1 text, got {len(response.embeddings)}.")
            return list(response.embeddings[0].values)
        except RuntimeError:
            raise
        except Exception as error:  # noqa: BLE001
            message = str(error)
            quota = "429" in message or "RESOURCE_EXHAUSTED" in message or "quota" in message.lower()
            if quota and ("PerDay" in message or "per day" in message.lower()):
                raise DailyQuotaReached(message) from error
            if quota and attempt < 7:
                print(f"  rate limit, waiting {delay}s ...", flush=True)
                time.sleep(delay)
                delay = min(delay * 2, 120)
                continue
            if quota:
                raise DailyQuotaReached(message) from error
            raise
    raise RuntimeError("embedding failed")


def embed_texts(texts: list[str], client=None) -> list[list[float]]:
    """Embed texts, one API call per text (gemini-embedding-2 merges a list into one vector)."""
    client = client or get_client()
    return [embed_one(text, client) for text in texts]


def embed_query(text: str) -> list[float]:
    """Embed a search query; answers are cached on disk so repeated questions cost no quota."""
    key = hashlib.sha1(text.encode()).hexdigest()
    cache = {}
    if QUERY_CACHE.is_file():
        try:
            cache = json.loads(QUERY_CACHE.read_text())
        except Exception:  # noqa: BLE001
            cache = {}
    if key in cache:
        return cache[key]
    vector = embed_texts([text])[0]
    cache[key] = vector
    INDEX_DIR.mkdir(exist_ok=True)
    QUERY_CACHE.write_text(json.dumps(cache))
    return vector


# --------------------------------------------------------------------------- storage

def get_collection(design: str):
    import chromadb

    INDEX_DIR.mkdir(exist_ok=True)
    client = chromadb.PersistentClient(path=str(INDEX_DIR))
    return client.get_or_create_collection(
        name=f"design_{design}", configuration={"hnsw": {"space": "cosine"}}
    )


def embedding_input(chunk: Chunk) -> str:
    """What gets embedded: the passage prefixed with where it comes from."""
    return f"{chunk.source}, {chunk.location}: {chunk.text}"


def embed_and_store(chunks: list[Chunk], design: str) -> dict:
    """Embed the chunks that have no saved vector yet and store them, batch by batch."""
    collection = get_collection(design)
    existing: set[str] = set()
    ids = [c.id for c in chunks]
    for i in range(0, len(ids), 200):
        existing.update(collection.get(ids=ids[i:i + 200], include=[])["ids"])
    todo = [c for c in chunks if c.id not in existing]
    stats = {"total": len(chunks), "already_indexed": len(chunks) - len(todo), "added": 0, "stopped_by_quota": False}
    if not todo:
        return stats
    client = get_client()
    for i in range(0, len(todo), EMBED_BATCH):
        batch = todo[i:i + EMBED_BATCH]
        try:
            vectors = embed_texts([embedding_input(c) for c in batch], client)
        except DailyQuotaReached as error:
            stats["stopped_by_quota"] = True
            print(f"\nDaily embedding quota reached after {stats['added']} new chunks.")
            print("Everything embedded so far is saved. Run the same command again after the")
            print("quota resets (midnight Pacific time = 09:00 in Spain) and it will continue.")
            print(f"({str(error)[:200]})")
            return stats
        collection.add(
            ids=[c.id for c in batch],
            embeddings=vectors,
            documents=[c.text for c in batch],
            metadatas=[{"source": c.source, "location": c.location, "design": c.design} for c in batch],
        )
        stats["added"] += len(batch)
        print(f"  design {design}: saved {stats['added']}/{len(todo)} new chunks", flush=True)
    return stats


# --------------------------------------------------------------------------- main

def summarise(design: str, chunks_by_source: dict[str, list[Chunk]], show: int = 2) -> None:
    print(f"\n=== design {design} ===")
    total = 0
    for source, chunks in chunks_by_source.items():
        words = sum(c.words for c in chunks)
        total += len(chunks)
        print(f"{source}: {len(chunks)} chunks, avg {words / max(len(chunks), 1):.0f} words")
        for chunk in chunks[len(chunks) // 2: len(chunks) // 2 + show]:
            print(f"    [{chunk.location}] {chunk.text[:110]}...")
    print(f"TOTAL design {design}: {total} chunks")


def main(argv: list[str]) -> int:
    dry_run = "--dry-run" in argv
    designs = [a for a in argv if a in DESIGNS] or list(DESIGNS)
    download_corpus()
    for design in designs:
        by_source = {path.stem: chunk_file(path, design) for path in corpus_files()}
        summarise(design, by_source)
        if dry_run:
            continue
        all_chunks = [c for chunks in by_source.values() for c in chunks]
        stats = embed_and_store(all_chunks, design)
        print(f"design {design}: {stats['added']} added, {stats['already_indexed']} already indexed, "
              f"{stats['total']} total")
        if stats["stopped_by_quota"]:
            return 0
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))