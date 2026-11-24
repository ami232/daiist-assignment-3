"""
Assignment 3: build the index (`main.py index`).

1. Download each document into corpus/ (skipped if the file is already there).
2. Extract the text with pdfium and clean it (page headers, footers, amendment markers,
   the BOE table of contents, words split across lines).
3. Split it into its legal units (articles, annexes, pliego sections) so every chunk
   carries its source and location.
4. Chunk it two ways ("fixed" windows and "structure" units) for the comparison.
5. Embed with Gemini and store in ChromaDB under index/. Every batch is written as soon
   as it comes back, and only chunks without a saved vector are embedded, so a crash or
   the daily quota loses nothing: run it again and it carries on.

server.py's add_document tool imports chunk_file(), embed_and_store() and friends from here.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import time
from collections import deque
from pathlib import Path

import config

# ----------------------------------------------------------------------------------
# Logging: stderr only, because server.py imports this module and stdout carries MCP.
# ----------------------------------------------------------------------------------


def log(message: str) -> None:
    print(message, file=sys.stderr, flush=True)


# ----------------------------------------------------------------------------------
# 1. Download
# ----------------------------------------------------------------------------------

HEADERS = {
    "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/124.0 Safari/537.36",
    "Accept": "application/pdf,*/*",
}


def download(doc: dict) -> Path:
    """Return corpus/<id>.pdf, downloading it first if needed. Tries each URL in turn.

    EUR-Lex answers scripts with an empty HTTP 202 bot challenge, so the EU regulation
    is committed in corpus/ (its CC BY 4.0 licence allows it) and never needs downloading.
    """
    import httpx

    config.CORPUS_DIR.mkdir(exist_ok=True)
    path = config.CORPUS_DIR / f"{doc['id']}.pdf"
    if path.exists() and path.stat().st_size > 10_000:
        return path
    errors = []
    for url in doc["urls"]:
        try:
            response = httpx.get(url, headers=HEADERS, follow_redirects=True, timeout=90)
            if response.status_code == 200 and response.content[:4] == b"%PDF":
                path.write_bytes(response.content)
                log(f"  downloaded {doc['id']} from {url}")
                return path
            errors.append(f"{url} -> HTTP {response.status_code}")
        except httpx.HTTPError as error:
            errors.append(f"{url} -> {type(error).__name__}: {error}")
    raise RuntimeError(
        f"Could not download {doc['id']}:\n  " + "\n  ".join(errors)
        + f"\n  Save it by hand as {path} and run again."
    )


# ----------------------------------------------------------------------------------
# 2. Extract and clean
# ----------------------------------------------------------------------------------


def extract_pages(path: Path) -> list[str]:
    """Text of each page.

    pdfium, not pypdf: on the EUR-Lex PDF pypdf breaks words apart ("q ue", "letr a",
    "jun io") because of how the file positions its glyphs; pdfium keeps them whole.
    """
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix in {".txt", ".md"}:
        return [path.read_text(encoding="utf-8")]
    if suffix in {".html", ".htm"}:
        from bs4 import BeautifulSoup

        return [BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser").get_text("\n")]
    import pypdfium2 as pdfium

    pdf = pdfium.PdfDocument(str(path))
    try:
        return [pdf[i].get_textpage().get_text_range() for i in range(len(pdf))]
    finally:
        pdf.close()


# Lines that are layout, not content.
NOISE_LINE = [
    re.compile(r"^\d{5}[RL]\d{4} — [A-Z]{2} — .*$"),   # EUR-Lex running header "02019R0033 — ES — ..."
    re.compile(r"^LEGISLACIÓN CONSOLIDADA$"),            # BOE footer
    re.compile(r"^BOLETÍN OFICIAL DEL ESTADO$"),         # BOE running header
    re.compile(r"^Página \d+$"),                         # BOE footer
    re.compile(r"^_{4,}$"),                              # EUR-Lex: text deleted by an amendment
    re.compile(r"^\d{1,2}$"),                            # bare page numbers (pliego)
    re.compile(r"^Página \d+ de \d+$"),                  # "Página 10 de 29" (other pliegos)
    re.compile(r"^[A-Z]{3}-[A-Z]{2}-[A-Z]\d+$"),           # EU file number alone on a line, e.g. PDO-ES-A0626
]
MARKERS = re.compile(r"[▼►][A-Z]\d*|◄")                  # EUR-Lex amendment markers ▼M3 ►B ◄
TOC_LINE = re.compile(r"\.{4,}\s*\d+\s*$")               # BOE table of contents "Artículo 3 ....... 7"


def clean_pages(pages: list[str], kind: str) -> list[tuple[int, str]]:
    """(page number, line) pairs with layout noise removed."""
    lines: list[tuple[int, str]] = []
    for page_no, text in enumerate(pages, 1):
        # pdfium marks a word hyphenated at a line end with U+FFFE: join the halves.
        text = re.sub(r"[￾\xad]\s*\n\s*", "", text).replace("￾", "").replace("\xad", "")
        text = MARKERS.sub("", text).replace("\r", "")
        for raw in text.split("\n"):
            line = re.sub(r"\s+", " ", raw).strip()
            if not line or any(p.match(line) for p in NOISE_LINE):
                continue
            lines.append((page_no, line))

    if kind == "boe":
        # Drop the table of contents: everything before the "TEXTO CONSOLIDADO" banner.
        start = next((i for i, (_, l) in enumerate(lines) if l == "TEXTO CONSOLIDADO"), 0)
        lines = [(p, l) for p, l in lines[start:] if not TOC_LINE.search(l)]
        lines = [(p, l) for p, l in lines if l not in {"TEXTO CONSOLIDADO"} and not l.startswith("Última modificación:")]
    return lines


# ----------------------------------------------------------------------------------
# 3. Split into legal units, each with a location
# ----------------------------------------------------------------------------------

EU_ARTICLE = re.compile(r"^Artículo (\d+(?: bis| ter)?)$")
EU_ANNEX = re.compile(r"^ANEXO ([IVXL]+(?: BIS)?)$")
EU_PART = re.compile(r"^PARTE ([A-Z])$")
BOE_ARTICLE = re.compile(r"^Art[íi]culo (\d+(?: bis| ter| quater)?)\.\s*(.*)$")
BOE_DISP = re.compile(r"^Disposición (adicional|transitoria|derogatoria|final) ([a-zúé]+)\.\s*(.*)$")
BOE_ANNEX = re.compile(r"^ANEXO ([IVXL]+(?: BIS)?)\.?\s*(.*)$", re.I)
BOE_PREAMBLE = re.compile(r"^(PREÁMBULO|Preámbulo)$")
PLIEGO_TOP = re.compile(r"^(\d)\.\s+([A-ZÁÉÍÓÚÑ][A-ZÁÉÍÓÚÑ ,/()]+)\.?\s*$")
PLIEGO_SUB = re.compile(r"^([a-z](?:\.\d+)*)[\.\)]\s*(\S.*)$")


def is_upper_title(text: str) -> bool:
    letters = [c for c in text if c.isalpha()]
    return bool(letters) and sum(c.isupper() for c in letters) / len(letters) > 0.8


def split_sections(lines: list[tuple[int, str]], kind: str) -> list[dict]:
    """Group lines into sections: {location, heading, page, lines}."""
    sections: list[dict] = []
    first = "Preámbulo" if kind == "boe" else "Encabezado"   # BOE laws open with their preamble
    current = {"location": first, "heading": "", "page": lines[0][0] if lines else 1, "lines": []}
    skip_title = False         # BOE puts a TÍTULO/CAPÍTULO name on the line after "TÍTULO I"
    pliego_top = None
    pending_title = False      # EU articles put their title on the line after "Artículo N"
    eu_annex = None

    def start(location: str, heading: str, page: int) -> None:
        nonlocal current
        if current["lines"] or current["heading"]:
            sections.append(current)
        current = {"location": location, "heading": heading, "page": page, "lines": []}

    next_lines = {n: lines[n + 1][1] for n in range(len(lines) - 1)}
    for n, (page, line) in enumerate(lines):
        if kind == "eu":
            if m := EU_ARTICLE.match(line):
                eu_annex = None
                start(f"Artículo {m.group(1)}", "", page)
                pending_title = True
                continue
            if m := EU_ANNEX.match(line):
                eu_annex = m.group(1)
                start(f"Anexo {eu_annex}", "", page)
                pending_title = True
                continue
            if eu_annex and (m := EU_PART.match(line)):
                start(f"Anexo {eu_annex}, Parte {m.group(1)}", "", page)
                pending_title = True
                continue
            if re.match(r"^(CAPÍTULO [IVX]+|SECCIÓN \d+)$", line):
                continue   # structural headings: the article/annex is the unit
            if pending_title:
                current["heading"] = line
                pending_title = False
                continue
        elif kind == "boe":
            if current["heading"] and not current["lines"] and not current["heading"].endswith(".") \
                    and current["location"] != "Preámbulo" and len(current["heading"]) < 200:
                current["heading"] += " " + line   # a title that runs onto a second line
                continue
            if m := BOE_ARTICLE.match(line):
                start(f"Artículo {m.group(1)}", m.group(2), page)
                continue
            if m := BOE_DISP.match(line):
                start(f"Disposición {m.group(1)} {m.group(2)}", m.group(3), page)
                continue
            if (m := BOE_ANNEX.match(line)) and line.split()[0].isupper():
                start(f"Anexo {m.group(1).upper()}", m.group(2), page)
                continue
            if BOE_PREAMBLE.match(line) or line == "EXPOSICIÓN DE MOTIVOS":
                if current["location"] != "Preámbulo" or current["lines"]:
                    start("Preámbulo", "", page)
                continue
            if re.match(r"^(TÍTULO|CAPÍTULO) ([IVXL]+|PRELIMINAR|[A-ZÚ]+)\.?\s*$", line):
                skip_title = True
                continue
            if re.match(r"^(TÍTULO|CAPÍTULO) [IVXL]+\.\s+\S", line):
                continue
            if skip_title:
                skip_title = False
                if len(line) < 120 and not line.endswith(":"):
                    continue
        elif kind == "pliego":
            # A numbered capitals line is a top-level section only if it is the next number
            # and is not itself followed by "N.1" (Ribera's tasting notes reuse 1./2./3.).
            if (m := PLIEGO_TOP.match(line)) and int(m.group(1)) == int(pliego_top or 0) + 1 \
                    and not next_lines.get(n, "").startswith(f"{m.group(1)}.1"):
                pliego_top = m.group(1)
                start(f"Sección {pliego_top}", m.group(2).title(), page)
                continue
            if pliego_top and (m := PLIEGO_SUB.match(line)):
                code, title = m.group(1), m.group(2)
                nested = "." in code
                if len(line) < 110 and (is_upper_title(title) or (nested and title[0].isupper())):
                    start(f"Sección {pliego_top}.{code}", title.rstrip(". "), page)
                    continue
        current["lines"].append(line)
    sections.append(current)
    for s in sections:
        s["text"] = join_lines(s["lines"])
    return [s for s in sections if s["text"] or s["heading"]]


ENUM_START = re.compile(r"^(\d+\.|[a-z]\)|[ivx]+\)|[a-z]\.\d+\)|•|—|-)\s")


def join_lines(lines: list[str]) -> str:
    """Re-flow PDF lines into paragraphs: a new paragraph starts at an enumerator
    (1., a), i), •) or after a line that ends a sentence."""
    paragraphs: list[str] = []
    for line in lines:
        if not paragraphs:
            paragraphs.append(line)
        elif ENUM_START.match(line) or paragraphs[-1].endswith((".", ":", ";")) and line[:1].isupper():
            paragraphs.append(line)
        else:
            paragraphs[-1] += " " + line
    return "\n".join(paragraphs)


def detect_kind(lines: list[tuple[int, str]]) -> str:
    """For files added later: guess the layout from the headings it contains."""
    text = [l for _, l in lines]
    scores = {
        "eu": sum(bool(EU_ARTICLE.match(l)) for l in text),
        "boe": sum(bool(BOE_ARTICLE.match(l)) for l in text),
        "pliego": sum(bool(PLIEGO_TOP.match(l)) for l in text) * 3,
    }
    kind, score = max(scores.items(), key=lambda kv: kv[1])
    return kind if score >= 3 else "pages"


# ----------------------------------------------------------------------------------
# 4. Chunk (two designs)
# ----------------------------------------------------------------------------------


def words(text: str) -> int:
    return len(text.split())


def structure_chunks(doc: dict, sections: list[dict]) -> list[dict]:
    """One chunk per legal unit; long units split at paragraph boundaries."""
    chunks = []
    for s in sections:
        if not s["text"]:
            continue   # a heading with nothing under it (its sub-sections carry the text)
        header = f"{doc['title']} — {s['location']}" + (f". {s['heading']}" if s["heading"] else "")
        paragraphs = []
        for para in s["text"].split("\n") if s["text"] else []:
            tokens = para.split()   # a paragraph longer than a chunk (a table) is cut by words
            paragraphs += [" ".join(tokens[i:i + config.STRUCT_MAX_WORDS])
                           for i in range(0, len(tokens), config.STRUCT_MAX_WORDS)] or [para]
        parts: list[list[str]] = [[]]
        for para in paragraphs:
            if parts[-1] and words(" ".join(parts[-1] + [para])) > config.STRUCT_MAX_WORDS:
                parts.append([])
            parts[-1].append(para)
        for n, part in enumerate(parts, 1):
            body = "\n".join(part) or "(sin texto)"
            suffix = f" (parte {n}/{len(parts)})" if len(parts) > 1 else ""
            chunks.append({
                "text": f"{header}{suffix}\n{body}",
                "location": s["location"],
                "locations": s["location"],
                "page": s["page"],
            })
    return chunks


def fixed_chunks(doc: dict, sections: list[dict]) -> list[dict]:
    """Sliding windows over the whole document, blind to its structure. The location
    recorded is the unit the window starts in; `locations` lists every unit it touches."""
    tokens: list[tuple[str, str, int]] = []      # (word, location, page)
    for s in sections:
        tokens += [(w, s["location"], s["page"]) for w in (s["heading"] + " " + s["text"]).split()]
    step = config.FIXED_WORDS - config.FIXED_OVERLAP
    chunks = []
    for start in range(0, max(len(tokens) - config.FIXED_OVERLAP, 1), step):
        window = tokens[start:start + config.FIXED_WORDS]
        seen = list(dict.fromkeys(loc for _, loc, _ in window))
        chunks.append({
            "text": " ".join(w for w, _, _ in window),
            "location": window[0][1],
            "locations": "|".join(seen),
            "page": window[0][2],
        })
    return chunks


def file_sha256(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def chunk_file(path: Path, design: str, doc: dict | None = None) -> list[dict]:
    """Extract, clean, split and chunk one file. Every chunk carries its metadata."""
    path = Path(path)
    doc = dict(doc or {})
    doc.setdefault("id", re.sub(r"[^a-z0-9_]+", "_", path.stem.lower()).strip("_"))
    doc.setdefault("title", path.stem)
    pages = extract_pages(path)
    kind = doc.get("kind")
    lines = clean_pages(pages, kind or "")
    if not kind:
        kind = detect_kind(lines)
        lines = clean_pages(pages, kind)
    if kind == "pages":   # unknown layout: one section per page, located by page number
        sections = [{"location": f"Página {p}", "heading": "", "page": p,
                     "text": join_lines([l for q, l in lines if q == p])} for p in sorted({p for p, _ in lines})]
    else:
        sections = split_sections(lines, kind)
    raw = (structure_chunks if design == "structure" else fixed_chunks)(doc, sections)
    sha = file_sha256(path)
    chunks = []
    for n, c in enumerate(raw):
        chunks.append({
            "id": f"{doc['id']}:{design}:{n:04d}",
            "text": c["text"],
            "metadata": {
                "source": doc["id"],
                "title": doc["title"],
                "location": c["location"],
                "locations": c["locations"],
                "page": c["page"],
                "words": words(c["text"]),
                "design": design,
                "file_sha256": sha,
                "text_sha": hashlib.sha256(c["text"].encode()).hexdigest()[:16],
                "url": (doc.get("urls") or [""])[0],
            },
        })
    return chunks


# ----------------------------------------------------------------------------------
# 5. Embed and store
# ----------------------------------------------------------------------------------

_client = None
_task_types = True   # gemini-embedding-2 is asked for retrieval-specific vectors when it accepts it


def genai_client():
    global _client
    if _client is None:
        from google import genai

        from api_key import load_api_key

        _client = genai.Client(api_key=load_api_key())
    return _client


class QuotaExhausted(RuntimeError):
    pass


class Pacer:
    """Keep requests and (estimated) tokens per rolling minute under the free-tier limits."""

    def __init__(self, tokens_per_min: int, requests_per_min: int):
        self.tokens_per_min, self.requests_per_min = tokens_per_min, requests_per_min
        self.log: deque[tuple[float, int]] = deque()

    def wait(self, tokens: int) -> None:
        while True:
            now = time.time()
            while self.log and now - self.log[0][0] > 60:
                self.log.popleft()
            used = sum(t for _, t in self.log)
            if len(self.log) < self.requests_per_min and used + tokens <= self.tokens_per_min:
                self.log.append((now, tokens))
                return
            time.sleep(max(0.5, 60 - (now - self.log[0][0]) + 0.1))


_pacer = Pacer(config.EMBED_TOKENS_PER_MIN, config.EMBED_REQUESTS_PER_MIN)


def estimate_tokens(text: str) -> int:
    return int(words(text) * 1.8) + 8     # Spanish legal text: ~1.6-1.8 tokens per word


def embed_texts(texts: list[str], task: str) -> list[list[float]]:
    """Embed a batch with Gemini, one vector per text, retrying on rate limits."""
    global _task_types
    from google.genai import errors, types

    contents = [types.Content(parts=[types.Part(text=t)]) for t in texts]
    for attempt in range(8):
        _pacer.wait(sum(estimate_tokens(t) for t in texts))
        try:
            cfg = types.EmbedContentConfig(task_type=task) if _task_types else None
            result = genai_client().models.embed_content(model=config.EMBED_MODEL, contents=contents, config=cfg)
            vectors = [e.values for e in result.embeddings]
            if len(vectors) != len(texts):
                raise RuntimeError(f"asked for {len(texts)} vectors, got {len(vectors)}")
            return vectors
        except errors.ClientError as error:
            message = str(error)
            if error.code == 400 and _task_types and "task" in message.lower():
                log("  this model does not take task_type; embedding without it")
                _task_types = False
                continue
            if error.code == 429:
                if "PerDay" in message or "per day" in message.lower():
                    raise QuotaExhausted(message) from error
                delay = 20 * (attempt + 1)
                if m := re.search(r"retry in ([\d.]+)s|retryDelay['\"]?: ?['\"]?(\d+)", message):
                    delay = float(m.group(1) or m.group(2)) + 1
                log(f"  rate limited, waiting {delay:.0f}s")
                time.sleep(delay)
                continue
            raise
        except errors.ServerError as error:
            log(f"  server error {error.code}, retrying")
            time.sleep(10 * (attempt + 1))
    raise RuntimeError("Embedding failed after 8 attempts")


def get_collection(design: str):
    import chromadb
    from chromadb.config import Settings

    client = chromadb.PersistentClient(path=str(config.CHROMA_DIR), settings=Settings(anonymized_telemetry=False))
    return client.get_or_create_collection(f"wine_{design}", metadata={"hnsw:space": "cosine"})


def embed_and_store(chunks: list[dict], collection, batch_words: int = 3500) -> int:
    """Embed the chunks that have no saved vector (or whose text changed) and store each
    batch immediately. Returns how many texts were embedded."""
    if not chunks:
        return 0
    stored = collection.get(ids=[c["id"] for c in chunks], include=["metadatas"])
    saved = {i: m.get("text_sha") for i, m in zip(stored["ids"], stored["metadatas"])}
    todo = [c for c in chunks if saved.get(c["id"]) != c["metadata"]["text_sha"]]
    embedded = 0
    batch: list[dict] = []

    def flush() -> None:
        nonlocal embedded, batch
        vectors = embed_texts([c["text"] for c in batch], "RETRIEVAL_DOCUMENT")
        collection.upsert(
            ids=[c["id"] for c in batch],
            documents=[c["text"] for c in batch],
            metadatas=[c["metadata"] for c in batch],
            embeddings=vectors,
        )
        embedded += len(batch)
        log(f"  embedded and saved {embedded}/{len(todo)}")
        batch = []

    for c in todo:
        if batch and (sum(words(b["text"]) for b in batch) + words(c["text"]) > batch_words or len(batch) >= 90):
            flush()
        batch.append(c)
    if batch:
        flush()
    return embedded


def load_query_cache() -> dict:
    if config.QUERY_CACHE.exists():
        return json.loads(config.QUERY_CACHE.read_text(encoding="utf-8"))
    return {}


def embed_query(text: str, cache: dict | None = None, save: bool = True) -> list[float]:
    """Vector for a search query. Cached on disk by text, so repeating a question
    (evaluation runs, the check script) costs no quota."""
    cache = load_query_cache() if cache is None else cache
    key = f"{config.EMBED_MODEL}|{text.strip()}"
    if key not in cache:
        cache[key] = embed_texts([text.strip()], "RETRIEVAL_QUERY")[0]
        if save:
            config.INDEX_DIR.mkdir(exist_ok=True)
            config.QUERY_CACHE.write_text(json.dumps(cache), encoding="utf-8")
    return cache[key]


def write_chunk_file(design: str, chunks: list[dict]) -> None:
    """index/chunks_<design>.jsonl: every chunk's text and metadata, for keyword search
    and for reading what the model is given."""
    path = config.INDEX_DIR / f"chunks_{design}.jsonl"
    path.write_text("".join(json.dumps(c, ensure_ascii=False) + "\n" for c in chunks), encoding="utf-8")


# ----------------------------------------------------------------------------------
# main.py index
# ----------------------------------------------------------------------------------


def main() -> None:
    config.INDEX_DIR.mkdir(exist_ok=True)
    stats: dict = {"documents": {}, "designs": {}}
    all_chunks: dict[str, list[dict]] = {d: [] for d in config.DESIGNS}
    for doc in config.DOCUMENTS:
        path = download(doc)
        pages = extract_pages(path)
        lines = clean_pages(pages, doc["kind"])
        stats["documents"][doc["id"]] = {
            "title": doc["title"], "pages": len(pages),
            "words_raw": sum(words(p) for p in pages), "words_clean": sum(words(l) for _, l in lines),
            "url": doc["urls"][0], "date": doc["date"], "licence": doc["licence"],
        }
        for design in config.DESIGNS:
            all_chunks[design] += chunk_file(path, design, doc)

    total = sum(d["words_clean"] for d in stats["documents"].values())
    print(f"{'document':<26}{'pages':>6}{'words':>9}")
    for doc_id, d in stats["documents"].items():
        print(f"{doc_id:<26}{d['pages']:>6}{d['words_clean']:>9,}")
    print(f"{'TOTAL':<26}{'':>6}{total:>9,}")

    for design, chunks in all_chunks.items():
        sizes = [c["metadata"]["words"] for c in chunks]
        stats["designs"][design] = {
            "chunks": len(chunks), "mean_words": round(sum(sizes) / len(sizes), 1),
            "max_words": max(sizes), "min_words": min(sizes),
        }
        write_chunk_file(design, chunks)
        print(f"design {design:<10} {len(chunks):>4} chunks, {sum(sizes) / len(sizes):.0f} words on average")
    (config.INDEX_DIR / "index_stats.json").write_text(json.dumps(stats, indent=2, ensure_ascii=False), encoding="utf-8")

    for design, chunks in all_chunks.items():
        collection = get_collection(design)
        try:
            n = embed_and_store(chunks, collection)
        except QuotaExhausted:
            print(f"\nDaily embedding quota reached while indexing '{design}'. Everything embedded so far is "
                  f"saved in index/. Run `main.py index` again after the quota resets (09:00 in Spain).")
            sys.exit(1)
        print(f"design {design:<10} {collection.count()} vectors stored ({n} embedded this run)")


if __name__ == "__main__":
    main()
