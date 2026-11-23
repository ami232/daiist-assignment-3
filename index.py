"""
Assignment 3: build the index (`main.py index`).

Corpus: EU passenger-rights rules, for a travel-agency customer-service agent.

1. Download each document into corpus/ (git-ignored) from the EU Publications
   Office. EUR-Lex itself blocks scripted downloads; the Publications Office
   serves the same official text.
2. Extract the text as blocks, each tagged with its location (Recital, Article,
   Annex, or guideline section), dropping footnotes.
3. Chunk it two ways, the two retrieval designs we compare:
   - "fixed":     ~150-word windows with 30 words of overlap;
   - "structure": one chunk per article / guideline section, long ones split
                  into pieces of at most ~300 words.
4. Embed with Gemini and store in index/ (ChromaDB), saving every batch as soon
   as it comes back and embedding only chunks that have no saved vector yet.

server.py imports `chunk_file` and `embed_and_store` for its add-document tool.

    uv run python index.py             # what main.py index runs
    uv run python index.py --dry-run   # chunk and report, embed nothing
"""

import hashlib
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

import chromadb
import httpx
from bs4 import BeautifulSoup
from google import genai
from google.genai import types
from pypdf import PdfReader

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"

DOCS = [
    {"celex": "32004R0261", "source": "Regulation (EC) No 261/2004", "mode": "air",
     "title": "Air passenger rights: denied boarding, cancellation, long delay", "date": "2004-02-11"},
    {"celex": "52024XC05687", "source": "Commission Guidelines on Regulation 261/2004 (2024)", "mode": "air",
     "title": "Interpretative Guidelines on Regulation (EC) No 261/2004", "date": "2024-07-22"},
    {"celex": "32021R0782", "source": "Regulation (EU) 2021/782", "mode": "rail",
     "title": "Rail passengers' rights and obligations", "date": "2021-04-29"},
    {"celex": "32011R0181", "source": "Regulation (EU) No 181/2011", "mode": "bus",
     "title": "Rights of passengers in bus and coach transport", "date": "2011-02-16"},
    {"celex": "32010R1177", "source": "Regulation (EU) No 1177/2010", "mode": "sea",
     "title": "Rights of passengers travelling by sea and inland waterway", "date": "2010-11-24"},
]
for d in DOCS:
    d["url"] = f"https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:{d['celex']}"
    d["path"] = CORPUS_DIR / f"{d['celex']}.html"

DESIGNS = {
    "fixed": {"size": 150, "overlap": 30},
    "structure": {"max_words": 300},
}
EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768      # Matryoshka truncation: a quarter of the size, keeps index/ well under 90 MB
EMBED_BATCH = 50


# =============================================================================
# 1. Download
# =============================================================================
def download(doc: dict) -> Path:
    if doc["path"].exists():
        return doc["path"]
    CORPUS_DIR.mkdir(exist_ok=True)
    response = httpx.get(
        f"https://publications.europa.eu/resource/celex/{doc['celex']}",
        headers={"Accept": "application/xhtml+xml, text/html", "Accept-Language": "eng"},
        follow_redirects=True, timeout=60,
    )
    response.raise_for_status()
    doc["path"].write_bytes(response.content)
    return doc["path"]


# =============================================================================
# 2. Extract: text blocks tagged with their location
# =============================================================================
@dataclass
class Block:
    text: str
    location: str          # "Article 7", "Recital (12)", "Annex II", "Section 4.3.2"
    heading: str = ""      # the article's or section's title, if any


ARTICLE = re.compile(r"^Article\s+(\d+[a-z]?)$")
RECITAL = re.compile(r"^\((\d+)\)\s")
ANNEX = re.compile(r"^ANNEX\s*([IVXL]*)$")
CHAPTER = re.compile(r"^(CHAPTER|SECTION)\s+[IVXL0-9]+$")
GUIDE_SECTION = re.compile(r"^(\d+(?:\.\d+)*)\.?\s+(\S.*)$")


def clean(text: str) -> str:
    text = text.replace("\xa0", " ")
    return re.sub(r"\s+", " ", text).strip()


def extract_html(path: Path) -> list[Block]:
    """Blocks in reading order, with footnotes removed.

    The Commission guidelines carry ~190 footnotes whose markers sit mid-sentence
    ("...compensation 12 ...") and whose bodies follow the text. Both are removed
    so sentences stay whole and case-law notes don't land in unrelated chunks.
    """
    soup = BeautifulSoup(path.read_bytes(), "html.parser")
    for tag in soup.select(".oj-note, .oj-note-tag, a[id^='ntc'], a[href^='#ntr'], .note, p.note"):
        tag.decompose()
    for sup in soup.find_all("span", class_="oj-super"):
        if sup.find_parent("a") or re.fullmatch(r"\s*\(?\d+\)?\s*", sup.get_text()):
            sup.decompose()
    is_guidelines = "XC" in path.stem

    blocks: list[Block] = []
    location, heading, started = "Preamble", "", False
    pending_title = False
    for p in soup.find_all("p"):
        if p.find("p"):
            continue  # the 2004 regulation wraps everything in one outer <p>; reading it would double the text
        text = clean(p.get_text(" "))
        if not text:
            continue
        classes = p.get("class") or []
        if is_guidelines:
            m = GUIDE_SECTION.match(text)
            if m and ("oj-ti-grseq-1" in classes or len(text) < 120 and text.split(".")[0].isdigit()):
                location, heading, started = f"Section {m.group(1)}", m.group(2), True
                blocks.append(Block(text, location, heading))
                continue
            blocks.append(Block(text, location if started else "Introduction", heading))
            continue
        if ARTICLE.match(text):
            location, heading, started, pending_title = f"Article {ARTICLE.match(text).group(1)}", "", True, True
            blocks.append(Block(text, location))
            continue
        if pending_title and len(text) < 120 and not text.endswith("."):
            heading, pending_title = text, False
            blocks.append(Block(text, location, heading))
            continue
        pending_title = False
        if ANNEX.match(text):
            location, heading, started = f"Annex {ANNEX.match(text).group(1)}".strip(), "", True
            blocks.append(Block(text, location))
            continue
        if not started and re.fullmatch(r"\((\d+)\)", text):
            location = f"Recital ({text.strip('()')})"  # newer acts put the recital number in its own cell
            continue
        if not started and RECITAL.match(text):
            location = f"Recital ({RECITAL.match(text).group(1)})"
        if CHAPTER.match(text):
            continue  # chapter labels carry no content; the article's own number locates it
        blocks.append(Block(text, location, heading))
    return blocks


def extract_pdf(path: Path) -> list[Block]:
    reader = PdfReader(str(path))
    return [Block(clean(page.extract_text() or ""), f"Page {i}") for i, page in enumerate(reader.pages, 1)
            if clean(page.extract_text() or "")]


def extract_text(path: Path) -> list[Block]:
    paragraphs = [clean(p) for p in path.read_text(encoding="utf-8", errors="replace").split("\n\n")]
    return [Block(p, f"Paragraph {i}") for i, p in enumerate(filter(None, paragraphs), 1)]


def extract(path: Path) -> list[Block]:
    suffix = path.suffix.lower()
    if suffix in (".html", ".htm", ".xhtml"):
        return extract_html(path)
    if suffix == ".pdf":
        return extract_pdf(path)
    return extract_text(path)


# =============================================================================
# 3. Chunk
# =============================================================================
@dataclass
class Chunk:
    text: str
    meta: dict = field(default_factory=dict)

    @property
    def id(self) -> str:
        key = f"{self.meta['design']}|{self.meta['source']}|{self.meta['location']}|{self.text}"
        return hashlib.sha1(key.encode()).hexdigest()[:16]


def location_label(locations: list[str]) -> str:
    """'Article 7' or 'Article 7 – Article 8' when a chunk spans two."""
    first, last = locations[0], locations[-1]
    return first if first == last else f"{first} – {last}"


def chunk_fixed(blocks: list[Block], size: int, overlap: int) -> list[tuple[str, str, str, list[str]]]:
    words, where = [], []
    for b in blocks:
        for w in b.text.split():
            words.append(w); where.append((b.location, b.heading))
    out, step = [], size - overlap
    for start in range(0, max(len(words) - overlap, 1), step):
        piece = words[start:start + size]
        locs = [where[i][0] for i in range(start, start + len(piece))]
        out.append((" ".join(piece), location_label(locs), where[start][1], list(dict.fromkeys(locs))))
    return out


def chunk_structure(blocks: list[Block], max_words: int) -> list[tuple[str, str, str, list[str]]]:
    units: list[list] = []  # [location, heading, paragraphs]
    for b in blocks:
        if units and units[-1][0] == b.location:
            units[-1][2].append(b.text)
            units[-1][1] = units[-1][1] or b.heading
        else:
            units.append([b.location, b.heading, [b.text]])
    # A unit that is only a heading (e.g. "2. SCOPE ..." followed straight by 2.1) is folded into the next one.
    merged: list[list] = []
    carry: list[str] = []
    for location, heading, paragraphs in units:
        if len(" ".join(paragraphs).split()) < 30:
            carry += paragraphs
            continue
        merged.append([location, heading, carry + paragraphs]); carry = []
    if carry and merged:
        merged[-1][2] += carry
    elif carry:  # a short document where every unit is under 30 words: keep it as one unit
        merged.append([units[0][0], units[0][1], carry])
    units = merged
    out = []
    for location, heading, paragraphs in units:
        piece: list[str] = []
        for para in paragraphs:
            if piece and len(" ".join(piece + [para]).split()) > max_words:
                out.append((" ".join(piece), location, heading, [location])); piece = []
            words = para.split()
            while len(words) > max_words:  # a single huge paragraph (e.g. an annex table)
                out.append((" ".join(words[:max_words]), location, heading, [location])); words = words[max_words:]
            piece.append(" ".join(words))
        if piece:
            out.append((" ".join(piece), location, heading, [location]))
    return out


def chunk_file(path: Path, design: str, source: str | None = None, extra: dict | None = None) -> list[Chunk]:
    """Extract and chunk one file. Used by main() and by server.py's add_document."""
    blocks = extract(Path(path))
    params = DESIGNS[design]
    raw = chunk_fixed(blocks, **params) if design == "fixed" else chunk_structure(blocks, **params)
    source = source or Path(path).stem
    chunks = []
    for i, (text, location, heading, locations) in enumerate(raw):
        # "locations" lists every article/section the chunk touches, so a fixed window that
        # runs from the end of Article 6 through Article 8 still counts as containing Article 7.
        meta = {"source": source, "location": location, "locations": "|".join(locations), "heading": heading,
                "design": design, "chunk": i, "words": len(text.split()), **(extra or {})}
        chunks.append(Chunk(text, meta))
    return chunks


# =============================================================================
# 4. Embed and store
# =============================================================================
def collection(design: str):
    client = chromadb.PersistentClient(path=str(INDEX_DIR / "chroma"))
    return client.get_or_create_collection(f"passenger_rights_{design}", metadata={"hnsw:space": "cosine"})


_client = None


def gemini() -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client(api_key=load_api_key())
    return _client


def embed(texts: list[str], task: str) -> list[list[float]]:
    """Embed texts, waiting and retrying on per-minute rate limits."""
    for attempt in range(6):
        try:
            # One Content per text: gemini-embedding-2 reads a plain list of strings as the
            # parts of a single document and returns one vector for all of them.
            result = gemini().models.embed_content(
                model=EMBED_MODEL, contents=[types.Content(parts=[types.Part(text=t)]) for t in texts],
                config=types.EmbedContentConfig(task_type=task, output_dimensionality=EMBED_DIM),
            )
            return [e.values for e in result.embeddings]
        except Exception as error:  # noqa: BLE001
            message = str(error)
            if "per day" in message.lower() or "PerDay" in message:
                raise SystemExit(
                    "Gemini's daily embedding quota is used up. Everything embedded so far is saved;\n"
                    "run the same command again after 09:00 (Spain) and it continues where it stopped."
                ) from error
            if "429" in message or "RESOURCE_EXHAUSTED" in message or "503" in message:
                wait = 20 * (attempt + 1)
                print(f"  rate limited, waiting {wait}s ...", file=sys.stderr)
                time.sleep(wait)
                continue
            raise
    raise RuntimeError("Embedding kept failing after retries.")


def embed_query(text: str) -> list[float]:
    return embed([text], "RETRIEVAL_QUERY")[0]


def embed_and_store(chunks: list[Chunk], design: str) -> int:
    """Embed only the chunks without a saved vector; save each batch immediately."""
    store = collection(design)
    existing = set(store.get(ids=[c.id for c in chunks])["ids"]) if chunks else set()
    kept = [c for c in chunks if c.id in existing]
    if kept:  # metadata can change without the text changing; refreshing it costs no embeddings
        store.update(ids=[c.id for c in kept], metadatas=[c.meta for c in kept])
    todo = [c for c in chunks if c.id not in existing]
    for i in range(0, len(todo), EMBED_BATCH):
        batch = todo[i:i + EMBED_BATCH]
        vectors = embed([c.text for c in batch], "RETRIEVAL_DOCUMENT")
        store.upsert(ids=[c.id for c in batch], documents=[c.text for c in batch],
                     embeddings=vectors, metadatas=[c.meta for c in batch])
        print(f"  {design}: saved {min(i + EMBED_BATCH, len(todo))}/{len(todo)} new vectors", file=sys.stderr)
    return len(todo)


def search(query: str, design: str, k: int = 5, vector: list[float] | None = None,
           where: dict | None = None) -> list[dict]:
    """Top-k chunks for a query, each with its text and citation metadata."""
    vector = vector or embed_query(query)
    result = collection(design).query(query_embeddings=[vector], n_results=k, where=where)
    return [{"id": i, "text": d, "distance": dist, **m}
            for i, d, m, dist in zip(result["ids"][0], result["documents"][0],
                                     result["metadatas"][0], result["distances"][0])]


def corpus_chunks(design: str) -> list[Chunk]:
    chunks = []
    for doc in DOCS:
        extra = {"mode": doc["mode"], "url": doc["url"], "celex": doc["celex"]}
        chunks += chunk_file(download(doc), design, source=doc["source"], extra=extra)
    return chunks


def main(dry_run: bool = False) -> None:
    for doc in DOCS:
        download(doc)
    for design in DESIGNS:
        chunks = corpus_chunks(design)
        words = [c.meta["words"] for c in chunks]
        print(f"{design}: {len(chunks)} chunks, {sum(words)} words, "
              f"median {sorted(words)[len(words) // 2]} words/chunk, max {max(words)}")
        if not dry_run:
            added = embed_and_store(chunks, design)
            print(f"{design}: {added} embedded this run, {collection(design).count()} in index")


if __name__ == "__main__":
    main(dry_run="--dry-run" in sys.argv)
