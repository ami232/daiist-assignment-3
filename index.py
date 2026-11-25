"""
Assignment 3: build the index (`main.py index`).

Downloads the corpus (Spanish takeover rules for a merger arbitrage desk) into
corpus/, extracts and cleans the text, chunks it with source and location
metadata, embeds it with Gemini and stores it in index/ (ChromaDB). Vectors are
saved batch by batch and only chunks without a saved vector are embedded, so a
crash or the daily quota loses nothing: run it again tomorrow and it resumes.

server.py's add_document tool imports `add_document` from here, which runs one
file through exactly the same chunk_file() and embed_and_store().

    uv run python index.py                    # download, chunk, embed every design
    uv run python index.py --design struct    # only one design
    uv run python index.py --dry-run          # download and chunk, no embeddings
    python3 index.py --download-only          # just the documents (works without uv)
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
import os
import re
import unicodedata
from dataclasses import dataclass, field
from pathlib import Path

import rag
from rag import ACTIVE_DESIGN, DESIGNS, EMBED_BATCH, INDEX_DIR, ROOT, log, sha

CORPUS_DIR = Path(os.environ.get("RAG_CORPUS_DIR", ROOT / "corpus"))
USER_AGENT = "daiist-assignment-3 (IE University coursework; jlopez.ieu2022@student.ie.edu)"

# ---------------------------------------------------------------- the corpus
# Spanish legislation is not protected by copyright (art. 13 LPI) and the BOE
# authorises reuse of its consolidated texts (aviso legal, Ley 37/2007).
# CNMV: its legal notice allows reuse if reproduced faithfully and the source
# is cited. (Directive 2004/25/EC was dropped: EUR-Lex answers scripts with an
# empty page, and the corpus has 80k words without it.)
BOE_LICENCE = "BOE: reutilización autorizada (Ley 37/2007, aviso legal BOE); texto consolidado de carácter informativo"

SOURCES = [
    {
        "doc_id": "RD1066-2007",
        "title": "Real Decreto 1066/2007, régimen de las ofertas públicas de adquisición de valores",
        "short": "RD 1066/2007 (OPAs)",
        "kind": "boe",
        "boe_id": "BOE-A-2007-14483",
        "url": "https://www.boe.es/eli/es/rd/2007/07/27/1066/con",
        "licence": BOE_LICENCE,
    },
    {
        "doc_id": "CNMV-QA-OPAS",
        "title": "CNMV, Preguntas y respuestas sobre ofertas públicas de adquisición de valores (opas)",
        "short": "CNMV Q&A OPAs",
        "kind": "pdf",
        "url": "https://www.cnmv.es/docportal/Legislacion/FAQ/QAs_OPAs.pdf",
        "licence": "CNMV: reutilización permitida citando la fuente y sin alterar el contenido (nota legal cnmv.es)",
    },
    {
        "doc_id": "LDC-15-2007",
        "title": "Ley 15/2007, de 3 de julio, de Defensa de la Competencia",
        "short": "Ley 15/2007 (Competencia)",
        "kind": "boe",
        "boe_id": "BOE-A-2007-12946",
        "url": "https://www.boe.es/eli/es/l/2007/07/03/15/con",
        "licence": BOE_LICENCE,
    },
    {
        "doc_id": "LEY19-2003",
        "title": "Ley 19/2003, régimen jurídico de los movimientos de capitales y de las transacciones económicas con el exterior",
        "short": "Ley 19/2003 (inversiones exteriores)",
        "kind": "boe",
        "boe_id": "BOE-A-2003-13471",
        "url": "https://www.boe.es/eli/es/l/2003/07/04/19/con",
        "licence": BOE_LICENCE,
    },
    {
        "doc_id": "RD571-2023",
        "title": "Real Decreto 571/2023, de 4 de julio, sobre inversiones exteriores",
        "short": "RD 571/2023 (inversiones exteriores)",
        "kind": "boe",
        "boe_id": "BOE-A-2023-15549",
        "url": "https://www.boe.es/eli/es/rd/2023/07/04/571/con",
        "licence": BOE_LICENCE,
    },
]
SOURCE_BY_ID = {s["doc_id"]: s for s in SOURCES}
BOE_API = "https://www.boe.es/datosabiertos/api/legislacion-consolidada/id/{boe_id}/texto"
BOE_HTML = "https://www.boe.es/buscar/act.php?id={boe_id}"
SUPPORTED = {".xml", ".html", ".htm", ".pdf", ".txt", ".md"}


def corpus_path(source: dict) -> Path:
    ext = {"boe": ".xml", "pdf": ".pdf", "eurlex": ".html"}[source["kind"]]
    return CORPUS_DIR / f"{source['doc_id']}{ext}"


def _fetch(url: str, accept: str = "*/*", headers: dict | None = None) -> bytes:
    """GET with the standard library only, so `python3 index.py --download-only`
    works even outside the uv environment (e.g. a Mac where uv sync fails)."""
    import ssl
    import urllib.request

    try:
        import certifi

        context = ssl.create_default_context(cafile=certifi.where())
    except ImportError:
        context = ssl.create_default_context()
    request = urllib.request.Request(url, headers={"User-Agent": USER_AGENT, "Accept": accept, **(headers or {})})
    with urllib.request.urlopen(request, timeout=60, context=context) as response:
        return response.read()


def _looks_complete(content: bytes) -> bool:
    """Bot-protection pages and errors are tiny or have no article in them.
    A PDF's text is compressed, so for PDFs only the header and size are checked."""
    if content.startswith(b"%PDF"):
        return len(content) > 20_000
    text = content[:2_000_000].decode("utf-8", errors="ignore")
    return len(content) > 20_000 and ("Artículo" in text or "Art&iacute;culo" in text or "<bloque" in text)


def download_corpus() -> None:
    """Fetch every source into corpus/ unless a non-empty copy is already there."""
    CORPUS_DIR.mkdir(parents=True, exist_ok=True)
    for source in SOURCES:
        if any(f.stat().st_size > 0 for f in _existing(source)):
            continue
        path = corpus_path(source)
        log(f"Downloading {source['doc_id']} ...")
        attempts = []
        if source["kind"] == "boe":
            attempts = [(BOE_API.format(boe_id=source["boe_id"]), {"Accept": "application/xml"}, path),
                        (BOE_HTML.format(boe_id=source["boe_id"]), {"Accept": "text/html"}, path.with_suffix(".html"))]
        else:
            attempts = [(source["url"], {}, path)] + [(url, h, path) for url, h in source.get("mirrors", [])]
        for url, headers, target in attempts:
            try:
                content = _fetch(url, headers=headers)
            except Exception as error:  # noqa: BLE001 - try the next source
                log(f"  {url}: {error}")
                continue
            if not _looks_complete(content):
                log(f"  {url}: empty or incomplete answer ({len(content)} bytes)")
                continue
            target.write_bytes(content)
            log(f"  saved {target.name} ({len(content) / 1e3:.0f} kB)")
            break
        else:
            if not source.get("optional"):
                raise RuntimeError(f"Could not download {source['doc_id']}")
            log(f"  {source['doc_id']} skipped: no source answered. The index is built without it.")


def _existing(source: dict) -> list[Path]:
    return [CORPUS_DIR / f"{source['doc_id']}{ext}" for ext in (".xml", ".html", ".pdf")
            if (CORPUS_DIR / f"{source['doc_id']}{ext}").exists()]


def find_corpus_file(source: dict) -> Path | None:
    for path in _existing(source):
        if path.stat().st_size > 0:
            return path
    if source.get("optional"):
        return None
    raise FileNotFoundError(f"{source['doc_id']} is not in corpus/. Run index.py to download it.")


def available_sources() -> list[dict]:
    """Sources with a file in corpus/ (optional ones may be missing)."""
    return [s for s in SOURCES if find_corpus_file(s) is not None]


# ---------------------------------------------------------------- extraction
# Every extractor returns Blocks: the natural units of the document (an article,
# a CNMV question, a page) with where they sit. Chunking works on Blocks.

@dataclass
class Block:
    location: str                 # "Artículo 13", "Pregunta 4", "Página 3": what a citation names
    paragraphs: list[str]
    section: str = ""             # enclosing chapter / title, for context
    page: int = 0                 # PDF page, when there is one
    extra: dict = field(default_factory=dict)

    @property
    def text(self) -> str:
        return "\n".join(self.paragraphs)

    @property
    def words(self) -> int:
        return len(self.text.split())


def clean(text: str) -> str:
    """Unicode NFC, no soft hyphens or odd spaces, single spaces."""
    text = unicodedata.normalize("NFC", text)
    text = text.replace("­", "").replace(" ", " ").replace(" ", " ").replace("﻿", "")
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    return text.strip()


ARTICLE_RE = re.compile(
    r"^(Art[ií]culo\s+\d+(?:\s*(?:bis|ter|quater|quinquies|sexies))?|"
    r"Disposici[oó]n\s+(?:adicional|transitoria|derogatoria|final)(?:\s+[a-záéíóúñ]+)?(?:\s+[a-záéíóúñ]+)?|"
    r"Pre[aá]mbulo|Anexo(?:\s+[IVX\d]+)?)",
    re.IGNORECASE,
)


def _location_from_heading(heading: str) -> str:
    """'Artículo 13. Condiciones de la oferta.' -> 'Artículo 13'."""
    heading = clean(heading)
    match = ARTICLE_RE.match(heading)
    if not match:
        return heading.rstrip(".")[:60]
    loc = match.group(1)
    loc = re.sub(r"(?i)^art[ií]culo", "Artículo", loc)
    loc = re.sub(r"(?i)^disposici[oó]n", "Disposición", loc)
    loc = re.sub(r"(?i)^pre[aá]mbulo", "Preámbulo", loc)
    loc = re.sub(r"\s+", " ", loc)
    # "Disposición final primera. Título" may have captured the first word of the title
    return loc.rstrip(".").strip()


def extract_boe_xml(path: Path) -> list[Block]:
    """BOE open-data API: <bloque id tipo titulo><version ...><p class=...> per block.

    A block can carry several <version>s (its history); the last one is in force.
    'encabezado' blocks are chapter headings; we keep them as the section.
    Editorial notes (class nota_pie..., blockquotes) about amendments are dropped.
    """
    import xml.etree.ElementTree as ET

    def paragraphs(version) -> list[str]:
        out = []
        for child in version:
            tag = child.tag.split("}")[-1]
            if tag == "blockquote" or "nota" in (child.get("class") or ""):
                continue
            if tag == "p":
                text = clean("".join(child.itertext()))
                if text:
                    out.append(text)
            elif tag == "table":  # one line per row, cells joined
                for row in child.iter("tr"):
                    text = clean(" | ".join(clean("".join(cell.itertext())) for cell in row
                                            if cell.tag.split("}")[-1] in ("td", "th")))
                    if text.strip(" |"):
                        out.append(text)
            elif tag != "img":  # lists and other wrappers: recurse
                out.extend(paragraphs(child))
        return out

    root = ET.fromstring(path.read_bytes())
    blocks, section = [], ""
    for bloque in root.iter("bloque"):
        versions = bloque.findall("version")
        if not versions:
            continue
        tipo = (bloque.get("tipo") or "").lower()
        paras = paragraphs(versions[-1])
        if not paras:
            continue
        if tipo == "encabezado":
            section = clean(" ".join(paras))[:160]
            continue
        if tipo in ("firma", "nota_inicial"):
            continue
        title = bloque.get("titulo") or paras[0]
        location = "Preámbulo" if tipo == "preambulo" or title.startswith("[") else _location_from_heading(title)
        blocks.append(Block(location=location, paragraphs=paras, section=section))
    return blocks


def extract_boe_html(path: Path) -> list[Block]:
    """Consolidated BOE page (act.php): <div class="bloque"> with h4/h5 headings."""
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(path.read_bytes(), "html.parser")
    root = soup.find(id="textoxslt") or soup.body or soup
    blocks, section = [], ""
    for div in root.find_all("div", class_="bloque"):
        heading = div.find(["h4", "h5", "h3"])
        paras = []
        for p in div.find_all("p"):
            css = " ".join(p.get("class", []))
            if "nota" in css or "bloque" in css or p.find_parent("blockquote") is not None:
                continue
            text = clean(p.get_text(" "))
            if text:
                paras.append(text)
        head = clean(heading.get_text(" ")) if heading else ""
        if heading and "articulo" not in " ".join(heading.get("class", [])) and not ARTICLE_RE.match(head):
            section = clean(" ".join([head] + paras))[:160]
            continue
        if not paras and not head:
            continue
        location = _location_from_heading(head) if head else "Preámbulo"
        blocks.append(Block(location=location, paragraphs=([head] if head else []) + paras, section=section))
    return blocks


def extract_eurlex_html(path: Path) -> list[Block]:
    """EUR-Lex OJ HTML: 'ti-art' / 'oj-ti-art' paragraphs start articles.

    Enumerations sit in tables ('a)' in one cell, text in the next), so each
    table row becomes one line. Recitals before Article 1 become 'Considerandos'.
    """
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(path.read_bytes(), "html.parser")
    body = soup.find(id="document1") or soup.body or soup
    blocks: list[Block] = []
    current = Block(location="Considerandos", paragraphs=[])
    for el in body.find_all(["p", "tr"]):
        if el.name == "p" and el.find_parent("tr") is not None:
            continue  # handled with its row
        css = " ".join(el.get("class", [])) if el.name == "p" else ""
        text = clean(el.get_text(" ")) if el.name == "p" else clean(
            " ".join(c.get_text(" ") for c in el.find_all(["td", "th"], recursive=False))
        )
        if not text:
            continue
        if re.search(r"(^|\s)(oj-)?ti-art(\s|$)", css) and re.match(r"Art[ií]culo\s+\d+", text):
            if current.paragraphs:
                blocks.append(current)
            current = Block(location=_location_from_heading(text), paragraphs=[text])
        elif re.search(r"(^|\s)(oj-)?ti-section", css):
            current.section = text
        else:
            current.paragraphs.append(text)
    if current.paragraphs:
        blocks.append(current)
    # Drop the EUR-Lex page chrome before the title, keep the recitals.
    return [b for b in blocks if b.words > 0]


def _pdf_pages(path: Path) -> list[str]:
    from pypdf import PdfReader

    return [page.extract_text() or "" for page in PdfReader(str(path)).pages]


def _strip_running_lines(pages: list[str]) -> list[list[str]]:
    """Remove running headers/footers: lines (digits ignored) on most pages.

    The CNMV Q&A repeats its title plus a page number at the top of every page;
    left in, it would land in the middle of answers and pollute every chunk.
    """
    split = [[clean(line) for line in page.splitlines() if clean(line)] for page in pages]
    if len(split) < 3:
        return split
    key = lambda line: re.sub(r"\d+", "#", line.lower())  # noqa: E731
    counts: dict[str, int] = {}
    for lines in split:
        for k in {key(line) for line in lines}:
            counts[k] = counts.get(k, 0) + 1
    running = {k for k, c in counts.items() if c >= max(3, 0.5 * len(split))}
    return [[line for line in lines if key(line) not in running and not re.fullmatch(r"\d{1,3}", line)]
            for lines in split]


def _join_lines(lines: list[str]) -> list[str]:
    """PDF lines -> paragraphs: mend hyphenated line breaks, join wrapped lines."""
    paras, buf = [], ""
    for line in lines:
        if buf.endswith("-") and line[:1].islower():
            buf = buf[:-1] + line
        elif buf and (buf.endswith((".", ":", "?", ";")) or re.match(r"^([a-z]\)|\d+\.|[-•·])\s", line)):
            paras.append(buf)
            buf = line
        else:
            buf = f"{buf} {line}".strip()
    if buf:
        paras.append(buf)
    return paras


def _mend_split_words(paragraphs: list[str]) -> list[str]:
    """PDF kerning sometimes splits a word ('art ículo', 'so ciedad', 'o ferente').
    Join two tokens when the joined word appears unsplit elsewhere in the
    document and one half never appears except in this very pair."""
    from collections import Counter

    text = " ".join(paragraphs)
    vocab = Counter(w.lower() for w in re.findall(r"\w+", text))
    pair_re = r"\b(\w+) (?=(\w+)\b)"  # lookahead: overlapping pairs
    pairs = Counter((m.group(1).lower(), m.group(2).lower()) for m in re.finditer(pair_re, text))

    def join(match: re.Match) -> str:
        a, b = match.group(1).lower(), match.group(2).lower()
        n = pairs[(a, b)]
        if vocab[a + b] and (vocab[b] == n or vocab[a] == n):
            return match.group(1)  # drop the space
        return match.group(0)

    return [re.sub(pair_re, join, para) for para in paragraphs]


def _question_starts(lines: list[tuple[int, str]]) -> list[tuple[int, int]]:
    """(line index, number) of the lines that open question 1, 2, 3... in order.

    A question opens with its number ('12. Tras la presentación de una opa,
    ¿es posible...') and has a '?' within the next few lines. Requiring the
    numbers in sequence keeps numbered lists inside answers ('1. Quien no
    vaya a alcanzar...') from being taken as questions.
    """
    starts, expected = [], 1
    for i, (_, line) in enumerate(lines):
        match = re.match(r"^(\d{1,2})\.\s+\S", line)
        if match and int(match.group(1)) in (expected, expected + 1):  # tolerate one missed number
            window = " ".join(text for _, text in lines[i:i + 16])
            if "?" in window[:1500]:
                starts.append((i, int(match.group(1))))
                expected = int(match.group(1)) + 1
    return starts


def extract_pdf(path: Path) -> list[Block]:
    """PDF: one Block per numbered question if it is a Q&A document, else per page."""
    pages = _strip_running_lines(_pdf_pages(path))
    lines = [(page_no, line) for page_no, page in enumerate(pages, 1) for line in page]
    starts = _question_starts(lines)
    blocks: list[Block] = []
    if len(starts) >= 3:
        bounds = [0] + [i for i, _ in starts] + [len(lines)]
        names = ["Introducción"] + [f"Pregunta {n}" for _, n in starts]
        for location, a, b in zip(names, bounds, bounds[1:]):
            if a == b:
                continue
            paras = _join_lines([text for _, text in lines[a:b]])
            blocks.append(Block(location=location, paragraphs=paras, page=lines[a][0]))
    else:
        for page_no, page in enumerate(pages, 1):
            paras = _join_lines(page)
            if paras:
                blocks.append(Block(location=f"Página {page_no}", paragraphs=paras, page=page_no))
    mended = _mend_split_words([p for b in blocks for p in b.paragraphs])
    i = 0
    for b in blocks:
        b.paragraphs, i = mended[i:i + len(b.paragraphs)], i + len(b.paragraphs)
    return [b for b in blocks if b.paragraphs]


def extract_text_file(path: Path) -> list[Block]:
    """Plain text / markdown: markdown headings or article headings start blocks."""
    blocks, current = [], Block(location="Inicio", paragraphs=[])
    for raw in path.read_text(encoding="utf-8", errors="replace").split("\n\n"):
        para = clean(raw.replace("\n", " "))
        if not para:
            continue
        heading = re.match(r"^#+\s*(.+)$", para)
        if heading or ARTICLE_RE.match(para):
            if current.paragraphs:
                blocks.append(current)
            title = heading.group(1) if heading else para
            current = Block(location=_location_from_heading(title), paragraphs=[] if heading else [para])
        else:
            current.paragraphs.append(para)
    if current.paragraphs:
        blocks.append(current)
    return blocks


def extract_html(path: Path) -> list[Block]:
    head = path.read_bytes()[:400_000].decode("utf-8", errors="ignore")
    if "ti-art" in head or "eur-lex" in head.lower():
        return extract_eurlex_html(path)
    if 'class="bloque"' in head:
        return extract_boe_html(path)
    from bs4 import BeautifulSoup  # generic page: headings start blocks

    soup = BeautifulSoup(head, "html.parser")
    blocks, current = [], Block(location="Inicio", paragraphs=[])
    for el in (soup.body or soup).find_all(["h1", "h2", "h3", "h4", "p", "li"]):
        text = clean(el.get_text(" "))
        if not text:
            continue
        if el.name.startswith("h"):
            if current.paragraphs:
                blocks.append(current)
            current = Block(location=_location_from_heading(text), paragraphs=[text])
        else:
            current.paragraphs.append(text)
    if current.paragraphs:
        blocks.append(current)
    return blocks


def extract(path: Path) -> list[Block]:
    suffix = path.suffix.lower()
    if suffix == ".xml":
        return extract_boe_xml(path)
    if suffix in (".html", ".htm"):
        return extract_html(path)
    if suffix == ".pdf":
        return extract_pdf(path)
    if suffix in (".txt", ".md"):
        return extract_text_file(path)
    raise ValueError(f"Unsupported file type {suffix!r}. Supported: {', '.join(sorted(SUPPORTED))}")


# ---------------------------------------------------------------- chunking

def doc_meta(path: Path, doc_id: str | None = None, title: str | None = None) -> dict:
    """Source metadata for a file: from SOURCES if it is a corpus file, else from its name."""
    doc_id = doc_id or path.stem
    source = SOURCE_BY_ID.get(doc_id)
    if source:
        return {"doc_id": doc_id, "doc_title": source["title"], "short": source["short"], "url": source["url"]}
    slug = re.sub(r"[^A-Za-z0-9]+", "-", doc_id).strip("-").upper()[:40] or "DOC"
    return {"doc_id": slug, "doc_title": title or path.stem, "short": title or path.stem, "url": str(path)}


def _split_long(paragraphs: list[str], max_words: int) -> list[list[str]]:
    """Greedy split of a long block on paragraph boundaries (sentences if one paragraph is too long)."""
    pieces: list[str] = []
    for para in paragraphs:
        if len(para.split()) <= max_words:
            pieces.append(para)
            continue
        sentences, buf = re.split(r"(?<=[.;:])\s+", para), ""
        for sentence in sentences:
            if buf and len((buf + " " + sentence).split()) > max_words:
                pieces.append(buf)
                buf = sentence
            else:
                buf = f"{buf} {sentence}".strip()
        if buf:
            pieces.append(buf)
    parts, current = [], []
    for piece in pieces:
        if current and len(" ".join(current + [piece]).split()) > max_words:
            parts.append(current)
            current = []
        current.append(piece)
    if current:
        parts.append(current)
    return parts


def chunk_blocks(blocks: list[Block], meta: dict, design: str) -> list[dict]:
    params = DESIGNS[design]
    chunks: list[dict] = []

    def add(text: str, location: str, locations: list[str], section: str, page: int, part: str = "") -> None:
        chunks.append({
            "text": text,
            "doc_id": meta["doc_id"],
            "doc_title": meta["doc_title"],
            "url": meta["url"],
            "location": location,
            "locations": "|".join(dict.fromkeys(locations)),
            "section": section,
            "page": page,
            "part": part,
            "design": design,
            "order": len(chunks),
            "words": len(text.split()),
        })

    if design == "fixed":
        # One stream of words, cut every `words` with `overlap`; structure is ignored
        # except to record which articles each window touches.
        stream = [(w, b.location, b.page, b.section) for b in blocks for w in b.text.split()]
        size, step = params["words"], params["words"] - params["overlap"]
        for start in range(0, max(len(stream) - params["overlap"], 1), step):
            window = stream[start:start + size]
            if not window:
                break
            locs = list(dict.fromkeys(w[1] for w in window))
            location = locs[0] if len(locs) == 1 else f"{locs[0]} a {locs[-1]}"
            add(" ".join(w[0] for w in window), location, locs, window[0][3], window[0][2])
    elif design == "struct":
        # One chunk per article / question, with the document and chapter as a
        # header so the chunk makes sense on its own. Long blocks are split on
        # paragraph boundaries and every part repeats the article heading.
        for block in blocks:
            if block.words < params["min_words"]:
                continue
            header = meta["short"] + (f" · {block.section}" if block.section else "")
            parts = _split_long(block.paragraphs, params["max_words"])
            for i, paras in enumerate(parts, 1):
                body = "\n".join(paras)
                if i > 1 and not body.startswith(block.paragraphs[0][:40]):
                    body = f"{block.paragraphs[0][:120]} (continuación)\n{body}"
                part = f"{i}/{len(parts)}" if len(parts) > 1 else ""
                add(f"{header}\n{body}", block.location, [block.location], block.section, block.page, part)
    else:
        raise ValueError(f"Unknown design {design!r}; choose from {list(DESIGNS)}")

    # Content-addressed ids: unchanged chunks keep their id (and saved vector) across runs.
    seen: set[str] = set()
    for c in chunks:
        base = f"{meta['doc_id']}:{sha(design + c['location'] + c['part'] + c['text'])}"
        cid, n = base, 1
        while cid in seen:
            n += 1
            cid = f"{base}-{n}"
        seen.add(cid)
        c["id"] = cid
    return chunks


def chunk_file(path: Path | str, design: str = ACTIVE_DESIGN, doc_id: str | None = None,
               title: str | None = None) -> list[dict]:
    """Extract, clean and chunk one file. Every chunk carries its source and location."""
    path = Path(path)
    blocks = extract(path)
    if not blocks:
        raise ValueError(f"No text could be extracted from {path.name}.")
    return chunk_blocks(blocks, doc_meta(path, doc_id, title), design)


# ---------------------------------------------------------------- embedding and storage

METADATA_KEYS = ("doc_id", "doc_title", "url", "location", "locations", "section", "page", "part",
                 "design", "order", "words")


def embed_and_store(chunks: list[dict], design: str = ACTIVE_DESIGN) -> dict:
    """Embed the chunks that have no saved vector yet and add them to the design's collection.

    Saves after every batch, so an interruption keeps everything embedded so far.
    """
    col = rag.collection(design)
    ids = [c["id"] for c in chunks]
    existing: set[str] = set()
    for i in range(0, len(ids), 500):
        existing |= set(col.get(ids=ids[i:i + 500], include=[])["ids"])
    todo = [c for c in chunks if c["id"] not in existing]
    done = 0
    for i in range(0, len(todo), EMBED_BATCH):
        batch = todo[i:i + EMBED_BATCH]
        vectors = rag.embedder().embed([c["text"] for c in batch], "RETRIEVAL_DOCUMENT")
        col.add(
            ids=[c["id"] for c in batch],
            embeddings=vectors,
            documents=[c["text"] for c in batch],
            metadatas=[{k: c[k] for k in METADATA_KEYS} for c in batch],
        )
        done += len(batch)
        log(f"  [{design}] embedded {done}/{len(todo)}")
    return {"chunks": len(chunks), "embedded_now": done, "already_saved": len(existing)}


def remove_stale(doc_id: str, keep_ids: set[str], design: str) -> int:
    """Delete a document's chunks that are no longer produced (e.g. after a chunking change)."""
    col = rag.collection(design)
    old = col.get(where={"doc_id": doc_id}, include=[])["ids"]
    stale = [i for i in old if i not in keep_ids]
    if stale:
        col.delete(ids=stale)
    return len(stale)


def file_sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# ---------------------------------------------------------------- add one document

# DECISION (Jesús): what happens when a document is already indexed.
#   same content (same SHA-256)          -> nothing is re-embedded, the tool says so
#   same doc_id, different content       -> treated as a new version: old chunks replaced
DUPLICATE_POLICY = "skip_identical_replace_new_version"


def add_document(path: Path | str, design: str = ACTIVE_DESIGN, title: str | None = None) -> dict:
    """Run one file through the index pipeline and store it. Used by server.py."""
    path = Path(path).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"No file at {path}")
    if path.suffix.lower() not in SUPPORTED:
        raise ValueError(f"Unsupported file type {path.suffix!r}. Supported: {', '.join(sorted(SUPPORTED))}")
    digest = file_sha(path)
    registry = rag.load_registry()
    for doc_id, entry in registry.items():
        if entry.get("sha256") == digest and design in entry.get("designs", {}):
            return {"status": "already_indexed", "doc_id": doc_id, "chunks": entry["designs"][design],
                    "message": f"{path.name} is already indexed as {doc_id}; nothing was embedded."}
    chunks = chunk_file(path, design, title=title)
    doc_id = chunks[0]["doc_id"]
    previous = registry.get(doc_id)
    stats = embed_and_store(chunks, design)
    removed = remove_stale(doc_id, {c["id"] for c in chunks}, design)
    registry[doc_id] = {
        **(previous or {}),
        "title": chunks[0]["doc_title"],
        "source": str(path),
        "sha256": digest,
        "words": sum(len(b.text.split()) for b in extract(path)),
        "added_by": (previous or {}).get("added_by", "add_document"),
        "updated_at": dt.datetime.now(dt.timezone.utc).isoformat(timespec="seconds"),
        "designs": {**(previous or {}).get("designs", {}), design: len(chunks)},
    }
    rag.save_registry(registry)
    status = "new_version" if previous else "added"
    return {"status": status, "doc_id": doc_id, "title": chunks[0]["doc_title"], "chunks": len(chunks),
            "embedded_now": stats["embedded_now"], "replaced_chunks": removed}


# ---------------------------------------------------------------- build everything

def build(designs: list[str], dry_run: bool = False) -> None:
    download_corpus()
    registry = rag.load_registry()
    stats = []
    for source in SOURCES:
        if find_corpus_file(source) is None:
            log(f"{source['doc_id']}: not in corpus/, left out of the index")
    for source in available_sources():
        path = find_corpus_file(source)
        blocks = extract(path)
        words = sum(b.words for b in blocks)
        entry = registry.setdefault(source["doc_id"], {})
        entry.update({"title": source["title"], "source": source["url"], "licence": source["licence"],
                      "sha256": file_sha(path), "words": words, "added_by": "index"})
        entry.setdefault("designs", {})
        stats.append({"doc_id": source["doc_id"], "blocks": len(blocks), "words": words})
        log(f"{source['doc_id']}: {len(blocks)} blocks, {words:,} words")
    log(f"Corpus: {sum(s['words'] for s in stats):,} words in {len(stats)} documents")

    for design in designs:
        all_chunks = []
        for source in available_sources():
            chunks = chunk_file(find_corpus_file(source), design, doc_id=source["doc_id"])
            registry[source["doc_id"]]["designs"][design] = len(chunks)
            all_chunks.append((source, chunks))
            next(s for s in stats if s["doc_id"] == source["doc_id"])[f"chunks_{design}"] = len(chunks)
        total = sum(len(c) for _, c in all_chunks)
        log(f"[{design}] {total} chunks")
        if dry_run:
            continue
        for source, chunks in all_chunks:
            removed = remove_stale(source["doc_id"], {c["id"] for c in chunks}, design)
            result = embed_and_store(chunks, design)
            log(f"[{design}] {source['doc_id']}: {result} stale removed: {removed}")
            rag.save_registry(registry)

    INDEX_DIR.mkdir(exist_ok=True)
    (INDEX_DIR / "corpus_stats.json").write_text(json.dumps(stats, ensure_ascii=False, indent=2))
    rag.save_registry(registry)
    if rag._EMBEDDER is not None:  # noqa: SLF001 - only report if we embedded anything
        log(f"Embedding calls: {rag.embedder().calls}, texts embedded: {rag.embedder().texts}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build the index.")
    parser.add_argument("--design", choices=list(DESIGNS), action="append",
                        help="design(s) to build (default: all)")
    parser.add_argument("--dry-run", action="store_true", help="download and chunk only, no embeddings")
    parser.add_argument("--download-only", action="store_true", help="only fetch the documents into corpus/")
    args = parser.parse_args()
    if args.download_only:
        download_corpus()
        raise SystemExit(0)
    try:
        build(args.design or list(DESIGNS), dry_run=args.dry_run)
    except rag.QuotaExhausted as error:
        log(f"\n{error}")
        raise SystemExit(0)
