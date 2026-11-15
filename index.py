"""
Assignment 3: build the index (`main.py index`).

Corpus: three EU regulations (AI Act, GDPR, DSA), English Official Journal
versions, fetched as XHTML from the EU Publications Office (CELLAR) into
corpus/. EUR-Lex itself blocks scripted downloads; CELLAR is its official
machine-readable back end.

Pipeline, per file:
    parse   -> units: one per recital, article or annex, with metadata
    chunk   -> one chunk per unit, long units split at paragraph boundaries,
               every chunk headed with its citation
    embed   -> gemini-embedding-2, only chunks without a saved vector,
               saved batch by batch so a crash or the daily quota loses nothing

Search (end of this file): two retrieval designs over the same vectors,
compared in evaluate.py, so the whole index fits in one day's free quota:
    vector   cosine similarity on the embeddings
    hybrid   vector + BM25 keyword ranking, merged by reciprocal rank fusion

server.py imports chunk_file(), embed_and_store() and search().
Logs go to stderr, so the MCP server can import this module safely.
"""

from __future__ import annotations

import hashlib
import json
import math
import re
import sys
import time
import urllib.request
from collections import Counter
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"

# The documents. `source` is the name used in citations and in eval/questions.csv.
CORPUS = {
    "32024R1689": {"source": "AI Act", "title": "Regulation (EU) 2024/1689 (Artificial Intelligence Act)",
                   "url": "https://eur-lex.europa.eu/eli/reg/2024/1689/oj"},
    "32016R0679": {"source": "GDPR", "title": "Regulation (EU) 2016/679 (General Data Protection Regulation)",
                   "url": "https://eur-lex.europa.eu/eli/reg/2016/679/oj"},
    "32022R2065": {"source": "DSA", "title": "Regulation (EU) 2022/2065 (Digital Services Act)",
                   "url": "https://eur-lex.europa.eu/eli/reg/2022/2065/oj"},
}
CELLAR_URL = "https://publications.europa.eu/resource/celex/{celex}"

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768          # smaller vectors keep index/ well under the 90 MB limit
EMBED_BATCH = 50

MAX_WORDS = 600          # split units longer than this at paragraph boundaries (900 chunks: one day's quota)
COLLECTION = "corpus"
QUERY_CACHE = INDEX_DIR / "query_cache.json"

MODES = ("vector", "hybrid")
DEFAULT_MODE = "vector"  # the design server.py uses: chosen by hit rate in evaluate.py (vector 96.6% vs hybrid 75.9% at k=5)


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


# --------------------------------------------------------------------------- download

def download_corpus() -> None:
    """Fetch each regulation from CELLAR unless it is already in corpus/."""
    CORPUS_DIR.mkdir(exist_ok=True)
    for celex in CORPUS:
        path = CORPUS_DIR / f"{celex}.html"
        if path.is_file() and path.stat().st_size > 10_000:
            continue
        log(f"Downloading {celex} from the Publications Office...")
        request = urllib.request.Request(
            CELLAR_URL.format(celex=celex),
            headers={"Accept": "application/xhtml+xml;q=0.9, text/html;q=0.8", "Accept-Language": "eng"},
        )
        with urllib.request.urlopen(request, timeout=120) as response:
            path.write_bytes(response.read())


# --------------------------------------------------------------------------- parse

AMENDMENT_MARK = re.compile(r"[▼►◄]\s*(?:[A-Z][0-9]*)?")   # consolidated texts: ▼B, ►M2 … ◄
MARKER = re.compile(r"^(\(?[0-9]{1,3}[a-z]?\)|\(?[a-z]{1,2}\)|\(?[ivxlc]{1,6}\)|[0-9]{1,3}\.|—|-|\*)$")


def clean_lines(element) -> list[str]:
    """Text of an HTML element as clean lines.

    Fixes two extraction problems in the Official Journal XHTML:
    - footnote markers like "(1)" sit inline in the text: removed;
    - list markers "(a)", "1." sit in their own table cell, so they come out
      as separate lines: merged with the text they introduce.
    """
    lines = [re.sub(r"\s+", " ", line).strip() for line in element.get_text("\n").split("\n")]
    lines = [AMENDMENT_MARK.sub("", line).replace("()", "").strip() for line in lines]
    lines = [line for line in lines if line]
    merged: list[str] = []
    pending = ""
    for line in lines:
        if MARKER.match(line):
            pending = f"{pending} {line}".strip()
            continue
        merged.append(f"{pending} {line}".strip() if pending else line)
        pending = ""
    if pending:
        merged.append(pending)
    return merged


def parse_eurlex(path: Path, source: str | None = None) -> list[dict]:
    """Split an Official Journal XHTML file into recitals, articles and annexes.

    Each unit: source, location ("Article 6", "Recital 32", "Annex III"),
    type, title (article heading), text (lines joined by newlines).
    The preamble citations, signatures and footnote lists are left out.
    """
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    for tag in soup.select(".oj-note-tag"):          # inline footnote markers
        (tag.find_parent("a") or tag).decompose()
    for note in soup.select(".oj-note, .footnote, .modref, .arrow"):   # footnote bodies, amendment banners
        note.decompose()
    for ref in soup.select("a .superscript"):                          # consolidated footnote markers
        ref.find_parent("a").decompose()

    if source is None:
        title = soup.find(class_="oj-doc-ti")
        source = title.get_text(" ", strip=True)[:80] if title else path.stem

    units = []
    patterns = [("recital", r"^rct_(\d+)$"), ("article", r"^art_(\d+)$"), ("annex", r"^anx_([IVXLC]+)$")]
    for unit_type, pattern in patterns:
        for element in soup.find_all(id=re.compile(pattern)):
            number = re.match(pattern, element["id"]).group(1)
            lines = clean_lines(element)
            heading = ""
            if unit_type == "recital":
                lines[0] = re.sub(r"^\(\d+\)\s*", "", lines[0])
            elif unit_type == "article":
                subtitle = element.find(class_=["oj-sti-art", "stitle-article-norm"])
                heading = subtitle.get_text(" ", strip=True) if subtitle else ""
                lines = lines[2:] if heading else lines[1:]     # drop "Article N" and its heading
            else:
                heading = lines[1] if len(lines) > 1 else ""
                lines = lines[2:]                               # drop "ANNEX N" and its heading
            lines = [line for line in lines if line]
            if not lines:
                continue
            units.append({
                "source": source,
                "location": f"{unit_type.capitalize()} {number}",
                "type": unit_type,
                "title": heading,
                "text": "\n".join(lines),
            })
    return units


def parse_pdf(path: Path, source: str) -> list[dict]:
    """One unit per page, for documents added later (e.g. Commission guidelines)."""
    from pypdf import PdfReader

    units = []
    for number, page in enumerate(PdfReader(path).pages, start=1):
        text = page.extract_text() or ""
        text = re.sub(r"-\n(\w)", r"\1", text)                  # re-join hyphenated words
        lines = [re.sub(r"\s+", " ", line).strip() for line in text.split("\n")]
        lines = [line for line in lines if line and not re.fullmatch(r"\d{1,3}", line)]  # page numbers
        if lines:
            units.append({"source": source, "location": f"Page {number}", "type": "page",
                          "title": "", "text": "\n".join(lines)})
    return units


def parse_text(text: str, source: str) -> list[dict]:
    """Plain text, Markdown or other HTML: one unit per blank-line-separated paragraph."""
    blocks = [re.sub(r"[ \t]+", " ", b).strip() for b in re.split(r"\n\s*\n", text)]
    return [{"source": source, "location": f"Paragraph {i}", "type": "paragraph", "title": "", "text": b}
            for i, b in enumerate([b for b in blocks if b], start=1)]


def source_name(path: Path) -> str:
    """Citation name: the known name for our three regulations, else the file name."""
    known = CORPUS.get(path.stem)
    return known["source"] if known else path.stem.replace("_", " ").replace("-", " ")


def parse_file(path: Path) -> list[dict]:
    path = Path(path)
    suffix = path.suffix.lower()
    if suffix in {".html", ".htm", ".xhtml", ".xml"}:
        head = path.read_text(encoding="utf-8", errors="ignore")[:200_000]
        if "eli-subdivision" in head or "oj-ti-art" in head:
            return parse_eurlex(path, source_name(path))
        text = BeautifulSoup(path.read_text(encoding="utf-8", errors="ignore"), "html.parser").get_text("\n\n")
        return parse_text(text, source_name(path))
    if suffix == ".pdf":
        return parse_pdf(path, source_name(path))
    if suffix in {".txt", ".md"}:
        return parse_text(path.read_text(encoding="utf-8"), source_name(path))
    raise ValueError(f"Unsupported file type: {suffix}. Use .html (EUR-Lex), .pdf, .txt or .md.")


# --------------------------------------------------------------------------- chunk

def citation(unit: dict) -> str:
    head = f"{unit['source']}, {unit['location']}"
    return f"{head} — {unit['title']}" if unit["title"] else head


def split_lines(lines: list[str], max_words: int) -> list[list[str]]:
    """Group lines into parts of at most max_words, never splitting a line unless it alone is too long."""
    parts, current, count = [], [], 0
    for line in lines:
        words = line.split()
        if len(words) > max_words:                        # one very long paragraph: hard split
            if current:
                parts.append(current)
                current, count = [], 0
            for start in range(0, len(words), max_words):
                parts.append([" ".join(words[start:start + max_words])])
            continue
        if current and count + len(words) > max_words:
            parts.append(current)
            current, count = [], 0
        current.append(line)
        count += len(words)
    if current:
        parts.append(current)
    return parts


def chunk_units(units: list[dict]) -> list[dict]:
    chunks = []
    for unit in units:
        parts = split_lines(unit["text"].split("\n"), MAX_WORDS)
        for i, part in enumerate(parts, start=1):
            label = citation(unit) + (f" (part {i} of {len(parts)})" if len(parts) > 1 else "")
            chunks.append({
                "text": f"{label}\n" + "\n".join(part),
                "source": unit["source"], "location": unit["location"],
                "type": unit["type"], "title": unit["title"], "part": i, "parts": len(parts),
            })
    return chunks


def chunk_file(path: Path | str) -> list[dict]:
    """Parse and chunk one file. Used by main() and by server.py's add-document tool."""
    chunks = chunk_units(parse_file(Path(path)))
    for chunk in chunks:
        chunk["file"] = Path(path).name
        digest = hashlib.sha1(chunk["text"].encode()).hexdigest()[:16]   # same text -> same id: never re-embedded
        slug = re.sub(r"\W+", "-", f"{chunk['source']}-{chunk['location']}-{chunk['part']}").strip("-")
        chunk["id"] = f"{slug}:{digest}"
    return chunks


# --------------------------------------------------------------------------- embed and store

class DailyQuotaExhausted(RuntimeError):
    pass


_client = None


def genai_client():
    global _client
    if _client is None:
        from google import genai

        from api_key import load_api_key
        _client = genai.Client(api_key=load_api_key())
    return _client


def embed_texts(texts: list[str], kind: str = "document") -> list[list[float]]:
    """Embed texts with Gemini, one vector per text.

    gemini-embedding-2 takes the retrieval task as a text prefix rather than
    a task_type parameter. Each text is sent as its own Content: a plain list
    of strings would be merged into a single input by the SDK for this model.
    Retries on per-minute limits; raises DailyQuotaExhausted on the daily one.
    """
    from google.genai import errors, types

    if kind == "query":
        prepared = [f"task: search result | query: {t}" for t in texts]
    else:
        prepared = [f"title: {t.split(chr(10), 1)[0]} | text: {t}" for t in texts]
    contents = [types.Content(parts=[types.Part(text=t)]) for t in prepared]

    for attempt in range(6):
        try:
            result = genai_client().models.embed_content(
                model=EMBED_MODEL, contents=contents,
                config=types.EmbedContentConfig(output_dimensionality=EMBED_DIM),
            )
            vectors = [e.values for e in result.embeddings]
            if len(vectors) != len(texts):
                raise RuntimeError(f"Asked for {len(texts)} embeddings, got {len(vectors)}.")
            return vectors
        except errors.ClientError as error:
            if error.code != 429:
                raise
            if "PerDay" in str(error) or "per day" in str(error).lower():
                raise DailyQuotaExhausted(str(error)) from error
            wait = 20 * (attempt + 1)
            log(f"  rate limited, waiting {wait}s...")
            time.sleep(wait)
    raise RuntimeError("Still rate limited after several retries.")


_chroma = None


def collection():
    """The Chroma collection in index/ (cosine distance)."""
    global _chroma
    import chromadb

    if _chroma is None:
        _chroma = chromadb.PersistentClient(
            path=str(INDEX_DIR), settings=chromadb.Settings(anonymized_telemetry=False))
    return _chroma.get_or_create_collection(COLLECTION, metadata={"hnsw:space": "cosine"})


def embed_and_store(chunks: list[dict]) -> tuple[int, int]:
    """Embed and store the chunks that have no saved vector yet. Returns (added, already_there)."""
    if not chunks:
        return 0, 0
    store = collection()
    existing = set(store.get(ids=[c["id"] for c in chunks], include=[])["ids"])
    todo = [c for c in chunks if c["id"] not in existing]
    for start in range(0, len(todo), EMBED_BATCH):
        batch = todo[start:start + EMBED_BATCH]
        vectors = embed_texts([c["text"] for c in batch])
        store.add(
            ids=[c["id"] for c in batch],
            embeddings=vectors,
            documents=[c["text"] for c in batch],
            metadatas=[{k: c[k] for k in ("source", "location", "type", "title",
                                          "part", "parts", "file")} for c in batch],
        )
        log(f"  embedded {min(start + EMBED_BATCH, len(todo))}/{len(todo)}")
    return len(todo), len(existing)


# --------------------------------------------------------------------------- search

CANDIDATES = 30   # how deep each ranking looks before fusion
RRF_K = 60        # standard reciprocal-rank-fusion constant

TOKEN = re.compile(r"[a-z0-9]+")
STOPWORDS = set("""a an and are as at be by can do does for from has have how i if in into is it its of on or our
should so that the their then there these they this to was we what when where which who will with you your""".split())


def tokenize(text: str) -> list[str]:
    return [t for t in TOKEN.findall(text.lower()) if t not in STOPWORDS]


def _load_query_cache() -> dict:
    try:
        return json.loads(QUERY_CACHE.read_text(encoding="utf-8"))
    except (FileNotFoundError, json.JSONDecodeError):
        return {}


_query_cache = _load_query_cache()


def query_vector(query: str) -> list[float]:
    """Embed a query once; cached in index/ so re-runs never spend quota on it again."""
    key = f"{EMBED_MODEL}:{EMBED_DIM}:{query.strip()}"
    if key not in _query_cache:
        _query_cache[key] = embed_texts([query.strip()], kind="query")[0]
        QUERY_CACHE.write_text(json.dumps(_query_cache), encoding="utf-8")
    return _query_cache[key]


_chunks: dict[str, dict] | None = None   # all stored chunks, loaded once, for BM25


def load_chunks(refresh: bool = False) -> dict[str, dict]:
    global _chunks
    if _chunks is None or refresh:
        data = collection().get(include=["documents", "metadatas"])
        _chunks = {i: {"id": i, "text": d, "tokens": Counter(tokenize(d)), **m}
                   for i, d, m in zip(data["ids"], data["documents"], data["metadatas"])}
    return _chunks


def bm25_ids(query: str, n: int, k1: float = 1.5, b: float = 0.75) -> list[str]:
    chunks = load_chunks()
    if not chunks:
        return []
    lengths = {i: sum(c["tokens"].values()) for i, c in chunks.items()}
    avg = sum(lengths.values()) / len(lengths)
    scores: dict[str, float] = {}
    for term in set(tokenize(query)):
        having = [i for i, c in chunks.items() if term in c["tokens"]]
        if not having:
            continue
        idf = math.log(1 + (len(chunks) - len(having) + 0.5) / (len(having) + 0.5))
        for i in having:
            tf = chunks[i]["tokens"][term]
            scores[i] = scores.get(i, 0.0) + idf * tf * (k1 + 1) / (tf + k1 * (1 - b + b * lengths[i] / avg))
    return sorted(scores, key=scores.get, reverse=True)[:n]


def vector_ids(query: str, n: int) -> list[str]:
    chunks = load_chunks()
    if not chunks:
        return []
    result = collection().query(query_embeddings=[query_vector(query)], n_results=min(n, len(chunks)), include=[])
    return result["ids"][0]


def search(query: str, k: int = 5, mode: str = DEFAULT_MODE) -> list[dict]:
    """Top-k chunks for a query (dicts with text, source, location, type, title, score)."""
    if mode not in MODES:
        raise ValueError(f"mode must be one of {MODES}")
    rankings = [vector_ids(query, CANDIDATES)]
    if mode == "hybrid":
        rankings.append(bm25_ids(query, CANDIDATES))
    scores: dict[str, float] = {}
    for ranking in rankings:
        for rank, i in enumerate(ranking, start=1):
            scores[i] = scores.get(i, 0.0) + 1 / (RRF_K + rank)
    top = sorted(scores, key=scores.get, reverse=True)[:k]
    chunks = load_chunks()
    return [{**{f: v for f, v in chunks[i].items() if f != "tokens"}, "score": round(scores[i], 4)} for i in top]


def format_results(results: list[dict]) -> str:
    """Search results as text for a model: a citation line, then the passage."""
    if not results:
        return "No passages found."
    blocks = []
    for n, r in enumerate(results, start=1):
        body = r["text"].split("\n", 1)[1] if "\n" in r["text"] else r["text"]
        title = f" — {r['title']}" if r.get("title") else ""
        part = f" (part {r['part']} of {r['parts']})" if r.get("parts", 0) > 1 else ""
        blocks.append(f"[{n}] Cite as: {r['source']}, {r['location']} | type: {r['type']}{title}{part}\n{body}")
    return "\n\n".join(blocks)


# --------------------------------------------------------------------------- main

def main() -> None:
    download_corpus()
    files = [CORPUS_DIR / f"{celex}.html" for celex in CORPUS]
    chunks = [c for path in files for c in chunk_file(path)]
    words = [len(c["text"].split()) for c in chunks]
    log(f"{len(chunks)} chunks, {sum(words):,} words, avg {sum(words) / len(words):.0f}, "
        f"max {max(words)} words per chunk")
    if "--dry-run" in sys.argv:
        return
    # Never rebuild: a chunk counts as indexed if its citation (law, location, part) is
    # stored, even if its text changed since. Only missing chunks are embedded, which
    # also resumes a build stopped by the daily quota. Nothing stored is deleted.
    stored = {i.split(":", 1)[0] for i in collection().get(include=[])["ids"]}
    missing = [c for c in chunks if c["id"].split(":", 1)[0] not in stored]
    try:
        added, _ = embed_and_store(missing)
    except DailyQuotaExhausted:
        log(f"Daily embedding quota reached with {collection().count()}/{len(chunks)} chunks stored.\n"
            f"Everything embedded so far is saved. Run `main.py index` again after 09:00 (Spain).")
        sys.exit(1)
    log(f"{added} newly embedded, {len(chunks) - len(missing)} already in index/ (not re-embedded).")

if __name__ == "__main__":
    main()
