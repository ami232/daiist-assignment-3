"""
Assignment 3: build the index (`main.py index`).

Corpus: 5 BOE norms on occupational risk prevention in construction, in their
CONSOLIDATED text (the version in force, from the BOE open-data API). They are
downloaded as XML into corpus_consolidado/ (git-ignored; the download date and
BOE update date of each norm go to index/corpus_manifest.json), split into
sections (articles), chunked with TWO designs, embedded with Gemini and stored
in index/ (ChromaDB):

  design "article": one chunk per article (long articles split at paragraph
                    boundaries, same location for every part);
  design "fixed"  : windows of ~150 words with overlap, location = the article
                    where the window starts.

Each vector is saved as soon as it arrives and only chunks without a saved
vector are embedded, so a run can be interrupted and repeated (free tier:
about 1,000 embeddings a day).

Functions used by server.py: chunk_file(path, design), embed_and_store(chunks,
design), embed_query(text), open_collection(design).
"""

import datetime
import hashlib
import json
import re
import sys
import time
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus_consolidado"
INDEX_DIR = ROOT / "index"
CHROMA_DIR = INDEX_DIR / "chroma"

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768
DESIGNS = ("article", "fixed")

ARTICLE_MAX_WORDS = 350   # split longer articles at paragraph boundaries
FIXED_WORDS = 150         # window size of the fixed design
FIXED_OVERLAP = 30

# BOE id -> short name used as `source` in the metadata.
BOE_DOCS = {
    "BOE-A-1995-24292": "Ley 31/1995",
    "BOE-A-1997-1853": "RD 39/1997",
    "BOE-A-1997-22614": "RD 1627/1997",
    "BOE-A-1997-17824": "RD 1215/1997",
    "BOE-A-2006-18205": "Ley 32/2006",
}
# Consolidated text (version in force). The API answers 400 without the Accept header.
BOE_URL = "https://www.boe.es/datosabiertos/api/legislacion-consolidada/id/{id}"
MANIFEST = INDEX_DIR / "corpus_manifest.json"  # download date + BOE update date per norm


def log(*a):
    print(*a, file=sys.stderr, flush=True)


# --------------------------------------------------------------------- download
def download_corpus() -> list[Path]:
    """Download the consolidated BOE XML files into corpus_consolidado/ (skips files
    already there) and record in index/corpus_manifest.json when each one was
    downloaded and which BOE update it holds."""
    import httpx

    CORPUS_DIR.mkdir(exist_ok=True)
    manifest = json.loads(MANIFEST.read_text(encoding="utf-8")) if MANIFEST.exists() else {}
    paths = []
    for boe_id in BOE_DOCS:
        dest = CORPUS_DIR / f"{boe_id}.xml"
        if not dest.exists():
            log(f"downloading {boe_id}")
            r = httpx.get(BOE_URL.format(id=boe_id), timeout=60, follow_redirects=True,
                          headers={"User-Agent": "daiist-assignment-3 (student project)",
                                   "Accept": "application/xml"})
            r.raise_for_status()
            dest.write_bytes(r.content)
            downloaded = datetime.date.today().isoformat()
        else:  # downloaded earlier: keep the recorded date, else use the file's date
            downloaded = manifest.get(boe_id, {}).get("downloaded") or \
                datetime.date.fromtimestamp(dest.stat().st_mtime).isoformat()
        meta = ET.parse(dest).getroot().find("data/metadatos")
        manifest[boe_id] = {
            "norm": BOE_DOCS[boe_id],
            "url": BOE_URL.format(id=boe_id),
            "downloaded": downloaded,
            "boe_updated": (meta.findtext("fecha_actualizacion") or "").strip() if meta is not None else "",
            "sha256": hashlib.sha256(dest.read_bytes()).hexdigest(),
        }
        paths.append(dest)
    INDEX_DIR.mkdir(exist_ok=True)
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=1) + "\n", encoding="utf-8")
    return paths


# ------------------------------------------------------------------- extraction
def _clean(text: str) -> str:
    text = text.replace("\xa0", " ")
    return re.sub(r"\s+", " ", text).strip()


def _location_from_heading(heading: str) -> str:
    """'Artículo 15. Principios de la acción preventiva.' -> 'Artículo 15'."""
    heading = re.sub(r"^\[precepto\]\s*", "", heading)
    m = re.match(r"^(Art[ií]culo\s+\d+(?:\s*(?:bis|ter|quater))?)", heading, re.I)
    if m:
        return m.group(1).replace("Articulo", "Artículo")
    m = re.match(r"^(Disposici[oó]n\s+\w+\s+(?:\w+)?)\.", heading)
    if m:
        return _clean(m.group(1))
    m = re.match(r"^([^.]{3,60})\.", heading)
    return _clean(m.group(1)) if m else _clean(heading[:60])


NOTE_CLASSES = {"nota_pie", "nota_pie_2"}  # "Se modifica por...": editorial notes, not law
_DEROGATED = re.compile(r"^\((Derogad[oa]|Suprimid[oa]|Sin contenido)", re.I)


def parse_boe(path: Path) -> tuple[str, list[tuple[str, list[str]]]]:
    """Return (source, [(location, [paragraph, ...]), ...]) for a BOE XML file,
    consolidated (API, root <response>) or original (diario_boe, root <documento>)."""
    root = ET.parse(path).getroot()
    if root.tag == "response":
        return parse_boe_consolidated(root, path)
    return parse_boe_original(root, path)


def parse_boe_consolidated(root, path: Path) -> tuple[str, list[tuple[str, list[str]]]]:
    """Consolidated text: <data><texto><bloque tipo titulo><version>...<p>.

    Only the LAST <version> of each block (the one in force) is read, so old
    wording (e.g. the 1995 fines in pesetas) never enters the index. The location
    is the block's `titulo` ("Artículo 32 bis", "Disposición adicional
    decimocuarta", "Anexo IV"); annex blocks are kept whatever their `tipo`.
    Footnotes are left out. A derogated block becomes a short section: its
    heading, "(Derogado)" and the note naming the derogating norm.
    """
    data = root.find("data")
    boe_id = (data.findtext("metadatos/identificador") or path.stem).strip()
    source = BOE_DOCS.get(boe_id) or _clean(data.findtext("metadatos/numero_oficial") or path.stem)
    body = data.find("texto")
    if body is None:
        return source, []
    skip = {"firma_rey", "firma_ministro", "capitulo_num", "capitulo_tit", "subseccion",
            "seccion", "titulo_num", "titulo_tit", "centro_redonda"}
    sections: list[tuple[str, list[str]]] = []
    for block in body.findall("bloque"):
        kind, title = block.get("tipo", ""), _clean(block.get("titulo") or "")
        is_annex = title.upper().startswith("ANEXO")
        if kind not in ("preambulo", "precepto") and not is_annex:
            continue  # chapter headings, signature
        versions = block.findall("version")
        if not versions:
            continue
        ps = list(versions[-1].iter("p"))
        text = [_clean("".join(p.itertext())) for p in ps
                if p.get("class") not in NOTE_CLASSES and p.get("class") not in skip]
        text = [t for t in text if t]
        if kind == "preambulo":
            loc = "Preámbulo"
        elif is_annex:
            loc = "Anexo" + title[5:]  # "ANEXO IV" -> "Anexo IV", "ANEXO" -> "Anexo"
        else:
            loc = title or (_location_from_heading(text[0]) if text else "")
        if not text or not loc:
            continue
        if any(_DEROGATED.match(t) for t in text[1:2]):
            notes = [_clean("".join(p.itertext())) for p in ps if p.get("class") in NOTE_CLASSES]
            text = text[:2] + [n for n in notes if n.lower().startswith("se deroga")]
        sections.append((loc, text))
    return source, sections


def parse_boe_original(root, path: Path) -> tuple[str, list[tuple[str, list[str]]]]:
    """Original text as published (diario_boe/xml.php): a flat list of <p>."""
    boe_id = (root.findtext("metadatos/identificador") or path.stem).strip()
    source = BOE_DOCS.get(boe_id)
    if source is None:
        source = _clean(root.findtext("metadatos/numero_oficial") or path.stem)
    body = root.find("texto")
    sections: list[tuple[str, list[str]]] = [("Preámbulo", [])]
    if body is None:
        return source, []
    skip = {"firma_rey", "firma_ministro", "capitulo_num", "capitulo_tit", "subseccion",
            "seccion", "titulo_num", "titulo_tit", "centro_redonda"}
    group = ""  # "adicional", "transitoria" or "final" inside RD 39/1997-style lists
    for p in body.iter("p"):
        cls = p.get("class", "")
        text = _clean("".join(p.itertext()))
        if not text:
            continue
        if cls == "capitulo":  # e.g. "[encabezado]DISPOSICIONES ADICIONALES"
            m = re.search(r"DISPOSICIONES\s+(ADICIONALES|TRANSITORIAS|FINALES|DEROGATORIAS)", text.upper())
            group = {"ADICIONALES": "adicional", "TRANSITORIAS": "transitoria",
                     "FINALES": "final", "DEROGATORIAS": "derogatoria"}[m.group(1)] if m else ""
            continue
        if cls in ("anexo_num", "anexo"):  # Ley 32/2006 uses class "anexo"
            sections.append(("Anexo " + re.sub(r"(?i)^anexo\s*", "", text).upper(), []))
        elif cls == "articulo":
            loc = _location_from_heading(text)
            if text.startswith("[precepto]") and group:  # "Primera. ..." under a group
                loc = f"Disposición {group} {loc[0].lower() + loc[1:]}"
            sections.append((loc, [text]))
        elif cls in skip:
            continue
        else:
            sections[-1][1].append(text)
    return source, [(loc, paras) for loc, paras in sections if paras]


def parse_generic(path: Path) -> tuple[str, list[tuple[str, list[str]]]]:
    """PDF, HTML, TXT or MD file added later with add_document."""
    source = path.stem
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        from pypdf import PdfReader

        sections = []
        for i, page in enumerate(PdfReader(str(path)).pages, start=1):
            paras = [_clean(x) for x in (page.extract_text() or "").split("\n\n") if _clean(x)]
            if paras:
                sections.append((f"p. {i}", paras))
        return source, sections
    raw = path.read_text(encoding="utf-8", errors="ignore")
    if suffix in (".html", ".htm"):
        from bs4 import BeautifulSoup

        raw = BeautifulSoup(raw, "html.parser").get_text("\n")
    paras = [_clean(x) for x in re.split(r"\n\s*\n", raw) if _clean(x)]
    sections, cur, words, n = [], [], 0, 1
    for para in paras:  # ~300-word sections
        cur.append(para)
        words += len(para.split())
        if words >= 300:
            sections.append((f"Sección {n}", cur))
            cur, words, n = [], 0, n + 1
    if cur:
        sections.append((f"Sección {n}", cur))
    return source, sections


def read_sections(path: Path):
    path = Path(path)
    if path.suffix.lower() == ".xml":
        return parse_boe(path)
    return parse_generic(path)


# --------------------------------------------------------------------- chunking
def _chunk(source: str, location: str, text: str, design: str, part: int) -> dict:
    header = f"{source}, {location}"
    full = f"{header}\n{text}"
    cid = hashlib.sha1(f"{design}|{source}|{location}|{part}|{text}".encode()).hexdigest()[:20]
    return {"id": cid, "text": full, "source": source, "location": location, "design": design}


def _split_paragraphs(paras: list[str], max_words: int) -> list[str]:
    parts, cur, n = [], [], 0
    for para in paras:
        w = len(para.split())
        if cur and n + w > max_words:
            parts.append("\n".join(cur))
            cur, n = [], 0
        cur.append(para)
        n += w
    if cur:
        parts.append("\n".join(cur))
    return parts


def chunk_file(path, design: str = "article") -> list[dict]:
    """Extract, clean and chunk one file. Every chunk has source and location."""
    if design not in DESIGNS:
        raise ValueError(f"design must be one of {DESIGNS}")
    source, sections = read_sections(Path(path))
    chunks: list[dict] = []
    if design == "article":
        for location, paras in sections:
            for i, text in enumerate(_split_paragraphs(paras, ARTICLE_MAX_WORDS)):
                chunks.append(_chunk(source, location, text, design, i))
        return chunks
    # fixed windows over the whole document; location = section of the first word
    words: list[tuple[str, str]] = []
    for location, paras in sections:
        for w in " ".join(paras).split():
            words.append((w, location))
    step = FIXED_WORDS - FIXED_OVERLAP
    for i, start in enumerate(range(0, max(len(words), 1), step)):
        window = words[start:start + FIXED_WORDS]
        if len(window) < 20 and i > 0:
            break
        chunks.append(_chunk(source, window[0][1], " ".join(w for w, _ in window), design, i))
    return chunks


# -------------------------------------------------------------------- embedding
_client = None


def _gemini():
    global _client
    if _client is None:
        from google import genai
        from api_key import resolve_api_key

        key, _ = resolve_api_key()
        if not key:
            raise RuntimeError("No Gemini API key found (see SETUP.md).")
        _client = genai.Client(api_key=key)
    return _client


def embed_text(text: str, retries: int = 6) -> list[float]:
    """Embed ONE text (one request per text keeps the vector tied to its chunk)."""
    from google.genai import types

    delay = 5.0
    for attempt in range(retries):
        try:
            res = _gemini().models.embed_content(
                model=EMBED_MODEL,
                contents=text,
                config=types.EmbedContentConfig(output_dimensionality=EMBED_DIM),
            )
            return list(res.embeddings[0].values)
        except Exception as e:  # rate limit or transient error
            msg = str(e)
            if "PerDay" in msg or "per day" in msg.lower():
                raise RuntimeError("Daily embedding quota reached. Run again tomorrow: saved vectors are kept.") from e
            if attempt == retries - 1:
                raise
            log(f"embed retry in {delay:.0f}s ({msg[:80]})")
            time.sleep(delay)
            delay *= 2
    raise RuntimeError("unreachable")


embed_query = embed_text


def open_collection(design: str):
    import chromadb

    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return client.get_or_create_collection(f"chunks_{design}", metadata={"hnsw:space": "cosine"})


def embed_and_store(chunks: list[dict], design: str | None = None) -> dict:
    """Embed only chunks without a saved vector; save each one immediately.

    Returns {"new": n, "already_indexed": m}. Re-adding a document is harmless:
    its chunks have the same ids, so nothing is embedded or duplicated.
    """
    if not chunks:
        return {"new": 0, "already_indexed": 0}
    design = design or chunks[0]["design"]
    col = open_collection(design)
    have = set(col.get(ids=[c["id"] for c in chunks], include=[])["ids"])
    todo = [c for c in chunks if c["id"] not in have]
    for i, c in enumerate(todo, start=1):
        vec = embed_text(c["text"])
        col.add(ids=[c["id"]], embeddings=[vec], documents=[c["text"]],
                metadatas=[{"source": c["source"], "location": c["location"], "design": design}])
        if i % 25 == 0:
            log(f"  {design}: embedded {i}/{len(todo)}")
    return {"new": len(todo), "already_indexed": len(have)}


def prune_collection(design: str, keep_ids: set[str]) -> int:
    """Delete every chunk whose id is not in keep_ids (e.g. chunks of an older
    version of the corpus). Returns how many were deleted."""
    col = open_collection(design)
    stale = [i for i in col.get(include=[])["ids"] if i not in keep_ids]
    for start in range(0, len(stale), 500):
        col.delete(ids=stale[start:start + 500])
    return len(stale)


# ------------------------------------------------------------------------- main
def main(designs: tuple[str, ...] = DESIGNS) -> None:
    """Index the corpus. Afterwards each collection holds exactly the corpus's
    chunks: vectors of unchanged chunks are reused (same id), stale ones deleted."""
    paths = download_corpus()
    for design in designs:
        all_chunks = [c for p in paths for c in chunk_file(p, design)]
        words = sum(len(c["text"].split()) for c in all_chunks)
        log(f"design {design}: {len(all_chunks)} chunks, ~{words} words")
        res = embed_and_store(all_chunks, design)
        res["deleted_stale"] = prune_collection(design, {c["id"] for c in all_chunks})
        log(f"design {design}: {res}")
    print("Index ready in", INDEX_DIR)


if __name__ == "__main__":
    main()