"""
Assignment 3: build the index (`main.py index`).

Corpus: Spanish traffic law, consolidated texts from the BOE open-data API.
Each BOE text comes as XML split into "bloques" (articles, headings, annexes),
each with one or more dated versions. We keep the version in force today,
turn tables into pipe-separated rows, drop amendment footnotes and image
placeholders, and make one chunk per article (long articles are split by
paragraph into parts, each part repeating the article heading).

Vectors go into a persistent ChromaDB collection in index/chroma. Embedding is
resumable: only chunks whose id is not already stored get embedded, and each
batch is written as soon as it comes back, so the daily quota or a crash loses
nothing. index/chunks.jsonl keeps the full chunk list (used for BM25).

server.py imports `chunk_file`, `embed_and_store`, `load_collection`.
"""

from __future__ import annotations

import hashlib
import json
import os
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"
CHROMA_DIR = INDEX_DIR / "chroma"
CHUNKS_FILE = INDEX_DIR / "chunks.jsonl"
# One ChromaDB collection per embedding model: vectors from different models
# live in different spaces and must never be mixed. gemini-embedding-2 and its
# preview share one daily quota; gemini-embedding-001 has its own.
COLLECTIONS = {"gemini-embedding-2": "trafico", "gemini-embedding-001": "trafico_e001"}
INDEX_MODELS = list(COLLECTIONS)            # `main.py index` fills both
EMBED_MODEL = os.environ.get("EMBED_MODEL", "gemini-embedding-001")  # what search uses: design G, see REPORT.md
COLLECTION = COLLECTIONS[EMBED_MODEL]
EMBED_DIM = 768
BATCH = 50
MAX_WORDS = 350  # articles longer than this are split into parts

API = "https://www.boe.es/datosabiertos/api/legislacion-consolidada/id/{boe_id}/texto"
PAGE = "https://www.boe.es/buscar/act.php?id={boe_id}"

# Annexes worth indexing per source (None = all). The rest are forms, card
# layouts, exam logistics, medical criteria and the sign catalogue: out of
# scope for "what does the rule say" questions and ~60k words of quota.
ANNEX_KEEP = {
    "LSV": {"Anexo I", "Anexo II", "Anexo III", "Anexo IV", "Anexo VIII", "Anexo IX"},
    "RGC": {"Anexo II", "Anexo III"},
    "RGCond": {"Anexo III"},
    "ITV": set(),  # the inspection manual annexes are long and technical
}

# Corpus: short source name (used in citations and in eval/questions.csv) -> BOE id
DOCUMENTS = {
    "LSV": ("BOE-A-2015-11722", "Ley sobre Tráfico, Circulación de Vehículos a Motor y Seguridad Vial (RDL 6/2015)"),
    "RGC": ("BOE-A-2003-23514", "Reglamento General de Circulación (RD 1428/2003)"),
    "RGCond": ("BOE-A-2009-9481", "Reglamento General de Conductores (RD 818/2009)"),
}
# Held back on purpose: added later through the add_document tool.
EXTRA_DOCUMENTS = {
    "ITV": ("BOE-A-2017-12841", "Real Decreto 920/2017, inspección técnica de vehículos"),
}

SKIP_CLASSES = {"nota_pie", "nota_pie_2", "imagen", "firma_ministro", "firma_rey", "siempreSeVe"}
HEADING_CLASSES = {"titulo_num", "titulo_tit", "titulo", "capitulo_num", "capitulo_tit", "capitulo",
                   "seccion", "subseccion", "anexo_num", "anexo_tit"}


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


# ---------------------------------------------------------------- download

def _get(url: str, accept: str) -> bytes:
    req = urllib.request.Request(url, headers={"Accept": accept, "User-Agent": "daiist-assignment-3"})
    with urllib.request.urlopen(req, timeout=60) as r:
        return r.read()


def download(source: str, boe_id: str) -> Path:
    """Fetch a consolidated BOE text into corpus/ (cached), plus the list of
    blocks the official consolidated page shows (see _shown_blocks)."""
    CORPUS_DIR.mkdir(exist_ok=True)
    path = CORPUS_DIR / f"{source}__{boe_id}.xml"
    if not path.exists():
        path.write_bytes(_get(API.format(boe_id=boe_id), "application/xml"))
        log(f"downloaded {path.name}")
    shown = path.with_suffix(".blocks.txt")
    if not shown.exists():
        page = _get(PAGE.format(boe_id=boe_id), "text/html").decode("utf-8", "ignore")
        ids = re.findall(r"\[Bloque \d+: #([^\]]+)\]", page)
        if ids:
            shown.write_text("\n".join(ids), encoding="utf-8")
    return path


def _shown_blocks(path: Path) -> set[str] | None:
    """Block ids the official consolidated page shows, if we have the list.

    The XML still carries articles that a later reform replaced wholesale
    (RGC arts. 151-173, the old sign rules, superseded in 2025-26) with no
    repeal marker, so they look in force. The BOE web page leaves them out;
    we keep only what it shows."""
    f = path.with_suffix(".blocks.txt")
    return set(f.read_text(encoding="utf-8").split()) if f.exists() else None


# ---------------------------------------------------------------- extract & clean

def _clean(text: str) -> str:
    return " ".join(text.replace("\xa0", " ").split())


def _table_rows(table: ET.Element) -> list[str]:
    """Render an HTML-ish table as one 'cell | cell' line per row.

    Flattening tables with itertext() glued every cell together, so the speed
    table in RGC art. 48 read as one run-on line with no way to tell which
    limit went with which vehicle. One row per line keeps the pairing.
    """
    rows = []
    for tr in table.iter("tr"):
        cells = [_clean("".join(td.itertext())) for td in tr if td.tag in ("td", "th")]
        cells = [c for c in cells if c]
        if cells:
            rows.append(" | ".join(cells))
    return rows


def _current_version(bloque: ET.Element, today: str) -> ET.Element | None:
    """The version in force today (latest fecha_vigencia not in the future)."""
    versions = bloque.findall("version")
    if not versions:
        return None
    in_force = [v for v in versions if (v.get("fecha_vigencia") or "0") <= today]
    return (in_force or versions)[-1]


def _lines(version: ET.Element) -> tuple[str | None, list[str], list[str]]:
    """(article heading, body lines, structural headings) for one version."""
    heading, body, struct = None, [], []
    for el in version:
        if el.tag == "table":
            body.extend(_table_rows(el))
            continue
        # <blockquote> holds the BOE's editorial notes: "téngase en cuenta",
        # "se modifica por...", and sometimes the whole repealed wording
        # ("Redacción anterior: ..."). Indexing those put the old 50 km/h
        # urban limit next to the current 30 km/h one, so they are dropped.
        if el.tag != "p":
            continue
        cls = el.get("class") or ""
        text = _clean("".join(el.itertext()))
        if not text or cls in SKIP_CLASSES:
            continue
        if cls == "articulo":
            heading = text
        elif cls in HEADING_CLASSES:
            struct.append(text)
        else:
            body.append(text)
    return heading, body, struct


def _annex_label(label: str) -> str | None:
    m = re.match(r"ANEXO\s+([IVXLC]+|ÚNICO|UNICO)\b", label.upper())
    return f"Anexo {m.group(1)}" if m else None


def _split_parts(body: list[str]) -> list[list[str]]:
    """Group paragraphs into parts of at most MAX_WORDS (a single longer
    paragraph stays whole rather than being cut mid-sentence)."""
    parts, cur, n = [], [], 0
    for line in body:
        w = len(line.split())
        if cur and n + w > MAX_WORDS:
            parts.append(cur)
            cur, n = [], 0
        cur.append(line)
        n += w
    if cur:
        parts.append(cur)
    return parts


def chunk_file(path: str | Path, source: str | None = None, title: str | None = None,
               annex_keep: set[str] | None = ...) -> list[dict]:
    """Extract, clean and chunk one BOE XML file.

    One chunk per article (parts of <= MAX_WORDS for long ones); annex text is
    chunked the same way under its annex label. Returns dicts with id, text
    (what gets embedded: source + heading + body) and metadata: source,
    boe_id, location (e.g. 'Artículo 20', 'Anexo II', 'Anexo II, Artículo 3'),
    heading, section, part, url, version_date, words, text_hash.
    """
    path = Path(path)
    stem = path.stem
    source = source or stem.split("__")[0]
    boe_id = stem.split("__")[-1] if "__" in stem else stem
    title = title or {**DOCUMENTS, **EXTRA_DOCUMENTS}.get(source, (boe_id, source))[1]
    if annex_keep is ...:
        annex_keep = ANNEX_KEEP.get(source)  # None = keep every annex
    today = date.today().strftime("%Y%m%d")

    root = ET.parse(path).getroot()
    if root.findtext("status/code") not in (None, "200"):
        raise ValueError(f"{path.name} is not a BOE text: {root.findtext('status/text')}")

    shown = _shown_blocks(path)
    # RGC and RGCond are approved by a short decree whose own dispositions
    # come before the regulation; the LSV likewise sits inside an approving
    # RDL. Both have e.g. a "Disposición final primera", so we prefix the
    # wrapper's ones until the regulation's own text starts.
    raw = path.read_text(encoding="utf-8", errors="ignore")
    wrapper = bool(re.search(r">\s*(REGLAMENTO GENERAL|TEXTO REFUNDIDO)", raw))
    chunks: list[dict] = []
    section: dict[str, str] = {}
    annex: str | None = None

    def emit(bid: str, location: str, heading: str, body: list[str], version) -> None:
        parts = _split_parts(body)
        for i, lines in enumerate(parts, 1):
            label = heading + (f" (parte {i}/{len(parts)})" if len(parts) > 1 else "")
            text = f"[{source} · {title}]\n{label}\n" + "\n".join(lines)
            chunks.append({
                "id": f"{source}:{bid}:{i}",
                "text": text,
                "metadata": {
                    "source": source,
                    "boe_id": boe_id,
                    "doc_title": title,
                    "location": location,
                    "heading": heading,
                    "section": " > ".join(v for v in section.values() if v),
                    "part": i,
                    "parts": len(parts),
                    "url": f"https://www.boe.es/buscar/act.php?id={boe_id}#{bid}",
                    "version_date": version.get("fecha_vigencia") or "",
                    "words": sum(len(x.split()) for x in lines),
                    "text_hash": hashlib.sha1(text.encode()).hexdigest()[:12],
                },
            })

    for bloque in root.iter("bloque"):
        tipo, bid = bloque.get("tipo"), bloque.get("id")
        if shown is not None and bid not in shown:
            continue
        version = _current_version(bloque, today)
        # the preamble explains why the law changed, not what it says: skip
        if version is None or tipo in ("nota_inicial", "firma", "preambulo"):
            continue
        heading, body, struct = _lines(version)
        words = sum(len(x.split()) for x in body)

        if tipo == "encabezado":
            if wrapper and body and re.match(r"(REGLAMENTO GENERAL|TEXTO REFUNDIDO)", body[0]):
                wrapper = False
                continue
            label = " ".join(struct)
            up = label.upper()
            new_annex = _annex_label(label)
            if new_annex:
                annex = new_annex
                section = {"anexo": label}
            elif up.startswith(("TÍTULO", "TITULO", "LIBRO")):
                annex, section = None, {"titulo": label}
            elif up.startswith(("CAPÍTULO", "CAPITULO")):
                section = {k: v for k, v in section.items() if k in ("titulo", "anexo")} | {"capitulo": label}
            elif label:
                section = {**section, "seccion": label}
            # annexes keep their text inside the heading block
            keep = annex and (annex_keep is None or annex in annex_keep)
            if keep and words > 30:
                sub = "" if new_annex else (label or "").split(".")[0]
                location = annex + (f", {sub}" if sub else "")
                emit(bid, location, label or annex, body, version)
            continue

        if not body or tipo != "precepto":
            continue
        if annex and annex_keep is not None and annex not in annex_keep:
            continue
        location = _clean(bloque.get("titulo") or bid)
        if annex:
            location = f"{annex}, {location}"
        elif wrapper:
            location = f"Norma aprobatoria, {location}"
        emit(bid, location, heading or location, body, version)
    return chunks


# ---------------------------------------------------------------- embed & store

_client = None


def gemini():
    global _client
    if _client is None:
        from google import genai
        from api_key import load_api_key
        _client = genai.Client(api_key=load_api_key())
    return _client


def embed(texts: list[str], task: str = "RETRIEVAL_DOCUMENT", model: str | None = None) -> list[list[float]]:
    """Embed a batch. gemini-embedding-2 merges a plain list of strings into
    ONE vector, so each text is wrapped in its own Content."""
    from google.genai import types
    cfg = types.EmbedContentConfig(task_type=task, output_dimensionality=EMBED_DIM)
    contents = [types.Content(parts=[types.Part(text=t)]) for t in texts]
    for attempt in range(6):
        try:
            r = gemini().models.embed_content(model=model or EMBED_MODEL, contents=contents, config=cfg)
            vecs = [e.values for e in r.embeddings]
            assert len(vecs) == len(texts), "embedding count mismatch"
            return vecs
        except Exception as e:  # rate limits / dropped connections: back off, then give up loudly
            msg = str(e)
            if any(t in type(e).__name__ for t in ("ProtocolError", "ConnectError", "ReadTimeout", "ReadError")) or "503" in msg:
                if attempt == 5:
                    raise
                time.sleep(3 * (attempt + 1))
            elif "429" in msg or "RESOURCE_EXHAUSTED" in msg:
                if "per day" in msg.lower() or attempt == 5:
                    raise
                wait = 20 * (attempt + 1)
                log(f"rate limited, waiting {wait}s")
                time.sleep(wait)
            else:
                raise
    raise RuntimeError("unreachable")


def load_collection(model: str | None = None):
    import chromadb
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    from chromadb.config import Settings
    client = chromadb.PersistentClient(path=str(CHROMA_DIR), settings=Settings(anonymized_telemetry=False))
    # embedding_function=None: we always pass our own Gemini vectors, and
    # Chroma must never fall back to its default local model.
    model = model or EMBED_MODEL
    return client.get_or_create_collection(COLLECTIONS[model], metadata={"hnsw:space": "cosine"},
                                           embedding_function=None)


def embed_and_store(chunks: list[dict], collection=None, prune_source: str | None = None) -> tuple[int, int]:
    """Embed chunks that have no stored vector for their current text; store
    each batch at once. A chunk whose text changed is re-embedded; one whose
    text is the same but metadata changed only gets its metadata updated.
    With prune_source, stored chunks of that source that are no longer
    produced are deleted. Returns (newly embedded, already present)."""
    col = collection or load_collection()
    ids = [c["id"] for c in chunks]
    stored = col.get(ids=ids, include=["metadatas"]) if chunks else {"ids": [], "metadatas": []}
    old_hash = {i: (m or {}).get("text_hash") for i, m in zip(stored["ids"], stored["metadatas"])}
    todo, relabel = [], []
    for c in chunks:
        if c["id"] not in old_hash:
            todo.append(c)
        elif old_hash[c["id"]] not in (None, c["metadata"]["text_hash"]):
            todo.append(c)  # text changed: new vector
        else:
            relabel.append(c)
    if relabel:
        col.update(ids=[c["id"] for c in relabel], metadatas=[c["metadata"] for c in relabel])
    if prune_source:
        current = set(ids)
        stale = [i for i, m in zip(*_all(col, prune_source)) if i not in current]
        if stale:
            col.delete(ids=stale)
            log(f"  removed {len(stale)} stale chunks of {prune_source}")
    for i in range(0, len(todo), BATCH):
        batch = todo[i:i + BATCH]
        vecs = embed([c["text"] for c in batch], model=model_of(col))
        col.upsert(ids=[c["id"] for c in batch], embeddings=vecs,
                   documents=[c["text"] for c in batch], metadatas=[c["metadata"] for c in batch])
        log(f"  embedded {min(i + BATCH, len(todo))}/{len(todo)}")
    _write_chunks_file(col)
    return len(todo), len(chunks) - len(todo)


def model_of(col) -> str:
    """The embedding model a collection's vectors come from."""
    return {v: k for k, v in COLLECTIONS.items()}[col.name]


def chunks_file(col) -> Path:
    """index/chunks.jsonl mirrors the gemini-embedding-2 collection; other
    collections get their own mirror (they can differ after add_document)."""
    return CHUNKS_FILE if col.name == "trafico" else INDEX_DIR / f"chunks_{col.name}.jsonl"


def _all(col, source: str):
    got = col.get(where={"source": source}, include=["metadatas"])
    return got["ids"], got["metadatas"]


def _write_chunks_file(col) -> None:
    """Mirror the collection to chunks.jsonl (for BM25 and for reading)."""
    got = col.get(include=["documents", "metadatas"])
    rows = sorted(zip(got["ids"], got["documents"], got["metadatas"]), key=lambda r: r[0])
    with chunks_file(col).open("w", encoding="utf-8") as f:
        for cid, doc, meta in rows:
            f.write(json.dumps({"id": cid, "text": doc, "metadata": meta}, ensure_ascii=False, sort_keys=True) + "\n")  # sorted: Chroma returns keys in varying order


def indexed_sources(col=None) -> dict[str, str]:
    """source -> version_date for every document in the index."""
    col = col or load_collection()
    out = {}
    for m in col.get(include=["metadatas"])["metadatas"]:
        out[m["source"]] = max(out.get(m["source"], ""), m.get("version_date", ""))
    return out


def main() -> None:
    for model in INDEX_MODELS:
        col = load_collection(model)
        total_new = 0
        for source, (boe_id, title) in DOCUMENTS.items():
            path = download(source, boe_id)
            chunks = chunk_file(path, source, title)
            words = sum(c["metadata"]["words"] for c in chunks)
            log(f"[{model}] {source}: {len(chunks)} chunks, {words} words")
            new, old = embed_and_store(chunks, col, prune_source=source)
            total_new += new
            log(f"[{model}] {source}: embedded {new}, already stored {old}")
        print(f"[{model}] {col.count()} chunks in collection {col.name} ({total_new} newly embedded).")
    print(f"Index ready in {CHROMA_DIR.relative_to(ROOT)}; search uses {EMBED_MODEL}.")


if __name__ == "__main__":
    main()
