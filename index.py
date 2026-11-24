"""
Build the index (`main.py index`).

Downloads the drone-rules corpus into corpus/, splits it into sections
(article / UAS.xxx point / AMC-GM heading), chunks each section into word
windows, embeds with Gemini and stores everything in index/ (ChromaDB).

Two chunk designs are built side by side (150 and 400 words) so evaluate.py
can compare them. Vectors are saved batch by batch and only missing chunks
get embedded, so a crash or the daily quota never loses work.
"""

import hashlib
import math
import re
import sys
import time
from collections import Counter, defaultdict
from pathlib import Path

import chromadb
import httpx
from bs4 import BeautifulSoup
from google import genai
from google.genai import errors, types
from pypdf import PdfReader

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768  # smaller vectors keep index/ well under the 90 MB limit
BATCH = 20

DESIGNS = {"w150": 150, "w400": 400}  # design name -> words per chunk
CHOSEN_DESIGN = "w150"  # set from the hit-rate numbers in eval/retrieval.csv

SOURCES = [
    {
        "source": "Reg 2019/947",
        "title": "Commission Implementing Regulation (EU) 2019/947 on the rules and procedures for the operation of unmanned aircraft (consolidated 04/04/2022)",
        "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:02019R0947-20220404",
        "file": "c947_20220404.html",
        "version": "consolidated text of 4 April 2022",
    },
    {
        "source": "Reg 2019/945",
        "title": "Commission Delegated Regulation (EU) 2019/945 on unmanned aircraft systems and third-country operators (consolidated 09/08/2020)",
        "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:02019R0945-20200809",
        "file": "c945_20200809.html",
        "version": "consolidated text of 9 August 2020",
    },
    {
        "source": "EASA AMC-GM Part-UAS",
        "title": "EASA Acceptable Means of Compliance and Guidance Material to Part-UAS, Issue 1 (ED Decision 2019/021/R, Annex II)",
        "url": "https://www.easa.europa.eu/sites/default/files/dfu/AMC%20&%20GM%20to%20Part-UAS%20%E2%80%94%20Issue%201.pdf",
        "file": "easa_amc_gm_part_uas.pdf",
        "version": "Issue 1 of 9 October 2019",
    },
]

# Headings that start a new section in the EUR-Lex text: a whole line like
# "Article 4" / "PART 2", or an annex point like "UAS.OPEN.020 UAS operations in ...".
HTML_HEADING = re.compile(
    r"^(?:(?:Article \d+[a-z]?|ANNEX|Appendix \d+|PART [A-Z0-9]+|CHAPTER [IVX]+|SECTION \d+)$|UAS\.[A-Z0-9-]+\.\d+\b)"
)
TITLED = re.compile(r"^(PART|CHAPTER|SECTION|Appendix) ")  # their title is on the next line
# AMC/GM headings in the EASA PDF, e.g. "AMC1 UAS.OPEN.020(1) and (2) UAS operations in subcategory A1".
PDF_HEADING = re.compile(r"^((?:AMC|GM)\d+ (?:UAS|Article)\S*(?: \S+)?)")
PDF_NOISE = re.compile(r"^(Annex I{1,2} to ED Decision 2019/021/R|Page \d+ of \d+)\s*$")


def log(*args) -> None:
    # stderr, so server.py can import this module without touching stdout
    print(*args, file=sys.stderr, flush=True)


# ---------- download & extract ----------

MIN_FILE_BYTES = 20_000  # every corpus file is far larger; an empty or blocked response is not


def download(src: dict) -> Path | None:
    """Local copy of a source, downloading it if needed. None if it can't be fetched:
    the vectors already committed in index/ are kept and nothing is re-embedded."""
    path = CORPUS_DIR / src["file"]
    if not path.exists() or path.stat().st_size < MIN_FILE_BYTES:
        CORPUS_DIR.mkdir(exist_ok=True)
        log(f"downloading {src['source']}")
        try:
            r = httpx.get(src["url"], headers={"User-Agent": "Mozilla/5.0"}, follow_redirects=True, timeout=120)
            r.raise_for_status()
        except httpx.HTTPError as e:
            log(f"  could not download {src['source']} ({e}); keeping its vectors in index/")
            return None
        if len(r.content) < MIN_FILE_BYTES:
            log(f"  {src['source']}: the site returned {len(r.content)} bytes; keeping its vectors in index/")
            return None
        path.write_bytes(r.content)
    return path


def html_sections(path: Path) -> list[dict]:
    """EUR-Lex HTML -> [{location, text}], one per article / annex point."""
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    for tag in soup.select(".modref, .arrow, script, style"):  # amendment markers like ▼M1
        tag.decompose()
    lines = [ln.replace("\xa0", " ").strip() for ln in soup.get_text("\n").splitlines()]
    lines = [ln for ln in lines if ln]

    # list labels "(a)" sit alone on a line; glue them to the text that follows
    merged = []
    for ln in lines:
        if merged and re.fullmatch(r"\(?[a-z0-9ivx]+[.)]", merged[-1]):
            merged[-1] += " " + ln
        else:
            merged.append(ln)

    sections, loc, buf = [], "Preamble", []
    for i, ln in enumerate(merged):
        if HTML_HEADING.match(ln):
            if buf:
                sections.append({"location": loc, "text": " ".join(buf)})
            loc, buf = ln, []
            nxt = merged[i + 1] if i + 1 < len(merged) else ""
            if TITLED.match(ln) and nxt and not HTML_HEADING.match(nxt) and len(nxt.split()) <= 15:
                loc += " " + nxt  # "PART 2" -> "PART 2 Requirements for a class C1 ..."
            loc = loc[:90]
        else:
            buf.append(ln)
    if buf:
        sections.append({"location": loc, "text": " ".join(buf)})

    # drop the EUR-Lex "documentation tool" disclaimer and empty title stubs
    return [s for s in sections if s["location"] != "Preamble" and len(s["text"].split()) > 5]


def pdf_sections(path: Path) -> list[dict]:
    """PDF -> [{location, text}]. Location = nearest AMC/GM heading + page."""
    sections, loc, buf, start_page = [], "Front matter", [], 1
    for pno, page in enumerate(PdfReader(path).pages, start=1):
        text = page.extract_text() or ""
        if text.count("....") > 5:  # table of contents page
            continue
        for ln in (l.strip() for l in text.splitlines()):
            if not ln or PDF_NOISE.match(ln):
                continue
            m = PDF_HEADING.match(ln)
            if m:
                if buf:
                    sections.append({"location": f"{loc} (p. {start_page})", "text": " ".join(buf)})
                loc, buf, start_page = ln[:90], [], pno
            else:
                buf.append(ln)
    if buf:
        sections.append({"location": f"{loc} (p. {start_page})", "text": " ".join(buf)})
    return sections


def clean(text: str) -> str:
    text = re.sub(r"(\w)- (\w)", r"\1\2", text)  # words hyphenated across lines
    return re.sub(r"\s+", " ", text).strip()


def extract(path: Path) -> list[dict]:
    ext = path.suffix.lower()
    if ext == ".pdf":
        secs = pdf_sections(path)
    elif ext in {".html", ".htm"}:
        secs = html_sections(path)
    else:  # plain text: one section per paragraph block
        blocks = [b for b in path.read_text(encoding="utf-8").split("\n\n") if b.strip()]
        secs = [{"location": f"paragraph {i + 1}", "text": b} for i, b in enumerate(blocks)]
    return [{**s, "text": clean(s["text"])} for s in secs]


# ---------- chunk ----------

def chunk_sections(sections: list[dict], size: int) -> list[dict]:
    """Word windows inside each section, so a chunk never mixes two articles."""
    step = size - size // 5  # 20% overlap
    chunks = []
    for s in sections:
        words = s["text"].split()
        for start in range(0, max(len(words) - size // 5, 1), step):
            chunks.append({"location": s["location"], "text": " ".join(words[start:start + size])})
    return chunks


def chunk_file(path: Path, source: str, title: str, design: str) -> list[dict]:
    """Extract + chunk one file; each chunk gets an id and its metadata."""
    digest = file_hash(path)
    chunks = chunk_sections(extract(path), DESIGNS[design])
    for i, c in enumerate(chunks):
        c["id"] = hashlib.sha1(f"{source}|{design}|{i}|{c['text']}".encode()).hexdigest()[:16]
        c["meta"] = {"source": source, "title": title, "location": c["location"], "chunk": i, "file_hash": digest}
    return chunks


def file_hash(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


# ---------- embed & store ----------

_client = None


def client() -> genai.Client:
    global _client
    if _client is None:
        _client = genai.Client(api_key=load_api_key())
    return _client


def embed(texts: list[str], task: str = "RETRIEVAL_DOCUMENT") -> list[list[float]]:
    """Embed with a few retries on rate limits (per-minute limits clear quickly)."""
    for attempt in range(5):
        try:
            res = client().models.embed_content(
                model=EMBED_MODEL,
                # one Content per text: a plain list would be embedded as a single item
                contents=[types.Content(parts=[types.Part(text=t)]) for t in texts],
                config=types.EmbedContentConfig(task_type=task, output_dimensionality=EMBED_DIM),
            )
            return [e.values for e in res.embeddings]
        except errors.ClientError as e:
            if e.code != 429 or attempt == 4:
                raise
            log(f"rate limited, waiting {20 * (attempt + 1)}s")
            time.sleep(20 * (attempt + 1))


def collection(design: str):
    db = chromadb.PersistentClient(path=str(INDEX_DIR / "chroma"))
    return db.get_or_create_collection(f"drones_{design}", metadata={"hnsw:space": "cosine"})


def embed_and_store(chunks: list[dict], design: str) -> int:
    """Embed only chunks not yet stored; save each batch straight away. Returns how many were added."""
    col = collection(design)
    have = set(col.get(ids=[c["id"] for c in chunks], include=[])["ids"]) if chunks else set()
    todo = [c for c in chunks if c["id"] not in have]
    for i in range(0, len(todo), BATCH):
        batch = todo[i:i + BATCH]
        # title + location go into the embedded text so headings help retrieval
        vecs = embed([f"{c['meta']['source']} | {c['location']}\n{c['text']}" for c in batch])
        col.add(ids=[c["id"] for c in batch], embeddings=vecs,
                documents=[c["text"] for c in batch], metadatas=[c["meta"] for c in batch])
        log(f"  {design}: {min(i + BATCH, len(todo))}/{len(todo)} embedded")
    return len(todo)


def loc_match(wanted: str, location: str) -> bool:
    """'PART 1' matches 'PART 1 Requirements...' but not 'PART 12'."""
    w, l = wanted.strip().lower(), location.strip().lower()
    return l.startswith(w) and (len(l) == len(w) or not l[len(w)].isalnum())


def retrieve(query: str, design: str = CHOSEN_DESIGN, k: int = 5, query_vec: list[float] | None = None,
             sources: list[str] | None = None) -> list[dict]:
    """Top-k chunks for a query. Pass query_vec to reuse an embedding across designs,
    and sources to search only those documents (the evaluation leaves out added ones)."""
    vec = query_vec or embed([query], task="RETRIEVAL_QUERY")[0]
    res = collection(design).query(query_embeddings=[vec], n_results=k, where=_only(sources))
    return [{"id": i, "text": d, **m, "score": round(1 - dist, 3)}
            for i, d, m, dist in zip(res["ids"][0], res["documents"][0], res["metadatas"][0], res["distances"][0])]


# ---------- hybrid retrieval: BM25 + dense, fused by reciprocal rank ----------
# Evaluated as a third design in evaluate.py. It reuses the stored vectors and the
# saved query vectors, so it needs no new embeddings.

_BM25: dict = {}


def _only(sources: list[str] | None) -> dict | None:
    return {"source": {"$in": list(sources)}} if sources else None


def _tokens(text: str) -> list[str]:
    return re.findall(r"[a-z0-9]+", text.lower())


def _bm25_index(design: str, sources: list[str] | None = None):
    key = (design, tuple(sources or ()))
    if key not in _BM25:
        got = collection(design).get(where=_only(sources), include=["documents", "metadatas"])
        docs = [Counter(_tokens(f"{m['source']} {m['location']} {d}"))
                for d, m in zip(got["documents"], got["metadatas"])]
        lengths = [sum(d.values()) for d in docs]
        df = Counter(t for d in docs for t in d)
        _BM25[key] = (got["ids"], docs, lengths, df, sum(lengths) / len(lengths))
    return _BM25[key]


def bm25_ranking(query: str, design: str, k1: float = 1.5, b: float = 0.75,
                 sources: list[str] | None = None) -> list[str]:
    """Chunk ids of a design, best first, by Okapi BM25 over source, location and text."""
    ids, docs, lengths, df, avgdl = _bm25_index(design, sources)
    n, terms = len(docs), set(_tokens(query))

    def score(i: int) -> float:
        s = 0.0
        for t in terms:
            tf = docs[i].get(t, 0)
            if tf:
                idf = math.log(1 + (n - df[t] + 0.5) / (df[t] + 0.5))
                s += idf * tf * (k1 + 1) / (tf + k1 * (1 - b + b * lengths[i] / avgdl))
        return s

    scores = [score(i) for i in range(n)]
    return [ids[i] for i in sorted(range(n), key=lambda i: -scores[i])]


def _chunks_by_id(design: str, ids: list[str]) -> dict:
    got = collection(design).get(ids=ids, include=["documents", "metadatas"])
    return {i: (d, m) for i, d, m in zip(got["ids"], got["documents"], got["metadatas"])}


def retrieve_bm25(query: str, design: str = CHOSEN_DESIGN, k: int = 5, sources: list[str] | None = None) -> list[dict]:
    """Top-k chunks by BM25 alone (no embeddings). Evaluated to explain how the hybrid behaves."""
    ranking = bm25_ranking(query, design, sources=sources)[:k]
    by_id = _chunks_by_id(design, ranking)
    return [{"id": i, "text": by_id[i][0], **by_id[i][1], "score": None} for i in ranking]


def retrieve_hybrid(query: str, design: str = CHOSEN_DESIGN, k: int = 5, query_vec: list[float] | None = None,
                    pool: int = 50, rrf_k: int = 60, sources: list[str] | None = None) -> list[dict]:
    """Top-k chunks by reciprocal rank fusion of the dense top-`pool` and the BM25 top-`pool`."""
    vec = query_vec or embed([query], task="RETRIEVAL_QUERY")[0]
    dense = collection(design).query(query_embeddings=[vec], n_results=pool, where=_only(sources))["ids"][0]
    fused = defaultdict(float)
    for ranking in (dense, bm25_ranking(query, design, sources=sources)[:pool]):
        for rank, cid in enumerate(ranking, start=1):
            fused[cid] += 1 / (rrf_k + rank)
    top = sorted(fused, key=fused.get, reverse=True)[:k]
    by_id = _chunks_by_id(design, top)
    return [{"id": i, "text": by_id[i][0], **by_id[i][1], "score": round(fused[i], 4)} for i in top]


def main() -> None:
    for src in SOURCES:
        path = download(src)
        if path is None:
            continue
        for design in DESIGNS:
            chunks = chunk_file(path, src["source"], src["title"], design)
            words = sum(len(s["text"].split()) for s in extract(path))
            log(f"{src['source']}: {words} words, {len(chunks)} chunks ({design})")
            if not embed_and_store(chunks, design):
                log(f"  {design}: every chunk already has a saved vector, nothing embedded")
    for design in DESIGNS:
        log(f"{design}: {collection(design).count()} chunks in index/")


if __name__ == "__main__":
    main()
