"""
Assignment 3: build the index (`main.py index`).

Corpus: EU AI Act, GDPR and the Commission's guidelines on the AI system
definition, for hotel managers and compliance officers deciding whether a
guest-facing AI tool is allowed.

Pipeline (each step is a function, so server.py's add_document tool reuses it):
    download_corpus()      fetch the PDFs into corpus/ (git-ignored)
    parse_document(path)   extract text, strip page furniture, split into units
                           (articles, annexes, numbered sections) and paragraphs
    chunk_fixed / chunk_structure   the two chunking designs we compare
    embed_and_store(...)   embed only chunks without a saved vector, save each
                           batch to Chroma straight away (index/chroma)
    retrieve(...)          vector search, or vector + BM25 ("hybrid")

Run:  uv run python index.py [--dry-run] [--design fixed|structure|both]
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import re
import sys
import time
from collections import Counter
from pathlib import Path

import numpy as np

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
EXTRA_DIR = ROOT / "extra"          # documents added later with add_document (demo)
INDEX_DIR = ROOT / "index"
CHROMA_DIR = INDEX_DIR / "chroma"
REGISTRY_FILE = INDEX_DIR / "documents.json"
CONFIG_FILE = INDEX_DIR / "config.json"
QUERY_CACHE_FILE = INDEX_DIR / "query_cache.json"

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768
BATCH = 16

FIXED_WORDS, FIXED_OVERLAP = 350, 50      # design A: fixed-size windows
STRUCT_MAX_WORDS = 450                    # design B: one unit, split only if longer

DESIGNS = ("fixed", "structure")

# Where each document comes from. Licence: EU legal acts and Commission
# documents may be reused with attribution (Commission Decision 2011/833/EU,
# CC BY 4.0).
DOCS = {
    "ai_act": dict(
        title="AI Act (Regulation (EU) 2024/1689)",
        url="https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=OJ:L_202401689",
        date="2024-06-13",
        licence="EU legal act, reuse under Commission Decision 2011/833/EU (CC BY 4.0)",
    ),
    "gdpr": dict(
        title="GDPR (Regulation (EU) 2016/679)",
        url="https://eur-lex.europa.eu/legal-content/EN/TXT/PDF/?uri=CELEX:32016R0679",
        date="2016-04-27",
        licence="EU legal act, reuse under Commission Decision 2011/833/EU (CC BY 4.0)",
    ),
    "ai_system_definition_guidelines": dict(
        title="Commission Guidelines on the definition of an AI system (C(2025) 5053)",
        url="https://ec.europa.eu/newsroom/dae/redirection/document/112455",
        date="2025-07-29",
        licence="Commission document, reuse under Commission Decision 2011/833/EU (CC BY 4.0)",
    ),
    "prohibited_practices_guidelines": dict(
        title="Commission Guidelines on prohibited AI practices (C(2025) 5052)",
        url="https://ec.europa.eu/newsroom/dae/redirection/document/112367",
        date="2025-07-29",
        licence="Commission document, reuse under Commission Decision 2011/833/EU (CC BY 4.0)",
    ),
}
INITIAL = ["ai_act", "gdpr", "ai_system_definition_guidelines"]
EXTRA = ["prohibited_practices_guidelines"]


def log(*a):
    print(*a, file=sys.stderr, flush=True)


# --------------------------------------------------------------------------
# Download
# --------------------------------------------------------------------------

def download_corpus(names=INITIAL, folder: Path = CORPUS_DIR) -> list[Path]:
    """Download the PDFs that are missing. Returns the local paths."""
    import httpx

    folder.mkdir(exist_ok=True)
    paths = []
    for name in names:
        path = folder / f"{name}.pdf"
        if not path.exists():
            log(f"downloading {name} ...")
            r = httpx.get(DOCS[name]["url"], follow_redirects=True, timeout=120)
            r.raise_for_status()
            if not r.content.startswith(b"%PDF"):
                raise RuntimeError(f"{DOCS[name]['url']} did not return a PDF")
            path.write_bytes(r.content)
        paths.append(path)
    return paths


# --------------------------------------------------------------------------
# Extraction and cleaning
# --------------------------------------------------------------------------

# Page furniture of the Official Journal and of Commission documents.
FURNITURE = [
    r"^OJ L, 12\.7\.2024\s+EN\s*$",
    r"^EN\s+OJ L, 12\.7\.2024\s*$",
    r"^(?:\d+/\d+\s+)?ELI: http\S+(?:\s+\d+/\d+)?\s*$",
    r"^\d+\.\d+\.\d{4}\s+EN\s+Official Journal of the European Union\s+L \d+/\d+\s*$",
    r"^\d+\.\d+\.\d{4}\s+L \d+/\d+\s+Official Journal of the European Union\s+EN\s*$",
    r"^L \d+/\d+\s+EN\s+Official Journal of the European Union\s+\d+\.\d+\.\d{4}\s*$",
    r"^Official Journal\s*$", r"^of the European Union\s*$", r"^L series\s*$",
    r"^2024/1689\s+12\.7\.2024\s*$", r"^EN\s*$",
    r"^\d{1,3}\s*$",                       # lone page numbers (Commission documents)
    r"^\(\d+\)\s.*\(OJ [LC] .*$",          # footnote citing the Official Journal
    r".*\.{5,}.*",                         # table-of-contents lines
]
FURNITURE_RE = [re.compile(p) for p in FURNITURE]

ARTICLE_RE = re.compile(r"^Article (\d+[a-z]?)\s*$")
ANNEX_RE = re.compile(r"^ANNEX ([IVX]+)\s*$")
CHAPTER_RE = re.compile(r"^CHAPTER ([IVX]+)\s*$")
SECTION_RE = re.compile(r"^SECTION (\d+)\s*$")
HEADING_RE = re.compile(r"^(\d+(?:\.\d+){0,3})\.\s+([A-Z‘'(].{2,150})$")
PART_RE = re.compile(r"^([IVX]+)\.\s+([A-Z].{3,150})$")
FOOTNOTE_RE = re.compile(
    r"^\d{1,3} (Article|Articles|Regulation|Directive|Recital|Recitals|Ibid|See|Judgment|Case|"
    r"Commission|Council|European|Communication|OJ)\b")
PARA_RE = re.compile(r"^(?:(\d+)\.|\((\d+)\))\s+\S")


def extract_pages(path: Path) -> list[tuple[int, list[str]]]:
    """(page number, cleaned lines) for each page of a pdf, txt, md or html file."""
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        from pypdf import PdfReader

        raw = [(i + 1, p.extract_text() or "") for i, p in enumerate(PdfReader(str(path)).pages)]
    elif suffix in (".html", ".htm"):
        from bs4 import BeautifulSoup

        raw = [(1, BeautifulSoup(path.read_text(errors="ignore"), "html.parser").get_text("\n"))]
    else:
        raw = [(1, path.read_text(errors="ignore"))]

    pages = []
    for number, text in raw:
        text = text.replace("\xad\n", "").replace("\xad", "").replace(" ", " ")
        lines = []
        for line in text.split("\n"):
            line = re.sub(r"\s+", " ", line).strip()
            if not line or any(rx.match(line) for rx in FURNITURE_RE):
                continue
            lines.append(line)
        pages.append((number, lines))
    return pages


def parse_document(path: Path) -> dict:
    """Split a document into units (Article N, Annex X, Section N.N) of paragraphs.

    Returns {"source", "title", "units": [{"unit", "title", "chapter",
    "paras": [{"label", "page", "text"}]}], "words"}.
    """
    path = Path(path)
    source = path.stem
    info = DOCS.get(source, {})
    pages = extract_pages(path)

    flat = [(pg, ln) for pg, lines in pages for ln in lines]
    is_regulation = sum(bool(ARTICLE_RE.match(ln)) for _, ln in flat) >= 5

    units: list[dict] = []
    cur = None
    chapter = ""
    skipping_signature = False
    started = not is_regulation        # for regulations, drop the recitals before the enacting terms

    def start(unit, title, pg):
        nonlocal cur
        cur = {"unit": unit, "title": title, "chapter": chapter, "paras": [], "page": pg}
        units.append(cur)

    i = 0
    while i < len(flat):
        pg, ln = flat[i]
        i += 1
        if not started:
            if ln.startswith("HAVE ADOPTED THIS REGULATION"):
                started = True
            continue
        if is_regulation:
            m = CHAPTER_RE.match(ln)
            if m:
                chapter = f"Chapter {m.group(1)}"
                if i < len(flat) and flat[i][1].isupper():
                    chapter += " - " + re.sub(r"\bAi\b", "AI", flat[i][1].title())
                    i += 1
                continue
            if SECTION_RE.match(ln):
                if i < len(flat) and flat[i][1][:1].isupper():
                    i += 1                           # section title
                continue
            if ln.startswith("Done at "):
                skipping_signature = True
                continue
            m = ANNEX_RE.match(ln)
            if m:
                skipping_signature = False
                title = flat[i][1] if i < len(flat) else ""
                i += 1
                chapter = "Annexes"
                start(f"Annex {m.group(1)}", title, pg)
                continue
            if skipping_signature:
                continue
            m = ARTICLE_RE.match(ln)
            if m:
                title = flat[i][1] if i < len(flat) else ""
                i += 1
                start(f"Article {m.group(1)}", title, pg)
                continue
        else:
            if FOOTNOTE_RE.match(ln):
                continue
            m = PART_RE.match(ln)
            if m and not ln.endswith((".", ",", ";", ":")):
                chapter = f"Part {m.group(1)} - {m.group(2)}"
                start(f"Part {m.group(1)}", m.group(2), pg)
                continue
            m = HEADING_RE.match(ln)
            if m and not ln.endswith((".", ",", ";", ":")):
                start(f"Section {m.group(1)}", m.group(2), pg)
                continue
        if cur is None:
            if is_regulation:
                continue
            start("Preamble", "", pg)               # text before the first heading
        cur["paras"].append((pg, ln))

    # lines -> paragraphs
    out_units = []
    for u in units:
        paras: list[dict] = []
        for pg, ln in u["paras"]:
            m = PARA_RE.match(ln)
            if m or not paras:
                label = (m.group(1) or m.group(2)) if m else ""
                paras.append({"label": label, "page": pg, "text": ln,
                              "kind": "num" if m and m.group(1) else "pt"})
            else:
                sep = "\n" if re.match(r"^\(?[a-z]{1,3}\)\s|^\([ivx]+\)\s|^[-•–]\s", ln) else " "
                paras[-1]["text"] += sep + ln
        if u["unit"] == "Preamble" and sum(len(p["text"].split()) for p in paras) < 60:
            continue                                # title page only
        if paras:
            u2 = {k: v for k, v in u.items() if k != "paras"}
            u2["paras"] = paras
            out_units.append(u2)
    words = sum(len(p["text"].split()) for u in out_units for p in u["paras"])
    return {"source": source, "title": info.get("title", source), "units": out_units, "words": words}


# --------------------------------------------------------------------------
# Chunking: two designs
# --------------------------------------------------------------------------

def _label(unit: str, paras: list[dict]) -> str:
    """'Article 5(1)-(2)' for a group of paragraphs of a unit."""
    labels = [p["label"] for p in paras if p["label"]]
    if not labels:
        return unit
    first, last = labels[0], labels[-1]
    if unit.startswith(("Section", "Part")):
        return f"{unit}, para ({first})" if first == last else f"{unit}, paras ({first})-({last})"
    return f"{unit}({first})" if first == last else f"{unit}({first})-({last})"


def chunk_fixed(doc: dict) -> list[dict]:
    """Design A: windows of FIXED_WORDS words, FIXED_OVERLAP overlap, ignoring structure.

    The chunk keeps the pages and the units it overlaps as metadata, but its text
    is only the words.
    """
    words, ann = [], []
    for u in doc["units"]:
        for p in u["paras"]:
            for w in p["text"].split():
                words.append(w)
                ann.append((p["page"], u["unit"]))
    chunks, step, start = [], FIXED_WORDS - FIXED_OVERLAP, 0
    while start < len(words):
        end = min(start + FIXED_WORDS, len(words))
        if len(chunks) and end - start < FIXED_OVERLAP + 20:
            break                                    # tail already covered by overlap
        a = ann[start:end]
        pages = sorted({p for p, _ in a})
        units = list(dict.fromkeys(u for _, u in a))
        chunks.append({
            "text": " ".join(words[start:end]),
            "unit": units[0], "units": ";".join(units),
            "location": f"pages {pages[0]}-{pages[-1]}" if len(pages) > 1 else f"page {pages[0]}",
            "page": pages[0], "page_end": pages[-1], "chapter": "",
        })
        if end == len(words):
            break
        start += step
    return chunks


def chunk_structure(doc: dict) -> list[dict]:
    """Design B: one chunk per article / annex / section; longer ones are split
    at paragraph boundaries. Every chunk starts with a header naming its place."""
    chunks = []
    short = doc["title"].split(" (")[0]
    for u in doc["units"]:
        groups, cur, n = [], [], 0
        for p in u["paras"]:
            w = len(p["text"].split())
            if w > STRUCT_MAX_WORDS:                 # one huge paragraph: split by words
                if cur:
                    groups.append(cur)
                    cur, n = [], 0
                toks = p["text"].split(" ")
                for s in range(0, len(toks), STRUCT_MAX_WORDS):
                    groups.append([{**p, "text": " ".join(toks[s:s + STRUCT_MAX_WORDS]),
                                    "part": s // STRUCT_MAX_WORDS + 1}])
                continue
            if cur and n + w > STRUCT_MAX_WORDS:
                groups.append(cur)
                cur, n = [], 0
            cur.append(p)
            n += w
        if cur:
            groups.append(cur)
        for g in groups:
            loc = _label(u["unit"], g)
            if g[0].get("part", 1) > 1:
                loc += f" (continued, part {g[0]['part']})"
            head = f"{short} | {u['chapter'] + ' | ' if u['chapter'] else ''}{loc} - {u['title']}"
            chunks.append({
                "text": head + "\n" + "\n".join(p["text"] for p in g),
                "unit": u["unit"], "units": u["unit"],
                "location": f"{loc} - {u['title']}",
                "page": g[0]["page"], "page_end": g[-1]["page"], "chapter": u["chapter"],
            })
    return chunks


CHUNKERS = {"fixed": chunk_fixed, "structure": chunk_structure}


def chunk_file(path: Path, design: str = "structure") -> tuple[dict, list[dict]]:
    """Parse a file and cut it into chunks with metadata. Returns (doc, chunks)."""
    doc = parse_document(Path(path))
    info = DOCS.get(doc["source"], {})
    chunks = CHUNKERS[design](doc)
    for n, c in enumerate(chunks):
        c["source"] = doc["source"]
        c["title"] = doc["title"]
        c["design"] = design
        c["n_words"] = len(c["text"].split())
        c["id"] = f"{design}:{doc['source']}:{n:04d}:{hashlib.sha1(c['text'].encode()).hexdigest()[:8]}"
    return doc, chunks


# --------------------------------------------------------------------------
# Embedding and storage
# --------------------------------------------------------------------------

_client = None


def genai_client():
    global _client
    if _client is None:
        from google import genai
        from api_key import load_api_key

        _client = genai.Client(api_key=load_api_key())
    return _client


class DailyQuotaExceeded(RuntimeError):
    pass


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed texts with Gemini (768 dims, unit length). Retries on rate limits;
    stops with DailyQuotaExceeded when the daily free quota is spent."""
    from google.genai import types

    vectors = []
    for s in range(0, len(texts), BATCH):
        batch = texts[s:s + BATCH]
        contents = [types.Content(parts=[types.Part(text=t)]) for t in batch]
        for attempt in range(8):
            try:
                r = genai_client().models.embed_content(
                    model=EMBED_MODEL, contents=contents,
                    config=types.EmbedContentConfig(output_dimensionality=EMBED_DIM))
                break
            except Exception as e:  # noqa: BLE001
                msg = str(e)
                if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
                    if "PerDay" in msg or "per day" in msg.lower():
                        raise DailyQuotaExceeded(msg[:300]) from e
                    m = re.search(r"retry in ([\d.]+)s", msg) or re.search(r"'retryDelay': '(\d+)s'", msg)
                    time.sleep(min(float(m.group(1)) + 1 if m else 5 * (attempt + 1), 70))
                elif "503" in msg or "500" in msg or "UNAVAILABLE" in msg:
                    time.sleep(3 * (attempt + 1))
                else:
                    raise
        else:
            raise RuntimeError("embedding kept failing")
        for e in r.embeddings:
            v = np.array(e.values, dtype=np.float32)
            vectors.append((v / np.linalg.norm(v)).tolist())
    return vectors


def collection(design: str):
    import chromadb

    INDEX_DIR.mkdir(exist_ok=True)
    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return client.get_or_create_collection(f"chunks_{design}", metadata={"hnsw:space": "cosine"})


def _meta(c: dict) -> dict:
    keys = ["source", "title", "design", "unit", "units", "location", "page", "page_end", "chapter", "n_words"]
    return {k: c[k] for k in keys}


def embed_and_store(chunks: list[dict], design: str) -> int:
    """Embed the chunks that have no saved vector and store them, batch by batch.
    Returns the number of newly embedded chunks."""
    col = collection(design)
    have = set(col.get(ids=[c["id"] for c in chunks], include=[])["ids"]) if chunks else set()
    todo = [c for c in chunks if c["id"] not in have]
    for s in range(0, len(todo), BATCH * 4):
        part = todo[s:s + BATCH * 4]
        vecs = embed_texts([c["text"] for c in part])
        col.add(ids=[c["id"] for c in part], embeddings=vecs,
                documents=[c["text"] for c in part], metadatas=[_meta(c) for c in part])
        log(f"  [{design}] embedded {min(s + len(part), len(todo))}/{len(todo)}")
    return len(todo)


def sha256(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def load_registry() -> dict:
    return json.loads(REGISTRY_FILE.read_text()) if REGISTRY_FILE.exists() else {}


def save_registry(reg: dict) -> None:
    INDEX_DIR.mkdir(exist_ok=True)
    REGISTRY_FILE.write_text(json.dumps(reg, indent=2, ensure_ascii=False))


def active_design() -> str:
    """The design the server searches and add_document writes to."""
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text()).get("design", "structure")
    return "structure"


def remove_document(source: str) -> bool:
    """Delete a document's chunks from every design and from the registry."""
    reg = load_registry()
    if source not in reg:
        return False
    for d in reg[source]["chunks"]:
        collection(d).delete(where={"source": source})
    reg.pop(source)
    save_registry(reg)
    bm25_reset()
    return True


def active_method() -> str:
    """How the server searches: "vector" or "hybrid" (set by the evaluation)."""
    if CONFIG_FILE.exists():
        return json.loads(CONFIG_FILE.read_text()).get("method", "vector")
    return "vector"


def index_file(path: Path, designs=DESIGNS) -> dict:
    """Run one file through the whole pipeline: parse, chunk, embed, store.

    If the same file (same SHA-256) is already indexed nothing is embedded and
    status is "already_indexed". If a file with the same name but different
    content is indexed, its old chunks are removed first ("replaced").
    """
    path = Path(path)
    digest = sha256(path)
    reg = load_registry()
    source = path.stem
    status = "added"
    if source in reg:
        if reg[source]["sha256"] == digest and all(d in reg[source]["chunks"] for d in designs):
            return {"status": "already_indexed", "source": source, "chunks": reg[source]["chunks"]}
        if reg[source]["sha256"] != digest:
            status = "replaced"
            for d in reg[source]["chunks"]:
                collection(d).delete(where={"source": source})
            reg.pop(source)
    counts, embedded, words = {}, 0, 0
    for d in designs:
        doc, chunks = chunk_file(path, d)
        if not chunks:
            raise ValueError(f"no text could be extracted from {path.name}")
        embedded += embed_and_store(chunks, d)
        counts[d] = len(chunks)
        words = doc["words"]
    entry = reg.get(source, {"chunks": {}})
    entry.update({"sha256": digest, "title": DOCS.get(source, {}).get("title", source),
                  "words": words, "file": path.name})
    entry["chunks"].update(counts)
    reg[source] = entry
    save_registry(reg)
    bm25_reset()
    return {"status": status, "source": source, "chunks": counts, "embedded": embedded, "words": words}


# --------------------------------------------------------------------------
# Retrieval: vector, or vector + BM25
# --------------------------------------------------------------------------

def _load_cache() -> dict:
    return json.loads(QUERY_CACHE_FILE.read_text()) if QUERY_CACHE_FILE.exists() else {}


def embed_query(query: str) -> list[float]:
    """Embed a question; vectors are cached in index/query_cache.json so that
    repeated evaluation runs do not spend quota."""
    key = hashlib.sha1(f"{EMBED_MODEL}:{EMBED_DIM}:{query}".encode()).hexdigest()
    cache = _load_cache()
    if key not in cache:
        cache[key] = [round(x, 5) for x in embed_texts([query])[0]]
        INDEX_DIR.mkdir(exist_ok=True)
        QUERY_CACHE_FILE.write_text(json.dumps(cache))
    return cache[key]


_bm25: dict = {}


def bm25_reset():
    _bm25.clear()


def _tok(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def _bm25_index(design: str):
    if design not in _bm25:
        got = collection(design).get(include=["documents", "metadatas"])
        docs = [_tok(t) for t in got["documents"]]
        df = Counter(w for d in docs for w in set(d))
        _bm25[design] = dict(ids=got["ids"], texts=got["documents"], metas=got["metadatas"],
                             tf=[Counter(d) for d in docs], len=np.array([len(d) for d in docs]), df=df)
    return _bm25[design]


def _bm25_scores(query: str, design: str, k1=1.5, b=0.75) -> np.ndarray:
    ix = _bm25_index(design)
    n, avg = len(ix["ids"]), max(ix["len"].mean(), 1)
    s = np.zeros(n)
    for w in set(_tok(query)):
        df = ix["df"].get(w, 0)
        if not df:
            continue
        idf = math.log(1 + (n - df + 0.5) / (df + 0.5))
        for i, tf in enumerate(ix["tf"]):
            f = tf.get(w, 0)
            if f:
                s[i] += idf * f * (k1 + 1) / (f + k1 * (1 - b + b * ix["len"][i] / avg))
    return s


def retrieve(query: str, k: int = 5, design: str | None = None, method: str | None = None) -> list[dict]:
    """Top-k chunks for a query: [{id, text, meta, score}].

    method "vector": cosine similarity of Gemini embeddings.
    method "hybrid": reciprocal-rank fusion of the vector and BM25 rankings.
    """
    design = design or active_design()
    method = method or active_method()
    col = collection(design)
    if col.count() == 0:
        return []
    qv = embed_query(query)
    pool = min(max(k, 30) if method == "hybrid" else k, col.count())
    r = col.query(query_embeddings=[qv], n_results=pool, include=["documents", "metadatas", "distances"])
    vec = [dict(id=i, text=t, meta=m, score=1 - d)
           for i, t, m, d in zip(r["ids"][0], r["documents"][0], r["metadatas"][0], r["distances"][0])]
    if method == "vector":
        return vec[:k]
    ix = _bm25_index(design)
    scores = _bm25_scores(query, design)
    order = np.argsort(-scores)[:pool]
    fused: dict[str, float] = {}
    for rank, h in enumerate(vec):
        fused[h["id"]] = fused.get(h["id"], 0) + 1 / (60 + rank)
    for rank, i in enumerate(order):
        if scores[i] > 0:
            fused[ix["ids"][i]] = fused.get(ix["ids"][i], 0) + 1 / (60 + rank)
    by_id = {h["id"]: h for h in vec}
    for i, cid in enumerate(ix["ids"]):
        if cid in fused and cid not in by_id:
            by_id[cid] = dict(id=cid, text=ix["texts"][i], meta=ix["metas"][i], score=0.0)
    top = sorted(fused, key=fused.get, reverse=True)[:k]
    return [{**by_id[c], "score": fused[c]} for c in top]


def citation(meta: dict) -> str:
    """Short citation: source, location and page, as shown to the model."""
    pg = meta["page"] if meta["page"] == meta["page_end"] else f"{meta['page']}-{meta['page_end']}"
    return f"{meta['source']} | {meta['location']} | PDF p. {pg}"


# --------------------------------------------------------------------------
# Command line
# --------------------------------------------------------------------------

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true", help="chunk only; print counts, no embedding")
    ap.add_argument("--design", choices=[*DESIGNS, "both"], default="both")
    args = ap.parse_args()
    designs = DESIGNS if args.design == "both" else (args.design,)

    paths = download_corpus(INITIAL)
    if args.dry_run:
        for p in paths:
            for d in designs:
                doc, ch = chunk_file(p, d)
                log(f"{p.stem:36s} {d:10s} {doc['words']:7d} words, {len(doc['units']):4d} units, {len(ch):4d} chunks")
        return
    t0 = time.time()
    for p in paths:
        log(f"== {p.name}")
        try:
            res = index_file(p, designs)
        except DailyQuotaExceeded as e:
            log(f"\nDaily embedding quota reached; progress is saved. Run again after the reset.\n{e}")
            sys.exit(1)
        log(f"  {res}")
    log(f"done in {time.time() - t0:.0f}s")


if __name__ == "__main__":
    main()
