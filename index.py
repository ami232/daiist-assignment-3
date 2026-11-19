"""
Assignment 3: build the index (`main.py index`).

Corpus: Spanish state legislation for autónomos, downloaded as consolidated
text from the BOE open-data API into corpus/ (git-ignored). Pipeline per file:

    fetch(source)                 -> corpus/<BOE id>.xml (+ .meta.xml)
    load_document(path)           -> DocMeta, [Block]   (current text only, notes stripped)
    chunk_document(meta, blocks, design) -> [Chunk]     (source + location metadata)
    embed_and_store(chunks, ...)  -> Chroma in index/   (Phase 3, not written yet)

server.py's add_document imports these functions; nothing here prints to
stdout on import or from the per-file functions (log to stderr only).

BOE reuse conditions: cite the source, keep the update date, and state that
consolidated texts are informational only (https://www.boe.es/informacion/aviso_legal).
"""

from __future__ import annotations

import csv
import hashlib
import logging
import re
import sys
import time
import xml.etree.ElementTree as ET
from dataclasses import asdict, dataclass
from pathlib import Path

import httpx

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"
OUTLINE_CSV = INDEX_DIR / "outline.csv"

BOE_API = "https://www.boe.es/datosabiertos/api/legislacion-consolidada/id/{boe_id}/{part}"
BOE_HTML = "https://www.boe.es/buscar/act.php?id={boe_id}"

log = logging.getLogger("index")


# --------------------------------------------------------------------------- #
# Sources                                                                      #
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class Source:
    """One document of the corpus. `start`/`end` are BOE block ids: start included, end excluded."""

    id: str                      # short id used in citations and in eval/questions.csv
    boe_id: str
    start: str | None = None
    end: str | None = None
    held_out: bool = False       # downloaded, but only indexed through add_document (demo)


SOURCES: list[Source] = [
    Source("LETA", "BOE-A-2007-13409"),                          # Estatuto del trabajo autónomo
    Source("LGSS", "BOE-A-2015-11724", start="tiv", end="tvi"),  # Títulos IV (RETA) y V (cese de actividad)
    # Reglamento de facturación only: the approving decree before it has its own "Artículo 1-3",
    # which would make citations like "RF, Artículo 1" ambiguous, and is out of scope anyway.
    Source("RF", "BOE-A-2012-14696", start="reglamento"),
    Source("RGAT", "BOE-A-2007-15984", start="tii", end="cv"),   # Título II caps. I-IV: censos, NIF, libros
    Source("COT2026", "BOE-A-2026-7296", start="a1-10", end="s3", held_out=True),  # Orden PJC/297/2026 arts. 18-19
]
SOURCES_BY_BOE_ID = {s.boe_id: s for s in SOURCES}


# --------------------------------------------------------------------------- #
# Chunking designs                                                             #
# --------------------------------------------------------------------------- #

@dataclass(frozen=True)
class ChunkDesign:
    name: str
    strategy: str                # "article": one chunk per article, split by apartado; "fixed": word windows
    max_words: int = 400         # article: articles longer than this are split
    size: int = 200              # fixed: window length in words
    overlap: int = 40            # fixed: words shared by consecutive windows


# PROVISIONAL parameters. Choosing them is the student's decision (tasks.md 3.2).
DESIGNS: dict[str, ChunkDesign] = {
    "article": ChunkDesign("article", "article", max_words=400),
    "fixed": ChunkDesign("fixed", "fixed", size=200, overlap=40),
}


# --------------------------------------------------------------------------- #
# Data model                                                                   #
# --------------------------------------------------------------------------- #

@dataclass
class DocMeta:
    source: str                  # "LETA"
    boe_id: str
    title: str                   # official title from the BOE metadata
    updated: str                 # consolidation date, "2026-09-02"
    url: str


@dataclass
class Block:
    block_id: str                # BOE block id, e.g. "a3-5" (not always readable: use `location`)
    location: str                # "Artículo 38 ter", "Disposición adicional segunda"
    path: str                    # "TÍTULO V Fomento … > CAPÍTULO II Incentivos …"
    text: str                    # current wording, notes stripped, one paragraph per line


@dataclass
class Chunk:
    id: str
    design: str
    source: str
    boe_id: str
    law_title: str
    location: str                # first location covered (the article for "article" chunks)
    locations: str               # every location covered, "; "-separated (fixed windows can span several)
    path: str
    block_id: str
    part: str                    # "1/1", "2/3"
    updated: str
    url: str
    n_words: int
    text: str

    def metadata(self) -> dict:
        """Everything but id and text, for the vector store (str/int values only)."""
        return {k: v for k, v in asdict(self).items() if k not in ("id", "text")}


# --------------------------------------------------------------------------- #
# Fetch                                                                        #
# --------------------------------------------------------------------------- #

def _get_xml(url: str, retries: int = 3) -> bytes:
    """GET a BOE API document, checking both HTTP status and the API's own status code."""
    for attempt in range(1, retries + 1):
        try:
            response = httpx.get(url, headers={"Accept": "application/xml"}, timeout=60, follow_redirects=True)
            response.raise_for_status()
            code = ET.fromstring(response.content).findtext("status/code")
            if code != "200":
                raise RuntimeError(f"BOE API status {code}")
            return response.content
        except Exception as error:  # noqa: BLE001 - retry anything, report the last one
            if attempt == retries:
                raise RuntimeError(f"Could not download {url}: {error}") from error
            log.warning("Retrying %s after %s", url, error)
            time.sleep(2 ** attempt)
    raise AssertionError("unreachable")


def fetch(source: Source, corpus_dir: Path = CORPUS_DIR) -> Path:
    """Download the consolidated text and metadata of `source` unless already in corpus/."""
    corpus_dir.mkdir(parents=True, exist_ok=True)
    text_path = corpus_dir / f"{source.boe_id}.xml"
    for part, path in (("texto", text_path), ("metadatos", text_path.with_suffix(".meta.xml"))):
        if path.is_file() and path.stat().st_size > 0:
            continue
        log.info("Downloading %s %s", source.boe_id, part)
        path.write_bytes(_get_xml(BOE_API.format(boe_id=source.boe_id, part=part)))
    return text_path


# --------------------------------------------------------------------------- #
# Extract and clean                                                            #
# --------------------------------------------------------------------------- #

NOTE_CLASSES = {"nota_pie", "nota_pie_2"}                 # "Se modifica por…", "Se añade por…"
SKIPPED_BLOCK_TYPES = {"preambulo", "firma", "nota_inicial", "encabezado"}
# A repealed article keeps only its heading and "(Derogado)": no law left, and its old title
# ("Beneficios en la cotización…") would compete in retrieval with the article that replaced it.
REPEALED_STUB = re.compile(r"^\((Derogad[oa]|Suprimid[oa]|Sin contenido)\)\.?$", re.IGNORECASE)


def _clean(text: str) -> str:
    return " ".join(text.replace("\xa0", " ").split())


def _version_text(version: ET.Element) -> str:
    """Text of one block version: paragraphs and table rows, editorial notes removed.

    BOE puts its annotations in <blockquote> ("Téngase en cuenta…", amendment
    history) and in p.nota_pie; neither is law, so both are dropped.
    """
    lines: list[str] = []
    for element in version:
        if element.tag == "blockquote" or element.get("class") in NOTE_CLASSES:
            continue
        if element.tag == "table":
            for row in element.iter("tr"):
                cells = [_clean(" ".join(cell.itertext())) for cell in row]
                if any(cells):
                    lines.append(" | ".join(cells))
        else:
            line = _clean("".join(element.itertext()))
            if line:
                lines.append(line)
    return "\n".join(lines)


def _heading(version: ET.Element) -> tuple[int, str]:
    """(level, text) of a heading block: 0 libro, 1 título, 2 capítulo, 3 sección, 4 subsección."""
    level, parts = None, []
    for p in version.iter("p"):
        css = p.get("class") or ""
        text = _clean("".join(p.itertext()))
        if css in NOTE_CLASSES or not text:
            continue
        if level is None:
            if css == "libro":
                level = 0
            elif css.startswith("capitulo"):
                level = 2
            elif text.startswith("Subsección"):
                level = 4
            elif text.startswith("Sección"):
                level = 3
            else:
                level = 1
        parts.append(text)
    return (level if level is not None else 1), " ".join(parts)


def _read_meta(text_path: Path) -> tuple[str, str, str]:
    """(boe_id, title, updated) from the sibling .meta.xml, else from the text itself."""
    meta_path = text_path.with_suffix(".meta.xml")
    if meta_path.is_file():
        meta = ET.parse(meta_path).getroot().find("data/metadatos")
        if meta is not None:
            stamp = meta.findtext("fecha_actualizacion") or ""
            updated = f"{stamp[:4]}-{stamp[4:6]}-{stamp[6:8]}" if len(stamp) >= 8 else "desconocida"
            return meta.findtext("identificador") or "", _clean(meta.findtext("titulo") or ""), updated
    first = ET.parse(text_path).getroot().find(".//version")
    boe_id = first.get("id_norma", text_path.stem) if first is not None else text_path.stem
    return boe_id, boe_id, "desconocida"


def load_document(path: Path, start: str | None = None, end: str | None = None) -> tuple[DocMeta, list[Block]]:
    """Parse a BOE consolidated-text XML into its current blocks.

    For each <bloque> only the last <version> (the one in force) is kept. Headings
    are tracked over the whole document, so a block range still gets its full path.
    Range defaults to the registry entry for this BOE id; unknown documents are read whole.
    """
    path = Path(path)
    boe_id, title, updated = _read_meta(path)
    source = SOURCES_BY_BOE_ID.get(boe_id)
    if source and start is None and end is None:
        start, end = source.start, source.end
    meta = DocMeta(
        source=source.id if source else boe_id,
        boe_id=boe_id,
        title=title,
        updated=updated,
        url=BOE_HTML.format(boe_id=boe_id),
    )

    root = ET.parse(path).getroot()
    if root.findtext("status/code") not in (None, "200"):
        raise ValueError(f"{path.name} is a BOE API error response, not a legal text")

    headings: list[tuple[int, str]] = []
    inside = start is None
    last_was_article = False
    blocks: list[Block] = []
    for bloque in root.iter("bloque"):
        block_id = bloque.get("id", "")
        if block_id == end:
            break
        if block_id == start:
            inside = True
        versions = bloque.findall("version")
        if not versions:
            continue
        current = versions[-1]
        kind = bloque.get("tipo")

        if kind == "encabezado":
            level, text = _heading(current)
            headings = [h for h in headings if h[0] < level] + [(level, text)]
            continue
        if not inside or kind in SKIPPED_BLOCK_TYPES:
            continue

        location = _clean(bloque.get("titulo") or block_id)
        # Disposiciones follow the last título without a heading of their own: don't inherit it.
        if location.startswith("Disposición") and last_was_article:
            headings = []
        last_was_article = location.startswith("Artículo")

        text = _version_text(current)
        lines = text.split("\n")
        if not text or (len(lines) <= 2 and REPEALED_STUB.match(lines[-1])):
            continue
        blocks.append(Block(block_id, location, " > ".join(h[1] for h in headings), text))

    if start is not None and not inside:
        raise ValueError(f"Block {start!r} not found in {path.name}")
    return meta, blocks


# --------------------------------------------------------------------------- #
# Chunk                                                                        #
# --------------------------------------------------------------------------- #

APARTADO = re.compile(r"^\d+\.\s")   # "1. ", "12. " start a numbered apartado


def _n_words(text: str) -> int:
    return len(text.split())


def _pack(units: list[str], max_words: int) -> list[str]:
    """Greedily join consecutive units into parts of at most max_words (a longer unit is cut by words)."""
    pieces: list[str] = []
    for unit in units:
        words = unit.split()
        if len(words) <= max_words:
            pieces.append(unit)
        else:
            pieces += [" ".join(words[i:i + max_words]) for i in range(0, len(words), max_words)]
    parts: list[str] = []
    for piece in pieces:
        if parts and _n_words(parts[-1]) + _n_words(piece) <= max_words:
            parts[-1] += "\n" + piece
        else:
            parts.append(piece)
    return parts


def _split_article(block: Block, max_words: int) -> list[str]:
    """The article whole if short enough; else split by apartado, repeating its heading line."""
    if _n_words(block.text) <= max_words:
        return [block.text]
    head, *lines = block.text.split("\n")
    units: list[str] = []
    for line in lines:
        if units and not APARTADO.match(line):
            units[-1] += "\n" + line        # letters, sub-paragraphs and table rows stay with their apartado
        else:
            units.append(line)
    budget = max_words - _n_words(head)
    if not units or budget < 50:                # one huge line, or a heading that eats the budget
        return _pack([block.text], max_words)
    parts = _pack(units, budget)
    return [f"{head} (parte {i}/{len(parts)})\n{part}" for i, part in enumerate(parts, 1)]


def _chunk_id(design: str, boe_id: str, block_id: str, part: str, text: str) -> str:
    return hashlib.sha1(f"{design}|{boe_id}|{block_id}|{part}|{text}".encode()).hexdigest()[:16]


def _make_chunk(meta: DocMeta, design: str, block: Block, locations: list[str], part: str, text: str) -> Chunk:
    return Chunk(
        id=_chunk_id(design, meta.boe_id, block.block_id, part, text),
        design=design,
        source=meta.source,
        boe_id=meta.boe_id,
        law_title=meta.title,
        location=block.location,
        locations="; ".join(locations),
        path=block.path,
        block_id=block.block_id,
        part=part,
        updated=meta.updated,
        url=f"{meta.url}#{block.block_id}",
        n_words=_n_words(text),
        text=text,
    )


def chunk_document(meta: DocMeta, blocks: list[Block], design: str | ChunkDesign) -> list[Chunk]:
    """Turn a document's blocks into chunks for one design."""
    cfg = DESIGNS[design] if isinstance(design, str) else design
    chunks: list[Chunk] = []

    if cfg.strategy == "article":
        for block in blocks:
            parts = _split_article(block, cfg.max_words)
            for i, text in enumerate(parts, 1):
                chunks.append(_make_chunk(meta, cfg.name, block, [block.location], f"{i}/{len(parts)}", text))

    elif cfg.strategy == "fixed":
        # One stream of words for the whole document; remember which block each word came from.
        words: list[str] = []
        owner: list[int] = []
        for b, block in enumerate(blocks):
            block_words = block.text.split()
            words += block_words
            owner += [b] * len(block_words)
        step = cfg.size - cfg.overlap
        starts = list(range(0, max(len(words) - cfg.overlap, 1), step))
        for n, i in enumerate(starts, 1):
            span = range(i, min(i + cfg.size, len(words)))
            covered = list(dict.fromkeys(owner[j] for j in span))
            first = blocks[covered[0]]
            text = " ".join(words[j] for j in span)
            chunks.append(_make_chunk(meta, cfg.name, first, [blocks[c].location for c in covered],
                                      f"{n}/{len(starts)}", text))
    else:
        raise ValueError(f"Unknown chunking strategy {cfg.strategy!r}")
    return chunks


# --------------------------------------------------------------------------- #
# Outline (lookup table for writing eval/questions.csv)                       #
# --------------------------------------------------------------------------- #

def write_outline(docs: list[tuple[Source, DocMeta, list[Block]]], path: Path = OUTLINE_CSV) -> None:
    """One row per location: the exact `source`/`location` strings to use in the test set."""
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["source", "location", "path", "words", "held_out", "url"])
        for source, meta, blocks in docs:
            for block in blocks:
                writer.writerow([meta.source, block.location, block.path, _n_words(block.text),
                                 int(source.held_out), f"{meta.url}#{block.block_id}"])


# --------------------------------------------------------------------------- #
# Main                                                                         #
# --------------------------------------------------------------------------- #

def load_corpus(sources: list[Source] = SOURCES) -> list[tuple[Source, DocMeta, list[Block]]]:
    docs = []
    for source in sources:
        meta, blocks = load_document(fetch(source))
        locations = [b.location for b in blocks]
        duplicates = {loc for loc in locations if locations.count(loc) > 1}
        if duplicates:
            raise ValueError(f"{source.id}: duplicate locations would make citations ambiguous: {sorted(duplicates)}")
        docs.append((source, meta, blocks))
    return docs


def main() -> None:
    logging.basicConfig(level=logging.INFO, stream=sys.stderr, format="%(message)s")
    logging.getLogger("httpx").setLevel(logging.WARNING)
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")

    docs = load_corpus()
    write_outline(docs)

    print(f"{'source':<8} {'words':>7} {'blocks':>6}  " + "  ".join(f"{d:>8}" for d in DESIGNS) + "  updated     title")
    total = 0
    chunks_per_design = {d: 0 for d in DESIGNS}
    for source, meta, blocks in docs:
        words = sum(_n_words(b.text) for b in blocks)
        counts = {d: len(chunk_document(meta, blocks, d)) for d in DESIGNS}
        flag = " (held out)" if source.held_out else ""
        if not source.held_out:
            total += words
            for d, n in counts.items():
                chunks_per_design[d] += n
        print(f"{meta.source:<8} {words:>7} {len(blocks):>6}  " + "  ".join(f"{counts[d]:>8}" for d in DESIGNS)
              + f"  {meta.updated}  {meta.title[:60]}{flag}")
    print(f"{'indexed':<8} {total:>7} {'':>6}  " + "  ".join(f"{chunks_per_design[d]:>8}" for d in DESIGNS))
    print(f"\nOutline written to {OUTLINE_CSV.relative_to(ROOT)}")
    if total < 50_000:
        raise SystemExit(f"Corpus has {total} words; the brief asks for at least 50,000.")

    # Phase 3: embed_and_store() for each design goes here.
    print("Embedding: not implemented yet (Phase 3).")


if __name__ == "__main__":
    main()
