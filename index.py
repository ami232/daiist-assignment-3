"""
Assignment 3: build the index (`main.py index`).

    download -> extract -> clean -> chunk (one or more designs) -> embed -> store

Every chunk carries `source` (document name) and `location` (section heading
and page range). Vectors are written to ChromaDB in index/ after every batch,
so a crash or the daily quota loses nothing; a rerun embeds only chunks that
have no saved vector yet.

server.py and evaluate.py import the functions in this file (`chunk_file`,
`embed_and_store`, `add_file`, `search`), so keep their signatures stable.
Progress goes to stderr: server.py's stdout carries the MCP protocol.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import sys
import time
import unicodedata
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"
QUERY_CACHE = INDEX_DIR / "query_vectors.json"
MANIFEST = INDEX_DIR / "manifest.json"

# ---------------------------------------------------------------------------
# Configuration. The corpus and the design choice are yours to fill in.
# ---------------------------------------------------------------------------

# The corpus. EUR-Lex serves its PDFs behind a bot challenge that scripts
# cannot pass, so the files are committed in corpus/ and `url` is the citation
# for the report; download_corpus() only fetches files that are missing.
# Licence: EU legal acts on EUR-Lex may be reused with acknowledgement of the
# source (Commission Decision 2011/833/EU).
LICENCE = "EUR-Lex, reuse authorised (Decision 2011/833/EU)"
SOURCES: list[dict] = [
    {"name": "MiFIR", "filename": "CELEX_32014R0600_EN_TXT.pdf", "licence": LICENCE,
     "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32014R0600",
     "title": "Regulation (EU) No 600/2014 on markets in financial instruments (MiFIR)"},
    {"name": "MiFID II", "filename": "CELEX_32014L0065_EN_TXT.pdf", "licence": LICENCE,
     "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32014L0065",
     "title": "Directive 2014/65/EU on markets in financial instruments (MiFID II)"},
    {"name": "MiFID II Delegated Regulation", "filename": "CELEX_32017R0565_EN_TXT.pdf", "licence": LICENCE,
     "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32017R0565",
     "title": "Commission Delegated Regulation (EU) 2017/565 supplementing MiFID II"},
    {"name": "PRIIPs", "filename": "CELEX_32014R1286_EN_TXT.pdf", "licence": LICENCE,
     "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32014R1286",
     "title": "Regulation (EU) No 1286/2014 on key information documents for PRIIPs"},
]
# Held back from the index: added later with the add_document tool to show an
# unanswerable question (q34, q35: summary risk indicator, performance
# scenarios) becoming answerable. Lives in reserve/, not corpus/.
RESERVE: list[dict] = [
    {"name": "PRIIPs RTS", "filename": "CELEX_32017R0653_EN_TXT.pdf", "licence": LICENCE,
     "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32017R0653",
     "title": "Commission Delegated Regulation (EU) 2017/653, regulatory technical standards for PRIIPs KIDs"},
]
SUPPORTED = {".pdf", ".html", ".htm", ".txt", ".md"}

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768        # smaller vectors keep index/ well under 90 MB
EMBED_BATCH = 50       # texts per request; each text counts against the daily quota

# Chunking designs to build. Each one is a separate ChromaDB collection and
# costs a full embedding pass, so add designs deliberately.
DESIGNS: dict[str, dict] = {
    # fixed-size word windows that ignore structure
    "words150": {"method": "fixed", "size": 150, "overlap": 30, "prefix": False},
    # one chunk per section, long sections split on sentence boundaries,
    # with "source - heading" prepended to the embedded text
    "sections": {"method": "section", "max_words": 350, "prefix": True},
}
# Served by server.py and embedded first. Chosen by hit rate (eval/retrieval.csv):
# sections+vector 0.76/0.94/0.97 at k=1/3/5 vs words150 0.58/0.88/0.91 and
# sections+hybrid 0.58/0.94/0.97.
DEFAULT_DESIGN = "sections"
DEFAULT_MODE = "vector"       # "vector" or "hybrid" (vector + BM25, no extra embeddings)
DEFAULT_K = 5

# Lines that start a new section in text extracted from PDFs. EU regulations:
# "Article 12", "Article 12a", "ANNEX I". (Numbered paragraphs and cross-
# references such as "Article 4(1) of Directive ..." must not match.)
HEADING_RE = re.compile(r"^(?:Article \d+[a-z]?|ANNEX(?: [IVXLC]+)?)$")
# In EU acts the line after "Article N" is the article's title.
TITLE_AFTER_HEADING = True
# Heading for text before the first article (citations, recitals).
FRONT_MATTER = "Recitals"
# Lines dropped wherever they appear, e.g. the Official Journal page header,
# which pypdf sometimes places mid-page.
NOISE_RE = re.compile(r"Official Journal of the European Union")


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


# ---------------------------------------------------------------------------
# Download
# ---------------------------------------------------------------------------

def _filename(source: dict) -> str:
    if source.get("filename"):
        return source["filename"]
    suffix = Path(source["url"].split("?")[0]).suffix.lower()
    return source["name"] + (suffix if suffix in SUPPORTED else ".html")


def download_corpus() -> list[Path]:
    """Download every entry of SOURCES into corpus/ (skipping ones already there)."""
    import httpx

    CORPUS_DIR.mkdir(exist_ok=True)
    paths = []
    for source in SOURCES:
        path = CORPUS_DIR / _filename(source)
        if not path.exists():
            log(f"Downloading {source['name']} ...")
            response = httpx.get(source["url"], follow_redirects=True, timeout=120,
                                 headers={"User-Agent": "Mozilla/5.0 (course assignment)"})
            response.raise_for_status()
            path.write_bytes(response.content)
        paths.append(path)
    return paths


# ---------------------------------------------------------------------------
# Extract and clean: file -> blocks of {"page", "heading", "text"}
# ---------------------------------------------------------------------------

def clean_text(text: str) -> str:
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("­", "")                    # soft hyphens
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)          # words hyphenated across lines
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    return text.strip()


def _is_heading(line: str) -> bool:
    return len(line) <= 120 and bool(HEADING_RE.match(line))


def _repeated_lines(pages: list[list[str]]) -> set[str]:
    """Running headers/footers: top/bottom lines (digits ignored) found on 30%+ of pages."""
    if len(pages) < 4:
        return set()
    counts = Counter()
    for lines in pages:
        counts.update({re.sub(r"\d+", "#", l) for l in lines[:3] + lines[-3:]})
    return {line for line, n in counts.items() if n >= 0.3 * len(pages)}


def _headings_have_titles(pages: list[list[str]]) -> bool:
    """False when most headings are followed straight by a numbered paragraph ("1. ..."),
    i.e. the document does not title its articles (as in the PRIIPs Regulation)."""
    lines = [l.strip() for page in pages for l in page if l.strip()]
    following = [lines[i + 1] for i in range(len(lines) - 1) if _is_heading(lines[i])]
    numbered = sum(bool(re.match(r"^\d+\.\s", l)) for l in following)
    return bool(following) and numbered < len(following) / 2


def extract_pdf(path: Path) -> list[dict]:
    from pypdf import PdfReader

    pages = [clean_text(p.extract_text() or "").split("\n") for p in PdfReader(path).pages]
    repeated = _repeated_lines(pages)
    blocks, heading, want_title, title_open = [], FRONT_MATTER, False, False
    has_titles = TITLE_AFTER_HEADING and _headings_have_titles(pages)
    for number, lines in enumerate(pages, start=1):
        paragraph: list[str] = []

        def flush():
            if paragraph:
                blocks.append({"page": number, "heading": heading, "text": " ".join(paragraph)})
                paragraph.clear()

        for i, line in enumerate(lines):
            line = line.strip()
            if not line or re.fullmatch(r"(page\s*)?\d+(\s*(of|/)\s*\d+)?", line, re.I):
                continue
            edge = i < 3 or i >= len(lines) - 3
            if edge and not _is_heading(line) and re.sub(r"\d+", "#", line) in repeated:
                continue
            if NOISE_RE.search(line):
                continue
            if _is_heading(line):
                flush()
                heading, want_title, title_open = line, has_titles, False
                continue
            if want_title:
                want_title = False
                if len(line.split()) <= 20 and not line.endswith((".", ":", ";")) and not re.match(r"^(\d+\.|\()", line):
                    heading, title_open = f"{heading} ({line})", True
                    continue
            if title_open:
                title_open = False
                if line[:1].islower() and len(line.split()) <= 20:    # title wrapped onto a second line
                    heading = f"{heading[:-1]} {line})"
                    continue
            paragraph.append(line)
            if line.endswith((".", ":", ";")) and len(" ".join(paragraph).split()) > 40:
                flush()
        flush()
    return blocks


def extract_html(path: Path) -> list[dict]:
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(path.read_bytes(), "html.parser")
    for tag in soup(["script", "style", "nav", "footer", "header", "aside", "form", "noscript"]):
        tag.decompose()
    blocks, heading = [], ""
    for el in soup.find_all(["h1", "h2", "h3", "h4", "p", "li", "td", "pre", "blockquote"]):
        if el.find(["p", "li", "td"]):           # avoid counting nested text twice
            continue
        text = clean_text(el.get_text(" ")).replace("\n", " ")
        if not text:
            continue
        if el.name in {"h1", "h2", "h3", "h4"}:
            heading = text[:120]
        else:
            blocks.append({"page": None, "heading": heading, "text": text})
    return blocks


def extract_text_file(path: Path) -> list[dict]:
    blocks, heading = [], ""
    for para in re.split(r"\n\s*\n", clean_text(path.read_text(encoding="utf-8", errors="replace"))):
        para = para.strip()
        if not para:
            continue
        if para.startswith("#") or (_is_heading(para) and "\n" not in para):
            heading = para.lstrip("# ").strip()
            continue
        blocks.append({"page": None, "heading": heading, "text": para.replace("\n", " ")})
    return blocks


def extract(path: Path) -> list[dict]:
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        return extract_pdf(path)
    if suffix in {".html", ".htm"}:
        return extract_html(path)
    if suffix in {".txt", ".md"}:
        return extract_text_file(path)
    raise ValueError(f"Unsupported file type {suffix!r}; supported: {', '.join(sorted(SUPPORTED))}")


# ---------------------------------------------------------------------------
# Chunk
# ---------------------------------------------------------------------------

def _location(heading: str, pages: list[int | None]) -> str:
    pages = sorted({p for p in pages if p})
    page = "" if not pages else (f"p. {pages[0]}" if len(pages) == 1 else f"pp. {pages[0]}-{pages[-1]}")
    return ", ".join(part for part in (heading, page) if part) or "whole document"


def _chunk(source: str, design: str, index: int, text: str, location: str, embed_text: str) -> dict:
    digest = hashlib.sha1(f"{source}|{design}|{location}|{text}".encode()).hexdigest()[:16]
    return {"id": f"{design}:{source}:{index}:{digest}", "text": text, "embed_text": embed_text,
            "source": source, "location": location, "design": design, "chunk": index,
            "words": len(text.split())}


def _title(source: str, heading: str) -> str:
    return f"{source} - {heading}" if heading else source


def _split_long(text: str, max_words: int) -> list[str]:
    """Split on sentence boundaries into pieces of at most ~max_words."""
    pieces, current = [], []
    for sentence in re.split(r"(?<=[.!?;])\s+", text):
        if current and len(" ".join(current + [sentence]).split()) > max_words:
            pieces.append(" ".join(current))
            current = []
        current.append(sentence)
    if current:
        pieces.append(" ".join(current))
    out = []
    for piece in pieces:                      # a single sentence longer than max_words
        words = piece.split()
        out += [" ".join(words[i:i + max_words]) for i in range(0, len(words), max_words)]
    return out


def chunk_blocks(blocks: list[dict], source: str, design: str) -> list[dict]:
    cfg = DESIGNS[design]
    chunks: list[dict] = []
    if cfg["method"] == "fixed":
        words = [(w, b["page"], b["heading"]) for b in blocks for w in b["text"].split()]
        step = cfg["size"] - cfg["overlap"]
        for start in range(0, max(len(words) - cfg["overlap"], 1) if words else 0, step):
            window = words[start:start + cfg["size"]]
            text = " ".join(w for w, _, _ in window)
            headings = list(dict.fromkeys(h for _, _, h in window if h))
            span = headings[0] if len(headings) == 1 else f"{headings[0]} to {headings[-1]}" if headings else ""
            location = _location(span, [p for _, p, _ in window])
            embed = f"{_title(source, window[0][2])}\n{text}" if cfg["prefix"] else text
            chunks.append(_chunk(source, design, len(chunks), text, location, embed))
    elif cfg["method"] == "section":
        groups: list[list[dict]] = []
        for block in blocks:
            if groups and groups[-1][0]["heading"] == block["heading"]:
                groups[-1].append(block)
            else:
                groups.append([block])
        for group in groups:
            heading = group[0]["heading"]
            current: list[dict] = []

            def emit(parts: list[dict]):
                text = " ".join(p["text"] for p in parts)
                for piece in _split_long(text, cfg["max_words"]):
                    location = _location(heading, [p["page"] for p in parts])
                    embed = f"{_title(source, heading)}\n{piece}" if cfg["prefix"] else piece
                    chunks.append(_chunk(source, design, len(chunks), piece, location, embed))

            for block in group:
                if current and sum(len(b["text"].split()) for b in current + [block]) > cfg["max_words"]:
                    emit(current)
                    current = []
                current.append(block)
            if current:
                emit(current)
    else:
        raise ValueError(f"Unknown chunking method {cfg['method']!r}")
    return [c for c in chunks if c["words"] >= 5]


def source_name(path: Path) -> str:
    for source in SOURCES + RESERVE:
        if _filename(source) == path.name:
            return source["name"]
    return path.stem


def chunk_file(path: str | Path, design: str = DEFAULT_DESIGN, source: str | None = None) -> list[dict]:
    """Extract, clean and chunk one file. Returns chunk dicts with source and location."""
    path = Path(path)
    return chunk_blocks(extract(path), source or source_name(path), design)


# ---------------------------------------------------------------------------
# Embed and store
# ---------------------------------------------------------------------------

class QuotaExhausted(RuntimeError):
    pass


_client = None


def genai_client():
    global _client
    if _client is None:
        from google import genai
        from api_key import load_api_key
        _client = genai.Client(api_key=load_api_key())
    return _client


def embed_texts(texts: list[str], task: str = "RETRIEVAL_DOCUMENT") -> list[list[float]]:
    """Embed a batch, retrying on per-minute limits; QuotaExhausted on the daily one."""
    from google.genai import errors, types

    config = types.EmbedContentConfig(task_type=task, output_dimensionality=EMBED_DIM)
    for attempt in range(6):
        try:
            # One Content per text: gemini-embedding-2 treats a plain list of
            # strings as ONE multi-part input and returns a single vector.
            contents = [types.Content(parts=[types.Part(text=t)]) for t in texts]
            result = genai_client().models.embed_content(model=EMBED_MODEL, contents=contents, config=config)
            vectors = [e.values for e in result.embeddings]
            if len(vectors) != len(texts):
                raise RuntimeError(f"Sent {len(texts)} texts, got {len(vectors)} embeddings back")
            return [_normalise(v) for v in vectors]
        except errors.APIError as error:
            message = str(error)
            if error.code == 429 and ("PerDay" in message or "per day" in message.lower()):
                raise QuotaExhausted(message) from error
            if error.code in (429, 500, 503) and attempt < 5:
                wait = 2 ** attempt * 5
                log(f"  {error.code} from Gemini, retrying in {wait}s ...")
                time.sleep(wait)
                continue
            raise
    raise RuntimeError("unreachable")


def _normalise(v: list[float]) -> list[float]:
    # Truncated (output_dimensionality < full) vectors are not unit length.
    norm = math.sqrt(sum(x * x for x in v)) or 1.0
    return [x / norm for x in v]


_chroma = None


def collection(design: str = DEFAULT_DESIGN):
    global _chroma
    import chromadb
    from chromadb.config import Settings

    if _chroma is None:
        INDEX_DIR.mkdir(exist_ok=True)
        _chroma = chromadb.PersistentClient(path=str(INDEX_DIR), settings=Settings(anonymized_telemetry=False))
    return _chroma.get_or_create_collection(f"chunks_{design}", metadata={"hnsw:space": "cosine"})


def embed_and_store(chunks: list[dict], design: str = DEFAULT_DESIGN, extra_metadata: dict | None = None) -> int:
    """Embed the chunks that have no saved vector and store them. Returns how many were embedded."""
    col = collection(design)
    ids = [c["id"] for c in chunks]
    existing = set()
    for i in range(0, len(ids), 500):
        existing |= set(col.get(ids=ids[i:i + 500], include=[])["ids"])
    todo = [c for c in chunks if c["id"] not in existing]
    for i in range(0, len(todo), EMBED_BATCH):
        batch = todo[i:i + EMBED_BATCH]
        vectors = embed_texts([c["embed_text"] for c in batch])
        col.upsert(
            ids=[c["id"] for c in batch],
            embeddings=vectors,
            documents=[c["text"] for c in batch],
            metadatas=[{"source": c["source"], "location": c["location"], "chunk": c["chunk"],
                        "words": c["words"], **(extra_metadata or {})} for c in batch],
        )
        log(f"  [{design}] embedded {min(i + EMBED_BATCH, len(todo))}/{len(todo)}")
    _bm25_cache.pop(design, None)
    return len(todo)


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def add_file(path: str | Path, design: str = DEFAULT_DESIGN) -> dict:
    """Index one file into one design (used by server.py's add_document).

    Policy for documents already indexed (identified by source name = file stem):
      - same content (sha256)   -> nothing to do
      - different content       -> old chunks removed, new ones embedded
    """
    path = Path(path).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"No such file: {path}")
    if path.suffix.lower() not in SUPPORTED:
        raise ValueError(f"Unsupported file type {path.suffix!r}; supported: {', '.join(sorted(SUPPORTED))}")
    source = source_name(path)
    digest = file_hash(path)
    col = collection(design)
    previous = col.get(where={"source": source}, include=["metadatas"])
    if previous["ids"]:
        old_hashes = {m.get("sha256") for m in previous["metadatas"]}
        if old_hashes == {digest}:
            return {"status": "unchanged", "source": source, "chunks": len(previous["ids"]), "embedded": 0}
        col.delete(ids=previous["ids"])
    chunks = chunk_file(path, design, source)
    if not chunks:
        raise ValueError(f"No text could be extracted from {path.name}")
    embedded = embed_and_store(chunks, design, {"sha256": digest, "path": str(path)})
    return {"status": "replaced" if previous["ids"] else "added", "source": source,
            "chunks": len(chunks), "embedded": embedded, "words": sum(c["words"] for c in chunks)}


# ---------------------------------------------------------------------------
# Search
# ---------------------------------------------------------------------------

def _query_key(query: str) -> str:
    # "v2": entries written before the one-Content-per-text fix are ignored.
    return f"v2|{EMBED_MODEL}|{EMBED_DIM}|{query}"


def embed_query(query: str) -> list[float]:
    """Query vectors are cached in index/ so repeated evaluations spend no quota."""
    cache = json.loads(QUERY_CACHE.read_text()) if QUERY_CACHE.exists() else {}
    key = _query_key(query)
    if key not in cache:
        cache[key] = embed_texts([query], task="RETRIEVAL_QUERY")[0]
        QUERY_CACHE.write_text(json.dumps(cache))
    return cache[key]


def warm_query_cache(queries: list[str]) -> int:
    """Embed the test questions in advance, so search on them needs no API call
    (check.py starts the server without the key in its environment)."""
    cache = json.loads(QUERY_CACHE.read_text()) if QUERY_CACHE.exists() else {}
    todo = list(dict.fromkeys(q for q in queries if _query_key(q) not in cache))
    for i in range(0, len(todo), EMBED_BATCH):
        batch = todo[i:i + EMBED_BATCH]
        for q, v in zip(batch, embed_texts(batch, task="RETRIEVAL_QUERY")):
            cache[_query_key(q)] = v
        QUERY_CACHE.write_text(json.dumps(cache))
    return len(todo)


_bm25_cache: dict[str, dict] = {}


def _tokens(text: str) -> list[str]:
    return re.findall(r"\w+", text.lower())


def _bm25_scores(query: str, design: str) -> dict[str, float]:
    if design not in _bm25_cache:
        data = collection(design).get(include=["documents"])
        docs = [Counter(_tokens(d)) for d in data["documents"]]
        df = Counter(t for d in docs for t in d)
        lengths = [sum(d.values()) for d in docs]
        _bm25_cache[design] = {"ids": data["ids"], "docs": docs, "df": df, "len": lengths,
                               "avg": (sum(lengths) / len(lengths)) if lengths else 1}
    b = _bm25_cache[design]
    n, k1, bb = len(b["docs"]), 1.5, 0.75
    scores = {}
    for doc_id, doc, length in zip(b["ids"], b["docs"], b["len"]):
        s = 0.0
        for t in set(_tokens(query)):
            if t in doc:
                idf = math.log(1 + (n - b["df"][t] + 0.5) / (b["df"][t] + 0.5))
                s += idf * doc[t] * (k1 + 1) / (doc[t] + k1 * (1 - bb + bb * length / b["avg"]))
        if s:
            scores[doc_id] = s
    return scores


def search(query: str, k: int = DEFAULT_K, design: str = DEFAULT_DESIGN, mode: str = DEFAULT_MODE,
           source: str | list[str] | None = None) -> list[dict]:
    """Top-k chunks: [{"id", "text", "source", "location", "score"}].
    Optional filter: one source name, or a list of names."""
    col = collection(design)
    if isinstance(source, list):
        where = {"source": {"$in": source}}
    else:
        where = {"source": source} if source else None
    pool = k if mode == "vector" else max(4 * k, 20)
    result = col.query(query_embeddings=[embed_query(query)], n_results=pool, where=where,
                       include=["documents", "metadatas", "distances"])
    hits = {i: {"id": i, "text": d, "source": m["source"], "location": m["location"], "score": 1 - dist}
            for i, d, m, dist in zip(result["ids"][0], result["documents"][0],
                                      result["metadatas"][0], result["distances"][0])}
    if mode == "vector":
        return list(hits.values())[:k]
    if mode != "hybrid":
        raise ValueError(f"Unknown search mode {mode!r}")
    # Reciprocal rank fusion of the vector ranking and a BM25 ranking.
    bm25 = _bm25_scores(query, design)
    if source:
        allowed = set(col.get(where=where, include=[])["ids"])
        bm25 = {i: s for i, s in bm25.items() if i in allowed}
    bm25_rank = sorted(bm25, key=bm25.get, reverse=True)[:pool]
    fused = Counter()
    for rank, i in enumerate(hits):
        fused[i] += 1 / (60 + rank)
    for rank, i in enumerate(bm25_rank):
        fused[i] += 1 / (60 + rank)
    missing = [i for i in bm25_rank if i not in hits]
    if missing:
        extra = col.get(ids=missing, include=["documents", "metadatas"])
        for i, d, m in zip(extra["ids"], extra["documents"], extra["metadatas"]):
            hits[i] = {"id": i, "text": d, "source": m["source"], "location": m["location"], "score": 0.0}
    out = []
    for i, score in fused.most_common(k):
        out.append({**hits[i], "score": round(score, 4)})
    return out


# ---------------------------------------------------------------------------
# main.py index
# ---------------------------------------------------------------------------

def main() -> int:
    if not SOURCES and not any(CORPUS_DIR.glob("*")):
        log("No documents yet: fill in SOURCES in index.py (or put files in corpus/).")
        return 1
    download_corpus()
    files = sorted(p for p in CORPUS_DIR.iterdir() if p.suffix.lower() in SUPPORTED)
    manifest = {"embed_model": EMBED_MODEL, "dim": EMBED_DIM, "default_design": DEFAULT_DESIGN,
                "documents": [], "designs": {}}   # designs: only fully embedded ones
    all_chunks = {design: [] for design in DESIGNS}
    for path in files:
        blocks = extract(path)
        words = sum(len(b["text"].split()) for b in blocks)
        meta = next((s for s in SOURCES if _filename(s) == path.name), {})
        manifest["documents"].append({"source": source_name(path), "file": path.name, "words": words,
                                      "url": meta.get("url", ""), "licence": meta.get("licence", "")})
        for design in DESIGNS:
            all_chunks[design] += chunk_blocks(blocks, source_name(path), design)
    total_words = sum(d["words"] for d in manifest["documents"])
    print(f"{len(files)} documents, {total_words:,} words")
    for d in manifest["documents"]:
        print(f"  {d['source']:<30} {d['words']:>8,} words")

    # Default design first, so the served index is complete before the others.
    order = [DEFAULT_DESIGN] + [d for d in DESIGNS if d != DEFAULT_DESIGN]
    try:
        questions_csv = ROOT / "eval" / "questions.csv"
        if questions_csv.exists():
            import csv
            with questions_csv.open(newline="", encoding="utf-8") as f:
                questions = [r["question"].strip() for r in csv.DictReader(f) if (r.get("question") or "").strip()]
            print(f"Test questions: {warm_query_cache(questions)} newly embedded for the query cache")
        for design in order:
            chunks = all_chunks[design]
            embedded = embed_and_store(chunks, design)
            manifest["designs"][design] = {"chunks": len(chunks), **DESIGNS[design],
                                           "mean_words": round(sum(c["words"] for c in chunks) / max(len(chunks), 1))}
            print(f"[{design}] {len(chunks)} chunks ({embedded} newly embedded)")
    except QuotaExhausted:
        print("Daily embedding quota reached. Everything embedded so far is saved; "
              "run `main.py index` again after the reset to continue.")
        return 1
    finally:
        MANIFEST.write_text(json.dumps(manifest, indent=2))
    return 0


if __name__ == "__main__":
    sys.exit(main())
