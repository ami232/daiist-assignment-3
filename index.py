"""
Assignment 3: build the index (`main.py index`).

Corpus: Spanish labour law, consolidated texts from the BOE open-data API
(https://www.boe.es/datosabiertos/). Downloads into corpus/ (git-ignored),
parses each law article by article (current version only, amendment notes
removed), chunks it, embeds with Gemini and stores the vectors in index/
(ChromaDB). Embedding is incremental: only chunks without a saved vector are
sent, and each batch is saved as soon as it comes back.

Two chunking designs are built so evaluate.py can compare them:
  - "article": one chunk per article; long articles split at numbered
    apartados into parts of at most ~MAX_WORDS words (structure-based).
  - "fixed":   fixed windows of FIXED_WORDS words with overlap, ignoring
    structure (baseline).

server.py imports chunk_file() and embed_and_store() for its add_document tool.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"
CHROMA_DIR = INDEX_DIR / "chroma"

EMBED_MODEL = "gemini-embedding-2"
BATCH = 50
MAX_WORDS = 350        # "article" design: split articles longer than this
FIXED_WORDS = 250      # "fixed" design: window size
FIXED_OVERLAP = 30
DESIGNS = ("article", "fixed")
PRODUCTION_DESIGN = "article"

BOE_API = "https://www.boe.es/datosabiertos/api/legislacion-consolidada/id/{id}/texto"
BOE_URL = "https://www.boe.es/buscar/act.php?id={id}"

# The base corpus. Ley 10/2021 (trabajo a distancia) is deliberately NOT here:
# it is the document added later through the add_document tool.
SOURCES = {
    "BOE-A-2015-11430": "Estatuto de los Trabajadores (RDL 2/2015)",
    "BOE-A-1995-24292": "Ley de Prevención de Riesgos Laborales (Ley 31/1995)",
    "BOE-A-2000-15060": "Ley sobre Infracciones y Sanciones en el Orden Social (RDL 5/2000)",
}
KNOWN_TITLES = {
    **SOURCES,
    "BOE-A-2021-11472": "Ley de trabajo a distancia (Ley 10/2021)",
}


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


# --------------------------------------------------------------------------- #
# Download
# --------------------------------------------------------------------------- #

def download(boe_id: str, dest_dir: Path = CORPUS_DIR) -> Path:
    """Fetch a consolidated law as XML from the BOE API (once)."""
    dest_dir.mkdir(parents=True, exist_ok=True)
    path = dest_dir / f"{boe_id}.xml"
    if not path.exists():
        req = urllib.request.Request(BOE_API.format(id=boe_id), headers={"Accept": "application/xml"})
        with urllib.request.urlopen(req, timeout=60) as r:
            path.write_bytes(r.read())
        log(f"downloaded {path.name}")
    return path


# --------------------------------------------------------------------------- #
# Extract and clean
# --------------------------------------------------------------------------- #

@dataclass
class Section:
    """One article (or disposición) of a law, cleaned."""
    source: str          # BOE id, e.g. BOE-A-2015-11430, or file stem
    title: str           # human title of the law/document
    location: str        # "Artículo 38", "Disposición adicional primera", "Página 3"
    heading: str         # "Artículo 38. Vacaciones anuales."
    hierarchy: str       # "TÍTULO I > CAPÍTULO II > Sección 4.ª"
    in_force_since: str  # date of the version used (YYYY-MM-DD) or ""
    paragraphs: list[str] = field(default_factory=list)


SKIP_BLOCKS = {"preambulo", "firma", "nota_inicial"}
WS = re.compile(r"\s+")


def clean(text: str) -> str:
    return WS.sub(" ", text.replace("\xa0", " ")).strip()


def parse_boe_xml(path: Path) -> list[Section]:
    """Parse a BOE consolidated-text XML into current-version articles.

    Each <bloque> holds every historical <version>; the last one is in force.
    Paragraphs with class nota_pie* are amendment notes ("Se modifica por...")
    and are dropped: they are not law and they pollute retrieval.
    """
    root = ET.parse(path).getroot()
    source = path.stem
    title = KNOWN_TITLES.get(source, source)
    levels: dict[str, str] = {}
    order = ["titulo", "capitulo", "seccion", "subseccion"]
    sections = []
    for bloque in root.iter("bloque"):
        tipo = bloque.get("tipo")
        versions = bloque.findall("version")
        if tipo in SKIP_BLOCKS or not versions:
            continue
        version = versions[-1]
        if tipo == "encabezado":
            for p in version:
                cls = (p.get("class") or "")
                text = clean("".join(p.itertext()))
                for i, lvl in enumerate(order):
                    if cls.startswith(lvl):
                        if cls.endswith("_num") or cls == lvl:
                            levels[lvl] = text
                            for deeper in order[i + 1:]:
                                levels.pop(deeper, None)
                        elif cls.endswith("_tit"):
                            levels[lvl] = f"{levels.get(lvl, '')} {text}".strip()
                        break
            continue
        if tipo != "precepto":
            continue
        heading, paragraphs = "", []
        for p in version:
            cls = p.get("class") or ""
            if cls.startswith("nota_pie") or p.tag != "p":
                continue
            text = clean("".join(p.itertext()))
            if not text:
                continue
            if cls == "articulo" and not heading:
                heading = text
            else:
                paragraphs.append(text)
        if not paragraphs:
            continue  # derogated articles keep only a heading
        if re.search(r"\(\s*[Dd]erogad[oa]\s*\)|^\s*\(?Sin contenido\)?\s*$", " ".join(paragraphs)):
            continue
        location = bloque.get("titulo") or heading.split(".")[0]
        d = version.get("fecha_vigencia") or ""
        sections.append(Section(
            source=source, title=title, location=location, heading=heading or location,
            hierarchy=" > ".join(levels[l] for l in order if l in levels),
            in_force_since=f"{d[:4]}-{d[4:6]}-{d[6:8]}" if len(d) == 8 else "",
            paragraphs=paragraphs,
        ))
    return sections


ARTICLE_RE = re.compile(r"^(Art[íi]culo\s+\d+[\w.]*|Disposici[óo]n\s+(adicional|transitoria|final|derogatoria)\s+\w+)", re.I)


def parse_plain(path: Path) -> list[Section]:
    """Fallback for files added by hand (.pdf, .txt, .md, .html).

    Splits on "Artículo N" / "Disposición ..." lines when the text has them,
    else one section per PDF page (or per ~MAX_WORDS block of plain text).
    """
    suffix = path.suffix.lower()
    pages: list[tuple[str, str]] = []
    if suffix == ".pdf":
        from pypdf import PdfReader
        pages = [(f"Página {i}", p.extract_text() or "") for i, p in enumerate(PdfReader(path).pages, 1)]
    elif suffix in {".html", ".htm"}:
        from bs4 import BeautifulSoup
        pages = [("", BeautifulSoup(path.read_text(encoding="utf-8", errors="ignore"), "html.parser").get_text("\n"))]
    else:
        pages = [("", path.read_text(encoding="utf-8", errors="ignore"))]

    title = KNOWN_TITLES.get(path.stem, path.stem)
    lines = [(loc, clean(l)) for loc, text in pages for l in text.splitlines() if clean(l)]
    sections: list[Section] = []
    current: Section | None = None
    for loc, line in lines:
        m = ARTICLE_RE.match(line)
        if m:
            current = Section(path.stem, title, m.group(1), line, "", "", [])
            sections.append(current)
        elif current is not None:
            current.paragraphs.append(line)
    if sections:
        return [s for s in sections if s.paragraphs]
    # No legal structure: group by page / size.
    out: dict[str, Section] = {}
    for loc, line in lines:
        key = loc or "Texto"
        out.setdefault(key, Section(path.stem, title, key, key, "", "", [])).paragraphs.append(line)
    return list(out.values())


def extract(path: Path) -> list[Section]:
    path = Path(path)
    if path.suffix.lower() == ".xml":
        return parse_boe_xml(path)
    return parse_plain(path)


# --------------------------------------------------------------------------- #
# Chunk
# --------------------------------------------------------------------------- #

APARTADO_RE = re.compile(r"^(\d+)\.\s")


def _chunk(design: str, sec: Section, text: str, location: str, seq: int) -> dict:
    digest = hashlib.sha1(f"{sec.source}|{location}|{text}".encode()).hexdigest()[:12]
    return {
        "id": f"{design}:{sec.source}:{seq:04d}:{digest}",
        "text": text,
        "source": sec.source,
        "title": sec.title,
        "location": location,
        "heading": sec.heading,
        "hierarchy": sec.hierarchy,
        "in_force_since": sec.in_force_since,
        "url": BOE_URL.format(id=sec.source) if sec.source.startswith("BOE-") else "",
        "words": len(text.split()),
    }


def chunk_by_article(sections: list[Section]) -> list[dict]:
    """One chunk per article; split long ones at apartado boundaries.

    Every part repeats the article heading so it still says what it is about.
    """
    chunks, seq = [], 0
    for sec in sections:
        groups: list[list[str]] = [[]]
        words = 0
        for p in sec.paragraphs:
            n = len(p.split())
            starts_apartado = bool(APARTADO_RE.match(p))
            if groups[-1] and words + n > MAX_WORDS and (starts_apartado or words > MAX_WORDS):
                groups.append([])
                words = 0
            groups[-1].append(p)
            words += n
        last_num = None
        for g in groups:
            nums = [APARTADO_RE.match(p).group(1) for p in g if APARTADO_RE.match(p)]
            if not APARTADO_RE.match(g[0]) and last_num:
                nums.insert(0, last_num)  # continues the previous apartado
            location = sec.location
            if len(groups) > 1 and nums:
                location += f", apdo. {nums[0]}" if nums[0] == nums[-1] else f", apdos. {nums[0]}-{nums[-1]}"
            elif len(groups) > 1:
                location += f" (parte {groups.index(g) + 1})"
            last_num = nums[-1] if nums else last_num
            text = sec.heading + "\n" + "\n".join(g)
            chunks.append(_chunk("article", sec, text, location, seq))
            seq += 1
    return chunks


def chunk_fixed(sections: list[Section]) -> list[dict]:
    """Fixed word windows over the whole document, ignoring articles.

    The location lists the article(s) each window overlaps, so citations and
    hit-rate still work.
    """
    if not sections:
        return []
    tagged: list[tuple[str, int]] = []  # (word, section index)
    for i, sec in enumerate(sections):
        for w in (sec.heading + " " + " ".join(sec.paragraphs)).split():
            tagged.append((w, i))
    chunks, seq, step = [], 0, FIXED_WORDS - FIXED_OVERLAP
    for start in range(0, len(tagged), step):
        window = tagged[start:start + FIXED_WORDS]
        idx = sorted({i for _, i in window})
        sec = sections[idx[0]]
        location = "; ".join(sections[i].location for i in idx)
        chunks.append(_chunk("fixed", sec, " ".join(w for w, _ in window), location, seq))
        seq += 1
        if start + FIXED_WORDS >= len(tagged):
            break
    return chunks


def chunk_file(path: str | Path, design: str = PRODUCTION_DESIGN) -> list[dict]:
    """Extract, clean and chunk one file. Each chunk carries source and location."""
    sections = extract(Path(path))
    chunks = chunk_by_article(sections) if design == "article" else chunk_fixed(sections)
    sha = hashlib.sha1(Path(path).read_bytes()).hexdigest()
    for c in chunks:
        c["file_sha1"] = sha
    return chunks


# --------------------------------------------------------------------------- #
# Embed and store
# --------------------------------------------------------------------------- #

class QuotaExhausted(RuntimeError):
    pass


_client = None


def genai_client():
    global _client
    if _client is None:
        from google import genai
        from api_key import load_api_key
        _client = genai.Client(api_key=load_api_key())
    return _client


def doc_prompt(chunk: dict) -> str:
    # gemini-embedding-2 takes the task as a text prefix (task_type is ignored).
    return f"title: {chunk['title']} — {chunk['heading']} | text: {chunk['text']}"


def query_prompt(query: str) -> str:
    return f"task: search result | query: {query}"


def embed_texts(texts: list[str], retries: int = 6) -> list[list[float]]:
    """Embed a batch, one Content per text (a plain list would be merged into one)."""
    from google.genai import errors, types
    contents = [types.Content(parts=[types.Part(text=t)]) for t in texts]
    for attempt in range(retries):
        try:
            r = genai_client().models.embed_content(model=EMBED_MODEL, contents=contents)
            return [e.values for e in r.embeddings]
        except errors.APIError as e:
            msg = str(e)
            if e.code == 429 and ("PerDay" in msg or "per day" in msg.lower()):
                raise QuotaExhausted(msg[:300]) from e
            if e.code in (429, 500, 503) and attempt < retries - 1:
                wait = 2 ** attempt * 5
                m = re.search(r"retry in ([\d.]+)s", msg)
                if m:
                    wait = float(m.group(1)) + 1
                log(f"  embed: {e.code}, retrying in {wait:.0f}s")
                time.sleep(wait)
                continue
            raise
    raise RuntimeError("unreachable")


def get_collection(design: str = PRODUCTION_DESIGN):
    import chromadb
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return client.get_or_create_collection(f"labour_{design}", metadata={"hnsw:space": "cosine"})


def _meta(c: dict) -> dict:
    return {k: c[k] for k in ("source", "title", "location", "heading", "hierarchy",
                              "in_force_since", "url", "words", "file_sha1") if k in c}


def embed_and_store(chunks: list[dict], collection=None) -> int:
    """Embed the chunks that have no saved vector yet and store them.

    Saves after every batch, so a crash or the daily limit loses nothing.
    Returns how many chunks were embedded now.
    """
    if not chunks:
        return 0
    if collection is None:
        collection = get_collection(chunks[0]["id"].split(":")[0])
    existing = set(collection.get(ids=[c["id"] for c in chunks], include=[])["ids"])
    todo = [c for c in chunks if c["id"] not in existing]
    done = 0
    for i in range(0, len(todo), BATCH):
        batch = todo[i:i + BATCH]
        vectors = embed_texts([doc_prompt(c) for c in batch])
        collection.add(ids=[c["id"] for c in batch], embeddings=vectors,
                       documents=[c["text"] for c in batch], metadatas=[_meta(c) for c in batch])
        done += len(batch)
        log(f"  {collection.name}: stored {len(existing) + done}/{len(chunks)}")
    return done


def save_chunks(design: str, chunks: list[dict]) -> None:
    """Keep a readable copy of every chunk next to the vectors (for inspection)."""
    path = INDEX_DIR / f"chunks_{design}.jsonl"
    with path.open("w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")


def main() -> None:
    INDEX_DIR.mkdir(exist_ok=True)
    paths = [download(boe_id) for boe_id in SOURCES]
    stats = {}
    for design in DESIGNS:
        chunks = [c for p in paths for c in chunk_file(p, design)]
        save_chunks(design, chunks)
        words = sum(c["words"] for c in chunks)
        log(f"{design}: {len(chunks)} chunks, {words} words "
            f"(avg {words / len(chunks):.0f}, max {max(c['words'] for c in chunks)})")
        collection = get_collection(design)
        # Drop vectors of chunks that no longer exist (e.g. after a re-chunk),
        # but keep documents added later through add_document.
        base = set(SOURCES)
        stale = [i for i, m in zip(*(lambda r: (r["ids"], r["metadatas"]))(collection.get(include=["metadatas"])))
                 if m["source"] in base and i not in {c["id"] for c in chunks}]
        if stale:
            collection.delete(ids=stale)
            log(f"  removed {len(stale)} stale chunks")
        try:
            embed_and_store(chunks, collection)
        except QuotaExhausted as e:
            log(f"Daily embedding quota reached; progress saved. Run again tomorrow.\n  {e}")
            stats[design] = {"chunks": len(chunks), "stored": collection.count()}
            break
        stats[design] = {"chunks": len(chunks), "stored": collection.count()}
    per_doc = {}
    for p in paths:
        secs = extract(p)
        per_doc[p.stem] = {"title": KNOWN_TITLES[p.stem], "articles": len(secs),
                           "words": sum(len((s.heading + " " + " ".join(s.paragraphs)).split()) for s in secs)}
    (INDEX_DIR / "stats.json").write_text(json.dumps({"documents": per_doc, "designs": stats},
                                                     ensure_ascii=False, indent=2), encoding="utf-8")
    print(json.dumps({"documents": per_doc, "designs": stats}, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
