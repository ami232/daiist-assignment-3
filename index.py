"""
Assignment 3: build the index (`main.py index`).

Corpus: parts of Title 29 of the US Code of Federal Regulations, downloaded from the
eCFR API as XML for ONE fixed snapshot date, so that no two documents come from
different editions of the rules:

    29 CFR Part 825   Family and Medical Leave Act      (indexed)
    29 CFR Part 785   Hours worked                      (indexed)
    29 CFR Part 531   Wage payments                     (indexed)
    29 CFR Part 778   Overtime compensation             (downloaded, NOT indexed: the
                                                         add_document tool adds it later)

Two chunking designs are built, each in its own ChromaDB collection, so retrieval can be
compared on the same questions:

    fixed     windows of a fixed number of words, 20% overlap, ignoring section boundaries
    section   one chunk per section (§); a long section is split into windows

Every chunk carries `source` ("29 CFR Part 825"), `location` ("§ 825.200") and `sections`,
the list of every section it touches (a fixed window can span several).

Vectors are saved as soon as each batch is embedded, and only chunks without a saved
vector are embedded, so a crash or the daily quota limit loses nothing.

Run:  uv run python main.py index          (or: uv run python index.py [--dry-run])
"""

import argparse
import hashlib
import json
import re
import sys
import xml.etree.ElementTree as ET
from pathlib import Path

import chromadb
import httpx

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"  # downloaded text, git-ignored
INDEX_DIR = ROOT / "index"  # ChromaDB and the query cache, committed

# ---- Decisions (change them here, nowhere else) -------------------------------------------

TITLE = 29
SNAPSHOT_DATE = "2026-11-01"  # one date for every document: no mixing of editions
INDEXED_PARTS = [825, 785, 531]
HELD_BACK_PARTS = [778]  # downloaded, but only added through the add_document tool

DESIGNS = {
    "fixed": {"size": 200, "overlap": 40},  # overlap = one fifth, as in the class notebook
    "section": {"max_words": 450, "overlap": 90},
}
ACTIVE_DESIGN = "fixed"  # the design server.py searches: set it after comparing hit rates

EMBEDDING_MODEL = "gemini-embedding-2"
BATCH_SIZE = 100
MAX_EMBEDS_PER_RUN = 800  # refuse a run that would use most of the ~1,000 embeddings a day

SKIP_TAGS = {"CITA"}  # source credits such as "[73 FR 68073, Nov. 17, 2008]": noise, not rules


# ---- 1. Download --------------------------------------------------------------------------


def corpus_path(part: int) -> Path:
    return CORPUS_DIR / f"{TITLE}cfr{part}_{SNAPSHOT_DATE}.xml"


def download_part(part: int) -> Path:
    """Download one part from the eCFR API for the fixed snapshot date, unless already saved."""
    path = corpus_path(part)
    if path.exists():
        return path
    CORPUS_DIR.mkdir(exist_ok=True)
    url = f"https://www.ecfr.gov/api/versioner/v1/full/{SNAPSHOT_DATE}/title-{TITLE}.xml"
    response = httpx.get(url, params={"part": part}, timeout=120, follow_redirects=True)
    response.raise_for_status()
    path.write_bytes(response.content)
    print(f"downloaded {path.name} ({len(response.content) / 1e3:.0f} KB)", file=sys.stderr)
    return path


# ---- 2. Extract and clean -----------------------------------------------------------------


def element_text(element) -> str:
    """All the text under an XML element, without the elements in SKIP_TAGS."""
    parts = [element.text or ""]
    for child in element:
        if child.tag not in SKIP_TAGS:
            parts.append(" " + element_text(child) + " ")
        parts.append(child.tail or "")
    return "".join(parts)


def clean(text: str) -> str:
    return " ".join(text.split())  # collapse line breaks and repeated spaces


def parse_part(path: Path):
    """Return (source, sections) for an eCFR XML file.

    A section is {"id": "§ 825.200", "heading": "Amount of leave.", "text": "..."}.
    Appendices are treated as sections too (their id is e.g. "Appendix A to Part 825").
    """
    root = ET.parse(path).getroot()
    source = f"{TITLE} CFR Part {root.get('N')}"
    sections = []
    for element in root.iter():
        if element.tag not in ("DIV8", "DIV9"):  # DIV8 = section, DIV9 = appendix
            continue
        text = clean(element_text(element))
        head = element.find("HEAD")
        heading = clean(element_text(head)) if head is not None else ""
        section_id = clean(element.get("N") or heading.split(".")[0])
        if re.fullmatch(r"\d+\.\d+", section_id):
            section_id = f"§ {section_id}"  # cite sections the way the CFR does: "§ 825.200"
        if re.search(r"\[(Reserved|Removed)\]", text) and len(text.split()) < 20:
            continue  # an empty placeholder section
        if text:
            sections.append({"id": section_id, "heading": heading, "text": text})
    return source, sections


def snapshot_of(path: Path) -> str:
    match = re.search(r"_(\d{4}-\d{2}-\d{2})\.xml$", path.name)
    return match.group(1) if match else "unknown"


# ---- 3. Chunk -----------------------------------------------------------------------------


def make_chunk(source, section_ids, heading, text, design, snapshot):
    location = section_ids[0] if len(section_ids) == 1 else f"{section_ids[0]} to {section_ids[-1]}"
    key = f"{design}|{source}|{location}|{text}"
    return {
        "id": hashlib.sha1(key.encode()).hexdigest()[:20],
        "text": text,
        "source": source,
        "location": location,
        "sections": ";".join(section_ids),
        "heading": heading,
        "design": design,
        "snapshot": snapshot,
        "words": len(text.split()),
    }


def chunk_fixed(source, sections, snapshot, size, overlap):
    """Windows of `size` words over the whole part, whatever the section boundaries."""
    words, owners, headings = [], [], {}
    for section in sections:
        section_words = section["text"].split()
        words += section_words
        owners += [section["id"]] * len(section_words)
        headings[section["id"]] = section["heading"]
    chunks = []
    for start in range(0, max(len(words) - overlap, 1), size - overlap):
        end = min(start + size, len(words))
        ids = list(dict.fromkeys(owners[start:end]))  # sections touched, in order
        chunks.append(make_chunk(source, ids, headings[ids[0]], " ".join(words[start:end]), "fixed", snapshot))
    return chunks


def chunk_by_section(source, sections, snapshot, max_words, overlap):
    """One chunk per section; a section longer than `max_words` becomes overlapping windows."""
    chunks = []
    for section in sections:
        words = section["text"].split()
        if len(words) <= max_words:
            chunks.append(make_chunk(source, [section["id"]], section["heading"], section["text"], "section", snapshot))
            continue
        for start in range(0, max(len(words) - overlap, 1), max_words - overlap):
            end = min(start + max_words, len(words))
            chunks.append(
                make_chunk(source, [section["id"]], section["heading"], " ".join(words[start:end]), "section", snapshot)
            )
    return chunks


def chunk_file(path, design: str = ACTIVE_DESIGN) -> list[dict]:
    """The whole text pipeline for one file: parse, clean, chunk. No API calls."""
    path = Path(path)
    if path.suffix.lower() != ".xml":
        raise ValueError(f"Only eCFR XML files are supported, got {path.name}.")
    source, sections = parse_part(path)
    snapshot = snapshot_of(path)
    if design == "fixed":
        return chunk_fixed(source, sections, snapshot, **DESIGNS["fixed"])
    if design == "section":
        return chunk_by_section(source, sections, snapshot, **DESIGNS["section"])
    raise ValueError(f"Unknown design {design!r}. Choose from {list(DESIGNS)}.")


# ---- 4. Embed and store -------------------------------------------------------------------

_client = None


def get_client():
    """The Gemini client, created on first use so that --dry-run needs no key."""
    global _client
    if _client is None:
        from google import genai
        from google.genai import types

        from api_key import load_api_key

        # On a rate limit (429) or an overloaded server (5xx) wait a minute and retry.
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


def _embed(texts: list[str]) -> list[list[float]]:
    """One vector per text. One Content per text: a plain list of strings would be merged into one."""
    from google.genai import types

    result = get_client().models.embed_content(
        model=EMBEDDING_MODEL,
        contents=[types.Content(parts=[types.Part(text=t)]) for t in texts],
    )
    return [list(e.values) for e in result.embeddings]


def document_text(chunk: dict) -> str:
    """What gets embedded: the same title/text format as the class notebook."""
    title = f"{chunk['source']}, {chunk['location']} {chunk['heading']}".strip()
    return f"title: {title} | text: {chunk['text']}"


def get_collection(design: str):
    db = chromadb.PersistentClient(path=str(INDEX_DIR))
    return db.get_or_create_collection(
        name=f"cfr_{design}",
        configuration={"hnsw": {"space": "cosine"}},
        embedding_function=None,  # we always pass our own vectors
    )


def metadata_of(chunk: dict) -> dict:
    return {k: chunk[k] for k in ("source", "location", "sections", "heading", "design", "snapshot", "words")}


def plan_file(path, design: str):
    """(all chunks, chunks that still need a vector, ids of stale chunks of this source).

    Stale = stored chunks of the same source that the current text no longer produces.
    """
    chunks = list(({c["id"]: c for c in chunk_file(path, design)}).values())  # drop exact duplicates
    collection = get_collection(design)
    stored = set(collection.get(ids=[c["id"] for c in chunks])["ids"])
    new = [c for c in chunks if c["id"] not in stored]
    old_ids = set(collection.get(where={"source": chunks[0]["source"]})["ids"]) if chunks else set()
    stale = sorted(old_ids - {c["id"] for c in chunks})
    return chunks, new, stale


def embed_and_store(chunks: list[dict], design: str) -> int:
    """Embed the chunks in batches and save each batch at once. Returns how many were stored."""
    collection = get_collection(design)
    stored = 0
    for start in range(0, len(chunks), BATCH_SIZE):
        batch = chunks[start : start + BATCH_SIZE]
        vectors = _embed([document_text(c) for c in batch])
        collection.add(
            ids=[c["id"] for c in batch],
            embeddings=vectors,
            documents=[c["text"] for c in batch],
            metadatas=[metadata_of(c) for c in batch],
        )
        stored += len(batch)
        print(f"  saved {stored}/{len(chunks)} vectors", file=sys.stderr)
    return stored


def index_file(path, design: str = ACTIVE_DESIGN) -> dict:
    """Add one file to the index. If it is already indexed, nothing is embedded twice:

    chunks whose id is already stored are kept (no new embedding, no duplicate), and stored
    chunks of the same source that the file no longer produces are deleted. Re-adding an
    unchanged file therefore changes nothing and costs nothing.
    """
    chunks, new, stale = plan_file(path, design)
    if stale:
        get_collection(design).delete(ids=stale)
    embedded = embed_and_store(new, design) if new else 0
    return {
        "source": chunks[0]["source"] if chunks else Path(path).name,
        "design": design,
        "chunks": len(chunks),
        "embedded": embedded,
        "kept": len(chunks) - embedded,
        "deleted": len(stale),
    }


# ---- 5. Search ----------------------------------------------------------------------------

QUERY_CACHE = INDEX_DIR / "query_cache.json"


def embed_query(question: str) -> list[float]:
    """Embed a question, remembering the vector on disk: every question costs quota."""
    try:
        cache = json.loads(QUERY_CACHE.read_text())
    except (OSError, ValueError):
        cache = {}
    key = hashlib.sha1(question.encode()).hexdigest()
    if key not in cache:
        cache[key] = _embed([f"task: search result | query: {question}"])[0]
        try:
            INDEX_DIR.mkdir(exist_ok=True)
            QUERY_CACHE.write_text(json.dumps(cache))
        except OSError:
            pass  # a read-only index is fine: the vector is simply not remembered
    return cache[key]


def retrieve(question: str, k: int = 5, design: str = ACTIVE_DESIGN, where: dict | None = None) -> list[dict]:
    """The k chunks closest to the question, best first, each with its score (1 = identical)."""
    result = get_collection(design).query(
        query_embeddings=[embed_query(question)], n_results=k, where=where
    )
    hits = []
    for text, meta, distance in zip(result["documents"][0], result["metadatas"][0], result["distances"][0]):
        hits.append({**meta, "text": text, "score": 1 - distance})
    return hits


# ---- 6. Command line ----------------------------------------------------------------------


def main(argv=None) -> None:
    parser = argparse.ArgumentParser(description="Download, chunk, embed and store the corpus.")
    parser.add_argument("--dry-run", action="store_true", help="count chunks and embeddings, spend no quota")
    parser.add_argument("--designs", nargs="+", default=list(DESIGNS), choices=list(DESIGNS))
    parser.add_argument("--max-embeds", type=int, default=MAX_EMBEDS_PER_RUN)
    args = parser.parse_args(argv)

    paths = {part: download_part(part) for part in INDEXED_PARTS + HELD_BACK_PARTS}
    print(f"Snapshot {SNAPSHOT_DATE}. Indexing parts {INDEXED_PARTS}; part(s) {HELD_BACK_PARTS} held back.")

    plans = []  # (design, path, chunks, new, stale)
    for design in args.designs:
        for part in INDEXED_PARTS:
            chunks, new, stale = plan_file(paths[part], design)
            plans.append((design, paths[part], chunks, new, stale))

    print(f"\n{'design':<9} {'document':<18} {'chunks':>7} {'new':>6} {'avg words':>10}")
    for design, path, chunks, new, _ in plans:
        average = sum(c["words"] for c in chunks) / max(len(chunks), 1)
        print(f"{design:<9} {chunks[0]['source']:<18} {len(chunks):>7} {len(new):>6} {average:>10.0f}")
    total_new = sum(len(p[3]) for p in plans)
    print(f"\nEmbeddings needed now: {total_new} (free tier: about 1,000 a day, questions count too)")

    if args.dry_run:
        return
    if total_new > args.max_embeds:
        sys.exit(f"That is more than --max-embeds {args.max_embeds}. Raise it on purpose or index one design at a time.")

    try:
        for design, path, _, _, _ in plans:
            print(f"\n{design}: {path.name}", file=sys.stderr)
            stats = index_file(path, design)
            print(f"{stats['design']:<9} {stats['source']:<18} embedded {stats['embedded']}, kept {stats['kept']}, deleted {stats['deleted']}")
    except Exception as error:  # noqa: BLE001 - quota or network: what is saved is kept
        sys.exit(f"\nStopped: {type(error).__name__}: {str(error)[:300]}\nVectors already saved are kept. Run it again (after 09:00 Spanish time if it is the daily quota).")

    for design in args.designs:
        print(f"{design}: {get_collection(design).count()} chunks stored in {INDEX_DIR.name}/")


if __name__ == "__main__":
    main()