"""
Assignment 3: build the index (`main.py index`).

Parts so far:
  3b  download the corpus, extract the text of each PDF page and clean it.
  3c  split each document into sections (articles, annexes, provisions) and cut
      it into chunks, in two designs:
        A  fixed-size windows: 150 words, 30 of them shared with the previous chunk.
        B  one chunk per section; sections longer than 300 words are cut at
           numbered clauses ("1.", "a)") so no clause is split when avoidable.
  3d  embed every chunk with Gemini and store each vector as soon as it arrives
      (index/vectors.jsonl). A chunk that already has a current vector is never
      embedded again.

The functions work on ONE file at a time, because server.py's add-document tool
imports them to index new documents.
"""

import argparse
import base64
import collections
import hashlib
import json
import os
import re
import statistics
import time
from pathlib import Path

import httpx
import numpy as np
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"  # git-ignored: the code downloads it
INDEX_DIR = ROOT / "index"    # committed: chunks and vectors
CHUNKS_FILE = INDEX_DIR / "chunks.jsonl"
VECTORS_FILE = INDEX_DIR / "vectors.jsonl"

# ---- Chunking settings. Changing one means embedding everything again. ----
CHUNK_WORDS = 150        # design A: words per chunk
CHUNK_OVERLAP = 30       # design A: words shared with the previous chunk
MAX_SECTION_WORDS = 300  # design B: longest chunk before a section is cut
MIN_PIECE_WORDS = 40     # design B: a last piece shorter than this joins the previous one

# Estatuto de los Trabajadores: only these articles are kept. Rule: the articles that
# the convenio cites, plus the ones on pay, working time, holidays and termination.
ET_KEEP = [
    "Artículo 3", "Artículo 4", "Artículo 15", "Artículo 16", "Artículo 22",
    "Artículo 26", "Artículo 27", "Artículo 29", "Artículo 31", "Artículo 34",
    "Artículo 35", "Artículo 36", "Artículo 37", "Artículo 38", "Artículo 46",
    "Artículo 48", "Artículo 48 bis", "Artículo 49", "Artículo 50", "Artículo 52",
    "Artículo 53", "Artículo 54", "Artículo 55", "Artículo 56",
]

# The documents of the corpus. All come from the BOE, Spain's official gazette.
SOURCES = [
    {
        "id": "convenio",
        "file": "convenio_vidrio_ceramicas_extractivas_BOE-A-2026-9578.pdf",
        "title": "XXIII Convenio colectivo estatal de industrias extractivas, vidrio, "
                 "cerámicas y comercio exclusivista (2025-2027)",
        "short": "Convenio vidrio-cerámicas-extractivas 2025-2027",
        "url": "https://www.boe.es/boe/dias/2026/05/02/pdfs/BOE-A-2026-9578.pdf",
    },
    {
        "id": "smi",
        "file": "rd_126_2026_smi_BOE-A-2026-3815.pdf",
        "title": "Real Decreto 126/2026, salario mínimo interprofesional para 2026",
        "short": "Real Decreto 126/2026 (SMI 2026)",
        "url": "https://www.boe.es/buscar/pdf/2026/BOE-A-2026-3815-consolidado.pdf",
    },
    {
        "id": "estatuto",
        "file": "estatuto_trabajadores_BOE-A-2015-11430.pdf",
        "title": "Estatuto de los Trabajadores (RDL 2/2015), texto consolidado",
        "short": "Estatuto de los Trabajadores",
        "url": "https://www.boe.es/buscar/pdf/2015/BOE-A-2015-11430-consolidado.pdf",
        "keep": ET_KEEP,
    },
]

# Lines starting like this are structure, never noise, even if they repeat.
STRUCTURE = re.compile(r"^(Artículo|ANEXO|Anexo|Disposición|CAPÍTULO|TÍTULO)\b")

# The BOE's publisher line appears once, on the last page, so the repeated-line
# detector cannot see it.
PUBLISHER_LINE = re.compile(r"ISSN: \d{4}-\d{3}[\dX]")


# =============================== 3b: download, extract, clean ===============================

def download_corpus() -> dict[str, Path]:
    """Download every source PDF that is not already in corpus/."""
    CORPUS_DIR.mkdir(exist_ok=True)
    paths = {}
    for src in SOURCES:
        dest = CORPUS_DIR / src["file"]
        if dest.exists():
            print(f"  already there: {dest.name}")
        else:
            print(f"  downloading:   {dest.name}")
            response = httpx.get(src["url"], follow_redirects=True, timeout=120)
            response.raise_for_status()
            if not response.content.startswith(b"%PDF"):
                raise RuntimeError(f"{src['url']} did not return a PDF")
            dest.write_bytes(response.content)
        paths[src["id"]] = dest
    return paths


def extract_pages(path: Path) -> list[str]:
    """Raw text of each page of a PDF (page 1 is the first item)."""
    return [page.extract_text() or "" for page in PdfReader(path).pages]


def _pattern(line: str) -> str:
    """A line with numbers masked and spaces collapsed, so 'Pág. 61075' and 'Pág.  61076' match."""
    return re.sub(r"\s+", " ", re.sub(r"\d+", "#", line)).strip()


def clean_pages(pages: list[str]) -> list[str]:
    """Remove page headers and footers; tidy spaces. Keeps one string per page.

    A header or footer is a line (numbers masked) that appears on at least 40%
    of the pages, e.g. 'BOLETÍN OFICIAL DEL ESTADO' or 'Página 12'. Documents
    with fewer than 4 pages are too short to tell, so they are left as they are.
    """
    noise = set()
    if len(pages) >= 4:
        counts = collections.Counter()
        for text in pages:
            counts.update({_pattern(line) for line in text.splitlines() if line.strip()})
        noise = {pattern for pattern, k in counts.items() if k >= 0.4 * len(pages)}

    cleaned = []
    for text in pages:
        lines = []
        for line in text.splitlines():
            line = re.sub(r"[ \t ]+", " ", line).strip()
            if not line:
                continue
            if PUBLISHER_LINE.search(line):
                continue
            if _pattern(line) in noise and not STRUCTURE.match(line):
                continue
            lines.append(line)
        cleaned.append("\n".join(lines))
    return cleaned


def load_clean_pages(path: Path) -> list[str]:
    """Extract and clean one PDF. The per-file entry point of part 3b."""
    return clean_pages(extract_pages(path))


def count_words(pages: list[str]) -> int:
    return sum(len(text.split()) for text in pages)


# =============================== 3c: sections ===============================

ARTICLE = re.compile(r"^Artículo (\d+)(?: (bis|ter|quater))?\s*\.")
ANNEX = re.compile(r"^ANEXO ([IVXLC]+)\b")
PROVISION = re.compile(r"^(Disposición [^\W\d_]+(?: [^\W\d_]+)?)\s*\.")
# Headings of a part of the document ("CAPÍTULO II", "Sección 3.ª ..."), which belong
# to no article. Their title lines follow, up to the next article.
PART_HEADING = re.compile(r"^(?:(?:TÍTULO|CAPÍTULO) [IVXLC]+\b|Sección \d+\.ª)")
DOT_LEADER = re.compile(r"\.{4,}|(?:\. ){4,}")
CLAUSE_START = re.compile(r"^(?:\d+\.\s|[a-z]\)\s|[-•]\s)")


def _heading(line: str):
    """(kind, label) if the line opens an article, annex or provision, else None."""
    m = ARTICLE.match(line)
    if m:
        return "article", f"Artículo {m.group(1)}" + (f" {m.group(2)}" if m.group(2) else "")
    m = ANNEX.match(line)
    if m:
        return "annex", f"Anexo {m.group(1)}"
    m = PROVISION.match(line)
    if m:
        return "provision", m.group(1)
    return None


def _drop_table_of_contents(lines: list[tuple[int, str]]) -> list[tuple[int, str]]:
    """Decree and Estatuto open with an ÍNDICE whose lines look like headings: drop it."""
    start = next((i for i, (page, line) in enumerate(lines)
                  if page <= 2 and line.strip().upper() == "ÍNDICE"), None)
    if start is None:
        return lines
    leaders = [i for i, (page, line) in enumerate(lines) if page <= 12 and DOT_LEADER.search(line)]
    if not leaders:
        return lines
    return lines[:start] + lines[max(leaders) + 1:]


def split_sections(path: Path, source: dict) -> list[dict]:
    """Split one PDF into sections: {label, kind, lines: [(page, text)], words, pages}.

    Text before the first heading is the 'Preliminar' section. If the source has a
    'keep' list, only the sections with those labels are returned.
    """
    lines = [(page, line)
             for page, text in enumerate(load_clean_pages(path), 1)
             for line in text.splitlines()]
    lines = _drop_table_of_contents(lines)

    sections, current, skipping = [], None, False
    for page, line in lines:
        heading = _heading(line)
        if heading:
            current = {"kind": heading[0], "label": heading[1], "lines": [(page, line)]}
            sections.append(current)
            skipping = False
            continue
        if current is None:
            current = {"kind": "preliminar", "label": "Preliminar", "lines": []}
            sections.append(current)
        if current["kind"] != "annex" and PART_HEADING.match(line):
            skipping = True
        if not skipping:
            current["lines"].append((page, line))

    keep = source.get("keep")
    result = []
    for section in sections:
        if not section["lines"] or (keep and section["label"] not in keep):
            continue
        section["words"] = sum(len(line.split()) for _, line in section["lines"])
        section["pages"] = sorted({page for page, _ in section["lines"]})
        result.append(section)
    return result


# =============================== 3c: chunks ===============================

def _page_range(pages) -> str:
    low, high = min(pages), max(pages)
    return str(low) if low == high else f"{low}-{high}"


def _make_chunk(design: str, source: dict, n: int, text: str, labels: list[str],
                pages, part: tuple[int, int] | None = None) -> dict:
    """One chunk. The embedded text starts with a header: document, location, part."""
    shown = "; ".join(labels) if len(labels) <= 3 else f"{labels[0]} … {labels[-1]}"
    header = f"{source['short']} | {shown}"
    if part and part[1] > 1:
        header += f" (parte {part[0]}/{part[1]})"
    return {
        "chunk_id": f"{design}-{source['id']}-{n:04d}",
        "design": design,
        "source": source["id"],
        "source_title": source["title"],
        "location": "; ".join(labels),
        "locations": labels,
        "pages": _page_range(pages),
        "words": len(text.split()),
        "text": f"{header}\n{text}",
    }


def _render(tokens) -> str:
    """Words back to text, keeping the original line breaks (tables need them)."""
    out = []
    for word, ends_line, *_ in tokens:
        out.append(word)
        out.append("\n" if ends_line else " ")
    return "".join(out).strip()


def chunks_fixed(sections: list[dict], source: dict) -> list[dict]:
    """Design A: windows of CHUNK_WORDS words, CHUNK_OVERLAP shared with the previous.

    The document is read as one stream of words (headings included). A window may
    cross from one article into the next; its metadata lists every article it touches.
    """
    tokens = []  # (word, ends_line, page, label)
    for section in sections:
        for page, line in section["lines"]:
            words = line.split()
            for k, word in enumerate(words):
                tokens.append((word, k == len(words) - 1, page, section["label"]))

    chunks, start, total = [], 0, len(tokens)
    while start < total:
        end = min(start + CHUNK_WORDS, total)
        if total - end < CHUNK_OVERLAP:  # a tail this short joins the last window
            end = total
        window = tokens[start:end]
        labels = list(dict.fromkeys(t[3] for t in window))
        chunks.append(_make_chunk("A", source, len(chunks) + 1, _render(window), labels,
                                  {t[2] for t in window}))
        if end == total:
            break
        start = end - CHUNK_OVERLAP
    return chunks


def _cut_section(lines: list[tuple[int, str]]) -> list[list[tuple[int, str]]]:
    """Cut a section into pieces of at most MAX_SECTION_WORDS, before a clause if possible."""
    blocks = []
    for item in lines:
        if not blocks or CLAUSE_START.match(item[1]):
            blocks.append([item])
        else:
            blocks[-1].append(item)

    def words(block):
        return sum(len(line.split()) for _, line in block)

    pieces, current, current_words = [], [], 0
    for block in blocks:
        block_words = words(block)
        if block_words > MAX_SECTION_WORDS:
            # One clause longer than the limit: fill the current piece, cut by lines.
            for item in block:
                line_words = len(item[1].split())
                if current and current_words + line_words > MAX_SECTION_WORDS:
                    pieces.append(current)
                    current, current_words = [], 0
                current.append(item)
                current_words += line_words
        else:
            if current and current_words + block_words > MAX_SECTION_WORDS:
                pieces.append(current)
                current, current_words = [], 0
            current.extend(block)
            current_words += block_words
    if current:
        pieces.append(current)
    if len(pieces) > 1 and words(pieces[-1]) < MIN_PIECE_WORDS:
        pieces[-2].extend(pieces.pop())
    return pieces


def chunks_by_section(sections: list[dict], source: dict) -> list[dict]:
    """Design B: one chunk per section; long sections cut at clauses, header on every piece."""
    chunks = []
    for section in sections:
        pieces = _cut_section(section["lines"])
        for k, piece in enumerate(pieces, 1):
            text = "\n".join(line for _, line in piece)
            chunks.append(_make_chunk("B", source, len(chunks) + 1, text, [section["label"]],
                                      {page for page, _ in piece}, (k, len(pieces))))
    return chunks


def source_for(path: Path) -> dict:
    """The SOURCES entry of a corpus file; any other file gets a generic one."""
    for src in SOURCES:
        if src["file"] == Path(path).name:
            return src
    stem = Path(path).stem
    return {"id": re.sub(r"\W+", "-", stem.lower()).strip("-")[:40], "title": stem, "short": stem}


def chunk_file(path: Path, design: str, source: dict | None = None) -> list[dict]:
    """Chunk ONE PDF with design 'A' or 'B'. Used by main() and by server.py's add_document."""
    source = source or source_for(path)
    sections = split_sections(Path(path), source)
    if design == "A":
        return chunks_fixed(sections, source)
    if design == "B":
        return chunks_by_section(sections, source)
    raise ValueError("design must be 'A' or 'B'")


def save_chunks(chunks: list[dict]) -> Path:
    INDEX_DIR.mkdir(exist_ok=True)
    out = CHUNKS_FILE
    with out.open("w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")
    return out


def describe(chunks: list[dict]) -> str:
    words = [c["words"] for c in chunks]
    return (f"{len(chunks):>4} chunks | words per chunk: min {min(words)}, "
            f"median {int(statistics.median(words))}, max {max(words)}")


# =============================== 3d: embeddings ===============================

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 3072                    # the model's full size; shorter vectors can be cut from these
EMBED_BATCH = 8                     # texts per request, so one request stays far under the token limit
RETRY_WAITS = (15, 30, 60, 60, 60)  # seconds to wait after each temporary error


class EmbeddingStopped(RuntimeError):
    """Gemini keeps refusing (daily limit, no network). Vectors saved so far are kept."""


def document_input(chunk: dict) -> str:
    """The text Gemini embeds for a chunk.

    gemini-embedding-2 reads the task from the text itself, not from a task_type
    setting: documents are 'title: ... | text: ...' and questions use query_input().
    """
    header, _, body = chunk["text"].partition("\n")
    return f"title: {header.replace(' | ', ' - ')} | text: {body}"


def query_input(question: str) -> str:
    return f"task: question answering | query: {question}"


def make_client():
    from google import genai
    from api_key import load_api_key
    return genai.Client(api_key=load_api_key())


def _call(client, texts: list[str]) -> list[list[float]]:
    """One embedding request, retried while the error is temporary."""
    from google.genai import types

    for attempt in range(len(RETRY_WAITS) + 1):
        try:
            response = client.models.embed_content(
                model=EMBED_MODEL,
                contents=texts,
                config=types.EmbedContentConfig(output_dimensionality=EMBED_DIM),
            )
            return [list(e.values) for e in response.embeddings]
        except Exception as error:  # noqa: BLE001 - decided below
            code = getattr(error, "code", None)
            temporary = code in (429, 500, 502, 503, 504) or isinstance(error, httpx.TransportError)
            if not temporary:
                raise
            if "perday" in str(error).lower().replace(" ", ""):
                raise EmbeddingStopped(
                    "the daily embedding limit is used up. Run the same command after "
                    "09:00 (Spain); nothing already embedded is lost."
                ) from error
            if attempt == len(RETRY_WAITS):
                raise EmbeddingStopped(
                    f"Gemini kept failing ({code or type(error).__name__}). Run the same "
                    f"command again in a few minutes; nothing already embedded is lost."
                ) from error
            wait = RETRY_WAITS[attempt]
            print(f"    temporary error ({code or type(error).__name__}), waiting {wait}s ...", flush=True)
            time.sleep(wait)


def _embed_batch(client, texts: list[str]) -> list[list[float]]:
    """One vector per text. If a batch comes back merged or is refused, go text by text."""
    try:
        vectors = _call(client, texts)
        if len(vectors) == len(texts):
            return vectors
    except EmbeddingStopped:
        raise
    except Exception:  # noqa: BLE001 - e.g. a batch the API refuses: try single texts
        if len(texts) == 1:
            raise
    return [_call(client, [text])[0] for text in texts]


def _unit(vector) -> np.ndarray:
    v = np.asarray(vector, dtype=np.float32)
    return v / np.linalg.norm(v)


def embed_texts(texts: list[str], client=None) -> np.ndarray:
    """Unit-length vectors for texts (one row each). Not saved anywhere."""
    client = client or make_client()
    rows = []
    for i in range(0, len(texts), EMBED_BATCH):
        rows += [_unit(v) for v in _embed_batch(client, texts[i:i + EMBED_BATCH])]
    return np.vstack(rows) if rows else np.zeros((0, EMBED_DIM), np.float32)


def embed_query(question: str, client=None) -> np.ndarray:
    """The vector of one question, built the same way for search and evaluation."""
    return embed_texts([query_input(question)], client)[0]


def vector_key(text: str) -> str:
    """Identifies what a vector was made from, so a changed chunk is never matched to an old vector."""
    return hashlib.sha1(f"{EMBED_MODEL}|{EMBED_DIM}|{text}".encode("utf-8")).hexdigest()[:16]


def _encode(vector: np.ndarray) -> str:
    return base64.b64encode(vector.astype("<f4").tobytes()).decode("ascii")


def _decode(text: str) -> np.ndarray:
    return np.frombuffer(base64.b64decode(text), dtype="<f4")


def load_vectors() -> dict[str, tuple[str, str]]:
    """chunk_id -> (key, encoded vector), from index/vectors.jsonl (the last line of an id wins)."""
    stored = {}
    if VECTORS_FILE.exists():
        with VECTORS_FILE.open(encoding="utf-8") as f:
            for line in f:
                try:
                    record = json.loads(line)
                    stored[record["chunk_id"]] = (record["key"], record["vector"])
                except (json.JSONDecodeError, KeyError):
                    continue  # a half-written last line after a crash
    return stored


def embed_and_store(chunks: list[dict], limit: int | None = None, client=None) -> dict:
    """Embed the chunks that have no current vector; append each batch to disk at once.

    limit: embed at most this many (to test with a few). Returns counts and, if
    Gemini stopped us, the reason in 'stopped'.
    """
    stored = load_vectors()
    missing = [c for c in chunks
               if stored.get(c["chunk_id"], (None, None))[0] != vector_key(document_input(c))]
    todo = missing[:limit] if limit is not None else missing
    stats = {"chunks": len(chunks), "already_done": len(chunks) - len(missing),
             "embedded": 0, "remaining": len(missing), "stopped": None}
    if not todo:
        return stats

    print(f"  {len(todo)} texts to embed now ({stats['already_done']} already have a vector; "
          f"the free tier allows about 1,000 a day)")
    client = client or make_client()
    INDEX_DIR.mkdir(exist_ok=True)
    with VECTORS_FILE.open("a", encoding="utf-8") as f:
        if f.tell() > 0 and not VECTORS_FILE.read_bytes().endswith(b"\n"):
            f.write("\n")  # a crash left half a line: start on a fresh one
        for i in range(0, len(todo), EMBED_BATCH):
            batch = todo[i:i + EMBED_BATCH]
            texts = [document_input(c) for c in batch]
            try:
                vectors = _embed_batch(client, texts)
            except EmbeddingStopped as error:
                stats["stopped"] = str(error)
                break
            if stats["embedded"] == 0:
                print(f"  first vector: {len(vectors[0])} numbers, length before normalising "
                      f"{float(np.linalg.norm(vectors[0])):.3f}")
            for chunk, text, vector in zip(batch, texts, vectors):
                if len(vector) != EMBED_DIM:
                    raise ValueError(f"expected {EMBED_DIM} numbers per vector, got {len(vector)}")
                f.write(json.dumps({"chunk_id": chunk["chunk_id"], "key": vector_key(text),
                                    "vector": _encode(_unit(vector))}) + "\n")
            f.flush()
            os.fsync(f.fileno())
            stats["embedded"] += len(batch)
            if (i // EMBED_BATCH) % 10 == 9 or stats["embedded"] == len(todo):
                print(f"    embedded {stats['embedded']}/{len(todo)}", flush=True)
    stats["remaining"] = len(missing) - stats["embedded"]
    return stats


def load_index(design: str | None = None) -> tuple[list[dict], np.ndarray]:
    """(chunks, matrix): every chunk that has a current vector, and its unit vectors as rows."""
    chunks = [json.loads(line) for line in CHUNKS_FILE.open(encoding="utf-8")]
    stored = load_vectors()
    kept, rows = [], []
    for chunk in chunks:
        if design and chunk["design"] != design:
            continue
        item = stored.get(chunk["chunk_id"])
        if item and item[0] == vector_key(document_input(chunk)):
            kept.append(chunk)
            rows.append(_decode(item[1]))
    matrix = np.vstack(rows) if rows else np.zeros((0, EMBED_DIM), np.float32)
    return kept, matrix


# =============================== main ===============================

def main(limit: int | None = None) -> None:
    print("1. Corpus")
    paths = download_corpus()

    print("\n2. Extract and clean")
    for src in SOURCES:
        raw = extract_pages(paths[src["id"]])
        clean = clean_pages(raw)
        print(f"  {src['id']:<9} {len(clean):>3} pages | words: {count_words(raw):>6} raw -> "
              f"{count_words(clean):>6} clean")

    print("\n3. Sections and chunks")
    all_chunks = []
    for src in SOURCES:
        sections = split_sections(paths[src["id"]], src)
        print(f"  {src['id']:<9} {len(sections):>3} sections, {sum(s['words'] for s in sections):>6} words kept")
        for design in ("A", "B"):
            chunks = chunk_file(paths[src["id"]], design, src)
            all_chunks += chunks
            print(f"      design {design}: {describe(chunks)}")
    for design in ("A", "B"):
        n = sum(1 for c in all_chunks if c["design"] == design)
        print(f"  total design {design}: {n} chunks")
    print(f"\n  chunks saved to {save_chunks(all_chunks).relative_to(ROOT)}")

    print("\n4. Embeddings")
    # Design B first: if a limit stops us, one design is complete.
    stats = embed_and_store(sorted(all_chunks, key=lambda c: c["design"] != "B"), limit=limit)
    size_mb = sum(p.stat().st_size for p in INDEX_DIR.rglob("*") if p.is_file()) / 1e6
    print(f"  embedded now: {stats['embedded']} | had a vector already: {stats['already_done']} | "
          f"still without: {stats['remaining']} | index/ is {size_mb:.1f} MB (limit 90)")
    if stats["stopped"]:
        raise SystemExit(f"\nStopped: {stats['stopped']}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Build the index: download, chunk, embed.")
    parser.add_argument("--limit", type=int, help="embed at most this many chunks (to test with a few)")
    main(parser.parse_args().limit)
