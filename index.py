"""
Assignment 3: build the index (`main.py index`).

Corpus: FDA drug labels (DailyMed SPL XML) for medicines an elderly heart
patient commonly takes. Each label is downloaded into corpus/ (git-ignored),
parsed section by section, chunked two ways, embedded with Gemini and stored in
ChromaDB under index/ (committed).

Two chunking designs, compared in evaluate.py:
  - "section": one chunk per numbered (sub)section, e.g. warfarin 7.3;
               sections longer than SECTION_MAX_WORDS are split at paragraph,
               row or sentence boundaries.
  - "fixed":   150-word windows with 30-word overlap over the whole label,
               ignoring structure.
Both start with the drug name, so the comparison isolates chunk boundaries.

Vectors are saved per batch under content-hash ids, so a rerun (or a crash, or
the daily quota) only embeds chunks that have no saved vector yet.

server.py and evaluate.py import: chunk_file, embed_and_store, search,
get_collection, DEFAULT_DESIGN.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
HELD_OUT_DIR = CORPUS_DIR / "held_out"
# CORPUS_INDEX_DIR lets the rivaroxaban demo work on a temporary copy of the index.
INDEX_DIR = Path(os.environ.get("CORPUS_INDEX_DIR", ROOT / "index"))
CHROMA_DIR = INDEX_DIR / "chroma"
QUERY_CACHE = INDEX_DIR / "query_vectors.json"

DAILYMED_XML = "https://dailymed.nlm.nih.gov/dailymed/services/v2/spls/{setid}.xml"
DAILYMED_PAGE = "https://dailymed.nlm.nih.gov/dailymed/drugInfo.cfm?setid={setid}"

# Manufacturer labels, pinned by DailyMed set id.
LABELS = {
    "warfarin": "19a69a72-ac5d-45d5-a94d-a5aaecbe4730",      # Jantoven, Upsher-Smith
    "apixaban": "e9481622-7cc6-418a-acb6-c5450daae9b0",      # Eliquis, Bristol-Myers Squibb
    "amiodarone": "4c4ec9b0-13a5-49a8-b57b-b3f64e4316a7",    # Pacerone, Upsher-Smith
    "metoprolol": "b5f4fed2-369c-4808-a682-8a5b8cfdbb4f",    # Lopressor, Validus
    "atorvastatin": "a60cc18b-0631-4cf0-b021-9f52224ece65",  # Lipitor, Viatris
    "digoxin": "d91e3646-4c63-4512-ab22-db39c085c4dc",       # Lanoxin, Advanz
}
# Downloaded but NOT indexed: added later through the add_document tool.
HELD_OUT = {
    "rivaroxaban": "10db92f9-2300-4a80-836b-673e1ae91610",   # Xarelto, Janssen
}

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768
EMBED_BATCH = 50

DESIGNS = ("section", "fixed")
DEFAULT_DESIGN = "section"  # revisit after the retrieval comparison in evaluate.py
SECTION_MAX_WORDS = 250
FIXED_WORDS, FIXED_OVERLAP = 150, 30

NS = {"v3": "urn:hl7-org:v3"}
# LOINC section codes that carry no clinical content.
SKIP_CODES = {
    "48780-1",  # SPL product data elements (ingredient tables)
    "51945-4",  # package label / principal display panel
    "42229-5",  # SPL unclassified (boilerplate)
    "43683-2",  # recent major changes (dates only)
}
# Unnumbered sections we keep, with a short name for citations.
NAMED_CODES = {
    "34066-1": ("BW", "Boxed Warning"),
    "42231-1": ("MG", "Medication Guide"),
    "42230-3": ("PI", "Patient Information"),
    "59845-8": ("IFU", "Instructions for Use"),
}


def log(*args) -> None:
    """Log to stderr: server.py imports this module and stdout carries MCP."""
    print(*args, file=sys.stderr, flush=True)


# --------------------------------------------------------------------------
# Download
# --------------------------------------------------------------------------

def download_label(name: str, setid: str, folder: Path = CORPUS_DIR) -> Path:
    """Fetch one SPL XML from DailyMed unless it is already on disk."""
    import httpx

    path = folder / f"{name}.xml"
    if path.exists() and path.stat().st_size > 0:
        return path
    folder.mkdir(parents=True, exist_ok=True)
    for attempt in range(3):
        try:
            response = httpx.get(DAILYMED_XML.format(setid=setid), timeout=60, follow_redirects=True)
            response.raise_for_status()
            path.write_bytes(response.content)
            log(f"downloaded {name} ({len(response.content):,} bytes)")
            return path
        except httpx.HTTPError as error:
            log(f"download {name} failed ({error}); retry {attempt + 1}/3")
            time.sleep(2 * (attempt + 1))
    raise RuntimeError(f"Could not download {name} from DailyMed")


def download_corpus() -> list[Path]:
    paths = [download_label(name, setid) for name, setid in LABELS.items()]
    for name, setid in HELD_OUT.items():
        download_label(name, setid, HELD_OUT_DIR)
    return paths


# --------------------------------------------------------------------------
# Extract: SPL XML -> blocks of clean text, each tagged with its section
# --------------------------------------------------------------------------

def _clean(text: str) -> str:
    return " ".join(text.replace(" ", " ").split())


def _text(el: ET.Element) -> str:
    return _clean("".join(el.itertext()))


def _table_lines(table: ET.Element) -> list[str]:
    """Flatten a table into one line per row: 'Header: value; Header: value'."""
    lines = []
    caption = table.find("v3:caption", NS)
    if caption is not None and _text(caption):
        lines.append(f"Table: {_text(caption)}")
    header_rows = table.findall("v3:thead/v3:tr", NS)
    headers = [_text(c) for c in header_rows[-1] if c.tag.endswith(("td", "th"))] if header_rows else []
    if len(header_rows) > 1:  # a spanning title row above the real headers
        lines.extend(_text(r) for r in header_rows[:-1] if _text(r))
    body_rows = table.findall("v3:tbody/v3:tr", NS) or table.findall("v3:tr", NS)
    for row in body_rows:
        cells = [_text(c) for c in row if c.tag.endswith(("td", "th"))]
        if not any(cells):
            continue
        if headers and len(headers) == len(cells):
            parts = [f"{h}: {v}" if h else v for h, v in zip(headers, cells) if v]
            lines.append("; ".join(parts))
        else:
            lines.append(" | ".join(c for c in cells if c))
    footer = table.find("v3:tfoot", NS)
    if footer is not None and _text(footer):
        lines.append(_text(footer))
    return lines


def _content_blocks(text_el: ET.Element) -> list[str]:
    """Direct content of a section's <text>: paragraphs, lists and tables."""
    blocks = []
    for child in text_el:
        tag = child.tag.split("}")[-1]
        if tag == "table":
            rows = _table_lines(child)
            if rows:
                blocks.append("\n".join(rows))
        elif tag == "list":
            items = [_text(i) for i in child.findall("v3:item", NS)]
            blocks.append("\n".join(f"- {i}" for i in items if i))
        elif tag == "renderMultiMedia":
            continue
        else:
            text = _text(child)
            if text:
                blocks.append(text)
    if not blocks and _clean(text_el.text or ""):  # bare text, no child elements
        blocks.append(_clean(text_el.text))
    return [b for b in blocks if b.strip()]


def _section_label(section: ET.Element, parent: tuple[str, str] | None) -> tuple[str, str]:
    """(number, title): ('7.3', 'Drugs that Increase...'), ('BW', 'Boxed Warning')."""
    title_el = section.find("v3:title", NS)
    title = _text(title_el) if title_el is not None else ""
    match = re.match(r"^(\d+(?:\.\d+)*)\s+(.*)$", title)
    if match:
        name = match.group(2)
        return match.group(1), name.title() if name.isupper() else name
    code_el = section.find("v3:code", NS)
    code = code_el.get("code") if code_el is not None else ""
    if code in NAMED_CODES:
        return NAMED_CODES[code]
    if parent:  # unnumbered subsection, e.g. a heading inside the Medication Guide
        return parent[0], f"{parent[1]} > {title}" if title else parent[1]
    return "", title or "Unlabelled section"


def _walk(section: ET.Element, parent: tuple[str, str] | None, out: list[dict]) -> None:
    code_el = section.find("v3:code", NS)
    # Skip codes apply to top-level sections only: subsections such as 2.1 or
    # 7.3 often carry the generic 42229-5 "unclassified" code.
    if parent is None and code_el is not None and code_el.get("code") in SKIP_CODES:
        return
    number, title = _section_label(section, parent)
    text_el = section.find("v3:text", NS)
    if text_el is not None:
        for block in _content_blocks(text_el):
            out.append({"number": number, "title": title, "text": block})
    for child in section.findall("v3:component/v3:section", NS):
        _walk(child, (number, title), out)


def extract_label(path: Path) -> dict:
    """Parse one SPL file into document metadata plus an ordered list of blocks."""
    root = ET.parse(path).getroot()
    setid_el = root.find("v3:setId", NS)
    product = root.find(".//v3:manufacturedProduct/v3:manufacturedProduct/v3:name", NS)
    generic = root.find(".//v3:manufacturedProduct/v3:manufacturedProduct//v3:genericMedicine/v3:name", NS)
    brand = _text(product) if product is not None else path.stem
    generic_name = _text(generic).lower() if generic is not None else path.stem
    blocks: list[dict] = []
    for section in root.findall(".//v3:structuredBody/v3:component/v3:section", NS):
        _walk(section, None, blocks)
    setid = setid_el.get("root") if setid_el is not None else ""
    # Source key = first word of the generic name ("warfarin sodium" -> "warfarin"),
    # so a renamed file is still recognised as the same drug.
    source = generic_name.split()[0] if generic is not None and generic_name else path.stem.lower()
    return {
        "source": source,
        "brand": brand.title() if brand.isupper() else brand,
        "generic": generic_name,
        "setid": setid,
        "version_date": root.find("v3:effectiveTime", NS).get("value", ""),
        "url": DAILYMED_PAGE.format(setid=setid) if setid else "",
        "blocks": blocks,
    }


# --------------------------------------------------------------------------
# Chunk
# --------------------------------------------------------------------------

def _location(number: str, title: str) -> str:
    return f"{number} {title}" if number and number[0].isdigit() else title


def _split_long(text: str, max_words: int) -> list[str]:
    """Split text at line, then sentence, then word boundaries into <= max_words pieces."""
    units: list[str] = []
    for line in text.split("\n"):
        if len(line.split()) <= max_words:
            units.append(line)
            continue
        for sentence in re.split(r"(?<=[.;:])\s+", line):
            words = sentence.split()
            units.extend(" ".join(words[i:i + max_words]) for i in range(0, len(words), max_words))
    pieces, current, count = [], [], 0
    for unit in units:
        n = len(unit.split())
        if current and count + n > max_words:
            pieces.append("\n".join(current))
            current, count = [], 0
        current.append(unit)
        count += n
    if current:
        pieces.append("\n".join(current))
    return pieces


def chunk_section(doc: dict, max_words: int = SECTION_MAX_WORDS) -> list[dict]:
    """Design A: one chunk per (sub)section; long sections split at natural boundaries."""
    groups: list[tuple[str, str, list[str]]] = []
    for block in doc["blocks"]:
        if groups and groups[-1][0] == block["number"] and groups[-1][1] == block["title"]:
            groups[-1][2].append(block["text"])
        else:
            groups.append((block["number"], block["title"], [block["text"]]))
    chunks = []
    for number, title, texts in groups:
        pieces = _split_long("\n".join(texts), max_words)
        for i, piece in enumerate(pieces, 1):
            part = f" (part {i}/{len(pieces)})" if len(pieces) > 1 else ""
            header = f"{doc['brand']} ({doc['generic']}) label, {_location(number, title)}{part}"
            chunks.append(_make_chunk(doc, header, piece, number, title, [number]))
    return chunks


def chunk_fixed(doc: dict, size: int = FIXED_WORDS, overlap: int = FIXED_OVERLAP) -> list[dict]:
    """Design B: fixed word windows over the whole label, ignoring sections."""
    words: list[str] = []
    owners: list[tuple[str, str]] = []  # (number, title) of the section each word came from
    for block in doc["blocks"]:
        block_words = block["text"].split()
        words.extend(block_words)
        owners.extend([(block["number"], block["title"])] * len(block_words))
    chunks = []
    step = size - overlap
    for start in range(0, max(len(words) - overlap, 1), step):
        window = slice(start, start + size)
        spanned = list(dict.fromkeys(owners[window]))
        number, title = spanned[0]
        header = f"{doc['brand']} ({doc['generic']}) label"
        chunks.append(_make_chunk(doc, header, " ".join(words[window]), number, title, [n for n, _ in spanned]))
    return chunks


def _make_chunk(doc: dict, header: str, body: str, number: str, title: str, numbers: list[str]) -> dict:
    text = f"{header}\n{body}"
    return {
        "id": hashlib.sha1(text.encode("utf-8")).hexdigest()[:20],
        "text": text,
        "metadata": {
            "source": doc["source"],
            "brand": doc["brand"],
            "section": number,
            "section_title": title,
            "location": _location(number, title),
            "sections": "," + ",".join(dict.fromkeys(numbers)) + ",",  # ',7,7.3,' for substring matching
            "words": len(body.split()),
            "version_date": doc["version_date"],
            "url": doc["url"],
        },
    }


CHUNKERS = {"section": chunk_section, "fixed": chunk_fixed}


def chunk_file(path: str | Path, design: str = DEFAULT_DESIGN) -> list[dict]:
    """Extract and chunk one SPL XML label. Used by main.py index and by add_document."""
    path = Path(path)
    if path.suffix.lower() != ".xml":
        raise ValueError(f"{path.name}: only DailyMed SPL .xml labels are supported")
    doc = extract_label(path)
    if not doc["blocks"]:
        raise ValueError(f"{path.name}: no label sections found; is this a DailyMed SPL file?")
    chunks = CHUNKERS[design](doc)
    unique = {c["id"]: c for c in chunks}  # identical text -> one chunk
    return list(unique.values())


# --------------------------------------------------------------------------
# Embed and store
# --------------------------------------------------------------------------

_client = None
_chroma = None


def genai_client():
    global _client
    if _client is None:
        from google import genai
        from api_key import load_api_key

        _client = genai.Client(api_key=load_api_key())
    return _client


def get_collection(design: str = DEFAULT_DESIGN):
    global _chroma
    import chromadb

    if _chroma is None:
        CHROMA_DIR.mkdir(parents=True, exist_ok=True)
        _chroma = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return _chroma.get_or_create_collection(f"labels_{design}", metadata={"hnsw:space": "cosine"})


def embed_texts(texts: list[str], task: str) -> list[list[float]]:
    """Embed with Gemini, retrying on rate limits. task: RETRIEVAL_DOCUMENT or RETRIEVAL_QUERY."""
    from google.genai import errors, types

    config = types.EmbedContentConfig(task_type=task, output_dimensionality=EMBED_DIM)
    # gemini-embedding-2 is multimodal: a plain list of strings is read as the
    # parts of ONE input and returns one vector. One Content per text instead.
    contents = [types.Content(parts=[types.Part(text=t)]) for t in texts]
    for attempt in range(6):
        try:
            result = genai_client().models.embed_content(model=EMBED_MODEL, contents=contents, config=config)
            vectors = [e.values for e in result.embeddings]
            if len(vectors) != len(texts):
                raise RuntimeError(f"asked for {len(texts)} embeddings, got {len(vectors)}")
            return vectors
        except errors.APIError as error:
            if error.code != 429 or attempt == 5:
                raise
            if "PerDay" in str(error) or "per day" in str(error).lower():
                raise RuntimeError("Daily embedding quota reached. Rerun after the reset; saved vectors are kept.") from error
            wait = 20 * (attempt + 1)
            log(f"rate limited; waiting {wait}s")
            time.sleep(wait)
    raise RuntimeError("unreachable")


def embed_and_store(chunks: list[dict], design: str = DEFAULT_DESIGN) -> tuple[int, int]:
    """Embed chunks that have no saved vector and store them. Returns (added, already_present)."""
    collection = get_collection(design)
    ids = [c["id"] for c in chunks]
    existing = set(collection.get(ids=ids, include=[])["ids"]) if ids else set()
    todo = [c for c in chunks if c["id"] not in existing]
    for i in range(0, len(todo), EMBED_BATCH):
        batch = todo[i:i + EMBED_BATCH]
        vectors = embed_texts([c["text"] for c in batch], "RETRIEVAL_DOCUMENT")
        collection.add(
            ids=[c["id"] for c in batch],
            embeddings=vectors,
            documents=[c["text"] for c in batch],
            metadatas=[c["metadata"] for c in batch],
        )
        log(f"  [{design}] embedded {min(i + EMBED_BATCH, len(todo))}/{len(todo)}")
    return len(todo), len(existing)


def remove_stale(chunks: list[dict], design: str, sources: set[str]) -> int:
    """Delete chunks of these sources that the current chunker no longer produces."""
    collection = get_collection(design)
    stored = collection.get(include=["metadatas"])
    keep = {c["id"] for c in chunks}
    stale = [cid for cid, meta in zip(stored["ids"], stored["metadatas"])
             if meta["source"] in sources and cid not in keep]
    if stale:
        collection.delete(ids=stale)
    return len(stale)


# --------------------------------------------------------------------------
# Retrieve
# --------------------------------------------------------------------------

def embed_query(query: str) -> list[float]:
    """Query vectors are cached in index/ so evaluation reruns cost no quota."""
    cache = json.loads(QUERY_CACHE.read_text()) if QUERY_CACHE.exists() else {}
    key = hashlib.sha1(f"{EMBED_MODEL}:{EMBED_DIM}:{query}".encode("utf-8")).hexdigest()
    if key not in cache:
        cache[key] = embed_texts([query], "RETRIEVAL_QUERY")[0]
        QUERY_CACHE.write_text(json.dumps(cache))
    return cache[key]


def search(query: str, k: int = 5, design: str = DEFAULT_DESIGN, source: str | None = None) -> list[dict]:
    """Top-k chunks for a query: [{id, text, score, **metadata}], best first."""
    collection = get_collection(design)
    result = collection.query(
        query_embeddings=[embed_query(query)],
        n_results=k,
        where={"source": source} if source else None,
        include=["documents", "metadatas", "distances"],
    )
    return [
        {"id": cid, "text": doc, "score": round(1 - dist, 4), **meta}
        for cid, doc, meta, dist in zip(
            result["ids"][0], result["documents"][0], result["metadatas"][0], result["distances"][0]
        )
    ]


# --------------------------------------------------------------------------
# main.py index
# --------------------------------------------------------------------------

def main() -> None:
    parser = argparse.ArgumentParser(description="Build the index.")
    parser.add_argument("--dry-run", action="store_true", help="chunk and report, embed nothing")
    args = parser.parse_args()

    paths = download_corpus()
    INDEX_DIR.mkdir(exist_ok=True)
    for design in DESIGNS:
        chunks = [c for path in paths for c in chunk_file(path, design)]
        words = [c["metadata"]["words"] for c in chunks]
        log(f"[{design}] {len(chunks)} chunks, {sum(words):,} words, "
            f"mean {sum(words) / len(words):.0f}, max {max(words)} words per chunk")
        dump = INDEX_DIR / f"chunks_{design}.jsonl"
        dump.write_text("".join(json.dumps(c, ensure_ascii=False) + "\n" for c in chunks), encoding="utf-8")
        if args.dry_run:
            continue
        removed = remove_stale(chunks, design, set(LABELS))
        added, kept = embed_and_store(chunks, design)
        log(f"[{design}] {added} embedded now, {kept} already saved, {removed} stale removed")


if __name__ == "__main__":
    main()
