"""
Assignment 3: build the index (`main.py index`).

Corpus: parts of Title 14 of the US Code of Federal Regulations (aviation),
downloaded from the eCFR API into corpus/ (git-ignored). US federal
regulations are public domain (17 U.S.C. 105).

Pipeline: download -> parse into sections -> chunk (<= ~200 words, every chunk
keeps its source and location) -> embed with Gemini (vectors saved as they
arrive, only chunks without a vector are embedded) -> index/chunks.jsonl.

The per-file steps are functions (`chunk_file`, `embed_and_store`) because
server.py's add_document tool imports them. The `Index` class holds the
retrieval designs compared in evaluate.py (vector, bm25, hybrid).
"""

import hashlib
import json
import math
import re
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"
CHUNKS_FILE = INDEX_DIR / "chunks.jsonl"
CONFIG_FILE = INDEX_DIR / "config.json"
QUERY_CACHE = INDEX_DIR / "query_cache.json"

EMBED_MODEL = "gemini-embedding-001"  # one vector per text (embedding-2 merges a list into ONE vector)
EMBED_DIM = 768
BATCH = 32
PAUSE_SECONDS = 15
MAX_WORDS = 200  # chunks are split on paragraphs above this size

ECFR_DATE = "2026-11-01"
ECFR = "https://www.ecfr.gov/api/versioner/v1/full/{date}/title-14.xml?part={part}"

# name used as `source` in the chunk metadata -> (file, URL)
CORPUS = {
    "14 CFR Part 107": ("part107.xml", ECFR.format(date=ECFR_DATE, part=107)),
    "14 CFR Part 48": ("part48.xml", ECFR.format(date=ECFR_DATE, part=48)),
    "14 CFR Part 89": ("part89.xml", ECFR.format(date=ECFR_DATE, part=89)),
    "14 CFR Part 101": ("part101.xml", ECFR.format(date=ECFR_DATE, part=101)),
    "14 CFR Part 67": ("part67.xml", ECFR.format(date=ECFR_DATE, part=67)),
    "14 CFR Part 91 Subpart A": ("part91A.xml", ECFR.format(date=ECFR_DATE, part=91) + "&subpart=A"),
    "14 CFR Part 91 Subpart B": ("part91B.xml", ECFR.format(date=ECFR_DATE, part=91) + "&subpart=B"),
    "14 CFR Part 91 Subpart C": ("part91C.xml", ECFR.format(date=ECFR_DATE, part=91) + "&subpart=C"),
    "14 CFR Part 91 Subpart D": ("part91D.xml", ECFR.format(date=ECFR_DATE, part=91) + "&subpart=D"),
}


def log(*a):
    print(*a, file=sys.stderr, flush=True)


# --------------------------------------------------------------------------- download

def download_corpus() -> None:
    import httpx

    CORPUS_DIR.mkdir(exist_ok=True)
    for source, (fname, url) in CORPUS.items():
        path = CORPUS_DIR / fname
        if path.exists() and path.stat().st_size > 1000:
            continue
        log(f"downloading {source}")
        r = httpx.get(url, timeout=120, follow_redirects=True, headers={"Accept-Encoding": "gzip"})
        r.raise_for_status()
        path.write_bytes(r.content)


def source_for_file(path: Path) -> str:
    for source, (fname, _) in CORPUS.items():
        if fname == path.name:
            return source
    return path.stem


# --------------------------------------------------------------------------- extraction + chunking

def _words(text: str) -> int:
    return len(text.split())


def _clean(text: str) -> str:
    text = text.replace(" ", " ")
    return re.sub(r"\s+", " ", text).strip()


def _pack(paragraphs: list[str], header: str) -> list[str]:
    """Greedy-pack paragraphs into pieces of at most MAX_WORDS words (header repeated)."""
    pieces, current, count = [], [], 0
    for p in paragraphs:
        w = _words(p)
        if current and count + w > MAX_WORDS:
            pieces.append(current)
            current, count = [], 0
        current.append(p)
        count += w
    if current:
        pieces.append(current)
    return [f"{header}\n" + "\n".join(piece) for piece in pieces]


def _chunks_from_ecfr(path: Path, source: str) -> list[dict]:
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(path.read_text(encoding="utf-8", errors="ignore"), "html.parser")
    out = []
    for sec in soup.find_all("div8", attrs={"type": "SECTION"}):
        head = sec.find("head")
        title = _clean(head.get_text(" ")) if head else ""
        m = re.match(r"§\s*([\d.]+\w*)\s*(.*)", title)
        number = m.group(1) if m else sec.get("n", "").replace("§", "").strip()
        heading = f"§ {number} {m.group(2) if m else title}".strip()
        for junk in sec.find_all(["head", "cita", "secauth", "img"]):
            junk.decompose()
        paragraphs = [_clean(p.get_text(" ")) for p in sec.find_all(["p", "pspace", "li"])]
        paragraphs = [p for p in paragraphs if p]
        if not paragraphs:
            paragraphs = [_clean(sec.get_text(" "))]
        if _words(" ".join(paragraphs)) < 6 or "[Reserved]" in heading:
            continue
        pieces = _pack(paragraphs, heading)
        for i, text in enumerate(pieces, 1):
            location = f"§ {number}" + (f" (part {i}/{len(pieces)})" if len(pieces) > 1 else "")
            out.append({"source": source, "location": location, "text": text})
    return out


def _chunks_from_pdf(path: Path, source: str) -> list[dict]:
    from pypdf import PdfReader

    out = []
    for n, page in enumerate(PdfReader(str(path)).pages, 1):
        text = _clean(page.extract_text() or "")
        words = text.split()
        for i in range(0, len(words), MAX_WORDS):
            out.append({"source": source, "location": f"p. {n}", "text": " ".join(words[i:i + MAX_WORDS])})
    return out


def _chunks_from_text(path: Path, source: str) -> list[dict]:
    raw = path.read_text(encoding="utf-8", errors="ignore")
    if path.suffix.lower() in {".html", ".htm"}:
        from bs4 import BeautifulSoup
        raw = BeautifulSoup(raw, "html.parser").get_text("\n")
    paragraphs = [_clean(p) for p in re.split(r"\n\s*\n", raw) if _clean(p)]
    out = []
    for n, piece in enumerate(_pack(paragraphs, ""), 1):
        out.append({"source": source, "location": f"block {n}", "text": piece.strip()})
    return out


def chunk_file(path) -> list[dict]:
    """Extract, clean and chunk one file. Every chunk has source, location, text, id."""
    path = Path(path)
    source = source_for_file(path)
    suffix = path.suffix.lower()
    if suffix == ".xml":
        chunks = _chunks_from_ecfr(path, source)
    elif suffix == ".pdf":
        chunks = _chunks_from_pdf(path, source)
    elif suffix in {".txt", ".md", ".html", ".htm"}:
        chunks = _chunks_from_text(path, source)
    else:
        raise ValueError(f"Unsupported file type: {suffix}")
    for c in chunks:
        c["id"] = hashlib.sha1(f"{c['source']}|{c['location']}|{c['text']}".encode()).hexdigest()[:16]
    return chunks


# --------------------------------------------------------------------------- embedding + storage

def load_records() -> dict[str, dict]:
    records = {}
    if CHUNKS_FILE.exists():
        for line in CHUNKS_FILE.read_text(encoding="utf-8").splitlines():
            if line.strip():
                r = json.loads(line)
                records[r["id"]] = r
    return records


def _client():
    from google import genai
    from api_key import load_api_key

    return genai.Client(api_key=load_api_key())


def _normalise(vectors) -> np.ndarray:
    v = np.asarray(vectors, dtype=np.float32)
    return v / np.maximum(np.linalg.norm(v, axis=1, keepdims=True), 1e-9)


def _embed(texts: list[str]) -> np.ndarray:
    from google.genai import types

    client = _client()
    for attempt in range(8):
        try:
            res = client.models.embed_content(
                model=EMBED_MODEL,
                contents=texts,
                config=types.EmbedContentConfig(output_dimensionality=EMBED_DIM),
            )
            if len(res.embeddings) != len(texts):
                raise SystemExit(
                    f"{EMBED_MODEL} returned {len(res.embeddings)} vectors for {len(texts)} texts; "
                    "refusing to store misaligned vectors."
                )
            return _normalise([e.values for e in res.embeddings])
        except Exception as e:  # noqa: BLE001
            msg = str(e)
            if attempt == 7 or ("RESOURCE_EXHAUSTED" in msg and "per day" in msg.lower()):
                raise
            # the free tier limits tokens per minute: wait as long as the API asks
            m = re.search(r"retry in ([\d.]+)s", msg)
            wait = float(m.group(1)) + 2 if m else 5 * (attempt + 1)
            log(f"embed retry {attempt + 1}: {type(e).__name__}, waiting {wait:.0f}s")
            time.sleep(wait)
    raise RuntimeError("unreachable")


def embed_and_store(chunks: list[dict]) -> dict:
    """Embed chunks that have no saved vector; append each batch to index/chunks.jsonl at once."""
    INDEX_DIR.mkdir(exist_ok=True)
    have = load_records()
    todo = [c for c in chunks if c["id"] not in have]
    stats = {"total": len(chunks), "already_indexed": len(chunks) - len(todo), "added": 0}
    for i in range(0, len(todo), BATCH):
        batch = todo[i:i + BATCH]
        vecs = _embed([f"{c['source']} {c['location']}\n{c['text']}" for c in batch])
        with CHUNKS_FILE.open("a", encoding="utf-8") as f:
            for c, v in zip(batch, vecs):
                f.write(json.dumps({**c, "vector": [round(float(x), 5) for x in v]}) + "\n")
        stats["added"] += len(batch)
        log(f"embedded {stats['added']}/{len(todo)}")
        if i + BATCH < len(todo):
            time.sleep(PAUSE_SECONDS)  # stay under the free-tier tokens-per-minute limit
    return stats


# --------------------------------------------------------------------------- retrieval designs

_TOKEN = re.compile(r"[a-z0-9]+(?:\.[0-9]+)?")


def tokenize(text: str) -> list[str]:
    return _TOKEN.findall(text.lower())


class Index:
    """Loads index/chunks.jsonl. Designs: 'vector', 'bm25', 'hybrid' (reciprocal rank fusion)."""

    def __init__(self):
        self.reload()

    def reload(self):
        recs = list(load_records().values())
        self.chunks = recs
        self.matrix = _normalise([r["vector"] for r in recs]) if recs else np.zeros((0, EMBED_DIM), np.float32)
        self.docs = [Counter(tokenize(f"{r['source']} {r['location']} {r['text']}")) for r in recs]
        self.doc_len = np.array([sum(d.values()) for d in self.docs], dtype=np.float32)
        self.avg_len = float(self.doc_len.mean()) if len(recs) else 1.0
        df = Counter()
        for d in self.docs:
            df.update(d.keys())
        n = max(len(recs), 1)
        self.idf = {t: math.log(1 + (n - c + 0.5) / (c + 0.5)) for t, c in df.items()}
        self._cache = None

    @property
    def default_mode(self) -> str:
        if CONFIG_FILE.exists():
            return json.loads(CONFIG_FILE.read_text()).get("mode", "hybrid")
        return "hybrid"

    def embed_query(self, query: str) -> np.ndarray:
        if self._cache is None:
            self._cache = json.loads(QUERY_CACHE.read_text()) if QUERY_CACHE.exists() else {}
        if query not in self._cache:
            self._cache[query] = [float(x) for x in _embed([query])[0]]
            QUERY_CACHE.write_text(json.dumps(self._cache))
        return np.asarray(self._cache[query], dtype=np.float32)

    def _bm25(self, query: str) -> np.ndarray:
        k1, b = 1.5, 0.75
        scores = np.zeros(len(self.chunks), dtype=np.float32)
        for t in set(tokenize(query)):
            idf = self.idf.get(t)
            if idf is None:
                continue
            for i, d in enumerate(self.docs):
                tf = d.get(t, 0)
                if tf:
                    scores[i] += idf * tf * (k1 + 1) / (tf + k1 * (1 - b + b * self.doc_len[i] / self.avg_len))
        return scores

    def search(self, query: str, k: int = 5, mode: str | None = None, source_prefix: str | None = None):
        """Return [(score, chunk)] best first. source_prefix is an optional metadata filter."""
        mode = mode or self.default_mode
        if not self.chunks:
            return []
        allowed = np.array([source_prefix is None or c["source"].startswith(source_prefix) for c in self.chunks])
        vec = self.matrix @ self.embed_query(query) if mode in ("vector", "hybrid") else None
        bm = self._bm25(query) if mode in ("bm25", "hybrid") else None
        if mode == "vector":
            score = vec
        elif mode == "bm25":
            score = bm
        else:
            score = np.zeros(len(self.chunks), dtype=np.float32)
            for s in (vec, bm):
                order = np.argsort(-np.where(allowed, s, -1e9))
                for rank, i in enumerate(order[:50]):
                    score[i] += 1.0 / (60 + rank + 1)
        score = np.where(allowed, score, -1e9)
        top = np.argsort(-score)[:k]
        return [(float(score[i]), self.chunks[i]) for i in top if score[i] > -1e8 and (mode != "bm25" or score[i] > 0)]


def format_results(results) -> str:
    if not results:
        return "No passages found."
    return "\n\n".join(
        f"[{n}] {c['source']} — {c['location']}\n{c['text']}" for n, (_, c) in enumerate(results, 1)
    )


# --------------------------------------------------------------------------- main

def main() -> None:
    download_corpus()
    total_words = 0
    all_chunks = []
    for source, (fname, _) in CORPUS.items():
        chunks = chunk_file(CORPUS_DIR / fname)
        words = sum(_words(c["text"]) for c in chunks)
        total_words += words
        all_chunks += chunks
        print(f"{source}: {len(chunks)} chunks, {words} words")
    print(f"TOTAL: {len(all_chunks)} chunks, {total_words} words")
    stats = embed_and_store(all_chunks)
    print(f"embedded {stats['added']} new chunks, {stats['already_indexed']} already had a vector")
    manifest = {s: sum(1 for c in all_chunks if c["source"] == s) for s in CORPUS}
    (INDEX_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2))


if __name__ == "__main__":
    main()
