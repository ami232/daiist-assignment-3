"""
Assignment 3: build the index (`main.py index`).

Corpus: EU air passenger rights (Regulations 261/2004, 2027/97, 1107/2006 and
the Commission's 2024 interpretative guidelines on 261/2004 and 1107/2006).

Pipeline, per file:
    download(celex)            -> corpus/<celex>.html  (Publications Office API)
    parse_file(path)           -> Document: sections (Article 7, Recital (12),
                                  Section 4.3.2, Annex I…) + footnotes
    chunk_document(doc, design)-> chunks with source + location metadata
        design "a": structure-based  (one chunk per article / recital group /
                                      guideline section; long ones split by
                                      paragraph at MAX_WORDS, tiny ones merged)
        design "b": fixed-size       (every MAX_WORDS words, ignoring structure)
    embed_and_store(chunks, design)-> Gemini vectors into ChromaDB (index/chroma),
                                      saved batch by batch; only chunks without
                                      a saved vector are embedded.

server.py imports chunk_file() and embed_and_store() for its add-document tool.
All logging goes to stderr (stdout belongs to the MCP protocol in server.py).

    uv run python index.py            # download, chunk, embed both designs
    uv run python index.py --dry-run  # everything except the embedding calls
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import statistics
import sys
import time
import urllib.request
from dataclasses import dataclass, field
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"
CHROMA_DIR = INDEX_DIR / "chroma"
QUERY_CACHE = INDEX_DIR / "query_cache.json"

EMBED_MODEL = "gemini-embedding-2"
MAX_WORDS = 300  # chunk size cap (design a) / fixed chunk size (design b)
MIN_WORDS = 50  # design a: a section shorter than this is merged into the next one
BATCH = 25  # texts per embedding request
DESIGNS = {"a": "structure", "b": "fixed"}

# The base corpus. doc_id is what eval/questions.csv uses as expected_source.
CORPUS = [
    {"doc_id": "reg_261_2004", "celex": "32004R0261",
     "title": "Regulation (EC) No 261/2004 on compensation and assistance to air passengers "
              "(denied boarding, cancellation, long delay)"},
    {"doc_id": "guidelines_261_2004", "celex": "52024XC05687",
     "title": "Commission Interpretative Guidelines (2024) on Regulation 261/2004 and Regulation 2027/97"},
    {"doc_id": "reg_2027_97", "celex": "01997R2027-20020530",
     "title": "Regulation (EC) No 2027/97 on air carrier liability for passengers and baggage "
              "(consolidated, as amended by Regulation 889/2002)"},
    {"doc_id": "reg_1107_2006", "celex": "32006R1107",
     "title": "Regulation (EC) No 1107/2006 on the rights of disabled persons and persons "
              "with reduced mobility when travelling by air"},
    {"doc_id": "guidelines_1107_2006", "celex": "52024XC05992",
     "title": "Commission Interpretative Guidelines (2024) on Regulation 1107/2006 "
              "(disabled persons and persons with reduced mobility)"},
]
BY_CELEX = {d["celex"]: d for d in CORPUS}


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


# --------------------------------------------------------------------------- download

def download(celex: str, dest_dir: Path = CORPUS_DIR) -> Path:
    """Fetch the English HTML of a EUR-Lex document by CELEX number (skipped if present).

    eur-lex.europa.eu blocks scripts, so this uses the Publications Office
    content API, which serves the same official HTML.
    """
    dest_dir.mkdir(parents=True, exist_ok=True)
    path = dest_dir / f"{celex}.html"
    if path.exists() and path.stat().st_size > 0:
        return path
    request = urllib.request.Request(
        f"http://publications.europa.eu/resource/celex/{celex}",
        headers={"Accept": "application/xhtml+xml;q=0.9, text/html;q=0.8", "Accept-Language": "eng"},
    )
    with urllib.request.urlopen(request, timeout=120) as response:
        path.write_bytes(response.read())
    log(f"downloaded {celex} -> {path.relative_to(ROOT)}")
    return path


# --------------------------------------------------------------------------- parsing

@dataclass
class Section:
    label: str  # "Article 7", "Recital (12)", "Section 4.3.2", "Annex I", "Preamble"
    title: str = ""
    paras: list[str] = field(default_factory=list)

    @property
    def words(self) -> int:
        return sum(len(strip_markers(p).split()) for p in self.paras)


@dataclass
class Document:
    doc_id: str
    title: str
    url: str
    sections: list[Section]
    notes: dict[str, str]  # footnote number -> text


FN = "⟦fn{}⟧"
FN_RE = re.compile(r"⟦fn(\w+)⟧")
ARTICLE_RE = re.compile(r"^Article (\d+[a-z]?)$")
ANNEX_RE = re.compile(r"^ANNEX(?: ([IVX]+))?$")
RECITAL_RE = re.compile(r"^\((\d+)\)\s+(.*)$")
SECTION_RE = re.compile(r"^(\d+(?:\.\d+)*)\.?\s+(.*)$")


def clean(text: str) -> str:
    text = re.sub(r"[▼►◄]\s*[A-Z]?\d*", " ", text)  # consolidation markers (▼M1 …)
    text = re.sub(r"\(\s*(⟦fn\w+⟧)\s*\)", r"\1", text)  # "( ⟦fn1⟧ )" -> "⟦fn1⟧"
    return " ".join(text.split())


def strip_markers(text: str) -> str:
    return " ".join(FN_RE.sub("", text).split())


def html_lines(soup: BeautifulSoup) -> list[tuple[str, str]]:
    """The document as (kind, text) lines in reading order.

    kind is "art"/"art_title"/"sec"/"doc_ti" when the HTML class says so,
    else "p". A table row (numbered list item, recital) becomes one line.
    """
    lines = []
    for el in soup.find_all(["tr", "p"]):
        if el.name == "tr":
            if el.find_parent("tr"):
                continue  # nested row: already inside its parent row's text
            cells = [c.get_text(" ") for c in el.find_all("td", recursive=False)]
            lines.append(("p", clean(" ".join(cells))))
            continue
        if el.find_parent("tr") or el.find("p"):
            continue
        classes = el.get("class") or []
        kind = ("art" if "oj-ti-art" in classes else
                "art_title" if "oj-sti-art" in classes else
                "sec" if "oj-ti-grseq-1" in classes else
                "doc_ti" if "oj-doc-ti" in classes else
                "toc" if "oj-ti-tbl" in classes else "p")
        lines.append((kind, clean(el.get_text(" "))))
    return [(k, t) for k, t in lines if t]


def extract_notes(soup: BeautifulSoup) -> dict[str, str]:
    """Pull footnotes out of the HTML and leave a ⟦fnN⟧ marker where each is cited."""
    notes = {}
    # Official Journal format: <p class="oj-note">; consolidated format: <p> holding a link back to "#src.E…"
    for p in soup.find_all("p"):
        back = p.find("a", href=re.compile(r"^#(ntc|src\.)"))
        if "oj-note" in (p.get("class") or []) or back:
            number = re.sub(r"\D", "", back.get_text() if back else "")
            text = clean(p.get_text(" "))
            text = re.sub(r"^\(\s*\d+\s*\)\s*", "", text)
            if number:
                notes[number] = text
            p.decompose()
    for a in soup.find_all("a", href=re.compile(r"^#(ntr|E\d)")):
        number = re.sub(r"\D", "", a.get_text())
        a.replace_with(f" {FN.format(number)} " if number in notes else "")
    return notes


def extract_plain_notes(lines: list[tuple[str, str]]) -> tuple[list[tuple[str, str]], dict[str, str]]:
    """Old EUR-Lex format (261/2004): notes are plain "(1) OJ C …" lines after the signature,
    cited as "Commission(1)" in the text."""
    end = next((i for i, (_, t) in enumerate(lines) if t.startswith("Done at")), None)
    if end is None:
        return lines, {}
    notes = {}
    for _, text in lines[end:]:
        m = RECITAL_RE.match(text)
        if m and re.match(r"(OJ|Opinion)", m.group(2)):
            notes[m.group(1)] = m.group(2)
    if not notes:
        return lines, {}
    ref = re.compile(r"(?<=[A-Za-z.)])\((\d+)\)")
    lines = [(k, ref.sub(lambda m: f" {FN.format(m.group(1))}" if m.group(1) in notes else m.group(0), t))
             for k, t in lines]
    return lines, notes


def parse_file(path: Path, doc_id: str | None = None, title: str | None = None) -> Document:
    """Turn one EUR-Lex HTML file into a Document of labelled sections."""
    path = Path(path)
    meta = BY_CELEX.get(path.stem, {})
    doc_id = doc_id or meta.get("doc_id") or re.sub(r"\W+", "_", path.stem).lower()
    soup = BeautifulSoup(path.read_bytes(), "html.parser")
    for junk in soup.select("script, style, #banner, h1"):
        junk.decompose()
    page_title = soup.title.get_text(" ").strip() if soup.title else path.stem
    for el in soup.select("title, head"):
        el.decompose()
    notes = extract_notes(soup)
    lines = html_lines(soup)
    if not notes:
        lines, notes = extract_plain_notes(lines)

    sections: list[Section] = [Section("Preamble")]
    in_toc = False
    after_signature = False
    seen_article = False
    pending_article_title = False
    for kind, text in lines:
        plain = strip_markers(text)
        if kind == "toc" or plain.upper() == "TABLE OF CONTENTS":
            in_toc = True
            continue
        if in_toc and kind != "sec":
            continue  # drop the table of contents: it repeats every heading
        in_toc = False

        if kind == "art" or (kind == "p" and ARTICLE_RE.match(plain)):
            sections.append(Section(f"Article {ARTICLE_RE.match(plain).group(1)}"))
            seen_article, after_signature, pending_article_title = True, False, True
            continue
        if pending_article_title and (kind == "art_title" or (kind == "p" and len(plain.split()) <= 12
                                                                and not plain[0].isdigit())):
            sections[-1].title = plain
            pending_article_title = False
            continue
        pending_article_title = False
        if ANNEX_RE.match(plain):
            sections.append(Section(f"Annex {ANNEX_RE.match(plain).group(1) or ''}".strip()))
            after_signature = False
            continue
        if kind == "sec":
            m = SECTION_RE.match(plain)
            if m:  # numbered heading (4.3.2. …) starts a section
                sections.append(Section(f"Section {m.group(1)}", m.group(2)))
                continue
            # unnumbered sub-heading ("a) …", "Pre-notification"): stays inside its section as a line
        if plain.startswith("This document is meant purely as a documentation tool"):
            continue  # disclaimer at the top of consolidated texts
        if plain.startswith("Done at") or plain.startswith("Commission Statement"):
            after_signature = True  # signatures, OJ notes, statements: not passenger rules
            continue
        if after_signature:
            continue
        if kind == "doc_ti" and sections[-1].label.startswith("Annex") and not sections[-1].title:
            sections[-1].title = plain
            continue
        recital = RECITAL_RE.match(plain)
        if recital and not seen_article and not any(s.label.startswith("Section") for s in sections):
            sections.append(Section(f"Recital ({recital.group(1)})"))
        sections[-1].paras.append(text)

    sections = [s for s in sections if s.paras]
    url = f"https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:{path.stem}"
    return Document(doc_id, title or meta.get("title") or page_title, url, sections, notes)


# --------------------------------------------------------------------------- chunking

def heading(section: Section) -> str:
    return f"{section.label} – {section.title}" if section.title else section.label


def split_words(paras: list[str], limit: int) -> list[list[str]]:
    """Group paragraphs into runs of at most `limit` words; split an oversized paragraph by sentence."""
    pieces = []
    for p in paras:
        if len(strip_markers(p).split()) <= limit:
            pieces.append(p)
        else:
            pieces.extend(s for s in re.split(r"(?<=[.;:])\s+(?=[A-Z(‘])", p) if s)
    groups, current, count = [], [], 0
    for piece in pieces:
        n = len(strip_markers(piece).split())
        if current and count + n > limit:
            groups.append(current)
            current, count = [], 0
        current.append(piece)
        count += n
    if current:
        groups.append(current)
    return groups


def make_chunk(doc: Document, design: str, labels: list[str], body: str, part: str = "") -> dict:
    """Attach the footnotes cited in `body`, then build the chunk record."""
    cited = list(dict.fromkeys(FN_RE.findall(body)))
    text = FN_RE.sub(lambda m: f"[{m.group(1)}]", body)
    text = re.sub(r" +\[", " [", text).strip()
    if cited:
        text += "\n\nFootnotes:\n" + "\n".join(f"[{n}] {doc.notes[n]}" for n in cited if n in doc.notes)
    labels = list(dict.fromkeys(labels))
    location = labels[0] if len(labels) == 1 else f"{labels[0]} to {labels[-1]}"
    return {
        "id": f"{doc.doc_id}:{design}:{hashlib.sha1(text.encode()).hexdigest()[:12]}",
        "text": text,
        "metadata": {
            "doc_id": doc.doc_id,
            "source": doc.title,
            "location": location + (f" (part {part})" if part else ""),
            "locations": "; ".join(labels),  # every section the chunk covers, for hit-rate checks
            "design": DESIGNS[design],
            "words": len(strip_markers(body).split()),
            "url": doc.url,
        },
    }


def chunk_structure(doc: Document) -> list[dict]:
    """Design a: one chunk per section. Recitals are packed together up to MAX_WORDS,
    sections under MIN_WORDS are merged into the next one, sections over MAX_WORDS
    are split at paragraph boundaries."""
    units: list[tuple[list[str], list[str]]] = []  # (labels, paragraphs with heading lines)
    for s in doc.sections:
        paras = ([heading(s)] if not s.label.startswith(("Recital", "Preamble")) else []) + s.paras
        if units:
            prev_labels, prev_paras = units[-1]
            prev_words = sum(len(strip_markers(p).split()) for p in prev_paras)
            both_recitals = s.label.startswith("Recital") and prev_labels[-1].startswith("Recital")
            if prev_words < MIN_WORDS or (both_recitals and prev_words + s.words <= MAX_WORDS):
                units[-1] = (prev_labels + [s.label], prev_paras + paras)
                continue
        units.append(([s.label], paras))

    chunks = []
    for labels, paras in units:
        groups = split_words(paras, MAX_WORDS)
        for i, group in enumerate(groups, 1):
            if i > 1 and not labels[0].startswith("Recital"):
                group = [f"{paras[0]} (continued)"] + group
            part = f"{i}/{len(groups)}" if len(groups) > 1 else ""
            chunks.append(make_chunk(doc, "a", labels, "\n".join(group), part))
    return chunks


def chunk_fixed(doc: Document) -> list[dict]:
    """Design b: the same text (headings included) cut every MAX_WORDS words, ignoring structure."""
    words: list[tuple[str, str]] = []  # (word, label of the section it belongs to)
    for s in doc.sections:
        lines = ([heading(s)] if not s.label.startswith(("Recital", "Preamble")) else []) + s.paras
        for line in lines:
            for w in line.split():
                words.append((w, s.label))
    chunks, current = [], []
    for w in words:
        current.append(w)
        if sum(1 for x, _ in current if not FN_RE.fullmatch(x)) >= MAX_WORDS:
            chunks.append(current)
            current = []
    if current:
        chunks.append(current)
    return [make_chunk(doc, "b", [lab for _, lab in c], " ".join(w for w, _ in c)) for c in chunks]


def chunk_document(doc: Document, design: str) -> list[dict]:
    return chunk_structure(doc) if design == "a" else chunk_fixed(doc)


def chunk_file(path: Path | str, design: str = "a", doc_id: str | None = None,
               title: str | None = None) -> list[dict]:
    """Parse and chunk one file (used by server.py's add-document tool)."""
    return chunk_document(parse_file(Path(path), doc_id, title), design)


# --------------------------------------------------------------------------- embedding

class QuotaExhausted(RuntimeError):
    pass


_client = None


def client():
    global _client
    if _client is None:
        from google import genai

        from api_key import load_api_key
        _client = genai.Client(api_key=load_api_key())
    return _client


def doc_prompt(chunk: dict) -> str:
    # gemini-embedding-2 takes the retrieval task as a text prefix (no task_type parameter).
    return f"title: {chunk['metadata']['source']} | text: {chunk['text']}"


def query_prompt(query: str) -> str:
    return f"task: search result | query: {query}"


def embed_texts(texts: list[str]) -> list[list[float]]:
    """One vector per text. Each text must be its own Content: a plain list of
    strings is embedded by gemini-embedding-2 as ONE input and returns ONE vector."""
    from google.genai import errors, types

    contents = [types.Content(parts=[types.Part(text=t)]) for t in texts]
    for attempt in range(7):
        try:
            result = client().models.embed_content(model=EMBED_MODEL, contents=contents)
            vectors = [e.values for e in result.embeddings]
            if len(vectors) != len(texts):
                raise RuntimeError(f"asked for {len(texts)} vectors, got {len(vectors)}")
            return vectors
        except errors.APIError as error:
            message = str(error)
            if error.code == 429 and re.search(r"per ?day|PerDay", message, re.I):
                raise QuotaExhausted(message) from error
            if error.code in (429, 500, 503) and attempt < 6:
                wait = min(60, 2 ** attempt * 2)
                log(f"embedding API {error.code}; retrying in {wait}s")
                time.sleep(wait)
                continue
            raise
    raise RuntimeError("unreachable")


def collection(design: str):
    import chromadb

    chroma = chromadb.PersistentClient(path=str(CHROMA_DIR))
    return chroma.get_or_create_collection(
        f"design_{design}", embedding_function=None, metadata={"hnsw:space": "cosine"})


def embed_and_store(chunks: list[dict], design: str) -> int:
    """Embed the chunks that have no saved vector yet and store them, batch by batch.
    Returns how many were embedded now."""
    if not chunks:
        return 0
    store = collection(design)
    ids = [c["id"] for c in chunks]
    saved = set(store.get(ids=ids, include=[])["ids"])
    todo = [c for c in chunks if c["id"] not in saved]
    for start in range(0, len(todo), BATCH):
        batch = todo[start:start + BATCH]
        vectors = embed_texts([doc_prompt(c) for c in batch])
        store.upsert(ids=[c["id"] for c in batch], embeddings=vectors,
                     documents=[c["text"] for c in batch], metadatas=[c["metadata"] for c in batch])
        log(f"design {design}: embedded {start + len(batch)}/{len(todo)}")
    return len(todo)


def embed_query(query: str) -> list[float]:
    """Embed a search query, caching vectors in index/query_cache.json so repeated
    questions (evaluation reruns, check.py) cost no quota."""
    text = query_prompt(query)
    key = hashlib.sha1(text.encode()).hexdigest()
    cache = json.loads(QUERY_CACHE.read_text()) if QUERY_CACHE.exists() else {}
    if key not in cache:
        cache[key] = embed_texts([text])[0]
        QUERY_CACHE.write_text(json.dumps(cache))
    return cache[key]


def search(query: str, design: str = "a", k: int = 5) -> list[dict]:
    """Return the k chunks of a design closest to the query, best first:
    [{"id", "text", "metadata", "score"}], score = cosine similarity."""
    store = collection(design)
    res = store.query(query_embeddings=[embed_query(query)], n_results=k,
                      include=["documents", "metadatas", "distances"])
    return [{"id": i, "text": t, "metadata": m, "score": round(1 - d, 4)}
            for i, t, m, d in zip(res["ids"][0], res["documents"][0], res["metadatas"][0], res["distances"][0])]


# --------------------------------------------------------------------------- main

def remove_stale(design: str, chunks: list[dict]) -> None:
    """Drop stored chunks of base-corpus documents that the current chunking no longer produces."""
    store = collection(design)
    current = {c["id"] for c in chunks}
    for doc in CORPUS:
        old = store.get(where={"doc_id": doc["doc_id"]}, include=[])["ids"]
        stale = [i for i in old if i not in current]
        if stale:
            store.delete(ids=stale)
            log(f"design {design}: removed {len(stale)} stale chunks of {doc['doc_id']}")


def main() -> int:
    parser = argparse.ArgumentParser(description="Build the index.")
    parser.add_argument("--dry-run", action="store_true", help="chunk and report, but don't embed")
    args = parser.parse_args()

    docs = [parse_file(download(d["celex"])) for d in CORPUS]
    total = sum(s.words for d in docs for s in d.sections)
    notes = sum(len(n.split()) for d in docs for n in d.notes.values())
    print(f"corpus: {len(docs)} documents, {total:,} words of text + {notes:,} words of footnotes")

    INDEX_DIR.mkdir(exist_ok=True)
    all_chunks = {}
    for design, name in DESIGNS.items():
        chunks = [c for d in docs for c in chunk_document(d, design)]
        all_chunks[design] = chunks
        sizes = [c["metadata"]["words"] for c in chunks]
        print(f"design {design} ({name}): {len(chunks)} chunks, words per chunk "
              f"min {min(sizes)} / median {statistics.median(sizes):.0f} / max {max(sizes)}")
        with (INDEX_DIR / f"chunks_design_{design}.jsonl").open("w", encoding="utf-8") as f:
            for c in chunks:
                f.write(json.dumps(c, ensure_ascii=False) + "\n")

    if args.dry_run:
        return 0
    for design, chunks in all_chunks.items():
        remove_stale(design, chunks)
        try:
            done = embed_and_store(chunks, design)
        except QuotaExhausted:
            print(f"Daily embedding quota reached during design {design}. Vectors so far are saved; "
                  f"run `main.py index` again after the quota resets (09:00 in Spain).", file=sys.stderr)
            return 1
        print(f"design {design}: {done} chunks embedded now, {len(chunks) - done} already saved")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
