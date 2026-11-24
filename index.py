"""
Assignment 3: build the index (`uv run python main.py index`).

Corpus: EU passenger-rights law (air, rail, bus, sea, package travel), from EUR-Lex.

Steps
1. download  - save each document's HTML in corpus/ (only if missing)
2. extract   - HTML -> clean lines of text
3. chunk     - two designs:
                 "fixed":   windows of 200 words, no structure
                 "article": one chunk per article (long articles split)
               every chunk keeps its source and location (e.g. "Article 7")
4. embed     - Gemini embeddings, saved in ChromaDB (index/), batch by batch.
               Chunks that already have a vector are skipped, so re-running costs nothing.

server.py imports chunk_file() and embed_and_store() for its add_document tool.
"""

import hashlib
import os
import re
import sys
import time
from pathlib import Path

import httpx
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
EXTRA_DIR = ROOT / "extra_docs"   # documents for the add_document demo, not in the base index
# CORPUS_INDEX_DIR lets evaluate.py try add_document on a copy of the index
INDEX_DIR = Path(os.environ.get("CORPUS_INDEX_DIR", ROOT / "index"))

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768          # smaller vectors -> smaller index, same quality for our use
BATCH = 50               # texts per embedding request

FIXED_WORDS = 200        # design "fixed": words per window
ARTICLE_MAX_WORDS = 350  # design "article": longer articles are split in parts

DESIGNS = ["fixed", "article"]
CHOSEN_DESIGN = "article"   # picked by the hit-rate numbers in evaluate.py (see REPORT.md)

# The five documents of the base corpus. source = the name used in citations.
DOCUMENTS = [
    {"source": "air-261-2004", "celex": "32004R0261",
     "title": "Regulation (EC) No 261/2004 - air passenger rights (denied boarding, cancellation, delay)"},
    {"source": "rail-2021-782", "celex": "32021R0782",
     "title": "Regulation (EU) 2021/782 - rail passengers' rights and obligations"},
    {"source": "bus-181-2011", "celex": "32011R0181",
     "title": "Regulation (EU) No 181/2011 - bus and coach passenger rights"},
    {"source": "sea-1177-2010", "celex": "32010R1177",
     "title": "Regulation (EU) No 1177/2010 - sea and inland waterway passenger rights"},
    {"source": "package-travel-2015-2302", "celex": "32015L2302",
     "title": "Directive (EU) 2015/2302 - package travel and linked travel arrangements"},
]

# Kept out of the base index on purpose: added later with the add_document tool.
EXTRA_DOCUMENTS = [
    {"source": "air-liability-889-2002", "celex": "32002R0889",
     "title": "Regulation (EC) No 889/2002 - air carrier liability for passengers and baggage"},
]


def log(*args) -> None:
    """Print to stderr (stdout is reserved for MCP when server.py imports this file)."""
    print(*args, file=sys.stderr, flush=True)


# ---------------------------------------------------------------- 1. download

def eurlex_url(celex: str) -> str:
    return f"https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:{celex}"


def download(doc: dict, folder: Path = CORPUS_DIR) -> Path:
    """Return <folder>/<source>.html, downloading it from EUR-Lex if it is missing.

    The HTML files are committed (EUR-Lex allows reuse), because EUR-Lex often
    answers scripts with a bot challenge (HTTP 202, empty page) instead of the text.
    """
    folder.mkdir(exist_ok=True)
    path = folder / f"{doc['source']}.html"
    if not path.exists():
        log(f"downloading {doc['source']} ...")
        response = httpx.get(eurlex_url(doc["celex"]), headers={"User-Agent": "Mozilla/5.0"},
                             follow_redirects=True, timeout=60)
        if response.status_code != 200 or not response.content:
            raise RuntimeError(f"EUR-Lex did not send {doc['celex']} (HTTP {response.status_code}). "
                               f"Download {eurlex_url(doc['celex'])} in a browser and save it as {path}.")
        path.write_bytes(response.content)
    return path


# ---------------------------------------------------------------- 2. extract and clean

def extract_lines(path: Path) -> list[str]:
    """HTML (or .txt) -> list of clean, non-empty text lines."""
    raw = path.read_text(encoding="utf-8", errors="replace")   # a non-UTF-8 file must not crash the tool
    if path.suffix.lower() in (".html", ".htm"):
        soup = BeautifulSoup(raw, "html.parser")
        for tag in soup(["script", "style"]):
            tag.decompose()
        raw = soup.get_text("\n")
    # " ".join(split()) also turns non-breaking spaces (\xa0) into normal spaces:
    # without this "Article\xa07" in the sea regulation is not recognised as a heading.
    lines = [" ".join(line.split()) for line in raw.splitlines()]
    return [line for line in lines if line]


ARTICLE_RE = re.compile(r"Article (\d+[a-z]?)")
ANNEX_RE = re.compile(r"ANNEX ?([IVX]*)")


def label_lines(lines: list[str]) -> list[tuple[str, str]]:
    """Give every line its location: 'Recitals', 'Article 7', 'Annex I, Article 3', 'Annex II'.

    Also drops the parts that only add noise: the EUR-Lex page header, the
    signatures after 'Done at ...' and correlation tables.
    """
    labelled = []
    location = None          # None = still in the page header, skip
    annex = None             # e.g. "Annex I" once we are inside an annex
    skipping = False         # True between "Done at" and the next annex
    for i, line in enumerate(lines):
        next_line = lines[i + 1] if i + 1 < len(lines) else ""
        if location is None:
            if line.startswith("Whereas") or line.startswith("THE EUROPEAN PARLIAMENT"):
                location = "Recitals"
            else:
                continue
        if line.startswith("Done at"):
            skipping = True
            continue
        annex_match = ANNEX_RE.fullmatch(line)
        if annex_match:
            annex = f"Annex {annex_match.group(1)}".strip()
            location = annex
            # correlation tables are lists of article numbers, useless to a reader
            skipping = "CORRELATION" in next_line.upper()
            continue
        if skipping:
            continue
        article_match = ARTICLE_RE.fullmatch(line)
        if article_match:
            article = f"Article {article_match.group(1)}"
            location = f"{annex}, {article}" if annex else article
            continue
        labelled.append((location, line))
    return labelled


# ---------------------------------------------------------------- 3. chunk

def make_chunk(source: str, design: str, n: int, locations: list[str], text: str) -> dict:
    # "location" = where the chunk starts; "locations" = every article it touches
    unique = list(dict.fromkeys(locations))
    return {
        "id": f"{design}:{source}:{n:04d}",
        "text": text,
        "source": source,
        "location": unique[0],
        "locations": " | ".join(unique),
        "design": design,
    }


def chunk_fixed(source: str, labelled: list[tuple[str, str]]) -> list[dict]:
    """Design 'fixed': cut the text every FIXED_WORDS words, ignoring structure."""
    words = [(loc, w) for loc, line in labelled for w in line.split()]
    chunks = []
    for start in range(0, len(words), FIXED_WORDS):
        window = words[start:start + FIXED_WORDS]
        chunks.append(make_chunk(source, "fixed", len(chunks), [loc for loc, _ in window],
                                 " ".join(w for _, w in window)))
    return chunks


def chunk_article(source: str, labelled: list[tuple[str, str]]) -> list[dict]:
    """Design 'article': one chunk per article (or recitals / annex), split if too long.

    The article title (its first line, e.g. 'Right to compensation') is repeated at
    the top of every part, so each part still says what it is about.
    """
    sections: dict[str, list[str]] = {}
    for loc, line in labelled:
        sections.setdefault(loc, []).append(line)

    chunks = []
    for loc, lines in sections.items():
        header = f"{loc}: {lines[0]}" if loc.split(", ")[-1].startswith("Article") else loc
        part, part_words = [], 0
        for line in lines:
            n = len(line.split())
            if part and part_words + n > ARTICLE_MAX_WORDS:
                chunks.append(make_chunk(source, "article", len(chunks), [loc], header + "\n" + " ".join(part)))
                part, part_words = [], 0
            part.append(line)
            part_words += n
        if part:
            chunks.append(make_chunk(source, "article", len(chunks), [loc], header + "\n" + " ".join(part)))
    return chunks


def chunk_file(path: str | Path, source: str | None = None, design: str = CHOSEN_DESIGN) -> list[dict]:
    """Extract, clean and chunk one file (.html or .txt). Used by main() and by server.py."""
    path = Path(path)
    # "Baggage Rules_2002.html" -> "baggage-rules-2002": the citation check in agent.py
    # only recognises lower-case source names with dashes.
    source = source or re.sub(r"[^a-z0-9]+", "-", path.stem.lower()).strip("-") or "document"
    labelled = label_lines(extract_lines(path))
    if not labelled:   # a file without EUR-Lex structure: treat it all as one section
        labelled = [("Full text", line) for line in extract_lines(path)]
    chunker = chunk_fixed if design == "fixed" else chunk_article
    chunks = chunker(source, labelled)
    file_hash = hashlib.sha256(path.read_bytes()).hexdigest()[:16]
    for c in chunks:
        c["file_hash"] = file_hash
    return chunks


# ---------------------------------------------------------------- 4. embed and store

def get_client():
    from google import genai
    from api_key import load_api_key
    return genai.Client(api_key=load_api_key())


def embed_texts(texts: list[str], client=None) -> list[list[float]]:
    """Embed a list of texts with Gemini. Waits and retries if we hit the rate limit."""
    from google.genai import types
    client = client or get_client()
    for attempt in range(6):
        try:
            # one Content per text: a plain list of strings is merged into ONE vector by gemini-embedding-2
            result = client.models.embed_content(
                model=EMBED_MODEL, contents=[types.Content(parts=[types.Part(text=t)]) for t in texts],
                config=types.EmbedContentConfig(output_dimensionality=EMBED_DIM),
            )
            return [e.values for e in result.embeddings]
        except Exception as error:  # noqa: BLE001
            if "429" in str(error) or "RESOURCE_EXHAUSTED" in str(error):
                wait = 20 * (attempt + 1)
                log(f"rate limited, waiting {wait}s ...")
                time.sleep(wait)
            else:
                raise
    raise RuntimeError("Embedding failed after several retries (daily limit reached?).")


def get_collection(design: str = CHOSEN_DESIGN):
    """The ChromaDB collection of one design, stored in index/."""
    import chromadb
    client = chromadb.PersistentClient(path=str(INDEX_DIR / "chroma"))
    return client.get_or_create_collection(f"corpus_{design}", metadata={"hnsw:space": "cosine"})


def embed_and_store(chunks: list[dict], design: str = CHOSEN_DESIGN) -> int:
    """Embed the chunks that are not in the index yet and store them. Returns how many were new."""
    collection = get_collection(design)
    ids = [c["id"] for c in chunks]
    existing = set(collection.get(ids=ids)["ids"]) if ids else set()
    todo = [c for c in chunks if c["id"] not in existing]
    if not todo:
        return 0
    client = get_client()
    for start in range(0, len(todo), BATCH):
        batch = todo[start:start + BATCH]
        vectors = embed_texts([c["text"] for c in batch], client)
        collection.add(   # saved right away: a crash later loses nothing
            ids=[c["id"] for c in batch],
            embeddings=vectors,
            documents=[c["text"] for c in batch],
            metadatas=[{k: c[k] for k in ("source", "location", "locations", "design", "file_hash")} for c in batch],
        )
        log(f"  embedded {start + len(batch)}/{len(todo)} new chunks ({design})")
    return len(todo)


def all_chunks(design: str) -> list[dict]:
    """Chunk the five base documents with one design."""
    chunks = []
    for doc in DOCUMENTS:
        chunks += chunk_file(download(doc), doc["source"], design)
    return chunks


def main() -> None:
    for doc in EXTRA_DOCUMENTS:
        download(doc, EXTRA_DIR)

    print("Corpus (words after cleaning):")
    for doc in DOCUMENTS:
        words = sum(len(line.split()) for _, line in label_lines(extract_lines(download(doc))))
        print(f"  {doc['source']:28s} {words:6d} words")

    for design in DESIGNS:
        chunks = all_chunks(design)
        sizes = [len(c["text"].split()) for c in chunks]
        print(f"\nDesign '{design}': {len(chunks)} chunks, {sum(sizes) / len(sizes):.0f} words on average")
        if "--dry-run" in sys.argv:
            continue
        new = embed_and_store(chunks, design)
        print(f"  {new} new vectors embedded, {len(chunks) - new} already saved")


if __name__ == "__main__":
    main()
