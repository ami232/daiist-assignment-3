"""
Assignment 3: ingestion pipeline and vector store. `uv run python main.py index`.

corpus/ -> extract -> clean -> chunk (two designs) -> embed with Gemini -> index/

index/chunks.jsonl   every chunk of every design: source, location, span, text
index/vectors.jsonl  one saved vector per unique chunk text (appended batch by batch)
index/queries.jsonl  saved query vectors, so repeated questions cost no quota
index/docs.json      file name -> content hash and word count (duplicate check)

Only chunks without a saved vector are embedded. server.py and evaluate.py
import this module; nothing here prints to stdout.
"""

from __future__ import annotations

import hashlib
import html
import json
import logging
import math
import re
import shutil
import sys
import time
import unicodedata
from collections import Counter
from dataclasses import dataclass
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"
CHUNKS_FILE = INDEX_DIR / "chunks.jsonl"
VECTORS_FILE = INDEX_DIR / "vectors.jsonl"
QUERIES_FILE = INDEX_DIR / "queries.jsonl"
DOCS_FILE = INDEX_DIR / "docs.json"

# One line on what the documents are; it goes into the search tool's description.
CORPUS_TOPIC = "EU passenger rights law (air, rail, bus and coach, sea) and the Montreal Convention on air carrier liability"

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768          # smaller vectors keep index/ well under 90 MB
BATCH = 50
SUPPORTED = {".pdf", ".txt", ".md", ".html", ".htm"}

DESIGNS = ("fixed", "structure")
# Set these from the table `main.py evaluate` prints (eval/retrieval.csv).
ACTIVE_DESIGN = "structure"
ACTIVE_MODE = "dense"   # "dense" or "hybrid" (dense + BM25, reciprocal rank fusion)
ACTIVE_SCOPE = "articles"  # "all" or "articles" (metadata filter: skip recitals/preamble, see Store.search)
TOP_K = 5

FIXED_WORDS, FIXED_OVERLAP = 150, 30
SECTION_MAX_WORDS, SECTION_OVERLAP, SECTION_MIN_WORDS = 300, 50, 8

log = logging.getLogger("index")
if not log.handlers:
    _h = logging.StreamHandler(sys.stderr)
    _h.setFormatter(logging.Formatter("%(message)s"))
    log.addHandler(_h)
    log.setLevel(logging.INFO)
    log.propagate = False


class QuotaExhausted(RuntimeError):
    """The daily embedding quota is used up; saved vectors are kept."""


# ---------------------------------------------------------------- files

def read_jsonl(path: Path) -> list[dict]:
    if not path.is_file():
        return []
    rows = []
    with path.open(encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line:
                try:
                    rows.append(json.loads(line))
                except json.JSONDecodeError:  # a line cut off by a crash
                    continue
    return rows


def append_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")


def write_jsonl(path: Path, rows: list[dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8") as f:
        for row in rows:
            f.write(json.dumps(row, ensure_ascii=False) + "\n")
    tmp.replace(path)


def read_docs() -> dict:
    return json.loads(DOCS_FILE.read_text(encoding="utf-8")) if DOCS_FILE.is_file() else {}


def write_docs(docs: dict) -> None:
    DOCS_FILE.parent.mkdir(parents=True, exist_ok=True)
    DOCS_FILE.write_text(json.dumps(docs, indent=2, sort_keys=True), encoding="utf-8")


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def sha1(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()


# ---------------------------------------------------------------- extract and clean

def extract(path: Path) -> list[tuple[int | None, str]]:
    """(page number or None, raw text) for each page."""
    ext = path.suffix.lower()
    if ext == ".pdf":
        from pypdf import PdfReader
        return [(i + 1, page.extract_text() or "") for i, page in enumerate(PdfReader(str(path)).pages)]
    raw = path.read_text(encoding="utf-8", errors="replace")
    if ext in (".html", ".htm"):
        raw = re.sub(r"(?is)<(script|style|head|nav|footer)\b.*?</\1>", " ", raw)
        raw = re.sub(r"(?i)<br\s*/?>|</(p|div|h[1-6]|li|tr|section|article|table)>", "\n", raw)
        raw = html.unescape(re.sub(r"<[^>]+>", " ", raw))
    return [(None, raw)]


PAGE_NUMBER = re.compile(r"(page\s*)?\d{1,4}(\s*(/|of)\s*\d{1,4})?", re.I)


def clean_lines(text: str) -> list[str]:
    text = unicodedata.normalize("NFKC", text).replace("­", "")
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)          # words hyphenated across lines
    lines = []
    for line in text.splitlines():
        line = re.sub(r"\s+", " ", line).strip()
        if line and not PAGE_NUMBER.fullmatch(line):
            lines.append(line)
    return lines


HEADING = re.compile(
    r"^(?:(Article|Art\.|Section|Chapter|Annex|Part|Title)\s+([0-9]+[a-z]?|[IVXLC]+)\b|(#{1,4})\s+(.+))",
    re.I,
)


def heading_label(line: str) -> str | None:
    """'Article 5', 'Chapter II', a Markdown heading, or None for body text."""
    if len(line) > 90:
        return None
    m = HEADING.match(line)
    if not m:
        return None
    if m.group(3):
        return m.group(4).strip()
    rest = line[m.end():].strip()
    if re.match(r"^(of|and|to|or|in|shall|may|is|are|\(|,|;)", rest, re.I):
        return None                                        # a reference inside a sentence
    word = "Article" if m.group(1).lower().startswith("art") else m.group(1).capitalize()
    return f"{word} {m.group(2)}"


@dataclass
class Line:
    text: str
    page: int | None
    heading: str | None


def load_document(path: Path) -> list[Line]:
    """Clean lines tagged with page and current section heading."""
    pages = [(p, clean_lines(t)) for p, t in extract(path)]
    repeated: set[str] = set()
    if len(pages) >= 5:                                     # running headers and footers
        counts = Counter(l for _, lines in pages for l in set(lines) if len(l) < 100)
        repeated = {l for l, n in counts.items() if n >= 0.5 * len(pages) and not heading_label(l)}
    out, heading = [], None
    for page, lines in pages:
        for line in lines:
            if line in repeated:
                continue
            heading = heading_label(line) or heading
            out.append(Line(line, page, heading))
    return out


# ---------------------------------------------------------------- chunk

def fmt_location(headings: list, pages: list) -> tuple[str, list[str]]:
    hs = [h for h in dict.fromkeys(headings) if h]
    ps = [p for p in dict.fromkeys(pages) if p]
    parts = []
    if hs:
        parts.append(hs[0] if len(hs) == 1 else f"{hs[0]} to {hs[-1]}")
    if ps:
        parts.append(f"p. {ps[0]}" if len(ps) == 1 else f"pp. {ps[0]}-{ps[-1]}")
    return ", ".join(parts) or "whole document", hs + [f"p. {p}" for p in ps]


def make_chunk(design: str, source: str, text: str, headings: list, pages: list) -> dict:
    location, span = fmt_location(headings, pages)
    embed_text = f"{source} | {location}\n{text}"
    return {
        "id": f"{design}:{sha1(source + text)[:16]}",
        "design": design,
        "source": source,
        "location": location,
        "span": span,
        "text": text,
        "key": sha1(embed_text),
        "embed_text": embed_text,
    }


def chunk_fixed(source: str, lines: list[Line]) -> list[dict]:
    """Design A: 150-word windows, 30 words of overlap, ignoring structure."""
    words = [(w, l.page, l.heading) for l in lines for w in l.text.split()]
    step = FIXED_WORDS - FIXED_OVERLAP
    chunks = []
    for start in range(0, max(len(words) - FIXED_OVERLAP, 1), step):
        piece = words[start:start + FIXED_WORDS]
        if not piece:
            break
        chunks.append(make_chunk("fixed", source, " ".join(w for w, _, _ in piece),
                                 [h for _, _, h in piece], [p for _, p, _ in piece]))
    return chunks


def chunk_structure(source: str, lines: list[Line]) -> list[dict]:
    """Design B: one chunk per article/section; long ones split at 300 words with 50 overlap."""
    sections: list[tuple[str | None, list[Line]]] = []
    for line in lines:
        if sections and sections[-1][0] == line.heading:
            sections[-1][1].append(line)
        else:
            sections.append((line.heading, [line]))
    chunks = []
    step = SECTION_MAX_WORDS - SECTION_OVERLAP
    for heading, sec in sections:
        words = [(w, l.page) for l in sec for w in l.text.split()]
        if len(words) < SECTION_MIN_WORDS:                 # table-of-contents lines, stray headings
            continue
        starts = [0] if len(words) <= SECTION_MAX_WORDS else range(0, len(words) - SECTION_OVERLAP, step)
        for start in starts:
            piece = words[start:start + SECTION_MAX_WORDS]
            text = " ".join(w for w, _ in piece)
            if heading and start > 0:
                text = f"{heading} (continued): {text}"
            chunks.append(make_chunk("structure", source, text, [heading], [p for _, p in piece]))
    return chunks


def chunk_document(path: Path) -> tuple[list[dict], int]:
    lines = load_document(path)
    words = sum(len(l.text.split()) for l in lines)
    return chunk_fixed(path.name, lines) + chunk_structure(path.name, lines), words


# ---------------------------------------------------------------- embed

_client = None


def _gemini():
    global _client
    if _client is None:
        from google import genai
        from api_key import load_api_key
        _client = genai.Client(api_key=load_api_key())
    return _client


def normalize(values) -> list[float]:
    v = np.asarray(values, dtype=np.float32)
    n = float(np.linalg.norm(v)) or 1.0
    return [round(float(x), 6) for x in v / n]


_task_types_ok = True


def embed_batch(texts: list[str], task: str) -> list[list[float]]:
    """Embed up to BATCH texts. Waits on per-minute limits, raises QuotaExhausted on the daily one."""
    global _task_types_ok
    from google.genai import errors, types
    for attempt in range(6):
        try:
            config = types.EmbedContentConfig(
                output_dimensionality=EMBED_DIM, task_type=task if _task_types_ok else None)
            # One Content per text: with a plain list of strings, gemini-embedding-2 (a multimodal
            # model) merges them into ONE input and returns a single vector for the whole batch.
            contents = [types.Content(role="user", parts=[types.Part(text=t)]) for t in texts]
            result = _gemini().models.embed_content(model=EMBED_MODEL, contents=contents, config=config)
            if len(result.embeddings) != len(texts):
                raise RuntimeError(f"Asked for {len(texts)} embeddings, got {len(result.embeddings)}; nothing saved.")
            return [normalize(e.values) for e in result.embeddings]
        except errors.ClientError as e:
            message = str(e)
            if e.code == 429:
                if "perday" in message.lower().replace(" ", "").replace("_", ""):
                    raise QuotaExhausted(message[:300]) from e
                wait = 20 * (attempt + 1)
                log.info(f"  rate limited, waiting {wait}s")
                time.sleep(wait)
            elif e.code == 400 and _task_types_ok and "task" in message.lower():
                _task_types_ok = False                     # model without task types
            else:
                raise
    raise QuotaExhausted("Still rate limited after six tries.")


def saved_keys() -> set[str]:
    return {r["k"] for r in read_jsonl(VECTORS_FILE)}


def embed_missing(chunks: list[dict]) -> int:
    """Embed chunks whose text has no saved vector; save after every batch."""
    have = saved_keys()
    todo: dict[str, str] = {}
    for c in chunks:
        if c["key"] not in have:
            todo.setdefault(c["key"], c["embed_text"])
    items = list(todo.items())
    for i in range(0, len(items), BATCH):
        batch = items[i:i + BATCH]
        vectors = embed_batch([t for _, t in batch], "RETRIEVAL_DOCUMENT")
        append_jsonl(VECTORS_FILE, [{"k": k, "v": v} for (k, _), v in zip(batch, vectors)])
        log.info(f"  embedded {min(i + BATCH, len(items))}/{len(items)}")
    return len(items)


# ---------------------------------------------------------------- search

STOP = set("a an the of to in on for and or is are be by with as at from that this it its what which who how when "
           "does do can may shall under any".split())


def tokenize(text: str) -> list[str]:
    return [t for t in re.findall(r"[a-z0-9]+", text.lower()) if t not in STOP]


class BM25:
    def __init__(self, docs: list[list[str]], k1: float = 1.5, b: float = 0.75):
        self.k1, self.b = k1, b
        self.tf = [Counter(d) for d in docs]
        self.lengths = np.array([len(d) for d in docs], dtype=np.float32)
        self.avg = float(self.lengths.mean()) if docs else 1.0
        df = Counter(t for d in self.tf for t in d)
        n = len(docs)
        self.idf = {t: math.log(1 + (n - m + 0.5) / (m + 0.5)) for t, m in df.items()}

    def scores(self, query: list[str]) -> np.ndarray:
        out = np.zeros(len(self.tf), dtype=np.float32)
        for i, tf in enumerate(self.tf):
            norm = self.k1 * (1 - self.b + self.b * self.lengths[i] / self.avg)
            for t in query:
                f = tf.get(t)
                if f:
                    out[i] += self.idf[t] * f * (self.k1 + 1) / (f + norm)
        return out


def ranks(scores: np.ndarray) -> np.ndarray:
    r = np.empty(len(scores), dtype=np.int64)
    r[np.argsort(-scores, kind="stable")] = np.arange(len(scores))
    return r


class Store:
    """The committed index, loaded once. Only queries are embedded."""

    def __init__(self):
        self.reload()

    def reload(self) -> None:
        self.chunks = read_jsonl(CHUNKS_FILE)
        self.vectors = {r["k"]: r["v"] for r in read_jsonl(VECTORS_FILE)}
        self.queries = {r["q"]: r["v"] for r in read_jsonl(QUERIES_FILE)}
        self._designs: dict = {}

    def _design(self, design: str):
        if design not in self._designs:
            cs = [c for c in self.chunks if c["design"] == design and c["key"] in self.vectors]
            matrix = (np.array([self.vectors[c["key"]] for c in cs], dtype=np.float32)
                      if cs else np.zeros((0, EMBED_DIM), dtype=np.float32))
            # A chunk is "structural" if it lies in an article, annex, chapter or section.
            # Documents with no detected structure (e.g. guidelines) count as structural throughout,
            # so the "articles" filter only drops the recitals/preamble of structured documents.
            labelled = [any(not s.startswith("p") for s in c.get("span", [])) for c in cs]
            has_structure = {c["source"] for c, l in zip(cs, labelled) if l}
            structural = np.array([l or c["source"] not in has_structure for c, l in zip(cs, labelled)], dtype=bool)
            self._designs[design] = (cs, matrix, BM25([tokenize(c["text"]) for c in cs]), structural)
        return self._designs[design]

    def query_vector(self, query: str) -> np.ndarray:
        if query not in self.queries:
            vector = embed_batch([query], "RETRIEVAL_QUERY")[0]
            self.queries[query] = vector
            append_jsonl(QUERIES_FILE, [{"q": query, "v": vector}])
        return np.asarray(self.queries[query], dtype=np.float32)

    def search(self, query: str, k: int = TOP_K, design: str = ACTIVE_DESIGN,
               mode: str = ACTIVE_MODE, source: str | None = None, scope: str = ACTIVE_SCOPE) -> list[dict]:
        chunks, matrix, bm25, structural = self._design(design)
        if not chunks:
            return []
        dense = matrix @ self.query_vector(query)
        if mode == "dense":
            fused = dense
        else:
            fused = 1 / (60 + ranks(dense)) + 1 / (60 + ranks(bm25.scores(tokenize(query))))
        if source:
            keep = np.array([c["source"].lower() == source.lower() for c in chunks])
            fused = np.where(keep, fused, -np.inf)
        if scope == "articles":
            fused = np.where(structural, fused, -np.inf)
        order = [i for i in np.argsort(-fused, kind="stable")[:k] if np.isfinite(fused[i])]
        return [{**chunks[i], "score": round(float(dense[i]), 4)} for i in order]


# ---------------------------------------------------------------- pipeline

def corpus_files() -> list[Path]:
    if not CORPUS_DIR.is_dir():
        return []
    return sorted(p for p in CORPUS_DIR.iterdir() if p.is_file() and p.suffix.lower() in SUPPORTED)


def save_chunks(chunks: list[dict]) -> None:
    write_jsonl(CHUNKS_FILE, [{k: v for k, v in c.items() if k != "embed_text"} for c in chunks])


def build_index() -> None:
    files = corpus_files()
    if not files:
        raise SystemExit(f"No documents in {CORPUS_DIR}. Put your corpus files there ({', '.join(sorted(SUPPORTED))}).")
    docs, chunks = {}, []
    for path in files:
        doc_chunks, words = chunk_document(path)
        docs[path.name] = {"sha256": file_sha(path), "words": words}
        chunks += doc_chunks
        per = Counter(c["design"] for c in doc_chunks)
        log.info(f"{path.name}: {words:,} words, " + ", ".join(f"{per[d]} {d} chunks" for d in DESIGNS))
    save_chunks(chunks)
    write_docs(docs)
    total = sum(d["words"] for d in docs.values())
    log.info(f"\n{len(docs)} documents, {total:,} words, {len(chunks)} chunks in {len(DESIGNS)} designs.")
    if len(docs) < 3 or total < 50_000:
        log.info("WARNING: the brief asks for at least 3 documents and 50,000 words.")
    try:
        n = embed_missing(chunks)
    except QuotaExhausted as e:
        log.info(f"\nDaily embedding quota reached; every vector so far is saved. Run again after 09:00 Spain time.\n{e}")
        raise SystemExit(1)
    log.info(f"Embedded {n} new chunk texts; the rest were already saved. Index is in {INDEX_DIR}.")


def add_document(path: str) -> str:
    """Index one file (used by server.py). Same file again: skipped. Same name, new content: replaced."""
    p = Path(path).expanduser()
    if not p.is_absolute():
        p = ROOT / p
    if not p.is_file():
        return f"Not added: {p} does not exist."
    if p.suffix.lower() not in SUPPORTED:
        return f"Not added: {p.suffix} files are not supported ({', '.join(sorted(SUPPORTED))})."
    sha = file_sha(p)
    docs = read_docs()
    for name, info in docs.items():
        if info["sha256"] == sha:
            # Same content already registered. If an earlier call stopped at the quota, finish it.
            pending = [c for c in read_jsonl(CHUNKS_FILE) if c["source"] == name and c["design"] == ACTIVE_DESIGN]
            have = saved_keys()
            missing = [c for c in pending if c["key"] not in have]
            if not missing:
                return f"Already indexed as {name}; the content is identical, so nothing was added or embedded."
            for c in missing:
                c["embed_text"] = f"{c['source']} | {c['location']}\n{c['text']}"
            try:
                n = embed_missing(missing)
            except QuotaExhausted:
                return f"{name} is registered but {len(missing)} chunks still lack vectors: the daily embedding quota ran out again."
            return f"Finished indexing {name}: embedded the {n} chunks a previous call could not; it is searchable now."
    replacing = p.name in docs
    new_chunks, words = chunk_document(p)
    if not new_chunks:
        return f"Not added: no text could be extracted from {p.name}."
    CORPUS_DIR.mkdir(exist_ok=True)
    target = CORPUS_DIR / p.name
    if p.resolve() != target.resolve():
        shutil.copy2(p, target)                            # so `main.py index` keeps it
    kept = [c for c in read_jsonl(CHUNKS_FILE) if c["source"] != p.name]
    save_chunks(kept + new_chunks)
    docs[p.name] = {"sha256": sha, "words": words}
    write_docs(docs)
    active = [c for c in new_chunks if c["design"] == ACTIVE_DESIGN]
    try:
        n = embed_missing(active)
    except QuotaExhausted:
        return (f"{p.name} was chunked but the daily embedding quota ran out; vectors saved so far are kept. "
                "Call add_document again tomorrow to finish.")
    verb = "Replaced the earlier version of" if replacing else "Added"
    return f"{verb} {p.name}: {words:,} words, {len(active)} chunks, {n} new embeddings. It is searchable now."


if __name__ == "__main__":
    build_index()