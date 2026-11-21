"""
Assignment 3: build the index (`main.py index`). May be index.ipynb instead.

Download the corpus (into corpus/, git-ignored), extract, clean and chunk it
with source and location metadata, embed with Gemini, and store everything in
index/. Save each vector as you get it and embed only chunks without one.

Write the per-file steps as functions (e.g. `chunk_file(path)`,
`embed_and_store(chunks)`): server.py's add-document tool imports them.

Useful commands:
    uv run python index.py --dry-run          # chunk only, no embedding, no quota used
    uv run python index.py --only vox_2023    # index one document
    uv run python index.py                    # index everything (what main.py index does)
"""

import argparse
import hashlib
import json
import logging
import os
import re
import sys
import time
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"
CHROMA_DIR = INDEX_DIR / "chroma"
QUERY_CACHE = INDEX_DIR / "query_cache.json"

# ---- Design choices (these go in your report) ------------------------------
EMBED_MODEL = "gemini-embedding-2"
EMBED_DIMS = 768          # 3072 is the default; 768 is a recommended size and keeps index/ small
CHUNK_WORDS = 450         # about 600 tokens: fits the quota (see SETUP.md) and keeps a measure with its context
OVERLAP_WORDS = 50        # neighbouring chunks share 50 words, so a sentence cut at the edge appears whole in one
MIN_TAIL_WORDS = 150      # a last piece shorter than this is merged into the chunk before it
MIN_PAGE_WORDS = 40       # pages with fewer words (covers, dividers, quote cards) are not indexed
REPEAT_SHARE = 0.20       # a line that appears on 20% of the pages is a header or footer
BATCH = 10                # chunks per embedding request; vectors are saved after each batch

# ---- The corpus -----------------------------------------------------------
# skip_pages: PDF page numbers (1 = first page of the file) that are not content
# (cover, table of contents, section dividers). Pages are numbered as the PDF
# viewer shows them, NOT as printed on the page. Citations use the same numbers.
SOURCES = {
    "psoe_2023": dict(
        party="PSOE", year=2023, skip_pages="1-11",
        url="https://www.elindependiente.com/wp-content/uploads/2023/07/ProgramaElectoral_ElexGenerales_PSOE_2023.pdf",
    ),
    "pp_2023": dict(
        party="PP", year=2023, skip_pages="1-5",
        url="https://www.pp.es/wp-content/uploads/2023/07/programa_electoral_pp_23j_feijoo_2023.pdf",
    ),
    "sumar_2023": dict(
        party="SUMAR", year=2023, skip_pages="1-6",
        url="https://movimientosumar.es/wp-content/uploads/2023/07/Un-Programa-para-ti.pdf",
    ),
    "vox_2023": dict(
        party="VOX", year=2023, skip_pages="1-6",
        url="https://theobjective.com/wp-content/uploads/2023/07/programa-vox-23j.pdf",
    ),
}


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


# ============================================================================
# 1. Getting the files
# ============================================================================
def ensure_file(source: str) -> Path | None:
    """Return corpus/<source>.pdf, downloading it first if it is not there."""
    path = CORPUS_DIR / f"{source}.pdf"
    if path.is_file():
        return path
    url = SOURCES.get(source, {}).get("url")
    if not url:
        log(f"WARNING: {path} is missing and {source} has no url.")
        return None
    import httpx

    log(f"Downloading {source} from {url} ...")
    try:
        response = httpx.get(url, follow_redirects=True, timeout=120,
                             headers={"User-Agent": "Mozilla/5.0 (corpus downloader)"})
        response.raise_for_status()
    except Exception as error:  # noqa: BLE001 - report any failure plainly
        log(f"WARNING: could not download {source}: {error}")
        return None
    if not response.content.startswith(b"%PDF"):
        log(f"WARNING: {url} did not return a PDF (it returned a web page?).")
        return None
    CORPUS_DIR.mkdir(exist_ok=True)
    path.write_bytes(response.content)
    return path


# ============================================================================
# 2. Extracting and cleaning
# ============================================================================
def parse_pages(spec: str) -> set[int]:
    """'1-11,15' -> {1, 2, ..., 11, 15}"""
    pages: set[int] = set()
    for part in filter(None, (p.strip() for p in spec.split(","))):
        if "-" in part:
            first, last = part.split("-")
            pages.update(range(int(first), int(last) + 1))
        else:
            pages.add(int(part))
    return pages


# Extraction problem we hit: the Vox 2023 PDF stores the "fi" ligature in a way that comes out as
# two Chinese characters ("de昀椀ende" instead of "defiende"). Left alone, searching for "defiende"
# would never match. We map those characters back to letters, and expand real ligature characters.
LIGATURES = str.maketrans({"昀": "f", "椀": "i", "氀": "l",
                           "ﬁ": "fi", "ﬂ": "fl", "ﬀ": "ff", "ﬃ": "ffi", "ﬄ": "ffl"})


def read_pages(path: Path) -> list[str]:
    """Raw text of every page, in order (page 1 is element 0)."""
    import pypdf

    logging.getLogger("pypdf").setLevel(logging.ERROR)  # silence font warnings
    reader = pypdf.PdfReader(str(path))
    return [(page.extract_text() or "").translate(LIGATURES) for page in reader.pages]


def line_key(line: str) -> str:
    """A line with its digits blanked, so 'MADRID 7 DE JULIO' and 'MADRID 8 DE JULIO' match."""
    return re.sub(r"\d+", "#", line.strip())


def find_repeated_lines(pages: list[str]) -> set[str]:
    """Short lines that appear on many pages: running headers and footers."""
    counts: Counter = Counter()
    for raw in pages:
        keys = {line_key(l) for l in raw.splitlines() if l.strip() and len(l.strip()) <= 80}
        counts.update(keys)
    threshold = max(3, REPEAT_SHARE * len(pages))
    return {key for key, n in counts.items() if n >= threshold}


def clean_text(raw: str, repeated: set[str]) -> str:
    kept = []
    for line in raw.splitlines():
        stripped = line.strip()
        if not stripped or line_key(stripped) in repeated:
            continue
        if re.fullmatch(r"[\W_]*\d{1,3}[\W_]*", stripped):  # a lone page number such as "41" or "/41"
            continue
        kept.append(stripped)
    text = "\n".join(kept)
    # Words split across two lines: "na -\ntalidad" and "pre-\nvención" become one word.
    text = re.sub(r"([a-záéíóúñü])\s?-\n([a-záéíóúñü])", r"\1\2", text)
    return " ".join(text.split())


def prepare_pages(raw_pages: list[str], skip: set[int]) -> tuple[dict[int, str], Counter]:
    """Return ({page number: clean text} for the pages worth indexing, counts of what was dropped)."""
    dropped: Counter = Counter()
    candidates: dict[int, str] = {}
    for number, raw in enumerate(raw_pages, start=1):
        if number in skip:
            dropped["listed in skip_pages"] += 1
        elif len(re.findall(r"\.{5,}", raw)) >= 4:  # dotted leaders: a table of contents
            dropped["table of contents"] += 1
        else:
            candidates[number] = raw
    repeated = find_repeated_lines(list(candidates.values()))
    pages: dict[int, str] = {}
    for number, raw in candidates.items():
        text = clean_text(raw, repeated)
        if len(text.split()) < MIN_PAGE_WORDS:
            dropped[f"under {MIN_PAGE_WORDS} words"] += 1
        else:
            pages[number] = text
    return pages, dropped


# ============================================================================
# 3. Chunking
# ============================================================================
def source_info(path: Path) -> dict:
    """Source id, party and year for a file: from SOURCES, else guessed from the file name."""
    source = path.stem
    if source in SOURCES:
        return {"source": source, "party": SOURCES[source]["party"], "year": SOURCES[source]["year"],
                "skip": parse_pages(SOURCES[source].get("skip_pages", ""))}
    match = re.match(r"([A-Za-z]+)[_-]?(\d{4})", source)
    party = match.group(1).upper() if match else source.upper()
    year = int(match.group(2)) if match else 0
    return {"source": source, "party": party, "year": year, "skip": set()}


def location_of(first: int, last: int) -> str:
    return f"p. {first}" if first == last else f"pp. {first}-{last}"


def chunk_file(path: str | Path) -> tuple[list[dict], Counter]:
    """Cut one PDF into chunks. Returns (chunks, counts of dropped pages).

    Each chunk: id, text, source, party, year, page_start, page_end, location, n_words.
    """
    path = Path(path)
    info = source_info(path)
    pages, dropped = prepare_pages(read_pages(path), info["skip"])

    words: list[tuple[str, int]] = [(w, n) for n, text in pages.items() for w in text.split()]
    chunks: list[dict] = []
    start, total, step = 0, len(words), CHUNK_WORDS - OVERLAP_WORDS
    while start < total:
        end = start + CHUNK_WORDS
        if total - end < MIN_TAIL_WORDS:  # do not leave a tiny last chunk
            end = total
        window = words[start:end]
        text = " ".join(w for w, _ in window)
        first, last = window[0][1], window[-1][1]
        chunks.append({
            "id": f"{info['source']}-p{first}-{hashlib.sha1(text.encode()).hexdigest()[:8]}",
            "text": text,
            "source": info["source"], "party": info["party"], "year": info["year"],
            "page_start": first, "page_end": last, "location": location_of(first, last),
            "n_words": len(window),
        })
        if end >= total:
            break
        start += step
    return chunks, dropped


# ============================================================================
# 4. Embedding and storing
# ============================================================================
class DailyQuotaError(RuntimeError):
    pass


def fake_vector(text: str) -> list[float]:
    """Deterministic stand-in vector for testing the pipeline without spending quota (FAKE_EMBED=1)."""
    import random

    rng = random.Random(hashlib.sha1(text.encode()).hexdigest())
    return [rng.uniform(-1, 1) for _ in range(EMBED_DIMS)]


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed texts with Gemini; one vector per text. Retries per-minute limits, stops on the daily one."""
    if os.environ.get("FAKE_EMBED"):
        return [fake_vector(t) for t in texts]
    from google import genai
    from google.genai import errors, types

    from api_key import load_api_key

    client = genai.Client(api_key=load_api_key())
    # One Content per text: a plain list of strings would come back as ONE merged vector.
    contents = [types.Content(parts=[types.Part.from_text(text=t)]) for t in texts]
    config = types.EmbedContentConfig(output_dimensionality=EMBED_DIMS)
    delay = 10
    for attempt in range(6):
        try:
            result = client.models.embed_content(model=EMBED_MODEL, contents=contents, config=config)
            return [e.values for e in result.embeddings]
        except errors.APIError as error:
            message = str(error)
            if error.code == 429 and re.search(r"per ?day|PerDay", message, re.I):
                raise DailyQuotaError(message) from error
            if error.code in (429, 500, 503) and attempt < 5:
                log(f"  Gemini said {error.code}; waiting {delay}s and trying again ...")
                time.sleep(delay)
                delay = min(delay * 2, 60)
                continue
            raise
    raise RuntimeError("unreachable")


def document_text(chunk: dict) -> str:
    """What gets embedded: Google's document format for gemini-embedding-2 (no task_type for this model)."""
    return f"title: {chunk['party']} {chunk['year']} | text: {chunk['text']}"


def get_collection():
    import chromadb
    from chromadb.config import Settings

    client = chromadb.PersistentClient(path=str(CHROMA_DIR), settings=Settings(anonymized_telemetry=False))
    return client.get_or_create_collection("chunks", metadata={"hnsw:space": "cosine"})


def embed_and_store(chunks: list[dict]) -> dict:
    """Store chunks of ONE document. Embeds only chunks that are not stored yet.

    Already indexed, unchanged  -> nothing is embedded (0 quota).
    Already indexed, changed    -> only the changed chunks are embedded; stored chunks
                                   of that document that no longer exist are deleted.
    """
    if not chunks:
        return {"new": 0, "already_stored": 0, "removed": 0}
    collection = get_collection()
    source = chunks[0]["source"]
    stored = set(collection.get(where={"source": source}, include=[])["ids"])
    wanted = {c["id"] for c in chunks}
    stale = stored - wanted
    if stale:
        collection.delete(ids=list(stale))
    todo = [c for c in chunks if c["id"] not in stored]
    for i in range(0, len(todo), BATCH):
        batch = todo[i:i + BATCH]
        vectors = embed_texts([document_text(c) for c in batch])
        collection.add(
            ids=[c["id"] for c in batch],
            embeddings=vectors,
            documents=[c["text"] for c in batch],
            metadatas=[{k: v for k, v in c.items() if k not in ("id", "text")} for c in batch],
        )
        log(f"  {source}: embedded and saved {min(i + BATCH, len(todo))}/{len(todo)}")
    return {"new": len(todo), "already_stored": len(wanted) - len(todo), "removed": len(stale)}


# ============================================================================
# 5. Searching (used by server.py and evaluate.py)
# ============================================================================
def embed_query(query: str) -> list[float]:
    """Embed a question. Each distinct question is embedded once and cached in index/query_cache.json."""
    key = query.strip()
    cache = json.loads(QUERY_CACHE.read_text()) if QUERY_CACHE.is_file() else {}
    if key not in cache:
        vector = embed_texts([f"task: search result | query: {key}"])[0]
        cache[key] = [round(x, 6) for x in vector]
        QUERY_CACHE.write_text(json.dumps(cache))
    return cache[key]


def retrieve(query: str, k: int = 5, parties: list[str] | None = None) -> list[dict]:
    """The k chunks closest to the query, optionally only from the given parties."""
    where = None
    if parties:
        names = [p.upper() for p in parties]
        where = {"party": names[0]} if len(names) == 1 else {"party": {"$in": names}}
    found = get_collection().query(
        query_embeddings=[embed_query(query)], n_results=k, where=where,
        include=["documents", "metadatas", "distances"],
    )
    return [
        {"id": i, "text": d, "distance": dist, **m}
        for i, d, m, dist in zip(found["ids"][0], found["documents"][0], found["metadatas"][0], found["distances"][0])
    ]


# ============================================================================
# Command line
# ============================================================================
def main() -> int:
    parser = argparse.ArgumentParser(description="Build the index.")
    parser.add_argument("--dry-run", action="store_true", help="chunk only; embed nothing, use no quota")
    parser.add_argument("--only", action="append", choices=list(SOURCES), help="index just this document")
    args = parser.parse_args()

    total_new = 0
    for source in args.only or list(SOURCES):
        path = ensure_file(source)
        if path is None:
            log(f"SKIPPED {source}: no PDF available.\n")
            continue
        chunks, dropped = chunk_file(path)
        words = sum(c["n_words"] for c in chunks)
        log(f"{source}: {len(chunks)} chunks (about {words} words counting the overlaps); "
            f"pages dropped: {dict(dropped) or 'none'}")
        if args.dry_run:
            continue
        try:
            result = embed_and_store(chunks)
        except DailyQuotaError as error:
            log(f"\nDaily embedding limit reached. Everything embedded so far is saved.\n"
                f"Run the same command after 09:00 Spanish time to continue.\n{error}")
            return 1
        total_new += result["new"]
        log(f"  -> {result['new']} new, {result['already_stored']} already stored, {result['removed']} removed\n")
    if not args.dry_run:
        log(f"Done. {total_new} chunks embedded this run; index holds {get_collection().count()} chunks.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())