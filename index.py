"""
Assignment 3: build the index (`main.py index`).

Downloads the corpus into corpus/, extracts and cleans the text, chunks it with
every design in config.CHUNKINGS, embeds with Gemini and stores the vectors in
index/chroma/. Vectors are saved after every batch, and only chunks without a
saved vector are embedded, so a crash or the daily quota loses nothing: run it
again and it carries on.

server.py's add_document tool imports `add_file()` from here.
All progress goes to stderr (stdout carries the MCP protocol in server.py).
"""

import hashlib
import json
import re
import sys
import time
import unicodedata
from pathlib import Path

import config as C


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


class QuotaExhausted(RuntimeError):
    """The embedding API's daily free-tier limit was reached."""


# ===========================================================================
# 1. Download
# ===========================================================================
def download(doc: dict, folder: Path) -> Path:
    import httpx

    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{doc['doc_id']}.pdf"
    if path.exists() and path.stat().st_size > 0:
        return path
    log(f"Downloading {doc['url']}")
    try:
        r = httpx.get(doc["url"], follow_redirects=True, timeout=120,
                      headers={"User-Agent": "Mozilla/5.0 (course assignment; RAG indexer)"})
        r.raise_for_status()
        if not r.content.startswith(b"%PDF"):
            raise ValueError("response is not a PDF")
    except Exception as e:  # noqa: BLE001
        raise SystemExit(
            f"Could not download {doc['url']}: {e}\n"
            f"Download it in a browser and save it as {path}, then run again."
        )
    path.write_bytes(r.content)
    return path


# ===========================================================================
# 2. Extract and clean
# ===========================================================================
PAGE_LABEL = re.compile(r"^\d{1,2}-\d{1,3}$")          # PHAK footer, e.g. "15-3"
LIGATURES = {"ﬁ": "fi", "ﬂ": "fl", "ﬀ": "ff", "ﬃ": "ffi", "ﬄ": "ffl"}


def normalise(text: str) -> str:
    for a, b in LIGATURES.items():
        text = text.replace(a, b)
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("•", "-").replace("­", "")   # bullets, soft hyphens
    return text


def extract_pages(path: Path) -> list[tuple[str, list[str]]]:
    """[(page label, cleaned lines)] for a PDF, .txt, .md or .html file."""
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        from pypdf import PdfReader

        pages = []
        for n, page in enumerate(PdfReader(str(path)).pages, start=1):
            lines = [l.strip() for l in normalise(page.extract_text() or "").splitlines()]
            lines = [l for l in lines if l]
            # The printed page number ("15-3") sits on its own line in the footer.
            # Use it as the location and drop it from the text.
            label = next((l for l in reversed(lines) if PAGE_LABEL.match(l)), None) \
                or next((l for l in lines if PAGE_LABEL.match(l)), None)
            lines = [l for l in lines if not PAGE_LABEL.match(l)]
            pages.append((label or f"pdf{n}", lines))
        return pages
    if suffix in {".html", ".htm"}:
        from bs4 import BeautifulSoup

        text = BeautifulSoup(path.read_text(encoding="utf-8", errors="ignore"), "html.parser").get_text("\n")
    elif suffix in {".txt", ".md"}:
        text = path.read_text(encoding="utf-8", errors="ignore")
    else:
        raise ValueError(f"Unsupported file type {suffix!r}: use .pdf, .txt, .md or .html")
    lines = [l.strip() for l in normalise(text).splitlines() if l.strip()]
    return [("1", lines)]


SENTENCE_END = (".", ":", ";", "?", "!", ")", '"')


def title_like(line: str) -> bool:
    """A short Title-Case line with no sentence punctuation at the end."""
    words = line.split()
    if not (1 <= len(words) <= 9) or len(line) > 70:
        return False
    if line.endswith(SENTENCE_END + (",", "-")) or not line[0].isupper():
        return False
    if line.lower().startswith(("figure", "table", "chapter summary")) and not line.lower() == "chapter summary":
        return False
    long_words = [w for w in words if len(w) >= 4]
    return not (long_words and sum(w[0].isupper() for w in long_words) / len(long_words) < 0.6)


def is_heading(line: str, prev: str | None, nxt: str | None) -> bool:
    """Heuristic heading detector for PDF text, which has no markup.

    A heading is a short Title-Case line, after the end of a sentence, a page
    start or another heading, followed by a line that starts with a capital.
    """
    if line.startswith("#"):                      # markdown
        return True
    if not title_like(line):
        return False
    if prev is not None and not (prev.endswith(SENTENCE_END) or title_like(prev)):
        return False
    if nxt is not None and not nxt[0].isupper():
        return False
    return True


def to_sections(pages: list[tuple[str, list[str]]], doc_title: str) -> list[dict]:
    """Split the document into sections: [{"heading", "tokens": [(word, page)]}].

    Also rejoins words hyphenated across line ends ("con-" + "trolled").
    """
    sections = [{"heading": doc_title, "tokens": []}]
    flat = [(label, line) for label, lines in pages for line in lines]
    for i, (label, line) in enumerate(flat):
        prev = flat[i - 1][1] if i > 0 else None
        nxt = flat[i + 1][1] if i + 1 < len(flat) else None
        if is_heading(line, prev, nxt):
            sections.append({"heading": line.lstrip("# ").strip(), "tokens": []})
            continue
        tokens = sections[-1]["tokens"]
        for word in line.split():
            if tokens and tokens[-1][0].endswith("-") and len(tokens[-1][0]) > 1 and word[:1].islower():
                tokens[-1] = (tokens[-1][0][:-1] + word, tokens[-1][1])
            else:
                tokens.append((word, label))
    return [s for s in sections if s["tokens"]]


# ===========================================================================
# 3. Chunk
# ===========================================================================
def _windows(n: int, size: int, overlap: int):
    step = max(size - overlap, 1)
    start = 0
    while start < n:
        yield start, min(start + size, n)
        if start + size >= n:
            break
        start += step


def _chunk(doc: dict, design: str, text: str, tokens: list, section: str, n: int) -> dict:
    pages = list(dict.fromkeys(p for _, p in tokens))
    cid = hashlib.sha1(f"{design}|{doc['doc_id']}|{text}".encode()).hexdigest()[:16]
    return {
        "id": f"{design}-{doc['doc_id']}-{n:04d}-{cid}",
        "text": text,
        "metadata": {
            "doc_id": doc["doc_id"], "title": doc["title"], "url": doc.get("url", ""),
            "pages": ",".join(pages), "page": pages[0], "section": section,
            "design": design, "words": len(tokens), "position": n,
        },
    }


def chunk_sections(sections: list[dict], doc: dict, design: str) -> list[dict]:
    spec = C.CHUNKINGS[design]
    chunks = []
    if spec["kind"] == "fixed":
        tokens = [(w, p, s["heading"]) for s in sections for w, p in s["tokens"]]
        for a, b in _windows(len(tokens), spec["size"], spec["overlap"]):
            window = tokens[a:b]
            text = " ".join(w for w, _, _ in window)
            chunks.append(_chunk(doc, design, text, [(w, p) for w, p, _ in window], window[0][2], len(chunks)))
        return chunks

    # section: never cross a heading; merge tiny sections into the next one
    pending = None
    for s in sections:
        if pending:
            s = {"heading": pending["heading"], "tokens": pending["tokens"] + s["tokens"]}
            pending = None
        if len(s["tokens"]) < spec["min_words"]:
            pending = s
            continue
        for a, b in _windows(len(s["tokens"]), spec["max_words"], spec["overlap"]):
            window = s["tokens"][a:b]
            # The heading path goes into the text, so it is embedded and shown to the model.
            text = f"{doc['title']} > {s['heading']}\n" + " ".join(w for w, _ in window)
            chunks.append(_chunk(doc, design, text, window, s["heading"], len(chunks)))
    if pending:
        text = f"{doc['title']} > {pending['heading']}\n" + " ".join(w for w, _ in pending["tokens"])
        chunks.append(_chunk(doc, design, text, pending["tokens"], pending["heading"], len(chunks)))
    return chunks


def chunk_file(path: Path, doc: dict, design: str) -> tuple[list[dict], int]:
    """(chunks, word count) for one file under one chunking design."""
    sections = to_sections(extract_pages(Path(path)), doc["title"])
    words = sum(len(s["tokens"]) for s in sections)
    return chunk_sections(sections, doc, design), words


# ===========================================================================
# 4. Embed and store
# ===========================================================================
_client = None


def gemini():
    global _client
    if _client is None:
        from google import genai
        from api_key import load_api_key

        _client = genai.Client(api_key=load_api_key())
    return _client


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed a batch with retries. Raises QuotaExhausted at the daily limit."""
    for attempt in range(6):
        try:
            result = gemini().models.embed_content(model=C.EMBED_MODEL, contents=texts)
            return [e.values for e in result.embeddings]
        except Exception as e:  # noqa: BLE001
            msg = str(e)
            if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
                if "PerDay" in msg or "per day" in msg.lower():
                    raise QuotaExhausted(msg) from e
                wait = 15 * (attempt + 1)
                log(f"  rate limited, waiting {wait}s")
                time.sleep(wait)
                continue
            if attempt < 2 and ("500" in msg or "503" in msg or "timed out" in msg.lower()):
                time.sleep(5)
                continue
            raise
    raise QuotaExhausted("still rate limited after 6 retries")


def collection(design: str):
    import chromadb

    C.CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    client = chromadb.PersistentClient(path=str(C.CHROMA_DIR))
    return client.get_or_create_collection(f"faa_{design}", metadata={"hnsw:space": "cosine"})


def embed_and_store(chunks: list[dict], design: str) -> int:
    """Store chunks that have no saved vector yet. Returns how many were embedded."""
    col = collection(design)
    existing = set(col.get(ids=[c["id"] for c in chunks], include=[])["ids"]) if chunks else set()
    todo = [c for c in chunks if c["id"] not in existing]
    for i in range(0, len(todo), C.EMBED_BATCH):
        batch = todo[i:i + C.EMBED_BATCH]
        vectors = embed_texts([c["text"] for c in batch])
        col.add(ids=[c["id"] for c in batch], documents=[c["text"] for c in batch],
                metadatas=[c["metadata"] for c in batch], embeddings=vectors)
        log(f"  [{design}] embedded {min(i + C.EMBED_BATCH, len(todo))}/{len(todo)}")
        time.sleep(1)
    return len(todo)


def remove_stale(design: str, doc_id: str, keep_ids: set[str]) -> int:
    """Delete chunks of this document that the current chunking no longer produces."""
    col = collection(design)
    ids = col.get(where={"doc_id": doc_id}, include=[])["ids"]
    stale = [i for i in ids if i not in keep_ids]
    if stale:
        col.delete(ids=stale)
    return len(stale)


def file_hash(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_registry() -> dict:
    return json.loads(C.DOCS_REGISTRY.read_text()) if C.DOCS_REGISTRY.exists() else {}


def save_registry(reg: dict) -> None:
    C.DOCS_REGISTRY.parent.mkdir(parents=True, exist_ok=True)
    C.DOCS_REGISTRY.write_text(json.dumps(reg, indent=2, ensure_ascii=False))


def index_document(path: Path, doc: dict, designs: list[str]) -> dict:
    """Chunk, embed and store one document under each design. Returns stats."""
    stats = {"doc_id": doc["doc_id"], "chunks": {}, "embedded": 0}
    for design in designs:
        chunks, words = chunk_file(path, doc, design)
        stats["words"] = words
        stats["chunks"][design] = len(chunks)
        stats["embedded"] += embed_and_store(chunks, design)
        removed = remove_stale(design, doc["doc_id"], {c["id"] for c in chunks})
        if removed:
            log(f"  [{design}] removed {removed} stale chunks of {doc['doc_id']}")
    return stats


# ===========================================================================
# 5. Add one document (used by server.py's add_document tool)
# ===========================================================================
def add_file(path: str | Path, designs: list[str] | None = None) -> str:
    """Index one new file. Policy for a document that is already indexed:

    - same doc_id and same file contents  -> nothing is embedded; say so.
    - same doc_id, different contents     -> treated as a new version: its
      chunks are re-embedded and the old version's chunks are deleted.
    - new doc_id                          -> indexed.
    doc_id is the file name without extension (e.g. phak-ch14).
    """
    path = Path(path).expanduser().resolve()
    if not path.is_file():
        return f"Error: no file at {path}."
    designs = designs or [C.ACTIVE_CHUNKING]
    doc_id = re.sub(r"[^a-z0-9\-]+", "-", path.stem.lower()).strip("-")
    reg = load_registry()
    digest = file_hash(path)
    known = reg.get(doc_id)
    if known and known.get("sha256") == digest and all(d in known.get("designs", []) for d in designs):
        return (f"Already indexed: {doc_id} ({known['words']} words, "
                f"{known['chunks']} chunks). Same contents, so nothing was embedded.")
    extra = {d["doc_id"]: d for d in C.EXTRA_DOCS + C.CORPUS}
    doc = {"doc_id": doc_id, "title": extra.get(doc_id, {}).get("title", path.stem),
           "url": extra.get(doc_id, {}).get("url", str(path.name))}
    try:
        stats = index_document(path, doc, designs)
    except QuotaExhausted:
        return "Error: the embedding API's daily limit is reached. Progress is saved; try again after 09:00 (Spain)."
    except ValueError as e:
        return f"Error: {e}"
    reg[doc_id] = {"title": doc["title"], "url": doc["url"], "licence": known.get("licence", "") if known else "",
                   "sha256": digest, "words": stats["words"],
                   "chunks": stats["chunks"][designs[0]], "designs": designs}
    save_registry(reg)
    action = "Updated (new version replaced the old one)" if known else "Added"
    return (f"{action}: {doc_id}, {stats['words']} words, {stats['chunks'][designs[0]]} chunks, "
            f"{stats['embedded']} newly embedded. Cite it as [{doc_id} p.PAGE].")


# ===========================================================================
# main.py index
# ===========================================================================
def main() -> int:
    reg = load_registry()
    total_words, embedded = 0, 0
    for doc in C.EXTRA_DOCS:
        download(doc, C.EXTRA_DIR)
    designs = list(C.CHUNKINGS)
    # Embed the active design first, so it is usable even if the quota runs out.
    designs.sort(key=lambda d: d != C.ACTIVE_CHUNKING)
    try:
        for doc in C.CORPUS:
            path = download(doc, C.CORPUS_DIR)
            log(f"{doc['doc_id']}: indexing")
            stats = index_document(path, doc, designs)
            total_words += stats["words"]
            embedded += stats["embedded"]
            reg[doc["doc_id"]] = {"title": doc["title"], "url": doc["url"], "licence": C.LICENCE,
                                  "sha256": file_hash(path), "words": stats["words"],
                                  "chunks": stats["chunks"][C.ACTIVE_CHUNKING], "designs": designs,
                                  "chunks_per_design": stats["chunks"]}
            save_registry(reg)
            log(f"{doc['doc_id']}: {stats['words']} words, chunks {stats['chunks']}, embedded {stats['embedded']}")
    except QuotaExhausted:
        log("\nDaily embedding limit reached. Everything embedded so far is saved in index/.\n"
            "Run `uv run python main.py index` again after 09:00 (Spain) to finish.")
        return 2

    log(f"\nCorpus: {len(C.CORPUS)} documents, {total_words:,} words "
        f"({'OK' if total_words >= 50_000 else 'BELOW the 50,000 required: add a document to config.CORPUS'}).")
    for d in designs:
        log(f"  {d}: {collection(d).count()} chunks stored")
    log(f"Embedded {embedded} new chunks this run.")
    return 0


def show(doc_id: str, n: int = 6) -> None:
    """Print the first chunks of one document under each design (no embedding)."""
    doc = next(d for d in C.CORPUS + C.EXTRA_DOCS if d["doc_id"] == doc_id)
    folder = C.EXTRA_DIR if doc in C.EXTRA_DOCS else C.CORPUS_DIR
    path = download(doc, folder)
    for design in C.CHUNKINGS:
        chunks, words = chunk_file(path, doc, design)
        print(f"\n===== {design}: {len(chunks)} chunks, {words} words")
        for c in chunks[:n]:
            m = c["metadata"]
            print(f"\n--- section: {m['section']} | pages: {m['pages']} | {m['words']} words\n{c['text'][:600]}")


if __name__ == "__main__":
    if len(sys.argv) == 3 and sys.argv[1] == "--show":
        show(sys.argv[2])
        sys.exit(0)
    sys.exit(main())
