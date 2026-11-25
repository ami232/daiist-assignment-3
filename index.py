"""
Assignment 3: build the index (`main.py index`).

Corpus: three Spanish laws from the BOE (consolidated texts), used for a
tenant/landlord assistant. See REPORT.md for the use case and licence.

Two chunking designs are built so that evaluate.py can compare them:
  * "article": one chunk per article / disposition, split only when long
  * "fixed":   sliding window of FIXED_WORDS words, ignoring structure

Layout of index/ (all committed):
  manifest.json          corpus documents (source, URL, download date, hash), default design
  chunks_<design>.jsonl  one chunk per line: id, key, source, location, section, pages, text
  vectors.jsonl          append-only cache {key, vector}; key = sha256 of the embedded text

Vectors are saved after every batch and only chunks without a saved vector
are embedded, so a crash or the daily free-tier limit loses nothing.

server.py imports the per-file functions: chunk_file, embed_and_store,
register_chunks, file_sha256, load_manifest.
"""

import hashlib
import json
import re
import sys
import time
from datetime import date
from pathlib import Path

import httpx
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"          # git-ignored; re-downloaded when missing
INDEX_DIR = ROOT / "index"
MANIFEST = INDEX_DIR / "manifest.json"
VECTORS = INDEX_DIR / "vectors.jsonl"

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIMS = 768
EMBED_BATCH = 50
DESIGNS = ("article", "fixed")
DEFAULT_DESIGN = "article"            # evaluate.py reports the numbers; change after comparing
FIXED_WORDS, FIXED_OVERLAP = 220, 40
MAX_ARTICLE_WORDS = 320               # longer articles are split on paragraph boundaries

# BOE consolidated texts. Reuse is allowed with attribution, without altering the meaning,
# and mentioning the date of the last update (https://www.boe.es/informacion/aviso_legal).
DOCS = [
    {"source": "LAU", "title": "Ley 29/1994, de Arrendamientos Urbanos",
     "boe_id": "BOE-A-1994-26003", "year": 1994},
    {"source": "Ley12-2023", "title": "Ley 12/2023, por el derecho a la vivienda",
     "boe_id": "BOE-A-2023-12203", "year": 2023},
    {"source": "LPH", "title": "Ley 49/1960, sobre propiedad horizontal",
     "boe_id": "BOE-A-1960-10906", "year": 1960},
]


def boe_url(doc: dict) -> str:
    return f"https://www.boe.es/buscar/pdf/{doc['year']}/{doc['boe_id']}-consolidado.pdf"


# --------------------------------------------------------------------------- download

def file_sha256(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def download_corpus() -> list[dict]:
    """Download the PDFs into corpus/ when missing. Returns manifest entries."""
    CORPUS_DIR.mkdir(exist_ok=True)
    entries = []
    for doc in DOCS:
        path = CORPUS_DIR / f"{doc['source']}.pdf"
        if not path.exists():
            print(f"Downloading {doc['source']} ...", file=sys.stderr)
            response = httpx.get(boe_url(doc), follow_redirects=True, timeout=120)
            response.raise_for_status()
            path.write_bytes(response.content)
        entries.append({**doc, "url": boe_url(doc), "file": path.name,
                        "sha256": file_sha256(path), "downloaded": date.today().isoformat()})
    return entries


# --------------------------------------------------------------------------- extract + clean

NOISE = re.compile(
    r"^(LEGISLACIÓN CONSOLIDADA|BOLETÍN OFICIAL DEL ESTADO|Página \d+|"
    r"Este texto consolidado no tiene valor jurídico\.?|Más información en .*|"
    r"cve: .*|Verificable en .*)$", re.I)
TOC_LINE = re.compile(r"\.{4,}")
ORDINAL = (r"(?:primera|segunda|tercera|cuarta|quinta|sexta|séptima|octava|novena|décima|"
           r"undécima|duodécima|decim\w+|vigésim\w+|única)")
HEADING = re.compile(
    r"^(Artículo (?:\d+|[a-záéíóú]+)(?:\s(?:bis|ter|quater|quinquies))?|"   # "Artículo 9" or "Artículo primero"
    rf"Disposición (?:adicional|transitoria|derogatoria|final)(?:\s+{ORDINAL})?|"
    r"Preámbulo|PREÁMBULO|ANEXO(?: [IVX]+)?)\s*(?:\.|$)\s*(.*)$")
SECTION = re.compile(r"^(TÍTULO|CAPÍTULO|Título|Capítulo|SECCIÓN|Sección)\s+[IVXLC\w]+\b.*$")
PARAGRAPH_START = re.compile(r"^(\d+\.\s|[a-zñ]\)\s|[A-Z]\)\s|«|\d+\.º)")


def extract_lines(path: Path) -> list[tuple[int, str]]:
    """(page number, clean line) pairs from a PDF, without headers and footers."""
    reader = PdfReader(str(path))
    lines: list[tuple[int, str]] = []
    for number, page in enumerate(reader.pages, start=1):
        for raw in (page.extract_text() or "").splitlines():
            line = re.sub(r"\s+", " ", raw).strip()
            if line and not NOISE.match(line):
                lines.append((number, line))
    return lines


def drop_index(lines: list[tuple[int, str]]) -> list[tuple[int, str]]:
    """The BOE PDF starts with a table of contents whose lines end in dot leaders
    (long titles wrap onto lines without leaders). The real text starts after the
    last leader line of that initial run."""
    first = next((i for i, (_, l) in enumerate(lines) if TOC_LINE.search(l)), None)
    if first is None:
        return lines
    end, gap = first, 0
    for i in range(first, len(lines)):
        if TOC_LINE.search(lines[i][1]):
            end, gap = i, 0
        else:
            gap += 1
            if gap > 12:   # a run of normal text: the index is over
                break
    return lines[end + 1:]


# --------------------------------------------------------------------------- chunking

def words(text: str) -> int:
    return len(text.split())


def paragraphs(lines: list[tuple[int, str]]) -> list[tuple[int, str]]:
    """Join wrapped lines into paragraphs. Returns (page where it starts, text)."""
    out: list[tuple[int, str]] = []
    for page, line in lines:
        starts_new = PARAGRAPH_START.match(line) is not None
        if out and not starts_new:
            previous = out[-1][1]
            if not previous.endswith((".", ":", ";")) or line[:1].islower():
                out[-1] = (out[-1][0], previous + " " + line)
                continue
        out.append((page, line))
    return out


def make_chunk(doc: dict, location: str, section: str, pages: tuple[int, int],
               text: str, design: str, part: int = 1, parts: int = 1) -> dict:
    return {"design": design, "source": doc["source"], "title": doc["title"],
            "location": location, "section": section,
            "pages": f"{pages[0]}-{pages[1]}" if pages[0] != pages[1] else str(pages[0]),
            "part": f"{part}/{parts}", "text": text.strip()}


def chunk_by_article(doc: dict, lines: list[tuple[int, str]]) -> list[dict]:
    """One chunk per article/disposition, split on paragraphs when over MAX_ARTICLE_WORDS."""
    lines = drop_index(lines)
    blocks: list[dict] = []
    section = ""
    current = None
    for page, line in lines:
        if SECTION.match(line) and not TOC_LINE.search(line):
            section = line
            continue
        match = HEADING.match(line)
        if match and not TOC_LINE.search(line):
            name = re.sub(r"\s+", " ", match.group(1)).strip()
            if name.isupper():
                name = name.capitalize()
            current = {"location": name, "heading": match.group(2).strip(),
                       "section": section, "lines": [], "page": page}
            blocks.append(current)
            continue
        if current is None:  # text before the first heading
            current = {"location": "Preámbulo", "heading": "", "section": section, "lines": [], "page": page}
            blocks.append(current)
        current["lines"].append((page, line))

    chunks: list[dict] = []
    for block in blocks:
        paras = paragraphs(block["lines"])
        if not paras:
            continue
        title = f"{block['location']}. {block['heading']}".strip(" .") if block["heading"] else block["location"]
        pieces: list[list[tuple[int, str]]] = [[]]
        for para in paras:
            if pieces[-1] and sum(words(p[1]) for p in pieces[-1]) + words(para[1]) > MAX_ARTICLE_WORDS:
                pieces.append([])
            pieces[-1].append(para)
        for n, piece in enumerate(pieces, start=1):
            body = "\n".join(p[1] for p in piece)
            if words(body) < 8:
                continue
            last_page = block["lines"][-1][0] if n == len(pieces) else piece[-1][0]
            chunks.append(make_chunk(doc, block["location"], block["section"], (piece[0][0], last_page),
                                     f"{title}\n{body}", "article", n, len(pieces)))
    return chunks


def chunk_fixed(doc: dict, lines: list[tuple[int, str]]) -> list[dict]:
    """Sliding window of FIXED_WORDS words with FIXED_OVERLAP overlap; location is the page."""
    lines = drop_index(lines)
    tokens: list[tuple[str, int]] = [(w, page) for page, line in lines for w in line.split()]
    step = FIXED_WORDS - FIXED_OVERLAP
    chunks = []
    for start in range(0, max(len(tokens) - FIXED_OVERLAP, 1), step):
        window = tokens[start:start + FIXED_WORDS]
        if len(window) < 20:
            break
        first, last = window[0][1], window[-1][1]
        chunks.append(make_chunk(doc, f"pág. {first}", "", (first, last),
                                 " ".join(w for w, _ in window), "fixed"))
    return chunks


def doc_info(path: Path) -> dict:
    """Metadata for a file: a known corpus document, or a generic one for added files."""
    for doc in DOCS:
        if Path(path).stem == doc["source"]:
            return doc
    return {"source": Path(path).stem, "title": Path(path).stem.replace("_", " ")}


def read_lines(path: Path) -> list[tuple[int, str]]:
    path = Path(path)
    if path.suffix.lower() == ".pdf":
        return extract_lines(path)
    text = path.read_text(encoding="utf-8", errors="replace")
    return [(1, re.sub(r"\s+", " ", l).strip()) for l in text.splitlines() if l.strip()]


def embedding_text(chunk: dict) -> str:
    """Document format gemini-embedding-2 expects (it has no task_type parameter)."""
    return f"title: {chunk['title']} - {chunk['location']} | text: {chunk['text']}"


def finish(chunks: list[dict]) -> list[dict]:
    for n, chunk in enumerate(chunks):
        chunk["key"] = hashlib.sha256(embedding_text(chunk).encode()).hexdigest()
        chunk["id"] = f"{chunk['design']}:{chunk['source']}:{n:04d}"
    return chunks


def chunk_file(path: Path, design: str = DEFAULT_DESIGN, doc: dict | None = None) -> list[dict]:
    """Extract, clean and chunk one file. Used by this stage and by server.add_document."""
    path = Path(path)
    doc = doc or doc_info(path)
    lines = read_lines(path)
    if design == "fixed":
        return finish(chunk_fixed(doc, lines))
    chunks = chunk_by_article(doc, lines)
    structured = sum(1 for c in chunks if c["location"].startswith(("Artículo", "Disposición")))
    if structured < 3:   # an added file without article structure: fall back to windows
        chunks = chunk_fixed(doc, lines)
    return finish(chunks)


# --------------------------------------------------------------------------- embeddings

def load_vectors() -> dict[str, list[float]]:
    vectors: dict[str, list[float]] = {}
    if VECTORS.exists():
        with VECTORS.open(encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    row = json.loads(line)
                    vectors[row["key"]] = row["vector"]
    return vectors


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed document texts. Each text is its own Content, otherwise Gemini returns ONE vector."""
    from google import genai
    from google.genai import types
    from api_key import load_api_key

    client = genai.Client(api_key=load_api_key())
    contents = [types.Content(parts=[types.Part(text=t)]) for t in texts]
    response = client.models.embed_content(
        model=EMBED_MODEL, contents=contents,
        config=types.EmbedContentConfig(output_dimensionality=EMBED_DIMS))
    return [list(e.values) for e in response.embeddings]


def embed_and_store(chunks: list[dict]) -> int:
    """Embed the chunks that have no saved vector; append each batch to vectors.jsonl.

    Returns the number of new embeddings. Stops cleanly (progress saved) on quota errors.
    """
    INDEX_DIR.mkdir(exist_ok=True)
    have = load_vectors()
    pending = list({c["key"]: c for c in chunks if c["key"] not in have}.values())
    done = 0
    for start in range(0, len(pending), EMBED_BATCH):
        batch = pending[start:start + EMBED_BATCH]
        vectors = None
        for attempt in range(6):
            try:
                vectors = embed_texts([embedding_text(c) for c in batch])
                break
            except Exception as error:  # noqa: BLE001
                limited = "429" in str(error) or "RESOURCE_EXHAUSTED" in str(error)
                if not limited:
                    raise
                if "PerDay" in str(error) or "per day" in str(error).lower():
                    break   # daily quota: waiting will not help
                print(f"  per-minute rate limit, waiting 65s (attempt {attempt + 1}/6)", file=sys.stderr)
                time.sleep(65)
        if vectors is None:
            print(f"Quota reached after {done} new embeddings ({len(pending) - done} left). "
                  f"Progress is saved; run again after 09:00 (Spain).", file=sys.stderr)
            break
        with VECTORS.open("a", encoding="utf-8") as f:
            for chunk, vector in zip(batch, vectors):
                f.write(json.dumps({"key": chunk["key"], "vector": [round(x, 6) for x in vector]}) + "\n")
        done += len(batch)
        print(f"  embedded {done}/{len(pending)}", file=sys.stderr)
        time.sleep(1)
    return done


# --------------------------------------------------------------------------- files

def write_chunks(design: str, chunks: list[dict], append: bool = False) -> None:
    INDEX_DIR.mkdir(exist_ok=True)
    with (INDEX_DIR / f"chunks_{design}.jsonl").open("a" if append else "w", encoding="utf-8") as f:
        for chunk in chunks:
            f.write(json.dumps(chunk, ensure_ascii=False) + "\n")


def load_manifest() -> dict:
    if MANIFEST.exists():
        return json.loads(MANIFEST.read_text(encoding="utf-8"))
    return {"documents": [], "default_design": DEFAULT_DESIGN, "embed_model": EMBED_MODEL, "dims": EMBED_DIMS}


def save_manifest(manifest: dict) -> None:
    INDEX_DIR.mkdir(exist_ok=True)
    MANIFEST.write_text(json.dumps(manifest, ensure_ascii=False, indent=2), encoding="utf-8")


def register_chunks(entry: dict, design_chunks: dict[str, list[dict]]) -> None:
    """Record an added document and append its chunks to each design's file (add_document)."""
    manifest = load_manifest()
    manifest["documents"] = [d for d in manifest["documents"] if d["sha256"] != entry["sha256"]] + [entry]
    save_manifest(manifest)
    for design, chunks in design_chunks.items():
        write_chunks(design, chunks, append=True)


# --------------------------------------------------------------------------- main

def build_index(embed: bool = True) -> None:
    entries = download_corpus()
    manifest = load_manifest()
    manifest["documents"] = entries
    save_manifest(manifest)
    for design in DESIGNS:
        all_chunks: list[dict] = []
        for doc, entry in zip(DOCS, entries):
            chunks = chunk_file(CORPUS_DIR / entry["file"], design, doc)
            for chunk in chunks:
                chunk["downloaded"] = entry["downloaded"]
            all_chunks += chunks
        write_chunks(design, all_chunks)
        total = sum(words(c["text"]) for c in all_chunks)
        print(f"{design}: {len(all_chunks)} chunks, {total} words in chunks", file=sys.stderr)
        if embed:
            print(f"{design}: {embed_and_store(all_chunks)} new embeddings", file=sys.stderr)


if __name__ == "__main__":
    build_index(embed="--no-embed" not in sys.argv)
