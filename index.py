"""
Assignment 3, index stage (`uv run python main.py index`).

Corpus: OSHA's construction safety standards, 29 CFR Part 1926, taken from the
official eCFR API (US government work, public domain). One document per subpart:

    E  Personal Protective and Life Saving Equipment
    K  Electrical
    L  Scaffolds
    M  Fall Protection
    P  Excavations
    Q  Concrete and Masonry Construction
    X  Stairways and Ladders

The stage downloads the XML into corpus/ (git-ignored), cuts it into chunks
that follow the regulation's own structure (one chunk per section, long
sections split on paragraph boundaries), embeds the chunks with Gemini and
stores them in index/ with their source and location.

Vectors are saved after every batch and only chunks without a saved vector are
embedded, so a crash or the daily quota never loses work and re-running is cheap.

server.py's add_document tool imports chunk_file() and embed_and_store() from
here, so there is exactly one pipeline.
"""

from __future__ import annotations

import csv
import hashlib
import json
import re
import sys
import time
import warnings
from datetime import date, timedelta
from pathlib import Path

import rag

# eCFR files are XML, but html.parser avoids needing lxml; the warning is just noise.
warnings.filterwarnings("ignore", message=".*looks like you're using an HTML parser.*")

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
QUESTIONS = ROOT / "eval" / "questions.csv"

SUBPARTS = {
    "E": "Personal Protective and Life Saving Equipment",
    "K": "Electrical",
    "L": "Scaffolds",
    "M": "Fall Protection",
    "P": "Excavations",
    "Q": "Concrete and Masonry Construction",
    "X": "Stairways and Ladders",
}
ECFR_TITLES = "https://www.ecfr.gov/api/versioner/v1/titles.json"
ECFR_FULL = "https://www.ecfr.gov/api/versioner/v1/full/{date}/title-29.xml"

MIN_CORPUS_WORDS = 50_000
TARGET_WORDS = 170      # start a new chunk once this many words are collected
MAX_WORDS = 250         # never let a chunk grow past this (unless one line is longer)
MIN_TAIL_WORDS = 60     # a last piece shorter than this is merged into the previous one


# --------------------------------------------------------------- small helpers

def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-") or "document"


def clean(text: str) -> str:
    """Collapse whitespace, including the non-breaking spaces eCFR uses."""
    text = text.replace(" ", " ").replace(" ", " ").replace("​", "")
    return re.sub(r"\s+", " ", text).strip()


def count_words(text: str) -> int:
    return len(text.split())


def sha1(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


# ------------------------------------------------------------------- download

def _latest_ecfr_dates(client) -> list[str]:
    """Dates to try for the eCFR snapshot, newest first."""
    dates: list[str] = []
    try:
        response = client.get(ECFR_TITLES)
        response.raise_for_status()
        for title in response.json().get("titles", []):
            if title.get("number") == 29:
                for field in ("latest_issue_date", "up_to_date_as_of", "latest_amended_on"):
                    if title.get(field):
                        dates.append(title[field])
    except Exception as error:  # noqa: BLE001
        rag.log(f"could not read the eCFR title list ({error}), falling back to recent dates")
    today = date.today()
    dates.extend((today - timedelta(days=n)).isoformat() for n in (2, 5, 10, 30))
    seen: set[str] = set()
    return [d for d in dates if not (d in seen or seen.add(d))]


def fetch_subpart(letter: str, folder: Path = CORPUS_DIR, force: bool = False) -> dict:
    """Download one subpart of 29 CFR 1926 as XML. Returns its manifest entry."""
    import httpx

    letter = letter.upper()
    folder.mkdir(parents=True, exist_ok=True)
    target = folder / f"1926-subpart-{letter}.xml"
    manifest_entry = {"file": target.name, "subpart": letter}
    headers = {"User-Agent": "daiist-assignment3 (student coursework)"}
    with httpx.Client(timeout=180, follow_redirects=True, headers=headers) as client:
        if force or not target.is_file():
            last_error = "no attempt made"
            for snapshot in _latest_ecfr_dates(client):
                url = ECFR_FULL.format(date=snapshot)
                try:
                    response = client.get(url, params={"part": "1926", "subpart": letter})
                    if response.status_code == 200 and len(response.content) > 500:
                        target.write_bytes(response.content)
                        manifest_entry.update(url=str(response.url), snapshot=snapshot)
                        break
                    last_error = f"HTTP {response.status_code} for {snapshot}"
                except httpx.HTTPError as error:
                    last_error = f"{type(error).__name__}: {error}"
            else:
                raise RuntimeError(
                    f"Could not download Subpart {letter} from the eCFR ({last_error}). "
                    f"Check your connection, or save the XML yourself as {target}."
                )
    manifest_entry["sha256"] = hashlib.sha256(target.read_bytes()).hexdigest()
    return manifest_entry


def download_corpus() -> list[dict]:
    CORPUS_DIR.mkdir(exist_ok=True)
    manifest_path = CORPUS_DIR / "manifest.json"
    previous = {}
    if manifest_path.is_file():
        previous = {e["file"]: e for e in json.loads(manifest_path.read_text(encoding="utf-8"))}
    entries = []
    for letter in SUBPARTS:
        file_name = f"1926-subpart-{letter}.xml"
        if (CORPUS_DIR / file_name).is_file() and file_name in previous:
            entries.append(previous[file_name])
            rag.log(f"Subpart {letter}: already downloaded")
            continue
        rag.log(f"Subpart {letter}: downloading ...")
        entries.append(fetch_subpart(letter))
    manifest_path.write_text(json.dumps(entries, indent=2), encoding="utf-8")
    return entries


# ------------------------------------------------------------------- chunking

def split_long(line: str, maximum: int = MAX_WORDS) -> list[str]:
    """Break a single over-long paragraph on sentence ends, then on words if it must."""
    if count_words(line) <= maximum:
        return [line]
    pieces: list[str] = []
    current: list[str] = []
    for sentence in re.split(r"(?<=[.;:!?])\s+", line):
        words = sentence.split()
        while len(words) > maximum:
            if current:
                pieces.append(" ".join(current))
                current = []
            pieces.append(" ".join(words[:maximum]))
            words = words[maximum:]
        if current and count_words(" ".join(current)) + len(words) > maximum:
            pieces.append(" ".join(current))
            current = []
        current.extend(words)
    if current:
        pieces.append(" ".join(current))
    return pieces


def group_lines(lines: list[str]) -> list[list[str]]:
    """Group paragraphs into chunks of roughly TARGET_WORDS, never splitting inside a paragraph."""
    pieces: list[str] = []
    for line in lines:
        pieces.extend(split_long(line))
    groups: list[list[str]] = []
    current: list[str] = []
    count = 0
    for piece in pieces:
        words = count_words(piece)
        if current and (count >= TARGET_WORDS or count + words > MAX_WORDS):
            groups.append(current)
            current, count = [], 0
        current.append(piece)
        count += words
    if current:
        groups.append(current)
    if len(groups) > 1:
        tail = sum(count_words(p) for p in groups[-1])
        previous = sum(count_words(p) for p in groups[-2])
        if tail < MIN_TAIL_WORDS and tail + previous <= MAX_WORDS + MIN_TAIL_WORDS:
            groups[-2].extend(groups.pop())
    return groups


def build_chunks(source: str, doc_title: str, location: str, heading: str, lines: list[str]) -> list[dict]:
    """Turn the paragraphs of one section (or page) into chunk records with metadata."""
    groups = group_lines([l for l in lines if l.strip()])
    chunks = []
    for number, group in enumerate(groups, start=1):
        label = heading if number == 1 else f"{heading} (continued)"
        text = f"{label}\n" + "\n".join(group)
        chunks.append({
            "id": f"{source}::{slug(location)}::{number:02d}",
            "text": text,
            "hash": sha1(text),
            "source": source,
            "doc_title": doc_title,
            "location": location,
            "heading": heading,
            "part": number,
            "n_parts": len(groups),
            "words": count_words(text),
        })
    return chunks


_INLINE = ["e", "i", "b", "em", "strong", "sub", "sup", "a", "span", "u", "fr"]


def _section_lines(element) -> list[str]:
    """The paragraphs of one eCFR section or appendix, cleaned, without its heading."""
    from bs4 import NavigableString

    for tag in element.find_all(["head", "auth", "cita", "source", "su", "edno", "effdnotp"]):
        tag.decompose()
    for row in element.find_all(["row", "tr"]):
        cells = [clean(c.get_text(" ")) for c in row.find_all(["ent", "td", "th"])]
        row.replace_with(NavigableString(" | ".join(c for c in cells if c) + "\n"))
    for tag in element.find_all(_INLINE):
        tag.unwrap()
    element.smooth()
    lines = [clean(line) for line in element.get_text("\n").split("\n")]
    return [line for line in lines if line]


def chunk_ecfr(path: Path) -> list[dict]:
    """Chunk an eCFR XML export: one section or appendix at a time, tagged with its subpart."""
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(path.read_text(encoding="utf-8", errors="replace"), "html.parser")
    is_type = lambda wanted: (lambda tag: (tag.get("type") or "").upper() in wanted)
    fallback = slug(path.stem)
    chunks: list[dict] = []
    for element in soup.find_all(is_type({"SECTION", "APPENDIX"})):
        head = element.find("head")
        heading = clean(head.get_text(" ")) if head else ""
        if not heading:
            continue

        subpart = element.find_parent(is_type({"SUBPART"}))
        source, doc_title = fallback, path.stem
        if subpart is not None and subpart.get("n"):
            letter = subpart["n"].strip().upper()
            subpart_head = subpart.find("head")
            name = ""
            if subpart_head is not None:
                name = re.split(r"[\u2014\u2013]|\s-\s", clean(subpart_head.get_text(" ")), maxsplit=1)[-1].strip()
            name = name or SUBPARTS.get(letter, "")
            source = f"1926-subpart-{letter}"
            doc_title = f"29 CFR 1926 Subpart {letter}" + (f", {name}" if name else "")

        section = re.match(r"§+\s*(\d+\.\d+[A-Za-z]?)", heading)
        appendix = re.match(r"Appendix\s+([A-Z]+)\s+to\s+Subpart\s+([A-Z]+)", heading, re.IGNORECASE)
        if section:
            location = section.group(1)
        elif appendix:
            location = f"Appendix {appendix.group(1).upper()} to Subpart {appendix.group(2).upper()}"
        else:
            location = heading[:60]

        lines = _section_lines(element)
        if count_words(" ".join(lines)) < 6:     # [Reserved] and similar
            continue
        chunks.extend(build_chunks(source, doc_title, location, heading, lines))
    if not chunks:
        raise ValueError(f"No sections found in {path.name}. Is it an eCFR XML export?")
    return chunks


def _chunk_pages(source: str, doc_title: str, pages: list[tuple[str, str]]) -> list[dict]:
    chunks: list[dict] = []
    for location, text in pages:
        sentences = [s for s in re.split(r"(?<=[.!?])\s+", clean(text)) if s]
        if count_words(" ".join(sentences)) < 6:
            continue
        chunks.extend(build_chunks(source, doc_title, location, f"{doc_title}, {location}", sentences))
    return chunks


def chunk_pdf(path: Path) -> list[dict]:
    from pypdf import PdfReader

    reader = PdfReader(str(path))
    pages = [(f"p. {n}", page.extract_text() or "") for n, page in enumerate(reader.pages, start=1)]
    chunks = _chunk_pages(slug(path.stem), path.stem, pages)
    if not chunks:
        raise ValueError(f"No text could be extracted from {path.name}. Is it a scanned PDF?")
    return chunks


def chunk_text_file(path: Path) -> list[dict]:
    raw = path.read_text(encoding="utf-8", errors="replace")
    if path.suffix.lower() in {".html", ".htm"}:
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(raw, "html.parser")
        for tag in soup(["script", "style", "nav", "footer"]):
            tag.decompose()
        raw = soup.get_text("\n")
    sections = re.split(r"\n(?=#{1,3} )", raw) if path.suffix.lower() == ".md" else [raw]
    pages = []
    for number, section in enumerate(sections, start=1):
        first = section.strip().split("\n", 1)[0].lstrip("# ").strip()
        pages.append((first[:60] if len(sections) > 1 and first else f"part {number}", section))
    chunks = _chunk_pages(slug(path.stem), path.stem, pages)
    if not chunks:
        raise ValueError(f"{path.name} has no usable text.")
    return chunks


def chunk_file(path) -> list[dict]:
    """Extract, clean and chunk one file. The per-file step server.py's add_document reuses."""
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix == ".xml":
        return chunk_ecfr(path)
    if suffix == ".pdf":
        return chunk_pdf(path)
    if suffix in {".txt", ".md", ".html", ".htm"}:
        return chunk_text_file(path)
    raise ValueError(f"Unsupported file type {suffix!r}. Use .xml (eCFR), .pdf, .txt, .md or .html.")


# ------------------------------------------------------------------ embedding

def embed_and_store(chunks: list[dict], replace: bool = True, quiet: bool = False) -> dict:
    """Embed the chunks that have no saved vector yet and store them in Chroma.

    A chunk counts as already embedded when its id exists with the same content hash.
    Each batch is written as soon as it comes back, so nothing is lost on a crash.
    With replace=True, chunks of the same source that no longer exist are removed,
    so re-adding an edited document replaces the old version.
    """
    collection = rag.get_collection()
    ids = [c["id"] for c in chunks]

    stored: dict[str, str | None] = {}
    for start in range(0, len(ids), 200):
        got = collection.get(ids=ids[start:start + 200], include=["metadatas"])
        for chunk_id, meta in zip(got["ids"], got["metadatas"]):
            stored[chunk_id] = (meta or {}).get("hash")
    todo = [c for c in chunks if stored.get(c["id"]) != c["hash"]]

    for start in range(0, len(todo), rag.EMBED_BATCH):
        batch = todo[start:start + rag.EMBED_BATCH]
        vectors = rag.embed_texts([c["text"] for c in batch])
        collection.upsert(
            ids=[c["id"] for c in batch],
            embeddings=vectors,
            documents=[c["text"] for c in batch],
            metadatas=[{k: v for k, v in c.items() if k != "text" and k != "id"} for c in batch],
        )
        if not quiet:
            rag.log(f"  embedded and saved {min(start + len(batch), len(todo))}/{len(todo)}")

    removed = 0
    if replace:
        keep = set(ids)
        for source in {c["source"] for c in chunks}:
            old = collection.get(where={"source": source}, include=[])["ids"]
            stale = [i for i in old if i not in keep]
            if stale:
                collection.delete(ids=stale)
                removed += len(stale)

    return {"chunks": len(chunks), "already_indexed": len(chunks) - len(todo),
            "embedded": len(todo), "removed": removed}


def embed_test_questions() -> int:
    """Cache the embeddings of eval/questions.csv so searching them costs no quota later."""
    if not QUESTIONS.is_file():
        return 0
    with QUESTIONS.open(newline="", encoding="utf-8") as handle:
        questions = [r["question"].strip() for r in csv.DictReader(handle) if (r.get("question") or "").strip()]
    return rag.save_baseline_queries(questions) if questions else 0


# ----------------------------------------------------------------------- main

def main() -> int:
    started = time.time()
    entries = download_corpus()

    all_chunks: list[dict] = []
    per_document = []
    for entry in entries:
        chunks = chunk_file(CORPUS_DIR / entry["file"])
        words = sum(c["words"] for c in chunks)
        per_document.append((entry["file"], chunks[0]["doc_title"], len({c["location"] for c in chunks}), len(chunks), words))
        entry["words"] = words
        entry["chunks"] = len(chunks)
        all_chunks.extend(chunks)
    (CORPUS_DIR / "manifest.json").write_text(json.dumps(entries, indent=2), encoding="utf-8")

    total_words = sum(row[4] for row in per_document)
    print("Corpus")
    for file_name, title, sections, chunk_count, words in per_document:
        print(f"  {title}: {sections} sections, {chunk_count} chunks, {words:,} words")
    print(f"  total: {len(per_document)} documents, {len(all_chunks)} chunks, {total_words:,} words")
    if total_words < MIN_CORPUS_WORDS:
        print(f"WARNING: the assignment needs at least {MIN_CORPUS_WORDS:,} words. Add subparts to SUBPARTS in index.py.")

    print(f"Embedding with {rag.EMBED_MODEL} ({rag.EMBED_DIMS} dimensions). Chunks without a saved vector only.")
    stats = embed_and_store(all_chunks)
    print(f"  {stats['embedded']} embedded, {stats['already_indexed']} already saved, {stats['removed']} stale removed")

    new_queries = embed_test_questions()
    print(f"  {new_queries} test questions embedded for the query cache")
    print(f"Index ready in index/ ({time.time() - started:.0f}s)")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except RuntimeError as error:
        print(f"\n{error}", file=sys.stderr)
        raise SystemExit(1)
