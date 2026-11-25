"""
Assignment 3: build the index (`main.py index`).

Pipeline, per document:
  1. download   corpus_sources.download()            BOE open-data XML -> corpus/
  2. extract    extract_units(path)                   one unit per article / annex, cleaned
  3. chunk      chunk_fixed(units) / chunk_structure(units)
  4. embed      embed_and_store(chunks, design)        Gemini, saved to ChromaDB in index/
                                                       batch by batch, skipping chunks that
                                                       already have a vector

Two retrieval designs are built side by side, one Chroma collection each:
  - "fixed":     ~300-word sliding windows over the whole document (50-word overlap)
  - "structure": one chunk per article; long articles are split at paragraph
                 boundaries (keeping the sub-article number, e.g. "10.2.1"),
                 and every chunk starts with "Document - Article. Title".

server.py imports index_file() and search() from here, so the add-document
tool runs exactly this pipeline.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import time
import xml.etree.ElementTree as ET
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent
INDEX_DIR = ROOT / "index"
CONFIG_FILE = INDEX_DIR / "config.json"
QUERY_CACHE = INDEX_DIR / "query_cache.json"

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768
BATCH = 20                      # texts per embed request
DESIGNS = ("fixed", "structure")
DEFAULT_DESIGN = "structure"    # overwritten by config.json once evaluate.py has chosen

FIXED_WORDS, FIXED_OVERLAP = 300, 50
STRUCT_MAX_WORDS, STRUCT_SPLIT_WORDS = 350, 300

SKIP_BLOCKS = {"preambulo", "firma"}   # exposición de motivos and signature: no rules in them
SUBLOC_RE = re.compile(r"^((?:\d+\.)+\d+|[SMP]\d+(?:\.\d+)*)\.?\s")   # 10.2.1 / S3 / M1 / P1
LABEL_RE = re.compile(r"^((?:Artículo|Disposición)\s.+?)\.(?:\s|$)")


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)   # stdout belongs to the MCP protocol


# --------------------------------------------------------------------------- extract

@dataclass
class Unit:
    """One article (or annex) of one document, cleaned."""
    source: str          # document id, e.g. "LO_11_2021"
    doc_title: str
    location: str        # "Artículo 15", "Disposición adicional primera", "Anexo"
    heading: str         # first line, e.g. "Artículo 15. Condiciones de realización de los controles."
    paragraphs: list[str] = field(default_factory=list)


def _clean(text: str) -> str:
    return " ".join(text.split())


def extract_units(path: Path, source: str | None = None, doc_title: str | None = None) -> list[Unit]:
    """Extract the units of one file. BOE consolidated XML, or plain text / markdown / PDF."""
    path = Path(path)
    source = source or path.stem
    doc_title = doc_title or source
    if path.suffix.lower() == ".xml":
        return _units_from_boe_xml(path, source, doc_title)
    if path.suffix.lower() == ".pdf":
        return _units_from_pdf(path, source, doc_title)
    return _units_from_text(path.read_text(encoding="utf-8"), source, doc_title)


def _units_from_boe_xml(path: Path, source: str, doc_title: str) -> list[Unit]:
    root = ET.parse(path).getroot()
    title_el = root.find(".//metadatos/titulo")
    if title_el is not None and title_el.text and doc_title == source:
        doc_title = _clean(title_el.text)
    units: list[Unit] = []
    for block in root.iter("bloque"):
        kind = block.get("tipo", "")
        if kind in SKIP_BLOCKS:
            continue
        versions = block.findall("version")
        if not versions:
            continue
        paras = [_clean("".join(p.itertext())) for p in versions[-1]]   # last = text in force
        paras = [p for p in paras if p]
        # drop BOE editorial notes ("Se modifica ... por el art. único ... Ref. BOE-A-...")
        paras = [p for p in paras if not re.match(r"^Se (modifica|añade|suprime|da nueva redacción)\b.*Ref\. BOE", p)]
        if not paras:
            continue
        if kind == "encabezado" and sum(len(p.split()) for p in paras) < 50:
            continue        # plain "TÍTULO I" / "CAPÍTULO II" headings
        if any(p.startswith("(Suprimido)") or p == "(Derogado)" for p in paras[:2]):
            continue        # repealed article: nothing to cite
        heading = paras[0]
        m = LABEL_RE.match(heading)
        if m:
            location = m.group(1)
        else:
            titulo = _clean(block.get("titulo") or "").strip("[] ")
            location = titulo.capitalize() if titulo.isupper() else (titulo or block.get("id"))
        body = paras[1:] if m or heading.isupper() else paras
        units.append(Unit(source, doc_title, location, heading, body or paras))
    return units


def _units_from_text(text: str, source: str, doc_title: str) -> list[Unit]:
    """Markdown / plain text: a unit per heading (#, ##, or 'Artículo N.')."""
    units: list[Unit] = []
    current = Unit(source, doc_title, "Inicio", doc_title, [])
    for line in text.splitlines():
        line = _clean(line)
        if not line:
            continue
        heading = line.lstrip("#").strip() if line.startswith("#") else None
        m = LABEL_RE.match(line)
        if heading or m:
            if current.paragraphs:
                units.append(current)
            label = m.group(1) if m else heading
            current = Unit(source, doc_title, label, line.lstrip("# "), [])
        else:
            current.paragraphs.append(line)
    if current.paragraphs:
        units.append(current)
    return units


def _units_from_pdf(path: Path, source: str, doc_title: str) -> list[Unit]:
    from pypdf import PdfReader
    units = []
    for i, page in enumerate(PdfReader(str(path)).pages, 1):
        paras = [_clean(p) for p in (page.extract_text() or "").split("\n\n") if _clean(p)]
        if paras:
            units.append(Unit(source, doc_title, f"Página {i}", f"Página {i}", paras))
    return units


# --------------------------------------------------------------------------- chunk

@dataclass
class Chunk:
    id: str
    text: str            # what the model reads (and what gets embedded, with the title)
    source: str
    doc_title: str
    location: str        # article-level, used for hit rate
    sublocation: str     # finer: "10.2.1", "S3"; "" if none
    covers: str          # all article-level locations in the chunk, "|"-joined

    def metadata(self) -> dict:
        return {k: getattr(self, k) for k in ("source", "doc_title", "location", "sublocation", "covers")}


def _chunk_id(design: str, source: str, text: str) -> str:
    return f"{design}:{source}:" + hashlib.sha1(text.encode("utf-8")).hexdigest()[:16]


def chunk_structure(units: list[Unit]) -> list[Chunk]:
    """One chunk per article; split long ones at paragraph boundaries."""
    chunks: list[Chunk] = []
    for u in units:
        pieces: list[str] = []          # split over-long paragraphs first
        for p in u.paragraphs:
            words = p.split()
            if len(words) <= STRUCT_MAX_WORDS:
                pieces.append(p)
            else:
                for i in range(0, len(words), STRUCT_SPLIT_WORDS):
                    pieces.append(" ".join(words[i:i + STRUCT_SPLIT_WORDS]))
        sub, buf, buf_sub, n = "", [], "", 0
        def flush():
            nonlocal buf, n
            if buf:
                header = f"{u.doc_title} — {u.heading}" + (f" [{buf_sub}]" if buf_sub else "")
                text = header + "\n" + "\n".join(buf)
                chunks.append(Chunk(_chunk_id("structure", u.source, text), text, u.source,
                                    u.doc_title, u.location, buf_sub, u.location))
            buf, n = [], 0
        for p in pieces:
            m = SUBLOC_RE.match(p)
            if m:
                sub = m.group(1)
            w = len(p.split())
            if buf and n + w > STRUCT_MAX_WORDS:
                flush()
            if not buf:
                buf_sub = sub
            buf.append(p)
            n += w
        flush()
    return chunks


def chunk_fixed(units: list[Unit]) -> list[Chunk]:
    """Sliding windows of FIXED_WORDS words over each document, ignoring structure."""
    chunks: list[Chunk] = []
    by_source: dict[str, list[tuple[str, str]]] = {}
    titles: dict[str, str] = {}
    for u in units:
        titles[u.source] = u.doc_title
        for p in [u.heading, *u.paragraphs]:
            by_source.setdefault(u.source, []).extend((w, u.location) for w in p.split())
    step = FIXED_WORDS - FIXED_OVERLAP
    for source, words in by_source.items():
        for start in range(0, max(len(words) - FIXED_OVERLAP, 1), step):
            window = words[start:start + FIXED_WORDS]
            text = " ".join(w for w, _ in window)
            locs = list(dict.fromkeys(loc for _, loc in window))
            chunks.append(Chunk(_chunk_id("fixed", source, text), f"{titles[source]}\n{text}", source,
                                titles[source], locs[0], "", "|".join(locs)))
    return chunks


def chunk_units(units: list[Unit], design: str) -> list[Chunk]:
    return chunk_structure(units) if design == "structure" else chunk_fixed(units)


# --------------------------------------------------------------------------- embed & store

_client = None


def gemini():
    global _client
    if _client is None:
        from google import genai
        from api_key import load_api_key
        _client = genai.Client(api_key=load_api_key())
    return _client


def _embed(texts: list[str]) -> list[list[float]]:
    """Embed a batch, one vector per text, retrying on rate limits."""
    from google.genai import types
    contents = [types.Content(parts=[types.Part(text=t)]) for t in texts]
    for attempt in range(6):
        try:
            res = gemini().models.embed_content(
                model=EMBED_MODEL, contents=contents,
                config=types.EmbedContentConfig(output_dimensionality=EMBED_DIM),
            )
            vectors = [e.values for e in res.embeddings]
            if len(vectors) != len(texts):
                raise RuntimeError(f"asked for {len(texts)} embeddings, got {len(vectors)}")
            return vectors
        except Exception as error:  # noqa: BLE001
            msg = str(error)
            if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
                if "PerDay" in msg or "per day" in msg.lower():
                    raise RuntimeError("Daily embedding quota used up. Run again after 09:00 (Spain); "
                                       "vectors saved so far are kept.") from error
                wait = 20 * (attempt + 1)
                log(f"  rate limited, waiting {wait}s ...")
                time.sleep(wait)
            else:
                raise
    raise RuntimeError("Gave up after repeated rate limits; run again later, nothing is lost.")


def document_text(chunk: Chunk) -> str:
    """Gemini Embedding 2 document format."""
    return f"title: {chunk.doc_title} | text: {chunk.text}"


def query_text(query: str) -> str:
    return f"task: question answering | query: {query}"


def collection(design: str):
    import chromadb
    from chromadb.config import Settings
    client = chromadb.PersistentClient(path=str(INDEX_DIR / "chroma"),
                                       settings=Settings(anonymized_telemetry=False))
    return client.get_or_create_collection(design, metadata={"hnsw:space": "cosine"})


def embed_and_store(chunks: list[Chunk], design: str) -> int:
    """Embed only chunks with no stored vector; store each batch as soon as it arrives."""
    col = collection(design)
    existing = set(col.get(ids=[c.id for c in chunks], include=[])["ids"]) if chunks else set()
    todo = [c for c in chunks if c.id not in existing]
    log(f"[{design}] {len(chunks)} chunks, {len(existing)} already embedded, {len(todo)} to embed")
    for i in range(0, len(todo), BATCH):
        batch = todo[i:i + BATCH]
        vectors = _embed([document_text(c) for c in batch])
        col.upsert(ids=[c.id for c in batch], embeddings=vectors,
                   documents=[c.text for c in batch], metadatas=[c.metadata() for c in batch])
        log(f"  [{design}] stored {min(i + BATCH, len(todo))}/{len(todo)}")
    return len(todo)


def remove_source(source: str, design: str) -> int:
    col = collection(design)
    ids = col.get(where={"source": source}, include=[])["ids"]
    if ids:
        col.delete(ids=ids)
    return len(ids)


def index_file(path: Path, source: str | None = None, doc_title: str | None = None,
               designs: tuple[str, ...] | None = None) -> dict:
    """Run one file through the whole pipeline. Used by main() and by server.py's add_document.

    Re-indexing the same file is a no-op (chunk ids are content hashes). If a document with the
    same source id was indexed with different content, its old chunks are replaced.
    """
    designs = designs or DESIGNS
    units = extract_units(path, source, doc_title)
    if not units:
        raise ValueError(f"No text could be extracted from {path}")
    report = {"source": units[0].source, "title": units[0].doc_title, "units": len(units)}
    for design in designs:
        chunks = chunk_units(units, design)
        col = collection(design)
        old = set(col.get(where={"source": units[0].source}, include=[])["ids"])
        new = {c.id for c in chunks}
        stale = list(old - new)
        if stale:
            col.delete(ids=stale)
        report[design] = {"chunks": len(chunks), "embedded_now": embed_and_store(chunks, design),
                          "replaced_old": len(stale)}
    return report


# --------------------------------------------------------------------------- search

def chosen_design() -> str:
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text()).get("design", DEFAULT_DESIGN)
    return DEFAULT_DESIGN


def chosen_design_collection() -> str:
    """The Chroma collection behind the chosen search variant (where add_document writes)."""
    return SEARCH_VARIANTS[chosen_design()][0]


def embed_query(query: str) -> list[float]:
    """Embed a query, caching it on disk so evaluation reruns cost no quota."""
    cache = json.loads(QUERY_CACHE.read_text()) if QUERY_CACHE.exists() else {}
    if query not in cache:
        cache[query] = _embed([query_text(query)])[0]
        QUERY_CACHE.write_text(json.dumps(cache))
    return cache[query]


# Search variants. A variant is a collection (chunking) plus a search method; methods other
# than "vector" cost no extra embeddings, so they can be compared on the same index.
SEARCH_VARIANTS = {
    "fixed": ("fixed", "vector"),
    "structure": ("structure", "vector"),
    "fixed+hybrid": ("fixed", "hybrid"),
    "structure+hybrid": ("structure", "hybrid"),
}

STOPWORDS = set("""a al algo como con de del el en entre es esa ese eso esta este esto la las le
lo los me mi mis o para pero por que qué se si sin su sus te tengo un una uno y ya yo puedo
cuál cuánto cuántos cuándo dónde hay ser son está están""".split())


def _tokens(text: str) -> list[str]:
    import unicodedata
    text = unicodedata.normalize("NFKD", text.lower())
    text = "".join(ch for ch in text if not unicodedata.combining(ch))
    return [t for t in re.findall(r"[a-z0-9]+", text) if t not in STOPWORDS and len(t) > 1]


_bm25_cache: dict[str, tuple] = {}


def _bm25(collection_name: str, query: str) -> list[tuple[str, float]]:
    """Plain BM25 (k1=1.5, b=0.75) over every chunk of a collection, built once per process."""
    import math
    from collections import Counter
    col = collection(collection_name)
    count = col.count()
    if collection_name not in _bm25_cache or _bm25_cache[collection_name][0] != count:
        data = col.get(include=["documents"])
        docs = [Counter(_tokens(d)) for d in data["documents"]]
        df = Counter(t for d in docs for t in d)
        avg = sum(sum(d.values()) for d in docs) / max(1, len(docs))
        _bm25_cache[collection_name] = (count, data["ids"], docs, df, avg)
    _, ids, docs, df, avg = _bm25_cache[collection_name]
    n = len(docs)
    q = _tokens(query)
    scores = []
    for cid, d in zip(ids, docs):
        length = sum(d.values())
        s = 0.0
        for t in q:
            if t in d:
                idf = math.log(1 + (n - df[t] + 0.5) / (df[t] + 0.5))
                s += idf * d[t] * 2.5 / (d[t] + 1.5 * (0.25 + 0.75 * length / avg))
        scores.append((cid, s))
    return sorted(scores, key=lambda x: -x[1])


def search(query: str, k: int = 5, design: str | None = None,
           exclude_sources: tuple[str, ...] = ()) -> list[dict]:
    """Top-k chunks for a query. `design` is a key of SEARCH_VARIANTS (default: the chosen one).

    `exclude_sources` hides documents added later (evaluation uses it to keep the retrieval
    comparison on the original corpus)."""
    if exclude_sources:
        wider = search(query, k + 40, design)
        return [r for r in wider if r["source"] not in exclude_sources][:k]
    collection_name, method = SEARCH_VARIANTS[design or chosen_design()]
    col = collection(collection_name)
    if method == "vector":
        res = col.query(query_embeddings=[embed_query(query)], n_results=min(k, col.count()),
                        include=["documents", "metadatas", "distances"])
        return [{"text": doc, **meta, "score": round(1 - dist, 4)}
                for doc, meta, dist in zip(res["documents"][0], res["metadatas"][0], res["distances"][0])]
    # hybrid: reciprocal rank fusion of the vector ranking and the BM25 ranking
    res = col.query(query_embeddings=[embed_query(query)], n_results=min(50, col.count()), include=[])
    fused: dict[str, float] = {}
    for rank, cid in enumerate(res["ids"][0]):
        fused[cid] = fused.get(cid, 0) + 1 / (60 + rank)
    for rank, (cid, _) in enumerate(_bm25(collection_name, query)[:50]):
        fused[cid] = fused.get(cid, 0) + 1 / (60 + rank)
    top = sorted(fused, key=lambda c: -fused[c])[:k]
    got = col.get(ids=top, include=["documents", "metadatas"])
    by_id = {i: (d, m) for i, d, m in zip(got["ids"], got["documents"], got["metadatas"])}
    return [{"text": by_id[c][0], **by_id[c][1], "score": round(fused[c], 4)} for c in top]


# --------------------------------------------------------------------------- main

def main() -> None:
    from corpus_sources import SOURCES, download
    for name, meta in SOURCES.items():
        path = download(name, meta["boe_id"])
        report = index_file(path, source=name, doc_title=meta["title"])
        log(json.dumps(report, ensure_ascii=False))
    log("Index ready in index/.")


if __name__ == "__main__":
    main()
