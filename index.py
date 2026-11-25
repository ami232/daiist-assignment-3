"""
Assignment 3: build the index (`main.py index`).

Corpus: the EU rules a student founder of an anonymous campus app has to follow.
  gdpr      Regulation (EU) 2016/679, General Data Protection Regulation
  dsa       Regulation (EU) 2022/2065, Digital Services Act
  eprivacy  Directive 2002/58/EC, consolidated text of 19 Dec 2009 (cookies, traffic data)

Held back on purpose, for the add-document demo (not indexed by `main.py index`):
  tco       Regulation (EU) 2021/784, terrorist content online

Texts come from the EU Publications Office (Cellar) as XHTML. EUR-Lex itself
blocks scripted downloads; Cellar serves the same official text.

Two chunkings ("designs") are built from the same cleaned articles:
  fixed     300-word windows with 50 words overlap, ignoring structure
  article   one chunk per article, split on numbered paragraphs past ~300 words

Vectors are cached in index/vectors.jsonl by text hash, appended after every
batch, so a crash or the daily quota loses nothing and nothing is embedded twice.
"""

from __future__ import annotations

import hashlib
import json
import re
import sys
import time
import urllib.request
from pathlib import Path

import numpy as np
from bs4 import BeautifulSoup

ROOT = Path(__file__).resolve().parent
CORPUS_DIR = ROOT / "corpus"
INDEX_DIR = ROOT / "index"
VECTOR_CACHE = INDEX_DIR / "vectors.jsonl"
EMBED_MODEL = "gemini-embedding-2"
EMBED_DIM = 768
BATCH = 50
DESIGNS = ("fixed", "article")

CELLAR = "https://publications.europa.eu/resource/celex/{celex}"
EURLEX = "https://eur-lex.europa.eu/legal-content/EN/TXT/?uri=CELEX:{celex}"

DOCS = {
    "gdpr": {"celex": "32016R0679", "title": "GDPR, Regulation (EU) 2016/679", "date": "2016-04-27"},
    "dsa": {"celex": "32022R2065", "title": "Digital Services Act, Regulation (EU) 2022/2065", "date": "2022-10-19"},
    "eprivacy": {"celex": "02002L0058-20091219", "title": "ePrivacy Directive 2002/58/EC (consolidated 2009)", "date": "2009-12-19"},
}
EXTRA_DOCS = {
    "tco": {"celex": "32021R0784", "title": "Terrorist Content Online, Regulation (EU) 2021/784", "date": "2021-04-29"},
}


def log(*args) -> None:
    print(*args, file=sys.stderr, flush=True)


# ---------------------------------------------------------------- download

def download(doc_id: str, meta: dict, folder: Path = CORPUS_DIR) -> Path:
    """Fetch one act's English XHTML from Cellar into corpus/<doc_id>.xhtml (skip if present)."""
    folder.mkdir(parents=True, exist_ok=True)
    path = folder / f"{doc_id}.xhtml"
    if path.exists() and path.stat().st_size > 10_000:
        return path
    req = urllib.request.Request(
        CELLAR.format(celex=meta["celex"]),
        headers={"Accept": "application/xhtml+xml", "Accept-Language": "eng"},
    )
    with urllib.request.urlopen(req, timeout=120) as r:
        path.write_bytes(r.read())
    log(f"downloaded {doc_id} ({path.stat().st_size // 1000} kB)")
    return path


# ---------------------------------------------------------------- extract and clean

ARTICLE_ID = re.compile(r"^art_(\d+[a-z]?)$")


def clean_text(text: str) -> str:
    text = text.replace("\xa0", " ")
    text = re.sub(r"[▼▲►◄][A-Z]?\d*", " ", text)        # consolidation markers like ▼M2
    text = re.sub(r"\(\s*\d{1,3}\s*\)(?=\s|$)", lambda m: m.group(0), text)
    text = re.sub(r"[ \t]+", " ", text)
    # a list label "(a)" or "1." on its own line belongs to the next line
    text = re.sub(r"(?m)^\s*(\([a-z0-9ivx]+\)|\d+\.)\s*\n\s*", r"\1 ", text)
    text = re.sub(r"\n\s*\n+", "\n", text)
    return text.strip()


def extract_articles(path: Path) -> list[dict]:
    """Return the act's articles in order: number, title, chapter and paragraphs.

    Works for both EU layouts: the Official Journal (oj-*) and consolidated texts.
    Footnote markers are dropped and table cells holding list labels are joined.
    """
    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    for tag in soup.select(".oj-note-tag, .oj-super, .superscript, .modref, .footnote, .oj-note"):
        tag.decompose()
    for cell in soup.find_all("td"):      # OJ lists are 2-column tables: "(a)" | text
        cell.insert_after(" ")
    articles = []
    for el in soup.find_all(id=ARTICLE_ID):
        number = ARTICLE_ID.match(el["id"]).group(1)
        lines = [l for l in clean_text(el.get_text("\n")).split("\n") if l.strip()]
        if not lines:
            continue
        # first line is "Article N", next is the subtitle
        body = lines[1:] if re.match(r"^Article\s+\d", lines[0]) else lines
        title = body[0] if body and not re.match(r"^\d+\.", body[0]) and len(body[0].split()) < 20 else ""
        if title:
            body = body[1:]
        chapter = ""
        parent = el.find_parent(id=re.compile(r"^cpt_"))
        if parent is not None:
            t = parent.find(class_="eli-title")
            chapter = " ".join(t.get_text(" ", strip=True).split()) if t else parent["id"]
        paragraphs = split_paragraphs(" \n".join(body))
        articles.append({"article": number, "title": title, "chapter": chapter, "paragraphs": paragraphs})
    return articles


def split_paragraphs(text: str) -> list[tuple[str, str]]:
    """Split article text on numbered paragraphs '1.', '2.' at line starts -> [(num, text)]."""
    parts = re.split(r"(?m)^\s*(\d{1,2})\.\s+", text)
    if len(parts) == 1:
        return [("", " ".join(text.split()))]
    out = []
    if parts[0].strip():
        out.append(("", " ".join(parts[0].split())))
    for num, chunk in zip(parts[1::2], parts[2::2]):
        out.append((num, " ".join(chunk.split())))
    return out


# ---------------------------------------------------------------- chunk

def _loc(article: str, paras: list[str]) -> str:
    nums = [p for p in paras if p]
    if not nums:
        return f"Article {article}"
    return f"Article {article}({nums[0]})" if len(nums) == 1 else f"Article {article}({nums[0]})-({nums[-1]})"


def chunk_articles(doc_id: str, title: str, articles: list[dict], max_words: int = 300) -> list[dict]:
    """Design 'article': one chunk per article; long articles split on paragraph boundaries."""
    chunks = []
    for a in articles:
        groups, cur, cur_words = [], [], 0
        pieces = []
        for num, text in a["paragraphs"]:      # a single huge paragraph (e.g. definitions) is cut in windows
            w = text.split()
            if len(w) <= max_words:
                pieces.append((num, text))
            else:
                for s in range(0, len(w), max_words - 30):
                    pieces.append((num, " ".join(w[s:s + max_words])))
        for num, text in pieces:
            n = len(text.split())
            if cur and cur_words + n > max_words:
                groups.append(cur)
                cur, cur_words = [], 0
            cur.append((num, text))
            cur_words += n
        if cur:
            groups.append(cur)
        for g in groups:
            paras = [num for num, _ in g]
            body = " ".join(f"{num}. {t}" if num else t for num, t in g)
            loc = _loc(a["article"], paras) if len(groups) > 1 else f"Article {a['article']}"
            header = f"{title}. Article {a['article']}: {a['title']}."
            chunks.append({
                "source": doc_id, "location": loc, "articles": [a["article"]],
                "chapter": a["chapter"], "text": f"{header}\n{body}",
            })
    return _with_ids(chunks, "article")


def chunk_fixed(doc_id: str, title: str, articles: list[dict], size: int = 300, overlap: int = 50) -> list[dict]:
    """Design 'fixed': sliding word windows over the whole act, blind to article boundaries."""
    words, owner = [], []
    for a in articles:
        tokens = f"Article {a['article']} {a['title']}".split()
        for _, text in a["paragraphs"]:
            tokens += text.split()
        words += tokens
        owner += [a["article"]] * len(tokens)
    chunks, start = [], 0
    while start < len(words):
        end = min(start + size, len(words))
        arts = list(dict.fromkeys(owner[start:end]))
        loc = f"Article {arts[0]}" if len(arts) == 1 else f"Articles {arts[0]}-{arts[-1]}"
        chunks.append({
            "source": doc_id, "location": loc, "articles": arts, "chapter": "",
            "text": f"{title}.\n" + " ".join(words[start:end]),
        })
        if end == len(words):
            break
        start = end - overlap
    return _with_ids(chunks, "fixed")


def _with_ids(chunks: list[dict], design: str) -> list[dict]:
    for i, c in enumerate(chunks):
        c["design"] = design
        c["id"] = f"{c['source']}-{design}-{i:04d}"
        c["hash"] = text_hash(c["text"])
        c["words"] = len(c["text"].split())
    return chunks


def chunk_file(path: str | Path, doc_id: str | None = None, title: str | None = None) -> dict[str, list[dict]]:
    """Run one file through extraction and both chunkings. Used by server.py's add_document.

    Supports EU XHTML/HTML (article structure) and plain .txt/.md (paragraph blocks
    treated as one 'article' each).
    """
    path = Path(path)
    doc_id = doc_id or re.sub(r"[^a-z0-9]+", "-", path.stem.lower()).strip("-")
    meta = {**DOCS, **EXTRA_DOCS}.get(doc_id, {})
    title = title or meta.get("title") or path.stem
    if path.suffix.lower() in {".xhtml", ".html", ".htm"}:
        articles = extract_articles(path)
    else:
        blocks = [b for b in re.split(r"\n\s*\n", path.read_text(encoding="utf-8")) if b.strip()]
        articles = [{"article": str(i + 1), "title": "", "chapter": "", "paragraphs": [("", " ".join(b.split()))]}
                    for i, b in enumerate(blocks)]
    if not articles:
        raise ValueError(f"No text found in {path}")
    return {
        "fixed": chunk_fixed(doc_id, title, articles),
        "article": chunk_articles(doc_id, title, articles),
    }


# ---------------------------------------------------------------- embed and store

def text_hash(text: str) -> str:
    return hashlib.sha1(text.encode("utf-8")).hexdigest()[:16]


def load_vector_cache() -> dict[str, list[float]]:
    cache = {}
    if VECTOR_CACHE.exists():
        for line in VECTOR_CACHE.read_text(encoding="utf-8").splitlines():
            if line.strip():
                row = json.loads(line)
                cache[row["h"]] = row["v"]
    return cache


_client = None


def client():
    global _client
    if _client is None:
        from google import genai
        from api_key import load_api_key
        _client = genai.Client(api_key=load_api_key())
    return _client


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Embed a batch with Gemini; retries on rate limits. Each text is its own Content."""
    from google.genai import types
    contents = [types.Content(parts=[types.Part(text=t)]) for t in texts]
    for attempt in range(6):
        try:
            r = client().models.embed_content(
                model=EMBED_MODEL, contents=contents,
                config=types.EmbedContentConfig(output_dimensionality=EMBED_DIM),
            )
            return [normalise(e.values) for e in r.embeddings]
        except Exception as e:  # noqa: BLE001
            msg = str(e)
            if ("429" in msg or "RESOURCE_EXHAUSTED" in msg) and "per day" not in msg.lower() and attempt < 5:
                wait = 20 * (attempt + 1)
                log(f"rate limited, waiting {wait}s")
                time.sleep(wait)
                continue
            raise
    raise RuntimeError("embedding failed")


def normalise(v) -> list[float]:
    a = np.asarray(v, dtype=np.float32)
    a = a / (np.linalg.norm(a) or 1.0)
    return [round(float(x), 5) for x in a]


def embed_and_store(chunks: list[dict]) -> int:
    """Embed only chunks whose text has no cached vector; append each batch to the cache."""
    cache = load_vector_cache()
    todo, seen = [], set()
    for c in chunks:
        if c["hash"] not in cache and c["hash"] not in seen:
            todo.append(c)
            seen.add(c["hash"])
    INDEX_DIR.mkdir(exist_ok=True)
    for i in range(0, len(todo), BATCH):
        batch = todo[i:i + BATCH]
        vectors = embed_texts([c["text"] for c in batch])
        with VECTOR_CACHE.open("a", encoding="utf-8") as f:
            for c, v in zip(batch, vectors):
                f.write(json.dumps({"h": c["hash"], "v": v}) + "\n")
        log(f"embedded {min(i + BATCH, len(todo))}/{len(todo)}")
    return len(todo)


def write_design(design: str, chunks: list[dict]) -> None:
    path = INDEX_DIR / f"chunks_{design}.jsonl"
    with path.open("w", encoding="utf-8") as f:
        for c in chunks:
            f.write(json.dumps(c, ensure_ascii=False) + "\n")


def read_design(design: str) -> list[dict]:
    path = INDEX_DIR / f"chunks_{design}.jsonl"
    if not path.exists():
        return []
    return [json.loads(l) for l in path.read_text(encoding="utf-8").splitlines() if l.strip()]


def write_manifest(entries: dict) -> None:
    (INDEX_DIR / "documents.json").write_text(json.dumps(entries, indent=2), encoding="utf-8")


def read_manifest() -> dict:
    p = INDEX_DIR / "documents.json"
    return json.loads(p.read_text(encoding="utf-8")) if p.exists() else {}


def file_hash(path: Path) -> str:
    return hashlib.sha1(path.read_bytes()).hexdigest()


def main() -> None:
    INDEX_DIR.mkdir(exist_ok=True)
    manifest = read_manifest()
    all_chunks = {d: [] for d in DESIGNS}
    stats = []
    for doc_id, meta in DOCS.items():
        path = download(doc_id, meta)
        per_design = chunk_file(path, doc_id, meta["title"])
        words = sum(len(p[1].split()) for a in extract_articles(path) for p in a["paragraphs"])
        for d in DESIGNS:
            all_chunks[d] += per_design[d]
        manifest[doc_id] = {
            "title": meta["title"], "url": EURLEX.format(celex=meta["celex"]), "date": meta["date"],
            "licence": "EU legal acts, free reuse with attribution (Commission Decision 2011/833/EU)",
            "file": path.name, "sha1": file_hash(path), "words": words,
            "chunks": {d: len(per_design[d]) for d in DESIGNS},
        }
        stats.append((doc_id, words, {d: len(per_design[d]) for d in DESIGNS}))
    # keep chunks of documents added later through add_document
    for d in DESIGNS:
        extra = [c for c in read_design(d) if c["source"] not in DOCS]
        all_chunks[d] += extra
        write_design(d, all_chunks[d])
    write_manifest(manifest)
    for doc_id, words, n in stats:
        log(f"{doc_id:9s} {words:6d} words  chunks {n}")
    log(f"total words {sum(s[1] for s in stats)}")
    for d in DESIGNS:
        new = embed_and_store(all_chunks[d])
        log(f"design {d}: {len(all_chunks[d])} chunks, {new} newly embedded")
    print("index built:", {d: len(all_chunks[d]) for d in DESIGNS})


if __name__ == "__main__":
    main()
