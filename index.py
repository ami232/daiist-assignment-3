"""
Assignment 3: build the index (`main.py index`).

Corpus: three EU banking texts in their current consolidated English versions,
downloaded from the EU Publications Office (Cellar) into corpus/:

    CRR       Regulation (EU) No 575/2013   (without Part Three Titles II-VI, Part Ten, annexes)
    CRD       Directive 2013/36/EU
    MiFID II  Directive 2014/65/EU

Pipeline, per file:  parse_file(path) -> articles -> chunk_articles(...) -> chunks
                     embed_and_store(chunks, design)

Two chunking designs are indexed, one ChromaDB collection each, so that
evaluate.py can compare them:

    fixed       300-word windows with 50-word overlap over the running text,
                ignoring structure (baseline);
    structural  one chunk per article, split at paragraph boundaries when it
                exceeds ~400 words, each prefixed with "Doc > Part > Article N: title".

Every vector is saved as soon as the API returns it, and only chunks without a
saved vector (same id and same text hash) are embedded, so the free-tier daily
limit or a crash loses nothing: run it again tomorrow and it carries on.
"""

from __future__ import annotations

import hashlib
import os
import re
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

import truststore

truststore.inject_into_ssl()  # use the OS certificate store (antivirus HTTPS scanning)
os.environ.setdefault("ANONYMIZED_TELEMETRY", "False")  # ChromaDB: no telemetry, nothing on stdout

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"
CHROMA_DIR = INDEX_DIR / "chroma"

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768          # smaller vectors keep index/ well under 90 MB
EMBED_BATCH = 50

DESIGNS = ("structural", "fixed")
FIXED_WORDS, FIXED_OVERLAP = 300, 50
STRUCT_MAX_WORDS = 400

CELLAR = "http://publications.europa.eu/resource/celex/{celex}"


@dataclass(frozen=True)
class Source:
    short: str           # what chunk metadata and eval/questions.csv call it
    celex: str
    title: str
    exclude_parts: tuple[str, ...] = ()
    include_annexes: bool = False

    @property
    def path(self) -> Path:
        return CORPUS_DIR / f"{self.celex}.xhtml"

    @property
    def url(self) -> str:
        return f"https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:{self.celex}"


SOURCES = [
    Source("CRR", "02013R0575-20260626",
           "Regulation (EU) No 575/2013 on prudential requirements for credit institutions (CRR), consolidated 26.6.2026",
           # Part Three Title I (Art. 92 own funds ratios) stays; the RWA calculation titles go
           exclude_parts=tuple(f"PART THREE/TITLE {t}" for t in ("II", "III", "IV", "V", "VI")) + ("PART TEN",)),
    Source("CRD", "02013L0036-20260711",
           "Directive 2013/36/EU on access to the activity of credit institutions and prudential supervision (CRD), consolidated 11.7.2026"),
    Source("MiFID II", "02014L0065-20260606",
           "Directive 2014/65/EU on markets in financial instruments (MiFID II), consolidated 6.6.2026"),
]


# --------------------------------------------------------------------------- download

def download(source: Source) -> Path:
    """Fetch the consolidated XHTML from Cellar (eur-lex.europa.eu blocks scripts)."""
    import httpx

    if source.path.exists() and source.path.stat().st_size > 100_000:
        return source.path
    CORPUS_DIR.mkdir(exist_ok=True)
    log(f"Downloading {source.short} ({source.celex}) ...")
    response = httpx.get(
        CELLAR.format(celex=source.celex),
        headers={"Accept": "application/xhtml+xml", "Accept-Language": "eng"},
        follow_redirects=True, timeout=120,
    )
    response.raise_for_status()
    source.path.write_bytes(response.content)
    return source.path


# --------------------------------------------------------------------------- parse and clean

MARKERS = re.compile(r"[▼►◄]\s*(?:[A-Z]\d*)?|(?<=\s)◄")


def clean(text: str) -> str:
    """Remove consolidation markers (▼M8, ►C2 … ◄), footnote calls and odd spacing."""
    text = MARKERS.sub(" ", text.replace("\xa0", " "))
    text = re.sub(r"\s+([,.;:)])", r"\1", text)
    text = re.sub(r"\(\s+", "(", text)
    return re.sub(r"\s+", " ", text).strip()


@dataclass
class Paragraph:
    number: str | None   # "1", "2a" … or None for unnumbered text
    text: str


@dataclass
class Article:
    source: str
    number: str          # "395", "92a"
    heading: str
    part: str = ""
    title: str = ""
    chapter: str = ""
    section: str = ""
    paragraphs: list[Paragraph] = field(default_factory=list)

    @property
    def label(self) -> str:
        return f"Article {self.number}"

    @property
    def path_label(self) -> str:
        bits = [self.source] + [b for b in (self.part, self.title, self.chapter) if b]
        return " > ".join(bits + [f"{self.label}: {self.heading}".rstrip(": ")])

    @property
    def text(self) -> str:
        return " ".join(p.text for p in self.paragraphs)


def _division_text(p) -> str:
    return clean(p.get_text(" ", strip=True))


def parse_eurlex(path: Path, source: str, exclude_parts=(), include_annexes=False) -> list[Article]:
    """Articles of a EUR-Lex consolidated XHTML, with Part/Title/Chapter/Section context."""
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    for junk in soup.select("p.modref, p.arrow, p.footnote, p.hd-modifiers, p.reference, .toc-1, .toc-2"):
        junk.decompose()
    for sup in soup.select("span.superscript a, a.footnote, span.footnote"):
        sup.decompose()

    context = {"PART": "", "TITLE": "", "CHAPTER": "", "Section": ""}
    articles: list[Article] = []
    for el in soup.find_all(["p", "div"]):
        classes = el.get("class", [])
        if el.name == "p" and "title-division-1" in classes:
            label = _division_text(el)
            name_el = el.find_next_sibling("p", class_="title-division-2")
            name = _division_text(name_el) if name_el else ""
            level = label.split(" ")[0]
            if level == "PART":
                context["_part_key"], context["_title_key"] = label, ""
            elif level == "TITLE":
                context["_title_key"] = label
            if level in context:
                head, _, rest = label.partition(" ")
                label = f"{head.capitalize()} {rest.upper() if re.fullmatch(r'[IVXLC]+', rest) else rest.capitalize()}"
                full = f"{label} ({name.capitalize()})" if name else label
                context[level] = full
                # a new level resets the lower ones
                order = ["PART", "TITLE", "CHAPTER", "Section"]
                for lower in order[order.index(level) + 1:]:
                    context[lower] = ""
        elif el.name == "p" and "title-annex-1" in classes:
            context["_part_key"] = "ANNEX"
        elif el.name == "div" and "eli-subdivision" in classes and el.get("id", "").startswith("art_"):
            part_key = context.get("_part_key", "")
            if part_key in exclude_parts or f"{part_key}/{context.get('_title_key', '')}" in exclude_parts:
                continue
            if context.get("_part_key") == "ANNEX" and not include_annexes:
                continue
            article = _parse_article(el, source, context)
            if article and article.text and not re.fullmatch(r"(?i)\W*deleted\W*", article.text):
                articles.append(article)
    return articles


def _parse_article(div, source: str, context: dict) -> Article | None:
    number_el = div.find("p", class_="title-article-norm")
    if number_el is None:
        return None
    match = re.search(r"Article\s+(\d+\s*[a-z]*)", _division_text(number_el))
    if not match:
        return None
    heading_el = div.find("p", class_="stitle-article-norm")
    article = Article(
        source=source,
        number=match.group(1).replace(" ", ""),
        heading=_division_text(heading_el) if heading_el else "",
        part=context["PART"], title=context["TITLE"], chapter=context["CHAPTER"], section=context["Section"],
    )
    current: Paragraph | None = None
    for child in div.find_all(recursive=False):
        classes = child.get("class", [])
        if "title-article-norm" in classes or "eli-title" in classes:
            continue
        number_span = child.find("span", class_="no-parag", recursive=False) if child.name == "div" else None
        text = clean(child.get_text(" ", strip=True))
        if not text:
            continue
        if number_span is not None:
            number = clean(number_span.get_text()).rstrip(".")
            current = Paragraph(number, text)
            article.paragraphs.append(current)
        elif current is not None:
            current.text += " " + text
        else:
            current = Paragraph(None, text)
            article.paragraphs.append(current)
    return article


def parse_plain(path: Path, source: str) -> list[Article]:
    """Fallback for PDFs and text files: one pseudo-article per page (PDF) or per blank-line block."""
    if path.suffix.lower() == ".pdf":
        from pypdf import PdfReader

        pages = [clean(page.extract_text() or "") for page in PdfReader(str(path)).pages]
        return [Article(source, f"p{i}", f"page {i}", paragraphs=[Paragraph(None, t)])
                for i, t in enumerate(pages, 1) if t]
    blocks = [clean(b) for b in re.split(r"\n\s*\n", path.read_text(encoding="utf-8", errors="replace"))]
    return [Article(source, f"b{i}", f"block {i}", paragraphs=[Paragraph(None, b)])
            for i, b in enumerate(blocks, 1) if b]


def parse_file(path: str | Path, source: str | None = None) -> list[Article]:
    """Articles of one file. EUR-Lex (X)HTML keeps its structure; PDF/text fall back to pages/blocks."""
    path = Path(path)
    known = next((s for s in SOURCES if s.path.resolve() == path.resolve()), None)
    if known:
        return parse_eurlex(path, known.short, known.exclude_parts, known.include_annexes)
    if path.suffix.lower() in (".xhtml", ".html", ".htm"):
        if source is None:  # an extract can name its act: <meta name="corpus-source" content="CRR"/>
            m = re.search(r'<meta name="corpus-source" content="([^"]+)"', path.read_text(encoding="utf-8")[:2000])
            source = m.group(1) if m else path.stem
        return parse_eurlex(path, source)
    source = source or path.stem
    return parse_plain(path, source)


# --------------------------------------------------------------------------- chunk

def _words(text: str) -> list[str]:
    return text.split()


def _split_long(text: str, limit: int) -> list[str]:
    """Split one over-long paragraph at sentence / list-item boundaries into pieces <= limit words."""
    pieces = re.split(r"(?<=[.;:])\s+(?=(?:\([a-z0-9]+\)\s)|[A-Z])", text)
    out, buf = [], []
    for piece in pieces:
        if buf and len(_words(" ".join(buf + [piece]))) > limit:
            out.append(" ".join(buf))
            buf = []
        buf.append(piece)
    if buf:
        out.append(" ".join(buf))
    # a single sentence above the limit is cut hard
    final = []
    for piece in out:
        words = _words(piece)
        final += [" ".join(words[i:i + limit]) for i in range(0, len(words), limit)]
    return final


def _base_metadata(article: Article) -> dict:
    return {
        "source": article.source,
        "part": article.part, "title": article.title, "chapter": article.chapter,
        "article": article.label, "article_title": article.heading,
    }


def chunk_structural(articles: list[Article], max_words: int = STRUCT_MAX_WORDS) -> list[dict]:
    """One chunk per article; long articles split at paragraph boundaries; header prefixed."""
    chunks = []
    for article in articles:
        units: list[tuple[str | None, str]] = []
        for p in article.paragraphs:
            if len(_words(p.text)) > max_words:
                units += [(p.number, t) for t in _split_long(p.text, max_words)]
            else:
                units.append((p.number, p.text))
        groups: list[list[tuple[str | None, str]]] = [[]]
        for unit in units:
            size = sum(len(_words(t)) for _, t in groups[-1])
            if groups[-1] and size + len(_words(unit[1])) > max_words:
                groups.append([])
            groups[-1].append(unit)
        for i, group in enumerate(groups):
            numbers = [n for n, _ in group if n]
            paras = ""
            if numbers and len(groups) > 1:
                paras = f"({numbers[0]})" if numbers[0] == numbers[-1] else f"({numbers[0]})-({numbers[-1]})"
            location = f"{article.label}{paras}"
            header = article.path_label + (f" [{location}]" if paras else "")
            body = " ".join(t for _, t in group)
            chunks.append({
                "id": f"{article.source}|{article.label}|{i}",
                "text": f"{header}\n{body}",
                "metadata": {**_base_metadata(article), "location": location,
                             "articles": article.label, "paragraphs": paras},
            })
    return chunks


def chunk_fixed(articles: list[Article], size: int = FIXED_WORDS, overlap: int = FIXED_OVERLAP) -> list[dict]:
    """Sliding word windows over the running text of each source, structure ignored (baseline)."""
    chunks = []
    by_source: dict[str, list[Article]] = {}
    for a in articles:
        by_source.setdefault(a.source, []).append(a)
    for source, arts in by_source.items():
        words, owner = [], []
        for k, a in enumerate(arts):
            running = f"{a.label} {a.heading} {a.text}"
            w = _words(running)
            words += w
            owner += [k] * len(w)
        step = size - overlap
        for n, start in enumerate(range(0, max(len(words) - overlap, 1), step)):
            window = slice(start, start + size)
            covered = [arts[k] for k in dict.fromkeys(owner[window])]
            labels = [a.label for a in covered]
            location = labels[0] if len(labels) == 1 else f"{labels[0]} to {labels[-1]}"
            first = covered[0]
            chunks.append({
                "id": f"{source}|fixed|{n}",
                "text": " ".join(words[window]),
                "metadata": {**_base_metadata(first), "location": location,
                             "articles": ";".join(labels), "paragraphs": ""},
            })
    return chunks


def chunk_articles(articles: list[Article], design: str) -> list[dict]:
    if design == "structural":
        return chunk_structural(articles)
    if design == "fixed":
        return chunk_fixed(articles)
    raise ValueError(f"unknown design {design!r}")


def chunk_file(path: str | Path, design: str = "structural", source: str | None = None) -> list[dict]:
    """Parse and chunk one file; every chunk carries source and location metadata."""
    chunks = chunk_articles(parse_file(path, source), design)
    for c in chunks:
        c["metadata"]["file"] = Path(path).name
        c["metadata"]["words"] = len(_words(c["text"]))
        c["metadata"]["hash"] = hashlib.sha1(c["text"].encode()).hexdigest()[:16]
    return chunks


# --------------------------------------------------------------------------- embed and store

def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


_client = None


def genai_client():
    global _client
    if _client is None:
        from google import genai

        from api_key import load_api_key

        _client = genai.Client(api_key=load_api_key())
    return _client


class QuotaExhausted(RuntimeError):
    pass


def embed_texts(texts: list[str], task: str = "RETRIEVAL_DOCUMENT") -> list[list[float]]:
    """Embed a batch with Gemini; retries short rate limits, raises QuotaExhausted on the daily cap."""
    from google.genai import errors, types

    config = types.EmbedContentConfig(output_dimensionality=EMBED_DIM, task_type=task)
    for attempt in range(6):
        try:
            # one Content per text: a plain list of strings is embedded as ONE multimodal item
            contents = [types.Content(parts=[types.Part(text=t)]) for t in texts]
            result = genai_client().models.embed_content(model=EMBED_MODEL, contents=contents, config=config)
            vectors = [e.values for e in result.embeddings]
            if len(vectors) != len(texts):
                raise RuntimeError(f"asked for {len(texts)} embeddings, got {len(vectors)}")
            return vectors
        except errors.ClientError as error:
            if error.code != 429:
                raise
            message = str(error)
            if "PerDay" in message or "per day" in message.lower():
                raise QuotaExhausted(message) from error
            wait = 20 * (attempt + 1)
            log(f"  rate limited, waiting {wait}s ...")
            time.sleep(wait)
    raise QuotaExhausted("still rate limited after several retries")


def collection(design: str):
    import chromadb

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return client.get_or_create_collection(f"corpus_{design}", metadata={"hnsw:space": "cosine"})


def embed_and_store(chunks: list[dict], design: str = "structural") -> dict:
    """Embed only chunks whose id+hash has no saved vector; upsert each batch as soon as it returns."""
    col = collection(design)
    ids = [c["id"] for c in chunks]
    existing = col.get(ids=ids, include=["metadatas"]) if ids else {"ids": [], "metadatas": []}
    saved = {i: (m or {}).get("hash") for i, m in zip(existing["ids"], existing["metadatas"])}
    todo = [c for c in chunks if saved.get(c["id"]) != c["metadata"]["hash"]]
    done = 0
    for start in range(0, len(todo), EMBED_BATCH):
        batch = todo[start:start + EMBED_BATCH]
        vectors = embed_texts([c["text"] for c in batch])
        col.upsert(ids=[c["id"] for c in batch], embeddings=vectors,
                   documents=[c["text"] for c in batch], metadatas=[c["metadata"] for c in batch])
        done += len(batch)
        log(f"  [{design}] embedded {done}/{len(todo)}")
    return {"chunks": len(chunks), "already_saved": len(chunks) - len(todo), "embedded": done}


# --------------------------------------------------------------------------- main

def corpus_chunks(design: str) -> list[dict]:
    chunks = []
    for source in SOURCES:
        chunks += chunk_file(download(source), design)
    return chunks


def main() -> int:
    INDEX_DIR.mkdir(exist_ok=True)
    all_chunks = {d: corpus_chunks(d) for d in DESIGNS}
    for design, chunks in all_chunks.items():
        words = sum(c["metadata"]["words"] for c in chunks)
        log(f"{design}: {len(chunks)} chunks, {words} words")
    try:
        for design in DESIGNS:
            stats = embed_and_store(all_chunks[design], design)
            log(f"{design}: {stats}")
    except QuotaExhausted as error:
        log(f"\n{str(error)[:1500]}")
        log("\nDaily embedding quota reached. Every vector so far is saved in index/; "
            "run `main.py index` again after the reset (09:00 Spain) to finish.")
        return 0
    log("Index complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
