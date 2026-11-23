"""
Assignment 3: build the index (`main.py index`).

Corpus: three EU data regulations from EUR-Lex, operative part only (articles,
no recitals). Two chunking designs are built and compared in evaluate.py:

  article : one chunk per article (long articles are split at paragraph
            boundaries); the article title is part of the embedded text.
  fixed   : sliding window of ~200 words with 40 words of overlap over the
            whole document, ignoring structure.

Every chunk carries: source, location ("Article 22"), title, chapter, part.
Vectors are saved in ChromaDB (index/) as soon as they are received; only
chunks without a saved vector are embedded. A daily budget stops the run
before the free-tier limit; run it again tomorrow and it resumes.

server.py imports: chunk_file, embed_and_store, add_file, embed_query,
open_collection, CHOSEN_DESIGN.
"""

from __future__ import annotations

import hashlib
import os
import re
import sys
import time
from pathlib import Path

import chromadb
import httpx
from bs4 import BeautifulSoup, Tag

from api_key import load_api_key

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = Path(os.environ.get("CORPUS_INDEX_DIR") or ROOT / "index")

EMBED_MODEL = "gemini-embedding-2"
EMBED_BATCH = 50          # texts per API call (each text counts for the quota)
DAILY_BUDGET = 850        # stop a run after this many new embeddings
FIXED_WORDS, FIXED_OVERLAP = 200, 40
ARTICLE_MAX_WORDS = 350   # split an article only above this size

DESIGNS = ("article", "fixed")
CHOSEN_DESIGN = "article"  # the design server.py searches and adds to; change after evaluate.py

#stem -> (label used as `source`, EUR-Lex URL). Anything else is added later via add_document.
CORPUS = {
    "gdpr": ("GDPR", "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32016R0679"),
    "data_act": ("Data Act", "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32023R2854"),
    "dga": ("Data Governance Act", "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32022R0868"),
}
#Held back for the "add a document" demo (not downloaded by `main.py index`).
EXTRA = {
    "free_flow": ("Free Flow of Non-Personal Data Regulation",
                  "https://eur-lex.europa.eu/legal-content/EN/TXT/HTML/?uri=CELEX:32018R1807"),
}
LABELS = {stem: label for stem, (label, _) in {**CORPUS, **EXTRA}.items()}


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)   # stdout is reserved for the MCP protocol in server.py


#download

def download(stem: str, url: str) -> Path:
    CORPUS_DIR.mkdir(exist_ok=True)
    path = CORPUS_DIR / f"{stem}.html"
    if path.exists() and path.stat().st_size > 10_000:
        return path
    log(f"downloading {stem} ...")
    response = httpx.get(url, follow_redirects=True, timeout=90,
                         headers={"User-Agent": "Mozilla/5.0 (course assignment; RAG corpus download)"})
    response.raise_for_status()
    path.write_bytes(response.content)
    return path


#extraction

def _clean(text: str) -> str:
    return re.sub(r"\s+", " ", text.replace("\xa0", " ")).strip()


def _blocks(node: Tag) -> list[str]:
    """Text blocks of an article in reading order: paragraphs, and one block per table row
    (EUR-Lex lays out '(a) text' lists as tables; reading cells separately would split them)."""
    out: list[str] = []
    for child in node.children:
        if not isinstance(child, Tag):
            continue
        classes = child.get("class") or []
        if "eli-title" in classes or "oj-ti-art" in classes or "oj-sti-art" in classes:
            continue
        if child.name == "p":
            text = _clean(child.get_text(" "))
            if text:
                out.append(text)
        elif child.name == "table":
            for row in child.find_all("tr"):
                text = _clean(" ".join(td.get_text(" ") for td in row.find_all("td")))
                if text:
                    out.append(text)
        else:
            out.extend(_blocks(child))
    return out


def parse_eurlex(html: str) -> list[dict]:
    """EUR-Lex HTML -> one dict per article: number, title, chapter, blocks."""
    soup = BeautifulSoup(html, "html.parser")
    articles = []
    for div in soup.find_all("div", id=re.compile(r"^art_\d+$")):
        number = int(div["id"].split("_")[1])
        title_tag = div.find("p", class_="oj-sti-art")
        title = _clean(title_tag.get_text(" ")) if title_tag else ""
        chapter = ""
        cpt = div.find_parent("div", id=re.compile(r"^cpt_[IVXLC]+$"))
        if cpt:
            heading = cpt.find("div", id=cpt["id"] + ".tit_1")
            name = _clean(heading.get_text(" ")) if heading else ""
            chapter = f"Chapter {cpt['id'].split('_')[1]}" + (f": {name}" if name else "")
        blocks = _blocks(div)
        if blocks:
            articles.append({"number": number, "title": title, "chapter": chapter, "blocks": blocks})
    return articles


def parse_generic(path: Path) -> list[dict]:
    """Fallback for files that are not EUR-Lex HTML: PDF pages, or text split into sections.
    Returned as pseudo-articles whose location is 'page N' / 'section N'."""
    suffix = path.suffix.lower()
    units: list[tuple[str, str]] = []
    if suffix == ".pdf":
        from pypdf import PdfReader
        for i, page in enumerate(PdfReader(str(path)).pages, 1):
            units.append((f"page {i}", page.extract_text() or ""))
    else:
        raw = path.read_text(encoding="utf-8", errors="ignore")
        if suffix in (".html", ".htm"):
            raw = BeautifulSoup(raw, "html.parser").get_text("\n")
        paragraphs = [p.strip() for p in re.split(r"\n\s*\n", raw) if p.strip()]
        group, count, n = [], 0, 1
        for p in paragraphs:
            group.append(p)
            count += len(p.split())
            if count >= ARTICLE_MAX_WORDS:
                units.append((f"section {n}", "\n".join(group)))
                group, count, n = [], 0, n + 1
        if group:
            units.append((f"section {n}", "\n".join(group)))
    return [{"location": loc, "title": "", "chapter": "",
             "blocks": [b for b in (_clean(x) for x in text.split("\n")) if b]} for loc, text in units if text.strip()]


def load_document(path: Path) -> list[dict]:
    """Every document becomes a list of units with a `location`, `title`, `chapter`, `blocks`."""
    if path.suffix.lower() in (".html", ".htm"):
        articles = parse_eurlex(path.read_text(encoding="utf-8", errors="ignore"))
        if articles:
            for a in articles:
                a["location"] = f"Article {a['number']}"
            return articles
    return parse_generic(path)


#chunking

def _wc(text: str) -> int:
    return len(text.split())


def _chunk_id(design: str, source: str, location: str, part: int, text: str) -> str:
    digest = hashlib.sha1(text.encode("utf-8")).hexdigest()[:12]
    return f"{design}|{source}|{location}|{part}|{digest}"


def chunk_article_design(source: str, units: list[dict]) -> list[dict]:
    chunks = []
    for u in units:
        # greedy grouping of blocks up to ARTICLE_MAX_WORDS
        groups, cur, count = [], [], 0
        for b in u["blocks"]:
            if cur and count + _wc(b) > ARTICLE_MAX_WORDS:
                groups.append(cur)
                cur, count = [], 0
            cur.append(b)
            count += _wc(b)
        if cur:
            groups.append(cur)
        for part, group in enumerate(groups, 1):
            body = "\n".join(group)
            header = f"{source}, {u['location']}" + (f": {u['title']}" if u["title"] else "")
            text = f"{header}\n{body}"
            chunks.append({
                "id": _chunk_id("article", source, u["location"], part, text),
                "text": text,
                "source": source, "location": u["location"], "locations": u["location"],
                "title": u["title"], "chapter": u["chapter"],
                "part": part, "parts": len(groups), "design": "article",
            })
    return chunks


def chunk_fixed_design(source: str, units: list[dict]) -> list[dict]:
    """Sliding window over all words of the document; the chunk's location is the unit where it
    starts, `locations` lists every unit it touches (used for hit-rate scoring)."""
    words: list[tuple[str, str]] = []   # (word, location)
    for u in units:
        for b in u["blocks"]:
            words.extend((w, u["location"]) for w in b.split())
    chunks, step, start, n = [], FIXED_WORDS - FIXED_OVERLAP, 0, 1
    while start < len(words):
        window = words[start:start + FIXED_WORDS]
        if len(window) < FIXED_OVERLAP and chunks:      # tail already covered by the overlap
            break
        text = " ".join(w for w, _ in window)
        locs = list(dict.fromkeys(loc for _, loc in window))
        chunks.append({
            "id": _chunk_id("fixed", source, locs[0], n, text),
            "text": text, "source": source, "location": locs[0], "locations": "; ".join(locs),
            "title": "", "chapter": "", "part": n, "parts": 0, "design": "fixed",
        })
        start += step
        n += 1
    return chunks


def chunk_file(path: str | Path, design: str = CHOSEN_DESIGN) -> list[dict]:
    """Extract, clean and chunk one file. Used by main.py index and by the add_document tool."""
    path = Path(path)
    source = LABELS.get(path.stem, path.stem)
    units = load_document(path)
    if design == "fixed":
        return chunk_fixed_design(source, units)
    return chunk_article_design(source, units)


#embedding + storage

_client = None


def _genai():
    global _client
    if _client is None:
        from google import genai
        _client = genai.Client(api_key=load_api_key())
    return _client


_single_mode = True    # gemini-embedding-2 merges a list into ONE vector, so embed one text per call


def _call(contents):
    result = _genai().models.embed_content(model=EMBED_MODEL, contents=contents)
    return [e.values for e in result.embeddings]


def _with_retries(contents) -> list[list[float]]:
    for attempt in range(6):
        try:
            return _call(contents)
        except Exception as error:  # noqa: BLE001
            message = str(error)
            if "429" in message or "RESOURCE_EXHAUSTED" in message:
                if "per day" in message.lower() or "daily" in message.lower():
                    raise QuotaExhausted(message) from error
                wait = 15 * (attempt + 1)
                log(f"rate limited, waiting {wait}s ...")
                time.sleep(wait)
                continue
            if attempt == 5:
                raise
            time.sleep(3)
    raise QuotaExhausted("rate limit did not clear after retries")


def embed_texts(texts: list[str]) -> list[list[float]]:
    """One vector per text. gemini-embedding-2 may merge a list into a single vector, so if the
    batch comes back with the wrong count we switch to one call per text (and stay there)."""
    global _single_mode
    if len(texts) > 1 and not _single_mode:
        vectors = _with_retries(texts)
        if len(vectors) == len(texts):
            return vectors
        log(f"model returned {len(vectors)} vectors for {len(texts)} texts; switching to one call per text")
        _single_mode = True
    out = []
    for text in texts:
        out.append(_with_retries([text])[0])
        time.sleep(0.7)
    return out


class QuotaExhausted(RuntimeError):
    pass


def embed_query(text: str) -> list[float]:
    return embed_texts([text])[0]


def open_collection(design: str = CHOSEN_DESIGN):
    INDEX_DIR.mkdir(exist_ok=True)
    client = chromadb.PersistentClient(path=str(INDEX_DIR))
    return client.get_or_create_collection(f"chunks_{design}", metadata={"hnsw:space": "cosine"})


def embed_and_store(chunks: list[dict], design: str = CHOSEN_DESIGN, budget: int | None = None) -> int:
    """Embed the chunks that have no saved vector yet and store them straight away.
    Returns the number of newly embedded chunks."""
    collection = open_collection(design)
    have = set(collection.get(ids=[c["id"] for c in chunks], include=[])["ids"]) if chunks else set()
    todo = [c for c in chunks if c["id"] not in have]
    done = 0
    for i in range(0, len(todo), EMBED_BATCH):
        batch = todo[i:i + EMBED_BATCH]
        if budget is not None and done + len(batch) > budget:
            batch = batch[: max(budget - done, 0)]
            if not batch:
                raise QuotaExhausted(f"daily budget of {budget} embeddings reached")
        vectors = embed_texts([c["text"] for c in batch])
        collection.add(
            ids=[c["id"] for c in batch],
            embeddings=vectors,
            documents=[c["text"] for c in batch],
            metadatas=[{k: v for k, v in c.items() if k not in ("id", "text")} for c in batch],
        )
        done += len(batch)
        log(f"  [{design}] stored {done}/{len(todo)}")
    return done


def add_file(path: str | Path) -> str:
    """Add-document pipeline: chunk_file -> embed_and_store, with an explicit duplicate policy.

    - same file, nothing changed      -> skipped, nothing is embedded
    - same source name, text changed  -> old chunks of that source are replaced
    - new source                      -> embedded and added
    """
    path = Path(path)
    if not path.is_file():
        return f"File not found: {path}"
    chunks = chunk_file(path, CHOSEN_DESIGN)
    if not chunks:
        return f"No text could be extracted from {path.name}."
    source = chunks[0]["source"]
    collection = open_collection(CHOSEN_DESIGN)
    existing = set(collection.get(where={"source": source}, include=[])["ids"])
    new_ids = {c["id"] for c in chunks}
    if existing and existing == new_ids:
        return f"'{source}' is already indexed ({len(existing)} chunks, unchanged). Nothing was added."
    stale = list(existing - new_ids)
    if stale:
        collection.delete(ids=stale)
    added = embed_and_store(chunks, CHOSEN_DESIGN)
    verb = "Replaced" if existing else "Added"
    return f"{verb} '{source}': {len(chunks)} chunks ({added} newly embedded, {len(stale)} outdated removed)."


#main

def corpus_words(paths: list[Path]) -> None:
    total = 0
    for p in paths:
        units = load_document(p)
        words = sum(_wc(b) for u in units for b in u["blocks"])
        total += words
        log(f"  {LABELS.get(p.stem, p.stem):22s} {len(units):4d} articles  {words:6d} words")
    log(f"  {'TOTAL':22s} {'':4s}           {total:6d} words")


def main() -> None:
    paths = [download(stem, url) for stem, (_, url) in CORPUS.items()]
    log("Corpus (operative part only):")
    corpus_words(paths)

    budget = DAILY_BUDGET
    for design in DESIGNS:
        chunks = [c for p in paths for c in chunk_file(p, design)]
        have = set(open_collection(design).get(include=[])["ids"])
        log(f"design '{design}': {len(chunks)} chunks, {len([c for c in chunks if c['id'] not in have])} to embed")
        try:
            budget -= embed_and_store(chunks, design, budget=budget)
        except QuotaExhausted as error:
            log(f"\nStopped: {error}\nVectors so far are saved. Run `main.py index` again after the quota resets "
                f"(09:00 Spain time) and it will continue where it stopped.")
            sys.exit(0)
    log("\nIndex complete: " + ", ".join(f"{d}={open_collection(d).count()}" for d in DESIGNS))


if __name__ == "__main__":
    main()
