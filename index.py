"""
Assignment 3: build the index (`main.py index`).

Pipeline, one function per step so server.py's add_document can reuse it:

    download_corpus()            fetch the 3 public documents into corpus/
    extract_blocks(path)         file -> ordered text blocks with section metadata
    chunk_blocks(blocks, design) blocks -> chunks for one chunking design
    embed_and_store(chunks, d)   embed only chunks without a saved vector
    add_document(path)           all of the above for one new file

Two chunking designs are built so evaluate.py can compare them:

    fixed      200-word windows, 40-word overlap, ignoring document structure
    structure  one chunk per section/subsection, split at paragraph boundaries
               (target <= 220 words), with the section heading attached

Each chunk carries: id, source (document id), title, section (the key used to
grade retrieval, e.g. "80b-5", "275.206(4)-2", "II.B.1"), location (human
citation, e.g. "15 U.S.C. 80b-5(b) [Advisers Act §205]"), text, words.

Storage (committed):
    index/documents.json             document registry (url, sha256, words, licence)
    index/<design>/chunks.jsonl      the chunks
    index/<design>/vectors.jsonl     {"hash", "embedding"}, appended batch by batch
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path

from settings import (
    CORPUS_DIR, DESIGNS, EMBED_BATCH, EMBED_DIMS, EMBED_MODEL, INDEX_DIR, ROOT,
    document_prefix,
)

# --------------------------------------------------------------------------
# The corpus
# --------------------------------------------------------------------------

LICENCE = "U.S. Government work, public domain (17 U.S.C. §105); no personal data"

CORPUS = [
    {
        "id": "advisers-act",
        "code": "IAA",
        "title": "Investment Advisers Act of 1940 (15 U.S.C. 80b-1 to 80b-21)",
        "url": "https://www.govinfo.gov/content/pkg/USCODE-2023-title15/html/USCODE-2023-title15-chap2D-subchapII.htm",
        "file": "advisers-act.htm",
        "date": "U.S. Code 2023 edition",
        "parser": "uscode",
    },
    {
        "id": "rules-275",
        "code": "R275",
        "title": "SEC rules under the Investment Advisers Act (17 CFR Part 275)",
        "url": "https://www.ecfr.gov/api/versioner/v1/full/2026-11-16/title-17.xml?part=275",
        "file": "rules-275.xml",
        "date": "eCFR as of 2026-11-16",
        "parser": "ecfr",
    },
    {
        "id": "fiduciary-2019",
        "code": "FID",
        "title": "SEC Interpretation Regarding Standard of Conduct for Investment Advisers (Release IA-5248, 84 FR 33669)",
        "url": "https://www.federalregister.gov/documents/full_text/html/2019/07/12/2019-12208.html",
        "file": "fiduciary-2019.html",
        "date": "2019-07-12",
        "parser": "fedreg",
    },
]

MIN_CORPUS_WORDS = 50_000
HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; daiist-assignment-3 coursework RAG indexer)"}

FIXED_WORDS, FIXED_OVERLAP = 200, 40
STRUCT_TARGET, STRUCT_MAX = 220, 320

ALLOWED_SUFFIXES = {".htm", ".html", ".xml", ".pdf", ".txt", ".md"}
MAX_FILE_MB = 20


def log(*args) -> None:
    """Log to stderr: stdout belongs to the MCP protocol when the server imports us."""
    print(*args, file=sys.stderr, flush=True)


def download_corpus() -> None:
    import httpx

    CORPUS_DIR.mkdir(exist_ok=True)
    for doc in CORPUS:
        target = CORPUS_DIR / doc["file"]
        if target.is_file() and target.stat().st_size > 1000:
            continue
        log(f"Downloading {doc['id']} from {doc['url']}")
        for attempt in range(4):
            try:
                response = httpx.get(doc["url"], headers=HEADERS, timeout=120, follow_redirects=True)
                response.raise_for_status()
                target.write_bytes(response.content)
                break
            except httpx.HTTPError as error:
                if attempt == 3:
                    raise SystemExit(
                        f"Could not download {doc['url']}: {error}\n"
                        f"Open it in a browser and save it as {target}, then run again."
                    )
                time.sleep(5 * (attempt + 1))


# --------------------------------------------------------------------------
# Extraction: file -> blocks
# --------------------------------------------------------------------------

@dataclass
class Block:
    """One paragraph (or heading line) of a document, in reading order."""
    section: str          # key used for grading retrieval, e.g. "80b-5"
    section_title: str    # e.g. "Investment advisory contracts"
    label: str            # finer location inside the section, e.g. "(b)" or "84 FR 33673"
    text: str
    is_heading: bool = False


@dataclass
class Document:
    id: str
    code: str
    title: str
    blocks: list[Block] = field(default_factory=list)
    location_style: str = "generic"   # how to print a location (see format_location)
    section_meta: dict = field(default_factory=dict)  # e.g. Advisers Act section numbers

    @property
    def words(self) -> int:
        return sum(len(b.text.split()) for b in self.blocks)


def clean(text: str) -> str:
    text = text.replace("–", "-").replace("—", "—").replace(" ", " ")
    text = text.replace("“", '"').replace("”", '"').replace("’", "'").replace("‘", "'")
    return re.sub(r"\s+", " ", text).strip()


def parse_uscode(html: str) -> tuple[list[Block], dict]:
    """govinfo U.S. Code HTML. Keeps statutory text; drops editorial/statutory notes.

    Extraction problem fixed: about 40% of the page (11,000 words) is amendment
    history and editorial notes ("1996—Pub. L. 104–290 substituted ...") that are
    not the law itself. They sit after an <h4 class="note-head"> until the next
    section heading, so we skip that span. Footnote markers (<sup>) are removed
    because they glued numbers into the text ("section 79z–4 1 of this title").
    """
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")
    for sup in soup.find_all("sup"):
        sup.decompose()

    blocks: list[Block] = []
    act_sections: dict[str, str] = {}
    section, title, label, in_notes = "", "", "", False
    for el in soup.find_all(["h3", "h4", "p"]):
        classes = " ".join(el.get("class") or [])
        text = clean(el.get_text(" "))
        if el.name == "h3" and "section-head" in classes:
            match = re.match(r"§+\s*([0-9a-z\-–]+(?:\s+to\s+[0-9a-z\-–]+)?)\.\s*(.*)", text)
            if not match:
                continue
            section, title, label, in_notes = match.group(1).replace("–", "-"), match.group(2), "", False
            continue
        if not section:
            continue
        if el.name == "h4" and "note-head" in classes:
            in_notes = True
        if in_notes or not text:
            continue
        if el.name == "p" and "source-credit" in classes:
            found = re.search(r"title II, §\s*(\d+[A-Z]?(?:\([a-z]\))?)", text)
            if found and section not in act_sections:
                act_sections[section] = found.group(1)
            continue
        if el.name == "p" and ("footnote" in classes or "statutory-body" not in classes):
            continue
        if el.name == "h4" and "subsection-head" in classes:
            sub = re.match(r"\(([a-z]{1,2})\)", text)
            label = f"({sub.group(1)})" if sub else label
        if el.name == "p" and not label:
            sub = re.match(r"\(([a-z])\)", text)
            label = f"({sub.group(1)})" if sub else ""
        blocks.append(Block(section, title, label, text, is_heading=(el.name == "h4")))
    return blocks, {"act_sections": act_sections}


def _xml_text(el: ET.Element) -> str:
    return clean("".join(el.itertext()))


def parse_ecfr(xml: bytes) -> list[Block]:
    """eCFR XML. One section = one <DIV8>. Keeps paragraphs and tables; drops
    the source citations (<CITA>) and authority lines, which are only
    Federal Register page references."""
    root = ET.fromstring(xml)
    blocks: list[Block] = []
    for div in root.iter("DIV8"):
        key = (div.get("N") or "").strip()
        head = div.find("HEAD")
        heading = _xml_text(head) if head is not None else key
        title = re.sub(r"^§+\s*[\w.()\-–]+\s*", "", heading).strip() or heading
        if "[Reserved]" in heading:
            continue
        top = None  # current top-level paragraph letter, e.g. "a"
        for child in div:
            if child.tag in {"HEAD", "CITA", "SECAUTH", "AUTH", "EDNOTE"}:
                continue
            if child.tag in {"GPOTABLE", "TABLE"} or child.find(".//TR") is not None or child.find(".//ROW") is not None:
                rows = [" | ".join(_xml_text(c) for c in tr if _xml_text(c))
                        for tr in list(child.iter("TR")) + list(child.iter("ROW"))]
                text = clean(" ; ".join(r for r in rows if r)) or _xml_text(child)
            else:
                text = _xml_text(child)
            if not text:
                continue
            match = re.match(r"\(([a-z])\)", text)
            if match:
                letter = match.group(1)
                expected = "a" if top is None else chr(ord(top) + 1)
                if letter == expected:   # "(i)" after "(h)" is a paragraph; after "(a)" it is a sub-item
                    top = letter
            label = f"({top})" if top else ""
            blocks.append(Block(key, title, label, text))
    return blocks


def _roman_letter_number(heading: str) -> str | None:
    match = re.match(r"^([IVX]+|[A-Z]|\d+)\.\s", heading)
    return match.group(1) if match else None


def parse_fedreg(html: str) -> list[Block]:
    """federalregister.gov full-text HTML of a release.

    Keeps the body from "I. Introduction" up to "List of Subjects" (the CFR
    amendment and signature after that add nothing). Footnote markers and the
    footnote list are removed. Section keys follow the outline: "II", "II.B",
    "II.B.1"; unnumbered sub-headings stay inside the numbered section. Each
    paragraph records its printed Federal Register page.
    """
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")
    for el in soup.select("sup, div.footnotes, .printed-page-details, .printed-page-inline, .footnote"):
        el.decompose()

    blocks: list[Block] = []
    parts = {"h2": None, "h3": None, "h4": None}
    titles = {"h2": "", "h3": "", "h4": ""}
    started = False
    volume = 84
    for el in soup.find_all(["h1", "h2", "h3", "h4", "p"]):
        text = clean(el.get_text(" "))
        if not text:
            continue
        if el.name in {"h1", "h2"} and text.startswith("List of Subjects"):
            break
        if el.name == "h2" and re.match(r"^I\.\s", text):
            started = True
        if not started:
            continue
        if el.name in parts:
            number = _roman_letter_number(text)
            if number is None:            # unnumbered sub-heading: keep current section
                blocks.append(Block(_fr_key(parts), _fr_title(titles), "", text, is_heading=True))
                continue
            parts[el.name], titles[el.name] = number, re.sub(r"^\S+\.\s*", "", text)
            if el.name == "h2":
                parts["h3"] = parts["h4"] = None
                titles["h3"] = titles["h4"] = ""
            if el.name == "h3":
                parts["h4"], titles["h4"] = None, ""
            blocks.append(Block(_fr_key(parts), _fr_title(titles), "", text, is_heading=True))
            continue
        if el.name == "p":
            page = el.get("data-page")
            label = f"{volume} FR {page}" if page else ""
            blocks.append(Block(_fr_key(parts), _fr_title(titles), label, text))
    return blocks


def _fr_key(parts: dict) -> str:
    return ".".join(p for p in (parts["h2"], parts["h3"], parts["h4"]) if p) or "front"


def _fr_title(titles: dict) -> str:
    return " — ".join(t for t in (titles["h2"], titles["h3"], titles["h4"]) if t)


def parse_generic_html(html: str) -> list[Block]:
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")
    for el in soup(["script", "style", "nav", "footer", "sup"]):
        el.decompose()
    blocks, section = [], "front"
    for el in soup.find_all(["h1", "h2", "h3", "h4", "p", "li"]):
        text = clean(el.get_text(" "))
        if not text:
            continue
        if el.name.startswith("h"):
            section = text[:80]
            blocks.append(Block(section, section, "", text, is_heading=True))
        else:
            blocks.append(Block(section, section, "", text))
    return blocks


def parse_pdf(path: Path) -> list[Block]:
    from pypdf import PdfReader

    blocks = []
    for number, page in enumerate(PdfReader(str(path)).pages, start=1):
        text = page.extract_text() or ""
        text = re.sub(r"-\n(\w)", r"\1", text)          # re-join hyphenated line breaks
        for para in re.split(r"\n\s*\n", text):
            para = clean(para)
            if para:
                blocks.append(Block(f"p{number}", f"page {number}", f"page {number}", para))
    return blocks


def parse_text(text: str) -> list[Block]:
    blocks, section = [], "front"
    for para in re.split(r"\n\s*\n", text):
        para = para.strip()
        if not para:
            continue
        if para.startswith("#"):
            section = clean(para.lstrip("#"))[:80]
            blocks.append(Block(section, section, "", section, is_heading=True))
        else:
            blocks.append(Block(section, section, "", clean(para)))
    return blocks


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", name.lower()).strip("-") or "document"


def extract_document(path: Path, meta: dict | None = None) -> Document:
    """Read any supported file into a Document of ordered blocks."""
    meta = dict(meta or {})
    suffix = path.suffix.lower()
    doc_id = meta.get("id") or slugify(path.stem)
    code = meta.get("code") or slugify(path.stem).upper().replace("-", "")[:8]
    raw = path.read_bytes()
    parser = meta.get("parser")
    section_meta: dict = {}

    if parser is None:  # added documents: sniff the format
        head = raw[:200_000].decode("utf-8", errors="ignore")
        if suffix == ".xml" and "<DIV8" in head:
            parser = "ecfr"
        elif suffix in {".htm", ".html"} and "statutory-body" in head:
            parser = "uscode"
        elif suffix in {".htm", ".html"} and "data-page=" in head:
            parser = "fedreg"
        elif suffix in {".htm", ".html", ".xml"}:
            parser = "html"
        elif suffix == ".pdf":
            parser = "pdf"
        else:
            parser = "text"

    if parser == "uscode":
        blocks, section_meta = parse_uscode(raw.decode("utf-8", errors="replace"))
    elif parser == "ecfr":
        blocks = parse_ecfr(raw)
    elif parser == "fedreg":
        blocks = parse_fedreg(raw.decode("utf-8", errors="replace"))
    elif parser == "html":
        blocks = parse_generic_html(raw.decode("utf-8", errors="replace"))
    elif parser == "pdf":
        blocks = parse_pdf(path)
    else:
        blocks = parse_text(raw.decode("utf-8", errors="replace"))

    title = meta.get("title")
    if not title and parser == "ecfr":
        root = ET.fromstring(raw)
        head = next(root.iter("HEAD"), None)
        title = _xml_text(head) if head is not None else path.stem
    return Document(doc_id, code, title or path.stem, blocks, parser, section_meta)


def format_location(doc: Document, section: str, labels: list[str]) -> str:
    labels = [l for l in dict.fromkeys(labels) if l]
    if doc.location_style == "uscode":
        sub = labels[0] + (f"-{labels[-1]}" if len(labels) > 1 else "") if labels else ""
        act = doc.section_meta.get("act_sections", {}).get(section)
        return f"15 U.S.C. {section}{sub}" + (f" [Advisers Act §{act}]" if act else "")
    if doc.location_style == "ecfr":
        sub = labels[0] + (f"-{labels[-1]}" if len(labels) > 1 else "") if labels else ""
        return f"17 CFR {section}{sub}"
    if doc.location_style == "fedreg":
        pages = sorted({l for l in labels if "FR" in l})
        page = pages[0] + (f"-{pages[-1].split()[-1]}" if len(pages) > 1 else "") if pages else ""
        return f"Part {section}" + (f" ({page})" if page else "")
    return section + (f" ({labels[0]})" if labels else "")


# --------------------------------------------------------------------------
# Chunking: blocks -> chunks
# --------------------------------------------------------------------------

def _hash(text: str) -> str:
    return hashlib.sha256(f"{EMBED_MODEL}|{EMBED_DIMS}|{text}".encode()).hexdigest()[:24]


def _make_chunk(doc: Document, cid: str, section: str, sections: list[str], title: str,
                labels: list[str], text: str) -> dict:
    location = format_location(doc, section, labels)
    embed_text = document_prefix(f"{doc.title} — {location} — {title}") + text
    return {
        "id": cid,
        "source": doc.id,
        "title": doc.title,
        "section": section,
        "sections": sections,
        "section_title": title,
        "location": location,
        "text": text,
        "words": len(text.split()),
        "hash": _hash(embed_text),
        "embed_text": embed_text,
    }


def _split_long(text: str, limit: int) -> list[str]:
    """Split an over-long paragraph at sentence ends into pieces <= limit words."""
    sentences = re.split(r"(?<=[.;:])\s+(?=[A-Z(])", text)
    pieces, current = [], []
    for sentence in sentences:
        if current and len(" ".join(current + [sentence]).split()) > limit:
            pieces.append(" ".join(current))
            current = []
        current.append(sentence)
    if current:
        pieces.append(" ".join(current))
    # a single sentence can still be too long (definitions lists): hard-split by words
    out = []
    for piece in pieces:
        words = piece.split()
        out.extend(" ".join(words[i:i + limit]) for i in range(0, len(words), limit))
    return out


def chunk_structure(doc: Document) -> list[dict]:
    """One chunk per section, split at paragraph boundaries near STRUCT_TARGET words.

    The section heading is repeated at the top of every piece, so a chunk that
    starts mid-section still says which rule or statute section it belongs to.
    """
    chunks: list[dict] = []
    by_section: dict[str, list[Block]] = {}
    for block in doc.blocks:
        by_section.setdefault(block.section, []).append(block)

    for section, blocks in by_section.items():
        title = blocks[0].section_title
        units: list[tuple[str, str]] = []
        for block in blocks:
            if len(block.text.split()) > STRUCT_MAX:
                units.extend((block.label, piece) for piece in _split_long(block.text, STRUCT_TARGET))
            else:
                units.append((block.label, block.text))

        groups, current, size = [], [], 0
        for label, text in units:
            n = len(text.split())
            if current and size + n > STRUCT_TARGET:
                groups.append(current)
                current, size = [], 0
            current.append((label, text))
            size += n
        if current:
            # merge a tiny tail into the previous group if it still fits under the max
            if groups and size < 60 and sum(len(t.split()) for _, t in groups[-1]) + size <= STRUCT_MAX:
                groups[-1].extend(current)
            else:
                groups.append(current)

        for n, group in enumerate(groups, start=1):
            header = f"{format_location(doc, section, [])} — {title}"
            text = header + "\n" + "\n".join(t for _, t in group)
            safe = re.sub(r"[\s\[\]]+", "-", section)[:40]   # ids must have no spaces: they are cited as [ID]
            chunks.append(_make_chunk(doc, f"{doc.code}:{safe}#{n}", section, [section], title,
                                      [l for l, _ in group], text))
    return chunks


def chunk_fixed(doc: Document) -> list[dict]:
    """Baseline: 200-word windows with 40 words of overlap across the whole document."""
    words: list[tuple[str, str, str, str]] = []   # (word, section, title, label)
    for block in doc.blocks:
        for word in block.text.split():
            words.append((word, block.section, block.section_title, block.label))
    chunks, step = [], FIXED_WORDS - FIXED_OVERLAP
    for n, start in enumerate(range(0, max(len(words) - FIXED_OVERLAP, 1), step), start=1):
        window = words[start:start + FIXED_WORDS]
        if not window:
            break
        sections = list(dict.fromkeys(w[1] for w in window))
        first = window[0]
        labels = [w[3] for w in window if w[1] == first[1]]
        text = " ".join(w[0] for w in window)
        chunk = _make_chunk(doc, f"{doc.code}:w{n}", first[1], sections, first[2], labels, text)
        if len(sections) > 1:
            chunk["location"] += f" … {format_location(doc, sections[-1], [])}"
        chunks.append(chunk)
    return chunks


def chunk_blocks(doc: Document, design: str) -> list[dict]:
    return chunk_structure(doc) if design == "structure" else chunk_fixed(doc)


# --------------------------------------------------------------------------
# Embedding and storage
# --------------------------------------------------------------------------

class QuotaExhausted(RuntimeError):
    """The free tier's daily embedding quota is used up. Saved vectors are kept."""


def _client():
    from google import genai
    from api_key import load_api_key

    return genai.Client(api_key=load_api_key())


def embed_texts(texts: list[str], client=None) -> list[list[float]]:
    """Embed texts with gemini-embedding-2, one vector per text.

    Each text is wrapped in its own Content: with gemini-embedding-2 a bare
    list of strings is merged into ONE embedding.
    """
    from google.genai import types, errors

    client = client or _client()
    contents = [types.Content(parts=[types.Part.from_text(text=t)]) for t in texts]
    for attempt in range(6):
        try:
            result = client.models.embed_content(
                model=EMBED_MODEL,
                contents=contents,
                config=types.EmbedContentConfig(output_dimensionality=EMBED_DIMS),
            )
            vectors = [list(e.values) for e in result.embeddings]
            if len(vectors) != len(texts):
                raise RuntimeError(f"asked for {len(texts)} embeddings, got {len(vectors)}")
            return vectors
        except errors.ClientError as error:
            message = str(error)
            if getattr(error, "code", None) == 429:
                if "PerDay" in message or "per day" in message.lower():
                    raise QuotaExhausted(message) from error
                wait = 20 * (attempt + 1)
                found = re.search(r"retry in ([\d.]+)s", message) or re.search(r"'retryDelay': '(\d+)s'", message)
                if found:
                    wait = float(found.group(1)) + 2
                log(f"  rate limited, waiting {wait:.0f}s")
                time.sleep(wait)
                continue
            raise
        except errors.ServerError:
            time.sleep(10 * (attempt + 1))
    raise QuotaExhausted("embedding kept failing after 6 attempts; saved vectors are kept, run again later")


def design_dir(design: str) -> Path:
    path = INDEX_DIR / design
    path.mkdir(parents=True, exist_ok=True)
    return path


def saved_hashes(design: str) -> set[str]:
    path = design_dir(design) / "vectors.jsonl"
    if not path.is_file():
        return set()
    hashes = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        if line.strip():
            try:
                hashes.add(json.loads(line)["hash"])
            except (json.JSONDecodeError, KeyError):
                continue   # a line cut short by a crash; that chunk is embedded again
    return hashes


def embed_and_store(chunks: list[dict], design: str, client=None) -> int:
    """Embed chunks that have no saved vector; append each batch to disk at once."""
    have = saved_hashes(design)
    todo, seen = [], set()
    for chunk in chunks:
        if chunk["hash"] not in have and chunk["hash"] not in seen:
            todo.append(chunk)
            seen.add(chunk["hash"])
    if not todo:
        return 0
    client = client or _client()
    path = design_dir(design) / "vectors.jsonl"
    done = 0
    with path.open("a", encoding="utf-8") as out:
        for start in range(0, len(todo), EMBED_BATCH):
            batch = todo[start:start + EMBED_BATCH]
            vectors = embed_texts([c["embed_text"] for c in batch], client)
            for chunk, vector in zip(batch, vectors):
                out.write(json.dumps({"hash": chunk["hash"], "embedding": [round(x, 6) for x in vector]}) + "\n")
            out.flush()
            done += len(batch)
            log(f"  [{design}] embedded {done}/{len(todo)}")
    return done


def write_chunks(design: str, chunks: list[dict]) -> None:
    path = design_dir(design) / "chunks.jsonl"
    tmp = path.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as out:
        for chunk in chunks:
            out.write(json.dumps({k: v for k, v in chunk.items() if k != "embed_text"}, ensure_ascii=False) + "\n")
    tmp.replace(path)


def read_chunks(design: str) -> list[dict]:
    path = design_dir(design) / "chunks.jsonl"
    if not path.is_file():
        return []
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def registry_path() -> Path:
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    return INDEX_DIR / "documents.json"


def read_registry() -> dict:
    path = registry_path()
    return json.loads(path.read_text(encoding="utf-8")) if path.is_file() else {}


def write_registry(registry: dict) -> None:
    registry_path().write_text(json.dumps(registry, indent=2, ensure_ascii=False), encoding="utf-8")


def sha256_file(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# --------------------------------------------------------------------------
# Stage entry points
# --------------------------------------------------------------------------

def build_index() -> None:
    download_corpus()
    registry = read_registry()
    documents: list[Document] = []
    for meta in CORPUS:
        path = CORPUS_DIR / meta["file"]
        doc = extract_document(path, meta)
        documents.append(doc)
        registry[doc.id] = {
            "title": doc.title, "code": doc.code, "url": meta["url"], "date": meta["date"],
            "path": str(path.relative_to(ROOT)), "sha256": sha256_file(path), "words": doc.words,
            "licence": LICENCE, "origin": "corpus",
        }
        log(f"{doc.id}: {len(doc.blocks)} blocks, {doc.words:,} words")

    # documents added later through add_document stay in the index when it is rebuilt
    for doc_id, entry in registry.items():
        if entry.get("origin") == "added" and (ROOT / entry["path"]).is_file():
            documents.append(extract_document(ROOT / entry["path"], {"id": doc_id, "code": entry["code"], "title": entry["title"]}))

    total = sum(registry[d["id"]]["words"] for d in CORPUS)
    log(f"Corpus: {len(CORPUS)} documents, {total:,} words")
    if total < MIN_CORPUS_WORDS:
        log(f"WARNING: corpus has fewer than {MIN_CORPUS_WORDS:,} words")
    write_registry(registry)

    client = None
    for design in DESIGNS:
        chunks = [c for doc in documents for c in chunk_blocks(doc, design)]
        ids = [c["id"] for c in chunks]
        if len(ids) != len(set(ids)):
            raise SystemExit(f"duplicate chunk ids in design {design}")
        write_chunks(design, chunks)
        words = sum(c["words"] for c in chunks) / max(len(chunks), 1)
        log(f"[{design}] {len(chunks)} chunks, {words:.0f} words on average")
        try:
            if client is None and any(c["hash"] not in saved_hashes(design) for c in chunks):
                client = _client()
            new = embed_and_store(chunks, design, client)
            log(f"[{design}] {new} new embeddings, {len(chunks) - new} reused")
        except QuotaExhausted as error:
            log(f"[{design}] daily embedding quota reached: {error}\n"
                "Vectors so far are saved. Run `uv run python main.py index` again after 09:00 (Spain).")
            raise SystemExit(2)
    log("Index ready.")


def add_document(path: str | Path) -> dict:
    """Index one new file (the add-document tool calls this).

    Already indexed?  Same content (sha256) -> nothing changes, the existing
    entry is reported. Same document id but different content -> the new
    version replaces the old one (its old chunks are removed), because a
    regulation that was amended must not be answered from both versions.
    """
    path = Path(path).expanduser()
    if not path.is_absolute():
        path = (ROOT / path).resolve()
    if not path.is_file():
        return {"status": "error", "message": f"No file at {path}"}
    if path.suffix.lower() not in ALLOWED_SUFFIXES:
        return {"status": "error", "message": f"Unsupported file type {path.suffix}; use one of {sorted(ALLOWED_SUFFIXES)}"}
    if path.stat().st_size > MAX_FILE_MB * 1e6:
        return {"status": "error", "message": f"File is larger than {MAX_FILE_MB} MB"}

    registry = read_registry()
    digest = sha256_file(path)
    for doc_id, entry in registry.items():
        if entry.get("sha256") == digest:
            return {"status": "already_indexed", "document": doc_id, "title": entry["title"],
                    "message": f"This exact file is already indexed as '{doc_id}'. Nothing was changed."}

    doc = extract_document(path)
    if not doc.blocks:
        return {"status": "error", "message": "No text could be extracted from this file."}
    replaced = doc.id in registry
    if replaced and registry[doc.id].get("origin") == "corpus":
        return {"status": "error", "message": f"'{doc.id}' is a core corpus document; rebuild with main.py index instead."}
    used_codes = {e.get("code") for i, e in registry.items() if i != doc.id}
    while doc.code in used_codes:
        doc.code += "X"

    try:
        rel = str(path.relative_to(ROOT))
    except ValueError:
        rel = str(path)
    total_chunks = {}
    for design in DESIGNS:
        kept = [c for c in read_chunks(design) if c["source"] != doc.id]
        new_chunks = chunk_blocks(doc, design)
        embed_and_store(new_chunks, design)   # may raise QuotaExhausted: nothing is written then
        write_chunks(design, kept + new_chunks)
        total_chunks[design] = len(new_chunks)
    registry[doc.id] = {
        "title": doc.title, "code": doc.code, "url": None, "date": time.strftime("%Y-%m-%d"),
        "path": rel, "sha256": digest, "words": doc.words, "licence": "added by user", "origin": "added",
    }
    write_registry(registry)
    return {"status": "replaced" if replaced else "added", "document": doc.id, "title": doc.title,
            "words": doc.words, "chunks": total_chunks,
            "message": f"{'Replaced' if replaced else 'Added'} '{doc.title}' ({doc.words} words, "
                       f"{total_chunks.get('structure', 0)} chunks in the structure design)."}


if __name__ == "__main__":
    build_index()
