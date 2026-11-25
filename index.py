"""
Assignment 3: build the index (`main.py index`).

Use case: a UCITS rules assistant for a fund compliance analyst.
Corpus: four EU UCITS legal acts, downloaded as HTML from the EU Publications Office
(the same texts EUR-Lex shows) into corpus/ (git-ignored). EU legal texts may be reused (Commission Decision 2011/833/EU).

Pipeline (per file): extract_lines -> split_sections -> chunk_sections -> embed_and_store
  - every chunk keeps its source (doc_id + title) and location (Recitals / Article N / Annex N,
    plus chapter and page for PDFs)
  - two chunking designs are built so retrieval can be compared:
      article : one chunk per article; articles over 450 words split at paragraph breaks
      fixed   : 200-word windows with a 40-word overlap, ignoring structure
  - each vector is saved to ChromaDB (index/chroma) as soon as it is received, and only
    chunks without a saved vector are embedded, so a crash or the daily limit loses nothing.

server.py imports add_file(), search() and format_hits() from here.
Run: uv run python main.py index      (or: uv run python index.py)
"""
from __future__ import annotations

import hashlib
import json
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"
CHROMA_DIR = INDEX_DIR / "chroma"
DOCS_FILE = INDEX_DIR / "documents.json"
ACTIVE_FILE = INDEX_DIR / "active_design.txt"
QUERY_CACHE_FILE = INDEX_DIR / "query_cache.json"

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768            # Matryoshka truncation keeps index/ small
SECONDS_BETWEEN_CALLS = 0.6  # stay under the per-minute limit

DESIGNS = ("article", "fixed")   # built in this order
DEFAULT_DESIGN = "article"       # the one the server uses until evaluation says otherwise
FIXED_WORDS, FIXED_OVERLAP = 200, 40
ARTICLE_MAX_WORDS, PIECE_WORDS = 450, 350

EURLEX_HTML = "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:{celex}"
CELLAR_URL = "http://publications.europa.eu/resource/celex/{celex}"
BROWSER_UA = ("Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
              "(KHTML, like Gecko) Chrome/124.0 Safari/537.36")

# min_words: a download shorter than this is incomplete (long acts come in several parts)
CORPUS = [
    {"doc_id": "ucits_directive", "celex": "32009L0065", "min_words": 30_000,
     "title": "Directive 2009/65/EC (UCITS Directive)"},
    {"doc_id": "eligible_assets", "celex": "32007L0016", "min_words": 3_000,
     "title": "Commission Directive 2007/16/EC (eligible assets)"},
    {"doc_id": "organisation", "celex": "32010L0043", "min_words": 8_000,
     "title": "Commission Directive 2010/43/EU (organisational requirements, conflicts of interest, risk management)"},
    {"doc_id": "kiid", "celex": "32010R0583", "min_words": 5_000,
     "title": "Commission Regulation (EU) No 583/2010 (key investor information)"},
]


def log(*args) -> None:
    """Log to stderr: stdout carries the MCP protocol when the server imports this module."""
    print(*args, file=sys.stderr, flush=True)


# --------------------------------------------------------------------------- download
def _download_sources(celex: str) -> list[tuple[str, dict]]:
    """Publications Office (Cellar) first: it serves the same EUR-Lex text to scripts and
    can return all parts of a long act as one zip. EUR-Lex itself often answers scripts
    with a bot check (HTTP 202)."""
    cellar = CELLAR_URL.format(celex=celex)
    return [
        (cellar, {"Accept": "application/zip;mtype=xhtml", "Accept-Language": "eng"}),
        (cellar, {"Accept": "application/xhtml+xml", "Accept-Language": "eng"}),
        (cellar, {"Accept": "text/html", "Accept-Language": "eng"}),
        (EURLEX_HTML.format(celex=celex), {"User-Agent": BROWSER_UA, "Accept-Language": "en"}),
    ]


def _natural_key(name: str):
    return [int(t) if t.isdigit() else t.lower() for t in re.split(r"(\d+)", name)]


def _word_count(html: str) -> int:
    from bs4 import BeautifulSoup

    return len(BeautifulSoup(html, "html.parser").get_text(" ").split())


def _looks_like_the_act(text: str) -> bool:
    return bool(re.search(r"Article(\s|&nbsp;|&#160;)+1\b", text))


def _fetch(client, url: str, headers: dict) -> tuple[str | None, str]:
    """Return (html, note). Joins every part when the act is split into several files."""
    import io
    import zipfile
    from urllib.parse import urljoin

    resp = client.get(url, headers=headers)
    if resp.status_code == 200 and resp.content[:2] == b"PK":           # zip with all parts
        archive = zipfile.ZipFile(io.BytesIO(resp.content))
        names = sorted((n for n in archive.namelist()
                        if n.lower().endswith((".html", ".xhtml", ".htm"))), key=_natural_key)
        parts = [archive.read(n).decode("utf-8", "ignore") for n in names]
        return ("\n".join(parts) if parts else None), f"zip with {len(parts)} part(s)"
    if resp.status_code == 300:                                            # list of parts
        from bs4 import BeautifulSoup

        links = []
        for a in BeautifulSoup(resp.text, "html.parser").find_all("a", href=True):
            href = urljoin(str(resp.url), a["href"])
            if "DOC_" in href and href not in links:
                links.append(href)
        links.sort(key=_natural_key)
        parts = []
        for link in links:
            part = client.get(link, headers=headers)
            if part.status_code == 200:
                parts.append(part.text)
        return ("\n".join(parts) if parts else None), f"{len(parts)} part(s) from a 300 list"
    if resp.status_code == 200:
        return resp.text, "single file"
    return None, f"HTTP {resp.status_code}"


def download_corpus() -> None:
    import httpx

    CORPUS_DIR.mkdir(exist_ok=True)
    with httpx.Client(follow_redirects=True, timeout=120) as client:
        for doc in CORPUS:
            path = CORPUS_DIR / f"{doc['doc_id']}.html"
            if path.exists():
                old = path.read_text(encoding="utf-8", errors="ignore")
                if _looks_like_the_act(old) and _word_count(old) >= doc["min_words"]:
                    continue
                log(f"{path.name} is incomplete; downloading it again")
            log(f"Downloading {doc['title']} ...")
            tried = []
            for url, headers in _download_sources(doc["celex"]):
                try:
                    html, note = _fetch(client, url, headers)
                except httpx.HTTPError as exc:
                    tried.append(f"{url} [{headers.get('Accept', 'browser')}] ({type(exc).__name__})")
                    continue
                words = _word_count(html) if html else 0
                if html and _looks_like_the_act(html) and words >= doc["min_words"]:
                    path.write_text(html, encoding="utf-8")
                    log(f"  saved {words:,} words ({note})")
                    break
                tried.append(f"{url} [{headers.get('Accept', 'browser')}] ({note}, {words:,} words)")
            else:
                raise RuntimeError(
                    "Could not download the full text of " + doc["title"] + ". Tried:\n  " +
                    "\n  ".join(tried) +
                    f"\nOpen {EURLEX_HTML.format(celex=doc['celex'])} in your browser, "
                    f"save it as {path.relative_to(ROOT)} (Save as: Webpage, HTML only), and run again."
                )


# --------------------------------------------------------------------------- extract
def clean_lines(text: str) -> list[str]:
    out = []
    for raw in text.splitlines():
        line = re.sub(r"\s+", " ", raw.replace("\xa0", " ")).strip()
        if line:
            out.append(line)
    return out


def extract_lines(path: Path) -> list[tuple[str, int]]:
    """Return (line, page) pairs. page is 0 when the format has no pages (HTML, text)."""
    suffix = path.suffix.lower()
    if suffix in (".html", ".htm"):
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(path.read_text(encoding="utf-8", errors="ignore"), "html.parser")
        for tag in soup(["script", "style", "head", "nav"]):
            tag.decompose()
        # EUR-Lex styles real article headings with class "ti-art" / "oj-ti-art". Mark them, so
        # that "Article 52" mentioned inside a sentence is never mistaken for a heading.
        for el in soup.find_all(class_=lambda c: bool(c) and re.search(r"(^|oj-)ti-art$", c)):
            el.replace_with(f"\n{ART_MARK}{el.get_text(' ', strip=True)}\n")
        return [(line, 0) for line in clean_lines(soup.get_text("\n"))]
    if suffix == ".pdf":
        from pypdf import PdfReader

        lines = []
        for number, page in enumerate(PdfReader(str(path)).pages, start=1):
            lines += [(line, number) for line in clean_lines(page.extract_text() or "")]
        return lines
    if suffix in (".txt", ".md"):
        return [(line, 0) for line in clean_lines(path.read_text(encoding="utf-8", errors="ignore"))]
    raise ValueError(f"Unsupported file type: {suffix} (use .html, .pdf, .txt or .md)")


# --------------------------------------------------------------------------- structure
ART_MARK = "@@ARTICLE@@ "   # put in front of real headings by extract_lines (HTML)
ART_RE = re.compile(r"^Article (\d+[a-z]?)$")
ANNEX_RE = re.compile(r"^ANNEX(?: ([IVXLC]+))?$")
HEADING_RE = re.compile(r"^(CHAPTER|SECTION|Section|TITLE|PART) ([IVXLC]+|\d+)$")
MARKER_RE = re.compile(r"^(\(?\d{1,3}[a-z]?[).]|\([a-z]{1,4}\)|[—–-])$")  # "(a)", "1.", "—" on their own line


def split_sections(lines: list[tuple[str, int]]) -> list[dict]:
    """Group lines into Recitals / Article N / Annex N, each with chapter and paragraphs."""
    sections: list[dict] = []
    current = {"label": "Recitals", "chapter": "", "paras": []}
    chapter, in_annex, pending, heading_title_next = "", False, "", False
    marked = any(text.startswith(ART_MARK) for text, _ in lines)  # headings known from HTML styling
    seen_article = False

    for text, page in lines:
        is_marked = text.startswith(ART_MARK)
        if is_marked:
            text = text[len(ART_MARK):]
        if heading_title_next:
            heading_title_next = False
            if len(text) < 120 and not text.endswith("."):
                chapter = f"{chapter} {text.title()}"
                continue
        art = None if in_annex or (marked and not is_marked) else ART_RE.match(text)
        annex = ANNEX_RE.match(text) if seen_article else None  # annex lists before Article 1 are not annexes
        heading = None if in_annex else HEADING_RE.match(text)
        if heading:
            if heading.group(1).upper() in ("CHAPTER", "TITLE", "PART"):
                chapter = f"{heading.group(1).title()} {heading.group(2)}"
            heading_title_next = True
            continue
        if art or annex:
            if current["paras"]:
                sections.append(current)
            if annex:
                in_annex = True
                label = f"Annex {annex.group(1)}" if annex.group(1) else "Annex"
                current = {"label": label, "chapter": "", "paras": []}
            else:
                current = {"label": f"Article {art.group(1)}", "chapter": chapter, "paras": []}
                seen_article = True
            continue
        if MARKER_RE.match(text):
            pending = f"{pending} {text}".strip()
            continue
        para = f"{pending} {text}".strip() if pending else text
        pending = ""
        current["paras"].append((para, page))
    if current["paras"]:
        sections.append(current)

    # correlation tables (lists of old vs new article numbers) only add noise
    return [s for s in sections if "CORRELATION TABLE" not in " ".join(p for p, _ in s["paras"][:2]).upper()]


# --------------------------------------------------------------------------- chunking
def _pack(paras: list[tuple[str, int]], limit: int) -> list[list[tuple[str, int]]]:
    pieces, piece, count = [], [], 0
    for para, page in paras:
        words = para.split()
        if len(words) > limit:  # one huge paragraph: cut it by words
            for i in range(0, len(words), limit):
                if piece:
                    pieces.append(piece)
                    piece, count = [], 0
                pieces.append([(" ".join(words[i:i + limit]), page)])
            continue
        if count + len(words) > limit and piece:
            pieces.append(piece)
            piece, count = [], 0
        piece.append((para, page))
        count += len(words)
    if piece:
        pieces.append(piece)
    return pieces


def _make_chunk(doc_id, title, design, text, labels, chapter, page, part, seen) -> dict:
    base = hashlib.sha1(f"{labels[0]}|{text}".encode()).hexdigest()[:16]
    chunk_id, n = f"{doc_id}-{design}-{base}", 1
    while chunk_id in seen:
        n += 1
        chunk_id = f"{doc_id}-{design}-{base}-{n}"
    seen.add(chunk_id)
    return {
        "id": chunk_id,
        "text": text,
        "meta": {
            "doc_id": doc_id,
            "source": title,
            "location": labels[0],
            "locations": "|".join(labels),
            "chapter": chapter or "",
            "page": int(page or 0),
            "part": part,
            "design": design,
            "words": len(text.split()),
        },
    }


def chunk_sections(doc_id: str, title: str, sections: list[dict], design: str) -> list[dict]:
    seen: set[str] = set()
    chunks = []
    if design == "article":
        for sec in sections:
            total = sum(len(p.split()) for p, _ in sec["paras"])
            pieces = [sec["paras"]] if total <= ARTICLE_MAX_WORDS else _pack(sec["paras"], PIECE_WORDS)
            for i, piece in enumerate(pieces, start=1):
                part = "" if len(pieces) == 1 else f"{i}/{len(pieces)}"
                text = "\n".join(p for p, _ in piece)
                chunks.append(_make_chunk(doc_id, title, design, text, [sec["label"]],
                                          sec["chapter"], piece[0][1], part, seen))
    elif design == "fixed":
        words = [(w, sec["label"], sec["chapter"], page)
                 for sec in sections for para, page in sec["paras"] for w in para.split()]
        step = FIXED_WORDS - FIXED_OVERLAP
        for start in range(0, max(len(words) - FIXED_OVERLAP, 1), step):
            window = words[start:start + FIXED_WORDS]
            labels = list(dict.fromkeys(w[1] for w in window))
            text = " ".join(w[0] for w in window)
            chunks.append(_make_chunk(doc_id, title, design, text, labels,
                                      window[0][2], window[0][3], "", seen))
    else:
        raise ValueError(f"Unknown design: {design}")
    return chunks


def chunk_file(path, design: str | None = None, doc_id: str | None = None,
               title: str | None = None) -> list[dict]:
    """Extract, clean and chunk one file with its source and location metadata."""
    path = Path(path)
    doc_id = doc_id or slugify(path.stem)
    title = title or path.stem.replace("_", " ").replace("-", " ")
    sections = split_sections(extract_lines(path))
    return chunk_sections(doc_id, title, sections, design or active_design())


def slugify(name: str) -> str:
    return re.sub(r"[^a-z0-9]+", "_", name.lower()).strip("_") or "document"


# --------------------------------------------------------------------------- embedding
class DailyQuotaReached(RuntimeError):
    pass


_client = None
_last_call = 0.0


def _genai():
    global _client
    if _client is None:
        from google import genai
        from api_key import load_api_key

        _client = genai.Client(api_key=load_api_key())
    return _client


def embed(text: str, retries: int = 6) -> list[float]:
    """Embed ONE text (gemini-embedding-2 merges a list into a single vector)."""
    global _last_call
    from google.genai import errors, types

    for attempt in range(retries):
        wait = SECONDS_BETWEEN_CALLS - (time.time() - _last_call)
        if wait > 0:
            time.sleep(wait)
        _last_call = time.time()
        try:
            result = _genai().models.embed_content(
                model=EMBED_MODEL,
                contents=text,
                config=types.EmbedContentConfig(output_dimensionality=EMBED_DIM),
            )
            return list(result.embeddings[0].values)
        except errors.ClientError as exc:
            if getattr(exc, "code", None) != 429:
                raise
            message = str(exc)
            if "PerDay" in message or "per day" in message.lower():
                raise DailyQuotaReached(message) from exc
            pause = 20 * (attempt + 1)
            log(f"  rate limited, waiting {pause}s ...")
            time.sleep(pause)
        except errors.ServerError:
            time.sleep(5 * (attempt + 1))
    raise DailyQuotaReached("Still rate limited after several retries (probably the daily limit).")


def document_text(chunk: dict) -> str:
    meta = chunk["meta"]
    return f"title: {meta['source']}, {meta['location']} | text: {chunk['text']}"


def query_text(query: str) -> str:
    return f"task: question answering | query: {query}"


# --------------------------------------------------------------------------- storage
_chroma = None


def collection(design: str):
    global _chroma
    import chromadb
    from chromadb.config import Settings

    if _chroma is None:
        CHROMA_DIR.mkdir(parents=True, exist_ok=True)
        _chroma = chromadb.PersistentClient(path=str(CHROMA_DIR),
                                            settings=Settings(anonymized_telemetry=False))
    return _chroma.get_or_create_collection(f"ucits_{design}", metadata={"hnsw:space": "cosine"})


def embed_and_store(chunks: list[dict], design: str | None = None) -> int:
    """Embed chunks that have no saved vector yet; save each vector immediately. Returns the count."""
    design = design or active_design()
    if not chunks:
        return 0
    col = collection(design)
    existing = set(col.get(ids=[c["id"] for c in chunks], include=[])["ids"])
    todo = [c for c in chunks if c["id"] not in existing]
    log(f"[{design}] {len(chunks)} chunks: {len(existing)} already embedded, {len(todo)} to embed")
    for n, chunk in enumerate(todo, start=1):
        vector = embed(document_text(chunk))
        col.add(ids=[chunk["id"]], embeddings=[vector], documents=[chunk["text"]],
                metadatas=[chunk["meta"]])
        if n % 25 == 0 or n == len(todo):
            log(f"[{design}]   embedded {n}/{len(todo)}")
    return len(todo)


def remove_stale(doc_id: str, design: str, keep_ids: set[str]) -> int:
    col = collection(design)
    old = [i for i in col.get(where={"doc_id": doc_id}, include=[])["ids"] if i not in keep_ids]
    if old:
        col.delete(ids=old)
    return len(old)


def load_docs() -> dict:
    return json.loads(DOCS_FILE.read_text()) if DOCS_FILE.exists() else {}


def save_docs(docs: dict) -> None:
    INDEX_DIR.mkdir(exist_ok=True)
    DOCS_FILE.write_text(json.dumps(docs, indent=2, ensure_ascii=False))


def active_design() -> str:
    if ACTIVE_FILE.exists():
        name = ACTIVE_FILE.read_text().strip()
        if name in DESIGNS:
            return name
    return DEFAULT_DESIGN


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# --------------------------------------------------------------------------- add one file
def add_file(path: str, title: str | None = None) -> str:
    """Index one new file into the active design. Identical content is skipped; changed content replaces."""
    file = Path(path).expanduser()
    if not file.is_absolute():
        file = (ROOT / file).resolve()
    if not file.exists():
        return f"File not found: {file}"
    design, digest, docs = active_design(), sha256(file), load_docs()
    for existing_id, info in docs.items():
        if info.get("sha256") == digest:
            return f"Already indexed as '{existing_id}' with identical content; nothing was embedded."
    doc_id = slugify(file.stem)
    replacing = doc_id in docs
    chunks = chunk_file(file, design, doc_id, title)
    if not chunks:
        return f"No text could be extracted from {file.name}; nothing was indexed."
    try:
        new = embed_and_store(chunks, design)
    except DailyQuotaReached:
        return ("The daily embedding limit was reached part-way. Chunks embedded so far are saved; "
                "run add_document again after 09:00 (Spain) to finish.")
    removed = remove_stale(doc_id, design, {c["id"] for c in chunks})
    docs[doc_id] = {"title": title or chunks[0]["meta"]["source"], "sha256": digest,
                    "path": str(file), "designs": [design], "chunks": len(chunks)}
    save_docs(docs)
    verb = "Replaced" if replacing else "Indexed"
    return (f"{verb} {file.name} as '{doc_id}': {len(chunks)} chunks in design '{design}' "
            f"({new} newly embedded, {removed} outdated chunks removed).")


# --------------------------------------------------------------------------- search
def embed_query(query: str) -> list[float]:
    """Query vectors are cached so repeated evaluation runs cost no embeddings."""
    cache = json.loads(QUERY_CACHE_FILE.read_text()) if QUERY_CACHE_FILE.exists() else {}
    key = f"{EMBED_MODEL}|{EMBED_DIM}|{query}"
    if key not in cache:
        cache[key] = embed(query_text(query))
        QUERY_CACHE_FILE.write_text(json.dumps(cache))
    return cache[key]


def citation(meta: dict) -> str:
    locs = meta["locations"].split("|")
    loc = locs[0] if len(locs) == 1 else f"{locs[0]} to {locs[-1]}"
    page = f", p. {meta['page']}" if meta.get("page") else ""
    return f"[{meta['doc_id']}, {loc}{page}]"


def search(query: str, k: int = 5, design: str | None = None, where: dict | None = None) -> list[dict]:
    col = collection(design or active_design())
    res = col.query(query_embeddings=[embed_query(query)], n_results=k, where=where)
    hits = []
    for chunk_id, text, meta, dist in zip(res["ids"][0], res["documents"][0],
                                          res["metadatas"][0], res["distances"][0]):
        hits.append({"id": chunk_id, "text": text, **meta,
                     "score": round(1 - dist, 4), "citation": citation(meta)})
    return hits


def format_hits(hits: list[dict]) -> str:
    if not hits:
        return "No passages found."
    return "\n\n---\n\n".join(
        f"{h['citation']} {h['source']} (relevance {h['score']:.2f})\n{h['text']}" for h in hits
    )


# --------------------------------------------------------------------------- build
def build(designs=DESIGNS) -> int:
    download_corpus()
    INDEX_DIR.mkdir(exist_ok=True)
    docs = load_docs()
    chunks_by_design = {d: [] for d in designs}
    total_words = 0

    for doc in CORPUS:
        path = CORPUS_DIR / f"{doc['doc_id']}.html"
        sections = split_sections(extract_lines(path))
        words = sum(len(p.split()) for s in sections for p, _ in s["paras"])
        total_words += words
        log(f"{doc['doc_id']}: {len(sections)} sections, {words:,} words")

        # readable copy for writing the test set (corpus/ is git-ignored)
        with open(CORPUS_DIR / f"{doc['doc_id']}.txt", "w", encoding="utf-8") as fh:
            fh.write(f"{doc['title']}\n\n")
            for s in sections:
                fh.write(f"\n### {s['label']}" + (f"  ({s['chapter']})" if s["chapter"] else "") + "\n")
                fh.write("\n".join(p for p, _ in s["paras"]) + "\n")

        for design in designs:
            chunks_by_design[design] += chunk_sections(doc["doc_id"], doc["title"], sections, design)
        docs[doc["doc_id"]] = {"title": doc["title"], "sha256": sha256(path),
                               "path": str(path.relative_to(ROOT)), "designs": list(designs),
                               "words": words, "celex": doc["celex"]}
    log(f"Corpus total: {total_words:,} words" + ("" if total_words >= 50_000 else "  (BELOW 50,000!)"))
    save_docs(docs)

    for design in designs:
        with open(INDEX_DIR / f"chunks_{design}.jsonl", "w", encoding="utf-8") as fh:
            for c in chunks_by_design[design]:
                fh.write(json.dumps({"id": c["id"], **c["meta"], "text": c["text"]}, ensure_ascii=False) + "\n")

    try:
        for design in designs:
            embed_and_store(chunks_by_design[design], design)
            for doc in CORPUS:
                keep = {c["id"] for c in chunks_by_design[design] if c["meta"]["doc_id"] == doc["doc_id"]}
                remove_stale(doc["doc_id"], design, keep)
    except DailyQuotaReached:
        log("\nDaily embedding limit reached. Everything embedded so far is saved.\n"
            "Run `uv run python main.py index` again after 09:00 (Spain) to continue.")
        return 0

    if not ACTIVE_FILE.exists():
        ACTIVE_FILE.write_text(DEFAULT_DESIGN)
    for design in designs:
        log(f"[{design}] collection holds {collection(design).count()} vectors")
    log("Index complete.")
    return 0


if __name__ == "__main__":
    sys.exit(build())
    