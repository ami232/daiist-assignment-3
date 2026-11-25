"""
Assignment 3: build the index (`main.py index`).

Corpus: three EU data-protection laws, downloaded from EUR-Lex as HTML into
corpus/ (EU legal texts may be reused, Commission Decision 2011/833/EU).

Pipeline per file: extract text -> clean -> split by the law's own structure
(one chunk per recital and per article; long articles are split at paragraph
boundaries) -> embed with Gemini -> store in a persistent ChromaDB collection
in index/. Every batch of vectors is stored as soon as it arrives and only
chunks without a stored vector are embedded, so re-running costs nothing and a
quota error loses nothing.

server.py's add_document tool imports `chunk_file`, `embed_and_store` and
`add_document` from here.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = Path(os.environ.get("CORPUS_INDEX_DIR", str(ROOT / "index")))
COLLECTION = "corpus"
EMBED_MODEL = os.environ.get("EMBED_MODEL", "gemini-embedding-2")
EMBED_DIM = 768
BATCH = 50
MAX_WORDS = 350  # articles longer than this are split at paragraph boundaries
MIN_WORDS = 40  # a last piece shorter than this is merged into the previous one

# short name (used in citations) -> (title, EUR-Lex URL)
DOCUMENTS = {
    "GDPR": (
        "Regulation (EU) 2016/679 - General Data Protection Regulation",
        "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32016R0679",
    ),
    "LED": (
        "Directive (EU) 2016/680 - Law Enforcement Directive",
        "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32016L0680",
    ),
    "ePrivacy": (
        "Directive 2002/58/EC - ePrivacy Directive (consolidated text of 19.12.2009)",
        "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:02002L0058-20091219",
    ),
}
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Accept-Language": "en",
}


class QuotaExhausted(RuntimeError):
    """The daily embedding quota is used up; what was stored so far is kept."""


def log(*args) -> None:
    """Log to stderr: stdout carries the MCP protocol when server.py imports this."""
    print(*args, file=sys.stderr, flush=True)


# ------------------------------------------------------------------ download


def download(name: str, url: str) -> Path:
    """Fetch one document into corpus/<name>.html unless it is already there."""
    import httpx

    CORPUS_DIR.mkdir(exist_ok=True)
    path = CORPUS_DIR / f"{name}.html"
    if path.is_file() and path.stat().st_size > 10_000:
        return path
    log(f"Downloading {name} from EUR-Lex ...")
    response = httpx.get(url, headers=HEADERS, follow_redirects=True, timeout=120)
    if "Article 1" not in response.text.replace("\xa0", " ") and "CELEX:" in url:
        # EUR-Lex shows a bot check to cloud machines (e.g. Codespaces, CI). The EU
        # Publications Office (Cellar) serves the same official text by CELEX number.
        celex = url.split("CELEX:")[1]
        response = httpx.get(
            f"https://publications.europa.eu/resource/celex/{celex}",
            headers={"Accept": "application/xhtml+xml", "Accept-Language": "eng"},
            follow_redirects=True,
            timeout=120,
        )
    response.raise_for_status()
    if "Article 1" not in response.text.replace("\xa0", " "):
        raise RuntimeError(
            f"{url} did not return the text of the law (EUR-Lex may have shown a bot check).\n"
            f"Open the URL in a browser, save the page as {path} and run again."
        )
    path.write_bytes(response.content)
    return path


# ------------------------------------------------------------------ extract and clean

MARKER_RE = re.compile(r"[\u25bc\u25ba]\s*[A-Z]\d*\b|\u25c4")  # consolidation markers such as "M2" arrows
LABEL_RE = re.compile(r"^(\((?:[a-z]{1,4}|\d{1,3})\)|\d{1,3}\.|[a-z]\))$")  # "(a)", "(12)", "3." alone on a line
FOOTNOTE_RE = re.compile(r"^\(\d+\)\s+(OJ [LC]\b|OJ No\b|Position of the European Parliament|Opinion of)")
ART_RE = re.compile(r"^Article\s+(\d+[a-z]?)$")
RECITAL_RE = re.compile(r"^\((\d+)\)\s+(\S.*)$")
CHAPTER_RE = re.compile(r"^(CHAPTER|Chapter)\s+[IVXLC]+$")
SECTION_RE = re.compile(r"^Section\s+\d+$")
ANNEX_RE = re.compile(r"^ANNEX\b")


def _is_note_class(value: str | None) -> bool:
    return bool(value) and "note" in value and "note-tag" not in value


def html_text(path: Path) -> str:
    """Visible text of an HTML file, one block element per line.

    Extraction problem fixed here: EUR-Lex wraps footnote markers in their own
    elements, so a plain get_text("\\n") put "(1)" on a line of its own in the
    middle of sentences, where it looked like a recital number. We drop the
    markers and the footnote bodies, and unwrap inline tags so that a sentence
    stays on one line.
    """
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(path.read_bytes(), "html.parser")
    for tag in soup(["script", "style", "noscript", "header", "nav", "footer"]):
        tag.decompose()
    for tag in soup.find_all(class_=_is_note_class):
        tag.decompose()  # footnote bodies at the end of the act
    for tag in soup.find_all(["a", "span", "sup"]):
        if tag.decomposed:
            continue
        text = tag.get_text(strip=True)
        classes = " ".join(tag.get("class") or [])
        if re.fullmatch(r"\(\s*\d+\s*\)", text) and (
            tag.name in ("a", "sup") or "super" in classes or "note" in classes
        ):
            tag.decompose()  # footnote markers inside sentences
    for tag in soup.find_all(["span", "a", "i", "b", "em", "strong", "sup", "sub", "abbr", "font", "u"]):
        tag.unwrap()
    return soup.get_text("\n")


def pdf_pages(path: Path) -> list[str]:
    from pypdf import PdfReader

    return [page.extract_text() or "" for page in PdfReader(str(path)).pages]


def clean_lines(text: str) -> list[str]:
    """Normalise whitespace, drop consolidation markers and footnotes, and glue
    point labels such as "(a)" or "2." to the line that follows them."""
    lines: list[str] = []
    pending = ""
    for raw in text.splitlines():
        line = MARKER_RE.sub(" ", raw.replace("\xa0", " ").replace("\u2002", " ").replace("\u2003", " "))
        line = re.sub(r"\s+", " ", line).strip()
        if not line or FOOTNOTE_RE.match(line):
            continue
        if LABEL_RE.match(line):
            pending = f"{pending} {line}".strip()
            continue
        if pending:
            line, pending = f"{pending} {line}", ""
        lines.append(line)
    if pending:
        lines.append(pending)
    return lines


# ------------------------------------------------------------------ structure


def parse_law(lines: list[str]) -> list[dict]:
    """Split an EU act into units: one per recital and one per article.

    Returns dicts with location ("Recital 12", "Article 33"), heading, chapter,
    kind and paragraphs. Recitals must be numbered consecutively, which keeps
    numbered points inside articles from being mistaken for recitals.
    """
    units: list[dict] = []
    zone = "preamble"
    current: dict | None = None
    next_recital = 1
    chapter = ""
    want_title = None  # "chapter", "section" or "article" when the next line is a title

    for line in lines:
        if line.startswith("Done at "):
            break
        if zone == "preamble" and line.startswith("Whereas"):
            zone = "recitals"
            continue
        if zone == "recitals" and line.startswith("HAVE ADOPTED"):
            zone, current = "body", None
            continue
        match = ART_RE.match(line)
        if match and zone != "recitals":
            zone = "body"
            current = {"location": f"Article {match.group(1)}", "heading": "", "chapter": chapter,
                       "kind": "article", "paras": []}
            units.append(current)
            want_title = "article"
            continue
        if zone == "body" and CHAPTER_RE.match(line):
            chapter, want_title, current = line, "chapter", None
            continue
        if zone == "body" and SECTION_RE.match(line):
            want_title, current = "section", None
            continue
        if zone == "body" and ANNEX_RE.match(line):
            current = {"location": "Annex", "heading": line, "chapter": "", "kind": "annex", "paras": []}
            units.append(current)
            continue
        if want_title:
            if want_title == "chapter":
                chapter = f"{chapter} - {line}"
            elif want_title == "article" and current is not None:
                current["heading"] = line
            want_title = None
            continue
        if zone == "recitals":
            rec = RECITAL_RE.match(line)
            if rec and int(rec.group(1)) == next_recital:
                current = {"location": f"Recital {next_recital}", "heading": "", "chapter": "",
                           "kind": "recital", "paras": [rec.group(2)]}
                units.append(current)
                next_recital += 1
            elif current is not None:
                current["paras"].append(line)
            continue
        if current is not None:
            current["paras"].append(line)
    return [u for u in units if u["paras"]]


def words(text: str) -> int:
    return len(text.split())


def split_paras(paras: list[str], max_words: int = MAX_WORDS) -> list[list[str]]:
    """Group paragraphs into pieces of at most max_words (a longer single
    paragraph stays whole), merging a short last piece into the previous one."""
    pieces: list[list[str]] = [[]]
    for para in paras:
        if pieces[-1] and words(" ".join(pieces[-1] + [para])) > max_words:
            pieces.append([])
        pieces[-1].append(para)
    if len(pieces) > 1 and words(" ".join(pieces[-1])) < MIN_WORDS:
        pieces[-2].extend(pieces.pop())
    return pieces


def make_chunk(source: str, location: str, heading: str, body: str, kind: str, part: int, n_parts: int,
               file: str, chapter: str = "") -> dict:
    label = location if n_parts == 1 else f"{location} (part {part}/{n_parts})"
    header = f"{source} {label}" + (f" - {heading}" if heading else "")
    text = f"{header}\n{body}"  # the header is embedded too: it carries the article title
    digest = hashlib.sha1(text.encode("utf-8")).hexdigest()[:10]
    return {
        "id": f"{source}|{location}|{part}|{digest}",
        "text": text,
        "source": source,
        "location": location,
        "heading": heading,
        "chapter": chapter,
        "kind": kind,
        "part": part,
        "file": file,
        "words": words(body),
    }


def chunk_file(path: str | Path, source: str | None = None) -> list[dict]:
    """Extract, clean and chunk one file (.html/.htm, .pdf, .txt/.md).

    EU acts are chunked by recital and article. Other files fall back to
    markdown headings (section), PDF pages (page) or paragraph windows (part).
    """
    path = Path(path)
    source = source or path.stem
    suffix = path.suffix.lower()
    chunks: list[dict] = []

    if suffix == ".pdf":
        for number, page in enumerate(pdf_pages(path), start=1):
            body = " ".join(clean_lines(page))
            if words(body) >= 5:
                chunks.append(make_chunk(source, f"page {number}", "", body, "page", 1, 1, path.name))
        return chunks

    if suffix in (".html", ".htm"):
        lines = clean_lines(html_text(path))
    elif suffix in (".txt", ".md"):
        lines = clean_lines(path.read_text(encoding="utf-8", errors="replace"))
    else:
        raise ValueError(f"Unsupported file type {suffix!r}: use .html, .pdf, .txt or .md")

    units = parse_law(lines)
    if sum(u["kind"] == "article" for u in units) >= 3:
        for unit in units:
            pieces = split_paras(unit["paras"])
            for part, paras in enumerate(pieces, start=1):
                chunks.append(make_chunk(source, unit["location"], unit["heading"], "\n".join(paras),
                                         unit["kind"], part, len(pieces), path.name, unit["chapter"]))
        return chunks

    # Not an EU act: markdown sections if there are headings, else paragraph windows.
    sections: list[tuple[str, list[str]]] = [("start", [])]
    for line in lines:
        if line.startswith("#"):
            sections.append((line.lstrip("# ").strip() or "section", []))
        else:
            sections[-1][1].append(line)
    sections = [s for s in sections if s[1]]
    if len(sections) <= 1:
        paras = sections[0][1] if sections else []
        for i, piece in enumerate(split_paras(paras), start=1):
            chunks.append(make_chunk(source, f"part {i}", "", "\n".join(piece), "section", 1, 1, path.name))
        return chunks
    for title, paras in sections:
        pieces = split_paras(paras)
        for part, piece in enumerate(pieces, start=1):
            chunks.append(make_chunk(source, f"section {title}", title, "\n".join(piece), "section",
                                     part, len(pieces), path.name))
    return chunks


# ------------------------------------------------------------------ embed and store

_client = None
_use_task_type = True
_collections: dict[str, object] = {}


def gemini():
    global _client
    if _client is None:
        from google import genai

        from api_key import load_api_key

        _client = genai.Client(api_key=load_api_key())
    return _client


def embed_texts(texts: list[str], task: str = "RETRIEVAL_DOCUMENT") -> list[list[float]]:
    """Embed a batch with Gemini, retrying on rate limits. Raises QuotaExhausted
    when the daily quota is gone, so callers can stop and keep what they stored."""
    global _use_task_type
    from google.genai import errors, types

    for attempt in range(1, 7):
        config = (types.EmbedContentConfig(task_type=task, output_dimensionality=EMBED_DIM)
                  if _use_task_type else types.EmbedContentConfig(output_dimensionality=EMBED_DIM))
        try:
            result = gemini().models.embed_content(model=EMBED_MODEL, contents=[types.Content(parts=[types.Part(text=t)]) for t in texts],  # one Content per text: gemini-embedding-2 merges a plain list of strings into ONE vector
                config=config)
            return [list(e.values) for e in result.embeddings]
        except errors.ClientError as error:
            message = str(error)
            if error.code == 400 and _use_task_type and "task" in message.lower():
                _use_task_type = False  # this model does not take task_type
                continue
            if error.code == 429:
                if "PerDay" in message or "per day" in message.lower():
                    raise QuotaExhausted(message) from error
                wait = 20 * attempt
                log(f"Rate limited, waiting {wait}s ...")
                time.sleep(wait)
                continue
            raise
        except errors.ServerError:
            time.sleep(10 * attempt)
    raise RuntimeError("Embedding failed after several retries.")


def normalise(vectors: list[list[float]]) -> list[list[float]]:
    """Unit length, so the dot product used for search is the cosine similarity."""
    import numpy as np

    array = np.asarray(vectors, dtype=np.float32)
    array /= np.linalg.norm(array, axis=1, keepdims=True) + 1e-12
    return array.tolist()


def collection(index_dir: Path | None = None):
    """The persistent Chroma collection in index/ (created if missing)."""
    import chromadb
    from chromadb.config import Settings

    path = Path(index_dir or INDEX_DIR) / "chroma"
    key = str(path)
    if key not in _collections:
        path.mkdir(parents=True, exist_ok=True)
        db = chromadb.PersistentClient(path=key, settings=Settings(anonymized_telemetry=False))
        _collections[key] = db.get_or_create_collection(COLLECTION)
    return _collections[key]


def metadata(chunk: dict) -> dict:
    return {k: chunk[k] for k in ("source", "location", "heading", "chapter", "kind", "part", "file", "words")}


def embed_and_store(chunks: list[dict], col=None) -> int:
    """Embed the chunks that have no stored vector yet and store each batch at
    once. Returns how many were embedded."""
    col = col or collection()
    if not chunks:
        return 0
    stored = set(col.get(ids=[c["id"] for c in chunks], include=[])["ids"])
    todo = [c for c in chunks if c["id"] not in stored]
    for start in range(0, len(todo), BATCH):
        batch = todo[start:start + BATCH]
        vectors = normalise(embed_texts([c["text"] for c in batch]))
        col.add(ids=[c["id"] for c in batch], embeddings=vectors,
                documents=[c["text"] for c in batch], metadatas=[metadata(c) for c in batch])
        log(f"  stored {min(start + BATCH, len(todo))}/{len(todo)} new vectors")
    return len(todo)


def add_document(path: str | Path, index_dir: Path | None = None) -> dict:
    """Index one more file. The source name is the file name without extension.

    Already indexed with the same content: nothing happens (no quota spent).
    Same name, changed content: changed chunks are replaced, unchanged ones
    keep their vectors.
    """
    path = Path(path).expanduser()
    if not path.is_absolute():
        path = (ROOT / path).resolve()
    if not path.is_file():
        raise FileNotFoundError(f"No file at {path}")
    chunks = chunk_file(path)
    if not chunks:
        raise ValueError(f"No text could be extracted from {path}")
    source = chunks[0]["source"]
    col = collection(index_dir)
    existing = set(col.get(where={"source": source}, include=[])["ids"])
    new_ids = {c["id"] for c in chunks}
    if existing == new_ids:
        return {"status": "already indexed", "source": source, "chunks": len(chunks), "embedded": 0}
    stale = sorted(existing - new_ids)
    embedded = embed_and_store(chunks, col)
    if stale:
        col.delete(ids=stale)
    return {"status": "updated" if existing else "added", "source": source, "chunks": len(chunks),
            "embedded": embedded, "removed": len(stale)}


# ------------------------------------------------------------------ main


def build() -> None:
    col = collection()
    stats = {}
    all_chunks: list[dict] = []
    for name, (title, url) in DOCUMENTS.items():
        path = download(name, url)
        chunks = chunk_file(path, source=name)
        stats[name] = {
            "title": title,
            "url": url,
            "words": sum(c["words"] for c in chunks),
            "chunks": len(chunks),
            "recitals": len({c["location"] for c in chunks if c["kind"] == "recital"}),
            "articles": len({c["location"] for c in chunks if c["kind"] == "article"}),
        }
        log(f"{name}: {stats[name]['words']} words, {len(chunks)} chunks")
        all_chunks.extend(chunks)

    # Remove chunks of the core documents that the current chunking no longer makes.
    wanted = {c["id"] for c in all_chunks}
    for name in DOCUMENTS:
        old = set(col.get(where={"source": name}, include=[])["ids"])
        if old - wanted:
            col.delete(ids=sorted(old - wanted))
            log(f"{name}: removed {len(old - wanted)} outdated chunks")

    try:
        embedded = embed_and_store(all_chunks, col)
    except QuotaExhausted:
        log("Daily embedding quota used up. Everything embedded so far is saved; "
            "run `main.py index` again tomorrow to finish.")
        sys.exit(2)

    stats["_total"] = {
        "words": sum(s["words"] for s in stats.values()),
        "chunks": len(all_chunks),
        "embedded_this_run": embedded,
        "in_index": col.count(),
        "model": EMBED_MODEL,
        "dimensions": EMBED_DIM,
    }
    (INDEX_DIR / "stats.json").write_text(json.dumps(stats, indent=2), encoding="utf-8")
    log(json.dumps(stats["_total"], indent=2))


if __name__ == "__main__":
    build()
