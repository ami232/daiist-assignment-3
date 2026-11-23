"""
Assignment 3: build the index (`main.py index`).

Pipeline: download -> extract -> chunk -> embed and store.

    uv run python index.py              # full pipeline (what main.py index runs)
    uv run python index.py --no-embed   # stop before embedding: counts and samples only

The per-file steps are functions so server.py's add_document tool can import them.
"""

import argparse
import hashlib
import re
import statistics
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

import chromadb
import httpx
from bs4 import BeautifulSoup, Tag
from google import genai
from google.genai import errors, types

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"

SE = "https://standardebooks.org/ebooks"

# The works. Each is the "single-page" XHTML edition from Standard Ebooks (texts public
# domain; Standard Ebooks' own work dedicated to the public domain under CC0).
# `chapters` lists the section ids we keep; None keeps every body chapter.
# `in_main_index: False` keeps a work out of `main.py index`: it is added later with add_document.
WORKS = {
    "hobbes_leviathan": {
        "url": f"{SE}/thomas-hobbes/leviathan/text/single-page",
        "source": "Hobbes, Leviathan (1651)",
        "chapters": [f"chapter-{n}" for n in range(13, 22)],
        "in_main_index": True,
    },
    "locke_second-treatise": {
        "url": f"{SE}/john-locke/two-treatises-of-government/text/single-page",
        "file": "locke_two-treatises",
        "source": "Locke, Second Treatise of Government (1689)",
        "chapters": [f"chapter-2-{n}" for n in range(1, 20)],
        "in_main_index": True,
    },
    "mill_on-liberty": {
        "url": f"{SE}/john-stuart-mill/on-liberty/text/single-page",
        "source": "Mill, On Liberty (1859)",
        "chapters": [f"chapter-{n}" for n in range(1, 6)],
        "in_main_index": True,
    },
    "wollstonecraft_vindication": {
        "url": f"{SE}/mary-wollstonecraft/a-vindication-of-the-rights-of-woman/text/single-page",
        "source": "Wollstonecraft, A Vindication of the Rights of Woman (1792)",
        "chapters": None,
        "in_main_index": False,
    },
}

# Chunking: whole paragraphs, grouped up to about TARGET_WORDS; a paragraph longer than
# MAX_WORDS is split at sentence ends. Chunks never cross a chapter.
TARGET_WORDS = 200
MAX_WORDS = 300

# Embeddings. 768 dimensions keeps index/ small; vectors come back normalised.
EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768
BATCH_SIZE = 50
COLLECTION = "corpus"


def log(message: str) -> None:
    """Progress goes to stderr, so the same functions are safe inside the MCP server."""
    print(message, file=sys.stderr, flush=True)


# --------------------------------------------------------------------------- 1. download

def download(name: str, url: str, corpus_dir: Path = CORPUS_DIR) -> Path:
    """Save one work into corpus/ unless it is already there."""
    corpus_dir.mkdir(exist_ok=True)
    path = corpus_dir / f"{name}.xhtml"
    if path.exists() and path.stat().st_size > 0:
        log(f"  have      {path.name}")
        return path
    response = httpx.get(url, follow_redirects=True, timeout=60, headers={"User-Agent": "daiist-assignment-3 (course project)"})
    response.raise_for_status()
    path.write_bytes(response.content)
    log(f"  download  {path.name} ({len(response.content) / 1e6:.1f} MB)")
    return path


def download_all() -> dict[str, Path]:
    log("1. Download")
    paths = {}
    for name, work in WORKS.items():
        paths[name] = download(work.get("file", name), work["url"])
    return paths


# --------------------------------------------------------------------------- 2. extract

# Standard Ebooks typesetting characters that would otherwise end up inside words or
# between them: word joiner, hair space, no-break space, zero-width space, soft hyphen.
INVISIBLE = {"⁠": "", "​": "", "­": "", " ": " ", " ": " "}


def clean(text: str) -> str:
    for char, replacement in INVISIBLE.items():
        text = text.replace(char, replacement)
    return re.sub(r"\s+", " ", text).strip()


@dataclass
class Chapter:
    source: str          # "Locke, Second Treatise of Government (1689)"
    doc_id: str          # "locke_second-treatise"
    section_id: str      # "chapter-2-2", the id in the XHTML
    location: str        # "Chapter II: Of the State of Nature"
    paragraphs: list[str] = field(default_factory=list)


def heading_of(section: Tag) -> str:
    """'Chapter XIII: Of the Natural Condition…' from an hgroup/header, or just 'Chapter XIII'."""
    head = section.find(["hgroup", "header"], recursive=False) or section.find(["h2", "h3", "h4"], recursive=False)
    if head is None:
        return section.get("id", "")
    number = head.find(["h2", "h3", "h4"]) if head.name in ("hgroup", "header") else head
    title = head.find("p") if head.name in ("hgroup", "header") else None
    label = f"Chapter {clean(number.get_text())}" if number else ""
    if title:
        label += f": {clean(title.get_text()).rstrip('.')}"
    return label or section.get("id", "")


def block_text(block: Tag) -> str:
    for ref in block.select('a[epub\\:type~="noteref"]'):  # footnote markers like the "2" in "law2"
        ref.decompose()
    if block.name in ("ol", "ul"):
        return " ".join(clean(li.get_text(" ")) for li in block.find_all("li"))
    return clean(block.get_text(" "))


def extract(path: Path, doc_id: str, source: str, chapters: list[str] | None = None) -> list[Chapter]:
    """Read one Standard Ebooks XHTML file and return its body chapters, in order.

    Keeps only body text: paragraphs, block quotes and lists directly inside a chapter.
    Title pages, imprint, introductions by editors, endnotes and colophon are skipped.
    """
    soup = BeautifulSoup(path.read_bytes(), "html.parser")
    if chapters is None:
        sections = [s for s in soup.find_all("section") if "chapter" in (s.get("epub:type") or "").split()]
    else:
        sections = [soup.find("section", id=sid) for sid in chapters]
        missing = [sid for sid, s in zip(chapters, sections) if s is None]
        if missing:
            raise ValueError(f"{path.name}: sections not found: {missing}")

    result = []
    for section in sections:
        chapter = Chapter(source, doc_id, section["id"], heading_of(section))
        # Paragraphs sit directly in the chapter, or in its subchapters (Wollstonecraft V, XIII).
        holders = [section] + section.find_all("section")
        for holder in holders:
            for block in holder.find_all(["p", "blockquote", "ol", "ul"], recursive=False):
                text = block_text(block)
                if text:
                    chapter.paragraphs.append(text)
        if chapter.paragraphs:
            result.append(chapter)
    return result


# --------------------------------------------------------------------------- 3. chunk

@dataclass
class Chunk:
    id: str
    doc_id: str
    source: str
    location: str        # "Chapter II: Of the State of Nature, ¶3–5"
    chapter: str         # "Chapter II: Of the State of Nature"
    paragraphs: str      # "3-5"
    words: int
    text: str

    def text_for_embedding(self) -> str:
        """The chunk with its citation in front, so the vector also knows author and chapter."""
        return f"{self.source}. {self.chapter}.\n\n{self.text}"


def split_long(paragraph: str) -> list[str]:
    """Split a paragraph over MAX_WORDS at sentence ends into pieces of about TARGET_WORDS."""
    if len(paragraph.split()) <= MAX_WORDS:
        return [paragraph]
    sentences = re.split(r"(?<=[.;:?!])\s+(?=[“‘A-Z])", paragraph)
    pieces, current = [], []
    for sentence in sentences:
        if current and len(" ".join(current + [sentence]).split()) > TARGET_WORDS:
            pieces.append(" ".join(current))
            current = []
        current.append(sentence)
    if current:
        pieces.append(" ".join(current))
    return pieces


def chunk_chapter(chapter: Chapter) -> list[Chunk]:
    """Group whole paragraphs up to about TARGET_WORDS; never cross the chapter."""
    units = []  # (paragraph number, piece of text)
    for number, paragraph in enumerate(chapter.paragraphs, start=1):
        units.extend((number, piece) for piece in split_long(paragraph))

    groups, current = [], []
    for unit in units:
        words = sum(len(t.split()) for _, t in current)
        new_total = words + len(unit[1].split())
        if current and (new_total > MAX_WORDS or (new_total > TARGET_WORDS and words >= TARGET_WORDS // 2)):
            groups.append(current)
            current = []
        current.append(unit)
    if current:
        groups.append(current)

    chunks = []
    for group in groups:
        first, last = group[0][0], group[-1][0]
        paragraphs = str(first) if first == last else f"{first}-{last}"
        text = "\n\n".join(t for _, t in group)
        digest = hashlib.sha1(text.encode("utf-8")).hexdigest()[:10]
        chunks.append(Chunk(
            id=f"{chapter.doc_id}:{chapter.section_id}:p{paragraphs}:{digest}",
            doc_id=chapter.doc_id,
            source=chapter.source,
            location=f"{chapter.location}, ¶{paragraphs.replace('-', '–')}",
            chapter=chapter.location,
            paragraphs=paragraphs,
            words=len(text.split()),
            text=text,
        ))
    return chunks


def chunk_file(path: Path, doc_id: str, source: str, chapters: list[str] | None = None) -> list[Chunk]:
    """Extract and chunk one file. server.py's add_document calls this."""
    return [chunk for chapter in extract(path, doc_id, source, chapters) for chunk in chunk_chapter(chapter)]


def chunk_corpus(paths: dict[str, Path], main_only: bool = True) -> list[Chunk]:
    log("2-3. Extract and chunk")
    chunks = []
    for name, work in WORKS.items():
        if main_only and not work["in_main_index"]:
            continue
        work_chunks = chunk_file(paths[name], name, work["source"], work["chapters"])
        words = sum(c.words for c in work_chunks)
        log(f"  {work['source']:<62} {words:>7,} words  {len(work_chunks):>4} chunks")
        chunks.extend(work_chunks)
    return chunks


def report(chunks: list[Chunk]) -> None:
    sizes = [c.words for c in chunks]
    log(f"\n  Total: {sum(sizes):,} words in {len(chunks)} chunks "
        f"(words per chunk: median {statistics.median(sizes):.0f}, min {min(sizes)}, max {max(sizes)})")
    assert len({c.id for c in chunks}) == len(chunks), "chunk ids are not unique"


# --------------------------------------------------------------------------- 4. embed and store

class QuotaExhausted(RuntimeError):
    """The daily embedding quota is used up. Vectors saved so far are kept."""


def get_collection(index_dir: Path = INDEX_DIR):
    """The ChromaDB collection in index/, created on first use (cosine distance)."""
    client = chromadb.PersistentClient(path=str(index_dir / "chroma"))
    return client.get_or_create_collection(COLLECTION, metadata={"hnsw:space": "cosine"})


_client: genai.Client | None = None


def embed(texts: list[str], task_type: str = "RETRIEVAL_DOCUMENT", retries: int = 5) -> list[list[float]]:
    """One Gemini call for a batch of texts.

    Each text goes in its own Content: gemini-embedding-2 merges a plain list of
    strings into ONE embedding. Rate limits are retried; the daily quota raises.
    """
    global _client
    _client = _client or genai.Client(api_key=load_api_key())
    contents = [types.Content(parts=[types.Part(text=t)]) for t in texts]
    config = types.EmbedContentConfig(task_type=task_type, output_dimensionality=EMBED_DIM)
    for attempt in range(retries):
        try:
            result = _client.models.embed_content(model=EMBED_MODEL, contents=contents, config=config)
            vectors = [e.values for e in result.embeddings]
            if len(vectors) != len(texts):
                raise RuntimeError(f"asked for {len(texts)} embeddings, got {len(vectors)}")
            return vectors
        except errors.ClientError as error:
            if error.code != 429:
                raise
            if "PerDay" in str(error) or "per day" in str(error).lower():
                raise QuotaExhausted(str(error)[:300]) from error
            wait = 15 * (attempt + 1)
            log(f"  rate limited, waiting {wait}s")
            time.sleep(wait)
    raise RuntimeError("still rate limited after retries")


def embed_and_store(chunks: list[Chunk], collection=None) -> int:
    """Embed only the chunks that have no saved vector; save each batch as soon as it arrives.

    Returns how many chunks were embedded now. server.py's add_document calls this.
    """
    collection = collection or get_collection()
    ids = [c.id for c in chunks]
    have = set()
    for start in range(0, len(ids), 500):
        have.update(collection.get(ids=ids[start:start + 500], include=[])["ids"])
    todo = [c for c in chunks if c.id not in have]
    log(f"4. Embed and store: {len(have)} chunks already have a vector, {len(todo)} to embed")

    done = 0
    for start in range(0, len(todo), BATCH_SIZE):
        batch = todo[start:start + BATCH_SIZE]
        vectors = embed([c.text_for_embedding() for c in batch])
        collection.upsert(
            ids=[c.id for c in batch],
            embeddings=vectors,
            documents=[c.text for c in batch],
            metadatas=[{
                "doc_id": c.doc_id, "source": c.source, "location": c.location,
                "chapter": c.chapter, "paragraphs": c.paragraphs, "words": c.words,
            } for c in batch],
        )
        done += len(batch)
        log(f"  saved {done}/{len(todo)}")
    return done


def prune(chunks: list[Chunk], collection=None) -> int:
    """Remove saved chunks of these documents that the current chunking no longer produces."""
    collection = collection or get_collection()
    keep = {c.id for c in chunks}
    stale = []
    for doc_id in {c.doc_id for c in chunks}:
        stale += [i for i in collection.get(where={"doc_id": doc_id}, include=[])["ids"] if i not in keep]
    if stale:
        collection.delete(ids=stale)
        log(f"  removed {len(stale)} outdated chunks")
    return len(stale)


# --------------------------------------------------------------------------- main

def main() -> None:
    parser = argparse.ArgumentParser(description="Build the index.")
    parser.add_argument("--no-embed", action="store_true", help="stop before embedding")
    args = parser.parse_args()
    paths = download_all()
    chunks = chunk_corpus(paths)
    report(chunks)
    if args.no_embed:
        return
    collection = get_collection()
    prune(chunks, collection)
    try:
        embed_and_store(chunks, collection)
    except QuotaExhausted as error:
        log(f"\nDaily embedding quota reached. Saved vectors are kept; run again after 09:00 (Spain).\n  {error}")
        sys.exit(1)
    log(f"\nindex/ holds {collection.count()} chunks.")


if __name__ == "__main__":
    main()
