"""
Assignment 3: build the index (`main.py index`).

Corpus: the complete Congreso trail of Proyecto de Ley Orgánica 121/000001,
"de representación paritaria y presencia equilibrada de mujeres y hombres",
whose Artículo primero amends the LOREG (LO 5/1985) and therefore governs the
candidate lists for the May 2027 elections.

Documents are downloaded into corpus/ (git-ignored), extracted with pypdf,
cleaned, chunked with source + location metadata, embedded with Gemini and
stored in index/. Vectors are cached on the SHA-256 of the chunk text, so
re-chunking never re-embeds an identical chunk and a crash costs nothing.

    uv run python main.py index            # full build (downloads, chunks, embeds)
    uv run python index.py --dry-run       # chunk and report only; no API calls

server.py imports chunk_file(), embed_and_store() and document_status().
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import time
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

import httpx
import numpy as np
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"
CHROMA_DIR = INDEX_DIR / "chroma"
VECTORS_PATH = INDEX_DIR / "vectors.npy"
VECTOR_KEYS_PATH = INDEX_DIR / "vector_keys.json"
CHUNKS_PATH = INDEX_DIR / "chunks.jsonl"
MANIFEST_PATH = INDEX_DIR / "manifest.json"

# A descriptive User-Agent is required: congreso.es answers 403 to a bare client.
USER_AGENT = "daiist-assignment3-indexer/1.0 (university coursework; public parliamentary documents)"
BASE_URL = "https://www.congreso.es/public_oficiales/L15/CONG"

# SETUP.md names this model and its ~1,000-texts-a-day free tier.
EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768  # reduced from the default to keep index/ far below the 90 MB cap
EMBED_BATCH = 16
EMBED_MAX_RETRIES = 6        # free tier caps embed tokens per minute; back off and retry

STRATEGIES = ("fixed_200", "structured")
DEFAULT_STRATEGY = "structured"

FIXED_SIZE, FIXED_OVERLAP = 200, 40
MAX_STRUCTURED_WORDS, STRUCTURED_OVERLAP = 400, 60


# --------------------------------------------------------------------------
# Corpus registry
# --------------------------------------------------------------------------

@dataclass(frozen=True)
class Source:
    doc_id: str
    titulo: str
    tramite: str
    genero: str                 # norma | enmiendas | debate
    path_fragment: str
    pages: tuple[tuple[int, int], ...] | None = None   # 1-indexed inclusive ranges
    held_back: bool = False     # excluded from the built index, for the add_document demo

    @property
    def url(self) -> str:
        return f"{BASE_URL}/{self.path_fragment}"

    @property
    def local_path(self) -> Path:
        return CORPUS_DIR / f"{self.doc_id}.PDF"


SOURCES: tuple[Source, ...] = (
    Source(
        "BOCG-15-A-1-1",
        "Proyecto de Ley Orgánica de representación paritaria y presencia equilibrada de mujeres y hombres",
        "proyecto", "norma", "BOCG/A/BOCG-15-A-1-1.PDF",
    ),
    Source(
        "BOCG-15-A-1-4",
        "Informe de la Ponencia",
        "informe_ponencia", "norma", "BOCG/A/BOCG-15-A-1-4.PDF",
    ),
    Source(
        "BOCG-15-A-1-8",
        "Aprobación definitiva por el Congreso de los Diputados",
        "aprobacion_definitiva", "norma", "BOCG/A/BOCG-15-A-1-8.PDF",
    ),
    Source(
        "DSCD-15-PL-54",
        "Debate y aprobación por el Pleno, sesión de 27 de junio de 2024",
        "debate_pleno", "debate", "DS/PL/DSCD-15-PL-54.PDF",
        # The session covers several agenda items. Pages 4-20 are this bill's
        # debate and 32-39 the votaciones, per the document's own orden del día.
        pages=((4, 20), (32, 39)),
    ),
    Source(
        "BOCG-15-A-1-2",
        "Enmiendas e índice de enmiendas al articulado",
        "enmiendas", "enmiendas", "BOCG/A/BOCG-15-A-1-2.PDF",
        held_back=True,
    ),
)

BY_DOC_ID = {s.doc_id: s for s in SOURCES}


# --------------------------------------------------------------------------
# Fetching
# --------------------------------------------------------------------------

def fetch(source: Source, force: bool = False) -> Path:
    """Download a document into corpus/, unless a valid copy is already there."""
    destination = source.local_path
    CORPUS_DIR.mkdir(parents=True, exist_ok=True)
    if destination.is_file() and not force and destination.read_bytes()[:4] == b"%PDF":
        return destination
    response = httpx.get(
        source.url,
        headers={"User-Agent": USER_AGENT},
        follow_redirects=True,
        timeout=60.0,
    )
    response.raise_for_status()
    if response.content[:4] != b"%PDF":
        raise RuntimeError(f"{source.url} did not return a PDF (got {response.headers.get('content-type')!r})")
    destination.write_bytes(response.content)
    return destination


# --------------------------------------------------------------------------
# Extraction and cleaning
# --------------------------------------------------------------------------

HEADER_PREFIXES = (
    "BOLETÍN OFICIAL DE LAS CORTES GENERALES",
    "CONGRESO DE LOS DIPUTADOS",
    "DIARIO DE SESIONES DEL CONGRESO DE LOS DIPUTADOS",
    "PLENO Y DIPUTACIÓN PERMANENTE",
    "CORTES GENERALES",
)
# "Serie A Núm. 1-8 31 de julio de 2024 Pág. 3" / "Núm. 54 27 de junio de 2024 Pág. 5"
RUNNING_HEAD = re.compile(
    r"^(?:Serie\s+\w+\s+)?Núm\.\s*[\w-]+\s+(?P<fecha>\d{1,2}\s+de\s+\w+\s+de\s+\d{4})\s+Pág\.\s*\d+\s*$"
)
CVE_LINE = re.compile(r"^cve:\s*(?P<cve>[\w-]+)\s*$", re.IGNORECASE)
DOT_LEADER = re.compile(r"\.{3,}\s*\d*\s*$")   # índice / sumario entries
HYPHEN_BREAK = re.compile(r"(\w)-\s*\n\s*(\w)")

MESES = {
    "enero": 1, "febrero": 2, "marzo": 3, "abril": 4, "mayo": 5, "junio": 6,
    "julio": 7, "agosto": 8, "septiembre": 9, "octubre": 10, "noviembre": 11, "diciembre": 12,
}


def _iso_date(spanish: str) -> str | None:
    match = re.match(r"(\d{1,2})\s+de\s+(\w+)\s+de\s+(\d{4})", spanish.strip(), re.IGNORECASE)
    if not match:
        return None
    day, month_name, year = match.groups()
    month = MESES.get(month_name.lower())
    return f"{year}-{month:02d}-{int(day):02d}" if month else None


@dataclass
class Page:
    number: int
    paragraphs: list[str]


@dataclass
class Document:
    doc_id: str
    titulo: str
    tramite: str
    genero: str
    url: str
    fecha: str
    cve: str
    pages: list[Page]
    front_matter: str = ""     # portada + sumario: skipped by the index, read for metadata
    content_sha256: str = ""

    @property
    def words(self) -> int:
        return sum(len(p.split()) for page in self.pages for p in page.paragraphs)


def _wanted(page_number: int, ranges: tuple[tuple[int, int], ...] | None) -> bool:
    return ranges is None or any(low <= page_number <= high for low, high in ranges)


def clean_page(raw: str) -> tuple[list[str], str | None, str | None]:
    """Return (paragraphs, fecha, cve) for one page.

    Strips the running header and the CVE stamp, repairs hyphenated line breaks
    and joins soft-wrapped lines back into paragraphs. The date and the CVE are
    captured before being discarded: both become chunk metadata, and the CVE is
    what lets a reader verify a citation against the signed original.
    """
    raw = HYPHEN_BREAK.sub(r"\1\2", raw)
    fecha = cve = None
    kept: list[str] = []

    for line in raw.splitlines():
        stripped = line.strip()
        if not stripped:
            kept.append("")
            continue
        if any(stripped.startswith(prefix) for prefix in HEADER_PREFIXES):
            continue
        head = RUNNING_HEAD.match(stripped)
        if head:
            fecha = fecha or _iso_date(head.group("fecha"))
            continue
        stamp = CVE_LINE.match(stripped)
        if stamp:
            cve = cve or stamp.group("cve")
            continue
        if DOT_LEADER.search(stripped):
            continue        # an índice entry, not body text
        kept.append(stripped)

    # Join soft wraps, but never across a structural heading. Legal texts are full
    # of short heading lines ("CAPÍTULO I", "Artículo primero.") that do not end in
    # sentence punctuation, so a naive join swallows them into the paragraph before
    # and silently destroys the article boundaries the structured chunker needs.
    paragraphs: list[str] = []
    buffer = ""
    for line in kept:
        if not line:
            if buffer:
                paragraphs.append(buffer.strip())
                buffer = ""
            continue
        if buffer and STRUCTURAL_START.match(line):
            paragraphs.append(buffer.strip())
            buffer = ""
        buffer = f"{buffer} {line}".strip() if buffer else line
        if re.search(r"[.:;!?»]$", line):
            paragraphs.append(buffer.strip())
            buffer = ""
    if buffer:
        paragraphs.append(buffer.strip())

    return [p for p in paragraphs if p], fecha, cve


def load_document(source: Source, path: Path | None = None) -> Document:
    """Extract, clean and page-filter one source into a Document."""
    pdf_path = path or source.local_path
    reader = PdfReader(str(pdf_path))
    pages: list[Page] = []
    fecha = cve = None

    front: list[str] = []
    for position, page in enumerate(reader.pages, start=1):
        paragraphs, page_fecha, page_cve = clean_page(page.extract_text() or "")
        fecha = fecha or page_fecha
        cve = cve or page_cve
        if position <= 3:
            front.extend(paragraphs)
        if _wanted(position, source.pages) and paragraphs:
            pages.append(Page(position, paragraphs))

    document = Document(
        doc_id=source.doc_id,
        titulo=source.titulo,
        tramite=source.tramite,
        genero=source.genero,
        url=source.url,
        fecha=fecha or "",
        cve=cve or source.doc_id,
        pages=pages,
        front_matter=" ".join(front),
    )
    body = "\n".join(p for page in pages for p in page.paragraphs)
    document.content_sha256 = hashlib.sha256(body.encode("utf-8")).hexdigest()
    return document


# --------------------------------------------------------------------------
# Chunking
# --------------------------------------------------------------------------

ORDINALES = (
    "primero|segundo|tercero|cuarto|quinto|sexto|séptimo|septimo|octavo|noveno|décimo|decimo|"
    "undécimo|undecimo|duodécimo|duodecimo|decimotercero|decimocuarto|decimoquinto|decimosexto|"
    "decimoséptimo|decimoseptimo|decimoctavo|decimonoveno|vigésimo|vigesimo|único|unico"
)
# The enacted text names articles with Spanish ordinals, not digits:
# "Artículo primero", not "Artículo 1". A ^Artículo \d regex matches nothing.
ARTICULO = re.compile(rf"^(Artículo\s+(?:{ORDINALES}|\d+)\b.*)")
DISPOSICION = re.compile(r"^(Disposición\s+(?:adicional|transitoria|derogatoria|final)\b.*)")
PREAMBULO = re.compile(r"^(PREÁMBULO|EXPOSICIÓN DE MOTIVOS|ÍNDICE)\s*$", re.IGNORECASE)
ENMIENDA = re.compile(r"^(ENMIENDA\s+NÚM\.\s*\d+)", re.IGNORECASE)
INTERVENCION = re.compile(r"^((?:El señor|La señora)\s+[A-ZÁÉÍÓÚÑÜ][^:]{0,80}):")
CAPITULO = re.compile(r"^((?:CAPÍTULO|TÍTULO|SECCIÓN)\s+[IVXLC]+\b.*)")

# Used by clean_page to stop a soft-wrap join from swallowing a heading.
STRUCTURAL_START = re.compile(
    "|".join(pattern.pattern for pattern in (ARTICULO, DISPOSICION, PREAMBULO, ENMIENDA, INTERVENCION, CAPITULO))
)
MIN_UNIT_WORDS = 25   # a bare "CAPÍTULO I" line is a label, not a chunk of its own

# Parliamentary groups, as they are written in this legislature's own documents.
# Listed because the group name is not delimited by punctuation in the enmiendas
# ("...Grupo Parlamentario VOX Enmienda a la totalidad..."), so a purely positional
# regex runs on into the next sentence. Unknown names fall back to the shape rule.
GRUPOS_CONOCIDOS = (
    "Popular en el Congreso", "Plurinacional SUMAR", "Junts per Catalunya",
    "Euskal Herria Bildu", "Vasco (EAJ-PNV)", "Confederal de Unidas Podemos",
    "Republicano", "Socialista", "Mixto", "VOX",
)
GRUPO_PREFIJO = re.compile(r"Grupo Parlamentario\s+")
GRUPO_FORMA = re.compile(
    r"((?:[A-ZÁÉÍÓÚÑ]\S*)(?:\s+(?:de|del|en|el|la|per|y|[A-ZÁÉÍÓÚÑ]\S*)){0,3})"
)
# Length-preserving fold, so offsets into the folded text still index the original.
_ACENTOS = str.maketrans("ÁÀÄÂÉÈËÊÍÌÏÎÓÒÖÔÚÙÜÛÑÇ", "AAAAEEEEIIIIOOOOUUUUNC")


def _fold(text: str) -> str:
    return text.upper().translate(_ACENTOS)


def grupos_en(text: str) -> list[str]:
    """Every parliamentary group named in this text, in order, de-duplicated."""
    found: list[str] = []
    for match in GRUPO_PREFIJO.finditer(text):
        tail = text[match.end():match.end() + 60]
        name = next((g for g in GRUPOS_CONOCIDOS if tail.startswith(g)), None)
        if name is None:
            shape = GRUPO_FORMA.match(tail)
            name = re.sub(r"[\s.,;:]+$", "", shape.group(1)) if shape else ""
        if name:
            found.append(name)
    return list(dict.fromkeys(found))


def grupo_del_interviniente(label: str, sumario: str) -> str:
    """The group a speaker belongs to, from the session's own sumario.

    The Diario de Sesiones never prints the group on the speech itself; it is only
    in the sumario, on the pages the index skips. The sumario lists speakers then
    their group ("... el señor Rego Candamil y la señora Belarra Urteaga, del Grupo
    Parlamentario Mixto"), so the first group named after a speaker is theirs.
    """
    upper = _fold(label)
    if "PRESIDENT" in upper:
        return "(presidencia)"
    if "MINISTR" in upper:
        return "(Gobierno, sin grupo)"
    surname = re.sub(r"^(El señor|La señora)\s+", "", label).strip()
    if not surname or not sumario:
        return ""
    folded_sumario, folded_surname = _fold(sumario), _fold(surname)
    position = folded_sumario.find(folded_surname)
    if position < 0:                       # try the first surname on its own
        first = folded_surname.split()[0] if folded_surname.split() else ""
        position = folded_sumario.find(first) if first else -1
    if position < 0:
        return ""
    grupos = grupos_en(sumario[position:])
    return grupos[0] if grupos else ""


@dataclass
class Chunk:
    text: str
    metadata: dict = field(default_factory=dict)

    @property
    def sha256(self) -> str:
        return hashlib.sha256(self.text.encode("utf-8")).hexdigest()

    @property
    def chunk_id(self) -> str:
        return f"{self.metadata['doc_id']}:{self.metadata['chunk_strategy']}:{self.metadata['ordinal']:04d}"


def _heading(paragraph: str, genero: str) -> str | None:
    """The structural label this paragraph starts, if it starts one."""
    if genero == "norma":
        for pattern in (ARTICULO, DISPOSICION, PREAMBULO, CAPITULO):
            match = pattern.match(paragraph)
            if match:
                return re.sub(r"\s+", " ", match.group(1))[:90].rstrip(". ")
    elif genero == "enmiendas":
        match = ENMIENDA.match(paragraph)
        if match:
            return match.group(1).upper()
    elif genero == "debate":
        match = INTERVENCION.match(paragraph)
        if match:
            return re.sub(r"\s+", " ", match.group(1))[:90]
    return None


SHORT_LABEL = re.compile(
    rf"^(Artículo\s+(?:{ORDINALES}|\d+)\b"
    r"|Disposición\s+(?:adicional|transitoria|derogatoria|final)\s+\S+"
    r"|CAPÍTULO\s+[IVXLC]+|TÍTULO\s+[IVXLC]+|SECCIÓN\s+[IVXLC]+"
    r"|ENMIENDA\s+NÚM\.\s*\d+)"
)


def _short_label(heading: str, genero: str) -> str:
    """A citation-sized label: 'Artículo primero', not the whole 90-character heading.

    This is what eval/questions.csv puts in expected_location, so it has to be
    short, stable and easy to write by hand.
    """
    if not heading:
        return "preámbulo"
    if genero == "debate":
        return heading
    match = SHORT_LABEL.match(heading)
    return match.group(1).rstrip(". ") if match else heading[:60].rstrip(". ")


def _base_metadata(document: Document, strategy: str) -> dict:
    return {
        "doc_id": document.doc_id,
        "titulo": document.titulo,
        "tramite": document.tramite,
        "genero": document.genero,
        "fecha": document.fecha,
        "cve": document.cve,
        "url": document.url,
        "expediente": "121/000001",
        "chunk_strategy": strategy,
        # Carried on every chunk so add_document can tell an identical re-add from a
        # revised edition without re-reading the whole document out of the index.
        "content_sha256": document.content_sha256,
        "superseded": False,
        "grupo": "",
    }


def _split_long(words: list[str], limit: int, overlap: int) -> list[list[str]]:
    if len(words) <= limit:
        return [words]
    pieces, start = [], 0
    while start < len(words):
        pieces.append(words[start:start + limit])
        if start + limit >= len(words):
            break
        start += limit - overlap
    return pieces


def chunk_fixed(document: Document, size: int = FIXED_SIZE, overlap: int = FIXED_OVERLAP) -> list[Chunk]:
    """Baseline: fixed-width word windows that ignore structure entirely."""
    words: list[tuple[str, int]] = [
        (word, page.number)
        for page in document.pages
        for paragraph in page.paragraphs
        for word in paragraph.split()
    ]
    chunks: list[Chunk] = []
    start = 0
    while start < len(words):
        window = words[start:start + size]
        if not window:
            break
        page_from, page_to = window[0][1], window[-1][1]
        metadata = _base_metadata(document, "fixed_200") | {
            "ordinal": len(chunks),
            "page": page_from,
            "page_to": page_to,
            "seccion": "",
            "interviniente": "",
            "location_label": f"{document.doc_id} · p. {page_from}"
            + (f"-{page_to}" if page_to != page_from else ""),
        }
        chunks.append(Chunk(" ".join(w for w, _ in window), metadata))
        if start + size >= len(words):
            break
        start += size - overlap
    return chunks


def chunk_structured(document: Document) -> list[Chunk]:
    """Structure-aware: one chunk per artículo, per enmienda, or per speaker turn.

    Paragraphs are carried with their page number all the way through, so that a
    long section split into several chunks cites the page each piece really came
    from. A citation a reader cannot verify is worse than no citation.
    """
    units: list[tuple[str, list[tuple[int, str]]]] = []
    heading, buffer = "", []

    for page in document.pages:
        for paragraph in page.paragraphs:
            found = _heading(paragraph, document.genero)
            if found:
                if buffer:
                    units.append((heading, buffer))
                heading, buffer = found, [(page.number, paragraph)]
            else:
                buffer.append((page.number, paragraph))
    if buffer:
        units.append((heading, buffer))

    # "CAPÍTULO I" sits alone on its line above the article it introduces. Fold such
    # stubs into the next unit so they become context instead of a one-line chunk.
    # Debates are left alone: a short "La señora PRESIDENTA: ..." is still a turn,
    # and merging it would misattribute it to the next speaker.
    if document.genero == "norma":
        folded: list[tuple[str, list[tuple[int, str]]]] = []
        carry: list[tuple[int, str]] = []
        for unit_heading, pairs in units:
            if sum(len(text.split()) for _, text in pairs) < MIN_UNIT_WORDS:
                carry.extend(pairs)
                continue
            folded.append((unit_heading, carry + pairs))
            carry = []
        if carry:
            if folded:
                folded[-1] = (folded[-1][0], folded[-1][1] + carry)
            else:
                folded.append(("", carry))
        units = folded

    chunks: list[Chunk] = []
    for unit_heading, pairs in units:
        words: list[tuple[str, int]] = [
            (word, page_number) for page_number, text in pairs for word in text.split()
        ]
        if not words:
            continue
        # The group is a property of the whole unit, so it must be resolved before
        # the unit is split: only the first piece carries the heading that names it.
        if document.genero == "debate":
            grupo = grupo_del_interviniente(unit_heading, document.front_matter)
        elif document.genero == "enmiendas":
            grupo = "; ".join(grupos_en(" ".join(text for _, text in pairs[:1])))
        else:
            grupo = ""
        pieces = _split_long(words, MAX_STRUCTURED_WORDS, STRUCTURED_OVERLAP)
        for part, piece in enumerate(pieces):
            page_from, page_to = piece[0][1], piece[-1][1]
            label = _short_label(unit_heading, document.genero)
            suffix = f" ({part + 1}/{len(pieces)})" if len(pieces) > 1 else ""
            pages = f"p. {page_from}" + (f"-{page_to}" if page_to != page_from else "")
            metadata = _base_metadata(document, "structured") | {
                "ordinal": len(chunks),
                "page": page_from,
                "page_to": page_to,
                "grupo": grupo,
                "seccion": label,
                "seccion_titulo": unit_heading or "",
                "interviniente": unit_heading if document.genero == "debate" else "",
                "location_label": f"{document.doc_id} · {label}{suffix} · {pages}",
            }
            chunks.append(Chunk(" ".join(word for word, _ in piece), metadata))
    return chunks


def chunk_document(document: Document, strategy: str) -> list[Chunk]:
    return chunk_fixed(document) if strategy == "fixed_200" else chunk_structured(document)


def infer_source(path: Path) -> Source:
    """Identify a PDF that is not in the registry, from its own CVE stamp and heading.

    Every BOCG and DS page carries `cve: <doc-id>`, so the document names itself.
    """
    reader = PdfReader(str(path))
    first = reader.pages[0].extract_text() or ""
    _, _, cve = clean_page(first)
    doc_id = cve or path.stem.upper()
    if doc_id in BY_DOC_ID:
        return BY_DOC_ID[doc_id]

    upper = first.upper()
    if "DIARIO DE SESIONES" in upper:
        genero, tramite = "debate", "debate"
    elif "ENMIENDA" in upper:
        genero, tramite = "enmiendas", "enmiendas"
    else:
        genero, tramite = "norma", "otro"
    fragment = ("DS/PL/" if genero == "debate" else "BOCG/A/") + f"{doc_id}.PDF"
    return Source(doc_id, f"Documento añadido: {doc_id}", tramite, genero, fragment)


def chunk_file(path: str | Path, strategy: str = DEFAULT_STRATEGY) -> list[Chunk]:
    """Public pipeline entry point. server.py's add_document calls this."""
    path = Path(path)
    if not path.is_file():
        raise FileNotFoundError(f"No such file: {path}")
    source = BY_DOC_ID.get(path.stem.upper()) or infer_source(path)
    document = load_document(source, path=path)
    return chunk_document(document, strategy)


# --------------------------------------------------------------------------
# Embedding, with a cache keyed on the chunk text
# --------------------------------------------------------------------------

def _load_vector_cache() -> dict[str, np.ndarray]:
    if not (VECTORS_PATH.is_file() and VECTOR_KEYS_PATH.is_file()):
        return {}
    keys = json.loads(VECTOR_KEYS_PATH.read_text(encoding="utf-8"))
    matrix = np.load(VECTORS_PATH)
    return {key: matrix[row] for row, key in enumerate(keys)}


def _save_vector_cache(cache: dict[str, np.ndarray]) -> None:
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    keys = list(cache)
    matrix = np.vstack([cache[key] for key in keys]).astype(np.float32) if keys else np.zeros((0, EMBED_DIM), np.float32)
    np.save(VECTORS_PATH, matrix)
    VECTOR_KEYS_PATH.write_text(json.dumps(keys), encoding="utf-8")


def _retry_delay(error: Exception, attempt: int) -> float | None:
    """Seconds to wait before retrying a rate-limited embed call, or None if fatal."""
    text = str(error)
    if "RESOURCE_EXHAUSTED" not in text and "429" not in text:
        return None
    match = re.search(r"retry in ([\d.]+)s", text, re.IGNORECASE)
    suggested = float(match.group(1)) if match else 0.0
    return max(suggested + 2.0, 5.0 * (attempt + 1))   # honour the server, else back off


def _embed_batch(texts: list[str], task_type: str) -> list[np.ndarray]:
    from google import genai
    from google.genai import types

    from api_key import load_api_key

    client = genai.Client(api_key=load_api_key())
    # One Content per text. google-genai treats a bare list[str] as the parts of a
    # SINGLE content and returns one embedding for the whole lot, which silently
    # drops every text but the first; the length check below makes that loud.
    contents = [types.Content(parts=[types.Part(text=t)]) for t in texts]
    response = None
    for attempt in range(EMBED_MAX_RETRIES):
        try:
            response = client.models.embed_content(
                model=EMBED_MODEL,
                contents=contents,
                config=types.EmbedContentConfig(task_type=task_type, output_dimensionality=EMBED_DIM),
            )
            break
        except Exception as error:  # noqa: BLE001 - only rate limits are retried
            delay = _retry_delay(error, attempt)
            if delay is None or attempt == EMBED_MAX_RETRIES - 1:
                raise
            print(f"    rate limited; waiting {delay:.0f}s", flush=True)
            time.sleep(delay)
    vectors = []
    for embedding in response.embeddings:
        vector = np.asarray(embedding.values, dtype=np.float32)
        norm = np.linalg.norm(vector)
        vectors.append(vector / norm if norm else vector)   # reduced dimensions need normalising
    if len(vectors) != len(texts):
        raise RuntimeError(
            f"embedding API returned {len(vectors)} vectors for {len(texts)} texts; "
            f"refusing to zip() them silently."
        )
    return vectors


def embed_texts(texts: list[str], task_type: str = "RETRIEVAL_DOCUMENT", log=print) -> list[np.ndarray]:
    """Embed texts, reusing any vector already cached for identical text."""
    cache = _load_vector_cache()
    wanted = {hashlib.sha256(t.encode("utf-8")).hexdigest(): t for t in texts}
    missing = [(key, text) for key, text in wanted.items() if key not in cache]
    if missing:
        log(f"  embedding {len(missing)} new texts ({len(wanted) - len(missing)} already cached)")
        for start in range(0, len(missing), EMBED_BATCH):
            batch = missing[start:start + EMBED_BATCH]
            for key, vector in zip((k for k, _ in batch), _embed_batch([t for _, t in batch], task_type)):
                cache[key] = vector
            _save_vector_cache(cache)   # save as we go: a crash or the daily cap loses nothing
            log(f"    {min(start + EMBED_BATCH, len(missing))}/{len(missing)}")
    return [cache[hashlib.sha256(t.encode("utf-8")).hexdigest()] for t in texts]


def _document_words(doc_id: str) -> int | None:
    """The document's own word count, the way a full build measures it."""
    source = BY_DOC_ID.get(doc_id)
    if source is None:
        return None
    try:
        return load_document(source).words
    except Exception:  # noqa: BLE001 - fall back to the caller's estimate
        return None


def record_added_document(chunks: list["Chunk"], strategy: str) -> dict:
    """Write an added document into chunks.jsonl and manifest.json.

    embed_and_store() updates Chroma and the vector cache, which is what search reads,
    but chunks.jsonl and manifest.json were only ever written by a full `main.py index`
    build. A document added through add_document was therefore invisible in both: the
    manifest still listed it as `held_back` while 209 of its chunks were being returned
    by search. Idempotent - re-recording the same document replaces its rows.
    """
    if not chunks:
        return {"recorded": 0}
    doc_id = chunks[0].metadata["doc_id"]

    existing = []
    if CHUNKS_PATH.is_file():
        with CHUNKS_PATH.open(encoding="utf-8") as handle:
            existing = [json.loads(line) for line in handle if line.strip()]
    kept = [r for r in existing
            if not (r.get("doc_id") == doc_id and r.get("chunk_strategy") == strategy)]
    with CHUNKS_PATH.open("w", encoding="utf-8") as handle:
        for record in kept:
            handle.write(json.dumps(record, ensure_ascii=False) + "\n")
        for chunk in chunks:
            handle.write(json.dumps(
                {"id": chunk.chunk_id, "text": chunk.text, **chunk.metadata},
                ensure_ascii=False) + "\n")

    if MANIFEST_PATH.is_file():
        manifest = json.loads(MANIFEST_PATH.read_text(encoding="utf-8"))
        meta = chunks[0].metadata
        manifest["held_back"] = [h for h in manifest.get("held_back", [])
                                 if h.get("doc_id") != doc_id]
        if not any(d.get("doc_id") == doc_id for d in manifest.get("documents", [])):
            manifest.setdefault("documents", []).append({
                "doc_id": doc_id,
                "titulo": meta.get("titulo", ""),
                "tramite": meta.get("tramite", ""),
                "genero": meta.get("genero", ""),
                "fecha": meta.get("fecha", ""),
                "cve": meta.get("cve", ""),
                "url": meta.get("url", ""),
                # Count words from the document's own text, as a full build does.
                # Summing chunk words double-counts the overlap between split chunks.
                "words": _document_words(doc_id) or sum(len(c.text.split()) for c in chunks),
                "content_sha256": meta.get("content_sha256", ""),
                "added_by": "add_document",
            })
        MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2),
                                 encoding="utf-8")
    return {"recorded": len(chunks), "doc_id": doc_id}


def _collection(strategy: str):
    import chromadb

    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return client.get_or_create_collection(name=strategy, metadata={"hnsw:space": "cosine"})


def document_status(doc_id: str, content_sha256: str, strategy: str = DEFAULT_STRATEGY) -> str:
    """'new', 'identical' or 'revised' — the add_document duplicate policy."""
    try:
        existing = _collection(strategy).get(where={"doc_id": doc_id}, include=["metadatas"])
    except Exception:
        return "new"
    metadatas = existing.get("metadatas") or []
    if not metadatas:
        return "new"
    hashes = {m.get("content_sha256") for m in metadatas}
    return "identical" if content_sha256 in hashes else "revised"


def embed_and_store(chunks: list[Chunk], strategy: str = DEFAULT_STRATEGY, log=print) -> dict:
    """Embed any chunk without a cached vector and upsert everything into Chroma."""
    if not chunks:
        return {"chunks": 0, "embedded": 0}
    before = len(_load_vector_cache())
    vectors = embed_texts([c.text for c in chunks], "RETRIEVAL_DOCUMENT", log=log)
    after = len(_load_vector_cache())

    collection = _collection(strategy)
    collection.upsert(
        ids=[c.chunk_id for c in chunks],
        embeddings=[v.tolist() for v in vectors],
        documents=[c.text for c in chunks],
        metadatas=[c.metadata for c in chunks],
    )
    return {"chunks": len(chunks), "embedded": max(after - before, 0), "strategy": strategy}


# --------------------------------------------------------------------------
# Build
# --------------------------------------------------------------------------

def build(dry_run: bool = False, strategies: tuple[str, ...] = STRATEGIES) -> dict:
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    active = [s for s in SOURCES if not s.held_back]

    print(f"Corpus: {len(active)} documents (expediente 121/000001)\n")
    documents: list[Document] = []
    for source in active:
        path = fetch(source)
        document = load_document(source)
        documents.append(document)
        print(f"  {document.doc_id:<16} {document.words:>7,} words  {len(document.pages):>3} pages  {document.fecha}  [{document.tramite}]")
    total_words = sum(d.words for d in documents)
    print(f"\n  total: {total_words:,} words\n")

    manifest: dict = {
        "expediente": "121/000001",
        "embed_model": EMBED_MODEL,
        "embed_dim": EMBED_DIM,
        "total_words": total_words,
        "licence": "congreso.es aviso legal: reuse permitted if content is unaltered, its sense "
                   "is not distorted, the source is cited and the last update date is given.",
        "documents": [
            {
                "doc_id": d.doc_id, "titulo": d.titulo, "tramite": d.tramite, "genero": d.genero,
                "fecha": d.fecha, "cve": d.cve, "url": d.url, "words": d.words,
                "content_sha256": d.content_sha256,
            }
            for d in documents
        ],
        "held_back": [
            {"doc_id": s.doc_id, "titulo": s.titulo, "url": s.url, "why": "reserved for the add_document demo"}
            for s in SOURCES if s.held_back
        ],
        "strategies": {},
    }

    all_chunks: list[Chunk] = []
    for strategy in strategies:
        chunks = [c for d in documents for c in chunk_document(d, strategy)]
        lengths = [len(c.text.split()) for c in chunks]
        manifest["strategies"][strategy] = {
            "chunks": len(chunks),
            "mean_words": round(sum(lengths) / len(lengths), 1) if lengths else 0,
            "max_words": max(lengths, default=0),
        }
        print(f"  {strategy:<12} {len(chunks):>4} chunks   mean {manifest['strategies'][strategy]['mean_words']:>5} words   max {manifest['strategies'][strategy]['max_words']}")
        all_chunks.extend(chunks)

        if not dry_run:
            result = embed_and_store(chunks, strategy)
            print(f"  {strategy:<12} stored {result['chunks']} chunks, {result['embedded']} new embeddings")

    with CHUNKS_PATH.open("w", encoding="utf-8") as handle:
        for chunk in all_chunks:
            handle.write(json.dumps({"id": chunk.chunk_id, "text": chunk.text, **chunk.metadata}, ensure_ascii=False) + "\n")
    MANIFEST_PATH.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")

    budget = sum(v["chunks"] for v in manifest["strategies"].values())
    print(f"\n  {budget} chunks in total -> at most {budget} embeddings for a cold build "
          f"(free tier is ~1,000/day)")
    if dry_run:
        print("  dry run: nothing embedded, no API calls made")
    return manifest


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the index.")
    parser.add_argument("--dry-run", action="store_true", help="chunk and report only; no API calls")
    parser.add_argument("--strategy", choices=STRATEGIES, help="build only one strategy")
    args = parser.parse_args()
    strategies = (args.strategy,) if args.strategy else STRATEGIES
    build(dry_run=args.dry_run, strategies=strategies)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
