"""
Assignment 3: build the index (`main.py index`).

Corpus: three Spanish housing laws, consolidated text from the BOE open-data API.
Pipeline per file: parse -> clean -> chunk (with source + location metadata)
-> embed with Gemini -> store in ChromaDB under index/.

Two chunking designs are built so evaluate.py can compare them:
  - "articles": structure-based. One chunk per article (or disposición), long
    articles split at paragraph boundaries into pieces of <= 300 words.
  - "fixed200": fixed 200-word windows over the whole law, ignoring structure.
    Each chunk records every article it spans.

Vectors are saved after every batch, and only chunks without a saved vector are
embedded, so a crash or the daily free-tier limit loses nothing: re-run tomorrow.

server.py's add_document imports `chunk_file` and `embed_and_store` from here.
"""

from __future__ import annotations

import hashlib
import html
import re
import sys
import time
from pathlib import Path

import chromadb
import httpx
from google import genai
from google.genai import types
from pypdf import PdfReader

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"
CHROMA_DIR = INDEX_DIR / "chroma"

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768
BATCH = 50

DESIGNS = {"articles": 300, "fixed200": 200}  # design name -> max words per chunk
DEFAULT_DESIGN = "articles"  # the design add_document uses

BOE_API = "https://www.boe.es/datosabiertos/api/legislacion-consolidada/id/{boe_id}"
BOE_HTML = "https://www.boe.es/buscar/act.php?id={boe_id}"

# The corpus. `source` is the short name used in citations and in eval/questions.csv.
CORPUS = [
    {"source": "LAU", "boe_id": "BOE-A-1994-26003", "title": "Ley 29/1994, de 24 de noviembre, de Arrendamientos Urbanos"},
    {"source": "LDV", "boe_id": "BOE-A-2023-12203", "title": "Ley 12/2023, de 24 de mayo, por el derecho a la vivienda"},
    {"source": "LPH", "boe_id": "BOE-A-1960-10906", "title": "Ley 49/1960, de 21 de julio, sobre propiedad horizontal"},
]


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


# ---------------------------------------------------------------- download

def download(doc: dict) -> Path:
    """Fetch the consolidated XML for one law into corpus/ (cached)."""
    CORPUS_DIR.mkdir(exist_ok=True)
    path = CORPUS_DIR / f"{doc['boe_id']}.xml"
    if not path.exists():
        log(f"Downloading {doc['source']} ({doc['boe_id']}) ...")
        r = httpx.get(BOE_API.format(boe_id=doc["boe_id"]), headers={"Accept": "application/xml"}, timeout=120)
        r.raise_for_status()
        path.write_bytes(r.content)
    return path


# ---------------------------------------------------------------- parse + clean

def _clean(text: str) -> str:
    text = html.unescape(re.sub(r"<[^>]+>", "", text))
    return re.sub(r"\s+", " ", text).strip()


def parse_boe(path: Path) -> tuple[dict, list[dict]]:
    """Return (document info, units). A unit is one article, disposición or preamble part.

    The BOE consolidated XML keeps EVERY historical version of each article.
    We keep only the last (current) one; otherwise repealed wording would be
    indexed next to the law in force. Footnotes (nota_pie) are editorial notes
    and are dropped.
    """
    x = path.read_text(encoding="utf-8", errors="ignore")
    boe_id = re.search(r"<identificador>([^<]+)", x).group(1)
    title = _clean(re.search(r"<titulo>([^<]+)", x).group(1)).rstrip(".")
    updated = re.search(r"<fecha_actualizacion>(\d{8})", x).group(1)
    known = next((d for d in CORPUS if d["boe_id"] == boe_id), None)
    source = known["source"] if known else boe_id
    info = {"source": source, "boe_id": boe_id, "title": title, "url": BOE_HTML.format(boe_id=boe_id),
            "version_date": f"{updated[:4]}-{updated[4:6]}-{updated[6:]}"}

    units, section = [], ""
    for block in re.findall(r"<bloque\b.*?</bloque>", x, re.S):
        kind = re.search(r'tipo="([^"]+)"', block).group(1)
        name_match = re.search(r'titulo="([^"]*)"', block)
        # the LDV writes "Artículo\xa01" (non-breaking space); normalise so citations match plain text
        name = _clean(name_match.group(1)) if name_match else ""
        versions = re.findall(r"<version\b(.*?)>(.*?)</version>", block, re.S)
        if not versions:
            continue
        attrs, body = versions[-1]
        since_match = re.search(r'fecha_vigencia="(\d{8})"', attrs)
        since = since_match.group(1) if since_match else ""
        paras = [(c, _clean(t)) for c, t in re.findall(r'<p class="([^"]+)"[^>]*>(.*?)</p>', body, re.S)]
        paras = [(c, t) for c, t in paras if t and not c.startswith("nota_pie")]

        if kind == "encabezado":  # TÍTULO / CAPÍTULO headings: keep as context
            section = " ".join(t for _, t in paras)
            continue
        if kind == "preambulo":
            # split the preamble at its roman-numeral subsections (I, II, ...)
            part, current = "Preámbulo", []
            for c, t in paras:
                if c == "subseccion" and re.fullmatch(r"[IVXL]+|\d+", t):
                    if current:
                        units.append({"location": part, "section": "Preámbulo", "paras": current, "since": since})
                    part, current = f"Preámbulo, apartado {t}", []
                elif c == "subseccion":
                    continue  # "JUAN CARLOS I", "PREÁMBULO" headers
                else:
                    current.append(t)
            if current:
                units.append({"location": part, "section": "Preámbulo", "paras": current, "since": since})
            continue
        if kind != "precepto":
            continue  # firma (signatures)
        texts = [t for _, t in paras]
        if sum(len(t.split()) for t in texts[1:]) < 8:
            continue  # "(Sin contenido)" / repealed placeholders
        units.append({"location": name or texts[0][:40], "section": section, "paras": texts, "since": since})
    return info, units


def parse_generic(path: Path) -> tuple[dict, list[dict]]:
    """PDF (one unit per page), or HTML/TXT/MD (one unit per heading section)."""
    suffix = path.suffix.lower()
    info = {"source": path.stem, "boe_id": "", "title": path.stem, "url": str(path), "version_date": ""}
    units = []
    if suffix == ".pdf":
        for i, page in enumerate(PdfReader(str(path)).pages, start=1):
            text = re.sub(r"[ \t]+", " ", page.extract_text() or "")
            paras = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
            if paras:
                units.append({"location": f"página {i}", "section": "", "paras": paras, "since": ""})
        return info, units
    raw = path.read_text(encoding="utf-8", errors="ignore")
    if suffix in (".html", ".htm"):
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(raw, "html.parser")
        if soup.title and soup.title.string:
            info["title"] = soup.title.string.strip()
        lines = [(el.name, el.get_text(" ", strip=True)) for el in soup.find_all(["h1", "h2", "h3", "h4", "p", "li"])]
    else:
        lines = [("h" if l.startswith("#") else "p", l.lstrip("# ").strip()) for l in raw.splitlines()]
    heading, current = "Inicio", []
    for tag, text in lines:
        if not text:
            continue
        if tag.startswith("h"):
            if current:
                units.append({"location": heading, "section": "", "paras": current, "since": ""})
            heading, current = text[:80], []
        else:
            current.append(text)
    if current:
        units.append({"location": heading, "section": "", "paras": current, "since": ""})
    return info, units


# ---------------------------------------------------------------- chunk

def _split_paragraphs(paras: list[str], max_words: int) -> list[list[str]]:
    """Group paragraphs into pieces of <= max_words; a single huge paragraph is cut by words."""
    pieces, current, n = [], [], 0
    for p in paras:
        words = p.split()
        while len(words) > max_words:  # oversized paragraph
            if current:
                pieces.append(current)
                current, n = [], 0
            pieces.append([" ".join(words[:max_words])])
            words = words[max_words:]
        if not words:
            continue
        if n + len(words) > max_words and current:
            pieces.append(current)
            current, n = [], 0
        current.append(" ".join(words))
        n += len(words)
    if current:
        pieces.append(current)
    return pieces


def _chunk(info: dict, location: str, section: str, text: str, part: int, parts: int,
           since: str, design: str, locations: list[str] | None = None) -> dict:
    label = location if parts == 1 else f"{location} (parte {part}/{parts})"
    header = f"{info['source']} – {info['title']} – {label}"
    meta = {
        "source": info["source"], "title": info["title"], "location": location,
        "locations": ";".join(locations or [location]), "part": part, "parts": parts,
        "section": section, "url": info["url"], "version_date": info["version_date"],
        "in_force_since": since, "design": design, "words": len(text.split()),
    }
    # the header is embedded too: it tells the model which law and article this is
    full = f"{header}\n{text}"
    chunk_id = hashlib.sha1(f"{design}|{full}".encode()).hexdigest()[:20]
    return {"id": chunk_id, "text": full, "metadata": meta}


def chunk_articles(info: dict, units: list[dict], max_words: int = DESIGNS["articles"]) -> list[dict]:
    chunks = []
    for u in units:
        pieces = _split_paragraphs(u["paras"], max_words)
        for i, piece in enumerate(pieces, start=1):
            chunks.append(_chunk(info, u["location"], u["section"], "\n".join(piece), i, len(pieces),
                                 u["since"], "articles"))
    return chunks


def chunk_fixed(info: dict, units: list[dict], size: int = DESIGNS["fixed200"]) -> list[dict]:
    """Fixed windows of `size` words across the whole document, ignoring article boundaries."""
    stream = [(w, u["location"]) for u in units for p in u["paras"] for w in p.split()]
    chunks = []
    for start in range(0, len(stream), size):
        window = stream[start:start + size]
        locs = list(dict.fromkeys(loc for _, loc in window))
        label = locs[0] if len(locs) == 1 else f"{locs[0]} – {locs[-1]}"
        chunks.append(_chunk(info, label, "", " ".join(w for w, _ in window), 1, 1, "", "fixed200", locs))
    return chunks


def chunk_file(path: str | Path, design: str = DEFAULT_DESIGN) -> list[dict]:
    """Parse, clean and chunk one file. BOE XML, PDF, HTML, TXT or MD."""
    path = Path(path)
    if path.suffix.lower() == ".xml":
        info, units = parse_boe(path)
    else:
        info, units = parse_generic(path)
    if not units:
        raise ValueError(f"No text could be extracted from {path.name}.")
    return chunk_articles(info, units) if design == "articles" else chunk_fixed(info, units)


# ---------------------------------------------------------------- embed + store

class QuotaExhausted(RuntimeError):
    pass


_client: genai.Client | None = None


def client() -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client(api_key=load_api_key())
    return _client


def embed(texts: list[str], task: str = "RETRIEVAL_DOCUMENT") -> list[list[float]]:
    """Embed a batch, retrying briefly on per-minute rate limits."""
    for attempt in range(5):
        try:
            # one Content per text: a plain list of strings is embedded as ONE multimodal input
            r = client().models.embed_content(
                model=EMBED_MODEL, contents=[types.Content(parts=[types.Part(text=t)]) for t in texts],
                config=types.EmbedContentConfig(task_type=task, output_dimensionality=EMBED_DIM),
            )
            if len(r.embeddings) != len(texts):
                raise RuntimeError(f"asked for {len(texts)} embeddings, got {len(r.embeddings)}")
            return [e.values for e in r.embeddings]
        except Exception as error:  # noqa: BLE001
            msg = str(error)
            if "429" not in msg and "RESOURCE_EXHAUSTED" not in msg:
                raise
            if "PerDay" in msg or "per day" in msg.lower() or attempt == 4:
                raise QuotaExhausted(msg) from error
            wait = 30 * (attempt + 1)
            log(f"  rate limited, waiting {wait}s ...")
            time.sleep(wait)
    raise RuntimeError("unreachable")


_db = None


def collection(design: str):
    global _db
    if _db is None:
        _db = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return _db.get_or_create_collection(design, metadata={"hnsw:space": "cosine"})


def embed_and_store(chunks: list[dict], design: str = DEFAULT_DESIGN) -> dict:
    """Embed only the chunks whose id is not stored yet, saving after every batch.

    Returns counts: {"new": embedded now, "existing": already stored}.
    """
    col = collection(design)
    ids = [c["id"] for c in chunks]
    existing = set(col.get(ids=ids, include=[])["ids"]) if ids else set()
    todo = [c for c in chunks if c["id"] not in existing]
    for i in range(0, len(todo), BATCH):
        batch = todo[i:i + BATCH]
        vectors = embed([c["text"] for c in batch])
        col.add(ids=[c["id"] for c in batch], embeddings=vectors,
                documents=[c["text"] for c in batch], metadatas=[c["metadata"] for c in batch])
        log(f"  [{design}] stored {min(i + BATCH, len(todo))}/{len(todo)} new chunks")
    return {"new": len(todo), "existing": len(existing)}


def source_ids(source: str, design: str = DEFAULT_DESIGN) -> list[str]:
    return collection(design).get(where={"source": source}, include=[])["ids"]


# ---------------------------------------------------------------- main

def main() -> None:
    INDEX_DIR.mkdir(exist_ok=True)
    total_words = 0
    for doc in CORPUS:
        path = download(doc)
        info, units = parse_boe(path)
        words = sum(len(p.split()) for u in units for p in u["paras"])
        total_words += words
        log(f"{info['source']}: {len(units)} units, {words} words")
        for design in DESIGNS:
            chunks = chunk_file(path, design)
            # drop stale chunks of this law (e.g. after a chunking change), then add missing ones
            keep = {c["id"] for c in chunks}
            stale = [i for i in source_ids(info["source"], design) if i not in keep]
            if stale:
                collection(design).delete(ids=stale)
            try:
                counts = embed_and_store(chunks, design)
            except QuotaExhausted:
                log("\nDaily embedding quota reached. Everything embedded so far is saved;"
                    "\nrun `main.py index` again after the quota resets (09:00 Spain).")
                return
            log(f"  {design:9} {len(chunks):4} chunks ({counts['new']} embedded now, "
                f"{counts['existing']} already saved)")
    log(f"\nCorpus: {total_words} words. Index in {CHROMA_DIR.relative_to(ROOT)}.")
    for design in DESIGNS:
        log(f"  {design}: {collection(design).count()} chunks stored")


if __name__ == "__main__":
    main()
