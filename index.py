"""
Assignment 3: build the index (`main.py index`).

    uv run python index.py              # download, extract, chunk, embed, store
    uv run python index.py --dry-run    # everything except embedding (no API quota)

Corpus: four European Commission documents on Erasmus+ student mobility, all
CC BY 4.0. Only the student-relevant pages of the Programme Guide are kept.

Steps per file, importable by server.py:
    extract_blocks(path, source)  -> paragraphs with page and section
    chunk_file(path, source, design) -> chunks with text and metadata
    embed_and_store(chunks, design)  -> embeds only chunks not yet in index/

Two chunking designs are built so evaluate.py can compare them:
    fixed      150-word windows, 25-word overlap, ignores structure
    structure  never crosses a section heading, up to ~250 words, and
               starts with "Document > Section" so the chunk carries context
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768
EMBED_BATCH = 20

DESIGNS = ("fixed", "structure")
DEFAULT_DESIGN = "structure"  # revisit after evaluate.py compares hit rates
FIXED_WORDS, FIXED_OVERLAP = 150, 25
STRUCT_MAX_WORDS, STRUCT_MIN_WORDS = 250, 40

EC = "https://erasmus-plus.ec.europa.eu"
SOURCES = [
    {
        "id": "programme_guide_2026",
        "title": "Erasmus+ Programme Guide 2026",
        "url": f"{EC}/sites/default/files/2025-11/programme-guide-2026_en.pdf",
        "file": "programme_guide_2026_en.pdf",
        "date": "2025-11-12 (version 1)",
        # Part A (general rules, who can take part), Key Action 1 with higher
        # education mobility, and the Part D glossary. The rest of the 456 pages
        # covers youth, sport, schools and funding for organisations.
        "pages": [(4, 36), (39, 72), (443, 456)],
    },
    {
        "id": "eche_guidelines",
        "title": "Erasmus Charter for Higher Education 2021-2027: Guidelines",
        "url": f"{EC}/sites/default/files/charter-annotated-guidelines-feb2020_en.pdf",
        "file": "eche_guidelines_2020_en.pdf",
        "date": "2020-02",
        "pages": [(5, None)],  # pages 1-4 are the cover and contents
    },
    {
        "id": "learning_agreement_guidelines",
        "title": "Guidelines on how to use the Erasmus+ Learning Agreement for Studies (KA131)",
        "url": f"{EC}/resources-and-tools/mobility-and-learning-agreements/learning-agreements/studies-agreement-guidelines-ka131",
        "file": "la_guidelines_ka131_en.html",
        "date": None,  # read from "Last updated" on the page
    },
    {
        "id": "student_charter",
        "title": "Erasmus+ Student Charter",
        "url": f"{EC}/resources-and-tools/erasmusplus-student-charter",
        "file": "student_charter_en.html",
        "date": None,
    },
]


def log(message: str) -> None:
    """Log to stderr: server.py imports this module and its stdout carries MCP."""
    print(message, file=sys.stderr, flush=True)


# --------------------------------------------------------------------------- download

def download(source: dict) -> Path:
    """Fetch a source into corpus/ unless it is already there."""
    import httpx

    path = CORPUS_DIR / "erasmus" / source["file"]
    if path.is_file() and path.stat().st_size > 0:
        return path
    path.parent.mkdir(parents=True, exist_ok=True)
    log(f"Downloading {source['url']}")
    response = httpx.get(source["url"], follow_redirects=True, timeout=120,
                         headers={"User-Agent": "Mozilla/5.0 (course assignment indexer)"})
    response.raise_for_status()
    if path.suffix == ".pdf" and not response.content.startswith(b"%PDF"):
        raise RuntimeError(f"{source['url']} did not return a PDF")
    path.write_bytes(response.content)
    return path


# --------------------------------------------------------------------------- cleaning

BULLETS = "•▪◦●○■"
RUNNING_HEADERS = [
    re.compile(r"^Erasmus Charter for Higher Education 2021-2027 Guidelines$", re.I),
    re.compile(r"^February 2020$"),
]


def fix_spacing(text: str) -> str:
    """Undo common PDF extraction artefacts: 'forward -looking', doubled spaces."""
    text = re.sub(r"(\w) -(\w)", r"\1-\2", text)
    text = text.replace("­", "")  # soft hyphen
    text = re.sub(r"\s+([,.;:])", r"\1", text)
    return re.sub(r"[ \t]+", " ", text).strip()


def has_marker(text: str, n: str) -> bool:
    """Does footnote number n appear as a marker in the text?

    Glued to a word ("funds.63") always counts. Separated by a space ("can be 65:",
    "12 months 66 of") counts only for two- or three-digit numbers, because a
    single digit after a space is usually a real number ("Group 3").
    """
    if re.search(rf"[A-Za-z\.\)\]”’,;:]{n}(?!\d)", text):
        return True
    if len(n) < 2:
        return False
    if re.search(rf"[A-Za-z\)\]”’,;:] {n}(?=[ ,.;:]|$)", text, re.M):
        return True
    # Glued to a number ("14" + footnote 78 = "1478"), but not a year.
    return any(not re.fullmatch(r"(19|20)\d\d", m.group(0)) for m in re.finditer(rf"\b\d{{1,2}}{n}\b", text))


def remove_marker(line: str, n: str) -> str:
    line = re.sub(rf"(?<=[A-Za-z\.\)\]”’,;:]){n}(?=\s|$|[,.;:])", "", line)
    if len(n) >= 2:
        line = re.sub(rf"(?<=[A-Za-z\)\]”’,;:]) {n}(?=[ ,.;:]|$)", "", line)
        # Glued to a number: "Regions 13 and 14" + footnote 78 reads "1478".
        # Only for long footnote numbers and never on something that looks like a year.
        line = re.sub(rf"\b(\d{{1,2}}){n}\b", lambda m: m.group(1) if not re.fullmatch(r"(19|20)\d\d", m.group(0)) else m.group(0), line)
    return line


def split_footnotes(lines: list[str]) -> tuple[list[str], list[str]]:
    """Separate the footnotes at the bottom of a page from the body.

    pypdf returns footnotes as ordinary lines at the end of the page. A footnote
    starts with a number N that also appears as a marker earlier on the page;
    the footnotes that follow it must be numbered N+1, N+2 ... Lines that don't
    start a new footnote continue the previous one.

    Returns (body lines without the markers, footnotes as "Note N: text").
    Footnotes are kept, not deleted: some hold real rules (e.g. "In one-cycle
    study programmes, such as medicine, students can be mobile for up to 24 months").
    """
    for cut in range(len(lines) // 3, len(lines)):
        m = re.match(r"^(\d{1,3})\s+(\S.*)$", lines[cut])
        if not m or not has_marker("\n".join(lines[:cut]), m.group(1)):
            continue
        notes: list[list[str]] = []
        expected = int(m.group(1))
        ok = True
        for line in lines[cut:]:
            m2 = re.match(r"^(\d{1,3})\s+(\S.*)$", line)
            if m2 and int(m2.group(1)) == expected:
                notes.append([m2.group(1), m2.group(2)]); expected += 1
            elif m2 and int(m2.group(1)) > expected:
                ok = False; break  # numbering jumps: this is not a footnote block
            elif line:
                notes[-1][1] += " " + line
        if not ok:
            continue
        body = lines[:cut]
        for n, _ in notes:
            body = [remove_marker(ln, n) for ln in body]
        return body, [f"Note {n}: {text}" for n, text in notes]
    return lines, []


def is_caps_heading(line: str) -> bool:
    """An all-caps line. Table cells in capitals ('786 EUR PER MONTH', 'MOBILITY',
    'DOCTORAL SHORT-TERM MOBILITY)') are excluded: they start with a digit, are a
    single word, or end with a bracket that was opened on another line."""
    letters = [c for c in line if c.isalpha()]
    return (
        len(letters) >= 4
        and len(line) <= 160
        and line[0] not in BULLETS
        and not line[0].isdigit()
        and not (line.endswith(")") and "(" not in line)
        and len(line.split()) >= 2
        and sum(c.isupper() for c in letters) / len(letters) > 0.9
    )


CONNECTORS = {"AND", "OF", "FOR", "THE", "IN", "TO", "ON", "WITH", "BY", "A", "AN", "OR", "–", "-"}


def heading_label(lines: list[str]) -> str:
    """Join consecutive heading lines into a section label.

    A line that ends in a connector word or a dash wraps onto the next line and
    is joined to it; otherwise the next line is a sub-heading: 'Parent > Child'.
    """
    parts: list[str] = []
    for line in lines:
        if parts and parts[-1].split()[-1].upper() in CONNECTORS:
            parts[-1] += " " + line
        else:
            parts.append(line)
    return " > ".join(fix_spacing(p) for p in parts)


def is_numbered_heading(line: str) -> bool:
    # "2. Staff mobility" or "2.4 When participating ...", but not "786 EUR per month".
    m = re.match(r"^(\d{1,2}\.(?:\d{1,2}\.?)*)\s+([A-Z][^.;:]{2,90})$", line)
    return bool(m) and len(line.split()) <= 12


# --------------------------------------------------------------------------- extraction

def page_ranges(source: dict, n_pages: int) -> list[int]:
    ranges = source.get("pages") or [(1, None)]
    pages = []
    for start, end in ranges:
        pages.extend(range(start, (end or n_pages) + 1))
    return [p for p in pages if 1 <= p <= n_pages]


def extract_pdf(path: Path, source: dict) -> list[dict]:
    """Paragraph blocks from the chosen pages, each with its page and section."""
    from pypdf import PdfReader

    reader = PdfReader(path)
    blocks: list[dict] = []
    section = ""
    para: list[str] = []
    para_page = None

    def flush():
        nonlocal para, para_page
        text = fix_spacing(" ".join(para))
        if len(text.split()) >= 3:
            blocks.append({"text": text, "page": para_page, "section": section})
        para, para_page = [], None

    for page_no in page_ranges(source, len(reader.pages)):
        raw = reader.pages[page_no - 1].extract_text() or ""
        lines = [ln.strip() for ln in raw.splitlines()]
        # Running page number and running headers.
        lines = [ln for ln in lines if not re.fullmatch(r"\d{1,3}", ln)
                 and not any(h.match(ln) for h in RUNNING_HEADERS)]
        lines, footnotes = split_footnotes(lines)

        pending_heading: list[str] = []
        # Footnotes go at the end of the page, each as its own paragraph.
        for line in lines + [""] + [x for note in footnotes for x in (note, "")]:
            heading = line and (is_caps_heading(line) or is_numbered_heading(line))
            if heading:
                flush()
                pending_heading.append(line)
                continue
            if pending_heading:  # multi-line headings are joined
                section = heading_label(pending_heading)
                pending_heading = []
            if not line:
                flush()
                continue
            if line[0] in BULLETS or re.match(r"^(o|-|[a-z]\)|\(\w\))\s", line):
                flush()
                line = "- " + line.lstrip(BULLETS + " ")
            if para_page is None:
                para_page = page_no
            para.append(line)
        flush()
    return blocks


def extract_html(path: Path, source: dict) -> list[dict]:
    """Paragraph blocks from the page's <main>, each with its heading path as section."""
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    main = soup.find("main") or soup.body or soup
    for tag in main(["script", "style", "nav", "header", "footer", "form", "button"]):
        tag.decompose()

    blocks: list[dict] = []
    headings = {"h1": "", "h2": "", "h3": "", "h4": ""}
    skipping = False
    last_updated = None
    for el in main.find_all(["h1", "h2", "h3", "h4", "p", "li", "td"]):
        text = fix_spacing(el.get_text(" ", strip=True))
        if not text:
            continue
        if el.name in headings:
            level = int(el.name[1])
            headings[el.name] = text
            for deeper in range(level + 1, 5):
                headings[f"h{deeper}"] = ""
            # Navigation lists, not content.
            skipping = text.lower() in {"on this page", "related links"}
            continue
        if skipping:
            continue
        if text.lower().startswith(("last updated", "banner photo")):
            continue
        if re.fullmatch(r"\d{1,2} \w+ \d{4}", text) and blocks and last_updated is None:
            last_updated = text
            continue
        # Avoid duplicates: a <p> inside an <li> or <td> is covered by its parent.
        if el.name == "p" and el.find_parent(["li", "td"]):
            continue
        if el.name in ("li", "td") and el.find(["li", "td"]):
            continue
        prefix = "- " if el.name == "li" else ""
        section = " > ".join(h for k, h in headings.items() if h and k != "h1")
        blocks.append({"text": prefix + text, "page": 0, "section": section})

    footer = soup.find(string=re.compile(r"Last updated", re.I))
    if footer and not source.get("date"):
        nxt = footer.find_next(string=re.compile(r"\d{4}"))
        if nxt:
            source["date"] = nxt.strip()
    return blocks


def extract_text(path: Path, source: dict) -> list[dict]:
    """Plain text or Markdown: blank-line paragraphs, '#' lines as sections."""
    blocks, section = [], ""
    for para in re.split(r"\n\s*\n", path.read_text(encoding="utf-8")):
        para = para.strip()
        if not para:
            continue
        if para.startswith("#"):
            section = para.lstrip("# ").splitlines()[0]
            para = "\n".join(para.splitlines()[1:]).strip()
            if not para:
                continue
        blocks.append({"text": fix_spacing(para.replace("\n", " ")), "page": 0, "section": section})
    return blocks


def extract_blocks(path: Path, source: dict) -> list[dict]:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return extract_pdf(path, source)
    if suffix in (".html", ".htm"):
        return extract_html(path, source)
    if suffix in (".txt", ".md"):
        return extract_text(path, source)
    raise ValueError(f"Unsupported file type: {suffix} (use .pdf, .html, .txt or .md)")


# --------------------------------------------------------------------------- chunking

def split_long(text: str, limit: int) -> list[str]:
    """Split an over-long paragraph at sentence ends, then by words if needed."""
    sentences = re.split(r"(?<=[.;:!?])\s+(?=[A-Z(\-])", text)
    pieces, current = [], []
    for sentence in sentences:
        words = sentence.split()
        while len(words) > limit:
            if current:
                pieces.append(" ".join(current)); current = []
            pieces.append(" ".join(words[:limit])); words = words[limit:]
        if len(current) + len(words) > limit and current:
            pieces.append(" ".join(current)); current = []
        current.extend(words)
    if current:
        pieces.append(" ".join(current))
    return pieces


def chunk_structure(blocks: list[dict]) -> list[dict]:
    chunks: list[dict] = []
    current: list[dict] = []

    def emit():
        if current:
            chunks.append({
                "text": "\n".join(b["text"] for b in current),
                "page": current[0]["page"],
                "page_end": current[-1]["page"],
                "section": current[0]["section"],
            })

    pieces = []
    for b in blocks:
        for piece in split_long(b["text"], STRUCT_MAX_WORDS):
            pieces.append({**b, "text": piece})

    words = 0
    for b in pieces:
        n = len(b["text"].split())
        new_section = current and b["section"] != current[0]["section"]
        if current and (new_section or words + n > STRUCT_MAX_WORDS):
            emit(); current, words = [], 0
        current.append(b); words += n
    emit()

    # Merge a tiny chunk into the previous one from the same section.
    merged: list[dict] = []
    for c in chunks:
        if (merged and len(c["text"].split()) < STRUCT_MIN_WORDS
                and merged[-1]["section"] == c["section"]
                and len(merged[-1]["text"].split()) + len(c["text"].split()) <= STRUCT_MAX_WORDS + STRUCT_MIN_WORDS):
            merged[-1]["text"] += "\n" + c["text"]
            merged[-1]["page_end"] = c["page_end"]
        else:
            merged.append(c)
    return merged


def chunk_fixed(blocks: list[dict]) -> list[dict]:
    words, where = [], []
    for b in blocks:
        for w in b["text"].split():
            words.append(w); where.append(b)
    chunks, step = [], FIXED_WORDS - FIXED_OVERLAP
    for start in range(0, len(words), step):
        end = min(start + FIXED_WORDS, len(words))
        chunks.append({
            "text": " ".join(words[start:end]),
            "page": where[start]["page"],
            "page_end": where[end - 1]["page"],
            "section": where[start]["section"],
        })
        if end == len(words):
            break
    return chunks


def location(chunk: dict) -> str:
    if chunk["page"]:
        pages = f"p. {chunk['page']}" if chunk["page"] == chunk["page_end"] else f"pp. {chunk['page']}-{chunk['page_end']}"
        return f"{pages}, {chunk['section']}" if chunk["section"] else pages
    return chunk["section"] or "(no section)"


def source_for_file(path: Path) -> dict:
    """Metadata for a file not in SOURCES (the add-document tool uses this)."""
    path = Path(path)
    for source in SOURCES:
        if source["file"] == path.name:
            return dict(source)
    slug = re.sub(r"[^a-z0-9]+", "_", path.stem.lower()).strip("_")
    return {"id": slug, "title": path.stem.replace("_", " ").replace("-", " "),
            "url": path.resolve().as_uri(), "file": path.name, "date": None}


def chunk_file(path: Path | str, source: dict | None = None, design: str = DEFAULT_DESIGN) -> list[dict]:
    """Extract, clean and chunk one file. Each chunk has an id, text and metadata."""
    path = Path(path)
    source = dict(source) if source else source_for_file(path)
    return chunk_blocks(extract_blocks(path, source), source, design)


def chunk_blocks(blocks: list[dict], source: dict, design: str) -> list[dict]:
    raw = chunk_structure(blocks) if design == "structure" else chunk_fixed(blocks)

    chunks = []
    for i, c in enumerate(raw):
        loc = location(c)
        # The structure design embeds a context line; both store the same metadata.
        embed_text = f"{source['title']} > {c['section']}\n{c['text']}" if design == "structure" and c["section"] else c["text"]
        digest = hashlib.sha1(embed_text.encode("utf-8")).hexdigest()[:12]
        chunks.append({
            "id": f"{source['id']}:{design}:{i:04d}:{digest}",
            "text": embed_text,
            "metadata": {
                "source": source["id"],
                "title": source["title"],
                "url": source["url"],
                "date": source.get("date") or "",
                "page": int(c["page"] or 0),
                "page_end": int(c["page_end"] or 0),
                "section": c["section"] or "",
                "location": loc,
                "design": design,
                "chunk": i,
                "words": len(c["text"].split()),
            },
        })
    return chunks


# --------------------------------------------------------------------------- embedding and storage

_client = None
_genai = None


def chroma():
    import chromadb
    from chromadb.config import Settings

    INDEX_DIR.mkdir(exist_ok=True)
    return chromadb.PersistentClient(path=str(INDEX_DIR), settings=Settings(anonymized_telemetry=False))


def collection(design: str = DEFAULT_DESIGN):
    return chroma().get_or_create_collection(f"erasmus_{design}", metadata={"hnsw:space": "cosine"})


def gemini():
    global _genai
    if _genai is None:
        from google import genai
        from api_key import load_api_key
        _genai = genai.Client(api_key=load_api_key())
    return _genai


class DailyQuotaExhausted(RuntimeError):
    pass


def embed(texts: list[str], task_type: str) -> list[list[float]]:
    """Embed a batch, waiting out per-minute limits; raise on the daily limit."""
    from google.genai import errors, types

    for attempt in range(6):
        try:
            # One Content per text: gemini-embedding-2 merges a plain list of
            # strings into a single input and returns one vector for all of them.
            result = gemini().models.embed_content(
                model=EMBED_MODEL, contents=[types.Content(parts=[types.Part(text=t)]) for t in texts],
                config=types.EmbedContentConfig(task_type=task_type, output_dimensionality=EMBED_DIM),
            )
            if len(result.embeddings) != len(texts):
                raise RuntimeError(f"Asked for {len(texts)} embeddings, got {len(result.embeddings)}")
            return [e.values for e in result.embeddings]
        except errors.ClientError as error:
            if error.code != 429:
                raise
            message = str(error)
            if "PerDay" in message or "per day" in message.lower():
                raise DailyQuotaExhausted(message) from error
            wait = 30 * (attempt + 1)
            log(f"Rate limited; waiting {wait}s ...")
            time.sleep(wait)
    raise RuntimeError("Gave up after repeated rate limiting.")


def embed_query(query: str) -> list[float]:
    return embed([query], "RETRIEVAL_QUERY")[0]


def embed_and_store(chunks: list[dict], design: str = DEFAULT_DESIGN, prune: bool = True) -> dict:
    """Embed the chunks that are not stored yet and store each batch at once.

    With prune, stored chunks of the same sources that are no longer produced
    (because chunking changed) are deleted. Returns counts.
    """
    col = collection(design)
    ids = [c["id"] for c in chunks]
    existing = set(col.get(ids=ids, include=[])["ids"]) if ids else set()
    todo = [c for c in chunks if c["id"] not in existing]

    # A chunk whose text is unchanged but whose position moved gets a new id.
    # Its vector is already stored under the old id (the id ends with a hash of
    # the text), so reuse it instead of paying for a new embedding.
    reused = 0
    if todo:
        stored = col.get(where={"source": {"$in": sorted({c["metadata"]["source"] for c in todo})}},
                         include=["embeddings"])
        by_hash = {i.rsplit(":", 1)[-1]: e for i, e in zip(stored["ids"], stored["embeddings"])}
        still_todo = []
        for c in todo:
            vector = by_hash.get(c["id"].rsplit(":", 1)[-1])
            if vector is None:
                still_todo.append(c)
            else:
                col.add(ids=[c["id"]], embeddings=[list(vector)], documents=[c["text"]], metadatas=[c["metadata"]])
                reused += 1
        todo = still_todo

    pruned = 0
    if prune:
        for source in {c["metadata"]["source"] for c in chunks}:
            stored = col.get(where={"source": source}, include=[])["ids"]
            stale = [i for i in stored if i not in set(ids)]
            if stale:
                col.delete(ids=stale); pruned += len(stale)

    added = 0
    for start in range(0, len(todo), EMBED_BATCH):
        batch = todo[start:start + EMBED_BATCH]
        vectors = embed([c["text"] for c in batch], "RETRIEVAL_DOCUMENT")
        col.add(ids=[c["id"] for c in batch], embeddings=vectors,
                documents=[c["text"] for c in batch], metadatas=[c["metadata"] for c in batch])
        added += len(batch)
        log(f"  [{design}] stored {added}/{len(todo)} new chunks")
    return {"embedded": added, "reused": reused, "already_indexed": len(existing), "pruned": pruned, "total": col.count()}


def search(query: str, k: int = 5, design: str = DEFAULT_DESIGN, source: str | None = None) -> list[dict]:
    """Top-k chunks for a query, with metadata and cosine distance."""
    col = collection(design)
    result = col.query(query_embeddings=[embed_query(query)], n_results=k,
                       where={"source": source} if source else None,
                       include=["documents", "metadatas", "distances"])
    return [{"id": i, "text": d, "metadata": m, "distance": dist}
            for i, d, m, dist in zip(result["ids"][0], result["documents"][0],
                                     result["metadatas"][0], result["distances"][0])]


# --------------------------------------------------------------------------- main

def build(dry_run: bool = False, designs=DESIGNS) -> None:
    all_chunks = {d: [] for d in designs}
    for source in SOURCES:
        source = dict(source)
        path = download(source)
        blocks = extract_blocks(path, source)
        for design in designs:
            all_chunks[design].extend(chunk_blocks(blocks, source, design))
        log(f"{source['id']}: {sum(len(b['text'].split()) for b in blocks)} words after cleaning")

    for design, chunks in all_chunks.items():
        sizes = [c["metadata"]["words"] for c in chunks]
        log(f"[{design}] {len(chunks)} chunks, {min(sizes)}-{max(sizes)} words, mean {sum(sizes) / len(sizes):.0f}")
        out = CORPUS_DIR / f"chunks_{design}.jsonl"
        with out.open("w", encoding="utf-8") as f:
            for c in chunks:
                f.write(json.dumps(c, ensure_ascii=False) + "\n")
        log(f"[{design}] wrote {out.relative_to(ROOT)} for inspection")

    if dry_run:
        log("Dry run: nothing embedded.")
        return

    for design, chunks in all_chunks.items():
        try:
            counts = embed_and_store(chunks, design)
        except DailyQuotaExhausted:
            log(f"[{design}] Daily embedding quota reached. Progress is saved; run again after "
                "09:00 (Spain) and only the missing chunks will be embedded.")
            sys.exit(2)
        log(f"[{design}] {counts}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build the Erasmus+ index.")
    parser.add_argument("--dry-run", action="store_true", help="download, extract and chunk, but do not embed")
    parser.add_argument("--design", choices=DESIGNS, help="build only one design")
    args = parser.parse_args()
    build(dry_run=args.dry_run, designs=(args.design,) if args.design else DESIGNS)
