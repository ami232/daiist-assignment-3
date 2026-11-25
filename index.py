"""
Assignment 3: build the index (`uv run python main.py index`).

What this script does, in order:
  1. DOWNLOAD  each FDA drug label from openFDA into corpus/ (skipped if already there).
  2. CLEAN     the text of every section we keep.
  3. CHUNK     the text in two ways (= two retrieval designs):
                 - "fixed":    200-word windows with a 40-word overlap
                 - "sections": one chunk per label subsection (2.1, 2.2, 8.6 ...)
  4. EMBED     every chunk with Gemini and STORE it in ChromaDB (index/).
               Chunks that already have a saved vector are skipped, so re-running
               costs nothing, and a crash or the daily limit loses nothing.

server.py imports chunk_file() and embed_and_store() from here for add_document.
"""

import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path

os.environ["ANONYMIZED_TELEMETRY"] = "False"   # stop ChromaDB from sending usage stats

import chromadb
import httpx
from google import genai
from google.genai import types

from api_key import load_api_key
from config import (CORPUS_DIR, DRUGS, EMBED_MODEL, EXTRA_DIR, EXTRA_DRUGS, FIXED_OVERLAP,
                    FIXED_WORDS, INDEX_DIR, SECTION_MAX_WORDS, SECTIONS)

OPENFDA_URL = "https://api.fda.gov/drug/label.json"


def log(message: str) -> None:
    """Print progress to stderr (stdout must stay clean when server.py imports us)."""
    print(message, file=sys.stderr, flush=True)


# =============================================================================
# 1. DOWNLOAD
# =============================================================================

def download_label(name: str, search: str, folder: Path) -> Path:
    """Download one drug label from openFDA and save it as folder/NAME.json."""
    path = folder / f"{name}.json"
    if path.exists():                      # already downloaded -> do nothing
        return path

    folder.mkdir(parents=True, exist_ok=True)
    log(f"Downloading {name} label from openFDA ...")
    # Ask openFDA for the most recent label that matches the search.
    params = {"search": search, "sort": "effective_time:desc", "limit": 1}
    response = httpx.get(OPENFDA_URL, params=params, timeout=60)
    response.raise_for_status()            # stop with an error if the download failed
    label = response.json()["results"][0]  # the label itself is the first (only) result

    path.write_text(json.dumps(label, indent=1), encoding="utf-8")
    return path


# =============================================================================
# 2. CLEAN
# =============================================================================

def clean_text(text: str) -> str:
    """Tidy one section's text."""
    # openFDA writes cross-references with spaces inside the brackets: "( 2.1 )".
    # Make them "(2.1)" so they never look like a subsection heading to our splitter.
    text = re.sub(r"\(\s*(\d+(?:\.\d+)*)\s*\)", r"(\1)", text)
    # Replace odd characters that come from the label's tables and bullets.
    text = text.replace(" ", " ").replace("•", "-")
    # Squash every run of spaces / newlines / tabs into a single space.
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def read_label(path: Path) -> tuple[str, str, list[tuple[str, str]]]:
    """Open a saved label and return (source name, version, [(section field, clean text)])."""
    label = json.loads(Path(path).read_text(encoding="utf-8"))
    source = Path(path).stem.upper()                    # file ELIQUIS.json -> "ELIQUIS"
    version = f"{label.get('set_id', '?')} v{label.get('version', '?')} ({label.get('effective_time', '?')})"

    sections = []
    for field in SECTIONS:
        if field not in label:                          # not every label has every section
            continue
        # openFDA stores each section as a LIST of strings -> join them into one text.
        text = clean_text(" ".join(label[field]))
        if text:
            sections.append((field, text))
    return source, version, sections


# =============================================================================
# 3. CHUNK
# =============================================================================

def split_into_subsections(field: str, text: str) -> list[tuple[str, str]]:
    """Cut one section into its numbered subsections.

    "2 DOSAGE AND ADMINISTRATION 2.1 Recommended Dose ... 2.2 Dosage Adjustments ..."
    becomes [("2", "2 DOSAGE AND ADMINISTRATION"), ("2.1", "2.1 Recommended Dose ..."), ("2.2", ...)].
    """
    if field == "boxed_warning":                        # the boxed warning has no number
        return [("Boxed Warning", text)]

    # The section number is at the very start, e.g. "2 DOSAGE AND ADMINISTRATION".
    start = re.match(r"(\d{1,2})\s+[A-Z]", text)
    if not start:                                       # older labels: no numbers at all
        return [(field.replace("_", " ").title(), text)]
    number = start.group(1)

    # Split right BEFORE every "2.x Capitalised-word" (a subsection heading of THIS section).
    # (?=...) means "look ahead without consuming", so the heading stays in its piece.
    pieces = re.split(rf"\s(?={number}\.\d{{1,2}}\s+[A-Z])", text)

    subsections = []
    for piece in pieces:
        heading = re.match(rf"{number}\.\d{{1,2}}", piece)     # e.g. "2.1"
        location = heading.group(0) if heading else number    # the intro text before 2.1 gets "2"
        subsections.append((location, piece))
    return subsections


def make_chunk(source: str, version: str, design: str, n: int, field: str,
               locations: list[str], words: list[str]) -> dict:
    """Package one chunk: its text (with a small header) and its metadata."""
    location = ";".join(locations)                      # e.g. "2.1" or "2.1;2.2"
    section_name = field.replace("_", " ").title()      # "dosage_and_administration" -> "Dosage And Administration"
    body = " ".join(words)
    # What the agent reads: a citation tag first, then the text.
    text = f"[{source} §{location}] ({section_name})\n{body}"
    # What we embed: Gemini's document format "title: ... | text: ...", as in class.
    # The title (drug + section) is embedded with every chunk, which helps retrieval.
    embed_text = f"title: {source} - {section_name} | text: {body}"
    # A stable id: same source + position + text -> same id -> we never embed it twice.
    digest = hashlib.md5(f"{source}|{n}|{embed_text}".encode()).hexdigest()[:12]
    return {
        "id": f"{source}-{design}-{n}-{digest}",
        "text": text,
        "embed_text": embed_text,
        "metadata": {"source": source, "location": location, "section": section_name,
                     "version": version, "design": design, "words": len(words)},
    }


def chunk_file(path: Path, design: str) -> list[dict]:
    """Read one label file and cut it into chunks for the given design ("fixed" or "sections")."""
    source, version, sections = read_label(path)
    chunks = []

    if design == "sections":
        # One chunk per subsection. Long subsections are cut into EQUAL parts of at most
        # SECTION_MAX_WORDS words (equal, so we never get a tiny 2-word leftover chunk).
        for field, text in sections:
            for location, piece in split_into_subsections(field, text):
                words = piece.split()
                if len(words) < 8:                      # a lone heading, no content -> skip
                    continue
                n_parts = -(-len(words) // SECTION_MAX_WORDS)   # rounding UP: 620 words -> 3 parts
                size = -(-len(words) // n_parts)                # 620 words / 3 parts -> 207 words each
                for start in range(0, len(words), size):
                    part = words[start:start + size]
                    chunks.append(make_chunk(source, version, design, len(chunks), field, [location], part))

    elif design == "fixed":
        # Ignore the structure: put all words of a section in one list, remembering
        # which subsection each word came from, then slide a window over the list.
        for field, text in sections:
            words, word_locations = [], []
            for location, piece in split_into_subsections(field, text):
                for word in piece.split():
                    words.append(word)
                    word_locations.append(location)
            step = FIXED_WORDS - FIXED_OVERLAP          # 200 - 40 = move 160 words each time
            for start in range(0, len(words), step):
                window = words[start:start + FIXED_WORDS]
                # The subsections this window touches, in order, without repeats.
                locations = list(dict.fromkeys(word_locations[start:start + FIXED_WORDS]))
                chunks.append(make_chunk(source, version, design, len(chunks), field, locations, window))
                if start + FIXED_WORDS >= len(words):   # this window reached the end
                    break
    else:
        raise ValueError(f"Unknown design: {design}")

    return chunks


# =============================================================================
# 4. EMBED AND STORE
# =============================================================================

def get_collection(name: str):
    """Open (or create) one ChromaDB collection inside index/."""
    client = chromadb.PersistentClient(path=str(INDEX_DIR))
    # embedding_function=None: WE give Chroma the vectors (from Gemini); Chroma never embeds.
    # "cosine": rank by cosine similarity, as in class.
    return client.get_or_create_collection(name, configuration={"hnsw": {"space": "cosine"}},
                                           embedding_function=None)


_client = None


def get_client():
    """One Gemini client for the whole program, created on first use (as in class).

    On a rate limit (429) or an overloaded server (5xx) it waits one minute and
    retries, up to 5 attempts in total.
    """
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
    """Embed already-prefixed texts in ONE call. Returns one vector per text."""
    global _client
    # One Content per text: a plain list of strings would be merged into a single vector.
    contents = [types.Content(parts=[types.Part(text=t)]) for t in texts]
    for attempt in range(2):
        try:
            response = get_client().models.embed_content(model=EMBED_MODEL, contents=contents)
            return [embedding.values for embedding in response.embeddings]
        except Exception as error:
            # The connection was closed under us: open a new one and try once more.
            if "closed" in str(error) and attempt == 0:
                log("  Gemini connection was closed; reconnecting")
                _client = None
                continue
            # Anything else (e.g. the daily limit) has already been retried 5 times by the client.
            raise SystemExit(
                f"Embedding failed: {error}\n"
                "If this is the DAILY limit, run the command again after 09:00 (Spain): "
                "every vector saved so far is kept."
            )


def embed_queries(questions: list[str]) -> list[list[float]]:
    """Questions get Gemini's query format, so they match the passages that answer them."""
    return embed_texts([f"task: search result | query: {q}" for q in questions])


def embed_and_store(chunks: list[dict], collection, batch_size: int = 10) -> int:
    """Embed the chunks that have NO saved vector yet, saving every batch immediately."""
    # Which chunk ids are already in the index? Those are skipped (no API call).
    existing = set(collection.get(ids=[c["id"] for c in chunks])["ids"]) if chunks else set()
    todo = [c for c in chunks if c["id"] not in existing]
    if not todo:
        return 0

    for i in range(0, len(todo), batch_size):
        batch = todo[i:i + batch_size]
        vectors = embed_texts([c["embed_text"] for c in batch])   # "title: ... | text: ..."
        # Save this batch right away: if the next batch fails, this one is safe on disk.
        collection.add(
            ids=[c["id"] for c in batch],
            embeddings=vectors,
            documents=[c["text"] for c in batch],
            metadatas=[c["metadata"] for c in batch],
        )
        log(f"  embedded {min(i + batch_size, len(todo))}/{len(todo)}")
        time.sleep(8)          # stay under the free tier's per-minute limits
    return len(todo)


def remove_stale(collection, source: str, keep_ids: set[str]) -> None:
    """Delete old chunks of `source` that are no longer produced (e.g. after changing chunk size)."""
    old = collection.get(where={"source": source})["ids"]
    stale = [i for i in old if i not in keep_ids]
    if stale:
        collection.delete(ids=stale)
        log(f"  removed {len(stale)} outdated {source} chunks")


# =============================================================================
# MAIN: run all the steps for the whole corpus
# =============================================================================

def main() -> None:
    # 1. Download the corpus, plus the extra label kept aside for the add-document demo.
    paths = [download_label(name, search, CORPUS_DIR) for name, search in DRUGS.items()]
    for name, search in EXTRA_DRUGS.items():
        download_label(name, search, EXTRA_DIR)

    # 2. Count the words we keep, per document (goes into the REPORT's corpus table).
    log("\nCorpus (words kept after selecting sections):")
    total = 0
    for path in paths:
        source, version, sections = read_label(path)
        words = sum(len(text.split()) for _, text in sections)
        total += words
        log(f"  {source:10} {words:>7,} words   {version}")
    log(f"  {'TOTAL':10} {total:>7,} words")
    if total < 50_000:
        # Stop BEFORE spending embeddings on a corpus that is too small.
        raise SystemExit("Below the 50,000 words required: add a section at the END of config.SECTIONS "
                         "(e.g. 'clinical_studies') or another drug to config.DRUGS, then run again.")

    # 3 + 4. Chunk every document in both designs, then embed what's missing.
    for design in ["sections", "fixed"]:      # "sections" first: it's the one the server will most likely use
        collection = get_collection(design)
        log(f"\nDesign '{design}':")
        for path in paths:
            chunks = chunk_file(path, design)
            remove_stale(collection, chunks[0]["metadata"]["source"], {c["id"] for c in chunks})
            added = embed_and_store(chunks, collection)
            log(f"  {path.stem}: {len(chunks)} chunks ({added} newly embedded)")
        log(f"  collection '{design}' now holds {collection.count()} chunks")

    log("\nDone. Commit the index/ folder.")


if __name__ == "__main__":
    main()
