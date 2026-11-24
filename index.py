"""
Assignment 3: build the index (`main.py index`).

Corpus: Spanish residential rental law, consolidated texts from the BOE open-data
API (https://www.boe.es/datosabiertos/), reusable under the BOE reuse conditions
(Real Decreto 1495/2011 / aviso legal BOE: free reuse citing the source).

Pipeline per file (server.py's add_document imports these):
    parse_file(path)            -> list of units (article / preamble paragraph runs)
    chunk_file(path, design)    -> list of chunk dicts with source + location metadata
    embed_and_store(chunks, collection) -> embeds only chunks not yet stored

Two retrieval designs, each in its own ChromaDB collection in index/:
    articles  - one chunk per article (long articles split on paragraph boundaries)
    fixed200  - fixed 200-word windows with 50-word overlap, ignoring structure
"""

from __future__ import annotations

import hashlib
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"

BOE_API = "https://www.boe.es/datosabiertos/api/legislacion-consolidada/id/{id}/texto"
BOE_URL = "https://www.boe.es/buscar/act.php?id={id}"

# The indexed corpus. `source` is the name used in citations and in eval/questions.csv.
DOCUMENTS = {
    "BOE-A-1994-26003": "LAU (Ley 29/1994)",
    "BOE-A-2023-12203": "Ley 12/2023 de vivienda",
    "BOE-A-2019-3108": "RDL 7/2019",
}
# Known but NOT indexed by `main.py index`: added later through add_document (the before/after demo).
EXTRA_DOCUMENTS = {
    "BOE-A-1960-10906": "LPH (Ley 49/1960)",
}

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768          # smaller vectors keep index/ well under 90 MB
EMBED_BATCH = 50
DESIGNS = ("articles", "fixed200")
DEFAULT_DESIGN = "articles"

MAX_ARTICLE_WORDS = 400  # longer articles are split on paragraph boundaries
FIXED_WORDS, FIXED_OVERLAP = 200, 50


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)  # stdout belongs to the MCP protocol in server.py


# --------------------------------------------------------------------------- download

def download(boe_id: str, force: bool = False) -> Path:
    """Fetch a consolidated law as XML into corpus/ (skipped if already there)."""
    CORPUS_DIR.mkdir(exist_ok=True)
    path = CORPUS_DIR / f"{boe_id}.xml"
    if path.exists() and not force:
        return path
    req = urllib.request.Request(BOE_API.format(id=boe_id), headers={"Accept": "application/xml"})
    with urllib.request.urlopen(req, timeout=60) as r:
        path.write_bytes(r.read())
    log(f"downloaded {boe_id} -> {path.relative_to(ROOT)}")
    return path


# --------------------------------------------------------------------------- extract + clean

def clean(text: str) -> str:
    text = text.replace("\xa0", " ")
    return re.sub(r"\s+", " ", text).strip()


def source_for(path: Path) -> tuple[str, str]:
    """(doc_id, source name) for a file, using the known BOE ids or the file name."""
    doc_id = path.stem
    name = DOCUMENTS.get(doc_id) or EXTRA_DOCUMENTS.get(doc_id) or doc_id
    return doc_id, name


def parse_boe_xml(path: Path) -> list[dict]:
    """Units of a BOE consolidated XML: one per article/provision, preamble kept as one unit.

    Cleaning decisions:
      * a block holds every historical version of the article; only the LAST is kept;
      * `nota_pie*` paragraphs ("Se modifica por...") are editorial notes, dropped;
      * `encabezado` blocks (TÍTULO / CAPÍTULO) are not indexed alone but kept as
        the heading path of the articles beneath them;
      * signature blocks are dropped.
    """
    root = ET.parse(path).getroot()
    units, heading = [], {}
    for block in root.iter("bloque"):
        versions = block.findall("version")
        if not versions:
            continue
        latest = versions[-1]
        paras = [(p.get("class") or "", clean("".join(p.itertext()))) for p in latest.iter("p")]
        paras = [(c, t) for c, t in paras if t and not c.startswith("nota_pie")]
        kind, title = block.get("tipo"), block.get("titulo") or ""

        if kind == "encabezado":
            level = "titulo" if title.upper().startswith(("TÍTULO", "LIBRO")) else "capitulo"
            name = " ".join(t for _, t in paras)
            heading[level] = name or title
            if level == "titulo":
                heading.pop("capitulo", None)
            continue
        if kind == "firma" or not paras:
            continue

        if kind == "preambulo":
            location = "Preámbulo"
            first = ""
        else:
            location = title or block.get("id", "")
            # first paragraph is usually "Artículo 9. Plazo mínimo." -> keep as article title
            first = paras[0][1] if paras[0][0] == "articulo" else ""
        body = [t for c, t in paras if not (first and t == first)]
        head = " / ".join(v for v in (heading.get("titulo"), heading.get("capitulo")) if v)
        # Fix: BOE puts amendments that are not yet in force INSIDE the current text,
        # after a "Téngase en cuenta que, con efectos de <date>, se modifica ..." line.
        # Split them into their own unit, labelled with the date, so current and future
        # rules are never mixed in one chunk.
        future = next((i for i, t in enumerate(body) if FUTURE_RE.match(t)), None)
        current_body, future_body = (body, []) if future is None else (body[:future], body[future:])
        units.append({"location": location, "heading": head, "title": first,
                      "paragraphs": current_body, "block_id": block.get("id", "")})
        if future_body:
            date = FUTURE_RE.match(future_body[0]).group(1)
            label = f"{(first or location).rstrip('.')} [redacción futura, en vigor desde el {date}]"
            units.append({"location": label, "heading": head, "title": label,
                          "paragraphs": future_body, "block_id": block.get("id", "") + "-futura"})
    return units


FUTURE_RE = re.compile(r"Téngase en cuenta que, con efectos de (\d{1,2} de \w+ de \d{4})")


ARTICLE_RE = re.compile(r"^(Art[íi]culo\s+\d+(?:\s+(?:bis|ter|quater))?\.?|Disposici[óo]n\s+\w+\s+\w+\.?)", re.I)


def parse_plain_text(text: str) -> list[dict]:
    """Fallback for .txt/.md/.pdf files: split on lines starting with 'Artículo N'."""
    units, current = [], {"location": "Inicio", "heading": "", "title": "", "paragraphs": [], "block_id": ""}
    for line in (clean(l) for l in text.splitlines()):
        if not line:
            continue
        m = ARTICLE_RE.match(line)
        if m:
            if current["paragraphs"] or current["title"]:
                units.append(current)
            current = {"location": m.group(1).rstrip("."), "heading": "", "title": line,
                       "paragraphs": [], "block_id": ""}
        else:
            current["paragraphs"].append(line)
    if current["paragraphs"] or current["title"]:
        units.append(current)
    return units


def parse_file(path: str | Path) -> list[dict]:
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix == ".xml":
        return parse_boe_xml(path)
    if suffix == ".pdf":
        from pypdf import PdfReader
        text = "\n".join(page.extract_text() or "" for page in PdfReader(str(path)).pages)
        return parse_plain_text(text)
    if suffix in (".txt", ".md"):
        return parse_plain_text(path.read_text(encoding="utf-8"))
    raise ValueError(f"Unsupported file type {suffix!r}: use a BOE .xml, .pdf, .txt or .md file")


# --------------------------------------------------------------------------- chunk

def _chunk(doc_id: str, source: str, location: str, heading: str, part: int, text: str, design: str) -> dict:
    header = f"{source} — {location}" + (f" ({heading})" if heading else "")
    full = f"{header}\n{text}"
    slug = re.sub(r"[^a-z0-9]+", "-", location.lower()).strip("-")
    return {
        "id": f"{design}:{doc_id}:{slug}:{part}",
        "text": full,
        "metadata": {
            "doc_id": doc_id,
            "source": source,
            "location": location,
            "heading": heading,
            "part": part,
            "url": BOE_URL.format(id=doc_id) if doc_id.startswith("BOE-") else "",
            "words": len(full.split()),
            "hash": hashlib.sha256(full.encode()).hexdigest()[:16],
            "design": design,
        },
    }


def _pack(paragraphs: list[str], limit: int) -> list[str]:
    """Group paragraphs into pieces of at most ~limit words, never splitting a paragraph."""
    pieces, cur, n = [], [], 0
    for p in paragraphs:
        w = len(p.split())
        if cur and n + w > limit:
            pieces.append(" ".join(cur))
            cur, n = [], 0
        cur.append(p)
        n += w
    if cur:
        pieces.append(" ".join(cur))
    return pieces


def chunk_by_article(path: Path) -> list[dict]:
    doc_id, source = source_for(path)
    chunks = []
    for u in parse_file(path):
        location = u["location"]
        if u["title"]:
            # "Artículo 9. Plazo mínimo." -> location "Artículo 9. Plazo mínimo"
            location = u["title"].rstrip(".")
        for part, piece in enumerate(_pack(u["paragraphs"] or [u["title"]], MAX_ARTICLE_WORDS), start=1):
            chunks.append(_chunk(doc_id, source, location, u["heading"], part, piece, "articles"))
    return chunks


def chunk_fixed(path: Path, size: int = FIXED_WORDS, overlap: int = FIXED_OVERLAP) -> list[dict]:
    """Structure-blind windows; location = the article where the window starts."""
    doc_id, source = source_for(path)
    words, owner = [], []
    for u in parse_file(path):
        loc = u["title"].rstrip(".") if u["title"] else u["location"]
        for w in " ".join(u["paragraphs"]).split():
            words.append(w)
            owner.append(loc)
    chunks, step = [], size - overlap
    for i, start in enumerate(range(0, max(len(words) - overlap, 1), step), start=1):
        window = words[start:start + size]
        end_loc = owner[min(start + size, len(owner)) - 1]
        loc = owner[start] if owner[start] == end_loc else f"{owner[start]} → {end_loc}"
        chunks.append(_chunk(doc_id, source, loc, "", i, " ".join(window), "fixed200"))
    return chunks


def chunk_file(path: str | Path, design: str = DEFAULT_DESIGN) -> list[dict]:
    path = Path(path)
    if design == "articles":
        return chunk_by_article(path)
    if design == "fixed200":
        return chunk_fixed(path)
    raise ValueError(f"unknown design {design!r}")


# --------------------------------------------------------------------------- embed + store

_client = None
_chroma = None


def genai_client():
    global _client
    if _client is None:
        from google import genai
        from api_key import load_api_key
        _client = genai.Client(api_key=load_api_key())
    return _client


def embed(texts: list[str], task: str = "RETRIEVAL_DOCUMENT") -> list[list[float]]:
    """Embed a batch, retrying on rate limits. One vector per text, checked."""
    from google.genai import types
    contents = [types.Content(parts=[types.Part(text=t)]) for t in texts]
    config = types.EmbedContentConfig(task_type=task, output_dimensionality=EMBED_DIM)
    for attempt in range(6):
        try:
            resp = genai_client().models.embed_content(model=EMBED_MODEL, contents=contents, config=config)
            vectors = [e.values for e in resp.embeddings]
            if len(vectors) != len(texts):
                raise RuntimeError(f"asked for {len(texts)} embeddings, got {len(vectors)}")
            return vectors
        except Exception as e:  # noqa: BLE001
            msg = str(e)
            if ("429" in msg or "RESOURCE_EXHAUSTED" in msg or "503" in msg) and attempt < 5:
                if "PerDay" in msg or "per day" in msg.lower():
                    raise RuntimeError("Daily embedding quota reached. Vectors so far are saved; "
                                       "run `main.py index` again tomorrow.") from e
                wait = 15 * (attempt + 1)
                log(f"  rate limited, waiting {wait}s ...")
                time.sleep(wait)
                continue
            raise


QUERY_CACHE = INDEX_DIR / "query_cache.json"
_query_cache: dict | None = None


def embed_query(query: str) -> list[float]:
    """Embed a search query, cached on disk: the same query never costs quota twice."""
    import json
    global _query_cache
    if _query_cache is None:
        _query_cache = json.loads(QUERY_CACHE.read_text()) if QUERY_CACHE.exists() else {}
    key = f"{EMBED_MODEL}:{EMBED_DIM}:{query.strip()}"
    if key not in _query_cache:
        _query_cache[key] = embed([query], task="RETRIEVAL_QUERY")[0]
        INDEX_DIR.mkdir(exist_ok=True)
        QUERY_CACHE.write_text(json.dumps(_query_cache))
    return _query_cache[key]


def chroma():
    global _chroma
    if _chroma is None:
        import chromadb
        from chromadb.config import Settings
        INDEX_DIR.mkdir(exist_ok=True)
        _chroma = chromadb.PersistentClient(path=str(INDEX_DIR), settings=Settings(anonymized_telemetry=False))
    return _chroma


def collection(design: str = DEFAULT_DESIGN):
    return chroma().get_or_create_collection(design, metadata={"hnsw:space": "cosine"})


def embed_and_store(chunks: list[dict], coll=None) -> int:
    """Store chunks; embed only those whose id+hash is not already saved. Returns # embedded.

    Each batch is written to ChromaDB as soon as it is embedded, so hitting the
    daily quota or crashing loses nothing.
    """
    if not chunks:
        return 0
    coll = coll or collection(chunks[0]["metadata"]["design"])
    existing = coll.get(ids=[c["id"] for c in chunks], include=["metadatas"])
    saved = {i: m.get("hash") for i, m in zip(existing["ids"], existing["metadatas"])}
    todo = [c for c in chunks if saved.get(c["id"]) != c["metadata"]["hash"]]
    for i in range(0, len(todo), EMBED_BATCH):
        batch = todo[i:i + EMBED_BATCH]
        vectors = embed([c["text"] for c in batch])
        coll.upsert(ids=[c["id"] for c in batch], embeddings=vectors,
                    documents=[c["text"] for c in batch], metadatas=[c["metadata"] for c in batch])
        log(f"  embedded {min(i + EMBED_BATCH, len(todo))}/{len(todo)} new chunks")
    return len(todo)


def remove_stale(doc_id: str, keep_ids: set[str], coll) -> int:
    """Delete chunks of doc_id that are no longer produced (document changed)."""
    old = coll.get(where={"doc_id": doc_id}, include=[])["ids"]
    stale = [i for i in old if i not in keep_ids]
    if stale:
        coll.delete(ids=stale)
    return len(stale)


def index_file(path: str | Path, designs=DESIGNS) -> dict:
    """Chunk, embed and store one file in every design. Idempotent: an unchanged,
    already-indexed file costs no embeddings; a changed one replaces its old chunks."""
    path = Path(path)
    report = {}
    for design in designs:
        coll = collection(design)
        chunks = chunk_file(path, design)
        new = embed_and_store(chunks, coll)
        stale = remove_stale(source_for(path)[0], {c["id"] for c in chunks}, coll)
        report[design] = {"chunks": len(chunks), "embedded": new, "removed": stale}
    return report


# --------------------------------------------------------------------------- search (used by server.py and evaluate.py)

def search(query: str, k: int = 5, design: str = DEFAULT_DESIGN, query_vector=None,
           where: dict | None = None) -> list[dict]:
    vec = query_vector if query_vector is not None else embed_query(query)
    res = collection(design).query(query_embeddings=[vec], n_results=k, where=where,
                                   include=["documents", "metadatas", "distances"])
    return [{"id": i, "text": d, "score": round(1 - dist, 4), **m}
            for i, d, m, dist in zip(res["ids"][0], res["documents"][0], res["metadatas"][0], res["distances"][0])]


# --------------------------------------------------------------------------- main

def main() -> None:
    dry = "--dry-run" in sys.argv  # chunk and report, no embeddings
    paths = [download(boe_id) for boe_id in DOCUMENTS]
    for design in DESIGNS:
        total_chunks = total_words = 0
        for p in paths:
            chunks = chunk_file(p, design)
            words = sum(len(c["text"].split()) for c in chunks)
            total_chunks += len(chunks)
            total_words += words
            log(f"[{design}] {source_for(p)[1]}: {len(chunks)} chunks, {words} words")
        log(f"[{design}] total: {total_chunks} chunks, {total_words} words "
            f"(avg {total_words // max(total_chunks, 1)} words/chunk)")
    if dry:
        return
    for p in paths:
        log(f"indexing {source_for(p)[1]} ...")
        log(f"  {index_file(p)}")
    for design in DESIGNS:
        log(f"[{design}] collection holds {collection(design).count()} chunks")


if __name__ == "__main__":
    main()
