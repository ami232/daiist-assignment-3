"""
Assignment 3: build the index (`main.py index`).

Corpus: eight GOV.UK pages on the UK Student and Graduate routes, under the
Open Government Licence v3.0. The pipeline, one step per function:

    download_corpus()       GOV.UK Content API -> corpus/<source>.json (kept, so
                            the text never changes under your test set)
    parse_blocks(source)    HTML -> paragraphs/list items/tables, each tagged
                            with its heading and rule number (e.g. "ST 4.2")
    chunk_fixed(blocks)     design "fixed":   ~150-word windows, 30-word overlap
    chunk_section(blocks)   design "section": one heading's text per chunk,
                            long sections split, tiny ones merged
    embed_and_store(...)    Gemini embeddings -> ChromaDB in index/chroma,
                            saved batch by batch; chunks already stored are skipped

    chunk_file(path)        the same steps for one local file (add_document uses it)

Run it:
    uv run python main.py index                  # both designs
    uv run python index.py --design section      # one design (spread quota over days)
    uv run python index.py --dry-run             # download + chunk only, no API calls

server.py and evaluate.py import search(), add_document() and the design names
from here. Importing this file prints nothing (stdout carries MCP in server.py).
"""

import argparse
import hashlib
import html
import json
import logging
import re
import sys
import time
import urllib.request
from collections import Counter
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"
CHROMA_DIR = INDEX_DIR / "chroma"
QUERY_CACHE = INDEX_DIR / "query_vectors.json"
OUTLINE_FILE = ROOT / "eval" / "corpus_outline.md"

log = logging.getLogger("index")
if not log.handlers:  # log to stderr only, never stdout
    handler = logging.StreamHandler(sys.stderr)
    handler.setFormatter(logging.Formatter("%(message)s"))
    log.addHandler(handler)
    log.setLevel(logging.INFO)
    log.propagate = False  # never reach a root handler that might write to stdout

# --------------------------------------------------------------------------
# Corpus: short source name -> GOV.UK path. The short name is what chunks,
# citations and eval/questions.csv's expected_source use.
# --------------------------------------------------------------------------
SOURCES = {
    "student-visa-guide": "student-visa",
    "appendix-student": "guidance/immigration-rules/immigration-rules-appendix-student",
    "student-caseworker-guidance": "government/publications/student-route-caseworker-guidance/student-and-child-student",
    "graduate-visa-guide": "graduate-visa",
    "appendix-graduate": "guidance/immigration-rules/immigration-rules-appendix-graduate",
    "graduate-caseworker-guidance": "government/publications/graduate-caseworker-guidance/graduate-caseworker-guidance-accessible-version",
    "appendix-finance": "guidance/immigration-rules/immigration-rules-appendix-finance",
    "appendix-english-language": "guidance/immigration-rules/immigration-rules-appendix-english-language",
}
CONTENT_API = "https://www.gov.uk/api/content/"
LICENCE = "Open Government Licence v3.0"

# Cleaning. Sections about the guidance document itself, not the rules:
SKIP_SECTIONS = {"contacts", "publication", "changes from last version of this guidance"}
# Blocks with no information: internal-only markers and redacted stubs.
NOISE = re.compile(r"^(official\s*[-–—]\s*sensitive\b.*|the information in this section has been removed\b.*)$", re.I)

# --------------------------------------------------------------------------
# Chunking designs. YOUR decision: these numbers are a starting point.
# --------------------------------------------------------------------------
FIXED_WORDS, FIXED_OVERLAP = 150, 30           # design "fixed"
SECTION_MAX_WORDS, SECTION_MIN_WORDS = 300, 40  # design "section" (a split's tiny tail
DESIGNS = ("fixed", "section")                  # joins the piece before it, so a
                                                # chunk can reach MAX + MIN words)
# YOUR decision, by the numbers: set this to the design with the better hit
# rate once evaluate.py has compared them. server.py searches this design.
CHOSEN_DESIGN = "section"

# --------------------------------------------------------------------------
# Embeddings. gemini-embedding-2 takes no task_type; the task goes in the text.
# Both designs get the same prefix (document title + heading), so the only
# thing the comparison changes is where chunks start and end.
# --------------------------------------------------------------------------
EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768        # smaller vectors, smaller index; the model normalises them
BATCH_SIZE = 20        # texts per API call
DOC_PREFIX = "title: {title} | text: {text}"
QUERY_PREFIX = "task: search result | query: {query}"

# A rule number at the start of a paragraph, e.g. "ST 4.2." GOV.UK writes one
# rule without the space ("ST26.1."); it is stored as "ST 26.1" like the rest.
RULE_ID = re.compile(r"^([A-Z]{2,5}) ?(\d+(?:\.\d+)+[A-Za-z]?)\.?\s")


def rule_id(text: str) -> str | None:
    found = RULE_ID.match(text)
    return f"{found.group(1)} {found.group(2)}" if found else None


class QuotaExhausted(RuntimeError):
    """The free tier's daily limit is used up; rerun after 09:00 (Spain)."""


class RateLimited(RuntimeError):
    """Per-minute limits kept refusing requests; wait a few minutes and rerun."""


# ==========================================================================
# 1. Download
# ==========================================================================
def fetch_json(url: str) -> dict:
    for attempt in range(3):
        try:
            with urllib.request.urlopen(url, timeout=60) as response:
                return json.loads(response.read().decode("utf-8"))
        except OSError as error:  # network hiccup: try again, then give up
            if attempt == 2:
                raise RuntimeError(f"Could not download {url}: {error}") from error
            time.sleep(5)


def download_corpus() -> dict:
    """Fetch every source once into corpus/; later runs reuse the saved copy."""
    CORPUS_DIR.mkdir(exist_ok=True)
    pages = {}
    for source, path in SOURCES.items():
        file = CORPUS_DIR / f"{source}.json"
        if not file.exists():
            log.info(f"Downloading {source} ...")
            page = fetch_json(CONTENT_API + path)
            page["_fetched"] = date.today().isoformat()
            file.write_text(json.dumps(page, ensure_ascii=False), encoding="utf-8")
        pages[source] = json.loads(file.read_text(encoding="utf-8"))
    return pages


def page_info(source: str, page: dict) -> dict:
    return {
        "source": source,
        "title": page.get("title", source).strip(),
        "url": "https://www.gov.uk" + page.get("base_path", "/" + SOURCES.get(source, source)),
        "updated": (page.get("public_updated_at") or "")[:10],
        "fetched": page.get("_fetched", ""),
    }


# ==========================================================================
# 2. Extract and clean: HTML -> blocks with heading and rule number
# ==========================================================================
def clean(text: str) -> str:
    """Normalise whitespace and undo the stray spaces that appear when inline
    tags are joined, e.g. "( CAS )" -> "(CAS)" and "visa ." -> "visa."."""
    text = html.unescape(text).replace(" ", " ")
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"([(\[]) ", r"\1", text)
    text = re.sub(r" ([)\]])", r"\1", text)
    text = re.sub(r" ([.,;:!?])(?=\s|$)", r"\1", text)
    return text.strip()


def html_to_blocks(body: str, top_heading: str | None = None) -> list[dict]:
    """Walk the HTML in order. Each paragraph, list item or table becomes a block
    remembering the heading it sits under (and its parents)."""
    from bs4 import BeautifulSoup, Comment, NavigableString, Tag

    soup = BeautifulSoup(body, "html.parser")
    path: list[tuple[int, str]] = [(1, top_heading)] if top_heading else []
    blocks: list[dict] = []

    def emit(text: str) -> None:
        text = clean(text)
        if not text or NOISE.match(text):
            return
        if any(h.lower() in SKIP_SECTIONS for _, h in path):
            return
        blocks.append({
            "text": text,
            "heading": path[-1][1] if path else "Introduction",
            "heading_path": " > ".join(h for _, h in path) or "Introduction",
            "rule": rule_id(text),
        })

    def walk(node) -> None:
        for child in node.children:
            if isinstance(child, Comment):
                continue
            if isinstance(child, NavigableString):
                emit(str(child))
                continue
            if not isinstance(child, Tag):
                continue
            name = child.name
            if re.fullmatch(r"h[1-6]", name):
                level = int(name[1])
                while path and path[-1][0] >= level:
                    path.pop()
                path.append((level, clean(child.get_text(" "))))
            elif name in ("ol", "ul"):
                for item in child.find_all("li", recursive=False):
                    emit(item.get_text(" "))
            elif name == "table":
                rows = [" | ".join(clean(c.get_text(" ")) for c in tr.find_all(["th", "td"]))
                        for tr in child.find_all("tr")]
                emit(" ; ".join(r for r in rows if r))
            elif name in ("html", "body", "main", "article", "section", "div", "details", "span"):
                walk(child)
            else:
                emit(child.get_text(" "))

    walk(soup)
    return blocks


def content_api_blocks(page: dict) -> list[dict]:
    """A GOV.UK guide has parts (each with a title); everything else has one body."""
    details = page.get("details", {})
    if details.get("parts"):
        blocks = []
        for part in details["parts"]:
            blocks += html_to_blocks(part.get("body", ""), top_heading=clean(part.get("title", "")))
        return blocks
    return html_to_blocks(details.get("body", ""))


def parse_blocks(source: str, page: dict) -> list[dict]:
    info = page_info(source, page)
    blocks = content_api_blocks(page)
    for b in blocks:
        b.update(source=info["source"], title=info["title"], url=info["url"])
    return blocks


# ==========================================================================
# 3. Chunk: two designs. Every chunk carries source + location.
# ==========================================================================
def make_chunk(design: str, blocks: list[dict], text: str) -> dict:
    first = blocks[0]
    return {
        "design": design,
        "source": first["source"],
        "title": first["title"],
        "url": first["url"],
        "location": first["rule"] or first["heading"],   # where the chunk starts
        "heading_path": first["heading_path"],
        # Everything the chunk covers, used to decide whether a search "hit" the
        # expected_location of a test question:
        "sections": " | ".join(dict.fromkeys(b["heading"] for b in blocks)),
        "paths": " | ".join(dict.fromkeys(b["heading_path"] for b in blocks)),
        "rules": " | ".join(dict.fromkeys(b["rule"] for b in blocks if b["rule"])),
        "text": text,
        "words": len(text.split()),
    }


def chunk_fixed(blocks: list[dict]) -> list[dict]:
    """Design "fixed": ignore structure, cut every FIXED_WORDS words with overlap."""
    words = []  # (word, index of the block it came from)
    for i, b in enumerate(blocks):
        words += [(w, i) for w in b["text"].split()]
    chunks, step = [], FIXED_WORDS - FIXED_OVERLAP
    for start in range(0, max(len(words) - FIXED_OVERLAP, 1), step):
        window = words[start:start + FIXED_WORDS]
        covered = [blocks[i] for i in dict.fromkeys(i for _, i in window)]
        chunks.append(make_chunk("fixed", covered, " ".join(w for w, _ in window)))
    return chunks


def chunk_section(blocks: list[dict]) -> list[dict]:
    """Design "section": group blocks under the same heading. Split a section
    over SECTION_MAX_WORDS at block boundaries; merge one under SECTION_MIN_WORDS
    into the next section of the same document."""
    sections: list[list[dict]] = []
    for b in blocks:
        if sections and sections[-1][-1]["heading_path"] == b["heading_path"]:
            sections[-1].append(b)
        else:
            sections.append([b])

    merged: list[list[dict]] = []
    carry: list[dict] = []
    for sec in sections:
        sec = carry + sec
        carry = []
        if sum(len(b["text"].split()) for b in sec) < SECTION_MIN_WORDS:
            carry = sec
        else:
            merged.append(sec)
    if carry:
        if merged:
            merged[-1] += carry
        else:
            merged.append(carry)

    chunks = []
    for sec in merged:
        pieces: list[tuple[list[dict], str]] = []  # (blocks, text) per chunk
        piece, count = [], 0
        for b in sec:
            n = len(b["text"].split())
            if piece and count + n > SECTION_MAX_WORDS:
                pieces.append((piece, "\n".join(x["text"] for x in piece)))
                piece, count = [], 0
            if n > SECTION_MAX_WORDS:  # one huge block (a long table): cut it by words
                ws = b["text"].split()
                cuts = [ws[s:s + SECTION_MAX_WORDS] for s in range(0, len(ws), SECTION_MAX_WORDS)]
                if len(cuts) > 1 and len(cuts[-1]) < SECTION_MIN_WORDS:
                    cuts[-2:] = [cuts[-2] + cuts[-1]]
                pieces += [([b], " ".join(cut)) for cut in cuts]
                continue
            piece.append(b)
            count += n
        if piece:
            pieces.append((piece, "\n".join(x["text"] for x in piece)))
        # A tiny leftover at the end of a split section joins the piece before it.
        if len(pieces) > 1 and len(pieces[-1][1].split()) < SECTION_MIN_WORDS:
            (blocks_a, text_a), (blocks_b, text_b) = pieces[-2], pieces[-1]
            pieces[-2:] = [(blocks_a + [b for b in blocks_b if b not in blocks_a], text_a + "\n" + text_b)]
        chunks += [make_chunk("section", blocks, text) for blocks, text in pieces]
    return chunks


def build_chunks(design: str, blocks_by_source: dict[str, list[dict]]) -> list[dict]:
    chunker = {"fixed": chunk_fixed, "section": chunk_section}[design]
    chunks = []
    for blocks in blocks_by_source.values():  # never let a chunk span two documents
        doc_chunks = chunker(blocks)
        for n, c in enumerate(doc_chunks):
            c["chunk_no"] = n
        chunks += doc_chunks
    return chunks


def chunk_id(chunk: dict) -> str:
    """Same text in the same design and source -> same id -> embedded only once."""
    key = f"{chunk['design']}|{chunk['source']}|{chunk['text']}"
    return hashlib.sha256(key.encode("utf-8")).hexdigest()[:24]


# ==========================================================================
# 4. Embed and store
# ==========================================================================
_gemini = None
_chroma = None


def gemini():
    global _gemini
    if _gemini is None:
        from google import genai
        from api_key import load_api_key
        _gemini = genai.Client(api_key=load_api_key())
    return _gemini


def embed_texts(texts: list[str]) -> list[list[float]]:
    """One API call for a batch. Each text is its own Content, otherwise
    gemini-embedding-2 returns ONE vector for the whole batch."""
    from google.genai import errors, types

    contents = [types.Content(parts=[types.Part.from_text(text=t)]) for t in texts]
    config = types.EmbedContentConfig(output_dimensionality=EMBED_DIM)
    for attempt in range(6):
        try:
            result = gemini().models.embed_content(model=EMBED_MODEL, contents=contents, config=config)
            vectors = [e.values for e in result.embeddings]
            if len(vectors) != len(texts):
                raise RuntimeError(f"Asked for {len(texts)} vectors, got {len(vectors)}")
            return vectors
        except errors.ClientError as error:
            if error.code != 429:
                raise
            message = str(error)
            if "PerDay" in message or "per day" in message.lower():
                raise QuotaExhausted(message) from error
            # Per-minute limit: wait as long as the API asks (RetryInfo), else back off.
            asked = re.search(r"retryDelay\W+(\d+(?:\.\d+)?)s", message)
            wait = float(asked.group(1)) + 1 if asked else 15 * (attempt + 1)
            log.info(f"  rate limited, waiting {wait:.0f}s ...")
            time.sleep(wait)
        except errors.ServerError:  # 5xx: Google's side, usually brief
            log.info("  Gemini server error, retrying in 10s ...")
            time.sleep(10)
    raise RateLimited("Gemini kept refusing requests after several retries.")


def collection(design: str):
    global _chroma
    if _chroma is None:
        import chromadb
        from chromadb.config import Settings
        _chroma = chromadb.PersistentClient(path=str(CHROMA_DIR), settings=Settings(anonymized_telemetry=False))
    return _chroma.get_or_create_collection(
        f"chunks_{design}", embedding_function=None, configuration={"hnsw": {"space": "cosine"}},
    )


METADATA_FIELDS = ("source", "title", "url", "location", "heading_path", "sections", "paths",
                   "rules", "words", "chunk_no", "design")


def embed_and_store(chunks: list[dict], design: str, origin: str = "corpus") -> int:
    """Embed only chunks the collection does not have yet; save after every batch.
    Returns how many were embedded."""
    col = collection(design)
    unique = {chunk_id(c): c for c in reversed(chunks)}  # identical chunks: keep the first
    ids = [i for i in dict.fromkeys(chunk_id(c) for c in chunks)]

    def metadata(c: dict) -> dict:
        return {k: c[k] for k in METADATA_FIELDS} | {"origin": origin}

    stored = {}
    for s in range(0, len(ids), 500):
        got = col.get(ids=ids[s:s + 500], include=["metadatas"])
        stored.update(zip(got["ids"], got["metadatas"]))
    # Same text but new labels (e.g. a rule number now recognised): update them, no API call.
    relabel = [i for i in ids if i in stored and stored[i] != metadata(unique[i])]
    for s in range(0, len(relabel), 500):
        batch = relabel[s:s + 500]
        col.update(ids=batch, metadatas=[metadata(unique[i]) for i in batch])
    todo = [(i, unique[i]) for i in ids if i not in stored]
    log.info(f"[{design}] {len(ids)} chunks, {len(stored)} already stored"
             f"{f' ({len(relabel)} relabelled)' if relabel else ''}, {len(todo)} to embed")

    done = 0
    for s in range(0, len(todo), BATCH_SIZE):
        batch = todo[s:s + BATCH_SIZE]
        texts = [DOC_PREFIX.format(title=f"{c['title']} - {c['heading_path']}", text=c["text"]) for _, c in batch]
        vectors = embed_texts(texts)
        col.upsert(
            ids=[i for i, _ in batch],
            embeddings=vectors,
            documents=[c["text"] for _, c in batch],
            metadatas=[metadata(c) for _, c in batch],
        )
        done += len(batch)
        log.info(f"  [{design}] saved {done}/{len(todo)}")
    return done


def drop_stale(chunks: list[dict], design: str) -> None:
    """Remove corpus chunks this run no longer produces (e.g. you changed the
    chunk size). Documents added with add_document are left alone."""
    col = collection(design)
    keep = {chunk_id(c) for c in chunks}
    stored = col.get(where={"origin": "corpus"}, include=[])["ids"]
    stale = [i for i in stored if i not in keep]
    if stale:
        col.delete(ids=stale)
        log.info(f"[{design}] removed {len(stale)} outdated chunks")


# ==========================================================================
# 5. Search (used by server.py and evaluate.py)
# ==========================================================================
def embed_query(query: str) -> list[float]:
    """Embed a question once and remember it: repeated questions cost no quota."""
    text = QUERY_PREFIX.format(query=query.strip())
    key = f"{EMBED_MODEL}|{EMBED_DIM}|{text}"
    cache = {}
    if QUERY_CACHE.exists():
        try:
            cache = json.loads(QUERY_CACHE.read_text(encoding="utf-8"))
        except (OSError, ValueError):
            cache = {}
    if key not in cache:
        cache[key] = embed_texts([text])[0]
        try:  # if two programs write at once, losing a cache entry is harmless
            INDEX_DIR.mkdir(exist_ok=True)
            tmp = QUERY_CACHE.with_suffix(f".{time.time_ns()}.tmp")
            tmp.write_text(json.dumps(cache), encoding="utf-8")
            tmp.replace(QUERY_CACHE)
        except OSError:
            pass
    return cache[key]


def search(query: str, k: int = 5, design: str | None = None, where: dict | None = None) -> list[dict]:
    """Top-k chunks for a question, best first, each with its citation fields.
    `where` filters on metadata, e.g. {"origin": "corpus"} skips added documents."""
    col = collection(design or CHOSEN_DESIGN)
    if col.count() == 0:
        raise RuntimeError(f"index/ has no '{design or CHOSEN_DESIGN}' chunks. Run `uv run python main.py index` first.")
    result = col.query(query_embeddings=[embed_query(query)], n_results=min(k, col.count()), where=where,
                       include=["documents", "metadatas", "distances"])
    return [
        {"id": i, "text": doc, "score": round(1 - dist, 4), **meta}
        for i, doc, meta, dist in zip(result["ids"][0], result["documents"][0],
                                      result["metadatas"][0], result["distances"][0])
    ]


# ==========================================================================
# 6. One local file (used by server.py's add_document tool)
# ==========================================================================
def file_blocks(path: Path) -> tuple[str, list[dict]]:
    """Extract (title, blocks) from a local .html/.htm, .json (GOV.UK Content API,
    like the files in corpus/), .pdf, .md or .txt file."""
    suffix = path.suffix.lower()
    title = path.stem
    if suffix in (".html", ".htm"):
        from bs4 import BeautifulSoup
        soup = BeautifulSoup(path.read_text(encoding="utf-8", errors="replace"), "html.parser")
        if soup.title and clean(soup.title.get_text()):
            title = clean(soup.title.get_text()).split(" - GOV.UK")[0]
        # A page saved from a browser also holds menus, cookie banners and footers.
        for tag in soup(["script", "style", "noscript", "nav", "header", "footer", "aside", "form", "svg"]):
            tag.decompose()
        main = soup.find("main") or soup.find("article") or soup.body or soup
        blocks = html_to_blocks(str(main))
    elif suffix == ".json":
        page = json.loads(path.read_text(encoding="utf-8"))
        title = page.get("title", title).strip()
        blocks = content_api_blocks(page)
    elif suffix == ".pdf":
        from pypdf import PdfReader
        blocks = []
        for n, page in enumerate(PdfReader(str(path)).pages, start=1):
            text = clean(page.extract_text() or "")
            if text:
                blocks.append({"text": text, "heading": f"p. {n}", "heading_path": f"p. {n}", "rule": None})
    elif suffix in (".md", ".txt"):
        blocks, heading = [], "Introduction"
        for para in re.split(r"\n\s*\n", path.read_text(encoding="utf-8", errors="replace")):
            para = para.strip()
            if para.startswith("#"):
                heading = clean(para.lstrip("#"))
            elif para:
                blocks.append({"text": clean(para), "heading": heading, "heading_path": heading,
                               "rule": rule_id(clean(para))})
    else:
        raise ValueError(f"Unsupported file type {suffix!r}: use .html, .json, .pdf, .md or .txt")
    return title, blocks


def chunk_file(path: str | Path, design: str | None = None) -> list[dict]:
    """The corpus pipeline for one local file: extract, clean, chunk. The file
    name becomes the source name, e.g. skilled-worker-visa.html -> skilled-worker-visa."""
    file = Path(path).expanduser().resolve()
    source = re.sub(r"[^a-z0-9-]+", "-", file.stem.lower()).strip("-") or "document"
    title, blocks = file_blocks(file)
    for b in blocks:
        b.update(source=source, title=title, url=file.as_uri())
    return build_chunks(design or CHOSEN_DESIGN, {source: blocks}) if blocks else []


def add_document(path: str, design: str | None = None) -> str:
    """Run one file through the same pipeline and store it.

    YOUR decision, already-indexed documents: here, a file whose chunks are all
    stored already is skipped (no quota spent); a changed file with the same
    name replaces its old chunks. The core corpus is never overwritten."""
    design = design or CHOSEN_DESIGN
    file = Path(path).expanduser().resolve()
    if not file.is_file():
        return f"No file at {file}."
    try:
        chunks = chunk_file(file, design)
    except ValueError as error:
        return str(error)
    if not chunks:
        return f"No text could be extracted from {file.name}."
    source = chunks[0]["source"]
    col = collection(design)
    if source in SOURCES or col.get(where={"$and": [{"source": source}, {"origin": "corpus"}]}, include=[])["ids"]:
        return f"'{source}' is part of the core corpus; rename the file to add it as a separate document."
    old = set(col.get(where={"source": source}, include=[])["ids"])
    new = {chunk_id(c) for c in chunks}
    if old and old == new:
        return f"{file.name} is already indexed as '{source}' ({len(new)} chunks); nothing added."
    if old - new:
        col.delete(ids=list(old - new))
    added = embed_and_store(chunks, design, origin="added")
    action = "Replaced" if old else "Added"
    return f"{action} '{source}': {len(new)} chunks, {added} newly embedded, in design '{design}'."


# ==========================================================================
# Outline for writing the test set
# ==========================================================================
def write_outline(blocks_by_source: dict[str, list[dict]], pages: dict) -> None:
    """eval/corpus_outline.md: every source name, heading and rule number, i.e.
    the exact strings to use in questions.csv's expected_source/expected_location."""
    lines = ["# Corpus outline", "",
             "Use these exact strings in `eval/questions.csv`: the source name as `expected_source`, "
             "and a heading or rule number as `expected_location`. A heading name used more than "
             "once in a document is shown as its full path; use that path to point at one of them.", ""]
    for source, blocks in blocks_by_source.items():
        info = page_info(source, pages[source])
        words = sum(len(b["text"].split()) for b in blocks)
        paths = list(dict.fromkeys(b["heading_path"] for b in blocks))
        repeated = {n for n, c in Counter(p.split(" > ")[-1] for p in paths).items() if c > 1}
        lines += [f"## `{source}`", "",
                  f"{info['title']}, {info['url']} (updated {info['updated']}, "
                  f"fetched {info['fetched']}, {LICENCE}, {words:,} words)", ""]
        for path in paths:
            name = path.split(" > ")[-1]
            rules = [b["rule"] for b in blocks if b["heading_path"] == path and b["rule"]]
            span = f" (rules {rules[0]} to {rules[-1]})" if len(rules) > 1 else (f" (rule {rules[0]})" if rules else "")
            label = f"`{path}`" if name in repeated else f"`{name}`"
            lines.append(f"{'  ' * path.count(' > ')}- {label}{span}")
        lines.append("")
    OUTLINE_FILE.parent.mkdir(exist_ok=True)
    OUTLINE_FILE.write_text("\n".join(lines), encoding="utf-8")


# ==========================================================================
def main() -> int:
    parser = argparse.ArgumentParser(description="Build the index.")
    parser.add_argument("--design", choices=DESIGNS, help="only this design (default: all)")
    parser.add_argument("--dry-run", action="store_true", help="download and chunk only; no API calls")
    args = parser.parse_args()

    pages = download_corpus()
    blocks_by_source = {s: parse_blocks(s, p) for s, p in pages.items()}
    write_outline(blocks_by_source, pages)

    print("Corpus:")
    total = 0
    for source, blocks in blocks_by_source.items():
        words = sum(len(b["text"].split()) for b in blocks)
        total += words
        print(f"  {source:30s} {words:>7,} words")
    print(f"  {'total':30s} {total:>7,} words\n")

    designs = [args.design] if args.design else list(DESIGNS)
    all_chunks = {d: build_chunks(d, blocks_by_source) for d in designs}
    for d, chunks in all_chunks.items():
        sizes = sorted(c["words"] for c in chunks)
        print(f"Design {d!r}: {len(chunks)} chunks, words per chunk min {sizes[0]}, "
              f"median {sizes[len(sizes) // 2]}, max {sizes[-1]}")
    print(f"Outline for writing questions: {OUTLINE_FILE.relative_to(ROOT)}\n")

    if args.dry_run:
        print("Dry run: nothing embedded.")
        return 0

    INDEX_DIR.mkdir(exist_ok=True)
    try:
        for d, chunks in all_chunks.items():
            embedded = embed_and_store(chunks, d)
            drop_stale(chunks, d)
            print(f"Design {d!r}: {embedded} chunks embedded this run, {collection(d).count()} stored.")
    except QuotaExhausted as error:
        print(f"\nDaily embedding quota reached. Everything embedded so far is saved;\n"
              f"run this again after 09:00 (Spain) to continue.\n  ({str(error)[:300]})")
        return 1
    except RateLimited as error:
        print(f"\n{error} Everything embedded so far is saved;\n"
              f"wait a few minutes and run this again to continue.")
        return 1
    print("\nIndex is up to date.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
