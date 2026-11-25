"""
Assignment 3: build the index (`main.py index`).

Corpus: EU merger control texts from EUR-Lex (regulation, notices, guidelines).
Steps per file: extract -> clean -> split into structural units (article,
recital, numbered paragraph) -> chunk (two designs) -> embed with Gemini ->
store in index/.

Every vector is appended to index/vectors.jsonl the moment it arrives, keyed by
a hash of (model, task, text). Re-running embeds only chunks without a saved
vector, so a crash or the free-tier daily limit loses nothing.

server.py's add_document tool imports `add_document()` from here.
"""

from __future__ import annotations

import base64
import hashlib
import json
import re
import shutil
import sys
import time
from dataclasses import dataclass, field
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"          # downloads, git-ignored
ADDED_DIR = ROOT / "added_docs"       # documents added through add_document, committed
INDEX_DIR = ROOT / "index"
VECTORS_FILE = INDEX_DIR / "vectors.jsonl"
CHROMA_DIR = INDEX_DIR / "chroma"
CONFIG_FILE = INDEX_DIR / "config.json"
DOCS_FILE = INDEX_DIR / "documents.json"

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768          # smaller vectors keep index/ well under 90 MB
BATCH = 20

# ---------------------------------------------------------------------------
# Corpus. All EUR-Lex; reuse allowed under Commission Decision 2011/833/EU
# (reuse of Commission documents, attribution required). No personal data.
# ---------------------------------------------------------------------------
EURLEX = "https://eur-lex.europa.eu/legal-content/EN/TXT/{fmt}/?uri=CELEX:{celex}"
DOCS = [
    {"id": "EUMR", "celex": "32004R0139", "date": "2004-01-20",
     "title": "Council Regulation (EC) No 139/2004 on the control of concentrations between undertakings (EU Merger Regulation)"},
    {"id": "JURISDICTIONAL_NOTICE", "celex": "52008XC0416(08)", "date": "2008-04-16",
     "title": "Commission Consolidated Jurisdictional Notice under Regulation (EC) No 139/2004"},
    {"id": "HORIZONTAL_GUIDELINES", "celex": "52004XC0205(02)", "date": "2004-02-05",
     "title": "Guidelines on the assessment of horizontal mergers"},
    {"id": "NONHORIZONTAL_GUIDELINES", "celex": "52008XC1018(03)", "date": "2008-10-18",
     "title": "Guidelines on the assessment of non-horizontal mergers"},
]
# Held back on purpose: added later through add_document to answer an
# unanswerable test question (before/after in the evaluation).
HELD_OUT = {"id": "SIMPLIFIED_NOTICE", "celex": "52023XC0505(01)", "date": "2023-05-05",
            "title": "Commission Notice on a simplified treatment for certain concentrations"}
LICENCE = "EUR-Lex, reuse authorised (Commission Decision 2011/833/EU)"


# ---------------------------------------------------------------------------
# Data structures
# ---------------------------------------------------------------------------
@dataclass
class Unit:
    """One structural unit: an article, a recital or a numbered paragraph."""
    source: str
    label: str            # "Article 5", "Recital 12", "para 145", "Preamble"
    section: str          # nearest heading above it
    title: str            # article title, if any
    lines: list[str] = field(default_factory=list)

    @property
    def text(self) -> str:
        return "\n".join(self.lines)

    @property
    def words(self) -> int:
        return len(self.text.split())


@dataclass
class Chunk:
    id: str
    source: str
    location: str         # human readable: "Article 5", "paras 12-14"
    units: list[str]      # every unit label the chunk covers
    section: str
    text: str             # what the reader sees
    embed_text: str       # what gets embedded (may carry a context header)
    added: bool = False

    def meta(self) -> dict:
        return {"source": self.source, "location": self.location, "units": "|".join(self.units),
                "section": self.section, "added": self.added}


# ---------------------------------------------------------------------------
# 1. Download
# ---------------------------------------------------------------------------
def download(doc: dict) -> Path:
    """Fetch the document into corpus/. Tries the Publications Office (Cellar)
    endpoint first, which serves the same EUR-Lex texts to scripts, then
    EUR-Lex itself, which often answers scripts with an empty anti-bot page.
    A file you put in corpus/<id>.html or corpus/<id>.pdf by hand is used as is."""
    import io
    import zipfile
    import httpx

    CORPUS_DIR.mkdir(exist_ok=True)
    for ext in ("html", "pdf"):
        p = CORPUS_DIR / f"{doc['id']}.{ext}"
        if p.exists() and p.stat().st_size > 1_000:
            return p
    ua = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 14_0) AppleWebKit/605.1.15 "
          "(KHTML, like Gecko) Version/17.0 Safari/605.1.15")
    from urllib.parse import quote
    cellar = f"https://publications.europa.eu/resource/celex/{doc['celex']}"
    cellar_enc = f"https://publications.europa.eu/resource/celex/{quote(doc['celex'], safe='')}"
    xhtml = {"Accept": "application/xhtml+xml, text/html;q=0.9", "Accept-Language": "eng"}
    pdf = {"Accept": "application/pdf", "Accept-Language": "eng"}
    attempts = [
        ("Cellar XHTML", cellar, xhtml, "html"),
        ("Cellar XHTML (encoded id)", cellar_enc, xhtml, "html"),
        ("Cellar PDF", cellar, pdf, "pdf"),
        ("Cellar PDF (encoded id)", cellar_enc, pdf, "pdf"),
        ("EUR-Lex HTML", EURLEX.format(fmt="HTML", celex=doc["celex"]), {"Accept-Language": "en"}, "html"),
        ("EUR-Lex PDF", EURLEX.format(fmt="PDF", celex=doc["celex"]), {"Accept-Language": "en"}, "pdf"),
    ]
    tried = set()
    for name, url, headers, ext in attempts:
        if (url, headers["Accept-Language"], ext) in tried:
            continue
        tried.add((url, headers["Accept-Language"], ext))
        try:
            r = httpx.get(url, headers={"User-Agent": ua, **headers}, follow_redirects=True, timeout=90)
        except httpx.HTTPError as e:
            log(f"  {doc['id']}: {name} failed ({type(e).__name__})")
            continue
        body = r.content
        if body[:2] == b"PK":  # Cellar sometimes wraps the manifestation in a zip
            with zipfile.ZipFile(io.BytesIO(body)) as z:
                names = [n for n in z.namelist() if n.lower().endswith((".html", ".xhtml", ".htm", ".pdf"))]
                if names:
                    body = z.read(names[0])
                    ext = "pdf" if names[0].lower().endswith(".pdf") else "html"
        good = (body[:4] == b"%PDF") if ext == "pdf" else (b"Article" in body or b"(1)" in body)
        if r.status_code == 200 and good and len(body) > 5_000:
            p = CORPUS_DIR / f"{doc['id']}.{ext}"
            p.write_bytes(body)
            log(f"  {doc['id']}: {name} ok ({len(body) // 1024} KB)")
            return p
        log(f"  {doc['id']}: {name} gave HTTP {r.status_code}, {len(body)} bytes")
    raise SystemExit(
        f"Could not download {doc['id']}. Open {EURLEX.format(fmt='HTML', celex=doc['celex'])} in Safari, "
        f"File > Save As, format 'Page Source', save it as corpus/{doc['id']}.html, then run again.")


# ---------------------------------------------------------------------------
# 2. Extract to clean lines
# ---------------------------------------------------------------------------
# Footnote bodies. In HTML they are removed by tag before this; in PDFs they
# sit at the page bottom as "(12) OJ L 24, ..." or "(12) Case T-102/96 ...".
FOOTNOTE_LINE = re.compile(r"^\(\s*\d{1,3}\s*\)\s+(OJ [LC]\b|Case[s]? [CT]-|Judgment of|Ibid|See also)")
PAGE_FURNITURE = re.compile(r"^(Official Journal of the European Union|EN|\d{1,2}\.\d{1,2}\.\d{4}|C \d+/\d+|L \d+/\d+|\d+)$")


def extract_html(path: Path) -> list[str]:
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(path.read_bytes(), "html.parser")
    for tag in soup(["script", "style", "nav", "header", "footer"]):
        tag.decompose()
    # Fix: footnote references glued to words ("undertakings (1)") and the
    # footnote bodies at the end. EUR-Lex marks both; drop them before text.
    for tag in soup.select("a[href^='#ntr'], a[href^='#ntc'], span.oj-note-tag, span.oj-super, sup, "
                           "p.note, p.oj-note, dl.note"):
        tag.decompose()
    # Fix: numbered points sit in two-cell tables ("(a)" | text); join each row
    # into one line instead of two orphan lines.
    for tr in soup.find_all("tr"):
        cells = [c.get_text(" ", strip=True) for c in tr.find_all(["td", "th"], recursive=False)]
        tr.replace_with(soup.new_string("\n" + " ".join(c for c in cells if c) + "\n"))
    body = soup.find(id="document1") or soup.find(id="TexteOnly") or soup.body or soup
    text = body.get_text("\n")
    return clean_lines(text.splitlines())


def extract_pdf(path: Path) -> list[str]:
    from pypdf import PdfReader

    lines = []
    for page in PdfReader(str(path)).pages:
        lines.extend((page.extract_text() or "").splitlines())
    # Fix: words hyphenated across PDF lines ("under-\ntakings").
    joined = []
    for ln in lines:
        if joined and joined[-1].endswith("-") and ln[:1].islower():
            joined[-1] = joined[-1][:-1] + ln
        else:
            joined.append(ln)
    return clean_lines(joined)


def extract_text_file(path: Path) -> list[str]:
    return clean_lines(path.read_text(encoding="utf-8", errors="replace").splitlines())


def clean_lines(raw: list[str]) -> list[str]:
    out = []
    for ln in raw:
        ln = re.sub(r"\s+", " ", ln.replace("\xa0", " ")).strip()
        # Fix: footnote numbers glued to a word ("Commission(1)", "undertakings(4)").
        # Only after a letter, so legal references like "Article 4(1)" stay.
        ln = re.sub(r"(?<=[A-Za-z])\(\d{1,2}\)", "", ln)
        if not ln or PAGE_FURNITURE.match(ln) or FOOTNOTE_LINE.match(ln):
            continue
        # a lone "(a)" / "1." left on its own line: glue to the next line
        if out and re.fullmatch(r"\(?[0-9a-z]{1,3}[.)]", out[-1]) :
            out[-1] = f"{out[-1]} {ln}"
            continue
        out.append(ln)
    return out


def extract(path: Path) -> list[str]:
    suffix = path.suffix.lower()
    if suffix in (".html", ".htm"):
        return extract_html(path)
    if suffix == ".pdf":
        return extract_pdf(path)
    if suffix in (".txt", ".md"):
        return extract_text_file(path)
    raise ValueError(f"Unsupported file type: {path.suffix} (use .html, .pdf, .txt or .md)")


# ---------------------------------------------------------------------------
# 3. Split into structural units
# ---------------------------------------------------------------------------
ARTICLE = re.compile(r"^Article\s+(\d+[a-z]?)$", re.I)
NUMBERED = re.compile(r"^\(?(\d{1,3})\)?[.)]?\s+(.+)$")
HEADING = re.compile(r"^((?:[IVX]+|[A-Z]|\d+(?:\.\d+)*)[.)]\s+.+|ANNEX.*|CHAPTER\s+\w+.*|[A-Z][A-Z ,'\-()]{6,}[A-Z)])$")
END_MARKERS = ("Done at Brussels", "For the Council", "For the Commission")


def to_units(lines: list[str], source: str) -> list[Unit]:
    """Walk the lines once and cut them into articles, recitals and numbered
    paragraphs. Paragraph numbers must run in sequence (n+1), which keeps list
    items and leftover footnotes from being taken as new paragraphs."""
    units: list[Unit] = [Unit(source, "Preamble", "", "")]
    section, mode, last_num = "", "para", 0
    pending_title = False
    for ln in lines:
        if any(ln.startswith(m) for m in END_MARKERS):
            mode = "end"
        if mode == "end" and not ln.upper().startswith("ANNEX"):
            continue
        if ln.upper().startswith("ANNEX"):
            mode, section = "annex", ln
            units.append(Unit(source, "Annex", section, ""))
            continue
        if ln.startswith("HAS ADOPTED THIS REGULATION") or ln.startswith("HAS ADOPTED THIS"):
            mode = "article"
            continue
        m = ARTICLE.match(ln)
        if m:
            mode = "article"
            units.append(Unit(source, f"Article {m.group(1)}", section, ""))
            pending_title = True
            continue
        if pending_title:  # line right after "Article 5" is its title
            pending_title = False
            if len(ln.split()) <= 14 and not ln.endswith("."):
                units[-1].title = ln
                continue
        if mode != "article" and mode != "annex":
            m = NUMBERED.match(ln)
            # Fix: some notices end with their footnote list as plain text
            # ("(1) Council Regulation ...", "(89) Commission Decision ...").
            # Numbering restarting at (1) after the real paragraphs marks it.
            if m and ln.startswith("(1)") and last_num > 5:
                mode = "end"
                continue
            if m and int(m.group(1)) == last_num + 1:
                rest = m.group(2)
                is_heading = len(rest.split()) <= 12 and not rest.rstrip().endswith((".", ":", ";"))
                if not is_heading:
                    last_num += 1
                    # in a regulation the numbered block before the articles is the recitals
                    label = f"Recital {last_num}" if source_is_regulation(units) else f"para {last_num}"
                    units.append(Unit(source, label, section, "", [ln]))
                    continue
        if HEADING.match(ln) and len(ln.split()) <= 15 and not ln.endswith("."):
            section = ln
            if mode == "article":
                units[-1].lines.append(ln)
            continue
        units[-1].lines.append(ln)
    return [u for u in units if u.words > 0]


def source_is_regulation(units: list[Unit]) -> bool:
    pre = " ".join(units[0].lines[:40]).upper()
    return "REGULATION" in pre and ("HAVING REGARD" in pre or "WHEREAS" in pre)


# ---------------------------------------------------------------------------
# 4. Chunk: two designs
# ---------------------------------------------------------------------------
DESIGNS = ("fixed", "structure")


def location_of(labels: list[str]) -> str:
    """["para 12","para 13","para 14"] -> "paras 12-14"; mixed -> first-last."""
    if len(labels) == 1:
        return labels[0]
    kinds = {l.rsplit(" ", 1)[0] for l in labels}
    if len(kinds) == 1 and all(l.rsplit(" ", 1)[1].isdigit() for l in labels):
        kind = kinds.pop()
        nums = [l.rsplit(" ", 1)[1] for l in labels]
        plural = {"para": "paras", "Recital": "Recitals", "Article": "Articles"}.get(kind, kind)
        return f"{plural} {nums[0]}-{nums[-1]}"
    return f"{labels[0]} to {labels[-1]}"


def chunk_fixed(units: list[Unit], size: int = 250, overlap: int = 50) -> list[Chunk]:
    """Design A: fixed windows of `size` words, ignoring structure. Metadata
    still records which units each window touches."""
    words, owner = [], []
    for u in units:
        for w in u.text.split():
            words.append(w)
            owner.append(u)
    chunks, start, n = [], 0, 0
    while start < len(words):
        end = min(start + size, len(words))
        covered = list(dict.fromkeys(o.label for o in owner[start:end]))
        text = " ".join(words[start:end])
        src = units[0].source
        chunks.append(Chunk(f"{src}:fixed:{n}", src, location_of(covered), covered,
                            owner[start].section, text, text))
        n += 1
        if end == len(words):
            break
        start = end - overlap
    return chunks


def chunk_structure(units: list[Unit], target: int = 300, max_words: int = 450) -> list[Chunk]:
    """Design B: never cut inside a short unit. Pack consecutive units of the
    same section up to `target` words; split a unit longer than `max_words`
    into overlapping pieces. Each chunk is embedded with a header naming the
    document, section and article title."""
    chunks: list[Chunk] = []
    src = units[0].source if units else "?"
    title = doc_title(src)

    def emit(group: list[Unit], text: str, part: str = ""):
        labels = [g.label for g in group]
        loc = location_of(labels) + part
        head_bits = [title, group[0].section, (f"{group[0].label} {group[0].title}".strip() if group[0].title else "")]
        header = " | ".join(b for b in head_bits if b)
        chunks.append(Chunk(f"{src}:structure:{len(chunks)}", src, loc, labels, group[0].section,
                            text, f"{header}\n{text}"))

    group: list[Unit] = []
    for u in units:
        if u.words > max_words:
            if group:
                emit(group, "\n".join(g.text for g in group)); group = []
            w = u.text.split()
            step = target - 50
            for i, s in enumerate(range(0, len(w), step)):
                emit([u], " ".join(w[s:s + target]), f" (part {i + 1})")
                if s + target >= len(w):
                    break
            continue
        kind = lambda x: x.label.rsplit(" ", 1)[0]
        same_section = not group or (group[0].section == u.section and kind(group[0]) == kind(u))
        if group and (sum(g.words for g in group) + u.words > target or not same_section):
            emit(group, "\n".join(g.text for g in group)); group = []
        group.append(u)
    if group:
        emit(group, "\n".join(g.text for g in group))
    return chunks


CHUNKERS = {"fixed": chunk_fixed, "structure": chunk_structure}


def doc_title(source: str) -> str:
    for d in DOCS + [HELD_OUT]:
        if d["id"] == source:
            return d["title"]
    return source


def source_id_for(path: Path) -> str:
    """Corpus files are named <ID>.html; anything else gets an id from its name."""
    stem = path.stem.upper()
    return re.sub(r"[^A-Z0-9_]+", "_", stem).strip("_") or "DOC"


def chunk_file(path: Path, design: str = "structure", source: str | None = None) -> list[Chunk]:
    source = source or source_id_for(path)
    units = to_units(extract(path), source)
    return CHUNKERS[design](units)


# ---------------------------------------------------------------------------
# 5. Embed, with a vector cache saved as we go
# ---------------------------------------------------------------------------
class DailyQuotaExceeded(RuntimeError):
    pass


def _key(text: str, task: str) -> str:
    return hashlib.sha256(f"{EMBED_MODEL}|{EMBED_DIM}|{task}|{text}".encode()).hexdigest()


def _enc(v: np.ndarray) -> str:
    return base64.b64encode(v.astype(np.float32).tobytes()).decode()


def _dec(s: str) -> np.ndarray:
    return np.frombuffer(base64.b64decode(s), dtype=np.float32)


_cache: dict[str, np.ndarray] | None = None


def load_vectors() -> dict[str, np.ndarray]:
    global _cache
    if _cache is None:
        _cache = {}
        if VECTORS_FILE.exists():
            for line in VECTORS_FILE.read_text().splitlines():
                if line.strip():
                    rec = json.loads(line)
                    _cache[rec["k"]] = _dec(rec["v"])
    return _cache


def _client():
    from google import genai
    from api_key import load_api_key
    return genai.Client(api_key=load_api_key())


def _embed_call(client, texts: list[str], task: str) -> list[np.ndarray]:
    from google.genai import types, errors

    cfg = types.EmbedContentConfig(task_type=task, output_dimensionality=EMBED_DIM)
    for attempt in range(6):
        try:
            res = client.models.embed_content(model=EMBED_MODEL, contents=texts, config=cfg)
            vecs = [np.array(e.values, dtype=np.float32) for e in res.embeddings]
            if len(vecs) != len(texts):  # model merged the batch: go one by one
                vecs = [np.array(client.models.embed_content(model=EMBED_MODEL, contents=t, config=cfg)
                                 .embeddings[0].values, dtype=np.float32) for t in texts]
            return [v / (np.linalg.norm(v) or 1.0) for v in vecs]
        except errors.ClientError as e:
            msg = str(e)
            if e.code == 429:
                if re.search(r"PerDay|per.day|per_day", msg, re.I):
                    raise DailyQuotaExceeded(msg) from e
                wait = 15 * (attempt + 1)
                m = re.search(r"retry in ([\d.]+)s|'retryDelay': '(\d+)s'", msg)
                if m:
                    wait = float(m.group(1) or m.group(2)) + 1
                if attempt == 0:
                    log("  Google says: " + re.sub(r"\s+", " ", msg)[:600])
                log(f"  rate limited, waiting {wait:.0f}s")
                time.sleep(wait)
                continue
            raise
        except errors.ServerError:
            time.sleep(10 * (attempt + 1))
    raise RuntimeError("Embedding kept failing after 6 attempts.")


def embed_texts(texts: list[str], task: str = "RETRIEVAL_DOCUMENT") -> list[np.ndarray]:
    """Return a vector per text, calling Gemini only for texts not yet saved."""
    cache = load_vectors()
    missing = list(dict.fromkeys(t for t in texts if _key(t, task) not in cache))
    if missing:
        client = _client()
        INDEX_DIR.mkdir(exist_ok=True)
        with VECTORS_FILE.open("a") as f:
            for i in range(0, len(missing), BATCH):
                batch = missing[i:i + BATCH]
                for t, v in zip(batch, _embed_call(client, batch, task)):
                    k = _key(t, task)
                    cache[k] = v
                    f.write(json.dumps({"k": k, "v": _enc(v)}) + "\n")
                    f.flush()
                if task == "RETRIEVAL_DOCUMENT":
                    log(f"  embedded {min(i + BATCH, len(missing))}/{len(missing)}")
    return [cache[_key(t, task)] for t in texts]


def embed_query(query: str) -> np.ndarray:
    return embed_texts([query], task="RETRIEVAL_QUERY")[0]


# ---------------------------------------------------------------------------
# 6. Store: chunks as JSONL (source of truth) + one Chroma collection per design
# ---------------------------------------------------------------------------
def chunks_file(design: str) -> Path:
    return INDEX_DIR / f"chunks_{design}.jsonl"


def read_chunks(design: str) -> list[Chunk]:
    p = chunks_file(design)
    if not p.exists():
        return []
    return [Chunk(**json.loads(l)) for l in p.read_text().splitlines() if l.strip()]


def write_chunks(design: str, chunks: list[Chunk]) -> None:
    INDEX_DIR.mkdir(exist_ok=True)
    with chunks_file(design).open("w") as f:
        for c in chunks:
            f.write(json.dumps(c.__dict__, ensure_ascii=False) + "\n")


def chroma_collection(design: str, reset: bool = False):
    import chromadb
    from chromadb.config import Settings

    client = chromadb.PersistentClient(path=str(CHROMA_DIR), settings=Settings(anonymized_telemetry=False))
    if reset:
        try:
            client.delete_collection(design)
        except Exception:
            pass
    return client.get_or_create_collection(design, metadata={"hnsw:space": "cosine"})


def embed_and_store(chunks: list[Chunk], design: str) -> int:
    """Embed (cached) and upsert into the design's Chroma collection. Returns
    how many chunks were stored."""
    if not chunks:
        return 0
    vecs = embed_texts([c.embed_text for c in chunks])
    col = chroma_collection(design)
    for i in range(0, len(chunks), 500):
        part = chunks[i:i + 500]
        col.upsert(ids=[c.id for c in part], embeddings=[v.tolist() for v in vecs[i:i + 500]],
                   documents=[c.text for c in part], metadatas=[c.meta() for c in part])
    return len(chunks)


def read_docs() -> dict:
    return json.loads(DOCS_FILE.read_text()) if DOCS_FILE.exists() else {}


def write_docs(docs: dict) -> None:
    DOCS_FILE.write_text(json.dumps(docs, indent=2, ensure_ascii=False))


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# ---------------------------------------------------------------------------
# add_document: used by server.py and evaluate.py
# ---------------------------------------------------------------------------
def served_design() -> str:
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text()).get("design", "structure")
    return "structure"


def add_document(path: str | Path, design: str | None = None) -> dict:
    """Run one file through the pipeline and add it to the served index.

    Already indexed (same source id, same bytes): nothing is embedded or
    changed. Same source id with different bytes: treated as a new version,
    the old chunks are removed and the new ones stored.
    """
    path = Path(path).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"No file at {path}")
    design = design or served_design()
    source = source_id_for(path)
    digest = file_hash(path)
    docs = read_docs()
    known = docs.get(source)
    if known and known.get("sha256") == digest:
        return {"status": "already_indexed", "source": source, "chunks": known["chunks"]}

    chunks = chunk_file(path, design, source)
    for c in chunks:
        c.added = True
    if not chunks:
        raise ValueError(f"No text could be extracted from {path.name}")

    existing = [c for c in read_chunks(design) if c.source != source]
    if known:  # new version: drop old chunks from Chroma too
        chroma_collection(design).delete(where={"source": source})
    embed_and_store(chunks, design)
    write_chunks(design, existing + chunks)

    ADDED_DIR.mkdir(exist_ok=True)
    kept = ADDED_DIR / f"{source}{path.suffix.lower()}"
    if path != kept:
        shutil.copyfile(path, kept)
    docs[source] = {"title": source, "file": str(kept.relative_to(ROOT)), "sha256": digest,
                    "chunks": len(chunks), "words": sum(len(c.text.split()) for c in chunks),
                    "added": True, "design": design}
    write_docs(docs)
    return {"status": "replaced" if known else "added", "source": source, "chunks": len(chunks)}


# ---------------------------------------------------------------------------
# Main: build both designs over the corpus (+ anything previously added)
# ---------------------------------------------------------------------------
def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)


def build() -> None:
    INDEX_DIR.mkdir(exist_ok=True)
    log("1/3 Downloading corpus")
    paths = {d["id"]: download(d) for d in DOCS}

    log("2/3 Chunking")
    docs, per_design = {}, {d: [] for d in DESIGNS}
    for d in DOCS:
        units = to_units(extract(paths[d["id"]]), d["id"])
        words = sum(u.words for u in units)
        docs[d["id"]] = {**d, "url": EURLEX.format(fmt="HTML", celex=d["celex"]), "licence": LICENCE,
                         "file": str(paths[d["id"]].relative_to(ROOT)), "sha256": file_hash(paths[d["id"]]),
                         "words": words, "units": len(units), "added": False}
        for design in DESIGNS:
            per_design[design].extend(CHUNKERS[design](units))
        log(f"  {d['id']:<26} {words:>7,} words  {len(units):>4} units")
    # previously added documents stay in the served design
    old_docs = read_docs()
    for src, info in old_docs.items():
        if info.get("added") and (ROOT / info["file"]).exists():
            chunks = chunk_file(ROOT / info["file"], info.get("design", "structure"), src)
            for c in chunks:
                c.added = True
            per_design[info.get("design", "structure")].extend(chunks)
            docs[src] = info
    total = sum(v["words"] for v in docs.values() if not v.get("added"))
    log(f"  total {total:,} words; chunks: " + ", ".join(f"{k}={len(v)}" for k, v in per_design.items()))

    log("3/3 Embedding (only chunks without a saved vector) and storing")
    for design, chunks in per_design.items():
        write_chunks(design, chunks)
        try:
            chroma_collection(design, reset=True)
            embed_and_store(chunks, design)
        except DailyQuotaExceeded:
            write_docs(docs)
            raise SystemExit("Daily embedding quota reached. Vectors so far are saved in index/vectors.jsonl; "
                             "run `main.py index` again after 09:00 (Spain) to continue.")
        log(f"  {design}: {len(chunks)} chunks stored")
    write_docs(docs)
    if not CONFIG_FILE.exists():
        CONFIG_FILE.write_text(json.dumps({"design": "structure", "hybrid": True}, indent=2))
    log("Done.")


if __name__ == "__main__":
    build()
