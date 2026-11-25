"""
Assignment 3: build the index (`main.py index`).

Corpus: three UK statutory instruments from legislation.gov.uk (Open Government
Licence v3.0). We keep only the <Body> (the regulations themselves) and skip
schedules, commentaries and explanatory notes.

Chunking: structure-based. One chunk per regulation; a regulation longer than
MAX_WORDS is split at its numbered paragraphs. Every chunk carries its source
document, regulation number, part, title and a URL.

Embedding: Gemini. Vectors are saved to ChromaDB (index/) after every batch,
and only chunks without a saved vector are embedded.

Functions used by server.py: index_file(path), embed_query(text), get_collection().

Test without spending any embedding quota:  uv run python index.py --dry-run
"""

import hashlib
import re
import sys
import time
import urllib.request
import xml.etree.ElementTree as ET
from pathlib import Path

ROOT = Path(__file__).resolve().parent
RAW_DIR = ROOT / "corpus" / "raw"
INDEX_DIR = ROOT / "index"
COLLECTION = "corpus"
EMBED_MODEL = "gemini-embedding-2"
MAX_WORDS = 300
BATCH = 20

# name -> (legislation.gov.uk path, human title)
CORPUS = {
    "money_laundering_regs_2017": ("uksi/2017/692", "Money Laundering, Terrorist Financing and Transfer of Funds Regulations 2017"),
    "payment_services_regs_2017": ("uksi/2017/752", "Payment Services Regulations 2017"),
    "electronic_money_regs_2011": ("uksi/2011/99", "Electronic Money Regulations 2011"),
}


# --------------------------------------------------------------------------
# Download
# --------------------------------------------------------------------------
def download_corpus() -> None:
    RAW_DIR.mkdir(parents=True, exist_ok=True)
    for name, (path, _) in CORPUS.items():
        target = RAW_DIR / f"{name}.xml"
        if target.exists():
            continue
        url = f"https://www.legislation.gov.uk/{path}/data.xml"
        req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (course assignment)"})
        target.write_bytes(urllib.request.urlopen(req, timeout=60).read())
        print(f"downloaded {name}", file=sys.stderr)


# --------------------------------------------------------------------------
# Extraction and chunking
# --------------------------------------------------------------------------
def local(el: ET.Element) -> str:
    return el.tag.split("}")[-1]


def clean(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def words(text: str) -> int:
    return len(text.split())


def text_of(el: ET.Element, skip: tuple[str, ...] = ()) -> str:
    """All text under el, leaving out child elements whose tag is in skip."""
    parts = [el.text or ""]
    for child in el:
        if local(child) not in skip:
            parts.append(text_of(child, skip))
        parts.append(child.tail or "")
    return clean(" ".join(parts))


def child_text(el: ET.Element, tag: str) -> str:
    for child in el:
        if local(child) == tag:
            return clean(text_of(child))
    return ""


def split_long(text: str) -> list[str]:
    """Last resort: cut a very long block into MAX_WORDS pieces."""
    w = text.split()
    return [" ".join(w[i:i + MAX_WORDS]) for i in range(0, len(w), MAX_WORDS)]


def split_regulation(p1: ET.Element) -> list[tuple[str, str]]:
    """Split a long regulation at its numbered paragraphs.

    Returns [(label, text)], where label is e.g. "(1)-(3)" or "" for one piece.
    """
    container = p1
    children = [c for c in p1 if local(c) != "Pnumber"]
    if len(children) == 1 and local(children[0]) == "P1para":
        container = children[0]
    units: list[tuple[str, str]] = []
    for child in container:
        if local(child) in ("Pnumber", "Title"):
            continue
        label = f"({child_text(child, 'Pnumber')})" if local(child) == "P2" and child_text(child, "Pnumber") else ""
        body = text_of(child, skip=("CommentaryRef",))
        if body:
            units.append((label, body))
    if not units:
        return [("", text)] if (text := text_of(p1, skip=("CommentaryRef",))) else []

    pieces: list[tuple[str, str]] = []
    cur_labels: list[str] = []
    cur_text: list[str] = []
    cur_words = 0

    def flush() -> None:
        nonlocal cur_labels, cur_text, cur_words
        if cur_text:
            labels = [l for l in cur_labels if l]
            label = labels[0] if len(labels) == 1 else (f"{labels[0]}-{labels[-1]}" if labels else "")
            pieces.append((label, " ".join(cur_text)))
        cur_labels, cur_text, cur_words = [], [], 0

    for label, body in units:
        n = words(body)
        if n > MAX_WORDS:
            flush()
            for part in split_long(body):
                pieces.append((label, part))
            continue
        if cur_words + n > MAX_WORDS:
            flush()
        cur_labels.append(label)
        cur_text.append(body)
        cur_words += n
    flush()
    return pieces


def walk(el: ET.Element, ctx: dict, out: list[dict]) -> None:
    """Depth-first walk of <Body>, tracking the current Part/Chapter/title."""
    tag = local(el)
    if tag == "Part":
        ctx = {**ctx, "part": f"Part {child_text(el, 'Number').replace('PART', '').strip()} {child_text(el, 'Title')}".strip()}
    elif tag == "P1group":
        ctx = {**ctx, "title": child_text(el, "Title")}
    elif tag == "P1":
        number = child_text(el, "Pnumber").rstrip(". ")
        full = text_of(el, skip=("CommentaryRef",))
        if number and full:
            if words(full) <= MAX_WORDS:
                pieces = [("", full)]
            else:
                pieces = split_regulation(el)
            for label, body in pieces:
                out.append({**ctx, "number": number, "label": label, "text": body})
        return
    for child in el:
        walk(child, ctx, out)


def chunk_legislation(path: Path, doc_title: str | None = None) -> list[dict]:
    """Chunks from a legislation.gov.uk XML file, with citations."""
    root = ET.parse(path).getroot()
    doc_name = path.stem
    title = doc_title or CORPUS.get(doc_name, ("", ""))[1] or next(
        (clean(e.text) for e in root.iter() if local(e) == "title" and e.text and clean(e.text)), doc_name)
    bodies = [el for el in root.iter() if local(el) == "Body"]
    raw: list[dict] = []
    for body in bodies:
        walk(body, {"part": "", "title": ""}, raw)

    chunks = []
    seen: dict[str, int] = {}
    for r in raw:
        base = f"{doc_name}:reg{r['number']}"
        seen[base] = seen.get(base, 0) + 1
        location = f"regulation {r['number']}{r['label']}" if r["label"] else f"regulation {r['number']}"
        header = f"{title}, {location}" + (f" - {r['title']}" if r["title"] else "")
        chunks.append({
            "id": f"{base}:{seen[base]}",
            "source": doc_name,
            "location": location,
            "part": r["part"],
            "heading": r["title"],
            "text": f"{header}\n{r['text']}",
        })
    return chunks


def chunk_plain(path: Path) -> list[dict]:
    """Chunks for .txt/.md (by paragraph blocks) and .pdf (by page)."""
    doc_name = path.stem
    chunks = []
    if path.suffix.lower() == ".pdf":
        from pypdf import PdfReader
        for page_no, page in enumerate(PdfReader(str(path)).pages, start=1):
            text = clean(page.extract_text() or "")
            for i, piece in enumerate(split_long(text) if text else [], start=1):
                chunks.append({"id": f"{doc_name}:p{page_no}:{i}", "source": doc_name,
                               "location": f"page {page_no}", "part": "", "heading": "",
                               "text": f"{doc_name}, page {page_no}\n{piece}"})
        return chunks
    blocks = [clean(b) for b in re.split(r"\n\s*\n", path.read_text(encoding="utf-8", errors="ignore")) if clean(b)]
    cur, n, idx = [], 0, 0
    for block in blocks + [None]:
        if block is None or (n + words(block) > MAX_WORDS and cur):
            idx += 1
            chunks.append({"id": f"{doc_name}:s{idx}", "source": doc_name, "location": f"section {idx}",
                           "part": "", "heading": "", "text": f"{doc_name}, section {idx}\n" + " ".join(cur)})
            cur, n = [], 0
        if block is not None:
            cur.append(block)
            n += words(block)
    return chunks


def chunk_file(path: Path) -> list[dict]:
    """Extract, clean and chunk one file. Used by main index and by add_document."""
    path = Path(path)
    if path.suffix.lower() == ".xml":
        return chunk_legislation(path)
    if path.suffix.lower() in (".txt", ".md", ".pdf"):
        return chunk_plain(path)
    raise ValueError(f"Unsupported file type {path.suffix!r}; use .xml, .pdf, .txt or .md")


# --------------------------------------------------------------------------
# Embedding and storage
# --------------------------------------------------------------------------
def get_collection():
    import chromadb
    client = chromadb.PersistentClient(path=str(INDEX_DIR))
    return client.get_or_create_collection(COLLECTION, metadata={"hnsw:space": "cosine"})


def _client():
    from google import genai
    from api_key import load_api_key
    return genai.Client(api_key=load_api_key())


def embed_texts(texts: list[str], client=None) -> list[list[float]]:
    """One vector per text. gemini-embedding-2 merges a list into ONE vector, so go one by one."""
    client = client or _client()
    return [_embed_one(t, client) for t in texts]


def _embed_one(text: str, client) -> list[float]:
    for attempt in range(6):
        try:
            res = client.models.embed_content(model=EMBED_MODEL, contents=text)
            return list(res.embeddings[0].values)
        except Exception as error:  # noqa: BLE001
            msg = str(error)
            if "PerDay" in msg or "per day" in msg.lower():
                raise SystemExit("Daily embedding limit reached. Vectors saved so far are kept; run again after 09:00 (Spain).")
            if "429" in msg or "RESOURCE_EXHAUSTED" in msg or "503" in msg:
                wait = 20 * (attempt + 1)
                print(f"rate limited, waiting {wait}s", file=sys.stderr)
                time.sleep(wait)
                continue
            raise
    raise SystemExit("Embedding kept failing; vectors saved so far are kept.")


def embed_query(text: str) -> list[float]:
    return embed_texts([text])[0]


def digest(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:16]


def embed_and_store(chunks: list[dict]) -> dict:
    """Embed only chunks without a saved vector (or whose text changed); save each batch at once."""
    col = get_collection()
    existing = {}
    ids = [c["id"] for c in chunks]
    for i in range(0, len(ids), 500):
        got = col.get(ids=ids[i:i + 500], include=["metadatas"])
        existing.update({cid: (m or {}).get("hash") for cid, m in zip(got["ids"], got["metadatas"])})

    todo = [c for c in chunks if existing.get(c["id"]) != digest(c["text"])]
    stats = {"total": len(chunks), "already_indexed": len(chunks) - len(todo), "embedded": 0}
    if not todo:
        return stats
    client = _client()
    for i in range(0, len(todo), BATCH):
        batch = todo[i:i + BATCH]
        vectors = embed_texts([c["text"] for c in batch], client)
        col.upsert(
            ids=[c["id"] for c in batch],
            embeddings=vectors,
            documents=[c["text"] for c in batch],
            metadatas=[{"source": c["source"], "location": c["location"], "part": c["part"],
                        "heading": c["heading"], "hash": digest(c["text"])} for c in batch],
        )
        stats["embedded"] += len(batch)
        print(f"  embedded {stats['embedded']}/{len(todo)}", file=sys.stderr)
    return stats


def index_file(path: str | Path) -> dict:
    """The whole pipeline for one file (add_document calls this)."""
    return embed_and_store(chunk_file(Path(path)))


# --------------------------------------------------------------------------
# Script
# --------------------------------------------------------------------------
def main() -> None:
    dry = "--dry-run" in sys.argv
    download_corpus()
    all_chunks: list[dict] = []
    for name in CORPUS:
        chunks = chunk_file(RAW_DIR / f"{name}.xml")
        wc = sum(words(c["text"]) for c in chunks)
        print(f"{name}: {len(chunks)} chunks, {wc:,} words")
        all_chunks += chunks
    print(f"TOTAL: {len(all_chunks)} chunks, {sum(words(c['text']) for c in all_chunks):,} words")
    if dry:
        import random
        for c in random.Random(1).sample(all_chunks, 3):
            print("\n---", c["id"], "|", c["location"], "|", c["part"], "\n", c["text"][:500])
        return
    print(embed_and_store(all_chunks))
    print(f"index now holds {get_collection().count()} chunks")


if __name__ == "__main__":
    main()
