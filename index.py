"""
Assignment 3: build the index (`main.py index`).

Corpus: EU food-supplement law from EUR-Lex (see DOCUMENTS). Pipeline per file:

    extract_lines(html)  -> clean text lines (tables become one line per row)
    segment(lines)       -> pieces tagged with their legal location
                            (Recital n, Article n, Annex X, Annex (nutrient))
    chunk_*(segments)    -> chunks for one retrieval design
    embed_and_store()    -> Gemini embeddings, saved to ChromaDB in index/
                            batch by batch; chunks that already have a vector
                            are never embedded again.

server.py's add_document tool imports `index_file()` from here, and the
search helpers (`search`, `embed_query`) live here too so that the server,
the agent and the evaluation all retrieve the same way.
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

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
EXTRA_DIR = CORPUS_DIR / "extra"          # documents kept out of the base index
INDEX_DIR = ROOT / "index"
CHROMA_DIR = INDEX_DIR / "chroma"
QUERY_CACHE = INDEX_DIR / "query_cache.json"
CONFIG_FILE = INDEX_DIR / "config.json"

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768            # smaller vectors keep index/ well under 90 MB
BATCH = 40

EURLEX = "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:{celex}"
CELLAR = "https://publications.europa.eu/resource/celex/{celex}"

# source id (as used in metadata, citations and eval/questions.csv) -> CELEX number
DOCUMENTS = {
    "Dir 2002/46/EC": "32002L0046",     # food supplements
    "Reg 1924/2006": "32006R1924",      # nutrition and health claims
    "Reg 1925/2006": "32006R1925",      # addition of vitamins, minerals, other substances
    "Reg 432/2012": "32012R0432",       # list of permitted health claims
    "Reg 2015/2283": "32015R2283",      # novel foods
    "Reg 1169/2011": "32011R1169",      # food information to consumers (labelling)
}
# Not in the base index: added later through the add_document tool.
EXTRA_DOCUMENTS = {"Reg 2022/860": "32022R0860"}   # monacolins from red yeast rice

DESIGNS = {
    "fixed": "fixed windows of 300 words, 50-word overlap, ignoring structure",
    "structure": "one chunk per article / annex part / health-claim group, max 300 words, with a heading",
}
DEFAULT_CONFIG = {"design": "structure", "mode": "hybrid", "k": 5}


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


# --------------------------------------------------------------------------- download

def download(celex: str, dest: Path) -> Path:
    """Fetch one EUR-Lex HTML document unless it is already on disk."""
    if dest.exists() and dest.stat().st_size > 5000:
        return dest
    dest.parent.mkdir(parents=True, exist_ok=True)
    attempts = [
        # EUR-Lex website (may answer scripts with a bot check)
        (EURLEX.format(celex=celex), {"Accept-Language": "en"}),
        # Publications Office "Cellar" API: same documents, meant for machines
        (CELLAR.format(celex=celex), {"Accept": "application/xhtml+xml", "Accept-Language": "eng"}),
        (CELLAR.format(celex=celex), {"Accept": "text/html", "Accept-Language": "eng"}),
    ]
    for url, headers in attempts:
        try:
            request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (Macintosh) daiist-assignment-3", **headers})
            with urllib.request.urlopen(request, timeout=90) as response:
                body = response.read()
        except Exception as e:  # noqa: BLE001
            log(f"  {celex}: {url[:60]}... failed ({e})")
            continue
        html = _unzip_html(body)
        if html and (b"Article 1" in html or b"ANNEX" in html) and len(html) > 5000:
            dest.write_bytes(html)
            log(f"downloaded {celex} ({len(html) // 1024} KB)")
            return dest
        log(f"  {celex}: {url[:60]}... returned no document (bot check?)")
    raise RuntimeError(f"Could not download {celex}. Open {EURLEX.format(celex=celex)} in a browser, "
                       f"save it (Cmd+S, 'Page Source') as {dest} and run again.")


def _unzip_html(body: bytes) -> bytes | None:
    """Cellar sometimes answers with a zip of the manifestation: take its (x)html file."""
    if body[:2] != b"PK":
        return body
    import io
    import zipfile

    with zipfile.ZipFile(io.BytesIO(body)) as z:
        names = [n for n in z.namelist() if n.lower().endswith((".html", ".xhtml", ".htm"))]
        return z.read(max(names, key=lambda n: z.getinfo(n).file_size)) if names else None


def download_corpus() -> dict[str, Path]:
    paths = {src: download(c, CORPUS_DIR / f"{c}.html") for src, c in DOCUMENTS.items()}
    for src, c in EXTRA_DOCUMENTS.items():      # only needed for the add-document demo
        try:
            download(c, EXTRA_DIR / f"{c}.html")
        except RuntimeError as e:
            log(f"  (extra document not available: {e})")
    return paths


# --------------------------------------------------------------------------- extract + clean

FOOTNOTE_LINE = re.compile(r"^\(\s*\d+\s*\)\s+(OJ [LC]|See |Opinion of|Position of|Council Decision)")
SPACES = re.compile(r"\s+")


def clean(text: str) -> str:
    text = text.replace("\xa0", " ").replace(" ", " ").replace("­", "")
    return SPACES.sub(" ", text).strip()


def extract_lines(html: str) -> list[str]:
    """HTML -> clean text lines. Paragraphs become lines; a table row becomes ONE line,
    cells joined with ' | ' (so a health claim keeps its nutrient, wording and
    conditions together). Footnotes and their markers are dropped."""
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "head"]):
        tag.decompose()
    # Footnote markers like "(1)" linking to the notes (newer OJ layout), and the notes themselves.
    for a in soup.find_all("a", href=True):
        if a["href"].startswith(("#ntr", "#ntc", "#E00")):
            a.decompose()
    for note in soup.select("p.oj-note, p.note, div.oj-note"):
        note.decompose()

    lines: list[str] = []
    body = soup.body or soup
    for el in body.find_all(["p", "tr", "h1", "h2", "h3", "h4"]):
        if el.find_parent("tr") is not None:      # inside a table row: the row handles it
            continue
        if el.name == "tr":
            cells = [clean(td.get_text(" ")) for td in el.find_all(["td", "th"], recursive=False)]
            cells = [c for c in cells if c]
            # Recitals and numbered points in the newer layout are 2-cell tables "(1)" | text
            if len(cells) == 2 and re.fullmatch(r"\(?[0-9a-z]{1,4}[).]?", cells[0]):
                line = f"{cells[0]} {cells[1]}"
            else:
                line = " | ".join(cells)
        else:
            line = own_text(el)
        line = re.sub(r"\(\s+(\d+)\s+\)", r"(\1)", line)
        if line and not FOOTNOTE_LINE.match(line):
            lines.append(line)
    return lines


BLOCKS = ["p", "tr", "h1", "h2", "h3", "h4"]


def own_text(el) -> str:
    """Text of a block without the text of blocks nested inside it. Old EUR-Lex pages
    leave <p> unclosed, so the parser nests every paragraph inside the first one;
    without this the whole act came out as one 3,500-word 'paragraph'."""
    parts = [str(t) for t in el.find_all(string=True) if t.find_parent(BLOCKS) is el]
    return clean(" ".join(parts))


def split_long(line: str, limit: int) -> list[str]:
    """Split a paragraph longer than `limit` words at sentence ends."""
    if words(line) <= limit:
        return [line]
    sentences = re.split(r"(?<=[.;:])\s+(?=[A-Z(])", line)
    out, cur = [], ""
    for sent in sentences:
        if cur and words(cur) + words(sent) > limit:
            out.append(cur)
            cur = sent
        else:
            cur = f"{cur} {sent}".strip()
    return out + ([cur] if cur else [])


def read_text_file(path: Path) -> list[str]:
    """Plain text / markdown / PDF -> lines (for add_document on non-HTML files)."""
    if path.suffix.lower() == ".pdf":
        from pypdf import PdfReader

        lines = []
        for n, page in enumerate(PdfReader(str(path)).pages, start=1):
            lines.append(f"[[PAGE {n}]]")
            lines += [clean(x) for x in (page.extract_text() or "").splitlines() if clean(x)]
        return lines
    return [clean(x) for x in path.read_text(encoding="utf-8", errors="ignore").splitlines() if clean(x)]


# --------------------------------------------------------------------------- segment by structure

ARTICLE = re.compile(r"^Article (\d+[a-z]?)$")
ANNEX = re.compile(r"^ANNEX(?:\s+([IVXLC]+))?\b(.*)$")
RECITAL = re.compile(r"^\((\d+)\)\s+(.*)")
CHAPTER = re.compile(r"^(CHAPTER|SECTION|TITLE) ([IVXLC0-9]+)$")
PAGE = re.compile(r"^\[\[PAGE (\d+)\]\]$")


def segment(lines: list[str]) -> list[dict]:
    """Walk the lines and tag each with where it sits in the act.

    Returns segments {section, title, lines}. A section is 'Recital 12',
    'Article 10', 'Annex II' or, for the table of permitted claims,
    'Annex (Vitamin C)' - one segment per table row, labelled by its nutrient.
    """
    segments: list[dict] = []
    section, title, in_preamble, after_whereas = "Preamble", "", True, False
    current: dict | None = None
    claims_table = False

    def start(sec: str, ttl: str = "") -> dict:
        seg = {"section": sec, "title": ttl, "lines": []}
        segments.append(seg)
        return seg

    current = start(section)
    i = 0
    while i < len(lines):
        line = lines[i]
        if m := PAGE.match(line):                       # PDFs: location is the page
            current = start(f"Page {m.group(1)}")
            i += 1
            continue
        if in_preamble and line.lower().startswith("whereas"):
            after_whereas = True
        if in_preamble and re.match(r"^(HAVE|HAS) ADOPTED THIS", line):
            in_preamble = False
            current = start("Enacting terms")
            i += 1
            continue
        if in_preamble and (m := RECITAL.match(line)):
            current = start(f"Recital {m.group(1)}")
            current["lines"].append(line)
            i += 1
            continue
        if m := ARTICLE.match(line):
            in_preamble = False
            nxt = lines[i + 1] if i + 1 < len(lines) else ""
            ttl = nxt if (len(nxt.split()) <= 14 and not re.match(r"^\d|^\(|^Article|^[A-Z ]+$", nxt)) else ""
            current = start(f"Article {m.group(1)}", ttl)
            i += 2 if ttl else 1
            continue
        if m := ANNEX.match(line):
            in_preamble = False
            num = m.group(1)
            current = start(f"Annex {num}" if num else "Annex")
            claims_table = False
            i += 1
            continue
        if CHAPTER.match(line):
            i += 1
            continue
        # The table of permitted health claims: one segment per row, labelled by nutrient.
        if current["section"].startswith("Annex") and " | " in line:
            cells = line.split(" | ")
            if cells[0].lower().startswith("nutrient, substance"):
                claims_table = True
                current["header"] = line
                i += 1
                continue
            if claims_table and len(cells) >= 3:
                base = current["section"].split(" (")[0]
                current = start(f"{base} ({cells[0]})")
                current["lines"].append(line)
                i += 1
                continue
        current["lines"].append(line)
        i += 1
    return [s for s in segments if s["lines"]]


# --------------------------------------------------------------------------- chunk designs

def words(text: str) -> int:
    return len(text.split())


def chunk_id(design: str, source: str, text: str) -> str:
    return hashlib.sha1(f"{design}|{source}|{text}".encode()).hexdigest()[:16]


def make_chunk(design, source, sections, text, title="", doc_hash="", origin="corpus") -> dict:
    sections = list(dict.fromkeys(sections))
    location = sections[0] if len(sections) == 1 else f"{sections[0]} - {sections[-1]}"
    if len(sections) > 1 and all(s.startswith("Annex (") for s in sections):
        location = "Annex (" + "; ".join(s[7:-1] for s in sections) + ")"
    if len(sections) > 1 and all(s.startswith("Recital ") for s in sections):
        location = f"Recitals {sections[0].split()[1]}-{sections[-1].split()[1]}"
    return {
        "id": chunk_id(design, source, text),
        "text": text,
        "source": source,
        "location": location,
        "sections": "|".join(sections),
        "title": title,
        "cite": f"{source}, {location}",
        "words": words(text),
        "doc_hash": doc_hash,
        "origin": origin,
    }


def chunk_fixed(source: str, segments: list[dict], size=300, overlap=50, **kw) -> list[dict]:
    """Design A: sliding windows over the whole text; location = sections it spans."""
    tagged = [(w, seg["section"]) for seg in segments for line in seg["lines"] for w in line.split()]
    chunks, step = [], size - overlap
    for start in range(0, max(len(tagged) - overlap, 1), step):
        window = tagged[start:start + size]
        if not window:
            break
        text = " ".join(w for w, _ in window)
        chunks.append(make_chunk("fixed", source, [s for _, s in window], text, **kw))
    return chunks


def _pack(pieces: list[tuple[str, str]], limit: int) -> list[list[tuple[str, str]]]:
    """Greedy packing of (section, text) pieces into groups of <= limit words."""
    groups, cur, n = [], [], 0
    for sec, text in pieces:
        w = words(text)
        if cur and n + w > limit:
            groups.append(cur)
            cur, n = [], 0
        cur.append((sec, text))
        n += w
    if cur:
        groups.append(cur)
    return groups


def chunk_structure(source: str, segments: list[dict], limit=300, **kw) -> list[dict]:
    """Design B: follow the act's structure.

    - an article (or annex part) is one chunk; long ones are split at paragraph
      boundaries into <= limit words, every piece keeping the article label;
    - consecutive recitals are packed together;
    - rows of the health-claims table are packed by neighbouring nutrients;
    - every chunk starts with a heading: source, location and article title.
    """
    chunks = []
    recitals = [(s["section"], " ".join(s["lines"])) for s in segments if s["section"].startswith("Recital")]
    claims = [(s["section"], " ".join(s["lines"])) for s in segments if s["section"].startswith("Annex (")]
    for group in _pack(recitals, limit):
        secs = [s for s, _ in group]
        head = f"{source} - recitals (reasons for the act)\n"
        chunks.append(make_chunk("structure", source, secs, head + "\n".join(t for _, t in group), **kw))
    for group in _pack(claims, limit):
        secs = [s for s, _ in group]
        head = (f"{source} - Annex, permitted health claims. Columns: nutrient/substance | claim | "
                f"conditions of use | restrictions/warnings | EFSA ref | entry no.\n")
        chunks.append(make_chunk("structure", source, secs, head + "\n".join(t for _, t in group), **kw))
    for seg in segments:
        sec = seg["section"]
        if sec.startswith(("Recital", "Annex (")):
            continue
        head = f"{source} - {sec}" + (f": {seg['title']}" if seg["title"] else "") + "\n"
        pieces = [(sec, part) for line in seg["lines"] for part in split_long(line, limit)]
        for group in _pack(pieces, limit):
            chunks.append(make_chunk("structure", source, [sec], head + "\n".join(t for _, t in group),
                                     title=seg["title"], **kw))
    return chunks


CHUNKERS = {"fixed": chunk_fixed, "structure": chunk_structure}


def chunk_file(path: Path, source: str, design: str, origin="corpus") -> list[dict]:
    """One file -> chunks for one design (the per-file step add_document reuses)."""
    raw = path.read_bytes()
    doc_hash = hashlib.sha256(raw).hexdigest()[:16]
    if path.suffix.lower() in (".html", ".htm"):
        lines = extract_lines(raw.decode("utf-8", errors="ignore"))
    else:
        lines = read_text_file(path)
    return CHUNKERS[design](source, segment(lines), doc_hash=doc_hash, origin=origin)


def guess_source(path: Path) -> str:
    """Name a new document the way the corpus names its sources ('Reg 2022/860')."""
    for src, celex in {**DOCUMENTS, **EXTRA_DOCUMENTS}.items():
        if celex in path.name:
            return src
    try:
        head = path.read_text(encoding="utf-8", errors="ignore")[:20000] if path.suffix.lower() != ".pdf" else ""
    except OSError:
        head = ""
    m = re.search(r"(Regulation|Directive)\s*\((?:EU|EC|EEC)\)\s*(?:No\s*)?(\d{2,4}/\d{2,4})", head)
    if m:
        return ("Reg " if m.group(1) == "Regulation" else "Dir ") + m.group(2)
    return path.stem


# --------------------------------------------------------------------------- embeddings + store

_client = None


def genai_client():
    global _client
    if _client is None:
        from google import genai
        from api_key import load_api_key

        _client = genai.Client(api_key=load_api_key())
    return _client


class DailyQuotaExhausted(RuntimeError):
    pass


def embed_texts(texts: list[str], task: str = "RETRIEVAL_DOCUMENT") -> list[list[float]]:
    """Embed a batch with Gemini, retrying on per-minute limits."""
    from google.genai import types

    for attempt in range(6):
        try:
            # gemini-embedding-2 is multimodal: a plain list of strings is read as the parts
            # of ONE input and returns one vector. One Content per text gives one vector each.
            contents = [types.Content(parts=[types.Part(text=t)]) for t in texts]
            try:
                cfg = types.EmbedContentConfig(output_dimensionality=EMBED_DIM, task_type=task)
                res = genai_client().models.embed_content(model=EMBED_MODEL, contents=contents, config=cfg)
            except Exception as e:  # some models reject task_type: retry without it
                if "task" not in str(e).lower():
                    raise
                cfg = types.EmbedContentConfig(output_dimensionality=EMBED_DIM)
                res = genai_client().models.embed_content(model=EMBED_MODEL, contents=contents, config=cfg)
            vecs = [list(e.values) for e in res.embeddings]
            if len(vecs) != len(texts):
                if len(texts) == 1:
                    raise RuntimeError(f"expected 1 embedding, got {len(vecs)}")
                log(f"  batch returned {len(vecs)} vectors for {len(texts)} texts: embedding one by one")
                return [v for t in texts for v in embed_texts([t], task)]
            return [_normalise(v) for v in vecs]
        except Exception as e:  # noqa: BLE001
            msg = str(e)
            if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
                if "PerDay" in msg or "per day" in msg.lower():
                    raise DailyQuotaExhausted(msg[:300]) from e
                wait = 20 * (attempt + 1)
                log(f"rate limited, waiting {wait}s")
                time.sleep(wait)
                continue
            raise
    raise RuntimeError("embedding kept failing after retries")


def _normalise(v):
    n = math.sqrt(sum(x * x for x in v)) or 1.0
    return [x / n for x in v]


def chroma():
    import chromadb

    return chromadb.PersistentClient(path=str(CHROMA_DIR))


def collection(design: str):
    return chroma().get_or_create_collection(
        name=design, embedding_function=None, metadata={"hnsw:space": "cosine"}
    )


def embed_and_store(chunks: list[dict], design: str) -> int:
    """Embed only the chunks whose id has no saved vector; save after every batch."""
    col = collection(design)
    have = set(col.get(ids=[c["id"] for c in chunks], include=[])["ids"]) if chunks else set()
    todo = [c for c in chunks if c["id"] not in have]
    # the same text can occur twice (e.g. repeated annex rows): keep one
    todo = list({c["id"]: c for c in todo}.values())
    done = 0
    for b in range(0, len(todo), BATCH):
        batch = todo[b:b + BATCH]
        vecs = embed_texts([c["text"] for c in batch])
        col.add(
            ids=[c["id"] for c in batch],
            embeddings=vecs,
            documents=[c["text"] for c in batch],
            metadatas=[{k: v for k, v in c.items() if k not in ("id", "text")} for c in batch],
        )
        done += len(batch)
        log(f"  [{design}] embedded {len(have) + done}/{len(have) + len(todo)}")
    return done


def index_file(path: str | Path, source: str | None = None, design: str | None = None,
               origin: str = "added") -> dict:
    """add_document's pipeline: chunk one file and store it in the active design.

    - same file already indexed (same content hash) -> nothing is embedded;
    - same source name but different content (a new version) -> old chunks of
      that source are deleted and the new version is indexed;
    - otherwise the chunks are embedded and added.
    """
    path = Path(path).expanduser().resolve()
    if not path.is_file():
        raise FileNotFoundError(f"No such file: {path}")
    design = design or load_config()["design"]
    source = source or guess_source(path)
    chunks = chunk_file(path, source, design, origin=origin)
    if not chunks:
        raise ValueError(f"No text could be extracted from {path.name}")
    col = collection(design)
    same = col.get(where={"doc_hash": chunks[0]["doc_hash"]}, include=["metadatas"])
    if same["ids"]:
        return {"status": "already_indexed", "source": same["metadatas"][0]["source"],
                "chunks": len(same["ids"]), "embedded": 0}
    old = col.get(where={"source": source}, include=[])["ids"]
    if old:
        col.delete(ids=old)
    embedded = embed_and_store(chunks, design)
    _BM25.pop(design, None)
    return {"status": "replaced" if old else "added", "source": source, "chunks": len(chunks),
            "embedded": embedded, "removed_old": len(old)}


# --------------------------------------------------------------------------- search

def load_config() -> dict:
    if CONFIG_FILE.exists():
        return {**DEFAULT_CONFIG, **json.loads(CONFIG_FILE.read_text())}
    return dict(DEFAULT_CONFIG)


def _load_cache() -> dict:
    if QUERY_CACHE.exists():
        return json.loads(QUERY_CACHE.read_text())
    return {}


_QCACHE: dict | None = None


def embed_query(query: str) -> list[float]:
    """Query vectors are cached in index/query_cache.json: re-running the
    evaluation costs no embedding quota."""
    global _QCACHE
    if _QCACHE is None:
        _QCACHE = _load_cache()
    key = hashlib.sha1(f"{EMBED_MODEL}|{EMBED_DIM}|{query.strip()}".encode()).hexdigest()
    if key not in _QCACHE:
        _QCACHE[key] = [round(x, 6) for x in embed_texts([query], task="RETRIEVAL_QUERY")[0]]
        QUERY_CACHE.parent.mkdir(exist_ok=True)
        QUERY_CACHE.write_text(json.dumps(_QCACHE))
    return _QCACHE[key]


TOKEN = re.compile(r"[a-z0-9]+(?:[./][a-z0-9]+)*")
STOP = set("the a an of and or to in for on is are be by with as at that this which from it its may shall "
           "not no any such these those than other into under per can what does do i my we our".split())


def tokenize(text: str) -> list[str]:
    return [t for t in TOKEN.findall(text.lower()) if t not in STOP]


class BM25:
    def __init__(self, ids, docs, k1=1.5, b=0.75):
        self.ids, self.k1, self.b = ids, k1, b
        self.toks = [Counter(tokenize(d)) for d in docs]
        self.len = [sum(t.values()) for t in self.toks]
        self.avg = sum(self.len) / max(len(self.len), 1)
        df = Counter(w for t in self.toks for w in t)
        n = len(docs)
        self.idf = {w: math.log(1 + (n - d + 0.5) / (d + 0.5)) for w, d in df.items()}

    def scores(self, query):
        q = tokenize(query)
        out = []
        for t, L in zip(self.toks, self.len):
            s = 0.0
            for w in q:
                f = t.get(w, 0)
                if f:
                    s += self.idf[w] * f * (self.k1 + 1) / (f + self.k1 * (1 - self.b + self.b * L / self.avg))
            out.append(s)
        return out


_BM25: dict[str, tuple] = {}


def _bm25(design, where):
    key = f"{design}|{json.dumps(where, sort_keys=True)}"
    if key not in _BM25:
        got = collection(design).get(where=where, include=["documents", "metadatas"])
        _BM25[key] = (BM25(got["ids"], got["documents"]), got)
    return _BM25[key]


def search(query: str, k: int = 5, design: str | None = None, mode: str | None = None,
           corpus_only: bool = False, source: str | None = None) -> list[dict]:
    """Top-k chunks. mode 'vector' (cosine), 'bm25' (keywords) or 'hybrid'
    (reciprocal-rank fusion of both). corpus_only hides documents added later;
    source restricts to one document (metadata filter)."""
    cfg = load_config()
    design, mode = design or cfg["design"], mode or cfg["mode"]
    conds = []
    if corpus_only:
        conds.append({"origin": "corpus"})
    if source:
        conds.append({"source": source})
    where = conds[0] if len(conds) == 1 else ({"$and": conds} if conds else None)
    col = collection(design)
    pool = max(k * 4, 20)
    ranked: dict[str, float] = {}
    meta: dict[str, tuple] = {}
    if mode in ("vector", "hybrid"):
        res = col.query(query_embeddings=[embed_query(query)], n_results=pool, where=where,
                        include=["documents", "metadatas", "distances"])
        for r, (i, d, m, dist) in enumerate(zip(res["ids"][0], res["documents"][0], res["metadatas"][0],
                                                res["distances"][0])):
            meta[i] = (d, m)
            ranked[i] = ranked.get(i, 0) + (1 / (60 + r) if mode == "hybrid" else 1 - dist)
    if mode in ("bm25", "hybrid"):
        bm, got = _bm25(design, where)
        sc = bm.scores(query)
        order = sorted(range(len(sc)), key=lambda j: -sc[j])[:pool]
        for r, j in enumerate(order):
            if sc[j] <= 0:
                break
            i = got["ids"][j]
            meta[i] = (got["documents"][j], got["metadatas"][j])
            ranked[i] = ranked.get(i, 0) + (1 / (60 + r) if mode == "hybrid" else sc[j])
    top = sorted(ranked, key=lambda i: -ranked[i])[:k]
    return [{"id": i, "text": meta[i][0], **meta[i][1], "score": round(ranked[i], 4)} for i in top]


def format_results(results: list[dict]) -> str:
    """How chunks are shown to a model: citation label first, then the text."""
    if not results:
        return "No passages found."
    return "\n\n".join(f"[{r['cite']}]\n{r['text']}" for r in results)


# --------------------------------------------------------------------------- main

def build(designs=("structure", "fixed")) -> None:
    INDEX_DIR.mkdir(exist_ok=True)
    paths = download_corpus()
    stats = {}
    try:
        for design in designs:
            all_chunks = []
            for source, path in paths.items():
                chunks = chunk_file(path, source, design)
                all_chunks += chunks
                stats.setdefault(design, {})[source] = len(chunks)
            log(f"[{design}] {len(all_chunks)} chunks")
            embed_and_store(all_chunks, design)
    except DailyQuotaExhausted as e:
        log(f"\nDaily embedding quota used up: {e}\nEverything embedded so far is saved. "
            f"Run `main.py index` again after 09:00 (Spain) to embed the rest.")
        raise SystemExit(2)
    words_per_doc = {s: sum(len(l.split()) for l in extract_lines(p.read_text(encoding="utf-8", errors="ignore")))
                     for s, p in paths.items()}
    (INDEX_DIR / "stats.json").write_text(json.dumps(
        {"chunks": stats, "words": words_per_doc, "total_words": sum(words_per_doc.values())}, indent=2))
    if not CONFIG_FILE.exists():
        CONFIG_FILE.write_text(json.dumps(DEFAULT_CONFIG, indent=2))
    print(f"Index ready: {json.dumps(stats)}; corpus words: {sum(words_per_doc.values())}")


if __name__ == "__main__":
    build()
