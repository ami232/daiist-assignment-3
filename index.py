"""
Assignment 3: build the index (`main.py index`).

Corpus: the EU Deforestation Regulation (EUDR) as a medium-sized cocoa importer
needs it. Steps:

1. download  the documents in CORPUS into corpus/ if they are missing
2. extract   structure-aware units: an article, a guidance section or an FAQ question,
             each with its source and location (e.g. "Article 9(1)", "Guidance §4(e)",
             "FAQ 1.3, p. 13")
3. chunk     two designs, so they can be compared by hit rate in evaluate.py:
               structure: one chunk per unit, long units split at paragraph boundaries
               fixed:     150-word windows with a 30-word overlap, ignoring structure
4. embed     with gemini-embedding-2, saving each batch in ChromaDB (index/chroma) as soon
             as it arrives; chunks that already have a vector are never embedded again

server.py imports chunk_file() and embed_and_store() for its add_document tool.

    uv run python index.py              # everything
    uv run python index.py --dry-run    # stop before embedding, print chunk statistics
"""

import hashlib
import json
import re
import sys
import time
from pathlib import Path

import httpx
from bs4 import BeautifulSoup
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"
CHROMA_DIR = INDEX_DIR / "chroma"

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768          # smaller vectors keep index/ well under 90 MB; quality loss is small
BATCH = 50               # texts per embedding request (each text counts towards the daily quota)
DESIGNS = ["structure", "fixed"]
DEFAULT_DESIGN = "structure"   # the design server.py searches; set from the hit rates in evaluate.py
DEFAULT_HYBRID = False         # add BM25 keyword ranking to the vector ranking (also chosen by hit rate)

MAX_WORDS = 350          # structure design: split units longer than this
WINDOW, OVERLAP = 150, 30  # fixed design

CELLAR = "https://publications.europa.eu/resource/celex/"
CORPUS = [
    {"source": "EUDR", "file": "eudr_consolidated_2026-09-18.html",
     "title": "Regulation (EU) 2023/1115 (EUDR), consolidated text of 18.9.2026",
     "url": CELLAR + "02023R1115-20260918"},
    {"source": "Guidance", "file": "eudr_guidance_C2026-3896.html",
     "title": "Commission Guidance document for Regulation (EU) 2023/1115 (C/2026/3896)",
     "url": CELLAR + "52026XC03896"},
    {"source": "FAQ", "file": "eudr_faq_v5_2026-04.pdf",
     "title": "Commission FAQ on the implementation of the EUDR, version 5 (April 2026)",
     "url": "https://webgate.ec.europa.eu/circabc-ewpp/d/d/workspace/SpacesStore/"
            "4dc28987-bc5a-4b71-bd46-a13b611f3ebb/download"},
]


def log(*args):
    print(*args, file=sys.stderr, flush=True)  # stderr: server.py imports this module and stdout carries MCP


# ---------------------------------------------------------------- 1. download

def download_corpus() -> None:
    for doc in CORPUS:
        path = CORPUS_DIR / doc["file"]
        if path.exists():
            continue
        log(f"downloading {doc['file']}")
        # EUR-Lex blocks scripts; the Publications Office (Cellar) serves the same texts by content negotiation.
        headers = {"Accept": "application/xhtml+xml", "Accept-Language": "eng"} if doc["url"].startswith(CELLAR) else {}
        response = httpx.get(doc["url"], headers=headers, follow_redirects=True, timeout=120)
        response.raise_for_status()
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(response.content)


# ---------------------------------------------------------------- 2. extract and clean

def clean(text: str) -> str:
    text = re.sub(r"[►▼]\s*(?:M\d+|B|C\d+|A\d+)\b|◄", " ", text)   # amendment markers of consolidated texts
    text = text.replace("\xa0", " ").replace("­", "")
    text = re.sub(r"(\w) -(\w)", r"\1-\2", text)                     # PDF artefact: "non -deforestation"
    text = re.sub(r"\s+([,.;:)])", r"\1", text)                       # PDF artefact: "using ,"
    text = re.sub(r"\(\s+", "(", text)
    return re.sub(r"\s+", " ", text).strip()


def block_text(element) -> str:
    """Text of an HTML block; tables become one line per row, cells joined by ' | '."""
    for tag in element.find_all(class_=["oj-note-tag", "footnote"]):
        tag.decompose()  # footnote numbers in the text
    if element.name == "table" or element.find("table"):
        rows = []
        for tr in element.find_all("tr"):
            cells = [clean(td.get_text(" ")) for td in tr.find_all("td", recursive=False)]
            rows.append(" | ".join(c for c in cells if c))
        return "\n".join(r for r in rows if r)
    return clean(element.get_text(" "))


def units_consolidated(soup, doc):
    """Consolidated EUR-Lex act: one unit per article (paragraphs kept apart) and per annex."""
    units = []
    for div in soup.find_all("div", class_="eli-subdivision", id=re.compile(r"^art_")):
        number = clean(div.find(class_="title-article-norm").get_text(" ")).replace("Article ", "")
        title = div.find(class_="eli-title")
        paragraphs = []
        for child in div.find_all(recursive=False):
            classes = child.get("class") or []
            if "title-article-norm" in classes or "eli-title" in classes or "modref" in classes:
                continue
            text = block_text(child)
            if text:
                label = re.match(r"^(\d+[a-z]?)\.\s", text)
                paragraphs.append((f"({label.group(1)})" if label else "", text))
        units.append({"location": f"Article {number}", "title": clean(title.get_text(" ")) if title else "",
                      "paragraphs": paragraphs, "page": None})
    for div in soup.find_all("div", id=re.compile(r"^anx_")):
        name = "Annex " + div["id"].removeprefix("anx_")
        paragraphs = []
        for child in div.find_all(recursive=False):
            classes = " ".join(child.get("class") or [])
            if child.name == "hr" or "title-annex-1" in classes or "modref" in classes:
                continue
            text = block_text(child)
            if text:
                paragraphs.append(("", text))
        units.append({"location": name, "title": "", "paragraphs": paragraphs, "page": None})
    return units


def units_oj(soup, doc):
    """Official Journal layout (the Guidance notice, implementing acts): split at headings."""
    units, current, top, sub = [], None, "", ""
    body = soup.body or soup
    for element in body.find_all(["p", "table"]):
        if element.find_parent("table") is not None:
            continue  # table cells are read with their table
        classes = " ".join(element.get("class") or [])
        if "oj-note" in classes:
            continue  # footnotes at the end of the notice
        text = block_text(element)
        if not text:
            continue
        if "oj-ti-art" in classes:                          # "Article 1" in an act
            current = {"location": text, "title": "", "paragraphs": [], "page": None}
            units.append(current)
        elif "oj-sti-art" in classes and current:
            current["title"] = text
        elif "oj-ti-grseq-1" in classes or ("oj-doc-ti" in classes and text.upper().startswith("ANNEX")):
            numbered = re.match(r"^(\d+)\.\s+(.*)", text)
            lettered = re.match(r"^\(([a-z])\)\s+(.*)", text)
            question = re.match(r"^(Q\d+):\s*(.*)", text)
            if numbered and numbered.group(2).isupper():     # "4. DUE DILIGENCE": a top-level section
                top = sub = numbered.group(1)
                location = f"{doc['source']} §{top}"
            elif numbered:                                   # "2. Clarification ..." inside section 11
                sub = f"{top}.{numbered.group(1)}"
                location = f"{doc['source']} §{sub}"
            elif lettered:
                location = f"{doc['source']} §{sub}({lettered.group(1)})"
            elif question:
                location = f"{doc['source']} §{sub} {question.group(1)}"
            elif text.upper().startswith("ANNEX"):
                location = text.title()
            else:
                location = f"{doc['source']} §{top} {text}" if top else f"{doc['source']} {text.title()}"
            title = numbered.group(2) if numbered else lettered.group(2) if lettered else question.group(2) if question else text
            current = {"location": location, "title": title.capitalize() if title.isupper() else title,
                       "paragraphs": [], "page": None}
            units.append(current)
        elif "oj-doc-ti" in classes or "oj-hd" in classes:
            continue  # document title block
        else:
            if current is None:
                current = {"location": f"{doc['source']} preamble", "title": "", "paragraphs": [], "page": None}
                units.append(current)
            current["paragraphs"].append(("", text))
    return units


def units_faq(path: Path, doc):
    """The FAQ PDF: skip the table of contents, one unit per numbered question, with its page."""
    lines = []
    for page_number, page in enumerate(PdfReader(path).pages, start=1):
        page_lines = (page.extract_text() or "").splitlines()
        if page_lines and page_lines[0].strip() == "":
            page_lines = page_lines[1:]
        if page_lines and page_lines[0].strip() == str(page_number):
            page_lines = page_lines[1:]  # running page number at the top
        lines += [(page_number, line) for line in page_lines]

    question_start = re.compile(r"^\s*(\d{1,2}\.\d{1,2}(?:\.\d{1,2})?)\.?\s+([A-Z(].*)$")
    title_end = re.compile(r"(\?|\((UPDATED|NEW|DELETED)\))\s*$")
    section_start = re.compile(r"^\s*(\d{1,2})\.\s+([A-Z][^.]{2,80})\s*$")
    toc_line = re.compile(r"\.{5,}\s*\d+\s*$")

    # The table of contents lists every question with dot leaders; the body starts after its last entry.
    toc_end = max(i for i, (_, line) in enumerate(lines) if toc_line.search(line))
    units, current, title_open, seen = [], None, False, set()
    for page_number, line in lines[toc_end + 1:]:
        match = question_start.match(line)
        if match and match.group(1) not in seen:
            seen.add(match.group(1))
            current = {"location": f"FAQ {match.group(1)}", "title": match.group(2).strip(),
                       "paragraphs": [], "page": page_number}
            units.append(current)
            title_open = not title_end.search(line)
            continue
        if title_open and current:                  # question titles can run over two or three lines
            current["title"] += " " + line.strip()
            title_open = not title_end.search(line) and len(current["title"]) < 300
            continue
        if section_start.match(line) and current and not current["paragraphs"]:
            continue
        if section_start.match(line):
            continue                                # "2. Due diligence" chapter headings
        if current is not None and line.strip():
            current["paragraphs"].append(("", line.strip()))
    for unit in units:
        unit["title"] = clean(re.sub(r"\((UPDATED|NEW|DELETED)\)", "", unit["title"]))
        # PDF lines are not paragraphs: rejoin them, then split at sentence ends into ~paragraph blocks.
        text = clean(" ".join(t for _, t in unit["paragraphs"]))
        sentences = re.split(r"(?<=[.:;])\s+(?=[A-Z(•–-])", text)
        unit["paragraphs"] = [("", s) for s in sentences if s]
    return units


def units_generic_pdf(path: Path, doc):
    """Any other PDF (add_document): one unit per page."""
    units = []
    for page_number, page in enumerate(PdfReader(path).pages, start=1):
        text = clean(page.extract_text() or "")
        if text:
            units.append({"location": f"p. {page_number}", "title": "", "page": page_number,
                          "paragraphs": [("", s) for s in re.split(r"(?<=[.;:])\s+(?=[A-Z])", text)]})
    return units


def units_text(path: Path, doc):
    """Plain text or Markdown (add_document): Markdown headings start units, blank lines split paragraphs."""
    units, current = [], None
    for block in re.split(r"\n\s*\n", path.read_text(encoding="utf-8", errors="replace")):
        block = block.strip()
        if not block:
            continue
        heading = re.match(r"^#+\s+(.*)", block)
        if heading or current is None:
            current = {"location": heading.group(1) if heading else "start", "title": "", "paragraphs": [], "page": None}
            units.append(current)
            if heading:
                continue
        current["paragraphs"].append(("", clean(block)))
    return units


def extract_units(path: Path, doc: dict) -> list[dict]:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return units_faq(path, doc) if doc["source"] == "FAQ" else units_generic_pdf(path, doc)
    if suffix in (".html", ".htm", ".xhtml", ".xml"):
        soup = BeautifulSoup(path.read_bytes(), "html.parser")
        if soup.find(class_="title-article-norm"):  # consolidated text layout (OJ acts use oj-ti-art)
            return units_consolidated(soup, doc)
        return units_oj(soup, doc)
    return units_text(path, doc)


# ---------------------------------------------------------------- 3. chunk

def make_chunk(doc, unit, text, design, index, location=None, covers=None):
    location = location or unit["location"]
    if unit.get("page") and "p." not in location:
        location += f", p. {unit['page']}"
    header = f"[{doc['title']} | {location}{' | ' + unit['title'] if unit['title'] else ''}]"
    words = len(text.split())
    digest = hashlib.sha1(f"{doc['file']}|{design}|{location}|{text}".encode()).hexdigest()[:16]
    return {"id": f"{design}-{doc['source']}-{index:04d}-{digest}", "design": design,
            "source": doc["source"], "file": doc["file"], "doc_title": doc["title"], "location": location,
            "unit_title": unit["title"], "text": text, "embed_text": f"{header}\n{text}", "words": words,
            "covers": covers or [location]}  # every unit the chunk contains, for hit-rate scoring


def chunk_structure(doc, units):
    chunks = []
    for unit in units:
        paragraphs = unit["paragraphs"]
        total = sum(len(t.split()) for _, t in paragraphs)
        if total < 5:
            continue
        if total <= MAX_WORDS:
            chunks.append(make_chunk(doc, unit, "\n".join(t for _, t in paragraphs), "structure", len(chunks)))
            continue
        # Long unit: group whole paragraphs up to MAX_WORDS; the location names the paragraphs it holds.
        pieces = []
        for label, text in paragraphs:
            if len(text.split()) <= MAX_WORDS:
                pieces.append((label, text))
                continue
            sentences, buffer = re.split(r"(?<=[.;:])\s+", text), ""
            for sentence in sentences:
                if buffer and len((buffer + " " + sentence).split()) > MAX_WORDS:
                    pieces.append((label, buffer))
                    buffer = ""
                buffer = (buffer + " " + sentence).strip()
            pieces.append((label, buffer))
        group, size, parts = [], 0, []
        for label, text in pieces:
            n = len(text.split())
            if group and size + n > MAX_WORDS:
                parts.append(group)
                group, size = [], 0
            group.append((label, text))
            size += n
        parts.append(group)
        for part_number, group in enumerate(parts, start=1):
            labels = [label for label, _ in group if label]
            if labels:
                location = unit["location"] + (labels[0] if len(labels) == 1 else f"{labels[0]}–{labels[-1]}")
            else:
                location = f"{unit['location']} (part {part_number}/{len(parts)})"
            text = "\n".join(t for _, t in group)
            chunks.append(make_chunk(doc, unit, text, "structure", len(chunks), location))
    return chunks


def chunk_fixed(doc, units):
    """150-word windows over the whole document. Each window is cited by the unit its first word is in."""
    words, owner = [], []
    for unit_index, unit in enumerate(units):
        for _, text in unit["paragraphs"]:
            for word in text.split():
                words.append(word)
                owner.append(unit_index)
    chunks, start = [], 0
    while start < len(words):
        end = min(start + WINDOW, len(words))
        unit = units[owner[start]]
        covers = [units[i]["location"] for i in dict.fromkeys(owner[start:end])]
        chunks.append(make_chunk(doc, unit, " ".join(words[start:end]), "fixed", len(chunks), covers=covers))
        if end == len(words):
            break
        start = end - OVERLAP
    return chunks


def doc_for(path: Path) -> dict:
    """Metadata for a corpus file, or a generic entry for a file given to add_document."""
    for doc in CORPUS:
        if doc["file"] == path.name:
            return doc
    if "benchmarking" in path.name or "2025-1093" in path.name:
        return {"source": "Benchmarking", "file": path.name, "url": CELLAR + "32025R1093",
                "title": "Commission Implementing Regulation (EU) 2025/1093: country risk list"}
    return {"source": path.stem, "file": path.name, "title": path.stem.replace("_", " "), "url": str(path)}


def chunk_file(path, design: str = DEFAULT_DESIGN) -> list[dict]:
    """Extract, clean and chunk one file. Used by main() and by server.py's add_document tool."""
    path = Path(path)
    doc = doc_for(path)
    units = extract_units(path, doc)
    return chunk_structure(doc, units) if design == "structure" else chunk_fixed(doc, units)


# ---------------------------------------------------------------- 4. embed and store

def collection(design: str):
    import chromadb  # imported here so --dry-run works without touching the index
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return client.get_or_create_collection(design, metadata={"hnsw:space": "cosine"})


class DailyQuotaExhausted(RuntimeError):
    pass


def embed_texts(texts: list[str], task: str) -> list[list[float]]:
    """Embed with Gemini. Retries per-minute limits; raises DailyQuotaExhausted on the daily one."""
    from google import genai
    from google.genai import types
    from api_key import load_api_key

    client = genai.Client(api_key=load_api_key())
    # gemini-embedding-2 is multimodal: a plain list of strings is read as the parts of ONE input and
    # returns a single vector. Each text must be its own Content to get one vector per text.
    contents = [types.Content(parts=[types.Part(text=t)]) for t in texts]
    for attempt in range(6):
        try:
            result = client.models.embed_content(
                model=EMBED_MODEL, contents=contents,
                config=types.EmbedContentConfig(task_type=task, output_dimensionality=EMBED_DIM))
            if len(result.embeddings) != len(texts):
                raise RuntimeError(f"asked for {len(texts)} vectors, got {len(result.embeddings)}")
            return [e.values for e in result.embeddings]
        except Exception as error:  # noqa: BLE001 - the API raises several error types for quota
            message = str(error)
            if any(s in message for s in ("SSL", "EOF", "Connection", "timed out", "503", "500")):
                log(f"  network error, retrying in 10s: {message[:80]}")
                time.sleep(10)
                continue
            if "429" not in message and "RESOURCE_EXHAUSTED" not in message:
                raise
            if "PerDay" in message or "per day" in message.lower():
                raise DailyQuotaExhausted(message[:300]) from error
            wait = 20 * (attempt + 1)
            log(f"  rate limited, waiting {wait}s")
            time.sleep(wait)
    raise RuntimeError("still rate limited after 6 attempts")


def embed_and_store(chunks: list[dict], design: str = DEFAULT_DESIGN) -> int:
    """Embed only chunks whose id has no stored vector; store each batch immediately. Returns how many were embedded."""
    store = collection(design)
    existing = set(store.get(ids=[c["id"] for c in chunks], include=[])["ids"]) if chunks else set()
    todo = [c for c in chunks if c["id"] not in existing]
    for start in range(0, len(todo), BATCH):
        batch = todo[start:start + BATCH]
        vectors = embed_texts([c["embed_text"] for c in batch], "RETRIEVAL_DOCUMENT")
        store.add(ids=[c["id"] for c in batch], embeddings=vectors, documents=[c["text"] for c in batch],
                  metadatas=[{k: c[k] for k in ("source", "file", "doc_title", "location", "unit_title", "words")}
                             for c in batch])
        log(f"  {design}: stored {start + len(batch)}/{len(todo)} new vectors")
    return len(todo)


def save_chunks(chunks: list[dict], design: str) -> None:
    """Chunk texts as JSON Lines too: keyword search and evaluation read them without ChromaDB."""
    path = INDEX_DIR / f"chunks_{design}.jsonl"
    path.write_text("".join(json.dumps(c, ensure_ascii=False) + "\n" for c in chunks), encoding="utf-8")


# ---------------------------------------------------------------- main

def main(dry_run: bool = False) -> None:
    download_corpus()
    all_chunks = {d: [] for d in DESIGNS}
    for doc in CORPUS:
        for design in DESIGNS:
            all_chunks[design] += chunk_file(CORPUS_DIR / doc["file"], design)
    INDEX_DIR.mkdir(exist_ok=True)
    for design, chunks in all_chunks.items():
        save_chunks(chunks, design)
        words = [c["words"] for c in chunks]
        by_source = {s: sum(1 for c in chunks if c["source"] == s) for s in dict.fromkeys(c["source"] for c in chunks)}
        print(f"{design}: {len(chunks)} chunks {by_source}, words per chunk min {min(words)} "
              f"median {sorted(words)[len(words) // 2]} max {max(words)}")
    if dry_run:
        return
    # The default design first, so the server has a complete index even if the daily quota runs out.
    for design in sorted(DESIGNS, key=lambda d: d != DEFAULT_DESIGN):
        try:
            n = embed_and_store(all_chunks[design], design)
            print(f"{design}: embedded {n} new chunks, {len(all_chunks[design]) - n} already had vectors")
        except DailyQuotaExhausted as error:
            print(f"Daily embedding quota reached during '{design}'. Everything embedded so far is saved; "
                  f"run `main.py index` again after the reset (09:00 in Spain).\n  {error}")
            sys.exit(1)


if __name__ == "__main__":
    main(dry_run="--dry-run" in sys.argv)
