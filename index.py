"""
Assignment 3: build the index (`main.py index`).

Corpus: EU rules for selling cosmetic products (see CORPUS below).
Pipeline: download (only what is missing) -> extract text -> clean running
headers/footers -> chunk with source and location -> embed with Gemini -> store
in index/ (ChromaDB). Every vector is saved as soon as its batch comes back, and
only chunks without a saved vector are embedded, so a crash or the daily limit
loses nothing and re-running is free.

Two chunking designs are built so retrieval can compare them by the numbers:
  "fixed"      windows of ~150 words with overlap, over the whole document
  "structure"  one chunk per Article / Annex / numbered section (long sections
               are split, tiny ones merged); page-based when a document has no
               reliable headings

Every chunk carries: source (document), location ("Article 4, p. 12"),
pages, and sections (all headings it touches), so a hit can be judged by
document + article/page.

Functions other modules import (server.py, evaluate.py):
  chunk_file(path, design)        -> list of chunk dicts, no network
  embed_and_store(chunks, design) -> embeds only missing chunks, returns count
  index_file(path, design)        -> chunk + embed one file (add_document tool)
  embed_query(text)               -> query vector, cached in index/query_cache.json
  search_chunks(query, k, design) -> nearest chunks with citations

Everything logs to stderr: server.py speaks MCP over stdout.

Environment variables:
  DRY_RUN=1            chunk and report only, embed nothing (use this first)
  INDEX_DESIGNS=...    comma list, default "structure,fixed"
  MAX_EMBEDS=900       stop after this many new embeddings in one run
"""

from __future__ import annotations

import hashlib
import json
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
STATS_FILE = INDEX_DIR / "corpus_stats.json"

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIMS = 768  # recommended by Google; smaller index, same quality for this size
BATCH_SIZE = 32
TOKENS_PER_MINUTE = 20_000  # stay under the free-tier tokens-per-minute limit (about 30,000)
MIN_WORDS_REQUIRED = 50_000

DESIGNS = ("structure", "fixed")
DEFAULT_DESIGN = "structure"  # server.py/agent.py use this; change it after the retrieval comparison

FIXED_SIZE, FIXED_OVERLAP = 150, 30
SECTION_MAX, SECTION_WINDOW, SECTION_OVERLAP, SECTION_MIN = 350, 250, 40, 25

# --------------------------------------------------------------------------
# The corpus. Page numbers in locations are PDF page numbers (1-based).
# "skip_between": drop everything from the first line matching the first
# pattern up to (not including) the first line matching the second. For
# Regulation 1223/2009 this removes Annexes II and III (lists of prohibited and
# restricted substances: ~40,000 words of tables that no one asks about in
# natural language, and that would eat the free embedding quota).
# --------------------------------------------------------------------------
CORPUS = {
    "reg_1223_2009.pdf": {
        "source": "Reg 1223/2009",
        "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32009R1223",
        "headings": ("article", "annex", "chapter"),
        "skip_between": (r"^ANNEX II$", r"^ANNEX IV$"),
    },
    "reg_655_2013.pdf": {
        "source": "Reg 655/2013",
        "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32013R0655",
        "headings": ("article", "annex", "numbered_top"),
    },
    "dec_2013_674.pdf": {
        "source": "Decision 2013/674",
        "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32013D0674",
        "headings": ("article", "annex", "numbered"),
    },
    "cpnp_guide.pdf": {
        "source": "CPNP guide",
        "url": "https://ec.europa.eu/docsroom/documents/29563/attachments/1/translations/en/renditions/pdf",
        "headings": (),  # numbered lines here are instructions, not titles: page-based
    },
}

HEADINGS = {
    "article": (re.compile(r"^Article (\d+[a-z]?)$"), lambda m: f"Article {m.group(1)}"),
    "annex": (re.compile(r"^ANNEX(?: ([IVX]+))?$"), lambda m: f"Annex {m.group(1)}" if m.group(1) else "Annex"),
    "chapter": (re.compile(r"^CHAPTER ([IVX]+)$"), lambda m: f"Chapter {m.group(1)}"),
    "numbered": (re.compile(r"^(\d+(?:\.\d+)+)\.? ([A-Z][a-z].{1,70})$"), lambda m: f"Section {m.group(1)}"),
    "numbered_top": (re.compile(r"^(\d+)\. ([A-Z][a-z][A-Za-z ,/&-]{2,37})$"), lambda m: f"Section {m.group(1)}: {m.group(2)}"),
}
GUARD_KINDS = ("article", "annex", "chapter")  # never treat these as running headers


def log(*parts) -> None:
    print(*parts, file=sys.stderr, flush=True)


class QuotaExhausted(RuntimeError):
    pass


# --------------------------------------------------------------------------
# Download
# --------------------------------------------------------------------------
def is_pdf(path: Path) -> bool:
    try:
        return path.stat().st_size > 1000 and path.read_bytes()[:5] == b"%PDF-"
    except OSError:
        return False


def download(url: str, path: Path, attempts: int = 8) -> bool:
    """EUR-Lex sometimes answers 200/202 with an empty body while it generates the PDF."""
    import httpx

    headers = {"User-Agent": "Mozilla/5.0"}
    with httpx.Client(follow_redirects=True, timeout=90, headers=headers) as client:
        for attempt in range(1, attempts + 1):
            try:
                response = client.get(url)
                if response.content[:5] == b"%PDF-":
                    path.write_bytes(response.content)
                    return True
                log(f"  attempt {attempt}/{attempts}: HTTP {response.status_code}, not a PDF yet; waiting")
            except httpx.HTTPError as error:
                log(f"  attempt {attempt}/{attempts}: {type(error).__name__}")
            time.sleep(6)
    return False


def ensure_corpus() -> None:
    CORPUS_DIR.mkdir(exist_ok=True)
    for name, info in CORPUS.items():
        path = CORPUS_DIR / name
        if is_pdf(path):
            continue
        log(f"Downloading {name} ...")
        if not download(info["url"], path):
            raise SystemExit(
                f"Could not download {name}.\n"
                f"  Open {info['url']} in a browser, save the PDF as corpus/{name} and run again."
            )


# --------------------------------------------------------------------------
# Extract and clean
# --------------------------------------------------------------------------
def extract_pages(path) -> list[str]:
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        from pypdf import PdfReader

        return [(page.extract_text() or "") for page in PdfReader(str(path)).pages]
    if suffix in (".txt", ".md"):
        words = path.read_text(encoding="utf-8", errors="replace").split()
        return [" ".join(words[i : i + 400]) for i in range(0, len(words), 400)] or [""]
    raise ValueError(f"Unsupported file type {path.suffix!r}: use a PDF, .txt or .md file.")


def normalise(line: str) -> str:
    return re.sub(r"\s+", " ", line.replace("\xa0", " ")).strip()


def shape(line: str) -> str:
    return re.sub(r"\d+", "#", line)


def match_heading(line: str, kinds) -> str | None:
    for kind in kinds:
        pattern, label = HEADINGS[kind]
        match = pattern.match(line)
        if match:
            return label(match)
    return None


def clean_pages(pages: list[str]) -> list[list[str]]:
    """Lines per page with running headers/footers removed.

    A header/footer is a short line among the first or last three of a page whose
    shape (digits blanked) repeats on at least 30% of pages (min 2).
    """
    split = [[n for n in (normalise(line) for line in page.splitlines()) if n] for page in pages]
    counts: Counter = Counter()
    for lines in split:
        edge = lines[:3] + lines[-3:]
        counts.update({shape(l) for l in edge if len(l) < 140 and not match_heading(l, GUARD_KINDS)})
    threshold = max(2, int(0.3 * len(split)))
    boiler = {s for s, c in counts.items() if c >= threshold}
    cleaned = []
    for lines in split:
        keep = []
        for i, line in enumerate(lines):
            at_edge = i < 3 or i >= len(lines) - 3
            if at_edge and len(line) < 140 and shape(line) in boiler and not match_heading(line, GUARD_KINDS):
                continue
            keep.append(line)
        cleaned.append(keep)
    return cleaned


def apply_skip(name: str, page_lines: list[list[str]], spec) -> list[list[str]]:
    if not spec:
        return page_lines
    start, end = re.compile(spec[0]), re.compile(spec[1])
    skipping = started = False
    out = []
    for lines in page_lines:
        keep = []
        for line in lines:
            if not skipping and start.match(line):
                skipping = started = True
            elif skipping and end.match(line):
                skipping = False
            if not skipping:
                keep.append(line)
        out.append(keep)
    if not started:
        raise SystemExit(f"{name}: could not find the start marker {spec[0]!r}; refusing to index the annexes by mistake.")
    if skipping:
        raise SystemExit(f"{name}: found {spec[0]!r} but never {spec[1]!r}; refusing to drop the rest of the document.")
    return out


def merge_hyphens(lines: list[str]) -> list[str]:
    out: list[str] = []
    for line in lines:
        if out and out[-1].endswith("-") and line[:1].islower():
            out[-1] = out[-1][:-1] + line
        else:
            out.append(line)
    return out


SPLIT_HEADS = {"Article": re.compile(r"^\d+[a-z]?$"), "ANNEX": re.compile(r"^[IVX]+$"), "CHAPTER": re.compile(r"^[IVX]+$")}


def join_split_headings(lines: list[str]) -> list[str]:
    """pypdf sometimes puts the word and the number of a heading on two lines ("Article" / "4")."""
    out: list[str] = []
    i = 0
    while i < len(lines):
        nxt = lines[i + 1] if i + 1 < len(lines) else ""
        if lines[i] in SPLIT_HEADS and SPLIT_HEADS[lines[i]].match(nxt):
            out.append(f"{lines[i]} {nxt}")
            i += 2
        else:
            out.append(lines[i])
            i += 1
    return out


ROMAN = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100}


def roman(text: str) -> int:
    total = 0
    for i, ch in enumerate(text):
        value = ROMAN[ch]
        total += -value if i + 1 < len(text) and ROMAN[text[i + 1]] > value else value
    return total


def accept_heading(label: str, last: dict) -> bool:
    """Articles, annexes and chapters come in order. A line that merely looks like a heading
    (e.g. a cross-reference wrapped onto its own line: "Article 251") breaks the order, so reject it."""
    kind, _, rest = label.partition(" ")
    if kind == "Article":
        n = int(re.match(r"\d+", rest).group())
    elif kind in ("Annex", "Chapter"):
        n = roman(rest) if rest else 1
    else:
        return True  # numbered sections: no order check
    ok = last[kind] < n <= last[kind] + 3 or (kind == "Article" and n == last[kind] and rest[-1].isalpha())
    if ok:
        last[kind] = max(last[kind], n)
    return ok


def tag_words(page_lines: list[list[str]], kinds) -> list[tuple[str, int, str]]:
    """(word, pdf page, current section label) for every word, in reading order."""
    words = []
    section = "Preamble"
    last = {"Article": 0, "Annex": 0, "Chapter": 0}
    for page_no, lines in enumerate(page_lines, 1):
        for line in merge_hyphens(join_split_headings(lines)):
            if kinds:
                label = match_heading(line, kinds)
                if label and accept_heading(label, last):
                    section = label
            else:
                section = f"p. {page_no}"
            words.extend((word, page_no, section) for word in line.split())
    return words


def load_words(path: Path):
    path = Path(path)
    info = CORPUS.get(path.name, {})
    pages = clean_pages(extract_pages(path))
    pages = apply_skip(path.name, pages, info.get("skip_between"))
    words = tag_words(pages, info.get("headings", ()))
    if not words:
        raise ValueError(f"{path.name}: no text could be extracted (a scanned PDF?).")
    return words, info.get("source", path.stem)


# --------------------------------------------------------------------------
# Chunk
# --------------------------------------------------------------------------
def window(items: list, size: int, overlap: int) -> list[list]:
    stride = size - overlap
    out, i = [], 0
    while i < len(items):
        out.append(items[i : i + size])
        if i + size >= len(items):
            break
        i += stride
    if len(out) > 1 and len(out[-1]) < size // 3:  # fold a tiny tail into the previous window
        tail = out.pop()
        out[-1] = out[-1] + tail[overlap:]
    return out


def make_chunk(source: str, design: str, words: list, label: str | None = None) -> dict:
    text = " ".join(w for w, _, _ in words)
    first_page, last_page = words[0][1], words[-1][1]
    pages = str(first_page) if first_page == last_page else f"{first_page}-{last_page}"
    sections = list(dict.fromkeys(s for _, _, s in words))
    first = label or sections[0]
    suffix = re.search(r" \(part \d+\)$", first)
    if first.startswith("p. "):
        location = f"p. {pages}{suffix.group(0) if suffix else ''}"
    else:
        location = f"{first}, p. {pages}"
    chunk_id = hashlib.sha1(f"{design}|{source}|{location}|{text}".encode()).hexdigest()[:20]
    return {
        "id": chunk_id,
        "design": design,
        "source": source,
        "location": location,
        "pages": pages,
        "sections": "; ".join(sections),
        "text": text,
        # Gemini Embedding 2: the task goes inside the text, not in task_type
        "embed_text": f"title: {source}, {location} | text: {text}",
    }


def chunk_fixed(words: list, source: str) -> list[dict]:
    return [make_chunk(source, "fixed", w) for w in window(words, FIXED_SIZE, FIXED_OVERLAP)]


def chunk_structure(words: list, source: str) -> list[dict]:
    groups: list[list] = []
    for item in words:
        if groups and groups[-1][0] == item[2]:
            groups[-1][1].append(item)
        else:
            groups.append([item[2], [item]])
    merged: list[list] = []
    carry: list = []
    for label, ws in groups:
        ws = carry + ws
        carry = []
        if len(ws) < SECTION_MIN:  # too small to stand alone: prepend to the next section
            carry = ws
            continue
        merged.append([label, ws])
    if carry:
        if merged:
            merged[-1][1] += carry
        else:
            merged.append([groups[-1][0], carry])
    chunks = []
    for label, ws in merged:
        if len(ws) <= SECTION_MAX:
            chunks.append(make_chunk(source, "structure", ws, label))
        else:
            for k, part in enumerate(window(ws, SECTION_WINDOW, SECTION_OVERLAP), 1):
                chunks.append(make_chunk(source, "structure", part, f"{label} (part {k})"))
    return chunks


def chunks_from_words(words: list, source: str, design: str) -> list[dict]:
    if design == "fixed":
        chunks = chunk_fixed(words, source)
    elif design == "structure":
        chunks = chunk_structure(words, source)
    else:
        raise ValueError(f"Unknown design {design!r}; use one of {DESIGNS}.")
    unique = {c["id"]: c for c in chunks}  # identical chunks would collide in the index
    return list(unique.values())


def chunk_file(path, design: str = DEFAULT_DESIGN) -> list[dict]:
    words, source = load_words(Path(path))
    return chunks_from_words(words, source, design)


# --------------------------------------------------------------------------
# Embed and store
# --------------------------------------------------------------------------
def get_client():
    from google import genai

    from api_key import load_api_key

    return genai.Client(api_key=load_api_key())


def get_collection(design: str = DEFAULT_DESIGN):
    import chromadb
    from chromadb.config import Settings

    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR), settings=Settings(anonymized_telemetry=False))
    return client.get_or_create_collection(f"cosmetics_{design}", metadata={"hnsw:space": "cosine"})


def _embed_batch(client, texts: list[str]) -> list[list[float]]:
    from google.genai import types

    # One Content per text: a bare list of strings would be merged into ONE vector.
    contents = [types.Content(parts=[types.Part.from_text(text=t)]) for t in texts]
    config = types.EmbedContentConfig(output_dimensionality=EMBED_DIMS)
    response = client.models.embed_content(model=EMBED_MODEL, contents=contents, config=config)
    vectors = [list(e.values) for e in response.embeddings]
    if len(vectors) != len(texts):
        raise RuntimeError(f"Sent {len(texts)} texts but got {len(vectors)} vectors. Nothing was stored.")
    if any(len(v) != EMBED_DIMS for v in vectors):
        raise RuntimeError(f"Expected {EMBED_DIMS}-dimensional vectors, got {len(vectors[0])}.")
    return vectors


def embed_texts(client, texts: list[str]) -> list[list[float]]:
    for attempt in range(1, 5):
        try:
            return _embed_batch(client, texts)
        except Exception as error:  # noqa: BLE001 - classify by message, SDK error types vary
            message = str(error)
            quota = "429" in message or "RESOURCE_EXHAUSTED" in message
            transient = any(c in message for c in ("500", "502", "503", "504", "UNAVAILABLE", "DEADLINE", "timed out"))
            daily = "PerDay" in message or "per day" in message.lower()
            if attempt == 4 or not (quota or transient) or (quota and daily):
                if quota:
                    raise QuotaExhausted(message[:1000]) from error
                raise
            hint = re.search(r"retryDelay\W+(\d+)", message)
            wait = (int(hint.group(1)) + 3 if hint else 20 * attempt) if quota else 5 * attempt
            log(f"  retry {attempt}/3 in {wait}s: {message[:90]}")
            time.sleep(wait)
    raise AssertionError("unreachable")


_verified = False


def smoke_test(client) -> None:
    """2 embeddings to prove one vector per text comes back, before spending a whole batch."""
    global _verified
    if _verified:
        return
    vectors = embed_texts(client, ["first test sentence", "second test sentence"])
    assert len(vectors) == 2 and vectors[0] != vectors[1], "embeddings are not one-per-text"
    _verified = True


def missing_ids(chunks: list[dict], design: str) -> list[str]:
    collection = get_collection(design)
    ids = [c["id"] for c in chunks]
    present: set[str] = set()
    for i in range(0, len(ids), 500):
        present |= set(collection.get(ids=ids[i : i + 500], include=[])["ids"])
    return [i for i in ids if i not in present]


def embed_and_store(chunks: list[dict], design: str = DEFAULT_DESIGN, max_new: int | None = None, client=None) -> int:
    """Embed only the chunks that have no saved vector. Returns how many were embedded."""
    missing = set(missing_ids(chunks, design))
    todo = [c for c in chunks if c["id"] in missing]
    log(f"[{design}] {len(chunks)} chunks, {len(chunks) - len(todo)} already stored, {len(todo)} to embed")
    if max_new is not None:
        todo = todo[: max(max_new, 0)]
    if not todo:
        return 0
    client = client or get_client()
    smoke_test(client)
    collection = get_collection(design)
    done = 0
    for i in range(0, len(todo), BATCH_SIZE):
        batch = todo[i : i + BATCH_SIZE]
        started = time.time()
        vectors = embed_texts(client, [c["embed_text"] for c in batch])
        collection.add(
            ids=[c["id"] for c in batch],
            embeddings=vectors,
            documents=[c["text"] for c in batch],
            metadatas=[
                {k: c[k] for k in ("source", "location", "pages", "sections", "design")} for c in batch
            ],
        )
        done += len(batch)
        log(f"  [{design}] stored {done}/{len(todo)}")
        tokens = sum(len(c["embed_text"]) for c in batch) / 3.5  # rough estimate
        time.sleep(max(1.0, tokens / TOKENS_PER_MINUTE * 60 - (time.time() - started)))
    return done


def index_file(path, design: str = DEFAULT_DESIGN) -> tuple[int, int]:
    """Chunk, embed and store one file. Returns (chunks in the file, newly embedded)."""
    chunks = chunk_file(path, design)
    return len(chunks), embed_and_store(chunks, design)


# --------------------------------------------------------------------------
# Query side (used by server.py and evaluate.py)
# --------------------------------------------------------------------------
def _load_cache() -> dict:
    try:
        return json.loads(QUERY_CACHE.read_text())
    except (OSError, ValueError):
        return {}


def embed_query(text: str, client=None) -> list[float]:
    key = hashlib.sha1(f"{EMBED_MODEL}|{EMBED_DIMS}|{text}".encode()).hexdigest()
    cache = _load_cache()
    if key in cache:
        return cache[key]
    client = client or get_client()
    vector = embed_texts(client, [f"task: search result | query: {text}"])[0]
    cache[key] = [round(x, 6) for x in vector]
    INDEX_DIR.mkdir(exist_ok=True)
    QUERY_CACHE.write_text(json.dumps(cache))
    return cache[key]


def search_chunks(query: str, k: int = 5, design: str = DEFAULT_DESIGN, source: str | None = None) -> list[dict]:
    collection = get_collection(design)
    result = collection.query(
        query_embeddings=[embed_query(query)],
        n_results=k,
        where={"source": source} if source else None,
    )
    hits = []
    for i, chunk_id in enumerate(result["ids"][0]):
        meta = result["metadatas"][0][i]
        hits.append(
            {
                "id": chunk_id,
                "text": result["documents"][0][i],
                "score": round(1 - result["distances"][0][i], 4),
                **meta,
            }
        )
    return hits


# --------------------------------------------------------------------------
# main: python main.py index
# --------------------------------------------------------------------------
def main() -> None:
    designs = [d for d in os.environ.get("INDEX_DESIGNS", ",".join(DESIGNS)).replace(" ", "").split(",") if d]
    for d in designs:
        if d not in DESIGNS:
            raise SystemExit(f"INDEX_DESIGNS contains {d!r}; valid designs: {', '.join(DESIGNS)}")
    dry_run = os.environ.get("DRY_RUN") == "1"
    budget = int(os.environ.get("MAX_EMBEDS", "900"))

    ensure_corpus()
    stats: dict = {"words": {}, "chunks": {d: {} for d in designs}}
    chunks: dict[str, list[dict]] = {d: [] for d in designs}
    for name, info in CORPUS.items():
        words, source = load_words(CORPUS_DIR / name)
        stats["words"][source] = len(words)
        stats.setdefault("sections", {})[source] = list(dict.fromkeys(s for _, _, s in words))
        for d in designs:
            cs = chunks_from_words(words, source, d)
            chunks[d] += cs
            stats["chunks"][d][source] = len(cs)
    total_words = sum(stats["words"].values())
    stats["total_words"] = total_words

    log("\nWords kept after cleaning and exclusions:")
    for source, n in stats["words"].items():
        log(f"  {source:<20} {n:>7}")
    log(f"  {'TOTAL':<20} {total_words:>7}   (the brief requires at least {MIN_WORDS_REQUIRED})")
    if total_words < MIN_WORDS_REQUIRED:
        log("  WARNING: below the required word count. Do not exclude fewer pages; add a document.")
    for d in designs:
        log(f"\nDesign {d!r}: {len(chunks[d])} chunks  " + str(stats["chunks"][d]))

    INDEX_DIR.mkdir(exist_ok=True)
    STATS_FILE.write_text(json.dumps(stats, indent=2))

    if dry_run:
        log("\nDRY_RUN=1: nothing was embedded. Sample locations (structure design):")
        if "structure" in chunks:
            for source in stats["words"]:
                locations = [c["location"] for c in chunks["structure"] if c["source"] == source]
                log(f"  {source}: {locations[:6]} ... {locations[-3:]}")
        log("\nHeadings found, in order (check them against the real documents):")
        for source, labels in stats["sections"].items():
            if source != "CPNP guide":
                log(f"  {source}: {', '.join(labels)}")
        return

    try:
        for d in designs:
            budget -= embed_and_store(chunks[d], d, max_new=budget)
    except QuotaExhausted as error:
        raise SystemExit(
            "\nThe Gemini embedding quota is used up for now. Progress is saved.\n"
            "Run `main.py index` again after 09:00 (Spain time), when the daily limit resets.\n"
            f"({error})"
        )
    pending = {d: len(missing_ids(chunks[d], d)) for d in designs}
    if any(pending.values()):
        raise SystemExit(f"\nStopped at the MAX_EMBEDS limit with chunks still missing: {pending}. Run again later; progress is saved.")
    log("\nIndex complete:", {d: get_collection(d).count() for d in designs})


if __name__ == "__main__":
    main()
