"""
Assignment 3: build the index (`main.py index`).

Deal Desk: an assistant for the associates of a small M&A advisory boutique that answers
questions about EU merger control and EU foreign-investment screening, from the legal texts.

Pipeline, one function per step so server.py can reuse it:
    download_corpus()        EUR-Lex HTML -> corpus/            (git-ignored, re-downloadable)
    extract_units(path)      HTML -> ordered list of legal units (recital, article paragraph,
                             numbered paragraph of a notice) with source and location
    chunk_units(units, d)    units -> chunks for one retrieval design ("fixed" or "structure")
    embed_and_store(chunks)  embeds only chunks without a saved vector, stores them in index/

Everything is saved as it goes: vectors are written to index/vectors.jsonl after every batch,
so the daily free-tier limit or a crash never loses an embedding.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import time
from dataclasses import asdict, dataclass, field
from pathlib import Path

ROOT = Path(__file__).resolve().parent
CORPUS = ROOT / "corpus"
INDEX = ROOT / "index"
VECTORS = INDEX / "vectors.jsonl"      # sha256(text) -> vector, the embedding cache
CHUNKS = INDEX / "chunks_{design}.jsonl"  # the chunks of each design, with metadata

EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768            # smaller vectors keep index/ well under the 90 MB limit
BATCH = 50
DESIGNS = ("structure", "fixed")

# The corpus: four EU legal texts, all from EUR-Lex (reuse allowed under Commission
# Decision 2011/833/EU, with acknowledgement of the source).
DOCUMENTS = {
    "EUMR": {
        "celex": "32004R0139",
        "title": "Council Regulation (EC) No 139/2004 on the control of concentrations between undertakings (EU Merger Regulation)",
        "date": "2004-01-20",
    },
    "CJN": {
        "celex": "52008XC0416(08)",
        "title": "Commission Consolidated Jurisdictional Notice under Council Regulation (EC) No 139/2004",
        "date": "2008-04-16",
    },
    "FDI": {
        "celex": "32019R0452",
        "title": "Regulation (EU) 2019/452 establishing a framework for the screening of foreign direct investments into the Union",
        "date": "2019-03-19",
    },
    "RN": {
        "celex": "52008XC1022(01)",
        "title": "Commission notice on remedies acceptable under Council Regulation (EC) No 139/2004 and under Commission Regulation (EC) No 802/2004 (Remedies Notice)",
        "date": "2008-10-22",
    },
    "ARN": {
        "celex": "52005XC0305(02)",
        "title": "Commission Notice on restrictions directly related and necessary to concentrations (Ancillary Restraints Notice)",
        "date": "2005-03-05",
    },
}
URL = "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:{celex}"


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)  # stderr: server.py imports this module


# --------------------------------------------------------------------------- download

def corpus_path(doc_id: str) -> Path:
    return CORPUS / f"{doc_id}.html"


def download_corpus() -> None:
    """Download every document that is not in corpus/ yet."""
    import httpx

    CORPUS.mkdir(exist_ok=True)
    for doc_id, meta in DOCUMENTS.items():
        path = corpus_path(doc_id)
        if path.exists() and path.stat().st_size > 10_000:
            continue
        url = URL.format(celex=meta["celex"])
        for attempt in range(5):
            r = httpx.get(url, follow_redirects=True, timeout=60, headers={"User-Agent": "Mozilla/5.0 (course assignment)"})
            if r.status_code == 200 and len(r.content) > 10_000:
                path.write_bytes(r.content)
                log(f"downloaded {doc_id} ({len(r.content):,} bytes)")
                break
            log(f"{doc_id}: EUR-Lex answered {r.status_code}, retrying in {5 * (attempt + 1)}s")
            time.sleep(5 * (attempt + 1))
        else:
            raise RuntimeError(f"Could not download {doc_id} from {url}. Save that page as {path} and run again.")


# --------------------------------------------------------------------------- extract

@dataclass
class Unit:
    """The smallest piece of a legal text that has its own citation."""
    source: str           # document id, e.g. "EUMR"
    location: str         # e.g. "Art. 1(2)", "Recital 10", "para. 54", "Annex I"
    heading: str          # article title or section heading, for context
    text: str


# Footnote markers look like "( 21 )" (with inner spaces) in the notices; legal references like
# "Article 3(1)" have none, so they are kept.
FOOTNOTE_MARK = re.compile(r"\s*\(\s+\d{1,3}\s+\)")


def strip_notes(text: str) -> str:
    text = re.sub(r"\s*\(\s*\)", "", FOOTNOTE_MARK.sub("", text))  # empty brackets left by removed notes
    return re.sub(r"\s+([,.;:])", r"\1", text).strip()


def _clean(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def _blocks(html: str) -> list[tuple[str, str]]:
    """The text blocks of a EUR-Lex page in reading order, as (css class, text).

    EUR-Lex uses three layouts: old plain <p> pages (EUMR), Official Journal pages where each
    numbered paragraph is a table row (the notices), and the newer "oj-" pages (FDI). Footnote
    texts (class note / oj-note) are dropped, and footnote markers inside the text are removed
    later, because they only cite cases and documents.
    """
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(html, "html.parser")
    for tag in soup(["script", "style", "head"]):
        tag.decompose()
    for sup in soup.select("span.oj-note-tag, a.oj-note-tag"):
        sup.decompose()
    blocks = []
    for el in soup.find_all(["p", "tr"]):
        classes = " ".join(el.get("class", []))
        if el.name == "p" and el.find_parent("tr"):
            continue  # its row is read as a whole
        if "note" in classes.split() or "oj-note" in classes.split():
            continue
        if el.name == "tr" and el.find("tr"):
            # a numbered paragraph that contains a list: keep the row's own text (its number
            # and lead-in sentence); the list items are nested rows read right after it
            own = [p for p in el.find_all("p") if p.find_parent("tr") is el]
            text = _clean(" ".join(p.get_text(" ") for p in own))
            if text:
                blocks.append((classes, text))
            continue
        text = _clean(el.get_text(" "))
        if text:
            blocks.append((classes, text))
    return blocks


ARTICLE = re.compile(r"^Article (\d+[a-z]?)$")
RECITAL = re.compile(r"^\((\d+)\)\s+(.*)")
NUMBERED = re.compile(r"^(\d+)\.\s+(.*)")
NOTICE_PARA = re.compile(r"^\(?(\d{1,3})\)?\.?(?:\s+(.+))?$")  # the text may be in nested list rows
ANNEX = re.compile(r"^ANNEX\s*([IVX]*)$", re.I)


def _regulation_units(source: str, blocks: list[tuple[str, str]]) -> list[Unit]:
    """Recitals, then Article N(p) paragraphs, then annexes."""
    units: list[Unit] = []
    article, heading, para, buf = None, "", None, []
    in_recitals, in_annex = False, None

    def flush():
        nonlocal buf
        if buf:
            text = strip_notes(" ".join(buf)).strip()
            if in_annex:
                loc = f"Annex {in_annex}".strip()
            elif para:
                loc = f"Art. {article}({para})"
            else:
                loc = f"Art. {article}"
            units.append(Unit(source, loc, heading, text))
        buf = []

    lines = [t for _, t in blocks]
    i = 0
    while i < len(lines):
        t = lines[i]
        if t.startswith("Whereas"):
            in_recitals = True
        elif in_recitals and t.startswith(("HAS ADOPTED", "HAVE ADOPTED")):
            in_recitals = False
        elif in_recitals and (m := RECITAL.match(t)):
            units.append(Unit(source, f"Recital {m.group(1)}", "Recitals", strip_notes(m.group(2))))
        elif m := ARTICLE.match(t):
            flush()
            article, para, in_annex = m.group(1), None, None
            heading = lines[i + 1] if i + 1 < len(lines) and not NUMBERED.match(lines[i + 1]) else ""
            if heading:
                i += 1
        elif m := ANNEX.match(t):
            flush()
            in_annex, article, para, heading = m.group(1) or "", None, None, "Annex"
        elif article or in_annex is not None:
            if t.startswith("This Regulation shall be binding in its entirety"):
                flush()
                break
            if (m := NUMBERED.match(t)) and not in_annex:
                flush()
                para = m.group(1)
                buf.append(m.group(2))
            else:
                buf.append(t)
        i += 1
    flush()
    return [u for u in units if len(u.text.split()) >= 3]


def _notice_units(source: str, blocks: list[tuple[str, str]]) -> list[Unit]:
    """Numbered paragraphs, each with the section heading it sits under."""
    units: list[Unit] = []
    heading, started = "", False
    for classes, t in blocks:
        if "ti-grseq" in classes or "ti-grseq-1" in classes:
            started = True
            heading = t
            continue
        if not started:
            continue  # title page and table of contents
        if "ti-" in classes and len(t.split()) < 20:
            heading = t
            continue
        m = NOTICE_PARA.match(t)
        last = int(units[-1].location.split()[-1]) if units else 0
        if m and last < int(m.group(1)) <= last + 3:  # paragraph numbers only go up; anything else
            # (a numbered row inside a table, a list item) is a continuation of the last paragraph
            text = strip_notes(m.group(2) or "").strip()
            units.append(Unit(source, f"para. {m.group(1)}", heading, text))
        elif units and not t.startswith(("OJ ", "Official Journal")):
            # an unnumbered continuation (a list inside a paragraph): attach it to the last one
            units[-1].text += " " + strip_notes(t)
    return units


def extract_units(path: str | Path, source: str | None = None) -> list[Unit]:
    """Read one EUR-Lex HTML file (or a plain .txt/.md file) and return its citable units."""
    path = Path(path)
    source = source or path.stem
    if path.suffix.lower() in {".txt", ".md"}:
        paras = [p.strip() for p in re.split(r"\n\s*\n", path.read_text(encoding="utf-8")) if p.strip()]
        return [Unit(source, f"para. {i}", "", _clean(p)) for i, p in enumerate(paras, 1)]
    if path.suffix.lower() == ".pdf":
        from pypdf import PdfReader
        units = []
        for n, page in enumerate(PdfReader(str(path)).pages, 1):
            text = _clean(page.extract_text() or "")
            if text:
                units.append(Unit(source, f"p. {n}", "", text))
        return units
    blocks = _blocks(path.read_text(encoding="utf-8", errors="replace"))
    is_regulation = any(ARTICLE.match(t) for _, t in blocks)
    is_notice = sum(1 for c, _ in blocks if "ti-grseq" in c) > 0 and not is_regulation
    units = _notice_units(source, blocks) if is_notice else _regulation_units(source, blocks)
    if not units:
        raise ValueError(f"No legal structure found in {path}.")
    return units


# --------------------------------------------------------------------------- chunk

@dataclass
class Chunk:
    id: str
    design: str
    source: str
    location: str          # citation: one unit, or "first – last" for a fixed window
    heading: str
    text: str              # what the reader sees
    embed_text: str        # what is embedded (text with its context header)
    units: list[str] = field(default_factory=list)  # every unit location the chunk covers

    @property
    def sha(self) -> str:
        return hashlib.sha256(self.embed_text.encode()).hexdigest()


def _header(source: str, heading: str, location: str) -> str:
    title = DOCUMENTS.get(source, {}).get("title", source)
    return f"{title} | {location} | {heading}".strip(" |")


def chunk_units(units: list[Unit], design: str, size: int = 200, overlap: int = 40,
                max_words: int = 300, min_words: int = 40) -> list[Chunk]:
    """Turn units into chunks for one retrieval design.

    structure: one chunk per legal unit (article paragraph, recital, notice paragraph); short
               paragraphs of the same article are merged up to max_words, long ones are split.
    fixed:     the document read as one stream and cut every `size` words with `overlap`,
               ignoring the structure; its citation is the range of units it covers.
    """
    chunks: list[Chunk] = []
    if design == "structure":
        groups: list[list[Unit]] = []
        for u in units:
            last = groups[-1] if groups else None
            same_article = last and u.location.split("(")[0] == last[-1].location.split("(")[0] and u.location.startswith("Art.")
            if last and same_article and sum(len(x.text.split()) for x in last) + len(u.text.split()) <= max_words \
                    and sum(len(x.text.split()) for x in last) < min_words * 3:
                last.append(u)
            else:
                groups.append([u])
        for g in groups:
            words = " ".join(u.text for u in g).split()
            loc = g[0].location if len(g) == 1 else _range_label(g[0].location, g[-1].location)
            parts = [words[i:i + max_words] for i in range(0, len(words), max_words - 50)] if len(words) > max_words else [words]
            for k, part in enumerate(parts):
                text = " ".join(part)
                cid = f"{g[0].source}|{loc}|{k}"
                chunks.append(Chunk(cid, design, g[0].source, loc, g[0].heading, text,
                                    _header(g[0].source, g[0].heading, loc) + "\n" + text, [u.location for u in g]))
    elif design == "fixed":
        by_source: dict[str, list[Unit]] = {}
        for u in units:
            by_source.setdefault(u.source, []).append(u)
        for source, us in by_source.items():
            stream: list[tuple[str, str]] = [(w, u.location) for u in us for w in u.text.split()]
            step = size - overlap
            for i in range(0, max(1, len(stream) - overlap), step):
                window = stream[i:i + size]
                if not window:
                    break
                covered = list(dict.fromkeys(loc for _, loc in window))
                loc = covered[0] if len(covered) == 1 else _range_label(covered[0], covered[-1])
                text = " ".join(w for w, _ in window)
                chunks.append(Chunk(f"{source}|w{i}", design, source, loc, "", text,
                                    _header(source, "", loc) + "\n" + text, covered))
    else:
        raise ValueError(f"Unknown design {design!r}")
    return chunks


def _range_label(first: str, last: str) -> str:
    if first.startswith("Art. ") and last.startswith("Art. ") and first.split("(")[0] == last.split("(")[0]:
        return f"{first}–({last.split('(', 1)[1]}" if "(" in last else f"{first}–{last}"
    return f"{first} – {last}"


def chunk_file(path: str | Path, design: str = "structure", source: str | None = None) -> list[Chunk]:
    """One file -> its chunks for a design. Used by add_document in server.py."""
    return chunk_units(extract_units(path, source), design)


# --------------------------------------------------------------------------- embed and store

def load_vectors() -> dict[str, list[float]]:
    vectors = {}
    if VECTORS.exists():
        for line in VECTORS.read_text().splitlines():
            if line.strip():
                rec = json.loads(line)
                vectors[rec["sha"]] = rec["v"]
    return vectors


def _client():
    from google import genai
    from api_key import load_api_key
    return genai.Client(api_key=load_api_key())


def embed_texts(texts: list[str], task: str = "RETRIEVAL_DOCUMENT", client=None) -> list[list[float]]:
    from google.genai import types
    client = client or _client()
    for attempt in range(6):
        try:
            # one Content per text: a plain list of strings is read as ONE multi-part input by
            # gemini-embedding-2 and comes back as a single vector
            contents = [types.Content(parts=[types.Part(text=t)]) for t in texts]
            res = client.models.embed_content(
                model=EMBED_MODEL, contents=contents,
                config=types.EmbedContentConfig(task_type=task, output_dimensionality=EMBED_DIM))
            return [e.values for e in res.embeddings]
        except Exception as error:  # noqa: BLE001 - rate limits are retried, the rest re-raised
            message = str(error)
            if "429" in message or "RESOURCE_EXHAUSTED" in message or "503" in message:
                if "PerDay" in message or "per day" in message.lower():
                    raise RuntimeError("Daily embedding quota reached. Vectors so far are saved; run again tomorrow.") from error
                wait = 20 * (attempt + 1)
                log(f"rate limited, waiting {wait}s")
                time.sleep(wait)
                continue
            raise
    raise RuntimeError("Embedding kept failing after retries.")


def embed_query(text: str) -> list[float]:
    return embed_texts([text], task="RETRIEVAL_QUERY")[0]


def embed_and_store(chunks: list[Chunk]) -> dict[str, list[float]]:
    """Embed only the chunks whose text has no saved vector; append each batch to index/vectors.jsonl."""
    INDEX.mkdir(exist_ok=True)
    vectors = load_vectors()
    todo = [c for c in chunks if c.sha not in vectors]
    todo = list({c.sha: c for c in todo}.values())
    if todo:
        log(f"embedding {len(todo)} new chunks ({len(chunks) - len(todo)} already saved)")
        client = _client()
        with VECTORS.open("a") as f:
            for i in range(0, len(todo), BATCH):
                batch = todo[i:i + BATCH]
                got = embed_texts([c.embed_text for c in batch], client=client)
                if len(got) != len(batch):
                    raise RuntimeError(f"asked for {len(batch)} embeddings, got {len(got)}")
                for c, v in zip(batch, got):
                    vectors[c.sha] = v
                    f.write(json.dumps({"sha": c.sha, "v": [round(x, 6) for x in v]}) + "\n")
                f.flush()
                log(f"  {min(i + BATCH, len(todo))}/{len(todo)}")
    return vectors


def save_chunks(chunks: list[Chunk], design: str, append: bool = False) -> None:
    path = Path(str(CHUNKS).format(design=design))
    mode = "a" if append else "w"
    with path.open(mode) as f:
        for c in chunks:
            rec = asdict(c)
            rec["sha"] = c.sha
            f.write(json.dumps(rec, ensure_ascii=False) + "\n")


def load_chunks(design: str) -> list[dict]:
    path = Path(str(CHUNKS).format(design=design))
    return [json.loads(line) for line in path.read_text().splitlines() if line.strip()] if path.exists() else []


def corpus_units() -> list[Unit]:
    units = []
    for doc_id in DOCUMENTS:
        units += extract_units(corpus_path(doc_id), doc_id)
    return units


def main() -> None:
    download_corpus()
    units = corpus_units()
    words = {d: sum(len(u.text.split()) for u in units if u.source == d) for d in DOCUMENTS}
    log("units per document:", {d: sum(u.source == d for u in units) for d in DOCUMENTS})
    log("words per document:", words, "total", sum(words.values()))
    stats = {"documents": {d: {"units": sum(u.source == d for u in units), "words": words[d]} for d in DOCUMENTS},
             "total_words": sum(words.values()), "designs": {}}
    for design in DESIGNS:
        chunks = chunk_units(units, design)
        stats["designs"][design] = {"chunks": len(chunks),
                                    "avg_words": round(sum(len(c.text.split()) for c in chunks) / len(chunks))}
        INDEX.mkdir(exist_ok=True)
        (INDEX / "stats.json").write_text(json.dumps(stats, indent=2))  # the numbers quoted in REPORT.md
        # keep chunks added later with add_document (they are not in DOCUMENTS)
        extra = [c for c in load_chunks(design) if c["source"] not in DOCUMENTS]
        save_chunks(chunks, design)
        if extra:
            with Path(str(CHUNKS).format(design=design)).open("a") as f:
                for rec in extra:
                    f.write(json.dumps(rec, ensure_ascii=False) + "\n")
        log(f"{design}: {len(chunks)} chunks, avg {sum(len(c.text.split()) for c in chunks) / len(chunks):.0f} words")
        embed_and_store(chunks)
    log("index ready in", INDEX)


if __name__ == "__main__":
    main()
