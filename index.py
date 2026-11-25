"""
Assignment 3: build the index (`main.py index`). May be index.ipynb instead.

Download the corpus (into corpus/, git-ignored), extract, clean and chunk it
with source and location metadata, embed with Gemini, and store everything in
index/. Save each vector as you get it and embed only chunks without one.

Write the per-file steps as functions (e.g. `chunk_file(path)`,
`embed_and_store(chunks)`): server.py's add-document tool imports them.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import time
import warnings
from dataclasses import dataclass, field
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"
CHROMA_DIR = INDEX_DIR / "chroma"
QUERY_CACHE = INDEX_DIR / "query_cache.jsonl"
MANIFEST = INDEX_DIR / "manifest.json"

warnings.filterwarnings("ignore", message=".*looks like you're using an HTML parser.*")

CORPUS_DATE = "20261118"

DOCUMENTS = [
    {
        "source": "UNCLOS",
        "title": "Convención de las Naciones Unidas sobre el Derecho del Mar (1982)",
        "boe_id": "BOE-A-1997-3296",
        "kind": "diario",
        "keep_parts": [
            "Instrumento de ratificación",
            "Preámbulo",
            "Parte I", "Parte II", "Parte III", "Parte IV",
            "Parte V", "Parte VI", "Parte VII",
            "Parte XVI",
        ],
        "keep_articles": ["Artículo 149"],
    },
    {
        "source": "UNESCO 2001",
        "title": "Convención sobre la Protección del Patrimonio Cultural Subacuático (UNESCO, 2001)",
        "boe_id": "BOE-A-2009-3787",
        "kind": "diario",
        "keep_parts": None,
    },
    {
        "source": "Ley 16/1985",
        "title": "Ley 16/1985, de 25 de junio, del Patrimonio Histórico Español",
        "boe_id": "BOE-A-1985-12534",
        "kind": "consolidated",
        "keep_parts": None,
    },
    {
        "source": "Ley 14/2014",
        "title": "Ley 14/2014, de 24 de julio, de Navegación Marítima",
        "boe_id": "BOE-A-2014-7877",
        "kind": "consolidated",
        "keep_parts": [
            "Título preliminar",
            "Título I",
            "Título VI",
        ],
    },
]

DESIGNS = {
    "article": {"kind": "article", "max_words": 300},
    "fixed": {"kind": "fixed", "words": 150, "overlap": 30},
}
DEFAULT_DESIGN = "article"

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768
EMBED_BATCH = 50
DOC_TEMPLATE = "title: {title} | text: {text}"
QUERY_TEMPLATE = "task: question answering | query: {text}"


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


def clean(text: str) -> str:
    text = text.replace("\xa0", " ").replace("\u200b", "")
    return re.sub(r"\s+", " ", text).strip()


def n_words(text: str) -> int:
    return len(text.split())


def sha(text: str, n: int = 16) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()[:n]


_UNITS = {"uno": 1, "un": 1, "dos": 2, "tres": 3, "cuatro": 4, "cinco": 5,
          "seis": 6, "siete": 7, "ocho": 8, "nueve": 9}
_SPECIAL = {"diez": 10, "once": 11, "doce": 12, "trece": 13, "catorce": 14,
            "quince": 15, "dieciséis": 16, "diecisiete": 17, "dieciocho": 18,
            "diecinueve": 19, "veinte": 20, "veintiuno": 21, "veintidós": 22,
            "veintitrés": 23, "veinticuatro": 24, "veinticinco": 25,
            "veintiséis": 26, "veintisiete": 27, "veintiocho": 28,
            "veintinueve": 29, "treinta": 30, "cuarenta": 40, "cincuenta": 50,
            "sesenta": 60, "setenta": 70, "ochenta": 80, "noventa": 90}
_ORDINALS = {"primero": 1, "segundo": 2, "tercero": 3, "cuarto": 4,
             "quinto": 5, "sexto": 6, "séptimo": 7, "octavo": 8, "noveno": 9,
             "décimo": 10}


def spanish_number(words: str) -> int | None:
    w = words.strip().lower()
    if w.isdigit():
        return int(w)
    if w in _ORDINALS:
        return _ORDINALS[w]
    if w in _SPECIAL:
        return _SPECIAL[w]
    m = re.fullmatch(r"(\w+) y (\w+)", w)
    if m and m.group(1) in _SPECIAL and m.group(2) in _UNITS:
        return _SPECIAL[m.group(1)] + _UNITS[m.group(2)]
    return None


def article_label(raw: str) -> str:
    m = re.match(r"Art[íi]culo\s+(.+?)(\s+bis|\s+ter)?\.?$", clean(raw), re.I)
    if not m:
        return clean(raw).rstrip(".")
    num = spanish_number(m.group(1))
    suffix = (m.group(2) or "").strip()
    if num is None:
        return clean(raw).rstrip(".")
    return f"Artículo {num}" + (f" {suffix}" if suffix else "")


@dataclass
class Unit:
    source: str
    title: str
    part: str
    part_title: str
    chapter: str
    section: str
    article: str
    url: str
    paragraphs: list[str] = field(default_factory=list)

    @property
    def text(self) -> str:
        return "\n".join(self.paragraphs)

    @property
    def location(self) -> str:
        part = f"{self.part}. {self.part_title}" if self.part_title else self.part
        bits = [part, self.chapter, self.section, self.article]
        out = []
        for b in bits:
            if b and (not out or b != out[-1]):
                out.append(b)
        return " › ".join(out)


def boe_url(doc: dict) -> str:
    if doc["kind"] == "consolidated":
        return f"https://www.boe.es/datosabiertos/api/legislacion-consolidada/id/{doc['boe_id']}/texto"
    return f"https://www.boe.es/diario_boe/xml.php?id={doc['boe_id']}"


def reader_url(doc: dict, anchor: str = "") -> str:
    if doc["kind"] == "consolidated":
        return f"https://www.boe.es/buscar/act.php?id={doc['boe_id']}" + (f"#{anchor}" if anchor else "")
    return f"https://www.boe.es/diario_boe/txt.php?id={doc['boe_id']}"


def download(doc: dict) -> Path:
    import httpx

    CORPUS_DIR.mkdir(exist_ok=True)
    path = CORPUS_DIR / f"{doc['boe_id']}.xml"
    if path.exists() and path.stat().st_size > 1000:
        return path
    log(f"Downloading {doc['source']} ({doc['boe_id']}) from the BOE ...")
    r = httpx.get(boe_url(doc), headers={"Accept": "application/xml"},
                  timeout=120, follow_redirects=True)
    r.raise_for_status()
    path.write_bytes(r.content)
    return path


_HEADING = re.compile(r"^(PARTE|T[ÍI]TULO|ANEXO|CAP[ÍI]TULO)\s*([IVXLC]+|PRELIMINAR)?\b", re.I)


def _heading_label(text: str) -> str:
    m = _HEADING.match(text)
    if not m:
        return text
    word = {"parte": "Parte", "titulo": "Título", "título": "Título",
            "anexo": "Anexo", "capitulo": "Capítulo", "capítulo": "Capítulo"}[m.group(1).lower()]
    num = (m.group(2) or "").upper()
    return f"{word} {'preliminar' if num == 'PRELIMINAR' else num}".strip()


def _p_class(p) -> str:
    cls = p.get("class") or [""]
    return cls[0] if isinstance(cls, list) else cls


def parse_consolidated(xml: str, doc: dict) -> list[Unit]:
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(xml, "html.parser")
    units: list[Unit] = []
    part = part_title = chapter = section = ""

    for bloque in soup.find_all("bloque"):
        tipo = bloque.get("tipo", "")
        if tipo in ("nota_inicial", "firma"):
            continue
        versions = [v for v in bloque.find_all("version")
                    if (v.get("fecha_vigencia") or v.get("fecha_publicacion") or "0") <= CORPUS_DATE]
        if not versions:
            continue
        version = max(versions, key=lambda v: v.get("fecha_vigencia") or v.get("fecha_publicacion") or "0")
        for note in version.find_all("blockquote"):
            note.decompose()
        ps = [(_p_class(p), clean(p.get_text(" "))) for p in version.find_all("p")]
        ps = [(c, t) for c, t in ps if t and c not in ("centro_redonda", "firma_rey", "firma_ministro")
              and not c.startswith("nota_pie")]

        if tipo == "encabezado":
            label = bloque.get("titulo", "")
            sub = " ".join(t for c, t in ps if c.endswith("_tit"))
            if re.match(r"T[ÍI]TULO", label, re.I):
                part, part_title, chapter, section = _heading_label(label), sub, "", ""
            elif re.match(r"CAP[ÍI]TULO", label, re.I):
                chapter, section = f"{_heading_label(label)}. {sub}".rstrip(". "), ""
            elif label.lower().startswith("sección"):
                section = clean(" ".join(t for _, t in ps)) or label
            continue

        if tipo == "preambulo":
            units.append(Unit(doc["source"], doc["title"], "Preámbulo", "", "", "", "Preámbulo",
                              reader_url(doc, "preambulo"), [t for _, t in ps]))
            continue

        label = bloque.get("titulo", "")
        if label.startswith("Disposición"):
            part, part_title, chapter, section = "Disposiciones", "", "", ""
        units.append(Unit(doc["source"], doc["title"], part, part_title, chapter, section,
                          article_label(label), reader_url(doc, bloque.get("id", "")),
                          [t for _, t in ps]))
    return [u for u in units if u.paragraphs]


def parse_diario(xml: str, doc: dict) -> list[Unit]:
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(xml, "html.parser")
    body = max(soup.find_all("texto"), key=lambda t: len(t.find_all("p")), default=soup)
    units: list[Unit] = []
    url = reader_url(doc)
    state = {"part": "Instrumento de ratificación", "part_title": "", "chapter": "", "section": ""}
    current: Unit | None = None

    def start(article: str) -> Unit:
        nonlocal current
        current = Unit(doc["source"], doc["title"], state["part"], state["part_title"],
                       state["chapter"], state["section"], article, url)
        units.append(current)
        return current

    def set_part(part: str) -> None:
        nonlocal current
        state.update(part=part, part_title="", chapter="", section="")
        current = None

    start("Instrumento de ratificación")
    in_table = False
    for p in body.find_all("p"):
        cls, text = _p_class(p), clean(p.get_text(" "))
        if not text or cls in ("firma_rey", "firma_ministro"):
            continue
        if "tabla" in cls:
            if not in_table:
                in_table = True
                set_part("Estados Parte y entrada en vigor")
                start("Estados Parte y entrada en vigor")
            continue
        if cls in ("titulo_num", "anexo_num"):
            if _HEADING.match(text):
                set_part(_heading_label(text))
            else:
                set_part("Preámbulo")
                start("Preámbulo")
            continue
        if cls == "anexo":
            set_part("Preámbulo")
            start("Preámbulo")
            continue
        if cls in ("titulo_tit", "anexo_tit", "capitulo"):
            state["part_title"] = text.capitalize() if text.isupper() else text
            continue
        if cls == "capitulo_num":
            state.update(chapter=text, section="")
            current = None
            continue
        if cls == "seccion":
            state["section"] = text
            current = None
            continue
        if cls == "subseccion":
            state["section"] = state["section"].split(" › ")[0] + " › " + text
            current = None
            continue
        if cls == "articulo":
            if state["part"] == "Preámbulo":
                set_part("Articulado")
            start(article_label(text.split(".")[0])).paragraphs.append(text)
            continue
        m = re.match(r"^Norma (\d+)\.", text)
        if m and state["part"].startswith("Anexo"):
            start(f"Norma {m.group(1)}").paragraphs.append(text)
            continue
        (current or start(state["part"])).paragraphs.append(text)
    return [u for u in units if u.paragraphs]


def keep(units: list[Unit], doc: dict) -> list[Unit]:
    parts, arts = doc.get("keep_parts"), set(doc.get("keep_articles") or [])
    if parts is None:
        return units
    return [u for u in units if u.part in parts or u.article in arts]


def load_document(doc: dict) -> list[Unit]:
    xml = download(doc).read_text(encoding="utf-8")
    parser = parse_consolidated if doc["kind"] == "consolidated" else parse_diario
    return keep(parser(xml, doc), doc)


def parse_file(path: str | Path, source: str | None = None, title: str | None = None) -> list[Unit]:
    path = Path(path).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"No file at {path}")
    source = source or path.stem
    title = title or path.stem.replace("_", " ").replace("-", " ")
    suffix = path.suffix.lower()
    url = path.as_uri()

    if suffix == ".xml":
        xml = path.read_text(encoding="utf-8")
        m = re.search(r"<titulo>([^<]+)</titulo>", xml)
        boe_id = re.search(r"BOE-[A-Z]-\d{4}-\d+", path.name)
        doc = {"source": source, "title": clean(m.group(1)) if m and not title else title,
               "boe_id": boe_id.group(0) if boe_id else path.stem,
               "kind": "consolidated" if "<bloque" in xml else "diario"}
        return (parse_consolidated if doc["kind"] == "consolidated" else parse_diario)(xml, doc)

    if suffix == ".pdf":
        from pypdf import PdfReader
        units = []
        for i, page in enumerate(PdfReader(str(path)).pages, start=1):
            raw = page.extract_text() or ""
            raw = re.sub(r"-\n(\w)", r"\1", raw)
            paras = [clean(p) for p in re.split(r"\n\s*\n", raw) if clean(p)]
            if paras:
                units.append(Unit(source, title, "", "", "", "", f"p. {i}", f"{url}#page={i}", paras))
        return units

    if suffix in (".html", ".htm"):
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(path.read_text(encoding="utf-8", errors="replace"), "html.parser")
        for tag in soup(["script", "style", "nav", "header", "footer"]):
            tag.decompose()
        units, current = [], None
        for el in soup.find_all(["h1", "h2", "h3", "h4", "p", "li"]):
            text = clean(el.get_text(" "))
            if not text:
                continue
            if el.name in ("h1", "h2", "h3", "h4"):
                current = Unit(source, title, "", "", "", "", text[:120], url, [text])
                units.append(current)
            else:
                if current is None:
                    current = Unit(source, title, "", "", "", "", "Inicio", url)
                    units.append(current)
                current.paragraphs.append(text)
        return [u for u in units if u.paragraphs]

    if suffix in (".txt", ".md", ".markdown"):
        units, current = [], None
        for block in re.split(r"\n\s*\n", path.read_text(encoding="utf-8", errors="replace")):
            text = clean(block)
            if not text:
                continue
            heading = re.match(r"^#{1,4}\s+(.*)", block.strip())
            if heading:
                current = Unit(source, title, "", "", "", "", clean(heading.group(1))[:120], url, [])
                units.append(current)
                continue
            if current is None:
                current = Unit(source, title, "", "", "", "", "Texto", url)
                units.append(current)
            current.paragraphs.append(text)
        return [u for u in units if u.paragraphs]

    raise ValueError(f"Unsupported file type {suffix!r}: use .xml, .pdf, .html, .md or .txt")


@dataclass
class Chunk:
    id: str
    design: str
    text: str
    source: str
    title: str
    location: str
    article: str
    articles: str
    part: str
    url: str
    doc_hash: str
    position: int

    def metadata(self) -> dict:
        return {"source": self.source, "title": self.title, "location": self.location,
                "article": self.article, "articles": self.articles, "part": self.part,
                "url": self.url, "doc_hash": self.doc_hash, "position": self.position,
                "words": n_words(self.text), "design": self.design}


def document_hash(units: list[Unit]) -> str:
    return sha("\n".join(u.location + "\n" + u.text for u in units), 24)


def _split_paragraphs(paragraphs: list[str], max_words: int) -> list[list[str]]:
    pieces, cur, cur_n = [], [], 0
    expanded = []
    for p in paragraphs:
        if n_words(p) <= max_words:
            expanded.append(p)
            continue
        sentences = re.split(r"(?<=[.;:])\s+", p)
        for s in sentences:
            words = s.split()
            for i in range(0, len(words), max_words):
                expanded.append(" ".join(words[i:i + max_words]))
    for p in expanded:
        n = n_words(p)
        if cur and cur_n + n > max_words:
            pieces.append(cur)
            cur, cur_n = [], 0
        cur.append(p)
        cur_n += n
    if cur:
        pieces.append(cur)
    return pieces


def chunk_units(units: list[Unit], design: str, doc_hash: str | None = None) -> list[Chunk]:
    cfg = DESIGNS[design]
    doc_hash = doc_hash or document_hash(units)
    chunks: list[Chunk] = []

    def make(text: str, first: Unit, covered: list[Unit], location: str) -> Chunk:
        pos = len(chunks)
        cid = sha(f"{design}|{first.source}|{location}|{text}", 20)
        arts = list(dict.fromkeys(u.article for u in covered))
        return Chunk(cid, design, text, first.source, first.title, location, first.article,
                     "; ".join(arts), first.part, first.url, doc_hash, pos)

    if cfg["kind"] == "article":
        for u in units:
            header = f"[{u.title} › {u.location}]"
            pieces = _split_paragraphs(u.paragraphs, cfg["max_words"])
            for i, piece in enumerate(pieces, start=1):
                loc = u.location + (f" (parte {i}/{len(pieces)})" if len(pieces) > 1 else "")
                head = header if len(pieces) == 1 else f"{header[:-1]} (parte {i}/{len(pieces)})]"
                chunks.append(make(head + "\n" + "\n".join(piece), u, [u], loc))
        return chunks

    if cfg["kind"] == "fixed":
        size, step = cfg["words"], cfg["words"] - cfg["overlap"]
        stream = [(w, i) for i, u in enumerate(units) for w in u.text.split()]
        for start in range(0, len(stream), step):
            window = stream[start:start + size]
            if not window or (start > 0 and len(window) <= cfg["overlap"]):
                break
            covered = [units[i] for i in dict.fromkeys(i for _, i in window)]
            loc = covered[0].location if len(covered) == 1 else f"{covered[0].location} … {covered[-1].location}"
            chunks.append(make(" ".join(w for w, _ in window), covered[0], covered, loc))
        return chunks

    raise ValueError(f"Unknown design kind {cfg['kind']!r}")


def chunk_file(path: str | Path, design: str = DEFAULT_DESIGN, source: str | None = None,
               title: str | None = None) -> list[Chunk]:
    units = parse_file(path, source, title)
    return chunk_units(units, design)


class QuotaExhausted(RuntimeError):
    pass


_genai_client = None


def genai_client():
    global _genai_client
    if _genai_client is None:
        from google import genai
        from api_key import load_api_key
        _genai_client = genai.Client(api_key=load_api_key())
    return _genai_client


def _embed(texts: list[str]) -> list[list[float]]:
    import numpy as np
    from google.genai import errors, types

    contents = [types.Content(parts=[types.Part(text=t)]) for t in texts]
    config = types.EmbedContentConfig(output_dimensionality=EMBED_DIM)
    for attempt in range(6):
        try:
            resp = genai_client().models.embed_content(model=EMBED_MODEL, contents=contents, config=config)
            vectors = [e.values for e in resp.embeddings]
            if len(vectors) != len(texts):
                raise RuntimeError(f"Asked for {len(texts)} vectors, got {len(vectors)}.")
            return [(np.asarray(v) / (np.linalg.norm(v) or 1.0)).tolist() for v in vectors]
        except errors.ClientError as e:
            if e.code != 429:
                raise
            msg = str(e)
            if "PerDay" in msg or "per day" in msg.lower():
                raise QuotaExhausted("Daily embedding quota reached.") from e
            m = re.search(r"retry(?:Delay)?['\"]?\s*[:=]?\s*['\"]?(\d+(?:\.\d+)?)s", msg, re.I)
            wait = float(m.group(1)) + 1 if m else 10 * (attempt + 1)
            log(f"  Rate-limited (per minute); waiting {wait:.0f}s ...")
            time.sleep(wait)
        except errors.ServerError:
            wait = 5 * (attempt + 1)
            log(f"  Gemini server error; retrying in {wait}s ...")
            time.sleep(wait)
    raise QuotaExhausted("Gave up after repeated rate limits.")


def embed_documents(chunks: list[Chunk]) -> list[list[float]]:
    return _embed([DOC_TEMPLATE.format(title=c.title, text=c.text) for c in chunks])


_query_cache: dict[str, list[float]] | None = None


def embed_query(query: str) -> list[float]:
    global _query_cache
    key = sha(f"{EMBED_MODEL}|{EMBED_DIM}|{QUERY_TEMPLATE}|{query}", 24)
    if _query_cache is None:
        _query_cache = {}
        if QUERY_CACHE.exists():
            for line in QUERY_CACHE.read_text(encoding="utf-8").splitlines():
                if line.strip():
                    row = json.loads(line)
                    _query_cache[row["key"]] = row["vector"]
    if key not in _query_cache:
        vec = _embed([QUERY_TEMPLATE.format(text=query)])[0]
        _query_cache[key] = vec
        INDEX_DIR.mkdir(exist_ok=True)
        with QUERY_CACHE.open("a", encoding="utf-8") as f:
            f.write(json.dumps({"key": key, "query": query,
                                "vector": [round(x, 6) for x in vec]}, ensure_ascii=False) + "\n")
    return _query_cache[key]


_chroma = None


def chroma():
    global _chroma
    if _chroma is None:
        import chromadb
        CHROMA_DIR.mkdir(parents=True, exist_ok=True)
        _chroma = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return _chroma


def collection_name(design: str) -> str:
    return f"corpus_{design}"


def open_collection(design: str = DEFAULT_DESIGN, create: bool = False):
    if create:
        return chroma().get_or_create_collection(
            collection_name(design), embedding_function=None,
            configuration={"hnsw": {"space": "cosine"}},
            metadata={"model": EMBED_MODEL, "dim": EMBED_DIM, "design": json.dumps(DESIGNS[design])})
    return chroma().get_collection(collection_name(design), embedding_function=None)


def embed_and_store(chunks: list[Chunk], collection) -> tuple[int, int]:
    if not chunks:
        return 0, 0
    have = set()
    ids = [c.id for c in chunks]
    for i in range(0, len(ids), 500):
        have.update(collection.get(ids=ids[i:i + 500], include=[])["ids"])
    todo = [c for c in chunks if c.id not in have]
    done = 0
    for i in range(0, len(todo), EMBED_BATCH):
        batch = todo[i:i + EMBED_BATCH]
        vectors = embed_documents(batch)
        collection.add(ids=[c.id for c in batch], embeddings=vectors,
                       documents=[c.text for c in batch], metadatas=[c.metadata() for c in batch])
        done += len(batch)
        log(f"  {collection.name}: embedded {done}/{len(todo)} new chunks")
    return done, len(have)


def remove_stale(collection, sources: list[str], keep_ids: set[str]) -> int:
    if not sources:
        return 0
    stale = [i for i in collection.get(where={"source": {"$in": sources}}, include=[])["ids"]
             if i not in keep_ids]
    for i in range(0, len(stale), 500):
        collection.delete(ids=stale[i:i + 500])
    return len(stale)


def search(query: str, k: int = 5, design: str = DEFAULT_DESIGN, where: dict | None = None) -> list[dict]:
    col = open_collection(design)
    res = col.query(query_embeddings=[embed_query(query)], n_results=k, where=where,
                    include=["documents", "metadatas", "distances"])
    out = []
    for rank, (doc, meta, dist) in enumerate(zip(res["documents"][0], res["metadatas"][0],
                                                 res["distances"][0]), start=1):
        out.append({"rank": rank, "score": round(1 - dist, 4), "text": doc, **meta})
    return out


def index_file(path: str | Path, source: str | None = None, title: str | None = None,
               designs: list[str] | None = None) -> dict:
    units = parse_file(path, source, title)
    if not units:
        raise ValueError(f"No text could be extracted from {path}")
    source, doc_hash = units[0].source, document_hash(units)
    report = {"source": source, "title": units[0].title, "units": len(units),
              "words": sum(n_words(u.text) for u in units), "designs": {}}
    for design in designs or list(DESIGNS):
        col = open_collection(design, create=True)
        if col.get(where={"doc_hash": doc_hash}, limit=1, include=[])["ids"]:
            report["designs"][design] = "already indexed, nothing to do"
            continue
        chunks = chunk_units(units, design, doc_hash)
        replaced = remove_stale(col, [source], {c.id for c in chunks})
        new, _ = embed_and_store(chunks, col)
        report["designs"][design] = f"{new} chunks embedded" + (f", {replaced} old chunks replaced" if replaced else "")
    return report


def build_corpus_units() -> tuple[dict[str, list[Unit]], list[str]]:
    units, failed = {}, []
    for doc in DOCUMENTS:
        try:
            units[doc["source"]] = load_document(doc)
        except Exception as e:
            log(f"WARNING: could not load {doc['source']}: {e}")
            failed.append(doc["source"])
    return units, failed


def print_stats(units: dict[str, list[Unit]]) -> None:
    print(f"\n{'Document':<14} {'units':>6} {'words':>8}")
    for source, us in units.items():
        print(f"{source:<14} {len(us):>6} {sum(n_words(u.text) for u in us):>8,}")
    print(f"{'Total':<14} {sum(len(u) for u in units.values()):>6} "
          f"{sum(n_words(u.text) for us in units.values() for u in us):>8,}")
    for design in DESIGNS:
        chunks = [c for us in units.values() for c in chunk_units(us, design)]
        avg = sum(n_words(c.text) for c in chunks) / max(len(chunks), 1)
        print(f"Design {design!r}: {len(chunks)} chunks, {avg:.0f} words on average")


def main() -> int:
    units, failed = build_corpus_units()
    print_stats(units)
    if "--stats" in sys.argv:
        return 0

    manifest = {"built": date.today().isoformat(), "corpus_date": CORPUS_DATE,
                "model": EMBED_MODEL, "dim": EMBED_DIM, "designs": DESIGNS,
                "documents": [{k: d[k] for k in ("source", "title", "boe_id", "kind")} |
                              {"url": reader_url(d), "words": sum(n_words(u.text) for u in units.get(d["source"], []))}
                              for d in DOCUMENTS],
                "chunks": {}}
    status = 0
    for design in DESIGNS:
        col = open_collection(design, create=True)
        chunks = [c for us in units.values() for c in chunk_units(us, design)]
        ok_sources = [s for s in units if s not in failed]
        removed = remove_stale(col, ok_sources, {c.id for c in chunks})
        print(f"\n[{design}] {len(chunks)} chunks" + (f", removed {removed} stale" if removed else ""))
        try:
            new, had = embed_and_store(chunks, col)
            print(f"[{design}] {had} already embedded, {new} embedded now, {col.count()} in the collection")
        except QuotaExhausted as e:
            print(f"\n[{design}] STOPPED: {e} {col.count()} of {len(chunks)} chunks are saved.\n"
                  "The free quota resets at midnight Pacific time (09:00 in Spain). "
                  "Run `uv run python main.py index` again then; it continues where it stopped.")
            status = 1
            break
        manifest["chunks"][design] = col.count()
    INDEX_DIR.mkdir(exist_ok=True)
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")
    return status


if __name__ == "__main__":
    sys.exit(main())
