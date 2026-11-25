"""
Assignment 3: build the index (`main.py index`).

Corpus: 49 synthetic B2B contracts (corpus/CONTRACT_xxx.pdf).

    uv run python main.py index              # both chunking designs
    uv run python index.py --dry-run         # chunk only, no API calls
    uv run python index.py --design clause   # only one design

Pipeline per file: extract_pages -> parse_contract -> chunk_file (one of two
designs) -> embed_and_store. Each vector is saved to index/ (ChromaDB) as soon
as it is returned, and only chunks without a saved vector are embedded, so a
crash or the daily quota loses nothing and a second run costs nothing.

server.py and evaluate.py import the functions below: chunk_file,
embed_and_store, index_file, retrieve.
"""

import argparse
import hashlib
import json
import os
import re
import sys
import time
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"
QUERY_CACHE = INDEX_DIR / "query_cache.json"

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768            # truncated from 3072; the model re-normalises it
BATCH_SIZE = 32            # texts per request
SAVE_EVERY = 32            # chunks per write to disk

# Two chunking designs, compared in evaluate.py. ACTIVE_DESIGN is the one the
# server and the agent use (decided from the hit rates; see REPORT.md).
DESIGNS = ("clause", "window")
ACTIVE_DESIGN = "clause"

# clause design: one chunk per numbered clause; tiny clauses are merged with
# their neighbour, huge ones are split at a sub-clause boundary.
CLAUSE_MIN_WORDS = 60
CLAUSE_MAX_WORDS = 320
CLAUSE_MERGE_MAX_WORDS = 220   # a merged chunk stays below this
# window design: fixed windows of words with overlap, blind to structure.
WINDOW_WORDS = 200
WINDOW_STEP = 160


def log(*args) -> None:
    """stderr only: when the server imports this module, stdout carries MCP."""
    print(*args, file=sys.stderr, flush=True)


# --------------------------------------------------------------------------
# 1. Extract and clean
# --------------------------------------------------------------------------

HEAD_RE = re.compile(r"^(\d{1,2})\.\s+([A-Z].*)$")                 # "6. Liability"
SUB_RE = re.compile(r"^(\d{1,2})\.(\d{1,2})\s+\S")                  # "6.1 The ..."
SCHED_RE = re.compile(r"^(Schedule\s+\d+)\s+[—-]\s+(.*)$")         # "Schedule 1 — ..."
SIGN_RE = re.compile(r"^Signed for\b")
BULLET_RE = re.compile(r"^[\x7f-•·▪●]\s*")            # glyph the PDF uses for bullets


def extract_pages(path: Path) -> list[tuple[int, str]]:
    """Text of each page, in layout mode so table columns stay apart."""
    from pypdf import PdfReader

    reader = PdfReader(str(path))
    return [(i + 1, page.extract_text(extraction_mode="layout")) for i, page in enumerate(reader.pages)]


def clean_lines(pages: list[tuple[int, str]]) -> list[tuple[int, str, bool]]:
    """(page, line, is_continuation_of_table_cell). Drops blank lines and page noise."""
    out = []
    for page_no, text in pages:
        for raw in text.splitlines():
            if not raw.strip():
                continue
            indent = len(raw) - len(raw.lstrip())
            line = BULLET_RE.sub("- ", raw.strip())
            out.append((page_no, line, indent >= 20))
    return out


def parse_contract(path: Path) -> dict:
    """Split one contract PDF into title, parties and numbered clauses with pages.

    Returns {"source", "doc_id", "title", "parties", "date", "clauses": [...]},
    each clause {"id", "heading", "paras": [(page, text)], "kind": clause|schedule}.
    """
    lines = clean_lines(extract_pages(path))
    # Header = everything before "Effective Date:". Long titles wrap onto a second line, so the
    # title runs up to the line that completes "CONTRACT ID: NNN"; the rest is the parties line.
    eff = next(i for i, (_, l, _) in enumerate(lines) if l.startswith("Effective Date"))
    head = [l for _, l, _ in lines[:eff]]
    cut = next(i + 1 for i in range(len(head)) if re.search(r"CONTRACT ID:\s*\d{3}\s*$", " ".join(head[:i + 1])))
    title, parties = " ".join(head[:cut]), " ".join(head[cut:])
    date = lines[eff][1].split(":", 1)[1].strip()
    doc_id = re.search(r"(\d{3})", path.stem).group(1)

    clauses: list[dict] = []
    current: dict | None = None
    in_table = False
    for page_no, line, indented in lines[eff + 1:]:
        if SIGN_RE.match(line):
            in_table = False
            current = None                       # signature block carries no content
            continue
        m_sched = SCHED_RE.match(line)
        m_head = HEAD_RE.match(line)
        if m_sched:
            current = {"id": m_sched.group(1), "heading": m_sched.group(2), "paras": [], "kind": "schedule"}
            clauses.append(current)
            in_table = True
            continue
        if m_head and not SUB_RE.match(line) and not in_table:
            current = {"id": m_head.group(1), "heading": m_head.group(2).rstrip("."), "paras": [], "kind": "clause"}
            clauses.append(current)
            continue
        if current is None:
            continue
        if in_table:
            cells = [c.strip() for c in re.split(r"\s{3,}", line) if c.strip()]
            if indented and current["paras"]:                      # wrapped table cell
                page0, prev = current["paras"][-1]
                current["paras"][-1] = (page0, prev + " " + " ".join(cells))
            elif len(cells) > 1:
                current["paras"].append((page_no, ": ".join([cells[0], " ".join(cells[1:])])))
            elif current["paras"] and not indented and cells and not cells[0][0].isupper():
                page0, prev = current["paras"][-1]
                current["paras"][-1] = (page0, prev + " " + cells[0])
            else:
                current["paras"].append((page_no, cells[0] if cells else line))
            continue
        starts_new = bool(SUB_RE.match(line)) or line.startswith("- ")
        if starts_new or not current["paras"]:
            current["paras"].append((page_no, line))
        else:                                                     # wrapped line of the same paragraph
            page0, prev = current["paras"][-1]
            current["paras"][-1] = (page0, prev + " " + line)
    clauses = [c for c in clauses if c["paras"]]
    return {"source": path.name, "doc_id": doc_id, "title": title, "parties": parties, "date": date, "clauses": clauses}


# --------------------------------------------------------------------------
# 2. Chunk (two designs)
# --------------------------------------------------------------------------

def words(text: str) -> int:
    return len(text.split())


def _span(paras: list[tuple[int, str]]) -> str:
    """'6.1-6.3' from the sub-clause numbers at the start of each paragraph, else ''."""
    nums = [m.group(0).split()[0] for _, p in paras if (m := SUB_RE.match(p))]
    return nums[0] if len(nums) == 1 else (f"{nums[0]}-{nums[-1]}" if nums else "")


def _pages(paras: list[tuple[int, str]]) -> tuple[int, int]:
    return min(p for p, _ in paras), max(p for p, _ in paras)


def _chunk_record(doc: dict, design: str, location: str, text: str, page_start: int, page_end: int, extra: dict) -> dict:
    pages = f"p. {page_start}" if page_start == page_end else f"pp. {page_start}-{page_end}"
    chunk_id = f"{design}:{doc['doc_id']}:{hashlib.sha1(text.encode()).hexdigest()[:12]}"
    meta = {
        "source": doc["source"], "doc_id": doc["doc_id"], "contract": doc["title"],
        "design": design, "location": f"{location}, {pages}",
        "page_start": page_start, "page_end": page_end, "words": words(text),
    }
    meta.update(extra)
    return {"id": chunk_id, "text": text, "metadata": meta}


def chunk_clauses(doc: dict) -> list[dict]:
    """Design A: one chunk per clause, with the contract's name and parties in the text.

    Each chunk starts with 'CONTRACT 049 - <title> - <parties>' because a clause
    alone ('The Provider may suspend...') does not say whose contract it is.
    """
    header = f"{doc['title']}\n{doc['parties']}"
    # 1) split oversize clauses at sub-clause boundaries
    units: list[dict] = []
    for c in doc["clauses"]:
        label = c["id"] if c["kind"] == "schedule" else f"Clause {c['id']}"
        groups, cur = [], []
        for para in c["paras"]:
            if cur and sum(words(p) for _, p in cur) + words(para[1]) > CLAUSE_MAX_WORDS and SUB_RE.match(para[1]):
                groups.append(cur)
                cur = []
            cur.append(para)
        groups.append(cur)
        for g in groups:
            units.append({"label": label, "heading": c["heading"], "paras": g, "ids": [c["id"]]})
    # 2) merge tiny units into the next one (e.g. "9. Governing Law" with "10. General")
    merged: list[dict] = []
    for u in units:
        if merged and words(" ".join(p for _, p in merged[-1]["paras"])) < CLAUSE_MIN_WORDS \
                and merged[-1]["label"].startswith("Clause") == u["label"].startswith("Clause") \
                and words(" ".join(p for _, p in merged[-1]["paras"] + u["paras"])) <= CLAUSE_MERGE_MAX_WORDS:
            merged[-1]["paras"] += [(u["paras"][0][0], f"{u['label']}. {u['heading']}")] + u["paras"]
            merged[-1]["heading"] += " / " + u["heading"]
            merged[-1]["ids"] += u["ids"]
        else:
            merged.append(u)
    chunks = []
    for u in merged:
        paras = u["paras"]
        body = "\n".join(t for _, t in paras)
        text = f"{header}\n{u['label']}. {u['heading']}\n{body}"
        span = _span([x for x in paras if not x[1].startswith(("Clause ", "Schedule "))])
        name = u["label"] if len(u["ids"]) == 1 else (f"Clauses {u['ids'][0]}-{u['ids'][-1]}" if u["label"].startswith("Clause") else u["label"])
        loc = f"{name} ({u['heading']})" + (f", {span}" if span else "")
        p0, p1 = _pages(paras)
        chunks.append(_chunk_record(doc, "clause", loc, text, p0, p1, {"clause": ",".join(u["ids"])}))
    return chunks


def chunk_windows(doc: dict) -> list[dict]:
    """Design B: fixed windows of WINDOW_WORDS words (step WINDOW_STEP), no structure, no header."""
    tokens: list[tuple[str, int]] = []
    for c in doc["clauses"]:
        label = c["id"] if c["kind"] == "schedule" else f"{c['id']}."
        tokens.append((label, c["paras"][0][0]))
        tokens += [(w, p) for p, t in c["paras"] for w in t.split()]
    chunks, start = [], 0
    while start < len(tokens):
        window = tokens[start:start + WINDOW_WORDS]
        if start and len(window) < WINDOW_WORDS // 3:                    # tail already covered by the overlap
            break
        text = " ".join(w for w, _ in window)
        loc = f"words {start + 1}-{start + len(window)}"
        chunks.append(_chunk_record(doc, "window", loc, text, window[0][1], window[-1][1], {"clause": ""}))
        if start + WINDOW_WORDS >= len(tokens):
            break
        start += WINDOW_STEP
    return chunks


CHUNKERS = {"clause": chunk_clauses, "window": chunk_windows}


def chunk_file(path: Path, design: str = ACTIVE_DESIGN) -> list[dict]:
    """Extract, clean and chunk one PDF. No API call. Used by main() and by add_document."""
    return CHUNKERS[design](parse_contract(Path(path)))


# --------------------------------------------------------------------------
# 3. Embed and store
# --------------------------------------------------------------------------

_client = None
_collections: dict = {}


def genai_client():
    global _client
    if _client is None:
        from google import genai
        from api_key import load_api_key
        _client = genai.Client(api_key=load_api_key())
    return _client


def collection(design: str):
    """The ChromaDB collection of one design. Vectors are ours: Chroma never embeds."""
    if design not in _collections:
        import chromadb
        db = chromadb.PersistentClient(path=str(INDEX_DIR))
        _collections[design] = db.get_or_create_collection(f"contracts_{design}", metadata={"hnsw:space": "cosine"})
    return _collections[design]


class QuotaExhausted(RuntimeError):
    pass


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed texts with Gemini, one vector per text. Retries per-minute limits; the daily limit raises.

    Each text is wrapped in its own Content: a plain list would come back as ONE aggregated vector.
    """
    from google.genai import errors, types

    contents = [types.Content(parts=[types.Part(text=t)]) for t in texts]
    config = types.EmbedContentConfig(output_dimensionality=EMBED_DIM)
    for attempt in range(6):
        try:
            response = genai_client().models.embed_content(model=EMBED_MODEL, contents=contents, config=config)
            vectors = [list(e.values) for e in response.embeddings]
            if len(vectors) != len(texts):
                raise RuntimeError(f"asked for {len(texts)} embeddings, got {len(vectors)}")
            return vectors
        except errors.APIError as error:
            message = str(error)
            if getattr(error, "code", None) == 429:
                if "PerDay" in message or "per day" in message.lower():
                    raise QuotaExhausted(message) from error
                wait = 20 * (attempt + 1)
                log(f"  rate limit, waiting {wait}s ...")
                time.sleep(wait)
                continue
            if getattr(error, "code", 0) >= 500:
                time.sleep(5 * (attempt + 1))
                continue
            raise
    raise RuntimeError("Gemini kept refusing after 6 attempts")


def document_text(chunk: dict) -> str:
    """What is embedded: the format gemini-embedding-2 expects for documents."""
    title = chunk["metadata"]["contract"] if chunk["metadata"]["design"] == "clause" else "none"
    return f"title: {title} | text: {chunk['text']}"


def embed_and_store(chunks: list[dict], design: str) -> dict:
    """Embed only the chunks without a saved vector and save them in batches.

    Returns {"new": n, "existing": n}. Raises QuotaExhausted if the daily limit is hit
    (everything embedded up to then is already saved).
    """
    if not chunks:
        return {"new": 0, "existing": 0}
    col = collection(design)
    ids = [c["id"] for c in chunks]
    have = set(col.get(ids=ids, include=[])["ids"])
    todo = [c for c in chunks if c["id"] not in have]
    for i in range(0, len(todo), SAVE_EVERY):
        part = todo[i:i + SAVE_EVERY]
        vectors: list = []
        for j in range(0, len(part), BATCH_SIZE):
            vectors += embed_texts([document_text(c) for c in part[j:j + BATCH_SIZE]])
        col.upsert(
            ids=[c["id"] for c in part], embeddings=vectors,
            documents=[c["text"] for c in part], metadatas=[c["metadata"] for c in part],
        )
    return {"new": len(todo), "existing": len(chunks) - len(todo)}


def drop_stale(source: str, design: str, keep_ids: list[str]) -> int:
    """Remove chunks of this source that the current text no longer produces (edited file)."""
    col = collection(design)
    old = col.get(where={"source": source}, include=[])["ids"]
    stale = [i for i in old if i not in set(keep_ids)]
    if stale:
        col.delete(ids=stale)
    return len(stale)


def index_file(path: Path, design: str = ACTIVE_DESIGN) -> dict:
    """The whole pipeline for one file. Idempotent: a file already indexed costs 0 embeddings."""
    chunks = chunk_file(path, design)
    stale = drop_stale(Path(path).name, design, [c["id"] for c in chunks])
    result = embed_and_store(chunks, design)
    result.update({"source": Path(path).name, "chunks": len(chunks), "removed": stale})
    return result


# --------------------------------------------------------------------------
# 4. Retrieve (used by server.py and evaluate.py)
# --------------------------------------------------------------------------

def _load_query_cache() -> dict:
    """The query cache; a damaged file (two processes writing at once) is salvaged, never fatal."""
    if not QUERY_CACHE.exists():
        return {}
    text = QUERY_CACHE.read_text()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        try:                                   # keep the first complete JSON object, drop the garbage after it
            data, _ = json.JSONDecoder().raw_decode(text)
            return data if isinstance(data, dict) else {}
        except json.JSONDecodeError:
            return {}


def _save_query_cache(new_items: dict) -> None:
    """Merge with what other processes saved meanwhile, and replace the file atomically."""
    cache = _load_query_cache()
    cache.update(new_items)
    tmp = QUERY_CACHE.with_name(f"{QUERY_CACHE.name}.{os.getpid()}.tmp")
    tmp.write_text(json.dumps(cache))
    os.replace(tmp, QUERY_CACHE)


def embed_query(query: str) -> list[float]:
    """Embed a question; cached on disk so repeated evaluation runs cost no quota."""
    key = hashlib.sha1(f"{EMBED_MODEL}:{EMBED_DIM}:{query}".encode()).hexdigest()
    cache = _load_query_cache()
    if key not in cache:
        cache[key] = [round(x, 6) for x in embed_texts([f"task: search result | query: {query}"])[0]]
        _save_query_cache({key: cache[key]})
    return cache[key]


def retrieve(query: str, k: int = 5, design: str = ACTIVE_DESIGN) -> list[dict]:
    """Top-k chunks: [{"text", "metadata", "distance"}], best first."""
    col = collection(design)
    if col.count() == 0:
        return []
    res = col.query(query_embeddings=[embed_query(query)], n_results=min(k, col.count()),
                    include=["documents", "metadatas", "distances"])
    return [{"text": d, "metadata": m, "distance": x}
            for d, m, x in zip(res["documents"][0], res["metadatas"][0], res["distances"][0])]


# --------------------------------------------------------------------------
# 5. Command line
# --------------------------------------------------------------------------

def corpus_files() -> list[Path]:
    files = sorted(CORPUS_DIR.glob("*.pdf"))
    if not files:
        raise SystemExit(f"No PDFs in {CORPUS_DIR}. Copy the contracts there first.")
    return files


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the index from corpus/.")
    parser.add_argument("--design", choices=[*DESIGNS, "both"], default="both")
    parser.add_argument("--dry-run", action="store_true", help="chunk and count only; no API calls")
    args = parser.parse_args()
    designs = DESIGNS if args.design == "both" else (args.design,)
    files = corpus_files()

    for design in designs:
        started, total, new, existing = time.time(), 0, 0, 0
        chunks_by_file = {f: chunk_file(f, design) for f in files}
        total = sum(len(c) for c in chunks_by_file.values())
        wc = sum(c["metadata"]["words"] for cs in chunks_by_file.values() for c in cs)
        log(f"[{design}] {len(files)} files -> {total} chunks, {wc} words (avg {wc // max(total, 1)})")
        if args.dry_run:
            continue
        for f, chunks in chunks_by_file.items():
            try:
                drop_stale(f.name, design, [c["id"] for c in chunks])
                r = embed_and_store(chunks, design)
            except QuotaExhausted as error:
                log(f"\nDaily Gemini embedding quota reached while indexing {f.name}.\n"
                    f"Everything embedded so far is saved in index/. Run the same command again after the quota "
                    f"resets (09:00 in Spain) and it will continue where it stopped.\n{str(error)[:300]}")
                raise SystemExit(1)
            new, existing = new + r["new"], existing + r["existing"]
            if r["new"]:
                log(f"  {f.name}: {r['new']} embedded, {r['existing']} already saved")
        log(f"[{design}] done in {time.time() - started:.0f}s: {new} embedded, {existing} already saved, "
            f"{collection(design).count()} chunks in index/")


if __name__ == "__main__":
    main()
