"""
Ingestion pipeline shared by index.py (main.py index) and server.py (add_document).

    parse_file(path)            EUR-Lex HTML -> document metadata + structural units
    chunk_units(units, design)  units -> chunks for one design (fixed / article / paragraph)
    embed_texts(texts)          Gemini embeddings through a content-hash cache on disk
    store_chunks(chunks)        embed what is missing and upsert into ChromaDB
    index_file(path)            all of the above for one file, for every design

A *unit* is one recital, one article paragraph (or definition point) or one
annex point, with its source and location. Every vector is written to the
SQLite cache in index/ as soon as Gemini returns it, so nothing is embedded twice.
"""

from __future__ import annotations

import hashlib
import json
import re
import sqlite3
import sys
import time
import unicodedata
from dataclasses import asdict, dataclass, field
from datetime import date
from pathlib import Path

import numpy as np
from bs4 import BeautifulSoup, Tag

ROOT = Path(__file__).resolve().parent
INDEX_DIR = ROOT / "index"
CACHE_PATH = INDEX_DIR / "embeddings.sqlite"
CHROMA_DIR = INDEX_DIR / "chroma"
MANIFEST_PATH = INDEX_DIR / "manifest.json"

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768
EMBED_BATCH = 50

# Scope decision (Phase 1): articles and annexes only; recitals are not indexed.
INDEXED_KINDS = ("article", "annex")

# Known acts: official number -> (short name, CELEX). Unknown acts fall back to the title.
KNOWN_ACTS = {
    "2016/679": ("GDPR", "32016R0679"),
    "2024/1689": ("AI Act", "32024R1689"),
    "2023/2854": ("Data Act", "32023R2854"),
    "2022/2555": ("NIS2", "32022L2555"),
}

# Units without paragraph structure longer than this are split into their points.
SPLIT_POINTS_ABOVE_WORDS = 300

PARA_ID = re.compile(r"^\d{3}\.\d{3}$")
ARTICLE_ID = re.compile(r"^art_(\d+[a-z]?)$")
ANNEX_ID = re.compile(r"^anx_([IVXLC]+)$")
RECITAL_ID = re.compile(r"^rct_(\d+)$")
LEADING_LABEL = re.compile(r"^\(?([0-9]+[a-z]?|[a-z]{1,4})[\).]\s*")


@dataclass
class Unit:
    doc: str            # short name, e.g. "GDPR"
    celex: str
    kind: str           # recital | article | annex
    ref: str            # article number, recital number or annex roman numeral
    title: str          # article or annex title ("" for recitals)
    chapter: str        # e.g. "CHAPTER III Rights of the data subject" ("" if none)
    para: str           # paragraph number or point label ("" if the whole unit)
    text: str
    order: int = 0      # position in the document, for windowing and sorting
    words: int = field(init=False)

    def __post_init__(self) -> None:
        self.words = len(self.text.split())

    @property
    def location(self) -> str:
        """Human-readable citation, e.g. 'Article 6(1)', 'Article 4, point (11)', 'Recital 32'."""
        if self.kind == "recital":
            return f"Recital {self.ref}"
        base = f"Article {self.ref}" if self.kind == "article" else f"Annex {self.ref}"
        if not self.para:
            return base
        if self.para.isdigit() and self.kind == "article":
            return f"{base}({self.para})"
        return f"{base}, point {self.para}"

    def to_dict(self) -> dict:
        d = asdict(self)
        d["location"] = self.location
        return d


# ---------------------------------------------------------------- cleaning

def clean(text: str) -> str:
    """Normalise Unicode (non-breaking and em spaces from EUR-Lex) and collapse whitespace."""
    text = unicodedata.normalize("NFKC", text)
    text = text.replace("’", "'").replace("‘", "'").replace("“", '"').replace("”", '"')
    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s+([.,;:)^])", r"\1", text)  # 'Union .' -> 'Union.', '10 ^25' -> '10^25' (left by inline tags)
    return re.sub(r"\(\s+", "(", text).strip()


def element_lines(node: Tag) -> list[str]:
    """Text of a block as lines: one per paragraph, one per list row ('(a) text')."""
    lines = []
    for child in node.children:
        if not isinstance(child, Tag):
            continue
        if child.name == "table":
            for row in child.find("tbody", recursive=False).find_all("tr", recursive=False) if child.find("tbody", recursive=False) else child.find_all("tr", recursive=False):
                cells = [clean(td.get_text(" ")) for td in row.find_all("td", recursive=False)]
                line = " ".join(c for c in cells if c)
                if line:
                    lines.append(line)
        elif child.name == "p":
            line = clean(child.get_text(" "))
            if line:
                lines.append(line)
        elif child.name == "div":
            lines.extend(element_lines(child))
    return lines


def strip_noise(soup: BeautifulSoup) -> None:
    """Remove footnotes and footnote markers, which are not part of the legal text."""
    for note in soup.select("p.oj-note, hr.oj-note"):
        note.decompose()
    for marker in soup.find_all("a", id=re.compile(r"^ntr")):
        marker.decompose()
    for marker in soup.select("span.oj-note-tag"):
        marker.decompose()
    # Superscripts carry meaning (AI Act Art. 51(2): 10^25 FLOPs); without this they read "10 25".
    for sup in soup.select("span.oj-super"):
        sup.replace_with("^" + sup.get_text(strip=True))


# ---------------------------------------------------------------- document identity

def identify(soup: BeautifulSoup, path: Path) -> tuple[str, str, str]:
    """Return (short name, CELEX, full title) of the act."""
    title_div = soup.find(id="tit_1")
    title = clean(title_div.get_text(" ")) if title_div else path.stem
    match = re.search(r"\(EU\)\s*(?:No\s*)?(\d{4}/\d+)", title)
    if match and match.group(1) in KNOWN_ACTS:
        short, celex = KNOWN_ACTS[match.group(1)]
        return short, celex, title
    paren = [p for p in re.findall(r"\(([^()]+)\)", title) if "EEA" not in p and not p.startswith("EU")]
    short = paren[-1] if paren else (match.group(1) if match else path.stem)
    return short, (match.group(1) if match else ""), title


# ---------------------------------------------------------------- structure

def chapter_of(node: Tag) -> str:
    """Title of the chapter that contains this node, e.g. 'CHAPTER III Rights of the data subject'."""
    for parent in node.parents:
        pid = parent.get("id", "") if isinstance(parent, Tag) else ""
        if re.fullmatch(r"cpt_[IVXLC]+", pid):
            heading = parent.find(id=f"{pid}.tit_1")
            label = parent.find("p", class_="oj-ti-section-1")
            parts = [clean(label.get_text(" ")) if label else "", clean(heading.get_text(" ")) if heading else ""]
            return " ".join(p for p in parts if p)
    return ""


def split_points(lines: list[str]) -> list[tuple[str, str]]:
    """Split the lines of an unstructured block into (point label, text) pairs.

    A line that starts with a label like '(11)' or '1.' opens a new point; lines
    without a label belong to the previous point. Text before the first label
    becomes an unlabelled intro point.
    """
    points: list[tuple[str, list[str]]] = []
    for line in lines:
        m = LEADING_LABEL.match(line)
        top_level = m and (m.group(1).isdigit() or not points)
        if top_level:
            points.append((f"({m.group(1)})" if m.group(1).isdigit() else m.group(1), [line]))
        elif points:
            points[-1][1].append(line)
        else:
            points.append(("", [line]))
    return [(label, " ".join(text)) for label, text in points]


def parse_recitals(soup: BeautifulSoup, doc: str, celex: str) -> list[Unit]:
    units = []
    for div in soup.find_all(id=RECITAL_ID):
        num = RECITAL_ID.match(div["id"]).group(1)
        text = " ".join(element_lines(div))
        text = re.sub(rf"^\({num}\)\s*", "", text)
        units.append(Unit(doc, celex, "recital", num, "", "", "", text))
    return units


def parse_articles(soup: BeautifulSoup, doc: str, celex: str) -> list[Unit]:
    units = []
    for div in soup.find_all(id=ARTICLE_ID):
        num = ARTICLE_ID.match(div["id"]).group(1)
        sub = div.find("p", class_="oj-sti-art")
        title = clean(sub.get_text(" ")) if sub else ""
        chapter = chapter_of(div)
        paras = [p for p in div.find_all("div", id=PARA_ID, recursive=False)]
        if paras:
            for p in paras:
                pnum = str(int(p["id"].split(".")[1]))
                units.append(Unit(doc, celex, "article", num, title, chapter, pnum, " ".join(element_lines(p))))
            continue
        # No numbered paragraphs: the body is everything except the two headings.
        body = [c for c in div.children if isinstance(c, Tag) and "oj-ti-art" not in (c.get("class") or []) and c.get("id") != f"{div['id']}.tit_1"]
        lines = []
        for c in body:
            lines.extend(element_lines(c) if c.name == "div" else element_lines(_wrap(c)))
        text = " ".join(lines)
        if len(text.split()) > SPLIT_POINTS_ABOVE_WORDS:
            for label, ptext in split_points(lines):
                units.append(Unit(doc, celex, "article", num, title, chapter, label, ptext))
        else:
            units.append(Unit(doc, celex, "article", num, title, chapter, "", text))
    return units


def parse_annexes(soup: BeautifulSoup, doc: str, celex: str) -> list[Unit]:
    units = []
    for div in soup.find_all(id=ANNEX_ID):
        roman = ANNEX_ID.match(div["id"]).group(1)
        heads = div.find_all("p", class_="oj-doc-ti", limit=2)
        title = clean(heads[1].get_text(" ")) if len(heads) > 1 else ""
        lines = []
        for c in div.children:
            if isinstance(c, Tag) and "oj-doc-ti" not in (c.get("class") or []):
                lines.extend(element_lines(c) if c.name == "div" else element_lines(_wrap(c)))
        text = " ".join(lines)
        if len(text.split()) > SPLIT_POINTS_ABOVE_WORDS:
            for label, ptext in split_points(lines):
                units.append(Unit(doc, celex, "annex", roman, title, "", label, ptext))
        else:
            units.append(Unit(doc, celex, "annex", roman, title, "", "", text))
    return units


def _wrap(tag: Tag) -> Tag:
    """Wrap a single element in a div so element_lines can walk it."""
    holder = BeautifulSoup("<div></div>", "html.parser").div
    holder.append(tag.__copy__())
    return holder


def parse_file(path: str | Path) -> tuple[dict, list[Unit]]:
    """Parse one EUR-Lex HTML file into (document metadata, ordered units)."""
    path = Path(path)
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    strip_noise(soup)
    doc, celex, title = identify(soup, path)
    units = parse_recitals(soup, doc, celex) + parse_articles(soup, doc, celex) + parse_annexes(soup, doc, celex)
    for i, u in enumerate(units):
        u.order = i
    meta = {"doc": doc, "celex": celex, "title": title, "file": path.name}
    return meta, units


# ================================================================ chunking designs

DESIGNS = ("fixed", "article", "paragraph")
FIXED_WORDS, FIXED_OVERLAP = 150, 30       # design "fixed": sliding window over the document
ARTICLE_MAX_WORDS = 1200                   # design "article": longer articles split into parts
PARAGRAPH_MIN_WORDS = 100                  # design "paragraph": merge small paragraphs up to this
PARAGRAPH_TAIL_WORDS = 40                  # a last piece shorter than this joins the previous one


@dataclass
class Chunk:
    design: str
    doc: str
    celex: str
    kind: str
    ref: str              # article number / annex numeral where the chunk starts
    title: str
    chapter: str
    location: str         # citation, e.g. "Article 6(1)-(2)"
    covers: str           # every article/annex the chunk touches, "|"-separated: "Article 5|Article 6"
    body: str             # legal text only
    source_file: str
    order: int

    @property
    def header(self) -> str:
        return f"{self.doc} {self.location}" + (f" - {self.title}" if self.title else "")

    @property
    def text(self) -> str:
        """What is embedded and shown: a citation header, then the legal text."""
        return f"{self.header}\n{self.body}"

    @property
    def words(self) -> int:
        return len(self.body.split())

    @property
    def id(self) -> str:
        return f"{self.design}:{content_hash(self.text)[:16]}"

    def metadata(self) -> dict:
        return {
            "design": self.design, "doc": self.doc, "celex": self.celex, "kind": self.kind,
            "ref": self.ref, "title": self.title, "chapter": self.chapter, "location": self.location,
            "covers": self.covers, "source_file": self.source_file, "order": self.order,
            "words": self.words, "hash": content_hash(self.text),
        }


def _base(u: Unit) -> str:
    return f"Article {u.ref}" if u.kind == "article" else f"Annex {u.ref}"


def _span_location(group: list[Unit], whole: bool) -> str:
    """Citation for a run of consecutive units of the same article or annex."""
    first, last = group[0], group[-1]
    if whole or (len(group) == 1 and not first.para):
        return _base(first)
    if len(group) == 1:
        return first.location
    a, b = first.para or "intro", last.para
    if first.kind == "article" and a.isdigit() and b.isdigit():
        return f"{_base(first)}({a})-({b})"
    return f"{_base(first)}, points {a} to {b}"


def _groups_by_section(units: list[Unit]) -> list[list[Unit]]:
    """Consecutive units of the same article/annex, in document order."""
    groups: list[list[Unit]] = []
    for u in units:
        if groups and (groups[-1][0].kind, groups[-1][0].ref) == (u.kind, u.ref):
            groups[-1].append(u)
        else:
            groups.append([u])
    return groups


def _make(design: str, group: list[Unit], whole: bool, source_file: str, order: int) -> Chunk:
    u = group[0]
    return Chunk(design, u.doc, u.celex, u.kind, u.ref, u.title, u.chapter,
                 _span_location(group, whole), _base(u),
                 " ".join(x.text for x in group), source_file, order)


def chunk_article(units: list[Unit], source_file: str) -> list[Chunk]:
    """One chunk per article/annex; very long ones are cut into parts at paragraph boundaries."""
    chunks = []
    for section in _groups_by_section(units):
        parts, cur = [], []
        for u in section:
            if cur and sum(x.words for x in cur) + u.words > ARTICLE_MAX_WORDS:
                parts.append(cur)
                cur = []
            cur.append(u)
        parts.append(cur)
        for part in parts:
            chunks.append(_make("article", part, len(parts) == 1, source_file, len(chunks)))
    return chunks


def chunk_paragraph(units: list[Unit], source_file: str) -> list[Chunk]:
    """Paragraph-level chunks: consecutive small paragraphs of one article merged up to ~100 words."""
    chunks = []
    for section in _groups_by_section(units):
        pieces, cur = [], []
        for u in section:
            cur.append(u)
            if sum(x.words for x in cur) >= PARAGRAPH_MIN_WORDS:
                pieces.append(cur)
                cur = []
        if cur:
            if pieces and sum(x.words for x in cur) < PARAGRAPH_TAIL_WORDS:
                pieces[-1].extend(cur)
            else:
                pieces.append(cur)
        for piece in pieces:
            chunks.append(_make("paragraph", piece, len(pieces) == 1, source_file, len(chunks)))
    return chunks


def chunk_fixed(units: list[Unit], source_file: str) -> list[Chunk]:
    """Naive baseline: a 150-word window sliding over the whole document, ignoring structure.

    Each window is labelled with the unit where it starts and records every
    article/annex it overlaps, so hit rate can still be measured.
    """
    words, owner = [], []          # every word and the unit it belongs to
    for i, u in enumerate(units):
        for w in u.text.split():
            words.append(w)
            owner.append(i)
    chunks, step = [], FIXED_WORDS - FIXED_OVERLAP
    for start in range(0, max(len(words) - FIXED_OVERLAP, 1), step):
        end = min(start + FIXED_WORDS, len(words))
        touched = list(dict.fromkeys(owner[start:end]))
        first = units[touched[0]]
        covers = "|".join(dict.fromkeys(_base(units[i]) for i in touched))
        chunks.append(Chunk("fixed", first.doc, first.celex, first.kind, first.ref, first.title, first.chapter,
                            first.location, covers, " ".join(words[start:end]), source_file, len(chunks)))
    return chunks


def chunk_units(units: list[Unit], design: str, source_file: str = "") -> list[Chunk]:
    units = [u for u in units if u.kind in INDEXED_KINDS and u.words > 0]
    if design == "fixed":
        return chunk_fixed(units, source_file)
    if design == "article":
        return chunk_article(units, source_file)
    if design == "paragraph":
        return chunk_paragraph(units, source_file)
    raise ValueError(f"Unknown design {design!r}; expected one of {DESIGNS}")


# ================================================================ embedding cache

class QuotaExhausted(RuntimeError):
    """The daily embedding quota is used up. Vectors obtained so far are already saved."""


def log(msg: str) -> None:
    print(msg, file=sys.stderr, flush=True)   # stderr: stdout carries the MCP protocol in server.py


def content_hash(text: str, task: str = "RETRIEVAL_DOCUMENT") -> str:
    return hashlib.sha256(f"{EMBED_MODEL}|{EMBED_DIM}|{task}|{text}".encode("utf-8")).hexdigest()


def _cache() -> sqlite3.Connection:
    INDEX_DIR.mkdir(exist_ok=True)
    con = sqlite3.connect(CACHE_PATH)
    con.execute("CREATE TABLE IF NOT EXISTS vectors (hash TEXT PRIMARY KEY, task TEXT, dim INTEGER, vector BLOB, created TEXT)")
    return con


def cached_vectors(hashes: list[str]) -> dict[str, np.ndarray]:
    found = {}
    con = _cache()
    try:
        for i in range(0, len(hashes), 500):
            batch = hashes[i:i + 500]
            rows = con.execute(f"SELECT hash, vector FROM vectors WHERE hash IN ({','.join('?' * len(batch))})", batch)
            found.update({h: np.frombuffer(v, dtype=np.float32) for h, v in rows})
    finally:
        con.close()
    return found


_client = None


def _gemini():
    global _client
    if _client is None:
        from google import genai
        from api_key import load_api_key
        _client = genai.Client(api_key=load_api_key())
    return _client


def _embed_batch(texts: list[str], task: str) -> list[np.ndarray]:
    """One API call, retrying on per-minute rate limits; raises QuotaExhausted on the daily one."""
    from google.genai import types
    from google.genai.errors import ClientError
    daily_hits = 0
    for attempt in range(8):
        try:
            # gemini-embedding-2 is multimodal: a plain list of strings is read as ONE
            # content with many parts and returns ONE vector. Wrap each text in its own Content.
            contents = [types.Content(parts=[types.Part(text=t)]) for t in texts]
            r = _gemini().models.embed_content(
                model=EMBED_MODEL, contents=contents,
                config=types.EmbedContentConfig(task_type=task, output_dimensionality=EMBED_DIM))
            if len(r.embeddings) != len(texts):
                raise RuntimeError(f"Asked for {len(texts)} embeddings, got {len(r.embeddings)}; not saving them.")
            return [np.asarray(e.values, dtype=np.float32) for e in r.embeddings]
        except ClientError as e:
            if e.code != 429:
                raise
            msg = str(e)
            m = re.search(r"retry in ([\d.]+)s", msg) or re.search(r"retryDelay.{0,5}?(\d+)s", msg)
            wait = float(m.group(1)) + 1 if m else 20 * (attempt + 1)
            if wait > 120:   # a per-minute limit never asks for minutes of waiting: this is the daily one
                raise QuotaExhausted(f"Gemini asks to wait {wait:.0f}s: daily embedding quota reached (resets 09:00 Spain time).") from e
            wait = min(wait, 70)
            # A per-minute 429 can also mention per-day metrics, so only give up after
            # the "daily" message survives two one-minute waits.
            if "PerDay" in msg or "per day" in msg.lower():
                daily_hits += 1
                log(f"  429 mentioning a daily limit ({daily_hits}/3): {msg[:300]}")
                if daily_hits >= 3:
                    raise QuotaExhausted("Daily embedding quota reached (resets 09:00 Spain time).") from e
                wait = max(wait, 65)
            log(f"  rate limited, waiting {wait:.0f}s")
            time.sleep(wait)
    raise QuotaExhausted("Still rate limited after several retries; try again later.")


def embed_texts(texts: list[str], task: str = "RETRIEVAL_DOCUMENT", budget: int | None = None) -> list[np.ndarray | None]:
    """Vectors for texts, from the cache when possible; new ones are saved batch by batch.

    `budget` caps how many new texts are embedded in this call; texts beyond it
    come back as None. Returns vectors in input order.
    """
    hashes = [content_hash(t, task) for t in texts]
    have = cached_vectors(list(dict.fromkeys(hashes)))
    todo = list(dict.fromkeys(h for h in hashes if h not in have))
    if budget is not None:
        todo = todo[:max(budget, 0)]
    by_hash = dict(zip(hashes, texts))
    for i in range(0, len(todo), EMBED_BATCH):
        batch = todo[i:i + EMBED_BATCH]
        vectors = _embed_batch([by_hash[h] for h in batch], task)
        con = _cache()                          # saved before the next request
        try:
            with con:
                con.executemany("INSERT OR REPLACE INTO vectors VALUES (?, ?, ?, ?, ?)",
                                [(h, task, EMBED_DIM, v.tobytes(), date.today().isoformat()) for h, v in zip(batch, vectors)])
        finally:
            con.close()
        have.update(zip(batch, vectors))
        log(f"  embedded {min(i + EMBED_BATCH, len(todo))}/{len(todo)} new texts")
    return [have.get(h) for h in hashes]


def embed_query(query: str) -> np.ndarray:
    return embed_texts([query], task="RETRIEVAL_QUERY")[0]


# ================================================================ vector store

def chroma():
    import chromadb
    from chromadb.config import Settings
    CHROMA_DIR.mkdir(parents=True, exist_ok=True)
    return chromadb.PersistentClient(path=str(CHROMA_DIR), settings=Settings(anonymized_telemetry=False))


def collection(design: str, client=None):
    client = client or chroma()
    return client.get_or_create_collection(name=f"eu_{design}", metadata={"hnsw:space": "cosine", "design": design})


def store_chunks(chunks: list[Chunk], budget: int | None = None, client=None) -> dict:
    """Embed the chunks that have no saved vector and upsert all of them into their design's collection.

    Returns counts: total chunks, newly embedded, stored, missing (not embedded because of budget).
    """
    if not chunks:
        return {"chunks": 0, "new": 0, "stored": 0, "missing": 0}
    before = set(cached_vectors([content_hash(c.text) for c in chunks]))
    vectors = embed_texts([c.text for c in chunks], budget=budget)
    ready = [(c, v) for c, v in zip(chunks, vectors) if v is not None]
    by_design: dict[str, list] = {}
    for c, v in ready:
        by_design.setdefault(c.design, []).append((c, v))
    for design, items in by_design.items():
        col = collection(design, client)
        unique = list({c.id: (c, v) for c, v in items}.values())
        # Skip chunks already stored: every upsert is logged inside chroma.sqlite3 and grows index/.
        existing = set(col.get(ids=[c.id for c, _ in unique], include=[])["ids"]) if unique else set()
        unique = [(c, v) for c, v in unique if c.id not in existing]
        for i in range(0, len(unique), 500):
            part = unique[i:i + 500]
            col.upsert(ids=[c.id for c, _ in part], embeddings=[v.tolist() for _, v in part],
                       documents=[c.text for c, _ in part], metadatas=[c.metadata() for c, _ in part])
    new = len({content_hash(c.text) for c, _ in ready} - before)
    return {"chunks": len(chunks), "new": new, "stored": len(ready), "missing": len(chunks) - len(ready)}


def chunk_file(path: str | Path, designs=DESIGNS) -> tuple[dict, list[Chunk]]:
    """Parse one file and chunk it with every requested design."""
    meta, units = parse_file(path)
    chunks = [c for d in designs for c in chunk_units(units, d, Path(path).name)]
    return meta, chunks


def index_file(path: str | Path, designs=DESIGNS, budget: int | None = None, client=None) -> dict:
    """Run one file through the whole pipeline: parse, chunk, embed what is missing, store."""
    meta, chunks = chunk_file(path, designs)
    stats = store_chunks(chunks, budget=budget, client=client)
    return {**meta, **stats}


# ================================================================ add a document (used by server.py)

def add_document(path: str | Path, designs=DESIGNS, client=None) -> dict:
    """Index one more EUR-Lex HTML act, with the duplicate policy decided in Phase 5.

    The act is identified by its CELEX number (or file name if it has none):
      - same act, identical chunks  -> "already indexed", nothing embedded or written;
      - same act, different chunks  -> "replaced": new chunks stored (unchanged text reuses
        cached vectors, so only changed chunks cost quota), outdated chunks deleted;
      - new act                     -> "added".
    Old chunks are only deleted once every new chunk is stored, so a quota stop
    never leaves the act half-replaced.
    """
    path = Path(path)
    meta, units = parse_file(path)
    if not any(u.kind in INDEXED_KINDS for u in units):
        raise ValueError(f"{path.name}: no articles or annexes found; add_document expects an EUR-Lex HTML act.")
    client = client or chroma()
    key = {"celex": meta["celex"]} if meta["celex"] else {"source_file": path.name}
    report = {"doc": meta["doc"], "celex": meta["celex"], "title": meta["title"], "designs": {}}
    for design in designs:
        chunks = chunk_units(units, design, path.name)
        col = collection(design, client)
        existing = set(col.get(where=key, include=[])["ids"])
        new_ids = {c.id for c in chunks}
        if existing == new_ids:
            report["designs"][design] = {"status": "already indexed", "chunks": len(chunks), "new_embeddings": 0}
            continue
        stats = store_chunks(chunks, client=client)
        removed = 0
        if stats["missing"] == 0 and existing - new_ids:
            col.delete(ids=list(existing - new_ids))
            removed = len(existing - new_ids)
        status = "incomplete" if stats["missing"] else ("replaced" if existing else "added")
        report["designs"][design] = {"status": status, "chunks": len(chunks), "new_embeddings": stats["new"],
                                     "removed_outdated": removed}
    if any(r["status"] != "already indexed" for r in report["designs"].values()):
        _record_added(path, report)
    return report


def _record_added(path: Path, report: dict) -> None:
    """Note documents added after the initial build in index/manifest.json."""
    manifest = json.loads(MANIFEST_PATH.read_text()) if MANIFEST_PATH.is_file() else {}
    added = manifest.setdefault("added_documents", {})
    added[path.name] = {"doc": report["doc"], "celex": report["celex"],
                        "designs": {d: r["status"] for d, r in report["designs"].items()},
                        "date": date.today().isoformat()}
    MANIFEST_PATH.write_text(json.dumps(manifest, indent=2))
