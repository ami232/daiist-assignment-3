"""
Assignment 3: build the index (`main.py index`).

Pipeline: download (corpus/, git-ignored) -> extract -> clean -> chunk with
source and location -> embed with Gemini -> store in index/.

Two chunking designs are built so evaluate.py can compare them by hit rate:

  article  structure-based: one chunk per article / recital / annex, long ones
           split at paragraph boundaries. Header carries source + location.
  fixed    baseline: sliding window of FIXED_WORDS words, ignoring structure.

Storage (index/<design>/chunks.jsonl): one JSON line per chunk with its text,
metadata and vector, appended as soon as a batch is embedded. A crash or the
daily quota therefore loses nothing, and a rerun embeds only chunks that have
no saved vector (chunk ids contain a hash of the text).

server.py imports `chunk_file`, `embed_and_store` and `index_file` from here.

    uv run python index.py              # same as `main.py index`
    uv run python index.py --stats      # words and chunks per document, no API calls
    uv run python index.py --list       # every chunk's source | location | title, to write test questions
    uv run python index.py --show "GDPR Article 33"   # print matching chunks in full
"""

from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
import sys
import time
import warnings
from dataclasses import dataclass, field
from datetime import datetime, timezone
from pathlib import Path

import httpx
from bs4 import BeautifulSoup, NavigableString, Tag, XMLParsedAsHTMLWarning

warnings.filterwarnings("ignore", category=XMLParsedAsHTMLWarning)

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
# RAG_INDEX_DIR lets a demo run on a throw-away copy (see before_after.py).
INDEX_DIR = Path(os.environ.get("RAG_INDEX_DIR") or ROOT / "index")

# ---------------------------------------------------------------- settings --
EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768          # 128..3072 allowed; 768 keeps index/ small
EMBED_BATCH = 16         # texts per API call (every text counts against the daily quota)

DESIGNS = ("article", "fixed")
CHOSEN_DESIGN = "article"        # what server.py searches; decided in REPORT.md by the numbers
ARTICLE_MAX_WORDS = 450          # an article up to this size stays in one chunk
ARTICLE_TARGET_WORDS = 300       # when it is longer, paragraphs are packed up to about this
FIXED_WORDS = 250                # baseline window: about the size of an article chunk, so the comparison isolates structure
FIXED_OVERLAP = 25

ALLOWED_SUFFIXES = {".xhtml", ".html", ".htm", ".pdf", ".txt", ".md"}
MAX_FILE_MB = 25


@dataclass(frozen=True)
class Doc:
    key: str                    # slug, also the file name in corpus/
    source: str                 # short name used in citations and in questions.csv
    title: str
    celex: str                  # CELEX number on EUR-Lex
    date: str                   # date of the act
    include_recitals: bool = False
    indexed: bool = True        # False: downloaded but kept out of the first index (add_document demo)

    @property
    def path(self) -> Path:
        return CORPUS_DIR / f"{self.key}.xhtml"

    @property
    def url(self) -> str:
        return f"https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:{self.celex}"


LICENCE = (
    "(c) European Union, reuse authorised with acknowledgement of the source "
    "(Commission Decision 2011/833/EU; see the EUR-Lex legal notice). No personal data."
)

# Edit this list to change the corpus. Recitals double the number of chunks for
# little extra value in a compliance question-answering setting, so they start off.
DOCS: list[Doc] = [
    Doc("ai-act", "AI Act", "Regulation (EU) 2024/1689 (Artificial Intelligence Act)", "32024R1689", "2024-06-13"),
    Doc("gdpr", "GDPR", "Regulation (EU) 2016/679 (General Data Protection Regulation)", "32016R0679", "2016-04-27"),
    Doc("data-act", "Data Act", "Regulation (EU) 2023/2854 (Data Act)", "32023R2854", "2023-12-13"),
    # Held out of the first index: write an unanswerable question about it, then add it with add_document.
    Doc("nis2", "NIS2", "Directive (EU) 2022/2555 (NIS2)", "32022L2555", "2022-12-14", indexed=False),
]


# ------------------------------------------------------------ data classes --
@dataclass
class Item:
    """A paragraph, list point or block of text inside a unit."""
    text: str
    kind: str = ""      # "para" (1.), "point" ((1) / (a)) or "" (unnumbered)
    num: str = ""

    @property
    def words(self) -> int:
        return len(self.text.split())


@dataclass
class Unit:
    """One structural unit of a document: an article, a recital, an annex, a page..."""
    label: str                  # "Article 5", "Recital 12", "Annex III", "p. 4"
    title: str = ""
    chapter: str = ""
    items: list[Item] = field(default_factory=list)

    @property
    def words(self) -> int:
        return sum(i.words for i in self.items)


# --------------------------------------------------------------- cleaning ---
_WS = re.compile(r"[ \t\r\f\v   ]+")


def clean(text: str) -> str:
    # soft hyphen and zero-width space are layout leftovers; one article title in the official file ends in a stray grave accent
    for junk in ("\u00ad", "\u200b", "`"):
        text = text.replace(junk, "")
    return _WS.sub(" ", text).strip()


def words_of(text: str) -> int:
    return len(text.split())


# ------------------------------------------------- EU official-journal HTML --
def _classes(tag: Tag) -> list[str]:
    return tag.get("class") or []


def _text(tag: Tag) -> str:
    for br in tag.find_all("br"):
        br.replace_with(" ")
    for sup in tag.find_all("span", class_="oj-super"):
        before = sup.previous_sibling
        if isinstance(before, NavigableString) and before.rstrip()[-1:].isdigit():
            sup.replace_with("^" + sup.get_text())  # 10<sup>25</sup> must not read "1025"; footnote marks "(1)" are left alone
    return clean(tag.get_text(""))


def _flatten_node(node, depth: int = 0) -> list[str]:
    """Lines of one node. Lists (tables of marker | text) keep their marker."""
    if not isinstance(node, Tag):
        return []
    if node.name == "p":
        if any("note" in c for c in _classes(node)):
            return []  # footnotes: bibliographic references, not content
        t = _text(node)
        return ["  " * depth + t] if t else []
    if node.name == "table":
        lines: list[str] = []
        for tr in node.find_all("tr"):
            if tr.find_parent("table") is not node:
                continue  # rows of nested tables are handled by the recursion below
            cells = tr.find_all("td", recursive=False)
            if len(cells) == 2:
                marker = _text(cells[0])
                body = _flatten(cells[1], depth + 1 if _MARKER_ONLY.match(marker) is None else depth)
                if body:
                    body[0] = "  " * depth + f"{marker} {body[0].lstrip()}".rstrip()
                    lines.extend(body)
            else:
                for cell in cells:
                    lines.extend(_flatten(cell, depth))
        return lines
    if node.name in {"div", "td", "span", "section"}:
        return _flatten(node, depth)
    if node.name in {"ul", "ol"}:
        return ["  " * depth + "- " + t for li in node.find_all("li", recursive=False) if (t := _text(li))]
    return []


def _flatten(el: Tag, depth: int = 0) -> list[str]:
    lines: list[str] = []
    for child in el.children:
        lines.extend(_flatten_node(child, depth))
    return lines


_MARKER_ONLY = re.compile(r"^(\(?[0-9a-zA-Z]{1,5}[.)]|—|–|-|•)$")


_PARA = re.compile(r"^(\d+)\.\s")
_POINT = re.compile(r"^\(([0-9]+|[a-z]{1,4}|[ivx]{1,5})\)\s")


def _marker(first_line: str) -> tuple[str, str]:
    s = first_line.strip()
    if m := _PARA.match(s):
        return "para", m.group(1)
    if m := _POINT.match(s):
        return "point", m.group(1)
    return "", ""


def _item(lines: list[str]) -> Item | None:
    lines = [l for l in lines if l.strip()]
    if not lines:
        return None
    kind, num = _marker(lines[0])
    return Item("\n".join(lines), kind, num)


def _head(div: Tag | None) -> str:
    """'CHAPTER III - HIGH-RISK AI SYSTEMS' from a chapter or section div."""
    if div is None:
        return ""
    label = next((c for c in div.children if isinstance(c, Tag) and c.name == "p"), None)
    title = next((c for c in div.children if isinstance(c, Tag) and "eli-title" in _classes(c)), None)
    parts = [_text(x) for x in (label, title) if x is not None]
    return " - ".join(p for p in parts if p)


def parse_eu_html(html: str, include_recitals: bool = False) -> list[Unit]:
    """Units of an EU act as served by the Publications Office (XHTML)."""
    soup = BeautifulSoup(html, "html.parser")
    ids = re.compile(r"^(rct_\d+|art_\d+[a-z]?|anx_[A-Za-z0-9]+)$")
    units: list[Unit] = []
    for div in soup.find_all("div", id=ids):
        ident = div["id"]
        if ident.startswith("rct_"):
            if not include_recitals:
                continue
            lines = _flatten(div)
            if lines:
                lines[0] = re.sub(r"^\(\d+\)\s*", "", lines[0])
            item = _item(lines)
            if item:
                item.kind, item.num = "", ""
                units.append(Unit(f"Recital {ident[4:]}", "", "", [item]))
        elif ident.startswith("art_"):
            label_p = div.find("p", class_="oj-ti-art", recursive=False)
            title_div = div.find("div", class_="eli-title", recursive=False)
            label = _text(label_p) if label_p else f"Article {ident[4:]}"
            title = _text(title_div) if title_div else ""
            chap = div.find_parent("div", id=re.compile(r"^cpt_[A-Za-z0-9]+$"))
            sect = div.find_parent("div", id=re.compile(r"^cpt_[A-Za-z0-9]+\.sct_\d+$"))
            chapter = " / ".join(x for x in (_head(chap), _head(sect)) if x)
            unit = Unit(label, title, chapter)
            for child in div.children:
                if not isinstance(child, Tag) or child is label_p or child is title_div:
                    continue
                item = _item(_flatten_node(child))
                if item:
                    unit.items.append(item)
            if unit.items:
                units.append(unit)
        else:  # annex
            heads = [c for c in div.children if isinstance(c, Tag) and c.name == "p" and "oj-doc-ti" in _classes(c)]
            label = re.sub(r"^ANNEX", "Annex", _text(heads[0])) if heads else f"Annex {ident[4:]}"
            title = " ".join(_text(h) for h in heads[1:])
            unit = Unit(label, title, "")
            for child in div.children:
                if not isinstance(child, Tag) or child in heads:
                    continue
                if child.name == "table":
                    # each top-level row of an annex list is its own item
                    for tr in child.find_all("tr"):
                        if tr.find_parent("table") is not child:
                            continue
                        cells = tr.find_all("td", recursive=False)
                        if len(cells) == 2:
                            marker = _text(cells[0])
                            body = _flatten(cells[1])
                            if body:
                                body[0] = f"{marker} {body[0].lstrip()}"
                                item = _item(body)
                                if item:
                                    unit.items.append(item)
                else:
                    item = _item(_flatten_node(child))
                    if item:
                        unit.items.append(item)
            if unit.items:
                units.append(unit)
    return units


# ------------------------------------------------------- generic text / PDF --
_HEADING = re.compile(
    r"^(?P<article>Article\s+\d+[a-z]?)\s*$|^(?P<annex>ANNEX\s+[IVXLC\d]+)\b.*$|^#{1,4}\s+(?P<md>.+)$|^(?P<num>\d+(?:\.\d+)*)\s+(?P<numtitle>[A-Z][^.]{2,80})$",
)


def parse_text_pages(pages: list[tuple[int, str]]) -> list[Unit]:
    """Units from plain text: headings (Article N, ANNEX X, '# title', '3.2 Title') or, failing that, pages."""
    lines: list[tuple[int, str]] = []
    for page_no, text in pages:
        for raw in text.splitlines():
            line = clean(raw)
            if line:
                lines.append((page_no, line))
    headings = sum(1 for _, l in lines if _HEADING.match(l))
    units: list[Unit] = []
    if headings >= 3:
        cur: Unit | None = None
        for page_no, line in lines:
            m = _HEADING.match(line)
            if m:
                if cur and cur.items:
                    units.append(cur)
                if m.group("article"):
                    label = m.group("article")
                elif m.group("annex"):
                    label = re.sub(r"^ANNEX", "Annex", m.group("annex"))
                elif m.group("md"):
                    label = m.group("md").strip()
                else:
                    label = f"Section {m.group('num')}"
                cur = Unit(f"{label} (p. {page_no})", m.group("numtitle") or "", "")
            elif cur is None:
                cur = Unit(f"p. {page_no}")
                cur.items.append(Item(line))
            else:
                cur.items.append(Item(line))
        if cur and cur.items:
            units.append(cur)
    else:
        by_page: dict[int, Unit] = {}
        for page_no, line in lines:
            by_page.setdefault(page_no, Unit(f"p. {page_no}")).items.append(Item(line))
        units = list(by_page.values())
    # merge consecutive lines into paragraphs of reasonable size (lines are PDF line wraps)
    for u in units:
        merged: list[Item] = []
        buf: list[str] = []
        for it in u.items:
            buf.append(it.text)
            if re.search(r"[.:;?!]$", it.text) and words_of(" ".join(buf)) >= 40:
                merged.append(Item(" ".join(buf)))
                buf = []
        if buf:
            merged.append(Item(" ".join(buf)))
        u.items = merged
    return units


def extract_units(path: Path, doc: Doc | None = None) -> list[Unit]:
    suffix = path.suffix.lower()
    if suffix in {".xhtml", ".html", ".htm"}:
        html = path.read_text(encoding="utf-8", errors="replace")
        if re.search(r'id="art_\d+', html):
            return parse_eu_html(html, include_recitals=bool(doc and doc.include_recitals))
        soup = BeautifulSoup(html, "html.parser")
        for tag in soup(["script", "style", "nav", "header", "footer"]):
            tag.decompose()
        return parse_text_pages([(1, soup.get_text("\n"))])
    if suffix == ".pdf":
        from pypdf import PdfReader

        reader = PdfReader(str(path))
        return parse_text_pages([(i + 1, page.extract_text() or "") for i, page in enumerate(reader.pages)])
    if suffix in {".txt", ".md"}:
        return parse_text_pages([(1, path.read_text(encoding="utf-8", errors="replace"))])
    raise ValueError(f"Unsupported file type {suffix!r}; use one of {sorted(ALLOWED_SUFFIXES)}")


# ---------------------------------------------------------------- chunking ---
def _fmt_location(label: str, items: list[Item], part: tuple[int, int] | None = None) -> str:
    marks = [(i.kind, i.num) for i in items if i.kind]
    if marks:
        same = [m for m in marks if m[1].isdigit() == marks[0][1].isdigit()]
        marks = same or marks
    loc = label
    if marks:
        (k1, a), (_, b) = marks[0], marks[-1]
        if label.startswith("Annex"):
            loc = f"{label}, point {a}" if a == b else f"{label}, points {a}-{b}"
        elif k1 == "para":
            loc = f"{label}({a})" if a == b else f"{label}({a})-({b})"
        else:
            loc = f"{label}, point ({a})" if a == b else f"{label}, points ({a})-({b})"
    if part and part[1] > 1:
        loc += f" (part {part[0]}/{part[1]})"
    return loc


def _split_long(item: Item, target: int) -> list[Item]:
    """Split one oversized item at line boundaries, then at sentence boundaries."""
    pieces: list[str] = []
    for line in item.text.split("\n"):
        if words_of(line) > target:
            pieces.extend(s for s in re.split(r"(?<=[.;:])\s+", line) if s)
        else:
            pieces.append(line)
    out: list[Item] = []
    buf: list[str] = []
    for p in pieces:
        if buf and words_of(" ".join(buf + [p])) > target:
            out.append(Item("\n".join(buf), item.kind, item.num))
            buf = []
        buf.append(p)
    if buf:
        out.append(Item("\n".join(buf), item.kind, item.num))
    return out


def _pack(items: list[Item], target: int) -> list[list[Item]]:
    groups: list[list[Item]] = []
    cur: list[Item] = []
    cur_w = 0
    for it in items:
        parts = _split_long(it, target) if it.words > ARTICLE_MAX_WORDS else [it]
        for p in parts:
            if cur and cur_w + p.words > target:
                groups.append(cur)
                cur, cur_w = [], 0
            cur.append(p)
            cur_w += p.words
    if cur:
        groups.append(cur)
    # a tiny tail is merged into the previous group
    if len(groups) > 1 and sum(i.words for i in groups[-1]) < 60:
        groups[-2].extend(groups.pop())
    return groups


def _make_chunk(doc: Doc, design: str, location: str, units: list[str], header: str, body: str, title: str, chapter: str) -> dict:
    digest = hashlib.sha1(f"{header}\n{body}".encode()).hexdigest()[:10]
    slug = re.sub(r"[^a-z0-9]+", "-", location.lower()).strip("-")
    return {
        "id": f"{design}:{doc.key}:{slug}:{digest}",
        "design": design,
        "doc": doc.key,
        "source": doc.source,
        "source_title": doc.title,
        "location": location,
        "units": units,
        "title": title,
        "chapter": chapter,
        "header": header,
        "body": body,
        "text": f"{header}\n{body}",
        "words": words_of(body),
    }


def chunks_article(doc: Doc, units: list[Unit]) -> list[dict]:
    chunks: list[dict] = []
    for u in units:
        groups = [u.items] if u.words <= ARTICLE_MAX_WORDS else _pack(u.items, ARTICLE_TARGET_WORDS)
        for n, group in enumerate(groups, 1):
            if len(groups) == 1:
                location = u.label
            else:
                location = _fmt_location(u.label, group, (n, len(groups)))
            header = f"{doc.source}, {location}" + (f" - {u.title}" if u.title else "")
            if u.chapter:
                header += f" [{u.chapter}]"
            body = "\n".join(i.text for i in group)
            chunks.append(_make_chunk(doc, "article", location, [u.label], header, body, u.title, u.chapter))
    return chunks


def chunks_fixed(doc: Doc, units: list[Unit], size: int = FIXED_WORDS, overlap: int = FIXED_OVERLAP) -> list[dict]:
    tokens: list[tuple[str, str]] = []
    for u in units:
        for it in u.items:
            tokens.extend((w, u.label) for w in it.text.split())
    chunks: list[dict] = []
    step = max(size - overlap, 1)
    i = 0
    while i < len(tokens):
        window = tokens[i : i + size]
        if i > 0 and len(window) <= overlap:
            break  # fully contained in the previous window
        labels = list(dict.fromkeys(label for _, label in window))
        location = labels[0] if len(labels) == 1 else f"{labels[0]} - {labels[-1]}"
        body = " ".join(w for w, _ in window)
        chunks.append(_make_chunk(doc, "fixed", location, labels, doc.source, body, "", ""))
        i += step
    return chunks


def doc_for_path(path: Path) -> Doc:
    for d in DOCS:
        if d.path.name == path.name:
            return d
    stem = re.sub(r"[^a-z0-9]+", "-", path.stem.lower()).strip("-") or "document"
    return Doc(stem, re.sub(r"[-_]+", " ", path.stem).strip().title() or stem, path.stem, "", "")


def chunk_file(path: str | Path, design: str = CHOSEN_DESIGN, doc: Doc | None = None) -> list[dict]:
    """Extract, clean and chunk one file. Every chunk carries source and location."""
    path = Path(path)
    doc = doc or doc_for_path(path)
    units = extract_units(path, doc)
    if not units:
        raise ValueError(f"No text could be extracted from {path.name}.")
    if design == "article":
        return chunks_article(doc, units)
    if design == "fixed":
        return chunks_fixed(doc, units)
    raise ValueError(f"Unknown design {design!r}")


# ------------------------------------------------------------------ store ----
def _store_path(design: str) -> Path:
    return INDEX_DIR / design / "chunks.jsonl"


def load_store(design: str) -> dict[str, dict]:
    path = _store_path(design)
    store: dict[str, dict] = {}
    if path.is_file():
        with path.open(encoding="utf-8") as f:
            for line in f:
                if line.strip():
                    rec = json.loads(line)
                    store[rec["id"]] = rec
    return store


def _append(design: str, records: list[dict]) -> None:
    path = _store_path(design)
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8", newline="\n") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False, separators=(",", ":")) + "\n")
        f.flush()
        os.fsync(f.fileno())


def _rewrite(design: str, records: list[dict]) -> None:
    path = _store_path(design)
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(".tmp")
    with tmp.open("w", encoding="utf-8", newline="\n") as f:
        for rec in records:
            f.write(json.dumps(rec, ensure_ascii=False, separators=(",", ":")) + "\n")
    tmp.replace(path)


def prune_doc(design: str, doc_key: str, keep_ids: set[str]) -> int:
    """Drop stored chunks of one document that are no longer produced by its file."""
    store = load_store(design)
    kept = [r for r in store.values() if r["doc"] != doc_key or r["id"] in keep_ids]
    removed = len(store) - len(kept)
    if removed:
        _rewrite(design, kept)
    return removed


def manifest_path() -> Path:
    return INDEX_DIR / "manifest.json"


def load_manifest() -> dict:
    p = manifest_path()
    return json.loads(p.read_text(encoding="utf-8")) if p.is_file() else {"documents": {}}


def save_manifest(manifest: dict) -> None:
    INDEX_DIR.mkdir(parents=True, exist_ok=True)
    manifest_path().write_text(json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


# ------------------------------------------------------------- embeddings ----
class QuotaExhausted(RuntimeError):
    """The daily free-tier quota is used up. Progress is saved; rerun later."""


_client = None


def _genai_client():
    global _client
    if _client is None:
        from google import genai

        from api_key import load_api_key

        _client = genai.Client(api_key=load_api_key())
    return _client


def document_input(chunk: dict) -> str:
    """gemini-embedding-2 has no task_type: the task goes into the text."""
    return f"title: {chunk['header']} | text: {chunk['body']}"


def query_input(query: str) -> str:
    return f"task: search result | query: {query}"


def _normalise(vec: list[float]) -> list[float]:
    norm = math.sqrt(sum(x * x for x in vec)) or 1.0
    return [round(x / norm, 6) for x in vec]


def _retry_delay(message: str) -> float:
    m = re.search(r"retry in ([\d.]+)s", message, re.I) or re.search(r"'retryDelay': '(\d+)s'", message)
    return float(m.group(1)) + 1 if m else 0.0


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed texts (already carrying their task prefix). One vector per text, normalised."""
    from google.genai import errors, types

    client = _genai_client()
    config = types.EmbedContentConfig(output_dimensionality=EMBED_DIM)
    # One Content per text: a plain list would be merged into ONE aggregated embedding.
    contents = [types.Content(parts=[types.Part(text=t)]) for t in texts]
    for attempt in range(7):
        try:
            resp = client.models.embed_content(model=EMBED_MODEL, contents=contents, config=config)
            vectors = [list(e.values) for e in resp.embeddings]
            if len(vectors) != len(texts):
                raise RuntimeError(f"Asked for {len(texts)} embeddings, got {len(vectors)}.")
            return [_normalise(v) for v in vectors]
        except errors.APIError as error:
            message = str(error)
            code = getattr(error, "code", None)
            if code == 429 or "RESOURCE_EXHAUSTED" in message:
                if re.search(r"per\s*day|PerDay|daily", message, re.I):
                    raise QuotaExhausted(message) from error
                time.sleep(max(_retry_delay(message), 5 * 2**attempt))
            elif code and code >= 500:
                time.sleep(3 * 2**attempt)
            else:
                raise
    raise RuntimeError("Gemini kept refusing the embedding request after 7 attempts.")


def embed_and_store(chunks: list[dict], design: str, log=lambda m: print(m, file=sys.stderr),
                    keyword_fallback: bool = False) -> dict:
    """Embed only chunks without a saved vector and append them to the store as they come.

    With keyword_fallback=True (used by add_document) a used-up daily quota does not abort: the chunks
    that could not be embedded are stored without a vector, so keyword search can still find them.
    """
    store = load_store(design)
    todo = [c for c in chunks if not (store.get(c["id"]) or {}).get("vector")]
    reused = len(chunks) - len(todo)
    done = 0
    try:
        for start in range(0, len(todo), EMBED_BATCH):
            batch = todo[start : start + EMBED_BATCH]
            vectors = embed_texts([document_input(c) for c in batch])
            _append(design, [{**c, "vector": v} for c, v in zip(batch, vectors)])
            done += len(batch)
            log(f"  [{design}] embedded {done}/{len(todo)}")
    except QuotaExhausted as error:
        if not keyword_fallback:
            log(f"\nDaily embedding quota reached after {done} new chunks (saved). Rerun after 09:00 Spain time.\n{str(error)[:300]}")
            raise
        rest = todo[done:]
        _append(design, [{**c, "vector": None} for c in rest if c["id"] not in store])
        log(f"\nDaily embedding quota reached after {done} new chunks; {len(rest)} stored without a vector (keyword search only).")
        return {"embedded": done, "reused": reused, "total": len(chunks), "keyword_only": len(rest)}
    return {"embedded": done, "reused": reused, "total": len(chunks), "keyword_only": 0}


# ----------------------------------------------------------- corpus & build ---
def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def download(doc: Doc) -> Path:
    """Official XHTML from the Publications Office (EUR-Lex itself blocks scripts)."""
    CORPUS_DIR.mkdir(exist_ok=True)
    headers = {
        "Accept": "application/xhtml+xml",
        "Accept-Language": "eng",
        "User-Agent": "Mozilla/5.0 (university RAG assignment; contact via IE University)",
    }
    url = f"http://publications.europa.eu/resource/celex/{doc.celex}"
    resp = httpx.get(url, headers=headers, follow_redirects=True, timeout=120)
    if resp.status_code != 200 or b'id="art_' not in resp.content:
        raise RuntimeError(
            f"Could not download {doc.source} (HTTP {resp.status_code}).\n"
            f"  Save it by hand as {doc.path} from {doc.url} (HTML format) and run this again."
        )
    doc.path.write_bytes(resp.content)
    return doc.path


def ensure_file(doc: Doc, manifest: dict) -> Path | None:
    if doc.path.is_file():
        return doc.path
    try:
        print(f"Downloading {doc.source} ...", file=sys.stderr)
        return download(doc)
    except Exception as error:  # noqa: BLE001
        entry = manifest["documents"].get(doc.key)
        if entry and all(entry.get("chunks", {}).get(d) for d in DESIGNS):
            print(f"{doc.source}: no download ({error}); the committed index already holds it.", file=sys.stderr)
            return None
        raise


def index_file(path: str | Path, design: str = CHOSEN_DESIGN, keyword_fallback: bool = False) -> dict:
    """Add one file to the index of one design. Used by server.py's add_document tool.

    Already indexed (same file content): nothing is embedded.
    Same document, new content: its old chunks are replaced; unchanged chunks keep their vectors.
    keyword_fallback: if the daily embedding quota runs out, store the rest without vectors (keyword
    search only); adding the same file again later embeds them.
    """
    path = Path(path)
    doc = doc_for_path(path)
    digest = file_sha256(path)
    manifest = load_manifest()
    for key, entry in manifest["documents"].items():
        if entry.get("sha256") == digest and entry.get("chunks", {}).get(design) and not entry.get("keyword_only"):
            return {"status": "already_indexed", "source": entry["source"], "chunks": entry["chunks"][design], "embedded": 0}
    chunks = chunk_file(path, design, doc)
    replaced = doc.key in manifest["documents"]
    result = embed_and_store(chunks, design, keyword_fallback=keyword_fallback)
    removed = prune_doc(design, doc.key, {c["id"] for c in chunks})
    entry = manifest["documents"].setdefault(doc.key, {"chunks": {}})
    entry.update(
        source=doc.source, title=doc.title, file=path.name, sha256=digest,
        words=sum(c["words"] for c in chunks) if design == "article" else entry.get("words", 0),
        date=doc.date, added=datetime.now(timezone.utc).isoformat(timespec="seconds"),
    )
    entry["chunks"][design] = len(chunks)
    entry["keyword_only"] = result["keyword_only"]
    save_manifest(manifest)
    return {
        "status": "replaced" if replaced else "added", "source": doc.source, "chunks": len(chunks),
        "embedded": result["embedded"], "reused": result["reused"], "removed": removed,
        "keyword_only": result["keyword_only"],
    }


def corpus_stats() -> None:
    manifest = load_manifest()
    rows, totals = [], {"words": 0, "article": 0, "fixed": 0}
    for doc in DOCS:
        path = ensure_file(doc, manifest)
        if path is None:
            continue
        units = extract_units(path, doc)
        words = sum(u.words for u in units)
        n_art, n_fix = len(chunks_article(doc, units)), len(chunks_fixed(doc, units))
        rows.append((doc, words, len(units), n_art, n_fix))
        if doc.indexed:
            totals["words"] += words
            totals["article"] += n_art
            totals["fixed"] += n_fix
    print(f"{'document':<10}{'indexed':<9}{'words':>8}{'units':>7}{'article':>9}{'fixed':>7}")
    for doc, words, n_units, n_art, n_fix in rows:
        print(f"{doc.source:<10}{'yes' if doc.indexed else 'held out':<9}{words:>8}{n_units:>7}{n_art:>9}{n_fix:>7}")
    print(f"{'TOTAL (indexed)':<19}{totals['words']:>8}{'':>7}{totals['article']:>9}{totals['fixed']:>7}")
    both = totals["article"] + totals["fixed"]
    print(f"\nTexts to embed for both designs: {both}. Free tier: about 1,000 a day (queries count too).")


def build_index() -> None:
    """Chosen design first, then the baseline, so a quota stop leaves the usable index complete."""
    manifest = load_manifest()
    docs: list[tuple[Doc, Path, list[Unit], str]] = []
    for doc in DOCS:
        if not doc.indexed:
            try:  # held out on purpose: downloaded so add_document can be demonstrated, but not embedded
                ensure_file(doc, manifest)
            except Exception as error:  # noqa: BLE001 - never fail the index because of the held-out document
                print(f"{doc.source}: not downloaded ({error})", file=sys.stderr)
            continue
        path = ensure_file(doc, manifest)
        if path is None:
            continue
        units = extract_units(path, doc)
        print(f"{doc.source}: {sum(u.words for u in units)} words, {len(units)} units", file=sys.stderr)
        docs.append((doc, path, units, file_sha256(path)))
    summary = []
    for design in sorted(DESIGNS, key=lambda d: d != CHOSEN_DESIGN):
        for doc, path, units, digest in docs:
            chunks = chunks_article(doc, units) if design == "article" else chunks_fixed(doc, units)
            result = embed_and_store(chunks, design)
            prune_doc(design, doc.key, {c["id"] for c in chunks})
            entry = manifest["documents"].setdefault(doc.key, {"chunks": {}})
            entry["chunks"][design] = len(chunks)
            entry.update(
                source=doc.source, title=doc.title, file=path.name, sha256=digest, date=doc.date,
                words=sum(u.words for u in units), url=doc.url, licence=LICENCE,
            )
            save_manifest(manifest)
            summary.append((doc.source, design, result))
    print("\nIndex ready:")
    for source, design, r in summary:
        print(f"  {source:<10} {design:<8} {r['total']:>4} chunks  ({r['embedded']} embedded now, {r['reused']} reused)")
    total_words = sum(e.get("words", 0) for e in manifest["documents"].values())
    print(f"  {len(manifest['documents'])} documents, {total_words} words")


def browse(show: str | None) -> None:
    """Read the corpus as it is chunked (design `article`), without any API call."""
    manifest = load_manifest()
    wanted = (show or "").lower().strip()
    for doc in DOCS:
        path = ensure_file(doc, manifest)
        if path is None:
            continue
        for chunk in chunk_file(path, "article", doc):
            label = f"{chunk['source']} | {chunk['location']}"
            if show is None:
                print(f"{label}" + (f" | {chunk['title']}" if chunk["title"] else "") + f"  ({chunk['words']} words)")
            elif wanted in f"{chunk['source']} {chunk['location']} {chunk['title']}".lower():
                print(f"\n==== {label}\n{chunk['text']}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Build the index (embeds only chunks without a saved vector).")
    parser.add_argument("--stats", action="store_true", help="words and chunks per document; no API calls")
    parser.add_argument("--list", action="store_true", help="list every chunk (source | location | title); no API calls")
    parser.add_argument("--show", metavar="TEXT", help="print the chunks whose source, location or title contains TEXT; no API calls")
    args = parser.parse_args()
    if args.stats:
        corpus_stats()
    elif args.list or args.show:
        browse(args.show)
    else:
        try:
            build_index()
        except QuotaExhausted:
            raise SystemExit(2)


if __name__ == "__main__":
    main()
