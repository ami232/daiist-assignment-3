"""
Assignment 3: build the index (`uv run python main.py index`).

1. Download the corpus (EU drone regulations, official XHTML from the EU Publications Office) into
   corpus/ (git-ignored).
2. Extract and clean the text, keeping where every passage comes from (article / annex section).
3. Chunk it two ways (two index designs, compared in evaluate.py):
     structure : one chunk per article or annex section; long ones split into ~220-word windows
                 (40-word overlap); every chunk starts with its citation header.
     fixed     : the plain text cut into 200-word windows (30-word overlap), ignoring structure.
4. Embed with Gemini (gemini-embedding-2, 768 dims) and store in index/ (ChromaDB + a vector cache).
   Every vector is saved as soon as it arrives; reruns embed only chunks without a saved vector.

server.py's add_document tool imports chunk_file() and embed_and_store() from here.
"""

from __future__ import annotations

import hashlib
import html
import json
import re
import urllib.request
from pathlib import Path

from rag import CORPUS_DIR, INDEX_DESIGNS, INDEX_DIR, collection, embed, log

# The corpus: official texts, © European Union, reuse authorised (Commission Decision 2011/833/EU).
CORPUS = [
    {"celex": "32019R0947", "source": "Regulation (EU) 2019/947",
     "title": "Commission Implementing Regulation (EU) 2019/947 on the rules and procedures for the operation of unmanned aircraft",
     "date": "2019-05-24"},
    {"celex": "32019R0945", "source": "Regulation (EU) 2019/945",
     "title": "Commission Delegated Regulation (EU) 2019/945 on unmanned aircraft systems and on third-country operators of unmanned aircraft systems",
     "date": "2019-03-12"},
    {"celex": "32020R1058", "source": "Regulation (EU) 2020/1058",
     "title": "Commission Delegated Regulation (EU) 2020/1058 amending Delegated Regulation (EU) 2019/945 (classes C5 and C6)",
     "date": "2020-04-27"},
    {"celex": "32021R0664", "source": "Regulation (EU) 2021/664",
     "title": "Commission Implementing Regulation (EU) 2021/664 on a regulatory framework for the U-space",
     "date": "2021-04-22"},
]
# Not in the initial index: added later through the MCP add_document tool (see REPORT.md).
LATER_DOCUMENT = {"celex": "32020R0639", "source": "Regulation (EU) 2020/639",
                  "title": "Commission Implementing Regulation (EU) 2020/639 amending Implementing Regulation (EU) 2019/947 (standard scenarios)",
                  "date": "2020-05-12"}

CELLAR = "http://publications.europa.eu/resource/celex/{celex}"
EURLEX = "https://eur-lex.europa.eu/eli/reg/{year}/{num}/oj/eng"
STRUCT_MAX, STRUCT_WIN, STRUCT_OVERLAP = 300, 220, 40
FIXED_WIN, FIXED_OVERLAP = 200, 30


def source_meta(celex: str) -> dict:
    for d in CORPUS + [LATER_DOCUMENT]:
        if d["celex"] == celex:
            return d
    return {"celex": celex, "source": celex, "title": celex, "date": ""}


def url_for(celex: str) -> str:
    m = re.match(r"3(\d{4})R(\d{4})", celex)
    return EURLEX.format(year=m.group(1), num=int(m.group(2))) if m else ""


def download(doc: dict) -> Path:
    """Fetch the official English XHTML (EUR-Lex itself blocks scripted downloads; the Publications
    Office cellar serves the same document)."""
    CORPUS_DIR.mkdir(exist_ok=True)
    path = CORPUS_DIR / f"{doc['celex']}.xhtml"
    if path.exists() and path.stat().st_size > 1000:
        return path
    req = urllib.request.Request(CELLAR.format(celex=doc["celex"]),
                                 headers={"Accept": "application/xhtml+xml", "Accept-Language": "eng"})
    with urllib.request.urlopen(req, timeout=120) as r:
        path.write_bytes(r.read())
    log(f"downloaded {doc['celex']} ({path.stat().st_size // 1024} KB)")
    return path


# ----------------------------------------------------------------------------- extraction
def _clean(text: str) -> str:
    text = html.unescape(text).replace("\xa0", " ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def extract_eurlex(path: Path) -> list[dict]:
    """Return ordered blocks {location, heading, text} from an EUR-Lex (Formex-converted) XHTML file.

    Fix for the main extraction problem: list items are laid out as two-cell table rows, with the
    label '(a)' in one cell and its text in the other. Extracting paragraph by paragraph separates
    every label from its sentence, so each innermost table row is joined into one line instead.
    Footnotes (OJ references) and the signature block are dropped.
    """
    from bs4 import BeautifulSoup

    soup = BeautifulSoup(path.read_text(encoding="utf-8"), "html.parser")
    blocks: list[dict] = []
    article = annex = section = None
    art_title = ""
    in_recitals = False
    stopped = False  # after "Done at Brussels" until the next annex
    done_rows = set()

    def loc() -> tuple[str, str]:
        if annex:
            return (f"{annex}" + (f", {section}" if section else ""), "")
        if article:
            return (article, art_title)
        return ("Recitals" if in_recitals else "Preamble", "")

    for p in soup.find_all("p"):
        cls = " ".join(p.get("class", []))
        text = _clean(p.get_text(" "))
        if not text or "oj-note" in cls or cls.startswith("oj-hd") or "oj-signatory" in cls:
            continue
        if "oj-doc-ti" in cls:
            if text.upper().startswith("ANNEX") or text.upper().startswith("APPENDIX"):
                word, _, rest = text.partition(" ")
                annex, section, stopped = (word.title() + (" " + rest.upper() if rest else "")).strip(), None, False
            elif annex:
                section = text
            continue
        if "oj-ti-art" in cls:
            article, art_title, stopped = text, "", False
            continue
        if "oj-sti-art" in cls:
            art_title = text
            continue
        if re.search(r"oj-ti-(grseq|section)", cls):
            if annex:
                section = text
            continue
        if text.startswith("Whereas"):
            in_recitals = True
            continue
        if text.startswith("Done at Brussels") or text.startswith("This Regulation shall be binding"):
            if text.startswith("Done at"):
                stopped = True
            if text.startswith("This Regulation shall be binding"):
                location, title = loc()
                blocks.append({"location": location, "heading": title, "text": text})
            continue
        if stopped:
            continue
        tr = p.find_parent("tr")
        if tr is not None:
            if id(tr) in done_rows:
                continue
            done_rows.add(id(tr))
            # Take every text node that belongs to this row itself (not to a nested table). Some rows
            # put their text directly in the <td> without a <p>, so reading only <p> elements loses it.
            strings = [s for s in tr.find_all(string=True)
                       if s.find_parent("tr") is tr
                       and not (s.find_parent("p") and "oj-note" in " ".join(s.find_parent("p").get("class", [])))]
            text = _clean(" ".join(strings))
            if not text:
                continue
        location, title = loc()
        blocks.append({"location": location, "heading": title, "text": text})
    return blocks


def extract_generic(path: Path) -> list[dict]:
    """Fallback for files added later that are not EUR-Lex XHTML: PDF (location = page), HTML or text
    (location = nearest heading)."""
    suffix = path.suffix.lower()
    if suffix == ".pdf":
        from pypdf import PdfReader

        return [{"location": f"page {i + 1}", "heading": "", "text": _clean(pg.extract_text() or "")}
                for i, pg in enumerate(PdfReader(str(path)).pages) if (pg.extract_text() or "").strip()]
    raw = path.read_text(encoding="utf-8", errors="replace")
    if suffix in {".html", ".htm", ".xhtml"}:
        from bs4 import BeautifulSoup

        soup = BeautifulSoup(raw, "html.parser")
        blocks, heading = [], "Document"
        for el in soup.find_all(["h1", "h2", "h3", "h4", "p", "li"]):
            t = _clean(el.get_text(" "))
            if not t:
                continue
            if el.name.startswith("h"):
                heading = t
            else:
                blocks.append({"location": heading, "heading": "", "text": t})
        return blocks
    blocks, heading = [], "Document"
    for para in re.split(r"\n\s*\n", raw):
        t = _clean(para)
        if not t:
            continue
        if para.lstrip().startswith("#"):
            heading = t.lstrip("# ")
            continue
        blocks.append({"location": heading, "heading": "", "text": t})
    return blocks


def extract(path: Path) -> list[dict]:
    head = path.read_bytes()[:3000].decode("utf-8", errors="ignore")
    if path.suffix.lower() in {".xhtml", ".html", ".htm"} and "oj-" in path.read_text(encoding="utf-8", errors="ignore"):
        return extract_eurlex(path)
    return extract_generic(path)


# ----------------------------------------------------------------------------- chunking
def _windows(words: list[str], win: int, overlap: int) -> list[tuple[int, int]]:
    if len(words) <= win:
        return [(0, len(words))]
    out, start = [], 0
    while start < len(words):
        end = min(start + win, len(words))
        out.append((start, end))
        if end == len(words):
            break
        start = end - overlap
    return out


def doc_id_for(path: Path) -> str:
    m = re.search(r"3\d{4}R\d{4}", path.name)
    return m.group(0) if m else re.sub(r"[^A-Za-z0-9_-]", "_", path.stem)


def chunk_file(path: str | Path, design: str = "structure", origin: str = "corpus") -> list[dict]:
    """Extract, clean and chunk one file. Each chunk: id, text, and metadata
    (source, doc_id, location, url, design, origin, words, content_hash)."""
    path = Path(path)
    doc_id = doc_id_for(path)
    meta = source_meta(doc_id)
    source = meta["source"] if meta["source"] != doc_id else path.stem
    content_hash = hashlib.sha256(path.read_bytes()).hexdigest()[:16]
    blocks = extract(path)
    base = {"source": source, "doc_id": doc_id, "url": url_for(doc_id), "design": design,
            "origin": origin, "content_hash": content_hash}
    chunks: list[dict] = []

    if design == "structure":
        groups: list[dict] = []
        for b in blocks:
            if groups and groups[-1]["location"] == b["location"]:
                groups[-1]["texts"].append(b["text"])
            else:
                groups.append({"location": b["location"], "heading": b["heading"], "texts": [b["text"]]})
        for g in groups:
            header = f"{source}, {g['location']}" + (f" ({g['heading']})" if g["heading"] else "")
            words = " ".join(g["texts"]).split()
            spans = [(0, len(words))] if len(words) <= STRUCT_MAX else _windows(words, STRUCT_WIN, STRUCT_OVERLAP)
            for j, (a, b) in enumerate(spans):
                part = f" (part {j + 1}/{len(spans)})" if len(spans) > 1 else ""
                chunks.append({**base, "location": g["location"] + part, "covers": g["location"],
                               "text": f"{header}{part}: " + " ".join(words[a:b])})
    elif design == "fixed":
        words, locs = [], []
        for b in blocks:
            w = b["text"].split()
            words += w
            locs += [b["location"]] * len(w)
        for a, b in _windows(words, FIXED_WIN, FIXED_OVERLAP):
            first, last = locs[a], locs[b - 1]
            location = first if first == last else f"{first} to {last}"
            covers = "; ".join(dict.fromkeys(locs[a:b]))
            chunks.append({**base, "location": location, "covers": covers, "text": " ".join(words[a:b])})
    else:
        raise ValueError(f"unknown design {design!r}")

    for i, c in enumerate(chunks):
        c["id"] = f"{doc_id}-{design[0]}{i:04d}"
        c["words"] = len(c["text"].split())
    return chunks


def embed_and_store(chunks: list[dict], design: str) -> int:
    """Embed chunks (reusing saved vectors) and upsert them into the design's Chroma collection."""
    if not chunks:
        return 0
    vecs = embed([c["text"] for c in chunks], task="RETRIEVAL_DOCUMENT")
    col = collection(design)
    meta_keys = ("source", "doc_id", "location", "covers", "url", "design", "origin", "words", "content_hash")
    col.upsert(ids=[c["id"] for c in chunks], embeddings=vecs, documents=[c["text"] for c in chunks],
               metadatas=[{k: c[k] for k in meta_keys} for c in chunks])
    return len(chunks)


def indexed_docs(design: str) -> dict[str, str]:
    """doc_id -> content_hash for documents already in a collection."""
    got = collection(design).get(include=["metadatas"])
    return {m["doc_id"]: m["content_hash"] for m in got["metadatas"]}


SUPPORTED_SUFFIXES = {".xhtml", ".html", ".htm", ".pdf", ".txt", ".md"}


def add_file(path: str | Path, design: str | None = None) -> str:
    """Index one new file into the active design (used by server.py's add_document tool).

    Policy for documents that are already indexed (matched by document id, e.g. the CELEX number):
    - same content hash  -> nothing is done (no tokens spent, no duplicates);
    - different content  -> treated as a new version: the old chunks are deleted, the new ones stored.
    """
    from rag import ACTIVE_DESIGN, SEARCH_DESIGNS

    path = Path(path)
    design = design or SEARCH_DESIGNS[ACTIVE_DESIGN][0]
    doc_id = doc_id_for(path)
    content_hash = hashlib.sha256(path.read_bytes()).hexdigest()[:16]
    col = collection(design)
    existing = col.get(where={"doc_id": doc_id}, include=["metadatas"])
    if existing["ids"]:
        old_hash = existing["metadatas"][0].get("content_hash")
        if old_hash == content_hash:
            return (f"Already indexed: {doc_id} ({len(existing['ids'])} chunks, same content). "
                    f"Nothing was added or re-embedded.")
        col.delete(ids=existing["ids"])
        action = f"Replaced a previous version of {doc_id} ({len(existing['ids'])} old chunks removed). "
    else:
        action = ""
    chunks = chunk_file(path, design, origin="added")
    n = embed_and_store(chunks, design)
    locs = list(dict.fromkeys(c["covers"] for c in chunks))
    return (f"{action}Added {chunks[0]['source'] if chunks else doc_id}: {n} chunks embedded and stored in the "
            f"'{design}' index. Sections include: {'; '.join(locs[:8])}{' ...' if len(locs) > 8 else ''}")


def main() -> None:
    INDEX_DIR.mkdir(exist_ok=True)
    stats = {"documents": [], "designs": {}}
    paths = [download(d) for d in CORPUS]
    for d, p in zip(CORPUS, paths):
        words = sum(len(b["text"].split()) for b in extract(p))
        stats["documents"].append({**d, "url": url_for(d["celex"]), "words": words,
                                   "licence": "© European Union; reuse authorised (Commission Decision 2011/833/EU)"})
    for design in INDEX_DESIGNS:
        chunks = [c for p in paths for c in chunk_file(p, design)]
        col = collection(design)
        got = col.get(include=["documents", "metadatas"])
        stored = {i: d for i, d, m in zip(got["ids"], got["documents"], got["metadatas"]) if m.get("origin") == "corpus"}
        new = [c for c in chunks if stored.get(c["id"]) != c["text"]]
        embed_and_store(new, design)  # vectors for unchanged texts come from the cache, not the API
        stale = set(stored) - {c["id"] for c in chunks}
        if stale:
            col.delete(ids=sorted(stale))
        (INDEX_DIR / f"chunks_{design}.jsonl").write_text(
            "\n".join(json.dumps({k: v for k, v in c.items()}) for c in chunks) + "\n", encoding="utf-8")
        wc = [c["words"] for c in chunks]
        stats["designs"][design] = {"chunks": len(chunks), "mean_words": round(sum(wc) / len(wc), 1),
                                    "max_words": max(wc), "min_words": min(wc)}
        log(f"{design}: {len(chunks)} chunks ({len(new)} new), mean {stats['designs'][design]['mean_words']} words")
    stats["total_words"] = sum(d["words"] for d in stats["documents"])
    (INDEX_DIR / "manifest.json").write_text(json.dumps(stats, indent=2), encoding="utf-8")
    print(json.dumps({"total_words": stats["total_words"], **{k: v["chunks"] for k, v in stats["designs"].items()}}))


if __name__ == "__main__":
    main()
