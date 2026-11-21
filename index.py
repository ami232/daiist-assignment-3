"""
Assignment 3: build the index (`main.py index`).

Downloads the EU cosmetics texts into corpus/ (git-ignored), extracts the
articles, sections and annex table entries with their location, cleans them,
chunks them two ways and embeds the chunks with Gemini into index/ (ChromaDB):

- "fixed":     ~200-word windows over the running text, 40 words of overlap.
- "structure": one chunk per article / section (split at paragraph boundaries
               when long), annex substance entries grouped without splitting
               an entry, and every chunk starting with its document + location.

Each design is its own collection. Only chunks without a saved vector are sent
to Gemini, and each batch is saved as soon as it comes back, so the free-tier
daily limit (~1,000 texts) or a crash loses nothing: run it again tomorrow.

server.py's add_document tool imports `chunk_file` and `embed_and_store`.
"""

import hashlib
import re
import sys
import time
from pathlib import Path

import httpx
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
CORPUS = ROOT / "corpus"
INDEX = ROOT / "index"

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768
BATCH = 50

DESIGNS = ("structure", "fixed")
DEFAULT_DESIGN = "structure"
FIXED_WORDS, FIXED_OVERLAP = 200, 40
STRUCT_MAX_WORDS = 250

DOCUMENTS = [
    {"celex": "02009R1223-20250501", "source": "Regulation (EC) No 1223/2009 (consolidated 2025-05-01)",
     "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:02009R1223-20250501"},
    {"celex": "32013D0674", "source": "Commission Implementing Decision 2013/674/EU (safety report guidelines)",
     "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32013D0674"},
    {"celex": "32013R0655", "source": "Commission Regulation (EU) No 655/2013 (claims criteria)",
     "url": "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:32013R0655"},
]

# Column labels of the substance tables, after the reference number.
ANNEX_COLUMNS = {
    "ANNEX II": ["Chemical name/INN", "CAS number", "EC number"],
    "ANNEX III": ["Chemical name/INN", "Common ingredient name", "CAS number", "EC number",
                  "Product type, body parts", "Maximum concentration in ready for use preparation",
                  "Other", "Wording of conditions of use and warnings"],
    "ANNEX IV": ["Chemical name", "Colour index number/common ingredient name", "CAS number", "EC number",
                 "Colour", "Product type, body parts", "Maximum concentration in ready for use preparation",
                 "Other", "Wording of conditions of use and warnings"],
}
ANNEX_COLUMNS["ANNEX V"] = ANNEX_COLUMNS["ANNEX VI"] = ANNEX_COLUMNS["ANNEX III"]
SKIP_ANNEXES = {"ANNEX IX", "ANNEX X"}  # repealed directives and a correlation table

# Consolidated-text markers (▼M12, ►C3, ◄) and deleted entries (—————).
MARKER = re.compile(r"[▼►◄]\s?[A-Z]?\d*")
DELETED = re.compile(r"^[—\-–\s]+$")


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


# --------------------------------------------------------------------- download

def download(doc: dict) -> Path:
    """Fetch the XHTML from the EU Publications Office (EUR-Lex blocks scripts)."""
    path = CORPUS / f"{doc['celex']}.xhtml"
    if not path.exists():
        CORPUS.mkdir(exist_ok=True)
        r = httpx.get(f"http://publications.europa.eu/resource/celex/{doc['celex']}", timeout=180,
                      follow_redirects=True,
                      headers={"Accept": "application/xhtml+xml", "Accept-Language": "eng"})
        r.raise_for_status()
        path.write_text(r.text, encoding="utf-8")
    return path


# --------------------------------------------------------------------- extract

def clean(text: str) -> str:
    text = MARKER.sub(" ", text.replace("\xa0", " "))
    return re.sub(r"\s+", " ", text).strip()


HEADING_CLASSES = {
    # consolidated texts
    "title-division-1": "chapter", "title-division-2": "chapter_name",
    "title-article-norm": "article", "stitle-article-norm": "article_name",
    "title-annex-1": "annex", "title-annex-2": "annex_name",
    "title-gr-seq-level-1": "part", "title-gr-seq-level-2": "section",
    # Official Journal texts
    "oj-ti-art": "article", "oj-sti-art": "article_name", "oj-doc-ti": "annex",
    "oj-ti-grseq-1": "part",
}
SKIP_CLASSES = {"modref", "arrow", "oj-note", "note", "title-fam-member", "title-fam-member-star"}


def extract_xhtml(path: Path) -> list[dict]:
    """Running blocks of a EUR-Lex XHTML file: {"location", "text", "entry"?}.

    Front matter (title, amendment list, recitals) is dropped: the body starts
    at the first chapter or article. A substance-table row becomes one block
    whose text names every column, so a chunk with it is readable on its own.
    """
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    for el in soup.find_all(class_=lambda c: c and set(c.split() if isinstance(c, str) else c) & SKIP_CLASSES):
        el.decompose()
    in_row = {id(d) for tr in soup.find_all("tr") for d in tr.descendants}
    state = {"chapter": "", "article": "", "article_name": "", "annex": "", "annex_name": "",
             "part": "", "section": ""}
    started, blocks, entry = False, [], None

    def location() -> str:
        if state["annex"]:
            bits = [state["annex"], state["annex_name"].capitalize(), state["part"], state["section"]]
        else:
            bits = [state["article"], state["article_name"]]
        return ", ".join(b for b in bits if b)

    for el in soup.find_all(["p", "div", "tr", "img"]):
        if id(el) in in_row:
            continue
        if el.name == "img":
            # Annex VII's symbols are pictures: keep a block so the section exists.
            if started and state["part"]:
                blocks.append({"location": location(), "text": f"{state['part']}: the symbol is shown as an image."})
            continue
        classes = set(el.get("class") or [])
        kind = next((HEADING_CLASSES[c] for c in classes if c in HEADING_CLASSES), None)
        text = clean(el.get_text(" "))
        if kind:
            if kind in ("chapter", "article") or (kind == "annex" and text.upper().startswith("ANNEX")):
                started = True
            if kind == "annex":
                state.update(annex=text if text.upper().startswith("ANNEX") else f"{state['annex']}, {text}",
                             annex_name="", part="", section="", article="", article_name="")
            elif kind == "article":
                state.update(article=text, article_name="", annex="", annex_name="", part="", section="")
            elif kind == "part":
                state.update(part=text, section="")
            else:
                state[kind] = text
            continue
        if not started or not text or state["annex"].split(",")[0] in SKIP_ANNEXES:
            continue
        if el.name == "tr":
            entry = table_row(el, state["annex"].split(",")[0], entry, blocks, location())
            continue
        if is_leaf(el) and el.find_parent("tr") is None:
            prefix = numbering(el)
            blocks.append({"location": location(), "text": f"{prefix} {text}" if prefix else text})
    return blocks


def table_row(tr, annex: str, entry: dict | None, blocks: list, loc: str) -> dict | None:
    """Turn a substance-table row into a block, or extend the previous entry.

    Rows that only continue an entry (another product type or concentration)
    carry no reference number; their cells line up with the right-hand columns.
    """
    cells = [clean(td.get_text(" ")) for td in tr.find_all(["td", "th"], recursive=False)]
    if not any(cells) or all(DELETED.match(c) or not c for c in cells):
        return entry
    labels = ANNEX_COLUMNS.get(annex)
    if labels is None:
        blocks.append({"location": loc, "text": " | ".join(c for c in cells if c)})
        return None
    ref = cells[0]
    if re.fullmatch(r"\d+[a-z]?", ref) and len(cells) > 2:
        if all(DELETED.match(c) or not c for c in cells[1:]):
            return None  # entry deleted by an amendment
        fields = [f"{lab}: {val}" for lab, val in zip(labels, cells[1:]) if val]
        entry = {"location": f"{annex}, entry {ref}", "text": f"{annex} entry {ref}. " + "; ".join(fields),
                 "entry": ref}
        blocks.append(entry)
        return entry
    if len(cells) == 1:  # footnotes under the table
        blocks.append({"location": f"{annex}, notes to the table", "text": cells[0]})
        return None
    if entry is not None and len(cells) <= len(labels):
        extra = [f"{lab}: {val}" for lab, val in zip(labels[-len(cells):], cells) if val]
        if extra:
            entry["text"] += "; " + "; ".join(extra)
    return entry


def is_leaf(el) -> bool:
    """A paragraph of text: a <p>, or a <div> holding text but no paragraphs.

    Consolidated texts put a one-paragraph point straight into a <div>
    (Article 5(1)); skipping divs lost those points.
    """
    if el.find(["p", "div", "table"]) is not None:
        return False
    if el.name == "div":
        return bool(clean(el.get_text(" ")))
    return el.name == "p"


def first_leaf(container):
    return next((x for x in container.find_all(["p", "div"]) if is_leaf(x)), None)


def numbering(p) -> str:
    """The paragraph number and point letter a consolidated text keeps outside
    the paragraph ("1.", "(a)"), so a chunk can still be cited as Article 19(1)(a)."""
    prefix = []
    column = p.find_parent(class_="grid-list-column-2")
    if column is not None and first_leaf(column) is p:
        marker = column.find_previous_sibling(class_="grid-list-column-1")
        if marker is not None:
            prefix.append(clean(marker.get_text(" ")))
    for norm in p.find_parents("div", class_="norm"):
        number = norm.find("span", class_="no-parag", recursive=False)
        if number is not None and first_leaf(norm) is p:
            prefix.insert(0, clean(number.get_text(" ")))
            break
    return " ".join(prefix)


def extract_pdf(path: Path) -> list[dict]:
    from pypdf import PdfReader
    return [{"location": f"page {i}", "text": clean(page.extract_text() or "")}
            for i, page in enumerate(PdfReader(str(path)).pages, start=1) if (page.extract_text() or "").strip()]


def extract_text(path: Path) -> list[dict]:
    paras = [clean(p) for p in re.split(r"\n\s*\n", path.read_text(encoding="utf-8", errors="replace"))]
    return [{"location": f"paragraph {i}", "text": p} for i, p in enumerate(paras, start=1) if p]


def extract(path: Path) -> list[dict]:
    suffix = path.suffix.lower()
    if suffix in (".xhtml", ".html", ".htm"):
        return extract_xhtml(path)
    if suffix == ".pdf":
        return extract_pdf(path)
    return extract_text(path)


# ----------------------------------------------------------------------- chunk

def chunk_fixed(blocks: list[dict], source: str) -> list[dict]:
    """Fixed word windows over the running text, blind to its structure."""
    words, owners = [], []
    for i, b in enumerate(blocks):
        w = b["text"].split()
        words += w
        owners += [i] * len(w)
    chunks, step = [], FIXED_WORDS - FIXED_OVERLAP
    for start in range(0, max(len(words) - FIXED_OVERLAP, 1), step):
        end = min(start + FIXED_WORDS, len(words))
        first, last = blocks[owners[start]]["location"], blocks[owners[end - 1]]["location"]
        loc = first if first == last else f"{first} to {last}"
        chunks.append({"source": source, "location": loc, "text": " ".join(words[start:end])})
    return chunks


def split_long(blocks: list[dict]) -> list[dict]:
    """Split a running-text block longer than a chunk at sentence ends.

    Substance entries stay whole: half an entry (a name without its limit) is
    worse than a long chunk.
    """
    out = []
    for b in blocks:
        if "entry" in b or len(b["text"].split()) <= STRUCT_MAX_WORDS:
            out.append(b)
            continue
        piece = []
        for sentence in re.split(r"(?<=[.;:])\s+(?=\(?\s?\w)", b["text"]):
            if piece and len(" ".join(piece + [sentence]).split()) > STRUCT_MAX_WORDS:
                out.append({**b, "text": " ".join(piece)})
                piece = []
            piece.append(sentence)
        out.append({**b, "text": " ".join(piece)})
    return out


def chunk_structure(blocks: list[dict], source: str) -> list[dict]:
    """Chunks that follow the document: never across two articles, sections or
    annexes; long ones split at paragraph or entry boundaries; each chunk
    starts with "<source>, <location>:" so it reads on its own."""
    chunks, group, words = [], [], 0

    def flush():
        nonlocal group, words
        if not group:
            return
        loc = group[0]["location"]
        refs = [b["entry"] for b in group if "entry" in b]
        if refs:
            annex = loc.split(", entry")[0]
            loc = f"{annex}, entry {refs[0]}" if len(refs) == 1 else f"{annex}, entries {refs[0]}-{refs[-1]}"
        body = " ".join(b["text"] for b in group)
        chunks.append({"source": source, "location": loc, "text": f"{source}, {loc}: {body}",
                       "entries": ",".join(refs)})
        group, words = [], 0

    for b in split_long(blocks):
        n = len(b["text"].split())
        section = lambda x: x["location"].split(", entry")[0]
        if group and (section(group[0]) != section(b) or words + n > STRUCT_MAX_WORDS):
            flush()
        group.append(b)
        words += n
    flush()
    return chunks


def chunk_file(path: Path | str, source: str | None = None, design: str = DEFAULT_DESIGN) -> list[dict]:
    """Extract, clean and chunk one file. The add_document tool calls this."""
    path = Path(path)
    blocks = extract(path)
    source = source or path.stem
    chunks = chunk_structure(blocks, source) if design == "structure" else chunk_fixed(blocks, source)
    for c in chunks:
        c["file"] = path.name
        c["id"] = hashlib.sha1(f"{design}|{source}|{c['location']}|{c['text']}".encode()).hexdigest()[:20]
    return chunks


# ----------------------------------------------------------------------- embed

_CLIENT = None


def client():
    """One Gemini client for the process (a temporary one closes its connection)."""
    global _CLIENT
    if _CLIENT is None:
        from google import genai
        from api_key import load_api_key
        _CLIENT = genai.Client(api_key=load_api_key())
    return _CLIENT


def collection(design: str = DEFAULT_DESIGN):
    import chromadb
    db = chromadb.PersistentClient(path=str(INDEX / "chroma"),
                                   settings=chromadb.Settings(anonymized_telemetry=False))
    return db.get_or_create_collection(design, metadata={"hnsw:space": "cosine"})


def embed(texts: list[str], task: str) -> list[list[float]]:
    from google.genai import types
    # One Content per text: a plain list of strings is read by gemini-embedding-2
    # as the parts of ONE content and comes back as a single vector.
    result = client().models.embed_content(
        model=EMBED_MODEL, contents=[types.Content(parts=[types.Part(text=t)]) for t in texts],
        config=types.EmbedContentConfig(task_type=task, output_dimensionality=EMBED_DIM))
    vectors = [e.values for e in result.embeddings]
    if len(vectors) != len(texts):
        raise RuntimeError(f"asked for {len(texts)} embeddings, got {len(vectors)}")
    return vectors


def embed_and_store(chunks: list[dict], design: str = DEFAULT_DESIGN) -> int:
    """Embed the chunks that have no saved vector yet and store them.

    Returns how many were embedded. Stops cleanly on the daily quota: what was
    stored stays stored, and the next run carries on from there.
    """
    col = collection(design)
    have = set(col.get(ids=[c["id"] for c in chunks], include=[])["ids"]) if chunks else set()
    todo = [c for c in {c["id"]: c for c in chunks}.values() if c["id"] not in have]
    done = 0
    for i in range(0, len(todo), BATCH):
        batch = todo[i:i + BATCH]
        for attempt in range(4):
            try:
                vectors = embed([c["text"] for c in batch], "RETRIEVAL_DOCUMENT")
                break
            except Exception as error:  # noqa: BLE001
                msg = str(error)
                if "RESOURCE_EXHAUSTED" in msg and ("PerDay" in msg or "per day" in msg.lower()):
                    log(f"Daily embedding quota reached after {done} new vectors; run again tomorrow.")
                    return done
                if attempt == 3:
                    raise
                wait = 30 * (attempt + 1)
                log(f"Embedding failed ({msg[:120]}); retrying in {wait}s")
                time.sleep(wait)
        col.add(ids=[c["id"] for c in batch], embeddings=vectors, documents=[c["text"] for c in batch],
                metadatas=[{k: c.get(k, "") for k in ("source", "location", "file", "entries", "sha")}
                           for c in batch])
        done += len(batch)
        log(f"[{design}] stored {done}/{len(todo)} new vectors")
    return done


# ------------------------------------------------------------------------ main

def build(designs=DESIGNS) -> None:
    for doc in DOCUMENTS:
        download(doc)
    for design in designs:
        chunks = [c for doc in DOCUMENTS
                  for c in chunk_file(CORPUS / f"{doc['celex']}.xhtml", doc["source"], design)]
        words = sum(len(c["text"].split()) for c in chunks)
        log(f"[{design}] {len(chunks)} chunks, {words} words")
        # Drop corpus chunks that no longer exist (the chunking changed); added
        # documents are kept.
        col, keep = collection(design), {c["id"] for c in chunks}
        files = [f"{doc['celex']}.xhtml" for doc in DOCUMENTS]
        stale = [i for i in col.get(where={"file": {"$in": files}}, include=[])["ids"] if i not in keep]
        if stale:
            col.delete(ids=stale)
            log(f"[{design}] removed {len(stale)} outdated chunks")
        embed_and_store(chunks, design)
        log(f"[{design}] collection holds {collection(design).count()} vectors")


if __name__ == "__main__":
    build()
