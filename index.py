"""
Assignment 3: build the index (`main.py index`). May be index.ipynb instead.

Download the corpus (into corpus/, git-ignored), extract, clean and chunk it
with source and location metadata, embed with Gemini, and store everything in
index/. Save each vector as you get it and embed only chunks without one.

Per-file steps are plain functions (`chunk_file`, `embed_and_store`) because
server.py's add-document tool imports them.

Scope: only the operative text (articles) of each regulation is indexed;
recitals and annexes are left out (see REPORT.md, Ingestion).
"""

import hashlib
import os
import re
import sys
import time
from pathlib import Path

from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
EURLEX_URL = "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri={uri}"

# key = file stem in corpus/; name = the `source` stored in every chunk
SOURCES = {
    "ai_act": {"name": "AI Act", "uri": "OJ:L_202401689"},     # Regulation (EU) 2024/1689
    "gdpr": {"name": "GDPR", "uri": "CELEX:32016R0679"},       # Regulation (EU) 2016/679
    "data_act": {"name": "Data Act", "uri": "CELEX:32023R2854"},  # Regulation (EU) 2023/2854
}

DESIGNS = ("fixed", "structure")

# documents added later with add_document (not downloaded; their file stem is not in SOURCES)
EXTRA_SOURCE_NAMES = {"ai_act_annex_iii": "AI Act Annex III"}


# --------------------------------------------------------------------------
# Download
# --------------------------------------------------------------------------
def download_corpus() -> None:
    """Fetch the three EUR-Lex texts into corpus/ (skips files already there)."""
    CORPUS_DIR.mkdir(exist_ok=True)
    for key, spec in SOURCES.items():
        path = CORPUS_DIR / f"{key}.html"
        if path.exists() and path.stat().st_size > 100_000:
            continue
        import httpx  # lazy: only needed when a file is missing

        print(f"downloading {spec['name']} ...", file=sys.stderr)
        r = httpx.get(
            EURLEX_URL.format(uri=spec["uri"]),
            follow_redirects=True, timeout=90, headers={"User-Agent": "Mozilla/5.0"},
        )
        r.raise_for_status()
        if b"oj-ti-art" not in r.content:
            raise RuntimeError(f"{spec['name']}: the download is not the legal text")
        path.write_bytes(r.content)


# --------------------------------------------------------------------------
# Extract and clean
# --------------------------------------------------------------------------
def _clean(text: str) -> str:
    """Normalise non-breaking spaces and whitespace ('Annex\\xa0III' -> 'Annex III')."""
    return re.sub(r"\s+", " ", text.replace("\xa0", " ")).strip()


def _strip_footnotes(soup: BeautifulSoup) -> None:
    """Remove footnote bodies and their '(1)' markers inside the running text."""
    for tag in soup.select(".oj-note"):
        tag.decompose()
    for tag in soup.select(".oj-note-tag"):
        link = tag.find_parent("a")
        (link or tag).decompose()


def _chapter_of(div) -> str:
    for parent in div.parents:
        if re.match(r"^cpt_[IVXLC]+$", parent.get("id", "") or ""):
            head = parent.find("p", class_="oj-ti-section-1")
            name = parent.find("p", class_="oj-ti-section-2")
            parts = [_clean(x.get_text(" ")) for x in (head, name) if x]
            return " - ".join(parts)
    return ""


_PARA_START = re.compile(r"^(?:(\d+)\.|\((\d+)\))\s")


def _paragraphs(div) -> list[dict]:
    """Split an article/annex body into numbered paragraphs: [{label, text}]."""
    paras: list[dict] = []
    for child in div.children:
        if getattr(child, "name", None) is None:
            continue
        classes = child.get("class") or []
        if "oj-ti-art" in classes or "oj-ti-grseq-1" in classes or "eli-title" in classes:
            continue
        text = _clean(child.get_text(" "))
        if not text:
            continue
        m = _PARA_START.match(text)
        if m or not paras:
            paras.append({"label": (m.group(1) or m.group(2)) if m else "", "text": text})
        else:  # a list table or continuation belongs to the previous paragraph
            paras[-1]["text"] += " " + text
    return paras


def parse_units(html: str, source: str, include_annexes: bool = False) -> list[dict]:
    """Return one unit per article (and per annex if asked)."""
    soup = BeautifulSoup(html, "html.parser")
    _strip_footnotes(soup)
    units = []
    for div in soup.find_all("div", id=re.compile(r"^art_\d+$")):
        num = div["id"].split("_")[1]
        title = div.find("p", class_="oj-sti-art")
        units.append({
            "source": source, "label": f"Article {num}",
            "title": _clean(title.get_text(" ")) if title else "",
            "chapter": _chapter_of(div), "paragraphs": _paragraphs(div),
        })
    if include_annexes:
        for div in soup.find_all("div", id=re.compile(r"^anx_[IVXLC]+$")):
            roman = div["id"].split("_")[1]
            title = div.find("p", class_="oj-doc-ti") or div.find("p", class_="oj-ti-grseq-1")
            units.append({
                "source": source, "label": f"Annex {roman}",
                "title": _clean(title.get_text(" ")) if title else "",
                "chapter": "", "paragraphs": _paragraphs(div),
            })
    return [u for u in units if u["paragraphs"]]


# --------------------------------------------------------------------------
# Chunking: two designs
# --------------------------------------------------------------------------
def _label_range(labels: list[str]) -> str:
    labels = [x for x in labels if x]
    if not labels:
        return ""
    return f"({labels[0]})" if labels[0] == labels[-1] else f"({labels[0]})-({labels[-1]})"


def _make_chunk(unit: dict, design: str, labels: list[str], text: str) -> dict:
    location = unit["label"] + _label_range(labels)
    header = " | ".join(x for x in (unit["source"], unit["chapter"], f"{unit['label']}: {unit['title']}") if x)
    return {
        "id": hashlib.sha1(f"{design}|{unit['source']}|{location}|{text}".encode()).hexdigest()[:16],
        "design": design, "source": unit["source"], "chapter": unit["chapter"],
        "article": unit["label"], "title": unit["title"], "location": location,
        "text": text, "embed_text": f"title: {header} | text: {text}", "words": len(text.split()),
    }


def chunk_fixed(unit: dict, size: int = 150, step: int = 120, tail: int = 30) -> list[dict]:
    """Design A: 150-word windows, 30 words of overlap, never crossing an article."""
    words, owners = [], []
    for p in unit["paragraphs"]:
        w = p["text"].split()
        words += w
        owners += [p["label"]] * len(w)
    n, start, out = len(words), 0, []
    while start < n:
        end = min(start + size, n)
        if n - end < tail:  # do not leave a tiny last window
            end = n
        labels = list(dict.fromkeys(owners[start:end]))
        out.append(_make_chunk(unit, "fixed", labels, " ".join(words[start:end])))
        if end == n:
            break
        start += step
    return out


def _split_sentences(text: str, max_words: int) -> list[str]:
    parts, cur = [], []
    for sent in re.split(r"(?<=[.;:])\s+", text):
        for piece in _hard_split(sent, max_words):
            if cur and len(" ".join(cur + [piece]).split()) > max_words:
                parts.append(" ".join(cur))
                cur = []
            cur.append(piece)
    if cur:
        parts.append(" ".join(cur))
    return parts


def _hard_split(sentence: str, max_words: int) -> list[str]:
    w = sentence.split()
    return [" ".join(w[i:i + max_words]) for i in range(0, len(w), max_words)] or [""]


def chunk_structure(unit: dict, min_words: int = 60, max_words: int = 250) -> list[dict]:
    """Design B: one chunk per numbered paragraph; tiny ones merged, huge ones split."""
    pieces = []
    for p in unit["paragraphs"]:
        if len(p["text"].split()) <= max_words:
            pieces.append((p["label"], p["text"]))
        else:
            pieces += [(p["label"], part) for part in _split_sentences(p["text"], max_words)]
    chunks, cur = [], None
    for label, text in pieces:
        small = cur and len(cur["text"].split()) < min_words
        if small and len(cur["text"].split()) + len(text.split()) <= max_words:
            cur["text"] += " " + text
            cur["labels"].append(label)
        else:
            if cur:
                chunks.append(cur)
            cur = {"text": text, "labels": [label]}
    if cur:
        chunks.append(cur)
    return [_make_chunk(unit, "structure", c["labels"], c["text"]) for c in chunks]


def chunk_file(path, design: str = "structure", include_annexes: bool = False) -> list[dict]:
    """Whole pipeline for one file: parse -> clean -> chunk. server.py imports this."""
    path = Path(path)
    source = SOURCES.get(path.stem, {}).get("name") or EXTRA_SOURCE_NAMES.get(path.stem, path.stem)
    html = path.read_text(encoding="utf-8", errors="replace")
    chunker = chunk_fixed if design == "fixed" else chunk_structure
    return [c for u in parse_units(html, source, include_annexes) for c in chunker(u)]


# --------------------------------------------------------------------------
# Embed and store (Gemini + ChromaDB)
# --------------------------------------------------------------------------
EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768  # allowed 128-3072; the model normalises truncated vectors itself
BATCH = 50
INDEX_DIR = Path(os.environ["INDEX_DIR"]) if os.environ.get("INDEX_DIR") else ROOT / "index"  # override: throwaway copy for the add-document demo
META_KEYS = ("design", "source", "chapter", "article", "title", "location", "words")


class DailyQuotaError(RuntimeError):
    """The free tier's daily embedding quota is spent."""


def log(*args) -> None:
    # stdout carries the MCP protocol when server.py imports this module
    print(*args, file=sys.stderr, flush=True)


def _client():
    from google import genai
    from api_key import load_api_key

    return genai.Client(api_key=load_api_key())


def embed_texts(texts: list[str], client=None) -> list[list[float]]:
    """One Gemini call, one vector per text (each text counts against the daily quota)."""
    from google.genai import types

    client = client or _client()
    contents = [types.Content(parts=[types.Part.from_text(text=t)]) for t in texts]
    config = types.EmbedContentConfig(output_dimensionality=EMBED_DIM)
    for attempt in range(1, 7):
        try:
            result = client.models.embed_content(model=EMBED_MODEL, contents=contents, config=config)
            vectors = [e.values for e in result.embeddings]
            if len(vectors) != len(texts):
                raise RuntimeError(f"asked for {len(texts)} vectors, got {len(vectors)}")
            return vectors
        except Exception as e:  # noqa: BLE001 - classify by status code below
            code = getattr(e, "code", None)
            message = str(e).lower().replace("_", "").replace(" ", "")
            if code == 429 and "perday" in message:
                raise DailyQuotaError("daily embedding quota reached") from e
            if code in (429, 500, 503) and attempt < 6:
                wait = 20 * attempt
                log(f"  Gemini returned {code}; waiting {wait}s (attempt {attempt}/5)")
                time.sleep(wait)
                continue
            raise


QUERY_PREFIX = "task: search result | query: "


def embed_query(query: str, client=None) -> list[float]:
    """Queries use a different prefix than documents (asymmetric retrieval)."""
    return embed_texts([QUERY_PREFIX + query], client)[0]


def get_collection(design: str):
    import chromadb

    INDEX_DIR.mkdir(exist_ok=True)
    return chromadb.PersistentClient(path=str(INDEX_DIR)).get_or_create_collection(f"chunks_{design}")


def embed_and_store(chunks: list[dict], design: str, limit: int | None = None) -> int:
    """Embed only the chunks without a saved vector; save after every batch."""
    col = get_collection(design)
    ids = [c["id"] for c in chunks]
    have: set[str] = set()
    for i in range(0, len(ids), 500):
        have |= set(col.get(ids=ids[i:i + 500], include=[])["ids"])
    todo = [c for c in chunks if c["id"] not in have]
    log(f"[{design}] {len(chunks)} chunks, {len(have)} already stored, {len(todo)} to embed")
    if limit is not None:
        todo = todo[:limit]
    client = _client() if todo else None
    done = 0
    for i in range(0, len(todo), BATCH):
        batch = todo[i:i + BATCH]
        vectors = embed_texts([c["embed_text"] for c in batch], client)
        col.add(
            ids=[c["id"] for c in batch], embeddings=vectors,
            documents=[c["text"] for c in batch],
            metadatas=[{k: c[k] for k in META_KEYS} for c in batch],
        )
        done += len(batch)
        log(f"  stored {done}/{len(todo)}")
    return done


# --------------------------------------------------------------------------
# Main
# --------------------------------------------------------------------------
def main() -> None:
    """DESIGNS=fixed,structure (default: both) and INDEX_LIMIT=n (smoke test) are optional."""
    download_corpus()
    designs = [d for d in os.environ.get("DESIGNS", ",".join(DESIGNS)).split(",") if d]
    for d in designs:
        if d not in DESIGNS:
            raise SystemExit(f"unknown design {d!r}; use one of {DESIGNS}")
    limit = int(os.environ["INDEX_LIMIT"]) if os.environ.get("INDEX_LIMIT") else None
    incomplete = False
    for design in designs:
        chunks = [c for key in SOURCES for c in chunk_file(CORPUS_DIR / f"{key}.html", design)]
        try:
            embed_and_store(chunks, design, limit)
        except DailyQuotaError:
            log(f"[{design}] daily quota reached: progress is saved, run again after 09:00 (Spain)")
        stored = get_collection(design).count()
        log(f"[{design}] index holds {stored}/{len(chunks)} chunks")
        incomplete |= stored < len(chunks)
    if incomplete:
        raise SystemExit("index incomplete: run the same command again to resume")


if __name__ == "__main__":
    main()
