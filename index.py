"""
Assignment 3: build the index (`main.py index`).

Corpus: Spanish residential-tenancy law, consolidated texts from the BOE
(Agencia Estatal Boletín Oficial del Estado). Each law is downloaded into
corpus/ (git-ignored), parsed article by article, cleaned, chunked with
source + location metadata, embedded with Gemini and stored in ChromaDB under
index/chroma. Every vector is written to Chroma as soon as its batch comes back,
and a chunk whose id (a hash of design + text) is already stored is never
embedded again.

Two chunking designs are built so evaluate.py can compare them:
  - "fixed":     300-word sliding windows (50-word overlap) over the whole
                 document, ignoring its structure.
  - "structure": one chunk per article (or disposición); articles longer than
                 MAX_WORDS are split on paragraph boundaries. Each chunk is
                 prefixed with "<law>, <article heading>" before embedding.

server.py's add_document tool imports `chunk_file` and `embed_and_store`.
"""

from __future__ import annotations

import hashlib
import re
import sys
import time
import urllib.request
from dataclasses import dataclass
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"
CHROMA_DIR = INDEX_DIR / "chroma"

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768
BATCH = 50

DESIGNS = ("fixed", "structure")
MAX_WORDS = 300          # structure design: split articles longer than this
FIXED_WORDS, FIXED_OVERLAP = 300, 50

# The base corpus. `source` is the short name used in citations and in eval/questions.csv.
DOCS = [
    {"source": "LAU", "boe_id": "BOE-A-1994-26003",
     "title": "Ley 29/1994, de 24 de noviembre, de Arrendamientos Urbanos"},
    {"source": "LDV", "boe_id": "BOE-A-2023-12203",
     "title": "Ley 12/2023, de 24 de mayo, por el derecho a la vivienda"},
    {"source": "LPH", "boe_id": "BOE-A-1960-10906",
     "title": "Ley 49/1960, de 21 de julio, sobre propiedad horizontal"},
]
BOE_URL = "https://www.boe.es/buscar/act.php?id={}"
SHORT_NAMES = {d["boe_id"]: d["source"] for d in DOCS} | {"BOE-A-2018-7833": "L5/2018"}


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)  # stdout is reserved when imported by server.py


# --------------------------------------------------------------------------- download

def download(doc: dict) -> Path:
    CORPUS_DIR.mkdir(exist_ok=True)
    path = CORPUS_DIR / f"{doc['boe_id']}.html"
    if not path.exists():
        log(f"downloading {doc['boe_id']} ...")
        req = urllib.request.Request(BOE_URL.format(doc["boe_id"]), headers={"User-Agent": "daiist-assignment-3"})
        with urllib.request.urlopen(req, timeout=60) as r:
            path.write_bytes(r.read())
    return path


# --------------------------------------------------------------------------- parse

@dataclass
class Unit:
    """One paragraph of law text with the article it belongs to."""
    location: str      # "Artículo 9", "Disposición adicional primera", "Preámbulo"
    heading: str       # full heading, e.g. "Artículo 9. Plazo mínimo."
    part: str          # enclosing Título / Capítulo, for context
    text: str


ART_RE = re.compile(r"^(Artículo\s+(?:\d+|[a-záéíóúñ]+)(?:\s+(?:bis|ter|quater))?|"
                    r"Disposición\s+(?:adicional|transitoria|derogatoria|final)(?:\s+\w+)?)", re.I)

# Text the BOE page shows that is not law: amendment notes, jurisprudence buttons, block markers.
NOISE_CLASSES = {"nota_pie", "nota_pie_2", "bloque", "linkSubir", "fuera"}


def clean(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text)
    return text.strip()


def short_location(heading: str) -> str:
    m = ART_RE.match(heading)
    if not m:
        return heading.rstrip(".")
    return clean(m.group(1)).rstrip(".")


def parse_boe_html(path: Path) -> tuple[str, str, list[Unit]]:
    """Return (boe_id, title, units) for a BOE consolidated (act.php) or original (doc.php) page."""
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    title_tag = soup.find("title")
    full_title = clean(title_tag.get_text()) if title_tag else path.stem
    m = re.match(r"(BOE-A-\d{4}-\d+)\s+(.*)", full_title)
    boe_id, title = (m.group(1), m.group(2)) if m else (path.stem, full_title)
    body = soup.find(id="textoxslt") or soup.find(id="DOdocText") or soup.body

    # Fix: amendment notes ("Se modifica por el art. 1.9 de la Ley 4/2013...") sit in <blockquote>
    # inside each article and would otherwise be embedded as if they were law text.
    for bq in body.find_all("blockquote"):
        bq.decompose()
    for tag in body.find_all(["form", "script", "style"]):
        tag.decompose()

    units: list[Unit] = []
    location, heading, part = "Preámbulo", "Preámbulo", ""
    titulo = capitulo = ""
    for el in body.find_all(["h3", "h4", "h5", "p"]):
        classes = set(el.get("class") or [])
        if classes & NOISE_CLASSES:
            continue
        text = clean(el.get_text(" "))
        if not text:
            continue
        if el.name == "h5" or "articulo" in classes:
            heading = text
            location = short_location(text)
            part = " · ".join(x for x in (titulo, capitulo) if x)
            continue
        if el.name in ("h3", "h4") or classes & {"titulo_num", "titulo_tit", "capitulo_num", "capitulo_tit",
                                                    "centro_redonda", "centro_negrita"}:
            if "titulo_num" in classes or text.upper().startswith("TÍTULO"):
                titulo, capitulo = text, ""
            elif "titulo_tit" in classes and titulo:
                titulo = f"{titulo.split('.')[0]}. {text}"
            elif "capitulo_num" in classes or text.upper().startswith("CAPÍTULO"):
                capitulo = text
            elif "capitulo_tit" in classes and capitulo:
                capitulo = f"{capitulo.split('.')[0]}. {text}"
            elif text.upper() in ("PREÁMBULO", "PREAMBULO", "EXPOSICIÓN DE MOTIVOS"):
                location = heading = "Preámbulo"
            continue
        if re.match(r"^Texto (añadido|modificado|derogado|suprimido)\b.*(publicado|en vigor)", text):
            continue  # BOE version stamp, not law text
        if location == "Preámbulo" and re.match(r"^(JUAN CARLOS|FELIPE|FRANCISCO FRANCO|A todos los que|Sabed:)", text):
            continue
        units.append(Unit(location, heading, part, text))
    return boe_id, title, units


# --------------------------------------------------------------------------- chunk

def chunk_id(design: str, text: str) -> str:
    return hashlib.sha1(f"{EMBED_MODEL}|{EMBED_DIM}|{design}|{text}".encode()).hexdigest()[:20]


def chunk_units(source: str, title: str, units: list[Unit], design: str, origin: str) -> list[dict]:
    chunks: list[dict] = []

    def add(text: str, locations: list[str], heading: str, part: str, embed_text: str) -> None:
        chunks.append({
            "id": chunk_id(design, embed_text),
            "text": text,
            "embed_text": embed_text,
            "metadata": {
                "source": source, "title": title, "design": design, "origin": origin,
                "location": locations[0], "locations": "|".join(dict.fromkeys(locations)),
                "heading": heading, "part": part, "words": len(text.split()),
                "chunk_index": len(chunks),
            },
        })

    if design == "fixed":
        words, owner = [], []
        for u in units:
            w = u.text.split()
            words += w
            owner += [u] * len(w)
        step = FIXED_WORDS - FIXED_OVERLAP
        for start in range(0, max(len(words) - FIXED_OVERLAP, 1), step):
            span = slice(start, start + FIXED_WORDS)
            text = " ".join(words[span])
            locs = [u.location for u in owner[span]]
            add(text, locs, owner[start].heading, owner[start].part, text)
        return chunks

    # structure: group paragraphs by article, split long articles on paragraph boundaries
    groups: list[list[Unit]] = []
    for u in units:
        if groups and groups[-1][0].location == u.location and groups[-1][0].heading == u.heading:
            groups[-1].append(u)
        else:
            groups.append([u])
    for g in groups:
        parts, cur = [], []
        for u in g:
            if cur and sum(len(x.text.split()) for x in cur) + len(u.text.split()) > MAX_WORDS:
                parts.append(cur)
                cur = []
            cur.append(u)
        parts.append(cur)
        for i, p in enumerate(parts):
            text = "\n".join(u.text for u in p)
            head = g[0].heading + (f" (parte {i + 1}/{len(parts)})" if len(parts) > 1 else "")
            prefix = f"{source} ({title}). {g[0].part + '. ' if g[0].part else ''}{head}"
            add(text, [g[0].location], head, g[0].part, f"{prefix}\n{text}")
    return chunks


def chunk_file(path: str | Path, design: str = "structure", source: str | None = None,
               origin: str = "corpus") -> list[dict]:
    """Parse one BOE HTML file and return its chunks (text + metadata), not yet embedded."""
    path = Path(path)
    if path.suffix.lower() not in (".html", ".htm"):
        raise ValueError(f"Only BOE HTML pages are supported, got {path.name}")
    boe_id, title, units = parse_boe_html(path)
    if not units:
        raise ValueError(f"No law text found in {path.name}")
    source = source or SHORT_NAMES.get(boe_id, boe_id)
    return chunk_units(source, title, units, design, origin)


# --------------------------------------------------------------------------- embed + store

_client = None


def genai_client():
    global _client
    if _client is None:
        from google import genai
        from api_key import load_api_key
        _client = genai.Client(api_key=load_api_key())
    return _client


def embed_texts(texts: list[str], task: str = "RETRIEVAL_DOCUMENT") -> list[list[float]]:
    """Embed with retries on rate limits. task: RETRIEVAL_DOCUMENT or RETRIEVAL_QUERY."""
    from google.genai import types
    cfg = types.EmbedContentConfig(task_type=task, output_dimensionality=EMBED_DIM)
    for attempt in range(6):
        try:
            # one Content per text: a plain list of strings is embedded as ONE multi-part input by gemini-embedding-2
            contents = [types.Content(parts=[types.Part(text=t)]) for t in texts]
            res = genai_client().models.embed_content(model=EMBED_MODEL, contents=contents, config=cfg)
            if len(res.embeddings) != len(texts):
                raise RuntimeError(f"asked for {len(texts)} embeddings, got {len(res.embeddings)}")
            return [e.values for e in res.embeddings]
        except Exception as e:  # noqa: BLE001
            msg = str(e)
            if ("429" in msg or "RESOURCE_EXHAUSTED" in msg or "503" in msg) and attempt < 5:
                if "PerDay" in msg or "per day" in msg.lower():
                    raise RuntimeError("Daily embedding quota exhausted; rerun tomorrow (stored vectors are kept).") from e
                wait = 20 * (attempt + 1)
                log(f"rate limited, waiting {wait}s ...")
                time.sleep(wait)
                continue
            raise
    raise RuntimeError("unreachable")


def get_collection(design: str):
    import chromadb
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return client.get_or_create_collection(f"tenancy_{design}", embedding_function=None,
                                           metadata={"hnsw:space": "cosine"})


def embed_and_store(chunks: list[dict], design: str = "structure") -> dict:
    """Embed the chunks that have no stored vector yet and add them to the design's collection.

    Returns counts: {"new": n_embedded, "existing": n_already_stored}.
    """
    col = get_collection(design)
    existing = set(col.get(ids=[c["id"] for c in chunks], include=[])["ids"]) if chunks else set()
    todo = [c for c in chunks if c["id"] not in existing]
    seen, unique = set(), []   # identical text twice in one batch would break Chroma's add
    for c in todo:
        if c["id"] not in seen:
            seen.add(c["id"])
            unique.append(c)
    for i in range(0, len(unique), BATCH):
        batch = unique[i:i + BATCH]
        vecs = embed_texts([c["embed_text"] for c in batch])
        col.add(ids=[c["id"] for c in batch], embeddings=vecs,
                documents=[c["text"] for c in batch], metadatas=[c["metadata"] for c in batch])
        log(f"  [{design}] stored {min(i + BATCH, len(unique))}/{len(unique)} new chunks")
    return {"new": len(unique), "existing": len(chunks) - len(todo)}


def build_all() -> None:
    total_words = 0
    for doc in DOCS:
        path = download(doc)
        _, _, units = parse_boe_html(path)
        words = sum(len(u.text.split()) for u in units)
        total_words += words
        for design in DESIGNS:
            chunks = chunk_file(path, design, source=doc["source"])
            res = embed_and_store(chunks, design)
            log(f"{doc['source']:4} {design:9} {len(chunks):4} chunks, {words} words, "
                f"{res['new']} embedded, {res['existing']} already stored")
    log(f"corpus: {len(DOCS)} documents, {total_words} words")
    for design in DESIGNS:
        log(f"collection tenancy_{design}: {get_collection(design).count()} chunks")


if __name__ == "__main__":
    build_all()
