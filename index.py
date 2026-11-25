"""
Assignment 3: build the index (`uv run python main.py index`).

Corpus: NTSB aircraft accident reports (US government works, public domain).
Pipeline per file: extract pages -> clean -> chunk (two designs) -> embed with
Gemini -> store in ChromaDB under index/.

Embedding is resumable: every chunk id is a hash of its text, each batch is
written to ChromaDB as soon as Gemini returns it, and chunks that already have
a stored vector are skipped. If the free-tier daily quota runs out, the run
stops cleanly; run it again after the reset (09:00 in Spain) to finish.

server.py imports `index_file`, `search`, `load_registry` and friends from here.
"""

from __future__ import annotations

import hashlib
import json
import logging
import os
import re
import sys
import time
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import httpx
import numpy as np
import pypdf

from api_key import load_api_key

logging.getLogger("pypdf").setLevel(logging.ERROR)  # "Rotated text discovered" on every figure page

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"
CHROMA_DIR = INDEX_DIR / "chroma"
REGISTRY = INDEX_DIR / "documents.json"
QUERY_CACHE = INDEX_DIR / "query_cache.json"

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768
BATCH = 20                 # texts per embed request (each text counts against the daily quota)
CHUNK_WORDS = 350          # target chunk size for both designs
OVERLAP_WORDS = 50         # overlap for the fixed-window design

DESIGNS = ("fixed", "sections")
CHOSEN_DESIGN = "sections"  # set from the retrieval comparison in evaluate.py (see REPORT.md)

# The base corpus: three NTSB reports on airspeed/energy management, crew
# monitoring and emergency handling. All public domain (17 U.S.C. 105).
CORPUS = [
    {
        "doc_id": "AAR1001",
        "title": "Loss of Control on Approach, Colgan Air Flight 3407, Clarence Center, NY, Feb 12 2009",
        "url": "https://www.ntsb.gov/investigations/AccidentReports/Reports/AAR1001.pdf",
        "date": "2010-02-02",
    },
    {
        "doc_id": "AAR1003",
        "title": "Loss of Thrust in Both Engines After Bird Strikes, US Airways Flight 1549, Hudson River, Jan 15 2009",
        "url": "https://www.ntsb.gov/investigations/AccidentReports/Reports/AAR1003.pdf",
        "date": "2010-05-04",
    },
    {
        "doc_id": "AAR1401",
        "title": "Descent Below Visual Glidepath and Impact With Seawall, Asiana Airlines Flight 214, San Francisco, Jul 6 2013",
        "url": "https://www.ntsb.gov/investigations/AccidentReports/Reports/AAR1401.pdf",
        "date": "2014-06-24",
    },
]
BASE_DOC_IDS = [d["doc_id"] for d in CORPUS]


def log(*args) -> None:
    """Log to stderr: stdout belongs to the MCP protocol when server.py imports us."""
    print(*args, file=sys.stderr, flush=True)


# --------------------------------------------------------------------------- download

def download_corpus() -> list[Path]:
    CORPUS_DIR.mkdir(exist_ok=True)
    paths = []
    for doc in CORPUS:
        path = CORPUS_DIR / f"{doc['doc_id']}.pdf"
        if not path.exists():
            log(f"Downloading {doc['url']}")
            r = httpx.get(doc["url"], follow_redirects=True, timeout=120,
                          headers={"User-Agent": "Mozilla/5.0 (course assignment corpus download)"})
            r.raise_for_status()
            path.write_bytes(r.content)
        paths.append(path)
    return paths


# --------------------------------------------------------------------------- extract & clean

HEADER_RE = re.compile(r"^\s*NTSB\s+Aircraft\s+Accident\s+Report\s*$", re.I)
HEADER_NUM_RE = re.compile(r"^\s*NTSB\s+Aircraft\s+Accident\s+Report\s+(\d{1,3}|[ivxlc]+)\s*$", re.I)
PAGENUM_RE = re.compile(r"^\s*([ivxlc]+|\d{1,3})\s*$", re.I)
DOT_LEADER_RE = re.compile(r"\.{6,}|(?:\. ){5,}")
# Numbered section headings: "1.1 History of Flight", "2.3.1 Monitoring", "3. Conclusions".
HEADING_RE = re.compile(r"^\s{0,12}(\d{1,2}(?:\.\d{1,2}){0,4})\.?\s{1,6}([A-Z][^.!?]{2,90})$")
NAMED_HEADINGS = ("Executive Summary", "Abstract", "Appendix", "Appendixes", "Appendices", "References")
FRONT_MATTER_RE = re.compile(r"^\s*(Contents|Figures|Tables|Abbreviations( and Acronyms)?|Acronyms)\s*$", re.I | re.M)


@dataclass
class Page:
    page: int               # 1-based PDF page (what a PDF viewer shows; used for citations)
    printed: str            # page number printed on the page, if any ("151", "ix", "")
    lines: list[str]
    skip: bool = False      # front matter (contents, list of figures, abbreviations)


def _dehyphenate(text: str) -> str:
    return re.sub(r"(\w)-\n\s*(\w)", r"\1\2", text)


def extract_pages(path: Path) -> list[Page]:
    """Extract every page with pypdf's layout mode.

    Plain mode splits words in these PDFs ("th eir", "adequa te", "go -around");
    layout mode keeps them whole. We then drop running headers and page-number
    lines (remembering the printed number) and flag table-of-contents and
    abbreviation pages so they are not chunked.
    """
    reader = pypdf.PdfReader(str(path))
    pages = []
    for i, p in enumerate(reader.pages):
        raw = p.extract_text(extraction_mode="layout") or ""
        raw = _dehyphenate(raw.replace("­", "").replace("ﬁ", "fi").replace("ﬂ", "fl"))
        lines, printed = [], ""
        for line in raw.splitlines():
            if HEADER_RE.match(line):
                continue
            m = HEADER_NUM_RE.match(line) or PAGENUM_RE.match(line)
            if m:
                printed = m.group(1)
                continue
            lines.append(line.rstrip())
        body = "\n".join(lines)
        skip = len(DOT_LEADER_RE.findall(body)) >= 4 or bool(FRONT_MATTER_RE.search(body[:200]))
        pages.append(Page(page=i + 1, printed=printed, lines=lines, skip=skip))
    # Abbreviation lists run over several pages without a title on each: once a
    # front-matter page is seen, keep skipping until the first real section.
    in_front = False
    for pg in pages:
        text = "\n".join(pg.lines)
        if pg.skip:
            in_front = True
        elif in_front:
            if re.search(r"^\s*(Executive Summary|1\.?\s+Factual Information)", text, re.M):
                in_front = False
            elif pg.page < 25:
                pg.skip = True
    return pages


def _norm(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


@dataclass
class Para:
    text: str
    page: int
    printed: str
    section: str


def paragraphs(pages: list[Page]) -> list[Para]:
    """Split pages into paragraphs (blank-line separated) tagged with page and section."""
    section = "Front matter"
    out: list[Para] = []
    for pg in pages:
        if pg.skip:
            continue
        block: list[str] = []

        def flush():
            t = _norm(" ".join(block))
            if len(t.split()) >= 3:
                out.append(Para(t, pg.page, pg.printed, section))
            block.clear()

        for line in pg.lines:
            s = line.strip()
            if not s:
                flush()
                continue
            h = HEADING_RE.match(line)
            # Named headings after the numbered body. Board Member statements and other parties'
            # comments are NOT NTSB findings, so they must get their own section label.
            if (h and len(s.split()) <= 12 and not s.endswith((",", ";"))) or s in NAMED_HEADINGS \
                    or re.match(r"^Appendix [A-Z]\b", s) or re.match(r"^Board Member Statements?$", s) \
                    or re.match(r"^COMMENTS OF THE\b", s):
                flush()
                section = _norm(s)
                continue
            block.append(s)
        flush()
    return out


# --------------------------------------------------------------------------- chunking

@dataclass
class Chunk:
    doc_id: str
    design: str
    text: str               # what the reader sees
    page_start: int
    page_end: int
    printed_start: str
    printed_end: str
    section: str
    meta: dict = field(default_factory=dict)

    @property
    def embed_text(self) -> str:
        # The sections design embeds a short header so a chunk "knows" which report and section it is from.
        if self.design == "sections":
            return f"{self.meta.get('title', self.doc_id)} | {self.section}\n{self.text}"
        return self.text

    @property
    def id(self) -> str:
        h = hashlib.sha1(self.embed_text.encode("utf-8")).hexdigest()[:16]
        return f"{self.doc_id}:{self.design}:{h}"

    def metadata(self) -> dict:
        return {
            "doc_id": self.doc_id, "design": self.design, "section": self.section,
            "page_start": self.page_start, "page_end": self.page_end,
            "printed_start": self.printed_start, "printed_end": self.printed_end,
            "title": self.meta.get("title", ""), "words": len(self.text.split()),
        }


def chunk_fixed(doc_id: str, paras: list[Para], meta: dict) -> list[Chunk]:
    """Design A: sliding windows of CHUNK_WORDS words with OVERLAP_WORDS overlap, ignoring structure."""
    words: list[tuple[str, Para]] = [(w, p) for p in paras for w in p.text.split()]
    step = CHUNK_WORDS - OVERLAP_WORDS
    chunks = []
    for start in range(0, max(len(words) - OVERLAP_WORDS, 1), step):
        window = words[start:start + CHUNK_WORDS]
        if not window:
            break
        first, last = window[0][1], window[-1][1]
        chunks.append(Chunk(doc_id, "fixed", " ".join(w for w, _ in window), first.page, last.page,
                            first.printed, last.printed, first.section, meta))
    return chunks


def chunk_sections(doc_id: str, paras: list[Para], meta: dict) -> list[Chunk]:
    """Design B: never cross a section heading; pack whole paragraphs up to CHUNK_WORDS.

    A paragraph longer than the limit is split at sentence ends. Findings and
    recommendations, which are short numbered paragraphs, stay whole. Each
    chunk is embedded with a "report title | section" header.
    """
    chunks: list[Chunk] = []
    buf: list[Para] = []

    def emit():
        if buf:
            text = " ".join(p.text for p in buf)
            chunks.append(Chunk(doc_id, "sections", text, buf[0].page, buf[-1].page,
                                buf[0].printed, buf[-1].printed, buf[0].section, meta))
            buf.clear()

    def pieces(p: Para):
        if len(p.text.split()) <= CHUNK_WORDS:
            yield p
            return
        sents = re.split(r"(?<=[.;:])\s+(?=[A-Z(“\"0-9])", p.text)
        cur: list[str] = []
        for s in sents:
            if cur and len(" ".join(cur + [s]).split()) > CHUNK_WORDS:
                yield Para(" ".join(cur), p.page, p.printed, p.section)
                cur = []
            cur.append(s)
        if cur:
            yield Para(" ".join(cur), p.page, p.printed, p.section)

    for para in paras:
        for p in pieces(para):
            size = sum(len(b.text.split()) for b in buf)
            if buf and (p.section != buf[0].section or size + len(p.text.split()) > CHUNK_WORDS):
                emit()
            buf.append(p)
    emit()
    # Tiny chunks (< 40 words: a section's last sentence, a stray heading) are merged into
    # the neighbour from the same section; tiny orphans under 15 words are dropped.
    merged: list[Chunk] = []
    for c in chunks:
        small = len(c.text.split()) < 40
        if small and merged and merged[-1].section == c.section:
            prev = merged.pop()
            c = Chunk(doc_id, "sections", prev.text + " " + c.text, prev.page_start, c.page_end,
                      prev.printed_start, c.printed_end, c.section, meta)
        elif merged and len(merged[-1].text.split()) < 40 and merged[-1].section == c.section:
            prev = merged.pop()
            c = Chunk(doc_id, "sections", prev.text + " " + c.text, prev.page_start, c.page_end,
                      prev.printed_start, c.printed_end, c.section, meta)
        merged.append(c)
    return [c for c in merged if len(c.text.split()) >= 15]


def chunk_file(path: Path, doc_id: str | None = None, title: str | None = None) -> dict[str, list[Chunk]]:
    """Extract, clean and chunk one PDF with both designs. Returns {design: [chunks]}."""
    path = Path(path)
    doc_id = doc_id or path.stem.upper()
    meta = {"title": title or doc_id}
    paras = paragraphs(extract_pages(path))
    return {"fixed": chunk_fixed(doc_id, paras, meta), "sections": chunk_sections(doc_id, paras, meta)}


# --------------------------------------------------------------------------- embedding

class QuotaExhausted(RuntimeError):
    pass


_client = None


def client():
    global _client
    if _client is None:
        from google import genai
        _client = genai.Client(api_key=load_api_key())
    return _client


def _embed_call(texts: list[str], task: str) -> np.ndarray:
    """Embed a batch. Each text must be its own Content: gemini-embedding-2 merges a
    plain list of strings into ONE multimodal input and returns a single vector."""
    from google.genai import types, errors
    contents = [types.Content(parts=[types.Part(text=t)]) for t in texts]
    cfg = types.EmbedContentConfig(task_type=task, output_dimensionality=EMBED_DIM)
    for attempt in range(6):
        try:
            r = client().models.embed_content(model=EMBED_MODEL, contents=contents, config=cfg)
            v = np.array([e.values for e in r.embeddings], dtype=np.float32)
            assert v.shape[0] == len(texts), f"asked for {len(texts)} vectors, got {v.shape[0]}"
            return v / np.linalg.norm(v, axis=1, keepdims=True)
        except errors.ClientError as e:
            msg = str(e)
            if getattr(e, "code", None) != 429:
                raise
            if "PerDay" in msg or "per day" in msg.lower():
                raise QuotaExhausted(msg[:300]) from e
            wait = 20 * (attempt + 1)
            m = re.search(r"retry in ([\d.]+)s|'retryDelay': '(\d+)s'", msg)
            if m:
                wait = float(m.group(1) or m.group(2)) + 2
            log(f"  rate limited, waiting {wait:.0f}s")
            time.sleep(wait)
    raise QuotaExhausted("still rate limited after 6 retries")


def embed_query(text: str) -> np.ndarray:
    """Embed a search query, cached on disk so repeated questions cost no quota."""
    cache = json.loads(QUERY_CACHE.read_text()) if QUERY_CACHE.exists() else {}
    key = hashlib.sha1(text.strip().encode("utf-8")).hexdigest()
    if key not in cache:
        cache[key] = _embed_call([text.strip()], "RETRIEVAL_QUERY")[0].round(6).tolist()
        QUERY_CACHE.write_text(json.dumps(cache))
    return np.array(cache[key], dtype=np.float32)


# --------------------------------------------------------------------------- storage

_chroma = None


def collection(design: str):
    global _chroma
    import chromadb
    if _chroma is None:
        CHROMA_DIR.mkdir(parents=True, exist_ok=True)
        _chroma = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return _chroma.get_or_create_collection(design, metadata={"hnsw:space": "cosine"})


def embed_and_store(chunks: list[Chunk]) -> tuple[int, int]:
    """Embed only chunks without a stored vector and write each batch straight away.

    Returns (newly embedded, already stored). Raises QuotaExhausted with progress saved.
    """
    if not chunks:
        return 0, 0
    col = collection(chunks[0].design)
    ids = [c.id for c in chunks]
    have = set()
    for i in range(0, len(ids), 500):
        have.update(col.get(ids=ids[i:i + 500], include=[])["ids"])
    todo = [c for c in chunks if c.id not in have]
    done = 0
    for i in range(0, len(todo), BATCH):
        batch = todo[i:i + BATCH]
        vecs = _embed_call([c.embed_text for c in batch], "RETRIEVAL_DOCUMENT")
        col.upsert(ids=[c.id for c in batch], embeddings=vecs.tolist(),
                   documents=[c.text for c in batch], metadatas=[c.metadata() for c in batch])
        done += len(batch)
        log(f"  {chunks[0].doc_id}/{chunks[0].design}: {len(have) + done}/{len(chunks)} stored")
    return done, len(have)


def prune(doc_id: str, design: str, keep_ids: set[str]) -> int:
    """Delete stored chunks of this document that the current chunker no longer produces."""
    col = collection(design)
    stale = [i for i in col.get(where={"doc_id": doc_id}, include=[])["ids"] if i not in keep_ids]
    if stale:
        col.delete(ids=stale)
    return len(stale)


# --------------------------------------------------------------------------- registry

def load_registry() -> dict:
    return json.loads(REGISTRY.read_text()) if REGISTRY.exists() else {}


def save_registry(reg: dict) -> None:
    INDEX_DIR.mkdir(exist_ok=True)
    REGISTRY.write_text(json.dumps(reg, indent=2))


def file_sha256(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def index_file(path: Path, doc_id: str | None = None, title: str | None = None,
               designs: tuple[str, ...] = DESIGNS, meta: dict | None = None) -> dict:
    """Run one file through the whole pipeline and record it in the registry.

    Returns a summary. Raises QuotaExhausted if the daily quota runs out (progress is kept).
    """
    path = Path(path)
    doc_id = doc_id or path.stem.upper()
    chunks_by_design = chunk_file(path, doc_id, title)
    summary = {"doc_id": doc_id, "designs": {}}
    reg = load_registry()
    entry = reg.get(doc_id, {})
    secs = chunks_by_design["sections"]
    entry.update({"doc_id": doc_id, "title": title or entry.get("title") or doc_id, "file": path.name,
                  "sha256": file_sha256(path), "pages": len(pypdf.PdfReader(str(path)).pages),
                  "words": sum(len(c.text.split()) for c in secs), **(meta or {})})
    entry.setdefault("indexed_at", datetime.now(timezone.utc).isoformat(timespec="seconds"))
    entry.setdefault("complete", {})
    reg[doc_id] = entry
    save_registry(reg)
    try:
        for design in designs:
            chunks = chunks_by_design[design]
            entry[f"chunks_{design}"] = len(chunks)
            entry["complete"][design] = False
            removed = prune(doc_id, design, {c.id for c in chunks})
            new, old = embed_and_store(chunks)
            summary["designs"][design] = {"chunks": len(chunks), "embedded_now": new, "already_stored": old, "pruned": removed}
            entry["complete"][design] = True
    finally:
        reg = load_registry()
        reg[doc_id] = entry
        save_registry(reg)
    return summary


# --------------------------------------------------------------------------- search (used by server.py and evaluate.py)

def search(query: str, k: int = 5, design: str = CHOSEN_DESIGN, doc_ids: list[str] | None = None,
           hybrid: bool = False) -> list[dict]:
    """Return the k best chunks as dicts with text, doc_id, pages, section and score."""
    col = collection(design)
    where = {"doc_id": {"$in": doc_ids}} if doc_ids else None
    qv = embed_query(query)
    n = k if not hybrid else max(30, k)
    res = col.query(query_embeddings=[qv.tolist()], n_results=n, where=where,
                    include=["documents", "metadatas", "distances"])
    hits = [{"id": i, "text": d, **m, "score": round(1 - dist, 4)}
            for i, d, m, dist in zip(res["ids"][0], res["documents"][0], res["metadatas"][0], res["distances"][0])]
    if hybrid:
        hits = _rerank_hybrid(query, hits, col, where, k)
    return hits[:k]


_bm25_cache: dict = {}


def _tokens(t: str) -> list[str]:
    return re.findall(r"[a-z0-9]+(?:-[a-z0-9]+)*", t.lower())


def _rerank_hybrid(query: str, dense_hits: list[dict], col, where, k: int) -> list[dict]:
    """Reciprocal-rank fusion of the dense ranking with a BM25 ranking over all chunks."""
    key = (col.name, col.count(), json.dumps(where, sort_keys=True))
    if key not in _bm25_cache:
        got = col.get(where=where, include=["documents", "metadatas"])
        docs = [_tokens(d) for d in got["documents"]]
        df: dict[str, int] = {}
        for d in docs:
            for t in set(d):
                df[t] = df.get(t, 0) + 1
        avg = sum(map(len, docs)) / max(len(docs), 1)
        _bm25_cache[key] = (got, docs, df, avg)
    got, docs, df, avg = _bm25_cache[key]
    N, q = len(docs), _tokens(query)
    scores = []
    for d in docs:
        tf: dict[str, int] = {}
        for t in d:
            tf[t] = tf.get(t, 0) + 1
        s = 0.0
        for t in q:
            if t in tf:
                idf = np.log(1 + (N - df[t] + 0.5) / (df[t] + 0.5))
                s += idf * tf[t] * 2.2 / (tf[t] + 1.2 * (0.25 + 0.75 * len(d) / avg))
        scores.append(s)
    bm_order = np.argsort(scores)[::-1][:30]
    fused: dict[str, float] = {}
    info: dict[str, dict] = {h["id"]: h for h in dense_hits}
    for r, h in enumerate(dense_hits):
        fused[h["id"]] = fused.get(h["id"], 0) + 1 / (60 + r)
    for r, j in enumerate(bm_order):
        cid = got["ids"][j]
        fused[cid] = fused.get(cid, 0) + 1 / (60 + r)
        info.setdefault(cid, {"id": cid, "text": got["documents"][j], **got["metadatas"][j], "score": None})
    order = sorted(fused, key=fused.get, reverse=True)
    return [info[i] for i in order[:k]]


def citation_tag(h: dict) -> str:
    """The tag the agent copies into its answer: [AAR1001 p.165] or [AAR1001 p.165-166] (PDF pages)."""
    pages = str(h["page_start"]) if h["page_start"] == h["page_end"] else f"{h['page_start']}-{h['page_end']}"
    return f"[{h['doc_id']} p.{pages}]"


BRACKET_RE = re.compile(r"\[([^\[\]]{4,200})\]")
DOC_PAGES_RE = re.compile(r"([A-Z]{3}\d{4})?\s*,?\s*pp?\.?\s*(\d{1,3})(?:\s*[-–]\s*(\d{1,3}))?")


def parse_citations(text: str) -> list[tuple[str, int, int]]:
    """All citation tags in a text, as (doc, first page, last page).

    Accepts the canonical [AAR1001 p.165] and [AAR1001 p.165-166], and the variants
    models write: [AAR1001 p.96, p.100] and [AAR1001 p.96; AAR1401 p.147].
    """
    out = []
    for inner in BRACKET_RE.findall(text):
        if not re.search(r"[A-Z]{3}\d{4}", inner):
            continue
        doc = None
        for d, a, b in DOC_PAGES_RE.findall(inner):
            doc = d or doc
            if doc:
                out.append((doc, int(a), int(b or a)))
    return out


def format_hits(hits: list[dict]) -> str:
    """Render hits: a citation tag, then where it is (section, printed page), then the text."""
    out = []
    for h in hits:
        printed = h.get("printed_start") or ""
        where = f"{h.get('title') or h['doc_id']} | section {h['section']}" + (f" | printed page {printed}" if printed else "")
        out.append(f"{citation_tag(h)}\n({where})\n{h['text']}")
    return "\n\n---\n\n".join(out)


# --------------------------------------------------------------------------- main

def main() -> int:
    paths = download_corpus()
    stopped = None
    designs = (CHOSEN_DESIGN,) + tuple(d for d in DESIGNS if d != CHOSEN_DESIGN)
    # Optional, to spread the work over days: INDEX_DESIGNS=sections uv run python main.py index
    only = [d.strip() for d in os.environ.get("INDEX_DESIGNS", "").split(",") if d.strip()]
    if only:
        designs = tuple(d for d in designs if d in only)
    # Embed the design the server uses for every document first, then the comparison design,
    # so a quota stop leaves a usable index.
    for design in designs:
        for doc, path in zip(CORPUS, paths):
            try:
                s = index_file(path, doc["doc_id"], doc["title"], designs=(design,),
                               meta={"url": doc["url"], "date": doc["date"], "licence": "Public domain (US government work)"})
                log(f"{doc['doc_id']}: {s['designs']}")
            except QuotaExhausted as e:
                stopped = e
                break
        if stopped:
            break
    for design in DESIGNS:
        log(f"collection '{design}': {collection(design).count()} chunks stored")
    if stopped:
        log("\nDaily embedding quota reached. Everything embedded so far is saved in index/.\n"
            "Run `uv run python main.py index` again after the quota resets (09:00 in Spain) to finish.")
    else:
        log("Index complete.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
