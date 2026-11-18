"""
Assignment 3: build the index (`main.py index`).

Corpus (documents/, consolidated BOE texts for a landlord renting a flat in Barcelona):
    BOE-A-1994-26003  Ley 29/1994 de Arrendamientos Urbanos (LAU)
    BOE-A-2008-3657   Llei 18/2007 del dret a l'habitatge (Catalonia, incl. Llei 11/2025)
    BOE-A-2024-281    Decret-llei 3/2023 on tourist flats (Catalonia)

Steps, as functions server.py's add-document tool can import:
    parse_units(path)        PDF -> legal units (preamble, articles, disposiciones,
                             annex) with their Título/Capítulo/Sección and pages
    chunk_file(path)         one chunk per unit; long ones split at apartados
    chunk_fixed(path)        baseline design: 300-word windows, 50 overlap, no structure
    embed_and_store(chunks)  embed only chunks without a saved vector, store each
                             batch in ChromaDB (index/chroma) as soon as it returns
    index_file(path, strategy)  chunk + drop stale chunks + embed_and_store; one
                             ChromaDB collection per design (chunks_structure, chunks_fixed)

Chunk ids hash the chunk text, so re-running embeds nothing already stored.
"""

import hashlib
import math
import re
import sys
import time
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent
DOCS_DIR = ROOT / "documents"
CHROMA_DIR = ROOT / "index" / "chroma"

EMBED_MODEL = "gemini-embedding-2"
EMBED_BATCH = 20
STRATEGY = "structure"   # chunking design; each design gets its own collection
MAX_WORDS = 300          # split a unit into several chunks above this

# Short names for citations; other documents use the title on their first page.
SHORT_NAMES = {
    "BOE-A-1994-26003": ("LAU", "Ley 29/1994, de 24 de noviembre, de Arrendamientos Urbanos"),
    "BOE-A-2008-3657": ("Llei 18/2007", "Ley 18/2007, de 28 de diciembre, del derecho a la vivienda (Cataluña)"),
    "BOE-A-2024-281": ("Decret-llei 3/2023", "Decreto-ley 3/2023, de 7 de noviembre, de medidas urgentes sobre "
                       "el régimen urbanístico de las viviendas de uso turístico (Cataluña)"),
}


def log(*args) -> None:
    """Log to stderr: server.py imports this module and stdout belongs to MCP."""
    print(*args, file=sys.stderr, flush=True)


# ---- 1. Extract and parse the legal structure ------------------------------ #

BOILERPLATE = re.compile(r"^(BOLETÍN OFICIAL DEL ESTADO|LEGISLACIÓN CONSOLIDADA|Página \d+"
                         r"|Este documento es de carácter informativo y no tiene valor jurídico\.)\s*$")
RE_TITULO = re.compile(r"^TÍTULO (PRELIMINAR|[IVXLC]+)\s*$")
RE_CAPITULO = re.compile(r"^CAPÍTULO (PRELIMINAR|ÚNICO|[IVXLC]+)\s*$")
RE_SECCION = re.compile(r"^Sección (\S+?)\.\s*(.*)$")
# Headings have two spaces (or end of line) after the dot; references in the text don't.
RE_UNIT = re.compile(
    r"^((?:Artículo \d+(?: (?:bis|ter|quater))?)"
    r"|(?:Disposición (?:adicional|transitoria|derogatoria|final)(?: [a-záéíóúñ]+)*?))"
    r"\.(?:\s{2,}|\s*$)(.*)$")
RE_ROMAN = re.compile(r"^([IVXL]+)\s*$")
RE_ANNEX = re.compile(r"^(ANEXO(?: [IVX\d]+)?)\s*$")
RE_APARTADO = re.compile(r"^(\d+(?: bis)?)\. ")


@dataclass
class Unit:
    kind: str           # preamble | article | disposicion | annex
    label: str          # "Artículo 36", "Preámbulo II"
    heading: str = ""   # "Fianza."
    titulo: str = ""
    capitulo: str = ""
    seccion: str = ""
    lines: list = field(default_factory=list)   # [(text, page)]


def wrapped(line: str) -> bool:
    """In BOE PDFs a line that continues on the next one ends in a space or hyphen."""
    return line.endswith((" ", "-"))


def parse_units(path: Path) -> tuple[dict, list[Unit]]:
    from pypdf import PdfReader

    lines = []
    for page_no, page in enumerate(PdfReader(path).pages, start=1):
        text = unicodedata.normalize("NFKC", page.extract_text() or "")   # 'ﬁ' -> 'fi'
        lines += [(l, page_no) for l in text.split("\n") if l.strip() and not BOILERPLATE.match(l.strip())]

    doc_id = path.stem.removesuffix("-consolidado")
    short, title = SHORT_NAMES.get(doc_id, (doc_id, lines[0][0].strip() if lines else doc_id))
    meta = {"doc_id": doc_id, "source": path.name, "short": short, "title": title}

    # Skip cover and table of contents: the body starts after "TEXTO CONSOLIDADO".
    start = next((i + 1 for i, (l, _) in enumerate(lines) if l.strip() == "TEXTO CONSOLIDADO"), 0)
    lines = [(l, p) for l, p in lines[start:] if not l.startswith("Última modificación:")]

    units, ctx = [], {"titulo": "", "capitulo": "", "seccion": ""}
    current = Unit("preamble", "Preámbulo")
    pending_name = None       # the next line(s) name the TÍTULO/CAPÍTULO just seen
    pending_heading = False   # the unit heading wraps onto the next line
    in_preamble = True

    def new_unit(kind, label, heading=""):
        nonlocal current
        if current.lines:
            units.append(current)
        current = Unit(kind, label, heading, **ctx)

    for line, page in lines:
        text = line.strip()
        if pending_heading:
            current.heading += line
            pending_heading = wrapped(line)
        elif pending_name:
            ctx[pending_name] += " " + line
            if not wrapped(line):
                ctx[pending_name] = re.sub(r"\s+", " ", ctx[pending_name]).strip()
                pending_name = None
        elif m := RE_TITULO.match(text):
            ctx.update(titulo=f"TÍTULO {m.group(1)}.", capitulo="", seccion="")
            pending_name, in_preamble = "titulo", False
        elif m := RE_CAPITULO.match(text):
            ctx.update(capitulo=f"CAPÍTULO {m.group(1)}.", seccion="")
            pending_name, in_preamble = "capitulo", False
        elif m := RE_SECCION.match(text):
            ctx["seccion"] = f"Sección {m.group(1)}. {m.group(2)}"
            pending_name = "seccion" if wrapped(line) else None
        elif m := RE_UNIT.match(line):
            label, heading = m.group(1), m.group(2)
            kind = "article" if label.startswith("Artículo") else "disposicion"
            if kind == "disposicion":
                ctx.update(titulo="", capitulo="", seccion="")
            new_unit(kind, label, heading)
            pending_heading, in_preamble = bool(heading.strip()) and wrapped(line), False
        elif RE_ANNEX.match(text):
            ctx.update(titulo="", capitulo="", seccion="")
            new_unit("annex", text.title())
            in_preamble = False
        elif in_preamble and text == "PREÁMBULO":
            pass
        elif in_preamble and (m := RE_ROMAN.match(text)):
            new_unit("preamble", f"Preámbulo {m.group(1)}")
        else:
            current.lines.append((line, page))

    if current.lines:
        units.append(current)
    for u in units:
        u.heading = re.sub(r"\s+", " ", u.heading).strip()
    return meta, units


# ---- 2. Chunk -------------------------------------------------------------- #

def paragraphs(unit: Unit) -> list[dict]:
    """Re-join wrapped lines into paragraphs, keeping pages and the apartado number."""
    out, buf, first_page, apartado = [], "", None, ""
    for line, page in unit.lines:
        first_page = first_page or page
        buf += line[:-1] if line.endswith("-") and not line.endswith(" -") else line
        if not wrapped(line):
            text = re.sub(r"\s+", " ", buf).strip()
            if m := RE_APARTADO.match(text):
                apartado = m.group(1)
            out.append({"text": text, "pages": (first_page, page), "apartado": apartado})
            buf, first_page = "", None
    if buf.strip():
        out.append({"text": re.sub(r"\s+", " ", buf).strip(),
                    "pages": (first_page, unit.lines[-1][1]), "apartado": apartado})
    return out


def split_long(p: dict, max_words: int) -> list[dict]:
    """Split one over-long paragraph at sentence ends."""
    if len(p["text"].split()) <= max_words:
        return [p]
    parts, buf = [], []
    for s in re.split(r"(?<=[.;:])\s+", p["text"]):
        if buf and len(" ".join(buf + [s]).split()) > max_words:
            parts.append(" ".join(buf))
            buf = []
        buf.append(s)
    parts.append(" ".join(buf))
    return [{**p, "text": t} for t in parts]


def pack(paras: list[dict], max_words: int) -> list[list[dict]]:
    """Group consecutive paragraphs into balanced groups of at most ~max_words."""
    total = sum(len(p["text"].split()) for p in paras)
    if total <= max_words:
        return [paras]
    target = total / math.ceil(total / max_words)
    groups, buf, n = [], [], 0
    for p in paras:
        w = len(p["text"].split())
        if buf and (n + w > max_words or n >= target):
            groups.append(buf)
            buf, n = [], 0
        buf.append(p)
        n += w
    return groups + [buf]


def chunk_file(path: str | Path, max_words: int = MAX_WORDS) -> list[dict]:
    """Chunk one PDF into dicts: id, text (embedded and shown to the model), metadata."""
    path = Path(path)
    meta, units = parse_units(path)
    chunks = []
    for unit in units:
        paras = [q for p in paragraphs(unit) for q in split_long(p, max_words)]
        if not paras:
            continue
        groups = pack(paras, max_words)
        for part, group in enumerate(groups, start=1):
            seen = [p["apartado"] for p in group if p["apartado"]]
            apartados = "" if not seen else seen[0] if seen[0] == seen[-1] else f"{seen[0]}–{seen[-1]}"
            location = unit.label
            if apartados:
                word = "entradas" if unit.kind == "annex" else "apartados" if "–" in apartados else "apartado"
                location += f", {word} {apartados}"
            elif len(groups) > 1:
                location += f" (parte {part}/{len(groups)})"
            page_start, page_end = group[0]["pages"][0], group[-1]["pages"][1]
            pages = f"p. {page_start}" if page_start == page_end else f"pp. {page_start}–{page_end}"

            # Header gives the embedding and the model the context the bare text lacks.
            header = f"[{meta['short']} — {meta['title']}]\n"
            hierarchy = " › ".join(x for x in (unit.titulo, unit.capitulo, unit.seccion) if x)
            header += f"{hierarchy}\n" if hierarchy else ""
            header += f"{unit.label}. {unit.heading}".strip(". ") if unit.heading else unit.label
            header += f" ({location.split(', ', 1)[1]})" if ", " in location else ""
            body = "\n".join(p["text"] for p in group)
            text = f"{header}\n\n{body}"

            digest = hashlib.sha1(f"{STRATEGY}|{max_words}|{text}".encode()).hexdigest()[:16]
            chunks.append({
                "id": f"{meta['doc_id']}:{digest}",
                "text": text,
                "metadata": {
                    "doc_id": meta["doc_id"], "source": meta["source"], "law": meta["short"],
                    "article": unit.label, "article_heading": unit.heading, "apartados": apartados,
                    "titulo": unit.titulo, "capitulo": unit.capitulo, "seccion": unit.seccion,
                    "page_start": page_start, "page_end": page_end,
                    "citation": f"{meta['short']}, {location}, {pages}",
                },
            })
    return chunks


def chunk_fixed(path: str | Path, size: int = 300, overlap: int = 50) -> list[dict]:
    """Baseline design: fixed windows of `size` words that ignore the legal structure.

    Same text as chunk_file (headings included inline), no context header. The
    articles a window touches are kept in metadata only, to score retrieval.
    """
    path = Path(path)
    meta, units = parse_units(path)
    words = []   # (word, page, unit label)
    for u in units:
        first_page = u.lines[0][1] if u.lines else 0
        heading = f"{u.label}. {u.heading}" if u.heading else u.label
        words += [(w, first_page, u.label) for w in heading.split()]
        words += [(w, page, u.label) for line, page in u.lines for w in line.split()]

    chunks = []
    for start in range(0, len(words), size - overlap):
        window = words[start:start + size]
        labels = list(dict.fromkeys(label for _, _, label in window))
        text = " ".join(w for w, _, _ in window)
        page_start, page_end = window[0][1], window[-1][1]
        pages = f"p. {page_start}" if page_start == page_end else f"pp. {page_start}–{page_end}"
        span = labels[0] if len(labels) == 1 else f"{labels[0]} – {labels[-1]}"
        digest = hashlib.sha1(f"fixed|{size}|{overlap}|{text}".encode()).hexdigest()[:16]
        chunks.append({
            "id": f"{meta['doc_id']}:{digest}",
            "text": text,
            "metadata": {
                "doc_id": meta["doc_id"], "source": meta["source"], "law": meta["short"],
                "articles": "|".join(labels), "page_start": page_start, "page_end": page_end,
                "citation": f"{meta['short']}, {span}, {pages}",
            },
        })
        if start + size >= len(words):
            break
    return chunks


CHUNKERS = {"structure": chunk_file, "fixed": chunk_fixed}


# ---- 3. Embed and store ---------------------------------------------------- #

_client = None


def embed_texts(texts: list[str], task_type: str = "RETRIEVAL_DOCUMENT") -> list[list[float]]:
    """Embed texts with Gemini; waits and retries when rate limited (HTTP 429)."""
    global _client
    from google import genai
    from google.genai import errors, types
    from api_key import load_api_key

    _client = _client or genai.Client(api_key=load_api_key())
    # One Content per text: gemini-embedding-2 would merge a plain list of strings
    # into ONE multimodal input and return a single vector.
    contents = [types.Content(parts=[types.Part(text=t)]) for t in texts]
    for attempt in range(6):
        try:
            result = _client.models.embed_content(
                model=EMBED_MODEL, contents=contents, config=types.EmbedContentConfig(task_type=task_type))
            return [e.values for e in result.embeddings]
        except errors.ClientError as error:
            if error.code != 429 or "PerDay" in str(error) or attempt == 5:
                raise
            m = re.search(r"retry in ([\d.]+)s", str(error))
            wait = float(m.group(1)) + 1 if m else 2 ** attempt * 10
            log(f"  rate limited, waiting {wait:.0f}s ...")
            time.sleep(wait)


def embed_query(query: str) -> list[float]:
    return embed_texts([query], task_type="RETRIEVAL_QUERY")[0]


def get_collection(strategy: str = STRATEGY):
    import chromadb
    return chromadb.PersistentClient(path=str(CHROMA_DIR)).get_or_create_collection(
        name=f"chunks_{strategy}", metadata={"hnsw:space": "cosine"})


def embed_and_store(chunks: list[dict], collection=None) -> dict:
    """Embed only chunks without a saved vector; store each batch as soon as it returns."""
    collection = collection or get_collection()
    existing = set(collection.get(ids=[c["id"] for c in chunks], include=[])["ids"])
    todo = [c for c in chunks if c["id"] not in existing]
    for i in range(0, len(todo), EMBED_BATCH):
        batch = todo[i:i + EMBED_BATCH]
        collection.add(ids=[c["id"] for c in batch], documents=[c["text"] for c in batch],
                       metadatas=[c["metadata"] for c in batch],
                       embeddings=embed_texts([c["text"] for c in batch]))
        log(f"  embedded {i + len(batch)}/{len(todo)}")
    return {"chunks": len(chunks), "already_indexed": len(existing), "embedded": len(todo)}


def index_file(path: str | Path, strategy: str = STRATEGY) -> dict:
    """Chunk one document, drop its chunks that no longer exist, embed the new ones."""
    path = Path(path)
    collection = get_collection(strategy)
    chunks = CHUNKERS[strategy](path)
    if not chunks:
        raise ValueError(f"No text could be extracted from {path.name}.")
    doc_id = chunks[0]["metadata"]["doc_id"]
    keep = {c["id"] for c in chunks}
    stale = [i for i in collection.get(where={"doc_id": doc_id}, include=[])["ids"] if i not in keep]
    if stale:
        collection.delete(ids=stale)
    return {**embed_and_store(chunks, collection), "source": path.name, "removed_stale": len(stale)}


def main() -> None:
    # Both designs are built so evaluate.py can compare them; the server uses STRATEGY.
    for strategy in CHUNKERS:
        for path in sorted(DOCS_DIR.glob("*.pdf")):
            log(f"[{strategy}] {path.name}")
            s = index_file(path, strategy)
            log(f"  {s['chunks']} chunks: {s['already_indexed']} already indexed, "
                f"{s['embedded']} embedded, {s['removed_stale']} stale removed")
        log(f"[{strategy}] {get_collection(strategy).count()} chunks in {CHROMA_DIR.relative_to(ROOT)}")


if __name__ == "__main__":
    main()
