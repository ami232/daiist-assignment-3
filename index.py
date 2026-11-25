"""
Assignment 3: build the index (`uv run python main.py index`).

Use case: the owner, manager or cook of a small US restaurant (including takeout
and delivery-only "ghost" kitchens) checks the food-safety rules they are inspected
against (FDA Food Code: temperatures, cooling, date marking, labels, allergens, sick
staff, handwashing). A wrong answer can make customers ill or fail an inspection,
so the assistant must cite its source and say when the documents do not cover a
question.

Steps, per document:
  1. download the PDF into corpus/ (skipped when it is already there; the PDFs
     are public-domain FDA works, so they are committed with the repo);
  2. extract the text page by page with pypdf and clean it;
  3. chunk it in two ways, one per retrieval design:
       - "sections": one chunk per Food Code section (e.g. 3-501.17) or per
         question of the Handbook, split further only if it is too long;
       - "windows":  fixed windows of 150 words with 30 words of overlap
         (the design from the class notebook);
  4. embed every chunk that has no saved vector yet with gemini-embedding-2,
     and store chunk, metadata and vector in ChromaDB under index/chroma.

Vectors are saved after every batch, so a crash or the daily limit loses
nothing, and running this again embeds only new or changed chunks.

server.py's add_document tool imports chunk_file() and embed_and_store().
"""

from __future__ import annotations

import hashlib
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"
CHROMA_DIR = INDEX_DIR / "chroma"

EMBEDDING_MODEL = "gemini-embedding-2"
BATCH_SIZE = 100  # texts per embedding request

DESIGNS = ("sections", "windows")
SECTION_MAX_WORDS = 300  # a section longer than this is split at its paragraphs
WINDOW_WORDS, WINDOW_OVERLAP = 150, 30

# The corpus. `pages` are PDF page numbers (1-based, inclusive) to keep.
DOCUMENTS = [
    {
        "source": "food_code_2026",
        "short": "Food Code 2026",
        "title": "FDA Food Code 2026, Chapters 1-6",
        "file": "fda-food-code-2026.pdf",
        "url": "https://www.fda.gov/media/194741/download?attachment",
        "date": "2026-09-30",
        "licence": "Public domain (U.S. federal government work)",
        "kind": "food_code",
        # Chapter 1 (definitions) to Chapter 6 (physical facilities). Chapter 7
        # is kept out on purpose: it is the document added later with add_document.
        "pages": [(29, 171)],
    },
    {
        "source": "employee_health_handbook_2020",
        "short": "Employee Health Handbook",
        "title": "FDA Employee Health and Personal Hygiene Handbook (IFS04, 2020)",
        "file": "fda-employee-health-handbook-2020.pdf",
        "url": "https://www.fda.gov/media/77065/download",
        "date": "2020-10",
        "licence": "Public domain (U.S. federal government work)",
        "kind": "handbook",
        # Skip the cover (1), table of contents (2), the list of forms and tables (22),
        # the three decision-tree flowcharts (40-42: their boxes and arrows extract
        # as loose fragments, and Tables 1a-4 hold the same rules) and the blank
        # "Notes" pages (43-45).
        "pages": [(3, 21), (23, 39)],
    },
    {
        "source": "cooling_guide_2024",
        "short": "Cooling Guide",
        "title": "FDA, Cooling Cooked TCS Foods and the FDA Food Code: for Food Employees (2024)",
        "file": "fda-cooling-tcs-foods-2024.pdf",
        "url": "https://www.fda.gov/media/181882/download?attachment",
        "date": "2024-07",
        "licence": "Public domain (U.S. federal government work)",
        "kind": "pages",
        "pages": [(1, 2)],
    },
]

SECTION_RE = re.compile(r"^(\d-\d{3}\.\d{2,3})\s+([A-Z].*)$")  # "3-501.17 Ready-to-Eat..." or "4-204.110 ..."
SUBPART_RE = re.compile(r"^\d-\d{1,3}\s+[A-Z]")  # "3-5 Limitation of Growth..." / "3-501 Temperature..."
QUESTION_START = re.compile(
    r"^(What|Who|When|Where|Why|How|Do|Does|Is|Are|Can|Should|Must|May|Will|If an?)\b"
)
TABLE_OR_FORM_RE = re.compile(r"^(2-201\.1[12]\s+Table\s+\w+.*|Form\s+1-[A-D]\b.*)$")


def log(*args) -> None:
    """Log to stderr: server.py imports this module, and its stdout carries MCP messages."""
    print(*args, file=sys.stderr, flush=True)


# --------------------------------------------------------------------------- download

def download(doc: dict) -> Path:
    """Return the local path of a corpus PDF, downloading it first if needed."""
    path = CORPUS_DIR / doc["file"]
    if path.exists():
        return path
    import httpx

    CORPUS_DIR.mkdir(exist_ok=True)
    log(f"Downloading {doc['url']} ...")
    # fda.gov rejects requests without a browser-like User-Agent.
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/537.36"}
    response = httpx.get(doc["url"], headers=headers, follow_redirects=True, timeout=120)
    response.raise_for_status()
    path.write_bytes(response.content)
    return path


# --------------------------------------------------------------------------- extract and clean

def read_pdf_pages(path: Path, page_ranges=None) -> list[tuple[int, str]]:
    """(pdf page number, raw text) for the selected pages."""
    from pypdf import PdfReader

    reader = PdfReader(str(path))
    wanted = set()
    for first, last in page_ranges or [(1, len(reader.pages))]:
        wanted.update(range(first, min(last, len(reader.pages)) + 1))
    return [(n, reader.pages[n - 1].extract_text() or "") for n in sorted(wanted)]


def clean_line(line: str) -> str:
    line = line.replace("\u00a0", " ").replace("\u2011", "-")  # no-break space, non-breaking hyphen
    line = line.replace("\u00ba", "\u00b0")  # the Food Code writes "5\u00baC" (ordinal sign) for "5\u00b0C"
    line = re.sub(r"(\d)o([CF])\b", "\\1\u00b0\\2", line)  # ... and sometimes "68oC (155oF)" with a letter o
    line = line.replace("\u00b0\u0160", "\u00b0")  # the Handbook prints "100\u00b0\u0160F"
    for ligature, letters in {"\ufb01": "fi", "\ufb02": "fl", "\ufb00": "ff", "\ufb03": "ffi", "\ufb04": "ffl"}.items():
        line = line.replace(ligature, letters)  # "quali\ufb01ed" -> "qualified"
    line = line.replace("*", "")  # Food Code marks defined terms as *FOOD EMPLOYEE
    # Food Code priority markers after a requirement: "... 15 seconds. P" or "...; Pf and"
    line = re.sub(r"\s+(?:Pf|PF|P)(?=[\s;,.]|$)", "", line)
    if line.strip() in ("P", "Pf", "PF"):
        return ""  # a marker printed on a line of its own
    return re.sub(r"\s+", " ", line).strip()


def page_lines(raw: str, kind: str) -> tuple[str | None, list[str]]:
    """Split a page into (printed page number, clean content lines)."""
    lines = [clean_line(l) for l in raw.splitlines()]
    lines = [l for l in lines if l]
    printed = None
    if kind == "food_code":
        # Every page starts with "FDA Food Code 2026  Chapter 3. Food" and then the printed page number.
        if lines and lines[0].startswith("FDA Food Code"):
            lines = lines[1:]
        if lines and re.fullmatch(r"\d+|[ivxlc]+", lines[0]):
            printed, lines = lines[0], lines[1:]
        lines = [l for l in lines if l != "This page is intentionally left blank."]
    elif kind == "handbook":
        if lines and re.fullmatch(r"\d+", lines[0]):
            printed, lines = lines[0], lines[1:]
    else:
        lines = [l for l in lines if not re.fullmatch(r"www\.fda\.gov/RetailFoodProtection \w+ \d{4}", l)]
        if lines and re.fullmatch(r"\d+", lines[0]):
            lines = lines[1:]
    return printed, lines


def join_lines(lines: list[str]) -> str:
    """Join wrapped lines; keep a word hyphenated across lines ("animal-" + "derived") together."""
    text = ""
    for line in lines:
        if not text:
            text = line
        elif text.endswith("-") and not text.endswith(" -"):
            text += line
        else:
            text += " " + line
    return text


# --------------------------------------------------------------------------- units (structure)

def section_key(number: str) -> tuple[int, int, int]:
    """'4-204.110' -> (4, 204, 110), so that 4-204.110 sorts after 4-204.19."""
    chapter, rest = number.split("-")
    subpart, item = rest.split(".")
    return int(chapter), int(subpart), int(item)


def food_code_units(pages: list[tuple[int, str]]) -> list[dict]:
    """One unit per Food Code section ("3-501.17 Ready-to-Eat..."), with its pages."""
    units, current, last_key = [], None, (0, 0, 0)
    for pdf_page, raw in pages:
        printed, lines = page_lines(raw, "food_code")
        page = printed or str(pdf_page)
        for line in lines:
            match = SECTION_RE.match(line)
            # A real heading is short and numbered after the previous one; this
            # rejects cross-references such as "3-501.17 of this Code" at a line start.
            if match and len(line) < 100 and section_key(match.group(1)) > last_key:
                last_key = section_key(match.group(1))
                current = {
                    "section": match.group(1),
                    "heading": match.group(2).strip(),
                    "lines": [],
                    "line_pages": [],
                    "pages": [page],
                }
                units.append(current)
                continue
            if current is not None and not current["lines"] and not current["heading"].endswith(".") \
                    and len(line) < 70 and (line.endswith(".") or len(line.split()) <= 3) \
                    and not line.startswith("("):
                current["heading"] += " " + line  # a heading that wraps: "...Date" + "Marking."
                continue
            if re.match(r"Chapter \d\.", line):
                current = None  # a new chapter: its title (which may wrap) is not part of the last section
                continue
            if line in ("Parts:", "Subparts:") or SUBPART_RE.match(line):
                continue  # navigation lists and part/subpart titles, not rules
            if current is None:
                continue  # text before the chapter's first section is headings only
            add_line(current, line, page)
    return units


def handbook_units(pages: list[tuple[int, str]]) -> list[dict]:
    """One unit per question ("What should a manager do when...?"), table or form."""
    units, current = [], None
    pending_question: list[str] = []
    in_forms = False  # the forms and tables at the back contain questions that are not headings
    for pdf_page, raw in pages:
        printed, lines = page_lines(raw, "handbook")
        page = printed or str(pdf_page)
        for line in lines:
            if pending_question:  # a question heading that wraps onto the next line
                pending_question.append(line)
                joined = " ".join(pending_question)
                if "?" in line and len(joined) <= 220:
                    current = _new_unit(units, joined, page)
                    pending_question = []
                elif "?" in line or len(pending_question) > 3:  # too long: it was ordinary text
                    if current is None:
                        current = _new_unit(units, "Introduction", page)
                    for pending in pending_question:
                        add_line(current, pending, page)
                    pending_question = []
                continue
            if TABLE_OR_FORM_RE.match(line):
                current = _new_unit(units, line, page)
                in_forms = True
                continue
            if in_forms and current is not None and not current["lines"] and len(line.split()) <= 4 \
                    and not line.startswith(("Food employees", "Preventing")):
                current["heading"] += " " + line  # a table title that wraps: "...for Symptomatic" + "Food Employees"
                continue
            if not in_forms and QUESTION_START.match(line) and not line.startswith("•"):
                if "?" in line:
                    current = _new_unit(units, line, page)
                    continue
                if len(line) > 60:  # long line with no "?" yet: probably a wrapped question
                    pending_question = [line]
                    continue
            if current is None:
                current = _new_unit(units, "Introduction", page)
            add_line(current, line, page)
    # A "question" that never closed with "?" was ordinary text: put it back.
    if pending_question and current is not None:
        for pending in pending_question:
            add_line(current, pending, current["pages"][-1])
    return [u for u in units if u["lines"]]


def _new_unit(units: list, heading: str, page: str) -> dict:
    unit = {"section": None, "heading": heading.rstrip(), "lines": [], "line_pages": [], "pages": [page]}
    units.append(unit)
    return unit


def add_line(unit: dict, line: str, page: str) -> None:
    """Add a content line to a unit and remember the page it is on."""
    if not unit["lines"]:
        unit["pages"] = [page]  # the unit starts where its first line is, not where its heading is
    unit["lines"].append(line)
    unit["line_pages"].append(page)
    if unit["pages"][-1] != page:
        unit["pages"].append(page)


def page_units(pages: list[tuple[int, str]]) -> list[dict]:
    """Fallback for documents without a structure we know: one unit per page."""
    units = []
    for pdf_page, raw in pages:
        _, lines = page_lines(raw, "pages")
        if lines:
            units.append({"section": None, "heading": f"Page {pdf_page}", "lines": lines,
                          "line_pages": [str(pdf_page)] * len(lines), "pages": [str(pdf_page)]})
    return units


# --------------------------------------------------------------------------- chunks

def split_long(lines: list[tuple[str, str]], max_words: int) -> list[list[tuple[str, str]]]:
    """Pack consecutive (line, page) pairs into pieces of at most max_words, breaking at paragraph starts if possible."""
    paragraph_start = re.compile(r"^(\([A-Z0-9]+\)|[\"“]|•|\d+\.)")
    blocks, block = [], []
    for line, page in lines:
        if block and paragraph_start.match(line):
            blocks.append(block)
            block = []
        block.append((line, page))
    if block:
        blocks.append(block)

    pieces, piece, words = [], [], 0
    for block in blocks:
        n = sum(len(l.split()) for l, _ in block)
        if piece and words + n > max_words:
            pieces.append(piece)
            piece, words = [], 0
        if n > max_words:  # one huge paragraph: cut it into word windows
            flat = [(w, p) for l, p in block for w in l.split()]
            for start in range(0, len(flat), max_words):
                part = flat[start : start + max_words]
                pieces.append([(" ".join(w for w, _ in part), part[0][1])])
            continue
        piece += block
        words += n
    if piece:
        pieces.append(piece)
    return pieces


def cite_label(doc: dict, section: str | None, pages: list[str]) -> str:
    """The text the agent must copy into its answer, e.g. "Food Code 2026 §3-501.17"."""
    if section:
        return f"{doc['short']} §{section}"
    return f"{doc['short']} p. {pages[0]}"


def chunk_id(design: str, source: str, text: str) -> str:
    return hashlib.sha1(f"{design}|{source}|{text}".encode()).hexdigest()[:20]


def make_chunk(design, doc, text, heading, sections, pages, part=None) -> dict:
    sections = [s for s in sections if s]
    page_text = f"p. {pages[0]}" if len(pages) == 1 else f"pp. {pages[0]}-{pages[-1]}"
    location = f"§{sections[0]} ({page_text})" if design == "sections" and sections else page_text
    cite = cite_label(doc, sections[0] if design == "sections" and sections else None, pages)
    if part:
        heading = f"{heading} (part {part})"
    return {
        "id": chunk_id(design, doc["source"], text),
        "text": text,
        "metadata": {
            "design": design,
            "source": doc["source"],
            "document": doc["title"],
            "heading": heading,
            "location": location,
            "cite": cite,
            # "|3-501.17|3-501.18|" and "|74|75|": strings, because ChromaDB metadata
            # cannot hold lists. evaluate.py checks a hit against them.
            "sections": "|" + "|".join(sections) + "|" if sections else "",
            "pages": "|" + "|".join(pages) + "|",
            "words": len(text.split()),
        },
    }


def section_chunks(doc: dict, units: list[dict]) -> list[dict]:
    chunks = []
    for unit in units:
        pieces = split_long(list(zip(unit["lines"], unit["line_pages"])), SECTION_MAX_WORDS)
        for i, piece in enumerate(pieces, start=1):
            text = join_lines([line for line, _ in piece])
            pages = list(dict.fromkeys(page for _, page in piece))
            part = i if len(pieces) > 1 else None
            heading = unit["heading"].rstrip(". ")
            chunks.append(make_chunk("sections", doc, text, heading, [unit["section"]], pages, part))
    return chunks


def window_chunks(doc: dict, units: list[dict]) -> list[dict]:
    """Fixed word windows over the whole document, ignoring its structure (except for metadata)."""
    words, word_page, word_section = [], [], []
    for unit in units:
        text_words = join_lines(unit["lines"]).split()
        line_word_pages = [p for line, p in zip(unit["lines"], unit["line_pages"]) for _ in line.split()]
        # join_lines can merge a hyphenated word across lines, so the two lists may differ by a few words.
        for i, w in enumerate(text_words):
            words.append(w)
            word_page.append(line_word_pages[min(i, len(line_word_pages) - 1)])
            word_section.append(unit["section"])
    chunks = []
    step = WINDOW_WORDS - WINDOW_OVERLAP
    for start in range(0, max(len(words) - WINDOW_OVERLAP, 1), step):
        end = min(start + WINDOW_WORDS, len(words))
        pages = list(dict.fromkeys(word_page[start:end]))
        sections = list(dict.fromkeys(s for s in word_section[start:end] if s))
        text = " ".join(words[start:end])
        chunks.append(make_chunk("windows", doc, text, doc["title"], sections, pages))
    return chunks


def doc_for_path(path: Path) -> dict:
    """The DOCUMENTS entry for a corpus file, or a new entry for any other file (add_document)."""
    for doc in DOCUMENTS:
        if (CORPUS_DIR / doc["file"]).resolve() == path.resolve():
            return doc
    stem = path.stem
    source = re.sub(r"[^a-z0-9]+", "_", stem.lower()).strip("_")
    short = re.sub(r"[-_]+", " ", stem).strip().title()
    if stem.lower().startswith("fda-food-code-2026"):
        short = "Food Code 2026"  # an extract of the Food Code cites like the Food Code
    title = short
    if path.suffix.lower() == ".pdf":
        from pypdf import PdfReader

        title = (PdfReader(str(path)).metadata or {}).get("/Title") or short
    return {"source": source, "short": short, "title": str(title), "file": path.name, "url": "", "kind": None, "pages": None}


def units_for(path: Path, doc: dict) -> list[dict]:
    if path.suffix.lower() in (".txt", ".md"):
        lines = [clean_line(l) for l in path.read_text(encoding="utf-8").splitlines()]
        lines = [l for l in lines if l]
        return [{"section": None, "heading": path.stem, "lines": lines, "line_pages": ["1"] * len(lines), "pages": ["1"]}]
    pages = read_pdf_pages(path, doc.get("pages"))
    kind = doc.get("kind")
    if kind is None:  # an added document: guess its structure from the text
        sample = "\n".join(t for _, t in pages)
        headings = re.findall(r"(?m)^\d-\d{3}\.\d{2,3}\s+[A-Z]", sample)
        kind = "food_code" if len(headings) >= 3 else "pages"
    if kind == "food_code":
        return food_code_units(pages)
    if kind == "handbook":
        return handbook_units(pages)
    return page_units(pages)


def chunk_file(path: str | Path, design: str = "sections") -> list[dict]:
    """Extract, clean and chunk one file (PDF, .txt or .md) for one design."""
    path = Path(path)
    doc = doc_for_path(path)
    units = units_for(path, doc)
    if design == "sections":
        return section_chunks(doc, units)
    if design == "windows":
        return window_chunks(doc, units)
    raise ValueError(f"Unknown design {design!r}; use one of {DESIGNS}.")


def file_sha256(path: str | Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


# --------------------------------------------------------------------------- embed and store

_client = None


def gemini_client():
    global _client
    if _client is None:
        from google import genai
        from google.genai import types

        from api_key import load_api_key

        # As in the class notebook: on a rate limit or server error, wait a minute and retry.
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
    """Embed already-prefixed texts in one request (at most BATCH_SIZE)."""
    from google.genai import types

    result = gemini_client().models.embed_content(
        model=EMBEDDING_MODEL,
        # One Content per text: a plain list of strings would be merged into one vector.
        contents=[types.Content(parts=[types.Part(text=t)]) for t in texts],
    )
    return [e.values for e in result.embeddings]


def document_prefix(chunk: dict) -> str:
    """gemini-embedding-2 document format: the title travels with every chunk."""
    m = chunk["metadata"]
    title = f"{m['document']} - {m['heading']}" if m["design"] == "sections" else m["document"]
    return f"title: {title} | text: {chunk['text']}"


def open_collection(design: str):
    import chromadb
    from chromadb.config import Settings

    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    db = chromadb.PersistentClient(path=str(CHROMA_DIR), settings=Settings(anonymized_telemetry=False))
    return db.get_or_create_collection(
        name=design,
        configuration={"hnsw": {"space": "cosine"}},
        embedding_function=None,  # we always pass our own Gemini vectors
    )


def embed_and_store(chunks: list[dict], collection, extra_metadata: dict | None = None) -> int:
    """Embed the chunks that are not in the collection yet and store them, batch by batch.

    Returns how many chunks were embedded.
    """
    ids = [c["id"] for c in chunks]
    existing = set(collection.get(ids=ids, include=[])["ids"]) if ids else set()
    todo = [c for c in chunks if c["id"] not in existing]
    for start in range(0, len(todo), BATCH_SIZE):
        batch = todo[start : start + BATCH_SIZE]
        vectors = embed_texts([document_prefix(c) for c in batch])
        collection.add(
            ids=[c["id"] for c in batch],
            embeddings=vectors,
            documents=[c["text"] for c in batch],
            metadatas=[{**c["metadata"], **(extra_metadata or {})} for c in batch],
        )  # saved to disk now: a later failure does not lose this batch
        log(f"  embedded {start + len(batch)}/{len(todo)}")
    return len(todo)


def remove_stale(collection, chunks: list[dict], source: str) -> int:
    """Delete chunks of `source` that the current chunking no longer produces (e.g. after a code change)."""
    keep = {c["id"] for c in chunks}
    stored = collection.get(where={"source": source}, include=[])["ids"]
    stale = [i for i in stored if i not in keep]
    if stale:
        collection.delete(ids=stale)
    return len(stale)


# --------------------------------------------------------------------------- main

def main() -> None:
    print(f"Index stage: {len(DOCUMENTS)} documents, designs {', '.join(DESIGNS)}\n")
    total_words = 0
    for doc in DOCUMENTS:
        path = download(doc)
        units = units_for(path, doc)
        words = sum(len(join_lines(u["lines"]).split()) for u in units)
        total_words += words
        print(f"{doc['short']:<26} {words:>6,} words after cleaning  ({doc['file']})")
    print(f"{'Total':<26} {total_words:>6,} words\n")

    for design in DESIGNS:
        collection = open_collection(design)
        print(f"Design '{design}':")
        for doc in DOCUMENTS:
            path = CORPUS_DIR / doc["file"]
            chunks = chunk_file(path, design)
            removed = remove_stale(collection, chunks, doc["source"])
            embedded = embed_and_store(chunks, collection, {"file_sha256": file_sha256(path)})
            avg = sum(c["metadata"]["words"] for c in chunks) / max(len(chunks), 1)
            print(
                f"  {doc['short']:<26} {len(chunks):>4} chunks (avg {avg:.0f} words), "
                f"{embedded} newly embedded" + (f", {removed} stale removed" if removed else "")
            )
        print(f"  collection now holds {collection.count()} chunks\n")
    print(f"Index saved in {CHROMA_DIR.relative_to(ROOT)}/")


if __name__ == "__main__":
    main()
