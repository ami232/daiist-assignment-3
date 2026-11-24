"""
Assignment 3: build the index (`main.py index`).

Corpus: FDA consumer food-safety pages, the FDA "Bad Bug Book" (2nd ed.) and the
FDA Refrigerator & Freezer Storage Chart (2019).
All are US federal government works (public domain, 17 U.S.C. 105).

Steps
1. download()          -> corpus/ (git-ignored), skipped if already there
2. chunk_file(path)    -> structure-based chunks: each HTML page is split at its
                          h2/h3 headings, the PDF at its bookmark outline
                          (pathogen > section); long sections are packed into
                          pieces of at most MAX_WORDS words.
3. embed_and_store()   -> Gemini embeddings, saved into ChromaDB (index/chroma)
                          batch by batch; only chunks without a saved vector
                          are embedded.

server.py's add_document tool imports chunk_file() and embed_and_store().
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"
CHROMA_DIR = INDEX_DIR / "chroma"

EMBED_MODEL = "gemini-embedding-2"
MAX_WORDS = 400          # max words per chunk (design parameter)
EMBED_BATCH = 20         # texts per embedding call
USER_AGENT = "Mozilla/5.0 (Macintosh) daiist-assignment-3 course project"

FDA = "https://www.fda.gov/food/"
# Consumer pages that help answer "can I still eat / serve / store this?"
FDA_PAGES = [
    "buy-store-serve-safe-food/food-facts-consumers",
    "buy-store-serve-safe-food/safe-food-handling",
    "buy-store-serve-safe-food/food-safety-your-kitchen",
    "buy-store-serve-safe-food/everyday-food-safety-young-adults",
    "buy-store-serve-safe-food/refrigerator-thermometers-cold-facts-about-food-safety",
    "buy-store-serve-safe-food/food-and-water-safety-during-power-outages-and-floods",
    "buy-store-serve-safe-food/handling-food-safely-while-eating-outdoors",
    "buy-store-serve-safe-food/serving-safe-buffets",
    "buy-store-serve-safe-food/holiday-food-safety",
    "buy-store-serve-safe-food/halloween-food-safety-tips-parents",
    "buy-store-serve-safe-food/four-easy-new-years-resolutions-be-food-safe",
    "buy-store-serve-safe-food/what-you-need-know-about-egg-safety",
    "buy-store-serve-safe-food/selecting-and-serving-produce-safely",
    "buy-store-serve-safe-food/selecting-and-serving-fresh-and-frozen-seafood-safely",
    "buy-store-serve-safe-food/dangers-raw-milk-unpasteurized-milk-can-pose-serious-health-risk",
    "buy-store-serve-safe-food/queso-fresco-type-cheeses-consumer-guidance",
    "buy-store-serve-safe-food/what-you-need-know-about-preventing-listeria-infections",
    "buy-store-serve-safe-food/what-you-need-know-about-juice-safety",
    "buy-store-serve-safe-food/enjoying-homemade-ice-cream-without-risk-salmonella-infection",
    "buy-store-serve-safe-food/handling-flour-safely-what-you-need-know",
    "buy-store-serve-safe-food/test-your-safety-knowledge-about-ready-cook-foods",
    "buy-store-serve-safe-food/food-recalls-what-you-need-know",
    "buy-store-serve-safe-food/food-allergies-what-you-need-know",
    "buy-store-serve-safe-food/surplus-salvaged-and-donated-foods",
    "buy-store-serve-safe-food/5-red-flags-look-when-shopping-meal-kits",
    "consumers/what-you-need-know-about-foodborne-illnesses",
    "consumers/people-risk-foodborne-illness",
    "consumers/how-cut-food-waste-and-maintain-food-safety",
    "consumers/tips-reduce-food-waste",
]
PDFS = [
    ("bad_bug_book.pdf", "https://www.fda.gov/media/83271/download",
     "FDA Bad Bug Book, 2nd ed. (2012)"),
    ("fda_storage_chart.pdf", "https://www.fda.gov/media/101389/download",
     "FDA: How to Cut Food Waste and Maintain Food Safety, with Refrigerator & Freezer Storage Chart (2019)"),
]


# --------------------------------------------------------------------------- #
# Data
# --------------------------------------------------------------------------- #
@dataclass
class Chunk:
    text: str
    source: str            # short document id, e.g. "fda:egg-safety" or "bad_bug_book"
    title: str             # human title of the document
    location: str          # section / page, e.g. "p. 12, Salmonella species > 4. Sources"
    url: str = ""
    extra: dict = field(default_factory=dict)

    @property
    def id(self) -> str:
        h = hashlib.sha1(f"{self.source}|{self.location}|{self.text}".encode()).hexdigest()
        return h[:20]

    @property
    def embed_text(self) -> str:
        # Title and section give the embedding context the bare paragraph lacks.
        return f"{self.title} | {self.location}\n{self.text}"

    def metadata(self) -> dict:
        return {"source": self.source, "title": self.title, "location": self.location,
                "url": self.url, "words": len(self.text.split()), **self.extra}


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


# --------------------------------------------------------------------------- #
# 1. Download
# --------------------------------------------------------------------------- #
def download(force: bool = False) -> list[Path]:
    """Fetch the corpus into corpus/. Returns the local paths."""
    import httpx

    CORPUS_DIR.mkdir(exist_ok=True)
    manifest_path = CORPUS_DIR / "manifest.json"
    manifest = json.loads(manifest_path.read_text()) if manifest_path.exists() else {}
    client = httpx.Client(headers={"User-Agent": USER_AGENT}, follow_redirects=True, timeout=90)

    def fetch(url: str, dest: Path) -> None:
        if dest.exists() and dest.stat().st_size > 0 and not force:
            return
        for attempt in range(4):
            try:
                r = client.get(url)
                r.raise_for_status()
                dest.write_bytes(r.content)
                log(f"  downloaded {dest.name}")
                return
            except Exception as e:  # noqa: BLE001
                log(f"  retry {attempt + 1} for {url}: {e}")
                time.sleep(3 * (attempt + 1))
        raise RuntimeError(f"could not download {url}")

    paths = []
    for slug in FDA_PAGES:
        name = "fda_" + slug.split("/")[-1] + ".html"
        dest = CORPUS_DIR / name
        fetch(FDA + slug, dest)
        manifest[name] = {"url": FDA + slug}
        paths.append(dest)

    for name, url, title in PDFS:
        fetch(url, CORPUS_DIR / name)
        manifest[name] = {"url": url, "title": title}
        paths.append(CORPUS_DIR / name)

    manifest_path.write_text(json.dumps(manifest, indent=2))
    return paths


def _manifest() -> dict:
    p = CORPUS_DIR / "manifest.json"
    return json.loads(p.read_text()) if p.exists() else {}


# --------------------------------------------------------------------------- #
# 2. Extract, clean, chunk
# --------------------------------------------------------------------------- #
def clean(text: str) -> str:
    text = text.replace(" ", " ").replace("­", "")
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)          # de-hyphenate line breaks
    text = re.sub(r"[ \t]+", " ", text)
    text = re.sub(r" ?\n ?", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def pack(paragraphs: list[str], max_words: int = MAX_WORDS) -> list[str]:
    """Greedy-pack paragraphs into pieces of <= max_words; split huge paragraphs."""
    pieces, cur, n = [], [], 0
    for p in paragraphs:
        words = p.split()
        if not words:
            continue
        if len(words) > max_words:                     # a single very long paragraph
            if cur:
                pieces.append("\n".join(cur)); cur, n = [], 0
            for i in range(0, len(words), max_words):
                pieces.append(" ".join(words[i:i + max_words]))
            continue
        if n + len(words) > max_words and cur:
            pieces.append("\n".join(cur)); cur, n = [], 0
        cur.append(p); n += len(words)
    if cur:
        pieces.append("\n".join(cur))
    return pieces


def _parent(loc: str) -> str:
    """'p. 66, Francisella > 5. Diagnosis' -> 'Francisella'; HTML sections share one parent."""
    loc = re.sub(r"^p\. \d+, ", "", loc)
    return loc.split(" > ")[0] if " > " in loc else ""


def merge_small_sections(sections, max_words: int):
    """Merge consecutive short sections of the same parent (same pathogen, same page)
    into one, keeping each heading inline, as long as the result fits max_words."""
    merged: list[tuple[str, list[str]]] = []
    size = lambda ps: sum(len(p.split()) for p in ps)  # noqa: E731
    for loc, ps in sections:
        heading = loc.split(" > ")[-1].removeprefix("Section: ")
        if (merged and _parent(merged[-1][0]) == _parent(loc)
                and size(merged[-1][1]) + size(ps) <= max_words):
            prev_loc, prev_ps = merged[-1]
            merged[-1] = (f"{prev_loc}; {heading}", prev_ps + [f"[{heading}]"] + ps)
        else:
            merged.append((loc, list(ps)))
    return merged


def _sections_to_chunks(sections, source, title, url, max_words) -> list[Chunk]:
    chunks = []
    for loc, paragraphs in merge_small_sections(sections, max_words):
        for i, piece in enumerate(pack(paragraphs, max_words)):
            location = loc if i == 0 else f"{loc} (part {i + 1})"
            chunks.append(Chunk(clean(piece), source, title, location, url))
    return [c for c in chunks if len(c.text.split()) >= 8]


def chunk_html(path: Path, max_words: int = MAX_WORDS, url: str = "") -> list[Chunk]:
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(path.read_text(encoding="utf-8", errors="ignore"), "html.parser")
    root = soup.select_one("article") or soup.select_one("main") or soup.body or soup
    for bad in root.select("nav, aside, script, style, .lcds-section-nav, .visually-hidden, "
                           "[class*=share], [class*=toolbar], footer"):
        bad.decompose()
    h1 = root.find("h1") or soup.find("title")
    title = h1.get_text(" ", strip=True) if h1 else path.stem
    title = re.sub(r"\s*\|\s*FDA\s*$", "", title)

    sections: list[tuple[str, list[str]]] = [("Introduction", [])]
    for el in root.find_all(["h2", "h3", "h4", "p", "li", "tr", "dt", "dd"]):
        if el.name in ("p", "li") and el.find_parent(["li", "tr", "dd"]) and el.name == "p":
            continue                                    # paragraph inside a list item/table: parent covers it
        if el.name == "li" and el.find("li"):
            continue                                    # outer list item of a nested list
        text = el.get_text(" ", strip=True)
        if not text:
            continue
        if el.name in ("h2", "h3", "h4"):
            if text.lower().startswith(("content current as of", "regulated product", "related information")):
                break                                   # page footer starts here
            sections.append((f"Section: {text}", []))
            continue
        if el.name == "tr":
            cells = [c.get_text(" ", strip=True) for c in el.find_all(["th", "td"])]
            text = " | ".join(c for c in cells if c)
        if text in ("Print & Share (PDF)", "Español (Spanish)") or text.startswith("Items on this page"):
            continue
        sections[-1][1].append(("• " + text) if el.name == "li" else text)
    sections = [(loc, ps) for loc, ps in sections if ps]

    source = "fda:" + path.stem.removeprefix("fda_") if path.stem.startswith("fda_") else path.stem
    return _sections_to_chunks(sections, source, title, url, max_words)


# Running header of the Bad Bug Book, sometimes split over two lines by pypdf.
PDF_RUNNING_HEADER = re.compile(
    r"(?m)^\s*(_{5,}|Bad Bug Book|(Foodborne Pathogenic )?Micro-?\s*$|"
    r"(Foodborne Pathogenic Micro)?organisms and Natural Toxins|Foodborne Pathogenic Micro)\s*$")


def chunk_pdf(path: Path, max_words: int = MAX_WORDS, url: str = "", title: str = "") -> list[Chunk]:
    """Split a PDF at its bookmark outline; fall back to one section per page."""
    import pypdf

    reader = pypdf.PdfReader(str(path))
    pages = [clean(p.extract_text() or "") for p in reader.pages]
    pages = [re.sub(r"(?m)^\s*\d{1,3}\s*$", "", p) for p in pages]   # bare page numbers
    pages = [PDF_RUNNING_HEADER.sub("", p) for p in pages]
    pages = [re.sub(r"(?m)^\s*\d{1,2}\.\s*$", "", p) for p in pages]   # stray "4." heading numbers
    title = title or (reader.metadata.title if reader.metadata and reader.metadata.title else path.stem)

    # Flatten the outline into (page_index, path_of_titles)
    marks: list[tuple[int, list[str]]] = []

    def walk(items, trail):
        last = None
        for it in items:
            if isinstance(it, list):
                if last is not None:
                    walk(it, trail + [last])
                continue
            pg = reader.get_destination_page_number(it)
            t = re.sub(r"\s+", " ", str(it.title)).strip()
            last = t
            if pg is not None:
                marks.append((pg, trail + [t]))

    try:
        walk(reader.outline, [])
    except Exception:  # noqa: BLE001
        marks = []

    sections: list[tuple[str, list[str]]] = []
    if not marks:
        for i, text in enumerate(pages):
            # no outline: pack line by line, so table rows (e.g. a storage chart) stay whole
            sections.append((f"p. {i + 1}", [ln for ln in text.split("\n") if ln.strip()]))
    else:
        # drop the document-title root from trails, keep the 2 most specific levels
        marks.sort(key=lambda m: m[0])
        bounds = []
        for k, (pg, trail) in enumerate(marks):
            end = marks[k + 1][0] if k + 1 < len(marks) else len(pages) - 1
            bounds.append((pg, max(pg, end), trail))
        # Sections that start on the same page: locate each heading inside the page text
        full, offsets = "", []
        for p in pages:
            offsets.append(len(full)); full += p + "\n\n"
        offsets.append(len(full))
        starts = []
        for pg, _, trail in bounds:
            head = trail[-1]
            key = re.escape(re.sub(r"^\d+\.\s*", "", head)[:40]).replace(r"\ ", r"\s*")
            m = re.search(r"(\d{1,2}\.\s*)?" + key, full[offsets[pg]:offsets[min(pg + 2, len(pages))]], flags=re.I)
            starts.append(offsets[pg] + (m.start() if m else 0))
        for k, (pg, _, trail) in enumerate(bounds):
            a = starts[k]
            b = starts[k + 1] if k + 1 < len(starts) else len(full)
            if b <= a:
                continue
            body = full[a:b]
            first_page = next(i for i in range(len(pages)) if offsets[i + 1] > a) + 1
            label = " > ".join(t for t in trail[-2:] if t != title) or trail[-1]
            paras = [re.sub(r"\s*\n\s*", " ", p).strip() for p in body.split("\n\n")]
            # pypdf gives few blank lines; break on sentence-ending line breaks too
            if len(paras) <= 2:
                paras = [re.sub(r"\s*\n\s*", " ", s).strip()
                         for s in re.split(r"(?<=[.:;])\s*\n", body) if s.strip()]
            sections.append((f"p. {first_page}, {label}", paras))

    source = path.stem
    return _sections_to_chunks(sections, source, title, url, max_words)


def chunk_text(path: Path, max_words: int = MAX_WORDS) -> list[Chunk]:
    """Plain text / Markdown: split at Markdown headings or blank lines."""
    raw = clean(path.read_text(encoding="utf-8", errors="ignore"))
    sections: list[tuple[str, list[str]]] = [("Introduction", [])]
    for block in raw.split("\n\n"):
        m = re.match(r"^#{1,4}\s+(.*)", block)
        if m:
            sections.append((f"Section: {m.group(1).strip()}", [block[m.end():].strip()]))
        else:
            sections[-1][1].append(block)
    sections = [(loc, [p for p in ps if p]) for loc, ps in sections if any(ps)]
    return _sections_to_chunks(sections, path.stem, path.stem, "", max_words)


def chunk_file(path: str | Path, max_words: int = MAX_WORDS) -> list[Chunk]:
    """Extract, clean and chunk one file (.html/.htm, .pdf, .txt, .md)."""
    path = Path(path).expanduser().resolve()
    info = _manifest().get(path.name, {})
    suffix = path.suffix.lower()
    if suffix in (".html", ".htm"):
        return chunk_html(path, max_words, info.get("url", ""))
    if suffix == ".pdf":
        return chunk_pdf(path, max_words, info.get("url", ""), info.get("title", ""))
    if suffix in (".txt", ".md"):
        return chunk_text(path, max_words)
    raise ValueError(f"unsupported file type: {suffix} (use .html, .pdf, .txt or .md)")


# --------------------------------------------------------------------------- #
# 3. Embed and store
# --------------------------------------------------------------------------- #
_client = None


def genai_client():
    global _client
    if _client is None:
        from google import genai
        from api_key import load_api_key
        _client = genai.Client(api_key=load_api_key())
    return _client


class QuotaExhausted(RuntimeError):
    pass


def embed(texts: list[str], task_type: str = "RETRIEVAL_DOCUMENT") -> list[list[float]]:
    """Embed a list of texts (one vector each). Retries on per-minute rate limits."""
    from google.genai import types

    contents = [types.Content(parts=[types.Part(text=t)]) for t in texts]
    for attempt in range(3):
        try:
            r = genai_client().models.embed_content(
                model=EMBED_MODEL, contents=contents,
                config=types.EmbedContentConfig(task_type=task_type))
            return [e.values for e in r.embeddings]
        except Exception as e:  # noqa: BLE001
            msg = str(e)
            if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
                if attempt < 2:
                    log(f"  rate limited, waiting 65 s (attempt {attempt + 1}/3)")
                    time.sleep(65)
                    continue
                raise QuotaExhausted(msg[:300]) from e
            raise
    raise QuotaExhausted("rate limit")


def embed_query(text: str) -> list[float]:
    return embed([text], task_type="RETRIEVAL_QUERY")[0]


def collection_name(max_words: int = MAX_WORDS) -> str:
    return f"food_safety_{max_words}w"


def get_collection(max_words: int = MAX_WORDS):
    import chromadb

    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return client.get_or_create_collection(collection_name(max_words), metadata={"hnsw:space": "cosine"},
                                           embedding_function=None)


def embed_and_store(chunks: list[Chunk], collection=None) -> dict:
    """Embed chunks that have no saved vector and add them to the collection.

    Saves after every batch, so a crash or the daily quota loses nothing.
    Returns counts: {"new": n_embedded, "skipped": n_already_there, "pending": n_left}.
    """
    col = collection or get_collection()
    unique = {c.id: c for c in chunks}
    existing = set(col.get(ids=list(unique), include=[])["ids"]) if unique else set()
    todo = [c for cid, c in unique.items() if cid not in existing]
    done = 0
    for i in range(0, len(todo), EMBED_BATCH):
        batch = todo[i:i + EMBED_BATCH]
        try:
            vectors = embed([c.embed_text for c in batch])
        except QuotaExhausted as e:
            log(f"  quota exhausted after {done} new vectors: {e}")
            return {"new": done, "skipped": len(existing), "pending": len(todo) - done}
        col.add(ids=[c.id for c in batch], embeddings=vectors,
                documents=[c.text for c in batch], metadatas=[c.metadata() for c in batch])
        done += len(batch)
        log(f"  embedded {done}/{len(todo)}")
    return {"new": done, "skipped": len(existing), "pending": 0}


# --------------------------------------------------------------------------- #
# Main
# --------------------------------------------------------------------------- #
def build_chunks(max_words: int = MAX_WORDS) -> list[Chunk]:
    chunks = []
    for path in download():
        cs = chunk_file(path, max_words)
        chunks.extend(cs)
    return chunks


def stats(chunks: list[Chunk]) -> str:
    words = [len(c.text.split()) for c in chunks]
    docs = {c.source for c in chunks}
    return (f"{len(docs)} documents, {len(chunks)} chunks, {sum(words):,} words "
            f"(mean {sum(words) / max(1, len(words)):.0f}, max {max(words, default=0)} words/chunk)")


def main() -> None:
    import argparse

    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="chunk only, no embeddings")
    ap.add_argument("--max-words", type=int, default=MAX_WORDS)
    args = ap.parse_args()

    log("Downloading and chunking ...")
    chunks = build_chunks(args.max_words)
    log(stats(chunks))
    (INDEX_DIR).mkdir(exist_ok=True)
    if args.dry_run:
        out = INDEX_DIR.parent / "corpus" / f"chunks_{args.max_words}w.jsonl"
        with out.open("w") as f:
            for c in chunks:
                f.write(json.dumps({"id": c.id, **c.metadata(), "text": c.text}) + "\n")
        log(f"dry run: wrote {out.relative_to(ROOT)}")
        return

    col = get_collection(args.max_words)
    result = embed_and_store(chunks, col)
    log(f"index: {col.count()} vectors in collection {col.name} "
        f"({result['new']} new, {result['skipped']} already saved, {result['pending']} pending)")
    if result["pending"]:
        log("Daily embedding quota reached. Run `main.py index` again after 09:00 (Spain) to finish.")


if __name__ == "__main__":
    main()
