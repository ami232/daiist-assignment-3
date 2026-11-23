"""Index stage: download the corpus, chunk it, embed the chunks with Gemini, store them in index/.

    uv run python main.py index                  # every design; embeds only chunks without a saved vector
    uv run python index.py --dry-run             # count what would be embedded, spends nothing
    uv run python index.py --design fixed150     # one design only (about 470 texts of the daily quota)
    uv run python index.py --design section300   # the other design (about 300 texts)

server.py imports chunk_file, embed_and_store, embed_query and get_collection from this file.
Everything it prints goes to stderr, because the MCP server uses stdout for the protocol.

Two chunking designs are kept side by side, one ChromaDB collection each, so the evaluation can
compare them:
    fixed150    windows of 150 words, 20 words of overlap, cut without looking at the structure
    section300  one chunk per section (heading); sections over 300 words are cut at paragraph ends

Each chunk carries its source (file name without extension), its title, its location (the section
heading, or "page N" for a PDF) and the URL it came from.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from pathlib import Path

import chromadb
from chromadb.config import Settings

from fetch_corpus import CORPUS_DIR, download_corpus, html_to_markdown

ROOT = Path(__file__).resolve().parent
INDEX_DIR = ROOT / "index"
QUERY_CACHE = INDEX_DIR / "query_cache.json"

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768  # 768 is one of the sizes Google recommends; the model normalises it itself
BATCH_SIZE = 20  # each text in a batch counts against the daily quota
MAX_NEW_DEFAULT = 900  # safety stop per run, so a bug cannot burn the whole daily quota

DESIGNS = {
    "fixed150": {"kind": "fixed", "size": 150, "overlap": 20},
    "section300": {"kind": "section", "max_words": 300},
}
ACTIVE_DESIGN = "section300"  # the design server.py searches; change it after comparing hit rates
MIN_SECTION_WORDS = 20  # sections shorter than this are page furniture (a bare title, a link)

HEADING = re.compile(r"^#{1,6}\s+(\S.*?)\s*$")
FOOTNOTE = re.compile(r"[ \t]?\[\d{1,3}\]")  # "[6]" markers: they would end up inside headings and citations


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


# --------------------------------------------------------------------------- reading and chunking


def read_document(path: Path) -> tuple[dict, str]:
    """Return (metadata, markdown text) for a .md, .txt, .html or .pdf file, without footnote markers."""
    meta, markdown = _read_raw(path)
    return meta, FOOTNOTE.sub("", markdown)


def _read_raw(path: Path) -> tuple[dict, str]:
    suffix = path.suffix.lower()
    meta = {"title": path.stem, "url": path.name, "retrieved": ""}
    if suffix == ".pdf":
        from pypdf import PdfReader

        pages = [(page.extract_text() or "") for page in PdfReader(str(path)).pages]
        markdown = "\n\n".join(f"## page {n}\n\n{text}" for n, text in enumerate(pages, 1) if text.strip())
        return meta, markdown
    text = path.read_text(encoding="utf-8", errors="replace")
    if suffix in {".html", ".htm"}:
        return meta, html_to_markdown(text)
    if text.startswith("---"):
        parts = text.split("---", 2)
        if len(parts) == 3:
            for line in parts[1].splitlines():
                key, _, value = line.partition(":")
                key, value = key.strip(), value.strip()
                if key == "title":
                    try:
                        value = json.loads(value)
                    except ValueError:
                        pass
                    meta["title"] = value or meta["title"]
                elif key == "source_url":
                    meta["url"] = value or meta["url"]
                elif key == "retrieved":
                    meta["retrieved"] = value
            text = parts[2]
    return meta, text.strip()


def split_sections(markdown: str) -> list[tuple[str, str]]:
    """[(heading, body)]. Text before the first heading gets the heading ''. Empty sections are dropped."""
    sections: list[tuple[str, str]] = []
    heading, lines = "", []
    for line in markdown.splitlines():
        match = HEADING.match(line)
        if match:
            sections.append((heading, "\n".join(lines).strip()))
            heading, lines = match.group(1).strip(), []
        else:
            lines.append(line)
    sections.append((heading, "\n".join(lines).strip()))
    return [(h, b) for h, b in sections if b]


def pack(units: list[str], max_words: int, sep: str) -> list[str]:
    """Join consecutive units into pieces of at most max_words (a unit is never cut here)."""
    out, current, count = [], [], 0
    for unit in units:
        words = len(unit.split())
        if current and count + words > max_words:
            out.append(sep.join(current))
            current, count = [], 0
        current.append(unit)
        count += words
    if current:
        out.append(sep.join(current))
    return out


def split_long(text: str, max_words: int) -> list[str]:
    """Cut a long section at paragraph ends; a paragraph that is itself too long is cut at sentence ends."""
    if len(text.split()) <= max_words:
        return [text]
    units: list[str] = []
    for paragraph in re.split(r"\n\s*\n", text):
        paragraph = paragraph.strip()
        if not paragraph:
            continue
        if len(paragraph.split()) <= max_words:
            units.append(paragraph)
            continue
        sentences: list[str] = []
        for sentence in re.split(r"(?<=[.!?])\s+", paragraph):
            words = sentence.split()
            for i in range(0, len(words), max_words):  # a single sentence over max_words is cut too
                sentences.append(" ".join(words[i:i + max_words]))
        units.extend(pack(sentences, max_words, " "))
    return pack(units, max_words, "\n\n")


def fixed_chunks(sections: list[tuple[str, str]], size: int, overlap: int) -> list[tuple[str, str]]:
    """Sliding windows over the words of the whole document. Location = heading of the window's first word."""
    stream = [(word, heading) for heading, body in sections for word in f"{heading} {body}".split()]
    step = size - overlap
    chunks = []
    for start in range(0, len(stream), step):
        window = stream[start:start + size]
        chunks.append((window[0][1], " ".join(word for word, _ in window)))
        if start + size >= len(stream):
            break
    return chunks


def chunk_id(design: str, source: str, location: str, text: str) -> str:
    return hashlib.sha1(f"{design}|{source}|{location}|{text}".encode("utf-8")).hexdigest()[:20]


def chunk_file(path, design: str | None = None) -> list[dict]:
    """Extract, clean and chunk one file. Every chunk has: id, text, source, title, location, url, ..."""
    design = design or ACTIVE_DESIGN
    config = DESIGNS[design]
    path = Path(path)
    meta, markdown = read_document(path)
    sections = split_sections(markdown)
    if config["kind"] == "fixed":
        pieces = fixed_chunks(sections, config["size"], config["overlap"])
    else:
        pieces = [(heading, part)
                  for heading, body in sections if len(body.split()) >= MIN_SECTION_WORDS
                  for part in split_long(body, config["max_words"])]
    source = path.stem
    chunks = []
    for number, (location, text) in enumerate(pieces):
        location = location or "(intro)"
        chunks.append({
            "id": chunk_id(design, source, location, text),
            "text": text,
            "source": source,
            "title": meta["title"],
            "location": location,
            "url": meta["url"],
            "retrieved": meta["retrieved"],
            "design": design,
            "chunk_index": number,
            "words": len(text.split()),
        })
    return chunks


# --------------------------------------------------------------------------- embedding


class DailyQuotaExceeded(RuntimeError):
    """The free tier's daily limit is used up. Vectors already stored are kept."""


_CLIENT = None


def _client():
    """One Client for the whole run. It must stay referenced: if it is a temporary object, Python
    deletes it and closes its connection before the request is sent."""
    global _CLIENT
    if _CLIENT is None:
        from google import genai

        from api_key import load_api_key

        _CLIENT = genai.Client(api_key=load_api_key())
    return _CLIENT


def _embed_batch(texts: list[str]) -> list[list[float]]:
    """One API call. gemini-embedding-2 merges a plain list of strings into ONE vector, so each text
    is wrapped in its own Content to get one vector per text."""
    from google.genai import types

    contents = [types.Content(parts=[types.Part.from_text(text=text)]) for text in texts]
    response = _client().models.embed_content(
        model=EMBED_MODEL, contents=contents,
        config=types.EmbedContentConfig(output_dimensionality=EMBED_DIM))
    vectors = [list(item.values) for item in response.embeddings]
    if len(vectors) != len(texts):
        raise RuntimeError(f"asked for {len(texts)} vectors, got {len(vectors)}")
    return vectors


def _embed_with_retry(texts: list[str]) -> list[list[float]]:
    for attempt in range(1, 6):
        try:
            return _embed_batch(texts)
        except Exception as error:  # noqa: BLE001
            message = str(error)
            if "429" in message or "RESOURCE_EXHAUSTED" in message:
                if re.search(r"per ?day|daily", message, re.IGNORECASE):
                    raise DailyQuotaExceeded(message[:300]) from error
                wait = 15 * attempt
                log(f"rate limited, waiting {wait}s (attempt {attempt}/5)")
                time.sleep(wait)
                continue
            raise
    raise RuntimeError("embedding failed after 5 attempts")


def embedding_text(chunk: dict) -> str:
    """Document format that Google prescribes for gemini-embedding-2 (it has no task_type)."""
    return f"title: {chunk['title']} > {chunk['location']} | text: {chunk['text']}"


def _load_cache() -> dict:
    try:
        return json.loads(QUERY_CACHE.read_text(encoding="utf-8"))
    except (OSError, ValueError):
        return {}


def embed_query(text: str) -> list[float]:
    """Embed a question. Vectors are cached on disk (index/query_cache.json), so asking the same
    question again, or re-running the evaluation, costs nothing."""
    cache = _load_cache()
    key = hashlib.sha1(text.encode("utf-8")).hexdigest()
    if key not in cache:
        cache[key] = [round(v, 6) for v in _embed_with_retry([f"task: search result | query: {text}"])[0]]
        INDEX_DIR.mkdir(exist_ok=True)
        temporary = QUERY_CACHE.with_suffix(".tmp")
        temporary.write_text(json.dumps(cache), encoding="utf-8")
        temporary.replace(QUERY_CACHE)
    return cache[key]


# --------------------------------------------------------------------------- storage


def get_collection(design: str | None = None):
    INDEX_DIR.mkdir(exist_ok=True)
    client = chromadb.PersistentClient(path=str(INDEX_DIR), settings=Settings(anonymized_telemetry=False))
    return client.get_or_create_collection(name=design or ACTIVE_DESIGN, configuration={"hnsw": {"space": "cosine"}})


def embed_and_store(chunks: list[dict], design: str | None = None, dry_run: bool = False,
                    max_new: int | None = None) -> dict:
    """Embed the chunks that have no saved vector yet and store them, one batch at a time.

    Chunk ids are a hash of design, source, location and text, so:
      - a chunk already stored is skipped (no embedding, no duplicate);
      - re-adding an unchanged document costs nothing;
      - re-adding a changed document replaces it: chunks of that source that are no longer
        produced are deleted, new ones are embedded.
    """
    design = design or ACTIVE_DESIGN
    collection = get_collection(design)
    unique = list({chunk["id"]: chunk for chunk in chunks}.values())
    new_ids = {chunk["id"] for chunk in unique}

    removed = 0
    for source in sorted({chunk["source"] for chunk in unique}):
        old = set(collection.get(where={"source": source}, include=[])["ids"])
        stale = sorted(old - new_ids)
        if stale and not dry_run:
            collection.delete(ids=stale)
        removed += len(stale)

    ids = [chunk["id"] for chunk in unique]
    have: set[str] = set()
    for i in range(0, len(ids), 200):
        have.update(collection.get(ids=ids[i:i + 200], include=[])["ids"])
    todo = [chunk for chunk in unique if chunk["id"] not in have]

    stats = {"design": design, "chunks": len(unique), "already_stored": len(have),
             "to_embed": len(todo), "embedded": 0, "removed_stale": removed, "left_over": 0}
    if dry_run or not todo:
        return stats
    if max_new is not None and len(todo) > max_new:
        stats["left_over"] = len(todo) - max_new
        todo = todo[:max_new]

    for i in range(0, len(todo), BATCH_SIZE):
        batch = todo[i:i + BATCH_SIZE]
        vectors = _embed_with_retry([embedding_text(chunk) for chunk in batch])
        collection.upsert(  # saved right away: a crash or the daily limit loses nothing
            ids=[chunk["id"] for chunk in batch],
            embeddings=vectors,
            documents=[chunk["text"] for chunk in batch],
            metadatas=[{k: v for k, v in chunk.items() if k not in ("id", "text")} for chunk in batch])
        stats["embedded"] += len(batch)
        log(f"  [{design}] embedded {stats['embedded']}/{len(todo)}")
        time.sleep(0.3)
    return stats


# --------------------------------------------------------------------------- command line


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("--design", action="append", choices=list(DESIGNS),
                        help="design to index (repeat for several); default: all")
    parser.add_argument("--dry-run", action="store_true", help="count only; nothing is embedded or stored")
    parser.add_argument("--max-new", type=int, default=MAX_NEW_DEFAULT,
                        help=f"stop after this many new embeddings (default {MAX_NEW_DEFAULT})")
    args = parser.parse_args(argv)
    designs = args.design or list(DESIGNS)

    failures = download_corpus()
    if failures:
        log(f"{len(failures)} document(s) could not be downloaded; indexing the ones that are in corpus/")
    files = sorted(CORPUS_DIR.glob("*.md"))
    if not files:
        log("corpus/ is empty and nothing could be downloaded.")
        return 1

    budget = args.max_new
    exit_code = 0
    for design in designs:
        chunks = [chunk for file in files for chunk in chunk_file(file, design)]
        try:
            stats = embed_and_store(chunks, design, dry_run=args.dry_run, max_new=budget)
        except DailyQuotaExceeded as error:
            log(f"\nDaily embedding quota reached; what was embedded is saved. Run again after 09:00 (Spain).\n{error}")
            return 2
        budget -= stats["embedded"]
        log(f"{design}: {stats['chunks']} chunks | already stored {stats['already_stored']} | "
            f"to embed {stats['to_embed']} | embedded now {stats['embedded']} | "
            f"stale removed {stats['removed_stale']} | left for a later run {stats['left_over']}")
        if stats["left_over"]:
            exit_code = 2
    if args.dry_run:
        log("dry run: nothing was embedded.")
    return exit_code


if __name__ == "__main__":
    sys.exit(main())