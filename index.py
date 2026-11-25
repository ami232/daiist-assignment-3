"""
Assignment 3: build the index (`main.py index`).

Pipeline, one agreement at a time:

    download_html(doc)      wto.org HTML page  -> corpus/<id>.htm   (cached, git-ignored)
    parse_provisions(doc)   HTML               -> list[Provision]   (one per paragraph, with its place in
                                                                     Agreement > Part > Section > Article > Paragraph)
    chunk_structured(...)   provisions         -> list[Chunk]       design A: whole articles, split at paragraphs
    chunk_fixed(...)        provisions         -> list[Chunk]       design B: fixed word windows, structure ignored
    embed_and_store(...)    chunks             -> index/chroma      embeds only chunks with no saved vector

server.py's add_document imports `chunk_file(path)` and `embed_and_store(chunks)`.

    uv run python main.py index                 # everything
    uv run python index.py --chunk-only         # parse + chunk + write index/chunks_*.jsonl, no API calls
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import time
import urllib.request
from dataclasses import asdict, dataclass, field
from pathlib import Path

from bs4 import BeautifulSoup, NavigableString, Tag

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"
CHROMA_DIR = INDEX_DIR / "chroma"

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768          # recommended size; 3072 would quadruple index/ for little gain
EMBED_BATCH = 50
STRUCTURED_MAX_WORDS = 350   # design A: articles longer than this are split at paragraph boundaries
FIXED_WORDS, FIXED_OVERLAP = 200, 40  # design B

BASE = "https://www.wto.org/english/docs_e/legal_e/"

# The corpus. `numerals` decides how article numbers are written; `para_sep` is the
# citation convention: GATT/GATS write "Art. III:4", the others "Art. 2.2".
DOCS = [
    dict(id="gatt1947", short="GATT", url=BASE + "gatt47_e.htm", numerals="roman", para_sep=":",
         title="General Agreement on Tariffs and Trade 1947 (as incorporated into GATT 1994)"),
    dict(id="gatt1994", short="GATT 1994", url=BASE + "gatt94_e.htm", numerals="arabic", para_sep=".",
         title="General Agreement on Tariffs and Trade 1994"),
    dict(id="gats", short="GATS", url=BASE + "gats_e.htm", numerals="roman", para_sep=":",
         title="General Agreement on Trade in Services"),
    dict(id="trips", short="TRIPS", url=BASE + "trips_e.htm", numerals="arabic", para_sep=".",
         title="Agreement on Trade-Related Aspects of Intellectual Property Rights (as amended 2017)"),
    dict(id="sps", short="SPS", url=BASE + "sps_e.htm", numerals="arabic", para_sep=".",
         title="Agreement on the Application of Sanitary and Phytosanitary Measures"),
    dict(id="dsu", short="DSU", url=BASE + "dsu_e.htm", numerals="arabic", para_sep=".",
         title="Understanding on Rules and Procedures Governing the Settlement of Disputes"),
]


def log(*args) -> None:
    """Everything goes to stderr: server.py imports this module and stdout is its MCP channel."""
    print(*args, file=sys.stderr, flush=True)


# --------------------------------------------------------------------------- data

@dataclass
class Provision:
    """One paragraph or sub-paragraph of an agreement, with its full place in the hierarchy."""
    doc_id: str
    agreement: str          # "GATS"
    part: str = ""          # "Part II: General Obligations and Disciplines"
    section: str = ""       # "Section 5: Patents" (TRIPS) or annex sub-heading
    article: str = ""       # "Article XIV" / "Ad Article XX" / "Annex A" / "Preamble"
    article_title: str = "" # "General Exceptions"
    anchor: str = ""        # HTML anchor of the article, for the source link
    para: str = ""          # "1", "(c)(ii)", "Paragraph 21" ...
    note: str = ""          # GATT: the "Ad Article" interpretive note this article points to (its '*')
    text: str = ""
    footnotes: list[str] = field(default_factory=list)


@dataclass
class Chunk:
    id: str
    design: str             # "structured" | "fixed"
    text: str               # what gets embedded and shown to the model (header + body)
    metadata: dict


# --------------------------------------------------------------------------- download

def download_html(doc: dict) -> Path:
    """Fetch the WTO page once into corpus/; later runs use the saved copy."""
    CORPUS_DIR.mkdir(exist_ok=True)
    path = CORPUS_DIR / f"{doc['id']}.htm"
    if not path.exists():
        log(f"downloading {doc['url']}")
        req = urllib.request.Request(doc["url"], headers={"User-Agent": "Mozilla/5.0 (course assignment)"})
        with urllib.request.urlopen(req, timeout=60) as r:
            path.write_bytes(r.read())
    return path


# --------------------------------------------------------------------------- parse

ROMAN = {"I": 1, "V": 5, "X": 10, "L": 50, "C": 100}


def roman_to_int(s: str) -> int:
    total, prev = 0, 0
    for ch in reversed(s.upper()):
        v = ROMAN[ch]
        total, prev = (total - v, prev) if v < prev else (total + v, v)
    return total


def int_to_roman(n: int) -> str:
    out = ""
    for v, r in [(50, "L"), (40, "XL"), (10, "X"), (9, "IX"), (5, "V"), (4, "IV"), (1, "I")]:
        while n >= v:
            out, n = out + r, n - v
    return out


KEEP_UPPER = {"GATT", "GATS", "TRIPS", "SPS", "DSU", "WTO", "MFN"}
SMALL_WORDS = {"a", "an", "and", "as", "at", "by", "for", "in", "of", "on", "or", "the", "to", "with"}


def nice_title(text: str) -> str:
    """'GENERAL OBLIGATIONS AND DISCIPLINES' -> 'General Obligations and Disciplines'."""
    def word(i: int, w: str) -> str:
        if w.upper() in KEEP_UPPER or re.fullmatch(r"[IVXL]{2,}|\d+[A-Z]", w.upper()):
            return w.upper()                    # roman numerals, "1C", acronyms
        if i and w.lower() in SMALL_WORDS:
            return w.lower()
        return w[:1].upper() + w[1:].lower()
    return " ".join(word(i, w) for i, w in enumerate(text.split()))


def strip_marks(text: str) -> str:
    """Drop footnote markers and GATT's '*' (= 'see the interpretive note') from headings and titles."""
    return re.sub(r"(\s*(\*|\(\d+\)))+$", "", text).strip()


def clean(text: str) -> str:
    text = text.replace("\xa0", " ").replace("’", "'").replace("‘", "'")
    text = text.replace("“", '"').replace("”", '"')
    return re.sub(r"\s+", " ", text).strip()


HEADING_TAGS = {"h1", "h2", "h3"}
RE_PART = re.compile(r"^PART\s+([IVXL]+)\b", re.I)
RE_SECTION = re.compile(r"^SECTION\s+([0-9A-Z]+)\b(.*)", re.I)
RE_ARTICLE = re.compile(r"^Article\s+([0-9IVXL]+(?:\s*(?:bis|ter|quater))?)\s*(?::\s*(.*))?$", re.I)  # TBT: "Article 2: Title"
RE_AD = re.compile(r"^Ad\s+(Articles?|Part)\s+(.+)$", re.I)
RE_ANNEX = re.compile(r"^(ANNEX|APPENDIX|ATTACHMENT)\b\s*(.*)$", re.I)
RE_LEADING_LABEL = re.compile(r"^(\d+(?:\.\d+)?)\.\s+|^\(([a-z]{1,4}|[ivx]+)\)\s+")


def anchor_to_para(anchor: str) -> str:
    """'art14_c_ii' -> '(c)(ii)', 'art2_1' -> '1', 'art31_a' -> '(a)'. '' if not a paragraph anchor."""
    m = re.match(r"^art\d+(?:_?bis|_?ter)?_(.+)$", anchor)
    if not m:
        return ""
    parts = m.group(1).split("_")
    if parts[0] == "sec" and len(parts) > 2:   # GATT XVI/XVIII: 'art18_sec_b_9' -> paragraph 9 (numbered
        parts = parts[2:]                       # continuously across Sections A-D, cited "Art. XVIII:9")
    elif parts[0] == "sec":
        return ""
    out = ""
    for p in parts:
        out += p if p.isdigit() and not out else f"({p})"
    return out


def load_footnotes(soup: BeautifulSoup) -> dict[str, str]:
    """The pages put footnotes in <ol class="footnote-list"><li id="fnt-N">; text refs are <a href="#fnt-N">."""
    notes = {}
    for ol in soup.select("ol.footnote-list"):
        for li in ol.find_all("li", id=True):
            ref = li.select_one(".reference-text")
            num = li.find("sup")
            notes[li["id"]] = clean(f"{num.get_text() if num else ''} {ref.get_text(' ') if ref else ''}")
        ol.decompose()
    return notes


def block_text(el: Tag, footnotes: dict[str, str]) -> tuple[str, list[str]]:
    """Text of a <p> or table row, with footnote markers turned into '[fn N]' and the notes collected."""
    found = []
    for sup in el.find_all("sup"):
        a = sup.find("a", href=True)
        if a and a["href"].startswith("#fnt-"):
            key = a["href"][1:]
            label = clean(a.get_text()).strip("()")
            if key in footnotes:
                found.append(footnotes[key])
            sup.replace_with(NavigableString(f" [fn {label}]"))
    if el.name == "tr":
        cells = [clean(td.get_text(" ")) for td in el.find_all("td")]
        text = " ".join(c for c in cells if c)
    else:
        text = clean(el.get_text(" "))
    return text, found


def parse_provisions(doc: dict, html_path: Path | None = None) -> list[Provision]:
    """Walk the page top to bottom and tag every paragraph with Part / Section / Article / paragraph.

    The WTO markup is not consistent (some headings carry anchors, some do not; TRIPS repeats each anchor
    four times), so structure comes from the visible heading text and anchors are only used when present.
    """
    html = (html_path or download_html(doc)).read_text(encoding="utf-8", errors="ignore")
    soup = BeautifulSoup(html, "html.parser")
    for junk in soup.select("script, style, .modal, .leftCol, .rightCol, #breadcrumbsDiv, .introDiv, noscript"):
        junk.decompose()
    footnotes = load_footnotes(soup)
    main = soup.select_one(".centerCol") or soup.select_one(".mainDiv") or soup.body
    # Some pages (GATS) open with a table of contents laid out as a table: many "Article ..." rows
    # and no paragraph anchors. Left in, it becomes a chunk that matches every query about anything.
    for table in main.find_all("table"):
        if not table.find("a", attrs={"name": True}) and len(re.findall(r"\bArticle\s", table.get_text(" "))) > 5:
            table.decompose()

    state = dict(part="", section="", article="Preamble", article_title="", anchor="", note="")
    expect = None           # "part_title" / "article_title": the next centred line names the heading above
    last_anchor = ""
    out: list[Provision] = []
    pending_notes: list[str] = []   # footnotes hung on a heading or title (SPS Annex A's "pests include weeds")

    def heading_anchor(el: Tag) -> str:
        a = el.find("a", attrs={"name": True})
        if a:
            return a["name"]
        prev = el.find_previous("a", attrs={"name": True})
        return prev["name"] if prev else ""

    for el in main.find_all(["h1", "h2", "h3", "p", "tr"]):
        if el.name == "p" and el.find_parent("tr"):
            continue
        text = clean(el.get_text(" "))
        if not text or text in {"Share", "Notes:"}:
            continue

        cls = el.get("class") or []
        is_centred = "center" in cls or "lead" in cls
        if el.name in HEADING_TAGS or (is_centred and expect):
            pending_notes += block_text(el, footnotes)[1]   # attach them to the first paragraph below

        if el.name in HEADING_TAGS:
            note_link = el.find("a", href=re.compile(r"^#ad_"))
            text = strip_marks(text)
            if text.upper() in {"WORLD TRADE ORGANIZATION"} or text.lower().startswith(doc["title"][:25].lower()):
                continue
            if m := RE_PART.match(text):
                state.update(part=f"Part {m.group(1).upper()}", section="", article="", article_title="")
                expect = "part_title"
            elif m := RE_SECTION.match(text):
                title = clean(m.group(2)).strip(": ")
                state["section"] = f"Section {m.group(1)}" + (f": {nice_title(strip_marks(title))}" if title else "")
                expect = "section_title" if not title else None
            elif m := RE_AD.match(text):
                state.update(part="Annex I: Notes and Supplementary Provisions", section="",
                             article=f"Ad {m.group(1).title()} {m.group(2)}", article_title="",
                             anchor=heading_anchor(el), note="")
                expect = None
            elif m := RE_ARTICLE.match(text):
                note = f"Ad Article {m.group(1)}" if note_link else ""
                title = clean(m.group(2) or "")
                state.update(article=f"Article {m.group(1)}", article_title=title, anchor=heading_anchor(el), note=note)
                expect = None if title else "article_title"
            elif m := RE_ANNEX.match(text):
                ident = m.group(2).strip()
                if re.fullmatch(r"1[ABC]", ident.upper()):    # "ANNEX 1B" = GATS's place in the WTO Agreement;
                    state.update(article="Preamble", article_title="", anchor="", note="")  # what follows is the preamble
                    expect = None
                    continue
                title = ""
                if t := re.match(r"^([0-9A-Z]{1,3})\s*:\s*(.+)$", ident):   # TBT: "ANNEX 1: TERMS AND ..."
                    ident, title = t.group(1), nice_title(t.group(2)) if t.group(2).isupper() else t.group(2)
                ident = ident.upper() if len(ident) <= 4 else nice_title(ident).replace("On ", "on ", 1)
                state.update(part="", section="", article=f"{m.group(1).title()} {ident}".strip(),
                             article_title=title, anchor=heading_anchor(el), note="")
                expect = None if title else "article_title"
            else:   # other headings (e.g. TRIPS 'ANNEX 1C', annex sub-titles) become the section
                state["section"] = nice_title(text)
                expect = None
            continue

        if is_centred and expect:
            text = strip_marks(text)
            if expect == "part_title":
                state["part"] += f": {nice_title(text)}"
            elif expect == "section_title":
                state["section"] += f": {nice_title(text)}"
            elif expect == "article_title":
                state["article_title"] = nice_title(text) if text.isupper() else text
            expect = None
            continue
        expect = None
        if is_centred and state["article"].startswith("Ad "):
            last_anchor = f"label:{text}"   # "Paragraph 21" / "Sub-paragraph (h)" inside an Ad note
            continue

        a = el.find("a", attrs={"name": True}) or el.find_previous("a", attrs={"name": True})
        anchor = a["name"] if a else ""
        body, notes = block_text(el, footnotes)
        notes, pending_notes = pending_notes + notes, []
        para = anchor_to_para(anchor) if anchor != last_anchor or not out else ""
        if last_anchor.startswith("label:"):
            para = last_anchor[6:]
            body = f"{para}: {body}"   # Ad notes say "this sub-paragraph"; keep which one
        if not para and (m := RE_LEADING_LABEL.match(body)):
            para = m.group(1) or f"({m.group(2)})"
        last_anchor = anchor
        out.append(Provision(doc_id=doc["id"], agreement=doc["short"], text=body, footnotes=notes, para=para,
                             **{k: state[k] for k in ("part", "section", "article", "article_title", "anchor", "note")}))
    # The rest of the GATS/TRIPS contents list sits in the preamble, before its opening word "Members,".
    pre = [i for i, p in enumerate(out) if p.article == "Preamble"]
    start = next((i for i in pre if re.match(r"^Members\b", out[i].text)), None)
    if start is not None:
        out = [p for i, p in enumerate(out) if not (p.article == "Preamble" and i < start)]

    # GATT 1994 has no articles, only numbered paragraphs: cite it as "GATT 1994, para. 1(b)".
    if not any(p.article.startswith("Article") for p in out):
        for p in out:
            p.article = "" if p.article == "Preamble" else p.article

    # GATT marks most annotated articles with '*', but not all (Article XX has a note and no '*'):
    # link every article to its "Ad Article" note whenever the note exists.
    notes = {p.article for p in out if p.article.startswith("Ad Article ")}
    for p in out:
        if not p.note and f"Ad {p.article}" in notes:
            p.note = f"Ad {p.article}"
    return out


# --------------------------------------------------------------------------- citations

def article_label(doc: dict, article: str) -> str:
    """'Article XIV' -> 'Art. XIV'; 'Ad Article XX' -> 'Ad Art. XX'; 'Annex A' unchanged."""
    return article.replace("Article ", "Art. ")


def citation(doc: dict, article: str, paras: list[str]) -> str:
    """'GATS Art. XIV(c)(ii)', 'GATT Art. III:4', 'SPS Art. 2.2-2.3', 'SPS Annex A'."""
    base = f"{doc['short']} {article_label(doc, article)}".strip()
    paras = [p for p in paras if p and not p.startswith(("Paragraph", "Sub-"))]
    if not paras or article.startswith("Ad "):   # a note's labels refer to the annotated article's paragraphs
        return base
    first, last = paras[0], paras[-1]
    if not article.startswith(("Article", "Ad Article")):          # annexes, appendices: "SPS Annex A, para. 1"
        return f"{base}, para. {first}" + ("" if first == last else f"-{last}")
    def one(p: str) -> str:
        return f"{doc['para_sep']}{p}" if p[0].isdigit() else p
    if first == last:
        return f"{base}{one(first)}"
    # "DSU Art. 22.1-22.3(b)", "GATT Art. III:1-III:4": repeat the article so the range is unambiguous
    art_no = article_label(doc, article).split()[-1]
    end = f"{art_no}{one(last)}" if last[0].isdigit() else last
    return f"{base}{one(first)}-{end}"


def source_url(doc: dict, anchor: str) -> str:
    return doc["url"] + (f"#{anchor}" if anchor else "")


def article_key(p: Provision) -> tuple:
    return (p.part, p.section, p.article)


def breadcrumb(p: Provision) -> str:
    art = p.article + (f": {p.article_title}" if p.article_title else "")
    return " > ".join(x for x in (p.agreement, p.part, p.section, art) if x)


# --------------------------------------------------------------------------- chunk

def _chunk_id(design: str, doc_id: str, text: str) -> str:
    return f"{doc_id}-{design}-{hashlib.sha1(text.encode()).hexdigest()[:12]}"


def _provision_text(p: Provision) -> str:
    return p.text + "".join(f"\n[Footnote {n}]" for n in p.footnotes)


def chunk_structured(doc: dict, provisions: list[Provision]) -> list[Chunk]:
    """Design A: one chunk per article; long articles are split between paragraphs, never inside one.

    Every chunk starts with its breadcrumb (Agreement > Part > Article: Title) so a retrieved fragment of
    Article XX still tells the model which agreement and exception it belongs to.
    """
    groups: dict[tuple, list[Provision]] = {}
    for p in provisions:
        groups.setdefault(article_key(p), []).append(p)

    chunks = []
    for key, provs in groups.items():
        pieces, current, words = [], [], 0
        for p in provs:
            n = len(_provision_text(p).split())
            if current and words + n > STRUCTURED_MAX_WORDS:
                pieces.append(current)
                current, words = [], 0
            current.append(p)
            words += n
        if current:
            pieces.append(current)

        first = provs[0]
        parent = f"{doc['id']}:{first.article}".replace(" ", "_")
        for i, piece in enumerate(pieces):
            paras = [p.para for p in piece]
            cite = citation(doc, first.article, paras if len(pieces) > 1 else [])
            header = f"[{cite}] {breadcrumb(first)}"
            body = "\n".join(_provision_text(p) for p in piece)
            text = f"{header}\n{body}"
            chunks.append(Chunk(
                id=_chunk_id("structured", doc["id"], text), design="structured", text=text,
                metadata=dict(
                    doc_id=doc["id"], agreement=doc["short"], document=doc["title"],
                    part=first.part, section=first.section, article=first.article,
                    article_title=first.article_title, paragraphs=", ".join(x for x in paras if x),
                    citation=cite, parent_id=parent, piece=i + 1, pieces=len(pieces),
                    interpretive_note=f"{doc['short']} {article_label(doc, first.note)}" if first.note else "",
                    url=source_url(doc, first.anchor), words=len(body.split()),
                ),
            ))
    return chunks


def chunk_fixed(doc: dict, provisions: list[Provision]) -> list[Chunk]:
    """Design B (baseline): fixed windows of FIXED_WORDS with overlap, ignoring article boundaries.

    Metadata still records which articles the window spans, so hit rate can be measured the same way.
    """
    words: list[tuple[str, Provision]] = []
    for p in provisions:
        words += [(w, p) for w in _provision_text(p).split()]
    chunks, step = [], FIXED_WORDS - FIXED_OVERLAP
    for start in range(0, max(len(words) - FIXED_OVERLAP, 1), step):
        window = words[start:start + FIXED_WORDS]
        arts = list(dict.fromkeys(p.article for _, p in window))
        first = window[0][1]
        text = " ".join(w for w, _ in window)
        cite = " / ".join(f"{doc['short']} {article_label(doc, a)}" for a in arts)
        chunks.append(Chunk(
            id=_chunk_id("fixed", doc["id"], f"{start}:{text}"), design="fixed", text=text,
            metadata=dict(
                doc_id=doc["id"], agreement=doc["short"], document=doc["title"],
                part=first.part, section=first.section, article=first.article,
                article_title=first.article_title, articles=" | ".join(arts), paragraphs="",
                citation=cite, parent_id="", piece=0, pieces=0, interpretive_note="",
                url=source_url(doc, first.anchor), words=len(window),
            ),
        ))
    return chunks


DESIGNS = {"structured": chunk_structured, "fixed": chunk_fixed}


def doc_for_path(path: Path) -> dict:
    """The DOCS entry for a saved page, or a new entry for a file add_document was given."""
    for doc in DOCS:
        if path.stem == doc["id"]:
            return doc
    stem = re.sub(r"[^a-z0-9]+", "-", path.stem.lower()).strip("-")
    for key, doc in EXTRA_DOCS.items():          # pages we expect add_document to receive
        if key in path.stem.lower():
            return dict(doc, url=BASE + f"{key}.htm")
    html = path.read_text(encoding="utf-8", errors="ignore")
    m = re.search(r"<title>(.*?)</title>", html, re.S | re.I)
    title = clean(re.sub(r"^WTO \|\s*(legal texts\s*-\s*)?", "", m.group(1))) if m else stem.replace("-", " ").title()
    return dict(id=stem, short=title[:40], url=path.resolve().as_uri(), numerals="arabic", para_sep=".", title=title)


# Other WTO legal texts with a known name, so their citations read well after add_document.
EXTRA_DOCS = {
    "17-tbt_e": dict(id="tbt", short="TBT", numerals="arabic", para_sep=".",
                     title="Agreement on Technical Barriers to Trade"),
}


def chunk_file(path: str | Path, design: str = "structured") -> list[Chunk]:
    """Parse one saved WTO HTML page (or any HTML file with the same layout) into chunks."""
    path = Path(path)
    doc = doc_for_path(path)
    return DESIGNS[design](doc, parse_provisions(doc, path))


# --------------------------------------------------------------------------- embed & store

def doc_prefix(chunk: Chunk) -> str:
    """gemini-embedding-2 takes no task_type; retrieval documents are written 'title: ... | text: ...'."""
    return f"title: {chunk.metadata['citation']} | text: {chunk.text}"


def query_prefix(query: str) -> str:
    return f"task: search result | query: {query}"


def embed_texts(texts: list[str]) -> list[list[float]]:
    from google import genai
    from google.genai import types

    from api_key import load_api_key

    client = genai.Client(api_key=load_api_key())
    for attempt in range(6):
        try:
            result = client.models.embed_content(
                model=EMBED_MODEL,
                contents=[types.Content(parts=[types.Part.from_text(text=t)]) for t in texts],
                config=types.EmbedContentConfig(output_dimensionality=EMBED_DIM),
            )
            return [e.values for e in result.embeddings]
        except Exception as error:  # noqa: BLE001
            msg = str(error)
            if "429" in msg or "RESOURCE_EXHAUSTED" in msg:
                if "per day" in msg.lower() or "PerDay" in msg:
                    raise SystemExit("Daily embedding quota used up. Vectors so far are saved; rerun tomorrow.")
                wait = 20 * (attempt + 1)
                log(f"rate limited, waiting {wait}s")
                time.sleep(wait)
                continue
            raise
    raise RuntimeError("embedding kept failing after retries")


def collection(design: str):
    import chromadb

    client = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return client.get_or_create_collection(f"wto_{design}", metadata={"hnsw:space": "cosine"})


def embed_and_store(chunks: list[Chunk], design: str | None = None) -> dict:
    """Upsert chunks into Chroma, embedding only those whose id has no stored vector yet.

    Ids are a hash of the chunk text, so an unchanged chunk is never embedded twice; a changed
    chunk gets a new id. Each batch is written as soon as it is embedded, so hitting the daily
    quota loses nothing. Returns counts.
    """
    design = design or (chunks[0].design if chunks else "structured")
    col = collection(design)
    ids = [c.id for c in chunks]
    existing = set(col.get(ids=ids, include=[])["ids"]) if ids else set()
    todo = [c for c in chunks if c.id not in existing]
    log(f"[{design}] {len(chunks)} chunks, {len(existing)} already embedded, {len(todo)} to embed")
    for i in range(0, len(todo), EMBED_BATCH):
        batch = todo[i:i + EMBED_BATCH]
        vectors = embed_texts([doc_prefix(c) for c in batch])
        col.upsert(ids=[c.id for c in batch], embeddings=vectors,
                   documents=[c.text for c in batch], metadatas=[c.metadata for c in batch])
        log(f"[{design}] stored {min(i + EMBED_BATCH, len(todo))}/{len(todo)}")
    return dict(total=len(chunks), already=len(existing), embedded=len(todo))


def prune(design: str, keep_ids: set[str], doc_ids: set[str]) -> int:
    """Drop stored chunks of these documents that the current chunking no longer produces."""
    col = collection(design)
    stale = [i for i, m in zip(*(lambda r: (r["ids"], r["metadatas"]))(col.get(include=["metadatas"])))
             if m.get("doc_id") in doc_ids and i not in keep_ids]
    if stale:
        col.delete(ids=stale)
    return len(stale)


# --------------------------------------------------------------------------- main

def build(chunk_only: bool = False) -> None:
    INDEX_DIR.mkdir(exist_ok=True)
    all_chunks: dict[str, list[Chunk]] = {d: [] for d in DESIGNS}
    for doc in DOCS:
        provisions = parse_provisions(doc)
        words = sum(len(p.text.split()) for p in provisions)
        log(f"{doc['short']:<10} {len(provisions):>4} provisions, {words:>6} words")
        for design, fn in DESIGNS.items():
            all_chunks[design] += fn(doc, provisions)

    for design, chunks in all_chunks.items():
        out = INDEX_DIR / f"chunks_{design}.jsonl"
        with out.open("w", encoding="utf-8") as f:
            for c in chunks:
                f.write(json.dumps(asdict(c), ensure_ascii=False) + "\n")
        log(f"[{design}] {len(chunks)} chunks -> {out.relative_to(ROOT)}")

    if chunk_only:
        return
    for design, chunks in all_chunks.items():
        removed = prune(design, {c.id for c in chunks}, {d["id"] for d in DOCS})
        if removed:
            log(f"[{design}] removed {removed} stale chunks")
        embed_and_store(chunks, design)


if __name__ == "__main__":
    build(chunk_only="--chunk-only" in sys.argv)
