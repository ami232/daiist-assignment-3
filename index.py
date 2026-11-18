"""
Assignment 3: build the index (`main.py index`).

Corpus: Spanish tourist-rental law, from the BOE consolidated-legislation API
(https://www.boe.es/datosabiertos/api/legislacion-consolidada). BOE texts may be
reused with attribution to the BOE as the source.

Pipeline: download_corpus -> chunk_file -> embed_and_store (ChromaDB in index/).
server.py imports chunk_file / embed_and_store for its add_document tool.

    uv run python index.py --stats      # download + chunk only, no embeddings
    uv run python index.py              # also embed chunks that have no vector yet
"""

import hashlib
import re
import sys
import time
import warnings
from datetime import date
from pathlib import Path

import httpx
from bs4 import BeautifulSoup, XMLParsedAsHTMLWarning

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIMS = 768
EMBED_BATCH = 50

BOE_API = "https://www.boe.es/datosabiertos/api/legislacion-consolidada/id/{id}/texto"
BOE_URL = "https://www.boe.es/buscar/act.php?id={id}"

# short name (used as `source` everywhere) -> BOE id
CORPUS = {
    "LAU": "BOE-A-1994-26003",            # Ley de Arrendamientos Urbanos
    "Ley 12/2023": "BOE-A-2023-12203",    # derecho a la vivienda
    "LPH": "BOE-A-1960-10906",            # Ley de Propiedad Horizontal
    "RDL 7/2019": "BOE-A-2019-3108",      # medidas urgentes vivienda y alquiler
    "Ley 15/2018 CV": "BOE-A-2018-8950",  # turismo, ocio y hospitalidad C. Valenciana
}
# Held back on purpose: used to demo add_document (answers an unanswerable question).
HELD_BACK = {"RD 1312/2024": "BOE-A-2024-26931"}  # Registro Único de Arrendamientos

DESIGNS = ("article", "fixed")
DEFAULT_DESIGN = "article"   # design used by search and add_document; chosen by hit rate
ARTICLE_MAX_WORDS = 220
FIXED_WORDS, FIXED_STRIDE = 150, 120


# ---------------------------------------------------------------- download

def download_corpus(include_held_back: bool = False) -> dict[str, Path]:
    """Download each law to corpus/<BOE id>.xml (skips files already there)."""
    CORPUS_DIR.mkdir(exist_ok=True)
    items = dict(CORPUS)
    if include_held_back:
        items.update(HELD_BACK)
    paths = {}
    for name, boe_id in items.items():
        path = CORPUS_DIR / f"{boe_id}.xml"
        if not path.exists():
            r = httpx.get(BOE_API.format(id=boe_id), headers={"Accept": "application/xml"}, timeout=90)
            r.raise_for_status()
            path.write_bytes(r.content)
            print(f"downloaded {name} ({boe_id})", file=sys.stderr)
        paths[name] = path
    return paths


def source_name_for(path: Path) -> str:
    """Short source name for a file: the known name for BOE ids, else the file stem."""
    for name, boe_id in {**CORPUS, **HELD_BACK}.items():
        if boe_id in path.name:
            return name
    return path.stem


# ------------------------------------------------------------------ extract

def _clean(text: str) -> str:
    text = text.replace("\xa0", " ")
    return re.sub(r"[ \t]+", " ", text).strip()


def _current_version(block, today: str):
    """Latest version of a block in force on `today` (YYYYMMDD)."""
    versions = [v for v in block.find_all("version") if (v.get("fecha_vigencia") or "00000000") <= today]
    return versions[-1] if versions else None


def parse_boe_xml(path: Path) -> list[dict]:
    """Return one dict per article/provision: location, section, paragraphs.

    The API returns every historical version of a block; we keep only the one in
    force today, so the index never mixes old and new wording.
    """
    # html.parser keeps this free of extra dependencies (lxml); the BOE XML is simple enough.
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    today = date.today().strftime("%Y%m%d")
    section_stack: dict[str, str] = {}
    articles = []
    for block in soup.find_all("bloque"):
        kind = block.get("tipo")
        version = _current_version(block, today)
        if version is None:
            continue
        # BOE footnotes (class nota_pie*: "Se modifica por...", "Ref. BOE-...") are
        # editorial annotations, not the law's text: drop them.
        paras = [_clean(p.get_text(" ")) for p in version.find_all("p")
                 if not any(c.startswith("nota_pie") for c in p.get("class", []))]
        paras = [p for p in paras if p]
        if kind == "encabezado":
            label = block.get("titulo") or (paras[0] if paras else "")
            rest = " ".join(paras[1:])
            words = label.split()
            level = words[0].upper() if words else "?"
            if words:
                words[0] = words[0].capitalize()   # "TÍTULO II" -> "Título II"
            for deeper in {"TÍTULO": ("CAPÍTULO", "SECCIÓN"), "CAPÍTULO": ("SECCIÓN",)}.get(level, ()):
                section_stack.pop(deeper, None)
            section_stack[level] = f"{' '.join(words)} {rest}".strip()
        elif kind == "precepto" and paras:
            body = " ".join(paras)
            if len(body.split()) < 8 or re.fullmatch(r".{0,80}\(?(derogad[oa]|suprimid[oa])\)?\.?", body, re.I):
                continue
            articles.append({
                "location": _clean(block.get("titulo") or paras[0][:60]),
                "section": " > ".join(section_stack.values()),
                "paragraphs": paras,
            })
    return articles


def parse_plain(path: Path) -> list[dict]:
    """PDF or text file -> pseudo-articles (one per page, or per blank-line block group)."""
    if path.suffix.lower() == ".pdf":
        from pypdf import PdfReader
        pages = [(f"p. {i}", (pg.extract_text() or "")) for i, pg in enumerate(PdfReader(str(path)).pages, 1)]
    else:
        raw = path.read_text(encoding="utf-8", errors="ignore")
        parts, buf = [], []
        for para in re.split(r"\n\s*\n", raw):
            buf.append(para)
            if sum(len(b.split()) for b in buf) >= 400:
                parts.append("\n\n".join(buf)); buf = []
        if buf:
            parts.append("\n\n".join(buf))
        pages = [(f"section {i}", t) for i, t in enumerate(parts, 1)]
    out = []
    for loc, text in pages:
        paras = [_clean(p) for p in re.split(r"\n\s*\n|\n(?=[A-ZÁÉÍÓÚ0-9])", text) if _clean(p)]
        if paras:
            out.append({"location": loc, "section": "", "paragraphs": paras})
    return out


# -------------------------------------------------------------------- chunk

def _split_long(paragraph: str, limit: int) -> list[str]:
    """Split one very long paragraph at sentence ends so no piece exceeds `limit` words."""
    pieces, cur = [], []
    for sentence in re.split(r"(?<=[.;:])\s+", paragraph):
        if cur and len(" ".join(cur + [sentence]).split()) > limit:
            pieces.append(" ".join(cur)); cur = []
        cur.append(sentence)
    if cur:
        pieces.append(" ".join(cur))
    return pieces


def _chunk_id(design: str, source: str, location: str, text: str) -> str:
    return hashlib.sha1(f"{design}|{source}|{location}|{text}".encode()).hexdigest()[:20]


def _make(design, source, source_id, location, locations, section, text, part, url):
    prefix = f"{source} — {location}" + (f" ({section})" if section else "")
    return {
        "id": _chunk_id(design, source, location, text),
        "design": design,
        "text": text,
        "embed_text": f"title: {prefix} | text: {text}",
        "meta": {
            "source": source, "source_id": source_id, "location": location,
            "locations": ";".join(locations), "section": section, "part": part,
            "words": len(text.split()), "url": url,
        },
    }


def chunk_file(path: Path | str, design: str = DEFAULT_DESIGN, source: str | None = None) -> list[dict]:
    """Extract, clean and chunk one file. Every chunk carries source and location.

    design "article": one chunk per article (long ones split at paragraph/sentence
        boundaries, at most ARTICLE_MAX_WORDS words).
    design "fixed":   sliding windows of FIXED_WORDS words, ignoring structure; the
        location is the article where the window starts (all covered ones in `locations`).
    """
    path = Path(path)
    source = source or source_name_for(path)
    source_id = path.stem
    url = BOE_URL.format(id=source_id) if source_id.startswith("BOE-") else path.name
    is_boe = path.suffix.lower() == ".xml"
    articles = parse_boe_xml(path) if is_boe else parse_plain(path)
    chunks = []

    if design == "article":
        for art in articles:
            pieces, cur = [], []
            for para in art["paragraphs"]:
                for piece in _split_long(para, ARTICLE_MAX_WORDS):
                    if cur and len(" ".join(cur + [piece]).split()) > ARTICLE_MAX_WORDS:
                        pieces.append(" ".join(cur)); cur = []
                    cur.append(piece)
            if cur:
                pieces.append(" ".join(cur))
            for i, text in enumerate(pieces, 1):
                chunks.append(_make(design, source, source_id, art["location"], [art["location"]],
                                    art["section"], text, i, url))
    elif design == "fixed":
        words, owners = [], []
        for art in articles:
            for w in " ".join(art["paragraphs"]).split():
                words.append(w); owners.append(art)
        for i, start in enumerate(range(0, max(len(words) - FIXED_WORDS + FIXED_STRIDE, 1), FIXED_STRIDE), 1):
            window = words[start:start + FIXED_WORDS]
            if len(window) < 30:
                continue
            owner = owners[start]
            locs = list(dict.fromkeys(o["location"] for o in owners[start:start + FIXED_WORDS]))
            chunks.append(_make(design, source, source_id, owner["location"], locs,
                                owner["section"], " ".join(window), i, url))
    else:
        raise ValueError(f"unknown design {design!r}")
    return chunks


# ------------------------------------------------------------ embed + store

def get_collection(design: str = DEFAULT_DESIGN):
    import chromadb
    client = chromadb.PersistentClient(path=str(INDEX_DIR))
    return client.get_or_create_collection(f"chunks_{design}", metadata={"hnsw:space": "cosine"})


def embed_texts(texts: list[str], retries: int = 4, query: bool = False) -> list[list[float]]:
    """Embed texts with Gemini (retrying on rate limits). Each text counts against the daily quota.

    Documents (chunks) are already prefixed by chunk_file; pass query=True for search queries.
    A plain list in `contents` would give ONE aggregated embedding, so each text is wrapped
    in its own Content to get one vector per text.
    """
    from google import genai
    from google.genai import types
    from api_key import load_api_key

    if query:
        texts = [f"task: search result | query: {t}" for t in texts]
    contents = [types.Content(parts=[types.Part.from_text(text=t)]) for t in texts]
    client = genai.Client(api_key=load_api_key())
    for attempt in range(retries):
        try:
            res = client.models.embed_content(
                model=EMBED_MODEL, contents=contents,
                config=types.EmbedContentConfig(output_dimensionality=EMBED_DIMS),
            )
            vectors = [e.values for e in res.embeddings]
            if len(vectors) != len(texts):
                raise ValueError(f"asked for {len(texts)} embeddings, got {len(vectors)}")
            return vectors
        except Exception as error:  # noqa: BLE001
            if attempt == retries - 1:
                raise
            wait = 20 * (attempt + 1)
            print(f"embed failed ({type(error).__name__}: {str(error)[:120]}); retry in {wait}s", file=sys.stderr)
            time.sleep(wait)

def embed_and_store(chunks: list[dict], design: str | None = None) -> dict:
    """Embed only chunks without a saved vector; save after every batch.

    Returns counts: {"new": n embedded now, "existing": n already stored}.
    """
    if not chunks:
        return {"new": 0, "existing": 0}
    design = design or chunks[0]["design"]
    col = get_collection(design)
    have = set(col.get(ids=[c["id"] for c in chunks], include=[])["ids"])
    todo = [c for c in chunks if c["id"] not in have]
    for i in range(0, len(todo), EMBED_BATCH):
        batch = todo[i:i + EMBED_BATCH]
        vectors = embed_texts([c["embed_text"] for c in batch])
        col.upsert(ids=[c["id"] for c in batch], embeddings=vectors,
                   documents=[c["text"] for c in batch], metadatas=[c["meta"] for c in batch])
        print(f"  stored {i + len(batch)}/{len(todo)} new chunks ({design})", file=sys.stderr)
        if i + EMBED_BATCH < len(todo):
            time.sleep(35)   # stay under the per-minute limit (~100 texts/min on the free tier)
    # Re-indexing a source replaces it: drop stored chunks of these sources that the
    # current text no longer produces (an edited document, or a fixed location label).
    keep = {c["id"] for c in chunks}
    stale = []
    for source in {c["meta"]["source"] for c in chunks}:
        stale += [i for i in col.get(where={"source": source}, include=[])["ids"] if i not in keep]
    if stale:
        col.delete(ids=stale)
    return {"new": len(todo), "existing": len(chunks) - len(todo), "removed": len(stale)}

# --------------------------------------------------------------------- main

def build_all(designs=DESIGNS, embed: bool = True) -> None:
    """Chunk every corpus file with each design and embed what has no vector yet.

    The free tier allows ~1,000 embeddings a day. If the limit is hit we stop
    cleanly: everything embedded so far is already saved, so run again later.
    """
    paths = download_corpus()
    for design in designs:
        all_chunks = []
        for name, path in paths.items():
            all_chunks += chunk_file(path, design, source=name)
        words = sum(c["meta"]["words"] for c in all_chunks)
        print(f"design={design}: {len(all_chunks)} chunks, {words} words, "
              f"avg {words / max(len(all_chunks), 1):.0f} words/chunk", file=sys.stderr)
        if not embed:
            continue
        try:
            print(f"  {embed_and_store(all_chunks, design)}", file=sys.stderr)
        except Exception as error:  # noqa: BLE001
            print(f"\nStopped while embedding design={design}: {type(error).__name__}: {str(error)[:200]}\n"
                  "Progress is saved. The daily limit resets at 09:00 (Spain); run the same command again.",
                  file=sys.stderr)
            return


if __name__ == "__main__":
    args = sys.argv[1:]
    chosen = DESIGNS
    for a in args:
        if a.startswith("--designs="):
            chosen = tuple(a.split("=", 1)[1].split(","))
    build_all(chosen, embed="--stats" not in args)
