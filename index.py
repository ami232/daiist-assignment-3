"""
Assignment 3: build the index (`main.py index`).

Corpus: the binding text (articles and annexes) of three EU laws a product team
needs when it ships an AI feature that handles personal data:
  - GDPR, Regulation (EU) 2016/679
  - AI Act, Regulation (EU) 2024/1689
  - ePrivacy Directive 2002/58/EC, consolidated version of 19.12.2009
    (the version with the cookie-consent rule in Article 5(3))

Pipeline: download from the EU Publications Office (into corpus/, git-ignored)
-> parse into sections (one per article or annex) -> chunk with two designs
-> embed with gemini-embedding-2 -> store in ChromaDB under index/.

Vectors are saved after every API call, and only chunks without a saved
vector are embedded, so a crash or the daily quota never loses work and a
re-run costs nothing.

server.py's add_document tool imports `chunk_file` and `embed_and_store`.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"
CHROMA_DIR = INDEX_DIR / "chroma"
CONFIG_FILE = INDEX_DIR / "config.json"

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768
EMBED_BATCH = 20  # texts per request; each text counts against the daily quota

CELLAR = "http://publications.europa.eu/resource/celex/{celex}"
EURLEX = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:{celex}"

SOURCES = [
    {
        "source": "GDPR",
        "title": "Regulation (EU) 2016/679 (General Data Protection Regulation)",
        "celex": "32016R0679",
        "date": "2016-04-27",
    },
    {
        "source": "AI Act",
        "title": "Regulation (EU) 2024/1689 (Artificial Intelligence Act)",
        "celex": "32024R1689",
        "date": "2024-06-13",
    },
    {
        "source": "ePrivacy Directive",
        "title": "Directive 2002/58/EC (ePrivacy Directive), consolidated 19.12.2009",
        "celex": "02002L0058-20091219",
        "date": "2009-12-19",
    },
]

# Chunking designs. Both start from the same parsed sections.
ARTICLE_MAX_WORDS = 450   # article design: split articles longer than this at paragraph breaks
ARTICLE_TARGET_WORDS = 350
FIXED_WORDS = 400         # fixed design: sliding window of 400 words ...
FIXED_STRIDE = 300        # ... moving 300 words at a time (100 words of overlap)
FIXED_MIN_SHARE = 40      # a fixed chunk is tagged with every article it holds >= 40 words of
DESIGNS = ("article", "fixed")


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


# --------------------------------------------------------------------------- data


@dataclass
class Section:
    """One article, annex, page or heading-delimited part of a document."""

    location: str              # "Article 6", "Annex III", "page 4", "§ Scope"
    heading: str               # "Lawfulness of processing"
    paragraphs: list[str]
    chapter: str = ""


@dataclass
class Document:
    source: str                # short name used in citations: "GDPR"
    title: str
    url: str
    doc_hash: str
    sections: list[Section]
    added: bool = False        # True when it came in through add_document


@dataclass
class Chunk:
    id: str
    text: str                  # what is shown to the model
    metadata: dict = field(default_factory=dict)


def words(text: str) -> int:
    return len(text.split())


def sha(text: str | bytes, n: int = 16) -> str:
    data = text.encode("utf-8") if isinstance(text, str) else text
    return hashlib.sha256(data).hexdigest()[:n]


# --------------------------------------------------------------------- download


def download_sources() -> list[Path]:
    """Fetch the three laws from the EU Publications Office (cached in corpus/)."""
    import httpx

    CORPUS_DIR.mkdir(exist_ok=True)
    paths = []
    for spec in SOURCES:
        path = CORPUS_DIR / f"{spec['celex']}.xhtml"
        if not path.exists() or path.stat().st_size < 10_000:
            log(f"Downloading {spec['source']} ({spec['celex']}) ...")
            response = httpx.get(
                CELLAR.format(celex=spec["celex"]),
                headers={"Accept": "application/xhtml+xml", "Accept-Language": "eng"},
                follow_redirects=True,
                timeout=120,
            )
            response.raise_for_status()
            path.write_bytes(response.content)
        paths.append(path)
    return paths


# ------------------------------------------------------------------------ parse

BLOCK_TAGS = ("p", "div", "table")
MARKERS = re.compile(r"[▼►◄]\s*[A-Z]\d+|[▼►◄]")


def clean(text: str) -> str:
    text = MARKERS.sub(" ", text)
    text = text.replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text).strip()
    text = re.sub(r"\s+([,.;:)])", r"\1", text)
    text = re.sub(r"\(\s+", "(", text)
    return text


def block_texts(el, limit: int = 300) -> list[str]:
    """Split an element into paragraph-sized texts, recursing into long blocks."""
    text = clean(el.get_text(" ", strip=True))
    if not text:
        return []
    children = [c for c in el.find_all(BLOCK_TAGS, recursive=False)]
    if words(text) <= limit or not children:
        return [text]
    out = []
    for child in children:
        out.extend(block_texts(child, limit))
    return out


def parse_eu_xhtml(raw: str) -> list[Section]:
    """Articles and annexes of an act published by the EU Publications Office.

    Works for both the Official Journal layout (GDPR, AI Act) and the
    consolidated layout (ePrivacy). Recitals are deliberately left out.
    """
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(raw, "html.parser")
    # footnote references, amendment markers and the consolidated-text arrows
    for el in soup.select('a[id^="ntc"], .modref, .arrow, .oj-note-tag'):
        el.decompose()

    sections: list[Section] = []
    for el in soup.find_all(id=re.compile(r"^(art_\d+[a-z]?|anx_[IVXLC]+)$")):
        if el.find_parent(id=re.compile(r"^(art_|anx_)")):
            continue
        ident = el["id"]
        if ident.startswith("art_"):
            location = f"Article {ident[4:]}"
            title_el = el.find(id=f"{ident}.tit_1")
            heading = clean(title_el.get_text(" ", strip=True)) if title_el else ""
            skip = {id(title_el)} if title_el else set()
            body = []
            for child in el.find_all(BLOCK_TAGS, recursive=False):
                cls = " ".join(child.get("class", []))
                if id(child) in skip or "ti-art" in cls or "title-article" in cls:
                    continue
                body.extend(block_texts(child))
        else:
            location = f"Annex {ident[4:]}"
            titles = [clean(t.get_text(" ", strip=True)) for t in el.select(".oj-doc-ti, .title-annex-1, .title-annex-2")]
            heading = next((t for t in titles if not t.upper().startswith("ANNEX")), "")
            body = []
            for child in el.find_all(BLOCK_TAGS, recursive=False):
                cls = " ".join(child.get("class", []))
                if "doc-ti" in cls or "title-annex" in cls:
                    continue
                body.extend(block_texts(child))
        chapter = ""
        cpt = el.find_parent(id=re.compile(r"^cpt_[IVXLC]+$"))
        if cpt is not None:
            tit = cpt.find(id=f"{cpt['id']}.tit_1")
            num = cpt.find(class_=re.compile("ti-section-1"))
            chapter = clean(" — ".join(x.get_text(" ", strip=True) for x in (num, tit) if x is not None))
        body = [b for b in body if b and b != heading]
        if body:
            sections.append(Section(location, heading, body, chapter))
    return sections


def parse_pdf(path: Path) -> list[Section]:
    from pypdf import PdfReader

    sections = []
    for i, page in enumerate(PdfReader(str(path)).pages, start=1):
        text = page.extract_text() or ""
        text = re.sub(r"-\n(?=[a-z])", "", text)           # re-join hyphenated words
        paras = [clean(p) for p in re.split(r"\n\s*\n|(?<=[.:;])\n", text)]
        paras = [p for p in paras if words(p) > 3]
        if paras:
            sections.append(Section(f"page {i}", "", paras))
    return sections


def parse_generic_html(raw: str) -> list[Section]:
    """Any other web page: one section per h1-h3 heading."""
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(raw, "html.parser")
    for el in soup(["script", "style", "nav", "header", "footer"]):
        el.decompose()
    sections, heading, paras = [], "Introduction", []
    for el in soup.find_all(["h1", "h2", "h3", "p", "li"]):
        text = clean(el.get_text(" ", strip=True))
        if not text:
            continue
        if el.name in ("h1", "h2", "h3"):
            if paras:
                sections.append(Section(f"§ {heading}", heading, paras))
            heading, paras = text, []
        else:
            paras.append(text)
    if paras:
        sections.append(Section(f"§ {heading}", heading, paras))
    return sections


def parse_text(raw: str) -> list[Section]:
    """Plain text or Markdown: '#' headings or 'Article N' lines start a section."""
    sections, location, heading, paras = [], "§ Start", "", []
    for block in re.split(r"\n\s*\n", raw):
        block = block.strip()
        if not block:
            continue
        first = block.splitlines()[0].strip()
        art = re.match(r"^(Article|Annex|Section|Clause)\s+([\w.]+)\b(.*)$", first)
        if first.startswith("#") or art:
            if paras:
                sections.append(Section(location, heading, paras))
            if art:
                location = f"{art.group(1)} {art.group(2)}"
                rest = block.splitlines()[1:]
                heading = clean(art.group(3)) or (rest[0].strip() if rest else "")
                body = clean(" ".join(rest[1:] if not clean(art.group(3)) else rest))
            else:
                heading = first.lstrip("# ").strip()
                location = f"§ {heading}"
                body = clean(" ".join(block.splitlines()[1:]))
            paras = [body] if body else []
        else:
            paras.append(clean(block))
    if paras:
        sections.append(Section(location, heading, paras))
    return sections


def load_document(path: Path, source: str | None = None, title: str | None = None,
                  url: str = "", added: bool = False) -> Document:
    """Read any supported file into a Document with sections."""
    path = Path(path)
    data = path.read_bytes()
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        sections = parse_pdf(path)
    elif suffix in (".html", ".htm", ".xhtml", ".xml"):
        raw = data.decode("utf-8", errors="replace")
        sections = parse_eu_xhtml(raw) if re.search(r'id="art_\d+', raw) else parse_generic_html(raw)
    elif suffix in (".txt", ".md"):
        sections = parse_text(data.decode("utf-8", errors="replace"))
    else:
        raise ValueError(f"Unsupported file type {suffix!r}: use .pdf, .html, .xhtml, .txt or .md")
    if not sections:
        raise ValueError(f"No text could be extracted from {path.name}")
    name = source or re.sub(r"[_-]+", " ", path.stem).strip()
    return Document(name, title or name, url or path.name, sha(data, 32), sections, added)


def corpus_documents() -> list[Document]:
    paths = download_sources()
    docs = []
    for spec, path in zip(SOURCES, paths):
        doc = load_document(path, spec["source"], spec["title"], EURLEX.format(celex=spec["celex"]))
        docs.append(doc)
    return docs


# ------------------------------------------------------------------------ chunk


def _base_meta(doc: Document, design: str) -> dict:
    return {
        "source": doc.source,
        "title": doc.title,
        "url": doc.url,
        "doc_hash": doc.doc_hash,
        "added": doc.added,
        "design": design,
    }


def chunk_article(doc: Document) -> list[Chunk]:
    """Structure-based: one chunk per article/annex; long ones split at paragraph breaks."""
    chunks = []
    for sec in doc.sections:
        groups: list[list[str]] = []
        total = sum(words(p) for p in sec.paragraphs)
        if total <= ARTICLE_MAX_WORDS:
            groups = [sec.paragraphs]
        else:
            current: list[str] = []
            for para in sec.paragraphs:
                if current and sum(words(p) for p in current) + words(para) > ARTICLE_TARGET_WORDS:
                    groups.append(current)
                    current = []
                current.append(para)
            if current:
                groups.append(current)
        for i, group in enumerate(groups, start=1):
            part = f" (part {i} of {len(groups)})" if len(groups) > 1 else ""
            header = f"{doc.source}, {sec.location}" + (f" — {sec.heading}" if sec.heading else "") + part
            text = header + "\n" + "\n".join(group)
            meta = _base_meta(doc, "article") | {
                "location": sec.location,
                "locations": sec.location,
                "heading": sec.heading,
                "chapter": sec.chapter,
                "part": i,
                "parts": len(groups),
                "words": words(text),
            }
            chunks.append(Chunk(f"article-{sha(doc.source + sec.location + str(i) + text)}", text, meta))
    return chunks


def chunk_fixed(doc: Document) -> list[Chunk]:
    """Fixed-size: 400-word windows over the whole document, ignoring structure."""
    stream: list[tuple[str, str]] = []  # (word, location)
    for sec in doc.sections:
        for para in sec.paragraphs:
            stream.extend((w, sec.location) for w in para.split())
    chunks = []
    start = 0
    while start < len(stream):
        window = stream[start:start + FIXED_WORDS]
        counts: dict[str, int] = {}
        for _, loc in window:
            counts[loc] = counts.get(loc, 0) + 1
        tagged = [loc for loc, n in counts.items() if n >= min(FIXED_MIN_SHARE, n if len(counts) == 1 else FIXED_MIN_SHARE)]
        tagged = tagged or [window[0][1]]
        first, last = window[0][1], window[-1][1]
        location = first if first == last else f"{first} to {last}"
        text = f"{doc.source}, {location}\n" + " ".join(w for w, _ in window)
        meta = _base_meta(doc, "fixed") | {
            "location": location,
            "locations": "; ".join(tagged),
            "heading": "",
            "chapter": "",
            "part": 1,
            "parts": 1,
            "words": len(window),
        }
        chunks.append(Chunk(f"fixed-{sha(doc.source + str(start) + text)}", text, meta))
        if start + FIXED_WORDS >= len(stream):
            break
        start += FIXED_STRIDE
    return chunks


def chunk_document(doc: Document, design: str) -> list[Chunk]:
    if design == "article":
        return chunk_article(doc)
    if design == "fixed":
        return chunk_fixed(doc)
    raise ValueError(f"Unknown design {design!r}")


def chunk_file(path: str | Path, design: str | None = None, source: str | None = None) -> list[Chunk]:
    """Load one file and chunk it with the given design (default: the chosen one)."""
    doc = load_document(Path(path), source=source, added=True)
    return chunk_document(doc, design or chosen_design()["design"])


# ------------------------------------------------------------------------ embed


class QuotaExhausted(RuntimeError):
    pass


_client = None


def client():
    global _client
    if _client is None:
        from google import genai

        from api_key import load_api_key

        _client = genai.Client(api_key=load_api_key())
    return _client


def doc_prompt(chunk: Chunk) -> str:
    m = chunk.metadata
    title = f"{m['source']} {m['location']}" + (f" {m['heading']}" if m.get("heading") else "")
    return f"title: {title} | text: {chunk.text}"


def query_prompt(query: str) -> str:
    return f"task: search result | query: {query}"


def embed_texts(texts: list[str]) -> list[list[float]]:
    """One vector per text. gemini-embedding-2 needs one Content per text,
    otherwise it returns a single aggregated vector for the whole list."""
    from google.genai import errors, types

    contents = [types.Content(parts=[types.Part(text=t)]) for t in texts]
    for attempt in range(8):
        try:
            result = client().models.embed_content(
                model=EMBED_MODEL,
                contents=contents,
                config=types.EmbedContentConfig(output_dimensionality=EMBED_DIM),
            )
            vectors = [e.values for e in result.embeddings]
            if len(vectors) != len(texts):
                raise RuntimeError(f"Asked for {len(texts)} embeddings, got {len(vectors)}")
            return vectors
        except errors.ClientError as error:
            message = str(error)
            if error.code != 429:
                raise
            if "PerDay" in message or "per day" in message.lower():
                raise QuotaExhausted(message) from error
            wait = 15 * (attempt + 1)
            match = re.search(r"retry in ([\d.]+)s|'retryDelay': '(\d+)s'", message)
            if match:
                wait = float(match.group(1) or match.group(2)) + 2
            log(f"  rate limited, waiting {wait:.0f}s ...")
            time.sleep(wait)
    raise RuntimeError("Gave up after repeated rate limits")


# ------------------------------------------------------------------------ store

_chroma = None


def chroma():
    global _chroma
    if _chroma is None:
        import chromadb
        from chromadb.config import Settings

        CHROMA_DIR.mkdir(parents=True, exist_ok=True)
        _chroma = chromadb.PersistentClient(path=str(CHROMA_DIR), settings=Settings(anonymized_telemetry=False))
    return _chroma


def collection(design: str):
    return chroma().get_or_create_collection(name=design, metadata={"hnsw:space": "cosine"})


def embed_and_store(chunks: list[Chunk], design: str) -> int:
    """Embed the chunks that have no saved vector yet and store them. Returns how many were embedded."""
    col = collection(design)
    have = set(col.get(ids=[c.id for c in chunks], include=[])["ids"]) if chunks else set()
    todo = [c for c in chunks if c.id not in have]
    if not todo:
        return 0
    done = 0
    for i in range(0, len(todo), EMBED_BATCH):
        batch = todo[i:i + EMBED_BATCH]
        vectors = embed_texts([doc_prompt(c) for c in batch])
        col.add(
            ids=[c.id for c in batch],
            embeddings=vectors,
            documents=[c.text for c in batch],
            metadatas=[c.metadata for c in batch],
        )
        done += len(batch)
        log(f"  [{design}] embedded {done}/{len(todo)}")
    return done


def remove_stale(design: str, keep_ids: set[str], sources: set[str]) -> int:
    """Delete chunks of the base corpus that the current chunking no longer produces."""
    col = collection(design)
    got = col.get(include=["metadatas"])
    stale = [i for i, m in zip(got["ids"], got["metadatas"]) if m["source"] in sources and not m.get("added") and i not in keep_ids]
    if stale:
        col.delete(ids=stale)
    return len(stale)


def chosen_design() -> dict:
    """The retrieval design the server and agent use (written after comparing hit rates)."""
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text())
    return {"design": "article", "method": "hybrid", "k": 5}


# ------------------------------------------------------------------------- main


def main() -> None:
    docs = corpus_documents()
    total_words = 0
    for doc in docs:
        n = sum(words(p) for s in doc.sections for p in s.paragraphs)
        total_words += n
        log(f"{doc.source}: {len(doc.sections)} sections, {n:,} words")
    log(f"Corpus: {len(docs)} documents, {total_words:,} words")

    stats = {}
    try:
        for design in DESIGNS:
            chunks = [c for doc in docs for c in chunk_document(doc, design)]
            removed = remove_stale(design, {c.id for c in chunks}, {d.source for d in docs})
            log(f"[{design}] {len(chunks)} chunks ({removed} stale removed); embedding the missing ones ...")
            embedded = embed_and_store(chunks, design)
            stats[design] = {"chunks": len(chunks), "embedded_now": embedded}
    except QuotaExhausted:
        log("\nThe daily embedding quota is used up. Everything embedded so far is saved;\n"
            "run `main.py index` again after the reset (09:00 in Spain) to finish.")
        sys.exit(2)

    if not CONFIG_FILE.exists():
        CONFIG_FILE.write_text(json.dumps(chosen_design(), indent=2) + "\n")
    summary = {"documents": [d.source for d in docs], "words": total_words, "designs": stats}
    (INDEX_DIR / "corpus_stats.json").write_text(json.dumps(summary, indent=2) + "\n")
    print(json.dumps(summary, indent=2))


if __name__ == "__main__":
    main()
