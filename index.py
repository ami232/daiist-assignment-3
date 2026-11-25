"""Build the index (`main.py index`). The per-file steps are functions that server.py's add_document imports.

    uv run python main.py index                       # download corpus if missing, embed article chunks
    uv run python index.py --designs article,fixed    # also the fixed-window baseline (needs more quota)
    uv run python index.py --stats                    # words / sections / chunks per document, no API calls
"""
from __future__ import annotations

import argparse
import hashlib
import sys
from pathlib import Path

from chunking import Chunk, make_chunks, parse_file, word_count
from config import CORPUS_DIR
from embed import QuotaExhausted, embed
from store import collection, log

EXTS = {".html", ".htm", ".txt", ".md", ".pdf"}


def file_sha(path: Path) -> str:
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()[:16]


def chunk_file(path: str | Path, kind: str = "article") -> tuple[str, list[Chunk], int]:
    """Extract, clean and chunk one file. Returns (doc_id, chunks, word_count). No API calls."""
    doc_id, title, secs = parse_file(path)
    if not secs:
        raise ValueError(f"no text could be extracted from {Path(path).name}")
    return doc_id, make_chunks(kind, doc_id, title, secs), word_count(secs)


def embed_and_store(chunks: list[Chunk], kind: str, doc_sha: str, batch: int = 50) -> int:
    """Embed only chunks that have no saved vector (same id and same text hash).
    Each batch is written to ChromaDB before the next is requested, so a crash or the daily
    quota loses nothing. Returns the number of chunks newly embedded."""
    col = collection(kind)
    ids = [f"{c.doc_id}|{kind}|{i:04d}" for i, c in enumerate(chunks)]
    have: dict[str, str | None] = {}
    for i in range(0, len(ids), 500):
        r = col.get(ids=ids[i:i + 500], include=["metadatas"])
        have.update({i_: m.get("text_hash") for i_, m in zip(r["ids"], r["metadatas"])})
    todo = [(i, c) for i, c in zip(ids, chunks) if have.get(i) != c.text_hash]
    for s in range(0, len(todo), batch):
        part = todo[s:s + batch]
        vecs = embed([c.text for _, c in part])
        col.upsert(
            ids=[i for i, _ in part], embeddings=vecs, documents=[c.text for _, c in part],
            metadatas=[dict(doc_id=c.doc_id, doc_title=c.doc_title, location=c.location,
                            locs=" | ".join(c.base_locs), chapter=c.chapter, title=c.title,
                            text_hash=c.text_hash, doc_sha=doc_sha) for _, c in part])
        log(f"  [{kind}] embedded {min(s + batch, len(todo))}/{len(todo)}")
    return len(todo)


def index_document(path: str | Path, kinds: tuple[str, ...] = ("article",)) -> dict:
    """chunk_file + embed_and_store for one file: used by this script AND by the MCP add_document tool.

    Already indexed?  same content (sha256)  -> 'unchanged', nothing embedded (idempotent)
                      different content      -> 'replaced': that doc_id's old chunks are deleted first,
                                                so a corrected document never leaves stale passages behind."""
    p = Path(path)
    sha = file_sha(p)
    result = dict(doc_id="", words=0, status="added", chunks={}, embedded={})
    for kind in kinds:
        doc_id, chunks, words = chunk_file(p, kind)
        result.update(doc_id=doc_id, words=words)
        col = collection(kind)
        old = col.get(where={"doc_id": doc_id}, include=["metadatas"])
        replaced = bool(old["ids"]) and any(m.get("doc_sha") != sha for m in old["metadatas"])
        if replaced:
            col.delete(ids=old["ids"])
            result["status"] = "replaced"
        n = embed_and_store(chunks, kind, sha)
        result["chunks"][kind], result["embedded"][kind] = len(chunks), n
        if old["ids"] and not replaced and n == 0:
            result["status"] = "unchanged"
    return result


def corpus_files() -> list[Path]:
    return sorted(p for p in CORPUS_DIR.glob("*") if p.suffix.lower() in EXTS)


def stats() -> None:
    total = 0
    for p in corpus_files():
        doc_id, title, secs = parse_file(p)
        n = {k: len(make_chunks(k, doc_id, title, secs)) for k in ("article", "fixed")}
        w = word_count(secs)
        total += w
        print(f"{doc_id:10s} {w:8d} words  {len(secs):4d} sections  chunks={n}")
    print(f"TOTAL {total} words in {len(corpus_files())} documents (need >= 50000 and >= 3)")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--designs", default="article", help="comma-separated: article,fixed")
    ap.add_argument("--stats", action="store_true")
    a = ap.parse_args()
    if not corpus_files():
        print("corpus/ is empty: downloading from EUR-Lex ...")
        from fetch_corpus import fetch_all
        fetch_all()
    if a.stats:
        return stats()
    files = corpus_files()
    if not files:
        sys.exit("No corpus files. See fetch_corpus.py for how to save them by hand.")
    try:
        for p in files:
            r = index_document(p, tuple(a.designs.split(",")))
            print(f"{p.name}: {r['status']}  words={r['words']}  chunks={r['chunks']}  newly embedded={r['embedded']}")
    except QuotaExhausted as e:
        sys.exit(f"{e}\nEverything embedded so far is saved in index/. Re-run when the quota resets (09:00 Spain).")


if __name__ == "__main__":
    main()
