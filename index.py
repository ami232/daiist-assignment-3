"""
Assignment 3: build the index (`main.py index`).

Corpus: three Spanish housing laws from the BOE (see SOURCES). The pipeline,
one function per step (server.py's add_document imports them):

    extract(path)      -> pages: [{"text", "location": "p. 12"}], BOE index pages skipped
    clean(text)        -> text without BOE page footers or broken hyphenation
    label_words(pages) -> every word with its page and the article it belongs to
    chunk_fixed / chunk_by_article(words) -> chunks with id, source, location
    embed_texts(texts) -> Gemini vectors, read from / saved to index/vectors.sqlite
    embed_and_store(chunks, collection)   -> adds new chunks to ChromaDB
    index_file(path)   -> all of the above for one document (add_document)

index/
    chroma/          one ChromaDB collection per chunking design
    vectors.sqlite   every embedding computed so far, keyed by hash(model, task, text)
    manifest.json    chunk and word counts per design and document (for REPORT.md)
"""

from __future__ import annotations

import hashlib
import itertools
import json
import re
import sqlite3
import sys
import time
from functools import lru_cache
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768  # instead of the default 3072: 4x less disk, small loss in quality
DOC_TASK, QUERY_TASK = "RETRIEVAL_DOCUMENT", "RETRIEVAL_QUERY"
SUPPORTED = {".pdf", ".txt", ".md"}

# Source: Agencia Estatal Boletín Oficial del Estado (https://www.boe.es),
# consolidated texts, reusable under the BOE's reuse conditions (Ley 37/2007).
SOURCES = [
    {"name": "LAU", "file": "LAU.pdf", "title": "Ley 29/1994, de Arrendamientos Urbanos",
     "url": "https://www.boe.es/buscar/pdf/1994/BOE-A-1994-26003-consolidado.pdf"},
    {"name": "LeyVivienda", "file": "LeyVivienda.pdf", "title": "Ley 12/2023, por el derecho a la vivienda",
     "url": "https://www.boe.es/buscar/pdf/2023/BOE-A-2023-12203-consolidado.pdf"},
    {"name": "LPH", "file": "LPH.pdf", "title": "Ley 49/1960, sobre propiedad horizontal",
     "url": "https://www.boe.es/buscar/pdf/1960/BOE-A-1960-10906-consolidado.pdf"},
]

# ---------------------------------------------------------------------------
# YOUR DECISIONS: the chunking designs you compare, and the one you keep.
# Each design is a full re-embedding of the corpus (~1,000 embeddings a day).
# ---------------------------------------------------------------------------
DESIGNS = {
    "fixed": {"size": 200, "overlap": 50},  # windows of `size` words
    "article": {"max_words": 400},          # one chunk per article, long ones split
}
CHOSEN_DESIGN = "fixed"  # set from the hit rates in evaluate.py
TOP_K = 5                # chunks the search tool returns

# "Artículo 36." / "Artículo 9 bis." / "Artículo noveno." / "Disposición adicional primera."
# at the start of a line, followed by a dot (a line that merely cites one is not a heading).
HEADING = re.compile(r"^(Artículo \w+(?: bis| ter)?|Disposición \w+ \w+)\.(?!\.)", re.MULTILINE)


def log(*args) -> None:
    """Print to stderr: stdout belongs to the MCP protocol when the server imports us."""
    print(*args, file=sys.stderr, flush=True)


# ---------------------------------------------------------------------------
# 1. Extract and clean
# ---------------------------------------------------------------------------

BOE_NOISE = re.compile(
    r"^(BOLETÍN OFICIAL DEL ESTADO|LEGISLACIÓN CONSOLIDADA|Página \d+"
    r"|Este documento es de carácter informativo y no tiene valor jurídico\.)$",
    re.MULTILINE,
)


def clean(text: str) -> str:
    """Remove BOE page footers and PDF line-break debris, keeping the lines."""
    text = BOE_NOISE.sub("", text)
    text = re.sub(r"(\w)-\n(\w)", r"\1\2", text)  # "arren-\ndatario" -> "arrendatario"
    lines = [re.sub(r"[ \t\xa0]+", " ", line).strip() for line in text.splitlines()]
    return re.sub(r"\n{3,}", "\n\n", "\n".join(lines)).strip()


def is_index_page(text: str) -> bool:
    """The BOE's table of contents: lines ending in dot leaders and a page number."""
    return bool(re.search(r"\.{10,}", text))


def extract(path: Path) -> list[dict]:
    """A PDF gives one unit per page (index pages skipped); a text file one unit."""
    path = Path(path)
    if path.suffix.lower() == ".pdf":
        from pypdf import PdfReader

        pages = [(i, page.extract_text() or "") for i, page in enumerate(PdfReader(path).pages, start=1)]
        return [{"text": clean(text), "location": f"p. {i}"} for i, text in pages if not is_index_page(text)]
    if path.suffix.lower() in {".txt", ".md"}:
        return [{"text": clean(path.read_text(encoding="utf-8")), "location": None}]
    raise ValueError(f"Unsupported file type {path.suffix!r}; use one of {sorted(SUPPORTED)}.")


# ---------------------------------------------------------------------------
# 2. Chunk
# ---------------------------------------------------------------------------

def label_words(units: list[dict]) -> list[tuple[str, str | None, str | None]]:
    """Every word as (word, page, article). Articles continue across pages."""
    labelled, article = [], None
    for unit in units:
        start = 0
        for heading in HEADING.finditer(unit["text"]):
            labelled += [(w, unit["location"], article) for w in unit["text"][start:heading.start()].split()]
            article, start = heading.group(1), heading.start()
        labelled += [(w, unit["location"], article) for w in unit["text"][start:].split()]
    return labelled


def make_chunk(source: str, words: list[tuple], n: int) -> dict:
    """A chunk is located by the article and page where it starts, e.g.
    "Artículo 36, p. 25". `articles` lists every article it touches (for evaluation)."""
    _, page, article = words[0]
    articles = list(dict.fromkeys(a for _, _, a in words if a))
    location = ", ".join(x for x in (article, page) if x) or "texto"
    text = " ".join(w for w, _, _ in words)
    digest = hashlib.sha1(f"{source}|{n}|{text}".encode()).hexdigest()[:12]
    return {"id": f"{source}-{digest}", "source": source, "location": location,
            "articles": " | ".join(articles), "text": text}


def chunk_fixed(words: list[tuple], source: str, size: int, overlap: int) -> list[dict]:
    """Windows of `size` words, each starting `size - overlap` words after the last."""
    chunks = []
    for start in range(0, len(words), size - overlap):
        chunks.append(make_chunk(source, words[start:start + size], len(chunks)))
        if start + size >= len(words):
            break
    return chunks


def chunk_by_article(words: list[tuple], source: str, max_words: int) -> list[dict]:
    """One chunk per article; an article longer than `max_words` becomes several."""
    chunks = []
    for _, group in itertools.groupby(words, key=lambda w: w[2]):
        group = list(group)
        for start in range(0, len(group), max_words):
            chunks.append(make_chunk(source, group[start:start + max_words], len(chunks)))
    return chunks


def build_chunks(path: Path, source: str, design: str) -> list[dict]:
    """extract -> label -> chunk with one design; every chunk records the file's hash."""
    words = label_words(extract(path))
    cfg = DESIGNS[design]
    if design == "fixed":
        chunks = chunk_fixed(words, source, cfg["size"], cfg["overlap"])
    else:
        chunks = chunk_by_article(words, source, cfg["max_words"])
    for chunk in chunks:
        chunk["doc_hash"] = file_hash(path)
    return chunks


def file_hash(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()[:16]


# ---------------------------------------------------------------------------
# 3. Embed, saving every vector as soon as it arrives
# ---------------------------------------------------------------------------

def cache_key(text: str, task: str) -> str:
    return hashlib.sha256(f"{EMBED_MODEL}|{EMBED_DIM}|{task}|{text}".encode()).hexdigest()


class VectorCache:
    """A small on-disk dictionary {cache_key: vector} in SQLite."""

    def __init__(self, path: Path):
        Path(path).parent.mkdir(parents=True, exist_ok=True)
        self.db = sqlite3.connect(str(path))
        self.db.execute("CREATE TABLE IF NOT EXISTS vectors (key TEXT PRIMARY KEY, vec BLOB NOT NULL)")

    def get(self, keys: list[str]) -> dict[str, list[float]]:
        found = {}
        for i in range(0, len(keys), 500):  # SQLite limits the number of ? per query
            batch = keys[i:i + 500]
            rows = self.db.execute(f"SELECT key, vec FROM vectors WHERE key IN ({','.join('?' * len(batch))})", batch)
            found.update({k: np.frombuffer(v, dtype=np.float32).tolist() for k, v in rows})
        return found

    def put_many(self, items: list[tuple[str, list[float]]]) -> None:
        self.db.executemany("INSERT OR REPLACE INTO vectors VALUES (?, ?)",
                            [(k, np.asarray(v, dtype=np.float32).tobytes()) for k, v in items])
        self.db.commit()


class QuotaExhausted(RuntimeError):
    """The daily embedding quota is used up; rerun after it resets (09:00 in Spain)."""


@lru_cache(maxsize=1)
def genai_client():
    from google import genai

    from api_key import load_api_key

    return genai.Client(api_key=load_api_key())


def gemini_embed(texts: list[str], task: str) -> list[list[float]]:
    """Embed one batch with Gemini. Waits out per-minute limits; stops on the daily one."""
    from google.genai import errors, types

    # One Content per text: a plain list of strings is read as ONE multi-part
    # content by gemini-embedding-2 and comes back as a single merged vector.
    contents = [types.Content(parts=[types.Part(text=t)]) for t in texts]
    for attempt in range(5):
        try:
            response = genai_client().models.embed_content(
                model=EMBED_MODEL, contents=contents,
                config=types.EmbedContentConfig(task_type=task, output_dimensionality=EMBED_DIM))
            return [e.values for e in response.embeddings]
        except errors.ClientError as error:
            if error.code != 429:
                raise
            if "PerDay" in str(error):
                raise QuotaExhausted("Daily embedding quota used up. Vectors so far are saved; rerun tomorrow.") from error
            log(f"  rate limited, waiting {30 * (attempt + 1)}s ...")
            time.sleep(30 * (attempt + 1))
    raise RuntimeError("Gemini kept rate-limiting the embedding calls.")


def embed_texts(texts: list[str], task: str, embed_fn=None, cache: VectorCache | None = None,
                batch_size: int = 50) -> list[list[float]]:
    """Vectors for `texts`, calling the API only for texts the cache does not have."""
    embed_fn = embed_fn or gemini_embed
    cache = cache or VectorCache(INDEX_DIR / "vectors.sqlite")
    keys = [cache_key(t, task) for t in texts]
    have = cache.get(keys)
    missing = list(dict.fromkeys(t for t, k in zip(texts, keys) if k not in have))
    for i in range(0, len(missing), batch_size):
        batch = missing[i:i + batch_size]
        vectors = embed_fn(batch, task)
        if len(vectors) != len(batch):  # never cache a vector under the wrong text
            raise ValueError(f"Sent {len(batch)} texts but got {len(vectors)} vectors back.")
        new = [(cache_key(t, task), v) for t, v in zip(batch, vectors)]
        cache.put_many(new)  # saved before the next call, so a crash loses nothing
        have.update(new)
        if len(missing) > batch_size:
            log(f"  embedded {i + len(batch)}/{len(missing)} new texts")
    return [have[k] for k in keys]


# ---------------------------------------------------------------------------
# 4. Store in ChromaDB
# ---------------------------------------------------------------------------

@lru_cache(maxsize=None)
def chroma_client(path: str):
    import chromadb
    from chromadb.config import Settings

    return chromadb.PersistentClient(path=path, settings=Settings(anonymized_telemetry=False))


def open_collection(design: str, path: Path = INDEX_DIR / "chroma"):
    """The collection for one design. We always pass our own vectors, so ChromaDB's
    built-in embedding model is switched off (embedding_function=None)."""
    return chroma_client(str(path)).get_or_create_collection(
        name=design, embedding_function=None, configuration={"hnsw": {"space": "cosine"}})


METADATA_KEYS = ("source", "location", "articles", "doc_hash")


def embed_and_store(chunks: list[dict], collection, embed_fn=None, cache: VectorCache | None = None) -> int:
    """Add the chunks the collection does not have yet; returns how many were added."""
    existing = set(collection.get(ids=[c["id"] for c in chunks], include=[])["ids"]) if chunks else set()
    new = [c for c in chunks if c["id"] not in existing]
    if not new:
        return 0
    vectors = embed_texts([c["text"] for c in new], DOC_TASK, embed_fn=embed_fn, cache=cache)
    collection.add(ids=[c["id"] for c in new], embeddings=vectors, documents=[c["text"] for c in new],
                   metadatas=[{k: c[k] for k in METADATA_KEYS if k in c} for c in new])
    return len(new)


# ---------------------------------------------------------------------------
# 5. One document end to end (what add_document runs)
# ---------------------------------------------------------------------------

def index_file(path: str | Path, design: str = CHOSEN_DESIGN, path_index: Path = INDEX_DIR, embed_fn=None) -> dict:
    """Index one document into `design`'s collection. The source name is the file name.

    Already indexed (same name, same content): nothing happens, nothing is spent.
    Same name but the file changed: the old chunks are replaced, but only after the
    new ones are embedded, so a failure (e.g. quota) leaves the old version searchable.
    """
    path = Path(path).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"No file at {path}")
    if path.suffix.lower() not in SUPPORTED:
        raise ValueError(f"Unsupported file type {path.suffix!r}; use one of {sorted(SUPPORTED)}.")
    source = path.stem
    collection = open_collection(design, path=Path(path_index) / "chroma")
    cache = VectorCache(Path(path_index) / "vectors.sqlite")

    previous = collection.get(where={"source": source}, include=["metadatas"], limit=1)
    if previous["ids"] and previous["metadatas"][0].get("doc_hash") == file_hash(path):
        return {"status": "already indexed", "source": source, "chunks": 0}

    chunks = build_chunks(path, source, design)
    embed_texts([c["text"] for c in chunks], DOC_TASK, embed_fn=embed_fn, cache=cache)
    if previous["ids"]:
        collection.delete(where={"source": source})
    added = embed_and_store(chunks, collection, embed_fn=embed_fn, cache=cache)
    return {"status": "updated" if previous["ids"] else "added", "source": source, "chunks": added}


# ---------------------------------------------------------------------------
# `main.py index`
# ---------------------------------------------------------------------------

def download_corpus() -> list[Path]:
    """Fetch every SOURCES entry into corpus/ unless it is already there."""
    import httpx

    CORPUS_DIR.mkdir(exist_ok=True)
    for src in SOURCES:
        target = CORPUS_DIR / src["file"]
        if not target.exists():
            log(f"downloading {src['name']} ...")
            response = httpx.get(src["url"], follow_redirects=True, timeout=120,
                                 headers={"User-Agent": "Mozilla/5.0 (course RAG assignment)"})
            response.raise_for_status()
            target.write_bytes(response.content)
    return [CORPUS_DIR / src["file"] for src in SOURCES]


def main() -> None:
    paths = download_corpus()
    manifest = {"embed_model": EMBED_MODEL, "embed_dim": EMBED_DIM, "chosen_design": CHOSEN_DESIGN, "designs": {}}
    try:
        for design in DESIGNS:
            collection = open_collection(design)
            per_source = {}
            for src, path in zip(SOURCES, paths):
                chunks = build_chunks(path, src["name"], design)
                added = embed_and_store(chunks, collection)
                per_source[src["name"]] = {"chunks": len(chunks), "words": sum(len(c["text"].split()) for c in chunks)}
                log(f"[{design}] {src['name']}: {len(chunks)} chunks ({added} newly embedded)")
            manifest["designs"][design] = {"config": DESIGNS[design], "chunks": collection.count(), "sources": per_source}
    except QuotaExhausted as stop:
        log(f"\n{stop}")
        raise SystemExit(1)
    (INDEX_DIR / "manifest.json").write_text(json.dumps(manifest, indent=2, ensure_ascii=False))
    log(f"index/ written. Chosen design: {CHOSEN_DESIGN}")


if __name__ == "__main__":
    main()
